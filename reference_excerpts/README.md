# reference_excerpts

Signed excerpts: quotes from closed papers, checked against a local copy of
the paper, so the check can be repeated without the paper.

Each `<cache stem>.yaml` bundle holds the reference id, its title, the length
of the text it was checked against, and the quotes that matched, each with a
`verification` record (`method`, `source_sha256`, `validator_version`,
`verified_at`). Nothing else from the paper is written.

Write bundles with `just sign-excerpts`. Never write or edit one by hand.
`.linkml-reference-validator.yaml` sets
`signed_excerpts_require_verification: true`, so an entry without a
verification record is ignored and its quote fails. The record is an
attestation, not a cryptographic signature. A reviewer checks it the same way
as any other change: the bundle's quotes should match the record's snippets,
and the diff should show only those quotes.

Workflow:

1. Put the paper's text in `local_full_text/` (gitignored) as
   `<cache stem>.md` or `.txt`, e.g. `DOI_10.1016_j.x.2025.11.017.md` for
   `DOI:10.1016/j.x.2025.11.017`.
2. Cite it as `DOI:` in the record and quote it verbatim.
3. `just validate kb/materials/<stem>.yaml` checks the quote against your copy.
4. `just sign-excerpts kb/materials/<stem>.yaml --reference DOI:...` writes
   the bundle here.
5. Commit the record and the bundle. Never commit the paper.

## ISO standards

A standard goes the same way, cited as `ISO.<number>:<part>_<year>_<edition>`
(e.g. `ISO.20795:1_2013_2`; see the `evidence-references` skill). Nothing is
fetched for an `ISO.` reference, so the local copy supplies the title too:

1. Convert the PDF to text (`pdftotext`, without `-layout`) and save it as
   `local_full_text/<cache stem>.md`, e.g. `ISO.20795_1_2013_2.md`.
2. Make its first line `# <title exactly as on the cover page>`. The title
   check compares `reference_title` with this line, so it only checks what
   the curator typed against what the curator typed: copy it, don't retype it.
3. Delete the running header, footer and licence lines that repeat on every
   page. A quote that crosses a page break fails while they are there.
4. Then steps 2 to 5 above, citing `ISO.` instead of `DOI:`.

The bundle holds only the quotes. A purchased copy is usually stamped with
the licensee's name; that stamp stays in the local copy and never goes in a
record, a commit, or a pull request.

See decision 9 in `docs/explanation/design-decisions.md`.
