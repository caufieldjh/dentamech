# Regulatory status

The question this section answers for each material: *what is it approved for, and by whom?*

## How FDA regulates dental materials

FDA regulates dental materials as medical devices through the Center for Devices and Radiological Health. Dental devices are classified in [21 CFR part 872](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-872); restorative and prosthetic materials sit in subpart D, *Prosthetic Devices*. Each section (for example `872.3690`, tooth shade resin material) gives an *identification* paragraph describing the device type and its intended use, and a *classification* paragraph assigning a risk class.

- **Class I**: general controls. Often exempt from premarket notification.
- **Class II**: general and special controls. Usually reaches market through a 510(k) premarket notification showing substantial equivalence to a predicate; some class II dental materials are 510(k)-exempt subject to the limits of `872.9`.
- **Class III**: premarket approval (PMA).

Each regulation maps to one or more three-letter **product codes** in FDA's [Product Classification database](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfPCD/classification.cfm). A product code is what individual 510(k) records carry, so it is the join key between a device type and the products cleared under it.

## Two levels in the model

**`regulatory_status`** is the device-type level. One entry per agency and regulation:

```yaml
regulatory_status:
- agency: FDA
  status: CLEARED                    # what standing the device type has
  regulation_number: '872.3690'      # section of 21 CFR 872
  regulation_title: Tooth shade resin material
  device_class: CLASS_II
  product_codes: [EBF, OFW]
  pathways: [PREMARKET_NOTIFICATION_510K]
  special_controls: []               # guidance documents named in the regulation
  identification: >-                 # paragraph (a), quoted verbatim
    Tooth shade resin material is a device composed of materials such as
    bisphenol-A glycidyl methacrylate (Bis-GMA) intended to restore carious
    lesions or structural defects in teeth.
  approved_uses:                     # what the regulation permits
  - name: Restoration of carious lesions or structural defects in teeth
    use_context: DIRECT_RESTORATION
  restrictions: []                   # population or labeling limits
  source_url: https://www.ecfr.gov/current/title-21/section-872.3690
  evidence: []
```

**`products`** is the product level. A branded product and its submissions:

```yaml
products:
- name: Filtek Supreme Ultra
  manufacturer: 3M ESPE
  submissions:
  - agency: FDA
    submission_number: K093412
    pathway: PREMARKET_NOTIFICATION_510K
    decision: CLEARED
    decision_date: '2010-01-22'
    product_code: EBF
    regulation_number: '872.3690'
    indications_for_use: >-
      (quoted from the 510(k) summary)
    source_url: https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID=K093412
```

The product example above is illustrative; check the record before curating it.

## Sources for the FDA databases

Every regulation number, class, and product code is re-verified from the CFR text *and* the
classification database on each curation run. The sources:

| Source | Where |
|---|---|
| CFR text | `https://www.law.cornell.edu/cfr/text/21/872.NNNN` |
| Product classification, human-readable record | `https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpcd/classification.cfm?start_search=1&regulationnumber=872.NNNN` |
| Product classification, JSON | `https://api.fda.gov/device/classification.json?search=regulation_number:"872.NNNN"&limit=50` (openFDA) |

Cite the `classification.cfm` URL: it is the human-readable record, and it renders device names in
lower case, which is what a `snippet` quoting it has to match.

`classification.cfm` sometimes answers with a ~2 kB "Your request is being processed. Please be
patient…" queue page, and was down with `HTTP 503` on 2026-10-24 (recovered by 2026-10-25). Neither
contains a record, so a search for a product code finds nothing. Read either as *no answer yet*,
never as *the value is absent*: retry later, and cross-check with openFDA meanwhile.

openFDA serves the same database as JSON with `product_code`, `device_name`, `device_class`, and
`submission_type_id`; across the eight codes in this file `submission_type_id` is `1` for the 510(k)
codes and `4` for the `510(K) Exempt` ones. It title-cases `device_name`, so quote it only when it is
the URL you cite. Reading both routes is the cheapest way to cross-check a product code that is new
to the KB, and openFDA additionally reports how many codes a regulation carries in total, which is
how the completeness claims in the table below were checked.

All five of the regulations curated for `Metal` - 872.3060, 872.3070, 872.3330, 872.3350, and
872.3710 - have been re-verified from the CFR text and the product classification database on every
run that has tended the entry, and **nothing has changed since 2026-09-06**. The facts worth reading
off that history instead of re-deriving them:

- Submission type in the classification database is `510(K) Exempt` for EJS, EJT, EJH, ELZ, and ELO,
  and `510(k)` for EJJ, ELY, and OIV.
- Per-regulation code counts, from openFDA: 872.3060 three (EJS, EJT, and the excluded EIT),
  872.3070 three, and 872.3330, 872.3350, and 872.3710 one each. The "only product code under the
  regulation" claims on the last three are therefore complete, not merely unrefuted.
- EIT stays excluded from 872.3060: it is a rapid wax applicator, a laboratory accessory rather than
  an alloy.
- `872.3330` is the route by which preformed stainless steel crowns reach the market, established from
  the device listings under ELZ - NuSmile, Hu-Friedy and Cargus all list preformed stainless steel
  crowns with ELZ as their only product code - and not from the identification paragraph, which names
  plastic, austenitic alloys and high-gold platinum-group alloys without naming stainless steel. Do not
  infer it from the austenitic clause alone: 872.3350 enumerates austenitic alloys and stainless steel
  as distinct materials in one sentence, so FDA's drafting does not treat them as synonyms. The
  `(stainless steel)` gloss on the 872.3330 row below is shorthand for that listing practice, not for
  the regulation's wording.

The audit trail below has one row per run that verified the mapping-table rows that follow it,
oldest first. The verdict on every row is the same - nothing had changed - so only the scope and
the route differ.

| Date | Scope checked | Route |
|---|---|---|
| 2026-09-06 | 872.3060, 872.3070, 872.3710: titles, identification paragraphs, classes, product codes | CFR text + classification database |
| 2026-09-09 | adds 872.3330 | same two |
| 2026-09-10 | adds 872.3350 | same two |
| 2026-10-01 | all five regulations, all eight product codes, all five identification paragraphs | same two |
| 2026-10-12 | five identification and five classification paragraphs, diffed character for character; eight product codes | eCFR versioner XML (2026-10-06 issue of title 21) + classification database |
| 2026-10-19 | five identification and classification paragraphs; eight product codes through both routes; the EIT exclusion | CFR text + `classification.cfm` + openFDA |
| 2026-10-22 | as above, plus the per-regulation code counts read rather than assumed | openFDA |
| 2026-10-23 | five identification paragraphs diffed character for character; five regulation titles against the section heads; eight product codes with submission type and code counts on each | eCFR versioner XML + `classification.cfm` + openFDA |
| 2026-10-24 | five regulation numbers, titles, classes, special-controls clauses and 510(k)-exemption clauses; five identification and five classification snippets confirmed verbatim; eight product codes on `device_name`, `device_class`, `submission_type_id`, `medical_specialty_description`, `regulation_number` | CFR text + openFDA only, `classification.cfm` returning HTTP 503 through every route |
| 2026-10-25 | five regulation numbers, titles, classes and exemption clauses; eight product codes including submission type on EJS and EJJ | CFR text + `classification.cfm`, recovered |
| 2026-10-26 | five regulation titles, identification paragraphs and classification clauses confirmed verbatim; eight product codes on device name, class, regulation number and submission type, plus the per-regulation code counts | CFR text + `classification.cfm` + openFDA |
| 2026-10-27 | five regulation numbers, titles, classes, identification paragraphs and 510(k)-exemption clauses re-read from the CFR text and diffed against the entry; eight product codes on device name, class, regulation number and submission type; per-regulation code completeness read from the `regulationnumber` result tables, including the EIT exclusion | CFR text + `classification.cfm` (both the `id` and `regulationnumber` routes) |
| 2026-10-28 | 872.3275, 872.3330 and 872.3350 titles, identification paragraphs and classification clauses re-read from the CFR text; the code sets and submission types under 872.3060, 872.3275, 872.3330 and 872.3350 read from openFDA, including the per-regulation code counts behind the EIT exclusion and the four codes under 872.3275 | CFR text + openFDA only, `classification.cfm` serving the queue page through every route |
| 2026-11-02 | five regulation numbers, titles, classes, identification paragraphs and 510(k)-exemption clauses re-read from the CFR text, with all five `identification` fields and all five classification snippets confirmed verbatim against it by programmatic substring check (10 of 10, 0 mismatched); eight product codes with per-regulation code completeness and submission type, including the EIT exclusion; ISO 22674, 9693 and 24234 recognition numbers, editions and extents re-read from the Recognized Consensus Standards database | CFR text + openFDA by `regulation_number` + `cfStandards/detail.cfm` |
| 2026-11-07 | five regulation numbers, titles, classes, identification paragraphs and 510(k)-exemption clauses re-read from the CFR text and confirmed verbatim by programmatic substring check (10 of 10, 0 mismatched); eight product codes on device name, class, regulation number and submission type, with per-regulation code counts read rather than assumed (872.3060 three including the excluded EIT, 872.3070 three, the other three one each); the four ELZ device listings behind the 872.3330 stainless steel claim; all 54 PMID-backed snippets re-checked against the abstracts PubMed serves, with the reference cache bypassed (54 of 54 verbatim) | CFR text + openFDA `classification.json` by `product_code` and `regulation_number` + openFDA `registrationlisting.json` + PubMed E-utilities |

**`classification.cfm` answered nothing but the queue page on 2026-10-28.** Both the `id=CODE` and
the `start_search=1&regulationnumber=` routes returned the same 1,986-byte "Your request is being
processed" page described above, on six consecutive attempts per route and across all six codes
tried. The status was `200`. Treat it as *no answer yet*. openFDA
answered normally throughout and was used to cross-check the codes instead.

One correction to the record: the 2026-10-22 and 2026-10-23 rows were originally written as though a
pull request accompanied those runs. No pull request existed on `curate/metal` on either date, and
`gh pr list --head curate/metal --state all` was still empty on 2026-10-24. Only the dating clause
was wrong; the verifications happened.

## A note on `872.9` exemptions

Some device types are class II *and* 510(k)-exempt — `872.3060` and `872.3710` both are. That combination is easy to misread: the exemption is granted in the classification paragraph itself and is bounded by `872.9`, which withdraws it when a device has a new intended use or operates on a different fundamental scientific technology. Record such a device type as `status: EXEMPT` with `pathways: [EXEMPT_510K]`, not as `CLEARED`. `872.3070` sits next to them as the counterexample: same class, same special-controls pattern, no exemption.

## Standards recognition

FDA's [Recognized Consensus Standards database](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfStandards/search.cfm) is where to verify a standard's current edition before recording it. Its per-standard page also lists the regulations and product codes the standard applies to, which makes it a useful independent check on a product code you have already looked up in the classification database. The search form posts to `results.cfm`; the citable per-standard URL is `detail.cfm?standard__identification_no=NNNNN`.

Recognitions verified on 2026-09-08 while curating `Metal`:

| Standard | Edition | Recognition number | Extent | Applies to |
|---|---|---|---|---|
| ISO 22674 | Third edition 2022-08 | 4-300 | Complete | 872.3060 (EJS, EJT), 872.3710 (EJH) |
| ISO 9693 | Third edition 2019-10 | 4-263 | Complete | 872.3060, 872.3710, 872.3920, 872.6660 |
| ISO 24234 | Third edition 2021-08 | 4-315 | Complete | 872.3070 (EJJ, ELY) |
| ISO 10271 | Third edition 2020-08 | 4-265 | Complete | 872.3060 (EJS, EJT), 872.3710 (EJH) |
| ISO 7405 | Third edition 2018-10 Corrected version 2018-12 | 4-261 | Complete | 872.3060, 872.3070, 872.3710 and others |

ISO 22674 excludes amalgam alloys by its own scope, which is why a metal entry needs ISO 24234 alongside it. ISO 10271 and ISO 7405 were verified on 2026-09-09; ISO 7405 is the one of the five recognised across the amalgam codes as well as the cast-alloy codes.

All five rows above - edition, recognition number, extent, and the regulation and product codes each standard is recognised against - were re-read from `detail.cfm` on 2026-10-29 and are unchanged. The audit trail above this section covers the regulations only, so standards recognitions need their own date: FDA re-recognises editions and retires them independently of the CFR, and a `standards` row can go stale while every regulation on the same entry stays correct.

## Mapping OHD materials to FDA regulations

The two systems cut the world differently. OHD classifies by *what the material is*; FDA classifies by *what the device is for*. So one OHD material can fall under several regulations (a resin composite used as a core build-up, a luting cement, or a pit and fissure sealant), and one regulation can cover several OHD materials (`872.3275` dental cement spans glass ionomer, zinc phosphate, zinc polycarboxylate, and resin cements). Record one `regulatory_status` entry per applicable regulation, and use `approved_uses` to say which use each one governs.

Regulations verified against the CFR text and the FDA product classification database on 2026-09-04:

| Regulation | Device name | Class | Product codes | Notes |
|---|---|---|---|---|
| 872.3060 | Noble metal alloy | II (special controls) | EJS, EJT | 510(k)-exempt subject to 872.9. The database also returns EIT (applicator, rapid wax, dental) under this regulation; it is a laboratory accessory, not an alloy |
| 872.3070 | Dental amalgam, mercury, and amalgam alloy | II (special controls) | EJJ, ELY, OIV | Special controls guidance named in the regulation |
| 872.3200 | Resin tooth bonding agent | II | | |
| 872.3250 | Calcium hydroxide cavity liner | II | | |
| 872.3275 | Dental cement | I (zinc oxide-eugenol, EMB, 510(k)-exempt); II (others, EMA) | EMA, EMB, MZW, NEA | Re-verified 2026-09-05. MZW (dental cement w/out zinc-oxide eugenol as an ulcer covering, class II) and NEA (cement, ear, nose and throat, class II) also sit under this regulation but are not dental restorative uses |
| 872.3330 | Preformed crown | I | ELZ | 510(k)-exempt subject to 872.9. Covers plastic and austenitic (stainless steel) preformed crowns, so it is not a metal-only device type |
| 872.3350 | Gold or stainless steel cusp | I | ELO | 510(k)-exempt subject to 872.9. The only device type in subpart D naming both gold and stainless steel; prosthodontic (permanent cusp against a removable denture), not restorative |
| 872.3640 | Endosseous dental implant | II (special controls) | DZE, NRQ, OAT | Root-form and blade-form |
| 872.3690 | Tooth shade resin material | II | EBF, OFW | |
| 872.3710 | Base metal alloy | II (special controls) | EJH | 510(k)-exempt subject to 872.9 |
| 872.3920 | Porcelain tooth | II | ELL | |

## Other regulators

`agency` also accepts EU MDR, Health Canada, MHRA, TGA, PMDA, NMPA, and ANVISA, with `device_class` values for the EU scheme (IIa, IIb). Nothing beyond FDA is curated yet; the slots exist so the model does not have to change when that happens.
