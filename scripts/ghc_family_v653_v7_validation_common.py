#!/usr/bin/env python3
"""Shared bounded validation helpers for Orin Thale v653-v7."""

from __future__ import annotations

from pathlib import Path

import ghc_family_v653_v2_validation_common as base


REPO = Path(__file__).resolve().parents[1]
PHASE = REPO / "docs/orin-thale/v653-v7"
PHASE_PREFIX = "docs/orin-thale/v653-v7/"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
PRIVACY_PATTERNS = base.PRIVACY_PATTERNS
SCANNER_DEFINITION_FILES = {
    "scripts/ghc_family_v653_v7_validation_common.py",
    "scripts/ghc_family_v653_v7_staged_review.py",
    "scripts/ghc_family_v653_v7_x1_validate.py",
}

base.REPO = REPO
base.PHASE = PHASE
base.PHASE_PREFIX = PHASE_PREFIX
base.ALLOWED_OUTCOMES = ALLOWED_OUTCOMES
base.SCANNER_DEFINITION_FILES = SCANNER_DEFINITION_FILES

read_json = base.read_json
write_json = base.write_json
git = base.git
staged_blob_map = base.staged_blob_map
revision_blob_map = base.revision_blob_map
batch_blob_bytes = base.batch_blob_bytes
sha256_bytes = base.sha256_bytes
scan_privacy_bytes = base.scan_privacy_bytes
scan_privacy_paths = base.scan_privacy_paths


def phase_public_paths() -> list[Path]:
    paths = [path for path in PHASE.rglob("*") if path.is_file()]
    paths.extend(
        path
        for path in (REPO / "scripts").glob("*v653_v7*.py")
        if path.is_file()
    )
    paths.extend(
        path
        for path in (REPO / "tests").glob("test_ghc_family_v653_v7*.py")
        if path.is_file()
    )
    runner_receipt = PHASE / "runners/runner-invocation-receipt.json"
    if runner_receipt.is_file():
        for row in read_json(runner_receipt)["runners"]:
            path = REPO / "scripts" / row["runner"]
            if path.is_file():
                paths.append(path)
    return sorted(set(paths))
