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
    ACTIVATION_OVERLAY,
    ALLOWED_OUTCOMES,
    BRANCH,
    DOCUMENT_WORD_CEILING,
    FILE_CEILING,
    INHERITED_FROZEN_PROPOSALS,
    OWNER,
    PHASE,
    PORTFOLIO_COUNTS,
    REL_PHASE_ROOT,
    ROOT,
    SOURCE_FINAL,
    STARTUP_FAILURES,
    TERMINAL_VERDICT,
    utc_now,
)


REVIEW_PATH = (REL_PHASE_ROOT / "validation/x1-staged-review.json").as_posix()
MANIFEST_PATH = (REL_PHASE_ROOT / "validation/x1-manifest.json").as_posix()
ALLOWLIST_PATH = (REL_PHASE_ROOT / "validation/x1-staged-allowlist.json").as_posix()
TEXT_SUFFIXES = {".json", ".md", ".html", ".yaml", ".yml", ".py", ".txt"}


def run_git(*args: str, check: bool = True, text: bool = True) -> subprocess.CompletedProcess[Any]:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=check,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=text,
    )


def git(*args: str) -> str:
    return run_git(*args).stdout.strip()


def staged_bytes(path: str) -> bytes:
    return run_git("show", f":{path}", text=False).stdout


def staged_oid(path: str) -> str:
    return git("rev-parse", f":{path}")


def staged_json(path: str) -> Any:
    return json.loads(staged_bytes(path))


def word_count(data: bytes) -> int:
    return len(re.findall(rb"\S+", data))


def privacy_patterns() -> dict[str, re.Pattern[str]]:
    return {
        "credential_assignment": re.compile(r"(?i)(?:password|secret|api[_-]?key|bearer|access[_-]?token)\s*[:=]\s*['\"][^'\"]+"),
        "email_address": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
        "private_absolute_path": re.compile(r"(?i)\b[A-Z]:\\(?:Users|Documents and Settings)\\[^\\\s]+"),
        "private_route_identifier": re.compile(r"(?i)(?:source_" + r"thread_id|private_" + r"callable_identifier|codex" + r"Delegation|resume_" + r"value)"),
        "raw_uuid": re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}\b"),
    }


def changed_python_security_findings(path: str, data: bytes) -> list[str]:
    findings: list[str] = []
    tree = ast.parse(data.decode("utf-8"), filename=path)
    banned_imports = {"requests", "urllib3", "httpx", "socket", "winreg"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] in banned_imports:
                    findings.append(f"{path}:{node.lineno}:banned_import:{alias.name}")
        elif isinstance(node, ast.ImportFrom) and node.module:
            if node.module.split(".")[0] in banned_imports:
                findings.append(f"{path}:{node.lineno}:banned_import:{node.module}")
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                pair = (node.func.value.id, node.func.attr)
                if pair in {("os", "system"), ("os", "popen")}:
                    findings.append(f"{path}:{node.lineno}:unsafe_process_call")
            for keyword in node.keywords:
                if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                    findings.append(f"{path}:{node.lineno}:shell_true")
    return findings


def compute(owner_tests: int, owner_tests_return_code: int) -> dict[str, Any]:
    staged_paths = [line for line in git("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if line]
    allowlist = staged_json(ALLOWLIST_PATH)
    expected_paths = allowlist["expected_paths"]
    checks: dict[str, bool] = {}
    details: dict[str, Any] = {}

    checks["branch_exact"] = git("branch", "--show-current") == BRANCH
    checks["head_is_source_before_x1_commit"] = git("rev-parse", "HEAD") == SOURCE_FINAL
    checks["staged_allowlist_exact"] = staged_paths == expected_paths
    checks["x1_only_paths"] = all(
        path.startswith("docs/elowen-cairn/v669-v2/x1/")
        or path.startswith("docs/elowen-cairn/v669-v2/method-flow/x1-")
        or path.startswith("docs/elowen-cairn/v669-v2/validation/x1-")
        or "elowen_cairn_v669_v2" in path
        for path in staged_paths
    )
    diff_check = run_git("diff", "--cached", "--check", check=False)
    checks["diff_hygiene"] = diff_check.returncode == 0
    details["diff_check_stderr"] = diff_check.stderr.splitlines()[-10:]

    json_paths = [path for path in staged_paths if Path(path).suffix == ".json"]
    python_paths = [path for path in staged_paths if Path(path).suffix == ".py"]
    markdown_paths = [path for path in staged_paths if Path(path).suffix == ".md"]
    parsed_json: dict[str, Any] = {}
    json_errors: list[dict[str, str]] = []
    for path in json_paths:
        try:
            parsed_json[path] = staged_json(path)
        except Exception as error:
            json_errors.append({"path": path, "error": f"{type(error).__name__}: {error}"})
    checks["strict_json"] = not json_errors
    details["json_errors"] = json_errors

    python_errors: list[dict[str, str]] = []
    security_findings: list[str] = []
    for path in python_paths:
        data = staged_bytes(path)
        try:
            ast.parse(data.decode("utf-8"), filename=path)
            security_findings.extend(changed_python_security_findings(path, data))
        except Exception as error:
            python_errors.append({"path": path, "error": f"{type(error).__name__}: {error}"})
    checks["python_ast"] = not python_errors
    checks["bounded_python_security"] = not security_findings
    details["python_errors"] = python_errors
    details["security_findings"] = security_findings

    patterns = privacy_patterns()
    privacy_candidates: list[dict[str, Any]] = []
    document_words: dict[str, int] = {}
    for path in staged_paths:
        suffix = Path(path).suffix.lower()
        if suffix not in TEXT_SUFFIXES:
            continue
        data = staged_bytes(path)
        text = data.decode("utf-8")
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(text):
                privacy_candidates.append(
                    {"class": class_name, "path": path, "sample_sha256": hashlib.sha256(match.group(0).encode("utf-8")).hexdigest()}
                )
        if suffix in {".md", ".html", ".txt"}:
            document_words[path] = word_count(data)
    checks["five_class_privacy_scan"] = not privacy_candidates
    checks["document_ceiling"] = not [count for count in document_words.values() if count > DOCUMENT_WORD_CEILING]
    checks["overview_floor"] = document_words.get((REL_PHASE_ROOT / "x1/integrated-overview.md").as_posix(), 0) >= 1500
    checks["file_ceiling"] = len(staged_paths) < FILE_CEILING
    details["privacy_candidates"] = privacy_candidates
    details["document_words"] = document_words

    proposal_freeze = parsed_json.get((REL_PHASE_ROOT / "x1/proposal-freeze.json").as_posix(), {})
    proposal_rows: list[dict[str, Any]] = []
    for path in proposal_freeze.get("shards", []):
        proposal_rows.extend(parsed_json.get(path, {}).get("rows", []))
    outcome_counts = Counter(row.get("expected_disposition") for row in proposal_rows)
    required_fields = {
        "proposal_id", "title", "hypothesis", "null_or_failure_condition", "approval_class",
        "execution_lane", "official_or_primary_source_needs", "concrete_artifacts",
        "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates", "expected_disposition",
    }
    checks["forty_proposals"] = len(proposal_rows) == 40 and len({row.get("proposal_id") for row in proposal_rows}) == 40
    checks["proposal_contracts_complete"] = all(required_fields <= set(row) for row in proposal_rows)
    checks["four_outcome_labels"] = set(outcome_counts) == set(ALLOWED_OUTCOMES)
    checks["planned_outcomes_exact"] = dict(outcome_counts) == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
    checks["mutations_exact"] = sum(len(row.get("negative_fixtures", [])) for row in proposal_rows) == 160
    checks["x1_zero_credit"] = all(row.get("x1_completion_credit") == 0 and row.get("observed_disposition") is None for row in proposal_rows)

    novelty = parsed_json.get((REL_PHASE_ROOT / "x1/semantic-novelty-audit.json").as_posix(), {})
    checks["bounded_novelty_exact"] = (
        novelty.get("declared_inherited_frozen_proposals") == INHERITED_FROZEN_PROPOSALS
        and novelty.get("exact_title_collisions") == 0
        and novelty.get("quarantined_proposals") == 0
        and novelty.get("unavailable_history_is_open_gap") is True
        and novelty.get("universal_novelty_claim") is False
        and novelty.get("maximum_neighbor", {}).get("neighbor", {}).get("score", 1.0) < 0.75
    )
    portfolio_actual: dict[str, int] = {}
    for category in PORTFOLIO_COUNTS:
        path = (REL_PHASE_ROOT / f"x1/portfolios/{category}.json").as_posix()
        portfolio_actual[category] = len(parsed_json.get(path, {}).get("rows", []))
    checks["portfolio_counts_exact"] = portfolio_actual == PORTFOLIO_COUNTS
    checks["exact_and_blocked_held"] = all(
        row.get("execution_state") == "held_unexecuted"
        for category in ("exact_approval", "blocked")
        for row in parsed_json.get((REL_PHASE_ROOT / f"x1/portfolios/{category}.json").as_posix(), {}).get("rows", [])
    )

    ledger = parsed_json.get((REL_PHASE_ROOT / "method-flow/x1-ledger.json").as_posix(), {})
    methods = ledger.get("methods", [])
    witnesses = ledger.get("witnesses", [])
    witness_ids = {row.get("witness_id") for row in witnesses}
    checks["method_flow_exact"] = (
        len(methods) == len(STARTUP_FAILURES)
        and Counter(row.get("result") for row in witnesses) == {"fail": len(STARTUP_FAILURES), "pass": len(STARTUP_FAILURES)}
        and all(set(row.get("validation_witness_ids", [])) <= witness_ids for row in methods)
        and ledger.get("activation_overlay") == ACTIVATION_OVERLAY
    )
    phase_truth = parsed_json.get((REL_PHASE_ROOT / "x1/phase-truth.json").as_posix(), {})
    checks["phase_truth_planning_only"] = (
        phase_truth.get("lifecycle") == "X1_PLANNING_CANDIDATE_NOT_COMMITTED"
        and phase_truth.get("observed_outcomes") == {label: 0 for label in ALLOWED_OUTCOMES}
        and phase_truth.get("canonical_validation") == "not_run"
        and phase_truth.get("terminal_verdict") == TERMINAL_VERDICT
    )

    manifest = parsed_json.get(MANIFEST_PATH, {})
    manifest_mismatches: list[dict[str, Any]] = []
    for entry in manifest.get("entries", []):
        path = entry["path"]
        try:
            data = staged_bytes(path)
            oid = staged_oid(path)
        except Exception as error:
            manifest_mismatches.append({"path": path, "error": f"{type(error).__name__}: {error}"})
            continue
        actual = {"bytes": len(data), "git_blob_oid": oid, "sha256": hashlib.sha256(data).hexdigest()}
        expected = {key: entry[key] for key in actual}
        if actual != expected:
            manifest_mismatches.append({"path": path, "expected": expected, "actual": actual})
    checks["manifest_replay_exact"] = (
        manifest.get("entry_count") == len(manifest.get("entries", []))
        and not manifest_mismatches
        and set(manifest.get("self_exclusions", [])) == {MANIFEST_PATH, REVIEW_PATH}
    )
    details["manifest_mismatches"] = manifest_mismatches

    checks["owner_tests"] = owner_tests == 16 and owner_tests_return_code == 0
    details["owner_tests"] = owner_tests
    details["owner_tests_return_code"] = owner_tests_return_code
    details["portfolio_counts"] = portfolio_actual
    details["outcome_counts"] = dict(outcome_counts)
    details["staged_paths"] = len(staged_paths)
    details["strict_json_count"] = len(json_paths)
    details["python_ast_count"] = len(python_paths)
    details["markdown_count"] = len(markdown_paths)

    return {
        "all_passed": all(checks.values()),
        "boundary": "Bounded owner-self-scoped x1 staged validation only; not x2 evidence, final canonical validation, full repository suite, or independent reproduction.",
        "checks": checks,
        "details": details,
        "generated_at_utc": utc_now(),
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.x1-staged-review.v2",
        "status": "PASS_X1_EXACT_STAGED" if all(checks.values()) else "FAIL_X1_EXACT_STAGED_ZERO_CREDIT",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner-tests", type=int, required=True)
    parser.add_argument("--owner-tests-return-code", type=int, required=True)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    receipt = compute(args.owner_tests, args.owner_tests_return_code)
    if args.write:
        path = ROOT / REVIEW_PATH
        path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
    raise SystemExit(0 if receipt["all_passed"] else 1)


if __name__ == "__main__":
    main()
