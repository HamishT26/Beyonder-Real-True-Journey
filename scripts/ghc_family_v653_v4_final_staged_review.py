#!/usr/bin/env python3
"""Review and manifest the exact staged Auren Lark v653-v4 final delta."""

from __future__ import annotations

import json

from ghc_family_v653_v4_validation_common import (
    PHASE,
    PHASE_PREFIX,
    batch_blob_bytes,
    git,
    scan_privacy_bytes,
    sha256_bytes,
    staged_blob_map,
    write_json,
)


REVIEW = "docs/auren-lark/v653-v4/validation/final-staged-review.json"
MANIFEST = "docs/auren-lark/v653-v4/validation/final-staged-manifest.json"
SELF_EXCLUSIONS = {REVIEW, MANIFEST}
EVIDENCE = "c75956f62b8aa2046405aa9be9a2c2d72276a347"
ALLOWED_TOOLS = {
    "scripts/build_ghc_family_v653_v4_closeout.py",
    "scripts/ghc_family_v653_v4_minimal_validator.py",
    "scripts/ghc_family_v653_v4_final_staged_review.py",
    "scripts/ghc_family_v653_v4_final_validate.py",
    "tests/test_ghc_family_v653_v4_core.py",
    "tests/test_ghc_family_v653_v4_closeout.py",
}


def build() -> dict:
    paths = sorted(
        path
        for path in git(
            "diff", "--cached", "--name-only", "--diff-filter=ACMRT"
        ).splitlines()
        if path
    )
    allowed = [
        path
        for path in paths
        if path.startswith(PHASE_PREFIX) or path in ALLOWED_TOOLS
    ]
    out_of_scope = sorted(set(paths) - set(allowed))
    included_paths = [path for path in paths if path not in SELF_EXCLUSIONS]
    blob_map = staged_blob_map(included_paths)
    payloads = batch_blob_bytes(blob_map.values())
    rows = [(path, payloads[blob_map[path]]) for path in included_paths]
    privacy = scan_privacy_bytes(rows)
    entries = [
        {
            "path": path,
            "git_blob": blob_map[path],
            "sha256": sha256_bytes(content),
            "bytes": len(content),
        }
        for path, content in rows
    ]
    names_hash = sha256_bytes(("\n".join(paths) + "\n").encode("utf-8"))
    write_json(
        PHASE / "validation/final-staged-manifest.json",
        {
            "schema": "ghc.family.v653-v4.final-staged-manifest.v1",
            "base_commit": EVIDENCE,
            "staged_path_count": len(paths),
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": sorted(SELF_EXCLUSIONS),
            "exact_staged_names_sha256": names_hash,
            "boundary": (
                "Raw Git-index byte manifest with two declared lifecycle "
                "self-exclusions."
            ),
        },
    )
    valid = (
        bool(paths)
        and not out_of_scope
        and privacy["valid"]
        and len(entries) == len(paths) - len(set(paths) & SELF_EXCLUSIONS)
    )
    result = {
        "schema": "ghc.family.v653-v4.final-staged-review.v1",
        "base_commit": EVIDENCE,
        "staged_path_count": len(paths),
        "manifest_entry_count": len(entries),
        "exact_staged_names_sha256": names_hash,
        "out_of_scope_paths": out_of_scope,
        "privacy": privacy,
        "valid": valid,
        "boundary": (
            "Exact final candidate review; it does not preclaim the containing "
            "commit or terminal pass."
        ),
    }
    write_json(PHASE / "validation/final-staged-review.json", result)
    return result


def main() -> None:
    result = build()
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    if not result["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
