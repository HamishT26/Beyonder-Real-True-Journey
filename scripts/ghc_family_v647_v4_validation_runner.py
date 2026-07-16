#!/usr/bin/env python3
"""Bounded current, scoped-detailed, and minimal validator for Sylven v647-v4."""

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
PHASE = ROOT / "docs" / "sylven-arc" / "v647-v4"
PATTERNS = {
    "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    "private_absolute_path": re.compile(r"(?:[A-Za-z]:\\(?:Users|GHC-Archives|Documents|AppData)\\|/Users/|/home/)", re.I),
    "credential_or_private_key": re.compile(r"(?:ghp_[A-Za-z0-9]{20,}|sk-(?:proj-|svcacct-)?[A-Za-z0-9]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|Bearer\s+[A-Za-z0-9._~-]{16,})", re.I),
    "private_callable_identifier": re.compile(r"\b(?:mcp__|codex_app__|browser_(?:send|probe|route|callable)_[a-z0-9_]{4,})", re.I),
    "private_conversation_or_session_record": re.compile(r"(?:source_thread_id|rollout_path|session_meta\.payload\.id|session[_ -]?stream|raw transcript)", re.I),
}


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def add(checks: list[dict[str, Any]], name: str, condition: bool, observed: Any) -> None:
    checks.append({"name": name, "pass": bool(condition), "observed": observed})


def run_tests(selection: list[str]) -> dict[str, Any]:
    total, outputs, codes = 0, [], []
    for relative in selection:
        proc = subprocess.run([sys.executable, str(ROOT / relative), "-v"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        combined = (proc.stdout + "\n" + proc.stderr).strip()
        combined = combined.replace(str(ROOT), "<repository-root>").replace(str(ROOT).replace("\\", "/"), "<repository-root>")
        match = re.search(r"Ran (\d+) tests?", combined)
        total += int(match.group(1)) if match else 0
        outputs.append(f"## {relative}\n{combined}")
        codes.append(proc.returncode)
    return {"run": True, "selection": selection, "returncode": max(codes) if codes else 1, "tests": total, "output": "\n\n".join(outputs)[-30000:]}


def validate(mode: str, lifecycle: str) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    required = [
        "x1-proposals.json", "x2-proposal-ledger.json", "retained-negative-register.json",
        "exact-open-gate-register.json", "phase-truth.json", "threat-model.json",
        "complete-incomplete-checklist.json", "v647-v4-integrated-overview.md",
        "deliverables/v647-v4-static-report.html", "deliverables/owner-scoped-packet.json",
        "skills/skill-build-receipt.json", "tooling/runner-execution.json",
        "method-flow/method-flow-state.json", "evidence-receipt.json",
    ]
    missing = [relative for relative in required if not (PHASE / relative).is_file()]
    add(checks, "required_files", not missing, missing)
    if missing:
        return {"valid": False, "mode": mode, "lifecycle": lifecycle, "checks": checks, "test_result": {"run": False, "tests": 0}}

    x1 = load("x1-proposals.json")
    x2 = load("x2-proposal-ledger.json")
    negatives = load("retained-negative-register.json")
    gates = load("exact-open-gate-register.json")
    skills = load("skills/skill-build-receipt.json")
    runners = load("tooling/runner-execution.json")
    method = load("method-flow/method-flow-state.json")
    outcomes = Counter(row["outcome"] for row in x2["rows"])
    add(checks, "x1_ten_and_frozen_510", len(x1["proposals"]) == 10 and x1["frozen_chain_count_after_x1"] == 510, [len(x1["proposals"]), x1["frozen_chain_count_after_x1"]])
    add(checks, "x2_ten", len(x2["rows"]) == 10, len(x2["rows"]))
    add(checks, "outcomes_6_2_1_1", outcomes == Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}), dict(outcomes))
    add(checks, "outcome_vocabulary", set(x2["outcome_vocabulary"]) == {"completed", "represented", "open_gap", "exact_gate"}, x2["outcome_vocabulary"])
    add(checks, "terminal_not_ready", x2["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", x2["terminal_verdict"])
    add(checks, "negative_arithmetic", negatives["effective_total"] == negatives["inherited_effective"] + negatives["x1_operational"] + negatives["preregistered_synthetic"] + negatives["x2_operational"], negatives["effective_total"])
    add(checks, "all_mutations", load("validation/preregistered-synthetic-negatives.json")["rejected"] == 70, load("validation/preregistered-synthetic-negatives.json")["rejected"])
    add(checks, "all_real_counters_zero", load("validation/real-world-zero-receipt.json")["all_zero"], load("validation/real-world-zero-receipt.json")["counters"])
    add(checks, "gate_counts", (gates["effective_open_gaps"], gates["effective_exact_gates"]) == (21, 22), [gates["effective_open_gaps"], gates["effective_exact_gates"]])
    add(checks, "skills_20", (skills["count"], skills["quick_validated"], skills["smoke_used"]) == (20, 20, 20), [skills["count"], skills["quick_validated"], skills["smoke_used"]])
    add(checks, "runners_10", (runners["built_count"], runners["used_count"]) == (10, 10), [runners["built_count"], runners["used_count"]])
    method_results = method["counts"]["witness_results"]
    method_flow_current = method_results["fail"] >= 3 and method_results["fail"] - method_results["pass"] in (0, 1)
    add(checks, "method_flow_failures_retained", method_flow_current, method_results)
    add(checks, "route_not_sent", load("phase-truth.json")["route_state"] == "PREPARED_NOT_SENT", load("phase-truth.json")["route_state"])
    add(checks, "full_suite_reserved", not load("phase-truth.json")["full_repository_suite_run"] and load("phase-truth.json")["full_repository_suite_owner"] == "Eiren Kestrel", load("phase-truth.json")["full_repository_suite_owner"])

    json_errors, privacy_hits, word_violations = [], [], []
    json_files = sorted(PHASE.rglob("*.json"))
    public_files = [path for path in sorted(PHASE.rglob("*")) if path.is_file()]
    for path in json_files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            json_errors.append({"path": path.relative_to(ROOT).as_posix(), "error": type(exc).__name__})
    for path in public_files:
        text = path.read_text(encoding="utf-8")
        for class_name, pattern in PATTERNS.items():
            if pattern.search(text):
                privacy_hits.append({"path": path.relative_to(ROOT).as_posix(), "class": class_name})
        if path.suffix.lower() in {".md", ".html"}:
            words = len(re.findall(r"\b\w+\b", text, re.UNICODE))
            if words > 6000:
                word_violations.append({"path": path.relative_to(ROOT).as_posix(), "words": words})
    add(checks, "json_parse", not json_errors, len(json_files) if not json_errors else json_errors)
    add(checks, "privacy_five_class_zero", not privacy_hits, privacy_hits)
    add(checks, "document_word_caps", not word_violations, word_violations)
    overview_words = len(re.findall(r"\b\w+\b", (PHASE / "v647-v4-integrated-overview.md").read_text(encoding="utf-8"), re.UNICODE))
    add(checks, "three_page_overview", 1200 <= overview_words <= 6000, overview_words)
    static = (PHASE / "deliverables" / "v647-v4-static-report.html").read_text(encoding="utf-8")
    static_tokens = ["<main", "<nav", "<caption", 'scope="col"', "Manual keyboard", "affected-user evaluation", "@media print"]
    add(checks, "static_report_structure", all(token in static for token in static_tokens), static_tokens)
    owner_files = sum(1 for path in PHASE.rglob("*") if path.is_file()) + sum(1 for path in (ROOT / "scripts").glob("*v647_v4*") if path.is_file()) + sum(1 for path in (ROOT / "tests").glob("*v647_v4*") if path.is_file())
    add(checks, "owner_file_threshold", owner_files < 15000, owner_files)

    test_result = {"run": False, "selection": [], "returncode": None, "tests": 0, "output": ""}
    if mode == "current":
        test_result = run_tests(["tests/test_ghc_family_v647_v4_x1.py", "tests/test_ghc_family_v647_v4.py"])
        add(checks, "current_phase_tests", test_result["returncode"] == 0 and test_result["tests"] > 0, test_result["tests"])
    elif mode == "detailed":
        selection = [
            "tests/test_ghc_family_v646_v7.py", "tests/test_ghc_family_v646_v8.py",
            "tests/test_ghc_family_v647_v1_x1.py", "tests/test_ghc_family_v647_v1.py",
            "tests/test_ghc_family_v647_v2_x1.py", "tests/test_ghc_family_v647_v2.py",
            "tests/test_ghc_family_v647_v3_x1.py", "tests/test_ghc_family_v647_v3.py",
        ]
        test_result = run_tests(selection)
        test_result["excluded"] = [
            "tests/test_ghc_family_v646_v7_closeout.py: original-phase commit and head assertions",
            "tests/test_ghc_family_v646_v8_closeout.py: original-phase commit and head assertions",
        ]
        add(checks, "authorized_recent_and_successor_scoped_tests", test_result["returncode"] == 0 and test_result["tests"] > 0, test_result["tests"])

    if mode == "minimal":
        minimal_names = {
            "required_files", "x1_ten_and_frozen_510", "x2_ten", "outcomes_6_2_1_1",
            "terminal_not_ready", "negative_arithmetic", "all_mutations", "all_real_counters_zero",
            "gate_counts", "route_not_sent", "full_suite_reserved", "json_parse",
            "privacy_five_class_zero", "owner_file_threshold",
        }
        checks = [row for row in checks if row["name"] in minimal_names]

    valid = all(row["pass"] for row in checks)
    return {
        "schema": f"ghc.family.v647-v4.validation.{mode}.v1",
        "mode": mode,
        "lifecycle": lifecycle,
        "valid": valid,
        "checks_total": len(checks),
        "checks_passed": sum(row["pass"] for row in checks),
        "json_files_parsed": len(json_files),
        "public_files_scanned": len(public_files),
        "privacy_pattern_classes": sorted(PATTERNS),
        "privacy_hits": privacy_hits,
        "word_cap_violations": word_violations,
        "test_result": test_result,
        "checks": checks,
        "boundary": "Scoped same-owner validation is not the Eiren-owned full repository suite, independent reproduction, external audit, production certification, complete privacy, exhaustive security, or complete accessibility conformance.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["current", "detailed", "minimal"], required=True)
    parser.add_argument("--lifecycle", choices=["evidence", "closeout", "final", "named_replay"], required=True)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = validate(args.mode, args.lifecycle)
    if not args.no_write:
        if args.receipt is None:
            raise SystemExit("--receipt is required unless --no-write is used")
        write(args.receipt, result)
        write(PHASE / "validation" / "runner-witnesses" / f"validation-{args.mode}-{args.lifecycle}.json", {"schema": "ghc.family.v647-v4.validation-runner-witness.v1", "runner": "ghc_family_v647_v4_validation_runner.py", "mode": args.mode, "lifecycle": args.lifecycle, "used": True, "same_owner_only": True, "independent_reproduction": False})
    print(json.dumps({"valid": result["valid"], "checks": result["checks_total"], "json": result.get("json_files_parsed", 0), "files": result.get("public_files_scanned", 0), "tests": result["test_result"].get("tests", 0)}, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
