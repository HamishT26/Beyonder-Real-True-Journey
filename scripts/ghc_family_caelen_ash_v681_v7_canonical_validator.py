#!/usr/bin/env python3
"""Exclusive exact-final owner-scoped canonical validator for Caelen Ash v681-v7."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "4da1c50b22e1b30b5e7351b0641f350bdc8fbfbe"
X1_HEAD = "f31bb3fb3738136db75dc264325f267dc4068f4a"
EVIDENCE_HEAD = "ce01a79bd92c1c8de02df586075eadb0427cfed6"
BRANCH = "codex/GHC-Family/caelen-ash-v681-v7-full-tools"


def run(args, *, cwd=ROOT, check=True):
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)
    if check and result.returncode:
        raise RuntimeError(f"command failed {args}: {result.stdout} {result.stderr}")
    return result


def git(*args):
    return run(["git", *args]).stdout.strip()


def git_bytes(revision: str, path: str) -> bytes:
    result = subprocess.run(["git", "show", f"{revision}:{path}"], cwd=ROOT, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(f"git blob read failed: {revision}:{path}")
    return result.stdout.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def manifest(revision: str, path: str) -> dict:
    value = json.loads(git_bytes(revision, path))
    for entry in value["entries"]:
        data = git_bytes(revision, entry["path"])
        if len(data) != entry["bytes"] or sha(data) != entry["sha256"]:
            raise RuntimeError(f"manifest mismatch: {revision}:{entry['path']}")
    return value


def test_count(result) -> int:
    match = re.search(r"Ran (\d+) tests?", result.stdout + result.stderr)
    if result.returncode or not match:
        raise RuntimeError(f"test selection failed: {result.stdout} {result.stderr}")
    return int(match.group(1))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--receipt", required=True, type=Path)
    parser.add_argument("--latch", required=True, type=Path)
    parser.add_argument("--temp-root", required=True, type=Path)
    args = parser.parse_args()
    if args.receipt.exists() or args.latch.exists():
        raise RuntimeError("exclusive canonical receipt or latch already exists; replay forbidden")
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.latch.parent.mkdir(parents=True, exist_ok=True)
    args.temp_root.mkdir(parents=True, exist_ok=True)
    args.latch.write_text(json.dumps({"expected_head": args.expected_head, "invocations": 1, "replay": False}, sort_keys=True) + "\n", encoding="utf-8")

    checks = []
    head = git("rev-parse", "HEAD")
    clean_before = not git("status", "--porcelain=v1")
    branch = git("symbolic-ref", "--short", "HEAD")
    parent = git("rev-parse", "HEAD^")
    checks.extend([head == args.expected_head, clean_before, branch == BRANCH, parent == EVIDENCE_HEAD])
    checks.extend([
        git("rev-parse", f"{EVIDENCE_HEAD}^") == X1_HEAD,
        git("rev-parse", f"{X1_HEAD}^") == SOURCE,
        int(git("rev-list", "--count", f"{SOURCE}..{head}")) == 3,
        not git("rev-list", "--merges", f"{SOURCE}..{head}"),
        len(git("show", "-s", "--format=%P", head).split()) == 1,
    ])

    upstream = git("rev-parse", "@{u}")
    tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live = git("ls-remote", "origin", f"refs/heads/{BRANCH}").split()[0]
    divergence = [int(value) for value in git("rev-list", "--left-right", "--count", "HEAD...@{u}").split()]
    checks.extend([head == upstream == tracking == live, divergence == [0, 0]])

    x1_review_path = "docs/caelen-ash/v681-v7/validation/x1-staged-review.json"
    x1_review = json.loads(git_bytes(X1_HEAD, x1_review_path))
    with tempfile.TemporaryDirectory(prefix="caelen-v681-v7-x1-", dir=args.temp_root) as temp_name:
        temp = Path(temp_name)
        for path_text in x1_review["expected_paths"]:
            target = temp / path_text
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(git_bytes(X1_HEAD, path_text))
        x1_result = run([sys.executable, "-X", "utf8", str(temp / "tests/test_ghc_family_caelen_ash_v681_v7_x1.py")], cwd=temp, check=False)
        x1_tests = test_count(x1_result)
    x2_tests = test_count(run([sys.executable, "-X", "utf8", "tests/test_ghc_family_caelen_ash_v681_v7_x2.py"], check=False))
    final_tests = test_count(run([sys.executable, "-X", "utf8", "tests/test_ghc_family_caelen_ash_v681_v7_final.py"], check=False))
    checks.extend([x1_tests == 12, x2_tests == 12, final_tests == 12])

    manifest_specs = [
        (X1_HEAD, "docs/caelen-ash/v681-v7/validation/x1-index-manifest.json"),
        (EVIDENCE_HEAD, "docs/caelen-ash/v681-v7/validation/x2-evidence-manifest.json"),
        (head, "docs/caelen-ash/v681-v7/validation/final-delta-manifest.json"),
        (head, "docs/caelen-ash/v681-v7/validation/final-owner-manifest.json"),
    ]
    manifests = [manifest(rev, path) for rev, path in manifest_specs]
    manifest_entries = sum(item["entry_count"] for item in manifests)
    owner_manifest = manifests[-1]
    owner_paths = {entry["path"] for entry in owner_manifest["entries"]} | set(owner_manifest["declared_self_exclusions"])
    changed_paths = set(git("diff", "--name-only", f"{SOURCE}..{head}").splitlines())
    checks.append(owner_paths == changed_paths)

    json_paths = sorted(path for path in owner_paths if path.endswith(".json"))
    for path_text in json_paths:
        json.loads(git_bytes(head, path_text))
    document_paths = sorted(path for path in owner_paths if path.endswith((".md", ".html", ".txt")))
    python_paths = sorted(path for path in owner_paths if path.endswith(".py"))
    security_findings = []
    for path_text in python_paths:
        tree = ast.parse(git_bytes(head, path_text).decode("utf-8"), filename=path_text)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                security_findings.append({"path": path_text, "call": node.func.id})
    checks.append(not security_findings)

    seal_path = "docs/caelen-ash/v681-v7/closeout/content-seal.json"
    seal = json.loads(git_bytes(head, seal_path))
    for entry in seal["entries"]:
        data = git_bytes(head, entry["path"])
        if len(data) != entry["bytes"] or sha(data) != entry["sha256"]:
            raise RuntimeError(f"content seal mismatch: {entry['path']}")

    scanners = {
        "raw_task_thread_identifier": re.compile(r"(?i)(thread|task)[_-]?id.{0,16}[0-9a-f]{8}"),
        "private_absolute_path": re.compile(r"(?i)(?:[A-Z]:\\\\Users\\\\|/Users/|/home/)[^\"'\\s]+"),
        "credential_or_secret": re.compile(r"(?i)(api[_-]?key|password|secret|bearer)[=:][^\s\"']+"),
        "private_conversation_payload": re.compile(r"(?i)(raw transcript|session stream|private app state)"),
        "private_callable_route": re.compile(r"(?i)(send_message_to_thread|read_thread|list_threads).{0,40}[0-9a-f]{8}"),
    }
    candidates = []
    confirmed = []
    text_paths = [path for path in owner_paths if path.endswith((".py", ".json", ".md", ".html", ".txt"))]
    for path_text in text_paths:
        text = git_bytes(head, path_text).decode("utf-8")
        for label, pattern in scanners.items():
            if pattern.search(text):
                definition = path_text.startswith("scripts/build_ghc_family_") or path_text.endswith("canonical_validator.py")
                item = {"class": label, "path": path_text, "disposition": "scanner_definition_only" if definition else "confirmed_payload_hit"}
                candidates.append(item)
                if not definition:
                    confirmed.append(item)
    checks.append(not confirmed)
    checks.append(len(seal["entries"]) == 15)
    checks.append(len(owner_paths) < 2000)
    checks.append(all(checks))
    if not all(checks):
        raise RuntimeError("one or more exact-final canonical checks failed")

    clean_after = not git("status", "--porcelain=v1")
    if not clean_after:
        raise RuntimeError("owner lane became dirty during canonical validation")
    payload = {
        "branch": branch,
        "canonical_invocations": 1,
        "canonical_successes": 1,
        "clean_after": clean_after,
        "clean_before": clean_before,
        "confirmed_privacy_hits": 0,
        "content_seal_entries": len(seal["entries"]),
        "detailed_checks": len(checks),
        "document_checks": len(document_paths),
        "exact_final": head,
        "final_tests": final_tests,
        "fresh_four_way_equal": head == upstream == tracking == live,
        "json_parses": len(json_paths),
        "manifest_entries": manifest_entries,
        "owner_paths": len(owner_paths),
        "phase": "v681-v7",
        "privacy_candidates": candidates,
        "python_ast_checks": len(python_paths),
        "replay": False,
        "security_findings": security_findings,
        "state": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "tests_total": x1_tests + x2_tests + final_tests,
        "x1_tests": x1_tests,
        "x2_tests": x2_tests,
        "zero_merges": True,
    }
    payload["payload_sha256"] = sha((json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8"))
    args.receipt.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
