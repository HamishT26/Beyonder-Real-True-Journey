#!/usr/bin/env python3
"""
Emit one Body policy-update trial record from the latest calibration report.

Reads docs/body-track-calibration-latest.json, extracts policy_delta_analysis
and recommendations, and appends one trial record to docs/body-track-policy-trials.jsonl
with delta_status=pending and observed_after=null. A future run or manual step
can fill observed_after and set delta_status to accepted/rejected.

See docs/body-track-policy-update-trial-design-v0.md for the trial protocol.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Emit one policy-update trial record from latest calibration.")
    parser.add_argument("--calibration-json", default="docs/body-track-calibration-latest.json")
    parser.add_argument("--trials-jsonl", default="docs/body-track-policy-trials.jsonl")
    parser.add_argument("--trial-id", default=None, help="Override trial id (default: trial-YYYYMMDD-001)")
    args = parser.parse_args()

    cal_path = Path(args.calibration_json)
    if not cal_path.exists():
        print(f"Calibration file not found: {cal_path}")
        return 1

    payload = json.loads(cal_path.read_text(encoding="utf-8"))
    policy_delta = payload.get("policy_delta_analysis")
    if not isinstance(policy_delta, dict):
        print("policy_delta_analysis missing or invalid")
        return 1

    recommended = policy_delta.get("recommended_policy") or {}
    before_after = policy_delta.get("false_alert_before_after") or {}
    apply_candidate = policy_delta.get("apply_recommendation_candidate", False)

    now = datetime.now(timezone.utc).replace(microsecond=0)
    trial_id = args.trial_id or f"trial-{now.strftime('%Y%m%d')}-001"

    # Trial 1: benchmark_profile dimension only
    trial = {
        "trial_id": trial_id,
        "generated_utc": now.isoformat(),
        "policy_dimension": "benchmark_profile",
        "recommended_value": recommended.get("benchmark_profile", "standard"),
        "expected_before": before_after.get("benchmark_before"),
        "expected_after": before_after.get("benchmark_after"),
        "observed_after": None,
        "delta_status": "pending",
        "apply_recommendation_candidate": apply_candidate,
    }

    out_path = Path(args.trials_jsonl)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(trial) + "\n")

    print(f"trial_id={trial_id}")
    print(f"trials_jsonl={out_path}")
    print(f"delta_status=pending (fill observed_after to set accepted/rejected)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
