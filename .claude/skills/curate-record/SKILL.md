---
name: curate-record
description: >-
  Create or improve one DentaMech dental material record end to end:
  scaffold, research, bind terms, quote evidence, validate, record history.
  Use when asked to add, curate, fill in, expand or fix a dental material
  record in kb/materials/. Not for read-only audits (use review-record)
  or for schema changes (use extend-schema).
---

# Curate one dental material record

A record is one dental material. Read `docs/DOMAIN.md` first if you have
not this session. It says what counts as a record and what does not.

## 1. Find or scaffold the record

```bash
ls kb/materials/ | grep -i <word>
just new-record [--id <CURIE>] --name "<name>"            # dry run
just new-record [--id <CURIE>] --name "<name>" --model <model-id> --apply
```

Find the id first, below. An id with the OHD prefix also
takes `--term-label "<its label>"`; `new-record` refuses it without one.

The id is the OHD CURIE when a term exists. Look it up;
never guess it:

```bash
just search-term sqlite:obo:ohd "<name>"
just term-info sqlite:obo:ohd <CURIE>
```

A record keyed by a term names it again in `record_term`, with the
ontology's label. `new-record` writes it from `--term-label`, and
`just validate` refuses an id with the OHD prefix without it. The term
check reaches `OHD:0000000` through `record_term`, so this is what
holds the id to the root:

```bash
just new-record --id <CURIE> --name "<name>" --term-label "<label from term-info>" --apply
```

If no term fits, leave out `--id`: the record gets a minted
`dentamech:<uuid>`. Open a `CURATION_TODO` discussion that says a term
is missing.

Check for duplicates by id and by synonym before creating anything.

## 2. Research

Gather sources before writing. For each source you intend to cite:

```bash
just fetch-reference PMID:<n>
```

Read what came back. If only the abstract is cached, you may quote only the
abstract. A claim you cannot tie to fetched text is not written. It becomes a
`KNOWLEDGE_GAP` discussion.

## 3. Write

Work section by section. For every descriptor:

- `preferred_term`: your words, as specific as the evidence allows.
- `term`: the ontology binding, found with the `ontology-terms` skill. Leave
  it out rather than guess.
- `evidence`: one or more items, added with `just add-evidence` (see the
  `evidence-references` skill). It fetches the source, checks the quote,
  fills the title and logs the change, so no one hand-writes evidence YAML.

Write the `description` last, from what the sections and sources say: two
or three sentences a newcomer can read. Every fact in it needs a quote.
Quote it at the description, where no section states the fact with
evidence already:

```bash
just add-evidence kb/materials/<stem>.yaml --at description --ref PMID:<n> --snippet "..."
```

A fact you cannot quote does not go in the description.

Set `status: PROPOSED` when the record is complete and valid. Never
`REVIEWED`.

## 4. Validate

```bash
just fill-titles kb/materials/<stem>.yaml --apply   # titles from the cache, for items written by hand
just validate kb/materials/<stem>.yaml
```

`fill-titles` lists any reference that is not cached yet. Fetch it with
`just fetch-reference` and run it again.

Fix every error. Do not change a correct term to silence a lookup outage.
Do not weaken a quote to make it pass. Find the real text.

## 5. Record

Append one event to the record's `curation_history`:

```yaml
  - timestamp: "<ISO-8601 UTC>"
    curator: <harness or login>
    llm_assisted: true
    model: <model-id>
    action: EDIT
    description: <what changed, one or two sentences>
```

Then one history record for the session:

```bash
just new-history --kind record --slug <stem> --event EDIT --outcome changed \
  --summary "..." --details "..." --actor <harness> --agent-tool <harness> \
  --model <model-id> --apply
```

## Dental rules

Materials are seeded from OHD, so the record almost always exists. If it doesn't,
the material isn't in OHD's `dental restoration material` branch. Don't invent a
term. Open an issue proposing the OHD term and stop.

Check that nobody else is on it, and continue on an open PR that covers it:

```bash
gh pr list --state all --search "\"<Material name>\"" --json number,title,state,url,headRefName --limit 50
```

Fill sections in this order: `composition`, `setting_mechanisms`,
`clinical_uses`, `regulatory_status`, `properties`, `clinical_performance`,
`adverse_effects`, `standards`, `products`, `synonyms`, `mappings`. Keep the
seeded `id`, `record_term`, `category` and `parents`.

**Verify regulatory facts (required for FDA records).** The research report's
regulatory section is a lead, not a source. The eCFR site blocks automated
fetches, so use these:

- Regulation text: `https://www.law.cornell.edu/cfr/text/21/872.NNNN`. Quote paragraph (a) into `identification`, and read paragraph (b) for class, special controls and 510(k) exemption.
- Product codes: `https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpcd/classification.cfm?start_search=1&regulationnumber=872.NNNN`.
- 510(k) records: `https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID=Kxxxxxx`.

Already verified regulations are in `docs/regulatory.md`. Reuse them, and add a
row when you verify a new one.

```yaml
regulatory_status:
- agency: FDA
  status: CLEARED            # CLEARED | EXEMPT | APPROVED | UNKNOWN ...
  regulation_number: '872.3690'
  regulation_title: Tooth shade resin material
  device_class: CLASS_II
  product_codes: [EBF, OFW]
  pathways: [PREMARKET_NOTIFICATION_510K]
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

Use one entry per applicable regulation. If no regulation names the material,
record `status: UNKNOWN` with `notes` explaining that, rather than guessing a
class. A specific brand's K-number goes under `products`, not `regulatory_status`.

`evidence_source` describes the cited source: `HUMAN_CLINICAL`, `IN_VITRO`,
`IN_SILICO`, `SYSTEMATIC_REVIEW`, `REGULATORY_DOCUMENT`, `STANDARD`,
`MANUFACTURER` or `TEXTBOOK`.

Useful term anchors: calcareous tooth `UBERON:0001091`, tooth crown
`UBERON:0003675`, tooth root `UBERON:0003677`, dental pulp `UBERON:0001754`,
dentine `UBERON:0001751`, enamel `UBERON:0001752`, jaw skeleton `UBERON:0001708`,
gingiva `UBERON:0001828`, carious teeth `HP:0000670`, oral lichenoid lesion
`HP:0031453`, allergic contact dermatitis `MONDO:0006525`.

Common mistakes: citing a PMID from memory, guessing a product code by analogy,
putting a brand's 510(k) under `regulatory_status`, and editing
`record_term.label`.

## 6. Hand off

Run `just qc`. Open a pull request with the record, the history record, and
any new files under `cache/` and `references_cache/`. List in the pull
request what you could not source.
