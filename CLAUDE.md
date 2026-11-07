# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What this is

The **Dental Materials Knowledge Base (dentamech)**: a LinkML-based knowledge base of dental restoration materials, modeled on [DisMech](https://github.com/monarch-initiative/dismech). It combines:

1. A LinkML schema (`src/dentamech/schema/dentamech.yaml`)
2. One YAML file per material in `kb/materials/`, each bound to one OHD term under `OHD:0000000`
3. Rendered pages (`pages/materials/`) and a faceted browser (`app/`)

Read `docs/explanation/design-decisions.md` before changing scope, the ontology set, or the evidence policy.

## Commands

```bash
just install                     # uv sync --group dev
just seed                        # stub every OHD material term (never overwrites)
just validate kb/materials/X.yaml   # schema + ontology terms for one file
just validate-all                # every file: schema + terms + parent links
just validate-references kb/materials/X.yaml   # snippet check against PubMed
just qc                          # validate-all + pytest
just render                      # pages/materials/*.html
just export-browser              # app/data.js
just gen-python                  # regenerate src/dentamech/datamodel after a schema edit
uv run pytest -q

# Deep research and references
just research-material claude_code Amalgam   # report -> research/Amalgam-deep-research-claude_code.md
just research-material falcon Amalgam        # needs EDISON_API_KEY; slow and thorough
just research-status                         # which materials have reports
just fetch-reference PMID:24683067           # cache an abstract; never hand-write references_cache/
```

## Skills and commands

- `.claude/skills/curate-material/SKILL.md`: the curation workflow, research first, regulatory verification, validation, PR. Follow it step by step.
- `.claude/skills/dentamech-pr-review/SKILL.md`: review checklist for KB pull requests.
- `/curate <File_Stem> [using <provider>]`: runs the curation skill end to end.

## Automation

Workflows in `.github/workflows/` run the curation loop: triage labels new issues, the scanner picks one `curation` issue or stalled PR every six hours and advances it, the review workflow approves or requests changes, and the pages workflow re-renders after merge. Details and required secrets are in `docs/workflows.md`. The deep research prompt is `templates/dental_material_research.md`.

## Curation rules

- **One OHD term per file.** `material_term.term.label` must match OHD exactly. Put friendlier names in `preferred_term` and `synonyms`.
- **`parents` are names of other files.** They mirror OHD's `is_a` links. Tests fail on a dangling parent.
- **Snippets are verbatim quotes.** Never paraphrase. Literature snippets are machine-checked against PubMed abstracts.
- **Regulatory text is quoted from the regulation.** Cite as `url:` to the eCFR section or FDA database record. Verified regulation numbers, classes, and product codes are tabulated in `docs/regulatory.md`; do not guess a product code or a regulation number from memory. Look it up:
  - CFR text: `https://www.law.cornell.edu/cfr/text/21/872.NNNN` (eCFR itself blocks automated fetches)
  - Product codes: `https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpcd/classification.cfm?start_search=1&regulationnumber=872.NNNN`
- **Device type vs product.** Classification of the material as a device type goes in `regulatory_status`. A specific brand's 510(k) goes in `products[].submissions`.
- **Ontology lookups** use OAK: `uv run runoak -i sqlite:obo:ohd search <text>` for OHD, `ols:chebi`, `ols:uberon`, `ols:hp`, `ols:pato` for the rest.
- **Bump `curation_status`** as sections fill in. Anything past `STUB` must carry evidence.
- After a schema change: `just gen-python`, then `uv run pytest -q`, then `just validate-all`.

## Layout

```
kb/materials/            knowledge base (source of truth)
src/dentamech/schema/    LinkML schema
src/dentamech/seed.py    OHD -> stub files
src/dentamech/cli.py     `dentamech` CLI (seed, list, render, export-browser, check-links)
src/dentamech/render.py + templates/     HTML pages
src/dentamech/export.py                  app/data.js
conf/oak_config.yaml     prefix -> OAK adapter
conf/reference_validator_config.yaml
tests/                   schema conformance + KB consistency + render smoke tests
docs/                    mkdocs narrative + generated schema docs
```
