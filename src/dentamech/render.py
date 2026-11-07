"""Render material YAML files to static HTML pages."""

from __future__ import annotations

import datetime
import re
from pathlib import Path
from typing import Any

import markdown as markdown_lib
from jinja2 import Environment, FileSystemLoader, select_autoescape

from dentamech.yaml_io import PAGES_DIR, SCHEMA_PATH, load_kb, safe_load_path, slugify

TEMPLATE_DIR = Path(__file__).parent / "templates"

OLS_BASE = "https://www.ebi.ac.uk/ols4/ontologies/{ont}/classes?obo_id={curie}"
ECFR_BASE = "https://www.ecfr.gov/current/title-21/section-{reg}"
FDA_PCD_BASE = "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfPCD/classification.cfm?start_search=1&productcode={code}"
FDA_510K_BASE = "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID={num}"
FDA_PMA_BASE = "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpma/pma.cfm?id={num}"
FDA_DENOVO_BASE = "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/denovo.cfm?id={num}"


def term_url(curie: str) -> str:
    prefix = curie.split(":", 1)[0].lower()
    return OLS_BASE.format(ont=prefix, curie=curie)


def reference_url(ref: str) -> str | None:
    if ref.startswith("PMID:"):
        return f"https://pubmed.ncbi.nlm.nih.gov/{ref[5:]}/"
    if ref.startswith("PMC:"):
        return f"https://www.ncbi.nlm.nih.gov/pmc/articles/{ref[4:]}/"
    if ref.startswith("DOI:"):
        return f"https://doi.org/{ref[4:]}"
    if ref.startswith("PPR:"):
        return f"https://europepmc.org/article/PPR/{ref[4:]}"
    if ref.lower().startswith("url:"):
        return ref[4:]
    return None


def submission_url(num: str) -> str | None:
    if num.startswith("K"):
        return FDA_510K_BASE.format(num=num)
    if num.startswith("P"):
        return FDA_PMA_BASE.format(num=num)
    if num.startswith("DEN"):
        return FDA_DENOVO_BASE.format(num=num)
    return None


def enum_title(value: str) -> str:
    return value.replace("_", " ").capitalize() if value else ""


def md(text: str) -> str:
    return markdown_lib.markdown(text or "", extensions=["tables"])


def _env() -> Environment:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=select_autoescape(["html", "j2"]),
    )
    env.filters["term_url"] = term_url
    env.filters["reference_url"] = reference_url
    env.filters["submission_url"] = submission_url
    env.filters["enum_title"] = enum_title
    env.filters["slugify"] = slugify
    env.filters["md"] = md
    env.filters["ecfr"] = lambda reg: ECFR_BASE.format(reg=reg)
    env.filters["fda_pcd"] = lambda code: FDA_PCD_BASE.format(code=code)
    return env


def _enum_titles(schema: dict[str, Any]) -> dict[str, dict[str, str]]:
    """{enum_name: {VALUE: title}} for nicer labels in templates."""
    out: dict[str, dict[str, str]] = {}
    for ename, edef in (schema.get("enums") or {}).items():
        pvs = edef.get("permissible_values") or {}
        out[ename] = {k: (v or {}).get("title") or enum_title(k) for k, v in pvs.items()}
    return out


def render_all(out_dir: Path = PAGES_DIR, only: list[Path] | None = None) -> int:
    kb = load_kb()
    schema = safe_load_path(SCHEMA_PATH)
    titles = _enum_titles(schema)
    children: dict[str, list[str]] = {}
    for name, data in kb.items():
        for parent in data.get("parents", []) or []:
            children.setdefault(parent, []).append(name)

    env = _env()
    page_tpl = env.get_template("material.html.j2")
    index_tpl = env.get_template("index.html.j2")
    out_dir.mkdir(parents=True, exist_ok=True)
    built = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d")

    selected = set()
    if only:
        for p in only:
            selected.add(safe_load_path(p)["name"])

    n = 0
    for name, data in kb.items():
        if selected and name not in selected:
            continue
        html = page_tpl.render(
            m=data,
            slug=slugify(name),
            children=sorted(children.get(name, [])),
            kb=kb,
            titles=titles,
            built=built,
        )
        (out_dir / f"{slugify(name)}.html").write_text(html, encoding="utf-8")
        n += 1

    # Index: group by category, then a tree from the roots.
    by_cat: dict[str, list[dict[str, Any]]] = {}
    for name, data in kb.items():
        by_cat.setdefault(data.get("category", "OTHER"), []).append(data)
    roots = sorted(name for name, data in kb.items() if not any(p in kb for p in data.get("parents", []) or []))
    n_fda = sum(1 for d in kb.values() if any(r.get("agency") == "FDA" and r.get("regulation_number") for r in d.get("regulatory_status", []) or []))
    n_stub = sum(1 for d in kb.values() if d.get("curation_status", "STUB") == "STUB")
    (out_dir / "index.html").write_text(
        index_tpl.render(
            kb=kb,
            by_cat=dict(sorted(by_cat.items())),
            roots=roots,
            children=children,
            titles=titles,
            built=built,
            n_fda=n_fda,
            n_stub=n_stub,
        ),
        encoding="utf-8",
    )
    return n


_STRIP = re.compile(r"\s+")
