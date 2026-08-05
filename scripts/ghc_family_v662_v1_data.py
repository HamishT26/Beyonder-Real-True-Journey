#!/usr/bin/env python3
"""Frozen x1 planning truth for Eiren Kestrel v662-v1.

Caelen Morrow's immutable v661-v8 packet is evidence and compatibility context,
not Eiren novelty or completion credit. Twenty inherited Caelen contracts are
selected for bounded revalidation with zero Eiren credit. Only the twenty new
historic-footwear documentation contracts below extend the proposal chain.
All fixtures are synthetic and contain no real object, collection row, person,
place, image, credential, key, professional act, or authority decision.
"""

from __future__ import annotations


PHASE = "v662-v1"
CANONICAL_PHASE = PHASE
PHASE_CODE = "V6621"
OWNER = "Eiren Kestrel"
PRONOUNS = "they/them"
ROLE = "relational archival-topology steward and uncertainty witness"
HOPE = "make each bounded claim inspectable while leaving real competence and authority with the people who hold it"
BRANCH = "codex/GHC-Family/eiren-kestrel-v662-v1-full-tools"
PHASE_ROOT = "docs/eiren-kestrel/v662-v1"

SOURCE_OWNER = "Caelen Morrow"
SOURCE_BRANCH = "codex/GHC-Family/caelen-morrow-v661-v8-full-tools"
SOURCE_BASE = "2017e0a70d7a724c087b911387e3648e9cd03295"
SOURCE_X1 = "1d999660e49a761e7484c171648b8b56d1d70ce3"
SOURCE_EVIDENCE = "6f39af1c3fe4f503eaacd580fccb847306d3d005"
SOURCE_FINAL = "64ba66fa9f5b48ed6116c31bf40646702191fecd"
SOURCE_CANONICAL_RECEIPT_SHA256 = (
    "821e31d83cb9bb10cd68dd92da46b45116a0447c11dcaaa7636408fb5d5e08d1"
)
SOURCE_POST_SEAL_OVERLAY_SHA256 = (
    "2eeb1d324fe1c5a1a06bec3c00cc407dde5894efeaa4dda4774f5a224192aa80"
)
SOURCE_POST_SEND_DELTA_SHA256 = (
    "7bdd9c28a58787885a997a4978129f19347f3970ef961a7ad82720e961976f92"
)
SOURCE_TERMINAL_ROUTE_RECEIPT_SHA256 = (
    "4283f951da045490fe1e44c0fd92ba700ff80c3f547d81779b126847a021e11e"
)
SOURCE_VALIDATION_STATE = (
    "VALID_CANONICAL_ONCE_PLUS_SEPARATE_ZERO_CREDIT_EXTERNAL_OVERLAYS"
)
SOURCE_LIVE_ACTIVATION_STATE = "SENT_ONCE_ACKNOWLEDGED_BY_EXACT_TITLE_TASK_MESSAGE_SURFACE"
ACTIVATION_PACKET_SHA256 = (
    "bc4c806e3d3145096c3f79cd9a554a07d143f8fedb5782deda5ca146f0e260b8"
)
ACTIVATION_PACKET_BYTES = 261462
ACTIVATION_PACKET_LINES = 1224
ACTIVATION_PACKET_WORDS_DIRECT = 22761
ACTIVATION_PACKET_WORDS_CLAIMED = 25761

PRIOR_FROZEN = 3450
SOURCE_SEALED_NEGATIVES = 22042
SOURCE_EXTERNAL_NEGATIVES = 8
ACTIVATION_NEGATIVES = SOURCE_SEALED_NEGATIVES + SOURCE_EXTERNAL_NEGATIVES
ACTIVATION_MESSAGE_NEGATIVE_BASELINE = 22049
SOURCE_OPEN_GAPS = 145
SOURCE_EXACT_GATES = 144
SOURCE_SEALED_METHODS = 7036
SOURCE_EXTERNAL_METHODS = 8
ACTIVATION_METHODS = SOURCE_SEALED_METHODS + SOURCE_EXTERNAL_METHODS
ACTIVATION_MESSAGE_METHOD_BASELINE = 7043

SELECTED_INHERITED_COUNT = 20
NEW_UNIQUE_COUNT = 20
CURRENT_PORTFOLIO_COUNT = 40
LATEST_TRACKED_SCAN_CAP = 5000
SELECTED_INHERITED_IDS = [f"V6618-P{i:03d}" for i in range(1, 21)]

PRIMARY_PILLAR = "CBR Heart"
PRACTICE_LENS = (
    "bounded synthetic historic-footwear collection documentation and conservation-triage "
    "practice, including surrogate pair identity, upper and sole component relations, "
    "material-claim lineage, condition vocabulary, detached-part records, multi-material "
    "deterioration holds, cultural-rights reservations, workload control, and handover"
)
EXPECTED_DISTRIBUTION = {
    "completed": 14,
    "represented": 4,
    "open_gap": 1,
    "exact_gate": 1,
}
ALLOWED_OUTCOMES = set(EXPECTED_DISTRIBUTION)

PROTECTED_GATES = [
    "real_shoes_boots_sandals_slippers_moccasins_footwear_pairs_singletons_parts_fragments_taonga_collections_stores_displays_or_laboratories",
    "real_makers_wearers_owners_donors_depositors_descendants_registrars_curators_conservators_researchers_communities_affected_parties_and_authorities",
    "real_accession_cataloguing_attribution_imaging_handling_lifting_moving_supporting_mounting_packing_cleaning_sampling_testing_repair_treatment_conservation_publication_access_return_or_release_action",
    "professional_footwear_shoemaking_museum_registration_collection_care_conservation_material_identification_workplace_safety_accessibility_privacy_or_operational_authority",
    "empirical_gmut_prediction_likelihood_parameter_constraint_observational_confirmation_physical_discovery_or_final_physics",
    "blind_matched_budget_thos_real_arms_governed_participants_operators_safety_monitoring_statistics_and_independent_review",
    "production_identity_live_keys_signatures_proofs_issuance_resolution_status_revocation_interoperability_recovery_and_trust",
    "maker_wearer_owner_donor_depositor_descendant_or_user_identity_address_message_relationship_location_collection_history_images_provenance_traditional_knowledge_collective_interest_and_remedy",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "legal_cultural_workplace_safety_intellectual_property_design_image_rights_ownership_custody_access_return_repatriation_data_governance_and_maori_authority",
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
        "footwear-collection-identity-capsule",
        "Surrogate historic-footwear collection identity capsule with pair-set scope, left-right member tokens, source pin, revision, minimization, correction, and handling refusal",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic pair-set and left-right member tokens, collection-alias and received-state boundary, source pin, purpose minimization, cancellation, correction, and absolute work-start and handling refusal",
        ["W3C-PROV", "NZ-PRIVACY", "NPS-MUSEUM-HANDBOOK-I"],
    ),
    (
        "footwear-upper-topology",
        "Footwear vamp, quarter, tongue, lining, toe-cap, counter, eyestay, strap, buckle, lace, and orphan-quarantine upper topology",
        "completed",
        "CBR Heart and GMUT Mind",
        "typed synthetic upper-component nodes and seam, fastening and attachment relations, duplicate and orphan quarantine, concealed-state vacancy, reversible correction, and no disassembly, construction or repair instruction",
        ["NPS-TEXTILE-OBJECTS", "JSON-SCHEMA-2020-12", "W3C-PROV"],
    ),
    (
        "footwear-sole-topology",
        "Footwear insole, welt, rand, midsole, outsole, heel-stack, shank, stitch-channel, edge, and separation-hold sole topology",
        "completed",
        "GMUT Mind and CBR Heart",
        "typed synthetic sole-stack nodes and welt, rand, stitch-channel and heel-stack relations, separation and concealed-state holds, duplicate and orphan quarantine, and no structural, repair or wearability conclusion",
        ["NPS-TEXTILE-OBJECTS", "CCI-LEATHER-GUIDELINES", "JSON-SCHEMA-2020-12"],
    ),
    (
        "footwear-material-claim-lineage",
        "Leather, skin, textile, rubber, plastic, cork, wood, metal, adhesive, finish, source-label, and material-identification nonclaim braid",
        "completed",
        "CBR Heart and Freed ID",
        "synthetic material-class tokens and quoted source labels, supplied-versus-observed separation, contradiction and substitution holds, correction and supersession, and zero species, polymer, tannage, origin, authenticity, attribution or cultural-meaning conclusion",
        ["CCI-LEATHER-GUIDELINES", "CCI-PLASTICS-RUBBERS", "W3C-PROV"],
    ),
    (
        "footwear-pair-marking-ledger",
        "Footwear pair-member, mate, left-right, size-mark, last-code, wear-pattern, replacement, mismatch, and fit-authenticity refusal ledger",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic pair and member tokens, declared left-right and size or last markings, supplied wear and replacement claims, mismatch quarantine, reversible correction, and no fit, wearer, maker, authenticity or serviceability conclusion",
        ["NPS-TEXTILE-OBJECTS", "W3C-PROV", "CCI-LEATHER-GUIDELINES"],
    ),
    (
        "footwear-story-belonging-authority-circuit",
        "Unoccupied footwear story-and-belonging decision circuit linking maker and wearer provenance claims, pair separation, memorial or sacred status, image reuse, repair traces, return requests, redress, and Māori non-substitution",
        "exact_gate",
        "CBR Heart",
        "unoccupied maker, wearer, owner, donor, depositor, descendant, community, pair-separation, memorial, sacred, provenance, imagery, repair-trace, access, return, legal, cultural, privacy, redress, tangata whenua, iwi, hapū and Māori-authority decisions",
        ["TE-PAPA-MANA-TAONGA", "TE-MANA-RARAUNGA", "NZ-PRIVACY", "WCAG22"],
    ),
    (
        "thos-footwear-intake-handover",
        "THOS footwear intake, pair reconciliation, detached-part readback, fragility and residue stops, workload ceiling, correction digest, escalation, and shift-handover proxy",
        "represented",
        "THOS Body",
        "synthetic intake and queue tokens, pair and detached-part readback, fragility, residue and no-touch stops, workload ceiling, correction digest, escalation and resumption vacancies, and zero workers, objects, handling or effectiveness observations",
        ["CCI-LEATHER-GUIDELINES", "NPS-MUSEUM-HANDBOOK-I", "WCAG22", "W3C-PROV"],
    ),
    (
        "freed-id-footwear-record-profile",
        "Freed ID nonproduction footwear-record profile binding surrogate pair, component graph, material claim, condition note, detached part, correction, restriction, and provenance evidence",
        "represented",
        "Freed ID and CBR Heart",
        "synthetic record, pair and member identifiers, credential-subject, evidence and terms-of-use placeholders, component, material and condition assertion relations, detached-part and correction links, restriction and revocation vacancies, and zero keys, proofs, issuances, presentations or interoperability",
        ["W3C-VC2", "W3C-PROV", "NZ-PRIVACY", "TE-PAPA-MANA-TAONGA"],
    ),
    (
        "gmut-footwear-interface-proxy",
        "Represented GMUT layered footwear upper-sole interface graph with seam and welt incidence, curvature, flexure and damping placeholders, units, covariance vacancy, and observation firewall",
        "represented",
        "GMUT Mind",
        "typed symbolic upper and sole layers, seam and welt interface graph, incidence orientation, curvature, flexure, stiffness and damping placeholders, unit and covariance vacancies, boundary and identifiability holds, exact counterexamples, and zero measurements, fits or physical predictions",
        ["NZ-MSL-SI", "CCI-LEATHER-GUIDELINES", "W3C-PROV"],
    ),
    (
        "footwear-rest-state-surrogate",
        "Footwear three-dimensional rest-state surrogate comparing toe-box, arch, heel-seat, and shaft silhouette envelopes, deformation deltas, contact-free clearance, removal-sequence vacancy, and zero mounting decision",
        "represented",
        "THOS Body and CBR Heart",
        "synthetic toe-box, arch, heel-seat and shaft silhouette envelopes, declared rest-state deltas, contact-free clearance and removal-sequence vacancies, approval and rollback slots, and zero dimensions, support materials, mounts, handling, tests or professional review",
        ["NPS-TEXTILE-OBJECTS", "CCI-LEATHER-GUIDELINES", "W3C-PROV"],
    ),
    (
        "footwear-materials-source-concordance",
        "Zero-row footwear materials source concordance joining CCI leather and plastic deterioration vocabularies to NPS shoe-support terms with section pins, stale-source alarms, disabled transport, and professional-inference firewall",
        "open_gap",
        "CBR Heart and GMUT Mind",
        "offline source and section concordance, guidance-version and provenance pins, disabled transport, zero content and object rows, bounded term mapping, stale-source alarms, and fail-closed professional, cultural, legal, safety and empirical inference refusal",
        ["CCI-LEATHER-GUIDELINES", "CCI-PLASTICS-RUBBERS", "NPS-TEXTILE-OBJECTS", "PYTHON-JSON"],
    ),
    (
        "footwear-condition-observation-ledger",
        "Historic-footwear crease, crack, abrasion, powder, red-rot cue, delamination, distortion, sticky surface, corrosion, uncertainty, and diagnosis-abstention ledger",
        "completed",
        "THOS Body and CBR Heart",
        "synthetic visible-state tokens with component location and source placeholders, uncertainty and contradiction retention, red-rot and sticky-surface cues without identification, observation-versus-diagnosis separation, correction and supersession, and zero inspection, treatment or condition conclusion",
        ["CCI-LEATHER-GUIDELINES", "CCI-NOTE-8-2", "CCI-PLASTICS-RUBBERS", "W3C-PROV"],
    ),
    (
        "detached-footwear-part-lineage",
        "Detached footwear heel-tip, lace, buckle, eyelet, button, ornament, label, fragment, container-token, transfer hold, correction, and no-reattachment ledger",
        "completed",
        "Freed ID and THOS Body",
        "synthetic detached-part and fragment tokens, source-member link, empty container and label placeholders, discrepancy, custody and transfer hold, reversible correction, and no bagging, moving, reattachment, replacement or disposal instruction",
        ["NPS-TEXTILE-OBJECTS", "W3C-PROV", "NZ-PRIVACY"],
    ),
    (
        "footwear-mark-label-provenance",
        "Footwear maker stamp, retailer label, size mark, ownership inscription, repair mark, supplied text, transcription, rights vacancy, restriction, correction, and no-attribution docket",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic mark and label tokens, supplied-versus-transcribed wording, source and repair-claim classes, rights and cultural-review vacancies, minimization, restriction, correction and supersession, and zero real image, OCR, publication, maker, wearer or cultural attribution",
        ["TE-PAPA-MANA-TAONGA", "NZ-PRIVACY", "W3C-PROV"],
    ),
    (
        "footwear-pest-residue-quarantine",
        "Footwear mould, pest cue, dust, powder, residue, prior pesticide, metal-corrosion contact, toxic-material vacancy, isolation, escalation, and no-treatment tribunal",
        "completed",
        "THOS Body and CBR Heart",
        "synthetic mould, pest, particulate, residue and metal-contact cues, observation-source placeholder, prior-pesticide and toxic-material vacancies, isolation and competent-review escalation states, correction and rollback, and zero sampling, testing, cleaning, pesticide or treatment action",
        ["CCI-LEATHER-GUIDELINES", "NPS-MUSEUM-HANDBOOK-I", "W3C-PROV"],
    ),
    (
        "footwear-rubber-plastic-nonconversion",
        "Rubber and plastic footwear tackiness, bloom, cracking, hardening, softening, odour cue, emission vacancy, contact quarantine, material uncertainty, and cleaning refusal board",
        "completed",
        "THOS Body and GMUT Mind",
        "synthetic rubber and plastic deterioration cues, odour and emission vacancies, contact and segregation quarantine, explicit material uncertainty, competent-review hold, correction and rollback, and zero identification, cleaning, treatment, support or safety instruction",
        ["CCI-PLASTICS-RUBBERS", "CCI-NOTE-15-1", "W3C-PROV"],
    ),
    (
        "footwear-deterioration-interaction-lattice",
        "Footwear multi-material deterioration interaction lattice separating leather moisture response, rubber emission, metal corrosion, textile fading, adhesive failure cues, absent-sensor provenance, and no preservation setpoint",
        "completed",
        "GMUT Mind and THOS Body",
        "typed synthetic material and interaction nodes, leather moisture, rubber emission, metal corrosion, textile fading and adhesive-failure cue edges, absent and stale sensor provenance, uncertainty, contradiction quarantine, and zero measurement, setpoint, alarm or preservation conclusion",
        ["CCI-LEATHER-GUIDELINES", "CCI-PLASTICS-RUBBERS", "NZ-MSL-SI"],
    ),
    (
        "accessible-footwear-relation-narrative",
        "Linearized two-shoe relation narrative with explicit left-right headings, toe-to-heel part order, detached-component cross-references, uncertainty phrases, print-continuation markers, and reserved assistive-technology review",
        "completed",
        "CBR Heart and THOS Body",
        "explicit left and right member headings, toe-to-heel component order, detached-part cross-references, plain uncertainty phrases, monochrome state vocabulary, stable keyboard and print continuation, and zero manual, browser-diverse, assistive-technology, Māori-language, cognitive or affected-user sessions",
        ["WCAG22", "NPS-TEXTILE-OBJECTS", "W3C-PROV"],
    ),
    (
        "canonical-footwear-component-claim-graph",
        "Canonical footwear component-and-claim graph bundle with Unicode preservation, ordered pair, part and lineage edges, correction, supersession, reversible migration, collision refusal, and no authenticity proof",
        "completed",
        "GMUT Mind and Freed ID",
        "synthetic pair, component, claim and prior-digest nodes, Unicode-preserving labels, stable part and lineage edges, correction, supersession and tombstone without erasure, reversible migration ancestry, duplicate and collision rejection, and zero key, signature, proof, identity or authenticity conclusion",
        ["IETF-JCS", "JSON-SCHEMA-2020-12", "PYTHON-JSON", "W3C-PROV"],
    ),
    (
        "stage20-footwear-care-firewall",
        "Footwear real-claim promotion cut-set requiring authenticated pair provenance, accountable custodian, material examination, competent conservation assessment, safety review, cultural-rights mandate, affected-party remedy, independent reproduction, and fail-closed Stage 20 refusal",
        "completed",
        "All pillars",
        "typed cut-set slots for authenticated real-pair provenance, accountable custodian, material examination, competent conservation and safety review, cultural-rights mandate, intervention, outcome, affected-party remedy and independent reproduction, with absolute nonpromotion while any slot is empty",
        ["W3C-PROV", "IETF-JCS", "JSON-SCHEMA-2020-12", "TE-PAPA-MANA-TAONGA"],
    ),
]
NEW_PROPOSAL_SPECS = [_proposal(*row) for row in _NEW_ROWS]

SELF_SAFE_CATEGORIES = [
    "Caelen source head and fresh four-way equality",
    "activation packet, canonical, post-seal, post-send, and terminal-route receipt digests",
    "three-thousand-four-hundred-fifty-row proposal-chain parse",
    "twenty inherited selection identities",
    "twenty-title novelty screen",
    "mechanism-level footwear collection and conservation-triage neighbour review",
    "new-outcome distribution",
    "workflow-plan policy",
    "identity and relational-language boundary",
    "Hamish-authorized Caelen-to-Eiren live edge and terminally gated Eiren-to-Elaren route",
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
    {
        "task_id": f"V6621-SAFE-{i:03d}",
        "title": f"Validate {name} inside the Eiren-owned v662-v1 lane",
        "owner": OWNER,
    }
    for i, name in enumerate(SELF_SAFE_CATEGORIES, 1)
]
SUCCESSOR_SAFE_SEEDS = [
    {
        "task_id": f"V6621-REC-SAFE-{i:03d}",
        "title": f"Elaren may reassess {name} only after Eiren's terminal gate and a fresh route reread",
        "recipient": "Elaren Kestrel",
        "completion_credit": 0,
    }
    for i, name in enumerate(SELF_SAFE_CATEGORIES[:20], 1)
]

SELF_CANDIDATE_CATEGORIES = [
    "synthetic footwear pair identity and left-right reconciliation capsule",
    "upper-component and sole-stack topology with orphan quarantine",
    "multi-material source-claim and identification-nonclaim braid",
    "condition-observation and detached-part abstention ledgers",
    "zero-row CCI-to-NPS footwear source concordance",
    "GMUT layered upper-sole interface and deterioration interaction firewalls",
    "THOS pair reconciliation, residue stop, workload, readback and handover proxy",
    "Freed ID footwear record and canonical claim-graph envelopes",
    "linearized two-shoe relation narrative and rest-state surrogate",
    "CBR story, belonging, image reuse, return, redress and Māori non-substitution circuit",
]
SELF_CANDIDATE_TASKS = [
    {
        "task_id": f"V6621-CAND-{i:03d}",
        "title": f"Build and test reversible {name}",
        "owner": OWNER,
    }
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]
SUCCESSOR_CANDIDATE_SEEDS = [
    {
        "task_id": f"V6621-REC-CAND-{i:03d}",
        "title": f"Elaren may consider a distinct refinement of {name} after terminal activation",
        "recipient": "Elaren Kestrel",
        "completion_credit": 0,
    }
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]

EXACT_QUEUE = [
    {
        "task_id": f"V6621-EXACT-{i:03d}",
        "title": title,
        "state": "exact_gate_unexecuted",
    }
    for i, title in enumerate(
        [
            "Accession, catalogue, attribute, image, handle, lift, move, support, pack, clean, vacuum, sample, test, treat, conserve, publish, disclose, restrict, return, repatriate, release, or dispose of any real footwear object, fragment, image, record, taonga, or collection item",
            "Make a real footwear construction, leather, textile, rubber, plastic, cork, wood, metal, adhesive, maker, wearer, origin, fit, condition, pest, residue, toxicity, authenticity, provenance, rights, safety, support, treatment, quality, wearability, or release determination",
            "Use real makers, wearers, owners, donors, depositors, descendants, registrars, curators, conservators, researchers, communities, affected parties, footwear, images, labels, locations, or personal information",
            "Disclose private identity, address, request, relationship, traditional knowledge, restricted collection history, image, provenance, attribution, custody, access, return, repatriation, or remedy record",
            "Make a professional footwear, shoemaking, museum-registration, collection-care, conservation, material-identification, workplace-safety, privacy, security, translation, or accessibility determination",
            "Publish a production identifier, catalogue record, credential, signature, proof, status, interoperability result, image asset, collection service, or operational record",
            "Allocate ownership, custody, maker attribution, intellectual-property or image rights, access, return, repatriation, remedy, beneficiary, affected-party, descendant, or community authority",
            "Make a tikanga, mātauranga, wording, tangata whenua, iwi, hapū, Māori data-governance, cultural-protocol, taonga-status, or Māori-authority decision",
            "Run a real participant study, collection-room shift, handling trial, support trial, safety review, professional assessment, publication trial, or independent reproduction",
            "Perform destructive cleanup or any mutation outside the exact Eiren Kestrel-owned lane",
        ],
        1,
    )
]
BLOCKED_QUEUE = [
    {
        "task_id": f"V6621-BLOCK-{i:03d}",
        "title": title,
        "state": "blocked_unexecuted",
    }
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
    ("ghc-family-footwear-pair-identity", "Validate purpose-bound synthetic pair, singleton and left-right identities, revision, minimization, correction, and handling refusal."),
    ("ghc-family-footwear-component-topology", "Check upper and sole component nodes, seams, attachments, separation, ambiguity, orphan quarantine, and no repair instruction."),
    ("ghc-family-footwear-material-claim-lineage", "Separate supplied leather, textile, rubber, plastic and other material claims from identification, attribution and cultural conclusions."),
    ("ghc-family-footwear-condition-abstention", "Preserve visible cues, uncertainty, contradiction, correction, hazard hold, and diagnosis or treatment abstention."),
    ("ghc-family-footwear-detached-part", "Check detached-part source-member links, container token, discrepancy, transfer hold, correction, and no reattachment action."),
    ("ghc-family-footwear-canonical-claim-graph", "Preserve pair, part, claim, correction, supersession, restriction, tombstone, migration and collision-refusal lineage."),
    ("ghc-family-footwear-residue-emission-hold", "Keep mould, pesticide, residue, corrosion-contact, odour and emission cues quarantined from identification or treatment."),
    ("ghc-family-footwear-accessibility-narrative", "Expose left-right headings, toe-to-heel ordering, detached-part cross-references, uncertainty phrases, print continuity, and reserved human review."),
    ("ghc-family-gmut-footwear-interface-firewall", "Preserve typed layer, seam, welt, incidence, unit, covariance, boundary, identifiability, and observation-firewall obligations."),
    ("ghc-family-footwear-story-belonging-authority", "Keep maker and wearer provenance, memorial or sacred status, image reuse, return, redress and Māori decisions unoccupied."),
]
SUCCESSOR_SKILL_SEEDS = [
    {
        "name": name.replace("footwear", "later-domain"),
        "recipient": "Elaren Kestrel",
        "state": "recommendation_only",
        "completion_credit": 0,
    }
    for name, _ in SELF_SKILL_SPECS
]
SELF_RUNNER_SPECS = [
    (name.replace("ghc-family-", "ghc_family_").replace("-", "_") + ".py", purpose)
    for name, purpose in SELF_SKILL_SPECS
]
SUCCESSOR_RUNNER_SEEDS = [
    {
        "name": name.replace("footwear", "later_domain"),
        "recipient": "Elaren Kestrel",
        "state": "recommendation_only",
        "completion_credit": 0,
    }
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
    "keep real footwear, pairs, singletons, parts, fragments, people, images, labels, locations, records, and connector rows empty",
    "retain scanner candidates separately from confirmed payload hits",
    "scan only declared public owner surfaces across five classes",
    "refresh owner manifests after every additive lifecycle change",
    "verify deterministic JSON ordering and parsing",
    "verify proposal append-only arithmetic",
    "verify inherited revalidation receives zero novelty and completion credit",
    "verify outcome labels use only the four authorized states",
    "reserve manual and affected-user accessibility evaluation",
    "reserve legal, cultural, ownership, attribution, access, return, repatriation, privacy, and Māori authority",
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
    {
        "task_id": f"V6621-CLEAN-{i:03d}",
        "title": title,
        "owner": OWNER,
        "mode": "additive_review_only",
    }
    for i, title in enumerate(SELF_CLEAN_CATEGORIES, 1)
]
SUCCESSOR_CLEAN_SEEDS = [
    {
        "task_id": f"V6621-REC-CLEAN-{i:03d}",
        "title": title,
        "recipient": "Elaren Kestrel",
        "completion_credit": 0,
    }
    for i, title in enumerate(SELF_CLEAN_CATEGORIES, 1)
]

OFFICIAL_SOURCES = [
    ("CCI-BASKETRY-GUIDELINES", "official_canadian_conservation_institute", "https://www.canada.ca/en/conservation-institute/services/preventive-conservation/guidelines-collections/basketry-plant-materials.html", "Inherited basketry and plant-material construction and preventive-care vocabulary only; no real object assessment, handling, treatment or professional recommendation."),
    ("CCI-NOTE-6-2", "official_canadian_conservation_institute", "https://www.canada.ca/en/conservation-institute/services/conservation-preservation-publications/canadian-conservation-institute-notes/care-basketry.html", "Inherited basketry care and detached-element vocabulary only; no real handling, support, cleaning, treatment or object-specific conclusion."),
    ("CCI-LEATHER-GUIDELINES", "official_canadian_conservation_institute", "https://www.canada.ca/en/conservation-institute/services/preventive-conservation/guidelines-collections/caring-leather-skin-fur.html", "Leather, skin and fur composition, deterioration-risk and preventive-conservation vocabulary only; no real footwear identification, handling, support, treatment or professional recommendation."),
    ("CCI-NOTE-8-2", "official_canadian_conservation_institute", "https://www.canada.ca/en/conservation-institute/services/conservation-preservation-publications/canadian-conservation-institute-notes/care-alum-vegetable-mineral-leather.html", "Tanned-leather condition, storage and support vocabulary only; no real material identification, cleaning, dressing, treatment or footwear-specific conclusion."),
    ("CCI-PLASTICS-RUBBERS", "official_canadian_conservation_institute", "https://www.canada.ca/en/conservation-institute/services/preventive-conservation/guidelines-collections/caring-plastics-rubbers.html", "Plastic and rubber deterioration, emission, support and contact-risk vocabulary only; no real material identification, storage design, treatment or professional conclusion."),
    ("CCI-NOTE-15-1", "official_canadian_conservation_institute", "https://www.canada.ca/en/conservation-institute/services/conservation-preservation-publications/canadian-conservation-institute-notes/care-rubber-plastic.html", "Rubber and plastic condition-cue and cleaning-risk vocabulary only; no real footwear diagnosis, segregation, cleaning, repair or conservation instruction."),
    ("NPS-TEXTILE-OBJECTS", "official_us_national_park_service", "https://www.nps.gov/subjects/museums/upload/MHI_AppK_TextilesObjects.pdf", "Museum textile-object and footwear-support vocabulary only; no NPS applicability, real support design, handling, storage, display or professional determination."),
    ("NPS-MUSEUM-HANDBOOK-I", "official_us_national_park_service", "https://www.nps.gov/subjects/museums/mh1.htm", "Museum-collection preservation, storage, infestation, handling, safety and accountability vocabulary only; no NPS applicability, real collection action, professional authority or endorsement."),
    ("TE-PAPA-MANA-TAONGA", "official_museum_of_new_zealand_te_papa_tongarewa", "https://collections.tepapa.govt.nz/topic/1702", "Mana Taonga and community-relationship boundary vocabulary only; no cultural interpretation, taonga classification, tikanga, wording, community representation, Māori authority or ratification."),
    ("TE-PAPA-TEXTILE-CARE", "official_museum_of_new_zealand_te_papa_tongarewa", "https://www.tepapa.govt.nz/learn/guides-caring-for-objects/how-care-for-textiles-and-kakahu-maori-cloaks", "Plant-material textile and kākahu care vocabulary only; no claim that footwear is textile, no treatment instruction, and no Māori-language, tikanga, taonga or conservation authority."),
    ("LOC-MARC255", "official_library_of_congress", "https://www.loc.gov/marc/bibliographic/bd255.html", "Current MARC 21 cartographic mathematical-data vocabulary for scale, projection, coordinates and provenance only; no cataloguing, interpretation, location, rights or professional conclusion."),
    ("LOC-MARC008", "official_library_of_congress", "https://www.loc.gov/marc/bibliographic/concise/bd008p.html", "Current MARC 21 map fixed-field vocabulary only; zero real records and no cataloguing authority."),
    ("LOC-COLLECTIONS-CARE", "official_library_of_congress", "https://www.loc.gov/preservation/care/", "General collections-care and handling vocabulary only; no real item handling, storage, treatment, conservation or professional recommendation."),
    ("OGC-API-RECORDS", "official_open_geospatial_consortium", "https://ogcapi.ogc.org/records/", "OGC API Records Part 1 discovery and record vocabulary only; disabled transport, zero calls, rows, writes, locations or conformance claim."),
    ("LINZ-NZGB", "official_nz_geographic_board", "https://www.linz.govt.nz/our-work/new-zealand-geographic-board/about-new-zealand-geographic-board/board-documents-policies-and-standards", "Official place-name policy and authority-boundary vocabulary only; no naming, spelling, macron, land, cultural or Māori-authority decision."),
    ("NZ-MSL-SI", "official_nz_metrology_institute", "https://www.measurement.govt.nz/metrology/si-units", "SI quantity and unit vocabulary only; zero measurements, calibrations, uncertainty results or physical confirmation."),
    ("W3C-PROV", "official_w3c", "https://www.w3.org/TR/prov-o/", "Entity, activity, agent-placeholder, derivation, revision, invalidation and qualified-provenance vocabulary only."),
    ("W3C-VC2", "official_w3c", "https://www.w3.org/TR/vc-data-model-2.0/", "Credential subject, issuer, evidence, terms-of-use, validity, status and privacy vocabulary only; zero keys, proofs, issuances, presentations or production identities."),
    ("WCAG22", "official_w3c", "https://www.w3.org/TR/WCAG22/", "Accessible structure, alternatives, noncolour, navigation, focus, status and print vocabulary with manual, browser, assistive-technology, Māori-language, cognitive and affected-user evaluation reserved."),
    ("NZ-PRIVACY", "official_nz_privacy_commissioner", "https://www.privacy.org.nz/privacy-principles/", "Current New Zealand privacy-principle vocabulary including IPP 3A from May 2026 only; no legal, compliance, collection, disclosure or remedy conclusion."),
    ("TE-MANA-RARAUNGA", "primary_maori_data_sovereignty_network", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Māori data-sovereignty and governance reservation vocabulary only; no Māori authority, ratification, wording, naming, tikanga, mātauranga, taonga-status or cultural decision."),
    ("JSON-SCHEMA-2020-12", "primary_json_schema_project", "https://json-schema.org/draft/2020-12", "Schema, vocabulary, validation, annotation and fail-closed structural vocabulary only."),
    ("IETF-JCS", "official_rfc_editor", "https://www.rfc-editor.org/rfc/rfc8785", "Canonical JSON digest vocabulary without key, signature, proof, credential, identity or production claims."),
    ("GIT-CAT-FILE", "official_git_docs", "https://git-scm.com/docs/git-cat-file", "Batch object inspection and exact blob-byte vocabulary for disposable and read-only repository checks."),
    ("GIT-SPARSE-CHECKOUT", "official_git_docs", "https://git-scm.com/docs/git-sparse-checkout", "Sparse working-tree and sparse-index vocabulary for disposable owner-local fixtures only."),
    ("GIT-LS-FILES", "official_git_docs", "https://git-scm.com/docs/git-ls-files", "Tracked, staged and skip-worktree inspection vocabulary only."),
    ("PYTHON-SUBPROCESS", "official_python_docs", "https://docs.python.org/3/library/subprocess.html", "Bounded process, dual-pipe and communicate vocabulary for disposable owner-local fixtures only."),
    ("PYTHON-JSON", "official_python_docs", "https://docs.python.org/3/library/json.html", "Deterministic UTF-8 JSON parse and serialization vocabulary."),
]
SOURCE_STATUS = {
    "CCI-BASKETRY-GUIDELINES": "inherited_official_page_checked_2026_08_05",
    "CCI-NOTE-6-2": "official_page_checked_2026_08_05",
    "CCI-LEATHER-GUIDELINES": "official_page_checked_2026_08_05",
    "CCI-NOTE-8-2": "official_page_checked_2026_08_05",
    "CCI-PLASTICS-RUBBERS": "official_page_checked_2026_08_05",
    "CCI-NOTE-15-1": "official_page_checked_2026_08_05",
    "NPS-TEXTILE-OBJECTS": "official_appendix_pdf_checked_2026_08_05",
    "NPS-MUSEUM-HANDBOOK-I": "official_page_checked_2026_08_05",
    "TE-PAPA-MANA-TAONGA": "official_page_checked_2026_08_05",
    "TE-PAPA-TEXTILE-CARE": "official_page_checked_2026_08_05",
    "LOC-MARC255": "official_page_checked_2026_08_05",
    "LOC-MARC008": "official_page_updated_2025_12_checked_2026_08_05",
    "LOC-COLLECTIONS-CARE": "official_page_checked_2026_08_05",
    "OGC-API-RECORDS": "official_part_1_core_1_0_0_checked_2026_08_05",
    "LINZ-NZGB": "official_policy_page_checked_2026_08_05",
    "NZ-MSL-SI": "current_official_si_units_page",
    "W3C-PROV": "stable_recommendation",
    "W3C-VC2": "recommendation_2025_checked_2026_08_05",
    "WCAG22": "recommendation_2024",
    "NZ-PRIVACY": "current_including_ipp3a_from_2026_05_01",
    "TE-MANA-RARAUNGA": "primary_principles_current",
    "JSON-SCHEMA-2020-12": "current_2020_12",
    "IETF-JCS": "stable_informational_rfc",
    "GIT-CAT-FILE": "current",
    "GIT-SPARSE-CHECKOUT": "current",
    "GIT-LS-FILES": "current",
    "PYTHON-SUBPROCESS": "current",
    "PYTHON-JSON": "current",
}


def _startup_failure(
    negative_id: str, signature: str, recovery: str
) -> dict[str, object]:
    return {
        "negative_id": negative_id,
        "signature": signature,
        "recovery": recovery,
        "recovery_passed": True,
        "completion_credit": 0,
    }


_SOURCE_STARTUP_FAILURE_ROWS_IGNORED = [
    ("parallel-memory-and-skill-discovery-wrapper-treated-one-expected-rg-no-match-as-fatal", "Split the memory and skill searches, inspect each scalar result, and preserve the wrapper failure at zero credit."),
    ("broad-repository-guidance-inventory-exceeded-the-output-budget", "Enumerate exact guidance directories and read only the required named skills and schemas through EOF."),
    ("combined-auth-skill-schema-and-current-state-read-was-truncated", "Reread the auth skill, schema, and complete state separately in bounded numbered windows through EOF."),
    ("combined-activation-packet-line-windows-were-truncated", "Read the committed packet in single contiguous bounded windows through line 1176 and verify EOF."),
    ("committed-packet-word-count-method-disagreed-with-the-live-activation-claim", "Preserve both the claimed 24,694-word label and the direct immutable-blob whitespace count of 21,364; use neither discrepancy as completion credit."),
    ("broad-source-phase-size-inventory-exceeded-model-context", "Probe exact named artifact sizes in small groups and avoid another repository-wide size presentation."),
    ("final-manifest-size-probe-used-two-guessed-nonexistent-manifest-names", "Enumerate the exact validation directory before requesting final-delta-manifest.json and final-owner-manifest.json."),
    ("proposal-ledger-summary-projected-array-fields_from_top_level_counts_and_overproduced_output", "Inspect top-level field types first, then read the forty-row program through bounded ID and title projections."),
    ("multi-root-external-receipt-enumeration-timed_out_after_locating_required_receipts", "Stop the broad search and inspect only the exact located Sylven receipt directory and named receipt files."),
    ("combined_preworktree_existence_projection_used_a_command_separator_inside_a_hash_value", "Assign branch, path, and worktree results to scalars before building the PowerShell projection."),
    ("combined_preworktree_remote_probe_exceeded_its_bounded_timeout", "Separate local absence checks from one exact fresh remote branch probe with a longer bounded process-start allowance."),
    ("owner_frozen_index_read_assumed_the_source_path_was_materialized_under_inherited_sparse_rules", "Inspect worktree-specific sparse configuration, add only the read-only Sylven source and Caelen owner paths, and reread the exact index."),
    ("sparse_checkout_add_probe_used_an_unsupported_no_cone_option", "Keep the existing non-cone mode and repeat only the owner-local add operation with the supported skip-checks form."),
    ("first_bulk_template_owner_source_replacement_collapsed_two_relational_names", "Overwrite only the four uncommitted Caelen template copies from immutable source and repeat the mechanical rewrite with disjoint placeholders."),
    ("temporary_hash_probe_was_blocked_before_execution_by_command_policy", "Use a read-only in-memory Python Git-blob probe and create no temporary file."),
    ("first_substantive_category_patch_used_pre_rewrite_context_and_was_rejected", "Reread the exact current lines and apply a bounded context-aware patch; the rejected patch changed no repository byte."),
    ("data_summary_probe_assumed_a_nonexistent_new_proposals_attribute", "Inspect the data module's declared symbols and repeat only the scalar summary against NEW_PROPOSAL_SPECS; the failed read-only probe changed no repository byte."),
    ("novelty_probe_wrapper_indexed_dictionary_specs_as_tuple_rows", "Inspect one preregistration specification's declared keys and repeat only the read-only novelty wrapper using the title key; the failed probe changed no repository byte."),
    ("novelty_probe_wrapper_guessed_a_nonexistent_source_index_filename", "Enumerate the exact bounded Sylven proposal-directory filenames and repeat only the read-only overlap screen against the committed frozen-chain index; the failed probe changed no repository byte."),
    ("novelty_probe_stdout_inherited_the_windows_cp1252_encoder", "Repeat only the read-only novelty process with explicit UTF-8 standard streams so Māori characters remain intact; the failed probe changed no repository byte."),
    ("first_bounded_novelty_screen_rejected_one_accessibility_title_for_excess_inherited_overlap", "Retitle and narrow the rejected row around numbered footwear-construction adjacency and page-continuity semantics, then rerun only the read-only overlap screen before x1 freeze."),
    ("postbuild_x1_leakage_scan_used_an_unbalanced_powershell_quote", "Separate the Git status, bounded path inventory, and literal-token leakage checks so shell quoting is independently reviewable; the failed wrapper changed no repository byte."),
    ("first_x1_scoped_test_pass_found_missing_workflow_refinement_receipts", "Run the selected family-current workflow-plan refinement against the frozen request, retain its invalid-attempt witness, refresh only x1 derived receipts, and rerun the scoped x1 module."),
    ("first_x1_scoped_test_pass_found_missing_governance_and_meta_tool_receipts", "Run the selected family-current roster, authorization, index, reflection, Method Flow, and meta-tool-box checks in the owner phase, refresh only x1 derived receipts, and rerun the scoped x1 module."),
    ("first_x1_scoped_test_pass_found_a_stale_pre_activation_route_assertion", "Update only the copied test assertion to the live Caelen-active and unresolved-later-edge state, regenerate the manifest, and rerun the scoped x1 module."),
    ("broad_external_family_receipt_command_search_exceeded_its_bounded_timeout", "List only the exact Sylven v661-v8 builder and runner filenames, then search those bounded files for the receipt-producing invocations."),
    ("full_source_family_index_json_projection_exceeded_the_output_budget", "Query only the preferred-current fields or exact script names required by the missing x1 receipts rather than serializing the complete index."),
    ("auth_validator_help_probe_assumed_a_repo_local_script_that_was_not_present", "Resolve the exact installed auth-permission skill runner path before invoking its read-only help or validation surface; the failed probe wrote no output."),
    ("combined_auth_runner_resolution_treated_an_expected_repo_no_match_as_command_failure", "Use the exact installed auth-permission runner already found and keep any optional repository-local absence probe non-fatal."),
    ("combined_family_current_runner_source_projection_exceeded_its_bounded_timeout", "Inspect only each runner's argument parser and output contract with bounded searches rather than projecting four full scripts together."),
    ("combined_runner_parser_search_returned_failure_when_one_optional_pattern_had_no_match", "Use installed skill runner locations and per-runner help output; treat optional source-pattern absence as a neutral finding rather than a failed wrapper."),
    ("preregistered_invalid_workflow_request_was_rejected_on_the_messaging_boundary", "Retain the invalid workflow-plan artifacts at zero credit, then run only the corrected frozen request through the family-current refinement runner."),
    ("source_receipt_test_name_retained_a_successful_once_label_for_an_invalid_aggregate", "Rename only the test function to state invalid canonical and narrow dependency recovery truth; preserve the assertions, failed receipt, and zero-credit boundary."),
    ("x1_precommit_summary_guessed_a_nonexistent_document_cap_maximum_words_field", "Inspect the exact receipt keys before projection, then repeat the bounded read-only summary using the declared max_words field; the failed summary earns zero aggregate credit."),
    ("corrected_precommit_summary_ran_before_regeneration_after_the_latest_data_edit", "Regenerate all x1 derived artifacts, rerun only input-dependent family receipts, validate Method Flow, finalize the manifest, and then repeat the read-only precommit summary."),
]
_STARTUP_FAILURE_ROWS = [
    ("first_memory_probe_called_an_unavailable_nested_exec_command_alias", "Retain the unavailable-tool result at zero credit and use the declared shell_command surface for every later scalar probe."),
    ("drive_guardian_skill_read_timed_out_after_returning_its_complete_small_body", "Retain the timeout separately, verify that the complete skill body reached EOF, and avoid claiming timing success from content completion."),
    ("broad_activation_packet_line_window_was_truncated", "Retain the truncated display and replace broad packet windows with section headings, structured row fields, exact hashes, and bounded terminal reads."),
    ("smaller_activation_packet_window_exceeded_context_and_triggered_compaction", "Continue from the preserved state and use a linear whole-file parser with explicit EOF evidence instead of replaying large prose windows."),
    ("first_whole_packet_powershell_regex_projection_timed_out_without_output", "Replace backtracking regular expressions and repeated array growth with one linear parser over the immutable packet."),
    ("linear_packet_projection_stdout_inherited_windows_cp1252", "Repeat only the read-only projection with UTF-8 stdout so Māori text is preserved without changing repository bytes."),
    ("committed_packet_direct_word_count_disagreed_with_the_live_activation_claim", "Preserve the claimed 25,761-word label and the direct immutable Git-blob whitespace count of 22,761; use neither discrepancy as completion credit."),
    ("combined_source_inventory_and_optional_digest_search_returned_nonzero_on_expected_no_match", "Treat the optional hash-reference absence as a neutral result and inspect the named immutable external receipt directory directly."),
    ("first_required_artifact_size_projection_piped_directly_from_a_powershell_foreach", "Materialize every projected row before ConvertTo-Json and retain the parser rejection as a read-only zero-credit witness."),
    ("proposal_ledger_audit_assumed_uniform_novelty_credit_keys_across_inherited_and_new_rows", "Inspect actual row keys, use explicit getters for optional credit fields, and preserve the KeyError without rewriting the source ledger."),
    ("broad_phase_script_inventory_matched_the_version_token_in_the_worktree_path", "Filter on literal basenames rather than full paths and enumerate only the exact current-phase scripts and tests."),
    ("combined_external_receipt_read_timed_out_before_returning_evidence", "Hash and read each named external receipt in its own bounded scalar process and never replay the successful canonical validator."),
    ("parallel_collision_capacity_sparse_and_equality_preflight_hit_its_overall_bound", "Run path, local ref, remote ref, D-drive, sparse posture and source equality probes separately before worktree creation."),
    ("first_scalar_path_probe_used_a_ten_second_bound_below_current_powershell_startup_latency", "Retain the timeout, increase only the process-start allowance, and repeat the same read-only path predicate."),
    ("first_twenty_title_footwear_screen_rejected_six_template_neighbours", "Retain the six failures, replace noun-substitution mechanisms with six distinct structures, and rerun only the read-only 3,450-title screen."),
    ("worktree_crlf_hash_was_initially_compared_instead_of_the_declared_git_blob_hash_domain", "Retain both byte domains, then hash the immutable Git blob directly through binary subprocess output for the activation packet pin."),
    ("broad_stale_label_search_over_the_copied_x1_builder_exceeded_the_output_budget", "Retain the oversized projection, split the review into bounded literal-pattern and line-window checks, and patch only the new Eiren-owned builder and tests."),
    ("first_novelty_probe_invocation_used_an_undeclared_json_flag_and_omitted_the_required_index", "Retain the argparse rejection, inspect the exact probe help, and invoke only its declared positional index and bounded options."),
    ("second_novelty_probe_invocation_omitted_the_required_stdin_title_array_and_misread_expected_count", "Retain the JSON decode failure, supply exactly twenty current titles on standard input, and keep the immutable index count as a separately asserted 3,450-row receipt field."),
    ("powershell_pipeline_replaced_a_maori_macron_in_the_read_only_novelty_receipt", "Retain the lossy console projection, set the PowerShell pipeline and console to UTF-8, and rerun only the read-only novelty probe while the builder also audits the direct in-process strings."),
    ("first_x1_scoped_test_aggregate_ran_before_family_current_tooling_receipts_were_materialized", "Retain the 21-of-23 dependency result at zero aggregate credit, generate only the preregistered workflow, index, reflection, Method Flow, roster, auth and meta-tool receipts, then rerun the two affected tests before considering any broader replay."),
    ("parallel_affected_tool_refresh_propagated_the_preregistered_invalid_workflow_exit_as_a_wrapper_failure", "Retain the wrapper failure, verify each independently written receipt, and handle the expected invalid-request exit code separately from the valid workflow and Method Flow validations."),
    ("precommit_stale_label_scan_repeatedly_searched_minified_index_artifacts_and_exceeded_its_bound", "Retain the timeout, exclude already hash-verified frozen and family indexes, and run one bounded multi-pattern scan over current-owner code and narrative artifacts."),
    ("first_bounded_multi_pattern_rg_argument_array_split_zero_and_null_suffix_literals", "Retain the malformed search and use one native PowerShell SimpleMatch pass over a materialized, explicitly excluded current-owner file list."),
]
STARTUP_FAILURES = [
    _startup_failure(f"V6621-X1-N{i:03d}", signature, recovery)
    for i, (signature, recovery) in enumerate(_STARTUP_FAILURE_ROWS, 1)
]

PREFILLED_X1_X2_FAILURES_IGNORED: tuple[dict[str, object], ...] = tuple()
X2_FAILURES: list[dict[str, object]] = []
