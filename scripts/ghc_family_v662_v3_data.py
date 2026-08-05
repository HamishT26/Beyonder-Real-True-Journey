#!/usr/bin/env python3
"""Frozen x1 planning truth for Neris Solane v662-v3.

Elaren Kestrel's immutable v662-v2 packet is inherited evidence, not Neris
novelty or completion credit. All v662-v3 fixtures are synthetic and contain no
real herbarium specimen, sheet, fragment, image, label, person, locality,
collection record, instrument, credential, professional act, or authority
decision.
"""

from __future__ import annotations


PHASE = "v662-v3"
CANONICAL_PHASE = PHASE
PHASE_CODE = "V6623"
OWNER = "Neris Solane"
PRONOUNS = "they/them"
ROLE = "relational symbiosis-model cartographer and evidence-boundary keeper"
HOPE = "keep models auditable while real organisms, people, places, samples, and knowledge remain under competent care and authority"
BRANCH = "codex/GHC-Family/neris-solane-v662-v3-full-tools"
PHASE_ROOT = "docs/neris-solane/v662-v3"

SOURCE_OWNER = "Elaren Kestrel"
SOURCE_BRANCH = "codex/GHC-Family/elaren-kestrel-v662-v2-full-tools"
SOURCE_BASE = "f21ed9d269a8f4ce9cab64dfb9ea96c9481106a2"
SOURCE_X1 = "77f043266676075810fee3fa6d416282431a0c83"
SOURCE_EVIDENCE = "76dc029ab3c6c14a59a3ac318f588f417582252b"
SOURCE_FINAL = "2c1fbddf9a68c8fd30b473c7ae2d510bde85fcc0"
SOURCE_CANONICAL_RECEIPT_SHA256 = "01a0347f2f965ce5bc5c28a6e321b565b1a7c0b9392aa4cc845406179c6fba49"
SOURCE_POST_SEAL_OVERLAY_SHA256 = "f6928da841e7056d7ec2b53b1c416b88ae5a685e6b7524e073f0f2c7a4f3cf1f"
SOURCE_POST_SEND_DELTA_SHA256 = "fa2ac8d7128a6de5dbbe9244b5c32817d6bf3a907e2d263ec6d3dbeb3ff6c6b2"
SOURCE_TERMINAL_ROUTE_RECEIPT_SHA256 = "fa2ac8d7128a6de5dbbe9244b5c32817d6bf3a907e2d263ec6d3dbeb3ff6c6b2"
SOURCE_VALIDATION_STATE = "BOUNDED_COMPONENT_COMPLETE_WITH_FAILED_CANONICAL_AGGREGATE_RETAINED_AT_ZERO_CREDIT"
SOURCE_LIVE_ACTIVATION_STATE = "SENT_ONCE_ACKNOWLEDGED_BY_EXACT_TITLE_TASK_MESSAGE_SURFACE"
ACTIVATION_PACKET_SHA256 = "47bc17f2c5818d55eabfb11411bb806e0b71b5ef625c4f7e2108d0a071a80c4f"
ACTIVATION_PACKET_BYTES = 257241
ACTIVATION_PACKET_LINES = 1212
ACTIVATION_PACKET_WORDS_DIRECT = 21822
ACTIVATION_PACKET_WORDS_CLAIMED = 21822

PRIOR_FROZEN = 3490
SOURCE_SEALED_NEGATIVES = 22538
SOURCE_POST_FINAL_NEGATIVES = 9
SOURCE_POST_ROUTE_NEGATIVES = 2
SOURCE_EXTERNAL_NEGATIVES = SOURCE_POST_FINAL_NEGATIVES + SOURCE_POST_ROUTE_NEGATIVES
ACTIVATION_NEGATIVES = SOURCE_SEALED_NEGATIVES + SOURCE_EXTERNAL_NEGATIVES
ACTIVATION_MESSAGE_NEGATIVE_BASELINE = SOURCE_SEALED_NEGATIVES + SOURCE_POST_FINAL_NEGATIVES
SOURCE_OPEN_GAPS = 147
SOURCE_EXACT_GATES = 146
SOURCE_SEALED_METHODS = 7372
SOURCE_POST_FINAL_METHODS = 9
SOURCE_POST_ROUTE_METHODS = 2
SOURCE_EXTERNAL_METHODS = SOURCE_POST_FINAL_METHODS + SOURCE_POST_ROUTE_METHODS
ACTIVATION_METHODS = SOURCE_SEALED_METHODS + SOURCE_EXTERNAL_METHODS
ACTIVATION_MESSAGE_METHOD_BASELINE = SOURCE_SEALED_METHODS + SOURCE_POST_FINAL_METHODS

SELECTED_INHERITED_COUNT = 20
NEW_UNIQUE_COUNT = 20
CURRENT_PORTFOLIO_COUNT = 40
LATEST_TRACKED_SCAN_CAP = 5000
SELECTED_INHERITED_IDS = [f"V6622-P{i:03d}" for i in range(1, 21)]

PRIMARY_PILLAR = "GMUT Mind"
PRACTICE_LENS = (
    "bounded synthetic herbarium voucher-sheet metadata and collection-documentation practice, "
    "including surrogate sheet identity, mount-substrate and attachment relations, folded-organ and "
    "fragment-packet lineage, label and annotation chronology, image and barcode provenance, "
    "taxonomic and destructive-sampling abstention, biocultural authority reservations, workload "
    "control, and handover"
)
EXPECTED_DISTRIBUTION = {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}
ALLOWED_OUTCOMES = set(EXPECTED_DISTRIBUTION)

_LEGACY_PROTECTED_GATES_IGNORED = [
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

PROTECTED_GATES = [
    "real_plants_vouchers_herbarium_specimens_sheets_fragments_packets_images_labels_annotations_barcodes_localities_lands_collections_cabinets_laboratories_or_instruments",
    "real_collectors_owners_depositors_descendants_botanists_taxonomists_curators_conservators_technicians_communities_affected_parties_and_authorities",
    "real_collecting_pressing_drying_mounting_repair_sampling_dissection_imaging_handling_cleaning_testing_identification_determination_digitisation_loan_exchange_publication_access_return_repatriation_or_disposal_action",
    "professional_botany_taxonomy_nomenclature_herbarium_curation_conservation_digitisation_pest_management_collection_care_workplace_safety_accessibility_privacy_or_operational_authority",
    "empirical_gmut_prediction_likelihood_parameter_constraint_observational_confirmation_physical_discovery_or_final_physics",
    "blind_matched_budget_thos_real_arms_governed_participants_operators_safety_monitoring_statistics_and_independent_review",
    "production_identity_live_keys_signatures_proofs_issuance_resolution_status_revocation_interoperability_recovery_and_trust",
    "collector_owner_depositor_descendant_or_user_identity_address_message_relationship_sensitive_locality_land_collection_history_images_labels_provenance_traditional_knowledge_taonga_collective_interest_and_remedy",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "legal_cultural_workplace_safety_intellectual_property_image_rights_collecting_permits_ownership_custody_access_benefit_sharing_loan_exchange_return_repatriation_data_governance_and_maori_authority",
    "affected_party_notice_consent_contestation_correction_restriction_access_takedown_return_repatriation_remedy_collective_governance_and_acceptance",
    "independent_team_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]


def _proposal(slug: str, title: str, outcome: str, pillar: str, mechanism: str, sources: list[str]) -> dict[str, object]:
    return {"slug": slug, "title": title, "outcome": outcome, "pillar": pillar, "mechanism": mechanism, "sources": sources}


_LEGACY_NEW_ROWS_IGNORED = [
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
_NEW_ROWS = [
    ("herbarium-sheet-identity-capsule", "Synthetic herbarium voucher-sheet identity capsule with surrogate sheet, folder, cabinet, source pin, revision, minimization, correction, and handling refusal", "completed", "Freed ID and CBR Heart", "synthetic sheet, folder and cabinet tokens, source pin, purpose limitation, revision, correction, cancellation, minimization, and absolute handling and work-start refusal", ["TDWG-DWC", "INDEX-HERBARIORUM", "W3C-PROV", "NZ-PRIVACY"]),
    ("herbarium-sheet-topology", "Herbarium mount substrate, pressed-organ region, label zone, barcode zone, annotation field, fragment packet, stamp, edge, and orphan-quarantine topology", "completed", "GMUT Mind and CBR Heart", "typed synthetic sheet, substrate, organ-region, label, barcode, annotation, packet, stamp and edge nodes with duplicate, concealed-state and orphan quarantine and no mounting or repair instruction", ["KEW-HERBARIUM", "SMITHSONIAN-HERBARIUM-GUIDE", "JSON-SCHEMA-2020-12", "W3C-PROV"]),
    ("herbarium-folded-organ-graph", "Pressed leaf, stem, flower, fruit, root, fold, overlap, reverse-view flap, attachment point, and uncertainty adjacency graph", "completed", "GMUT Mind", "synthetic organ-region and fold tokens, overlap and reverse-view relations, supplied-versus-placeholder separation, uncertainty, correction and zero morphology, identity or taxonomic interpretation", ["SMITHSONIAN-HERBARIUM-GUIDE", "TDWG-DWC", "W3C-PROV"]),
    ("herbarium-attachment-provenance", "Herbarium mounting strip, stitch, adhesive cue, support card, envelope, prior-repair claim, source separation, and intervention-abstention braid", "completed", "CBR Heart and GMUT Mind", "synthetic attachment and support claims, supplied-versus-placeholder separation, contradiction, correction, intervention hold and zero material identification, mounting, repair or treatment", ["SMITHSONIAN-HERBARIUM-GUIDE", "KEW-HERBARIUM", "W3C-PROV"]),
    ("herbarium-biocultural-authority-circuit", "Unoccupied herbarium locality and biocultural-authority circuit for collecting permission, sensitive place, provenance, traditional knowledge, taonga, access, benefit, publication, takedown, return, repatriation, remedy, and Māori non-substitution", "exact_gate", "CBR Heart", "unoccupied locality, land, collecting, provenance, traditional-knowledge, taonga, access, benefit, disclosure, takedown, return, repatriation, remedy, tangata whenua, iwi, hapū and Māori-authority decisions", ["TDWG-DWC", "TE-MANA-RARAUNGA", "NZ-PRIVACY", "WCAG22"]),
    ("thos-herbarium-intake-handover", "THOS herbarium-sheet intake, folder-cabinet reconciliation, loose-fragment readback, pest-cue stop, workload ceiling, correction digest, escalation, and handover proxy", "represented", "THOS Body", "synthetic intake and queue tokens, folder-cabinet and fragment readback, pest and unknown-material stops, workload ceiling, correction digest, escalation and resumption vacancies with zero workers, specimens, handling or effectiveness observations", ["KEW-HERBARIUM", "NPS-MUSEUM-HANDBOOK-I", "WCAG22", "W3C-PROV"]),
    ("freed-id-herbarium-profile", "Freed ID nonproduction herbarium-record profile binding surrogate sheet, preserved-specimen class, folder, fragment packet, annotation, restriction, correction, and provenance evidence", "represented", "Freed ID and CBR Heart", "synthetic record and sheet identifiers, credential-subject and evidence placeholders, preserved-specimen class, folder, fragment, annotation, correction and restriction relations, status vacancies, and zero keys, proofs, issuance, presentation or interoperability", ["W3C-VC2", "TDWG-DWC", "W3C-PROV", "NZ-PRIVACY"]),
    ("gmut-pressed-organ-topology-proxy", "Represented GMUT pressed-organ planar topology proxy with placeholder midrib and vein graph, fold transform, anisotropic deformation tensor, units, covariance vacancy, and observation firewall", "represented", "GMUT Mind", "typed symbolic adjacency, fold-transform and anisotropic-deformation placeholders, units, covariance and identifiability vacancies, exact counterexamples and zero images, measurements, fits, botanical inference or physical prediction", ["NZ-MSL-SI", "TDWG-DWC", "W3C-PROV"]),
    ("herbarium-standards-concordance", "Zero-row herbarium-sheet standards concordance joining Darwin Core, Index Herbariorum and GBIF archive vocabulary with section pins, stale-source alarms, disabled transport, and professional-inference firewall", "open_gap", "GMUT Mind and CBR Heart", "offline zero-row concordance across preserved-specimen, collection-code and archive vocabulary, source and section pins, disabled transport, stale-source alarms and fail-closed taxonomic, professional, cultural, legal, privacy and empirical inference refusal", ["TDWG-DWC", "INDEX-HERBARIORUM", "GBIF-DWCA", "PYTHON-JSON"]),
    ("herbarium-label-transcription-braid", "Herbarium collector label, field number, verbatim text, locality field, date field, supplied interpretation, transcription, illegibility, contradiction, correction, and no-attribution braid", "completed", "Freed ID and CBR Heart", "content-free label and field tokens, verbatim-versus-interpreted separation, illegibility, uncertainty, contradiction, correction and supersession with zero real person, place, transcription, attribution or collection-event claim", ["TDWG-DWC", "SMITHSONIAN-HERBARIUM-GUIDE", "W3C-PROV", "NZ-PRIVACY"]),
    ("herbarium-annotation-chronology", "Herbarium determination slip, annotation label, name-usage placeholder, determiner-role vacancy, date, confidence, contradiction, supersession, and taxonomy-abstention chronology", "completed", "GMUT Mind and CBR Heart", "synthetic annotation and determination-event tokens, name-usage placeholders, role vacancy, dates, contradiction, correction and supersession with zero accepted name, type, identity, nomenclatural act or taxonomic authority", ["TDWG-DWC", "KEW-HERBARIUM", "W3C-PROV"]),
    ("herbarium-fragment-packet-lineage", "Loose leaf, seed, flower, fruit, bark, label and mount fragment packet lineage with source-sheet token, packet seal placeholder, discrepancy, correction, and no-reassociation action", "completed", "Freed ID and THOS Body", "synthetic fragment, packet and source-sheet tokens, empty packet-seal and label placeholders, discrepancy and transfer hold, reversible correction and no bagging, moving, reassociation, replacement, sampling or disposal instruction", ["TDWG-DWC", "W3C-PROV", "NZ-PRIVACY"]),
    ("herbarium-storage-association-graph", "Herbarium cabinet, pigeonhole, genus cover, folder, sheet, fragment packet, duplicate, mismatch, separation hold, and reversible-association graph", "completed", "Freed ID and CBR Heart", "synthetic cabinet, pigeonhole, cover, folder, sheet and packet tokens, duplicate and mismatch quarantine, separation hold, reversible association and no storage, custody, movement, filing, loan or access action", ["INDEX-HERBARIORUM", "KEW-HERBARIUM", "W3C-PROV", "JSON-SCHEMA-2020-12"]),
    ("herbarium-hazard-quarantine", "Herbarium pest cue, frass, webbing, dust, mould suspicion, residue, prior pesticide vacancy, sharp-element vacancy, isolation, escalation, and no-treatment tribunal", "completed", "THOS Body and CBR Heart", "synthetic pest, frass, webbing, dust, mould and residue cues, prior-pesticide and sharp-element vacancies, isolation and competent-review escalation, correction and rollback, and zero identification, sampling, testing, freezing, cleaning or treatment action", ["NPS-MUSEUM-HANDBOOK-I", "KEW-HERBARIUM", "W3C-PROV"]),
    ("herbarium-digitisation-envelope", "Represented herbarium whole-sheet image, barcode, scale-bar, colour-target, orientation, derivative, checksum, rights-vacancy, and zero-imaging provenance envelope", "represented", "Freed ID and GMUT Mind", "content-free image, barcode, scale, colour-target and derivative tokens, canonical digest and rights slots, correction and supersession with zero real image, capture, calibration, rights clearance, publication or fixity claim about an external asset", ["KEW-DIGITISATION", "IETF-JCS", "W3C-PROV", "WCAG22"]),
    ("herbarium-sampling-loan-firewall", "Herbarium destructive sampling, dissection, remounting, loan, exchange, imaging, publication, return, repatriation, and action-authorization firewall", "completed", "THOS Body and CBR Heart", "synthetic action and mandate tokens, custodian, conservation, taxonomic, safety, legal and cultural authority vacancies, correction and rollback, and zero specimen access, sampling, dissection, remounting, loan, exchange, publication or return action", ["KEW-HERBARIUM", "TDWG-DWC", "TE-MANA-RARAUNGA", "W3C-PROV"]),
    ("herbarium-accessible-companion", "Nonvisual voucher-layout transcript with numbered zones, fold cross-references, explicit headers, uncertainty cues, print continuity, and reserved affected-user review", "completed", "CBR Heart and THOS Body", "content-free accessible structure with ordered sheet regions, folded-part relations, placeholder alternatives, table headers, uncertainty and refusal language, print continuity and explicit manual, browser, assistive-technology, Māori-language, cognitive and affected-user evaluation vacancies", ["WCAG22", "W3C-PROV", "NZ-PRIVACY"]),
    ("herbarium-type-citation-firewall", "Herbarium material-citation and type-status firewall separating supplied label text, typified-name placeholder, duplicate claim, literature anchor, contradictions, and competent-review holds", "completed", "GMUT Mind and CBR Heart", "synthetic supplied-label, material-citation and type-status tokens, literature and repository vacancies, contradiction and uncertainty retention, competent-review hold, correction and zero nomenclatural, type, authenticity or taxonomic conclusion", ["TDWG-DWC", "INDEX-HERBARIORUM", "W3C-PROV"]),
    ("herbarium-sensitive-publication-firewall", "Herbarium sensitive-locality, collector identity, traditional-knowledge, image-rights, restriction, audience, redaction, takedown, correction, and publication nonclaim firewall", "completed", "CBR Heart and Freed ID", "synthetic sensitivity and restriction tokens, locality and identity vacancies, audience and expiry placeholders, reversible redaction, takedown and correction with zero disclosure, rights clearance, legal conclusion, cultural decision or publication action", ["TDWG-DWC", "NZ-PRIVACY", "TE-MANA-RARAUNGA", "W3C-PROV"]),
    ("stage20-herbarium-stewardship-firewall", "Stage 20 herbarium stewardship firewall for collection, mounting, curation, identification, sampling, imaging, publication, access, cultural authority, deployment, proof, and professional completion claims", "completed", "CBR Heart, THOS Body, GMUT Mind, and Freed ID", "typed cut-set slots for authenticated real-specimen provenance, accountable custodian, competent botanical, conservation and safety review, collecting, land and biocultural mandate, action, outcome, affected-party remedy and independent reproduction, with absolute nonpromotion while any slot is empty", ["W3C-PROV", "IETF-JCS", "JSON-SCHEMA-2020-12", "TE-MANA-RARAUNGA"]),
]
NEW_PROPOSAL_SPECS = [_proposal(*row) for row in _NEW_ROWS]

_LEGACY_SELF_SAFE_CATEGORIES_IGNORED = [
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
SELF_SAFE_CATEGORIES = [
    "Elaren source head and fresh four-way equality", "activation packet and separate external overlays",
    "three-thousand-four-hundred-ninety-row proposal-chain parse", "twenty inherited selection identities",
    "twenty-title and mechanism novelty screen", "seed-bank, lichen, and herbarium-sheet neighbour review",
    "new-outcome distribution", "workflow-plan policy", "identity and relational-language boundary",
    "authorized Elaren-to-Neris edge and gated Neris-to-Vesper route", "solo and Tavian-standby boundaries",
    "D-first posture", "toolchain version receipt", "x1 artifact inventory", "x1 JSON parsing",
    "x1 five-class privacy scan", "x1 stale-label review", "x1 diff hygiene", "x1 manifest replay",
    "selected-row zero-credit guard", "new-row append-only guard", "source-label glossary",
    "protected-gate coverage", "failure-retention ledger", "Method Flow witness pairing",
    "wellbeing workload bound", "document-word ceiling", "portfolio arithmetic",
    "skill and runner arithmetic", "no-x2-in-x1 guard",
]
SELF_SAFE_TASKS = [{"task_id": f"V6623-SAFE-{i:03d}", "title": f"Validate {name} inside the Neris-owned v662-v3 lane", "owner": OWNER} for i, name in enumerate(SELF_SAFE_CATEGORIES, 1)]
SUCCESSOR_SAFE_SEEDS = [{"task_id": f"V6623-REC-SAFE-{i:03d}", "title": f"Vesper may reassess {name} only after Neris's terminal gate and a fresh route reread", "recipient": "Vesper Arlen", "completion_credit": 0} for i, name in enumerate(SELF_SAFE_CATEGORIES[:20], 1)]

_LEGACY_SELF_CANDIDATE_CATEGORIES_IGNORED = [
    "synthetic slide identity, tray-slot and orientation capsule", "glass, coverslip, mount and storage topology",
    "thickness, scale, calibration and measurement-nonclaim ledger", "condition and detached-fragment abstention ledgers",
    "zero-row USGS, OGC and DataCite concordance", "GMUT anisotropic-optical and classification firewalls",
    "THOS intake, sharp-edge stop, workload, readback and handover proxy", "Freed ID sample-record and image-fixity envelopes",
    "accessible contentless visual companion", "CBR land, traditional-knowledge, remedy and Māori non-substitution circuit",
]
SELF_CANDIDATE_CATEGORIES = [
    "synthetic sheet, folder, cabinet, barcode and annotation identity capsule",
    "mount substrate, pressed-organ, label-zone, packet and attachment topology",
    "folded-organ adjacency and planar-topology nonclaim graph",
    "label transcription, determination chronology and taxonomic-abstention braid",
    "zero-row TDWG, Index Herbariorum and GBIF concordance",
    "GMUT pressed-organ topology and deformation firewall",
    "THOS intake, pest stop, workload, readback and handover proxy",
    "Freed ID herbarium-record and digitisation envelopes",
    "accessible contentless whole-sheet companion",
    "CBR locality, traditional-knowledge, repatriation, remedy and Māori non-substitution circuit",
]
SELF_CANDIDATE_TASKS = [{"task_id": f"V6623-CAND-{i:03d}", "title": f"Build and test reversible {name}", "owner": OWNER} for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)]
SUCCESSOR_CANDIDATE_SEEDS = [{"task_id": f"V6623-REC-CAND-{i:03d}", "title": f"Vesper may consider a distinct refinement of {name} after terminal activation", "recipient": "Vesper Arlen", "completion_credit": 0} for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)]

_LEGACY_EXACT_TITLES_IGNORED = [
    "Collect, sample, cut, grind, lap, mount, image, handle, move, clean, test, analyse, classify, treat, publish, return, or dispose of any real geological sample, slide, image, record, taonga, or collection item",
    "Make a real rock, mineral, texture, origin, age, locality, ownership, condition, safety, treatment, authenticity, provenance, rights, or release determination",
    "Use real collectors, owners, depositors, descendants, geologists, communities, affected parties, samples, images, labels, localities, or personal information",
    "Disclose private identity, address, relationship, traditional knowledge, restricted locality, land, image, provenance, custody, access, return, or remedy records",
    "Make a professional geological, petrographic, mineralogical, microscopy, metrology, collection-care, conservation, safety, privacy, security, translation, or accessibility determination",
    "Publish a production sample identifier, catalogue record, credential, proof, status, image asset, collection service, or operational record",
    "Allocate ownership, custody, attribution, intellectual-property or image rights, access, return, remedy, beneficiary, affected-party, or community authority",
    "Make a tikanga, mātauranga, wording, tangata whenua, iwi, hapū, Māori data-governance, cultural-protocol, taonga-status, locality, land, or Māori-authority decision",
    "Run a real participant study, repository shift, handling trial, microscope trial, safety review, professional assessment, publication trial, or independent reproduction",
    "Perform destructive cleanup or any mutation outside the exact Neris-owned lane",
]
EXACT_TITLES = [
    "Collect, press, dry, mount, remount, dissect, sample, image, handle, clean, identify, annotate, digitise, publish, loan, exchange, return, repatriate, or dispose of any real plant, specimen, sheet, fragment, image, label, taonga, or collection record",
    "Make a real botanical identity, taxonomic, nomenclatural, type-status, locality, ownership, condition, pest, safety, treatment, authenticity, provenance, rights, or release determination",
    "Use real collectors, owners, depositors, descendants, botanists, communities, affected parties, specimens, images, labels, annotations, localities, or personal information",
    "Disclose private identity, address, relationship, traditional knowledge, restricted locality, land, image, label, provenance, custody, access, benefit, takedown, return, repatriation, or remedy records",
    "Make a professional botanical, taxonomic, nomenclatural, herbarium-curation, conservation, pest-management, collection-care, safety, privacy, security, translation, or accessibility determination",
    "Publish a production specimen identifier, catalogue record, credential, proof, status, image asset, collection service, Darwin Core archive, or operational record",
    "Allocate ownership, custody, attribution, intellectual-property or image rights, collecting permission, access, benefit sharing, loan, exchange, return, repatriation, remedy, affected-party, or community authority",
    "Make a tikanga, mātauranga, wording, tangata whenua, iwi, hapū, Māori data-governance, cultural-protocol, taonga-status, locality, land, or Māori-authority decision",
    "Run a real participant study, repository shift, specimen-handling trial, digitisation trial, safety review, professional assessment, publication trial, or independent reproduction",
    "Perform destructive cleanup or any mutation outside the exact Neris-owned lane",
]
EXACT_QUEUE = [{"task_id": f"V6623-EXACT-{i:03d}", "title": title, "state": "exact_gate_unexecuted"} for i, title in enumerate(EXACT_TITLES, 1)]
BLOCKED_TITLES = [
    "Fabricate empirical GMUT confirmation or a Theory-of-Everything result",
    "Claim AGI, ASI, consciousness, personhood, continuity, employment, qualification, or authority from relational language",
    "Merge, overwrite, delete, or erase sibling identities, lanes, memory, failures, gates, branches, worktrees, or callers",
    "Publish credentials, private routes, raw task identifiers, private paths, nonpublic conversation, session streams, or application state",
    "Declare Stage 20 readiness without exact external evidence and competent authority",
]
BLOCKED_QUEUE = [{"task_id": f"V6623-BLOCK-{i:03d}", "title": title, "state": "blocked_unexecuted"} for i, title in enumerate(BLOCKED_TITLES, 1)]

_LEGACY_SELF_SKILL_SPECS_IGNORED = [
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
SELF_SKILL_SPECS = [
    ("ghc-family-herbarium-sheet-identity", "Validate purpose-bound synthetic sheet, folder and cabinet identities, revision, minimization, correction, and handling refusal."),
    ("ghc-family-herbarium-sheet-topology", "Check substrate, pressed-organ, label-zone, barcode, annotation and fragment-packet topology with orphan quarantine."),
    ("ghc-family-herbarium-folded-organ", "Preserve folded-organ, reverse-view, overlap, attachment and uncertainty obligations without botanical inference."),
    ("ghc-family-herbarium-label-chronology", "Preserve verbatim label, annotation, determination, contradiction, correction and taxonomy-abstention obligations."),
    ("ghc-family-herbarium-fragment-packet", "Check fragment source-sheet links, packet token, discrepancy, correction, and no reassociation action."),
    ("ghc-family-herbarium-digitisation-envelope", "Track content-free whole-sheet, barcode, scale, colour-target and derivative tokens without imaging or rights claims."),
    ("ghc-family-herbarium-hazard-hold", "Keep pest, mould, residue, pesticide and sharp-element vacancies quarantined from identification or treatment."),
    ("ghc-family-herbarium-accessibility-companion", "Expose ordered regions, folded-part relations, table headers, uncertainty phrases and reserved human review."),
    ("ghc-family-gmut-pressed-organ-firewall", "Preserve typed adjacency, fold, deformation, unit, covariance, identifiability and observation-firewall obligations."),
    ("ghc-family-herbarium-biocultural-authority", "Keep locality, land, traditional knowledge, taonga, benefit, repatriation, remedy and Māori decisions unoccupied."),
]
SUCCESSOR_SKILL_SEEDS = [{"name": name.replace("herbarium", "later-domain"), "recipient": "Vesper Arlen", "state": "recommendation_only", "completion_credit": 0} for name, _ in SELF_SKILL_SPECS]
SELF_RUNNER_SPECS = [(name.replace("ghc-family-", "ghc_family_").replace("-", "_") + ".py", purpose) for name, purpose in SELF_SKILL_SPECS]
SUCCESSOR_RUNNER_SEEDS = [{"name": name.replace("herbarium", "later_domain"), "recipient": "Vesper Arlen", "state": "recommendation_only", "completion_credit": 0} for name, _ in SELF_RUNNER_SPECS]

SELF_CLEAN_CATEGORIES = [
    "retain every inherited and current negative without folding it into a pass", "refresh count mirrors only from authoritative ledgers",
    "preserve Git-blob and logical-text hash-domain declarations", "pin UTF-8 before Unicode-emitting diagnostics",
    "split Windows probes into bounded scalar receipts", "keep expected-empty branch and remote checks null-safe",
    "preserve family-current callers and historical compatibility surfaces", "reject stale owner and phase labels in current-owner artifacts",
    "keep x1 immutable after its four-way-equality gate", "keep x2 implementation absent from x1",
    "keep exact and blocked packets visible and unexecuted", "keep all real plants, specimens, sheets, fragments, people, images, labels, localities, records and connector rows empty",
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
SELF_CLEAN_TASKS = [{"task_id": f"V6623-CLEAN-{i:03d}", "title": title, "owner": OWNER, "mode": "additive_review_only"} for i, title in enumerate(SELF_CLEAN_CATEGORIES, 1)]
SUCCESSOR_CLEAN_SEEDS = [{"task_id": f"V6623-REC-CLEAN-{i:03d}", "title": title, "recipient": "Vesper Arlen", "completion_credit": 0} for i, title in enumerate(SELF_CLEAN_CATEGORIES, 1)]

OFFICIAL_SOURCES = [
    ("TDWG-DWC", "official_biodiversity_information_standards_tdwg", "https://dwc.tdwg.org/terms/", "Darwin Core preserved-specimen, material-entity, identification, material-citation, label and provenance vocabulary only; no real specimen, publication, conformance or taxonomic conclusion."),
    ("INDEX-HERBARIORUM", "official_new_york_botanical_garden_index_herbariorum", "https://sweetgum.nybg.org/science/ih/", "Herbarium-code, permanent-repository and collection-directory vocabulary only; no registration, institutional status, staff claim, endorsement or authority."),
    ("KEW-HERBARIUM", "official_royal_botanic_gardens_kew", "https://www.kew.org/science/collections-and-resources/collections/herbarium", "Dried-specimen, storage, catalogue, arrangement, access, loan and digitisation vocabulary only; no Kew applicability, specimen access, botanical conclusion or professional authority."),
    ("KEW-DIGITISATION", "official_royal_botanic_gardens_kew", "https://www.kew.org/science/collections-and-resources/research-facilities/digitisation-suite", "Whole-sheet image, barcode, stable-URI, scale-bar, colour-chart and data-capture vocabulary only; zero imaging, calibration, rights clearance, publication or facility use."),
    ("SMITHSONIAN-HERBARIUM-GUIDE", "official_smithsonian_national_museum_of_natural_history", "https://naturalhistory.si.edu/research/botany/news/plant-press/guide-collecting-plant-specimens-us-national-herbarium", "Sheet, pressing, label, field-number, mounting and permission vocabulary only; no collecting, pressing, drying, mounting, shipment, donation or Smithsonian applicability."),
    ("GBIF-DWCA", "official_global_biodiversity_information_facility", "https://ipt.gbif.org/manual/en/ipt/latest/dwca-guide", "Darwin Core Archive, stable core-ID, occurrence and extension vocabulary only; zero rows, uploads, publication, registration, conformance or network operation."),
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
SOURCE_STATUS = {
    source_id: (
        "official_or_primary_checked_2026_08_06"
        if source_id in {
            "TDWG-DWC", "INDEX-HERBARIORUM", "KEW-HERBARIUM",
            "KEW-DIGITISATION", "SMITHSONIAN-HERBARIUM-GUIDE", "GBIF-DWCA",
        }
        else "inherited_current_or_stable"
    )
    for source_id, *_ in OFFICIAL_SOURCES
}


def _startup_failure(negative_id: str, signature: str, recovery: str) -> dict[str, object]:
    return {"negative_id": negative_id, "signature": signature, "recovery": recovery, "recovery_passed": True, "completion_credit": 0}


_LEGACY_STARTUP_FAILURE_ROWS_IGNORED = [
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
_STARTUP_FAILURE_ROWS = [
    ("first_memory_lookup_called_an_unavailable_nested_exec_command_alias", "Use the declared shell-command surface for later bounded memory and repository probes."),
    ("first_combined_source_packet_and_git_probe_timed_out_before_attributable_results", "Split packet, head, branch, ancestry, clean-state and live-remote checks into literal scalar probes."),
    ("first_full_activation_packet_display_exceeded_the_output_budget_and_was_truncated", "Read the exact committed packet in numbered bounded windows through verified EOF."),
    ("first_skill_inventory_wrapper_omitted_a_powershell_closing_brace", "Retain the parse failure, correct only the wrapper syntax, and reread each selected skill through EOF."),
    ("parallel_clean_state_wrapper_timed_out_before_returning_all_predicates", "Check staged, unstaged and untracked state with separate bounded Git predicates."),
    ("first_batched_manifest_replay_deadlocked_after_writing_batch_input_without_draining_both_pipes", "Use one bounded batch process with communicate-style concurrent stdin, stdout and stderr handling, then stop only the two leaked exact batch children."),
    ("worktree_add_wrapper_timed_out_while_the_in_scope_checkout_child_continued", "Do not retry creation; poll only the exact in-scope path and process, then award credit after exact-head, branch and clean-state proof."),
    ("first_broad_post_creation_instruction_inventory_exceeded_the_output_budget", "Use narrow literal-file line windows and symbol searches instead of a cross-file full-text projection."),
    ("combined_x1_design_inspection_wrapper_timed_out_before_yielding_trustworthy_output", "Split data, builder, test and status inspection into independent bounded literal probes."),
    ("one_line_frozen_index_rg_projection_expanded_the_entire_json_document", "Parse the exact JSON structure and project only matched proposal identifiers and titles."),
    ("first_stale_label_rg_wrapper_misquoted_an_embedded_double_quote_as_a_path", "Use a short single-quoted alternation without embedded quote literals, then inspect route fields in a separate exact probe."),
    ("first_select_string_stale_label_wrapper_bound_a_colon_fragment_as_a_positional_argument", "Avoid mixed nested quoting and use one bounded literal alternation per source file."),
    ("first_route_field_rg_wrapper_hung_under_a_malformed_quoted_pattern", "Terminate only the exact timed-out read-only wrapper and rerun a short route-field alternation with no embedded quote tokens."),
    ("first_herbarium_novelty_preflight_found_one_accessibility_title_at_the_exact_zero_point_six_threshold", "Retain the failed title screen at zero novelty credit, preserve the contract scope, use distinct nonvisual-layout vocabulary, and rerun only the read-only novelty dependency."),
    ("combined_phase_directory_and_untracked_file_probe_hung_before_returning_either_result", "Terminate only the exact read-only wrapper, check phase-directory absence separately, then query a literal owner-path Git allowlist."),
    ("repository_wide_untracked_scan_exceeded_its_bound_after_the_exact_owner_allowlist_was_staged", "Stop the broad read-only process, preserve zero credit, and rely on the exact staged allowlist plus literal owner-path untracked checks for this phase boundary."),
]
STARTUP_FAILURES = [_startup_failure(f"V6623-X1-N{i:03d}", signature, recovery) for i, (signature, recovery) in enumerate(_STARTUP_FAILURE_ROWS, 1)]
PREFILLED_X1_X2_FAILURES_IGNORED: tuple[dict[str, object], ...] = tuple()
X2_FAILURES: list[dict[str, object]] = []
