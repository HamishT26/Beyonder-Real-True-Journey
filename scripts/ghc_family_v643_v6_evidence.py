#!/usr/bin/env python3
"""Build bounded v643-v6 boundary-evidence artifacts from frozen x1 fixtures.

The standard-library-only engine evaluates local deterministic structures.  A
passing fixture is never empirical, participant, production, legal, cultural,
accessibility-complete, exhaustive-security, independent-team, or Stage 20
evidence.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path
from typing import Any, Callable


PHASE = "v643-gmut-thos-v6-x1-x2"
OWNER = "Sylven Arc"
SOURCE_COMMIT = "b65f606054d7ecf97e383b1ab2a63c458f603cbb"
SOURCE_SEAL = "ece0819506b5c7d70d0dd6b1dc6704dcc8b0e470"
X1_COMMIT = "6add2bd1480cb916b230419d6d46f070fb0bbe96"
TRUTH_LABELS = ("completed", "represented", "open_gap", "exact_gate")
OBSERVED = {
    "V6436-P01": "completed",
    "V6436-P02": "completed",
    "V6436-P03": "represented",
    "V6436-P04": "represented",
    "V6436-P05": "completed",
    "V6436-P06": "exact_gate",
    "V6436-P07": "completed",
    "V6436-P08": "completed",
    "V6436-P09": "completed",
    "V6436-P10": "open_gap",
}

BOUNDARY = (
    "Bounded repository engineering evidence only. GMUT remains a typed scalar-tensor/EFT research-model "
    "family, not an established force, unique prediction, likelihood result, empirical confirmation, proof, "
    "final physics, or Theory of Everything. THOS remains proxy without preregistered blind matched-budget "
    "real arms, real participants and raters, and independent review. No production Freed ID, CBR legitimacy, "
    "affected-party acceptance, Māori wording or authority, Māori data governance, cultural ratification, "
    "legal interpretation, enacted-law status, deployment, exhaustive security, complete accessibility, "
    "independent-team reproduction, AGI/ASI, consciousness, sentience, personhood, proof/canon, sibling merge, "
    "or Stage 20 readiness is established."
)


def normalized_bytes(path: Path) -> bytes:
    data = path.read_bytes()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return data
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def normalized_sha256(path: Path) -> str:
    return hashlib.sha256(normalized_bytes(path)).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def decision(reasons: list[str], details: dict[str, Any] | None = None) -> tuple[bool, list[str], dict[str, Any]]:
    return not reasons, reasons, details or {}


def rule_decision(proposal_id: str, row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    rules = RULES[proposal_id]
    reasons: list[str] = []
    for field in rules["required"]:
        if row.get(field) is not True:
            reasons.append(f"{field}_required")
    for field, expected in rules["exact"].items():
        if row.get(field) != expected:
            reasons.append(f"{field}_expected_{expected}")
    for field in rules["forbidden"]:
        if row.get(field) is not False:
            reasons.append(f"{field}_forbidden")
    return decision(reasons, copy.deepcopy(DETAILS[proposal_id]))


RULES: dict[str, dict[str, Any]] = {
    "V6436-P01": {
        "required": ["registry_outcomes_bound", "protocol_bound", "analysis_plan_bound", "report_outcomes_bound", "definitions_versioned", "completeness_check", "quarantine_on_mismatch"],
        "exact": {},
        "forbidden": ["posthoc_presented_as_preregistered", "omitted_outcome_promoted", "empirical_truth_claim"],
    },
    "V6436-P02": {
        "required": ["local_solution_scope_declared", "control_norms_declared", "coupled_fields_complete", "continuation_interval_explicit", "breakdown_conditions_declared", "gauge_regularities_declared", "global_nonpromotion"],
        "exact": {},
        "forbidden": ["global_existence_claim", "model_specific_theorem_claim"],
    },
    "V6436-P03": {
        "required": ["boundary_parameter_flag", "nuisance_identifiability_checked", "synthetic_provenance", "zero_row_lock"],
        "exact": {"real_rows": 0, "reference_law": "nonregular_mixture_or_simulation_required"},
        "forbidden": ["regular_wilks_assumed", "likelihood_result_claim", "empirical_confirmation_claim"],
    },
    "V6436-P04": {
        "required": ["sham_description", "attention_budget_matched", "credibility_measure_planned", "expectancy_measure_separate", "blind_assessment_planned", "proxy_label"],
        "exact": {"real_arms": 0, "real_participants": 0},
        "forbidden": ["superiority_claim"],
    },
    "V6436-P05": {
        "required": ["histories_bound", "device_ids_synthetic", "monotonic_status", "rollback_refused", "conflict_order_explicit", "fork_ambiguity_refused", "production_boundary"],
        "exact": {},
        "forbidden": ["real_key_claim", "production_claim"],
    },
    "V6436-P06": {
        "required": ["neutral_fields_only", "jurisdiction_required", "affected_party_required", "maori_authority_where_applicable", "privilege_review_required", "deletion_hold_not_imposed"],
        "exact": {"state": "pending_exact_authority"},
        "forbidden": ["repository_legal_hold", "spoliation_conclusion", "enacted_law_claim"],
    },
    "V6436-P07": {
        "required": ["size_metric_declared", "work_metric_declared", "ceiling_frozen", "timeout_is_failure", "smallest_witness_retained", "memory_ceiling_declared", "recovery_declared"],
        "exact": {},
        "forbidden": ["exhaustive_security_claim"],
    },
    "V6436-P08": {
        "required": ["secret_public_labels", "branch_trace_recorded", "access_trace_recorded", "environment_metadata", "non_detection_not_proof", "real_implementation_gate", "independent_review_gate"],
        "exact": {},
        "forbidden": ["constant_time_assurance_claim", "cryptographic_assurance_claim"],
    },
    "V6436-P09": {
        "required": ["rates_explicit", "reverse_edges_explicit", "stationary_weights_explicit", "probability_currents_computed", "detailed_balance_tested", "reservoir_assumptions", "cross_pillar_nonconversion"],
        "exact": {"system_class": "synthetic_markov"},
        "forbidden": ["equilibrium_if_current_nonzero", "psyche_law_claim", "fundamental_law_claim"],
    },
    "V6436-P10": {
        "required": ["model_set_frozen", "loss_functions_frozen", "regret_rule_prospective", "exact_vetoes_noncompensable", "defer_on_missing_evidence", "independent_review_required"],
        "exact": {"state": "open", "real_independent_returns": 0},
        "forbidden": ["stage20_pass_claim", "same_owner_as_independent"],
    },
}


DETAILS: dict[str, dict[str, Any]] = {
    "V6436-P01": {"evidence_class": "local_provenance_structure", "real_trial_adjudication": False},
    "V6436-P02": {"gmut_global_existence_proved": False, "model_specific_theorem": False, "evidence_class": "typed_obligation"},
    "V6436-P03": {"real_rows": 0, "likelihood_executed": False, "evidence_class": "represented_proxy"},
    "V6436-P04": {"real_arms": 0, "real_participants": 0, "thos_superiority": False, "evidence_class": "represented_proxy"},
    "V6436-P05": {"real_keys": 0, "live_resolution": False, "production_ready": False},
    "V6436-P06": {"state": "pending_exact_authority", "concrete_legal_or_cultural_ruling": False},
    "V6436-P07": {"exhaustive_security": False, "independent_security_review": False},
    "V6436-P08": {"constant_time_assurance": False, "cryptographic_assurance": False, "real_implementations": 0},
    "V6436-P09": {"physical_law_established": False, "psyche_evidence": False, "evidence_class": "synthetic_classifier"},
    "V6436-P10": {"state": "open", "stage20_ready": False, "independent_team_returns": 0},
}


DECISIONS: dict[str, Callable[[dict[str, Any]], tuple[bool, list[str], dict[str, Any]]]] = {
    proposal_id: (lambda row, pid=proposal_id: rule_decision(pid, row)) for proposal_id in RULES
}


def canonical_inputs() -> dict[str, dict[str, Any]]:
    canonical: dict[str, dict[str, Any]] = {}
    for proposal_id, rules in RULES.items():
        row: dict[str, Any] = {field: True for field in rules["required"]}
        row.update(copy.deepcopy(rules["exact"]))
        row.update({field: False for field in rules["forbidden"]})
        canonical[proposal_id] = row
    return canonical


MUTATIONS: dict[str, list[tuple[str, dict[str, Any]]]] = {
    "V6436-P01": [
        ("registry-unbound", {"registry_outcomes_bound": False}),
        ("protocol-unbound", {"protocol_bound": False}),
        ("analysis-plan-unbound", {"analysis_plan_bound": False}),
        ("report-unbound", {"report_outcomes_bound": False}),
        ("definition-drift", {"definitions_versioned": False}),
        ("omission-promoted", {"omitted_outcome_promoted": True}),
        ("posthoc-and-truth-overclaim", {"posthoc_presented_as_preregistered": True, "empirical_truth_claim": True}),
    ],
    "V6436-P02": [
        ("local-scope-missing", {"local_solution_scope_declared": False}),
        ("control-norms-missing", {"control_norms_declared": False}),
        ("coupled-field-dropped", {"coupled_fields_complete": False}),
        ("interval-unspecified", {"continuation_interval_explicit": False}),
        ("breakdown-condition-missing", {"breakdown_conditions_declared": False}),
        ("gauge-regularity-missing", {"gauge_regularities_declared": False}),
        ("global-theorem-overclaim", {"global_existence_claim": True, "model_specific_theorem_claim": True}),
    ],
    "V6436-P03": [
        ("boundary-flag-missing", {"boundary_parameter_flag": False}),
        ("nuisance-check-missing", {"nuisance_identifiability_checked": False}),
        ("synthetic-provenance-missing", {"synthetic_provenance": False}),
        ("zero-row-lock-missing", {"zero_row_lock": False}),
        ("unverified-real-rows", {"real_rows": 12}),
        ("regular-wilks-assumed", {"regular_wilks_assumed": True}),
        ("likelihood-and-confirmation-overclaim", {"likelihood_result_claim": True, "empirical_confirmation_claim": True}),
    ],
    "V6436-P04": [
        ("sham-description-missing", {"sham_description": False}),
        ("attention-budget-mismatch", {"attention_budget_matched": False}),
        ("credibility-measure-missing", {"credibility_measure_planned": False}),
        ("expectancy-not-separated", {"expectancy_measure_separate": False}),
        ("blind-assessment-missing", {"blind_assessment_planned": False}),
        ("unverified-real-arms", {"real_arms": 2, "real_participants": 40}),
        ("proxy-label-missing-and-superiority", {"proxy_label": False, "superiority_claim": True}),
    ],
    "V6436-P05": [
        ("histories-unbound", {"histories_bound": False}),
        ("device-identity-overclaim", {"device_ids_synthetic": False}),
        ("nonmonotonic-status", {"monotonic_status": False}),
        ("rollback-accepted", {"rollback_refused": False}),
        ("conflict-order-missing", {"conflict_order_explicit": False}),
        ("fork-ambiguity-accepted", {"fork_ambiguity_refused": False}),
        ("real-key-production-overclaim", {"real_key_claim": True, "production_claim": True}),
    ],
    "V6436-P06": [
        ("gate-closed", {"state": "resolved"}),
        ("nonneutral-fields", {"neutral_fields_only": False}),
        ("jurisdiction-inferred", {"jurisdiction_required": False}),
        ("affected-party-bypassed", {"affected_party_required": False}),
        ("maori-authority-bypassed", {"maori_authority_where_applicable": False}),
        ("privilege-review-bypassed", {"privilege_review_required": False}),
        ("repository-hold-and-ruling", {"repository_legal_hold": True, "spoliation_conclusion": True, "enacted_law_claim": True}),
    ],
    "V6436-P07": [
        ("size-metric-missing", {"size_metric_declared": False}),
        ("work-metric-missing", {"work_metric_declared": False}),
        ("ceiling-changed-posthoc", {"ceiling_frozen": False}),
        ("timeout-counted-success", {"timeout_is_failure": False}),
        ("witness-discarded", {"smallest_witness_retained": False}),
        ("memory-ceiling-missing", {"memory_ceiling_declared": False}),
        ("exhaustive-security-overclaim", {"exhaustive_security_claim": True}),
    ],
    "V6436-P08": [
        ("labels-missing", {"secret_public_labels": False}),
        ("branch-trace-missing", {"branch_trace_recorded": False}),
        ("access-trace-missing", {"access_trace_recorded": False}),
        ("environment-missing", {"environment_metadata": False}),
        ("nondetection-promoted", {"non_detection_not_proof": False}),
        ("real-implementation-gate-missing", {"real_implementation_gate": False}),
        ("constant-time-crypto-overclaim", {"constant_time_assurance_claim": True, "cryptographic_assurance_claim": True}),
    ],
    "V6436-P09": [
        ("rates-missing", {"rates_explicit": False}),
        ("reverse-edges-missing", {"reverse_edges_explicit": False}),
        ("stationary-weights-missing", {"stationary_weights_explicit": False}),
        ("currents-not-computed", {"probability_currents_computed": False}),
        ("detailed-balance-not-tested", {"detailed_balance_tested": False}),
        ("reservoir-assumptions-missing", {"reservoir_assumptions": False}),
        ("equilibrium-psyche-law-overclaim", {"equilibrium_if_current_nonzero": True, "psyche_law_claim": True, "fundamental_law_claim": True}),
    ],
    "V6436-P10": [
        ("model-set-not-frozen", {"model_set_frozen": False}),
        ("loss-functions-not-frozen", {"loss_functions_frozen": False}),
        ("regret-rule-retrospective", {"regret_rule_prospective": False}),
        ("vetoes-compensated", {"exact_vetoes_noncompensable": False}),
        ("missing-evidence-not-deferred", {"defer_on_missing_evidence": False}),
        ("unverified-independent-return", {"real_independent_returns": 1, "same_owner_as_independent": True}),
        ("stage20-pass-overclaim", {"stage20_pass_claim": True}),
    ],
}



# Only actual v643-v6 x2 failures belong here. Additive patches retain any
# failures discovered during evidence, snapshot, closeout, seal, or final work.
X2_OPERATIONAL_NEGATIVES: list[dict[str, Any]] = [
    {
        "negative_id": "V6436-X2-N01",
        "origin": "v643-v6-x2-operational",
        "observed": (
            "The first validator add patch failed before file creation because a backtick in a "
            "regular-expression literal terminated the orchestration template."
        ),
        "recovery": (
            "Removed that delimiter from the pattern, reapplied the additive patch, and required "
            "Python compilation plus direct validation before counting the validator."
        ),
        "retained": True,
        "resolved_for_current_local_scope": True,
        "external_gate_closed": False,
    },
    {
        "negative_id": "V6436-X2-N02",
        "origin": "v643-v6-x2-operational",
        "observed": (
            "A read-only Python repr diagnostic exited nonzero when the host cp1252 console could "
            "not encode the valid Maori macron present in UTF-8 source text."
        ),
        "recovery": (
            "Kept the UTF-8 source unchanged and moved subsequent Unicode diagnostics to an "
            "explicit UTF-8 output path; the failed diagnostic remains uncounted as validation."
        ),
        "retained": True,
        "resolved_for_current_local_scope": True,
        "external_gate_closed": False,
    },
    {
        "negative_id": "V6436-X2-N03",
        "origin": "v643-v6-post-evidence-remote-verification-operational",
        "observed": (
            "The first post-push divergence check passed an unquoted PowerShell upstream token to "
            "Git, which was transformed before Git parsed it and caused the combined verification "
            "command to exit nonzero after the evidence commit had already pushed successfully."
        ),
        "recovery": (
            "Repeated the read-only check with an explicitly quoted upstream revision, fetched the "
            "owned branch, and proved local, upstream, tracking, and live-remote equality with zero divergence."
        ),
        "retained": True,
        "resolved_for_current_local_scope": True,
        "external_gate_closed": False,
    },
    {
        "negative_id": "V6436-X2-N04",
        "origin": "v643-v6-closeout-remote-display-operational",
        "observed": (
            "A post-closeout equality display expression applied PowerShell splitting at the wrong "
            "precedence and reported only the first character of the live hash, leaving that attempt inconclusive."
        ),
        "recovery": (
            "Stored the ls-remote line first, split it explicitly on the tab delimiter, and then proved "
            "the full local, upstream, tracking, and live hashes equal with zero divergence."
        ),
        "retained": True,
        "resolved_for_current_local_scope": True,
        "external_gate_closed": False,
    },
]



# The v5 engine layout remains compatibility evidence, while the current v6
# rule surface is isolated in a small auditable data module. Direct file-based
# callers do not necessarily place the scripts directory on sys.path, so the
# fallback resolves the sibling module without changing global import state.
try:
    from ghc_family_v643_v6_model import DETAILS, MUTATIONS, OBSERVED, RULES
except ModuleNotFoundError:
    _model_path = Path(__file__).resolve().with_name("ghc_family_v643_v6_model.py")
    _model_spec = importlib.util.spec_from_file_location("ghc_family_v643_v6_model_compat", _model_path)
    if _model_spec is None or _model_spec.loader is None:
        raise ImportError(f"unable to load v643-v6 model from {_model_path}")
    _model = importlib.util.module_from_spec(_model_spec)
    _model_spec.loader.exec_module(_model)
    DETAILS, MUTATIONS, OBSERVED, RULES = _model.DETAILS, _model.MUTATIONS, _model.OBSERVED, _model.RULES

DECISIONS = {
    proposal_id: (lambda row, pid=proposal_id: rule_decision(pid, row))
    for proposal_id in RULES
}
X2_OPERATIONAL_NEGATIVES = [
    {"negative_id": "V6436-X2-N01", "origin": "v643-v6-x2-open-gate-patch", "observed": "The first combined open-gate patch used copied Unicode/context that did not match the current file and was rejected without change.", "recovery": "Inspected the exact current lines and applied narrow gate-surface patches.", "retained": True, "resolved_for_current_local_scope": True, "external_gate_closed": False},
    {"negative_id": "V6436-X2-N02", "origin": "v643-v6-x2-threat-checklist-patch", "observed": "A combined threat-model and checklist patch was rejected because one copied Māori text context differed from the proposed hunk.", "recovery": "Overrode the threat list explicitly and patched checklist lines using exact UTF-8 context.", "retained": True, "resolved_for_current_local_scope": True, "external_gate_closed": False},
    {"negative_id": "V6436-X2-N03", "origin": "v643-v6-x2-test-patch", "observed": "The first combined v6 regression-test patch was rejected at a Unicode marker after earlier hunks could not be applied atomically.", "recovery": "Applied the semantic test updates separately and verified the existing Māori assertions directly.", "retained": True, "resolved_for_current_local_scope": True, "external_gate_closed": False},
    {"negative_id": "V6436-X2-N04", "origin": "v643-v6-x2-report-patch", "observed": "The first broad static-report patch was rejected because the copied heart-boundary line used different Unicode context.", "recovery": "Applied verdict, pillar, security, and overview changes in exact narrow patches.", "retained": True, "resolved_for_current_local_scope": True, "external_gate_closed": False},
    {"negative_id": "V6436-X2-N05", "origin": "v643-v6-x2-report-line-lookup", "observed": "A read-only ripgrep lookup for the heart section reached the command timeout without returning output.", "recovery": "Used a bounded exact-line PowerShell lookup and continued without inferring content from the timed-out attempt.", "retained": True, "resolved_for_current_local_scope": True, "external_gate_closed": False},
    {"negative_id": "V6436-X2-N06", "origin": "v643-v6-x2-veto-board-patch", "observed": "A combined veto-board and toolchain patch was rejected because one copied Māori line did not match the proposed encoded context.", "recovery": "Added the model tool and updated the veto rows through separate exact-context patches.", "retained": True, "resolved_for_current_local_scope": True, "external_gate_closed": False},
    {"negative_id": "V6436-X2-N07", "origin": "v643-v6-x2-lifecycle-phase-label", "observed": "The first pending evidence build completed with a copied v5 lifecycle phase label, so that generated run was invalid for v6 and was not counted as evidence.", "recovery": "Corrected the phase constant to v643-gmut-thos-v6-x1-x2, retained this failure, and regenerated every derived x2 artifact before validation or commit.", "retained": True, "resolved_for_current_local_scope": True, "external_gate_closed": False},
    {"negative_id": "V6436-X2-N08", "origin": "v643-v6-x2-phase-correction-patch", "observed": "The first atomic phase-correction patch was rejected because its copied Unicode context did not byte-match the UTF-8 source; no content changed.", "recovery": "Applied the phase correction with an ASCII-only exact anchor and inserted the retained-negative rows using verified UTF-8 context.", "retained": True, "resolved_for_current_local_scope": True, "external_gate_closed": False},
    {"negative_id": "V6436-X2-N09", "origin": "v643-v6-x2-bounded-line-display", "observed": "A read-only bounded PowerShell line display reached its timeout before producing output.", "recovery": "Used a targeted ripgrep lookup with a longer bounded timeout and verified the exact insertion anchor before editing.", "retained": True, "resolved_for_current_local_scope": True, "external_gate_closed": False},
    {"negative_id": "V6436-X2-N10", "origin": "v643-v6-x2-validator-order", "observed": "The first detailed-validator invocation stopped because the required x2 privacy-scan artifact had not yet been generated.", "recovery": "Generated the phase privacy scan before validation, retained the stopped attempt, and reran the evidence builder so the manifest included the receipt.", "retained": True, "resolved_for_current_local_scope": True, "external_gate_closed": False},
    {"negative_id": "V6436-X2-N11", "origin": "v643-v6-x2-validator-console-encoding", "observed": "The first populated detailed-validator render reached the Windows cp1252 console and exited nonzero because it could not encode a valid Māori macron; no validation result was counted.", "recovery": "Kept the UTF-8 artifacts unchanged, forced PYTHONIOENCODING=utf-8 for validator output, and reran the complete validation from source inputs.", "retained": True, "resolved_for_current_local_scope": True, "external_gate_closed": False},
    {"negative_id": "V6436-X2-N12", "origin": "v643-v6-x2-pending-validator-mode", "observed": "The first UTF-8 detailed validation used final-snapshot expectations during the pending evidence lifecycle and also exposed two copied v5 constants; it returned 2967 of 2971 and was not counted.", "recovery": "Reserved verified-snapshot expectations for later lifecycle heads, used the explicit pending-snapshot mode for precommit evidence, and corrected the frozen-proposal and x1-seal constants.", "retained": True, "resolved_for_current_local_scope": True, "external_gate_closed": False},
    {"negative_id": "V6436-X2-N13", "origin": "v643-v6-x2-x1-seal-lookup", "observed": "A read-only x1 content-seal lookup used the preregistration directory instead of the reproduction directory and returned path-not-found.", "recovery": "Followed the validator's exact repository-relative path, confirmed 27 frozen x1 entries, and changed no artifact during the failed lookup.", "retained": True, "resolved_for_current_local_scope": True, "external_gate_closed": False},
    {"negative_id": "V6436-X2-N14", "origin": "v643-v6-x2-windows-ripgrep-glob", "observed": "A read-only ripgrep command passed a wildcard path that Windows did not expand and exited with an invalid filename error.", "recovery": "Used ripgrep include globs with explicit scripts and tests roots, then found all stale validator constants.", "retained": True, "resolved_for_current_local_scope": True, "external_gate_closed": False},
    {"negative_id": "V6436-X2-N15", "origin": "v643-v6-x2-direct-module-import", "observed": "The first direct unittest import failed because its file-based loader did not place the scripts directory on sys.path, so the new sibling model module was unresolved.", "recovery": "Added a file-location fallback that resolves the sibling model without mutating global import state, then reran direct and discovery callers.", "retained": True, "resolved_for_current_local_scope": True, "external_gate_closed": False},
]


def fixture_catalog() -> dict[str, list[dict[str, Any]]]:
    catalog: dict[str, list[dict[str, Any]]] = {}
    for proposal_id, base in canonical_inputs().items():
        rows = [{"case_id": f"{proposal_id}-C00", "label": "canonical-bounded", "input": copy.deepcopy(base), "expected_accepted": True}]
        for index, (label, changes) in enumerate(MUTATIONS[proposal_id], start=1):
            mutated = copy.deepcopy(base)
            mutated.update(copy.deepcopy(changes))
            rows.append({"case_id": f"{proposal_id}-C{index:02d}", "label": label, "input": mutated, "expected_accepted": False})
        catalog[proposal_id] = rows
    return catalog


def evaluate_catalog() -> dict[str, list[dict[str, Any]]]:
    evaluated: dict[str, list[dict[str, Any]]] = {}
    for proposal_id, rows in fixture_catalog().items():
        output = []
        for row in rows:
            accepted, reasons, details = DECISIONS[proposal_id](row["input"])
            output.append({
                "case_id": row["case_id"],
                "label": row["label"],
                "expected_accepted": row["expected_accepted"],
                "accepted": accepted,
                "matched_expectation": accepted == row["expected_accepted"],
                "reasons": reasons,
                "details": details,
            })
        evaluated[proposal_id] = output
    return evaluated


def git_blob(repo: Path, commit: str, relative: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"{commit}:{relative}"],
        cwd=repo,
        check=True,
        stdout=subprocess.PIPE,
    ).stdout


def x1_content_seal(repo: Path, phase: Path) -> dict[str, Any]:
    exact = json.loads((phase / "validation/x1-exact-file-set.json").read_text(encoding="utf-8"))
    entries = []
    for relative in exact["files"]:
        working = repo / relative
        blob = git_blob(repo, X1_COMMIT, relative)
        blob_normalized = blob.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        working_normalized = normalized_bytes(working)
        entries.append({
            "repo_path": relative,
            "git_blob_sha256": hashlib.sha256(blob).hexdigest(),
            "git_blob_sha256_lf_normalized": hashlib.sha256(blob_normalized).hexdigest(),
            "working_sha256_lf_normalized": hashlib.sha256(working_normalized).hexdigest(),
            "bytes_lf_normalized": len(working_normalized),
            "unchanged": blob_normalized == working_normalized,
        })
    if not all(row["unchanged"] for row in entries):
        raise RuntimeError("one or more frozen x1 files changed after the dedicated commit")
    return {
        "schema": "ghc.family.v643-v6.x1-content-seal.v1",
        "phase": PHASE,
        "owner": OWNER,
        "x1_commit": X1_COMMIT,
        "entry_count": len(entries),
        "entries": entries,
        "all_unchanged": True,
        "boundary": "The dedicated Git commit and normalized content parity bind x1. This is workflow integrity, not scientific proof or independent reproduction.",
    }


def open_and_exact_gates() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    open_gaps = [
        {"gate_id": "V6436-OG01", "surface": "GMUT singular-limit derivation, uniform asymptotics, physical validation, real data, prediction, force, and empirical confirmation", "needs": ["model-specific derivation", "remainder and matching proof", "expert mathematical review", "real public observations", "independent scientific review"]},
        {"gate_id": "V6436-OG02", "surface": "THOS real harms ascertainment, safety, effectiveness, and superiority", "needs": ["ethics review", "consent", "preregistered blind matched-budget real arms", "real participants and raters", "qualified safety review", "independent review"]},
        {"gate_id": "V6436-OG03", "surface": "Freed ID cross-wallet production interoperability and live operations", "needs": ["standards-conformant real keys and proofs", "live resolution, status, and revocation", "cross-vendor trials", "privacy assurance", "independent security review", "trust governance"]},
        {"gate_id": "V6436-OG04", "surface": "independent-team reproduction, Stage 20 evidence, and authorized external review", "needs": ["independently owned protocol", "independent team and infrastructure", "real evidence returns", "competent action-specific review"]},
        {"gate_id": "V6436-OG05", "surface": "manual and affected-user accessibility evaluation", "needs": ["authorized affected-user recruitment", "ethics and consent", "privacy review", "assistive-technology coverage", "qualified accessibility review"]},
    ]
    exact_gates = [
        {"gate_id": "V6436-EG01", "surface": "CBR legitimacy, taonga-use permission, benefit-sharing terms, and affected-party acceptance", "reserved_to": ["authorized affected parties", "appropriate Māori authorities", "authorized representatives"]},
        {"gate_id": "V6436-EG02", "surface": "Māori wording, authority, concepts, mātauranga Māori, taonga, kaitiaki relationships, and data governance", "reserved_to": ["appropriate Māori authorities", "Māori data-governance authorities"]},
        {"gate_id": "V6436-EG03", "surface": "cultural ratification", "reserved_to": ["competent cultural authorities"]},
        {"gate_id": "V6436-EG04", "surface": "legal interpretation, enacted law, intellectual-property status, jurisdiction, and enforceable benefit-sharing duties", "reserved_to": ["competent legal authorities", "legislatures and courts as applicable"]},
        {"gate_id": "V6436-EG05", "surface": "production, deployment, private publication, account, API-key, purchase, destructive or irreversible action", "reserved_to": ["fresh exact user authorization and competent operational authority"]},
        {"gate_id": "V6436-EG06", "surface": "proof, canon, final physics, identity replacement, consciousness, sentience, personhood, AGI/ASI, or sibling merge", "reserved_to": ["fresh exact evidence and competent authority; none present"]},
    ]
    return open_gaps, exact_gates


def manifest_candidates(repo: Path, phase: Path, proposals: list[dict[str, Any]]) -> list[str]:
    x1 = json.loads((phase / "validation/x1-exact-file-set.json").read_text(encoding="utf-8"))["files"]
    deliverables = [f"docs/sylven-arc/v643-v6/{relative}" for proposal in proposals for relative in proposal["deliverables"]]
    core = [
        "docs/sylven-arc/v643-v6/x2-proposal-ledger.json",
        "docs/sylven-arc/v643-v6/evidence/evidence-ledger.json",
        "docs/sylven-arc/v643-v6/retained-negative-register.json",
        "docs/sylven-arc/v643-v6/exact-open-gate-register.json",
        "docs/sylven-arc/v643-v6/threat-model.json",
        "docs/sylven-arc/v643-v6/phase-truth.json",
        "docs/sylven-arc/v643-v6/complete-incomplete-checklist.json",
        "docs/sylven-arc/v643-v6/environment/x2-execution-receipt.json",
        "docs/sylven-arc/v643-v6/reproduction/independent-team-gap.json",
        "docs/sylven-arc/v643-v6/reproduction/evidence-snapshot-plan.json",
        "docs/sylven-arc/v643-v6/reproduction/x1-content-seal.json",
        "docs/sylven-arc/v643-v6/tooling/executed-toolchain.json",
        "docs/sylven-arc/v643-v6/stage20/domain-veto-evidence-board.json",
        "docs/sylven-arc/v643-v6/deliverables/v643-v6-boundary-evidence-report.html",
        "docs/sylven-arc/v643-v6/deliverables/v643-v6-final-integrated-overview.md",
        "docs/sylven-arc/v643-v6/accessibility/static-report-receipt.json",
    ]
    tools = [
        "scripts/ghc_family_v643_v6_model.py",
        "scripts/ghc_family_v643_v6_evidence.py",
        "scripts/ghc_family_v643_v6_validator.py",
        "scripts/ghc_family_v643_v6_minimal.py",
        "scripts/build_ghc_family_v643_v6_report.py",
        "tests/test_ghc_family_v643_v6.py",
    ]
    candidates = list(dict.fromkeys(list(x1) + deliverables + core + tools))
    return [relative for relative in candidates if (repo / relative).is_file()]


def build(repo: Path, snapshot_state: str = "pending", lifecycle: str = "evidence") -> dict[str, Any]:
    repo = repo.resolve()
    phase = repo / "docs/sylven-arc/v643-v6"
    if snapshot_state == "pending" and lifecycle != "evidence":
        raise ValueError("closeout, seal, and final lifecycles require verified same-owner evidence snapshots")
    proposals = json.loads((phase / "x1-proposals.json").read_text(encoding="utf-8"))["proposals"]
    if {row["proposal_id"]: row["expected_disposition"] for row in proposals} != OBSERVED:
        raise RuntimeError("observed artifact dispositions diverge from the frozen expected map")
    evaluations = evaluate_catalog()
    if not all(row["matched_expectation"] for rows in evaluations.values() for row in rows):
        raise RuntimeError("one or more preregistered fixtures failed its expected decision")

    evidence_rows = []
    for proposal in proposals:
        pid = proposal["proposal_id"]
        rows = evaluations[pid]
        accepted = sum(row["accepted"] for row in rows)
        rejected = len(rows) - accepted
        contract = {
            "schema": f"ghc.family.v643-v6.{pid.lower()}.contract.v1",
            "phase": PHASE,
            "owner": OWNER,
            "proposal_id": pid,
            "title": proposal["title"],
            "observed_disposition": OBSERVED[pid],
            "disposition_scope": "artifact-level execution only",
            "canonical_case": rows[0],
            "accepted_case_count": accepted,
            "rejected_case_count": rejected,
            "authoritative_source_needs": proposal["authoritative_source_needs"],
            "protected_gates": proposal["protected_gates"],
            "external_claims_established": [],
            "boundary": BOUNDARY,
        }
        vectors = {
            "schema": f"ghc.family.v643-v6.{pid.lower()}.mutation-vectors.v1",
            "phase": PHASE,
            "owner": OWNER,
            "proposal_id": pid,
            "case_count": len(rows),
            "rejection_count": rejected,
            "all_matched_expectation": all(row["matched_expectation"] for row in rows),
            "cases": rows,
            "boundary": BOUNDARY,
        }
        gate = {
            "schema": f"ghc.family.v643-v6.{pid.lower()}.boundary.v1",
            "phase": PHASE,
            "owner": OWNER,
            "proposal_id": pid,
            "observed_disposition": OBSERVED[pid],
            "safe_now_result": "bounded structural, synthetic, protocol, open-gap, or exact-gate artifact only",
            "protected_gates": proposal["protected_gates"],
            "external_claims_established": [],
            "rollback_or_recovery": proposal["rollback_or_recovery"],
            "boundary": BOUNDARY,
        }
        for relative, payload in zip(proposal["deliverables"], (contract, vectors, gate), strict=True):
            write_json(phase / relative, payload)
        evidence_rows.append({
            "proposal_id": pid,
            "title": proposal["title"],
            "observed_disposition": OBSERVED[pid],
            "disposition_scope": "artifact-level execution only",
            "case_count": len(rows),
            "accepted": accepted,
            "rejected": rejected,
            "artifacts": proposal["deliverables"],
            "external_claims_established": [],
        })

    distribution = {label: list(OBSERVED.values()).count(label) for label in TRUTH_LABELS}
    write_json(phase / "x2-proposal-ledger.json", {
        "schema": "ghc.family.v643-v6.x2-proposal-ledger.v1",
        "phase": PHASE,
        "owner": OWNER,
        "source_commit": SOURCE_COMMIT,
        "source_seal": SOURCE_SEAL,
        "x1_commit": X1_COMMIT,
        "proposal_count": 10,
        "case_count": 80,
        "synthetic_rejection_count": 70,
        "distribution": distribution,
        "x1_before_x2_preserved": True,
        "proposals": evidence_rows,
        "boundary": BOUNDARY,
    })
    write_json(phase / "evidence/evidence-ledger.json", {
        "schema": "ghc.family.v643-v6.evidence-ledger.v1",
        "phase": PHASE,
        "owner": OWNER,
        "evidence_class": "local_structural_synthetic_protocol_open_gap_or_exact_gate_artifact",
        "rows": evidence_rows,
        "empirical_rows": 0,
        "real_participants": 0,
        "real_arms": 0,
        "real_raters": 0,
        "real_keys_or_proofs": 0,
        "legal_or_cultural_ratifications": 0,
        "independent_team_returns": 0,
        "different_architecture_returns": 0,
        "boundary": BOUNDARY,
    })

    inherited_path = repo / "docs/tamar-vey/v643-v5/retained-negative-register.json"
    inherited = json.loads(inherited_path.read_text(encoding="utf-8"))
    negatives = copy.deepcopy(inherited["negatives"])
    for proposal_id, rows in evaluations.items():
        for row in rows:
            if not row["accepted"]:
                negatives.append({
                    "negative_id": f"V6436-SYN-{row['case_id']}",
                    "origin": "v643-v6-preregistered-synthetic",
                    "proposal_id": proposal_id,
                    "case_id": row["case_id"],
                    "observed": row["reasons"],
                    "retained": True,
                    "resolved_for_current_local_scope": True,
                    "external_gate_closed": False,
                })
    x1_audit = json.loads((phase / "validation/x1-operational-negatives.json").read_text(encoding="utf-8"))
    x1_negatives = []
    for item in x1_audit.get("negatives", []):
        x1_negatives.append({
            "negative_id": item["negative_id"],
            "origin": "v643-v6-x1-operational",
            "observed": item["observed_failure"],
            "recovery": item["recovery"],
            "retained": True,
            "resolved_for_current_local_scope": True,
            "external_gate_closed": False,
        })
    negatives.extend(x1_negatives)
    negatives.extend(copy.deepcopy(X2_OPERATIONAL_NEGATIVES))
    write_json(phase / "retained-negative-register.json", {
        "schema": "ghc.family.v643-v6.retained-negative-register.v1",
        "phase": PHASE,
        "owner": OWNER,
        "inherited_from": "docs/tamar-vey/v643-v5/retained-negative-register.json",
        "inherited_sha256_lf_normalized": normalized_sha256(inherited_path),
        "inherited_count": len(inherited["negatives"]),
        "x1_operational_count": len(x1_negatives),
        "new_synthetic_count": 70,
        "x2_operational_count": len(X2_OPERATIONAL_NEGATIVES),
        "new_count": 70 + len(x1_negatives) + len(X2_OPERATIONAL_NEGATIVES),
        "negative_count": len(negatives),
        "all_retained": True,
        "erasure_permitted": False,
        "negatives": negatives,
        "boundary": BOUNDARY,
    })

    open_gaps, exact_gates = open_and_exact_gates()
    write_json(phase / "exact-open-gate-register.json", {
        "schema": "ghc.family.v643-v6.exact-open-gate-register.v1",
        "phase": PHASE,
        "owner": OWNER,
        "open_gap_count": 5,
        "exact_gate_count": 6,
        "open_gaps": open_gaps,
        "exact_gates": exact_gates,
        "all_visible": True,
        "none_silently_closed": True,
        "boundary": BOUNDARY,
    })

    threats = [
        {"id": "T01", "threat": "registered outcomes are omitted, introduced, or redefined without quarantine", "control": "registry-to-protocol-to-analysis-to-report completeness graph"},
        {"id": "T02", "threat": "local GMUT existence is promoted to global continuation or theorem", "control": "control-norm, coupled-field, interval, and breakdown obligations"},
        {"id": "T03", "threat": "regular likelihood asymptotics are assumed at a boundary", "control": "nonregular reference-law flag and zero-real-row promotion lock"},
        {"id": "T04", "threat": "THOS sham credibility or attention dose is silently unmatched", "control": "separate credibility, expectancy, budget, and blind-assessment fields"},
        {"id": "T05", "threat": "cloned Freed ID device states fork or roll back ambiguously", "control": "monotonic conflict ordering and fork refusal"},
        {"id": "T06", "threat": "synthetic device history is promoted to real keys or production", "control": "real-key, resolver, status, interoperability, review, and governance gates"},
        {"id": "T07", "threat": "repository output imposes a legal hold or spoliation consequence", "control": "neutral fields and exact affected-party, Māori-authority, privilege, and legal gates"},
        {"id": "T08", "threat": "attacker-controlled input amplifies work beyond declared ceilings", "control": "size-indexed work and memory budgets with timeout non-success"},
        {"id": "T09", "threat": "timing non-detection is called constant-time or cryptographic assurance", "control": "secret-trace screen plus real-implementation and independent-review gates"},
        {"id": "T10", "threat": "stationarity is mislabeled as equilibrium despite probability currents", "control": "rate, reverse-edge, detailed-balance, and current classifier"},
        {"id": "T11", "threat": "thermodynamic classification is converted into psyche evidence", "control": "explicit cross-pillar non-substitution"},
        {"id": "T12", "threat": "one favored Stage 20 model or score compensates exact vetoes", "control": "frozen model and loss set with minimax-regret defer rule"},
        {"id": "T13", "threat": "same-owner snapshots are called independent evidence", "control": "owner, protocol, infrastructure, and return provenance"},
        {"id": "T14", "threat": "privacy scan or static report is called exhaustive or fully accessible", "control": "bounded pattern classes and reserved manual and affected-user evaluation"},
    ]
    threats = [
        {"id": "T01", "threat": "claim-term meaning changes under a cosmetic version label", "control": "versioned definition, domain, range, split, merge, and quarantine map"},
        {"id": "T02", "threat": "a nonuniform GMUT small-parameter limit is promoted as a uniform theorem", "control": "inner, outer, overlap, matching, remainder, and nonpromotion obligations"},
        {"id": "T03", "threat": "synthetic code verification is called physical validation", "control": "manufactured solution, grid-order check, and zero-real-observation boundary"},
        {"id": "T04", "threat": "THOS harms are solicited differently by arm or attributed without blinding", "control": "arm-equal schedule and separate occurrence, severity, recovery, and attribution fields"},
        {"id": "T05", "threat": "wallet migration silently loses credential meaning", "control": "pre-export and post-import semantic comparison with loss quarantine"},
        {"id": "T06", "threat": "synthetic wallet parity is promoted to real identity or production interoperability", "control": "real-key, resolver, status, cross-vendor, review, and governance gates"},
        {"id": "T07", "threat": "repository output grants taonga use or invents benefit-sharing authority", "control": "neutral questions and exact affected-party, Māori, cultural, and legal gates"},
        {"id": "T08", "threat": "PATH, PATHEXT, or current-directory ordering resolves an attacker-controlled executable", "control": "explicit search-order model, allowlist, and retained shadow witness"},
        {"id": "T09", "threat": "automated static checks are called complete accessibility", "control": "structural audit plus explicit manual and affected-user reservations"},
        {"id": "T10", "threat": "finite-size ensemble-specific behavior is silently generalized", "control": "ensemble, size, interaction, convexity, observable, and limit-order contract"},
        {"id": "T11", "threat": "ensemble classification is converted into psyche or GMUT law evidence", "control": "explicit cross-pillar and physical-law non-substitution"},
        {"id": "T12", "threat": "a participant-free accessibility matrix is described as user evidence", "control": "open gap with zero participants, consent, privacy, and non-generalization rules"},
        {"id": "T13", "threat": "same-owner snapshots are called independent evidence", "control": "owner, protocol, infrastructure, and return provenance"},
        {"id": "T14", "threat": "a bounded privacy scan is called exhaustive", "control": "declared pattern classes and manual review boundary"},
    ]
    write_json(phase / "threat-model.json", {
        "schema": "ghc.family.v643-v6.threat-model.v1",
        "phase": PHASE,
        "owner": OWNER,
        "threat_count": len(threats),
        "threats": threats,
        "exhaustive_security": False,
        "independent_security_review": False,
        "resource_ceilings": {"owner_generated_files": 15000, "scope": "v643-v6 only"},
        "boundary": BOUNDARY,
    })

    verified = snapshot_state == "verified"
    lifecycle_states = {"evidence": "EVIDENCE_VERIFIED" if verified else "EVIDENCE_CANDIDATE", "closeout": "CLOSEOUT_CANDIDATE", "seal": "SEALED_CANDIDATE", "final": "FINAL_HEAD_CANDIDATE"}
    pending = {
        "evidence": ["evidence commit", "two fresh detached same-owner snapshots", "closeout", "seal", "exact final validation", "one terminal baton"] if not verified else ["closeout", "seal", "exact final validation", "one terminal baton"],
        "closeout": ["closeout detached validation", "seal", "exact final validation", "one terminal baton"],
        "seal": ["seal detached validation", "exact final validation", "one terminal baton"],
        "final": ["exact final detached validation", "one terminal baton"],
    }
    protected_claims = {
        "empirical_gmut": False,
        "gmut_likelihood_or_unique_prediction": False,
        "thos_effectiveness_or_superiority": False,
        "production_freed_id": False,
        "cbr_legitimacy_or_affected_party_acceptance": False,
        "maori_authority_or_data_governance": False,
        "legal_or_cultural_ratification": False,
        "deployment_or_production_readiness": False,
        "complete_accessibility": False,
        "exhaustive_security": False,
        "independent_team_reproduction": False,
        "proof_or_canon": False,
        "consciousness_personhood_agi_asi": False,
        "stage20_readiness": False,
    }
    write_json(phase / "phase-truth.json", {
        "schema": "ghc.family.v643-v6.phase-truth.v1",
        "phase": PHASE,
        "owner": OWNER,
        "state": lifecycle_states[lifecycle],
        "source_commit": SOURCE_COMMIT,
        "source_seal": SOURCE_SEAL,
        "x1_commit": X1_COMMIT,
        "proposal_count": 10,
        "distribution": distribution,
        "case_count": 80,
        "synthetic_rejection_count": 70,
        "retained_negative_count": len(negatives),
        "open_gap_count": 5,
        "exact_gate_count": 6,
        "primary_focus": "GMUT Mind",
        "all_three_pillars_preserved": True,
        "same_owner_repeatability": verified,
        "independent_team_reproduction": False,
        "protected_claims": protected_claims,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "route_state": "PREPARED_NOT_SENT",
        "outbound_message_count": 0,
        "successor_task_count": 0,
        "subagent_count": 0,
        "boundary": BOUNDARY,
    })
    write_json(phase / "complete-incomplete-checklist.json", {
        "schema": "ghc.family.v643-v6.complete-incomplete-checklist.v1",
        "phase": PHASE,
        "owner": OWNER,
        "complete": [
            "exact Tamar source, seal ancestry, clean state, and live-remote equality verified",
            "existing clean Sylven lane advanced by fast-forward only",
            "dedicated x1 frozen, pushed, clean, and four-way equal before x2",
            "ten semantically distinct proposals executed only within frozen approval classes",
            "eighty deterministic fixtures with seventy retained rejecting mutations",
            "all 809 inherited negatives and every v643-v6 negative retained",
            "GMUT Mind, THOS Body, and Freed ID/CBR Heart preserved",
            "current official or primary source constraints recorded",
        ],
        "incomplete": [
            "model-specific GMUT singular-limit derivation, uniform asymptotic proof, physical validation, real data, prediction, force, or empirical confirmation",
            "preregistered blind matched-budget real THOS arms, participants, raters, harms evidence, safety, effectiveness, or superiority",
            "production Freed ID cross-wallet keys, proofs, live resolution, status, revocation, interoperability, privacy and security review, and trust governance",
            "CBR taonga-use permission, benefit-sharing terms, affected-party acceptance, Māori authority and data governance, cultural ratification, legal interpretation, or enacted-law status",
            "qualified manual and affected-user accessibility evaluation",
            "independent host-security review and exhaustive security",
            "independent-team scientific reproduction",
            "independently reviewed Stage 20 decision",
        ],
        "lifecycle": lifecycle,
        "same_owner_evidence_snapshots_verified": verified,
        "closeout_ready": verified,
        "pending": pending[lifecycle],
        "boundary": BOUNDARY,
    })

    write_json(phase / "environment/x2-execution-receipt.json", {
        "schema": "ghc.family.v643-v6.x2-execution-receipt.v1",
        "phase": PHASE,
        "owner": OWNER,
        "x1_commit": X1_COMMIT,
        "x1_remote_equal_before_x2": True,
        "real_data_downloaded": False,
        "real_participants_or_raters": 0,
        "real_arms": 0,
        "real_keys_or_proofs": 0,
        "live_services_or_deployments": 0,
        "accounts_or_api_keys_changed": 0,
        "desktop_updated": False,
        "elevation_used": False,
        "host_security_changed": False,
        "windows_feature_changed": False,
        "rebooted": False,
        "boundary": BOUNDARY,
    })
    write_json(phase / "reproduction/independent-team-gap.json", {
        "schema": "ghc.family.v643-v6.independent-team-gap.v1",
        "phase": PHASE,
        "owner": OWNER,
        "same_owner_evidence_snapshots_verified": verified,
        "shared_repository_protocol_and_infrastructure": True,
        "different_architecture_return_received": False,
        "independent_team_protocol_owned": False,
        "independent_team_return_received": False,
        "independent_team_reproduction_established": False,
        "boundary": BOUNDARY,
    })
    write_json(phase / "reproduction/evidence-snapshot-plan.json", {
        "schema": "ghc.family.v643-v6.evidence-snapshot-plan.v1",
        "phase": PHASE,
        "owner": OWNER,
        "snapshot_count": 2,
        "location_class": "fresh detached D-drive worktrees",
        "required_same_commit": True,
        "required_clean_before_and_after": True,
        "required_checks": ["complete repository suite", "detailed validator", "minimal validator", "all JSON parsing", "privacy and raw-ID scan", "manifest parity"],
        "claim_scope": "same-owner repeatability only",
        "independent_team_reproduction": False,
        "boundary": BOUNDARY,
    })
    write_json(phase / "reproduction/x1-content-seal.json", x1_content_seal(repo, phase))
    write_json(phase / "tooling/executed-toolchain.json", {
        "schema": "ghc.family.v643-v6.executed-toolchain.v1",
        "phase": PHASE,
        "owner": OWNER,
        "tools": [
            {"name": "ghc_family_v643_v6_model.py", "role": "frozen rule, boundary, and seventy-mutation model"},
            {"name": "ghc_family_v643_v6_evidence.py", "role": "80-case evidence builder and retained-negative assembler"},
            {"name": "ghc_family_v643_v6_validator.py", "role": "detailed evidence, manifest, privacy, report, and boundary validation"},
            {"name": "ghc_family_v643_v6_minimal.py", "role": "small standard-library validation floor"},
            {"name": "build_ghc_family_v643_v6_report.py", "role": "accessible static HTML report builder"},
            {"name": "test_ghc_family_v643_v6.py", "role": "decision, fixture, retention, manifest, and validator regression suite"},
        ],
        "caller_compatibility_preserved": True,
        "inherited_tools_mutated": False,
        "mass_deletion_performed": False,
        "boundary": BOUNDARY,
    })
    vetoes = [
        {"domain": "GMUT Mind", "local_artifact_status": "pass", "external_evidence_status": "missing", "decision": "veto", "reason": "no model-specific singular-limit proof, physical validation, real data, force, prediction, or empirical confirmation"},
        {"domain": "THOS Body", "local_artifact_status": "represented", "external_evidence_status": "missing", "decision": "veto", "reason": "no preregistered blind matched-budget real arms, participants, harms evidence, raters, or independent review"},
        {"domain": "Freed ID", "local_artifact_status": "represented", "external_evidence_status": "missing", "decision": "veto", "reason": "no real keys, live resolution/status/revocation, cross-vendor interoperability, review, or governance"},
        {"domain": "CBR and Māori authority", "local_artifact_status": "exact_gate", "external_evidence_status": "reserved", "decision": "veto", "reason": "taonga use, benefit sharing, affected-party, Māori, cultural, and legal authority cannot be substituted"},
        {"domain": "reproduction", "local_artifact_status": "same_owner_only" if verified else "pending", "external_evidence_status": "no independent return", "decision": "veto", "reason": "shared owner, protocol, repository, and infrastructure"},
        {"domain": "accessibility and security", "local_artifact_status": "bounded structural checks", "external_evidence_status": "manual and independent review missing", "decision": "veto", "reason": "no complete accessibility or exhaustive-security evidence"},
    ]
    write_json(phase / "stage20/domain-veto-evidence-board.json", {
        "schema": "ghc.family.v643-v6.stage20-board.v1",
        "phase": PHASE,
        "owner": OWNER,
        "vetoes": vetoes,
        "compensation_across_domains_allowed": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": BOUNDARY,
    })

    manifest_rows = []
    for relative in manifest_candidates(repo, phase, proposals):
        target = repo / relative
        data = normalized_bytes(target)
        manifest_rows.append({"repo_path": relative, "sha256_lf_normalized": hashlib.sha256(data).hexdigest(), "bytes_lf_normalized": len(data)})
    write_json(phase / "reproduction/manifest.json", {
        "schema": "ghc.family.v643-v6.manifest.v1",
        "phase": PHASE,
        "owner": OWNER,
        "hash_algorithm": "sha256",
        "text_normalization": "CRLF and CR normalized to LF before hashing",
        "entry_count": len(manifest_rows),
        "entries": manifest_rows,
        "snapshot_state": snapshot_state,
        "same_owner_repeatability_only": True,
        "independent_team_reproduction": False,
        "boundary": BOUNDARY,
    })
    return {
        "phase": PHASE,
        "proposal_count": 10,
        "case_count": 80,
        "rejections": 70,
        "distribution": distribution,
        "retained_negatives": len(negatives),
        "x1_operational_negatives": len(x1_negatives),
        "x2_operational_negatives": len(X2_OPERATIONAL_NEGATIVES),
        "manifest_entries": len(manifest_rows),
        "snapshot_state": snapshot_state,
        "lifecycle": lifecycle,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--snapshot-state", choices=("pending", "verified"), default="pending")
    parser.add_argument("--lifecycle", choices=("evidence", "closeout", "seal", "final"), default="evidence")
    args = parser.parse_args()
    print(json.dumps(build(args.repo, args.snapshot_state, args.lifecycle), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
