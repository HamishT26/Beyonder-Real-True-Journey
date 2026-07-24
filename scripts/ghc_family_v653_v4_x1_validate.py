#!/usr/bin/env python3
"""Validate the exact staged Auren Lark v653-v4 x1-only packet."""

from __future__ import annotations

from pathlib import Path

import ghc_family_v653_v2_x1_validate as base


REPO = Path(__file__).resolve().parents[1]
PHASE_PREFIX = "docs/auren-lark/v653-v4/"
PHASE = REPO / PHASE_PREFIX
ALLOWED_EXACT = {
    "scripts/ghc_family_v653_v4_phase_data.py",
    "scripts/build_ghc_family_v653_v4_preregistration.py",
    "scripts/ghc_family_v653_v4_x1_validate.py",
    "tests/test_ghc_family_v653_v4_x1.py",
}
RECEIPTS = {
    f"{PHASE_PREFIX}validation/x1-staged-manifest.json",
    f"{PHASE_PREFIX}validation/x1-staged-privacy.json",
    f"{PHASE_PREFIX}validation/x1-staged-review.json",
}

base.REPO = REPO
base.PHASE_PREFIX = PHASE_PREFIX
base.PHASE = PHASE
base.ALLOWED_EXACT = ALLOWED_EXACT
base.RECEIPTS = RECEIPTS

_compute = base.compute


def compute():
    manifest, privacy, review = _compute()
    manifest["schema"] = "ghc.family.v653-v4.x1-staged-manifest.v1"
    privacy["schema"] = "ghc.family.v653-v4.x1-staged-privacy.v1"
    review["schema"] = "ghc.family.v653-v4.x1-staged-review.v1"
    return manifest, privacy, review


base.compute = compute


if __name__ == "__main__":
    base.main()
