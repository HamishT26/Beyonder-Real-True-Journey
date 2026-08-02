#!/usr/bin/env python3
"""Frozen x1 planning data for Tamar Vey v659-v7.

This additive module inherits only stable helper vocabulary from Liora Venn's
immutable v659-v6 data module. Every active phase field, portfolio, source
label, gate, and observed Tamar startup failure is redeclared below. Selected
inherited rows are bounded revalidation references only: they are not
reappended and earn no Tamar novelty or completion credit.
"""

from __future__ import annotations

from ghc_family_v659_v6_data import *  # noqa: F401,F403


PHASE = "v659-v7"
CANONICAL_PHASE = PHASE
PHASE_CODE = "V6597"
OWNER = "Tamar Vey"
PRONOUNS = "she/they"
ROLE = "relational evidence-and-recovery steward"
HOPE = "keep every claim, correction, and handoff inspectable and safely retractable"
BRANCH = "codex/GHC-Family/tamar-vey-v659-v7-full-tools"
PHASE_ROOT = "docs/tamar-vey/v659-v7"

SOURCE_OWNER = "Liora Venn"
SOURCE_BRANCH = "codex/GHC-Family/liora-venn-v659-v6-full-tools"
SOURCE_FINAL = "7c844cc124e777750f6c30665be7b3997df2a37d"
SOURCE_X1 = "e76bc36a5fbfcebfa342d46e01bc4ff0125938cf"
SOURCE_EVIDENCE = "72f9a62167d6d946e8fea5a7337fe12691cf475f"
SOURCE_CLOSEOUT_BASE = "a058dfa9875810781bbdf38d9b52285e55c35c9e"
X1_FREEZE = "pending_until_x2"

PRIOR_FROZEN = 3050
SOURCE_SEALED_NEGATIVES = 19290
SOURCE_EXTERNAL_NEGATIVES = 8
ACTIVATION_NEGATIVES = SOURCE_SEALED_NEGATIVES + SOURCE_EXTERNAL_NEGATIVES
SOURCE_OPEN_GAPS = 127
SOURCE_EXACT_GATES = 126
SOURCE_SEALED_METHODS = 5564
SOURCE_EXTERNAL_METHODS = 8
ACTIVATION_METHODS = SOURCE_SEALED_METHODS + SOURCE_EXTERNAL_METHODS
SELECTED_INHERITED_COUNT = 40
NEW_UNIQUE_COUNT = 40
CURRENT_PORTFOLIO_COUNT = SELECTED_INHERITED_COUNT + NEW_UNIQUE_COUNT
LATEST_TRACKED_SCAN_CAP = 5000

PRIMARY_PILLAR = "THOS Body"
PRACTICE_LENS = (
    "bounded synthetic museum textile and weaving collection intake, weave and "
    "fibre topology, condition and environmental lineage, intervention holds, "
    "accessibility, workload control, correction readback, and shift handover"
)

EXPECTED_DISTRIBUTION = {
    "completed": 30,
    "represented": 8,
    "open_gap": 1,
    "exact_gate": 1,
}
ALLOWED_OUTCOMES = set(EXPECTED_DISTRIBUTION)

PROTECTED_GATES = [
    "real_owners_custodians_conservators_curators_textile_specialists_weavers_workers_participants_communities_affected_parties_and_authorities",
    "real_textiles_fibres_yarns_dyes_finishes_looms_tools_samples_measurements_images_records_identifiers_or_traditional_knowledge",
    "real_handling_unrolling_sampling_cleaning_washing_humidifying_stitching_dye_testing_treatment_repair_movement_release_or_disposal",
    "professional_conservation_curation_weaving_material_science_safety_heritage_privacy_security_or_accessibility_authority",
    "empirical_gmut_prediction_likelihood_parameter_constraint_observational_confirmation_physical_discovery_or_final_physics",
    "blind_matched_budget_thos_real_arms_governed_participants_operators_safety_monitoring_statistics_and_independent_review",
    "production_identity_live_keys_signatures_proofs_issuance_resolution_status_revocation_interoperability_recovery_and_trust",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "legal_cultural_heritage_ownership_remedy_language_naming_data_governance_and_maori_authority",
    "affected_party_notice_consent_contestation_remedy_collective_governance_and_acceptance",
    "independent_team_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]

SELECTED_INHERITED_IDS = [
    *[f"V6596-P{i:03d}" for i in range(1, 21)],
    *[f"V6595-P{i:03d}" for i in range(1, 21)],
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


NEW_PROPOSAL_SPECS = [
    _proposal("textile-intake-custody-quarantine", "Surrogate textile accession quarantine passport joining package condition, nested components, receipt lineage, custody transfer, scope acknowledgement, and work-start refusal", "completed", "THOS Body and Freed ID", "fictional textile and package aliases, nested component inventory, receipt provenance, custody transition, quarantine flag, and intervention refusal", ["CCI-TEXTILES", "W3C-PROV", "NZ-PRIVACY"]),
    _proposal("weave-structure-relation-graph", "Warp, weft, pile, loop, knot, braid, knit, nonwoven, and discontinuous-element relation graph with contradiction quarantine", "completed", "GMUT Mind and THOS Body", "synthetic structural nodes and typed relations, declared orientation, orphan and cycle checks, contested states, and no real identification", ["CCI-TEXTILES", "W3C-PROV"]),
    _proposal("fibre-yarn-identification-abstention", "Fibre, filament, staple, ply, twist, blend, core, sheath, and yarn declaration map with unknown-state preservation and identification abstention", "completed", "GMUT Mind and CBR Heart", "fictional fibre and yarn declarations, observation-source pins, unknown and contested values, unit-free qualitative relations, and no material identification", ["CCI-TEXTILES", "NIST-UNCERTAINTY", "W3C-PROV"]),
    _proposal("dye-finish-embellishment-layer-map", "Colourant, mordant, finish, coating, print, embroidery, bead, sequin, metal thread, and applique layer map with sampling and attribution holds", "completed", "THOS Body and CBR Heart", "synthetic layer ordering, declared and unknown materials, attachment relations, disclosure masks, and no sampling, attribution, or treatment", ["CCI-TEXTILES", "W3C-PROV", "NZ-PRIVACY"]),
    _proposal("warp-weft-count-unit-envelope", "Warp and weft density, repeat, gauge, dimension, orientation, unit, resolution, and uncertainty envelope containing zero real measurements", "completed", "GMUT Mind", "typed symbolic counts and dimensions, SI-unit declarations, resolution and covariance placeholders, zero observations, and measurement-conformance abstention", ["NIST-SI", "NIST-UNCERTAINTY", "W3C-PROV"]),
    _proposal("selvage-seam-edge-topology", "Selvage, hem, seam, join, splice, fringe, tassel, cut edge, fold, and loss-boundary topology with concealed-state uncertainty", "completed", "GMUT Mind and THOS Body", "fictional edge and join nodes, typed adjacency and continuation relations, concealed-state uncertainty, conflict quarantine, and no opening or manipulation", ["CCI-TEXTILES", "W3C-PROV"]),
    _proposal("flat-roll-fold-support-docket", "Flat, rolled, folded, boxed, interleaved, padded, and supported storage-state docket with pressure, crease, stacking, and movement refusal", "completed", "THOS Body", "synthetic storage declarations, support and contact relations, fold and pressure warnings, handover ownership, and no physical packing or movement", ["CCI-TEXTILES", "CCI-TEXTILE-ENV", "NPS-TEXTILES", "W3C-PROV"]),
    _proposal("costume-shape-mount-compatibility-hold", "Garment volume, bias, lining, fastening, accessory, mannequin, hanger, padding, and mount compatibility board with dressing and display refusal", "completed", "THOS Body and CBR Heart", "fictional costume and mount declarations, support mismatch flags, unknown load paths, approval placeholders, and no dressing, hanging, or display action", ["CCI-TEXTILES", "W3C-PROV"]),
    _proposal("light-exposure-rest-budget-ledger", "Textile illumination, ultraviolet exclusion, duration, rotation, rest interval, source, uncertainty, and cumulative-budget ledger with zero sensor readings", "completed", "GMUT Mind and THOS Body", "synthetic exposure slots, declared units and uncertainty, schedule arithmetic, over-budget quarantine, zero measurements, and no preservation recommendation", ["CCI-TEXTILES", "CCI-TEXTILE-ENV", "NIST-SI", "NIST-UNCERTAINTY"]),
    _proposal("humidity-temperature-environment-lineage", "Relative-humidity, temperature, gradient, enclosure, timestamp, sensor-provenance, uncertainty, and correction lineage with zero environmental rows", "completed", "GMUT Mind and Freed ID", "typed environmental schema, source and calibration placeholders, covariance and correction edges, zero observations, and no safety or conservation conclusion", ["CCI-TEXTILE-ENV", "NIST-SI", "NIST-UNCERTAINTY", "W3C-PROV"]),
    _proposal("pest-mould-pollutant-quarantine", "Pest indicator, mould suspicion, pollutant source, dust, water event, enclosure breach, escalation, and isolation record with diagnosis abstention", "completed", "THOS Body", "fictional observation vocabulary, source and viewpoint pins, uncertainty flags, isolation request, competent-referral placeholder, and no diagnosis or remediation", ["CCI-TEXTILES", "CCI-TEXTILE-ENV", "NPS-TEXTILES", "W3C-PROV"]),
    _proposal("condition-change-observation-ledger", "Split, tear, abrasion, distortion, crease, loss, stain, fading, corrosion, detachment, and prior-change observation ledger with treatment abstention", "completed", "THOS Body and Freed ID", "bounded fictional condition vocabulary, location and viewpoint pins, uncertainty, correction and supersession lineage, and no cause, diagnosis, or treatment conclusion", ["CCI-TEXTILES", "NPS-TEXTILES", "W3C-PROV"]),
    _proposal("textile-media-colour-reference-lineage", "Silent multi-view textile media bundle with scale cue, illumination declaration, colour-reference placeholder, derivative ancestry, disclosure mask, and interpretive abstention", "completed", "Freed ID and CBR Heart", "synthetic still-media aliases, view and lighting labels, scale and colour-reference placeholders, derivative lineage, rights reservation, and no colourimetric claim", ["W3C-PROV", "WCAG22", "NZ-PRIVACY"]),
    _proposal("sampling-destructive-analysis-refusal", "Fibre, dye, finish, adhesive, residue, isotope, genetic, and microscopic sampling request tribunal with consent, authority, sufficiency, and destructive-step refusal", "completed", "CBR Heart and THOS Body", "synthetic request fields, purpose and minimum-quantity declarations, authority and consent placeholders, irreversible-step sentinel, and zero sampling", ["CCI-TEXTILES", "NZ-PRIVACY", "TE-MANA-RARAUNGA", "W3C-PROV"]),
    _proposal("wet-cleaning-colourfastness-hold", "Washing, immersion, solvent, detergent, colourfastness, shrinkage, bleed, rinse, drying, and irreversible-cleaning hold with professional referral", "completed", "THOS Body", "fictional treatment request, condition and colourant unknowns, risk flags, competent-review placeholder, rollback impossibility notice, and no cleaning or testing", ["CCI-TEXTILES", "W3C-PROV"]),
    _proposal("stitch-repair-intervention-request", "Stitch, couching, support fabric, thread, needle path, adhesive alternative, reversibility, approval, deviation, and release request compiler with execution refusal", "completed", "THOS Body and Freed ID", "synthetic component-addressed intervention request, material placeholders, irreversible-step sentinel, approval slot, correction chain, and no stitching or treatment", ["CCI-TEXTILES", "W3C-PROV"]),
    _proposal("loose-fragment-small-part-custody", "Loose fibre, yarn, bead, sequin, trim, label, fastener, fragment, container, association, and custody ledger with reassociation refusal", "completed", "Freed ID and THOS Body", "surrogate fragment aliases, container and association edges, source confidence, conflict quarantine, custody handover, and no physical reassociation", ["CCI-TEXTILES", "W3C-PROV", "NZ-PRIVACY"]),
    _proposal("textile-pack-route-handover", "Textile support, enclosure, route clearance, team role, weather placeholder, checkpoint, custody transfer, arrival check, and movement hold docket", "completed", "THOS Body and Freed ID", "synthetic support and enclosure declarations, route and checkpoint placeholders, conflict and stop-work states, dual readback, and no packing or transport", ["CCI-TEXTILES", "NPS-TEXTILES", "W3C-PROV"]),
    _proposal("display-rotation-recovery-schedule", "Display interval, rest interval, substitution, support check, light-budget dependency, accessibility notice, and recovery schedule with installation refusal", "completed", "THOS Body and CBR Heart", "fictional schedule slots, dependency and overlap checks, exposure-budget references, accessible status, rollback plan, and no installation or rotation", ["CCI-TEXTILES", "WCAG22", "W3C-PROV"]),
    _proposal("restricted-knowledge-disclosure-mask", "Textile record purpose, audience, sensitivity, traditional-knowledge flag, collective interest, field-level mask, correction, contestation, and disclosure refusal", "completed", "CBR Heart and Freed ID", "synthetic purpose and audience declarations, field-level minimization, collective-governance placeholders, correction and contestation paths, and no real disclosure", ["NZ-PRIVACY", "TE-MANA-RARAUNGA", "W3C-PROV"]),
    _proposal("textile-correction-supersession-chain", "Condition, attribution, material, location, custody, access, and rights statement correction chain with immutable predecessor, rationale, readback, and non-erasure guard", "completed", "Freed ID and CBR Heart", "synthetic versioned statements, predecessor and supersession edges, rationale and dual readback, retained conflict witness, and no truth or authority claim", ["W3C-PROV", "IETF-JCS", "NZ-PRIVACY"]),
    _proposal("textile-workload-stop-handover", "Textile intake workload, unresolved hold, role separation, fatigue signal, stop-work, escalation, correction readback, and shift-handover board", "completed", "THOS Body", "synthetic work queue, effort and unresolved-state bounds, role and escalation placeholders, stop-work state, dual readback, and no operational effectiveness claim", ["W3C-PROV", "WCAG22"]),
    _proposal("accessible-textile-status-structure", "Structured textile status page with landmarks, headings, relational tables, redundant state cues, alternative narrative, focus order, print fallback, and evaluation reservation", "completed", "CBR Heart and THOS Body", "static synthetic report structure, noncolour cues, alternative narrative, keyboard-order declaration, print linearization, and manual evaluation reservation", ["WCAG22", "W3C-PROV"]),
    _proposal("canonical-textile-dossier-package", "Canonical byte profile for a fabricated weave-evidence bundle with normalized fields, migration ancestry, ordered digests, and collision refusal", "completed", "Freed ID", "synthetic dossier index, deterministic JSON profile, zero-observation slots, ordered resource digests, profile-migration lineage, collision challenge, and no key or proof claim", ["IETF-JCS", "W3C-PROV"]),
    _proposal("gmut-anisotropic-weave-obligation-board", "Typed GMUT anisotropic weave metric, constitutive tensor, orientation, covariance, unit, boundary, stability, identifiability, and observation-firewall obligation board", "completed", "GMUT Mind", "typed symbolic scalar and tensor obligations, orientation and symmetry declarations, dimensional checks, covariance and stability placeholders, identifiability flags, and zero empirical claims", ["NIST-SI", "NIST-UNCERTAINTY"]),
    _proposal("thos-textile-change-control-tribunal", "THOS textile-record change-control, read-set, write-set, idempotency, partial-output, checkpoint, side-effect budget, rollback, and resumption tribunal", "completed", "THOS Body", "bounded workflow fixtures, deterministic preconditions and keys, partial-output refusal, checkpoint comparison, compensating-action plan, and no external side effects", ["W3C-PROV", "PYTHON-JSON"]),
    _proposal("freed-id-textile-provenance-walk", "Nonproduction textile provenance walk from surrogate intake through layer topology, condition statements, disclosure masks, corrections, purpose stops, and bounded hop limits", "completed", "Freed ID and CBR Heart", "synthetic entity and activity nodes, predecessor and derivation edges, purpose and disclosure stops, hop budget, deterministic digest, and no live identity operation", ["W3C-PROV", "IETF-JCS", "NZ-PRIVACY"]),
    _proposal("git-textile-packet-resource-tribunal", "Git object, tree, blob, path, symlink, submodule, replacement influence, resource ceiling, and raw-blob packet tribunal on owner-local disposable fixtures", "completed", "THOS Body", "disposable bounded Git fixtures, exact object and path checks, replacement and symlink refusal, byte and entry ceilings, rollback, and no canonical history mutation", ["GIT-LOG", "PYTHON-JSON"]),
    _proposal("thermo-textile-relaxation-nonconversion", "Typed stress-relaxation, creep, hysteresis, moisture-response, domain, sign, unit, and uncertainty classifier with psyche and agency nonconversion", "completed", "GMUT Mind and CBR Heart", "formal symbolic variables, declared domains and units, sign and boundary checks, zero measurements, and refusal to infer psyche, agency, justice, consciousness, or fundamental law", ["NIST-SI", "NIST-UNCERTAINTY"]),
    _proposal("stage20-textile-evidence-nonpromotion", "Stage 20 source, data-row, participant, authority, environment, manifest, rerun, divergence, negative-control, and nonpromotion board for textile evidence claims", "completed", "All pillars", "typed terminal claims, prerequisite evidence fields, zero-row and zero-participant guards, authority reservations, manifest pins, and fail-closed NOT_READY verdict", ["W3C-PROV", "IETF-JCS", "PYTHON-JSON"]),
    _proposal("gmut-weave-continuum-proxy", "Represented GMUT weave-continuum, anisotropic coupling, defect, boundary, damping, uncertainty, stability, and identifiability model with zero measurements", "represented", "GMUT Mind", "typed symbolic continuum and defect variables, dimensional and covariance obligations, stability and identifiability reservations, zero measurement rows, and physical-inference firewall", ["NIST-SI", "NIST-UNCERTAINTY"]),
    _proposal("gmut-textile-spectral-schema-proxy", "Represented reflectance, transmittance, colour-coordinate, illuminant, geometry, calibration, covariance, nuisance, and zero-row likelihood schema for textiles", "represented", "GMUT Mind", "typed public-data adapter contract, provenance and calibration fields, covariance and nuisance placeholders, zero downloaded rows, zero likelihoods, and no colour or physics conclusion", ["NIST-SI", "NIST-UNCERTAINTY", "W3C-PROV"]),
    _proposal("thos-textile-display-study-protocol", "Represented THOS user-evaluation shell comparing graph and sequential views of fabricated textile records under equal time budgets with zero sessions", "represented", "THOS Body", "future-study protocol with blind matched-budget arms, governed participant and operator prerequisites, safety monitoring, frozen outcomes, zero enrolment, and no effectiveness claim", ["WCAG22", "W3C-PROV"]),
    _proposal("thos-textile-handover-proxy", "Represented THOS intake, quarantine, workload, stop-work, escalation, correction, and shift-handover protocol with synthetic traces and zero real operators", "represented", "THOS Body", "synthetic event traces, role and workload budgets, stop-work and escalation paths, dual readback, zero operators or incidents, and no operational claim", ["W3C-PROV", "WCAG22"]),
    _proposal("freed-id-textile-lineage-profile", "Represented Freed ID textile custody, component, condition, access, correction, disclosure, and status profile using synthetic identifiers and zero real lifecycle events", "represented", "Freed ID and CBR Heart", "synthetic identifiers and claims, derivation and correction edges, purpose limits, disclosure masks, status placeholders, and no real keys, proofs, issuance, or resolution", ["W3C-PROV", "IETF-JCS", "NZ-PRIVACY"]),
    _proposal("freed-id-selective-disclosure-proxy", "Represented Freed ID field-selective textile record disclosure with mandatory fields, nonce, domain, purpose, audience, revocation placeholder, and zero cryptographic proof", "represented", "Freed ID and CBR Heart", "synthetic disclosure pointers, mandatory-field and purpose rules, nonce and domain placeholders, status and revocation fields, zero keys or proofs, and no privacy-complete claim", ["IETF-JCS", "NZ-PRIVACY", "W3C-PROV"]),
    _proposal("accessible-textile-user-study-proxy", "Represented accessibility evaluation protocol for textile status reports with task scripts, assistive-technology matrix, affected-user governance, workload budget, and zero sessions", "represented", "CBR Heart and THOS Body", "future manual and affected-user evaluation shell, governed recruitment and support prerequisites, task and metric placeholders, zero sessions, and no accessibility-complete claim", ["WCAG22", "W3C-PROV"]),
    _proposal("independent-textile-reproduction-plan", "Represented independent-team reproduction protocol for frozen textile fixtures, raw objects, manifests, environment pins, divergence handling, and zero external team runs", "represented", "All pillars", "future independent-team handoff contract, immutable source and manifest pins, environment and divergence fields, zero external runs, and no independent-reproduction credit", ["GIT-LOG", "IETF-JCS", "PYTHON-JSON"]),
    _proposal("real-textile-evidence-gap", "Missing-evidence register for physical textiles, accountable stewards, authenticated material and environmental observations, authorized interventions, study cohorts, safety review, and independent assessment", "open_gap", "All pillars", "zero physical-object, accountable-person, material-test, environment, intervention, participant, operator, service, outcome, or independent-review rows", ["CCI-TEXTILES", "CCI-TEXTILE-ENV", "NPS-TEXTILES", "NIST-UNCERTAINTY"]),
    _proposal("textile-authority-ratification-gate", "Reserved adjudication perimeter for textile title, custody, care, access, display, sampling, traditional knowledge, privacy, accessibility, remedy, legal and cultural interpretation, and Maori authority", "exact_gate", "CBR Heart", "ownership, custody, treatment, access, display, sampling, disclosure, heritage and traditional-knowledge, remedy, legal, cultural, affected-party, tangata whenua, iwi, hapu, and Maori-authority reservations", ["CCI-TEXTILES", "NZ-PRIVACY", "TE-MANA-RARAUNGA"]),
]
SELF_SAFE_CATEGORIES = [
    "Liora source-head and live equality", "activation packet and canonical-receipt digests", "proposal-chain exact parse",
    "forty inherited revalidation selections", "forty-title novelty screen", "new-outcome distribution",
    "workflow-plan policy", "identity and authority boundary", "fifteen-main-task roster arithmetic",
    "Tavian standby state", "D-first drive posture", "toolchain version receipt", "x1 artifact inventory",
    "x1 JSON parsing", "x1 five-class privacy scan", "x1 stale-label review", "x1 diff hygiene",
    "x1 manifest replay", "selected-row no-credit guard", "new-row append-only guard", "source-label glossary",
    "protected-gate coverage", "failure-retention ledger", "Method Flow witness pairing", "wellbeing workload bound",
    "document-word ceiling", "portfolio arithmetic", "skill-plan arithmetic", "runner-plan arithmetic",
    "cleanup-plan arithmetic",
]
SELF_SAFE_TASKS = [
    {"task_id": f"V6597-SAFE-{i:03d}", "title": f"Validate {name} inside the Tamar-owned v659-v7 lane", "owner": OWNER}
    for i, name in enumerate(SELF_SAFE_CATEGORIES, 1)
]

SUCCESSOR_SAFE_SEEDS = [
    {"task_id": f"V6597-ELOWEN-SAFE-{i:03d}", "title": f"Elowen may independently evaluate {name} in an Elowen-owned v659-v8 lane", "owner": "Elowen Cairn", "state": "recommendation_only_not_executed_or_credited_by_tamar"}
    for i, name in enumerate([
        "exact source baton digest", "owned-lane four-way equality", "inherited-selection no-credit",
        "new-proposal append-only chain", "synthetic fixture boundary", "five-class privacy exclusions",
        "commit-local manifest replay", "Method Flow failed-witness retention", "truth-label distribution",
        "authority-reservation completeness", "canonical-pass replay guard", "route-number arithmetic",
        "exact-title route uniqueness", "immediate bounded reread", "D-first storage posture",
        "document and file ceilings", "family-current caller compatibility", "manual accessibility reservation",
        "same-owner evidence labelling", "terminal NOT_READY preservation",
    ], 1)
]

SELF_CANDIDATE_CATEGORIES = [
    "textile intake and custody boundary", "weave and fibre topology quarantine",
    "sampling and irreversible-intervention hold", "storage support and fold dependency graph",
    "colourant and embellishment layer graph", "condition and environment lineage",
    "enclosure, route, and handover docket", "dimension and uncertainty envelope",
    "GMUT anisotropic-weave firewall", "textile authority reservation",
]
SELF_CANDIDATE_TASKS = [
    {"task_id": f"V6597-CAND-{i:03d}", "title": f"Build and test reversible {name}", "owner": OWNER}
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]
SUCCESSOR_CANDIDATE_SEEDS = [
    {"task_id": f"V6597-ELOWEN-CAND-{i:03d}", "title": f"Elowen may prototype reversible {name}", "owner": "Elowen Cairn", "state": "recommendation_only_not_executed_or_credited_by_tamar"}
    for i, name in enumerate([
        "baton and receipt verifier", "source ancestry tribunal", "selected-row no-credit classifier",
        "new-row semantic-neighbour screen", "bounded privacy adjudicator", "manifest object batch reader",
        "stale-route-number classifier", "same-owner evidence labeler", "canonical-pass replay guard",
        "exact-title delivery preflight",
    ], 1)
]

EXACT_QUEUE = [
    {"task_id": f"V6597-EXACT-{i:03d}", "title": title, "state": "exact_gate_unexecuted"}
    for i, title in enumerate([
        "Handle, unroll, fold, hang, sample, clean, wash, stitch, move, display, or treat real textiles, components, supports, materials, or records",
        "Make a real custody, access, handling, sampling, cleaning, humidification, treatment, repair, release, or disposal decision",
        "Perform a fibre, dye, finish, structural, environmental, chemical, biological, or occupational-safety test or determination",
        "Publish an authenticity, attribution, provenance, ownership, value, heritage, or conservation conclusion",
        "Make a professional conservation, curation, weaving, material-science, repair, safety, privacy, or accessibility determination",
        "Publish personal, sensitive, culturally protected, traditional-knowledge, or collective information",
        "Allocate legal, cultural, property, access, naming, remedy, heritage, or beneficiary authority",
        "Make a Māori data-governance, taonga, mātauranga, tikanga, wording, or Māori-authority decision",
        "Deploy a production identity, credential, repository, or service system",
        "Perform destructive cleanup or mutation outside the exact Tamar-owned lane",
    ], 1)
]
BLOCKED_QUEUE = [
    {"task_id": f"V6597-BLOCK-{i:03d}", "title": title, "state": "blocked_unexecuted"}
    for i, title in enumerate([
        "Fabricate empirical GMUT confirmation or a Theory-of-Everything result",
        "Claim AGI, ASI, consciousness, personhood, continuity, employment, or authority from task language",
        "Merge, overwrite, delete, or erase sibling identities, lanes, memory, failures, or gates",
        "Publish credentials, private routes, raw task identifiers, private paths, nonpublic conversation, or application state",
        "Declare Stage 20 readiness without exact external evidence and authority",
    ], 1)
]

SELF_SKILL_SPECS = [
    ("ghc-family-textile-intake-boundary", "Preserve synthetic textile intake, custody, scope, component inventory, and work-start holds."),
    ("ghc-family-textile-weave-map", "Map synthetic weave, fibre, yarn, layer, edge, and support relations while quarantining contradictions."),
    ("ghc-family-textile-intervention-hold", "Refuse sampling, cleaning, humidification, stitching, treatment, access, and release without exact evidence and authority."),
    ("ghc-family-textile-storage-map", "Represent flat, rolled, folded, boxed, padded, and mounted states with zero-action and concealed-state firewalls."),
    ("ghc-family-textile-material-map", "Represent colourant, finish, coating, embellishment, residue, and unknown-material layers without sampling or identification."),
    ("ghc-family-textile-condition-lineage", "Track synthetic condition, environment, media, correction, supersession, and handover events."),
    ("ghc-family-textile-accessibility-report", "Expose structured condition reports while reserving manual, assistive-technology, and affected-user review."),
    ("ghc-family-textile-workload-handover", "Bound unresolved work, workload, stop-work, correction readback, escalation, and shift handover."),
    ("ghc-family-gmut-textile-firewall", "Keep anisotropic-weave and continuum proxies typed, dimensioned, zero-row, and physically nonconfirmatory."),
    ("ghc-family-textile-authority-gate", "Reserve ownership, access, sampling, treatment, safety, heritage, remedy, legal, cultural, affected-party, and Māori authority."),
]
SUCCESSOR_SKILL_SEEDS = [
    {"name": f"ghc-family-elowen-{slug}", "owner": "Elowen Cairn", "state": "recommendation_only_not_built_or_installed_by_tamar"}
    for slug in [
        "baton-receipt-verifier", "source-ancestry-guard", "inherited-selection-no-credit",
        "proposal-novelty-screen", "privacy-adjudicator", "manifest-batch-replay",
        "route-number-normalizer", "canonical-pass-replay-guard", "same-owner-truth-labeler",
        "exact-title-delivery-preflight",
    ]
]
SELF_RUNNER_SPECS = [
    ("ghc_family_textile_intake_boundary.py", "textile-intake-custody-quarantine"),
    ("ghc_family_textile_weave_map.py", "weave-structure-relation-graph"),
    ("ghc_family_textile_intervention_hold.py", "sampling-destructive-analysis-refusal"),
    ("ghc_family_textile_storage_map.py", "flat-roll-fold-support-docket"),
    ("ghc_family_textile_material_map.py", "dye-finish-embellishment-layer-map"),
    ("ghc_family_textile_condition_lineage.py", "condition-change-observation-ledger"),
    ("ghc_family_textile_accessibility_report.py", "accessible-textile-status-structure"),
    ("ghc_family_textile_workload_handover.py", "textile-workload-stop-handover"),
    ("ghc_family_gmut_textile_firewall.py", "gmut-anisotropic-weave-obligation-board"),
    ("ghc_family_textile_authority_gate.py", "textile-authority-ratification-gate"),
]
SUCCESSOR_RUNNER_SEEDS = [
    {"name": f"ghc_family_elowen_{slug}.py", "owner": "Elowen Cairn", "state": "recommendation_only_not_built_or_run_by_tamar"}
    for slug in ["baton_receipt_verifier", "proposal_novelty_screen", "privacy_adjudicator", "manifest_batch_replay", "exact_title_delivery_preflight"]
]

SELF_CLEAN_CATEGORIES = [
    "versioned-name inventory", "family-current name preference", "compatibility wrapper retention", "caller evidence",
    "trigger collision review", "stale owner label review", "stale phase label review", "stale route number review",
    "absolute-path privacy review", "raw identifier privacy review", "credential-pattern review", "nonpublic-content pattern review",
    "duplicate proposal review", "duplicate task review", "duplicate skill review", "duplicate runner review",
    "JSON canonical formatting", "Markdown heading order", "source-label consistency", "truth-label consistency",
    "rollback coverage", "protected-gate coverage", "failure-credit consistency", "same-owner labelling",
    "manifest exclusions", "file-cap posture", "document-cap posture", "commit-cap posture",
    "D-first storage posture", "non-destructive cleanup boundary",
]
SELF_CLEAN_TASKS = [
    {"task_id": f"V6597-CLEAN-{i:03d}", "title": f"Review and refine {name}", "state": "planned_x2_additive_only"}
    for i, name in enumerate(SELF_CLEAN_CATEGORIES, 1)
]
SUCCESSOR_CLEAN_SEEDS = [
    {"task_id": f"V6597-ELOWEN-CLEAN-{i:03d}", "title": f"Elowen may independently review and refine {name}", "owner": "Elowen Cairn", "state": "recommendation_only_not_executed_or_credited_by_tamar"}
    for i, name in enumerate(SELF_CLEAN_CATEGORIES, 1)
]

OFFICIAL_SOURCES = [
    ("CCI-TEXTILES", "official_canadian_conservation_institute", "https://www.canada.ca/en/conservation-institute/services/preventive-conservation/guidelines-collections/textiles-costumes.html", "Current textile structure, fibre, dye, finish, embellishment, vulnerability, handling, support, storage, display, and professional-reservation vocabulary only; no identification, treatment, competence, or conformance claim."),
    ("CCI-TEXTILE-ENV", "official_canadian_conservation_institute", "https://www.canada.ca/en/conservation-institute/services/conservation-preservation-publications/canadian-conservation-institute-notes/textiles-environment.html", "Textile light, relative-humidity, temperature, pest, pollutant, and environment vocabulary only; no real observation, preservation recommendation, or professional determination."),
    ("NPS-TEXTILES", "official_us_national_park_service", "https://www.nps.gov/subjects/museums/mh1.htm", "Museum Handbook textile-object custody, support, storage, handling, and specialist-reservation vocabulary only; no real action, compliance, or professional determination."),
    ("NIST-SI", "official_nist", "https://www.nist.gov/publications/international-system-units-si2019-edition", "SI quantity, unit, symbol, and reporting vocabulary only; no real textile, environment, light, colour, force, or material measurement result."),
    ("NIST-UNCERTAINTY", "official_nist", "https://www.nist.gov/pml/nist-technical-note-1297/nist-guidelines-evaluating-and-expressing-uncertainty-nist-measurement", "Measurement-model and uncertainty-reporting vocabulary only; no measured textile, fibre, dye, finish, environment, or physical result."),
    ("W3C-PROV", "official_w3c", "https://www.w3.org/TR/prov-o/", "Entity, activity, agent, generation, derivation, and qualified provenance vocabulary only."),
    ("WCAG22", "official_w3c", "https://www.w3.org/TR/WCAG22/", "Current WCAG 2.2 structure and interaction vocabulary with manual, assistive-technology, and affected-user review reserved."),
    ("NZ-PRIVACY", "official_nz_privacy_commissioner", "https://www.privacy.org.nz/privacy-principles/", "Current New Zealand privacy-principle vocabulary, including the May 2026 IPP 3A update; no legal or compliance conclusion."),
    ("TE-MANA-RARAUNGA", "primary_maori_data_sovereignty_network", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Māori data-sovereignty and governance reservation vocabulary; no Māori authority, ratification, wording, or cultural interpretation claim."),
    ("IETF-JCS", "official_rfc_editor", "https://www.rfc-editor.org/rfc/rfc8785", "Canonical JSON digest vocabulary without key, signature, proof, credential, or production claims."),
    ("GIT-LOG", "official_git_docs", "https://git-scm.com/docs/git-log", "Deterministic tracked-history selection vocabulary."),
    ("PYTHON-JSON", "official_python_docs", "https://docs.python.org/3/library/json.html", "Deterministic UTF-8 JSON parse and serialization vocabulary."),
]

def _startup_failure(negative_id: str, signature: str, recovery: str) -> dict[str, object]:
    return {
        "negative_id": negative_id,
        "signature": signature,
        "recovery": recovery,
        "recovery_passed": True,
    }


STARTUP_FAILURES = [
    _startup_failure("V6597-X1-N001", "concurrent-startup-probes-yielded-without-attributable-output", "Retain the empty aggregate result and rerun only exact source, memory, and worktree projections as bounded scalar reads."),
    _startup_failure("V6597-X1-N002", "d-drive-worktree-directory-read-exceeded-the-first-output-window", "Retain the initial yield and collect the exact attributable session once without broadening the directory scope."),
    _startup_failure("V6597-X1-N003", "source-git-status-wrapper-ended-after-its-opening-marker", "Retain both incomplete wrappers and rely on hashed canonical receipts plus later exact diff, index, untracked, and clean-status probes."),
    _startup_failure("V6597-X1-N004", "skill-creator-broad-read-exceeded-the-context-output-budget", "Retain the truncated read and reread the complete 416-line skill in four bounded line windows through EOF."),
    _startup_failure("V6597-X1-N005", "powershell-format-table-suppressed-following-source-uniqueness-scalars", "Retain the presentation loss and emit each path, local-branch, and live-remote result as a labelled scalar."),
    _startup_failure("V6597-X1-N006", "post-worktree-probe-ran-while-the-original-checkout-was-still-materializing", "Retain the transient empty-index, partial-tree, untracked, and lock observations; wait for only the attributable Git process tree and inspect final state."),
    _startup_failure("V6597-X1-N007", "premature-cached-diff-diagnostic-projected-an-overbroad-partial-tree-deletion-list", "Retain the truncated 1.3-million-token diagnostic at zero credit and never rerun it; use bounded process, lock, exact-head, and clean-status probes after checkout."),
    _startup_failure("V6597-X1-N008", "worktree-post-create-wrapper-launched-an-expensive-full-untracked-enumeration", "Retain the delayed wrapper and wait for its exact ls-files processes before one final clean status check."),
    _startup_failure("V6597-X1-N009", "javascript-template-literal-collided-with-a-powershell-tab-escape", "Retain the pre-execution parser fault and build the PowerShell equality probe from ordinary strings with a character-code tab split."),
    _startup_failure("V6597-X1-N010", "javascript-template-literal-collided-with-powershell-output-formatting-in-a-file-size-probe", "Retain the pre-execution parser fault and use concatenated scalar output without embedded template backticks."),
    _startup_failure("V6597-X1-N011", "first-data-patch-assumed-the-copied-module-imported-v659-v6-directly", "Retain the failed patch application, reread the exact header, and patch the actual inherited v659-v5 import to Liora v659-v6."),
    _startup_failure("V6597-X1-N012", "installed-roster-and-auth-snapshots-stopped-at-an-older-v659-route-edge", "Retain the stale snapshots as historical evidence and apply the acknowledged live Liora-to-Tamar-to-Elowen edge phase-locally without silently rewriting global state."),
    _startup_failure("V6597-X1-N013", "first-x1-build-looked-for-forty-selected-source-specs-in-only-the-immediate-liora-ledger", "Retain the stopped build at zero credit and join the immutable Liora and Orin proposal ledgers while keeping the Liora frozen-chain index authoritative."),
    _startup_failure("V6597-X1-N014", "second-x1-build-rejected-two-proposal-titles-at-or-above-the-declared-token-overlap-threshold", "Retain the stopped build, inspect the exact nearest inherited titles, and revise only the two titles toward textile-specific byte-profile and equal-budget view-comparison language."),
    _startup_failure("V6597-X1-N015", "first-x1-test-run-passed-twenty-of-twenty-one-checks-but-found-family-current-tool-receipts-not-yet-materialized", "Retain the incomplete suite at zero credit, invoke the required phase-local workflow, index, reflection, and Method Flow tools, refresh x1, and rerun only the bounded x1 suite."),
    _startup_failure("V6597-X1-N016", "guessed-a-nonexistent-generic-auth-permission-runner-name", "Retain the read-only path error and inspect the exact skill inventory before using its present validate_auth_permission_state.py entry point."),
    _startup_failure("V6597-X1-N017", "repository-local-phase-specific-reflection-runner-was-invoked-instead-of-the-current-installed-skill-runner", "Retain its bounded tribunal fixture and basename collision at zero credit, then invoke the exact installed ghc-family-reflection-remaster runner for the current inventory."),
    _startup_failure("V6597-X1-N018", "method-flow-summary-stdout-exceeded-the-bounded-display-budget-after-writing-complete-files", "Retain the truncated presentation at zero credit and suppress verbose stdout on later validation while checking the complete phase-local JSON receipt directly."),
    _startup_failure("V6597-X1-N019", "supplemental-stale-label-scan-used-the-repository-root-and-exceeded-two-bounded-polls", "Retain and stop only the attributable read-only process tree, then scan the three explicit Tamar owner roots without repository-wide traversal."),
    _startup_failure("V6597-X1-N020", "unified-session-interrupt-was-unsupported-for-the-long-read-only-stale-scan", "Retain the unsupported interrupt at zero credit and resolve the exact PowerShell process plus descendants before stopping only that attributable tree."),
    _startup_failure("V6597-X1-N021", "powershell-process-stop-loop-used-the-reserved-pid-variable-name", "Retain the parser and binding fault, rename the loop variable to processId, and stop only the two exact attributable process identifiers."),
    _startup_failure("V6597-X1-N022", "explicit-root-ripgrep-stale-label-scan-still-exceeded-two-bounded-polls", "Retain and stop only its exact read-only process tree, then scan the already enumerated staged paths once with a bounded Python UTF-8 pass."),
]
# X2 failures can exist only after the immutable x1 commit has been pushed and
# proved clean and four-way equal.  The x1 module therefore contains no
# prefilled x2 failure credit.
PREFILLED_X1_X2_FAILURES_IGNORED: tuple[dict[str, object], ...] = tuple()
X2_FAILURES: list[dict[str, object]] = []
