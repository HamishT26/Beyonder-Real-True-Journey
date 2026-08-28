from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "3ba783297438ee89d5778065e30de737af470855"
X1_COMMIT = "763969929943d9c9bcb674999508fe33694fa357"
EVIDENCE_COMMIT = "7d0a8f09df1bf70f69369ad78e5c3da4fce85c66"
BRANCH = "codex/GHC-Family/auren-lark-v674-v1-full-tools"
X1_MANIFEST = "docs/auren-lark/v674-v1/x1/x1-manifest.json"
EVIDENCE_MANIFEST = "docs/auren-lark/v674-v1/validation/x2-evidence-manifest.json"
FINAL_MANIFEST = "docs/auren-lark/v674-v1/validation/final-index-manifest.json"
GIT_CMD = shutil.which("git.exe") or shutil.which("git")


def git_command() -> str:
    if not GIT_CMD:
        raise RuntimeError("Git executable is absent")
    return GIT_CMD


def git_text(*args: str) -> str:
    return subprocess.run(  # nosec B603
        [git_command(), "-C", str(ROOT), *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


def git_bytes(head: str, path: str) -> bytes:
    return subprocess.check_output(  # nosec B603
        [git_command(), "-C", str(ROOT), "cat-file", "blob", f"{head}:{path}"]
    )


def normalized(blob: bytes) -> bytes:
    return blob.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def strict_json(blob: bytes) -> Any:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    return json.loads(blob.decode("utf-8"), object_pairs_hook=reject_duplicates)


def replay_raw_manifest(head: str, manifest_path: str) -> tuple[int, int]:
    manifest = strict_json(git_bytes(head, manifest_path))
    failures: list[str] = []
    for row in manifest["entries"]:
        blob = git_bytes(head, row["path"])
        if len(blob) != row["bytes"] or hashlib.sha256(blob).hexdigest() != row["sha256"]:
            failures.append(row["path"])
    if failures:
        raise RuntimeError(f"raw manifest replay failures: {failures[:3]}")
    return manifest["entry_count"], len(failures)


def replay_normalized_manifest(head: str, manifest_path: str) -> tuple[int, int]:
    manifest = strict_json(git_bytes(head, manifest_path))
    failures: list[str] = []
    for row in manifest["entries"]:
        blob = normalized(git_bytes(head, row["path"]))
        if len(blob) != row["bytes"] or hashlib.sha256(blob).hexdigest() != row["sha256_normalized_lf"]:
            failures.append(row["path"])
    if failures:
        raise RuntimeError(f"normalized manifest replay failures: {failures[:3]}")
    return manifest["entry_count"], len(failures)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--receipt-dir", required=True)
    args = parser.parse_args()
    receipt_dir = Path(args.receipt_dir)
    receipt_dir.mkdir(parents=True, exist_ok=False)
    receipt_path = receipt_dir / "canonical-receipt.json"
    receipt: dict[str, Any] = {
        "status": "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "expected_head": args.expected_head,
        "invoked_once": True,
        "successful_replay_permitted": False,
        "full_repository_suite": False,
        "independent_reproduction": False,
        "checks": [],
    }
    try:
        head = git_text("rev-parse", "HEAD")
        parent = git_text("rev-parse", "HEAD^")
        grandparent = git_text("rev-parse", "HEAD^^")
        great_grandparent = git_text("rev-parse", "HEAD^^^")
        branch = git_text("branch", "--show-current")
        upstream = git_text("rev-parse", "@{upstream}")
        tracking = git_text("rev-parse", f"refs/remotes/origin/{BRANCH}")
        fresh = git_text("ls-remote", "origin", f"refs/heads/{BRANCH}").split()[0]
        divergence = git_text("rev-list", "--left-right", "--count", f"HEAD...refs/remotes/origin/{BRANCH}").split()
        clean = not git_text("status", "--porcelain")
        commits = int(git_text("rev-list", "--count", f"{SOURCE}..{head}"))
        merges = int(git_text("rev-list", "--merges", "--count", f"{SOURCE}..{head}"))
        if head != args.expected_head:
            raise RuntimeError("expected-head mismatch")
        if parent != EVIDENCE_COMMIT or grandparent != X1_COMMIT or great_grandparent != SOURCE:
            raise RuntimeError("direct source/x1/evidence/final ancestry mismatch")
        if branch != BRANCH or commits != 3 or merges != 0:
            raise RuntimeError("branch or history mismatch")
        if not clean or len({head, upstream, tracking, fresh}) != 1 or divergence != ["0", "0"]:
            raise RuntimeError("clean, divergence, or four-way equality mismatch")
        receipt["checks"].extend(
            [
                "exact_head",
                "direct_source_x1_evidence_final_ancestry",
                "exact_branch",
                "three_commits",
                "zero_merges",
                "clean_state",
                "zero_divergence",
                "four_way_equality",
            ]
        )

        x1_entries, _ = replay_raw_manifest(X1_COMMIT, X1_MANIFEST)
        evidence_entries, _ = replay_normalized_manifest(EVIDENCE_COMMIT, EVIDENCE_MANIFEST)
        final_entries, _ = replay_normalized_manifest(head, FINAL_MANIFEST)
        receipt["checks"].extend(["frozen_x1_manifest_replay", "immutable_x2_manifest_replay", "final_manifest_replay"])

        changed = git_text("diff", "--name-only", SOURCE, head).splitlines()
        owner_paths = [
            path
            for path in changed
            if path.startswith(
                (
                    "docs/auren-lark/v674-v1/",
                    "scripts/build_ghc_family_auren_lark_v674_v1_",
                    "scripts/validate_ghc_family_auren_lark_v674_v1_",
                    "scripts/ghc_family_seismic_",
                    "tests/test_ghc_family_auren_lark_v674_v1_",
                )
            )
        ]
        if set(changed) != set(owner_paths):
            raise RuntimeError("source-to-final path escaped Auren owner scope")
        if len(owner_paths) >= 2000:
            raise RuntimeError("owner path ceiling exceeded")
        receipt["checks"].extend(["owner_scope", "file_ceiling"])

        json_paths = [path for path in owner_paths if path.endswith(".json")]
        for path in json_paths:
            strict_json(git_bytes(head, path))
        receipt["checks"].append("strict_json")

        patterns = {
            "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
            "openai_token": re.compile(r"(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}"),
            "github_token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
            "aws_access_key": re.compile(r"\bAKIA[A-Z0-9]{16}\b"),
            "consumer_email": re.compile(
                r"\b[A-Za-z0-9._%+-]+@(gmail|outlook|hotmail|yahoo)\.[A-Za-z]{2,}\b",
                re.IGNORECASE,
            ),
        }
        text_paths = [
            path for path in owner_paths if Path(path).suffix.lower() in {".json", ".md", ".py", ".txt", ".html"}
        ]
        privacy_hits: list[dict[str, str]] = []
        for path in text_paths:
            text = git_bytes(head, path).decode("utf-8")
            for label, pattern in patterns.items():
                if pattern.search(text):
                    privacy_hits.append({"path": path, "class": label})
        if privacy_hits:
            raise RuntimeError(f"privacy candidates: {privacy_hits[:3]}")
        receipt["checks"].append("five_class_privacy")

        python_paths = [path for path in owner_paths if path.endswith(".py")]
        security_findings: list[dict[str, object]] = []
        for path in python_paths:
            tree = ast.parse(git_bytes(head, path).decode("utf-8"), filename=path)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                    security_findings.append({"path": path, "line": node.lineno})
                if isinstance(node, ast.Call):
                    for keyword in node.keywords:
                        if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                            security_findings.append({"path": path, "line": node.lineno})
        if security_findings:
            raise RuntimeError(f"security findings: {security_findings[:3]}")
        receipt["checks"].append("bounded_python_security")

        pytest_result = subprocess.run(  # nosec B603
            [
                sys.executable,
                "-m",
                "pytest",
                "-q",
                "tests/test_ghc_family_auren_lark_v674_v1_x2.py",
                "tests/test_ghc_family_auren_lark_v674_v1_final.py",
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if pytest_result.returncode != 0:
            raise RuntimeError(f"final test failure: {pytest_result.stdout[-1500:]}")
        receipt["checks"].append("x2_and_final_tests")

        receipt.update(
            {
                "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
                "head": head,
                "parent": parent,
                "grandparent": grandparent,
                "great_grandparent": great_grandparent,
                "branch": branch,
                "local": head,
                "upstream": upstream,
                "tracking": tracking,
                "fresh_live_remote": fresh,
                "divergence": {"ahead": 0, "behind": 0},
                "source_to_final_commits": commits,
                "source_to_final_merges": merges,
                "x1_manifest_entries": x1_entries,
                "evidence_manifest_entries": evidence_entries,
                "final_manifest_entries": final_entries,
                "json_parses": len(json_paths),
                "privacy_files": len(text_paths),
                "privacy_confirmed_hits": 0,
                "python_files": len(python_paths),
                "security_findings": 0,
                "owner_paths": len(owner_paths),
                "owner_file_ceiling": 2000,
                "test_output": pytest_result.stdout.strip(),
                "terminal_verdict": "NOT_READY_FOR_STAGE_20",
                "claims": {
                    "complete_repository_suite": False,
                    "independent_reproduction": False,
                    "complete_privacy": False,
                    "complete_accessibility": False,
                    "exhaustive_security": False,
                    "production_certification": False,
                    "stage_20_authority": False,
                },
            }
        )
    except (
        IndexError,
        OSError,
        RuntimeError,
        subprocess.SubprocessError,
        SyntaxError,
        UnicodeDecodeError,
        ValueError,
    ) as exc:
        receipt["failure"] = f"{type(exc).__name__}: {exc}"
        receipt_path.write_text(
            json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        return 1

    canonical_payload = json.dumps(receipt, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    receipt["canonical_payload_sha256"] = hashlib.sha256(canonical_payload.encode("utf-8")).hexdigest()
    receipt_path.write_text(
        json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
