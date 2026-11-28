"""The paper log: every paper considered as a source, with its verdict.

    python -m dentamech.paper_log lookup PAPER          # every row for a paper; exit 1 if none
    python -m dentamech.paper_log add PAPER VERDICT --note "..." [--record STEM] [--apply]
    python -m dentamech.paper_log validate [FILE]
    python -m dentamech.paper_log check-append --base REV     # earlier rows unchanged; new rows' links exist
    python -m dentamech.paper_log coverage --base REV FILE...  # new citations with no log row (advisory)
    python -m dentamech.paper_log check-cited                 # each citation's newest row is ACCEPT (QC gate)
    python -m dentamech.paper_log migrate [--apply]           # rewrite a log keyed by a bare `doi` column

PAPER is a DOI (bare, `DOI:`, `doi:` or a doi.org URL) or a PubMed id
(`PMID:NNN`). A PMID whose cached reference has a DOI is keyed by that DOI, so a
paper never has two keys; a paper with no DOI is keyed `PMID:NNN`.

The data model is `schema/paper_log.yaml`. The data is `curation/paper_log.tsv`:
one `PaperLogEntry` per row, the schema's slot names as the header, `|` between
values of a multivalued column. The file is append-only; the newest row for a
paper is its current verdict.

A row's `records` and `history` must exist when the row is written (`add`, and
`check-append` for rows new since the base). They are not rechecked later: a
record can be renamed, merged or removed, and an append-only row cannot follow it.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import re
import subprocess
import sys
from functools import cache
from pathlib import Path

from linkml_runtime.utils.schemaview import SchemaView

from .paths import PAPER_LOG_PATH, PAPER_LOG_SCHEMA_PATH, RECORDS_DIR, REPO_ROOT
from .validate import load, loads, schema_errors

ENTRY_CLASS = "PaperLogEntry"
LOG_CLASS = "PaperLog"
MULTI_SEP = "|"
_DOI_PREFIX = re.compile(r"^(?:doi:|https?://(?:dx\.)?doi\.org/)", re.IGNORECASE)
_PMID = re.compile(r"^(?:pmid:\s*)?0*([1-9][0-9]*)$", re.IGNORECASE)
LITERATURE = ("DOI", "PMID")
# The header before #73, when rows were keyed by a bare DOI.
LEGACY_COLUMNS = ("doi", "considered_on", "verdict", "note", "records", "history")


@cache
def _view() -> SchemaView:
    return SchemaView(str(PAPER_LOG_SCHEMA_PATH))


@cache
def columns() -> tuple[str, ...]:
    """The TSV header: the entry class's slots, in schema order."""
    return tuple(_view().class_slots(ENTRY_CLASS))


@cache
def multivalued() -> frozenset[str]:
    view = _view()
    return frozenset(s for s in columns() if view.induced_slot(s, ENTRY_CLASS).multivalued)


@cache
def verdicts() -> tuple[str, ...]:
    return tuple(_view().get_enum("PaperVerdictEnum").permissible_values)


def normalize_doi(value: str) -> str:
    """Bare, lower-case DOI: `DOI:10.1016/J.X` and `https://doi.org/10.1016/j.x` both give `10.1016/j.x`."""
    return _DOI_PREFIX.sub("", value.strip()).strip().lower()


def canonical(value: str) -> str:
    """A paper's key in canonical form, without consulting the cache.

    `10.1016/J.X`, `doi:10.1016/j.x` and `https://doi.org/10.1016/j.x` give
    `DOI:10.1016/j.x`; `PMID:0123` and `pmid:123` give `PMID:123`. Anything else
    comes back stripped and unchanged, for the schema to reject.
    """
    text = value.strip()
    pmid = _PMID.match(text)
    if pmid and text.lower().startswith("pmid:"):
        return f"PMID:{pmid.group(1)}"
    bare = normalize_doi(text)
    if bare.startswith("10."):
        return f"DOI:{bare}"
    return text


def is_cached(reference: str) -> bool:
    """Whether a reference has a file in the reference cache."""
    from .validate import _fetcher  # the validator's own cache naming

    try:
        return _fetcher().get_cache_path(reference).is_file()
    except (OSError, ValueError):
        return False


def uncached_pmid_error(paper: str) -> str | None:
    """Why a PMID can't be logged yet, or None.

    An uncached PMID can't be resolved to its DOI, so logging it would key a
    paper that has a DOI as `PMID:NNN`, and the paper would have two keys.
    """
    key = canonical(paper)
    if key.startswith("PMID:") and not is_cached(key):
        return (f"{key} is not in the reference cache, so its DOI (if it has one) is unknown and the "
                f"paper could end up with two keys. Fetch it first: just fetch-reference {key}")
    return None


def paper_key(value: str) -> str:
    """The key a paper is logged under: its DOI when one is known, else its PMID.

    A PMID is resolved through the committed reference cache, so this works
    offline; a PMID that is not cached, or whose cached record has no DOI,
    stays `PMID:NNN`.
    """
    key = canonical(value)
    if key.startswith("PMID:"):
        doi = doi_for(key)
        if doi:
            return f"DOI:{doi}"
    return key


def _to_entry(row: dict[str, str]) -> dict:
    entry: dict = {}
    for col in columns():
        raw = (row.get(col) or "").strip()
        if not raw:
            continue
        if col in multivalued():
            entry[col] = [v.strip() for v in raw.split(MULTI_SEP) if v.strip()]
        else:
            entry[col] = raw
    return entry


def _to_row(entry: dict) -> str:
    cells = []
    for col in columns():
        value = entry.get(col, "")
        if isinstance(value, list):
            value = MULTI_SEP.join(value)
        cells.append(str(value))
    return "\t".join(cells)


def read(path: Path | None = None) -> tuple[list[tuple[int, dict]], list[str]]:
    """(line number, entry) for every data row, and any errors in the file's shape."""
    path = path or PAPER_LOG_PATH
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines:
        return [], [f"{path}: empty; the header must be {chr(9).join(columns())!r}"]
    header = lines[0].split("\t")
    if tuple(header) != columns():
        return [], [f"line 1: header {header} is not the schema's columns {list(columns())}"]
    entries, errors = [], []
    reader = csv.reader(lines[1:], delimiter="\t", quoting=csv.QUOTE_NONE)
    for lineno, cells in enumerate(reader, start=2):
        if not any(c.strip() for c in cells):
            errors.append(f"line {lineno}: blank line")
            continue
        if len(cells) != len(columns()):
            errors.append(f"line {lineno}: {len(cells)} columns, expected {len(columns())}")
            continue
        entries.append((lineno, _to_entry(dict(zip(columns(), cells, strict=True)))))
    return entries, errors


def entry_errors(entry: dict, today: dt.date | None = None, links: bool = True) -> list[str]:
    """Schema errors plus the rules the schema cannot express.

    `links=False` skips the checks that the named record and history files exist.
    """
    errors = schema_errors(entry, ENTRY_CLASS, PAPER_LOG_SCHEMA_PATH)
    today = today or dt.date.today()

    ref = entry.get("reference")
    if isinstance(ref, str) and ref != canonical(ref):
        errors.append(f"reference {ref!r} is not canonical; write {canonical(ref)!r}")

    date = entry.get("considered_on")
    if isinstance(date, str):
        try:
            day = dt.date.fromisoformat(date)
        except ValueError:
            errors.append(f"considered_on {date!r} is not a calendar date")
        else:
            # A day of slack: CI runs on UTC, and a curator east of UTC is a day ahead.
            if day > today + dt.timedelta(days=1):
                errors.append(f"considered_on {date} is in the future")

    if links:
        errors += link_errors(entry)
    return errors


def link_errors(entry: dict) -> list[str]:
    """The records and history file a row names must exist (checked only on new rows)."""
    errors = []
    for stem in entry.get("records") or []:
        if not (RECORDS_DIR / f"{stem}.yaml").exists():
            errors.append(f"records: no record {stem!r} in {RECORDS_DIR.name}/")
    hist = entry.get("history")
    if isinstance(hist, str) and not (REPO_ROOT / hist).is_file():
        errors.append(f"history: {hist} does not exist")
    return errors


def validate_log(path: Path | None = None, today: dt.date | None = None) -> list[str]:
    """Every row against the schema and rules, except that linked files exist.

    Those links are checked when a row is new (`add`, `check-append`), because a
    merged row can't be edited when a record it names is later renamed or removed.
    """
    entries, errors = read(path)
    seen: dict[str, int] = {}
    for lineno, entry in entries:
        errors += [f"line {lineno}: {e}" for e in entry_errors(entry, today, links=False)]
        key = _to_row(entry)
        if key in seen:
            errors.append(f"line {lineno}: repeats line {seen[key]} exactly")
        seen.setdefault(key, lineno)
    if not errors:
        # The whole file, as the model's root class.
        errors += schema_errors({"entries": [e for _, e in entries]}, LOG_CLASS, PAPER_LOG_SCHEMA_PATH)
    return errors


def lookup(paper: str, path: Path | None = None) -> list[dict]:
    """Every entry for a paper, oldest first. The last is the current verdict.

    A PMID also finds rows keyed by the DOI the cache gives it.
    """
    targets = {canonical(paper), paper_key(paper)}
    entries, _ = read(path)
    return [e for _, e in entries if e.get("reference") in targets]


def build_entry(paper: str, verdict: str, note: str, records: list[str] | None = None,
                history: str | None = None, date: str | None = None) -> dict:
    entry: dict = {
        "reference": paper_key(paper),
        "considered_on": date or dt.date.today().isoformat(),
        "verdict": verdict.upper(),
        "note": " ".join(note.split()),  # a tab or newline would break the row
    }
    if records:
        entry["records"] = records
    if history:
        entry["history"] = history
    return entry


def append(entry: dict, path: Path | None = None) -> None:
    # Defaults resolve at call time, never at import, so a caller (or a test)
    # that repoints PAPER_LOG_PATH is honored.
    path = path or PAPER_LOG_PATH
    text = path.read_text(encoding="utf-8")
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + _to_row(entry) + "\n", encoding="utf-8")


def rev_exists(rev: str) -> bool:
    out = subprocess.run(["git", "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}"],
                         cwd=REPO_ROOT, capture_output=True, text=True)
    return out.returncode == 0


def _git_show(rev: str, path: Path) -> str | None:
    """A file's text at a revision, or None if it did not exist there. Check `rev_exists` first."""
    rel = path.resolve().relative_to(REPO_ROOT).as_posix()
    out = subprocess.run(["git", "show", f"{rev}:{rel}"], cwd=REPO_ROOT, capture_output=True, text=True)
    return out.stdout if out.returncode == 0 else None


def _match_base(base_text: str | None, head_text: str) -> tuple[list[str], list[int]]:
    """(errors, 0-based indexes of head lines that are new since base).

    Every line of the base log must still be in the head log, in the same order.
    New rows may come anywhere (a union merge interleaves them), but an earlier
    row is never edited, reordered or removed.
    """
    head = head_text.splitlines()
    if base_text is None:
        return [], list(range(1, len(head)))  # every data row is new; line 0 is the header
    matched: set[int] = set()
    i = 0
    for lineno, line in enumerate(base_text.splitlines(), start=1):
        while i < len(head) and head[i] != line:
            i += 1
        if i == len(head):
            return [f"line {lineno} of the base log was edited, reordered or removed: {line[:120]!r}. "
                    "The paper log is append-only; add a new row instead."], []
        matched.add(i)
        i += 1
    return [], [n for n in range(len(head)) if n not in matched]


def migrate_text(text: str) -> str:
    """A log keyed by a bare `doi` column, rewritten to the `reference` column.

    Each row's DOI becomes `DOI:<doi>`; nothing else in the row changes. Text
    already in the current form comes back unchanged.
    """
    lines = text.splitlines()
    if not lines or tuple(lines[0].split("\t")) != LEGACY_COLUMNS:
        return text
    out = ["\t".join(columns())]
    for line in lines[1:]:
        cells = line.split("\t")
        if cells and cells[0].strip():
            cells[0] = canonical(cells[0])
        out.append("\t".join(cells))
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


def append_errors(base_text: str | None, head_text: str) -> list[str]:
    """Earlier rows unchanged, and the records and history named by new rows exist.

    A base still in the legacy `doi` form is migrated first, so the one-time
    rewrite to `reference` is checked like any other change: every earlier row
    must survive it unchanged apart from its key's form.
    """
    if base_text is not None:
        base_text = migrate_text(base_text)
    errors, new = _match_base(base_text, head_text)
    if errors:
        return errors
    head = head_text.splitlines()
    for n in new:
        cells = next(csv.reader([head[n]], delimiter="\t", quoting=csv.QUOTE_NONE), [])
        if len(cells) != len(columns()):
            continue  # `validate` reports the row's shape
        entry = _to_entry(dict(zip(columns(), cells, strict=True)))
        errors += [f"line {n + 1} (new): {e}" for e in link_errors(entry)]
    return errors


def _references(data: object) -> set[str]:
    """Every `reference:` value anywhere in a record."""
    found: set[str] = set()
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "reference" and isinstance(value, str):
                found.add(value.strip())
            else:
                found |= _references(value)
    elif isinstance(data, list):
        for item in data:
            found |= _references(item)
    return found


def doi_for(reference: str) -> str | None:
    """The DOI behind a reference: itself for `DOI:`, from the reference cache for `PMID:`."""
    prefix, _, local = reference.partition(":")
    if prefix.upper() == "DOI":
        return normalize_doi(local)
    if prefix.upper() != "PMID":
        return None
    from .validate import _fetcher  # the validator's own cache naming

    try:
        cached = _fetcher().get_cache_path(reference)
        text = cached.read_text(encoding="utf-8")
    except (OSError, ValueError):
        return None
    match = re.search(r"^doi:\s*['\"]?([^'\"\s]+)", text.split("\n---", 1)[0], re.MULTILINE)
    return normalize_doi(match.group(1)) if match else None


def coverage(files: list[Path], base: str | None, log: Path | None = None) -> list[str]:
    """References newly cited in these records whose paper has no row in the log.

    Only literature counts (`DOI:` and `PMID:`); regulatory `url:` pages are not papers.
    Advisory: a missing row is a reminder, not an error.
    """
    logged = {e.get("reference") for _, e in read(log)[0]}
    warnings = []
    for f in files:
        head = _references(load(f))
        old = _git_show(base, f) if base else None
        if old is not None:
            head -= _references(loads(old))
        for ref in sorted(head):
            if ref.partition(":")[0].upper() not in LITERATURE:
                continue
            key = paper_key(ref)
            if key not in logged and canonical(ref) not in logged:
                fix = f'just log-paper {key} ACCEPT --note "..." --record {f.stem} --apply'
                warnings.append(f"{f}: {ref} ({key}) is newly cited but has no row in the paper log. "
                                f"Add one: {fix}")
    return warnings


def cited_errors(records_dir: Path | None = None, log: Path | None = None) -> list[str]:
    """Every paper a record cites has, as its newest row naming that record, an ACCEPT.

    The QC gate behind `check-cited`. The verdict is per (paper, record): the
    newest row that names the record decides, so a paper accepted for a record
    and later rejected or deferred for it fails. A row that names no record
    applies to none, and does not revoke an ACCEPT given for a record.

    Offline: a PMID is resolved to its DOI through the committed reference
    cache. Only literature counts (`DOI:` and `PMID:`); regulations, web pages
    and standards are not papers.
    """
    records_dir = records_dir or RECORDS_DIR
    newest: dict[tuple[str, str], tuple[int, str]] = {}  # (reference, stem) -> (line, verdict)
    # Line order is time order: the log is append-only, and check-append fails
    # any edited, reordered or removed row. Don't switch to `considered_on`,
    # which ties for rows logged on the same day.
    for lineno, e in read(log)[0]:
        for stem in e.get("records") or []:
            newest[(e.get("reference", ""), stem)] = (lineno, e.get("verdict", ""))
    errors = []
    for f in sorted(records_dir.glob("*.yaml")):
        for ref in sorted(_references(load(f))):
            if ref.partition(":")[0].upper() not in LITERATURE:
                continue
            key = paper_key(ref)
            found = [newest[(k, f.stem)] for k in {key, canonical(ref)} if (k, f.stem) in newest]
            verdict = max(found)[1] if found else None
            if verdict == "ACCEPT":
                continue
            where = (f"its newest row for {f.stem} is {verdict}" if verdict
                     else f"no row in the paper log names {f.stem}")
            errors.append(f"{f.relative_to(REPO_ROOT)}: cites {ref} ({key}), but {where}. Log it: "
                          f'just log-paper {key} ACCEPT --note "..." --record {f.stem} --apply, '
                          "or stop citing it")
    return errors


def _show(entry: dict) -> str:
    extra = ""
    if entry.get("records"):
        extra += f"  records: {', '.join(entry['records'])}"
    if entry.get("history"):
        extra += f"  history: {entry['history']}"
    return f"{entry.get('considered_on')}  {entry.get('verdict'):<6}  {entry.get('note')}{extra}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="cmd", required=True)

    look = sub.add_parser("lookup", help="every row for a paper; exit 1 if it was never considered")
    look.add_argument("paper", help="DOI or PMID:NNN")

    add = sub.add_parser("add", help="append a row (dry-run unless --apply)")
    add.add_argument("paper", help="DOI or PMID:NNN; a PMID with a known DOI is logged under the DOI")
    add.add_argument("verdict", type=str.upper, choices=verdicts())
    add.add_argument("--note", required=True, help="why this verdict, in your own words")
    add.add_argument("--record", action="append", dest="records", help="record stem; repeatable")
    add.add_argument("--history", help="repo-relative path of the session's history record")
    add.add_argument("--date", help="YYYY-MM-DD; defaults to today")
    add.add_argument("--apply", action="store_true", help="write the row")

    val = sub.add_parser("validate", help="check the log against its schema and rules")
    val.add_argument("path", nargs="?", type=Path, default=PAPER_LOG_PATH)

    app = sub.add_parser("check-append",
                         help="fail if a row present at REV was edited or removed, "
                              "or a new row names a missing file")
    app.add_argument("--base", required=True, help="git revision to compare with, e.g. origin/main")
    app.add_argument("path", nargs="?", type=Path, default=PAPER_LOG_PATH)

    cov = sub.add_parser("coverage", help="newly cited papers with no log row (advisory; exit 0)")
    cov.add_argument("--base", help="git revision to compare the records with; omit to check every citation")
    cov.add_argument("--github", action="store_true", help="print GitHub Actions ::warning annotations")
    cov.add_argument("files", nargs="+", type=Path)

    cited_help = "fail unless each cited paper's newest row for the citing record is ACCEPT"
    sub.add_parser("check-cited", help=cited_help)

    mig = sub.add_parser("migrate", help="rewrite a log keyed by a bare doi column (dry-run unless --apply)")
    mig.add_argument("path", nargs="?", type=Path, default=PAPER_LOG_PATH)
    mig.add_argument("--apply", action="store_true", help="write the rewritten log")

    args = parser.parse_args(argv)

    if getattr(args, "base", None) and not rev_exists(args.base):
        print(f"ERROR: git revision {args.base!r} not found. Fetch it first (git fetch origin), "
              "or check the clone is not shallow.")
        return 2

    if args.cmd == "check-append":
        errors = append_errors(_git_show(args.base, args.path), args.path.read_text(encoding="utf-8"))
        for e in errors:
            print(f"ERROR {args.path}: {e}")
        print("The paper log has errors since the base." if errors else
              "The paper log only grew, and its new rows' records and history exist.")
        return 1 if errors else 0

    if args.cmd == "coverage":
        warnings = coverage(args.files, args.base)
        for w in warnings:
            if args.github:
                path, _, msg = w.partition(": ")
                print(f"::warning file={path}::{msg}")
            else:
                print(f"WARNING {w}")
        print(f"{len(warnings)} newly cited paper(s) missing from the paper log.")
        return 0

    if args.cmd == "check-cited":
        errors = cited_errors()
        for e in errors:
            print(f"ERROR {e}")
        print(f"{len(errors)} cited paper(s) whose newest row for the citing record is not ACCEPT.")
        return 1 if errors else 0

    if args.cmd == "migrate":
        old = args.path.read_text(encoding="utf-8")
        new = migrate_text(old)
        if new == old:
            print(f"{args.path}: already keyed by reference; nothing to do")
            return 0
        print(f"{args.path}: {len(old.splitlines()) - 1} row(s) to rewrite from doi to reference")
        if not args.apply:
            print("# dry run; pass --apply to write")
            return 0
        args.path.write_text(new, encoding="utf-8")
        print(f"rewrote {args.path}")
        return 0

    if args.cmd == "validate":
        errors = validate_log(args.path)
        for e in errors:
            print(f"ERROR {args.path}: {e}")
        print(f"{len(errors)} error(s) in the paper log.")
        return 1 if errors else 0

    if args.cmd == "lookup":
        found = lookup(args.paper)
        key = paper_key(args.paper)
        if not found:
            print(f"{key}: not in the paper log")
            return 1
        print(key)
        for entry in found:
            print("  " + _show(entry))
        return 0

    uncached = uncached_pmid_error(args.paper)
    if uncached:
        print(f"ERROR: {uncached}")
        return 1
    entry = build_entry(args.paper, args.verdict, args.note, args.records, args.history, args.date)
    errors = entry_errors(entry)
    previous = lookup(entry["reference"])
    if previous:
        print(f"# already considered {len(previous)} time(s); latest: {_show(previous[-1])}")
    print(_to_row(entry))
    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1
    if not args.apply:
        print(f"# dry run; would append to {PAPER_LOG_PATH.relative_to(REPO_ROOT)}")
        return 0
    append(entry)
    print(f"appended to {PAPER_LOG_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
