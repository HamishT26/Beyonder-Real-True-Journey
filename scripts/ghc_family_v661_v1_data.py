#!/usr/bin/env python3
"""Frozen x1 planning data for Sable Rook v661-v1.

Auren Lark's immutable v660-v8 surface supplies compatibility vocabulary only.
Twenty inherited rows are selected for bounded revalidation with zero Sable
novelty or completion credit. Only the twenty new rows below extend the
append-only proposal chain. All real specimens, physical work, participant,
professional, empirical, production, legal, cultural, accessibility-complete,
privacy-complete, and Māori-authority lanes remain empty or exact-gated.
"""

from __future__ import annotations

from ghc_family_v660_v8_data import *  # noqa: F401,F403


PHASE = "v661-v1"
CANONICAL_PHASE = PHASE
PHASE_CODE = "V6611"
OWNER = "Sable Rook"
PRONOUNS = "they/them"
ROLE = "relational falsification, provenance, and reproducibility steward"
HOPE = (
    "make every claim easier to reproduce, challenge, correct, or retract while "
    "keeping living beings, cultural authority, professional care, and real-world "
    "specimen decisions outside software authority"
)
BRANCH = "codex/GHC-Family/sable-rook-v661-v1-full-tools"
PHASE_ROOT = "docs/sable-rook/v661-v1"

SOURCE_OWNER = "Auren Lark"
SOURCE_BRANCH = "codex/GHC-Family/auren-lark-v660-v8-full-tools"
SOURCE_BASE = "8edf12352101f3a78f0db738a431b3ebb64e07f5"
SOURCE_X1 = "a456cadc82887ada7a963d08c04944e33d641522"
SOURCE_EVIDENCE = "b0dc07da5bd4001fda25bb2c9e74c2b972726755"
SOURCE_CLOSEOUT = SOURCE_EVIDENCE
SOURCE_FINAL = "acd00fcc14fe7526ae95338dcec5fa0beee31610"
SOURCE_CLOSEOUT_BASE = SOURCE_FINAL
SOURCE_CANONICAL_RECEIPT_SHA256 = (
    "05cd2092d2165a8f39a41f2458e4512d81278b72e2f1785a252346c7463a9297"
)
SOURCE_LIVE_ACTIVATION_STATE = "SENT_ONCE_ACKNOWLEDGED"
ACTIVATION_PACKET_SHA256 = (
    "436967cf6273e0947b3587229701627ed459840007e793c39d222ae33c39e01c"
)
X1_FREEZE = "pending_until_x2"

PRIOR_FROZEN = 3290
SOURCE_SEALED_NEGATIVES = 20871
SOURCE_EXTERNAL_NEGATIVES = 3
ACTIVATION_NEGATIVES = SOURCE_SEALED_NEGATIVES + SOURCE_EXTERNAL_NEGATIVES
ACTIVATION_MESSAGE_NEGATIVE_BASELINE = 20874
SOURCE_OPEN_GAPS = 137
SOURCE_EXACT_GATES = 136
SOURCE_SEALED_METHODS = 6505
SOURCE_EXTERNAL_METHODS = 3
ACTIVATION_METHODS = SOURCE_SEALED_METHODS + SOURCE_EXTERNAL_METHODS
ACTIVATION_MESSAGE_METHOD_BASELINE = 6508
SELECTED_INHERITED_COUNT = 20
NEW_UNIQUE_COUNT = 20
CURRENT_PORTFOLIO_COUNT = SELECTED_INHERITED_COUNT + NEW_UNIQUE_COUNT
LATEST_TRACKED_SCAN_CAP = 5000

PRIMARY_PILLAR = "Freed ID and CBR Heart"
PRACTICE_LENS = (
    "bounded synthetic natural-history taxidermy-mount documentation, accession "
    "quarantine, component and support topology, condition lineage, hazard hold, "
    "accessibility, correction, provenance, workload, and handover lens"
)

EXPECTED_DISTRIBUTION = {
    "completed": 14,
    "represented": 4,
    "open_gap": 1,
    "exact_gate": 1,
}
ALLOWED_OUTCOMES = set(EXPECTED_DISTRIBUTION)

PROTECTED_GATES = [
    "real_animals_human_remains_taxidermy_mounts_skins_pelts_feathers_bones_horns_antlers_tissues_labels_cases_supports_or_collection_records",
    "real_collectors_donors_source_communities_custodians_conservators_preparators_registrars_curators_workers_visitors_affected_parties_and_authorities",
    "real_accession_cataloguing_identification_sampling_pest_treatment_cleaning_repair_mounting_movement_display_deaccession_disposal_or_repatriation_action",
    "professional_taxidermy_natural_history_conservation_biosafety_chemical_safety_collection_care_pest_control_or_return_to_service_authority",
    "empirical_gmut_prediction_likelihood_parameter_constraint_observational_confirmation_physical_discovery_or_final_physics",
    "blind_matched_budget_thos_real_arms_governed_participants_operators_safety_monitoring_statistics_and_independent_review",
    "production_identity_live_keys_signatures_proofs_issuance_resolution_status_revocation_interoperability_recovery_and_trust",
    "specimen_identity_taxonomy_provenance_locality_sensitive_species_human_remains_sacred_material_traditional_knowledge_collective_interest_and_repatriation",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "legal_cultural_biosecurity_collection_title_custody_deaccession_disposal_repatriation_data_governance_and_maori_authority",
    "affected_party_notice_consent_contestation_correction_restriction_return_remedy_collective_governance_and_acceptance",
    "independent_team_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]

SELECTED_INHERITED_IDS = [f"V6608-P{i:03d}" for i in range(1, 21)]


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
        "taxidermy-dossier-identity",
        "Surrogate taxidermy-mount dossier identity capsule with specimen-class placeholder, accession quarantine, component scope, revision, source pin, and handling refusal",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic dossier and revision tokens, specimen-class placeholder, accession quarantine, component scope, source pin, correction, tombstone, and zero-real-specimen states",
        ["SPNHC-ACCESSION", "TDWG-DWC", "W3C-PROV", "JSON-SCHEMA-2020-12"],
    ),
    _proposal(
        "taxidermy-component-topology",
        "Taxidermy mount, base, armature, hide, appendage, detachable part, label, and enclosure topology with orphan, duplicate, concealed-state, and intervention quarantine",
        "completed",
        "Freed ID and CBR Heart",
        "typed synthetic mount, base, armature, skin, appendage, detachable-part, label and enclosure relations with orphan, duplicate, concealed, contradiction, and no-disassembly guards",
        ["NPS-DRY-SPECIMENS", "SPNHC-TAXIDERMY", "JSON-SCHEMA-2020-12"],
    ),
    _proposal(
        "taxidermy-support-state-ledger",
        "Taxidermy support-state ledger for base contact, restraint, centre-of-mass placeholder, tilt cue, load-path unknown, movement hold, and stability-claim refusal",
        "completed",
        "GMUT Mind and THOS Body",
        "synthetic support nodes, contact edges, restraint placeholders, centre-of-mass and tilt unknowns, load-path gaps, contradiction retention, movement hold, and stability-claim refusal",
        ["NPS-DRY-SPECIMENS", "BIPM-SI", "W3C-PROV"],
    ),
    _proposal(
        "taxidermy-condition-observation",
        "Taxidermy condition-observation vocabulary for dust, loss, split, detachment, fading, pest cue, residue suspicion, deformation, uncertainty, and diagnosis abstention",
        "completed",
        "THOS Body and CBR Heart",
        "synthetic condition tokens, observation time, location scope, confidence, uncertainty, contradiction, correction, hazard escalation, and diagnosis or treatment abstention",
        ["SPNHC-TAXIDERMY", "NPS-CONSERVE-O-GRAMS", "W3C-PROV"],
    ),
    _proposal(
        "taxidermy-label-transcription",
        "Taxidermy label transcription and normalization contract for line order, abbreviation, illegibility, supplied text, locality masking, source image absence, and interpretation refusal",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic label lines, exact and supplied text separation, abbreviation and illegibility flags, locality mask, source-image absence, round-trip digest, and interpretation refusal",
        ["TDWG-DWC", "W3C-PROV", "IETF-JCS", "NZ-PRIVACY"],
    ),
    _proposal(
        "taxidermy-claim-braid",
        "Taxidermy identification, preparation, provenance, condition, attribution, locality, source, contestation, supersession, and authority-abstention assertion braid",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic identification, preparation, provenance, condition and attribution assertions with source status, uncertainty, contradiction, retraction, correction, sensitive-locality mask, and authority abstention",
        ["TDWG-DWC", "SPNHC-ACCESSION", "W3C-PROV", "NZ-PRIVACY"],
    ),
    _proposal(
        "taxidermy-hazard-hold",
        "Taxidermy legacy-pesticide, residue, mould, pest, sharp support, unstable base, handling, isolation, referral, and no-clearance hazard-hold board",
        "completed",
        "THOS Body and CBR Heart",
        "synthetic hazard cues, unknown substance state, exposure and handling refusal, isolation, referral, stop token, correction, and zero testing or clearance claims",
        ["SPNHC-TAXIDERMY", "SPNHC-TAXIDERMY-DISPOSAL", "NPS-DRY-SPECIMENS"],
    ),
    _proposal(
        "taxidermy-correction-lineage",
        "Taxidermy identifier, component, condition, hazard, provenance, locality, correction, supersession, readback, and unresolved-ambiguity lineage",
        "completed",
        "THOS Body and Freed ID",
        "synthetic identifiers, component and condition claims, hazard and provenance placeholders, correction, supersession, readback, ambiguity hold, cancellation, and non-erasure",
        ["W3C-PROV", "IETF-JCS", "TDWG-DWC"],
    ),
    _proposal(
        "taxidermy-provenance-custody",
        "Synthetic taxidermy provenance and custody covenant with accession-status placeholder, acquisition-source hold, transfer chain, component association, privacy mask, and title refusal",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic accession and custody placeholders, transfer and component association, documentary source, disclosure mask, consent and rights holds, correction, and ownership or title refusal",
        ["SPNHC-ACCESSION", "SPNHC-NUMBERING", "W3C-PROV", "NZ-PRIVACY"],
    ),
    _proposal(
        "taxidermy-bitemporal-memory",
        "Bitemporal taxidermy identifier, component, condition, hazard, custody, disclosure, correction, retraction, tombstone, and non-erasure memory",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic assertion and record intervals, predecessor links, correction, retraction, supersession, tombstone, contradiction retention, disclosure expiry, and record-erasure refusal",
        ["W3C-PROV", "IETF-JCS", "JSON-SCHEMA-2020-12"],
    ),
    _proposal(
        "taxidermy-measurement-uncertainty",
        "Taxidermy mount dimension, orientation, support-angle, mass placeholder, SI unit, resolution, covariance, missingness, and zero-measurement uncertainty envelope",
        "completed",
        "GMUT Mind",
        "typed synthetic dimension, angle and mass placeholders, SI units, resolution, covariance, uncertainty, missingness, calibration hold, zero observations, and fitness firewall",
        ["BIPM-SI", "W3C-PROV", "JSON-SCHEMA-2020-12"],
    ),
    _proposal(
        "gmut-taxidermy-support-graph-obligations",
        "GMUT typed support graph, load path, boundary condition, unit, covariance, conservation residual, stability, identifiability, and observation-firewall obligation board",
        "completed",
        "GMUT Mind",
        "typed symbolic support nodes, load-path and boundary placeholders, units, covariance, conservation-residual and stability obligations, identifiability limits, counterexample slots, and zero physical observations",
        ["BIPM-SI", "W3C-PROV", "IETF-JCS"],
    ),
    _proposal(
        "taxidermy-action-authorization-firewall",
        "Taxidermy handling, sampling, cleaning, pest treatment, repair, movement, display, deaccession, disposal, publication, and repatriation action-authorization firewall",
        "completed",
        "CBR Heart and THOS Body",
        "synthetic action request, object and hazard scope, custodian, conservator, registrar, legal, cultural, affected-party and Māori-authority holds, stop token, and execution refusal",
        ["SPNHC-TAXIDERMY", "SPNHC-ACCESSION", "NMAI-CONSERVATION", "TE-MANA-RARAUNGA"],
    ),
    _proposal(
        "stage20-taxidermy-evidence-board",
        "Stage 20 taxidermy dependency cut-set and noncompensating specimen, participant, authority, infrastructure, and independent-team deficit lattice",
        "completed",
        "All pillars",
        "typed synthetic evidence nodes, dependency cut sets, specimen, participant, authority, infrastructure and independent-team deficit classes, noncompensation rules, retained negatives, and fail-closed terminal abstention",
        ["W3C-PROV", "IETF-JCS", "JSON-SCHEMA-2020-12"],
    ),
    _proposal(
        "gmut-taxidermy-hygromechanical-proxy",
        "GMUT taxidermy support, skin-shell, moisture-response, interface, damping, boundary, covariance, stability, and identifiability proxy with zero specimen observations",
        "represented",
        "GMUT Mind",
        "typed symbolic support and shell placeholders, moisture-response and interface terms, damping, boundaries, covariance, zero fitted coefficients, zero likelihood rows, and physical-inference abstention",
        ["BIPM-SI", "NPS-DRY-SPECIMENS", "W3C-PROV"],
    ),
    _proposal(
        "thos-taxidermy-handover",
        "THOS bounded taxidermy documentation handoff with hazard debt, unresolved component and claim budgets, stop conditions, readback, acceptance digest, and workload refusal",
        "represented",
        "THOS Body",
        "synthetic documentation queues, hazard and ambiguity debt, workload ceilings, stop tokens, correction readback, escalation, acceptance digest, handover, and zero conservators or operators",
        ["SPNHC-TAXIDERMY", "WCAG22", "W3C-PROV"],
    ),
    _proposal(
        "taxidermy-matched-budget-protocol",
        "Counterbalanced empty-session protocol comparing topology-first and sequential-record-first synthetic taxidermy explanations",
        "represented",
        "THOS Body",
        "future blind matched-budget synthetic dossiers, shuffled tasks, equal action budgets, masked scoring, safety and withdrawal rules, zero participants, and no comprehension or effectiveness claim",
        ["WCAG22", "TDWG-DWC", "W3C-PROV"],
    ),
    _proposal(
        "taxidermy-access-companion",
        "Sensitive-content-prefaced taxidermy relation export with adjacency breadcrumbs, focus-return checkpoints, downloadable plain text, and reserved affected-user evaluation",
        "represented",
        "CBR Heart and THOS Body",
        "sensitive-content preface, structural headings, component and condition adjacency breadcrumbs, focus-return checkpoints, downloadable plain text, noncolour status, language reservations, and zero affected-user sessions",
        ["WCAG22", "TDWG-DWC", "W3C-PROV"],
    ),
    _proposal(
        "gbif-taxidermy-zero-row-adapter",
        "GBIF preserved-specimen occurrence adapter with basis-of-record, institution and collection, taxonomy, locality masking, issue flags, pagination, checksum, covariance, likelihood, and zero-row refusal",
        "open_gap",
        "GMUT Mind and Freed ID",
        "zero API calls, downloads, authenticated records, preserved-specimen rows, taxonomy decisions, locality disclosures, calibrated measurements, likelihood evaluations, posterior samples, or empirical claims",
        ["GBIF-OCCURRENCE-API", "TDWG-DWC", "GBIF-DATA-QUALITY", "NZ-PRIVACY"],
    ),
    _proposal(
        "taxidermy-rights-authority",
        "Unoccupied authority circuit for specimen title, acquisition, custody, sensitive locality, sacred or taonga possibility, access, sampling, display, deaccession, disposal, return, repatriation, remedy, and Māori decision non-substitution",
        "exact_gate",
        "CBR Heart",
        "unoccupied donor, source community, custodian, conservator, registrar, curator, legal, cultural, privacy, traditional-knowledge, collective-interest, tangata whenua, iwi, hapū, affected-party, remedy, return, repatriation, and Māori-authority reservations",
        ["SPNHC-ACCESSION", "NMAI-CONSERVATION", "NZ-PRIVACY", "TE-MANA-RARAUNGA"],
    ),
]

SELF_SAFE_CATEGORIES = [
    "Auren source head and fresh equality",
    "activation packet and external receipt digests",
    "three-thousand-two-hundred-ninety-row proposal-chain parse",
    "twenty inherited selection identities",
    "twenty-title novelty screen",
    "mechanism-level taxidermy-neighbor review",
    "new-outcome distribution",
    "workflow-plan policy",
    "identity and relational-language boundary",
    "Hamish-authorized Auren-to-Sable live edge",
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
    {"task_id": f"V6611-SAFE-{i:03d}", "title": f"Validate {name} inside the Sable-owned v661-v1 lane", "owner": OWNER}
    for i, name in enumerate(SELF_SAFE_CATEGORIES, 1)
]
SUCCESSOR_SAFE_SEEDS = [
    {"task_id": f"V6612-REC-SAFE-{i:03d}", "title": f"Reassess {name} for Caelen-only v661-v2", "recipient": "Caelen Ash", "completion_credit": 0}
    for i, name in enumerate(SELF_SAFE_CATEGORIES[:20], 1)
]

SELF_CANDIDATE_CATEGORIES = [
    "synthetic taxidermy-dossier identity ledger",
    "component, support, and enclosure topology tribunal",
    "condition-observation and diagnosis-abstention vocabulary",
    "label transcription and locality-minimisation contract",
    "provenance, claim, contestation, and correction braid",
    "legacy-hazard cue and no-clearance board",
    "bitemporal custody and disclosure memory",
    "GMUT support-graph obligation board",
    "GBIF preserved-specimen zero-row adapter",
    "taxidermy rights, return, repatriation, and Māori-authority circuit",
]
SELF_CANDIDATE_TASKS = [
    {"task_id": f"V6611-CAND-{i:03d}", "title": f"Build and test reversible {name}", "owner": OWNER}
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]
SUCCESSOR_CANDIDATE_SEEDS = [
    {"task_id": f"V6612-REC-CAND-{i:03d}", "title": f"Consider a distinct Caelen-owned refinement of {name}", "recipient": "Caelen Ash", "completion_credit": 0}
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]

EXACT_QUEUE = [
    {"task_id": f"V6611-EXACT-{i:03d}", "title": title, "state": "exact_gate_unexecuted"}
    for i, title in enumerate(
        [
            "Handle, sample, clean, treat, repair, move, mount, display, deaccession, dispose of, return, repatriate, or publish any real specimen, mount, component, label, image, record, or restricted information",
            "Make a real taxonomic identification, condition diagnosis, hazard clearance, treatment, pest-control, stability, storage, display, transport, or fitness determination",
            "Use real animals, remains, specimens, donors, source communities, workers, visitors, custodians, conservators, preparators, registrars, curators, collections, or personal information",
            "Disclose private identity, locality, endangered-species, donor, source-community, sacred-material, traditional-knowledge, dispute, or restricted collection information",
            "Make a professional conservation, taxidermy, biosafety, chemical-safety, collection-care, privacy, security, translation, or accessibility determination",
            "Publish a production identifier, accession, catalog record, provenance claim, credential, signature, proof, status, interoperability result, or collection record",
            "Allocate title, ownership, custody, authorship, attribution, access, sampling, deaccession, disposal, return, repatriation, remedy, or beneficiary authority",
            "Make a tikanga, mātauranga, wording, naming, tangata whenua, iwi, hapū, Māori data-governance, cultural-protocol, taonga-status, or Māori-authority decision",
            "Run a real participant study, collection trial, treatment trial, professional review, public access trial, or independent reproduction",
            "Perform destructive cleanup or any mutation outside the exact Sable-owned lane",
        ],
        1,
    )
]
BLOCKED_QUEUE = [
    {"task_id": f"V6611-BLOCK-{i:03d}", "title": title, "state": "blocked_unexecuted"}
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
    ("ghc-family-taxidermy-dossier-identity", "Validate bounded synthetic dossier identity, accession quarantine, source pin, revision, tombstone, and real-specimen refusal."),
    ("ghc-family-taxidermy-component-topology", "Check synthetic mount, base, armature, skin, appendage, label, enclosure, orphan, duplicate, and disassembly-refusal relations."),
    ("ghc-family-taxidermy-support-state", "Preserve synthetic support contacts, restraint, load-path unknowns, movement holds, and stability-claim refusal."),
    ("ghc-family-taxidermy-condition-observation", "Represent bounded condition observations with uncertainty, contradiction, correction, hazard escalation, and diagnosis abstention."),
    ("ghc-family-taxidermy-label-transcription", "Separate exact and supplied synthetic label text while preserving illegibility, locality masking, provenance, and interpretation refusal."),
    ("ghc-family-taxidermy-claim-braid", "Retain identification, provenance, condition, source, contestation, correction, supersession, and authority abstention."),
    ("ghc-family-taxidermy-hazard-hold", "Expose synthetic legacy-residue, mould, pest, sharp-support, unstable-base, isolation, referral, and no-clearance states."),
    ("ghc-family-taxidermy-correction-lineage", "Preserve identifiers, component and condition claims, hazards, corrections, supersession, readback, ambiguity, and non-erasure."),
    ("ghc-family-gmut-taxidermy-support-graph", "Preserve typed support, boundary, unit, covariance, conservation, stability, identifiability, and observation-firewall obligations."),
    ("ghc-family-taxidermy-rights-authority", "Keep title, custody, locality, access, sampling, return, repatriation, remedy, cultural, and Māori decision rights unoccupied."),
]
SUCCESSOR_SKILL_SEEDS = [
    {"name": name.replace("taxidermy", "successor-domain"), "recipient": "Caelen Ash", "state": "recommendation_only", "completion_credit": 0}
    for name, _ in SELF_SKILL_SPECS
]
SELF_RUNNER_SPECS = [
    (name.replace("ghc-family-", "ghc_family_").replace("-", "_") + ".py", purpose)
    for name, purpose in SELF_SKILL_SPECS
]
SUCCESSOR_RUNNER_SEEDS = [
    {"name": name.replace("taxidermy", "successor_domain"), "recipient": "Caelen Ash", "state": "recommendation_only", "completion_credit": 0}
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
    "keep real specimen, participant, and connector rows empty",
    "retain scanner candidates separately from confirmed payload hits",
    "scan only declared public owner surfaces across five classes",
    "refresh owner manifests after every additive lifecycle change",
    "verify deterministic JSON ordering and parsing",
    "verify proposal append-only arithmetic",
    "verify inherited revalidation receives zero novelty and completion credit",
    "verify outcome labels use only the four authorized states",
    "reserve manual and affected-user accessibility evaluation",
    "reserve legal, cultural, religious, biological-collection, and Māori authority",
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
    {"task_id": f"V6611-CLEAN-{i:03d}", "title": title, "owner": OWNER, "mode": "additive_review_only"}
    for i, title in enumerate(SELF_CLEAN_CATEGORIES, 1)
]
SUCCESSOR_CLEAN_SEEDS = [
    {"task_id": f"V6612-REC-CLEAN-{i:03d}", "title": title, "recipient": "Caelen Ash", "completion_credit": 0}
    for i, title in enumerate(SELF_CLEAN_CATEGORIES, 1)
]

OFFICIAL_SOURCES = [
    ("SPNHC-TAXIDERMY", "primary_professional_society", "https://spnhc.org/taxidermy-and-skins/", "Current SPNHC care, preservation, storage, pest, disaster, and health-and-safety resource vocabulary only; no professional interpretation, treatment, handling, clearance, or endorsement."),
    ("SPNHC-TAXIDERMY-DISPOSAL", "primary_professional_society", "https://spnhc.org/spnhc-statement-on-taxidermy-disposal/", "SPNHC risk, care, preservation, and expert-referral context only; no hazard clearance, disposal decision, legal conclusion, or institutional authority."),
    ("SPNHC-ACCESSION", "primary_professional_society", "https://spnhc.org/accession-of-specimens/", "Accession, provenance, documentation, title-dependency, permit, and competent-signature vocabulary only; no accession, title, ownership, permit, or legal decision."),
    ("SPNHC-NUMBERING", "primary_professional_society", "https://spnhc.org/numbering-natural-history-collections/", "Catalog, accession, component association, legacy number, and persistent-identifier vocabulary only; no live cataloguing or identity authority."),
    ("NPS-DRY-SPECIMENS", "official_us_nps", "https://www.nps.gov/museum/publications/conserveogram/11-09.pdf", "Dry bird and mammal specimen handling, support, storage, and damage-observation requirements only; no real handling, storage release, treatment, or professional decision."),
    ("NPS-CONSERVE-O-GRAMS", "official_us_nps", "https://www.nps.gov/subjects/museums/conserve-o-grams.htm", "Current official collections-care topic and revision-status vocabulary only; no treatment instruction is executed."),
    ("NPS-MUSEUM-HANDBOOK", "official_us_nps", "https://www.nps.gov/subjects/museums/mh1.htm", "Museum-collection preservation, documentation, biological-collection care, hazard, and referral context only; no institutional or professional authority."),
    ("NMAI-CONSERVATION", "official_smithsonian", "https://americanindian.si.edu/explore/collections/conservation", "Collaborative conservation and constituency-partnership context only; no substitution for Indigenous, affected-party, cultural, or Māori authority."),
    ("TDWG-DWC", "primary_biodiversity_standard", "https://dwc.tdwg.org/terms/", "Current Darwin Core preserved-specimen, collection, identifier, information-withheld, data-generalization, measurement, and relationship vocabulary only."),
    ("GBIF-OCCURRENCE-API", "official_gbif", "https://techdocs.gbif.org/en/openapi/v1/occurrence", "Current occurrence search, pagination, download, citation, basis-of-record, and API-limit requirements only; zero requests and zero rows."),
    ("GBIF-DATA-QUALITY", "official_gbif", "https://techdocs.gbif.org/en/data-use/occurrence-issues-and-flags", "Current issue-flag and interpretation-warning vocabulary only; no record-quality, taxonomic, locality, or fitness conclusion."),
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
    "SPNHC-TAXIDERMY": "current_resource_checked_2026_08_04",
    "SPNHC-TAXIDERMY-DISPOSAL": "published_2023_checked_2026_08_04",
    "SPNHC-ACCESSION": "current_resource_checked_2026_08_04",
    "SPNHC-NUMBERING": "current_resource_checked_2026_08_04",
    "NPS-DRY-SPECIMENS": "conserve_o_gram_11_9_checked_2026_08_04",
    "NPS-CONSERVE-O-GRAMS": "current_index_updated_2026_checked_2026_08_04",
    "NPS-MUSEUM-HANDBOOK": "official_part_i_checked_2026_08_04",
    "NMAI-CONSERVATION": "official_current_page_checked_2026_08_04",
    "TDWG-DWC": "current_recommended_terms_checked_2026_08_04",
    "GBIF-OCCURRENCE-API": "current_openapi_v1_checked_2026_08_04",
    "GBIF-DATA-QUALITY": "current_technical_guidance_checked_2026_08_04",
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
    _startup_failure("V6611-X1-N001", "broad-memory-registry-search-truncated-before-attributable-current-route-results", "Retain the truncated search at zero credit and use narrow current-route and prior-Sable line windows only."),
    _startup_failure("V6611-X1-N002", "first-activation-line-count-probe-undercounted-the-mixed-line-projection", "Retain the undercount at zero credit and read the immutable Git blob through deterministic fixed line windows to the exact EOF."),
    _startup_failure("V6611-X1-N003", "oversized-activation-remainder-projection-truncated-before-eof", "Retain the truncated projection at zero credit and use materialized fifty-five-line Git-blob windows through line 1080."),
    _startup_failure("V6611-X1-N004", "default-console-encoding-corrupted-maori-text-in-a-read-only-skill-display", "Retain the display corruption at zero credit, persist none of it, pin UTF-8, and reread the exact skill and references."),
    _startup_failure("V6611-X1-N005", "first-git-ls-tree-size-filter-omitted-the-path-separator-and-returned-no-rows", "Retain the empty projection at zero credit and use the exact revision followed by a literal path separator."),
    _startup_failure("V6611-X1-N006", "canonical-receipt-hash-content-search-returned-no-match-because-the-receipt-does-not-self-embed-its-digest", "Retain the empty search at zero credit and resolve the exact receipt by bounded filename inventory plus independent file hashing."),
    _startup_failure("V6611-X1-N007", "combined-post-checkout-status-and-agent-inventory-projection-overran-before-attributable-output", "Retain the combined wrapper at zero credit and recover with separate scalar head, branch, cleanliness, and tracked-agent probes."),
    _startup_failure("V6611-X1-N008", "broad-binding-keyword-novelty-sweep-overmatched-cryptographic-holder-binding-titles", "Retain the noisy semantic method at zero credit and use domain-specific natural-history and taxidermy terms with readable collision reasons."),
    _startup_failure("V6611-X1-N009", "broad-domain-sweep-hit-a-cp1252-unicode-output-failure-after-partial-results", "Retain the partial projection at zero credit, persist none of it, and rerun the isolated title audit under forced UTF-8."),
    _startup_failure("V6611-X1-N010", "temporary-file-activation-digest-wrapper-was-policy-rejected-before-execution", "Retain the rejected method at zero credit and hash the immutable Git blob entirely in memory without creating or deleting a temporary path."),
    _startup_failure("V6611-X1-N011", "first-isolated-novelty-invocation-guessed-an-unsupported-json-switch-and-omitted-the-required-index", "Retain the argument rejection at zero credit, inspect the exact probe interface, and bind the frozen index positionally."),
    _startup_failure("V6611-X1-N012", "second-isolated-novelty-invocation-supplied-the-index-but-omitted-the-standard-input-title-array", "Retain the empty-input JSON failure at zero credit and bind both the immutable index and the twenty UTF-8 titles explicitly."),
    _startup_failure("V6611-X1-N013", "first-complete-title-screen-refused-the-generic-stage20-and-accessibility-titles-at-the-declared-threshold", "Retain the eighteen-of-twenty witness at zero credit, preserve the threshold, and replace those mechanisms with a dependency cut-set deficit lattice and sensitive-content relation export."),
    _startup_failure("V6611-X1-N014", "intentional-invalid-workflow-fixture-was-rejected-on-the-messaging-boundary", "Retain the rejecting witness at zero credit, leave its issue packet visible, and validate the separately corrected request without changing the authorized route."),
    _startup_failure("V6611-X1-N015", "first-current-x1-suite-passed-twenty-one-of-twenty-three-and-found-two-missing-skill-generated-receipt-families", "Retain the failed aggregate at zero credit, materialize only the declared workflow, governance, index, reflection, Method Flow, and meta-tool receipts, refresh manifests, and rerun the scoped x1 suite once."),
    _startup_failure("V6611-X1-N016", "bounded-source-tree-inventory-pipeline-returned-exit-one-after-emitting-the-requested-current-file-list", "Retain the nonzero wrapper at zero credit and use exact tracked filenames and scalar file reads for subsequent template inspection."),
    _startup_failure("V6611-X1-N017", "combined-prestage-allowlist-json-privacy-and-diff-wrapper-output-truncated-before-attributable-result", "Retain the truncated wrapper at zero credit; split allowlist parity, JSON parsing, privacy and x2-absence review, owner-file counting, and diff hygiene into scalar probes."),
]

# X2 failures may be appended only after the immutable x1 commit is pushed and
# proved clean and four-way equal.
PREFILLED_X1_X2_FAILURES_IGNORED: tuple[dict[str, object], ...] = tuple()
X2_FAILURES: list[dict[str, object]] = []
