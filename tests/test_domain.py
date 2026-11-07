"""Dental rules across the whole knowledge base: parent links, evidence, FDA facts."""

from __future__ import annotations

import pytest

from dentamech import validate

RECORDS = {path.stem: validate.load(path) for path in validate.iter_records()}
ALLOWED_REFERENCE_PREFIXES = ("PMID:", "PMC:", "DOI:", "PPR:", "url:", "URL:")


def walk_evidence(node, path="root"):
    if isinstance(node, dict):
        for item in node.get("evidence") or []:
            yield path, item
        for key, value in node.items():
            if key != "evidence":
                yield from walk_evidence(value, f"{path}.{key}")
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from walk_evidence(value, f"{path}[{index}]")


def test_kb_not_empty():
    assert RECORDS


def test_records_are_keyed_by_ohd():
    assert not [stem for stem, data in RECORDS.items() if not data["id"].startswith("OHD:")]


def test_parent_links_resolve():
    ids = {data["id"] for data in RECORDS.values()}
    missing = [(stem, p) for stem, d in RECORDS.items() for p in d.get("parents") or [] if p not in ids]
    assert not missing, f"parents without a record: {missing}"


def test_no_parent_cycles():
    graph = {d["id"]: d.get("parents") or [] for d in RECORDS.values()}

    def visit(node, seen):
        assert node not in seen, f"cycle through {node}"
        for parent in graph.get(node, []):
            visit(parent, seen | {node})

    for node in graph:
        visit(node, frozenset())


def test_evidence_references_well_formed():
    bad = []
    for stem, data in RECORDS.items():
        for where, item in walk_evidence(data):
            ref = item.get("reference", "")
            if not ref.startswith(ALLOWED_REFERENCE_PREFIXES):
                bad.append((stem, where, ref))
            if ref.startswith(("PMID:", "PMC:", "DOI:")) and not (item.get("snippet") or "").strip():
                bad.append((stem, where, "literature reference without a snippet"))
    assert not bad, bad


def test_fda_entries_have_regulation():
    """An FDA status with a device class must say which regulation it comes from."""
    bad = [stem for stem, data in RECORDS.items() for rs in data.get("regulatory_status") or []
           if rs.get("agency") == "FDA" and rs.get("device_class") and not rs.get("regulation_number")]
    assert not bad, f"FDA class without regulation number: {bad}"


@pytest.mark.parametrize("section", ["composition", "clinical_uses", "regulatory_status"])
def test_curated_sections_carry_evidence(section):
    """A record with curated content, or past DRAFT, carries evidence somewhere."""
    bad = [stem for stem, data in RECORDS.items()
           if data.get(section) and not any(True for _ in walk_evidence(data))]
    assert not bad, f"{section} without any evidence: {bad}"


def test_proposed_records_carry_evidence():
    bad = [stem for stem, data in RECORDS.items()
           if data.get("status") in ("PROPOSED", "REVIEWED") and not any(True for _ in walk_evidence(data))]
    assert not bad, f"past DRAFT without evidence: {bad}"
