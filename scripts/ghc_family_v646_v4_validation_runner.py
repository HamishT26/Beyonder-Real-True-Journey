#!/usr/bin/env python3
"""Run current-phase, successor-scoped, detailed, and minimal v646-v4 checks."""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

from ghc_family_v646_v4_validator import validate


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/orin-thale/v646-v4"
MODULES = ["tests.test_ghc_family_v646_v4_x1", "tests.test_ghc_family_v646_v4"]


def flatten(suite: unittest.TestSuite):
    for item in suite:
        if isinstance(item, unittest.TestSuite): yield from flatten(item)
        else: yield item


def load_modules() -> unittest.TestSuite:
    suite = unittest.TestSuite()
    for module_name in MODULES:
        path = ROOT / (module_name.replace(".", "/") + ".py")
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"cannot load {path}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))
    return suite


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--revision")
    parser.add_argument("--require-clean", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    suite = load_modules()
    discovered = list(flatten(suite))
    result = unittest.TextTestRunner(stream=sys.stderr, verbosity=1).run(unittest.TestSuite(discovered))
    passed = result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped)
    current = {
        "schema": "ghc.family.v646-v4.current-phase-tests.v1", "modules": MODULES,
        "tests": result.testsRun, "passed": passed, "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped),
        "valid": result.wasSuccessful(), "same_owner_only": True, "independent_reproduction": False,
    }
    validation_dir = PHASE / "validation"; validation_dir.mkdir(parents=True, exist_ok=True)
    (validation_dir / "current-phase-tests.json").write_text(json.dumps(current, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    scoped_output = validation_dir / "successor-scoped-tests.json"
    command = [sys.executable, str(ROOT / "scripts/ghc_family_v646_v4_scoped_tests.py"), "--output", str(scoped_output)]
    if args.revision: command.extend(["--revision", args.revision])
    if args.require_clean: command.append("--require-clean")
    scoped_run = subprocess.run(command, cwd=ROOT, text=True, encoding="utf-8", capture_output=True)
    scoped = json.loads(scoped_output.read_text(encoding="utf-8")) if scoped_output.is_file() else {"valid": False, "error": scoped_run.stderr}
    minimal = validate("minimal", args.revision, args.require_clean)
    detailed = validate("detailed", args.revision, args.require_clean)
    (validation_dir / "minimal-validation.json").write_text(json.dumps(minimal, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    (validation_dir / "detailed-validation.json").write_text(json.dumps(detailed, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    valid = current["valid"] and scoped.get("valid") is True and minimal["valid"] and detailed["valid"]
    payload = {
        "schema": "ghc.family.v646-v4.validation-runner.v1", "mode": "exact_clean" if args.require_clean else "working_candidate",
        "current_phase": current, "successor_scoped": {key: scoped.get(key) for key in ("discovered_count", "excluded_count", "eligible_count", "tests_run", "passed", "failures", "errors", "valid")},
        "minimal": {"checks": minimal["check_count"], "issues": minimal["issue_count"], "valid": minimal["valid"]},
        "detailed": {"checks": detailed["check_count"], "issues": detailed["issue_count"], "json": detailed.get("json_parse_count"), "privacy_files": detailed.get("privacy", {}).get("file_count"), "privacy_hits": detailed.get("privacy", {}).get("confirmed_hit_count"), "valid": detailed["valid"]},
        "full_repository_suite_run": False, "same_owner_only": True, "independent_reproduction": False,
        "passed": valid, "valid": valid,
        "boundary": "Non-Eiren scoped validation only; the complete repository suite remains Eiren-owned and same-owner checks are not independent reproduction.",
    }
    rendered = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    print(json.dumps({"current": current["tests"], "current_passed": current["passed"], "scoped": scoped.get("tests_run"), "scoped_passed": scoped.get("passed"), "minimal": minimal["check_count"], "detailed": detailed["check_count"], "json": detailed.get("json_parse_count"), "privacy_files": detailed.get("privacy", {}).get("file_count"), "valid": valid}))
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
