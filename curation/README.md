# Curation inputs

`source_queue.tsv` ranks the sources that feed curation. One row per source.

| Column | Meaning |
|---|---|
| `rank` | Integer. 1 is next. |
| `source` | Name. |
| `url` | Landing page or API. |
| `kind` | `literature`, `database`, `knowledge_base`, `ontology`, `dataset`. |
| `license` | SPDX id or a short phrase. Unknown is written `UNKNOWN`, never guessed. |
| `status` | `CANDIDATE`, `EVALUATING`, `ADOPTED`, `REJECTED`. |
| `notes` | What it gives, what it costs, why the rank. |

A source is `ADOPTED` when code or a documented procedure that uses it is
merged, not when the row is edited. The `source-queue` skill triages the list.

## The paper log

`paper_log.tsv` records every paper considered as a source, whatever the
verdict, so no paper is read and judged twice. Its data model is the LinkML
schema `src/dentamech/schema/paper_log.yaml`: each row is a `PaperLogEntry`,
and the header is that class's slots in order.

| Column | Required | Meaning |
|---|---|---|
| `doi` | yes | Bare DOI in lower case, e.g. `10.1016/j.ajodo.2025.11.017`. |
| `considered_on` | yes | `YYYY-MM-DD`. |
| `verdict` | yes | `ACCEPT` (used as evidence), `REJECT` (not usable), `DEFER` (blocked; the note says by what). |
| `note` | yes | Why, in one or two sentences of your own. Never text from the paper. |
| `records` | no | Record stems in `kb/materials/` the paper fed, separated by `\|`. |
| `history` | no | Path of the session's `history/` record. |

The file is append-only. A paper that is reconsidered gets a new row; the
newest row for a DOI is its current verdict. Use the recipes rather than
editing by hand:

```bash
just lookup-paper 10.1016/j.ajodo.2025.11.017     # exit 1 if never considered
just log-paper 10.1016/j.ajodo.2025.11.017 REJECT --note "Why." --apply
just validate-paper-log                           # also part of `just qc`
```

`.gitattributes` merges this file with git's `union` driver, so two branches
that each append a row keep both rows instead of conflicting.
