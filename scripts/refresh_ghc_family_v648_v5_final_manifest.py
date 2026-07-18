#!/usr/bin/env python3
"""Refresh the v648-v5 final manifest from exact current Git-blob inputs."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from build_ghc_family_v648_v5_closeout import EVIDENCE_COMMIT, PHASE, ROOT, SELF_EXCLUSIONS


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


def status_paths() -> list[str]:
    paths = set(filter(None, git("diff", "--name-only").splitlines()))
    paths.update(filter(None, git("diff", "--cached", "--name-only").splitlines()))
    paths.update(filter(None, git("ls-files", "--others", "--exclude-standard").splitlines()))
    return sorted(path.replace("\\", "/") for path in paths)


def main() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE_COMMIT:
        raise RuntimeError("final manifest refresh is restricted to the evidence-head closeout surface")
    entries = []
    for relative in status_paths():
        if relative in SELF_EXCLUSIONS:
            continue
        path = ROOT / relative
        if not path.is_file():
            continue
        entries.append(
            {
                "path": relative,
                "git_blob": git("hash-object", f"--path={relative}", relative),
                "bytes": path.stat().st_size,
            }
        )
    payload = {
        "schema": "ghc.family.v648-v5.final-staged-manifest.v1",
        "hash_domain": "git_hash_object_path_filtered_blob",
        "evidence_commit": EVIDENCE_COMMIT,
        "entry_count": len(entries),
        "entries": entries,
        "self_exclusions": SELF_EXCLUSIONS,
        "boundary": "Static closeout entries are exact Git blobs; result receipts are declared self-exclusions finalized without rerunning the canonical pass.",
    }
    (PHASE / "validation/final-staged-manifest.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({"entries": len(entries), "self_exclusions": len(SELF_EXCLUSIONS)}))


if __name__ == "__main__":
    main()
