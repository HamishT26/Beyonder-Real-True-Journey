#!/usr/bin/env python3
"""Build an exact staged-blob review for Auren Lark v672-v2 x1."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

PHASE_PREFIX = "docs/auren-lark/v672-v2/"
ALLOWED_EXACT = {
    "scripts/build_ghc_family_auren_lark_v672_v2_x1.py",
    "scripts/build_ghc_family_auren_lark_v672_v2_staged_review.py",
    "tests/test_ghc_family_auren_lark_v672_v2_x1.py",
}


def git(root: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(root), *args])


def main() -> None:
    root = Path(
        git(Path.cwd(), "rev-parse", "--show-toplevel").decode("utf-8").strip()
    )
    staged = [
        row
        for row in git(root, "diff", "--cached", "--name-only", "--diff-filter=ACMR")
        .decode("utf-8")
        .splitlines()
        if row
    ]
    deletions = git(root, "diff", "--cached", "--name-only", "--diff-filter=D").decode(
        "utf-8"
    ).splitlines()
    out_of_scope = [
        path
        for path in staged
        if not (path.startswith(PHASE_PREFIX) or path in ALLOWED_EXACT)
    ]
    x2_paths = [path for path in staged if "/x2/" in path or path.endswith("_x2.py")]
    patterns = {
        "aws_access_key": re.compile(rb"A" + rb"KIA[0-9A-Z]{16}"),
        "github_token": re.compile(rb"gh" + rb"p_[A-Za-z0-9]{20,}"),
        "private_key": re.compile(rb"BEGIN [A-Z ]*PRIVATE" + rb" KEY"),
        "raw_task_identifier": re.compile(rb"\b019[a-f0-9]{5}-[a-f0-9-]{20,}\b"),
        "credential_assignment": re.compile(rb"(?i)(password|secret|token)\s*[:=]\s*['\"][^'\"]{8,}"),
    }
    rows = []
    privacy_candidates = []
    strict_json_parses = 0
    working_index_mismatches = []
    for path in staged:
        blob = git(root, "show", f":{path}")
        disk = (root / path).read_bytes()
        if disk != blob:
            working_index_mismatches.append(path)
        if path.endswith(".json"):
            json.loads(blob.decode("utf-8"))
            strict_json_parses += 1
        for name, pattern in patterns.items():
            if pattern.search(blob):
                privacy_candidates.append({"path": path, "privacy_class": name})
        rows.append(
            {
                "path": path,
                "bytes": len(blob),
                "sha256": hashlib.sha256(blob).hexdigest(),
            }
        )

    receipt_path = root / PHASE_PREFIX / "validation" / "x1-staged-review.json"
    valid = not (
        deletions
        or out_of_scope
        or x2_paths
        or privacy_candidates
        or working_index_mismatches
    )
    payload = {
        "schema": "ghc.family.x1-staged-review.v2",
        "owner": "Auren Lark",
        "phase": "v672-v2",
        "lifecycle": "X1_PLANNING_ONLY",
        "staged_before_self": staged,
        "staged_count_before_self": len(staged),
        "staged_count_with_self": len(staged) + 1,
        "blob_rows": rows,
        "strict_json_parses": strict_json_parses,
        "deletions": deletions,
        "out_of_scope": out_of_scope,
        "x2_paths": x2_paths,
        "confirmed_privacy_candidates": privacy_candidates,
        "working_index_mismatches": working_index_mismatches,
        "valid": valid,
    }
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({"receipt": receipt_path.relative_to(root).as_posix(), "valid": valid}))
    if not valid:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
