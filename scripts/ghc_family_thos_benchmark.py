#!/usr/bin/env python3
"""Score matched-budget THOS benchmark result ledgers.

This scorer aggregates externally graded task results. It does not grade free
text itself and a synthetic calibration fixture is not an agent benchmark.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from statistics import fmean
from typing import Any


REQUIRED = {
    "task_id",
    "passed",
    "confidence",
    "latency_ms",
    "token_cost",
    "content_fingerprint",
    "privacy_incident",
    "handoff_loss",
    "recovered",
}


def score_results(results: list[dict[str, Any]], *, fixture_kind: str) -> dict[str, Any]:
    if not results:
        raise ValueError("results must not be empty")
    seen: set[str] = set()
    for index, row in enumerate(results):
        missing = REQUIRED - row.keys()
        if missing:
            raise ValueError(f"results[{index}] missing: {sorted(missing)}")
        if row["task_id"] in seen:
            raise ValueError(f"duplicate task_id: {row['task_id']}")
        seen.add(row["task_id"])
        confidence = float(row["confidence"])
        if not 0.0 <= confidence <= 1.0:
            raise ValueError(f"confidence out of range: {confidence}")
        if float(row["latency_ms"]) < 0 or float(row["token_cost"]) < 0:
            raise ValueError("latency and token cost must be non-negative")

    actual = [1.0 if row["passed"] else 0.0 for row in results]
    confidence = [float(row["confidence"]) for row in results]
    brier = fmean((p - y) ** 2 for p, y in zip(confidence, actual, strict=True))
    fingerprints = {str(row["content_fingerprint"]) for row in results}
    return {
        "schema": "ghc.family.thos-benchmark-score.v1",
        "fixture_kind": fixture_kind,
        "task_count": len(results),
        "success_rate": fmean(actual),
        "brier_score": brier,
        "mean_latency_ms": fmean(float(row["latency_ms"]) for row in results),
        "mean_token_cost": fmean(float(row["token_cost"]) for row in results),
        "unique_content_ratio": len(fingerprints) / len(results),
        "privacy_incident_count": sum(bool(row["privacy_incident"]) for row in results),
        "handoff_loss_count": sum(bool(row["handoff_loss"]) for row in results),
        "recovery_rate_when_needed": (
            fmean(1.0 if row["recovered"] else 0.0 for row in results if row["handoff_loss"])
            if any(row["handoff_loss"] for row in results)
            else None
        ),
        "finite_metrics": all(
            math.isfinite(value)
            for value in [brier, fmean(float(row["latency_ms"]) for row in results)]
        ),
        "interpretation_boundary": (
            "synthetic_scoring_calibration_not_agent_or_model_performance"
            if fixture_kind == "synthetic_scoring_calibration"
            else "requires_blind_matched_budget_tasks_and_external_grading"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    report = score_results(payload["results"], fixture_kind=payload["fixture_kind"])
    encoded = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
