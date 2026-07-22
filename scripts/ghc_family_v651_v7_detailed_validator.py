#!/usr/bin/env python3
"""Detailed phase-local validator for Vesper v651-v7."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/vesper-arlen/v651-v7"


def load(relative: str) -> dict[str, Any]:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def validate() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    def check(name: str, observed: Any, expected: Any) -> None:
        checks.append({"name": name, "observed": observed, "expected": expected, "passed": observed == expected})
    proposal = load("preregistration/proposals.json")
    outcomes = load("outcomes/core-outcomes.json")
    negatives = load("truth/retained-negative-register-x2.json")
    gates = load("gates/exact-open-gate-register.json")
    portfolio = load("portfolios/x2-portfolio-outcomes.json")
    skills = load("tooling/skill-build-receipt.json")
    runners = load("tooling/runner-build-receipt.json")
    method = load("method-flow/method-flow-ledger.json")
    truth = load("truth/evidence-phase-truth.json")
    manifest = load("validation/evidence-staged-manifest.json")
    privacy = load("validation/evidence-staged-privacy.json")
    review = load("validation/evidence-staged-review.json")
    check("proposal_count", proposal["new_proposal_count"], 30)
    check("frozen_chain", proposal["frozen_rows_after_x1"], 1090)
    check("outcome_count", outcomes["proposal_count"], 30)
    check("completed", outcomes["outcome_counts"]["completed"], 23)
    check("represented", outcomes["outcome_counts"]["represented"], 5)
    check("open_gap", outcomes["outcome_counts"]["open_gap"], 1)
    check("exact_gate", outcomes["outcome_counts"]["exact_gate"], 1)
    check("mutation_count", load("validation/mutation-execution-receipt.json")["executed"], 100)
    check("mutation_rejected", load("validation/mutation-execution-receipt.json")["rejected"], 100)
    check("mutation_accepted", load("validation/mutation-execution-receipt.json")["accepted"], 0)
    check("effective_negatives", negatives["effective_total"], 7452)
    check("failures_erased", negatives["failures_erased"], 0)
    check("open_gaps", gates["effective_open_gaps"], 59)
    check("exact_gates", gates["effective_exact_gates"], 60)
    check("silently_closed", gates["silently_closed"], 0)
    check("safe_now", portfolio["counts"]["safe_now_completed"], 30)
    check("candidate", portfolio["counts"]["candidate_resolved"], 20)
    check("skills", skills["skill_count"], 12)
    check("skills_valid", all(row["valid"] for row in skills["skills"]), True)
    check("runners", runners["runner_count"], 10)
    check("runners_valid", all(row["valid"] for row in runners["runners"]), True)
    check("unique_surfaces", runners["unique_surface_coverage"], 30)
    check("method_count", method["counts"]["methods"], 14)
    check("method_failures", method["counts"]["witness_results"]["fail"], 14)
    check("method_passes", method["counts"]["witness_results"]["pass"], 14)
    check("real_rows", truth["real_data_rows"], 0)
    check("participants", truth["participants"], 0)
    check("real_keys", truth["real_keys_or_tokens"], 0)
    check("authority_decisions", truth["authority_decisions"], 0)
    check("production_actions", truth["production_actions"], 0)
    check("future_cli_launched", truth["future_cli_seats_launched"], 0)
    check("independent_reproduction", truth["independent_reproduction"], False)
    check("verdict", truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
    check("privacy_confirmed_hits", privacy["confirmed_hit_count"], 0)
    check("manifest_review_count", manifest["entry_count"] + len(manifest["self_exclusions"]), review["intended_path_count"])
    check("out_of_scope", review["out_of_scope_paths"], [])
    check("overview_minimum", len((ROOT / "overview/integrated-overview.md").read_text(encoding="utf-8").split()) >= 2500, True)
    check("overview_cap", len((ROOT / "overview/integrated-overview.md").read_text(encoding="utf-8").split()) <= 100000, True)
    check("allowed_labels", sorted({row["truth_label"] for row in outcomes["outcomes"]}), sorted(["completed", "represented", "open_gap", "exact_gate"]))
    return {"schema": "ghc.family.v651-v7.detailed-validation.v1", "check_count": len(checks), "passed_count": sum(row["passed"] for row in checks), "checks": checks, "valid": all(row["passed"] for row in checks), "boundary": "Phase-local structural validation only."}


def main() -> None:
    print(json.dumps(validate(), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
