#!/usr/bin/env python3
"""Build the combined closeout, seal, and final-record candidate for Vesper special."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/vesper-arlen/v651-v7-special-cli-prep"
BASE = "96684c6fd22b33254aa37de2db7990f2e28bd88e"
X1 = "07785aa97b0aa46a4fbf0c60109a8ee8e678aacf"


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=True).stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-commit", required=True)
    args = parser.parse_args()
    if git("rev-parse", "HEAD") != args.evidence_commit:
        raise SystemExit("closeout builder must start at the exact evidence commit")
    if git("status", "--porcelain"):
        # Method Flow closeout additions plus this builder and its tests are
        # expected owner-scoped inputs to the final lifecycle commit.
        changed = git("status", "--porcelain").splitlines()
        allowed = (
            "docs/vesper-arlen/v651-v7-special-cli-prep/method-flow/",
            "scripts/build_ghc_family_v651_v7_special_closeout.py",
            "tests/test_ghc_family_v651_v7_special_closeout.py",
            "tests/test_ghc_family_v651_v7_special_x2.py",
        )
        if not all(any(path in row for path in allowed) for row in changed):
            raise SystemExit("unexpected pre-closeout working-tree changes")

    negative = load("truth/retained-negative-register.json")
    negative["post_evidence_operational"] = 1
    negative["effective_total"] = 7570
    negative["post_evidence_failures"] = [
        "an unanchored lifecycle-path expression misclassified four legitimate nested tooling paths"
    ]
    write("truth/retained-negative-register.json", negative)

    truth = load("truth/phase-truth.json")
    truth["effective_negatives"] = 7570
    truth["evidence_commit"] = args.evidence_commit
    truth["phase_commit_count_before_final"] = 2
    truth["terminal_delivery_state"] = "PREPARED_NOT_SENT"
    write("truth/phase-truth.json", truth)

    overview_path = PHASE / "overview/special-integrated-overview.md"
    overview = overview_path.read_text(encoding="utf-8")
    overview = overview.replace(
        "Effective retained negatives are 7,569: 7,458 inherited from the sealed ordinary v651-v7 phase, five x1 operational failures, six x2 operational failures, and one hundred rejected synthetic mutations.",
        "Effective retained negatives are 7,570: 7,458 inherited from the sealed ordinary v651-v7 phase, five x1 operational failures, six x2 operational failures, one hundred rejected synthetic mutations, and one post-evidence wrapper failure.",
    )
    overview_path.write_text(overview, encoding="utf-8", newline="\n")
    report_path = PHASE / "reports/accessible-static-report.html"
    report = report_path.read_text(encoding="utf-8").replace("Effective negatives: 7,569.", "Effective negatives: 7,570.")
    report_path.write_text(report, encoding="utf-8", newline="\n")

    evidence_validation = load("validation/evidence-validation-credited.json")
    write(
        "lifecycle/anchor-contract.json",
        {
            "schema": "ghc.family.v651-v7-special.anchor-contract.v1",
            "sealed_ordinary_source": BASE,
            "x1": X1,
            "evidence": args.evidence_commit,
            "final_binding": "resolved by the exact-head terminal validator and acknowledged activation message",
            "required_ancestry": [BASE, X1, args.evidence_commit],
            "max_special_commits": 12,
            "planned_special_commits": 3,
            "merge_commits_allowed": 0,
        },
    )
    write(
        "closeout/closeout-receipt.json",
        {
            "schema": "ghc.family.v651-v7-special.closeout.v1",
            "owner": "Vesper Arlen",
            "phase": "v651-v7-special-cli-prep",
            "evidence_commit": args.evidence_commit,
            "evidence_validation": {
                "valid": evidence_validation["valid"],
                "tests": evidence_validation["tests"]["tests_run"],
                "detailed": f"{evidence_validation['checks_passed']}/{evidence_validation['check_count']}",
                "minimal": f"{evidence_validation['minimal_checks_passed']}/{evidence_validation['minimal_check_count']}",
                "json": evidence_validation["json_files"],
                "privacy_files": evidence_validation["privacy_files"],
                "manifest": evidence_validation["manifest_entries"],
            },
            "outcomes": truth["outcomes"],
            "effective_negatives": 7570,
            "effective_open_gaps": 59,
            "effective_exact_gates": 60,
            "future_cli_seats": {"prepared": 8, "named": 0, "launched": 0},
            "immediate_successor": {"owner": "Ilyra Fen", "phase": "v651-v8"},
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "complete": True,
            "boundary": "Owner-scoped closeout only; exact final head and delivery remain terminal gates.",
        },
    )
    write(
        "seal/seal-receipt.json",
        {
            "schema": "ghc.family.v651-v7-special.seal.v1",
            "state": "READY_FOR_FINAL_COMMIT",
            "source": BASE,
            "x1": X1,
            "evidence": args.evidence_commit,
            "intended_final_parent": args.evidence_commit,
            "intended_total_special_commits": 3,
            "zero_merges_required": True,
            "single_parent_required": True,
            "canonical_terminal_passes_required": 1,
            "replay_after_success": False,
            "future_cli_created": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write(
        "final/final-record.json",
        {
            "schema": "ghc.family.v651-v7-special.final-record.v1",
            "state": "FINAL_CANDIDATE_PENDING_EXACT_HEAD_VALIDATION",
            "branch": "codex/GHC-Family/vesper-arlen-v651-v7-special-cli-prep",
            "exact_head_binding": "the terminal validator expected-head argument and acknowledged Ilyra activation message",
            "outcomes": truth["outcomes"],
            "effective_negatives": 7570,
            "effective_open_gaps": 59,
            "effective_exact_gates": 60,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "same_owner_only": True,
            "independent_reproduction": False,
            "delivery_state": "PREPARED_NOT_SENT",
        },
    )
    write(
        "completion/completion-gate-receipt.json",
        {
            "schema": "ghc.family.v651-v7-special.completion-gate.v1",
            "status": "READY_FOR_EXACT_FINAL_VALIDATION",
            "completed_checks": [
                "x1 frozen and four-way equal before x2",
                "evidence committed pushed clean and four-way equal",
                "thirty outcomes resolved within permitted vocabulary",
                "eight future seats prepared unnamed and unlaunched",
                "full file-backed Ilyra baton and compact pointer prepared",
                "all known failures retained through Method Flow or post-evidence register",
            ],
            "open_terminal_gates": ["combined final commit", "push and four-way equality", "one exact-head terminal validation", "one acknowledged Ilyra message"],
            "next_safe_step": "stage and review only closeout seal final manifest validator and related truth updates",
        },
    )
    write(
        "validation/terminal-validation-plan.json",
        {
            "schema": "ghc.family.v651-v7-special.terminal-validation-plan.v1",
            "single_canonical_pass": True,
            "replay_after_success": False,
            "full_repository_suite": {"run": False, "owner": "Eiren Kestrel"},
            "checks": [
                "exact head and clean before after",
                "local upstream tracking fresh live remote equality",
                "source x1 evidence ancestry",
                "three single-parent special commits and zero merges",
                "twenty-six scoped tests",
                "complete phase JSON parsing",
                "five-class privacy scan",
                "exact HEAD owner-manifest parity",
                "word file stale-label and diff hygiene",
                "truth gate future-seat and delivery boundaries",
            ],
        },
    )
    print(json.dumps({"valid": True, "evidence": args.evidence_commit, "negatives": 7570, "delivery": "PREPARED_NOT_SENT"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
