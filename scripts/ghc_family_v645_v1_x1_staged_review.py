#!/usr/bin/env python3
"""Review the exact staged Tamar Vey v645-v1 x1-only packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


PHASE = "v645-gmut-thos-v1-x1-x2"
PHASE_ROOT = "docs/tamar-vey/v645-v1/"
SELF_PATH = PHASE_ROOT + "validation/x1-staged-review.json"
FILE_SET_PATH = PHASE_ROOT + "validation/x1-exact-file-set.json"
CONTENT_SEAL_PATH = PHASE_ROOT + "reproduction/x1-content-seal.json"


def git_bytes(repo: Path, *args: str, check: bool = True) -> bytes:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=check,
    ).stdout


def staged_blob(repo: Path, path: str) -> bytes:
    return git_bytes(repo, "show", f":{path}")


def load_staged_json(repo: Path, path: str) -> dict[str, Any]:
    return json.loads(staged_blob(repo, path).decode("utf-8"))


def run(repo: Path) -> dict[str, Any]:
    repo = repo.resolve()
    staged_names = [
        raw.decode("utf-8")
        for raw in git_bytes(repo, "diff", "--cached", "--name-only", "-z").split(b"\0")
        if raw
    ]
    reviewed_names = sorted(name for name in staged_names if name != SELF_PATH)
    file_set = json.loads((repo / FILE_SET_PATH).read_text(encoding="utf-8"))
    expected = set(file_set["expected_files"])
    expected_without_self = expected - {SELF_PATH}
    missing = sorted(expected_without_self - set(reviewed_names))
    extra = sorted(set(reviewed_names) - expected_without_self)

    status_rows = git_bytes(repo, "status", "--porcelain=v1", "--untracked-files=all").decode(
        "utf-8", errors="replace"
    ).splitlines()
    unstaged_rows = [
        row for row in status_rows
        if row[3:].replace("\\", "/") != SELF_PATH
        and (row.startswith("??") or (len(row) > 1 and row[1] not in {" ", "?"}))
    ]

    json_parse_issues: list[str] = []
    json_count = 0
    privacy_patterns = {
        "raw_task_or_thread_uuid": re.compile(
            rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
            re.IGNORECASE,
        ),
        "raw_delegation_markup": re.compile(rb"<(?:codex_delegation|source_thread_id)>", re.IGNORECASE),
        "private_local_path": re.compile(rb"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.IGNORECASE),
        "private_app_uri": re.compile(rb"\b(?:app|plugin)://", re.IGNORECASE),
        "credential_assignment": re.compile(
            rb"\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']",
            re.IGNORECASE,
        ),
        "screenshot_file": re.compile(rb"\bscreenshot\s+\d{4}[-_]\d{2}[-_]\d{2}[^\r\n ]*\.(?:png|jpg|jpeg)\b", re.IGNORECASE),
    }
    privacy_issues: list[dict[str, str]] = []
    lf_entries = 0
    crlf_entries = 0
    for name in reviewed_names:
        payload = staged_blob(repo, name)
        if b"\r\n" in payload:
            crlf_entries += 1
        elif b"\n" in payload:
            lf_entries += 1
        if name.endswith(".json"):
            json_count += 1
            try:
                json.loads(payload.decode("utf-8"))
            except Exception as exc:
                json_parse_issues.append(f"{name}: {type(exc).__name__}")
        for label, pattern in privacy_patterns.items():
            if pattern.search(payload):
                privacy_issues.append({"path": name, "pattern_class": label})

    seal = load_staged_json(repo, CONTENT_SEAL_PATH)
    seal_mismatches: list[str] = []
    for entry in seal["entries"]:
        path = entry["path"]
        try:
            digest = hashlib.sha256(staged_blob(repo, path)).hexdigest()
        except subprocess.CalledProcessError:
            seal_mismatches.append(path + ":missing")
            continue
        if digest != entry["sha256"]:
            seal_mismatches.append(path)

    diff_check = subprocess.run(
        ["git", "diff", "--cached", "--check"],
        cwd=repo,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    no_x2_paths = not any(
        name.endswith("/x2-proposal-ledger.json")
        or name.endswith("/phase-truth.json")
        or name == "scripts/ghc_family_v645_v1_evidence.py"
        for name in reviewed_names
    )
    issues: list[str] = []
    if missing:
        issues.append("missing expected x1 files")
    if extra:
        issues.append("extra staged files")
    if unstaged_rows:
        issues.append("unstaged or untracked files remain")
    if json_parse_issues:
        issues.append("staged JSON parse failure")
    if privacy_issues:
        issues.append("privacy pattern hit")
    if seal_mismatches:
        issues.append("x1 content seal mismatch")
    if diff_check.returncode != 0:
        issues.append("git diff --cached --check failed")
    if not no_x2_paths:
        issues.append("x2 path staged in x1")

    return {
        "schema": "ghc.family.v645-v1.x1-staged-review.v1",
        "phase": PHASE,
        "review_scope": "exact x1-only Git index before the dedicated freeze commit",
        "state": "exact_staged_review",
        "self_receipt_path": SELF_PATH,
        "self_receipt_excluded_from_blob_review": True,
        "expected_file_count": len(expected),
        "staged_file_count": len(expected),
        "reviewed_file_count": len(reviewed_names),
        "missing_expected_files": missing,
        "extra_staged_files": extra,
        "unstaged_file_count": len(unstaged_rows),
        "json_blobs_parsed": json_count,
        "json_parse_issues": json_parse_issues,
        "privacy_pattern_classes": sorted(privacy_patterns),
        "privacy_issues": privacy_issues,
        "content_seal_entry_count": len(seal["entries"]),
        "content_seal_mismatches": seal_mismatches,
        "staged_index_lf_entry_count": lf_entries,
        "staged_index_crlf_entry_count": crlf_entries,
        "diff_check_valid": diff_check.returncode == 0,
        "diff_check_output": diff_check.stdout,
        "no_x2_paths_staged": no_x2_paths,
        "stale_label_review": "Inherited sibling, predecessor-phase, route-order, source, proposal-chain, and retained-negative labels remain historical context. Current owner, phase, primary pillar, canonical branch, and successor are Tamar Vey, v645-v1, Freed ID/CBR Heart, the Tamar canonical branch, and Sylven Arc v645-v2.",
        "full_repository_suite_run": False,
        "full_repository_suite_owner": "Eiren Kestrel only",
        "valid": not issues,
        "issues": issues,
        "boundary": "This exact staged-blob review is x1 workflow evidence, not x2 execution, exhaustive security, complete privacy or accessibility assurance, scientific confirmation, authority, or independent reproduction.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, default=Path(SELF_PATH))
    args = parser.parse_args()
    repo = args.repo.resolve()
    output = args.output if args.output.is_absolute() else repo / args.output
    result = run(repo)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    keys = (
        "valid", "expected_file_count", "staged_file_count", "reviewed_file_count",
        "json_blobs_parsed", "content_seal_entry_count", "privacy_issues", "issues",
    )
    print(json.dumps({key: result[key] for key in keys}, ensure_ascii=False))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
