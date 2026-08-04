#!/usr/bin/env python3
"""Frozen x1 planning data for Orin Thale v661-v3.

Caelen Ash's immutable v661-v2 surface supplies compatibility vocabulary only.
Twenty inherited rows are selected for bounded revalidation with zero Orin
novelty or completion credit. Only the twenty new rows below extend the
append-only chain. Real floristry work, people, plants, protected data,
professional decisions, empirical claims, production identity, legal or
cultural ratification, and Māori authority remain empty or exact-gated.
"""

from __future__ import annotations

from ghc_family_v661_v2_data import *  # noqa: F401,F403


PHASE = "v661-v3"
CANONICAL_PHASE = PHASE
PHASE_CODE = "V6613"
OWNER = "Orin Thale"
PRONOUNS = "they/them"
ROLE = "relational evidence-and-boundary steward"
HOPE = "keep every surviving claim traceable, falsifiable, and easy to retract"
BRANCH = "codex/GHC-Family/orin-thale-v661-v3-full-tools"
PHASE_ROOT = "docs/orin-thale/v661-v3"

SOURCE_OWNER = "Caelen Ash"
SOURCE_BRANCH = "codex/GHC-Family/caelen-ash-v661-v2-full-tools"
SOURCE_BASE = "0cac4abe8131df05d30e0f744d05bc392d22e73d"
SOURCE_X1 = "d62c0c856df45aec5d828a2da1212be9e8e55718"
SOURCE_EVIDENCE = "23780ad45b681c8eb4de13f114e6a18a8583ed5d"
SOURCE_CLOSEOUT = SOURCE_EVIDENCE
SOURCE_FINAL = "7197e39b3d1ecc29e44d4598405f2975d249345b"
SOURCE_CLOSEOUT_BASE = SOURCE_FINAL
SOURCE_CANONICAL_RECEIPT_SHA256 = (
    "3f3b3e427730973d60e7bcbfbacfbf1ac846c0f251a9262a40d28798aef53e1f"
)
SOURCE_LIVE_ACTIVATION_STATE = "SENT_ONCE_ACKNOWLEDGED"
ACTIVATION_PACKET_SHA256 = (
    "4e8972052c4bbc96e9cb8bfce05979e69b01126b12d0f9a14584c2133fb10e5a"
)
ACTIVATION_PACKET_BYTES = 228751
ACTIVATION_PACKET_LINES = 1074
X1_FREEZE = "pending_until_x2"

PRIOR_FROZEN = 3330
SOURCE_SEALED_NEGATIVES = 21121
SOURCE_EXTERNAL_NEGATIVES = 1
ACTIVATION_NEGATIVES = SOURCE_SEALED_NEGATIVES + SOURCE_EXTERNAL_NEGATIVES
ACTIVATION_MESSAGE_NEGATIVE_BASELINE = 21122
SOURCE_OPEN_GAPS = 139
SOURCE_EXACT_GATES = 138
SOURCE_SEALED_METHODS = 6595
SOURCE_EXTERNAL_METHODS = 1
ACTIVATION_METHODS = SOURCE_SEALED_METHODS + SOURCE_EXTERNAL_METHODS
ACTIVATION_MESSAGE_METHOD_BASELINE = 6596
SELECTED_INHERITED_COUNT = 20
NEW_UNIQUE_COUNT = 20
CURRENT_PORTFOLIO_COUNT = SELECTED_INHERITED_COUNT + NEW_UNIQUE_COUNT
LATEST_TRACKED_SCAN_CAP = 5000

PRIMARY_PILLAR = "Freed ID and CBR Heart"
PRACTICE_LENS = (
    "bounded synthetic community floristry cut-flower intake, stem-lot and "
    "substitution documentation, condition placeholders, accessible collection "
    "notice, correction readback, workload control, and shift handover"
)

EXPECTED_DISTRIBUTION = {
    "completed": 14,
    "represented": 4,
    "open_gap": 1,
    "exact_gate": 1,
}
ALLOWED_OUTCOMES = set(EXPECTED_DISTRIBUTION)

PROTECTED_GATES = [
    "real_flower_orders_stems_foliage_plants_species_lots_bouquets_vessels_tools_chemicals_cold_rooms_vehicles_shops_or_venues",
    "real_growers_importers_florists_workers_couriers_recipients_bystanders_children_affected_parties_regulators_and_authorities",
    "real_receipt_identification_conditioning_cutting_arranging_storage_transport_delivery_treatment_disposal_or_release_action",
    "professional_floristry_botany_biosecurity_plant_health_chemical_safety_accessibility_privacy_or_operational_authority",
    "empirical_gmut_prediction_likelihood_parameter_constraint_observational_confirmation_physical_discovery_or_final_physics",
    "blind_matched_budget_thos_real_arms_governed_participants_operators_safety_monitoring_statistics_and_independent_review",
    "production_identity_live_keys_signatures_proofs_issuance_resolution_status_revocation_interoperability_recovery_and_trust",
    "recipient_identity_address_message_relationship_location_order_history_images_species_provenance_traditional_knowledge_collective_interest_and_remedy",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "legal_cultural_biosecurity_plant_health_product_safety_ownership_custody_access_data_governance_and_maori_authority",
    "affected_party_notice_consent_contestation_correction_restriction_access_return_remedy_collective_governance_and_acceptance",
    "independent_team_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]

SELECTED_INHERITED_IDS = [f"V6612-P{i:03d}" for i in range(1, 21)]


def _proposal(
    slug: str,
    title: str,
    outcome: str,
    pillar: str,
    mechanism: str,
    sources: list[str],
) -> dict[str, object]:
    return {
        "slug": slug,
        "title": title,
        "outcome": outcome,
        "pillar": pillar,
        "mechanism": mechanism,
        "sources": sources,
    }


NEW_PROPOSAL_SPECS = [
    _proposal(
        "floristry-order-identity",
        "Surrogate floristry order identity capsule with purpose, channel, revision, source pin, recipient minimization, cancellation, and fulfilment refusal",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic order and revision tokens, purpose and channel declarations, source pin, recipient minimization, cancellation, correction, tombstone, and zero-real-order states",
        ["W3C-PROV", "W3C-VC2", "NZ-PRIVACY", "IETF-JCS"],
    ),
    _proposal(
        "cut-flower-stem-lot-topology",
        "Cut-flower stem-lot, foliage-lot, container, bundle, arrangement-placeholder, split, merge, substitution, orphan, and physical-handling refusal graph",
        "completed",
        "Freed ID and THOS Body",
        "typed synthetic stem and foliage lots, containers and bundles, split and merge edges, arrangement placeholders, substitutions, orphan quarantine, contradiction retention, and no handling action",
        ["MPI-CUTFLOWER-IHS", "USDA-APHIS-CUTFLOWERS", "W3C-PROV"],
    ),
    _proposal(
        "botanical-claim-quarantine",
        "Floristry botanical-name, supplier-label, stated-origin, taxon-placeholder, uncertainty, conflict, correction, and identification-authority quarantine",
        "completed",
        "Freed ID and CBR Heart",
        "supplier-stated names and origins, taxon placeholders, source distinctions, uncertainty and conflict, correction and supersession, and botanical-identification refusal",
        ["MPI-CUTFLOWER-IHS", "GBIF-OCCURRENCE", "W3C-PROV"],
    ),
    _proposal(
        "conditioning-solution-state",
        "Synthetic cut-flower conditioning-solution, vessel, water-source placeholder, additive-label, preparation-time, contamination cue, compatibility unknown, and use refusal ledger",
        "completed",
        "THOS Body",
        "synthetic vessel and solution tokens, stated water and additive labels, preparation timestamps, contamination cues, compatibility unknowns, quarantine, and zero mixing or application",
        ["MPI-CUTFLOWER-IHS", "MSL-SI", "W3C-PROV"],
    ),
    _proposal(
        "floristry-cold-chain-observation",
        "Floristry storage and transit temperature-placeholder, duration, sensor-status, gap, excursion, uncertainty, correction, and no-quality-inference envelope",
        "completed",
        "GMUT Mind and THOS Body",
        "synthetic temperature and duration placeholders, sensor status, missingness, resolution and uncertainty, excursion flags, correction, and zero real measurement or quality inference",
        ["MSL-SI", "W3C-PROV", "IETF-JCS"],
    ),
    _proposal(
        "floristry-substitution-consent",
        "Floristry requested-item, substitute-option, reason, price-placeholder, preference, consent-unoccupied, withdrawal, correction, and no-allocation decision board",
        "completed",
        "CBR Heart and Freed ID",
        "synthetic requested and substitute tokens, reasons and price placeholders, preference minimization, unoccupied consent, withdrawal and correction, and no allocation or purchase decision",
        ["NZ-PRIVACY", "W3C-PROV", "WCAG22"],
    ),
    _proposal(
        "floristry-allergen-toxicity-hold",
        "Floristry fragrance, pollen, thorn, sap, ingestion, pet-exposure, pesticide-residue unknown, warning-placeholder, referral, and safety-clearance refusal board",
        "completed",
        "CBR Heart and THOS Body",
        "synthetic hazard cues and unknowns, recipient and bystander exposure placeholders, warning and referral states, stop tokens, correction, and zero diagnosis, treatment, handling, or clearance",
        ["MPI-CUTFLOWER-IHS", "USDA-APHIS-CUTFLOWERS", "WCAG22"],
    ),
    _proposal(
        "floristry-correction-lineage",
        "Floristry order, lot, botanical claim, condition-placeholder, substitution, notice, correction, supersession, cancellation, readback, and unresolved-ambiguity lineage",
        "completed",
        "Freed ID and THOS Body",
        "synthetic order and lot assertions, botanical and condition placeholders, substitution and notice claims, correction, supersession, cancellation, readback, ambiguity hold, and non-erasure",
        ["W3C-PROV", "IETF-JCS", "JSON-SCHEMA-2020-12"],
    ),
    _proposal(
        "floral-provenance-custody",
        "Synthetic floristry supplier, stem-lot, custody, transfer, stated-origin, image-placeholder, disclosure mask, correction, and title-refusal covenant",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic supplier and lot placeholders, custody and transfer assertions, stated origin, absent-image references, disclosure masks, correction, contestation, and title refusal",
        ["W3C-PROV", "NZ-PRIVACY", "TE-MANA-RARAUNGA"],
    ),
    _proposal(
        "privacy-minimized-recipient-notice",
        "Privacy-minimized floristry recipient and collection notice with purpose binding, indirect-source flag, contact-channel placeholder, disclosure ceiling, correction path, and delivery refusal",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic recipient aliases, purpose and indirect-source flags, contact-channel placeholders, disclosure ceilings, access and correction routes, retention holds, and zero delivery",
        ["NZ-PRIVACY", "W3C-VC2", "WCAG22"],
    ),
    _proposal(
        "accessible-floristry-companion",
        "Accessible floristry order and collection companion with relational tables, noncolour status, text alternatives, focus order, plain-language holds, and reserved affected-user evaluation",
        "completed",
        "CBR Heart and THOS Body",
        "structural headings, order and lot tables, text alternatives, noncolour status, focus order, status messages, downloadable plain text, and zero manual or affected-user sessions",
        ["WCAG22", "NZ-PRIVACY", "W3C-PROV"],
    ),
    _proposal(
        "gmut-floristry-transport-obligations",
        "GMUT typed advection-diffusion-reaction surrogate for a floristry chain with state vector, boundary flux, source term, dissipation, units, uncertainty, identifiability, and observation firewall",
        "completed",
        "GMUT Mind",
        "typed symbolic lot nodes, transport edges, state and flux placeholders, source and dissipation terms, units and uncertainty, identifiability limits, counterexample slots, and zero observations",
        ["MSL-SI", "W3C-PROV", "IETF-JCS"],
    ),
    _proposal(
        "floristry-action-authorization-firewall",
        "Floristry receipt, identification, conditioning, cutting, arranging, storage, transport, delivery, treatment, disposal, and release action-authorization firewall",
        "completed",
        "CBR Heart and THOS Body",
        "synthetic action requests and scopes with florist, botanist, biosecurity, chemical-safety, recipient, legal, cultural, affected-party, and Māori-authority holds plus execution refusal",
        ["MPI-CUTFLOWER-IHS", "USDA-APHIS-CUTFLOWERS", "NZ-PRIVACY", "TE-MANA-RARAUNGA"],
    ),
    _proposal(
        "stage20-floristry-evidence-board",
        "Terminal evidence antichain for synthetic floristry claims with unfilled plant, participant, authority, infrastructure, empirical, independent-team, and Stage 20 prerequisites",
        "completed",
        "All pillars",
        "typed evidence antichain, unfilled plant, participant, authority, infrastructure, empirical and independent-team prerequisites, non-substitution rules, retained negatives, and terminal abstention",
        ["W3C-PROV", "IETF-JCS", "JSON-SCHEMA-2020-12"],
    ),
    _proposal(
        "gmut-floristry-water-uptake-proxy",
        "GMUT floristry stem-water-uptake, porous-flow, transpiration-placeholder, boundary, covariance, stability, and identifiability proxy with zero plant observations",
        "represented",
        "GMUT Mind",
        "typed symbolic porous-flow and transpiration placeholders, boundary and covariance terms, zero fitted coefficients, zero likelihood rows, and physical-inference abstention",
        ["MSL-SI", "W3C-PROV", "IETF-JCS"],
    ),
    _proposal(
        "thos-floristry-handover",
        "THOS reciprocal floristry shift brief with unresolved order and hazard queues, substitution budget, stop token, correction readback, workload ceiling, and zero workers",
        "represented",
        "THOS Body",
        "synthetic shift brief, unresolved order, hazard and ambiguity queues, substitution budget, workload ceiling, stop token, correction readback, escalation, and zero workers",
        ["WCAG22", "W3C-PROV", "NZ-PRIVACY"],
    ),
    _proposal(
        "floristry-matched-budget-protocol",
        "Preregistered vacancy matrix for two floristry explanation formats with randomized synthetic order packets, balanced exposure time, masked error coding, withdrawal sentinel, and zero enrolment",
        "represented",
        "THOS Body",
        "future randomized synthetic order packets, balanced exposure time, two explanation formats, masked error coding, withdrawal and safety sentinels, zero enrolment, and no effectiveness claim",
        ["WCAG22", "W3C-PROV", "NZ-PRIVACY"],
    ),
    _proposal(
        "freed-id-floristry-order-profile",
        "Freed ID synthetic floristry order, lot, substitution, notice, document, namespace, collision, correction, status-hold, minimization, and nonproduction relation profile",
        "represented",
        "Freed ID and CBR Heart",
        "synthetic order, lot and relation identifiers, namespace and version placeholders, collisions, correction, supersession, status and revocation holds, privacy mask, zero keys or proofs, and nonproduction refusal",
        ["W3C-VC2", "W3C-VC-DI", "NZ-PRIVACY", "IETF-JCS"],
    ),
    _proposal(
        "gbif-cut-flower-zero-row-adapter",
        "GBIF cut-flower taxon and occurrence evidence adapter with query purpose, name match, basis-of-record, location sensitivity, issue flags, pagination, checksum, covariance, likelihood, and zero-row refusal",
        "open_gap",
        "GMUT Mind and Freed ID",
        "zero network calls, occurrence rows, commercial-lot links, botanical determinations, location disclosures, covariance rows, likelihood evaluations, posterior samples, constraints, or empirical claims",
        ["GBIF-OCCURRENCE", "NZ-PRIVACY", "IETF-JCS", "MSL-SI"],
    ),
    _proposal(
        "floristry-rights-authority",
        "Unoccupied authority circuit for plant-health action, recipient privacy, substitution, delivery, disposal, cultural use, remedy, data governance, affected-party legitimacy, and Māori decision non-substitution",
        "exact_gate",
        "CBR Heart",
        "unoccupied grower, importer, florist, worker, courier, recipient, bystander, regulator, accessibility, privacy, biosecurity, legal, cultural, collective-interest, tangata whenua, iwi, hapū, affected-party, remedy, and Māori-authority reservations",
        ["MPI-CUTFLOWER-IHS", "NZ-PRIVACY", "TE-MANA-RARAUNGA", "WCAG22"],
    ),
]

SELF_SAFE_CATEGORIES = [
    "Caelen source head and fresh equality",
    "activation packet and external receipt digests",
    "three-thousand-three-hundred-thirty-row proposal-chain parse",
    "twenty inherited selection identities",
    "twenty-title novelty screen",
    "mechanism-level floristry-neighbour review",
    "new-outcome distribution",
    "workflow-plan policy",
    "identity and relational-language boundary",
    "Hamish-authorized Caelen-to-Orin live edge",
    "solo and Tavian-standby boundaries",
    "D-first posture",
    "toolchain version receipt",
    "x1 artifact inventory",
    "x1 JSON parsing",
    "x1 five-class privacy scan",
    "x1 stale-label review",
    "x1 diff hygiene",
    "x1 manifest replay",
    "selected-row zero-credit guard",
    "new-row append-only guard",
    "source-label glossary",
    "protected-gate coverage",
    "failure-retention ledger",
    "Method Flow witness pairing",
    "wellbeing workload bound",
    "document-word ceiling",
    "portfolio arithmetic",
    "skill and runner arithmetic",
    "no-x2-in-x1 guard",
]
SELF_SAFE_TASKS = [
    {"task_id": f"V6613-SAFE-{i:03d}", "title": f"Validate {name} inside the Orin-owned v661-v3 lane", "owner": OWNER}
    for i, name in enumerate(SELF_SAFE_CATEGORIES, 1)
]
SUCCESSOR_SAFE_SEEDS = [
    {"task_id": f"V6614-REC-SAFE-{i:03d}", "title": f"Reassess {name} for Liora-only v661-v4", "recipient": "Liora Venn", "completion_credit": 0}
    for i, name in enumerate(SELF_SAFE_CATEGORIES[:20], 1)
]

SELF_CANDIDATE_CATEGORIES = [
    "synthetic floristry order identity capsule",
    "stem-lot, foliage-lot, split, merge, and substitution topology tribunal",
    "botanical claim, stated origin, uncertainty, and correction quarantine",
    "conditioning solution, vessel, contamination-cue, and use-refusal ledger",
    "storage and transit placeholder uncertainty envelope",
    "substitution preference and unoccupied-consent board",
    "allergen, thorn, sap, pet-exposure, referral, and no-clearance board",
    "floristry correction and non-erasure lineage",
    "GMUT transport-obligation and observation-firewall board",
    "floristry privacy, plant-health, remedy, and Māori-authority circuit",
]
SELF_CANDIDATE_TASKS = [
    {"task_id": f"V6613-CAND-{i:03d}", "title": f"Build and test reversible {name}", "owner": OWNER}
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]
SUCCESSOR_CANDIDATE_SEEDS = [
    {"task_id": f"V6614-REC-CAND-{i:03d}", "title": f"Consider a distinct Liora-owned refinement of {name}", "recipient": "Liora Venn", "completion_credit": 0}
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]

EXACT_QUEUE = [
    {"task_id": f"V6613-EXACT-{i:03d}", "title": title, "state": "exact_gate_unexecuted"}
    for i, title in enumerate(
        [
            "Receive, identify, condition, cut, arrange, store, transport, deliver, treat, dispose of, or release any real flower, foliage, plant, lot, bouquet, order, or chemical",
            "Make a real botanical-identification, plant-health, biosecurity, allergen, toxicity, chemical-safety, product-safety, quality, or release determination",
            "Use real growers, importers, florists, workers, couriers, recipients, bystanders, children, regulators, plants, orders, or personal information",
            "Disclose private recipient identity, address, message, relationship, location, order history, image, supplier detail, traditional knowledge, or restricted provenance",
            "Make a professional floristry, botany, biosecurity, plant-health, chemical-safety, privacy, security, translation, or accessibility determination",
            "Publish a production order identifier, plant-health record, credential, signature, proof, status, interoperability result, or operational record",
            "Allocate ownership, custody, substitution, delivery, disposal, access, remedy, attribution, beneficiary, or affected-party authority",
            "Make a tikanga, mātauranga, wording, naming, tangata whenua, iwi, hapū, Māori data-governance, cultural-protocol, taonga-status, or Māori-authority decision",
            "Run a real participant study, floristry shift, handling trial, plant-health inspection, professional review, delivery trial, or independent reproduction",
            "Perform destructive cleanup or any mutation outside the exact Orin-owned lane",
        ],
        1,
    )
]
BLOCKED_QUEUE = [
    {"task_id": f"V6613-BLOCK-{i:03d}", "title": title, "state": "blocked_unexecuted"}
    for i, title in enumerate(
        [
            "Fabricate empirical GMUT confirmation or a Theory-of-Everything result",
            "Claim AGI, ASI, consciousness, personhood, continuity, employment, qualification, or authority from relational language",
            "Merge, overwrite, delete, or erase sibling identities, lanes, memory, failures, gates, branches, worktrees, or callers",
            "Publish credentials, private routes, raw task identifiers, private paths, nonpublic conversation, session streams, or application state",
            "Declare Stage 20 readiness without exact external evidence and competent authority",
        ],
        1,
    )
]

SELF_SKILL_SPECS = [
    ("ghc-family-floristry-order-identity", "Validate synthetic purpose-bound floristry order identity, revision, minimization, cancellation, and fulfilment refusal."),
    ("ghc-family-floristry-stem-lot-topology", "Check synthetic stem and foliage lots, containers, splits, merges, substitutions, orphans, and handling refusal."),
    ("ghc-family-floristry-botanical-claim-hold", "Preserve stated botanical names and origins, uncertainty, conflicts, corrections, and identification-authority refusal."),
    ("ghc-family-floristry-conditioning-state", "Preserve synthetic vessels, solutions, additive labels, contamination cues, compatibility unknowns, and use refusal."),
    ("ghc-family-floristry-substitution-consent", "Expose requested items, alternatives, preference minimization, consent vacancy, withdrawal, and no-allocation states."),
    ("ghc-family-floristry-correction-lineage", "Preserve order, lot, claim, substitution, notice, correction, supersession, cancellation, ambiguity, and non-erasure."),
    ("ghc-family-floristry-privacy-minimization", "Keep recipient, address, message, relationship, source, retention, disclosure, and correction data minimized."),
    ("ghc-family-floristry-accessibility-companion", "Expose structural tables, noncolour status, alternatives, focus order, plain-language holds, and reserved human review."),
    ("ghc-family-gmut-floristry-transport", "Preserve typed transport, boundary, source, unit, covariance, stability, identifiability, and observation-firewall obligations."),
    ("ghc-family-floristry-rights-authority", "Keep plant health, privacy, substitution, delivery, remedy, cultural, and Māori decision rights unoccupied."),
]
SUCCESSOR_SKILL_SEEDS = [
    {"name": name.replace("floristry", "successor-domain"), "recipient": "Liora Venn", "state": "recommendation_only", "completion_credit": 0}
    for name, _ in SELF_SKILL_SPECS
]
SELF_RUNNER_SPECS = [
    (name.replace("ghc-family-", "ghc_family_").replace("-", "_") + ".py", purpose)
    for name, purpose in SELF_SKILL_SPECS
]
SUCCESSOR_RUNNER_SEEDS = [
    {"name": name.replace("floristry", "successor_domain"), "recipient": "Liora Venn", "state": "recommendation_only", "completion_credit": 0}
    for name, _ in SELF_RUNNER_SPECS
]

SELF_CLEAN_CATEGORIES = [
    "retain every inherited and current negative without folding it into a pass",
    "refresh count mirrors only from authoritative ledgers",
    "preserve Git-blob and logical-text hash-domain declarations",
    "pin UTF-8 before Unicode-emitting diagnostics",
    "split Windows probes into bounded scalar receipts",
    "keep expected-empty branch and remote checks null-safe",
    "preserve family-current callers and historical compatibility surfaces",
    "reject stale owner and phase labels in current-owner artifacts",
    "keep x1 immutable after its four-way-equality gate",
    "keep x2 implementation absent from x1",
    "keep exact and blocked packets visible and unexecuted",
    "keep real plant, order, participant, and connector rows empty",
    "retain scanner candidates separately from confirmed payload hits",
    "scan only declared public owner surfaces across five classes",
    "refresh owner manifests after every additive lifecycle change",
    "verify deterministic JSON ordering and parsing",
    "verify proposal append-only arithmetic",
    "verify inherited revalidation receives zero novelty and completion credit",
    "verify outcome labels use only the four authorized states",
    "reserve manual and affected-user accessibility evaluation",
    "reserve legal, cultural, biosecurity, plant-health, and Māori authority",
    "reserve empirical GMUT and professional THOS claims",
    "reserve production Freed ID keys, proofs, status, recovery, and trust governance",
    "reserve privacy-complete and exhaustive-security claims",
    "keep every document under the declared word ceiling",
    "keep owner additions under the declared file ceiling",
    "verify source-to-final single-parent zero-merge ancestry",
    "hold terminal routing until exact final proof",
    "send no precontact or duplicate activation",
    "preserve NOT_READY_FOR_STAGE_20",
]
SELF_CLEAN_TASKS = [
    {"task_id": f"V6613-CLEAN-{i:03d}", "title": title, "owner": OWNER, "mode": "additive_review_only"}
    for i, title in enumerate(SELF_CLEAN_CATEGORIES, 1)
]
SUCCESSOR_CLEAN_SEEDS = [
    {"task_id": f"V6614-REC-CLEAN-{i:03d}", "title": title, "recipient": "Liora Venn", "completion_credit": 0}
    for i, title in enumerate(SELF_CLEAN_CATEGORIES, 1)
]

OFFICIAL_SOURCES = [
    ("MPI-CUTFLOWER-IHS", "official_new_zealand_regulator", "https://www.mpi.govt.nz/dmsdocument/1150/direct", "Current 2025 fresh cut flowers and foliage import-health vocabulary only; no import, inspection, treatment, release, biosecurity, legal, or professional determination."),
    ("USDA-APHIS-CUTFLOWERS", "official_us_regulator", "https://www.aphis.usda.gov/trade-management-manuals", "Current APHIS commodity and cut-flower import-requirement vocabulary only; no shipment, inspection, treatment, permit, or compliance conclusion."),
    ("GBIF-OCCURRENCE", "primary_biodiversity_infrastructure", "https://techdocs.gbif.org/en/openapi/v1/occurrence", "Current occurrence API field, pagination, issue, location and citation vocabulary only; zero network calls, rows, downloads, accounts, or commercial-lot inferences."),
    ("W3C-PROV", "official_w3c", "https://www.w3.org/TR/prov-o/", "Entity, activity, agent-placeholder, generation, derivation, revision, invalidation, and qualified-provenance vocabulary only."),
    ("W3C-VC2", "official_w3c", "https://www.w3.org/TR/vc-data-model-2.0/", "Current credential subject, issuer, evidence, validity, status and privacy vocabulary only; zero keys, proofs, issuances, presentations, or production identities."),
    ("W3C-VC-DI", "official_w3c", "https://www.w3.org/TR/vc-data-integrity/", "Data-integrity context, verification-method and proof-structure vocabulary only; zero keys, signatures, cryptographic verification, or truth-of-claim conclusion."),
    ("WCAG22", "official_w3c", "https://www.w3.org/TR/WCAG22/", "Accessible structure, text alternative, noncolour, navigation, status, and interaction vocabulary with manual, assistive-technology, Māori-language, and affected-user evaluation reserved."),
    ("MSL-SI", "official_new_zealand_metrology_institute", "https://www.measurement.govt.nz/metrology/si-units", "Current SI unit and quantity vocabulary only; no measurement, calibration, uncertainty result, plant-quality inference, or physical confirmation."),
    ("NZ-PRIVACY", "official_nz_privacy_commissioner", "https://www.privacy.org.nz/privacy-principles/", "Current New Zealand privacy-principle vocabulary including IPP 3A from May 2026 only; no legal, compliance, collection, disclosure, or remedy conclusion."),
    ("TE-MANA-RARAUNGA", "primary_maori_data_sovereignty_network", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Māori data-sovereignty and governance reservation vocabulary only; no Māori authority, ratification, wording, naming, tikanga, mātauranga, taonga-status, or cultural decision."),
    ("JSON-SCHEMA-2020-12", "primary_json_schema_project", "https://json-schema.org/draft/2020-12", "Schema, vocabulary, tuple, applicator, validation, annotation, and fail-closed structural vocabulary only."),
    ("IETF-JCS", "official_rfc_editor", "https://www.rfc-editor.org/rfc/rfc8785", "Canonical JSON digest vocabulary without key, signature, proof, credential, identity, or production claims."),
    ("GIT-LOG", "official_git_docs", "https://git-scm.com/docs/git-log", "Deterministic tracked-history selection and ancestry vocabulary."),
    ("PYTHON-JSON", "official_python_docs", "https://docs.python.org/3/library/json.html", "Deterministic UTF-8 JSON parse and serialization vocabulary."),
]
SOURCE_STATUS = {
    "MPI-CUTFLOWER-IHS": "current_2025_standard_checked_2026_08_05",
    "USDA-APHIS-CUTFLOWERS": "current_page_last_modified_2026_07_02_checked_2026_08_05",
    "GBIF-OCCURRENCE": "current_live_openapi_checked_2026_08_05",
    "W3C-PROV": "stable_recommendation",
    "W3C-VC2": "recommendation_2025_checked_2026_08_05",
    "W3C-VC-DI": "recommendation_checked_2026_08_05",
    "WCAG22": "recommendation_2024",
    "MSL-SI": "current_checked_2026_08_05",
    "NZ-PRIVACY": "current_including_ipp3a_from_2026_05_01",
    "TE-MANA-RARAUNGA": "primary_principles_current",
    "JSON-SCHEMA-2020-12": "current_2020_12",
    "IETF-JCS": "stable_informational_rfc",
    "GIT-LOG": "current",
    "PYTHON-JSON": "current",
}


def _startup_failure(negative_id: str, signature: str, recovery: str) -> dict[str, object]:
    return {
        "negative_id": negative_id,
        "signature": signature,
        "recovery": recovery,
        "recovery_passed": True,
        "completion_credit": 0,
    }


STARTUP_FAILURES = [
    _startup_failure("V6613-X1-N001", "broad-memory-registry-search-produced-oversized-truncated-output", "Retain the truncated search and use bounded exact memory registry terms; no live route fact was inferred from memory."),
    _startup_failure("V6613-X1-N002", "login-profile-worktree-list-returned-no-attributable-output", "Retain the empty wrapper and use exact no-profile scalar Git probes."),
    _startup_failure("V6613-X1-N003", "full-worktree-porcelain-list-was-slow-and-oversized", "Retain the broad probe and resolve only the exact source and owner worktree entries."),
    _startup_failure("V6613-X1-N004", "powershell-path-getrelativepath-api-was-unavailable", "Retain the unavailable API assumption and use verified root-prefix subtraction only after absolute containment checks."),
    _startup_failure("V6613-X1-N005", "broad-validation-receipt-bank-listing-exceeded-the-output-budget", "Retain the broad listing and resolve the exact receipt named by the baton."),
    _startup_failure("V6613-X1-N006", "first-complete-baton-display-truncated-before-eof", "Retain the partial display and reread the committed baton in bounded numbered windows through line 1074."),
    _startup_failure("V6613-X1-N007", "parallel-ripgrep-hit-a-minified-proposal-index-and-obscured-scalar-results", "Retain the oversized projection and parse the exact JSON object before bounded filtering."),
    _startup_failure("V6613-X1-N008", "combined-native-parent-summary-returned-empty-powershell-output", "Retain the empty wrapper and recover with sequential native parent and ancestry probes."),
    _startup_failure("V6613-X1-N009", "thread-list-query-argument-was-not-supported-by-the-live-tool", "Retain the rejected read-only query and use the bounded default registry page without sending."),
    _startup_failure("V6613-X1-N010", "first-bounded-thread-list-projection-truncated", "Retain the truncated registry display and use bounded local exact-title filtering only at the terminal gate."),
    _startup_failure("V6613-X1-N011", "per-blob-git-show-manifest-replay-exceeded-supervision", "Retain the timed-out replay and validate current-tree parity with exact manifest entries plus the authoritative immutable receipt."),
    _startup_failure("V6613-X1-N012", "inline-python-source-manifest-probes-lost-literal-quotes", "Retain the syntax failures and use quote-simple PowerShell and structured JSON probes."),
    _startup_failure("V6613-X1-N013", "cat-file-batch-pipeline-blocked-before-attributable-output", "Retain the blocked transport, terminate only its exact helpers, and avoid write-before-read batch assumptions."),
    _startup_failure("V6613-X1-N014", "git-archive-manifest-replay-left-a-zero-byte-temporary-archive", "Retain the failed archive attempt, stop exact helpers, verify zero bytes, and remove only the owner-named temporary file."),
    _startup_failure("V6613-X1-N015", "parallel-scalar-git-probes-intermittently-returned-empty-payloads", "Retain the empty wrappers and recover with sequential attributable Git commands."),
    _startup_failure("V6613-X1-N016", "initial-worktree-add-full-checkout-progress-was-unbounded-for-the-owner-lane", "Retain the partial checkout and recover only inside the Orin worktree with a verified source-identical index and bounded materialization."),
    _startup_failure("V6613-X1-N017", "second-worktree-attach-correctly-refused-the-already-registered-path", "Retain the refused duplicate attach and reuse only the single registered Orin worktree."),
    _startup_failure("V6613-X1-N018", "transient-status-showed-staged-deletions-while-the-original-checkout-held-the-index", "Retain the transient witness and award no clean-state credit until all exact Git helpers stopped and both diffs were rechecked."),
    _startup_failure("V6613-X1-N019", "worktree-add-internal-reset-helper-conflicted-with-the-no-reset-phase-boundary", "Retain the helper incident, stop only that exact process, and make no sibling or source change."),
    _startup_failure("V6613-X1-N020", "sparse-read-tree-recovery-exceeded-bounded-supervision", "Retain the timed-out sparse operation and use the clean same-head source index plus exact byte-copy materialization."),
    _startup_failure("V6613-X1-N021", "partial-sparse-patterns-did-not-materialize-required-script-and-test-surfaces", "Retain the incomplete sparse result and byte-copy inherited scripts and tests from the clean read-only same-head source."),
    _startup_failure("V6613-X1-N022", "copied-source-files-produced-stat-only-modified-markers", "Retain the stat-only observation, prove both logical diffs empty, then refresh the index without changing any blob identity."),
    _startup_failure("V6613-X1-N023", "powershell-empty-pipe-and-inline-hashtable-conditional-assumptions-were-rejected", "Retain both parser assumptions and materialize arrays and scalar values before projection."),
    _startup_failure("V6613-X1-N024", "first-zero-byte-temp-removal-was-blocked-while-exact-helper-state-was-unsettled", "Retain the refusal, verify no live exact helper and zero-byte size, then remove only that literal owner temp path."),
    _startup_failure("V6613-X1-N025", "first-structured-novelty-result-projection-used-an-empty-foreach-pipe", "Retain the parser rejection and materialize the novelty result array before JSON conversion."),
    _startup_failure("V6613-X1-N026", "first-novelty-title-stream-hit-the-default-cp1252-encoder-before-producing-valid-json", "Retain the failed stream and pin UTF-8 or emit ASCII-escaped JSON before the bounded novelty probe."),
    _startup_failure("V6613-X1-N027", "first-complete-twenty-title-novelty-screen-passed-nineteen-and-rejected-one-inherited-comparison-template-neighbour", "Retain the nineteen-of-twenty witness and replace only the comparison title and mechanism with a domain-specific vacancy-matrix design before rerunning the bounded screen."),
    _startup_failure("V6613-X1-N028", "first-x1-build-used-the-crlf-worktree-activation-hash-where-source-verification-required-the-immutable-git-blob-domain", "Retain the refused build at zero credit and bind the source packet digest and byte count to the exact immutable Git blob."),
    _startup_failure("V6613-X1-N029", "first-x1-test-aggregate-ran-before-family-index-and-governance-tooling-receipts-existed", "Retain the twenty-one-pass two-error aggregate at zero credit and build only the preregistered missing family-current receipts before testing again."),
    _startup_failure("V6613-X1-N030", "second-x1-test-aggregate-repeated-the-same-two-missing-tooling-receipt-errors-during-state-inspection", "Retain the repeated twenty-one-pass two-error aggregate at zero credit, stop aggregate retries, and complete the known receipt prerequisite set first."),
    _startup_failure("V6613-X1-N031", "combined-workflow-refinement-console-projection-exceeded-the-model-output-budget", "Retain the truncated projection, do not replay either workflow run, and validate the already-written rejecting and passing receipts through exact literal-path reads."),
]

# X2 failures are appended only after the immutable x1 commit is pushed and
# proved clean and four-way equal.
PREFILLED_X1_X2_FAILURES_IGNORED: tuple[dict[str, object], ...] = tuple()
X2_FAILURES: list[dict[str, object]] = []
