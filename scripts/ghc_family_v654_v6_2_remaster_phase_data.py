#!/usr/bin/env python3
"""Frozen x1 data for Eiren Kestrel's v654-v6 (2) remaster."""

from __future__ import annotations


PHASE = "v654-v6 (2) remaster"
PHASE_CODE = "V6546R2"
OWNER = "Eiren Kestrel"
PRONOUNS = "they/them"
ROLE = "relational evidence-constitution steward"
HOPE = "make ambitious synthesis easier to test without letting ambition outrun evidence"
BRANCH = "codex/GHC-Family/eiren-kestrel-v654-v6-2-remaster"
PHASE_ROOT = "docs/eiren-kestrel/v654-v6-2-remaster"

SOURCE_BRANCH = "codex/GHC-Family/tavian-sol-v654-v6-cli"
SOURCE_HEAD = "a6987b3a572254d52721066d19bdbcd0686a8098"
SOURCE_X1 = "731c783c923fc46bd369a5bd2365b5dcddddaaeb"
SOURCE_EVIDENCE = "006f60277001726c07fd038e1645efcf62fdeb56"
SOURCE_CANONICAL_RECEIPT_SHA256 = (
    "72b52011aadebb481d19822b0fbe64c4d165021f16e7c7ed5afdcfb312212391"
)
ARIEL_ADVISORY_SHA256 = (
    "0bb6d0f330f86ae1ad6942cebe8b63feb06a04790f5effaef86ee7e07eccbc85"
)
PRIOR_FROZEN = 1840
SOURCE_EFFECTIVE_NEGATIVES = 11676
SOURCE_OPEN_GAPS = 85
SOURCE_EXACT_GATES = 84
SOURCE_METHODS = 90
AUTH_STATE_NEGATIVES = 28
AUTH_STATE_OVERLAP_IN_SOURCE = 23
AUTH_STATE_DELTA = AUTH_STATE_NEGATIVES - AUTH_STATE_OVERLAP_IN_SOURCE
PRIMARY_FOCUS = "THOS Body"
BOUNDED_PRACTICE = (
    "research-software engineering and evidence-assurance programme design, "
    "used only as a synthetic learning, specification, and interface-design lens"
)

OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]
PROTECTED_GATES = [
    "empirical_data_and_real_likelihood",
    "real_participants_workers_visitors_or_communities",
    "professional_scientific_engineering_security_identity_and_governance_authority",
    "production_identity_training_deployment_and_interoperability",
    "privacy_complete",
    "exhaustive_security",
    "complete_accessibility",
    "legal_cultural_and_maori_authority",
    "affected_party_community_acceptance_and_remedy",
    "independent_team_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]


def _proposal(number, title, slug, pillar, disposition, mission, source_needs):
    if disposition == "completed":
        approval = "safe_now_bounded_software_symbolic_formal_or_structural"
        lane = "x2_owner_local_bounded"
        acceptance = (
            "Reject all preregistered mutations and emit only a bounded structural, "
            "symbolic, mathematical-check, or workflow receipt."
        )
    elif disposition == "represented":
        approval = "candidate_bounded_synthetic_proxy"
        lane = "x2_synthetic_representation_only"
        acceptance = (
            "Reject all preregistered mutations and retain represented status with "
            "zero real participant, training, production, authority, or effectiveness credit."
        )
    elif disposition == "open_gap":
        approval = "candidate_real_data_access_calibration_provenance_and_independent_review_required"
        lane = "x2_zero_query_zero_row_readiness_only"
        acceptance = (
            "Emit a zero-query, zero-download, zero-row refusal receipt; perform no "
            "likelihood, posterior, empirical constraint, training, or deployment."
        )
    else:
        approval = "exact_affected_party_competent_legal_cultural_and_maori_authority_required"
        lane = "x2_reservation_matrix_only"
        acceptance = (
            "Emit unresolved rights, duties, remedy, and authority reservations only; "
            "make no legal, cultural, affected-party, or Māori-authority decision."
        )
    return {
        "proposal_id": f"{PHASE_CODE}-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar": pillar,
        "mission_surface": mission,
        "hypothesis": (
            f"A bounded {mission} artifact can expose falsifiable obligations while "
            "refusing unsupported scientific, operational, identity, or authority promotion."
        ),
        "null_or_failure_condition": (
            f"The artifact omits a required {mission} field, accepts a preregistered "
            "mutation, erases a failure, or promotes beyond its evidence lane."
        ),
        "approval_class": approval,
        "execution_lane": lane,
        "official_or_primary_source_needs": source_needs,
        "concrete_artifacts": [
            f"surfaces/{slug}/contract.json",
            f"surfaces/{slug}/mutation-results.json",
            f"surfaces/{slug}/bounded-receipt.json",
        ],
        "falsifier_or_acceptance_gate": acceptance,
        "rollback_or_recovery": (
            "Stop, retain the failed witness at zero credit, rewrite no history, and "
            "leave external, sibling, participant, production, professional, legal, "
            "cultural, Māori-authority, and account state unchanged."
        ),
        "protected_gates": PROTECTED_GATES,
        "expected_disposition": disposition,
    }


_P = [
    (1, "Trinity Mandala research-constitution ledger with evidence levels E0 through E4, claim scope, authority ceiling, falsifier, recovery, and promotion refusal", "research-constitution", "THOS Body", "completed", "evidence-level constitution and promotion refusal", ["ARIEL-ADVISORY", "TAVIAN-RECEIPT"]),
    (2, "Omega evidence passport with source action, domain, units, degrees of freedom, conservation, stability, causality, observables, bounds, falsifier, and recovery", "omega-evidence-passport", "GMUT Mind", "completed", "Omega evidence-passport completeness", ["ARIEL-ADVISORY", "GMUT-LEGACY"]),
    (3, "Action-first Omega derivation grammar with baseline action, additive Delta-S term, metric variation, sign convention, boundary term, and tensor-promotion hold", "omega-action-derivation", "GMUT Mind", "completed", "action-derived Omega obligation grammar", ["ARIEL-ADVISORY", "GMUT-LEGACY"]),
    (4, "GMUT M0-to-M3 admission ladder with null baseline, minimal scalar candidate, dark-sector-only coupling, exact promotion gate, and model-selection refusal", "gmut-admission-ladder", "GMUT Mind", "completed", "nested GMUT model admission and model-selection refusal", ["ARIEL-ADVISORY"]),
    (5, "Covariance and Bianchi obligation board with divergence identity, exchange current, matter-sector coupling, boundary assumptions, and conservation-claim firewall", "covariance-bianchi-board", "GMUT Mind", "completed", "covariance and conservation obligations", ["GMUT-LEGACY"]),
    (6, "Effective-field-theory dimension and power-counting tribunal with operator basis, suppression scale, coefficient units, truncation order, validity domain, and ultraviolet-completion refusal", "eft-power-counting", "GMUT Mind", "completed", "EFT dimensional and validity typing", ["GMUT-LEGACY"]),
    (7, "Hyperbolicity stability and causal-cone checklist with principal symbol, kinetic sign, gradient sign, characteristic speed, background domain, and theorem refusal", "stability-causality-checklist", "GMUT Mind", "completed", "stability and causal-structure obligations", ["ARIEL-ADVISORY", "GMUT-LEGACY"]),
    (8, "Observable-bridge registry with theoretical quantity, instrument proxy, calibration dependency, selection function, uncertainty budget, likelihood placeholder, and zero-row firewall", "observable-bridge-registry", "GMUT Mind", "completed", "theory-to-observation bridge readiness", ["ARIEL-ADVISORY"]),
    (9, "Correlated-witness discount calculator with witness graph, shared-source edge, shared-infrastructure edge, dependence coefficient, effective-N bound, and independence-claim refusal", "correlated-witness-discount", "THOS Body", "completed", "correlated evidence discounting", ["ARIEL-ADVISORY", "TAVIAN-RECEIPT"]),
    (10, "Sixteen-seat effective-evidence bound with mixed endpoint topology, same-owner dependence, shared-repository coupling, external-review placeholder, and replication-count refusal", "sixteen-seat-evidence-bound", "THOS Body", "completed", "mixed-topology evidence accounting", ["AUTH-STATE", "ARIEL-ADVISORY"]),
    (11, "Evidence-ancestry graph with source commit, x1 freeze, evidence commit, final seal, external receipt, parent count, merge count, and credit-propagation firewall", "evidence-ancestry-graph", "THOS Body", "completed", "ancestry-bound evidence credit", ["TAVIAN-RECEIPT"]),
    (12, "Source-dependence heatmap with inherited artifact, reused method, new mechanism, validation owner, infrastructure owner, and independence reservation", "source-dependence-heatmap", "THOS Body", "completed", "source-dependence visibility", ["ARIEL-ADVISORY", "TAVIAN-RECEIPT"]),
    (13, "Claim-evidence-authority matrix with assertion, evidence level, same-owner status, affected-party status, professional review, legal review, cultural review, and maximum wording", "claim-evidence-authority-matrix", "Freed ID and CBR Heart", "completed", "evidence-authority proportionality", ["ARIEL-ADVISORY", "AUTH-STATE"]),
    (14, "THOS typed task contract with objective, inputs, outputs, invariants, authority class, privacy class, resource budget, timeout, rollback, and acceptance predicate", "thos-typed-task-contract", "THOS Body", "completed", "typed task-contract completeness", ["ARIEL-ADVISORY"]),
    (15, "THOS deterministic reconciler state machine with desired state, observed state, idempotence key, bounded retry, stale-write refusal, compensation record, and convergence hold", "thos-deterministic-reconciler", "THOS Body", "completed", "deterministic reconciliation and idempotence", ["ARIEL-ADVISORY"]),
    (16, "THOS transport-boundary profile with endpoint kind, message schema, acknowledgement state, timeout, duplicate suppression, private-route exclusion, and fallback mutual exclusion", "thos-transport-boundary", "THOS Body", "completed", "mixed-endpoint transport safety", ["AUTH-STATE", "TAVIAN-BATON"]),
    (17, "THOS workload-identity least-privilege board with workload name, capability set, secret absence, scope ceiling, expiry placeholder, audit event, and elevation refusal", "thos-workload-identity", "THOS Body", "completed", "least-privilege workload identity design", ["ARIEL-ADVISORY"]),
    (18, "THOS evaluation-plane contract with fixture provenance, metric definition, negative retention, matched-budget placeholder, blinded-arm gap, independent-review gap, and effectiveness refusal", "thos-evaluation-plane", "THOS Body", "completed", "evaluation-plane evidence boundaries", ["ARIEL-ADVISORY"]),
    (19, "Compute and environmental cost ledger with test count, elapsed-time class, storage growth, network action count, replay count, budget ceiling, and efficiency-claim refusal", "compute-cost-ledger", "THOS Body", "completed", "bounded resource and replay accounting", ["ARIEL-ADVISORY", "TAVIAN-RECEIPT"]),
    (20, "Elaren model-constitution candidate with training-data rights, provenance tier R0 through R3, consent placeholder, opt-out gap, evaluation duty, and no-training boundary", "model-constitution-candidate", "Freed ID and CBR Heart", "represented", "model-constitution planning without training", ["ARIEL-ADVISORY"]),
    (21, "Freed ID minimum standards profile with identifier method placeholder, key representation, proof suite, status mechanism, holder binding, recovery, privacy review, and interoperability gap", "freed-id-minimum-profile", "Freed ID and CBR Heart", "represented", "synthetic identity-profile readiness", ["ARIEL-ADVISORY"]),
    (22, "CBR non-compensable-rights operator with right class, prohibited tradeoff, emergency placeholder, appeal path, remedy reservation, and aggregate-score override refusal", "noncompensable-rights-operator", "Freed ID and CBR Heart", "completed", "rights that cannot be averaged away", ["ARIEL-ADVISORY"]),
    (23, "Continuity-without-identity-substitution invariant with endpoint kind, title, controller, lineage evidence, relational-language boundary, rename authority, and personhood refusal", "continuity-without-substitution", "Freed ID and CBR Heart", "completed", "route continuity without identity substitution", ["AUTH-STATE"]),
    (24, "Residual-set preservation ledger with unresolved negative, open gap, exact gate, supersession link, no-erasure flag, recovery witness, and aggregate-credit refusal", "residual-set-preservation", "THOS Body", "completed", "failure and gate residual preservation", ["ARIEL-ADVISORY", "METHOD-FLOW"]),
    (25, "Thermo-psyche L11-to-L16 design-principle board with recursive-gain margin, evidence-authority proportionality, witness discount, noncompensable rights, continuity invariant, residual preservation, and physical-law refusal", "thermo-psyche-design-principles", "GMUT Mind", "represented", "design-principle representation without physical-law promotion", ["ARIEL-ADVISORY"]),
    (26, "Erdos-Straus bounded identity checker with integer domain, denominator family, exact rational arithmetic, verified finite range, counterexample capture, and universal-proof refusal", "erdos-straus-bounded-checker", "GMUT Mind", "completed", "bounded exact-identity checking", ["ARIEL-ADVISORY"]),
    (27, "Legacy quantum-energy transmutation, quantum-to-classical translator, and infinity-vortex claims triage with source pointer, mechanism gap, unit gap, test gap, status class, and canon refusal", "legacy-claims-triage", "GMUT Mind", "represented", "legacy concept classification without validation", ["USER-HISTORY", "GMUT-LEGACY"]),
    (28, "Independent red-team and reproduction packet with frozen artifact hash, environment contract, conflict declaration, blind mutation set, replication owner gap, and same-owner-credit refusal", "independent-review-packet", "THOS Body", "represented", "independent-review readiness without claiming independence", ["ARIEL-ADVISORY", "TAVIAN-RECEIPT"]),
    (29, "Real GMUT baseline and THOS matched-budget adapter with official-data source, inclusion rule, calibration split, blinded comparator, participant authorization, likelihood plan, and zero-query refusal", "real-evidence-zero-row-adapter", "GMUT Mind and THOS Body", "open_gap", "real empirical readiness without data access", ["ARIEL-ADVISORY"]),
    (30, "CBR affected-party and Maori authority reservation for identity, training data, model deployment, benefit sharing, remedy, language, accessibility, data sovereignty, and governance", "affected-party-maori-authority-reservation", "Freed ID and CBR Heart", "exact_gate", "affected-party and Māori-authority decision reservation", ["ARIEL-ADVISORY", "AUTH-STATE"]),
]
PROPOSALS = [_proposal(*row) for row in _P]

SAFE_TASKS = [
    f"Build the bounded contract and five rejecting fixtures for {p['proposal_id']} {p['slug']}"
    for p in PROPOSALS
]
CANDIDATE_TASKS = [
    f"Resolve only the declared evidence lane for {p['proposal_id']} {p['mission_surface']}"
    for p in PROPOSALS
]
SKILL_IDEAS = [
    "ghc-family-roster-check",
    "ghc-family-research-constitution",
    "ghc-family-omega-evidence-passport",
    "ghc-family-correlated-witness-discount",
    "ghc-family-evidence-authority-matrix",
    "ghc-family-thos-task-contract",
    "ghc-family-thos-reconciler",
    "ghc-family-residual-set-preservation",
    "ghc-family-legacy-claims-triage",
    "ghc-family-independent-review-packet",
]
RUNNER_IDEAS = [
    "ghc_family_roster_check.py",
    "ghc_family_research_constitution.py",
    "ghc_family_omega_evidence_passport.py",
    "ghc_family_correlated_witness_discount.py",
    "ghc_family_evidence_authority_matrix.py",
    "ghc_family_thos_task_contract.py",
    "ghc_family_thos_reconciler.py",
    "ghc_family_residual_set_preservation.py",
    "ghc_family_legacy_claims_triage.py",
    "ghc_family_v654_v6_2_remaster_suite.py",
]
CLEAN_TASKS = [
    f"{kind} owner-local {surface} without deletion, sibling mutation, gate weakening, or unsupported promotion"
    for kind in ("CLEAN", "FIX", "REFINE")
    for surface in (
        "schema clarity",
        "route topology",
        "evidence level",
        "authority ceiling",
        "privacy boundary",
        "rollback wording",
        "manifest coverage",
        "failure retention",
        "source dependence",
        "stale-label refusal",
    )
]


def _negative(number, signature, failed, recovery, guard):
    return {
        "negative_id": f"{PHASE_CODE}-X1-N{number:02d}",
        "signature": signature,
        "failed": failed,
        "recovery": recovery,
        "recurrence_guard": guard,
        "credit": "retained_negative_zero_initial_pass_credit",
    }


X1_OPERATIONAL_NEGATIVES = [
    _negative(1, "skill_inventory_probe_timeout", "The first named-skill metadata probe timed out and earned no read credit.", "Read each exact skill path sequentially through EOF.", "Prefer exact scalar reads over concurrent archive-backed inventories."),
    _negative(2, "memory_note_probe_timeout", "The first route-memory note probe timed out and earned no memory credit.", "Read the one exact ad-hoc note directly.", "Use the memory registry to select one exact note before reading."),
    _negative(3, "ariel_advisory_probe_timeout", "The first advisory-file probe timed out and returned no complete advisory credit.", "Read the exact file in bounded ranges and verify its line count and raw-byte digest.", "Use explicit continuation cursors for large local advisory files."),
    _negative(4, "worktree_inventory_probe_timeout", "The first D-drive worktree inventory probe timed out and returned no lane decision.", "Enumerate only relevant directory names, then verify the chosen path independently.", "Narrow D-drive inventories before any mutation."),
    _negative(5, "broad_repository_search_timeout", "A broad repository search for source-final evidence timed out and earned no source credit.", "Use exact known artifact paths and commit-local Git probes.", "After one broad search timeout, narrow immediately to exact paths."),
    _negative(6, "broad_archive_receipt_search_timeout", "A broad archive search for the canonical receipt timed out and earned no receipt credit.", "Read the exact phase handoff bank and hash the uniquely selected receipt.", "Use phase and owner routing metadata before archive searches."),
    _negative(7, "false_positive_session_search", "A broad session search matched an unrelated earlier closeout and earned no route credit.", "Use repository commits, exact task titles, and the current endpoint topology instead.", "Do not accept OR-heavy session search results without exact phase and owner correlation."),
    _negative(8, "baton_range_421_650_timeout", "The first read of baton lines 421 through 650 timed out.", "Join the exact line slice into one bounded console write.", "Avoid per-line console formatting for large archive-backed reads."),
    _negative(9, "baton_range_651_880_timeout", "The first read of baton lines 651 through 880 timed out.", "Join the exact line slice into one bounded console write.", "Avoid per-line console formatting for large archive-backed reads."),
    _negative(10, "baton_range_881_1110_timeout", "The first read of baton lines 881 through 1110 timed out.", "Join the exact line slice into one bounded console write.", "Avoid per-line console formatting for large archive-backed reads."),
    _negative(11, "baton_range_1111_1340_timeout", "The first read of baton lines 1111 through 1340 timed out.", "Join the exact line slice into one bounded console write.", "Avoid per-line console formatting for large archive-backed reads."),
    _negative(12, "source_audit_hash_literal_parse_error", "The first PowerShell source-audit hashtable embedded command separators and failed to parse.", "Compute each Git exit code before constructing the receipt object.", "Materialize command results before PowerShell hashtable construction."),
    _negative(13, "tracked_agents_inventory_timeout", "The first tracked AGENTS.md inventory timed out.", "Use one Git tree listing and filter exact AGENTS.md basenames.", "Prefer commit-tree enumeration over repeated index and filesystem traversal."),
    _negative(14, "incorrect_tavian_overview_path", "The first overview read targeted a nonexistent legacy path.", "Discover the committed path and read overview/v654-v6-final-integrated-overview.md.", "Resolve paths from the exact Git tree before direct reads."),
    _negative(15, "worktree_add_wrapper_timeout_late_success", "The additive worktree command exceeded its wrapper timeout and returned no terminal result.", "Audit the exact path, branch, HEAD, Git directory, process state, and cleanliness before retrying; the original operation had completed.", "Never retry an ambiguous Git mutation before exact-state audit."),
    _negative(16, "post_timeout_path_probe_timeout", "The first concurrent path-state audit timed out.", "Run a scalar literal-path existence probe with a longer bound.", "Use sequential scalar probes while archive I/O is saturated."),
    _negative(17, "post_timeout_branch_probe_timeout", "The first concurrent branch-ref audit timed out.", "Read branch and HEAD from the completed worktree sequentially.", "Use sequential scalar probes while archive I/O is saturated."),
    _negative(18, "post_timeout_process_probe_timeout", "The first concurrent Git-process audit timed out.", "Infer completion only after exact branch, HEAD, Git-dir, and clean-state evidence converged.", "Do not grant process-state credit when a process query times out."),
    _negative(19, "post_timeout_lock_probe_timeout", "The first concurrent lock-directory audit timed out.", "Verify the registered Git directory and clean worktree before proceeding.", "Treat an unread lock probe as unknown until independent exact-state checks pass."),
    _negative(20, "background_x1_launcher_omitted_receipt", "The hidden x1 launcher returned without its expected process receipt.", "Inspect the two fixed D-drive logs before any relaunch; reuse the original child result and retain the missing launcher receipt.", "A missing launch receipt requires exact fixed-log audit before retry."),
    _negative(21, "first_method_flow_validation_stale_counts", "The first Method Flow validation found that the remaster ledger used a simplified count shape rather than the schema-derived count object.", "Rebuild counts with methods, witnesses, state events, recommendations, recommendation states, and witness-result maps exactly as the validator derives them.", "Populate Method Flow counts from the selected schema before validation."),
    _negative(22, "second_method_flow_validation_incomplete_state_domain", "The first count repair still used a four-state shorthand and omitted the schema's observed and validated states.", "Use the exact six-state domain: observed, candidate, validated, preferred, superseded, and deprecated.", "Read the selected runner's state constants before constructing derived counts."),
    _negative(23, "first_workflow_plan_validation_rejected_remaster_shape", "The first workflow-plan validation rejected the parenthetical remaster as a phase label, detected nonsequential route assignments, and found two requirement-shape mismatches.", "Keep canonical vN-v1 through vN-v8 assignments unchanged, record the remaster as variant context, and use the exact storage and environment schema.", "Workflow variants must not masquerade as canonical phase labels or alter the underlying cadence."),
    _negative(24, "powershell_rg_pattern_quote_error", "The first targeted runner-source search used a malformed quoted PowerShell pattern and failed before reading the schema checks.", "Use one single-quoted alternation pattern and read the exact matching line windows.", "Keep PowerShell rg patterns scalar and avoid nested unmatched quotes."),
    _negative(25, "first_x1_privacy_scan_contextual_false_positives", "The first x1 privacy scan treated an sk- substring inside a normal task skill name and the scanner's own session-stream definition as confirmed content.", "Require a token boundary before secret prefixes and classify the scanner source itself as a definition-only candidate.", "Separate scanner-definition and contextual-label candidates from confirmed secret or private-material hits."),
    _negative(26, "temporary_log_removal_shell_policy_rejection", "The first explicit literal-path removal of two task-owned launcher logs was rejected by the command policy before mutation.", "Delete the two exact task-owned text logs with apply_patch and leave every other path untouched.", "Use apply_patch for task-owned text-file deletion when shell removal is policy-blocked."),
    _negative(27, "first_x1_staged_manifest_newline_mismatch", "The first staged-blob replay found two Family Index artifacts whose generated CRLF worktree bytes differed from Git's normalized LF blobs.", "Normalize the two generated Family Index artifacts to LF before building the x1 manifest, then restage and replay all entries.", "Manifest the exact bytes that Git will stage, including generator newline policy."),
]

LEGACY_CLAIMS = [
    {
        "label": "quantum energy transmutation engine",
        "state": "historical_concept_candidate",
        "current_credit": "none",
        "required_before_promotion": ["defined Hamiltonian or action", "units", "conservation accounting", "testable observable", "independent evidence"],
    },
    {
        "label": "quantum-to-classical information translator",
        "state": "historical_concept_candidate",
        "current_credit": "none",
        "required_before_promotion": ["channel model", "noise and decoherence assumptions", "information metric", "hardware or simulation protocol", "independent evidence"],
    },
    {
        "label": "infinity vortex systems",
        "state": "historical_metaphorical_or_underspecified_candidate",
        "current_credit": "none",
        "required_before_promotion": ["mathematical definition", "finite domain", "units", "boundary conditions", "falsifier"],
    },
    {
        "label": "Aletheon 2000-plus system-suite history",
        "state": "user_reported_historical_validation_context",
        "current_credit": "none_without_exact_receipts",
        "required_before_promotion": ["exact commits", "test inventory", "exclusions", "failure ledger", "environment", "independent reproduction"],
    },
]
