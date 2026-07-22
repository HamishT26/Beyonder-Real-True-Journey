#!/usr/bin/env python3
"""Validate the immutable x1 surface for Ilyra v651-v8 SPECIAL CLI prep."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


PHASE_ROOT = Path("docs/ilyra-fen/v651-v8-special-cli-prep")


def check(condition: bool, label: str, issues: list[str]) -> None:
    if not condition:
        issues.append(label)


def load(repo: Path, rel: str) -> object:
    return json.loads((repo / PHASE_ROOT / rel).read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    repo = args.repo.resolve()
    issues: list[str] = []
    checks = 0

    proposals = load(repo, "preregistration/proposals.json")
    portfolio = load(repo, "portfolios/x1-portfolio-plan.json")
    novelty = load(repo, "provenance/semantic-novelty-audit.json")
    chain = load(repo, "provenance/frozen-chain-proposal-index.json")
    placeholders = load(repo, "cli/future-seat-placeholders.json")
    route = load(repo, "route/candidate-immediate-route.json")
    truth = load(repo, "truth/x1-phase-truth.json")
    workflow = load(repo, "workflow/workflow-plan-request.json")

    assertions = [
        (proposals["count"] == 30, "proposal_count"),
        (len(proposals["proposals"]) == 30, "proposal_rows"),
        (Counter(p["expected_disposition"] for p in proposals["proposals"]) == Counter({"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}), "expected_distribution"),
        (set(proposals["allowed_outcomes"]) == {"completed", "represented", "open_gap", "exact_gate"}, "outcome_vocabulary"),
        (novelty["all_novel"] and len(novelty["audit_rows"]) == 30, "novelty"),
        (chain["prior_count"] == 1150 and chain["count"] == 1180, "proposal_chain"),
        (portfolio["counts"] == {"candidate_tasks": 30, "clean_fix_refine_tasks": 40, "runner_ideas": 12, "safe_now_tasks": 40, "skill_ideas": 20}, "portfolio_counts"),
        (placeholders["named_cli_siblings"] == 0 and placeholders["created_tasks"] == 0 and placeholders["launched_cli_siblings"] == 0, "placeholder_counts"),
        (len(placeholders["placeholders"]) == 8 and all(p["name"] is None for p in placeholders["placeholders"]), "placeholder_identity"),
        (route["immediate_successor"] == {"phase": "v652-v1", "seat": "Sable Rook"}, "immediate_successor"),
        (route["terminal_send_state"] == "HELD_UNTIL_SPECIAL_FINAL_PROOF", "route_hold"),
        (workflow["requirements"]["commit_cap"] == {"total": 12, "x1": 6, "x2": 6}, "special_commit_cap"),
        (workflow["requirements"]["validation"]["replay_policy"] == "skip_when_first_passes", "single_pass_policy"),
        (truth["state"] == "x1_frozen_not_executed", "x1_state"),
        (truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", "terminal_verdict"),
    ]
    for condition, label in assertions:
        checks += 1
        check(condition, label, issues)

    forbidden = ["outcome-ledger.json", "execution-ledger.json", "final-record.json", "seal-receipt.json"]
    present = {p.name for p in (repo / PHASE_ROOT).rglob("*") if p.is_file()}
    for name in forbidden:
        checks += 1
        check(name not in present, f"x2_file_present:{name}", issues)

    receipt = {
        "checks": checks,
        "issues": issues,
        "no_x2_outcomes": not any(name in present for name in forbidden),
        "passed": not issues,
        "phase": "v651-v8-special-cli-prep",
        "schema": "ghc.family.x1-validation.v1",
    }
    if args.receipt:
        target = args.receipt if args.receipt.is_absolute() else repo / args.receipt
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(receipt, sort_keys=True))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
