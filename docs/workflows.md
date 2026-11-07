# Automation

The repository runs a small curation loop on GitHub Actions, cut down from
DisMech's. Each workflow does one thing.

| Workflow | Trigger | What it does |
|---|---|---|
| `main.yaml` | push, PR | Lint, schema generation, whole-KB validation, tests, render check |
| `deploy-docs.yaml` | push to main | Renders pages and the browser, builds mkdocs, deploys to GitHub Pages |
| `generate-pages.yaml` | push to main touching `kb/` or the renderer | Re-renders `pages/` and `app/data.js` and commits them |
| `claude.yml` | `@claude` in an issue, comment, or review by a collaborator | General-purpose agent with repo access |
| `claude-code-review.yml` | PR touching `kb/`, schema, or cache | Reviews with the `dentamech-pr-review` skill and approves or requests changes |
| `claude-issue-triage.yml` | issue opened | Labels the issue and posts an assessment |
| `curation-scanner.yml` | every 6 hours, or by hand | Picks one `curation` issue or stalled PR and advances it; files a new issue when the queue is empty |

## Secrets

| Secret | Needed by | Notes |
|---|---|---|
| `CLAUDE_CODE_OAUTH_TOKEN` | all Claude workflows | From `claude setup-token`. Subscription-billed, subject to the weekly usage cap. |
| `ANTHROPIC_API_KEY` | all Claude workflows (optional) | When set it is preferred over the OAuth token; pay-per-use, no cap. |
| `EDISON_API_KEY` or `FUTUREHOUSE_API_KEY` | `falcon` research provider | Optional. Same key under either name. |
| `OPENAI_API_KEY` | `openai` research provider | Optional. |

Set one with:

```bash
gh secret set CLAUDE_CODE_OAUTH_TOKEN --repo caufieldjh/dentamech
```

The `claude_code` research provider needs no extra secret. It reuses the
Claude Code credential the workflow already has, which is why it is the
scanner's default.

## The curation loop

1. Someone opens a **Curate a material** issue (template provided), or the scanner files one for the next stub.
2. Triage labels it `curation`.
3. The scanner picks it up, runs `just research-material`, fills the entry following the `curate-material` skill, verifies regulatory facts against the CFR and FDA database, validates, and opens a draft PR.
4. The review workflow checks the PR and approves or requests changes.
5. The scanner tends stalled PRs on later runs, up to the comment limit below.
6. A human merges. The pages workflow re-renders; the deploy workflow publishes.

## Comment limit

The scanner stops working on a `curation` issue or PR after three consecutive agent comments. Before each run, `python -m dentamech.scanner` counts agent comments since the latest comment, review, or commit from a person, and the workflow passes the results to the scanner. Agent commits don't count toward the limit, and comments from all agent accounts do, including the review workflow's.

An item returns to selection once a person responds. While any item is paused, the scanner files no new issues, so unreviewed work doesn't pile up. Naming a material in the manual trigger still curates it directly.

## Running the pieces by hand

```bash
just research-material claude_code Glass_Ionomer_Cement
just research-material falcon Glass_Ionomer_Cement
just research-status
just validate-research-reference research/Glass_Ionomer_Cement-deep-research-falcon.md
just fetch-reference PMID:27367737
```

In Claude Code, `/curate Glass_Ionomer_Cement using falcon` runs the whole
skill.

## Model choice

Each workflow sets `AGENT_MODEL` at the top of its file. The scanner and the
review use `claude-opus-5`; triage uses `claude-sonnet-5`. The scanner's
manual trigger accepts a model override.

## Deliberately left out of DisMech's set

PR shepherd, literature and preprint scans, knowledge-gap scans, discussion
scanning, the GitHub App writer and reviewer identities, and the central
agent-config resolver. Add them back when the queue justifies them.
