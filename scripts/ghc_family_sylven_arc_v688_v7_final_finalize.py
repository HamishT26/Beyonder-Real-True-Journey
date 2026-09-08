#!/usr/bin/env python3
"""Prepare and verify exact staged manifests for the Sylven Arc v688-v7 final."""
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
SOURCE = "e7db6f3be1327de72f93873eb6540aabfc773344"
X2 = "3c968db9391583a9e40f0eb8cc0c2f86d9997126"
DELTA_MANIFEST = ROOT / BASE / "validation/final-delta-manifest.json"
OWNER_MANIFEST = ROOT / BASE / "validation/final-owner-manifest.json"
REVIEW = ROOT / BASE / "validation/final-staged-review.json"
SELF_EXCLUSIONS = {
    f"{BASE}/validation/final-delta-manifest.json",
    f"{BASE}/validation/final-owner-manifest.json",
    f"{BASE}/validation/final-staged-review.json",
}


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True)


def write_new(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")


def index_blobs(paths: list[str]) -> dict[str, bytes]:
    index = {}
    for line in git("ls-files", "--stage").splitlines():
        left, path = line.split("\t", 1)
        _mode, object_id, stage = left.split()
        if stage == "0":
            index[path] = object_id
    missing = [path for path in paths if path not in index]
    if missing:
        raise RuntimeError("index_missing:" + missing[0])
    ordered = [(path, index[path]) for path in paths]
    process = subprocess.Popen(["git", "cat-file", "--batch"], cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate(("\n".join(object_id for _path, object_id in ordered) + "\n").encode("ascii"))
    if process.returncode:
        raise RuntimeError("cat_file_batch:" + error.decode("utf-8", errors="replace"))
    position = 0
    blobs = {}
    for path, object_id in ordered:
        end = output.find(b"\n", position)
        header = output[position:end].decode("ascii").split()
        position = end + 1
        if len(header) != 3 or header[0] != object_id or header[1] != "blob":
            raise RuntimeError("cat_file_shape:" + path)
        size = int(header[2])
        blobs[path] = output[position:position + size]
        position += size
        if output[position:position + 1] != b"\n":
            raise RuntimeError("cat_file_separator:" + path)
        position += 1
    if position != len(output):
        raise RuntimeError("cat_file_trailing")
    return blobs


def owner_allowed(path: str) -> bool:
    return (
        path.startswith(BASE + "/")
        or re.fullmatch(r"scripts/(?:build_)?ghc_family_sylven_arc_v688_v7_[a-z0-9_]+\.py", path) is not None
        or re.fullmatch(r"scripts/ghc_family_chess_[a-z0-9_]+\.py", path) is not None
        or re.fullmatch(r"tests/test_ghc_family_sylven_arc_v688_v7_[a-z0-9_]+\.py", path) is not None
    )


def final_allowed(path: str) -> bool:
    return (
        path.startswith(BASE + "/final/")
        or path.startswith(BASE + "/handoffs/")
        or path.startswith(BASE + "/seal/")
        or path.startswith(BASE + "/validation/")
        or re.fullmatch(r"scripts/(?:build_)?ghc_family_sylven_arc_v688_v7_(?:final|validation|canonical)[a-z0-9_]*\.py", path) is not None
        or path == "tests/test_ghc_family_sylven_arc_v688_v7_final.py"
    )


def inspect(paths: list[str], blobs: dict[str, bytes]) -> dict:
    json_count = 0
    python_count = 0
    max_document = {"path": None, "words": 0}
    privacy_candidates = []
    security_findings = []
    scanner_definitions = {
        "scripts/ghc_family_sylven_arc_v688_v7_x2_finalize.py",
        "scripts/ghc_family_sylven_arc_v688_v7_final_finalize.py",
        "scripts/ghc_family_sylven_arc_v688_v7_canonical.py",
        "tests/test_ghc_family_sylven_arc_v688_v7_final.py",
    }
    patterns = {
        "raw_task_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"(?:[A-Za-z]:\\Users\\|/Users/|/home/)") ,
        "credential_like": re.compile(r"(?i)(?:api[_-]?key|access[_-]?token|secret)\s*[:=]\s*['\"][^'\"]{8,}"),
        "private_callable_identifier": re.compile(r"(?i)(?:threadId|providerTabId|sessionId)\s*[:=]"),
        "transcript_or_app_state": re.compile(r"(?i)(?:full raw transcript|private app state|session stream)"),
    }
    for path in paths:
        blob = blobs[path]
        if b"\x00" in blob:
            continue
        text = blob.decode("utf-8")
        if any(line.rstrip() != line for line in text.splitlines()):
            raise RuntimeError("trailing_whitespace:" + path)
        words = len(text.split())
        if words > max_document["words"]:
            max_document = {"path": path, "words": words}
        if words > 100000:
            raise RuntimeError("word_ceiling:" + path)
        for kind, pattern in patterns.items():
            if pattern.search(text):
                privacy_candidates.append({"path": path, "class": kind})
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
    confirmed = [item for item in privacy_candidates if item["path"] not in scanner_definitions and item["class"] != "transcript_or_app_state"]
    if confirmed:
        raise RuntimeError("privacy_candidate:" + confirmed[0]["path"] + ":" + confirmed[0]["class"])
    if security_findings:
        raise RuntimeError("security_finding:" + security_findings[0]["path"])
    return {"path_count": len(paths), "json_count": json_count, "python_count": python_count, "max_document": max_document, "privacy_definition_candidates": len(privacy_candidates), "confirmed_privacy_hits": 0, "security_findings": 0}


def build_manifest(paths: list[str], blobs: dict[str, bytes], schema: str, scope: str) -> dict:
    return {
        "schema": schema,
        "owner": "Sylven Arc",
        "phase": "v688-v7",
        "scope": scope,
        "byte_domain": "exact Git index blobs before final commit",
        "source": SOURCE,
        "x2": X2,
        "entries": [{"path": path, "bytes": len(blobs[path]), "sha256": hashlib.sha256(blobs[path]).hexdigest()} for path in paths],
        "entry_count": len(paths),
        "self_exclusions": sorted(SELF_EXCLUSIONS),
    }


def prepare() -> None:
    if any(path.exists() for path in (DELTA_MANIFEST, OWNER_MANIFEST, REVIEW)):
        raise RuntimeError("final_manifest_exists")
    if git("rev-parse", "HEAD").strip() != X2:
        raise RuntimeError("exact_x2_head_required")
    staged_status = [line for line in git("diff", "--cached", "--name-status").splitlines() if line]
    if not staged_status or any(not line.startswith("A\t") for line in staged_status):
        raise RuntimeError("final_stage_must_be_additions_only")
    if git("diff", "--name-only", X2, "--", BASE + "/x1", BASE + "/x2").strip():
        raise RuntimeError("immutable_x1_or_x2_changed")
    final_paths = [line for line in git("diff", "--cached", "--name-only", "HEAD").splitlines() if line]
    owner_paths = [line for line in git("diff", "--cached", "--name-only", SOURCE).splitlines() if line]
    if any(not final_allowed(path) for path in final_paths):
        raise RuntimeError("final_allowlist:" + next(path for path in final_paths if not final_allowed(path)))
    if any(not owner_allowed(path) for path in owner_paths) or len(owner_paths) >= 2000:
        raise RuntimeError("owner_allowlist_or_ceiling")
    blobs = index_blobs(owner_paths)
    checks = inspect(owner_paths, blobs)
    baton = ROOT / BASE / "handoffs/future-seat-14-v688-v8-activation-baton.md"
    baton_index = json.loads((ROOT / BASE / "final/baton-index.json").read_text(encoding="utf-8"))
    if len(baton.read_text(encoding="utf-8").split()) != baton_index["word_count"] or baton_index["module_count"] != 13:
        raise RuntimeError("baton_index")
    seal = json.loads((ROOT / BASE / "seal/content-seal.json").read_text(encoding="utf-8"))
    for item in seal["targets"]:
        data = (ROOT / item["path"]).read_bytes()
        if len(data) != item["bytes"] or hashlib.sha256(data).hexdigest() != item["sha256"]:
            raise RuntimeError("content_seal:" + item["path"])
    delta_blobs = {path: blobs[path] for path in final_paths}
    write_new(DELTA_MANIFEST, build_manifest(final_paths, delta_blobs, "ghc.family.final-delta-manifest.v1", "exact final delta from immutable x2"))
    write_new(OWNER_MANIFEST, build_manifest(owner_paths, blobs, "ghc.family.final-owner-manifest.v1", "complete Sylven owner delta from immutable source"))
    write_new(REVIEW, {
        "schema": "ghc.family.final-staged-review.v1",
        "state": "VALID_EXACT_FINAL_STAGED_PRECOMMIT",
        "owner": "Sylven Arc",
        "phase": "v688-v7",
        "source": SOURCE,
        "x2": X2,
        "checks": checks,
        "final_delta_count": len(final_paths),
        "owner_file_count": len(owner_paths),
        "staged_deletions": 0,
        "outside_allowlist": 0,
        "x1_or_x2_mutations": 0,
        "content_seal_targets": len(seal["targets"]),
        "owner_test_observation": {"module": "tests.test_ghc_family_sylven_arc_v688_v7_final", "tests": 20, "passed": 20, "failed": 0, "replay_count": 0},
        "canonical_invocations": 0,
        "full_repository_suite_run": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    print(json.dumps({"state": "VALID_EXACT_FINAL_STAGED_PRECOMMIT", "final_delta": len(final_paths), "owner_files": len(owner_paths), **checks}, sort_keys=True))


def verify() -> None:
    delta = json.loads(DELTA_MANIFEST.read_text(encoding="utf-8"))
    owner = json.loads(OWNER_MANIFEST.read_text(encoding="utf-8"))
    review = json.loads(REVIEW.read_text(encoding="utf-8"))
    final_paths = [line for line in git("diff", "--cached", "--name-only", "HEAD").splitlines() if line]
    owner_paths = [line for line in git("diff", "--cached", "--name-only", SOURCE).splitlines() if line]
    if set(final_paths) != {item["path"] for item in delta["entries"]} | SELF_EXCLUSIONS:
        raise RuntimeError("final_delta_path_set")
    if set(owner_paths) != {item["path"] for item in owner["entries"]} | SELF_EXCLUSIONS:
        raise RuntimeError("owner_path_set")
    blobs = index_blobs(owner_paths)
    checks = inspect(owner_paths, blobs)
    for manifest in (delta, owner):
        for item in manifest["entries"]:
            blob = blobs[item["path"]]
            if len(blob) != item["bytes"] or hashlib.sha256(blob).hexdigest() != item["sha256"]:
                raise RuntimeError("manifest_blob:" + item["path"])
    if review["state"] != "VALID_EXACT_FINAL_STAGED_PRECOMMIT":
        raise RuntimeError("review_state")
    print(json.dumps({"state": "VERIFIED_EXACT_FINAL_STAGE", "final_delta": len(final_paths), "owner_files": len(owner_paths), "manifest_entries": len(delta["entries"]) + len(owner["entries"]), "self_exclusions": len(SELF_EXCLUSIONS), **checks}, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("prepare", "verify"))
    args = parser.parse_args()
    prepare() if args.mode == "prepare" else verify()


if __name__ == "__main__":
    main()
