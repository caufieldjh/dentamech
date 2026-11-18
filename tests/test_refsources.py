"""CFR: references: fetched from the eCFR renderer API and checked like any other source."""

import re

import pytest
from linkml_reference_validator.etl.sources.base import ReferenceSourceRegistry
from linkml_reference_validator.etl.sources.url import URLSource
from linkml_reference_validator.models import ReferenceContent, ReferenceValidationConfig

from dentamech import refsources
from dentamech.paths import REPO_ROOT

SECTION_TEXT = """Editorial Note on Part 872
§ 872.3275 Dental cement.
(a) Zinc oxide-eugenol —
(1) Identification. Zinc oxide-eugenol is a device composed of zinc oxide-eugenol.
(2) Classification. Class I (general controls). See § 872.9.
"""


def test_section_url():
    assert refsources.section_url("872.3275") == (
        "https://www.ecfr.gov/api/renderer/v1/content/enhanced/current/title-21?part=872&section=872.3275"
    )


@pytest.mark.parametrize("bad", ["872", "21 CFR 872.3275", "872.3275(a)", ""])
def test_section_url_refuses_anything_but_a_section(bad):
    with pytest.raises(ValueError):
        refsources.section_url(bad)


def test_section_title_takes_the_cited_sections_heading():
    assert refsources.section_title(SECTION_TEXT, "872.3275") == "21 CFR 872.3275 Dental cement"
    assert refsources.section_title(SECTION_TEXT, "872.3690") is None


def test_fetch_rewrites_id_title_and_source(monkeypatch):
    seen = {}

    def fake_fetch(self, identifier, config):
        seen["url"] = identifier
        return ReferenceContent(
            reference_id=f"url:{identifier}", title="", content=SECTION_TEXT, content_type="url"
        )

    monkeypatch.setattr(URLSource, "fetch", fake_fetch)
    content = refsources.CFRSource().fetch("872.3275", ReferenceValidationConfig())
    assert seen["url"] == refsources.section_url("872.3275")
    assert content.reference_id == "CFR:872.3275"
    assert content.title == "21 CFR 872.3275 Dental cement"
    assert content.source_url == seen["url"]


def test_fetch_failure_is_none(monkeypatch):
    monkeypatch.setattr(URLSource, "fetch", lambda self, identifier, config: None)
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
