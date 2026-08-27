#!/usr/bin/env python3
"""One-shot exact-final owner-scoped canonical validator for Auren v672-v2."""

from __future__ import annotations

import argparse
import ast
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

SOURCE = "40db1e418c1251e12d77f832c0890869b990dba5"
X1 = "821a40be02af8db39524dc862aeaadf32e1543c3"
EVIDENCE = "e735ac99202e9ad69252ed39ce9eb41d684bf671"
BRANCH = "codex/GHC-Family/auren-lark-v672-v2-full-tools"
PHASE_PREFIX = "docs/auren-lark/v672-v2/"


def git(root: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(root), *args])


def git_text(root: Path, *args: str) -> str:
    return git(root, *args).decode("utf-8").strip()


def git_json(root: Path, commit: str, path: str) -> dict:
    return json.loads(git(root, "show", f"{commit}:{path}").decode("utf-8"))


def replay_manifest(
    root: Path,
    manifest: dict,
    anchor: str,
    field: str = "entries",
) -> tuple[int, list[dict[str, object]]]:
    mismatches = []
    rows = manifest[field]
    for expected in rows:
        path = expected["path"]
        blob_id = git_text(root, "rev-parse", f"{anchor}:{path}")
        blob = git(root, "cat-file", "blob", blob_id)
        actual = {
            "bytes": len(blob),
            "sha256": hashlib.sha256(blob).hexdigest(),
            "git_blob": blob_id,
        }
        for key in ("bytes", "sha256", "git_blob"):
            if key in expected and expected[key] != actual[key]:
                mismatches.append(
                    {
                        "path": path,
                        "field": key,
                        "expected": expected[key],
                        "actual": actual[key],
                    }
                )
    return len(rows), mismatches


def selected_test_run(root: Path, test_path: Path, cwd: Path) -> dict[str, object]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [
            sys.executable,
            "-B",
            "-m",
            "pytest",
            "-q",
            "-p",
            "no:cacheprovider",
            str(test_path),
        ],
        cwd=cwd,
        env=env,
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
    )
    output = completed.stdout + completed.stderr
    match = re.search(r"(\d+) passed", output)
    passed = int(match.group(1)) if match else 0
    return {
        "path": test_path.relative_to(cwd).as_posix()
        if test_path.is_relative_to(cwd)
        else test_path.name,
        "exit": completed.returncode,
        "passed": passed,
        "output_sha256": hashlib.sha256(output.encode("utf-8")).hexdigest(),
    }


def materialize_x1(root: Path, scratch_parent: Path) -> Path:
    scratch = Path(tempfile.mkdtemp(prefix="x1-context-", dir=scratch_parent))
    paths = [
        "docs/auren-lark/v672-v2/x1",
        "docs/auren-lark/v672-v2/validation/x1-staged-review.json",
        "scripts/build_ghc_family_auren_lark_v672_v2_x1.py",
        "scripts/build_ghc_family_auren_lark_v672_v2_staged_review.py",
        "tests/test_ghc_family_auren_lark_v672_v2_x1.py",
    ]
    archive = git(root, "archive", "--format=tar", X1, *paths)
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as bundle:
        members = bundle.getmembers()
        if any(member.name.startswith(("/", "../")) or "/../" in member.name for member in members):
            raise RuntimeError("unsafe x1 archive member")
        bundle.extractall(scratch, filter="data")
    return scratch


def privacy_scan(root: Path, head: str) -> tuple[int, list[dict[str, str]]]:
    paths = git_text(root, "diff", "--name-only", SOURCE, head).splitlines()
    text_suffixes = {".json", ".md", ".py", ".txt", ".yaml", ".yml", ".toml"}
    patterns = {
        "aws_access_key": re.compile(rb"A" + rb"KIA[0-9A-Z]{16}"),
        "github_token": re.compile(rb"gh" + rb"p_[A-Za-z0-9]{20,}"),
        "private_key": re.compile(rb"BEGIN [A-Z ]*PRIVATE" + rb" KEY"),
        "raw_task_identifier": re.compile(rb"\b019[a-f0-9]{5}-[a-f0-9-]{20,}\b"),
        "credential_assignment": re.compile(rb"(?i)(password|secret|token)\s*[:=]\s*['\"][^'\"]{8,}"),
    }
    hits = []
    scanned = 0
    for path in paths:
        if Path(path).suffix.lower() not in text_suffixes:
            continue
        blob = git(root, "show", f"{head}:{path}")
        scanned += 1
        for name, pattern in patterns.items():
            if pattern.search(blob):
                hits.append({"path": path, "privacy_class": name})
    return scanned, hits


def security_scan(root: Path, head: str) -> tuple[int, list[dict[str, object]]]:
    paths = [
        path
        for path in git_text(root, "diff", "--name-only", SOURCE, head).splitlines()
        if path.endswith(".py")
    ]
    findings = []
    for path in paths:
        tree = ast.parse(git(root, "show", f"{head}:{path}").decode("utf-8"), filename=path)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                findings.append({"path": path, "line": node.lineno, "kind": node.func.id})
            for keyword in node.keywords:
                if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                    findings.append({"path": path, "line": node.lineno, "kind": "shell_true"})
    return len(paths), findings


def validate(root: Path, expected_head: str, receipt_path: Path) -> dict:
    if receipt_path.exists():
        raise RuntimeError("successful canonical receipt already exists; replay refused")
    failed_path = receipt_path.with_name("canonical-failed-001.json")
    if failed_path.exists():
        raise RuntimeError("failed canonical receipt already exists; aggregate replay refused")

    local = git_text(root, "rev-parse", "HEAD")
    branch = git_text(root, "branch", "--show-current")
    upstream = git_text(root, "rev-parse", "@{upstream}")
    tracking = git_text(root, "rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_rows = git_text(root, "ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}").splitlines()
    live = live_rows[0].split()[0] if len(live_rows) == 1 else ""
    divergence = git_text(root, "rev-list", "--left-right", "--count", "HEAD...@{upstream}")
    status = git_text(root, "status", "--porcelain=v1", "--untracked-files=all")
    if not (
        local == expected_head == upstream == tracking == live
        and branch == BRANCH
        and divergence.replace("\t", " ") == "0 0"
        and status == ""
    ):
        raise RuntimeError("exact-final clean fresh-four-way preflight failed")
    parents = git_text(root, "show", "-s", "--format=%P", expected_head).split()
    if parents != [EVIDENCE]:
        raise RuntimeError("final is not the direct single parent child of evidence")
    if git_text(root, "rev-parse", f"{X1}^") != SOURCE:
        raise RuntimeError("x1 parent mismatch")
    if git_text(root, "rev-parse", f"{EVIDENCE}^") != X1:
        raise RuntimeError("evidence parent mismatch")
    commit_count = int(git_text(root, "rev-list", "--count", f"{SOURCE}..{expected_head}"))
    merge_count = int(
        git_text(root, "rev-list", "--count", "--merges", f"{SOURCE}..{expected_head}")
    )
    if commit_count != 3 or merge_count != 0:
        raise RuntimeError("source-to-final history mismatch")

    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    x1_context = materialize_x1(root, receipt_path.parent)
    test_runs = [
        selected_test_run(
            root,
            x1_context / "tests" / "test_ghc_family_auren_lark_v672_v2_x1.py",
            x1_context,
        ),
        selected_test_run(
            root,
            root / "tests" / "test_ghc_family_auren_lark_v672_v2_x2.py",
            root,
        ),
        selected_test_run(
            root,
            root / "tests" / "test_ghc_family_auren_lark_v672_v2_final.py",
            root,
        ),
    ]
    if any(run["exit"] != 0 for run in test_runs):
        raise RuntimeError("selected owner test module failed")

    json_paths = sorted((root / PHASE_PREFIX).rglob("*.json"))
    for path in json_paths:
        json.loads(path.read_text(encoding="utf-8"))

    x1_build = git_json(
        root, X1, "docs/auren-lark/v672-v2/x1/build-receipt.json"
    )
    x1_count, x1_mismatches = replay_manifest(root, x1_build, X1, field="manifest")
    x2_manifest = git_json(
        root, EVIDENCE, "docs/auren-lark/v672-v2/x2/owner-manifest.json"
    )
    x2_count, x2_mismatches = replay_manifest(root, x2_manifest, EVIDENCE)
    evidence_manifest = git_json(
        root,
        expected_head,
        "docs/auren-lark/v672-v2/closeout/immutable-evidence-manifest.json",
    )
    evidence_count, evidence_mismatches = replay_manifest(
        root, evidence_manifest, EVIDENCE
    )
    closeout_manifest = git_json(
        root, expected_head, "docs/auren-lark/v672-v2/closeout/owner-manifest.json"
    )
    closeout_count, closeout_mismatches = replay_manifest(
        root, closeout_manifest, expected_head
    )
    all_manifest_mismatches = (
        x1_mismatches + x2_mismatches + evidence_mismatches + closeout_mismatches
    )
    if all_manifest_mismatches:
        raise RuntimeError("manifest replay mismatch")

    privacy_files, privacy_hits = privacy_scan(root, expected_head)
    python_files, security_findings = security_scan(root, expected_head)
    if privacy_hits or security_findings:
        raise RuntimeError("privacy or bounded security gate failed")

    review = git_json(
        root,
        expected_head,
        "docs/auren-lark/v672-v2/validation/final-staged-review.json",
    )
    if not review.get("valid"):
        raise RuntimeError("final staged review invalid")
    truth = git_json(
        root, expected_head, "docs/auren-lark/v672-v2/closeout/phase-truth.json"
    )
    route = git_json(
        root, expected_head, "docs/auren-lark/v672-v2/closeout/route-candidate.json"
    )
    if truth["terminal_verdict"] != "NOT_READY_FOR_STAGE_20":
        raise RuntimeError("terminal verdict promotion")
    if route["delivery_state"] != "PREPARED_NOT_SENT" or route["send_count"] != 0:
        raise RuntimeError("route state promoted before validation")

    materialized_files = sum(
        1
        for path in root.rglob("*")
        if path.is_file() and path.name != ".git"
    )
    if materialized_files >= 2000:
        raise RuntimeError("materialized file ceiling reached")

    return {
        "schema": "ghc.family.exact-final-owner-scoped-canonical.v1",
        "owner": "Auren Lark",
        "phase": "v672-v2",
        "state": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "exact_final": expected_head,
        "branch": BRANCH,
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "history": {
            "commits_from_source": commit_count,
            "merges_from_source": merge_count,
            "final_parent": EVIDENCE,
        },
        "equality": {
            "local": local,
            "upstream": upstream,
            "tracking": tracking,
            "fresh_live_remote": live,
            "divergence": "0/0",
            "clean": True,
        },
        "canonical_invocations": 1,
        "successful_invocations": 1,
        "replayed": False,
        "selected_test_runs": test_runs,
        "selected_tests_passed": sum(run["passed"] for run in test_runs),
        "strict_json_parses": len(json_paths),
        "manifest_replays": {
            "x1": x1_count,
            "x2_owner": x2_count,
            "immutable_evidence": evidence_count,
            "closeout": closeout_count,
            "mismatches": 0,
        },
        "privacy": {
            "files_scanned": privacy_files,
            "classes": 5,
            "confirmed_candidates": 0,
        },
        "security": {
            "changed_python_files": python_files,
            "bounded_ast_findings": 0,
        },
        "materialized_files": materialized_files,
        "complete_repository_suite": False,
        "same_owner_shared_infrastructure": True,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    root = Path(
        git(Path.cwd(), "rev-parse", "--show-toplevel").decode("utf-8").strip()
    )
    receipt_path = Path(args.receipt).resolve()
    try:
        payload = validate(root, args.expected_head, receipt_path)
    except Exception as exc:
        failed_path = receipt_path.with_name("canonical-failed-001.json")
        if not failed_path.exists() and not receipt_path.exists():
            failed_path.parent.mkdir(parents=True, exist_ok=True)
            message = str(exc).replace(str(root), "<owner-lane>")
            failed_path.write_text(
                json.dumps(
                    {
                        "schema": "ghc.family.exact-final-owner-scoped-canonical-failure.v1",
                        "owner": "Auren Lark",
                        "phase": "v672-v2",
                        "state": "FAILED_RETAINED_ZERO_SUCCESS_CREDIT",
                        "error_type": type(exc).__name__,
                        "error": message,
                        "canonical_success_credit": 0,
                        "aggregate_replay_permitted": False,
                        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
                    },
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
                newline="\n",
            )
        raise
    temporary = receipt_path.with_suffix(receipt_path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    temporary.replace(receipt_path)
    print(
        json.dumps(
            {
                "state": payload["state"],
                "selected_tests_passed": payload["selected_tests_passed"],
                "strict_json_parses": payload["strict_json_parses"],
                "manifest_mismatches": payload["manifest_replays"]["mismatches"],
                "privacy_candidates": payload["privacy"]["confirmed_candidates"],
                "security_findings": payload["security"]["bounded_ast_findings"],
                "replayed": payload["replayed"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
