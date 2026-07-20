#!/usr/bin/env python3
"""Run the sole exact-final scoped v650-v6 aggregate and integrity gates."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
PHASE_ROOT = "docs/sylven-arc/v650-v6"
SOURCE = "29439b5ed36d5b181c0d0f6a428dd872673d5194"
X1 = "b8e0109a003e2fa90794b48b3691dc76a3c06ef2"
EVIDENCE = "b8b858c3eb91201bcdea81813999a19426089f97"
BRANCH = "codex/GHC-Family/sylven-arc-v642-v8-full-tools"
TEST_MODULES = [
    "tests.test_ghc_family_v650_v5_x1",
    "tests.test_ghc_family_v650_v5_x2",
    "tests.test_ghc_family_v650_v5_closeout",
    "tests.test_ghc_family_v650_v6_x1",
    "tests.test_ghc_family_v650_v6_x2",
    "tests.test_ghc_family_v650_v6_closeout",
]


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        list(args), cwd=REPO, check=check, capture_output=True,
        text=True, encoding="utf-8", env=env,
    )


def git(*args: str) -> str:
    return run("git", *args).stdout.strip()


def batch_blobs(oids: list[str]) -> list[bytes]:
    request = ("\n".join(oids) + "\n").encode("ascii")
    completed = subprocess.run(
        ["git", "cat-file", "--batch"], cwd=REPO,
        input=request, capture_output=True, check=True,
    )
    output = completed.stdout
    position = 0
    blobs = []
    for expected in oids:
        end = output.index(b"\n", position)
        header = output[position:end].decode("ascii").split()
        position = end + 1
        oid, kind, size = header[0], header[1], int(header[2])
        blob = output[position:position + size]
        position += size + 1
        if oid != expected or kind != "blob" or len(blob) != size:
            raise RuntimeError(f"invalid batch object for {expected}")
        blobs.append(blob)
    return blobs


def tree_map(commit: str) -> dict[str, str]:
    raw = run("git", "ls-tree", "-r", "-z", commit, "--", PHASE_ROOT).stdout
    result = {}
    for row in raw.split("\0"):
        if not row:
            continue
        metadata, path = row.split("\t", 1)
        mode, kind, oid = metadata.split()
        if kind == "blob":
            result[path] = oid
    return result


def verify_manifest(commit: str, relative: str) -> dict[str, Any]:
    manifest = json.loads(git("show", f"{commit}:{PHASE_ROOT}/{relative}"))
    phase_tree = tree_map(commit)
    entries = manifest["entries"]
    blobs = batch_blobs([row["git_blob"] for row in entries])
    mismatches = []
    for row, blob in zip(entries, blobs):
        path = row["path"]
        if path.startswith(PHASE_ROOT + "/"):
            actual_oid = phase_tree.get(path)
        else:
            probe = run("git", "rev-parse", f"{commit}:{path}", check=False)
            actual_oid = probe.stdout.strip() if probe.returncode == 0 else None
        if (
            actual_oid != row["git_blob"]
            or len(blob) != row["bytes"]
            or hashlib.sha256(blob).hexdigest() != row["sha256"]
        ):
            mismatches.append(path)
    missing_exclusions = []
    for path in manifest["self_exclusions"]:
        probe = run("git", "cat-file", "-e", f"{commit}:{path}", check=False)
        if probe.returncode != 0:
            missing_exclusions.append(path)
    return {
        "commit": commit,
        "manifest": relative,
        "entry_count": len(entries),
        "self_exclusion_count": len(manifest["self_exclusions"]),
        "mismatches": mismatches,
        "missing_exclusions": missing_exclusions,
        "passed": not mismatches and not missing_exclusions,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--external-output", type=Path, required=True)
    args = parser.parse_args()

    clean_before = not git("status", "--porcelain=v1")
    head = git("rev-parse", "HEAD")
    upstream = git("rev-parse", "@{u}")
    tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_rows = git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}").split()
    live = live_rows[0] if live_rows else ""
    divergence = git("rev-list", "--left-right", "--count", "HEAD...@{u}")
    parent = git("rev-parse", "HEAD^")
    parent_count = len(git("show", "-s", "--format=%P", "HEAD").split())
    phase_commits = int(git("rev-list", "--count", f"{SOURCE}..HEAD"))
    merge_count = int(git("rev-list", "--merges", "--count", f"{SOURCE}..HEAD"))
    ancestry = {
        anchor: run("git", "merge-base", "--is-ancestor", anchor, "HEAD", check=False).returncode == 0
        for anchor in (SOURCE, X1, EVIDENCE)
    }
    diff_hygiene = run("git", "diff", "--check", f"{SOURCE}..HEAD", check=False).returncode == 0

    phase_tree = tree_map("HEAD")
    phase_paths = sorted(phase_tree)
    phase_blobs = batch_blobs([phase_tree[path] for path in phase_paths])
    blob_map = dict(zip(phase_paths, phase_blobs))
    json_paths = [path for path in phase_paths if path.endswith(".json")]
    json_errors = []
    for path in json_paths:
        try:
            json.loads(blob_map[path].decode("utf-8"))
        except Exception as exc:  # retained in external receipt if triggered
            json_errors.append({"path": path, "error": type(exc).__name__})

    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
        "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
        "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
        "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
        "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
    }
    scanner_receipts = {
        f"{PHASE_ROOT}/validation/x1-staged-privacy.json",
        f"{PHASE_ROOT}/validation/evidence-staged-privacy.json",
        f"{PHASE_ROOT}/validation/final-staged-privacy.json",
    }
    privacy_candidates = []
    privacy_confirmed = []
    for path, blob in blob_map.items():
        try:
            text = blob.decode("utf-8")
        except UnicodeDecodeError:
            continue
        for pattern_class, pattern in patterns.items():
            if pattern.search(text):
                row = {"path": path, "pattern_class": pattern_class}
                privacy_candidates.append(row)
                if path not in scanner_receipts:
                    privacy_confirmed.append(row)

    documents = {}
    for path, blob in blob_map.items():
        if Path(path).suffix.lower() in {".md", ".html", ".txt"}:
            documents[path] = len(blob.decode("utf-8").split())
    word_cap_violations = [path for path, count in documents.items() if count > 6000]
    stale_unquarantined = []
    current_paths = [
        f"{PHASE_ROOT}/final/phase-truth.json",
        f"{PHASE_ROOT}/final/final-receipt.json",
        f"{PHASE_ROOT}/final/terminal-route-state.json",
        f"{PHASE_ROOT}/handoffs/eiren-kestrel-v650-v7-prepared.md",
    ]
    for path in current_paths:
        text = blob_map[path].decode("utf-8")
        if "v650-v5" in text or "v649-v" in text or "SENT" in text and "PREPARED_NOT_SENT" not in text:
            stale_unquarantined.append(path)

    manifests = [
        verify_manifest(X1, "validation/x1-staged-manifest.json"),
        verify_manifest(EVIDENCE, "validation/evidence-staged-manifest.json"),
        verify_manifest(head, "validation/final-staged-manifest.json"),
    ]

    test_command = [sys.executable, "-B", "-m", "unittest", *TEST_MODULES, "-v"]
    tests = run(*test_command, check=False)
    test_output = tests.stdout + "\n" + tests.stderr
    match = re.search(r"Ran\s+(\d+)\s+tests?", test_output)
    tests_run = int(match.group(1)) if match else 0
    tests_passed = tests.returncode == 0 and re.search(r"\nOK\s*$", test_output) is not None

    detailed = {
        "expected_head": head == args.expected_head,
        "clean_before": clean_before,
        "four_way_equal": len({head, upstream, tracking, live}) == 1,
        "zero_divergence": divergence == "0\t0",
        "evidence_direct_parent": parent == EVIDENCE,
        "one_final_parent": parent_count == 1,
        "three_phase_commits": phase_commits == 3,
        "zero_merges": merge_count == 0,
        "source_ancestral": ancestry[SOURCE],
        "x1_ancestral": ancestry[X1],
        "evidence_ancestral": ancestry[EVIDENCE],
        "diff_hygiene": diff_hygiene,
        "all_json_parse": not json_errors,
        "privacy_zero_confirmed": not privacy_confirmed,
        "all_manifests_exact": all(row["passed"] for row in manifests),
        "document_cap": not word_cap_violations,
        "owner_file_threshold": len(phase_paths) < 15000,
        "stale_labels_zero": not stale_unquarantined,
        "scoped_tests_pass": tests_passed,
        "test_count_nonzero": tests_run > 0,
    }
    minimal = {
        "head_exact": detailed["expected_head"],
        "clean": detailed["clean_before"],
        "remote_equal": detailed["four_way_equal"] and detailed["zero_divergence"],
        "history": detailed["three_phase_commits"] and detailed["zero_merges"] and detailed["one_final_parent"],
        "anchors": all(ancestry.values()),
        "json": detailed["all_json_parse"],
        "privacy": detailed["privacy_zero_confirmed"],
        "manifests": detailed["all_manifests_exact"],
        "documents": detailed["document_cap"],
        "tests": detailed["scoped_tests_pass"],
        "not_full_suite": True,
        "no_replay": True,
        "terminal_verdict": json.loads(blob_map[f"{PHASE_ROOT}/final/phase-truth.json"].decode())["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "route_prepared": json.loads(blob_map[f"{PHASE_ROOT}/final/terminal-route-state.json"].decode())["state"] == "PREPARED_NOT_SENT",
    }
    clean_after = not git("status", "--porcelain=v1")
    passed = all(detailed.values()) and all(minimal.values()) and clean_after
    receipt = {
        "schema":"ghc.family.v650-v6.external-final-validation.v1",
        "passed":passed, "exact_head":head, "expected_head":args.expected_head,
        "upstream":upstream, "tracking":tracking, "fresh_live_remote":live,
        "divergence":divergence, "clean_before":clean_before, "clean_after":clean_after,
        "phase_commits":phase_commits, "merge_count":merge_count, "final_parent_count":parent_count,
        "ancestry":ancestry, "tests":{"modules":TEST_MODULES,"run":tests_run,"passed":tests_passed,"returncode":tests.returncode},
        "detailed_checks":{"passed":sum(detailed.values()),"total":len(detailed),"results":detailed},
        "minimal_checks":{"passed":sum(minimal.values()),"total":len(minimal),"results":minimal},
        "json_parses":{"passed":len(json_paths)-len(json_errors),"total":len(json_paths),"errors":json_errors},
        "privacy":{"scanned_files":len(phase_paths),"pattern_classes":len(patterns),"candidate_count":len(privacy_candidates),"confirmed_hits":privacy_confirmed},
        "manifests":manifests, "document_count":len(documents),
        "maximum_document_words":max(documents.values()), "document_cap_violations":word_cap_violations,
        "owner_file_count":len(phase_paths), "stale_unquarantined":stale_unquarantined,
        "full_repository_suite":False, "successful_exact_final_aggregate":passed,
        "post_success_replay":False, "same_owner_only":True, "independent_reproduction":False,
        "terminal_verdict":"NOT_READY_FOR_STAGE_20",
    }
    args.external_output.parent.mkdir(parents=True, exist_ok=True)
    args.external_output.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8", newline="\n",
    )
    print(json.dumps({
        "passed":passed, "exact_head":head, "tests":f"{tests_run}/{tests_run if tests_passed else 0}",
        "detailed":f"{sum(detailed.values())}/{len(detailed)}",
        "minimal":f"{sum(minimal.values())}/{len(minimal)}",
        "json":f"{len(json_paths)-len(json_errors)}/{len(json_paths)}",
        "privacy_files":len(phase_paths),
        "manifest_entries":[row["entry_count"] for row in manifests],
        "clean_after":clean_after,
    }, indent=2))
    if not passed:
        error_tail = "\n".join(test_output.splitlines()[-30:])
        if error_tail:
            print(error_tail, file=sys.stderr)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
