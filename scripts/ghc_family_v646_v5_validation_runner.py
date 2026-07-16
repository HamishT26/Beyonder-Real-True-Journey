#!/usr/bin/env python3
"""Run bounded current, successor-scoped, detailed, minimal, JSON, and privacy checks."""

from __future__ import annotations

import argparse
import importlib.util
import io
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/tamar-vey/v646-v5"
CURRENT_FILES = [ROOT / "tests/test_ghc_family_v646_v5_x1.py", ROOT / "tests/test_ghc_family_v646_v5.py"]
SCOPED_FILES = [ROOT / f"tests/test_ghc_family_v646_v{i}{suffix}.py" for i in range(1, 6) for suffix in ("_x1", "")]
EXCLUDED = {
    "tests.test_ghc_family_v646_v1.V646V1EvidenceTests.test_detailed_validator_precommit": "original v646-v1 phase-local commit-cap assertion",
    "tests.test_ghc_family_v646_v1.V646V1EvidenceTests.test_minimal_validator_precommit": "original v646-v1 phase-local commit-cap assertion",
}
PRIVATE = {
    "raw_uuid_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
    "private_route_or_callable": re.compile("(?:source_" + "thread_id|client" + "ThreadId|app" + "://|codex" + "://|private_" + "callable_id)", re.I),
    "credential_or_secret_material": re.compile("(?:BEGIN (?:RSA |EC |OPENSSH )?PRIVATE " + "KEY|api[_-]?" + "key\\s*[:=]|authorization:\\s*bearer\\s+[A-Za-z0-9._~-]{12,})", re.I),
    "private_absolute_local_path": re.compile("(?:[A-Za-z]:\\\\" + "Users\\\\[^\\\\\\s]+\\\\|D:\\\\GHC-" + "Archives\\\\)", re.I),
    "private_session_artifact": re.compile("(?:session[_ -]?" + "stream[_ -]?(?:path|id)|transcript[_ -]?(?:path|id)|screenshot[_ -]?(?:path|id))", re.I),
}
BOUNDARY = "Non-Eiren bounded validation only; not the complete repository suite, independent reproduction, exhaustive security, complete privacy, complete accessibility, production certification, or authority."


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def flatten(suite: unittest.TestSuite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def load_file(path: Path) -> unittest.TestSuite:
    module_name = "tests." + path.stem
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path.name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return unittest.defaultTestLoader.loadTestsFromModule(module)


def run_tests(paths: list[Path], scoped: bool) -> dict[str, Any]:
    suite = unittest.TestSuite()
    modules = []
    for path in paths:
        if not path.is_file():
            continue
        modules.append(path.stem)
        suite.addTests(load_file(path))
    discovered = list(flatten(suite))
    eligible = [test for test in discovered if not scoped or test.id() not in EXCLUDED]
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=1).run(unittest.TestSuite(eligible))
    passed = result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped)
    return {
        "modules": modules, "discovered_count": len(discovered),
        "excluded_phase_local_tests": [{"test_id": key, "reason": value} for key, value in sorted(EXCLUDED.items())] if scoped else [],
        "excluded_count": len(discovered) - len(eligible), "eligible_count": len(eligible), "tests_run": result.testsRun,
        "passed": passed, "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped),
        "valid": result.wasSuccessful() and (not scoped or len(eligible) == len(discovered) - len(EXCLUDED)),
    }


def minimal() -> dict[str, Any]:
    truth = load("phase-truth.json")
    ledger = load("x2-proposal-ledger.json")
    negatives = load("retained-negative-register.json")
    gates = load("exact-open-gate-register.json")
    checks = {
        "proposal_count": ledger["proposal_count"] == 10,
        "distribution": ledger["distribution"] == {"completed": 6, "exact_gate": 1, "open_gap": 1, "represented": 2},
        "all_acceptance_gates": all(row["acceptance_gate_passed"] for row in ledger["proposals"]),
        "mutation_total": sum(row["mutations_executed"] for row in ledger["proposals"]) == 70,
        "negative_total": negatives["effective_total"] == 2884,
        "failure_retained": negatives["no_negative_erased"],
        "open_gaps": gates["effective_open_gaps"] == 14,
        "exact_gates": gates["effective_exact_gates"] == 15,
        "no_silent_gate_close": gates["silently_closed"] == 0,
        "terminal_verdict": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "same_owner_only": truth["same_owner_repeatability_only"] and not truth["independent_team_reproduction"],
        "route_unsent": load("orchestration/terminal-route-plan.json")["current_state"] == "PREPARED_NOT_SENT",
        "no_real_data": ledger["real_data_rows"] == 0,
        "no_real_participants": ledger["real_participants_or_animals"] == 0,
        "no_real_identity": ledger["real_keys_or_transactions"] == 0,
        "no_authority": ledger["authority_delegated"] is False,
        "safe_30": load("approval-packets/x2-safe-now-execution.json")["count"] == 30,
        "candidate_20": load("prototypes/x2-candidate-execution.json")["count"] == 20,
        "cleanup_30": load("maintenance/x2-clean-refine-ledger.json")["count"] == 30,
        "skills_20": len(load("prototypes/x1-skill-runner-plan.json")["skills"]) == 20,
        "runners_10": len(load("prototypes/x1-skill-runner-plan.json")["runners"]) == 10,
        "full_suite_not_run": load("environment/x2-environment-receipt.json")["full_repository_suite_run"] is False,
    }
    return {"schema": "ghc.family.v646-v5.minimal-validation.v1", "checks": checks, "check_count": len(checks), "passed": sum(checks.values()), "valid": all(checks.values()), "boundary": BOUNDARY}


def detailed() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    def add(label: str, valid: bool) -> None:
        checks.append({"check": label, "valid": bool(valid)})
    ledger = load("x2-proposal-ledger.json")
    for row in ledger["proposals"]:
        add(f"{row['proposal_id']}:expected", row["outcome"] == row["expected_disposition"])
        add(f"{row['proposal_id']}:gate", row["acceptance_gate_passed"])
        add(f"{row['proposal_id']}:seven_mutations", row["mutations_executed"] == row["mutations_rejected"] == 7)
        add(f"{row['proposal_id']}:authority", not row["authority_delegated"])
    for relative in ("approval-packets/x2-safe-now-execution.json", "prototypes/x2-candidate-execution.json", "maintenance/x2-clean-refine-ledger.json"):
        for row in load(relative)["tasks"]:
            add(f"{row['packet_id']}:gate", row["acceptance_gate_passed"])
            add(f"{row['packet_id']}:owner", row["owner_scoped"])
            add(f"{row['packet_id']}:protected", not row["protected_gate_executed"])
    for source in load("sources/source-ledger.json")["sources"]:
        add(f"{source['source_id']}:status", source["status"] in {"current", "stable", "draft", "watch"})
        add(f"{source['source_id']}:use", bool(source["use"]))
    for skill in load("prototypes/x1-skill-runner-plan.json")["skills"]:
        path = PHASE / f"prototypes/skills/{skill['name']}/SKILL.md"
        add(f"{skill['name']}:package", path.is_file())
        add(f"{skill['name']}:boundary", path.is_file() and "## Boundaries" in path.read_text(encoding="utf-8"))
    synthetic = load("validation/x2-synthetic-negative-register.json")
    for row in synthetic["rows"]:
        add(f"{row['negative_id']}:executed", row["executed"])
        add(f"{row['negative_id']}:rejected", row["rejected"])
        add(f"{row['negative_id']}:retained", row["retained"])
    return {"schema": "ghc.family.v646-v5.detailed-validation.v1", "check_count": len(checks), "passed": sum(row["valid"] for row in checks), "failed": [row for row in checks if not row["valid"]], "checks": checks, "valid": all(row["valid"] for row in checks), "boundary": BOUNDARY}


def json_privacy() -> dict[str, Any]:
    json_count = 0
    files = 0
    hits = []
    parse_failures = []
    for path in sorted(PHASE.rglob("*")):
        if not path.is_file():
            continue
        files += 1
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        relative = path.relative_to(ROOT).as_posix()
        for label, pattern in PRIVATE.items():
            if pattern.search(text):
                hits.append({"path": relative, "pattern_class": label})
        if path.suffix == ".json":
            json_count += 1
            try:
                json.loads(text)
            except Exception as exc:
                parse_failures.append({"path": relative, "error": str(exc)})
    return {"schema": "ghc.family.v646-v5.json-privacy-validation.v1", "files_scanned": files, "json_parse_count": json_count, "json_parse_failures": parse_failures, "privacy_pattern_classes": sorted(PRIVATE), "privacy_confirmed_hits": hits, "privacy_confirmed_hit_count": len(hits), "valid": not parse_failures and not hits, "boundary": BOUNDARY}


def write(relative: str, payload: dict[str, Any]) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("current", "scoped", "minimal", "detailed", "json-privacy", "all"), default="all")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    results: dict[str, dict[str, Any]] = {}
    if args.mode in {"current", "all"}:
        results["current"] = run_tests(CURRENT_FILES, False)
    if args.mode in {"scoped", "all"}:
        results["scoped"] = run_tests(SCOPED_FILES, True)
    if args.mode in {"minimal", "all"}:
        results["minimal"] = minimal()
    if args.mode in {"detailed", "all"}:
        results["detailed"] = detailed()
    if args.mode in {"json-privacy", "all"}:
        results["json_privacy"] = json_privacy()
    valid = all(row["valid"] for row in results.values())
    payload = {"schema": "ghc.family.v646-v5.validation-runner.v1", "modes": results, "full_repository_suite_run": False, "same_owner_only": True, "independent_reproduction": False, "valid": valid, "boundary": BOUNDARY}
    if args.write:
        mapping = {"current": "validation/current-phase-tests.json", "scoped": "validation/successor-scoped-tests.json", "minimal": "validation/minimal-validation.json", "detailed": "validation/detailed-validation.json", "json_privacy": "validation/json-privacy-validation.json"}
        for key, row in results.items():
            write(mapping[key], row)
        write("validation/validation-runner-summary.json", payload)
    summary = {key: {k: value for k, value in row.items() if k in {"tests_run", "passed", "failures", "errors", "excluded_count", "check_count", "files_scanned", "json_parse_count", "privacy_confirmed_hit_count", "valid"}} for key, row in results.items()}
    print(json.dumps({"modes": summary, "valid": valid}, sort_keys=True))
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
