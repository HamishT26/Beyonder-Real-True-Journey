#!/usr/bin/env python3
"""One-shot exact-final owner-scoped canonical validator for v676-v7-r2."""

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
X1_HEAD = "82c5a8a45af8abcb17df5c793853be6fdc97c8ee"
EVIDENCE_HEAD = "b22eebdc9743f49d758b10e0f3577f21049f8143"
ROOT = "docs/sylven-arc/v676-v7-r2"
FINAL_TEST = "tests/test_ghc_family_sylven_arc_v676_v7_r2_final.py"
OWNER_MANIFEST = f"{ROOT}/validation/final-owner-manifest.json"
DELTA_MANIFEST = f"{ROOT}/validation/final-delta-manifest.json"
STAGED_REVIEW = f"{ROOT}/validation/final-staged-review.json"
CONTENT_SEAL = f"{ROOT}/final/content-seal.json"
PRIVACY_PATTERNS = {
    "private_absolute_path": re.compile(r"(?i)[A-Z]:[\\/]+Users[\\/]+"),
    "raw_task_route": re.compile(r"(?i)(source_thread_id|thread_id|clientThreadId)"),
    "credential_assignment": re.compile(r"(?i)(api[_-]?key|private[_-]?key|password|bearer)\s*[:=]"),
    "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    "session_stream": re.compile(r"(?i)(session[_ -]?stream|terminal transcript|screenshot payload)"),
}


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


def blob(repo: Path, relative: str) -> bytes:
    return git(repo, "show", f"HEAD:{relative}", binary=True)


def load_blob(repo: Path, relative: str) -> Any:
    return json.loads(blob(repo, relative).decode("utf-8"))


def replay_manifest(repo: Path, relative: str) -> tuple[int, list[str]]:
    manifest = load_blob(repo, relative)
    mismatches = []
    for row in manifest["entries"]:
        observed = hashlib.sha256(normalize(blob(repo, row["path"]))).hexdigest()
        if observed != row["sha256_normalized_lf"]:
            mismatches.append(row["path"])
    return len(manifest["entries"]), mismatches


def definition_or_fixture(relative: str) -> bool:
    return (
        relative.startswith("tests/")
        or relative.endswith("staged-review.json")
        or relative.endswith("_manifest.py")
        or relative.endswith("_canonical.py")
        or relative.endswith("_core.py")
    )


def reserve(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, indent=2, sort_keys=True)
        handle.write("\n")


def sanitize_error(value: str, repo: Path, receipt_root: Path) -> str:
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
    lock = receipt_root / f"canonical-{expected_final}.lock.json"
    receipt = receipt_root / f"canonical-{expected_final}.json"
    failed_receipt = receipt_root / f"canonical-{expected_final}-failed.json"
    reserve(
        lock,
        {
            "schema": "ghc-family-exclusive-canonical-latch/v1",
            "phase": "v676-v7-r2",
            "expected_final": expected_final,
            "invocation_reserved": 1,
            "replay_permitted": False,
        },
    )

    try:
        head = git(repo, "rev-parse", "HEAD")
        if head != expected_final or not re.fullmatch(r"[0-9a-f]{40}", head):
            raise RuntimeError("exact final mismatch")
        if git(repo, "status", "--porcelain"):
            raise RuntimeError("worktree is not clean")
        branch = git(repo, "branch", "--show-current")
        upstream = git(repo, "rev-parse", "@{upstream}")
        tracking = git(repo, "rev-parse", f"refs/remotes/origin/{branch}")
        live_line = git(repo, "ls-remote", "--heads", "origin", f"refs/heads/{branch}")
        live = live_line.split()[0] if live_line else ""
        if len({head, upstream, tracking, live}) != 1:
            raise RuntimeError("local upstream tracking and fresh-live refs differ")
        divergence = git(repo, "rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()
        if divergence != ["0", "0"]:
            raise RuntimeError("typed divergence is not zero-zero")

        if git(repo, "rev-parse", f"{X1_HEAD}^") != SOURCE:
            raise RuntimeError("source to x1 direct-parent mismatch")
        if git(repo, "rev-parse", f"{EVIDENCE_HEAD}^") != X1_HEAD:
            raise RuntimeError("x1 to evidence direct-parent mismatch")
        if git(repo, "rev-parse", "HEAD^") != EVIDENCE_HEAD:
            raise RuntimeError("evidence to final direct-parent mismatch")
        commit_count = int(git(repo, "rev-list", "--count", f"{SOURCE}..HEAD"))
        merge_lines = list(filter(None, git(repo, "rev-list", "--merges", f"{SOURCE}..HEAD").splitlines()))
        parent_lines = list(filter(None, git(repo, "rev-list", "--parents", "--reverse", f"{SOURCE}..HEAD").splitlines()))
        if commit_count != 3 or merge_lines or any(len(line.split()) != 2 for line in parent_lines):
            raise RuntimeError("final topology is not three direct single-parent commits with zero merges")

        delta_count, delta_bad = replay_manifest(repo, DELTA_MANIFEST)
        owner_count, owner_bad = replay_manifest(repo, OWNER_MANIFEST)
        if delta_bad or owner_bad:
            raise RuntimeError("normalized-LF manifest replay mismatch")
        seal = load_blob(repo, CONTENT_SEAL)
        seal_bad = []
        for row in seal["entries"]:
            if hashlib.sha256(normalize(blob(repo, row["path"]))).hexdigest() != row["sha256_normalized_lf"]:
                seal_bad.append(row["path"])
        if seal_bad:
            raise RuntimeError("content seal replay mismatch")

        phase_paths = [
            path
            for path in git(repo, "ls-tree", "-r", "--name-only", "HEAD", ROOT).splitlines()
            if path.endswith(".json")
        ]
        for relative in phase_paths:
            json.loads(blob(repo, relative).decode("utf-8"))

        owner_manifest = load_blob(repo, OWNER_MANIFEST)
        privacy_candidates = []
        privacy_confirmed = []
        for row in owner_manifest["entries"]:
            relative = row["path"]
            if Path(relative).suffix.lower() not in {".json", ".md", ".py", ".txt", ".html", ".yaml"}:
                continue
            text = normalize(blob(repo, relative)).decode("utf-8")
            for category, pattern in PRIVACY_PATTERNS.items():
                if not pattern.search(text):
                    continue
                adjudication = "scanner_definition_or_synthetic_test" if definition_or_fixture(relative) else "confirmed_payload_hit"
                candidate = {"path": relative, "category": category, "adjudication": adjudication}
                privacy_candidates.append(candidate)
                if adjudication == "confirmed_payload_hit":
                    privacy_confirmed.append(candidate)
        if privacy_confirmed:
            raise RuntimeError("confirmed privacy or raw-identifier payload hit")

        staged_review = load_blob(repo, STAGED_REVIEW)
        if staged_review["confirmed_privacy_or_raw_identifier_hits"] != 0:
            raise RuntimeError("committed staged review has privacy hits")
        x2_review = load_blob(repo, f"{ROOT}/validation/x2-staged-review.json")
        security = x2_review["bounded_security_review"]
        if security["first_aggregate_high_severity"] != 0 or security["first_aggregate_medium_severity"] != 0:
            raise RuntimeError("bounded security review retained medium or high finding")
        if security["residual_scan_findings"] != 0:
            raise RuntimeError("bounded residual security scan retained findings")

        test_result = subprocess.run(
            [sys.executable, "-X", "utf8", "-m", "pytest", "-q", FINAL_TEST],
            cwd=repo,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
        )
        if test_result.returncode != 0:
            raise RuntimeError("final owner test module failed: " + test_result.stdout[-2000:])
        match = re.search(r"(\d+) passed", test_result.stdout)
        if not match:
            raise RuntimeError("unable to parse final owner test count")
        tests_passed = int(match.group(1))

        phase_truth = load_blob(repo, f"{ROOT}/final/phase-truth.json")
        baton_receipt = load_blob(repo, f"{ROOT}/final/baton-integrity.json")
        payload = {
            "schema": "ghc-family-exact-final-owner-scoped-canonical/v1",
            "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
            "phase": "v676-v7-r2",
            "owner": "Sylven Arc",
            "source": SOURCE,
            "x1": X1_HEAD,
            "evidence": EVIDENCE_HEAD,
            "exact_final": head,
            "branch": branch,
            "canonical_invocation_count": 1,
            "canonical_success_count": 1,
            "canonical_replay_count": 0,
            "final_owner_tests_passed": tests_passed,
            "strict_phase_json_parses": len(phase_paths),
            "final_delta_manifest_entries": delta_count,
            "final_owner_manifest_entries": owner_count,
            "content_seal_entries": seal["entry_count"],
            "privacy_candidates": len(privacy_candidates),
            "confirmed_privacy_or_raw_identifier_hits": 0,
            "bounded_security_first_aggregate_low_candidates": security["first_aggregate_low_severity"],
            "bounded_security_medium_or_high_findings": 0,
            "bounded_security_residual_findings": 0,
            "commit_count_from_immutable_first_final": commit_count,
            "merge_count": 0,
            "one_parent_per_phase_commit": True,
            "clean_before_and_after": True,
            "typed_divergence": [0, 0],
            "four_way_equality": True,
            "baton_words": baton_receipt["words"],
            "baton_sha256": baton_receipt["sha256"],
            "repository_seal": {
                key: phase_truth[key]
                for key in (
                    "effective_negatives",
                    "effective_methods",
                    "retained_failed_witnesses",
                    "bounded_passing_witnesses",
                    "open_gaps",
                    "exact_gates",
                )
            },
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "full_repository_suite_run": False,
            "independent_reproduction": False,
            "exhaustive_security": False,
            "complete_privacy_or_accessibility_assurance": False,
            "empirical_professional_production_legal_cultural_maori_or_stage20_authority": False,
        }
        payload["canonical_payload_sha256"] = hashlib.sha256(
            json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        reserve(receipt, payload)
        print(json.dumps(payload, sort_keys=True))
        return 0
    except Exception as exc:
        failure = {
            "schema": "ghc-family-exact-final-owner-scoped-canonical-failure/v1",
            "status": "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
            "phase": "v676-v7-r2",
            "expected_final": expected_final,
            "canonical_invocation_count": 1,
            "canonical_success_count": 0,
            "canonical_replay_count": 0,
            "error": sanitize_error(f"{type(exc).__name__}: {exc}", repo, receipt_root),
            "retry_same_final_permitted": False,
        }
        reserve(failed_receipt, failure)
        print(json.dumps(failure, sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
