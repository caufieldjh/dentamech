---
name: dentamech-pr-review
description: >
  Review a pull request that changes kb/materials/ entries for scientific
  validity, regulatory accuracy, ontology term correctness, evidence quality,
  and schema conformance. Use for PR review requests and as a self-review
  before opening a curation PR.
---

# dentamech-pr-review

## Gather

```bash
gh pr view <N> --json title,body,files,headRefName
gh pr diff <N>
```

For each changed `kb/materials/*.yaml`, run the real checks rather than
eyeballing:

```bash
just validate kb/materials/<File>.yaml
just validate-references kb/materials/<File>.yaml
uv run pytest -q
```

## Check, in this order

1. **Identity.** `material_term.term.id` is under OHD:0000000 and the label is
   OHD's label verbatim. `parents` name real entries. `category` fits.
2. **Regulatory accuracy.** For every `regulatory_status` entry with `agency: FDA`:
   - `regulation_number` exists in 21 CFR 872 and its `regulation_title` matches the CFR device name.
   - `device_class` matches paragraph (b) of that section.
   - `product_codes` are listed under that regulation in the FDA product classification database.
   - `identification` is paragraph (a) verbatim.
   - `approved_uses` restate what the identification paragraph permits and nothing more.
   - `status` is consistent with the pathway (EXEMPT with EXEMPT_510K; CLEARED with 510(k)).
   Verify against `https://www.law.cornell.edu/cfr/text/21/872.NNNN` and the FDA database search URL in the curate-material skill. Cross-check `docs/regulatory.md`. A product-level record (K-number) under `regulatory_status` instead of `products` is an IMPORTANT finding.
3. **Evidence quality.** Every literature snippet passes the reference validator. `evidence_source` describes the source type correctly (a Cochrane review is SYSTEMATIC_REVIEW, a bench study is IN_VITRO). `supports` is honest: a snippet that only partly backs the claim is PARTIAL.
4. **Ontology terms.** CHEBI, UBERON, HP, MONDO, PATO, and OHD procedure terms exist and are specific. A generic term where a specific one exists is a SUGGESTION; a wrong term is IMPORTANT.
5. **Science.** Composition, properties, and uses match the literature for this material at this level of the OHD tree. Values carry units and a method. Claims about comparators name the comparator.
6. **Hygiene.** No hand-written `references_cache/` files. No `pages/` or `app/` changes in a curation PR. `curation_status` reflects what is actually filled.

## Report

Lead with a checklist:

- [ ] Schema and term validation pass
- [ ] Reference validation passes (all snippets verbatim)
- [ ] FDA regulation, class, and product codes verified against source
- [ ] Identification text verbatim; approved uses match it
- [ ] Ontology terms correct and specific
- [ ] evidence_source and supports values honest
- [ ] No cache or page files hand-edited

Then findings by severity:

- 🔴 CRITICAL: wrong regulatory fact, hallucinated PMID, failing validation, snippet not verbatim
- 🟡 IMPORTANT: wrong ontology term, misfiled product record, wrong evidence_source, missing regulation for a stated class
- 🔵 SUGGESTION: more specific term, extra property, style

Submit the review with `gh pr review <N> --request-changes` when any CRITICAL
or IMPORTANT finding stands, else `gh pr review <N> --approve`. Approving is
allowed and expected once blocking items are cleared; a comment does not clear
a CHANGES_REQUESTED review.
