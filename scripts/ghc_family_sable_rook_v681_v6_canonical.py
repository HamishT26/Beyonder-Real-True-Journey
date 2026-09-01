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
BASE = "docs/sable-rook/v681-v6"
BRANCH = "codex/GHC-Family/sable-rook-v681-v6-full-tools"
SOURCE = "2a0210a495cbe557158095505671d599e0c33159"
X1 = "7285d38579cdf5e2fce3c6b0b013b49e940f44b5"
EVIDENCE = "7fe9cd2c6c487a7b871ab96ad9b635ea3a8580ba"
MANIFEST_PATHS = [
    f"{BASE}/validation/x1-index-manifest.json",
    f"{BASE}/validation/x2-index-manifest.json",
    f"{BASE}/validation/final-delta-manifest.json",
    f"{BASE}/validation/final-owner-manifest.json",
]
EXPECTED_COUNTS = {
    "effective_negatives": 54528,
    "effective_methods": 62915,
    "failed_witnesses": 26189,
    "bounded_passing_witnesses": 44737,
    "open_gaps": 482,
    "exact_gates": 473,
}
EXPECTED_OUTCOMES = {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}


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
    if not paths:
        return {}
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
        "declared_self_exclusions": manifest.get("declared_self_exclusions", []),
        "entries": manifest["entry_count"],
        "mismatches": mismatches,
        "path": path,
    }


def words(text: str) -> int:
    return len(text.split())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--receipt", required=True, type=Path)
    args = parser.parse_args()

    receipt = args.receipt.resolve()
    if receipt == ROOT.resolve() or ROOT.resolve() in receipt.parents:
        raise RuntimeError("canonical receipt must remain external to the repository")
    if receipt.exists():
        raise RuntimeError("canonical receipt already exists; no replay after success")
    if not re.fullmatch(r"[0-9a-f]{40}", args.expected_head):
        raise RuntimeError("expected head must be one exact lowercase Git object id")

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
        raise RuntimeError("fresh live remote branch is absent")
    live = live_line.split()[0]
    divergence = [
        int(value)
        for value in git("rev-list", "--left-right", "--count", "HEAD...@{upstream}").stdout.split()
    ]
    four_way = head == upstream == tracking == live

    manifest_results = [manifest_replay(head, path) for path in MANIFEST_PATHS]
    manifest_mismatches = sum(len(row["mismatches"]) for row in manifest_results)
    owner_manifest = json.loads(blob(head, MANIFEST_PATHS[-1]).decode("utf-8-sig"))
    final_delta_manifest = json.loads(blob(head, MANIFEST_PATHS[-2]).decode("utf-8-sig"))
    owner_paths = [row["path"] for row in owner_manifest["entries"]]
    owner_exclusions = owner_manifest["declared_self_exclusions"]
    bounded_owner_paths = sorted(set(owner_paths) | set(owner_exclusions))
    owner_blobs = batch_blobs(head, bounded_owner_paths)

    content_seal_path = f"{BASE}/final/content-seal.json"
    content_seal = json.loads(blob(head, content_seal_path).decode("utf-8-sig"))
    seal_paths = [row["path"] for row in content_seal["entries"]]
    seal_blobs = batch_blobs(head, seal_paths)
    seal_mismatches = []
    for row in content_seal["entries"]:
        data = normalized(seal_blobs[row["path"]])
        if len(data) != row["bytes"] or digest(data) != row["sha256"]:
            seal_mismatches.append(row["path"])

    json_paths = sorted(path for path in bounded_owner_paths if path.endswith(".json"))
    json_failures = []
    for path in json_paths:
        try:
            json.loads(owner_blobs[path].decode("utf-8-sig"))
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
        "scripts/build_ghc_family_sable_rook_v681_v6_x1.py",
        "scripts/build_ghc_family_sable_rook_v681_v6_x2.py",
        "scripts/build_ghc_family_sable_rook_v681_v6_final.py",
        "scripts/ghc_family_sable_rook_v681_v6_canonical.py",
    }
    privacy_candidates = []
    confirmed_privacy = []
    for path, raw in owner_blobs.items():
        text = raw.decode("utf-8", errors="replace")
        for class_name, pattern in scanners.items():
            if pattern.search(text):
                item = {
                    "class": class_name,
                    "disposition": (
                        "scanner_definition_only"
                        if path in scanner_definition_paths
                        else "confirmed_payload_hit"
                    ),
                    "path": path,
                }
                privacy_candidates.append(item)
                if item["disposition"] == "confirmed_payload_hit":
                    confirmed_privacy.append(item)

    python_paths = sorted(path for path in owner_paths if path.endswith(".py"))
    ast_failures = []
    for path in python_paths:
        try:
            ast.parse(owner_blobs[path].decode("utf-8-sig"), filename=path)
        except (UnicodeDecodeError, SyntaxError) as exc:
            ast_failures.append({"error": type(exc).__name__, "path": path})

    ruff_paths = sorted(
        row["path"] for row in final_delta_manifest["entries"] if row["path"].endswith(".py")
    )
    ruff = subprocess.run(
        [sys.executable, "-m", "ruff", "check", *ruff_paths],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    tests = subprocess.run(
        [
            sys.executable,
            "-X",
            "utf8",
            "-m",
            "unittest",
            "-v",
            "tests.test_ghc_family_sable_rook_v681_v6_final",
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    baton_path = f"{BASE}/handoffs/caelen-ash-v681-v7-activation-candidate.md"
    overview_path = f"{BASE}/final/integrated-overview.md"
    baton_text = owner_blobs[baton_path].decode("utf-8")
    overview_text = owner_blobs[overview_path].decode("utf-8")
    baton_words = words(baton_text)
    overview_words = words(overview_text)
    markdown_word_violations = []
    for path in [item for item in owner_paths if item.endswith(".md")]:
        count = words(owner_blobs[path].decode("utf-8", errors="replace"))
        if count > 100000:
            markdown_word_violations.append({"path": path, "words": count})

    truth = json.loads(owner_blobs[f"{BASE}/final/phase-truth.json"].decode("utf-8-sig"))
    method = json.loads(owner_blobs[f"{BASE}/final/method-flow-final.json"].decode("utf-8-sig"))
    retained = json.loads(owner_blobs[f"{BASE}/final/retained-negative-register.json"].decode("utf-8-sig"))
    route = json.loads(owner_blobs[f"{BASE}/final/route-gate.json"].decode("utf-8-sig"))
    privacy_receipt = json.loads(owner_blobs[f"{BASE}/validation/final-privacy-scan.json"].decode("utf-8-sig"))
    staged_review = json.loads(owner_blobs[f"{BASE}/validation/final-staged-review.json"].decode("utf-8-sig"))
    changed_paths = sorted(
        path
        for path in git("diff", "--name-only", f"{EVIDENCE}..{head}").stdout.splitlines()
        if path
    )

    truth_boundary = (
        truth["counts"] == EXPECTED_COUNTS
        and truth["outcomes"] == EXPECTED_OUTCOMES
        and truth["declared_chain"] == 10070
        and truth["proposal_count"] == 60
        and truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    )
    failure_boundary = (
        not method["failure_erasure"]
        and not method["independent_reproduction_claimed"]
        and method["same_owner_only"]
        and len(method["startup_failures"]) == 4
        and method["x1_postcommit_failures"] == []
        and len(method["x2_operational_failures"]) == 5
        and len(method["closeout_operational_failures"]) == 3
        and retained["retained_mutations"] == 300
        and retained["startup_failures"] == 4
        and retained["x2_operational_failures"] == 5
        and retained["closeout_operational_failures"] == 3
    )
    route_boundary = (
        route["route_state"] == "PREPARED_NOT_SENT"
        and route["exact_title"] == "Caelen Ash"
        and route["next_phase"] == "v681-v7"
        and not route["recipient_contacted"]
        and route["send_requires_exact_final_canonical_success"]
        and "Caelen Ash" in baton_text
        and "v681-v7" in baton_text
    )

    detailed = {
        "baton_word_bounds": 10000 <= baton_words <= 100000,
        "branch": branch == BRANCH,
        "clean_before": clean_before,
        "commit_ceiling": commits == 3,
        "content_seal": not seal_mismatches and content_seal["entry_count"] == 15,
        "direct_evidence_parent": evidence_parent == X1,
        "direct_final_parent": parent == EVIDENCE,
        "direct_x1_parent": x1_parent == SOURCE,
        "divergence": divergence == [0, 0],
        "evidence_ancestry": evidence_ancestral,
        "exact_changed_path_review": changed_paths == sorted(staged_review["expected_paths"]),
        "exact_head": head == args.expected_head,
        "failure_boundary": failure_boundary,
        "final_privacy_receipt": privacy_receipt["confirmed_hits"] == [],
        "four_way_equality": four_way,
        "json": not json_failures,
        "manifest_parity": manifest_mismatches == 0,
        "markdown_word_caps": not markdown_word_violations,
        "materialized_file_ceiling": len(bounded_owner_paths) < 2000,
        "overview_floor": overview_words >= 1800,
        "privacy": not confirmed_privacy,
        "python_ast": not ast_failures,
        "route_boundary": route_boundary,
        "ruff": ruff.returncode == 0,
        "ruff_scope": set(ruff_paths) == {path for path in changed_paths if path.endswith(".py")},
        "tests": tests.returncode == 0,
        "three_single_parent_commits": commits == 3 and merges == 0,
        "truth_boundary": truth_boundary,
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
                    "markdown_word_violations": markdown_word_violations,
                    "ruff_stderr": ruff.stderr[-3000:],
                    "ruff_stdout": ruff.stdout[-3000:],
                    "seal_mismatches": seal_mismatches,
                    "test_stderr": tests.stderr[-3000:],
                    "test_stdout": tests.stdout[-3000:],
                },
                indent=2,
            )
        )

    clean_after = not git("status", "--porcelain=v1").stdout.strip()
    if not clean_after:
        raise RuntimeError("canonical validation changed the repository worktree")

    payload = {
        "baton_sha256": digest(normalized(owner_blobs[baton_path])),
        "baton_words": baton_words,
        "bounded_passing_witnesses": EXPECTED_COUNTS["bounded_passing_witnesses"],
        "canonical_invocations": 1,
        "canonical_successes": 1,
        "clean_after": clean_after,
        "clean_before": clean_before,
        "content_seal_entries": content_seal["entry_count"],
        "content_seal_mismatches": len(seal_mismatches),
        "detailed_check_count": len(detailed),
        "detailed_checks": detailed,
        "divergence": divergence,
        "effective_methods": EXPECTED_COUNTS["effective_methods"],
        "effective_negatives": EXPECTED_COUNTS["effective_negatives"],
        "exact_gates": EXPECTED_COUNTS["exact_gates"],
        "exact_head": head,
        "failed_witnesses": EXPECTED_COUNTS["failed_witnesses"],
        "final_delta_entries": manifest_results[2]["entries"],
        "fresh_live_remote": live,
        "full_repository_suite_run": False,
        "independent_reproduction_claimed": False,
        "json_documents": len(json_paths),
        "manifest_entries": sum(row["entries"] for row in manifest_results),
        "manifest_mismatches": manifest_mismatches,
        "manifest_results": manifest_results,
        "merges": merges,
        "open_gaps": EXPECTED_COUNTS["open_gaps"],
        "outcome_counts": EXPECTED_OUTCOMES,
        "owner_files": len(bounded_owner_paths),
        "owner_manifest_entries": owner_manifest["entry_count"],
        "overview_words": overview_words,
        "phase": "v681-v6",
        "privacy_candidates": len(privacy_candidates),
        "privacy_confirmed_hits": len(confirmed_privacy),
        "python_ast_files": len(python_paths),
        "route_state": "PREPARED_NOT_SENT",
        "ruff_returncode": ruff.returncode,
        "ruff_files": len(ruff_paths),
        "ruff_scope": "exact_final_delta_python_with_owner_wide_ast",
        "same_owner_only": True,
        "schema": "ghc.family.canonical-exact-final.v681.v6",
        "state": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "test_cases": 23,
        "test_returncode": tests.returncode,
        "test_summary": tests.stderr.strip() or tests.stdout.strip(),
        "three_phase_commits": commits,
    }
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
