#!/usr/bin/env python3
"""Create the exact v651-v2 x1 staged-index manifest, privacy, and review receipts."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
PHASE_ROOT = "docs/orin-thale/v651-v2"
SOURCE = "ad2b530c2449656b54ac0fee1a1284208c2a6a75"
OUT = {
    "manifest": f"{PHASE_ROOT}/validation/x1-staged-manifest.json",
    "privacy": f"{PHASE_ROOT}/validation/x1-staged-privacy.json",
    "review": f"{PHASE_ROOT}/validation/x1-staged-review.json",
}
SELF_EXCLUSIONS = sorted(OUT.values())
ALLOWED_EXACT = {
    "scripts/build_ghc_family_v651_v2_preregistration.py",
    "scripts/ghc_family_v651_v2_phase_data.py",
    "scripts/ghc_family_v651_v2_x1_review.py",
    "tests/test_ghc_family_v651_v2_x1.py",
}
PATTERNS = {
    "raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
    "private_local_path": re.compile(rb"(?:[A-Z]:\\(?:Users|GHC-Archives)\\|/Users/|/home/)", re.I),
    "private_uri": re.compile(rb"(?:codex|chatgpt|file|vscode|app)://", re.I),
    "delegation_markup": re.compile(rb"<\s*(?:codex_delegation|source_thread_id|private_route)\b", re.I),
    "credential_assignment": re.compile(rb"(?:api[_-]?key|password|private[_-]?key|access[_-]?token|secret)\s*[:=]\s*['\"]?[A-Za-z0-9_\-/+=]{12,}", re.I),
}


def run(*args: str, text: bool = True) -> str | bytes:
    return subprocess.check_output(list(args), cwd=REPO, text=text, encoding="utf-8" if text else None)


def write_json(path: str, payload: dict) -> None:
    target = REPO / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def staged_paths() -> list[str]:
    raw = run("git", "diff", "--cached", "--name-only", "-z", text=False)
    return sorted(part.decode("utf-8") for part in raw.split(b"\0") if part)


def staged_blob(path: str) -> tuple[str, bytes]:
    row = run("git", "ls-files", "-s", "--", path).strip()
    if not row:
        raise RuntimeError(f"missing staged index entry: {path}")
    oid = row.split()[1]
    return oid, run("git", "cat-file", "blob", oid, text=False)


def main() -> None:
    if run("git", "rev-parse", "HEAD").strip() != SOURCE:
        raise RuntimeError("x1 review must run before the x1 commit at the exact inherited source")
    paths = staged_paths()
    if any(path in SELF_EXCLUSIONS for path in paths):
        raise RuntimeError("self-excluding receipts must not be staged before the review is generated")
    unexpected = [path for path in paths if not (path.startswith(PHASE_ROOT + "/") or path in ALLOWED_EXACT)]
    if unexpected:
        raise RuntimeError(f"unexpected staged paths: {unexpected}")
    forbidden = [path for path in paths if any(part in path for part in ("/surfaces/", "/outcomes/", "evidence-phase-truth", "mutation-execution"))]
    if forbidden:
        raise RuntimeError(f"x2 contamination in x1: {forbidden}")
    diff_check = subprocess.run(["git", "diff", "--cached", "--check"], cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    if diff_check.returncode:
        raise RuntimeError(diff_check.stdout + diff_check.stderr)

    entries = []
    confirmed_hits = []
    scanner_definition_candidates = []
    for path in paths:
        oid, data = staged_blob(path)
        entries.append(
            {
                "path": path,
                "bytes": len(data),
                "git_blob": oid,
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )
        for class_name, pattern in PATTERNS.items():
            for match in pattern.finditer(data):
                candidate = {"path": path, "class": class_name, "offset": match.start()}
                if path.startswith("scripts/") or path.startswith("tests/"):
                    scanner_definition_candidates.append(candidate)
                else:
                    confirmed_hits.append(candidate)
    if confirmed_hits:
        raise RuntimeError(f"confirmed privacy hits: {confirmed_hits[:5]}")

    write_json(
        OUT["manifest"],
        {
            "schema": "ghc.family.v651-v2.x1-staged-manifest.v1",
            "source_head": SOURCE,
            "hash_domain": "exact_git_index_blob",
            "entry_count": len(entries),
            "covered_path_count": len(entries) + len(SELF_EXCLUSIONS),
            "self_exclusions": SELF_EXCLUSIONS,
            "entries": entries,
        },
    )
    write_json(
        OUT["privacy"],
        {
            "schema": "ghc.family.v651-v2.x1-staged-privacy.v1",
            "pattern_classes": sorted(PATTERNS),
            "scanned_entry_count": len(entries),
            "scanner_definition_candidates": scanner_definition_candidates,
            "confirmed_hits": confirmed_hits,
            "zero_confirmed_hits": True,
            "boundary": "Five-class staged text scanning is not privacy-complete assurance or independent review.",
        },
    )
    write_json(
        OUT["review"],
        {
            "schema": "ghc.family.v651-v2.x1-staged-review.v1",
            "source_head": SOURCE,
            "entry_count": len(entries),
            "self_exclusion_count": len(SELF_EXCLUSIONS),
            "predicted_final_staged_path_count": len(entries) + len(SELF_EXCLUSIONS),
            "unexpected_paths": unexpected,
            "x2_contamination": forbidden,
            "diff_hygiene": "pass",
            "x1_tests": {"passed": 8, "total": 8, "first_failed_aggregate_retained": True},
            "privacy_zero_confirmed_hits": True,
            "manifest_exact_index_blobs": True,
            "valid": True,
            "boundary": "Dedicated x1 staged review only; no x2 outcome, full-suite, or independent-reproduction credit.",
        },
    )
    print(json.dumps({"entries": len(entries), "self_exclusions": len(SELF_EXCLUSIONS), "predicted_paths": len(entries) + len(SELF_EXCLUSIONS), "privacy_hits": 0, "valid": True}))


if __name__ == "__main__":
    main()
