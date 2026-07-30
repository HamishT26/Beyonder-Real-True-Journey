#!/usr/bin/env python3
"""Review and manifest the exact staged Sylven Arc v656-v3 final delta."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
PHASE_PREFIX = "docs/sylven-arc/v656-v3/"
PHASE = REPO / PHASE_PREFIX
BASE = "f0de53a52e9f4e99e6dda1ee6d02de8cfb4e7da6"
FINAL_CODE_PATHS = {
    "scripts/build_ghc_family_v656_v3_closeout.py",
    "scripts/ghc_family_v656_v3_final_staged_review.py",
    "scripts/ghc_family_v656_v3_final_validate.py",
    "tests/test_ghc_family_v656_v3_closeout.py",
}
SELF_EXCLUSIONS = {
    f"{PHASE_PREFIX}validation/final-owner-manifest.json",
    f"{PHASE_PREFIX}validation/final-staged-manifest.json",
    f"{PHASE_PREFIX}validation/final-staged-review.json",
}
SCANNER_PATHS = {
    "scripts/ghc_family_v656_v3_final_staged_review.py",
    "scripts/ghc_family_v656_v3_final_validate.py",
}


def run(*args: str, input_bytes: bytes | None = None) -> bytes:
    return subprocess.run(
        list(args),
        cwd=REPO,
        check=True,
        input=input_bytes,
        capture_output=True,
    ).stdout


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def staged_paths() -> list[str]:
    raw = run("git", "diff", "--cached", "--name-only", "-z", BASE)
    return sorted(
        row.decode("utf-8", errors="strict")
        for row in raw.split(b"\0")
        if row
    )


def index_rows(prefix: str | None = None) -> list[tuple[str, str]]:
    args = ["git", "ls-files", "-s", "-z"]
    if prefix:
        args.extend(["--", prefix])
    raw = run(*args)
    rows: list[tuple[str, str]] = []
    for item in raw.split(b"\0"):
        if not item:
            continue
        metadata, path = item.split(b"\t", 1)
        _mode, oid, stage = metadata.decode("ascii").split()
        if stage != "0":
            raise RuntimeError(f"unmerged index entry: {path!r}")
        rows.append((path.decode("utf-8"), oid))
    return rows


def blobs(oids: list[str]) -> dict[str, bytes]:
    unique = list(dict.fromkeys(oids))
    request = "".join(f"{oid}\n" for oid in unique).encode("ascii")
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=REPO,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = process.communicate(request)
    if process.returncode != 0:
        raise RuntimeError(stderr.decode("utf-8", errors="replace"))
    offset = 0
    result: dict[str, bytes] = {}
    for requested in unique:
        line_end = stdout.index(b"\n", offset)
        header = stdout[offset:line_end].decode("ascii")
        offset = line_end + 1
        actual, kind, size_text = header.split()
        if kind != "blob":
            raise RuntimeError(f"{requested} resolved as {kind}")
        size = int(size_text)
        content = stdout[offset : offset + size]
        offset += size
        if stdout[offset : offset + 1] != b"\n":
            raise RuntimeError(f"batch framing failure for {requested}")
        offset += 1
        result[requested] = content
        if actual != requested:
            raise RuntimeError(f"unexpected object id {actual} for {requested}")
    return result


def entries(rows: list[tuple[str, str]]) -> list[dict[str, Any]]:
    content = blobs([oid for _path, oid in rows])
    return [
        {
            "path": path,
            "git_blob": oid,
            "bytes": len(content[oid]),
            "sha256": hashlib.sha256(content[oid]).hexdigest(),
        }
        for path, oid in sorted(rows)
    ]


def exists_at_base(path: str) -> bool:
    return (
        subprocess.run(
            ["git", "cat-file", "-e", f"{BASE}:{path}"],
            cwd=REPO,
            capture_output=True,
        ).returncode
        == 0
    )


def privacy_scan(
    rows: list[tuple[str, str]], blob_map: dict[str, bytes]
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    patterns = {
        "raw_uuid": re.compile(
            r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-"
            r"[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
            re.I,
        ),
        "private_absolute_path": re.compile(
            r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives)[\\/]"
        ),
        "credential_or_secret": re.compile(
            r"(?:(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}|"
            r"(?<![A-Za-z0-9])ghp_[A-Za-z0-9]{20,}|"
            r"(?<![A-Za-z0-9])AKIA[0-9A-Z]{16}|"
            r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)"
        ),
        "raw_thread_or_task_identifier": re.compile(
            r"\b(?:thread|task)[_-]?id\s*[:=]\s*[A-Za-z0-9_-]{12,}\b",
            re.I,
        ),
        "private_callable_or_session_stream": re.compile(
            r"\b(?:private_callable_id|session_stream|app_state)\s*[:=]",
            re.I,
        ),
    }
    candidates: list[dict[str, str]] = []
    for path, oid in rows:
        text = blob_map[oid].decode("utf-8", errors="replace")
        for label, pattern in patterns.items():
            if pattern.search(text):
                candidates.append({"path": path, "class": label})
    definition_only = [row for row in candidates if row["path"] in SCANNER_PATHS]
    confirmed = [row for row in candidates if row["path"] not in SCANNER_PATHS]
    return confirmed, definition_only


def main() -> None:
    head = run("git", "rev-parse", "HEAD").decode().strip()
    if head != BASE:
        raise RuntimeError(f"staged review requires evidence head {BASE}, got {head}")
    paths = staged_paths()
    unexpected = [
        path
        for path in paths
        if not path.startswith(PHASE_PREFIX) and path not in FINAL_CODE_PATHS
    ]
    missing_code = sorted(FINAL_CODE_PATHS - set(paths))
    changed_existing = [
        path
        for path in paths
        if path not in SELF_EXCLUSIONS and exists_at_base(path)
    ]
    index = index_rows()
    index_map = dict(index)
    staged_rows = [
        (path, index_map[path])
        for path in paths
        if path not in SELF_EXCLUSIONS
    ]
    staged_blob_map = blobs([oid for _path, oid in staged_rows])
    confirmed, definition_only = privacy_scan(staged_rows, staged_blob_map)
    json_errors: list[dict[str, str]] = []
    json_count = 0
    for path, oid in staged_rows:
        if not path.endswith(".json"):
            continue
        json_count += 1
        try:
            json.loads(staged_blob_map[oid].decode("utf-8"))
        except Exception as exc:
            json_errors.append({"path": path, "error": type(exc).__name__})

    owner_rows = [
        (path, oid)
        for path, oid in index_rows(PHASE_PREFIX)
        if path not in SELF_EXCLUSIONS
    ]
    owner_entries = entries(owner_rows)
    delta_entries = entries(staged_rows)
    owner_manifest = {
        "schema": "ghc.family.v656-v3.final-owner-manifest.v1",
        "content_basis": "prospective_exact_git_index",
        "boundary": (
            "Complete owner-phase coverage except three declared lifecycle "
            "self-exclusions; exact committed parity is checked once at final."
        ),
        "self_exclusions": sorted(SELF_EXCLUSIONS),
        "entry_count": len(owner_entries),
        "entries": owner_entries,
    }
    delta_manifest = {
        "schema": "ghc.family.v656-v3.final-staged-manifest.v1",
        "base_commit": BASE,
        "content_basis": "prospective_exact_git_index",
        "boundary": "Exact combined closeout and seal delta with three self-exclusions.",
        "self_exclusions": sorted(SELF_EXCLUSIONS),
        "entry_count": len(delta_entries),
        "entries": delta_entries,
    }
    valid = (
        bool(paths)
        and not unexpected
        and not missing_code
        and not changed_existing
        and not confirmed
        and not json_errors
        and len(owner_entries) < 2000
    )
    review = {
        "schema": "ghc.family.v656-v3.final-staged-review.v1",
        "base_commit": BASE,
        "staged_path_count_including_self_exclusions": len(paths),
        "reviewed_entry_count": len(delta_entries),
        "owner_manifest_entry_count": len(owner_entries),
        "staged_json_count": json_count,
        "json_errors": json_errors,
        "privacy_scan_classes": 5,
        "privacy_confirmed_hits": confirmed,
        "privacy_definition_only_candidates": definition_only,
        "unexpected_paths": unexpected,
        "missing_final_code_paths": missing_code,
        "frozen_evidence_paths_changed": changed_existing,
        "diff_hygiene": "PASS" if valid else "FAIL",
        "valid": valid,
        "boundary": (
            "Prospective staged review only; exact-final commit, clean state, "
            "remote equality, canonical validation, and route delivery remain pending."
        ),
    }
    write_json(PHASE / "validation/final-owner-manifest.json", owner_manifest)
    write_json(PHASE / "validation/final-staged-manifest.json", delta_manifest)
    write_json(PHASE / "validation/final-staged-review.json", review)
    print(
        json.dumps(
            {
                "valid": valid,
                "staged": len(paths),
                "reviewed": len(delta_entries),
                "owner": len(owner_entries),
                "json": json_count,
                "privacy_hits": len(confirmed),
                "changed_existing": len(changed_existing),
                "unexpected": len(unexpected),
            },
            sort_keys=True,
        )
    )
    if not valid:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
