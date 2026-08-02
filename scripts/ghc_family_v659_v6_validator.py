#!/usr/bin/env python3
"""Detailed same-owner validator for Liora Venn v659-v6."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

import ghc_family_v659_v6_x2_data as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
EVIDENCE_COMMIT = "72f9a62167d6d946e8fea5a7337fe12691cf475f"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def validate_phase() -> dict:
    checks: list[dict] = []
    expected_frozen = d.PRIOR_FROZEN + d.NEW_UNIQUE_COUNT
    expected_negatives = d.ACTIVATION_NEGATIVES + len(d.STARTUP_FAILURES) + len(d.X2_FAILURES) + 100
    expected_methods = d.ACTIVATION_METHODS + len(d.STARTUP_FAILURES) + len(d.X2_FAILURES) + 100
    expected_gaps = d.SOURCE_OPEN_GAPS + d.EXPECTED_DISTRIBUTION["open_gap"]
    expected_gates = d.SOURCE_EXACT_GATES + d.EXPECTED_DISTRIBUTION["exact_gate"]

    def check(name: str, passed: bool, detail: str = "") -> None:
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    truth = load("final/final-truth.json")
    outcomes = load("evidence/proposal-outcomes.json")
    route = load("route/prepared-route.json")
    lifecycle = load("final/lifecycle-summary.json")
    flow = load("final/lifecycle-method-flow.json")
    evidence = load("final/evidence-receipt.json")
    open_gates = load("final/open-gate-register.json")
    checklist = load("final/completion-checklist.json")
    skills = load("tooling/skill-validation.json")
    runners = load("tooling/runner-aggregate.json")
    scan = load("evidence/latest-tracked-file-scan.json")
    method = load("tooling/method-flow/validation-x2.json")
    toolbox = load("tooling/meta-tool-box-x2/validation.json")
    privacy = load("validation/closeout-privacy-scan.json")
    cap = load("validation/final-document-cap.json")
    delta = load("validation/final-delta-manifest.json")
    owner = load("final/final-owner-manifest.json")
    staged = load("validation/closeout-staged-review.json")
    baton = (PHASE / "handoffs/tamar-vey-v659-v7-activation.md").read_text(encoding="utf-8")

    check("owner", truth["owner"] == "Liora Venn")
    check("phase", truth["phase"] == "v659-v6")
    check("frozen_chain", truth["effective_frozen"] == expected_frozen)
    check("effective_negatives", truth["effective_negatives"] == expected_negatives)
    check("effective_methods", truth["effective_methods"] == expected_methods)
    check("open_gaps", truth["effective_open_gaps"] == expected_gaps)
    check("exact_gates", truth["effective_exact_gates"] == expected_gates)
    check("terminal_verdict", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20")
    check("x2_evidence", truth["x2_evidence"] == EVIDENCE_COMMIT)
    check("outcome_total", outcomes["proposal_count"] == 20 and outcomes["selected_inherited_count"] == 20)
    check("outcome_distribution", Counter(row["observed_outcome"] for row in outcomes["outcomes"]) == Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}))
    check("valid_fixtures", truth["valid_fixtures"] == 20)
    check("mutations", truth["retained_rejected_mutations"] == 100)
    check("candidate_prototypes", truth["candidate_prototypes_completed"] == 10)
    check("cleanup", truth["cleanup_reviews_completed"] == 30)
    check("skills", skills["all_valid"] and skills["valid_skill_count"] == 10)
    check("runners", runners["all_built_tested_used"] and runners["valid_runner_count"] == 10 and runners["runner_count"] == 10)
    check("latest_scan", scan["selected_file_count"] == 5000 and scan["confirmed_high_risk_count"] == 0)
    check("method_flow", method["valid"] and method["method_count"] == 113)
    check("meta_tool", toolbox["valid"] and toolbox["card_count"] == 20)
    check("lifecycle_failure_count", lifecycle["operational_failure_count"] == 42)
    check("lifecycle_arithmetic", lifecycle["effective_negatives"] == expected_negatives and lifecycle["effective_methods"] == expected_methods)
    check("final_method_pair", flow["method_count"] == 10 and flow["witness_count"] == 20)
    check("evidence_receipt", evidence["x2_evidence"] == EVIDENCE_COMMIT and evidence["retained_mutations"] == 100)
    check("gate_register", open_gates["current_open_gaps"] == expected_gaps and open_gates["current_exact_gates"] == expected_gates and open_gates["closed_by_phase"] == 0)
    check("checklist_route_held", "single_acknowledged_send" in checklist["incomplete"])
    check("route_tamar", route["next_exact_title"] == "Tamar Vey" and route["next_phase"] == "v659-v7")
    check("route_after_tamar", route["recipient_next_exact_title"] == "Elowen Cairn" and route["recipient_next_phase"] == "v659-v8")
    check("route_unsent", route["state"] == "HELD_UNTIL_LIORA_EXACT_TERMINAL_GATE" and not route["message_sent"] and not route["task_lookup_performed"])
    check("tavian_standby", route["tavian_sol_state"] == "ON_STANDBY")
    check("baton_words", len(re.findall(r"\b[\w'-]+\b", baton, flags=re.UNICODE)) >= 10_000)
    check("baton_prepared", "PREPARED_BY_LIORA_VENN = true" in baton and "SENT_BY_LIORA_VENN = false" in baton)
    check("baton_route", "ACTIVATION_TARGET_EXACT_TITLE = Tamar Vey" in baton and "ACTIVATION_TARGET_PHASE = v659-v7" in baton)
    check("privacy", privacy["confirmed_hit_count"] == 0 and not privacy["privacy_complete"])
    check("document_cap", cap["passes"] and cap["activation_packet_words"] >= 10_000)
    check("delta_manifest", delta["entry_count"] == len(delta["entries"]) and len(delta["self_exclusions"]) == 4)
    check("owner_manifest", owner["entry_count"] > 220 and owner["below_threshold"] and len(owner["self_exclusions"]) == 3)
    check("staged_review", staged["valid"] and staged["staged_path_count"] > 0 and staged["all_owner_closeout_updates"] and not staged["outside_declared_final_surface"])
    check("accessible_report", (PHASE / "deliverables/v659-v6-accessible-static-report.html").is_file())
    check("overview", (PHASE / "deliverables/v659-v6-final-overview.md").is_file())

    failures = [row for row in checks if not row["passed"]]
    return {
        "schema": "ghc.family.v659-v6.detailed-validation.v1",
        "owner": d.OWNER, "phase": d.PHASE, "check_count": len(checks),
        "passed_count": len(checks) - len(failures), "failed_count": len(failures),
        "checks": checks, "valid": not failures,
        "boundary": "Same-owner structural validation only; not independent reproduction or broader assurance.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    receipt = validate_phase()
    rendered = json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    print(json.dumps({"valid": receipt["valid"], "checks": receipt["check_count"], "passed": receipt["passed_count"]}, sort_keys=True))
    return 0 if receipt["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
