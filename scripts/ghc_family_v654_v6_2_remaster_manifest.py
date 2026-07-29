#!/usr/bin/env python3
"""Build and validate exact staged and owner manifests for the remaster."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
PHASE_ROOT = "docs/eiren-kestrel/v654-v6-2-remaster"
OWNER_PREFIXES = (
    PHASE_ROOT + "/",
    "scripts/ghc_family_v654_v6_2_remaster",
    "scripts/build_ghc_family_v654_v6_2_remaster",
    "scripts/ghc_family_roster_check.py",
    "scripts/ghc_family_research_constitution.py",
    "scripts/ghc_family_omega_evidence_passport.py",
    "scripts/ghc_family_correlated_witness_discount.py",
    "scripts/ghc_family_evidence_authority_matrix.py",
    "scripts/ghc_family_thos_task_contract.py",
    "scripts/ghc_family_thos_reconciler.py",
    "scripts/ghc_family_residual_set_preservation.py",
    "scripts/ghc_family_legacy_claims_triage.py",
    "tests/test_ghc_family_v654_v6_2_remaster",
)


def git_bytes(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=REPO)


def git_text(*args: str) -> str:
    return git_bytes(*args).decode("utf-8", errors="strict").strip()


def index_bytes(path: str) -> bytes:
    return git_bytes("show", f":{path}")


def ref_bytes(ref: str, path: str) -> bytes:
    return git_bytes("show", f"{ref}:{path}")


def batch_blob_bytes(specs: list[str]) -> dict[str, bytes]:
    """Read many Git blobs through one cat-file process."""
    if not specs:
        return {}
    process = subprocess.run(
        ["git", "cat-file", "--batch"],
        cwd=REPO,
        input=("\n".join(specs) + "\n").encode("utf-8"),
        capture_output=True,
        check=True,
    )
    rows: dict[str, bytes] = {}
    output = process.stdout
    cursor = 0
    for spec in specs:
        line_end = output.find(b"\n", cursor)
        if line_end < 0:
            raise RuntimeError(f"missing cat-file header for {spec}")
        header = output[cursor:line_end].decode("utf-8", errors="strict")
        cursor = line_end + 1
        if header.endswith(" missing"):
            raise RuntimeError(f"missing Git blob: {spec}")
        parts = header.split()
        if len(parts) != 3 or parts[1] != "blob":
            raise RuntimeError(f"unexpected cat-file header for {spec}: {header}")
        size = int(parts[2])
        content = output[cursor : cursor + size]
        cursor += size
        if output[cursor : cursor + 1] != b"\n":
            raise RuntimeError(f"missing cat-file separator for {spec}")
        cursor += 1
        rows[spec] = content
    return rows


def batch_index_bytes(paths: list[str]) -> dict[str, bytes]:
    specs = [f":{path}" for path in paths]
    blobs = batch_blob_bytes(specs)
    return {path: blobs[f":{path}"] for path in paths}


def batch_ref_bytes(ref: str, paths: list[str]) -> dict[str, bytes]:
    specs = [f"{ref}:{path}" for path in paths]
    blobs = batch_blob_bytes(specs)
    return {path: blobs[f"{ref}:{path}"] for path in paths}


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def entry(path: str, content: bytes) -> dict[str, Any]:
    return {
        "path": path,
        "bytes": len(content),
        "sha256": hashlib.sha256(content).hexdigest(),
    }


def staged_paths(base: str | None) -> list[str]:
    args = ["diff", "--cached", "--name-only", "--diff-filter=ACMR"]
    if base:
        args.append(base)
    return sorted(filter(None, git_text(*args).splitlines()))


def is_owner_path(path: str) -> bool:
    return any(path.startswith(prefix) for prefix in OWNER_PREFIXES)


def command_staged(args: argparse.Namespace) -> int:
    output = args.output.resolve()
    relative_output = output.relative_to(REPO).as_posix()
    excluded = set(args.exclude or []) | {relative_output}
    paths = [
        path
        for path in staged_paths(args.base)
        if path not in excluded and is_owner_path(path)
    ]
    blobs = batch_index_bytes(paths)
    entries = [entry(path, blobs[path]) for path in paths]
    payload = {
        "schema": "ghc.family.v654-v6-2-remaster.staged-manifest.v1",
        "lifecycle": args.lifecycle,
        "base": args.base,
        "entry_count": len(entries),
        "entries": entries,
        "exact_exclusions": sorted(excluded),
        "source": "exact staged Git blobs",
        "valid": True,
    }
    write_json(output, payload)
    print(json.dumps({"entry_count": len(entries), "lifecycle": args.lifecycle}))
    return 0


def command_owner(args: argparse.Namespace) -> int:
    output = args.output.resolve()
    relative_output = output.relative_to(REPO).as_posix()
    excluded = set(args.exclude or []) | {relative_output}
    paths = sorted(
        path
        for path in git_text("ls-files", "--cached").splitlines()
        if path and path not in excluded and is_owner_path(path)
    )
    blobs = batch_index_bytes(paths)
    entries = [entry(path, blobs[path]) for path in paths]
    payload = {
        "schema": "ghc.family.v654-v6-2-remaster.owner-manifest.v1",
        "lifecycle": args.lifecycle,
        "entry_count": len(entries),
        "entries": entries,
        "exact_exclusions": sorted(excluded),
        "source": "exact complete owner domain from staged Git index",
        "owner_file_cap": 2000,
        "within_owner_file_cap": len(entries) < 2000,
        "valid": len(entries) < 2000,
    }
    write_json(output, payload)
    print(json.dumps({"entry_count": len(entries), "lifecycle": args.lifecycle}))
    return 0 if payload["valid"] else 1


def command_validate(args: argparse.Namespace) -> int:
    manifest_path = args.manifest.resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    issues = []
    manifest_entries = manifest.get("entries", [])
    paths = [row["path"] for row in manifest_entries]
    try:
        blobs = (
            batch_index_bytes(paths)
            if args.ref == ":"
            else batch_ref_bytes(args.ref, paths)
        )
    except (RuntimeError, subprocess.CalledProcessError) as exc:
        blobs = {}
        issues.append({"path": None, "issue": f"batch_blob_error:{type(exc).__name__}"})
    for row in manifest_entries:
        content = blobs.get(row["path"])
        if content is None:
            issues.append({"path": row.get("path"), "issue": "missing_blob"})
            continue
        digest = hashlib.sha256(content).hexdigest()
        if digest != row.get("sha256") or len(content) != row.get("bytes"):
            issues.append({"path": row.get("path"), "issue": "content_mismatch"})
    receipt = {
        "schema": "ghc.family.v654-v6-2-remaster.manifest-validation.v1",
        "manifest": manifest_path.relative_to(REPO).as_posix(),
        "ref": args.ref,
        "entry_count": len(manifest.get("entries", [])),
        "issue_count": len(issues),
        "issues": issues,
        "valid": not issues,
    }
    if args.receipt:
        write_json(args.receipt, receipt)
    print(json.dumps(receipt, sort_keys=True))
    return 0 if receipt["valid"] else 1


def owner_index_paths() -> list[str]:
    return sorted(
        path
        for path in git_text("ls-files", "--cached").splitlines()
        if path and is_owner_path(path)
    )


def command_privacy(args: argparse.Namespace) -> int:
    patterns = {
        "raw_uuid": re.compile(
            rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
            re.I,
        ),
        "private_absolute_path": re.compile(rb"\b[A-Za-z]:[\\/](?:Users|GHC-Archives)[\\/]", re.I),
        "credential_or_secret": re.compile(
            rb"(?:(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}|(?<![A-Za-z0-9])ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY)"
        ),
        "assigned_private_route_identifier": re.compile(
            rb"[\"'](?:task_id|thread_id|agent_id|agent_path|subagent_path|session_id|callable_id|resume_token)[\"']\s*:\s*[\"'][^\"']+[\"']",
            re.I,
        ),
        "private_application_material": re.compile(
            rb"(?:<codex_delegation>|source_thread_id|Screenshot\s+\d{4}-\d{2}-\d{2})",
            re.I,
        ),
    }
    candidates = []
    scanned = 0
    paths = [
        path
        for path in owner_index_paths()
        if Path(path).suffix.lower() in {".py", ".json", ".md", ".txt", ".yaml", ".yml"}
    ]
    blobs = batch_index_bytes(paths)
    for path in paths:
        content = blobs[path]
        scanned += 1
        for label, pattern in patterns.items():
            if pattern.search(content):
                candidates.append({"path": path, "class": label})
    definition_paths = {
        Path(__file__).relative_to(REPO).as_posix(),
        "scripts/build_ghc_family_v654_v6_2_remaster_x1.py",
    }
    confirmed = [row for row in candidates if row["path"] not in definition_paths]
    payload = {
        "schema": "ghc.family.v654-v6-2-remaster.privacy-scan.v1",
        "classes": list(patterns),
        "scanned_file_count": scanned,
        "candidate_count": len(candidates),
        "definition_only_count": len(candidates) - len(confirmed),
        "confirmed_hits": confirmed,
        "confirmed_hit_count": len(confirmed),
        "valid": not confirmed,
        "boundary": "Five-class exact owner-domain scan; not privacy-complete assurance.",
    }
    write_json(args.output, payload)
    print(json.dumps({"scanned": scanned, "confirmed_hits": len(confirmed)}))
    return 0 if payload["valid"] else 1


def command_json(args: argparse.Namespace) -> int:
    rows = []
    paths = [path for path in owner_index_paths() if path.endswith(".json")]
    blobs = batch_index_bytes(paths)
    for path in paths:
        try:
            json.loads(blobs[path].decode("utf-8"))
            rows.append({"path": path, "valid": True})
        except Exception as exc:  # pragma: no cover - emitted as a receipt
            rows.append({"path": path, "valid": False, "error": type(exc).__name__})
    invalid = [row for row in rows if not row["valid"]]
    payload = {
        "schema": "ghc.family.v654-v6-2-remaster.json-parse.v1",
        "json_count": len(rows),
        "invalid_count": len(invalid),
        "invalid": invalid,
        "valid": not invalid,
    }
    write_json(args.output, payload)
    print(json.dumps({"json_count": len(rows), "invalid": len(invalid)}))
    return 0 if payload["valid"] else 1


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    sub = result.add_subparsers(dest="command", required=True)
    staged = sub.add_parser("staged")
    staged.add_argument("--lifecycle", required=True)
    staged.add_argument("--base")
    staged.add_argument("--output", type=Path, required=True)
    staged.add_argument("--exclude", action="append")
    staged.set_defaults(func=command_staged)
    owner = sub.add_parser("owner")
    owner.add_argument("--lifecycle", required=True)
    owner.add_argument("--output", type=Path, required=True)
    owner.add_argument("--exclude", action="append")
    owner.set_defaults(func=command_owner)
    validate = sub.add_parser("validate")
    validate.add_argument("--manifest", type=Path, required=True)
    validate.add_argument("--ref", default=":")
    validate.add_argument("--receipt", type=Path)
    validate.set_defaults(func=command_validate)
    privacy = sub.add_parser("privacy")
    privacy.add_argument("--output", type=Path, required=True)
    privacy.set_defaults(func=command_privacy)
    json_parser = sub.add_parser("json")
    json_parser.add_argument("--output", type=Path, required=True)
    json_parser.set_defaults(func=command_json)
    return result


def main() -> int:
    args = parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
