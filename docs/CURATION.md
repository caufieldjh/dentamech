# Curating DentaMech

## The loop

1. Pick a target. From the source queue, an issue, or a gap in `just report`.
2. Scaffold or open the record. `just new-record [--id ...] --name ... --apply`.
   An id with the OHD prefix also goes in `record_term`, with
   the ontology's label: add `--term-label "<label>"`.
3. Research. Fetch every source you cite: `just fetch-reference PMID:NNN`.
   Read what came back. For a thin record in a large literature,
   `just research PROVIDER <stem>` writes a deep-research report to
   `research/`: a list of leads to check, never a source to cite.
4. Write. Terms through `just search-term` and `just term-info`. Quotes
   copied from the fetched text and added with `just add-evidence`, which
   checks each quote against its source before writing it.
5. Validate. `just fill-titles kb/materials/<stem>.yaml --apply` fills
   any missing `reference_title` from the cache. Then
   `just validate kb/materials/<stem>.yaml` until clean. Then set
   `status: PROPOSED`, never `REVIEWED`.
6. Record. Append a `curation_history` event to the record. Add a history
   record with `just new-history ... --apply`.
7. Open a pull request. A person reviews it.

## Evidence

Every claim that could be wrong carries evidence:

```yaml
evidence:
  - reference: PMID:<number>
    reference_title: <title, as fetched>
    supports: SUPPORT        # SUPPORT, REFUTE, PARTIAL, NO_EVIDENCE, WRONG_STATEMENT
    evidence_source: IN_VITRO
    snippet: <exact text from the abstract or full text>
    explanation: <how the quote bears on the claim, in your words>
```

- The description is a claim too. Each fact in it is quoted in
  `description_evidence` (`just add-evidence FILE --at description ...`), or
  stated with evidence in a section. `just compliance` flags a description
  with no `description_evidence`, and review checks each fact.
- The snippet is checked verbatim against the cached source. `...` marks
  omitted text between two exact spans. `[...]` marks an editorial note.
  Nothing else may differ from the source.
- Cite the source that states the claim, not a review that cites a review.
- `REFUTE` evidence is kept. A record that shows disagreement is better
  than one that hides it. Open a `CONTROVERSY` discussion.
- No source found? Say so. Open a `KNOWLEDGE_GAP` discussion. Do not reach.

## Terms

- Search, then inspect. Read the definition and the parents before you bind.
- The label is copied from the ontology. `preferred_term` says it your way.
- A term that is not under the enum root fails validation. That usually
  means the wrong term, not the wrong root.
- A missing term is a finding. Record it as a `CURATION_TODO` and consider
  a new-term request to the ontology.

## Status

`DRAFT`, then `PROPOSED` when complete and valid, then `REVIEWED` when a
person accepts it. Agents never set `REVIEWED`. `DEPRECATED` keeps a record
for provenance.

## Dental rules

- `record_term.label` must match OHD exactly. Put friendlier names in `name` and `synonyms`.
- `parents` are the ids of other records, mirroring OHD's `is_a` links.
- Literature goes in as `PMID:` where a PMID exists, else `DOI:` or `PMC:`. Quotes are checked against abstracts. `.linkml-reference-validator.yaml` turns full-text fetching off so the check stays against abstracts.
- Regulatory text goes in as `url:` pointing at the CFR section, the FDA product classification record, or the 510(k) or PMA record. Those pages block automated fetches, so `url:` quotes are skipped by the validator and checked by people.
- Standards are cited as `url:` to the ISO or ADA catalog entry. Their text is paywalled, so keep the quote to what the catalog shows.
- Verified regulation numbers, classes and product codes are in `docs/regulatory.md`.
