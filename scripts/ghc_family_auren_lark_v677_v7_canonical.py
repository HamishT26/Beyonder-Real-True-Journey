from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT_REL = "docs/auren-lark/v677-v7"
FINAL = REPO / ROOT_REL / "final"
VALIDATION = REPO / ROOT_REL / "validation"
SOURCE = "62ac8de91e2fec0d6a024f51eff6a3ad8d807a4d"
X1 = "73bf85d9371b74dda26953e743958ce684ea1436"
EVIDENCE = "3f91c32cb1acda2900ce69bedc60971353084775"
FAILED_FINAL = "4aaf45add92b18c5f8bef68ba15dd112e0f5703c"
EXPECTED_BRANCH = "codex/GHC-Family/auren-lark-v677-v7-full-tools"
RECEIPT_BASE = Path(
    "D:/GHC-Archives/validation-receipts/auren-lark/v677-v7"
)


def run(
    *args: str, check: bool = True
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=REPO,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=check,
    )


def git(*args: str) -> str:
    return run("git", *args).stdout.strip()


def git_bytes(spec: str) -> bytes:
    return subprocess.check_output(["git", "show", spec], cwd=REPO)


def normalized(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_json(value) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")


def load_blob(final_sha: str, path: str):
    return json.loads(git_bytes(f"{final_sha}:{path}").decode("utf-8"))


def replay_manifest(final_sha: str, path: str) -> tuple[dict, int]:
    manifest = load_blob(final_sha, path)
    for row in manifest["entries"]:
        raw = normalized(git_bytes(f"{final_sha}:{row['path']}"))
        if (
            len(raw) != row["bytes_normalized_lf"]
            or digest(raw) != row["sha256_normalized_lf"]
        ):
            raise RuntimeError(
                f"manifest mismatch: {path} -> {row['path']}"
            )
    return manifest, len(manifest["entries"])


def privacy_scan(
    final_sha: str, owner_manifest: dict
) -> tuple[list[dict], list[dict]]:
    patterns = {
        "private_absolute_path": re.compile(rb"(?i)[A-Z]:[\\/]+Users[\\/]+"),
        "raw_task_identifier": re.compile(
            rb"(?i)(source_thread_id|clientThreadId)"
        ),
        "credential_or_secret": re.compile(
            rb"(?i)(-----BEGIN [A-Z ]*PRIVATE KEY-----|AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9_]{20,})"
        ),
        "uuid_like_private_identifier": re.compile(
            rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
            re.I,
        ),
        "private_session_material": re.compile(
            rb"(?i)(private app state|session stream|raw transcript payload|screenshot payload)"
        ),
    }
    candidates: list[dict] = []
    confirmed: list[dict] = []
    for row in owner_manifest["entries"]:
        path = row["path"]
        if Path(path).suffix.lower() not in {
            ".json",
            ".md",
            ".txt",
            ".html",
            ".py",
            ".yaml",
            ".yml",
        }:
            continue
        raw = git_bytes(f"{final_sha}:{path}")
        for category, pattern in patterns.items():
            if pattern.search(raw):
                scanner_definition = path.startswith(("scripts/", "tests/"))
                item = {
                    "path": path,
                    "category": category,
                    "scanner_definition": scanner_definition,
                }
                candidates.append(item)
                if not scanner_definition:
                    confirmed.append(item)
    return candidates, confirmed


def fresh_equality(final_sha: str) -> dict:
    branch = git("branch", "--show-current")
    if branch != EXPECTED_BRANCH:
        raise RuntimeError(f"unexpected branch {branch}")
    upstream_name = git(
        "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"
    )
    if upstream_name != f"origin/{EXPECTED_BRANCH}":
        raise RuntimeError(f"unexpected upstream {upstream_name}")
    run(
        "git",
        "fetch",
        "origin",
        f"refs/heads/{EXPECTED_BRANCH}:refs/remotes/origin/{EXPECTED_BRANCH}",
    )
    local = git("rev-parse", "HEAD")
    upstream = git("rev-parse", "@{u}")
    tracking = git(
        "rev-parse", f"refs/remotes/origin/{EXPECTED_BRANCH}"
    )
    remote_rows = git(
        "ls-remote",
        "--heads",
        "origin",
        f"refs/heads/{EXPECTED_BRANCH}",
    ).splitlines()
    if len(remote_rows) != 1:
        raise RuntimeError(
            "fresh live remote did not return exactly one branch row"
        )
    live = remote_rows[0].split()[0]
    divergence = git(
        "rev-list", "--left-right", "--count", "HEAD...@{u}"
    ).split()
    if (
        [local, upstream, tracking, live] != [final_sha] * 4
        or divergence != ["0", "0"]
    ):
        raise RuntimeError(
            "four-way equality failed "
            f"local={local} upstream={upstream} tracking={tracking} "
            f"live={live} divergence={divergence}"
        )
    return {
        "branch": branch,
        "local": local,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live_remote": live,
        "ahead": 0,
        "behind": 0,
    }


def main() -> None:
    if len(sys.argv) != 2 or not re.fullmatch(r"[0-9a-f]{40}", sys.argv[1]):
        raise SystemExit("usage: canonical.py <exact-final-sha>")
    final_sha = sys.argv[1]
    receipt_dir = RECEIPT_BASE / final_sha
    try:
        os.makedirs(receipt_dir, exist_ok=False)
    except FileExistsError as exc:
        raise SystemExit(
            "exclusive receipt latch already exists; same-final retry forbidden"
        ) from exc

    attempt = {
        "state": "CANONICAL_ATTEMPT_RESERVED",
        "exact_final": final_sha,
        "reserved_utc": datetime.now(timezone.utc).isoformat(),
        "invocation_limit": 1,
    }
    (receipt_dir / "attempt.json").write_bytes(canonical_json(attempt))
    try:
        if git("rev-parse", "HEAD") != final_sha:
            raise RuntimeError("argument is not current exact HEAD")
        if git("status", "--porcelain"):
            raise RuntimeError("working tree is not clean before canonical")
        if (
            git("rev-parse", f"{X1}^") != SOURCE
            or git("rev-parse", f"{EVIDENCE}^") != X1
            or git("rev-parse", f"{FAILED_FINAL}^") != EVIDENCE
            or git("rev-parse", f"{final_sha}^") != FAILED_FINAL
        ):
            raise RuntimeError("direct-parent lifecycle mismatch")
        if int(git("rev-list", "--count", f"{SOURCE}..{final_sha}")) != 4:
            raise RuntimeError("phase commit count is not exactly four")
        if git("rev-list", "--merges", f"{SOURCE}..{final_sha}"):
            raise RuntimeError("merge commit detected")
        for sha in (X1, EVIDENCE, FAILED_FINAL, final_sha):
            if len(
                git("rev-list", "--parents", "-n", "1", sha).split()
            ) != 2:
                raise RuntimeError(
                    f"non-single-parent phase commit: {sha}"
                )

        equality = fresh_equality(final_sha)
        historical_delta, historical_delta_count = replay_manifest(
            FAILED_FINAL,
            f"{ROOT_REL}/validation/final-delta-manifest.json",
        )
        historical_owner, historical_owner_count = replay_manifest(
            FAILED_FINAL,
            f"{ROOT_REL}/validation/final-owner-manifest.json",
        )
        historical_seal, historical_seal_count = replay_manifest(
            FAILED_FINAL, f"{ROOT_REL}/final/content-seal.json"
        )
        correction_delta, correction_delta_count = replay_manifest(
            final_sha,
            f"{ROOT_REL}/validation/correction-delta-manifest.json",
        )
        correction_owner, correction_owner_count = replay_manifest(
            final_sha,
            f"{ROOT_REL}/validation/correction-owner-manifest.json",
        )
        if (
            historical_delta["status"] != "REPOSITORY_PREPARED_FINAL_DELTA"
            or historical_owner["status"]
            != "FINAL_OWNER_FROM_ILYRA_V677_V6_SOURCE"
            or historical_seal["status"]
            != "SEALED_REPOSITORY_PREPARED_FINAL"
            or correction_delta["status"]
            != "CORRECTION_DELTA_FROM_FAILED_CANONICAL_FINAL"
            or correction_owner["status"]
            != "CORRECTED_OWNER_FROM_ILYRA_V677_V6_SOURCE"
        ):
            raise RuntimeError("manifest or seal lifecycle status mismatch")

        json_parses = 0
        for row in correction_owner["entries"]:
            if row["path"].endswith(".json"):
                json.loads(
                    git_bytes(f"{final_sha}:{row['path']}").decode("utf-8")
                )
                json_parses += 1
        for path in correction_owner["self_exclusions"]:
            json.loads(git_bytes(f"{final_sha}:{path}").decode("utf-8"))
            json_parses += 1
        candidates, confirmed = privacy_scan(final_sha, correction_owner)
        if confirmed:
            raise RuntimeError(f"confirmed privacy findings: {confirmed}")
        historical_security = load_blob(
            FAILED_FINAL, f"{ROOT_REL}/final/bounded-security-review.json"
        )
        if (
            historical_security["findings"]
            or historical_security["medium_or_high_findings"] != 0
        ):
            raise RuntimeError(
                "historical bounded owner Python security review has findings"
            )
        correction_security = load_blob(
            final_sha,
            f"{ROOT_REL}/validation/correction-security-scan.json",
        )
        if correction_security["findings"]:
            raise RuntimeError(
                "bounded correction Python security review has findings"
            )
        failed_receipt = load_blob(
            final_sha,
            f"{ROOT_REL}/correction/failed-canonical-receipt.json",
        )
        if (
            failed_receipt["head"] != FAILED_FINAL
            or failed_receipt["status"]
            != "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT"
            or failed_receipt["tests_passed"] != 25
            or failed_receipt["tests_failed"] != 1
            or failed_receipt["same_head_retry_permitted"] is not False
        ):
            raise RuntimeError("failed canonical retention mismatch")
        correction_truth = load_blob(
            final_sha,
            f"{ROOT_REL}/correction/terminal-correction.json",
        )
        expected_counts = {
            "effective_negatives": 45718,
            "effective_methods": 43036,
            "retained_failed_witnesses": 17379,
            "bounded_passing_witnesses": 26362,
            "open_gaps": 389,
            "exact_gates": 380,
        }
        if any(
            correction_truth.get(key) != value
            for key, value in expected_counts.items()
        ):
            raise RuntimeError("corrected terminal truth mismatch")
        replay_recovery = load_blob(
            final_sha,
            f"{ROOT_REL}/correction/index-replay-recovery.json",
        )
        if (
            len(replay_recovery["pairs"]) != 2
            or replay_recovery["exact_streaming_replay_state"]
            != "EXACT_LENGTH_EXTERNAL_PRECOMMIT_EVIDENCE_ONLY"
            or replay_recovery["pairs"][1]["failure"]["state"]
            != "FAILED_ZERO_VALIDATION_CREDIT"
            or replay_recovery["pairs"][1]["failure"]["retained"] is not True
            or replay_recovery["pairs"][1]["recovery"]["state"]
            != "bounded_passing_exact_length_streaming_recovery"
            or replay_recovery["pairs"][1]["recovery"][
                "failed_streaming_attempt_replayed"
            ]
            is not False
            or
            replay_recovery["failure"]["state"]
            != "FAILED_ZERO_VALIDATION_CREDIT"
            or replay_recovery["failure"]["retained"] is not True
            or replay_recovery["recovery"]["state"]
            != "bounded_passing_streaming_recovery"
            or replay_recovery["recovery"]["failed_batch_replayed"] is not False
            or replay_recovery["repository_mutation_during_failure"] is not False
            or replay_recovery["tests_run_during_failure_or_recovery"] != 0
        ):
            raise RuntimeError("correction index-replay retention mismatch")

        test = run(
            sys.executable,
            "-B",
            "-m",
            "pytest",
            "-q",
            "-p",
            "no:cacheprovider",
            "tests/test_ghc_family_auren_lark_v677_v7_final.py::test_method_flow_preserves_failures_and_closeout_witnesses",
            "tests/test_ghc_family_auren_lark_v677_v7_correction.py",
            check=False,
        )
        if test.returncode != 0:
            raise RuntimeError(
                "owner final tests failed\n"
                f"STDOUT:\n{test.stdout}\nSTDERR:\n{test.stderr}"
            )
        match = re.search(r"(\d+) passed", test.stdout)
        if not match:
            raise RuntimeError(
                f"could not parse test count from output: {test.stdout}"
            )
        tests_passed = int(match.group(1))
        if git("status", "--porcelain"):
            raise RuntimeError("working tree changed during canonical")
        equality_after = fresh_equality(final_sha)

        payload = {
            "state": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
            "owner": "Auren Lark",
            "phase": "v677-v7",
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "failed_canonical_final": FAILED_FINAL,
            "exact_final": final_sha,
            "tests_passed": tests_passed,
            "previous_failed_head_tests_passed": 25,
            "previous_failed_head_tests_failed": 1,
            "previously_passing_final_tests_replayed": False,
            "historical_delta_manifest_entries": historical_delta_count,
            "historical_owner_manifest_entries": historical_owner_count,
            "historical_content_seal_entries": historical_seal_count,
            "correction_delta_manifest_entries": correction_delta_count,
            "correction_owner_manifest_entries": correction_owner_count,
            "strict_json_parses": json_parses,
            "privacy_classes": 5,
            "privacy_candidates": len(candidates),
            "confirmed_privacy_hits": 0,
            "historical_bounded_security_reviewed_files": historical_security[
                "reviewed_file_count"
            ],
            "correction_bounded_security_reviewed_files": correction_security[
                "changed_python_parses"
            ],
            "bounded_security_findings": 0,
            "phase_commits": 4,
            "merges": 0,
            "single_parent_commits": 4,
            "clean_before_and_after": True,
            "four_way_equality_before": equality,
            "four_way_equality_after": equality_after,
            "complete_repository_suite": False,
            "same_owner_validation": True,
            "independent_reproduction": False,
            "prior_failed_canonical": {
                "head": FAILED_FINAL,
                "status": "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT",
            },
            "total_canonical_attempts_across_distinct_heads": 2,
            "total_canonical_successes": 1,
            "one_success_no_replay": True,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        }
        payload_bytes = canonical_json(payload)
        payload_sha256 = digest(payload_bytes)
        receipt = {
            "status": payload["state"],
            "payload_sha256": payload_sha256,
            "payload": payload,
            "test_stdout": test.stdout.strip(),
            "completed_utc": datetime.now(timezone.utc).isoformat(),
        }
        receipt_bytes = (
            json.dumps(
                receipt,
                indent=2,
                ensure_ascii=False,
                sort_keys=True,
            )
            + "\n"
        ).encode("utf-8")
        (receipt_dir / "canonical-receipt.json").write_bytes(receipt_bytes)
        print(
            json.dumps(
                {
                    "status": payload["state"],
                    "exact_final": final_sha,
                    "payload_sha256": payload_sha256,
                    "external_receipt_sha256": digest(receipt_bytes),
                    "tests_passed": tests_passed,
                    "json_parses": json_parses,
                    "owner_manifest_entries": correction_owner_count,
                },
                sort_keys=True,
            )
        )
    except Exception as exc:
        failure = {
            "status": "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
            "exact_final": final_sha,
            "error": str(exc),
            "same_final_retry_forbidden": True,
            "completed_utc": datetime.now(timezone.utc).isoformat(),
        }
        failure_bytes = (
            json.dumps(
                failure,
                indent=2,
                ensure_ascii=False,
                sort_keys=True,
            )
            + "\n"
        ).encode("utf-8")
        (receipt_dir / "failed-canonical-receipt.json").write_bytes(
            failure_bytes
        )
        print(
            json.dumps(
                {
                    "status": failure["status"],
                    "exact_final": final_sha,
                    "failed_receipt_sha256": digest(failure_bytes),
                    "error": str(exc),
                },
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        raise SystemExit(1)


if __name__ == "__main__":
    main()
