"""The paper log: its schema, its rules, and the committed file."""

from __future__ import annotations

import datetime as dt

import pytest

from dentamech import paper_log, paths
from dentamech.validate import schema_errors

HEADER = "doi\tconsidered_on\tverdict\tnote\trecords\thistory\n"
TODAY = dt.date(2026, 11, 16)
GOOD = {"doi": "10.1000/xyz.1", "considered_on": "2026-11-01", "verdict": "REJECT", "note": "Out of scope."}


def _record_stem() -> str:
    return sorted(paths.RECORDS_DIR.glob("*.yaml"))[0].stem


def _history_path() -> str:
    first = sorted(paths.HISTORY_DIR.rglob("*.yaml"))[0]
    return str(first.relative_to(paths.REPO_ROOT))


def _write(tmp_path, *rows: str):
    f = tmp_path / "paper_log.tsv"
    f.write_text(HEADER + "".join(r + "\n" for r in rows), encoding="utf-8")
    return f


def test_committed_log_is_valid():
    assert paper_log.validate_log(paths.PAPER_LOG_PATH) == []


def test_header_is_the_schema_slots():
    assert paper_log.columns() == ("doi", "considered_on", "verdict", "note", "records", "history")
    assert paths.PAPER_LOG_PATH.read_text(encoding="utf-8").startswith(HEADER)
    assert paper_log.multivalued() == {"records"}
    assert paper_log.verdicts() == ("ACCEPT", "REJECT", "DEFER")


def test_good_entry_with_every_column_passes():
    entry = dict(GOOD, verdict="ACCEPT", records=[_record_stem()], history=_history_path())
    assert paper_log.entry_errors(entry, TODAY) == []


@pytest.mark.parametrize(
    "change",
    [
        {"doi": "10.1000/XYZ.1"},            # upper case
        {"doi": "doi:10.1000/xyz.1"},        # prefixed
        {"doi": "not-a-doi"},
        {"verdict": "MAYBE"},
        {"note": " "},
        {"considered_on": "16/11/2026"},
        {"records": ["Acid_Base_Cement"]},   # stems are lower snake case
        {"history": "elsewhere/x.yaml"},
    ],
)
def test_schema_rejects(change):
    entry = dict(GOOD, **change)
    assert schema_errors(entry, "PaperLogEntry", paths.PAPER_LOG_SCHEMA_PATH)


@pytest.mark.parametrize("missing", ["doi", "considered_on", "verdict", "note"])
def test_required_columns(missing):
    entry = {k: v for k, v in GOOD.items() if k != missing}
    assert paper_log.entry_errors(entry, TODAY)


@pytest.mark.parametrize(
    "change, fragment",
    [
        ({"considered_on": "2026-02-30"}, "not a calendar date"),
        ({"considered_on": "2026-11-18"}, "in the future"),
        ({"records": ["no_such_record"]}, "no record"),
        ({"history": "history/records/none/none.yaml"}, "does not exist"),
    ],
)
def test_rules_beyond_the_schema(change, fragment):
    errors = paper_log.entry_errors(dict(GOOD, **change), TODAY)
    assert any(fragment in e for e in errors), errors


def test_one_day_of_slack_for_time_zones():
    assert paper_log.entry_errors(dict(GOOD, considered_on="2026-11-17"), TODAY) == []


def test_file_shape_errors(tmp_path):
    row = "10.1000/xyz.1\t2026-11-01\tREJECT\tOut of scope.\t\t"
    assert any("repeats line 2" in e for e in paper_log.validate_log(_write(tmp_path, row, row), TODAY))
    short = _write(tmp_path, "10.1000/xyz.1\tREJECT")
    assert any("columns" in e for e in paper_log.validate_log(short, TODAY))
    assert any("blank line" in e for e in paper_log.validate_log(_write(tmp_path, row, ""), TODAY))
    bad_header = tmp_path / "h.tsv"
    bad_header.write_text("doi\tverdict\n", encoding="utf-8")
    assert any("header" in e for e in paper_log.validate_log(bad_header, TODAY))


def test_multivalued_records_split_on_bar(tmp_path):
    a, b = sorted(p.stem for p in paths.RECORDS_DIR.glob("*.yaml"))[:2]
    f = _write(tmp_path, f"10.1000/xyz.1\t2026-11-01\tACCEPT\tUsed.\t{a}|{b}\t")
    [(_, entry)] = paper_log.read(f)[0]
    assert entry["records"] == [a, b]
    assert paper_log.validate_log(f, TODAY) == []


@pytest.mark.parametrize(
    "raw",
    ["10.1000/XYZ.1", "DOI:10.1000/xyz.1", "doi:10.1000/xyz.1", "https://doi.org/10.1000/XYZ.1",
     "http://dx.doi.org/10.1000/xyz.1", "  10.1000/xyz.1 "],
)
def test_normalize_doi(raw):
    assert paper_log.normalize_doi(raw) == "10.1000/xyz.1"


def test_lookup_returns_every_consideration_newest_last(tmp_path):
    f = _write(
        tmp_path,
        "10.1000/xyz.1\t2026-10-01\tDEFER\tNo access.\t\t",
        "10.1000/other\t2026-10-02\tREJECT\tOff topic.\t\t",
        "10.1000/xyz.1\t2026-11-01\tREJECT\tRead it; out of scope.\t\t",
    )
    found = paper_log.lookup("https://doi.org/10.1000/XYZ.1", f)
    assert [e["verdict"] for e in found] == ["DEFER", "REJECT"]
    assert paper_log.lookup("10.1000/never", f) == []


def test_add_is_dry_run_unless_apply(tmp_path, monkeypatch, capsys):
    real = paths.PAPER_LOG_PATH.read_bytes()
    f = _write(tmp_path)
    monkeypatch.setattr(paper_log, "PAPER_LOG_PATH", f)
    monkeypatch.setattr(paper_log, "REPO_ROOT", tmp_path)
    args = ["add", "DOI:10.1000/XYZ.1", "defer", "--note", "Needs   a\tterm.", "--date", "2026-11-01"]

    assert paper_log.main(args) == 0
    assert f.read_text(encoding="utf-8") == HEADER

    assert paper_log.main(args + ["--apply"]) == 0
    assert f.read_text(encoding="utf-8") == HEADER + "10.1000/xyz.1\t2026-11-01\tDEFER\tNeeds a term.\t\t\n"
    assert paper_log.validate_log(f, TODAY) == []

    assert paper_log.main(args) == 0
    assert "already considered 1 time(s)" in capsys.readouterr().out
    assert paths.PAPER_LOG_PATH.read_bytes() == real, "a test wrote to the committed log"


def test_add_refuses_an_invalid_row(tmp_path, monkeypatch):
    f = _write(tmp_path)
    monkeypatch.setattr(paper_log, "PAPER_LOG_PATH", f)
    monkeypatch.setattr(paper_log, "REPO_ROOT", tmp_path)
    assert paper_log.main(["add", "10.1000/x", "ACCEPT", "--note", "x", "--record", "no_such_record",
                           "--apply"]) == 1
    assert f.read_text(encoding="utf-8") == HEADER


BASE = HEADER + "10.1000/a\t2026-11-01\tREJECT\tOne.\t\t\n10.1000/b\t2026-11-02\tDEFER\tTwo.\t\t\n"


@pytest.mark.parametrize(
    "head, ok",
    [
        (BASE, True),
        (BASE + "10.1000/c\t2026-11-03\tACCEPT\tThree.\t\t\n", True),
        # a union merge puts the other branch's rows between ours
        (HEADER + "10.1000/a\t2026-11-01\tREJECT\tOne.\t\t\n10.1000/z\t2026-11-03\tREJECT\tZ.\t\t\n"
         "10.1000/b\t2026-11-02\tDEFER\tTwo.\t\t\n", True),
        (BASE.replace("Two.", "Two, edited."), False),
        (HEADER + "10.1000/a\t2026-11-01\tREJECT\tOne.\t\t\n", False),
        (HEADER + "10.1000/b\t2026-11-02\tDEFER\tTwo.\t\t\n10.1000/a\t2026-11-01\tREJECT\tOne.\t\t\n", False),
    ],
)
def test_append_only(head, ok):
    assert (paper_log.append_errors(BASE, head) == []) is ok


def test_append_only_passes_when_the_log_is_new():
    assert paper_log.append_errors(None, BASE) == []


def test_doi_for_reads_the_reference_cache():
    cached = next(p for p in sorted(paths.REFERENCES_DIR.glob("PMID_*.md"))
                  if "\ndoi:" in p.read_text(encoding="utf-8"))
    pmid = "PMID:" + cached.stem.split("_", 1)[1]
    doi = paper_log.doi_for(pmid)
    assert doi and doi.startswith("10.") and doi == doi.lower()
    assert paper_log.doi_for("DOI:10.1000/XYZ") == "10.1000/xyz"
    assert paper_log.doi_for("url:https://www.law.cornell.edu/cfr/text/21/872.3275") is None
    assert paper_log.doi_for("PMID:1") is None  # not cached


def test_coverage_warns_only_on_new_unlogged_papers(tmp_path, monkeypatch):
    record = tmp_path / "some_cement.yaml"
    record.write_text(
        "name: some cement\nevidence:\n"
        "  - reference: DOI:10.1000/old\n"
        "  - reference: DOI:10.1000/logged\n"
        "  - reference: DOI:10.1000/new\n"
        "  - reference: url:https://example.org/x\n",
        encoding="utf-8",
    )
    log = _write(tmp_path, "10.1000/logged\t2026-11-01\tACCEPT\tUsed.\t\t")
    monkeypatch.setattr(paper_log, "_git_show",
                        lambda rev, path: "evidence:\n  - reference: DOI:10.1000/old\n")
    warnings = paper_log.coverage([record], "BASE", log)
    assert len(warnings) == 1 and "10.1000/new" in warnings[0]
    assert len(paper_log.coverage([record], None, log)) == 2  # no base: every citation counts
