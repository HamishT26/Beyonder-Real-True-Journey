#!/usr/bin/env python3
"""Create the immutable precommit x1 manifest and staged-review records."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


OWNER_PREFIXES = (
    "docs/caelen-ash/v676-v2/",
    "scripts/build_ghc_family_caelen_ash_v676_v2_x1.py",
    "scripts/ghc_family_caelen_ash_v676_v2_x1_manifest.py",
    "tests/test_ghc_family_caelen_ash_v676_v2_x1.py",
)
MANIFEST = "docs/caelen-ash/v676-v2/validation/x1-manifest.json"
STAGED_REVIEW = "docs/caelen-ash/v676-v2/validation/x1-staged-review.json"
SOURCE = "939312172819669aad250cf034d8a6a7efe3df5b"
BRANCH = "codex/GHC-Family/caelen-ash-v676-v2-full-tools"


def git(repo: Path, *args: str, text: bool = True):
    return subprocess.check_output(["git", "-C", str(repo), *args], text=text)


def normalize_lf(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    repo = Path(__file__).resolve().parents[1]
    branch = git(repo, "branch", "--show-current").strip()
    head = git(repo, "rev-parse", "HEAD").strip()
    if branch != BRANCH or head != SOURCE:
        raise SystemExit("x1 manifest builder requires the exact owner branch at the Sable source head")
    staged = [line for line in git(repo, "diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if line]
    unexpected = [path for path in staged if not path.startswith(OWNER_PREFIXES)]
    if unexpected:
        raise SystemExit(f"unexpected staged paths: {unexpected}")
    if any("/x2/" in f"/{path}/" or "v676_v2_x2" in path for path in staged):
        raise SystemExit("x2 path found in planning-only x1 stage")
    exclusions = {
        MANIFEST: "self-referential manifest output",
        STAGED_REVIEW: "self-referential staged-review output",
    }
    entries = []
    for path in sorted(path for path in staged if path not in exclusions):
        raw = git(repo, "show", f":{path}", text=False)
        normalized = normalize_lf(raw)
        oid = subprocess.check_output(["git", "-C", str(repo), "hash-object", "--stdin"], input=raw).decode().strip()
        entries.append(
            {
                "path": path,
                "bytes": len(raw),
                "normalized_lf_bytes": len(normalized),
                "sha256_normalized_lf": hashlib.sha256(normalized).hexdigest(),
                "git_blob_oid": oid,
            }
        )
    write_json(
        repo / MANIFEST,
        {
            "manifest_kind": "immutable_x1_precommit_git_blob_manifest",
            "owner": "Caelen Ash",
            "phase": "v676-v2",
            "source": SOURCE,
            "entry_count": len(entries),
            "entries": entries,
            "declared_exclusions": [{"path": path, "reason": reason} for path, reason in sorted(exclusions.items())],
            "normalization_domain": "Git index bytes normalized CRLF and CR to LF for SHA-256; Git blob OID uses exact staged bytes",
            "x2_paths_present": False,
        },
    )
    write_json(
        repo / STAGED_REVIEW,
        {
            "review_kind": "planning_only_x1_exact_stage",
            "source": SOURCE,
            "expected_branch": BRANCH,
            "staged_before_self_outputs": len(staged),
            "manifest_entries": len(entries),
            "declared_self_exclusions": len(exclusions),
            "reviewed_paths": sorted(staged),
            "unexpected_paths": [],
            "x2_paths": [],
            "planning_only": True,
            "outcome_claims_executed": 0,
            "review_status": "PASS_PRECOMMIT_X1",
        },
    )
    print(json.dumps({"manifest_entries": len(entries), "declared_exclusions": len(exclusions), "staged_paths": len(staged)}, sort_keys=True))


if __name__ == "__main__":
    main()
