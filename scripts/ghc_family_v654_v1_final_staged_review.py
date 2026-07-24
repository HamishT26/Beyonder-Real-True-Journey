#!/usr/bin/env python3
"""Build or verify Tamar Vey's exact staged v654-v1 lifecycle manifests."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/tamar-vey/v654-v1"
EVIDENCE = "136d55ba5af1f4f596da0c47d9be931a785cdb18"
DELTA_MANIFEST = "docs/tamar-vey/v654-v1/validation/final-delta-manifest.json"
OWNER_MANIFEST = "docs/tamar-vey/v654-v1/validation/final-owner-manifest.json"
STAGED_REVIEW = "docs/tamar-vey/v654-v1/validation/final-staged-review.json"
PRIVACY_RECEIPT = "docs/tamar-vey/v654-v1/validation/final-privacy-receipt.json"
SELF_EXCLUSIONS = {
    DELTA_MANIFEST,
    OWNER_MANIFEST,
    STAGED_REVIEW,
    PRIVACY_RECEIPT,
}
RUNNERS = {
    "scripts/ghc_family_ceramic_material_ledger.py",
    "scripts/ghc_family_kiln_state_boards.py",
    "scripts/ghc_family_worker_boundary_boards.py",
    "scripts/ghc_family_food_waste_release_refusal.py",
    "scripts/ghc_family_gmut_heat_phase_fields.py",
    "scripts/ghc_family_thos_ceramics_proxy.py",
    "scripts/ghc_family_freed_id_ceramic_profiles.py",
    "scripts/ghc_family_accessible_ceramics_audit.py",
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
        path.startswith("docs/tamar-vey/v654-v1/")
        or path.startswith("scripts/ghc_family_v654_v1_")
        or path.startswith("scripts/build_ghc_family_v654_v1_")
        or path.startswith("tests/test_ghc_family_v654_v1")
        or path in RUNNERS
    )


def index_map() -> dict[str, str]:
    result: dict[str, str] = {}
    for raw in git_bytes("ls-files", "--stage", "-z").split(b"\0"):
        if not raw:
            continue
        metadata, path_bytes = raw.split(b"\t", 1)
        _, oid, stage = metadata.decode("ascii").split()
        if stage != "0":
            raise RuntimeError(f"nonzero index stage: {path_bytes!r}")
        result[path_bytes.decode("utf-8")] = oid
    return result


def tree_map(commit: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for raw in git_bytes("ls-tree", "-r", "-z", commit).split(b"\0"):
        if not raw:
            continue
        metadata, path_bytes = raw.split(b"\t", 1)
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


def entries(paths: list[str], objects: dict[str, str], blobs: dict[str, bytes]) -> list[dict[str, Any]]:
    return [
        {
            "path": path,
            "git_blob": objects[path],
            "bytes": len(blobs[path]),
            "sha256": hashlib.sha256(blobs[path]).hexdigest(),
        }
        for path in paths
    ]


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
            r"(?i)(session_stream|raw_transcript|conversation_export)"
        ),
    }
    definitions = {
        "scripts/ghc_family_v654_v1_x1_validate.py",
        "scripts/ghc_family_v654_v1_evidence_validate.py",
        "scripts/build_ghc_family_v654_v1_preregistration.py",
        "scripts/ghc_family_v654_v1_final_staged_review.py",
        "scripts/ghc_family_v654_v1_final_validate.py",
        "docs/tamar-vey/v654-v1/validation/x1-staged-privacy.json",
        "docs/tamar-vey/v654-v1/validation/evidence-privacy.json",
        PRIVACY_RECEIPT,
    }
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    scanned = 0
    for path in paths:
        try:
            content = blobs[path].decode("utf-8")
        except UnicodeDecodeError:
            continue
        scanned += 1
        for pattern_class, pattern in patterns.items():
            if not pattern.search(content):
                continue
            disposition = (
                "scanner_definition"
                if path in definitions
                else "confirmed_payload_hit"
            )
            row = {
                "path": path,
                "pattern_class": pattern_class,
                "disposition": disposition,
            }
            candidates.append(row)
            if disposition == "confirmed_payload_hit":
                confirmed.append(row)
    return {
        "schema": "ghc.family.v654-v1.final-privacy.v1",
        "scanned_file_count": scanned,
        "pattern_classes": sorted(patterns),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "boundary": (
            "Five structural classes with scanner-definition quarantine; "
            "zero confirmed hits is not complete privacy assurance."
        ),
    }


def computed() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    objects = index_map()
    delta_paths = sorted(
        path
        for path in git(
            "diff",
            "--cached",
            "--name-only",
            "--diff-filter=ACMR",
            EVIDENCE,
        ).splitlines()
        if path and path not in SELF_EXCLUSIONS
    )
    all_delta = sorted(
        path
        for path in git(
            "diff",
            "--cached",
            "--name-only",
            "--diff-filter=ACMR",
            EVIDENCE,
        ).splitlines()
        if path
    )
    out_of_scope = [path for path in all_delta if not owner_path(path)]
    if not all_delta or out_of_scope:
        raise RuntimeError(
            f"invalid final staged scope: count={len(all_delta)} out={out_of_scope}"
        )
    owner_paths = sorted(
        path
        for path in objects
        if owner_path(path) and path not in SELF_EXCLUSIONS
    )
    needed = {path: objects[path] for path in sorted(set(delta_paths + owner_paths))}
    blobs = batch_blobs(needed)
    delta_entries = entries(delta_paths, objects, blobs)
    owner_entries = entries(owner_paths, objects, blobs)
    privacy = privacy_scan(owner_paths, blobs)
    if privacy["confirmed_hit_count"]:
        raise RuntimeError(f"confirmed privacy hits: {privacy['confirmed_hits']}")
    x1 = json.loads(
        git(
            "show",
            "e5d685fb3a4a84af32fe5914eb0f8d069c854e97:"
            "docs/tamar-vey/v654-v1/validation/x1-staged-manifest.json",
        )
    )
    evidence = json.loads(
        git(
            "show",
            f"{EVIDENCE}:docs/tamar-vey/v654-v1/validation/evidence-manifest.json",
        )
    )
    x1_tree = tree_map("e5d685fb3a4a84af32fe5914eb0f8d069c854e97")
    evidence_tree = tree_map(EVIDENCE)
    x1_mismatch = [
        row["path"]
        for row in x1["entries"]
        if x1_tree.get(row["path"]) != row["git_blob"]
    ]
    evidence_mismatch = [
        row["path"]
        for row in evidence["entries"]
        if evidence_tree.get(row["path"]) != row["git_blob"]
    ]
    if x1_mismatch or evidence_mismatch:
        raise RuntimeError(
            f"commit-local manifest mismatch: x1={x1_mismatch} evidence={evidence_mismatch}"
        )
    delta_manifest = {
        "schema": "ghc.family.v654-v1.final-delta-manifest.v1",
        "base_commit": EVIDENCE,
        "hash_domain": "exact_staged_git_blobs",
        "entries": delta_entries,
        "entry_count": len(delta_entries),
        "self_exclusions": sorted(SELF_EXCLUSIONS),
        "coverage_boundary": (
            "Every final delta file except four declared self-referential "
            "lifecycle receipts."
        ),
    }
    owner_manifest = {
        "schema": "ghc.family.v654-v1.final-owner-manifest.v1",
        "hash_domain": "exact_index_git_blobs",
        "entries": owner_entries,
        "entry_count": len(owner_entries),
        "self_exclusions": sorted(SELF_EXCLUSIONS),
        "coverage_boundary": (
            "Every Tamar v654-v1 owner-scoped index path except four declared "
            "self-referential lifecycle receipts."
        ),
    }
    review = {
        "schema": "ghc.family.v654-v1.final-staged-review.v1",
        "base_commit": EVIDENCE,
        "staged_path_count": len(all_delta),
        "delta_manifest_entry_count": len(delta_entries),
        "owner_manifest_entry_count": len(owner_entries),
        "self_exclusion_count": len(SELF_EXCLUSIONS),
        "out_of_scope_staged_paths": out_of_scope,
        "privacy_scanned_file_count": privacy["scanned_file_count"],
        "privacy_confirmed_hit_count": privacy["confirmed_hit_count"],
        "x1_manifest_entries_replayed": len(x1["entries"]),
        "x1_manifest_mismatches": x1_mismatch,
        "evidence_manifest_entries_replayed": len(evidence["entries"]),
        "evidence_manifest_mismatches": evidence_mismatch,
        "valid": (
            not out_of_scope
            and not x1_mismatch
            and not evidence_mismatch
            and privacy["confirmed_hit_count"] == 0
        ),
        "boundary": (
            "Exact staged and index review only; not the postcommit canonical "
            "test pass, full repository suite, or broader assurance."
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
    mismatches = [name for name in expected if observed[name] != expected[name]]
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
    raise SystemExit(0 if review["valid"] else 1)


if __name__ == "__main__":
    main()
