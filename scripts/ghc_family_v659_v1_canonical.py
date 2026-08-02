#!/usr/bin/env python3
"""Run one attributable exact-final canonical aggregate for Ilyra v659-v1."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import platform
import subprocess
import unittest
from datetime import datetime, timezone
from pathlib import Path

import ghc_family_v659_v1_data as d
from ghc_family_v659_v1_final_validator import validate_final
from ghc_family_v659_v1_minimal import validate_minimal
from ghc_family_v659_v1_validator import validate_phase


ROOT = Path(__file__).resolve().parents[1]
TEST_MODULES = [
    "tests.test_ghc_family_v659_v1_x1",
    "tests.test_ghc_family_v659_v1_x2",
    "tests.test_ghc_family_v659_v1_closeout",
]


def git(*args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True,
        encoding="utf-8", check=check,
    )
    return result.stdout.strip()


def command_version(command: list[str]) -> str:
    try:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=20)
        return (result.stdout or result.stderr).strip().splitlines()[0]
    except Exception as exc:
        return f"unavailable:{type(exc).__name__}"


def remote_state(branch: str) -> dict:
    git("fetch", "origin", branch)
    local = git("rev-parse", "HEAD")
    upstream = git("rev-parse", "@{u}")
    tracking = git("rev-parse", f"refs/remotes/origin/{branch}")
    live_line = git("ls-remote", "--heads", "origin", f"refs/heads/{branch}")
    live = live_line.split()[0] if live_line else ""
    divergence = git("rev-list", "--left-right", "--count", "HEAD...@{u}")
    return {
        "local": local, "upstream": upstream, "tracking": tracking,
        "fresh_live_remote": live, "divergence": divergence,
        "four_way_equal": local == upstream == tracking == live,
    }


def run_tests() -> dict:
    loader = unittest.defaultTestLoader
    suite = unittest.TestSuite(loader.loadTestsFromName(name) for name in TEST_MODULES)
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    return {
        "modules": TEST_MODULES,
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "unexpected_successes": len(result.unexpectedSuccesses),
        "successful": result.wasSuccessful(),
        "diagnostic_sha256": hashlib.sha256(stream.getvalue().encode("utf-8")).hexdigest(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-final", required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    receipt_path = args.receipt.resolve()
    if ROOT == receipt_path or ROOT in receipt_path.parents:
        raise SystemExit("canonical receipt must be external to the repository")
    if receipt_path.suffix.casefold() != ".json":
        raise SystemExit("canonical receipt must be an explicit JSON filename")
    if receipt_path.exists():
        raise SystemExit("canonical receipt path already exists; no replay or overwrite")
    receipt_path.parent.mkdir(parents=True, exist_ok=True)

    started = datetime.now(timezone.utc)
    receipt: dict = {
        "schema": "ghc.family.v659-v1.external-canonical-receipt.v1",
        "owner": d.OWNER, "phase": d.PHASE, "expected_final": args.expected_final,
        "started_utc": started.isoformat(), "full_repository_suite_run": False,
        "full_repository_suite_owner": "Eiren Kestrel", "same_owner_only": True,
        "independent_reproduction": False, "valid": False,
        "boundary": "One attributable same-owner scoped aggregate; not independent reproduction, production certification, scientific confirmation, legal or cultural authority, Māori authority, or Stage 20 evidence.",
    }
    try:
        head = git("rev-parse", "HEAD")
        branch = git("branch", "--show-current")
        if head != args.expected_final:
            raise RuntimeError("HEAD differs from expected final")
        if branch != d.BRANCH:
            raise RuntimeError("canonical branch differs from declared Ilyra branch")
        if git("status", "--porcelain=v1"):
            raise RuntimeError("canonical lane is not clean before aggregate")
        before = remote_state(branch)
        if not before["four_way_equal"] or before["divergence"].replace("\t", " ") != "0 0":
            raise RuntimeError("canonical lane is not four-way remote-equal before aggregate")

        tests = run_tests()
        detailed = validate_phase()
        minimal = validate_minimal()
        final = validate_final(args.expected_final)
        if not tests["successful"]:
            raise RuntimeError("authorized scoped tests failed")
        if not detailed["valid"] or not minimal["valid"] or not final["valid"]:
            raise RuntimeError("one or more validators failed")
        if git("status", "--porcelain=v1"):
            raise RuntimeError("canonical lane changed during aggregate")
        after = remote_state(branch)
        if not after["four_way_equal"] or after["divergence"].replace("\t", " ") != "0 0":
            raise RuntimeError("canonical lane is not four-way remote-equal after aggregate")
        if git("status", "--porcelain=v1"):
            raise RuntimeError("canonical lane is not clean after remote postflight")

        finished = datetime.now(timezone.utc)
        receipt.update({
            "observed_final": head, "branch": branch,
            "finished_utc": finished.isoformat(),
            "elapsed_seconds": round((finished - started).total_seconds(), 6),
            "tests": tests,
            "detailed": {"checks": detailed["check_count"], "passed": detailed["passed_count"], "valid": detailed["valid"]},
            "minimal": {"checks": minimal["check_count"], "passed": minimal["passed_count"], "valid": minimal["valid"]},
            "final": {
                "checks": final["check_count"], "passed": final["passed_count"],
                "valid": final["valid"], "json_parses": final["json_parse_count"],
                "owner_manifest_entries": final["owner_manifest_entry_count"],
                "delta_manifest_entries": final["delta_manifest_entry_count"],
                "privacy_candidates": final["privacy_candidate_count"],
                "privacy_confirmed_hits": final["privacy_confirmed_hit_count"],
            },
            "remote_before": before, "remote_after": after,
            "history": {
                "source": d.SOURCE_FINAL, "x1": d.X1_FREEZE,
                "evidence": "88f4734cda8049c887ad7ba12df088e63737c929",
                "phase_commits": int(git("rev-list", "--count", f"{d.SOURCE_FINAL}..{head}")),
                "merge_commits": int(git("rev-list", "--merges", "--count", f"{d.SOURCE_FINAL}..{head}")),
            },
            "versions": {
                "python": platform.python_version(),
                "git": command_version(["git", "--version"]),
                "codex_cli": command_version(["codex", "--version"]),
            },
            "post_success_replay_permitted": False,
            "valid": True,
        })
    except Exception as exc:
        receipt.update({
            "finished_utc": datetime.now(timezone.utc).isoformat(),
            "failure_type": type(exc).__name__, "failure_message": str(exc),
            "credit": 0, "valid": False,
        })
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({
        "valid": receipt["valid"], "expected_final": args.expected_final,
        "tests": receipt.get("tests", {}).get("tests_run", 0),
        "detailed": receipt.get("detailed", {}).get("passed", 0),
        "minimal": receipt.get("minimal", {}).get("passed", 0),
        "final": receipt.get("final", {}).get("passed", 0),
    }, sort_keys=True))
    return 0 if receipt["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
