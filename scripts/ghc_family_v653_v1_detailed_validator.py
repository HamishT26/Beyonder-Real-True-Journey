#!/usr/bin/env python3
"""Detailed bounded evidence validator for Vesper Arlen v653-v1."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v653_v1_phase_data as data
from ghc_family_v653_v1_validation_common import PHASE, read_json, write_json


def validate() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def check(name: str, condition: bool, detail: Any) -> None:
        checks.append({"name": name, "passed": bool(condition), "detail": detail})

    outcomes: Counter[str] = Counter()
    mutations = 0
    rejected = 0
    for proposal in data.PROPOSALS:
        target = PHASE / "surfaces" / proposal["slug"]
        contract = read_json(target / "contract.json")
        mutation = read_json(target / "mutation-results.json")
        receipt = read_json(target / "bounded-receipt.json")
        prefix = proposal["proposal_id"]
        check(f"{prefix}:three_files", target.is_dir() and len(list(target.iterdir())) == 3, proposal["slug"])
        check(
            f"{prefix}:identity_and_outcome",
            contract["proposal_id"] == prefix
            and receipt["proposal_id"] == prefix
            and contract["outcome"] == proposal["expected_disposition"]
            and receipt["outcome"] == proposal["expected_disposition"],
            receipt["outcome"],
        )
        check(f"{prefix}:obligations", contract["obligation_count"] >= 6 and len(contract["obligations"]) >= 6, contract["obligation_count"])
        check(
            f"{prefix}:protected_boundaries",
            contract["real_data_rows"] == 0
            and not contract["empirical_confirmation"]
            and not contract["independent_reproduction"]
            and not contract["production_keys_or_credentials"]
            and not contract["participant_or_authority_decision"],
            contract["protected_gates"],
        )
        check(
            f"{prefix}:mutations",
            mutation["mutation_count"] == 5
            and mutation["rejected_count"] == 5
            and all(row["rejected"] and row["credit"] == "retained_negative" for row in mutation["results"]),
            mutation["rejected_count"],
        )
        check(
            f"{prefix}:bounded_receipt",
            receipt["valid_contract"]
            and receipt["all_mutations_rejected"]
            and receipt["real_data_rows"] == 0
            and not any(
                receipt[field]
                for field in (
                    "empirical_confirmation",
                    "independent_reproduction",
                    "production_ready",
                    "professional_validation",
                    "legal_or_cultural_authority",
                    "maori_authority",
                    "complete_accessibility",
                    "exhaustive_security",
                )
            )
            and receipt["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
            receipt["outcome"],
        )
        outcomes[receipt["outcome"]] += 1
        mutations += mutation["mutation_count"]
        rejected += mutation["rejected_count"]

    skill = read_json(PHASE / "skills/skill-build-receipt.json")
    runner = read_json(PHASE / "runners/runner-invocation-receipt.json")
    portfolio = read_json(PHASE / "portfolios/execution-receipt.json")
    final_negative_path = PHASE / "retained-negative-register-final.json"
    negatives = read_json(final_negative_path if final_negative_path.is_file() else PHASE / "retained-negative-register-x2.json")
    gates = read_json(PHASE / "exact-open-gate-register-x2.json")
    final_method_path = PHASE / "method-flow/final-method-flow-ledger.json"
    methods = read_json(final_method_path if final_method_path.is_file() else PHASE / "method-flow/evidence-method-flow-ledger.json")
    truth = read_json(PHASE / "phase-truth.json")
    threshold = read_json(PHASE / "validation/owner-file-threshold-receipt.json")
    workflow = read_json(PHASE / "workflow/workflow-plan-validation.json")
    workflow_issues = read_json(PHASE / "workflow/workflow-plan-issues.json")
    route_overlay = read_json(PHASE / "workflow/current-live-route-overlay.json")
    reflection = read_json(PHASE / "reflection-remaster/x2-remaster-decision.json")
    overview_words = len((PHASE / "reports/x1-integrated-overview.md").read_text(encoding="utf-8").split())
    report = (PHASE / "reports/evidence-static-report.html").read_text(encoding="utf-8")

    expected = Counter({"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1})
    check("aggregate:outcomes", outcomes == expected, dict(outcomes))
    check("aggregate:proposal_count", sum(outcomes.values()) == 30, sum(outcomes.values()))
    check("aggregate:mutations", mutations == 150 and rejected == 150, {"mutations": mutations, "rejected": rejected})
    check("aggregate:skills", skill["initialized_count"] == skill["customized_count"] == skill["quick_validated_count"] == 10 and not skill["globally_installed"], skill)
    check("aggregate:runners", runner["runner_count"] == runner["invoked_count"] == runner["valid_count"] == 10, runner["valid_count"])
    check("aggregate:portfolios", portfolio["unresolved_authorized_internal_tasks"] == 0 and portfolio["safe_now"]["resolved"] == 30 and portfolio["candidate"]["resolved"] == 30, portfolio)
    expected_negatives = negatives["effective_total"]
    synthetic_preserved = read_json(PHASE / "retained-negative-register-x2.json")["synthetic_mutation_count"] == 150
    check("aggregate:negatives", truth["effective_negatives"] == expected_negatives and negatives["none_erased"] and synthetic_preserved, negatives["effective_total"])
    check("aggregate:gates", gates["effective_open_gaps"] == 70 and gates["effective_exact_gates"] == 71 and gates["none_silently_closed"], gates)
    expected_methods = methods["counts"]["methods"]
    check(
        "aggregate:method_flow",
        methods["counts"]["witness_results"] == {"fail": expected_methods, "pass": expected_methods}
        and methods["counts"]["states"]["preferred"] == expected_methods,
        methods["counts"],
    )
    check("aggregate:truth", truth["outcomes"] == dict(expected) and truth["effective_negatives"] == expected_negatives and truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", truth)
    check("aggregate:file_threshold", threshold["below_threshold"] and threshold["owner_generated_file_count"] < 2000, threshold)
    check("aggregate:report_accessibility", 'lang="en"' in report and "<main" in report and "prefers-reduced-motion" in report and "manual" in report.lower(), "static report")
    check("aggregate:overview_words", 1500 <= overview_words <= 100000, overview_words)
    check(
        "aggregate:workflow",
        workflow["status"] == "needs_refinement"
        and not workflow["valid"]
        and workflow["policy_checks"] == 20
        and workflow["policy_checks_passed"] == 19
        and workflow_issues["counts"]["errors"] == 1
        and [row["code"] for row in workflow_issues["issues"]]
        == ["policy_messaging_boundary"]
        and not route_overlay["tool_result_promoted_to_activation_authority"],
        workflow["status"],
    )
    check("aggregate:reflection", reflection["decision"] == "additive_specialized_surfaces" and reflection["globally_installed"] == [], reflection["decision"])

    return {
        "schema": "ghc.family.v653-v1.detailed-validation.v1",
        "check_count": len(checks),
        "passed_count": sum(row["passed"] for row in checks),
        "checks": checks,
        "valid": all(row["passed"] for row in checks),
        "boundary": "Bounded same-owner symbolic, structural, and software evidence only.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    result = validate()
    if args.receipt:
        write_json(args.receipt, result)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    if not result["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
