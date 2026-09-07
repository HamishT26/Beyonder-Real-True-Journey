#!/usr/bin/env python3
"""Bind the pycache-remediated Orin v687-v7 global promotion."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "orin-thale" / "v687-v7"
OPERATIONS = ["spectral_axis_monotonicity", "spectral_unit_roundtrip", "flux_missingness_boundary", "spectral_bin_topology", "calibration_lineage_expiry", "spectral_segment_fixity", "uncertainty_covariance_shape", "provenance_frontier", "accessible_spectrum_summary", "release_authority_reservation"]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skill-root", type=Path, required=True)
    ap.add_argument("--runner-root", type=Path, required=True)
    args = ap.parse_args()
    source_receipt = PHASE / "x2" / "promotion-receipt.json"
    original = json.loads(source_receipt.read_text(encoding="utf-8"))
    if original.get("status") != "PROMOTED_COLLISION_FREE_VALIDATED_AND_USED" or original.get("member_count") != 66:
        raise RuntimeError("unexpected original promotion receipt")
    members = []
    for operation in OPERATIONS:
        name = "ghc-family-" + operation.replace("_", "-")
        local = PHASE / "skills" / name
        global_root = args.skill_root / name
        if list(local.rglob("__pycache__")) or list(global_root.rglob("__pycache__")):
            raise RuntimeError(f"pycache remains: {name}")
        local_files = sorted(path for path in local.rglob("*") if path.is_file())
        if len(local_files) != 5:
            raise RuntimeError(f"unexpected local member count: {name}: {len(local_files)}")
        for source in local_files:
            relative = source.relative_to(local); destination = global_root / relative
            if not destination.is_file() or source.read_bytes() != destination.read_bytes():
                raise RuntimeError(f"corrected parity mismatch: {name}/{relative}")
            members.append({"kind": "skill", "name": name, "relative": relative.as_posix(), "source": source.relative_to(ROOT).as_posix(), "sha256": sha(source)})
    for name in [f"ghc_family_spectral_archive_{i:02d}_runner.py" for i in range(1, 6)] + ["ghc_family_spectral_archive_contract.py"]:
        source = ROOT / "scripts" / name; destination = args.runner_root / name
        if not destination.is_file() or source.read_bytes() != destination.read_bytes():
            raise RuntimeError(f"corrected runner parity mismatch: {name}")
        members.append({"kind": "runner" if "_runner" in name else "core_dependency", "name": name, "relative": name, "source": source.relative_to(ROOT).as_posix(), "sha256": sha(source)})
    receipt = PHASE / "x2" / "promotion-correction-receipt.json"
    if receipt.exists():
        raise RuntimeError("promotion correction already exists")
    value = {"schema": "ghc.family.promotion-correction.v1", "status": "CORRECTED_PROMOTION_PRIVACY_CLEAN", "retained_negative_id": "OR6877-X2-N003", "original_receipt_sha256": sha(source_receipt), "original_member_count": 66, "removed_generated_local_pycache_files": 10, "removed_generated_global_pycache_files": 10, "final_member_count": len(members), "members": members, "all_source_global_bytes_equal": True, "original_receipt_rewritten": False, "same_owner_shared_infrastructure": True, "independent_reproduction": False}
    receipt.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": value["status"], "final_members": len(members)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
