#!/usr/bin/env python3
"""One-shot exact-final scoped canonical validator for v656-v5."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
ROOT_REL = "docs/eiren-kestrel/v656-v5"
ROOT = REPO / ROOT_REL
SOURCE = "c1518e6873068f6cc20ff69a30437d69404ef057"
X1 = "e313d47c1bc6386d3dbdf1773d1d7cb4026bc7f9"
EVIDENCE = "f9662c901407a86cf271eef9b54467a782c99455"
CLOSEOUT = "3181608db19f39bb7b91be01fc62e64840a86c5e"
BRANCH = "codex/GHC-Family/eiren-kestrel-v656-v5-full-tools"


def run(*args: str, text: bool = True) -> str | bytes:
    env = os.environ.copy()
    env.update(
        {
            "PYTHONUTF8": "1",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    result = subprocess.run(
        list(args),
        cwd=REPO,
        check=True,
        capture_output=True,
        text=text,
        encoding="utf-8" if text else None,
        env=env,
    )
    return result.stdout.strip() if text else result.stdout


def git_text(*args: str) -> str:
    value = run("git", *args)
    assert isinstance(value, str)
    return value


def tree_map(commit: str) -> dict[str, str]:
    raw = subprocess.run(
        ["git", "ls-tree", "-r", "-z", commit],
        cwd=REPO,
        check=True,
        capture_output=True,
    ).stdout
    result: dict[str, str] = {}
    for record in raw.split(b"\0"):
        if not record:
            continue
        metadata, path = record.split(b"\t", 1)
        _mode, kind, oid = metadata.decode("ascii").split()
        if kind == "blob":
            result[path.decode("utf-8")] = oid
    return result


def blobs(commit: str, paths: list[str]) -> dict[str, bytes]:
    mapping = tree_map(commit)
    missing = [path for path in paths if path not in mapping]
    if missing:
        raise RuntimeError(f"paths missing from {commit}: {missing[:5]}")
    oids = [mapping[path] for path in paths]
    completed = subprocess.run(
        ["git", "cat-file", "--batch"],
        cwd=REPO,
        input=("".join(f"{oid}\n" for oid in oids)).encode("ascii"),
        check=True,
        capture_output=True,
    )
    stream = io.BytesIO(completed.stdout)
    result: dict[str, bytes] = {}
    for path, expected_oid in zip(paths, oids):
        header = stream.readline().decode("ascii").strip().split()
        if len(header) != 3 or header[0] != expected_oid or header[1] != "blob":
            raise RuntimeError(f"unexpected cat-file header for {path}: {header}")
        size = int(header[2])
        data = stream.read(size)
        newline = stream.read(1)
        if newline != b"\n":
            raise RuntimeError(f"missing cat-file separator for {path}")
        result[path] = data
    return result


def json_blob(blob: bytes) -> Any:
    return json.loads(blob.decode("utf-8"))


def manifest_check(
    final: str,
    base: str,
    manifest_path: str,
) -> dict[str, Any]:
    manifest_blob = blobs(final, [manifest_path])[manifest_path]
    manifest = json_blob(manifest_blob)
    entries = {item["path"]: item for item in manifest["entries"]}
    exclusions = {item["path"] for item in manifest["declared_exclusions"]}
    actual = set(
        filter(None, git_text("diff", "--name-only", base, final).splitlines())
    )
    expected = set(entries) | exclusions
    if expected != actual:
        raise RuntimeError(
            f"manifest path mismatch {manifest_path}: "
            f"missing={sorted(actual-expected)[:5]} extra={sorted(expected-actual)[:5]}"
        )
    content = blobs(final, sorted(entries))
    for path, entry in entries.items():
        data = content[path]
        if len(data) != entry["bytes"]:
            raise RuntimeError(f"manifest byte mismatch: {path}")
        if hashlib.sha256(data).hexdigest() != entry["sha256"]:
            raise RuntimeError(f"manifest sha mismatch: {path}")
    return {
        "manifest": manifest_path,
        "entries": len(entries),
        "exclusions": len(exclusions),
        "actual_paths": len(actual),
        "valid": True,
    }


def selected_unit_tests() -> dict[str, Any]:
    modules = [
        "tests.test_ghc_family_v656_v5_x1",
        "tests.test_ghc_family_v656_v5_core",
        "tests.test_ghc_family_v656_v5_validation",
        "tests.test_ghc_family_v656_v5_closeout",
        "tests.test_ghc_family_v656_v5_correction",
    ]
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    excluded = {
        (
            "tests.test_ghc_family_v656_v5_x1."
            "EirenKestrelV656V5X1Tests.test_manifest_bytes_hashes_and_exact_path_set"
        ),
        (
            "tests.test_ghc_family_v656_v5_x1."
            "EirenKestrelV656V5X1Tests.test_x1_contains_no_x2_surface_or_observed_outcome"
        ),
    }
    selected_names: list[str] = []
    for module in modules:
        loaded = loader.loadTestsFromName(module)
        for group in loaded:
            for test in group:
                test_id = test.id()
                if test_id in excluded:
                    continue
                suite.addTest(test)
                selected_names.append(test_id)
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise RuntimeError(f"selected unit tests failed:\n{stream.getvalue()}")
    return {
        "selected": result.testsRun,
        "passed": result.testsRun,
        "failed": len(result.failures) + len(result.errors),
        "excluded": [
            {
                "test": sorted(excluded)[0],
                "reason": (
                    "x1 lifecycle-local working-head path assertion; replaced by exact "
                    "commit-local x1 manifest replay at immutable x1"
                ),
            },
            {
                "test": sorted(excluded)[1],
                "reason": (
                    "x1 lifecycle-local absence assertion; replaced by exact x1 tree "
                    "inspection in the correction test module"
                ),
            },
        ],
        "replacement": [
            "manifest_check(final=X1, base=SOURCE, x1-file-manifest)",
            "correction test inspects immutable x1 tree for absent x2 paths and outcomes",
        ],
        "output_tail": stream.getvalue().splitlines()[-4:],
    }


def privacy_scan(owner_blobs: dict[str, bytes]) -> dict[str, Any]:
    patterns = {
        "raw_uuid": re.compile(
            r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"
        ),
        "private_absolute_path": re.compile(
            r"(?i)(?:[a-z]:\\\\users\\\\[^\\\\\s]+|[a-z]:\\\\ghc-archives)"
        ),
        "credential_or_token": re.compile(
            r"(?i)(?:api[_-]?key|access[_-]?token|authorization:\s*bearer|sk-[a-z0-9]{12,})\s*[:=]"
        ),
        "raw_task_identifier": re.compile(
            r"(?i)(?:source_thread_id|thread_id|task_id|conversation_id)\s*[:=]"
        ),
        "private_callable_detail": re.compile(
            r"(?i)(?:send_message_to_thread|private_target|callable_route_id)\s*[:=(]"
        ),
    }
    hits = {label: [] for label in patterns}
    scanned = 0
    for path, data in owner_blobs.items():
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        scanned += 1
        for label, pattern in patterns.items():
            if pattern.search(text):
                hits[label].append(path)
    confirmed = sum(len(value) for value in hits.values())
    if confirmed:
        raise RuntimeError(f"privacy scan hits: {hits}")
    return {
        "classes": len(patterns),
        "scanned_files": scanned,
        "confirmed_hits": confirmed,
        "valid": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    receipt = Path(args.receipt)
    if receipt.exists():
        raise RuntimeError("successful canonical receipt already exists; replay refused")
    receipt.parent.mkdir(parents=True, exist_ok=True)
    if str(REPO) not in sys.path:
        sys.path.insert(0, str(REPO))

    final = git_text("rev-parse", "HEAD")
    if final != args.expected_head:
        raise RuntimeError(f"head mismatch: {final} != {args.expected_head}")
    if git_text("branch", "--show-current") != BRANCH:
        raise RuntimeError("wrong branch")
    if git_text("status", "--porcelain=v1", "--untracked-files=all"):
        raise RuntimeError("worktree is not clean")
    upstream = git_text("rev-parse", "@{upstream}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_raw = git_text("ls-remote", "origin", f"refs/heads/{BRANCH}")
    live = live_raw.split("\t")[0]
    divergence = git_text("rev-list", "--left-right", "--count", "HEAD...@{upstream}")
    if not (final == upstream == tracking == live) or divergence != "0\t0":
        raise RuntimeError("four-way equality or divergence check failed")

    commits = git_text("rev-list", "--reverse", f"{SOURCE}..{final}").splitlines()
    if commits != [X1, EVIDENCE, CLOSEOUT, final]:
        raise RuntimeError(f"unexpected phase history: {commits}")
    if git_text("rev-list", "--count", "--merges", f"{SOURCE}..{final}") != "0":
        raise RuntimeError("merge commit found")
    for commit in commits:
        if len(git_text("show", "-s", "--format=%P", commit).split()) != 1:
            raise RuntimeError(f"non-single-parent commit: {commit}")
    if git_text("rev-parse", f"{CLOSEOUT}^") != EVIDENCE:
        raise RuntimeError("closeout candidate is not direct child of evidence")
    if git_text("rev-parse", f"{final}^") != CLOSEOUT:
        raise RuntimeError("corrected final is not direct child of closeout candidate")

    manifests = [
        manifest_check(
            X1,
            SOURCE,
            f"{ROOT_REL}/validation/x1-file-manifest.json",
        ),
        manifest_check(
            EVIDENCE,
            X1,
            f"{ROOT_REL}/validation/evidence-candidate-manifest.json",
        ),
        manifest_check(
            CLOSEOUT,
            EVIDENCE,
            f"{ROOT_REL}/validation/final-staged-manifest.json",
        ),
        manifest_check(
            final,
            CLOSEOUT,
            f"{ROOT_REL}/validation/correction-staged-manifest.json",
        ),
        manifest_check(
            final,
            SOURCE,
            f"{ROOT_REL}/validation/final-owner-manifest.json",
        ),
    ]
    owner_paths = sorted(
        filter(None, git_text("diff", "--name-only", SOURCE, final).splitlines())
    )
    if len(owner_paths) > 2000:
        raise RuntimeError("owner file cap exceeded")
    owner_content = blobs(final, owner_paths)
    json_paths = [path for path in owner_paths if path.endswith(".json")]
    for path in json_paths:
        json_blob(owner_content[path])

    max_words = 0
    max_word_path = ""
    for path, data in owner_content.items():
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        words = len(text.split())
        if words > max_words:
            max_words = words
            max_word_path = path
        if words > 100000:
            raise RuntimeError(f"document word cap exceeded: {path} {words}")
    baton_path = f"{ROOT_REL}/handoffs/elaren-kestrel-v656-v6-activation.md"
    baton_words = len(
        owner_content[baton_path].decode("utf-8").split()
    )
    if not 10000 <= baton_words <= 100000:
        raise RuntimeError(f"baton word count outside bounds: {baton_words}")

    sys.path.insert(0, str(REPO / "scripts"))
    from ghc_family_v656_v5_validate import validate

    tests = selected_unit_tests()
    validation = validate()
    if not validation["valid"]:
        raise RuntimeError("82/82 detailed or 15/15 minimal validation failed")
    privacy = privacy_scan(owner_content)

    outcome = json_blob(
        owner_content[f"{ROOT_REL}/truth/phase-truth-final.json"]
    )
    method_flow = json_blob(
        owner_content[f"{ROOT_REL}/method-flow/method-flow-ledger-final.json"]
    )
    if outcome["outcomes"] != {
        "completed": 23,
        "represented": 5,
        "open_gap": 1,
        "exact_gate": 1,
    }:
        raise RuntimeError("outcome truth mismatch")
    if (
        outcome["effective_negatives"] != 14549
        or outcome["effective_open_gaps"] != 101
        or outcome["effective_exact_gates"] != 100
    ):
        raise RuntimeError("effective negative, gap, or gate count mismatch")
    if (
        method_flow["counts"]["methods"] != 835
        or method_flow["counts"]["witness_results"] != {"fail": 835, "pass": 835}
    ):
        raise RuntimeError("Method Flow count mismatch")
    if outcome["verdict"] != "NOT_READY_FOR_STAGE_20":
        raise RuntimeError("terminal verdict mismatch")

    payload = {
        "schema": "ghc.family.v656-v5.final-validation-receipt.v1",
        "valid": True,
        "canonical_test_aggregate_run": True,
        "canonical_success_credit": True,
        "post_success_replay": False,
        "full_repository_suite_run": False,
        "independent_reproduction": False,
        "same_owner_only": True,
        "exact_head": final,
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "closeout_candidate": CLOSEOUT,
        "corrected_final": final,
        "phase_commits": 4,
        "merge_commits": 0,
        "single_parent_phase_commits": 4,
        "closeout_direct_child_of_evidence": True,
        "corrected_final_direct_child_of_closeout": True,
        "four_way_equality": {
            "local": final,
            "upstream": upstream,
            "tracking": tracking,
            "fresh_live": live,
            "divergence": divergence,
            "valid": True,
        },
        "tests": tests,
        "detailed": {
            "count": validation["detailed"]["count"],
            "passed": validation["detailed"]["passed"],
        },
        "minimal": {
            "count": validation["minimal"]["count"],
            "passed": validation["minimal"]["passed"],
        },
        "json_parses": len(json_paths),
        "privacy": privacy,
        "manifests": manifests,
        "owner_files": len(owner_paths),
        "max_document_words": max_words,
        "max_document_word_path": max_word_path,
        "baton_words": baton_words,
        "outcomes": outcome["outcomes"],
        "effective_negatives": outcome["effective_negatives"],
        "effective_open_gaps": outcome["effective_open_gaps"],
        "effective_exact_gates": outcome["effective_exact_gates"],
        "method_flow": method_flow["counts"],
        "terminal_verdict": outcome["verdict"],
        "boundary": (
            "One same-owner dependency-justified scoped aggregate under shared "
            "infrastructure only; not the full repository suite, independent reproduction, "
            "external audit, exhaustive security, privacy-complete or accessibility-complete "
            "assurance, empirical or professional validation, legal or cultural ratification, "
            "Māori authority, consciousness or personhood evidence, Theory-of-Everything "
            "proof, or Stage 20 authority."
        ),
    }
    encoded = (
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    temp = receipt.with_suffix(receipt.suffix + ".partial")
    temp.write_bytes(encoded)
    temp.replace(receipt)
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
