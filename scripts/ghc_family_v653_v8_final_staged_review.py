#!/usr/bin/env python3
"""Review Liora Venn's exact staged v653-v8 closeout delta and owner surface."""

from __future__ import annotations

import json

import ghc_family_v653_v7_final_staged_review as base
from ghc_family_v653_v8_validation_common import (
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


BASE_COMMIT = "67e51031ed4be4bb64962635e79c459b8a01e7d4"
OWNER_MANIFEST = (
    "docs/liora-venn/v653-v8/validation/final-owner-manifest.json"
)
FINAL_MANIFEST = (
    "docs/liora-venn/v653-v8/validation/final-staged-manifest.json"
)
FINAL_REVIEW = (
    "docs/liora-venn/v653-v8/validation/final-staged-review.json"
)
SELF_EXCLUSIONS = {OWNER_MANIFEST, FINAL_MANIFEST, FINAL_REVIEW}
ALLOWED_TOOLS = {
    "scripts/build_ghc_family_v653_v8_closeout.py",
    "scripts/ghc_family_v653_v8_final_staged_review.py",
    "scripts/ghc_family_v653_v8_final_validate.py",
    "tests/test_ghc_family_v653_v8_closeout.py",
}

base.PHASE = PHASE
base.PHASE_PREFIX = PHASE_PREFIX
base.REPO = REPO
base.BASE_COMMIT = BASE_COMMIT
base.OWNER_MANIFEST = OWNER_MANIFEST
base.FINAL_MANIFEST = FINAL_MANIFEST
base.FINAL_REVIEW = FINAL_REVIEW
base.SELF_EXCLUSIONS = SELF_EXCLUSIONS
base.ALLOWED_TOOLS = ALLOWED_TOOLS
base.batch_blob_bytes = batch_blob_bytes
base.git = git
base.scan_privacy_bytes = scan_privacy_bytes
base.sha256_bytes = sha256_bytes
base.staged_blob_map = staged_blob_map
base.write_json = write_json


def owner_path(path: str, runners: set[str]) -> bool:
    return (
        path.startswith(PHASE_PREFIX)
        or path.startswith("scripts/ghc_family_v653_v8_")
        or path.startswith("scripts/build_ghc_family_v653_v8_")
        or path.startswith("tests/test_ghc_family_v653_v8_")
        or path in runners
    )


base.owner_path = owner_path
_base_build = base.build


def build():
    result = _base_build()
    replacements = [
        ("ghc.family.v653-v7.final-staged-manifest.v1", "ghc.family.v653-v8.final-staged-manifest.v1"),
        ("ghc.family.v653-v7.final-owner-manifest.v1", "ghc.family.v653-v8.final-owner-manifest.v1"),
        ("ghc.family.v653-v7.final-staged-review.v1", "ghc.family.v653-v8.final-staged-review.v1"),
        ("All Orin v653-v7 owner-scoped", "All Liora v653-v8 owner-scoped"),
    ]
    for relative in (
        "validation/final-staged-manifest.json",
        "validation/final-owner-manifest.json",
        "validation/final-staged-review.json",
    ):
        path = PHASE / relative
        text = path.read_text(encoding="utf-8")
        for old, new in replacements:
            text = text.replace(old, new)
        path.write_text(text, encoding="utf-8", newline="\n")
    result["schema"] = "ghc.family.v653-v8.final-staged-review.v1"
    write_json(PHASE / "validation/final-staged-review.json", result)
    return result


base.build = build


if __name__ == "__main__":
    if hasattr(__import__("sys").stdout, "reconfigure"):
        __import__("sys").stdout.reconfigure(encoding="utf-8")
    base.main()
