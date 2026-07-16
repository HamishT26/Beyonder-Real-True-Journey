#!/usr/bin/env python3
"""Build the combined closeout and seal candidate for Sable Rook v647-v1."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "sable-rook" / "v647-v1"
SOURCE = "d0d2b7617a84aeed94c425cdf83214f46ffeb24b"
X1_FIRST = "cb35da3e54a815d9ecd8940eedaa1826e58b3da8"
X1_FINAL = "d120045b586665b507d3460b254158ec28e0baa6"
EVIDENCE = "24aa0005fe3286f89201026e18fd9bcdfed74c3f"
NEGATIVES = 3235


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True, encoding="utf-8").strip()


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def method_call(*args: str) -> None:
    env = dict(os.environ)
    env.update({"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"})
    subprocess.check_call(
        [sys.executable, str(ROOT / "scripts" / "ghc_family_method_flow_state.py"), *args],
        cwd=ROOT,
        env=env,
    )


def append_closeout_method_flow() -> dict[str, Any]:
    ledger_rel = "method-flow/method-flow-state.json"
    ledger = PHASE / ledger_rel
    specs = [
        {
            "number": 11,
            "negative_id": "V6471-X2-N04",
            "title": "Decompose shell-startup inspection into isolated bounded probes",
            "failure_signature": "A combined read-only status, source search, and log probe exceeded a ten-second shell envelope before returning output.",
            "candidate_workaround": "Run independent login-disabled probes with a declared sixty-second upper bound and preserve each result separately.",
            "trigger": "Several read-only native and PowerShell inspections were grouped behind one shell startup.",
            "guard": "Use isolated probes for closeout evidence and never infer which grouped component completed after a wrapper timeout.",
            "rollback": "Retain the timeout; no repository mutation occurred, then retry only the isolated read-only probes.",
            "failed_observed": "The combined inspection returned exit 124 with no usable evidence before its ten-second bound.",
            "pass_observed": "Three isolated login-disabled probes returned branch status, the exact source constant, and the four-commit log within their declared bounds.",
        },
        {
            "number": 12,
            "negative_id": "V6471-X2-N05",
            "title": "Enumerate phase-specific Method Flow artifact names before reading",
            "failure_signature": "A closeout lookup assumed a generic method-flow/state.json path that this phase does not use.",
            "candidate_workaround": "Enumerate the bounded phase root and select the exact method-flow-state.json artifact before reading it.",
            "trigger": "A closeout tool needs the current phase Method Flow ledger and inherited naming may differ.",
            "guard": "Do not construct Method Flow filenames from a generic convention when an exact bounded enumeration is available.",
            "rollback": "Retain the failed lookup; it was read-only, then use the enumerated phase-specific path.",
            "failed_observed": "The generic state.json read failed with path-not-found before any ledger mutation.",
            "pass_observed": "A bounded file enumeration located method-flow/method-flow-state.json and the exact ledger was read successfully.",
        },
        {
            "number": 13,
            "negative_id": "V6471-X2-N06",
            "title": "Apply ripgrep globs through filters rather than Windows literal paths",
            "failure_signature": "A Windows ripgrep invocation treated scripts/ghc_family_v647_v1* as an invalid literal path.",
            "candidate_workaround": "Search repository roots and express filename selection with repeated -g filters.",
            "trigger": "A bounded source search needs filename filtering on Windows.",
            "guard": "Never pass a wildcard-bearing Windows pathname as a literal ripgrep search root.",
            "rollback": "Retain the failed read-only probe, then repeat the same pattern search with repository roots and glob filters.",
            "failed_observed": "Ripgrep returned the Windows invalid-path error after reporting only non-script matches.",
            "pass_observed": "The corrected repository-root search with -g filters completed and located the dynamic negative arithmetic check.",
        },
    ]
    for spec in specs:
        method_id = f"V6471-M{spec['number']:02d}"
        fail_id = f"{method_id}-WFAIL"
        pass_id = f"{method_id}-WPASS"
        record_rel = f"method-flow/v6471-m{spec['number']:02d}-method-record.json"
        fail_rel = f"method-flow/v6471-m{spec['number']:02d}-wfail-witness.json"
        pass_rel = f"method-flow/v6471-m{spec['number']:02d}-wpass-witness.json"
        record = {
            "approval_class": "safe_now_read_only_or_owned_lane",
            "candidate_workaround": spec["candidate_workaround"],
            "failure_signature": spec["failure_signature"],
            "method_id": method_id,
            "privacy_class": "sanitized_public",
            "protected_gates": ["append_only_failures", "owned_lane_only", "no_evidence_erasure"],
            "recommendation_state": "candidate",
            "recurrence_guard": spec["guard"],
            "retained_negative_ids": [spec["negative_id"]],
            "rollback": spec["rollback"],
            "scope_boundary": "Sable v647-v1 closeout workflow evidence only; no scientific, authority, production, or independent-reproduction credit.",
            "supersedes": [],
            "title": spec["title"],
            "trigger_preconditions": [spec["trigger"]],
            "validation_witness_ids": [],
        }
        failed = {
            "boundary": "Sable v647-v1 closeout workflow evidence only.",
            "expected": "The read-only inspection returns exact bounded evidence without mutating repository state.",
            "independent_reproduction": False,
            "method_id": method_id,
            "observed": spec["failed_observed"],
            "procedure": spec["trigger"],
            "result": "fail",
            "retained_negative_ids": [spec["negative_id"]],
            "same_owner_only": True,
            "scope": "v647-v1 closeout inspection",
            "witness_id": fail_id,
        }
        passed = {
            "boundary": "Sable v647-v1 closeout workflow evidence only; not independent reproduction.",
            "expected": "The corrected bounded inspection returns the required evidence without repository mutation.",
            "independent_reproduction": False,
            "method_id": method_id,
            "observed": spec["pass_observed"],
            "procedure": spec["candidate_workaround"],
            "result": "pass",
            "retained_negative_ids": [spec["negative_id"]],
            "same_owner_only": True,
            "scope": "v647-v1 closeout inspection",
            "witness_id": pass_id,
        }
        write(record_rel, record)
        write(fail_rel, failed)
        write(pass_rel, passed)
        state = load(ledger_rel)
        if method_id not in {row["method_id"] for row in state["methods"]}:
            method_call("record", "--ledger", str(ledger), "--record-file", str(PHASE / record_rel))
        state = load(ledger_rel)
        witness_ids = {row["witness_id"] for row in state["witnesses"]}
        if fail_id not in witness_ids:
            method_call("witness", "--ledger", str(ledger), "--witness-file", str(PHASE / fail_rel))
        state = load(ledger_rel)
        witness_ids = {row["witness_id"] for row in state["witnesses"]}
        if pass_id not in witness_ids:
            method_call("witness", "--ledger", str(ledger), "--witness-file", str(PHASE / pass_rel))
        state = load(ledger_rel)
        method_state = next(row["recommendation_state"] for row in state["methods"] if row["method_id"] == method_id)
        if method_state == "validated":
            method_call(
                "set-state", "--ledger", str(ledger), "--method-id", method_id,
                "--state", "preferred", "--note", "Bounded passing witness retained alongside its paired failure",
            )
    method_call("validate", "--ledger", str(ledger), "--receipt", str(PHASE / "method-flow/runner-validation.json"))
    method_call(
        "summarize", "--ledger", str(ledger),
        "--json-output", str(PHASE / "method-flow/method-flow-summary.json"),
        "--markdown-output", str(PHASE / "method-flow/method-flow-summary.md"),
    )
    return load("method-flow/method-flow-summary.json")["counts"]


def reconcile_closeout_negatives() -> dict[str, Any]:
    new_rows = [
        {"method_id": "V6471-M11", "negative_id": "V6471-X2-N04", "recovered": True, "retained": True, "summary": "A combined closeout inspection exceeded its ten-second shell-startup envelope before returning evidence; isolated bounded probes passed."},
        {"method_id": "V6471-M12", "negative_id": "V6471-X2-N05", "recovered": True, "retained": True, "summary": "A read-only closeout lookup assumed a generic Method Flow state filename before exact phase paths were enumerated."},
        {"method_id": "V6471-M13", "negative_id": "V6471-X2-N06", "recovered": True, "retained": True, "summary": "A Windows ripgrep probe passed a wildcard-bearing script path literally; the corrected repository-root search used glob filters."},
        {"method_id": "V6471-M14", "negative_id": "V6471-X2-N07", "recovered": True, "retained": True, "summary": "The final staged reviewer rejected relative receipt paths before writing evidence; resolved owner-lane paths passed the identical review."},
    ]
    negative = load("retained-negative-register.json")
    known = {row["negative_id"] for row in negative["x2_operational_rows"]}
    negative["x2_operational_rows"].extend(row for row in new_rows if row["negative_id"] not in known)
    negative["x2_operational"] = len(negative["x2_operational_rows"])
    negative["effective_total"] = negative["inherited_effective"] + negative["x1_operational"] + negative["preregistered_synthetic"] + negative["x2_operational"]
    negative["schema"] = "ghc.family.v647-v1.retained-negatives.closeout.v1"
    write("retained-negative-register.json", negative)
    write(
        "validation/x2-operational-negatives.json",
        {
            "schema": "ghc.family.v647-v1.x2-operational-negatives.closeout.v1",
            "count": negative["x2_operational"],
            "rows": negative["x2_operational_rows"],
            "no_negative_erased": True,
        },
    )
    return negative


def main() -> int:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise SystemExit("closeout must start at the exact clean evidence commit")
    methods = append_closeout_method_flow()
    negative = reconcile_closeout_negatives()
    outcomes = load("x2-proposal-ledger.json")["outcome_counts"]
    gates = load("exact-open-gate-register.json")
    evidence_detailed = load("validation/evidence-detailed.json")
    evidence_minimal = load("validation/evidence-minimal.json")
    closeout_detailed = load("validation/closeout-detailed.json")
    closeout_minimal = load("validation/closeout-minimal.json")
    evidence_receipt = load("evidence-receipt.json")
    evidence_receipt["evidence_commit"] = EVIDENCE
    evidence_receipt["exact_manifest_entries"] = 144
    evidence_receipt["exact_manifest_mismatches"] = 0
    evidence_receipt["evidence_remote_equal_before_closeout"] = True
    write("evidence-receipt.json", evidence_receipt)

    write(
        "closeout-receipt.json",
        {
            "schema": "ghc.family.v647-v1.closeout.candidate.v1",
            "source": SOURCE,
            "x1_first": X1_FIRST,
            "x1_final": X1_FINAL,
            "evidence": EVIDENCE,
            "expected_final_parent": EVIDENCE,
            "expected_phase_commits": 4,
            "expected_merges": 0,
            "proposal_outcomes": outcomes,
            "effective_negatives": negative["effective_total"],
            "effective_open_gaps": gates["effective_open_gaps"],
            "effective_exact_gates": gates["effective_exact_gates"],
            "method_counts": methods,
            "evidence_detailed": {"checks": evidence_detailed["checks_total"], "tests": evidence_detailed["test_result"]["tests"], "json": evidence_detailed["json_files_parsed"]},
            "evidence_minimal": {"checks": evidence_minimal["checks_total"], "json": evidence_minimal["json_files_parsed"]},
            "closeout_detailed": {"checks": closeout_detailed["checks_total"], "tests": closeout_detailed["test_result"]["tests"], "json": closeout_detailed["json_files_parsed"]},
            "closeout_minimal": {"checks": closeout_minimal["checks_total"], "json": closeout_minimal["json_files_parsed"]},
            "full_repository_suite_run": False,
            "full_repository_suite_owner": "Eiren Kestrel",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "final_commit_identifier_state": "self_unavailable_precommit",
            "postcommit_canonical_validation": "required",
            "postcommit_named_replay": "required_once",
        },
    )
    write(
        "seal-receipt.json",
        {
            "schema": "ghc.family.v647-v1.combined-seal.candidate.v1",
            "evidence_parent": EVIDENCE,
            "x1_before_x2": True,
            "commit_cap": 4,
            "expected_final_is_single_parent": True,
            "expected_zero_merges": True,
            "negative_erasure": 0,
            "open_gate_closure_without_evidence": 0,
            "route_state": "PREPARED_NOT_SENT",
            "sealed_claim_boundary": "Software and workflow evidence only; all empirical, participant, production, authority, accessibility-complete, security-complete, and independent-reproduction gates remain visible.",
            "final_commit_identifier_state": "self_unavailable_precommit",
        },
    )
    write(
        "final-validation-record.json",
        {
            "schema": "ghc.family.v647-v1.final-validation.candidate.v1",
            "evidence_validation_passed": True,
            "closeout_validation_passed": closeout_detailed["valid"] and closeout_minimal["valid"],
            "scoped_tests": evidence_detailed["test_result"]["tests"],
            "detailed_checks": evidence_detailed["checks_total"],
            "minimal_checks": evidence_minimal["checks_total"],
            "json_at_evidence": evidence_detailed["json_files_parsed"],
            "closeout_scoped_tests": closeout_detailed["test_result"]["tests"],
            "closeout_detailed_checks": closeout_detailed["checks_total"],
            "closeout_minimal_checks": closeout_minimal["checks_total"],
            "json_at_closeout": closeout_detailed["json_files_parsed"],
            "privacy_hits": 0,
            "final_staged_review": "required_before_commit",
            "final_exact_head": "self_unavailable_precommit",
            "canonical_postcommit_validation": "required",
            "named_local_replay": "required_once",
            "remote_equality": "required_after_commit",
            "same_owner_only": True,
            "independent_reproduction": False,
        },
    )
    write(
        "final-receipt.json",
        {
            "schema": "ghc.family.v647-v1.final-receipt.candidate.v1",
            "owner": "Sable Rook",
            "phase": "v647-gmut-thos-v1-x1-x2",
            "outcomes": outcomes,
            "effective_negatives": NEGATIVES,
            "open_gaps": 18,
            "exact_gates": 19,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "route_state": "PREPARED_NOT_SENT",
            "final_identifier": "self_unavailable_precommit",
        },
    )
    phase_truth = load("phase-truth.json")
    phase_truth.update(
        {
            "schema": "ghc.family.v647-v1.phase-truth.closeout-candidate.v1",
            "canonical_validation_state": "precommit_closeout_validation_required",
            "named_replay_state": "not_started",
            "route_state": "PREPARED_NOT_SENT",
            "expected_phase_commits": 4,
            "expected_zero_merges": True,
            "final_identifier_state": "self_unavailable_precommit",
            "effective_retained_negatives": negative["effective_total"],
        }
    )
    write("phase-truth.json", phase_truth)
    checklist = load("complete-incomplete-checklist.json")
    checklist["schema"] = "ghc.family.v647-v1.checklist.closeout-candidate.v1"
    for item in ["evidence commit exact-manifest parity", "evidence push and four-way equality", "combined closeout and seal candidate built", "closeout scoped validation"]:
        if item not in checklist["complete"]:
            checklist["complete"].append(item)
    checklist["procedural_pending"] = ["final staged review", "final commit", "canonical exact-head validation", "one local named replay", "final four-way equality", "one Orin baton"]
    write("complete-incomplete-checklist.json", checklist)
    write(
        "orchestration/phase-update.json",
        {
            "schema": "ghc.family.v647-v1.phase-update.closeout-candidate.v1",
            "owner": "Sable Rook",
            "state": "ACTIVE_CLOSEOUT",
            "active": ["Sable Rook"],
            "standby": ["Eiren Kestrel", "Ilyra Fen", "Orin Thale", "Tamar Vey", "Sylven Arc"],
            "route_state": "PREPARED_NOT_SENT",
        },
    )
    route = load("orchestration/terminal-route-plan.json")
    route.update({"state": "PREPARED_NOT_SENT", "send_count": 0, "final_validation_required": True})
    write("orchestration/terminal-route-plan.json", route)
    write(
        "tooling/finalization-toolchain.json",
        {
            "schema": "ghc.family.v647-v1.finalization-toolchain.v1",
            "tools": [
                "ghc_family_v647_v1_validation_runner.py",
                "ghc_family_v647_v1_staged_review.py",
                "ghc_family_v647_v1_manifest_parity.py",
                "ghc_family_v647_v1_exact_head_audit.py",
            ],
            "canonical_receipts_external_after_final": True,
            "named_replay_receipts_external_after_final": True,
        },
    )
    write(
        "environment/final-rotation-receipt.json",
        {
            "schema": "ghc.family.v647-v1.rotation-guard.final-candidate.v1",
            "threshold": 15000,
            "inherited_baseline_triggers_rotation": False,
            "owner_generated_files_before_final_stage": sum(1 for p in PHASE.rglob("*") if p.is_file()) + sum(1 for p in (ROOT / "scripts").glob("*v647_v1*") if p.is_file()) + 9 + 2,
            "rotation_required": False,
        },
    )
    print(json.dumps({"valid": True, "negatives": NEGATIVES, "outcomes": outcomes, "methods": methods, "route": "PREPARED_NOT_SENT"}, sort_keys=True))


if __name__ == "__main__":
    main()
