#!/usr/bin/env python3
"""Dry-run THOS supervisor gate.

This script classifies proposed shell, skill, plugin, connector, watcher, and
document actions. It never executes the requested action. The output is a local
decision report that can be used by phase artifacts and publication guards.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ALLOWED_ROW_STATUSES = {"FAIL_BLOCKER", "OPEN_GAP", "NOT_RUN", "PASS_SHAPE_ONLY"}
OBSERVE_CLASSES = {"none", "observe", "read_only", "dry_validate"}
MUTATING_CLASSES = {
    "local_write",
    "remote_write",
    "connector_mutate",
    "external_spend",
    "credential",
    "destructive",
    "mixed",
}
WRITE_VERBS = {
    "add",
    "archive",
    "batchupdate",
    "comment",
    "commit",
    "create",
    "delete",
    "deploy",
    "edit",
    "enable",
    "install",
    "label",
    "merge",
    "move",
    "push",
    "remove",
    "send",
    "share",
    "trash",
    "update",
    "upload",
}
CONNECTOR_SURFACES = {
    "connector",
    "plugin",
    "google_drive",
    "google_docs",
    "google_sheets",
    "google_slides",
    "github",
    "gmail",
    "calendar",
    "nvidia",
}
LOCAL_WRITE_APPROVALS = {"approved_live_write_action_pack", "approved_scope_limited"}
REMOTE_WRITE_APPROVALS = {"approved_scope_limited"}


def norm(value: Any) -> str:
    return str(value or "").strip().lower().replace(" ", "_").replace("-", "_")


def aggregate(rows: list[dict[str, Any]]) -> str:
    statuses = [row["status"] for row in rows]
    if "FAIL_BLOCKER" in statuses:
        return "FAIL_BLOCKER"
    if "OPEN_GAP" in statuses:
        return "OPEN_GAP"
    if statuses and all(status == "NOT_RUN" for status in statuses):
        return "NOT_RUN"
    return "PASS_SHAPE_ONLY"


def write_verb(operation: str) -> bool:
    return norm(operation) in WRITE_VERBS


def required_missing(request: dict[str, Any]) -> list[str]:
    required = ["request_id", "actor", "target_surface", "mutation_class", "operation", "scope"]
    return [field for field in required if not request.get(field)]


def decision_for(request: dict[str, Any]) -> dict[str, Any]:
    request_id = str(request.get("request_id") or "unknown_request")
    surface = norm(request.get("target_surface"))
    mutation_class = norm(request.get("mutation_class"))
    operation = str(request.get("operation") or "")
    approval = norm(request.get("approval_status"))
    scope = norm(request.get("scope"))
    bounded = bool(request.get("bounded_scope"))
    validators = request.get("validators") or []
    spend_limit = request.get("spend_limit_usd")
    result = {
        "request_id": request_id,
        "surface": surface or "unknown",
        "mutation_class": mutation_class or "unknown",
        "operation": operation or "unknown",
        "gate_result": "handoff",
        "status": "OPEN_GAP",
        "reason_code": "unclassified",
        "mutation_performed": False,
        "connector_write_performed": False,
        "validator_refs": validators,
    }

    missing = required_missing(request)
    if missing:
        result.update(
            gate_result="handoff",
            status="OPEN_GAP",
            reason_code="missing_required_fields",
            missing_fields=missing,
        )
        return result

    if mutation_class in {"credential", "destructive"}:
        result.update(
            gate_result="refuse",
            status="FAIL_BLOCKER",
            reason_code=f"{mutation_class}_request_not_allowed_by_dry_gate",
        )
        return result

    if mutation_class == "mixed":
        result.update(
            gate_result="handoff",
            status="OPEN_GAP",
            reason_code="mixed_read_write_request_must_be_split",
        )
        return result

    if not bounded:
        result.update(
            gate_result="handoff",
            status="OPEN_GAP",
            reason_code="scope_not_bounded",
        )
        return result

    if surface in CONNECTOR_SURFACES and (write_verb(operation) or mutation_class in {"remote_write", "connector_mutate"}):
        if approval not in REMOTE_WRITE_APPROVALS:
            result.update(
                gate_result="refuse",
                status="FAIL_BLOCKER",
                reason_code="connector_write_requires_named_scope_and_separate_approval",
            )
            return result
        if spend_limit is None:
            result.update(
                gate_result="handoff",
                status="OPEN_GAP",
                reason_code="connector_write_missing_spend_limit",
            )
            return result
        result.update(
            gate_result="dry_run_only",
            status="PASS_SHAPE_ONLY",
            reason_code="connector_write_shape_only_approved_but_not_executed",
        )
        return result

    if mutation_class == "local_write":
        if approval not in LOCAL_WRITE_APPROVALS:
            result.update(
                gate_result="handoff",
                status="OPEN_GAP",
                reason_code="local_write_requires_curated_approval",
            )
            return result
        result.update(
            gate_result="dry_run_only",
            status="PASS_SHAPE_ONLY",
            reason_code="local_write_shape_only_approved_but_not_executed",
        )
        return result

    if mutation_class == "external_spend":
        result.update(
            gate_result="handoff",
            status="OPEN_GAP",
            reason_code="external_spend_requires_named_budget_and_action_packet",
        )
        return result

    if mutation_class in OBSERVE_CLASSES:
        result.update(
            gate_result="dry_run_only" if mutation_class == "dry_validate" else "watch_only",
            status="PASS_SHAPE_ONLY",
            reason_code="observe_or_dry_validate_only",
        )
        return result

    if mutation_class in MUTATING_CLASSES:
        result.update(
            gate_result="handoff",
            status="OPEN_GAP",
            reason_code="mutation_class_requires_policy_mapping",
        )
        return result

    result.update(
        gate_result="handoff",
        status="OPEN_GAP",
        reason_code="unknown_mutation_class",
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a dry-run THOS supervisor gate.")
    parser.add_argument("--input", required=True, help="JSON file containing a request or requests list")
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    requests = data.get("requests", data if isinstance(data, list) else [data])
    if not isinstance(requests, list):
        raise SystemExit("input must be a request object, list, or object with requests list")

    rows = [decision_for(request) for request in requests if isinstance(request, dict)]
    report = {
        "validator_mode": "local_non_mutating_supervisor_gate",
        "input_file": Path(args.input).as_posix(),
        "aggregate_status": aggregate(rows),
        "mutation_performed": False,
        "connector_write_performed": False,
        "gmUT_gate_effect": "none_open_not_tested",
        "rows": rows,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if report["aggregate_status"] == "FAIL_BLOCKER" else 0


if __name__ == "__main__":
    sys.exit(main())
