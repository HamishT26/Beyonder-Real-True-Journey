#!/usr/bin/env python3
"""Build exact precommit final-delta and owner-domain Git-blob manifests."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


EVIDENCE = "bc7f321d66c094422ddc69275d811eb8ec917f3b"
BRANCH = "codex/GHC-Family/caelen-ash-v676-v2-full-tools"
DELTA = "docs/caelen-ash/v676-v2/validation/final-delta-manifest.json"
OWNER = "docs/caelen-ash/v676-v2/validation/final-owner-manifest.json"
REVIEW = "docs/caelen-ash/v676-v2/validation/final-staged-review.json"
PREFIXES = (
    "docs/caelen-ash/v676-v2/",
    "scripts/build_ghc_family_caelen_ash_v676_v2_",
    "scripts/ghc_family_caelen_ash_v676_v2_",
    "tests/test_ghc_family_caelen_ash_v676_v2_",
)


def git(repo: Path, *args: str, text: bool = True):
    return subprocess.check_output(["git", "-C", str(repo), *args], text=text)


def write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    repo = Path(__file__).resolve().parents[1]
    if git(repo, "branch", "--show-current").strip() != BRANCH or git(repo, "rev-parse", "HEAD").strip() != EVIDENCE:
        raise SystemExit("final manifest builder requires the immutable evidence head")
    staged = [line for line in git(repo, "diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if line]
    unexpected = [path for path in staged if not path.startswith(PREFIXES)]
    if unexpected:
        raise SystemExit(f"unexpected staged paths: {unexpected}")
    lifecycle_contamination = [path for path in staged if "/x1/" in f"/{path}/" or "/x2/" in f"/{path}/"]
    if lifecycle_contamination:
        raise SystemExit(f"immutable lifecycle path modified in final stage: {lifecycle_contamination}")
    exclusions = {
        DELTA: "self-referential final-delta manifest",
        OWNER: "self-referential final-owner manifest",
        REVIEW: "self-referential final staged review",
    }
    index = {}
    for line in git(repo, "ls-files", "-s").splitlines():
        left, path = line.split("\t", 1)
        index[path] = left.split()[1]
    owner_paths = sorted(path for path in index if path.startswith(PREFIXES))
    delta_paths = sorted(path for path in staged if path not in exclusions)
    owner_included = sorted(path for path in owner_paths if path not in exclusions)
    proc = subprocess.Popen(["git", "-C", str(repo), "cat-file", "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert proc.stdin and proc.stdout
    cache: dict[str, bytes] = {}

    def raw_for(path: str) -> bytes:
        oid = index[path]
        if oid not in cache:
            proc.stdin.write((oid + "\n").encode("ascii"))
            proc.stdin.flush()
            header = proc.stdout.readline().split()
            if len(header) < 3 or header[1] != b"blob":
                raise RuntimeError(f"not a blob: {path}")
            raw = proc.stdout.read(int(header[2]))
            proc.stdout.read(1)
            cache[oid] = raw
        return cache[oid]

    def entry(path: str) -> dict[str, object]:
        raw = raw_for(path)
        norm = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        return {
            "path": path,
            "bytes": len(raw),
            "normalized_lf_bytes": len(norm),
            "sha256_normalized_lf": hashlib.sha256(norm).hexdigest(),
            "git_blob_oid": index[path],
        }

    delta_entries = [entry(path) for path in delta_paths]
    owner_entries = [entry(path) for path in owner_included]
    proc.stdin.close()
    stderr = proc.stderr.read().decode("utf-8", "replace") if proc.stderr else ""
    code = proc.wait()
    if code != 0:
        raise RuntimeError(stderr)
    declared = [{"path": path, "reason": reason} for path, reason in sorted(exclusions.items())]
    write(
        repo / DELTA,
        {
            "manifest_kind": "final_delta_precommit_git_blob_manifest",
            "evidence": EVIDENCE,
            "entry_count": len(delta_entries),
            "entries": delta_entries,
            "declared_exclusions": declared,
            "normalization_domain": "Git index bytes normalized CRLF and CR to LF for SHA-256; exact Git blob OIDs retained",
        },
    )
    write(
        repo / OWNER,
        {
            "manifest_kind": "source_to_final_owner_domain_precommit_git_blob_manifest",
            "evidence": EVIDENCE,
            "entry_count": len(owner_entries),
            "entries": owner_entries,
            "declared_exclusions": declared,
            "owner_rotation_ceiling": 2000,
            "below_rotation_ceiling": len(owner_paths) < 2000,
            "normalization_domain": "Git index bytes normalized CRLF and CR to LF for SHA-256; exact Git blob OIDs retained",
        },
    )
    write(
        repo / REVIEW,
        {
            "review_kind": "exact_final_precommit_stage",
            "evidence": EVIDENCE,
            "expected_branch": BRANCH,
            "staged_before_self_outputs": len(staged),
            "delta_manifest_entries": len(delta_entries),
            "owner_manifest_entries": len(owner_entries),
            "declared_self_exclusions": len(exclusions),
            "reviewed_paths": sorted(staged),
            "unexpected_paths": [],
            "immutable_x1_or_x2_modifications": [],
            "review_status": "PASS_PRECOMMIT_FINAL",
        },
    )
    print(json.dumps({"delta_entries": len(delta_entries), "owner_entries": len(owner_entries), "declared_exclusions": len(exclusions)}, sort_keys=True))


if __name__ == "__main__":
    main()
