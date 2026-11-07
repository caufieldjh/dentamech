"""Data conformance tests for the dental materials knowledge base.

Fast and offline. Ontology term validation (which needs OAK) runs through
`just validate-all`, not here.
"""

from __future__ import annotations

import glob
from collections import Counter
from functools import lru_cache
from pathlib import Path

import pytest
from linkml.validator import Validator
from linkml.validator.plugins import JsonschemaValidationPlugin

from dentamech.yaml_io import KB_DIR, SCHEMA_PATH, safe_load_path, slugify

ROOT = Path(__file__).resolve().parents[1]
VALID_DIR = ROOT / "tests" / "data" / "valid"
INVALID_DIR = ROOT / "tests" / "data" / "invalid"

KB_FILES = sorted(glob.glob(str(KB_DIR / "*.yaml")))
VALID_FILES = sorted(glob.glob(str(VALID_DIR / "*.yaml")))
INVALID_FILES = sorted(glob.glob(str(INVALID_DIR / "*.yaml")))

ALLOWED_REFERENCE_PREFIXES = ("PMID:", "PMC:", "DOI:", "PPR:", "url:", "URL:")


@lru_cache(maxsize=1)
def validator() -> Validator:
    return Validator(
        schema=str(SCHEMA_PATH),
        validation_plugins=[JsonschemaValidationPlugin(closed=True)],
    )


@lru_cache(maxsize=1)
def kb() -> dict[str, dict]:
    out = {}
    for f in KB_FILES:
        data = safe_load_path(f)
        out[data["name"]] = data
    return out


def _report(path: str) -> list[str]:
    data = safe_load_path(path)
    report = validator().validate(data, target_class="DentalMaterial")
    return [f"{r.severity}: {r.message}" for r in report.results]


# --- schema conformance -----------------------------------------------------

@pytest.mark.parametrize("path", VALID_FILES, ids=lambda p: Path(p).name)
def test_valid_examples(path):
    assert _report(path) == []


@pytest.mark.parametrize("path", INVALID_FILES, ids=lambda p: Path(p).name)
def test_invalid_examples(path):
    assert _report(path), f"{path} should fail validation"


@pytest.mark.parametrize("path", KB_FILES, ids=lambda p: Path(p).name)
def test_kb_file_validates(path):
    assert _report(path) == []


# --- whole-KB consistency ---------------------------------------------------

def test_kb_not_empty():
    assert len(KB_FILES) > 0


def test_filenames_match_names():
    for f in KB_FILES:
        data = safe_load_path(f)
        assert Path(f).stem == slugify(data["name"]), f"{f}: expected {slugify(data['name'])}.yaml"


def test_names_unique():
    names = Counter(safe_load_path(f)["name"] for f in KB_FILES)
    dupes = [n for n, c in names.items() if c > 1]
    assert not dupes, f"duplicate names: {dupes}"


def test_terms_unique():
    ids = Counter(safe_load_path(f)["material_term"]["term"]["id"] for f in KB_FILES)
    dupes = [n for n, c in ids.items() if c > 1]
    assert not dupes, f"OHD terms bound to more than one entry: {dupes}"


def test_material_terms_are_ohd():
    for name, data in kb().items():
        assert data["material_term"]["term"]["id"].startswith("OHD:"), name


def test_parent_links_resolve():
    names = set(kb())
    missing = [(n, p) for n, d in kb().items() for p in d.get("parents") or [] if p not in names]
    assert not missing, f"parents without an entry: {missing}"


def test_no_parent_cycles():
    graph = {n: d.get("parents") or [] for n, d in kb().items()}

    def visit(node, seen):
        assert node not in seen, f"cycle through {node}"
        for p in graph.get(node, []):
            visit(p, seen | {node})

    for n in graph:
        visit(n, frozenset())


def _walk_evidence(node, path="root"):
    if isinstance(node, dict):
        for e in node.get("evidence") or []:
            yield path, e
        for k, v in node.items():
            if k != "evidence":
                yield from _walk_evidence(v, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from _walk_evidence(v, f"{path}[{i}]")


def test_evidence_references_well_formed():
    bad = []
    for name, data in kb().items():
        for where, e in _walk_evidence(data):
            ref = e.get("reference", "")
            if not ref.startswith(ALLOWED_REFERENCE_PREFIXES):
                bad.append((name, where, ref))
            if ref.startswith(("PMID:", "PMC:", "DOI:")) and not (e.get("snippet") or "").strip():
                bad.append((name, where, "literature reference without a snippet"))
    assert not bad, bad


def test_fda_entries_have_regulation_or_note():
    """An FDA status with a device class must say which regulation it comes from."""
    bad = []
    for name, data in kb().items():
        for rs in data.get("regulatory_status") or []:
            if rs.get("agency") == "FDA" and rs.get("device_class") and not rs.get("regulation_number"):
                bad.append(name)
    assert not bad, f"FDA class without regulation number: {bad}"


def test_curated_entries_have_evidence():
    """Anything past STUB must carry at least one evidence item somewhere."""
    bad = [
        name
        for name, data in kb().items()
        if data.get("curation_status", "STUB") != "STUB" and not any(True for _ in _walk_evidence(data))
    ]
    assert not bad, f"curated without evidence: {bad}"
