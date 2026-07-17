#!/usr/bin/env python3
"""Run the bounded non-Eiren v647-v6 validation selection."""

from __future__ import annotations

import argparse
import io
import json
import re
import sys
import unittest
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/ilyra-fen/v647-v6"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def load(relative: str) -> dict[str, Any]:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def run_tests(include_closeout: bool) -> dict[str, Any]:
    names = ["tests.test_ghc_family_v647_v5_closeout", "tests.test_ghc_family_v647_v6_x1", "tests.test_ghc_family_v647_v6"]
    if include_closeout and (ROOT / "tests/test_ghc_family_v647_v6_closeout.py").exists():
        names.append("tests.test_ghc_family_v647_v6_closeout")
    suite = unittest.TestLoader().loadTestsFromNames(names)
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=1).run(suite)
    return {
        "modules": names, "tests_run": result.testsRun, "failures": len(result.failures),
        "errors": len(result.errors), "skipped": len(result.skipped), "successful": result.wasSuccessful(),
        "failure_ids": [case.id() for case, _ in result.failures],
        "error_ids": [case.id() for case, _ in result.errors],
        "full_repository_suite_run": False,
    }


def check(name: str, condition: bool, details: Any = None) -> dict[str, Any]:
    return {"name": name, "pass": bool(condition), "details": details}


def detailed_checks(stage: str) -> list[dict[str, Any]]:
    x1 = load("x1-proposals.json")
    x2 = load("x2-proposal-ledger.json")
    approval = load("approval-packets/x2-portfolio-execution.json")
    candidates = load("prototypes/x2-candidate-execution.json")
    skills = load("prototypes/skill-build-use-receipt.json")
    runners = load("prototypes/runner-build-use-receipt.json")
    clean = load("maintenance/x2-clean-refine-ledger.json")
    negatives = load("retained-negative-register-x2.json")
    synthetic = load("validation/preregistered-synthetic-negatives.json")
    gates = load("exact-open-gate-register-x2.json")
    truth = load("phase-truth.json")
    seal = load("reproduction/x1-content-seal.json")
    method = load("method-flow/method-flow-state.json")
    outcomes = Counter(row["outcome"] for row in x2["proposals"])
    rows = [
        check("x1 proposal count", len(x1["proposals"]) == 10),
        check("x1 remains plan only", x1["x2_execution_present"] is False),
        check("frozen chain count", x1["frozen_chain_count_after_x1"] == 530),
        check("x2 proposal count", len(x2["proposals"]) == 10),
        check("outcome vocabulary", set(outcomes) == {"completed", "represented", "open_gap", "exact_gate"}),
        check("outcome distribution", outcomes == Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})),
        check("safe count", approval["safe_now_completed"] == 30),
        check("candidate portfolio count", approval["candidates_completed"] == 20),
        check("candidate prototypes", candidates["invoked_count"] == 20),
        check("skill count", skills["skill_count"] == 20),
        check("skill validation", skills["validated_count"] == 20),
        check("skill smoke use", skills["smoke_used_count"] == 20),
        check("runner inventory", runners["runner_count"] == 10),
        check("runner invocation", runners["invoked_count"] >= (9 if stage == "evidence" else 10)),
        check("cleanup count", clean["completed_count"] == 30),
        check("cleanup nondestructive", clean["destructive_count"] == 0),
        check("exact packets unexecuted", approval["exact_executed"] == 0),
        check("blocked packets unexecuted", approval["blocked_executed"] == 0),
        check("synthetic count", synthetic["count"] == 70),
        check("synthetic rejected", synthetic["rejected_count"] == 70),
        check("synthetic retained", synthetic["retained_count"] == 70),
        check("negative total", negatives["effective_total"] >= 3669),
        check("no erased negative", negatives["erased_negative_count"] == 0),
        check("open gaps", gates["effective_open_gaps"] == 23),
        check("exact gates", gates["effective_exact_gates"] == 24),
        check("no gate software closure", gates["closed_by_software"] == 0),
        check("x1 seal entries", seal["entry_count"] == 8),
        check("x1 seal parity", seal["mismatch_count"] == 0),
        check("method failures retained", method["counts"]["witness_results"]["fail"] >= 5),
        check("method passing witnesses", method["counts"]["witness_results"]["pass"] >= 5),
        check("zero real rows", truth["real_rows"] == 0),
        check("zero real people", truth["real_people_or_operations"] == 0),
        check("zero real keys", truth["real_keys_or_tokens"] == 0),
        check("zero authority decisions", truth["authority_decisions"] == 0),
        check("terminal abstention", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"),
        check("route held", truth["route_state"] == "PREPARED_NOT_SENT"),
        check("stage vocabulary", stage in {"evidence", "final"}),
    ]
    return rows


def minimal_checks(stage: str) -> list[dict[str, Any]]:
    truth = load("phase-truth.json")
    required = [
        "x1-proposals.json", "x2-proposal-ledger.json", "phase-truth.json", "threat-model.json",
        "complete-incomplete-checklist.json", "retained-negative-register-x2.json", "exact-open-gate-register-x2.json",
        "evidence-receipt.json", "deliverables/v647-v6-final-integrated-overview.md",
        "deliverables/v647-v6-static-report.html", "deliverables/v647-v6-x2-wellbeing.md",
        "sources/source-ledger.json", "method-flow/method-flow-state.json",
        "prototypes/skill-build-use-receipt.json", "prototypes/runner-build-use-receipt.json",
    ]
    rows = [check(f"required {path}", (PHASE / path).is_file()) for path in required]
    rows.extend([
        check("phase identity", truth["phase"] == "v647-gmut-thos-v6-x1-x2"),
        check("owner identity", truth["owner"] == "Ilyra Fen"),
        check("proposal chain", truth["frozen_proposals_through_phase"] == 530),
        check("abstention", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"),
        check("stage", stage in {"evidence", "final"}),
    ])
    return rows


def parse_json() -> tuple[int, list[str]]:
    issues = []
    count = 0
    for path in PHASE.rglob("*.json"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
            count += 1
        except Exception as exc:  # pragma: no cover
            issues.append(f"{path.relative_to(PHASE).as_posix()}: {type(exc).__name__}")
    return count, issues


def privacy_scan() -> tuple[int, list[dict[str, str]]]:
    patterns = {
        "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_local_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
        "private_uri": re.compile(r"\b(?:app|plugin)://", re.I),
        "delegation_markup": re.compile(r"<(?:codex_delegation|source_thread_id)>", re.I),
        "credential_assignment": re.compile(r"\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']", re.I),
    }
    hits = []
    files = 0
    for path in PHASE.rglob("*"):
        if not path.is_file():
            continue
        files += 1
        text = path.read_text(encoding="utf-8")
        for label, pattern in patterns.items():
            if pattern.search(text):
                hits.append({"path": path.relative_to(PHASE).as_posix(), "pattern_class": label})
    return files, hits


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=["evidence", "final"], default="evidence")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--read-only", action="store_true")
    parser.add_argument("--external-output", type=Path)
    args = parser.parse_args()
    tests = run_tests(args.stage == "final")
    detailed = detailed_checks(args.stage)
    minimal = minimal_checks(args.stage)
    json_count, json_issues = parse_json()
    privacy_files, privacy_hits = privacy_scan()
    issues = []
    if not tests["successful"]:
        issues.append("bounded unittest selection failed")
    issues.extend(row["name"] for row in detailed + minimal if not row["pass"])
    issues.extend(json_issues)
    issues.extend(f"privacy:{row['pattern_class']}:{row['path']}" for row in privacy_hits)
    payload = {
        "schema": "ghc.family.v647-v6.validation.v1", "stage": args.stage,
        "tests": tests, "detailed_check_count": len(detailed), "detailed_pass_count": sum(row["pass"] for row in detailed),
        "minimal_check_count": len(minimal), "minimal_pass_count": sum(row["pass"] for row in minimal),
        "json_parse_count": json_count, "json_issues": json_issues,
        "privacy_file_count": privacy_files, "privacy_pattern_classes": 5, "privacy_confirmed_hits": privacy_hits,
        "issue_count": len(issues), "issues": issues, "valid": not issues,
        "full_repository_suite_run": False, "same_owner_only": True, "independent_reproduction": False,
        "boundary": "Bounded non-Eiren validation only; no empirical, production, professional, authority, complete-accessibility, exhaustive-security, or independent-reproduction claim.",
    }
    output = args.external_output if args.read_only else args.output
    if output:
        write_json(output, payload)
    print(json.dumps({"stage": args.stage, "tests": tests["tests_run"], "detailed": len(detailed), "minimal": len(minimal), "json": json_count, "privacy_files": privacy_files, "privacy_hits": len(privacy_hits), "issues": len(issues), "valid": not issues}))
    raise SystemExit(0 if not issues else 1)


if __name__ == "__main__":
    main()
