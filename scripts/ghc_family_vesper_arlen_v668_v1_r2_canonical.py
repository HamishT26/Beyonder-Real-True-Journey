#!/usr/bin/env python3
"""One-shot exact-final owner-scoped validator for Vesper v668-v1-r2."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PHASE_PREFIX = "docs/vesper-arlen/v668-v1-r2/"
SOURCE = "d3fd3065a4570046335689c62af8faf636be7a86"
X1 = "be908eb829185971c10be6d100c2c85fd35871e0"
EVIDENCE = "813b4bd702c85476cc87791790d1e1cd27e4b5ff"
PRIOR_FINAL = "707cfde5a5dd9418531b7bc84c98c04143a0f7d7"
BRANCH = "codex/GHC-Family/vesper-arlen-v668-v1-r2-remaster"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
TEXT_SUFFIXES = {".json", ".md", ".txt", ".html", ".py", ".toml", ".yaml", ".yml", ".mjs", ".js"}
POLICY_DEFINITION_PATHS = {
    "scripts/ghc_family_vesper_arlen_v668_v1_r2_staged_review.py",
    "scripts/ghc_family_vesper_arlen_v668_v1_r2_canonical.py",
}
PRIVACY_CLASSES = {
    "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.IGNORECASE),
    "credential_or_token_assignment": re.compile(r"(?i)\b(?:api[_-]?key|password|secret|bearer|token)\b\s*[:=]\s*['\"][^'\"]{8,}"),
    "private_absolute_local_path": re.compile(r"\b[A-Za-z]:[\\/](?!/)"),
    "private_conversation_or_route_material": re.compile(r"(?i)\b(?:source_thread_id|codex_delegation|resume_value|raw_task_id)\b"),
    "private_callable_or_app_state": re.compile(r"(?i)\b(?:private_callable_identifier|private_app_state|session_stream_payload)\b"),
}


def run(command: list[str], *, check: bool = False, timeout: int = 600) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(command, cwd=ROOT, capture_output=True, check=check, timeout=timeout)


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return run(["git", "-C", str(ROOT), *args], check=check)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def blob(commit: str, path: str) -> bytes:
    return git("show", f"{commit}:{path}").stdout


def document(commit: str, path: str) -> Any:
    return json.loads(blob(commit, path).decode("utf-8"))


def manifest_check(commit: str, path: str) -> dict[str, Any]:
    manifest = document(commit, path)
    mismatches = []
    for row in manifest["entries"]:
        data = blob(commit, row["path"])
        if len(data) != row["bytes"] or sha256(data) != row["sha256"]:
            mismatches.append(row["path"])
    return {"path": path, "entries": len(manifest["entries"]), "mismatches": mismatches, "passed": not mismatches, "self_exclusions": manifest.get("self_exclusions", [])}


def allowed_owner_path(path: str) -> bool:
    if path.startswith(PHASE_PREFIX):
        return True
    name = Path(path).name
    return path.startswith("scripts/") and "v668_v1_r2" in name or path.startswith("tests/") and "v668_v1_r2" in name


def privacy_scan(commit: str, paths: list[str]) -> dict[str, Any]:
    hits: list[dict[str, str]] = []
    scanned = 0
    excluded = []
    for path in sorted(paths):
        if Path(path).suffix.casefold() not in TEXT_SUFFIXES:
            continue
        if path in POLICY_DEFINITION_PATHS:
            excluded.append(path)
            continue
        text = blob(commit, path).decode("utf-8", errors="replace")
        scanned += 1
        for class_name, pattern in PRIVACY_CLASSES.items():
            if pattern.search(text):
                hits.append({"path": path, "class": class_name})
    return {"classes": len(PRIVACY_CLASSES), "files_scanned": scanned, "policy_definition_exclusions": excluded, "confirmed_hits": hits, "confirmed_hit_count": len(hits)}


def python_review(commit: str, paths: list[str]) -> dict[str, Any]:
    findings: list[dict[str, str]] = []
    parsed = 0
    for path in sorted(item for item in paths if item.endswith(".py")):
        source = blob(commit, path).decode("utf-8")
        tree = ast.parse(source, filename=path)
        parsed += 1
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                name = ""
                if isinstance(node.func, ast.Name):
                    name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    name = node.func.attr
                qualified = name
                if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                    qualified = f"{node.func.value.id}.{node.func.attr}"
                if qualified in {"eval", "exec", "os.system", "pickle.loads", "marshal.loads", "yaml.load"}:
                    findings.append({"path": path, "call": qualified})
                if name in {"run", "Popen", "call", "check_call", "check_output"} and any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords):
                    findings.append({"path": path, "call": "subprocess_shell_true"})
    return {"python_files": parsed, "findings": findings, "finding_count": len(findings)}


def bool_check(checks: list[dict[str, Any]], label: str, passed: bool, detail: Any = None) -> None:
    checks.append({"label": label, "passed": bool(passed), "detail": detail})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    receipt_path = Path(args.receipt)
    if receipt_path.exists():
        raise SystemExit("one-shot receipt already exists; canonical replay refused")
    receipt_path.parent.mkdir(parents=True, exist_ok=True)

    head = git("rev-parse", "HEAD").stdout.decode().strip()
    parent = git("rev-parse", "HEAD^").stdout.decode().strip()
    branch = git("branch", "--show-current").stdout.decode().strip()
    status_before = git("status", "--porcelain").stdout.decode().strip()
    upstream = git("rev-parse", "@{u}").stdout.decode().strip()
    tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}").stdout.decode().strip()
    live_line = git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}").stdout.decode().strip()
    live = live_line.split()[0] if live_line else ""
    divergence = git("rev-list", "--left-right", "--count", "HEAD...@{u}").stdout.decode().strip().split()
    history = git("rev-list", "--reverse", f"{SOURCE}..{head}").stdout.decode().splitlines()
    merge_count = len(git("rev-list", "--merges", f"{SOURCE}..{head}").stdout.decode().splitlines())
    changed_paths = git("diff", "--name-only", f"{SOURCE}..{head}").stdout.decode().splitlines()
    out_of_scope = [path for path in changed_paths if not allowed_owner_path(path)]

    test_command = [
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "tests/test_ghc_family_vesper_arlen_v668_v1_r2_x1.py",
        "tests/test_ghc_family_vesper_arlen_v668_v1_r2_x2.py",
        "tests/test_ghc_family_vesper_arlen_v668_v1_r2_final.py",
    ]
    test_result = run(test_command, timeout=600)
    test_text = (test_result.stdout + test_result.stderr).decode("utf-8", errors="replace")
    passed_match = re.search(r"(\d+) passed", test_text)
    tests_passed = int(passed_match.group(1)) if passed_match else 0

    owner_manifest_path = f"{PHASE_PREFIX}validation/final-owner-manifest.json"
    owner_manifest = document(head, owner_manifest_path)
    owner_paths = [row["path"] for row in owner_manifest["entries"]] + owner_manifest["self_exclusions"]
    owner_paths = sorted(set(owner_paths))
    manifests = [
        manifest_check(X1, f"{PHASE_PREFIX}x1/manifest.json"),
        manifest_check(EVIDENCE, f"{PHASE_PREFIX}validation/evidence-content-manifest.json"),
        manifest_check(head, owner_manifest_path),
        manifest_check(head, f"{PHASE_PREFIX}validation/final-delta-manifest.json"),
    ]
    privacy = privacy_scan(head, owner_paths)
    python_security = python_review(head, owner_paths)
    phase_json_paths = sorted(path for path in owner_paths if path.startswith(PHASE_PREFIX) and path.endswith(".json"))
    json_errors = []
    for path in phase_json_paths:
        try:
            document(head, path)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            json_errors.append({"path": path, "error_class": type(exc).__name__})

    outcomes = document(head, f"{PHASE_PREFIX}x2/proposals/proposal-outcomes.json")
    mutations = document(head, f"{PHASE_PREFIX}x2/proposals/negative-mutation-results.json")
    inherited = document(head, f"{PHASE_PREFIX}x2/proposals/inherited-refinement-review.json")
    portfolio = document(head, f"{PHASE_PREFIX}x2/portfolio/owner-execution.json")
    tools_original = document(head, f"{PHASE_PREFIX}x2/toolchain/toolchain-transaction.json")
    tools_correction = document(head, f"{PHASE_PREFIX}x2/toolchain/toolchain-audit-correction.json")
    tools_catalog = document(head, f"{PHASE_PREFIX}x2/toolchain/installed-tool-catalog-corrected.json")
    skills = document(head, f"{PHASE_PREFIX}x2/skills/skill-catalog.json")
    promotion = document(head, f"{PHASE_PREFIX}x2/skills/global-promotion-receipt.json")
    runners = document(head, f"{PHASE_PREFIX}x2/runners/runner-catalog.json")
    cards = document(head, f"{PHASE_PREFIX}x2/cards/deck.json")
    flow = document(head, f"{PHASE_PREFIX}method-flow/method-flow-ledger.json")
    closeout_flow = document(head, f"{PHASE_PREFIX}method-flow/closeout-operational-method-flow.json")
    route = document(head, f"{PHASE_PREFIX}closeout/route-and-roster-record.json")
    final_record = document(head, f"{PHASE_PREFIX}final/final-record.json")
    staged_review = document(head, f"{PHASE_PREFIX}validation/final-staged-review.json")
    seal = document(head, f"{PHASE_PREFIX}seal/content-seal.json")
    baton_path = f"{PHASE_PREFIX}handoffs/lyren-moss-v668-v2-activation.md"
    baton = blob(head, baton_path)
    baton_words = len(baton.decode("utf-8").split())

    owner_manifest_bytes = blob(head, owner_manifest_path)
    delta_manifest_path = f"{PHASE_PREFIX}validation/final-delta-manifest.json"
    delta_manifest_bytes = blob(head, delta_manifest_path)
    diff_check = git("diff", "--check", f"{SOURCE}..{head}", check=False)
    stale_labels = [row for row in outcomes["outcomes"] if row["outcome"] not in ALLOWED_OUTCOMES]

    detailed: list[dict[str, Any]] = []
    bool_check(detailed, "tests", test_result.returncode == 0 and tests_passed > 0, tests_passed)
    bool_check(detailed, "branch", branch == BRANCH, branch)
    bool_check(detailed, "clean_before", not status_before)
    bool_check(detailed, "parent_prior_final", parent == PRIOR_FINAL, parent)
    bool_check(detailed, "history_four_commits", history == [X1, EVIDENCE, PRIOR_FINAL, head], history)
    bool_check(detailed, "zero_merges", merge_count == 0, merge_count)
    bool_check(detailed, "owner_scope", not out_of_scope, out_of_scope)
    bool_check(detailed, "four_way_equality", len({head, upstream, tracking, live}) == 1, {"head": head, "upstream": upstream, "tracking": tracking, "live": live})
    bool_check(detailed, "zero_divergence", divergence == ["0", "0"], divergence)
    bool_check(detailed, "manifest_parity", all(row["passed"] for row in manifests), manifests)
    bool_check(detailed, "json_parse", not json_errors, {"parsed": len(phase_json_paths), "errors": json_errors})
    bool_check(detailed, "privacy", privacy["confirmed_hit_count"] == 0, privacy)
    bool_check(detailed, "python_security", python_security["finding_count"] == 0, python_security)
    bool_check(detailed, "diff_hygiene", diff_check.returncode == 0, diff_check.returncode)
    bool_check(detailed, "outcomes", outcomes["outcome_counts"] == {"completed": 28, "exact_gate": 2, "open_gap": 2, "represented": 8})
    bool_check(detailed, "outcome_vocabulary", not stale_labels, stale_labels)
    bool_check(detailed, "mutations", mutations["count"] == 160 and mutations["all_rejected"] and mutations["all_retained"])
    bool_check(detailed, "inherited_zero_credit", inherited["count"] == 20 and inherited["completion_credit"] == 0 and inherited["novelty_credit"] == 0)
    bool_check(detailed, "portfolio", portfolio["counts"] == {"safe_now": 60, "candidates": 30, "skills": 20, "runners": 10, "clean_fix_refine": 60, "exact_unexecuted": 20, "blocked_unexecuted": 10})
    bool_check(detailed, "original_audit_retained", tools_original["state"] == "QUARANTINED_AUDIT_FINDINGS" and tools_original["pip_audit"]["vulnerability_count"] == 7)
    bool_check(detailed, "corrected_audit", tools_correction["state"] == "VALID_DEPENDENCY_CORRECTED_COMPOSITE_WITH_ZERO_ORIGINAL_AUDIT_CREDIT" and tools_correction["python_dependency_audit_corrected"]["vulnerability_count"] == 0)
    bool_check(detailed, "tool_catalog", tools_catalog["count"] == 13 and tools_catalog["audit_gate_passed"])
    bool_check(detailed, "skills", skills["count"] == 20 and skills["global_promoted_count"] == 10)
    bool_check(detailed, "promotion", promotion["promoted_count"] == 10 and promotion["collision_count"] == 0 and all(row["byte_parity"] for row in promotion["promotions"]))
    bool_check(detailed, "runners", runners["count"] == 10 and runners["all_pass"])
    bool_check(detailed, "cards", cards["card_count"] == 40 and cards["minimum_sections_per_card"] >= 13)
    bool_check(detailed, "method_flow_evidence", flow["effective_before_canonical"] == {"effective_negatives": 29039, "methods": 15625, "failed_witnesses": 1340, "passing_witnesses": 2175, "open_gaps": 209, "exact_gates": 204})
    bool_check(detailed, "method_flow_closeout", closeout_flow["effective_before_canonical"] == {"effective_negatives": 29043, "methods": 15629, "failed_witnesses": 1344, "passing_witnesses": 2179, "open_gaps": 209, "exact_gates": 204})
    bool_check(detailed, "route", route["prospective_next"] == {"owner": "Lyren Moss", "phase": "v668-v2", "state": "PREPARED_NOT_SENT"} and route["lyren_next_reminder"]["owner"] == "Ilyra Fen")
    bool_check(detailed, "baton_words", 10_000 <= baton_words <= 100_000, baton_words)
    bool_check(detailed, "baton_hash", sha256(baton) == seal["baton_sha256"], seal["baton_sha256"])
    bool_check(detailed, "content_seal", sha256(owner_manifest_bytes) == seal["owner_manifest_sha256"] and sha256(delta_manifest_bytes) == seal["delta_manifest_sha256"])
    bool_check(detailed, "staged_review", staged_review["state"] == "PASS_EXACT_FINAL_STAGE" and staged_review["privacy_hit_count"] == 0)
    bool_check(detailed, "terminal_verdict", final_record["terminal_verdict"] == "NOT_READY_FOR_STAGE_20")
    bool_check(detailed, "successor_unsent", final_record["successor_contacted"] is False and route["successor_contacted"] is False)
    bool_check(detailed, "file_guard", len(owner_paths) < 2000, len(owner_paths))

    minimal_labels = [
        "tests",
        "clean_before",
        "parent_prior_final",
        "history_four_commits",
        "zero_merges",
        "owner_scope",
        "four_way_equality",
        "zero_divergence",
        "manifest_parity",
        "json_parse",
        "privacy",
        "python_security",
        "baton_words",
        "terminal_verdict",
        "successor_unsent",
    ]
    by_label = {row["label"]: row for row in detailed}
    minimal = [by_label[label] for label in minimal_labels]
    success = all(row["passed"] for row in detailed)
    status_after = git("status", "--porcelain").stdout.decode().strip()
    success = success and not status_after

    payload = {
        "schema": "ghc.family.canonical-external-receipt.v1",
        "state": "PASS_EXACT_FINAL_OWNER_CANONICAL_ONCE" if success else "FAIL_EXACT_FINAL_OWNER_CANONICAL_ZERO_CREDIT",
        "canonical_invocation_count": 1,
        "canonical_success_credit": 1 if success else 0,
        "post_success_replay": False,
        "head": head,
        "branch": branch,
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "prior_final": PRIOR_FINAL,
        "history": history,
        "merge_count": merge_count,
        "tests": {"exit_code": test_result.returncode, "passed": tests_passed, "stdout_sha256": sha256(test_result.stdout), "stderr_sha256": sha256(test_result.stderr)},
        "detailed": {"passed": sum(row["passed"] for row in detailed), "total": len(detailed), "checks": detailed},
        "minimal": {"passed": sum(row["passed"] for row in minimal), "total": len(minimal), "checks": minimal},
        "json": {"parsed": len(phase_json_paths), "errors": json_errors},
        "privacy": privacy,
        "python_security": python_security,
        "manifests": manifests,
        "method_flow_effective": closeout_flow["effective_before_canonical"],
        "owner_path_count": len(owner_paths),
        "changed_path_count": len(changed_paths),
        "out_of_scope_paths": out_of_scope,
        "baton": {"path": baton_path, "words": baton_words, "sha256": sha256(baton)},
        "git": {"clean_before": not status_before, "clean_after": not status_after, "local": head, "upstream": upstream, "tracking": tracking, "fresh_live": live, "divergence": divergence},
        "same_owner_shared_infrastructure_only": True,
        "independent_reproduction": False,
        "external_audit": False,
        "repository_wide_suite": False,
        "successor_contacted": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    wrapper = {"payload": payload, "payload_sha256": sha256(canonical_bytes(payload))}
    receipt_path.write_bytes(canonical_bytes(wrapper) + b"\n")
    file_sha256 = sha256(receipt_path.read_bytes())
    print(json.dumps({"state": payload["state"], "head": head, "tests_passed": tests_passed, "detailed": f"{payload['detailed']['passed']}/{payload['detailed']['total']}", "minimal": f"{payload['minimal']['passed']}/{payload['minimal']['total']}", "json_parsed": len(phase_json_paths), "privacy_hits": privacy["confirmed_hit_count"], "manifest_entries": sum(row["entries"] for row in manifests), "receipt_sha256": file_sha256}, sort_keys=True))
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
