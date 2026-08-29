#!/usr/bin/env python3
"""One-shot owner-scoped exact-final canonical validator for Lyren v675-v6."""

from __future__ import annotations

import argparse
import ast
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OWNER = "Lyren Moss"
PHASE = "v675-v6"
SOURCE_FINAL = "0aa1f2b1250e5540650b683d221f92e8762cd991"
X1_COMMIT = "920c8e89dff0c4625087a52a3dc5ee2916b0b659"
EVIDENCE_COMMIT = "78b4cbd6bc91cc422d99497bbb4b59e5dfac9eb6"
BRANCH = "codex/GHC-Family/lyren-moss-v675-v6-full-tools"
TRACKING = "refs/remotes/origin/codex/GHC-Family/lyren-moss-v675-v6-full-tools"
REMOTE_REF = "refs/heads/codex/GHC-Family/lyren-moss-v675-v6-full-tools"
BASE = "docs/lyren-moss/v675-v6"


def git(*args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, text=True, encoding="utf-8", errors="replace",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def git_blob(commit: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=ROOT)


def git_json(commit: str, path: str) -> Any:
    return json.loads(git_blob(commit, path).decode("utf-8"))


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE))


def owner_paths(head: str) -> list[str]:
    rows = git("ls-tree", "-r", "--name-only", head).splitlines()
    return sorted(
        path for path in rows
        if path.startswith(BASE + "/")
        or (path.startswith("scripts/") and "lyren_moss_v675_v6" in path)
        or (path.startswith("tests/") and "lyren_moss_v675_v6" in path)
    )


def replay_entries(commit: str, entries: list[dict[str, Any]], label: str) -> tuple[int, list[dict[str, str]]]:
    mismatches = []
    for entry in entries:
        path = entry["path"]
        try:
            oid = git("rev-parse", f"{commit}:{path}").strip()
            blob = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=ROOT)
        except (RuntimeError, subprocess.CalledProcessError) as exc:
            mismatches.append({"label": label, "path": path, "reason": f"missing: {exc}"})
            continue
        if oid != entry["git_blob"]:
            mismatches.append({"label": label, "path": path, "reason": "git_blob_mismatch"})
        elif len(blob) != entry["bytes"]:
            mismatches.append({"label": label, "path": path, "reason": "byte_count_mismatch"})
        elif sha256(blob) != entry["sha256"]:
            mismatches.append({"label": label, "path": path, "reason": "sha256_mismatch"})
    return len(entries), mismatches


def privacy_scan(head: str, paths: list[str]) -> dict[str, Any]:
    patterns = {
        "private_route_or_task_ids": re.compile(r"(?:source_thread_id|clientThreadId|threadId)"),
        "raw_delegation_or_transcript": re.compile(r"(?:<codex_delegation>|<source_thread_id>)", re.IGNORECASE),
        "private_filesystem_paths": re.compile(r"(?:[A-Za-z]:[\\/](?:Users|GHC-Archives)[\\/]|/Users/|/home/)"),
        "credential_or_secret_labels": re.compile(r"(?:api_key|access_token|refresh_token|authorization:\\s*bearer)", re.IGNORECASE),
        "email_or_raw_identifier": re.compile(r"(?:[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,}|OMEGA44TOKEN-)", re.IGNORECASE),
    }
    candidates = []
    confirmed = []
    text_paths = [path for path in paths if Path(path).suffix.lower() in {".json", ".md", ".html", ".py", ".txt"} or path.endswith("SKILL.md")]
    for path in text_paths:
        text = git_blob(head, path).decode("utf-8", errors="replace")
        for line_number, line in enumerate(text.splitlines(), 1):
            for privacy_class, pattern in patterns.items():
                if not pattern.search(line):
                    continue
                declaration = path.endswith(".py") and any(token in line for token in (
                    "source_thread_id", "clientThreadId", "threadId", "api_key", "access_token",
                    "refresh_token", "GHC-Archives", "codex_delegation", "OMEGA44TOKEN-", "re.compile", "forbidden =",
                ))
                row = {"path": path, "line": line_number, "privacy_class": privacy_class, "classification": "rejected_known_test_or_scanner_declaration" if declaration else "confirmed"}
                candidates.append(row)
                if not declaration:
                    confirmed.append(row)
    return {
        "classes": list(patterns), "files_scanned": len(text_paths),
        "candidate_count": len(candidates), "candidates": candidates,
        "confirmed_hit_count": len(confirmed), "confirmed_hits": confirmed,
        "complete_privacy_claim": False,
    }


def ast_security_scan(head: str, paths: list[str]) -> dict[str, Any]:
    findings = []
    python_paths = [path for path in paths if path.endswith(".py")]
    for path in python_paths:
        text = git_blob(head, path).decode("utf-8")
        try:
            tree = ast.parse(text, filename=path)
        except SyntaxError as exc:
            findings.append({"path": path, "line": exc.lineno or 0, "kind": "syntax_error"})
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                findings.append({"path": path, "line": node.lineno, "kind": node.func.id})
            if isinstance(node.func, ast.Attribute):
                owner = node.func.value.id if isinstance(node.func.value, ast.Name) else ""
                if owner == "os" and node.func.attr == "system":
                    findings.append({"path": path, "line": node.lineno, "kind": "os.system"})
                if owner == "pickle" and node.func.attr in {"load", "loads"}:
                    findings.append({"path": path, "line": node.lineno, "kind": f"pickle.{node.func.attr}"})
                if owner == "subprocess" and any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords):
                    findings.append({"path": path, "line": node.lineno, "kind": "subprocess_shell_true"})
    return {"python_files": len(python_paths), "findings": findings, "finding_count": len(findings), "exhaustive_security_claim": False}


def run_final_tests() -> dict[str, Any]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [sys.executable, "tests/test_ghc_family_lyren_moss_v675_v6_final.py", "-v"],
        cwd=ROOT, env=env, text=True, encoding="utf-8", errors="replace",
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
    )
    match = re.search(r"Ran (\d+) tests?", result.stdout)
    return {
        "command": "python tests/test_ghc_family_lyren_moss_v675_v6_final.py -v",
        "returncode": result.returncode,
        "tests": int(match.group(1)) if match else 0,
        "output_sha256": sha256(result.stdout.encode("utf-8")),
        "output_tail": result.stdout[-4000:],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    receipt_path = Path(args.receipt)
    if receipt_path.drive.upper() != "D:":
        raise RuntimeError("canonical receipt must use the D: evidence bank")
    if receipt_path.exists():
        raise RuntimeError("exclusive canonical receipt already exists; success replay is forbidden")

    head = git("rev-parse", "HEAD").strip()
    branch = git("branch", "--show-current").strip()
    upstream = git("rev-parse", "@{upstream}").strip()
    tracking = git("rev-parse", TRACKING).strip()
    remote_rows = git("ls-remote", "--heads", "origin", REMOTE_REF).split()
    fresh_live = remote_rows[0] if remote_rows else ""
    divergence = git("rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()
    clean_before = not bool(git("status", "--porcelain").strip())
    if len(set((head, upstream, tracking, fresh_live))) != 1 or divergence != ["0", "0"] or not clean_before:
        raise RuntimeError("exact-final equality, divergence, or clean precondition failed")
    if branch != BRANCH:
        raise RuntimeError("canonical validator is on the wrong branch")

    paths = owner_paths(head)
    json_paths = [path for path in paths if path.endswith(".json")]
    json_errors = []
    for path in json_paths:
        try:
            json.loads(git_blob(head, path).decode("utf-8"))
        except Exception as exc:
            json_errors.append({"path": path, "error": str(exc)})

    final_truth = git_json(head, f"{BASE}/final/phase-truth.json")
    route = git_json(head, f"{BASE}/final/route-state.json")
    baton_text = git_blob(head, f"{BASE}/handoffs/ilyra-fen-v675-v7-activation-candidate.md").decode("utf-8")
    baton_words = words(baton_text)
    owner_manifest = git_json(head, f"{BASE}/validation/final-owner-manifest.json")
    delta_manifest = git_json(head, f"{BASE}/validation/final-delta-manifest.json")
    x1_manifest = git_json(head, f"{BASE}/validation/x1-manifest.json")
    evidence_manifest = git_json(head, f"{BASE}/validation/evidence-manifest.json")
    content_seal = git_json(head, f"{BASE}/closeout/content-seal.json")

    replay_total = 0
    replay_mismatches: list[dict[str, str]] = []
    checks = [
        (X1_COMMIT, x1_manifest["entries"], "x1_manifest"),
        (X1_COMMIT, evidence_manifest["immutable_x1_entries"], "evidence_immutable_x1"),
        (EVIDENCE_COMMIT, evidence_manifest["staged_x2_entries"], "evidence_x2"),
        (EVIDENCE_COMMIT, owner_manifest["immutable_entries"], "final_owner_immutable"),
        (head, owner_manifest["final_delta_entries"], "final_owner_delta"),
        (head, delta_manifest["entries"], "final_delta"),
        (head, content_seal["entries"], "content_seal"),
    ]
    for commit, entries, label in checks:
        count, mismatches = replay_entries(commit, entries, label)
        replay_total += count
        replay_mismatches.extend(mismatches)

    self_exclusions = sorted(set(owner_manifest["self_exclusions"]) | set(delta_manifest["self_exclusions"]) | set(content_seal["self_exclusions"]))
    missing_exclusions = [path for path in self_exclusions if not git("cat-file", "-e", f"{head}:{path}", check=False) == ""]
    # git cat-file -e writes no stdout on both success and our unchecked failure; use rev-parse instead.
    missing_exclusions = []
    for path in self_exclusions:
        result = subprocess.run(["git", "cat-file", "-e", f"{head}:{path}"], cwd=ROOT)
        if result.returncode != 0:
            missing_exclusions.append(path)

    privacy = privacy_scan(head, paths)
    security = ast_security_scan(head, paths)
    test_result = run_final_tests()
    parent_counts = [
        len(git("rev-list", "--parents", "-n", "1", commit).split()) - 1
        for commit in (X1_COMMIT, EVIDENCE_COMMIT, head)
    ]
    phase_commits = int(git("rev-list", "--count", f"{SOURCE_FINAL}..{head}").strip())
    phase_merges = int(git("rev-list", "--merges", "--count", f"{SOURCE_FINAL}..{head}").strip())
    outcome_expected = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
    truth = final_truth["sealed_working_truth"]

    detailed = {
        "branch_exact": branch == BRANCH,
        "head_equals_upstream": head == upstream,
        "head_equals_tracking": head == tracking,
        "head_equals_fresh_live": head == fresh_live,
        "zero_divergence": divergence == ["0", "0"],
        "clean_before": clean_before,
        "x1_parent_source": git("rev-parse", f"{X1_COMMIT}^").strip() == SOURCE_FINAL,
        "evidence_parent_x1": git("rev-parse", f"{EVIDENCE_COMMIT}^").strip() == X1_COMMIT,
        "final_parent_evidence": git("rev-parse", "HEAD^").strip() == EVIDENCE_COMMIT,
        "three_phase_commits": phase_commits == 3,
        "zero_merges": phase_merges == 0,
        "single_parent_each": parent_counts == [1, 1, 1],
        "owner_file_ceiling": len(paths) < 2000,
        "commit_ceiling": phase_commits <= 8,
        "baton_word_bounds": 10_000 <= baton_words <= 100_000,
        "outcomes_exact": final_truth["outcomes"] == outcome_expected,
        "labels_exact": set(final_truth["allowed_outcome_labels"]) == set(outcome_expected),
        "negative_count": truth["effective_negatives"] == 41113,
        "method_count": truth["method_flow_methods"] == 29405,
        "failed_witness_count": truth["failed_witnesses"] == 12774,
        "passing_witness_count": truth["bounded_passing_witnesses"] == 16856,
        "open_gap_count": truth["open_gaps"] == 341,
        "exact_gate_count": truth["exact_gates"] == 333,
        "proposal_count": truth["declared_proposals"] == 7270,
        "verdict_protected": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "route_prepared_not_sent": route["state"] == "PREPARED_NOT_SENT" and not route["sent_by_lyren_moss"],
        "json_parse_clean": not json_errors,
        "manifest_replay_clean": not replay_mismatches,
        "self_exclusions_present": not missing_exclusions and len(self_exclusions) == 6,
        "privacy_confirmed_zero": privacy["confirmed_hit_count"] == 0,
        "bounded_security_zero": security["finding_count"] == 0,
        "final_tests_pass": test_result["returncode"] == 0 and test_result["tests"] >= 20,
        "baton_prepared_marker": "PREPARED_NOT_SENT = true" in baton_text,
        "baton_unsent_marker": "SENT_BY_LYREN_MOSS = false" in baton_text,
        "source_adapter_zero": git_json(head, f"{BASE}/x2/source-adapter.json")["network_calls"] == 0,
    }
    failed_detailed = [name for name, passed in detailed.items() if not passed]
    if failed_detailed:
        raise RuntimeError(json.dumps({"failed_detailed": failed_detailed, "json_errors": json_errors, "replay_mismatches": replay_mismatches, "missing_exclusions": missing_exclusions, "privacy": privacy, "security": security, "tests": test_result}, indent=2))

    fresh_after_rows = git("ls-remote", "--heads", "origin", REMOTE_REF).split()
    fresh_after = fresh_after_rows[0] if fresh_after_rows else ""
    clean_after = not bool(git("status", "--porcelain").strip())
    minimal = {
        "exact_head": head == git("rev-parse", "HEAD").strip(),
        "clean_after": clean_after,
        "fresh_live_after": fresh_after == head,
        "zero_divergence_after": git("rev-list", "--left-right", "--count", "HEAD...@{upstream}").split() == ["0", "0"],
        "three_commits": phase_commits == 3,
        "zero_merges": phase_merges == 0,
        "x1_direct": detailed["x1_parent_source"],
        "evidence_direct": detailed["evidence_parent_x1"],
        "final_direct": detailed["final_parent_evidence"],
        "tests_pass": detailed["final_tests_pass"],
        "json_clean": not json_errors,
        "privacy_clean": privacy["confirmed_hit_count"] == 0,
        "manifest_clean": not replay_mismatches,
        "route_unsent": detailed["route_prepared_not_sent"],
        "stage20_protected": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
    }
    if len(minimal) != 15 or not all(minimal.values()):
        raise RuntimeError(f"minimal canonical checks failed: {minimal}")

    payload = {
        "schema": "ghc.family.external-canonical-receipt.v12",
        "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "owner": OWNER,
        "phase": PHASE,
        "validated_at_utc": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "branch": BRANCH,
        "source_final": SOURCE_FINAL,
        "x1_commit": X1_COMMIT,
        "evidence_commit": EVIDENCE_COMMIT,
        "exact_final": head,
        "invocation_count": 1,
        "success_count": 1,
        "replayed_after_success": False,
        "scope": "exact Lyren source-to-final owner delta and declared dependencies",
        "full_repository_suite": False,
        "independent_reproduction": False,
        "external_audit": False,
        "production_certification": False,
        "complete_privacy_or_accessibility_assurance": False,
        "exhaustive_security": False,
        "detailed_checks": {"passed": len(detailed), "total": len(detailed), "rows": detailed},
        "minimal_checks": {"passed": len(minimal), "total": len(minimal), "rows": minimal},
        "tests": {"passed": test_result["tests"], "returncode": test_result["returncode"], "output_sha256": test_result["output_sha256"]},
        "strict_json_parses": len(json_paths),
        "manifest_replays": replay_total,
        "manifest_mismatches": 0,
        "owner_files": len(paths),
        "privacy": {"files_scanned": privacy["files_scanned"], "classes": len(privacy["classes"]), "candidates": privacy["candidate_count"], "confirmed_hits": 0},
        "bounded_python_security": {"python_files": security["python_files"], "findings": 0},
        "baton_words": baton_words,
        "phase_commits": phase_commits,
        "phase_merges": phase_merges,
        "parent_counts": parent_counts,
        "four_way_equal_before_and_after": True,
        "zero_divergence_before_and_after": True,
        "clean_before_and_after": True,
        "outcomes": final_truth["outcomes"],
        "working_truth": truth,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    payload["canonical_payload_sha256"] = sha256(canonical)
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    with receipt_path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": payload["status"], "exact_final": head,
        "detailed": f"{len(detailed)}/{len(detailed)}", "minimal": "15/15",
        "tests": test_result["tests"], "strict_json_parses": len(json_paths),
        "manifest_replays": replay_total, "owner_files": len(paths),
        "privacy_confirmed_hits": 0, "security_findings": 0,
        "baton_words": baton_words, "canonical_payload_sha256": payload["canonical_payload_sha256"],
        "receipt": str(receipt_path),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
