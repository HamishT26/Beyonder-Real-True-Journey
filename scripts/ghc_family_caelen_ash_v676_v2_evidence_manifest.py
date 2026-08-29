#!/usr/bin/env python3
"""Create the immutable precommit x2 evidence manifest and staged review."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


X1 = "39daa2da64125b839714efa8b7488d8ed9ed364b"
BRANCH = "codex/GHC-Family/caelen-ash-v676-v2-full-tools"
MANIFEST = "docs/caelen-ash/v676-v2/validation/evidence-manifest.json"
STAGED_REVIEW = "docs/caelen-ash/v676-v2/validation/evidence-staged-review.json"
PREFIXES = (
    "docs/caelen-ash/v676-v2/",
    "scripts/build_ghc_family_caelen_ash_v676_v2_",
    "scripts/ghc_family_caelen_ash_v676_v2_",
    "tests/test_ghc_family_caelen_ash_v676_v2_",
)


def git(repo: Path, *args: str, text: bool = True):
    return subprocess.check_output(["git", "-C", str(repo), *args], text=text)


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    repo = Path(__file__).resolve().parents[1]
    if git(repo, "branch", "--show-current").strip() != BRANCH or git(repo, "rev-parse", "HEAD").strip() != X1:
        raise SystemExit("evidence manifest requires the exact immutable x1 head")
    staged = [line for line in git(repo, "diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if line]
    unexpected = [path for path in staged if not path.startswith(PREFIXES)]
    if unexpected:
        raise SystemExit(f"unexpected staged paths: {unexpected}")
    if any("/final/" in f"/{path}/" or "/closeout/" in f"/{path}/" for path in staged):
        raise SystemExit("final or closeout path found in evidence stage")
    exclusions = {
        MANIFEST: "self-referential evidence manifest",
        STAGED_REVIEW: "self-referential evidence staged review",
    }
    entries = []
    for path in sorted(path for path in staged if path not in exclusions):
        raw = git(repo, "show", f":{path}", text=False)
        norm = normalized(raw)
        oid = subprocess.check_output(["git", "-C", str(repo), "hash-object", "--stdin"], input=raw).decode().strip()
        entries.append(
            {
                "path": path,
                "bytes": len(raw),
                "normalized_lf_bytes": len(norm),
                "sha256_normalized_lf": hashlib.sha256(norm).hexdigest(),
                "git_blob_oid": oid,
            }
        )
    write_json(
        repo / MANIFEST,
        {
            "manifest_kind": "immutable_x2_evidence_precommit_git_blob_manifest",
            "owner": "Caelen Ash",
            "phase": "v676-v2",
            "x1_anchor": X1,
            "entry_count": len(entries),
            "entries": entries,
            "declared_exclusions": [{"path": path, "reason": reason} for path, reason in sorted(exclusions.items())],
            "normalization_domain": "Git index bytes normalized CRLF and CR to LF for SHA-256; Git blob OID uses exact staged bytes",
            "final_or_closeout_paths_present": False,
        },
    )
    write_json(
        repo / STAGED_REVIEW,
        {
            "review_kind": "x2_evidence_exact_stage",
            "x1_anchor": X1,
            "expected_branch": BRANCH,
            "staged_before_self_outputs": len(staged),
            "manifest_entries": len(entries),
            "declared_self_exclusions": len(exclusions),
            "reviewed_paths": sorted(staged),
            "unexpected_paths": [],
            "final_or_closeout_paths": [],
            "review_status": "PASS_PRECOMMIT_EVIDENCE",
        },
    )
    print(json.dumps({"manifest_entries": len(entries), "declared_exclusions": len(exclusions), "staged_paths": len(staged)}, sort_keys=True))


if __name__ == "__main__":
    main()
