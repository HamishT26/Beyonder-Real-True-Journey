#!/usr/bin/env python3
"""Run the sole exact-final bounded canonical validation for Tamar v650-v5."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
PHASE_REL = "docs/tamar-vey/v650-v5"
PHASE = REPO / PHASE_REL
BRANCH = "codex/GHC-Family/tamar-vey-full-tools"
SOURCE = "e3d115d7caade153086dea794131035bcd2192d0"
X1_INITIAL = "7c15d7e0f96e1ce5a1b7fd6049ef3c3285debc30"
X1_FINAL = "56ff8d5ab41d4b477184c854037122c81e2cc6a3"
EVIDENCE = "f485c4b053272eb384594d989ceeb6d85160111a"
TEST_MODULES = [
    "tests.test_ghc_family_v650_v4_x1",
    "tests.test_ghc_family_v650_v4_x2",
    "tests.test_ghc_family_v650_v4_closeout",
    "tests.test_ghc_family_v650_v5_x1",
    "tests.test_ghc_family_v650_v5_x2",
    "tests.test_ghc_family_v650_v5_closeout",
]
PATTERNS = {
    "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
    "private_local_path": re.compile(r"(?:[A-Z]:\\Users\\|/home/[^/\s]+/|/Users/[^/\s]+/)", re.I),
    "private_uri": re.compile(r"(?:codex|vscode|file)://", re.I),
    "credential_assignment": re.compile(r"(?i)(?:api[_-]?key|password|secret|token)\s*[:=]\s*['\"][^'\"]+"),
    "delegation_markup": re.compile(r"<codex_delegation>|<source_thread_id>|raw task identifier", re.I),
}


def run(*args: str, check: bool = True, input_bytes: bytes | None = None) -> subprocess.CompletedProcess[bytes]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONUTF8"] = "1"
    return subprocess.run(args, cwd=REPO, check=check, input=input_bytes, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)


def text(*args: str, check: bool = True) -> str:
    return run(*args, check=check).stdout.decode("utf-8").strip()


def read_json(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def git_blob(commit: str, path: str) -> bytes:
    return run("git", "show", f"{commit}:{path}").stdout


def verify_manifest(commit: str, relative: str) -> dict[str, Any]:
    full = f"{PHASE_REL}/{relative}"
    manifest = json.loads(git_blob(commit, full).decode("utf-8"))
    entries = manifest["entries"]
    payload = "".join(f"{row['git_blob']}\n" for row in entries).encode("ascii")
    batch = run("git", "cat-file", "--batch", input_bytes=payload).stdout
    offset = 0
    mismatches = []
    for row in entries:
        end = batch.index(b"\n", offset)
        header = batch[offset:end].decode("ascii").split()
        if len(header) != 3 or header[1] != "blob":
            mismatches.append({"path": row["path"], "reason": "invalid_batch_header"})
            break
        size = int(header[2])
        start = end + 1
        data = batch[start:start + size]
        offset = start + size + 1
        if header[0] != row["git_blob"] or len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
            mismatches.append({"path": row["path"], "reason": "blob_or_hash_mismatch"})
    return {
        "commit": commit,
        "path": relative,
        "entry_count": len(entries),
        "declared_entry_count": manifest["entry_count"],
        "self_exclusion_count": len(manifest["self_exclusions"]),
        "mismatch_count": len(mismatches),
        "passed": len(entries) == manifest["entry_count"] and not mismatches,
    }


def run_tests() -> dict[str, Any]:
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromNames(TEST_MODULES)
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=1).run(suite)
    return {
        "run": result.testsRun,
        "passed": result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped),
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "successful": result.wasSuccessful(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = Path(args.output)
    if output.exists():
        raise RuntimeError("refusing to overwrite an existing canonical validation receipt")

    head = text("git", "rev-parse", "HEAD")
    clean_before = not bool(text("git", "status", "--porcelain"))
    branch = text("git", "branch", "--show-current")
    upstream = text("git", "rev-parse", "@{u}")
    tracking = text("git", "rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_line = text("git", "ls-remote", "origin", f"refs/heads/{BRANCH}")
    live = live_line.split()[0] if live_line else ""
    phase_commits = int(text("git", "rev-list", "--count", f"{SOURCE}..HEAD"))
    merges = int(text("git", "rev-list", "--merges", "--count", f"{SOURCE}..HEAD"))
    parents = text("git", "show", "-s", "--format=%P", "HEAD").split()
    ancestry = {
        anchor: run("git", "merge-base", "--is-ancestor", anchor, "HEAD", check=False).returncode == 0
        for anchor in (SOURCE, X1_INITIAL, X1_FINAL, EVIDENCE)
    }

    tests = run_tests()
    json_paths = sorted(PHASE.rglob("*.json"))
    json_errors = []
    for path in json_paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            json_errors.append({"path": path.relative_to(PHASE).as_posix(), "error": type(exc).__name__})

    public_paths = sorted(path for path in PHASE.rglob("*") if path.is_file())
    privacy_hits = []
    for path in public_paths:
        try:
            value = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for class_name, pattern in PATTERNS.items():
            for match in pattern.finditer(value):
                privacy_hits.append({"path": path.relative_to(PHASE).as_posix(), "class": class_name, "line": value.count("\n", 0, match.start()) + 1})

    manifests = [
        verify_manifest(X1_INITIAL, "validation/x1-staged-manifest.json"),
        verify_manifest(X1_FINAL, "validation/x1-staged-manifest.json"),
        verify_manifest(EVIDENCE, "validation/evidence-staged-manifest.json"),
        verify_manifest(head, "validation/final-staged-manifest.json"),
    ]
    truth = read_json("phase-truth.json")
    negatives = read_json("retained-negative-register.json")
    gates = read_json("exact-open-gate-register.json")
    route = read_json("orchestration/terminal-route-state.json")
    doc_cap = read_json("validation/final-document-cap-receipt.json")
    owner_cap = read_json("validation/final-owner-file-threshold.json")
    hygiene = run("git", "diff", "--check", f"{EVIDENCE}..HEAD", check=False)

    detailed = []
    for row in read_json("x2-evidence-ledger.json")["proposals"]:
        detailed.append({"check": f"proposal:{row['proposal_id']}", "passed": row["passed"]})
    for path in sorted((PHASE / "skill-witnesses").glob("*.json")):
        row = json.loads(path.read_text(encoding="utf-8"))
        detailed.append({"check": f"skill:{row['skill_id']}", "passed": row["smoke_passed"]})
    for path in sorted((PHASE / "runner-witnesses").glob("*.json")):
        row = json.loads(path.read_text(encoding="utf-8"))
        detailed.append({"check": f"runner:{row['group']}", "passed": row["passed"]})
    for name, expected in (("safe-now-execution.json", 40), ("candidate-execution.json", 30), ("skill-execution.json", 20), ("runner-execution.json", 10), ("clean-fix-refine-execution.json", 40)):
        row = read_json(f"portfolios/{name}")
        detailed.append({"check": f"portfolio:{name}", "passed": row["completed"] == expected})
    detailed.extend([
        {"check": "mutations:100", "passed": read_json("validation/x2-synthetic-mutation-results.json")["rejected_or_quarantined_count"] == 100},
        {"check": "stale_labels", "passed": read_json("validation/stale-label-review.json")["confirmed_current_stale_claim_count"] == 0},
        {"check": "document_cap", "passed": doc_cap["passed"]},
        {"check": "owner_cap", "passed": not owner_cap["exceeded"]},
        {"check": "route_unsent", "passed": route["state"] == "PREPARED_NOT_SENT" and route["messages_sent"] == 0},
    ])

    clean_after = not bool(text("git", "status", "--porcelain"))
    minimal = {
        "branch_exact": branch == BRANCH,
        "clean_before": clean_before,
        "clean_after": clean_after,
        "local_equals_upstream": head == upstream,
        "local_equals_tracking": head == tracking,
        "local_equals_live": head == live,
        "source_ancestral": ancestry[SOURCE],
        "x1_initial_ancestral": ancestry[X1_INITIAL],
        "x1_final_ancestral": ancestry[X1_FINAL],
        "evidence_ancestral": ancestry[EVIDENCE],
        "phase_commit_count_four": phase_commits == 4,
        "zero_merges": merges == 0,
        "one_final_parent": len(parents) == 1,
        "final_parent_is_evidence": parents == [EVIDENCE],
        "distribution_exact": truth["distribution"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "negative_count_exact": negatives["effective_total"] == 6055,
        "open_gap_count_exact": gates["effective_open_gaps"] == 47,
        "exact_gate_count_exact": gates["effective_exact_gates"] == 48,
        "terminal_verdict_exact": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "route_prepared_not_sent": route["state"] == "PREPARED_NOT_SENT" and route["messages_sent"] == 0,
        "all_json_parsed": not json_errors,
        "privacy_zero_confirmed_hits": not privacy_hits,
        "all_manifests_pass": all(row["passed"] for row in manifests),
        "diff_hygiene": hygiene.returncode == 0,
        "document_and_owner_caps": doc_cap["passed"] and not owner_cap["exceeded"],
    }
    passed = (
        tests["successful"]
        and tests["run"] == 62
        and len(minimal) == 25
        and all(minimal.values())
        and all(row["passed"] for row in detailed)
    )
    receipt = {
        "schema": "ghc.family.v650-v5.external-final-canonical-validation.v1",
        "phase": "v650-v5",
        "owner": "Tamar Vey",
        "exact_head": head,
        "branch": branch,
        "tests": tests,
        "minimal_checks": {"count": len(minimal), "passed": sum(minimal.values()), "checks": minimal},
        "detailed_checks": {"count": len(detailed), "passed": sum(row["passed"] for row in detailed)},
        "json": {"parsed": len(json_paths), "errors": json_errors},
        "privacy": {"scanned_files": len(public_paths), "pattern_classes": list(PATTERNS), "confirmed_hit_count": len(privacy_hits), "hits": privacy_hits, "complete_privacy_claim": False},
        "manifests": manifests,
        "history": {"source": SOURCE, "x1_initial": X1_INITIAL, "x1_final": X1_FINAL, "evidence": EVIDENCE, "phase_commits": phase_commits, "merges": merges, "parent_count": len(parents)},
        "remote_equality": {"local": head, "upstream": upstream, "tracking": tracking, "live": live, "equal": head == upstream == tracking == live},
        "full_repository_suite": False,
        "post_success_replay": False,
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "passed": passed,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"head": head, "tests": tests, "minimal": receipt["minimal_checks"], "detailed": receipt["detailed_checks"], "json": receipt["json"], "privacy": {"scanned_files": len(public_paths), "confirmed_hit_count": len(privacy_hits)}, "manifests": manifests, "passed": passed}, ensure_ascii=False, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
