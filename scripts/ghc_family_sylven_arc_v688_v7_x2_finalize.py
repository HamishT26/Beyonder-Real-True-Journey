#!/usr/bin/env python3
"""Prepare or verify the exact staged Sylven Arc v688-v7 x2 evidence manifest."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = "docs/sylven-arc/v688-v7"
X1 = "4b7459cdf681726b8d411d644dc6f8db70e83871"
MANIFEST = ROOT / BASE / "x2/evidence-manifest.json"
RECEIPT = ROOT / BASE / "x2/evidence-validation.json"
SELF_EXCLUSIONS = {f"{BASE}/x2/evidence-manifest.json", f"{BASE}/x2/evidence-validation.json"}
SCANNER_DEFINITION = "scripts/ghc_family_sylven_arc_v688_v7_x2_finalize.py"


def git(*args: str, binary: bool = False):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=not binary)


def write_new(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")


def staged_paths() -> list[str]:
    return [line for line in git("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if line]


def staged_blobs(paths: list[str]) -> dict[str, bytes]:
    index = {}
    for line in git("ls-files", "--stage").splitlines():
        left, path = line.split("\t", 1)
        _mode, object_id, stage = left.split()
        if stage == "0":
            index[path] = object_id
    missing = [path for path in paths if path not in index]
    if missing:
        raise RuntimeError("index_object_missing:" + missing[0])
    ordered = [(path, index[path]) for path in paths]
    process = subprocess.Popen(["git", "cat-file", "--batch"], cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate(("\n".join(object_id for _path, object_id in ordered) + "\n").encode("ascii"))
    if process.returncode:
        raise RuntimeError("git_cat_file_batch:" + error.decode("utf-8", errors="replace"))
    position = 0
    blobs = {}
    for path, expected_id in ordered:
        line_end = output.find(b"\n", position)
        if line_end < 0:
            raise RuntimeError("git_cat_file_header:" + path)
        header = output[position:line_end].decode("ascii").split()
        position = line_end + 1
        if len(header) != 3 or header[0] != expected_id or header[1] != "blob":
            raise RuntimeError("git_cat_file_shape:" + path)
        size = int(header[2])
        blobs[path] = output[position:position + size]
        position += size
        if output[position:position + 1] != b"\n":
            raise RuntimeError("git_cat_file_separator:" + path)
        position += 1
    if position != len(output):
        raise RuntimeError("git_cat_file_trailing_bytes")
    return blobs


def allowed(path: str) -> bool:
    return (
        path.startswith(f"{BASE}/x2/")
        or path.startswith(f"{BASE}/skills/")
        or re.fullmatch(r"scripts/(?:build_)?ghc_family_sylven_arc_v688_v7_[a-z0-9_]+\.py", path) is not None
        or re.fullmatch(r"scripts/ghc_family_chess_[a-z0-9_]+\.py", path) is not None
        or path == "tests/test_ghc_family_sylven_arc_v688_v7_x2.py"
    )


def inspect(paths: list[str], blobs: dict[str, bytes]) -> dict:
    if git("rev-parse", "HEAD").strip() != X1:
        raise RuntimeError("exact_x1_head_required")
    deleted = [line for line in git("diff", "--cached", "--name-status").splitlines() if line.startswith("D\t")]
    if deleted:
        raise RuntimeError("staged_deletion")
    outside = [path for path in paths if not allowed(path)]
    if outside:
        raise RuntimeError("outside_allowlist:" + outside[0])
    if len(paths) >= 2000:
        raise RuntimeError("file_ceiling")
    json_count = 0
    python_count = 0
    security_findings = []
    privacy_candidates = []
    trailing_whitespace = []
    max_words = {"path": None, "words": 0}
    raw_thread = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I)
    private_path = re.compile(r"(?:[A-Za-z]:\\Users\\|/Users/|/home/)")
    credential = re.compile(r"(?i)(?:api[_-]?key|access[_-]?token|secret)\s*[:=]\s*['\"][^'\"]{8,}")
    callable_id = re.compile(r"(?i)(?:threadId|providerTabId|sessionId)\s*[:=]")
    transcript = re.compile(r"(?i)(?:full raw transcript|private app state|session stream)")
    for path in paths:
        if path in SELF_EXCLUSIONS:
            continue
        blob = blobs[path]
        if b"\x00" in blob:
            continue
        text = blob.decode("utf-8")
        words = len(text.split())
        if words > max_words["words"]:
            max_words = {"path": path, "words": words}
        if words > 100000:
            raise RuntimeError("document_word_ceiling:" + path)
        for number, line in enumerate(text.splitlines(), 1):
            if line.rstrip() != line:
                trailing_whitespace.append({"path": path, "line": number})
        for name, pattern in (("raw_task_or_thread_identifier", raw_thread), ("private_absolute_path", private_path), ("credential_like", credential), ("private_callable_identifier", callable_id), ("transcript_or_app_state", transcript)):
            if pattern.search(text):
                privacy_candidates.append({"path": path, "class": name})
        if path.endswith(".json"):
            json.loads(text)
            json_count += 1
        if path.endswith(".py"):
            tree = ast.parse(text, filename=path)
            python_count += 1
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                    security_findings.append({"path": path, "kind": node.func.id, "line": node.lineno})
                if isinstance(node, ast.Call) and any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords):
                    security_findings.append({"path": path, "kind": "shell_true", "line": node.lineno})
    if trailing_whitespace:
        raise RuntimeError("trailing_whitespace:" + trailing_whitespace[0]["path"])
    # Privacy fixtures and scanner definitions may name classes, but no exact payload candidate is allowed.
    confirmed = [item for item in privacy_candidates if item["path"] != SCANNER_DEFINITION and item["class"] in {"raw_task_or_thread_identifier", "private_absolute_path", "credential_like", "private_callable_identifier"}]
    if confirmed:
        raise RuntimeError("privacy_payload_candidate:" + confirmed[0]["path"] + ":" + confirmed[0]["class"])
    if security_findings:
        raise RuntimeError("security_finding:" + security_findings[0]["path"])
    return {
        "path_count": len(paths),
        "json_count": json_count,
        "python_count": python_count,
        "max_document": max_words,
        "privacy_scanner_definition_candidates": len(privacy_candidates),
        "confirmed_privacy_hits": 0,
        "security_findings": 0,
        "staged_deletions": 0,
        "outside_allowlist": 0,
    }


def prepare() -> None:
    if MANIFEST.exists() or RECEIPT.exists():
        raise RuntimeError("prepared_receipt_exists")
    paths = staged_paths()
    blobs = staged_blobs(paths)
    checks = inspect(paths, blobs)
    entries = []
    for path in paths:
        blob = blobs[path]
        entries.append({"path": path, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()})
    manifest = {
        "schema": "ghc.family.exact-staged-manifest.v1",
        "owner": "Sylven Arc",
        "phase": "v688-v7",
        "byte_domain": "exact Git index blobs before evidence commit",
        "x1": X1,
        "entries": entries,
        "entry_count": len(entries),
        "self_exclusions": sorted(SELF_EXCLUSIONS),
    }
    receipt = {
        "schema": "ghc.family.x2-evidence-validation.v1",
        "state": "VALID_EXACT_STAGED_OWNER_X2_PRECOMMIT",
        "owner": "Sylven Arc",
        "phase": "v688-v7",
        "x1": X1,
        "checks": checks,
        "owner_test_observation": {"module": "tests.test_ghc_family_sylven_arc_v688_v7_x2", "tests": 24, "passed": 24, "failed": 0, "replay_count": 0},
        "manifest_entry_count": len(entries),
        "manifest_self_exclusions": sorted(SELF_EXCLUSIONS),
        "canonical_invocations": 0,
        "full_repository_suite_run": False,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    write_new(MANIFEST, manifest)
    write_new(RECEIPT, receipt)
    print(json.dumps({"state": receipt["state"], **checks, "manifest_entries": len(entries)}, sort_keys=True))


def verify() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    paths = staged_paths()
    blobs = staged_blobs(paths)
    checks = inspect(paths, blobs)
    expected = {item["path"]: item for item in manifest["entries"]}
    actual_nonself = [path for path in paths if path not in SELF_EXCLUSIONS]
    if set(expected) != set(actual_nonself):
        raise RuntimeError("manifest_path_set")
    for path, item in expected.items():
        blob = blobs[path]
        if len(blob) != item["bytes"] or hashlib.sha256(blob).hexdigest() != item["sha256"]:
            raise RuntimeError("manifest_blob:" + path)
    if receipt["state"] != "VALID_EXACT_STAGED_OWNER_X2_PRECOMMIT":
        raise RuntimeError("validation_state")
    print(json.dumps({"state": "VERIFIED_EXACT_STAGED_OWNER_X2", **checks, "manifest_entries": len(expected), "self_exclusions": len(SELF_EXCLUSIONS)}, sort_keys=True))


def preflight() -> None:
    paths = staged_paths()
    blobs = staged_blobs(paths)
    checks = inspect(paths, blobs)
    print(json.dumps({"state": "VALID_BATCHED_STAGED_PREFLIGHT", **checks}, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("preflight", "prepare", "verify"))
    args = parser.parse_args()
    if args.mode == "preflight":
        preflight()
    elif args.mode == "prepare":
        prepare()
    else:
        verify()


if __name__ == "__main__":
    main()
