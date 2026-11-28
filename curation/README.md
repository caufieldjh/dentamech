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
| `reference` | yes | The paper as a CURIE: `DOI:` and the DOI in lower case (`DOI:10.1016/j.ajodo.2025.11.017`) whenever it has one, `PMID:` and the PubMed id (`PMID:6948048`) only when it has none, so a paper never has two keys. |
| `considered_on` | yes | `YYYY-MM-DD`. |
| `verdict` | yes | `ACCEPT` (used as evidence), `REJECT` (not usable), `DEFER` (blocked; the note says by what). |
| `note` | yes | Why, in one or two sentences of your own. Never text from the paper. |
| `records` | no | Record stems in `kb/materials/` the paper fed, separated by `\|`. |
| `history` | no | Path of the session's `history/` record. |

The file is append-only. A paper that is reconsidered gets a new row; the
newest row for a paper is its current verdict. Use the recipes rather than
editing by hand. They take a DOI in any common form or `PMID:NNN`, and log a
PMID whose cached reference has a DOI under that DOI:

```bash
just lookup-paper 10.1016/j.ajodo.2025.11.017     # exit 1 if never considered
just lookup-paper PMID:6948048                    # a paper with no DOI
just log-paper 10.1016/j.ajodo.2025.11.017 REJECT --note "Why." --apply
just validate-paper-log                           # also part of `just qc`
just paper-log-cited                              # also part of `just qc`
```

On a pull request, CI fails if a row already on the base branch was edited
or removed, or if a new row names a record or history file that does not
exist (`just paper-log-append origin/main`; fetch `origin/main` first, or it
stops with an error). It warns for each paper a
changed record newly cites that has no row (`just paper-log-coverage --base
origin/main <files>`). The curation scanner and the review agent both read
the log.

`just qc` also fails if any paper a record cites (a `DOI:` or `PMID:`
reference) has no `ACCEPT` row naming that record (`just paper-log-cited`).
It works offline: a PMID is resolved to its DOI through `references_cache/`,
so fetch a new reference before logging it. Regulations, web pages and
standards are not papers and are not checked.

Until #73 the log was keyed by a bare `doi` column. `check-append` migrates a
base still in that form before comparing, and `python -m dentamech.paper_log
migrate --apply` rewrites such a file.

Links are checked only when a row is new. `just validate-paper-log` does not
check that an older row's records and history still exist. A record may later
be renamed, merged or removed, and the old row can't be edited to follow it.

`.gitattributes` merges this file with git's `union` driver, so two branches
that each append a row keep both rows instead of conflicting. That holds for
merges made with git itself. GitHub's merge button may not use the driver, so
two pull requests that both add rows can still show a conflict on GitHub.
If one does, merge the base branch into the pull request's branch locally and
push; the union driver keeps both rows.
