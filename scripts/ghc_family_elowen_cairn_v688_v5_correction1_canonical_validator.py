#!/usr/bin/env python3
"""One-shot dependency-corrected canonical composite for Elowen v688-v5."""

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
SOURCE = "adadd367036e49cfb5c480f2aa0b598c164cac1c"
X1 = "a4fffe1213f944e0017a8dd81f227d98785d43d1"
EVIDENCE = "1b0574be8cebf6b44107fbd1e7005d1b3dddb6ef"
FIRST_FINAL = "3fb142f2d2b2281da4a562196ffc684a2c5e2564"
BRANCH = "codex/GHC-Family/elowen-cairn-v688-v5-full-tools"
BASE = "docs/elowen-cairn/v688-v5"
FAILED_RECEIPT_SHA256 = "1790204b92fb499305f55fbb474c3d9b488f74829671b4d43113f5f1da3cf963"
FAILED_PAYLOAD_SHA256 = "30f545e2805de59759c3030dbfb0ac1c59e56dabeb747dffa01e21da6cfc7240"
EXPECTED_COUNTS = {
    "proposals": 16430,
    "negatives": 84364,
    "methods": 94016,
    "failed_witnesses": 55212,
    "passing_witnesses": 86065,
    "open_gaps": 758,
    "exact_gates": 765,
}


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


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def allowed(path: str) -> bool:
    return (
        path.startswith(f"{BASE}/correction1/")
        or path.startswith(f"{BASE}/validation/correction1-")
        or path == "scripts/build_ghc_family_elowen_cairn_v688_v5_correction1.py"
        or path == "scripts/ghc_family_elowen_cairn_v688_v5_correction1_canonical_validator.py"
        or path == "tests/test_ghc_family_elowen_cairn_v688_v5_correction1.py"
    )


def batch_blobs(commit: str, paths: list[str]) -> dict[str, bytes]:
    if not paths:
        return {}
    query = b"".join(f"{commit}:{path}\n".encode("utf-8") for path in paths)
    proc = subprocess.run(
        ["git", "cat-file", "--batch"],
        cwd=ROOT,
        input=query,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode:
        raise RuntimeError(proc.stderr.decode("utf-8", "replace"))
    result: dict[str, bytes] = {}
    position = 0
    for path in paths:
        end = proc.stdout.find(b"\n", position)
        header = proc.stdout[position:end].decode("utf-8", "replace").split()
        position = end + 1
        if len(header) != 3 or header[1] != "blob":
            raise RuntimeError({"path": path, "header": header})
        size = int(header[2])
        result[path] = proc.stdout[position : position + size]
        position += size + 1
    return result


def replay_manifest(commit: str, path: str) -> dict[str, Any]:
    manifest = load(commit, path)
    paths = [row["path"] for row in manifest["entries"]]
    blobs = batch_blobs(commit, paths)
    failures = []
    for row in manifest["entries"]:
        data = normalized(blobs[row["path"]])
        if (
            len(data) != row["bytes_normalized_lf"]
            or hashlib.sha256(data).hexdigest() != row["sha256_normalized_lf"]
        ):
            failures.append(row["path"])
    return {
        "path": path,
        "entry_count": len(paths),
        "exclusion_count": len(manifest["declared_self_exclusions"]),
        "failures": failures,
        "valid": not failures,
    }


def correction_privacy(paths: list[str], blobs: dict[str, bytes]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(rb"\b019[a-f0-9]{29,}\b", re.I),
        "private_absolute_path": re.compile(rb"(?:[A-Za-z]:\\Users\\|D:\\GHC-Archives\\)", re.I),
        "credential_or_private_key": re.compile(rb"(?:(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)"),
        "private_callable_identifier": re.compile(rb"\b(?:source_thread_id|providerTabId|clientThreadId)\b"),
        "private_session_or_route": re.compile(rb"(?:codex://|app://|session[_ -]?stream)", re.I),
    }
    definitions = {
        "scripts/build_ghc_family_elowen_cairn_v688_v5_correction1.py",
        "scripts/ghc_family_elowen_cairn_v688_v5_correction1_canonical_validator.py",
    }
    candidates = []
    confirmed = []
    for path in paths:
        if Path(path).suffix.lower() not in {".py", ".json", ".md", ".html", ".yaml", ".yml", ".txt"}:
            continue
        for class_name, pattern in patterns.items():
            matches = list(pattern.finditer(blobs[path]))
            if not matches:
                continue
            row = {
                "path": path,
                "class": class_name,
                "match_count": len(matches),
                "adjudication": "scanner_definition_not_payload" if path in definitions else "confirmed_payload_hit",
            }
            candidates.append(row)
            if row["adjudication"] == "confirmed_payload_hit":
                confirmed.append(row)
    return {
        "scanned_file_count": len(paths),
        "candidate_count": len(candidates),
        "confirmed_hit_count": len(confirmed),
        "candidates": candidates,
        "confirmed_hits": confirmed,
        "valid": not confirmed,
    }


def correction_security(paths: list[str], blobs: dict[str, bytes]) -> dict[str, Any]:
    findings = []
    parsed = 0
    for path in paths:
        if not path.endswith(".py"):
            continue
        parsed += 1
        tree = ast.parse(blobs[path].decode("utf-8"), filename=path)
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
    parser.add_argument("--failed-receipt", required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    failed_path = Path(args.failed_receipt)
    receipt_path = Path(args.receipt)
    if receipt_path.exists():
        raise SystemExit("exclusive correction canonical receipt already exists; replay prohibited")
    if not failed_path.is_file():
        raise SystemExit("failed canonical receipt is missing")
    receipt_path.parent.mkdir(parents=True, exist_ok=True)

    failed_bytes = failed_path.read_bytes()
    failed_hash = hashlib.sha256(failed_bytes).hexdigest()
    failed = json.loads(failed_bytes.decode("utf-8"))
    head = git_text("rev-parse", "HEAD")
    branch = git_text("branch", "--show-current")
    status_before = git_text("status", "--porcelain=v1", "-uall")
    upstream = git_text("rev-parse", "@{upstream}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{branch}")
    live_line = git_text("ls-remote", "--heads", "origin", f"refs/heads/{branch}")
    live = live_line.split()[0] if live_line else ""
    divergence = git_text("rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()
    commits = [line for line in git_text("rev-list", "--reverse", f"{SOURCE}..{head}").splitlines() if line]
    merges = [line for line in git_text("rev-list", "--merges", f"{SOURCE}..{head}").splitlines() if line]
    parent_counts = [len(git_text("rev-list", "--parents", "-n", "1", commit).split()) - 1 for commit in commits]
    correction_paths = [line for line in git_text("diff", "--name-only", f"{FIRST_FINAL}..{head}").splitlines() if line]
    blobs = batch_blobs(head, correction_paths)

    correction_test = run([sys.executable, "-B", "tests/test_ghc_family_elowen_cairn_v688_v5_correction1.py"])
    correction_test_output = (correction_test.stdout + correction_test.stderr).decode("utf-8", "replace")
    json_paths = [path for path in correction_paths if path.endswith(".json")]
    json_failures = []
    for path in json_paths:
        try:
            json.loads(blobs[path].decode("utf-8"))
        except Exception as exc:
            json_failures.append({"path": path, "error": str(exc)})
    manifests = [
        replay_manifest(head, f"{BASE}/validation/correction1-delta-manifest.json"),
        replay_manifest(head, f"{BASE}/validation/correction1-owner-manifest.json"),
    ]
    seal = load(head, f"{BASE}/correction1/content-seal.json")
    seal_paths = [row["path"] for row in seal["targets"]]
    seal_blobs = batch_blobs(head, seal_paths)
    seal_failures = []
    for row in seal["targets"]:
        data = normalized(seal_blobs[row["path"]])
        if (
            len(data) != row["bytes_normalized_lf"]
            or hashlib.sha256(data).hexdigest() != row["sha256_normalized_lf"]
        ):
            seal_failures.append(row["path"])
    privacy = correction_privacy(correction_paths, blobs)
    security = correction_security(correction_paths, blobs)
    truth = load(head, f"{BASE}/correction1/phase-truth.json")
    review = load(head, f"{BASE}/validation/correction1-staged-review.json")
    first_overview = show(FIRST_FINAL, f"{BASE}/final/final-integrated-overview.md")
    head_overview = show(head, f"{BASE}/final/final-integrated-overview.md")
    failed_detail = {key for key, value in failed["detailed_checks"].items() if not value}

    checks = {
        "failed_receipt_hash_exact": failed_hash == FAILED_RECEIPT_SHA256,
        "failed_payload_hash_exact": failed["canonical_payload_sha256"] == FAILED_PAYLOAD_SHA256,
        "failed_status_preserved": failed["status"] == "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "failed_head_exact": failed["head"] == FIRST_FINAL,
        "failed_success_zero": failed["canonical_success_count"] == 0,
        "failed_replay_zero": failed["canonical_replay_count"] == 0,
        "failed_only_final_tests": failed_detail == {"final_tests_pass"},
        "failed_minimal_all_passed": failed["minimal_pass_count"] == failed["minimal_check_count"] == 15,
        "failed_manifests_all_passed": all(row["valid"] for row in failed["manifest_results"]),
        "failed_privacy_passed": failed["privacy"]["valid"] and failed["privacy"]["confirmed_hit_count"] == 0,
        "failed_security_passed": failed["security"]["valid"] and failed["security"]["finding_count"] == 0,
        "failed_json_passed": failed["json_parse_failures"] == [],
        "failed_documents_passed": failed["document_failures"] == [],
        "failed_seal_passed": failed["seal_failures"] == [],
        "exact_branch": branch == BRANCH,
        "correction_parent_is_first_final": git_text("rev-parse", f"{head}^") == FIRST_FINAL,
        "source_to_correction_four_commits": len(commits) == 4,
        "exact_prior_commits": commits[:3] == [X1, EVIDENCE, FIRST_FINAL],
        "zero_merges": not merges,
        "single_parent_each": parent_counts == [1, 1, 1, 1],
        "correction_paths_only": bool(correction_paths) and all(allowed(path) for path in correction_paths),
        "original_overview_unchanged": first_overview == head_overview,
        "clean_before": status_before == "",
        "zero_divergence": divergence == ["0", "0"],
        "local_upstream_tracking_live_equal": head == upstream == tracking == live,
        "correction_test_pass": correction_test.returncode == 0 and "Ran 1 test" in correction_test_output,
        "correction_json_pass": json_failures == [],
        "correction_manifests_pass": all(row["valid"] for row in manifests),
        "correction_seal_pass": seal_failures == [],
        "correction_privacy_pass": privacy["valid"],
        "correction_security_pass": security["valid"],
        "correction_counts_exact": truth["effective_counts"] == EXPECTED_COUNTS,
        "outcomes_unchanged": truth["outcomes_unchanged"] == {"completed": 165, "represented": 26, "open_gap": 3, "exact_gate": 6},
        "failed_canonical_not_promoted": truth["failed_canonical_success_credit"] == 0 and not truth["failed_canonical_replayed"],
        "prepared_not_sent": truth["prepared_successor_state"] == "PREPARED_NOT_SENT",
        "no_successor_contact": truth["successor_contacts"] == 0,
        "review_exact": review["unexpected_paths"] == [] and review["deletions"] == [] and review["prior_lifecycle_mutations"] == [],
        "not_ready_for_stage20": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
    }
    status_after = git_text("status", "--porcelain=v1", "-uall")
    checks["clean_after"] = status_after == ""
    checks["head_stable"] = head == git_text("rev-parse", "HEAD")
    success = all(checks.values())
    payload = {
        "schema": "ghc.family.dependency-corrected-exact-final-owner-scoped-canonical-composite.v688.v5",
        "status": (
            "VALID_DEPENDENCY_CORRECTED_EXACT_FINAL_OWNER_SCOPED_CANONICAL_COMPOSITE"
            if success
            else "INVALID_DEPENDENCY_CORRECTED_EXACT_FINAL_OWNER_SCOPED_CANONICAL_COMPOSITE"
        ),
        "owner": "Elowen Cairn",
        "phase": "v688-v5",
        "head": head,
        "branch": branch,
        "canonical_invocation_count_at_corrected_head": 1,
        "canonical_success_count_at_corrected_head": 1 if success else 0,
        "canonical_replay_count_at_corrected_head": 0,
        "original_canonical_invocation_count": 1,
        "original_canonical_success_count": 0,
        "original_canonical_replay_count": 0,
        "original_failed_receipt_sha256": failed_hash,
        "original_failed_payload_sha256": failed["canonical_payload_sha256"],
        "original_successful_components_replayed": False,
        "correction_test_count": 1,
        "correction_test_exit_code": correction_test.returncode,
        "correction_test_output": correction_test_output,
        "correction_path_count": len(correction_paths),
        "correction_json_parse_count": len(json_paths),
        "correction_json_failures": json_failures,
        "manifest_results": manifests,
        "manifest_entry_total": sum(row["entry_count"] for row in manifests),
        "seal_target_count": seal["target_count"],
        "seal_failures": seal_failures,
        "privacy": privacy,
        "security": security,
        "checks": checks,
        "pass_count": sum(checks.values()),
        "check_count": len(checks),
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
    print(
        json.dumps(
            {
                "status": receipt["status"],
                "head": head,
                "payload_sha256": payload_hash,
                "correction_test": "1/1" if correction_test.returncode == 0 else "0/1",
                "checks": f"{receipt['pass_count']}/{receipt['check_count']}",
                "manifests": receipt["manifest_entry_total"],
                "json": len(json_paths),
                "privacy_confirmed": privacy["confirmed_hit_count"],
                "security_findings": security["finding_count"],
                "original_success_credit": 0,
                "original_components_replayed": False,
            },
            sort_keys=True,
        )
    )
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
