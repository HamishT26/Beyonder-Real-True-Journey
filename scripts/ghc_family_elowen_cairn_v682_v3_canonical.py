"""Exclusive exact-final owner-scoped canonical validator for Elowen Cairn v682-v3."""

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

from scripts.ghc_family_privacy_candidate_adjudication import scan_text_items


ROOT = Path(__file__).resolve().parents[1]
BRANCH = "codex/GHC-Family/elowen-cairn-v682-v3-full-tools"
SOURCE = "ed63ba1080cbb0a69701e56fd9bee9c80221a709"
X1 = "607c6742f44e2dbd3d7d66bf20348ad3ffe8bcfb"
EVIDENCE = "743bdbcf879dd600f05e5cbea645e00557cbbf85"
REMOTE_REF = f"refs/heads/{BRANCH}"


def run(args: list[str], *, check: bool = True, text: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        args,
        cwd=ROOT,
        check=check,
        capture_output=True,
        text=text,
        encoding="utf-8" if text else None,
    )


def git_text(*args: str) -> str:
    return run(["git", *args]).stdout.strip()


def git_blob(commit: str, path: str) -> bytes:
    return run(["git", "show", f"{commit}:{path}"], text=False).stdout


def load_git_json(commit: str, path: str) -> Any:
    return json.loads(git_blob(commit, path).decode("utf-8"))


def replay_manifest(commit: str, path: str) -> dict[str, Any]:
    manifest = load_git_json(commit, path)
    failures: list[dict[str, str]] = []
    for entry in manifest["entries"]:
        data = git_blob(commit, entry["path"])
        if len(data) != entry["bytes"]:
            failures.append({"path": entry["path"], "reason": "byte_count"})
        if hashlib.sha256(data).hexdigest() != entry["sha256"]:
            failures.append({"path": entry["path"], "reason": "sha256"})
    return {
        "declared_self_exclusions": len(manifest["declared_self_exclusions"]),
        "entry_count": manifest["entry_count"],
        "failure_count": len(failures),
        "failures": failures,
        "path": path,
        "valid": not failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    receipt = args.receipt.resolve()
    if receipt.exists():
        print(json.dumps({"status": "REFUSED_EXISTING_CANONICAL_RECEIPT"}, separators=(",", ":")))
        return 2
    receipt.parent.mkdir(parents=True, exist_ok=True)

    head = git_text("rev-parse", "HEAD")
    branch = git_text("branch", "--show-current")
    upstream = git_text("rev-parse", "@{upstream}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_line = git_text("ls-remote", "--heads", "origin", BRANCH)
    live = live_line.split()[0] if live_line else ""
    status_before = git_text("status", "--porcelain=v1", "--untracked-files=all")
    divergence = git_text("rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()

    final_tests = run(
        [
            sys.executable,
            "-X",
            "utf8",
            "-m",
            "unittest",
            "tests.test_ghc_family_elowen_cairn_v682_v3_final",
            "-q",
        ],
        check=False,
    )
    final_test_success = final_tests.returncode == 0

    manifests = {
        "x1": replay_manifest(X1, "docs/elowen-cairn/v682-v3/validation/x1-index-manifest.json"),
        "evidence": replay_manifest(EVIDENCE, "docs/elowen-cairn/v682-v3/validation/evidence-index-manifest.json"),
        "final_delta": replay_manifest(head, "docs/elowen-cairn/v682-v3/validation/final-delta-manifest.json"),
        "final_owner": replay_manifest(head, "docs/elowen-cairn/v682-v3/validation/final-owner-manifest.json"),
    }
    owner_manifest = load_git_json(head, "docs/elowen-cairn/v682-v3/validation/final-owner-manifest.json")
    owner_paths = sorted(
        {row["path"] for row in owner_manifest["entries"]}
        | set(owner_manifest["declared_self_exclusions"])
    )
    json_paths = [path for path in owner_paths if path.endswith(".json")]
    json_failures: list[str] = []
    for path in json_paths:
        try:
            json.loads(git_blob(head, path).decode("utf-8"))
        except Exception:
            json_failures.append(path)

    python_paths = [path for path in owner_paths if path.endswith(".py")]
    ast_failures: list[str] = []
    security_findings: list[dict[str, str]] = []
    risky_calls = {"eval", "exec", "compile", "__import__"}
    for path in python_paths:
        try:
            tree = ast.parse(git_blob(head, path).decode("utf-8"), filename=path)
        except Exception:
            ast_failures.append(path)
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in risky_calls:
                security_findings.append({"path": path, "call": node.func.id})

    markdown_paths = [path for path in owner_paths if path.endswith(".md")]
    markdown_failures: list[str] = []
    for path in markdown_paths:
        text = git_blob(head, path).decode("utf-8")
        if not text.strip() or ("SKILL.md" not in path and not text.lstrip().startswith("#")):
            markdown_failures.append(path)
    yaml_paths = [path for path in owner_paths if path.endswith((".yaml", ".yml"))]
    yaml_failures: list[str] = []
    for path in yaml_paths:
        text = git_blob(head, path).decode("utf-8")
        if "interface:" not in text or "display_name:" not in text:
            yaml_failures.append(path)
    html_paths = [path for path in owner_paths if path.endswith(".html")]
    html_failures: list[str] = []
    for path in html_paths:
        text = git_blob(head, path).decode("utf-8").lower()
        if not all(token in text for token in ('<html lang="en">', "<main", "<h1", "<table", "skip to main")):
            html_failures.append(path)

    privacy = scan_text_items(
        (path, git_blob(head, path).decode("utf-8"))
        for path in owner_paths
        if Path(path).suffix.lower() in {".json", ".md", ".py", ".yaml", ".yml", ".html"}
    )
    privacy_candidates = privacy["candidates"]
    confirmed_privacy_hits = privacy["confirmed_hits"]

    oversized: list[dict[str, Any]] = []
    maximum_words = 0
    maximum_word_path = ""
    for path in owner_paths:
        if Path(path).suffix.lower() not in {".json", ".md", ".py", ".yaml", ".yml", ".html"}:
            continue
        words = len(git_blob(head, path).decode("utf-8").split())
        if words > maximum_words:
            maximum_words = words
            maximum_word_path = path
        if words > 100000:
            oversized.append({"path": path, "words": words})

    seal = load_git_json(head, "docs/elowen-cairn/v682-v3/closeout/content-seal.json")
    seal_failures: list[str] = []
    for entry in seal["targets"]:
        data = git_blob(head, entry["path"])
        if len(data) != entry["bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
            seal_failures.append(entry["path"])

    source_to_final = git_text("rev-list", "--reverse", f"{SOURCE}..{head}").splitlines()
    merges = git_text("rev-list", "--merges", f"{SOURCE}..{head}").splitlines()
    direct_edges = {
        "x1_parent_source": git_text("rev-parse", f"{X1}^") == SOURCE,
        "evidence_parent_x1": git_text("rev-parse", f"{EVIDENCE}^") == X1,
        "final_parent_evidence": git_text("rev-parse", "HEAD^") == EVIDENCE,
    }
    final_parent_count = len(git_text("show", "-s", "--format=%P", "HEAD").split())

    status_after = git_text("status", "--porcelain=v1", "--untracked-files=all")
    upstream_after = git_text("rev-parse", "@{upstream}")
    tracking_after = git_text("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_after_line = git_text("ls-remote", "--heads", "origin", BRANCH)
    live_after = live_after_line.split()[0] if live_after_line else ""
    divergence_after = git_text("rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()

    checks = {
        "ast_valid": not ast_failures,
        "bounded_security_findings_zero": not security_findings,
        "branch_exact": branch == BRANCH,
        "clean_after": status_after == "",
        "clean_before": status_before == "",
        "commit_count_three": len(source_to_final) == 3,
        "direct_edges": all(direct_edges.values()),
        "divergence_after_zero": divergence_after == ["0", "0"],
        "divergence_before_zero": divergence == ["0", "0"],
        "final_parent_one": final_parent_count == 1,
        "final_tests": final_test_success,
        "four_way_after": head == upstream_after == tracking_after == live_after,
        "four_way_before": head == upstream == tracking == live,
        "html_structural_checks": not html_failures,
        "json_parses": not json_failures,
        "manifest_replays": all(row["valid"] for row in manifests.values()),
        "markdown_structures": not markdown_failures,
        "owner_file_ceiling": len(owner_paths) < 2000,
        "privacy_confirmed_hits_zero": not confirmed_privacy_hits,
        "seal_replays": not seal_failures,
        "word_ceiling": not oversized,
        "yaml_structures": not yaml_failures,
        "zero_merges": not merges,
    }
    payload = {
        "canonical_invocation_count": 1,
        "canonical_replay_count": 0,
        "canonical_success_count": 1 if all(checks.values()) else 0,
        "checks": checks,
        "counts": {
            "ast_checks": len(python_paths),
            "detailed_checks": len(checks),
            "final_owner_tests": 16 if final_test_success else 0,
            "html_checks": len(html_paths),
            "json_parses": len(json_paths),
            "manifest_entries": sum(row["entry_count"] for row in manifests.values()),
            "markdown_checks": len(markdown_paths),
            "owner_files": len(owner_paths),
            "privacy_candidates": len(privacy_candidates),
            "privacy_confirmed_hits": len(confirmed_privacy_hits),
            "seal_targets": seal["target_count"],
            "security_findings": len(security_findings),
            "yaml_checks": len(yaml_paths),
        },
        "direct_edges": direct_edges,
        "head": head,
        "manifests": manifests,
        "maximum_document_words": maximum_words,
        "maximum_document_path": maximum_word_path,
        "owner": "Elowen Cairn",
        "phase": "v682-v3",
        "same_owner_not_independent_reproduction": True,
        "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" if all(checks.values()) else "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    payload_bytes = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    receipt_payload = {**payload, "payload_sha256": hashlib.sha256(payload_bytes).hexdigest()}
    receipt.write_text(json.dumps(receipt_payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({
        "checks_passed": sum(1 for value in checks.values() if value),
        "checks_total": len(checks),
        "head": head,
        "payload_sha256": receipt_payload["payload_sha256"],
        "status": receipt_payload["status"],
    }, separators=(",", ":")))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
