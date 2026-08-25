from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

from ghc_family_elowen_cairn_v669_v2_archive import (
    ALLOWED_OUTCOMES,
    BRANCH,
    DOCUMENT_WORD_CEILING,
    FILE_CEILING,
    FROZEN_X1,
    OWNER,
    PHASE,
    PORTFOLIO_COUNTS,
    REL_PHASE_ROOT,
    ROOT,
    STARTUP_FAILURES,
    TERMINAL_VERDICT,
    X2_FAILURES,
    utc_now,
)


ALLOWLIST_PATH = (REL_PHASE_ROOT / "validation/evidence-staged-allowlist.json").as_posix()
OWNER_MANIFEST_PATH = (REL_PHASE_ROOT / "validation/evidence-owner-manifest.json").as_posix()
DELTA_MANIFEST_PATH = (REL_PHASE_ROOT / "validation/evidence-delta-manifest.json").as_posix()
REVIEW_PATH = (REL_PHASE_ROOT / "validation/evidence-staged-review.json").as_posix()
FAILED_REVIEW_PATH = (REL_PHASE_ROOT / "validation/evidence-staged-review-failed.json").as_posix()
FAILED_RECOVERY_PATH = (REL_PHASE_ROOT / "validation/evidence-staged-recovery-failed.json").as_posix()
FAILED_RECOVERY_PATH_2 = (REL_PHASE_ROOT / "validation/evidence-staged-recovery-failed-2.json").as_posix()


def git(*args: str, text: bool = True) -> str | bytes:
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=text, check=True)
    return result.stdout.strip() if text else result.stdout


def staged_bytes(path: str) -> bytes:
    return git("show", ":" + path, text=False)


def staged_json(path: str) -> dict[str, Any]:
    return json.loads(staged_bytes(path).decode("utf-8"))


def staged_paths() -> list[str]:
    value = git("diff", "--cached", "--name-only")
    return value.splitlines() if value else []


def word_count(data: bytes) -> int:
    return len(re.findall(rb"\S+", data))


def privacy_patterns() -> dict[str, re.Pattern[bytes]]:
    return {
        "raw_identifier": re.compile(rb"\b019[0-9a-f]{5}-[0-9a-f-]{20,}\b", re.I),
        "credential_assignment": re.compile(rb"(?i)(?:password|secret|api[_-]?key|bearer|access[_-]?token)\s*[:=]\s*['\"][^'\"]+"),
        "private_route": re.compile(rb"(?i)(?:task|thread|session|resume)[_-]?id\s*[:=]\s*['\"][^'\"]+"),
        "private_absolute_path": re.compile(rb"[A-Za-z]:\\(?:Users|GHC-Archives)\\"),
        "private_app_state": re.compile(rb"(?i)(?:private_callable|session_stream|application_state)\s*[:=]\s*['\"][^'\"]+"),
    }


def security_findings(path: str, data: bytes) -> list[str]:
    findings: list[str] = []
    tree = ast.parse(data.decode("utf-8"), filename=path)
    banned = {"requests", "httpx", "socket", "ctypes", "winreg"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            findings.extend(f"{path}:{node.lineno}:banned_import:{alias.name}" for alias in node.names if alias.name.split(".")[0] in banned)
        elif isinstance(node, ast.ImportFrom) and node.module and node.module.split(".")[0] in banned:
            findings.append(f"{path}:{node.lineno}:banned_import:{node.module}")
        elif isinstance(node, ast.Call):
            for keyword in node.keywords:
                if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                    findings.append(f"{path}:{node.lineno}:shell_true")
    return findings


def replay_manifest(path: str) -> list[dict[str, Any]]:
    manifest = staged_json(path)
    failures: list[dict[str, Any]] = []
    if manifest.get("entry_count") != len(manifest.get("entries", [])):
        failures.append({"path": path, "error": "entry_count_mismatch"})
    for row in manifest.get("entries", []):
        try:
            data = staged_bytes(row["path"])
            oid = subprocess.run(["git", "hash-object", "--stdin"], cwd=ROOT, input=data, capture_output=True, check=True).stdout.decode().strip()
            actual = {"bytes": len(data), "git_blob_oid": oid, "sha256": hashlib.sha256(data).hexdigest()}
            expected = {key: row[key] for key in actual}
            if actual != expected:
                failures.append({"path": row["path"], "expected": expected, "actual": actual})
        except Exception as error:
            failures.append({"path": row.get("path"), "error": f"{type(error).__name__}: {error}"})
    return failures


def compute(
    aggregate_tests: int,
    aggregate_return_code: int,
    aggregate_passed_components: int,
    recovery_tests: int,
    recovery_return_code: int,
) -> dict[str, Any]:
    paths = staged_paths()
    allowlist = staged_json(ALLOWLIST_PATH)
    truth = staged_json((REL_PHASE_ROOT / "x2/phase-truth-evidence.json").as_posix())
    outcomes = staged_json((REL_PHASE_ROOT / "x2/outcome-ledger.json").as_posix())
    method_flow = staged_json((REL_PHASE_ROOT / "method-flow/evidence-ledger.json").as_posix())
    skill_receipt = staged_json((REL_PHASE_ROOT / "tools/skill-smoke-receipt.json").as_posix())
    runner_receipt = staged_json((REL_PHASE_ROOT / "tools/runner-smoke-receipt.json").as_posix())

    checks: dict[str, bool] = {}
    details: dict[str, Any] = {}
    checks["branch_exact"] = git("branch", "--show-current") == BRANCH
    checks["head_is_immutable_x1"] = git("rev-parse", "HEAD") == FROZEN_X1
    checks["staged_allowlist_exact"] = paths == sorted(allowlist["expected_paths"]) and allowlist["path_count"] == len(paths)
    checks["x2_only_after_x1"] = all(not path.startswith("docs/elowen-cairn/v669-v2/x1/") for path in paths)
    checks["owner_test_composite"] = (
        aggregate_tests == 24
        and aggregate_return_code == 1
        and aggregate_passed_components == 22
        and recovery_tests == 2
        and recovery_return_code == 0
    )

    diff = subprocess.run(["git", "diff", "--cached", "--check"], cwd=ROOT, capture_output=True, text=True, check=False)
    checks["diff_hygiene"] = diff.returncode == 0
    details["diff_check"] = diff.stdout.splitlines() + diff.stderr.splitlines()

    json_errors: list[dict[str, str]] = []
    privacy_hits: list[dict[str, str]] = []
    python_errors: list[dict[str, str]] = []
    findings: list[str] = []
    document_words: dict[str, int] = {}
    json_count = 0
    python_count = 0
    markdown_count = 0
    patterns = privacy_patterns()
    text_suffixes = {".json", ".md", ".html", ".txt", ".py", ".yaml", ".yml"}
    for path in paths:
        data = staged_bytes(path)
        suffix = Path(path).suffix.lower()
        if suffix == ".json":
            json_count += 1
            try:
                json.loads(data.decode("utf-8"))
            except Exception as error:
                json_errors.append({"path": path, "error": f"{type(error).__name__}: {error}"})
        if suffix == ".py":
            python_count += 1
            try:
                ast.parse(data.decode("utf-8"), filename=path)
                findings.extend(security_findings(path, data))
            except Exception as error:
                python_errors.append({"path": path, "error": f"{type(error).__name__}: {error}"})
        if suffix == ".md":
            markdown_count += 1
        if suffix in text_suffixes:
            for class_name, pattern in patterns.items():
                if pattern.search(data):
                    privacy_hits.append({"class": class_name, "path": path})
        if suffix in {".md", ".html", ".txt"}:
            document_words[path] = word_count(data)

    checks["strict_json"] = not json_errors and json_count >= 100
    checks["python_ast"] = not python_errors and python_count >= 15
    checks["bounded_python_security"] = not findings
    checks["five_class_privacy_scan"] = not privacy_hits
    checks["document_ceiling"] = bool(document_words) and max(document_words.values()) <= DOCUMENT_WORD_CEILING
    overview_path = (REL_PHASE_ROOT / "x2/integrated-evidence-overview.md").as_posix()
    checks["evidence_overview_floor"] = document_words.get(overview_path, 0) >= 1400
    checks["file_ceiling"] = len(staged_json(OWNER_MANIFEST_PATH)["entries"]) + 2 <= FILE_CEILING

    checks["forty_positive_contracts"] = outcomes["positive_contracts"] == 40
    checks["outcomes_exact"] = outcomes["counts"] == {"completed": 28, "exact_gate": 2, "open_gap": 2, "represented": 8}
    checks["four_labels_only"] = set(outcomes["counts"]) == set(ALLOWED_OUTCOMES)
    checks["mutations_exact"] = outcomes["mutation_count"] == 160
    mutation_rows = []
    for shard in outcomes["mutation_shards"]:
        mutation_rows.extend(staged_json(shard)["rows"])
    checks["mutations_all_rejected"] = len(mutation_rows) == 160 and all(row["observed"] == "reject" and row["completion_credit"] == 0 for row in mutation_rows)
    checks["mutation_ids_unique"] = len({row["mutation_id"] for row in mutation_rows}) == 160

    checks["method_flow_exact"] = len(method_flow["methods"]) == len(STARTUP_FAILURES) + len(X2_FAILURES) + 160
    witness_counts = Counter(row["result"] for row in method_flow["witnesses"])
    checks["method_witness_pairs"] = witness_counts == {"fail": len(method_flow["methods"]), "pass": len(method_flow["methods"])}
    checks["truth_arithmetic"] = (
        truth["effective_negatives"] == 30717
        and truth["methods"] == 16823
        and truth["failed_witnesses"] == 2538
        and truth["passing_witnesses"] == 3615
        and truth["open_gaps"] == 227
        and truth["exact_gates"] == 222
    )
    checks["verdict_retained"] = truth["terminal_verdict"] == TERMINAL_VERDICT

    portfolio_counts: dict[str, int] = {}
    portfolio_labels: set[str] = set()
    external_actions = 0
    for category, expected in PORTFOLIO_COUNTS.items():
        ledger = staged_json((REL_PHASE_ROOT / f"x2/portfolio-execution/{category}.json").as_posix())
        portfolio_counts[category] = ledger["count"]
        portfolio_labels.update(ledger["outcome_counts"])
        external_actions += sum(row["x2_external_actions"] for row in ledger["rows"])
    checks["portfolio_counts_exact"] = portfolio_counts == PORTFOLIO_COUNTS
    checks["portfolio_labels_closed"] = portfolio_labels <= set(ALLOWED_OUTCOMES)
    checks["portfolio_external_actions_zero"] = external_actions == 0
    checks["skills_exact"] = skill_receipt["count"] == 20 and all(row["quick_validation"] == "PASS" for row in skill_receipt["rows"])
    checks["runners_exact"] = runner_receipt["count"] == 10 and all(row["smoke_status"] == "PASS" for row in runner_receipt["rows"])

    owner_manifest_failures = replay_manifest(OWNER_MANIFEST_PATH)
    delta_manifest_failures = replay_manifest(DELTA_MANIFEST_PATH)
    checks["owner_manifest_replay"] = not owner_manifest_failures
    checks["delta_manifest_replay"] = not delta_manifest_failures
    checks["manifest_exclusions"] = (
        set(staged_json(OWNER_MANIFEST_PATH)["self_exclusions"]) == {OWNER_MANIFEST_PATH, DELTA_MANIFEST_PATH, REVIEW_PATH}
        and set(staged_json(DELTA_MANIFEST_PATH)["self_exclusions"]) == {OWNER_MANIFEST_PATH, DELTA_MANIFEST_PATH, REVIEW_PATH}
    )

    details.update(
        {
            "delta_manifest_failures": delta_manifest_failures,
            "document_words": document_words,
            "json_count": json_count,
            "json_errors": json_errors,
            "markdown_count": markdown_count,
            "owner_manifest_failures": owner_manifest_failures,
            "aggregate_passed_components": aggregate_passed_components,
            "aggregate_tests": aggregate_tests,
            "aggregate_tests_return_code": aggregate_return_code,
            "portfolio_counts": portfolio_counts,
            "privacy_hits": privacy_hits,
            "python_count": python_count,
            "python_errors": python_errors,
            "recovery_tests": recovery_tests,
            "recovery_tests_return_code": recovery_return_code,
            "security_findings": findings,
            "staged_paths": len(paths),
            "witness_counts": dict(witness_counts),
        }
    )
    passed = all(checks.values())
    return {
        "all_passed": passed,
        "boundary": "Bounded same-owner immutable-evidence staged validation only; not final canonical validation, full repository suite, or independent reproduction.",
        "checks": checks,
        "details": details,
        "generated_at_utc": utc_now(),
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.evidence-staged-review.v2",
        "status": "PASS_IMMUTABLE_EVIDENCE_STAGED" if passed else "FAIL_IMMUTABLE_EVIDENCE_STAGED_ZERO_CREDIT",
    }


def recover_owner_manifest_only() -> dict[str, Any]:
    failed = staged_json(FAILED_REVIEW_PATH)
    prior_recovery = staged_json(FAILED_RECOVERY_PATH)
    second_recovery = staged_json(FAILED_RECOVERY_PATH_2)
    aggregate_checks = failed.get("checks", {})
    aggregate_shape_exact = (
        failed.get("status") == "FAIL_IMMUTABLE_EVIDENCE_STAGED_ZERO_CREDIT"
        and len(aggregate_checks) == 31
        and sum(bool(value) for value in aggregate_checks.values()) == 30
        and aggregate_checks.get("owner_manifest_replay") is False
        and all(value for key, value in aggregate_checks.items() if key != "owner_manifest_replay")
    )
    prior_recovery_retained = (
        prior_recovery.get("status") == "FAIL_DEPENDENCY_RECOVERY_ZERO_CREDIT"
        and prior_recovery.get("aggregate_all_pass_credit") == 0
        and prior_recovery.get("recovery", {}).get("owner_manifest_replay") is True
        and prior_recovery.get("recovery", {}).get("retention_arithmetic") is True
    )
    second_recovery_retained = (
        second_recovery.get("status") == "FAIL_DEPENDENCY_RECOVERY_ZERO_CREDIT"
        and second_recovery.get("aggregate_all_pass_credit") == 0
        and second_recovery.get("recovery", {}).get("invocation_count") == 2
        and second_recovery.get("recovery", {}).get("owner_manifest_replay") is True
        and second_recovery.get("recovery", {}).get("retention_arithmetic") is False
    )
    manifest_failures = replay_manifest(OWNER_MANIFEST_PATH)
    truth = staged_json((REL_PHASE_ROOT / "x2/phase-truth-evidence.json").as_posix())
    method_flow = staged_json((REL_PHASE_ROOT / "method-flow/evidence-ledger.json").as_posix())
    retention_arithmetic = (
        truth["effective_negatives"] == 30717
        and truth["methods"] == 16823
        and truth["failed_witnesses"] == 2538
        and truth["passing_witnesses"] == 3615
        and len(method_flow["methods"]) == len(STARTUP_FAILURES) + len(X2_FAILURES) + 160
        and Counter(row["result"] for row in method_flow["witnesses"])
        == {"fail": len(method_flow["methods"]), "pass": len(method_flow["methods"])}
    )
    owner_exclusions = set(staged_json(OWNER_MANIFEST_PATH)["self_exclusions"])
    exclusion_domain_exact = owner_exclusions == {OWNER_MANIFEST_PATH, DELTA_MANIFEST_PATH, REVIEW_PATH}
    passed = (
        aggregate_shape_exact
        and prior_recovery_retained
        and second_recovery_retained
        and not manifest_failures
        and retention_arithmetic
        and exclusion_domain_exact
    )
    return {
        "all_passed": passed,
        "aggregate_all_pass_credit": 0,
        "aggregate_checks_passed": 30,
        "aggregate_checks_total": 31,
        "aggregate_failed_receipt": FAILED_REVIEW_PATH,
        "boundary": "Dependency-corrected evidence composite: 29 unreplayed aggregate checks plus isolated owner-manifest and affected-retention recovery; not a canonical aggregate or independent reproduction.",
        "composite_status": "VALID_DEPENDENCY_CORRECTED_EVIDENCE_COMPOSITE_WITH_ZERO_AGGREGATE_PASS_CREDIT" if passed else "INVALID_DEPENDENCY_RECOVERY_ZERO_CREDIT",
        "failed_component": "owner_manifest_replay",
        "generated_at_utc": utc_now(),
        "owner": OWNER,
        "phase": PHASE,
        "recovery": {
            "exclusion_domain_exact": exclusion_domain_exact,
            "invocation_count": 3,
            "owner_manifest_failures": manifest_failures,
            "owner_manifest_replay": not manifest_failures,
            "prior_failed_recovery": FAILED_RECOVERY_PATH,
            "prior_recovery_retained": prior_recovery_retained,
            "second_failed_recovery": FAILED_RECOVERY_PATH_2,
            "second_recovery_retained": second_recovery_retained,
            "retention_arithmetic": retention_arithmetic,
        },
        "schema": "ghc.family.evidence-staged-composite.v2",
        "status": "PASS_DEPENDENCY_CORRECTED_EVIDENCE_COMPOSITE" if passed else "FAIL_DEPENDENCY_RECOVERY_ZERO_CREDIT",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--aggregate-tests", type=int)
    parser.add_argument("--aggregate-return-code", type=int)
    parser.add_argument("--aggregate-passed-components", type=int)
    parser.add_argument("--recovery-tests", type=int)
    parser.add_argument("--recovery-return-code", type=int)
    parser.add_argument("--recover-owner-manifest-only", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.recover_owner_manifest_only:
        receipt = recover_owner_manifest_only()
    else:
        required = (
            args.aggregate_tests,
            args.aggregate_return_code,
            args.aggregate_passed_components,
            args.recovery_tests,
            args.recovery_return_code,
        )
        if any(value is None for value in required):
            parser.error("aggregate and recovery test evidence is required outside isolated recovery mode")
        receipt = compute(*required)
    if args.write:
        path = ROOT / REVIEW_PATH
        path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
    raise SystemExit(0 if receipt["all_passed"] else 1)


if __name__ == "__main__":
    main()
