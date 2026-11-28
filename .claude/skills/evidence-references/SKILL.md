---
name: evidence-references
description: >-
  Find, fetch, quote and validate the evidence behind a claim in DentaMech.
  Use when adding or fixing an `evidence` item, when a snippet fails
  reference validation, when choosing between sources, or when asked whether
  a claim is supported.
---

# Evidence and references

Every evidence item is checked by `linkml-reference-validator`. It fetches
the cited source, caches it under `references_cache/`, and requires the
snippet to appear in it verbatim.

Regulation text is cited as `CFR:872.NNNN` and checked the same way, against
the section as eCFR serves it (`src/dentamech/refsources.py`). The validator
skips `url:` and `FDA_PRODUCT_CODE`, so quotes from FDA database pages are
still checked by people.

An ISO standard is cited as `ISO.<number>:<part>_<year>_<edition>`:
`ISO.20795:1_2013_2` is ISO 20795-1:2013, second edition, and a standard
without parts drops the part (`ISO.4049:2019_5`). Each standard is its own
prefix, so declare `ISO.<number>` in the schema's `prefixes` before citing it
(a test checks). Standards are sold, not published: nothing is fetched, and a
quote is checked against a local copy and signed, as for a closed paper (see
`reference_excerpts/README.md`). Take the part, year and edition from the
document's cover page, never from a catalogue URL, and set `evidence_source:
STANDARD`. `reference_title` is the title on the cover page.

The form holds one numeric part and nothing else. An ISO/TS or ISO/TR
document (e.g. ISO/TS 11405), an amendment, or a multi-level part cannot be
cited this way yet. Never squeeze one in, say by putting `Amd 1` into the
edition field. Cite its catalogue entry as `url:`, and open an issue to extend
`ISO_REFERENCE` in `src/dentamech/refsources.py`: the form is a schema and
policy decision, since it fixes reference ids and bundle filenames.

## Writing an item

1. Find a primary source that states the claim. Prefer the paper that
   showed it over a review that repeats it. Check whether it was considered
   before: `just lookup-paper <DOI|PMID:NNN>`. A paper logged `REJECT` is not cited
   unless you have a new reason, recorded in a new row.
2. Fetch it and read it:

   ```bash
   just fetch-reference PMID:<n>
   ```

3. Copy the snippet from the fetched text. `...` joins two exact spans.
   `[...]` marks an editorial note. Nothing else may differ.
4. Add it with `just add-evidence`. `--at` names where it goes: `record` for
   the record's own evidence, or a path to one entry of a section, such as
   `<section>[0]` or `<section>[2].<subsection>[1]`:

   ```bash
   just add-evidence kb/materials/<stem>.yaml --at <place> \
     --ref PMID:<n> --snippet "<verbatim>" --source <EvidenceSourceEnum value> \
     --explanation "<how it bears on the claim>" --model <model-id>
   ```

   That is a dry run: it fetches the source if needed, checks the quote with
   the same validator `just validate` uses, fills `reference_title`, and
   prints the diff. Add `--apply` to write it. It also appends a
   `curation_history` event, and refuses a quote it cannot find, a
   duplicate, or a place the schema gives no `evidence`.

   The item it writes:

   ```yaml
   - reference: PMID:<n>
     reference_title: <as fetched>
     supports: SUPPORT
     evidence_source: <EvidenceSourceEnum value>
     snippet: <verbatim>
     explanation: <how it bears on the claim>
   ```

   An item written another way, by hand or by a conversion script, gets its
   title from the cache with `just fill-titles <file> --apply`.

5. Validate the whole record once its evidence is in:

   ```bash
   just validate kb/materials/<stem>.yaml
   ```

## `supports`

| Value | When |
|---|---|
| `SUPPORT` | The quote states or directly shows the claim. |
| `PARTIAL` | It supports part of the claim, or with a caveat that matters. |
| `REFUTE` | It contradicts the claim. Keep it. Open a `CONTROVERSY` discussion. |
| `NO_EVIDENCE` | Relevant context that does not bear on the claim. |
| `WRONG_STATEMENT` | The claim was found wrong. Kept for provenance. |

## When validation fails

- **Snippet not found.** Your quote differs from the source. Fetch again and
  copy. If the text is in the full paper but only the abstract is cached,
  quote the abstract, find an open-access copy, or, if a curator holds a
  copy of the closed paper, use a signed excerpt (see Closed papers below).
  Do not paraphrase.
- **Snippet not found, signed excerpt.** The quote is not in the bundle in
  `reference_excerpts/`, or the bundle entry has no `verification` record.
  Re-run `just sign-excerpts` with the paper in `local_full_text/`. Never
  write or edit a bundle by hand.
- **Reference not found.** The identifier is wrong. Search PubMed for the
  title. Never adjust digits until something resolves.
- **Unknown prefix.** The reference type is not supported by the validator.
  Use a PMID or DOI for the same work.

Every paper you read for a claim gets a row in the paper log, cited or not:
`just log-paper <DOI|PMID:NNN> ACCEPT|REJECT|DEFER --note "..." [--record <stem>] --apply`.
The note is your reason, never text from the paper. Pass the PMID as cited:
`log-paper` logs it under the DOI in its `references_cache/` file when there is
one, and as `PMID:NNN` when there is none. `just qc` fails unless, for each cited
paper, the newest row naming the citing record is `ACCEPT`.

## Closed papers: signed excerpts

Quotes from a closed paper's full text are allowed when a local copy exists.

1. The text goes in `local_full_text/<cache stem>.md` (gitignored), e.g.
   `DOI_10.1016_j.x.2025.11.017.md`. Never copy it anywhere tracked.
2. Cite `DOI:`, quote verbatim, and `just validate` the record. Matching uses
   the local copy.
3. `just sign-excerpts kb/materials/<stem>.yaml --reference DOI:...` writes
   the matching quotes, and only those, to `reference_excerpts/`.
4. Commit the record and the bundle. Check `git status` first: no paper text
   may be staged, in `references_cache/` or anywhere else.

Without the local copy (in CI, or on another machine), the same quote passes
only through the signed bundle.

Fair-use caps bound what is quoted: 1,000 characters a quote, 600 an unbroken
part, 6,000 from one source across the corpus, and 10% of a local copy per
bundle (counts exclude whitespace; `reference_excerpts/README.md`). They bind
every source, abstracts and CFR included. On "too long for fair use", cut the
quote to what the claim needs, or split it with `...`. On "Cumulative quoted
text ... exceeds", the source is quoted enough already: reuse a quote that is
there, or cite a different source.

## When no source exists

Do not reach. Write the claim as a `KNOWLEDGE_GAP` discussion with
`rationale` saying what evidence would settle it. Sketch a
`proposed_experiments` entry if one is obvious.
