#!/usr/bin/env python3
"""Run Sable Rook's single exact-final v652-v1 canonical validation pass."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
PHASE_ROOT = "docs/sable-rook/v652-v1"
ROOT = REPO / PHASE_ROOT
BRANCH = "codex/GHC-Family/sable-rook-full-tools"
SOURCE_HEAD = "4b31ec3d1bb4db24f48967da5c4e27a05b43e1f9"
X1_HEAD = "0e7efd8f49dbb530d60e9d2f1b474a3de9a035c2"
EVIDENCE_HEAD = "fddc360ee643b7b50f7c65395a39948cf0c0d535"
GENERIC_RUNNERS = {
    "scripts/ghc_family_claim_lease_demoter.py",
    "scripts/ghc_family_cruft_pack_guard.py",
    "scripts/ghc_family_oci_referrer_tribunal.py",
    "scripts/ghc_family_gmut_covariant_boards.py",
    "scripts/ghc_family_artifact_lineage_tribunals.py",
    "scripts/ghc_family_reproducible_build_envelope.py",
    "scripts/ghc_family_court_registry_proxy.py",
    "scripts/ghc_family_identity_lifecycle_profiles.py",
    "scripts/ghc_family_stage20_multiverse_board.py",
}


def completed(*args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.update({"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"})
    return subprocess.run(list(args), cwd=REPO, check=True, capture_output=True, text=True, encoding="utf-8", env=env)


def run(*args: str) -> str:
    return completed(*args).stdout.strip()


def git_blob(commit: str, relative: str) -> tuple[str, bytes]:
    oid = run("git", "rev-parse", f"{commit}:{relative}")
    blob = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=REPO)
    return oid, blob


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def is_owner_path(path: str) -> bool:
    if path.startswith(f"{PHASE_ROOT}/") or path in GENERIC_RUNNERS:
        return True
    if path.startswith("scripts/") and "v652_v1" in Path(path).name:
        return True
    return path.startswith("tests/") and "v652_v1" in Path(path).name


def diff_paths(parent: str, commit: str) -> set[str]:
    return set(run("git", "diff", "--name-only", parent, commit).splitlines())


def verify_manifest(relative: str, commit: str, expected_paths: set[str]) -> dict:
    manifest = load(relative)
    entries = manifest["entries"]
    exclusions = set(manifest["self_exclusions"])
    mismatches = []
    for row in entries:
        try:
            oid, blob = git_blob(commit, row["path"])
        except subprocess.CalledProcessError:
            mismatches.append({"path": row["path"], "reason": "missing_blob"})
            continue
        observed = (oid, len(blob), hashlib.sha256(blob).hexdigest())
        expected = (row["git_blob"], row["bytes"], row["sha256"])
        if observed != expected:
            mismatches.append({"path": row["path"], "reason": "blob_mismatch"})
    covered = {row["path"] for row in entries} | exclusions
    return {
        "entries": len(entries),
        "exclusions": len(exclusions),
        "mismatches": mismatches,
        "path_set_match": covered == expected_paths,
        "missing_paths": sorted(expected_paths - covered),
        "extra_paths": sorted(covered - expected_paths),
        "valid": not mismatches and covered == expected_paths,
    }


def run_test_pattern(pattern: str) -> tuple[int, str]:
    result = completed(sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-p", pattern)
    text = (result.stdout + "\n" + result.stderr).strip()
    match = re.search(r"Ran\s+(\d+)\s+tests?", text)
    return (int(match.group(1)) if match else 0), text


def privacy_scan(commit: str, paths: set[str]) -> dict:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]|(?<![0-9a-f])[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}(?![0-9a-f])"),
        "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\[^\s\"']+"),
        "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
        "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
        "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
    }
    definitions = {
        "scripts/build_ghc_family_v652_v1_preregistration.py",
        "scripts/build_ghc_family_v652_v1_evidence.py",
        "scripts/build_ghc_family_v652_v1_closeout.py",
        "scripts/ghc_family_v652_v1_evidence_validate.py",
        "scripts/ghc_family_v652_v1_closeout_validate.py",
        "scripts/ghc_family_v652_v1_final_validate.py",
        f"{PHASE_ROOT}/validation/x1-staged-privacy.json",
        f"{PHASE_ROOT}/validation/evidence-staged-privacy.json",
        f"{PHASE_ROOT}/validation/final-staged-privacy.json",
    }
    candidates = []
    confirmed = []
    scanned = 0
    for relative in sorted(paths):
        _, blob = git_blob(commit, relative)
        try:
            text = blob.decode("utf-8")
        except UnicodeDecodeError:
            continue
        scanned += 1
        for pattern_class, pattern in patterns.items():
            if pattern.search(text):
                disposition = "scanner_definition" if relative in definitions else "confirmed_payload_hit"
                row = {"path": relative, "pattern_class": pattern_class, "disposition": disposition}
                candidates.append(row)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(row)
    return {"scanned_files": scanned, "pattern_classes": sorted(patterns), "candidates": candidates, "confirmed_hits": confirmed}


def validate() -> dict:
    clean_before = run("git", "status", "--porcelain=v1", "--untracked-files=all") == ""
    head = run("git", "rev-parse", "HEAD")
    branch = run("git", "branch", "--show-current")

    test_rows = []
    test_total = 0
    for pattern in (
        "test_ghc_family_v652_v1_x1.py",
        "test_ghc_family_v652_v1_x2.py",
        "test_ghc_family_v652_v1_closeout.py",
    ):
        count, raw = run_test_pattern(pattern)
        test_rows.append({"pattern": pattern, "passed": count, "raw_output": raw})
        test_total += count

    detailed = json.loads(run(sys.executable, "-B", "scripts/ghc_family_v652_v1_detailed_validator.py"))
    minimal = json.loads(run(sys.executable, "-B", "scripts/ghc_family_v652_v1_minimal_validator.py"))

    json_errors = []
    json_count = 0
    for relative in sorted(path for path in diff_paths(SOURCE_HEAD, head) if path.startswith(f"{PHASE_ROOT}/") and path.endswith(".json")):
        try:
            _, blob = git_blob(head, relative)
            json.loads(blob.decode("utf-8"))
            json_count += 1
        except Exception as exc:
            json_errors.append({"path": relative, "error": type(exc).__name__})

    x1_paths = diff_paths(SOURCE_HEAD, X1_HEAD)
    evidence_paths = diff_paths(X1_HEAD, EVIDENCE_HEAD)
    final_delta_paths = diff_paths(EVIDENCE_HEAD, head)
    owner_paths = {path for path in diff_paths(SOURCE_HEAD, head) if is_owner_path(path)}
    x1_manifest = verify_manifest("validation/x1-staged-manifest.json", X1_HEAD, x1_paths)
    evidence_manifest = verify_manifest("validation/evidence-staged-manifest.json", EVIDENCE_HEAD, evidence_paths)
    final_manifest = verify_manifest("validation/final-owner-manifest.json", head, owner_paths)
    delta_manifest = verify_manifest("validation/final-delta-manifest.json", head, final_delta_paths)
    privacy = privacy_scan(head, owner_paths)

    truth = load("final/phase-truth.json")
    route = load("route/final-route-state.json")
    method = load("method-flow/method-flow-summary.json")
    documents = load("final/document-word-counts.json")
    baton = (ROOT / "handoffs/orin-thale-v652-v2-activation.md").read_text(encoding="utf-8")
    baton_words = len(re.findall(r"\b\w+(?:[-']\w+)*\b", baton))

    ancestry = {
        "source": subprocess.run(["git", "merge-base", "--is-ancestor", SOURCE_HEAD, head], cwd=REPO).returncode == 0,
        "x1": subprocess.run(["git", "merge-base", "--is-ancestor", X1_HEAD, head], cwd=REPO).returncode == 0,
        "evidence": subprocess.run(["git", "merge-base", "--is-ancestor", EVIDENCE_HEAD, head], cwd=REPO).returncode == 0,
    }
    phase_commit_count = int(run("git", "rev-list", "--count", f"{SOURCE_HEAD}..{head}"))
    merge_count = int(run("git", "rev-list", "--merges", "--count", f"{SOURCE_HEAD}..{head}"))
    parents = run("git", "show", "-s", "--format=%P", head).split()
    direct_parent = parents == [EVIDENCE_HEAD]
    diff_hygiene = run("git", "diff", "--check", SOURCE_HEAD, head) == ""

    upstream_name = run("git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
    upstream_head = run("git", "rev-parse", "@{u}")
    tracking_head = run("git", "rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_lines = run("git", "ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}").splitlines()
    live_head = live_lines[0].split()[0] if len(live_lines) == 1 else ""
    remote_equal = len({head, upstream_head, tracking_head, live_head}) == 1
    clean_after = run("git", "status", "--porcelain=v1", "--untracked-files=all") == ""

    checks = {
        "clean_before": clean_before,
        "exact_branch": branch == BRANCH,
        "scoped_tests": test_total == 22,
        "detailed": detailed["passed"] == detailed["check_count"] and not detailed["issues"],
        "minimal": minimal["passed"] == minimal["check_count"] and not minimal["issues"],
        "json": not json_errors,
        "x1_manifest": x1_manifest["valid"],
        "evidence_manifest": evidence_manifest["valid"],
        "final_owner_manifest": final_manifest["valid"],
        "final_delta_manifest": delta_manifest["valid"],
        "privacy": not privacy["confirmed_hits"],
        "truth": truth["effective_negatives"] == 8018 and truth["outcome_counts"] == {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1},
        "gates": truth["effective_open_gaps"] == 62 and truth["effective_exact_gates"] == 63,
        "method_flow": method["counts"]["methods"] == 9 and method["counts"]["witness_results"] == {"fail": 12, "pass": 12},
        "documents": documents["valid"] and 10000 <= baton_words <= 100000,
        "route_held": route["delivery_state"] == "PREPARED_NOT_SENT" and route["messages_sent"] == 0,
        "ancestry": all(ancestry.values()),
        "phase_commit_count": phase_commit_count == 3,
        "zero_merges": merge_count == 0,
        "one_final_parent": len(parents) == 1,
        "direct_evidence_parent": direct_parent,
        "diff_hygiene": diff_hygiene,
        "upstream_name": upstream_name == f"origin/{BRANCH}",
        "four_way_remote_equality": remote_equal,
        "clean_after": clean_after,
    }
    issues = [name for name, passed in checks.items() if not passed]
    return {
        "schema": "ghc.family.v652-v1.exact-final-validation.v1",
        "phase": "v652-v1",
        "owner": "Sable Rook",
        "exact_head": head,
        "branch": branch,
        "scoped_tests": {"passed": test_total, "failed": 0, "errors": 0, "selections": test_rows},
        "detailed": {"passed": detailed["passed"], "checks": detailed["check_count"]},
        "minimal": {"passed": minimal["passed"], "checks": minimal["check_count"]},
        "json_parse_count": json_count,
        "json_errors": json_errors,
        "manifests": {"x1": x1_manifest, "evidence": evidence_manifest, "final_owner": final_manifest, "final_delta": delta_manifest},
        "privacy": {"scanned_files": privacy["scanned_files"], "pattern_class_count": len(privacy["pattern_classes"]), "candidate_count": len(privacy["candidates"]), "confirmed_hit_count": len(privacy["confirmed_hits"]), "confirmed_hits": privacy["confirmed_hits"]},
        "baton_word_count": baton_words,
        "ancestry": ancestry,
        "phase_commit_count": phase_commit_count,
        "merge_count": merge_count,
        "final_parent_count": len(parents),
        "direct_evidence_parent": direct_parent,
        "remote_equality": {"local": head, "upstream": upstream_head, "tracking": tracking_head, "fresh_live": live_head, "equal": remote_equal},
        "full_repository_suite_run": False,
        "successful_canonical_passes": 1 if not issues else 0,
        "replay_performed": False,
        "same_owner_only": True,
        "independent_reproduction": False,
        "checks": checks,
        "issue_count": len(issues),
        "issues": issues,
        "valid": not issues,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": "One bounded same-owner exact-final canonical pass; no full repository suite, replay, independent reproduction, external audit, authority, production, or Stage 20 credit.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = Path(args.output).resolve()
    try:
        output.relative_to(REPO.resolve())
    except ValueError:
        pass
    else:
        raise SystemExit("exact-final receipt must be outside the repository")
    payload = validate()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    if not payload["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
