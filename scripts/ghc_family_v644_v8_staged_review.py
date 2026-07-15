#!/usr/bin/env python3
"""Review every substantive staged Orin Thale v644-v8 blob before commit."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


PHASE = "v644-gmut-thos-v8-x1-x2"
PHASE_ROOT = "docs/orin-thale/v644-v8/"
SELF_PATH = PHASE_ROOT + "validation/evidence-staged-review.json"
X1_FILE_SET = PHASE_ROOT + "validation/x1-exact-file-set.json"
X1_COMMIT = "669b1b3a331879711a625961c574bed94630a15e"
APPEND_ONLY_X1 = {
    PHASE_ROOT + "method-flow/method-flow-state.json",
    PHASE_ROOT + "method-flow/runner-validation.json",
}
ALLOWED_EXACT = {
    "scripts/ghc_family_gitlink_visibility.py",
    "scripts/ghc_family_v644_v8_evidence.py",
    "scripts/ghc_family_v644_v8_model.py",
    "scripts/ghc_family_v644_v8_staged_review.py",
    "scripts/ghc_family_v644_v8_validator.py",
    "tests/test_ghc_family_v644_v8.py",
}


def git_bytes(repo: Path, *args: str, check: bool = True) -> bytes:
    return subprocess.run(
        ["git", *args], cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check
    ).stdout


def allowed(name: str) -> bool:
    return name.startswith(PHASE_ROOT) or name in ALLOWED_EXACT


def load_blob_json(repo: Path, spec: str) -> dict[str, Any]:
    return json.loads(git_bytes(repo, "show", spec).decode("utf-8"))


def method_append_only(repo: Path) -> dict[str, Any]:
    relative = PHASE_ROOT + "method-flow/method-flow-state.json"
    before = load_blob_json(repo, f"{X1_COMMIT}:{relative}")
    after = load_blob_json(repo, f":{relative}")
    before_methods = {row["method_id"]: row for row in before["methods"]}
    after_methods = {row["method_id"]: row for row in after["methods"]}
    changed_existing: list[str] = []
    for method_id, old in before_methods.items():
        new = after_methods.get(method_id)
        if new is None:
            changed_existing.append(method_id + ":missing")
            continue
        old_copy = dict(old)
        new_copy = dict(new)
        old_witnesses = old_copy.pop("validation_witness_ids")
        new_witnesses = new_copy.pop("validation_witness_ids")
        if old_copy != new_copy or new_witnesses[: len(old_witnesses)] != old_witnesses:
            changed_existing.append(method_id)
    before_witnesses = [row["witness_id"] for row in before["witnesses"]]
    after_witnesses = [row["witness_id"] for row in after["witnesses"]]
    before_events = before["state_events"]
    after_events = after["state_events"]
    return {
        "old_method_count": len(before_methods),
        "new_method_count": len(after_methods),
        "old_methods_missing_or_rewritten": changed_existing,
        "old_witness_prefix_retained": after_witnesses[: len(before_witnesses)] == before_witnesses,
        "old_state_event_prefix_retained": after_events[: len(before_events)] == before_events,
        "valid": (
            not changed_existing
            and after_witnesses[: len(before_witnesses)] == before_witnesses
            and after_events[: len(before_events)] == before_events
            and len(after_methods) >= len(before_methods)
        ),
    }


def run(repo: Path, self_path: str = SELF_PATH) -> dict[str, Any]:
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
    x1_files = set(x1_payload["expected_files"])
    frozen_x1 = x1_files - APPEND_ONLY_X1
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
                "x1_frozen_path": name in frozen_x1,
                "x1_append_only_path": name in APPEND_ONLY_X1,
            }
        )
    diff_check = subprocess.run(
        ["git", "diff", "--cached", "--check"], cwd=repo, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace", check=False,
    )
    frozen_diff = [
        item.decode("utf-8")
        for item in git_bytes(repo, "diff", "--name-only", "-z", X1_COMMIT, "--", *sorted(frozen_x1)).split(b"\0")
        if item
    ]
    deleted = [row for row in rows if "D" in (row["index_status"] or "")]
    method_check = method_append_only(repo)
    issues = []
    if not rows:
        issues.append("no substantive staged files")
    if any(not row["allowed_scope"] for row in rows):
        issues.append("out-of-scope staged path")
    if any(row["x1_frozen_path"] for row in rows):
        issues.append("frozen x1 path staged")
    if frozen_diff:
        issues.append("frozen x1 content differs from x1 commit")
    if deleted:
        issues.append("staged deletion")
    if diff_check.returncode != 0:
        issues.append("git diff --cached --check failed")
    if not method_check["valid"]:
        issues.append("Method Flow append-only check failed")
    return {
        "schema": "ghc.family.v644-v8.evidence-staged-review.v1",
        "phase": PHASE,
        "base_commit": X1_COMMIT,
        "self_receipt_path": self_path,
        "self_receipt_excluded_from_blob_review": True,
        "reviewed_file_count": len(rows),
        "expected_final_staged_file_count": len(rows) + 1,
        "deleted_file_count": len(deleted),
        "frozen_x1_file_count_staged": sum(row["x1_frozen_path"] for row in rows),
        "append_only_x1_file_count_staged": sum(row["x1_append_only_path"] for row in rows),
        "frozen_x1_diff_paths": frozen_diff,
        "method_flow_append_only": method_check,
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
    parser.add_argument("--output", type=Path, default=Path(SELF_PATH))
    args = parser.parse_args()
    repo = args.repo.resolve()
    output = args.output if args.output.is_absolute() else repo / args.output
    try:
        self_path = output.resolve().relative_to(repo).as_posix()
    except ValueError:
        self_path = SELF_PATH
    result = run(repo, self_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    keys = (
        "valid", "reviewed_file_count", "expected_final_staged_file_count",
        "deleted_file_count", "frozen_x1_file_count_staged", "append_only_x1_file_count_staged", "issues",
    )
    print(json.dumps({key: result[key] for key in keys}, ensure_ascii=False))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
