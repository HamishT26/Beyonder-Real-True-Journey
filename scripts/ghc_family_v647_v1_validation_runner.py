#!/usr/bin/env python3
"""Scoped detailed/minimal validator for Sable Rook v647-v1."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "sable-rook" / "v647-v1"
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
        "v647-v1-integrated-overview.md",
        "deliverables/v647-v1-static-report.html",
        "skills/skill-build-receipt.json",
        "tooling/runner-execution.json",
    ]
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
    outcomes = Counter(row["outcome"] for row in x2["rows"])
    add(checks, "x1_ten", len(x1["proposals"]) == 10, len(x1["proposals"]))
    add(checks, "frozen_480", x1["frozen_chain_count_after_x1"] == 480, x1["frozen_chain_count_after_x1"])
    add(checks, "x2_ten", len(x2["rows"]) == 10, len(x2["rows"]))
    add(checks, "outcomes_6_2_1_1", outcomes == Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}), dict(outcomes))
    add(checks, "terminal_not_ready", x2["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", x2["terminal_verdict"])
    add(checks, "negatives_arithmetic", negatives["effective_total"] == negatives["inherited_effective"] + negatives["x1_operational"] + negatives["preregistered_synthetic"] + negatives["x2_operational"], negatives["effective_total"])
    add(checks, "all_mutations", load("validation/preregistered-synthetic-negatives.json")["rejected"] == 70, load("validation/preregistered-synthetic-negatives.json")["rejected"])
    add(checks, "gate_counts", (gates["effective_open_gaps"], gates["effective_exact_gates"]) == (18, 19), [gates["effective_open_gaps"], gates["effective_exact_gates"]])
    add(checks, "skills_20", (skills["count"], skills["quick_validated"], skills["smoke_used"]) == (20, 20, 20), [skills["count"], skills["quick_validated"], skills["smoke_used"]])
    add(checks, "runners_built", runners["built_count"] == 10, runners["built_count"])

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
        selection = [
            "tests.test_ghc_family_v646_v7",
            "tests.test_ghc_family_v646_v8",
            "tests.test_ghc_family_v647_v1_x1",
            "tests.test_ghc_family_v647_v1",
        ]
        proc = subprocess.run(
            [sys.executable, "-m", "unittest", *selection, "-v"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        combined = (proc.stdout + "\n" + proc.stderr).strip()
        match = re.search(r"Ran (\d+) tests?", combined)
        test_result = {
            "run": True,
            "selection": selection,
            "returncode": proc.returncode,
            "tests": int(match.group(1)) if match else 0,
            "output": combined[-12000:],
            "excluded": [
                "tests.test_ghc_family_v646_v7_closeout: original-phase commit/head assertions",
                "tests.test_ghc_family_v646_v8_closeout: original-phase commit/head assertions",
            ],
        }
        add(checks, "scoped_tests", proc.returncode == 0 and test_result["tests"] > 0, test_result["tests"])

    valid = all(row["pass"] for row in checks)
    return {
        "schema": f"ghc.family.v647-v1.validation.{mode}.v1",
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
    args = parser.parse_args()
    witness_path = PHASE / "validation" / "runner-witnesses" / "validation-runner.json"
    write(
        witness_path,
        {
            "schema": "ghc.family.v647-v1.runner-witness.v1",
            "runner": "ghc_family_v647_v1_validation_runner.py",
            "mode": args.mode,
            "lifecycle": args.lifecycle,
            "used": True,
            "same_owner_only": True,
            "independent_reproduction": False,
        },
    )
    result = validate(args.mode, args.lifecycle)
    write(args.receipt, result)
    print(json.dumps({"valid": result["valid"], "checks": result["checks_total"], "json": result.get("json_files_parsed", 0), "tests": result["test_result"].get("tests", 0)}, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
