# CLAUDE.md

Operational guidance for Claude Code and other agents in this repository.
`AGENTS.md` points here.

## What this is

DentaMech (Dental Materials Knowledge Base) is a Mech: an AI agent-curated,
ontology-grounded, evidence-backed knowledge base. DentaMech records dental materials, restorative and otherwise: composition, setting, clinical use, performance, adverse effects, regulatory status and standards, one record per material, grounded to OHD where it has a term, with every claim quoted from its source.

One record is one dental material. One record is one YAML file under
`kb/materials/`, validated against the `DentalMaterial` class in
`src/dentamech/schema/dentamech.yaml`.

The pattern comes from [DisMech](https://github.com/monarch-initiative/dismech).
mechmaker's [design decisions](https://monarch-initiative.github.io/mechmaker/design/) apply to
every Mech. Where this one adapts them, `docs/DOMAIN.md` says how.
The registry of Mechs is [MechRegistry](https://github.com/monarch-initiative/mechregistry).

Read before changing domain content:

- `docs/DOMAIN.md`: what a record is, what it is not, identity, granularity.
- `docs/CURATION.md`: evidence rules, the curation loop, review.
- `curation/source_queue.tsv`: the sources that feed curation, ranked.

## Commands

```bash
just                   # list every recipe
just install           # uv sync
just qc                # the offline gate CI blocks on
just qc-full           # qc plus terms and quotes for every record (network)
just validate FILE     # closed schema, ontology terms, verbatim quotes
just sign-excerpts FILE --reference DOI:...   # sign quotes from a local closed paper into reference_excerpts/
just new-record ...    # scaffold a record (dry-run unless --apply); an id with the OHD prefix needs --term-label
just import-schema SRC --record-class C   # start the schema from an existing one (dry-run unless --apply)
just new-history ...   # scaffold a history record (dry-run unless --apply)
just add-evidence FILE --at PLACE --ref REF --snippet "..."   # checked evidence (dry-run unless --apply)
just convert scripts/convert_X.py --limit 5   # convert an existing knowledge base (dry-run unless --apply)
just fetch-reference PMID:NNN   # fetch and cache a source; read it before quoting it
just fill-titles [FILE...]      # fill missing reference_title from the cache (dry-run unless --apply)
just search-term PREFIX "text"  # search an ontology through its configured adapter; "l~text" for a partial label match
just term-ancestors CURIE       # where a term sits; use when an enum root rejects it
just term-parents CURIE         # direct is-a parents
just check-identity [FILE...]   # record ids follow the identity enum's rule (network, in qc-full)
just report            # corpus statistics
just compliance        # completeness per record, lowest first
just export            # every format in conf/export.yaml, into build/export/, each read back
just load TARGET       # fill a database in conf/load.yaml (MongoDB, Neo4j); --replace to overwrite
just labels            # create the GitHub labels the workflows use
just docs-serve        # the documentation site at http://127.0.0.1:8000
just site-check        # check conf/site.yaml: colors, theme, contrast
just research-providers         # which deep-research providers are ready here
just research PROVIDER TARGET   # a deep-research report on one record (costs a run)
```

Quote counts from `just report` or a live command, never from prose.

## Rules that matter most

- **Never guess a CURIE.** Look it up with `just search-term` and
  `just term-info`. An unverified ontology term, PMID or accession is worse
  than none. Leave `term` unset, keep `preferred_term`, and open a
  `CURATION_TODO` discussion.
- **A label is the ontology's label.** `term.label` must match the ontology
  exactly. Put nuance in `preferred_term`, never in `label`.
- **A snippet is a verbatim quote.** Fetch the source with
  `just fetch-reference`, copy the text, and add it with `just add-evidence`,
  which checks the quote before writing. Paraphrase goes in `explanation`.
  `just validate-references` fails a paraphrase, and it should.
- **Bind the most specific accurate term.** If only a broad term fits, bind
  it and say so in `notes`. Do not bind a narrow term because it exists.
- **A deep-research report is a lead, never a source.** Never cite one in a
  record. Fetch the primary source it points to and quote that.
- **Declare every prefix.** Each CURIE prefix a record uses has its full
  URI in the schema's `prefixes`. The RDF exports depend on it, and
  `just export` fails on a prefix with no URI.
- **Closed schema.** An unknown field is an error. If the schema lacks a
  place for something real, use the `extend-schema` skill. Do not stuff it
  into `notes`.
- **An agent takes a record no further than `PROPOSED`.** It starts `DRAFT`
  and becomes `PROPOSED` when complete and valid. Promotion to `REVIEWED`
  is a human decision, recorded as a human `REVIEW` event.
- **Record what you did.** Every change appends a `curation_history` event
  to the record, and every session adds a history record with
  `just new-history ... --apply`. Fill `--details`.

## Files not to edit here

- `src/dentamech/schema/mech_shared.yaml` and
  `src/dentamech/schema/history.yaml` are vendored byte-identical from
  the Mech fleet canon. A test checks their hashes. Change them upstream.
- `pages/` is generated by `just render`, for a local look, and not
  committed. Edit `src/dentamech/templates/` instead. A Mech made
  from an older template may still track it: `git rm -r --cached pages`.
- `docs/elements/`, `docs/schema/`, `docs/records/`, `docs/structure.md`,
  `docs/corpus.md`, `docs/downloads.md` and `.mkdocs.site.yml` are generated
  by `just docs-build` and not committed. Colors and layout settings live in
  `conf/site.yaml`. Improve a schema page by improving the schema's
  descriptions. The Downloads page follows `conf/export.yaml`.
- `cache/` and `references_cache/` are written by the validators. Commit
  them. Never hand-edit a row.
- `.copier-answers.yml` is written by Copier. To take newer template
  changes from mechmaker, follow mechmaker's `sync-mech` skill
  (`npx skills add monarch-initiative/mechmaker`): it shows each change,
  lets the person choose, and migrates records where a change needs it.
  `just update-template` takes every change at once.

## Skills

Project skills live in `.claude/skills/`. Use them.

| Skill | Use it to |
|---|---|
| `curate-record` | create or improve one record end to end |
| `ontology-terms` | choose, bind, check or repair a term |
| `evidence-references` | find a source, quote it, validate the quote |
| `review-record` | audit one record without editing it |
| `extend-schema` | change the data model and migrate records |
| `source-queue` | triage the sources that feed curation |
| `github-workflows` | turn on, configure, adapt or debug the GitHub workflows |
| `site-design` | change how the documentation site and record browser look |
| `deep-research` | run deep research on a record, and turn its leads into evidence |
| `curate-mappings` | map a record to identifiers elsewhere, with evidence, for the SSSOM export |


## Workflows

`docs/WORKFLOWS.md` lists every GitHub workflow, on or off. Agent workflows
read their prompts from `.github/prompts/` and their models from
`.github/agent-config.yaml`. When you run inside one, the prompt is your
task; this file and the skills still apply. Turn workflows on or off through Copier, never by copying
files; see the `github-workflows` skill.

## Git

One pull request per coherent change. The pull request is the human review
gate. Do not merge without approval.

**Work in worktrees.** The primary checkout (wherever the repository was
cloned) always stays on the default branch. Branches live only in worktrees,
so two sessions never share one set of files.

- Start each change with `just worktree <branch>`. It makes the branch from
  origin's default branch, in `~/worktrees/<checkout folder>/<branch>`, and prints
  the path; work there. In a cloud session or a CI job that gave you a fresh
  clone and a branch to work on, use that clone instead.
- Never leave the primary checkout on a branch, and never check out the
  default branch in a worktree. If `git checkout main` says it is already
  checked out, `git worktree list` shows where.
- A worktree with no `.venv` of its own uses the primary checkout's, so run
  `just install` in the primary checkout, not in each worktree. A branch that
  changes `pyproject.toml` or `uv.lock` gets its own: run `just install`
  there. Only `just` recipes and the record hook know this: a bare `uv run`
  in a worktree builds a new `.venv`, so run commands through `just`.
- Commands find the repository from the working directory
  (`repo_root()` in `src/dentamech/paths.py`), so run them inside the
  worktree. Set `DENTAMECH_ROOT` to name a checkout explicitly. In code, build
  repository paths from `REPO_ROOT`, never from `__file__`; `__file__` is only
  for files inside the package.
- Stage files by name (`git add kb/materials/ references_cache/`). Never
  `git add -A` or `git add .`.
- After a pull request merges, `just worktree-clean` removes its worktree and
  branch.

## Dental rules

- **One OHD term per record, where OHD has the material.** `record_term.label` must match OHD exactly. Put friendlier names in `name` and `synonyms`.
- **Scope is every dental material.** Restorative, preventive or auxiliary; commercial or experimental. A material OHD lacks (e.g. denture base resin, an impression material) gets a minted id (`just new-record` without `--id`), no `record_term`, and a `CURATION_TODO` discussion proposing the term to OHD or another ontology. See `docs/DOMAIN.md`, Identity.
- **Experimental materials are classified.** `experimental: true` needs `purpose` (`PREVENTIVE`, `AUXILIARY`, `RESTORATIVE`), and a restorative one needs `restorative_class` (`CERAMIC`, `COMPOSITE`, `POLYMER`, `METAL`). This is separate from `category`, but must not contradict it: category `METAL`, `CERAMIC`, `RESIN_COMPOSITE` or `POLYMER` allows only the matching `restorative_class` (`docs/DOMAIN.md`, Classification by purpose).
- **`parents` are record ids.** They mirror OHD's `is_a` links; a minted record's parent is the curator's choice of the closest record. Tests fail on a dangling parent.
- **Snippets are verbatim quotes.** Never paraphrase. Literature snippets are checked against PubMed abstracts, or, for a closed paper held locally, against the local copy and then committed as a signed excerpt in `reference_excerpts/` (`just sign-excerpts`). Local copies live in gitignored `local_full_text/` and are never committed.
- **Regulatory text is quoted from the regulation.** Cite a 21 CFR section as `CFR:872.NNNN`; its quotes are machine-checked against the eCFR text (`src/dentamech/refsources.py`). Cite an FDA database record as `url:`; those quotes are still checked by people, until linkml/linkml-reference-validator#179. Verified regulation numbers, classes and product codes are in `docs/regulatory.md`. Do not guess a product code or a regulation number from memory. Look it up:
  - CFR text: `just fetch-reference CFR:872.NNNN`, then read `references_cache/CFR_872.NNNN.md`
  - Product codes: `https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpcd/classification.cfm?start_search=1&regulationnumber=872.NNNN`
- **Device type vs product.** Classification of the material as a device type goes in `regulatory_status`. A specific brand's 510(k) goes in `products[].submissions`.
- `just seed` stubs each OHD material term that has no record. `/curate <file_stem>` runs the `curate-record` skill end to end.
- Read `docs/explanation/design-decisions.md` before changing scope, the ontology set, or the evidence policy.
