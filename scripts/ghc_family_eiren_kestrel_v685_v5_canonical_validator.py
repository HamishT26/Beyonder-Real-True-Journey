#!/usr/bin/env python3
"""One-shot exact-final owner-scoped canonical validator for Eiren v685-v5."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = "87a74f84afaa197f8c388767a2ed536bbb853aba"
X1 = "167e626c0684ac9ac1cd2d2184a831e1456f43b9"
EVIDENCE = "871d70712c827acd4c5b49ffe90c8735056a9c53"
BRANCH = "codex/GHC-Family/eiren-kestrel-v685-v5-full-tools"
BASE = "docs/eiren-kestrel/v685-v5"


def run(args: list[str], *, input_bytes: bytes | None = None) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(args, cwd=ROOT, input=input_bytes, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def git(*args: str, check: bool = True) -> bytes:
    proc = run(["git", *args])
    if check and proc.returncode:
        raise RuntimeError(proc.stderr.decode("utf-8", "replace"))
    return proc.stdout


def git_text(*args: str) -> str:
    return git(*args).decode("utf-8", "replace").strip()


def show(commit: str, path: str) -> bytes:
    return git("show", f"{commit}:{path}")


def load(commit: str, path: str) -> Any:
    return json.loads(show(commit, path).decode("utf-8"))


def owner_path(path: str) -> bool:
    return path.startswith(f"{BASE}/") or path.startswith("scripts/ghc_family_astronomy_") or "eiren_kestrel_v685_v5" in path


def replay_manifest(commit: str, path: str) -> dict[str, Any]:
    manifest = load(commit, path)
    failures = []
    for entry in manifest["entries"]:
        data = show(commit, entry["path"])
        if len(data) != entry["bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
            failures.append(entry["path"])
    return {"path": path, "entry_count": manifest["entry_count"], "failure_count": len(failures), "failures": failures, "valid": not failures}


def privacy_scan(commit: str, paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(rb"\b019[a-f0-9]{29,}\b", re.I),
        "private_absolute_path": re.compile(rb"(?:[A-Za-z]:\\Users\\|D:\\GHC-Archives\\)", re.I),
        "credential_or_private_key": re.compile(rb"(?:sk-[A-Za-z0-9_-]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)"),
        "private_callable_identifier": re.compile(rb"\b(?:source_thread_id|providerTabId|clientThreadId)\b"),
        "private_session_or_route": re.compile(rb"(?:codex://|app://|session[_ -]?stream)", re.I),
    }
    definitions = {p for p in paths if p.endswith(("_x1.py", "_x2.py", "_final.py", "_canonical_validator.py"))}
    candidates, confirmed = [], []
    for path in paths:
        if not path.endswith((".py", ".json", ".md", ".html", ".yaml", ".yml", ".txt")):
            continue
        data = show(commit, path)
        for class_name, pattern in patterns.items():
            matches = pattern.findall(data)
            if not matches:
                continue
            digest_values = set()
            if class_name == "raw_task_or_thread_identifier" and path.endswith("/x2/rejecting-mutations.json"):
                try:
                    digest_values = {row["fixture_sha256"] for row in json.loads(data.decode("utf-8"))["mutations"]}
                except (KeyError, TypeError, UnicodeDecodeError, json.JSONDecodeError):
                    digest_values = set()
            digest_only = bool(digest_values) and all(match.decode("ascii").lower() in digest_values for match in matches)
            prohibition_only = class_name == "private_session_or_route" and path.endswith("/handoffs/future-sibling-01-v685-v6-activation-candidate.md") and b"Keep raw task identifiers, private callable routes, credentials, private paths, transcripts, screenshots, session streams" in data
            adjudication = "scanner_definition_not_payload" if path in definitions else "sha256_digest_not_identifier" if digest_only else "explicit_prohibition_vocabulary_not_payload" if prohibition_only else "confirmed_payload_hit"
            item = {"path": path, "class": class_name, "match_count": len(matches), "adjudication": adjudication}
            candidates.append(item)
            if adjudication == "confirmed_payload_hit":
                confirmed.append(item)
    return {"scanned_file_count": len(paths), "candidate_count": len(candidates), "candidates": candidates, "confirmed_hit_count": len(confirmed), "confirmed_hits": confirmed, "valid": not confirmed}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    receipt = args.receipt.resolve()
    if receipt.exists():
        raise SystemExit("canonical receipt already exists; replay refused")
    head_before = git_text("rev-parse", "HEAD")
    branch = git_text("branch", "--show-current")
    clean_before = not git_text("status", "--porcelain", "--untracked-files=all")
    fetch = run(["git", "fetch", "origin", BRANCH])
    checks: dict[str, bool] = {
        "branch_exact": branch == BRANCH,
        "clean_before": clean_before,
        "head_parent_evidence": git_text("show", "-s", "--format=%P", head_before) == EVIDENCE,
        "evidence_parent_x1": git_text("show", "-s", "--format=%P", EVIDENCE) == X1,
        "x1_parent_source": git_text("show", "-s", "--format=%P", X1) == SOURCE,
        "three_phase_commits": len(git_text("rev-list", "--reverse", f"{SOURCE}..{head_before}").splitlines()) == 3,
        "zero_merges": not git_text("rev-list", "--merges", f"{SOURCE}..{head_before}"),
        "fetch_pass": fetch.returncode == 0,
    }
    local = head_before
    upstream = git_text("rev-parse", "@{upstream}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{BRANCH}")
    remote_rows = git_text("ls-remote", "origin", f"refs/heads/{BRANCH}").split()
    fresh_live = remote_rows[0] if remote_rows else ""
    divergence = git_text("rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()
    checks.update({
        "local_upstream_equal": local == upstream,
        "local_tracking_equal": local == tracking,
        "local_fresh_live_equal": local == fresh_live,
        "zero_divergence": divergence == ["0", "0"],
    })
    final_test = run([sys.executable, "-m", "unittest", "tests.test_ghc_family_eiren_kestrel_v685_v5_final", "-v"])
    checks["final_tests_pass"] = final_test.returncode == 0
    paths = [p for p in git_text("ls-tree", "-r", "--name-only", head_before).splitlines() if owner_path(p)]
    json_failures, markdown_failures, python_findings = [], [], []
    json_count = markdown_count = 0
    for path in paths:
        data = show(head_before, path)
        if path.endswith(".json"):
            json_count += 1
            try:
                json.loads(data.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                json_failures.append({"path": path, "error": str(exc)})
        if path.endswith(".md"):
            markdown_count += 1
            try:
                text = data.decode("utf-8")
                words = len(re.findall(r"\S+", text))
                if words > 100000:
                    markdown_failures.append({"path": path, "words": words, "error": "word_cap"})
                if path.endswith("future-sibling-01-v685-v6-activation-candidate.md") and words < 10000:
                    markdown_failures.append({"path": path, "words": words, "error": "baton_floor"})
                if path.endswith("final-integrated-overview.md") and words < 1800:
                    markdown_failures.append({"path": path, "words": words, "error": "overview_floor"})
            except UnicodeDecodeError as exc:
                markdown_failures.append({"path": path, "error": str(exc)})
        if path.endswith(".py"):
            try:
                ast.parse(data.decode("utf-8"), filename=path)
            except (UnicodeDecodeError, SyntaxError) as exc:
                python_findings.append({"path": path, "error": str(exc)})
    checks.update({"json_parse_pass": not json_failures, "document_checks_pass": not markdown_failures, "python_review_pass": not python_findings})
    manifests = [
        replay_manifest(X1, f"{BASE}/validation/x1-index-manifest.json"),
        replay_manifest(EVIDENCE, f"{BASE}/validation/evidence-index-manifest.json"),
        replay_manifest(head_before, f"{BASE}/validation/final-delta-manifest.json"),
        replay_manifest(head_before, f"{BASE}/validation/final-owner-manifest.json"),
    ]
    checks["manifest_replay_pass"] = all(row["valid"] for row in manifests)
    privacy = privacy_scan(head_before, paths)
    checks["privacy_pass"] = privacy["valid"]
    seal = load(head_before, f"{BASE}/seal/content-seal.json")
    seal_failures = []
    for entry in seal["targets"]:
        data = show(head_before, entry["path"])
        if len(data) != entry["bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
            seal_failures.append(entry["path"])
    checks["content_seal_pass"] = not seal_failures
    truth = load(head_before, f"{BASE}/final/phase-truth.json")
    checks.update({
        "outcomes_exact": truth["outcomes"] == {"completed": 84, "represented": 24, "open_gap": 6, "exact_gate": 6},
        "terminal_verdict_preserved": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "prepared_not_sent": load(head_before, f"{BASE}/final/route-state-candidate.json")["current_state"] == "PREPARED_NOT_SENT",
    })
    head_after = git_text("rev-parse", "HEAD")
    clean_after = not git_text("status", "--porcelain", "--untracked-files=all")
    checks.update({"head_stable": head_after == head_before, "clean_after": clean_after})
    status = "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" if all(checks.values()) else "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL"
    payload = {
        "schema": "ghc.family.exact-final-owner-scoped-canonical.v685.v5", "owner": "Eiren Kestrel", "phase": "v685-v5",
        "branch": BRANCH, "head": head_before, "source": SOURCE, "x1": X1, "evidence": EVIDENCE,
        "status": status, "canonical_invocation_count": 1, "canonical_success_count": 1 if status.startswith("VALID") else 0,
        "canonical_replay_count": 0, "replay_prohibited": True, "complete_repository_suite": False,
        "same_owner_shared_infrastructure": True, "independent_reproduction": False,
        "check_count": len(checks), "pass_count": sum(checks.values()), "checks": checks,
        "owner_test_exit_code": final_test.returncode, "owner_test_output": final_test.stdout.decode("utf-8", "replace") + final_test.stderr.decode("utf-8", "replace"),
        "owner_file_count": len(paths), "json_parse_count": json_count, "json_parse_failures": json_failures,
        "markdown_check_count": markdown_count, "markdown_failures": markdown_failures,
        "python_file_count": sum(p.endswith(".py") for p in paths), "python_findings": python_findings,
        "manifest_entry_total": sum(row["entry_count"] for row in manifests), "manifest_results": manifests,
        "privacy": privacy, "seal_target_count": seal["target_count"], "seal_failures": seal_failures,
        "local": local, "upstream": upstream, "tracking": tracking, "fresh_live": fresh_live, "divergence": divergence,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    payload["canonical_payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": status, "head": head_before, "pass_count": payload["pass_count"], "check_count": payload["check_count"]}, sort_keys=True))
    return 0 if status.startswith("VALID") else 2


if __name__ == "__main__":
    raise SystemExit(main())
