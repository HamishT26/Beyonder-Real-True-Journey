#!/usr/bin/env python3
"""Record bounded evidence-stage recovery without replaying Caelen x2."""

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
            "method_id": "CA6724-RECOVERY-METHOD-003",
            "failure_id": "CA6724-X2-022",
            "trigger": "the first evidence-stage add encountered twelve generated owner runners outside the sparse definition",
            "preferred_method": "extend the no-cone sparse definition with only the exact Caelen owner runner paths and inspect the partial index",
            "failure": "evidence staging was incomplete and received zero stage credit",
            "passing": "all exact Caelen runner paths became stageable without widening sibling or shared material",
            "recommendation": "predeclare generated owner runner paths in the sparse definition before evidence staging",
        },
        {
            "method_id": "CA6724-RECOVERY-METHOD-004",
            "failure_id": "CA6724-X2-023",
            "trigger": "the first stage review continued over the partial index and lacked a required-path completeness gate",
            "preferred_method": "add an exact required-evidence set, restage the complete owner surface, and regenerate both receipts",
            "failure": "the partial stage review was structurally insufficient despite not mutating x1",
            "passing": "the regenerated review requires every key x2 runner, receipt, test, and evidence ledger",
            "recommendation": "combine allowlist validation with explicit required-path completeness checks",
        },
    ]
    flow_path = X2 / "method-flow" / "ledger.json"
    flow = load(flow_path)
    if any(row.get("method_id") == additions[0]["method_id"] for row in flow["methods"]):
        raise SystemExit("stage recovery already recorded")
    for row in additions:
        flow["methods"].append(
            {
                "method_id": row["method_id"],
                "trigger": row["trigger"],
                "preferred_method": row["preferred_method"],
                "state": "preferred_after_bounded_passing_witness",
                "rollback": "retain the failed stage projection and change only Caelen-owned sparse or review dependencies",
                "sibling_recommendation": row["recommendation"],
            }
        )
        flow["witnesses"].extend(
            [
                {
                    "witness_id": row["failure_id"] + "-FAIL",
                    "method_id": row["method_id"],
                    "kind": "failed",
                    "credit": 0,
                    "description": row["failure"],
                    "state": "retained_zero_credit",
                },
                {
                    "witness_id": row["failure_id"] + "-PASS",
                    "method_id": row["method_id"],
                    "kind": "passing",
                    "credit": "bounded_stage_recovery_only",
                    "description": row["passing"],
                    "state": "bounded_passing_not_original_success",
                },
            ]
        )
    flow["current_delta"] = {
        "effective_negatives": 79,
        "failed_witnesses": 79,
        "methods": 40,
        "passing_witnesses": 59,
    }
    flow["effective_counts"].update(
        {
            "effective_negatives": 35410,
            "effective_methods": 21980,
            "effective_failed_witnesses": 7231,
            "effective_passing_witnesses": 9285,
        }
    )
    write(flow_path, flow)

    negatives_path = X2 / "retained-negative-register.json"
    negatives = load(negatives_path)
    negatives["x2_unexpected_operational_failures"] = 23
    negatives["x2_operational_failure_ids"].extend([row["failure_id"] for row in additions])
    negatives["effective_total"] = 35410
    write(negatives_path, negatives)

    truth_path = X2 / "phase-truth.json"
    truth = load(truth_path)
    truth["effective_counts"].update(
        {
            "negatives": 35410,
            "methods": 21980,
            "failed_witnesses": 7231,
            "passing_witnesses": 9285,
        }
    )
    truth["stage_recovery"] = {
        "retained_failures": 2,
        "failure_credit": 0,
        "recovery": "exact_sparse_paths_plus_required_stage_completeness",
        "runner_smoke_replayed": False,
        "skill_smoke_replayed": False,
    }
    write(truth_path, truth)

    write(
        X2 / "evidence-stage-recovery.json",
        {
            "schema": "ghc.family.caelen.v672-v4.evidence-stage-recovery.v1",
            "failed_stage_credit": 0,
            "failures": [
                {
                    "failure_id": additions[0]["failure_id"],
                    "failure": additions[0]["failure"],
                    "recovery": additions[0]["passing"],
                },
                {
                    "failure_id": additions[1]["failure_id"],
                    "failure": additions[1]["failure"],
                    "recovery": additions[1]["passing"],
                },
            ],
            "runner_smoke_replayed": False,
            "skill_smoke_replayed": False,
            "canonical_invocations": 0,
            "canonical_successes": 0
        },
    )


if __name__ == "__main__":
    main()
