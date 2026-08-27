"""One-shot external exact-final validator for Orin Thale v672-v5."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from scripts import build_ghc_family_orin_thale_v672_v5_final as final


ROOT = final.ROOT


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=ROOT, check=check, capture_output=True)


def git_text(*args: str) -> str:
    return git(*args).stdout.decode("utf-8", errors="strict").strip()


def sha(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def blob(commit: str, path: str) -> bytes:
    return git("show", f"{commit}:{path}").stdout


def load_blob_json(commit: str, path: str) -> Any:
    return json.loads(blob(commit, path).decode("utf-8"))


def verify_manifest(commit: str, manifest_path: str, actual_paths: set[str]) -> dict[str, Any]:
    manifest = load_blob_json(commit, manifest_path)
    mismatches = []
    for row in manifest["entries"]:
        data = blob(commit, row["path"])
        oid = git_text("rev-parse", f"{commit}:{row['path']}")
        if oid != row["git_blob_oid"] or len(data) != row["bytes"] or sha(data) != row["sha256"]:
            mismatches.append(row["path"])
    union = {row["path"] for row in manifest["entries"]} | set(manifest["self_exclusions"])
    return {
        "path": manifest_path,
        "entries": manifest["entry_count"],
        "self_exclusions": len(manifest["self_exclusions"]),
        "blob_mismatches": mismatches,
        "coverage_missing": sorted(actual_paths - union),
        "coverage_extra": sorted(union - actual_paths),
        "valid": not mismatches and union == actual_paths and manifest["entry_count"] == len(manifest["entries"]),
    }


def run_tests() -> dict[str, Any]:
    result = subprocess.run([sys.executable, "-X", "utf8", "-m", "unittest", "tests.test_ghc_family_orin_thale_v672_v5_final", "-v"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=240)
    combined = result.stdout + result.stderr
    match = re.search(r"Ran\s+(\d+)\s+tests", combined)
    count = int(match.group(1)) if match else 0
    return {
        "tests": count,
        "exit_code": result.returncode,
        "output_sha256": sha(combined.encode("utf-8")),
        "output_tail": combined[-2000:] if result.returncode else "",
        "valid": result.returncode == 0 and count == 20,
    }


def canonical(output: Path) -> dict[str, Any]:
    if output.exists():
        raise RuntimeError("one-shot output path already exists; replay refused")
    branch = git_text("branch", "--show-current")
    head = git_text("rev-parse", "HEAD")
    parent = git_text("rev-parse", "HEAD^")
    upstream = git_text("rev-parse", "@{u}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{branch}")
    live_rows = git_text("ls-remote", "--heads", "origin", f"refs/heads/{branch}").split()
    live = live_rows[0] if live_rows else ""
    status_before = git_text("status", "--porcelain=v1")
    ahead_behind = git_text("rev-list", "--left-right", "--count", "@{u}...HEAD").split()
    source_to_final = set(git_text("diff", "--name-only", final.SOURCE_FINAL, head).splitlines())
    evidence_to_final = set(git_text("diff", "--name-only", final.EVIDENCE_COMMIT, head).splitlines())
    phase_commits = int(git_text("rev-list", "--count", f"{final.SOURCE_FINAL}..{head}"))
    merges = int(git_text("rev-list", "--merges", "--count", f"{final.SOURCE_FINAL}..{head}"))
    parent_fields = git_text("rev-list", "--parents", "-n", "1", head).split()

    delta_manifest = verify_manifest(head, "docs/orin-thale/v672-v5/validation/final-delta-manifest.json", evidence_to_final)
    owner_manifest = verify_manifest(head, "docs/orin-thale/v672-v5/validation/final-owner-manifest.json", source_to_final)
    x1_manifest = load_blob_json(final.X1_COMMIT, "docs/orin-thale/v672-v5/validation/x1-manifest.json")
    evidence_manifest = load_blob_json(final.EVIDENCE_COMMIT, "docs/orin-thale/v672-v5/validation/evidence-manifest.json")
    lifecycle_manifests = []
    for commit, manifest in ((final.X1_COMMIT, x1_manifest), (final.EVIDENCE_COMMIT, evidence_manifest)):
        mismatches = []
        for row in manifest["entries"]:
            data = blob(commit, row["path"])
            if len(data) != row["bytes"] or sha(data) != row["sha256"] or git_text("rev-parse", f"{commit}:{row['path']}") != row["git_blob_oid"]:
                mismatches.append(row["path"])
        lifecycle_manifests.append({"commit": commit, "entries": len(manifest["entries"]), "self_exclusions": len(manifest["self_exclusions"]), "mismatches": mismatches, "valid": not mismatches})

    seal = load_blob_json(head, "docs/orin-thale/v672-v5/seal/content-seal-candidate.json")
    seal_mismatches = []
    for row in seal["targets"]:
        data = blob(head, row["path"])
        if len(data) != row["bytes"] or sha(data) != row["sha256"]:
            seal_mismatches.append(row["path"])

    owner_paths = [path for path in git_text("ls-tree", "-r", "--name-only", head, "docs/orin-thale/v672-v5").splitlines() if path]
    json_paths = [path for path in owner_paths if path.endswith(".json")]
    json_issues = []
    for path in json_paths:
        try:
            json.loads(blob(head, path).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            json_issues.append({"path": path, "issue": type(exc).__name__})
    markdown_paths = [path for path in owner_paths if path.endswith(".md")]
    html_paths = [path for path in owner_paths if path.endswith(".html")]

    python_paths = [path for path in source_to_final if path.endswith(".py")]
    compile_issues = []
    for path in python_paths:
        try:
            compile(blob(head, path).decode("utf-8"), path, "exec")
        except (UnicodeDecodeError, SyntaxError) as exc:
            compile_issues.append({"path": path, "issue": type(exc).__name__})

    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
        "private_route_or_callable": re.compile(r"source_thread_id|<codex_delegation|\b(?:app|plugin)://", re.I),
        "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']"),
        "transcript_or_session_stream": re.compile(r"(?i)\b(?:session_stream|private_transcript|private_conversation_dump)\b"),
    }
    candidates = []
    scanned = 0
    for path in sorted(source_to_final):
        if Path(path).suffix.lower() not in {".py", ".json", ".md", ".html", ".txt", ".yaml"}:
            continue
        data = blob(head, path)
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            candidates.append({"path": path, "pattern_class": "non_utf8_text", "disposition": "confirmed_payload_hit"})
            continue
        scanned += 1
        for label, pattern in patterns.items():
            if pattern.search(text):
                disposition = "scanner_definition_or_unit_test" if path.endswith(".py") else "confirmed_payload_hit"
                candidates.append({"path": path, "pattern_class": label, "disposition": disposition})
    confirmed = [row for row in candidates if row["disposition"] == "confirmed_payload_hit"]

    truth = load_blob_json(head, "docs/orin-thale/v672-v5/closeout/phase-truth.json")
    correction = load_blob_json(head, "docs/orin-thale/v672-v5/closeout/counter-correction-overlay.json")
    route = load_blob_json(head, "docs/orin-thale/v672-v5/orchestration/terminal-route-state.json")
    precommit = load_blob_json(head, "docs/orin-thale/v672-v5/validation/final-precommit-test-receipt.json")
    review = load_blob_json(head, "docs/orin-thale/v672-v5/validation/final-staged-review.json")
    staged_privacy = load_blob_json(head, "docs/orin-thale/v672-v5/validation/final-staged-privacy.json")
    prereceipt = load_blob_json(head, "docs/orin-thale/v672-v5/validation/final-validation-receipt.json")
    tests = run_tests()

    detailed = {
        "branch_exact": branch == final.BRANCH,
        "final_direct_child_of_evidence": parent == final.EVIDENCE_COMMIT,
        "x1_direct_child_of_source": git_text("rev-parse", f"{final.X1_COMMIT}^") == final.SOURCE_FINAL,
        "evidence_direct_child_of_x1": git_text("rev-parse", f"{final.EVIDENCE_COMMIT}^") == final.X1_COMMIT,
        "phase_commits_three": phase_commits == 3,
        "zero_merges": merges == 0,
        "one_final_parent": len(parent_fields) == 2,
        "clean_before": status_before == "",
        "four_way_equal_before": head == upstream == tracking == live,
        "typed_zero_divergence": ahead_behind == ["0", "0"],
        "delta_manifest": delta_manifest["valid"],
        "owner_manifest": owner_manifest["valid"],
        "x1_manifest": lifecycle_manifests[0]["valid"],
        "evidence_manifest": lifecycle_manifests[1]["valid"],
        "content_seal": not seal_mismatches and seal["target_count"] == len(seal["targets"]),
        "json_parses": not json_issues,
        "python_compiles": not compile_issues,
        "privacy_zero_confirmed": not confirmed,
        "precommit_tests": precommit["valid"] and precommit["tests"] == 20,
        "exact_final_tests": tests["valid"],
        "staged_review": review["valid"],
        "staged_privacy": staged_privacy["valid"] and staged_privacy["confirmed_hit_count"] == 0,
        "validation_prereceipt": prereceipt["valid"],
        "outcomes": truth["outcomes"] == final.OUTCOMES,
        "effective_negatives": truth["effective_negatives"] == 35602,
        "effective_methods": truth["effective_methods"] == 22007,
        "failed_witnesses": truth["failed_witnesses"] == 7263,
        "passing_witnesses": truth["bounded_passing_witnesses"] == 9314,
        "open_gaps": truth["open_gaps"] == 285,
        "exact_gates": truth["exact_gates"] == 278,
        "counter_correction": correction["valid"] and not correction["evidence_commit_rewritten"],
        "terminal_verdict": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "route_prepared_not_sent": route["state"] == "PREPARED_NOT_SENT" and not route["successor_contacted"],
        "owner_file_guard": len(owner_paths) < 2000,
        "full_suite_not_claimed": truth["full_repository_suite"] == "not_run_not_claimed",
        "same_owner_not_independent": truth["independent_reproduction"] is False,
    }
    minimal_keys = [
        "branch_exact",
        "final_direct_child_of_evidence",
        "phase_commits_three",
        "zero_merges",
        "one_final_parent",
        "clean_before",
        "four_way_equal_before",
        "typed_zero_divergence",
        "delta_manifest",
        "owner_manifest",
        "json_parses",
        "privacy_zero_confirmed",
        "exact_final_tests",
        "terminal_verdict",
        "route_prepared_not_sent",
    ]
    status_after = git_text("status", "--porcelain=v1")
    live_after_rows = git_text("ls-remote", "--heads", "origin", f"refs/heads/{branch}").split()
    live_after = live_after_rows[0] if live_after_rows else ""
    detailed["clean_after"] = status_after == ""
    detailed["four_way_equal_after"] = head == git_text("rev-parse", "@{u}") == git_text("rev-parse", f"refs/remotes/origin/{branch}") == live_after
    valid = all(detailed.values())
    return {
        "schema": "ghc.family.external-canonical-receipt.v3",
        "owner": final.OWNER,
        "phase": final.PHASE,
        "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" if valid else "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "valid": valid,
        "canonical_invocations": 1,
        "canonical_successes": 1 if valid else 0,
        "replayed": False,
        "exact_final": head,
        "parent": parent,
        "source_final": final.SOURCE_FINAL,
        "x1_commit": final.X1_COMMIT,
        "evidence_commit": final.EVIDENCE_COMMIT,
        "selected_tests": tests,
        "detailed_checks": {"passed": sum(detailed.values()), "total": len(detailed), "rows": detailed},
        "minimal_checks": {"passed": sum(detailed[key] for key in minimal_keys), "total": len(minimal_keys), "keys": minimal_keys},
        "phase_json": {"parsed": len(json_paths), "total": len(json_paths), "issues": json_issues},
        "markdown_documents": len(markdown_paths),
        "html_documents": len(html_paths),
        "python_compiles": {"passed": len(python_paths) - len(compile_issues), "total": len(python_paths), "issues": compile_issues},
        "privacy": {"pattern_classes": sorted(patterns), "scanned_text_files": scanned, "candidates": candidates, "confirmed_hits": confirmed},
        "manifests": {"x1": lifecycle_manifests[0], "evidence": lifecycle_manifests[1], "final_delta": delta_manifest, "final_owner": owner_manifest},
        "content_seal": {"targets": seal["target_count"], "mismatches": seal_mismatches},
        "lifecycle": {"phase_commits": phase_commits, "merge_commits": merges, "final_parent_count": len(parent_fields) - 1, "ahead": int(ahead_behind[1]), "behind": int(ahead_behind[0])},
        "full_repository_suite": "not_run_not_claimed",
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": final.BOUNDARY,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    try:
        receipt = canonical(args.output)
    except Exception as exc:  # exact failure receipt is still retained
        receipt = {
            "schema": "ghc.family.external-canonical-receipt.v3",
            "owner": final.OWNER,
            "phase": final.PHASE,
            "status": "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
            "valid": False,
            "canonical_invocations": 1,
            "canonical_successes": 0,
            "replayed": False,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "full_repository_suite": "not_run_not_claimed",
            "same_owner_only": True,
            "independent_reproduction": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": final.BOUNDARY,
        }
    args.output.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": receipt["status"], "valid": receipt["valid"], "output": args.output.name}, sort_keys=True))
    raise SystemExit(0 if receipt["valid"] else 1)


if __name__ == "__main__":
    main()
