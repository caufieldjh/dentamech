from __future__ import annotations

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal
from enum import Enum
from typing import (
    Any,
    ClassVar,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    SerializationInfo,
    SerializerFunctionWrapHandler,
    field_validator,
    model_serializer
)


metamodel_version = "1.11.0"
version = "None"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        serialize_by_alias = True,
        validate_by_name = True,
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )





class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'default_prefix': 'dentamech',
     'default_range': 'string',
     'description': 'Schema for the Dental Materials Knowledge Base (dentamech). '
                    'One YAML file per material, anchored to the Oral Health and '
                    'Disease Ontology (OHD) branch under OHD:0000000 "dental '
                    'restoration material". Each entry records what the material '
                    'is made of, how it sets, what it is used for clinically, how '
                    'it performs, what can go wrong, and how regulators (FDA '
                    'first) classify it and what they permit it to be used for. '
                    'Every claim can carry literature or regulatory-document '
                    'evidence with an exact quoted snippet, following the DisMech '
                    'evidence model.',
     'id': 'https://w3id.org/caufieldjh/dentamech',
     'imports': ['linkml:types'],
     'license': 'BSD-3-Clause',
     'name': 'dentamech',
     'prefixes': {'BFO': {'prefix_prefix': 'BFO',
                          'prefix_reference': 'http://purl.obolibrary.org/obo/BFO_'},
                  'CFR': {'prefix_prefix': 'CFR',
                          'prefix_reference': 'https://www.ecfr.gov/current/title-21/section-'},
                  'CHEBI': {'prefix_prefix': 'CHEBI',
                            'prefix_reference': 'http://purl.obolibrary.org/obo/CHEBI_'},
                  'DOI': {'prefix_prefix': 'DOI',
                          'prefix_reference': 'https://doi.org/'},
                  'FDA_PRODUCT_CODE': {'prefix_prefix': 'FDA_PRODUCT_CODE',
                                       'prefix_reference': 'https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfPCD/classification.cfm?start_search=1&productcode='},
                  'HP': {'prefix_prefix': 'HP',
                         'prefix_reference': 'http://purl.obolibrary.org/obo/HP_'},
                  'MONDO': {'prefix_prefix': 'MONDO',
                            'prefix_reference': 'http://purl.obolibrary.org/obo/MONDO_'},
                  'NCIT': {'prefix_prefix': 'NCIT',
                           'prefix_reference': 'http://purl.obolibrary.org/obo/NCIT_'},
                  'OBI': {'prefix_prefix': 'OBI',
                          'prefix_reference': 'http://purl.obolibrary.org/obo/OBI_'},
                  'OHD': {'prefix_prefix': 'OHD',
                          'prefix_reference': 'http://purl.obolibrary.org/obo/OHD_'},
                  'PATO': {'prefix_prefix': 'PATO',
                           'prefix_reference': 'http://purl.obolibrary.org/obo/PATO_'},
                  'PMID': {'prefix_prefix': 'PMID',
                           'prefix_reference': 'http://www.ncbi.nlm.nih.gov/pubmed/'},
                  'UBERON': {'prefix_prefix': 'UBERON',
                             'prefix_reference': 'http://purl.obolibrary.org/obo/UBERON_'},
                  'dentamech': {'prefix_prefix': 'dentamech',
                                'prefix_reference': 'https://w3id.org/caufieldjh/dentamech/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'skos': {'prefix_prefix': 'skos',
                           'prefix_reference': 'http://www.w3.org/2004/02/skos/core#'},
                  'xsd': {'prefix_prefix': 'xsd',
                          'prefix_reference': 'http://www.w3.org/2001/XMLSchema#'}},
     'see_also': ['https://github.com/caufieldjh/dentamech',
                  'https://github.com/monarch-initiative/dismech'],
     'source_file': 'src/dentamech/schema/dentamech.yaml',
     'title': 'Dental Materials Knowledge Base Schema',
     'types': {'ReferenceIdentifier': {'base': 'str',
                                       'description': 'A CURIE-style identifier '
                                                      'for a citable source. '
                                                      'Literature references use '
                                                      'PMID:, PMC:, DOI:, or PPR: '
                                                      '(Europe PMC preprints). Web '
                                                      'sources use url:. '
                                                      'Regulatory documents should '
                                                      'be cited by url: pointing '
                                                      'at the eCFR section, the '
                                                      'FDA 510(k)/PMA database '
                                                      'record, or the guidance '
                                                      'document.',
                                       'from_schema': 'https://w3id.org/caufieldjh/dentamech',
                                       'name': 'ReferenceIdentifier',
                                       'typeof': 'string',
                                       'uri': 'xsd:string'}}} )

class EvidenceItemSupportEnum(str, Enum):
    """
    How the cited source relates to the claim it is attached to
    """
    Supports = "SUPPORT"
    """
    The cited evidence directly supports the claim
    """
    Partially_supports = "PARTIAL"
    """
    The cited evidence partially or indirectly supports the claim
    """
    Refutes = "REFUTE"
    """
    The cited evidence directly contradicts the claim
    """
    No_evidence = "NO_EVIDENCE"
    """
    The cited reference does not contain evidence relevant to the claim
    """
    Wrong_statement = "WRONG_STATEMENT"
    """
    The claim contains a demonstrable factual error and the cited source documents the correct information
    """


class EvidenceSourceEnum(str, Enum):
    """
    The kind of source an evidence item comes from
    """
    Human_clinical = "HUMAN_CLINICAL"
    """
    Clinical trials, cohort studies, case series, or practice-based research in patients
    """
    In_vitro_SOLIDUS_laboratory = "IN_VITRO"
    """
    Bench testing of the material (mechanical, physical, chemical, cytotoxicity, wear simulation)
    """
    Computational = "IN_SILICO"
    """
    Finite element analysis, simulation, or other modeling
    """
    Systematic_review_or_meta_analysis = "SYSTEMATIC_REVIEW"
    """
    Pooled or systematically reviewed evidence
    """
    Regulatory_document = "REGULATORY_DOCUMENT"
    """
    A regulation (e.g. 21 CFR 872), a classification database record, a 510(k) summary, a PMA approval order, a guidance document, or an equivalent from another jurisdiction
    """
    Technical_standard = "STANDARD"
    """
    An ISO, ADA/ANSI, or ASTM standard or specification
    """
    Manufacturer_document = "MANUFACTURER"
    """
    Instructions for use, safety data sheet, technical profile, or product literature
    """
    Textbook_or_monograph = "TEXTBOOK"
    """
    A textbook, monograph, or reference work
    """
    Other = "OTHER"
    """
    Evidence not fitting the above
    """


class MaterialCategoryEnum(str, Enum):
    """
    Broad material class. Derived from the OHD ancestry of the bound term when seeding, and kept as an explicit slot so the browser can facet on it without walking the ontology.
    """
    METAL = "METAL"
    """
    Metals and alloys (amalgam, noble and base metal alloys, titanium, stainless steel)
    """
    CERAMIC = "CERAMIC"
    """
    Glass-matrix, polycrystalline, and resin-matrix ceramics
    """
    RESIN_COMPOSITE = "RESIN_COMPOSITE"
    """
    Resin-based composites (polymer matrix reinforced with filler)
    """
    CEMENT = "CEMENT"
    """
    Luting, lining, base, and endodontic cements, whether acid-base, resin, or hydraulic
    """
    POLYMER = "POLYMER"
    """
    Unfilled or lightly filled polymers (denture base resins, impression materials, sealants)
    """
    ADHESIVE = "ADHESIVE"
    """
    Bonding agents, primers, and their monomers
    """
    HYBRID = "HYBRID"
    """
    Materials that deliberately combine two categories (e.g. compomers, resin-modified glass ionomers)
    """
    OTHER = "OTHER"
    """
    Does not fit the other categories
    """


class SettingMechanismEnum(str, Enum):
    """
    How the material hardens or is formed into its final state
    """
    LIGHT_CURED = "LIGHT_CURED"
    """
    Photopolymerization initiated by visible (typically blue) light
    """
    SELF_CURED = "SELF_CURED"
    """
    Chemically initiated polymerization (two-paste or powder-liquid)
    """
    DUAL_CURED = "DUAL_CURED"
    """
    Both light-initiated and chemically initiated polymerization
    """
    ACID_BASE_REACTION = "ACID_BASE_REACTION"
    """
    Acid-base setting reaction between a basic powder and an acidic liquid
    """
    AMALGAMATION = "AMALGAMATION"
    """
    Reaction of mercury with alloy particles
    """
    HYDRATION = "HYDRATION"
    """
    Hydraulic setting on contact with water (e.g. calcium silicate cements)
    """
    SINTERING = "SINTERING"
    """
    Densification of a powder compact or milled blank at high temperature
    """
    HEAT_PRESSING = "HEAT_PRESSING"
    """
    Pressing of a heated glass ceramic ingot into a mold
    """
    CASTING = "CASTING"
    """
    Lost-wax casting of a molten alloy
    """
    MILLING = "MILLING"
    """
    Subtractive CAD/CAM machining of a prefabricated block or disc
    """
    ADDITIVE_MANUFACTURING = "ADDITIVE_MANUFACTURING"
    """
    3D printing (stereolithography, selective laser melting, etc.)
    """
    COLD_WORKING = "COLD_WORKING"
    """
    Condensation or burnishing without a chemical set (e.g. gold foil)
    """
    NONE = "NONE"
    """
    Supplied in final form; no setting step
    """


class ComponentRoleEnum(str, Enum):
    """
    The functional role a component plays in the material's formulation
    """
    MATRIX = "MATRIX"
    """
    Continuous phase (polymer matrix, glass phase, metal matrix)
    """
    FILLER = "FILLER"
    """
    Dispersed reinforcing or bulking particles or fibers
    """
    COUPLING_AGENT = "COUPLING_AGENT"
    """
    Agent bonding filler to matrix (e.g. silane)
    """
    INITIATOR = "INITIATOR"
    """
    Initiates polymerization (e.g. camphorquinone, benzoyl peroxide)
    """
    ACTIVATOR = "ACTIVATOR"
    """
    Co-initiator or accelerator (e.g. tertiary amine)
    """
    INHIBITOR = "INHIBITOR"
    """
    Stabilizer that prevents premature polymerization
    """
    POWDER = "POWDER"
    """
    Powder component of a powder-liquid system
    """
    LIQUID = "LIQUID"
    """
    Liquid component of a powder-liquid system
    """
    ALLOYING_ELEMENT = "ALLOYING_ELEMENT"
    """
    Element present in an alloy
    """
    CRYSTALLINE_PHASE = "CRYSTALLINE_PHASE"
    """
    Crystalline phase in a ceramic
    """
    STABILIZER = "STABILIZER"
    """
    Phase stabilizer (e.g. yttria in zirconia)
    """
    RADIOPACIFIER = "RADIOPACIFIER"
    """
    Added to make the material radiopaque
    """
    PIGMENT = "PIGMENT"
    """
    Colorant or opacifier
    """
    SOLVENT = "SOLVENT"
    """
    Carrier or solvent
    """
    FLUORIDE_SOURCE = "FLUORIDE_SOURCE"
    """
    Component that releases fluoride
    """
    OTHER = "OTHER"
    """
    Other role
    """


class PropertyTypeEnum(str, Enum):
    """
    Physical, mechanical, chemical, optical, and biological properties commonly reported for dental materials. Units are recorded on the property itself; this enum only names the quantity.
    """
    FLEXURAL_STRENGTH = "FLEXURAL_STRENGTH"
    """
    Flexural (bending) strength, typically MPa
    """
    COMPRESSIVE_STRENGTH = "COMPRESSIVE_STRENGTH"
    """
    Compressive strength, typically MPa
    """
    TENSILE_STRENGTH = "TENSILE_STRENGTH"
    """
    Tensile or diametral tensile strength, typically MPa
    """
    ELASTIC_MODULUS = "ELASTIC_MODULUS"
    """
    Elastic (Young's) modulus, typically GPa
    """
    FRACTURE_TOUGHNESS = "FRACTURE_TOUGHNESS"
    """
    Fracture toughness, typically MPa·m^0.5
    """
    HARDNESS = "HARDNESS"
    """
    Surface hardness (Vickers, Knoop)
    """
    WEAR_RESISTANCE = "WEAR_RESISTANCE"
    """
    Wear or abrasion resistance
    """
    BOND_STRENGTH = "BOND_STRENGTH"
    """
    Bond strength to tooth structure or another substrate, typically MPa
    """
    POLYMERIZATION_SHRINKAGE = "POLYMERIZATION_SHRINKAGE"
    """
    Volumetric or linear shrinkage on setting, typically percent
    """
    SHRINKAGE_STRESS = "SHRINKAGE_STRESS"
    """
    Stress generated during setting
    """
    DEGREE_OF_CONVERSION = "DEGREE_OF_CONVERSION"
    """
    Fraction of monomer converted to polymer, typically percent
    """
    DEPTH_OF_CURE = "DEPTH_OF_CURE"
    """
    Depth to which a light-cured material polymerizes adequately, typically mm
    """
    WATER_SORPTION = "WATER_SORPTION"
    """
    Water sorption, typically µg/mm^3
    """
    SOLUBILITY = "SOLUBILITY"
    """
    Solubility or disintegration in water or acid
    """
    THERMAL_EXPANSION = "THERMAL_EXPANSION"
    """
    Coefficient of thermal expansion
    """
    THERMAL_CONDUCTIVITY = "THERMAL_CONDUCTIVITY"
    """
    Thermal conductivity
    """
    RADIOPACITY = "RADIOPACITY"
    """
    Radiopacity, typically relative to aluminum thickness
    """
    TRANSLUCENCY = "TRANSLUCENCY"
    """
    Translucency or contrast ratio
    """
    COLOR_STABILITY = "COLOR_STABILITY"
    """
    Resistance to discoloration
    """
    FLUORIDE_RELEASE = "FLUORIDE_RELEASE"
    """
    Fluoride release or recharge
    """
    SETTING_TIME = "SETTING_TIME"
    """
    Time to set, typically minutes
    """
    WORKING_TIME = "WORKING_TIME"
    """
    Time available for manipulation, typically minutes
    """
    FILM_THICKNESS = "FILM_THICKNESS"
    """
    Film thickness of a luting agent, typically µm
    """
    CORROSION_RESISTANCE = "CORROSION_RESISTANCE"
    """
    Resistance to corrosion or tarnish
    """
    BIOCOMPATIBILITY = "BIOCOMPATIBILITY"
    """
    Biological response (cytotoxicity, sensitization, irritation)
    """
    ANTIBACTERIAL_ACTIVITY = "ANTIBACTERIAL_ACTIVITY"
    """
    Antibacterial or antimicrobial effect
    """
    DENSITY = "DENSITY"
    """
    Density
    """
    MELTING_RANGE = "MELTING_RANGE"
    """
    Melting or fusion temperature range
    """
    OTHER = "OTHER"
    """
    Other property
    """


class ClinicalUseContextEnum(str, Enum):
    """
    The broad clinical context in which the material is used
    """
    DIRECT_RESTORATION = "DIRECT_RESTORATION"
    """
    Placed and shaped directly in the prepared tooth (fillings)
    """
    INDIRECT_RESTORATION = "INDIRECT_RESTORATION"
    """
    Fabricated outside the mouth and cemented (inlays, onlays, crowns, bridges, veneers)
    """
    LUTING = "LUTING"
    """
    Cementing an indirect restoration, post, or orthodontic appliance
    """
    LINER_OR_BASE = "LINER_OR_BASE"
    """
    Cavity liner or base under a restoration
    """
    PULP_THERAPY = "PULP_THERAPY"
    """
    Pulp capping, pulpotomy, or other vital pulp therapy
    """
    ENDODONTIC = "ENDODONTIC"
    """
    Root canal filling, sealing, perforation repair, apexification
    """
    IMPLANT = "IMPLANT"
    """
    Endosseous implant fixture or abutment
    """
    PROSTHODONTIC = "PROSTHODONTIC"
    """
    Denture base, denture teeth, or framework
    """
    ORTHODONTIC = "ORTHODONTIC"
    """
    Brackets, wires, or bonding of appliances
    """
    PREVENTIVE = "PREVENTIVE"
    """
    Pit and fissure sealant or protective coating
    """
    ADHESIVE = "ADHESIVE"
    """
    Bonding agent or primer
    """
    IMPRESSION = "IMPRESSION"
    """
    Impression or bite registration
    """
    TEMPORARY = "TEMPORARY"
    """
    Provisional restoration or temporary filling
    """
    SURGICAL = "SURGICAL"
    """
    Bone graft, membrane, or other surgical use
    """
    OTHER = "OTHER"
    """
    Other context
    """


class PerformanceMeasureEnum(str, Enum):
    """
    Kind of clinical performance statistic being reported
    """
    SURVIVAL_RATE = "SURVIVAL_RATE"
    """
    Proportion of restorations surviving at a given follow-up
    """
    SUCCESS_RATE = "SUCCESS_RATE"
    """
    Proportion meeting a stricter success criterion (survival without repair or complication)
    """
    ANNUAL_FAILURE_RATE = "ANNUAL_FAILURE_RATE"
    """
    Annual failure rate, percent per year
    """
    MEDIAN_SURVIVAL_TIME = "MEDIAN_SURVIVAL_TIME"
    """
    Median time to failure or replacement
    """
    RETENTION_RATE = "RETENTION_RATE"
    """
    Proportion retained (sealants, veneers, cervical restorations)
    """
    COMPLICATION_RATE = "COMPLICATION_RATE"
    """
    Proportion experiencing a named complication (chipping, secondary caries, fracture)
    """
    OTHER = "OTHER"
    """
    Other measure
    """


class AdverseEffectCategoryEnum(str, Enum):
    """
    Broad category of an adverse effect or safety concern
    """
    ALLERGIC_OR_HYPERSENSITIVITY = "ALLERGIC_OR_HYPERSENSITIVITY"
    """
    Contact allergy, lichenoid reaction, or systemic hypersensitivity
    """
    TOXICITY = "TOXICITY"
    """
    Local or systemic toxicity, including cytotoxicity and leachables
    """
    MECHANICAL_FAILURE = "MECHANICAL_FAILURE"
    """
    Fracture, chipping, debonding, or wear of the restoration
    """
    SECONDARY_CARIES = "SECONDARY_CARIES"
    """
    Recurrent caries at the restoration margin
    """
    PULPAL_RESPONSE = "PULPAL_RESPONSE"
    """
    Pulpal irritation, sensitivity, or necrosis
    """
    PERIODONTAL_RESPONSE = "PERIODONTAL_RESPONSE"
    """
    Gingival or periodontal inflammation adjacent to the material
    """
    ANTAGONIST_WEAR = "ANTAGONIST_WEAR"
    """
    Wear of opposing natural teeth or restorations
    """
    ESTHETIC = "ESTHETIC"
    """
    Discoloration, staining, or shade mismatch
    """
    OCCUPATIONAL = "OCCUPATIONAL"
    """
    Hazard to dental personnel during handling
    """
    ENVIRONMENTAL = "ENVIRONMENTAL"
    """
    Environmental release (e.g. mercury in wastewater)
    """
    OTHER = "OTHER"
    """
    Other
    """


class RegulatoryAgencyEnum(str, Enum):
    """
    The regulator whose decision or classification is being recorded. FDA is the first target; the others are listed so the model does not have to change when they are curated.
    """
    US_Food_and_Drug_Administration = "FDA"
    """
    United States. Dental devices are regulated under 21 CFR part 872 by CDRH.
    """
    European_Union_LEFT_PARENTHESISMDR_2017SOLIDUS745RIGHT_PARENTHESIS = "EU_MDR"
    """
    CE marking under the Medical Device Regulation, via a notified body for class IIa and above.
    """
    Health_Canada = "HEALTH_CANADA"
    UK_Medicines_and_Healthcare_products_Regulatory_Agency = "MHRA"
    Australian_Therapeutic_Goods_Administration = "TGA"
    Japan_Pharmaceuticals_and_Medical_Devices_Agency = "PMDA"
    China_National_Medical_Products_Administration = "NMPA"
    Brazil_Agência_Nacional_de_Vigilância_Sanitária = "ANVISA"
    Other_regulator = "OTHER"


class DeviceClassEnum(str, Enum):
    """
    Risk-based device class. FDA uses I, II, III. The EU MDR uses I, IIa, IIb, III. Record the class as the regulator states it; the agency slot disambiguates the scheme.
    """
    Class_I = "CLASS_I"
    """
    Lowest risk; general controls (FDA) or self-certification (EU)
    """
    Class_IIa = "CLASS_IIA"
    """
    EU MDR medium-low risk
    """
    Class_II = "CLASS_II"
    """
    FDA moderate risk; general and special controls
    """
    Class_IIb = "CLASS_IIB"
    """
    EU MDR medium-high risk
    """
    Class_III = "CLASS_III"
    """
    Highest risk; premarket approval (FDA) or full conformity assessment (EU)
    """
    Unclassified = "UNCLASSIFIED"
    """
    No classification regulation applies or classification not yet determined
    """
    Not_regulated_as_a_device = "NOT_A_DEVICE"
    """
    The material is not regulated as a medical device in this jurisdiction
    """


class RegulatoryPathwayEnum(str, Enum):
    """
    The premarket route by which the material or product reached the market
    """
    number_510LEFT_PARENTHESISkRIGHT_PARENTHESIS_premarket_notification = "PREMARKET_NOTIFICATION_510K"
    """
    FDA clearance by demonstrating substantial equivalence to a predicate device
    """
    Premarket_approval_LEFT_PARENTHESISPMARIGHT_PARENTHESIS = "PREMARKET_APPROVAL_PMA"
    """
    FDA approval of a class III device on its own safety and effectiveness data
    """
    De_Novo_classification = "DE_NOVO"
    """
    FDA pathway for novel low-to-moderate risk devices without a predicate
    """
    number_510LEFT_PARENTHESISkRIGHT_PARENTHESIS_exempt = "EXEMPT_510K"
    """
    Marketed without premarket notification, subject to the limitations of 21 CFR 872.9, but still subject to registration, listing, and general controls
    """
    Humanitarian_device_exemption = "HUMANITARIAN_DEVICE_EXEMPTION"
    Pre_amendment_device = "PRE_AMENDMENT"
    """
    Marketed before the 1976 Medical Device Amendments and grandfathered
    """
    CE_marking = "CE_MARK"
    """
    EU conformity assessment under MDR or the earlier MDD
    """
    Other = "OTHER"


class RegulatoryStatusEnum(str, Enum):
    """
    The current standing of the material or product with the regulator
    """
    CLEARED = "CLEARED"
    """
    Cleared for marketing (FDA 510(k))
    """
    APPROVED = "APPROVED"
    """
    Approved for marketing (FDA PMA, or equivalent)
    """
    GRANTED = "GRANTED"
    """
    De Novo request granted
    """
    EXEMPT = "EXEMPT"
    """
    Exempt from premarket notification; may be marketed under general controls
    """
    CE_MARKED = "CE_MARKED"
    """
    Carries a CE mark under EU device law
    """
    REGISTERED = "REGISTERED"
    """
    Registered or listed with the regulator without a specific marketing decision
    """
    PENDING = "PENDING"
    """
    Submission under review
    """
    RESTRICTED = "RESTRICTED"
    """
    Marketed with use restrictions imposed by the regulator (e.g. population-specific recommendations)
    """
    WITHDRAWN = "WITHDRAWN"
    """
    Withdrawn from the market by the manufacturer
    """
    RECALLED = "RECALLED"
    """
    Subject to a recall
    """
    BANNED = "BANNED"
    """
    Prohibited by the regulator
    """
    NOT_REGULATED = "NOT_REGULATED"
    """
    Not regulated as a device in this jurisdiction
    """
    UNKNOWN = "UNKNOWN"
    """
    Status not yet curated
    """


class CurationStatusEnum(str, Enum):
    """
    How far along this entry is
    """
    STUB = "STUB"
    """
    Seeded from the ontology only; no curated content beyond name, definition, and term
    """
    IN_PROGRESS = "IN_PROGRESS"
    """
    Some sections curated
    """
    CURATED = "CURATED"
    """
    All recommended sections populated with evidence
    """
    REVIEWED = "REVIEWED"
    """
    Curated and reviewed by a domain expert
    """


class MappingPredicateEnum(str, Enum):
    """
    SKOS mapping relation between this material and a term in another vocabulary
    """
    EXACT_MATCH = "EXACT_MATCH"
    CLOSE_MATCH = "CLOSE_MATCH"
    BROAD_MATCH = "BROAD_MATCH"
    NARROW_MATCH = "NARROW_MATCH"
    RELATED_MATCH = "RELATED_MATCH"


class DentalMaterialTerm(str):
    """
    A dental restoration material term from OHD. The root itself is included so the top-of-tree entry validates.
    """
    pass


class DentalProcedureTerm(str):
    """
    A dental procedure term from OHD
    """
    pass


class ChemicalEntityTerm(str):
    """
    A chemical entity from CHEBI
    """
    pass


class AnatomicalEntityTerm(str):
    """
    An anatomical entity from UBERON
    """
    pass


class PhenotypeTerm(str):
    """
    A phenotype (HP) or disease (MONDO) term, for adverse effects
    """
    pass


class QualityTerm(str):
    """
    A quality from PATO, for typed material properties
    """
    pass



class Term(ConfiguredBaseModel):
    """
    A structured reference to an ontology term
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/caufieldjh/dentamech'})

    id: str = Field(default=..., description="""A CURIE identifying an ontology term""", json_schema_extra = { "linkml_meta": {'domain_of': ['Term', 'Mapping'], 'examples': [{'value': 'OHD:0000036'}]} })
    label: str = Field(default=..., description="""The canonical label of the ontology term, as validated against the source ontology""", json_schema_extra = { "linkml_meta": {'domain_of': ['Term', 'Mapping']} })


class Descriptor(ConfiguredBaseModel):
    """
    Base class for a thing described by a preferred term, an optional description, and an optional bound ontology term
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True, 'from_schema': 'https://w3id.org/caufieldjh/dentamech'})

    preferred_term: Optional[str] = Field(default=None, description="""The preferred human-readable term for this descriptor. May be more specific than the bound ontology term's label.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Descriptor']} })
    description: Optional[str] = Field(default=None, description="""Free-text description""", json_schema_extra = { "linkml_meta": {'domain_of': ['Descriptor',
                       'Component',
                       'MaterialProperty',
                       'ClinicalUse',
                       'ClinicalPerformance',
                       'AdverseEffect',
                       'ApprovedUse',
                       'CommercialProduct',
                       'DentalMaterial']} })
    term: Optional[Term] = Field(default=None, description="""Structured ontology term reference""", json_schema_extra = { "linkml_meta": {'domain_of': ['Descriptor'], 'recommended': True} })


class DentalMaterialDescriptor(Descriptor):
    """
    A descriptor bindable to the OHD dental restoration material branch
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/caufieldjh/dentamech',
         'slot_usage': {'term': {'bindings': [{'binds_value_of': 'id',
                                               'obligation_level': 'REQUIRED',
                                               'range': 'DentalMaterialTerm'}],
                                 'name': 'term',
                                 'required': True}}})

    preferred_term: Optional[str] = Field(default=None, description="""The preferred human-readable term for this descriptor. May be more specific than the bound ontology term's label.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Descriptor']} })
    description: Optional[str] = Field(default=None, description="""Free-text description""", json_schema_extra = { "linkml_meta": {'domain_of': ['Descriptor',
                       'Component',
                       'MaterialProperty',
                       'ClinicalUse',
                       'ClinicalPerformance',
                       'AdverseEffect',
                       'ApprovedUse',
                       'CommercialProduct',
                       'DentalMaterial']} })
    term: Term = Field(default=..., description="""Structured ontology term reference""", json_schema_extra = { "linkml_meta": {'bindings': [{'binds_value_of': 'id',
                       'obligation_level': 'REQUIRED',
                       'range': 'DentalMaterialTerm'}],
         'domain_of': ['Descriptor'],
         'recommended': True} })


class DentalProcedureDescriptor(Descriptor):
    """
    A descriptor bindable to the OHD dental procedure branch
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/caufieldjh/dentamech',
         'slot_usage': {'term': {'bindings': [{'binds_value_of': 'id',
                                               'obligation_level': 'REQUIRED',
                                               'range': 'DentalProcedureTerm'}],
                                 'name': 'term'}}})

    preferred_term: Optional[str] = Field(default=None, description="""The preferred human-readable term for this descriptor. May be more specific than the bound ontology term's label.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Descriptor']} })
    description: Optional[str] = Field(default=None, description="""Free-text description""", json_schema_extra = { "linkml_meta": {'domain_of': ['Descriptor',
                       'Component',
                       'MaterialProperty',
                       'ClinicalUse',
                       'ClinicalPerformance',
                       'AdverseEffect',
                       'ApprovedUse',
                       'CommercialProduct',
                       'DentalMaterial']} })
    term: Optional[Term] = Field(default=None, description="""Structured ontology term reference""", json_schema_extra = { "linkml_meta": {'bindings': [{'binds_value_of': 'id',
                       'obligation_level': 'REQUIRED',
                       'range': 'DentalProcedureTerm'}],
         'domain_of': ['Descriptor'],
         'recommended': True} })


class ChemicalEntityDescriptor(Descriptor):
    """
    A descriptor bindable to CHEBI
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/caufieldjh/dentamech',
         'slot_usage': {'term': {'bindings': [{'binds_value_of': 'id',
                                               'obligation_level': 'REQUIRED',
                                               'range': 'ChemicalEntityTerm'}],
                                 'name': 'term'}}})

    preferred_term: Optional[str] = Field(default=None, description="""The preferred human-readable term for this descriptor. May be more specific than the bound ontology term's label.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Descriptor']} })
    description: Optional[str] = Field(default=None, description="""Free-text description""", json_schema_extra = { "linkml_meta": {'domain_of': ['Descriptor',
                       'Component',
                       'MaterialProperty',
                       'ClinicalUse',
                       'ClinicalPerformance',
                       'AdverseEffect',
                       'ApprovedUse',
                       'CommercialProduct',
                       'DentalMaterial']} })
    term: Optional[Term] = Field(default=None, description="""Structured ontology term reference""", json_schema_extra = { "linkml_meta": {'bindings': [{'binds_value_of': 'id',
                       'obligation_level': 'REQUIRED',
                       'range': 'ChemicalEntityTerm'}],
         'domain_of': ['Descriptor'],
         'recommended': True} })


class AnatomicalEntityDescriptor(Descriptor):
    """
    A descriptor bindable to UBERON
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/caufieldjh/dentamech',
         'slot_usage': {'term': {'bindings': [{'binds_value_of': 'id',
                                               'obligation_level': 'REQUIRED',
                                               'range': 'AnatomicalEntityTerm'}],
                                 'name': 'term'}}})

    preferred_term: Optional[str] = Field(default=None, description="""The preferred human-readable term for this descriptor. May be more specific than the bound ontology term's label.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Descriptor']} })
    description: Optional[str] = Field(default=None, description="""Free-text description""", json_schema_extra = { "linkml_meta": {'domain_of': ['Descriptor',
                       'Component',
                       'MaterialProperty',
                       'ClinicalUse',
                       'ClinicalPerformance',
                       'AdverseEffect',
                       'ApprovedUse',
                       'CommercialProduct',
                       'DentalMaterial']} })
    term: Optional[Term] = Field(default=None, description="""Structured ontology term reference""", json_schema_extra = { "linkml_meta": {'bindings': [{'binds_value_of': 'id',
                       'obligation_level': 'REQUIRED',
                       'range': 'AnatomicalEntityTerm'}],
         'domain_of': ['Descriptor'],
         'recommended': True} })


class PhenotypeDescriptor(Descriptor):
    """
    A descriptor bindable to HP or MONDO
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/caufieldjh/dentamech',
         'slot_usage': {'term': {'bindings': [{'binds_value_of': 'id',
                                               'obligation_level': 'REQUIRED',
                                               'range': 'PhenotypeTerm'}],
                                 'name': 'term'}}})

    preferred_term: Optional[str] = Field(default=None, description="""The preferred human-readable term for this descriptor. May be more specific than the bound ontology term's label.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Descriptor']} })
    description: Optional[str] = Field(default=None, description="""Free-text description""", json_schema_extra = { "linkml_meta": {'domain_of': ['Descriptor',
                       'Component',
                       'MaterialProperty',
                       'ClinicalUse',
                       'ClinicalPerformance',
                       'AdverseEffect',
                       'ApprovedUse',
                       'CommercialProduct',
                       'DentalMaterial']} })
    term: Optional[Term] = Field(default=None, description="""Structured ontology term reference""", json_schema_extra = { "linkml_meta": {'bindings': [{'binds_value_of': 'id',
                       'obligation_level': 'REQUIRED',
                       'range': 'PhenotypeTerm'}],
         'domain_of': ['Descriptor'],
         'recommended': True} })


class QualityDescriptor(Descriptor):
    """
    A descriptor bindable to PATO
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/caufieldjh/dentamech',
         'slot_usage': {'term': {'bindings': [{'binds_value_of': 'id',
                                               'obligation_level': 'REQUIRED',
                                               'range': 'QualityTerm'}],
                                 'name': 'term'}}})

    preferred_term: Optional[str] = Field(default=None, description="""The preferred human-readable term for this descriptor. May be more specific than the bound ontology term's label.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Descriptor']} })
    description: Optional[str] = Field(default=None, description="""Free-text description""", json_schema_extra = { "linkml_meta": {'domain_of': ['Descriptor',
                       'Component',
                       'MaterialProperty',
                       'ClinicalUse',
                       'ClinicalPerformance',
                       'AdverseEffect',
                       'ApprovedUse',
                       'CommercialProduct',
                       'DentalMaterial']} })
    term: Optional[Term] = Field(default=None, description="""Structured ontology term reference""", json_schema_extra = { "linkml_meta": {'bindings': [{'binds_value_of': 'id',
                       'obligation_level': 'REQUIRED',
                       'range': 'QualityTerm'}],
         'domain_of': ['Descriptor'],
         'recommended': True} })


class EvidenceItem(ConfiguredBaseModel):
    """
    A citation plus an exact quote, tied to the claim it sits under
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/caufieldjh/dentamech'})

    reference: str = Field(default=..., description="""The citable source for this evidence item""", json_schema_extra = { "linkml_meta": {'domain_of': ['EvidenceItem'],
         'examples': [{'value': 'PMID:24560216'},
                      {'value': 'url:https://www.ecfr.gov/current/title-21/section-872.3690'}],
         'implements': ['linkml:authoritative_reference']} })
    reference_title: Optional[str] = Field(default=None, description="""Title of the referenced source""", json_schema_extra = { "linkml_meta": {'domain_of': ['EvidenceItem'], 'recommended': True} })
    supports: EvidenceItemSupportEnum = Field(default=..., description="""How the source relates to the claim""", json_schema_extra = { "linkml_meta": {'domain_of': ['EvidenceItem']} })
    evidence_source: Optional[EvidenceSourceEnum] = Field(default=None, description="""The kind of source""", json_schema_extra = { "linkml_meta": {'domain_of': ['EvidenceItem'], 'recommended': True} })
    snippet: Optional[str] = Field(default=None, description="""An exact quote from the referenced source that supports or refutes the claim. Validated verbatim against the fetched abstract or document by linkml-reference-validator where the source can be fetched.""", json_schema_extra = { "linkml_meta": {'domain_of': ['EvidenceItem'], 'implements': ['linkml:excerpt']} })
    explanation: Optional[str] = Field(default=None, description="""Why this snippet bears on the claim""", json_schema_extra = { "linkml_meta": {'domain_of': ['EvidenceItem']} })


class Mapping(ConfiguredBaseModel):
    """
    A mapping to a term in another vocabulary
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/caufieldjh/dentamech'})

    id: str = Field(default=..., description="""A CURIE identifying an ontology term""", json_schema_extra = { "linkml_meta": {'domain_of': ['Term', 'Mapping'], 'examples': [{'value': 'OHD:0000036'}]} })
    label: str = Field(default=..., description="""The canonical label of the ontology term, as validated against the source ontology""", json_schema_extra = { "linkml_meta": {'domain_of': ['Term', 'Mapping']} })
    predicate: MappingPredicateEnum = Field(default=..., description="""SKOS mapping relation""", json_schema_extra = { "linkml_meta": {'domain_of': ['Mapping']} })
    source: Optional[str] = Field(default=None, description="""Where the mapping or record came from""", json_schema_extra = { "linkml_meta": {'domain_of': ['Mapping']} })


class Component(ConfiguredBaseModel):
    """
    A constituent of the material
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/caufieldjh/dentamech',
         'slot_usage': {'name': {'identifier': False,
                                 'name': 'name',
                                 'required': True}}})

    name: str = Field(default=..., description="""Human-readable name; the identifier for top-level entries""", json_schema_extra = { "linkml_meta": {'domain_of': ['Component',
                       'MaterialProperty',
                       'ClinicalUse',
                       'ClinicalPerformance',
                       'AdverseEffect',
                       'ApprovedUse',
                       'CommercialProduct',
                       'DentalMaterial'],
         'examples': [{'value': 'Resin-based composite'}]} })
    description: Optional[str] = Field(default=None, description="""Free-text description""", json_schema_extra = { "linkml_meta": {'domain_of': ['Descriptor',
                       'Component',
                       'MaterialProperty',
                       'ClinicalUse',
                       'ClinicalPerformance',
                       'AdverseEffect',
                       'ApprovedUse',
                       'CommercialProduct',
                       'DentalMaterial']} })
    role: Optional[ComponentRoleEnum] = Field(default=None, description="""Functional role of the component in the formulation""", json_schema_extra = { "linkml_meta": {'domain_of': ['Component']} })
    chemical: Optional[ChemicalEntityDescriptor] = Field(default=None, description="""Chemical identity of the component, bound to CHEBI where possible""", json_schema_extra = { "linkml_meta": {'domain_of': ['Component']} })
    proportion: Optional[str] = Field(default=None, description="""Typical proportion of this component, as free text so ranges and bases (weight or volume percent) can be stated as the source states them""", json_schema_extra = { "linkml_meta": {'domain_of': ['Component'], 'examples': [{'value': '60-80 wt%'}]} })
    evidence: Optional[list[EvidenceItem]] = Field(default=None, description="""Evidence items supporting or refuting the enclosing claim""", json_schema_extra = { "linkml_meta": {'domain_of': ['Component',
                       'MaterialProperty',
                       'ClinicalUse',
                       'ClinicalPerformance',
                       'AdverseEffect',
                       'ApprovedUse',
                       'RegulatoryStatus',
                       'RegulatorySubmission'],
         'recommended': True} })


class MaterialProperty(ConfiguredBaseModel):
    """
    A reported property value
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/caufieldjh/dentamech',
         'slot_usage': {'name': {'description': 'Short label for the property row '
                                                '(e.g. "Flexural strength, 24 h water '
                                                'storage")',
                                 'identifier': False,
                                 'name': 'name'}}})

    name: Optional[str] = Field(default=None, description="""Short label for the property row (e.g. \"Flexural strength, 24 h water storage\")""", json_schema_extra = { "linkml_meta": {'domain_of': ['Component',
                       'MaterialProperty',
                       'ClinicalUse',
                       'ClinicalPerformance',
                       'AdverseEffect',
                       'ApprovedUse',
                       'CommercialProduct',
                       'DentalMaterial'],
         'examples': [{'value': 'Resin-based composite'}]} })
    property_type: PropertyTypeEnum = Field(default=..., description="""Which property is being reported""", json_schema_extra = { "linkml_meta": {'domain_of': ['MaterialProperty']} })
    quality_term: Optional[QualityDescriptor] = Field(default=None, description="""Optional PATO quality term for the property""", json_schema_extra = { "linkml_meta": {'domain_of': ['MaterialProperty']} })
    value: Optional[str] = Field(default=None, description="""Reported value, as a number or a free-text range""", json_schema_extra = { "linkml_meta": {'domain_of': ['MaterialProperty', 'ClinicalPerformance']} })
    unit: Optional[str] = Field(default=None, description="""Unit for the value""", json_schema_extra = { "linkml_meta": {'domain_of': ['MaterialProperty', 'ClinicalPerformance'],
         'examples': [{'value': 'MPa'}]} })
    test_method: Optional[str] = Field(default=None, description="""Standard or method used to measure the property""", json_schema_extra = { "linkml_meta": {'domain_of': ['MaterialProperty'],
         'examples': [{'value': 'ISO 4049:2019 three-point bending'}]} })
    conditions: Optional[str] = Field(default=None, description="""Test or storage conditions that qualify the value""", json_schema_extra = { "linkml_meta": {'domain_of': ['MaterialProperty']} })
    description: Optional[str] = Field(default=None, description="""Free-text description""", json_schema_extra = { "linkml_meta": {'domain_of': ['Descriptor',
                       'Component',
                       'MaterialProperty',
                       'ClinicalUse',
                       'ClinicalPerformance',
                       'AdverseEffect',
                       'ApprovedUse',
                       'CommercialProduct',
                       'DentalMaterial']} })
    evidence: Optional[list[EvidenceItem]] = Field(default=None, description="""Evidence items supporting or refuting the enclosing claim""", json_schema_extra = { "linkml_meta": {'domain_of': ['Component',
                       'MaterialProperty',
                       'ClinicalUse',
                       'ClinicalPerformance',
                       'AdverseEffect',
                       'ApprovedUse',
                       'RegulatoryStatus',
                       'RegulatorySubmission'],
         'recommended': True} })


class ClinicalUse(ConfiguredBaseModel):
    """
    A clinical application of the material
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/caufieldjh/dentamech',
         'slot_usage': {'name': {'identifier': False,
                                 'name': 'name',
                                 'required': True}}})

    name: str = Field(default=..., description="""Human-readable name; the identifier for top-level entries""", json_schema_extra = { "linkml_meta": {'domain_of': ['Component',
                       'MaterialProperty',
                       'ClinicalUse',
                       'ClinicalPerformance',
                       'AdverseEffect',
                       'ApprovedUse',
                       'CommercialProduct',
                       'DentalMaterial'],
         'examples': [{'value': 'Resin-based composite'}]} })
    description: Optional[str] = Field(default=None, description="""Free-text description""", json_schema_extra = { "linkml_meta": {'domain_of': ['Descriptor',
                       'Component',
                       'MaterialProperty',
                       'ClinicalUse',
                       'ClinicalPerformance',
                       'AdverseEffect',
                       'ApprovedUse',
                       'CommercialProduct',
                       'DentalMaterial']} })
    use_context: ClinicalUseContextEnum = Field(default=..., description="""Broad clinical context""", json_schema_extra = { "linkml_meta": {'domain_of': ['ClinicalUse', 'ApprovedUse']} })
    procedure: Optional[DentalProcedureDescriptor] = Field(default=None, description="""The OHD dental procedure this use corresponds to""", json_schema_extra = { "linkml_meta": {'domain_of': ['ClinicalUse', 'ApprovedUse']} })
    anatomical_site: Optional[AnatomicalEntityDescriptor] = Field(default=None, description="""Where in the mouth the material is placed""", json_schema_extra = { "linkml_meta": {'domain_of': ['ClinicalUse', 'ApprovedUse']} })
    indications: Optional[list[str]] = Field(default=None, description="""Situations in which this use is indicated""", json_schema_extra = { "linkml_meta": {'domain_of': ['ClinicalUse']} })
    contraindications: Optional[list[str]] = Field(default=None, description="""Situations in which this use is contraindicated""", json_schema_extra = { "linkml_meta": {'domain_of': ['ClinicalUse']} })
    evidence: Optional[list[EvidenceItem]] = Field(default=None, description="""Evidence items supporting or refuting the enclosing claim""", json_schema_extra = { "linkml_meta": {'domain_of': ['Component',
                       'MaterialProperty',
                       'ClinicalUse',
                       'ClinicalPerformance',
                       'AdverseEffect',
                       'ApprovedUse',
                       'RegulatoryStatus',
                       'RegulatorySubmission'],
         'recommended': True} })


class ClinicalPerformance(ConfiguredBaseModel):
    """
    A longevity or outcome statistic
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/caufieldjh/dentamech',
         'slot_usage': {'name': {'identifier': False,
                                 'name': 'name',
                                 'required': True}}})

    name: str = Field(default=..., description="""Human-readable name; the identifier for top-level entries""", json_schema_extra = { "linkml_meta": {'domain_of': ['Component',
                       'MaterialProperty',
                       'ClinicalUse',
                       'ClinicalPerformance',
                       'AdverseEffect',
                       'ApprovedUse',
                       'CommercialProduct',
                       'DentalMaterial'],
         'examples': [{'value': 'Resin-based composite'}]} })
    measure_type: PerformanceMeasureEnum = Field(default=..., description="""Which performance statistic is being reported""", json_schema_extra = { "linkml_meta": {'domain_of': ['ClinicalPerformance']} })
    value: Optional[str] = Field(default=None, description="""Reported value, as a number or a free-text range""", json_schema_extra = { "linkml_meta": {'domain_of': ['MaterialProperty', 'ClinicalPerformance']} })
    unit: Optional[str] = Field(default=None, description="""Unit for the value""", json_schema_extra = { "linkml_meta": {'domain_of': ['MaterialProperty', 'ClinicalPerformance'],
         'examples': [{'value': 'MPa'}]} })
    follow_up_years: Optional[float] = Field(default=None, description="""Follow-up duration in years""", json_schema_extra = { "linkml_meta": {'domain_of': ['ClinicalPerformance']} })
    population: Optional[str] = Field(default=None, description="""The population or setting the statistic applies to""", json_schema_extra = { "linkml_meta": {'domain_of': ['ClinicalPerformance']} })
    comparator: Optional[str] = Field(default=None, description="""The material or treatment it was compared against, if any""", json_schema_extra = { "linkml_meta": {'domain_of': ['ClinicalPerformance']} })
    description: Optional[str] = Field(default=None, description="""Free-text description""", json_schema_extra = { "linkml_meta": {'domain_of': ['Descriptor',
                       'Component',
                       'MaterialProperty',
                       'ClinicalUse',
                       'ClinicalPerformance',
                       'AdverseEffect',
                       'ApprovedUse',
                       'CommercialProduct',
                       'DentalMaterial']} })
    evidence: Optional[list[EvidenceItem]] = Field(default=None, description="""Evidence items supporting or refuting the enclosing claim""", json_schema_extra = { "linkml_meta": {'domain_of': ['Component',
                       'MaterialProperty',
                       'ClinicalUse',
                       'ClinicalPerformance',
                       'AdverseEffect',
                       'ApprovedUse',
                       'RegulatoryStatus',
                       'RegulatorySubmission'],
         'recommended': True} })


class AdverseEffect(ConfiguredBaseModel):
    """
    An adverse effect, safety concern, or failure mode
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/caufieldjh/dentamech',
         'slot_usage': {'name': {'identifier': False,
                                 'name': 'name',
                                 'required': True}}})

    name: str = Field(default=..., description="""Human-readable name; the identifier for top-level entries""", json_schema_extra = { "linkml_meta": {'domain_of': ['Component',
                       'MaterialProperty',
                       'ClinicalUse',
                       'ClinicalPerformance',
                       'AdverseEffect',
                       'ApprovedUse',
                       'CommercialProduct',
                       'DentalMaterial'],
         'examples': [{'value': 'Resin-based composite'}]} })
    description: Optional[str] = Field(default=None, description="""Free-text description""", json_schema_extra = { "linkml_meta": {'domain_of': ['Descriptor',
                       'Component',
                       'MaterialProperty',
                       'ClinicalUse',
                       'ClinicalPerformance',
                       'AdverseEffect',
                       'ApprovedUse',
                       'CommercialProduct',
                       'DentalMaterial']} })
    effect_category: AdverseEffectCategoryEnum = Field(default=..., description="""Broad category of the adverse effect""", json_schema_extra = { "linkml_meta": {'domain_of': ['AdverseEffect']} })
    effect_term: Optional[PhenotypeDescriptor] = Field(default=None, description="""The phenotype or disease the effect corresponds to""", json_schema_extra = { "linkml_meta": {'domain_of': ['AdverseEffect']} })
    frequency: Optional[str] = Field(default=None, description="""How often the effect occurs, as stated by the source""", json_schema_extra = { "linkml_meta": {'domain_of': ['AdverseEffect']} })
    evidence: Optional[list[EvidenceItem]] = Field(default=None, description="""Evidence items supporting or refuting the enclosing claim""", json_schema_extra = { "linkml_meta": {'domain_of': ['Component',
                       'MaterialProperty',
                       'ClinicalUse',
                       'ClinicalPerformance',
                       'AdverseEffect',
                       'ApprovedUse',
                       'RegulatoryStatus',
                       'RegulatorySubmission'],
         'recommended': True} })


class ApprovedUse(ConfiguredBaseModel):
    """
    A use the regulator permits for this device type or product
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/caufieldjh/dentamech',
         'slot_usage': {'name': {'identifier': False, 'name': 'name', 'required': True},
                        'use_context': {'name': 'use_context', 'required': False}}})

    name: str = Field(default=..., description="""Human-readable name; the identifier for top-level entries""", json_schema_extra = { "linkml_meta": {'domain_of': ['Component',
                       'MaterialProperty',
                       'ClinicalUse',
                       'ClinicalPerformance',
                       'AdverseEffect',
                       'ApprovedUse',
                       'CommercialProduct',
                       'DentalMaterial'],
         'examples': [{'value': 'Resin-based composite'}]} })
    description: Optional[str] = Field(default=None, description="""Free-text description""", json_schema_extra = { "linkml_meta": {'domain_of': ['Descriptor',
                       'Component',
                       'MaterialProperty',
                       'ClinicalUse',
                       'ClinicalPerformance',
                       'AdverseEffect',
                       'ApprovedUse',
                       'CommercialProduct',
                       'DentalMaterial']} })
    use_context: Optional[ClinicalUseContextEnum] = Field(default=None, description="""Broad clinical context""", json_schema_extra = { "linkml_meta": {'domain_of': ['ClinicalUse', 'ApprovedUse']} })
    procedure: Optional[DentalProcedureDescriptor] = Field(default=None, description="""The OHD dental procedure this use corresponds to""", json_schema_extra = { "linkml_meta": {'domain_of': ['ClinicalUse', 'ApprovedUse']} })
    anatomical_site: Optional[AnatomicalEntityDescriptor] = Field(default=None, description="""Where in the mouth the material is placed""", json_schema_extra = { "linkml_meta": {'domain_of': ['ClinicalUse', 'ApprovedUse']} })
    evidence: Optional[list[EvidenceItem]] = Field(default=None, description="""Evidence items supporting or refuting the enclosing claim""", json_schema_extra = { "linkml_meta": {'domain_of': ['Component',
                       'MaterialProperty',
                       'ClinicalUse',
                       'ClinicalPerformance',
                       'AdverseEffect',
                       'ApprovedUse',
                       'RegulatoryStatus',
                       'RegulatorySubmission'],
         'recommended': True} })


class RegulatoryStatus(ConfiguredBaseModel):
    """
    Regulatory classification of the material as a device type, under one agency and one regulation
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/caufieldjh/dentamech'})

    agency: RegulatoryAgencyEnum = Field(default=..., description="""The regulator""", json_schema_extra = { "linkml_meta": {'domain_of': ['RegulatoryStatus', 'RegulatorySubmission']} })
    jurisdiction: Optional[str] = Field(default=None, description="""Country or region, when the agency slot alone is ambiguous""", json_schema_extra = { "linkml_meta": {'domain_of': ['RegulatoryStatus']} })
    status: RegulatoryStatusEnum = Field(default=..., description="""Current standing with the regulator""", json_schema_extra = { "linkml_meta": {'domain_of': ['RegulatoryStatus']} })
    regulation_number: Optional[str] = Field(default=None, description="""The classification regulation. For FDA this is a section of 21 CFR part 872, written as e.g. 872.3690.""", json_schema_extra = { "linkml_meta": {'domain_of': ['RegulatoryStatus', 'RegulatorySubmission'],
         'examples': [{'value': '872.3690'}]} })
    regulation_title: Optional[str] = Field(default=None, description="""Device name as given in the classification regulation""", json_schema_extra = { "linkml_meta": {'domain_of': ['RegulatoryStatus'],
         'examples': [{'value': 'Tooth shade resin material'}]} })
    device_class: Optional[DeviceClassEnum] = Field(default=None, description="""Risk class assigned by the regulator""", json_schema_extra = { "linkml_meta": {'domain_of': ['RegulatoryStatus']} })
    product_codes: Optional[list[str]] = Field(default=None, description="""FDA three-letter product codes (or the equivalent classification codes of another agency) that fall under this regulation for this material""", json_schema_extra = { "linkml_meta": {'domain_of': ['RegulatoryStatus'], 'examples': [{'value': 'EBF'}]} })
    pathways: Optional[list[RegulatoryPathwayEnum]] = Field(default=None, description="""Premarket routes available or used for this device type""", json_schema_extra = { "linkml_meta": {'domain_of': ['RegulatoryStatus']} })
    special_controls: Optional[list[str]] = Field(default=None, description="""Special controls or guidance documents named in the regulation""", json_schema_extra = { "linkml_meta": {'domain_of': ['RegulatoryStatus']} })
    identification: Optional[str] = Field(default=None, description="""The regulator's own identification text for the device type, quoted verbatim. For FDA this is paragraph (a) of the regulation.""", json_schema_extra = { "linkml_meta": {'domain_of': ['RegulatoryStatus']} })
    approved_uses: Optional[list[ApprovedUse]] = Field(default=None, description="""Uses the regulator permits, as stated in the regulation, clearance, or approval""", json_schema_extra = { "linkml_meta": {'domain_of': ['RegulatoryStatus']} })
    restrictions: Optional[list[str]] = Field(default=None, description="""Population, labeling, or use restrictions imposed by the regulator""", json_schema_extra = { "linkml_meta": {'domain_of': ['RegulatoryStatus']} })
    effective_date: Optional[date] = Field(default=None, description="""Date the classification or decision took effect (YYYY-MM-DD)""", json_schema_extra = { "linkml_meta": {'domain_of': ['RegulatoryStatus']} })
    source_url: Optional[str] = Field(default=None, description="""URL of the regulation, database record, or decision document""", json_schema_extra = { "linkml_meta": {'domain_of': ['RegulatoryStatus', 'RegulatorySubmission']} })
    notes: Optional[str] = Field(default=None, description="""Curator notes that do not belong in any structured section""", json_schema_extra = { "linkml_meta": {'domain_of': ['RegulatoryStatus', 'DentalMaterial']} })
    evidence: Optional[list[EvidenceItem]] = Field(default=None, description="""Evidence items supporting or refuting the enclosing claim""", json_schema_extra = { "linkml_meta": {'domain_of': ['Component',
                       'MaterialProperty',
                       'ClinicalUse',
                       'ClinicalPerformance',
                       'AdverseEffect',
                       'ApprovedUse',
                       'RegulatoryStatus',
                       'RegulatorySubmission'],
         'recommended': True} })

    @field_validator('regulation_number')
    def pattern_regulation_number(cls, v):
        pattern=re.compile(r"^\d{3}\.\d{4}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid regulation_number format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid regulation_number format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('product_codes')
    def pattern_product_codes(cls, v):
        pattern=re.compile(r"^[A-Z]{3}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid product_codes format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid product_codes format: {v}"
            raise ValueError(err_msg)
        return v


class RegulatorySubmission(ConfiguredBaseModel):
    """
    One premarket submission for a commercial product and its outcome
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/caufieldjh/dentamech'})

    agency: RegulatoryAgencyEnum = Field(default=..., description="""The regulator""", json_schema_extra = { "linkml_meta": {'domain_of': ['RegulatoryStatus', 'RegulatorySubmission']} })
    submission_number: Optional[str] = Field(default=None, description="""Submission identifier. FDA 510(k) numbers start with K, PMAs with P, De Novo requests with DEN.""", json_schema_extra = { "linkml_meta": {'domain_of': ['RegulatorySubmission'], 'examples': [{'value': 'K123456'}]} })
    pathway: Optional[RegulatoryPathwayEnum] = Field(default=None, description="""Premarket route for this submission""", json_schema_extra = { "linkml_meta": {'domain_of': ['RegulatorySubmission']} })
    decision: Optional[RegulatoryStatusEnum] = Field(default=None, description="""Outcome of the submission""", json_schema_extra = { "linkml_meta": {'domain_of': ['RegulatorySubmission']} })
    decision_date: Optional[date] = Field(default=None, description="""Date of the decision (YYYY-MM-DD)""", json_schema_extra = { "linkml_meta": {'domain_of': ['RegulatorySubmission']} })
    product_code: Optional[str] = Field(default=None, description="""FDA product code assigned to this submission""", json_schema_extra = { "linkml_meta": {'domain_of': ['RegulatorySubmission']} })
    regulation_number: Optional[str] = Field(default=None, description="""The classification regulation. For FDA this is a section of 21 CFR part 872, written as e.g. 872.3690.""", json_schema_extra = { "linkml_meta": {'domain_of': ['RegulatoryStatus', 'RegulatorySubmission'],
         'examples': [{'value': '872.3690'}]} })
    indications_for_use: Optional[str] = Field(default=None, description="""Indications for use statement, quoted from the decision document""", json_schema_extra = { "linkml_meta": {'domain_of': ['RegulatorySubmission']} })
    source_url: Optional[str] = Field(default=None, description="""URL of the regulation, database record, or decision document""", json_schema_extra = { "linkml_meta": {'domain_of': ['RegulatoryStatus', 'RegulatorySubmission']} })
    evidence: Optional[list[EvidenceItem]] = Field(default=None, description="""Evidence items supporting or refuting the enclosing claim""", json_schema_extra = { "linkml_meta": {'domain_of': ['Component',
                       'MaterialProperty',
                       'ClinicalUse',
                       'ClinicalPerformance',
                       'AdverseEffect',
                       'ApprovedUse',
                       'RegulatoryStatus',
                       'RegulatorySubmission'],
         'recommended': True} })

    @field_validator('submission_number')
    def pattern_submission_number(cls, v):
        pattern=re.compile(r"^(K|P|DEN|N|H|BK)\d{6}(?:/S\d{3})?$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid submission_number format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid submission_number format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('product_code')
    def pattern_product_code(cls, v):
        pattern=re.compile(r"^[A-Z]{3}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid product_code format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid product_code format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('regulation_number')
    def pattern_regulation_number(cls, v):
        pattern=re.compile(r"^\d{3}\.\d{4}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid regulation_number format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid regulation_number format: {v}"
            raise ValueError(err_msg)
        return v


class CommercialProduct(ConfiguredBaseModel):
    """
    A branded product that is an instance of this material type
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/caufieldjh/dentamech',
         'slot_usage': {'name': {'identifier': False,
                                 'name': 'name',
                                 'required': True}}})

    name: str = Field(default=..., description="""Human-readable name; the identifier for top-level entries""", json_schema_extra = { "linkml_meta": {'domain_of': ['Component',
                       'MaterialProperty',
                       'ClinicalUse',
                       'ClinicalPerformance',
                       'AdverseEffect',
                       'ApprovedUse',
                       'CommercialProduct',
                       'DentalMaterial'],
         'examples': [{'value': 'Resin-based composite'}]} })
    manufacturer: Optional[str] = Field(default=None, description="""Manufacturer or applicant""", json_schema_extra = { "linkml_meta": {'domain_of': ['CommercialProduct']} })
    description: Optional[str] = Field(default=None, description="""Free-text description""", json_schema_extra = { "linkml_meta": {'domain_of': ['Descriptor',
                       'Component',
                       'MaterialProperty',
                       'ClinicalUse',
                       'ClinicalPerformance',
                       'AdverseEffect',
                       'ApprovedUse',
                       'CommercialProduct',
                       'DentalMaterial']} })
    submissions: Optional[list[RegulatorySubmission]] = Field(default=None, description="""Regulatory submissions and decisions for the product""", json_schema_extra = { "linkml_meta": {'domain_of': ['CommercialProduct']} })
    see_also: Optional[list[str]] = Field(default=None, description="""URLs for further reading""", json_schema_extra = { "linkml_meta": {'domain_of': ['CommercialProduct', 'DentalMaterial']} })


class Standard(ConfiguredBaseModel):
    """
    A technical standard or specification
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/caufieldjh/dentamech'})

    identifier: str = Field(default=..., description="""Standard designation""", json_schema_extra = { "linkml_meta": {'domain_of': ['Standard'], 'examples': [{'value': 'ISO 4049:2019'}]} })
    title: Optional[str] = Field(default=None, description="""Title of the standard""", json_schema_extra = { "linkml_meta": {'domain_of': ['Standard']} })
    organization: Optional[str] = Field(default=None, description="""Standards body""", json_schema_extra = { "linkml_meta": {'domain_of': ['Standard'], 'examples': [{'value': 'ISO'}]} })
    url: Optional[str] = Field(default=None, description="""URL""", json_schema_extra = { "linkml_meta": {'domain_of': ['Standard']} })


class DentalMaterial(ConfiguredBaseModel):
    """
    A dental material entry. One file per material in kb/materials/, anchored to an OHD term.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/caufieldjh/dentamech', 'tree_root': True})

    name: str = Field(default=..., description="""Human-readable name; the identifier for top-level entries""", json_schema_extra = { "linkml_meta": {'domain_of': ['Component',
                       'MaterialProperty',
                       'ClinicalUse',
                       'ClinicalPerformance',
                       'AdverseEffect',
                       'ApprovedUse',
                       'CommercialProduct',
                       'DentalMaterial'],
         'examples': [{'value': 'Resin-based composite'}]} })
    description: Optional[str] = Field(default=None, description="""Free-text description""", json_schema_extra = { "linkml_meta": {'domain_of': ['Descriptor',
                       'Component',
                       'MaterialProperty',
                       'ClinicalUse',
                       'ClinicalPerformance',
                       'AdverseEffect',
                       'ApprovedUse',
                       'CommercialProduct',
                       'DentalMaterial']} })
    creation_date: Optional[str] = Field(default=None, description="""ISO 8601 timestamp for when this entry was first created""", json_schema_extra = { "linkml_meta": {'domain_of': ['DentalMaterial'], 'recommended': True} })
    curation_status: Optional[CurationStatusEnum] = Field(default=None, description="""How far along this entry is""", json_schema_extra = { "linkml_meta": {'domain_of': ['DentalMaterial'], 'recommended': True} })
    material_term: DentalMaterialDescriptor = Field(default=..., description="""The OHD term this material entry is anchored to""", json_schema_extra = { "linkml_meta": {'domain_of': ['DentalMaterial']} })
    category: MaterialCategoryEnum = Field(default=..., description="""Broad material class""", json_schema_extra = { "linkml_meta": {'domain_of': ['DentalMaterial']} })
    parents: Optional[list[str]] = Field(default=None, description="""Names of the parent material entries in this knowledge base. Mirrors the OHD subclass hierarchy. Each value must match the `name` of another file in kb/materials/.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DentalMaterial']} })
    synonyms: Optional[list[str]] = Field(default=None, description="""Alternative names, including common clinical shorthand""", json_schema_extra = { "linkml_meta": {'domain_of': ['DentalMaterial'], 'examples': [{'value': 'GIC'}]} })
    mappings: Optional[list[Mapping]] = Field(default=None, description="""Mappings to terms in other vocabularies (NCIT, SNOMED CT, MeSH, CDT)""", json_schema_extra = { "linkml_meta": {'domain_of': ['DentalMaterial']} })
    setting_mechanisms: Optional[list[SettingMechanismEnum]] = Field(default=None, description="""How the material hardens or is formed""", json_schema_extra = { "linkml_meta": {'domain_of': ['DentalMaterial'], 'recommended': True} })
    composition: Optional[list[Component]] = Field(default=None, description="""Components of the material and their roles""", json_schema_extra = { "linkml_meta": {'domain_of': ['DentalMaterial'], 'recommended': True} })
    properties: Optional[list[MaterialProperty]] = Field(default=None, description="""Measured or typical physical, mechanical, chemical, and biological properties""", json_schema_extra = { "linkml_meta": {'domain_of': ['DentalMaterial']} })
    clinical_uses: Optional[list[ClinicalUse]] = Field(default=None, description="""What the material is used for clinically""", json_schema_extra = { "linkml_meta": {'domain_of': ['DentalMaterial'], 'recommended': True} })
    clinical_performance: Optional[list[ClinicalPerformance]] = Field(default=None, description="""Longevity and outcome statistics from clinical studies""", json_schema_extra = { "linkml_meta": {'domain_of': ['DentalMaterial']} })
    adverse_effects: Optional[list[AdverseEffect]] = Field(default=None, description="""Adverse effects, safety concerns, and failure modes""", json_schema_extra = { "linkml_meta": {'domain_of': ['DentalMaterial']} })
    regulatory_status: Optional[list[RegulatoryStatus]] = Field(default=None, description="""Regulatory classification and permitted uses at the level of the material or device type. One entry per agency (and per regulation when a material falls under more than one). Product-level decisions (a specific 510(k) for a specific brand) go under `products`.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DentalMaterial'], 'recommended': True} })
    products: Optional[list[CommercialProduct]] = Field(default=None, description="""Specific commercial products of this material type, with their regulatory submissions""", json_schema_extra = { "linkml_meta": {'domain_of': ['DentalMaterial']} })
    standards: Optional[list[Standard]] = Field(default=None, description="""Technical standards the material is tested or specified against""", json_schema_extra = { "linkml_meta": {'domain_of': ['DentalMaterial']} })
    see_also: Optional[list[str]] = Field(default=None, description="""URLs for further reading""", json_schema_extra = { "linkml_meta": {'domain_of': ['CommercialProduct', 'DentalMaterial']} })
    notes: Optional[str] = Field(default=None, description="""Curator notes that do not belong in any structured section""", json_schema_extra = { "linkml_meta": {'domain_of': ['RegulatoryStatus', 'DentalMaterial']} })

    @field_validator('creation_date')
    def pattern_creation_date(cls, v):
        pattern=re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+\-]\d{2}:\d{2})$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid creation_date format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid creation_date format: {v}"
            raise ValueError(err_msg)
        return v


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Term.model_rebuild()
Descriptor.model_rebuild()
DentalMaterialDescriptor.model_rebuild()
DentalProcedureDescriptor.model_rebuild()
ChemicalEntityDescriptor.model_rebuild()
AnatomicalEntityDescriptor.model_rebuild()
PhenotypeDescriptor.model_rebuild()
QualityDescriptor.model_rebuild()
EvidenceItem.model_rebuild()
Mapping.model_rebuild()
Component.model_rebuild()
MaterialProperty.model_rebuild()
ClinicalUse.model_rebuild()
ClinicalPerformance.model_rebuild()
AdverseEffect.model_rebuild()
ApprovedUse.model_rebuild()
RegulatoryStatus.model_rebuild()
RegulatorySubmission.model_rebuild()
CommercialProduct.model_rebuild()
Standard.model_rebuild()
DentalMaterial.model_rebuild()
