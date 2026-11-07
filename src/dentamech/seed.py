"""Seed material stubs from the OHD dental restoration material branch.

Every non-obsolete descendant of OHD:0000000 becomes one file in
kb/materials/. A stub carries only what the ontology knows: name, definition,
the bound term, its parents, and a broad category derived from ancestry.
Existing files are never overwritten unless --force is given, so curated
content survives a reseed.
"""

from __future__ import annotations

import datetime
from pathlib import Path
from typing import Any

from oaklib import get_adapter
from oaklib.datamodels.vocabulary import IS_A

from dentamech.yaml_io import KB_DIR, dump_path, slugify

ROOT_TERM = "OHD:0000000"
SUFFIX = " dental restoration material"
# OHD has one typo'd label; keep the ontology label in `term.label` (the
# validator checks it verbatim) but give the entry a clean name.
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


def build_stub(adapter, curie: str, now: str) -> dict[str, Any]:
    label = adapter.label(curie)
    definition = adapter.definition(curie) or ""
    ancestors = set(adapter.ancestors([curie], predicates=[IS_A], reflexive=True))
    parents = [
        clean_name(adapter.label(p))
        for _, _, p in adapter.relationships([curie], predicates=[IS_A])
        if p != curie and (p == ROOT_TERM or p in set(adapter.descendants([ROOT_TERM], predicates=[IS_A])))
    ]
    parents = sorted(set(parents))
    category = _first_match(ancestors, CATEGORY_RULES, "OTHER")
    if curie == ROOT_TERM:
        category = "OTHER"
    setting = _first_match(ancestors, SETTING_RULES, None)

    stub: dict[str, Any] = {
        "name": clean_name(label),
        "creation_date": now,
        "curation_status": "STUB",
        "description": " ".join(definition.split()),
        "material_term": {
            "preferred_term": clean_name(label),
            "term": {"id": curie, "label": label},
        },
        "category": category,
    }
    if parents:
        stub["parents"] = parents
    if setting:
        stub["setting_mechanisms"] = setting
    syns = sorted({a for a in adapter.entity_aliases(curie) if a != label})
    if syns:
        stub["synonyms"] = syns
    return stub


def seed(kb_dir: Path = KB_DIR, force: bool = False, include_root: bool = True) -> list[Path]:
    adapter = get_adapter("sqlite:obo:ohd")
    now = datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    kb_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    obsoletes = set(adapter.obsoletes())
    for curie in sorted(adapter.descendants([ROOT_TERM], predicates=[IS_A], reflexive=include_root)):
        if curie == ROOT_TERM and not include_root:
            continue
        label = adapter.label(curie) or ""
        if label.startswith("obsolete") or curie in obsoletes:
            continue
        stub = build_stub(adapter, curie, now)
        path = kb_dir / f"{slugify(stub['name'])}.yaml"
        if path.exists() and not force:
            continue
        dump_path(stub, path)
        written.append(path)
    return written
