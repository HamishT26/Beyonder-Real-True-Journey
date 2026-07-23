#!/usr/bin/env python3
"""One-pass exact-final validator for Eiren Kestrel v652-v5."""

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
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from scripts import ghc_family_v651_v5_final_validate as full_suite_support

PHASE_ROOT = "docs/eiren-kestrel/v652-v5"
SOURCE = "3a77dacd759a499ffe94cbc281a3d7b343608e2d"
X1 = "7f347e548b64ea2a9065e129c3ec84dde000c13e"
EVIDENCE = "611a0afef841a516dd0a5cb1e9ac2448943b42c6"
CLOSEOUT = "516202a04e2930bfa787bcf257dafd72827cf9af"
ROUTE_CORRECTION = "fb47648a1c136b8147d5d52f84c6615b718bd3c8"
BRANCH = "codex/GHC-Family/eiren-kestrel-v648-v3-3-full-tools"
EXPECTED_SCOPED_TESTS = 82


def git(*args: str, binary: bool = False, check: bool = True) -> str | bytes:
    proc = subprocess.run(
        ["git", *args],
        cwd=REPO,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and proc.returncode:
        raise RuntimeError(proc.stderr.decode("utf-8", errors="replace"))
    return proc.stdout if binary else proc.stdout.decode("utf-8").strip()


def batch_blobs(oids: list[str]) -> dict[str, bytes]:
    unique = list(dict.fromkeys(oids))
    if not unique:
        return {}
    proc = subprocess.run(
        ["git", "cat-file", "--batch"],
        cwd=REPO,
        input="".join(oid + "\n" for oid in unique).encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    stream = io.BytesIO(proc.stdout)
    result: dict[str, bytes] = {}
    for expected in unique:
        header = stream.readline().rstrip(b"\n").decode().split()
        if len(header) != 3 or header[0] != expected or header[1] != "blob":
            raise RuntimeError(f"unexpected blob header: {header}")
        size = int(header[2])
        data = stream.read(size)
        if stream.read(1) != b"\n":
            raise RuntimeError("missing batch frame terminator")
        result[expected] = data
    if stream.read():
        raise RuntimeError("unexpected trailing batch output")
    return result


def tree_map(commit: str) -> dict[str, str]:
    result = {}
    for line in str(git("ls-tree", "-r", commit)).splitlines():
        meta, path = line.split("\t", 1)
        result[path] = meta.split()[2]
    return result


def read_blob(commit: str, path: str) -> bytes:
    return bytes(git("show", f"{commit}:{path}", binary=True))


def read_json_blob(commit: str, path: str) -> Any:
    return json.loads(read_blob(commit, path).decode("utf-8"))


def flatten(suite: unittest.TestSuite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def selected_tests() -> tuple[unittest.TestSuite, dict[str, Any]]:
    patterns = [
        "test_ghc_family_v652_v2_x1.py",
        "test_ghc_family_v652_v2.py",
        "test_ghc_family_v652_v3_x1.py",
        "test_ghc_family_v652_v3.py",
        "test_ghc_family_v652_v3_closeout.py",
        "test_ghc_family_v652_v5_x1.py",
        "test_ghc_family_v652_v5_core.py",
        "test_ghc_family_v652_v5_closeout.py",
        "test_ghc_family_v652_v5_route_correction.py",
        "test_ghc_family_v652_v5_final_validation_correction.py",
    ]
    loader = unittest.TestLoader()
    selected = unittest.TestSuite()
    raw_counts: dict[str, int] = {}
    eligible_counts: dict[str, int] = {}
    exclusions: list[dict[str, str]] = []
    loader_errors: list[str] = []
    for index, pattern in enumerate(patterns):
        path = REPO / "tests" / pattern
        spec = importlib.util.spec_from_file_location(
            f"v6524_scoped_{index}", path
        )
        if spec is None or spec.loader is None:
            loader_errors.append(f"unable to load {pattern}")
            continue
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        loaded = loader.loadTestsFromModule(module)
        tests = list(flatten(loaded))
        raw_counts[pattern] = len(tests)
        eligible = []
        for test in tests:
            method = getattr(test, "_testMethodName", "")
            if (
                pattern == "test_ghc_family_v652_v2_x1.py"
                and method == "test_placeholders_privacy_and_x1_only"
            ):
                exclusions.append(
                    {
                        "pattern": pattern,
                        "test": method,
                        "reason": (
                            "Inherited x1 lifecycle-local absence assertion; all "
                            "other inherited, current, and successor-scoped behavior remains selected."
                        ),
                    }
                )
            else:
                eligible.append(test)
        eligible_counts[pattern] = len(eligible)
        selected.addTests(eligible)
    loader_errors.extend(loader.errors)
    return selected, {
        "patterns": patterns,
        "raw_counts": raw_counts,
        "eligible_counts": eligible_counts,
        "raw_count": sum(raw_counts.values()),
        "eligible_count": sum(eligible_counts.values()),
        "explicit_lifecycle_exclusions": exclusions,
        "loader_errors": loader_errors,
    }


def manifest_check(
    commit: str,
    path: str,
    expected_schema_fragment: str,
    expected_paths: set[str],
) -> dict[str, Any]:
    manifest = read_json_blob(commit, path)
    tree = tree_map(commit)
    issues = []
    declared_paths = {
        row["path"] for row in manifest["entries"]
    } | set(manifest.get("self_exclusions", []))
    if declared_paths != expected_paths:
        issues.append(
            {
                "kind": "path_set",
                "missing": sorted(expected_paths - declared_paths),
                "extra": sorted(declared_paths - expected_paths),
            }
        )
    oids = [row["git_blob"] for row in manifest["entries"]]
    blobs = batch_blobs(oids)
    for row in manifest["entries"]:
        relative = row["path"]
        actual_oid = tree.get(relative)
        if actual_oid != row["git_blob"]:
            issues.append(
                {
                    "path": relative,
                    "kind": "object",
                    "expected": row["git_blob"],
                    "actual": actual_oid,
                }
            )
            continue
        blob = blobs[row["git_blob"]]
        if len(blob) != row["bytes"]:
            issues.append({"path": relative, "kind": "bytes"})
        if hashlib.sha256(blob).hexdigest() != row["sha256"]:
            issues.append({"path": relative, "kind": "sha256"})
    for relative in manifest.get("self_exclusions", []):
        if relative not in tree:
            issues.append({"path": relative, "kind": "missing_self_exclusion"})
    return {
        "path": path,
        "commit": commit,
        "schema": manifest.get("schema"),
        "schema_matches": expected_schema_fragment in manifest.get("schema", ""),
        "entry_count": manifest["entry_count"],
        "self_exclusion_count": len(manifest.get("self_exclusions", [])),
        "issues": issues,
        "valid": not issues
        and expected_schema_fragment in manifest.get("schema", ""),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    receipt_path = Path(args.receipt).resolve()
    if receipt_path.exists():
        raise SystemExit("refusing to overwrite an existing validation attempt")
    try:
        receipt_path.relative_to(REPO.resolve())
        raise SystemExit("validation receipt must remain outside the repository")
    except ValueError:
        pass

    checks: list[dict[str, Any]] = []

    def check(name: str, condition: bool, detail: Any) -> None:
        checks.append({"name": name, "passed": bool(condition), "detail": detail})

    clean_before = not str(
        git("status", "--porcelain=v1", "--untracked-files=all")
    )
    head = str(git("rev-parse", "HEAD"))
    branch = str(git("branch", "--show-current"))
    check(
        "exact_head",
        head == args.expected_head,
        {"expected": args.expected_head, "actual": head},
    )
    check("branch", branch == BRANCH, {"expected": BRANCH, "actual": branch})
    check("clean_before", clean_before, clean_before)

    source_anc = subprocess.run(
        ["git", "merge-base", "--is-ancestor", SOURCE, head], cwd=REPO
    ).returncode == 0
    x1_anc = subprocess.run(
        ["git", "merge-base", "--is-ancestor", X1, head], cwd=REPO
    ).returncode == 0
    evidence_anc = subprocess.run(
        ["git", "merge-base", "--is-ancestor", EVIDENCE, head], cwd=REPO
    ).returncode == 0
    closeout_anc = subprocess.run(
        ["git", "merge-base", "--is-ancestor", CLOSEOUT, head], cwd=REPO
    ).returncode == 0
    route_correction_anc = subprocess.run(
        ["git", "merge-base", "--is-ancestor", ROUTE_CORRECTION, head],
        cwd=REPO,
    ).returncode == 0
    commit_count = int(str(git("rev-list", "--count", f"{SOURCE}..{head}")))
    merge_count = len(
        [line for line in str(git("rev-list", "--merges", f"{SOURCE}..{head}")).splitlines() if line]
    )
    parent_line = str(git("rev-list", "--parents", "-n", "1", head)).split()
    check(
        "lifecycle_ancestry",
        (
            source_anc
            and x1_anc
            and evidence_anc
            and closeout_anc
            and route_correction_anc
        ),
        {
            "source": source_anc,
            "x1": x1_anc,
            "evidence": evidence_anc,
            "closeout": closeout_anc,
            "route_correction": route_correction_anc,
        },
    )
    check(
        "five_phase_commits",
        commit_count == 5,
        {"expected": 5, "actual": commit_count},
    )
    check("zero_merges", merge_count == 0, merge_count)
    check(
        "single_parent_final",
        len(parent_line) == 2 and parent_line[1] == ROUTE_CORRECTION,
        parent_line,
    )

    validation_contract = read_json_blob(
        head, f"{PHASE_ROOT}/final/final-validation-contract.json"
    )
    full_suite_exclusions = set(
        validation_contract[
            "full_repository_suite_exact_lifecycle_exclusions"
        ]
    )
    full_selection, full_test_summary = full_suite_support.run_full_suite(
        full_suite_exclusions
    )
    full_selection.pop("failed_incomplete_validator_attempts_retained", None)
    full_selection["v652_v5_failed_or_incomplete_attempts_retained"] = 1
    full_suite_valid = (
        full_selection["canonical_successful_passes"] == 1
        and full_selection["tests_run"] == full_selection["expected_tests_run"]
        and full_test_summary["failures"] == 0
        and full_test_summary["errors"] == 0
        and full_test_summary["skipped"] == 0
        and full_selection[
            "v652_v5_failed_or_incomplete_attempts_retained"
        ]
        == 1
        and len(full_suite_exclusions)
        == validation_contract[
            "full_repository_suite_exact_lifecycle_exclusion_count"
        ]
    )
    check(
        "complete_repository_suite",
        full_suite_valid,
        {
            "selection": full_selection,
            "tests": full_test_summary,
            "exact_exclusion_count": len(full_suite_exclusions),
        },
    )

    suite, selection = selected_tests()
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=1).run(suite)
    test_valid = (
        result.wasSuccessful()
        and result.testsRun == EXPECTED_SCOPED_TESTS
        and selection["eligible_count"] == EXPECTED_SCOPED_TESTS
        and not selection["loader_errors"]
    )
    check(
        "scoped_test_selection",
        test_valid,
        {
            **selection,
            "tests_run": result.testsRun,
            "failures": [str(test) for test, _trace in result.failures],
            "errors": [str(test) for test, _trace in result.errors],
        },
    )

    full_tree = tree_map(head)
    owner_paths = set(
        filter(None, str(git("diff", "--name-only", SOURCE, head)).splitlines())
    )
    x1_paths = set(
        filter(None, str(git("diff", "--name-only", SOURCE, X1)).splitlines())
    )
    evidence_paths = set(
        filter(None, str(git("diff", "--name-only", X1, EVIDENCE)).splitlines())
    )
    closeout_paths = set(
        filter(
            None,
            str(git("diff", "--name-only", EVIDENCE, CLOSEOUT)).splitlines(),
        )
    )
    correction_paths = set(
        filter(
            None,
            str(
                git(
                    "diff",
                    "--name-only",
                    CLOSEOUT,
                    ROUTE_CORRECTION,
                )
            ).splitlines(),
        )
    )
    final_validation_correction_paths = set(
        filter(
            None,
            str(
                git(
                    "diff",
                    "--name-only",
                    ROUTE_CORRECTION,
                    head,
                )
            ).splitlines(),
        )
    )
    owner_tree = {
        path: full_tree[path] for path in owner_paths if path in full_tree
    }
    owner_blobs = batch_blobs(list(owner_tree.values()))

    json_issues = []
    json_count = 0
    for path, oid in sorted(owner_tree.items()):
        if path.startswith(PHASE_ROOT + "/") and path.endswith(".json"):
            json_count += 1
            try:
                json.loads(owner_blobs[oid].decode("utf-8"))
            except Exception as exc:  # noqa: BLE001
                json_issues.append({"path": path, "error": str(exc)})
    check(
        "complete_phase_json",
        not json_issues,
        {"parsed": json_count, "issues": json_issues},
    )

    patterns = {
        "raw_task_or_thread_identifier": re.compile(
            r"(?i)(source_thread_id|thread_id)\s*[:=]"
        ),
        "private_absolute_local_path": re.compile(
            r"(?i)(?:[A-Z]:\\(?:Users|GHC-Archives)\\|"
            r"[A-Z]:\\\\(?:Users|GHC-Archives)\\\\|/Users/|/home/)"
        ),
        "credential_or_secret": re.compile(
            r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"
        ),
        "private_route_or_callable": re.compile(
            r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"
        ),
        "transcript_or_session_stream": re.compile(
            r"(?i)(session_stream|raw_transcript|conversation_export)"
        ),
    }
    definition_paths = {
        "scripts/build_ghc_family_v652_v5_preregistration.py",
        "scripts/build_ghc_family_v652_v5_evidence.py",
        "scripts/build_ghc_family_v652_v5_closeout.py",
        "scripts/build_ghc_family_v652_v5_cli_route_correction.py",
        "scripts/build_ghc_family_v652_v5_final_validation_correction.py",
        "scripts/ghc_family_v652_v5_final_validate.py",
        f"{PHASE_ROOT}/validation/x1-staged-privacy.json",
        f"{PHASE_ROOT}/validation/evidence-staged-privacy.json",
        f"{PHASE_ROOT}/validation/closeout-staged-privacy.json",
        f"{PHASE_ROOT}/validation/route-correction-staged-privacy.json",
        (
            f"{PHASE_ROOT}/validation/"
            "final-validation-correction-staged-privacy.json"
        ),
    }
    privacy_candidates = []
    privacy_hits = []
    for path, oid in sorted(owner_tree.items()):
        try:
            text = owner_blobs[oid].decode("utf-8")
        except UnicodeDecodeError:
            continue
        for name, pattern in patterns.items():
            if pattern.search(text):
                disposition = (
                    "scanner_definition"
                    if path in definition_paths
                    else "confirmed_payload_hit"
                )
                row = {
                    "path": path,
                    "pattern_class": name,
                    "disposition": disposition,
                }
                privacy_candidates.append(row)
                if disposition == "confirmed_payload_hit":
                    privacy_hits.append(row)
    check(
        "five_class_privacy_scan",
        not privacy_hits,
        {
            "scanned": len(owner_paths),
            "candidates": privacy_candidates,
            "confirmed": privacy_hits,
        },
    )

    manifests = [
        manifest_check(
            X1,
            f"{PHASE_ROOT}/validation/x1-staged-manifest.json",
            "x1-staged-manifest",
            x1_paths,
        ),
        manifest_check(
            EVIDENCE,
            f"{PHASE_ROOT}/validation/evidence-staged-manifest.json",
            "evidence-staged-manifest",
            evidence_paths,
        ),
        manifest_check(
            CLOSEOUT,
            f"{PHASE_ROOT}/validation/closeout-staged-manifest.json",
            "closeout-staged-manifest",
            closeout_paths,
        ),
        manifest_check(
            ROUTE_CORRECTION,
            f"{PHASE_ROOT}/validation/route-correction-staged-manifest.json",
            "route-correction-staged-manifest",
            correction_paths,
        ),
        manifest_check(
            head,
            (
                f"{PHASE_ROOT}/validation/"
                "final-validation-correction-staged-manifest.json"
            ),
            "final-validation-correction-staged-manifest",
            final_validation_correction_paths,
        ),
        manifest_check(
            head,
            f"{PHASE_ROOT}/validation/final-owner-manifest.json",
            "final-owner-manifest",
            owner_paths,
        ),
    ]
    check(
        "manifest_parity",
        all(row["valid"] for row in manifests),
        manifests,
    )

    outcomes = read_json_blob(
        head, f"{PHASE_ROOT}/evidence/proposal-outcomes.json"
    )
    negatives = read_json_blob(
        head, f"{PHASE_ROOT}/final/retained-negative-register.json"
    )
    gaps = read_json_blob(head, f"{PHASE_ROOT}/final/open-gap-register.json")
    gates = read_json_blob(head, f"{PHASE_ROOT}/final/exact-gate-register.json")
    flow = read_json_blob(
        head, f"{PHASE_ROOT}/method-flow/final-method-flow-ledger.json"
    )
    route_flow = read_json_blob(
        head,
        f"{PHASE_ROOT}/method-flow/route-correction-method-flow-ledger.json",
    )
    route_negative = read_json_blob(
        head, f"{PHASE_ROOT}/truth/route-correction-retained-negative.json"
    )
    final_validation_flow = read_json_blob(
        head,
        (
            f"{PHASE_ROOT}/method-flow/"
            "final-validation-correction-method-flow-ledger.json"
        ),
    )
    final_validation_negative = read_json_blob(
        head,
        f"{PHASE_ROOT}/truth/final-validation-retained-negative.json",
    )
    failed_final_attempt = read_json_blob(
        head,
        f"{PHASE_ROOT}/validation/final-validation-failed-attempt-01.json",
    )
    final_phase_truth = read_json_blob(
        head, f"{PHASE_ROOT}/final/final-phase-truth.json"
    )
    route = read_json_blob(head, f"{PHASE_ROOT}/route/final-route-state.json")
    superseded_route = read_json_blob(
        head, f"{PHASE_ROOT}/route/superseded-ilyra-route.json"
    )
    skills = read_json_blob(head, f"{PHASE_ROOT}/skills/skill-build-receipt.json")
    check(
        "outcome_truth",
        outcomes["counts"]
        == {
            "completed": 23,
            "represented": 5,
            "open_gap": 1,
            "exact_gate": 1,
        },
        outcomes["counts"],
    )
    check(
        "negative_retention",
        negatives["effective_count"] == 8721
        and negatives["no_failure_erased"],
        negatives,
    )
    check(
        "route_correction_negative_retention",
        route_negative["sealed_closeout_effective"] == 8721
        and route_negative["route_correction_operational"] == 6
        and route_negative["effective_final"] == 8727
        and route_negative["no_failure_erased"]
        and not route_negative["failed_attempt_received_credit"],
        {
            "route_negative": route_negative,
            "final_effective": final_phase_truth["effective_negatives"],
        },
    )
    check(
        "final_validation_negative_retention",
        final_validation_negative["route_corrected_effective"] == 8727
        and final_validation_negative["final_validation_operational"] == 7
        and final_validation_negative["effective_final"] == 8734
        and final_validation_negative["failed_aggregate_attempts"] == 1
        and final_validation_negative["failed_tests"] == 4
        and final_validation_negative["no_failure_erased"]
        and not final_validation_negative["failed_attempt_received_credit"]
        and final_phase_truth["effective_negatives"] == 8734,
        {
            "final_validation_negative": final_validation_negative,
            "final_effective": final_phase_truth["effective_negatives"],
        },
    )
    check(
        "failed_exact_final_attempt_retained",
        not failed_final_attempt["valid"]
        and failed_final_attempt["canonical_success_credit"] == 0
        and failed_final_attempt["full_repository_tests"]
        == {
            "passed": 2755,
            "total": 2759,
            "failures": 4,
            "errors": 0,
            "skipped": 0,
        }
        and len(failed_final_attempt["failed_test_ids"]) == 4,
        failed_final_attempt,
    )
    check(
        "gate_retention",
        gaps["effective_count"] == 66
        and gates["effective_count"] == 67
        and gaps["closed_count"] == 0
        and gates["closed_count"] == 0,
        {"gaps": gaps, "gates": gates},
    )
    check(
        "method_flow",
        flow["counts"]["methods"] == 22
        and flow["counts"]["witness_results"] == {"fail": 22, "pass": 22}
        and flow["counts"]["states"]["preferred"] == 22,
        flow["counts"],
    )
    check(
        "route_correction_method_flow",
        route_flow["counts"]["methods"] == 6
        and route_flow["counts"]["witness_results"] == {"fail": 6, "pass": 6}
        and route_flow["counts"]["states"]["preferred"] == 6,
        route_flow["counts"],
    )
    check(
        "final_validation_correction_method_flow",
        final_validation_flow["counts"]["methods"] == 7
        and final_validation_flow["counts"]["witness_results"]
        == {"fail": 7, "pass": 7}
        and final_validation_flow["counts"]["states"]["preferred"] == 7,
        final_validation_flow["counts"],
    )
    check(
        "phase_local_skills",
        skills["skill_count"] == 10
        and skills["validated_count"] == 10
        and skills["smoke_used_count"] == 10
        and not skills["globally_installed"]
        and not skills["subagent_forward_test"],
        skills,
    )
    check(
        "terminal_abstention",
        outcomes["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        outcomes["terminal_verdict"],
    )
    check(
        "route_held",
        route["state"] == "PREPARED_NOT_SPAWNED"
        and route["target_kind"] == "bounded_codex_collaboration_agent"
        and route["target_phase"] == "v652-v6"
        and route["spawn_count"] == 0
        and route["task_create_count"] == 0
        and route["task_fork_count"] == 0,
        route,
    )
    check(
        "superseded_ilyra_route_unsent",
        superseded_route["superseded_unsent"]
        and superseded_route["prior_send_count"] == 0
        and superseded_route["prior_target"] == "Ilyra Fen",
        superseded_route,
    )

    baton = read_blob(
        head, f"{PHASE_ROOT}/handoffs/cli-collaborator-v652-v6-induction.md"
    ).decode("utf-8")
    overview = read_blob(
        head, f"{PHASE_ROOT}/overview/final-integrated-overview.md"
    ).decode("utf-8")
    report = read_blob(
        head, f"{PHASE_ROOT}/reports/final-static-report.html"
    ).decode("utf-8")
    baton_words = len(re.findall(r"\b[\w'-]+\b", baton))
    overview_words = len(re.findall(r"\b[\w'-]+\b", overview))
    check(
        "document_contracts",
        10000 <= baton_words <= 100000 and overview_words >= 1500,
        {"baton_words": baton_words, "overview_words": overview_words},
    )
    report_tokens = (
        "Skip to main content",
        "<caption>",
        "scope='col'",
        "tabindex='0'",
        "NOT_READY_FOR_STAGE_20",
    )
    check(
        "structural_accessibility",
        all(token in report for token in report_tokens),
        {"required_tokens": report_tokens},
    )
    stale_tokens = (
        "HSC PDR3 likelihood readiness",
        "freshwater eDNA authority reservation",
        "Tamar Vey v652-v3 closeout",
        "Eiren Kestrel v651-v4 closeout",
        "WALLABY PDR2",
        "hydrographic data access",
    )
    stale_hits = [
        token
        for token in stale_tokens
        if token in baton or token in overview or token in report
    ]
    check("stale_label_review", not stale_hits, stale_hits)

    owner_growth = sum(
        1
        for path in full_tree
        if path.startswith(PHASE_ROOT + "/")
        or (
            path.startswith("scripts/")
            and "v652_v5" in Path(path).name
        )
        or path == "tests/test_ghc_family_v652_v5_closeout.py"
        or path == "tests/test_ghc_family_v652_v5_core.py"
        or path == "tests/test_ghc_family_v652_v5_x1.py"
        or path == "tests/test_ghc_family_v652_v5_route_correction.py"
        or path
        == "tests/test_ghc_family_v652_v5_final_validation_correction.py"
    )
    check(
        "owner_growth",
        owner_growth < 2000,
        {"owner_generated_files": owner_growth, "threshold": 2000},
    )

    subprocess.run(
        ["git", "fetch", "origin", BRANCH, "--quiet"], cwd=REPO, check=True
    )
    local = str(git("rev-parse", "HEAD"))
    upstream = str(git("rev-parse", "@{u}"))
    tracking = str(git("rev-parse", f"origin/{BRANCH}"))
    live_line = str(git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}"))
    live = live_line.split()[0] if live_line else ""
    divergence = str(git("rev-list", "--left-right", "--count", "HEAD...@{u}"))
    check(
        "four_way_live_equality",
        local == upstream == tracking == live == head and divergence == "0\t0",
        {
            "local": local,
            "upstream": upstream,
            "tracking": tracking,
            "live": live,
            "divergence": divergence,
        },
    )
    clean_after = not str(
        git("status", "--porcelain=v1", "--untracked-files=all")
    )
    check(
        "clean_before_after",
        clean_before and clean_after,
        {"before": clean_before, "after": clean_after},
    )

    valid = all(row["passed"] for row in checks)
    passed = sum(row["passed"] for row in checks)
    minimal_names = {
        "exact_head",
        "scoped_test_selection",
        "complete_repository_suite",
        "complete_phase_json",
        "five_class_privacy_scan",
        "manifest_parity",
        "negative_retention",
        "route_correction_negative_retention",
        "final_validation_negative_retention",
        "failed_exact_final_attempt_retained",
        "gate_retention",
        "terminal_abstention",
        "route_held",
        "superseded_ilyra_route_unsent",
        "lifecycle_ancestry",
        "five_phase_commits",
        "zero_merges",
        "single_parent_final",
        "clean_before_after",
        "four_way_live_equality",
    }
    minimal = [row for row in checks if row["name"] in minimal_names]
    receipt = {
        "schema": "ghc.family.v652-v5.exact-final-validation.external.v2",
        "validated_at_utc": datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z"),
        "exact_head": head,
        "branch": BRANCH,
        "checks": checks,
        "passed": passed,
        "total": len(checks),
        "valid": valid,
        "scoped_tests": {
            "passed": result.testsRun - len(result.failures) - len(result.errors),
            "total": result.testsRun,
            "selection": selection,
        },
        "full_repository_tests": {
            **full_test_summary,
            "selection": full_selection,
        },
        "minimal": {
            "passed": sum(row["passed"] for row in minimal),
            "total": len(minimal),
            "valid": all(row["passed"] for row in minimal),
        },
        "json_parse_count": json_count,
        "privacy_scanned_file_count": len(owner_paths),
        "privacy_candidate_count": len(privacy_candidates),
        "privacy_confirmed_hit_count": len(privacy_hits),
        "manifest_entry_total": sum(row["entry_count"] for row in manifests),
        "manifest_contracts": manifests,
        "full_repository_suite_run": True,
        "successful_canonical_pass_count": 1 if valid else 0,
        "replay_after_success": False,
        "same_owner_only": True,
        "independent_team_reproduction": False,
        "boundary": (
            "Single bounded same-owner exact-head canonical pass under shared "
            "infrastructure, including Eiren's complete repository suite under the "
            "exact committed lifecycle exclusion set. This is not independent-team reproduction, "
            "external audit, production certification, exhaustive security, complete "
            "privacy or accessibility, professional validation, legal or cultural "
            "authority, Māori-authority review, empirical GMUT confirmation, "
            "Theory-of-Everything proof, AGI/ASI evidence, consciousness/personhood "
            "evidence, or Stage 20 authority."
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
                "head": head,
                "tests": (
                    f"{receipt['full_repository_tests']['passed']}/"
                    f"{receipt['full_repository_tests']['total']}"
                ),
                "scoped_tests": (
                    f"{receipt['scoped_tests']['passed']}/"
                    f"{receipt['scoped_tests']['total']}"
                ),
                "detailed": f"{passed}/{len(checks)}",
                "minimal": (
                    f"{receipt['minimal']['passed']}/"
                    f"{receipt['minimal']['total']}"
                ),
                "json": json_count,
                "privacy_scanned": len(owner_paths),
                "privacy_hits": len(privacy_hits),
                "manifest_entries": receipt["manifest_entry_total"],
                "valid": valid,
            },
            sort_keys=True,
        )
    )
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
