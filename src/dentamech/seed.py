"""Seed records from the OHD dental restoration material branch.

Every non-obsolete descendant of OHD:0000000 gets one record in kb/materials/.
A stub carries only what the ontology knows: name, definition, the bound term,
its parents, and a broad category derived from ancestry. An existing record is
never overwritten, so curated content survives a reseed.

    just seed            # dry run
    just seed --apply
"""

from __future__ import annotations

import argparse
import datetime as dt
from typing import Any

from oaklib import get_adapter
from oaklib.datamodels.vocabulary import IS_A

from .paths import RECORDS_DIR
from .records import append_curation_event, write_validated_record
from .validate import slugify

ROOT_TERM = "OHD:0000000"
SUFFIX = " dental restoration material"
# OHD has one typo'd label; keep the ontology label in `record_term.label` (the
# validator checks it verbatim) but give the record a clean name.
NAME_FIXES = {"cobalt chromium metal dental resotration material": "cobalt chromium metal"}

# Category is decided by the nearest matching ancestor, checked in this
# order. HEMA is an adhesive monomer; the rest follow the OHD branches.
CATEGORY_RULES: list[tuple[str, str]] = [
    ("OHD:0001019", "HYBRID"),  # compomer
    ("OHD:0001026", "HYBRID"),  # resin-modified glass ionomer
    ("OHD:0001008", "HYBRID"),  # calcium aluminate / GI hybrid
    ("OHD:0001082", "ADHESIVE"),  # HEMA
    ("OHD:0000048", "METAL"),
    ("OHD:0000135", "CERAMIC"),
    ("OHD:0000036", "RESIN_COMPOSITE"),
    ("OHD:0001021", "CEMENT"),  # acid-base cement
    ("OHD:0001005", "CEMENT"),  # resin cement
    ("OHD:00001025", "CEMENT"),  # MTA
    ("OHD:0001045", "CEMENT"),  # calcium hydroxide
]

# Setting mechanism hints by ancestor. Only the safe, definitional ones.
SETTING_RULES: list[tuple[str, list[str]]] = [
    ("OHD:0000001", ["AMALGAMATION"]),
    ("OHD:0000034", ["COLD_WORKING"]),
    ("OHD:00001025", ["HYDRATION"]),
    ("OHD:0001021", ["ACID_BASE_REACTION"]),
    ("OHD:0001033", ["SINTERING", "MILLING"]),
]


def clean_name(label: str) -> str:
    label = NAME_FIXES.get(label, label)
    if label == "dental restoration material":
        return "Dental restoration material"
    name = label.removesuffix(SUFFIX)
    return name[:1].upper() + name[1:]


def _first_match(ancestors: set[str], rules: list[tuple[str, Any]], default: Any) -> Any:
    for curie, value in rules:
        if curie in ancestors:
            return value
    return default


def build_stub(adapter, curie: str, members: set[str]) -> dict[str, Any]:
    label = adapter.label(curie)
    ancestors = set(adapter.ancestors([curie], predicates=[IS_A], reflexive=True))
    parents = sorted({p for _, _, p in adapter.relationships([curie], predicates=[IS_A])
                      if p != curie and p in members})
    stub: dict[str, Any] = {
        "id": curie,
        "name": clean_name(label),
        "description": " ".join((adapter.definition(curie) or "").split()),
        "record_term": {"id": curie, "label": label},
        "status": "DRAFT",
        "category": "OTHER" if curie == ROOT_TERM else _first_match(ancestors, CATEGORY_RULES, "OTHER"),
        "creation_date": dt.date.today().isoformat(),
    }
    if parents:
        stub["parents"] = parents
    setting = _first_match(ancestors, SETTING_RULES, None)
    if setting:
        stub["setting_mechanisms"] = setting
    synonyms = sorted({a for a in adapter.entity_aliases(curie) if a != label})
    if synonyms:
        stub["synonyms"] = synonyms
    return stub


def seed(apply: bool = False, curator: str = "dentamech-seed") -> list[str]:
    """Write a stub for each OHD term with no record. Returns the names of new stubs."""
    adapter = get_adapter("sqlite:obo:ohd")
    members = set(adapter.descendants([ROOT_TERM], predicates=[IS_A], reflexive=True))
    obsoletes = set(adapter.obsoletes())
    written = []
    for curie in sorted(members):
        label = adapter.label(curie) or ""
        if label.startswith("obsolete") or curie in obsoletes:
            continue
        stub = build_stub(adapter, curie, members)
        path = RECORDS_DIR / f"{slugify(stub['name'])}.yaml"
        if path.exists():
            continue
        append_curation_event(stub, action="CREATE", curator=curator, llm_assisted=False,
                              description=f"Seeded from OHD term {curie}.")
        write_validated_record(stub, path, dry_run=not apply)
        written.append(stub["name"])
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="write the stubs")
    args = parser.parse_args(argv)
    written = seed(apply=args.apply)
    print(f"{'Wrote' if args.apply else 'Would write'} {len(written)} stub(s).")
    for name in written:
        print(f"  {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
