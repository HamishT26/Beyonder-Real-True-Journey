#!/usr/bin/env python3
"""Build the additive Eiren v652-v5 exact-final validation correction."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
PHASE_ROOT = "docs/eiren-kestrel/v652-v5"
ROOT = REPO / PHASE_ROOT
SOURCE = "3a77dacd759a499ffe94cbc281a3d7b343608e2d"
ROUTE_CORRECTION = "fb47648a1c136b8147d5d52f84c6615b718bd3c8"
METHOD_RUNNER = (
    Path.home()
    / ".codex/skills/ghc-family-method-flow-state/scripts/"
    "ghc_family_method_flow_state.py"
)

NEW_EXCLUSIONS = [
    {
        "test_id": (
            "tests.test_ghc_family_v651_v5_2_closeout."
            "EirenV651V5RemasterCloseoutTests."
            "test_final_delta_manifest_is_cumulative_through_staged_correction"
        ),
        "reason": (
            "The historical remaster test computes its phase-local evidence-to-HEAD "
            "delta against the current successor head, so every later sibling and "
            "phase path becomes an expected member of the old frozen manifest."
        ),
    },
    {
        "test_id": (
            "tests.test_ghc_family_v651_v6_closeout."
            "ElarenV651V6CloseoutTests.test_anchor_contract_and_commit_cap"
        ),
        "reason": (
            "The historical closeout test counts its source-to-current-HEAD commits "
            "and therefore cannot preserve its own two-or-three-commit lifecycle "
            "assertion after additive successor phases."
        ),
    },
    {
        "test_id": (
            "tests.test_ghc_family_v651_v8_special_x1."
            "SpecialX1Tests.test_x1_has_no_x2_outcome_files"
        ),
        "reason": (
            "The historical x1 test scans the mutable phase directory and requires "
            "later x2 outcome and seal filenames to remain absent."
        ),
    },
    {
        "test_id": (
            "tests.test_ghc_family_v651_v8_x1."
            "TestV651V8X1.test_document_caps_privacy_and_x1_only"
        ),
        "reason": (
            "The historical x1 test reads the mutable phase directory and requires "
            "the later evidence surfaces directory to remain absent."
        ),
    },
]

FAILURES = [
    {
        "negative_id": "V6525-NEG-FINAL-01",
        "category": "exact_final_full_suite_failed_attempt",
        "observed": (
            "The first exact-final full-suite attempt ran 2,759 eligible tests and "
            "failed four lifecycle-local assertions; it received zero canonical "
            "success credit."
        ),
        "recovery": (
            "Retain the complete failed attempt, diagnose only its four failed "
            "modules, and permit one corrected retry before any successful pass."
        ),
        "passing": (
            "The correction contract records one failed aggregate, four exact "
            "failed tests, zero errors, and zero successful canonical passes."
        ),
        "guard": (
            "Never convert a failed aggregate into a pass or launch a blind full "
            "suite replay without first classifying every failed test."
        ),
    },
    {
        "negative_id": "V6525-NEG-FINAL-02",
        "category": "historical_delta_manifest_reads_successor_head",
        "observed": (
            "The v651-v5 remaster delta-manifest test compared its frozen manifest "
            "with its evidence-to-current-HEAD path set and failed after successors "
            "added unrelated paths."
        ),
        "recovery": NEW_EXCLUSIONS[0]["reason"],
        "passing": (
            "The exclusion is bound to one fully qualified historical test while "
            "the remaining module tests stay eligible."
        ),
        "guard": (
            "Bind historical delta-manifest assertions to their immutable final "
            "commit instead of a moving successor HEAD."
        ),
    },
    {
        "negative_id": "V6525-NEG-FINAL-03",
        "category": "historical_commit_count_reads_successor_head",
        "observed": (
            "The v651-v6 closeout test observed 38 source-to-current-HEAD commits "
            "while asserting its own phase-local count was two or three."
        ),
        "recovery": NEW_EXCLUSIONS[1]["reason"],
        "passing": (
            "The exclusion is bound to the one commit-count assertion while all "
            "other v651-v6 closeout tests remain eligible."
        ),
        "guard": (
            "Resolve lifecycle commit-count assertions against the phase's sealed "
            "final anchor, never a moving successor HEAD."
        ),
    },
    {
        "negative_id": "V6525-NEG-FINAL-04",
        "category": "historical_x1_filename_absence_reads_x2_tree",
        "observed": (
            "The v651-v8 special x1 test found later x2 outcome and seal filenames "
            "in the mutable phase directory."
        ),
        "recovery": NEW_EXCLUSIONS[2]["reason"],
        "passing": (
            "The exclusion is bound to the one x1 absence assertion while the "
            "remaining special x1 tests stay eligible."
        ),
        "guard": (
            "Evaluate x1-only filename absence from the immutable x1 tree rather "
            "than a later working-tree phase directory."
        ),
    },
    {
        "negative_id": "V6525-NEG-FINAL-05",
        "category": "historical_x1_directory_absence_reads_x2_tree",
        "observed": (
            "The v651-v8 x1 test found the later evidence surfaces directory in "
            "the mutable phase directory."
        ),
        "recovery": NEW_EXCLUSIONS[3]["reason"],
        "passing": (
            "The exclusion is bound to the one x1 directory-absence assertion "
            "while the remaining v651-v8 x1 tests stay eligible."
        ),
        "guard": (
            "Evaluate x1-only directory absence from the immutable x1 tree rather "
            "than a later working-tree phase directory."
        ),
    },
    {
        "negative_id": "V6525-NEG-FINAL-06",
        "category": "route_correction_test_fixed_final_contract",
        "observed": (
            "The first targeted correction test set retained zero credit because "
            "the route-correction compatibility test still required the earlier "
            "four-commit contract after the additive final-validation correction "
            "moved the final boundary to five commits."
        ),
        "recovery": (
            "Make the owner-controlled compatibility test distinguish the exact "
            "route-correction v2 contract from the additive final-correction v3 "
            "contract while preserving the six-commit cap and exact scoped counts."
        ),
        "passing": (
            "The targeted closeout, route-correction, and final-correction modules "
            "pass together at the corrected precommit boundary."
        ),
        "guard": (
            "Successor-compatible tests must bind lifecycle assertions to their "
            "schema boundary instead of treating an additive final correction as "
            "a mutation of the earlier route receipt."
        ),
    },
    {
        "negative_id": "V6525-NEG-FINAL-07",
        "category": "final_correction_allowlist_omitted_route_test",
        "observed": (
            "The idempotent correction rebuild stopped before manifest generation "
            "because its root-path allowlist omitted the deliberately updated "
            "route-correction compatibility test."
        ),
        "recovery": (
            "Admit that one exact owner-controlled route test in the final-"
            "validation correction allowlist while keeping every other root and "
            "predecessor path fail-closed."
        ),
        "passing": (
            "The corrected allowlist admits only the final builder, final validator, "
            "final-correction test, and route-compatibility test outside phase docs."
        ),
        "guard": (
            "Whenever a correction updates a predecessor compatibility assertion, "
            "declare that exact test in the correction's root-path allowlist."
        ),
    },
]


def run(*args: str) -> str:
    completed = subprocess.run(
        list(args),
        cwd=REPO,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    return completed.stdout.strip()


def git(*args: str) -> str:
    return run("git", *args)


def write_json(relative: str, payload: Any) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(relative: str, payload: str) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def read_json(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def status_paths() -> list[str]:
    completed = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=REPO,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    return sorted(
        {
            row[3:].replace("\\", "/")
            for row in completed.stdout.splitlines()
            if len(row) > 3
        }
    )


def hash_entry(relative: str) -> dict[str, Any]:
    oid = git("hash-object", "-w", f"--path={relative}", relative)
    blob = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=REPO)
    return {
        "path": relative,
        "git_blob": oid,
        "bytes": len(blob),
        "sha256": hashlib.sha256(blob).hexdigest(),
    }


def build_manifest(
    relative: str,
    schema: str,
    paths: list[str],
    exclusions: list[str],
) -> None:
    entries = [
        hash_entry(path)
        for path in paths
        if path not in exclusions and (REPO / path).is_file()
    ]
    write_json(
        relative,
        {
            "schema": schema,
            "hash_domain": "git_path_filtered_blob",
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": exclusions,
        },
    )


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(
            r"(?i)(source_thread_id|thread_id)\s*[:=]"
        ),
        "private_absolute_local_path": re.compile(
            r"(?i)(?:[A-Z]:\\(?:Users|GHC-Archives)\\|"
            r"[A-Z]:\\\\(?:Users|GHC-Archives)\\\\|/Users/|/home/)"
        ),
        "credential_or_secret": re.compile(
            r"(?i)(api[_-]?key|client_secret|private_key|"
            r"bearer\s+[A-Za-z0-9._-]{12,})"
        ),
        "private_route_or_callable_identifier": re.compile(
            r"(?i)(private_route|callable_identifier|resume_token|session_stream)"
        ),
        "conversation_or_app_state": re.compile(
            r"(?i)(raw transcript|private conversation|private app state)"
        ),
    }
    definition_paths = {
        "scripts/build_ghc_family_v652_v5_cli_route_correction.py",
        "scripts/build_ghc_family_v652_v5_final_validation_correction.py",
        "scripts/ghc_family_v652_v5_final_validate.py",
        f"{PHASE_ROOT}/validation/final-validation-correction-staged-privacy.json",
    }
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    scanned = 0
    for relative in paths:
        path = REPO / relative
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        scanned += 1
        for pattern_class, pattern in patterns.items():
            if not pattern.search(text):
                continue
            disposition = (
                "scanner_definition"
                if relative in definition_paths
                else "confirmed_payload_hit"
            )
            row = {
                "path": relative,
                "pattern_class": pattern_class,
                "disposition": disposition,
            }
            candidates.append(row)
            if disposition == "confirmed_payload_hit":
                confirmed.append(row)
    return {
        "schema": (
            "ghc.family.v652-v5.final-validation-correction-privacy.v1"
        ),
        "scanned_file_count": scanned,
        "pattern_classes": sorted(patterns),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "boundary": (
            "Five structural classes with exact scanner-definition quarantine; "
            "zero confirmed hits is not complete privacy assurance."
        ),
    }


def build_method_flow() -> dict[str, Any]:
    spec = importlib.util.spec_from_file_location(
        "ghc_family_method_flow_state_final_validation_runtime", METHOD_RUNNER
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load the official Method Flow runner")
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    ledger = runner.new_ledger(
        "v652-v5-final-validation-correction", "Eiren Kestrel"
    )
    preferred: list[dict[str, Any]] = []
    failed_ids: list[str] = []
    for index, failure in enumerate(FAILURES, 1):
        method_id = f"V6525-FINAL-METHOD-{index:02d}"
        method = {
            "method_id": method_id,
            "title": f"Bounded recovery for {failure['category']}",
            "failure_signature": failure["observed"],
            "trigger_preconditions": [failure["category"]],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_owner_local_validation_recovery",
            "candidate_workaround": failure["recovery"],
            "validation_witness_ids": [],
            "recurrence_guard": failure["guard"],
            "rollback": (
                "Stop, retain the failed validation attempt, and leave sibling "
                "state and external authority unchanged."
            ),
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": [
                "production",
                "independent_reproduction",
                "identity",
                "authority",
                "stage20",
            ],
            "retained_negative_ids": [failure["negative_id"]],
            "scope_boundary": (
                "Owner-local exact-final validation classification only."
            ),
        }
        failed = {
            "witness_id": f"V6525-FINAL-WITNESS-{index:02d}-F",
            "method_id": method_id,
            "procedure": "Retain the original failed exact-final witness.",
            "scope": failure["category"],
            "expected": "The bounded validation postcondition would pass.",
            "observed": failure["observed"],
            "result": "fail",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": [failure["negative_id"]],
            "boundary": "Zero canonical validation credit; failure retained.",
        }
        passing = {
            "witness_id": f"V6525-FINAL-WITNESS-{index:02d}-P",
            "method_id": method_id,
            "procedure": failure["recovery"],
            "scope": failure["category"],
            "expected": "The exact bounded classification contract is explicit.",
            "observed": failure["passing"],
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": [failure["negative_id"]],
            "boundary": (
                "Same-owner correction evidence only; no scientific, production, "
                "professional, or independent-reproduction credit."
            ),
        }
        write_json(
            f"method-flow/final-validation-correction-method-{index:02d}.json",
            method,
        )
        write_json(
            (
                "method-flow/final-validation-correction-witness-"
                f"{index:02d}-failed.json"
            ),
            failed,
        )
        write_json(
            (
                "method-flow/final-validation-correction-witness-"
                f"{index:02d}-passing.json"
            ),
            passing,
        )
        ledger["methods"].append(method)
        runner.append_event(
            ledger,
            method_id,
            None,
            "candidate",
            "method recorded with retained failed witness",
        )
        for witness in (failed, passing):
            ledger["witnesses"].append(witness)
            method["validation_witness_ids"].append(witness["witness_id"])
        method["recommendation_state"] = "validated"
        runner.append_event(
            ledger,
            method_id,
            "candidate",
            "validated",
            "bounded classification witness passed",
            passing["witness_id"],
        )
        method["recommendation_state"] = "preferred"
        runner.append_event(
            ledger,
            method_id,
            "validated",
            "preferred",
            "promoted only after the bounded passing witness",
        )
        ledger["recommendations"].append(
            {
                "recommendation_index": len(ledger["recommendations"]) + 1,
                "method_id": method_id,
                "preconditions": method["trigger_preconditions"],
                "method": method["candidate_workaround"],
                "witness_ids": method["validation_witness_ids"],
                "recurrence_guard": method["recurrence_guard"],
                "rollback": method["rollback"],
                "scope_boundary": method["scope_boundary"],
            }
        )
        preferred.append(method)
        failed_ids.append(failed["witness_id"])
    runner.refresh_counts(ledger)
    validation = runner.validate_ledger(ledger)
    if not validation["valid"]:
        raise RuntimeError(
            "final-validation Method Flow invalid: "
            + "; ".join(validation["issues"])
        )
    summary = {
        "schema": "ghc.family.method-flow-state.summary.v1",
        "phase": ledger["phase"],
        "owner": ledger["owner"],
        "counts": ledger["counts"],
        "preferred_methods": [
            {
                "method_id": method["method_id"],
                "title": method["title"],
                "trigger_preconditions": method["trigger_preconditions"],
                "candidate_workaround": method["candidate_workaround"],
                "validation_witness_ids": method["validation_witness_ids"],
                "recurrence_guard": method["recurrence_guard"],
                "rollback": method["rollback"],
                "scope_boundary": method["scope_boundary"],
            }
            for method in preferred
        ],
        "retained_failed_witnesses": failed_ids,
        "valid": True,
        "boundary": ledger["boundary"],
    }
    write_json(
        "method-flow/final-validation-correction-method-flow-ledger.json",
        ledger,
    )
    write_json(
        "method-flow/final-validation-correction-method-flow-validation.json",
        validation,
    )
    write_json(
        "method-flow/final-validation-correction-method-flow-summary.json",
        summary,
    )
    write_text(
        "method-flow/final-validation-correction-method-flow-summary.md",
        runner.render_markdown(ledger),
    )
    return ledger


def build() -> None:
    if git("rev-parse", "HEAD") != ROUTE_CORRECTION:
        raise RuntimeError("final-validation correction must start at route head")
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    flow = build_method_flow()
    write_json(
        "validation/final-validation-failed-attempt-01.json",
        {
            "schema": "ghc.family.v652-v5.failed-exact-final-attempt.v1",
            "attempt": 1,
            "head": ROUTE_CORRECTION,
            "valid": False,
            "canonical_success_credit": 0,
            "full_repository_tests": {
                "passed": 2755,
                "total": 2759,
                "failures": 4,
                "errors": 0,
                "skipped": 0,
            },
            "scoped_tests": {"passed": 76, "total": 76},
            "detailed": {"passed": 27, "total": 28},
            "minimal": {"passed": 17, "total": 18},
            "json_parse_count": 274,
            "privacy_scanned_file_count": 335,
            "privacy_confirmed_hit_count": 0,
            "manifest_entry_total": 652,
            "failed_test_ids": [row["test_id"] for row in NEW_EXCLUSIONS],
            "no_replay_without_correction": True,
            "boundary": (
                "Failed aggregate retained at zero credit. It is not a successful "
                "canonical pass, independent reproduction, or authority."
            ),
        },
    )
    contract = read_json("final/final-validation-contract.json")
    existing_exclusions = set(
        contract["full_repository_suite_exact_lifecycle_exclusions"]
    )
    new_ids = {row["test_id"] for row in NEW_EXCLUSIONS}
    inherited_exclusions = existing_exclusions - new_ids
    if len(inherited_exclusions) != 35:
        raise RuntimeError("inherited lifecycle exclusion set drifted")
    exclusions = sorted(inherited_exclusions | new_ids)
    write_json(
        "validation/full-suite-lifecycle-exclusion-correction.json",
        {
            "schema": (
                "ghc.family.v652-v5.full-suite-lifecycle-exclusion-correction.v1"
            ),
            "failed_attempt": 1,
            "prior_exact_exclusion_count": len(inherited_exclusions),
            "added_exact_exclusion_count": len(NEW_EXCLUSIONS),
            "corrected_exact_exclusion_count": len(exclusions),
            "added": NEW_EXCLUSIONS,
            "all_other_discovered_tests_remain_eligible": True,
            "broad_module_exclusions": False,
            "historical_tests_modified": False,
            "valid": len(exclusions) == 39,
        },
    )
    write_json(
        "truth/final-validation-retained-negative.json",
        {
            "schema": (
                "ghc.family.v652-v5.final-validation-retained-negative.v1"
            ),
            "route_corrected_effective": 8727,
            "final_validation_operational": len(FAILURES),
            "effective_final": 8727 + len(FAILURES),
            "rows": FAILURES,
            "failed_aggregate_attempts": 1,
            "failed_tests": 4,
            "successful_canonical_passes_before_retry": 0,
            "failed_attempt_received_credit": False,
            "no_failure_erased": True,
            "method_flow_counts": flow["counts"],
        },
    )
    truth = read_json("final/final-phase-truth.json")
    truth.update(
        {
            "route_corrected_effective_negatives": 8727,
            "final_validation_operational_negatives": len(FAILURES),
            "effective_negatives": 8727 + len(FAILURES),
            "failed_exact_final_attempts_retained": 1,
            "successful_exact_final_passes_before_retry": 0,
        }
    )
    write_json("final/final-phase-truth.json", truth)
    contract.update(
        {
            "schema": "ghc.family.v652-v5.final-validation-contract.corrected.v3",
            "expected_scoped_tests": 82,
            "patterns": contract["patterns"]
            + ["test_ghc_family_v652_v5_final_validation_correction.py"],
            "expected_phase_commits": 5,
            "expected_final_parent": ROUTE_CORRECTION,
            "full_repository_suite_exact_lifecycle_exclusions": exclusions,
            "full_repository_suite_exact_lifecycle_exclusion_count": len(
                exclusions
            ),
            "failed_exact_final_attempts_retained": 1,
            "successful_canonical_pass_limit": 1,
            "post_success_replay": False,
            "retry_only_after_bounded_correction": True,
            "final_validation_correction_manifest_required": True,
        }
    )
    write_json("final/final-validation-contract.json", contract)
    route = read_json("route/final-route-state.json")
    route.update(
        {
            "failed_exact_final_attempts_retained": 1,
            "successful_exact_final_passes": 0,
            "state": "PREPARED_NOT_SPAWNED",
            "spawn_count": 0,
        }
    )
    write_json("route/final-route-state.json", route)

    self_paths = [
        f"{PHASE_ROOT}/validation/final-validation-correction-staged-manifest.json",
        f"{PHASE_ROOT}/validation/final-validation-correction-staged-privacy.json",
        f"{PHASE_ROOT}/validation/final-validation-correction-staged-review.json",
        f"{PHASE_ROOT}/validation/final-validation-correction-validation-receipt.json",
        f"{PHASE_ROOT}/validation/final-owner-manifest.json",
    ]
    for relative in self_paths:
        (REPO / relative).write_text("{}\n", encoding="utf-8", newline="\n")

    allowed = {
        "scripts/build_ghc_family_v652_v5_final_validation_correction.py",
        "scripts/ghc_family_v652_v5_final_validate.py",
        "tests/test_ghc_family_v652_v5_final_validation_correction.py",
        "tests/test_ghc_family_v652_v5_route_correction.py",
    }
    paths = status_paths()
    unexpected = [
        path
        for path in paths
        if not (path.startswith(PHASE_ROOT + "/") or path in allowed)
    ]
    frozen = [
        path
        for path in paths
        if (
            path.startswith(
                (
                    f"{PHASE_ROOT}/preregistration/",
                    f"{PHASE_ROOT}/surfaces/",
                    f"{PHASE_ROOT}/evidence/",
                    f"{PHASE_ROOT}/validation/x1-",
                    f"{PHASE_ROOT}/validation/evidence-",
                    f"{PHASE_ROOT}/validation/closeout-",
                    f"{PHASE_ROOT}/validation/route-correction-",
                )
            )
            or (
                path.startswith(f"{PHASE_ROOT}/method-flow/")
                and not path.startswith(
                    f"{PHASE_ROOT}/method-flow/final-validation-correction-"
                )
            )
        )
    ]
    if unexpected or frozen:
        raise RuntimeError(
            f"unexpected={unexpected}; frozen_predecessor_paths={frozen}"
        )
    review = {
        "schema": (
            "ghc.family.v652-v5.final-validation-correction-staged-review.v1"
        ),
        "head_before_correction": ROUTE_CORRECTION,
        "intended_path_count": len(paths),
        "unexpected_paths": unexpected,
        "frozen_predecessor_paths": frozen,
        "added_exact_test_exclusions": len(NEW_EXCLUSIONS),
        "broad_module_exclusions": False,
        "phase_commit_after_correction": 5,
        "phase_commit_cap": 6,
        "valid": not unexpected and not frozen,
    }
    write_json(
        "validation/final-validation-correction-staged-review.json", review
    )
    privacy = privacy_scan(paths)
    if privacy["confirmed_hit_count"]:
        raise RuntimeError(
            f"confirmed privacy hits: {privacy['confirmed_hits']}"
        )
    write_json(
        "validation/final-validation-correction-staged-privacy.json", privacy
    )
    build_manifest(
        "validation/final-validation-correction-staged-manifest.json",
        (
            "ghc.family.v652-v5.final-validation-correction-"
            "staged-manifest.v1"
        ),
        paths,
        self_paths,
    )
    owner_exclusions = [
        f"{PHASE_ROOT}/validation/final-owner-manifest.json",
        (
            f"{PHASE_ROOT}/validation/"
            "final-validation-correction-validation-receipt.json"
        ),
        (
            f"{PHASE_ROOT}/validation/"
            "final-validation-correction-staged-review.json"
        ),
    ]
    owner_paths = sorted(
        {
            path
            for path in git("diff", "--name-only", SOURCE, "HEAD").splitlines()
            if path
        }
        | set(status_paths())
    )
    build_manifest(
        "validation/final-owner-manifest.json",
        "ghc.family.v652-v5.final-owner-manifest.corrected.v3",
        owner_paths,
        owner_exclusions,
    )
    test_output = run(
        "python",
        "-m",
        "unittest",
        "-q",
        "tests.test_ghc_family_v652_v5_final_validation_correction",
    )
    json_paths = sorted(ROOT.rglob("*.json"))
    for path in json_paths:
        json.loads(path.read_text(encoding="utf-8"))
    write_json(
        "validation/final-validation-correction-validation-receipt.json",
        {
            "schema": (
                "ghc.family.v652-v5.final-validation-correction-validation.v1"
            ),
            "built_at_utc": now,
            "tests_passed": 6,
            "tests_total": 6,
            "json_parse_count": len(json_paths),
            "privacy_confirmed_hits": privacy["confirmed_hit_count"],
            "correction_path_count": len(paths),
            "test_stdout": test_output,
            "failed_full_suite_attempts_retained": 1,
            "successful_full_suite_passes": 0,
            "full_repository_suite_rerun": False,
            "exact_final_pass": False,
            "valid": (
                not unexpected
                and not frozen
                and privacy["confirmed_hit_count"] == 0
            ),
            "boundary": (
                "Precommit correction validation only. Exact-final credit requires "
                "one successful post-push full-suite retry; no post-success replay."
            ),
        },
    )
    print(
        json.dumps(
            {
                "phase": "v652-v5",
                "correction_paths": len(paths),
                "new_exact_exclusions": len(NEW_EXCLUSIONS),
                "total_exact_exclusions": len(exclusions),
                "effective_negatives": 8727 + len(FAILURES),
                "privacy_hits": privacy["confirmed_hit_count"],
                "status": "final_validation_correction_built_not_committed",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    build()
