# Deep research: Metal (OHD:0000048)

- **Material name:** Metal
- **OHD term:** OHD:0000048 (metal dental restoration material)
- **Category:** METAL
- **OHD definition:** A dental restoration material that consists mostly of metal and metal alloys.
- **Provider:** `claude_code`
- **Date:** 2026-09-14

## How this report was produced, and what that means for its authority

`just research-material claude_code Metal` cannot run in the CI runner. The
`deep-research-client` shim spawns the Claude Code CLI as a subprocess that inherits no
credentials, and every keyed provider is set-but-empty:

```
WARNING - agentapi not found in PATH
ERROR - claude_code: success Not logged in - Please run /login -- the API key is missing,
invalid, or lacks access to this endpoint.
```

This has blocked the whole curation queue since 2026-09-06 and is recorded on #4 and #5.
Because the curating agent for this run *is* Claude Code, the research pass was run
directly instead of through the shim: PubMed was searched through the E-utilities API and
every abstract quoted below was cached through `just fetch-reference`, so the quotes are
checkable against `references_cache/` rather than against a model's recollection.

**Two honest limits on this report.** It is narrower than a full agentic deep-research run
would be: it is a targeted sweep aimed at the template's sections and at finding gaps in an
entry that was already substantially complete, not an exhaustive survey. And it is a
*research* artifact — nothing here is authoritative for the knowledge base. Under the
scanner rules every regulation number, class, product code and snippet must be re-read from
its primary source before it enters `kb/materials/Metal.yaml`. Treat every claim below as a
lead.

## Standing on the existing entry

`kb/materials/Metal.yaml` was already at `IN_PROGRESS` when this report was written, with 11
composition rows, 8 clinical uses, 3 properties, 8 clinical-performance rows, 5 adverse
effects, 5 regulatory device types and 5 standards, across 64 evidence rows. This report
therefore concentrates on (a) confirming the shape of what is there and (b) the sections
where something class-level is missing. Section 12 lists what actually changed as a result.

---

### 1. Identity and nomenclature

The class is the metallic branch of the restorative-material taxonomy, defined by the
metallic bond rather than by any shared formulation. Its practical division is the FDA's and
the ADA's: **noble** (gold-based and other noble), **predominantly base metal**
(nickel-chromium, cobalt-chromium, titanium), and **amalgam**, with **gold foil** and
**preformed stainless steel** as direct-placement outliers. That three-way split is the same
one the regulations use, which is why the class maps to several device types rather than one
(section 8).

The entry records `MESH:D003722` (Dental Alloys) as a `CLOSE_MATCH`, correctly close rather
than exact: the MeSH heading is about *alloys*, and the OHD class also admits commercially
pure metals — gold foil and cp-titanium are not alloys. No exact-match term was found in
NCIT or SNOMED for "metal dental restoration material" at this level of abstraction. Leaving
`mappings` at one defensible row is the right call; a forced `EXACT_MATCH` here would be
wrong.

Children in OHD: Amalgam (OHD:0000001), Gold foil (OHD:0000034), Noble metal (OHD:0000146),
Predominantly base metal (OHD:0000156), Stainless steel (OHD:0000137), Titanium
(OHD:0000136).

### 2. Composition

No class-level formulation exists and none should be asserted. What generalises is the
recurring **alloying-element set**: gold, palladium, platinum, silver, nickel, chromium,
cobalt, titanium, tin, copper, mercury. The entry records exactly these eleven with
`role: ALLOYING_ELEMENT` and ChEBI terms, each supported by a regulation or abstract that
names the element rather than by a textbook generalisation. That is the correct treatment
for an abstract parent and no change is proposed.

The element list is corroborated from the allergy literature, which enumerates the offending
metals across all families — a useful cross-check because it is derived from patients rather
than from formulations (PMID:42106203, quoted in the entry).

For the amalgam branch specifically, the IADR position statement gives a compact composition
(PMID:42200317):

> "Composed of approximately 50% elemental mercury alloyed with silver, tin, copper, and other metals"

This belongs on the **Amalgam** child, not here.

### 3. Setting and handling

The class is defined at this level by **fabrication route**, not by a setting reaction, and
the entry's five `setting_mechanisms` (casting, milling, additive manufacturing,
amalgamation, cold working) cover the routes the families actually use. Amalgamation is the
only chemical reaction among them; the rest are metallurgical or subtractive/additive
shaping.

Additive manufacturing is the live area. A 2026 systematic review of selective laser melting
(PMID:41206334) finds fit is governed by process parameters rather than by the alloy:

> "Key factors influencing the fit of SLM-fabricated FDPs included tooth finish line and preparation design, printing orientation, and printing parameters such as lamination layer thickness and laser settings."

> "Within the limitations of current evidence, clinically acceptable fit was associated with cobalt chromium alloys printed at 0 or 30 degrees with a 25- to 50-µm layer thickness and optimized laser parameters."

These are cobalt-chromium numbers and belong on that child. They do, however, independently
support the class-level property the entry already records — that a mechanical or fit value
for a metal is only meaningful with its fabrication route attached (PMID:39741083).

### 4. Properties

The entry records only three properties and that restraint is correct. Strength, hardness,
modulus and wear span more than an order of magnitude across the families; asserting a
class-level number would be false. The three that survive are corrosion in the oral
environment, plastic deformation rather than brittle fracture, and the dependence of
mechanical properties on fabrication route.

Searches for two further candidates that looked class-level did **not** produce a usable
class-level source:

- **Thermal conductivity.** Metals conduct heat, and this is textbook, but the retrieved
  literature is material-specific (amalgam and composite cores, liners) rather than a claim
  about metallic restoratives as a group. No snippet was found that could be quoted at class
  level without overreaching. Not added.
- **Radiopacity.** Same outcome. The radiopacity literature is dominated by composites and
  ceramics, where radiopacity is a formulation variable worth measuring; for metals it is so
  obvious that nobody states it as a finding. Not added.

Both are recorded here as searched-and-not-found so a later curator does not repeat the
search.

### 5. Clinical uses

The entry's eight uses span direct filling, cast and porcelain-fused-to-metal crown and
bridge, inlays, onlays, implant-supported single crowns, fixed dental prostheses, removable
frameworks, and preformed crowns, each with an OHD procedure term. This matches the range of
uses the five regulations permit. No gap found.

The comparative context for the direct-filling use is a 2026 Cochrane overview of systematic
reviews (PMID:42444634), which is the current best summary of amalgam against its
mercury-free alternatives:

> "One Cochrane review reported low-certainty evidence that the risk of restoration failure may be 7% less with dental amalgam than RBC"

with the caveat the same review attaches:

> "Studies in this review began recruitment in the late 1990s, which may affect the generalisability of this evidence to contemporary practice"

This is an Amalgam-child claim, not a class claim — it says nothing about noble or base metal
restorations — and is left there.

### 6. Clinical performance and longevity

The entry carries eight pooled figures drawn from systematic reviews of metal-ceramic
tooth-supported and implant-supported prostheses plus cast gold partial crowns. A useful
comparator not currently cited is the ceramic-versus-metal-ceramic implant meta-analysis
(PMID:30661882), which bears on whether the class is being displaced. It is a reasonable
future addition but is a *comparison* rather than a property of the class, and the entry
already records the metal-ceramic arm's own survival figures, so it was not added in this
pass.

### 7. Adverse effects

The entry's five effects — dental metal allergy, nickel contact allergy, oral lichenoid
contact lesions, element release through corrosion, galvanic current between dissimilar
restorations — are the ones that genuinely generalise, and each carries a MONDO or HP term.

**This section is where the research pass found a real gap.** Metallic restorations degrade
cone-beam CT imaging, which is a consequence of being metallic, applies to every family, and
is a recognised diagnostic problem rather than a nuisance. A 2026 systematic review states it
as its opening premise (PMID:42203681):

> "The presence of metallic restorations introduces severe artifacts that compromise diagnostic accuracy of cone beam computed tomography (CBCT) images."

And a 2026 in vitro comparison across four CBCT systems shows the severity is family-
dependent in the same way corrosion is (PMID:42267249):

> "Amalgam produced the most severe artifacts, reflected by the lowest MGVs, while cobalt-chromium yielded the highest variability (SD) (p < 0.005)."

> "Detector type, metal composition, and the number and position of metallic objects within the FOV significantly influence artifact formation in CBCT images."

This has the same shape as the entry's other class-level rows: true of the class, graded
across the families, with the per-family numbers belonging to the children. **Added to the
entry in this run** under `effect_category: OTHER` — the enum has no imaging or diagnostic
category, and none of ALLERGIC_OR_HYPERSENSITIVITY, TOXICITY, MECHANICAL_FAILURE,
ANTAGONIST_WEAR or ESTHETIC fits. No `effect_term`, because the effect is a property of the
radiograph and not a phenotype of the patient, so neither MONDO nor HP has anything honest to
offer.

Two other template categories were considered and rejected:

- **ANTAGONIST_WEAR.** Genuinely a metal concern, but it splits rather than generalises —
  gold is famously kind to opposing enamel while base metals are not — and the retrieved
  sources compare specific alloys against zirconia rather than establishing anything about
  the class. Belongs on the children.
- **ENVIRONMENTAL.** The mercury life-cycle and Minamata phase-down material
  (PMID:42200317, PMID:42444634) is entirely amalgam-specific. Recording it on the parent
  would attribute a mercury problem to gold foil and titanium. Belongs on **Amalgam**.

### 8. Regulatory status

The class maps to **no single regulation**, which is the most important structural fact about
it. Five device types under 21 CFR 872 are in scope, and the entry records all five
separately with a note on each saying which child it covers:

| Regulation | Device type | Class | Product codes | Pathway |
|---|---|---|---|---|
| 872.3060 | Noble metal alloy | II, special controls | EJS, EJT | 510(k)-exempt subject to 872.9 |
| 872.3070 | Dental amalgam, mercury, and amalgam alloy | II, special controls | EJJ, ELY, OIV | 510(k) — **not** exempt |
| 872.3330 | Preformed crown | I | ELZ | 510(k)-exempt subject to 872.9 |
| 872.3350 | Gold or stainless steel cusp | I | ELO | 510(k)-exempt subject to 872.9 |
| 872.3710 | Base metal alloy | II, special controls | EJH | 510(k)-exempt subject to 872.9 |

**872.3070 is the counterexample worth keeping.** It carries the same class and the same
special-controls pattern as 872.3060 and 872.3710, but its classification paragraph grants no
exemption. That asymmetry is written up in `docs/regulatory.md` under "A note on `872.9`
exemptions".

`872.3060` also returns product code `EIT` (rapid wax applicator). It is excluded as a
laboratory accessory rather than a restorative material, and the exclusion is stated in both
the entry's `notes` and `docs/regulatory.md`.

**This report did not re-verify any of the above and must not be used as the source for it.**
All five regulations, all eight product codes and all five identification paragraphs were
verified against the CFR text at law.cornell.edu and the openFDA classification endpoint
during earlier scanner runs on this branch, and the snippets in the entry are verbatim from
those sources. A reviewer should check the entry against the CFR and the FDA database, not
against this table.

**8c. Other jurisdictions.** Not researched. No EU MDR class, Health Canada, MHRA, TGA, PMDA,
NMPA or ANVISA status was verified for this class, and none is recorded in the entry. This is
one of the two reasons `curation_status` stays `IN_PROGRESS`.

### 9. Standards

Five, all verified against the FDA Recognized Consensus Standards database in earlier runs
(recognition numbers 4-300, 4-263, 4-315, 4-265, 4-261): ISO 22674 (metallic materials for
fixed and removable restorations), ISO 9693 (metal-ceramic systems), ISO 24234 (dental
amalgam), ISO 10271 (corrosion test methods), ISO 7405 (biocompatibility).

ISO 22674 alone is not sufficient for the class: it excludes amalgam alloys by its own scope,
which is why ISO 24234 sits alongside it. That is the standards-level echo of the same fact
that makes the regulatory section span five device types.

### 10. Commercial products

**Intentionally empty, and should stay empty.** Brands are instances of the children —
Amalgam, Titanium, Noble metal, Stainless steel — not of the abstract parent. Recording a
product here would put a specific alloy's 510(k) on a class that also contains gold foil.

### 11. History and trends

Metals are the oldest restorative class still in routine use; the IADR puts amalgam alone at
"over 150 years" of service (PMID:42200317). The live direction is contraction on two fronts:
the Minamata Convention phase-down of amalgam, and the displacement of metal-ceramic by
all-ceramic in the esthetic zone. Against that, additive manufacturing is expanding the base
metal branch. None of this is a property of the class in the schema's sense, so none of it
entered the entry; it is recorded here as context for whoever curates the children.

### 12. What changed in the entry as a result of this report

One addition: the CBCT metal-artifact adverse effect from section 7, with two cached sources.
Four candidates were searched and deliberately rejected (thermal conductivity, radiopacity,
antagonist wear, environmental mercury), each for the reason given above. Everything else in
this report confirms what was already there.

`curation_status` stays `IN_PROGRESS`. The two reasons are unchanged and both are recorded in
the entry's `notes`: no full texts were read, and no non-US regulator was verified.

## References cached for this report

| PMID | Title | Used for |
|---|---|---|
| 42203681 | Artificial intelligence for reducing metal artifacts in dental CBCT images: a systematic review | §7, added to entry |
| 42267249 | What Drives Metal Artifacts in CBCT? A Comparative Study of Detector Types and Metallic Object Configurations | §7, added to entry |
| 41206334 | Factors affecting the fit of metal-based restorations fabricated by selective laser melting: A systematic review | §3, context only |
| 42444634 | Restorative materials for direct coronal restoration of permanent posterior teeth: an overview of systematic reviews | §5, §7, context only |
| 42200317 | The IADR Policy and Position Statements on Safety of Dental Amalgam | §2, §7, §11, context only |
| 30661882 | Ceramic versus metal-ceramic implant-supported prostheses: A systematic review and meta-analysis | §6, considered and not added |
