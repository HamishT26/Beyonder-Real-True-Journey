#!/usr/bin/env python3
"""Run Eiren's one coherent module-isolated full repository pass."""

from __future__ import annotations

import argparse
import importlib
import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
EXCLUDED = {
    "tests.test_ghc_family_v648_v6_closeout.TestGhcFamilyV648V6Closeout.test_final_validation_plan_reserves_one_pass_and_no_replay",
    "tests.test_ghc_family_v648_v6_closeout.TestGhcFamilyV648V6Closeout.test_stage20_board_and_closeout_candidate_abstain",
    "tests.test_ghc_family_v648_v3_2_x1.V648V3RepeatX1Tests.test_exact_source_and_commit_boundary",
    "tests.test_ghc_family_v648_v3_closeout.V648V3CloseoutTests.test_anchor_contract_and_commit_cap",
}
NON_UNITTEST_SOURCE_TRANSFORMS = {
    "tests.test_ghc_family_v645_v6_x1",
    "tests.test_ghc_family_v645_v7_x1",
    "tests.test_ghc_family_v645_v8_x1",
}


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


def flatten(suite: unittest.TestSuite) -> list[unittest.TestCase]:
    rows: list[unittest.TestCase] = []
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            rows.extend(flatten(item))
        else:
            rows.append(item)
    return rows


def plan() -> tuple[list[dict[str, object]], list[str]]:
    rows: list[dict[str, object]] = []
    discovered: list[str] = []
    for path in sorted((ROOT / "tests").glob("test*.py")):
        module = f"tests.{path.stem}"
        if module in NON_UNITTEST_SOURCE_TRANSFORMS:
            rows.append({"module": module, "test_ids": [], "classification": "historical_source_transform_no_unittest_credit"})
            continue
        importlib.invalidate_caches()
        imported = importlib.import_module(module)
        suite = unittest.defaultTestLoader.loadTestsFromModule(imported)
        tests = flatten(suite)
        failed_loads = [test.id() for test in tests if test.__class__.__name__ == "_FailedTest"]
        if failed_loads:
            raise RuntimeError(f"test discovery failed for {module}: {failed_loads}")
        ids = sorted(test.id() for test in tests)
        discovered.extend(ids)
        eligible = [test_id for test_id in ids if test_id not in EXCLUDED]
        rows.append({"module": module, "test_ids": eligible, "discovered_count": len(ids), "eligible_count": len(eligible)})
    missing_exclusions = sorted(EXCLUDED - set(discovered))
    if missing_exclusions:
        raise RuntimeError(f"declared exact exclusions were not discovered: {missing_exclusions}")
    return rows, discovered


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan-only", action="store_true")
    parser.add_argument("--expected-head")
    parser.add_argument("--receipt")
    args = parser.parse_args()
    rows, discovered = plan()
    eligible_count = sum(int(row.get("eligible_count", 0)) for row in rows)
    if args.plan_only:
        print(json.dumps({
            "module_files": len(rows), "discovered_tests": len(discovered),
            "eligible_tests": eligible_count, "exact_exclusions": len(EXCLUDED),
            "non_unittest_source_transforms": len(NON_UNITTEST_SOURCE_TRANSFORMS),
        }, sort_keys=True))
        return 0
    if not args.expected_head or not args.receipt:
        raise RuntimeError("canonical mode requires --expected-head and --receipt")
    receipt = Path(args.receipt)
    if receipt.exists():
        raise RuntimeError("a canonical suite receipt already exists; replay is prohibited")
    head = git("rev-parse", "HEAD")
    if head != args.expected_head:
        raise RuntimeError("expected head does not match HEAD")
    if git("status", "--porcelain"):
        raise RuntimeError("canonical full suite requires a clean worktree")
    module_results = []
    total_run = total_failures = total_errors = total_skipped = 0
    environment = {**os.environ, "PYTHONUTF8": "1"}
    for row in rows:
        module = str(row["module"])
        ids = list(row.get("test_ids", []))
        if not ids:
            module_results.append({"module": module, "tests_run": 0, "failures": 0, "errors": 0, "skipped": 0, "successful": True, "classification": row.get("classification", "zero_discovered_tests")})
            continue
        result = subprocess.run(
            [sys.executable, "-B", "-m", "unittest", "-q", *ids],
            cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=environment,
        )
        output = result.stdout + result.stderr
        ran = re.search(r"Ran\s+(\d+)\s+tests?", output)
        count = int(ran.group(1)) if ran else 0
        failed = re.search(r"FAILED\s*\(([^)]*)\)", output)
        fields = dict((name, int(value)) for name, value in re.findall(r"(failures|errors|skipped)=(\d+)", failed.group(1))) if failed else {}
        failures = fields.get("failures", 0)
        errors = fields.get("errors", 0)
        skipped_match = re.search(r"OK\s*\(skipped=(\d+)\)", output)
        skipped = fields.get("skipped", int(skipped_match.group(1)) if skipped_match else 0)
        if result.returncode and failures + errors == 0:
            errors = 1
        total_run += count
        total_failures += failures
        total_errors += errors
        total_skipped += skipped
        module_results.append({
            "module": module, "tests_run": count, "failures": failures,
            "errors": errors, "skipped": skipped,
            "successful": result.returncode == 0,
        })
    successful = total_failures == 0 and total_errors == 0 and all(row["successful"] for row in module_results)
    payload = {
        "schema": "ghc.family.v649-v1.full-repository-suite.external.v1",
        "owner": "Eiren Kestrel", "canonical": True,
        "exact_head": head, "branch": git("branch", "--show-current"),
        "mode": "one_coherent_module_isolated_pass",
        "module_file_count": len(rows), "module_execution_count": sum(bool(row.get("test_ids")) for row in rows),
        "tests_discovered": len(discovered), "tests_excluded": len(EXCLUDED),
        "tests_run": total_run, "failures": total_failures,
        "errors": total_errors, "skipped": total_skipped,
        "successful": successful, "canonical_successful_passes": 1 if successful else 0,
        "failed_modules": [row for row in module_results if not row["successful"]],
        "exact_excluded_test_ids": sorted(EXCLUDED),
        "non_unittest_source_transforms": sorted(NON_UNITTEST_SOURCE_TRANSFORMS),
        "module_reexecutions": 0, "replay_runs": 0,
        "same_owner_only": True, "independent_reproduction": False,
        "boundary": "One Eiren-owned full repository pass with exact inherited lifecycle exclusions; not replay, independent reproduction, external audit, production certification, or Stage 20 authority.",
    }
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({key: payload[key] for key in ("tests_run", "failures", "errors", "skipped", "successful")}, sort_keys=True))
    return 0 if successful else 1


if __name__ == "__main__":
    raise SystemExit(main())
