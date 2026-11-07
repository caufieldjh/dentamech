"""Rendering and export smoke tests."""

from __future__ import annotations

import json
from pathlib import Path

from dentamech.export import build_records, export_browser_data
from dentamech.render import reference_url, render_all, submission_url, term_url
from dentamech.yaml_io import load_kb, slugify


def test_url_helpers():
    assert term_url("OHD:0000001").endswith("ontologies/ohd/classes?obo_id=OHD:0000001")
    assert reference_url("PMID:123") == "https://pubmed.ncbi.nlm.nih.gov/123/"
    assert reference_url("DOI:10.1/x") == "https://doi.org/10.1/x"
    assert reference_url("url:https://example.org") == "https://example.org"
    assert reference_url("ISO:4049") is None
    assert submission_url("K123456").endswith("pmn.cfm?ID=K123456")
    assert submission_url("P123456").endswith("pma.cfm?id=P123456")


def test_slugify():
    assert slugify("Resin-based composite") == "Resin-based_Composite"
    assert slugify("3Y-TZP zirconia ceramic") == "3Y-TZP_Zirconia_Ceramic"


def test_render_all(tmp_path: Path):
    n = render_all(out_dir=tmp_path)
    kb = load_kb()
    assert n == len(kb)
    assert (tmp_path / "index.html").exists()
    for name in kb:
        page = tmp_path / f"{slugify(name)}.html"
        assert page.exists()
        assert name in page.read_text(encoding="utf-8")


def test_browser_export(tmp_path: Path):
    out = tmp_path / "data.js"
    n = export_browser_data(out)
    text = out.read_text(encoding="utf-8")
    assert text.startswith("// Generated")
    payload = json.loads(text.split("=", 1)[1].rstrip().rstrip(";"))
    assert len(payload) == n == len(load_kb())
    rec = next(r for r in build_records() if r["name"] == "Amalgam")
    assert rec["category"] == "METAL"
    assert rec["term_id"] == "OHD:0000001"
