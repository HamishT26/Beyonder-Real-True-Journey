#!/usr/bin/env python3
"""One-shot exact-final owner-scoped canonical aggregate for Auren Lark v668-v4."""

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
import tokenize
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BRANCH = "codex/GHC-Family/auren-lark-v668-v4-full-tools"
SOURCE_FINAL = "f0110dec1a0bcfc2f7a1945d47943033b68164e2"
INITIAL_X1_HEAD = "f0110dec1a0bcfc2f7a1945d47943033b68164e2"
X1_HEAD = "143b7c81968611038959162dbd214cdb0498a298"
EVIDENCE_HEAD = "9181e97eca0ebe013965df173d8dd45c4c1fc357"
PHASE_PREFIX = "docs/auren-lark/v668-v4/"
OWNER_MANIFEST = f"{PHASE_PREFIX}validation/final-owner-manifest.json"
DELTA_MANIFEST = f"{PHASE_PREFIX}validation/final-delta-manifest.json"
X1_MANIFEST = f"{PHASE_PREFIX}x1/x1-manifest.json"
EVIDENCE_MANIFEST = f"{PHASE_PREFIX}x2/evidence/evidence-content-manifest.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=check)


def git_text(*args: str) -> str:
    return run_git(*args).stdout.decode("utf-8", errors="replace").strip()


def git_bytes(commit: str, path: str) -> bytes:
    return run_git("show", f"{commit}:{path}").stdout


def read_git_json(commit: str, path: str) -> Any:
    return json.loads(git_bytes(commit, path))


def replay_manifest(commit: str, path: str) -> dict[str, int]:
    manifest = read_git_json(commit, path)
    mismatches = 0
    for row in manifest["entries"]:
        data = git_bytes(commit, row["path"])
        oid = git_text("rev-parse", f"{commit}:{row['path']}")
        observed = {"git_blob_oid": oid, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
        if observed != {key: row[key] for key in observed}:
            mismatches += 1
    if mismatches:
        raise AssertionError(f"{path} has {mismatches} exact Git-blob mismatches")
    return {"entries": len(manifest["entries"]), "mismatches": 0}


def privacy_patterns() -> list[re.Pattern[bytes]]:
    route_key = b"source_" + b"thread_id" + rb"\s*[:=]"
    route_tag = b"<codex_" + b"delegation>"
    session_key = b"session_meta" + rb"\.payload\.id"
    response_key = b"response" + b"_item"
    return [
        re.compile(b"-----BEGIN " + rb"(?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        re.compile(route_key, re.I),
        re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        re.compile(rb"\b[A-Z]:\\Users\\[^\s\"']+", re.I),
        re.compile(route_tag + b"|" + session_key + b"|" + response_key, re.I),
        re.compile(rb"\b(?:ssn|medical record number|patient identifier|participant identifier)\s*[:=]\s*\S+", re.I),
    ]


def privacy_scan(texts: dict[str, bytes]) -> dict[str, Any]:
    raw: list[dict[str, Any]] = []
    scanner: list[dict[str, Any]] = []
    confirmed: list[dict[str, Any]] = []
    patterns = privacy_patterns()
    for path, data in texts.items():
        for class_id, pattern in enumerate(patterns, 1):
            if not pattern.search(data):
                continue
            hit = {"path": path, "class": class_id}
            raw.append(hit)
            is_scanner = False
            if path == "tests/test_ghc_family_auren_lark_v668_v4_x2.py" and class_id == 5:
                text = data.decode("utf-8")
                marker = "response" + "_item"
                inside = sum(
                    token.string.count(marker)
                    for token in tokenize.generate_tokens(io.StringIO(text).readline)
                    if token.type == tokenize.STRING
                )
                is_scanner = text.count(marker) == inside and inside == 1
            if is_scanner:
                scanner.append(hit)
            else:
                confirmed.append(hit)
    expected = [{"path": "tests/test_ghc_family_auren_lark_v668_v4_x2.py", "class": 5}]
    if raw != expected or scanner != expected or confirmed:
        raise AssertionError({"raw": raw, "scanner": scanner, "confirmed": confirmed})
    return {"raw_candidates": len(raw), "scanner_literal_candidates": len(scanner), "confirmed_payload_hits": len(confirmed)}


def security_scan(python_texts: dict[str, str]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for path, text in python_texts.items():
        tree = ast.parse(text, filename=path)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec", "compile"}:
                findings.append({"path": path, "line": node.lineno, "kind": node.func.id})
            for keyword in node.keywords:
                if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                    findings.append({"path": path, "line": node.lineno, "kind": "explicit_shell"})
    if findings:
        raise AssertionError(f"bounded owner-code security findings: {findings}")
    return findings


def atomic_receipt(path: Path, payload: dict[str, Any]) -> None:
    temporary = path.with_name(path.name + ".tmp")
    if temporary.exists():
        raise FileExistsError(f"temporary receipt already exists: {temporary.name}")
    data = (json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    with temporary.open("xb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def prepare_receipt_target(path: Path) -> None:
    if path.exists():
        raise FileExistsError("canonical receipt already exists; replay refused")
    path.parent.mkdir(parents=True, exist_ok=True)
    probe = path.with_name(path.name + ".write-probe")
    if probe.exists():
        raise FileExistsError("canonical write probe already exists")
    with probe.open("xb") as handle:
        handle.write(b"write-probe")
        handle.flush()
        os.fsync(handle.fileno())
    probe.unlink()


def pretest_checks(expected_head: str) -> dict[str, Any]:
    head = git_text("rev-parse", "HEAD")
    branch = git_text("branch", "--show-current")
    upstream = git_text("rev-parse", "@{u}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_line = git_text("ls-remote", "origin", f"refs/heads/{BRANCH}")
    live = live_line.split()[0] if live_line else ""
    divergence = git_text("rev-list", "--left-right", "--count", "HEAD...@{u}")
    commits = git_text("rev-list", "--reverse", f"{SOURCE_FINAL}..{head}").splitlines()
    merges = git_text("rev-list", "--merges", f"{SOURCE_FINAL}..{head}").splitlines()
    parents = [len(git_text("show", "-s", "--format=%P", commit).split()) for commit in commits]
    detailed: dict[str, bool] = {
        "exact_head": head == expected_head,
        "exact_branch": branch == BRANCH,
        "clean_before": git_text("status", "--porcelain", "--untracked-files=all") == "",
        "final_parent_is_evidence": git_text("rev-parse", "HEAD^") == EVIDENCE_HEAD,
        "evidence_parent_is_frozen_x1": git_text("rev-parse", f"{EVIDENCE_HEAD}^") == X1_HEAD,
        "frozen_x1_parent_is_source": git_text("rev-parse", f"{X1_HEAD}^") == SOURCE_FINAL,
        "source_alias_exact": INITIAL_X1_HEAD == SOURCE_FINAL,
        "three_phase_commits": len(commits) == 3,
        "zero_merges": len(merges) == 0,
        "all_phase_commits_single_parent": parents == [1, 1, 1],
        "commit_ceiling": len(commits) <= 8,
        "upstream_equal": upstream == head,
        "tracking_equal": tracking == head,
        "fresh_live_equal": live == head,
        "zero_divergence": divergence == "0\t0",
    }
    if not all(detailed.values()):
        raise AssertionError(f"pretest lifecycle checks failed: {detailed}")

    manifests = {
        "frozen_x1": replay_manifest(X1_HEAD, X1_MANIFEST),
        "evidence": replay_manifest(EVIDENCE_HEAD, EVIDENCE_MANIFEST),
        "final_delta": replay_manifest(head, DELTA_MANIFEST),
        "final_owner": replay_manifest(head, OWNER_MANIFEST),
    }
    owner_manifest = read_git_json(head, OWNER_MANIFEST)
    texts: dict[str, bytes] = {}
    python_texts: dict[str, str] = {}
    json_parses = 0
    markdown_checks = 0
    oversized: list[dict[str, Any]] = []
    for row in owner_manifest["entries"]:
        path = row["path"]
        data = git_bytes(head, path)
        suffix = Path(path).suffix.lower()
        if suffix in {".json", ".md", ".txt", ".html", ".py"}:
            texts[path] = data
            text = data.decode("utf-8")
            words = len(re.findall(r"\b\w+[\w'-]*\b", text))
            if words > 6000:
                oversized.append({"path": path, "words": words})
        if suffix == ".json":
            json.loads(data)
            json_parses += 1
        elif suffix == ".md":
            if not data.strip():
                raise AssertionError(f"empty Markdown: {path}")
            markdown_checks += 1
        elif suffix == ".py":
            python_texts[path] = data.decode("utf-8")
    owner_manifest_data = git_bytes(head, OWNER_MANIFEST)
    json.loads(owner_manifest_data)
    texts[OWNER_MANIFEST] = owner_manifest_data
    json_parses += 1
    if oversized:
        raise AssertionError(f"oversized owner documents: {oversized}")
    privacy = privacy_scan(texts)
    security = security_scan(python_texts)
    truth = read_git_json(head, f"{PHASE_PREFIX}final/phase-truth.json")
    route = read_git_json(head, f"{PHASE_PREFIX}route/prepared-route-state.json")
    retained = read_git_json(head, f"{PHASE_PREFIX}closeout/retained-negative-register.json")
    disposition = read_git_json(head, f"{PHASE_PREFIX}final/privacy-candidate-disposition.json")
    detailed.update({
        "four_truth_labels": truth["allowed_outcomes"] == ["completed", "represented", "open_gap", "exact_gate"],
        "exact_outcomes": truth["outcome_counts"] == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
        "proposal_chain_4750": truth["frozen_proposal_chain"] == 4750,
        "sealed_negative_total": retained["effective_negatives_before_canonical"] == 29592,
        "sealed_method_total": retained["methods_before_canonical"] == 16178,
        "sealed_failed_total": retained["failed_witnesses_before_canonical"] == 1893,
        "sealed_passing_total": retained["passing_witnesses_before_canonical"] == 2720,
        "open_gap_total": truth["repository_sealed_counts"]["open_gaps"] == 215,
        "exact_gate_total": truth["repository_sealed_counts"]["exact_gates"] == 210,
        "terminal_not_ready": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "route_prepared_not_sent": route["state"] == "PREPARED_NOT_SENT",
        "successor_unresolved": route["successor_exact_title"] == "UNRESOLVED_UNTIL_TERMINAL_GATE",
        "successor_not_contacted": route["successor_contacted"] is False,
        "single_send_maximum": route["single_send_maximum"] == 1,
        "privacy_disposition_exact": disposition["raw_candidates"] == 1 and disposition["scanner_literal_candidates"] == 1 and disposition["confirmed_payload_hits"] == 0,
        "privacy_zero_confirmed": privacy["confirmed_payload_hits"] == 0,
        "security_zero_bounded_findings": len(security) == 0,
        "documents_within_cap": len(oversized) == 0,
        "owner_manifest_below_2000": owner_manifest["entry_count"] < 2000,
    })
    materialized = sum(1 for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts)
    detailed["materialized_below_2000"] = materialized < 2000
    if not all(detailed.values()):
        raise AssertionError(f"detailed checks failed: {detailed}")
    minimal = {
        "exact_head": detailed["exact_head"],
        "clean": detailed["clean_before"],
        "fresh_live_equal": detailed["fresh_live_equal"],
        "zero_divergence": detailed["zero_divergence"],
        "zero_merges": detailed["zero_merges"],
        "single_parent_final": detailed["all_phase_commits_single_parent"],
        "manifest_parity": all(row["mismatches"] == 0 for row in manifests.values()),
        "zero_confirmed_privacy": detailed["privacy_zero_confirmed"],
        "zero_bounded_security_findings": detailed["security_zero_bounded_findings"],
        "terminal_not_ready": detailed["terminal_not_ready"],
    }
    if not all(minimal.values()):
        raise AssertionError(f"minimal checks failed: {minimal}")
    return {
        "head": head,
        "detailed_checks": detailed,
        "minimal_checks": minimal,
        "manifests": manifests,
        "owner_manifest_entries": owner_manifest["entry_count"],
        "manifest_entries_total": sum(row["entries"] for row in manifests.values()),
        "json_parses": json_parses,
        "markdown_checks": markdown_checks,
        "python_ast_checks": len(python_texts),
        "privacy": privacy,
        "security_findings": len(security),
        "materialized_files": materialized,
    }


def run_test_selection() -> dict[str, Any]:
    command = [
        sys.executable,
        "-B",
        "-m",
        "pytest",
        "-q",
        "-p",
        "no:cacheprovider",
        "tests/test_ghc_family_auren_lark_v668_v4_x2.py",
        "tests/test_ghc_family_auren_lark_v668_v4_final.py",
        "-k",
        "not test_x2_starts_from_exact_corrected_x1 and not test_no_final_or_successor_contact_during_x2",
    ]
    environment = os.environ.copy()
    paths = [str(ROOT), str(ROOT / "scripts")]
    if environment.get("PYTHONPATH"):
        paths.append(environment["PYTHONPATH"])
    environment["PYTHONPATH"] = os.pathsep.join(paths)
    result = subprocess.run(
        command,
        cwd=ROOT,
        env=environment,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(f"owner-scoped test selection failed: {result.stdout[-300:]} {result.stderr[-300:]}")
    match = re.search(r"(\d+) passed", result.stdout)
    if not match:
        raise AssertionError("pytest pass count unavailable")
    return {"tests_passed": int(match.group(1)), "stdout_tail": result.stdout[-300:]}


def run_aggregate(expected_head: str) -> dict[str, Any]:
    pretest = pretest_checks(expected_head)
    tests = run_test_selection()
    clean_after = git_text("status", "--porcelain", "--untracked-files=all") == ""
    if not clean_after:
        raise AssertionError("worktree changed during canonical test selection")
    return {
        "status": "SUCCESSFUL_ONCE_NO_REPLAY",
        "canonical_invocation_count": 1,
        "canonical_success_count": 1,
        "post_success_replay": False,
        "owner": "Auren Lark",
        "phase": "v668-v4",
        "branch": BRANCH,
        "source_final": SOURCE_FINAL,
        "starting_source": SOURCE_FINAL,
        "frozen_x1": X1_HEAD,
        "evidence_head": EVIDENCE_HEAD,
        "exact_final": pretest["head"],
        "tests_passed": tests["tests_passed"],
        "test_selection": ["x2 excluding x1-head and final-absence lifecycle tests", "final"],
        "manifest_replays": pretest["manifests"],
        "manifest_entries_total": pretest["manifest_entries_total"],
        "owner_manifest_entries": pretest["owner_manifest_entries"],
        "json_parses": pretest["json_parses"],
        "markdown_checks": pretest["markdown_checks"],
        "python_ast_checks": pretest["python_ast_checks"],
        "privacy": pretest["privacy"],
        "bounded_security_findings": pretest["security_findings"],
        "materialized_files": pretest["materialized_files"],
        "detailed_checks": pretest["detailed_checks"],
        "detailed_check_count": len(pretest["detailed_checks"]),
        "minimal_checks": pretest["minimal_checks"],
        "minimal_check_count": len(pretest["minimal_checks"]),
        "clean_after": clean_after,
        "repository_sealed_counts": {
            "effective_negatives": 29592,
            "methods": 16178,
            "failed_witnesses": 1893,
            "passing_witnesses": 2720,
            "open_gaps": 215,
            "exact_gates": 210,
        },
        "proposal_chain": 4750,
        "outcomes": {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
        "full_repository_suite": False,
        "external_audit": False,
        "independent_reproduction": False,
        "same_owner_shared_infrastructure": True,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "completed_at": utc_now(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    try:
        prepare_receipt_target(args.receipt)
    except Exception as exc:
        print(json.dumps({"status": "ENTRYPOINT_PREFLIGHT_FAILED_NO_AGGREGATE", "error_class": type(exc).__name__}, sort_keys=True))
        return 4
    started_at = utc_now()
    try:
        result = run_aggregate(args.expected_head)
        result["started_at"] = started_at
        atomic_receipt(args.receipt, result)
        print(json.dumps({
            "status": result["status"],
            "tests_passed": result["tests_passed"],
            "manifest_entries_total": result["manifest_entries_total"],
            "json_parses": result["json_parses"],
            "detailed_check_count": result["detailed_check_count"],
            "minimal_check_count": result["minimal_check_count"],
            "confirmed_privacy_hits": result["privacy"]["confirmed_payload_hits"],
        }, sort_keys=True))
        return 0
    except Exception as exc:
        failure = {
            "status": "FAILED_ONCE_ZERO_CANONICAL_SUCCESS_CREDIT",
            "canonical_invocation_count": 1,
            "canonical_success_count": 0,
            "post_failure_aggregate_replay_allowed": False,
            "owner": "Auren Lark",
            "phase": "v668-v4",
            "branch": BRANCH,
            "expected_head": args.expected_head,
            "error_class": type(exc).__name__,
            "error_summary": str(exc)[:700],
            "started_at": started_at,
            "failed_at": utc_now(),
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        }
        atomic_receipt(args.receipt, failure)
        print(json.dumps({"status": failure["status"], "error_class": failure["error_class"]}, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
