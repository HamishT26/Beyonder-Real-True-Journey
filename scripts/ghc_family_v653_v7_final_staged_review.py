#!/usr/bin/env python3
"""Review Orin Thale's exact staged v653-v7 closeout delta and owner surface."""

from __future__ import annotations

import json
from pathlib import Path

from ghc_family_v653_v7_validation_common import (
    PHASE,
    PHASE_PREFIX,
    REPO,
    batch_blob_bytes,
    git,
    scan_privacy_bytes,
    sha256_bytes,
    staged_blob_map,
    write_json,
)


BASE_COMMIT = "e94f2f3c048678b6d7c87c6d4037dc8b24787c4a"
OWNER_MANIFEST = (
    "docs/orin-thale/v653-v7/validation/final-owner-manifest.json"
)
FINAL_MANIFEST = (
    "docs/orin-thale/v653-v7/validation/final-staged-manifest.json"
)
FINAL_REVIEW = (
    "docs/orin-thale/v653-v7/validation/final-staged-review.json"
)
SELF_EXCLUSIONS = {OWNER_MANIFEST, FINAL_MANIFEST, FINAL_REVIEW}
ALLOWED_TOOLS = {
    "scripts/build_ghc_family_v653_v7_closeout.py",
    "scripts/build_ghc_family_v653_v7_terminal_correction.py",
    "scripts/ghc_family_v653_v7_final_staged_review.py",
    "scripts/ghc_family_v653_v7_final_validate.py",
    "tests/test_ghc_family_v653_v7_closeout.py",
}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def index_paths() -> list[str]:
    return sorted(
        row
        for row in git("ls-files").splitlines()
        if row
    )


def runner_paths() -> set[str]:
    receipt = read_json(PHASE / "runners/runner-invocation-receipt.json")
    return {f"scripts/{row['runner']}" for row in receipt["runners"]}


def owner_path(path: str, runners: set[str]) -> bool:
    return (
        path.startswith(PHASE_PREFIX)
        or path.startswith("scripts/ghc_family_v653_v7_")
        or path.startswith("scripts/build_ghc_family_v653_v7_")
        or path.startswith("tests/test_ghc_family_v653_v7_")
        or path in runners
    )


def entries_for(paths: list[str]) -> tuple[list[dict], list[tuple[str, bytes]]]:
    blob_map = staged_blob_map(paths)
    payload_by_blob = batch_blob_bytes(blob_map.values())
    rows = [(path, payload_by_blob[blob_map[path]]) for path in paths]
    entries = [
        {
            "path": path,
            "git_blob": blob_map[path],
            "sha256": sha256_bytes(payload),
            "bytes": len(payload),
        }
        for path, payload in rows
    ]
    return entries, rows


def frozen_mismatches(
    manifest_path: Path,
    current_blobs: dict[str, str],
) -> list[dict[str, str]]:
    manifest = read_json(manifest_path)
    mismatches = []
    for entry in manifest["entries"]:
        observed = current_blobs.get(entry["path"])
        if observed != entry["git_blob"]:
            mismatches.append(
                {
                    "path": entry["path"],
                    "expected": entry["git_blob"],
                    "observed": observed or "missing",
                }
            )
    return mismatches


def build() -> dict:
    staged = sorted(
        row
        for row in git(
            "diff", "--cached", "--name-only", "--diff-filter=ACMRT"
        ).splitlines()
        if row
    )
    runners = runner_paths()
    out_of_scope = [
        path
        for path in staged
        if not path.startswith(PHASE_PREFIX) and path not in ALLOWED_TOOLS
    ]
    staged_included = [
        path for path in staged if path not in SELF_EXCLUSIONS
    ]
    staged_entries, staged_rows = entries_for(staged_included)
    staged_privacy = scan_privacy_bytes(staged_rows)

    owner_all = [
        path for path in index_paths() if owner_path(path, runners)
    ]
    owner_included = [
        path for path in owner_all if path not in SELF_EXCLUSIONS
    ]
    owner_entries, owner_rows = entries_for(owner_included)
    owner_privacy = scan_privacy_bytes(owner_rows)
    current_blobs = staged_blob_map(owner_included)
    x1_mismatches = frozen_mismatches(
        PHASE / "validation/x1-staged-manifest.json",
        current_blobs,
    )
    evidence_mismatches = frozen_mismatches(
        PHASE / "validation/evidence-candidate-manifest.json",
        current_blobs,
    )

    final_names_hash = sha256_bytes(
        ("\n".join(staged) + "\n").encode("utf-8")
    )
    owner_names_hash = sha256_bytes(
        ("\n".join(owner_all) + "\n").encode("utf-8")
    )
    write_json(
        PHASE / "validation/final-staged-manifest.json",
        {
            "schema": "ghc.family.v653-v7.final-staged-manifest.v1",
            "base_commit": BASE_COMMIT,
            "staged_path_count": len(staged),
            "entry_count": len(staged_entries),
            "entries": staged_entries,
            "self_exclusions": sorted(SELF_EXCLUSIONS),
            "exact_staged_names_sha256": final_names_hash,
            "boundary": (
                "Exact Git-index closeout-delta bytes with three declared "
                "lifecycle self-exclusions."
            ),
        },
    )
    write_json(
        PHASE / "validation/final-owner-manifest.json",
        {
            "schema": "ghc.family.v653-v7.final-owner-manifest.v1",
            "hash_domain": "exact Git index",
            "owner_path_count": len(owner_all),
            "entry_count": len(owner_entries),
            "entries": owner_entries,
            "self_exclusions": sorted(SELF_EXCLUSIONS),
            "exact_owner_names_sha256": owner_names_hash,
            "boundary": (
                "All Orin v653-v7 owner-scoped repository paths except the "
                "three recursive lifecycle manifests."
            ),
        },
    )
    valid = (
        bool(staged)
        and not out_of_scope
        and staged_privacy["valid"]
        and owner_privacy["valid"]
        and not x1_mismatches
        and not evidence_mismatches
        and len(staged_entries)
        == len(staged) - len(set(staged) & SELF_EXCLUSIONS)
        and len(owner_entries)
        == len(owner_all) - len(set(owner_all) & SELF_EXCLUSIONS)
    )
    review = {
        "schema": "ghc.family.v653-v7.final-staged-review.v1",
        "base_commit": BASE_COMMIT,
        "staged_path_count": len(staged),
        "staged_manifest_entry_count": len(staged_entries),
        "owner_path_count": len(owner_all),
        "owner_manifest_entry_count": len(owner_entries),
        "out_of_scope_paths": out_of_scope,
        "x1_manifest_mismatches": x1_mismatches,
        "evidence_manifest_mismatches": evidence_mismatches,
        "staged_privacy": staged_privacy,
        "owner_privacy": owner_privacy,
        "exact_staged_names_sha256": final_names_hash,
        "exact_owner_names_sha256": owner_names_hash,
        "diff_hygiene_required_separately": True,
        "valid": valid,
        "boundary": (
            "Exact closeout candidate review only; it does not preclaim the "
            "containing commit or the one canonical exact-final pass."
        ),
    }
    write_json(PHASE / "validation/final-staged-review.json", review)
    return review


def main() -> None:
    result = build()
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    if not result["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
