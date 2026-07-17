#!/usr/bin/env python3
"""Review staged v647-v7 closeout blobs and build the exact owner manifest."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE_PREFIX = "docs/sable-rook/v647-v7/"
REVIEW = PHASE_PREFIX + "validation/closeout-staged-review.json"
MANIFEST = PHASE_PREFIX + "validation/closeout-staged-manifest.json"
OWNER_MANIFEST = PHASE_PREFIX + "validation/final-owner-manifest.json"
SELF = {REVIEW, MANIFEST, OWNER_MANIFEST}
OWNER_SELF = {path.removeprefix(PHASE_PREFIX) for path in SELF}
FROZEN = {
    PHASE_PREFIX + "x1-proposals.json", PHASE_PREFIX + "x1-preregistration.md",
    PHASE_PREFIX + "approval-packets/x1-approval-portfolio.json", PHASE_PREFIX + "prototypes/x1-skill-runner-plan.json",
    PHASE_PREFIX + "maintenance/x1-clean-refine-plan.json", PHASE_PREFIX + "provenance/prior-proposal-collision-audit.json",
    PHASE_PREFIX + "provenance/prior-portfolio-collision-audit.json", PHASE_PREFIX + "sources/source-ledger.json",
}
ALLOWED_OUTSIDE = {
    "scripts/build_ghc_family_v647_v7_closeout.py",
    "scripts/ghc_family_v647_v7_closeout_staged_review.py",
    "scripts/ghc_family_v647_v7_validation_runner.py",
    "tests/test_ghc_family_v647_v7_closeout.py",
}


def zlist(args: list[str]) -> list[str]:
    raw = subprocess.run(args, cwd=ROOT, check=True, capture_output=True).stdout
    return sorted(item.decode("utf-8") for item in raw.split(b"\0") if item)


def blob(path: str) -> bytes:
    return subprocess.run(["git", "show", f":{path}"], cwd=ROOT, check=True, capture_output=True).stdout


def entry(path: str, relative: bool = False) -> dict:
    data = blob(path)
    git_blob = subprocess.run(["git", "rev-parse", f":{path}"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    return {"path": path.removeprefix(PHASE_PREFIX) if relative else path, "git_blob": git_blob, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}


def write(path: str, data: dict) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    staged = zlist(["git", "diff", "--cached", "--name-only", "-z"])
    owner_paths = zlist(["git", "ls-files", "-z", "--", PHASE_PREFIX])
    allowed = all(path.startswith(PHASE_PREFIX) or path in ALLOWED_OUTSIDE for path in staged)
    frozen_changes = sorted(FROZEN & set(staged))
    privacy = {
        "raw_uuid": re.compile(rb"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}\b"),
        "private_absolute_path": re.compile(rb"\b[A-Za-z]:[\\/]"),
        "credential_assignment": re.compile(rb"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*[^\s,}]+"),
        "delegation_markup": re.compile(("<codex_" + "delegation").encode(), re.IGNORECASE),
        "private_uri": re.compile(("(?:codex|app)" + r"://").encode(), re.IGNORECASE),
    }
    hits = []
    json_count = 0
    for path in staged:
        data = blob(path)
        if path.endswith(".json"):
            json.loads(data.decode("utf-8"))
            json_count += 1
        for kind, pattern in privacy.items():
            if pattern.search(data):
                hits.append({"path": path, "class": kind})
    staged_entries = [entry(path) for path in staged if path not in SELF]
    owner_entries = [entry(path, relative=True) for path in owner_paths if path not in SELF]
    staged_exclusions = len([path for path in staged if path in SELF])
    owner_exclusions = len([path for path in owner_paths if path in SELF])
    diff = subprocess.run(["git", "diff", "--cached", "--check"], cwd=ROOT, capture_output=True, text=True)
    valid = bool(staged) and allowed and not frozen_changes and not hits and diff.returncode == 0 and len(staged_entries) + staged_exclusions == len(staged) and len(owner_entries) + owner_exclusions == len(owner_paths)
    write(MANIFEST, {"schema": "ghc.family.v647-v7.closeout-staged-manifest.v1", "hash_domain": "exact staged Git-index blobs", "staged_path_count": len(staged), "entry_count": len(staged_entries), "self_exclusions": sorted(SELF), "entries": staged_entries})
    write(OWNER_MANIFEST, {"schema": "ghc.family.v647-v7.final-owner-manifest.v1", "hash_domain": "exact prospective final Git-index blobs", "owner_path_count": len(owner_paths), "entry_count": len(owner_entries), "self_exclusions": sorted(OWNER_SELF), "entries": owner_entries, "valid": valid, "boundary": "Prospective final owner-surface parity only; exact final commit validation remains postcommit."})
    review = {"schema": "ghc.family.v647-v7.closeout-staged-review.v1", "staged_path_count": len(staged), "owner_path_count": len(owner_paths), "json_parse_count": json_count, "allowed_surface": allowed, "frozen_x1_path_changes": frozen_changes, "privacy_pattern_classes": sorted(privacy), "confirmed_privacy_hits": hits, "diff_hygiene": diff.returncode == 0, "staged_manifest_entries": len(staged_entries), "owner_manifest_entries": len(owner_entries), "self_exclusion_count": staged_exclusions, "valid": valid, "boundary": "Exact prospective closeout structural review only; not final-head proof or independent reproduction."}
    write(REVIEW, review)
    print(json.dumps(review, ensure_ascii=False))
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
