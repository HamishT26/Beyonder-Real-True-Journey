#!/usr/bin/env python3
"""Review every substantive staged Sylven Arc v645-v2 blob before commit."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

from ghc_family_index_stage_guard import classify_stage_bytes


PHASE = "v645-gmut-thos-v2-x1-x2"
PHASE_ROOT = "docs/sylven-arc/v645-v2/"
SELF_PATH = PHASE_ROOT + "validation/evidence-staged-review.json"
X1_FILE_SET = PHASE_ROOT + "validation/x1-exact-file-set.json"
X1_COMMIT = "d874818d61adcbe31f65c72ce8c019b3e1f81e22"
APPEND_ONLY_X1 = {
    PHASE_ROOT + "method-flow/method-flow-state.json",
    PHASE_ROOT + "method-flow/method-flow-summary.json",
    PHASE_ROOT + "method-flow/method-flow-summary.md",
    PHASE_ROOT + "method-flow/runner-validation.json",
}
ALLOWED_EXACT = {
    "scripts/ghc_family_index_stage_guard.py",
    "scripts/ghc_family_v645_v2_evidence.py",
    "scripts/ghc_family_v645_v2_final_manifest.py",
    "scripts/ghc_family_v645_v2_model.py",
    "scripts/ghc_family_v645_v2_staged_review.py",
    "scripts/ghc_family_v645_v2_validator.py",
    "tests/test_ghc_family_v645_v2.py",
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
    privacy_patterns = {
        "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "delegation_markup": re.compile(r"<(?:codex_delegation|source_thread_id)>", re.I),
        "private_local_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
        "private_uri": re.compile(r"\b(?:app|plugin)://", re.I),
        "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']"),
    }
    privacy_hits: list[dict[str, str]] = []
    json_blob_count = 0
    json_parse_issues: list[str] = []
    rows = []
    for name in reviewed_names:
        payload = git_bytes(repo, "show", f":{name}")
        text = payload.decode("utf-8", errors="replace")
        for label, pattern in privacy_patterns.items():
            if pattern.search(text):
                privacy_hits.append({"path": name, "pattern_class": label})
        if name.endswith(".json"):
            json_blob_count += 1
            try:
                json.loads(text)
            except Exception as error:  # pragma: no cover - diagnostic receipt
                json_parse_issues.append(f"{name}: {type(error).__name__}")
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
    index_stage_guard = classify_stage_bytes(git_bytes(repo, "ls-files", "--stage", "-z"))
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
    if privacy_hits:
        issues.append("staged privacy or raw-identifier scan failed")
    if json_parse_issues:
        issues.append("staged JSON parsing failed")
    if not index_stage_guard["accepted"]:
        issues.append("candidate index contains malformed or unresolved higher-stage entries")
    stage = next((name for name in ("closeout", "seal", "final") if f"/{name}-" in self_path), "evidence")
    return {
        "schema": f"ghc.family.v645-v2.{stage}-staged-review.v1",
        "stage": stage,
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
        "json_blobs_parsed": json_blob_count,
        "json_parse_issues": json_parse_issues,
        "privacy_scan": {
            "files_scanned": len(rows),
            "pattern_classes": sorted(privacy_patterns),
            "hits": privacy_hits,
            "hit_count": len(privacy_hits),
            "valid": not privacy_hits,
        },
        "index_stage_guard": {
            "accepted": index_stage_guard["accepted"],
            "classification": index_stage_guard["classification"],
            "record_count": index_stage_guard["record_count"],
            "higher_stage_count": index_stage_guard["higher_stage_count"],
            "multiplicity_path_count": index_stage_guard["multiplicity_path_count"],
            "index_mutation_count": index_stage_guard["index_mutation_count"],
        },
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
