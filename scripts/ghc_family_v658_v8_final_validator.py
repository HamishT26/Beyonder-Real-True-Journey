#!/usr/bin/env python3
"""Exact-final validator for Lyren Moss v658-v8."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import ghc_family_v658_v8_phase_data as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
X1_COMMIT = "3a7cc57b4d1637b4de1836648a57419422bb517f"
EVIDENCE_COMMIT = "88a4d48e2b98494c0861996a8f61a7ea7c696fb6"
BRANCH_REF = "refs/heads/codex/GHC-Family/lyren-moss-v658-v8-full-tools"
TRACKING_REF = "refs/remotes/origin/codex/GHC-Family/lyren-moss-v658-v8-full-tools"


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


def validate_final(
    exact_final: str | None = None, *, require_remote: bool = False
) -> dict[str, Any]:
    checks: list[str] = []
    errors: list[str] = []

    def check(name: str, condition: bool, detail: str = "") -> None:
        checks.append(name)
        if not condition:
            errors.append(f"{name}:{detail}")

    truth = load("truth/phase-truth.json")
    x2_truth = load("truth/phase-truth-x2.json")
    negatives = load("truth/retained-negative-register-final.json")
    flow = load("method-flow/method-flow-state-final.json")
    bridge = load("truth/truth-bridge-final.json")
    closeout = load("closeout/closeout-receipt.json")
    seal = load("seal/seal-receipt.json")
    route = load("orchestration/route-state-final-candidate.json")
    review = load("validation/closeout-staged-review.json")
    caps = load("validation/final-caps.json")
    privacy = load("validation/closeout-privacy-scan.json")
    evidence_manifest = load("validation/evidence-commit-local-manifest.json")
    delta_manifest = load("validation/final-delta-manifest.json")
    owner_manifest = load("final/final-owner-manifest.json")
    prerequisites = load("final/final-validation-prerequisites.json")

    check("owner", truth["owner"] == d.OWNER)
    check("phase", truth["phase"] == d.PHASE)
    check("source", truth["source_final"] == d.SOURCE_FINAL)
    check("x1", truth["x1_commit"] == X1_COMMIT)
    check("evidence", truth["evidence_commit"] == EVIDENCE_COMMIT)
    check("outcomes", truth["outcome_counts"] == d.EXPECTED_DISTRIBUTION)
    check("proposal_chain", truth["effective_frozen_proposals"] == 2890)
    check("negative_bridge", truth["effective_negatives"] == negatives["effective_count"])
    check("negative_inheritance", negatives["evidence_effective_count"] == x2_truth["effective_negatives"])
    check("all_failures_retained", negatives["all_retained"] is True)
    check("methods", truth["effective_methods"] == flow["counts"]["effective_methods"])
    check("method_inheritance", flow["counts"]["inherited_methods"] == x2_truth["effective_methods"])
    check("method_failures_retained", flow["all_failed_witnesses_retained"] is True)
    check("gaps", truth["effective_open_gaps"] == 120)
    check("gates", truth["effective_exact_gates"] == 119)
    check("labels", bridge["allowed_labels"] == ["completed", "represented", "open_gap", "exact_gate"])
    check("none_closed", bridge["none_silently_closed"] is True)
    check("not_ready", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20")
    check("same_owner_only", truth["same_owner_only"] is True)
    check("not_independent", truth["independent_reproduction"] is False)
    check("route_open_gap", route["state"] == "OPEN_ROUTE_GAP")
    check("route_null", route["next_exact_title"] is None and route["next_phase"] is None)
    check("route_unsent", route["message_sent"] is False)
    check("route_no_creation", route["task_created"] is False and route["task_forked"] is False)
    check("route_no_delegation", route["delegated"] is False and route["subagent_spawned"] is False)
    check("tavian_standby", route["tavian_sol_state"] == "ON_STANDBY")
    check("closeout_route", closeout["route_state"] == "OPEN_ROUTE_GAP")
    check("no_successor_authority", closeout["successor_authorized"] is False)
    check("seal_evidence", seal["evidence_commit"] == EVIDENCE_COMMIT)
    check("seal_postcommit_gate", seal["postcommit_exact_final_validation_required"] is True)
    check("privacy", privacy["valid"] is True and privacy["hit_count"] == 0)
    check("evidence_manifest_count", evidence_manifest["entry_count"] == 208)
    check("evidence_manifest_unique", evidence_manifest["entry_count"] == len({row["path"] for row in evidence_manifest["entries"]}))
    check("delta_manifest_count", delta_manifest["entry_count"] == len(delta_manifest["entries"]))
    check("delta_manifest_unique", delta_manifest["entry_count"] == len({row["path"] for row in delta_manifest["entries"]}))
    check("owner_manifest_count", owner_manifest["entry_count"] == len(owner_manifest["entries"]))
    check("owner_manifest_unique", owner_manifest["entry_count"] == len({row["path"] for row in owner_manifest["entries"]}))
    check("owner_cap", owner_manifest["below_threshold"] is True)
    check("commit_cap", caps["within_commit_cap_if_direct_final"] is True)
    check("canonical_limit", load("validation/terminal-gate-plan.json")["canonical_pass_limit"] == 1)
    check("no_replay", load("validation/terminal-gate-plan.json")["replay_after_success_permitted"] is False)
    check("prerequisites_pending_in_tree", prerequisites["completed"] is False)
    check("no_final_preclaim", prerequisites["preclaims_exact_final"] is False)
    check("no_canonical_preclaim", prerequisites["preclaims_canonical_success"] is False)
    check("no_route_preclaim", prerequisites["preclaims_route_sent"] is False)

    if exact_final is not None:
        check("exact_head", git("rev-parse", "HEAD") == exact_final)
        check("final_direct_child", git("rev-parse", f"{exact_final}^") == EVIDENCE_COMMIT)
        check("x1_direct_child_source", git("rev-parse", f"{X1_COMMIT}^") == d.SOURCE_FINAL)
        commits = git("rev-list", "--reverse", f"{d.SOURCE_FINAL}..{exact_final}").splitlines()
        check("three_new_commits", len(commits) == 3, str(commits))
        merges = git("rev-list", "--merges", f"{d.SOURCE_FINAL}..{exact_final}").splitlines()
        check("zero_merges", not merges, str(merges))
        parent_counts = [
            len(git("rev-list", "--parents", "-n", "1", commit).split()) - 1
            for commit in commits
        ]
        check("single_parent_history", parent_counts == [1, 1, 1], str(parent_counts))
        check("under_eight_commit_cap", len(commits) <= 8)
        final_paths = sorted(
            line
            for line in git(
                "diff-tree", "--no-commit-id", "--name-only", "-r", exact_final
            ).splitlines()
            if line
        )
        check("final_path_count", len(final_paths) == review["expected_staged_path_count"])
        check("final_path_set", final_paths == review["expected_staged_paths"])
        check("review_exact", review["state"] == "EXACT_INDEX_REVIEW_PASSED")
        check("review_zero_exceptions", not review["deletions"] and not review["x1_or_evidence_changed_paths"] and not review["outside_owner_paths"])

        evidence_bad = [
            row["path"]
            for row in evidence_manifest["entries"]
            if git("rev-parse", f"{EVIDENCE_COMMIT}:{row['path']}") != row["git_blob"]
        ]
        check("evidence_manifest_replay", not evidence_bad, str(evidence_bad))
        delta_bad = [
            row["path"]
            for row in delta_manifest["entries"]
            if git("rev-parse", f"{exact_final}:{row['path']}") != row["git_blob"]
        ]
        check("delta_manifest_replay", not delta_bad, str(delta_bad))
        owner_bad = [
            row["path"]
            for row in owner_manifest["entries"]
            if git("rev-parse", f"{exact_final}:{row['path']}") != row["git_blob"]
        ]
        check("owner_manifest_replay", not owner_bad, str(owner_bad))
        for relative in delta_manifest["self_exclusions"]:
            check(
                f"delta_self:{relative}",
                bool(git("rev-parse", f"{exact_final}:{d.PHASE_ROOT}/{relative}")),
            )
        for relative in owner_manifest["self_exclusions"]:
            check(
                f"owner_self:{relative}",
                bool(git("rev-parse", f"{exact_final}:{d.PHASE_ROOT}/{relative}")),
            )
        status = git("-c", "core.fsmonitor=false", "status", "--porcelain=v1", "--untracked-files=all")
        check("clean", status == "", status)

        if require_remote:
            local = git("rev-parse", "HEAD")
            upstream = git("rev-parse", "@{upstream}")
            tracking = git("rev-parse", TRACKING_REF)
            live_line = git(
                "-c",
                "credential.interactive=never",
                "ls-remote",
                "--heads",
                "origin",
                BRANCH_REF,
            )
            live = live_line.split()[0] if live_line else ""
            divergence = git("rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()
            check("four_way_equality", local == upstream == tracking == live == exact_final, str([local, upstream, tracking, live]))
            check("zero_divergence", divergence == ["0", "0"], str(divergence))

    return {
        "valid": not errors,
        "check_count": len(checks),
        "checks": checks,
        "error_count": len(errors),
        "errors": errors,
        "exact_final": exact_final,
        "remote_required": require_remote,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--exact-final")
    parser.add_argument("--require-remote", action="store_true")
    parser.add_argument("--json")
    args = parser.parse_args()
    result = validate_final(args.exact_final, require_remote=args.require_remote)
    if args.json:
        path = ROOT / args.json
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    print(
        json.dumps(
            {
                "valid": result["valid"],
                "checks": result["check_count"],
                "errors": result["error_count"],
            }
        )
    )
    if not result["valid"]:
        for error in result["errors"]:
            print(error, file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
