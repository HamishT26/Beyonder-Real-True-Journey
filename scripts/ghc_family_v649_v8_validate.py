#!/usr/bin/env python3
"""Single-pass scoped canonical validator for Elaren Kestrel v649-v8."""

from __future__ import annotations

import argparse
import io
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "elaren-kestrel" / "v649-v8"
SOURCE = "68f54882fa665f75cb181d9a9a64853802db5554"
X1 = "4664cdb728f0b9c2b11f478b35c1deb2e893f34f"
BRANCH = "codex/GHC-Family/elaren-kestrel-v649-v8-full-tools"


def git(*args: str, check: bool = True, timeout: int = 180) -> str:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, check=check, capture_output=True, timeout=timeout,
        text=True, encoding="utf-8", errors="replace",
    )
    return result.stdout.strip()


def load(relative: str) -> dict[str, Any]:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def record(checks: list[dict[str, Any]], name: str, passed: bool, observed: Any = None) -> None:
    checks.append({"name": name, "passed": bool(passed), "observed": observed})


def run_tests(include_closeout: bool) -> dict[str, Any]:
    modules = [
        "tests.test_ghc_family_v649_v7",
        "tests.test_ghc_family_v649_v8_x1",
        "tests.test_ghc_family_v649_v8_x2",
    ]
    if include_closeout:
        modules.append("tests.test_ghc_family_v649_v8_closeout")
    suite = unittest.TestSuite()
    loader = unittest.defaultTestLoader
    for module in modules:
        suite.addTests(loader.loadTestsFromName(module))
    result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)
    return {
        "modules": modules,
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "failed_test_ids": sorted(test.id() for test, _trace in result.failures),
        "error_test_ids": sorted(test.id() for test, _trace in result.errors),
        "passed": result.wasSuccessful(),
    }


def detailed_checks() -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    truth = load("phase-truth-evidence.json")
    outcomes = load("x2/core-outcome-ledger.json")
    negatives = load("x2/retained-negative-register.json")
    gates = load("x2/gate-register.json")
    record(checks, "proposal_count", outcomes["proposal_count"] == 20, outcomes["proposal_count"])
    record(checks, "outcome_distribution", outcomes["distribution"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}, outcomes["distribution"])
    record(checks, "effective_negatives_match_truth", negatives["effective_at_evidence"] == truth["effective_negatives"], negatives["effective_at_evidence"])
    record(checks, "negative_erased_false", negatives["negative_erased"] is False)
    record(checks, "open_gaps", gates["effective_open_gaps"] == 42, gates["effective_open_gaps"])
    record(checks, "exact_gates", gates["effective_exact_gates"] == 43, gates["effective_exact_gates"])
    record(checks, "nothing_silently_closed", gates["silently_closed"] == 0)
    record(checks, "terminal_verdict", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20")
    record(checks, "no_full_suite", truth["full_repository_suite"] is False)
    record(checks, "no_replay", truth["replay_used"] is False)
    for row in outcomes["outcomes"]:
        root = PHASE / row["artifact_root"]
        contract = json.loads((root / "contract.json").read_text(encoding="utf-8"))
        mutation = json.loads((root / "mutation-results.json").read_text(encoding="utf-8"))
        receipt = json.loads((root / "bounded-receipt.json").read_text(encoding="utf-8"))
        prefix = row["proposal_id"]
        record(checks, f"{prefix}_contract_bounded", contract["bounded"] is True)
        record(checks, f"{prefix}_no_production", contract["production"] is False)
        record(checks, f"{prefix}_no_authority", contract["authority_credit"] is False)
        record(checks, f"{prefix}_no_stage20", contract["stage20"] is False)
        record(checks, f"{prefix}_no_real_rows", contract["real_rows"] == 0)
        record(checks, f"{prefix}_no_real_people", contract["real_people"] == 0)
        record(checks, f"{prefix}_five_mutations", mutation["count"] == 5)
        record(checks, f"{prefix}_five_rejected", mutation["rejected_count"] == 5)
        for item in mutation["mutations"]:
            record(checks, f"{item['mutation_id']}_rejected", item["rejected"] is True)
            record(checks, f"{item['mutation_id']}_retained", item["negative_retained"] is True)
        record(checks, f"{prefix}_receipt_label", receipt["outcome"] == row["outcome"])
        record(checks, f"{prefix}_same_owner_only", receipt["same_owner_only"] is True and receipt["independent_reproduction"] is False)
    portfolio_specs = [
        ("x2/safe-now-results.json", 40),
        ("x2/candidate-results.json", 30),
        ("x2/skill-use-ledger.json", 20),
        ("x2/runner-use-ledger.json", 10),
        ("x2/clean-fix-refine-results.json", 40),
    ]
    for path, count in portfolio_specs:
        payload = load(path)
        record(checks, f"{path}_completed", payload["completed_count"] == count, payload["completed_count"])
        record(checks, f"{path}_pending_zero", payload.get("pending_count", 0) == 0)
    skills = load("x2/skill-use-ledger.json")
    for row in skills["skills"]:
        record(checks, f"{row['skill_id']}_validated", row["quick_validate_returncode"] == 0)
        record(checks, f"{row['skill_id']}_smoke", row["smoke_used"] is True)
    runners = load("x2/runner-use-ledger.json")
    for row in runners["runners"]:
        record(checks, f"{row['runner_id']}_pass", row["passing_fixture"] is True)
        record(checks, f"{row['runner_id']}_reject", row["rejecting_fixture"] is True)
        record(checks, f"{row['runner_id']}_secondary", row["secondary_library_use"] is True)
    methods = load("method-flow/method-flow-summary-x2.json")
    record(checks, "method_count", methods["counts"]["methods"] >= 10, methods["counts"]["methods"])
    record(checks, "method_witness_parity", methods["counts"]["witness_results"]["fail"] == methods["counts"]["witness_results"]["pass"], methods["counts"]["witness_results"])
    documents = load("validation/document-cap-receipt.json")
    record(checks, "document_cap", documents["all_under_20000"] is True, documents["maximum_words"])
    record(checks, "overview_length", documents["overview_three_page_equivalent"] is True, documents["overview_words"])
    owner_files = load("validation/owner-file-threshold-receipt.json")
    record(checks, "owner_file_cap", owner_files["below_threshold"] is True, owner_files["owner_file_count"])
    return checks


def minimal_checks() -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    truth = load("phase-truth-evidence.json")
    expected = {
        "owner": "Elaren Kestrel",
        "proposal_count": 20,
        "outcomes": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "effective_open_gaps": 42,
        "effective_exact_gates": 43,
        "skills_completed": 20,
        "runners_completed": 10,
        "safe_completed": 40,
        "candidates_completed": 30,
        "clean_refine_completed": 40,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    for key, value in expected.items():
        record(checks, f"truth_{key}", truth[key] == value, truth[key])
    record(checks, "full_suite_false", truth["full_repository_suite"] is False)
    record(checks, "replay_false", truth["replay_used"] is False)
    record(checks, "route_prepared", load("orchestration/phase-state-evidence.json")["terminal_route"] == "PREPARED_NOT_SENT")
    record(checks, "subagents_zero", load("orchestration/phase-state-evidence.json")["subagents"] == 0)
    record(checks, "mutations_100", load("x2/synthetic-mutation-results.json")["rejected_count"] == 100)
    record(checks, "privacy_precommit_zero", load("validation/evidence-staged-privacy.json")["confirmed_hit_count"] == 0)
    record(checks, "x1_frozen", load("validation/evidence-staged-review.json")["x1_frozen_changes"] == [])
    record(checks, "static_report", (PHASE / "deliverables" / "v649-v8-bounded-evidence-report.html").is_file())
    record(checks, "overview", (PHASE / "deliverables" / "v649-v8-integrated-overview.md").is_file())
    record(checks, "same_owner_not_independent", all(row["same_owner_only"] and not row["independent_reproduction"] for row in [json.loads((PHASE / item["artifact_root"] / "bounded-receipt.json").read_text(encoding="utf-8")) for item in load("x2/core-outcome-ledger.json")["outcomes"]]))
    record(checks, "identity_boundary", "not evidence of consciousness" in load("identity-receipt.json")["boundary"])
    record(checks, "no_external_messages", load("orchestration/phase-state-evidence.json")["cross_platform_messages"] == 0)
    record(checks, "source_nonconversion", load("sources/source-execution-ledger.json")["citation_converted_to_data"] is False)
    return checks


PRIVACY = {
    "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
    "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
    "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
    "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
    "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
}


def privacy_scan() -> dict[str, Any]:
    files = [path for path in PHASE.rglob("*") if path.is_file()]
    files.extend(ROOT / path for path in git("ls-files", "scripts/*v649_v8*.py", "tests/test_ghc_family_v649_v8*.py").splitlines())
    definitions = {ROOT / "scripts" / "ghc_family_v649_v8_x1.py", ROOT / "scripts" / "ghc_family_v649_v8_x2.py", ROOT / "scripts" / "ghc_family_v649_v8_validate.py"}
    definitions.update(PHASE / "validation" / name for name in ("x1-staged-privacy.json", "evidence-staged-privacy.json", "final-staged-privacy.json"))
    hits: list[dict[str, str]] = []
    scanned = 0
    for path in sorted(set(files)):
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        scanned += 1
        if path in definitions:
            continue
        for name, pattern in PRIVACY.items():
            if pattern.search(text):
                hits.append({"path": path.relative_to(ROOT).as_posix(), "pattern_class": name})
    return {"scanned_file_count": scanned, "pattern_class_count": len(PRIVACY), "confirmed_hits": hits, "confirmed_hit_count": len(hits)}


def manifest_check() -> dict[str, Any]:
    relative = "validation/final-owner-manifest.json" if (PHASE / "validation/final-owner-manifest.json").is_file() else "validation/evidence-staged-manifest.json"
    payload = load(relative)
    mismatches = []
    for row in payload["entries"]:
        repository_path = row.get("repository_path", row["path"])
        if not repository_path.startswith("docs/") and relative.endswith("final-owner-manifest.json"):
            repository_path = f"docs/elaren-kestrel/v649-v8/{repository_path}"
        actual = git("rev-parse", f"HEAD:{repository_path}", check=False)
        if actual != row["git_blob"]:
            mismatches.append(repository_path)
    return {"manifest": relative, "entry_count": payload["entry_count"], "mismatches": mismatches, "passed": not mismatches}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--require-clean", action="store_true")
    parser.add_argument("--canonical-pass", action="store_true")
    args = parser.parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    clean_before = not git("status", "--porcelain=v1")
    tests = run_tests((PHASE / "closeout-receipt.json").is_file())
    detailed = detailed_checks()
    minimal = minimal_checks()
    json_errors: list[str] = []
    json_count = 0
    for path in sorted(PHASE.rglob("*.json")):
        try:
            json.loads(path.read_text(encoding="utf-8"))
            json_count += 1
        except Exception:
            json_errors.append(path.relative_to(PHASE).as_posix())
    privacy = privacy_scan()
    manifest = manifest_check()
    local = git("rev-parse", "HEAD")
    upstream = git("rev-parse", "@{upstream}")
    tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_row = git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")
    live = live_row.split("\t", 1)[0] if live_row else ""
    anchors = {anchor: subprocess.run(["git", "merge-base", "--is-ancestor", anchor, "HEAD"], cwd=ROOT).returncode == 0 for anchor in (SOURCE, X1)}
    merge_count = int(git("rev-list", "--count", "--merges", f"{SOURCE}..HEAD"))
    commit_count = int(git("rev-list", "--count", f"{SOURCE}..HEAD"))
    parent_count = len(git("rev-list", "--parents", "-n", "1", "HEAD").split()) - 1
    clean_after = not git("status", "--porcelain=v1")
    valid = all([
        tests["passed"], all(row["passed"] for row in detailed), all(row["passed"] for row in minimal),
        not json_errors, privacy["confirmed_hit_count"] == 0, manifest["passed"],
        local == args.expected_head, local == upstream == tracking == live,
        all(anchors.values()), merge_count == 0, commit_count <= 4, parent_count == 1,
        (not args.require_clean or (clean_before and clean_after)),
    ])
    payload = {
        "schema": "ghc.family.v649-v8.single-pass-canonical-validation.v1",
        "canonical_pass": args.canonical_pass, "successful_pass_count": 1 if valid and args.canonical_pass else 0,
        "post_success_replay": False, "valid": valid, "expected_head": args.expected_head,
        "head": local, "tests": tests,
        "detailed_check_count": len(detailed), "detailed_failures": [row for row in detailed if not row["passed"]],
        "minimal_check_count": len(minimal), "minimal_failures": [row for row in minimal if not row["passed"]],
        "json_parse_count": json_count, "json_errors": json_errors, "privacy": privacy, "manifest": manifest,
        "local_upstream_tracking_live_equal": local == upstream == tracking == live,
        "anchors": anchors, "source_to_head_commit_count": commit_count, "merge_count": merge_count,
        "parent_count": parent_count, "clean_before": clean_before, "clean_after": clean_after,
        "full_repository_suite_run": False, "same_owner_only": True, "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({
        "valid": valid, "tests": tests["tests_run"], "detailed": len(detailed), "minimal": len(minimal),
        "json": json_count, "privacy_files": privacy["scanned_file_count"], "manifest": manifest["entry_count"],
        "commits": commit_count, "merges": merge_count,
    }, sort_keys=True))
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
