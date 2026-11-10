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
patient…" queue page, and is sometimes down with `HTTP 503`. Neither
contains a record, so a search for a product code finds nothing. Read either as *no answer yet*,
never as *the value is absent*: retry later, and cross-check with openFDA meanwhile.

openFDA serves the same database as JSON with `product_code`, `device_name`, `device_class`, and
`submission_type_id`; across the eight codes in this file `submission_type_id` is `1` for the 510(k)
codes and `4` for the `510(K) Exempt` ones. It title-cases `device_name`, so quote it only when it is
the URL you cite. Reading both routes is the cheapest way to cross-check a product code that is new
to the KB, and openFDA additionally reports how many codes a regulation carries in total, which is
how the completeness claims in the table below were checked.

Facts about the five regulations curated for `Metal` (872.3060, 872.3070, 872.3330, 872.3350 and
872.3710):

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
  872.3330 row below says so: stainless steel crowns reach it through the ELZ listings, not through
  the regulation's wording.

## A note on `872.9` exemptions

Some device types are class II *and* 510(k)-exempt — `872.3060` and `872.3710` both are. That combination is easy to misread: the exemption is granted in the classification paragraph itself and is bounded by `872.9`, which withdraws it when a device has a new intended use or operates on a different fundamental scientific technology. Record such a device type as `status: EXEMPT` with `pathways: [EXEMPT_510K]`, not as `CLEARED`. `872.3070` sits next to them as the counterexample: same class, same special-controls pattern, no exemption.

## Standards recognition

FDA's [Recognized Consensus Standards database](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfStandards/search.cfm) is where to verify a standard's current edition before recording it. Its per-standard page also lists the regulations and product codes the standard applies to, which makes it a useful independent check on a product code you have already looked up in the classification database. The search form posts to `results.cfm`; the citable per-standard URL is `detail.cfm?standard__identification_no=NNNNN`.

Recognitions recorded for `Metal`:

| Standard | Edition | Recognition number | Extent | Applies to |
|---|---|---|---|---|
| ISO 22674 | Third edition 2022-08 | 4-300 | Complete | 872.3060 (EJS, EJT), 872.3710 (EJH) |
| ISO 9693 | Third edition 2019-10 | 4-263 | Complete | 872.3060, 872.3710, 872.3920, 872.6660 |
| ISO 24234 | Third edition 2021-08 | 4-315 | Complete | 872.3070 (EJJ, ELY) |
| ISO 10271 | Third edition 2020-08 | 4-265 | Complete | 872.3060 (EJS, EJT), 872.3710 (EJH) |
| ISO 7405 | Third edition 2018-10 Corrected version 2018-12 | 4-261 | Complete | 872.3060, 872.3070, 872.3710 and others |

ISO 22674 excludes amalgam alloys by its own scope, which is why a metal entry needs ISO 24234 alongside it. ISO 7405 is the one of the five recognised across the amalgam codes as well as the cast-alloy codes.

## Mapping OHD materials to FDA regulations

The two systems cut the world differently. OHD classifies by *what the material is*; FDA classifies by *what the device is for*. So one OHD material can fall under several regulations (a resin composite used as a core build-up, a luting cement, or a pit and fissure sealant), and one regulation can cover several OHD materials (`872.3275` dental cement spans glass ionomer, zinc phosphate, zinc polycarboxylate, and resin cements). Record one `regulatory_status` entry per applicable regulation, and use `approved_uses` to say which use each one governs.

### `regulation_title` is the device name, not the section heading

The schema defines `regulation_title` as the *device name as given in the classification regulation*. The two differ whenever one section classifies more than one device type, and then only the device name carries the class.

`872.3275` is the case in this KB. Its heading is `§ 872.3275 Dental cement.`, but it names two devices with two different classes:

| CFR paragraph | Device name as the regulation gives it | Class | Product code |
|---|---|---|---|
| `(a)` | Zinc oxide-eugenol | I (general controls), exempt subject to 872.9 | EMB |
| `(b)` | Dental cement other than zinc oxide-eugenol | II | EMA |

So an entry asserting `device_class: CLASS_II` under this regulation carries `regulation_title: Dental cement other than zinc oxide-eugenol`. Using the section heading would drop the distinction the class depends on. The table below has one row per section, so it prints the heading; material entries use the device name.

### Looking up a product code

Both URL forms work. The `?id=<CODE>` form returns that one record; the `?start_search=1&regulationnumber=NNNN` form returns every code under one regulation, which is what justifies the codes an entry omits.

```
https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpcd/classification.cfm?id=KLE
https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpcd/classification.cfm?start_search=1&regulationnumber=872.3200
```

Two pitfalls:

- Without `-L` you see only the `302` redirect stub, not the page it leads to.
- Intermittently, the site answers with a ~2 kB queue page reading *"Your request is being processed. Please be patient and wait for this page to refresh in a few seconds"*, served as readily with `400` as with `200`. It carries no record. Read it as *no answer yet*, never as *the value is absent*, and retry.

So confirm a response actually contains a record before concluding that a product code is absent from the database.

Verified against the product classification database on 2026-10-27 and re-read unchanged on 2026-10-30: `KLE` -> 872.3200, class 2, 510(k), "agent, tooth bonding, resin"; `EMA` -> 872.3275, class 2, 510(k), "cement, dental"; `EMB` -> 872.3275, class 1, 510(k) exempt, "zinc oxide eugenol". The `872.3200` and `872.3275` rows below were re-confirmed on both dates. `872.3275` carries four codes in total (`EMA`, `MZW`, `NEA`, `EMB`); an entry citing only `EMA` is scoping to "cement, dental", not overlooking the others.

Regulations verified against the CFR text and the FDA product classification database on 2026-09-04:

| Regulation | Device name | Class | Product codes | Notes |
|---|---|---|---|---|
| 872.3060 | Noble metal alloy | II (special controls) | EJS, EJT | 510(k)-exempt subject to 872.9. The database also returns EIT (applicator, rapid wax, dental) under this regulation; it is a laboratory accessory, not an alloy |
| 872.3070 | Dental amalgam, mercury, and amalgam alloy | II (special controls) | EJJ, ELY, OIV | Special controls guidance named in the regulation |
| 872.3200 | Resin tooth bonding agent | II | KLE | |
| 872.3250 | Calcium hydroxide cavity liner | II | | |
| 872.3275 | Dental cement | I (zinc oxide-eugenol, EMB, 510(k)-exempt); II (others, EMA) | EMA, EMB, MZW, NEA | Re-verified 2026-09-05. MZW (dental cement w/out zinc-oxide eugenol as an ulcer covering, class II) and NEA (cement, ear, nose and throat, class II) also sit under this regulation but are not dental restorative uses |
| 872.3330 | Preformed crown | I | ELZ | 510(k)-exempt subject to 872.9. Covers plastic and austenitic preformed crowns, so it is not a metal-only device type; stainless steel crowns are listed under ELZ |
| 872.3350 | Gold or stainless steel cusp | I | ELO | 510(k)-exempt subject to 872.9. The only device type in subpart D naming both gold and stainless steel; prosthodontic (permanent cusp against a removable denture), not restorative |
| 872.3640 | Endosseous dental implant | II (special controls) | DZE, NRQ, OAT | Root-form and blade-form |
| 872.3690 | Tooth shade resin material | II | EBF, OFW | |
| 872.3710 | Base metal alloy | II (special controls) | EJH | 510(k)-exempt subject to 872.9 |
| 872.3920 | Porcelain tooth | II | ELL | Prefabricated device the regulation defines as made of the 872.6660 material. Re-verified 2026-10-28 |
| 872.6660 | Porcelain powder for clinical use | II | EIH | Subpart G. The material-level device type for dental ceramics; modern lithium disilicate and zirconia blanks clear under EIH. Re-verified 2026-10-28 |

## FDA performance criteria for dental cements

FDA's final guidance *Dental Cements - Performance Criteria for Safety and Performance Based Pathway* (September 2024, docket FDA-2024-D-4171) gives performance criteria that a 510(k) may use in place of a direct predicate comparison. It applies to class II dental cements under `872.3275` (EMA), `872.3200` (KLE) and `872.3750` (DYH), and explicitly excludes `872.3275` EMB and MZW, `872.3690` (EBF, OFW) and `872.3250` (EJK). Its criteria are drawn from ISO 9917-1 and ISO 9917-2, so it is a convenient, citable source for class-level values (film thickness, net setting time, compressive strength, acid erosion) when the ISO text itself is not to hand.

The guidance scopes each test item separately, and **not all items have the same scope**, so a class-level entry cannot apply one blanket caveat to all of them. Verified against the guidance PDF on 2026-10-06:

| Test item | Scope as the guidance marks it | Reaches resin-modified members? |
|---|---|---|
| 3. Film thickness | "as applicable, luting cements only" | Yes — scoped by application, cites both parts |
| 4. Net setting time | *no restriction* | Yes — Table 2 has a fourth, resin-modified row |
| 5. Compressive strength | "as applicable, powder/liquid acid-base cements only" | No |
| 6. Acid erosion | "as applicable, powder/liquid acid-base cements only" | No |
| 7. Working time | "as applicable, resin-modified cements only" | Resin-modified only |
| 8. Flexural strength | "as applicable, resin-modified cements only" | Resin-modified only |

Items 3 and 4 name "ISO 9917-1 **or** ISO 9917-2" as methodology, so their `test_method` should name both parts. Table 2's resin-modified row reads `tsetting ≤ 8 min` / `tsetting ≤ 6 min` — an upper bound with no lower bound, unlike the three powder/liquid rows. Quote Table 2 complete; a range such as `1.5-8 min` is the envelope of the stated limits, and its lower end is not a minimum for all four families.

**Read the per-item scope inside the document scope, never instead of it.** The two columns above are about test items, and a test item with no "as applicable" marking is unrestricted only *within* the three product codes section III admits. Item 4 is the trap: "no restriction" does not make net setting time class-wide for an OHD cement class, because section III has already excluded `872.3275` EMB — and a zinc oxide-eugenol cement is a member of the OHD acid-base cement class (`OHD:0001007` under `OHD:0001022` under `OHD:0001021`). The reach of item 4 is the four families Table 2 names, which is not the same set as the class. The same applies to item 3: "luting cements only" is the guidance's phrase for its own luting cements, not for every luting cement in an OHD class. When a class-level entry sources a property here, scope the row to the families the criterion names and say so in `conditions`.

Editions of a standard should be checked against FDA's [Recognized Consensus Standards database](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfStandards/search.cfm), which is searched through its form (a `POST` to `results.cfm`). A query string is ignored and returns the unfiltered listing, so check that a response says `1 result found` before reading a row from it. The ISO catalogue blocks automated retrieval (`403` on 2026-10-10), so an ISO catalogue URL recorded on a `standards` row cannot be confirmed from the catalogue itself; confirm the edition here and the catalogue number through a reseller listing that quotes it.

## Other regulators

`agency` also accepts EU MDR, Health Canada, MHRA, TGA, PMDA, NMPA, and ANVISA, with `device_class` values for the EU scheme (IIa, IIb). Nothing beyond FDA is curated yet; the slots exist so the model does not have to change when that happens.
