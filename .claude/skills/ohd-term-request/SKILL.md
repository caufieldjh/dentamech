---
name: ohd-term-request
description: >-
  Propose a new term to the Oral Health and Disease Ontology (OHD) as a New
  Term Request (NTR) issue on oral-health-and-disease-ontologies/ohd-ontology:
  check that OHD is the right home and lacks the term, assemble label,
  definition, definition source, parent and synonyms from verified evidence,
  draft the issue for a person to approve, file it, and record the issue on
  the DentaMech record. Use when a record has a minted `dentamech:` id and a
  `CURATION_TODO` discussion proposing an OHD term, when curation meets a
  material OHD lacks (a missing parent, a subtype a source names), or when
  asked to request, propose or submit a term to OHD.
---

# New term requests to OHD

A record whose material OHD lacks gets a minted `dentamech:<uuid>` id and a
`CURATION_TODO` discussion proposing the term (`docs/DOMAIN.md`, Identity).
This skill turns that proposal into an issue on
<https://github.com/oral-health-and-disease-ontologies/ohd-ontology/issues>,
so OHD can add the term and the record can later be bound to it.

OHD has no issue template for term requests. Its own requests (#187, #190)
use the title `NTR: <label>` and propose a small hierarchy in one issue.
`ntr-template.md`, beside this file, is the format this project uses. It
gives OHD's editors every field they would otherwise have to ask for.

A concept need not have a record to be requested. A parent that a minted
child needs, or a subtype a source names, can be proposed alongside it. Say
in the issue which proposals have DentaMech records and which do not.

## 1. Is OHD the right home?

OHD's materials sit under `dental restoration material` (`OHD:0000000`), "A
processed material that bears a dental restoration material role". They are
edited in `src/ontology/components/dental_material.owl`, which also holds a
few constituent chemicals (oxides) and roles.

- **A restorative material, or a subtype of one OHD has.** OHD is the home.
- **A non-restorative material** (impression material, denture base,
  sealant, varnish, wax, gypsum). OHD has no branch for these yet. It is
  still the most likely home, but the request must say so and ask where the
  term belongs, offering a placement rather than assuming one. Read OHD #102
  (the definition of the dental restoration material role) and #103 (roles
  for multi-use materials) first, because they bear on this.
- **A chemical constituent.** Search ChEBI first (`just search-term CHEBI
  "..."`). OHD holds a few oxides of its own, but ask it for a chemical only
  when ChEBI lacks one.
- **A brand or product.** It is not a term. It goes in the record's
  `products`, and may appear in the request as an example.

Propose at the grain of the record (`docs/DOMAIN.md`, Identity). One
laboratory formulation from one study is usually too narrow for a term.
Propose the broader class it belongs to, name the formulation as an example,
and say why you chose that grain.

## 2. Make sure the term is not already there

1. Search the release, with the name and every synonym, as a partial match:

   ```bash
   just search-term OHD "l~<part of the name>"
   ```

   An empty result without `l~` is not evidence. See the `ontology-terms`
   skill.
2. The release can lag the source, so search OHD's main branch too: the
   materials component, and the edit file, which holds everything else
   (prostheses, procedures):

   ```bash
   base=https://raw.githubusercontent.com/oral-health-and-disease-ontologies/ohd-ontology/main/src/ontology
   for f in components/dental_material.owl ohd-edit.owl; do
     curl -sL "$base/$f" | grep -i 'rdfs:label' | grep -i "<word>"
   done
   ```

   A term found there but not in the release exists. Do not request it again.
   Note its CURIE in the discussion and wait for the release to bind it.
3. Search OHD's issues, open and closed, and this repository's:

   ```bash
   gh issue list -R oral-health-and-disease-ontologies/ohd-ontology --state all --search "<word>"
   grep -rn "ohd-ontology/issues" kb/materials/
   ```

   If a request exists, comment on it instead, after the approval in step 4,
   rather than opening a duplicate.

Write the queries and the date in the issue. "OHD lacks this" is a claim the
editors can check.

## 3. Assemble the request

Copy `ntr-template.md` to the scratchpad and fill every field. Each field maps
to the annotation OHD's editors will write:

| Field | OHD annotation | Rule |
|---|---|---|
| Label | `rdfs:label` | Under an existing OHD material, follow OHD's pattern: the qualifier, then the parent's label (`flowable resin-based composite dental restoration material` under `resin-based composite dental restoration material`). Outside that branch, use the name the field's standard or main source uses (`denture base polymer`), and ask in the issue whether OHD wants its own form. Lowercase, except symbols such as `3Y-TZP`. |
| Definition | `IAO:0000115` | Genus and differentia, in one sentence: "A <parent label> that ...". It is OHD's own wording, written from the source, not a pasted quote. |
| Definition source | `IAO:0000119` | **At least one, required.** An identifier, as OHD writes them: for example `PMID:32103673`, `doi:10.3390/jfb7030016`, `ISBN:0323478212`. For a standard, its designation (`ISO 20795-1:2013`). |
| Parent | `SubClassOf` | A CURIE and its exact label, checked with `just term-info OHD <CURIE>` and `just term-ancestors <CURIE>`. Name its other children that the new term sits beside. With no OHD branch to put it in, propose the nearest class OHD has (`processed material`, `OBI:0000047`, which `OHD:0000000` sits under) and say so. When the fit is uncertain, offer the alternatives and ask. |
| Synonyms | `oboInOwl:has*Synonym` | Each with its scope (exact, related, broad, narrow), from the source or the record's `synonyms`. |
| Child terms | | Any further terms proposed in the same issue, each with its own label, definition and source. |
| Contributor | `dcterms:contributor` | The ORCID of the person filing, if they give it. Ask them for it, and never guess it. Optional. |

### The source

The source is what gives the editors confidence in the term. It must be one
you have read:

- **Use evidence the record already holds and `just validate-references`
  passes.** For a concept with no record, fetch the source with
  `just fetch-reference` and read it first.
- **Quote one or two short sentences** that support the definition, verbatim,
  with the reference. A record's validated snippets are ready-made quotes.
- **Never cite a deep-research report.** Cite the primary source it points
  to.
- **The issue is a publication.** A quote from a closed paper or a standard
  stays within the fair-use caps in `reference_excerpts/README.md`. Never copy
  an ISO licensee stamp. Cite an ISO standard by its designation, and quote it
  only briefly.

### Where it fits

Placement is the part the editors most need help with. Give:

- the proposed parent, with a sentence on why the definition makes the new
  term a kind of it;
- the siblings it would sit beside, so the editors can see the differentia is
  distinct from theirs;
- for a non-restorative material, or any uncertain fit, a second placement
  and the question to decide between them.

The record's `parents` and its `CURATION_TODO` prompt usually say most of
this already.

## 4. Draft, show, file

Filing posts publicly on another group's repository. **Show the person the
title and the full body, and file only when they approve.**

File after the record has merged, so the issue's link to it works. If it has
not, link its pull request instead, and update the issue with the record's
link once it merges. In a GitHub
workflow, do not file. Put the draft in the pull request or comment instead.

- Title: `NTR: <label>`. For a parent with children: `NTR: <parent label> and subtypes`.
- Do not @-mention OHD's editors unless the person asks you to.
- Do not add labels. OHD has none for term requests, and you cannot create
  them there.

```bash
gh issue create -R oral-health-and-disease-ontologies/ohd-ontology \
  --title "NTR: <label>" --body-file <scratchpad>/ntr-<stem>.md
```

The command prints the issue's URL. Keep it for step 5.

## 5. Record the issue on the record

`Discussion` says external threads are cited in its `evidence`. In the
record's `CURATION_TODO` discussion for the term, set `status` and add the
issue by hand. There is no quote to check, so do not use `just add-evidence`:

```yaml
  - discussion_id: ohd-term-<stem>
    kind: CURATION_TODO
    status: UNDER_DISCUSSION
    prompt: '...'                       # unchanged
    evidence:
      - reference: url:https://github.com/oral-health-and-disease-ontologies/ohd-ontology/issues/<n>
        reference_title: 'NTR: <label>'
        supports: NO_EVIDENCE
        explanation: The new term request filed on OHD for this record's term.
```

`supports` is `NO_EVIDENCE`, because the issue is context, not evidence for a
claim. `OTHER` is refused there. Then:

1. Append a `curation_history` event (`action: EDIT`) naming the issue, and
   update `updated_date`.
2. `just validate kb/materials/<stem>.yaml`.
3. `just new-history --kind record --slug <stem> --event EDIT ... --apply`,
   with `--details` naming the issue.

A concept with no record has no discussion to update. Mention its issue in the
discussion of the record that needed it.

## 6. When OHD answers

- **The term is added.** Wait until `just search-term OHD` finds it in the
  release. Then the record is bound to it (`docs/DOMAIN.md`, Identity: "When
  the term exists, the record is re-grounded to it"). No recipe moves a record
  from a minted id to an OHD id yet. Ask the person how to proceed rather than
  improvising one. Set the discussion `RESOLVED`, with `resolved_date` and a
  `resolution_note` naming the term.
- **OHD places it differently or renames it.** Follow OHD. Bind its label
  exactly, and revisit `parents`.
- **OHD declines it.** Set the discussion `RESOLVED`, give the reason in
  `resolution_note`, and consider whether another ontology fits
  (`docs/DOMAIN.md`).
- **No answer.** Leave it `UNDER_DISCUSSION`.
