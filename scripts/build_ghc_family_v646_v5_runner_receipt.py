#!/usr/bin/env python3
"""Invoke and record all ten frozen family-current v646-v5 runners."""

from __future__ import annotations

import json
import hashlib
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/tamar-vey/v646-v5"


RUNS = [
    ("runtime", ["scripts/ghc_family_v646_v5_runtime.py", "--surface", "all"]),
    ("core-runner", ["scripts/ghc_family_v646_v5_core_runner.py", "--surface", "all"]),
    ("portfolio-runner", ["scripts/ghc_family_v646_v5_portfolio_runner.py"]),
    ("skill-runner", ["scripts/ghc_family_v646_v5_skill_runner.py"]),
    ("staged-review", ["scripts/ghc_family_v646_v5_staged_review.py", "--stage", "evidence"]),
    ("validation-runner", ["scripts/ghc_family_v646_v5_validation_runner.py", "--mode", "all"]),
    ("optimistic-concurrency", ["scripts/ghc_family_v646_v5_optimistic_concurrency.py"]),
    ("reftable-tribunal", ["scripts/ghc_family_v646_v5_reftable_tribunal.py"]),
    ("source-gate", ["scripts/ghc_family_v646_v5_source_gate.py"]),
    ("named-lane-audit", ["scripts/ghc_family_v646_v5_named_lane_audit.py", "--self-test"]),
]


def main() -> int:
    rows = []
    for name, command in RUNS:
        result = subprocess.run([sys.executable, *command], cwd=ROOT, text=True, capture_output=True, encoding="utf-8", timeout=180)
        stderr_category = "none"
        if result.stderr:
            stderr_category = "unicode_console_encoding_error" if "UnicodeEncodeError" in result.stderr else "sanitized_runner_error"
        row = {
            "runner": name,
            "entrypoint": command[0],
            "arguments": command[1:],
            "returncode": result.returncode,
            "invoked": True,
            "passed": result.returncode == 0,
            "stdout_bytes": len(result.stdout.encode("utf-8")),
            "stdout_sha256": hashlib.sha256(result.stdout.encode("utf-8")).hexdigest(),
            "stderr_bytes": len(result.stderr.encode("utf-8")),
            "stderr_sha256": hashlib.sha256(result.stderr.encode("utf-8")).hexdigest(),
            "stderr_category": stderr_category,
            "raw_streams_retained": False,
            "same_owner_only": True,
            "independent_reproduction": False,
        }
        rows.append(row)
        target = PHASE / f"prototypes/runner-witnesses/{name}.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(row, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
        if result.returncode:
            print(json.dumps(row, ensure_ascii=True))
            return 1
    payload = {"schema": "ghc.family.v646-v5.runner-build-use.v1", "runner_count": len(rows), "built_count": sum((ROOT / row["entrypoint"]).is_file() for row in rows), "invoked_count": sum(row["invoked"] for row in rows), "passed_count": sum(row["passed"] for row in rows), "runners": rows, "global_installation": False, "full_repository_suite_run": False, "same_owner_only": True, "independent_reproduction": False, "valid": len(rows) == 10 and all(row["passed"] for row in rows), "boundary": "Runner build and invocation evidence is bounded same-owner software evidence only; it grants no production, professional, authority, empirical, security-complete, or independent-reproduction credit."}
    target = PHASE / "prototypes/runner-build-use-receipt.json"
    target.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"runners": len(rows), "built": payload["built_count"], "invoked": payload["invoked_count"], "passed": payload["passed_count"], "valid": payload["valid"]}))
    return 0 if payload["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
