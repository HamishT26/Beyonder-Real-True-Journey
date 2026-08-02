#!/usr/bin/env python3
"""Exact-final lifecycle and committed-tree validator for Lyren's remaster."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Callable

import ghc_family_v658_v8_2_remaster_data as d


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_COMMIT = "e08a7bb24c9fc9c442374d251b985437a88ade11"


def git(*args: str, text: bool = True) -> str | bytes:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=text,
        encoding="utf-8" if text else None,
    )
    return result.stdout.strip() if text else result.stdout


def blob(revision: str, path: str) -> bytes:
    return git("show", f"{revision}:{path}", text=False)  # type: ignore[return-value]


def payload(revision: str, path: str) -> Any:
    return json.loads(blob(revision, path).decode("utf-8"))


def validate_final(expected_final: str) -> dict[str, Any]:
    passed: list[str] = []
    errors: list[str] = []

    def check(name: str, predicate: bool | Callable[[], bool]) -> None:
        try:
            valid = predicate() if callable(predicate) else predicate
        except Exception as exc:
            errors.append(f"{name}: {type(exc).__name__}: {exc}")
            return
        (passed if valid else errors).append(name)

    head = str(git("rev-parse", "HEAD"))
    branch = str(git("branch", "--show-current"))
    upstream = str(git("rev-parse", "@{upstream}"))
    tracking = str(git("rev-parse", f"refs/remotes/origin/{branch}"))
    live_line = str(git("ls-remote", "--heads", "origin", f"refs/heads/{branch}"))
    live = live_line.split()[0] if live_line else ""
    divergence = [int(value) for value in str(git("rev-list", "--left-right", "--count", "@{upstream}...HEAD")).split()]
    commits = str(git("rev-list", "--reverse", f"{d.SOURCE_FINAL}..{head}")).splitlines()
    truth = payload(head, f"{d.PHASE_ROOT}/final/final-truth.json")
    route = payload(head, f"{d.PHASE_ROOT}/route/prepared-route.json")
    privacy = payload(head, f"{d.PHASE_ROOT}/validation/closeout-privacy-scan.json")
    plan = payload(head, f"{d.PHASE_ROOT}/validation/canonical-pass-plan.json")
    baton = blob(head, f"{d.PHASE_ROOT}/handoffs/ilyra-fen-v659-v1-activation.md").decode("utf-8")

    check("exact_head", head == expected_final)
    check("exact_branch", branch == d.BRANCH)
    check("clean", str(git("status", "--porcelain=v1")) == "")
    check("final_parent", str(git("rev-parse", f"{head}^")) == EVIDENCE_COMMIT)
    check("evidence_parent", str(git("rev-parse", f"{EVIDENCE_COMMIT}^")) == d.X1_FREEZE)
    check("x1_parent", str(git("rev-parse", f"{d.X1_FREEZE}^")) == d.SOURCE_FINAL)
    check("three_commits", len(commits) == 3)
    check("zero_merges", str(git("rev-list", "--merges", "--count", f"{d.SOURCE_FINAL}..{head}")) == "0")
    check(
        "single_parent_commits",
        all(len(str(git("rev-list", "--parents", "-n", "1", commit)).split()) == 2 for commit in commits),
    )
    check("local_upstream_equal", head == upstream)
    check("local_tracking_equal", head == tracking)
    check("local_live_equal", head == live)
    check("zero_divergence", divergence == [0, 0])
    check("truth_evidence", truth["x2_evidence"] == EVIDENCE_COMMIT)
    check("truth_frozen", truth["effective_frozen"] == 2910)
    check("truth_negatives", truth["effective_negatives"] == 18078)
    check("truth_methods", truth["effective_methods"] == 4352)
    check("truth_gaps_gates", truth["effective_open_gaps"] == 121 and truth["effective_exact_gates"] == 120)
    check("truth_verdict", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20")
    check("route_unsent", route["state"] == "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED" and not route["message_sent"])
    check("route_ilyra", route["next_exact_title"] == "Ilyra Fen" and route["next_phase"] == "v659-v1")
    check("route_auren", route["recipient_next_exact_title"] == "Auren Lark" and route["recipient_next_phase"] == "v659-v2")
    check("tavian_standby", route["tavian_sol_state"] == "ON_STANDBY")
    check("canonical_plan_unspent", plan["state"] == "NOT_RUN_FINAL_CANDIDATE_REQUIRED")
    check("privacy_zero", privacy["hit_count"] == 0 and len(privacy["classes"]) == 5)
    check("privacy_not_complete", not privacy["privacy_complete"] and not privacy["security_complete"])
    check("baton_word_floor", len(re.findall(r"\b[\w'-]+\b", baton, flags=re.UNICODE)) >= 10000)
    check("baton_prepared", "SENT_BY_LYREN_MOSS = false" in baton)
    check("baton_no_private_path", "C:\\Users\\" not in baton and "D:\\GHC-Archives\\" not in baton)
    check("baton_no_trailing_whitespace", all(line == line.rstrip() for line in baton.splitlines()))

    replay_count = 0
    for manifest_path in [
        f"{d.PHASE_ROOT}/validation/final-delta-manifest.json",
        f"{d.PHASE_ROOT}/final/final-owner-manifest.json",
    ]:
        manifest = payload(head, manifest_path)
        valid = manifest["entry_count"] == len(manifest["entries"])
        for row in manifest["entries"]:
            data = blob(head, row["path"])
            valid = valid and len(data) == row["bytes"] and hashlib.sha256(data).hexdigest() == row["sha256"]
            replay_count += 1
        check(f"committed_manifest:{manifest_path}", valid)

    phase_paths = [
        path
        for path in str(git("ls-tree", "-r", "--name-only", head, d.PHASE_ROOT)).splitlines()
        if path
    ]
    json_count = 0
    json_valid = True
    for path in phase_paths:
        if path.endswith(".json"):
            try:
                json.loads(blob(head, path).decode("utf-8"))
                json_count += 1
            except Exception:
                json_valid = False
    check("all_phase_json", json_valid and json_count > 200)
    check("phase_file_count_bounded", 250 <= len(phase_paths) < 2000)

    return {
        "schema": "ghc.family.v658-v8-2-remaster.final-validation.v1",
        "phase": d.PHASE,
        "head": head,
        "check_count": len(passed) + len(errors),
        "passed_count": len(passed),
        "error_count": len(errors),
        "checks": passed,
        "errors": errors,
        "manifest_replay_count": replay_count,
        "phase_json_count": json_count,
        "phase_file_count": len(phase_paths),
        "valid": not errors,
        "boundary": "Exact-final same-owner lifecycle validation only; not independent reproduction or broader assurance.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-final", required=True)
    args = parser.parse_args()
    result = validate_final(args.expected_final)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
