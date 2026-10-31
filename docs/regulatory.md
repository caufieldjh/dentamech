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

On `accessdata.fda.gov` the block is a `User-Agent` *blocklist on automated clients*, not a desktop-browser requirement. Sending **no** `User-Agent` header works; sending a recognisable tool's own header does not. Measured on 2026-10-30 and re-measured unchanged on 2026-10-31, `?id=KLE` with `-L`:

| `User-Agent` sent | Result |
|---|---|
| none (`-A ''`) | `200`, the real KLE record (5 of 5 attempts) |
| a desktop browser string | `200`, the real KLE record (5 of 5) |
| `curl/8.18.0` (curl's default, i.e. no `-A` flag) | `404` abuse-detection apology (11 of 11) |
| `Wget/1.21.3`, `python-urllib3/2.0.7` | `404` abuse-detection apology |

The distinction matters because **"no `User-Agent`" and "no `-A` flag" are opposites here**: plain `curl` without `-A` still sends `User-Agent: curl/8.18.0`, which is exactly what is refused. Earlier versions of this note read that failure as "a desktop `User-Agent` is required"; it is not required, it is merely one string that is not on the blocklist. Either `-A ''` or a browser string works.

**The rule is host-specific and does not generalise.** It governs `accessdata.fda.gov`, which serves the classification, 510(k) and registration databases. `www.fda.gov`, which serves the guidance documents, accepts the *opposite* set of headers: re-measured 2026-10-31, `https://www.fda.gov/media/182280/download` returns the 541 kB PDF under curl's own default header (3 of 3) and a bare `404` with a 10-byte body under both `-A ''` and a desktop browser string (3 of 3 each). Choose the header per host, and do not carry one host's recipe to the other. Note also that the two failures do not look alike: only `accessdata` serves the abuse-detection apology page, which is the one that can be misread as *the record does not exist*; the `www.fda.gov` 404 has no body to misread.

Two further pitfalls, so do not treat the header as the only variable:

- Without `-L` you see only the `302` redirect stub, not the apology page it leads to. The `404` above is the followed redirect.
- Intermittently, and *with* an accepted header, the site answers a ~2 kB queue page reading *"Your request is being processed. Please be patient and wait for this page to refresh in a few seconds"*, served as readily with `400` as with `200`. It carries no record and is not the apology page. Read it as *no answer yet*, never as *the value is absent*, and retry.

So confirm a response actually contains a record before concluding that a product code is absent from the database.

Verified against the product classification database on 2026-10-27 and re-read unchanged on 2026-10-30: `KLE` -> 872.3200, class 2, 510(k), "agent, tooth bonding, resin"; `EMA` -> 872.3275, class 2, 510(k), "cement, dental"; `EMB` -> 872.3275, class 1, 510(k) exempt, "zinc oxide eugenol". The `872.3200` and `872.3275` rows below were re-confirmed on both dates. `872.3275` carries four codes in total (`EMA`, `MZW`, `NEA`, `EMB`); an entry citing only `EMA` is scoping to "cement, dental", not overlooking the others.

Regulations verified against the CFR text and the FDA product classification database on 2026-09-04:

| Regulation | Device name | Class | Product codes | Notes |
|---|---|---|---|---|
| 872.3060 | Noble metal alloy | II (special controls) | EJS, EJT | 510(k)-exempt subject to 872.9 |
| 872.3070 | Dental amalgam, mercury, and amalgam alloy | II (special controls) | EJJ, ELY, OIV | Special controls guidance named in the regulation |
| 872.3200 | Resin tooth bonding agent | II | KLE | |
| 872.3250 | Calcium hydroxide cavity liner | II | | |
| 872.3275 | Dental cement | I (zinc oxide-eugenol, EMB, 510(k)-exempt); II (others, EMA) | EMA, EMB | |
| 872.3640 | Endosseous dental implant | II (special controls) | DZE, NRQ, OAT | Root-form and blade-form |
| 872.3690 | Tooth shade resin material | II | EBF, OFW | |
| 872.3710 | Base metal alloy | II (special controls) | EJH | 510(k)-exempt subject to 872.9 |
| 872.3920 | Porcelain tooth | II | ELL | |

## Other regulators

`agency` also accepts EU MDR, Health Canada, MHRA, TGA, PMDA, NMPA, and ANVISA, with `device_class` values for the EU scheme (IIa, IIb). Nothing beyond FDA is curated yet; the slots exist so the model does not have to change when that happens.
