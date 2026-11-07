# The DentaMech domain model

This file is the design record for what DentaMech knows. mechmaker
wrote the skeleton. mechmaker's `design-mech-schema` skill fills it in, and every
later schema change updates it. Sections marked TODO are not done.

## What a record is

One record is one dental material.

A dental material is one class of restoration material as OHD defines it, under
`OHD:0000000` *dental restoration material*. A record says what the material is
made of, how it sets, what it is used for, how it performs, what can go wrong,
and how regulators classify it.

Equipment such as curing lights and handpieces, procedures as such, and clinical
guidance are not records. A specific brand is not a record either: it is an item
under `products` on the record of its material. The knowledge base describes
materials. It does not tell anyone what to put in a tooth.

## Identity

Records are keyed by OHD CURIEs where a term exists, descending from `OHD:0000000`.
Where none exists, the record gets a minted id, `dentamech:<uuid>`
(`just new-record` mints one when given no `--id`), and can be re-grounded
later.

An id never changes when a record is renamed, and no two records share one.

The filename stem is derived from `name`: lowercase, runs of non-alphanumerics
become one underscore.

One OHD term is one record, so OHD's granularity is this Mech's. A subtype gets
its own record exactly when OHD gives it a term, and `parents` mirrors OHD's
`is_a` links as record ids. `just seed` writes a stub for each term. A material
with no OHD term is not given a record: propose the term to OHD first. Report a
class at the level of its term, naming subtypes without describing them in full.

## Sections

| Section | Ontology | Purpose |
|---|---|---|
| `category` | none | Broad material class, set without needing an ontology. Example: `METAL` |
| `parents` | OHD | Parent records, mirroring `is_a`. Example: `OHD:0000048` |
| `setting_mechanisms` | none | How it hardens or is formed. Example: `AMALGAMATION` |
| `composition` | CHEBI under `CHEBI:24431`, checked with `ols:chebi` | Components, roles and proportions. Example: mercury, `LIQUID` |
| `properties` | PATO under `PATO:0000001`, checked with `ols:pato` | Reported values with unit, method and conditions. Example: flexural strength in MPa |
| `clinical_uses` | OHD procedures under `OHD:0000002`; UBERON under `UBERON:0001062`, checked with `ols:uberon` | What it is used for, and where. Example: `DIRECT_RESTORATION` |
| `clinical_performance` | none | Survival and failure outcomes, with populations |
| `adverse_effects` | HP under `HP:0000118`, checked with `ols:hp`; MONDO under `MONDO:0000001`, checked with `ols:mondo` | What can go wrong. Example: oral lichenoid lesion |
| `regulatory_status` | none | Classification of the device type, FDA first. See `docs/regulatory.md` |
| `products` | none | Specific brands and their 510(k) or PMA submissions |
| `standards` | none | Standards it is tested or specified against. Example: ISO 4049 |
| `mappings` | NCIT and others | Terms in other vocabularies |
| `evidence` | PMID, DOI, url | Record-level citations |
| `discussions` | none | Open questions and knowledge gaps (mech_shared) |
| `datasets` | accessions | Public datasets (mech_shared) |

The regulatory model has two levels. Classification of the material as a device
type goes in `regulatory_status`. A specific brand's 510(k) goes in
`products[].submissions`. `docs/explanation/design-decisions.md` gives the reasons
for this and the other decisions.

## Sources

PubMed for literature, with quotes checked against abstracts. The Code of Federal
Regulations and FDA's product classification and 510(k) databases for regulatory
facts, cited as `url:` and verified by a person or agent, because those sites
block automated checks. ISO and ADA catalogs for standards. OHD for the record
set. Each source goes in `curation/source_queue.tsv` with its license.

## Out of scope

Equipment, procedures as such, and clinical guidance, because the knowledge base describes materials. Brand-level detail beyond a regulatory decision worth recording.

## Related Mechs

None yet. See
https://monarch-initiative.github.io/mechregistry/.
