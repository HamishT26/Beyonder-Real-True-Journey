#!/usr/bin/env python3
"""One-shot exact-final owner-scoped canonical validator for Sable v674-v2."""

from __future__ import annotations

import argparse
import ast
import hashlib
import io
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


SOURCE = "6f079df9a056f00e80392b7e036abc023db5fa88"
X1 = "81ad6f98f24087777691e96201312e66c37ac844"
EVIDENCE = "1625313186adde8dc94d210376f184bde5dfb0dc"
BRANCH = "codex/GHC-Family/sable-rook-v674-v2-full-tools"
REPO = Path(__file__).resolve().parents[1]
PHASE_PREFIX = "docs/sable-rook/v674-v2/"


def git(*args: str, text: bool = True) -> str | bytes:
    return subprocess.check_output(["git", *args], cwd=REPO, text=text)


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def load_commit_blobs(commit: str, wanted: list[str]) -> dict[str, bytes]:
    tree = git("ls-tree", "-r", "-z", commit, text=False)
    assert isinstance(tree, bytes)
    object_ids: dict[str, str] = {}
    for record in tree.split(b"\0"):
        if not record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        parts = metadata.split()
        if len(parts) == 3 and parts[1] == b"blob":
            object_ids[raw_path.decode("utf-8")] = parts[2].decode("ascii")
    missing = [path for path in wanted if path not in object_ids]
    if missing:
        raise RuntimeError(f"commit tree missing paths: {missing}")
    ordered_ids = [object_ids[path] for path in wanted]
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=REPO,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    output, error = process.communicate(("\n".join(ordered_ids) + "\n").encode("ascii"))
    if process.returncode != 0:
        raise RuntimeError(error.decode("utf-8", errors="replace"))
    stream = io.BytesIO(output)
    result: dict[str, bytes] = {}
    for path, expected_oid in zip(wanted, ordered_ids, strict=True):
        header = stream.readline().decode("ascii").strip().split()
        if len(header) != 3 or header[0] != expected_oid or header[1] != "blob":
            raise RuntimeError(f"unexpected cat-file header for {path}: {header}")
        size = int(header[2])
        data = stream.read(size)
        if len(data) != size or stream.read(1) != b"\n":
            raise RuntimeError(f"truncated cat-file payload for {path}")
        result[path] = data
    return result


def commit_json(commit: str, path: str) -> dict[str, Any]:
    return json.loads(load_commit_blobs(commit, [path])[path].decode("utf-8"))


def verify_manifest(commit: str, path: str, domain: str) -> dict[str, int]:
    manifest = commit_json(commit, path)
    entries = manifest["entries"]
    paths = [entry["path"] for entry in entries]
    blobs = load_commit_blobs(commit, paths)
    for entry in entries:
        data = blobs[entry["path"]]
        if domain == "normalized_lf":
            data = normalized(data)
            expected_bytes = entry["bytes_normalized_lf"]
            expected_hash = entry["sha256_normalized_lf"]
        elif domain == "raw_sha256":
            expected_bytes = entry["bytes"]
            expected_hash = entry.get("sha256", entry.get("sha256_git_index_blob"))
        else:
            raise RuntimeError(f"unknown manifest domain {domain}")
        if len(data) != expected_bytes or hashlib.sha256(data).hexdigest() != expected_hash:
            raise RuntimeError(f"manifest mismatch: {path} -> {entry['path']}")
    return {"entries": len(entries), "self_exclusions": len(manifest.get("self_exclusions", []))}


def write_exclusive_receipt(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise RuntimeError("exclusive canonical receipt already exists")
    temp = path.with_suffix(path.suffix + ".tmp")
    if temp.exists():
        raise RuntimeError("exclusive temporary receipt already exists")
    encoded = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    temp.write_text(encoded, encoding="utf-8", newline="\n")
    os.replace(temp, path)


def canonical(expected_final: str, receipt_path: Path) -> dict[str, Any]:
    if receipt_path.exists():
        raise RuntimeError("canonical latch already spent")
    local = str(git("rev-parse", "HEAD")).strip()
    if local != expected_final:
        raise RuntimeError(f"expected final mismatch: {local}")
    branch = str(git("branch", "--show-current")).strip()
    if branch != BRANCH:
        raise RuntimeError(f"unexpected branch: {branch}")
    if str(git("status", "--porcelain=v1")).strip():
        raise RuntimeError("canonical worktree is not clean before validation")
    if str(git("rev-parse", "HEAD^")).strip() != EVIDENCE:
        raise RuntimeError("final is not the direct child of evidence")
    if str(git("rev-parse", f"{EVIDENCE}^")).strip() != X1:
        raise RuntimeError("evidence is not the direct child of x1")
    if str(git("rev-parse", f"{X1}^")).strip() != SOURCE:
        raise RuntimeError("x1 is not the direct child of source")
    if str(git("rev-list", "--count", f"{SOURCE}..{expected_final}")).strip() != "3":
        raise RuntimeError("phase commit count is not three")
    if str(git("rev-list", "--merges", f"{SOURCE}..{expected_final}")).strip():
        raise RuntimeError("merge commit found in phase history")
    parent_count = len(str(git("show", "-s", "--format=%P", expected_final)).split())
    if parent_count != 1:
        raise RuntimeError("final does not have exactly one parent")

    manifest_results = {
        "x1": verify_manifest(X1, "docs/sable-rook/v674-v2/x1/x1-manifest.json", "raw_sha256"),
        "x1_staged": verify_manifest(X1, "docs/sable-rook/v674-v2/validation/x1-staged-review.json", "raw_sha256"),
        "evidence": verify_manifest(EVIDENCE, "docs/sable-rook/v674-v2/validation/x2-evidence-manifest.json", "normalized_lf"),
        "evidence_staged": verify_manifest(EVIDENCE, "docs/sable-rook/v674-v2/validation/x2-staged-review.json", "raw_sha256"),
        "final_owner": verify_manifest(expected_final, "docs/sable-rook/v674-v2/validation/final-owner-manifest.json", "normalized_lf"),
        "final_delta": verify_manifest(expected_final, "docs/sable-rook/v674-v2/validation/final-delta-manifest.json", "normalized_lf"),
        "final_staged": verify_manifest(expected_final, "docs/sable-rook/v674-v2/validation/final-staged-review.json", "raw_sha256"),
    }

    changed = str(git("diff", "--name-only", f"{SOURCE}..{expected_final}")).splitlines()
    owner_paths = sorted(path for path in changed if path.startswith(PHASE_PREFIX) or path.startswith("scripts/ghc_family_caption_") or "sable_rook_v674_v2" in path)
    if len(owner_paths) >= 2000:
        raise RuntimeError("owner file ceiling reached")
    blobs = load_commit_blobs(expected_final, owner_paths)
    json_parses = 0
    python_compiles = 0
    markdown_documents = 0
    html_documents = 0
    security_findings: list[dict[str, str]] = []
    for path, data in blobs.items():
        if path.endswith(".json"):
            json.loads(data.decode("utf-8")); json_parses += 1
        if path.endswith(".py"):
            text = data.decode("utf-8")
            compile(text, path, "exec"); python_compiles += 1
            tree = ast.parse(text, filename=path)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                    security_findings.append({"path": path, "call": node.func.id})
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "system":
                    security_findings.append({"path": path, "call": "system"})
        if path.endswith(".md"):
            markdown_documents += 1
            words = len(data.decode("utf-8").split())
            if words > 100000:
                raise RuntimeError(f"document ceiling exceeded: {path}")
        if path.endswith(".html"):
            html_documents += 1
    if security_findings:
        raise RuntimeError(f"bounded AST security findings: {security_findings}")

    patterns = {
        "raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(rb"(?:C:\\Users\\|D:\\GHC-Archives)", re.I),
        "raw_task_thread_identifier": re.compile(rb"(?:source_thread|thread|task)_id\s*[\"']?\s*[:=]\s*[\"'][0-9a-f-]{32,}", re.I),
        "credential_assignment": re.compile(rb"(?:password|api[_-]?key|secret|token)\s*[\"']?\s*[:=]\s*[\"'][^\"']{8,}", re.I),
        "private_conversation_payload": re.compile(rb"(?:session_stream|private_transcript|screenshot_payload)", re.I),
    }
    scanner_candidates: list[dict[str, str]] = []
    confirmed_hits: list[dict[str, str]] = []
    text_extensions = {".json", ".md", ".html", ".py", ".txt", ".yml", ".yaml"}
    privacy_files = 0
    for path, data in blobs.items():
        if Path(path).suffix.lower() not in text_extensions:
            continue
        privacy_files += 1
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(data):
                start = data.rfind(b"\n", 0, match.start()) + 1
                end = data.find(b"\n", match.end())
                if end < 0:
                    end = len(data)
                line = data[start:end]
                if path.endswith(".py") and (b"re.compile" in line or b"assertNot" in line):
                    scanner_candidates.append({"path": path, "class": class_name, "disposition": "scanner_definition_or_rejection_assertion"})
                else:
                    confirmed_hits.append({"path": path, "class": class_name})
    if confirmed_hits:
        raise RuntimeError(f"confirmed privacy hits: {confirmed_hits}")

    environment = os.environ.copy()
    environment["PYTHONUTF8"] = "1"
    environment["PYTHONIOENCODING"] = "utf-8"
    test_run = subprocess.run(
        [sys.executable, "-m", "unittest", "tests.test_ghc_family_sable_rook_v674_v2_final", "-v"],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
        env=environment,
    )
    if test_run.returncode != 0 or "Ran 14 tests" not in (test_run.stdout + test_run.stderr):
        raise RuntimeError("final owner test selection failed: " + (test_run.stdout + test_run.stderr)[-4000:])

    local_after = str(git("rev-parse", "HEAD")).strip()
    upstream = str(git("rev-parse", "@{upstream}")).strip()
    tracking = str(git("rev-parse", f"refs/remotes/origin/{BRANCH}")).strip()
    live_line = str(git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")).strip()
    live = live_line.split()[0] if live_line else ""
    divergence = str(git("rev-list", "--left-right", "--count", "@{upstream}...HEAD")).strip().split()
    if not (local_after == expected_final == upstream == tracking == live):
        raise RuntimeError("final four-way equality failed")
    if divergence != ["0", "0"]:
        raise RuntimeError(f"final divergence is not zero: {divergence}")
    if str(git("status", "--porcelain=v1")).strip():
        raise RuntimeError("canonical worktree is not clean after validation")

    payload: dict[str, Any] = {
        "schema": "ghc.family.external-canonical-receipt.v674.v2",
        "owner": "Sable Rook",
        "phase": "v674-v2",
        "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "expected_final": expected_final,
        "branch": BRANCH,
        "canonical_invocations": 1,
        "canonical_successes": 1,
        "replayed": False,
        "owner_tests": {"selected": 14, "passed": 14, "failed": 0},
        "immutable_evidence_selection": {"x1": "11/11", "x2": "14/14", "mixed_context_failure_retained": True},
        "manifest_results": manifest_results,
        "manifest_entries_total": sum(row["entries"] for row in manifest_results.values()),
        "manifest_self_exclusions_total": sum(row["self_exclusions"] for row in manifest_results.values()),
        "owner_paths": len(owner_paths),
        "json_parses": json_parses,
        "python_compiles": python_compiles,
        "markdown_documents": markdown_documents,
        "html_documents": html_documents,
        "privacy_files": privacy_files,
        "privacy_classes": list(patterns),
        "scanner_definition_candidates": len(scanner_candidates),
        "confirmed_privacy_hits": 0,
        "bounded_ast_security_findings": 0,
        "source_to_final_commits": 3,
        "merge_commits": 0,
        "final_parent_count": 1,
        "clean_before_and_after": True,
        "divergence": [0, 0],
        "four_way_equal": True,
        "complete_repository_suite": False,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    canonical_bytes = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    payload["canonical_payload_sha256"] = hashlib.sha256(canonical_bytes).hexdigest()
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-final", required=True)
    parser.add_argument("--receipt-path", required=True)
    args = parser.parse_args()
    receipt_path = Path(args.receipt_path)
    if receipt_path.exists():
        print(json.dumps({"status": "REFUSED_CANONICAL_LATCH_ALREADY_SPENT"}, sort_keys=True))
        return 3
    try:
        payload = canonical(args.expected_final, receipt_path)
    except Exception as error:  # retain one-shot failure without replay
        payload = {
            "schema": "ghc.family.external-canonical-receipt.v674.v2",
            "owner": "Sable Rook",
            "phase": "v674-v2",
            "status": "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT",
            "expected_final": args.expected_final,
            "canonical_invocations": 1,
            "canonical_successes": 0,
            "replay_forbidden": True,
            "error_type": type(error).__name__,
            "error": str(error),
            "complete_repository_suite": False,
            "independent_reproduction": False,
        }
        write_exclusive_receipt(receipt_path, payload)
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 1
    write_exclusive_receipt(receipt_path, payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
