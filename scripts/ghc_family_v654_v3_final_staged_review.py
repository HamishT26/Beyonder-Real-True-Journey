#!/usr/bin/env python3
"""Build or verify Sylven Arc's exact staged v654-v3 manifests."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/sylven-arc/v654-v3"
X1 = "0c53bce867ec5259d9b7de8c14b92b07b678641f"
EVIDENCE = "780acdf2225624080463c274dc88c001f5a65d54"
DELTA_MANIFEST = "docs/sylven-arc/v654-v3/validation/final-delta-manifest.json"
OWNER_MANIFEST = "docs/sylven-arc/v654-v3/validation/final-owner-manifest.json"
STAGED_REVIEW = "docs/sylven-arc/v654-v3/validation/final-staged-review.json"
PRIVACY_RECEIPT = "docs/sylven-arc/v654-v3/validation/final-privacy-receipt.json"
SELF_EXCLUSIONS = {
    DELTA_MANIFEST,
    OWNER_MANIFEST,
    STAGED_REVIEW,
    PRIVACY_RECEIPT,
}
RUNNERS = {
    "scripts/ghc_family_accessible_bicycle_audit.py",
    "scripts/ghc_family_bicycle_brake_steering_boards.py",
    "scripts/ghc_family_bicycle_fitment_refusal.py",
    "scripts/ghc_family_bicycle_intake_ledger.py",
    "scripts/ghc_family_bicycle_recall_quarantine.py",
    "scripts/ghc_family_freed_id_bicycle_profiles.py",
    "scripts/ghc_family_gmut_bicycle_fields.py",
    "scripts/ghc_family_thos_bicycle_proxy.py",
}
SCANNER_DEFINITIONS = {
    "scripts/build_ghc_family_v654_v3_preregistration.py",
    "scripts/ghc_family_v654_v3_x1_validate.py",
    "scripts/ghc_family_v654_v3_evidence_validate.py",
    "scripts/ghc_family_v654_v3_final_staged_review.py",
    "scripts/ghc_family_v654_v3_final_validate.py",
    "docs/sylven-arc/v654-v3/validation/x1-staged-privacy.json",
    "docs/sylven-arc/v654-v3/validation/evidence-privacy.json",
    PRIVACY_RECEIPT,
}


def git_bytes(*args: str, input_bytes: bytes | None = None) -> bytes:
    return subprocess.run(
        ["git", *args],
        cwd=REPO,
        input=input_bytes,
        check=True,
        capture_output=True,
    ).stdout


def git(*args: str) -> str:
    return git_bytes(*args).decode("utf-8").strip()


def write(relative: str, payload: Any) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def owner_path(path: str) -> bool:
    return (
        path.startswith("docs/sylven-arc/v654-v3/")
        or path.startswith("scripts/ghc_family_v654_v3_")
        or path.startswith("scripts/build_ghc_family_v654_v3_")
        or path.startswith("tests/test_ghc_family_v654_v3")
        or path in RUNNERS
    )


def index_map() -> dict[str, str]:
    result: dict[str, str] = {}
    for row in git_bytes("ls-files", "-s", "-z").split(b"\0"):
        if not row:
            continue
        metadata, path_bytes = row.split(b"\t", 1)
        _, oid, stage = metadata.decode("ascii").split()
        if stage == "0":
            result[path_bytes.decode("utf-8")] = oid
    return result


def tree_map(commit: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for row in git_bytes("ls-tree", "-r", "-z", commit).split(b"\0"):
        if not row:
            continue
        metadata, path_bytes = row.split(b"\t", 1)
        _, kind, oid = metadata.decode("ascii").split()
        if kind == "blob":
            result[path_bytes.decode("utf-8")] = oid
    return result


def batch_blobs(rows: dict[str, str]) -> dict[str, bytes]:
    ordered = list(rows.items())
    request = b"".join(f"{oid}\n".encode("ascii") for _, oid in ordered)
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=REPO,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    raw, _ = process.communicate(input=request, timeout=60)
    if process.returncode != 0:
        raise RuntimeError("git cat-file --batch failed")
    output: dict[str, bytes] = {}
    cursor = 0
    for path, oid in ordered:
        newline = raw.find(b"\n", cursor)
        if newline < 0:
            raise RuntimeError(f"missing cat-file header for {path}")
        header = raw[cursor:newline].decode("ascii")
        cursor = newline + 1
        parts = header.split()
        if len(parts) != 3 or parts[0] != oid or parts[1] != "blob":
            raise RuntimeError(f"unexpected cat-file header for {path}: {header}")
        size = int(parts[2])
        payload = raw[cursor : cursor + size]
        cursor += size
        if len(payload) != size or raw[cursor : cursor + 1] != b"\n":
            raise RuntimeError(f"truncated cat-file payload for {path}")
        cursor += 1
        output[path] = payload
    if cursor != len(raw):
        raise RuntimeError("unexpected trailing cat-file output")
    return output


def manifest_entries(
    paths: list[str], objects: dict[str, str], blobs: dict[str, bytes]
) -> list[dict[str, Any]]:
    return [
        {
            "path": path,
            "git_blob": objects[path],
            "bytes": len(blobs[path]),
            "sha256": hashlib.sha256(blobs[path]).hexdigest(),
        }
        for path in paths
    ]


def replay_manifest(commit: str, path: str) -> tuple[int, list[str]]:
    payload = json.loads(git("show", f"{commit}:{path}"))
    objects = tree_map(commit)
    requested = {
        row["path"]: objects.get(row["path"], "")
        for row in payload["entries"]
        if objects.get(row["path"])
    }
    blobs = batch_blobs(requested)
    mismatches: list[str] = []
    for row in payload["entries"]:
        observed_oid = objects.get(row["path"])
        if observed_oid != row["git_blob"]:
            mismatches.append(f"{row['path']}:oid")
            continue
        data = blobs[row["path"]]
        if len(data) != row["bytes"]:
            mismatches.append(f"{row['path']}:bytes")
        if hashlib.sha256(data).hexdigest() != row["sha256"]:
            mismatches.append(f"{row['path']}:sha256")
    return len(payload["entries"]), mismatches


def privacy_scan(paths: list[str], blobs: dict[str, bytes]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(
            r"(?i)(source_thread_id|thread_id)\s*[:=]"
        ),
        "private_absolute_local_path": re.compile(
            r"(?i)[A-Z]:\\Users\\[^\s\"']+"
        ),
        "credential_or_secret": re.compile(
            r"(?i)(?:(?:api[_-]?key|client_secret|private_key)\s*[:=]\s*"
            r"[\"']?[A-Za-z0-9._-]{8,}|bearer\s+[A-Za-z0-9._-]{12,})"
        ),
        "private_route_or_callable": re.compile(
            r"(?i)(private_route|callable_identifier|"
            r"browser_send_submitted_response_active)"
        ),
        "transcript_or_session_stream": re.compile(
            r"(?i)(session_stream|conversation_transcript|resume_token)"
        ),
    }
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    scanned = 0
    text_suffixes = {
        ".json",
        ".md",
        ".html",
        ".htm",
        ".py",
        ".yaml",
        ".yml",
        ".txt",
    }
    for path in paths:
        if Path(path).suffix.casefold() not in text_suffixes:
            continue
        scanned += 1
        text = blobs[path].decode("utf-8", errors="replace")
        for pattern_class, pattern in patterns.items():
            if not pattern.search(text):
                continue
            row = {
                "path": path,
                "pattern_class": pattern_class,
                "disposition": (
                    "scanner_definition"
                    if path in SCANNER_DEFINITIONS
                    else "confirmed_payload_hit"
                ),
            }
            candidates.append(row)
            if row["disposition"] != "scanner_definition":
                confirmed.append(row)
    return {
        "schema": "ghc.family.v654-v3.final-privacy.v1",
        "pattern_classes": list(patterns),
        "scanned_file_count": scanned,
        "candidate_count": len(candidates),
        "candidates": candidates,
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "boundary": (
            "Five structural classes with exact scanner-definition quarantine; "
            "zero confirmed hits is not complete privacy assurance."
        ),
    }


def computed() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    all_delta = sorted(
        row
        for row in git(
            "diff", "--cached", "--name-only", "--diff-filter=ACMR"
        ).splitlines()
        if row
    )
    deleted = [
        row
        for row in git(
            "diff", "--cached", "--name-only", "--diff-filter=D"
        ).splitlines()
        if row
    ]
    out_of_scope = [path for path in all_delta if not owner_path(path)]
    if not all_delta or deleted or out_of_scope:
        raise RuntimeError(
            f"invalid final staged scope: count={len(all_delta)} "
            f"deleted={deleted} out={out_of_scope}"
        )

    objects = index_map()
    delta_paths = [
        path
        for path in all_delta
        if path not in SELF_EXCLUSIONS and path in objects
    ]
    owner_paths = sorted(
        path
        for path in objects
        if owner_path(path) and path not in SELF_EXCLUSIONS
    )
    requested_paths = sorted(set(delta_paths) | set(owner_paths))
    blobs = batch_blobs({path: objects[path] for path in requested_paths})
    delta_entries = manifest_entries(delta_paths, objects, blobs)
    owner_entries = manifest_entries(owner_paths, objects, blobs)

    privacy = privacy_scan(owner_paths, blobs)
    if privacy["confirmed_hit_count"]:
        raise RuntimeError(f"confirmed privacy hits: {privacy['confirmed_hits']}")

    x1_count, x1_mismatch = replay_manifest(
        X1,
        "docs/sylven-arc/v654-v3/validation/x1-staged-manifest.json",
    )
    evidence_count, evidence_mismatch = replay_manifest(
        EVIDENCE,
        "docs/sylven-arc/v654-v3/validation/evidence-manifest.json",
    )
    if x1_mismatch or evidence_mismatch:
        raise RuntimeError(
            f"commit-local manifest mismatch: x1={x1_mismatch} "
            f"evidence={evidence_mismatch}"
        )

    delta_manifest = {
        "schema": "ghc.family.v654-v3.final-delta-manifest.v1",
        "hash_domain": "exact_staged_git_blobs",
        "base_commit": EVIDENCE,
        "entries": delta_entries,
        "entry_count": len(delta_entries),
        "self_exclusions": sorted(SELF_EXCLUSIONS),
    }
    owner_manifest = {
        "schema": "ghc.family.v654-v3.final-owner-manifest.v1",
        "hash_domain": "exact_staged_git_blobs",
        "entries": owner_entries,
        "entry_count": len(owner_entries),
        "self_exclusions": sorted(SELF_EXCLUSIONS),
    }
    review = {
        "schema": "ghc.family.v654-v3.final-staged-review.v1",
        "base_commit": EVIDENCE,
        "staged_path_count": len(all_delta),
        "delta_manifest_entry_count": len(delta_entries),
        "owner_manifest_entry_count": len(owner_entries),
        "self_exclusion_count": len(SELF_EXCLUSIONS),
        "deleted_staged_paths": deleted,
        "out_of_scope_staged_paths": out_of_scope,
        "privacy_scanned_file_count": privacy["scanned_file_count"],
        "privacy_confirmed_hit_count": privacy["confirmed_hit_count"],
        "x1_manifest_entries_replayed": x1_count,
        "x1_manifest_mismatches": x1_mismatch,
        "evidence_manifest_entries_replayed": evidence_count,
        "evidence_manifest_mismatches": evidence_mismatch,
        "valid": (
            bool(all_delta)
            and not deleted
            and not out_of_scope
            and not x1_mismatch
            and not evidence_mismatch
            and privacy["confirmed_hit_count"] == 0
        ),
        "boundary": (
            "Exact staged and index review only; not the postcommit canonical pass."
        ),
    }
    return delta_manifest, owner_manifest, review, privacy


def build() -> dict[str, Any]:
    delta, owner, review, privacy = computed()
    write("validation/final-delta-manifest.json", delta)
    write("validation/final-owner-manifest.json", owner)
    write("validation/final-privacy-receipt.json", privacy)
    write("validation/final-staged-review.json", review)
    return review


def verify() -> dict[str, Any]:
    delta, owner, review, privacy = computed()
    observed = {
        "delta": json.loads((REPO / DELTA_MANIFEST).read_text(encoding="utf-8")),
        "owner": json.loads((REPO / OWNER_MANIFEST).read_text(encoding="utf-8")),
        "review": json.loads((REPO / STAGED_REVIEW).read_text(encoding="utf-8")),
        "privacy": json.loads((REPO / PRIVACY_RECEIPT).read_text(encoding="utf-8")),
    }
    expected = {
        "delta": delta,
        "owner": owner,
        "review": review,
        "privacy": privacy,
    }
    mismatches = [key for key in expected if observed[key] != expected[key]]
    if mismatches:
        raise RuntimeError(f"staged lifecycle receipt drift: {mismatches}")
    return review


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    review = verify() if args.verify else build()
    print(
        json.dumps(
            {
                "valid": review["valid"],
                "staged": review["staged_path_count"],
                "delta_entries": review["delta_manifest_entry_count"],
                "owner_entries": review["owner_manifest_entry_count"],
                "privacy_hits": review["privacy_confirmed_hit_count"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
