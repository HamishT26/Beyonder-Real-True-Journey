#!/usr/bin/env python3
"""Run the one canonical exact-final Ilyra v650-v8 validation pass."""

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
ROOT = REPO / "docs/ilyra-fen/v650-v8"
SOURCE = "f566d4b67bce4457cf5207f5409bbaa3427428a0"
X1 = "d8726faad1ae416ef31f98a8744901eeedfe3c56"
EVIDENCE = "325c410a16241cd8fa21706f82ab2bfd8ed47531"
ORIGINAL_FINAL = "4dc0a911415cc19b871008cb903e03605a7bfca5"
PREVIOUS_FINAL = "549e39d8020955188cdf49618a1e60ce4df205ba"


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO).decode("utf-8").strip()


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def manifest_issues(relative: str, base: str) -> tuple[list[str], int]:
    manifest = load(relative)
    issues = []
    for row in manifest["entries"]:
        try:
            oid = git("rev-parse", f"HEAD:{row['path']}")
            blob = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=REPO)
        except subprocess.CalledProcessError:
            issues.append(row["path"])
            continue
        if oid != row["git_blob"] or len(blob) != row["bytes"] or hashlib.sha256(blob).hexdigest() != row["sha256"]:
            issues.append(row["path"])
    changed = set(filter(None, git("diff", "--name-only", f"{base}..HEAD").splitlines()))
    declared = {row["path"] for row in manifest["entries"]} | set(manifest["self_exclusions"])
    issues.extend(sorted(changed ^ declared))
    return sorted(set(issues)), manifest["entry_count"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    receipt = Path(args.receipt)
    clean_before = not git("status", "--porcelain=v1", "--untracked-files=all")
    checks: list[dict[str, object]] = []
    def check(name: str, passed: bool) -> None:
        checks.append({"name": name, "passed": bool(passed)})

    head = git("rev-parse", "HEAD")
    branch = git("branch", "--show-current")
    check("exact_head", head == args.expected_head)
    check("branch_namespace", branch == "codex/GHC-Family/ilyra-fen-full-tools")
    check("clean_before", clean_before)
    check("direct_child_of_previous_final", git("rev-parse", "HEAD^") == PREVIOUS_FINAL)
    check("five_phase_commits", int(git("rev-list", "--count", f"{SOURCE}..HEAD")) == 5)
    check("zero_merges", int(git("rev-list", "--merges", "--count", f"{SOURCE}..HEAD")) == 0)
    check("one_final_parent", len(git("show", "-s", "--format=%P", "HEAD").split()) == 1)
    for name, anchor in (("source", SOURCE), ("x1", X1), ("evidence", EVIDENCE), ("original_final", ORIGINAL_FINAL), ("previous_final", PREVIOUS_FINAL)):
        check(f"{name}_ancestral", subprocess.run(["git", "merge-base", "--is-ancestor", anchor, "HEAD"], cwd=REPO).returncode == 0)

    env = os.environ.copy()
    env.update({"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"})
    tests = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_ghc_family_v650_v8_*.py", "-v"], cwd=REPO, capture_output=True, text=True, encoding="utf-8", env=env)
    test_text = tests.stdout + tests.stderr
    match = re.search(r"Ran (\d+) tests?", test_text)
    test_count = int(match.group(1)) if match else 0
    check("current_phase_tests_20_of_20", tests.returncode == 0 and test_count == 20)

    json_files = sorted(ROOT.rglob("*.json"))
    json_issues = []
    for path in json_files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            json_issues.append({"path": path.relative_to(REPO).as_posix(), "error": type(exc).__name__})
    check("all_phase_json_parse", not json_issues)

    owner_issues, owner_entries = manifest_issues("validation/final-owner-manifest.json", SOURCE)
    delta_issues, delta_entries = manifest_issues("validation/final-delta-manifest.json", EVIDENCE)
    check("owner_manifest_parity", not owner_issues)
    check("delta_manifest_parity", not delta_issues)
    owner_privacy = load("validation/final-owner-privacy.json")
    delta_privacy = load("validation/final-delta-privacy.json")
    check("owner_privacy_zero_confirmed", owner_privacy["confirmed_hit_count"] == 0 and len(owner_privacy["pattern_classes"]) == 5)
    check("delta_privacy_zero_confirmed", delta_privacy["confirmed_hit_count"] == 0 and len(delta_privacy["pattern_classes"]) == 5)

    truth = load("final/phase-truth.json")
    check("truth_counts", truth["effective_negatives"] == 6443 and truth["effective_open_gaps"] == 50 and truth["effective_exact_gates"] == 51)
    check("truth_distribution", truth["outcome_counts"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
    check("terminal_verdict", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20")
    check("route_held", load("route/final-phase-state.json")["terminal_route"] == "PREPARED_NOT_SENT")
    check("full_suite_not_run", truth["full_repository_suite_run"] is False)
    check("no_replay_lane", truth["replay_lane_created"] is False)

    document_issues = []
    max_words = 0
    baton_words = 0
    for path in sorted(list(ROOT.rglob("*.md")) + list(ROOT.rglob("*.html"))):
        text = path.read_text(encoding="utf-8")
        if path.suffix == ".html":
            text = re.sub(r"<[^>]+>", " ", text)
        words = len(re.findall(r"\b\w+\b", text, flags=re.UNICODE))
        max_words = max(max_words, words)
        if path.name == "sable-rook-v651-v1-activation.md":
            baton_words = words
        elif words > 6000:
            document_issues.append(path.relative_to(REPO).as_posix())
    check("ordinary_document_cap", not document_issues)
    check("baton_range", 8000 <= baton_words <= 20000)

    local = head
    upstream = git("rev-parse", "@{upstream}")
    tracking = git("rev-parse", f"refs/remotes/origin/{branch}")
    live_line = git("ls-remote", "origin", f"refs/heads/{branch}")
    live = live_line.split()[0] if live_line else ""
    check("four_way_remote_equality", local == upstream == tracking == live)
    check("zero_divergence", git("rev-list", "--left-right", "--count", "HEAD...@{upstream}").split() == ["0", "0"])
    clean_after = not git("status", "--porcelain=v1", "--untracked-files=all")
    check("clean_after", clean_after)

    payload = {"schema": "ghc.family.v650-v8.exact-final-validation.external.v1", "exact_head": head, "branch": branch, "check_count": len(checks), "passed_count": sum(bool(row["passed"]) for row in checks), "checks": checks, "valid": all(bool(row["passed"]) for row in checks), "scoped_tests_run": test_count, "test_output_tail": test_text.strip().splitlines()[-4:], "json_parse_count": len(json_files), "json_issues": json_issues, "owner_manifest_entries": owner_entries, "owner_manifest_issues": owner_issues, "delta_manifest_entries": delta_entries, "delta_manifest_issues": delta_issues, "owner_privacy_files": owner_privacy["scanned_file_count"], "owner_privacy_candidates": owner_privacy["candidate_count"], "owner_privacy_confirmed_hits": owner_privacy["confirmed_hit_count"], "delta_privacy_files": delta_privacy["scanned_file_count"], "delta_privacy_candidates": delta_privacy["candidate_count"], "delta_privacy_confirmed_hits": delta_privacy["confirmed_hit_count"], "baton_words": baton_words, "max_document_words_including_baton": max_words, "full_repository_suite_run": False, "post_success_replay": False, "same_owner_only": True, "independent_reproduction": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": "One canonical exact-final non-Eiren scoped pass; not a replay, full-suite result, independent reproduction, external audit, production assurance, complete privacy or accessibility, professional or clinical validation, legal or cultural ratification, Maori-authority review, empirical GMUT confirmation, or Stage 20 authority."}
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"checks": len(checks), "passed": payload["passed_count"], "tests": test_count, "json": len(json_files), "owner_manifest": owner_entries, "delta_manifest": delta_entries, "privacy_hits": owner_privacy["confirmed_hit_count"] + delta_privacy["confirmed_hit_count"], "baton_words": baton_words, "valid": payload["valid"]}, sort_keys=True))
    return 0 if payload["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
