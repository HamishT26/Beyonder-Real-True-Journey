#!/usr/bin/env python3
"""Run Caelen v654-v4's one post-push canonical scoped validation pass."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
ROOT = "docs/caelen-morrow/v654-v4"
BRANCH = "codex/GHC-Family/caelen-morrow-v654-v4-full-tools"
SOURCE = "53354454690c40c5688aaeb86dc46a61ee079fe7"
X1 = "4af17107d0042eb6b41ef17a9b32aebd6eabdc2a"
EVIDENCE = "47746b3b52c02e97ee5c4e66632f7584a2834fca"
ROUTE_STATE = "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED"
EXPECTED_OUTCOMES = {
    "completed": 23,
    "represented": 5,
    "open_gap": 1,
    "exact_gate": 1,
}
TEST_MODULES = [
    "tests.test_ghc_family_v654_v4_x1",
    "tests.test_ghc_family_v654_v4",
    "tests.test_ghc_family_v654_v4_closeout",
    "tests.test_ghc_family_v654_v3_x1",
    "tests.test_ghc_family_v654_v3",
    "tests.test_ghc_family_v654_v3_closeout",
]
FINAL_SELF_EXCLUSIONS = {
    f"{ROOT}/validation/final-delta-manifest.json",
    f"{ROOT}/validation/final-owner-manifest.json",
    f"{ROOT}/validation/final-staged-privacy.json",
    f"{ROOT}/validation/final-staged-review.json",
    f"{ROOT}/validation/final-diff-hygiene.json",
}
RUNNER_PATHS = {
    "scripts/ghc_family_accessible_garment_audit.py",
    "scripts/ghc_family_freed_id_garment_profiles.py",
    "scripts/ghc_family_garment_compatibility_refusal.py",
    "scripts/ghc_family_garment_hazard_boards.py",
    "scripts/ghc_family_garment_intake_ledger.py",
    "scripts/ghc_family_garment_notice_quarantine.py",
    "scripts/ghc_family_gmut_textile_fields.py",
    "scripts/ghc_family_thos_garment_proxy.py",
}
PHASE_SCRIPT_PATHS = {
    "scripts/ghc_family_v654_v4_phase_data.py",
    "scripts/ghc_family_v654_v4_x2_data.py",
    "scripts/ghc_family_v654_v4_core.py",
    "scripts/build_ghc_family_v654_v4_method_flow.py",
    "scripts/build_ghc_family_v654_v4_preregistration.py",
    "scripts/ghc_family_v654_v4_x1_validate.py",
    "scripts/build_ghc_family_v654_v4_x2_method_flow.py",
    "scripts/build_ghc_family_v654_v4_evidence.py",
    "scripts/ghc_family_v654_v4_evidence_validate.py",
    "scripts/ghc_family_v654_v4_detailed_validator.py",
    "scripts/ghc_family_v654_v4_bounded_suite.py",
    "scripts/build_ghc_family_v654_v4_closeout.py",
    "scripts/ghc_family_v654_v4_final_staged_review.py",
    "scripts/ghc_family_v654_v4_final_validate.py",
}
PHASE_TEST_PATHS = {
    "tests/test_ghc_family_v654_v4_x1.py",
    "tests/test_ghc_family_v654_v4.py",
    "tests/test_ghc_family_v654_v4_closeout.py",
}
ALLOWED_NON_DOC_PATHS = RUNNER_PATHS | PHASE_SCRIPT_PATHS | PHASE_TEST_PATHS


def git(*args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=check,
    )
    return result.stdout.strip()


def git_bytes(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=REPO)


def load_at(anchor: str, relative: str) -> Any:
    return json.loads(git("show", f"{anchor}:{relative}"))


def blob_at(anchor: str, relative: str) -> bytes:
    oid = git("rev-parse", f"{anchor}:{relative}")
    return git_bytes("cat-file", "blob", oid)


def owner_path(relative: str) -> bool:
    return relative.startswith(f"{ROOT}/") or relative in ALLOWED_NON_DOC_PATHS


def tree_paths(anchor: str) -> list[str]:
    return sorted(
        path
        for path in git("ls-tree", "-r", "--name-only", anchor).splitlines()
        if path
    )


def replay_manifest(anchor: str, relative: str) -> dict[str, Any]:
    manifest = load_at(anchor, relative)
    mismatches = []
    for row in manifest["entries"]:
        observed = git("rev-parse", f"{anchor}:{row['path']}", check=False)
        if observed != row["git_blob"]:
            mismatches.append(
                {
                    "path": row["path"],
                    "expected": row["git_blob"],
                    "observed": observed or None,
                }
            )
            continue
        blob = git_bytes("cat-file", "blob", observed)
        digest = hashlib.sha256(blob).hexdigest()
        if len(blob) != row["bytes"] or digest != row["sha256"]:
            mismatches.append(
                {
                    "path": row["path"],
                    "reason": "bytes_or_sha256",
                    "expected_bytes": row["bytes"],
                    "observed_bytes": len(blob),
                    "expected_sha256": row["sha256"],
                    "observed_sha256": digest,
                }
            )
    return {
        "path": relative,
        "entries": len(manifest["entries"]),
        "declared_entries": manifest["entry_count"],
        "self_exclusions": manifest.get("self_exclusions", []),
        "mismatches": mismatches,
        "valid": manifest["entry_count"] == len(manifest["entries"])
        and not mismatches,
    }


def privacy_scan(anchor: str, paths: list[str]) -> dict[str, Any]:
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
            r"(?i)(session_stream|raw_transcript|conversation_export)"
        ),
    }
    candidates = []
    confirmed = []
    scanned = 0
    for relative in paths:
        try:
            content = blob_at(anchor, relative).decode("utf-8")
        except (UnicodeDecodeError, subprocess.CalledProcessError):
            continue
        scanned += 1
        is_definition = (
            relative.endswith("_validate.py")
            or relative.endswith("_staged_review.py")
            or relative.endswith("-privacy.json")
            or relative == "scripts/build_ghc_family_v654_v4_preregistration.py"
        )
        for pattern_class, pattern in patterns.items():
            if pattern.search(content):
                disposition = (
                    "scanner_definition" if is_definition else "confirmed_payload_hit"
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
        "scanned_file_count": scanned,
        "pattern_classes": sorted(patterns),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "boundary": (
            "Five structural classes with scanner-definition quarantine; zero "
            "confirmed hits is not complete privacy assurance."
        ),
    }


def parse_owner_json(anchor: str, paths: list[str]) -> dict[str, Any]:
    json_paths = [path for path in paths if path.endswith(".json")]
    failures = []
    for relative in json_paths:
        try:
            json.loads(blob_at(anchor, relative).decode("utf-8"))
        except Exception as exc:
            failures.append({"path": relative, "error": type(exc).__name__})
    return {
        "count": len(json_paths),
        "failures": failures,
        "valid": not failures,
    }


def run_scoped_tests() -> dict[str, Any]:
    env = os.environ.copy()
    env.update(
        {
            "PYTHONUTF8": "1",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    result = subprocess.run(
        [sys.executable, "-m", "unittest", *TEST_MODULES],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )
    combined = "\n".join(part for part in (result.stdout, result.stderr) if part)
    match = re.search(r"Ran\s+(\d+)\s+tests?", combined)
    return {
        "modules": TEST_MODULES,
        "module_count": len(TEST_MODULES),
        "test_count": int(match.group(1)) if match else None,
        "returncode": result.returncode,
        "passed": result.returncode == 0,
        "output_tail": "\n".join(combined.splitlines()[-8:]),
        "full_repository_suite_run": False,
        "boundary": (
            "Dependency-justified current-phase and direct-parent modules only; "
            "not Eiren's complete repository suite."
        ),
    }


def parent_count(anchor: str) -> int:
    parents = git("show", "-s", "--format=%P", anchor).split()
    return len(parents)


def write_receipt(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--external-receipt", required=True)
    args = parser.parse_args()
    expected_head = args.expected_head
    receipt_path = Path(args.external_receipt).resolve()

    existing: dict[str, Any] = {}
    if receipt_path.exists():
        existing = json.loads(receipt_path.read_text(encoding="utf-8"))
        if existing.get("canonical_success_count", 0) >= 1:
            raise SystemExit(
                "canonical success already recorded; replay is prohibited"
            )
    attempts = list(existing.get("attempts", []))
    attempt_number = len(attempts) + 1
    started = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    checks: list[dict[str, Any]] = []

    def check(name: str, passed: bool, observed: Any) -> None:
        checks.append({"name": name, "passed": bool(passed), "observed": observed})

    try:
        head = git("rev-parse", "HEAD")
        branch = git("branch", "--show-current")
        status = git("status", "--porcelain=v1", "--untracked-files=all")
        upstream = git("rev-parse", "@{upstream}")
        tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}")
        live_row = git("ls-remote", "origin", f"refs/heads/{BRANCH}")
        fresh_live = live_row.split()[0] if live_row else None
        divergence = git("rev-list", "--left-right", "--count", "HEAD...@{upstream}")

        check("exact_head", head == expected_head, head)
        check("exact_branch", branch == BRANCH, branch)
        check("clean_state", status == "", status.splitlines())
        check(
            "four_way_equality",
            len({head, upstream, tracking, fresh_live}) == 1,
            {
                "local": head,
                "upstream": upstream,
                "tracking": tracking,
                "fresh_live": fresh_live,
            },
        )
        check("zero_divergence", divergence == "0\t0", divergence)

        source_parent = git("rev-parse", f"{X1}^")
        x1_parent = source_parent
        evidence_parent = git("rev-parse", f"{EVIDENCE}^")
        final_parent = git("rev-parse", "HEAD^")
        phase_count = int(git("rev-list", "--count", f"{SOURCE}..HEAD"))
        merges = [
            row
            for row in git("rev-list", "--merges", f"{SOURCE}..HEAD").splitlines()
            if row
        ]
        check("source_to_x1", x1_parent == SOURCE, x1_parent)
        check("x1_to_evidence", evidence_parent == X1, evidence_parent)
        check("evidence_to_final", final_parent == EVIDENCE, final_parent)
        check(
            "single_parent_chain",
            parent_count(X1) == parent_count(EVIDENCE) == parent_count(head) == 1,
            {
                "x1": parent_count(X1),
                "evidence": parent_count(EVIDENCE),
                "final": parent_count(head),
            },
        )
        check("phase_commit_count", phase_count == 3, phase_count)
        check("zero_merges", not merges, merges)

        source_owner = replay_manifest(
            SOURCE,
            "docs/sylven-arc/v654-v3/validation/final-owner-manifest.json",
        )
        x1_manifest = replay_manifest(
            X1, f"{ROOT}/validation/x1-staged-manifest.json"
        )
        evidence_manifest = replay_manifest(
            EVIDENCE, f"{ROOT}/validation/evidence-manifest.json"
        )
        delta_manifest = replay_manifest(
            head, f"{ROOT}/validation/final-delta-manifest.json"
        )
        owner_manifest = replay_manifest(
            head, f"{ROOT}/validation/final-owner-manifest.json"
        )
        check(
            "source_owner_manifest",
            source_owner["valid"] and source_owner["entries"] == 392,
            source_owner,
        )
        check(
            "x1_manifest",
            x1_manifest["valid"] and x1_manifest["entries"] == 92,
            x1_manifest,
        )
        check(
            "evidence_manifest",
            evidence_manifest["valid"] and evidence_manifest["entries"] == 179,
            evidence_manifest,
        )
        check("final_delta_manifest", delta_manifest["valid"], delta_manifest)
        check("final_owner_manifest", owner_manifest["valid"], owner_manifest)

        final_tree = tree_paths(head)
        owner_paths = sorted(path for path in final_tree if owner_path(path))
        expected_owner_manifest_paths = sorted(
            path for path in owner_paths if path not in FINAL_SELF_EXCLUSIONS
        )
        declared_owner_paths = sorted(
            row["path"]
            for row in load_at(
                head, f"{ROOT}/validation/final-owner-manifest.json"
            )["entries"]
        )
        check(
            "owner_manifest_coverage",
            expected_owner_manifest_paths == declared_owner_paths
            and FINAL_SELF_EXCLUSIONS <= set(owner_paths),
            {
                "owner_paths": len(owner_paths),
                "declared": len(declared_owner_paths),
                "missing": sorted(
                    set(expected_owner_manifest_paths) - set(declared_owner_paths)
                ),
                "extra": sorted(
                    set(declared_owner_paths) - set(expected_owner_manifest_paths)
                ),
            },
        )

        final_changed = sorted(
            path
            for path in git(
                "diff-tree",
                "--no-commit-id",
                "--name-only",
                "-r",
                head,
            ).splitlines()
            if path
        )
        expected_delta_paths = sorted(
            path for path in final_changed if path not in FINAL_SELF_EXCLUSIONS
        )
        declared_delta_paths = sorted(
            row["path"]
            for row in load_at(
                head, f"{ROOT}/validation/final-delta-manifest.json"
            )["entries"]
        )
        check(
            "delta_manifest_coverage",
            expected_delta_paths == declared_delta_paths
            and FINAL_SELF_EXCLUSIONS <= set(final_changed),
            {
                "changed": len(final_changed),
                "declared": len(declared_delta_paths),
                "missing": sorted(set(expected_delta_paths) - set(declared_delta_paths)),
                "extra": sorted(set(declared_delta_paths) - set(expected_delta_paths)),
            },
        )

        json_parse = parse_owner_json(head, owner_paths)
        check("owner_json_parse", json_parse["valid"], json_parse)
        privacy = privacy_scan(head, owner_paths)
        check("privacy_scan", privacy["confirmed_hit_count"] == 0, privacy)

        truth = load_at(head, f"{ROOT}/final/phase-truth.json")
        negatives = load_at(head, f"{ROOT}/final/retained-negative-register.json")
        gates = load_at(head, f"{ROOT}/final/exact-open-gate-register.json")
        method = load_at(head, f"{ROOT}/method-flow/final-method-flow-ledger.json")
        route = load_at(head, f"{ROOT}/route/terminal-existing-task-baton.json")
        seal = load_at(head, f"{ROOT}/final/seal-receipt.json")
        stale = load_at(head, f"{ROOT}/validation/stale-label-review-final.json")
        staged_review = load_at(head, f"{ROOT}/validation/final-staged-review.json")
        diff_hygiene = load_at(head, f"{ROOT}/validation/final-diff-hygiene.json")
        docs = load_at(head, f"{ROOT}/validation/document-cap-final.json")
        owners = load_at(head, f"{ROOT}/validation/owner-file-threshold-final.json")
        protocol = load_at(head, f"{ROOT}/validation/final-validation-protocol.json")
        method_states = Counter(row["recommendation_state"] for row in method["methods"])
        witnesses = Counter(row["result"] for row in method["witnesses"])
        baton = blob_at(
            head, f"{ROOT}/handoffs/eiren-kestrel-v654-v5-activation.md"
        ).decode("utf-8")
        baton_words = len(baton.split())

        check("outcomes", truth["outcomes"] == EXPECTED_OUTCOMES, truth["outcomes"])
        check(
            "negative_retention",
            negatives["effective_total"] == 11322
            and negatives["inherited_effective"] == 11155
            and negatives["x1_operational_count"] == 14
            and negatives["x2_operational_count"] == 0
            and negatives["closeout_operational_count"] == 3
            and negatives["synthetic_mutation_negative_count"] == 150
            and negatives["no_failure_erased"],
            negatives,
        )
        check(
            "open_gaps",
            gates["effective_open_gaps"] == 83
            and gates["open_gap_closed_count"] == 0,
            gates["effective_open_gaps"],
        )
        check(
            "exact_gates",
            gates["effective_exact_gates"] == 82
            and gates["exact_gate_closed_count"] == 0,
            gates["effective_exact_gates"],
        )
        check(
            "method_flow",
            len(method["methods"]) == 59
            and method_states == {"preferred": 59}
            and witnesses == {"fail": 59, "pass": 59},
            {
                "methods": len(method["methods"]),
                "states": dict(method_states),
                "witnesses": dict(witnesses),
            },
        )
        check(
            "route_prepared_not_sent",
            route["state"] == ROUTE_STATE
            and route["recipient_title"] == "Eiren Kestrel"
            and route["existing_task_only"]
            and route["task_created_count"] == 0
            and route["task_contacted_count"] == 0
            and route["message_limit"] == 1,
            route,
        )
        check(
            "no_postcommit_preclaim",
            not seal["successor_task_created"]
            and not seal["successor_task_contacted"]
            and "existing-task message acknowledgement"
            in seal["postcommit_facts_not_preclaimed"],
            seal,
        )
        check(
            "baton",
            10000 <= baton_words <= 100000
            and ROUTE_STATE in baton
            and "Eiren Kestrel" in baton
            and "source_thread_id" not in baton.casefold(),
            baton_words,
        )
        check("stale_labels", stale["valid"] and not stale["matches"], stale)
        check(
            "staged_review",
            staged_review["valid"]
            and not staged_review["canonical_final_pass_run"]
            and staged_review["privacy_confirmed_hit_count"] == 0,
            staged_review,
        )
        check(
            "diff_hygiene",
            diff_hygiene["valid"]
            and not diff_hygiene["out_of_scope_paths"]
            and not diff_hygiene["sibling_document_paths"]
            and not diff_hygiene["x1_document_paths_changed"]
            and not diff_hygiene["evidence_artifact_paths_changed"],
            diff_hygiene,
        )
        check("document_cap", docs["valid"], docs)
        check("owner_file_cap", owners["valid"], owners)
        check(
            "terminal_truth",
            truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
            and truth["real_data_rows"] == 0
            and not truth["independent_team_reproduction"]
            and not truth["full_repository_suite_run"],
            truth["terminal_verdict"],
        )
        check(
            "canonical_protocol",
            protocol["canonical_success_limit"] == 1
            and not protocol["post_success_replay_permitted"]
            and protocol["scoped_test_modules"] == TEST_MODULES,
            protocol,
        )

        tests = run_scoped_tests()
        check("scoped_tests", tests["passed"], tests)

        detailed_names = [
            "exact_head",
            "exact_branch",
            "clean_state",
            "four_way_equality",
            "zero_divergence",
            "source_to_x1",
            "x1_to_evidence",
            "evidence_to_final",
            "single_parent_chain",
            "phase_commit_count",
            "zero_merges",
            "source_owner_manifest",
            "x1_manifest",
            "evidence_manifest",
            "final_delta_manifest",
            "final_owner_manifest",
            "owner_manifest_coverage",
            "delta_manifest_coverage",
            "owner_json_parse",
            "privacy_scan",
            "outcomes",
            "negative_retention",
            "open_gaps",
            "exact_gates",
            "method_flow",
            "route_prepared_not_sent",
            "no_postcommit_preclaim",
            "baton",
            "stale_labels",
            "staged_review",
            "diff_hygiene",
            "document_cap",
            "owner_file_cap",
            "terminal_truth",
            "canonical_protocol",
            "scoped_tests",
        ]
        by_name = {row["name"]: row for row in checks}
        detailed = [by_name[name] for name in detailed_names]
        minimal_names = [
            "exact_head",
            "clean_state",
            "four_way_equality",
            "zero_divergence",
            "evidence_to_final",
            "phase_commit_count",
            "zero_merges",
            "x1_manifest",
            "evidence_manifest",
            "final_delta_manifest",
            "final_owner_manifest",
            "owner_json_parse",
            "privacy_scan",
            "outcomes",
            "negative_retention",
            "open_gaps",
            "exact_gates",
            "method_flow",
            "route_prepared_not_sent",
            "baton",
            "diff_hygiene",
            "owner_file_cap",
            "terminal_truth",
            "scoped_tests",
        ]
        minimal = [by_name[name] for name in minimal_names]
        success = all(row["passed"] for row in checks)
        completed = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        attempt = {
            "attempt_number": attempt_number,
            "started_at_utc": started,
            "completed_at_utc": completed,
            "expected_head": expected_head,
            "observed_head": head,
            "status": "success" if success else "failure",
            "aggregate_credit": 1 if success else 0,
            "checks_passed": sum(row["passed"] for row in checks),
            "checks_total": len(checks),
            "detailed_passed": sum(row["passed"] for row in detailed),
            "detailed_total": len(detailed),
            "minimal_passed": sum(row["passed"] for row in minimal),
            "minimal_total": len(minimal),
            "tests": tests,
            "json_parse": json_parse,
            "privacy": privacy,
            "manifests": {
                "source_owner": source_owner,
                "x1": x1_manifest,
                "evidence": evidence_manifest,
                "final_delta": delta_manifest,
                "final_owner": owner_manifest,
            },
            "history": {
                "source": SOURCE,
                "x1": X1,
                "evidence": EVIDENCE,
                "final": head,
                "phase_commits": phase_count,
                "merges": len(merges),
                "final_parent_count": parent_count(head),
            },
            "four_way": {
                "local": head,
                "upstream": upstream,
                "tracking": tracking,
                "fresh_live": fresh_live,
                "divergence": divergence,
            },
            "route_state": ROUTE_STATE,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "full_repository_suite_run": False,
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": (
                "One dependency-justified same-owner canonical scoped pass; not "
                "independent reproduction, external audit, production assurance, "
                "authority, complete privacy or accessibility, or Stage 20."
            ),
            "checks": checks,
        }
    except Exception as exc:
        success = False
        attempt = {
            "attempt_number": attempt_number,
            "started_at_utc": started,
            "completed_at_utc": datetime.now(timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
            "expected_head": expected_head,
            "status": "failure",
            "aggregate_credit": 0,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "checks": checks,
            "boundary": "Failed or incomplete attempt retained with zero aggregate credit.",
        }

    attempts.append(attempt)
    success_count = sum(row.get("status") == "success" for row in attempts)
    receipt = {
        "schema": "ghc.family.v654-v4.external-canonical-validation.v1",
        "phase": "v654-v4",
        "owner": "Caelen Morrow",
        "branch": BRANCH,
        "canonical_attempt_count": len(attempts),
        "canonical_success_count": success_count,
        "successful_replay_permitted": False,
        "attempts": attempts,
        "latest_status": attempt["status"],
        "terminal_gate_ready_for_exact_existing_eiren_message": success,
        "delivery_state": (
            "PREPARED_NOT_SENT" if success else "BLOCKED_BY_FAILED_VALIDATION"
        ),
        "boundary": (
            "External receipt for bounded same-owner validation only; message "
            "delivery requires a separate acknowledged existing-task call."
        ),
    }
    write_receipt(receipt_path, receipt)
    print(
        json.dumps(
            {
                "attempt": attempt_number,
                "status": attempt["status"],
                "checks": [
                    sum(row["passed"] for row in attempt.get("checks", [])),
                    len(attempt.get("checks", [])),
                ],
                "detailed": [
                    attempt.get("detailed_passed"),
                    attempt.get("detailed_total"),
                ],
                "minimal": [
                    attempt.get("minimal_passed"),
                    attempt.get("minimal_total"),
                ],
                "tests": attempt.get("tests", {}).get("test_count"),
                "json": attempt.get("json_parse", {}).get("count"),
                "privacy_hits": attempt.get("privacy", {}).get(
                    "confirmed_hit_count"
                ),
                "receipt": str(receipt_path),
            },
            sort_keys=True,
        )
    )
    raise SystemExit(0 if success else 1)


if __name__ == "__main__":
    main()
