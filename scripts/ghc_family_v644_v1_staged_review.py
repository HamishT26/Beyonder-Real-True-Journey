#!/usr/bin/env python3
"""Review every substantive staged v644-v1 blob before commit.

The output receipt excludes only its own path to avoid a self-hash cycle. The
receipt records the expected final staged count after that one receipt is
added, so callers can verify the final index shape exactly.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


SELF_PATH = "docs/sable-rook/v644-v1/validation/evidence-staged-review.json"
ALLOWED_PREFIXES = (
    "docs/sable-rook/v644-v1/",
    "scripts/build_ghc_family_v644_v1_report.py",
    "scripts/ghc_family_v644_v1_",
    "tests/test_ghc_family_v644_v1.py",
)


def git_bytes(repo: Path, *args: str, check: bool = True) -> bytes:
    return subprocess.run(
        ["git", *args], cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check
    ).stdout


def run(repo: Path) -> dict[str, Any]:
    repo = repo.resolve()
    names = [
        item.decode("utf-8")
        for item in git_bytes(repo, "diff", "--cached", "--name-only", "-z").split(b"\0")
        if item
    ]
    reviewed_names = [name for name in names if name != SELF_PATH]
    status_rows = {}
    for line in git_bytes(repo, "diff", "--cached", "--name-status").decode("utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) >= 2:
            status_rows[parts[-1]] = parts[0]
    x1 = json.loads((repo / "docs/sable-rook/v644-v1/validation/x1-exact-file-set.json").read_text(encoding="utf-8"))
    x1_set = set(x1["files"])
    rows = []
    for name in reviewed_names:
        payload = git_bytes(repo, "show", f":{name}")
        rows.append({
            "repo_path": name,
            "index_status": status_rows.get(name),
            "staged_blob_sha256": hashlib.sha256(payload).hexdigest(),
            "staged_bytes": len(payload),
            "allowed_scope": any(name == prefix or name.startswith(prefix) for prefix in ALLOWED_PREFIXES),
            "x1_frozen_path": name in x1_set,
        })
    diff_check = subprocess.run(
        ["git", "diff", "--cached", "--check"], cwd=repo, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace", check=False,
    )
    deleted = [row for row in rows if row["index_status"] and "D" in row["index_status"]]
    issues = []
    if not rows:
        issues.append("no substantive staged files")
    if any(not row["allowed_scope"] for row in rows):
        issues.append("out-of-scope staged path")
    if any(row["x1_frozen_path"] for row in rows):
        issues.append("x1 frozen path staged")
    if deleted:
        issues.append("staged deletion")
    if diff_check.returncode != 0:
        issues.append("git diff --cached --check failed")
    return {
        "schema": "ghc.family.v644-v1.evidence-staged-review.v1",
        "phase": "v644-gmut-thos-v1-x1-x2",
        "self_receipt_path": SELF_PATH,
        "self_receipt_excluded_from_blob_review": True,
        "reviewed_file_count": len(rows),
        "expected_final_staged_file_count": len(rows) + 1,
        "deleted_file_count": len(deleted),
        "x1_frozen_file_count_staged": sum(row["x1_frozen_path"] for row in rows),
        "diff_check_returncode": diff_check.returncode,
        "diff_check_output": diff_check.stdout,
        "all_paths_in_owner_scope": all(row["allowed_scope"] for row in rows),
        "files": rows,
        "issues": issues,
        "valid": not issues,
        "boundary": "Exact staged-blob review does not replace semantic, privacy, scientific, legal, cultural, or external-authority review.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, default=Path(SELF_PATH))
    args = parser.parse_args()
    repo = args.repo.resolve()
    result = run(repo)
    output = args.output if args.output.is_absolute() else repo / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({key: result[key] for key in ("valid", "reviewed_file_count", "expected_final_staged_file_count", "deleted_file_count", "x1_frozen_file_count_staged", "issues")}, ensure_ascii=False))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
