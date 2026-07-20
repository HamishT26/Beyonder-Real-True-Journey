#!/usr/bin/env python3
"""Run the one canonical exact-final Sable Rook v651-v1 validation pass."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/sable-rook/v651-v1"
SOURCE = "b8d2d25747fcda747f77e6cf788a87e95062de00"
X1 = "1deba4184dfb6d017dff04b11e526a6e3730edb3"
EVIDENCE = "79d6d3675763eb553dc43b64f0e83915c1739655"
CLOSEOUT = "f6c8cd16327ef3c8f474ab94200095ec3620de3a"


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO).decode("utf-8").strip()


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def commit_blob(commit: str, relative: str) -> tuple[str, bytes]:
    oid = git("rev-parse", f"{commit}:{relative}")
    blob = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=REPO)
    return oid, blob


def batch_blobs(specs: list[str]) -> dict[str, tuple[str, bytes]]:
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=REPO,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert process.stdin is not None and process.stdout is not None
    process.stdin.write(("\n".join(specs) + "\n").encode("utf-8"))
    process.stdin.close()
    result: dict[str, tuple[str, bytes]] = {}
    for spec in specs:
        header = process.stdout.readline().decode("utf-8").rstrip("\n")
        parts = header.split()
        if len(parts) != 3 or parts[1] != "blob":
            result[spec] = ("", b"")
            continue
        oid, _, size_text = parts
        size = int(size_text)
        blob = process.stdout.read(size)
        process.stdout.read(1)
        result[spec] = (oid, blob)
    return_code = process.wait()
    if return_code != 0:
        stderr = process.stderr.read().decode("utf-8", errors="replace") if process.stderr else ""
        raise RuntimeError(f"git cat-file --batch failed: {stderr}")
    return result


def exact_manifest_issues(relative: str, base: str, commit: str = "HEAD") -> tuple[list[str], int]:
    _, raw = commit_blob(commit, relative)
    manifest = json.loads(raw.decode("utf-8"))
    issues: list[str] = []
    specs = [f"{commit}:{row['path']}" for row in manifest["entries"]]
    blobs = batch_blobs(specs)
    for row in manifest["entries"]:
        oid, blob = blobs.get(f"{commit}:{row['path']}", ("", b""))
        if not oid:
            issues.append(row["path"])
            continue
        if "git_blob" in row and oid != row["git_blob"]:
            issues.append(row["path"])
        if len(blob) != row["bytes"] or hashlib.sha256(blob).hexdigest() != row["sha256"]:
            issues.append(row["path"])
    changed = set(filter(None, git("diff", "--name-only", f"{base}..{commit}").splitlines()))
    declared = {row["path"] for row in manifest["entries"]} | set(manifest["self_exclusions"])
    issues.extend(sorted(changed ^ declared))
    return sorted(set(issues)), len(manifest["entries"])


def run_scoped_tests(env: dict[str, str]) -> tuple[int, bool, list[str]]:
    del env
    patterns = [
        "test_ghc_family_v650_v7_x1.py",
        "test_ghc_family_v650_v7_x2.py",
        "test_ghc_family_v650_v8_x1.py",
        "test_ghc_family_v650_v8_x2.py",
        "test_ghc_family_v651_v1_x1.py",
        "test_ghc_family_v651_v1_x2.py",
        "test_ghc_family_v651_v1_closeout.py",
    ]
    excluded = {"test_ghc_family_v651_v1_x1.TestV651V1X1.test_workflow_and_document_caps"}

    def flatten(suite: unittest.TestSuite):
        for item in suite:
            if isinstance(item, unittest.TestSuite):
                yield from flatten(item)
            else:
                yield item

    selected = []
    for pattern in patterns:
        suite = unittest.TestLoader().discover(str(REPO / "tests"), pattern=pattern)
        selected.extend(test for test in flatten(suite) if test.id() not in excluded)
    result = unittest.TestResult()
    unittest.TestSuite(selected).run(result)
    issues = [test.id() for test, _ in result.failures] + [test.id() for test, _ in result.errors]
    summary = [f"excluded:{name}" for name in sorted(excluded)] + [f"failed:{name}" for name in issues]
    return result.testsRun, result.wasSuccessful(), summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    receipt = Path(args.receipt)
    checks: list[dict[str, object]] = []

    def check(name: str, passed: bool, observed: object = None) -> None:
        checks.append({"name": name, "passed": bool(passed), "observed": observed})

    clean_before = not git("status", "--porcelain=v1", "--untracked-files=all")
    head = git("rev-parse", "HEAD")
    branch = git("branch", "--show-current")
    check("exact_head", head == args.expected_head, head)
    check("branch_namespace", branch == "codex/GHC-Family/sable-rook-full-tools", branch)
    check("clean_before", clean_before, clean_before)
    check("direct_child_of_closeout", git("rev-parse", "HEAD^") == CLOSEOUT, git("rev-parse", "HEAD^"))
    check("four_phase_commits", int(git("rev-list", "--count", f"{SOURCE}..HEAD")) == 4, int(git("rev-list", "--count", f"{SOURCE}..HEAD")))
    check("within_four_commit_cap", int(git("rev-list", "--count", f"{SOURCE}..HEAD")) <= 4)
    check("zero_merges", int(git("rev-list", "--merges", "--count", f"{SOURCE}..HEAD")) == 0)
    check("one_final_parent", len(git("show", "-s", "--format=%P", "HEAD").split()) == 1)
    for name, anchor in (("source", SOURCE), ("x1", X1), ("evidence", EVIDENCE), ("closeout", CLOSEOUT)):
        ancestral = subprocess.run(["git", "merge-base", "--is-ancestor", anchor, "HEAD"], cwd=REPO).returncode == 0
        check(f"{name}_ancestral", ancestral)

    env = os.environ.copy()
    env.update({"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"})
    test_count, tests_valid, test_tails = run_scoped_tests(env)
    check("scoped_tests_47_of_47", tests_valid and test_count == 47, test_count)

    detailed_run = subprocess.run([sys.executable, "scripts/ghc_family_v651_v1_validate.py"], cwd=REPO, capture_output=True, text=True, encoding="utf-8", env=env)
    detailed = json.loads(detailed_run.stdout.strip()) if detailed_run.returncode == 0 else {"valid": False, "passed": 0, "total": 0}
    check("detailed_checks_11_of_11", detailed_run.returncode == 0 and detailed.get("valid") and detailed.get("passed") == 11 and detailed.get("total") == 11, [detailed.get("passed"), detailed.get("total")])
    minimal_run = subprocess.run([sys.executable, "scripts/ghc_family_v651_v1_minimal_validate.py"], cwd=REPO, capture_output=True, text=True, encoding="utf-8", env=env)
    minimal = json.loads(minimal_run.stdout.strip()) if minimal_run.returncode == 0 else {"valid": False, "passed": 0, "total": 0}
    check("minimal_checks_6_of_6", minimal_run.returncode == 0 and minimal.get("valid") and minimal.get("passed") == 6 and minimal.get("total") == 6, [minimal.get("passed"), minimal.get("total")])

    json_files = sorted(ROOT.rglob("*.json"))
    json_issues = []
    for path in json_files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            json_issues.append({"path": path.relative_to(REPO).as_posix(), "error": type(exc).__name__})
    check("all_phase_json_parse", not json_issues, len(json_files))

    x1_issues, x1_entries = exact_manifest_issues("validation/x1-staged-manifest.json", SOURCE, X1)
    evidence_issues, evidence_entries = exact_manifest_issues("validation/evidence-staged-manifest.json", X1, EVIDENCE)
    closeout_issues, closeout_entries = exact_manifest_issues("validation/closeout-staged-manifest.json", EVIDENCE, CLOSEOUT)
    correction_issues, correction_entries = exact_manifest_issues("validation/correction-staged-manifest.json", CLOSEOUT, "HEAD")
    owner_issues, owner_entries = exact_manifest_issues("validation/final-owner-manifest.json", SOURCE, "HEAD")
    delta_issues, delta_entries = exact_manifest_issues("validation/final-delta-manifest.json", EVIDENCE, "HEAD")
    check("x1_manifest_parity", not x1_issues, x1_entries)
    check("evidence_manifest_parity", not evidence_issues, evidence_entries)
    check("closeout_manifest_parity", not closeout_issues, closeout_entries)
    check("correction_manifest_parity", not correction_issues, correction_entries)
    check("owner_manifest_parity", not owner_issues, owner_entries)
    check("delta_manifest_parity", not delta_issues, delta_entries)

    privacy_receipts = [load("validation/x1-staged-privacy.json"), load("validation/evidence-staged-privacy.json"), load("validation/closeout-staged-privacy.json"), load("validation/correction-staged-privacy.json"), load("validation/final-owner-privacy.json"), load("validation/final-delta-privacy.json")]
    privacy_scanned = sum(row.get("scanned_file_count", row.get("scanned_path_count", 0)) for row in privacy_receipts)
    privacy_hits = sum(row["confirmed_hit_count"] for row in privacy_receipts)
    check("five_class_privacy_zero_confirmed", privacy_hits == 0 and all(len(row.get("pattern_classes", row.get("scan_classes", []))) == 5 for row in privacy_receipts), privacy_hits)

    truth = load("final/phase-truth.json")
    check("truth_counts", truth["effective_negatives"] == 6563 and truth["effective_open_gaps"] == 51 and truth["effective_exact_gates"] == 52, [truth["effective_negatives"], truth["effective_open_gaps"], truth["effective_exact_gates"]])
    check("truth_distribution", truth["outcome_counts"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
    check("terminal_verdict", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20")
    check("route_held", load("route/final-phase-state.json")["terminal_route"] == "PREPARED_NOT_SENT")
    check("full_suite_not_run", truth["full_repository_suite_run"] is False)
    check("no_replay_planned", truth["post_success_replay_planned"] is False)
    check("same_owner_only", truth["same_owner_only"] is True and truth["independent_reproduction_claimed"] is False)

    document_issues = []
    max_ordinary_words = 0
    baton_words = 0
    for path in sorted(list(ROOT.rglob("*.md")) + list(ROOT.rglob("*.html"))):
        text = path.read_text(encoding="utf-8")
        if path.suffix == ".html":
            text = re.sub(r"<[^>]+>", " ", text)
        words = len(re.findall(r"\b\w+\b", text, flags=re.UNICODE))
        if path.name == "orin-thale-v651-v2-activation.md":
            baton_words = words
        else:
            max_ordinary_words = max(max_ordinary_words, words)
            if words > 6000:
                document_issues.append(path.relative_to(REPO).as_posix())
    check("ordinary_document_cap", not document_issues, max_ordinary_words)
    check("baton_word_range", 8000 <= baton_words <= 20000, baton_words)
    owner_paths = set(filter(None, git("diff", "--name-only", f"{SOURCE}..HEAD").splitlines()))
    check("owner_growth_below_15000", len(owner_paths) < 15000, len(owner_paths))

    diff_hygiene = subprocess.run(["git", "diff", "--check", f"{SOURCE}..HEAD"], cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    check("diff_hygiene", diff_hygiene.returncode == 0, diff_hygiene.stdout.strip())
    final_text = "\n".join((ROOT / relative).read_text(encoding="utf-8") for relative in ["deliverables/final-integrated-overview.md", "final/phase-truth.json", "final/closeout-receipt.json"])
    stale = [label for label in ["frozen_unexecuted", "expected_open_gap", "expected_exact_gate"] if label in final_text]
    check("final_stale_label_review", not stale, stale)

    local = head
    upstream = git("rev-parse", "@{upstream}")
    tracking = git("rev-parse", f"refs/remotes/origin/{branch}")
    live_line = git("ls-remote", "origin", f"refs/heads/{branch}")
    live = live_line.split()[0] if live_line else ""
    check("four_way_remote_equality", local == upstream == tracking == live, {"local": local, "upstream": upstream, "tracking": tracking, "live": live})
    divergence = git("rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()
    check("zero_divergence", divergence == ["0", "0"], divergence)
    clean_after = not git("status", "--porcelain=v1", "--untracked-files=all")
    check("clean_after", clean_after, clean_after)

    payload = {
        "schema": "ghc.family.v651-v1.exact-final-validation.external.v1",
        "exact_head": head,
        "branch": branch,
        "check_count": len(checks),
        "passed_count": sum(bool(row["passed"]) for row in checks),
        "checks": checks,
        "valid": all(bool(row["passed"]) for row in checks),
        "scoped_tests_run": test_count,
        "test_output_tail": test_tails,
        "detailed_checks": {"passed": detailed.get("passed", 0), "total": detailed.get("total", 0)},
        "minimal_checks": {"passed": minimal.get("passed", 0), "total": minimal.get("total", 0)},
        "json_parse_count": len(json_files),
        "json_issues": json_issues,
        "manifest_entries": {"x1": x1_entries, "evidence": evidence_entries, "closeout": closeout_entries, "correction": correction_entries, "owner": owner_entries, "delta": delta_entries},
        "manifest_issues": {"x1": x1_issues, "evidence": evidence_issues, "closeout": closeout_issues, "correction": correction_issues, "owner": owner_issues, "delta": delta_issues},
        "privacy_scanned_receipt_total": privacy_scanned,
        "privacy_confirmed_hits": privacy_hits,
        "owner_changed_paths": len(owner_paths),
        "baton_words": baton_words,
        "max_ordinary_document_words": max_ordinary_words,
        "full_repository_suite_run": False,
        "post_success_replay": False,
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": "One canonical exact-final non-Eiren scoped pass; not a replay, full-suite result, independent reproduction, external audit, production assurance, complete privacy or accessibility, professional or aviation validation, legal or cultural ratification, Maori-authority review, empirical GMUT confirmation, or Stage 20 authority.",
    }
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"checks": len(checks), "passed": payload["passed_count"], "tests": test_count, "detailed": detailed.get("passed", 0), "minimal": minimal.get("passed", 0), "json": len(json_files), "manifests": payload["manifest_entries"], "privacy_hits": privacy_hits, "baton_words": baton_words, "valid": payload["valid"]}, ensure_ascii=False, sort_keys=True))
    return 0 if payload["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
