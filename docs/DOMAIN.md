# The DentaMech domain model

This file is the design record for what DentaMech knows. mechmaker
wrote the skeleton. mechmaker's `design-mech-schema` skill fills it in, and every
later schema change updates it. Sections marked TODO are not done.
Where DentaMech adapts mechmaker's
[design decisions](https://monarch-initiative.github.io/mechmaker/design/), this file says how, and why.

## What a record is

One record is one dental material.

A dental material is a material used in dentistry, whatever it is for:
restorative, preventive or auxiliary (see Classification by purpose). Where OHD
has a term for the material, the record is keyed by it; so far those terms all
sit under `OHD:0000000` *dental restoration material*. Where OHD has none, the
record gets a minted id, whether the material is commercial or experimental:
denture base resins (ISO 20795-1), impression materials, or an antibacterial
composite reported in one study. OHD is not comprehensive, and curating a
material it lacks is how this knowledge base finds the terms to request from
OHD or another ontology. A record says what the material is
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

One OHD term is one record, so OHD's granularity is this Mech's where OHD has
the material. A subtype gets its own record exactly when OHD gives it a term, and
`parents` mirrors OHD's `is_a` links as record ids (for a minted record, see
below). `just seed` writes a stub for each term in the restoration branch;
materials outside it are curated by hand. Report a class at the level of its term, naming subtypes without
describing them in full.

A material with no OHD term still gets a record, under a minted id. This holds
for any purpose and for commercial materials as well as experimental ones: a
commercial impression material with no OHD term gets a record. Search OHD first
(`just search-term OHD "l~..."`); if a term fits, bind it instead. A minted
record is made at the grain you would propose as a term. It leaves
`record_term` unset, and carries a `CURATION_TODO` discussion proposing the
term to OHD, or to another ontology where it fits better. Its `parents` are
the curator's choice of the closest record, OHD-keyed where one fits (an
experimental composite under resin-based composite, `OHD:0000036`), not an
OHD `is_a` link. The `ohd-term-request` skill turns the proposal into a New
Term Request on OHD's issue tracker. When the term exists, the record is
re-grounded to it.

The identity rule accepts an OHD term only under `OHD:0000000`. OHD has no
material terms for impressions, gypsum, sealants, varnishes or waxes (searched
2026-11-19), so this does not bite yet. The first time a non-restorative
material has an OHD term outside that branch, the identity root in the schema
must be widened (the `extend-schema` skill) before the record can bind it.

## Classification by purpose

Alongside `category`, a record can carry the two-level classification proposed
by the project's dental materials expert (issue #50):

1. `purpose`: `PREVENTIVE`, `AUXILIARY` or `RESTORATIVE`.
2. `restorative_class`, for a `RESTORATIVE` material only: `CERAMIC`,
   `COMPOSITE`, `POLYMER` or `METAL`.

`experimental: true` marks a formulation made in a laboratory and reported in
research, with no commercial product behind it. Set it only when the source
describes the material that way. An experimental record must give `purpose`,
and `restorative_class` too when it is restorative; `just validate` enforces
both, and refuses `restorative_class` under any other purpose. For other
records the classification is optional, and existing records were not
reclassified.

This classification is separate from `category` on purpose. `category` says what
a material is made of, on every record, and has places for cements, adhesives
and hybrids. `purpose` says what it is for. `restorative_class` is a second,
coarser answer to what a restorative material is made of, so it overlaps
`category`, and the two must agree where they name the same class:

| `category` | allows `restorative_class` |
|---|---|
| `METAL` | `METAL` only |
| `CERAMIC` | `CERAMIC` only |
| `RESIN_COMPOSITE` | `COMPOSITE` only |
| `POLYMER` | `POLYMER` only |
| `CEMENT`, `ADHESIVE`, `HYBRID`, `OTHER` | any (a resin cement or a compomer may be `COMPOSITE`) |

`just validate` enforces the table. How far the two slots should overlap at all,
and what each means exactly, is issue #56. Whether the classification should cover every
record is an open question (`docs/explanation/design-decisions.md`, section 10).

## Sections

| Section | Ontology | Purpose |
|---|---|---|
| `category` | none | Broad material class, set without needing an ontology. Example: `METAL` |
| `experimental`, `purpose`, `restorative_class` | none | Experimental marker and the two-level classification by purpose. Example: `RESTORATIVE`, `COMPOSITE` |
| `parents` | OHD | Parent records, mirroring `is_a`; for a minted record, the closest record by the curator's choice. Example: `OHD:0000048` |
| `setting_mechanisms` | none | How it hardens or is formed. Example: `AMALGAMATION` |
| `composition` | CHEBI under `CHEBI:24431`, checked with `ols:chebi` | Components, roles and proportions. Example: mercury, `LIQUID` |
| `properties` | PATO under `PATO:0000001`, checked with `ols:pato` | Reported values with unit, method and conditions. Example: flexural strength in MPa |
| `clinical_uses` | OHD procedures under `OHD:0000002`; UBERON under `UBERON:0001062`, checked with `ols:uberon` | What it is used for, and where. Example: `DIRECT_RESTORATION` |
| `clinical_performance` | none | Survival and failure outcomes, with populations |
| `adverse_effects` | HP under `HP:0000118`, checked with `ols:hp`; MONDO under `MONDO:0000001`, checked with `ols:mondo` | What can go wrong. Example: oral lichenoid lesion |
| `regulatory_status` | none | Classification of the device type, FDA first. See `docs/regulatory.md` |
| `products` | none | Specific brands and their 510(k) or PMA submissions |
| `standards` | none | Standards it is tested or specified against. Example: ISO 4049 |
| `mappings` | NCIT, MeSH, ChEBI and others; each prefix declared in the schema | Terms in other vocabularies, in SSSOM's fields (`predicate_id`, `object_id`, `mapping_justification`). `just export` writes them as one SSSOM mapping set. An agent's mapping is `semapv:UnspecifiedMatching`. See the `curate-mappings` skill |
| `evidence` | PMID, DOI, url | Record-level citations |
| `discussions` | none | Open questions and knowledge gaps (mech_shared) |
| `datasets` | accessions | Public datasets (mech_shared) |

The regulatory model has two levels. Classification of the material as a device
type goes in `regulatory_status`. A specific brand's 510(k) goes in
`products[].submissions`. `docs/explanation/design-decisions.md` gives the reasons
for this and the other decisions.

## Sources

PubMed for literature, with quotes checked against abstracts, or against a local copy of a closed paper through signed excerpts. The Code of Federal
Regulations and FDA's product classification and 510(k) databases for regulatory
facts, cited as `url:` and verified by a person or agent, because those sites
block automated checks. ISO and ADA catalogs for standards, and the text of an
ISO standard itself, cited as `ISO.<number>:<part>_<year>_<edition>` and quoted
from a local copy through signed excerpts. OHD for the record
set. Each source goes in `curation/source_queue.tsv` with its license.

## Out of scope

Equipment, instruments and devices that are not materials (curing lights, handpieces), procedures as such, and clinical guidance, because the knowledge base describes materials. Brand-level detail beyond a regulatory decision worth recording. Purpose is not a boundary: preventive and auxiliary materials are in scope, as restorative ones are.

## Related Mechs

None yet. See
https://monarch-initiative.github.io/mechregistry/.
