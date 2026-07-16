#!/usr/bin/env python3
"""Run the non-Eiren scoped v646-v8 validation selection; never the full suite."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import ghc_family_v646_v8_definitions as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/ilyra-fen/v646-v8"
X1 = "37c0e57d82fa8826d891a5b39f1fcb8ce0812a4a"

PATTERNS = {
    "raw_task_or_thread_identifier": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    "private_local_path": re.compile(rb"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Documents|AppData)[\\/]", re.I),
    "credential_material": re.compile(rb"(?<![A-Za-z0-9_-])(?:ghp_[A-Za-z0-9]{20,}|sk-(?:proj-|svcacct-)?[A-Za-z0-9]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|Bearer\s+[A-Za-z0-9._~-]{16,})", re.I),
    "private_callable_identifier": re.compile(rb"\b(?:mcp__|codex_app__|browser_[a-z0-9_]{6,})", re.I),
    "session_transcript_or_stream": re.compile(rb"(?:sessions[\\/][0-9]{4}[\\/]|rollout-[0-9]{4}|session[_ -]?stream|raw transcript)", re.I),
}


def read(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8").strip()


def mark_validation_runner_invoked() -> None:
    path = PHASE / "prototypes/runner-build-use-receipt.json"
    if not path.is_file():
        return
    receipt = json.loads(path.read_text(encoding="utf-8"))
    for row in receipt["runners"]:
        if row["name"] == "ghc_family_v646_v8_validation_runner.py":
            row["invoked"] = True
            row["passing_witness"] = "scoped validation runner entered with full-suite prohibition active"
    receipt["built_count"] = sum(row["built"] for row in receipt["runners"])
    receipt["invoked_count"] = sum(row["invoked"] for row in receipt["runners"])
    receipt["result"] = "pass" if receipt["built_count"] == receipt["invoked_count"] == 10 else "fail"
    path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def check(checks: list[dict[str, Any]], name: str, condition: bool, detail: Any) -> None:
    checks.append({"check": name, "passed": bool(condition), "detail": detail})


def privacy_scan() -> dict[str, Any]:
    files = sorted(path for path in PHASE.rglob("*") if path.is_file())
    hits = []
    for path in files:
        raw = path.read_bytes()
        for class_name, pattern in PATTERNS.items():
            count = len(list(pattern.finditer(raw)))
            if count:
                relative = path.relative_to(PHASE).as_posix()
                disposition = "confirmed_payload_hit"
                if relative == "accessibility/carousel-motion-contract.json" and class_name == "private_callable_identifier" and b"browser_diversity_evaluation" in raw:
                    disposition = "semantic_accessibility_field_candidate"
                elif relative in {"method-flow/v6468-m11-method-record.json", "method-flow/method-flow-state.json"} and class_name == "private_callable_identifier" and b"browser_diversity_evaluation" in raw:
                    disposition = "retained_scanner_incident_candidate"
                hits.append({"path": relative, "class": class_name, "count": count, "disposition": disposition})
    confirmed = [row for row in hits if row["disposition"] == "confirmed_payload_hit"]
    return {"files_scanned": len(files), "pattern_classes": len(PATTERNS), "candidate_hits": hits, "candidate_hit_count": sum(row["count"] for row in hits), "confirmed_hits": confirmed, "confirmed_hit_count": sum(row["count"] for row in confirmed)}


def json_parse() -> dict[str, Any]:
    issues = []
    count = 0
    for path in sorted(PHASE.rglob("*.json")):
        try:
            json.loads(path.read_text(encoding="utf-8"))
            count += 1
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            issues.append({"path": path.relative_to(PHASE).as_posix(), "error": str(exc)})
    return {"parsed": count, "issues": issues}


def run_scoped_tests() -> dict[str, Any]:
    result = subprocess.run(
        [sys.executable, str(ROOT / "tests/test_ghc_family_v646_v8.py"), "-v"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=120,
        check=False,
    )
    combined = result.stdout + result.stderr
    match = re.search(r"Ran (\d+) tests?", combined)
    diagnostic_tail = [line for line in combined.splitlines()[-24:] if line.strip()] if result.returncode else []
    return {"returncode": result.returncode, "tests_run": int(match.group(1)) if match else 0, "failures": combined.count("FAIL:"), "errors": combined.count("ERROR:"), "diagnostic_tail": diagnostic_tail, "result": "pass" if result.returncode == 0 else "fail"}


def validate(mode: str, expected_head: str | None, require_clean: bool, include_tests: bool) -> dict[str, Any]:
    mark_validation_runner_invoked()
    checks: list[dict[str, Any]] = []
    truth = read("phase-truth.json")
    ledger = read("x2-proposal-ledger.json")
    portfolio = read("approval-packets/x2-portfolio-execution.json")
    skills = read("prototypes/skill-build-use-receipt.json")
    runners = read("prototypes/runner-build-use-receipt.json")
    negatives = read("retained-negative-register.json")
    gates = read("exact-open-gate-register.json")
    check(checks, "ten_core_outcomes", len(ledger["outcomes"]) == 10, len(ledger["outcomes"]))
    check(checks, "exact_distribution", ledger["distribution"] == {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}, ledger["distribution"])
    check(checks, "allowed_outcomes", set(row["disposition"] for row in ledger["outcomes"]) <= set(d.OUTCOME_CLASSES), sorted(set(row["disposition"] for row in ledger["outcomes"])))
    check(checks, "safe_portfolio", portfolio["safe_completed"] == 30, portfolio["safe_completed"])
    check(checks, "candidate_portfolio", portfolio["candidate_completed"] == 20, portfolio["candidate_completed"])
    check(checks, "protected_packets_unexecuted", portfolio["exact_executed"] == portfolio["blocked_executed"] == 0, [portfolio["exact_executed"], portfolio["blocked_executed"]])
    check(checks, "skills_built_validated_used", (skills["built_count"], skills["validated_count"], skills["smoke_used_count"]) == (20, 20, 20), [skills["built_count"], skills["validated_count"], skills["smoke_used_count"]])
    check(checks, "runners_built_invoked", (runners["built_count"], runners["invoked_count"]) == (10, 10), [runners["built_count"], runners["invoked_count"]])
    check(checks, "negative_arithmetic", negatives["effective_total"] == negatives["inherited_effective"] + negatives["x1_operational"] + negatives["preregistered_synthetic"] + negatives["x2_operational"], negatives["effective_total"])
    check(checks, "synthetic_negatives", negatives["preregistered_synthetic"] == 70, negatives["preregistered_synthetic"])
    check(checks, "gates_preserved", (gates["effective_open_gaps"], gates["effective_exact_gates"], gates["silently_closed"]) == (17, 18, 0), [gates["effective_open_gaps"], gates["effective_exact_gates"], gates["silently_closed"]])
    check(checks, "real_data_zero", truth["real_rows"] == truth["likelihood_evaluations"] == truth["gmut_empirical_claims"] == 0, [truth["real_rows"], truth["likelihood_evaluations"], truth["gmut_empirical_claims"]])
    check(checks, "people_operations_zero", truth["real_people"] == truth["real_aircraft"] == truth["real_operations"] == 0, [truth["real_people"], truth["real_aircraft"], truth["real_operations"]])
    check(checks, "identity_production_zero", truth["real_keys_or_signatures"] == truth["production_identity_events"] == truth["interoperability_events"] == 0, [truth["real_keys_or_signatures"], truth["production_identity_events"], truth["interoperability_events"]])
    check(checks, "stage20_abstention", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", truth["terminal_verdict"])
    check(checks, "same_owner_only", truth["same_owner_repeatability_only"] and not truth["independent_reproduction"], [truth["same_owner_repeatability_only"], truth["independent_reproduction"]])
    check(checks, "source_ancestry", subprocess.run(["git", "merge-base", "--is-ancestor", d.SOURCE_REVISION, "HEAD"], cwd=ROOT, check=False).returncode == 0, d.SOURCE_REVISION)
    check(checks, "x1_ancestry", subprocess.run(["git", "merge-base", "--is-ancestor", X1, "HEAD"], cwd=ROOT, check=False).returncode == 0, X1)
    merge_count = int(git("rev-list", "--merges", "--count", f"{d.SOURCE_REVISION}..HEAD") or "0")
    check(checks, "zero_merges", merge_count == 0, merge_count)
    phase_commits = int(git("rev-list", "--count", f"{d.SOURCE_REVISION}..HEAD") or "0")
    check(checks, "commit_cap", phase_commits <= 4, phase_commits)
    if expected_head:
        check(checks, "exact_head", git("rev-parse", "HEAD") == expected_head, git("rev-parse", "HEAD"))
    if require_clean:
        status = git("status", "--porcelain")
        check(checks, "clean_worktree", status == "", status)

    parsed = json_parse()
    privacy = privacy_scan()
    check(checks, "json_parse", not parsed["issues"], parsed)
    check(checks, "five_class_privacy", privacy["confirmed_hit_count"] == 0, privacy)
    docs = [path for path in PHASE.rglob("*") if path.is_file() and path.suffix.lower() in {".md", ".html"}]
    over = [{"path": path.relative_to(PHASE).as_posix(), "words": len(path.read_text(encoding="utf-8").split())} for path in docs if len(path.read_text(encoding="utf-8").split()) > 6000]
    check(checks, "document_word_cap", not over, over)
    owner_files = sum(1 for path in PHASE.rglob("*") if path.is_file())
    check(checks, "owner_file_threshold", owner_files < 15000, owner_files)
    tests = run_scoped_tests() if include_tests else {"result": "not_requested", "tests_run": 0}
    if include_tests:
        check(checks, "scoped_tests", tests["result"] == "pass", tests)
    issues = [row for row in checks if not row["passed"]]
    return {
        "schema": f"ghc.family.v646-v8.{mode}-validation.v1",
        "phase": d.PHASE,
        "owner": d.OWNER,
        "mode": mode,
        "full_repository_suite_run": False,
        "full_repository_suite_owner": "Eiren Kestrel",
        "checks": checks,
        "check_count": len(checks),
        "issue_count": len(issues),
        "issues": issues,
        "json": parsed,
        "privacy": privacy,
        "scoped_tests": tests,
        "head": git("rev-parse", "HEAD"),
        "result": "pass" if not issues else "fail",
        "boundary": d.TRUTH_BOUNDARY,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["minimal", "detailed", "final"], required=True)
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--expected-head")
    parser.add_argument("--require-clean", action="store_true")
    parser.add_argument("--run-tests", action="store_true")
    args = parser.parse_args()
    payload = validate(args.mode, args.expected_head, args.require_clean, args.run_tests)
    write(args.receipt, payload)
    print(json.dumps({"mode": args.mode, "checks": payload["check_count"], "json": payload["json"]["parsed"], "privacy_files": payload["privacy"]["files_scanned"], "tests": payload["scoped_tests"].get("tests_run", 0), "issues": payload["issue_count"], "result": payload["result"]}, ensure_ascii=False))
    return 0 if payload["result"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
