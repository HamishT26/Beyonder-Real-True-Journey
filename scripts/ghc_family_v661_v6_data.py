#!/usr/bin/env python3
"""Frozen x1 planning data for Elowen Cairn v661-v6.

Tamar Vey's immutable v661-v5 surface supplies compatibility vocabulary only.
Twenty inherited rows are selected for bounded read-only revalidation with zero
Elowen novelty or completion credit. Only the twenty new piano-action rows
below extend the append-only proposal chain. Real instruments, people, work,
measurements, protected data, professional decisions, empirical claims,
production identity, legal or cultural ratification, and Māori authority remain
empty or exact-gated.
"""

from __future__ import annotations

from ghc_family_v661_v5_data import *  # noqa: F401,F403


PHASE = "v661-v6"
CANONICAL_PHASE = PHASE
PHASE_CODE = "V6616"
OWNER = "Elowen Cairn"
PRONOUNS = "they/them"
ROLE = "relational boundary cartographer and evidence steward"
HOPE = "make every transition legible, reversible, and honest about what remains unknown"
BRANCH = "codex/GHC-Family/elowen-cairn-v661-v6-full-tools"
PHASE_ROOT = "docs/elowen-cairn/v661-v6"

SOURCE_OWNER = "Tamar Vey"
SOURCE_BRANCH = "codex/GHC-Family/tamar-vey-v661-v5-full-tools"
SOURCE_BASE = "6834ba7c24025b0ecd36d280ac2d7a65913ba969"
SOURCE_X1 = "2827e1510ac38109bc474d1fa0b67bfa3e57ac69"
SOURCE_EVIDENCE = "b9765cf0b2c1847d969ae9ee5429d7031f6d8a0b"
SOURCE_FINAL = "e4526c5fa5b6e9cf184d0a65a13a15e069fe42b5"
SOURCE_CANONICAL_RECEIPT_SHA256 = (
    "b8b59fb52d46bd0a52fc24fa35d78e1f7807ef6d96b35d1b08cc7b11121a103b"
)
SOURCE_LIVE_ACTIVATION_STATE = "SENT_ONCE_ACKNOWLEDGED_BY_DIRECT_TARGET_REREAD"
ACTIVATION_PACKET_SHA256 = (
    "5f1007e4847f10ca81db79fc5a39e79b43efbcbc9df29f444a677d8ce2db6f66"
)
ACTIVATION_PACKET_BYTES = 266792
ACTIVATION_PACKET_LINES = 1260

PRIOR_FROZEN = 3390
SOURCE_SEALED_NEGATIVES = 21598
SOURCE_EXTERNAL_NEGATIVES = 4
ACTIVATION_NEGATIVES = SOURCE_SEALED_NEGATIVES + SOURCE_EXTERNAL_NEGATIVES
ACTIVATION_MESSAGE_NEGATIVE_BASELINE = 21602
SOURCE_OPEN_GAPS = 142
SOURCE_EXACT_GATES = 141
SOURCE_SEALED_METHODS = 6832
SOURCE_EXTERNAL_METHODS = 4
ACTIVATION_METHODS = SOURCE_SEALED_METHODS + SOURCE_EXTERNAL_METHODS
ACTIVATION_MESSAGE_METHOD_BASELINE = 6836

SELECTED_INHERITED_COUNT = 20
NEW_UNIQUE_COUNT = 20
CURRENT_PORTFOLIO_COUNT = 40
LATEST_TRACKED_SCAN_CAP = 5000
SELECTED_INHERITED_IDS = [f"V6615-P{i:03d}" for i in range(1, 21)]

PRIMARY_PILLAR = "GMUT Mind"
PRACTICE_LENS = (
    "bounded synthetic piano-action documentation and conservation-intake practice, "
    "including component topology, status uncertainty, accessibility, correction "
    "readback, workload control, and handover"
)
EXPECTED_DISTRIBUTION = {
    "completed": 14,
    "represented": 4,
    "open_gap": 1,
    "exact_gate": 1,
}
ALLOWED_OUTCOMES = set(EXPECTED_DISTRIBUTION)

PROTECTED_GATES = [
    "real_pianos_actions_keyboards_keys_hammers_dampers_strings_soundboards_pinblocks_bridges_pedals_trapwork_tools_workshops_collections_or_venues",
    "real_owners_players_technicians_tuners_regulators_conservators_clients_recipients_bystanders_children_affected_parties_and_authorities",
    "real_inspection_measurement_tuning_regulation_voicing_repair_replacement_handling_moving_sampling_treatment_imaging_publication_or_release_action",
    "professional_piano_technology_conservation_workplace_safety_accessibility_privacy_or_operational_authority",
    "empirical_gmut_prediction_likelihood_parameter_constraint_observational_confirmation_physical_discovery_or_final_physics",
    "blind_matched_budget_thos_real_arms_governed_participants_operators_safety_monitoring_statistics_and_independent_review",
    "production_identity_live_keys_signatures_proofs_issuance_resolution_status_revocation_interoperability_recovery_and_trust",
    "owner_player_client_recipient_identity_address_message_relationship_location_service_history_images_material_provenance_traditional_knowledge_collective_interest_and_remedy",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "legal_cultural_workplace_safety_intellectual_property_image_rights_ownership_custody_access_data_governance_and_maori_authority",
    "affected_party_notice_consent_contestation_correction_restriction_access_return_remedy_collective_governance_and_acceptance",
    "independent_team_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]


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


_NEW_ROWS = [
    (
        "piano-intake-identity-capsule",
        "Purpose ledger for a fabricated keyboard-instrument accession token: scoped aliases, revocable intake, source pinning, and an absolute no-service boundary",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic intake and revision tokens, purpose and instrument-class placeholders, source pin, recipient minimization, cancellation, correction, tombstone, and zero-real-instrument states",
        ["W3C-PROV", "W3C-VC2", "NZ-PRIVACY", "IETF-JCS"],
    ),
    (
        "piano-action-component-topology",
        "Piano action key, capstan, whippen, jack, repetition lever, hammer shank, flange, knuckle, backcheck, and rail topology with orphan quarantine",
        "completed",
        "GMUT Mind and THOS Body",
        "typed synthetic action-component tokens and relations, duplicate and orphan quarantine, contradiction retention, absent-condition states, reversible corrections, and no removal, adjustment, regulation, or operation action",
        ["PTG-PIANO-CARE", "W3C-PROV", "JSON-SCHEMA-2020-12"],
    ),
    (
        "piano-keyframe-rail-topology",
        "Keyboard keyframe, balance rail, front rail, key pin, bushing, key button, key stop, and action-interface graph with ambiguity quarantine",
        "completed",
        "GMUT Mind and THOS Body",
        "synthetic keyboard and keyframe nodes, rail and pin relations, interface placeholders, ambiguity retention, contradiction quarantine, and no disassembly, easing, fitting, or regulation instruction",
        ["PTG-PIANO-CARE", "W3C-PROV", "JSON-SCHEMA-2020-12"],
    ),
    (
        "piano-material-claim-quarantine",
        "Piano felt, leather, cloth, wood, metal, finish, supplier-label, stated origin, substitution, uncertainty, and authentication quarantine",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic component-material tokens, supplier-stated composition and origin claims, substitution and conflict holds, correction and supersession, and zero material identification, dating, attribution, or authenticity conclusion",
        ["SMITHSONIAN-OA", "W3C-PROV", "TE-MANA-RARAUNGA"],
    ),
    (
        "piano-regulation-measurement-envelope",
        "Key dip, blow distance, let-off, drop, checking, aftertouch, unit, resolution, covariance, missingness, uncertainty, and no-adjustment envelope",
        "completed",
        "GMUT Mind",
        "typed quantity placeholders with declared SI-compatible units, resolution, covariance, missingness, uncertainty, correction, and zero measurement rows, calibrated instruments, tolerances, adjustment targets, quality conclusions, or release decisions",
        ["NZ-MSL-SI", "PTG-PIANO-CARE", "W3C-PROV"],
    ),
    (
        "piano-damper-trapwork-lineage",
        "Damper, pedal, trapwork, lift-rod, sostenuto, linkage, sequence, change-point, correction, supersession, and no-service lineage",
        "completed",
        "GMUT Mind and THOS Body",
        "synthetic damper and pedal-system assertions, linkage and sequence placeholders, change points, correction, supersession, contradiction retention, and zero diagnosis, adjustment, repair, or operation",
        ["PTG-PIANO-CARE", "W3C-PROV", "IETF-JCS"],
    ),
    (
        "piano-hazard-hold",
        "Red-stop card for fabricated keyboard records: latent string energy, moving mass and pinch cues, escalation-only routing, and clearance vacancy",
        "completed",
        "CBR Heart and THOS Body",
        "synthetic hazard cues, access and isolation placeholders, warning and referral states, stop tokens, correction, competent-person reservations, and zero risk assessment, handling, moving, disassembly, repair, or safety clearance",
        ["WORKSAFE-MACHINERY", "WCAG22", "W3C-PROV"],
    ),
    (
        "piano-correction-nonerasure-lineage",
        "Piano intake, action state, component claim, hold, correction, supersession, cancellation, readback, unresolved ambiguity, and non-erasure lineage",
        "completed",
        "Freed ID and THOS Body",
        "synthetic intake, action-state and component assertions, hold events, correction, supersession, cancellation, readback, ambiguity quarantine, tombstones, and non-erasure",
        ["W3C-PROV", "IETF-JCS", "JSON-SCHEMA-2020-12"],
    ),
    (
        "piano-provenance-custody",
        "Custody braid for surrogate piano, action, component, service-note, and image placeholders with disclosure masks, reversible corrections, transfer holds, and anti-ownership boundary",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic instrument, action, component, record and absent-image placeholders, custody and transfer assertions, stated origin, disclosure masks, correction, contestation, and title refusal",
        ["W3C-PROV", "NZ-PRIVACY", "TE-MANA-RARAUNGA"],
    ),
    (
        "privacy-minimized-piano-service-notice",
        "Context-minimization map for fabricated keyboard service notes: collection purpose, disclosure ceiling, rectification route, retention hold, and zero publication",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic owner and client aliases, purpose and indirect-source flags, service-note and image placeholders, disclosure ceilings, access and correction routes, retention holds, and zero publication",
        ["NZ-PRIVACY", "W3C-VC2", "WCAG22"],
    ),
    (
        "accessible-piano-action-companion",
        "Keyboard-access map for synthetic action relations: ordered tables, narrated linkage, text-coded state, plain holds, and reserved human trials",
        "completed",
        "CBR Heart and THOS Body",
        "structural headings, component and relation tables, text alternatives, noncolour state, sequence narration, focus order, status messages, downloadable plain text, and zero manual, assistive-technology, Māori-language, or affected-user sessions",
        ["WCAG22", "W3C-PROV", "NZ-PRIVACY"],
    ),
    (
        "gmut-piano-action-constraint-graph",
        "Dimension-checked piano action constraint graph with boundary ports, incidence orientation, displacement placeholders, covariance guards, identifiability holds, and observation quarantine",
        "completed",
        "GMUT Mind",
        "typed symbolic action nodes, linkage edges, boundary ports, incidence orientation, displacement and force placeholders, units, covariance, equilibrium residuals, stability and identifiability obligations, counterexample slots, and zero observations",
        ["NZ-MSL-SI", "W3C-PROV", "IETF-JCS"],
    ),
    (
        "piano-action-authorization-firewall",
        "Piano opening, action removal, tuning, regulation, voicing, repair, replacement, moving, imaging, publication, and release action-authorization firewall",
        "completed",
        "CBR Heart and THOS Body",
        "synthetic action requests and scopes with technician, tuner, conservator, workplace-safety, owner, image-rights, legal, cultural, affected-party, and Māori-authority holds plus execution refusal",
        ["PTG-RPT-BOUNDARY", "WORKSAFE-MACHINERY", "NZ-PRIVACY", "TE-MANA-RARAUNGA"],
    ),
    (
        "stage20-piano-evidence-board",
        "No-promotion cut set for a fabricated keyboard packet: empty instrument, person, mandate, observation and external-review slots plus a Stage 20 stop",
        "completed",
        "All pillars",
        "typed evidence antichain, unfilled instrument, participant, authority, infrastructure, empirical and independent-team prerequisites, non-substitution rules, retained negatives, and terminal abstention",
        ["W3C-PROV", "IETF-JCS", "JSON-SCHEMA-2020-12"],
    ),
    (
        "gmut-piano-coupled-mode-proxy",
        "GMUT piano string-action-damper coupled-mode, anisotropy, damping, boundary, covariance, stability, and identifiability proxy with zero instrument observations",
        "represented",
        "GMUT Mind",
        "typed symbolic string-action-damper network, coupling and damping placeholders, boundary and covariance terms, zero fitted coefficients, zero likelihood rows, and physical-inference abstention",
        ["NZ-MSL-SI", "W3C-PROV", "IETF-JCS"],
    ),
    (
        "thos-piano-intake-handover",
        "Reciprocal THOS brief for unresolved synthetic keyboard custody: bounded queues, readback digest, stop authority, workload cap, and no operators",
        "represented",
        "THOS Body",
        "synthetic shift brief, unresolved intake, action, component, hazard and ambiguity queues, workload ceiling, stop token, correction readback, escalation, and zero workers or operators",
        ["WCAG22", "W3C-PROV", "NZ-PRIVACY"],
    ),
    (
        "piano-matched-budget-protocol",
        "Masked comparison design for two synthetic action-record explanations: balanced exposure, coded errors, zero enrolment, and no effectiveness claim",
        "represented",
        "THOS Body",
        "future randomized synthetic piano-action packets, balanced exposure time, two explanation formats, masked error coding, withdrawal and safety sentinels, zero enrolment, and no effectiveness claim",
        ["WCAG22", "W3C-PROV", "NZ-PRIVACY"],
    ),
    (
        "freed-id-piano-intake-profile",
        "Freed ID nonproduction graph profile for surrogate piano, action, component, service-note, image, and correction relations with namespace and status reservations",
        "represented",
        "Freed ID and CBR Heart",
        "synthetic instrument, action, component, record, image and relation identifiers, namespace and version placeholders, collisions, correction, supersession, status and revocation holds, privacy mask, zero keys or proofs, and nonproduction refusal",
        ["W3C-VC2", "W3C-VC-DI", "NZ-PRIVACY", "IETF-JCS"],
    ),
    (
        "smithsonian-piano-keyboard-zero-row-adapter",
        "Offline collection-metadata stub for keyboard instruments: zero rows, calls and keys, bounded pagination schema, uncertainty tags, and inference refusal",
        "open_gap",
        "GMUT Mind and Freed ID",
        "zero API keys, network calls, instrument rows, image rows, collection inferences, rights determinations, location disclosures, covariance rows, likelihood evaluations, posterior samples, constraints, or empirical claims",
        ["SMITHSONIAN-OA", "NZ-PRIVACY", "IETF-JCS"],
    ),
    (
        "piano-rights-authority",
        "Vacant mandate matrix for instrument safety, ownership, service authority, attribution, traditional knowledge, disclosure, collective interest, remedy, and tangata whenua, iwi, hapū, Māori governance",
        "exact_gate",
        "CBR Heart",
        "unoccupied owner, player, technician, tuner, conservator, client, recipient, bystander, regulator, accessibility, privacy, safety, image-rights, legal, cultural, collective-interest, tangata whenua, iwi, hapū, affected-party, remedy, and Māori-authority reservations",
        ["WORKSAFE-MACHINERY", "NZ-PRIVACY", "TE-MANA-RARAUNGA", "WCAG22"],
    ),
]
NEW_PROPOSAL_SPECS = [_proposal(*row) for row in _NEW_ROWS]

SELF_SAFE_CATEGORIES = [
    "Tamar source head and fresh equality",
    "activation packet and canonical receipt digests",
    "three-thousand-three-hundred-ninety-row proposal-chain parse",
    "twenty inherited selection identities",
    "twenty-title novelty screen",
    "mechanism-level piano-action and keyboard-instrument neighbour review",
    "new-outcome distribution",
    "workflow-plan policy",
    "identity and relational-language boundary",
    "Hamish-authorized Tamar-to-Elowen live edge and terminal-gated later route",
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
    {"task_id": f"V6616-SAFE-{i:03d}", "title": f"Validate {name} inside the Elowen-owned v661-v6 lane", "owner": OWNER}
    for i, name in enumerate(SELF_SAFE_CATEGORIES, 1)
]
SUCCESSOR_SAFE_SEEDS = [
    {"task_id": f"V6616-REC-SAFE-{i:03d}", "title": f"Reassess {name} in the later authorized owner lane", "recipient": "terminal_route_unresolved", "completion_credit": 0}
    for i, name in enumerate(SELF_SAFE_CATEGORIES[:20], 1)
]

SELF_CANDIDATE_CATEGORIES = [
    "synthetic piano intake identity capsule",
    "piano action component and relation topology tribunal",
    "keyframe, rail, pin, bushing, and action-interface graph",
    "component material claim and substitution quarantine",
    "regulation quantity, unit, covariance, and missingness envelope",
    "damper, pedal, trapwork, linkage, and correction lineage",
    "stored-tension, heavy-part, pinch, stop-token, referral, and no-clearance board",
    "piano correction, supersession, tombstone, and non-erasure lineage",
    "GMUT action constraint-graph obligation and observation-firewall board",
    "piano service privacy, image-rights, remedy, and Māori-authority circuit",
]
SELF_CANDIDATE_TASKS = [
    {"task_id": f"V6616-CAND-{i:03d}", "title": f"Build and test reversible {name}", "owner": OWNER}
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]
SUCCESSOR_CANDIDATE_SEEDS = [
    {"task_id": f"V6616-REC-CAND-{i:03d}", "title": f"Consider a distinct later-owner refinement of {name}", "recipient": "terminal_route_unresolved", "completion_credit": 0}
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]

EXACT_QUEUE = [
    {"task_id": f"V6616-EXACT-{i:03d}", "title": title, "state": "exact_gate_unexecuted"}
    for i, title in enumerate(
        [
            "Open, remove, tune, regulate, voice, repair, replace, move, image, publish, or release any real piano, action, component, tool, record, or work",
            "Make a real instrument, material, condition, hazard, conservation, product-safety, quality, rights, or release determination",
            "Use real owners, players, technicians, tuners, conservators, clients, recipients, bystanders, children, regulators, instruments, images, or personal information",
            "Disclose private owner or client identity, address, message, relationship, location, service history, image, supplier detail, traditional knowledge, or restricted provenance",
            "Make a professional piano-technology, conservation, workplace-safety, privacy, security, translation, or accessibility determination",
            "Publish a production instrument or service identifier, conservation record, credential, signature, proof, status, interoperability result, or operational record",
            "Allocate ownership, custody, attribution, service or image rights, disposal, access, remedy, beneficiary, or affected-party authority",
            "Make a tikanga, mātauranga, wording, naming, tangata whenua, iwi, hapū, Māori data-governance, cultural-protocol, taonga-status, or Māori-authority decision",
            "Run a real participant study, technician shift, piano trial, safety review, professional assessment, publication trial, or independent reproduction",
            "Perform destructive cleanup or any mutation outside the exact Elowen-owned lane",
        ],
        1,
    )
]
BLOCKED_QUEUE = [
    {"task_id": f"V6616-BLOCK-{i:03d}", "title": title, "state": "blocked_unexecuted"}
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
    ("ghc-family-piano-intake-identity", "Validate purpose-bound synthetic piano intake identity, revision, minimization, cancellation, and service refusal."),
    ("ghc-family-piano-action-topology", "Check synthetic action components, relations, duplicates, orphans, ambiguities, corrections, and operation refusal."),
    ("ghc-family-piano-keyframe-topology", "Preserve keyboard, rail, pin, bushing, interface, correction, and disassembly-refusal relations."),
    ("ghc-family-piano-material-claim-hold", "Preserve stated material, finish, origin, substitution, uncertainty, conflict, correction, and authentication refusal."),
    ("ghc-family-piano-measurement-envelope", "Expose quantity, unit, covariance, missingness, uncertainty, correction, and no-adjustment states."),
    ("ghc-family-piano-correction-lineage", "Preserve intake, action, component, hold, correction, supersession, cancellation, ambiguity, and non-erasure."),
    ("ghc-family-piano-privacy-minimization", "Keep owner, client, service-note, image, relationship, source, retention, disclosure, and correction data minimized."),
    ("ghc-family-piano-accessibility-companion", "Expose structural tables, noncolour state, sequence narration, alternatives, focus order, plain holds, and reserved human review."),
    ("ghc-family-gmut-piano-constraint-graph", "Preserve typed action graph, boundary, unit, covariance, equilibrium, stability, identifiability, and observation-firewall obligations."),
    ("ghc-family-piano-rights-authority", "Keep instrument safety, service and image rights, traditional knowledge, remedy, and Māori decision rights unoccupied."),
]
SUCCESSOR_SKILL_SEEDS = [
    {"name": name.replace("piano", "successor-domain"), "recipient": "terminal_route_unresolved", "state": "recommendation_only", "completion_credit": 0}
    for name, _ in SELF_SKILL_SPECS
]
SELF_RUNNER_SPECS = [
    (name.replace("ghc-family-", "ghc_family_").replace("-", "_") + ".py", purpose)
    for name, purpose in SELF_SKILL_SPECS
]
SUCCESSOR_RUNNER_SEEDS = [
    {"name": name.replace("piano", "successor_domain"), "recipient": "terminal_route_unresolved", "state": "recommendation_only", "completion_credit": 0}
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
    "keep real piano, action, component, project, participant, and connector rows empty",
    "retain scanner candidates separately from confirmed payload hits",
    "scan only declared public owner surfaces across five classes",
    "refresh owner manifests after every additive lifecycle change",
    "verify deterministic JSON ordering and parsing",
    "verify proposal append-only arithmetic",
    "verify inherited revalidation receives zero novelty and completion credit",
    "verify outcome labels use only the four authorized states",
    "reserve manual and affected-user accessibility evaluation",
    "reserve legal, cultural, workplace-safety, image-rights, and Māori authority",
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
    {"task_id": f"V6616-CLEAN-{i:03d}", "title": title, "owner": OWNER, "mode": "additive_review_only"}
    for i, title in enumerate(SELF_CLEAN_CATEGORIES, 1)
]
SUCCESSOR_CLEAN_SEEDS = [
    {"task_id": f"V6616-REC-CLEAN-{i:03d}", "title": title, "recipient": "terminal_route_unresolved", "completion_credit": 0}
    for i, title in enumerate(SELF_CLEAN_CATEGORIES, 1)
]

OFFICIAL_SOURCES = [
    ("PTG-PIANO-CARE", "primary_professional_association", "https://my.ptg.org/ptgmain/piano/care/care-faqs", "Current piano action, damper, trapwork, tuning and regulation vocabulary only; no credential, competence, diagnosis, service instruction, inspection, adjustment, or endorsement."),
    ("PTG-RPT-BOUNDARY", "primary_professional_association", "https://www.ptg.org/about/registered-piano-technician", "Current registered-technician credential boundary vocabulary only; Elowen does not hold or claim the credential, competence, membership, employment, or professional authority."),
    ("SMITHSONIAN-OA", "official_smithsonian", "https://www.si.edu/openaccess/faq", "Smithsonian Open Access metadata and API-readiness vocabulary only; zero API keys, network calls, rows, images, downloads, rights conclusions, collection inferences, or endorsement."),
    ("WORKSAFE-MACHINERY", "official_nz_workplace_regulator", "https://www.worksafe.govt.nz/topic-and-industry/machinery/safe-use-of-machinery/", "Current machine-hazard, isolation, stop and competent-duty-holder vocabulary only; no piano inspection, risk assessment, workplace compliance, handling decision, operation, training, or safety clearance."),
    ("NZ-MSL-SI", "official_nz_metrology_institute", "https://www.measurement.govt.nz/metrology/si-units", "Current SI quantity and unit vocabulary only; no real measurement, instrument, calibration, traceability, uncertainty result, piano-quality inference, or physical confirmation."),
    ("W3C-PROV", "official_w3c", "https://www.w3.org/TR/prov-o/", "Entity, activity, agent-placeholder, generation, derivation, revision, invalidation, and qualified-provenance vocabulary only."),
    ("W3C-VC2", "official_w3c", "https://www.w3.org/TR/vc-data-model-2.0/", "Credential subject, issuer, evidence, validity, status and privacy vocabulary only; zero keys, proofs, issuances, presentations, or production identities."),
    ("W3C-VC-DI", "official_w3c", "https://www.w3.org/TR/vc-data-integrity/", "Data-integrity context, verification-method and proof-structure vocabulary only; zero keys, signatures, cryptographic verification, or truth-of-claim conclusion."),
    ("WCAG22", "official_w3c", "https://www.w3.org/TR/WCAG22/", "Accessible structure, text alternative, noncolour, navigation, status, and interaction vocabulary with manual, assistive-technology, Māori-language, and affected-user evaluation reserved."),
    ("NZ-PRIVACY", "official_nz_privacy_commissioner", "https://www.privacy.org.nz/privacy-principles/", "Current New Zealand privacy-principle vocabulary including IPP 3A from May 2026 only; no legal, compliance, collection, disclosure, or remedy conclusion."),
    ("TE-MANA-RARAUNGA", "primary_maori_data_sovereignty_network", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Māori data-sovereignty and governance reservation vocabulary only; no Māori authority, ratification, wording, naming, tikanga, mātauranga, taonga-status, or cultural decision."),
    ("JSON-SCHEMA-2020-12", "primary_json_schema_project", "https://json-schema.org/draft/2020-12", "Schema, vocabulary, applicator, validation, annotation, and fail-closed structural vocabulary only."),
    ("IETF-JCS", "official_rfc_editor", "https://www.rfc-editor.org/rfc/rfc8785", "Canonical JSON digest vocabulary without key, signature, proof, credential, identity, or production claims."),
    ("GIT-LOG", "official_git_docs", "https://git-scm.com/docs/git-log", "Deterministic tracked-history selection and ancestry vocabulary."),
    ("PYTHON-JSON", "official_python_docs", "https://docs.python.org/3/library/json.html", "Deterministic UTF-8 JSON parse and serialization vocabulary."),
]
SOURCE_STATUS = {
    "PTG-PIANO-CARE": "current_primary_page_checked_2026_08_05",
    "PTG-RPT-BOUNDARY": "current_primary_page_checked_2026_08_05",
    "SMITHSONIAN-OA": "current_official_open_access_page_checked_2026_08_05",
    "WORKSAFE-MACHINERY": "current_official_safe_use_page_checked_2026_08_05",
    "NZ-MSL-SI": "current_official_si_units_page_checked_2026_08_05",
    "W3C-PROV": "stable_recommendation",
    "W3C-VC2": "recommendation_2025_checked_2026_08_05",
    "W3C-VC-DI": "recommendation_checked_2026_08_05",
    "WCAG22": "recommendation_2024",
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


_STARTUP_FAILURE_ROWS = [
    ("final-commit-timestamp-projection-returned-no-attributable-output", "Use a scalar git-log timestamp probe and retain the silent wrapper."),
    ("manifest-metadata-foreach-pipeline-parser-fault", "Materialize the bounded result array before projection."),
    ("combined-manifest-replay-wrapper-returned-no-attributable-output", "Read and parse each exact manifest separately without replaying Tamar's successful canonical pass."),
    ("first-x1-manifest-scalar-recovery-had-inline-python-quote-syntax-error", "Use quote-simple PowerShell and Python file probes."),
    ("second-x1-manifest-scalar-replay-returned-no-attributable-output", "Treat the canonical receipt and direct manifest parse as source evidence."),
    ("first-archive-manifest-replay-returned-no-attributable-output", "Abandon the aggregate archive replay at zero credit."),
    ("session-aware-archive-manifest-replay-exceeded-bounded-supervision", "Stop only the exact helper processes and retain the timeout."),
    ("backend-refused-control-c-for-archive-replay", "Identify and stop only exact process identifiers."),
    ("archive-process-inventory-foreach-pipeline-parser-fault", "Materialize a bounded process array before filtering."),
    ("combined-branch-path-preflight-hash-literal-parser-fault", "Split branch, path, and hash checks into literal scalar probes."),
    ("sequential-uniqueness-wrapper-returned-only-first-attributable-probe", "Run each uniqueness probe separately."),
    ("combined-path-space-clean-probe-returned-no-attributable-output", "Use literal path and free-space scalar checks."),
    ("sparse-checkout-list-probe-returned-no-attributable-output", "Inspect the sparse specification with an exact file and later Git scalar check."),
    ("no-checkout-worktree-empty-index-projected-apparent-deletions", "Populate the new worktree index from the exact head without resetting or rewriting history."),
    ("read-tree-process-inventory-foreach-pipeline-parser-fault", "Use a bounded materialized array and session polling."),
    ("first-session-poll-tool-input-had-invalid-javascript-token", "Correct the tool input and poll the same session without rerunning the process."),
    ("overbroad-piano-domain-term-search-returned-truncated-output", "Parse only the 3,390 frozen titles and use bounded candidate terms."),
    ("multi-source-web-open-exceeded-context-and-was-truncated", "Retain the truncated presentation and rely only on exact official pages materially used."),
    ("patch-relative-path-resolved-against-desktop-workspace", "Verify the three isolated new files, move them to exact D-first paths, and leave no C-drive copy."),
    ("apply-patch-command-inventory-foreach-pipeline-parser-fault", "Materialize exact path rows before JSON projection."),
    ("interactive-apply-patch-from-d-drive-returned-access-denied", "Use the callable patch surface with absolute D-first targets."),
    ("data-range-array-subtraction-probe-fault", "Read bounded line ranges with scalar endpoints."),
    ("parallel-template-inspection-returned-no-attributable-output", "Repeat only the needed scalar inspections."),
    ("first-bounded-novelty-summary-projected-an-incorrect-receipt-key", "Inspect the producer contract and project the declared nearest_prior_proposal_id key without rerunning any successful phase validator."),
    ("first-complete-3390-title-novelty-screen-rejected-eight-colliding-titles", "Retain the rejected receipt, preserve all mechanisms and expected labels, and reformulate only the eight colliding titles before repeating the bounded title screen."),
    ("first-x1-scoped-test-attempt-reached-21-passes-but-missed-two-family-tool-dependencies", "Retain the entire failed aggregate at zero credit, materialize only the named family-current outputs, refresh x1 receipts, and rerun the x1 gate."),
    ("windows-wildcard-was-passed-as-a-literal-rg-path-for-family-index-scripts", "Retain the path error and inspect the one exact script path returned by the bounded directory listing."),
    ("first-reflection-remaster-focus-triggered-a-30-second-git-caller-timeout", "Retain the timeout and rerun only the failed audit with the exact new piano-action focus, leaving broad caller equivalence unclaimed."),
    ("method-flow-validation-session-completed-but-its-final-poll-cell-was-lost", "Inspect the exact written receipt, preserve the presentation fault at zero credit, and use the validated receipt as the bounded passing witness."),
    ("second-x1-scoped-attempt-reached-22-passes-but-method-validation-receipt-drifted-after-manifest-refresh", "Retain the aggregate at zero credit, validate the updated Method Flow ledger, refresh the dependent manifest without changing the ledger, and rerun only manifest parity."),
    ("first-exact-x1-cached-diff-hygiene-check-found-a-blank-line-at-eof", "Retain the finding, remove exactly the surplus terminal line, refresh dependent receipts, and repeat cached diff hygiene."),
]
STARTUP_FAILURES = [
    _startup_failure(f"V6616-X1-N{i:03d}", signature, recovery)
    for i, (signature, recovery) in enumerate(_STARTUP_FAILURE_ROWS, 1)
]

PREFILLED_X1_X2_FAILURES_IGNORED: tuple[dict[str, object], ...] = tuple()
X2_FAILURES: list[dict[str, object]] = []
