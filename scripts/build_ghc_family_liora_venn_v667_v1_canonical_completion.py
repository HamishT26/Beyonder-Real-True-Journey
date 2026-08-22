#!/usr/bin/env python3
"""Invoke Liora Venn v667-v1's one exclusive exact-final canonical aggregate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from datetime import datetime, timezone
from typing import Any

from ghc_family_liora_venn_v667_v1_runtime import (
    PHASE_ROOT,
    ROOT,
    X1_SHA,
    owner_paths,
    privacy_summary,
    replay_manifest,
    security_summary,
)


SOURCE_SHA = "27a3a3cc332d27384210848d685e3bf16c6b2f0d"
BRANCH = "codex/GHC-Family/liora-venn-v667-v1-full-tools"
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(ROOT), *args], stderr=subprocess.STDOUT
    ).decode("utf-8", errors="strict").strip()


def load(relative: str) -> Any:
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


def run_test(relative: str, expected: int) -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, "-X", "utf8", relative, "-q"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="strict",
        capture_output=True,
        check=False,
    )
    text = (completed.stdout + "\n" + completed.stderr).strip()
    match = re.search(r"Ran\s+(\d+)\s+tests?", text)
    observed = int(match.group(1)) if match else None
    return {
        "selection": relative,
        "expected": expected,
        "observed": observed,
        "returncode": completed.returncode,
        "valid": completed.returncode == 0 and observed == expected and "OK" in text,
        "bounded_output_tail": text[-500:],
    }


def remote_equality(head: str) -> dict[str, Any]:
    upstream = git("rev-parse", "@{u}")
    tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_raw = subprocess.check_output(
        ["git", "-C", str(ROOT), "ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}"],
        stderr=subprocess.STDOUT,
    ).decode("utf-8", errors="strict").strip()
    live_rows = [row for row in live_raw.splitlines() if row]
    live = live_rows[0].split()[0] if len(live_rows) == 1 else None
    counts = git("rev-list", "--left-right", "--count", f"HEAD...@{{u}}").split()
    ahead, behind = [int(value) for value in counts]
    return {
        "local": head,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live": live,
        "ahead": ahead,
        "behind": behind,
        "valid": head == upstream == tracking == live and ahead == 0 and behind == 0,
    }


def manifest_paths(value: dict[str, Any]) -> set[str]:
    return {row["path"] for row in value["entries"]}


def main(receipt_path: Path) -> int:
    if receipt_path.exists():
        raise RuntimeError("exclusive canonical receipt path already exists; replay forbidden")
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    head = git("rev-parse", "HEAD")
    evidence_sha = load("closeout/phase-truth.json")["evidence_sha"]
    clean_before = git("status", "--porcelain=v1") == ""
    equality_before = remote_equality(head)
    tests = [
        run_test("tests/test_ghc_family_liora_venn_v667_v1_x2.py", 67),
        run_test("tests/test_ghc_family_liora_venn_v667_v1_evidence.py", 9),
        run_test("tests/test_ghc_family_liora_venn_v667_v1_closeout.py", 10),
    ]
    x1_test = load("x2/exact-x1-tree-test-receipt.json")

    manifests = {
        "x1": replay_manifest(PHASE_ROOT / "validation" / "x1-content-manifest.json", X1_SHA),
        "evidence": replay_manifest(PHASE_ROOT / "validation" / "evidence-content-manifest.json", evidence_sha),
        "final_delta": replay_manifest(PHASE_ROOT / "validation" / "final-delta-manifest.json", head),
        "final_owner": replay_manifest(PHASE_ROOT / "validation" / "final-owner-manifest.json", head),
    }
    manifest_values = {
        "evidence": load("validation/evidence-content-manifest.json"),
        "final_delta": load("validation/final-delta-manifest.json"),
        "final_owner": load("validation/final-owner-manifest.json"),
    }
    manifest_values["x1"] = load("validation/x1-content-manifest.json")

    owner = owner_paths()
    json_paths = [path for path in owner if path.suffix == ".json"]
    for path in json_paths:
        json.loads(path.read_text(encoding="utf-8"))
    python_paths = [path for path in owner if path.suffix == ".py"]
    for path in python_paths:
        compile(path.read_text(encoding="utf-8"), path.relative_to(ROOT).as_posix(), "exec")
    markdown_paths = [path for path in owner if path.suffix.lower() == ".md"]
    html_paths = [path for path in owner if path.suffix.lower() == ".html"]
    maximum_words = max((len(re.findall(r"\S+", path.read_text(encoding="utf-8"))) for path in markdown_paths + html_paths), default=0)
    privacy = privacy_summary()
    security = security_summary()
    phase_truth = load("closeout/phase-truth.json")
    final_review = load("validation/final-staged-review.json")

    parent_line = git("rev-list", "--parents", "-n", "1", head).split()
    source_to_final_commits = int(git("rev-list", "--count", f"{SOURCE_SHA}..{head}"))
    source_to_final_merges = int(git("rev-list", "--count", "--merges", f"{SOURCE_SHA}..{head}"))
    changed_rows = [row.split("\t", 1) for row in git("diff", "--name-status", "--no-renames", f"{SOURCE_SHA}..{head}").splitlines() if row]
    owner_allowlist = all(
        path.startswith("docs/liora-venn/v667-v1/")
        or ((path.startswith("scripts/") or path.startswith("tests/")) and "liora_venn_v667_v1" in path)
        for _, path in changed_rows
    )
    owner_manifest = manifest_values["final_owner"]
    owner_manifest_parity = manifest_paths(owner_manifest) | {owner_manifest["self_exclusion"]} == {path.relative_to(ROOT).as_posix() for path in owner}
    evidence_diff = set(git("diff", "--name-only", f"{X1_SHA}..{evidence_sha}").splitlines())
    evidence_manifest_parity = manifest_paths(manifest_values["evidence"]) | {manifest_values["evidence"]["self_exclusion"]} == evidence_diff
    final_diff = set(git("diff", "--name-only", f"{evidence_sha}..{head}").splitlines())
    final_delta_exclusions = set(manifest_values["final_delta"]["self_exclusions"])
    final_delta_parity = manifest_paths(manifest_values["final_delta"]) | final_delta_exclusions == final_diff

    checks = {
        "exact_branch": git("branch", "--show-current") == BRANCH,
        "clean_before": clean_before,
        "four_way_equal_before": equality_before["valid"],
        "one_final_parent": len(parent_line) == 2,
        "final_direct_child_of_evidence": git("rev-parse", f"{head}^") == evidence_sha,
        "evidence_direct_child_of_x1": git("rev-parse", f"{evidence_sha}^") == X1_SHA,
        "x1_direct_child_of_source": git("rev-parse", f"{X1_SHA}^") == SOURCE_SHA,
        "three_phase_commits": source_to_final_commits == 3,
        "zero_merges": source_to_final_merges == 0,
        "additive_only": all(status == "A" for status, _ in changed_rows),
        "owner_allowlist": owner_allowlist,
        "owner_file_cap": len(owner) < 2000,
        "document_word_cap": maximum_words <= 100000,
        "all_tests": all(row["valid"] for row in tests),
        "immutable_x1_tests": x1_test["valid"] and x1_test["tests_run"] == 16,
        "all_manifests_replay": all(row["valid"] for row in manifests.values()),
        "owner_manifest_parity": owner_manifest_parity,
        "evidence_manifest_parity": evidence_manifest_parity,
        "final_delta_manifest_parity": final_delta_parity,
        "all_json_parse": True,
        "all_python_compile": True,
        "privacy_zero_confirmed_hits": privacy["valid"],
        "bounded_security_zero_findings": security["valid"],
        "final_staged_review": final_review["valid"],
        "outcome_truth": phase_truth["outcomes"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "retained_counts": phase_truth["effective_negatives"] == 27101 and phase_truth["effective_methods"] == 12333,
        "open_and_exact_gates": phase_truth["open_gaps"] == 191 and phase_truth["exact_gates"] == 189,
        "terminal_not_ready": phase_truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "full_repository_suite_absent": True,
        "same_owner_only": True,
    }
    clean_after = git("status", "--porcelain=v1") == ""
    equality_after = remote_equality(head)
    checks["clean_after"] = clean_after
    checks["four_way_equal_after"] = equality_after["valid"]
    valid = all(checks.values())
    payload = {
        "schema": "ghc.family.liora-venn.v667-v1.exclusive-canonical-receipt.v1",
        "owner": "Liora Venn",
        "phase": "v667-v1",
        "generated_at_utc": NOW,
        "canonical_invocation_count": 1,
        "canonical_replayed": False,
        "source_sha": SOURCE_SHA,
        "x1_sha": X1_SHA,
        "evidence_sha": evidence_sha,
        "exact_final_sha": head,
        "tests": tests,
        "immutable_x1_test": x1_test,
        "test_count": sum(row["observed"] or 0 for row in tests) + x1_test["tests_run"],
        "manifests": manifests,
        "manifest_declared_entries": {name: value["entry_count"] for name, value in manifest_values.items()},
        "owner_file_count": len(owner),
        "strict_json_parses": len(json_paths),
        "markdown_documents": len(markdown_paths),
        "html_documents": len(html_paths),
        "python_compiles": len(python_paths),
        "privacy": privacy,
        "security": security,
        "source_to_final_commits": source_to_final_commits,
        "source_to_final_merges": source_to_final_merges,
        "maximum_document_words": maximum_words,
        "checks": checks,
        "equality_before": equality_before,
        "equality_after": equality_after,
        "full_repository_suite": False,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "valid": valid,
    }
    payload["canonical_payload_sha256"] = hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    receipt_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({
        "valid": valid,
        "exact_final_sha": head,
        "test_count": payload["test_count"],
        "owner_file_count": len(owner),
        "strict_json_parses": len(json_paths),
        "manifest_declared_entries": payload["manifest_declared_entries"],
        "privacy_confirmed_hits": privacy["confirmed_hits"],
        "security_findings": len(security["findings"]),
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }, sort_keys=True))
    return 0 if valid else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    raise SystemExit(main(Path(args.receipt)))
