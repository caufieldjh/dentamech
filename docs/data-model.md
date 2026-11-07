# Data model

Every file in `kb/materials/` is one `DentalMaterial`. The schema lives in `src/dentamech/schema/dentamech.yaml`; the generated reference is under [Schema](elements/index.md). This page walks the sections in the order they appear in a file.

## Identity

```yaml
name: Glass ionomer cement          # identifier; the filename is the slugified name
creation_date: '2026-09-04T20:17:41Z'
curation_status: STUB               # STUB | IN_PROGRESS | CURATED | REVIEWED
description: >-
  An acid-base cement dental restoration material containing ...
material_term:                      # required; bound to OHD under OHD:0000000
  preferred_term: Glass ionomer cement
  term:
    id: OHD:0001006
    label: glass ionomer cement dental restoration material
category: CEMENT                    # METAL | CERAMIC | RESIN_COMPOSITE | CEMENT | POLYMER | ADHESIVE | HYBRID | OTHER
parents:                            # names of other entries; mirrors OHD is_a
- Acid-base cement
synonyms: [GIC]
mappings:                           # other vocabularies, SKOS predicates
- {id: NCIT:C62213, label: Dental Composite Resin, predicate: CLOSE_MATCH}
setting_mechanisms: [ACID_BASE_REACTION]
```

`term.label` must match the ontology's label exactly; `preferred_term` is where a friendlier name goes. The seeder fills all of this from OHD, and `just validate-all` checks every `term.id` and `term.label` against OHD through OAK.

## Composition

A list of `Component` rows: name, functional `role` (matrix, filler, initiator, powder, liquid, alloying element, stabilizer, and so on), an optional CHEBI-bound `chemical`, a free-text `proportion`, and evidence.

## Properties

A list of `MaterialProperty` rows. `property_type` is a controlled list (flexural strength, elastic modulus, polymerization shrinkage, fluoride release, setting time, radiopacity, biocompatibility, and so on). `value` and `unit` are free text so ranges can be recorded as the source states them. `test_method` names the standard (ISO 4049, ISO 9917) and `conditions` qualifies it. A PATO term can be attached through `quality_term` when a typed quality is wanted.

## Clinical uses

A list of `ClinicalUse` entries. Each has a broad `use_context` (direct restoration, indirect restoration, luting, liner or base, pulp therapy, endodontic, implant, prosthodontic, orthodontic, preventive, adhesive, impression, temporary, surgical), an optional OHD `procedure` from the `dental procedure` branch, an optional UBERON `anatomical_site`, lists of `indications` and `contraindications`, and evidence.

## Clinical performance

`ClinicalPerformance` rows carry survival, success, annual failure, retention, and complication statistics with `follow_up_years`, `population`, and `comparator`. These are the numbers a systematic review reports.

## Adverse effects

`AdverseEffect` rows are typed by `effect_category` (hypersensitivity, toxicity, mechanical failure, secondary caries, pulpal response, periodontal response, antagonist wear, esthetic, occupational, environmental) and can bind an HP or MONDO term through `effect_term`.

## Regulatory status and products

Two levels. `regulatory_status` records the classification of the material *as a device type* under one agency and one regulation. `products` records specific branded products and their individual submissions (a 510(k) number, a decision, a date, an indications-for-use statement). See [Regulatory status](regulatory.md).

## Standards

`Standard` rows: an identifier such as `ISO 4049:2019`, a title, the organization, and a URL.

## Evidence

Any of the rows above can carry `evidence`, a list of `EvidenceItem`:

```yaml
evidence:
- reference: PMID:24683067
  reference_title: Direct composite resin fillings versus amalgam fillings for permanent or adult posterior teeth.
  supports: SUPPORT              # SUPPORT | PARTIAL | REFUTE | NO_EVIDENCE | WRONG_STATEMENT
  evidence_source: SYSTEMATIC_REVIEW
  snippet: "resin restorations had a significantly higher risk of failure than amalgam restorations"
  explanation: Why this bears on the claim.
```

`snippet` must be an exact quote. For literature references (`PMID:`, `PMC:`, `DOI:`), `linkml-reference-validator` fetches the abstract and checks the quote verbatim. Regulatory sources are cited as `url:` and the validator skips fetching them (the FDA and eCFR sites block automated fetches), so the curator carries the burden of quoting them exactly.
