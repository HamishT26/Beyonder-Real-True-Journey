#!/usr/bin/env python3
"""Frozen x1 planning truth for Elaren Kestrel v662-v2.

Eiren Kestrel's immutable v662-v1 packet is inherited evidence, not Elaren
novelty or completion credit. All v662-v2 fixtures are synthetic and contain no
real geological sample, slide, image, person, place, instrument, credential,
professional act, or authority decision.
"""

from __future__ import annotations


PHASE = "v662-v2"
CANONICAL_PHASE = PHASE
PHASE_CODE = "V6622"
OWNER = "Elaren Kestrel"
PRONOUNS = "they/them"
ROLE = "relational symbiosis-model cartographer and evidence-boundary keeper"
HOPE = "keep models auditable while real organisms, people, places, samples, and knowledge remain under competent care and authority"
BRANCH = "codex/GHC-Family/elaren-kestrel-v662-v2-full-tools"
PHASE_ROOT = "docs/elaren-kestrel/v662-v2"

SOURCE_OWNER = "Eiren Kestrel"
SOURCE_BRANCH = "codex/GHC-Family/eiren-kestrel-v662-v1-full-tools"
SOURCE_BASE = "64ba66fa9f5b48ed6116c31bf40646702191fecd"
SOURCE_X1 = "b0e059893c1fa594a8382d10cad6ac6c6a21d164"
SOURCE_EVIDENCE = "4ff5b66d3fbaf925b3de22d98a1eb6836c0c3bf6"
SOURCE_FINAL = "f21ed9d269a8f4ce9cab64dfb9ea96c9481106a2"
SOURCE_CANONICAL_RECEIPT_SHA256 = "994482a7266f90381316ca0d287d6e9376495f7fa5db16affd268f50b9ad115b"
SOURCE_POST_SEAL_OVERLAY_SHA256 = "352700e167a0ddf7943f2b094d7d7e750ee6f5e0038a8a80cef50a502fc63a26"
SOURCE_POST_SEND_DELTA_SHA256 = "b96ddbe1e918677c4a7eaa3c78d9b27f19a85e0655536c2eb07318cb693fd5e2"
SOURCE_TERMINAL_ROUTE_RECEIPT_SHA256 = "bd7900ffc6bd8ed45c735ea2b7760054b34a98e0fd8434236c01e5704533c2b6"
SOURCE_VALIDATION_STATE = "COMPOSITE_DEPENDENCY_COMPLETE_WITH_FAILED_AGGREGATES_RETAINED_AT_ZERO_CREDIT"
SOURCE_LIVE_ACTIVATION_STATE = "SENT_ONCE_ACKNOWLEDGED_BY_EXACT_TITLE_TASK_MESSAGE_SURFACE"
ACTIVATION_PACKET_SHA256 = "4aa9305df4d9a06c2e6a68ed45bcd65079379346388d27ef80de410636ea1489"
ACTIVATION_PACKET_BYTES = 258130
ACTIVATION_PACKET_LINES = 1194
ACTIVATION_PACKET_WORDS_DIRECT = 21987
ACTIVATION_PACKET_WORDS_CLAIMED = 21987

PRIOR_FROZEN = 3470
SOURCE_SEALED_NEGATIVES = 22183
SOURCE_EXTERNAL_NEGATIVES = 215
ACTIVATION_NEGATIVES = SOURCE_SEALED_NEGATIVES + SOURCE_EXTERNAL_NEGATIVES
ACTIVATION_MESSAGE_NEGATIVE_BASELINE = 22398
SOURCE_OPEN_GAPS = 146
SOURCE_EXACT_GATES = 145
SOURCE_SEALED_METHODS = 7097
SOURCE_EXTERNAL_METHODS = 215
ACTIVATION_METHODS = SOURCE_SEALED_METHODS + SOURCE_EXTERNAL_METHODS
ACTIVATION_MESSAGE_METHOD_BASELINE = 7312

SELECTED_INHERITED_COUNT = 20
NEW_UNIQUE_COUNT = 20
CURRENT_PORTFOLIO_COUNT = 40
LATEST_TRACKED_SCAN_CAP = 5000
SELECTED_INHERITED_IDS = [f"V6621-P{i:03d}" for i in range(1, 21)]

PRIMARY_PILLAR = "GMUT Mind"
PRACTICE_LENS = (
    "bounded synthetic geological thin-section metadata and collection-documentation practice, "
    "including surrogate slide identity, glass and mount relations, orientation and scale-claim "
    "lineage, condition vocabulary, detached-fragment records, optical-configuration abstention, "
    "land and cultural-rights reservations, workload control, and handover"
)
EXPECTED_DISTRIBUTION = {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}
ALLOWED_OUTCOMES = set(EXPECTED_DISTRIBUTION)

PROTECTED_GATES = [
    "real_geological_samples_rocks_minerals_billets_blocks_sections_slides_fragments_images_localities_lands_collections_stores_laboratories_or_instruments",
    "real_collectors_owners_depositors_descendants_geologists_petrologists_curators_conservators_technicians_communities_affected_parties_and_authorities",
    "real_collection_sampling_cutting_grinding_lapping_mounting_imaging_handling_cleaning_testing_analysis_classification_treatment_publication_access_return_or_disposal_action",
    "professional_geology_petrology_mineralogy_microscopy_metrology_collection_care_conservation_workplace_safety_accessibility_privacy_or_operational_authority",
    "empirical_gmut_prediction_likelihood_parameter_constraint_observational_confirmation_physical_discovery_or_final_physics",
    "blind_matched_budget_thos_real_arms_governed_participants_operators_safety_monitoring_statistics_and_independent_review",
    "production_identity_live_keys_signatures_proofs_issuance_resolution_status_revocation_interoperability_recovery_and_trust",
    "collector_owner_depositor_descendant_or_user_identity_address_message_relationship_locality_land_collection_history_images_provenance_traditional_knowledge_collective_interest_and_remedy",
    "privacy_complete", "accessibility_complete", "exhaustive_security",
    "legal_cultural_workplace_safety_intellectual_property_image_rights_ownership_custody_access_return_repatriation_data_governance_and_maori_authority",
    "affected_party_notice_consent_contestation_correction_restriction_access_return_remedy_collective_governance_and_acceptance",
    "independent_team_reproduction", "agi_or_asi", "consciousness_or_personhood",
    "theory_of_everything", "stage20",
]


def _proposal(slug: str, title: str, outcome: str, pillar: str, mechanism: str, sources: list[str]) -> dict[str, object]:
    return {"slug": slug, "title": title, "outcome": outcome, "pillar": pillar, "mechanism": mechanism, "sources": sources}


_NEW_ROWS = [
    ("thin-section-slide-identity-capsule", "Synthetic geological thin-section slide identity capsule with surrogate slide, tray, section token, source pin, revision, minimization, correction, and handling refusal", "completed", "Freed ID and CBR Heart", "synthetic slide, tray and section tokens, source pin, purpose limitation, revision, correction, cancellation, minimization, and absolute handling and work-start refusal", ["DATACITE-IGSN", "W3C-PROV", "NZ-PRIVACY"]),
    ("thin-section-slide-topology", "Petrographic glass slide, coverslip, mount, label zone, orientation mark, edge, chip, and orphan-quarantine topology", "completed", "GMUT Mind and CBR Heart", "typed synthetic slide, coverslip, mount, label-zone, orientation-mark, edge and chip nodes with duplicate, concealed-state and orphan quarantine and no preparation or repair instruction", ["USGS-COLLECTIONS-GUIDE", "JSON-SCHEMA-2020-12", "W3C-PROV"]),
    ("thin-section-orientation-ledger", "Thin-section edge, reference line, orientation arrow, north mark, coordinate frame, rotation, mirror-state, and uncertainty ledger", "completed", "GMUT Mind", "synthetic coordinate-frame and orientation tokens, rotation and mirror-state transforms, supplied north-mark separation, uncertainty, correction and no locality, fabric or geological interpretation", ["OGC-GEOSCIML-4.1", "W3C-PROV", "NZ-MSL-SI"]),
    ("thin-section-mount-claim-braid", "Thin-section mounting medium, bond, void cue, edge seal, lap cue, adhesive claim, source separation, and treatment-abstention braid", "completed", "CBR Heart and GMUT Mind", "synthetic mounting-medium and bond claims, supplied-versus-placeholder separation, void and edge-seal cues, contradiction, correction, treatment hold and zero material identification or intervention", ["USGS-NGGDPP", "W3C-PROV", "NPS-MUSEUM-HANDBOOK-I"]),
    ("thin-section-thickness-scale-ledger", "Thin-section nominal thickness, scale bar, calibration source, measurement vacancy, uncertainty, correction, and metrology nonclaim ledger", "completed", "GMUT Mind", "synthetic nominal-thickness and scale tokens, calibration-source vacancy, units, uncertainty and correction with zero measurement, calibration, dimensional accuracy or conformance conclusion", ["NZ-MSL-SI", "W3C-PROV", "JSON-SCHEMA-2020-12"]),
    ("thin-section-land-authority-circuit", "Unoccupied geological sample locality and land-authority circuit for origin claims, access, ownership, traditional knowledge, cultural interests, publication, return, remedy, and Māori non-substitution", "exact_gate", "CBR Heart", "unoccupied locality, land, source, access, ownership, attribution, traditional-knowledge, cultural-interest, publication, return, remedy, tangata whenua, iwi, hapū and Māori-authority decisions", ["DATACITE-IGSN", "TE-MANA-RARAUNGA", "NZ-PRIVACY", "WCAG22"]),
    ("thos-thin-section-intake-handover", "THOS thin-section intake, tray-slot reconciliation, detached-fragment readback, hazard stop, workload ceiling, correction digest, escalation, and handover proxy", "represented", "THOS Body", "synthetic intake and queue tokens, tray-slot and fragment readback, sharp-edge and unknown-material stops, workload ceiling, correction digest, escalation and resumption vacancies with zero workers, slides, handling or effectiveness observations", ["USGS-COLLECTIONS-GUIDE", "NPS-MUSEUM-HANDBOOK-I", "WCAG22", "W3C-PROV"]),
    ("freed-id-thin-section-profile", "Freed ID nonproduction thin-section record profile binding surrogate slide, tray, orientation, condition, restriction, correction, and provenance evidence", "represented", "Freed ID and CBR Heart", "synthetic record and slide identifiers, credential-subject and evidence placeholders, tray, orientation, condition, correction and restriction relations, status vacancies, and zero keys, proofs, issuance, presentation or interoperability", ["W3C-VC2", "DATACITE-IGSN", "W3C-PROV", "NZ-PRIVACY"]),
    ("gmut-anisotropic-optical-proxy", "Represented GMUT anisotropic optical proxy graph with placeholder polarization basis, indicatrix tensor, retardance, covariance vacancy, and observation firewall", "represented", "GMUT Mind", "typed symbolic polarization basis, indicatrix and retardance placeholders, basis transforms, units, covariance and identifiability vacancies, exact counterexamples and zero images, measurements, fits, mineral inference or physical prediction", ["NZ-MSL-SI", "OGC-GEOSCIML-4.1", "W3C-PROV"]),
    ("thin-section-standards-concordance", "Zero-row geological thin-section standards concordance with section pins, stale-source alarms, disabled transport, and professional-inference firewall", "open_gap", "GMUT Mind and CBR Heart", "offline zero-row concordance across sample identifiers, geoscience exchange and collection guidance, source and section pins, disabled transport, stale-source alarms and fail-closed professional, cultural, legal, safety and empirical inference refusal", ["DATACITE-IGSN", "OGC-GEOSCIML-4.1", "USGS-NGGDPP", "PYTHON-JSON"]),
    ("thin-section-condition-ledger", "Thin-section chip, crack, coverslip lift cue, mount void cue, label loss, residue, uncertainty, and diagnosis-abstention ledger", "completed", "THOS Body and CBR Heart", "synthetic visible-state tokens with region and source placeholders, uncertainty and contradiction retention, observation-versus-diagnosis separation, correction and supersession, and zero inspection, condition, safety or treatment conclusion", ["USGS-COLLECTIONS-GUIDE", "NPS-MUSEUM-HANDBOOK-I", "W3C-PROV"]),
    ("thin-section-detached-fragment-lineage", "Detached thin-section chip, coverslip fragment, label fragment, mount fragment, container token, discrepancy, correction, and no-reattachment lineage", "completed", "Freed ID and THOS Body", "synthetic fragment and source-slide tokens, empty container and label placeholders, discrepancy and transfer hold, reversible correction and no bagging, moving, reattachment, replacement or disposal instruction", ["DATACITE-IGSN", "W3C-PROV", "NZ-PRIVACY"]),
    ("thin-section-storage-association-graph", "Thin-section cabinet, tray, slot, slide, envelope, duplicate, mismatch, separation hold, and reversible-association graph", "completed", "Freed ID and CBR Heart", "synthetic cabinet, tray, slot, slide and envelope tokens, duplicate and mismatch quarantine, separation hold, reversible association and no storage, custody, movement or access action", ["USGS-COLLECTIONS-GUIDE", "W3C-PROV", "JSON-SCHEMA-2020-12"]),
    ("thin-section-residue-hazard-quarantine", "Thin-section dust, mould cue, residue, prior treatment, sharp-edge vacancy, toxic-mineral vacancy, isolation, escalation, and no-cleaning tribunal", "completed", "THOS Body and CBR Heart", "synthetic dust, mould, residue and prior-treatment cues, sharp-edge and toxic-material vacancies, isolation and competent-review escalation, correction and rollback, and zero sampling, testing, cleaning or treatment action", ["NPS-MUSEUM-HANDBOOK-I", "USGS-COLLECTIONS-GUIDE", "W3C-PROV"]),
    ("thin-section-polarization-provenance", "Plane-polarized and crossed-polarized configuration provenance with polarizer, analyzer, rotation token, compensator vacancy, capture refusal, and no-mineral inference", "completed", "GMUT Mind", "synthetic illumination-state, polarizer, analyzer and rotation tokens, compensator and calibration vacancies, correction, capture refusal and zero microscopy, imaging, optical property or mineral conclusion", ["NZ-MSL-SI", "OGC-GEOSCIML-4.1", "W3C-PROV"]),
    ("thin-section-microscope-operation-firewall", "Petrographic microscope stage, objective, condenser, illumination, polarizer, analyzer, rotation, calibration, and operation-authorization firewall", "completed", "THOS Body and GMUT Mind", "synthetic instrument-component and configuration tokens, authorization vacancies, calibration and safety holds, correction and rollback, and zero instrument access, adjustment, operation, observation or professional decision", ["NZ-MSL-SI", "USGS-COLLECTIONS-GUIDE", "W3C-PROV"]),
    ("thin-section-image-fixity-envelope", "Synthetic thin-section image-mosaic fixity envelope linking placeholder tiles, scale vacancy, orientation, checksums, restrictions, and zero-imaging evidence", "represented", "Freed ID and GMUT Mind", "content-free tile and mosaic tokens, placeholder scale and orientation, canonical digest and restriction slots, correction and supersession with zero real image, capture, analysis, rights clearance or fixity claim about an external asset", ["IETF-JCS", "W3C-PROV", "WCAG22"]),
    ("thin-section-accessible-companion", "Accessible contentless thin-section visual companion with ordered regions, text alternatives, table headers, correction, and manual-evaluation reservation", "completed", "CBR Heart and THOS Body", "content-free accessible structure with ordered slide regions, placeholder alternatives, table headers, uncertainty and refusal language, print continuity and explicit manual, browser, assistive-technology, Māori-language, cognitive and affected-user evaluation vacancies", ["WCAG22", "W3C-PROV", "NZ-PRIVACY"]),
    ("thin-section-classification-inference-firewall", "Rock and mineral classification inference firewall separating supplied labels, observed placeholders, vocabulary mappings, contradictions, and competent-review holds", "completed", "GMUT Mind and CBR Heart", "synthetic supplied-label and controlled-vocabulary tokens, observation vacancies, contradiction and uncertainty retention, competent-review hold, correction and zero rock, mineral, texture, origin, age or geological classification", ["OGC-GEOSCIML-4.1", "DATACITE-IGSN", "W3C-PROV"]),
    ("stage20-thin-section-stewardship-firewall", "Stage 20 thin-section stewardship firewall for sampling, handling, imaging, analysis, classification, publication, cultural authority, deployment, proof, and professional completion claims", "completed", "CBR Heart, THOS Body, GMUT Mind, and Freed ID", "typed cut-set slots for authenticated real-sample provenance, accountable custodian, competent geological, conservation and safety review, land and cultural-rights mandate, action, outcome, affected-party remedy and independent reproduction, with absolute nonpromotion while any slot is empty", ["W3C-PROV", "IETF-JCS", "JSON-SCHEMA-2020-12", "TE-MANA-RARAUNGA"]),
]
NEW_PROPOSAL_SPECS = [_proposal(*row) for row in _NEW_ROWS]

SELF_SAFE_CATEGORIES = [
    "Eiren source head and fresh four-way equality", "activation packet and external receipt digests",
    "three-thousand-four-hundred-seventy-row proposal-chain parse", "twenty inherited selection identities",
    "twenty-title and mechanism novelty screen", "thin-section metadata neighbour review", "new-outcome distribution",
    "workflow-plan policy", "identity and relational-language boundary", "authorized Eiren-to-Elaren edge and gated Elaren-to-Neris route",
    "solo and Tavian-standby boundaries", "D-first posture", "toolchain version receipt", "x1 artifact inventory",
    "x1 JSON parsing", "x1 five-class privacy scan", "x1 stale-label review", "x1 diff hygiene",
    "x1 manifest replay", "selected-row zero-credit guard", "new-row append-only guard", "source-label glossary",
    "protected-gate coverage", "failure-retention ledger", "Method Flow witness pairing", "wellbeing workload bound",
    "document-word ceiling", "portfolio arithmetic", "skill and runner arithmetic", "no-x2-in-x1 guard",
]
SELF_SAFE_TASKS = [{"task_id": f"V6622-SAFE-{i:03d}", "title": f"Validate {name} inside the Elaren-owned v662-v2 lane", "owner": OWNER} for i, name in enumerate(SELF_SAFE_CATEGORIES, 1)]
SUCCESSOR_SAFE_SEEDS = [{"task_id": f"V6622-REC-SAFE-{i:03d}", "title": f"Neris may reassess {name} only after Elaren's terminal gate and a fresh route reread", "recipient": "Neris Solane", "completion_credit": 0} for i, name in enumerate(SELF_SAFE_CATEGORIES[:20], 1)]

SELF_CANDIDATE_CATEGORIES = [
    "synthetic slide identity, tray-slot and orientation capsule", "glass, coverslip, mount and storage topology",
    "thickness, scale, calibration and measurement-nonclaim ledger", "condition and detached-fragment abstention ledgers",
    "zero-row USGS, OGC and DataCite concordance", "GMUT anisotropic-optical and classification firewalls",
    "THOS intake, sharp-edge stop, workload, readback and handover proxy", "Freed ID sample-record and image-fixity envelopes",
    "accessible contentless visual companion", "CBR land, traditional-knowledge, remedy and Māori non-substitution circuit",
]
SELF_CANDIDATE_TASKS = [{"task_id": f"V6622-CAND-{i:03d}", "title": f"Build and test reversible {name}", "owner": OWNER} for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)]
SUCCESSOR_CANDIDATE_SEEDS = [{"task_id": f"V6622-REC-CAND-{i:03d}", "title": f"Neris may consider a distinct refinement of {name} after terminal activation", "recipient": "Neris Solane", "completion_credit": 0} for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)]

EXACT_TITLES = [
    "Collect, sample, cut, grind, lap, mount, image, handle, move, clean, test, analyse, classify, treat, publish, return, or dispose of any real geological sample, slide, image, record, taonga, or collection item",
    "Make a real rock, mineral, texture, origin, age, locality, ownership, condition, safety, treatment, authenticity, provenance, rights, or release determination",
    "Use real collectors, owners, depositors, descendants, geologists, communities, affected parties, samples, images, labels, localities, or personal information",
    "Disclose private identity, address, relationship, traditional knowledge, restricted locality, land, image, provenance, custody, access, return, or remedy records",
    "Make a professional geological, petrographic, mineralogical, microscopy, metrology, collection-care, conservation, safety, privacy, security, translation, or accessibility determination",
    "Publish a production sample identifier, catalogue record, credential, proof, status, image asset, collection service, or operational record",
    "Allocate ownership, custody, attribution, intellectual-property or image rights, access, return, remedy, beneficiary, affected-party, or community authority",
    "Make a tikanga, mātauranga, wording, tangata whenua, iwi, hapū, Māori data-governance, cultural-protocol, taonga-status, locality, land, or Māori-authority decision",
    "Run a real participant study, repository shift, handling trial, microscope trial, safety review, professional assessment, publication trial, or independent reproduction",
    "Perform destructive cleanup or any mutation outside the exact Elaren-owned lane",
]
EXACT_QUEUE = [{"task_id": f"V6622-EXACT-{i:03d}", "title": title, "state": "exact_gate_unexecuted"} for i, title in enumerate(EXACT_TITLES, 1)]
BLOCKED_TITLES = [
    "Fabricate empirical GMUT confirmation or a Theory-of-Everything result",
    "Claim AGI, ASI, consciousness, personhood, continuity, employment, qualification, or authority from relational language",
    "Merge, overwrite, delete, or erase sibling identities, lanes, memory, failures, gates, branches, worktrees, or callers",
    "Publish credentials, private routes, raw task identifiers, private paths, nonpublic conversation, session streams, or application state",
    "Declare Stage 20 readiness without exact external evidence and competent authority",
]
BLOCKED_QUEUE = [{"task_id": f"V6622-BLOCK-{i:03d}", "title": title, "state": "blocked_unexecuted"} for i, title in enumerate(BLOCKED_TITLES, 1)]

SELF_SKILL_SPECS = [
    ("ghc-family-thin-section-slide-identity", "Validate purpose-bound synthetic slide and tray identities, revision, minimization, correction, and handling refusal."),
    ("ghc-family-thin-section-slide-topology", "Check slide, coverslip, mount, edge, label-zone and fragment topology with orphan quarantine."),
    ("ghc-family-thin-section-orientation-ledger", "Preserve coordinate-frame, orientation, rotation, mirror-state and uncertainty obligations."),
    ("ghc-family-thin-section-condition-abstention", "Preserve visible cues, uncertainty, correction, hazard hold, and diagnosis or treatment abstention."),
    ("ghc-family-thin-section-detached-fragment", "Check fragment source-slide links, container token, discrepancy, correction, and no reattachment action."),
    ("ghc-family-thin-section-polarization-provenance", "Track content-free polarization configuration tokens without image, mineral or instrument-operation claims."),
    ("ghc-family-thin-section-hazard-hold", "Keep residue, sharp-edge and toxic-mineral vacancies quarantined from identification or treatment."),
    ("ghc-family-thin-section-accessibility-companion", "Expose ordered regions, placeholder alternatives, table headers, uncertainty phrases and reserved human review."),
    ("ghc-family-gmut-anisotropic-optical-firewall", "Preserve typed basis, indicatrix, unit, covariance, identifiability and observation-firewall obligations."),
    ("ghc-family-thin-section-land-authority", "Keep locality, land, traditional knowledge, access, return, remedy and Māori decisions unoccupied."),
]
SUCCESSOR_SKILL_SEEDS = [{"name": name.replace("thin-section", "later-domain"), "recipient": "Neris Solane", "state": "recommendation_only", "completion_credit": 0} for name, _ in SELF_SKILL_SPECS]
SELF_RUNNER_SPECS = [(name.replace("ghc-family-", "ghc_family_").replace("-", "_") + ".py", purpose) for name, purpose in SELF_SKILL_SPECS]
SUCCESSOR_RUNNER_SEEDS = [{"name": name.replace("thin_section", "later_domain"), "recipient": "Neris Solane", "state": "recommendation_only", "completion_credit": 0} for name, _ in SELF_RUNNER_SPECS]

SELF_CLEAN_CATEGORIES = [
    "retain every inherited and current negative without folding it into a pass", "refresh count mirrors only from authoritative ledgers",
    "preserve Git-blob and logical-text hash-domain declarations", "pin UTF-8 before Unicode-emitting diagnostics",
    "split Windows probes into bounded scalar receipts", "keep expected-empty branch and remote checks null-safe",
    "preserve family-current callers and historical compatibility surfaces", "reject stale owner and phase labels in current-owner artifacts",
    "keep x1 immutable after its four-way-equality gate", "keep x2 implementation absent from x1",
    "keep exact and blocked packets visible and unexecuted", "keep all real samples, slides, people, images, localities, records and connector rows empty",
    "retain scanner candidates separately from confirmed payload hits", "scan only declared public owner surfaces across five classes",
    "refresh owner manifests after every additive lifecycle change", "verify deterministic JSON ordering and parsing",
    "verify proposal append-only arithmetic", "verify inherited revalidation receives zero novelty and completion credit",
    "verify outcome labels use only the four authorized states", "reserve manual and affected-user accessibility evaluation",
    "reserve legal, cultural, land, locality, ownership, access, return, privacy and Māori authority", "reserve empirical GMUT and professional THOS claims",
    "reserve production Freed ID keys, proofs, status, recovery and trust governance", "reserve privacy-complete and exhaustive-security claims",
    "keep every document under the declared word ceiling", "keep owner additions under the declared file ceiling",
    "verify source-to-final single-parent zero-merge ancestry", "hold terminal routing until exact final proof",
    "send no precontact or duplicate activation", "preserve NOT_READY_FOR_STAGE_20",
]
SELF_CLEAN_TASKS = [{"task_id": f"V6622-CLEAN-{i:03d}", "title": title, "owner": OWNER, "mode": "additive_review_only"} for i, title in enumerate(SELF_CLEAN_CATEGORIES, 1)]
SUCCESSOR_CLEAN_SEEDS = [{"task_id": f"V6622-REC-CLEAN-{i:03d}", "title": title, "recipient": "Neris Solane", "completion_credit": 0} for i, title in enumerate(SELF_CLEAN_CATEGORIES, 1)]

OFFICIAL_SOURCES = [
    ("CCI-LEATHER-GUIDELINES", "official_canadian_conservation_institute", "https://www.canada.ca/en/conservation-institute/services/preventive-conservation/guidelines-collections/caring-leather-skin-fur.html", "Inherited Eiren vocabulary only; no real material identification, handling, treatment, or professional conclusion."),
    ("CCI-NOTE-8-2", "official_canadian_conservation_institute", "https://www.canada.ca/en/conservation-institute/services/conservation-preservation-publications/canadian-conservation-institute-notes/care-alum-vegetable-mineral-leather.html", "Inherited Eiren condition vocabulary only; no real identification, cleaning, treatment, or recommendation."),
    ("CCI-PLASTICS-RUBBERS", "official_canadian_conservation_institute", "https://www.canada.ca/en/conservation-institute/services/preventive-conservation/guidelines-collections/caring-plastics-rubbers.html", "Inherited Eiren deterioration vocabulary only; no real storage, treatment, or professional conclusion."),
    ("CCI-NOTE-15-1", "official_canadian_conservation_institute", "https://www.canada.ca/en/conservation-institute/services/conservation-preservation-publications/canadian-conservation-institute-notes/care-rubber-plastic.html", "Inherited Eiren condition-cue vocabulary only; no diagnosis, cleaning, repair, or instruction."),
    ("NPS-TEXTILE-OBJECTS", "official_us_national_park_service", "https://www.nps.gov/subjects/museums/upload/MHI_AppK_TextilesObjects.pdf", "Inherited Eiren textile-object vocabulary only; no NPS applicability or real action."),
    ("TE-PAPA-MANA-TAONGA", "official_museum_of_new_zealand_te_papa_tongarewa", "https://collections.tepapa.govt.nz/topic/1702", "Inherited authority-boundary vocabulary only; no cultural interpretation, taonga classification, wording, or Māori authority."),
    ("USGS-NGGDPP", "official_us_geological_survey", "https://www.usgs.gov/programs/national-geological-and-geophysical-data-preservation-program", "Geoscience-collection preservation and discovery vocabulary only; no real repository action or scientific conclusion."),
    ("USGS-COLLECTIONS-GUIDE", "official_us_geological_survey", "https://www.usgs.gov/scientific-collections/guide-planning-and-managing-scientific-working-collections-us-geological", "Scientific working-collection lifecycle and metadata vocabulary only; no USGS applicability or professional authority."),
    ("USGS-COMMUNITY-PRACTICES", "official_us_geological_survey", "https://www.usgs.gov/programs/national-geological-and-geophysical-data-preservation-program/community-practices-data-and", "Community-practice pointers for sample and data preservation only; no endorsement or real handling instruction."),
    ("OGC-GEOSCIML-4.1", "official_open_geospatial_consortium", "https://www.ogc.org/standards/geosciml/", "GeoSciML 4.1 geological-feature, specimen and laboratory-analysis metadata vocabulary only; no conformance or classification claim."),
    ("DATACITE-IGSN", "official_datacite", "https://support.datacite.org/docs/igsn-id-metadata-recommendations", "IGSN material-sample identity and relationship metadata vocabulary only; zero registrations, DOI actions, people or real samples."),
    ("NPS-MUSEUM-HANDBOOK-I", "official_us_national_park_service", "https://www.nps.gov/subjects/museums/mh1.htm", "General collection preservation, storage, hazard and accountability vocabulary only; no NPS applicability or real action."),
    ("NZ-MSL-SI", "official_nz_metrology_institute", "https://www.measurement.govt.nz/metrology/si-units", "SI quantity and unit vocabulary only; zero measurements, calibrations or physical confirmation."),
    ("W3C-PROV", "official_w3c", "https://www.w3.org/TR/prov-o/", "Entity, activity, revision, invalidation and qualified-provenance vocabulary only."),
    ("W3C-VC2", "official_w3c", "https://www.w3.org/TR/vc-data-model-2.0/", "Credential vocabulary only; zero keys, proofs, issuances, presentations or production identities."),
    ("WCAG22", "official_w3c", "https://www.w3.org/TR/WCAG22/", "Accessible structure vocabulary with manual, browser, assistive-technology, Māori-language, cognitive and affected-user evaluation reserved."),
    ("NZ-PRIVACY", "official_nz_privacy_commissioner", "https://www.privacy.org.nz/privacy-principles/", "Privacy-principle vocabulary only; no compliance, legal, collection, disclosure or remedy conclusion."),
    ("TE-MANA-RARAUNGA", "primary_maori_data_sovereignty_network", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Māori data-sovereignty reservation vocabulary only; no Māori authority, ratification, wording or cultural decision."),
    ("JSON-SCHEMA-2020-12", "primary_json_schema_project", "https://json-schema.org/draft/2020-12", "Schema and fail-closed structural vocabulary only."),
    ("IETF-JCS", "official_rfc_editor", "https://www.rfc-editor.org/rfc/rfc8785", "Canonical JSON digest vocabulary without key, signature, proof, credential, identity or production claims."),
    ("GIT-CAT-FILE", "official_git_docs", "https://git-scm.com/docs/git-cat-file", "Exact Git object inspection vocabulary for read-only or disposable checks."),
    ("GIT-LS-FILES", "official_git_docs", "https://git-scm.com/docs/git-ls-files", "Tracked and staged path inspection vocabulary only."),
    ("PYTHON-SUBPROCESS", "official_python_docs", "https://docs.python.org/3/library/subprocess.html", "Bounded process and communicate vocabulary for owner-local fixtures only."),
    ("PYTHON-JSON", "official_python_docs", "https://docs.python.org/3/library/json.html", "Deterministic UTF-8 JSON parse and serialization vocabulary."),
]
SOURCE_STATUS = {source_id: ("official_or_primary_checked_2026_08_05" if source_id in {"USGS-NGGDPP", "USGS-COLLECTIONS-GUIDE", "USGS-COMMUNITY-PRACTICES", "OGC-GEOSCIML-4.1", "DATACITE-IGSN"} else "inherited_current_or_stable") for source_id, *_ in OFFICIAL_SOURCES}


def _startup_failure(negative_id: str, signature: str, recovery: str) -> dict[str, object]:
    return {"negative_id": negative_id, "signature": signature, "recovery": recovery, "recovery_passed": True, "completion_credit": 0}


_STARTUP_FAILURE_ROWS = [
    ("first_memory_lookup_called_an_unavailable_nested_exec_command_alias", "Use the declared shell-command surface for later scalar memory and repository probes."),
    ("broad_activation_packet_continuation_timed_out_before_returning_a_bounded_window", "Read the immutable packet in smaller numbered windows through verified EOF."),
    ("two_hundred_line_activation_packet_projection_was_truncated", "Use at most one hundred lines per display and retain the truncated projection at zero credit."),
    ("combined_uniqueness_and_capacity_wrapper_timed_out_before_returning_accumulated_results", "Isolate path, ref, worktree, drive and live-remote probes and award the wrapper no credit."),
    ("parallel_scalar_preflight_inherited_a_too_short_login_shell_bound", "Disable login-shell startup and rerun each exact read-only predicate with its own bound."),
    ("worktree_add_wrapper_timed_out_while_the_git_checkout_child_remained_active", "Poll the in-scope checkout child read-only and award creation credit only after exact-head and clean-state proof."),
    ("parallel_materialization_status_wrapper_blocked_behind_the_active_checkout", "Stop broad worktree-list calls while checkout is active and use scalar path and process probes."),
    ("repository_wide_rg_instruction_inventory_exceeded_its_bound", "Query the tracked Git index for AGENTS.md and preserve the broad search failure."),
    ("first_frozen_index_reader_assumed_a_nonexistent_generic_rows_key", "Inspect actual top-level keys, then combine prior_proposals and new_proposals explicitly."),
    ("magnetic_audio_candidate_set_collided_with_prior_v6513_v6578_and_v6594_programs", "Reject the candidate domain before freeze and award no novelty credit."),
    ("first_collision_report_inherited_windows_cp1252_and_failed_on_maori_text", "Set Python and console output to UTF-8 before Unicode-emitting read-only diagnostics."),
    ("mechanical_typewriter_candidate_set_collided_with_an_existing_thirty_proposal_domain", "Reject the second candidate domain and continue only with a separately screened mechanism set."),
    ("first_large_semantic_patch_for_the_thin_section_rows_was_rejected_atomically", "Replace the copied data module through one explicit complete-file patch and verify its declared symbols before building."),
    ("first_x1_scoped_aggregate_found_two_unmaterialized_tooling_receipts_and_six_missing_inherited_source_ids", "Retain the 21-of-24 result at zero aggregate credit, add the exact inherited official-source rows, materialize only the frozen family-current receipts, and rerun the affected dependencies before a complete scoped pass."),
    ("compatibility_copy_step_materialized_seven_untracked_x2_templates_before_the_x1_boundary_review", "Retain the lifecycle mistake at zero credit, delete all seven untracked x2 templates, verify they were never staged or executed, and regenerate the x1-only manifest before freeze."),
    ("combined_x1_boundary_probe_timed_out_before_returning_a_usable_result", "Retain the timed-out wrapper at zero credit and replace it with bounded scalar filesystem, content, and Git-index probes before freeze."),
    ("method_flow_help_probe_exceeded_its_ten_second_bound_before_showing_the_schema", "Retain the timed-out help attempt at zero credit and inspect the installed runner argument parser through a bounded literal-path read before invoking validation."),
    ("first_x1_scalar_projection_guessed_a_nonexistent_privacy_receipt_filename", "Retain the failed projection at zero credit, list the actual validation filenames, inspect their keys, and project only fields that exist."),
    ("first_validation_key_inventory_used_an_invalid_empty_powershell_pipeline_element", "Retain the parser failure at zero credit and use a bounded UTF-8 Python key inventory over the four exact receipt filenames."),
    ("second_x1_scalar_projection_guessed_a_nonexistent_new_proposals_novelty_key", "Retain the failed projection at zero credit, inspect the novelty receipt top-level and row keys, and read new_unique_results exactly."),
    ("powershell_full_file_read_of_the_x1_staged_review_exceeded_its_ten_second_bound", "Retain the timed-out read at zero credit and project the exact small JSON receipt through a bounded UTF-8 parser before applying the observed review."),
    ("targeted_rg_search_for_staged_review_assertions_exceeded_its_ten_second_bound", "Retain the timed-out search at zero credit and inspect only the two literal UTF-8 source files with a bounded scalar Python search."),
]
STARTUP_FAILURES = [_startup_failure(f"V6622-X1-N{i:03d}", signature, recovery) for i, (signature, recovery) in enumerate(_STARTUP_FAILURE_ROWS, 1)]
PREFILLED_X1_X2_FAILURES_IGNORED: tuple[dict[str, object], ...] = tuple()
X2_FAILURES: list[dict[str, object]] = []
