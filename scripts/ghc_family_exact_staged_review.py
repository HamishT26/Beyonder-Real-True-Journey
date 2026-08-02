#!/usr/bin/env python3
"""Review an exact staged lifecycle surface without phase-specific mutation.

The runner reads Git-index blobs, not checkout bytes, so Windows line-ending
conversion cannot silently change the review domain.  It writes only the
explicit receipt path supplied by the caller.  A passing receipt is bounded
same-owner workflow evidence, never privacy completeness, exhaustive security,
independent reproduction, production certification, or authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


PRIVACY_PATTERNS = {
    "raw_uuid": re.compile(
        rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
        re.I,
    ),
    "private_absolute_path": re.compile(rb"\b[A-Za-z]:[\\/]"),
    "credential": re.compile(
        rb"(?:(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}|"
        rb"(?<![A-Za-z0-9])ghp_[A-Za-z0-9]{20,}|"
        rb"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY)"
    ),
    "private_route_identifier": re.compile(
        rb"(?:thread_id|task_id|agent_id|resume_token|private_callable)[\"']?\s*[:=]\s*[\"']?"
        rb"(?!(?:V\d|false\b|true\b|null\b|\[REDACTED_SECRET\]))[A-Za-z0-9_-]{24,}",
        re.I,
    ),
    "transcript_or_session": re.compile(
        rb"(?:raw transcript|session stream|private app state)", re.I
    ),
}


def run_git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=check,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def staged_paths(repo: Path) -> list[str]:
    result = run_git(repo, "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z")
    return sorted(
        part.decode("utf-8")
        for part in result.stdout.split(b"\0")
        if part
    )


def staged_blob(repo: Path, path: str) -> bytes:
    return run_git(repo, "show", f":{path}").stdout


def clean_domain(payload: bytes) -> bytes:
    return payload.replace(b"\r\n", b"\n")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--phase-root", required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--candidate-receipt", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--owner", required=True)
    parser.add_argument("--phase", required=True)
    parser.add_argument("--lifecycle", required=True)
    args = parser.parse_args()

    repo = args.repo.resolve()
    manifest_path = (repo / args.manifest).resolve() if not args.manifest.is_absolute() else args.manifest
    candidate_path = (
        (repo / args.candidate_receipt).resolve()
        if not args.candidate_receipt.is_absolute()
        else args.candidate_receipt
    )
    receipt_path = (repo / args.receipt).resolve() if not args.receipt.is_absolute() else args.receipt
    for path in (manifest_path, candidate_path, receipt_path):
        if repo != path and repo not in path.parents:
            raise SystemExit("all paths must remain within the repository")

    staged = staged_paths(repo)
    candidate = load_json(candidate_path)
    manifest = load_json(manifest_path)
    expected = sorted(candidate["intended_allowlist"])
    exclusions = sorted(
        f"{args.phase_root}/{relative}" for relative in manifest.get("exclusions", [])
    )

    blobs: dict[str, bytes] = {}
    blob_errors: list[dict[str, str]] = []
    for path in staged:
        try:
            blobs[path] = staged_blob(repo, path)
        except subprocess.CalledProcessError as exc:
            blob_errors.append(
                {"path": path, "error": exc.stderr.decode("utf-8", errors="replace")[:300]}
            )

    json_errors: list[dict[str, str]] = []
    json_parse_count = 0
    privacy_candidates: list[dict[str, str]] = []
    scanner_definition_candidates: list[dict[str, str]] = []
    root_capacity_probe_candidates: list[dict[str, str]] = []
    for path, payload in blobs.items():
        if path.endswith(".json"):
            try:
                json.loads(payload.decode("utf-8"))
                json_parse_count += 1
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                json_errors.append({"path": path, "error": str(exc)})
        for label, pattern in PRIVACY_PATTERNS.items():
            if pattern.search(payload):
                row = {"path": path, "class": label}
                is_scanner_definition = (
                    path.startswith("scripts/")
                    and label == "transcript_or_session"
                    and b"raw transcript|session stream|private app state" in payload
                    and (b"PRIVACY_PATTERNS" in payload or b"def privacy_scan" in payload)
                )
                decoded_lines = payload.decode("utf-8", errors="replace").splitlines()
                matched_path_lines = [
                    line for line in decoded_lines
                    if PRIVACY_PATTERNS["private_absolute_path"].search(line.encode("utf-8"))
                ]
                is_root_capacity_probe = (
                    label == "private_absolute_path"
                    and bool(matched_path_lines)
                    and all(
                        'shutil.disk_usage("' in line and ':\\\\")' in line
                        for line in matched_path_lines
                    )
                )
                if is_scanner_definition:
                    scanner_definition_candidates.append(row)
                elif is_root_capacity_probe:
                    root_capacity_probe_candidates.append(row)
                else:
                    privacy_candidates.append(row)

    manifest_mismatches: list[dict[str, Any]] = []
    for row in manifest["entries"]:
        path = row["path"]
        payload = blobs.get(path)
        if payload is None:
            manifest_mismatches.append({"path": path, "reason": "missing_staged_blob"})
            continue
        normalized = clean_domain(payload)
        observed_hash = hashlib.sha256(normalized).hexdigest()
        observed_bytes = len(normalized)
        if observed_hash != row["sha256"] or observed_bytes != row["bytes"]:
            manifest_mismatches.append(
                {
                    "path": path,
                    "reason": "hash_or_size_mismatch",
                    "expected_sha256": row["sha256"],
                    "observed_sha256": observed_hash,
                    "expected_bytes": row["bytes"],
                    "observed_bytes": observed_bytes,
                }
            )

    diff_check = run_git(repo, "diff", "--cached", "--check", check=False)
    allowlist_missing = sorted(set(expected) - set(staged))
    allowlist_unexpected = sorted(set(staged) - set(expected))
    manifest_paths = {row["path"] for row in manifest["entries"]}
    coverage_missing = sorted(set(staged) - set(exclusions) - manifest_paths)
    coverage_extra = sorted(manifest_paths - set(staged))
    issues: list[str] = []
    if allowlist_missing or allowlist_unexpected:
        issues.append("staged_allowlist")
    if blob_errors:
        issues.append("staged_blob_read")
    if json_errors:
        issues.append("staged_json_parse")
    if privacy_candidates:
        issues.append("privacy_candidates_require_adjudication")
    if manifest_mismatches or coverage_missing or coverage_extra:
        issues.append("manifest_parity")
    if diff_check.returncode != 0:
        issues.append("diff_hygiene")

    receipt = {
        "schema": "ghc.family.exact-staged-review.v1",
        "owner": args.owner,
        "phase": args.phase,
        "lifecycle": args.lifecycle,
        "staged_path_count": len(staged),
        "staged_paths": staged,
        "expected_staged_path_count": len(expected),
        "allowlist_missing": allowlist_missing,
        "allowlist_unexpected": allowlist_unexpected,
        "blob_errors": blob_errors,
        "json_parse_count": json_parse_count,
        "json_errors": json_errors,
        "privacy_pattern_classes": list(PRIVACY_PATTERNS),
        "scanner_definition_candidates": scanner_definition_candidates,
        "root_capacity_probe_candidates": root_capacity_probe_candidates,
        "privacy_candidates": privacy_candidates,
        "privacy_confirmed_hits": [],
        "manifest_entry_count": manifest["entry_count"],
        "manifest_mismatches": manifest_mismatches,
        "manifest_exclusions": exclusions,
        "manifest_coverage_missing": coverage_missing,
        "manifest_coverage_extra": coverage_extra,
        "diff_check_exit_code": diff_check.returncode,
        "diff_check_output": diff_check.stdout.decode("utf-8", errors="replace"),
        "issues": issues,
        "valid": not issues,
        "boundary": "Exact staged same-owner workflow evidence only; not privacy completeness, exhaustive security, independent reproduction, production certification, professional authority, legal or cultural ratification, Māori authority, empirical confirmation, Theory-of-Everything proof, or Stage 20 readiness.",
    }
    write_json(receipt_path, receipt)
    print(
        json.dumps(
            {
                "valid": receipt["valid"],
                "staged": len(staged),
                "json": json_parse_count,
                "manifest": manifest["entry_count"],
                "privacy_candidates": len(privacy_candidates),
                "issues": issues,
            },
            sort_keys=True,
        )
    )
    return 0 if receipt["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
