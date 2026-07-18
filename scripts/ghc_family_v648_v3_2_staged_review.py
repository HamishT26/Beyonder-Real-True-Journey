#!/usr/bin/env python3
"""Exact Git-index review for Eiren Kestrel v648-v3 repeat lifecycle commits."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE_PREFIX = "docs/eiren-kestrel/v648-v3-2/"
SCRIPT_MARKERS = ("ghc_family_v648_v3_2", "build_ghc_family_v648_v3_2")
TEST_PREFIX = "tests/test_ghc_family_v648_v3_2"
PATTERNS = {
    "raw_task_or_thread_id": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
    "private_absolute_path": re.compile(rb"(?:[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b|/(?:Users|home)/)", re.I),
    "credential_or_private_key": re.compile(rb"\b(?:sk-[A-Za-z0-9_-]{20,}|gh[opusr]_[A-Za-z0-9]{20,}|BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY)\b"),
    "private_session_or_route": re.compile(rb"(?i)(?:source_thread_id|rollout_path|session_meta\.payload\.id|(?:thread|app|plugin)://)"),
    "private_callable_identifier": re.compile(rb"(?i)(?:mcp__|codex_app__send_message_to_thread)"),
}
SCANNER_DEFINITIONS = {
    "scripts/build_ghc_family_v648_v3_2_preregistration.py",
    "scripts/ghc_family_v648_v3_2_staged_review.py",
    "scripts/ghc_family_v648_v3_2_x1_review.py",
}


def git_text(*args: str) -> str:
    return subprocess.run(["git", "-C", str(ROOT), *args], check=True, capture_output=True, text=True, encoding="utf-8").stdout


def index_bytes(path: str) -> bytes:
    return subprocess.run(["git", "-C", str(ROOT), "show", f":{path}"], check=True, capture_output=True).stdout


def write(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def allowed(path: str) -> bool:
    return path.startswith(PHASE_PREFIX) or (path.startswith("scripts/") and any(marker in path for marker in SCRIPT_MARKERS)) or path.startswith(TEST_PREFIX)


def repository_relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lifecycle", choices=["x1", "evidence", "final"], required=True)
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--privacy", type=Path, required=True)
    args = parser.parse_args()

    staged = [row for row in git_text("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if row]
    outputs = {repository_relative(args.review), repository_relative(args.manifest), repository_relative(args.privacy)}
    manifest_paths = [path for path in staged if path not in outputs]
    unexpected = [path for path in staged if not allowed(path)]
    x1_contamination = []
    if args.lifecycle == "x1":
        for path in staged:
            name = Path(path).name
            if name.startswith("x2-") or name in {"evidence-receipt.json", "closeout-receipt.json", "seal-receipt.json", "final-validation-record.json"}:
                x1_contamination.append(path)

    entries = []
    json_parsed = 0
    candidates = []
    confirmed = []
    for path in manifest_paths:
        blob = index_bytes(path)
        entries.append({"path": path, "sha256": hashlib.sha256(blob).hexdigest(), "bytes": len(blob)})
        if path.endswith(".json"):
            json.loads(blob.decode("utf-8"))
            json_parsed += 1
        for class_name, pattern in PATTERNS.items():
            if pattern.search(blob):
                candidate = {"path": path, "class": class_name, "disposition": "scanner_definition" if path in SCANNER_DEFINITIONS else "confirmed_payload_hit"}
                candidates.append(candidate)
                if path not in SCANNER_DEFINITIONS:
                    confirmed.append(candidate)

    diff_check = subprocess.run(["git", "-C", str(ROOT), "diff", "--cached", "--check"], capture_output=True, text=True, encoding="utf-8")
    valid = bool(staged) and not unexpected and not x1_contamination and not confirmed and diff_check.returncode == 0
    write(args.manifest, {
        "schema": f"ghc.family.v648-v3-r2.{args.lifecycle}-staged-manifest.v1",
        "lifecycle": args.lifecycle,
        "self_exclusions": sorted(outputs),
        "entry_count": len(entries),
        "entries": entries,
        "hash_domain": "sha256 of exact Git-index blob bytes",
    })
    write(args.privacy, {
        "schema": f"ghc.family.v648-v3-r2.{args.lifecycle}-privacy-scan.v1",
        "classes": sorted(PATTERNS),
        "files_scanned": len(manifest_paths),
        "candidate_count": len(candidates),
        "confirmed_hit_count": len(confirmed),
        "candidates": candidates,
        "confirmed_hits": confirmed,
        "boundary": "A zero confirmed-hit structural scan is not complete privacy assurance.",
    })
    write(args.review, {
        "schema": f"ghc.family.v648-v3-r2.{args.lifecycle}-staged-review.v1",
        "valid": valid,
        "lifecycle": args.lifecycle,
        "staged_file_count": len(staged),
        "manifest_entry_count": len(entries),
        "json_parsed": json_parsed,
        "unexpected_paths": unexpected,
        "x1_contamination": x1_contamination,
        "privacy_confirmed_hits": len(confirmed),
        "diff_hygiene_pass": diff_check.returncode == 0,
        "diff_hygiene_output": diff_check.stdout.strip() or diff_check.stderr.strip(),
        "exact_staged_paths": staged,
    })
    print(json.dumps({"valid": valid, "staged": len(staged), "manifest": len(entries), "json": json_parsed, "confirmed": len(confirmed)}, sort_keys=True))
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
