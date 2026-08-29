#!/usr/bin/env python3
"""Build third additive-correction manifests from the staged Tamar index."""

from __future__ import annotations

import json
from pathlib import Path

from scripts.ghc_family_tamar_vey_v676_v5_correction_manifest import PRIVACY_PATTERNS, SOURCE, allowed, blob, dump, entry, git, index_map, normalized


BASE = "2133ec23c7226b4614abd1b63818136dd02202bd"
OWNER_PREFIX = "docs/tamar-vey/v676-v5/"
DELTA_PATH = OWNER_PREFIX + "validation/correction3-delta-manifest.json"
OWNER_PATH = OWNER_PREFIX + "validation/correction3-owner-manifest.json"
REVIEW_PATH = OWNER_PREFIX + "validation/correction3-staged-review.json"
SELF_EXCLUSIONS = [
    {"path": DELTA_PATH, "reason": "self-referential third-correction delta manifest"},
    {"path": OWNER_PATH, "reason": "self-referential third-correction owner manifest"},
    {"path": REVIEW_PATH, "reason": "self-referential third-correction staged review"},
]
PRIVACY_EXCLUSIONS = {
    OWNER_PREFIX + f"validation/{stem}{suffix}"
    for stem in ("final", "correction", "correction2", "correction3")
    for suffix in ("-delta-manifest.json", "-owner-manifest.json", "-staged-review.json")
}


def main() -> None:
    repo = Path(__file__).resolve().parents[1]
    if git(repo, "rev-parse", "HEAD") != BASE:
        raise SystemExit("third-correction manifests must be built at the second correction head")
    staged = sorted(path for path in git(repo, "diff", "--cached", "--name-only", "--diff-filter=ACMR", BASE, "--").splitlines() if path)
    exclusions = {row["path"] for row in SELF_EXCLUSIONS}
    staged_input = sorted(path for path in staged if path not in exclusions)
    unexpected = sorted(path for path in staged if not allowed(path))
    if unexpected:
        raise SystemExit(f"unexpected third-correction paths: {unexpected!r}")
    required = {
        OWNER_PREFIX + "correction3/correction-receipt.json",
        OWNER_PREFIX + "correction3/phase-truth.json",
        OWNER_PREFIX + "correction3/method-flow-overlay.json",
        OWNER_PREFIX + "correction3/content-seal.json",
        OWNER_PREFIX + "handoffs/elowen-cairn-v676-v6-activation-candidate-corrected3.md",
        OWNER_PREFIX + "orchestration/terminal-route-hold-corrected3.json",
        "scripts/ghc_family_tamar_vey_v676_v5_final_validator.py",
        "tests/test_ghc_family_tamar_vey_v676_v5_correction3.py",
    }
    if not required.issubset(staged_input):
        raise SystemExit(f"missing third-correction paths: {sorted(required - set(staged_input))!r}")
    committed = {path for path in git(repo, "diff", "--name-only", "--diff-filter=ACMR", SOURCE, BASE, "--").splitlines() if path and allowed(path)}
    owner_paths = sorted((committed | set(staged)) - exclusions)
    index = index_map(repo)
    missing = sorted(path for path in owner_paths if path not in index)
    if missing:
        raise SystemExit(f"third-correction paths missing from index: {missing[:10]!r}")
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
        raise SystemExit(f"confirmed third-correction privacy hits: {confirmed!r}")
    common = {"owner": "Tamar Vey", "phase": "v676-v5-third-additive-correction", "source": SOURCE, "second_correction_final": BASE, "normalization_domain": "Git index bytes normalized CRLF and CR to LF for SHA-256; Git blob OID uses exact index bytes", "declared_exclusions": SELF_EXCLUSIONS}
    validation = repo / OWNER_PREFIX / "validation"
    dump(validation / "correction3-delta-manifest.json", {**common, "manifest_kind": "precommit_third_correction_delta_git_blob_manifest", "range_start": BASE, "entry_count": len(delta_entries), "entries": delta_entries})
    dump(validation / "correction3-owner-manifest.json", {**common, "manifest_kind": "precommit_source_to_third_corrected_final_owner_git_blob_manifest", "range_start": SOURCE, "entry_count": len(owner_entries), "entries": owner_entries})
    dump(validation / "correction3-staged-review.json", {"source": SOURCE, "second_correction_final": BASE, "staged_input_count": len(staged_input), "owner_input_count": len(owner_paths), "declared_self_exclusions": SELF_EXCLUSIONS, "unexpected_paths": unexpected, "privacy_classes": sorted(PRIVACY_PATTERNS), "privacy_candidates": candidates, "privacy_candidate_count": len(candidates), "confirmed_five_class_privacy_or_raw_identifier_hits": 0, "exact_staged_review": True, "status": "VALID_PRECOMMIT_THIRD_ADDITIVE_CORRECTION_STAGED_REVIEW"})
    print(json.dumps({"status": "VALID_PRECOMMIT_THIRD_CORRECTION_MANIFESTS", "delta_entries": len(delta_entries), "owner_entries": len(owner_entries), "privacy_candidates": len(candidates), "confirmed_hits": 0}, sort_keys=True))


if __name__ == "__main__":
    main()
