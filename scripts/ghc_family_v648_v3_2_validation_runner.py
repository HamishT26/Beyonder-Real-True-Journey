#!/usr/bin/env python3
"""Single-pass bounded canonical validator for Eiren Kestrel v648-v3 repeat.

This runner deliberately executes the authorized unittest selection once.  The
remaining gates are structural reads over the same canonical worktree; there is
no detached or named replay and no full-repository-suite invocation.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/eiren-kestrel/v648-v3-2"
SOURCE = "f3a90b0280ff8f3504353da3b6a37ef0540e3296"
X1 = "723753e1a88427e1f8cd6ee572e3479c721dce84"
EVIDENCE = "e619a0221dc4a82aeb80ce783385a694e1d93657"
SELECTION = [
    "tests.test_ghc_family_v648_v2",
    "tests.test_ghc_family_v648_v3",
    "tests.test_ghc_family_v648_v3_2",
]
PATTERNS = {
    "raw_task_or_thread_id": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
    "private_absolute_path": re.compile(r"(?:[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b|/(?:Users|home)/)", re.I),
    "credential_or_private_key": re.compile(r"\b(?:sk-[A-Za-z0-9_-]{20,}|gh[opusr]_[A-Za-z0-9]{20,}|BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY)\b"),
    "private_session_or_route": re.compile(r"(?:source_thread_id|rollout_path|session_meta\.payload\.id|(?:thread|app|plugin)://)", re.I),
    "private_callable_identifier": re.compile(r"(?:mcp__|codex_app__send_message_to_thread)", re.I),
}
MINIMAL_NAMES = {
    "required evidence files",
    "exact source head",
    "source ancestry",
    "x1 ancestry",
    "zero merges",
    "ten frozen proposals",
    "590 proposal chain",
    "exact outcome distribution",
    "70 mutations rejected",
    "safe portfolio complete",
    "candidate portfolio complete",
    "skill portfolio complete",
    "runner portfolio complete",
    "cleanup terminal reservation",
    "negative arithmetic",
    "gate counts",
    "zero real evidence rows",
    "not ready verdict",
    "no replay credit",
    "route prepared not sent",
}


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=check,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def add(checks: list[dict[str, Any]], name: str, condition: bool, observed: Any) -> None:
    checks.append({"name": name, "pass": bool(condition), "observed": observed})


def committed_bytes(path: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(ROOT), "show", f"{EVIDENCE}:{path}"],
        check=True,
        capture_output=True,
    ).stdout


def run_tests_once() -> dict[str, Any]:
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    suite = unittest.defaultTestLoader.loadTestsFromNames(SELECTION)
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=1).run(suite)
    failures = [case.id() for case, _ in result.failures]
    errors = [case.id() for case, _ in result.errors]
    return {
        "run_count": 1,
        "selection": SELECTION,
        "tests_run": result.testsRun,
        "failures": failures,
        "errors": errors,
        "skipped": len(result.skipped),
        "successful": result.wasSuccessful(),
        "sanitized_output_tail": stream.getvalue()[-12000:],
    }


def validate() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    required = [
        "x1-proposals.json",
        "x2-proposal-ledger.json",
        "retained-negative-register-x2.json",
        "exact-open-gate-register-x2.json",
        "phase-truth-x2.json",
        "threat-model.json",
        "maintenance/x2-clean-refine-ledger.json",
        "tooling/x2-runner-ledger.json",
        "tooling/x2-skill-ledger.json",
        "method-flow/method-flow-ledger.json",
        "validation/evidence-staged-manifest.json",
        "validation/evidence-staged-review.json",
        "deliverables/v648-v3-r2-integrated-overview.md",
        "deliverables/v648-v3-r2-static-report.html",
    ]
    missing = [relative for relative in required if not (PHASE / relative).is_file()]
    add(checks, "required evidence files", not missing, missing)
    if missing:
        return {"valid": False, "checks": checks, "test_result": {"run_count": 0}}

    head = git("rev-parse", "HEAD").stdout.strip()
    add(checks, "exact source head", head == EVIDENCE, head)
    source_ancestor = git("merge-base", "--is-ancestor", SOURCE, "HEAD", check=False).returncode == 0
    x1_ancestor = git("merge-base", "--is-ancestor", X1, "HEAD", check=False).returncode == 0
    merges = int(git("rev-list", "--count", "--merges", f"{SOURCE}..HEAD").stdout.strip())
    add(checks, "source ancestry", source_ancestor, source_ancestor)
    add(checks, "x1 ancestry", x1_ancestor, x1_ancestor)
    add(checks, "zero merges", merges == 0, merges)

    x1 = load("x1-proposals.json")
    x2 = load("x2-proposal-ledger.json")
    mutations = load("validation/preregistered-synthetic-negatives.json")
    safe = load("approval-packets/x2-safe-now-ledger.json")
    candidates = load("prototypes/x2-candidate-ledger.json")
    skills = load("tooling/x2-skill-ledger.json")
    runners = load("tooling/x2-runner-ledger.json")
    cleanup = load("maintenance/x2-clean-refine-ledger.json")
    negatives = load("retained-negative-register-x2.json")
    gates = load("exact-open-gate-register-x2.json")
    truth = load("phase-truth-x2.json")
    threat = load("threat-model.json")
    methods = load("method-flow/method-flow-ledger.json")

    outcome_counts = Counter(row["observed_outcome"] for row in x2["proposals"])
    add(checks, "ten frozen proposals", len(x1["proposals"]) == 10, len(x1["proposals"]))
    add(checks, "590 proposal chain", x1["frozen_chain_count_after_x1"] == 590, x1["frozen_chain_count_after_x1"])
    add(checks, "ten executed proposals", len(x2["proposals"]) == 10, len(x2["proposals"]))
    add(checks, "exact outcome distribution", outcome_counts == Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}), dict(outcome_counts))
    add(checks, "70 mutations rejected", (mutations["count"], mutations["retained_count"], mutations["all_rejected"]) == (70, 70, True), [mutations["count"], mutations["retained_count"], mutations["all_rejected"]])
    add(checks, "safe portfolio complete", safe["completed_count"] == 15, safe["completed_count"])
    add(checks, "candidate portfolio complete", candidates["completed_count"] == 20, candidates["completed_count"])
    add(checks, "skill portfolio complete", (skills["skill_count"], skills["all_initialized"], skills["all_structure_valid"], skills["all_used"]) == (20, True, True, True), [skills["skill_count"], skills["all_initialized"], skills["all_structure_valid"], skills["all_used"]])
    add(checks, "runner portfolio complete", (runners["runner_count"], runners["invoked_count"]) == (10, 10), [runners["runner_count"], runners["invoked_count"]])
    add(checks, "cleanup terminal reservation", (cleanup["completed_count"], cleanup["pending_final_count"]) == (28, 2), [cleanup["completed_count"], cleanup["pending_final_count"]])
    expected_negative = negatives["inherited_effective"] + negatives["x1_operational"] + negatives["x2_operational"] + negatives["synthetic_rejected"]
    add(checks, "negative arithmetic", negatives["effective_total"] == expected_negative == 4211 and negatives["erased_negative_count"] == 0, [negatives["effective_total"], expected_negative])
    add(checks, "gate counts", (gates["effective_open_gaps"], gates["effective_exact_gates"]) == (29, 30), [gates["effective_open_gaps"], gates["effective_exact_gates"]])
    add(checks, "method flow retained", (methods["counts"]["methods"], methods["counts"]["witness_results"]) == (12, {"fail": 13, "pass": 13}), [methods["counts"]["methods"], methods["counts"]["witness_results"]])
    add(checks, "zero real evidence rows", (truth["real_data_rows"], truth["real_people_or_operations"], truth["real_keys_or_tokens"], truth["authority_decisions"]) == (0, 0, 0, 0), [truth["real_data_rows"], truth["real_people_or_operations"], truth["real_keys_or_tokens"], truth["authority_decisions"]])
    add(checks, "not ready verdict", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", truth["terminal_verdict"])
    add(checks, "no replay credit", (truth["replay_runs"], truth["repeatability_credit"], truth["independent_reproduction"]) == (0, 0, False), [truth["replay_runs"], truth["repeatability_credit"], truth["independent_reproduction"]])
    add(checks, "route prepared not sent", truth["route_state"] == "PREPARED_NOT_SENT", truth["route_state"])
    add(checks, "sandbox deferred without probe", threat["sandbox_and_hyper_v"] == "deferred_by_user_no_probe_or_activation", threat["sandbox_and_hyper_v"])
    add(checks, "cross platform messaging deferred", threat["cross_platform_chatgpt_messaging"] == "deferred_by_user_no_send_attempt", threat["cross_platform_chatgpt_messaging"])

    json_errors: list[dict[str, str]] = []
    json_files = sorted(PHASE.rglob("*.json"))
    for path in json_files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError, UnicodeDecodeError) as exc:
            json_errors.append({"path": path.relative_to(PHASE).as_posix(), "error": type(exc).__name__})
    add(checks, "all phase JSON parses", not json_errors, {"count": len(json_files), "errors": json_errors})

    privacy_hits: list[dict[str, str]] = []
    word_violations: list[dict[str, Any]] = []
    public_files = [path for path in sorted(PHASE.rglob("*")) if path.is_file()]
    for path in public_files:
        text = path.read_text(encoding="utf-8")
        for class_name, pattern in PATTERNS.items():
            if pattern.search(text):
                privacy_hits.append({"path": path.relative_to(PHASE).as_posix(), "class": class_name})
        if path.suffix.casefold() in {".md", ".html", ".txt"}:
            words = len(re.findall(r"\b\w+\b", text, re.UNICODE))
            if words > 6000:
                word_violations.append({"path": path.relative_to(PHASE).as_posix(), "words": words})
    add(checks, "five class privacy scan", not privacy_hits, privacy_hits)
    add(checks, "document word caps", not word_violations, word_violations)

    manifest = load("validation/evidence-staged-manifest.json")
    mismatches: list[str] = []
    for row in manifest["entries"]:
        observed = hashlib.sha256(committed_bytes(row["path"])).hexdigest()
        if observed != row["sha256"]:
            mismatches.append(row["path"])
    add(checks, "evidence committed manifest parity", not mismatches and manifest["entry_count"] == len(manifest["entries"]), {"entries": manifest["entry_count"], "mismatches": mismatches})

    test_result = run_tests_once()
    add(checks, "authorized scoped tests", test_result["successful"] and test_result["tests_run"] > 0, {"tests": test_result["tests_run"], "failures": test_result["failures"], "errors": test_result["errors"]})

    minimal = [row for row in checks if row["name"] in MINIMAL_NAMES]
    missing_minimal = sorted(MINIMAL_NAMES - {row["name"] for row in minimal})
    detailed_valid = all(row["pass"] for row in checks)
    minimal_valid = not missing_minimal and len(minimal) == 20 and all(row["pass"] for row in minimal)
    return {
        "schema": "ghc.family.v648-v3-r2.single-pass-canonical-validation.v1",
        "valid": detailed_valid and minimal_valid,
        "canonical_validation_runs": 1,
        "full_repository_suite_run": False,
        "named_replay_runs": 0,
        "detached_replay_runs": 0,
        "repeatability_credit": 0,
        "independent_reproduction": False,
        "head": head,
        "detailed_check_count": len(checks),
        "detailed_checks_passed": sum(row["pass"] for row in checks),
        "minimal_check_count": len(minimal),
        "minimal_checks_passed": sum(row["pass"] for row in minimal),
        "minimal_missing": missing_minimal,
        "json_parse_count": len(json_files),
        "privacy_file_count": len(public_files),
        "privacy_pattern_classes": sorted(PATTERNS),
        "privacy_confirmed_hits": privacy_hits,
        "document_word_cap_violations": word_violations,
        "manifest_entry_count": manifest["entry_count"],
        "test_result": test_result,
        "checks": checks,
        "boundary": "One canonical same-owner validation only. This is not a full repository suite, replay, independent reproduction, external audit, production certification, complete privacy, exhaustive security, complete accessibility, or authority evidence.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    result = validate()
    write(args.receipt, result)
    print(json.dumps({
        "valid": result["valid"],
        "tests": result["test_result"]["tests_run"],
        "detailed": [result["detailed_checks_passed"], result["detailed_check_count"]],
        "minimal": [result["minimal_checks_passed"], result["minimal_check_count"]],
        "json": result["json_parse_count"],
        "privacy_files": result["privacy_file_count"],
        "manifest": result["manifest_entry_count"],
    }, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
