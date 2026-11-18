---
name: review-record
description: >-
  Audit one DentaMech record, or a pull request that changes records,
  without editing anything. Use when asked to review, check, audit or assess
  a dental material record or a curation pull request. Produces findings;
  changes nothing.
---

# Review a record

Read only. The output is a list of findings, each with a location and a
reason. Fixes belong to `curate-record`, in a separate step, when asked.

## Checks, in order

1. **Machine checks.** `just validate kb/materials/<stem>.yaml`. Every
   error is a finding. A clean run proves the citations exist, the quotes are
   exact and the terms are real. It proves nothing else.
2. **Scope.** Is this one dental material by the rules in `docs/DOMAIN.md`?
   Is it a duplicate of another record?
3. **Quote fit.** For each evidence item, read the snippet against the claim
   it is attached to. A real quote under the wrong claim passes validation and
   is still wrong. This is the check machines cannot do.
4. **Term fit.** Is each bound term the most specific accurate one? Is a
   broad binding explained in `notes`?
5. **Direction.** Does `supports` match what the quote says?
6. **Description.** Take each fact the `description` states (a date, a
   place, a use, a number). Each needs a quote: in `description_evidence`,
   or in the section that states the same fact. A fact with neither is an
   `error`, even when it is true.
7. **Gaps.** What does the record claim with no evidence? What is missing
   that the sources would support?

8. **Regulatory accuracy.** For every `regulatory_status` item with `agency: FDA`:
   - `regulation_number` exists in 21 CFR 872, and `regulation_title` matches the CFR device name.
   - `device_class` matches paragraph (b) of that section.
   - `product_codes` are listed under that regulation in the FDA product classification database.
   - `identification` is paragraph (a) verbatim.
   - `approved_uses` restate what the identification paragraph permits and nothing more.
   - `status` fits the pathway: `EXEMPT` with a 510(k) exemption, `CLEARED` with a 510(k).

   Check against the cached section (`references_cache/CFR_872.NNNN.md`), the FDA search in `curate-record`, and `docs/regulatory.md`. Quotes cited as `CFR:` are machine-checked, but whether they support the claim is not. Quotes from FDA database pages are cited as `url:` and are not machine-checked, so this check is the only one they get. A wrong regulatory fact is an `error`.
9. **Science.** Do composition, properties and uses match the literature for this material at this level of the OHD tree? Do values carry units and a method?
10. **Paper log.** Every paper the record newly cites should have a row in
    `curation/paper_log.tsv` (`just paper-log-coverage --base origin/main kb/materials/<stem>.yaml`
    lists the missing ones). For each new row, check:
    - `ACCEPT` rows name the records that cite the paper, and no cited paper is logged `REJECT`.
    - A `REJECT` or `DEFER` reason is sound, and a `DEFER` names what blocks it.
    - The note is the curator's own words, never text copied from the paper.
    - No earlier row was edited or removed, and the records and history new rows name exist
      (`just paper-log-append origin/main`).

    A missing row is a `warning`. Copied paper text in a note is an `error`.

## Output

A table: location (section and item), finding, severity (`error`, `warning`,
`note`), and the evidence for the finding. End with a verdict: approve,
approve with notes, or changes needed. If you were asked to record the
review, add a history record with `--event REVIEW`, and `--outcome no_change`
when you changed nothing.
