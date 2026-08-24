#!/usr/bin/env python3
"""Review the exact staged Vesper v668-v1-r2 owner delta."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PHASE_PREFIX = "docs/vesper-arlen/v668-v1-r2/"
TEXT_SUFFIXES = {".json", ".md", ".txt", ".html", ".py", ".toml", ".yaml", ".yml", ".mjs", ".js"}
PRIVACY_CLASSES = {
    "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.IGNORECASE),
    "credential_or_token_assignment": re.compile(r"(?i)\b(?:api[_-]?key|password|secret|bearer|token)\b\s*[:=]\s*['\"][^'\"]{8,}"),
    "private_absolute_local_path": re.compile(r"\b[A-Za-z]:[\\/](?!/)"),
    "private_conversation_or_route_material": re.compile(r"(?i)\b(?:source_thread_id|codex_delegation|resume_value|raw_task_id)\b"),
    "private_callable_or_app_state": re.compile(r"(?i)\b(?:private_callable_identifier|private_app_state|session_stream_payload)\b"),
}


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", "-C", str(ROOT), *args], check=check, capture_output=True)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def staged_bytes(path: str) -> bytes:
    return git("show", f":{path}").stdout


def allowed(path: str) -> bool:
    if path.startswith(PHASE_PREFIX):
        return True
    name = Path(path).name
    return path.startswith("scripts/") and "v668_v1_r2" in name or path.startswith("tests/") and "v668_v1_r2" in name


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()

    source = git("rev-parse", f"{args.source}^{{commit}}").stdout.decode().strip()
    name_status = git("diff", "--cached", "--name-status", source).stdout.decode("utf-8", errors="replace").splitlines()
    staged = []
    deletions = []
    for line in name_status:
        if not line:
            continue
        fields = line.split("\t")
        status = fields[0]
        path = fields[-1].replace("\\", "/")
        staged.append(path)
        if status.startswith("D"):
            deletions.append(path)
    out_of_scope = sorted(path for path in staged if not allowed(path))
    if deletions or out_of_scope:
        raise RuntimeError(f"stage scope violation deletions={deletions} out_of_scope={out_of_scope}")

    json_parsed = 0
    privacy_hits: list[dict[str, str]] = []
    scanner_path = "scripts/ghc_family_vesper_arlen_v668_v1_r2_staged_review.py"
    for path in sorted(staged):
        data = staged_bytes(path)
        suffix = Path(path).suffix.casefold()
        if suffix == ".json":
            json.loads(data.decode("utf-8"))
            json_parsed += 1
        if suffix not in TEXT_SUFFIXES or path == scanner_path:
            continue
        text = data.decode("utf-8", errors="replace")
        for class_name, pattern in PRIVACY_CLASSES.items():
            if pattern.search(text):
                privacy_hits.append({"path": path, "class": class_name})

    manifest_path = f"{PHASE_PREFIX}validation/evidence-content-manifest.json"
    manifest = json.loads(staged_bytes(manifest_path).decode("utf-8"))
    manifest_mismatches: list[dict[str, str]] = []
    for row in manifest["entries"]:
        data = staged_bytes(row["path"])
        if len(data) != row["bytes"] or sha256(data) != row["sha256"]:
            manifest_mismatches.append({"path": row["path"], "reason": "staged blob differs from manifest"})
    expected_exclusions = {
        manifest_path,
        f"{PHASE_PREFIX}validation/evidence-staged-review.json",
    }
    if set(manifest["self_exclusions"]) != expected_exclusions:
        manifest_mismatches.append({"path": manifest_path, "reason": "self-exclusion drift"})

    diff_check = git("diff", "--cached", "--check", check=False)
    materialized = [path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts and "__pycache__" not in path.parts and path.suffix != ".pyc"]
    receipt = {
        "schema": "ghc.family.exact-staged-review.v1",
        "state": "PASS_EXACT_EVIDENCE_STAGE" if not privacy_hits and not manifest_mismatches and diff_check.returncode == 0 else "FAIL_EXACT_EVIDENCE_STAGE",
        "source": source,
        "staged_file_count": len(staged),
        "staged_paths": sorted(staged),
        "deletions": deletions,
        "out_of_scope_paths": out_of_scope,
        "json_parsed": json_parsed,
        "privacy_class_count": len(PRIVACY_CLASSES),
        "privacy_hits": privacy_hits,
        "privacy_hit_count": len(privacy_hits),
        "scanner_policy_definition_exclusions": [scanner_path],
        "manifest_entries_checked": len(manifest["entries"]),
        "manifest_mismatches": manifest_mismatches,
        "diff_check_exit": diff_check.returncode,
        "diff_check_stdout_sha256": sha256(diff_check.stdout),
        "diff_check_stderr_sha256": sha256(diff_check.stderr),
        "materialized_file_count": len(materialized),
        "file_guard": 2000,
        "file_guard_passed": len(materialized) < 2000,
        "boundary": "Exact staged owner-delta review only; not complete privacy, exhaustive security, independent reproduction, or Stage 20 evidence.",
    }
    receipt_path = ROOT / args.receipt
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_bytes(canonical_bytes(receipt))
    print(json.dumps({key: receipt[key] for key in ("state", "staged_file_count", "json_parsed", "privacy_hit_count", "manifest_entries_checked", "materialized_file_count")}, sort_keys=True))
    return 0 if receipt["state"] == "PASS_EXACT_EVIDENCE_STAGE" and receipt["file_guard_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
