#!/usr/bin/env python3
"""Record immutable-x1 archive verification and retained cleanup failures."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
X2 = ROOT / "docs" / "caelen-ash" / "v672-v4" / "x2"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value):
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> None:
    additions = [
        {
            "method_id": "CA6724-RECOVERY-METHOD-005",
            "failure_id": "CA6724-X2-024",
            "trigger": "the host rejected a combined immutable-archive verification and recursive-cleanup wrapper before launch",
            "preferred_method": "separate read-only archive verification from independently guarded cleanup",
            "failure": "combined wrapper received zero verification and cleanup credit",
            "passing": None,
        },
        {
            "method_id": "CA6724-RECOVERY-METHOD-006",
            "failure_id": "CA6724-X2-025",
            "trigger": "the first Git archive selection named an untracked tests package initializer",
            "preferred_method": "archive only the tracked x1 packet, builder, and x1 test module",
            "failure": "the first archive selection failed before extraction",
            "passing": "the corrected exact-x1 archive ran all sixteen x1 tests successfully",
        },
        {
            "method_id": "CA6724-RECOVERY-METHOD-007",
            "failure_id": "CA6724-X2-026",
            "trigger": "the host rejected recursive removal of the resolved D-drive verification target before launch",
            "preferred_method": "remove verified descendants individually and retain any blocked binary residual",
            "failure": "recursive cleanup received zero credit",
            "passing": None,
        },
        {
            "method_id": "CA6724-RECOVERY-METHOD-008",
            "failure_id": "CA6724-X2-027",
            "trigger": "the host also rejected the first enumerated nonrecursive cleanup wrapper before launch",
            "preferred_method": "delete UTF-8 text artifacts with exact patch targets and keep binary cleanup separate",
            "failure": "the enumerated cleanup wrapper received zero credit",
            "passing": "fifteen exact extracted UTF-8 files were removed without touching repository or sibling state",
        },
        {
            "method_id": "CA6724-RECOVERY-METHOD-009",
            "failure_id": "CA6724-X2-028",
            "trigger": "the host rejected exact nonrecursive shell deletion of the two remaining binary files",
            "preferred_method": "retain the bounded D-drive residual rather than bypass host deletion policy",
            "failure": "binary cleanup remained incomplete",
            "passing": None,
        },
        {
            "method_id": "CA6724-RECOVERY-METHOD-010",
            "failure_id": "CA6724-X2-029",
            "trigger": "the patch tool could not decode the Python bytecode as UTF-8 and aborted binary deletion",
            "preferred_method": "retain and disclose the two binary residuals without retry loops",
            "failure": "binary-aware patch cleanup remained incomplete",
            "passing": None,
        },
    ]
    flow_path = X2 / "method-flow" / "ledger.json"
    flow = load(flow_path)
    if any(row.get("method_id") == additions[0]["method_id"] for row in flow["methods"]):
        raise SystemExit("archive recovery already recorded")
    for row in additions:
        flow["methods"].append(
            {
                "method_id": row["method_id"],
                "trigger": row["trigger"],
                "preferred_method": row["preferred_method"],
                "state": "bounded_recovery_or_retained_residual",
                "rollback": "preserve exact x1 and all repository state; do not bypass host deletion policy",
                "sibling_recommendation": "keep archive verification and cleanup independent and use only tracked selections",
            }
        )
        flow["witnesses"].append(
            {
                "witness_id": row["failure_id"] + "-FAIL",
                "method_id": row["method_id"],
                "kind": "failed",
                "credit": 0,
                "description": row["failure"],
                "state": "retained_zero_credit",
            }
        )
        if row["passing"]:
            flow["witnesses"].append(
                {
                    "witness_id": row["failure_id"] + "-PASS",
                    "method_id": row["method_id"],
                    "kind": "passing",
                    "credit": "bounded_archive_or_text_cleanup_only",
                    "description": row["passing"],
                    "state": "bounded_passing_not_original_success",
                }
            )
    flow["current_delta"] = {
        "effective_negatives": 85,
        "failed_witnesses": 85,
        "methods": 46,
        "passing_witnesses": 61,
    }
    flow["effective_counts"].update(
        {
            "effective_negatives": 35416,
            "effective_methods": 21986,
            "effective_failed_witnesses": 7237,
            "effective_passing_witnesses": 9287,
        }
    )
    write(flow_path, flow)

    negatives_path = X2 / "retained-negative-register.json"
    negatives = load(negatives_path)
    negatives["x2_unexpected_operational_failures"] = 29
    negatives["x2_operational_failure_ids"].extend([row["failure_id"] for row in additions])
    negatives["effective_total"] = 35416
    write(negatives_path, negatives)

    truth_path = X2 / "phase-truth.json"
    truth = load(truth_path)
    truth["effective_counts"].update(
        {
            "negatives": 35416,
            "methods": 21986,
            "failed_witnesses": 7237,
            "passing_witnesses": 9287,
        }
    )
    truth["immutable_x1_archive_verification"] = {
        "tests": 16,
        "passed": 16,
        "x1_commit": "0ebc12367f26a7d6cf5cca9466843f2cbaade293",
        "x2_paths_in_archive": 0,
        "runner_smoke_replayed": False,
        "skill_smoke_replayed": False,
    }
    truth["temporary_cleanup_residual"] = {
        "location_class": "bounded_D_drive_temporary_verification_folder",
        "removed_utf8_files": 15,
        "residual_files": ["verification_archive", "python_bytecode_cache"],
        "repository_or_sibling_state_affected": False,
        "host_deletion_policy_bypassed": False,
    }
    write(truth_path, truth)

    write(
        X2 / "immutable-x1-archive-recovery.json",
        {
            "schema": "ghc.family.caelen.v672-v4.immutable-x1-archive-recovery.v1",
            "failed_invocations": 6,
            "failed_invocation_credit": 0,
            "immutable_x1_tests": 16,
            "immutable_x1_passes": 16,
            "text_files_removed": 15,
            "binary_residual_files": 2,
            "residual_location_class": "bounded_D_drive_temporary_verification_folder",
            "repository_state_changed_by_cleanup": False,
            "runner_smoke_replayed": False,
            "skill_smoke_replayed": False,
            "canonical_invocations": 0,
            "canonical_successes": 0,
        },
    )


if __name__ == "__main__":
    main()
