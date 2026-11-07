# Dental Materials Knowledge Base (dentamech)

A curated, schema-validated knowledge base of dental restoration materials: composition, setting behavior, clinical uses, clinical performance, adverse effects, regulatory status (FDA first), standards, and commercial products. Built on the same bones as [DisMech](https://github.com/monarch-initiative/dismech), anchored to the [Oral Health and Disease Ontology (OHD)](https://obofoundry.org/ontology/ohd.html).

## Not clinical or regulatory advice

Entries summarize published literature and public regulatory records. They are not a substitute for a product's labeling, a regulator's database, or a clinician's judgment.

## Layout

| Path | What |
|---|---|
| `kb/materials/*.yaml` | The knowledge base. One file per material, one OHD term per file. |
| `src/dentamech/schema/dentamech.yaml` | LinkML schema. |
| `src/dentamech/` | Seeder, CLI, renderer, browser export. |
| `pages/materials/` | Rendered HTML pages. |
| `app/` | Faceted browser. |
| `conf/` | Ontology adapter and reference validator configuration. |
| `docs/` | Narrative docs and generated schema reference. |

## Quick start

```bash
just install                 # uv sync
just seed                    # stub every OHD material term (never overwrites)
just validate-all            # schema + ontology terms + parent links
just qc                      # validate-all + pytest
just render                  # pages/materials/*.html
just export-browser          # app/data.js
just serve-pages             # http://localhost:8765/pages/materials/index.html
```

Validate one file:

```bash
just validate kb/materials/Amalgam.yaml
just validate-references kb/materials/Amalgam.yaml
```

## An entry, briefly

```yaml
name: Amalgam
material_term:
  term: {id: OHD:0000001, label: amalgam dental restoration material}
category: METAL
parents: [Metal]
setting_mechanisms: [AMALGAMATION]
composition:
- name: Mercury
  role: LIQUID
  chemical: {term: {id: CHEBI:16170, label: mercury atom}}
regulatory_status:
- agency: FDA
  status: CLEARED
  regulation_number: '872.3070'
  regulation_title: Dental amalgam, mercury, and amalgam alloy
  device_class: CLASS_II
  product_codes: [EJJ, ELY, OIV]
  identification: >-
    Dental amalgam is a device that consists of a combination of elemental mercury ...
  approved_uses:
  - name: Direct filling of carious lesions or structural defects in teeth
    use_context: DIRECT_RESTORATION
  source_url: https://www.ecfr.gov/current/title-21/section-872.3070
```

Every section can carry `evidence` items with a verbatim `snippet` from the cited source. See [docs/data-model.md](docs/data-model.md) and [docs/regulatory.md](docs/regulatory.md).

## Validation

1. **Schema**: `linkml-validate` against `DentalMaterial`.
2. **Ontology terms**: `linkml-term-validator` checks every bound term ID and label against OHD, CHEBI, UBERON, HP, MONDO, and PATO through OAK.
3. **References**: `linkml-reference-validator` fetches PubMed abstracts and checks that quoted snippets appear verbatim.
4. **Consistency**: pytest checks filenames, unique names and terms, parent links, cycles, reference prefixes, and that anything past `STUB` carries evidence.

## Credits

Template: [linkml-project-copier](https://github.com/linkml/linkml-project-copier). Design and evidence model: [DisMech](https://github.com/monarch-initiative/dismech). Material terms: [OHD](https://obofoundry.org/ontology/ohd.html).
