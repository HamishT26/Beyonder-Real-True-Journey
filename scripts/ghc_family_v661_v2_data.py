#!/usr/bin/env python3
"""Frozen x1 planning data for Caelen Ash v661-v2.

Sable Rook's immutable v661-v1 surface supplies compatibility vocabulary only.
Twenty inherited rows are selected for bounded revalidation with zero Caelen
novelty or completion credit. Only the twenty new rows below extend the
append-only proposal chain. All real layouts, rolling stock, electrical work,
operations, participants, professional, empirical, production, legal, cultural,
accessibility-complete, privacy-complete, and Māori-authority lanes remain empty
or exact-gated.
"""

from __future__ import annotations

from ghc_family_v661_v1_data import *  # noqa: F401,F403


PHASE = "v661-v2"
CANONICAL_PHASE = PHASE
PHASE_CODE = "V6612"
OWNER = "Caelen Ash"
PRONOUNS = "they/them"
ROLE = "relational provenance-and-remedy cartographer"
HOPE = (
    "make every handoff traceable, every authority boundary visible, and every "
    "correction recoverable without mistaking simulation for service"
)
BRANCH = "codex/GHC-Family/caelen-ash-v661-v2-full-tools"
PHASE_ROOT = "docs/caelen-ash/v661-v2"

SOURCE_OWNER = "Sable Rook"
SOURCE_BRANCH = "codex/GHC-Family/sable-rook-v661-v1-full-tools"
SOURCE_BASE = "acd00fcc14fe7526ae95338dcec5fa0beee31610"
SOURCE_X1 = "5a94096fb5e4a9243b16088e3488ddac355c6d94"
SOURCE_EVIDENCE = "e1ee91023a0fa14e50a15f4674908e0d2f65961d"
SOURCE_CLOSEOUT = SOURCE_EVIDENCE
SOURCE_FINAL = "0cac4abe8131df05d30e0f744d05bc392d22e73d"
SOURCE_CLOSEOUT_BASE = SOURCE_FINAL
SOURCE_CANONICAL_RECEIPT_SHA256 = (
    "3d0c837b2dcbab2bb211631f42e5090c50184734b62570a6971682ec016a0943"
)
SOURCE_LIVE_ACTIVATION_STATE = "SENT_ONCE_ACKNOWLEDGED"
ACTIVATION_PACKET_SHA256 = (
    "a0e13d13b7ee6b0e4479515355bd1493bca5394f2cde59d3ad9fce9bb9a4390a"
)
X1_FREEZE = "pending_until_x2"

PRIOR_FROZEN = 3310
SOURCE_SEALED_NEGATIVES = 20993
SOURCE_EXTERNAL_NEGATIVES = 3
ACTIVATION_NEGATIVES = SOURCE_SEALED_NEGATIVES + SOURCE_EXTERNAL_NEGATIVES
ACTIVATION_MESSAGE_NEGATIVE_BASELINE = 20996
SOURCE_OPEN_GAPS = 138
SOURCE_EXACT_GATES = 137
SOURCE_SEALED_METHODS = 6547
SOURCE_EXTERNAL_METHODS = 3
ACTIVATION_METHODS = SOURCE_SEALED_METHODS + SOURCE_EXTERNAL_METHODS
ACTIVATION_MESSAGE_METHOD_BASELINE = 6550
SELECTED_INHERITED_COUNT = 20
NEW_UNIQUE_COUNT = 20
CURRENT_PORTFOLIO_COUNT = SELECTED_INHERITED_COUNT + NEW_UNIQUE_COUNT
LATEST_TRACKED_SCAN_CAP = 5000

PRIMARY_PILLAR = "THOS Body"
PRACTICE_LENS = (
    "bounded synthetic model-railway layout, rolling-stock, track topology, "
    "extra-low-voltage control-state documentation, fault isolation, correction, "
    "accessibility, provenance, workload, and session-handover lens"
)

EXPECTED_DISTRIBUTION = {
    "completed": 14,
    "represented": 4,
    "open_gap": 1,
    "exact_gate": 1,
}
ALLOWED_OUTCOMES = set(EXPECTED_DISTRIBUTION)

PROTECTED_GATES = [
    "real_model_railway_layouts_modules_track_turnouts_signals_rolling_stock_power_supplies_command_stations_decoders_wiring_buildings_or_venues",
    "real_owners_operators_club_members_visitors_children_workers_maintainers_electrical_workers_manufacturers_affected_parties_and_authorities",
    "real_wiring_programming_testing_repair_energisation_operation_switching_dispatch_public_display_transport_sale_or_return_to_service_action",
    "professional_electrical_engineering_model_railway_conformance_accessibility_public_safety_maintenance_or_operational_authority",
    "empirical_gmut_prediction_likelihood_parameter_constraint_observational_confirmation_physical_discovery_or_final_physics",
    "blind_matched_budget_thos_real_arms_governed_participants_operators_safety_monitoring_statistics_and_independent_review",
    "production_identity_live_keys_signatures_proofs_issuance_resolution_status_revocation_interoperability_recovery_and_trust",
    "asset_identity_ownership_location_images_layout_design_manufacturer_claims_private_roster_data_traditional_knowledge_collective_interest_and_remedy",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "legal_cultural_electrical_safety_product_conformance_ownership_custody_public_access_data_governance_and_maori_authority",
    "affected_party_notice_consent_contestation_correction_restriction_access_return_remedy_collective_governance_and_acceptance",
    "independent_team_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]

SELECTED_INHERITED_IDS = [f"V6611-P{i:03d}" for i in range(1, 21)]


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
        "model-railway-layout-identity",
        "Surrogate model-railway layout identity capsule with scale, gauge, module set, revision, source pin, ownership hold, and operation refusal",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic layout and revision tokens, declared scale and gauge, module-set identity, source pin, ownership uncertainty, correction, tombstone, and zero-real-layout states",
        ["NMRA-STANDARDS", "MOROP-NEM", "W3C-PROV", "JSON-SCHEMA-2020-12"],
    ),
    _proposal(
        "model-railway-track-topology",
        "Model-railway module, track section, turnout, crossing, buffer stop, boundary connector, and adjacency topology with orphan, loop, gauge-conflict, and construction refusal",
        "completed",
        "THOS Body and GMUT Mind",
        "typed synthetic modules, track sections, turnouts, crossings, buffer stops and boundary connectors with adjacency, direction, orphan, loop, gauge-conflict, contradiction, and no-construction guards",
        ["NMRA-STANDARDS", "MOROP-NEM", "JSON-SCHEMA-2020-12"],
    ),
    _proposal(
        "model-railway-rolling-stock-register",
        "Model-railway rolling-stock, wheelset, coupler, loading-gauge, scale, provenance, compatibility, condition-placeholder, and fitness-refusal register",
        "completed",
        "THOS Body and Freed ID",
        "synthetic rolling-stock tokens, wheelset and coupler classes, loading-gauge and scale declarations, provenance, compatibility unknowns, condition placeholders, quarantine, and fitness refusal",
        ["NMRA-STANDARDS", "MOROP-NEM", "W3C-PROV"],
    ),
    _proposal(
        "model-railway-power-district-map",
        "De-energised model-railway power-district, feeder, return, isolating-gap, source, polarity, capacity-unknown, conflict, and connection-refusal map",
        "completed",
        "THOS Body",
        "synthetic power districts, feeders, returns, isolating gaps, source and polarity placeholders, capacity unknowns, conflicting assignments, de-energised defaults, and connection refusal",
        ["NMRA-STANDARDS", "NMRA-DCC", "WORKSAFE-ELV", "JSON-SCHEMA-2020-12"],
    ),
    _proposal(
        "model-railway-dcc-provenance",
        "Model-railway DCC command-station, decoder-address, configuration-variable placeholder, firmware, manufacturer-claim, collision, supersession, and programming-hold ledger",
        "completed",
        "THOS Body and Freed ID",
        "synthetic command-station and decoder tokens, address and configuration-variable placeholders, firmware and manufacturer claims, collision detection, correction, supersession, and zero-device programming",
        ["NMRA-DCC", "NMRA-STANDARDS", "W3C-PROV", "IETF-JCS"],
    ),
    _proposal(
        "model-railway-turnout-route-dependency",
        "Model-railway turnout, route, conflicting path, detection-unknown, lock-placeholder, cancellation, release-hold, and no-signalling-safety dependency board",
        "completed",
        "THOS Body",
        "synthetic turnout and route tokens, conflicting-path edges, detection unknowns, lock and release placeholders, cancellation, contradiction, manual hold, and no signalling-safety claim",
        ["NMRA-LCC", "MOROP-NEM", "W3C-PROV"],
    ),
    _proposal(
        "model-railway-session-cue-ledger",
        "Model-railway session timetable, train alias, route cue, prerequisite, dwell-placeholder, cancellation, manual readback, workload, and no-dispatch ledger",
        "completed",
        "THOS Body",
        "synthetic train aliases, route and cue dependencies, timetable and dwell placeholders, cancellations, correction readback, workload ceilings, stop tokens, and zero dispatch or movement authority",
        ["NMRA-OPERATIONS", "WCAG22", "W3C-PROV"],
    ),
    _proposal(
        "model-railway-fault-isolation",
        "Model-railway short-circuit cue, overload, thermal cue, derailment-placeholder, unknown fault, stop token, isolation, referral, and no-clearance board",
        "completed",
        "THOS Body and CBR Heart",
        "synthetic fault cues, unknown electrical and mechanical states, de-energised stop tokens, isolation placeholders, referral, correction, and zero testing, repair, energisation, or clearance claims",
        ["WORKSAFE-ELV", "NMRA-STANDARDS", "W3C-PROV"],
    ),
    _proposal(
        "model-railway-correction-lineage",
        "Model-railway layout, asset, address, route, condition, fault, correction, supersession, cancellation, readback, and unresolved-ambiguity lineage",
        "completed",
        "THOS Body and Freed ID",
        "synthetic layout and asset assertions, address and route claims, condition and fault placeholders, correction, supersession, cancellation, readback, ambiguity hold, and non-erasure",
        ["W3C-PROV", "IETF-JCS", "JSON-SCHEMA-2020-12"],
    ),
    _proposal(
        "model-railway-provenance-custody",
        "Synthetic model-railway layout, module, rolling-stock, controller, image, custody, transfer, disclosure, correction, privacy, and ownership-refusal covenant",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic asset and custody placeholders, transfer and component association, documentary source, image and location disclosure masks, consent and rights holds, correction, and ownership refusal",
        ["W3C-PROV", "NZ-PRIVACY", "IETF-JCS"],
    ),
    _proposal(
        "model-railway-access-companion",
        "Accessible model-railway layout and session companion with topology table, noncolour state, text alternatives, focus order, plain-language holds, and reserved affected-user evaluation",
        "completed",
        "THOS Body and CBR Heart",
        "structural headings, topology and session tables, text alternatives, noncolour state, focus order, status messages, downloadable plain text, language reservations, and zero affected-user sessions",
        ["WCAG22", "W3C-PROV", "NZ-PRIVACY"],
    ),
    _proposal(
        "gmut-model-railway-network-obligations",
        "GMUT port-Hamiltonian surrogate for a model-railway graph with state vector, incidence matrix, effort-flow ports, dissipation, unit ledger, uncertainty, identifiability, and observation firewall",
        "completed",
        "GMUT Mind",
        "typed symbolic track and electrical nodes, incidence matrix, effort-flow port placeholders, energy-storage and dissipation terms, unit and uncertainty ledgers, identifiability limits, counterexample slots, and zero physical observations",
        ["BIPM-SI", "W3C-PROV", "IETF-JCS"],
    ),
    _proposal(
        "model-railway-action-authorization-firewall",
        "Model-railway wiring, programming, testing, repair, energisation, operation, switching, dispatch, public display, transport, sale, and return-to-service authorization firewall",
        "completed",
        "CBR Heart and THOS Body",
        "synthetic action request, asset and fault scope, owner, operator, maintainer, electrical-worker, legal, cultural, affected-party and Māori-authority holds, stop token, and execution refusal",
        ["WORKSAFE-ELV", "NMRA-STANDARDS", "NZ-PRIVACY", "TE-MANA-RARAUNGA"],
    ),
    _proposal(
        "stage20-model-railway-evidence-board",
        "Terminal evidence antichain for synthetic model-railway claims listing unfilled real-device, participant, authority, infrastructure, empirical, reproduction, and Stage 20 prerequisites",
        "completed",
        "All pillars",
        "typed synthetic evidence antichain, unfilled device, participant, authority, infrastructure, empirical and independent-team prerequisites, non-substitution rules, retained negatives, and fail-closed terminal abstention",
        ["W3C-PROV", "IETF-JCS", "JSON-SCHEMA-2020-12"],
    ),
    _proposal(
        "gmut-model-railway-traction-network-proxy",
        "GMUT model-railway traction, wheel-rail, motor, load, electrical-network, damping, boundary, covariance, stability, and identifiability proxy with zero device observations",
        "represented",
        "GMUT Mind",
        "typed symbolic motor, wheel-rail, load and electrical-network placeholders, damping, boundaries, covariance, zero fitted coefficients, zero likelihood rows, and physical-inference abstention",
        ["BIPM-SI", "NMRA-STANDARDS", "W3C-PROV"],
    ),
    _proposal(
        "thos-model-railway-handover",
        "THOS reciprocal model-railway shift brief with isolated-fault queue, unresolved route budget, stop token, two-party-readback placeholder, workload ceiling, and zero operators",
        "represented",
        "THOS Body",
        "synthetic shift brief, isolated-fault and ambiguity queues, route budget, workload ceiling, stop token, correction, two-party-readback placeholder, escalation, and zero real operators or maintainers",
        ["NMRA-OPERATIONS", "WCAG22", "W3C-PROV"],
    ),
    _proposal(
        "model-railway-matched-budget-protocol",
        "Empty synthetic comparison protocol for graph-guided versus cue-card-guided model-railway record interpretation with equal budgets and no participants",
        "represented",
        "THOS Body",
        "future blind matched-budget synthetic records, shuffled tasks, graph-guided and cue-card-guided arms, equal action budgets, masked scoring, safety and withdrawal rules, zero participants, and no comprehension or effectiveness claim",
        ["WCAG22", "NMRA-OPERATIONS", "W3C-PROV"],
    ),
    _proposal(
        "freed-id-model-railway-asset-profile",
        "Freed ID synthetic model-railway layout, module, rolling-stock, decoder, document, image, namespace, collision, correction, status-hold, and nonproduction relation profile",
        "represented",
        "Freed ID and CBR Heart",
        "synthetic asset and relation identifiers, namespace and version placeholders, collisions, correction, supersession, status and revocation holds, privacy mask, zero keys or proofs, and nonproduction refusal",
        ["W3C-PROV", "IETF-JCS", "NZ-PRIVACY"],
    ),
    _proposal(
        "nmra-conformance-zero-device-adapter",
        "NMRA standards and conformance evidence adapter with document version, product claim, inspection placeholder, test procedure, result digest, appeal path, and zero-device refusal",
        "open_gap",
        "THOS Body and Freed ID",
        "zero devices, inspections, electrical measurements, manufacturer submissions, warrants, conformance results, live registrations, keys, signatures, external calls, or professional conclusions",
        ["NMRA-STANDARDS", "NMRA-CONFORMANCE", "NMRA-DCC", "IETF-JCS"],
    ),
    _proposal(
        "model-railway-rights-authority",
        "Unoccupied authority circuit for layout ownership, electrical work, operation, public access, child safety, images, place and rail narratives, cultural knowledge, remedy, and Māori decision non-substitution",
        "exact_gate",
        "CBR Heart",
        "unoccupied owner, operator, maintainer, electrical-worker, venue, manufacturer, visitor, parent or guardian, accessibility, legal, cultural, privacy, traditional-knowledge, collective-interest, tangata whenua, iwi, hapū, affected-party, remedy, and Māori-authority reservations",
        ["WORKSAFE-ELV", "NZ-PRIVACY", "TE-MANA-RARAUNGA", "WCAG22"],
    ),
]

SELF_SAFE_CATEGORIES = [
    "Sable source head and fresh equality",
    "activation packet and external receipt digests",
    "three-thousand-three-hundred-ten-row proposal-chain parse",
    "twenty inherited selection identities",
    "twenty-title novelty screen",
    "mechanism-level model-railway-neighbor review",
    "new-outcome distribution",
    "workflow-plan policy",
    "identity and relational-language boundary",
    "Hamish-authorized Sable-to-Caelen live edge",
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
    {"task_id": f"V6612-SAFE-{i:03d}", "title": f"Validate {name} inside the Caelen-owned v661-v2 lane", "owner": OWNER}
    for i, name in enumerate(SELF_SAFE_CATEGORIES, 1)
]
SUCCESSOR_SAFE_SEEDS = [
    {"task_id": f"V6613-REC-SAFE-{i:03d}", "title": f"Reassess {name} for Orin-only v661-v3", "recipient": "Orin Thale", "completion_credit": 0}
    for i, name in enumerate(SELF_SAFE_CATEGORIES[:20], 1)
]

SELF_CANDIDATE_CATEGORIES = [
    "synthetic model-railway layout identity ledger",
    "module, track, turnout, and boundary topology tribunal",
    "rolling-stock provenance and compatibility register",
    "de-energised power-district and feeder map",
    "DCC address, configuration, and collision provenance ledger",
    "turnout, route, conflict, cancellation, and release-hold board",
    "session cue, readback, workload, and no-dispatch ledger",
    "fault-isolation and no-clearance board",
    "GMUT network-obligation and observation-firewall board",
    "model-railway rights, electrical-work, public-access, remedy, and Māori-authority circuit",
]
SELF_CANDIDATE_TASKS = [
    {"task_id": f"V6612-CAND-{i:03d}", "title": f"Build and test reversible {name}", "owner": OWNER}
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]
SUCCESSOR_CANDIDATE_SEEDS = [
    {"task_id": f"V6613-REC-CAND-{i:03d}", "title": f"Consider a distinct Orin-owned refinement of {name}", "recipient": "Orin Thale", "completion_credit": 0}
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]

EXACT_QUEUE = [
    {"task_id": f"V6612-EXACT-{i:03d}", "title": title, "state": "exact_gate_unexecuted"}
    for i, title in enumerate(
        [
            "Wire, program, test, repair, energise, operate, switch, dispatch, exhibit, transport, sell, or return to service any real model-railway layout, module, vehicle, controller, decoder, power supply, or accessory",
            "Make a real electrical-safety, mechanical-fitness, track, wheel, coupler, control, fault, conformance, public-safety, or return-to-service determination",
            "Use real owners, operators, club members, visitors, children, workers, maintainers, electrical workers, manufacturers, venues, devices, layouts, or personal information",
            "Disclose private identity, location, image, layout design, asset roster, ownership dispute, access detail, traditional knowledge, or restricted venue information",
            "Make a professional electrical, engineering, model-railway, conformance, public-safety, privacy, security, translation, or accessibility determination",
            "Publish a production asset identifier, decoder roster, conformance record, credential, signature, proof, status, interoperability result, or operational record",
            "Allocate ownership, custody, authorship, attribution, access, operation, child-safety, public-display, return, remedy, or beneficiary authority",
            "Make a tikanga, mātauranga, wording, naming, tangata whenua, iwi, hapū, Māori data-governance, cultural-protocol, taonga-status, or Māori-authority decision",
            "Run a real participant study, operating session, electrical or mechanical trial, professional review, public access trial, or independent reproduction",
            "Perform destructive cleanup or any mutation outside the exact Caelen-owned lane",
        ],
        1,
    )
]
BLOCKED_QUEUE = [
    {"task_id": f"V6612-BLOCK-{i:03d}", "title": title, "state": "blocked_unexecuted"}
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
    ("ghc-family-model-railway-layout-identity", "Validate bounded synthetic layout identity, scale, gauge, module set, source pin, revision, ownership hold, and operation refusal."),
    ("ghc-family-model-railway-track-topology", "Check synthetic modules, track, turnouts, crossings, connectors, adjacency, orphans, loops, gauge conflicts, and construction refusal."),
    ("ghc-family-model-railway-rolling-stock", "Preserve synthetic rolling-stock, wheelset, coupler, scale, provenance, compatibility, quarantine, and fitness-refusal states."),
    ("ghc-family-model-railway-power-district", "Preserve de-energised synthetic districts, feeders, returns, gaps, polarity, capacity unknowns, conflicts, and connection refusal."),
    ("ghc-family-model-railway-dcc-provenance", "Retain synthetic command-station, decoder, address, configuration, firmware, collision, correction, and zero-programming states."),
    ("ghc-family-model-railway-route-dependency", "Expose synthetic turnout, route, conflict, detection unknown, lock, cancellation, release hold, and no-safety-claim relations."),
    ("ghc-family-model-railway-fault-isolation", "Preserve short-circuit, overload, thermal, derailment, unknown-fault, stop, isolation, referral, and no-clearance states."),
    ("ghc-family-model-railway-correction-lineage", "Preserve layout, asset, address, route, fault, correction, supersession, cancellation, readback, ambiguity, and non-erasure."),
    ("ghc-family-gmut-model-railway-network", "Preserve typed network, boundary, unit, covariance, conservation, stability, identifiability, and observation-firewall obligations."),
    ("ghc-family-model-railway-rights-authority", "Keep ownership, electrical work, operation, public access, images, remedy, cultural, and Māori decision rights unoccupied."),
]
SUCCESSOR_SKILL_SEEDS = [
    {"name": name.replace("model-railway", "successor-domain"), "recipient": "Orin Thale", "state": "recommendation_only", "completion_credit": 0}
    for name, _ in SELF_SKILL_SPECS
]
SELF_RUNNER_SPECS = [
    (name.replace("ghc-family-", "ghc_family_").replace("-", "_") + ".py", purpose)
    for name, purpose in SELF_SKILL_SPECS
]
SUCCESSOR_RUNNER_SEEDS = [
    {"name": name.replace("model-railway", "successor_domain"), "recipient": "Orin Thale", "state": "recommendation_only", "completion_credit": 0}
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
    "keep real layout, device, participant, and connector rows empty",
    "retain scanner candidates separately from confirmed payload hits",
    "scan only declared public owner surfaces across five classes",
    "refresh owner manifests after every additive lifecycle change",
    "verify deterministic JSON ordering and parsing",
    "verify proposal append-only arithmetic",
    "verify inherited revalidation receives zero novelty and completion credit",
    "verify outcome labels use only the four authorized states",
    "reserve manual and affected-user accessibility evaluation",
    "reserve legal, cultural, electrical, public-safety, and Māori authority",
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
    {"task_id": f"V6612-CLEAN-{i:03d}", "title": title, "owner": OWNER, "mode": "additive_review_only"}
    for i, title in enumerate(SELF_CLEAN_CATEGORIES, 1)
]
SUCCESSOR_CLEAN_SEEDS = [
    {"task_id": f"V6613-REC-CLEAN-{i:03d}", "title": title, "recipient": "Orin Thale", "completion_credit": 0}
    for i, title in enumerate(SELF_CLEAN_CATEGORIES, 1)
]

OFFICIAL_SOURCES = [
    ("NMRA-STANDARDS", "primary_model_railway_standards_body", "https://www.nmra.org/index-nmra-standards-and-recommended-practices", "Current NMRA scale, gauge, trackwork, wheel, coupler, electrical, DCC, LCC, interchange and document-version vocabulary only; no product, layout, safety, legal, or conformance determination."),
    ("NMRA-DCC", "primary_model_railway_standards_body", "https://www.nmra.org/digital-command-control-dcc", "Current NMRA DCC command, address, packet, decoder and interoperability context only; no device programming, testing, operation, compatibility, or conformance claim."),
    ("NMRA-LCC", "primary_model_railway_standards_body", "https://www.nmra.org/categories/standards-and-conformance", "Current NMRA Layout Command Control and standards-category vocabulary only; no live route control, signalling, device, or safety authority."),
    ("NMRA-CONFORMANCE", "primary_model_railway_standards_body", "https://www.nmra.org/conformance-and-inspection-main-page", "Current NMRA inspection, non-conformance, test-procedure, manufacturer-ID, warrant and appeal-context vocabulary only; zero devices, submissions, inspections, warrants, or conformance claims."),
    ("NMRA-OPERATIONS", "primary_model_railway_association", "https://www.nmra.org/introduction-layout-modules", "Current NMRA module interface and operating-context vocabulary only; no real layout assembly, operation, dispatch, public access, or safety conclusion."),
    ("MOROP-NEM", "primary_european_model_railway_standards_body", "https://morop.org/images/NEM_register/NEM_E/nem101_en_2025.pdf", "Current NEM scale, gauge, track, vehicle, electrical and compatibility vocabulary only; no device, layout, conformance, or professional claim."),
    ("WORKSAFE-ELV", "official_new_zealand_regulator", "https://www.worksafe.govt.nz/topic-and-industry/electricity/installations-and-networks/low-voltage-electrical-installations/", "Current New Zealand low and extra-low-voltage safety, qualification, testing, certification and competent-worker boundary vocabulary only; no electrical work, connection, inspection, compliance, or legal conclusion."),
    ("W3C-PROV", "official_w3c", "https://www.w3.org/TR/prov-o/", "Entity, activity, agent-placeholder, generation, derivation, revision, invalidation, and qualified-provenance vocabulary only."),
    ("JSON-SCHEMA-2020-12", "primary_json_schema_project", "https://json-schema.org/draft/2020-12", "Schema, vocabulary, tuple, applicator, validation, annotation, and fail-closed structural vocabulary only."),
    ("IETF-JCS", "official_rfc_editor", "https://www.rfc-editor.org/rfc/rfc8785", "Canonical JSON digest vocabulary without key, signature, proof, credential, identity, or production claims."),
    ("WCAG22", "official_w3c", "https://www.w3.org/TR/WCAG22/", "Accessible structure, text alternative, noncolour, navigation, status, and interaction vocabulary with manual, assistive-technology, Māori-language, sensitive-content, and affected-user evaluation reserved."),
    ("BIPM-SI", "official_bipm", "https://www.bipm.org/en/publications/si-brochure", "SI length, mass, angle, temperature, quantity, unit, symbol, covariance, uncertainty-context, and reporting vocabulary only; no measurement or calibration result."),
    ("NZ-PRIVACY", "official_nz_privacy_commissioner", "https://www.privacy.org.nz/privacy-principles/", "Current New Zealand privacy-principle vocabulary only; no legal, compliance, collection, disclosure, locality, or remedy conclusion."),
    ("TE-MANA-RARAUNGA", "primary_maori_data_sovereignty_network", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Māori data-sovereignty and governance reservation vocabulary only; no Māori authority, ratification, wording, naming, tikanga, mātauranga, taonga-status, or repatriation claim."),
    ("GIT-LOG", "official_git_docs", "https://git-scm.com/docs/git-log", "Deterministic tracked-history selection and ancestry vocabulary."),
    ("PYTHON-JSON", "official_python_docs", "https://docs.python.org/3/library/json.html", "Deterministic UTF-8 JSON parse and serialization vocabulary."),
]
SOURCE_STATUS = {
    "NMRA-STANDARDS": "current_index_including_2026_updates_checked_2026_08_04",
    "NMRA-DCC": "current_primary_page_checked_2026_08_04",
    "NMRA-LCC": "current_standards_category_checked_2026_08_04",
    "NMRA-CONFORMANCE": "current_inspection_materials_checked_2026_08_04",
    "NMRA-OPERATIONS": "current_module_introduction_checked_2026_08_04",
    "MOROP-NEM": "current_nem_index_and_2025_documents_checked_2026_08_04",
    "WORKSAFE-ELV": "current_guidance_including_2025_regulatory_amendments_checked_2026_08_04",
    "W3C-PROV": "stable_recommendation",
    "JSON-SCHEMA-2020-12": "current_2020_12",
    "IETF-JCS": "stable_informational_rfc",
    "WCAG22": "recommendation_2024",
    "BIPM-SI": "ninth_edition_updated_2026",
    "NZ-PRIVACY": "current_including_ipp3a_from_2026_05_01",
    "TE-MANA-RARAUNGA": "primary_principles_current",
    "GIT-LOG": "current",
    "PYTHON-JSON": "current",
}


def _startup_failure(negative_id: str, signature: str, recovery: str) -> dict[str, object]:
    return {"negative_id": negative_id, "signature": signature, "recovery": recovery, "recovery_passed": True}


STARTUP_FAILURES = [
    _startup_failure("V6612-X1-N001", "combined-activation-and-skill-probe-produced-no-attributable-output-before-recovery", "Retain the empty wrapper at zero credit and split activation, skill, and source reads into exact bounded probes."),
    _startup_failure("V6612-X1-N002", "first-skill-inventory-foreach-pipeline-hit-powershell-empty-pipe-syntax-error", "Retain the parser rejection at zero credit and materialize the array before JSON projection."),
    _startup_failure("V6612-X1-N003", "combined-skill-display-truncated-before-all-required-skill-eofs", "Retain the partial display at zero credit and reread each selected skill and reference individually through EOF."),
    _startup_failure("V6612-X1-N004", "one-shot-authorization-state-display-truncated-before-eof", "Retain the truncated projection at zero credit and read the exact current-state file in deterministic numbered windows."),
    _startup_failure("V6612-X1-N005", "broad-d-drive-canonical-receipt-search-exceeded-the-bounded-time-window", "Retain the timed-out search at zero credit, stop only its verified read-only process, and use bounded top-level receipt discovery."),
    _startup_failure("V6612-X1-N006", "exec-session-cancel-attempt-used-an-unsupported-write-stdin-route", "Retain the unsupported cancellation attempt at zero credit and stop only the exact verified read-only search process by process identifier."),
    _startup_failure("V6612-X1-N007", "first-top-level-directory-projection-hit-powershell-empty-pipe-syntax-error", "Retain the parser rejection at zero credit and materialize the directory rows before projection."),
    _startup_failure("V6612-X1-N008", "combined-local-git-probe-hit-powershell-parenthesized-command-parse-errors", "Retain the parser rejection at zero credit and recover with scalar head, branch, divergence, and cleanliness probes."),
    _startup_failure("V6612-X1-N009", "first-x2-manifest-replay-compared-the-evidence-manifest-against-the-later-final-tree", "Retain the three expected lifecycle mismatches at zero credit and replay the x2 manifest at the immutable evidence commit, where all entries matched."),
    _startup_failure("V6612-X1-N010", "broad-worktree-proposal-index-search-exceeded-the-bounded-time-window", "Retain the timed-out search at zero credit, stop only its verified read-only process, and resolve the exact index path with Git tree metadata."),
    _startup_failure("V6612-X1-N011", "broad-domain-collision-projection-exceeded-the-output-budget", "Retain the truncated projection at zero credit and use structured JSON counts plus bounded samples for each candidate domain."),
    _startup_failure("V6612-X1-N012", "planetarium-lens-collided-with-seven-exact-frozen-proposals", "Retain the rejected lens at zero credit and choose no planetarium proposal."),
    _startup_failure("V6612-X1-N013", "stained-glass-lens-collided-with-two-frozen-phase-families", "Retain the rejected lens at zero credit and choose no stained-glass proposal."),
    _startup_failure("V6612-X1-N014", "carillon-lens-collided-with-the-frozen-change-ringing-phase-family", "Retain the rejected lens at zero credit and choose no bell, carillon, or change-ringing proposal."),
    _startup_failure("V6612-X1-N015", "worktree-add-wrapper-yielded-before-its-authorized-child-checkout-finished", "Retain the premature wrapper state at zero credit and wait for the exact authorized Git process tree to finish naturally."),
    _startup_failure("V6612-X1-N016", "premature-status-probe-observed-in-progress-index-deletions-during-authorized-checkout", "Retain the transient observation at zero credit, make no repair, and recheck only after the exact worktree-add process completed."),
    _startup_failure("V6612-X1-N017", "bounded-restore-preflight-refused-while-authorized-git-checkout-processes-were-live", "Retain the refused recovery at zero credit, perform no restore, wait for natural completion, and prove the resulting worktree clean."),
    _startup_failure("V6612-X1-N018", "first-read-only-data-summary-wrapper-lost-python-raw-string-quotes-at-the-powershell-boundary", "Retain the syntax rejection at zero credit and bind the module path process-locally with a quote-simple inspection command."),
    _startup_failure("V6612-X1-N019", "second-read-only-data-summary-wrapper-lost-python-subscript-quotes-in-native-argument-marshalling", "Retain the name-resolution rejection at zero credit and stream the bounded inspection program to Python standard input instead of using a native command-line code argument."),
    _startup_failure("V6612-X1-N020", "first-complete-novelty-screen-passed-eighteen-of-twenty-and-rejected-two-template-neighbour-titles", "Retain the eighteen-of-twenty witness at zero credit, preserve the threshold, and replace the terminal-deficit, handover, comparison, and near-neighbour network formulations with domain-specific mechanisms."),
    _startup_failure("V6612-X1-N021", "first-current-x1-suite-passed-twenty-one-of-twenty-three-and-found-two-missing-family-tool-receipt-families", "Retain the failed aggregate at zero credit, materialize only the declared workflow, governance, index, reflection, Method Flow, and meta-tool receipts, refresh manifests, and rerun the scoped x1 module once."),
    _startup_failure("V6612-X1-N022", "intentional-invalid-workflow-fixture-was-rejected-on-the-messaging-boundary", "Retain the rejecting workflow witness at zero credit, preserve its issue packet, and use the separately corrected request without changing the authorized route."),
]

# X2 failures may be appended only after the immutable x1 commit is pushed and
# proved clean and four-way equal.
PREFILLED_X1_X2_FAILURES_IGNORED: tuple[dict[str, object], ...] = tuple()
X2_FAILURES: list[dict[str, object]] = []
