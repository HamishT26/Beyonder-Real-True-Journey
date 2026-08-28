#!/usr/bin/env python3
"""Family-current bounded synthetic contract runner for Liora v674-v5."""
from __future__ import annotations
import json
from typing import Any

REQUIRED = ("record_id", "state", "vacancies", "correction_parent", "authority_claim", "real_world_action", "expected_valid")

def validate_record(record: dict[str, Any]) -> dict[str, Any]:
    missing = [key for key in REQUIRED if key not in record]
    reasons: list[str] = []
    if missing:
        reasons.append("missing_required:" + ",".join(missing))
    if record.get("state") != "synthetic_bounded":
        reasons.append("state_not_synthetic_bounded")
    vacancies = record.get("vacancies")
    if not isinstance(vacancies, list) or not vacancies:
        reasons.append("vacancy_not_visible")
    if not record.get("correction_parent"):
        reasons.append("correction_lineage_absent")
    if record.get("authority_claim") is not False:
        reasons.append("authority_claim_present")
    if record.get("real_world_action") is not False:
        reasons.append("real_world_action_present")
    valid = not reasons
    return {"record_id": record.get("record_id"), "valid": valid, "reasons": reasons, "expected_valid": record.get("expected_valid")}

def run_batch(records: list[dict[str, Any]], runner_id: str) -> dict[str, Any]:
    results = [validate_record(record) for record in records]
    expectation_matches = all(result["valid"] is result["expected_valid"] for result in results)
    return {
        "runner_id": runner_id,
        "record_count": len(results),
        "accepted": sum(result["valid"] for result in results),
        "rejected": sum(not result["valid"] for result in results),
        "expectation_matches": expectation_matches,
        "results": results,
    }
