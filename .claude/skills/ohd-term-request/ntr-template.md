<!--
Body of a New Term Request for oral-health-and-disease-ontologies/ohd-ontology.
Title: NTR: <label>   (or: NTR: <parent label> and subtypes)
Fill every field, delete these comments and any section that does not apply,
and show the result to a person before filing. See SKILL.md beside this file.
-->

We would like to propose a new term for OHD. It came up while curating
[DentaMech](https://github.com/caufieldjh/dentamech), a knowledge base of
dental materials that is keyed to OHD terms where they exist.

## Proposed term

- **Label:** <label, following OHD's pattern>
- **Definition:** A <parent label> that <differentia>.
- **Definition source:** <PMID:… | doi:… | ISBN:… | ISO designation>
- **Parent:** <CURIE> ! <parent label>   <!-- or: none in OHD's materials yet; see "Where it fits" -->
- **Synonyms:**
  - <synonym> (exact | related | broad | narrow)
- **Contributor:** <https://orcid.org/…, if the person filing gave one>

<!-- Repeat "Proposed term" under a "Child terms" heading for any subtypes
proposed in the same issue. -->

## Where it fits

<One to three sentences: why the definition makes this a kind of the parent,
and how it differs from the siblings below.>

Siblings under <parent label>:

- <OHD:NNNNNNN> ! <label>
- <OHD:NNNNNNN> ! <label>

<!-- When the fit is uncertain, or the material is not restorative: -->
Alternative placement: <OHD:NNNNNNN> ! <label>, if <condition>. <The question
for the editors.>

## Source

<Full citation: authors, year, title, journal, DOI or PMID.>

> <One or two short verbatim sentences supporting the definition.>

<!-- Examples, optional: commercial products the source names. -->
Examples: <product names, as the source gives them>

## Searches

We found no existing term. Searched <YYYY-MM-DD>:

- the OHD release, for <queries>
- `src/ontology/components/dental_material.owl` and `src/ontology/ohd-edit.owl` on `main`, for <words>
- this repository's issues, for <words>

## In DentaMech

- Record: [<name>](https://github.com/caufieldjh/dentamech/blob/main/kb/materials/<stem>.yaml), under the provisional id `<dentamech:uuid>`
  <!-- Not merged yet? Link the pull request instead, and update this line once it merges. -->
- <Note any proposals here that have no DentaMech record.>

## Open questions

- <Anything the editors need to decide, such as grain, placement or naming.>
