#!/usr/bin/env python3
"""Detailed same-owner validator for Ilyra Fen v659-v1."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

import ghc_family_v659_v1_data as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
EVIDENCE_COMMIT = "88f4734cda8049c887ad7ba12df088e63737c929"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def validate_phase() -> dict:
    checks: list[dict] = []

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
    scan = load("tooling/runner-smoke/ghc_family_observation_provenance_scan.json")
    method = load("tooling/method-flow/validation-x2.json")
    toolbox = load("tooling/meta-tool-box-x2/validation.json")
    privacy = load("validation/closeout-privacy-scan.json")
    cap = load("validation/final-document-cap.json")
    delta = load("validation/final-delta-manifest.json")
    owner = load("final/final-owner-manifest.json")
    staged = load("validation/closeout-staged-review.json")
    baton = (PHASE / "handoffs/auren-lark-v659-v2-activation.md").read_text(encoding="utf-8")

    check("owner", truth["owner"] == "Ilyra Fen")
    check("phase", truth["phase"] == "v659-v1")
    check("frozen_chain", truth["effective_frozen"] == 2930)
    check("effective_negatives", truth["effective_negatives"] == 18317)
    check("effective_methods", truth["effective_methods"] == 4591)
    check("open_gaps", truth["effective_open_gaps"] == 122)
    check("exact_gates", truth["effective_exact_gates"] == 121)
    check("terminal_verdict", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20")
    check("x2_evidence", truth["x2_evidence"] == EVIDENCE_COMMIT)
    check("outcome_total", outcomes["proposal_count"] == 40)
    check("outcome_distribution", Counter(row["observed_outcome"] for row in outcomes["outcomes"]) == Counter({"completed": 33, "represented": 5, "open_gap": 1, "exact_gate": 1}))
    check("valid_fixtures", truth["valid_fixtures"] == 40)
    check("mutations", truth["retained_rejected_mutations"] == 200)
    check("candidate_prototypes", truth["candidate_prototypes_completed"] == 10)
    check("cleanup", truth["cleanup_reviews_completed"] == 30)
    check("skills", skills["all_valid"] and skills["valid_skill_count"] == 10)
    check("runners", runners["all_built_tested_used"] and runners["valid_runner_count"] == 10 and runners["runner_count"] == 10)
    check("latest_scan", scan["selected_file_count"] == 5000 and scan["confirmed_high_risk_count"] == 0)
    check("method_flow", method["valid"] and method["method_count"] == 214)
    check("meta_tool", toolbox["valid"] and toolbox["card_count"] == 20)
    check("lifecycle_failure_count", lifecycle["operational_failure_count"] == 36)
    check("lifecycle_arithmetic", lifecycle["effective_negatives"] == 18317 and lifecycle["effective_methods"] == 4591)
    check("final_method_pair", flow["method_count"] == 9 and flow["witness_count"] == 18)
    check("evidence_receipt", evidence["x2_evidence"] == EVIDENCE_COMMIT and evidence["retained_mutations"] == 200)
    check("gate_register", open_gates["current_open_gaps"] == 122 and open_gates["current_exact_gates"] == 121 and open_gates["closed_by_phase"] == 0)
    check("checklist_route_held", "single_acknowledged_send" in checklist["incomplete"])
    check("route_auren", route["next_exact_title"] == "Auren Lark" and route["next_phase"] == "v659-v2")
    check("route_sable", route["recipient_next_exact_title"] == "Sable Rook" and route["recipient_next_phase"] == "v659-v3")
    check("route_unsent", route["state"] == "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED" and not route["message_sent"] and not route["task_lookup_performed"])
    check("tavian_standby", route["tavian_sol_state"] == "ON_STANDBY")
    check("baton_words", len(re.findall(r"\b[\w'-]+\b", baton, flags=re.UNICODE)) >= 10_000)
    check("baton_prepared", "PREPARED_BY_ILYRA_FEN = true" in baton and "SENT_BY_ILYRA_FEN = false" in baton)
    check("baton_route", "NEXT_EXACT_TITLE = Auren Lark" in baton and "RECIPIENT_NEXT_EXACT_TITLE = Sable Rook" in baton)
    check("privacy", privacy["confirmed_hit_count"] == 0 and not privacy["privacy_complete"])
    check("document_cap", cap["passes"] and cap["activation_packet_words"] >= 10_000)
    check("delta_manifest", delta["entry_count"] == 19 and len(delta["self_exclusions"]) == 5)
    check("owner_manifest", owner["entry_count"] > 300 and owner["below_threshold"] and len(owner["self_exclusions"]) == 2)
    check("staged_review", staged["valid"] and staged["expected_staged_path_count"] == 24)
    check("accessible_report", (PHASE / "deliverables/v659-v1-accessible-static-report.html").is_file())
    check("overview", (PHASE / "deliverables/v659-v1-final-overview.md").is_file())

    failures = [row for row in checks if not row["passed"]]
    return {
        "schema": "ghc.family.v659-v1.detailed-validation.v1",
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
