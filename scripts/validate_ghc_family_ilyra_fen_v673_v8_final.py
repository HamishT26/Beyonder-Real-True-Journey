from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "c1818f0c09737c69a1870ef6bf8ed7fc339cb727"
X1_COMMIT = "b567a67858066e6c23f3abb82828f5185d7ab65e"
EVIDENCE_COMMIT = "ca26e19e01d117055130da6201ac001311fd41d2"
BRANCH = "codex/GHC-Family/ilyra-fen-v673-v8-full-tools"
MANIFEST_PATH = "docs/ilyra-fen/v673-v8/validation/final-index-manifest.json"


def git_text(*args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


def git_bytes(head: str, path: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(ROOT), "cat-file", "blob", f"{head}:{path}"])


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
        "full_repository_suite": False,
        "independent_reproduction": False,
        "checks": [],
    }
    try:
        head = git_text("rev-parse", "HEAD")
        parent = git_text("rev-parse", "HEAD^")
        grandparent = git_text("rev-parse", "HEAD^^")
        branch = git_text("branch", "--show-current")
        upstream = git_text("rev-parse", "@{upstream}")
        tracking = git_text("rev-parse", f"refs/remotes/origin/{BRANCH}")
        fresh = git_text("ls-remote", "origin", f"refs/heads/{BRANCH}").split()[0]
        clean = not git_text("status", "--porcelain")
        commits = int(git_text("rev-list", "--count", f"{SOURCE}..{head}"))
        merges = int(git_text("rev-list", "--merges", "--count", f"{SOURCE}..{head}"))
        if head != args.expected_head:
            raise RuntimeError("expected-head mismatch")
        if parent != EVIDENCE_COMMIT or grandparent != X1_COMMIT:
            raise RuntimeError("direct final ancestry mismatch")
        if branch != BRANCH or commits != 3 or merges != 0:
            raise RuntimeError("branch or history mismatch")
        if not clean or len({head, upstream, tracking, fresh}) != 1:
            raise RuntimeError("clean or four-way equality mismatch")
        receipt["checks"].extend(
            [
                "exact_head",
                "direct_parent",
                "direct_grandparent",
                "exact_branch",
                "three_commits",
                "zero_merges",
                "clean_state",
                "four_way_equality",
            ]
        )

        manifest = strict_json(git_bytes(head, MANIFEST_PATH))
        manifest_failures = []
        for row in manifest["entries"]:
            blob = normalized(git_bytes(head, row["path"]))
            if len(blob) != row["bytes"]:
                manifest_failures.append(f"bytes:{row['path']}")
            if hashlib.sha256(blob).hexdigest() != row["sha256_normalized_lf"]:
                manifest_failures.append(f"sha:{row['path']}")
        if manifest_failures:
            raise RuntimeError(f"manifest replay failures: {manifest_failures[:3]}")
        receipt["checks"].append("final_manifest_replay")

        changed = git_text("diff", "--name-only", SOURCE, head).splitlines()
        owner_paths = [
            path
            for path in changed
            if path.startswith(
                (
                    "docs/ilyra-fen/v673-v8/",
                    "scripts/build_ghc_family_ilyra_fen_v673_v8_",
                    "scripts/validate_ghc_family_ilyra_fen_v673_v8_",
                    "scripts/ghc_family_loom_",
                    "tests/test_ghc_family_ilyra_fen_v673_v8_",
                )
            )
        ]
        if set(changed) != set(owner_paths):
            raise RuntimeError("source-to-final path escaped owner scope")
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
        privacy_hits = []
        text_paths = [
            path
            for path in owner_paths
            if Path(path).suffix.lower() in {".json", ".md", ".py", ".txt"}
        ]
        for path in text_paths:
            text = git_bytes(head, path).decode("utf-8")
            for label, pattern in patterns.items():
                if pattern.search(text):
                    privacy_hits.append({"path": path, "class": label})
        if privacy_hits:
            raise RuntimeError(f"privacy candidates: {privacy_hits[:3]}")
        receipt["checks"].append("five_class_privacy")

        security_findings = []
        python_paths = [path for path in owner_paths if path.endswith(".py")]
        for path in python_paths:
            tree = ast.parse(git_bytes(head, path).decode("utf-8"), filename=path)
            for node in ast.walk(tree):
                if (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Name)
                    and node.func.id in {"eval", "exec"}
                ):
                    security_findings.append({"path": path, "line": node.lineno})
                if isinstance(node, ast.Call):
                    for keyword in node.keywords:
                        if (
                            keyword.arg == "shell"
                            and isinstance(keyword.value, ast.Constant)
                            and keyword.value.value is True
                        ):
                            security_findings.append({"path": path, "line": node.lineno})
        if security_findings:
            raise RuntimeError(f"security findings: {security_findings[:3]}")
        receipt["checks"].append("bounded_python_security")

        pytest_result = subprocess.run(
            [
                "python",
                "-m",
                "pytest",
                "-q",
                "tests/test_ghc_family_ilyra_fen_v673_v8_final.py",
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if pytest_result.returncode != 0:
            raise RuntimeError(f"final test failure: {pytest_result.stdout[-1000:]}")
        receipt["checks"].append("final_tests")

        receipt.update(
            {
                "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
                "head": head,
                "parent": parent,
                "grandparent": grandparent,
                "branch": branch,
                "local": head,
                "upstream": upstream,
                "tracking": tracking,
                "fresh_live_remote": fresh,
                "source_to_final_commits": commits,
                "source_to_final_merges": merges,
                "manifest_entries": manifest["entry_count"],
                "json_parses": len(json_paths),
                "privacy_files": len(text_paths),
                "privacy_confirmed_hits": 0,
                "python_files": len(python_paths),
                "security_findings": 0,
                "owner_paths": len(owner_paths),
                "materialized_file_ceiling": 2000,
                "final_test_output": pytest_result.stdout.strip(),
                "terminal_verdict": "NOT_READY_FOR_STAGE_20",
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
        payload = json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
        receipt_path.write_text(payload, encoding="utf-8", newline="\n")
        return 1

    canonical_payload = json.dumps(receipt, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    receipt["canonical_payload_sha256"] = hashlib.sha256(canonical_payload.encode()).hexdigest()
    receipt_path.write_text(
        json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
