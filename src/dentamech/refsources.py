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

from linkml_reference_validator.etl.sources.base import ReferenceSourceRegistry
from linkml_reference_validator.etl.sources.url import URLSource

#: eCFR renderer API for one section of title 21; "current" is the latest issue.
ECFR_SECTION_URL = "https://www.ecfr.gov/api/renderer/v1/content/enhanced/current/title-21?part={part}&section={section}"

_SECTION = re.compile(r"^(\d+)\.(\d+)$")
_HEADING = re.compile(r"§\s*(\d+\.\d+)\s+(.+?)\.?\s*$", re.MULTILINE)


def section_url(section: str) -> str:
    """The eCFR renderer URL for a 21 CFR section number.

    >>> section_url("872.3275")
    'https://www.ecfr.gov/api/renderer/v1/content/enhanced/current/title-21?part=872&section=872.3275'
    >>> section_url("872")
    Traceback (most recent call last):
    ...
    ValueError: not a 21 CFR section number: '872'
    """
    match = _SECTION.match(section.strip())
    if not match:
        raise ValueError(f"not a 21 CFR section number: {section!r}")
    return ECFR_SECTION_URL.format(part=match.group(1), section=section.strip())


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
    """A 21 CFR section, fetched from the eCFR renderer API.

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
        url = section_url(section)
        content = super().fetch(url, config)
        if content is None:
            return None
        content.reference_id = f"CFR:{section}"
        content.title = section_title(content.content or "", section) or content.title
        content.source_url = url
        return content


def register() -> None:
    """Make ``CFR:`` fetchable by the validator in this process. Safe to call twice."""
    ReferenceSourceRegistry.register(CFRSource)
