"""One-shot exact-final owner-scoped canonical validator for Caelen Ash v670-v5."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OWNER_PREFIX = "docs/caelen-ash/v670-v5/"
BRANCH = "codex/GHC-Family/caelen-ash-v670-v5-full-tools"
SOURCE = "2791ab06f51c12d7fcaaeb158498710318b3d283"
X1 = "36f3cd2658ef15a037032d1c03e49c3ab344cfd9"
EVIDENCE = "69eb9f178c59c6f41e0a8a10858a0fa381f1005d"
X1_MANIFEST = OWNER_PREFIX + "validation/x1-manifest.json"
EVIDENCE_MANIFEST = OWNER_PREFIX + "validation/evidence-manifest.json"
FINAL_DELTA_MANIFEST = OWNER_PREFIX + "validation/final-delta-manifest.json"
FINAL_OWNER_MANIFEST = OWNER_PREFIX + "validation/final-owner-manifest.json"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}


class ValidationError(RuntimeError):
    """Raised when the one-shot aggregate must fail closed."""


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=ROOT, check=check, capture_output=True)


def git_text(*args: str) -> str:
    return git(*args).stdout.decode("utf-8", errors="strict").strip()


def blob(commit: str, path: str) -> bytes:
    return git("show", f"{commit}:{path}").stdout


def unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValidationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise ValidationError(f"nonfinite JSON constant: {value}")


def strict_json_bytes(data: bytes) -> Any:
    try:
        value = json.loads(data.decode("utf-8", errors="strict"), object_pairs_hook=unique_pairs, parse_constant=reject_constant)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValidationError(f"strict JSON parse failed: {exc}") from exc
    if isinstance(value, float) and not math.isfinite(value):
        raise ValidationError("nonfinite JSON root")
    return value


def tree_paths(commit: str) -> list[str]:
    return git_text("diff", "--name-only", SOURCE, commit).splitlines()


def replay_manifest(commit: str, path: str) -> dict[str, Any]:
    manifest = strict_json_bytes(blob(commit, path))
    mismatches = []
    for row in manifest["entries"]:
        data = blob(commit, row["path"])
        if len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
            mismatches.append(row["path"])
    if mismatches or manifest["entry_count"] != len(manifest["entries"]):
        raise ValidationError(f"manifest replay failed: {path}: {mismatches}")
    return {"path": path, "entries": len(manifest["entries"]), "self_exclusions": len(manifest["self_exclusions"]), "mismatches": 0}


def manifest_coverage(head: str) -> dict[str, bool]:
    x1 = strict_json_bytes(blob(X1, X1_MANIFEST))
    evidence = strict_json_bytes(blob(EVIDENCE, EVIDENCE_MANIFEST))
    delta = strict_json_bytes(blob(head, FINAL_DELTA_MANIFEST))
    owner = strict_json_bytes(blob(head, FINAL_OWNER_MANIFEST))
    checks = {
        "x1": {row["path"] for row in x1["entries"]} | set(x1["self_exclusions"]) == set(git_text("diff", "--name-only", SOURCE, X1).splitlines()),
        "evidence": {row["path"] for row in evidence["entries"]} | set(evidence["self_exclusions"]) == set(git_text("diff", "--name-only", X1, EVIDENCE).splitlines()),
        "final_delta": {row["path"] for row in delta["entries"]} | set(delta["self_exclusions"]) == set(git_text("diff", "--name-only", EVIDENCE, head).splitlines()),
        "final_owner": {row["path"] for row in owner["entries"]} | set(owner["self_exclusions"]) == set(git_text("diff", "--name-only", SOURCE, head).splitlines()),
    }
    if not all(checks.values()):
        raise ValidationError(f"manifest coverage failed: {checks}")
    return checks


def git_gate(expected_head: str) -> dict[str, Any]:
    branch = git_text("branch", "--show-current")
    head = git_text("rev-parse", "HEAD")
    upstream = git_text("rev-parse", "@{upstream}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{branch}")
    live_rows = git_text("ls-remote", "--heads", "origin", f"refs/heads/{branch}").split()
    live = live_rows[0] if live_rows else ""
    commits = git_text("rev-list", "--reverse", f"{SOURCE}..{head}").splitlines()
    parents = [len(git_text("show", "-s", "--format=%P", commit).split()) for commit in commits]
    gate = {
        "branch": branch, "head": head, "upstream": upstream, "tracking": tracking, "fresh_live": live,
        "clean": git_text("status", "--porcelain", "--untracked-files=all") == "",
        "divergence": git_text("rev-list", "--left-right", "--count", "HEAD...@{upstream}"),
        "four_way_equal": head == upstream == tracking == live,
        "final_parent": git_text("rev-parse", "HEAD^"),
        "phase_commits": len(commits), "parent_counts": parents,
        "merge_commits": len(git_text("rev-list", "--merges", f"{SOURCE}..{head}").splitlines()),
        "source_ancestor": git("merge-base", "--is-ancestor", SOURCE, head, check=False).returncode == 0,
        "x1_ancestor": git("merge-base", "--is-ancestor", X1, head, check=False).returncode == 0,
        "evidence_ancestor": git("merge-base", "--is-ancestor", EVIDENCE, head, check=False).returncode == 0,
    }
    required = [
        head == expected_head, branch == BRANCH, gate["clean"], gate["four_way_equal"],
        gate["divergence"].split() == ["0", "0"], gate["final_parent"] == EVIDENCE,
        gate["phase_commits"] == 3, gate["parent_counts"] == [1, 1, 1], gate["merge_commits"] == 0,
        gate["source_ancestor"], gate["x1_ancestor"], gate["evidence_ancestor"],
    ]
    if not all(required):
        raise ValidationError(f"exact-final Git gate failed: {gate}")
    return gate


def run_owner_tests() -> dict[str, Any]:
    command = [sys.executable, "-m", "unittest", "tests.test_ghc_family_caelen_ash_v670_v5_x2", "tests.test_ghc_family_caelen_ash_v670_v5_final", "-v"]
    environment = os.environ.copy()
    environment["PYTHONPATH"] = os.pathsep.join([str(ROOT), str(ROOT / "scripts"), environment.get("PYTHONPATH", "")])
    result = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, text=True, encoding="utf-8", timeout=180)
    combined = result.stdout + result.stderr
    match = re.search(r"Ran\s+(\d+)\s+tests", combined)
    count = int(match.group(1)) if match else 0
    if result.returncode != 0 or count < 45:
        raise ValidationError(f"owner tests failed: code={result.returncode}, count={count}, tail={combined[-3000:]}")
    return {"passed": count, "returncode": result.returncode, "immutable_x1_passed_before_x2": 24, "sequential_total": 24 + count, "full_repository_suite": "not_run_not_claimed"}


def privacy_scan(head: str, paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
        "private_route_or_callable": re.compile(r"source_thread_id|<codex_delegation|\b(?:app|plugin)://", re.I),
        "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']"),
        "transcript_or_session_stream": re.compile(r"(?i)\b(?:session_stream|private_transcript|private_conversation_dump)\b"),
    }
    candidates = []
    confirmed = []
    text_paths = [path for path in paths if Path(path).suffix.lower() in {".py", ".json", ".md", ".txt", ".html", ".yaml"}]
    for path in text_paths:
        text = blob(head, path).decode("utf-8", errors="strict")
        for label, pattern in patterns.items():
            if pattern.search(text):
                scanner = path.endswith(".py") and ("caelen_ash_v670_v5" in path or "caelen_v670_v5" in path)
                row = {"path": path, "pattern_class": label, "disposition": "scanner_definition_or_synthetic_test" if scanner else "confirmed_payload_hit"}
                candidates.append(row)
                if not scanner:
                    confirmed.append(row)
    if confirmed:
        raise ValidationError(f"confirmed privacy hits: {confirmed}")
    return {"text_files": len(text_paths), "candidates": len(candidates), "confirmed_hits": 0, "privacy_complete": False}


def bounded_security(head: str, paths: list[str]) -> dict[str, Any]:
    python_paths = [path for path in paths if path.endswith(".py")]
    findings = []
    for path in python_paths:
        tree = ast.parse(blob(head, path).decode("utf-8", errors="strict"), filename=path)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            name = node.func.id if isinstance(node.func, ast.Name) else ""
            if name in {"eval", "exec"}:
                findings.append({"path": path, "line": node.lineno, "rule": name})
            for keyword in node.keywords:
                if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                    findings.append({"path": path, "line": node.lineno, "rule": "shell_true"})
    if findings:
        raise ValidationError(f"bounded security findings: {findings}")
    return {"changed_python_files": len(python_paths), "bounded_findings": 0, "exhaustive_security": False}


def validate_content(head: str, paths: list[str]) -> dict[str, Any]:
    json_paths = [path for path in paths if path.endswith(".json")]
    text_paths = [path for path in paths if Path(path).suffix.lower() in {".json", ".md", ".html", ".txt", ".yaml"}]
    oversized = []
    for path in json_paths:
        strict_json_bytes(blob(head, path))
    for path in text_paths:
        words = len(blob(head, path).decode("utf-8", errors="strict").split())
        if words > 100000:
            oversized.append({"path": path, "words": words})
    materialized = len([path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts])
    if oversized or materialized >= 2000:
        raise ValidationError(f"document or file ceiling failed: {oversized}, materialized={materialized}")
    return {"json_parses": len(json_paths), "documents": len(text_paths), "oversized": 0, "materialized_files": materialized, "file_ceiling": 2000}


def validate_truth(head: str) -> dict[str, Any]:
    truth = strict_json_bytes(blob(head, OWNER_PREFIX + "closeout/phase-truth.json"))
    route = strict_json_bytes(blob(head, OWNER_PREFIX + "orchestration/route-state-final-candidate.json"))
    expected = {
        "effective_negatives": 32772, "effective_methods": 18949,
        "effective_failed_witnesses": 4593, "effective_passing_witnesses": 5988,
        "open_gaps": 249, "exact_gates": 244,
    }
    if any(truth[key] != value for key, value in expected.items()):
        raise ValidationError(f"terminal counts drifted: {truth}")
    if set(truth["outcomes"]) != ALLOWED_OUTCOMES or truth["outcomes"] != {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}:
        raise ValidationError("outcome truth drifted")
    if truth["terminal_verdict"] != "NOT_READY_FOR_STAGE_20" or route["state"] != "PREPARED_NOT_SENT" or route["successor_contacted"] is not False or route["prospective_exact_title"] is not None:
        raise ValidationError("terminal or route truth drifted")
    return {"counts": expected, "outcomes": truth["outcomes"], "route_state": route["state"], "terminal_verdict": truth["terminal_verdict"]}


def aggregate(expected_head: str) -> dict[str, Any]:
    gate = git_gate(expected_head)
    head = gate["head"]
    paths = tree_paths(head)
    manifests = {
        "x1": replay_manifest(X1, X1_MANIFEST),
        "evidence": replay_manifest(EVIDENCE, EVIDENCE_MANIFEST),
        "final_delta": replay_manifest(head, FINAL_DELTA_MANIFEST),
        "final_owner": replay_manifest(head, FINAL_OWNER_MANIFEST),
    }
    coverage = manifest_coverage(head)
    tests = run_owner_tests()
    content = validate_content(head, paths)
    privacy = privacy_scan(head, paths)
    security = bounded_security(head, paths)
    truth = validate_truth(head)
    detailed = [
        gate["branch"] == BRANCH, gate["clean"], gate["four_way_equal"], gate["divergence"].split() == ["0", "0"],
        gate["final_parent"] == EVIDENCE, gate["phase_commits"] == 3, gate["parent_counts"] == [1, 1, 1], gate["merge_commits"] == 0,
        gate["source_ancestor"], gate["x1_ancestor"], gate["evidence_ancestor"], tests["returncode"] == 0,
        tests["passed"] >= 45, all(row["mismatches"] == 0 for row in manifests.values()), all(coverage.values()),
        content["json_parses"] >= 150, content["oversized"] == 0, content["materialized_files"] < 2000,
        privacy["confirmed_hits"] == 0, security["bounded_findings"] == 0,
        truth["counts"]["effective_negatives"] == 32772, truth["counts"]["effective_methods"] == 18949,
        truth["counts"]["effective_failed_witnesses"] == 4593, truth["counts"]["effective_passing_witnesses"] == 5988,
        truth["counts"]["open_gaps"] == 249, truth["counts"]["exact_gates"] == 244,
        truth["outcomes"] == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
        truth["route_state"] == "PREPARED_NOT_SENT", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        git_text("status", "--porcelain", "--untracked-files=all") == "",
    ]
    if not all(detailed):
        raise ValidationError("one or more detailed terminal checks failed")
    minimal = detailed[:15]
    return {
        "schema": "ghc.family.exact-final-canonical-receipt.v5",
        "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "owner": "Caelen Ash", "phase": "v670-v5", "head": head,
        "git": gate, "tests": tests, "manifests": manifests, "manifest_coverage": coverage,
        "content": content, "privacy": privacy, "bounded_security": security, "truth": truth,
        "detailed_checks": {"passed": sum(detailed), "total": len(detailed)},
        "minimal_checks": {"passed": sum(minimal), "total": len(minimal)},
        "canonical_invocations": 1, "canonical_successes": 1, "canonical_replayed": False,
        "full_repository_suite": "not_run_not_claimed", "same_owner_only": True,
        "independent_reproduction": False, "external_audit": False,
        "production_certification": False, "privacy_complete": False,
        "accessibility_complete": False, "exhaustive_security": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }


def atomic_write(path: Path, payload: dict[str, Any]) -> None:
    data = (json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    handle, temp_name = tempfile.mkstemp(prefix="caelen-v670-v5-", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(handle, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--lock", required=True)
    args = parser.parse_args()
    receipt = Path(args.receipt)
    lock = Path(args.lock)
    if not receipt.is_absolute() or not lock.is_absolute() or receipt.parent != lock.parent:
        raise SystemExit("receipt and lock must be absolute sibling paths")
    if not receipt.parent.is_dir() or receipt.parent.is_symlink() or receipt.exists() or lock.exists():
        raise SystemExit("exclusive external receipt gate failed")
    lock_handle = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    with os.fdopen(lock_handle, "w", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps({"owner": "Caelen Ash", "phase": "v670-v5", "state": "INVOKED_ONCE"}, sort_keys=True) + "\n")
        stream.flush()
        os.fsync(stream.fileno())
    try:
        result = aggregate(args.expected_head)
    except Exception as exc:
        failure = {
            "schema": "ghc.family.exact-final-canonical-receipt.v5",
            "status": "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT", "owner": "Caelen Ash", "phase": "v670-v5",
            "error_type": type(exc).__name__, "error": str(exc),
            "canonical_invocations": 1, "canonical_successes": 0, "replay_allowed": False,
        }
        atomic_write(receipt, failure)
        raise
    atomic_write(receipt, result)
    print(json.dumps({"status": result["status"], "head": result["head"], "tests": result["tests"], "detailed_checks": result["detailed_checks"], "minimal_checks": result["minimal_checks"], "json_parses": result["content"]["json_parses"], "privacy": result["privacy"], "manifests": {key: value["entries"] for key, value in result["manifests"].items()}}, sort_keys=True))


if __name__ == "__main__":
    main()
