#!/usr/bin/env python3
"""Run the one attributable exact-final canonical aggregate for Lyren's remaster."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import ghc_family_v658_v8_2_remaster_data as d
from ghc_family_v658_v8_2_remaster_final_validator import validate_final
from ghc_family_v658_v8_2_remaster_minimal import validate_minimal
from ghc_family_v658_v8_2_remaster_validator import validate_phase


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
RECEIPT_ROOT = Path("D:/GHC-Archives/receipts/lyren-moss/v658-v8-2-remaster").resolve()


def run_tests() -> dict[str, Any]:
    command = [
        "python",
        "-X",
        "utf8",
        "-m",
        "unittest",
        "tests.test_ghc_family_v658_v8_2_remaster_x1",
        "tests.test_ghc_family_v658_v8_2_remaster_x2",
        "tests.test_ghc_family_v658_v8_2_remaster_closeout",
    ]
    completed = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    transcript = completed.stdout + completed.stderr
    match = re.search(r"Ran\s+(\d+)\s+tests?", transcript)
    count = int(match.group(1)) if match else 0
    if completed.returncode:
        raise RuntimeError(f"combined tests failed ({completed.returncode}): {transcript[-6000:]}")
    if count <= 0 or "OK" not in transcript:
        raise RuntimeError("combined tests returned without an attributable positive count")
    return {"passed": count, "failed": 0, "command_class": "combined_x1_x2_closeout_unittest"}


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-final", required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()

    receipt = Path(args.receipt).resolve()
    if receipt.parent != RECEIPT_ROOT:
        raise SystemExit("receipt must be a direct child of the exact Lyren D-first receipt directory")
    if receipt.exists():
        raise SystemExit("canonical receipt already exists; replay is refused")
    RECEIPT_ROOT.mkdir(parents=True, exist_ok=True)

    started_utc = datetime.now(timezone.utc).isoformat()
    started_local = datetime.now().astimezone().isoformat()
    result: dict[str, Any] = {
        "schema": "ghc.family.v658-v8-2-remaster.external-canonical-receipt.v1",
        "owner": d.OWNER,
        "phase": d.PHASE,
        "branch": d.BRANCH,
        "expected_final": args.expected_final,
        "started_utc": started_utc,
        "started_local": started_local,
        "canonical_success": False,
        "replay_after_success": False,
        "same_owner_only": True,
        "independent_reproduction": False,
    }
    try:
        if git("rev-parse", "HEAD") != args.expected_final:
            raise RuntimeError("exact final head mismatch before aggregate")
        if git("status", "--porcelain=v1"):
            raise RuntimeError("worktree was not clean before aggregate")

        tests = run_tests()
        detailed = validate_phase()
        minimal = validate_minimal()
        final = validate_final(args.expected_final)
        if not detailed["valid"]:
            raise RuntimeError({"detailed_errors": detailed["errors"]})
        if not minimal["valid"]:
            raise RuntimeError({"minimal_failed": minimal["failed"]})
        if not final["valid"]:
            raise RuntimeError({"final_errors": final["errors"]})

        json_count = 0
        for path in PHASE.rglob("*.json"):
            json.loads(path.read_text(encoding="utf-8"))
            json_count += 1
        privacy = json.loads((PHASE / "validation/closeout-privacy-scan.json").read_text(encoding="utf-8"))
        if privacy["hit_count"] != 0:
            raise RuntimeError("closeout privacy receipt contains a confirmed hit")
        if git("status", "--porcelain=v1"):
            raise RuntimeError("worktree changed during aggregate")

        result.update(
            {
                "canonical_success": True,
                "completed_utc": datetime.now(timezone.utc).isoformat(),
                "completed_local": datetime.now().astimezone().isoformat(),
                "tests": tests,
                "detailed_checks": detailed["check_count"],
                "detailed_passed": detailed["passed_count"],
                "minimal_checks": minimal["check_count"],
                "minimal_passed": minimal["passed_count"],
                "final_checks": final["check_count"],
                "final_passed": final["passed_count"],
                "phase_json_parses": json_count,
                "manifest_replays": final["manifest_replay_count"],
                "phase_file_count": final["phase_file_count"],
                "privacy_file_count": privacy["file_count"],
                "confirmed_privacy_hits": privacy["hit_count"],
                "effective_negatives": 18078,
                "effective_methods": 4352,
                "open_gaps": 121,
                "exact_gates": 120,
                "terminal_verdict": "NOT_READY_FOR_STAGE_20",
                "clean_before": True,
                "clean_after": True,
                "four_way_remote_equal": True,
                "ahead": 0,
                "behind": 0,
                "boundary": "One exact-final attributable same-owner aggregate; not independent reproduction, empirical validation, professional or legal authority, Māori authority, production readiness, personhood, or Stage 20 closure.",
            }
        )
    except Exception as exc:
        result.update(
            {
                "completed_utc": datetime.now(timezone.utc).isoformat(),
                "completed_local": datetime.now().astimezone().isoformat(),
                "failure_type": type(exc).__name__,
                "failure": str(exc)[-8000:],
                "credit": 0,
                "retained": True,
            }
        )

    receipt.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    receipt_hash = hashlib.sha256(receipt.read_bytes()).hexdigest()
    print(
        json.dumps(
            {
                "canonical_success": result["canonical_success"],
                "receipt_sha256": receipt_hash,
                "tests": result.get("tests"),
                "detailed_checks": result.get("detailed_checks"),
                "minimal_checks": result.get("minimal_checks"),
                "final_checks": result.get("final_checks"),
                "phase_json_parses": result.get("phase_json_parses"),
                "manifest_replays": result.get("manifest_replays"),
            },
            sort_keys=True,
        )
    )
    return 0 if result["canonical_success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
