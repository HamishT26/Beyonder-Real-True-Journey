#!/usr/bin/env python3
"""Single launch-scoped exact-final validator for Tavian Sol v652-v6."""

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


sys.dont_write_bytecode = True
REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
PHASE_ROOT = "docs/tavian-sol/v652-v6"
SOURCE = "ad2a2e472c8e859296e62f1d2d6ce1f9f2b2b584"
X1 = "9e5074cd42a0fdcbc342980c1960c15a30abe28f"
EVIDENCE = "58b0ecfd1af72ba4cdee5657a87275747bbcbe0a"
CLOSEOUT = "bdb02fbe63e189700b915e18c45bc00b80e5aaeb"
CORRECTION1 = "6c6e491e5f1163979879865ce820ea718ed94084"
BRANCH = "codex/GHC-Family/tavian-sol-v652-v6-cli"
EXPECTED_SCOPED_TESTS = 58
EXPECTED_NEGATIVES = 8916
EXPECTED_OPEN_GAPS = 67
EXPECTED_EXACT_GATES = 68
TEST_PATTERNS = [
    "test_ghc_family_v652_v5_closeout.py",
    "test_ghc_family_v652_v5_route_correction.py",
    "test_ghc_family_v652_v5_final_validation_correction.py",
    "test_ghc_family_v652_v6_x1.py",
    "test_ghc_family_v652_v6_core.py",
    "test_ghc_family_v652_v6_closeout.py",
    "test_ghc_family_v652_v6_final_validation_correction.py",
]


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
        input="".join(oid + "\n" for oid in unique).encode("ascii"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    stream = io.BytesIO(proc.stdout)
    result: dict[str, bytes] = {}
    for expected in unique:
        header = stream.readline().rstrip(b"\n").decode("ascii").split()
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
    result: dict[str, str] = {}
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
    loader = unittest.TestLoader()
    selected = unittest.TestSuite()
    counts: dict[str, int] = {}
    errors: list[str] = []
    for index, pattern in enumerate(TEST_PATTERNS):
        path = REPO / "tests" / pattern
        if not path.is_file():
            errors.append(f"missing test module: {pattern}")
            continue
        spec = importlib.util.spec_from_file_location(
            f"tavian_v652_v6_scoped_{index}", path
        )
        if spec is None or spec.loader is None:
            errors.append(f"unable to load test module: {pattern}")
            continue
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        loaded = loader.loadTestsFromModule(module)
        tests = list(flatten(loaded))
        counts[pattern] = len(tests)
        selected.addTests(tests)
    errors.extend(loader.errors)
    return selected, {
        "patterns": TEST_PATTERNS,
        "module_counts": counts,
        "eligible_count": sum(counts.values()),
        "explicit_lifecycle_exclusions": [],
        "loader_errors": errors,
    }


def manifest_check(
    commit: str,
    path: str,
    expected_schema_fragment: str,
    expected_paths: set[str],
) -> dict[str, Any]:
    manifest = read_json_blob(commit, path)
    tree = tree_map(commit)
    issues: list[dict[str, Any]] = []
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
    blobs = batch_blobs([row["git_blob"] for row in manifest["entries"]])
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
    schema_matches = expected_schema_fragment in manifest.get("schema", "")
    return {
        "path": path,
        "commit": commit,
        "schema": manifest.get("schema"),
        "schema_matches": schema_matches,
        "entry_count": manifest["entry_count"],
        "self_exclusion_count": len(manifest.get("self_exclusions", [])),
        "issues": issues,
        "valid": not issues and schema_matches,
    }


def inherited_repository_receipt() -> dict[str, Any]:
    """Represent Eiren's source-head receipt without rerunning its suite."""
    receipt_path = (
        REPO.parents[1]
        / "validation"
        / f"eiren-v652-v5-{SOURCE}.json"
    )
    raw = receipt_path.read_bytes()
    payload = json.loads(raw.decode("utf-8"))
    full = payload["full_repository_tests"]
    selection = full["selection"]
    valid = (
        payload["valid"]
        and payload["exact_head"] == SOURCE
        and full["passed"] == 2761
        and full["total"] == 2761
        and selection["tests_discovered"] == 2800
        and selection["tests_run"] == 2761
        and selection["tests_excluded"] == 39
        and selection["canonical_successful_passes"] == 1
        and not selection["post_success_replay"]
    )
    return {
        "owner": "Eiren Kestrel",
        "source_head": SOURCE,
        "receipt_name": receipt_path.name,
        "receipt_sha256": hashlib.sha256(raw).hexdigest(),
        "valid": valid,
        "passed": full["passed"],
        "total": full["total"],
        "tests_discovered": selection["tests_discovered"],
        "tests_excluded": selection["tests_excluded"],
        "canonical_successful_passes": selection[
            "canonical_successful_passes"
        ],
        "post_success_replay": selection["post_success_replay"],
        "represented_only": True,
        "rerun_by_tavian": False,
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

    ancestry = {
        name: subprocess.run(
            ["git", "merge-base", "--is-ancestor", commit, head],
            cwd=REPO,
        ).returncode
        == 0
        for name, commit in {
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "closeout": CLOSEOUT,
            "correction1": CORRECTION1,
        }.items()
    }
    commit_count = int(str(git("rev-list", "--count", f"{SOURCE}..{head}")))
    merge_count = len(
        [
            row
            for row in str(
                git("rev-list", "--merges", f"{SOURCE}..{head}")
            ).splitlines()
            if row
        ]
    )
    parent_line = str(git("rev-list", "--parents", "-n", "1", head)).split()
    check("lifecycle_ancestry", all(ancestry.values()), ancestry)
    check(
        "five_phase_commits",
        commit_count == 5,
        {"expected": 5, "actual": commit_count},
    )
    check("zero_merges", merge_count == 0, merge_count)
    check(
        "single_parent_final",
        len(parent_line) == 2 and parent_line[1] == CORRECTION1,
        parent_line,
    )

    contract = read_json_blob(
        head, f"{PHASE_ROOT}/final/final-validation-contract.json"
    )
    contract_valid = (
        contract["validation_scope"] == "launch_scoped"
        and contract["launch_scoped_validator_owner"] == "Tavian Sol"
        and contract["expected_scoped_tests"] == EXPECTED_SCOPED_TESTS
        and contract["patterns"] == TEST_PATTERNS
        and contract["explicit_lifecycle_exclusions"] == []
        and not contract["full_repository_suite_required"]
        and not contract["full_repository_suite_run_at_exact_final"]
        and contract["full_repository_suite_owner"] == "Eiren Kestrel"
        and contract["inherited_full_repository_receipt_represented"]
        and contract["expected_phase_commits"] == 5
        and contract["retained_failed_exact_final_attempts"] == 2
        and contract["successful_pass_limit"] == 1
        and not contract["replay_after_success"]
    )
    check("launch_scoped_contract", contract_valid, contract)

    inherited_receipt = inherited_repository_receipt()
    check(
        "inherited_full_repository_receipt_representation",
        inherited_receipt["valid"]
        and inherited_receipt["represented_only"]
        and not inherited_receipt["rerun_by_tavian"],
        inherited_receipt,
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
        "launch_scoped_tests",
        test_valid,
        {
            **selection,
            "tests_run": result.testsRun,
            "failures": [str(test) for test, _trace in result.failures],
            "errors": [str(test) for test, _trace in result.errors],
            "skipped": len(result.skipped),
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
    correction1_paths = set(
        filter(
            None,
            str(git("diff", "--name-only", CLOSEOUT, CORRECTION1)).splitlines(),
        )
    )
    correction2_paths = set(
        filter(
            None,
            str(git("diff", "--name-only", CORRECTION1, head)).splitlines(),
        )
    )
    closeout_owner_paths = set(
        filter(
            None,
            str(git("diff", "--name-only", SOURCE, CLOSEOUT)).splitlines(),
        )
    )
    owner_tree = {
        path: full_tree[path] for path in owner_paths if path in full_tree
    }
    owner_blobs = batch_blobs(list(owner_tree.values()))

    json_issues: list[dict[str, str]] = []
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

    privacy_patterns = {
        "raw_task_or_thread_identifier": re.compile(
            r"(?i)(source_thread_id|thread_id)\s*[:=]"
        ),
        "private_absolute_local_path": re.compile(
            r"(?i)(?:[A-Z]:\\[^\s\"']+|[A-Z]:\\\\[^\s\"']+|"
            r"/Users/[^\s\"']+|/home/[^\s\"']+)"
        ),
        "credential_or_secret": re.compile(
            r"(?i)(api[_-]?key|client_secret|private_key|"
            r"bearer\s+[A-Za-z0-9._-]{12,})"
        ),
        "private_route_or_callable": re.compile(
            r"(?i)(private_route|callable_identifier|"
            r"browser_send_submitted_response_active)"
        ),
        "transcript_or_session_stream": re.compile(
            r"(?i)(session_stream|raw_transcript|conversation_export)"
        ),
    }
    definition_paths = {
        "scripts/build_ghc_family_v652_v6_preregistration.py",
        "scripts/build_ghc_family_v652_v6_evidence.py",
        "scripts/build_ghc_family_v652_v6_closeout.py",
        "scripts/build_ghc_family_v652_v6_final_validation_correction.py",
        "scripts/build_ghc_family_v652_v6_final_validation_correction_2.py",
        "scripts/ghc_family_v652_v6_final_validate.py",
        f"{PHASE_ROOT}/validation/x1-staged-privacy.json",
        f"{PHASE_ROOT}/validation/evidence-staged-privacy.json",
        f"{PHASE_ROOT}/validation/closeout-staged-privacy.json",
        (
            f"{PHASE_ROOT}/validation/"
            "final-validation-correction-staged-privacy.json"
        ),
        (
            f"{PHASE_ROOT}/validation/"
            "final-validation-correction-2-staged-privacy.json"
        ),
    }
    privacy_candidates: list[dict[str, str]] = []
    privacy_hits: list[dict[str, str]] = []
    for path, oid in sorted(owner_tree.items()):
        try:
            text = owner_blobs[oid].decode("utf-8")
        except UnicodeDecodeError:
            continue
        for pattern_class, pattern in privacy_patterns.items():
            if pattern.search(text):
                disposition = (
                    "scanner_definition"
                    if path in definition_paths
                    else "confirmed_payload_hit"
                )
                row = {
                    "path": path,
                    "pattern_class": pattern_class,
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
            CLOSEOUT,
            f"{PHASE_ROOT}/validation/final-owner-manifest.json",
            "final-owner-manifest",
            closeout_owner_paths,
        ),
        manifest_check(
            CORRECTION1,
            (
                f"{PHASE_ROOT}/validation/"
                "final-validation-correction-staged-manifest.json"
            ),
            "final-validation-correction-staged-manifest",
            correction1_paths,
        ),
        manifest_check(
            CORRECTION1,
            f"{PHASE_ROOT}/validation/final-corrected-owner-manifest.json",
            "final-corrected-owner-manifest",
            set(
                filter(
                    None,
                    str(
                        git("diff", "--name-only", SOURCE, CORRECTION1)
                    ).splitlines(),
                )
            ),
        ),
        manifest_check(
            head,
            (
                f"{PHASE_ROOT}/validation/"
                "final-validation-correction-2-staged-manifest.json"
            ),
            "final-validation-correction-2-staged-manifest",
            correction2_paths,
        ),
        manifest_check(
            head,
            f"{PHASE_ROOT}/validation/final-corrected-owner-manifest-v2.json",
            "final-corrected-owner-manifest-v2",
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
    route = read_json_blob(head, f"{PHASE_ROOT}/route/final-route-state.json")
    skills = read_json_blob(head, f"{PHASE_ROOT}/skills/skill-build-receipt.json")
    final_truth = read_json_blob(
        head, f"{PHASE_ROOT}/final/final-phase-truth.json"
    )
    build_receipt = read_json_blob(
        head, f"{PHASE_ROOT}/validation/closeout-build-receipt.json"
    )
    closeout_receipt = read_json_blob(
        head, f"{PHASE_ROOT}/validation/closeout-validation-receipt.json"
    )
    minimal_receipt = read_json_blob(
        head, f"{PHASE_ROOT}/validation/closeout-minimal-validation.json"
    )
    failed_attempt = read_json_blob(
        head, f"{PHASE_ROOT}/validation/final-validation-failed-attempt-01.json"
    )
    correction_failed_attempt = read_json_blob(
        head,
        (
            f"{PHASE_ROOT}/validation/"
            "final-validation-correction-failed-attempt-01.json"
        ),
    )
    diagnostic_failed_attempt = read_json_blob(
        head,
        (
            f"{PHASE_ROOT}/validation/"
            "final-validation-diagnostic-failed-attempt-01.json"
        ),
    )
    correction_receipt = read_json_blob(
        head,
        (
            f"{PHASE_ROOT}/validation/"
            "final-validation-correction-validation-receipt.json"
        ),
    )
    failed_attempt_2 = read_json_blob(
        head, f"{PHASE_ROOT}/validation/final-validation-failed-attempt-02.json"
    )
    patch_failed_attempt = read_json_blob(
        head,
        (
            f"{PHASE_ROOT}/validation/"
            "final-validation-patch-failed-attempt-01.json"
        ),
    )
    correction_receipt_2 = read_json_blob(
        head,
        (
            f"{PHASE_ROOT}/validation/"
            "final-validation-correction-2-validation-receipt.json"
        ),
    )

    expected_outcomes = {
        "completed": 23,
        "represented": 5,
        "open_gap": 1,
        "exact_gate": 1,
    }
    check(
        "outcome_truth",
        outcomes["counts"] == expected_outcomes
        and outcomes["proposal_count"] == 30
        and outcomes["mutation_count"] == 150
        and outcomes["mutation_rejected_or_quarantined_count"] == 150,
        {
            "counts": outcomes["counts"],
            "proposals": outcomes["proposal_count"],
            "mutations": outcomes["mutation_count"],
            "rejected_or_quarantined": outcomes[
                "mutation_rejected_or_quarantined_count"
            ],
        },
    )
    check(
        "negative_retention",
        negatives["effective_count"] == EXPECTED_NEGATIVES
        and negatives["inherited"] == 8736
        and negatives["x1_operational"] == 17
        and negatives["x2_operational"] == 2
        and negatives["closeout_lifecycle_operational"] == 5
        and negatives["final_validation_operational"] == 6
        and negatives["synthetic_mutations"] == 150
        and negatives["no_failure_erased"]
        and negatives["failed_attempts_receive_zero_aggregate_credit"]
        and final_truth["effective_negatives"] == EXPECTED_NEGATIVES,
        negatives,
    )
    check(
        "gate_retention",
        gaps["effective_count"] == EXPECTED_OPEN_GAPS
        and gates["effective_count"] == EXPECTED_EXACT_GATES
        and gaps["closed_count"] == 0
        and gates["closed_count"] == 0,
        {"gaps": gaps, "gates": gates},
    )
    check(
        "method_flow",
        flow["counts"]["methods"] == 30
        and flow["counts"]["witness_results"] == {"fail": 30, "pass": 30}
        and flow["counts"]["states"]["preferred"] == 30,
        flow["counts"],
    )
    check(
        "failed_exact_final_attempt_retained",
        failed_attempt["attempted_head"] == CLOSEOUT
        and failed_attempt["failure_stage"] == "selected_test_import"
        and failed_attempt["tests_run"] == 0
        and failed_attempt["canonical_success_credit"] == 0
        and not failed_attempt["external_receipt_written"]
        and failed_attempt["retained_negative_id"] == "V6526-FINAL-N01",
        {
            "canonical": failed_attempt,
            "correction": correction_failed_attempt,
            "diagnostic": diagnostic_failed_attempt,
        },
    )
    check(
        "failed_correction_attempts_retained",
        correction_failed_attempt["tests_run"] == 7
        and correction_failed_attempt["passed"] == 6
        and correction_failed_attempt["failures"] == 1
        and correction_failed_attempt["canonical_success_credit"] == 0
        and correction_failed_attempt["retained_negative_id"] == "V6526-FINAL-N02"
        and diagnostic_failed_attempt["tests_run"] == 7
        and diagnostic_failed_attempt["passed"] == 6
        and diagnostic_failed_attempt["failures"] == 1
        and diagnostic_failed_attempt["canonical_success_credit"] == 0
        and diagnostic_failed_attempt["retained_negative_id"] == "V6526-FINAL-N03",
        {
            "correction": correction_failed_attempt,
            "diagnostic": diagnostic_failed_attempt,
        },
    )
    check(
        "failed_exact_final_retry_retained",
        failed_attempt_2["attempted_head"] == CORRECTION1
        and failed_attempt_2["tests_run"] == 58
        and failed_attempt_2["tests_passed"] == 57
        and failed_attempt_2["detailed_passed"] == 27
        and failed_attempt_2["detailed_total"] == 29
        and failed_attempt_2["canonical_success_credit"] == 0
        and failed_attempt_2["external_receipt_written"]
        and failed_attempt_2["retained_negative_id"] == "V6526-FINAL-N05"
        and patch_failed_attempt["canonical_success_credit"] == 0
        and patch_failed_attempt["retained_negative_id"] == "V6526-FINAL-N06",
        {
            "retry": failed_attempt_2,
            "patch": patch_failed_attempt,
        },
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
        "closeout_receipts",
        build_receipt["valid"]
        and build_receipt["expected_scoped_tests"] == 51
        and not build_receipt["full_repository_suite"]
        and closeout_receipt["valid"]
        and not closeout_receipt["full_repository_suite"]
        and minimal_receipt["valid"]
        and correction_receipt["valid"]
        and correction_receipt["correction_tests_passed"] == 7
        and correction_receipt["correction_tests_total"] == 7
        and correction_receipt_2["valid"]
        and correction_receipt_2["correction_2_tests_passed"] == 6
        and correction_receipt_2["correction_2_tests_total"] == 6
        and correction_receipt_2["corrected_closeout_tests_passed"] == 8
        and correction_receipt_2["corrected_closeout_tests_total"] == 8,
        {
            "build": build_receipt,
            "closeout": closeout_receipt,
            "minimal": minimal_receipt,
            "correction": correction_receipt,
            "correction_2": correction_receipt_2,
        },
    )
    check(
        "terminal_abstention",
        outcomes["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
        and final_truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        {
            "outcomes": outcomes["terminal_verdict"],
            "final": final_truth["terminal_verdict"],
        },
    )
    route_valid = (
        route["state"] == "PREPARED_NOT_SENT"
        and route["target_exact_title"] == "Elaren Kestrel"
        and route["target_phase"] == "v652-v7"
        and route["return_owner"] == "Eiren Kestrel"
        and route["send_count"] == 0
        and route["create_or_fork_count"] == 0
        and route["spawn_count"] == 0
        and route["contact_count"] == 0
        and not route["requires_unique_exact_title_resolution"]
        and not route["requires_tool_acknowledgement"]
        and not route["tool_acknowledgement_received"]
    )
    check("route_prepared_not_sent", route_valid, route)

    baton = read_blob(
        head,
        f"{PHASE_ROOT}/handoffs/elaren-kestrel-v652-v7-prepared-baton.md",
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
        "# ILYRA FEN — prepared v652-v6 activation",
        "The IXPE path remained zero-row",
        "THOS meteorological work remains synthetic",
        "Primary focus was Freed ID/CBR Heart",
        "Regge-calculus, Ashtekar-Barbero, Komar-charge, Petrov-classification",
        "`SENT_BY_EIREN_KESTREL = false`",
        "unique existing Ilyra Fen task",
    )
    stale_hits = [
        token
        for token in stale_tokens
        if token in baton or token in overview or token in report
    ]
    check("stale_label_review", not stale_hits, stale_hits)

    owner_growth = len(owner_paths)
    check(
        "owner_growth",
        owner_growth < 2000,
        {"owner_generated_files": owner_growth, "threshold": 2000},
    )

    subprocess.run(
        ["git", "fetch", "origin", BRANCH, "--quiet"],
        cwd=REPO,
        check=True,
    )
    local = str(git("rev-parse", "HEAD"))
    upstream = str(git("rev-parse", "@{u}"))
    tracking = str(git("rev-parse", f"origin/{BRANCH}"))
    live_line = str(
        git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")
    )
    live = live_line.split()[0] if live_line else ""
    divergence = str(git("rev-list", "--left-right", "--count", "HEAD...@{u}"))
    equality = local == upstream == tracking == live == head and divergence == "0\t0"
    check(
        "four_way_live_equality",
        equality,
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
        "lifecycle_ancestry",
        "five_phase_commits",
        "zero_merges",
        "single_parent_final",
        "launch_scoped_contract",
        "inherited_full_repository_receipt_representation",
        "launch_scoped_tests",
        "complete_phase_json",
        "five_class_privacy_scan",
        "manifest_parity",
        "negative_retention",
        "failed_exact_final_attempt_retained",
        "failed_correction_attempts_retained",
        "failed_exact_final_retry_retained",
        "gate_retention",
        "method_flow",
        "terminal_abstention",
        "route_prepared_not_sent",
        "clean_before_after",
        "four_way_live_equality",
    }
    minimal = [row for row in checks if row["name"] in minimal_names]
    receipt = {
        "schema": "ghc.family.v652-v6.exact-final-validation.external.v1",
        "validated_at_utc": datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z"),
        "exact_head": head,
        "branch": BRANCH,
        "validation_scope": "launch_scoped",
        "checks": checks,
        "passed": passed,
        "total": len(checks),
        "valid": valid,
        "launch_scoped_tests": {
            "passed": result.testsRun - len(result.failures) - len(result.errors),
            "total": result.testsRun,
            "selection": selection,
        },
        "full_repository_suite_run": False,
        "full_repository_suite_owner": "Eiren Kestrel",
        "inherited_full_repository_receipt": inherited_receipt,
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
        "successful_canonical_pass_count": 1 if valid else 0,
        "replay_after_success": False,
        "same_owner_only": True,
        "independent_team_reproduction": False,
        "route_state": "PREPARED_NOT_SENT",
        "boundary": (
            "Single bounded same-owner launch-scoped exact-head pass under shared "
            "infrastructure. Eiren Kestrel's source-head full-repository receipt is "
            "represented and was not rerun. This is not independent-team reproduction, "
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
                    f"{receipt['launch_scoped_tests']['passed']}/"
                    f"{receipt['launch_scoped_tests']['total']}"
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
                "full_repository_suite_run": False,
                "valid": valid,
            },
            sort_keys=True,
        )
    )
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
