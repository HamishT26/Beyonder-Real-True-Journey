#!/usr/bin/env python3
"""One-shot dependency-corrected terminal composite for v676-v7-r2."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


SOURCE = "e66201e9efd19cb3fc98baf672ea4df440758616"
FAILED_FINAL = "cee57870903bdb12dd908623bf29a49b63cc464e"
FAILED_RECEIPT_SHA256 = "f92408636933aae36fdd22e36432c31bab97febf10f459766e6cda2a54b5c426"
ROOT = "docs/sylven-arc/v676-v7-r2"
CORRECTION = f"{ROOT}/correction1"
MANIFEST = f"{CORRECTION}/delta-manifest.json"
REVIEW = f"{CORRECTION}/staged-review.json"
TEST_NODE = (
    "tests/test_ghc_family_sylven_arc_v676_v7_r2_final.py::"
    "test_baton_is_sanitized_prepared_state_not_delivery"
)


def git(repo: Path, *args: str, binary: bool = False):
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=not binary,
        encoding=None if binary else "utf-8",
    )
    return result.stdout if binary else result.stdout.strip()


def normalize(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def blob(repo: Path, revision: str, relative: str) -> bytes:
    return git(repo, "show", f"{revision}:{relative}", binary=True)


def load_blob(repo: Path, revision: str, relative: str) -> Any:
    return json.loads(blob(repo, revision, relative).decode("utf-8"))


def reserve(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, indent=2, sort_keys=True)
        handle.write("\n")


def sanitize(value: str, repo: Path, receipt_root: Path) -> str:
    return value.replace(str(repo), "<repo>").replace(str(receipt_root), "<receipt-root>")[:4000]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--expected-final", required=True)
    parser.add_argument("--receipt-root", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    receipt_root = args.receipt_root.resolve()
    expected_final = args.expected_final
    lock = receipt_root / f"correction1-composite-{expected_final}.lock.json"
    receipt = receipt_root / f"correction1-composite-{expected_final}.json"
    failure_receipt = receipt_root / f"correction1-composite-{expected_final}-failed.json"
    reserve(
        lock,
        {
            "schema": "ghc-family-exclusive-correction-composite-latch/v1",
            "phase": "v676-v7-r2-correction1",
            "expected_final": expected_final,
            "invocation_reserved": 1,
            "replay_permitted": False,
        },
    )
    try:
        head = git(repo, "rev-parse", "HEAD")
        if head != expected_final:
            raise RuntimeError("corrected exact final mismatch")
        if git(repo, "status", "--porcelain"):
            raise RuntimeError("corrected final worktree is not clean")
        if git(repo, "rev-parse", "HEAD^") != FAILED_FINAL:
            raise RuntimeError("correction is not the direct child of the failed final")

        branch = git(repo, "branch", "--show-current")
        upstream = git(repo, "rev-parse", "@{upstream}")
        tracking = git(repo, "rev-parse", f"refs/remotes/origin/{branch}")
        live_line = git(repo, "ls-remote", "--heads", "origin", f"refs/heads/{branch}")
        live = live_line.split()[0] if live_line else ""
        if len({head, upstream, tracking, live}) != 1:
            raise RuntimeError("corrected local/upstream/tracking/fresh-live refs differ")
        if git(repo, "rev-list", "--left-right", "--count", "HEAD...@{upstream}").split() != ["0", "0"]:
            raise RuntimeError("corrected typed divergence is not zero-zero")

        commit_count = int(git(repo, "rev-list", "--count", f"{SOURCE}..HEAD"))
        merges = list(filter(None, git(repo, "rev-list", "--merges", f"{SOURCE}..HEAD").splitlines()))
        parents = list(filter(None, git(repo, "rev-list", "--parents", "--reverse", f"{SOURCE}..HEAD").splitlines()))
        if commit_count != 4 or merges or any(len(line.split()) != 2 for line in parents):
            raise RuntimeError("correction topology is not four direct single-parent commits and zero merges")

        changed = set(filter(None, git(repo, "diff", "--name-only", FAILED_FINAL, "HEAD").splitlines()))
        manifest = load_blob(repo, "HEAD", MANIFEST)
        review = load_blob(repo, "HEAD", REVIEW)
        expected_changed = {row["path"] for row in manifest["entries"]} | set(manifest["declared_self_exclusions"])
        if changed != expected_changed:
            raise RuntimeError("correction changed-path set differs from its manifest contract")
        if any(path.startswith(f"{ROOT}/final/") or f"{ROOT}/x1/" in path or f"{ROOT}/x2/" in path for path in changed):
            raise RuntimeError("correction altered immutable lifecycle content")
        mismatches = []
        for row in manifest["entries"]:
            observed = hashlib.sha256(normalize(blob(repo, "HEAD", row["path"]))).hexdigest()
            if observed != row["sha256_normalized_lf"]:
                mismatches.append(row["path"])
        if mismatches:
            raise RuntimeError("correction manifest mismatch")
        if review["confirmed_privacy_or_raw_identifier_hits"] != 0:
            raise RuntimeError("correction staged review has confirmed privacy hits")

        immutable_paths = [
            f"{ROOT}/final/content-seal.json",
            f"{ROOT}/final/handoffs/caelen-morrow-v676-v8-activation-candidate.md",
            f"{ROOT}/validation/final-delta-manifest.json",
            f"{ROOT}/validation/final-owner-manifest.json",
        ]
        for relative in immutable_paths:
            if blob(repo, FAILED_FINAL, relative) != blob(repo, "HEAD", relative):
                raise RuntimeError("correction changed immutable final evidence")

        failed_receipt = receipt_root / f"canonical-{FAILED_FINAL}-failed.json"
        if not failed_receipt.is_file():
            raise RuntimeError("failed canonical receipt is missing")
        if hashlib.sha256(failed_receipt.read_bytes()).hexdigest() != FAILED_RECEIPT_SHA256:
            raise RuntimeError("failed canonical receipt digest mismatch")

        test_result = subprocess.run(
            [sys.executable, "-X", "utf8", "-m", "pytest", "-q", TEST_NODE],
            cwd=repo,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
        )
        if test_result.returncode != 0 or not re.search(r"1 passed", test_result.stdout):
            raise RuntimeError("isolated failed dependency did not pass: " + test_result.stdout[-2000:])

        payload = {
            "schema": "ghc-family-dependency-corrected-terminal-composite/v1",
            "status": "VALID_DEPENDENCY_CORRECTED_EXACT_FINAL_COMPOSITE_WITH_ZERO_FAILED_CANONICAL_CREDIT",
            "phase": "v676-v7-r2-correction1",
            "owner": "Sylven Arc",
            "source": SOURCE,
            "failed_canonical_final": FAILED_FINAL,
            "corrected_exact_final": head,
            "branch": branch,
            "failed_canonical_receipt_sha256": FAILED_RECEIPT_SHA256,
            "failed_canonical_invocation_count": 1,
            "failed_canonical_success_credit": 0,
            "failed_canonical_replay_count": 0,
            "retained_passing_owner_test_observations": 19,
            "isolated_failed_dependency_passed": 1,
            "dependency_corrected_owner_test_composite": "20/20",
            "correction_composite_invocation_count": 1,
            "correction_composite_success_count": 1,
            "correction_composite_replay_count": 0,
            "correction_manifest_entries": len(manifest["entries"]),
            "correction_changed_paths": len(changed),
            "immutable_final_artifacts_replayed": 4,
            "commit_count_from_immutable_first_final": commit_count,
            "merge_count": 0,
            "one_parent_per_phase_commit": True,
            "clean_state": True,
            "typed_divergence": [0, 0],
            "four_way_equality": True,
            "full_owner_test_module_replayed": False,
            "full_repository_suite_run": False,
            "repository_seal_rewritten": False,
            "effective_external_overlay_after_composite": {
                "effective_negatives": 43193,
                "effective_methods": 35457,
                "retained_failed_witnesses": 14854,
                "bounded_passing_witnesses": 21292,
                "open_gaps": 365,
                "exact_gates": 356
            },
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "independent_reproduction": False,
            "exhaustive_security": False,
            "empirical_professional_production_legal_cultural_maori_or_stage20_authority": False,
        }
        payload["composite_payload_sha256"] = hashlib.sha256(
            json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        reserve(receipt, payload)
        print(json.dumps(payload, sort_keys=True))
        return 0
    except Exception as exc:
        failure = {
            "schema": "ghc-family-dependency-corrected-terminal-composite-failure/v1",
            "status": "INVALID_DEPENDENCY_CORRECTED_TERMINAL_COMPOSITE",
            "phase": "v676-v7-r2-correction1",
            "expected_final": expected_final,
            "invocation_count": 1,
            "success_count": 0,
            "replay_count": 0,
            "retry_same_final_permitted": False,
            "error": sanitize(f"{type(exc).__name__}: {exc}", repo, receipt_root),
        }
        reserve(failure_receipt, failure)
        print(json.dumps(failure, sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
