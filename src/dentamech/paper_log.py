"""The paper log: every paper considered as a source, with its verdict.

    python -m dentamech.paper_log lookup DOI            # every row for a DOI; exit 1 if none
    python -m dentamech.paper_log add DOI VERDICT --note "..." [--record STEM] [--apply]
    python -m dentamech.paper_log validate [FILE]

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
import sys
from functools import cache
from pathlib import Path

from linkml_runtime.utils.schemaview import SchemaView

from .paths import PAPER_LOG_PATH, PAPER_LOG_SCHEMA_PATH, RECORDS_DIR, REPO_ROOT
from .validate import schema_errors

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

    args = parser.parse_args(argv)

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
