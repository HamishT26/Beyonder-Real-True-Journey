#!/usr/bin/env python3
"""Review every substantive staged Sylven Arc v644-v4 blob before commit."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


SELF_PATH = "docs/sylven-arc/v644-v4/validation/evidence-staged-review.json"
X1_FILE_SET = "docs/sylven-arc/v644-v4/validation/x1-exact-file-set.json"
ALLOWED_EXACT = {
    "scripts/build_ghc_family_v644_v4_report.py",
    "scripts/ghc_family_v644_v4_complete_suite.py",
    "scripts/ghc_family_v644_v4_evidence.py",
    "scripts/ghc_family_v644_v4_minimal.py",
    "scripts/ghc_family_v644_v4_model.py",
    "scripts/ghc_family_v644_v4_staged_review.py",
    "scripts/ghc_family_v644_v4_validator.py",
    "tests/test_ghc_family_v644_v4.py",
}


def git_bytes(repo: Path, *args: str, check: bool = True) -> bytes:
    return subprocess.run(
        ["git", *args], cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check
    ).stdout


def allowed(name: str) -> bool:
    return name.startswith("docs/sylven-arc/v644-v4/") or name in ALLOWED_EXACT


def run(repo: Path, base: str, self_path: str = SELF_PATH) -> dict[str, Any]:
    repo = repo.resolve()
    names = [
        item.decode("utf-8")
        for item in git_bytes(repo, "diff", "--cached", "--name-only", "-z").split(b"\0")
        if item
    ]
    reviewed_names = [name for name in names if name != self_path]
    status_rows: dict[str, str] = {}
    for line in git_bytes(repo, "diff", "--cached", "--name-status").decode("utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) >= 2:
            status_rows[parts[-1]] = parts[0]
    x1_payload = json.loads((repo / X1_FILE_SET).read_text(encoding="utf-8"))
    x1_files = set(x1_payload["files"])
    rows = []
    for name in reviewed_names:
        payload = git_bytes(repo, "show", f":{name}")
        rows.append(
            {
                "repo_path": name,
                "index_status": status_rows.get(name),
                "staged_blob_sha256": hashlib.sha256(payload).hexdigest(),
                "staged_bytes": len(payload),
                "allowed_scope": allowed(name),
                "x1_frozen_path": name in x1_files,
            }
        )
    diff_check = subprocess.run(
        ["git", "diff", "--cached", "--check"], cwd=repo, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace", check=False,
    )
    x1_diff = [
        item.decode("utf-8")
        for item in git_bytes(repo, "diff", "--name-only", "-z", base, "--", *sorted(x1_files)).split(b"\0")
        if item
    ]
    deleted = [row for row in rows if "D" in (row["index_status"] or "")]
    issues = []
    if not rows:
        issues.append("no substantive staged files")
    if any(not row["allowed_scope"] for row in rows):
        issues.append("out-of-scope staged path")
    if any(row["x1_frozen_path"] for row in rows):
        issues.append("x1 frozen path staged")
    if x1_diff:
        issues.append("x1 content differs from frozen commit")
    if deleted:
        issues.append("staged deletion")
    if diff_check.returncode != 0:
        issues.append("git diff --cached --check failed")
    return {
        "schema": "ghc.family.v644-v4.evidence-staged-review.v1",
        "phase": "v644-gmut-thos-v4-x1-x2",
        "base_commit": base,
        "self_receipt_path": self_path,
        "self_receipt_excluded_from_blob_review": True,
        "reviewed_file_count": len(rows),
        "expected_final_staged_file_count": len(rows) + 1,
        "deleted_file_count": len(deleted),
        "x1_frozen_file_count_staged": sum(row["x1_frozen_path"] for row in rows),
        "x1_diff_paths": x1_diff,
        "diff_check_returncode": diff_check.returncode,
        "diff_check_output": diff_check.stdout,
        "all_paths_in_owner_scope": all(row["allowed_scope"] for row in rows),
        "files": rows,
        "issues": issues,
        "valid": not issues,
        "boundary": "Exact staged-blob review does not replace semantic, privacy, scientific, legal, cultural, accessibility, security, or external-authority review.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--base", default="a33c6d53a37f3f86fe143bba81dcacf52b4e20c0")
    parser.add_argument("--output", type=Path, default=Path(SELF_PATH))
    args = parser.parse_args()
    repo = args.repo.resolve()
    output = args.output if args.output.is_absolute() else repo / args.output
    try:
        self_path = output.resolve().relative_to(repo).as_posix()
    except ValueError:
        self_path = SELF_PATH
    result = run(repo, args.base, self_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    keys = ("valid", "reviewed_file_count", "expected_final_staged_file_count", "deleted_file_count", "x1_frozen_file_count_staged", "issues")
    print(json.dumps({key: result[key] for key in keys}, ensure_ascii=False))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
