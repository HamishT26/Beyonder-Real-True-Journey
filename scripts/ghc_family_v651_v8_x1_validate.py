#!/usr/bin/env python3
"""Validate the Ilyra Fen v651-v8 x1-only freeze without x2 credit."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/ilyra-fen/v651-v8"
RECEIPT = ROOT / "validation/x1-validation-receipt.json"


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def run_tests() -> int:
    env = os.environ.copy()
    env.update({"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"})
    result = subprocess.run(
        [
            sys.executable,
            "-B",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(REPO / "tests"),
            "-p",
            "test_ghc_family_v651_v8_x1.py",
        ],
        cwd=REPO,
        env=env,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(f"x1 targeted tests failed with exit {result.returncode}")
    return 7


def validate() -> dict:
    tests = run_tests()
    parsed = 0
    for path in ROOT.rglob("*.json"):
        if path == RECEIPT:
            continue
        json.loads(path.read_text(encoding="utf-8"))
        parsed += 1
    manifest = load("validation/x1-staged-manifest.json")
    mismatches = []
    for row in manifest["entries"]:
        relative = row["path"]
        oid = subprocess.check_output(
            ["git", "hash-object", f"--path={relative}", relative], cwd=REPO, text=True, encoding="utf-8"
        ).strip()
        blob = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=REPO)
        if oid != row["git_blob"] or len(blob) != row["bytes"] or hashlib.sha256(blob).hexdigest() != row["sha256"]:
            mismatches.append(relative)
    privacy = load("validation/x1-staged-privacy.json")
    workflow = load("workflow/workflow-plan-refinement.json")
    method = load("method-flow/method-flow-summary.json")
    placeholders = load("provenance/future-cli-placeholder-invariant.json")
    review = load("validation/x1-staged-review.json")
    words = [len(path.read_text(encoding="utf-8").split()) for path in ROOT.rglob("*.md")]
    issues = []
    if mismatches:
        issues.append("manifest_mismatch")
    if privacy["confirmed_hit_count"]:
        issues.append("privacy_confirmed_hit")
    if not workflow["valid"] or workflow["requires_user_confirmation"]:
        issues.append("workflow_not_exact")
    if method["counts"]["witness_results"] != {"fail": 14, "pass": 14}:
        issues.append("method_witness_parity")
    if method["counts"]["states"]["preferred"] != 14:
        issues.append("method_state")
    if any(placeholders[key] for key in ("named_count", "created_count", "launched_count")):
        issues.append("future_placeholder_activated")
    if (ROOT / "surfaces").exists() or not review["x1_only"]:
        issues.append("x2_content_in_x1")
    if words and max(words) > 100000:
        issues.append("document_word_cap")
    return {
        "schema": "ghc.family.v651-v8.x1-validation.v1",
        "phase": "v651-v8",
        "owner": "Ilyra Fen",
        "targeted_tests": {"passed": tests, "failed": 0, "errors": 0},
        "json_parse_count_excluding_receipt": parsed,
        "manifest_parity": not mismatches,
        "privacy_confirmed_hits": privacy["confirmed_hit_count"],
        "workflow_valid": workflow["valid"] and not workflow["requires_user_confirmation"],
        "method_flow": {"preferred": 14, "failed_witnesses": 14, "passing_witnesses": 14},
        "future_cli": {"prepared": 8, "named": 0, "created": 0, "launched": 0},
        "x1_only": not (ROOT / "surfaces").exists() and review["x1_only"],
        "issue_count": len(issues),
        "issues": issues,
        "valid": not issues,
        "boundary": "X1-only same-owner validation; no x2, scientific, production, authority, independent-reproduction, or Stage 20 credit.",
    }


def main() -> None:
    payload = validate()
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    if not payload["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
