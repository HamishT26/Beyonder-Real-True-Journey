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
ROOT_REL = "docs/auren-lark/v679-v6"
FINAL = REPO / ROOT_REL / "final"
SOURCE = "3bbb29f9c7d2fe13a44ce607cda3e88323546dda"
X1 = "5d72a72dc0fe8062d8cb2e56efdf83e175a92d86"
EVIDENCE = "4ea13458e0a21c5fbee6a62544190937caea860a"
EXPECTED_BRANCH = "codex/GHC-Family/auren-lark-v679-v6-full-tools"
RECEIPT_BASE = Path("D:/GHC-Archives/validation-receipts/auren-lark/v679-v6")


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
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


class GitBlobBatch:
    """Read exact Git blobs through one persistent cat-file process."""

    def __init__(self) -> None:
        self.process: subprocess.Popen[bytes] | None = None
        self.cache: dict[str, bytes] = {}

    def __enter__(self) -> "GitBlobBatch":
        self.process = subprocess.Popen(
            ["git", "cat-file", "--batch"],
            cwd=REPO,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return self

    def read(self, spec: str) -> bytes:
        if spec in self.cache:
            return self.cache[spec]
        if (
            self.process is None
            or self.process.stdin is None
            or self.process.stdout is None
        ):
            raise RuntimeError("Git blob batch is not open")
        self.process.stdin.write(spec.encode("utf-8") + b"\n")
        self.process.stdin.flush()
        header = (
            self.process.stdout.readline()
            .decode("utf-8", errors="replace")
            .strip()
        )
        parts = header.split()
        if len(parts) != 3 or parts[1] != "blob":
            raise RuntimeError(f"unexpected cat-file header for {spec}: {header}")
        size = int(parts[2])
        raw = self.process.stdout.read(size)
        separator = self.process.stdout.read(1)
        if len(raw) != size or separator != b"\n":
            raise RuntimeError(f"truncated cat-file payload for {spec}")
        self.cache[spec] = raw
        return raw

    def __exit__(self, exc_type, exc, traceback) -> None:
        if self.process is None:
            return
        if self.process.stdin is not None:
            self.process.stdin.close()
        returncode = self.process.wait(timeout=30)
        if returncode and exc is None:
            stderr = (
                b""
                if self.process.stderr is None
                else self.process.stderr.read()
            )
            raise RuntimeError(
                f"git cat-file --batch failed: {stderr.decode('utf-8', errors='replace')}"
            )


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


def load_blob(batch: GitBlobBatch, final_sha: str, path: str):
    return json.loads(batch.read(f"{final_sha}:{path}").decode("utf-8"))


def replay_manifest(
    batch: GitBlobBatch, final_sha: str, path: str
) -> tuple[dict, int]:
    manifest = load_blob(batch, final_sha, path)
    for row in manifest["entries"]:
        raw = normalized(batch.read(f"{final_sha}:{row['path']}"))
        if (
            len(raw) != row["bytes_normalized_lf"]
            or digest(raw) != row["sha256_normalized_lf"]
        ):
            raise RuntimeError(f"manifest mismatch: {path} -> {row['path']}")
    return manifest, len(manifest["entries"])


def privacy_scan(
    batch: GitBlobBatch, final_sha: str, owner_manifest: dict
) -> tuple[list[dict], list[dict]]:
    patterns = {
        "private_absolute_path": re.compile(rb"(?i)[A-Z]:[\\/]+Users[\\/]+"),
        "raw_task_identifier": re.compile(rb"(?i)(source_thread_id|clientThreadId)"),
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
        raw = batch.read(f"{final_sha}:{path}")
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
    tracking = git("rev-parse", f"refs/remotes/origin/{EXPECTED_BRANCH}")
    remote_rows = git(
        "ls-remote", "--heads", "origin", f"refs/heads/{EXPECTED_BRANCH}"
    ).splitlines()
    if len(remote_rows) != 1:
        raise RuntimeError("fresh live remote did not return exactly one branch row")
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
            or git("rev-parse", f"{final_sha}^") != EVIDENCE
        ):
            raise RuntimeError("direct-parent lifecycle mismatch")
        if int(git("rev-list", "--count", f"{SOURCE}..{final_sha}")) != 3:
            raise RuntimeError("phase commit count is not exactly three")
        if git("rev-list", "--merges", f"{SOURCE}..{final_sha}"):
            raise RuntimeError("merge commit detected")
        for sha in (X1, EVIDENCE, final_sha):
            if len(git("rev-list", "--parents", "-n", "1", sha).split()) != 2:
                raise RuntimeError(f"non-single-parent phase commit: {sha}")

        equality = fresh_equality(final_sha)
        with GitBlobBatch() as blobs:
            delta, delta_count = replay_manifest(
                blobs,
                final_sha,
                f"{ROOT_REL}/validation/final-delta-manifest.json",
            )
            owner, owner_count = replay_manifest(
                blobs,
                final_sha,
                f"{ROOT_REL}/validation/final-owner-manifest.json",
            )
            seal, seal_count = replay_manifest(
                blobs,
                final_sha,
                f"{ROOT_REL}/final/content-seal.json",
            )
            if (
                delta["status"] != "REPOSITORY_PREPARED_FINAL_DELTA"
                or owner["status"] != "FINAL_OWNER_FROM_ILYRA_V679_V5_SOURCE"
                or seal["status"] != "SEALED_REPOSITORY_PREPARED_FINAL"
            ):
                raise RuntimeError("manifest or seal lifecycle status mismatch")

            json_parses = 0
            for row in owner["entries"]:
                if row["path"].endswith(".json"):
                    json.loads(
                        blobs.read(f"{final_sha}:{row['path']}").decode("utf-8")
                    )
                    json_parses += 1
            candidates, confirmed = privacy_scan(blobs, final_sha, owner)
            if confirmed:
                raise RuntimeError(f"confirmed privacy findings: {confirmed}")
            security = load_blob(
                blobs,
                final_sha,
                f"{ROOT_REL}/final/bounded-security-review.json",
            )
            if security["findings"] or security["medium_or_high_findings"] != 0:
                raise RuntimeError(
                    "bounded owner Python security review has findings"
                )

        test = run(
            sys.executable,
            "-B",
            "-m",
            "pytest",
            "-q",
            "-p",
            "no:cacheprovider",
            "tests/test_ghc_family_auren_lark_v679_v6_final.py",
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
            "phase": "v679-v6",
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "exact_final": final_sha,
            "tests_passed": tests_passed,
            "delta_manifest_entries": delta_count,
            "owner_manifest_entries": owner_count,
            "content_seal_entries": seal_count,
            "strict_json_parses": json_parses,
            "privacy_classes": 5,
            "privacy_candidates": len(candidates),
            "confirmed_privacy_hits": 0,
            "bounded_security_reviewed_files": security["reviewed_file_count"],
            "bounded_security_findings": 0,
            "phase_commits": 3,
            "merges": 0,
            "single_parent_commits": 3,
            "clean_before_and_after": True,
            "four_way_equality_before": equality,
            "four_way_equality_after": equality_after,
            "complete_repository_suite": False,
            "same_owner_validation": True,
            "independent_reproduction": False,
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
            json.dumps(receipt, indent=2, ensure_ascii=False, sort_keys=True)
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
                    "owner_manifest_entries": owner_count,
                    "delta_manifest_entries": delta_count,
                    "content_seal_entries": seal_count,
                    "privacy_candidates": len(candidates),
                    "bounded_security_reviewed_files": security[
                        "reviewed_file_count"
                    ],
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
            json.dumps(failure, indent=2, ensure_ascii=False, sort_keys=True)
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
