"""The paper log: its schema, its rules, and the committed file."""

from __future__ import annotations

import datetime as dt

import pytest

from dentamech import paper_log, paths
from dentamech.validate import schema_errors

HEADER = "reference\tconsidered_on\tverdict\tnote\trecords\thistory\n"
TODAY = dt.date(2026, 11, 16)
GOOD = {"reference": "DOI:10.1000/xyz.1", "considered_on": "2026-11-01", "verdict": "REJECT",
        "note": "Out of scope."}


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
    assert paper_log.columns() == ("reference", "considered_on", "verdict", "note", "records", "history")
    assert paths.PAPER_LOG_PATH.read_text(encoding="utf-8").startswith(HEADER)
    assert paper_log.multivalued() == {"records"}
    assert paper_log.verdicts() == ("ACCEPT", "REJECT", "DEFER")


def test_good_entry_with_every_column_passes():
    entry = dict(GOOD, verdict="ACCEPT", records=[_record_stem()], history=_history_path())
    assert paper_log.entry_errors(entry, TODAY) == []


@pytest.mark.parametrize(
    "change",
    [
        {"reference": "DOI:10.1000/XYZ.1"},  # upper case
        {"reference": "10.1000/xyz.1"},      # bare, no prefix
        {"reference": "doi:10.1000/xyz.1"},  # lower-case prefix
        {"reference": "not-a-doi"},
        {"reference": "PMID:0123"},          # leading zero
        {"reference": "PMID:abc"},
        {"reference": "url:https://example.org/x"},  # not a paper
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


@pytest.mark.parametrize("missing", ["reference", "considered_on", "verdict", "note"])
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
    row = "DOI:10.1000/xyz.1\t2026-11-01\tREJECT\tOut of scope.\t\t"
    assert any("repeats line 2" in e for e in paper_log.validate_log(_write(tmp_path, row, row), TODAY))
    short = _write(tmp_path, "DOI:10.1000/xyz.1\tREJECT")
    assert any("columns" in e for e in paper_log.validate_log(short, TODAY))
    assert any("blank line" in e for e in paper_log.validate_log(_write(tmp_path, row, ""), TODAY))
    bad_header = tmp_path / "h.tsv"
    bad_header.write_text("reference\tverdict\n", encoding="utf-8")
    assert any("header" in e for e in paper_log.validate_log(bad_header, TODAY))


def test_multivalued_records_split_on_bar(tmp_path):
    a, b = sorted(p.stem for p in paths.RECORDS_DIR.glob("*.yaml"))[:2]
    f = _write(tmp_path, f"DOI:10.1000/xyz.1\t2026-11-01\tACCEPT\tUsed.\t{a}|{b}\t")
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
        "DOI:10.1000/xyz.1\t2026-10-01\tDEFER\tNo access.\t\t",
        "DOI:10.1000/other\t2026-10-02\tREJECT\tOff topic.\t\t",
        "DOI:10.1000/xyz.1\t2026-11-01\tREJECT\tRead it; out of scope.\t\t",
    )
    found = paper_log.lookup("https://doi.org/10.1000/XYZ.1", f)
    assert [e["verdict"] for e in found] == ["DEFER", "REJECT"]
    assert paper_log.lookup("DOI:10.1000/never", f) == []


def test_add_is_dry_run_unless_apply(tmp_path, monkeypatch, capsys):
    real = paths.PAPER_LOG_PATH.read_bytes()
    f = _write(tmp_path)
    monkeypatch.setattr(paper_log, "PAPER_LOG_PATH", f)
    monkeypatch.setattr(paper_log, "REPO_ROOT", tmp_path)
    args = ["add", "DOI:10.1000/XYZ.1", "defer", "--note", "Needs   a\tterm.", "--date", "2026-11-01"]

    assert paper_log.main(args) == 0
    assert f.read_text(encoding="utf-8") == HEADER

    assert paper_log.main(args + ["--apply"]) == 0
    expected = HEADER + "DOI:10.1000/xyz.1\t2026-11-01\tDEFER\tNeeds a term.\t\t\n"
    assert f.read_text(encoding="utf-8") == expected
    assert paper_log.validate_log(f, TODAY) == []

    assert paper_log.main(args) == 0
    assert "already considered 1 time(s)" in capsys.readouterr().out
    assert paths.PAPER_LOG_PATH.read_bytes() == real, "a test wrote to the committed log"


def test_add_refuses_an_invalid_row(tmp_path, monkeypatch):
    f = _write(tmp_path)
    monkeypatch.setattr(paper_log, "PAPER_LOG_PATH", f)
    monkeypatch.setattr(paper_log, "REPO_ROOT", tmp_path)
    assert paper_log.main(["add", "DOI:10.1000/x", "ACCEPT", "--note", "x", "--record", "no_such_record",
                           "--apply"]) == 1
    assert f.read_text(encoding="utf-8") == HEADER


BASE = HEADER + "DOI:10.1000/a\t2026-11-01\tREJECT\tOne.\t\t\nDOI:10.1000/b\t2026-11-02\tDEFER\tTwo.\t\t\n"


@pytest.mark.parametrize(
    "head, ok",
    [
        (BASE, True),
        (BASE + "DOI:10.1000/c\t2026-11-03\tACCEPT\tThree.\t\t\n", True),
        # a union merge puts the other branch's rows between ours
        (HEADER + "DOI:10.1000/a\t2026-11-01\tREJECT\tOne.\t\t\nDOI:10.1000/z\t2026-11-03\tREJECT\tZ.\t\t\n"
         "DOI:10.1000/b\t2026-11-02\tDEFER\tTwo.\t\t\n", True),
        (BASE.replace("Two.", "Two, edited."), False),
        (HEADER + "DOI:10.1000/a\t2026-11-01\tREJECT\tOne.\t\t\n", False),
        (HEADER + "DOI:10.1000/b\t2026-11-02\tDEFER\tTwo.\t\t\n"
         "DOI:10.1000/a\t2026-11-01\tREJECT\tOne.\t\t\n", False),
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
    log = _write(tmp_path, "DOI:10.1000/logged\t2026-11-01\tACCEPT\tUsed.\t\t")
    monkeypatch.setattr(paper_log, "_git_show",
                        lambda rev, path: "evidence:\n  - reference: DOI:10.1000/old\n")
    warnings = paper_log.coverage([record], "BASE", log)
    assert len(warnings) == 1 and "DOI:10.1000/new" in warnings[0]
    assert len(paper_log.coverage([record], None, log)) == 2  # no base: every citation counts


def test_a_renamed_record_does_not_break_an_old_row(tmp_path):
    # An ACCEPT row whose record was later renamed or removed still validates:
    # the row is append-only and can't follow the record.
    f = _write(tmp_path, "DOI:10.1000/a\t2026-11-01\tACCEPT\tUsed.\tno_such_record\thistory/gone.yaml")
    assert paper_log.validate_log(f, TODAY) == []
    # ...and it is not rechecked once it is on the base branch.
    text = f.read_text(encoding="utf-8")
    assert paper_log.append_errors(text, text + "DOI:10.1000/b\t2026-11-02\tREJECT\tNo.\t\t\n") == []


def test_a_new_row_must_name_files_that_exist():
    stem = next(paths.RECORDS_DIR.glob("*.yaml")).stem
    good = BASE + f"DOI:10.1000/c\t2026-11-03\tACCEPT\tUsed.\t{stem}\t\n"
    assert paper_log.append_errors(BASE, good) == []
    bad = BASE + "DOI:10.1000/c\t2026-11-03\tACCEPT\tUsed.\tno_such_record\thistory/gone.yaml\n"
    errors = paper_log.append_errors(BASE, bad)
    assert len(errors) == 2 and all("line 4 (new)" in e for e in errors)
    # a brand-new log: every row is new
    assert len(paper_log.append_errors(None, bad)) == 2


def test_an_unknown_base_revision_fails_loudly(capsys):
    assert paper_log.main(["check-append", "--base", "no-such-revision-xyz"]) == 2
    assert "not found" in capsys.readouterr().out
    assert paper_log.main(["coverage", "--base", "no-such-revision-xyz", "README.md"]) == 2
    assert paper_log.rev_exists("HEAD")


# --- #73: reference keys, PMIDs, the doi -> reference migration, and the cited-paper gate ---

LEGACY_HEADER = "doi\tconsidered_on\tverdict\tnote\trecords\thistory\n"
LEGACY_BASE = (LEGACY_HEADER + "10.1000/a\t2026-11-01\tREJECT\tOne.\t\t\n"
               "10.1000/b\t2026-11-02\tDEFER\tTwo.\t\t\n")


def _cached_pmid(with_doi: bool) -> tuple[str, str | None]:
    """A cached PMID with (or without) a DOI, and that DOI."""
    for p in sorted(paths.REFERENCES_DIR.glob("PMID_*.md")):
        pmid = "PMID:" + p.stem.split("_", 1)[1]
        doi = paper_log.doi_for(pmid)
        if bool(doi) is with_doi:
            return pmid, doi
    pytest.skip("no cached PMID of that kind")


@pytest.mark.parametrize(
    "raw, key",
    [
        ("10.1000/XYZ.1", "DOI:10.1000/xyz.1"),
        ("doi:10.1000/xyz.1", "DOI:10.1000/xyz.1"),
        ("DOI:10.1000/XYZ.1", "DOI:10.1000/xyz.1"),
        ("https://doi.org/10.1000/XYZ.1", "DOI:10.1000/xyz.1"),
        ("PMID:123", "PMID:123"),
        ("pmid:0123", "PMID:123"),
        (" PMID:123 ", "PMID:123"),
    ],
)
def test_canonical(raw, key):
    assert paper_log.canonical(raw) == key


def test_a_pmid_only_row_is_valid():
    assert paper_log.entry_errors(dict(GOOD, reference="PMID:6948048"), TODAY) == []
    errors = paper_log.entry_errors(dict(GOOD, reference="doi:10.1000/xyz.1"), TODAY)
    assert any("not canonical" in e for e in errors)


def test_a_pmid_with_a_known_doi_is_keyed_by_the_doi():
    pmid, doi = _cached_pmid(with_doi=True)
    assert paper_log.paper_key(pmid) == f"DOI:{doi}"
    assert paper_log.build_entry(pmid, "ACCEPT", "x")["reference"] == f"DOI:{doi}"


def test_a_pmid_without_a_doi_stays_a_pmid():
    pmid, _ = _cached_pmid(with_doi=False)
    assert paper_log.paper_key(pmid) == pmid
    assert paper_log.paper_key("PMID:1") == "PMID:1"  # not cached at all


def test_lookup_by_pmid_finds_rows_keyed_by_its_doi(tmp_path):
    pmid, doi = _cached_pmid(with_doi=True)
    f = _write(tmp_path, f"DOI:{doi}\t2026-11-01\tREJECT\tNo.\t\t")
    assert [e["verdict"] for e in paper_log.lookup(pmid, f)] == ["REJECT"]


def test_migrate_text_rewrites_only_the_key():
    legacy = LEGACY_BASE
    assert paper_log.migrate_text(legacy) == BASE
    assert paper_log.migrate_text(BASE) == BASE  # already migrated: unchanged


def test_append_only_across_the_migration():
    legacy = LEGACY_BASE
    assert paper_log.append_errors(legacy, BASE) == []
    assert paper_log.append_errors(legacy, BASE + "PMID:42\t2026-11-03\tACCEPT\tThree.\t\t\n") == []
    # an edit hidden inside the rewrite is still caught
    assert paper_log.append_errors(legacy, BASE.replace("Two.", "Two, edited."))
    # and a row dropped in the rewrite
    assert paper_log.append_errors(legacy, HEADER + "DOI:10.1000/a\t2026-11-01\tREJECT\tOne.\t\t\n")


def _kb(tmp_path, refs: list[str]):
    kb = tmp_path / "kb"
    kb.mkdir()
    body = "name: x\nevidence:\n" + "".join(f"  - reference: {r}\n" for r in refs)
    (kb / "some_cement.yaml").write_text(body, encoding="utf-8")
    return kb


def test_cited_errors(tmp_path, monkeypatch):
    monkeypatch.setattr(paper_log, "REPO_ROOT", tmp_path)
    kb = _kb(tmp_path, ["DOI:10.1000/logged", "DOI:10.1000/missing", "PMID:1",
                        "DOI:10.1000/other_record", "DOI:10.1000/rejected",
                        "url:https://example.org/x", "CFR:872.3275"])
    log = _write(
        tmp_path,
        "DOI:10.1000/logged\t2026-11-01\tACCEPT\tUsed.\tsome_cement\t",
        "PMID:1\t2026-11-01\tACCEPT\tUsed.\tsome_cement\t",
        "DOI:10.1000/other_record\t2026-11-01\tACCEPT\tUsed.\tanother_cement\t",
        "DOI:10.1000/rejected\t2026-11-01\tREJECT\tNo.\tsome_cement\t",
    )
    errors = paper_log.cited_errors(kb, log)
    flagged = sorted(e.split(" cites ")[1].split(" ")[0] for e in errors)
    # not logged at all; logged only for another record; logged but not ACCEPT
    assert flagged == ["DOI:10.1000/missing", "DOI:10.1000/other_record", "DOI:10.1000/rejected"]


def test_cited_errors_uses_the_newest_row_per_record(tmp_path, monkeypatch):
    monkeypatch.setattr(paper_log, "REPO_ROOT", tmp_path)
    kb = _kb(tmp_path, ["DOI:10.1000/revoked", "DOI:10.1000/reaccepted", "DOI:10.1000/unscoped_reject"])
    log = _write(
        tmp_path,
        # accepted, then rejected for the same record: fails
        "DOI:10.1000/revoked\t2026-11-01\tACCEPT\tUsed.\tsome_cement\t",
        "DOI:10.1000/revoked\t2026-11-02\tREJECT\tWithdrawn.\tsome_cement\t",
        # rejected, then accepted for the record: passes
        "DOI:10.1000/reaccepted\t2026-11-01\tDEFER\tNo access.\tsome_cement\t",
        "DOI:10.1000/reaccepted\t2026-11-02\tACCEPT\tRead it.\tsome_cement\t",
        # a later REJECT naming no record revokes nothing: passes
        "DOI:10.1000/unscoped_reject\t2026-11-01\tACCEPT\tUsed.\tsome_cement\t",
        "DOI:10.1000/unscoped_reject\t2026-11-02\tREJECT\tNot for another record.\t\t",
    )
    errors = paper_log.cited_errors(kb, log)
    assert len(errors) == 1 and "DOI:10.1000/revoked" in errors[0] and "is REJECT" in errors[0]


def test_every_cited_paper_in_the_committed_kb_is_logged():
    assert paper_log.cited_errors() == []


def test_add_refuses_an_uncached_pmid(tmp_path, monkeypatch, capsys):
    # An uncached PMID can't be resolved to its DOI; logging it could give a paper two keys.
    f = _write(tmp_path)
    monkeypatch.setattr(paper_log, "PAPER_LOG_PATH", f)
    monkeypatch.setattr(paper_log, "REPO_ROOT", tmp_path)
    assert paper_log.main(["add", "PMID:1", "REJECT", "--note", "x", "--apply"]) == 1
    assert "just fetch-reference PMID:1" in capsys.readouterr().out
    assert f.read_text(encoding="utf-8") == HEADER


def test_add_accepts_a_cached_pmid_with_no_doi(tmp_path, monkeypatch):
    pmid, _ = _cached_pmid(with_doi=False)
    f = _write(tmp_path)
    monkeypatch.setattr(paper_log, "PAPER_LOG_PATH", f)
    monkeypatch.setattr(paper_log, "REPO_ROOT", tmp_path)
    assert paper_log.main(["add", pmid, "REJECT", "--note", "x", "--date", "2026-11-01", "--apply"]) == 0
    assert f.read_text(encoding="utf-8").splitlines()[1].startswith(pmid + "\t")


def test_a_doi_is_never_refused_for_the_cache():
    assert paper_log.uncached_pmid_error("10.1000/not.cached") is None
