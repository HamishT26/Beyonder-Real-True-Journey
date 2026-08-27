#!/usr/bin/env python3
"""One-shot exact-final owner-scoped canonical validator for v673-v6."""

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
OWNER = "Vesper Arlen"
PHASE = "v673-v6"
BRANCH = "codex/GHC-Family/vesper-arlen-v673-v6-full-tools"
SOURCE_FINAL = "2400427269b28496acaa07cd6c18f5a2236510f7"
X1_COMMIT = "9a5d432a877d5c11ac60e0d331cf27cfb55c482b"
EVIDENCE_COMMIT = "5b208ceb2cababd14dd5de7e35af792533b12c68"
OUT_PREFIX = "docs/vesper-arlen/v673-v6/"
SELF_EXCLUSIONS = {
    "docs/vesper-arlen/v673-v6/validation/final-owner-manifest.json",
    "docs/vesper-arlen/v673-v6/validation/final-delta-manifest.json",
    "docs/vesper-arlen/v673-v6/validation/final-staged-review.json",
    "docs/vesper-arlen/v673-v6/validation/final-staged-privacy.json",
    "docs/vesper-arlen/v673-v6/seal/content-seal.json",
}


def git(*args: str) -> bytes:
    result = subprocess.run(["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if result.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.decode('utf-8', 'replace')}")
    return result.stdout


def git_text(*args: str) -> str:
    return git(*args).decode("utf-8")


def git_blob(commit: str, path: str) -> bytes:
    return git("show", f"{commit}:{path}")


def git_json(commit: str, path: str) -> Any:
    return json.loads(git_blob(commit, path).decode("utf-8"))


def normalized_sha256(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()


def owner_paths(commit: str) -> list[str]:
    paths = git_text("ls-tree", "-r", "--name-only", commit).splitlines()
    exact = {
        "ghc-family-index/references/v673-v6-vesper-arlen.md",
        "scripts/build_ghc_family_vesper_arlen_v673_v6_x1.py",
        "scripts/build_ghc_family_vesper_arlen_v673_v6_x2.py",
        "scripts/build_ghc_family_vesper_arlen_v673_v6_closeout.py",
        "scripts/ghc_family_sextant_contracts.py",
        "scripts/ghc_family_sextant_runners.py",
        "scripts/validate_ghc_family_vesper_arlen_v673_v6_final.py",
        "tests/test_ghc_family_vesper_arlen_v673_v6_x1.py",
        "tests/test_ghc_family_vesper_arlen_v673_v6_x2.py",
        "tests/test_ghc_family_vesper_arlen_v673_v6_final.py",
    }
    return sorted(path for path in paths if path.startswith(OUT_PREFIX) or path in exact)


def replay_manifest(commit: str, manifest_path: str, blob_commit: str | None = None) -> dict[str, Any]:
    manifest = git_json(commit, manifest_path)
    domain = blob_commit or commit
    failures = []
    for row in manifest["entries"]:
        try:
            data = git_blob(domain, row["path"])
        except RuntimeError as exc:
            failures.append({"path": row["path"], "error": str(exc)})
            continue
        actual = normalized_sha256(data)
        if actual != row["sha256_normalized_lf"] or len(data) != row["bytes"]:
            failures.append({"path": row["path"], "expected_sha256": row["sha256_normalized_lf"], "actual_sha256": actual, "expected_bytes": row["bytes"], "actual_bytes": len(data)})
    return {"path": manifest_path, "entry_count": manifest["entry_count"], "replayed": len(manifest["entries"]), "failures": failures, "passed": not failures}


PRIVACY_PATTERNS = {
    "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    "credential_or_secret_assignment": re.compile(r"(?i)\b(?:api[_-]?key|secret|access[_-]?token|password)\s*[:=]\s*['\"]?[A-Za-z0-9_./+-]{12,}"),
    "private_absolute_user_path": re.compile(r"(?i)\b[A-Z]:\\\\Users\\\\[^\\\s]+"),
    "private_callable_or_session_stream": re.compile(r"(?i)\b(?:source_thread_id|session_stream|private_callable_id)\b"),
    "raw_app_state_or_transcript": re.compile(r"(?i)\b(?:raw_app_state|private_transcript|conversation_export)\b"),
}


def privacy_scan(commit: str, paths: list[str]) -> dict[str, Any]:
    candidates, hits = [], []
    text_files = 0
    for path in paths:
        if Path(path).suffix.casefold() not in {".json", ".md", ".txt", ".html", ".py"}:
            continue
        text_files += 1
        text = git_blob(commit, path).decode("utf-8", "replace")
        for class_name, pattern in PRIVACY_PATTERNS.items():
            for match in pattern.finditer(text):
                row = {"path": path, "class": class_name, "offset": match.start(), "confirmed": True}
                window = text[max(0, match.start() - 180):match.end() + 180]
                if path.endswith(".py") and "re.compile" in window:
                    row.update({"confirmed": False, "classification": "scanner_definition"})
                    candidates.append(row)
                else:
                    hits.append(row)
    return {"classes": sorted(PRIVACY_PATTERNS), "text_files": text_files, "scanner_definition_candidates": candidates, "confirmed_hits": hits, "confirmed_hit_count": len(hits), "passed": not hits}


def ast_scan(commit: str, paths: list[str]) -> dict[str, Any]:
    findings = []
    scanned = 0
    for path in paths:
        if not path.endswith(".py"):
            continue
        scanned += 1
        tree = ast.parse(git_blob(commit, path).decode("utf-8"), filename=path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                name = ""
                if isinstance(node.func, ast.Name):
                    name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    name = f"{getattr(node.func.value, 'id', '')}.{node.func.attr}"
                if name in {"eval", "exec", "os.system"}:
                    findings.append({"path": path, "line": node.lineno, "rule": "dynamic_or_shell_execution", "name": name})
                if any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords):
                    findings.append({"path": path, "line": node.lineno, "rule": "subprocess_shell_true"})
            if isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                value = node.value
                for target in targets:
                    if isinstance(target, ast.Name) and target.id.casefold() in {"password", "secret", "access_token", "api_key"} and isinstance(value, ast.Constant) and isinstance(value.value, str) and value.value:
                        findings.append({"path": path, "line": node.lineno, "rule": "hardcoded_sensitive_assignment", "name": target.id})
    return {"python_files": scanned, "findings": findings, "finding_count": len(findings), "passed": not findings, "exhaustive_security": False}


def strict_json_scan(commit: str, paths: list[str]) -> dict[str, Any]:
    failures = []
    parsed = 0
    for path in paths:
        if not path.endswith(".json"):
            continue
        try:
            json.loads(git_blob(commit, path).decode("utf-8"))
            parsed += 1
        except Exception as exc:  # exact receipt, no recovery credit
            failures.append({"path": path, "error": str(exc)})
    return {"parsed": parsed, "failures": failures, "passed": not failures}


def run_tests(toolbank: Path) -> dict[str, Any]:
    env = dict(os.environ)
    env["VESPER_V6736_TOOLBANK"] = str(toolbank)
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "tests/test_ghc_family_vesper_arlen_v673_v6_x1.py", "tests/test_ghc_family_vesper_arlen_v673_v6_x2.py", "tests/test_ghc_family_vesper_arlen_v673_v6_final.py"],
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        text=True,
        encoding="utf-8",
    )
    match = re.search(r"(\d+) passed", result.stdout)
    return {"returncode": result.returncode, "passed_count": int(match.group(1)) if match else 0, "output_tail": result.stdout[-4000:], "passed": result.returncode == 0 and match is not None}


def fresh_equality(expected_head: str) -> dict[str, Any]:
    upstream = git_text("rev-parse", "@{u}").strip()
    tracking = git_text("rev-parse", f"refs/remotes/origin/{BRANCH}").strip()
    live_lines = git_text("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}").splitlines()
    live = live_lines[0].split()[0] if len(live_lines) == 1 else None
    divergence = git_text("rev-list", "--left-right", "--count", "HEAD...@{u}").strip()
    return {"local": expected_head, "upstream": upstream, "tracking": tracking, "fresh_live": live, "divergence": divergence, "passed": expected_head == upstream == tracking == live and divergence.replace("\t", " ") == "0 0"}


def load_toolbank(path: Path) -> dict[str, Any]:
    resolved = path.resolve()
    if resolved.drive.upper() != "D:":
        raise RuntimeError("toolbank is not D-isolated")
    site = resolved / "site-packages"
    if not site.is_dir():
        raise RuntimeError("toolbank site-packages missing")
    sys.path.insert(0, str(site))
    import importlib.metadata as metadata

    versions = {name: metadata.version(name) for name in ("rfc8785", "jsonpath-ng", "treelib", "six")}
    expected = {"rfc8785": "0.1.4", "jsonpath-ng": "1.8.0", "treelib": "1.8.0", "six": "1.17.0"}
    if versions != expected:
        raise RuntimeError(f"tool versions differ: {versions}")
    return {"resolved": resolved, "versions": versions}


def preflight(args: argparse.Namespace) -> int:
    tool = load_toolbank(Path(args.toolbank))
    receipt = Path(args.receipt_dir).resolve()
    checks = {
        "receipt_absent": not receipt.exists(),
        "receipt_parent_exists": receipt.parent.is_dir(),
        "receipt_parent_d_drive": receipt.drive.upper() == "D:",
        "branch_exact": git_text("branch", "--show-current").strip() == BRANCH,
        "head_is_evidence_before_final_commit": git_text("rev-parse", "HEAD").strip() == EVIDENCE_COMMIT,
        "tool_versions_exact": tool["versions"] == {"rfc8785": "0.1.4", "jsonpath-ng": "1.8.0", "treelib": "1.8.0", "six": "1.17.0"},
        "validator_test_present": (ROOT / "tests" / "test_ghc_family_vesper_arlen_v673_v6_final.py").is_file(),
        "final_manifest_staged": (ROOT / "docs" / "vesper-arlen" / "v673-v6" / "validation" / "final-owner-manifest.json").is_file(),
    }
    payload = {"mode": "dependency_preflight_only", "checks": checks, "passed": all(checks.values()), "canonical_invoked": False, "receipt_written": False}
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["passed"] else 1


def validate(args: argparse.Namespace) -> int:
    if not re.fullmatch(r"[0-9a-f]{40}", args.expected_head):
        raise RuntimeError("expected head must be an exact forty-hex commit")
    tool = load_toolbank(Path(args.toolbank))
    receipt_dir = Path(args.receipt_dir).resolve()
    if receipt_dir.exists():
        raise RuntimeError("one-shot receipt latch already exists; canonical replay refused")
    if receipt_dir.drive.upper() != "D:" or not receipt_dir.parent.is_dir():
        raise RuntimeError("receipt directory must be a new child of an existing D-drive parent")
    receipt_dir.mkdir()
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    expected = args.expected_head
    checks: dict[str, bool] = {}
    payload: dict[str, Any] = {
        "owner": OWNER,
        "phase": PHASE,
        "canonical_invocations": 1,
        "replayed": False,
        "started_utc": started,
        "expected_head": expected,
        "receipt_directory": "D-isolated external bank; absolute path withheld",
        "full_repository_suite": False,
        "independent_reproduction": False,
    }
    try:
        head = git_text("rev-parse", "HEAD").strip()
        clean_before = git_text("status", "--porcelain") == ""
        branch = git_text("branch", "--show-current").strip()
        commits = int(git_text("rev-list", "--count", f"{SOURCE_FINAL}..{head}").strip())
        merges = int(git_text("rev-list", "--merges", "--count", f"{SOURCE_FINAL}..{head}").strip())
        final_parents = git_text("rev-list", "--parents", "--max-count=1", head).split()
        checks.update({
            "exact_head": head == expected,
            "clean_before": clean_before,
            "branch_exact": branch == BRANCH,
            "three_phase_commits": commits == 3,
            "zero_merges": merges == 0,
            "final_one_parent": len(final_parents) == 2,
            "final_direct_child_of_evidence": len(final_parents) == 2 and final_parents[1] == EVIDENCE_COMMIT,
            "evidence_direct_child_of_x1": git_text("rev-parse", f"{EVIDENCE_COMMIT}^").strip() == X1_COMMIT,
            "x1_direct_child_of_source": git_text("rev-parse", f"{X1_COMMIT}^").strip() == SOURCE_FINAL,
        })
        paths = owner_paths(head)
        json_result = strict_json_scan(head, paths)
        privacy_result = privacy_scan(head, paths)
        ast_result = ast_scan(head, paths)
        x1_manifest = replay_manifest(X1_COMMIT, "docs/vesper-arlen/v673-v6/validation/x1-manifest.json", X1_COMMIT)
        evidence_manifest = replay_manifest(EVIDENCE_COMMIT, "docs/vesper-arlen/v673-v6/validation/evidence-manifest.json", EVIDENCE_COMMIT)
        owner_manifest = replay_manifest(head, "docs/vesper-arlen/v673-v6/validation/final-owner-manifest.json", head)
        delta_manifest = replay_manifest(head, "docs/vesper-arlen/v673-v6/validation/final-delta-manifest.json", head)
        content_seal = replay_manifest(head, "docs/vesper-arlen/v673-v6/seal/content-seal.json", head)
        declared_owner = git_json(head, "docs/vesper-arlen/v673-v6/validation/final-owner-manifest.json")
        route = git_json(head, "docs/vesper-arlen/v673-v6/route/route-state.json")
        handoff = git_blob(head, "docs/vesper-arlen/v673-v6/handoffs/lyren-moss-v673-v7-activation-candidate.md").decode("utf-8")
        handoff_words = len(re.findall(r"\b\S+\b", handoff))
        stale_label = "Vesper Row" + "an"
        stale_hits = [path for path in paths if stale_label in git_blob(head, path).decode("utf-8", "replace")]
        tests = run_tests(tool["resolved"])
        equality = fresh_equality(head)
        clean_after = git_text("status", "--porcelain") == ""
        checks.update({
            "owner_file_ceiling": 0 < len(paths) < 2000,
            "strict_json": json_result["passed"],
            "privacy_zero_confirmed": privacy_result["passed"],
            "bounded_ast_zero_findings": ast_result["passed"],
            "x1_manifest": x1_manifest["passed"],
            "evidence_manifest": evidence_manifest["passed"],
            "final_owner_manifest": owner_manifest["passed"],
            "final_delta_manifest": delta_manifest["passed"],
            "content_seal": content_seal["passed"],
            "owner_manifest_path_parity": declared_owner["owner_path_count"] == len(paths) and declared_owner["entry_count"] + len(declared_owner["self_exclusions"]) == len(paths),
            "selected_owner_tests": tests["passed"],
            "handoff_word_range": 10000 <= handoff_words <= 100000,
            "route_prepared_not_sent": route["state"] == "PREPARED_NOT_SENT" and route["sent_by_vesper_arlen"] is False and route["precontact_performed"] is False,
            "no_stale_owner_label": not stale_hits,
            "fresh_four_way_equality": equality["passed"],
            "clean_after": clean_after,
        })
        payload.update({
            "head": head,
            "branch": branch,
            "history": {"source": SOURCE_FINAL, "x1": X1_COMMIT, "evidence": EVIDENCE_COMMIT, "final": head, "phase_commits": commits, "merges": merges, "final_parent": final_parents[1:]},
            "checks": checks,
            "check_count": len(checks),
            "check_passed": sum(checks.values()),
            "tests": tests,
            "json": json_result,
            "privacy": privacy_result,
            "ast_security": ast_result,
            "manifests": {"x1": x1_manifest, "evidence": evidence_manifest, "owner": owner_manifest, "delta": delta_manifest, "content_seal": content_seal},
            "owner_files": len(paths),
            "owner_manifest_entries": declared_owner["entry_count"],
            "owner_manifest_self_exclusions": len(declared_owner["self_exclusions"]),
            "handoff_words": handoff_words,
            "stale_label_hits": stale_hits,
            "remote_equality": equality,
            "clean_before": clean_before,
            "clean_after": clean_after,
            "tool_versions": tool["versions"],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" if all(checks.values()) else "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
            "finished_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        })
    except Exception as exc:
        payload.update({"checks": checks, "status": "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL", "exception": f"{type(exc).__name__}: {exc}", "finished_utc": dt.datetime.now(dt.timezone.utc).isoformat(), "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    canonical_bytes = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    canonical_sha = hashlib.sha256(canonical_bytes).hexdigest()
    receipt = {
        "owner": OWNER,
        "phase": PHASE,
        "status": payload["status"],
        "canonical_payload_sha256": canonical_sha,
        "canonical_invocations": 1,
        "replayed": False,
        "expected_head": args.expected_head,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "same_owner": True,
        "independent_reproduction": False,
    }
    (receipt_dir / "canonical-payload.json").write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    (receipt_dir / "canonical-receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if payload["status"] == "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--toolbank", required=True)
    parser.add_argument("--receipt-dir", required=True)
    parser.add_argument("--expected-head")
    parser.add_argument("--preflight", action="store_true")
    args = parser.parse_args()
    if args.preflight:
        return preflight(args)
    if not args.expected_head:
        parser.error("--expected-head is required for the one-shot canonical invocation")
    return validate(args)


if __name__ == "__main__":
    raise SystemExit(main())
