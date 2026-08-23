#!/usr/bin/env python3
"""Exclusive owner-scoped canonical validator for Caelen Morrow v667-v5.

``--self-test`` is a bounded x2 runner smoke. ``--exact-final`` performs the
single terminal owner-delta aggregate and writes one external receipt. The full
repository suite is intentionally outside this runner's scope.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import py_compile
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, BinaryIO

try:
    from ghc_family_caelen_morrow_v667_v5_core import ROOT, runner_self_test
except ModuleNotFoundError:
    from scripts.ghc_family_caelen_morrow_v667_v5_core import ROOT, runner_self_test


OWNER = "Caelen Morrow"
OWNER_SLUG = "caelen-morrow"
PHASE = "v667-v5"
SOURCE_SHA = "08cdc8ad3c201ea6d7c576ca5fa67bdc43910a93"
X1_SHA = "b7b73cc81266e28ae9cbb1e4c429d2e93be30999"
BRANCH = "codex/GHC-Family/caelen-morrow-v667-v5-full-tools"
PHASE_PREFIX = f"docs/{OWNER_SLUG}/{PHASE}/"


def git_bytes(*args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def git(*args: str) -> str:
    return git_bytes(*args).decode("utf-8").strip()


def read_exact(stream: BinaryIO, size: int) -> bytes:
    chunks: list[bytes] = []
    remaining = size
    while remaining:
        chunk = stream.read(remaining)
        if not chunk:
            raise RuntimeError(f"batch stream ended with {remaining} bytes unread")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def batch_blobs(objects: list[str]) -> dict[str, bytes]:
    process = subprocess.Popen(
        ["git", "-C", str(ROOT), "cat-file", "--batch"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert process.stdin is not None and process.stdout is not None and process.stderr is not None
    result: dict[str, bytes] = {}
    try:
        for object_name in objects:
            process.stdin.write(object_name.encode("utf-8") + b"\n")
            process.stdin.flush()
            header = process.stdout.readline()
            if not header:
                raise RuntimeError(f"missing batch header for {object_name}")
            fields = header.rstrip(b"\n").split()
            if fields[-1:] == [b"missing"]:
                raise RuntimeError(f"missing Git object {object_name}")
            if len(fields) != 3 or fields[1] != b"blob":
                raise RuntimeError(f"unexpected batch header for {object_name}: {header!r}")
            size = int(fields[2])
            raw = read_exact(process.stdout, size)
            if process.stdout.read(1) != b"\n":
                raise RuntimeError(f"missing batch delimiter for {object_name}")
            result[object_name] = raw
        process.stdin.close()
        returncode = process.wait(timeout=30)
        if returncode != 0:
            raise RuntimeError(process.stderr.read().decode("utf-8", errors="replace"))
    finally:
        if process.poll() is None:
            process.kill()
    return result


def blob_json(commit: str, path: str) -> dict[str, Any]:
    raw = batch_blobs([f"{commit}:{path}"])[f"{commit}:{path}"]
    return json.loads(raw.decode("utf-8"))


def replay_manifest(manifest_commit: str, blob_commit: str, path: str) -> dict[str, Any]:
    manifest = blob_json(manifest_commit, path)
    entries = manifest["entries"]
    objects = [f"{blob_commit}:{row['path']}" for row in entries]
    blobs = batch_blobs(objects)
    mismatches = []
    for row in entries:
        raw = blobs[f"{blob_commit}:{row['path']}"]
        if len(raw) != row["bytes"] or hashlib.sha256(raw).hexdigest() != row["sha256"]:
            mismatches.append(row["path"])
    return {
        "manifest_path": path,
        "manifest_commit": manifest_commit,
        "blob_commit": blob_commit,
        "entry_count": len(entries),
        "self_exclusion_count": len(manifest.get("self_exclusions", [])),
        "mismatches": mismatches,
        "valid": not mismatches,
    }


def parse_divergence(value: str) -> tuple[int, int]:
    fields = value.split()
    if len(fields) != 2:
        raise RuntimeError(f"unexpected divergence: {value!r}")
    return int(fields[0]), int(fields[1])


def run_selected_tests() -> dict[str, Any]:
    x1_class = "tests.test_ghc_family_caelen_morrow_v667_v5_x1.CaelenMorrowV667V5X1Tests"
    x1_methods = [
        "test_complete_4410_row_novelty_audit_is_valid",
        "test_domain_novelty_and_rejected_horology_are_visible",
        "test_every_proposal_has_complete_preregistration_contract",
        "test_exact_twenty_new_proposals_and_frozen_total",
        "test_expected_outcomes_use_only_four_labels",
        "test_flashcard_architecture_is_four_tier_thirteen_section_and_nonidentity",
        "test_inherited_counts_and_eight_caelen_startup_failures",
        "test_lifecycle_scoped_compile_counts_remain_distinct",
        "test_overview_checklist_privacy_and_caps",
        "test_portfolio_counts_and_holds",
        "test_primary_pillar_practice_and_relational_boundary",
        "test_source_chain_manifest_and_validation_truth",
        "test_source_ledger_uses_current_official_or_primary_surfaces",
    ]
    selections = [f"{x1_class}.{method}" for method in x1_methods]
    selections.extend([
        "tests.test_ghc_family_caelen_morrow_v667_v5_x2",
        "tests.test_ghc_family_caelen_morrow_v667_v5_closeout",
        "tests.test_ghc_family_freed_id_flashcards",
    ])
    completed = subprocess.run(
        [sys.executable, "-m", "unittest", "-v", *selections],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )
    combined = completed.stdout + "\n" + completed.stderr
    match = re.search(r"Ran (\d+) tests?", combined)
    return {
        "selection_count": len(selections),
        "tests_run": int(match.group(1)) if match else None,
        "exit_code": completed.returncode,
        "passed": completed.returncode == 0 and match is not None,
        "failure_markers": combined.count("FAIL:") + combined.count("ERROR:"),
        "immutable_x1_worktree_absence_test_excluded": True,
    }


def privacy_scan(paths: list[str], blobs: dict[str, bytes]) -> dict[str, Any]:
    local_file_scheme = "file" + "://"
    local_app_scheme = "app" + "://"
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?:source_thread_id|threadId)[\"']?\s*[:=]\s*[\"'][^\"']+[\"']|\b019[a-f0-9]{5,}-[a-f0-9-]{20,}\b", re.I),
        "private_absolute_path_or_route": re.compile(r"\b[A-Z]:\\(?:Users|GHC-Archives)\\|" + re.escape(local_file_scheme) + r"[^\s\"']+|" + re.escape(local_app_scheme) + r"[^\s\"']+|private[_ -]?route\s*[:=]\s*[\"'][^\"']+", re.I),
        "credential_key_or_token_material": re.compile(r"(?:api[_-]?key|password|bearer|secret[_-]?key|access[_-]?token)\s*[:=]\s*[\"'][^\"']+[\"']", re.I),
        "transcript_screenshot_or_session_stream": re.compile(r"(?:transcript|screenshot|session[_ -]?stream)\s*[:=]\s*[\"'][^\"']+", re.I),
        "private_callable_or_application_state": re.compile(r"(?:private[_ -]?callable|private[_ -]?(?:application|app)[_ -]?state|resume[_ -]?value)\s*[:=]\s*[\"'][^\"']+", re.I),
    }
    hits = []
    isolated_mentions = []
    for path in paths:
        text = blobs[f"HEAD:{path}"].decode("utf-8")
        if re.search(r"source_thread_id|threadId", text, re.I):
            isolated_mentions.append({"path": path, "disposition": "policy_test_or_retained_failure_label_without_payload"})
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(text):
                hits.append({"class": class_name, "path": path, "matched_text": match.group(0)})
    return {
        "classes": len(patterns), "files_scanned": len(paths),
        "nonconfirming_label_mentions": isolated_mentions,
        "confirmed_hits": hits, "confirmed_hit_count": len(hits), "valid": not hits,
    }


def validate_exact_final(expected_head: str, evidence_sha: str) -> dict[str, Any]:
    clean_before = git("status", "--porcelain") == ""
    head = git("rev-parse", "HEAD")
    local_branch = git("branch", "--show-current")
    upstream = git("rev-parse", "@{u}")
    tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_line = git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")
    fresh_live = live_line.split()[0] if live_line else ""
    ahead, behind = parse_divergence(git("rev-list", "--left-right", "--count", "HEAD...@{u}"))

    commits = [row for row in git("rev-list", "--reverse", f"{SOURCE_SHA}..{head}").splitlines() if row]
    merges = [row for row in git("rev-list", "--merges", f"{SOURCE_SHA}..{head}").splitlines() if row]
    parent_counts = {commit: len(git("show", "-s", "--format=%P", commit).split()) for commit in commits}
    direct_chain = (
        len(commits) == 3
        and commits[0] == X1_SHA
        and commits[1] == evidence_sha
        and commits[2] == head
        and git("rev-parse", f"{X1_SHA}^") == SOURCE_SHA
        and git("rev-parse", f"{evidence_sha}^") == X1_SHA
        and git("rev-parse", f"{head}^") == evidence_sha
    )

    x1_paths = [row for row in git("ls-tree", "-r", "--name-only", X1_SHA, PHASE_PREFIX).splitlines() if row]
    x1_forbidden = [path for path in x1_paths if "/x2/" in path or "/evidence/" in path or "/closeout/" in path or "/seal/" in path or "/final/" in path]
    evidence_delta = [row for row in git("diff", "--name-only", f"{X1_SHA}..{evidence_sha}").splitlines() if row]
    evidence_x1_mutations = [path for path in evidence_delta if path.startswith(f"{PHASE_PREFIX}x1/") or path.endswith("_x1.py")]
    final_delta = [row for row in git("diff", "--name-only", f"{evidence_sha}..{head}").splitlines() if row]
    final_evidence_mutations = [path for path in final_delta if path.startswith(f"{PHASE_PREFIX}x1/") or path.startswith(f"{PHASE_PREFIX}x2/") or path.startswith(f"{PHASE_PREFIX}evidence/") or path.startswith(f"{PHASE_PREFIX}deck/") or path.startswith(f"{PHASE_PREFIX}skills/")]

    manifest_specs = [
        (X1_SHA, X1_SHA, f"{PHASE_PREFIX}validation/x1-content-manifest.json"),
        (evidence_sha, evidence_sha, f"{PHASE_PREFIX}validation/evidence-content-manifest.json"),
        (head, head, f"{PHASE_PREFIX}validation/closeout-content-manifest.json"),
        (head, head, f"{PHASE_PREFIX}validation/final-delta-manifest.json"),
        (head, head, f"{PHASE_PREFIX}validation/final-owner-manifest.json"),
    ]
    manifests = [replay_manifest(manifest_commit, blob_commit, path) for manifest_commit, blob_commit, path in manifest_specs]

    owner_paths = [row for row in git("ls-tree", "-r", "--name-only", head, PHASE_PREFIX).splitlines() if row]
    changed_paths = [row for row in git("diff", "--name-only", f"{SOURCE_SHA}..{head}").splitlines() if row]
    public_owner_paths = [
        path for path in changed_paths
        if path.startswith(PHASE_PREFIX)
        or path.startswith("scripts/ghc_family_caelen_morrow_v667_v5_")
        or path.startswith("scripts/build_ghc_family_caelen_morrow_v667_v5_")
        or path.startswith("tests/test_ghc_family_caelen_morrow_v667_v5_")
    ]
    final_blobs = batch_blobs([f"HEAD:{path}" for path in public_owner_paths])
    json_paths = [path for path in owner_paths if path.endswith(".json")]
    json_blobs = batch_blobs([f"HEAD:{path}" for path in json_paths])
    json_errors = []
    stale_owner_phase = []
    for path in json_paths:
        try:
            value = json.loads(json_blobs[f"HEAD:{path}"].decode("utf-8"))
            if isinstance(value, dict):
                if "owner" in value and value["owner"] != OWNER:
                    stale_owner_phase.append({"path": path, "field": "owner", "value": value["owner"]})
                if "phase" in value and value["phase"] != PHASE:
                    stale_owner_phase.append({"path": path, "field": "phase", "value": value["phase"]})
        except Exception as exc:
            json_errors.append({"path": path, "error": type(exc).__name__})
    markdown_paths = [path for path in owner_paths if path.endswith(".md")]
    markdown_blobs = batch_blobs([f"HEAD:{path}" for path in markdown_paths])
    markdown_errors = []
    max_document_words = 0
    for path in owner_paths:
        if path.endswith((".json", ".md", ".html", ".yaml", ".py")):
            raw = batch_blobs([f"HEAD:{path}"])[f"HEAD:{path}"]
            try:
                text = raw.decode("utf-8")
                max_document_words = max(max_document_words, len(re.findall(r"\S+", text)))
            except UnicodeDecodeError:
                if path.endswith(".md"):
                    markdown_errors.append(path)
    privacy = privacy_scan(public_owner_paths, final_blobs)

    python_paths = [path for path in public_owner_paths if path.endswith(".py")]
    compile_errors = []
    security_findings = []
    for path in python_paths:
        try:
            py_compile.compile(str(ROOT / path), doraise=True)
            tree = ast.parse((ROOT / path).read_text(encoding="utf-8"), filename=path)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                    security_findings.append({"path": path, "finding": f"dynamic_{node.func.id}"})
        except Exception as exc:
            compile_errors.append({"path": path, "error": type(exc).__name__})

    tests = run_selected_tests()
    details = {
        "expected_head": head == expected_head,
        "branch": local_branch == BRANCH,
        "clean_before": clean_before,
        "four_way_equal": head == upstream == tracking == fresh_live,
        "zero_divergence": ahead == 0 and behind == 0,
        "three_phase_commits": len(commits) == 3,
        "zero_merges": not merges,
        "one_parent_each": all(count == 1 for count in parent_counts.values()),
        "direct_chain": direct_chain,
        "immutable_x1_tree": not x1_forbidden,
        "no_evidence_x1_mutation": not evidence_x1_mutations,
        "no_final_evidence_mutation": not final_evidence_mutations,
        "all_manifests": all(row["valid"] for row in manifests),
        "json_parses": not json_errors,
        "markdown_decodes": not markdown_errors,
        "privacy_scan": privacy["valid"],
        "python_compiles": not compile_errors,
        "bounded_python_security": not security_findings,
        "selected_tests": tests["passed"],
        "owner_phase_labels": not stale_owner_phase,
        "file_cap": len(owner_paths) <= 2000,
        "word_cap": max_document_words <= 100000,
    }
    minimal = {
        "head": head == expected_head,
        "x1_ancestral": git("merge-base", "--is-ancestor", X1_SHA, head) == "",
        "evidence_ancestral": git("merge-base", "--is-ancestor", evidence_sha, head) == "",
        "final_parent": git("rev-parse", f"{head}^") == evidence_sha,
        "source_parent": git("rev-parse", f"{X1_SHA}^") == SOURCE_SHA,
        "commit_count": len(commits) == 3,
        "merge_count": not merges,
        "parent_counts": all(count == 1 for count in parent_counts.values()),
        "clean": clean_before,
        "ahead": ahead == 0,
        "behind": behind == 0,
        "upstream": upstream == head,
        "tracking": tracking == head,
        "fresh_live": fresh_live == head,
        "terminal_verdict": blob_json(head, f"{PHASE_PREFIX}closeout/phase-truth.json").get("terminal_verdict") == "NOT_READY_FOR_STAGE_20",
    }
    clean_after = git("status", "--porcelain") == ""
    valid = all(details.values()) and all(minimal.values()) and clean_after
    return {
        "schema": "ghc-family-caelen-v667-v5-exclusive-owner-canonical-v1",
        "status": "VALID_EXCLUSIVE_OWNER_SCOPED_CANONICAL_COMPLETION" if valid else "INVALID_EXCLUSIVE_OWNER_SCOPED_CANONICAL_COMPLETION",
        "valid": valid,
        "owner": OWNER,
        "phase": PHASE,
        "exact_head": head,
        "source": SOURCE_SHA,
        "x1": X1_SHA,
        "evidence": evidence_sha,
        "branch": BRANCH,
        "commit_count": len(commits),
        "merge_count": len(merges),
        "parent_counts": parent_counts,
        "clean_before": clean_before,
        "clean_after": clean_after,
        "ahead": ahead,
        "behind": behind,
        "four_way_equal": head == upstream == tracking == fresh_live,
        "manifests": manifests,
        "manifest_entry_total": sum(row["entry_count"] for row in manifests),
        "json_parse_count": len(json_paths),
        "json_errors": json_errors,
        "markdown_decode_count": len(markdown_paths),
        "markdown_errors": markdown_errors,
        "privacy": privacy,
        "python_compile_count": len(python_paths),
        "compile_errors": compile_errors,
        "bounded_python_security_findings": security_findings,
        "tests": tests,
        "detailed_checks": details,
        "detailed_pass_count": sum(details.values()),
        "detailed_check_count": len(details),
        "minimal_checks": minimal,
        "minimal_pass_count": sum(minimal.values()),
        "minimal_check_count": len(minimal),
        "owner_file_count": len(owner_paths),
        "max_document_words": max_document_words,
        "full_repository_suite": False,
        "same_owner_only": True,
        "independent_reproduction": False,
        "replayed": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": "Bounded same-owner software and documentation validation only; not independent reproduction, external audit, navigation or professional validation, production certification, exhaustive security, complete privacy or accessibility assurance, legal or cultural review, Māori-authority review, empirical GMUT confirmation, Theory-of-Everything proof, AGI or ASI evidence, consciousness or personhood evidence, canon, or Stage 20 authority.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--exact-final", action="store_true")
    parser.add_argument("--expected-head")
    parser.add_argument("--evidence")
    parser.add_argument("--output")
    args = parser.parse_args()
    if args.self_test:
        result = runner_self_test("canonical")
        print(json.dumps(result, indent=2, ensure_ascii=True))
        return 0 if result["passed"] else 1
    if not args.expected_head or not re.fullmatch(r"[0-9a-f]{40}", args.expected_head):
        raise SystemExit("--expected-head must be an exact lowercase Git object id")
    if not args.evidence or not re.fullmatch(r"[0-9a-f]{40}", args.evidence):
        raise SystemExit("--evidence must be an exact lowercase Git object id")
    if not args.output:
        raise SystemExit("--output is required")
    output = Path(args.output)
    if output.exists():
        raise SystemExit("exclusive canonical output already exists; replay refused")
    result = validate_exact_final(args.expected_head, args.evidence)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"valid": result["valid"], "status": result["status"], "tests_run": result["tests"]["tests_run"], "manifest_entry_total": result["manifest_entry_total"], "json_parse_count": result["json_parse_count"]}, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
