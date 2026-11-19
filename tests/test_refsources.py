"""CFR: references: fetched from the eCFR renderer API and checked like any other source."""

import re

import pytest
import yaml
from linkml_reference_validator.etl.sources.base import ReferenceSourceRegistry
from linkml_reference_validator.etl.sources.url import URLSource
from linkml_reference_validator.models import ReferenceContent, ReferenceValidationConfig

from dentamech import refsources
from dentamech.paths import REPO_ROOT, SCHEMA_PATH

SECTION_TEXT = """Editorial Note on Part 872
§ 872.3275 Dental cement.
(a) Zinc oxide-eugenol —
(1) Identification. Zinc oxide-eugenol is a device composed of zinc oxide-eugenol.
(2) Classification. Class I (general controls). See § 872.9.
"""


TITLES = {"titles": [{"number": 20, "latest_issue_date": "2026-01-01"},
                      {"number": 21, "latest_issue_date": "2026-11-12"}]}


def test_section_url():
    assert refsources.section_url("872.3275", "2026-11-12") == (
        "https://www.ecfr.gov/api/renderer/v1/content/enhanced/2026-11-12/title-21?part=872&section=872.3275"
    )


@pytest.mark.parametrize("bad", ["872", "21 CFR 872.3275", "872.3275(a)", ""])
def test_section_url_refuses_anything_but_a_section(bad):
    with pytest.raises(ValueError):
        refsources.section_url(bad, "2026-11-12")


@pytest.mark.parametrize("bad", ["current", "2026-11", ""])
def test_section_url_refuses_anything_but_an_issue_date(bad):
    with pytest.raises(ValueError):
        refsources.section_url("872.3275", bad)


def test_latest_issue_date_is_title_21s():
    assert refsources.latest_issue_date(TITLES) == "2026-11-12"
    assert refsources.latest_issue_date({"titles": [{"number": 21, "latest_issue_date": "soon"}]}) is None
    assert refsources.latest_issue_date(None) is None


def test_section_title_takes_the_cited_sections_heading():
    assert refsources.section_title(SECTION_TEXT, "872.3275") == "21 CFR 872.3275 Dental cement"
    assert refsources.section_title(SECTION_TEXT, "872.3690") is None


def test_fetch_rewrites_id_title_source_and_revision(monkeypatch):
    seen = {}
    monkeypatch.setattr(refsources, "get_json", lambda url, label: TITLES)

    def fake_fetch(self, identifier, config):
        seen["url"] = identifier
        return ReferenceContent(
            reference_id=f"url:{identifier}", title="", content=SECTION_TEXT, content_type="url"
        )

    monkeypatch.setattr(URLSource, "fetch", fake_fetch)
    content = refsources.CFRSource().fetch("872.3275", ReferenceValidationConfig())
    assert seen["url"] == refsources.section_url("872.3275", "2026-11-12")
    assert content.reference_id == "CFR:872.3275"
    assert content.title == "21 CFR 872.3275 Dental cement"
    assert content.source_url == seen["url"]
    assert content.source_revision == "2026-11-12"


def test_fetch_failure_is_none(monkeypatch):
    monkeypatch.setattr(refsources, "get_json", lambda url, label: TITLES)
    monkeypatch.setattr(URLSource, "fetch", lambda self, identifier, config: None)
    assert refsources.CFRSource().fetch("872.3275", ReferenceValidationConfig()) is None


def test_no_issue_date_fetches_nothing(monkeypatch):
    """Without an issue date the fetch fails, so the cached copy is served instead of undated text."""
    monkeypatch.setattr(refsources, "get_json", lambda url, label: None)

    def must_not_fetch(self, identifier, config):
        raise AssertionError("fetched without an issue date")

    monkeypatch.setattr(URLSource, "fetch", must_not_fetch)
    assert refsources.CFRSource().fetch("872.3275", ReferenceValidationConfig()) is None


def test_register_is_idempotent():
    refsources.register()
    refsources.register()
    assert ReferenceSourceRegistry._sources.count(refsources.CFRSource) == 1
    assert refsources.CFRSource.can_handle("CFR:872.3275")


def test_cfr_is_not_skipped():
    config = (REPO_ROOT / ".linkml-reference-validator.yaml").read_text(encoding="utf-8")
    skipped = re.search(r"skip_prefixes:\n((?:\s+- .+\n)+)", config).group(1)
    assert "CFR" not in [line.strip()[2:] for line in skipped.splitlines()]


def test_every_cited_section_is_cached():
    """CI checks CFR: quotes from the committed cache, so each cited section must be in it."""
    cited = set()
    for path in (REPO_ROOT / "kb" / "materials").glob("*.yaml"):
        cited |= set(re.findall(r"reference: CFR:(\d+\.\d+)\s*$", path.read_text(encoding="utf-8"), re.M))
    assert cited, "no record cites CFR:"
    missing = sorted(s for s in cited if not (REPO_ROOT / "references_cache" / f"CFR_{s}.md").is_file())
    assert not missing, f"not cached; run just fetch-reference CFR:<section>: {missing}"


def test_iso_fetches_nothing():
    assert refsources.ISOSource().fetch("1_2013_2", ReferenceValidationConfig()) is None
    refsources.register()
    assert ReferenceSourceRegistry.get_source("ISO.20795:1_2013_2") is refsources.ISOSource


@pytest.mark.parametrize("ref, ok", [
    ("ISO.20795:1_2013_2", True), ("ISO.4049:2019_5", True),
    ("ISO:20795-1:2013", False), ("ISO.20795:1-2013", False), ("ISO.20795:1_2013", False),
])
def test_iso_reference_form(ref, ok):
    assert refsources.ISOSource.can_handle(ref) is ok


def test_iso_is_not_skipped():
    config = (REPO_ROOT / ".linkml-reference-validator.yaml").read_text(encoding="utf-8")
    skipped = re.search(r"skip_prefixes:\n((?:\s+- .+\n)+)", config).group(1)
    assert "ISO" not in [line.strip()[2:] for line in skipped.splitlines()]


ISO_TEXT = ("# Made-up standard\n\n"
            "This part of ISO 99999 specifies the requirements for an imaginary material.\n")


def _lrv(tmp_path, *args):
    import subprocess
    import sys

    return subprocess.run([sys.executable, "-m", "dentamech.lrv", *args, "--config", "lrv.yaml"],
                          cwd=tmp_path, capture_output=True, text=True)


def _iso_record(tmp_path, snippet):
    (tmp_path / "record.yaml").write_text(
        "id: dentamech:00000000-0000-4000-8000-000000000009\nname: Imaginary material\n"
        "status: DRAFT\ncategory: OTHER\nevidence:\n  - reference: ISO.99999:1_2099_1\n"
        "    reference_title: Made-up standard\n    supports: SUPPORT\n    evidence_source: STANDARD\n"
        f"    snippet: {snippet}\n", encoding="utf-8")


def test_an_iso_quote_is_signed_then_checked_without_the_standard(tmp_path):
    """The ISO path end to end: matched against the local copy, signed, then checked from the bundle alone."""
    (tmp_path / "lrv.yaml").write_text(
        "validation:\n  cache_dir: cache\n  unknown_prefix_severity: ERROR\n  fetch_full_text: false\n"
        "  local_full_text_dir: local_full_text\n  signed_excerpts_dir: reference_excerpts\n"
        "  signed_excerpts_require_verification: true\n  trust_cached_entries: true\n", encoding="utf-8")
    (tmp_path / "local_full_text").mkdir()
    copy = tmp_path / "local_full_text" / "ISO.99999_1_2099_1.md"
    copy.write_text(ISO_TEXT, encoding="utf-8")
    schema = str(SCHEMA_PATH)
    check = ("validate", "data", "record.yaml", "--schema", schema, "--target-class", "DentalMaterial",
             "--no-full-text")
    _iso_record(tmp_path, "the requirements for an imaginary material")
    signed = _lrv(tmp_path, "excerpts", "sign", "record.yaml")
    assert signed.returncode == 0, signed.stdout + signed.stderr
    assert (tmp_path / "reference_excerpts" / "ISO.99999_1_2099_1.yaml").is_file()

    copy.unlink()
    assert _lrv(tmp_path, *check).returncode == 0  # the bundle alone suffices
    cached = [p.read_text(encoding="utf-8") for p in (tmp_path / "cache").glob("**/*") if p.is_file()]
    assert not any("imaginary" in text for text in cached)  # the standard's text is never cached

    _iso_record(tmp_path, "the requirements for every imaginary material")
    assert _lrv(tmp_path, *check).returncode != 0  # an altered quote fails


def test_every_cited_iso_standard_has_its_prefix():
    """One prefix per ISO standard, so each one cited must be declared, or the RDF exports fail."""
    schema = yaml.safe_load(SCHEMA_PATH.read_text(encoding="utf-8"))
    declared = set(schema["prefixes"])
    cited = set()
    for path in (REPO_ROOT / "kb" / "materials").glob("*.yaml"):
        cited |= set(re.findall(r"reference: (ISO\.\d+):", path.read_text(encoding="utf-8")))
    assert not cited - declared, f"declare these in the schema's prefixes: {sorted(cited - declared)}"
