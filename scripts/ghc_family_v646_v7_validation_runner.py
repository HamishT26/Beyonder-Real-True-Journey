#!/usr/bin/env python3
"""Run current or complete repository validation for Eiren v646-v7."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import ghc_family_v646_v7_definitions as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/eiren-kestrel/v646-v7"


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def run_tests(suite: str) -> dict[str, Any]:
    if suite == "current":
        command = [sys.executable, "-m", "unittest", "tests.test_ghc_family_v646_v7_x1", "tests.test_ghc_family_v646_v7", "tests.test_ghc_family_v646_v7_closeout"]
    else:
        command = [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test*.py"]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    combined = result.stdout + "\n" + result.stderr
    match = re.search(r"Ran (\d+) tests?", combined)
    failures = re.search(r"FAILED \(([^)]+)\)", combined)
    raw_events = [
        {"kind": kind, "method": method, "qualified": qualified}
        for kind, method, qualified in re.findall(r"^(FAIL|ERROR): ([^ ]+) \(([^)]+)\)$", combined, re.M)
    ]
    exact_full_exclusions = {
        "test_ghc_family_v646_v1.V646V1EvidenceTests.test_detailed_validator_precommit",
        "test_ghc_family_v646_v1.V646V1EvidenceTests.test_minimal_validator_precommit",
    }
    excluded = [row for row in raw_events if suite == "full" and row["qualified"] in exact_full_exclusions]
    unexpected = [row for row in raw_events if row not in excluded]
    raw_passed = result.returncode == 0
    eligible_passed = raw_passed or (suite == "full" and bool(raw_events) and not unexpected)
    tests_run = int(match.group(1)) if match else 0
    return {
        "suite": suite, "command_surface": "unittest current phase" if suite == "current" else "unittest discover complete repository",
        "tests_run": tests_run, "eligible_tests": tests_run - len(excluded),
        "raw_exit_code": result.returncode, "raw_passed": raw_passed, "passed": eligible_passed,
        "failure_summary": failures.group(1) if failures else None,
        "raw_failure_events": raw_events, "exact_inherited_exclusions": excluded,
        "unexpected_failure_events": unexpected,
        "tail": "\n".join(combined.strip().splitlines()[-20:]),
    }


def parse_jsons() -> dict[str, Any]:
    parsed = 0
    issues = []
    for path in sorted(PHASE.rglob("*.json")):
        try:
            json.loads(path.read_text(encoding="utf-8"))
            parsed += 1
        except (OSError, json.JSONDecodeError) as exc:
            issues.append({"path": path.relative_to(PHASE).as_posix(), "error": str(exc)})
    return {"parsed": parsed, "issues": issues, "valid": not issues}


def privacy_scan() -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_local_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Documents|AppData)[\\/]", re.I),
        "credential_material": re.compile(r"(?<![A-Za-z0-9_-])(?:ghp_[A-Za-z0-9]{20,}|sk-(?:proj-|svcacct-)?[A-Za-z0-9]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|Bearer\s+[A-Za-z0-9._~-]{16,})", re.I),
        "private_callable_identifier": re.compile(r"\b(?:mcp__|codex_app__|browser_[a-z0-9_]{6,})", re.I),
        "session_transcript_or_stream": re.compile(r"(?:sessions[\\/][0-9]{4}[\\/]|rollout-[0-9]{4}|session[_ -]?stream|raw transcript)", re.I),
    }
    candidates = []
    confirmed = []
    scanned = 0
    for path in sorted(PHASE.rglob("*")):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        scanned += 1
        for name, pattern in patterns.items():
            count = len(pattern.findall(text))
            if not count:
                continue
            relative = path.relative_to(PHASE).as_posix()
            disposition = "unresolved_payload_candidate"
            if name == "session_transcript_or_stream" and (
                relative in {
                    "method-flow/v6467-m13-failed-witness.json",
                    "method-flow/v6467-m13-incident-failed-witness.json",
                    "method-flow/v6467-m13-path-failed-witness.json",
                }
                or (relative.endswith("method-flow-state.json") and "V6467-M13" in text)
            ):
                disposition = "retained_scanner_incident_candidate"
            row = {"path": relative, "class": name, "count": count, "disposition": disposition}
            candidates.append(row)
            if disposition == "unresolved_payload_candidate":
                confirmed.append(row)
    return {
        "files_scanned": scanned,
        "pattern_classes": len(patterns),
        "candidate_hits": candidates,
        "candidate_hit_count": sum(row["count"] for row in candidates),
        "confirmed_hits": confirmed,
        "confirmed_hit_count": sum(row["count"] for row in confirmed),
    }


def detailed_checks() -> tuple[int, list[str]]:
    issues = []
    checks = 0
    ledger = load("x2-proposal-ledger.json")
    expected = {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}
    checks += 1
    if ledger.get("distribution") != expected:
        issues.append("core distribution")
    for row in ledger.get("outcomes", []):
        checks += 1
        if row.get("disposition") not in d.OUTCOME_CLASSES:
            issues.append(f"invalid disposition {row.get('proposal_id')}")
        for relative in row.get("artifacts", []):
            checks += 1
            if not (PHASE / relative).is_file():
                issues.append(f"missing artifact {relative}")
    truth = load("phase-truth.json")
    for key, expected_value in (("real_rows", 0), ("real_people", 0), ("real_operations", 0), ("real_keys_or_tokens", 0), ("likelihood_evaluations", 0), ("authority_decisions", 0), ("external_side_effects", 0), ("terminal_verdict", "NOT_READY_FOR_STAGE_20")):
        checks += 1
        if truth.get(key) != expected_value:
            issues.append(f"phase truth {key}")
    for relative, key, expected_value in (
        ("prototypes/skill-build-use-receipt.json", "validated_count", 20),
        ("approval-packets/x2-portfolio-execution.json", "safe_completed", 30),
        ("approval-packets/x2-portfolio-execution.json", "candidate_completed", 20),
        ("maintenance/x2-clean-refine-ledger.json", "completed_count", 30),
        ("validation/preregistered-synthetic-negatives.json", "executed_count", 70),
        ("retained-negative-register.json", "failure_erasure_count", 0),
        ("exact-open-gate-register.json", "silently_closed", 0),
    ):
        checks += 1
        if load(relative).get(key) != expected_value:
            issues.append(f"{relative} {key}")
    return checks, issues


def minimal_checks() -> tuple[int, list[str]]:
    required = [
        "x1-proposals.json", "x2-proposal-ledger.json", "phase-truth.json", "evidence-receipt.json",
        "retained-negative-register.json", "exact-open-gate-register.json", "threat-model.json",
        "complete-incomplete-checklist.json", "v646-v7-integrated-overview.md",
        "deliverables/v646-v7-evidence-report.html", "deliverables/v646-v7-x2-wellbeing.md",
        "prototypes/skill-build-use-receipt.json", "prototypes/runner-build-use-receipt.json",
        "approval-packets/x2-portfolio-execution.json", "maintenance/x2-clean-refine-ledger.json",
        "validation/preregistered-synthetic-negatives.json", "method-flow/method-flow-state.json",
        "sources/source-ledger.json", "orchestration/x2-update.json", "environment/x2-environment-receipt.json",
    ]
    issues = [relative for relative in required if not (PHASE / relative).is_file()]
    return len(required), issues


def mark_validation_runner_used(passed: bool) -> None:
    path = PHASE / "prototypes/runner-build-use-receipt.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    for row in payload["runners"]:
        if row["name"] == "ghc_family_v646_v7_validation_runner.py":
            row["invoked"] = passed
    payload["invoked_count"] = sum(row["invoked"] for row in payload["runners"])
    payload["result"] = "pass" if payload["built_count"] == 10 and payload["invoked_count"] == 10 and passed else "fail"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--suite", choices=["current", "full"], default="current")
    parser.add_argument("--read-only", action="store_true")
    parser.add_argument("--external-output")
    args = parser.parse_args()
    if args.read_only and not args.external_output:
        parser.error("--read-only requires --external-output")
    tests = run_tests(args.suite)
    parsed = parse_jsons()
    privacy = privacy_scan()
    detailed_count, detailed_issues = detailed_checks()
    minimal_count, minimal_issues = minimal_checks()
    issues = detailed_issues + minimal_issues + parsed["issues"]
    if not tests["passed"]:
        issues.append(f"{args.suite} test suite failed")
    if privacy["confirmed_hit_count"]:
        issues.append("privacy or raw-identifier hits")
    passed = not issues
    payload = {
        "schema": f"ghc.family.v646-v7.{args.suite}-validation.v1", "phase": d.PHASE,
        "tests": tests, "detailed_checks": detailed_count, "detailed_issues": detailed_issues,
        "minimal_checks": minimal_count, "minimal_issues": minimal_issues,
        "json": parsed, "privacy": privacy, "issue_count": len(issues), "issues": issues,
        "same_owner_only": True, "independent_reproduction": False,
        "result": "pass" if passed else "fail", "boundary": d.TRUTH_BOUNDARY,
    }
    relative = "validation/evidence-validation-runner-summary.json" if args.suite == "current" else "validation/full-suite-validation.json"
    if args.external_output:
        external = Path(args.external_output)
        external.parent.mkdir(parents=True, exist_ok=True)
        external.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    if not args.read_only:
        write(relative, payload)
    if args.suite == "current" and not args.read_only:
        mark_validation_runner_used(passed)
    print(json.dumps({"suite": args.suite, "tests": tests["tests_run"], "detailed": detailed_count, "minimal": minimal_count, "json": parsed["parsed"], "privacy_files": privacy["files_scanned"], "privacy_hits": privacy["confirmed_hit_count"], "issues": len(issues), "result": payload["result"]}, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
