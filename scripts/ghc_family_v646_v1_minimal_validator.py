#!/usr/bin/env python3
"""Minimal fail-closed validator for the Eiren v646-v1 packet."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/eiren-kestrel/v646-v1"
SOURCE = "6dc3311e3c4c390c945d001f75fb17d320c0a548"
X1 = "7b7824b7643bfb3a80cf778a10ca65055554b5db"


def load(name: str) -> Any:
    return json.loads((PHASE / name).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "git command failed")
    return result.stdout.strip()


def validate(expected_head: str | None, require_clean: bool) -> dict[str, Any]:
    issues: list[str] = []
    checks: list[dict[str, Any]] = []

    def check(name: str, condition: bool, detail: str) -> None:
        checks.append({"name": name, "passed": bool(condition), "detail": detail})
        if not condition:
            issues.append(f"{name}: {detail}")

    proposals = load("x1-proposals.json")
    ledger = load("x2-proposal-ledger.json")
    truth = load("phase-truth.json")
    negatives = load("retained-negative-register.json")
    gates = load("open-exact-gate-register.json")
    approval = load("approval-packets/x2-execution-ledger.json")
    skills = load("prototypes/skill-build-receipt.json")
    runners = load("prototypes/runner-build-receipt.json")
    cleanup = load("maintenance/x2-clean-refine-receipt.json")
    manifest = load("validation/evidence-manifest.json")
    head = git("rev-parse", "HEAD")
    dirty = git("status", "--porcelain=v1", "-uno")
    merges = int(git("rev-list", "--merges", "--count", f"{SOURCE}..{head}") or "0")
    phase_commits = int(git("rev-list", "--count", f"{SOURCE}..{head}") or "0")

    check("proposal_count", len(proposals.get("proposals", [])) == 10, "exactly ten proposals required")
    check("frozen_chain", proposals.get("frozen_chain_count_after_x1") == 400, "frozen chain must total 400")
    check("outcome_count", len(ledger.get("outcomes", [])) == 10, "exactly ten outcomes required")
    check("outcome_distribution", ledger.get("outcome_distribution") == {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}, "required 6/2/1/1 distribution")
    check("stage20", truth.get("terminal_verdict") == "NOT_READY_FOR_STAGE_20", "terminal abstention required")
    check("zero_real_evidence", all(truth.get(key) == 0 for key in ("real_data_rows_ingested", "likelihood_evaluations", "real_participants", "real_keys_or_proofs", "real_operational_actions")), "real-evidence counters must remain zero")
    check("negative_total", negatives.get("effective_total") == 2506 and negatives.get("erased_count") == 0, "2,506 negatives and zero erasures required")
    check("gate_preservation", gates.get("inherited_open_gap_count") == 10 and gates.get("inherited_exact_gate_count") == 11 and gates.get("silently_closed_count") == 0, "inherited gates must remain open")
    check("approval_counts", approval.get("safe_now_executed") == 30 and approval.get("candidates_executed") == 20, "expanded safe/candidate counts required")
    check("approval_boundaries", approval.get("exact_or_external_packets_executed") == 0 and approval.get("blocked_packets_executed") == 0, "exact and blocked packets must remain unexecuted")
    check("skills", skills.get("valid") is True and skills.get("validated_count") == 20, "twenty skills must validate")
    check("runners", runners.get("valid") is True and runners.get("used_count") == 10, "ten runners must be used")
    check("cleanup", cleanup.get("valid") is True and cleanup.get("completed_count") == 30 and cleanup.get("destructive_action_count") == 0, "thirty non-destructive cleanup receipts required")
    check("manifest", manifest.get("entry_count") == len(manifest.get("entries", [])) and manifest.get("entry_count", 0) >= 120, "manifest count and minimum surface required")
    check("source_ancestry", subprocess.run(["git", "merge-base", "--is-ancestor", SOURCE, head], cwd=ROOT).returncode == 0, "source must be ancestral")
    check("x1_ancestry", subprocess.run(["git", "merge-base", "--is-ancestor", X1, head], cwd=ROOT).returncode == 0, "x1 must be ancestral")
    check("zero_merges", merges == 0, "phase history must have zero merges")
    check("commit_cap", phase_commits <= 4, "phase history must remain within four commits")
    check("expected_head", expected_head is None or head == expected_head, "HEAD must match the requested revision")
    check("clean_state", not require_clean or not dirty, "clean worktree required")

    return {
        "schema": "ghc.family.v646-v1.minimal-validation.v1",
        "head": head,
        "expected_head": expected_head,
        "check_count": len(checks),
        "checks": checks,
        "phase_commit_count": phase_commits,
        "merge_count": merges,
        "clean_required": require_clean,
        "clean": not bool(dirty),
        "issues": issues,
        "valid": not issues,
        "boundary": "Minimal validation is owner-scoped structural evidence, not empirical confirmation or independent reproduction.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head")
    parser.add_argument("--require-clean", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = validate(args.expected_head, args.require_clean)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8", newline="\n")
    else:
        print(payload, end="")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
