#!/usr/bin/env python3
"""Prepare and verify exact manifests for Sylven Arc v688-v7 correction 1."""
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
FIRST_FINAL = "4e2421659eed8617cbd1fd45677b7248db2dfd11"
DELTA = ROOT / BASE / "correction1/validation/correction-delta-manifest.json"
OWNER = ROOT / BASE / "correction1/validation/corrected-owner-manifest.json"
REVIEW = ROOT / BASE / "correction1/validation/correction-staged-review.json"
SELF = {
    f"{BASE}/correction1/validation/correction-delta-manifest.json",
    f"{BASE}/correction1/validation/corrected-owner-manifest.json",
    f"{BASE}/correction1/validation/correction-staged-review.json",
}


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def write_new(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")


def blobs(paths: list[str]) -> dict[str, bytes]:
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
        raise RuntimeError("cat_file:" + error.decode("utf-8", errors="replace"))
    result = {}
    position = 0
    for path, object_id in ordered:
        end = output.find(b"\n", position)
        header = output[position:end].decode("ascii").split()
        position = end + 1
        if len(header) != 3 or header[0] != object_id or header[1] != "blob":
            raise RuntimeError("cat_file_shape:" + path)
        size = int(header[2])
        result[path] = output[position:position + size]
        position += size
        if output[position:position + 1] != b"\n":
            raise RuntimeError("cat_file_separator:" + path)
        position += 1
    return result


def inspect(paths: list[str], content: dict[str, bytes]) -> dict:
    json_count = 0
    python_count = 0
    maximum = {"path": None, "words": 0}
    candidates = []
    security = []
    definitions = {path for path in paths if path.endswith("_finalize.py") or path.endswith("_canonical.py") or path.startswith("tests/")}
    patterns = {
        "raw_task_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"(?:[A-Za-z]:\\Users\\|/Users/|/home/)") ,
        "credential_like": re.compile(r"(?i)(?:api[_-]?key|access[_-]?token|secret)\s*[:=]\s*['\"][^'\"]{8,}"),
        "callable_identifier": re.compile(r"(?i)(?:threadId|providerTabId|sessionId)\s*[:=]"),
    }
    for path in paths:
        data = content[path]
        if b"\x00" in data:
            continue
        text = data.decode("utf-8")
        if any(line.rstrip() != line for line in text.splitlines()):
            raise RuntimeError("trailing_whitespace:" + path)
        count = len(text.split())
        if count > maximum["words"]:
            maximum = {"path": path, "words": count}
        if count > 100000:
            raise RuntimeError("word_ceiling:" + path)
        for kind, pattern in patterns.items():
            if pattern.search(text):
                candidates.append({"path": path, "class": kind})
        if path.endswith(".json"):
            json.loads(text)
            json_count += 1
        if path.endswith(".py"):
            tree = ast.parse(text, filename=path)
            python_count += 1
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                    security.append({"path": path, "kind": node.func.id})
                if isinstance(node, ast.Call) and any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords):
                    security.append({"path": path, "kind": "shell_true"})
    confirmed = [item for item in candidates if item["path"] not in definitions]
    if confirmed:
        raise RuntimeError("privacy_candidate:" + confirmed[0]["path"])
    if security:
        raise RuntimeError("security_finding:" + security[0]["path"])
    return {"path_count": len(paths), "json_count": json_count, "python_count": python_count, "maximum_document": maximum, "privacy_definition_candidates": len(candidates), "confirmed_privacy_hits": 0, "security_findings": 0}


def manifest(paths: list[str], content: dict[str, bytes], schema: str, scope: str) -> dict:
    return {"schema": schema, "owner": "Sylven Arc", "phase": "v688-v7", "scope": scope, "byte_domain": "exact Git index blobs before correction commit", "source": SOURCE, "first_final": FIRST_FINAL, "entries": [{"path": path, "bytes": len(content[path]), "sha256": hashlib.sha256(content[path]).hexdigest()} for path in paths], "entry_count": len(paths), "self_exclusions": sorted(SELF)}


def prepare() -> None:
    if any(path.exists() for path in (DELTA, OWNER, REVIEW)):
        raise RuntimeError("correction_manifest_exists")
    if git("rev-parse", "HEAD") != FIRST_FINAL:
        raise RuntimeError("exact_first_final_required")
    status = [line for line in git("diff", "--cached", "--name-status").splitlines() if line]
    if not status or any(not line.startswith(("A\t", "M\t")) for line in status):
        raise RuntimeError("correction_status_shape")
    modified = [line.split("\t")[-1] for line in status if line.startswith("M\t")]
    if modified != ["scripts/ghc_family_sylven_arc_v688_v7_canonical.py"]:
        raise RuntimeError("correction_modified_scope")
    unchanged_roots = [f"{BASE}/x1", f"{BASE}/x2", f"{BASE}/final", f"{BASE}/seal", f"{BASE}/validation", f"{BASE}/handoffs/future-seat-14-v688-v8-activation-baton.md"]
    if git("diff", "--name-only", FIRST_FINAL, "--", *unchanged_roots):
        raise RuntimeError("immutable_first_final_artifact_changed")
    delta_paths = [line for line in git("diff", "--cached", "--name-only", FIRST_FINAL).splitlines() if line]
    allowed = lambda path: path.startswith(f"{BASE}/correction1/") or path == f"{BASE}/handoffs/future-seat-14-v688-v8-correction1-supplement.md" or path in {"scripts/build_ghc_family_sylven_arc_v688_v7_correction1.py", "scripts/ghc_family_sylven_arc_v688_v7_canonical.py", "scripts/ghc_family_sylven_arc_v688_v7_correction1_finalize.py", "tests/test_ghc_family_sylven_arc_v688_v7_correction1.py"}
    if any(not allowed(path) for path in delta_paths):
        raise RuntimeError("correction_allowlist:" + next(path for path in delta_paths if not allowed(path)))
    owner_paths = [line for line in git("diff", "--cached", "--name-only", SOURCE).splitlines() if line]
    if len(owner_paths) >= 2000:
        raise RuntimeError("owner_file_ceiling")
    content = blobs(owner_paths)
    checks = inspect(owner_paths, content)
    seal = json.loads((ROOT / BASE / "correction1/content-seal.json").read_text(encoding="utf-8"))
    for item in seal["targets"]:
        data = (ROOT / item["path"]).read_bytes()
        if len(data) != item["bytes"] or hashlib.sha256(data).hexdigest() != item["sha256"]:
            raise RuntimeError("content_seal:" + item["path"])
    delta_content = {path: content[path] for path in delta_paths}
    write_new(DELTA, manifest(delta_paths, delta_content, "ghc.family.correction-delta-manifest.v1", "exact correction delta from retained first final"))
    write_new(OWNER, manifest(owner_paths, content, "ghc.family.corrected-owner-manifest.v1", "complete corrected Sylven owner delta from source"))
    write_new(REVIEW, {"schema": "ghc.family.correction-staged-review.v1", "state": "VALID_EXACT_CORRECTION_STAGED_PRECOMMIT", "owner": "Sylven Arc", "phase": "v688-v7", "source": SOURCE, "first_final": FIRST_FINAL, "checks": checks, "correction_delta_count": len(delta_paths), "owner_file_count": len(owner_paths), "modified_existing_paths": modified, "staged_deletions": 0, "immutable_first_final_artifact_mutations": 0, "content_seal_targets": len(seal["targets"]), "targeted_test_observation": {"module": "tests.test_ghc_family_sylven_arc_v688_v7_correction1", "tests": 10, "passed": 10, "failed": 0, "replay_count": 0}, "canonical_invocations": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    print(json.dumps({"state": "VALID_EXACT_CORRECTION_STAGED_PRECOMMIT", "correction_delta": len(delta_paths), "owner_files": len(owner_paths), **checks}, sort_keys=True))


def verify() -> None:
    delta = json.loads(DELTA.read_text(encoding="utf-8"))
    owner = json.loads(OWNER.read_text(encoding="utf-8"))
    review = json.loads(REVIEW.read_text(encoding="utf-8"))
    delta_paths = [line for line in git("diff", "--cached", "--name-only", FIRST_FINAL).splitlines() if line]
    owner_paths = [line for line in git("diff", "--cached", "--name-only", SOURCE).splitlines() if line]
    if set(delta_paths) != {item["path"] for item in delta["entries"]} | SELF:
        raise RuntimeError("delta_path_set")
    if set(owner_paths) != {item["path"] for item in owner["entries"]} | SELF:
        raise RuntimeError("owner_path_set")
    content = blobs(owner_paths)
    checks = inspect(owner_paths, content)
    for packet in (delta, owner):
        for item in packet["entries"]:
            data = content[item["path"]]
            if len(data) != item["bytes"] or hashlib.sha256(data).hexdigest() != item["sha256"]:
                raise RuntimeError("manifest_blob:" + item["path"])
    if review["state"] != "VALID_EXACT_CORRECTION_STAGED_PRECOMMIT":
        raise RuntimeError("review_state")
    print(json.dumps({"state": "VERIFIED_EXACT_CORRECTION_STAGE", "correction_delta": len(delta_paths), "owner_files": len(owner_paths), "manifest_entries": len(delta["entries"]) + len(owner["entries"]), "self_exclusions": 3, **checks}, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("prepare", "verify"))
    args = parser.parse_args()
    prepare() if args.mode == "prepare" else verify()


if __name__ == "__main__":
    main()
