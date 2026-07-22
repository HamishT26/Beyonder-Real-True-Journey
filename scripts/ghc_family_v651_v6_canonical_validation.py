#!/usr/bin/env python3
"""Run the one credited scoped canonical validation for Elaren v651-v6."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import io
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
PHASE_ROOT = "docs/elaren-kestrel/v651-v6"
SOURCE = "7c4309d6b57bc4827ebd49bcb7c9dfc669c46e3d"
X1 = "b0ba19472777bc07f91c0358186b48311aa3bce3"
EVIDENCE = "94b9afc4f8289e8fdf1a304c90c0765e3beb055f"
BRANCH = "codex/GHC-Family/elaren-kestrel-v649-v8-full-tools"
TEST_FILES = [
    "tests/test_ghc_family_v651_v6_x1.py",
    "tests/test_ghc_family_v651_v6_x2.py",
    "tests/test_ghc_family_v651_v6_closeout.py",
]
PATTERNS = {
    "raw_identifier": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
    "private_path": re.compile(rb"(?:[A-Z]:\\(?:Users|GHC-Archives)\\|/Users/|/home/)", re.I),
    "private_uri": re.compile(rb"(?:codex|chatgpt|file|vscode|app|thread)://", re.I),
    "delegation_markup": re.compile(rb"<\s*(?:codex_delegation|source_thread_id|private_route)\b", re.I),
    "credential_assignment": re.compile(rb"(?:api[_-]?key|password|private[_-]?key|access[_-]?token|secret)\s*[:=]\s*['\"]?[A-Za-z0-9_\-/+=]{12,}", re.I),
}


def git(*args: str, binary: bool = False) -> str | bytes:
    proc = subprocess.run(["git", *args], cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode:
        raise RuntimeError(proc.stderr.decode("utf-8", errors="replace"))
    return proc.stdout if binary else proc.stdout.decode("utf-8").strip()


def load_at(commit: str, path: str) -> dict:
    return json.loads(str(git("show", f"{commit}:{path}")))


def tree_map(commit: str, prefix: str) -> dict[str, str]:
    raw = bytes(git("ls-tree", "-r", "-z", commit, "--", prefix, binary=True))
    result: dict[str, str] = {}
    for record in raw.split(b"\0"):
        if record:
            meta, path = record.split(b"\t", 1)
            _mode, kind, oid = meta.decode("ascii").split()
            if kind == "blob":
                result[path.decode("utf-8")] = oid
    return result


def batch_blobs(oids: list[str]) -> dict[str, bytes]:
    unique = list(dict.fromkeys(oids))
    proc = subprocess.run(
        ["git", "cat-file", "--batch"], cwd=REPO,
        input="".join(oid + "\n" for oid in unique).encode("ascii"),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
    )
    stream = io.BytesIO(proc.stdout)
    result: dict[str, bytes] = {}
    for expected in unique:
        header = stream.readline().rstrip(b"\n").decode("ascii").split()
        if len(header) != 3 or header[0] != expected or header[1] != "blob":
            raise RuntimeError(f"unexpected cat-file header: {header}")
        size = int(header[2])
        result[expected] = stream.read(size)
        if stream.read(1) != b"\n":
            raise RuntimeError("missing cat-file batch terminator")
    return result


def manifest_check(commit: str, manifest_path: str, expected_paths: set[str]) -> dict:
    manifest = load_at(commit, manifest_path)
    entries = manifest["entries"]
    declared = {row["path"] for row in entries} | set(manifest["self_exclusions"])
    blobs = batch_blobs([row["git_blob"] for row in entries])
    issues = []
    if declared != expected_paths:
        issues.append({"issue": "path_set", "missing": sorted(expected_paths - declared), "extra": sorted(declared - expected_paths)})
    for row in entries:
        oid = str(git("rev-parse", f"{commit}:{row['path']}"))
        data = blobs[row["git_blob"]]
        if oid != row["git_blob"]:
            issues.append({"issue": "blob", "path": row["path"]})
        if len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
            issues.append({"issue": "content", "path": row["path"]})
    return {"path": manifest_path, "entries": len(entries), "self_exclusions": len(manifest["self_exclusions"]), "issues": issues, "valid": not issues}


def run_tests() -> dict:
    if str(REPO) not in sys.path:
        sys.path.insert(0, str(REPO))
    suite = unittest.TestSuite()
    loader = unittest.defaultTestLoader
    for index, relative in enumerate(TEST_FILES):
        path = REPO / relative
        spec = importlib.util.spec_from_file_location(f"elaren_v651_v6_selected_{index}", path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"cannot load {relative}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        suite.addTests(loader.loadTestsFromModule(module))
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=1).run(suite)
    return {
        "selected_modules": TEST_FILES,
        "tests_run": result.testsRun,
        "passed": result.testsRun - len(result.failures) - len(result.errors),
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "failure_ids": [test.id() for test, _trace in result.failures],
        "error_ids": [test.id() for test, _trace in result.errors],
        "full_repository_suite_run": False,
        "valid": result.wasSuccessful(),
    }


def import_module(relative: str, name: str):
    spec = importlib.util.spec_from_file_location(name, REPO / relative)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {relative}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = Path(args.output).resolve()
    if output.exists():
        raise SystemExit("refusing to overwrite an existing canonical validation attempt")
    try:
        output.relative_to(REPO.resolve())
        raise SystemExit("canonical validation output must remain outside the repository")
    except ValueError:
        pass
    output.parent.mkdir(parents=True, exist_ok=True)

    head = str(git("rev-parse", "HEAD"))
    branch = str(git("branch", "--show-current"))
    clean_before = not bool(str(git("status", "--porcelain=v1", "--untracked-files=all")))
    upstream = str(git("rev-parse", "@{upstream}"))
    tracking = str(git("rev-parse", f"refs/remotes/origin/{BRANCH}"))
    live_line = str(git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}"))
    live = live_line.split()[0] if live_line else ""

    tests = run_tests()
    detailed_module = import_module("scripts/ghc_family_v651_v6_validator.py", "elaren_v651_v6_detailed")
    detailed_base = detailed_module.validate()
    minimal_module = import_module("scripts/ghc_family_v651_v6_minimal.py", "elaren_v651_v6_minimal")
    minimal_base = minimal_module.verify()

    x1_paths = set(filter(None, str(git("diff", "--name-only", f"{SOURCE}..{X1}")).splitlines()))
    evidence_paths = set(filter(None, str(git("diff", "--name-only", f"{X1}..{EVIDENCE}")).splitlines()))
    final_paths = set(filter(None, str(git("diff", "--name-only", f"{EVIDENCE}..{head}")).splitlines()))
    owner_map = tree_map(head, PHASE_ROOT)
    manifests = [
        manifest_check(X1, f"{PHASE_ROOT}/validation/x1-staged-manifest.json", x1_paths),
        manifest_check(EVIDENCE, f"{PHASE_ROOT}/validation/evidence-staged-manifest.json", evidence_paths),
        manifest_check(head, f"{PHASE_ROOT}/validation/final-delta-manifest.json", final_paths),
        manifest_check(head, f"{PHASE_ROOT}/validation/final-owner-manifest.json", set(owner_map)),
    ]

    owner_blobs = batch_blobs(list(owner_map.values()))
    json_count = 0
    json_issues = []
    privacy_hits = []
    document_issues = []
    for path, oid in owner_map.items():
        data = owner_blobs[oid]
        if path.endswith(".json"):
            try:
                json.loads(data.decode("utf-8"))
                json_count += 1
            except Exception as exc:
                json_issues.append({"path": path, "error": type(exc).__name__})
        for name, pattern in PATTERNS.items():
            for match in pattern.finditer(data):
                privacy_hits.append({"path": path, "class": name, "offset": match.start()})
        if path.endswith((".md", ".html", ".txt")):
            count = len(re.findall(r"\b[\w'-]+\b", data.decode("utf-8", errors="replace")))
            if count > 100000:
                document_issues.append({"path": path, "words": count})

    truth = load_at(head, f"{PHASE_ROOT}/final/phase-truth.json")
    negatives = load_at(head, f"{PHASE_ROOT}/final/retained-negative-register.json")
    gates = load_at(head, f"{PHASE_ROOT}/final/gate-register.json")
    route = load_at(head, f"{PHASE_ROOT}/orchestration/final-route-state.json")
    plan = load_at(head, f"{PHASE_ROOT}/validation/final-validation-plan.json")
    review = load_at(head, f"{PHASE_ROOT}/validation/final-staged-review.json")
    closeout_methods = load_at(head, f"{PHASE_ROOT}/method-flow/closeout-method-flow-ledger.json")
    caps = load_at(head, f"{PHASE_ROOT}/validation/final-document-cap-receipt.json")
    threshold = load_at(head, f"{PHASE_ROOT}/validation/final-owner-file-threshold.json")
    baton = str(git("show", f"{head}:{PHASE_ROOT}/handoffs/vesper-arlen-v651-v7-activation.md"))
    overview = str(git("show", f"{head}:{PHASE_ROOT}/overview/final-integrated-overview.md"))
    baton_words = len(re.findall(r"\b[\w'-]+\b", baton))
    overview_words = len(re.findall(r"\b[\w'-]+\b", overview))
    phase_commits = int(str(git("rev-list", "--count", f"{SOURCE}..{head}")))
    merges = int(str(git("rev-list", "--count", "--merges", f"{SOURCE}..{head}")))
    parent_row = str(git("rev-list", "--parents", "-n", "1", head)).split()

    def ancestor(anchor: str) -> bool:
        return subprocess.run(["git", "merge-base", "--is-ancestor", anchor, head], cwd=REPO).returncode == 0

    final_checks = {
        "exact_branch": branch == BRANCH,
        "clean_before": clean_before,
        "four_way_equality": head == upstream == tracking == live,
        "source_ancestral": ancestor(SOURCE),
        "x1_ancestral": ancestor(X1),
        "evidence_ancestral": ancestor(EVIDENCE),
        "three_phase_commits": phase_commits == 3,
        "within_six_commit_cap": phase_commits <= 6,
        "zero_merges": merges == 0,
        "one_final_parent": len(parent_row) == 2 and parent_row[1] == EVIDENCE,
        "tests_selected_only": tests["valid"] and tests["tests_run"] == 71 and not tests["full_repository_suite_run"],
        "x1_manifest": manifests[0]["valid"],
        "evidence_manifest": manifests[1]["valid"],
        "final_delta_manifest": manifests[2]["valid"],
        "final_owner_manifest": manifests[3]["valid"],
        "json": not json_issues,
        "privacy": not privacy_hits,
        "documents": not document_issues and 10000 <= baton_words <= 100000 and overview_words >= 3000 and caps["valid"],
        "owner_threshold": threshold["within_threshold"] and len(owner_map) < 2000,
        "outcomes": truth["outcomes"] == {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1},
        "negatives": negatives["effective"] == 7327 and negatives["no_failure_erased"],
        "gaps": gates["effective_open_gaps"] == 57 and gates["silently_closed"] == 0,
        "gates": gates["effective_exact_gates"] == 58 and gates["silently_closed"] == 0,
        "route_prepared": route["state"] == "PREPARED_NOT_SENT" and route["target_exact_title"] == "Vesper Arlen" and route["send_count"] == 0,
        "no_task_or_subagent": not route["task_created"] and not route["task_forked"] and not route["subagent_spawned"] and not route["cli_sibling_created"],
        "single_pass_plan": plan["successful_canonical_pass_limit"] == 1 and not plan["post_success_replay"] and not plan["full_repository_suite"],
        "staged_review": review["valid"] and not review["unexpected_paths"] and not review["frozen_evidence_changes"],
        "closeout_method_flow": closeout_methods["aggregate_with_evidence"] == {"methods": 8, "preferred": 8, "fail": 8, "pass": 8} and closeout_methods["valid"],
        "no_real_evidence": all(truth[key] == 0 for key in ("real_data_rows", "participants", "real_keys_or_proofs", "authority_decisions", "production_actions")),
        "same_owner_boundary": truth["same_owner_only"] and not truth["independent_reproduction"],
        "no_full_suite": not truth["full_repository_suite_run"],
        "no_post_success_replay": not truth["post_success_replay_run"],
        "no_cli_sibling": truth["cli_siblings_created"] == 0,
        "stage20": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
    }
    minimal_final_names = [
        "clean_before", "four_way_equality", "source_ancestral", "x1_ancestral", "evidence_ancestral",
        "three_phase_commits", "zero_merges", "one_final_parent", "tests_selected_only", "final_delta_manifest",
        "final_owner_manifest", "privacy", "route_prepared", "stage20",
    ]
    clean_after = not bool(str(git("status", "--porcelain=v1", "--untracked-files=all")))
    final_checks["clean_after"] = clean_after
    detailed_passed = detailed_base["check_count"] - len(detailed_base["issues"]) + sum(final_checks.values())
    detailed_total = detailed_base["check_count"] + len(final_checks)
    minimal_passed = minimal_base["passed"] + sum(final_checks[name] for name in minimal_final_names)
    minimal_total = minimal_base["check_count"] + len(minimal_final_names)
    issues = list(detailed_base["issues"]) + [name for name, value in final_checks.items() if not value]
    valid = not issues and tests["valid"] and minimal_base["valid"] and all(row["valid"] for row in manifests)
    receipt = {
        "schema": "ghc.family.v651-v6.exact-final-validation.v1",
        "owner": "Elaren Kestrel",
        "phase": "v651-v6",
        "exact_head": head,
        "branch": branch,
        "tests": tests,
        "detailed": {"passed": detailed_passed, "total": detailed_total, "base": detailed_base, "final_checks": final_checks},
        "minimal": {"passed": minimal_passed, "total": minimal_total, "base": minimal_base, "final_check_names": minimal_final_names},
        "json": {"parsed": json_count, "issues": json_issues},
        "privacy": {"files_scanned": len(owner_map), "pattern_classes": sorted(PATTERNS), "confirmed_hits": privacy_hits, "zero_confirmed_hits": not privacy_hits},
        "manifests": manifests,
        "documents": {"baton_words": baton_words, "overview_words": overview_words, "issues": document_issues},
        "history": {"source": SOURCE, "x1": X1, "evidence": EVIDENCE, "final": head, "phase_commits": phase_commits, "commit_cap": 6, "merges": merges, "final_parent_count": len(parent_row) - 1},
        "equality": {"local": head, "upstream": upstream, "tracking": tracking, "live": live, "all_equal": head == upstream == tracking == live},
        "clean_before": clean_before,
        "clean_after": clean_after,
        "full_repository_suite_run": False,
        "canonical_successful_passes": 1 if valid else 0,
        "post_success_replay_run": False,
        "same_owner_only": True,
        "independent_reproduction": False,
        "issues": issues,
        "valid": valid,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": "One non-Eiren scoped canonical aggregate at the exact pushed final head; no complete repository suite and no replay after success.",
    }
    output.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({
        "head": head,
        "tests": f"{tests['passed']}/{tests['tests_run']}",
        "detailed": f"{detailed_passed}/{detailed_total}",
        "minimal": f"{minimal_passed}/{minimal_total}",
        "json": json_count,
        "privacy_files": len(owner_map),
        "manifest_entries": sum(row["entries"] for row in manifests),
        "clean_before": clean_before,
        "clean_after": clean_after,
        "four_way_equal": head == upstream == tracking == live,
        "valid": valid,
    }, sort_keys=True))
    raise SystemExit(0 if valid else 1)


if __name__ == "__main__":
    main()
