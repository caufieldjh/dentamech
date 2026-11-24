---
provider: claude_code
model: claude-fable-5-2, claude-haiku-5-5, claude-opus-5-5
cached: false
start_time: '2026-11-24T12:13:07.014593'
end_time: '2026-11-24T12:30:38.308783'
duration_seconds: 1051.29
template_file: /home/harry/worktrees/dentmatmech/curate-amalgam/research/templates/record.md
template_variables:
  name: Amalgam
  id: OHD:0000001
  label: amalgam dental restoration material
  synonyms: dental amalgam, silver filling, silver amalgam
  record_noun: dental material
provider_config:
  timeout: 1800
  max_retries: 3
  parameters:
    allowed_domains: []
    claude_executable: claude
    skip_permissions: false
    allowed_tools:
    - WebSearch
    - WebFetch
    add_dirs: []
    timeout: 1800
    min_report_chars: 200
    extra_args: []
run_metadata:
  models_used:
  - claude-fable-5-2
  - claude-haiku-5-5
  - claude-opus-5-5
  web_search_requests: 12
  num_turns: 42
  total_cost_usd: 4.657385059999999
  session_id: fe07f281-033e-4730-bc4f-822d75de5104
  stop_reason: end_turn
  permission_denials: 7
  denied_tools:
  - Bash
  - Write
  assistant_text_blocks: 6
citation_count: 48
reference_validation:
  total_references: 87
  verified: 84
  not_found: 3
  unverifiable: 0
  confabulation_rate: 0.034
  quotes_checked: 38
  quotes_valid: 30
  quotes_unsupported: 8
  unsupported_quote_references:
  - PMC:PMC3010024
  - PMID:37176331
  - PMID:28220332
  - PMID:21217947
  - PMID:38316638
  - PMID:26314975
  quotes_not_checkable: 3
  relevance_assessed: 84
  on_topic: 39
  unresolved_references:
  - PMID:37380250
  - PMID:19370602
  - PMID:16417916
  needs_review: true
  validator_version: 0.8.0
term_validation:
  total_terms: 12
  verified: 12
  not_found: 0
  obsolete: 0
  unverifiable: 0
  confabulation_rate: 0.0
  labels_checked: 3
  labels_matching: 0
  labels_mismatched: 3
  mislabelled_terms:
  - term_id: CHEBI:30512
    reported_labels:
    - existing record
    ontology_label: silver atom
  - term_id: CHEBI:27007
    reported_labels:
    - existing record
    ontology_label: tin atom
  - term_id: CHEBI:28694
    reported_labels:
    - existing record
    ontology_label: copper atom
  needs_review: true
  adapter: 'ols:'
  validator_version: 0.4.5
---

## Question

# Dental Material Research Template

## Target Material
- **Material name:** Amalgam
- **OHD term:** OHD:0000001 (amalgam dental restoration material)
- **Other names:** dental amalgam, silver filling, silver amalgam

## Research Objectives

Provide a comprehensive, citation-dense research report on **Amalgam** as a
dental restoration material. The report will be used to populate an entry in a
structured knowledge base. Every factual claim must carry a citation. Prefer primary
literature and systematic reviews with PubMed IDs (PMID). For regulatory facts, cite
the regulation or database record itself by URL.

Treat the material at the level of the OHD term above. If the term is a class (for
example "glass ionomer cement"), report on the class and name the notable subtypes.
If the term is a specific subtype (for example "3Y-TZP zirconia ceramic"), stay at
that level and say how it differs from its siblings.

For each section, **suggested sources** are listed. Search those first.

---

### 1. Identity and Nomenclature
> **Search first:** OHD (Oral Health and Disease Ontology), ISO 1942 dental vocabulary, MeSH, NCI Thesaurus, SNOMED CT, ADA/CDT

- Concise definition of the material and what distinguishes it from neighboring materials.
- Synonyms, trade-class names, and clinical shorthand (e.g. "GIC", "PFM", "3Y-TZP").
- Identifiers in other vocabularies (MeSH heading, NCIT concept, SNOMED CT code) if they exist.
- Where the material sits in a materials taxonomy: parent class, sibling classes, recognized subtypes.

### 2. Composition
> **Search first:** PubMed, manufacturer technical profiles and safety data sheets, Phillips' Science of Dental Materials, Craig's Restorative Dental Materials, ChEBI

For each component:
- Name and chemical identity (suggest a ChEBI term where one exists).
- Functional role: matrix, filler, coupling agent, initiator, activator, inhibitor, powder or liquid phase, alloying element, crystalline phase, stabilizer, radiopacifier, pigment, fluoride source.
- Typical proportion (weight or volume percent, or a range), and how it varies across subtypes or generations.
- Named formulation variants (e.g. high-copper vs low-copper amalgam; 3Y vs 4Y vs 5Y zirconia; conventional vs resin-modified glass ionomer).

### 3. Setting and Handling
> **Search first:** PubMed, ISO test standards, manufacturer instructions for use

- Setting mechanism(s): light-cured, self-cured, dual-cured, acid-base reaction, amalgamation, hydration, sintering, heat pressing, casting, milling, additive manufacturing, cold working.
- Working time and setting time, and what affects them (temperature, powder-liquid ratio, light intensity).
- Processing route for indirect materials (CAD/CAM soft vs hard machining, pressing, layering).
- Handling sensitivities and technique factors that determine clinical success.

### 4. Physical, Mechanical, Chemical, and Biological Properties
> **Search first:** PubMed, ISO 4049 / ISO 9917 / ISO 6872 / ISO 22674 / ISO 24234 / ISO 6876 test literature, Dental Materials journal, Journal of Dental Research

Report values with units, the test method or standard, and test conditions, for as many of these as the literature supports:
- Flexural strength, compressive strength, tensile or diametral tensile strength
- Elastic modulus, fracture toughness, hardness (Vickers or Knoop)
- Wear resistance and antagonist wear
- Bond strength to enamel, dentin, and other substrates
- Polymerization shrinkage and shrinkage stress; degree of conversion; depth of cure
- Water sorption and solubility
- Thermal expansion and thermal conductivity
- Radiopacity
- Translucency and color stability
- Fluoride release and recharge
- Film thickness (luting agents)
- Corrosion and tarnish resistance
- Biocompatibility: cytotoxicity, sensitization, pulpal response, leachables and degradation products
- Antibacterial activity

Give ranges rather than single values where the literature varies, and say which subtype or product the value belongs to.

### 5. Clinical Uses and Indications
> **Search first:** PubMed, Cochrane Oral Health reviews, ADA clinical practice guidelines, textbooks of operative dentistry and prosthodontics, OHD dental procedure terms

For each use:
- The clinical context: direct restoration, indirect restoration (inlay, onlay, crown, bridge, veneer), luting, liner or base, pulp therapy, endodontic, implant, prosthodontic, orthodontic, preventive, adhesive, impression, temporary, surgical.
- The corresponding dental procedure (suggest an OHD procedure term, e.g. "resin filling restoration procedure", "ceramic crown restoration procedure", "pulp capping procedure").
- Anatomical site (suggest a UBERON term: calcareous tooth, tooth crown, tooth root, dental pulp, dentine, enamel, jaw skeleton, gingiva).
- Indications and contraindications as stated in guidelines or reviews.
- Primary vs permanent dentition considerations.

### 6. Clinical Performance and Longevity
> **Search first:** PubMed (systematic reviews, meta-analyses, practice-based research networks), Cochrane Oral Health

- Survival rate and success rate at stated follow-up intervals.
- Annual failure rate.
- Median survival or time to replacement.
- Retention rate where relevant (sealants, veneers, cervical restorations).
- Main reasons for failure (secondary caries, fracture, wear, debonding, chipping, discoloration).
- Comparators: how the material performs against its main alternatives (e.g. composite vs amalgam; zirconia vs lithium disilicate; conventional vs resin-modified glass ionomer).
- Patient- and tooth-level factors that change outcomes (caries risk, cavity size, position, bruxism).

### 7. Adverse Effects and Safety
> **Search first:** PubMed, FDA safety communications, FDA MAUDE, SCENIHR/SCHEER opinions (EU), Minamata Convention documents where relevant

For each effect, give the category and, where possible, a phenotype or disease term (HP or MONDO):
- Allergic and hypersensitivity reactions (contact allergy, oral lichenoid lesions, nickel/cobalt/palladium allergy, methacrylate allergy)
- Toxicity: local (pulpal, mucosal) and systemic; leachables such as mercury, BPA-related monomers, metal ions
- Mechanical failure modes
- Secondary caries
- Pulpal response and postoperative sensitivity
- Periodontal or gingival response
- Wear of opposing teeth
- Esthetic problems: discoloration, staining
- Occupational hazards for dental staff
- Environmental release and disposal concerns
- Frequency, where reported

### 8. Regulatory Status (REQUIRED, FDA FIRST)
> **Search first:** eCFR 21 CFR Part 872 Subpart D (Prosthetic Devices) at https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-872 or the Cornell LII mirror at https://www.law.cornell.edu/cfr/text/21/part-872/subpart-D; FDA Product Classification Database at https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfPCD/classification.cfm; FDA 510(k) database at https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm; FDA PMA database; FDA De Novo database; FDA guidance documents; FDA dental device pages

This section is the reason the knowledge base exists. Be exact.

**8a. Device-type classification (the material as a device type)**
- Which section(s) of 21 CFR 872 apply. Write the section as `872.NNNN` and give the device name exactly as the regulation states it (e.g. `872.3690` "Tooth shade resin material"; `872.3275` "Dental cement"; `872.3070` "Dental amalgam, mercury, and amalgam alloy"; `872.3060` "Noble metal alloy"; `872.3710` "Base metal alloy"; `872.3640` "Endosseous dental implant"; `872.3250` "Calcium hydroxide cavity liner"; `872.3200` "Resin tooth bonding agent"; `872.3765` "Pit and fissure sealant and conditioner"; `872.3820` "Root canal filling resin"; `872.3920` "Porcelain tooth").
- Quote the regulation's **(a) Identification** paragraph verbatim.
- Quote the **(b) Classification** paragraph verbatim: device class (I, II, III), whether special controls apply and which guidance document is named, and whether the device is exempt from premarket notification under 872.9.
- The FDA **product code(s)** (three capital letters) listed under that regulation, with the device name attached to each code.
- The uses the regulation permits, as stated in the identification paragraph (these become the "approved uses").
- Any restrictions: prescription-only status, population-specific FDA recommendations (e.g. the 2020 amalgam recommendations for high-risk groups), labeling requirements.
- If the material can fall under more than one regulation depending on use (e.g. a resin used as a restorative, a core build-up, a luting cement, or a sealant), list each regulation and say which use it governs.
- If no regulation names the material and products reach market under a related device type, say so explicitly and name the regulation and product code those products actually use.

**8b. Notable product-level decisions**
- Representative 510(k) clearances: K-number, product name, applicant, decision date, product code, regulation number, and the indications-for-use statement quoted from the 510(k) summary or decision letter.
- Any PMA approvals (P-number) or De Novo grants (DEN-number) for this material class.
- Any recalls, safety communications, or market withdrawals.
- Give the FDA database URL for each record cited.

**8c. Other jurisdictions (brief)**
- EU MDR class (I, IIa, IIb, III) and whether a notified body is involved; relevant harmonized standards.
- Health Canada, MHRA, TGA, PMDA, NMPA, ANVISA status if readily available. Do not guess; say "not found" when it is not found.

**Accuracy rules for this section.** Do not infer a regulation number, product code, or class from memory or from analogy with a similar material. Every value must be read from the eCFR text, the Cornell mirror, or an FDA database record, and the URL of that source must be given next to it. If a lookup fails, say the lookup failed rather than filling the gap.

### 9. Standards and Specifications
> **Search first:** ISO Online Browsing Platform (https://www.iso.org/obp), ADA Standards Committee on Dental Products (ANSI/ADA), ASTM

- ISO standards the material is tested or specified against (number, year, and title), e.g. ISO 4049 polymer-based restorative materials, ISO 9917-1 water-based cements, ISO 24234 dental amalgam, ISO 6872 ceramic materials, ISO 22674 metallic materials for fixed and removable restorations, ISO 5832 implant metals, ISO 6876 root canal sealing materials, ISO 3107 zinc oxide cements, ISO 7405 biocompatibility of dental materials, ISO 10993 biological evaluation of medical devices.
- Corresponding ANSI/ADA specifications.
- The FDA-recognized consensus standards relevant to the device type, if the FDA recognized standards database lists them.

### 10. Commercial Products
> **Search first:** FDA 510(k) database, manufacturer websites, ADA Seal of Acceptance, product reviews in Dental Materials and JADA

- Representative branded products (name, manufacturer) that are instances of this material class, spanning the main subtypes.
- For each, the FDA submission number if found (cross-reference section 8b).
- Products commonly used as comparators in the clinical literature.

### 11. History and Trends (brief)
> **Search first:** PubMed reviews, textbooks

- When and how the material entered dental use.
- Major generational changes in formulation.
- Current direction: phase-downs, replacements, new subtypes.

---

## Citation Requirements

- Cite a PMID for every clinical, laboratory, and mechanistic claim. Use DOI only when no PMID exists.
- Include **direct quotes from abstracts** to support key statements. Quotes must be exact. Do not paraphrase inside quotation marks.
- Distinguish evidence source types: human clinical, in vitro / laboratory, computational, systematic review, regulatory document, technical standard, manufacturer document, textbook.
- For regulatory claims, cite the regulation section or database record by URL and quote it verbatim.
- For standards, cite the ISO or ADA catalog entry by URL. (Curators quote an ISO standard's own text separately, from a local copy.)
- Never fabricate an identifier. If you cannot find a PMID, say so and give the title and authors instead.

## Output Format

Structure the report as a narrative organized by the numbered sections above. For each section provide:
- Factual content with specific values, units, ranges, and named subtypes or products.
- Ontology term suggestions where applicable: OHD (materials and procedures), ChEBI (components), UBERON (sites), HP or MONDO (adverse effects), PATO (qualities).
- Citations with PMIDs, and direct abstract quotes for key claims.
- For regulatory content: regulation number, device name, class, product codes, and verbatim identification text, each with its source URL.
- A clear statement when information is not available or not applicable for this material.

This report will be used to populate a knowledge base entry with:
- Composition rows (component, role, ChEBI term, proportion, evidence)
- Property rows (property type, value, unit, test method, conditions, evidence)
- Clinical use entries (context, OHD procedure, UBERON site, indications, contraindications, evidence)
- Clinical performance rows (measure, value, follow-up, population, comparator, evidence)
- Adverse effect entries (category, HP/MONDO term, frequency, evidence)
- Regulatory status entries (agency, regulation, class, product codes, pathway, special controls, verbatim identification, approved uses, restrictions, source URL, evidence)
- Product entries with regulatory submissions (K/P/DEN number, pathway, decision, date, product code, indications for use, source URL)
- Standards
- Evidence items with PMIDs and exact abstract quotes throughout


## Output

Screwdriver out, Harry. Case comes off amalgam now; the repo, eCFR and PubMed go on the bench first.

Two shell commands got refused for how they were written, so I'm using small scripts instead. The report stays inline, no separate doc.

Scripts and direct network calls need approval that I don't have, so I won't push it. Web search works, and so does the page reader, which I'm using to fetch the PubMed abstracts and FDA records.

Every screw goes back. The first pass left a few holes, so I'm running a targeted second one.

Some 510(k) PDFs came down as raw files. I'm opening them myself.

# Amalgam (OHD:0000001) as a dental restoration material: research report

Prepared 2026-11-24.

**How far to trust each item**
- **Read directly:** 21 CFR 872.3070 (repository eCFR cache, issue 2026-11-12); FDA PDFs K223182, K140125, K093587, K033434 and K974035; the cached abstracts of PMID 21217947, 24683067 and 8940574; the FIDE classification list (pages 1–6).
- **Read through a page reader:** other PubMed abstracts, openFDA and web pages. These quotes are fragments of 125 characters or fewer. Re-check each with `just fetch-reference` and `just add-evidence`.
- **[S] = search summary only.** The primary page was not opened or refused access. Treat these as leads.

**Main findings**
- **Regulation:** US amalgam is Class II with special controls and is not 510(k)-exempt (872.3070; codes EJJ, ELY, OIV).
- **Longevity:** older randomized evidence favors amalgam over composite, at low certainty. A 2025 meta-analysis found no significant difference.
- **Policy:** the EU ended routine use on 1 January 2025, and Minamata parties agreed a 2034 phase-out [S].
- **Property gaps:** no sourced value was found for elastic modulus, fracture toughness, thermal expansion or conductivity, or calibrated radiopacity.

---

## 1. Identity and nomenclature

**Definition.** OHD (fragment, truncated in retrieval): "A metal dental restoration material that consists of alloy that is formed by reacting mercury with silver, copper, tin and sometimes palladium, zinc and other elements..." ([OLS/OHD](https://www.ebi.ac.uk/ols4/api/search?q=amalgam&ontology=ohd&rows=40)). Amalgam differs from cast dental alloys because it sets by reaction with liquid mercury. It differs from composites and glass ionomers because it is metallic.

**Synonyms.** Dental amalgam; silver amalgam; silver filling. "Non-gamma-2" is the trade-class term for high-copper types.

| Vocabulary | Identifier | Source |
|---|---|---|
| OHD material | OHD:0000001, amalgam dental restoration material | [OLS](https://www.ebi.ac.uk/ols4/api/search?q=amalgam&ontology=ohd&rows=40) |
| OHD procedure | OHD:0000041, amalgam filling restoration procedure | same |
| CDT classes in OHD | CDT_0002140, 0002150, 0002160, 0002161 | same |
| MeSH | D003723, Dental Amalgam | [MeSH](https://id.nlm.nih.gov/mesh/D003723.json) |
| SNOMED CT | 256447001 Amalgam (silver) dental filling material; 256448006 low copper; 256449003 high copper; 468321001 Dental amalgam mercury | [OLS](https://www.ebi.ac.uk/ols4/api/search?q=amalgam&ontology=snomed&rows=15) |
| NCIt | Not found in the first 10 of 128 hits; not ruled out | [EVS](https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/search?term=dental%20amalgam&pageSize=10) |

MeSH scope note: "An alloy used in restorative dentistry that contains mercury, silver, tin, copper, and possibly zinc."

**Taxonomy.** The existing record's parent is OHD:0000048. Useful subtype axes:
- **Copper:** low or high.
- **Particle shape:** lathe-cut, spherical, or admixed.
- **Alloy design:** single-composition or dispersed-phase.
- **Zinc:** present or absent.

Gallium alloys are mercury-free substitutes, not amalgams. Dentists rated amalgam above a gallium alloy on each handling characteristic (PMID:8258585, simulated clinical).

---

## 2. Composition

### Components

| Component | Role | Proportion | ChEBI |
|---|---|---|---|
| Mercury | Liquid phase | 45–54.5% of the mix in cleared products listed below | CHEBI:25195 mercury atom; alternatives CHEBI:16170 mercury(0), CHEBI:35113 elemental mercury |
| Silver | Alloying element | 40–70% of alloy | CHEBI:30512 (existing record) |
| Tin | Alloying element | 12–30% of alloy | CHEBI:27007 (existing record) |
| Copper | Alloying element; suppresses gamma-2 | 12–24% of alloy in "currently used" alloys | CHEBI:28694 (existing record) |
| Zinc | Alloying element | Up to 1% | CHEBI:27363 zinc atom |
| Indium | Optional alloying element | 0–4% | Element term not found; leave unset |
| Palladium | Optional alloying element | 0.5% | Element term not found; leave unset |

The alloy ranges come from PMID:21217947 full text (review): "Composition of currently used alloy is silver 40–70%, tin 12–30% and copper 12–24%. It may also include indium 0–4%, palladium 0.5% and zinc up to 1%." ([PMC3010024](https://pmc.ncbi.nlm.nih.gov/articles/PMC3010024/)).

FDA states: "Approximately half (50%) of dental amalgam is elemental mercury by weight." ([FDA](https://www.fda.gov/medical-devices/dental-devices/dental-amalgam-fillings), current as of 2021-02-18). The closest ChEBI term for liquid elemental mercury is a curator choice. The record's "mercury atom" matches the pattern used for its other metals.

### Low versus high copper (wt%)

| Type | Ag | Sn | Cu | Other | Source |
|---|---|---|---|---|---|
| Low copper | 55–60 | 20–29 | 6–8 | Zn <2 | PMID:37176331 (introduction; in vitro paper) |
| High copper | 40–60 | 12–30 | 8.5–33 | In 0.5–9, Zn 1–3.5, trace Pd 0.7 | same |
| Low copper | 63–70 | 26–28 | 2–5 | Zn 0–2 | Patent [S]; not for citation |

The sources disagree on low-copper ranges, so check a textbook before recording one.

### Product compositions from FDA summaries

| Product | Ag | Sn | Cu | Zn / In | Hg in mix | Particles |
|---|---|---|---|---|---|---|
| Sybraloy | 39.4–43.7 | 28.8–32.5 | 25.8–29.8 | Zn 0 | 45–51 | Spherical |
| Contour | 41 | 31 | 28 | Zn 0 | 47 | Spherical + lathe-cut |
| Dispersalloy | 70 | 16 | 13 | Zn 1 | 50 | Spherical + lathe-cut |
| NU Alloy DP 40 | 40 | 31.8 | 28.21 | Zn 0 | 47.5 | Spherical + lathe-cut |
| NU Alloy DP | 44.85 | 31.95 | 23.24 | Zn 0 | 49.6 | Spherical + lathe-cut |
| NU Alloy DP Active | 44.74 | 31.54 | 23.96 | Zn 0 | 49.6 | Spherical + lathe-cut |
| Micronic (low copper) | 70.14 | 26.89 | 3.86 | Zn 0 | 52.4–54.5 | Lathe-cut |
| World Work type a | 44.5 | 30 | 25.5 | – | 50 | Admixed |
| World Work type b | 70 | 18 | 12 | – | 50 | Admixed |
| Permite | 56 | 27.9 | 15.4 | Zn 0.2 / In 0.5 | 46.2–49.5 | Admixed |

Sources: [K140125](https://www.accessdata.fda.gov/cdrh_docs/pdf14/K140125.pdf) (first seven) and [K223182](https://www.accessdata.fda.gov/cdrh_docs/pdf22/K223182.pdf) (last three). "Low copper" for Micronic is my label, based on its 3.86% Cu. As printed, NU Alloy DP, DP Active and Micronic sum to slightly over 100%.

### Phases
- **Low copper:** gamma-1 (Ag2Hg3) and gamma-2 (Sn8Hg) form. "the Sn8Hg (γ2 phase) occupies about 15% vol. of the mixed alloy" (PMID:37176331).
- **High copper:** Cu6Sn5 (eta′) forms instead. Microprobe work on three such amalgams found "no detectable Sn8Hg (gamma 2)" (PMID:6588080, in vitro).
- **Copper threshold:** "at around 12%, it has almost disappeared" (gamma-2; PMID:28220332).
- **Ageing:** gamma-1 "is transformed to the β1-phase with considerably less mercury" (PMID:28220332).

---

## 3. Setting and handling

**Mechanism.** Amalgamation.

**Times.**

| Parameter | Value | Source |
|---|---|---|
| Condensing time | 2.5–5 min | K223182 (World Work and Permite) |
| Carving time | 4.5–7 min (World Work); 5.5–7 min (Permite) | K223182 |
| Maximum working time | 12 min (Sybraloy, Contour); 8 min (NU Alloy DP family); 7 min (Micronic) | K140125, regular-set capsules |
| Trituration | 4–8 s (World Work); 6–8 s (Permite) | K223182 |
| Trituration | 7–10 s (Sybraloy); 8–10 s (Contour); 10–14 s (Dispersalloy); 7–14 s (Micronic) | K140125 |

Trituration time depends on spill size and amalgamator (K223182). No harmonized setting time was found.

**Technique factors**
- **Mercury ratio:** "In 1959, Dr. Wilmer Eames recommended a 1:1 ratio of mercury to alloy" (PMID:21217947).
- **Condensation force:** "Specimens condensed at 3 MPa showed substantially lower strength." Trituration mattered less: "Variations in trituration time between 5 and 12 seconds had little effect." (PMID:7880469, high-copper, in vitro).
- **Particle shape:** powders that are lathe-cut or admixed "tend to resist condensation better than amalgams made entirely from spherical powders" (K223182).
- **Moisture:** contamination "affected the compressive strength and creep but not the hardness" (PMID:6937502, high-copper, in vitro). Zinc: "Some researchers believe that if zinc containing amalgam is contaminated with moisture, it causes delayed expansion." (PMID:21217947).
- **Repair:** joined specimens reached "between 11.5% and 51.4%" of intact flexural strength (PMID:6758471, in vitro).
- **Adhesive liners:** Panavia EX "significantly reduced the strength of the Tytin specimens prepared by hand-condensing (P less than 0.05)" (PMID:1930843, in vitro).

Indirect processing (CAD/CAM, pressing, layering) does not apply.

---

## 4. Properties

### Strength, creep and dimensional change (manufacturer bench data in FDA summaries)

| Product | Compressive 1 h (MPa) | Compressive 24 h (MPa) | Creep (%) | Dimensional change (%) |
|---|---|---|---|---|
| Sybraloy | 185 | 534 | 0.08 | 0.06 |
| Contour | 124.11 | 441.26 | 0.10 max | −0.1 |
| Dispersalloy | 127.5 | 427.5 | 0.86 | 0.03 |
| NU Alloy DP 40 | 87 | 364 | 0.23 | −0.05 |
| NU Alloy DP | 182 | 526 | 0.30 | −0.05 |
| NU Alloy DP Active | 159 | 500 | 0.18 | −0.06 |
| Micronic | 183 | 398 | 0.20 | −0.03 |
| World Work | 171 | 443 | 0.5 | 0.1 |
| Permite | 260 | 500 | 0.2 | −0.04 |

Limits as each submission printed them; these are not quotations of ISO text:

| Submission | 1 h | 24 h | Creep | Dimensional change |
|---|---|---|---|---|
| K140125 (citing ISO 24234:2004) | 80 MPa min | 300 MPa min | 2.0% max | −0.10 to +0.20% |
| K223182 (citing ISO 24234, edition not stated) | >100 MPa | >350 MPa | Max. 2% | −0.10 to +0.15 |

K223182 also lists composition limits: Ag ≥ 40, Sn ≤ 32, Cu ≤ 30, Zn ≤ 2.

### Other properties

| Property | Finding | Source |
|---|---|---|
| Diametral tensile strength | Silver amalgam: "The mean DTS value was high in Group III (73.7 MPa)" | PMID:39450364 (2024, in vitro) |
| Compressive strength, same study | "256.2"; unit not attached to this value in the retrieved abstract | PMID:39450364 |
| Experimental ball-milled alloy | 1 h compressive 228 MPa; creep "measured to be 0.12%"; 24 h DTS "177 MPa" | PMID:21176947 (2011, in vitro). Not representative of marketed products; its DTS is far above the 73.7 MPa value, so check the full text |
| Hardness (HV200, 6 weeks) | 64 at 11.8% Cu; 80 at 15.4%; 93 at 20%; 100 at 25%; 100.8 at 26%; 101.7 at 28%; 112 at 31%; 129 at 33% | PMID:37176331 (2023, in vitro) |
| Dimensional change, copper-rich | "from 36 to 101 micrometers/cm at 37 C." | PMID:288781 (in vitro; alloy subset not confirmed) |
| Abrasion wear | "The lowest abrasion wear was recorded for the amalgam and for the microfill and smaller-particle composites." | PMID:9002838 (in vitro, 50,000 cycles) |
| Antagonist wear | Amalgam wore faster than enamel fossae but was "less destructive against their opposing enamel cusps" | PMID:2263933 |
| Dentin bond, Tytin | "24-hour shear bond strength (7.11 +/- 1.93 MPa)" | PMID:8710705; adhesive system not captured |
| Dentin bond, Dispersalloy + Amalgambond Plus | "10.41 +/- 1.47 MPa" | PMID:7986444 |
| Dentin bond, four agents | "8.13 +/- 1.48 for AB2, 7.06 +/- 1.41 for SBMP, 4.2 +/- 1.06 for HQB, 3.04 +/- 0.68 for CL" | PMID:11345686 |
| Enamel bond | "1.2 and 1.6 MPa"; other groups "ranged from 14.2 to 15.7 MPa" | PMID:11552167 |
| Radiopacity | "Amalgam had the highest radiopacity."; enamel equivalent to 2 mm Al | PMID:37079911 (2023, in vitro) |
| Radiopacity, estimate | "extrapolated estimates were 11.90 and 10.92 mm Al, respectively" | PMID:42806803 (2026); beyond calibration range, do not record as measured |
| Corrosion, palladium | "no more than 0.5 wt% Palladium in a high copper amalgam powder" improves corrosion to 10 years | PMID:12628436 (in vitro) |
| Corrosion products | 2 µg/cm² (World Work), 2.5 µg/cm² (Permite); vapor <65 ng/cm² in 4 h for both | K223182 |
| Galvanic couple with titanium | "of the order of 10(-8) A/cm2 for the Ti/amalgam couple" | PMID:10863427 (in vitro) |
| Microleakage | "Spherical particle alloys as a group exhibited the highest microleakage values." | PMID:8854611 (in vitro) |

**Biocompatibility**
- **Cytotoxicity:** "Pure copper and zinc showed intensive cytotoxicity" (PMID:2016001). Zinc-containing amalgams were more cytotoxic (PMID:3166005).
- **Antibacterial activity, conflicting by specimen.** Constituents were active, in the order "Hg > Cu > F > Zn" (PMID:10023205). Set amalgam "produced no measureable zones of inhibition whether aged or fresh" (PMID:7843065).
- **Pulp, bonded amalgam:** "Nine out of 12 teeth showed no inflammatory pulp responses at 35 days" (PMID:10785298).

**Conflict on copper and mercury vapor**
- PMID:37176331, freshly condensed: "the higher the copper content present in the alloy, the less mercury vapor is released from the amalgam." Its Table 1 unit (kg/m3) is implausible, so do not use those absolute values.
- PMID:28220332: "the high copper amalgams emits 3–43 times as much mercury vapor depending on brand."
- PMID:7929981: emission tracked tin in gamma-1 ("R2 = 0.94 (p < 0.001)").
- The studies differ in materials and conditions. Do not record a simple copper effect.

**MRI.** Ex vivo mercury in artificial saliva was "673 μg/L ± 179 in the 7.0-T MRI group, 172 μg/L ± 60 in the 1.5-T MRI group, and 141 μg/L ± 152 in the control group." (PMID:29944087; an erratum exists, PMID:30998445).

**Not found with a usable value:** intact flexural strength, elastic modulus, fracture toughness, thermal expansion, thermal conductivity or diffusivity, wear rate, calibrated radiopacity.

**Not applicable:** polymerization shrinkage, degree of conversion, depth of cure, translucency. Fluoride release, film thickness and water sorption were not found for conventional amalgam.

---

## 5. Clinical uses and indications

| Use | Procedure / site | Evidence |
|---|---|---|
| Direct posterior restoration (Class I, II) | OHD:0000041; calcareous tooth UBERON:0001091 (existing record) | K140125: "cavities class I and II in molars and premolars"; K033434 likewise |
| Economic posterior restoration | same | "For the present, amalgam should remain the material of choice for economic direct restoration of posterior teeth." (PMID:21217947, 2010; predates current policy) |
| Core build-up | OHD procedure not looked up | Septalloy/Securalloy: "filling cavities in posterior teeth (class I and class II restorations) and core build-up" ([K051010 mirror](https://fda.innolitics.com/device/K051010), OCR) |
| Root-end filling (historical) | Tooth root; UBERON ID not looked up | "The two RCTs indicated that glass ionomer cement appeared to be equivalent to amalgam." (PMID:12950570, systematic review) |
| Adhesively bonded amalgam | as direct restoration | One trial: "50 out of 53 restorations in the non-bonded group survived, and 55 of 60 bonded restorations survived" at two years (PMID:26954446, Cochrane) |

**Guideline.** The 2023 ADA panel "formulated 16 recommendations and good practice statements" (PMID:37380250). Its supporting review found "limited evidence to support important differences between direct restorative materials used in practice." (PMID:36610925). Material-level recommendations were not extracted.

**Contraindications and cautions**
- **FDA labeling:** "do not use in persons with a known mercury allergy" (special controls guidance, section 8a).
- **FDA high-risk groups:** section 8a.
- **Labeling precaution:** "do not place the device in direct contact with other types of metals".
- **Esthetics:** "When esthetic concerns are paramount, tooth-colored materials, placed meticulously, can provide an acceptable alternative." (PMID:21217947).

**Primary dentition.** Cochrane 2009 included three studies: "There were no significant differences found in all three trials for all of the outcomes assessed." (PMID:19370602; its update, PMID:27748505, is marked withdrawn). EU and Minamata provisions restrict use in children (sections 8c, 11).

---

## 6. Clinical performance and longevity

| Study (type) | Result |
|---|---|
| PMID:24683067, Cochrane 2014 | "resin restorations had a significantly higher risk of failure than amalgam restorations (risk ratio (RR) 1.89, 95% confidence interval (CI) 1.52 to 2.35, P value < 0.001 (fixed-effect model) (low-quality evidence))"; secondary caries RR 2.14 (1.67–2.74); fracture RR 0.87 (0.46–1.64). All seven trials at high risk of bias; ≥3 years |
| PMID:34387873, Cochrane 2021 update | "composite resin restorations had almost double the risk of failure compared to amalgam restorations"; secondary caries "RR 2.14, 95% CI 1.67 to 2.74; P < 0.001" |
| PMID:40578032, meta-analysis 2025 | "did not find any statistically significant difference in failure risk between amalgam and composite resin restorations" |
| PMID:26116767, meta-analysis 2015 | Composite posterior restorations "still have less longevity and a higher number of secondary caries" |
| PMID:17545266, RCT in children | Survival "94.4 percent" amalgam vs "85.5 percent" composite; annual failure "0.16 to 2.83 percent" vs "0.94 to 9.43 percent"; secondary caries "3.5 times greater in the composite group" |
| PMID:17545265, RCT (NECAT), permanent teeth | Replacement: "14.9 percent of composites versus 10.8 percent of amalgams (P=.45)"; composites needed "seven times as many repairs" |
| PMID:16417916, retrospective | Amalgam "89.6% at 5 years and 79.2% at 10 years"; composite "91.7% at 5 years and 82.2% at 10 years" |
| PMID:20660797, 12-year retrospective | "After 12 years, 293 amalgam and 114 composite restorations had failed." Counts only; denominators not retrieved, so do not compare |
| PMID:15470871, review | Mean annual failure "3.0% (1.9) for amalgam restorations, 2.2% (2.0) for direct composites" |
| PMID:26790901, Dutch practice network | "mean AFR 4.6% over 10 years." All direct restorations, not amalgam alone |
| PMID:32585263, 2020 | "Amalgam and resin composite restorations had similar survival rates" |
| PMID:40873828, systematic review 2025 | "median survival times exceeding 16 years, compared to 11 years for composite restorations." |
| PMID:42032607, 2026, short term | Clinical success "88.8% vs. 87.6%; χ²=5.174, p = 0.075" (composite vs amalgam) |
| PMID:40482587, 2025, health records | Failure higher "for amalgam (8.84 %) compared to composite (4.36 %)" |
| PMID:40458903, 2025, complex restorations | "Only two studies compared AM and RC restorations." |

**Alloy effect.** In a secondary analysis of 14 trials and 3,119 restorations, 13-year survival was 25% for conventional zinc-free alloys, "70% after 13 years when either was present" (zinc or high copper), and "85% after 13 years" for zinc-containing high-copper alloys (PMID:9372797).

**Creep.** Across "2068 amalgam restorations", creep correlated with marginal fracture in low-copper but not high-copper non-gamma-2 amalgams (PMID:3463718).

**Cusp fracture.** "1.88 percent" for amalgam vs "2.29 percent" for composite (PMID:15387051).

**Economics.** UK-based modeling favors amalgam ("Amalgam Dominates", title of PMID:41423779; see also PMID:42498765). These are models, not observed survival.

**Interpretation.** Randomized trials in children drive the pooled advantage for amalgam. Observational results vary, and operator choice and patient risk are likely confounders. Amalgam-specific effects of cavity size, caries risk or bruxism were not retrieved.

---

## 7. Adverse effects and safety

| Effect | Category / term | Evidence |
|---|---|---|
| Oral lichenoid lesion | Hypersensitivity; HP:0031453 | Replacement: "complete resolution in 54.2% (n = 423/781)" (PMID:33273245). "From 16% to 91% of patients had positive patch test results for at least 1 mercury compound." (PMID:15529127). Resolution "OR = 122.18; 95 % CI: 55.64-268.26; p < 0.001", with suspected publication bias (PMID:41658369, 2026). Population prevalence not found |
| Amalgam tattoo | Esthetic; HP/MONDO not found | 17.43% of 241 pigmented oral lesions in a biopsy series (PMID:34753186); not a population rate |
| Galvanic pain | Local | "Galvanic currents can occur and cause pain, but this is generally shortlived and should not influence the dentist's choice of an appropriate restorative material." (PMID:8940574) |
| Postoperative sensitivity | Pulpal | No difference from composite (PMID:1939803). In a later UK survey, composite had "a higher reported incidence of postoperative complications than amalgam" (PMID:33300416) |
| Secondary caries | Failure mode | Lower than composite in Cochrane (section 6) |
| Marginal, bulk or cusp fracture | Mechanical | Section 6 |

**Systemic exposure**
- **Dose:** "low absorbed doses (1-3 micrograms/day)" (PMID:9391753, review, 1997).
- **Urine:** "98.2% of participants had urinary mercury levels below 7 μg Hg/L." (PMID:24015978, descriptive).
- **Blood:** total mercury geometric means of "0.48, 0.69 and 1.17μg/l" by restoration group (PMID:27639196, NHANES).
- **Contrary estimate:** daily vapor dose exceeded the California EPA limit "for about 86 million (54.3%) adults" (PMID:35786065, modeling). The same author's 2024 paper discloses directorship of an advocacy-linked nonprofit: "Both authors are directors of the nonprofit Institute of Chronic Illnesses, Inc." (PMID:38316638; "advocacy-linked" is my characterization).

**Children**
- **RCT (NECAT):** "no statistically significant differences"; IQ change "3.1 vs 2.1, P = .21" (PMID:16622139).
- **RCT (Casa Pia):** neurobehavioral measures "P values from .29 to .91" (PMID:16622140).
- **Kidney:** microalbuminuria "adjusted odds ratio 1.8; 95% confidence interval, 1.1-2.9" in years 3–5 (PMID:18335109).

**Pregnancy**
- **MoBa:** perinatal death "ranged from 0.20% in women with no amalgam-filled teeth to 0.67%"; adjusted "OR of 2.34 (95% CI 1.27 to 4.32; p = 0.007)" in the highest group (PMID:30532171, observational).
- **MoBa, preterm delivery:** "no significant associations between the number of teeth with amalgam fillings and early preterm delivery" (PMID:27146796).
- **Seychelles:** no significant adverse associations (PMID:22041415).

**Removal.** In patients attributing symptoms to amalgam, scores fell "from 43.3 (SD 17.8) at baseline to 30.5 (SD 14.4) at follow-up" (PMID:32810306). The adjusted difference was −8.0 (95% CI −15.4 to −0.5). The design was not randomized. FDA does not recommend removing sound fillings (section 8a).

**Occupational**
- Turkish dental personnel: "33.6% had a blood concentration above 5 ng Hg/mL" (PMID:19081894).
- Clinic air: "84.7 ± 18.67 to 609.3 ± 238.90 µg/m3" (PMID:29043874; one regional study).
- US dentists: tremor "OR, 1.10 [95% CI, 1.00-1.22]"; multiple sclerosis "0.85; 95% CI, 0.39-1.85" (PMID:26314975).

**Expert bodies**
- SCENIHR 2015 found current evidence does not preclude using amalgam or its alternatives, and advised alternatives for primary teeth and pregnant patients ([opinion](https://ec.europa.eu/health/scientific_committees/emerging/docs/scenihr_o_046.pdf)) [S].
- A 2020 risk analysis concluded "amalgam restorations in children and women of childbearing age should be avoided." (PMID:35623360).

**Environment**
- **US rule:** "Dental offices that place or remove amalgam must operate and maintain an amalgam separator and must not discharge scrap amalgam or use certain kinds of line cleaners." EPA expects a reduction "by 5.1 tons" of mercury annually ([EPA](https://www.epa.gov/eg/dental-effluent-guidelines); 40 CFR Part 441).
- **Separator performance:** at least 95% removal efficiency, with existing sources to comply "No later than July 14, 2020." ([eCFR](https://www.ecfr.gov/api/renderer/v1/content/enhanced/2026-10-01/title-40?part=441)).
- Crematorium emissions: no source retrieved.

**Reports.** openFDA MAUDE totals are 161 (EJJ) and 34 (OIV), updated 2026-11-11 ([EJJ](https://api.fda.gov/device/event.json?search=device.device_report_product_code:EJJ&limit=1), [OIV](https://api.fda.gov/device/event.json?search=device.device_report_product_code:OIV&limit=1)). Counts are not incidence rates.

---

## 8. Regulatory status

### 8a. Device type

**21 CFR 872.3070, "Dental amalgam, mercury, and amalgam alloy"** ([eCFR](https://www.ecfr.gov/current/title-21/section-872.3070)).

> (a) Identification. Dental amalgam is a device that consists of a combination of elemental mercury, supplied as a liquid in bulk, sachet, or predosed capsule form, and amalgam alloy composed primarily of silver, tin, and copper, supplied as a powder in bulk, tablet, or predosed capsule form, for the direct filling of carious lesions or structural defects in teeth. This device also includes the individual component devices, mercury and amalgam alloy, when intended to be combined with each other to form dental amalgam.

> (b) Classification. Class II (special controls). The special control for this device is FDA's "Class II Special Controls Guidance Document: Dental Amalgam, Mercury, and Amalgam Alloy." See § 872.1(e) for the availability of this guidance document.

Citation line: [74 FR 38714, Aug. 4, 2009]. The paragraph grants no 872.9 exemption. The regulation uses curly quotation marks around the guidance title. The existing record's snippet uses straight single quotes, which may matter to the quote check.

The existing record's `identification` omits the regulation's final sentence ("This device also includes the individual component devices…").

| Code | Device name | Class | submission_type_id |
|---|---|---|---|
| EJJ | Alloy, Amalgam | 2 | 1 |
| ELY | Mercury | 2 | 1 |
| OIV | Dental Amalgam | 2 | 1 |

These are all three codes under the regulation ([openFDA](https://api.fda.gov/device/classification.json?search=regulation_number:872.3070&limit=20), updated 2026-11-09).

**Approved use:** "the direct filling of carious lesions or structural defects in teeth".

**Former section.** Older letters cite 872.3050 "Amalgam Alloy". The [current-date eCFR request for 872.3050](https://www.ecfr.gov/api/renderer/v1/content/enhanced/2026-11-12/title-21?part=872&section=872.3050) returned 404. FDA's 2009 rule reclassified mercury from class I to class II and classified dental amalgam as class II ([FDA](https://www.fda.gov/medical-devices/dental-amalgam/appendix-i-summary-changes-classification-dental-amalgam-and-mercury)) [S]. The text stating what happened to 872.3050 was not read.

**Special controls guidance** ([FDA](https://www.fda.gov/medical-devices/guidance-documents-medical-devices-and-radiation-emitting-products/dental-amalgam-mercury-and-amalgam-alloy-class-ii-special-controls-guidance-industry-and-fda-staff), issued 2009-07-28):
- Warnings: "WARNING -- CONTAINS MERCURY"; "may be harmful if vapors are inhaled".
- Contraindication: "do not use in persons with a known mercury allergy".
- Precautions: "use with adequate ventilation"; "single-use only"; "store in a cool, well ventilated place".
- Statement of mercury content: "Contains [ ]% mercury by weight".
- Standards named: ISO 24234:2004(E) and ISO 7405:1997(E).

**Prescription status.** K223182, K093587, K033434 and K974035 are marked for prescription use.

**FDA 2020 recommendation.** "the agency is recommending certain high-risk groups avoid getting dental amalgam whenever possible and appropriate." ([FDA, 2020-09-24](https://www.fda.gov/news-events/press-announcements/fda-issues-recommendations-certain-high-risk-groups-regarding-mercury-containing-dental-amalgam)). Groups ([FDA](https://www.fda.gov/medical-devices/dental-devices/dental-amalgam-fillings)):
- pregnant women and their developing fetuses
- women planning to become pregnant
- nursing women and their newborns and infants
- children, especially those younger than six
- people with pre-existing neurological disease
- people with impaired kidney function
- people with known heightened sensitivity (allergy) to mercury or other components

Removal: "The FDA does not recommend anyone remove or replace existing amalgam fillings in good condition" unless considered medically necessary.

**2026 US policy [S].** No 2026 FDA reclassification was found.
- The Indian Health Service will end amalgam use by 2027 ([HHS](https://hhs.gov/press-room/ihs-to-end-use-of-mercury-containing-dental-amalgam-by-2027.html), 2026-02-09).
- HHS encouraged states to restrict Medicaid coverage for D2140–D2161 ([HHS](https://www.hhs.gov/press-room/trump-administration-encourages-states-end-mercury-containing-dental-fillings.html), 2026-07-22).
- The ADA disputes long-term harm ([ADA](https://ada.org/about/press-releases/ada-statement-on-use-of-dental-amalgam-in-the-us), 2026-02-11).

### 8b. Product decisions (all substantially equivalent)

| K number | Product / applicant | Date | Codes | Indications for use |
|---|---|---|---|---|
| [K223182](https://www.accessdata.fda.gov/cdrh_docs/pdf22/K223182.pdf) | Arial Dental, Mistral, World Work Dental Amalgam, BMS Non Gamma 2 Alloy, Flexi Alloy, Hi-S Alloy, WW Dental Amalgam, Hi-Mix, Non Gamma 2 Alloy / WorldWork S.R.L | 2023-05-01 | OIV, EJJ (letter) | "Filling material as a treatment for dental caries" |
| [K140125](https://www.accessdata.fda.gov/cdrh_docs/pdf14/K140125.pdf) | New Stetic Dental Amalgam Alloy (NU Alloy DP 40, DP, DP Active, Micronic) / New Stetic | 2014-04-29 | OIV, EJJ, ELY (letter) | Intended use: "commonly used as a filling material for restoring the morphology and function of posterior teeth (cavities class I and II in molars and premolars), when these have lost their structure due to injuries such as cavities or fractures." |
| [K093587](https://www.accessdata.fda.gov/cdrh_docs/pdf9/K093587.pdf) | Dental Mercury / DMG USA | 2010-01-21 | ELY | "Dental Mercury is elemental mercury, supplied as a liquid packaged in sachets, intended to be combined with amalgam alloy for the direct filling of carious lesions or structural defects in teeth." |
| [K081273](https://api.fda.gov/device/510k.json?search=k_number:K081273) | Ultracaps S / SDI | 2008-07-10 | OIV | Not retrieved (Statement) |
| [K051010](https://fda.innolitics.com/device/K051010) | Securalloy, Septalloy NG 50, NG 70 / Septodont | 2005-05-02 | EJJ | Section 5 (OCR mirror) |
| [K033434](https://www.accessdata.fda.gov/cdrh_docs/pdf3/K033434.pdf) | Bestaloy / We Dong Myung | 2003-11-12 | EJJ | "This is a dental amalgam for the filling of tooth cavities of Black's Classes I and II." |
| [K974035](https://www.accessdata.fda.gov/cdrh_docs/pdf/K974035.pdf) | 21st Century Alloy / Dentsply | 1997-12-17 | EJJ | "21ST CENTURY ALLOY is a dental alloy designed for stress-bearing Class 1 and Class 2 restorations." |
| [K935535](https://api.fda.gov/device/510k.json?search=k_number:K935535) | Tytin / Kerr | 1994-03-11 | EJJ | Not retrieved |
| [K940675](https://api.fda.gov/device/510k.json?search=k_number:K940675) | Sybraloy / Sybron | 1994-04-29 | EJJ | Not retrieved |
| [K820181](https://api.fda.gov/device/510k.json?search=k_number:K820181) | Sybron/Kerr Contour / Sybron | 1982-02-24 | EJJ | Not retrieved |
| [K802967](https://api.fda.gov/device/510k.json?search=k_number:K802967) | Dispersalloy self-… (name truncated) / Johnson & Johnson | 1980-12-30 | DZS | Not retrieved |
| [K801639](https://api.fda.gov/device/510k.json?search=k_number:K801639) | Permite / Southern Dental Industries | 1980-08-27 | EJJ | Not retrieved |
| [K801690](https://api.fda.gov/device/510k.json?search=k_number:K801690) | Valiant / L.D. Caulk | 1980-08-13 | EJJ | Not retrieved |

The decision outcome of the last four records was not captured.

openFDA totals: EJJ 74, ELY 4, OIV 3 510(k) records.

**Discrepancies for the curator**
- **K223182 codes:** letter OIV and EJJ; summary EJJ; openFDA OIV.
- **K140125 codes:** letter OIV, EJJ, ELY; openFDA OIV.
- **Dispersalloy predicate:** K140125 prints K820967 in text but K802967 in tables. openFDA shows K820967 is a biopsy forceps and K802967 is Dispersalloy.
- **K093587:** both the letter and summary print "21 CFR 872.3700", although the regulation name matches 872.3070. It looks like a transposition; openFDA lists ELY under 872.3070.
- **Records under these codes that are not amalgam:** K913814 (sphygmomanometer, ELY), K922100 (drape, EJJ) and K913175 (Miracle Mix glass ionomer, EJJ). The last two are from a model-extracted list.
- **K955285, Galloy:** listed under EJJ in the same unverified list. Galloy is understood to be a gallium alloy, but that was not checked here.

**PMA and De Novo.** PMA queries for OIV, EJJ and ELY returned HTTP 404, which usually means no match but was not confirmed. De Novo, OIV: "No records were found". De Novo was not checked for EJJ or ELY.

**Recalls**

| Number | Product | Started | Reason |
|---|---|---|---|
| Z-1006-2024 | Valiant PhD No. 1 Econo (Ivoclar Vivadent) | 2023-12-21; "Open, Classified" | "the amalgam powder may not triturate correctly" |
| Z-1788-2014 | Tytin Regular Set, lot 3-1294 (Kerr) | 2014-05-29; terminated 2014-10-27 | "it may set faster than specified in the Directions for Use." |

Source: [openFDA EJJ recalls](https://api.fda.gov/device/recall.json?search=product_code:EJJ&limit=20). OIV and ELY recall queries returned 404 (no match, unconfirmed). Recall class was not captured.

### 8c. Other jurisdictions

- **EU MDR class:** IIa, Rule 8, "Placed in the teeth" ([FIDE list, 2022](https://www.fide-online.org/wp-content/uploads/2023/10/Classification_of_dental_devices_according_MDR_2022-02-01-final.pdf)). FIDE is an industry body and its list "does not claim to be complete or legally valid". Notified-body route and harmonized standards were not verified.
- **EU mercury law:** Regulation (EU) 2024/1849 amends 2017/852. "from 1 January 2025, dental amalgam should not be used for dental treatment in the Union", except when strictly necessary. Derogation "until 30 June 2026"; export ban from 2025-01-01; import and manufacture ban from 2026-07-01 ([Parliament summary](https://oeil.europarl.europa.eu/oeil/en/document-summary?id=1786205)). The [EUR-Lex text](https://eur-lex.europa.eu/eli/reg/2024/1849/oj/eng) could not be loaded.
- **Canada [S]:** a Health Canada review kept the 1996 position statement, and bulk powder licences were discontinued ([review](https://dhpp.hpfb-dgpsa.ca/review-documents/resource/SSR00263)). Risk class not found.
- **Northern Ireland [S]:** phase-out date 2034-12-31 unless an earlier global date is agreed ([BDA](https://www.bda.org/news-and-opinion/news/minamata-convention-decision-on-phasing-out-amalgam/)).
- **MHRA class, TGA:** not found. **PMDA, NMPA, ANVISA:** not searched.

---

## 9. Standards

| Standard | Title | FDA recognition |
|---|---|---|
| [ISO 24234:2021](https://www.iso.org/standard/77495.html) (3rd ed., 2021-08) | Dentistry - Dental Amalgam | 4-315, complete; EJJ, ELY (repository notes) |
| ISO 20749:2023 (2nd ed.) | Dentistry - Pre-capsulated dental amalgam | 4-318; listed for OIV |
| ISO 7488:2018 (2nd ed.) | Dentistry - Mixing machines for dental amalgam | 4-288 |
| ISO 11143:2008 (2nd ed.) | Dentistry - Amalgam separators | 4-334, complete |
| ANSI/ADA 41-2020 | Biocompatibility in dentistry | 4-295; listed for OIV |
| ISO 7405:2018 (3rd ed., corrected 2018-12) | Biocompatibility of dental devices (title to verify) | 4-261 (repository notes) |
| ANSI/ADA 144-2025 | Counterpart to ISO 20749 | As listed by FDA search |
| ANSI/ADA 108-2009, Addendum (R2022) | Amalgam Separators | As listed by FDA search |
| ANSI/ADA 43-2020 (R2025) | Electrically Powered Dental Amalgamators | As listed by FDA search |

Sources: [FDA recognized standards search](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfStandards/results.cfm?title=dental+amalgam), [OIV record](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpcd/classification.cfm?ID=OIV), and `docs/regulatory.md`. FDA's 11143 listing differs from any newer ISO edition; currency was not checked. ISO lists 24234:2021 as marked for revision [S].

**Edition history** (PMID:28220332):

| Edition | Ag min | Sn max | Cu max | Zn max | Other max |
|---|---|---|---|---|---|
| ISO 1559:1978 | 65% | 29% | 6% | 2% | Hg 3% |
| ISO 1559:1986 | 40% | 32% | 30% | 2% | Hg 3% |
| ISO 24234:2015 | 40% | 32% | 30% | 2% | In 5%, Pd 1%, Pt 1%, Hg 3% |

---

## 10. Commercial products

| Product | Manufacturer | Subtype | FDA reference |
|---|---|---|---|
| Dispersalloy | Johnson & Johnson (1980) | Admixed, high copper | K802967 |
| Tytin | Kerr | "spherical amalgam" (PMID:8710705) | K935535; recall Z-1788-2014 |
| Sybraloy | Sybron/Kerr | Spherical, high copper | K940675 |
| Contour | Sybron/Kerr | Admixed, high copper | K820181 |
| Permite | SDI | "non-gamma 2 admix alloy" ([SDI](https://www.sdi.com.au/en-us/product/permite/)) | K801639 |
| GS-80 Spherical | SDI | Spherical, non-gamma-2 ([SDI](https://www.sdi.com.au/en-eu/?p=7945)) | EJJ listing; K number not found |
| Ultracaps S | SDI | Not established | K081273 |
| Valiant | L.D. Caulk (1980) | Not established | K801690 |
| Valiant PhD | Ivoclar Vivadent (recalling firm) | Not established | Recall Z-1006-2024; K number not found |
| Micronic | New Stetic | Lathe-cut, low copper | K140125 |

Openly listed registrations: [OIV](https://api.fda.gov/device/registrationlisting.json?search=products.product_code:OIV&limit=20) (5), [EJJ](https://api.fda.gov/device/registrationlisting.json?search=products.product_code:EJJ&limit=20) (46). A listing does not prove current sale. Laboratory studies cited here repeatedly use Dispersalloy and Tytin as comparators.

---

## 11. History and trends

- **Early period:** amalgam has been the traditional posterior material "for the last 150 years" (PMID:24683067, 2014). A historical review covers G. V. Black and the two Amalgam Wars (PMID:1557606).
- **Formulation:** ISO copper limits rose from 6% to 30% between the 1978 and 1986 editions (PMID:28220332). The 1963 Innes and Youdelis dispersion paper was not found in PubMed, so no PMID is given.
- **US use:** amalgam restorations in FDA-identified populations "declined from 21.8% in 2017 to 4.1% in 2023" (PMID:39243252). In NHANES 2011–2016, "about half (51.5 percent) of restored teeth in the US population contained amalgam." (PMID:33954994). Private pediatric claims showed the sharpest decline in 2014 (PMID:37500233).
- **England:** amalgam "still represented a large proportion (42%) of the restorations (circa 1.8 million)" (PMID:31864347, 2019; population and year not captured).
- **Minamata [S]:** COP-6 (Geneva, 3–7 November 2025) agreed to phase out manufacture, import and export by 2034, with exceptions where practitioners consider amalgam necessary ([UNEP](https://www.unep.org/globalmercurypartnership/our-work/mercury-products/phasing-down-the-use-of-dental-amalgam), [Convention](https://minamataconvention.org/en/topics/dental-amalgam/insights)). Earlier measures restrict use in children and in pregnant or breastfeeding women. The decision text was not read.
- **Readiness:** among surveyed dentists in Türkiye, "Only 40.2% had heard of the Minamata Convention, and 21.1% were aware" of the 2034 phase-out (PMID:42714322, 2026; the final clause is paraphrased).

---

## Curation priorities

1. **Regulatory:** complete the identification text, and add the 2020 FDA groups and the labeling controls.
2. **Composition and properties:** use the K140125 and K223182 tables, labeled as manufacturer bench data.
3. **Performance:** record both the Cochrane 2021 result and the conflicting 2025 meta-analysis.
4. **Lichenoid lesions:** attach PMID:33273245. Do not support "rare" from these sources, because they give no population frequency.
5. **Before quoting:** open every [S] source, and re-fetch every PMID not listed as read directly.
6. **Remaining searches:** modulus, fracture toughness, thermal values, gingival response, crematorium emissions, palladium and indium ChEBI element terms, NCIt, and non-EU device classes.

## Reference Validation

Checked with `linkml-reference-validator` 0.8.0.

| Outcome | Count |
| --- | --- |
| References checked | 87 |
| Resolved | 84 |
| Unresolved (possible confabulation) | 3 |
| Unverifiable | 0 |
| Quoted claims checked | 38 |
| Quoted claims found in source | 30 |
| Quoted claims **not** found in source | 8 |
| Quoted claims with nothing to check against | 3 |
| References weighed for topical relevance | 84 |
| On topic | 39 |
| Off topic | 0 |

### Unresolved references

These identifiers did not resolve to a record and may be fabricated. A lookup that failed for transport reasons is indistinguishable from one that failed because the record does not exist, so spot-check before acting on them:

- `PMID:37380250` (1 mention) - Identifier did not resolve to a record
- `PMID:19370602` (1 mention) - Identifier did not resolve to a record
- `PMID:16417916` (1 mention) - Identifier did not resolve to a record

### Quotes not found in the cited source

Searched the abstract, any retrieved full text, and the title. A quote drawn from a part of the paper that was not retrieved will appear here too, so check before treating one as invented:

Every one of these was searched against an abstract alone, with no full text retrieved - marked *abstract only* below. Where full text can be fetched, re-running with it will settle them; where the source publishes only a summary to PubMed, as GeneReviews chapters do, it will not, and the quote has to be checked by hand against the chapter itself.

- `PMC:PMC3010024` *(abstract only)*: "Composition of currently used alloy is silver 40–70%, tin 12–30% and copper 12–24%. It may also include indium 0–4%, palladium 0.5% and zinc up to 1%."
  - closest text in source: "The PubMed database was used initially; the reference list for dental amalgam featured 8641 articles and 13 publications dealing with recent advances in dental amalgam"
- `PMID:37176331` *(abstract only)*: "the Sn8Hg (γ2 phase) occupies about 15% vol. of the mixed alloy"
  - closest text in source: "Dental amalgam is an alloy consisting of a mixture of fine metallic powder of silver, tin, zinc, copper, and a trace amount of palladium in combination with about fifty percent elemental mercury that forms a matrix phase"
- `PMID:28220332` *(abstract only)*: "at around 12%, it has almost disappeared"
  - Text part not found as substring: 'at around 12%, it has almost disappeared' (note: only abstract available for PMID:28220332, full text may contain this excerpt)
- `PMID:28220332` *(abstract only)*: "is transformed to the β1-phase with considerably less mercury"
  - closest text in source: "Firstly, when subjected to wear/polishing, droplets rich in mercury are formed on the surface, showing that mercury is not being strongly bonded to the base or alloy metals"
- `PMID:21217947` *(abstract only)*: "In 1959, Dr. Wilmer Eames recommended a 1:1 ratio of mercury to alloy"
  - Text part not found as substring: 'In 1959, Dr. Wilmer Eames recommended a 1:1 ratio of mercury to alloy' (note: only abstract available for PMID:21217947, full text may contain this excerpt)
- `PMID:21217947` *(abstract only)*: "Some researchers believe that if zinc containing amalgam is contaminated with moisture, it causes delayed expansion."
  - closest text in source: "The PubMed database was used initially; the reference list for dental amalgam featured 8641 articles and 13 publications dealing with recent advances in dental amalgam"
- `PMID:38316638` *(abstract only)*: "Both authors are directors of the nonprofit Institute of Chronic Illnesses, Inc."
  - Text part not found as substring: 'Both authors are directors of the nonprofit Institute of Chronic Illnesses, Inc.' (note: only abstract available for PMID:38316638, full text may contain this excerpt)
- `PMID:26314975` *(abstract only)*: "0.85; 95% CI, 0.39-1.85"
  - Text part not found as substring: '0.85; 95% CI, 0.39-1.85' (note: only abstract available for PMID:26314975, full text may contain this excerpt)

### Quotes that could not be checked

There was no text to compare these against, so they are neither confirmed nor contradicted:

- `PMID:30998445`: "673 μg/L ± 179 in the 7.0-T MRI group, 172 μg/L ± 60 in the 1.5-T MRI group, and 141 μg/L ± 152 in the control group."
  - Reference resolved but exposes no abstract or full text to search
- `PMID:37380250`: "formulated 16 recommendations and good practice statements"
  - Reference did not resolve, so the quote could not be checked
- `PMID:19370602`: "There were no significant differences found in all three trials for all of the outcomes assessed."
  - Reference did not resolve, so the quote could not be checked

## Term Validation

Checked with `linkml-term-validator` 0.4.5, through the `ols:` adapter.

| Outcome | Count |
| --- | --- |
| Terms checked | 12 |
| Resolved | 12 |
| Unresolved (possible confabulation) | 0 |
| Obsolete | 0 |
| Unverifiable | 0 |
| Terms whose name was checked | 3 |
| Terms named correctly | 0 |
| Terms named as a **different** term | 3 |

### Terms the report names something else

These identifiers resolve, so nothing about them looks wrong, and the ontology calls them something unrelated to what the report calls them. That usually means the identifier is not the one the sentence needs:

- `CHEBI:30512` (1 mention) - the report calls it "existing record"; CHEBI calls it **silver atom**
- `CHEBI:27007` (1 mention) - the report calls it "existing record"; CHEBI calls it **tin atom**
- `CHEBI:28694` (1 mention) - the report calls it "existing record"; CHEBI calls it **copper atom**