#!/usr/bin/env python3
"""Scoped detailed/minimal validator for Sylven Arc v648-v2."""

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
PHASE = ROOT / "docs" / "sylven-arc" / "v648-v2"
RAW_ID = re.compile(r"\b019[a-f0-9]{5}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\b", re.I)
PRIVATE_PATH = re.compile(r"(?:[A-Za-z]:\\(?:Users|GHC-Archives)\\|/Users/|/home/)", re.I)
SECRET_ASSIGNMENT = re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|private[_-]?key|client[_-]?secret)\s*[:=]\s*['\"][^'\"]+")
PRIVATE_RECORD = re.compile(r"(?i)(?:source_thread_id|rollout_path|session_meta\.payload\.id)")
PRIVATE_CALLABLE = re.compile(r"(?i)(?:mcp__|codex_app__send_message_to_thread)")


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def add(checks: list[dict[str, Any]], name: str, condition: bool, observed: Any) -> None:
    checks.append({"name": name, "pass": bool(condition), "observed": observed})


def validate(mode: str, lifecycle: str) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    required = [
        "x1-proposals.json",
        "x2-proposal-ledger.json",
        "retained-negative-register.json",
        "exact-open-gate-register.json",
        "phase-truth.json",
        "threat-model.json",
        "complete-incomplete-checklist.json",
        "v648-v2-integrated-overview.md",
        "deliverables/v648-v2-static-report.html",
        "skills/skill-build-receipt.json",
        "tooling/runner-execution.json",
        "method-flow/method-flow-validation.json",
    ]
    if lifecycle != "evidence":
        required.extend(
            [
                "closeout-receipt.json",
                "seal-receipt.json",
                "final-receipt.json",
                "final-validation-record.json",
                "retained-negative-register-final.json",
                "validation/lifecycle-operational-negatives.json",
                "validation/final-validation-protocol.json",
                "orchestration/successor-baton-preparation.json",
                "orchestration/terminal-route-state.json",
            ]
        )
    missing = [path for path in required if not (PHASE / path).exists()]
    add(checks, "required_files", not missing, missing)
    if missing:
        return {"valid": False, "mode": mode, "lifecycle": lifecycle, "checks": checks}

    x1 = load("x1-proposals.json")
    x2 = load("x2-proposal-ledger.json")
    negatives = load("retained-negative-register.json")
    gates = load("exact-open-gate-register.json")
    skills = load("skills/skill-build-receipt.json")
    runners = load("tooling/runner-execution.json")
    method_state = load("method-flow/method-flow-state.json")
    method_validation = load("method-flow/method-flow-validation.json")
    outcomes = Counter(row["outcome"] for row in x2["rows"])
    witness_results = Counter(row["result"] for row in method_state["witnesses"])
    add(checks, "x1_ten", len(x1["proposals"]) == 10, len(x1["proposals"]))
    add(checks, "frozen_570", x1["frozen_chain_count_after_x1"] == 570, x1["frozen_chain_count_after_x1"])
    add(checks, "x2_ten", len(x2["rows"]) == 10, len(x2["rows"]))
    add(checks, "outcomes_6_2_1_1", outcomes == Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}), dict(outcomes))
    add(checks, "terminal_not_ready", x2["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", x2["terminal_verdict"])
    add(checks, "negatives_arithmetic", negatives["effective_total"] == negatives["inherited_effective"] + negatives["x1_operational"] + negatives["preregistered_synthetic"] + negatives["x2_operational"], negatives["effective_total"])
    add(checks, "activation_baseline", negatives["inherited_effective"] == 3938, negatives["inherited_effective"])
    add(checks, "x1_and_synthetic_negatives", (negatives["x1_operational"], negatives["preregistered_synthetic"]) == (7, 70), [negatives["x1_operational"], negatives["preregistered_synthetic"]])
    add(checks, "x2_failures_retained", negatives["x2_operational"] >= 6, negatives["x2_operational"])
    mutation_register = load("validation/preregistered-synthetic-negatives.json")
    add(checks, "all_mutations", (mutation_register["executed"], mutation_register["rejected"]) == (70, 70), [mutation_register["executed"], mutation_register["rejected"]])
    add(checks, "gate_counts", (gates["effective_open_gaps"], gates["effective_exact_gates"]) == (27, 28), [gates["effective_open_gaps"], gates["effective_exact_gates"]])
    add(checks, "skills_20", (skills["count"], skills["quick_validated"], skills["smoke_used"]) == (20, 20, 20), [skills["count"], skills["quick_validated"], skills["smoke_used"]])
    add(checks, "runners_built_and_used", (runners["built_count"], runners["used_count"]) == (10, 10), [runners["built_count"], runners["used_count"]])
    add(checks, "method_flow_balanced", witness_results["fail"] == witness_results["pass"] and witness_results["fail"] >= method_state["counts"]["methods"], dict(witness_results))
    add(checks, "method_flow_preferred", all(row["recommendation_state"] == "preferred" for row in method_state["methods"]), method_state["counts"]["states"])
    add(checks, "method_flow_valid", method_validation["valid"] and not method_validation["privacy_hits"], method_validation.get("issues", []))
    if lifecycle != "evidence":
        final_negatives = load("retained-negative-register-final.json")
        closeout = load("closeout-receipt.json")
        route = load("orchestration/successor-baton-preparation.json")
        add(checks, "final_negative_arithmetic", final_negatives["effective_total"] == final_negatives["inherited_effective"] + final_negatives["x1_operational"] + final_negatives["preregistered_synthetic"] + final_negatives["x2_operational"] + final_negatives["lifecycle_operational"], final_negatives["effective_total"])
        add(checks, "no_negative_erasure", final_negatives["erased_negative_count"] == 0, final_negatives["erased_negative_count"])
        add(checks, "closeout_counts", (closeout["effective_open_gaps"], closeout["effective_exact_gates"]) == (27, 28), [closeout["effective_open_gaps"], closeout["effective_exact_gates"]])
        add(checks, "route_prepared_for_eiren", route["target_existing_task_title"] == "Eiren Kestrel" and route["state"] == "PREPARED_NOT_SENT", [route["target_existing_task_title"], route["state"]])

    json_errors = []
    json_files = sorted(PHASE.rglob("*.json"))
    for path in json_files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # pragma: no cover
            json_errors.append({"path": path.relative_to(ROOT).as_posix(), "error": type(exc).__name__})
    add(checks, "json_parse", not json_errors, len(json_files))

    privacy_hits = []
    word_violations = []
    patterns = {
        "raw_task_or_thread_id": RAW_ID,
        "private_absolute_path": PRIVATE_PATH,
        "credential_or_key_assignment": SECRET_ASSIGNMENT,
        "private_session_or_route_record": PRIVATE_RECORD,
        "private_callable_identifier": PRIVATE_CALLABLE,
    }
    public_files = [path for path in sorted(PHASE.rglob("*")) if path.is_file()]
    for path in public_files:
        text = path.read_text(encoding="utf-8")
        for class_name, pattern in patterns.items():
            if pattern.search(text):
                privacy_hits.append({"path": path.relative_to(ROOT).as_posix(), "class": class_name})
        if path.suffix.lower() in {".md", ".html"}:
            words = len(re.findall(r"\b\w+\b", text, re.UNICODE))
            if words > 6000:
                word_violations.append({"path": path.relative_to(ROOT).as_posix(), "words": words})
    add(checks, "privacy_zero", not privacy_hits, privacy_hits)
    add(checks, "word_caps", not word_violations, word_violations)

    test_result = {"run": False, "returncode": None, "tests": 0, "output": ""}
    if mode == "detailed":
        if str(ROOT) not in sys.path:
            sys.path.insert(0, str(ROOT))
        selection = [
            "tests.test_ghc_family_v647_v8_x1",
            "tests.test_ghc_family_v647_v8",
            "tests.test_ghc_family_v647_v8_closeout.V647V8CloseoutTests.test_closeout_counts_and_abstention",
            "tests.test_ghc_family_v647_v8_closeout.V647V8CloseoutTests.test_closeout_operational_negatives_are_retained",
            "tests.test_ghc_family_v647_v8_closeout.V647V8CloseoutTests.test_final_records_do_not_preclaim_postcommit_proof",
            "tests.test_ghc_family_v647_v8_closeout.V647V8CloseoutTests.test_route_is_prepared_not_sent",
            "tests.test_ghc_family_v647_v8_closeout.V647V8CloseoutTests.test_documents_and_growth_are_bounded",
            "tests.test_ghc_family_v647_v8_closeout.V647V8CloseoutTests.test_owner_manifest_covers_exact_phase_surface",
            "tests.test_ghc_family_v648_v1_x1",
            "tests.test_ghc_family_v648_v1",
            "tests.test_ghc_family_v648_v1_closeout.V648V1CloseoutTests.test_closeout_counts_and_abstention",
            "tests.test_ghc_family_v648_v1_closeout.V648V1CloseoutTests.test_closeout_operational_negatives_are_retained",
            "tests.test_ghc_family_v648_v1_closeout.V648V1CloseoutTests.test_final_records_do_not_preclaim_postcommit_proof",
            "tests.test_ghc_family_v648_v1_closeout.V648V1CloseoutTests.test_route_is_prepared_not_sent",
            "tests.test_ghc_family_v648_v1_closeout.V648V1CloseoutTests.test_documents_and_growth_are_bounded",
            "tests.test_ghc_family_v648_v1_closeout.V648V1CloseoutTests.test_owner_manifest_covers_exact_phase_surface",
            "tests.test_ghc_family_v648_v2_x1",
            "tests.test_ghc_family_v648_v2",
        ]
        if lifecycle != "evidence":
            selection.append("tests.test_ghc_family_v648_v2_closeout")
        suite = unittest.defaultTestLoader.loadTestsFromNames(selection)
        stream = io.StringIO()
        result = unittest.TextTestRunner(stream=stream, verbosity=1).run(suite)
        test_result = {
            "run": True,
            "selection": selection,
            "returncode": 0 if result.wasSuccessful() else 1,
            "tests": result.testsRun,
            "output": stream.getvalue()[-20000:],
            "excluded": [
                "tests.test_ghc_family_v647_v8_closeout.V647V8CloseoutTests.test_anchor_contract_and_commit_cap: original phase-local source-to-head assertion",
                "tests.test_ghc_family_v648_v1_closeout.V648V1CloseoutTests.test_anchor_contract_and_commit_cap: inherited source phase-local assertion",
            ],
        }
        add(checks, "scoped_tests", result.wasSuccessful() and result.testsRun > 0, result.testsRun)

    valid = all(row["pass"] for row in checks)
    return {
        "schema": f"ghc.family.v648-v2.validation.{mode}.v1",
        "mode": mode,
        "lifecycle": lifecycle,
        "valid": valid,
        "checks_total": len(checks),
        "checks_passed": sum(row["pass"] for row in checks),
        "json_files_parsed": len(json_files),
        "public_files_scanned": len(public_files),
        "privacy_pattern_classes": sorted(patterns),
        "privacy_hits": privacy_hits,
        "word_cap_violations": word_violations,
        "test_result": test_result,
        "checks": checks,
        "boundary": "Scoped same-owner validation is not the Eiren-owned full repository suite, independent reproduction, external audit, production certification, complete privacy, exhaustive security, or complete accessibility conformance.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["detailed", "minimal"], required=True)
    parser.add_argument("--lifecycle", choices=["evidence", "closeout", "final", "named_replay"], required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--no-write-witness", action="store_true")
    args = parser.parse_args()
    witness_path = PHASE / "validation" / "runner-witnesses" / "validation-runner.json"
    if not args.no_write_witness:
        write(
            witness_path,
            {
                "schema": "ghc.family.v648-v2.runner-witness.v1",
                "runner": "ghc_family_v648_v2_validation_runner.py",
                "mode": args.mode,
                "lifecycle": args.lifecycle,
                "used": True,
                "same_owner_only": True,
                "independent_reproduction": False,
            },
        )
    result = validate(args.mode, args.lifecycle)
    write(args.receipt, result)
    print(json.dumps({"valid": result["valid"], "checks": result.get("checks_total", len(result["checks"])), "json": result.get("json_files_parsed", 0), "tests": result.get("test_result", {}).get("tests", 0)}, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
