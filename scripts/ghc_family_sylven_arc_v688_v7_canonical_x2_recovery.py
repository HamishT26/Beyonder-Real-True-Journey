#!/usr/bin/env python3
"""Recover only the failed x2 lifecycle-test dependency from the invalid canonical."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
X2 = "3c968db9391583a9e40f0eb8cc0c2f86d9997126"
FAILED_HEAD = "1b00ec2df09e02ef63b370d6c8b15180044b3a38"
MANIFEST = "docs/sylven-arc/v688-v7/x1/x1-manifest.json"
MODULE = "tests/test_ghc_family_sylven_arc_v688_v7_x2.py"


def git_blob(spec: str) -> bytes:
    return subprocess.check_output(["git", "show", spec], cwd=ROOT)


def write_external(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bank", type=Path, required=True)
    args = parser.parse_args()
    bank = args.bank.resolve()
    failed_path = bank / "canonical/exact-final-owner-scoped-canonical.json"
    failed = json.loads(failed_path.read_text(encoding="utf-8"))
    if failed["head"] != FAILED_HEAD or failed["status"] != "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" or failed["canonical_invocation_count"] != 1 or failed["canonical_success_count"] != 0:
        raise RuntimeError("failed_canonical_gate")
    if [item["stage"] for item in failed["test_modules"] if not item["passed"]] != ["x2"]:
        raise RuntimeError("failed_stage_scope")
    view = bank / "canonical/definition-x2"
    if not (view / MODULE).is_file():
        raise RuntimeError("x2_definition_view_missing")
    manifest = json.loads(git_blob(X2 + ":" + MANIFEST))
    paths = [item["path"] for item in manifest["entries"]] + manifest["self_exclusions"]
    added = []
    verified_existing = []
    for path in paths:
        data = git_blob(X2 + ":" + path)
        destination = view / path
        if destination.exists():
            if destination.read_bytes() != data:
                raise RuntimeError("existing_dependency_mismatch:" + path)
            verified_existing.append(path)
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            with destination.open("xb") as stream:
                stream.write(data)
            added.append(path)
    process = subprocess.run([sys.executable, "-B", "-X", "utf8", str(view / MODULE)], cwd=view, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONUTF8": "1"}, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
    stdout_path = bank / "canonical/x2-dependency-recovery.stdout.txt"
    stderr_path = bank / "canonical/x2-dependency-recovery.stderr.txt"
    stdout_path.write_bytes(process.stdout)
    stderr_path.write_bytes(process.stderr)
    match = re.search(r"Ran (\d+) tests?", process.stderr.decode("utf-8", errors="replace"))
    count = int(match.group(1)) if match else 0
    passed = process.returncode == 0 and count == 24
    receipt = {
        "schema": "ghc.family.canonical-x2-dependency-recovery.v1",
        "failed_canonical_head": FAILED_HEAD,
        "failed_canonical_receipt_sha256": hashlib.sha256(failed_path.read_bytes()).hexdigest(),
        "failed_stage": "x2",
        "failure_class": "definition materialization omitted immutable x1 dependencies",
        "x1_dependency_manifest": MANIFEST,
        "x1_dependencies_added": len(added),
        "already_present_and_equal": len(verified_existing),
        "successful_canonical_components_replayed": 0,
        "aggregate_replayed": False,
        "rerun_scope": MODULE,
        "test_count": count,
        "expected_test_count": 24,
        "returncode": process.returncode,
        "passed": passed,
        "stdout_sha256": hashlib.sha256(process.stdout).hexdigest(),
        "stderr_sha256": hashlib.sha256(process.stderr).hexdigest(),
        "canonical_success_credit": 0,
        "state": "VALID_ISOLATED_X2_DEPENDENCY_RECOVERY" if passed else "FAILED_ISOLATED_X2_DEPENDENCY_RECOVERY",
        "boundary": "Focused same-owner lifecycle recovery only; the original canonical remains invalid and receives zero aggregate success credit.",
    }
    write_external(bank / "canonical/dependency-corrected-x2.json", receipt)
    print(json.dumps({"state": receipt["state"], "tests": count, "passed": passed, "dependencies_added": len(added), "successful_components_replayed": 0}, sort_keys=True))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
