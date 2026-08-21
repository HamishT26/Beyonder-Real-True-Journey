#!/usr/bin/env python3
"""One-shot exact-final canonical validator for Caelen Ash v664-v8."""

from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE_FINAL = "682666c064b14f09def75fb46f3bafb0e987a7a2"
X1_HEAD = "0832a8260dec6c5d776a6b22f6cf9b2c9e81d705"
EVIDENCE_HEAD = "970a13c1a2ac2ef411f6d8199877d356a77d693c"
FIRST_FINAL = "915c260845229bd31f433ff24a59290c95e21b1e"
BRANCH = "codex/GHC-Family/caelen-ash-v664-v8-full-tools"
PREFIX = "docs/caelen-ash/v664-v8/"
OWNER_MANIFEST = f"{PREFIX}validation/correction-owner-manifest.json"
DELTA_MANIFEST = f"{PREFIX}validation/correction-delta-manifest.json"
PHASE_TRUTH = f"{PREFIX}correction/phase-truth.json"
OUTCOME_LEDGER = f"{PREFIX}x2/outcome-ledger.json"
EXPECTED_OUTCOMES = {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}
TEST_MODULES = [
    "tests.test_ghc_family_caelen_v664_v8_x1",
    "tests.test_ghc_family_caelen_v664_v8_x2",
    "tests.test_ghc_family_caelen_v664_v8_closeout",
    "tests.test_ghc_family_caelen_v664_v8_terminal_correction",
]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


class CanonicalError(RuntimeError):
    """Raised when an exact-final invariant fails."""


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
    )
    if check and result.returncode:
        raise CanonicalError(
            f"git {' '.join(args)} failed ({result.returncode}): "
            f"{result.stderr.decode('utf-8', 'replace').strip()}"
        )
    return result


def strict_json(raw: bytes | str, label: str) -> Any:
    text = raw.decode("utf-8") if isinstance(raw, bytes) else raw

    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in pairs:
            if key in value:
                raise CanonicalError(f"duplicate JSON key in {label}: {key}")
            value[key] = item
        return value

    try:
        return json.loads(text, object_pairs_hook=reject_duplicates)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CanonicalError(f"strict JSON failed for {label}: {exc}") from exc


def git_blob(head: str, path: str) -> bytes:
    return run_git("show", f"{head}:{path}").stdout


def git_json(head: str, path: str) -> dict[str, Any]:
    value = strict_json(git_blob(head, path), path)
    if not isinstance(value, dict):
        raise CanonicalError(f"JSON root is not an object: {path}")
    return value


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def equality_snapshot(expected_head: str) -> dict[str, Any]:
    local = run_git("rev-parse", "HEAD").stdout.decode().strip()
    upstream = run_git("rev-parse", "@{u}").stdout.decode().strip()
    tracking = run_git("rev-parse", f"refs/remotes/origin/{BRANCH}").stdout.decode().strip()
    live_rows = run_git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}").stdout.decode().split()
    live = live_rows[0] if live_rows else ""
    divergence = run_git("rev-list", "--left-right", "--count", "HEAD...@{u}").stdout.decode().split()
    clean = not run_git("status", "--porcelain=v1").stdout
    result = {
        "local": local,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live": live,
        "ahead": int(divergence[0]),
        "behind": int(divergence[1]),
        "clean": clean,
    }
    result["valid"] = (
        local == expected_head
        and local == upstream == tracking == live
        and result["ahead"] == 0
        and result["behind"] == 0
        and clean
    )
    return result


def replay_manifest(head: str, path: str) -> dict[str, Any]:
    manifest = git_json(head, path)
    mismatches = []
    for entry in manifest["entries"]:
        raw = git_blob(head, entry["path"])
        object_id = run_git("rev-parse", f"{head}:{entry['path']}").stdout.decode().strip()
        if (
            sha256(raw) != entry["sha256"]
            or len(raw) != entry["size"]
            or object_id != entry["git_blob"]
        ):
            mismatches.append(entry["path"])
    return {
        "path": path,
        "intended_path_count": manifest["intended_path_count"],
        "entry_count": len(manifest["entries"]),
        "exclusion_count": len(manifest["declared_self_exclusions"]),
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "coverage_valid": manifest["coverage_valid"],
        "valid": manifest["coverage_valid"] and not mismatches,
        "manifest": manifest,
    }


def run_tests() -> dict[str, Any]:
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromNames(TEST_MODULES)
    count = suite.countTestCases()
    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)
    result = runner.run(suite)
    output = stream.getvalue()
    return {
        "module_count": len(TEST_MODULES),
        "test_count": count,
        "tests_run": result.testsRun,
        "failure_count": len(result.failures),
        "error_count": len(result.errors),
        "skipped_count": len(result.skipped),
        "output_sha256": sha256(output.encode("utf-8")),
        "successful": result.wasSuccessful() and count == 117 and result.testsRun == 117,
    }


def scan_text(path: str, text: str) -> list[dict[str, str]]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(
            r"(?i)\b" + r"[0-9a-f]{8}" + r"(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b"
        ),
        "private_absolute_local_path": re.compile(r"(?i)\b[a-z]:[\\/](?:users|ghc-archives)[\\/]"),
        "credential_or_secret_assignment": re.compile(
            r"(?i)(?:api[_-]?key|password|private[_-]?key|access[_-]?token)\s*[:=]\s*['\"][^'\"]+"
        ),
        "private_route_value": re.compile(r"(?i)(?:resume[_ -]?value|raw[_ -]?route[_ -]?key)\s*[:=]\s*\S+"),
        "transcript_or_session_payload": re.compile(r"(?i)(?:conversation[_ -]?export|session[_ -]?stream[_ -]?payload)\s*[:=]\s*\S+"),
    }
    hits = []
    for class_name, pattern in patterns.items():
        for match in pattern.finditer(text):
            hits.append(
                {
                    "path": path,
                    "class": class_name,
                    "excerpt_sha256": sha256(match.group(0).encode("utf-8")),
                }
            )
    return hits


def inspect_owner_surface(head: str, owner_manifest: dict[str, Any]) -> dict[str, Any]:
    paths = [
        entry["path"] for entry in owner_manifest["entries"]
    ] + owner_manifest["declared_self_exclusions"]
    paths = sorted(set(paths))
    json_count = 0
    markdown_count = 0
    html_count = 0
    python_count = 0
    word_count = 0
    privacy_hits: list[dict[str, str]] = []
    security_findings: list[dict[str, str]] = []
    markdown_issues: list[str] = []
    html_issues: list[str] = []
    for path in paths:
        raw = git_blob(head, path)
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise CanonicalError(f"non-UTF-8 owner file: {path}: {exc}") from exc
        privacy_hits.extend(scan_text(path, text))
        if path.endswith(".json"):
            strict_json(raw, path)
            json_count += 1
        if path.endswith(".md"):
            if not (text.startswith("# ") or text.startswith("---\n")):
                markdown_issues.append(f"{path}: missing H1 or skill frontmatter")
            if any(line.rstrip() != line for line in text.splitlines()):
                markdown_issues.append(f"{path}: trailing whitespace")
            markdown_count += 1
        if path.endswith(".html"):
            for token in ("<html lang=", "<main", "<h1", "<h2", "NOT_READY_FOR_STAGE_20"):
                if token not in text:
                    html_issues.append(f"{path}: missing {token}")
            html_count += 1
        if path.endswith(".py"):
            compile(text, path, "exec")
            tree = ast.parse(text, filename=path)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                        security_findings.append({"path": path, "finding": f"dangerous built-in {node.func.id}"})
                    if (
                        isinstance(node.func, ast.Attribute)
                        and isinstance(node.func.value, ast.Name)
                        and node.func.value.id == "os"
                        and node.func.attr == "system"
                    ):
                        security_findings.append({"path": path, "finding": "os.system"})
                    if any(
                        keyword.arg == "shell"
                        and isinstance(keyword.value, ast.Constant)
                        and keyword.value.value is True
                        for keyword in node.keywords
                    ):
                        security_findings.append({"path": path, "finding": "shell=True"})
            python_count += 1
        if Path(path).suffix.lower() in {".json", ".md", ".html", ".txt"}:
            word_count += len(re.findall(r"\S+", text))
    return {
        "owner_path_count": len(paths),
        "strict_json_count": json_count,
        "markdown_check_count": markdown_count,
        "markdown_issue_count": len(markdown_issues),
        "markdown_issues": markdown_issues,
        "html_check_count": html_count,
        "html_issue_count": len(html_issues),
        "html_issues": html_issues,
        "python_compile_count": python_count,
        "privacy_candidate_count": len(privacy_hits),
        "privacy_confirmed_hit_count": len(privacy_hits),
        "privacy_hits": privacy_hits,
        "bounded_security_finding_count": len(security_findings),
        "bounded_security_findings": security_findings,
        "document_word_count": word_count,
        "owner_file_ceiling": 2_000,
        "document_word_ceiling": 100_000,
        "valid": (
            len(paths) < 2_000
            and word_count <= 100_000
            and not markdown_issues
            and not html_issues
            and not privacy_hits
            and not security_findings
        ),
    }


def ancestry(head: str) -> dict[str, Any]:
    x1_parent = run_git("rev-parse", f"{X1_HEAD}^").stdout.decode().strip()
    evidence_parent = run_git("rev-parse", f"{EVIDENCE_HEAD}^").stdout.decode().strip()
    first_final_parent = run_git("rev-parse", f"{FIRST_FINAL}^").stdout.decode().strip()
    final_parent = run_git("rev-parse", f"{head}^").stdout.decode().strip()
    phase_commits = int(run_git("rev-list", "--count", f"{SOURCE_FINAL}..{head}").stdout)
    merges = int(run_git("rev-list", "--count", "--merges", f"{SOURCE_FINAL}..{head}").stdout)
    final_parent_count = len(run_git("show", "-s", "--format=%P", head).stdout.decode().split())
    return {
        "x1_parent": x1_parent,
        "evidence_parent": evidence_parent,
        "first_final_parent": first_final_parent,
        "final_parent": final_parent,
        "phase_commit_count": phase_commits,
        "merge_count": merges,
        "final_parent_count": final_parent_count,
        "valid": (
            x1_parent == SOURCE_FINAL
            and evidence_parent == X1_HEAD
            and first_final_parent == EVIDENCE_HEAD
            and final_parent == FIRST_FINAL
            and phase_commits == 4
            and merges == 0
            and final_parent_count == 1
        ),
    }


def validate(expected_head: str) -> dict[str, Any]:
    before = equality_snapshot(expected_head)
    owner = replay_manifest(expected_head, OWNER_MANIFEST)
    delta = replay_manifest(expected_head, DELTA_MANIFEST)
    surface = inspect_owner_surface(expected_head, owner["manifest"])
    tests = run_tests()
    history = ancestry(expected_head)
    truth = git_json(expected_head, PHASE_TRUTH)
    outcomes = git_json(expected_head, OUTCOME_LEDGER)
    truth_valid = (
        truth["core_outcomes"] == EXPECTED_OUTCOMES
        and truth["effective_negatives"] == 25_071
        and truth["effective_methods"] == 9_003
        and truth["effective_open_gaps"] == 174
        and truth["effective_exact_gates"] == 172
        and truth["frozen_proposal_total"] == 4_010
        and truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
        and outcomes["counts"] == EXPECTED_OUTCOMES
        and outcomes["unknown_outcome_count"] == 0
    )
    route = git_json(expected_head, f"{PREFIX}orchestration/terminal-route-state-correction.json")
    route_valid = (
        route["state"] == "PREPARED_NOT_SENT"
        and route["target_exact_title"] == "Orin Thale"
        and route["send_count"] == 0
        and route["tavian_sol"] == "ON_STANDBY"
    )
    diff_check = run_git("diff", "--check", f"{SOURCE_FINAL}..{expected_head}", check=False)
    after = equality_snapshot(expected_head)
    valid = all(
        (
            before["valid"],
            owner["valid"],
            delta["valid"],
            surface["valid"],
            tests["successful"],
            history["valid"],
            truth_valid,
            route_valid,
            diff_check.returncode == 0,
            after["valid"],
        )
    )
    return {
        "schema": "ghc.family.caelen.v664-v8.exclusive-canonical-receipt.v2",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "owner": "Caelen Ash",
        "phase": "v664-v8",
        "branch": BRANCH,
        "exact_final": expected_head,
        "source_final": SOURCE_FINAL,
        "x1_head": X1_HEAD,
        "evidence_head": EVIDENCE_HEAD,
        "first_final": FIRST_FINAL,
        "pre_validation_equality": before,
        "tests": tests,
        "owner_manifest": {key: value for key, value in owner.items() if key != "manifest"},
        "delta_manifest": {key: value for key, value in delta.items() if key != "manifest"},
        "owner_surface": surface,
        "ancestry": history,
        "truth_checks": {"valid": truth_valid, "core_outcomes": truth["core_outcomes"], "effective_negatives": truth["effective_negatives"], "effective_methods": truth["effective_methods"], "open_gaps": truth["effective_open_gaps"], "exact_gates": truth["effective_exact_gates"], "frozen_proposals": truth["frozen_proposal_total"], "terminal_verdict": truth["terminal_verdict"]},
        "route_checks": {"valid": route_valid, "state": route["state"], "target_exact_title": route["target_exact_title"], "send_count": route["send_count"]},
        "diff_hygiene_issue_count": 0 if diff_check.returncode == 0 else 1,
        "post_validation_equality": after,
        "full_repository_suite": False,
        "same_owner_validation": True,
        "independent_team_reproduction": False,
        "success": valid,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--receipt-out", required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"[0-9a-f]{40}", args.expected_head):
        raise SystemExit("expected head must be a lowercase forty-character Git hash")
    receipt_path = Path(args.receipt_out)
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    if receipt_path.exists():
        raise SystemExit("exclusive receipt path already exists; canonical replay refused")
    try:
        receipt = validate(args.expected_head)
    except Exception as exc:
        receipt = {
            "schema": "ghc.family.caelen.v664-v8.exclusive-canonical-receipt.v2",
            "recorded_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "owner": "Caelen Ash",
            "phase": "v664-v8",
            "exact_final": args.expected_head,
            "success": False,
            "failure_type": type(exc).__name__,
            "failure_message": str(exc),
        }
    with receipt_path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(receipt, handle, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        handle.write("\n")
    print(
        json.dumps(
            {
                "success": receipt.get("success", False),
                "exact_final": args.expected_head,
                "receipt_sha256": sha256(receipt_path.read_bytes()),
                "test_count": receipt.get("tests", {}).get("test_count", 0),
                "owner_paths": receipt.get("owner_surface", {}).get("owner_path_count", 0),
                "strict_json": receipt.get("owner_surface", {}).get("strict_json_count", 0),
                "privacy_confirmed_hits": receipt.get("owner_surface", {}).get("privacy_confirmed_hit_count", 0),
            },
            sort_keys=True,
        )
    )
    return 0 if receipt.get("success", False) else 1


if __name__ == "__main__":
    raise SystemExit(main())
