#!/usr/bin/env python3
"""Review and manifest the exact staged Liora Venn v653-v8 evidence delta."""

from __future__ import annotations

import ghc_family_v653_v2_staged_review as base
from ghc_family_v653_v8_validation_common import (
    PHASE,
    PHASE_PREFIX,
    batch_blob_bytes,
    git,
    scan_privacy_bytes,
    sha256_bytes,
    staged_blob_map,
    write_json,
)


REVIEW_PATH = "docs/liora-venn/v653-v8/validation/evidence-staged-review.json"
MANIFEST_PATH = (
    "docs/liora-venn/v653-v8/validation/evidence-candidate-manifest.json"
)
VALIDATION_PATH = (
    "docs/liora-venn/v653-v8/validation/evidence-validation.json"
)
SELF_EXCLUSIONS = {REVIEW_PATH, MANIFEST_PATH, VALIDATION_PATH}
X1_COMMIT = "ee3a0c035c9821ebad1561e94afb11daf9bdc028"

base.PHASE = PHASE
base.PHASE_PREFIX = PHASE_PREFIX
base.REVIEW_PATH = REVIEW_PATH
base.MANIFEST_PATH = MANIFEST_PATH
base.VALIDATION_PATH = VALIDATION_PATH
base.SELF_EXCLUSIONS = SELF_EXCLUSIONS
base.X1_COMMIT = X1_COMMIT
base.batch_blob_bytes = batch_blob_bytes
base.git = git
base.scan_privacy_bytes = scan_privacy_bytes
base.sha256_bytes = sha256_bytes
base.staged_blob_map = staged_blob_map
base.write_json = write_json


def allowed(path: str, runner_names: set[str]) -> bool:
    return (
        path.startswith(PHASE_PREFIX)
        or path.startswith("scripts/ghc_family_v653_v8_")
        or path.startswith("scripts/build_ghc_family_v653_v8_")
        or path.startswith("tests/test_ghc_family_v653_v8_")
        or path in {f"scripts/{name}" for name in runner_names}
    )


base.allowed = allowed

_base_build = base.build


def build():
    result = _base_build()
    result["schema"] = "ghc.family.v653-v8.evidence-staged-review.v1"
    manifest_path = PHASE / "validation/evidence-candidate-manifest.json"
    manifest = manifest_path.read_text(encoding="utf-8")
    manifest = manifest.replace(
        "ghc.family.v653-v2.evidence-candidate-manifest.v1",
        "ghc.family.v653-v8.evidence-candidate-manifest.v1",
    )
    manifest_path.write_text(manifest, encoding="utf-8", newline="\n")
    write_json(PHASE / "validation/evidence-staged-review.json", result)
    return result


base.build = build


if __name__ == "__main__":
    base.main()
