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

See decision 9 in `docs/explanation/design-decisions.md`.
