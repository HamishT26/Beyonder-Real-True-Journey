#!/usr/bin/env python3
"""Review and manifest the exact staged Neris Solane v652-v8 evidence delta."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from ghc_family_v652_v8_validation_common import PHASE, PHASE_PREFIX, REPO, git, scan_privacy_bytes, sha256_bytes, write_json


REVIEW_PATH = "docs/neris-solane/v652-v8/validation/evidence-staged-review.json"
MANIFEST_PATH = "docs/neris-solane/v652-v8/validation/evidence-candidate-manifest.json"
VALIDATION_PATH = "docs/neris-solane/v652-v8/validation/evidence-validation.json"
SELF_EXCLUSIONS = {REVIEW_PATH, MANIFEST_PATH, VALIDATION_PATH}


def staged_paths() -> list[str]:
    return sorted(
        path
        for path in git("diff", "--cached", "--name-only", "--diff-filter=ACMRT").splitlines()
        if path
    )


def index_bytes(path: str) -> bytes:
    return subprocess.run(
        ["git", "show", f":{path}"],
        cwd=REPO,
        check=True,
        capture_output=True,
    ).stdout


def allowed(path: str, runner_names: set[str]) -> bool:
    return (
        path.startswith(PHASE_PREFIX)
        or path.startswith("scripts/ghc_family_v652_v8_")
        or path.startswith("scripts/build_ghc_family_v652_v8_")
        or path.startswith("tests/test_ghc_family_v652_v8_")
        or path in {f"scripts/{name}" for name in runner_names}
    )


def build() -> dict:
    paths = staged_paths()
    runner_names = {
        row["runner"]
        for row in json.loads((PHASE / "runners/runner-invocation-receipt.json").read_text(encoding="utf-8"))["runners"]
    }
    out_of_scope = [path for path in paths if not allowed(path, runner_names)]
    frozen_phase_changes = [
        path
        for path in paths
        if path.startswith(PHASE_PREFIX)
        and path in set(git("ls-tree", "-r", "--name-only", "6e5c0e6fbe1bc569bd2eb8971629f2125f1c1984", "--", PHASE_PREFIX.rstrip("/")).splitlines())
    ]
    permitted_historical_test_update = "tests/test_ghc_family_v652_v8_x1.py"
    historical_changes = [
        path
        for path in paths
        if path == permitted_historical_test_update
    ]
    content_rows = [(path, index_bytes(path)) for path in paths if path not in SELF_EXCLUSIONS]
    privacy = scan_privacy_bytes((path, content) for path, content in content_rows)
    entries = [
        {
            "path": path,
            "git_blob": git("rev-parse", f":{path}"),
            "sha256": sha256_bytes(content),
            "bytes": len(content),
        }
        for path, content in content_rows
    ]
    names_hash = sha256_bytes(("\n".join(paths) + "\n").encode("utf-8"))
    manifest = {
        "schema": "ghc.family.v652-v8.evidence-candidate-manifest.v1",
        "hash_domain": "exact staged Git index content",
        "staged_path_count": len(paths),
        "entry_count": len(entries),
        "entries": entries,
        "self_exclusions": sorted(SELF_EXCLUSIONS),
        "exact_staged_names_sha256": names_hash,
        "boundary": "The three lifecycle receipts are explicit self-exclusions; every other staged path is byte-bound.",
    }
    valid = (
        bool(paths)
        and not out_of_scope
        and not frozen_phase_changes
        and historical_changes in ([], [permitted_historical_test_update])
        and privacy["valid"]
        and len(entries) == len(paths) - len(set(paths) & SELF_EXCLUSIONS)
    )
    review = {
        "schema": "ghc.family.v652-v8.evidence-staged-review.v1",
        "staged_path_count": len(paths),
        "manifest_entry_count": len(entries),
        "exact_staged_names_sha256": names_hash,
        "out_of_scope_paths": out_of_scope,
        "frozen_x1_phase_path_changes": frozen_phase_changes,
        "permitted_historical_test_update": historical_changes,
        "privacy": privacy,
        "diff_hygiene_required_separately": True,
        "valid": valid,
        "boundary": "Exact Git-index review for the evidence delta; no post-commit or route claim.",
    }
    write_json(PHASE / "validation/evidence-candidate-manifest.json", manifest)
    write_json(PHASE / "validation/evidence-staged-review.json", review)
    return review


def main() -> None:
    result = build()
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    if not result["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
