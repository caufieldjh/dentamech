# Design decisions

The decision register, in the style of [DisMech's](https://github.com/monarch-initiative/dismech/blob/main/docs/explanation/design-decisions.md). It records why the project is built the way it is. Change a decision by opening an issue, then updating this page and the schema in the same pull request.

## 1. Scope

**Decision.** One entry per dental restoration material as OHD defines it. The knowledge base covers composition, setting, clinical use, performance, safety, regulatory status, standards, and commercial products.

**In scope.** Any material under `OHD:0000000`. Product-level records are in scope when they carry a regulatory decision worth recording.

**Out of scope.** Equipment (curing lights, handpieces), procedures as such, and clinical guidance. The knowledge base describes materials; it does not tell anyone what to put in a tooth.

## 2. Anchor ontology

**Decision.** OHD is the anchor. Every entry binds exactly one OHD term, and the parent links mirror OHD's subclass hierarchy.

**Rationale.** OHD is the OBO Foundry ontology for oral health, its materials branch already has definitions for the classes clinicians recognize, and it is small enough to validate locally. Where OHD lacks a material, the right move is to request the term upstream, not to mint one here.

**Consequence.** The seeder derives the whole tree from OHD, and a new OHD release can add entries without touching curated files.

## 3. Schema framework

**Decision.** LinkML, for the same reasons DisMech chose it: YAML authoring, ontology-bound dynamic enums validated by `linkml-term-validator`, verbatim-quote validation by `linkml-reference-validator`, and generated Python, JSON Schema, and documentation from one source.

## 4. Regulatory model

**Decision.** Two levels. Device-type classification (`regulatory_status`) is separated from product-level decisions (`products[].submissions`).

**Rationale.** FDA's classification regulations describe device *types* and their intended uses; 510(k) clearances belong to *products*. Folding them together would force a choice between duplicating the regulation on every product or losing the product-level indications statement. Keeping both levels means the "what is it approved for" question can be answered at the level the source answers it.

**Decision.** `regulation_number`, `product_codes`, and `submission_number` are validated by pattern, and `identification` is the regulation's own text quoted verbatim.

**Rationale.** These are the join keys to FDA's public databases. A malformed one is worse than a missing one.

**Decision.** Agencies other than FDA are in the enum from the start.

**Rationale.** Cheap now, painful later.

## 5. Evidence policy

**Decision.** The DisMech evidence model, unchanged: reference, verbatim snippet, support level, source type, explanation. Snippets from literature are machine-checked; snippets from regulatory pages are not, because those sites block automated fetches.

## 6. Ontology set

**Decision.** OHD (materials and procedures), CHEBI (chemistry), UBERON (anatomy), HP and MONDO (adverse effects), PATO (qualities), NCIT (mappings only). The list is enforced by `conf/oak_config.yaml`.

**Deferred.** SNOMED CT and CDT codes as mappings; MeSH for literature retrieval; ISO 1942 vocabulary alignment.

## 7. Categories as a slot, not just ancestry

**Decision.** `category` is an explicit required slot even though it could be derived from OHD ancestry.

**Rationale.** The browser needs it without an ontology in the loop, and some materials (compomers, resin-modified glass ionomers) belong to a category the ontology's tree does not express as a single branch.

## 8. Built on mechmaker

**Decision.** The project was converted to a [mechmaker](https://github.com/monarch-initiative/mechmaker) Mech. It started from `linkml-project-copier`, so `sync-mech` could not follow it. The domain schema, the OHD seeder, and the FDA rules were kept; mechmaker supplies the record contract, the gates, the site, and the workflows.

**Consequences.**

- Records are keyed by `id` and named in `record_term`. `curation_status` became `status`, and all 57 records converted as `DRAFT`. `just compliance` now shows how complete a record is.
- Filenames are lowercase, derived from `name`, and `parents` hold ids.
- `pages/` is no longer committed, and the faceted `app/` browser is replaced by the filterable table on the site's Records page.
- `.copier-answers.yml` names mechmaker, so `sync-mech` works from here on.

## 9. Abstract-only quote checks

**Decision.** `linkml-reference-validator` runs with full-text fetching off and with cached entries trusted.

**Rationale.** Evidence quotes are checked against abstracts. By default the validator fetches publisher full text and rewrites the committed cache, so a quote from outside the abstract could pass.

## 10. Open questions

- Whether product records should live in their own files once there are many.
- Whether to model *material systems* (a bonding agent plus its composite) as a separate class.
- How to represent regional restrictions such as amalgam phase-down commitments under the Minamata Convention. For now they go in `restrictions` and `notes`.
