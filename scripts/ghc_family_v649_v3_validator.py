#!/usr/bin/env python3
"""Detailed, minimal, and exact-head validators for Sable v649-v3."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "sable-rook" / "v649-v3"
SOURCE = "a801ebd12f89f0afdc224a65ea311239ad5a94ca"
X1 = "dd1da40467292a06c130e0edf3ba8fcbb7b083bd"
BRANCH = "codex/GHC-Family/sable-rook-full-tools"
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}

PATTERNS = {
    "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"),
    "private_absolute_path": re.compile(r"(?i)\b[A-Z]:[\\/]Users[\\/][^\s\"']+"),
    "delegation_markup": re.compile(r"(?i)<\/?codex_delegation\b"),
    "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|password|secret|token)\s*[:=]\s*[\"'][^\"']+[\"']"),
    "private_uri": re.compile(r"(?i)\b(?:codex|thread|app)://[^\s\"']+"),
}


def git(*args: str, check: bool = True) -> str:
    completed = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=False)
    if check and completed.returncode != 0:
        raise RuntimeError((completed.stderr or completed.stdout).strip())
    return completed.stdout.strip()


def load(relative: str) -> dict[str, Any]:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def parse_json_and_scan() -> tuple[int, int, list[dict[str, str]], list[str], int]:
    json_count = 0
    parse_issues: list[str] = []
    hits: list[dict[str, str]] = []
    public_files = [path for path in PHASE.rglob("*") if path.is_file()]
    for path in public_files:
        relative = path.relative_to(ROOT).as_posix()
        if path.suffix.lower() == ".json":
            try:
                json.loads(path.read_text(encoding="utf-8"))
                json_count += 1
            except Exception as exc:  # pragma: no cover - fail receipt
                parse_issues.append(f"{relative}:{type(exc).__name__}")
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for class_name, pattern in PATTERNS.items():
            if pattern.search(text):
                hits.append({"class": class_name, "path": relative})
    return len(public_files), json_count, hits, parse_issues, len(PATTERNS)


def x1_blob_parity() -> tuple[int, list[str]]:
    paths = [line for line in git("diff-tree", "--no-commit-id", "--name-only", "-r", X1).splitlines() if line]
    mismatches: list[str] = []
    head = git("rev-parse", "HEAD")
    for path in paths:
        if git("rev-parse", f"{X1}:{path}", check=False) != git("rev-parse", f"{head}:{path}", check=False):
            mismatches.append(path)
    return len(paths), mismatches


def commit_manifest_parity(commit: str, relative: str) -> tuple[bool, dict[str, Any]]:
    repository_path = f"docs/sable-rook/v649-v3/validation/{relative}"
    try:
        manifest = json.loads(git("show", f"{commit}:{repository_path}"))
    except Exception as exc:
        return False, {"manifest": relative, "error": type(exc).__name__}
    entries = manifest.get("entries", [])
    exclusions = manifest.get("self_exclusions", [])
    declared = {row["path"] for row in entries} | set(exclusions)
    changed = {line for line in git("diff-tree", "--no-commit-id", "--name-only", "-r", commit).splitlines() if line}
    coverage_missing = sorted(changed - declared)
    coverage_extra = sorted(declared - changed)
    blob_mismatches = []
    for row in entries:
        observed = git("rev-parse", f"{commit}:{row['path']}", check=False)
        if observed != row["git_blob"]:
            blob_mismatches.append(row["path"])
    valid = not coverage_missing and not coverage_extra and not blob_mismatches
    return valid, {"manifest": relative, "entries": len(entries), "exclusions": len(exclusions), "changed": len(changed), "coverage_missing": coverage_missing, "coverage_extra": coverage_extra, "blob_mismatches": blob_mismatches}


def word_cap() -> tuple[int, list[str]]:
    checked = 0
    issues: list[str] = []
    for path in PHASE.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".html"}:
            checked += 1
            words = len(re.findall(r"\b\w+\b", path.read_text(encoding="utf-8")))
            if words > 6000:
                issues.append(f"{path.relative_to(ROOT).as_posix()}:{words}")
    return checked, issues


def check_result(name: str, condition: bool, observed: Any) -> dict[str, Any]:
    return {"check": name, "passed": bool(condition), "observed": observed}


def phase_checks(include_terminal: bool, expected_head: str | None, evidence_head: str | None) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    public_count, json_count, privacy_hits, parse_issues, pattern_count = parse_json_and_scan()
    ledger = load("x2-proposal-ledger.json")
    mutations = load("validation/synthetic-mutation-results.json")
    safe = load("portfolios/safe-now-execution.json")
    candidates = load("portfolios/candidate-execution.json")
    skills = load("portfolios/skill-execution.json")
    runners = load("portfolios/runner-execution.json")
    cleanup = load("portfolios/clean-fix-refine-execution.json")
    negatives_name = "retained-negative-register-final.json" if (PHASE / "retained-negative-register-final.json").exists() else "retained-negative-register-evidence.json"
    gates_name = "exact-open-gate-register-final.json" if (PHASE / "exact-open-gate-register-final.json").exists() else "exact-open-gate-register-evidence.json"
    negatives = load(negatives_name)
    gates = load(gates_name)
    route_name = "orchestration/phase-state-final.json" if (PHASE / "orchestration/phase-state-final.json").exists() else "orchestration/terminal-route-hold-evidence.json"
    route = load(route_name)
    truth_name = "phase-truth-final.json" if (PHASE / "phase-truth-final.json").exists() else "phase-truth-evidence.json"
    truth = load(truth_name)
    word_files, word_issues = word_cap()
    x1_paths, x1_mismatches = x1_blob_parity()
    outcome_counts = Counter(row["observed_outcome"] for row in ledger["proposals"])
    head = git("rev-parse", "HEAD")
    branch = git("branch", "--show-current")
    status = git("status", "--porcelain=v1")
    checks = [
        check_result("ten_core_proposals", ledger["proposal_count"] == 10, ledger["proposal_count"]),
        check_result("four_outcome_vocabulary", set(outcome_counts) <= ALLOWED, sorted(outcome_counts)),
        check_result("outcome_distribution", outcome_counts == Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}), dict(outcome_counts)),
        check_result("seventy_mutations_executed", mutations["executed"] == 70, mutations["executed"]),
        check_result("seventy_mutations_rejected", mutations["rejected"] == 70 and mutations["unexpected_acceptances"] == 0, mutations["rejected"]),
        check_result("safe_floor", safe["completed_bounded"] == 30, safe["completed_bounded"]),
        check_result("candidate_floor", candidates["completed_bounded"] == 20, candidates["completed_bounded"]),
        check_result("skill_floor", skills["valid_count"] == 20, skills["valid_count"]),
        check_result("runner_floor", runners["valid_count"] == 10, runners["valid_count"]),
        check_result("cleanup_floor", cleanup["completed_additive"] == 30, cleanup["completed_additive"]),
        check_result("skill_no_global_install", skills["global_install"] is False, skills["global_install"]),
        check_result("skill_no_subagent_forward_test", skills["subagent_forward_test"] == "prohibited_not_run", skills["subagent_forward_test"]),
        check_result("complete_json_parse", not parse_issues, {"parsed": json_count, "issues": parse_issues}),
        check_result("five_privacy_classes", pattern_count == 5, pattern_count),
        check_result("zero_confirmed_privacy_hits", not privacy_hits, privacy_hits),
        check_result("document_word_cap", not word_issues, {"checked": word_files, "issues": word_issues}),
        check_result("owner_file_threshold", public_count < 15000, public_count),
        check_result("x1_immutable_blob_parity", not x1_mismatches, {"paths": x1_paths, "mismatches": x1_mismatches}),
        check_result("open_gap_count", gates["effective_open_gaps"] == 37, gates["effective_open_gaps"]),
        check_result("exact_gate_count", gates["effective_exact_gates"] == 38, gates["effective_exact_gates"]),
        check_result("negatives_preserved", negatives.get("none_erased", True) is True and negatives["current_effective"] >= 4921, negatives["current_effective"]),
        check_result("stage20_not_ready", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", truth["terminal_verdict"]),
        check_result("full_suite_not_run", truth["full_repository_suite"] is False, truth["full_repository_suite"]),
        check_result("no_replay", truth["replay"] is False, truth["replay"]),
        check_result("route_held", route["state"] == "PREPARED_NOT_SENT", route["state"]),
        check_result("expected_branch", branch == BRANCH, branch),
        check_result("worktree_clean", status == "", len(status.splitlines()) if status else 0),
    ]
    if include_terminal:
        merge_count = int(git("rev-list", "--count", "--merges", f"{SOURCE}..{head}"))
        phase_commits = int(git("rev-list", "--count", f"{SOURCE}..{head}"))
        parent_count = len(git("show", "-s", "--format=%P", head).split())
        x1_manifest_valid, x1_manifest = commit_manifest_parity(X1, "x1-staged-manifest.json")
        evidence_manifest_valid, evidence_manifest = commit_manifest_parity(evidence_head or "", "evidence-staged-manifest.json") if evidence_head else (False, {"error": "missing_evidence_head"})
        final_manifest_valid, final_manifest = commit_manifest_parity(head, "final-staged-manifest.json")
        stage_union = set()
        for commit in (X1, evidence_head or "", head):
            if commit:
                stage_union.update(line for line in git("diff-tree", "--no-commit-id", "--name-only", "-r", commit).splitlines() if line)
        source_to_head = {line for line in git("diff", "--name-only", f"{SOURCE}..{head}").splitlines() if line}
        owner_union_valid = stage_union == source_to_head and all(path.startswith("docs/sable-rook/v649-v3/") or path.startswith("scripts/ghc_family_v649_v3_") or path.startswith("scripts/build_ghc_family_v649_v3_") or path.startswith("tests/test_ghc_family_v649_v3_") for path in source_to_head)
        checks.extend(
            [
                check_result("source_ancestral", subprocess.run(["git", "merge-base", "--is-ancestor", SOURCE, head], cwd=ROOT).returncode == 0, SOURCE),
                check_result("x1_ancestral", subprocess.run(["git", "merge-base", "--is-ancestor", X1, head], cwd=ROOT).returncode == 0, X1),
                check_result("evidence_ancestral", bool(evidence_head) and subprocess.run(["git", "merge-base", "--is-ancestor", evidence_head or "", head], cwd=ROOT).returncode == 0, evidence_head),
                check_result("three_phase_commits", phase_commits == 3, phase_commits),
                check_result("zero_merges", merge_count == 0, merge_count),
                check_result("one_final_parent", parent_count == 1, parent_count),
                check_result("exact_head", bool(expected_head) and head == expected_head, head),
                check_result("x1_commit_manifest_parity", x1_manifest_valid, x1_manifest),
                check_result("evidence_commit_manifest_parity", evidence_manifest_valid, evidence_manifest),
                check_result("final_commit_manifest_parity", final_manifest_valid, final_manifest),
                check_result("owner_union_manifest_parity", owner_union_valid, {"stage_union": len(stage_union), "source_to_head": len(source_to_head)}),
            ]
        )
    context = {"public_file_count": public_count, "json_parse_count": json_count, "privacy_pattern_classes": pattern_count, "privacy_hits": privacy_hits, "word_documents": word_files, "x1_paths": x1_paths, "head": head, "branch": branch}
    return checks, context


def minimal_checks(expected_head: str | None, evidence_head: str | None) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    detailed, context = phase_checks(False, expected_head, evidence_head)
    names = [
        "ten_core_proposals", "four_outcome_vocabulary", "outcome_distribution",
        "seventy_mutations_executed", "seventy_mutations_rejected", "safe_floor",
        "candidate_floor", "skill_floor", "runner_floor", "cleanup_floor",
        "complete_json_parse", "five_privacy_classes", "zero_confirmed_privacy_hits",
        "document_word_cap", "owner_file_threshold", "x1_immutable_blob_parity",
        "open_gap_count", "exact_gate_count", "stage20_not_ready", "route_held",
    ]
    lookup = {row["check"]: row for row in detailed}
    return [lookup[name] for name in names], context


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("detailed", "minimal", "terminal"), required=True)
    parser.add_argument("--expected-head")
    parser.add_argument("--evidence-head")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.mode == "minimal":
        checks, context = minimal_checks(args.expected_head, args.evidence_head)
    else:
        checks, context = phase_checks(args.mode == "terminal", args.expected_head, args.evidence_head)
    issues = [row["check"] for row in checks if not row["passed"]]
    payload = {
        "schema": f"ghc.family.v649-v3.validation.{args.mode}.v1",
        "mode": args.mode,
        "check_count": len(checks),
        "passed_count": len(checks) - len(issues),
        "issue_count": len(issues),
        "issues": issues,
        "checks": checks,
        "context": context,
        "valid": not issues,
        "boundary": "Same-owner bounded validation under shared infrastructure; not independent reproduction or broader certification.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"mode": args.mode, "passed": payload["passed_count"], "checks": payload["check_count"], "issues": issues}, sort_keys=True))
    return 0 if payload["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
