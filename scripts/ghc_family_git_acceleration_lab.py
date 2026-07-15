#!/usr/bin/env python3
"""Exercise Git acceleration structures in a new disposable local repository."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def run(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8").stdout.strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lab-dir", type=Path, required=True)
    parser.add_argument("--canonical-repo", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    if args.lab_dir.exists():
        raise SystemExit("lab directory already exists; refusing reuse")
    canonical_before = run(args.canonical_repo, "rev-parse", "HEAD")
    args.lab_dir.mkdir(parents=True)
    run(args.lab_dir, "init", "--initial-branch=main")
    run(args.lab_dir, "config", "user.name", "GHC Fixture")
    run(args.lab_dir, "config", "user.email", "fixture.invalid@example.invalid")
    for index in range(1, 7):
        (args.lab_dir / f"fixture-{index:02d}.txt").write_text(f"fixture generation one {index}\n", encoding="utf-8", newline="\n")
        run(args.lab_dir, "add", ".")
        run(args.lab_dir, "commit", "-m", f"fixture one {index}")
    run(args.lab_dir, "repack", "-ad")
    for index in range(7, 13):
        (args.lab_dir / f"fixture-{index:02d}.txt").write_text(f"fixture generation two {index}\n", encoding="utf-8", newline="\n")
        run(args.lab_dir, "add", ".")
        run(args.lab_dir, "commit", "-m", f"fixture two {index}")
    run(args.lab_dir, "repack", "-d")
    pack_dir = args.lab_dir / ".git/objects/pack"
    pack_count = len(list(pack_dir.glob("*.pack")))
    run(args.lab_dir, "commit-graph", "write", "--reachable", "--changed-paths")
    run(args.lab_dir, "commit-graph", "verify")
    run(args.lab_dir, "multi-pack-index", "write", "--bitmap")
    run(args.lab_dir, "multi-pack-index", "verify")
    run(args.lab_dir, "fsck", "--strict")
    canonical_after = run(args.canonical_repo, "rev-parse", "HEAD")
    receipt = {
        "schema": "ghc.family.git-acceleration-lab.v1", "fixture_commit_count": 12,
        "pack_count": pack_count, "commit_graph_verified": True, "multi_pack_index_verified": True,
        "reachability_bitmap_requested": True, "strict_fsck_passed": True,
        "canonical_head_unchanged": canonical_before == canonical_after,
        "lab_retained_local_only": True, "same_owner_only": True, "independent_reproduction": False,
        "valid": pack_count >= 2 and canonical_before == canonical_after,
        "boundary": "The additive local fixture does not establish canonical-repository security, production performance, or independent reproduction.",
    }
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(receipt, indent=2))
    if not receipt["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
