#!/usr/bin/env python3
"""Validate the Orin Thale v647-v8 x1-only packet."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/orin-thale/v647-v8"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def main() -> int:
    checks: list[dict[str, object]] = []

    def check(name: str, condition: bool, detail: object) -> None:
        checks.append({"check": name, "passed": bool(condition), "detail": detail})

    proposals = load("x1-proposals.json")
    approval = load("approval-packets/x1-approval-portfolio.json")
    plan = load("prototypes/x1-skill-runner-plan.json")
    cleanup = load("maintenance/x1-clean-refine-plan.json")
    sources = load("sources/source-ledger.json")
    proposal_audit = load("provenance/prior-proposal-collision-audit.json")
    portfolio_audit = load("provenance/prior-portfolio-collision-audit.json")
    negatives = load("retained-negative-register.json")
    methods = load("method-flow/method-flow-state.json")
    gates = load("exact-open-gate-register.json")
    route = load("orchestration/terminal-route-plan.json")
    freeze = load("reproduction/x1-freeze-contract.json")

    check("ten proposals", len(proposals["proposals"]) == 10, len(proposals["proposals"]))
    check("540 prior proposals", proposals["prior_frozen_proposal_count"] == 540, proposals["prior_frozen_proposal_count"])
    check("550 after x1", proposals["frozen_chain_count_after_x1"] == 550, proposals["frozen_chain_count_after_x1"])
    check("x1 only", proposals["freeze_stage"] == "x1_only" and proposals["x2_execution_present"] is False, proposals["freeze_stage"])
    expected = Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})
    check("expected distribution", Counter(row["expected_disposition"] for row in proposals["proposals"]) == expected, proposals["expected_distribution"])
    required = {"hypothesis", "null_or_failure", "approval_class", "execution_lane", "current_primary_or_official_source_needs", "concrete_artifacts", "test_falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates", "expected_disposition"}
    check("proposal fields", all(required <= set(row) for row in proposals["proposals"]), sorted(required))
    check("proposal novelty", proposal_audit["valid"] and proposal_audit["exact_collision_count"] == 0, proposal_audit["exact_collision_count"])
    check("portfolio novelty", portfolio_audit["valid"] and portfolio_audit["exact_collision_count"] == 0, portfolio_audit["exact_collision_count"])
    check("portfolio floors", (approval["safe_now_count"], approval["candidate_count"], plan["skill_count"], plan["runner_count"], cleanup["task_count"]) == (30, 20, 20, 10, 30), [approval["safe_now_count"], approval["candidate_count"], plan["skill_count"], plan["runner_count"], cleanup["task_count"]])
    check("inherited gates visible", approval["exact_approval_count"] == 10 and approval["blocked_count"] == 5 and not approval["inherited_exact_and_blocked_receive_new_completion_credit"], [approval["exact_approval_count"], approval["blocked_count"]])
    check("no x2 credit", approval["x2_completion_credit"] == 0 and plan["x2_completion_credit"] == 0 and cleanup["x2_completion_credit"] == 0, 0)
    check("source vocabulary", set(sources["status_counts"]) <= {"current", "stable", "draft", "watch"}, sources["status_counts"])
    check("source boundary", sources["real_rows"] == 0 and sources["real_people_or_operations"] == 0 and sources["real_keys_or_tokens"] == 0 and not sources["authority_delegated"], [sources["real_rows"], sources["real_people_or_operations"], sources["real_keys_or_tokens"]])
    check("negative preservation", negatives["inherited_effective_negatives"] == 3753 and negatives["x1_operational_negative_count"] == 8 and negatives["erased_negative_count"] == 0, negatives["effective_x1_total"])
    check("method parity", methods["counts"]["methods"] == 8 and methods["counts"]["witness_results"] == {"fail": 8, "pass": 8}, methods["counts"])
    check("gate carry", gates["inherited_open_gaps"] == 24 and gates["inherited_exact_gates"] == 25 and gates["closed_in_x1"] == 0, [gates["inherited_open_gaps"], gates["inherited_exact_gates"]])
    check("route held", route["state"] == "PREPARED_NOT_SENT" and not route["task_creation_authorized"], route["state"])
    check("replay bounded", freeze["same_owner_replay_only"] and not freeze["independent_reproduction"], freeze["same_owner_replay_only"])
    check("phase file threshold", sum(1 for path in PHASE.rglob("*") if path.is_file()) < 15000, sum(1 for path in PHASE.rglob("*") if path.is_file()))

    privacy_patterns = {
        "raw_uuid": re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}\b"),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/]"),
        "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*[^\s,}]+"),
        "delegation_markup": re.compile("<codex_" + "delegation", re.IGNORECASE),
        "private_uri": re.compile("(?:codex|app)" + r"://", re.IGNORECASE),
    }
    hits = []
    for path in PHASE.rglob("*"):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for kind, pattern in privacy_patterns.items():
            if pattern.search(text):
                hits.append({"path": path.relative_to(ROOT).as_posix(), "class": kind})
    check("phase privacy scan", not hits, hits)

    word_violations = []
    for path in PHASE.rglob("*"):
        if path.suffix.lower() not in {".md", ".html"}:
            continue
        count = len(re.findall(r"\b\w+\b", path.read_text(encoding="utf-8", errors="replace")))
        if count > 6000:
            word_violations.append({"path": path.relative_to(ROOT).as_posix(), "words": count})
    check("document cap", not word_violations, word_violations)

    valid = all(row["passed"] for row in checks)
    payload = {"schema": "ghc.family.v647-v8.x1-review.v1", "check_count": len(checks), "issue_count": sum(not row["passed"] for row in checks), "checks": checks, "valid": valid}
    receipt = PHASE / "validation/x1-review.json"
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
