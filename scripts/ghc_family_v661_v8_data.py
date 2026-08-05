#!/usr/bin/env python3
"""Frozen x1 planning truth for Caelen Morrow v661-v8.

Sylven Arc's immutable v661-v7 packet is evidence and compatibility context,
not Caelen novelty or completion credit. Twenty inherited Sylven contracts are
selected for bounded revalidation with zero Caelen credit. Only the twenty new
basketry-collection documentation contracts below extend the proposal chain.
All fixtures are synthetic and contain no real object, collection row, person,
place, image, credential, key, professional act, or authority decision.
"""

from __future__ import annotations


PHASE = "v661-v8"
CANONICAL_PHASE = PHASE
PHASE_CODE = "V6618"
OWNER = "Caelen Morrow"
PRONOUNS = "they/them"
ROLE = "relational chronometry boundary-mapper and failure custodian"
HOPE = "keep claims traceable while leaving real competence and authority with the people who hold it"
BRANCH = "codex/GHC-Family/caelen-morrow-v661-v8-full-tools"
PHASE_ROOT = "docs/caelen-morrow/v661-v8"

SOURCE_OWNER = "Sylven Arc"
SOURCE_BRANCH = "codex/GHC-Family/sylven-arc-v661-v7-full-tools"
SOURCE_BASE = "29c45767ef5d2b6b48a14460708576bbba29efa2"
SOURCE_X1 = "7b14e314d4e16cf18a1726c8988cd5e11843f410"
SOURCE_EVIDENCE = "7a81185d14d4255329824cbf9bbf67520039d630"
SOURCE_FINAL = "2017e0a70d7a724c087b911387e3648e9cd03295"
SOURCE_CANONICAL_RECEIPT_SHA256 = (
    "25bf1488d9885827dba140f5c524a77a400f0ce4a8869914489bc9be6eed10de"
)
SOURCE_DEPENDENCY_RECOVERY_SHA256 = (
    "c26d0f504a5521311af50bfc12be67bc53d2841c59ffa5f45c07f72abeee3163"
)
SOURCE_VALIDATION_STATE = (
    "VALID_DEPENDENCY_CORRECTED_COMPOSITE_WITH_ZERO_CANONICAL_AGGREGATE_CREDIT"
)
SOURCE_LIVE_ACTIVATION_STATE = "SENT_ONCE_ACKNOWLEDGED_BY_DIRECT_TARGET_REREAD"
ACTIVATION_PACKET_SHA256 = (
    "109816e9127ba0ead545bd8b42d199900f72a9f24fcfdbc0ccad89bf5bb7194b"
)
ACTIVATION_PACKET_BYTES = 245656
ACTIVATION_PACKET_LINES = 1176
ACTIVATION_PACKET_WORDS_DIRECT = 21364
ACTIVATION_PACKET_WORDS_CLAIMED = 24694

PRIOR_FROZEN = 3430
SOURCE_SEALED_NEGATIVES = 21896
SOURCE_EXTERNAL_NEGATIVES = 3
ACTIVATION_NEGATIVES = SOURCE_SEALED_NEGATIVES + SOURCE_EXTERNAL_NEGATIVES
ACTIVATION_MESSAGE_NEGATIVE_BASELINE = 21899
SOURCE_OPEN_GAPS = 144
SOURCE_EXACT_GATES = 143
SOURCE_SEALED_METHODS = 6970
SOURCE_EXTERNAL_METHODS = 3
ACTIVATION_METHODS = SOURCE_SEALED_METHODS + SOURCE_EXTERNAL_METHODS
ACTIVATION_MESSAGE_METHOD_BASELINE = 6973

SELECTED_INHERITED_COUNT = 20
NEW_UNIQUE_COUNT = 20
CURRENT_PORTFOLIO_COUNT = 40
LATEST_TRACKED_SCAN_CAP = 5000
SELECTED_INHERITED_IDS = [f"V6617-P{i:03d}" for i in range(1, 21)]

PRIMARY_PILLAR = "CBR Heart"
PRACTICE_LENS = (
    "bounded synthetic basketry collection documentation and conservation-triage "
    "practice, including surrogate object identity, construction relations, source-claim "
    "lineage, condition vocabulary, detached-element records, preventive-care holds, "
    "cultural-rights reservations, workload control, correction readback, and handover"
)
EXPECTED_DISTRIBUTION = {
    "completed": 14,
    "represented": 4,
    "open_gap": 1,
    "exact_gate": 1,
}
ALLOWED_OUTCOMES = set(EXPECTED_DISTRIBUTION)

PROTECTED_GATES = [
    "real_baskets_mats_hats_bags_woven_or_interworked_plant_objects_fragments_taonga_collections_stores_displays_or_laboratories",
    "real_makers_owners_donors_depositors_descendants_registrars_curators_conservators_researchers_communities_affected_parties_and_authorities",
    "real_accession_cataloguing_attribution_imaging_handling_lifting_moving_supporting_packing_cleaning_vacuuming_sampling_testing_pest_treatment_conservation_publication_access_or_release_action",
    "professional_basketry_museum_registration_collection_care_conservation_material_identification_workplace_safety_accessibility_privacy_or_operational_authority",
    "empirical_gmut_prediction_likelihood_parameter_constraint_observational_confirmation_physical_discovery_or_final_physics",
    "blind_matched_budget_thos_real_arms_governed_participants_operators_safety_monitoring_statistics_and_independent_review",
    "production_identity_live_keys_signatures_proofs_issuance_resolution_status_revocation_interoperability_recovery_and_trust",
    "maker_owner_donor_depositor_descendant_or_user_identity_address_message_relationship_location_collection_history_images_provenance_traditional_knowledge_collective_interest_and_remedy",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "legal_cultural_workplace_safety_intellectual_property_image_rights_ownership_custody_access_return_repatriation_data_governance_and_maori_authority",
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
        "basketry-collection-identity-capsule",
        "Surrogate basketry collection identity capsule with object-class placeholder, component scope, source pin, revision, minimization, cancellation, correction, and handling refusal",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic object-class and collection-alias tokens, component scope, received-state boundary, source pin, revision, purpose minimization, cancellation, correction, and absolute work-start and handling refusal",
        ["W3C-PROV", "NZ-PRIVACY", "NPS-MUSEUM-HANDBOOK-I"],
    ),
    (
        "basketry-construction-topology",
        "Basketry spoke, stake, stave, weaver, coil, row, plait, splint, rim, base, handle, lashing, and orphan-quarantine topology",
        "completed",
        "CBR Heart and GMUT Mind",
        "typed synthetic passive and active element nodes, coiling, twining, plaiting, wicker and splint relations, rim, base, handle and lashing edges, duplicate and orphan quarantine, concealed-state vacancy, and no construction or repair instruction",
        ["CCI-BASKETRY-GUIDELINES", "JSON-SCHEMA-2020-12", "W3C-PROV"],
    ),
    (
        "basketry-material-claim-lineage",
        "Plant-fibre, bark, root, cane, wicker, splint, dye, coating, source-label, maker-claim, collector-claim, and material-attribution nonclaim braid",
        "completed",
        "CBR Heart and Freed ID",
        "synthetic material and preparation tokens, quoted source-label and maker or collector claim classes, supplied-versus-observed separation, contradiction and substitution holds, correction and supersession, and zero species, origin, authenticity, attribution or cultural-meaning conclusion",
        ["CCI-BASKETRY-GUIDELINES", "W3C-PROV", "TE-PAPA-MANA-TAONGA"],
    ),
    (
        "basketry-condition-observation-ledger",
        "Basketry break, split, loss, abrasion, distortion, staining, fading, powder, pest cue, residue, uncertainty, and diagnosis-abstention ledger",
        "completed",
        "THOS Body and CBR Heart",
        "synthetic visible-state tokens with location and source placeholders, uncertainty and contradiction retention, observation-versus-diagnosis separation, hazard escalation vacancy, correction and supersession, and zero inspection, material identification, treatment or condition conclusion",
        ["CCI-BASKETRY-GUIDELINES", "CCI-NOTE-6-2", "W3C-PROV"],
    ),
    (
        "detached-basketry-element-lineage",
        "Detached basketry element, fragment, loss-location, container-token, label-link, transfer hold, discrepancy, correction, and no-handling-action ledger",
        "completed",
        "Freed ID and THOS Body",
        "synthetic detached-element and fragment tokens, source-object link, reported loss location, empty container and label placeholders, discrepancy, custody-vacancy and transfer hold, reversible correction, and no bagging, moving, reattachment or disposal instruction",
        ["CCI-NOTE-6-2", "W3C-PROV", "NZ-PRIVACY"],
    ),
    (
        "basketry-rights-authority-matrix",
        "Vacant mandate matrix for basketry ownership, custody, maker attribution, traditional knowledge, imagery, access, return, repatriation, remedy, and tangata whenua, iwi, hapū, Māori authority",
        "exact_gate",
        "CBR Heart",
        "unoccupied maker, owner, donor, depositor, descendant, community, custody, attribution, traditional-knowledge, imagery, access, return, repatriation, legal, cultural, privacy, affected-party, remedy, tangata whenua, iwi, hapū and Māori-authority reservations",
        ["TE-PAPA-MANA-TAONGA", "TE-MANA-RARAUNGA", "NZ-PRIVACY", "WCAG22"],
    ),
    (
        "thos-basketry-intake-handover",
        "THOS basketry intake, fragility hold, detached-element readback, pest-cue stop, workload ceiling, correction digest, escalation, and shift-handover proxy",
        "represented",
        "THOS Body",
        "synthetic intake and queue tokens, object and detached-element readback, fragility and pest-cue holds, no-touch stop, workload ceiling, correction digest, escalation and resumption vacancies, and zero workers, objects, handling or effectiveness observations",
        ["CCI-BASKETRY-GUIDELINES", "NPS-MUSEUM-HANDBOOK-I", "WCAG22", "W3C-PROV"],
    ),
    (
        "freed-id-basketry-record-profile",
        "Freed ID nonproduction basketry-record profile binding surrogate object, construction assertion, condition note, detached element, source claim, correction, restriction, and provenance evidence",
        "represented",
        "Freed ID and CBR Heart",
        "synthetic record and object identifiers, credential-subject, evidence and terms-of-use placeholders, construction and condition assertion relations, detached-element and correction links, restriction and revocation vacancies, privacy mask, and zero keys, proofs, issuances, presentations or interoperability",
        ["W3C-VC2", "W3C-PROV", "NZ-PRIVACY", "TE-PAPA-MANA-TAONGA"],
    ),
    (
        "gmut-basketry-interlacement-proxy",
        "Represented GMUT anisotropic basketry interlacement graph with passive and active directions, junction incidence, curvature, strain and damping placeholders, units, covariance vacancy, and observation firewall",
        "represented",
        "GMUT Mind",
        "typed symbolic passive and active direction fields, interlacement and junction graph, incidence orientation, curvature, strain, stiffness and damping placeholders, unit and covariance vacancies, boundary and identifiability holds, exact counterexamples, and zero measurements, fits or physical predictions",
        ["NZ-MSL-SI", "CCI-BASKETRY-GUIDELINES", "W3C-PROV"],
    ),
    (
        "basketry-support-review-shell",
        "Represented basketry support and mount review shell with contact-zone placeholders, clearance, load-path vacancy, enclosure relation, access hold, rollback, and zero-object review",
        "represented",
        "THOS Body and CBR Heart",
        "synthetic object-envelope and support tokens, contact-zone and clearance placeholders, load-path and material-compatibility vacancies, enclosure and access relations, approval and rollback slots, and zero dimensions, materials, mounts, handling, tests or professional review",
        ["CCI-BASKETRY-GUIDELINES", "NPS-MUSEUM-HANDBOOK-I", "W3C-PROV"],
    ),
    (
        "official-basketry-zero-row-adapter",
        "Official CCI basketry-guidance and NPS museum-handbook adapter with zero calls, rows, credentials, objects, images, measurements, treatment instructions, rights conclusions, or professional claims",
        "open_gap",
        "CBR Heart and GMUT Mind",
        "offline source and section schema, guidance-version and provenance placeholders, disabled transport, zero content rows, zero objects and images, bounded parser vocabulary, stale-source hold, and fail-closed professional, cultural, legal, safety and empirical inference refusal",
        ["CCI-BASKETRY-GUIDELINES", "NPS-MUSEUM-HANDBOOK-I", "PYTHON-JSON", "NZ-PRIVACY"],
    ),
    (
        "basketry-technique-syntax-tribunal",
        "Coiling, twining, plaiting, wickerwork, splintwork, bark-sheet, mixed-technique, passive-element, active-element, row-direction, and classification-abstention syntax tribunal",
        "completed",
        "CBR Heart and GMUT Mind",
        "synthetic technique and element tokens, passive-versus-active relation, row and direction placeholders, mixed and unknown cases, ambiguity and contradiction quarantine, reversible supplied-text preservation, and zero cultural, maker, origin, authenticity or professional classification claim",
        ["CCI-BASKETRY-GUIDELINES", "JSON-SCHEMA-2020-12", "W3C-PROV"],
    ),
    (
        "basketry-environment-risk-nonconversion",
        "Basketry physical-force, fire, water, pollutant, light, temperature, relative-humidity, duration, uncertainty, missing-sensor, and preservation-nonconversion board",
        "completed",
        "THOS Body and GMUT Mind",
        "synthetic risk-class and environment placeholders, explicit units and source, missing and stale sensor states, uncertainty and duration vacancies, threshold-source hold, nonconversion from guidance to object-specific prescription, and zero measurements, setpoints, alarms or conservation conclusions",
        ["CCI-BASKETRY-GUIDELINES", "NPS-MUSEUM-HANDBOOK-I", "NZ-MSL-SI"],
    ),
    (
        "basketry-pest-hazard-quarantine",
        "Basketry pest cue, particulate, dust, soot, powder, residue, mould suspicion, prior-use evidence hold, toxic-material vacancy, isolation, escalation, and no-treatment tribunal",
        "completed",
        "THOS Body and CBR Heart",
        "synthetic pest and particulate cues, observation-source placeholder, prior-use-evidence hold, toxic-material and mould identification vacancies, isolation and competent-review escalation states, correction and rollback, and zero sampling, testing, cleaning, pesticide, freezing or treatment action",
        ["CCI-BASKETRY-GUIDELINES", "NPS-MUSEUM-HANDBOOK-I", "W3C-PROV"],
    ),
    (
        "basketry-image-label-provenance",
        "Basketry image and label provenance docket with surrogate asset token, viewpoint, source-class, supplied text, transcription, rights vacancy, redaction, restriction, correction, and no-attribution claim",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic image and label asset tokens, viewpoint and source class, supplied-versus-transcribed text, rights and cultural-review vacancies, minimization and redaction, access restriction, correction and supersession, and zero real image, OCR, publication, maker or cultural attribution",
        ["TE-PAPA-MANA-TAONGA", "NZ-PRIVACY", "W3C-PROV"],
    ),
    (
        "accessible-basketry-record-companion",
        "Keyboard-readable basketry construction adjacency transcript with numbered surrogate elements, edge summaries, uncertainty cues, monochrome state keys, page-break continuity, and reserved human evaluation",
        "completed",
        "CBR Heart and THOS Body",
        "ordered surrogate element indices, adjacency sentences, edge and uncertainty summaries, monochrome state keys, stable keyboard order, page-break continuity, plain-language scope notes, and zero manual, browser-diverse, assistive-technology, Māori-language, cognitive or affected-user sessions",
        ["WCAG22", "CCI-BASKETRY-GUIDELINES", "W3C-PROV"],
    ),
    (
        "basketry-brittle-interface-tribunal",
        "Basketry brittle-flexible interface, rim and base attachment, protrusion, fold line, contact zone, load-path vacancy, deformation cue, uncertainty, and stability-refusal tribunal",
        "completed",
        "GMUT Mind and THOS Body",
        "synthetic interface and attachment nodes, flexible-versus-rigid state, protrusion and fold-line cues, contact and load-path vacancies, deformation and uncertainty states, contradiction quarantine, and zero load test, structural diagnosis, handling, support or stability conclusion",
        ["CCI-BASKETRY-GUIDELINES", "JSON-SCHEMA-2020-12", "W3C-PROV"],
    ),
    (
        "stage20-basketry-care-firewall",
        "Stage 20 basketry-care evidence firewall with object, practitioner, mandate, observation, intervention, outcome, independent-review, affected-party, and authority vacancies",
        "completed",
        "All pillars",
        "typed evidence slots for real objects, competent practitioners, mandate, observations, intervention, safety monitoring, outcome, independent review, affected parties and authorities, explicit non-substitution rules, retained failures, and absolute nonpromotion while every slot is empty",
        ["W3C-PROV", "IETF-JCS", "JSON-SCHEMA-2020-12"],
    ),
    (
        "basketry-correction-supersession-braid",
        "Basketry assertion correction and supersession braid with prior digest, changed field set, source class, evidence vacancy, contestation, restriction, tombstone, non-erasure, and no cryptographic proof",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic assertion and prior-digest placeholders, changed-field set, supplied and observed source classes, evidence vacancy, contestation, restriction, correction, supersession and tombstone without erasure, and zero issuer, key, signature, proof or authority determination",
        ["W3C-PROV", "W3C-VC2", "IETF-JCS", "NZ-PRIVACY"],
    ),
    (
        "canonical-basketry-construction-graph",
        "Canonical basketry construction graph bundle with Unicode preservation, ordered element and relation edges, explicit hash domain, reversible migration ancestry, duplicate collapse, collision refusal, and no authenticity proof",
        "completed",
        "GMUT Mind and Freed ID",
        "synthetic element and relation graph, Unicode-preserving labels, stable node and edge ordering, declared Git-clean and logical-text hash domains, reversible migration ancestry, duplicate and collision rejection, bounded resource limits, and no key, signature, proof, identity, authenticity or production claim",
        ["IETF-JCS", "JSON-SCHEMA-2020-12", "PYTHON-JSON", "W3C-PROV"],
    ),
]
NEW_PROPOSAL_SPECS = [_proposal(*row) for row in _NEW_ROWS]

SELF_SAFE_CATEGORIES = [
    "Sylven source head and fresh four-way equality",
    "activation packet, invalid canonical receipt, and dependency-recovery digests",
    "three-thousand-four-hundred-thirty-row proposal-chain parse",
    "twenty inherited selection identities",
    "twenty-title novelty screen",
    "mechanism-level basketry collection and conservation-triage neighbour review",
    "new-outcome distribution",
    "workflow-plan policy",
    "identity and relational-language boundary",
    "Hamish-authorized Sylven-to-Caelen live edge and unresolved terminal route",
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
        "task_id": f"V6618-SAFE-{i:03d}",
        "title": f"Validate {name} inside the Caelen-owned v661-v8 lane",
        "owner": OWNER,
    }
    for i, name in enumerate(SELF_SAFE_CATEGORIES, 1)
]
SUCCESSOR_SAFE_SEEDS = [
    {
        "task_id": f"V6618-REC-SAFE-{i:03d}",
        "title": f"Reassess {name} only if a later owner is explicitly authorized after Caelen's terminal gate",
        "recipient": None,
        "completion_credit": 0,
    }
    for i, name in enumerate(SELF_SAFE_CATEGORIES[:20], 1)
]

SELF_CANDIDATE_CATEGORIES = [
    "synthetic basketry collection identity and purpose capsule",
    "basketry passive-active element and construction-relation topology",
    "plant-material and maker-claim source-lineage braid",
    "condition-observation and detached-element non-diagnosis ledgers",
    "official basketry-guidance zero-row adapter",
    "GMUT anisotropic interlacement and brittle-interface firewalls",
    "THOS fragility-hold, workload, readback and handover proxy",
    "Freed ID basketry record and correction envelopes",
    "accessible basketry report and construction-relation companion",
    "CBR ownership, attribution, knowledge, access, return, remedy and Māori-authority circuit",
]
SELF_CANDIDATE_TASKS = [
    {
        "task_id": f"V6618-CAND-{i:03d}",
        "title": f"Build and test reversible {name}",
        "owner": OWNER,
    }
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]
SUCCESSOR_CANDIDATE_SEEDS = [
    {
        "task_id": f"V6618-REC-CAND-{i:03d}",
        "title": f"Consider a distinct later-owner refinement of {name}",
        "recipient": None,
        "completion_credit": 0,
    }
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]

EXACT_QUEUE = [
    {
        "task_id": f"V6618-EXACT-{i:03d}",
        "title": title,
        "state": "exact_gate_unexecuted",
    }
    for i, title in enumerate(
        [
            "Accession, catalogue, attribute, image, handle, lift, move, support, pack, clean, vacuum, sample, test, treat, conserve, publish, disclose, restrict, return, repatriate, release, or dispose of any real basketry object, fragment, image, record, taonga, or collection item",
            "Make a real construction-technique, plant-material, maker, origin, condition, pest, residue, toxicity, authenticity, provenance, rights, safety, access, support, treatment, quality, or release determination",
            "Use real makers, owners, donors, depositors, descendants, registrars, curators, conservators, researchers, communities, affected parties, objects, images, labels, locations, or personal information",
            "Disclose private identity, address, request, relationship, traditional knowledge, restricted collection history, image, provenance, attribution, custody, access, return, repatriation, or remedy record",
            "Make a professional basketry, museum-registration, collection-care, conservation, material-identification, workplace-safety, privacy, security, translation, or accessibility determination",
            "Publish a production identifier, catalogue record, credential, signature, proof, status, interoperability result, image asset, collection service, or operational record",
            "Allocate ownership, custody, maker attribution, intellectual-property or image rights, access, return, repatriation, remedy, beneficiary, affected-party, descendant, or community authority",
            "Make a tikanga, mātauranga, wording, tangata whenua, iwi, hapū, Māori data-governance, cultural-protocol, taonga-status, or Māori-authority decision",
            "Run a real participant study, collection-room shift, handling trial, support trial, safety review, professional assessment, publication trial, or independent reproduction",
            "Perform destructive cleanup or any mutation outside the exact Caelen Morrow-owned lane",
        ],
        1,
    )
]
BLOCKED_QUEUE = [
    {
        "task_id": f"V6618-BLOCK-{i:03d}",
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
    ("ghc-family-basketry-collection-identity", "Validate purpose-bound synthetic basketry collection identity, revision, minimization, cancellation, and handling refusal."),
    ("ghc-family-basketry-construction-topology", "Check passive and active element nodes, construction relations, ambiguity, orphan quarantine, and no construction instruction."),
    ("ghc-family-basketry-material-claim-lineage", "Separate supplied material, maker and collector claims from observation, attribution and cultural-meaning conclusions."),
    ("ghc-family-basketry-condition-abstention", "Preserve observation, uncertainty, contradiction, correction, hazard hold, and diagnosis or treatment abstention."),
    ("ghc-family-basketry-detached-element", "Check detached-element source links, reported location, empty container, discrepancy, transfer hold, and no handling action."),
    ("ghc-family-basketry-correction-lineage", "Preserve source, assertion, correction, supersession, contestation, restriction, tombstone, and non-erasure."),
    ("ghc-family-basketry-privacy-access-hold", "Keep identity, image, source, retention, disclosure, access, return, repatriation, correction, and remedy data minimized."),
    ("ghc-family-basketry-accessibility-companion", "Expose structural tables, textual construction relations, noncolour state, alternatives, focus order, print fallback, and reserved human review."),
    ("ghc-family-gmut-interlacement-firewall", "Preserve typed direction, junction, incidence, unit, covariance, boundary, identifiability, and observation-firewall obligations."),
    ("ghc-family-basketry-rights-authority", "Keep ownership, attribution, traditional knowledge, imagery, access, return, repatriation, remedy, and Māori decision rights unoccupied."),
]
SUCCESSOR_SKILL_SEEDS = [
    {
        "name": name.replace("basketry", "later-domain"),
        "recipient": None,
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
        "name": name.replace("basketry", "later_domain"),
        "recipient": None,
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
    "keep real basketry objects, fragments, people, images, labels, locations, records, and connector rows empty",
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
        "task_id": f"V6618-CLEAN-{i:03d}",
        "title": title,
        "owner": OWNER,
        "mode": "additive_review_only",
    }
    for i, title in enumerate(SELF_CLEAN_CATEGORIES, 1)
]
SUCCESSOR_CLEAN_SEEDS = [
    {
        "task_id": f"V6618-REC-CLEAN-{i:03d}",
        "title": title,
        "recipient": None,
        "completion_credit": 0,
    }
    for i, title in enumerate(SELF_CLEAN_CATEGORIES, 1)
]

OFFICIAL_SOURCES = [
    ("CCI-BASKETRY-GUIDELINES", "official_canadian_conservation_institute", "https://www.canada.ca/en/conservation-institute/services/preventive-conservation/guidelines-collections/basketry-plant-materials.html", "Basketry and plant-material construction, deterioration-risk and preventive-care vocabulary only; no real object assessment, handling, support, cleaning, pest response, treatment or professional recommendation."),
    ("CCI-NOTE-6-2", "official_canadian_conservation_institute", "https://www.canada.ca/en/conservation-institute/services/conservation-preservation-publications/canadian-conservation-institute-notes/care-basketry.html", "General basketry care, detached-element recording, storage and pest-check vocabulary only; no real handling, bagging, support, cleaning, treatment or object-specific conclusion."),
    ("NPS-MUSEUM-HANDBOOK-I", "official_us_national_park_service", "https://www.nps.gov/subjects/museums/mh1.htm", "Museum-collection preservation, storage, infestation, handling, safety and accountability vocabulary only; no NPS applicability, real collection action, professional authority or endorsement."),
    ("TE-PAPA-MANA-TAONGA", "official_museum_of_new_zealand_te_papa_tongarewa", "https://collections.tepapa.govt.nz/topic/1702", "Mana Taonga and community-relationship boundary vocabulary only; no cultural interpretation, taonga classification, tikanga, wording, community representation, Māori authority or ratification."),
    ("TE-PAPA-TEXTILE-CARE", "official_museum_of_new_zealand_te_papa_tongarewa", "https://www.tepapa.govt.nz/learn/guides-caring-for-objects/how-care-for-textiles-and-kakahu-maori-cloaks", "Plant-material textile and kākahu care vocabulary only; no claim that basketry is textile, no treatment instruction, and no Māori-language, tikanga, taonga or conservation authority."),
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
    "CCI-BASKETRY-GUIDELINES": "official_page_checked_2026_08_05",
    "CCI-NOTE-6-2": "official_page_checked_2026_08_05",
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


_STARTUP_FAILURE_ROWS = [
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
    ("first_bounded_novelty_screen_rejected_one_accessibility_title_for_excess_inherited_overlap", "Retitle and narrow the rejected row around numbered basketry-construction adjacency and page-continuity semantics, then rerun only the read-only overlap screen before x1 freeze."),
    ("postbuild_x1_leakage_scan_used_an_unbalanced_powershell_quote", "Separate the Git status, bounded path inventory, and literal-token leakage checks so shell quoting is independently reviewable; the failed wrapper changed no repository byte."),
    ("first_x1_scoped_test_pass_found_missing_workflow_refinement_receipts", "Run the selected family-current workflow-plan refinement against the frozen request, retain its invalid-attempt witness, refresh only x1 derived receipts, and rerun the scoped x1 module."),
    ("first_x1_scoped_test_pass_found_missing_governance_and_meta_tool_receipts", "Run the selected family-current roster, authorization, index, reflection, Method Flow, and meta-tool-box checks in the owner phase, refresh only x1 derived receipts, and rerun the scoped x1 module."),
    ("first_x1_scoped_test_pass_found_a_stale_pre_activation_route_assertion", "Update only the copied test assertion to the live Caelen-active and unresolved-later-edge state, regenerate the manifest, and rerun the scoped x1 module."),
    ("broad_external_family_receipt_command_search_exceeded_its_bounded_timeout", "List only the exact Sylven v661-v7 builder and runner filenames, then search those bounded files for the receipt-producing invocations."),
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
STARTUP_FAILURES = [
    _startup_failure(f"V6618-X1-N{i:03d}", signature, recovery)
    for i, (signature, recovery) in enumerate(_STARTUP_FAILURE_ROWS, 1)
]

PREFILLED_X1_X2_FAILURES_IGNORED: tuple[dict[str, object], ...] = tuple()
X2_FAILURES: list[dict[str, object]] = []
