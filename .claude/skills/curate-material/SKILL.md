---
name: curate-material
description: >
  Curate one dental material entry in kb/materials/: run deep research, fill
  composition, properties, clinical uses, performance, adverse effects,
  regulatory status (FDA first), standards, and products, with verbatim
  evidence. Use when asked to curate, enrich, or research a material, or to
  work a `curation` issue.
---

# curate-material

Turn a stub (or a partly filled entry) into a curated entry. Research first,
then write, then validate. Nothing goes into the file that cannot be traced to
a source.

## Step 1. Locate the entry and run the duplicate preflight

Materials are seeded from OHD, so the file almost always exists already:

```bash
ls kb/materials/ | grep -i "<name fragment>"
uv run dentamech list | grep -i "<name fragment>"
```

If it does not exist, the material is not in OHD's `dental restoration material`
branch. Do not invent a term. Open an issue proposing the OHD term and stop.

Check that nobody else is already on it:

```bash
git fetch origin main
gh pr list --state all --search "\"<Material name>\"" --json number,title,state,url,headRefName --limit 50
gh issue list --state all --search "\"<Material name>\"" --json number,title,state,url,labels --limit 50
```

If an open PR covers the same material, continue there rather than starting over.

## Step 2. Work on a branch

Create a worktree or branch off `origin/main`. Confirm with `pwd` that you are
in it before writing anything. Root every file operation there.

```bash
git worktree add ../dentamech-<slug> -b curate/<slug> origin/main
cd ../dentamech-<slug>
```

## Step 3. Deep research (REQUIRED)

Always go through the just recipe. Do not improvise your own research prompt;
the template is what makes the regulatory section come back in a usable shape.

```bash
just research-material claude_code <File_Stem>     # default in CI; no extra key
just research-material falcon <File_Stem>          # EDISON_API_KEY / FUTUREHOUSE_API_KEY; slow, thorough
just research-material openai <File_Stem>          # OPENAI_API_KEY
```

The report lands at `research/<File_Stem>-deep-research-<provider>.md` with a
citations file beside it. **Read the whole report before writing.**

Then read its reference validation. The frontmatter carries
`reference_validation:` with `needs_review`, `unresolved_references`,
`off_topic_references`, and quote counts. Rules:

- Anything under `unresolved_references`: do not cite it.
- `quotes_valid < quotes_checked`: the report misattributed a quote. Find which before reusing quoted text.
- `off_topic_references`: read the paper before citing or dropping it.
- Older reports without the section: `just validate-research-reference research/<file>.md`.

The report's regulatory section is a lead, not a source. Verify every
regulation number, class, and product code yourself in Step 5.

## Step 4. Fetch references

For every PMID or DOI you intend to cite:

```bash
just fetch-reference PMID:nnnnnnnn PMID:nnnnnnnn DOI:10.xxxx/yyyy
```

This writes `references_cache/*.md`. Never create those files by hand. Read
the cached abstract and copy quotes from it, not from the research report.

If the report gives only a title, find the PMID:

```bash
curl -sG "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi" \
  --data-urlencode "db=pubmed" --data-urlencode "retmode=json" \
  --data-urlencode "term=<author>[Author] AND <topic words>[Title]"
```

Exact-title searches with colons or hyphens tend to return nothing; search by
author plus topic instead. Do not trust a PMID from memory; half of them are
wrong.

## Step 5. Verify regulatory facts (REQUIRED for FDA entries)

The eCFR site blocks automated fetches. Use these instead:

- Regulation text: `https://www.law.cornell.edu/cfr/text/21/872.NNNN`. Quote paragraph (a) into `identification` and read paragraph (b) for class, special controls, and 510(k) exemption.
- Product codes: `https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpcd/classification.cfm?start_search=1&regulationnumber=872.NNNN`. The `?id=` form of that URL is an internal record number, not a regulation number; do not use it.
- 510(k) records: `https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID=Kxxxxxx`.

Already-verified regulations are tabulated in `docs/regulatory.md`. Reuse them.
Add a row there when you verify a new one.

Map the regulation onto the entry:

```yaml
regulatory_status:
- agency: FDA
  status: CLEARED            # CLEARED | EXEMPT | APPROVED | UNKNOWN ...
  regulation_number: '872.3690'
  regulation_title: Tooth shade resin material
  device_class: CLASS_II
  product_codes: [EBF, OFW]
  pathways: [PREMARKET_NOTIFICATION_510K]
  special_controls: []
  identification: <paragraph (a), verbatim>
  approved_uses:
  - name: <use as the regulation states it>
    use_context: DIRECT_RESTORATION
  source_url: https://www.ecfr.gov/current/title-21/section-872.3690
  evidence:
  - reference: url:https://www.law.cornell.edu/cfr/text/21/872.3690
    reference_title: 21 CFR 872.3690 Tooth shade resin material
    supports: SUPPORT
    evidence_source: REGULATORY_DOCUMENT
    snippet: <verbatim from paragraph (b)>
    explanation: Classification paragraph.
```

One entry per applicable regulation. If products of this material reach market
only under a related device type and no regulation names the material, record
`status: UNKNOWN` with a `notes` explaining that, rather than guessing a class.

Product-level records (a specific brand's K-number) go under `products`, not
`regulatory_status`.

## Step 6. Write the entry

Fill sections in this order, each row with evidence where a claim could be
contested: `composition`, `setting_mechanisms`, `clinical_uses`,
`regulatory_status`, `properties`, `clinical_performance`, `adverse_effects`,
`standards`, `products`, `synonyms`, `mappings`.

Keep the seeded fields: `name`, `creation_date`, `material_term` (label must
match OHD exactly), `category`, `parents`. Set `curation_status` to
`IN_PROGRESS` or `CURATED`.

Evidence item shape:

```yaml
evidence:
- reference: PMID:24683067
  reference_title: <title>
  supports: SUPPORT
  evidence_source: SYSTEMATIC_REVIEW    # HUMAN_CLINICAL | IN_VITRO | IN_SILICO | SYSTEMATIC_REVIEW | REGULATORY_DOCUMENT | STANDARD | MANUFACTURER | TEXTBOOK
  snippet: "<exact quote from the cached abstract>"
  explanation: <why it bears on the claim>
```

`evidence_source` describes the cited source, not who is curating.

YAML trap: a snippet containing `: ` must be quoted, or the parser reads it as
a new key.

## Step 7. Bind ontology terms

```bash
uv run runoak -i sqlite:obo:ohd search "l~<procedure words>"     # OHD procedures under OHD:0000002
uv run runoak -i ols:chebi search "l~<chemical>"                  # composition
uv run runoak -i ols:uberon search "l~<site>"                     # anatomical_site
uv run runoak -i ols:hp search "l~<phenotype>"                    # adverse effect terms
uv run runoak -i ols:mondo search "l~<disease>"
```

Copy the label exactly. Leave `term` off when no fitting term exists; say so
in `description`.

Useful anchors: calcareous tooth `UBERON:0001091`, tooth crown `UBERON:0003675`,
tooth root `UBERON:0003677`, dental pulp `UBERON:0001754`, dentine
`UBERON:0001751`, enamel `UBERON:0001752`, jaw skeleton `UBERON:0001708`,
gingiva `UBERON:0001828`; carious teeth `HP:0000670`, oral lichenoid lesion
`HP:0031453`, allergic contact dermatitis `MONDO:0006525`.

## Step 8. Validate

```bash
just validate kb/materials/<File_Stem>.yaml            # schema + ontology terms
just validate-references kb/materials/<File_Stem>.yaml # snippets vs abstracts
uv run pytest -q
```

The reference validator prints `Total checks: 0` on success. It counts
failures only. A wrong quote is reported as an ERROR with the location.

## Step 9. Render and look

```bash
just render-one kb/materials/<File_Stem>.yaml
```

Open `pages/materials/<File_Stem>.html` and read it as a reader would.

## Step 10. Commit and open a PR

Stage only what belongs to this material:

```bash
git add kb/materials/<File_Stem>.yaml references_cache/ research/<File_Stem>-* docs/regulatory.md
git commit -m "Curate <Material name> (<OHD id>)"
git push -u origin curate/<slug>
gh pr create --draft --title "Curate <Material name>" --body "<what was filled, which provider, which regulations verified, validation results, what was left out and why>" 
```

Link the issue with `Closes #N` in the body when one exists. Then run the
`dentamech-pr-review` skill in a fresh subagent as a first review before
marking the PR ready.

## Common mistakes

- Citing a PMID recalled from memory. Search, fetch, read, then quote.
- Paraphrasing inside `snippet`. The validator will fail it.
- Guessing a product code or regulation number by analogy. Look it up.
- Putting a brand's 510(k) under `regulatory_status`. It goes under `products`.
- Editing `material_term.term.label`. It must equal the OHD label.
- Hand-writing `references_cache/*.md`.
- Staging `pages/` or `app/` in a curation PR. The pages workflow rebuilds them.
