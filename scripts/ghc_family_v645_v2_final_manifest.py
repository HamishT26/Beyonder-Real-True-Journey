#!/usr/bin/env python3
"""Build the exact staged-index manifest for Sylven Arc v645-v2 finalization."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


PHASE = "v645-gmut-thos-v2-x1-x2"
OUTPUT = "docs/sylven-arc/v645-v2/reproduction/final-staged-manifest.json"
EXCLUDED = {
    OUTPUT,
    "docs/sylven-arc/v645-v2/validation/final-candidate-detailed.json",
    "docs/sylven-arc/v645-v2/validation/final-candidate-minimal.json",
    "docs/sylven-arc/v645-v2/validation/final-privacy-scan.json",
    "docs/sylven-arc/v645-v2/validation/final-staged-review.json",
}
ROOTS = [
    "docs/sylven-arc/v645-v2",
    "scripts/build_ghc_family_v645_v2_preregistration.py",
    "scripts/ghc_family_index_stage_guard.py",
    "scripts/ghc_family_v645_v2_evidence.py",
    "scripts/ghc_family_v645_v2_final_manifest.py",
    "scripts/ghc_family_v645_v2_model.py",
    "scripts/ghc_family_v645_v2_staged_review.py",
    "scripts/ghc_family_v645_v2_validator.py",
    "scripts/ghc_family_v645_v2_x1_definitions.py",
    "scripts/ghc_family_v645_v2_x1_staged_review.py",
    "tests/test_ghc_family_v645_v2_x1.py",
    "tests/test_ghc_family_v645_v2.py",
]


def git(repo: Path, *args: str) -> bytes:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True).stdout


def build(repo: Path) -> dict:
    raw = git(repo, "ls-files", "-z", "--", *ROOTS)
    paths = sorted(
        item.decode("utf-8") for item in raw.split(b"\0") if item and item.decode("utf-8") not in EXCLUDED
    )
    entries = []
    for relative in paths:
        data = git(repo, "show", f":{relative}")
        entries.append({"path": relative, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
    return {
        "schema": "ghc.family.v645-v2.final-staged-manifest.v1",
        "phase": PHASE,
        "target": "INDEX",
        "target_kind": "staged_index",
        "hash_domain": "exact staged Git blob bytes",
        "roots": ROOTS,
        "excluded_self_referential_receipts": sorted(EXCLUDED),
        "entry_count": len(entries),
        "entries": entries,
        "same_owner_repeatability_only": True,
        "independent_reproduction": False,
        "boundary": "The explicit receipt exclusions prevent self-referential hashes; this is change-detection evidence, not a signature or independent reproduction.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, default=Path(OUTPUT))
    args = parser.parse_args()
    repo = args.repo.resolve()
    payload = build(repo)
    output = args.output if args.output.is_absolute() else repo / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"entries": payload["entry_count"], "excluded": len(EXCLUDED), "output": str(args.output)}))


if __name__ == "__main__":
    main()
