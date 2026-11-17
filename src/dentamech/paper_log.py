"""The paper log: every paper considered as a source, with its verdict.

    python -m dentamech.paper_log lookup DOI            # every row for a DOI; exit 1 if none
    python -m dentamech.paper_log add DOI VERDICT --note "..." [--record STEM] [--apply]
    python -m dentamech.paper_log validate [FILE]
    python -m dentamech.paper_log check-append --base REV     # earlier rows unchanged since REV
    python -m dentamech.paper_log coverage --base REV FILE...  # new citations with no log row (advisory)

The data model is `schema/paper_log.yaml`. The data is `curation/paper_log.tsv`:
one `PaperLogEntry` per row, the schema's slot names as the header, `|` between
values of a multivalued column. The file is append-only; the newest row for a
DOI is its current verdict.
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


def entry_errors(entry: dict, today: dt.date | None = None) -> list[str]:
    """Schema errors plus the rules the schema cannot express."""
    errors = schema_errors(entry, ENTRY_CLASS, PAPER_LOG_SCHEMA_PATH)
    today = today or dt.date.today()

    doi = entry.get("doi")
    if isinstance(doi, str) and doi != normalize_doi(doi):
        errors.append(f"doi {doi!r} is not canonical; write {normalize_doi(doi)!r}")

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

    for stem in entry.get("records") or []:
        if not (RECORDS_DIR / f"{stem}.yaml").exists():
            errors.append(f"records: no record {stem!r} in {RECORDS_DIR.name}/")

    hist = entry.get("history")
    if isinstance(hist, str) and not (REPO_ROOT / hist).is_file():
        errors.append(f"history: {hist} does not exist")
    return errors


def validate_log(path: Path | None = None, today: dt.date | None = None) -> list[str]:
    entries, errors = read(path)
    seen: dict[str, int] = {}
    for lineno, entry in entries:
        errors += [f"line {lineno}: {e}" for e in entry_errors(entry, today)]
        key = _to_row(entry)
        if key in seen:
            errors.append(f"line {lineno}: repeats line {seen[key]} exactly")
        seen.setdefault(key, lineno)
    if not errors:
        # The whole file, as the model's root class.
        errors += schema_errors({"entries": [e for _, e in entries]}, LOG_CLASS, PAPER_LOG_SCHEMA_PATH)
    return errors


def lookup(doi: str, path: Path | None = None) -> list[dict]:
    """Every entry for a DOI, oldest first. The last is the current verdict."""
    target = normalize_doi(doi)
    entries, _ = read(path)
    return [e for _, e in entries if normalize_doi(e.get("doi", "")) == target]


def build_entry(doi: str, verdict: str, note: str, records: list[str] | None = None,
                history: str | None = None, date: str | None = None) -> dict:
    entry: dict = {
        "doi": normalize_doi(doi),
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


def _git_show(rev: str, path: Path) -> str | None:
    """A file's text at a revision, or None if it did not exist there."""
    rel = path.resolve().relative_to(REPO_ROOT).as_posix()
    out = subprocess.run(["git", "show", f"{rev}:{rel}"], cwd=REPO_ROOT, capture_output=True, text=True)
    return out.stdout if out.returncode == 0 else None


def append_errors(base_text: str | None, head_text: str) -> list[str]:
    """Every line of the base log must still be in the head log, in the same order.

    New rows may come anywhere after that (a union merge interleaves them), but an
    earlier row is never edited, reordered or removed.
    """
    if base_text is None:
        return []
    head = head_text.splitlines()
    i = 0
    for lineno, line in enumerate(base_text.splitlines(), start=1):
        while i < len(head) and head[i] != line:
            i += 1
        if i == len(head):
            return [f"line {lineno} of the base log was edited, reordered or removed: {line[:120]!r}. "
                    "The paper log is append-only; add a new row instead."]
        i += 1
    return []


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
    logged = {normalize_doi(e.get("doi", "")) for _, e in read(log)[0]}
    warnings = []
    for f in files:
        head = _references(load(f))
        old = _git_show(base, f) if base else None
        if old is not None:
            head -= _references(loads(old))
        for ref in sorted(head):
            if ref.partition(":")[0].upper() not in ("DOI", "PMID"):
                continue
            doi = doi_for(ref)
            if doi is None:
                warnings.append(f"{f}: {ref} is newly cited, but its DOI is not known (fetch it with "
                                "just fetch-reference), so the paper log cannot be checked")
            elif doi not in logged:
                fix = f'just log-paper {doi} ACCEPT --note "..." --record {f.stem} --apply'
                warnings.append(f"{f}: {ref} (doi {doi}) is newly cited but has no row in the paper log. "
                                f"Add one: {fix}")
    return warnings


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

    look = sub.add_parser("lookup", help="every row for a DOI; exit 1 if it was never considered")
    look.add_argument("doi")

    add = sub.add_parser("add", help="append a row (dry-run unless --apply)")
    add.add_argument("doi")
    add.add_argument("verdict", type=str.upper, choices=verdicts())
    add.add_argument("--note", required=True, help="why this verdict, in your own words")
    add.add_argument("--record", action="append", dest="records", help="record stem; repeatable")
    add.add_argument("--history", help="repo-relative path of the session's history record")
    add.add_argument("--date", help="YYYY-MM-DD; defaults to today")
    add.add_argument("--apply", action="store_true", help="write the row")

    val = sub.add_parser("validate", help="check the log against its schema and rules")
    val.add_argument("path", nargs="?", type=Path, default=PAPER_LOG_PATH)

    app = sub.add_parser("check-append", help="fail if a row present at REV was edited or removed")
    app.add_argument("--base", required=True, help="git revision to compare with, e.g. origin/main")
    app.add_argument("path", nargs="?", type=Path, default=PAPER_LOG_PATH)

    cov = sub.add_parser("coverage", help="newly cited papers with no log row (advisory; exit 0)")
    cov.add_argument("--base", help="git revision to compare the records with; omit to check every citation")
    cov.add_argument("--github", action="store_true", help="print GitHub Actions ::warning annotations")
    cov.add_argument("files", nargs="+", type=Path)

    args = parser.parse_args(argv)

    if args.cmd == "check-append":
        errors = append_errors(_git_show(args.base, args.path), args.path.read_text(encoding="utf-8"))
        for e in errors:
            print(f"ERROR {args.path}: {e}")
        print("The paper log lost or changed a row." if errors else "The paper log only grew.")
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

    if args.cmd == "validate":
        errors = validate_log(args.path)
        for e in errors:
            print(f"ERROR {args.path}: {e}")
        print(f"{len(errors)} error(s) in the paper log.")
        return 1 if errors else 0

    if args.cmd == "lookup":
        found = lookup(args.doi)
        if not found:
            print(f"{normalize_doi(args.doi)}: not in the paper log")
            return 1
        print(normalize_doi(args.doi))
        for entry in found:
            print("  " + _show(entry))
        return 0

    entry = build_entry(args.doi, args.verdict, args.note, args.records, args.history, args.date)
    errors = entry_errors(entry)
    previous = lookup(entry["doi"])
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
