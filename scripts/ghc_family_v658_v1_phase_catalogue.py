#!/usr/bin/env python3
"""Frozen x1 catalogue for Elowen Cairn's v658-v1 phase."""

from __future__ import annotations


def source(
    source_id: str,
    title: str,
    publisher: str,
    url: str,
    status: str,
    use: str,
) -> dict:
    return {
        "source_id": source_id,
        "title": title,
        "publisher": publisher,
        "url": url,
        "status": status,
        "observed_on": "2026-08-01",
        "use": use,
    }


OFFICIAL_SOURCES = [
    source(
        "UNESCO-DRY-STONE-2018",
        "Art of dry stone walling, knowledge and techniques",
        "UNESCO Intangible Cultural Heritage",
        "https://ich.unesco.org/en/decisions/13.com/10.b.10",
        "stable",
        "international heritage and community-transmission context only; no conservation, practice, ownership, or cultural-authority determination",
    ),
    source(
        "UNESCO-DRY-STONE-2024",
        "Art of dry stone construction, knowledge and techniques",
        "UNESCO Intangible Cultural Heritage",
        "https://ich.unesco.org/en/RL/art-of-dry-stone-construction-knowledge-and-techniques-02106?RL=02106",
        "current",
        "current inscription vocabulary and community-context boundaries only; no local status, consent, practice, or authority inference",
    ),
    source(
        "HISTORIC-ENGLAND-REPAIR",
        "Principles of Repair for Historic Buildings",
        "Historic England",
        "https://historicengland.org.uk/advice/technical-advice/buildings/principles-of-repair-for-historic-buildings/",
        "current",
        "compatibility, minimal intervention, reversibility, evidence retention, and repair-record vocabulary only",
    ),
    source(
        "HISTORIC-ENGLAND-MAINTENANCE",
        "Maintenance and Repair of Older Buildings",
        "Historic England",
        "https://historicengland.org.uk/advice/technical-advice/buildings/maintenance-and-repair-of-older-buildings/",
        "current",
        "inspection, maintenance, defect-observation, and specialist-referral context only; no real building assessment",
    ),
    source(
        "HSE-STONE-SERIES",
        "Stonemasonry health and safety guidance series",
        "UK Health and Safety Executive",
        "https://www.hse.gov.uk/pubns/guidance/stseries.htm",
        "current",
        "hazard-recognition and stop-work vocabulary only; no work method, safety approval, or jurisdictional determination",
    ),
    source(
        "HSE-STONE-START",
        "Getting started in stonemasonry health and safety",
        "UK Health and Safety Executive",
        "https://www.hse.gov.uk/stonemasonry/getting-started.htm",
        "current",
        "high-level stonemasonry hazard and competence context only; no real task authorization or instruction",
    ),
    source(
        "WORKSAFE-NZ-SILICA",
        "Silica dust in the workplace",
        "WorkSafe New Zealand",
        "https://www.worksafe.govt.nz/topic-and-industry/dust/silica-dust-in-the-workplace/",
        "current",
        "New Zealand silica-hazard and risk-control context only; no exposure assessment, work method, or clearance",
    ),
    source(
        "WORKSAFE-NZ-CONSTRUCTION",
        "Construction",
        "WorkSafe New Zealand",
        "https://www.worksafe.govt.nz/topic-and-industry/construction/",
        "current",
        "New Zealand construction duty and hazard context only; no site, person, work, competence, or safety determination",
    ),
    source(
        "BIPM-SI-9",
        "The International System of Units (SI Brochure), ninth edition",
        "Bureau International des Poids et Mesures",
        "https://www.bipm.org/en/publications/si-brochure",
        "current",
        "units, quantities, dimensions, and expression obligations only; no real measurement or calibration claim",
    ),
    source(
        "BIPM-JCGM-GUIDES",
        "JCGM Guides in Metrology",
        "Bureau International des Poids et Mesures",
        "https://www.bipm.org/en/web/guest/publications/guides",
        "current",
        "uncertainty, traceability, and metrology vocabulary only; no laboratory or field-measurement authority",
    ),
    source(
        "NIST-TRACEABILITY",
        "Metrological Traceability",
        "National Institute of Standards and Technology",
        "https://www.nist.gov/metrology/metrological-traceability",
        "current",
        "traceability-chain and uncertainty-context vocabulary only; no NIST endorsement or calibration result",
    ),
    source(
        "NIST-MEASUREMENTS",
        "Measurements and Calibrations",
        "National Institute of Standards and Technology",
        "https://www.nist.gov/pml/productsservices/measurements-calibrations",
        "current",
        "measurement-service and calibration-context vocabulary only; no service use, certificate, or measured result",
    ),
    source(
        "W3C-PROV",
        "PROV family of specifications",
        "World Wide Web Consortium",
        "https://www.w3.org/groups/wg/prov/publications/",
        "stable",
        "entity, activity, agent-placeholder, derivation, revision, invalidation, and attribution lineage",
    ),
    source(
        "W3C-WCAG-22",
        "Web Content Accessibility Guidelines 2.2",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/WCAG22/",
        "stable",
        "machine-checkable report structure and accessibility vocabulary; manual and affected-user evaluation remain reserved",
    ),
    source(
        "W3C-VC-DM-20",
        "Verifiable Credentials Data Model v2.0",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/vc-data-model-2.0/",
        "stable",
        "synthetic credential role, status, validity, disclosure, and lifecycle vocabulary only; no live identity operation",
    ),
    source(
        "W3C-DATA-INTEGRITY",
        "Verifiable Credential Data Integrity 1.0",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/vc-data-integrity/",
        "stable",
        "synthetic proof-configuration and verification-result schema vocabulary only; no real key, proof, or interoperability",
    ),
    source(
        "RFC-3339",
        "Date and Time on the Internet: Timestamps",
        "RFC Editor",
        "https://www.rfc-editor.org/rfc/rfc3339.html",
        "stable",
        "synthetic observation, revision, validity, expiry, and handover timestamps",
    ),
    source(
        "RFC-8785",
        "JSON Canonicalization Scheme",
        "RFC Editor",
        "https://www.rfc-editor.org/rfc/rfc8785.html",
        "stable",
        "deterministic synthetic JSON representation vocabulary only; no cryptographic or production assurance",
    ),
    source(
        "NZ-PRIVACY-PRINCIPLES",
        "Privacy principles",
        "Office of the Privacy Commissioner New Zealand",
        "https://www.privacy.org.nz/privacy-principles/",
        "current",
        "privacy minimization, notice, access, correction, retention, use, and disclosure context only; no legal advice or compliance finding",
    ),
    source(
        "HERITAGE-NZ-ACT-S4",
        "Heritage New Zealand Pouhere Taonga Act 2014, section 4",
        "New Zealand Legislation",
        "https://www.legislation.govt.nz/act/public/2014/26/en/latest/sections/DLM4005421/",
        "current",
        "statutory-purpose and Treaty-principle context only; no legal interpretation, permission, site status, or authority",
    ),
    source(
        "ICOMOS-NZ-CHARTER",
        "ICOMOS New Zealand Charter for the Conservation of Places of Cultural Heritage Value",
        "ICOMOS New Zealand",
        "https://icomos.org.nz/wp-content/uploads/2020/12/NZ_Charter.pdf",
        "stable",
        "conservation-process, evidence, setting, intervention, record, and stakeholder-context vocabulary only; no charter conformance claim",
    ),
    source(
        "TE-MANA-RARAUNGA",
        "Principles of Māori Data Sovereignty",
        "Te Mana Raraunga",
        "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
        "current",
        "Māori data-sovereignty reservation and authority-routing context only; no substitution for tangata whenua, iwi, hapū, or Māori authority",
    ),
    source(
        "LOCAL-CONTEXTS-TK-MULTI",
        "TK Multiple Communities Label",
        "Local Contexts",
        "https://localcontexts.org/label/tk-multiple-communities/",
        "current",
        "community-plurality, custodianship, provenance, and non-unilateral-labeling context only; no label application or community authority",
    ),
]


PROTECTED_GATES = [
    "real_owners_landholders_occupiers_wallers_engineers_conservators_workers_visitors_communities_and_affected_parties",
    "real_sites_walls_stones_foundations_ground_loads_weather_water_vegetation_tools_equipment_and_measurements",
    "real_access_inspection_handling_lifting_cutting_dressing_dismantling_rebuilding_repair_maintenance_or_release",
    "real_structural_condition_stability_collapse_risk_safety_exposure_measurement_calibration_or_professional_judgment",
    "real_likelihood_prediction_parameter_constraint_detected_force_material_law_empirical_gmut_confirmation_or_theory_of_everything",
    "professional_wallers_engineering_conservation_archaeology_heritage_health_and_safety_privacy_security_or_accessibility_authority",
    "land_title_property_access_planning_building_consent_heritage_protection_liability_insurance_and_legal_interpretation",
    "landscape_traditional_knowledge_culturally_restricted_information_taonga_and_collective_interests",
    "production_identity_live_keys_signatures_proofs_issuance_resolution_status_revocation_interoperability_recovery_and_trust",
    "privacy_complete",
    "exhaustive_security",
    "complete_accessibility",
    "legal_cultural_language_heritage_data_governance_and_maori_authority",
    "affected_party_consent_notice_contestation_remedy_collective_governance_and_acceptance",
    "independent_team_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]


def proposal(
    number: int,
    title: str,
    slug: str,
    pillar: str,
    mechanism: str,
    sources: list[str],
) -> dict:
    if number <= 23:
        expected_disposition = "completed"
        approval = "safe_now_bounded_structural_formal_or_synthetic_software"
        lane = "x2_owner_local_bounded_synthetic"
    elif number <= 28:
        expected_disposition = "represented"
        approval = "candidate_proxy_protocol_or_nonproduction_schema"
        lane = "x2_owner_local_representation_only"
    elif number == 29:
        expected_disposition = "open_gap"
        approval = "candidate_external_readiness_without_network_call"
        lane = "x2_owner_local_zero_row_readiness"
    else:
        expected_disposition = "exact_gate"
        approval = "exact_approval_authorized_affected_party_required"
        lane = "not_executed_authority_reservation"
    return {
        "proposal_id": f"V6581-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar_relation": pillar,
        "mechanism": mechanism,
        "hypothesis": (
            f"A bounded {mechanism} contract can expose falsifiable synthetic obligations "
            "while refusing unsupported real-site, empirical, participant, professional, safety, "
            "production, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, "
            "identity, Theory-of-Everything, or Stage 20 promotion."
        ),
        "null_or_failure_condition": (
            f"The artifact omits a required {mechanism} obligation, accepts a frozen mutation, "
            "erases a failure, or crosses a protected site, person, stone, structure, measurement, "
            "work, rights, professional, empirical, production, legal, cultural, Māori-authority, "
            "identity, privacy, accessibility, security, Theory-of-Everything, or Stage 20 gate."
        ),
        "approval_class": approval,
        "execution_lane": lane,
        "official_or_primary_source_needs": sources,
        "concrete_artifacts": [
            f"surfaces/{slug}/contract.json",
            f"surfaces/{slug}/mutation-results.json",
            f"surfaces/{slug}/bounded-receipt.json",
        ],
        "falsifier_or_acceptance_gate": (
            "The valid synthetic fixture passes, five preregistered mutations are rejected, and "
            "the receipt grants no real person, site, wall, stone, measurement, work, structural, "
            "safety, professional, production, legal, cultural, Māori-authority, identity, privacy-complete, "
            "accessibility-complete, exhaustive-security, independent-reproduction, Theory-of-Everything, "
            "or Stage 20 credit."
        ),
        "rollback_or_recovery": (
            "Stop, retain the failed witness at zero credit, rewrite no history, and leave real "
            "people, sites, land, walls, stones, measurements, work, sibling lanes, external systems, "
            "and authority state unchanged."
        ),
        "protected_gates": PROTECTED_GATES,
        "expected_disposition": expected_disposition,
    }


PROPOSAL_SPECS = [
    ("Dry-stone work-request quarantine with purpose, location placeholder, access precondition, reversible intake, abort rule, and no-work-start lock", "ds-work-request-lock", "THOS Body and CBR Heart", "work request, purpose, location placeholder, access precondition, reversible intake, abort, and work-start refusal", ["HISTORIC-ENGLAND-MAINTENANCE", "WORKSAFE-NZ-CONSTRUCTION", "W3C-PROV"]),
    ("Wall-segment locator with synthetic segment code, endpoint convention, orientation, adjacency, revision lineage, and no-site-identification rule", "ds-segment-locator", "THOS Body and Freed ID", "synthetic wall-segment identity, orientation, adjacency, revision, and site-identification refusal", ["W3C-PROV", "RFC-3339", "NZ-PRIVACY-PRINCIPLES"]),
    ("Land-access and ownership authority hold with role placeholders, permission states, expiry, contest route, and no-entry decision", "ds-land-access-hold", "CBR Heart and Freed ID", "land access, ownership placeholder, permission state, expiry, contestation, and entry-decision refusal", ["HERITAGE-NZ-ACT-S4", "NZ-PRIVACY-PRINCIPLES", "W3C-PROV"]),
    ("Weather-exposure observation envelope with wind, rain, freeze-thaw placeholder, epoch, missingness, uncertainty, and no-deterioration prediction", "ds-weather-envelope", "GMUT Mind and THOS Body", "weather exposure, observation epoch, missingness, uncertainty, and deterioration-prediction refusal", ["BIPM-SI-9", "BIPM-JCGM-GUIDES", "HISTORIC-ENGLAND-MAINTENANCE"]),
    ("Stone-lot provenance register with synthetic lot, source placeholder, custody event, reuse state, correction, and no-origin authentication", "ds-stone-lot-provenance", "Freed ID and THOS Body", "stone-lot identity, source placeholder, custody, reuse, correction, and origin-authentication refusal", ["W3C-PROV", "RFC-3339", "ICOMOS-NZ-CHARTER"]),
    ("Stone geometry envelope with length, breadth, depth, shape class, unit, tolerance, uncertainty, and no-fit instruction", "ds-stone-geometry", "GMUT Mind and THOS Body", "stone geometry, units, tolerance, uncertainty, missingness, and fit-instruction refusal", ["BIPM-SI-9", "BIPM-JCGM-GUIDES", "NIST-TRACEABILITY"]),
    ("Face-course, hearting, and core topology with synthetic stone nodes, contact edges, void placeholders, revision, and no-construction sequence", "ds-course-core-topology", "THOS Body and GMUT Mind", "face-course, hearting, core topology, stone nodes, contact edges, void placeholders, and construction-sequence refusal", ["UNESCO-DRY-STONE-2018", "W3C-PROV", "HISTORIC-ENGLAND-REPAIR"]),
    ("Wall-batter profile envelope with reference plane, station convention, offset, unit, covariance, stale-state hold, and no-plumb judgment", "ds-batter-profile", "GMUT Mind", "wall batter, reference plane, station offset, covariance, stale-state hold, and plumb-judgment refusal", ["BIPM-SI-9", "BIPM-JCGM-GUIDES", "NIST-MEASUREMENTS"]),
    ("Through-stone tie topology with span placeholder, face linkage, course relation, ambiguity, invalidation, and no-placement instruction", "ds-through-stone-topology", "THOS Body and GMUT Mind", "through-stone topology, face linkage, course relation, ambiguity, invalidation, and placement-instruction refusal", ["UNESCO-DRY-STONE-2024", "W3C-PROV", "HISTORIC-ENGLAND-REPAIR"]),
    ("Foundation-ground interface ledger with substrate placeholder, bearing-zone geometry, drainage relation, uncertainty, quarantine, and no-bearing-capacity claim", "ds-foundation-interface", "GMUT Mind and THOS Body", "foundation-ground interface, substrate placeholder, bearing zone, drainage relation, uncertainty, and capacity-claim refusal", ["BIPM-SI-9", "HISTORIC-ENGLAND-REPAIR", "W3C-PROV"]),
    ("Drainage and seepage path graph with source placeholder, ingress, egress, ponding, obstruction, epoch, and no-remediation instruction", "ds-water-path", "THOS Body and GMUT Mind", "drainage, seepage path, ingress, egress, ponding, obstruction, epoch, and remediation-instruction refusal", ["HISTORIC-ENGLAND-MAINTENANCE", "W3C-PROV", "RFC-3339"]),
    ("Vegetation and biological-growth observation register with species placeholder, root-zone relation, extent, uncertainty, escalation, and no-removal instruction", "ds-vegetation-observation", "THOS Body and CBR Heart", "vegetation, biological growth, root-zone relation, extent, uncertainty, escalation, and removal-instruction refusal", ["HISTORIC-ENGLAND-MAINTENANCE", "W3C-PROV", "ICOMOS-NZ-CHARTER"]),
    ("Bulge, lean, and out-of-plane observation matrix with station, reference, sign convention, uncertainty, covariance, and no-stability verdict", "ds-movement-observation", "GMUT Mind", "bulge, lean, out-of-plane observation, reference, sign, uncertainty, covariance, and stability-verdict refusal", ["BIPM-JCGM-GUIDES", "NIST-TRACEABILITY", "BIPM-SI-9"]),
    ("Displacement change envelope with paired epochs, datum placeholder, interval, correlated uncertainty, significance refusal, and correction lineage", "ds-displacement-envelope", "GMUT Mind and Freed ID", "paired displacement epochs, datum placeholder, interval, covariance, significance refusal, and correction", ["BIPM-JCGM-GUIDES", "NIST-TRACEABILITY", "W3C-PROV"]),
    ("Photogrammetry surrogate manifest with synthetic frames, camera placeholder, scale target, control-point uncertainty, occlusion, and no-survey equivalence", "ds-photogrammetry-surrogate", "THOS Body and GMUT Mind", "synthetic photogrammetry frames, scale, controls, uncertainty, occlusion, and survey-equivalence refusal", ["BIPM-JCGM-GUIDES", "W3C-PROV", "NIST-MEASUREMENTS"]),
    ("GMUT dry-stone static-equilibrium proxy with typed force placeholders, moment convention, boundary conditions, residual, and no-real-load inference", "ds-gmut-equilibrium-proxy", "GMUT Mind", "typed static equilibrium, force placeholders, moments, boundary conditions, residuals, and real-load-inference refusal", ["BIPM-SI-9", "BIPM-JCGM-GUIDES", "W3C-PROV"]),
    ("GMUT friction-contact proxy with normal-force placeholder, coefficient interval, slip inequality, unit checks, uncertainty, and no-material calibration", "ds-gmut-contact-proxy", "GMUT Mind", "friction contact, normal-force placeholder, coefficient interval, slip inequality, uncertainty, and material-calibration refusal", ["BIPM-SI-9", "BIPM-JCGM-GUIDES", "NIST-TRACEABILITY"]),
    ("GMUT granular-interlock identifiability tribunal with contact network, geometry, friction, loading, boundary, and confounding alternatives", "ds-gmut-interlock-identifiability", "GMUT Mind", "granular interlock, contact network, geometry, friction, loading, boundary confounding, and causal-claim refusal", ["BIPM-JCGM-GUIDES", "W3C-PROV", "NIST-TRACEABILITY"]),
    ("Dry-stone load-path graph with synthetic contacts, tributary placeholders, support nodes, disconnected components, cycle checks, and no-capacity release", "ds-load-path-graph", "GMUT Mind and THOS Body", "load-path graph, contacts, tributary placeholders, support nodes, connectivity, cycles, and capacity-release refusal", ["BIPM-SI-9", "W3C-PROV", "HISTORIC-ENGLAND-REPAIR"]),
    ("Reversible-intervention option graph with observe, protect, refer, record, defer, undo conditions, evidence cost, and no-repair selection", "ds-reversible-options", "THOS Body and CBR Heart", "reversible intervention options, observation, protection, referral, deferral, undo conditions, and repair-selection refusal", ["HISTORIC-ENGLAND-REPAIR", "ICOMOS-NZ-CHARTER", "W3C-PROV"]),
    ("Salvage and reuse mass-balance ledger with synthetic inventory, retained fraction, waste placeholder, discrepancy, lineage, and no-disposal decision", "ds-salvage-mass-balance", "THOS Body and Freed ID", "salvage inventory, reuse mass balance, retained fraction, discrepancy, provenance, and disposal-decision refusal", ["HISTORIC-ENGLAND-REPAIR", "W3C-PROV", "RFC-8785"]),
    ("Condition-grade vocabulary firewall with observation facts, uncertainty, assessor placeholder, escalation state, and no-professional grade assignment", "ds-condition-grade-firewall", "THOS Body and CBR Heart", "condition observations, uncertainty, assessor placeholder, escalation, and professional-grade refusal", ["HISTORIC-ENGLAND-MAINTENANCE", "ICOMOS-NZ-CHARTER", "W3C-PROV"]),
    ("Work-zone, manual-handling, cutting, dust, and silica stop-state board with hazard flags, competent-person hold, emergency route, and no-work instruction", "ds-safety-stop-board", "THOS Body and CBR Heart", "work-zone, handling, cutting, dust, silica, stop state, competent-person hold, and work-instruction refusal", ["HSE-STONE-SERIES", "WORKSAFE-NZ-SILICA", "WORKSAFE-NZ-CONSTRUCTION"]),
    ("THOS dry-stone shift and workload handover proxy with matched synthetic event budget, interruption log, stop threshold, readback, and no-operator evidence", "thos-ds-handover-proxy", "THOS Body", "synthetic workload, matched event budget, interruption, stop threshold, readback, handover, and operator-evidence refusal", ["RFC-3339", "W3C-WCAG-22", "WORKSAFE-NZ-CONSTRUCTION"]),
    ("Freed ID synthetic wall-segment custody receipt with pseudonymous segment, observation event, validity window, correction, expiry, and nonproduction boundary", "freed-id-ds-segment-custody", "Freed ID and CBR Heart", "synthetic wall-segment custody, pseudonym, observation event, validity, correction, expiry, and production refusal", ["W3C-VC-DM-20", "W3C-PROV", "NZ-PRIVACY-PRINCIPLES"]),
    ("Freed ID synthetic stone-part provenance graph with lot, part, position placeholder, derivation, revision, invalidation, redaction, and no-property claim", "freed-id-ds-part-provenance", "Freed ID and CBR Heart", "synthetic stone-part provenance, lot, position placeholder, derivation, revision, invalidation, redaction, and property-claim refusal", ["W3C-PROV", "RFC-8785", "NZ-PRIVACY-PRINCIPLES"]),
    ("Freed ID synthetic wall credential proof and lifecycle profile with suite placeholder, status, expiry, recovery, unlinkability hold, and no-live verification", "freed-id-ds-proof-lifecycle", "Freed ID and THOS Body", "synthetic wall credential, proof placeholder, status, expiry, recovery, unlinkability hold, and live-verification refusal", ["W3C-VC-DM-20", "W3C-DATA-INTEGRITY", "RFC-3339"]),
    ("Community maintenance workload protocol with invitation placeholder, voluntary participation, matched synthetic budget, abort, feedback, remedy route, and no-acceptance claim", "cbr-ds-community-workload", "CBR Heart and THOS Body", "community workload protocol, invitation placeholder, voluntary participation, matched budget, abort, feedback, remedy, and acceptance-claim refusal", ["UNESCO-DRY-STONE-2024", "W3C-WCAG-22", "NZ-PRIVACY-PRINCIPLES"]),
    ("Official dry-stone and heritage source adapter with zero-row default, declared query placeholder, provenance, schema quarantine, no network call, and no evidence promotion", "ds-official-zero-row-adapter", "THOS Body and GMUT Mind", "official-source adapter, zero-row default, query placeholder, provenance, schema quarantine, no-network execution, and evidence-promotion refusal", ["UNESCO-DRY-STONE-2024", "HISTORIC-ENGLAND-REPAIR", "HERITAGE-NZ-ACT-S4"]),
    ("CBR land, landscape, heritage, traditional-knowledge, affected-party, and Māori-data authority covenant with refusal-by-default and no unilateral wording", "cbr-ds-authority-covenant", "CBR Heart across all pillars", "land, landscape, heritage, traditional knowledge, affected-party, Māori-data, tangata whenua, iwi, hapū, and Māori-authority reservation", ["HERITAGE-NZ-ACT-S4", "ICOMOS-NZ-CHARTER", "TE-MANA-RARAUNGA", "LOCAL-CONTEXTS-TK-MULTI"]),
]


PROPOSALS = [proposal(index, *spec) for index, spec in enumerate(PROPOSAL_SPECS, 1)]


SKILL_SPECS = [
    ("ghc-family-dry-stone-intake-boundary", "Constrain purpose, site placeholders, access, role, abort, and no-work-start states."),
    ("ghc-family-dry-stone-segment-provenance", "Constrain segment, stone-lot, revision, derivation, correction, invalidation, and redaction lineage."),
    ("ghc-family-dry-stone-geometry-uncertainty", "Constrain units, references, geometry, tolerance, covariance, missingness, and traceability refusal."),
    ("ghc-family-dry-stone-structure-topology", "Constrain course, core, through-stone, contact, support, connectivity, and capacity refusal."),
    ("ghc-family-dry-stone-water-vegetation", "Constrain water-path and biological observations while refusing treatment or removal instruction."),
    ("ghc-family-dry-stone-movement-observation", "Constrain bulge, lean, displacement, epoch, datum, uncertainty, and stability-verdict refusal."),
    ("ghc-family-dry-stone-gmut-firewall", "Keep equilibrium, friction, interlock, identifiability, and load-path proxies inside typed research bounds."),
    ("ghc-family-dry-stone-thos-handover", "Constrain workload, interruption, stop state, evidence, ownership, readback, and handover."),
    ("ghc-family-dry-stone-freed-id-custody", "Constrain synthetic custody, proof, status, expiry, recovery, privacy, and nonproduction boundaries."),
    ("ghc-family-dry-stone-authority-reservation", "Fail closed around land, heritage, safety, law, culture, data governance, affected parties, and Māori authority."),
]


RUNNER_SPECS = [
    ("ghc_family_dry_stone_intake_boundary.py", "ds-work-request-lock"),
    ("ghc_family_dry_stone_segment_provenance.py", "ds-stone-lot-provenance"),
    ("ghc_family_dry_stone_geometry_uncertainty.py", "ds-stone-geometry"),
    ("ghc_family_dry_stone_structure_topology.py", "ds-course-core-topology"),
    ("ghc_family_dry_stone_water_vegetation.py", "ds-water-path"),
    ("ghc_family_dry_stone_movement_observation.py", "ds-movement-observation"),
    ("ghc_family_dry_stone_gmut_firewall.py", "ds-gmut-equilibrium-proxy"),
    ("ghc_family_dry_stone_thos_handover.py", "thos-ds-handover-proxy"),
    ("ghc_family_dry_stone_freed_id_custody.py", "freed-id-ds-segment-custody"),
    ("ghc_family_dry_stone_authority_reservation.py", "cbr-ds-authority-covenant"),
]


def negative(number: int, slug: str, failure: str, recovery: str, guard: str) -> dict:
    return {
        "negative_id": f"V6581-X1-N{number:02d}",
        "scope": "startup_and_x1",
        "signature": slug,
        "observed": failure,
        "credit": 0,
        "retained": True,
        "recovery": recovery,
        "recurrence_guard": guard,
        "same_owner_only": True,
        "independent_reproduction": False,
    }


X1_OPERATIONAL_NEGATIVES = [
    negative(1, "combined-required-guidance-read-truncated", "The first grouped required-guidance read exceeded the attributable output window and could not prove every file through EOF.", "Read every required skill, routing reference, state, and schema independently in bounded ranges through EOF.", "Do not combine complete-read obligations into one output window."),
    negative(2, "source-closeout-manifest-whole-render-truncated", "A whole-file render of Tamar's 288-entry closeout manifest truncated before EOF and earned no complete-manifest credit.", "Read the manifest in bounded ordered chunks and independently verify every declared Git blob and size.", "Count long manifest lines or entries first, then inspect bounded ranges and exact objects."),
    negative(3, "x1-manifest-size-property-assumption", "The first source x1-manifest replay assumed git_clean_bytes, while the committed schema declares git_blob_bytes, so the attempt failed at zero credit.", "Inspect the exact manifest keys and replay the declared git_blob and git_blob_bytes fields against commit-local Git objects.", "Discover JSON keys before traversing or projecting an inherited manifest."),
    negative(4, "overbroad-archive-receipt-search-timeout", "A recursive receipt search across the full archive bank ran too long and was stopped after its exact search process was identified.", "Use the authoritative receipt directory and exact final-head filename from the activation, then hash that literal path.", "Never search the whole archive bank when the owner, phase, receipt class, and head are known."),
    negative(5, "overbroad-validation-receipt-search-timeout", "A narrower but still recursive validation-root receipt search ran too long and was stopped without evidence credit.", "Probe only the exact owner-phase external receipt directory and the committed source pointers.", "Reduce receipt discovery to literal owner and phase paths before invoking content search."),
    negative(6, "compact-frozen-index-raw-grep-truncated", "A raw text search matched the entire compact single-line 2,650-proposal index and truncated its output.", "Parse the index object and query exact proposal title fields and bounded vocabulary counts.", "Use schema-aware JSON parsing for compact ledgers instead of line-oriented raw rendering."),
    negative(7, "source-catalogue-multichunk-render-truncated", "The first grouped source-catalogue template render exceeded the useful output window and did not establish a complete read.", "Locate section boundaries, then read only the required helper and schema sections in bounded attributable chunks.", "Map long source files by definitions before selecting bounded ranges."),
    negative(8, "combined-template-and-builder-read-truncated", "A later combined catalogue, test, data, and builder read again exceeded the output window; only complete bounded subreads earned credit.", "Read phase data and tests independently and inspect builder sections by exact function boundary.", "Do not aggregate multiple long implementation templates into one tool result."),
    negative(9, "foreach-result-direct-pipeline-parser-fault", "A PowerShell foreach result was piped without first being materialized, triggering EmptyPipeElement before the intended hash receipt ran.", "Assign the foreach output to a scalar collection, then pipe the completed collection to ConvertTo-Json.", "Materialize direct foreach output before any downstream PowerShell pipeline."),
    negative(10, "parallel-large-worktree-status-lost-attribution", "A parallel large-worktree git status probe yielded and its wrapper retained no session handle or attributable output, so it earned no clean-state credit.", "Use exact owner-path untracked and tracked-diff probes, or supervise and poll a single yielded status session through completion.", "Never discard nested command metadata when a large-worktree Git probe may yield."),
]


SAFE_TASKS = [
    {
        "task_id": f"V6581-SAFE-{index:03d}",
        "proposal_id": item["proposal_id"],
        "task": f"Build and validate the bounded synthetic contract for {item['slug']}.",
        "approval_class": "safe_now_owner_local_additive",
        "x1_execution": False,
        "planned_lane": "x2",
    }
    for index, item in enumerate(PROPOSALS, 1)
]


CANDIDATE_TASKS = [
    {
        "task_id": f"V6581-CAND-{index:03d}",
        "task": f"Prototype a reversible cross-surface refinement for {PROPOSALS[(index - 1) % len(PROPOSALS)]['slug']}.",
        "approval_class": "candidate_owner_local_review_required",
        "x1_execution": False,
        "planned_lane": "x2_if_bounded_evidence_permits",
    }
    for index in range(1, 21)
]


CLEAN_TASKS = [
    {
        "task_id": f"V6581-CLEAN-{index:03d}",
        "task": f"Run additive compatibility, privacy, provenance, stale-label, and nonpromotion cleanup for {item['slug']}.",
        "approval_class": "safe_now_additive_cleanup",
        "x1_execution": False,
        "planned_lane": "x2",
    }
    for index, item in enumerate(PROPOSALS, 1)
]
