#!/usr/bin/env python3
"""Single-use exact-final owner-scoped canonical validator for Tamar v685-v1."""

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
SOURCE = "f138d0e9fd37d424a81887bb7a1bafa3eacba860"
X1 = "a640f907d154d6b5c7747c990a3c0b1d6fe987eb"
EVIDENCE = "9484532c6e45c6b3c87d068e06213dc4260cd7e1"
BRANCH = "codex/GHC-Family/tamar-vey-v685-v1-full-tools"
BASE = "docs/tamar-vey/v685-v1"


def run(args: list[str]) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(args, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def git(*args: str, check: bool = True) -> bytes:
    proc = run(["git", *args])
    if check and proc.returncode:
        raise RuntimeError(proc.stderr.decode("utf-8", "replace"))
    return proc.stdout


def git_text(*args: str) -> str:
    return git(*args).decode("utf-8", "replace").strip()


def show(commit: str, path: str) -> bytes:
    return git("show", f"{commit}:{path}")


def load(commit: str, path: str) -> Any:
    return json.loads(show(commit, path).decode("utf-8"))


def owner_path(path: str) -> bool:
    return (
        path.startswith(f"{BASE}/")
        or path.startswith("scripts/build_ghc_family_tamar_vey_v685_v1_")
        or path.startswith("scripts/ghc_family_tamar_vey_v685_v1_")
        or path.startswith("scripts/ghc_family_broommaking_")
        or path.startswith("tests/test_ghc_family_tamar_vey_v685_v1_")
    )


def replay_manifest(commit: str, path: str) -> dict[str, Any]:
    manifest = load(commit, path)
    failures = []
    for entry in manifest["entries"]:
        try:
            data = show(commit, entry["path"])
            mode = git_text("ls-tree", commit, "--", entry["path"]).split()[0]
        except Exception as exc:
            failures.append({"path": entry["path"], "error": str(exc)})
            continue
        if len(data) != entry["bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"] or mode != entry["mode"]:
            failures.append({"path": entry["path"], "error": "blob_or_mode_mismatch"})
    return {
        "path": path,
        "entry_count": len(manifest["entries"]),
        "exclusion_count": len(manifest["declared_self_exclusions"]),
        "failure_count": len(failures),
        "failures": failures,
        "valid": not failures,
    }


def privacy_scan(commit: str, paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(rb"\b019[a-f0-9]{29,}\b", re.I),
        "private_absolute_path": re.compile(rb"(?:[A-Za-z]:\\Users\\|D:\\GHC-Archives\\)", re.I),
        "credential_or_private_key": re.compile(rb"(?:sk-[A-Za-z0-9_-]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)"),
        "private_callable_identifier": re.compile(rb"\b(?:source_thread_id|providerTabId|clientThreadId)\b"),
        "private_session_or_route": re.compile(rb"(?:codex://|app://|session[_ -]?stream)", re.I),
    }
    candidates = []
    confirmed = []
    for path in paths:
        if Path(path).suffix.lower() not in {".py", ".json", ".md", ".html", ".yaml", ".yml", ".txt"}:
            continue
        data = show(commit, path)
        for class_name, pattern in patterns.items():
            if pattern.search(data):
                definition = (
                    path.startswith("scripts/build_ghc_family_tamar_vey_v685_v1_")
                    or path == "scripts/ghc_family_tamar_vey_v685_v1_canonical_validator.py"
                )
                row = {
                    "path": path,
                    "class": class_name,
                    "adjudication": "scanner_definition_not_payload" if definition else "confirmed_payload_hit",
                }
                candidates.append(row)
                if not definition:
                    confirmed.append(row)
    return {
        "scanned_file_count": len(paths),
        "candidate_count": len(candidates),
        "confirmed_hit_count": len(confirmed),
        "candidates": candidates,
        "confirmed_hits": confirmed,
        "valid": not confirmed,
    }


def ast_security(commit: str, paths: list[str]) -> dict[str, Any]:
    findings = []
    parsed = 0
    for path in paths:
        if not path.endswith(".py"):
            continue
        parsed += 1
        tree = ast.parse(show(commit, path).decode("utf-8"), filename=path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                findings.append({"path": path, "line": node.lineno, "kind": node.func.id})
            if isinstance(node, ast.Call):
                for keyword in node.keywords:
                    if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                        findings.append({"path": path, "line": node.lineno, "kind": "subprocess_shell_true"})
    return {"python_file_count": parsed, "finding_count": len(findings), "findings": findings, "valid": not findings}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    receipt_path = Path(args.receipt)
    if receipt_path.exists():
        raise SystemExit("exclusive canonical receipt already exists; replay prohibited")
    receipt_path.parent.mkdir(parents=True, exist_ok=True)

    head = git_text("rev-parse", "HEAD")
    branch = git_text("branch", "--show-current")
    status_before = git_text("status", "--porcelain=v1", "-uall")
    upstream = git_text("rev-parse", "@{upstream}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{branch}")
    live_line = git_text("ls-remote", "--heads", "origin", f"refs/heads/{branch}")
    live = live_line.split()[0] if live_line else ""
    divergence = git_text("rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()
    phase_commits = int(git_text("rev-list", "--count", f"{SOURCE}..{head}"))
    merges = [line for line in git_text("rev-list", "--merges", f"{SOURCE}..{head}").splitlines() if line]
    commits = [line for line in git_text("rev-list", "--reverse", f"{SOURCE}..{head}").splitlines() if line]
    parent_counts = [len(git_text("rev-list", "--parents", "-n", "1", commit).split()) - 1 for commit in commits]

    final_test = run([sys.executable, "-B", "tests/test_ghc_family_tamar_vey_v685_v1_final.py"])
    final_test_output = (final_test.stdout + final_test.stderr).decode("utf-8", "replace")
    owner_paths = [
        line
        for line in git_text("ls-tree", "-r", "--name-only", head).splitlines()
        if line and owner_path(line)
    ]
    json_paths = [path for path in owner_paths if path.endswith(".json")]
    json_failures = []
    for path in json_paths:
        try:
            json.loads(show(head, path).decode("utf-8"))
        except Exception as exc:
            json_failures.append({"path": path, "error": str(exc)})
    document_paths = [path for path in owner_paths if Path(path).suffix.lower() in {".md", ".html", ".yaml", ".yml"}]
    document_failures = []
    max_words = 0
    max_word_path = ""
    for path in document_paths:
        text = show(head, path).decode("utf-8")
        words = len(text.split())
        if words > max_words:
            max_words = words
            max_word_path = path
        if words > 100000:
            document_failures.append({"path": path, "error": "word_cap"})
        if path.endswith(".html") and not all(token in text for token in ("<title>", "<main>", 'lang="en"')):
            document_failures.append({"path": path, "error": "html_structure"})
        if path.endswith("SKILL.md") and not text.startswith("---\nname:"):
            document_failures.append({"path": path, "error": "skill_frontmatter"})

    manifest_results = [
        replay_manifest(X1, f"{BASE}/validation/x1-index-manifest.json"),
        replay_manifest(EVIDENCE, f"{BASE}/validation/evidence-index-manifest.json"),
        replay_manifest(head, f"{BASE}/validation/final-delta-manifest.json"),
        replay_manifest(head, f"{BASE}/validation/final-owner-manifest.json"),
    ]
    seal = load(head, f"{BASE}/seal/content-seal.json")
    seal_failures = []
    for entry in seal["targets"]:
        data = show(head, entry["path"])
        if hashlib.sha256(data).hexdigest() != entry["sha256"] or len(data) != entry["bytes"]:
            seal_failures.append(entry["path"])
    privacy = privacy_scan(head, owner_paths)
    security = ast_security(head, owner_paths)
    final_truth = load(head, f"{BASE}/final/phase-truth.json")
    final_review = load(head, f"{BASE}/validation/final-staged-review.json")
    final_manifest = load(head, f"{BASE}/validation/final-owner-manifest.json")
    expected_owner = set(owner_paths) - set(final_manifest["declared_self_exclusions"])
    actual_owner = {row["path"] for row in final_manifest["entries"]}

    checks = {
        "exact_branch": branch == BRANCH,
        "head_is_parented_by_evidence": git_text("rev-parse", f"{head}^") == EVIDENCE,
        "source_to_final_three_commits": phase_commits == 3,
        "phase_commit_list_count": len(commits) == 3,
        "zero_merges": not merges,
        "single_parent_per_phase_commit": parent_counts == [1, 1, 1],
        "x1_exact": commits[0] == X1 if len(commits) == 3 else False,
        "evidence_exact": commits[1] == EVIDENCE if len(commits) == 3 else False,
        "clean_before": status_before == "",
        "zero_ahead": divergence == ["0", "0"],
        "local_upstream_equal": head == upstream,
        "local_tracking_equal": head == tracking,
        "local_fresh_live_equal": head == live,
        "final_tests_pass": final_test.returncode == 0 and "Ran 12 tests" in final_test_output,
        "strict_json_pass": not json_failures,
        "document_checks_pass": not document_failures,
        "word_cap_pass": max_words <= 100000,
        "x1_manifest_pass": manifest_results[0]["valid"],
        "evidence_manifest_pass": manifest_results[1]["valid"],
        "final_delta_manifest_pass": manifest_results[2]["valid"],
        "final_owner_manifest_pass": manifest_results[3]["valid"],
        "final_owner_scope_exact": expected_owner == actual_owner,
        "content_seal_pass": not seal_failures,
        "privacy_pass": privacy["valid"],
        "security_pass": security["valid"],
        "outcome_labels_exact": final_truth["outcomes"] == {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3},
        "terminal_verdict_preserved": final_truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "prepared_not_sent": seal["prepared_successor_state"] == "PREPARED_NOT_SENT",
        "no_deletions": final_review["deletions"] == [],
        "no_outside_owner_paths": final_review["outside_owner_paths"] == [],
    }
    minimal = {
        "source_ancestral": git_text("merge-base", "--is-ancestor", SOURCE, head) == "",
        "x1_ancestral": git_text("merge-base", "--is-ancestor", X1, head) == "",
        "evidence_parent": git_text("rev-parse", f"{head}^") == EVIDENCE,
        "head_exact": head == git_text("rev-parse", "HEAD"),
        "branch_exact": branch == BRANCH,
        "clean": status_before == "",
        "zero_divergence": divergence == ["0", "0"],
        "fresh_live_equal": head == live,
        "three_commits": phase_commits == 3,
        "zero_merges": not merges,
        "one_final_parent": parent_counts[-1:] == [1],
        "manifests_valid": all(row["valid"] for row in manifest_results),
        "privacy_zero_confirmed": privacy["confirmed_hit_count"] == 0,
        "security_zero_findings": security["finding_count"] == 0,
        "not_ready_for_stage_20": final_truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
    }
    status_after = git_text("status", "--porcelain=v1", "-uall")
    checks["clean_after"] = status_after == ""
    checks["head_stable"] = head == git_text("rev-parse", "HEAD")
    success = all(checks.values()) and all(minimal.values())
    payload = {
        "schema": "ghc.family.exact-final-owner-scoped-canonical.v685.v1",
        "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" if success else "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "owner": "Tamar Vey",
        "phase": "v685-v1",
        "head": head,
        "branch": branch,
        "canonical_invocation_count": 1,
        "canonical_success_count": 1 if success else 0,
        "canonical_replay_count": 0,
        "replay_prohibited": True,
        "final_test_count": 12,
        "final_test_exit_code": final_test.returncode,
        "final_test_output": final_test_output,
        "json_parse_count": len(json_paths),
        "json_parse_failures": json_failures,
        "document_check_count": len(document_paths),
        "document_failures": document_failures,
        "maximum_document_words": max_words,
        "maximum_document_path": max_word_path,
        "owner_file_count": len(owner_paths),
        "manifest_results": manifest_results,
        "manifest_entry_total": sum(row["entry_count"] for row in manifest_results),
        "seal_target_count": seal["target_count"],
        "seal_failures": seal_failures,
        "privacy": privacy,
        "security": security,
        "detailed_checks": checks,
        "detailed_pass_count": sum(checks.values()),
        "detailed_check_count": len(checks),
        "minimal_checks": minimal,
        "minimal_pass_count": sum(minimal.values()),
        "minimal_check_count": len(minimal),
        "same_owner_shared_infrastructure": True,
        "independent_reproduction": False,
        "complete_repository_suite": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    payload_hash = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    receipt = {**payload, "canonical_payload_sha256": payload_hash}
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": receipt["status"],
        "head": head,
        "payload_sha256": payload_hash,
        "detailed": f"{receipt['detailed_pass_count']}/{receipt['detailed_check_count']}",
        "minimal": f"{receipt['minimal_pass_count']}/{receipt['minimal_check_count']}",
        "json": len(json_paths),
        "owner_files": len(owner_paths),
        "manifests": receipt["manifest_entry_total"],
        "privacy_confirmed": privacy["confirmed_hit_count"],
        "security_findings": security["finding_count"],
    }, sort_keys=True))
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
