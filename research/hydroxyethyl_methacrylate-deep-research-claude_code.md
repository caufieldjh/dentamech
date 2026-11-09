---
provider: claude_code
model: claude-fable-5-1, claude-haiku-4-5-20251001
cached: false
start_time: '2026-09-04T21:58:17.737105'
end_time: '2026-09-04T22:09:31.493597'
duration_seconds: 673.76
template_file: templates/dental_material_research.md
template_variables:
  material_name: Hydroxyethyl methacrylate
  ohd_id: OHD:0001082
  ohd_label: hydroxyethyl methacrylate dental restoration material
  category: ADHESIVE
  ohd_definition: A dental restoration material which is a hydrophilic monomer used
    in dental adhesives, and primers.
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
  - claude-fable-5-1
  - claude-haiku-4-5-20251001
  web_search_requests: 9
  num_turns: 73
  total_cost_usd: 4.99960925
  session_id: 80b45055-eaf3-4ad9-b534-68f0da97d009
  stop_reason: end_turn
  permission_denials: 4
  denied_tools:
  - Bash
  assistant_text_blocks: 3
citation_count: 25
reference_validation:
  total_references: 49
  verified: 49
  not_found: 0
  unverifiable: 0
  confabulation_rate: 0.0
  quotes_checked: 32
  quotes_valid: 29
  quotes_unsupported: 3
  unsupported_quote_references:
  - PMID:15186380
  - PMID:26916063
  - DOI:10.3389/fdmed.2023.1155820
  relevance_assessed: 49
  on_topic: 33
  needs_review: true
  validator_version: 0.2.1
---

## Question

# Dental Material Research Template

## Target Material
- **Material name:** Hydroxyethyl methacrylate
- **OHD term:** OHD:0001082 (hydroxyethyl methacrylate dental restoration material)
- **Category:** ADHESIVE
- **OHD definition:** A dental restoration material which is a hydrophilic monomer used in dental adhesives, and primers.

## Research Objectives

Provide a comprehensive, citation-dense research report on **Hydroxyethyl methacrylate** as a
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
- For standards, cite the ISO or ADA catalog entry by URL.
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

I will research HEMA now and write the report inline. First I load the web tools.

I need verbatim abstracts for Schweikl 2006, Van Landuyt 2005, and Gerzina and Hume 1996, plus the first three PMIDs from the MMP search. Both fetches are independent.

The OAK lookups for OHD and ChEBI did not run. The approval gate blocked both commands. I verified the ChEBI term through the OLS API instead. The OHD term comes from the template only. The iso.org catalog refused fetches, so ISO titles come from the FDA recognized standards list and vendor mirrors. The EUR-Lex fetch did not return Annex VIII, so the EU rule is reported from secondary sources and flagged as such.

# Hydroxyethyl methacrylate (HEMA) as a dental restoration material

**Target:** OHD:0001082, hydroxyethyl methacrylate dental restoration material. Category ADHESIVE. OHD definition: "A dental restoration material which is a hydrophilic monomer used in dental adhesives, and primers."

**Evidence key.** [HC] human clinical. [IV] in vitro or laboratory. [SR] systematic review or meta-analysis. [REV] narrative review. [REG] regulatory document. [STD] technical standard. [MFR] manufacturer document. [DB] database record.

---

## 1. Identity and nomenclature

HEMA is a monomer, not a finished restorative. It is the monomethacrylate ester of ethylene glycol. It carries one polymerizable methacrylate group and one free hydroxyl. The hydroxyl makes it miscible with water. The methacrylate lets it copolymerize with the dimethacrylates that form the bulk of adhesive resins. That is the whole reason it is in the mouth. It sits between water and resin and joins the two.

ChEBI defines it as "An enoate ester that is the monomethacryloyl derivative of ethylene glycol." (CHEBI:34288, retrieved via the OLS API, https://www.ebi.ac.uk/ols4/api/search?q=2-hydroxyethyl%20methacrylate&ontology=chebi) [DB]

**Distinction from neighbors.** HEMA is monofunctional and hydrophilic. Its neighbors in an adhesive are the cross-linking dimethacrylates (bis-GMA, UDMA, TEGDMA) and the acidic functional monomers (10-MDP, 4-META, phenyl-P). HEMA does not etch and does not cross-link. It wets and it carries. The Leuven review states the class of ingredients this way: "Irrespective of the number of bottles, an adhesive system typically contains resin monomers, curing initiators, inhibitors or stabilizers, solvents and sometimes inorganic filler. Each one of these components has a specific function." (Van Landuyt et al., Biomaterials 2007, PMID:17543382) [SR]

**Synonyms and shorthand**

| Form | Source |
|---|---|
| 2-hydroxyethyl methacrylate | ChEBI:34288, NCIt C47791 |
| HEMA, 2-HEMA | universal clinical shorthand; "2-HEMA" in the dermatology literature (PMID:16958920, PMID:17937748) |
| 2-hydroxyethyl 2-methylprop-2-enoate | IUPAC name, PubChem CID 13360 |
| ethylene glycol monomethacrylate, glycol methacrylate | trade and older chemical names (not verified against a vocabulary this session) |
| CAS 868-77-9 | stated on the 3M Scotchbond Universal SDS (see §2) |

**Identifiers in other vocabularies**

| Vocabulary | Identifier | Note |
|---|---|---|
| ChEBI | CHEBI:34288 "2-hydroxyethyl methacrylate" | Related: CHEBI:53537 poly(2-hydroxyethyl methacrylate) macromolecule; CHEBI:60758 poly(2-hydroxyethyl methacrylate) polymer |
| NCIt | C47791 "2-Hydroxyethyl Methacrylate" | https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/search?term=hydroxyethyl%20methacrylate |
| PubChem | CID 13360 | C6H10O3, MW 130.14, InChIKey WOBHKFSMXKNTIM-UHFFFAOYSA-N |
| Wikidata | Q424799 | |
| MeSH | No descriptor of its own found. PubMed indexes HEMA papers under the descriptor "Methacrylates" (see the cached records for PMID:29649505 and PMID:35341601). A MeSH database search for "hydroxyethyl methacrylate" returned only supplementary concept records for branded products that contain HEMA (e.g. UID 67446260 "One-Up-Bond F", UID 67407402 "Unifil Bond"). I did not confirm whether a standalone HEMA supplementary concept exists. | |
| SNOMED CT | Not searched. | |
| OHD | OHD:0001082 (from the template). The OAK lookup was blocked, so parent and sibling links in OHD were not read this session. | |

**Taxonomy.** HEMA belongs to the methacrylate monomers. In the dental materials taxonomy it is a component class, used in: dental adhesives and primers (its OHD category), resin-modified glass ionomer cements (RMGIC), resin cements, desensitizers (with glutaraldehyde), and some composites. There are no recognized "subtypes" of HEMA. The meaningful split in practice is between HEMA-containing and HEMA-free adhesives.

---

## 2. Composition

HEMA is itself a single compound. This section reports what it is, and how much of it sits in the materials that contain it.

**Chemical identity** [DB]

| Property | Value | Source |
|---|---|---|
| Formula | C6H10O3 | PubChem CID 13360 |
| Molecular weight | 130.14 g/mol | PubChem CID 13360 |
| ChEBI role suggestion | CHEBI:34288 as the monomer; polyHEMA CHEBI:60758 for the cured phase | OLS |

**Functional role by host material**

| Host material | Role of HEMA | Typical proportion | Source |
|---|---|---|---|
| Etch-and-rinse and self-etch adhesives, primers | Hydrophilic co-monomer, wetting agent, diffusion promoter, solvent-compatibilizer that prevents phase separation | 10 to 36 wt% in experimental one-step adhesives (PMID:18433860); 15 to 25 wt% in 3M Scotchbond Universal per its SDS | [IV], [MFR] |
| Resin-modified glass ionomer cement (liquid) | Polymerizable resin component of the liquid; makes the acid-base cement light-curable | 25 to 50 wt% of the liquid in GC Fuji II LC (Improved) per its SDS | [MFR] |
| Desensitizer (Gluma) | Active agent with glutaraldehyde | 35% HEMA with 5% glutaraldehyde (PMID:34013195) | [HC] |
| Resin cements | Hydrophilic monomer | Not quantified this session; HEMA is released from RelyX ARC, Panavia F 2.0, and Multilink Automix (PMID:26714346) | [IV] |

The Leuven group states the rationale in one line: "In spite of its high allergenic potential, 2-hydroxyethyl methacrylate (HEMA), a low-molecular-weight monomer, is frequently used in adhesives for its positive influence on the bond strength." (PMID:18433860) [IV]

Chemical analysis of commercial products supports the frequency claim: "The most frequently occurring methacrylates in the bonding materials were 2-hydroxyethyl methacrylate (2-HEMA) and bis-GMA." (Henriks-Eckerman et al., Contact Dermatitis 2004, PMID:15186380) [IV] The same paper found that "information about methacrylates was given in the safety data sheets for about half of the products."

Manufacturer sources for proportions:
- 3M Scotchbond Universal SDS (multiple mirrors returned by search; e.g. https://www.henryschein.co.nz/documents/msds/LIVE/3M/Scotchbond%20Universal_SDS_EXP_20240410.pdf). Search summary reported 2-hydroxyethyl methacrylate, CAS 868-77-9, at 15 to 25% by weight. I did not open the PDF itself. [MFR]
- GC Fuji II LC (Improved, Liquid) SDS, https://www.gc.dental/america/sites/america.gc.dental/files/products/downloads/gcfujiiilc/sds/gc-fuji-ii-lc-improved-liquid-sds-en.pdf. Search summary reported HEMA 25 to 50%, polybasic carboxylic acid 5 to 10%, UDMA 1 to 5%, dimethacrylate 1 to 5%. I did not open the PDF itself. [MFR]

**Named formulation variants.** The clinically meaningful split is HEMA-containing versus HEMA-free adhesives. HEMA-free products replace it with other hydrophilic monomers, methacrylamides, or rely on solvents alone. Alternatives studied: glycerol dimethacrylate (PMID:29574280), methacrylamide-methacrylate hybrids (PMID:32536589), hydroxypropyl methacrylate and tetrahydrofurfuryl methacrylate in RMGIC (PMID:34462139).

---

## 3. Setting and handling

**Setting mechanism.** HEMA polymerizes by free-radical addition through its methacrylate group. In adhesives that is light-cured (camphorquinone and amine systems), self-cured, or dual-cured. In RMGIC it runs alongside the acid-base reaction: "The setting of resin-modified glass ionome cements (RMGIC) involves the acid-base reaction and the polymerization of HEMA monomers." (Dursun et al., Dent Mater 2016, PMID:26916063; the quoted fragment is as the summarizer returned it, with "ionomer" spelled in full in the original) [IV]

**What HEMA does during application.** It stops the resin from separating from water. Van Landuyt et al. 2005 observed droplets in HEMA-free one-step adhesives and found the droplets vanished when HEMA was added. Their reading: the finding "strongly suggests that the adhesive monomers separate from water upon evaporation of ethanol/acetone." (J Dent Res 2005, PMID:15668338) [IV] The 2025 systematic review restates the trade: "the lack of HEMA in the adhesive composition may lead to a separation phase between hydrophobic and hydrophilic components." (PMID:39838443) [SR]

**Concentration matters.** Too much HEMA hurts. "A small amount of HEMA (10%) improved the bond strength of a one-step self-etch adhesive. When added in higher concentrations, this beneficial effect of HEMA on the bond strength is lost due to increased osmosis, which resulted in many droplets." (PMID:18433860) [IV] At the polymer level: "At 40 s of light activation time, groups G30 and G50 showed a decrease of 30% and 61%, respectively, in degree of conversion compared to control." (Collares et al., J Adhes Dent 2011, PMID:21594225) [IV]

**Dentin moisture.** HEMA-containing and HEMA-free adhesives want different dentin. "Dry surfaces enabled obtaining optimal bonding for HEMA-containing adhesives to bur-cut dentin, while wet surfaces enabled optimal bonding for HEMA-free adhesives." (Saeed et al., J Adhes Dent 2021, PMID:34269543) [IV]

**RMGIC timing.** Delay before light-curing raises HEMA release. Dursun et al. found "a delay in light-activation caused a significant increase in the cumulative HEMA release" and that "a short delay before light-curing could limit the HEMA release and could be more biocompatible." (PMID:26916063) [IV]

**Working and setting times.** These belong to the host product, not to HEMA. Not reported at the monomer level.

**Technique sensitivity.** Simplified HEMA-rich adhesives take up water. Tay and Pashley asked the question in the title: "Have dentin adhesives become too hydrophilic?" They wrote that "simplified adhesives are more permeable to water and hence absorb more water over time," and that this can cause "incompatibility of chemically or dual-cured composites" and "expedited degradation of resin-dentin bonds." (J Can Dent Assoc 2003, PMID:14653938) [REV]

---

## 4. Physical, mechanical, chemical, and biological properties

**Physical constants of the monomer** (PubChem CID 13360, Experimental Properties section, https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/13360/JSON?heading=Experimental+Properties) [DB]

| Property | Value | Cited source in PubChem |
|---|---|---|
| Boiling point | 67 °C at 3.5 mm Hg | CRC Handbook |
| Freezing point | −12 °C | Hawley's |
| Density | 1.034 at 25 °C/4 °C | CRC Handbook |
| Water solubility | "Miscible with water and soluble in common org solvents" | Hawley's |
| Vapor pressure | 0.126 mm Hg at 25 °C | Physical and Thermodynamic Properties of Pure Chemicals |
| Refractive index | 1.4515 at 20 °C | CRC Handbook |
| log P (octanol/water) | 0.47 | Hansch et al. |
| Flash point | 97 °C closed cup | Handbook of Organic Chemistry |

**Bond strength** [IV]

| Adhesive (HEMA status) | Substrate, test | Value | Source |
|---|---|---|---|
| Glutaraldehyde/HEMA on EDTA-treated dentin | Tensile | 17.5 ± 1.0 MPa, "unaffected by water storage at 37 degrees C for up to 6 months" | PMID:3933103 (1985) |
| HEMA + propionic aldehyde; HEMA + glutaraldehyde | Tensile to dentine | 15 and 18 MN/m² | PMID:3926655 (1985) |
| Scotchbond Universal Plus (HEMA-containing) | Shear to dentin | mean 24.78 MPa | PMID:36837160 (2023) |
| G2-Bond Universal (HEMA-free two-bottle) | Shear to dentin, after one year | mean 35.15 MPa | PMID:36837160 (2023) |
| Five universal adhesives, selective enamel etch, human enamel and dentin | Shear, before and after 10,000 thermocycles | "Lowest shear bond strength values were observed for 2-hydroxyethylmethacrylate (HEMA)-free systems." | PMID:38308570 (2024) |
| Experimental one-step self-etch, 0/10/19/36% HEMA | Microtensile, 24 h | "Exp-10 performed best." Exp-36 "yielded the lowest bond strength." | PMID:18433860 (2008) |

The two 2023 and 2024 shear studies point in opposite directions on HEMA-free versus HEMA-containing. Both are single-lab in vitro tests with different products and protocols. Jäggi et al. close with: "When applied in the selective enamel etching mode, a stable bond can be expected from adhesives containing HEMA and monomers with phosphate groups." (PMID:38308570) Brkanović et al. close with: "These findings imply that the HEMA-free universal adhesive G2-Bond Universal is the most effective universal adhesive for clinical practices, particularly when applied in the self-etch mode." (PMID:36837160)

**Degree of conversion, water sorption, solubility, ultimate tensile strength** [IV]

Collares et al. varied HEMA at 0, 15, 30, and 50 wt% in a bis-GMA/bis-EMA/TEGDMA blend. Degree of conversion fell 30% at 30 wt% and 61% at 50 wt%. "Water sorption and solubility differed for all groups, and was statistically higher in G50. For ultimate tensile strength, the control and G15 groups showed statistically higher values than the other groups (p < 0.05)." Conclusion: "Higher HEMA content increases dental adhesive resin degradation." (PMID:21594225)

Araújo-Neto et al. compared 20 wt% HEMA against 20 wt% glycerol dimethacrylate: "The nanoleakage was higher and gaps were found in the interface of HEMA-containing adhesives, which were less present in GDMA equivalents." (PMID:29574280) Water sorption and solubility in that study followed the ISO 4049 method.

Park et al. used bis-GMA/HEMA as the control in a urethane trimethacrylate study; all experimental blends "showed less water sorption, lower tandelta peak heights, and higher rubbery modulus than the control." (PMID:19709724)

**Hydrolytic stability.** The ester bond in HEMA is labile. Fugolin et al.: "The susceptibility of methacrylates to hydrolytic and enzymatic degradation may be a contributing factor limiting the clinical lifespan of resin composite restorations. The elimination of labile ester bonds is a potential advantage of methacrylamides, which have been shown to produce more stable restorative interfaces." (Dent Mater 2020, PMID:32536589) [IV]

**Diffusion through dentin** [IV]

- Gerzina and Hume 1996: a HEMA-containing bonding resin under a TEGDMA composite "reduced TEGDMA diffusion only slightly" and added substantial HEMA diffusion into the pulp chamber. (PMID:8636483)
- Tak and Usumez 2015: HEMA from three resin cements was detected in the pulp chamber elutes of all 60 teeth. Thinner remaining dentin increased diffusion. (Am J Dent 2015, PMID:26714346)
- Tak and Usumez 2013: HEMA diffusion did not differ between caries-affected and sound dentin (p = 0.80). The authors judged the highest eluted concentration to be below cytotoxic levels. (J Prosthodont 2013, PMID:23107279)

**HEMA release from RMGIC** [IV]

- "Vitremer showed highest HEMA release" among Advance, Vitremer, and Protec-Cem; "Protec-Cem showed the lowest values." The authors wrote that this "release may be relevant both to the risk of adverse pulpal responses in patients and to the risk of allergy." (Beriat and Nalbant, Eur J Dent 2009, PMID:19826597)
- Delayed light activation raised cumulative HEMA release (PMID:26916063).

**Biocompatibility and cytotoxicity** [IV]

| Cell system | Concentration | Finding | Source |
|---|---|---|---|
| Human lymphocytes, A549 | up to 10 mM, 1 h | No loss of viability, but "HEMA induced concentration-dependent DNA damage in lymphocytes"; "HEMA induced apoptosis in a concentration-dependent manner and caused cell-cycle delay at the G0/G1-checkpoint." | PMID:20079459 (2010) |
| Human dental pulp mesenchymal stem cells | 3 and 5 mM, 24 to 72 h | "2-Hydroxyethyl methacrylate exhibited cytotoxicity, inhibited cell growth and induced morphological changes in cultured DP-MSCs." IL-6 and IL-8 up-regulated. | PMID:21899564 (2012) |
| Dental pulp stem cells, angiogenic differentiation | 0.1 and 0.5 mM | "Non-cytotoxic HEMA concentrations seem to have a minor impact on the expression of angiogenic markers, essentially on the mRNA level, without affecting the angiogenic differentiation process itself on a detectable level." | PMID:33579530 (2021) |
| Human pulp fibroblasts and odontoblast-like cells, LPS/LTA stimulated | not stated in abstract | "HEMA inhibited the LPS- and LTA-induced IL-6 release"; "The protective immune response in odontoblasts and pulp fibroblasts is impaired by monomers such as HEMA through the disturbance of the redox homeostasis." | PMID:35341601 (2022) |
| Human pulp fibroblasts | HEMA 10 to 1000 nM; Single Bond eluates | "Protein levels of CXCL12 were significantly decreased only by HEMA." Authors warn that adhesives used "as pulp capping materials must be viewed with caution due to its large cytotoxic effect when in close contact with the pulp." | PMID:30517439 (2018) |
| Human dental pulp cells, experimental adhesive eluates | 0, 10, 20% HEMA, ± 10% ethanol | "Higher HEMA concentrations, combined with the presence of solvent, can promote significant reduction on HDPC viability, increasing the release of anti- and pro-inflammatory mediators." | PMID:31461952 (2019) |

The mechanism review by Schweikl, Spagnuolo, and Schmalz frames this as oxidative stress: monomers deplete glutathione, reactive oxygen species rise, and antioxidants such as N-acetylcysteine, ascorbate, and Trolox block the effect. (J Dent Res 2006, PMID:16998124) [REV]

For RMGIC as a host: "HEMA is known to be released" with effects "ranging from pulpal inflammation to allergic contact dermatitis"; the authors conclude RMGICs "cannot be considered biocompatible to nearly the same extent as conventional glass-ionomers." (Nicholson and Czarnecka, Dent Mater 2008, PMID:18539324) [REV] Sidhu and Nicholson repeat that RMGIC biocompatibility is "somewhat compromised by the presence of the resin component, 2 hydroxyethyl methacrylate." (J Funct Biomater 2016, PMID:27367737) [REV]

**Sensitization.** See §7. HEMA is the lead methacrylate allergen in dental personnel.

**Antibacterial activity.** None attributed to HEMA. Not applicable.

**Properties not reported at the monomer level.** Flexural strength, compressive strength, elastic modulus, fracture toughness, hardness, wear, shrinkage stress, depth of cure, thermal expansion, radiopacity, translucency, fluoride release, film thickness, corrosion. These belong to host products. HEMA lowers cross-link density and modulus when raised in proportion (PMID:21594225, PMID:29574280), but no absolute value for a HEMA phase is meaningful.

---

## 5. Clinical uses and indications

HEMA has no stand-alone indication. Its uses are the uses of its host products.

| Clinical context | Host material | Suggested OHD procedure | Suggested UBERON site | Evidence |
|---|---|---|---|---|
| Adhesive bonding of direct resin composite | Etch-and-rinse, self-etch, universal adhesives | resin filling restoration procedure; tooth bonding procedure | dentine (UBERON:0001752), enamel (UBERON:0001753) | PMID:29649505 [SR], PMID:39838443 [SR] |
| Dentin priming | Primers of two-step self-etch and three-step etch-and-rinse systems | tooth bonding procedure | dentine | PMID:17543382 [SR] |
| Luting of indirect restorations, core build-up bonding, repair | Universal adhesives per the 510(k) indications | crown restoration procedure; luting procedure | tooth crown (UBERON:0001754) | K192961 [REG] |
| Restoration and lining with RMGIC | Fuji II LC, Vitremer and similar | glass ionomer filling restoration procedure | dentine, tooth crown | PMID:27367737 [REV], PMID:18539324 [REV] |
| Dentin hypersensitivity treatment | Gluma Desensitizer (5% glutaraldehyde, 35% HEMA) | dentin desensitization procedure | dentine, tooth root (UBERON:0001756) | PMID:34013195 [HC], PMID:23243978 [HC], PMID:16296439 [HC] |
| Dentin sealing before amalgam, fissure sealant bonding, root surface desensitization | Universal adhesive per label | | | K192961 [REG] |

The regulatory indications for one HEMA-containing universal adhesive read: "A material primarily intended to be used as a bonding-promoting substance between tooth substance and dental restorations. It may also be used as a dentin sealant and as a bonding agent for repair of restorations." (K192961 summary as mirrored at https://fda.innolitics.com/device/K192961) [REG]

**Desensitizer evidence.** After orthodontic debonding, Gluma and a remineralizing paste both produced "98 percent reduction in DH between T0 and T3" (PMID:34013195) [HC]. Against oxalate and placebo over six months, "Pain reduction with GLU was consistently highest" (PMID:23243978) [HC]. In vitro, Gluma cut dentin permeability on albumin-soaked discs (PMID:21552716) [IV].

**Contraindications.** Known methacrylate or HEMA allergy in the patient. Direct pulp contact is cautioned in the pulp-cell literature (PMID:30517439). Product labels carry these; I did not read a label this session.

**Primary versus permanent dentition.** The two systematic reviews on HEMA-free versus HEMA-containing adhesives restricted to permanent dentition (PMID:39838443 excluded primary teeth explicitly). No primary-dentition evidence specific to HEMA was found.

---

## 6. Clinical performance and longevity

The clinical question that has been asked is whether HEMA helps or hurts. The answer from two systematic reviews is that it does neither, measurably.

**Meta-analysis, non-carious cervical lesions.** Twenty-two RCTs, 997 participants. "no significant statistical difference was found between the clinical performances of HEMA-free and HEMA-containing adhesive systems for all parameters analyzed: retention risk difference (RD) 0.03 [-0.01, 0.07] (p = 0.13); marginal discoloration RD 0.02 [-0.01, 0.04] (p = 0.19); marginal adaptation RD -0.01 [-0.04, 0.01] (p = 0.34); caries RD 0.00 [-0.01, 0.01] (p = 0.92); or postoperative sensitivity RD -0.00 [-0.02, 0.01] (p = 0.72)". Conclusion: "HEMA-free and HEMA-containing adhesive systems showed a similar clinical performance in NCCL restorations." (da Silva et al., J Dent 2018, PMID:29649505) [SR]

**Systematic review, 2013 to 2023 trials, at least 2 years.** Seven RCTs. "the majority of studies reported no significant difference between the two types of adhesives for the parameter of retention." Concern remained on margins: "There was some concern about their influence on marginal adaptation and marginal discoloration due to the conflicted results reported by the included trials." (Abdelkhalek et al., Syst Rev 2025, PMID:39838443) [SR]

**Trial-level numbers** (as tabulated in PMID:39838443, Table 2) [HC]

| Trial | Design, lesion | HEMA-free arm | HEMA-containing arm | Follow-up |
|---|---|---|---|---|
| Moretto et al. 2013 | RCT, 175 NCCLs | G-Bond, success 97.6% | Clearfil S3 Bond, success 92.6% | 3 years |
| Van Dijken 2013 (Class II) | Split-mouth, 115 Class II | G-Bond, success 91.5% | FL-Bond, success 82.3% | 6 years |
| Van Dijken 2013 (NCCL) | Split-mouth, 169 NCCLs | G-Bond AFR 1.6%; cfm (HEMA/TEGDMA-free) AFR 1.7% | XP Bond AFR 5.4% | 5 years |
| Van Landuyt et al. 2014 | RCT, 267 NCCLs | G-Bond, success 87.4% | OptiBond FL, success 90.9% | 5 years |
| Peumans et al. 2018 | RCT, 267 NCCLs | G-Bond, success 80.3%; retention 89.7% | OptiBond FL, success 79.5%; retention 89.7% | 9 years |
| Tekce et al. 2018 | Split-mouth, 160 Class I | G-aenial Bond, 100% | Clearfil S3 Bond, 100% | 2 years |
| Oliveira et al. 2023 | RCT, 60 NCCLs | Prime&Bond U | OptiBond All-in-One, Clearfil SE | 2 years |

**Main reasons for failure.** In the 9-year Peumans trial, "Nine HEMA-free (8.7%) and 7 restoration HEMA-containing (6.7%) failed as a result of severe generalized marginal discoloration." The review notes that the marginal defect rate was "7.9% for HEMA-free and 27.1% for HEMA-containing after 5-year follow-up" in one Van Dijken trial, and that three trials found HEMA-free systems "had significantly more marginal defects than HEMA-containing ones." (all from the full text of PMID:39838443) [SR] Secondary caries was rare in every arm.

**Patient and tooth factors.** Large and sclerotic lesions were a risk factor for retention loss in Van Landuyt et al. 2014. Smokers had more marginal discoloration in Moretto et al. 2013, and more so in the HEMA-containing group (p = 0.0229). (PMID:39838443 full text) [SR]

**Annual failure rate.** Only the Van Dijken NCCL trial reports AFR: 1.6% and 1.7% for the two HEMA-free adhesives, 5.4% for the HEMA-containing XP Bond over 5 years. (PMID:39838443, Table 2) [HC]

**Comparators.** The comparators are HEMA-free adhesives. Against them, HEMA-containing adhesives retain as well and show fewer enamel margin defects in some trials and more marginal discoloration in others. That is the whole of the clinical signal.

---

## 7. Adverse effects and safety

**Allergic contact dermatitis and sensitization** (suggested term: HP:0000964 Eczema, or MONDO:0005480 contact dermatitis) [SR, HC]

HEMA is the leading methacrylate allergen. It "was added to the European baseline series in 2019." Prevalence: "HEMA is an important cause of contact allergy/allergic contact dermatitis in North America and Europe with recent prevalences of >3% in the USA + Canada and 1.5%-3.7% in Europe. Currently, most cases are caused by nail cosmetics, both in consumers and professional nail stylists." (de Groot and Rustemeyer, Contact Dermatitis 2023, PMID:37752620)

Part 2 covers cross-reaction and atypical forms: "There is a strong cross-allergy between HEMA, ethylene glycol dimethacrylate (EGDMA), and hydroxypropyl methacrylate; many reactions to EGDMA are cross-reactions to primary HEMA sensitization. Rare atypical manifestations of HEMA-allergy include lichen planus, lymphomatoid papulosis, systemic contact dermatitis, leukoderma after positive patch tests, and systemic side effects such as nausea, diarrhoea, malaise, and palpitations. The occurrence of respiratory disease caused by methacrylates such as asthma is not infrequent. HEMA is the most frequently patch test-positive methacrylate." (PMID:37778325, 2024)

Oral lichenoid reaction is thus a documented rare form (suggested term: MONDO:0006564 oral lichen planus, as a lichenoid contact reaction).

**Occupational hazards** [HC]

- Southern Sweden, 1,632 patch-tested subjects: methacrylate positives in 2.3% of dental patients and 5.8% of dental personnel. "The most common allergen for both groups was 2-hydroxyethyl methacrylate (2-HEMA)." Testing HEMA alone would find 96.7% of allergic patients and 100% of allergic personnel. (Goon et al., Contact Dermatitis 2006, PMID:16958920)
- Finland, 1994 to 2006, 32 sensitized dental workers: "2-HEMA was the most important allergen in dentists and dental nurses, and MMA and EGDMA in dental technicians." (Aalto-Korte et al., Contact Dermatitis 2007, PMID:17937748)
- Germany IVDK, 226 dental technicians with occupational dermatitis: "Positive reactions were most frequently observed to methacrylates and/or acrylates (n = 67)." HEMA was the top allergen. (Heratizadeh et al., Contact Dermatitis 2018, PMID:29327359)
- Bishop and Roberts 2020 note that HEMA sensitivity has grown with the artificial-nail industry, that respiratory symptoms and asthma are increasingly reported, and that NIOSH regards gloves and other PPE as an inadequate primary defense against methacrylate penetration. (J Esthet Restor Dent 2020, PMID:32744420) [REV]

Geurtsen wrote in 2000 that "Each resin-based material releases several components into the oral environment," naming HEMA and TEGDMA, and noted "increasing numbers of dental nurses, technicians, and dentists" with allergic reactions. (Crit Rev Oral Biol Med 2000, PMID:11021634) [REV]

**Pulpal toxicity and inflammation** (suggested term: HP:0011122 or MONDO:0002238 pulpitis) [IV]

HEMA crosses dentin to the pulp chamber (PMID:8636483, PMID:26714346, PMID:23107279). In pulp cells it is cytotoxic in the millimolar range, induces IL-6 and IL-8 (PMID:21899564), dampens the LPS and LTA immune response (PMID:35341601), and cuts CXCL12 (PMID:30517439). No frequency of clinical pulpitis attributable to HEMA was found. The 2013 diffusion study judged eluted levels to be below cytotoxic thresholds (PMID:23107279).

**Genotoxicity** [IV]. Oxidative DNA base damage, apoptosis, and G0/G1 delay in lymphocytes at up to 10 mM, repaired within 120 minutes (PMID:20079459). Mechanism reviewed in PMID:16998124.

**Postoperative sensitivity** (HP:0000000 not applicable; suggest PATO or the OHD dentin sensitivity finding). Meta-analysis found no difference between HEMA-free and HEMA-containing: RD −0.00 [−0.02, 0.01], p = 0.72 (PMID:29649505) [SR]. In the 9-year trial both arms had 7.7% sensitivity (PMID:39838443) [HC].

**Secondary caries.** No difference: RD 0.00 [−0.01, 0.01], p = 0.92 (PMID:29649505) [SR].

**Mechanical failure.** Loss of retention and marginal breakdown at the adhesive interface. Rates are in §6. The mechanism proposed is water uptake and hydrolysis of the HEMA-rich hybrid layer (PMID:14653938, PMID:21594225).

**Esthetic problems.** Marginal discoloration is the most frequent finding in the long trials, in both arms (§6).

**Systemic toxicity.** Rare systemic contact dermatitis and symptoms after exposure are described in the allergy review (PMID:37778325). No BPA relevance. Not a mercury or metal ion source.

**Environmental release and disposal.** Not found for HEMA specifically this session.

**FDA MAUDE.** At least one adverse event report exists for 3M Scotchbond Universal Adhesive under product code KLE (https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/detail.cfm?mdrfoi__id=5104671&pc=KLE). I did not read the narrative. [DB]

---

## 8. Regulatory status (FDA first)

### 8a. Device-type classification

No FDA regulation names HEMA. The monomer reaches market inside products classed by their use. The primary regulation for its OHD category is the resin tooth bonding agent regulation.

**21 CFR 872.3200, "Resin tooth bonding agent"**
Source: https://www.law.cornell.edu/cfr/text/21/872.3200 [REG]

- (a) Identification, verbatim: "A resin tooth bonding agent is a device material, such as methylmethacrylate, intended to be painted on the interior of a prepared cavity of a tooth to improve retention of a restoration, such as a filling."
- (b) Classification, verbatim: "Class II."
- The Cornell page returned no special-controls guidance name and no 872.9 exemption statement in paragraph (b). Products under this regulation file 510(k)s (see 8b), and the product code record lists the submission type as 510(k).

**Product code under 872.3200**
Source: https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpcd/classification.cfm?start_search=1&regulationnumber=872.3200 [DB]

| Product code | Device name | Class | Submission type |
|---|---|---|---|
| KLE | "agent, tooth bonding, resin" | 2 | 510(k) |

**Permitted use** as stated in the identification: painting on the interior of a prepared cavity to improve retention of a restoration. The cleared indications of individual products are broader (see 8b).

**Restrictions.** Prescription-only status and labeling requirements were not read from the regulation text this session. No population-specific FDA recommendation exists for HEMA.

**Second regulation, for HEMA in resin-modified glass ionomer cements: 21 CFR 872.3275, "Dental cement"**
Source: https://www.law.cornell.edu/cfr/text/21/872.3275 [REG]

The Cornell fetch returned the identification paragraph for dental cement other than zinc oxide-eugenol as: "Dental cement other than zinc oxide-eugenol is a device composed of various materials other than zinc oxide-eugenol intended to serve as a temporary tooth filling or as a base cement to affix a temporary tooth filling, to affix dental devices such as crowns or bridges, or to be applied to a tooth to protect the tooth pulp." The classification returned for this paragraph was "Class II." The fetch summary merged the two subsections of this regulation. The paragraph numbering (a)(1), (a)(2), (b)(1), (b)(2) should be re-read from the source before it goes into the KB.

Product codes under 872.3275 (https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpcd/classification.cfm?start_search=1&regulationnumber=872.3275) [DB]:

| Product code | Device name | Class |
|---|---|---|
| EMA | "cement, dental" | 2 |
| MZW | "dental cement w/out zinc-oxide eugenol as an ulcer..." (truncated on the page) | 2 |
| EMB | "zinc oxide eugenol" | 1 |
| NEA | "cement, ear, nose and throat" | 2 |

RMGIC restoratives with HEMA would fall under EMA. I did not verify a specific RMGIC 510(k) this session.

**Other host regulations.** HEMA also appears in tooth shade resin materials (872.3690) and pit and fissure sealants (872.3765). I did not fetch those sections this session and do not report their text.

### 8b. Notable product-level decisions

**510(k) clearances** [DB]

| K number | Device name | Applicant | Decision | Date | Product code | Regulation | Source |
|---|---|---|---|---|---|---|---|
| K110302 | "ADHESIVE EXL-759" (marketed as Scotchbond Universal) | 3M Espe AG | "Substantially Equivalent (SESE)" | 05/19/2011 | KLE | 872.3200 | https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID=K110302 |
| K192961 | "ADH19" (marketed as Scotchbond Universal Plus) | 3M Deutschland GmbH | "Substantially Equivalent (SESE)" | 10/31/2019 | KLE | 872.3200 | https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID=K192961 |

K192961 indications for use, quoted from the 510(k) summary as mirrored at https://fda.innolitics.com/device/K192961: "A material primarily intended to be used as a bonding-promoting substance between tooth substance and dental restorations. It may also be used as a dentin sealant and as a bonding agent for repair of restorations." The mirror lists direct indications (bonding composite or compomer, root surface desensitization, fissure sealant bonding, cavity sealing before amalgam) and indirect ones (cementation of indirect restorations, core build-up bonding, veneer cementation, intraoral repair). Device description as mirrored: "ADH19 is a one-component dental adhesive used by dentists in clinical settings to bond restorative materials to tooth structure. It functions via self-etch, selective enamel etch, or total-etch modes." The FDA-hosted PDF at https://www.accessdata.fda.gov/cdrh_docs/pdf19/K192961.pdf did not parse in this session. The marketing name link between EXL-759/ADH19 and Scotchbond Universal comes from a web search result and the K192961 summary, not from the FDA record page itself.

The link between the Scotchbond products and HEMA: the SDS lists HEMA at 15 to 25% (§2).

**PMA or De Novo.** None found for this device type.

**Recalls under product code KLE** (https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfres/res.cfm?start_search=1&productcode=KLE) [DB]

| Product | Firm | Date | Class |
|---|---|---|---|
| 3M Unitek Transbond Plus Self-Etching Primer | 3M Unitek Corporation | 01/02/2025 | 2 |
| Peak Universal Bond Self-Etch Bottle Kit | Ultradent Products, Inc. | 07/12/2022 | 2 |
| Cosmedent's Etching Gel | Cosmedent, Inc. | 02/27/2018 | 2 |
| VOCO Futurabond M+ adhesive | Voco GmbH | 01/06/2017 | 2 |
| Henry Schein Natural Elegance SE Bond | Novocol, Inc. | 07/29/2014 | 2 |
| Darby Dental Supply Compolite Bond SE | Novocol, Inc. | 07/29/2014 | 2 |
| Peak SE Primer Kits | Ultradent Products, Inc. | 06/18/2012 | 2 |
| Bond-1 Primer/Adhesive | Kerr Corporation | 03/02/2012 | 3 |
| Bond-1 Primer/Adhesive | Sybron Dental Specialties | 03/16/2010 | 2 |
| Heraeus Kulzer GLUMA Comfort Bond + Desensitizer | Heraeus Kulzer Inc. | 10/02/2007 | 3 |

The page showed ten records. Reasons for recall were not read. None is known to be HEMA-specific. The Gluma product is a HEMA-based desensitizing bond.

**Safety communications.** None found for HEMA or for resin bonding agents.

### 8c. Other jurisdictions

- **EU MDR (2017/745).** Annex VIII Rule 8 places implantable and long-term surgically invasive devices in Class IIb, with an exception for devices "intended to be placed in the teeth," which are Class IIa. I did not read that text on EUR-Lex; the fetch returned the articles without the annexes. Secondary sources reporting the rule: MedDeviceGuide (https://meddeviceguide.com/blog/eu-mdr-classification-rules-annex-viii-guide) and BSI slides (https://compliancenavigator.bsigroup.com/globalassets/mdr-presentation-slides-29-40.pdf). Mohn and Zehnder 2023 write that "Dental fillings, an implantable device as defined within the regulation, is Class IIa, whereas dental implants and their abutments are Class IIb." (Front Dent Med 2023, https://www.frontiersin.org/journals/dental-medicine/articles/10.3389/fdmed.2023.1155820/full) Class IIa requires a notified body. Harmonized standards relevant: EN ISO 4049, EN ISO 7405, EN ISO 10993-1 (not verified against the OJEU list this session).
- **Health Canada.** The Health Canada classification page states: "Class III devices such as tooth bonding resins and hip prostheses, and Class IV devices..." require a medical device licence application. (https://www.canada.ca/en/health-canada/services/drugs-health-products/classification-health-products-device-drug-interface.html) [REG] A specific MDALL licence for a HEMA adhesive was not found.
- **TGA (Australia).** ARTG entry not found.
- **MHRA, PMDA, NMPA, ANVISA.** Not searched.

---

## 9. Standards and specifications

**FDA-recognized consensus standards listed for product code KLE**
Source: https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfStandards/results.cfm?start_search=1&productcode=KLE [DB]

| Recognition number | Standard | Title as listed |
|---|---|---|
| 4-219 | ISO 29022 (2013-06-01) | "Dentistry - Adhesive - Notched-edge sheer bond strength test" |
| 4-261 | ISO 7405 (2018-10, corrected 2018-12) | "Dentistry - Evaluation of biocompatibility of medical devices used in dentistry" |
| 4-324 | ISO TS 16506 (2017-07, corrected 2018-03) | "Dentistry - Polymer-based luting materials containing adhesive components" |
| 4-348 | ISO 9917-1 (2025-05) | "Dentistry - Water-based cements - Part 1: Acid-base cements" |
| 4-364 | ISO 3990 (2023-07) | "Dentistry - Evaluation of antibacterial activity of dental restorative materials, luting materials, fissure sealants and orthodontic bonding or luting materials" |

("sheer" is the spelling on the FDA page.)

**Other ISO standards used in the HEMA literature** [STD]

- ISO/TS 11405:2015, Dentistry, Testing of adhesion to tooth structure. Gives guidance on substrate selection, storage, handling, tensile bond strength, marginal gap, microleakage, and clinical usage tests. Catalog entry https://www.iso.org/standard/62898.html (iso.org refused the fetch; title and scope from the ANSI webstore mirror https://webstore.ansi.org/standards/iso/isots114052015).
- ISO 4049:2019, Dentistry, Polymer-based restorative materials. Water sorption and solubility of HEMA adhesives are measured by this method in PMID:29574280 and PMID:29270433. Catalog https://www.iso.org/standard/67596.html (title from https://webstore.ansi.org/standards/iso/iso40492019). The standard states it does not cover luting materials with an adhesive component.
- ISO 9917-2, Dentistry, Water-based cements, Part 2: Resin-modified cements. Applies to RMGIC hosts. Not fetched this session.
- ISO 10993-1, biological evaluation of medical devices. General; not fetched.

**ANSI/ADA specifications.** Not verified this session.

---

## 10. Commercial products

**HEMA-containing adhesives and primers** (HEMA status from the trials and SDS cited)

| Product | Manufacturer | Notes | FDA record |
|---|---|---|---|
| Scotchbond Universal | 3M / Solventum | HEMA 15 to 25% per SDS | K110302 |
| Scotchbond Universal Plus | 3M / Solventum | | K192961 |
| Clearfil SE Bond | Kuraray Noritake | Two-step self-etch; HEMA and 10-MDP; used as the gold standard comparator (PMID:39838443, PMID:36837160) | not looked up |
| Clearfil S3 Bond, Clearfil Universal Bond Quick | Kuraray Noritake | HEMA-rich one-step; the Quick version adds a methacrylamide (PMID:34269543) | not looked up |
| OptiBond FL | Kerr | Three-step etch-and-rinse; HEMA-containing comparator in the 9-year Peumans trial | not looked up |
| Adper Single Bond / Single Bond 2 | 3M | HEMA-containing etch-and-rinse; used in pulp-cell studies (PMID:30517439) | not looked up |
| XP Bond | Dentsply | HEMA-containing two-step etch-and-rinse (Van Dijken trial) | not looked up |
| Adhese Universal | Ivoclar | HEMA-containing universal (PMID:38308570) | not looked up |

**HEMA-containing cements and desensitizers**

| Product | Manufacturer | Notes |
|---|---|---|
| GC Fuji II LC (Improved) | GC | RMGIC; liquid HEMA 25 to 50% per SDS |
| Vitremer | 3M | RMGIC; highest HEMA release of three tested (PMID:19826597) |
| Gluma Desensitizer | Kulzer | 5% glutaraldehyde, 35% HEMA (PMID:34013195); KLE recall record for "GLUMA Comfort Bond + Desensitizer" 2007 |
| RelyX ARC, Panavia F 2.0, Multilink Automix | 3M, Kuraray, Ivoclar | Resin cements releasing HEMA through dentin (PMID:26714346) |

**HEMA-free comparators used in the literature**

| Product | Manufacturer | Source |
|---|---|---|
| G-Bond, G-aenial Bond, G-Premio Bond, G2-Bond Universal | GC | PMID:39838443, PMID:36837160, PMID:38308570 |
| Prime&Bond Universal, Prime&Bond active, Prime&Bond U, Prime&Bond Elect | Dentsply Sirona | PMID:34269543, PMID:38308570, PMID:29211130 |
| BeautiBond Universal | Shofu | PMID:34269543 |
| Gluma Bond Universal | Kulzer | HEMA-free universal (PMID:38600935) |
| All-Bond 3 | Bisco | PMID:29211130 |
| cfm | Saremco | HEMA/TEGDMA-free etch-and-rinse (Van Dijken trial) |

---

## 11. History and trends

HEMA entered dentin bonding in the early 1980s. Asmussen and Munksgaard screened aldehydes and monomers in water: "Among the monomers investigated HEMA (hydroxyethyl-methacrylate) gave rise to the bond of highest strength." (Int Dent J 1985, PMID:3926655) Their 1984 paper found bond strength "highly dependent on the HEMA concentration, with a maximum at 35%" (J Dent Res 1984, PMID:6430986). That mixture became Gluma. In the same years Nakabayashi described the hybrid layer with 4-META, and the idea of hydrophilic monomers infiltrating etched dentin took hold (J Biomed Mater Res 1982, PMID:7085687).

By the 1990s HEMA was in nearly every adhesive. Chemical surveys confirmed it as the most common monomer in bonding agents (PMID:15186380). The 2000s brought the hydrophilicity critique (PMID:14653938), the phase-separation finding that explained why one-step adhesives needed HEMA (PMID:15668338), and the concentration study that set the useful dose near 10% (PMID:18433860).

The allergy record grew in parallel. HEMA became the top dental methacrylate allergen in Sweden, Finland, and Germany (PMID:16958920, PMID:17937748, PMID:29327359). It joined the European baseline patch series in 2019 (PMID:37752620).

The current direction is away from HEMA where possible. HEMA-free adhesives arrived with G-Bond and spread; Ikemura et al. described "a new single-bottle, self-etching, 2-hydroxyethyl methacrylate (HEMA)-free adhesive" in a 2011 review (PMID:22123001). Replacements under study are glycerol dimethacrylate (PMID:29574280), methacrylamides that resist hydrolysis (PMID:32536589, PMID:34269543), and alternate monomers in RMGIC (PMID:34462139). The 2025 review's opening sentence states the state of the field: "Hydrophilic monomer 2-hydroxyethyl methacrylate (HEMA)-free adhesive systems are gaining increasing popularity nowadays." (PMID:39838443)

The clinical data do not yet reward the move. Retention is equal. Margins differ trial by trial. HEMA stays in the bottle because it is cheap, it works, and nothing has replaced it in full.

---

## Gaps and lookups that failed

- OHD parent and sibling links for OHD:0001082 were not read. The OAK command was blocked.
- MeSH: no standalone HEMA record confirmed. SNOMED CT not searched.
- 21 CFR 872.3275 paragraph numbering needs a direct re-read; the fetch merged subsections.
- 21 CFR 872.3690 and 872.3765 not fetched.
- EU MDR Annex VIII text not read from EUR-Lex.
- ISO catalog pages refused fetches; ISO 9917-2 and ISO 10993-1 not verified.
- TGA, MHRA, PMDA, NMPA, ANVISA: not found or not searched.
- Manufacturer SDS values for HEMA content came from search summaries. The PDFs were not opened.
- Abstracts for PMID:27367737, PMID:11021634, PMID:18539324, PMID:16998124, PMID:15668338, PMID:8636483, PMID:26916063, PMID:19826597, PMID:34462139, PMID:14653938, PMID:22123001, PMID:32744420, PMID:17937748, PMID:16958920, PMID:29327359, and PMID:15186380 were returned partly summarized. Only the fragments shown in quotation marks above were returned as verbatim. Run `just fetch-reference` on each before curation to get the full abstracts for snippet checking.

## Reference Validation

Checked with `linkml-reference-validator` 0.2.1.

| Outcome | Count |
| --- | --- |
| References checked | 49 |
| Resolved | 49 |
| Unresolved (possible confabulation) | 0 |
| Unverifiable | 0 |
| Quoted claims checked | 32 |
| Quoted claims found in source | 29 |
| Quoted claims **not** found in source | 3 |
| References weighed for topical relevance | 49 |
| On topic | 33 |
| Off topic | 0 |

### Quotes not found in the cited source

Searched the abstract, any retrieved full text, and the title. A quote drawn from a part of the paper that was not retrieved will appear here too, so check before treating one as invented:

Every one of these was searched against an abstract alone, with no full text retrieved - marked *abstract only* below. Where full text can be fetched, re-running with it will settle them; where the source publishes only a summary to PubMed, as GeneReviews chapters do, it will not, and the quote has to be checked by hand against the chapter itself.

- `PMID:15186380` *(abstract only)*: "The most frequently occurring methacrylates in the bonding materials were 2-hydroxyethyl methacrylate (2-HEMA) and bis-GMA."
  - closest text in source: "The most frequently occurring methacrylates in the bonding materials were 2-hydroxyethyl methacrylate (2-HEMA) and 2,2-bis-[4-(2-hydroxy-3-methacryloxypropoxy)phenyl]-propane (bis-GMA)"
- `PMID:26916063` *(abstract only)*: "The setting of resin-modified glass ionome cements (RMGIC) involves the acid-base reaction and the polymerization of HEMA monomers."
  - closest text in source: "OBJECTIVE: The setting of resin-modified glass ionomer cements (RMGIC) involves the acid-base reaction and the polymerization of HEMA monomers"
- `DOI:10.3389/fdmed.2023.1155820` *(abstract only)*: "Dental fillings, an implantable device as defined within the regulation, is Class IIa, whereas dental implants and their abutments are Class IIb."
  - closest text in source: "This regulation is termed EU 2017/745 or Medical Device Regulation (MDR)"