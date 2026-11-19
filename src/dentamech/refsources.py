"""Reference sources this Mech adds to linkml-reference-validator.

``CFR:872.3275`` cites a section of 21 CFR. The schema expands the prefix to
the section's eCFR page. To check a quote, the source fetches the section from
eCFR's renderer API, which serves it as HTML, so the validator's own HTML
flattening applies and a quote may run across the italic paragraph headings.
eCFR's versioner API serves the same text as XML, which the validator caches
unflattened (linkml/linkml-reference-validator#179), so it is not used here.

The validator loads only JSON API sources from configuration, so this one is
registered in-process: ``python -m dentamech.lrv`` runs the validator's
command line with it, and code that calls the validator calls ``register()``.
"""

from __future__ import annotations

import re

from linkml_reference_validator.etl.sources.base import ReferenceSource, ReferenceSourceRegistry
from linkml_reference_validator.etl.sources.url import URLSource
from linkml_reference_validator.etl.sources.utils import get_json

#: An ISO standard reference: ISO.<number>:[<part>_]<year>_<edition>.
ISO_REFERENCE = re.compile(r"^ISO\.\d+:(?:\d+_)?\d{4}_\d+$")

#: eCFR renderer API for one section of title 21, as of one issue date.
ECFR_SECTION_URL = (
    "https://www.ecfr.gov/api/renderer/v1/content/enhanced/{date}/title-21?part={part}&section={section}"
)
#: eCFR versioner API: each title's latest issue date.
ECFR_TITLES_URL = "https://www.ecfr.gov/api/versioner/v1/titles.json"

_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def latest_issue_date(titles: object) -> str | None:
    """Title 21's latest issue date from the versioner API's titles listing.

    >>> latest_issue_date({"titles": [{"number": 20}, {"number": 21, "latest_issue_date": "2026-11-12"}]})
    '2026-11-12'
    >>> latest_issue_date({"titles": []}) is None, latest_issue_date(None) is None
    (True, True)
    """
    for title in (titles or {}).get("titles", []) if isinstance(titles, dict) else []:
        date = title.get("latest_issue_date")
        if title.get("number") == 21 and isinstance(date, str) and _DATE.match(date):
            return date
    return None

_SECTION = re.compile(r"^(\d+)\.(\d+)$")
_HEADING = re.compile(r"§\s*(\d+\.\d+)\s+(.+?)\.?\s*$", re.MULTILINE)


def section_url(section: str, date: str) -> str:
    """The eCFR renderer URL for a 21 CFR section number, as of an issue date.

    >>> section_url("872.3275", "2026-11-12")
    'https://www.ecfr.gov/api/renderer/v1/content/enhanced/2026-11-12/title-21?part=872&section=872.3275'
    >>> section_url("872", "2026-11-12")
    Traceback (most recent call last):
    ...
    ValueError: not a 21 CFR section number: '872'
    """
    match = _SECTION.match(section.strip())
    if not match:
        raise ValueError(f"not a 21 CFR section number: {section!r}")
    if not _DATE.match(date):
        raise ValueError(f"not an eCFR issue date: {date!r}")
    return ECFR_SECTION_URL.format(date=date, part=match.group(1), section=section.strip())


def section_title(text: str, section: str) -> str | None:
    """'21 CFR <section> <heading>' from the section's flattened text, as records title it.

    >>> section_title("Editorial note\\n§ 872.3275 Dental cement.\\n(a) ...", "872.3275")
    '21 CFR 872.3275 Dental cement'
    >>> section_title("§ 872.9 Limitations.", "872.3275") is None
    True
    """
    for match in _HEADING.finditer(text or ""):
        if match.group(1) == section:
            return f"21 CFR {section} {match.group(2).strip()}"
    return None


class CFRSource(URLSource):
    """A 21 CFR section, fetched from the eCFR renderer API as of title 21's latest issue.

    The issue date is recorded as the cache entry's ``source_revision``, so the
    committed cache says which text a quote was checked against. If the date
    cannot be had, the fetch fails and the validator serves the cached copy,
    rather than fetching undated text.

    >>> CFRSource.prefix()
    'CFR'
    >>> CFRSource.can_handle("CFR:872.3275"), CFRSource.can_handle("url:https://x")
    (True, False)
    """

    @classmethod
    def prefix(cls) -> str:
        return "CFR"

    def fetch(self, identifier, config):
        section = identifier.strip()
        date = latest_issue_date(get_json(ECFR_TITLES_URL, "eCFR titles"))
        if date is None:
            return None
        url = section_url(section, date)
        content = super().fetch(url, config)
        if content is None:
            return None
        content.reference_id = f"CFR:{section}"
        content.title = section_title(content.content or "", section) or content.title
        content.source_url = url
        content.source_revision = date
        return content


class ISOSource(ReferenceSource):
    """An ISO standard: one prefix per standard, ``ISO.<number>``, and a local id of
    ``<part>_<year>_<edition>``. ``ISO.20795:1_2013_2`` is ISO 20795-1:2013, second
    edition. This follows bioregistry's ``iso.3166`` and ``iso.639-3`` prefixes. A
    standard without parts drops the part: ``ISO.4049:2019_5``.

    ISO standards are sold, not published, so nothing is fetched. A curator
    who holds a copy puts its text in ``local_full_text/`` under the cache stem
    (``ISO.20795_1_2013_2.md``, first line ``# <title from the cover page>``);
    quotes are matched against it and signed into ``reference_excerpts/`` by
    ``just sign-excerpts``, the same path as a closed paper. Without the copy,
    only signed excerpts pass.

    >>> ISOSource.can_handle("ISO.20795:1_2013_2"), ISOSource.can_handle("ISO:20795")
    (True, False)
    >>> ISOSource().fetch("1_2013_2", None) is None
    True
    """

    @classmethod
    def prefix(cls) -> str:
        return "ISO"

    @classmethod
    def can_handle(cls, reference_id: str) -> bool:
        return ISO_REFERENCE.match(reference_id) is not None

    def fetch(self, identifier, config):
        return None


def register() -> None:
    """Make ``CFR:`` and ``ISO:`` known to the validator in this process. Safe to call twice."""
    ReferenceSourceRegistry.register(CFRSource)
    ReferenceSourceRegistry.register(ISOSource)
