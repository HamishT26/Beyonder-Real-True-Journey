#!/usr/bin/env python3
"""Collision-free byte-preserving promotion for Orin v687-v7 skills/runners."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "orin-thale" / "v687-v7"
OPERATIONS = ["spectral_axis_monotonicity", "spectral_unit_roundtrip", "flux_missingness_boundary", "spectral_bin_topology", "calibration_lineage_expiry", "spectral_segment_fixity", "uncertainty_covariance_shape", "provenance_frontier", "accessible_spectrum_summary", "release_authority_reservation"]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def files(root: Path):
    return sorted(path for path in root.rglob("*") if path.is_file())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skill-root", type=Path, required=True)
    ap.add_argument("--runner-root", type=Path, required=True)
    ap.add_argument("--quick-validate", type=Path, required=True)
    ap.add_argument("--scratch", type=Path, required=True)
    args = ap.parse_args()
    receipt = PHASE / "x2" / "promotion-receipt.json"
    current = json.loads(receipt.read_text(encoding="utf-8"))
    if current.get("status") != "PENDING_COLLISION_FREE_PROMOTION":
        raise RuntimeError("promotion already attempted or complete")
    skill_names = ["ghc-family-" + op.replace("_", "-") for op in OPERATIONS]
    runner_names = [f"ghc_family_spectral_archive_{i:02d}_runner.py" for i in range(1, 6)]
    core_name = "ghc_family_spectral_archive_contract.py"
    destinations = [args.skill_root / name for name in skill_names] + [args.runner_root / name for name in runner_names + [core_name]]
    collisions = [str(path.name) for path in destinations if path.exists()]
    if collisions:
        raise RuntimeError(f"promotion collision: {collisions}")
    args.scratch.mkdir(parents=True, exist_ok=True)
    members = []
    for name in skill_names:
        source = PHASE / "skills" / name
        destination = args.skill_root / name
        shutil.copytree(source, destination)
        result = subprocess.run([sys.executable, "-X", "utf8", str(args.quick_validate), str(destination)], capture_output=True, text=True, encoding="utf-8", check=False, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONUTF8": "1"})
        if result.returncode:
            raise RuntimeError(f"global skill validation failed: {name}: {result.stdout} {result.stderr}")
        for src in files(source):
            relative = src.relative_to(source); dst = destination / relative
            if src.read_bytes() != dst.read_bytes():
                raise RuntimeError(f"skill parity mismatch: {name}/{relative}")
            members.append({"kind": "skill", "name": name, "relative": relative.as_posix(), "source": src.relative_to(ROOT).as_posix(), "sha256": sha(src)})
    for name in runner_names + [core_name]:
        source = ROOT / "scripts" / name; destination = args.runner_root / name
        shutil.copy2(source, destination)
        if source.read_bytes() != destination.read_bytes():
            raise RuntimeError(f"runner parity mismatch: {name}")
        members.append({"kind": "runner" if name in runner_names else "core_dependency", "name": name, "relative": name, "source": source.relative_to(ROOT).as_posix(), "sha256": sha(source)})
    # Smoke-use each global runner once with one matching synthetic fixture.
    smokes = []
    proposals = json.loads((PHASE / "x1" / "new-proposals.json").read_text(encoding="utf-8"))["proposals"]
    for no, name in enumerate(runner_names, 1):
        row = proposals[(no - 1) * 40]
        fixture = args.scratch / f"runner-{no:02d}.json"
        fixture.write_text(json.dumps(row["input"], ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        result = subprocess.run([sys.executable, str(args.runner_root / name), "--input", str(fixture)], cwd=args.runner_root, capture_output=True, text=True, encoding="utf-8", check=False, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONUTF8": "1"})
        matched = result.returncode == 0 and json.loads(result.stdout) == row["expected_output"]
        if not matched:
            raise RuntimeError(f"global runner smoke failed: {name}")
        smokes.append({"runner": name, "operation": row["operation"], "matched": True})
    value = {"schema": "ghc.family.promotion-receipt.v1", "status": "PROMOTED_COLLISION_FREE_VALIDATED_AND_USED", "skills": len(skill_names), "runners": len(runner_names), "core_dependencies": 1, "members": members, "member_count": len(members), "collisions": [], "overwrites": 0, "global_runner_smokes": smokes, "same_owner_shared_infrastructure": True, "independent_reproduction": False, "rollback": "Stop selecting the promoted package; preserve source and global bytes."}
    receipt.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": value["status"], "skills": len(skill_names), "runners": len(runner_names), "members": len(members), "smokes": len(smokes)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
