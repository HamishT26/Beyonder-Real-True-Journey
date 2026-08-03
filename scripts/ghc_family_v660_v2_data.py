#!/usr/bin/env python3
"""Frozen x1 planning data for Eiren Kestrel v660-v2.

The module inherits stable helper vocabulary from Sylven Arc's immutable
v660-v1 data surface but redeclares every Eiren-owned field. Twenty inherited
rows are references for bounded revalidation only: they are not reappended and
earn no Eiren novelty or completion credit. Only twenty genuinely new rows
extend the frozen proposal chain.
"""

from __future__ import annotations

from ghc_family_v660_v1_data import *  # noqa: F401,F403


PHASE = "v660-v2"
CANONICAL_PHASE = PHASE
PHASE_CODE = "V6602"
OWNER = "Eiren Kestrel"
PRONOUNS = "they/them"
ROLE = "relational provenance-lantern and ambiguity steward"
HOPE = "make every synthetic claim traceable while keeping real stewardship and authority with the people who hold them"
BRANCH = "codex/GHC-Family/eiren-kestrel-v660-v2-full-tools"
PHASE_ROOT = "docs/eiren-kestrel/v660-v2"

SOURCE_OWNER = "Sylven Arc"
SOURCE_BRANCH = "codex/GHC-Family/sylven-arc-v660-v1-full-tools"
SOURCE_TAMAR = "507e78bd8e86bd6f6395302004d89c751344afb0"
SOURCE_X1 = "d18cbd8bc001e51997e0b5c772ad6dddbb5c7c32"
SOURCE_EVIDENCE = "be9af1d659046857877c7cfde2875130228b10e9"
SOURCE_CLOSEOUT = SOURCE_EVIDENCE
SOURCE_FINAL = "718b7282aa5921a405e7576561026f4cd1094e17"
SOURCE_CLOSEOUT_BASE = SOURCE_FINAL
X1_FREEZE = "pending_until_x2"

PRIOR_FROZEN = 3150
SOURCE_SEALED_NEGATIVES = 19924
SOURCE_EXTERNAL_NEGATIVES = 2
ACTIVATION_NEGATIVES = SOURCE_SEALED_NEGATIVES + SOURCE_EXTERNAL_NEGATIVES
ACTIVATION_MESSAGE_NEGATIVE_BASELINE = ACTIVATION_NEGATIVES
SOURCE_OPEN_GAPS = 130
SOURCE_EXACT_GATES = 129
SOURCE_SEALED_METHODS = 6118
SOURCE_EXTERNAL_METHODS = 2
ACTIVATION_METHODS = SOURCE_SEALED_METHODS + SOURCE_EXTERNAL_METHODS
ACTIVATION_MESSAGE_METHOD_BASELINE = ACTIVATION_METHODS
SELECTED_INHERITED_COUNT = 20
NEW_UNIQUE_COUNT = 20
CURRENT_PORTFOLIO_COUNT = SELECTED_INHERITED_COUNT + NEW_UNIQUE_COUNT
LATEST_TRACKED_SCAN_CAP = 5000

PRIMARY_PILLAR = "CBR Heart"
PRACTICE_LENS = (
    "bounded synthetic stained-glass documentation and conservation-planning "
    "records, topology, annotation, provenance, accessibility, workload, and handover stewardship"
)

EXPECTED_DISTRIBUTION = {
    "completed": 14,
    "represented": 4,
    "open_gap": 1,
    "exact_gate": 1,
}
ALLOWED_OUTCOMES = set(EXPECTED_DISTRIBUTION)

PROTECTED_GATES = [
    "real_owners_custodians_conservators_glaziers_building_managers_installers_scaffolders_communities_affected_parties_and_authorities",
    "real_stained_glass_panels_lancets_glass_pieces_paint_cames_tie_bars_frames_protective_glazing_buildings_scaffolds_chemicals_lead_dust_images_records_measurements_identifiers_or_traditional_knowledge",
    "real_access_inspection_handling_removal_lifting_cleaning_sampling_repair_soldering_releading_repainting_glazing_installation_scaffolding_testing_transport_release_or_disposal",
    "professional_stained_glass_conservation_glazing_heritage_building_structural_work_at_height_lead_hazard_privacy_security_or_accessibility_authority",
    "empirical_gmut_prediction_likelihood_parameter_constraint_observational_confirmation_physical_discovery_or_final_physics",
    "blind_matched_budget_thos_real_arms_governed_participants_operators_safety_monitoring_statistics_and_independent_review",
    "production_identity_live_keys_signatures_proofs_issuance_resolution_status_revocation_interoperability_recovery_and_trust",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "legal_cultural_heritage_iconography_donor_bearer_ownership_remedy_language_naming_data_governance_and_maori_authority",
    "affected_party_notice_consent_contestation_takedown_remedy_collective_governance_and_acceptance",
    "independent_team_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]

SELECTED_INHERITED_IDS = [f"V6601-P{i:03d}" for i in range(1, 21)]


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
    _proposal("stained-glass-intake-provenance-passport", "Surrogate stained-glass panel intake passport linking panel, lancet, light, bay, image set, receipt scope, quarantine, and handling-start refusal", "completed", "CBR Heart and Freed ID", "fabricated panel, lancet, light, bay and image-set aliases, receipt provenance, scope acknowledgement, custody transition, quarantine, and handling-start refusal", ["NPS-PB33", "W3C-PROV", "LOC-PREMIS-3"]),
    _proposal("lead-came-topology-graph", "Directed lead-came and glass-piece topology graph with junction incidence, boundary segments, tie-bar placeholders, orphan detection, ambiguity quarantine, and no structural conclusion", "completed", "CBR Heart and GMUT Mind", "synthetic glass-piece, came, junction, boundary and tie-bar nodes, directed incidence, orphan detection, ambiguity quarantine, and no structural conclusion", ["NPS-PB33", "HISTORIC-ENGLAND-STAINED-GLASS", "W3C-PROV"]),
    _proposal("glass-piece-segmentation-register", "Stained-glass piece-map register with polygon surrogate, border-confidence ceiling, painted-detail layer, occlusion flag, contested segmentation, and no material identification", "completed", "CBR Heart and Freed ID", "fabricated polygon regions, border-confidence ceilings, painted-detail layers, occlusion flags, contested segmentation, correction, and no material identification", ["IIIF-PRESENTATION-3", "W3C-ANNOTATION", "NPS-PB33"]),
    _proposal("stained-glass-dual-light-capture-ledger", "Interior and exterior illumination-capture ledger with exposure declaration, viewpoint frame, scale placeholder, derivative lineage, comparison hold, and zero calibrated observations", "completed", "CBR Heart and GMUT Mind", "synthetic interior and exterior capture events, exposure declarations, viewpoint frames, scale placeholders, derivative lineage, comparison holds, and zero calibrated observations", ["IIIF-PRESENTATION-3", "NIST-SI", "NIST-UNCERTAINTY", "NPS-PB33"]),
    _proposal("stained-glass-colour-reference-envelope", "Stained-glass colour-reference and transmittance placeholder envelope with target declaration, profile identifier, unit and uncertainty fields, drift flag, and no colorimetric conclusion", "completed", "GMUT Mind and CBR Heart", "typed target declarations, profile identifiers, unit and uncertainty fields, drift flags, zero measurements, and no colorimetric or transmittance conclusion", ["IIIF-PRESENTATION-3", "NIST-SI", "NIST-UNCERTAINTY"]),
    _proposal("stained-glass-condition-annotation-ledger", "Bitemporal stained-glass condition-annotation ledger retaining crack, bowing, corrosion, deposit, gap, uncertainty, contradiction, correction, and no-diagnosis states", "completed", "CBR Heart and Freed ID", "synthetic transaction and effective times, condition-term assertions, uncertainty, contradiction retention, correction lineage, and no diagnosis or treatment conclusion", ["W3C-ANNOTATION", "LOC-PREMIS-3", "W3C-PROV"]),
    _proposal("stained-glass-fragment-association-lineage", "Fragment, stopgap, replacement, infill, lead-came, panel, storage carrier, association, detachment, substitution, and reassociation-refusal lineage", "completed", "Freed ID and CBR Heart", "synthetic fragment, stopgap, replacement, infill, came, panel and carrier entities, association and detachment events, substitution lineage, contested provenance, and reassociation refusal", ["LOC-PREMIS-3", "W3C-PROV", "NPS-PB33"]),
    _proposal("stained-glass-intervention-planning-machine", "Fail-closed stained-glass intervention-planning state machine with prerequisite evidence, authorization hold, cancellation, checkpoint, partial-output quarantine, and treatment-execution refusal", "completed", "THOS Body and CBR Heart", "owner-local planning prerequisites, authority holds, cancellation and checkpoint states, partial-output quarantine, resume witness, zero external side effects, and treatment-execution refusal", ["LOC-PREMIS-3", "W3C-PROV", "HISTORIC-ENGLAND-STAINED-GLASS", "WORKSAFE-HEIGHTS"]),
    _proposal("stained-glass-iiif-annotation-package", "IIIF stained-glass documentation package with canvas, multi-light image layers, Web Annotations, motivation declarations, region selectors, rights placeholder, and publication refusal", "completed", "CBR Heart and Freed ID", "synthetic IIIF canvases, multi-light image layers, Web Annotations, motivations, selectors, rights placeholders, access reservations, and publication refusal", ["IIIF-PRESENTATION-3", "W3C-ANNOTATION", "WCAG22"]),
    _proposal("stained-glass-documentation-handover", "Two-person synthetic stained-glass documentation handover with unresolved-leaf count, image-set digest, condition-card readback, stop token, acceptance handshake, and zero practitioners", "completed", "THOS Body and CBR Heart", "synthetic documentation events, unresolved-leaf counts, image-set digest, condition-card readback, stop token, acceptance handshake, zero practitioners, and no operational claim", ["W3C-PROV", "LOC-PREMIS-3", "IETF-JCS"]),
    _proposal("stained-glass-noncolour-topology-report", "Noncolour stained-glass topology report with piece and came crosswalk, linear long description, deterministic heading path, print fallback, and manual accessibility hold", "completed", "CBR Heart and THOS Body", "static topology report structure, piece and came crosswalk, redundant noncolour states, linear long description, deterministic headings, print fallback, and manual evaluation reservation", ["WCAG22", "IIIF-PRESENTATION-3", "W3C-ANNOTATION"]),
    _proposal("stained-glass-attribution-assertion-graph", "Stained-glass maker, donor, inscription, iconography, building-context, and date-claim assertion graph with evidence rank, contestation, retraction, and attribution abstention", "completed", "CBR Heart and Freed ID", "synthetic maker, donor, inscription, iconography, context and date assertions, evidence ranks, contestation, retraction, cultural reservation, and attribution abstention", ["NPS-PB33", "W3C-PROV", "NZ-PRIVACY", "LOCAL-CONTEXTS-TK"]),
    _proposal("stained-glass-component-canonicalizer", "Ordinal-independent stained-glass component-graph canonicalizer using normalized typed edges, profile version, panel-root digest, collision quarantine, migration witness, and zero proofs", "completed", "Freed ID", "synthetic graph normalization, sorted typed edges, profile migration, panel-root digest, ambiguity and collision refusal, zero keys or proofs, and no identity claim", ["IETF-JCS", "W3C-PROV"]),
    _proposal("gmut-pane-came-obligation-board", "Typed GMUT pane-came interface obligation board with shell and network fields, boundary conditions, unit checks, covariance placeholders, rank flags, and observation firewall", "completed", "GMUT Mind", "typed symbolic pane-shell and came-network fields, boundary conditions, dimensional checks, covariance placeholders, rank and domain flags, and zero empirical claims", ["NIST-SI", "NIST-UNCERTAINTY"]),
    _proposal("gmut-stained-glass-transmission-proxy", "Represented GMUT stained-glass luminous-transmission and thermo-mechanical proxy with spectral and interface placeholders, zero coefficients, zero likelihood rows, and physical-inference refusal", "represented", "GMUT Mind", "typed symbolic spectral and thermo-mechanical fields, interface placeholders, unit and covariance obligations, zero coefficients or likelihood rows, and physical-inference refusal", ["NIST-SI", "NIST-UNCERTAINTY", "IIIF-PRESENTATION-3"]),
    _proposal("thos-stained-glass-view-trial-proxy", "Counterbalanced comprehension protocol for synthetic lancet dossiers using shuffled clue cards, latency bins, withdrawal boundary, sealed scoring, and zero human observations", "represented", "THOS Body", "future counterbalanced comprehension protocol, randomized synthetic dossier and clue order, preregistered latency and error bins, withdrawal boundary, governed user prerequisites, zero observations, and no effectiveness claim", ["WCAG22", "W3C-PROV"]),
    _proposal("thos-stained-glass-triage-lattice", "Represented THOS condition-card triage lattice tracking frozen queues, contradiction debt, workload ceiling, dual acceptance digest, escalation clock, and zero operators", "represented", "THOS Body", "synthetic condition-card queues, contradiction-debt states, workload ceilings, dual acceptance digest, escalation clock, zero operators, and no operational claim", ["W3C-PROV", "HISTORIC-ENGLAND-STAINED-GLASS", "IETF-JCS"]),
    _proposal("stained-glass-accessibility-evaluation-proxy", "Assistive-use evidence vacancy matrix for synthetic lancet records reserving tactile orientation, speech navigation, high zoom, monochrome print, language support, and affected-user review", "represented", "CBR Heart and THOS Body", "future governed assistive-use evidence matrix, tactile-orientation and speech-navigation reservations, high-zoom and monochrome-print checks, language support, zero sessions, and no conformance claim", ["WCAG22", "IIIF-PRESENTATION-3", "TE-MANA-RARAUNGA"]),
    _proposal("real-stained-glass-evidence-gap", "Zero-row stained-glass evidence escrow requiring authenticated panels, accountable custodians, competent conservators, calibrated imaging, lead and height safety review, authorized interventions, and independent assessment", "open_gap", "All pillars", "zero authenticated physical-panel, accountable-person, calibrated-image, material-test, condition assessment, intervention, lead or height safety review, outcome, or independent-assessment rows", ["NPS-PB33", "WORKSAFE-HEIGHTS", "WORKSAFE-LEAD", "NIST-UNCERTAINTY"]),
    _proposal("stained-glass-empty-chair-authority", "Unoccupied mandate register for depicted ancestors, dedications, inscriptions, sacred motifs, community protocols, correction and removal requests, and Māori decision reservation", "exact_gate", "CBR Heart", "donor, bearer, depicted-person, community, affected-party, traditional-knowledge, consent, mandate, correction, removal, remedy, contested naming, tangata whenua, iwi, hapū, and Māori-authority reservations", ["NZ-PRIVACY", "TE-MANA-RARAUNGA", "LOCAL-CONTEXTS-TK", "W3C-PROV"]),
]

SELF_SAFE_CATEGORIES = [
    "Sylven source-head and fresh equality", "activation and external-receipt digests", "three-thousand-one-hundred-fifty-row proposal-chain parse",
    "twenty inherited selection identities", "twenty-title novelty screen", "new-outcome distribution", "workflow-plan policy", "identity boundary",
    "bounded Sylven-to-Eiren override", "solo and standby boundaries", "D-first posture", "toolchain version receipt", "x1 artifact inventory",
    "x1 JSON parsing", "x1 five-class privacy scan", "x1 stale-label review", "x1 diff hygiene", "x1 manifest replay",
    "selected-row no-credit guard", "new-row append-only guard", "source-label glossary", "protected-gate coverage", "failure-retention ledger",
    "Method Flow witness pairing", "wellbeing workload bound", "document-word ceiling", "portfolio arithmetic", "skill and runner arithmetic",
    "cleanup-plan arithmetic", "no-x2-in-x1 guard",
]
SELF_SAFE_TASKS = [
    {"task_id": f"V6602-SAFE-{i:03d}", "title": f"Validate {name} inside the Eiren-owned v660-v2 lane", "owner": OWNER}
    for i, name in enumerate(SELF_SAFE_CATEGORIES, 1)
]
SUCCESSOR_SAFE_SEEDS: list[dict[str, object]] = []

SELF_CANDIDATE_CATEGORIES = [
    "panel intake and provenance boundary", "came and glass-piece topology quarantine", "dual-light documentation envelope",
    "condition annotation and bitemporal correction", "fragment and replacement lineage", "intervention-planning refusal state machine",
    "IIIF and Web Annotation package", "noncolour topology report", "GMUT pane-came observation firewall", "empty-chair authority circuit",
]
SELF_CANDIDATE_TASKS = [
    {"task_id": f"V6602-CAND-{i:03d}", "title": f"Build and test reversible {name}", "owner": OWNER}
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]
SUCCESSOR_CANDIDATE_SEEDS: list[dict[str, object]] = []

EXACT_QUEUE = [
    {"task_id": f"V6602-EXACT-{i:03d}", "title": title, "state": "exact_gate_unexecuted"}
    for i, title in enumerate([
        "Access, inspect, handle, remove, lift, clean, sample, repair, solder, relead, repaint, glaze, install, scaffold, test, transport, release, or dispose of real stained glass or associated material",
        "Make a real custody, ownership, donor, bearer, attribution, iconography, access, intervention, release, or takedown decision",
        "Perform a structural, glazing, material, lead, dust, chemical, working-at-height, scaffold, fire, occupational, building, or public-safety determination",
        "Publish an authenticity, origin, maker, date, cultural meaning, traditional-knowledge, condition, value, treatment, or safety conclusion",
        "Make a professional stained-glass conservation, glazing, heritage, building, structural, safety, privacy, security, translation, or accessibility determination",
        "Publish personal, sensitive, culturally protected, traditional-knowledge, donor, custodian, worker, visitor, or collective information",
        "Allocate legal, cultural, intellectual-property, donor, bearer, iconography, access, remedy, heritage, or beneficiary authority",
        "Make a Māori data-governance, taonga, mātauranga, tikanga, wording, naming, or Māori-authority decision",
        "Deploy a production identity, signed statement, credential, repository, collection system, or building-control system",
        "Perform destructive cleanup or mutation outside the exact Eiren-owned lane",
    ], 1)
]
BLOCKED_QUEUE = [
    {"task_id": f"V6602-BLOCK-{i:03d}", "title": title, "state": "blocked_unexecuted"}
    for i, title in enumerate([
        "Fabricate empirical GMUT confirmation or a Theory-of-Everything result",
        "Claim AGI, ASI, consciousness, personhood, continuity, employment, qualification, or authority from relational language",
        "Merge, overwrite, delete, or erase sibling identities, lanes, memory, failures, gates, branches, worktrees, or callers",
        "Publish credentials, private routes, raw task identifiers, private paths, nonpublic conversation, session streams, or application state",
        "Declare Stage 20 readiness without exact external evidence and authority",
    ], 1)
]

SELF_SKILL_SPECS = [
    ("ghc-family-stained-glass-intake-boundary", "Preserve synthetic panel intake, custody, scope, component inventory, quarantine, and handling-start holds."),
    ("ghc-family-stained-glass-topology-graph", "Map synthetic glass-piece, came, junction, boundary, tie-bar, orphan, and ambiguity states."),
    ("ghc-family-stained-glass-capture-envelope", "Keep multi-light captures, viewpoints, scales, profiles, units, uncertainty, and zero-observation claims typed."),
    ("ghc-family-stained-glass-condition-ledger", "Represent synthetic condition assertions, uncertainty, contradictions, corrections, and no-diagnosis states."),
    ("ghc-family-stained-glass-intervention-firewall", "Bound planning prerequisites, authorization holds, cancellation, checkpoints, and treatment-execution refusal."),
    ("ghc-family-stained-glass-fragment-lineage", "Track synthetic fragments, replacements, associations, detachments, amendments, and reassociation refusal."),
    ("ghc-family-stained-glass-iiif-report", "Expose IIIF and annotation structure while reserving rights, publication, manual, language, and affected-user review."),
    ("ghc-family-stained-glass-handover", "Bound unresolved documentation, readback, stop, digest, acceptance, workload, and zero-operator states."),
    ("ghc-family-gmut-pane-came-firewall", "Keep pane-came symbolic fields, units, rank, covariance, likelihood, and observation obligations nonempirical."),
    ("ghc-family-stained-glass-authority-circuit", "Reserve donor, bearer, iconography, tradition, privacy, remedy, cultural, affected-party, and Māori authority."),
]
SUCCESSOR_SKILL_SEEDS: list[dict[str, object]] = []
SELF_RUNNER_SPECS = [
    ("ghc_family_stained_glass_intake_boundary.py", "stained-glass-intake-provenance-passport"),
    ("ghc_family_stained_glass_topology_graph.py", "lead-came-topology-graph"),
    ("ghc_family_stained_glass_capture_envelope.py", "stained-glass-dual-light-capture-ledger"),
    ("ghc_family_stained_glass_condition_ledger.py", "stained-glass-condition-annotation-ledger"),
    ("ghc_family_stained_glass_intervention_firewall.py", "stained-glass-intervention-planning-machine"),
    ("ghc_family_stained_glass_fragment_lineage.py", "stained-glass-fragment-association-lineage"),
    ("ghc_family_stained_glass_iiif_report.py", "stained-glass-iiif-annotation-package"),
    ("ghc_family_stained_glass_handover.py", "stained-glass-documentation-handover"),
    ("ghc_family_gmut_pane_came_firewall.py", "gmut-pane-came-obligation-board"),
    ("ghc_family_stained_glass_authority_circuit.py", "stained-glass-empty-chair-authority"),
]
SUCCESSOR_RUNNER_SEEDS: list[dict[str, object]] = []

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
    {"task_id": f"V6602-CLEAN-{i:03d}", "title": f"Review and refine {name}", "state": "planned_x2_additive_only"}
    for i, name in enumerate(SELF_CLEAN_CATEGORIES, 1)
]
SUCCESSOR_CLEAN_SEEDS: list[dict[str, object]] = []

OFFICIAL_SOURCES = [
    ("NPS-PB33", "official_us_national_park_service", "https://home.nps.gov/orgs/1739/upload/preservation-brief-33-stained-leaded-glass.pdf", "Historic stained- and leaded-glass component, documentation, deterioration, and professional-care vocabulary only; no real inspection, diagnosis, treatment, authenticity, ownership, or conformance claim."),
    ("HISTORIC-ENGLAND-STAINED-GLASS", "official_historic_england", "https://historicengland.org.uk/images-books/publications/stained-glass-windows-managing-environmental-deterioration/", "Environmental deterioration, protective glazing, documentation, monitoring, and expert-conservator reservation vocabulary only; no real building, panel, condition, intervention, or safety decision."),
    ("WORKSAFE-HEIGHTS", "official_worksafe_new_zealand", "https://www.worksafe.govt.nz/topic-and-industry/working-at-height/working-at-height-in-nz/", "Working-at-height hazard, planning, competent-person, fall-control, and stop vocabulary only; no real access, scaffold, ladder, lift, workplace, plan, competence, or safety determination."),
    ("WORKSAFE-LEAD", "official_worksafe_new_zealand", "https://www.worksafe.govt.nz/assets/dmsassets/zero/983WKS-2-work-related-health-management-of-lead-based-paint.pdf", "Lead hazard, exposure, containment, competent-person, hygiene, and health-monitoring reservation vocabulary only; no stained-glass procedure, exposure finding, treatment, or safety determination."),
    ("IIIF-PRESENTATION-3", "official_iiif_consortium", "https://iiif.io/api/presentation/3.0/", "Manifest, canvas, annotation-page, image, range, rights, behavior, and accessibility-summary vocabulary only; no live service, image authenticity, rights clearance, interoperability, or conformance claim."),
    ("W3C-ANNOTATION", "official_w3c", "https://www.w3.org/TR/annotation-model/", "Web Annotation body, target, motivation, selector, state, provenance, and lifecycle vocabulary only; no condition diagnosis, attribution, publication authority, or interoperability claim."),
    ("LOC-PREMIS-3", "official_library_of_congress", "https://www.loc.gov/standards/premis/", "Preservation object, event, agent-placeholder, rights, relationship, fixity, and outcome-detail vocabulary only; no real custody, treatment, rights, or preservation decision."),
    ("W3C-PROV", "official_w3c", "https://www.w3.org/TR/prov-o/", "Entity, activity, agent, generation, derivation, revision, invalidation, and qualified-provenance vocabulary only."),
    ("WCAG22", "official_w3c", "https://www.w3.org/TR/WCAG22/", "Web-accessibility structure, text-alternative, noncolour, navigation, status, and interaction vocabulary with manual, assistive-technology, language, and affected-user review reserved."),
    ("NIST-SI", "official_nist", "https://www.nist.gov/publications/international-system-units-si2019-edition", "SI quantity, unit, symbol, and reporting vocabulary only; no real dimension, light, temperature, displacement, load, motion, or physical result."),
    ("NIST-UNCERTAINTY", "official_nist", "https://www.nist.gov/pml/nist-technical-note-1297/nist-guidelines-evaluating-and-expressing-uncertainty-nist-measurement", "Measurement-model and uncertainty-reporting vocabulary only; no measured panel, glass, came, building, light, temperature, or physical result."),
    ("NZ-PRIVACY", "official_nz_privacy_commissioner", "https://www.privacy.org.nz/privacy-principles/", "Current New Zealand privacy-principle vocabulary, including the IPP 3A indirect-collection notification change effective May 2026, only; no legal, compliance, collection, use, disclosure, retention, or remedy conclusion."),
    ("TE-MANA-RARAUNGA", "primary_maori_data_sovereignty_network", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Māori data-sovereignty and governance reservation vocabulary; no Māori authority, ratification, wording, naming, tikanga, mātauranga, or cultural interpretation claim."),
    ("LOCAL-CONTEXTS-TK", "primary_local_contexts", "https://localcontexts.org/labels/traditional-knowledge-labels/", "Community-defined traditional-knowledge access, use, provenance, permission, and authority-reservation context only; no label is selected, authored, displayed, or applied by this phase."),
    ("IETF-JCS", "official_rfc_editor", "https://www.rfc-editor.org/rfc/rfc8785", "Canonical JSON digest vocabulary without key, signature, proof, credential, identity, or production claims."),
    ("GIT-LOG", "official_git_docs", "https://git-scm.com/docs/git-log", "Deterministic tracked-history selection and ancestry vocabulary."),
    ("PYTHON-JSON", "official_python_docs", "https://docs.python.org/3/library/json.html", "Deterministic UTF-8 JSON parse and serialization vocabulary."),
]


def _startup_failure(negative_id: str, signature: str, recovery: str) -> dict[str, object]:
    return {"negative_id": negative_id, "signature": signature, "recovery": recovery, "recovery_passed": True}


STARTUP_FAILURES = [
    _startup_failure("V6602-X1-N001", "skill-inventory-projection-piped-directly-from-a-powershell-foreach-block", "Retain the EmptyPipeElement parser fault and materialize rows before projection or JSON serialization."),
    _startup_failure("V6602-X1-N002", "fresh-remote-probe-used-a-short-branch-name-that-produced-no-attributable-ref-row", "Retain the empty short-name probe and query the exact refs/heads source branch without changing any remote."),
    _startup_failure("V6602-X1-N003", "activation-packet-boundary-convertto-json-serialized-filesystem-metadata-and-overflowed-output", "Retain the oversized metadata projection and cast packet boundary values to explicit scalar strings before bounded serialization."),
    _startup_failure("V6602-X1-N004", "raw-blob-source-verifier-python-stdin-wrapper-returned-no-attributable-output", "Retain the silent wrapper and reduce the verification to exact immutable object and manifest predicates."),
    _startup_failure("V6602-X1-N005", "first-inline-python-source-verifier-had-a-quote-construction-syntax-fault", "Retain the syntax error and avoid quote-heavy inline construction for the source replay."),
    _startup_failure("V6602-X1-N006", "corrected-inline-source-verifier-still-returned-no-attributable-output", "Retain the second silent wrapper and move the bounded replay into an external receipt helper on D drive."),
    _startup_failure("V6602-X1-N007", "per-object-git-subprocess-source-manifest-replay-exceeded-the-bounded-runtime", "Retain the timed-out attempt and replay immutable blobs through one git cat-file batch process."),
    _startup_failure("V6602-X1-N008", "combined-lane-collision-equality-and-drive-wrapper-returned-no-attributable-output", "Retain the silent wrapper and run branch, remote, path, registry, equality, and free-space probes as separate scalars."),
    _startup_failure("V6602-X1-N009", "multi-domain-novelty-screen-exceeded-the-bounded-runtime", "Retain the timeout and parse the frozen chain structurally with bounded domain groups before the exact twenty-title screen."),
    _startup_failure("V6602-X1-N010", "worktree-add-returned-while-the-original-large-checkout-still-held-the-initializing-lock", "Preserve the initializing lock, wait for the original Git process to finish, and never unlock or mutate the partial checkout."),
    _startup_failure("V6602-X1-N011", "combined-post-checkout-cleanliness-wrapper-returned-incomplete-evidence", "Retain the incomplete wrapper and use an explicit porcelain-v2 status receipt after materialization finishes."),
    _startup_failure("V6602-X1-N012", "quote-heavy-rg-inspection-expression-was-misparsed-by-powershell", "Retain the command-construction fault and split the inspection into single-quoted bounded search expressions."),
    _startup_failure("V6602-X1-N013", "novelty-probe-json-output-hit-the-windows-cp1252-maori-character-boundary", "Retain the UnicodeEncodeError and rerun the same read-only probe with Python UTF-8 mode enabled."),
    _startup_failure("V6602-X1-N014", "first-twenty-title-novelty-screen-rejected-three-source-template-shaped-drafts", "Retain the seventeen-pass and three-rejection receipt, replace the matched-trial, generic-accessibility, and empty-chair title shapes with distinct mechanisms, and rerun the exact twenty-title screen."),
    _startup_failure("V6602-X1-N015", "first-workflow-plan-audit-rejected-a-stricter-but-undeclared-codex-route-enum-value", "Retain the 19-of-20 policy receipt, use the validator-declared terminal-gated route enum, and preserve unresolved-next-edge semantics in separate explicit fields before rerunning only the workflow dependency."),
    _startup_failure("V6602-X1-N016", "post-staged-combined-cleanliness-wrapper-returned-incomplete-evidence", "Retain the incomplete wrapper and run unstaged diff, untracked count, and forbidden-path checks as separate scalar commands before committing."),
    _startup_failure("V6602-X1-N017", "separate-powershell-untracked-count-wrapper-returned-no-attributable-output", "Retain the silent wrapper and use a bounded Python subprocess projection over porcelain status for an attributable untracked count."),
]

# X2 failures can exist only after the immutable x1 commit is pushed and proved
# clean and four-way equal.  X1 contains no prefilled x2 failure credit.
PREFILLED_X1_X2_FAILURES_IGNORED: tuple[dict[str, object], ...] = tuple()
X2_FAILURES: list[dict[str, object]] = []
