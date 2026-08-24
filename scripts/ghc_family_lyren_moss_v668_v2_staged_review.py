#!/usr/bin/env python3
"""Exact staged-final review for Lyren Moss v668-v2; writes no artifacts."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs/lyren-moss/v668-v2"
EXPECTED_PARENT = "6bb6b96b08eb26646c362967f8ed30263d348c15"


def git_text(*args: str, check: bool = True) -> str:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=check,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.strip()


def index_bytes(path: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(ROOT), "show", f":{path}"], check=True, capture_output=True
    ).stdout


def read_index_json(path: str) -> Any:
    return json.loads(index_bytes(path).decode("utf-8"))


def manifest_replay(path: str) -> dict[str, int]:
    manifest = read_index_json(path)
    mismatches = 0
    for row in manifest["entries"]:
        data = index_bytes(row["path"])
        if len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
            mismatches += 1
    if mismatches:
        raise AssertionError(f"{path} has {mismatches} index manifest mismatches")
    return {"entries": len(manifest["entries"]), "mismatches": mismatches}


def privacy_scan(texts: dict[str, str]) -> dict[str, int]:
    joined = "\n".join(texts.values())
    patterns = {
        "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:\\(?:Users|GHC-Archives)\\", re.I),
        "secret_token": re.compile(r"(?:AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)"),
        "raw_route_tag": re.compile(r"<(?:source_thread_id|thread_id|client_thread_id)>|" + "client" + "ThreadId", re.I),
        "personal_email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    }
    hits = {name: len(pattern.findall(joined)) for name, pattern in patterns.items()}
    if any(hits.values()):
        raise AssertionError(f"confirmed bounded privacy candidates: {hits}")
    return hits


def security_scan(python_texts: dict[str, str]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for path, text in python_texts.items():
        tree = ast.parse(text, filename=path)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                findings.append({"path": path, "line": node.lineno, "call": node.func.id})
            if isinstance(node.func, ast.Attribute):
                parts: list[str] = []
                current: ast.AST = node.func
                while isinstance(current, ast.Attribute):
                    parts.append(current.attr)
                    current = current.value
                if isinstance(current, ast.Name):
                    parts.append(current.id)
                name = ".".join(reversed(parts))
                if name in {"os.system", "pickle.loads", "marshal.loads", "yaml.load"}:
                    findings.append({"path": path, "line": node.lineno, "call": name})
            for keyword in node.keywords:
                if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                    findings.append({"path": path, "line": node.lineno, "call": "shell=True"})
    if findings:
        raise AssertionError(f"bounded changed-Python security findings: {findings}")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-parent", default=EXPECTED_PARENT)
    args = parser.parse_args()
    if git_text("rev-parse", "HEAD") != args.expected_parent:
        raise SystemExit("staged review must run before the final commit at exact evidence head")
    if git_text("diff", "--name-only"):
        raise SystemExit("unstaged changes exist during exact staged review")
    staged = git_text("diff", "--cached", "--name-only").splitlines()
    if not staged:
        raise SystemExit("no staged final files")
    allowed_code = {
        "scripts/build_ghc_family_lyren_moss_v668_v2_final.py",
        "scripts/ghc_family_lyren_moss_v668_v2_staged_review.py",
        "scripts/ghc_family_lyren_moss_v668_v2_canonical.py",
        "tests/test_ghc_family_lyren_moss_v668_v2_final.py",
    }
    allowed_doc_prefixes = (
        "docs/lyren-moss/v668-v2/closeout/",
        "docs/lyren-moss/v668-v2/final/",
        "docs/lyren-moss/v668-v2/handoffs/",
        "docs/lyren-moss/v668-v2/validation/",
    )
    allowed_doc_exact = {"docs/lyren-moss/v668-v2/method-flow/method-flow-ledger.json"}
    unexpected = [
        path for path in staged
        if path not in allowed_code
        and path not in allowed_doc_exact
        and not path.startswith(allowed_doc_prefixes)
    ]
    if unexpected:
        raise SystemExit(f"unexpected staged paths: {unexpected}")
    diff_check = subprocess.run(
        ["git", "-C", str(ROOT), "diff", "--cached", "--check"], capture_output=True, text=True
    )
    if diff_check.returncode:
        raise SystemExit(diff_check.stdout + diff_check.stderr)

    final_delta = manifest_replay("docs/lyren-moss/v668-v2/validation/final-delta-manifest.json")
    final_owner = manifest_replay("docs/lyren-moss/v668-v2/validation/final-owner-manifest.json")
    owner_manifest = read_index_json("docs/lyren-moss/v668-v2/validation/final-owner-manifest.json")
    texts: dict[str, str] = {}
    json_parses = 0
    markdown_checks = 0
    python_compiles = 0
    for row in owner_manifest["entries"]:
        path = row["path"]
        data = index_bytes(path)
        text = data.decode("utf-8")
        texts[path] = text
        if path.endswith(".json"):
            json.loads(text)
            json_parses += 1
        elif path.endswith(".md"):
            if not text.strip():
                raise AssertionError(f"empty Markdown file: {path}")
            markdown_checks += 1
        elif path.endswith(".py"):
            compile(text, path, "exec")
            python_compiles += 1
    privacy = privacy_scan(texts)
    python_texts = {path: text for path, text in texts.items() if path.endswith(".py")}
    security = security_scan(python_texts)
    truth = read_index_json("docs/lyren-moss/v668-v2/final/phase-truth.json")
    if set(truth["allowed_outcomes"]) != {"completed", "represented", "open_gap", "exact_gate"}:
        raise AssertionError("truth label drift")
    if truth["outcome_counts"] != {"completed": 28, "exact_gate": 2, "open_gap": 2, "represented": 8}:
        raise AssertionError("outcome count drift")
    route = read_index_json("docs/lyren-moss/v668-v2/closeout/route-and-roster-record.json")
    if route["state"] != "PREPARED_NOT_SENT" or route["successor_contacted"]:
        raise AssertionError("route advanced before terminal")
    if owner_manifest["entry_count"] >= 2000:
        raise AssertionError("owner scope reached rotation ceiling")
    result = {
        "state": "PASS_EXACT_STAGED_FINAL_REVIEW",
        "staged_files": len(staged),
        "final_delta_manifest": final_delta,
        "final_owner_manifest": final_owner,
        "json_parses": json_parses,
        "markdown_checks": markdown_checks,
        "python_compiles": python_compiles,
        "privacy_classes": privacy,
        "bounded_security_findings": len(security),
        "route": "PREPARED_NOT_SENT",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
