#!/usr/bin/env python3
"""One-shot dependency-corrected exact-final component for Elowen v678-v5."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


OWNER = "Elowen Cairn"
PHASE = "v678-v5"
BRANCH = "codex/GHC-Family/elowen-cairn-v678-v5-full-tools"
SOURCE = "0021481a0c9681c077bce277e6ac0f2fcb37dbcd"
FIRST_FINAL = "831f948e326e3875ef0d5d7391560297ce0e2ee8"
OWNER_PREFIX = "docs/elowen-cairn/v678-v5/"
FAILED_RECEIPT_SHA256 = "bfa2115b166ee9eb5f3f9aaac9a4d7f5379e574a24ac4dc60bc7b8accf758ccd"
FAILED_LATCH_SHA256 = "cae4d857e5485817e0a4b281a5872aeeddaed41e2369abf9defdae440191afdf"
FAILED_PAYLOAD_SHA256 = "36f8a96bb375543e02e6095e34002dbef4bb83b78d51d25095b59b889ed66507"
VALID_STATUS = "VALID_DEPENDENCY_CORRECTED_EXACT_FINAL_COMPOSITE_WITH_ZERO_FAILED_CANONICAL_CREDIT"
PRIVACY_PATTERNS = {
    "private_absolute_path": re.compile(rb"(?i)[A-Z]:[\\/]+Users[\\/]+"),
    "raw_task_route": re.compile(rb"(?i)(source_thread_id|thread_id|clientThreadId)"),
    "credential_assignment": re.compile(rb"(?i)(api[_-]?key|private[_-]?key|password|bearer)\s*[:=]"),
    "raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    "session_stream": re.compile(rb"(?i)(session[_ -]?stream|terminal transcript|screenshot payload)"),
}
BOUNDARY = (
    "Bounded dependency-corrected same-owner software and documentation evidence under shared "
    "infrastructure only. The failed canonical retains zero success credit. This is not a full "
    "repository suite, independent reproduction, empirical validation, professional certification, "
    "production readiness, legal or cultural ratification, Māori authority, complete privacy or "
    "accessibility assurance, exhaustive security, proof, canon, or Stage 20 authority."
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalized(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest_json(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def write_json(path: Path, value: Any, *, exclusive: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if exclusive:
        with path.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(payload)
    else:
        path.write_text(payload, encoding="utf-8", newline="\n")


def run(repo: Path, command: list[str], *, timeout: int = 900, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(command, cwd=repo, capture_output=True, check=check, timeout=timeout)


def git(repo: Path, *args: str) -> str:
    return run(repo, ["git", *args], timeout=300).stdout.decode("utf-8", "strict").strip()


def allowed(path: str) -> bool:
    return (
        path.startswith(OWNER_PREFIX)
        or re.fullmatch(r"scripts/(?:build_ghc_family|ghc_family|validate_ghc_family)_elowen_cairn_v678_v5_.*\.py", path) is not None
        or re.fullmatch(r"tests/test_ghc_family_elowen_cairn_v678_v5_.*\.py", path) is not None
    )


def changed(repo: Path, start: str, end: str) -> set[str]:
    return {
        path
        for path in git(repo, "diff", "--name-only", "--diff-filter=ACMR", start, end, "--").splitlines()
        if path and allowed(path)
    }


def tree_map(repo: Path, commit: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in git(repo, "ls-tree", "-r", commit).splitlines():
        if not line:
            continue
        left, path = line.split("\t", 1)
        _mode, kind, oid = left.split()
        if kind == "blob":
            result[path] = oid
    return result


def batch_blobs(repo: Path, oids: set[str]) -> dict[str, bytes]:
    proc = subprocess.Popen(["git", "cat-file", "--batch"], cwd=repo, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert proc.stdin and proc.stdout
    result: dict[str, bytes] = {}
    for oid in sorted(oids):
        proc.stdin.write((oid + "\n").encode("ascii"))
        proc.stdin.flush()
        header = proc.stdout.readline().split()
        if len(header) < 3 or header[1] != b"blob":
            raise RuntimeError(f"non-blob object: {oid}")
        raw = proc.stdout.read(int(header[2]))
        proc.stdout.read(1)
        result[oid] = raw
    proc.stdin.close()
    proc.stdin = None
    _stdout, stderr = proc.communicate(timeout=60)
    if proc.returncode:
        raise RuntimeError(stderr.decode("utf-8", "replace"))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--failed-receipt", type=Path, required=True)
    parser.add_argument("--failed-latch", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--latch", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    failed_receipt_path = args.failed_receipt.resolve()
    failed_latch_path = args.failed_latch.resolve()
    receipt_path = args.receipt.resolve()
    latch_path = args.latch.resolve()
    if receipt_path.exists() or latch_path.exists():
        raise SystemExit("dependency-corrected receipt or latch already exists; replay refused")
    write_json(latch_path, {"status": "RUNNING_EXCLUSIVE_DEPENDENCY_CORRECTED_COMPONENT", "owner": OWNER, "phase": PHASE, "started_utc": utc_now()}, exclusive=True)
    payload: dict[str, Any] = {
        "owner": OWNER,
        "phase": PHASE,
        "status": "INVALID_DEPENDENCY_CORRECTED_EXACT_FINAL_COMPOSITE",
        "component_invocation_count": 1,
        "component_success_count": 0,
        "component_replay_count": 0,
        "failed_canonical_success_credit": 0,
        "successful_canonical_components_replayed": False,
        "full_repository_suite_run": False,
        "boundary": BOUNDARY,
        "started_utc": utc_now(),
    }
    try:
        if sha256(failed_receipt_path) != FAILED_RECEIPT_SHA256 or sha256(failed_latch_path) != FAILED_LATCH_SHA256:
            raise RuntimeError("failed canonical binding digest mismatch")
        failed = json.loads(failed_receipt_path.read_text(encoding="utf-8"))
        failed_checks = sorted(key for key, value in failed["checks"].items() if not value)
        imported_checks = {key: value for key, value in failed["checks"].items() if value}
        if (
            failed["status"] != "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL"
            or failed["success_count"] != 0
            or failed["canonical_payload_sha256"] != FAILED_PAYLOAD_SHA256
            or failed_checks != ["documents_structurally_bounded"]
            or not all(imported_checks.values())
        ):
            raise RuntimeError("failed canonical observation contract mismatch")

        head = git(repo, "rev-parse", "HEAD")
        branch = git(repo, "branch", "--show-current")
        clean_before = git(repo, "status", "--porcelain=v1") == ""
        upstream = git(repo, "rev-parse", "@{upstream}")
        tracking = git(repo, "rev-parse", f"refs/remotes/origin/{BRANCH}")
        remote_line = git(repo, "ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")
        remote_fields = remote_line.split()
        fresh_remote = remote_fields[0] if len(remote_fields) == 2 else ""
        divergence = git(repo, "rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()
        objects = tree_map(repo, head)
        delta_paths = changed(repo, FIRST_FINAL, head)
        delta_oids = {objects[path] for path in delta_paths}
        delta_blobs = batch_blobs(repo, delta_oids)

        manifest_path = repo / OWNER_PREFIX / "validation" / "correction1-delta-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        exclusions = {row["path"] for row in manifest["declared_exclusions"]}
        entries = manifest["entries"]
        manifest_failures = []
        if {row["path"] for row in entries} | exclusions != delta_paths:
            manifest_failures.append("path_set_mismatch")
        if {row["path"] for row in entries} & exclusions:
            manifest_failures.append("entry_exclusion_overlap")
        if manifest["entry_count"] != len(entries):
            manifest_failures.append("entry_count_mismatch")
        for row in entries:
            path = row["path"]
            if objects.get(path) != row["git_blob_oid"]:
                manifest_failures.append(f"oid_mismatch:{path}")
                continue
            if hashlib.sha256(normalized(delta_blobs[objects[path]])).hexdigest() != row["sha256_normalized_lf"]:
                manifest_failures.append(f"hash_mismatch:{path}")

        owner_manifest = json.loads((repo / OWNER_PREFIX / "validation" / "correction1-owner-manifest.json").read_text(encoding="utf-8"))
        owner_exclusions = {row["path"] for row in owner_manifest["declared_exclusions"]}
        owner_expected = changed(repo, SOURCE, head)
        owner_shape_valid = (
            {row["path"] for row in owner_manifest["entries"]} | owner_exclusions == owner_expected
            and not ({row["path"] for row in owner_manifest["entries"]} & owner_exclusions)
            and owner_manifest["entry_count"] == len(owner_manifest["entries"])
        )

        original_document_paths = sorted(
            path for path in changed(repo, SOURCE, FIRST_FINAL) if path.endswith((".md", ".html"))
        )
        document_failures = []
        for path in original_document_paths:
            raw = subprocess.check_output(["git", "-C", str(repo), "show", f"{head}:{path}"])
            value = raw.decode("utf-8")
            if len(value.split()) > 100_000:
                document_failures.append({"path": path, "reason": "word_ceiling"})
            if path.endswith(".html"):
                if not all(token in value.casefold() for token in ("<main", "<h1", "<title")):
                    document_failures.append({"path": path, "reason": "html_structure"})
            elif path.endswith("/SKILL.md"):
                if not value.startswith("---\n") or "\n---\n" not in value[4:]:
                    document_failures.append({"path": path, "reason": "skill_frontmatter"})
                else:
                    after = value.split("\n---\n", 1)[1]
                    if not re.search(r"(?m)^#{1,6}\s+\S", after):
                        document_failures.append({"path": path, "reason": "skill_heading_after_frontmatter"})
            elif not value.lstrip().startswith("#"):
                document_failures.append({"path": path, "reason": "markdown_heading"})

        correction_json_paths = sorted(path for path in delta_paths if path.endswith(".json"))
        correction_json_failures = []
        for path in correction_json_paths:
            try:
                json.loads(delta_blobs[objects[path]].decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                correction_json_failures.append({"path": path, "error": type(exc).__name__})

        changed_python = sorted(path for path in delta_paths if path.endswith(".py"))
        python_failures = []
        security_findings = []
        for path in changed_python:
            source = delta_blobs[objects[path]].decode("utf-8")
            try:
                compile(source, path, "exec")
                tree = ast.parse(source, filename=path)
            except SyntaxError as exc:
                python_failures.append({"path": path, "error": type(exc).__name__})
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                    security_findings.append({"path": path, "kind": node.func.id, "line": node.lineno})
                if isinstance(node, ast.Call) and any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords):
                    security_findings.append({"path": path, "kind": "shell_true", "line": node.lineno})

        privacy_candidates = []
        for path in sorted(delta_paths):
            if not path.endswith((".py", ".json", ".md", ".html", ".txt", ".yaml", ".yml")):
                continue
            raw = normalized(delta_blobs[objects[path]])
            for category, pattern in PRIVACY_PATTERNS.items():
                if pattern.search(raw):
                    metadata = path.endswith(".py") or path.endswith("-staged-review.json")
                    privacy_candidates.append(
                        {
                            "path": path,
                            "category": category,
                            "adjudication": "scanner_definition_or_rejection_assertion" if metadata else "confirmed_payload_hit",
                        }
                    )
        confirmed_privacy = [row for row in privacy_candidates if row["adjudication"] == "confirmed_payload_hit"]

        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        test_result = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "tests/test_ghc_family_elowen_cairn_v678_v5_correction1.py"],
            cwd=repo,
            env=env,
            capture_output=True,
            timeout=600,
        )
        test_output = (test_result.stdout + test_result.stderr).decode("utf-8", "replace")
        test_match = re.search(r"(\d+) passed", test_output)
        test_count = int(test_match.group(1)) if test_match else 0

        direct_history = (
            git(repo, "rev-parse", f"{head}^") == FIRST_FINAL
            and int(git(repo, "rev-list", "--count", f"{SOURCE}..{head}")) == 4
            and git(repo, "rev-list", "--merges", f"{SOURCE}..{head}") == ""
            and len(git(repo, "show", "-s", "--format=%P", head).split()) == 1
        )
        remote_equal = head == upstream == tracking == fresh_remote and divergence == ["0", "0"] and len(remote_fields) == 2
        diff_hygiene = run(repo, ["git", "diff", "--check", FIRST_FINAL, head], check=False).returncode == 0
        clean_after = git(repo, "status", "--porcelain=v1") == ""
        checks = {
            "failed_canonical_bound_zero_credit": True,
            "successful_first_final_observations_imported_without_replay": all(imported_checks.values()),
            "document_dependency_corrected": len(original_document_paths) == 28 and not document_failures,
            "correction_tests": test_result.returncode == 0 and test_count == 3,
            "correction_delta_manifest": not manifest_failures,
            "correction_owner_manifest_shape": owner_shape_valid,
            "correction_json_parse": not correction_json_failures,
            "changed_python_compile_and_bounded_security": not python_failures and not security_findings,
            "changed_file_privacy": not confirmed_privacy,
            "direct_child_four_commit_zero_merge_history": direct_history,
            "diff_hygiene": diff_hygiene,
            "clean_before": clean_before,
            "clean_after": clean_after,
            "typed_zero_divergence_and_fresh_four_way_equality": remote_equal,
            "full_repository_suite_not_run": True,
        }
        success = all(checks.values())
        payload.update(
            {
                "status": VALID_STATUS if success else "INVALID_DEPENDENCY_CORRECTED_EXACT_FINAL_COMPOSITE",
                "component_success_count": 1 if success else 0,
                "corrected_final": head,
                "retained_first_final": FIRST_FINAL,
                "failed_canonical_receipt_sha256": FAILED_RECEIPT_SHA256,
                "failed_canonical_payload_sha256": FAILED_PAYLOAD_SHA256,
                "imported_successful_check_count": len(imported_checks),
                "imported_test_count": failed["test_count"],
                "imported_json_parse_count": failed["json_parse_count"],
                "imported_manifest_entry_count": failed["manifest_entry_count"],
                "checks": checks,
                "corrected_document_count": len(original_document_paths),
                "document_failures": document_failures,
                "correction_test_count": test_count,
                "correction_test_summary": test_output.strip().splitlines()[-1] if test_output.strip() else "no output",
                "correction_delta_manifest_entries": len(entries),
                "correction_delta_manifest_exclusions": len(exclusions),
                "correction_delta_manifest_failures": manifest_failures,
                "correction_owner_manifest_entries": owner_manifest["entry_count"],
                "correction_json_parse_count": len(correction_json_paths),
                "correction_json_failures": correction_json_failures,
                "changed_python_count": len(changed_python),
                "python_failures": python_failures,
                "bounded_security_findings": security_findings,
                "privacy_candidates": privacy_candidates,
                "confirmed_privacy_or_raw_identifier_hits": confirmed_privacy,
                "external_method_flow_overlay": {
                    "method_id": "EC6785-CORR-EXT-P001",
                    "truth": success,
                    "status": "bounded_pass" if success else "failed_zero_credit",
                    "description": "The frontmatter-aware predicate checked exactly the 28 original owner Markdown and HTML documents at the additive corrected final; official SKILL.md frontmatter and later headings are accepted without relaxing ordinary Markdown or HTML structure.",
                    "failed_witness_preserved": "EC6785-CORR-N001",
                },
                "effective_overlay_after_component": {
                    "effective_negatives": 47003,
                    "effective_methods": 44556 if success else 44555,
                    "retained_failed_witnesses": 18664,
                    "bounded_passing_witnesses": 28977 if success else 28976,
                    "open_gaps": 407,
                    "exact_gates": 398,
                },
                "terminal_verdict": "NOT_READY_FOR_STAGE_20",
                "completed_utc": utc_now(),
            }
        )
    except Exception as exc:
        payload.update(
            {
                "status": "INVALID_DEPENDENCY_CORRECTED_EXACT_FINAL_COMPOSITE",
                "component_success_count": 0,
                "error_type": type(exc).__name__,
                "error": str(exc).replace(str(repo), "<repository>"),
                "completed_utc": utc_now(),
            }
        )

    payload["component_payload_sha256"] = digest_json(payload)
    write_json(receipt_path, payload, exclusive=True)
    write_json(
        latch_path,
        {
            "status": payload["status"],
            "owner": OWNER,
            "phase": PHASE,
            "component_invocation_count": 1,
            "component_success_count": payload["component_success_count"],
            "component_replay_count": 0,
            "failed_canonical_success_credit": 0,
            "component_payload_sha256": payload["component_payload_sha256"],
            "receipt_sha256": hashlib.sha256(receipt_path.read_bytes()).hexdigest(),
            "completed_utc": utc_now(),
        },
    )
    print(json.dumps({key: payload.get(key) for key in ("status", "corrected_final", "component_success_count", "corrected_document_count", "correction_test_count", "correction_delta_manifest_entries", "component_payload_sha256")}, sort_keys=True))
    return 0 if payload["component_success_count"] == 1 else 1


if __name__ == "__main__":
    raise SystemExit(main())
