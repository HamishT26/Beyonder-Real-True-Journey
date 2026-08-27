#!/usr/bin/env python3
"""Record the bounded v672-v3 evidence-selection recovery without replaying smoke."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
X2 = ROOT / "docs" / "sable-rook" / "v672-v3" / "x2"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value):
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> None:
    flow_path = X2 / "method-flow" / "ledger.json"
    flow = load(flow_path)
    if any(row.get("method_id") == "SR6723-RECOVERY-METHOD-001" for row in flow["methods"]):
        raise SystemExit("recovery already recorded")
    additions = [
        {
            "method_id": "SR6723-RECOVERY-METHOD-001",
            "failure_id": "SR6723-X2-001",
            "trigger": "x1-only x2-absence assertion selected against the advanced x2 tree",
            "preferred_method": "materialize the immutable x1 Git archive and run the unchanged x1 module there",
            "failure": "combined advanced-tree selection failed the lifecycle-local x1 assertion",
            "passing": "immutable x1 archive selection passed without changing the canonical lane",
            "recommendation": "bind lifecycle-local tests to their exact commit context",
        },
        {
            "method_id": "SR6723-RECOVERY-METHOD-002",
            "failure_id": "SR6723-X2-002",
            "trigger": "integrated overview was 1330 words against the frozen 1400-word floor",
            "preferred_method": "expand only reversibility and human challenge-path explanation",
            "failure": "first current x2 selection failed the overview floor",
            "passing": "current x2 module passed after bounded explanatory expansion",
            "recommendation": "measure required prose before the evidence selection",
        },
    ]
    for row in additions:
        flow["methods"].append(
            {
                "method_id": row["method_id"],
                "trigger": row["trigger"],
                "preferred_method": row["preferred_method"],
                "state": "preferred_after_bounded_passing_witness",
                "rollback": "retain the failed selection and change only the affected dependency",
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
                    "credit": "bounded_recovery_only",
                    "description": row["passing"],
                    "state": "bounded_passing_not_original_success",
                },
            ]
        )
    flow["current_delta"] = {
        "effective_negatives": 58,
        "failed_witnesses": 58,
        "methods": 38,
        "passing_witnesses": 38,
    }
    flow["effective_counts"].update(
        {
            "effective_negatives": 35326,
            "effective_methods": 21937,
            "effective_failed_witnesses": 7147,
            "effective_passing_witnesses": 9224,
        }
    )
    write(flow_path, flow)

    negatives_path = X2 / "retained-negative-register.json"
    negatives = load(negatives_path)
    negatives["x2_unexpected_operational_failures"] = 2
    negatives["x2_operational_failure_ids"] = ["SR6723-X2-001", "SR6723-X2-002"]
    negatives["effective_total"] = 35326
    write(negatives_path, negatives)

    truth_path = X2 / "phase-truth.json"
    truth = load(truth_path)
    truth["effective_counts"].update(
        {
            "negatives": 35326,
            "methods": 21937,
            "failed_witnesses": 7147,
            "passing_witnesses": 9224,
        }
    )
    truth["evidence_selection"] = {
        "first_combined_selection": "failed_zero_full_selection_credit",
        "retained_failures": 2,
        "recovery": "immutable_x1_context_plus_current_x2_context",
        "smoke_replayed": False,
    }
    write(truth_path, truth)

    write(
        X2 / "evidence-selection-recovery.json",
        {
            "schema": "ghc.family.sable.v672-v3.evidence-selection-recovery.v1",
            "failed_selection_credit": 0,
            "failures": [
                {
                    "failure_id": "SR6723-X2-001",
                    "failure": "x1 lifecycle-only x2-absence assertion ran against the advanced tree",
                    "recovery": "unchanged x1 module in immutable x1 Git-archive context",
                },
                {
                    "failure_id": "SR6723-X2-002",
                    "failure": "overview word count was 1330 below the frozen 1400 floor",
                    "recovery": "bounded reversibility and human challenge-path explanation",
                },
            ],
            "runner_smoke_replayed": False,
            "skill_smoke_replayed": False,
            "canonical_invocations": 0,
            "canonical_successes": 0,
            "recovery_broader_credit": 0,
        },
    )


if __name__ == "__main__":
    main()
