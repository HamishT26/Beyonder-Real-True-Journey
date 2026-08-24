#!/usr/bin/env python3
"""Exact pre-commit staged review for Ilyra Fen v668-v3 final closeout."""

from __future__ import annotations

import ast
import hashlib
import json
import pathlib
import re
import subprocess
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[1]
PHASE_PREFIX = "docs/ilyra-fen/v668-v3/"
SOURCE_FINAL = "da0d852ccacbfc228f7257888691b809a280ad86"
X1_HEAD = "c9cde9ebf7f39c7a3b4b4cf4775fd9426bba4e52"
EVIDENCE_HEAD = "a22360acce1a200ef852a97110cc8da12497775b"
OWNER_MANIFEST = f"{PHASE_PREFIX}validation/final-owner-manifest.json"
DELTA_MANIFEST = f"{PHASE_PREFIX}validation/final-delta-manifest.json"


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=check)


def git_text(*args: str) -> str:
    return run_git(*args).stdout.decode("utf-8").strip()


def git_bytes(*args: str) -> bytes:
    return run_git(*args).stdout


def index_bytes(path: str) -> bytes:
    return git_bytes("show", f":{path}")


def read_index_json(path: str) -> Any:
    return json.loads(index_bytes(path))


def index_has(path: str) -> bool:
    return run_git("cat-file", "-e", f":{path}", check=False).returncode == 0


def replay_manifest(manifest_path: str, *, owner: bool) -> dict[str, int]:
    manifest = read_index_json(manifest_path)
    mismatches = 0
    for row in manifest["entries"]:
        if index_has(row["path"]):
            data = index_bytes(row["path"])
            oid = git_text("rev-parse", f":{row['path']}")
        elif owner:
            data = git_bytes("show", f"{EVIDENCE_HEAD}:{row['path']}")
            oid = git_text("rev-parse", f"{EVIDENCE_HEAD}:{row['path']}")
        else:
            raise AssertionError(f"delta manifest path not staged: {row['path']}")
        observed = {"git_blob_oid": oid, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
        expected = {key: row[key] for key in observed}
        if observed != expected:
            mismatches += 1
    return {"entries": len(manifest["entries"]), "mismatches": mismatches}


def replay_committed_manifest(commit: str, manifest_path: str) -> dict[str, int]:
    manifest = json.loads(git_bytes("show", f"{commit}:{manifest_path}"))
    mismatches = 0
    for row in manifest["entries"]:
        data = git_bytes("show", f"{commit}:{row['path']}")
        if hashlib.sha256(data).hexdigest() != row["sha256"] or len(data) != row["bytes"]:
            mismatches += 1
    return {"entries": len(manifest["entries"]), "mismatches": mismatches}


def privacy_patterns() -> list[re.Pattern[bytes]]:
    route_key = b"source_" + b"thread_id" + rb"\s*[:=]"
    route_tag = b"<codex_" + b"delegation>"
    session_key = b"session_meta" + rb"\.payload\.id"
    response_key = b"response" + b"_item"
    return [
        re.compile(b"-----BEGIN " + rb"(?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        re.compile(route_key, re.I),
        re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        re.compile(rb"\b[A-Z]:\\Users\\[^\s\"']+", re.I),
        re.compile(route_tag + b"|" + session_key + b"|" + response_key, re.I),
        re.compile(rb"\b(?:ssn|medical record number|patient identifier|participant identifier)\s*[:=]\s*\S+", re.I),
    ]


def security_findings(python_texts: dict[str, str]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for path, text in python_texts.items():
        tree = ast.parse(text, filename=path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec", "compile"}:
                findings.append({"path": path, "line": node.lineno, "kind": node.func.id})
            if isinstance(node, ast.Call):
                for keyword in node.keywords:
                    if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                        findings.append({"path": path, "line": node.lineno, "kind": "explicit_shell"})
    return findings


def main() -> int:
    if git_text("rev-parse", "HEAD") != EVIDENCE_HEAD:
        raise AssertionError("staged final must be reviewed at exact immutable evidence parent")
    staged = [part.decode("utf-8") for part in git_bytes("diff", "--cached", "--name-only", "-z").split(b"\0") if part]
    unstaged = git_text("diff", "--name-only")
    if unstaged:
        raise AssertionError(f"unstaged tracked paths present: {unstaged}")
    delta = read_index_json(DELTA_MANIFEST)
    owner = read_index_json(OWNER_MANIFEST)
    if len(staged) != delta["entry_count"] + 2:
        raise AssertionError(f"staged count {len(staged)} does not equal delta plus two manifests")
    allowed_scripts = {
        "scripts/build_ghc_family_ilyra_fen_v668_v3_final.py",
        "scripts/ghc_family_ilyra_fen_v668_v3_staged_review.py",
        "scripts/ghc_family_ilyra_fen_v668_v3_canonical.py",
        "tests/test_ghc_family_ilyra_fen_v668_v3_final.py",
    }
    allowed_doc_roots = (
        f"{PHASE_PREFIX}closeout/",
        f"{PHASE_PREFIX}final/",
        f"{PHASE_PREFIX}handoffs/",
        f"{PHASE_PREFIX}route/",
        f"{PHASE_PREFIX}seal/",
        f"{PHASE_PREFIX}validation/",
    )
    allowed_doc_exact = {f"{PHASE_PREFIX}method-flow/final-operational.json"}
    out_of_scope = [path for path in staged if path not in allowed_scripts and path not in allowed_doc_exact and not path.startswith(allowed_doc_roots)]
    if out_of_scope:
        raise AssertionError(f"out-of-scope final paths: {out_of_scope}")
    if any("/x1/" in path or "/x2/" in path for path in staged):
        raise AssertionError("x1 or x2 path mixed into final delta")
    if git_text("diff", "--cached", "--check"):
        raise AssertionError("cached diff hygiene reported output")
    delta_replay = replay_manifest(DELTA_MANIFEST, owner=False)
    owner_replay = replay_manifest(OWNER_MANIFEST, owner=True)
    if delta_replay["mismatches"] or owner_replay["mismatches"]:
        raise AssertionError({"delta": delta_replay, "owner": owner_replay})
    x1_replay = replay_committed_manifest(X1_HEAD, f"{PHASE_PREFIX}x1/x1-manifest.json")
    evidence_replay = replay_committed_manifest(EVIDENCE_HEAD, f"{PHASE_PREFIX}x2/evidence/evidence-content-manifest.json")
    if x1_replay["mismatches"] or evidence_replay["mismatches"]:
        raise AssertionError({"x1": x1_replay, "evidence": evidence_replay})

    json_count = 0
    markdown_count = 0
    privacy_hits: list[dict[str, Any]] = []
    oversized: list[dict[str, Any]] = []
    python_texts: dict[str, str] = {}
    patterns = privacy_patterns()
    for path in staged:
        data = index_bytes(path)
        suffix = pathlib.PurePosixPath(path).suffix.lower()
        if suffix == ".json":
            json.loads(data)
            json_count += 1
        if suffix == ".md":
            markdown_count += 1
        if suffix in {".json", ".md", ".txt", ".html", ".py"}:
            text = data.decode("utf-8")
            for class_id, pattern in enumerate(patterns, 1):
                if pattern.search(data):
                    privacy_hits.append({"path": path, "class": class_id})
            words = len(re.findall(r"\b\w+[\w'-]*\b", text))
            if words > 6000:
                oversized.append({"path": path, "words": words})
        if suffix == ".py":
            python_texts[path] = data.decode("utf-8")
    if privacy_hits:
        raise AssertionError(f"confirmed staged privacy candidates: {privacy_hits}")
    if oversized:
        raise AssertionError(f"oversized staged documents: {oversized}")
    findings = security_findings(python_texts)
    if findings:
        raise AssertionError(f"bounded changed-code security findings: {findings}")
    materialized = sum(1 for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts)
    if materialized >= 2000:
        raise AssertionError(f"materialized file ceiling exceeded: {materialized}")
    print(json.dumps({
        "state": "FINAL_EXACT_STAGED_REVIEW_PASS",
        "staged_paths": len(staged),
        "delta_manifest": delta_replay,
        "owner_manifest": owner_replay,
        "x1_manifest": x1_replay,
        "evidence_manifest": evidence_replay,
        "strict_json_parses": json_count,
        "markdown_checks": markdown_count,
        "python_ast_checks": len(python_texts),
        "confirmed_privacy_hits": len(privacy_hits),
        "security_findings": len(findings),
        "oversized_documents": len(oversized),
        "materialized_files": materialized,
        "out_of_scope": len(out_of_scope),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
