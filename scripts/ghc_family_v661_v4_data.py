#!/usr/bin/env python3
"""Frozen x1 planning data for Liora Venn v661-v4.

Orin Thale's immutable v661-v3 surface supplies compatibility vocabulary only.
Twenty inherited rows are selected for bounded revalidation with zero Liora
novelty or completion credit. Only the twenty new rows below extend the
append-only chain. Real paper-marbling work, people, materials, protected data,
professional decisions, empirical claims, production identity, legal or
cultural ratification, and Māori authority remain empty or exact-gated.
"""

from __future__ import annotations

from ghc_family_v661_v3_data import *  # noqa: F401,F403


PHASE = "v661-v4"
CANONICAL_PHASE = PHASE
PHASE_CODE = "V6614"
OWNER = "Liora Venn"
PRONOUNS = "she/they"
ROLE = "relational continuity-and-evidence steward"
HOPE = "make every boundary legible and every correction easier than concealment"
BRANCH = "codex/GHC-Family/liora-venn-v661-v4-full-tools"
PHASE_ROOT = "docs/liora-venn/v661-v4"

SOURCE_OWNER = "Orin Thale"
SOURCE_BRANCH = "codex/GHC-Family/orin-thale-v661-v3-full-tools"
SOURCE_BASE = "7197e39b3d1ecc29e44d4598405f2975d249345b"
SOURCE_X1 = "e7529a4bc2ddb4c095fc6a1ebbd6933f8d2faa8f"
SOURCE_EVIDENCE = "21c05d5f2d2701ef7e83292ccfcddea734f4c023"
SOURCE_CLOSEOUT = SOURCE_EVIDENCE
SOURCE_FINAL = "77cadeec2b7b8ce051b56f83fa1a815ec5926376"
SOURCE_CLOSEOUT_BASE = SOURCE_FINAL
SOURCE_CANONICAL_RECEIPT_SHA256 = (
    "2e3f62bb892eba9f38ddd536f13a8118e903fd0abfd1a26b90ca76079018a2ea"
)
SOURCE_LIVE_ACTIVATION_STATE = "SENT_ONCE_ACKNOWLEDGED_BY_DIRECT_TARGET_REREAD"
ACTIVATION_PACKET_SHA256 = (
    "e3ba1b6f0176047b083694ba41dc29be0f136d03af2e733ae4a36c826ae833bc"
)
ACTIVATION_PACKET_BYTES = 270746
ACTIVATION_PACKET_LINES = 1302
X1_FREEZE = "pending_until_x2"

PRIOR_FROZEN = 3350
SOURCE_SEALED_NEGATIVES = 21287
# N001 was present in the delivered activation. N002 was discovered later in
# Orin's read-only post-send record and is preserved without rewriting either
# the delivered baseline or Orin's sealed repository count.
SOURCE_EXTERNAL_NEGATIVES = 2
ACTIVATION_NEGATIVES = SOURCE_SEALED_NEGATIVES + SOURCE_EXTERNAL_NEGATIVES
ACTIVATION_MESSAGE_NEGATIVE_BASELINE = 21288
SOURCE_OPEN_GAPS = 140
SOURCE_EXACT_GATES = 139
SOURCE_SEALED_METHODS = 6681
SOURCE_EXTERNAL_METHODS = 2
ACTIVATION_METHODS = SOURCE_SEALED_METHODS + SOURCE_EXTERNAL_METHODS
ACTIVATION_MESSAGE_METHOD_BASELINE = 6682
SELECTED_INHERITED_COUNT = 20
NEW_UNIQUE_COUNT = 20
CURRENT_PORTFOLIO_COUNT = SELECTED_INHERITED_COUNT + NEW_UNIQUE_COUNT
LATEST_TRACKED_SCAN_CAP = 5000

PRIMARY_PILLAR = "GMUT Mind"
PRACTICE_LENS = (
    "bounded synthetic community paper-marbling job and sheet-lot intake, bath "
    "and colour-state documentation, pattern-transfer placeholders, accessible "
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
    "real_paper_marbling_jobs_sheets_papers_trays_baths_pigments_inks_binders_surfactants_thickeners_mordants_solvents_tools_water_rinses_dryers_presses_studios_or_venues",
    "real_makers_workers_clients_recipients_suppliers_conservators_bystanders_children_affected_parties_regulators_and_authorities",
    "real_material_identification_preparation_mixing_dropping_combing_transfer_rinsing_drying_pressing_trimming_disposal_imaging_publication_or_release_action",
    "professional_paper_marbling_paper_conservation_chemical_safety_waste_accessibility_privacy_or_operational_authority",
    "empirical_gmut_prediction_likelihood_parameter_constraint_observational_confirmation_physical_discovery_or_final_physics",
    "blind_matched_budget_thos_real_arms_governed_participants_operators_safety_monitoring_statistics_and_independent_review",
    "production_identity_live_keys_signatures_proofs_issuance_resolution_status_revocation_interoperability_recovery_and_trust",
    "maker_client_recipient_identity_address_message_relationship_location_job_history_design_images_material_provenance_traditional_knowledge_collective_interest_and_remedy",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "legal_cultural_chemical_safety_waste_intellectual_property_image_rights_ownership_custody_access_data_governance_and_maori_authority",
    "affected_party_notice_consent_contestation_correction_restriction_access_return_remedy_collective_governance_and_acceptance",
    "independent_team_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]

SELECTED_INHERITED_IDS = [f"V6613-P{i:03d}" for i in range(1, 21)]


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
        "paper-marbling-job-identity",
        "Surrogate paper-marbling job identity capsule with purpose, sheet-count placeholder, revision, source pin, recipient minimization, cancellation, and production refusal",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic job and revision tokens, purpose and sheet-count placeholders, source pin, recipient minimization, cancellation, correction, tombstone, and zero-real-job states",
        ["W3C-PROV", "W3C-VC2", "NZ-PRIVACY", "IETF-JCS"],
    ),
    _proposal(
        "paper-sheet-lot-topology",
        "Paper sheet-lot, tray, carrier, trial-strip, finished-sheet placeholder, split, merge, substitution, orphan, and handling-refusal graph",
        "completed",
        "Freed ID and THOS Body",
        "typed synthetic sheet lots, trays, carriers and trial strips, split and merge edges, finished-sheet placeholders, substitutions, orphan quarantine, contradiction retention, and no handling action",
        ["LOC-PAPER-CARE", "W3C-PROV", "JSON-SCHEMA-2020-12"],
    ),
    _proposal(
        "paper-material-claim-quarantine",
        "Paper fibre, sizing, coating, supplier-label, stated-origin, uncertainty, conflict, correction, and material-authentication quarantine",
        "completed",
        "Freed ID and CBR Heart",
        "supplier-stated paper, fibre, sizing, coating and origin claims, source distinctions, uncertainty and conflict, correction and supersession, and material-authentication refusal",
        ["LOC-PAPER-CARE", "W3C-PROV", "IIIF-PRESENTATION"],
    ),
    _proposal(
        "paper-marbling-bath-state",
        "Synthetic paper-marbling bath, tray, thickener label, water-source placeholder, preparation time, contamination cue, compatibility unknown, and use-refusal ledger",
        "completed",
        "THOS Body",
        "synthetic bath and tray tokens, stated thickener and water labels, preparation timestamps, contamination cues, compatibility unknowns, quarantine, and zero mixing or application",
        ["NIST-SI", "OSHA-HAZCOM", "W3C-PROV"],
    ),
    _proposal(
        "paper-marbling-floating-colour-state",
        "Paper-marbling colourant, binder, surfactant, drop sequence, dilution placeholder, contamination cue, incompatibility, correction, and mixing-refusal board",
        "completed",
        "GMUT Mind and THOS Body",
        "synthetic colourant, binder and surfactant tokens, drop sequence and dilution placeholders, contamination and incompatibility cues, correction, quarantine, and zero real mixing",
        ["NIST-SI", "OSHA-HAZCOM", "W3C-PROV"],
    ),
    _proposal(
        "paper-marbling-pattern-tool-topology",
        "Paper-marbling stylus, comb, rake, spacing placeholder, stroke sequence, pattern label, revision, breakage cue, and process-authorization refusal map",
        "completed",
        "GMUT Mind and THOS Body",
        "synthetic tool tokens, spacing placeholders, stroke sequences, pattern labels, revisions, breakage cues, contradiction retention, and no combing or process authorization",
        ["W3C-PROV", "JSON-SCHEMA-2020-12", "IETF-JCS"],
    ),
    _proposal(
        "paper-marbling-chemical-hazard-hold",
        "Paper-marbling pigment, surfactant, preservative, mordant, solvent, unknown mixture, label, SDS placeholder, exposure cue, referral, and safety-clearance refusal board",
        "completed",
        "CBR Heart and THOS Body",
        "synthetic chemical-label and SDS placeholders, mixture and exposure unknowns, warning and referral states, stop tokens, correction, and zero hazard classification, handling, treatment, or clearance",
        ["OSHA-HAZCOM", "WCAG22", "W3C-PROV"],
    ),
    _proposal(
        "paper-marbling-pattern-transfer-lineage",
        "Paper-marbling job, bath state, colour sequence, tool path, sheet lot, transfer placeholder, correction, supersession, cancellation, readback, and ambiguity lineage",
        "completed",
        "Freed ID and THOS Body",
        "synthetic job, bath, colour, tool-path and sheet assertions, transfer placeholders, correction, supersession, cancellation, readback, ambiguity hold, and non-erasure",
        ["W3C-PROV", "IETF-JCS", "JSON-SCHEMA-2020-12"],
    ),
    _proposal(
        "marbled-paper-provenance-custody",
        "Custody braid for surrogate marbling artifacts with disclosure masks, origin assertions, reversible corrections, transfer holds, and anti-ownership boundary",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic material, tool, bath and sheet placeholders, custody and transfer assertions, stated origin, absent-image references, disclosure masks, correction, contestation, and title refusal",
        ["W3C-PROV", "NZ-PRIVACY", "TE-MANA-RARAUNGA"],
    ),
    _proposal(
        "privacy-minimized-paper-marbling-design-notice",
        "Privacy-minimized paper-marbling design and image notice with purpose binding, indirect-source flag, attribution placeholder, disclosure ceiling, correction path, and publication refusal",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic maker and client aliases, purpose and indirect-source flags, attribution and image placeholders, disclosure ceilings, access and correction routes, retention holds, and zero publication",
        ["NZ-PRIVACY", "W3C-VC2", "WCAG22"],
    ),
    _proposal(
        "accessible-paper-marbling-companion",
        "Multimodal navigation contract for surrogate marbling records with structural relations, nonchromatic status, narrated sequence, keyboard order, plain hold text, and evaluation vacancy",
        "completed",
        "CBR Heart and THOS Body",
        "structural headings, job and sheet tables, text alternatives, noncolour state, sequence narration, focus order, status messages, downloadable plain text, and zero manual or affected-user sessions",
        ["WCAG22", "NZ-PRIVACY", "W3C-PROV"],
    ),
    _proposal(
        "gmut-paper-marbling-transport-obligations",
        "Dimension-checked free-surface state-transition kernel for a zero-observation marbling proxy with flux ports, dissipation guards, uncertainty partitions, and inference quarantine",
        "completed",
        "GMUT Mind",
        "typed symbolic surface field and transport edges, state and flux placeholders, source and dissipation terms, units and uncertainty, identifiability limits, counterexample slots, and zero observations",
        ["NIST-SI", "W3C-PROV", "IETF-JCS"],
    ),
    _proposal(
        "paper-marbling-action-authorization-firewall",
        "Paper-marbling preparation, mixing, dropping, combing, transfer, rinsing, drying, pressing, trimming, disposal, imaging, and release action-authorization firewall",
        "completed",
        "CBR Heart and THOS Body",
        "synthetic action requests and scopes with maker, conservator, chemical-safety, waste, client, image-rights, legal, cultural, affected-party, and Māori-authority holds plus execution refusal",
        ["OSHA-HAZCOM", "LOC-PAPER-CARE", "NZ-PRIVACY", "TE-MANA-RARAUNGA"],
    ),
    _proposal(
        "stage20-paper-marbling-evidence-board",
        "Nonpromotion lattice separating surrogate marbling software from missing material, human, governance, infrastructure, observational, external-team, and Stage 20 evidence",
        "completed",
        "All pillars",
        "typed evidence antichain, unfilled material, participant, authority, infrastructure, empirical and independent-team prerequisites, non-substitution rules, retained negatives, and terminal abstention",
        ["W3C-PROV", "IETF-JCS", "JSON-SCHEMA-2020-12"],
    ),
    _proposal(
        "gmut-paper-marbling-interface-proxy",
        "GMUT paper-marbling free-surface pigment-interface, Marangoni placeholder, viscosity, boundary, covariance, stability, and identifiability proxy with zero fluid observations",
        "represented",
        "GMUT Mind",
        "typed symbolic free-surface, pigment-interface, viscosity and Marangoni placeholders, boundary and covariance terms, zero fitted coefficients, zero likelihood rows, and physical-inference abstention",
        ["NIST-SI", "W3C-PROV", "IETF-JCS"],
    ),
    _proposal(
        "thos-paper-marbling-handover",
        "THOS two-way handover envelope for surrogate bath-state work queues, hazard pauses, correction echo, bounded load, and worker-free fixtures",
        "represented",
        "THOS Body",
        "synthetic shift brief, unresolved job, bath, hazard and ambiguity queues, bath-state budget, workload ceiling, stop token, correction readback, escalation, and zero workers",
        ["WCAG22", "W3C-PROV", "NZ-PRIVACY"],
    ),
    _proposal(
        "paper-marbling-matched-budget-protocol",
        "Empty-arm comparison protocol for paired marbling explanations using blinded synthetic packets, equal exposure budgets, masked scoring, withdrawal marker, and no enrolment",
        "represented",
        "THOS Body",
        "future randomized synthetic job packets, balanced exposure time, two explanation formats, masked error coding, withdrawal and safety sentinels, zero enrolment, and no effectiveness claim",
        ["WCAG22", "W3C-PROV", "NZ-PRIVACY"],
    ),
    _proposal(
        "freed-id-marbled-sheet-profile",
        "Freed ID nonproduction graph profile for surrogate marbling records with job, bath, sheet, pattern, image links, namespace boundaries, collision holds, minimization, corrections, and status reservations",
        "represented",
        "Freed ID and CBR Heart",
        "synthetic job, bath, sheet, pattern, image and relation identifiers, namespace and version placeholders, collisions, correction, supersession, status and revocation holds, privacy mask, zero keys or proofs, and nonproduction refusal",
        ["W3C-VC2", "W3C-VC-DI", "NZ-PRIVACY", "IETF-JCS"],
    ),
    _proposal(
        "smithsonian-marbled-paper-zero-row-adapter",
        "Smithsonian Open Access marbled-paper object and image evidence adapter with query purpose, object identifier, title, date, medium, rights, image metadata, pagination, checksum, covariance, likelihood, and zero-row refusal",
        "open_gap",
        "GMUT Mind and Freed ID",
        "zero network calls, object rows, image rows, collection inferences, rights determinations, location disclosures, covariance rows, likelihood evaluations, posterior samples, constraints, or empirical claims",
        ["SI-OPEN-ACCESS", "IIIF-PRESENTATION", "NZ-PRIVACY", "IETF-JCS"],
    ),
    _proposal(
        "paper-marbling-rights-authority",
        "Unoccupied authority circuit for chemical safety, material handling, design attribution, image publication, cultural pattern, remedy, data governance, affected-party legitimacy, and Māori decision non-substitution",
        "exact_gate",
        "CBR Heart",
        "unoccupied maker, worker, supplier, client, recipient, bystander, regulator, conservator, accessibility, privacy, chemical-safety, waste, image-rights, legal, cultural, collective-interest, tangata whenua, iwi, hapū, affected-party, remedy, and Māori-authority reservations",
        ["OSHA-HAZCOM", "NZ-PRIVACY", "TE-MANA-RARAUNGA", "WCAG22"],
    ),
]

SELF_SAFE_CATEGORIES = [
    "Orin source head and fresh equality",
    "activation packet and external receipt digests",
    "three-thousand-three-hundred-fifty-row proposal-chain parse",
    "twenty inherited selection identities",
    "twenty-title novelty screen",
    "mechanism-level paper-marbling-neighbour review",
    "new-outcome distribution",
    "workflow-plan policy",
    "identity and relational-language boundary",
    "Hamish-authorized Orin-to-Liora live edge",
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
    {"task_id": f"V6614-SAFE-{i:03d}", "title": f"Validate {name} inside the Liora-owned v661-v4 lane", "owner": OWNER}
    for i, name in enumerate(SELF_SAFE_CATEGORIES, 1)
]
SUCCESSOR_SAFE_SEEDS = [
    {"task_id": f"V6614-REC-SAFE-{i:03d}", "title": f"Reassess {name} for Tamar-only v661-v5", "recipient": "Tamar Vey", "completion_credit": 0}
    for i, name in enumerate(SELF_SAFE_CATEGORIES[:20], 1)
]

SELF_CANDIDATE_CATEGORIES = [
    "synthetic paper-marbling job identity capsule",
    "sheet-lot, tray, trial-strip, split, merge, and substitution topology tribunal",
    "paper material, sizing, stated-origin, uncertainty, and correction quarantine",
    "marbling bath, tray, contamination-cue, and use-refusal ledger",
    "colourant, binder, surfactant, and drop-sequence state board",
    "stylus, comb, rake, spacing, stroke-sequence, and process-refusal map",
    "chemical label, SDS placeholder, exposure cue, referral, and no-clearance board",
    "paper-marbling correction and non-erasure lineage",
    "GMUT surface-transport obligation and observation-firewall board",
    "paper-marbling privacy, image-rights, remedy, and Māori-authority circuit",
]
SELF_CANDIDATE_TASKS = [
    {"task_id": f"V6614-CAND-{i:03d}", "title": f"Build and test reversible {name}", "owner": OWNER}
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]
SUCCESSOR_CANDIDATE_SEEDS = [
    {"task_id": f"V6614-REC-CAND-{i:03d}", "title": f"Consider a distinct Tamar-owned refinement of {name}", "recipient": "Tamar Vey", "completion_credit": 0}
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]

EXACT_QUEUE = [
    {"task_id": f"V6614-EXACT-{i:03d}", "title": title, "state": "exact_gate_unexecuted"}
    for i, title in enumerate(
        [
            "Prepare, identify, mix, drop, comb, transfer, rinse, dry, press, trim, dispose of, image, publish, or release any real paper, bath, pigment, ink, binder, surfactant, thickener, mordant, solvent, tool, sheet, or design",
            "Make a real material-identification, chemical-hazard, conservation, waste, product-safety, quality, image-rights, or release determination",
            "Use real makers, workers, clients, recipients, suppliers, conservators, bystanders, children, regulators, materials, jobs, designs, images, or personal information",
            "Disclose private maker or client identity, address, message, relationship, location, job history, design, image, supplier detail, traditional knowledge, or restricted provenance",
            "Make a professional paper-marbling, paper-conservation, chemical-safety, waste, privacy, security, translation, or accessibility determination",
            "Publish a production job or sheet identifier, conservation record, credential, signature, proof, status, interoperability result, or operational record",
            "Allocate ownership, custody, attribution, image rights, disposal, access, remedy, beneficiary, or affected-party authority",
            "Make a tikanga, mātauranga, wording, naming, tangata whenua, iwi, hapū, Māori data-governance, cultural-protocol, taonga-status, or Māori-authority decision",
            "Run a real participant study, paper-marbling shift, handling trial, chemical review, professional assessment, publication trial, or independent reproduction",
            "Perform destructive cleanup or any mutation outside the exact Liora-owned lane",
        ],
        1,
    )
]
BLOCKED_QUEUE = [
    {"task_id": f"V6614-BLOCK-{i:03d}", "title": title, "state": "blocked_unexecuted"}
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
    ("ghc-family-paper-marbling-job-identity", "Validate synthetic purpose-bound paper-marbling job identity, revision, minimization, cancellation, and production refusal."),
    ("ghc-family-paper-marbling-sheet-lot-topology", "Check synthetic sheet lots, trays, carriers, trial strips, splits, merges, substitutions, orphans, and handling refusal."),
    ("ghc-family-paper-marbling-material-claim-hold", "Preserve stated paper and material claims, origins, uncertainty, conflicts, corrections, and authentication refusal."),
    ("ghc-family-paper-marbling-bath-state", "Preserve synthetic baths, trays, thickener labels, contamination cues, compatibility unknowns, and use refusal."),
    ("ghc-family-paper-marbling-pattern-tool-topology", "Expose synthetic stylus, comb, rake, spacing, stroke sequence, breakage, revision, and process-refusal states."),
    ("ghc-family-paper-marbling-correction-lineage", "Preserve job, bath, colour, tool path, sheet, transfer, correction, supersession, cancellation, ambiguity, and non-erasure."),
    ("ghc-family-paper-marbling-privacy-minimization", "Keep maker, client, design, image, relationship, source, retention, disclosure, and correction data minimized."),
    ("ghc-family-paper-marbling-accessibility-companion", "Expose structural tables, noncolour state, sequence narration, alternatives, focus order, plain-language holds, and reserved human review."),
    ("ghc-family-gmut-paper-marbling-transport", "Preserve typed surface transport, boundary, source, unit, covariance, stability, identifiability, and observation-firewall obligations."),
    ("ghc-family-paper-marbling-rights-authority", "Keep chemical safety, image rights, cultural pattern, remedy, and Māori decision rights unoccupied."),
]
SUCCESSOR_SKILL_SEEDS = [
    {"name": name.replace("paper-marbling", "successor-domain"), "recipient": "Tamar Vey", "state": "recommendation_only", "completion_credit": 0}
    for name, _ in SELF_SKILL_SPECS
]
SELF_RUNNER_SPECS = [
    (name.replace("ghc-family-", "ghc_family_").replace("-", "_") + ".py", purpose)
    for name, purpose in SELF_SKILL_SPECS
]
SUCCESSOR_RUNNER_SEEDS = [
    {"name": name.replace("paper_marbling", "successor_domain"), "recipient": "Tamar Vey", "state": "recommendation_only", "completion_credit": 0}
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
    "keep real paper, bath, colourant, job, participant, and connector rows empty",
    "retain scanner candidates separately from confirmed payload hits",
    "scan only declared public owner surfaces across five classes",
    "refresh owner manifests after every additive lifecycle change",
    "verify deterministic JSON ordering and parsing",
    "verify proposal append-only arithmetic",
    "verify inherited revalidation receives zero novelty and completion credit",
    "verify outcome labels use only the four authorized states",
    "reserve manual and affected-user accessibility evaluation",
    "reserve legal, cultural, chemical-safety, image-rights, and Māori authority",
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
    {"task_id": f"V6614-CLEAN-{i:03d}", "title": title, "owner": OWNER, "mode": "additive_review_only"}
    for i, title in enumerate(SELF_CLEAN_CATEGORIES, 1)
]
SUCCESSOR_CLEAN_SEEDS = [
    {"task_id": f"V6614-REC-CLEAN-{i:03d}", "title": title, "recipient": "Tamar Vey", "completion_credit": 0}
    for i, title in enumerate(SELF_CLEAN_CATEGORIES, 1)
]

OFFICIAL_SOURCES = [
    ("LOC-PAPER-CARE", "official_us_library", "https://www.loc.gov/preservation/care/paper.html", "Works-on-paper handling, support, enclosure, environment, and light-exposure vocabulary only; no treatment, material identification, conservation, handling, storage, or professional determination."),
    ("NARA-FADGI", "official_us_archives", "https://www.archives.gov/records-mgmt/policy/digitization", "FADGI 2023 digitization-policy and technical-metadata vocabulary only; no real object, image, measurement, quality, compliance, or preservation conclusion."),
    ("IIIF-PRESENTATION", "primary_iiif_consortium", "https://iiif.io/api/presentation/3.0/", "Current stable 3.0.0 Manifest, Canvas, Annotation, structure, rights-link and presentation vocabulary only; zero publication, hosted resource, dereference, or interoperability claim."),
    ("SI-OPEN-ACCESS", "official_smithsonian", "https://www.si.edu/openaccess/faq", "Smithsonian Open Access metadata and API-readiness vocabulary only; zero keys, network calls, rows, images, downloads, rights conclusions, or collection inferences."),
    ("OSHA-HAZCOM", "official_us_workplace_safety_regulator", "https://www.osha.gov/hazcom/", "Hazard-label and safety-data-sheet structure vocabulary only; no workplace, substance, mixture, exposure, classification, compliance, training, handling, or safety determination."),
    ("NIST-SI", "official_us_metrology_institute", "https://www.nist.gov/publications/guide-use-international-system-units-si", "Current SI quantity, unit and reporting vocabulary only; no measurement, calibration, uncertainty result, process-quality inference, or physical confirmation."),
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
    "LOC-PAPER-CARE": "current_official_page_checked_2026_08_05",
    "NARA-FADGI": "fadgi_2023_guidelines_page_current_checked_2026_08_05",
    "IIIF-PRESENTATION": "latest_stable_3_0_0_checked_2026_08_05",
    "SI-OPEN-ACCESS": "current_official_open_access_page_checked_2026_08_05",
    "OSHA-HAZCOM": "current_hazard_communication_page_checked_2026_08_05",
    "NIST-SI": "sp811_page_updated_2026_05_07_checked_2026_08_05",
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
    _startup_failure("V6614-X1-N001", "login-profile-read-only-wrappers-returned-no-attributable-output", "Retain the empty wrappers and use no-profile scalar commands with explicit exit and payload checks."),
    _startup_failure("V6614-X1-N002", "broad-external-receipt-digest-content-scan-exceeded-bounded-supervision", "Retain the bounded timeout, stop only the exact search helpers, and resolve the exact receipt path from the read-only source task before hashing it."),
    _startup_failure("V6614-X1-N003", "first-selected-revalidation-invariant-projection-guessed-numeric-mutation-fields", "Retain the false assumption and inspect the exact JSON keys and Boolean zero-credit semantics before evaluating the invariant."),
    _startup_failure("V6614-X1-N004", "powershell-selected-revalidation-detail-projection-used-an-empty-foreach-pipe", "Retain the parser rejection and materialize the result array before JSON conversion."),
    _startup_failure("V6614-X1-N005", "powershell-manifest-detail-projection-used-an-empty-foreach-pipe", "Retain the parser rejection and collect manifest projections in an explicit array before conversion."),
    _startup_failure("V6614-X1-N006", "per-entry-python-manifest-replay-completed-without-attributable-output", "Retain the silent replay at zero credit and use one communicate-style cat-file batch with an attributable structured summary."),
    _startup_failure("V6614-X1-N007", "first-batch-manifest-inline-python-f-string-lost-literal-quotes", "Retain the syntax error and use quote-simple concatenation in the bounded batch transport."),
    _startup_failure("V6614-X1-N008", "guessed-phase-lifecycle-filename-was-absent", "Retain the missing-path assumption and list the exact bounded lifecycle directory before reading its actual anchor contract."),
    _startup_failure("V6614-X1-N009", "powershell-command-discovery-projection-used-an-empty-foreach-pipe", "Retain the parser rejection and materialize command-discovery rows before projection."),
    _startup_failure("V6614-X1-N010", "workflow-summary-probe-guessed-two-absent-method-flow-filenames", "Retain the guessed names and enumerate the exact method-flow directory before reading both state files."),
    _startup_failure("V6614-X1-N011", "source-task-reread-request-exceeded-the-live-per-item-output-limit", "Retain the rejected read-only request and retry once at the documented maximum without messaging the source task."),
    _startup_failure("V6614-X1-N012", "eight-turn-source-task-projection-exceeded-the-output-budget", "Retain the truncated projection and request only the two newest turns before locally selecting agent messages."),
    _startup_failure("V6614-X1-N013", "combined-candidate-domain-powershell-projection-returned-no-attributable-output", "Retain the silent projection and use a bounded UTF-8 Python JSON parser over the exact 3350-row chain."),
    _startup_failure("V6614-X1-N014", "temporary-file-digest-wrapper-was-rejected-before-execution", "Retain the policy rejection and compute the exact immutable blob digest in memory without a temporary file."),
    _startup_failure("V6614-X1-N015", "python-unicode-repr-projection-hit-the-default-cp1252-encoder", "Retain the encoding failure and pin PYTHONIOENCODING to UTF-8 before Unicode-emitting diagnostics."),
    _startup_failure("V6614-X1-N016", "first-data-patch-assumed-a-shifted-bare-current-owner-label", "Retain the rejected patch and reread the exact current lines before applying smaller verified hunks."),
    _startup_failure("V6614-X1-N017", "first-category-patch-assumed-shifted-bare-source-labels", "Retain the rejected patch and patch exact bare labels only after a UTF-8 numbered reread."),
    _startup_failure("V6614-X1-N018", "first-stale-label-ripgrep-orchestration-script-had-an-extra-closing-parenthesis", "Retain the JavaScript syntax rejection and rerun the same bounded read-only search with a syntactically checked wrapper."),
    _startup_failure("V6614-X1-N019", "first-novelty-probe-invocation-omitted-the-required-index-and-standard-input-title-array", "Retain the argparse rejection and invoke the read-only probe with the immutable 3,350-row index plus the exact twenty preregistered titles on standard input."),
    _startup_failure("V6614-X1-N020", "first-x1-build-hit-a-sparse-checkout-missing-inherited-v659-v8-data-module", "Retain the import failure and add only the immutable tracked v659-v7/v659-v8 data dependency patterns to this owner worktree's sparse materialization before rebuilding."),
    _startup_failure("V6614-X1-N021", "first-sparse-checkout-add-used-an-unsupported-no-cone-option-on-the-add-subcommand", "Retain the usage rejection and add the two bounded patterns under the worktree's already-active non-cone mode without repeating that option."),
    _startup_failure("V6614-X1-N022", "first-materialized-novelty-gate-rejected-at-least-one-new-title-above-the-bounded-overlap-threshold", "Retain the rejected x1 build, inspect the exact prior and peer collision scores, and rename only colliding proposals without changing their preregistered mechanisms or expected truth labels."),
    _startup_failure("V6614-X1-N023", "first-corrected-novelty-pipeline-lost-python-string-quotes-and-fed-empty-input-to-the-probe", "Retain both attributable pipeline errors as one failed invocation and use a PowerShell-safe double-quoted Python program with single-quoted literals before rerunning the read-only probe."),
    _startup_failure("V6614-X1-N024", "mechanical-template-copy-materialized-untracked-x2-and-closeout-seeds-before-the-immutable-x1-boundary", "Retain the premature-materialization fault, remove only Liora's seven reproducible untracked x2/closeout seeds, prove no x2 surface remains, and recreate them from Orin's immutable source only after x1 is pushed clean and fresh-remote equal."),
    _startup_failure("V6614-X1-N025", "first-combined-current-label-scan-used-an-unterminated-powershell-quoted-pattern", "Retain the parser failure and perform the bounded stale-current-label review with a UTF-8 Python literal list instead of a shell-quoted alternation."),
    _startup_failure("V6614-X1-N026", "first-combined-domain-scan-passed-windows-wildcards-as-literal-ripgrep-paths", "Retain the two invalid-path diagnostics and use explicit directories plus include globs, while adjudicating inherited selected-row and novelty-neighbour matches separately."),
    _startup_failure("V6614-X1-N027", "first-python-current-label-scan-lost-an-apostrophe-bearing-literal-through-the-shell", "Retain the syntax failure and use a PowerShell SimpleMatch array containing only quote-safe stale-current phrases over the five exact x1 code paths."),
]

# X2 failures are appended only after the immutable x1 commit is pushed and
# proved clean and four-way equal.
PREFILLED_X1_X2_FAILURES_IGNORED: tuple[dict[str, object], ...] = tuple()
X2_FAILURES: list[dict[str, object]] = []
