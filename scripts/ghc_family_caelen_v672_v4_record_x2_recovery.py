#!/usr/bin/env python3
"""Record one bounded post-smoke recovery without replaying Caelen x2."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
X2 = ROOT / "docs" / "caelen-ash" / "v672-v4" / "x2"
METHOD_ID = "CA6724-RECOVERY-METHOD-002"
FAILURE_ID = "CA6724-X2-021"


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
    if any(row.get("method_id") == METHOD_ID for row in flow["methods"]):
        raise SystemExit("post-smoke recovery already recorded")
    flow["methods"].append(
        {
            "method_id": METHOD_ID,
            "trigger": "a Windows shell passed a wildcard path literally to the stale-label rg invocation",
            "preferred_method": "use explicit directories and rg-native glob filters",
            "state": "preferred_after_bounded_passing_witness",
            "rollback": "retain the failed read-only sweep and change no repository artifact",
            "sibling_recommendation": "on Windows, give rg explicit directory roots and use -g for filename selection",
        }
    )
    flow["witnesses"].extend(
        [
            {
                "witness_id": FAILURE_ID + "-FAIL",
                "method_id": METHOD_ID,
                "kind": "failed",
                "credit": 0,
                "description": "the first stale-label sweep failed before scanning because the wildcard path was invalid on Windows",
                "state": "retained_zero_credit_no_state_change",
            },
            {
                "witness_id": FAILURE_ID + "-PASS",
                "method_id": METHOD_ID,
                "kind": "passing",
                "credit": "bounded_read_only_recovery",
                "description": "explicit roots plus rg-native globs completed the stale-label sweep",
                "state": "bounded_passing_not_original_success",
            },
        ]
    )
    flow["current_delta"] = {
        "effective_negatives": 77,
        "failed_witnesses": 77,
        "methods": 38,
        "passing_witnesses": 57,
    }
    flow["effective_counts"].update(
        {
            "effective_negatives": 35408,
            "effective_methods": 21978,
            "effective_failed_witnesses": 7229,
            "effective_passing_witnesses": 9283,
        }
    )
    write(flow_path, flow)

    negatives_path = X2 / "retained-negative-register.json"
    negatives = load(negatives_path)
    negatives["x2_unexpected_operational_failures"] = 21
    negatives["x2_operational_failure_ids"].append(FAILURE_ID)
    negatives["effective_total"] = 35408
    write(negatives_path, negatives)

    truth_path = X2 / "phase-truth.json"
    truth = load(truth_path)
    truth["effective_counts"].update(
        {
            "negatives": 35408,
            "methods": 21978,
            "failed_witnesses": 7229,
            "passing_witnesses": 9283,
        }
    )
    truth["post_smoke_recovery"] = {
        "failure_id": FAILURE_ID,
        "failure_credit": 0,
        "method_id": METHOD_ID,
        "recovery": "explicit_roots_plus_rg_native_globs",
        "runner_smoke_replayed": False,
        "skill_smoke_replayed": False,
    }
    write(truth_path, truth)

    write(
        X2 / "post-smoke-recovery.json",
        {
            "schema": "ghc.family.caelen.v672-v4.post-smoke-recovery.v1",
            "failure_id": FAILURE_ID,
            "failure": "Windows rejected a literal wildcard path before the read-only stale-label scan",
            "failure_credit": 0,
            "recovery": "explicit directory roots and rg-native glob filters",
            "recovery_scope": "read_only_stale_label_sweep",
            "runner_smoke_replayed": False,
            "skill_smoke_replayed": False,
            "canonical_invocations": 0,
            "canonical_successes": 0,
        },
    )


if __name__ == "__main__":
    main()
