# Deep research: Ceramic (OHD:0000135)

- **Material name:** Ceramic
- **OHD term:** OHD:0000135 (ceramic dental restoration material)
- **Category:** CERAMIC
- **OHD definition:** A dental restoration material that has a nonmetallic inorganic structure consisting primarily of compounds containing oxygen combined with one or more metallic or semi-metallic elements that are processed at high temperatures, pressed, and polished or milled.
- **Provider:** `claude_code`
- **Date:** 2026-09-27

## How this report was produced, and what that means for its authority

`just research-material claude_code Ceramic` cannot run in the CI runner. The
`deep-research-client` shim spawns the Claude Code CLI as a subprocess that inherits no
credentials, and every keyed provider is set-but-empty (`ANTHROPIC_API_KEY`,
`OPENAI_API_KEY`, `EDISON_API_KEY`, `FUTUREHOUSE_API_KEY` all length 0):

```
WARNING - agentapi not found in PATH
ERROR - claude_code: success Not logged in - Please run /login -- the API key is missing,
invalid, or lacks access to this endpoint.
```

This is the same blocker recorded on #4, #5 and the `curate/metal` branch since 2026-09-06.
Because the curating agent for this run *is* Claude Code, the research pass was run directly
instead of through the shim, exactly as `research/Metal-deep-research-claude_code.md` did.

Two differences from the Metal run are worth stating. First, PubMed's `esearch.fcgi` was
returning HTTP 500 for every query during this run, so **discovery** was done through the
Europe PMC REST API instead; every reference found that way was then **fetched and cached
through `just fetch-reference`** (which uses PubMed directly and worked normally), so all
quotes below are checkable against `references_cache/`. Second, FDA device-type discovery
used the openFDA API to *find* candidate regulations and product codes, and then every one
was re-read from the primary sources named in the skill (eCFR renderer API and the
accessdata classification / standards / 510(k) pages). openFDA was a search index here, not
a citation.

**This is a research artifact. Nothing here is authoritative for the knowledge base.** Every
regulation number, class, product code and snippet was re-read from its primary source
before entering `kb/materials/Ceramic.yaml`. Treat every claim below as a lead.

## Scope decision

OHD:0000135 is a class with 20 descendants, so this report stays at the level of *ceramic as
a restorative device type*. Where the only available numbers are subtype-specific, they are
reported as bounds on the class **with the subtype named**, which is what issue #6 asked
for ("as ranges spanning the class, with the span attributed"). Anything that is only true
of one zirconia grade or one glass-ceramic belongs in the child entries.

One correction to the issue's framing: the issue states that all 20 descendants are `STUB`.
`Zirconia_Polycrystalline_Ceramic.yaml` (OHD:0001034) is already `IN_PROGRESS` on `main`.
That does not change the choice of material, but it does mean one child already exists to be
consistent with — see the regulatory note below, where it is **inconsistent** with what this
run verified.

---

## 1. Identity and nomenclature

The three-family split that organises OHD's ceramic subtree is Gracis et al. 2015
(PMID:25965634), and the abstract states the classification criterion explicitly:

> This new classification system categorizes ceramic restorative materials into three
> families: (1) glass-matrix ceramics, (2) polycrystalline ceramics, and (3) resin-matrix
> ceramics.

> an all-ceramic material is classified according to whether a glass-matrix phase is present
> (glass-matrix ceramics) or absent (polycrystalline ceramics) or whether the material
> contains an organic matrix highly filled with ceramic particles (resin-matrix ceramics)

This maps one-to-one onto `Glass_Matrix_Ceramic`, `Polycrystalline_Ceramic` and
`Resin_Matrix_Ceramic`, the three children already linked in the KB.

The contemporary subfamily inventory is in Wang et al. 2026 (PMID:41990584), a **narrative**
review (recorded as `OTHER`, not `SYSTEMATIC_REVIEW`):

> The main classifications of chairside CAD/CAM materials include feldspathic ceramics,
> leucite-reinforced ceramics, lithium disilicate ceramics, zirconia-reinforced lithium
> silicates, resin nanoceramics, polymer-infiltrated ceramic-network and zirconia.

**Vocabulary mappings.** NCIT has no dental-ceramic material concept: `l~ceramic` returns
only ceramide chemistry and `Respirable Ceramic Fiber`, and `l~porcelain` returns
`NCIT:C52584 Porcelain Veneer` (a restoration, not a material) and `NCIT:C165377 Porcelaine`.
The nearest honest mapping is `NCIT:C42634 Dental Material` as a `BROAD_MATCH`. MeSH has
*Dental Porcelain*, but MeSH is not in `conf/oak_config.yaml`, so it is not recorded.

## 2. Composition

The FDA device-type identification (see §5) names the traditional constituents, and all
three have ChEBI terms: kaolin `CHEBI:140503`, feldspar `CHEBI:48733`, quartz `CHEBI:46727`.
Note FDA spells feldspar "felspar"; the quote is reproduced verbatim.

For the modern crystalline phases, PMID:12901984 names them alongside their toughness:

> The third group KIc values were 2.8 MPa m(1/2) for a lithium disilicate glass-ceramic,
> 3.1 MPa m(1/2) for a glass-infused alumina, and 4.9 MPa m(1/2) for zirconia.

giving aluminium oxide `CHEBI:30187` and zirconium dioxide `CHEBI:747200`. Yttria is the
stabiliser that indexes the zirconia grades (PMID:40738693, PMID:38443872) but **has no
ChEBI term** (`l~yttrium oxide` returns nothing), so that row carries no `term`. Same for
leucite and lithium disilicate.

## 3. Setting and handling

Three routes are evidenced at class level: **sintering/firing** (the regulation's own
"heating the powder mixture to a high temperature in an oven"; PMID:41990584 on "rapid
sintering techniques"), **heat pressing** (PMID:25489158 on "pressable all ceramic core
materials"), and **milling** (PMID:41990584, chairside CAD/CAM). Additive manufacturing of
dental ceramics exists but no cached abstract in this corpus supports it, so it is not
recorded.

## 4. Properties

| Property | Value | Source |
|---|---|---|
| Flexural strength, leucite-based pressable glass-ceramic | 124.89-163.95 MPa biaxial | PMID:25489158 |
| Flexural strength, translucent zirconia | 4Y-PSZ 803 ± 233 MPa; 5Y-PSZ 570 ± 116 MPa | PMID:40738693 |
| Fracture toughness across the class | <2 (micaceous glass-ceramic, feldspathic porcelain) to 4.9 MPa·m^1/2 (zirconia) | PMID:12901984 |
| Fracture toughness, leucite-based pressable | 1.063-1.225 | PMID:25489158 |
| Translucency | glass-ceramics still exceed even high-yttria zirconia | PMID:33581910 |
| Translucency drivers | yttria content, additives, microstructure, thickness, sintering | PMID:38443872 |
| Translucency after hydrothermal aging | changes mostly within acceptability thresholds | PMID:32275345 |
| Chemical solubility | ISO 6872:2015 method is geometry-sensitive and manipulable | PMID:31759562 |
| Thermal expansion | zirconia 10.80; veneering ceramics 7.83-12.95 ×10⁻⁶/°C | PMID:29721230 |
| Biocompatibility / biofilm | glazed zirconia: lower fibroblast viability, higher *S. mutans* adhesion | PMID:40551320 |

Two cautions carried into the entry. PMID:25489158's abstract gives fracture toughness in
"MPa" where the quantity is MPa·m^1/2; the entry quotes it verbatim and records the unit
discrepancy rather than silently correcting the source. And the 124.89-163.95 MPa span is
the low end of the *class*, not of glass-matrix ceramics generally — it is three leucite
core materials in one in-vitro study.

## 5. Regulatory (leads only — all re-verified before entry)

The issue's suspicion was right that `872.3920 Porcelain tooth` is not the material-level
device type, and the regulation says why in its own text: a porcelain tooth is *"a
prefabricated device made of porcelain powder for clinical use (§ 872.6660)"*. So the
material-level device type is **872.6660 Porcelain powder for clinical use**, Class II,
product code **EIH**, and 872.3920 sits downstream of it.

That is not merely a textual inference. openFDA's 510(k) index shows EIH is what modern
dental ceramics actually clear under — zirconia blanks (KATANA, Upcera, Zirkonzahn, Vatech,
Dental Direkt), lithium disilicate and glass-ceramics (IPS e.max CAD/ZirCAD, IPS e.max One,
Straumann n!ce), across four decades of clearances.

Neighbouring device types deliberately **not** recorded as the material's own status:
`872.3630` endosseous dental implant abutment (NHA) is where ceramic abutments clear, but
its identification names no material; `872.3661` (NOF) is the CAD/CAM system, not the
ceramic.

> ⚠️ **Inconsistency with an existing child entry.** `Zirconia_Polycrystalline_Ceramic.yaml`
> records `status: UNKNOWN` with a note saying zirconia CAD/CAM blanks are "typically cleared
> by 510(k) under 872.3690 (tooth shade resin material, product code EBF)". This run's
> verification contradicts that: zirconia blanks clear under **EIH / 872.6660**, and that
> entry's own note admits the records "have not yet been verified". Fixing the child is out
> of scope for this one-item run and is flagged for a later one.

## 6. Clinical performance

Class-level survival evidence is unusually good for this material, because the Sailer /
Pjetursson series reports by ceramic family:

- **Single crowns, 5 y (PMID:41489982, 64 studies, 8,051 all-ceramic SCs):** 98.5% monolithic
  lithium-disilicate, 97.3% veneered densely-sintered zirconia, 97.1% metal-ceramic, 96.8%
  monolithic densely-sintered zirconia, 95.7% veneered leucite/lithium-disilicate, 94.5%
  densely-sintered alumina, 94.3% glass-infiltrated alumina, 90.4% feldspathic/silica-based.
- **Single crowns, 5 y, earlier round (PMID:25842099):** metal-ceramic 94.7%; feldspathic
  significantly lower; "Zirconia-based SCs should not be considered as primary option due to
  their high incidence of technical problems" — a verdict the 2026 review supersedes for
  monolithic designs, which is itself worth recording as the direction of travel.
- **Implant-supported SCs, 5 y (PMID:30328190):** zirconia 97.6% vs metal-ceramic 98.3%.
- **Inlays/onlays/overlays (PMID:27287305):** 92-95% at 5 y, 91% at 10 y.
- **Laminate veneers at 10.4 y (PMID:39523553):** feldspathic 96.13%, LRGC 93.70%, LDS 96.81%.
- **Partial coverage restorations (PMID:40245384):** LDS 93.7%, resin-matrix ceramic 89.3%.
- **Zirconia FDPs at 10 y (PMID:29520468):** 95.0% survival but only 78.8% chipping-free.
- **Monolithic zirconia crowns at 3 y (PMID:36104182):** 89.8%.

## 7. Adverse effects

Fracture and chipping dominate: PMID:27287305 ("fractures were the most frequent cause of
failure"), PMID:25842099 (veneering fracture and loss of retention vs metal-ceramic),
PMID:41489982 (monolithic designs reduce both), PMID:29520468 (21% chipped by 10 years).
Antagonist enamel wear is real but not ceramic-specific — PMID:38925985 finds wear against
*all* antagonists including natural enamel, with metal-ceramic worst. Low-temperature
degradation (PMID:38281620) and hydrothermal translucency loss (PMID:32275345) are
zirconia-specific ageing mechanisms recorded with that attribution. PMID:29520468 also found
periodontal tissues adjacent to abutments "inferior to the ones of control teeth".

**Not found:** no cached source in this corpus documents ceramic hypersensitivity or allergy
in the sense the issue's scope line allowed for ("hypersensitivity where documented"). It is
therefore not recorded. `40551320` is in-vitro fibroblast viability and biofilm, which is a
biocompatibility property, not a clinical adverse effect.

## 8. Standards

All six re-read from their own FDA recognition detail pages (not from the per-product-code
query, which would imply completeness):

| Standard | Recognition | id |
|---|---|---|
| ISO 6872 Fifth edition 2024-08, Dentistry - Ceramic materials | 4-329 | 45644 |
| ISO 18675 First edition 2022-05, Dentistry - Machinable ceramic blanks | 4-322 | 45030 |
| ISO 9693 Third edition 2019-10, Compatibility testing for metal-ceramic and ceramic-ceramic systems | 4-263 | 41090 |
| ISO 7405 Third edition 2018-10, Evaluation of biocompatibility | 4-261 | 40211 |
| ANSI/ADA No. 131-2015 (R2020), Dental CAD/CAM Machinable Zirconia Blanks | 4-255 | 38749 |
| ANSI/ADA No. 187-2024, Dentistry - Dental CAD/CAM Machinable Ceramic Blanks | 4-345 | 46037 |

The 45644 page carries a transition notice worth recording: recognition of ISO 6872 Fourth
edition [4-251] "will be superseded by" the Fifth edition [4-329], with conformity
declarations to 4-251 accepted "until December 20, 2026".

## 9. Products

Three EIH clearances verified in the 510(k) database: **IPS e.max CAD / IPS e.max ZirCAD**
(K051705, Ivoclar Vivadent Inc., SE 2005-10-14), **KATANA Zirconia** (K131534, Kuraray
Noritake Dental Inc., SE 2013-10-11), **IPS e.max One** (K211916, Ivoclar Vivadent AG, SE
2021-08-20). Only K211916 filed a Summary; the other two filed a Statement, so no
indications-for-use text is available from the database for them and none is invented.

## 10. References considered and not used

- PMID:29395472 (strength and fracture toughness of zirconia dental ceramics) — an R-curve
  fracture-mechanics analysis of 3Y-TZP vs 12Ce-TZP. Sound, but too far below class level.
- PMID:39947786 — a J Evid Based Dent Pract critical summary *of* PMID:38925985. Citing both
  would double-count one study.

Neither is cached, so `references_cache/` contains only what the entry cites.
