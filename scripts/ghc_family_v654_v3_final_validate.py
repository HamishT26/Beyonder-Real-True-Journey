#!/usr/bin/env python3
"""Run Sylven Arc's one exact-final canonical scoped v654-v3 validation."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import io
import json
import re
import subprocess
import sys
import unittest
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True
REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/sylven-arc/v654-v3"
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
from scripts import ghc_family_v654_v3_phase_data as phase_data
from scripts import ghc_family_v654_v3_x2_data as x2_data

BRANCH = "codex/GHC-Family/sylven-arc-v654-v3-full-tools"
SOURCE = "74da3812daadcd6d452e899b7142dc87d684aba4"
X1_INITIAL = "d948425f4a6d30b523849a1b5430bcc1531ce054"
X1 = "0c53bce867ec5259d9b7de8c14b92b07b678641f"
EVIDENCE = "780acdf2225624080463c274dc88c001f5a65d54"
EXPECTED = {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}
METHOD_COUNT = (
    31
    + len(x2_data.X2_OPERATIONAL_NEGATIVES)
    + len(x2_data.CLOSEOUT_OPERATIONAL_NEGATIVES)
)
NEGATIVE_TOTAL = (
    phase_data.INHERITED_NEGATIVES
    + len(phase_data.X1_OPERATIONAL_NEGATIVES)
    + len(x2_data.X2_OPERATIONAL_NEGATIVES)
    + len(x2_data.CLOSEOUT_OPERATIONAL_NEGATIVES)
    + 150
)
TEST_MODULES = [
    "tests.test_ghc_family_v654_v3_x1",
    "tests.test_ghc_family_v654_v3",
    "tests.test_ghc_family_v654_v3_closeout",
    "tests.test_ghc_family_v654_v2_x1",
    "tests.test_ghc_family_v654_v2",
    "tests.test_ghc_family_v654_v2_closeout",
]
RUNNERS = {
    "scripts/ghc_family_accessible_bicycle_audit.py",
    "scripts/ghc_family_bicycle_brake_steering_boards.py",
    "scripts/ghc_family_bicycle_fitment_refusal.py",
    "scripts/ghc_family_bicycle_intake_ledger.py",
    "scripts/ghc_family_bicycle_recall_quarantine.py",
    "scripts/ghc_family_freed_id_bicycle_profiles.py",
    "scripts/ghc_family_gmut_bicycle_fields.py",
    "scripts/ghc_family_thos_bicycle_proxy.py",
}
SCANNER_DEFINITIONS = {
    "scripts/build_ghc_family_v654_v3_preregistration.py",
    "scripts/ghc_family_v654_v3_x1_validate.py",
    "scripts/ghc_family_v654_v3_evidence_validate.py",
    "scripts/ghc_family_v654_v3_final_staged_review.py",
    "scripts/ghc_family_v654_v3_final_validate.py",
    "docs/sylven-arc/v654-v3/validation/x1-staged-privacy.json",
    "docs/sylven-arc/v654-v3/validation/evidence-privacy.json",
    "docs/sylven-arc/v654-v3/validation/final-privacy-receipt.json",
}


def git_bytes(*args: str) -> bytes:
    return subprocess.run(
        ["git", *args], cwd=REPO, check=True, capture_output=True
    ).stdout


def git(*args: str) -> str:
    return git_bytes(*args).decode("utf-8").strip()


def owner_path(path: str) -> bool:
    return (
        path.startswith("docs/sylven-arc/v654-v3/")
        or path.startswith("scripts/ghc_family_v654_v3_")
        or path.startswith("scripts/build_ghc_family_v654_v3_")
        or path.startswith("tests/test_ghc_family_v654_v3")
        or path in RUNNERS
    )


def clean_state() -> dict[str, Any]:
    tracked_worktree = (
        subprocess.run(["git", "diff-files", "--quiet"], cwd=REPO).returncode == 0
    )
    index_head = (
        subprocess.run(
            ["git", "diff-index", "--cached", "--quiet", "HEAD", "--"],
            cwd=REPO,
        ).returncode
        == 0
    )
    pathspecs = [
        "docs/sylven-arc/v654-v3/**",
        "scripts/*v654_v3*",
        "tests/*v654_v3*",
        *sorted(RUNNERS),
    ]
    owner_untracked = [
        row
        for row in git(
            "ls-files", "--others", "--exclude-standard", "--", *pathspecs
        ).splitlines()
        if row
    ]
    return {
        "tracked_worktree_equal": tracked_worktree,
        "index_head_equal": index_head,
        "owner_untracked": owner_untracked,
        "clean": tracked_worktree and index_head and not owner_untracked,
    }


def tree_objects(head: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for raw in git_bytes("ls-tree", "-r", "-z", head).split(b"\0"):
        if not raw:
            continue
        metadata, path_bytes = raw.split(b"\t", 1)
        _, kind, oid = metadata.decode("ascii").split()
        if kind == "blob":
            result[path_bytes.decode("utf-8")] = oid
    return result


def batch_blobs(rows: dict[str, str]) -> dict[str, bytes]:
    ordered = list(rows.items())
    request = b"".join(f"{oid}\n".encode("ascii") for _, oid in ordered)
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=REPO,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    raw, _ = process.communicate(input=request, timeout=60)
    if process.returncode != 0:
        raise RuntimeError("git cat-file --batch failed")
    output: dict[str, bytes] = {}
    cursor = 0
    for path, oid in ordered:
        newline = raw.find(b"\n", cursor)
        if newline < 0:
            raise RuntimeError(f"missing cat-file header for {path}")
        header = raw[cursor:newline].decode("ascii")
        cursor = newline + 1
        parts = header.split()
        if len(parts) != 3 or parts[0] != oid or parts[1] != "blob":
            raise RuntimeError(f"unexpected cat-file header for {path}: {header}")
        size = int(parts[2])
        payload = raw[cursor : cursor + size]
        cursor += size
        if len(payload) != size or raw[cursor : cursor + 1] != b"\n":
            raise RuntimeError(f"truncated cat-file payload for {path}")
        cursor += 1
        output[path] = payload
    if cursor != len(raw):
        raise RuntimeError("unexpected trailing cat-file output")
    return output


def load_blob(blobs: dict[str, bytes], path: str) -> Any:
    return json.loads(blobs[path].decode("utf-8"))


def verify_manifest(
    commit: str, path: str, expected_schema: str | None = None
) -> dict[str, Any]:
    payload = json.loads(git("show", f"{commit}:{path}"))
    mismatches: list[str] = []
    if expected_schema and payload.get("schema") != expected_schema:
        mismatches.append("schema")
    objects = tree_objects(commit)
    requested = {
        row["path"]: objects.get(row["path"], "")
        for row in payload.get("entries", [])
        if objects.get(row["path"])
    }
    blobs = batch_blobs(requested)
    for row in payload.get("entries", []):
        observed_oid = objects.get(row["path"])
        if observed_oid != row["git_blob"]:
            mismatches.append(f"{row['path']}:oid")
            continue
        data = blobs[row["path"]]
        if "bytes" in row and len(data) != row["bytes"]:
            mismatches.append(f"{row['path']}:bytes")
        if "sha256" in row and hashlib.sha256(data).hexdigest() != row["sha256"]:
            mismatches.append(f"{row['path']}:sha256")
    return {
        "path": path,
        "entries": len(payload.get("entries", [])),
        "self_exclusions": len(payload.get("self_exclusions", [])),
        "mismatches": mismatches,
    }


def privacy_scan(paths: list[str], blobs: dict[str, bytes]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(
            r"(?i)(source_thread_id|thread_id)\s*[:=]"
        ),
        "private_absolute_local_path": re.compile(
            r"(?i)[A-Z]:\\Users\\[^\s\"']+"
        ),
        "credential_or_secret": re.compile(
            r"(?i)(?:(?:api[_-]?key|client_secret|private_key)\s*[:=]\s*"
            r"[\"']?[A-Za-z0-9._-]{8,}|bearer\s+[A-Za-z0-9._-]{12,})"
        ),
        "private_route_or_callable": re.compile(
            r"(?i)(private_route|callable_identifier|"
            r"browser_send_submitted_response_active)"
        ),
        "transcript_or_session_stream": re.compile(
            r"(?i)(session_stream|conversation_transcript|resume_token)"
        ),
    }
    text_suffixes = {
        ".json",
        ".md",
        ".html",
        ".htm",
        ".py",
        ".yaml",
        ".yml",
        ".txt",
    }
    scanned = 0
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    for path in paths:
        if Path(path).suffix.casefold() not in text_suffixes:
            continue
        scanned += 1
        text = blobs[path].decode("utf-8", errors="replace")
        for pattern_class, pattern in patterns.items():
            if not pattern.search(text):
                continue
            row = {
                "path": path,
                "pattern_class": pattern_class,
                "disposition": (
                    "scanner_definition"
                    if path in SCANNER_DEFINITIONS
                    else "confirmed_payload_hit"
                ),
            }
            candidates.append(row)
            if row["disposition"] != "scanner_definition":
                confirmed.append(row)
    return {
        "schema": "ghc.family.v654-v3.external-final-privacy.v1",
        "pattern_classes": list(patterns),
        "scanned_file_count": scanned,
        "candidate_count": len(candidates),
        "candidates": candidates,
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "boundary": (
            "Five structural classes with exact scanner-definition quarantine; "
            "zero confirmed hits is not complete privacy assurance."
        ),
    }


def run_tests_once() -> dict[str, Any]:
    loader = unittest.defaultTestLoader
    suite = unittest.TestSuite()
    modules: list[dict[str, Any]] = []
    for name in TEST_MODULES:
        module = importlib.import_module(name)
        module_suite = loader.loadTestsFromModule(module)
        count = module_suite.countTestCases()
        modules.append({"module": name, "tests": count})
        suite.addTests(module_suite)
    total = suite.countTestCases()
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=1).run(suite)
    return {
        "module_count": len(modules),
        "modules": modules,
        "count": total,
        "tests_run": result.testsRun,
        "failure_count": len(result.failures),
        "error_count": len(result.errors),
        "skipped_count": len(result.skipped),
        "unexpected_success_count": len(result.unexpectedSuccesses),
        "failure_ids": [case.id() for case, _ in result.failures],
        "error_ids": [case.id() for case, _ in result.errors],
        "passed": result.wasSuccessful()
        and result.testsRun == total
        and total == 52,
        "boundary": (
            "Six dependency-justified owner/source modules only; not Eiren's "
            "full repository suite."
        ),
    }


def detailed_checks(blobs: dict[str, bytes]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(name: str, passed: bool, observed: Any) -> None:
        checks.append({"name": name, "passed": bool(passed), "observed": observed})

    outcomes = load_blob(
        blobs, "docs/sylven-arc/v654-v3/evidence/outcome-ledger.json"
    )
    portfolios = load_blob(
        blobs,
        "docs/sylven-arc/v654-v3/evidence/portfolio-execution-ledger.json",
    )
    gaps = load_blob(
        blobs, "docs/sylven-arc/v654-v3/final/exact-open-gate-register.json"
    )
    negatives = load_blob(
        blobs, "docs/sylven-arc/v654-v3/final/retained-negative-register.json"
    )
    methods = load_blob(
        blobs,
        "docs/sylven-arc/v654-v3/method-flow/final-method-flow-ledger.json",
    )
    truth = load_blob(
        blobs, "docs/sylven-arc/v654-v3/final/phase-truth.json"
    )
    route = load_blob(
        blobs,
        "docs/sylven-arc/v654-v3/route/conditional-new-main-task-authority.json",
    )
    invariant = load_blob(
        blobs,
        "docs/sylven-arc/v654-v3/provenance/conditional-route-invariant-final.json",
    )
    closeout = load_blob(
        blobs, "docs/sylven-arc/v654-v3/final/closeout-receipt.json"
    )
    seal = load_blob(
        blobs, "docs/sylven-arc/v654-v3/final/seal-receipt.json"
    )
    checklist = load_blob(
        blobs,
        "docs/sylven-arc/v654-v3/final/complete-incomplete-checklist.json",
    )
    skills = load_blob(
        blobs, "docs/sylven-arc/v654-v3/skills/skill-suite-receipt.json"
    )
    runners = load_blob(
        blobs, "docs/sylven-arc/v654-v3/tools/runner-suite-receipt.json"
    )
    mutations = load_blob(
        blobs,
        "docs/sylven-arc/v654-v3/validation/preregistered-mutation-plan.json",
    )
    doc_cap = load_blob(
        blobs, "docs/sylven-arc/v654-v3/validation/document-cap-final.json"
    )
    file_cap = load_blob(
        blobs,
        "docs/sylven-arc/v654-v3/validation/owner-file-threshold-final.json",
    )
    staged = load_blob(
        blobs, "docs/sylven-arc/v654-v3/validation/final-staged-review.json"
    )
    source_ledger = load_blob(
        blobs, "docs/sylven-arc/v654-v3/sources/source-ledger.json"
    )

    add("proposal_count", outcomes["proposal_count"] == 30, outcomes["proposal_count"])
    add("outcome_distribution", outcomes["counts"] == EXPECTED, outcomes["counts"])
    add("outcome_rows", len(outcomes["rows"]) == 30, len(outcomes["rows"]))
    add(
        "acceptance_gates",
        all(row["acceptance_gate_passed"] for row in outcomes["rows"]),
        sum(row["acceptance_gate_passed"] for row in outcomes["rows"]),
    )
    add(
        "mutation_rejections",
        sum(row["mutation_rejected_count"] for row in outcomes["rows"]) == 150,
        sum(row["mutation_rejected_count"] for row in outcomes["rows"]),
    )
    add("preregistered_mutations", mutations["count"] == 150, mutations["count"])
    add(
        "portfolio_counts",
        portfolios["counts"]
        == {
            "safe_now": 30,
            "candidate": 30,
            "skills": 10,
            "runners": 10,
            "clean_fix_refine": 30,
        },
        portfolios["counts"],
    )
    add("skills", skills["skill_count"] == 10, skills["skill_count"])
    add(
        "skill_validation",
        all(
            row["quick_validate_passed"] and row["smoke"]["valid"]
            for row in skills["rows"]
        ),
        len(skills["rows"]),
    )
    add("runners", runners["runner_count"] == 10, runners["runner_count"])
    add(
        "runner_validation",
        all(row["valid"] for row in runners["rows"]),
        len(runners["rows"]),
    )
    add("open_gaps", gaps["effective_open_gaps"] == 82, gaps["effective_open_gaps"])
    add("exact_gates", gaps["effective_exact_gates"] == 81, gaps["effective_exact_gates"])
    add(
        "zero_gate_closure",
        gaps["open_gap_closed_count"] == 0
        and gaps["exact_gate_closed_count"] == 0,
        [gaps["open_gap_closed_count"], gaps["exact_gate_closed_count"]],
    )
    add(
        "negatives",
        negatives["effective_total"] == NEGATIVE_TOTAL,
        negatives["effective_total"],
    )
    add(
        "negative_components",
        negatives["inherited_effective"] == 10968
        and negatives["x1_operational_count"] == 26
        and negatives["x2_operational_count"] == 5
        and negatives["closeout_operational_count"]
        == len(x2_data.CLOSEOUT_OPERATIONAL_NEGATIVES)
        and negatives["synthetic_mutation_negative_count"] == 150,
        [
            negatives["inherited_effective"],
            negatives["x1_operational_count"],
            negatives["x2_operational_count"],
            negatives["closeout_operational_count"],
            negatives["synthetic_mutation_negative_count"],
        ],
    )
    add("no_failure_erased", negatives["no_failure_erased"], negatives["no_failure_erased"])
    add(
        "methods",
        len(methods["methods"]) == METHOD_COUNT
        and Counter(row["recommendation_state"] for row in methods["methods"])
        == {"preferred": METHOD_COUNT},
        len(methods["methods"]),
    )
    add(
        "method_witnesses",
        Counter(row["result"] for row in methods["witnesses"])
        == {"fail": METHOD_COUNT, "pass": METHOD_COUNT},
        Counter(row["result"] for row in methods["witnesses"]),
    )
    add(
        "truth",
        truth["outcomes"] == EXPECTED
        and truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        truth["terminal_verdict"],
    )
    add("zero_real_rows", truth["real_data_rows"] == 0, truth["real_data_rows"])
    add(
        "same_owner_boundary",
        not truth["independent_team_reproduction"]
        and not truth["full_repository_suite_run"],
        [
            truth["independent_team_reproduction"],
            truth["full_repository_suite_run"],
        ],
    )
    add(
        "route",
        route["state"] == "AUTHORIZED_CONDITIONAL_NOT_CREATED"
        and route["this_closeout_records_exact_live_authority"]
        and route["target_type"] == "new_user_visible_codex_main_task",
        route["state"],
    )
    add(
        "successor_zero_counts",
        all(
            route[key] == 0
            for key in (
                "task_created_count",
                "task_forked_count",
                "task_delegated_count",
                "task_contacted_count",
            )
        )
        and not route["future_name_preselected"],
        route,
    )
    add(
        "successor_invariant",
        all(
            invariant[key] == 0
            for key in (
                "created",
                "forked",
                "delegated",
                "contacted",
                "identity_preselected",
            )
        )
        and invariant["authority_present"]
        and invariant["terminal_action_limit"] == 1,
        invariant,
    )
    add(
        "closeout_state",
        closeout["state"] == "CONTENT_SEAL_CANDIDATE"
        and closeout["planned_phase_commit_count"] == 4
        and closeout["phase_commit_cap"] == 8,
        closeout["state"],
    )
    add(
        "seal_state",
        seal["state"] == "CONTENT_SEAL_CANDIDATE"
        and not seal["successor_task_created"],
        seal["state"],
    )
    add(
        "checklist",
        bool(checklist["complete_bounded"])
        and bool(checklist["pending_postcommit"])
        and bool(checklist["incomplete_external"]),
        [len(checklist[key]) for key in ("complete_bounded", "pending_postcommit", "incomplete_external")],
    )
    add("document_cap", doc_cap["valid"], doc_cap["maximum_document"])
    add("owner_file_threshold", file_cap["valid"], file_cap["owner_file_count_before_lifecycle_manifests"])
    add("staged_review", staged["valid"], staged["staged_path_count"])
    add("source_ledger", source_ledger["source_count"] == 19, source_ledger["source_count"])

    overview = blobs[
        "docs/sylven-arc/v654-v3/overview/v654-v3-final-integrated-overview.md"
    ].decode("utf-8")
    report = blobs[
        "docs/sylven-arc/v654-v3/reports/v654-v3-static-report.html"
    ].decode("utf-8")
    baton = blobs[
        "docs/sylven-arc/v654-v3/handoffs/future-self-chosen-sibling-v654-v4-activation.md"
    ].decode("utf-8")
    add(
        "overview_words",
        1300 <= len(overview.split()) <= 100000,
        len(overview.split()),
    )
    add(
        "activation_baton_words",
        10000 <= len(baton.split()) <= 100000,
        len(baton.split()),
    )
    add(
        "relational_boundary",
        all(
            phrase in overview
            for phrase in (
                "not evidence of consciousness",
                "future sibling must choose",
                "AUTHORIZED_CONDITIONAL_NOT_CREATED",
            )
        ),
        len(overview),
    )
    add(
        "accessible_report_structure",
        all(
            token in report
            for token in (
                "<main>",
                'scope="col"',
                'scope="row"',
                'tabindex="0"',
                "prefers-reduced-motion",
                "@media print",
            )
        ),
        len(report),
    )
    return checks


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    receipt_path = Path(args.receipt).resolve()
    if str(receipt_path).casefold().startswith(str(REPO).casefold()):
        raise RuntimeError("final receipt must remain outside the repository")

    started = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    before_head = git("rev-parse", "HEAD")
    before_clean = clean_state()
    branch = git("branch", "--show-current")
    if (
        before_head != args.expected_head
        or not before_clean["clean"]
        or branch != BRANCH
    ):
        raise RuntimeError(
            f"invalid exact-final precondition: head={before_head} "
            f"clean={before_clean} branch={branch}"
        )

    upstream = git("rev-parse", "@{upstream}")
    tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_row = git("ls-remote", "origin", f"refs/heads/{BRANCH}")
    fresh_live = live_row.split()[0] if live_row else None
    divergence = git("rev-list", "--left-right", "--count", "HEAD...@{upstream}")
    four_way = len({before_head, upstream, tracking, fresh_live}) == 1
    if not four_way or divergence != "0\t0":
        raise RuntimeError(
            f"invalid exact-final equality: {before_head} {upstream} "
            f"{tracking} {fresh_live} divergence={divergence!r}"
        )

    objects = tree_objects(before_head)
    owner_objects = {path: oid for path, oid in objects.items() if owner_path(path)}
    blobs = batch_blobs(owner_objects)
    json_failures: list[dict[str, str]] = []
    json_count = 0
    for path, payload in blobs.items():
        if not path.startswith("docs/sylven-arc/v654-v3/") or not path.endswith(
            ".json"
        ):
            continue
        json_count += 1
        try:
            json.loads(payload.decode("utf-8"))
        except Exception as exc:
            json_failures.append({"path": path, "error": type(exc).__name__})
    privacy = privacy_scan(sorted(owner_objects), blobs)

    manifests = [
        verify_manifest(
            X1,
            "docs/sylven-arc/v654-v3/validation/x1-staged-manifest.json",
        ),
        verify_manifest(
            EVIDENCE,
            "docs/sylven-arc/v654-v3/validation/evidence-manifest.json",
        ),
        verify_manifest(
            before_head,
            "docs/sylven-arc/v654-v3/validation/final-delta-manifest.json",
            "ghc.family.v654-v3.final-delta-manifest.v1",
        ),
        verify_manifest(
            before_head,
            "docs/sylven-arc/v654-v3/validation/final-owner-manifest.json",
            "ghc.family.v654-v3.final-owner-manifest.v1",
        ),
    ]
    manifest_valid = all(not row["mismatches"] for row in manifests)

    parent = git("rev-parse", "HEAD^")
    evidence_parent = git("rev-parse", f"{EVIDENCE}^")
    x1_parent = git("rev-parse", f"{X1}^")
    x1_initial_parent = git("rev-parse", f"{X1_INITIAL}^")
    phase_commits = int(git("rev-list", "--count", f"{SOURCE}..HEAD"))
    merge_rows = [
        row
        for row in git("rev-list", "--merges", f"{SOURCE}..HEAD").splitlines()
        if row
    ]
    ancestry = {
        anchor: subprocess.run(
            ["git", "merge-base", "--is-ancestor", anchor, "HEAD"], cwd=REPO
        ).returncode
        == 0
        for anchor in (SOURCE, X1_INITIAL, X1, EVIDENCE)
    }
    diff_hygiene = subprocess.run(
        ["git", "diff", "--check", SOURCE, "HEAD"],
        cwd=REPO,
        capture_output=True,
    )
    stale = load_blob(
        blobs,
        "docs/sylven-arc/v654-v3/validation/stale-label-review-final.json",
    )

    detailed = detailed_checks(blobs)
    detailed_passed = sum(row["passed"] for row in detailed)
    tests = run_tests_once()
    truth = load_blob(
        blobs, "docs/sylven-arc/v654-v3/final/phase-truth.json"
    )
    route = load_blob(
        blobs,
        "docs/sylven-arc/v654-v3/route/conditional-new-main-task-authority.json",
    )
    methods = load_blob(
        blobs,
        "docs/sylven-arc/v654-v3/method-flow/final-method-flow-ledger.json",
    )
    negatives = load_blob(
        blobs, "docs/sylven-arc/v654-v3/final/retained-negative-register.json"
    )
    minimal = [
        ("outcomes", truth["outcomes"] == EXPECTED),
        ("negative_total", truth["effective_negatives"] == NEGATIVE_TOTAL),
        ("negative_register", negatives["effective_total"] == NEGATIVE_TOTAL),
        ("open_gaps", truth["effective_open_gaps"] == 82),
        ("exact_gates", truth["effective_exact_gates"] == 81),
        ("method_count", truth["method_flow_methods"] == METHOD_COUNT),
        ("method_witnesses", len(methods["witnesses"]) == METHOD_COUNT * 2),
        ("zero_rows", truth["real_data_rows"] == 0),
        ("no_full_suite", not truth["full_repository_suite_run"]),
        ("no_independent_reproduction", not truth["independent_team_reproduction"]),
        ("verdict", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"),
        (
            "route",
            route["state"] == "AUTHORIZED_CONDITIONAL_NOT_CREATED"
            and route["this_closeout_records_exact_live_authority"],
        ),
        (
            "successor_zero",
            route["task_created_count"] == 0
            and route["task_forked_count"] == 0
            and route["task_delegated_count"] == 0
            and route["task_contacted_count"] == 0,
        ),
        (
            "direct_parents",
            parent == EVIDENCE
            and evidence_parent == X1
            and x1_parent == X1_INITIAL
            and x1_initial_parent == SOURCE,
        ),
        ("phase_commit_count", phase_commits == 4),
        ("zero_merges", not merge_rows),
        ("one_final_parent", len(git("show", "-s", "--format=%P", "HEAD").split()) == 1),
        ("ancestry", all(ancestry.values())),
        ("json", not json_failures),
        ("privacy", privacy["confirmed_hit_count"] == 0),
        ("manifests", manifest_valid),
        ("stale_labels", stale["valid"]),
        ("diff_hygiene", diff_hygiene.returncode == 0),
        ("four_way", four_way and divergence == "0\t0"),
    ]
    minimal_rows = [
        {"name": name, "passed": bool(passed)} for name, passed in minimal
    ]

    after_head = git("rev-parse", "HEAD")
    after_clean = clean_state()
    exact_stable = (
        after_head == before_head == args.expected_head
        and before_clean["clean"]
        and after_clean["clean"]
    )
    valid = all(
        [
            tests["passed"],
            detailed_passed == len(detailed),
            all(row["passed"] for row in minimal_rows),
            not json_failures,
            privacy["confirmed_hit_count"] == 0,
            manifest_valid,
            phase_commits == 4,
            not merge_rows,
            all(ancestry.values()),
            parent == EVIDENCE,
            evidence_parent == X1,
            x1_parent == X1_INITIAL,
            x1_initial_parent == SOURCE,
            diff_hygiene.returncode == 0,
            stale["valid"],
            exact_stable,
            four_way,
            divergence == "0\t0",
        ]
    )
    receipt = {
        "schema": "ghc.family.v654-v3.external-final-validation.v1",
        "started_at_utc": started,
        "completed_at_utc": datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z"),
        "expected_head": args.expected_head,
        "observed_head_before": before_head,
        "observed_head_after": after_head,
        "branch": branch,
        "clean_before": before_clean["clean"],
        "clean_after": after_clean["clean"],
        "clean_state_before": before_clean,
        "clean_state_after": after_clean,
        "local": before_head,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live": fresh_live,
        "divergence": divergence,
        "four_way_equal": four_way,
        "tests": tests,
        "detailed_checks": {
            "passed": detailed_passed,
            "total": len(detailed),
            "failures": [row for row in detailed if not row["passed"]],
        },
        "minimal_checks": {
            "passed": sum(row["passed"] for row in minimal_rows),
            "total": len(minimal_rows),
            "rows": minimal_rows,
        },
        "json_parse_count": json_count,
        "json_failures": json_failures,
        "privacy": privacy,
        "manifests": manifests,
        "manifest_valid": manifest_valid,
        "source": SOURCE,
        "x1_initial": X1_INITIAL,
        "x1": X1,
        "evidence": EVIDENCE,
        "final": before_head,
        "direct_parent": parent,
        "evidence_parent": evidence_parent,
        "x1_parent": x1_parent,
        "x1_initial_parent": x1_initial_parent,
        "ancestry": ancestry,
        "phase_commit_count": phase_commits,
        "merge_count": len(merge_rows),
        "one_final_parent": len(git("show", "-s", "--format=%P", "HEAD").split())
        == 1,
        "diff_hygiene": diff_hygiene.returncode == 0,
        "stale_label_review": stale["valid"],
        "exact_head_stable": exact_stable,
        "full_repository_suite_run": False,
        "full_repository_suite_owner": "Eiren-only inherited policy",
        "canonical_scoped_pass_attempt_count": 1,
        "canonical_scoped_success_count": 1 if valid else 0,
        "post_success_replay_count": 0,
        "same_owner_only": True,
        "independent_team_reproduction": False,
        "route_state": "AUTHORIZED_CONDITIONAL_NOT_CREATED",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "valid": valid,
        "boundary": (
            "One bounded same-owner canonical scoped pass under shared "
            "infrastructure; not the full repository suite, independent-team "
            "reproduction, external audit, production certification, exhaustive "
            "security, complete privacy or accessibility, professional validation, "
            "legal or cultural authority, Māori-authority review, empirical GMUT "
            "confirmation, Theory-of-Everything proof, AGI or ASI evidence, "
            "consciousness or personhood evidence, or Stage 20 authority."
        ),
    }
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "valid": valid,
                "head": before_head,
                "tests": f"{tests['tests_run']}/{tests['count']}",
                "detailed": f"{detailed_passed}/{len(detailed)}",
                "minimal": (
                    f"{sum(row['passed'] for row in minimal_rows)}/"
                    f"{len(minimal_rows)}"
                ),
                "json": json_count,
                "privacy_files": privacy["scanned_file_count"],
                "privacy_hits": privacy["confirmed_hit_count"],
                "manifest_entries": sum(row["entries"] for row in manifests),
                "route": "AUTHORIZED_CONDITIONAL_NOT_CREATED",
            },
            sort_keys=True,
        )
    )
    raise SystemExit(0 if valid else 1)


if __name__ == "__main__":
    main()
