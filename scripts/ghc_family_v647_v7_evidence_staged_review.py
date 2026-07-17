#!/usr/bin/env python3
"""Review exact staged v647-v7 evidence blobs and emit a fixed-point manifest."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW = "docs/sable-rook/v647-v7/validation/evidence-staged-review.json"
MANIFEST = "docs/sable-rook/v647-v7/validation/evidence-staged-manifest.json"
SELF_EXCLUSIONS = {REVIEW, MANIFEST}
FROZEN = {
    "docs/sable-rook/v647-v7/x1-proposals.json",
    "docs/sable-rook/v647-v7/x1-preregistration.md",
    "docs/sable-rook/v647-v7/approval-packets/x1-approval-portfolio.json",
    "docs/sable-rook/v647-v7/prototypes/x1-skill-runner-plan.json",
    "docs/sable-rook/v647-v7/maintenance/x1-clean-refine-plan.json",
    "docs/sable-rook/v647-v7/provenance/prior-proposal-collision-audit.json",
    "docs/sable-rook/v647-v7/provenance/prior-portfolio-collision-audit.json",
    "docs/sable-rook/v647-v7/sources/source-ledger.json",
}
ALLOWED_SCRIPTS = {
    "scripts/build_ghc_family_v647_v7_evidence.py",
    "scripts/ghc_family_v647_v7_runtime.py",
    "scripts/ghc_family_v647_v7_validation_runner.py",
    "scripts/ghc_family_v647_v7_evidence_staged_review.py",
    "scripts/ghc_family_in_toto_provenance_tribunal.py",
    "scripts/ghc_family_picard_lefschetz_obligations.py",
    "scripts/ghc_family_spt3g_d1_zero_row.py",
    "scripts/ghc_family_building_inspection_handover.py",
    "scripts/ghc_family_oauth_resource_metadata.py",
    "scripts/ghc_family_dns_wire_tribunal.py",
    "scripts/ghc_family_virtualized_feed_audit.py",
    "scripts/ghc_family_fugacity_domain_guard.py",
    "scripts/ghc_family_rosenbaum_nonpromotion.py",
}
ALLOWED_TESTS = {"tests/test_ghc_family_v647_v7_x1.py", "tests/test_ghc_family_v647_v7.py"}


def paths() -> list[str]:
    raw = subprocess.run(["git", "diff", "--cached", "--name-only", "-z"], cwd=ROOT, check=True, capture_output=True).stdout
    return sorted(item.decode("utf-8") for item in raw.split(b"\0") if item)


def blob(path: str) -> bytes:
    return subprocess.run(["git", "show", f":{path}"], cwd=ROOT, check=True, capture_output=True).stdout


def write(path: str, data: dict) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    staged = paths()
    allowed = all(path.startswith("docs/sable-rook/v647-v7/") or path in ALLOWED_SCRIPTS or path in ALLOWED_TESTS for path in staged)
    frozen_changes = sorted(FROZEN & set(staged))
    entries = []
    json_count = 0
    hits = []
    privacy = {
        "raw_uuid": re.compile(rb"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}\b"),
        "private_absolute_path": re.compile(rb"\b[A-Za-z]:[\\/]"),
        "credential_assignment": re.compile(rb"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*[^\s,}]+"),
        "delegation_markup": re.compile(("<codex_" + "delegation").encode(), re.IGNORECASE),
        "private_uri": re.compile(("(?:codex|app)" + r"://").encode(), re.IGNORECASE),
    }
    for path in staged:
        data = blob(path)
        if path.endswith(".json"):
            json.loads(data.decode("utf-8"))
            json_count += 1
        for kind, pattern in privacy.items():
            if pattern.search(data):
                hits.append({"path": path, "class": kind})
        if path not in SELF_EXCLUSIONS:
            git_blob = subprocess.run(["git", "rev-parse", f":{path}"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
            entries.append({"path": path, "git_blob": git_blob, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
    diff = subprocess.run(["git", "diff", "--cached", "--check"], cwd=ROOT, capture_output=True, text=True)
    exclusion_count = len([path for path in staged if path in SELF_EXCLUSIONS])
    valid = bool(staged) and allowed and not frozen_changes and not hits and diff.returncode == 0 and len(entries) + exclusion_count == len(staged)
    manifest = {"schema": "ghc.family.v647-v7.evidence-staged-manifest.v1", "hash_domain": "exact staged Git-index blobs", "staged_path_count": len(staged), "entry_count": len(entries), "self_exclusions": sorted(SELF_EXCLUSIONS), "entries": entries}
    review = {"schema": "ghc.family.v647-v7.evidence-staged-review.v1", "staged_path_count": len(staged), "json_parse_count": json_count, "allowed_surface": allowed, "frozen_x1_path_changes": frozen_changes, "privacy_pattern_classes": sorted(privacy), "confirmed_privacy_hits": hits, "diff_hygiene": diff.returncode == 0, "manifest_entry_count": len(entries), "self_exclusion_count": exclusion_count, "valid": valid, "boundary": "Exact evidence-stage structural review only; not complete privacy assurance or independent reproduction."}
    write(MANIFEST, manifest)
    write(REVIEW, review)
    print(json.dumps(review, ensure_ascii=False))
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
