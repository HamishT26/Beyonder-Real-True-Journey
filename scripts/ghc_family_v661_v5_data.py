#!/usr/bin/env python3
"""Frozen x1 planning data for Tamar Vey v661-v5.

Liora Venn's immutable v661-v4 surface supplies compatibility vocabulary only.
Twenty inherited rows are selected for bounded revalidation with zero Tamar
novelty or completion credit. Only the twenty new rows below extend the
append-only chain. Real handloom work, people, materials, protected data,
professional decisions, empirical claims, production identity, legal or
cultural ratification, and Māori authority remain empty or exact-gated.
"""

from __future__ import annotations

from ghc_family_v661_v4_data import *  # noqa: F401,F403


PHASE = "v661-v5"
CANONICAL_PHASE = PHASE
PHASE_CODE = "V6615"
OWNER = "Tamar Vey"
PRONOUNS = "she/they"
ROLE = "relational evidence-and-recovery steward"
HOPE = "keep every claim, correction, and handoff inspectable and retractable"
BRANCH = "codex/GHC-Family/tamar-vey-v661-v5-full-tools"
PHASE_ROOT = "docs/tamar-vey/v661-v5"

SOURCE_OWNER = "Liora Venn"
SOURCE_BRANCH = "codex/GHC-Family/liora-venn-v661-v4-full-tools"
SOURCE_BASE = "77cadeec2b7b8ce051b56f83fa1a815ec5926376"
SOURCE_X1 = "177e00fee935b76290bbd8c4cea9edba13681800"
SOURCE_EVIDENCE = "619d774a6bf32bf3fbe7a09abe0fd20e1fcd42bd"
SOURCE_FINAL = "6834ba7c24025b0ecd36d280ac2d7a65913ba969"
SOURCE_CLOSEOUT = SOURCE_FINAL
SOURCE_CLOSEOUT_BASE = SOURCE_FINAL
SOURCE_CANONICAL_RECEIPT_SHA256 = (
    "eac00ba7482ba4e64303aaffe176c0b07b4fa35f490e04af4dbc4c6f82512d4f"
)
SOURCE_LIVE_ACTIVATION_STATE = "SENT_ONCE_ACKNOWLEDGED_BY_DIRECT_TARGET_REREAD"
ACTIVATION_PACKET_SHA256 = (
    "21d05f569c9c97da7e28491eefb6c1805cbf13f2b63a4f32de01b7cfe016c383"
)
ACTIVATION_PACKET_BYTES = 255457
ACTIVATION_PACKET_LINES = 1212
X1_FREEZE = "pending_until_x2"

PRIOR_FROZEN = 3370
SOURCE_SEALED_NEGATIVES = 21437
# Both post-final failures are preserved externally without rewriting Liora's
# repository-sealed source count.
SOURCE_EXTERNAL_NEGATIVES = 2
ACTIVATION_NEGATIVES = SOURCE_SEALED_NEGATIVES + SOURCE_EXTERNAL_NEGATIVES
ACTIVATION_MESSAGE_NEGATIVE_BASELINE = 21439
SOURCE_OPEN_GAPS = 141
SOURCE_EXACT_GATES = 140
SOURCE_SEALED_METHODS = 6751
SOURCE_EXTERNAL_METHODS = 2
ACTIVATION_METHODS = SOURCE_SEALED_METHODS + SOURCE_EXTERNAL_METHODS
ACTIVATION_MESSAGE_METHOD_BASELINE = 6753
SELECTED_INHERITED_COUNT = 20
NEW_UNIQUE_COUNT = 20
CURRENT_PORTFOLIO_COUNT = SELECTED_INHERITED_COUNT + NEW_UNIQUE_COUNT
LATEST_TRACKED_SCAN_CAP = 5000

PRIMARY_PILLAR = "THOS Body"
PRACTICE_LENS = (
    "bounded synthetic community handloom project, loom-state, weaving-draft, "
    "warp and weft lineage, accessible notice, correction readback, workload "
    "control, and shift handover"
)

EXPECTED_DISTRIBUTION = {
    "completed": 14,
    "represented": 4,
    "open_gap": 1,
    "exact_gate": 1,
}
ALLOWED_OUTCOMES = set(EXPECTED_DISTRIBUTION)

PROTECTED_GATES = [
    "real_handloom_projects_looms_frames_beams_shafts_heddles_reeds_treadles_shuttles_bobbins_warp_weft_yarns_textiles_tools_studios_or_venues",
    "real_weavers_workers_clients_recipients_suppliers_conservators_bystanders_children_affected_parties_regulators_and_authorities",
    "real_material_identification_warping_threading_sleying_tying_tensioning_treadling_picking_beating_cutting_finishing_imaging_publication_or_release_action",
    "professional_weaving_textile_conservation_machinery_safety_accessibility_privacy_or_operational_authority",
    "empirical_gmut_prediction_likelihood_parameter_constraint_observational_confirmation_physical_discovery_or_final_physics",
    "blind_matched_budget_thos_real_arms_governed_participants_operators_safety_monitoring_statistics_and_independent_review",
    "production_identity_live_keys_signatures_proofs_issuance_resolution_status_revocation_interoperability_recovery_and_trust",
    "weaver_client_recipient_identity_address_message_relationship_location_project_history_drafts_images_material_provenance_traditional_knowledge_collective_interest_and_remedy",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "legal_cultural_machinery_safety_intellectual_property_image_rights_ownership_custody_access_data_governance_and_maori_authority",
    "affected_party_notice_consent_contestation_correction_restriction_access_return_remedy_collective_governance_and_acceptance",
    "independent_team_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]

SELECTED_INHERITED_IDS = [f"V6614-P{i:03d}" for i in range(1, 21)]


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
        "handloom-project-identity",
        "Surrogate handloom project identity capsule with declared purpose, loom-class placeholder, revision, source pin, recipient minimization, cancellation, and weaving refusal",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic project and revision tokens, purpose and loom-class placeholders, source pin, recipient minimization, cancellation, correction, tombstone, and zero-real-project states",
        ["W3C-PROV", "W3C-VC2", "NZ-PRIVACY", "IETF-JCS"],
    ),
    _proposal(
        "handloom-component-topology",
        "Handloom frame, warp beam, cloth beam, shaft, heddle, reed, treadle, shuttle, bobbin, and lease-stick topology with orphan quarantine and operation refusal",
        "completed",
        "Freed ID and THOS Body",
        "typed synthetic loom-component tokens and relations, duplicate and orphan quarantine, contradiction retention, absent-condition states, reversible corrections, and no assembly, adjustment, or operation action",
        ["WORKSAFE-MACHINERY", "W3C-PROV", "JSON-SCHEMA-2020-12"],
    ),
    _proposal(
        "handloom-draft-warp-topology",
        "Handloom draft, threading, tie-up, treadling, warp-end, cross, lease, dent, sleying, and sequence graph with ambiguity quarantine and no setup instruction",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic draft cells, shaft and treadle indices, threading, tie-up and treadling sequences, warp-end groups, cross and lease relations, dent placeholders, ambiguity retention, and no warping or loom-setup authorization",
        ["W3C-PROV", "JSON-SCHEMA-2020-12", "IETF-JCS"],
    ),
    _proposal(
        "handloom-yarn-claim-quarantine",
        "Handloom warp and weft yarn lot, supplier-label, fibre-content placeholder, twist, colour, finish, stated origin, substitution, uncertainty, and authentication quarantine",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic warp and weft yarn-lot tokens, supplier-stated fibre, twist, colour, finish and origin claims, substitution and conflict holds, correction and supersession, and zero material identification or authenticity conclusion",
        ["SMITHSONIAN-OA", "W3C-PROV", "TE-MANA-RARAUNGA"],
    ),
    _proposal(
        "handloom-dimension-tension-envelope",
        "Warp length, width, sett, denting, pick density, yarn count, tension, resolution, covariance, missingness, uncertainty, correction, and no-quality-inference envelope",
        "completed",
        "GMUT Mind and THOS Body",
        "typed length, width, density and tension placeholders with declared SI-compatible units, resolution, covariance, missingness, uncertainty, correction and zero measurement rows, calibrated instruments, strength findings, quality conclusions, or release decisions",
        ["NZ-MSL-SI", "W3C-PROV", "IETF-JCS"],
    ),
    _proposal(
        "handloom-weft-sequence-lineage",
        "Shuttle, bobbin, weft lot, pick sequence, selvedge placeholder, colour-order, change point, correction, supersession, and no-weaving lineage",
        "completed",
        "GMUT Mind and THOS Body",
        "synthetic shuttle, bobbin, weft-lot and pick-sequence assertions, selvedge and colour-order placeholders, change points, correction, supersession, contradiction retention, and zero weaving action",
        ["W3C-PROV", "JSON-SCHEMA-2020-12", "IETF-JCS"],
    ),
    _proposal(
        "handloom-machinery-hazard-hold",
        "Handloom pinch, crush, entanglement, stored-tension, falling-part, sharp-tool, access, isolation, stop token, referral, and safety-clearance refusal board",
        "completed",
        "CBR Heart and THOS Body",
        "synthetic hazard cues, access and isolation placeholders, warning and referral states, stop tokens, correction, competent-person reservations, and zero risk assessment, guarding decision, machinery use, treatment, or safety clearance",
        ["WORKSAFE-MACHINERY", "WCAG22", "W3C-PROV"],
    ),
    _proposal(
        "handloom-correction-nonerasure-lineage",
        "Handloom project, loom state, draft, warp and weft sequence, hold, correction, supersession, cancellation, readback, unresolved ambiguity, and non-erasure lineage",
        "completed",
        "Freed ID and THOS Body",
        "synthetic project, loom-state, draft, warp and weft assertions, hold events, correction, supersession, cancellation, readback, ambiguity quarantine, tombstones, and non-erasure",
        ["W3C-PROV", "IETF-JCS", "JSON-SCHEMA-2020-12"],
    ),
    _proposal(
        "handloom-provenance-custody",
        "Custody braid for surrogate handloom drafts, yarn lots, work-in-progress records, and images with disclosure masks, reversible corrections, transfer holds, and anti-ownership boundary",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic loom, yarn, draft, work-in-progress and image placeholders, custody and transfer assertions, stated origin, absent-image references, disclosure masks, correction, contestation, and title refusal",
        ["W3C-PROV", "NZ-PRIVACY", "TE-MANA-RARAUNGA"],
    ),
    _proposal(
        "privacy-minimized-handloom-design-notice",
        "Purpose-bound indirect-source minimization ledger for surrogate handloom drafts, sketches, and media with disclosure ceiling, rectification path, retention hold, and no release",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic weaver and client aliases, purpose and indirect-source flags, draft attribution and image placeholders, disclosure ceilings, access and correction routes, retention holds, and zero publication",
        ["NZ-PRIVACY", "W3C-VC2", "WCAG22"],
    ),
    _proposal(
        "accessible-handloom-draft-companion",
        "Multimodal handloom-draft companion with threading, tie-up and treadling tables, noncolour status, narrated sequence, keyboard order, plain hold text, and evaluation vacancy",
        "completed",
        "CBR Heart and THOS Body",
        "structural headings, draft and project tables, text alternatives, noncolour state, sequence narration, focus order, status messages, downloadable plain text, and zero manual, assistive-technology, Māori-language, or affected-user sessions",
        ["WCAG22", "NZ-PRIVACY", "W3C-PROV"],
    ),
    _proposal(
        "gmut-handloom-lattice-obligations",
        "Dimension-checked bipartite warp-weft lattice obligation kernel with boundary ports, incidence orientation, tension placeholders, covariance guards, identifiability holds, and observation quarantine",
        "completed",
        "GMUT Mind",
        "typed symbolic warp and weft nodes, crossing edges, boundary ports, incidence orientation, tension and displacement placeholders, units, covariance, equilibrium residuals, stability and identifiability obligations, counterexample slots, and zero observations",
        ["NZ-MSL-SI", "W3C-PROV", "IETF-JCS"],
    ),
    _proposal(
        "handloom-action-authorization-firewall",
        "Handloom assembly, warping, threading, sleying, tying, tensioning, treadling, picking, beating, cutting, finishing, imaging, publication, and release action-authorization firewall",
        "completed",
        "CBR Heart and THOS Body",
        "synthetic action requests and scopes with weaver, technician, machinery-safety, conservator, client, image-rights, legal, cultural, affected-party, and Māori-authority holds plus execution refusal",
        ["WORKSAFE-MACHINERY", "SMITHSONIAN-OA", "NZ-PRIVACY", "TE-MANA-RARAUNGA"],
    ),
    _proposal(
        "stage20-handloom-evidence-board",
        "Terminal evidence cut-set for the handloom packet with unfilled object, person, mandate, infrastructure, observation, external-team, and Stage 20 prerequisites",
        "completed",
        "All pillars",
        "typed evidence antichain, unfilled material, participant, authority, infrastructure, empirical and independent-team prerequisites, non-substitution rules, retained negatives, and terminal abstention",
        ["W3C-PROV", "IETF-JCS", "JSON-SCHEMA-2020-12"],
    ),
    _proposal(
        "gmut-handloom-tension-network-proxy",
        "GMUT handloom warp-weft tension-network, anisotropy, coupling, damping, boundary, covariance, stability, and identifiability proxy with zero textile observations",
        "represented",
        "GMUT Mind",
        "typed symbolic warp-weft network, anisotropy, coupling and damping placeholders, boundary and covariance terms, zero fitted coefficients, zero likelihood rows, and physical-inference abstention",
        ["NZ-MSL-SI", "W3C-PROV", "IETF-JCS"],
    ),
    _proposal(
        "thos-handloom-handover",
        "THOS reciprocal shift brief for synthetic loom configuration, unresolved draft debt, warp alarms, stop tokens, readback digest, workload ceiling, and zero operators",
        "represented",
        "THOS Body",
        "synthetic shift brief, unresolved project, loom, draft, warp, hazard and ambiguity queues, workload ceiling, stop token, correction readback, escalation, and zero workers or operators",
        ["WCAG22", "W3C-PROV", "NZ-PRIVACY"],
    ),
    _proposal(
        "handloom-matched-budget-protocol",
        "Counterbalanced zero-participant evaluation plan comparing graph-guided and sequence-guided handloom record interpretation under matched exposure and masked error coding",
        "represented",
        "THOS Body",
        "future randomized synthetic handloom packets, balanced exposure time, two explanation formats, masked error coding, withdrawal and safety sentinels, zero enrolment, and no effectiveness claim",
        ["WCAG22", "W3C-PROV", "NZ-PRIVACY"],
    ),
    _proposal(
        "freed-id-handloom-profile",
        "Freed ID nonproduction graph profile for surrogate handloom project, loom, draft, yarn, warp, weft, image, and correction relations with namespace and status reservations",
        "represented",
        "Freed ID and CBR Heart",
        "synthetic project, loom, draft, yarn, warp, weft, image and relation identifiers, namespace and version placeholders, collisions, correction, supersession, status and revocation holds, privacy mask, zero keys or proofs, and nonproduction refusal",
        ["W3C-VC2", "W3C-VC-DI", "NZ-PRIVACY", "IETF-JCS"],
    ),
    _proposal(
        "smithsonian-handloom-textile-zero-row-adapter",
        "Zero-ingestion Smithsonian collection-vocabulary bridge for loom and woven-object metadata, licensing fields, pagination budget, digests, uncertainty, covariance, and likelihood refusal",
        "open_gap",
        "GMUT Mind and Freed ID",
        "zero API keys, network calls, object rows, image rows, collection inferences, rights determinations, location disclosures, covariance rows, likelihood evaluations, posterior samples, constraints, or empirical claims",
        ["SMITHSONIAN-OA", "NZ-PRIVACY", "IETF-JCS"],
    ),
    _proposal(
        "handloom-rights-authority",
        "Vacant mandate matrix for loom safety, draft authorship, traditional design, disclosure, collective interest, remedy, affected-party consent, and tangata whenua, iwi, hapū, Māori governance",
        "exact_gate",
        "CBR Heart",
        "unoccupied weaver, worker, supplier, client, recipient, bystander, regulator, conservator, accessibility, privacy, machinery-safety, image-rights, legal, cultural, collective-interest, tangata whenua, iwi, hapū, affected-party, remedy, and Māori-authority reservations",
        ["WORKSAFE-MACHINERY", "NZ-PRIVACY", "TE-MANA-RARAUNGA", "WCAG22"],
    ),
]

SELF_SAFE_CATEGORIES = [
    "Liora source head and fresh equality",
    "activation packet and external receipt digests",
    "three-thousand-three-hundred-seventy-row proposal-chain parse",
    "twenty inherited selection identities",
    "twenty-title novelty screen",
    "mechanism-level handloom and woven-textile-neighbour review",
    "new-outcome distribution",
    "workflow-plan policy",
    "identity and relational-language boundary",
    "Hamish-authorized Liora-to-Tamar live edge and terminal-gated Tamar-to-Elowen edge",
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
    {"task_id": f"V6615-SAFE-{i:03d}", "title": f"Validate {name} inside the Tamar-owned v661-v5 lane", "owner": OWNER}
    for i, name in enumerate(SELF_SAFE_CATEGORIES, 1)
]
SUCCESSOR_SAFE_SEEDS = [
    {"task_id": f"V6615-REC-SAFE-{i:03d}", "title": f"Reassess {name} for Elowen-only v661-v6", "recipient": "Elowen Cairn", "completion_credit": 0}
    for i, name in enumerate(SELF_SAFE_CATEGORIES[:20], 1)
]

SELF_CANDIDATE_CATEGORIES = [
    "synthetic handloom project identity capsule",
    "loom component and relation topology tribunal",
    "draft, threading, tie-up, treadling, warp-end, and denting graph",
    "warp and weft yarn claim and substitution quarantine",
    "dimension, density, tension, covariance, and missingness envelope",
    "shuttle, bobbin, pick-sequence, and correction lineage",
    "machinery hazard cue, stop-token, referral, and no-clearance board",
    "handloom correction, supersession, tombstone, and non-erasure lineage",
    "GMUT bipartite warp-weft lattice obligation and observation-firewall board",
    "handloom design, privacy, image-rights, remedy, and Māori-authority circuit",
]
SELF_CANDIDATE_TASKS = [
    {"task_id": f"V6615-CAND-{i:03d}", "title": f"Build and test reversible {name}", "owner": OWNER}
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]
SUCCESSOR_CANDIDATE_SEEDS = [
    {"task_id": f"V6615-REC-CAND-{i:03d}", "title": f"Consider a distinct Elowen-owned refinement of {name}", "recipient": "Elowen Cairn", "completion_credit": 0}
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]

EXACT_QUEUE = [
    {"task_id": f"V6615-EXACT-{i:03d}", "title": title, "state": "exact_gate_unexecuted"}
    for i, title in enumerate(
        [
            "Assemble, warp, thread, sley, tie, tension, treadle, pick, beat, cut, finish, image, publish, or release any real loom, draft, warp, weft, yarn, textile, tool, work, or design",
            "Make a real material-identification, machinery-hazard, conservation, product-safety, quality, image-rights, or release determination",
            "Use real weavers, workers, clients, recipients, suppliers, conservators, bystanders, children, regulators, materials, projects, designs, images, or personal information",
            "Disclose private weaver or client identity, address, message, relationship, location, project history, draft, image, supplier detail, traditional knowledge, or restricted provenance",
            "Make a professional weaving, textile-conservation, machinery-safety, privacy, security, translation, or accessibility determination",
            "Publish a production project, draft, loom, yarn, or textile identifier, conservation record, credential, signature, proof, status, interoperability result, or operational record",
            "Allocate ownership, custody, attribution, draft or image rights, disposal, access, remedy, beneficiary, or affected-party authority",
            "Make a tikanga, mātauranga, wording, naming, tangata whenua, iwi, hapū, Māori data-governance, cultural-protocol, taonga-status, or Māori-authority decision",
            "Run a real participant study, weaving shift, loom trial, machinery review, professional assessment, publication trial, or independent reproduction",
            "Perform destructive cleanup or any mutation outside the exact Tamar-owned lane",
        ],
        1,
    )
]
BLOCKED_QUEUE = [
    {"task_id": f"V6615-BLOCK-{i:03d}", "title": title, "state": "blocked_unexecuted"}
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
    ("ghc-family-handloom-project-identity", "Validate synthetic purpose-bound handloom project identity, revision, minimization, cancellation, and operation refusal."),
    ("ghc-family-handloom-component-topology", "Check synthetic frames, beams, shafts, heddles, reeds, treadles, shuttles, bobbins, leases, orphans, and operation refusal."),
    ("ghc-family-handloom-draft-topology", "Preserve draft threading, tie-up, treadling, warp-end, cross, lease, dent, correction, and setup-refusal relations."),
    ("ghc-family-handloom-yarn-claim-hold", "Preserve stated yarn, fibre, twist, finish, origin, substitution, uncertainty, conflict, correction, and authentication refusal."),
    ("ghc-family-handloom-measurement-envelope", "Expose dimension, density, tension, unit, covariance, missingness, uncertainty, and no-quality-inference states."),
    ("ghc-family-handloom-correction-lineage", "Preserve loom, draft, warp, weft, hold, correction, supersession, cancellation, ambiguity, and non-erasure."),
    ("ghc-family-handloom-privacy-minimization", "Keep weaver, client, draft, image, relationship, source, retention, disclosure, and correction data minimized."),
    ("ghc-family-handloom-accessibility-companion", "Expose structural draft tables, noncolour state, sequence narration, alternatives, focus order, plain-language holds, and reserved human review."),
    ("ghc-family-gmut-handloom-lattice", "Preserve typed warp-weft graph, boundary, unit, covariance, equilibrium, stability, identifiability, and observation-firewall obligations."),
    ("ghc-family-handloom-rights-authority", "Keep machinery safety, draft and image rights, traditional knowledge, remedy, and Māori decision rights unoccupied."),
]
SUCCESSOR_SKILL_SEEDS = [
    {"name": name.replace("handloom", "successor-domain"), "recipient": "Elowen Cairn", "state": "recommendation_only", "completion_credit": 0}
    for name, _ in SELF_SKILL_SPECS
]
SELF_RUNNER_SPECS = [
    (name.replace("ghc-family-", "ghc_family_").replace("-", "_") + ".py", purpose)
    for name, purpose in SELF_SKILL_SPECS
]
SUCCESSOR_RUNNER_SEEDS = [
    {"name": name.replace("handloom", "successor_domain"), "recipient": "Elowen Cairn", "state": "recommendation_only", "completion_credit": 0}
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
    "keep real loom, yarn, textile, project, participant, and connector rows empty",
    "retain scanner candidates separately from confirmed payload hits",
    "scan only declared public owner surfaces across five classes",
    "refresh owner manifests after every additive lifecycle change",
    "verify deterministic JSON ordering and parsing",
    "verify proposal append-only arithmetic",
    "verify inherited revalidation receives zero novelty and completion credit",
    "verify outcome labels use only the four authorized states",
    "reserve manual and affected-user accessibility evaluation",
    "reserve legal, cultural, machinery-safety, image-rights, and Māori authority",
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
    {"task_id": f"V6615-CLEAN-{i:03d}", "title": title, "owner": OWNER, "mode": "additive_review_only"}
    for i, title in enumerate(SELF_CLEAN_CATEGORIES, 1)
]
SUCCESSOR_CLEAN_SEEDS = [
    {"task_id": f"V6615-REC-CLEAN-{i:03d}", "title": title, "recipient": "Elowen Cairn", "completion_credit": 0}
    for i, title in enumerate(SELF_CLEAN_CATEGORIES, 1)
]

OFFICIAL_SOURCES = [
    ("SMITHSONIAN-OA", "official_smithsonian", "https://www.si.edu/openaccess/faq", "Smithsonian Open Access metadata and API-readiness vocabulary only; zero API keys, network calls, rows, images, downloads, rights conclusions, collection inferences, or endorsement."),
    ("WORKSAFE-MACHINERY", "official_nz_workplace_regulator", "https://www.worksafe.govt.nz/topic-and-industry/machinery/safe-use-of-machinery/", "Current machine-hazard, guarding, isolation, stop and competent-duty-holder vocabulary only; no loom inspection, risk assessment, workplace compliance, guarding decision, operation, training, or safety clearance."),
    ("NZ-MSL-SI", "official_nz_metrology_institute", "https://www.measurement.govt.nz/metrology/si-units", "Current SI quantity and unit vocabulary only; no real measurement, instrument, calibration, traceability, uncertainty result, textile-quality inference, or physical confirmation."),
    ("W3C-PROV", "official_w3c", "https://www.w3.org/TR/prov-o/", "Entity, activity, agent-placeholder, generation, derivation, revision, invalidation, and qualified-provenance vocabulary only."),
    ("W3C-VC2", "official_w3c", "https://www.w3.org/TR/vc-data-model-2.0/", "Current credential subject, issuer, evidence, validity, status and privacy vocabulary only; zero keys, proofs, issuances, presentations, or production identities."),
    ("W3C-VC-DI", "official_w3c", "https://www.w3.org/TR/vc-data-integrity/", "Data-integrity context, verification-method and proof-structure vocabulary only; zero keys, signatures, cryptographic verification, or truth-of-claim conclusion."),
    ("WCAG22", "official_w3c", "https://www.w3.org/TR/WCAG22/", "Accessible structure, text alternative, noncolour, navigation, status, and interaction vocabulary with manual, assistive-technology, Māori-language, and affected-user evaluation reserved."),
    ("NZ-PRIVACY", "official_nz_privacy_commissioner", "https://www.privacy.org.nz/privacy-principles/", "Current New Zealand privacy-principle vocabulary including IPP 3A from May 2026 only; no legal, compliance, collection, disclosure, or remedy conclusion."),
    ("TE-MANA-RARAUNGA", "primary_maori_data_sovereignty_network", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Māori data-sovereignty and governance reservation vocabulary only; no Māori authority, ratification, wording, naming, tikanga, mātauranga, taonga-status, or cultural decision."),
    ("JSON-SCHEMA-2020-12", "primary_json_schema_project", "https://json-schema.org/draft/2020-12", "Schema, vocabulary, tuple, applicator, validation, annotation, and fail-closed structural vocabulary only."),
    ("IETF-JCS", "official_rfc_editor", "https://www.rfc-editor.org/rfc/rfc8785", "Canonical JSON digest vocabulary without key, signature, proof, credential, identity, or production claims."),
    ("GIT-LOG", "official_git_docs", "https://git-scm.com/docs/git-log", "Deterministic tracked-history selection and ancestry vocabulary."),
    ("PYTHON-JSON", "official_python_docs", "https://docs.python.org/3/library/json.html", "Deterministic UTF-8 JSON parse and serialization vocabulary."),
]
SOURCE_STATUS = {
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


STARTUP_FAILURES = [
    _startup_failure("V6615-X1-N001", "runtime-lacked-sha256-hashdata-helper", "Retain the unavailable API result and use the supported incremental SHA-256 implementation."),
    _startup_failure("V6615-X1-N002", "runtime-lacked-convert-tohexstring-helper", "Retain the unavailable API result and encode the supported digest with bounded lowercase hexadecimal formatting."),
    _startup_failure("V6615-X1-N003", "byte-aggregation-flattened-arrays-and-produced-unbounded-conversion-errors", "Retain the failed digest wrapper, stop it exactly, and use one bounded stream hash implementation."),
    _startup_failure("V6615-X1-N004", "unified-exec-backend-refused-control-c-for-runaway-helper", "Retain the refused interrupt and recover by identifying and stopping only the exact helper process."),
    _startup_failure("V6615-X1-N005", "first-targeted-helper-cleanup-matched-its-own-command-line", "Retain the self-match and recover with an exact process identifier and literal executable check."),
    _startup_failure("V6615-X1-N006", "overbroad-phase-skill-search-returned-truncated-output", "Retain the truncated search and read only the activation-named skills and direct required references through EOF."),
    _startup_failure("V6615-X1-N007", "powershell-foreach-pipeline-form-had-an-empty-pipe-parser-fault", "Retain the parser fault and materialize the bounded result array before projection."),
    _startup_failure("V6615-X1-N008", "inline-python-quote-construction-raised-a-syntax-error", "Retain the syntax failure and use quote-simple bounded scalar probes."),
    _startup_failure("V6615-X1-N009", "full-auth-current-state-display-was-truncated", "Retain the truncated display and read the exact file in bounded sequential chunks through EOF."),
    _startup_failure("V6615-X1-N010", "broad-external-receipt-hash-walk-exceeded-bounded-supervision", "Retain the timeout and resolve the exact receipt path before hashing one file."),
    _startup_failure("V6615-X1-N011", "backend-refused-control-c-for-receipt-hash-walk", "Retain the refused interrupt and stop only the exact Python process identified by PID."),
    _startup_failure("V6615-X1-N012", "broad-thread-tool-catalog-filter-was-truncated", "Retain the truncated discovery and use only the exact bounded task tools at the terminal gate."),
    _startup_failure("V6615-X1-N013", "first-source-task-read-returned-an-overlarge-truncated-history", "Retain the truncated read and recover with the committed activation plus a compact newest-turn projection."),
    _startup_failure("V6615-X1-N014", "combined-branch-and-path-uniqueness-wrapper-returned-no-attributable-output", "Retain the silent wrapper and prove uniqueness with separate scalar branch, remote-ref, and literal-path probes."),
    _startup_failure("V6615-X1-N015", "overbroad-domain-novelty-search-returned-a-305580-token-truncated-result", "Retain the overbroad probe and parse only the exact 3,370-row frozen-title index with bounded candidate terms."),
    _startup_failure("V6615-X1-N016", "parallel-numbered-data-chunk-wrapper-returned-no-attributable-output", "Retain the silent wrapper and read each bounded numbered file window separately."),
    _startup_failure("V6615-X1-N017", "perl-mechanical-rewrite-command-was-unavailable", "Retain the unavailable-tool witness and use a bounded UTF-8 PowerShell mechanical rewrite followed by exact diff review."),
    _startup_failure("V6615-X1-N018", "combined-post-rewrite-label-scan-returned-no-attributable-output", "Retain the silent wrapper and use no-login scalar reads plus bounded exact-pattern scans."),
    _startup_failure("V6615-X1-N019", "first-standalone-novelty-producer-hit-cp1252-and-left-the-consumer-empty", "Retain both attributable errors as one failed pipeline invocation and pin PYTHONIOENCODING to UTF-8 before generating and consuming the exact title array."),
    _startup_failure("V6615-X1-N020", "first-utf8-novelty-screen-passed-only-fourteen-of-twenty-titles", "Retain the rejected receipt, preserve each mechanism and expected label, rename only the six colliding titles, and rerun the bounded screen before freeze."),
    _startup_failure("V6615-X1-N021", "literal-x1-allowlist-staging-was-blocked-by-the-sparse-index-boundary", "Retain the zero-staged refusal and repeat the identical literal allowlist with git add --sparse without changing sparse rules or adding any undeclared path."),
    _startup_failure("V6615-X1-N022", "combined-cached-blob-audit-returned-no-attributable-payload", "Retain the silent wrapper and split recovery into exact staged-name parity, Git-clean staged-to-working byte parity, manifest replay, cached diff hygiene, and receipt-bound privacy counts."),
    _startup_failure("V6615-X1-N023", "second-python-cached-blob-parity-wrapper-returned-no-attributable-payload", "Retain the silent wrapper, stop using per-path git-show subprocesses, and prove index parity with zero unstaged paths plus the already-passing manifest unit test and direct scalar receipt reads."),
]

# X2 failures are appended only after the immutable x1 commit is pushed and
# proved clean and four-way equal.
PREFILLED_X1_X2_FAILURES_IGNORED: tuple[dict[str, object], ...] = tuple()
X2_FAILURES: list[dict[str, object]] = []
