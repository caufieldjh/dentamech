# Design decisions

The decision register, in the style of [DisMech's](https://github.com/monarch-initiative/dismech/blob/main/docs/explanation/design-decisions.md). It records why the project is built the way it is. Change a decision by opening an issue, then updating this page and the schema in the same pull request.

## 1. Scope

**Decision.** One entry per dental material, whatever its purpose (restorative, preventive or auxiliary), keyed by its OHD term where OHD has one and by a minted id where it does not. The knowledge base covers composition, setting, clinical use, performance, safety, regulatory status, standards, and commercial products.

**In scope.** Any material under `OHD:0000000`. Any other dental material, restorative or not, commercial or experimental, with or without an OHD term: denture base materials (ISO 20795-1; issue #51), impression materials, sealants, an experimental formulation reported in research, marked `experimental` (issue #50). Product-level records are in scope when they carry a regulatory decision worth recording.

**Rationale for the widening.** The project's dental materials expert answered issues #50 and #51: denture base materials are a class of materials specified by their own ISO standard, and experimental materials should be recorded, labelled as experimental and placed in a classification by purpose (section 11). Deferring every paper about a material OHD lacks left real literature unusable. The maintainer then widened the scope deliberately, in review of #53: the project is still in development, OHD is not comprehensive, and curating materials OHD lacks is how DentaMech will find the terms to request from OHD or elsewhere. The scope is broad on purpose; narrowing it later is a decision to record here.

**Out of scope.** Equipment, instruments and devices that are not materials (curing lights, handpieces), procedures as such, and clinical guidance. Purpose is not a boundary. The knowledge base describes materials; it does not tell anyone what to put in a tooth.

## 2. Anchor ontology

**Decision.** OHD is the anchor. Every entry whose material OHD has binds exactly one OHD term, and the parent links mirror OHD's subclass hierarchy. An entry whose material OHD lacks gets a minted `dentamech:<uuid>` id, leaves `record_term` unset, and is re-grounded when OHD adds the term. Its parent links are the curator's choice of the closest record, not OHD links. The seeder and the identity root (`OHD:0000000`) still cover the restoration branch only; an OHD term for a non-restorative material elsewhere in OHD needs the identity root widened first.

**Rationale.** OHD is the OBO Foundry ontology for oral health, its materials branch already has definitions for the classes clinicians recognize, and it is small enough to validate locally. Where OHD lacks a material, request the term upstream, and meanwhile record the material under a minted id rather than leave its literature unused. A minted id is a placeholder for a term, never a term: nothing outside this knowledge base should treat it as an ontology class.

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

## 9. Quote checks: abstracts, plus signed excerpts from closed papers

**Decision.** `linkml-reference-validator` runs with full-text fetching off and with cached entries trusted, so fetched sources are checked against their abstracts. Quotes from the full text of a closed paper are allowed when a curator holds a copy: the quote is checked against that local copy, and the quotes that match are written as signed excerpts to `reference_excerpts/`, which is committed. The paper itself never is.

**Rationale.** By default the validator fetches publisher full text and rewrites the committed cache, so a quote from outside the abstract could pass with nothing a reviewer can see. Many dental materials papers are closed, and their abstracts leave out the composition and setting details records need. Signed excerpts keep those quotes checkable in CI without redistributing the paper.

**Consequences.**

- Local copies go in `local_full_text/`, named by cache stem (e.g. `DOI_10.1016_j.x.2025.11.017.md`). It is gitignored, as are DOI-named folders at the repo root. Since linkml-reference-validator 0.8.0, a local file's text is never written to `references_cache/`.
- `just sign-excerpts` writes a bundle per reference. Each excerpt carries a `verification` record with the SHA-256 of the text it matched. `signed_excerpts_require_verification: true` makes validation ignore entries without one, so a hand-typed excerpt fails.
- The record is an attestation, not a cryptographic signature. Anyone who can edit a bundle can edit its record. Review is the safeguard: a bundle change should add only quotes that appear as snippets in the same pull request.
- A quote from a local copy is limited by the validator's fair-use caps.

## 10. Open questions

- Whether the classification by purpose (section 11) should be set on every record, and how it relates to `category` once it is.
- What evidence an experimental record needs: whether one in vitro or animal study is enough, or whether there is a minimum.
- Whether `purpose` should allow more than one value, for a material that is, say, both restorative and preventive.

- Whether product records should live in their own files once there are many.
- Whether to model *material systems* (a bonding agent plus its composite) as a separate class.
- How to represent regional restrictions such as amalgam phase-down commitments under the Minamata Convention. For now they go in `restrictions` and `notes`.

## 11. Classification by purpose, beside category

**Decision.** Three optional slots: `experimental` (boolean), `purpose` (`PREVENTIVE`, `AUXILIARY`, `RESTORATIVE`) and `restorative_class` (`CERAMIC`, `COMPOSITE`, `POLYMER`, `METAL`, for a restorative material only). An experimental record must give `purpose`, and `restorative_class` when it is restorative. `just validate` enforces this.

**Rationale.** This is the hierarchy the project's dental materials expert proposed for experimental materials (issue #50): first what the material is for, then, for a restorative material, what class of material it is. It is kept separate from `category` (section 7) because the two answer different questions, and because `category` has places for cements, adhesives and hybrids that the restorative classes do not. Folding one into the other would have meant re-sorting every record on a scheme proposed for experimental materials.

**Consequence.** No existing record changed. A record outside the experimental set may carry the classification; none is required to.
