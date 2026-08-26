"""One-shot exact-final owner-scoped validator for Auren Lark v670-v3."""

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

from scripts.ghc_family_auren_v670_v3_evidence_guard import five_class_scan

ROOT = Path(__file__).resolve().parents[1]
OWNER_PREFIX = "docs/auren-lark/v670-v3/"
BRANCH = "codex/GHC-Family/auren-lark-v670-v3-full-tools"
SOURCE = "a2e0262e7b9f3333fd06a826781516c29181580d"
X1 = "65769017d514255d2763b23c9dd0d0b3e46685f1"
EVIDENCE = "282ba12ec106a1ae87d87badbaedcb90d31f0b97"
X1_MANIFEST = OWNER_PREFIX + "validation/x1-manifest.json"
EVIDENCE_MANIFEST = OWNER_PREFIX + "validation/evidence-manifest.json"
FINAL_DELTA_MANIFEST = OWNER_PREFIX + "validation/final-delta-manifest.json"
FINAL_OWNER_MANIFEST = OWNER_PREFIX + "validation/final-owner-manifest.json"
BATON_PATH = OWNER_PREFIX + "handoffs/next-authorized-v670-v4-activation-candidate.md"
BATON_INTEGRITY = OWNER_PREFIX + "handoffs/activation-candidate-integrity.json"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}


class ValidationError(RuntimeError):
    """Raised when the exact-final aggregate must fail closed."""


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
        payload = json.loads(
            data.decode("utf-8", errors="strict"),
            object_pairs_hook=unique_pairs,
            parse_constant=reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValidationError(f"strict JSON parse failed: {exc}") from exc
    if isinstance(payload, float) and not math.isfinite(payload):
        raise ValidationError("nonfinite JSON root")
    return payload


def tree_paths(commit: str, prefix: str) -> list[str]:
    return git_text("ls-tree", "-r", "--name-only", commit, prefix).splitlines()


def replay_manifest(commit: str, manifest_path: str) -> dict[str, Any]:
    manifest = strict_json_bytes(blob(commit, manifest_path))
    mismatches = []
    for row in manifest["entries"]:
        data = blob(commit, row["path"])
        actual = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
        if actual["bytes"] != row["bytes"] or actual["sha256"] != row["sha256"]:
            mismatches.append({"path": row["path"], "actual": actual})
    if mismatches or manifest["entry_count"] != len(manifest["entries"]):
        raise ValidationError(f"manifest replay failed: {manifest_path}: {mismatches}")
    return {
        "path": manifest_path,
        "entry_count": manifest["entry_count"],
        "self_exclusions": len(manifest["self_exclusions"]),
        "hash_domain": manifest["hash_domain"],
        "mismatches": 0,
    }


def verify_manifest_coverage(head: str) -> dict[str, Any]:
    x1 = strict_json_bytes(blob(X1, X1_MANIFEST))
    evidence = strict_json_bytes(blob(EVIDENCE, EVIDENCE_MANIFEST))
    delta = strict_json_bytes(blob(head, FINAL_DELTA_MANIFEST))
    owner = strict_json_bytes(blob(head, FINAL_OWNER_MANIFEST))
    x1_expected = set(git_text("diff", "--name-only", SOURCE, X1).splitlines())
    evidence_expected = set(git_text("diff", "--name-only", X1, EVIDENCE).splitlines())
    final_expected = set(git_text("diff", "--name-only", EVIDENCE, head).splitlines())
    owner_expected = set(tree_paths(head, OWNER_PREFIX))
    checks = {
        "x1": {row["path"] for row in x1["entries"]} | set(x1["self_exclusions"]) == x1_expected,
        "evidence": {row["path"] for row in evidence["entries"]} | set(evidence["self_exclusions"]) == evidence_expected,
        "final_delta": {row["path"] for row in delta["entries"]} | set(delta["self_exclusions"]) == final_expected,
        "final_owner": {row["path"] for row in owner["entries"]} | set(owner["self_exclusions"]) == owner_expected,
    }
    if not all(checks.values()):
        raise ValidationError(f"manifest coverage failed: {checks}")
    return checks


def verify_git_gate() -> dict[str, Any]:
    branch = git_text("branch", "--show-current")
    head = git_text("rev-parse", "HEAD")
    upstream = git_text("rev-parse", "@{u}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{branch}")
    live_tokens = git_text("ls-remote", "--heads", "origin", f"refs/heads/{branch}").split()
    live = live_tokens[0] if live_tokens else None
    divergence = git_text("rev-list", "--left-right", "--count", "HEAD...@{u}")
    clean = not git_text("status", "--porcelain")
    parent = git_text("rev-parse", "HEAD^")
    parent_count = len(git_text("rev-list", "--parents", "-n", "1", "HEAD").split()) - 1
    commit_count = int(git_text("rev-list", "--count", f"{SOURCE}..{head}"))
    merge_count = int(git_text("rev-list", "--merges", "--count", f"{SOURCE}..{head}"))
    gate = {
        "branch": branch,
        "head": head,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live": live,
        "divergence": divergence,
        "clean": clean,
        "four_way_equal": head == upstream == tracking == live,
        "final_parent": parent,
        "parent_count": parent_count,
        "phase_commit_count": commit_count,
        "merge_count": merge_count,
        "source_ancestor": git("merge-base", "--is-ancestor", SOURCE, head, check=False).returncode == 0,
        "x1_ancestor": git("merge-base", "--is-ancestor", X1, head, check=False).returncode == 0,
        "evidence_ancestor": git("merge-base", "--is-ancestor", EVIDENCE, head, check=False).returncode == 0,
    }
    required = [
        branch == BRANCH,
        clean,
        gate["four_way_equal"],
        divergence.split() == ["0", "0"],
        parent == EVIDENCE,
        parent_count == 1,
        commit_count == 3,
        merge_count == 0,
        gate["source_ancestor"],
        gate["x1_ancestor"],
        gate["evidence_ancestor"],
    ]
    if not all(required):
        raise ValidationError(f"exact-final Git gate failed: {gate}")
    return gate


def run_owner_tests() -> dict[str, Any]:
    args = [
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "tests/test_ghc_family_auren_lark_v670_v3_x1.py",
        "tests/test_ghc_family_auren_lark_v670_v3_x2.py",
        "tests/test_ghc_family_auren_lark_v670_v3_final.py",
        "-k",
        "not test_no_x2_or_closeout_material_exists_in_x1",
    ]
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, check=False)
    output = result.stdout + result.stderr
    passed = re.search(r"(\d+) passed", output)
    deselected = re.search(r"(\d+) deselected", output)
    if result.returncode != 0 or not passed:
        raise ValidationError(f"owner tests failed with code {result.returncode}: {output[-4000:]}")
    return {
        "passed": int(passed.group(1)),
        "deselected_lifecycle_checks": int(deselected.group(1)) if deselected else 0,
        "returncode": result.returncode,
        "selection": "x1 plus x2 plus final, excluding only x1 pre-x2 absence",
    }


def validate_owner_json(head: str) -> dict[str, Any]:
    paths = [path for path in tree_paths(head, OWNER_PREFIX) if path.endswith(".json")]
    for path in paths:
        strict_json_bytes(blob(head, path))
    return {"strict_json_parses": len(paths), "failures": 0}


def validate_owner_privacy(head: str) -> dict[str, Any]:
    suffixes = (".json", ".md", ".html", ".txt", ".tex")
    paths = [path for path in tree_paths(head, OWNER_PREFIX) if path.lower().endswith(suffixes)]
    candidates = []
    for path in paths:
        text = blob(head, path).decode("utf-8", errors="strict")
        hits = five_class_scan(text)["confirmed_hits"]
        if hits:
            candidates.append({"path": path, "classes": hits})
    if candidates:
        raise ValidationError(f"confirmed owner privacy candidates: {candidates}")
    return {"owner_text_files": len(paths), "confirmed_hits": 0, "privacy_complete": False}


def validate_changed_python(head: str) -> dict[str, Any]:
    paths = [path for path in git_text("diff", "--name-only", SOURCE, head).splitlines() if path.endswith(".py")]
    findings = []
    for path in paths:
        source = blob(head, path).decode("utf-8", errors="strict")
        tree = ast.parse(source, filename=path)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            name = ""
            if isinstance(node.func, ast.Name):
                name = node.func.id
            elif isinstance(node.func, ast.Attribute):
                parts = []
                cursor: ast.expr = node.func
                while isinstance(cursor, ast.Attribute):
                    parts.append(cursor.attr)
                    cursor = cursor.value
                if isinstance(cursor, ast.Name):
                    parts.append(cursor.id)
                name = ".".join(reversed(parts))
            if name in {"eval", "exec", "os.system"}:
                findings.append({"path": path, "line": node.lineno, "rule": name})
            for keyword in node.keywords:
                if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                    findings.append({"path": path, "line": node.lineno, "rule": "shell_true"})
    if findings:
        raise ValidationError(f"bounded AST findings: {findings}")
    return {"changed_python_files": len(paths), "bounded_findings": 0, "exhaustive_security": False}


def validate_documents(head: str) -> dict[str, Any]:
    text_suffixes = (".json", ".md", ".html", ".txt", ".tex")
    paths = [path for path in tree_paths(head, OWNER_PREFIX) if path.lower().endswith(text_suffixes)]
    oversized = []
    for path in paths:
        words = len(blob(head, path).decode("utf-8", errors="strict").split())
        if words > 100000:
            oversized.append({"path": path, "words": words})
    materialized = len([path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts])
    if oversized or materialized >= 2000:
        raise ValidationError(f"document or materialization ceiling failed: {oversized}, {materialized}")
    return {"documents_checked": len(paths), "oversized": 0, "materialized_files": materialized, "file_ceiling": 2000}


def validate_baton(head: str) -> dict[str, Any]:
    integrity = strict_json_bytes(blob(head, BATON_INTEGRITY))
    data = blob(head, BATON_PATH)
    words = len(data.decode("utf-8", errors="strict").split())
    actual = hashlib.sha256(data).hexdigest()
    if integrity["path"] != BATON_PATH or integrity["sha256"] != actual or integrity["bytes"] != len(data) or integrity["words"] != words or not 10000 <= words <= 100000 or integrity["state"] != "PREPARED_NOT_SENT":
        raise ValidationError("baton Git-blob integrity failed")
    return {"bytes": len(data), "words": words, "sha256": actual, "state": integrity["state"]}


def validate_truth(head: str) -> dict[str, Any]:
    truth = strict_json_bytes(blob(head, OWNER_PREFIX + "closeout/phase-truth.json"))
    outcomes = truth["outcomes"]
    route = strict_json_bytes(blob(head, OWNER_PREFIX + "orchestration/route-state-final-candidate.json"))
    expected_counts = {
        "effective_negatives": 32409,
        "effective_methods": 18520,
        "effective_failed_witnesses": 4230,
        "effective_passing_witnesses": 5561,
        "open_gaps": 245,
        "exact_gates": 240,
    }
    if any(truth[key] != value for key, value in expected_counts.items()):
        raise ValidationError(f"final counts drifted: {truth}")
    if set(outcomes) != ALLOWED_OUTCOMES or outcomes != {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}:
        raise ValidationError(f"final outcomes drifted: {outcomes}")
    if (
        truth["terminal_verdict"] != "NOT_READY_FOR_STAGE_20"
        or route["state"] != "PREPARED_NOT_SENT"
        or route["successor_contacted"] is not False
        or route["prospective_exact_title"] is not None
        or route["recipient_state"] != "UNRESOLVED_UNTIL_TERMINAL_LIVE_REFRESH"
    ):
        raise ValidationError("terminal truth or route state drifted")
    return {"counts": expected_counts, "outcomes": outcomes, "terminal_verdict": truth["terminal_verdict"], "route_state": route["state"]}


def aggregate() -> dict[str, Any]:
    git_gate = verify_git_gate()
    head = git_gate["head"]
    manifests = {
        "x1": replay_manifest(X1, X1_MANIFEST),
        "evidence": replay_manifest(EVIDENCE, EVIDENCE_MANIFEST),
        "final_delta": replay_manifest(head, FINAL_DELTA_MANIFEST),
        "final_owner": replay_manifest(head, FINAL_OWNER_MANIFEST),
    }
    coverage = verify_manifest_coverage(head)
    tests = run_owner_tests()
    json_result = validate_owner_json(head)
    privacy = validate_owner_privacy(head)
    security = validate_changed_python(head)
    documents = validate_documents(head)
    baton = validate_baton(head)
    truth = validate_truth(head)
    detailed = [
        git_gate["branch"] == BRANCH,
        git_gate["clean"],
        git_gate["four_way_equal"],
        git_gate["divergence"].split() == ["0", "0"],
        git_gate["final_parent"] == EVIDENCE,
        git_gate["parent_count"] == 1,
        git_gate["phase_commit_count"] == 3,
        git_gate["merge_count"] == 0,
        git_gate["source_ancestor"],
        git_gate["x1_ancestor"],
        git_gate["evidence_ancestor"],
        tests["returncode"] == 0,
        tests["deselected_lifecycle_checks"] == 1,
        manifests["x1"]["mismatches"] == 0,
        manifests["evidence"]["mismatches"] == 0,
        manifests["final_delta"]["mismatches"] == 0,
        manifests["final_owner"]["mismatches"] == 0,
        all(coverage.values()),
        json_result["failures"] == 0,
        privacy["confirmed_hits"] == 0,
        security["bounded_findings"] == 0,
        documents["oversized"] == 0,
        documents["materialized_files"] < 2000,
        baton["state"] == "PREPARED_NOT_SENT",
        10000 <= baton["words"] <= 100000,
        truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        truth["route_state"] == "PREPARED_NOT_SENT",
        truth["outcomes"] == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
        truth["counts"]["effective_negatives"] == 32409,
        truth["counts"]["open_gaps"] == 245,
        truth["counts"]["exact_gates"] == 240,
        git_text("status", "--porcelain") == "",
    ]
    if not all(detailed):
        raise ValidationError("one or more detailed terminal checks failed")
    minimal = detailed[:15]
    return {
        "schema": "ghc.family.exact-final-canonical-receipt.v5",
        "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "owner": "Auren Lark",
        "phase": "v670-v3",
        "head": head,
        "git": git_gate,
        "tests": tests,
        "manifests": manifests,
        "manifest_coverage": coverage,
        "json": json_result,
        "privacy": privacy,
        "bounded_security": security,
        "documents": documents,
        "baton": baton,
        "truth": truth,
        "detailed_checks": {"passed": sum(detailed), "total": len(detailed)},
        "minimal_checks": {"passed": sum(minimal), "total": len(minimal)},
        "canonical_invocations": 1,
        "canonical_successes": 1,
        "canonical_replayed": False,
        "full_repository_suite": "not_run_not_claimed",
        "independent_reproduction": False,
        "external_audit": False,
        "production_certification": False,
        "privacy_complete": False,
        "accessibility_complete": False,
        "exhaustive_security": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }


def atomic_write(path: Path, payload: dict[str, Any]) -> None:
    data = (json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    handle, temp_name = tempfile.mkstemp(prefix="auren-v670-v3-", suffix=".tmp", dir=path.parent)
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
        stream.write(json.dumps({"owner": "Auren Lark", "phase": "v670-v3", "state": "INVOKED_ONCE"}, sort_keys=True) + "\n")
        stream.flush()
        os.fsync(stream.fileno())
    try:
        result = aggregate()
    except Exception as exc:
        failure = {
            "schema": "ghc.family.exact-final-canonical-receipt.v5",
            "status": "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT",
            "owner": "Auren Lark",
            "phase": "v670-v3",
            "error_type": type(exc).__name__,
            "error": str(exc),
            "canonical_invocations": 1,
            "canonical_successes": 0,
            "replay_allowed": False,
        }
        atomic_write(receipt, failure)
        raise
    atomic_write(receipt, result)
    print(json.dumps({"status": result["status"], "head": result["head"], "tests": result["tests"], "detailed_checks": result["detailed_checks"], "minimal_checks": result["minimal_checks"], "json": result["json"], "privacy": result["privacy"], "manifests": {key: value["entry_count"] for key, value in result["manifests"].items()}}, sort_keys=True))


if __name__ == "__main__":
    main()
