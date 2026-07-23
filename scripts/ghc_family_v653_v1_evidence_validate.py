#!/usr/bin/env python3
"""Run the bounded evidence validation for Vesper Arlen v653-v1."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import ghc_family_v653_v1_detailed_validator as detailed
import ghc_family_v653_v1_minimal_validator as minimal
from ghc_family_v653_v1_validation_common import PHASE, REPO, phase_public_paths, scan_privacy_paths, write_json


TEST_MODULES = [
    "tests.test_ghc_family_v653_v1_x1",
    "tests.test_ghc_family_v653_v1_core",
    "tests.test_ghc_family_v653_v1_validation",
]


def run_tests() -> dict[str, Any]:
    env = os.environ.copy()
    env.update({"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"})
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "-q", *TEST_MODULES],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )
    output = result.stdout + result.stderr
    match = re.search(r"Ran (\d+) tests?", output)
    return {
        "modules": TEST_MODULES,
        "tests_run": int(match.group(1)) if match else 0,
        "failures": len(re.findall(r"^FAIL:", output, flags=re.MULTILINE)),
        "errors": len(re.findall(r"^ERROR:", output, flags=re.MULTILINE)),
        "exit_code": result.returncode,
        "valid": result.returncode == 0 and match is not None,
    }


def validate() -> dict[str, Any]:
    tests = run_tests()
    detailed_result = detailed.validate()
    minimal_result = minimal.validate()
    json_paths = sorted(PHASE.rglob("*.json"))
    parse_failures: list[dict[str, str]] = []
    for path in json_paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            parse_failures.append({"path": path.relative_to(REPO).as_posix(), "error": type(exc).__name__})
    privacy = scan_privacy_paths(phase_public_paths())
    valid = (
        tests["valid"]
        and detailed_result["valid"]
        and minimal_result["valid"]
        and not parse_failures
        and privacy["valid"]
    )
    return {
        "schema": "ghc.family.v653-v1.evidence-validation.v1",
        "tests": tests,
        "detailed_check_count": detailed_result["check_count"],
        "detailed_passed_count": detailed_result["passed_count"],
        "minimal_check_count": minimal_result["check_count"],
        "minimal_passed_count": minimal_result["passed_count"],
        "json_parse_count": len(json_paths),
        "json_parse_failures": parse_failures,
        "privacy": privacy,
        "full_repository_suite_run": False,
        "full_repository_suite_owner": "not claimed by Vesper v653-v1",
        "valid": valid,
        "boundary": "One bounded Vesper evidence pass; not the exact-final canonical pass, not a full-repository suite, and not independent reproduction.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, default=PHASE / "validation/evidence-validation.json")
    args = parser.parse_args()
    result = validate()
    write_json(args.receipt, result)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    if not result["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
