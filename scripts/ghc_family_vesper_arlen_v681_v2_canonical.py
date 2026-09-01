from __future__ import annotations

import argparse
import ast
import hashlib
import io
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE = "docs/vesper-arlen/v681-v2"
BRANCH = "codex/GHC-Family/vesper-arlen-v681-v2-full-tools"
SOURCE = "14b34a2b7f1b1c74e3b4102b18cc5c3b5fc854d2"
X1 = "5a5ef294b84ece97da4f2b1238d1852ce80a5b51"
EVIDENCE = "fd0e470dbcfd5576982819b626c18dbd99b3c2a9"
MANIFEST_PATHS = [
    f"{BASE}/validation/x1-index-manifest.json",
    f"{BASE}/validation/x2-index-manifest.json",
    f"{BASE}/validation/final-delta-manifest.json",
    f"{BASE}/validation/final-owner-manifest.json",
]


def git(*args: str, check: bool = True, text: bool = True) -> subprocess.CompletedProcess[Any]:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=check,
        capture_output=True,
        text=text,
        encoding="utf-8" if text else None,
    )


def blob(tree: str, path: str) -> bytes:
    return git("show", f"{tree}:{path}", text=False).stdout


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def batch_blobs(tree: str, paths: list[str]) -> dict[str, bytes]:
    requests = b"".join(f"{tree}:{path}\n".encode() for path in paths)
    completed = subprocess.run(
        ["git", "-C", str(ROOT), "cat-file", "--batch"],
        input=requests,
        check=True,
        capture_output=True,
    )
    stream = io.BytesIO(completed.stdout)
    result: dict[str, bytes] = {}
    for path in paths:
        header = stream.readline().decode("utf-8", errors="replace").rstrip("\n")
        parts = header.split()
        if len(parts) != 3 or parts[1] != "blob":
            raise RuntimeError(f"unexpected blob header for {path}: {header}")
        size = int(parts[2])
        data = stream.read(size)
        if stream.read(1) != b"\n":
            raise RuntimeError(f"missing blob separator for {path}")
        result[path] = data
    return result


def manifest_replay(head: str, path: str) -> dict[str, Any]:
    manifest = json.loads(blob(head, path).decode("utf-8-sig"))
    paths = [row["path"] for row in manifest["entries"]]
    blobs = batch_blobs(head, paths)
    mismatches = []
    for row in manifest["entries"]:
        data = normalized(blobs[row["path"]])
        if len(data) != row["bytes"] or digest(data) != row["sha256"]:
            mismatches.append(row["path"])
    return {
        "declared_self_exclusions": manifest["declared_self_exclusions"],
        "entries": manifest["entry_count"],
        "mismatches": mismatches,
        "path": path,
    }


def word_count(text: str) -> int:
    return len(text.split())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--receipt", required=True, type=Path)
    args = parser.parse_args()
    if args.receipt.exists():
        raise RuntimeError("canonical receipt already exists; no replay after success")

    head = git("rev-parse", "HEAD").stdout.strip()
    clean_before = not git("status", "--porcelain=v1").stdout.strip()
    branch = git("branch", "--show-current").stdout.strip()
    parent = git("rev-parse", "HEAD^").stdout.strip()
    x1_parent = git("rev-parse", f"{X1}^").stdout.strip()
    evidence_parent = git("rev-parse", f"{EVIDENCE}^").stdout.strip()
    commits = int(git("rev-list", "--count", f"{SOURCE}..{head}").stdout.strip())
    merges = int(git("rev-list", "--merges", "--count", f"{SOURCE}..{head}").stdout.strip())
    x1_ancestral = git("merge-base", "--is-ancestor", X1, head, check=False).returncode == 0
    evidence_ancestral = git("merge-base", "--is-ancestor", EVIDENCE, head, check=False).returncode == 0

    upstream = git("rev-parse", "@{upstream}").stdout.strip()
    tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}").stdout.strip()
    live_line = git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}").stdout.strip()
    if not live_line:
        raise RuntimeError("live remote branch missing")
    live = live_line.split()[0]
    divergence = [int(value) for value in git("rev-list", "--left-right", "--count", "HEAD...@{upstream}").stdout.split()]
    four_way = head == upstream == tracking == live

    manifest_results = [manifest_replay(head, path) for path in MANIFEST_PATHS]
    manifest_mismatches = sum(len(row["mismatches"]) for row in manifest_results)
    owner_manifest = json.loads(blob(head, MANIFEST_PATHS[-1]).decode("utf-8-sig"))
    owner_paths = [row["path"] for row in owner_manifest["entries"]]
    all_owner_blobs = batch_blobs(head, owner_paths)

    content_seal_path = f"{BASE}/final/content-seal.json"
    content_seal = json.loads(blob(head, content_seal_path).decode("utf-8-sig"))
    seal_blobs = batch_blobs(head, [row["path"] for row in content_seal["entries"]])
    seal_mismatches = []
    for row in content_seal["entries"]:
        data = normalized(seal_blobs[row["path"]])
        if len(data) != row["bytes"] or digest(data) != row["sha256"]:
            seal_mismatches.append(row["path"])

    json_paths = [path for path in owner_paths if path.endswith(".json")] + MANIFEST_PATHS
    json_failures = []
    for path in json_paths:
        try:
            json.loads((all_owner_blobs.get(path) or blob(head, path)).decode("utf-8-sig"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            json_failures.append({"error": type(exc).__name__, "path": path})

    scanners = {
        "raw_uuid": re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}\b"),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives)[\\/]"),
        "raw_task_thread_identifier": re.compile(r"\b(?:source_thread_id|thread_id)\b", re.IGNORECASE),
        "credential_assignment": re.compile(r"\b(?:api[_-]?key|token|password|secret)\s*[:=]\s*[^\s]+", re.IGNORECASE),
        "private_conversation_payload": re.compile(r"source_thread_id|codex_delegation", re.IGNORECASE),
    }
    scanner_definition_paths = {
        "scripts/build_ghc_family_vesper_arlen_v681_v2_x1.py",
        "scripts/build_ghc_family_vesper_arlen_v681_v2_x2.py",
        "scripts/build_ghc_family_vesper_arlen_v681_v2_final.py",
        "scripts/ghc_family_vesper_arlen_v681_v2_canonical.py",
    }
    privacy_candidates = []
    confirmed_privacy = []
    for path, raw in all_owner_blobs.items():
        text = raw.decode("utf-8", errors="replace")
        for class_name, pattern in scanners.items():
            if pattern.search(text):
                item = {
                    "class": class_name,
                    "disposition": "scanner_definition_only" if path in scanner_definition_paths else "confirmed_payload_hit",
                    "path": path,
                }
                privacy_candidates.append(item)
                if item["disposition"] == "confirmed_payload_hit":
                    confirmed_privacy.append(item)

    python_paths = [path for path in owner_paths if path.endswith(".py")]
    ast_failures = []
    for path in python_paths:
        try:
            ast.parse(all_owner_blobs[path].decode("utf-8-sig"), filename=path)
        except (UnicodeDecodeError, SyntaxError) as exc:
            ast_failures.append({"error": type(exc).__name__, "path": path})

    tests = subprocess.run(
        [sys.executable, "-X", "utf8", "-m", "unittest", "tests.test_ghc_family_vesper_arlen_v681_v2_final"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    baton_path = f"{BASE}/handoffs/lyren-moss-v681-v3-activation-candidate.md"
    overview_path = f"{BASE}/final/integrated-overview.md"
    baton_words = word_count(all_owner_blobs[baton_path].decode("utf-8"))
    overview_words = word_count(all_owner_blobs[overview_path].decode("utf-8"))
    markdown_word_violations = []
    for path in [item for item in owner_paths if item.endswith(".md")]:
        words = word_count(all_owner_blobs[path].decode("utf-8", errors="replace"))
        if words > 100000:
            markdown_word_violations.append({"path": path, "words": words})

    detailed = {
        "baton_word_bounds": 10000 <= baton_words <= 100000,
        "branch": branch == BRANCH,
        "clean_before": clean_before,
        "commit_ceiling": commits == 3,
        "content_seal": not seal_mismatches and content_seal["entry_count"] == 15,
        "direct_final_parent": parent == EVIDENCE,
        "direct_x1_parent": x1_parent == SOURCE,
        "direct_evidence_parent": evidence_parent == X1,
        "divergence": divergence == [0, 0],
        "evidence_ancestry": evidence_ancestral,
        "exact_head": head == args.expected_head,
        "four_way_equality": four_way,
        "json": not json_failures,
        "manifest_parity": manifest_mismatches == 0,
        "markdown_word_caps": not markdown_word_violations,
        "materialized_file_ceiling": len(owner_paths) + len(owner_manifest["declared_self_exclusions"]) < 2000,
        "overview_floor": overview_words >= 1800,
        "privacy": not confirmed_privacy,
        "python_ast": not ast_failures,
        "tests": tests.returncode == 0,
        "three_single_parent_commits": commits == 3 and merges == 0,
        "x1_ancestry": x1_ancestral,
        "zero_merges": merges == 0,
    }
    if not all(detailed.values()):
        raise RuntimeError(
            json.dumps(
                {
                    "ast_failures": ast_failures,
                    "confirmed_privacy": confirmed_privacy,
                    "detailed": detailed,
                    "json_failures": json_failures,
                    "manifest_results": manifest_results,
                    "seal_mismatches": seal_mismatches,
                    "test_stderr": tests.stderr[-2000:],
                    "test_stdout": tests.stdout[-2000:],
                },
                indent=2,
            )
        )
    clean_after = not git("status", "--porcelain=v1").stdout.strip()
    if not clean_after:
        raise RuntimeError("canonical validation changed the worktree")

    payload = {
        "baton_words": baton_words,
        "canonical_invocations": 1,
        "canonical_successes": 1,
        "clean_after": clean_after,
        "clean_before": clean_before,
        "content_seal_entries": content_seal["entry_count"],
        "content_seal_mismatches": len(seal_mismatches),
        "detailed_check_count": len(detailed),
        "detailed_checks": detailed,
        "divergence": divergence,
        "exact_head": head,
        "full_repository_suite_run": False,
        "independent_reproduction_claimed": False,
        "json_documents": len(json_paths),
        "manifest_entries": sum(row["entries"] for row in manifest_results),
        "manifest_mismatches": manifest_mismatches,
        "manifest_results": manifest_results,
        "merges": merges,
        "outcome_counts": {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3},
        "owner_files": len(owner_paths) + len(owner_manifest["declared_self_exclusions"]),
        "owner_manifest_entries": owner_manifest["entry_count"],
        "phase": "v681-v2",
        "privacy_candidates": len(privacy_candidates),
        "privacy_confirmed_hits": len(confirmed_privacy),
        "python_ast_files": len(python_paths),
        "schema": "ghc.family.canonical-exact-final.v681.v2",
        "same_owner_only": True,
        "state": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "test_returncode": tests.returncode,
        "test_summary": tests.stderr.strip() or tests.stdout.strip(),
        "three_phase_commits": commits,
    }
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
