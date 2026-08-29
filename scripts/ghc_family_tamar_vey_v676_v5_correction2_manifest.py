#!/usr/bin/env python3
"""Build second additive-correction manifests from the staged Tamar index."""

from __future__ import annotations

import json
from pathlib import Path

from scripts.ghc_family_tamar_vey_v676_v5_correction_manifest import (
    PRIVACY_PATTERNS,
    SOURCE,
    allowed,
    blob,
    dump,
    entry,
    git,
    index_map,
    normalized,
)


BASE = "8d64b74e2f92c0675addf6fcc10e68f8c774e3e8"
OWNER_PREFIX = "docs/tamar-vey/v676-v5/"
DELTA_PATH = OWNER_PREFIX + "validation/correction2-delta-manifest.json"
OWNER_PATH = OWNER_PREFIX + "validation/correction2-owner-manifest.json"
REVIEW_PATH = OWNER_PREFIX + "validation/correction2-staged-review.json"
SELF_EXCLUSIONS = [
    {"path": DELTA_PATH, "reason": "self-referential second-correction delta manifest"},
    {"path": OWNER_PATH, "reason": "self-referential second-correction owner manifest"},
    {"path": REVIEW_PATH, "reason": "self-referential second-correction staged review"},
]
PRIVACY_EXCLUSIONS = {
    DELTA_PATH,
    OWNER_PATH,
    REVIEW_PATH,
    OWNER_PREFIX + "validation/final-delta-manifest.json",
    OWNER_PREFIX + "validation/final-owner-manifest.json",
    OWNER_PREFIX + "validation/final-staged-review.json",
    OWNER_PREFIX + "validation/correction-delta-manifest.json",
    OWNER_PREFIX + "validation/correction-owner-manifest.json",
    OWNER_PREFIX + "validation/correction-staged-review.json",
}


def main() -> None:
    repo = Path(__file__).resolve().parents[1]
    if git(repo, "rev-parse", "HEAD") != BASE:
        raise SystemExit("second-correction manifests must be built at the first correction head")
    staged = sorted(path for path in git(repo, "diff", "--cached", "--name-only", "--diff-filter=ACMR", BASE, "--").splitlines() if path)
    exclusions = {row["path"] for row in SELF_EXCLUSIONS}
    staged_input = sorted(path for path in staged if path not in exclusions)
    unexpected = sorted(path for path in staged if not allowed(path))
    if unexpected:
        raise SystemExit(f"unexpected second-correction paths: {unexpected!r}")
    required = {
        OWNER_PREFIX + "correction2/correction-receipt.json",
        OWNER_PREFIX + "correction2/phase-truth.json",
        OWNER_PREFIX + "correction2/method-flow-overlay.json",
        OWNER_PREFIX + "correction2/content-seal.json",
        OWNER_PREFIX + "handoffs/elowen-cairn-v676-v6-activation-candidate-corrected2.md",
        OWNER_PREFIX + "orchestration/terminal-route-hold-corrected2.json",
        "scripts/ghc_family_tamar_vey_v676_v5_final_validator.py",
        "tests/test_ghc_family_tamar_vey_v676_v5_correction2.py",
    }
    if not required.issubset(staged_input):
        raise SystemExit(f"missing second-correction paths: {sorted(required - set(staged_input))!r}")
    committed = {
        path for path in git(repo, "diff", "--name-only", "--diff-filter=ACMR", SOURCE, BASE, "--").splitlines()
        if path and allowed(path)
    }
    owner_paths = sorted((committed | set(staged)) - exclusions)
    index = index_map(repo)
    missing = sorted(path for path in owner_paths if path not in index)
    if missing:
        raise SystemExit(f"second-correction owner paths missing from index: {missing[:10]!r}")
    delta_entries = [entry(repo, path, index[path]) for path in staged_input]
    owner_entries = [entry(repo, path, index[path]) for path in owner_paths]
    candidates = []
    for path in owner_paths:
        if path in PRIVACY_EXCLUSIONS or not path.endswith((".py", ".json", ".md", ".html", ".txt", ".yaml", ".yml")):
            continue
        raw = normalized(blob(repo, index[path]))
        for category, pattern in PRIVACY_PATTERNS.items():
            if pattern.search(raw):
                metadata = path.endswith(".py") or path.endswith("-staged-review.json") or path.endswith("privacy-adjudication.json")
                candidates.append({"path": path, "category": category, "adjudication": "scanner_definition_or_adjudication_metadata" if metadata else "confirmed_payload_hit"})
    confirmed = [row for row in candidates if row["adjudication"] == "confirmed_payload_hit"]
    if confirmed:
        raise SystemExit(f"confirmed second-correction privacy hits: {confirmed!r}")
    common = {
        "owner": "Tamar Vey",
        "phase": "v676-v5-second-additive-correction",
        "source": SOURCE,
        "first_correction_final": BASE,
        "normalization_domain": "Git index bytes normalized CRLF and CR to LF for SHA-256; Git blob OID uses exact index bytes",
        "declared_exclusions": SELF_EXCLUSIONS,
    }
    validation = repo / OWNER_PREFIX / "validation"
    dump(validation / "correction2-delta-manifest.json", {**common, "manifest_kind": "precommit_second_correction_delta_git_blob_manifest", "range_start": BASE, "entry_count": len(delta_entries), "entries": delta_entries})
    dump(validation / "correction2-owner-manifest.json", {**common, "manifest_kind": "precommit_source_to_second_corrected_final_owner_git_blob_manifest", "range_start": SOURCE, "entry_count": len(owner_entries), "entries": owner_entries})
    dump(validation / "correction2-staged-review.json", {
        "source": SOURCE,
        "first_correction_final": BASE,
        "staged_input_count": len(staged_input),
        "owner_input_count": len(owner_paths),
        "declared_self_exclusions": SELF_EXCLUSIONS,
        "unexpected_paths": unexpected,
        "privacy_classes": sorted(PRIVACY_PATTERNS),
        "privacy_candidates": candidates,
        "privacy_candidate_count": len(candidates),
        "confirmed_five_class_privacy_or_raw_identifier_hits": 0,
        "exact_staged_review": True,
        "status": "VALID_PRECOMMIT_SECOND_ADDITIVE_CORRECTION_STAGED_REVIEW",
    })
    print(json.dumps({"status": "VALID_PRECOMMIT_SECOND_CORRECTION_MANIFESTS", "delta_entries": len(delta_entries), "owner_entries": len(owner_entries), "privacy_candidates": len(candidates), "confirmed_hits": 0}, sort_keys=True))


if __name__ == "__main__":
    main()
