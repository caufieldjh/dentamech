# Curating DentaMech

## The loop

1. Pick a target. From the source queue, an issue, or a gap in `just report`.
2. Scaffold or open the record.
   `just new-record [--id ...] --name ... --category ... --apply`.
   An id with the OHD prefix also goes in `record_term`, with
   the ontology's label: add `--term-label "<label>"`. An experimental
   material adds `--experimental --purpose ...`, and `--restorative-class ...`
   when the purpose is RESTORATIVE.
3. Research. Before reading a paper, check whether it was considered
   already: `just lookup-paper <DOI>`. Fetch every source you cite:
   `just fetch-reference PMID:NNN`. Read what came back. Log every paper
   you considered, whatever the verdict:
   `just log-paper <DOI> ACCEPT|REJECT|DEFER --note "..." --apply`. For a thin record in a large literature,
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

- `record_term.label`, when the record has one, must match OHD exactly. Put friendlier names in `name` and `synonyms`.
- `parents` are the ids of other records, mirroring OHD's `is_a` links.
- Literature goes in as `PMID:` where a PMID exists, else `DOI:` or `PMC:`. Quotes are checked against abstracts. `.linkml-reference-validator.yaml` turns full-text fetching off so the check stays against abstracts.
- A quote from the full text of a closed paper is allowed when you hold a copy. Cite it as `DOI:`, put the text in `local_full_text/` (gitignored) named by cache stem, validate, then `just sign-excerpts FILE --reference DOI:...` and commit the bundle in `reference_excerpts/`. Never commit the paper. See `reference_excerpts/README.md`.
- Regulatory text goes in as `CFR:872.NNNN` for a 21 CFR section; its quotes are checked against the eCFR text. The FDA product classification record and the 510(k) or PMA record go in as `url:`; the validator skips `url:`, so those quotes are checked by people (see `docs/regulatory.md`).
- A quote from the text of an ISO standard goes in as `ISO.<number>:<part>_<year>_<edition>`, checked against a local copy and signed into `reference_excerpts/`, as for a closed paper; see the `evidence-references` skill. Everything else about a standard is cited as `url:` to its catalogue entry: ADA standards, ISO documents the `ISO.` form cannot hold yet (technical specifications and reports, amendments), and catalogue facts such as edition or scope when nobody holds a copy. Keep those quotes to what the catalogue page shows.
- Verified regulation numbers, classes and product codes are in `docs/regulatory.md`.
