#!/usr/bin/env python3
"""Verify the bounded successor selection and its two explicit phase-local exclusions."""

from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/ghc_family_v646_v3_scoped_tests.py"
EXPECTED_EXCLUSIONS = {
    "tests.test_ghc_family_v646_v1.V646V1EvidenceTests.test_detailed_validator_precommit",
    "tests.test_ghc_family_v646_v1.V646V1EvidenceTests.test_minimal_validator_precommit",
}


def literal_assignment(tree: ast.Module, name: str):
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == name for target in node.targets):
            return ast.literal_eval(node.value)
    raise KeyError(name)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
    modules = literal_assignment(tree, "MODULES")
    exclusions = literal_assignment(tree, "EXCLUDED")
    checks = [
        len(modules) == len(set(modules)),
        "tests.test_ghc_family_v646_v2" in modules,
        "tests.test_ghc_family_v646_v3_x1" in modules,
        "tests.test_ghc_family_v646_v3" in modules,
        set(exclusions) == EXPECTED_EXCLUSIONS,
        all("original v646-v1 phase-local commit-cap assertion" in reason for reason in exclusions.values()),
    ]
    payload = {
        "schema": "ghc.family.phase-local-test-quarantine.v1",
        "checks": len(checks), "passed": all(checks), "modules": modules,
        "excluded_phase_local_tests": [{"test_id": key, "reason": exclusions[key]} for key in sorted(exclusions)],
        "excluded_count": len(exclusions), "full_repository_suite_run": False,
        "boundary": "Only the two named original-phase commit-cap assertions are quarantined; no broader exclusion is authorized.",
    }
    rendered = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    else:
        print(rendered, end="")
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
