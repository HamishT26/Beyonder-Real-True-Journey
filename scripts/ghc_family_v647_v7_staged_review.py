#!/usr/bin/env python3
"""Review exact staged v647-v7 x1 blobs and emit a self-excluding manifest."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/sable-rook/v647-v7"
REVIEW = "docs/sable-rook/v647-v7/validation/x1-staged-review.json"
MANIFEST = "docs/sable-rook/v647-v7/validation/x1-staged-manifest.json"
SELF_EXCLUSIONS = {REVIEW, MANIFEST}


def staged_paths() -> list[str]:
    raw = subprocess.run(["git", "diff", "--cached", "--name-only", "-z"], cwd=ROOT, check=True, capture_output=True).stdout
    return sorted(item.decode("utf-8") for item in raw.split(b"\0") if item)


def staged_bytes(path: str) -> bytes:
    return subprocess.run(["git", "show", f":{path}"], cwd=ROOT, check=True, capture_output=True).stdout


def write(relative: str, payload: dict) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    paths = staged_paths()
    allowed = all(
        path.startswith("docs/sable-rook/v647-v7/")
        or re.fullmatch(r"scripts/(?:build_)?ghc_family_v647_v7_[a-z0-9_]+\.py", path)
        or path == "tests/test_ghc_family_v647_v7_x1.py"
        for path in paths
    )
    entries = []
    json_count = 0
    candidates = []
    forbidden_credit = ("x2_completion" + "_credit\": true").encode("utf-8")
    privacy = {
        "raw_uuid": re.compile(rb"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}\b"),
        "private_absolute_path": re.compile(rb"\b[A-Za-z]:[\\/]"),
        "credential_assignment": re.compile(rb"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*[^\s,}]+"),
        "delegation_markup": re.compile(("<codex_" + "delegation").encode(), re.IGNORECASE),
        "private_uri": re.compile(("(?:codex|app)" + r"://").encode(), re.IGNORECASE),
    }
    x2_credit_hits = []
    for path in paths:
        data = staged_bytes(path)
        if path.endswith(".json"):
            json.loads(data.decode("utf-8"))
            json_count += 1
        if forbidden_credit in data.lower():
            x2_credit_hits.append(path)
        for kind, pattern in privacy.items():
            for _ in pattern.finditer(data):
                candidates.append({"path": path, "class": kind, "confirmed_payload_hit": True})
        if path not in SELF_EXCLUSIONS:
            blob = subprocess.run(["git", "rev-parse", f":{path}"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
            entries.append({"path": path, "git_blob": blob, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
    diff = subprocess.run(["git", "diff", "--cached", "--check"], cwd=ROOT, capture_output=True, text=True)
    manifest = {
        "schema": "ghc.family.v647-v7.x1-staged-manifest.v1", "hash_domain": "exact staged Git-index blobs",
        "staged_path_count": len(paths), "entry_count": len(entries), "self_exclusions": sorted(SELF_EXCLUSIONS),
        "entries": entries,
    }
    valid = bool(paths) and allowed and not candidates and not x2_credit_hits and diff.returncode == 0 and len(entries) + len([p for p in paths if p in SELF_EXCLUSIONS]) == len(paths)
    review = {
        "schema": "ghc.family.v647-v7.x1-staged-review.v1", "staged_path_count": len(paths),
        "json_parse_count": json_count, "allowed_surface": allowed, "privacy_pattern_classes": sorted(privacy),
        "privacy_candidates": candidates, "confirmed_privacy_hits": len(candidates), "x2_credit_hits": x2_credit_hits,
        "diff_hygiene": diff.returncode == 0, "manifest_entry_count": len(entries), "self_exclusion_count": len([p for p in paths if p in SELF_EXCLUSIONS]),
        "valid": valid, "boundary": "Exact staged-blob structural review only; it is not complete privacy assurance or independent reproduction.",
    }
    write(MANIFEST, manifest)
    write(REVIEW, review)
    print(json.dumps(review, ensure_ascii=False))
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
