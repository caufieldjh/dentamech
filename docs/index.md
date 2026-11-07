# Dental Materials Knowledge Base (dentamech)

A curated, schema-validated knowledge base of dental restoration materials: what they are made of, how they set, what they are used for, how they perform, what can go wrong, and how regulators classify them.

It is built the way [DisMech](https://github.com/monarch-initiative/dismech) is built: one YAML file per entry, a [LinkML](https://linkml.io) schema, ontology-bound terms validated against their source ontologies, and evidence items that quote their sources verbatim. Where DisMech anchors on Mondo, this project anchors on the [Oral Health and Disease Ontology (OHD)](https://obofoundry.org/ontology/ohd.html) branch under `OHD:0000000` *dental restoration material*.

## Where things live

| Path | What |
|---|---|
| `kb/materials/*.yaml` | The knowledge base. One file per material. |
| `src/dentamech/schema/dentamech.yaml` | The LinkML schema. |
| `pages/materials/*.html` | Rendered material pages (`just render`). |
| `app/index.html` | Faceted browser over `app/data.js` (`just export-browser`). |
| `conf/oak_config.yaml` | Which ontologies back which prefixes for term validation. |

## Reading on

- [Data model](data-model.md): the sections of a material entry and what goes in each.
- [Regulatory status](regulatory.md): how FDA classification, product codes, and clearances are recorded.
- [Curation](curation.md): the workflow, the validation gates, and the evidence rules.
- [Design decisions](explanation/design-decisions.md): why it is built this way.
- [Schema reference](elements/index.md): generated from the LinkML schema.

## Status

The knowledge base was seeded from OHD on 2026-09-04. Every OHD material term has a stub entry. A handful of entries carry curated composition, use, and FDA regulatory content as worked examples; the rest await curation.
