#!/usr/bin/env python3
"""Single-use exact-final owner-scoped canonical validator for Elowen v688-v5."""

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
BRANCH = "codex/GHC-Family/elowen-cairn-v688-v5-full-tools"
BASE = "docs/elowen-cairn/v688-v5"
EXPECTED_COUNTS = {
    "proposals": 16430,
    "negatives": 84363,
    "methods": 94015,
    "failed_witnesses": 55211,
    "passing_witnesses": 86064,
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


def owner_path(path: str) -> bool:
    return (
        path.startswith(f"{BASE}/")
        or path.startswith("scripts/build_ghc_family_elowen_cairn_v688_v5_")
        or path.startswith("scripts/ghc_family_elowen_cairn_v688_v5_")
        or path.startswith("scripts/ghc_family_go_")
        or path.startswith("scripts/ghc_family_sgf_")
        or path.startswith("tests/test_ghc_family_elowen_cairn_v688_v5_")
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
        line_end = proc.stdout.find(b"\n", position)
        if line_end < 0:
            raise RuntimeError(f"missing batch header for {path}")
        header = proc.stdout[position:line_end].decode("utf-8", "replace").split()
        position = line_end + 1
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
    for entry in manifest["entries"]:
        data = normalized(blobs[entry["path"]])
        if (
            len(data) != entry["bytes_normalized_lf"]
            or hashlib.sha256(data).hexdigest() != entry["sha256_normalized_lf"]
        ):
            failures.append({"path": entry["path"], "error": "normalized_blob_mismatch"})
    return {
        "path": path,
        "entry_count": len(manifest["entries"]),
        "exclusion_count": len(manifest["declared_self_exclusions"]),
        "failure_count": len(failures),
        "failures": failures,
        "valid": not failures,
    }


def privacy_scan(paths: list[str], blobs: dict[str, bytes]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(rb"\b019[a-f0-9]{29,}\b", re.I),
        "private_absolute_path": re.compile(rb"(?:[A-Za-z]:\\Users\\|D:\\GHC-Archives\\)", re.I),
        "credential_or_private_key": re.compile(rb"(?:(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)"),
        "private_callable_identifier": re.compile(rb"\b(?:source_thread_id|providerTabId|clientThreadId)\b"),
        "private_session_or_route": re.compile(rb"(?:codex://|app://|session[_ -]?stream)", re.I),
    }
    definitions = {
        "scripts/build_ghc_family_elowen_cairn_v688_v5_x1.py",
        "scripts/build_ghc_family_elowen_cairn_v688_v5_x2.py",
        "scripts/build_ghc_family_elowen_cairn_v688_v5_final.py",
        "scripts/ghc_family_elowen_cairn_v688_v5_canonical_validator.py",
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
            boundary_vocabulary = (
                path == f"{BASE}/x1/integrated-overview.md"
                and class_name == "private_session_or_route"
                and all(match.group(0).lower() == b"session stream" for match in matches)
                and b"Repository artifacts exclude" in blobs[path]
            )
            row = {
                "path": path,
                "class": class_name,
                "match_count": len(matches),
                "adjudication": (
                    "scanner_definition_not_payload"
                    if path in definitions
                    else "boundary_vocabulary_not_payload"
                    if boundary_vocabulary
                    else "confirmed_payload_hit"
                ),
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


def ast_security(paths: list[str], blobs: dict[str, bytes]) -> dict[str, Any]:
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
    commits = [line for line in git_text("rev-list", "--reverse", f"{SOURCE}..{head}").splitlines() if line]
    merges = [line for line in git_text("rev-list", "--merges", f"{SOURCE}..{head}").splitlines() if line]
    parent_counts = [len(git_text("rev-list", "--parents", "-n", "1", commit).split()) - 1 for commit in commits]

    final_test = run([sys.executable, "-B", "tests/test_ghc_family_elowen_cairn_v688_v5_final.py"])
    final_test_output = (final_test.stdout + final_test.stderr).decode("utf-8", "replace")
    candidate_paths = [
        line
        for line in git_text("ls-tree", "-r", "--name-only", head, "--", BASE, "scripts", "tests").splitlines()
        if line
    ]
    owner_paths = sorted(path for path in candidate_paths if owner_path(path))
    owner_blobs = batch_blobs(head, owner_paths)

    json_paths = [path for path in owner_paths if path.endswith(".json")]
    json_failures = []
    for path in json_paths:
        try:
            json.loads(owner_blobs[path].decode("utf-8"))
        except Exception as exc:
            json_failures.append({"path": path, "error": str(exc)})

    document_paths = [path for path in owner_paths if Path(path).suffix.lower() in {".md", ".html", ".yaml", ".yml"}]
    document_failures = []
    max_words = 0
    max_word_path = ""
    for path in document_paths:
        text = owner_blobs[path].decode("utf-8")
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

    manifests = [
        replay_manifest(X1, f"{BASE}/validation/x1-manifest.json"),
        replay_manifest(EVIDENCE, f"{BASE}/validation/evidence-manifest.json"),
        replay_manifest(head, f"{BASE}/validation/final-delta-manifest.json"),
        replay_manifest(head, f"{BASE}/validation/final-owner-manifest.json"),
    ]
    final_manifest = load(head, f"{BASE}/validation/final-owner-manifest.json")
    expected_owner = set(owner_paths) - set(final_manifest["declared_self_exclusions"])
    actual_owner = {row["path"] for row in final_manifest["entries"]}
    seal = load(head, f"{BASE}/seal/content-seal.json")
    seal_paths = [row["path"] for row in seal["targets"]]
    seal_blobs = batch_blobs(head, seal_paths)
    seal_failures = []
    for entry in seal["targets"]:
        data = normalized(seal_blobs[entry["path"]])
        if (
            len(data) != entry["bytes_normalized_lf"]
            or hashlib.sha256(data).hexdigest() != entry["sha256_normalized_lf"]
        ):
            seal_failures.append(entry["path"])

    privacy = privacy_scan(owner_paths, owner_blobs)
    security = ast_security(owner_paths, owner_blobs)
    truth = load(head, f"{BASE}/final/phase-truth.json")
    review = load(head, f"{BASE}/validation/final-staged-review.json")
    baton = owner_blobs[f"{BASE}/handoffs/future-seat-13-v688-v6-activation-candidate.md"].decode("utf-8")
    baton_words = len(baton.split())

    checks = {
        "exact_branch": branch == BRANCH,
        "head_parent_is_evidence": git_text("rev-parse", f"{head}^") == EVIDENCE,
        "source_to_final_three_commits": len(commits) == 3,
        "zero_merges": not merges,
        "single_parent_each": parent_counts == [1, 1, 1],
        "x1_exact": len(commits) == 3 and commits[0] == X1,
        "evidence_exact": len(commits) == 3 and commits[1] == EVIDENCE,
        "clean_before": status_before == "",
        "zero_divergence": divergence == ["0", "0"],
        "local_upstream_equal": head == upstream,
        "local_tracking_equal": head == tracking,
        "local_fresh_live_equal": head == live,
        "final_tests_pass": final_test.returncode == 0 and "Ran 16 tests" in final_test_output,
        "strict_json_pass": not json_failures,
        "document_checks_pass": not document_failures,
        "word_cap_pass": max_words <= 100000,
        "manifests_pass": all(row["valid"] for row in manifests),
        "owner_manifest_scope_exact": expected_owner == actual_owner,
        "content_seal_pass": not seal_failures,
        "privacy_pass": privacy["valid"],
        "security_pass": security["valid"],
        "outcome_labels_exact": truth["outcomes"] == {"completed": 165, "represented": 26, "open_gap": 3, "exact_gate": 6},
        "effective_counts_exact": truth["effective_counts"] == EXPECTED_COUNTS,
        "method_flow_exact": truth["owner_method_flow"]["methods"] == 70 and truth["owner_method_flow"]["witness_results"] == {"fail": 509, "pass": 509},
        "terminal_verdict_preserved": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "prepared_not_sent": truth["prepared_successor_state"] == "PREPARED_NOT_SENT" and seal["prepared_successor_state"] == "PREPARED_NOT_SENT",
        "future_identity_unassigned": truth["future_seat_13_resolved"] is False and seal["recipient_identity_preassigned"] is False,
        "baton_word_budget": 10000 <= baton_words <= 100000,
        "baton_thirteen_modules": baton.count("\n## Module ") == 13,
        "file_budget": len(owner_paths) < 2000,
        "no_deletions": review["deletions"] == [],
        "no_outside_owner_paths": review["outside_owner_paths"] == [],
        "no_x1_or_x2_mutations_in_final": review["x1_or_x2_mutations"] == [],
    }
    minimal = {
        "source_ancestral": run(["git", "merge-base", "--is-ancestor", SOURCE, head]).returncode == 0,
        "x1_ancestral": run(["git", "merge-base", "--is-ancestor", X1, head]).returncode == 0,
        "evidence_parent": git_text("rev-parse", f"{head}^") == EVIDENCE,
        "branch_exact": branch == BRANCH,
        "clean": status_before == "",
        "zero_divergence": divergence == ["0", "0"],
        "fresh_live_equal": head == live,
        "three_commits": len(commits) == 3,
        "zero_merges": not merges,
        "one_final_parent": parent_counts[-1:] == [1],
        "manifests_valid": all(row["valid"] for row in manifests),
        "privacy_zero_confirmed": privacy["confirmed_hit_count"] == 0,
        "security_zero_findings": security["finding_count"] == 0,
        "not_ready_for_stage20": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "future_seat_unresolved": truth["future_seat_13_resolved"] is False,
    }
    status_after = git_text("status", "--porcelain=v1", "-uall")
    checks["clean_after"] = status_after == ""
    checks["head_stable"] = head == git_text("rev-parse", "HEAD")
    success = all(checks.values()) and all(minimal.values())
    payload = {
        "schema": "ghc.family.exact-final-owner-scoped-canonical.v688.v5",
        "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" if success else "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "owner": "Elowen Cairn",
        "phase": "v688-v5",
        "head": head,
        "branch": branch,
        "canonical_invocation_count": 1,
        "canonical_success_count": 1 if success else 0,
        "canonical_replay_count": 0,
        "replay_prohibited": True,
        "final_test_count": 16,
        "final_test_exit_code": final_test.returncode,
        "final_test_output": final_test_output,
        "json_parse_count": len(json_paths),
        "json_parse_failures": json_failures,
        "document_check_count": len(document_paths),
        "document_failures": document_failures,
        "maximum_document_words": max_words,
        "maximum_document_path": max_word_path,
        "owner_file_count": len(owner_paths),
        "manifest_results": manifests,
        "manifest_entry_total": sum(row["entry_count"] for row in manifests),
        "seal_target_count": seal["target_count"],
        "seal_failures": seal_failures,
        "privacy": privacy,
        "security": security,
        "baton_word_count": baton_words,
        "baton_module_count": baton.count("\n## Module "),
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
    print(
        json.dumps(
            {
                "status": receipt["status"],
                "head": head,
                "payload_sha256": payload_hash,
                "tests": f"{16 if final_test.returncode == 0 else 0}/16",
                "detailed": f"{receipt['detailed_pass_count']}/{receipt['detailed_check_count']}",
                "minimal": f"{receipt['minimal_pass_count']}/{receipt['minimal_check_count']}",
                "json": len(json_paths),
                "owner_files": len(owner_paths),
                "manifests": receipt["manifest_entry_total"],
                "privacy_confirmed": privacy["confirmed_hit_count"],
                "security_findings": security["finding_count"],
            },
            sort_keys=True,
        )
    )
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
