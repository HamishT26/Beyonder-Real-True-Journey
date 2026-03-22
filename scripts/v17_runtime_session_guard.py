#!/usr/bin/env python3
"""Validate the v17 runtime-session schema, log completeness, and overlay truth gate."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent


def _repo_path(path_str: str) -> Path:
    resolved = (ROOT / path_str).resolve()
    resolved.relative_to(ROOT)
    return resolved


def _load_json(path_str: str, failures: list[str], label: str) -> dict[str, Any]:
    try:
        payload = json.loads(_repo_path(path_str).read_text(encoding="utf-8"))
    except FileNotFoundError:
        failures.append(f"{label} missing: {path_str}")
        return {}
    except json.JSONDecodeError as exc:
        failures.append(f"{label} invalid json: {path_str} ({exc})")
        return {}
    if not isinstance(payload, dict):
        failures.append(f"{label} must decode to an object: {path_str}")
        return {}
    return payload


def _status(failures: list[str], warnings: list[str]) -> str:
    if failures:
        return "FAIL"
    if warnings:
        return "WARN"
    return "PASS"


def _check(name: str, ok: bool, success_detail: str, failure_detail: str, failures: list[str]) -> dict[str, str]:
    if ok:
        return {"name": name, "status": "PASS", "detail": success_detail}
    failures.append(failure_detail)
    return {"name": name, "status": "FAIL", "detail": failure_detail}


def _non_empty(value: object) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    return True


def _runtime_value_complete(field: str, value: object) -> bool:
    if field == "runtime_surface":
        text = str(value or "").strip()
        return bool(text) and text != "unknown"
    return _non_empty(value)


def _allowed_values(payload: dict[str, Any], field: str) -> list[str]:
    values = payload.get(field, [])
    if not isinstance(values, list):
        return []
    return [str(item) for item in values if str(item).strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the v17 runtime-session guard.")
    parser.add_argument("--schema", default="docs/v17-runtime-session-schema-v1.json")
    parser.add_argument("--session-log", default="docs/v17-runtime-session-log-latest.json")
    parser.add_argument("--control-tower", default="docs/v17-evidence-first-control-tower-latest.json")
    parser.add_argument("--handoff", default="docs/v19-omega-handoff-policy-v1.json")
    parser.add_argument("--runtime-resolution", default="docs/trinity-runtime-model-resolution-v1.json")
    parser.add_argument("--shadow-clone-policy", default="docs/trinity-shadow-clone-policy-v1.json")
    parser.add_argument("--latest-json", default="docs/v17-runtime-session-validation-latest.json")
    parser.add_argument("--fail-on-warn", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []
    warnings: list[str] = []
    checks: list[dict[str, str]] = []

    schema = _load_json(args.schema, failures, "schema")
    session_log = _load_json(args.session_log, failures, "session log")
    control_tower = _load_json(args.control_tower, failures, "control tower")
    handoff = _load_json(args.handoff, failures, "handoff")
    runtime_resolution = _load_json(args.runtime_resolution, failures, "runtime resolution")
    shadow_clone_policy = _load_json(args.shadow_clone_policy, failures, "shadow clone policy")

    session_required_fields = schema.get("session_required_fields", [])
    agent_required_fields = schema.get("agent_required_fields", [])
    expected_slots = [int(item) for item in schema.get("required_overlay_slots", []) if str(item).strip()]
    display_map_raw = schema.get("required_display_names", {})
    role_map_raw = schema.get("required_overlay_roles", {})
    required_runtime_fields = _allowed_values(schema, "required_runtime_fields")
    complete_runtime_fields = _allowed_values(schema, "non_empty_fields_for_complete_truth")
    allowed_runtime_surfaces = set(_allowed_values(schema, "allowed_runtime_surfaces"))
    complete_truth_runtime_surfaces = set(_allowed_values(schema, "complete_truth_runtime_surfaces"))
    allowed_incomplete_states = set(_allowed_values(schema, "incomplete_truth_allowed_overlay_states"))
    truth_status_values = set(_allowed_values(schema, "truth_status_values"))
    control_tower_state_field = str(schema.get("control_tower_state_field") or "external_live_overlay_state")

    display_map = {int(key): str(value) for key, value in display_map_raw.items()} if isinstance(display_map_raw, dict) else {}
    role_map = {int(key): str(value) for key, value in role_map_raw.items()} if isinstance(role_map_raw, dict) else {}

    schema_required_ok = (
        isinstance(session_required_fields, list)
        and isinstance(agent_required_fields, list)
        and bool(expected_slots)
        and bool(display_map)
        and bool(role_map)
        and bool(required_runtime_fields)
        and bool(complete_runtime_fields)
        and bool(allowed_runtime_surfaces)
        and bool(complete_truth_runtime_surfaces)
        and bool(allowed_incomplete_states)
        and bool(truth_status_values)
    )
    checks.append(
        _check(
            "schema_definition",
            schema_required_ok,
            f"schema_version={schema.get('schema_version')}, slots={expected_slots}",
            "schema must define required session, agent, runtime, and overlay-state rules",
            failures,
        )
    )

    handoff_agents = handoff.get("deployed_main_agents")
    if not isinstance(handoff_agents, list):
        handoff_agents = handoff.get("active_runtime_agents")
    if not isinstance(handoff_agents, list):
        handoff_agents = handoff.get("agents", [])
    handoff_slots = sorted(
        int(row.get("slot_number", 0))
        for row in handoff_agents
        if isinstance(row, dict) and row.get("slot_number") is not None and str(row.get("slot_number")).strip()
    )
    handoff_required_fields = handoff.get("runtime_truth_policy", {}).get("required_runtime_fields", [])
    if not isinstance(handoff_required_fields, list):
        handoff_required_fields = handoff.get("live_thread_requirements", {}).get("required_runtime_fields", [])
    handoff_ok = handoff_slots == sorted(expected_slots) and list(handoff_required_fields) == required_runtime_fields
    checks.append(
        _check(
            "handoff_alignment",
            handoff_ok,
            f"handoff_slots={handoff_slots}, required_runtime_fields={handoff_required_fields}",
            "handoff agents and required runtime fields must align with the v17 schema",
            failures,
        )
    )

    resolution_agents = runtime_resolution.get("deployed_main_agents")
    if not isinstance(resolution_agents, list):
        resolution_agents = runtime_resolution.get("external_overlay_agents", [])
    resolution_slots = sorted(
        int(row.get("slot_number", 0))
        for row in resolution_agents
        if isinstance(row, dict) and row.get("slot_number") is not None and str(row.get("slot_number")).strip()
    )
    resolution_ok = resolution_slots == sorted(expected_slots)
    checks.append(
        _check(
            "runtime_resolution_alignment",
            resolution_ok,
            f"runtime_resolution_slots={resolution_slots}",
            "runtime-resolution overlay roster must align with the v17 schema",
            failures,
        )
    )

    missing_session_fields = [
        field
        for field in session_required_fields
        if isinstance(session_required_fields, list) and field not in session_log
    ]
    overlay_agents = session_log.get("overlay_agents", [])
    session_shape_ok = isinstance(overlay_agents, list) and not missing_session_fields
    checks.append(
        _check(
            "session_log_shape",
            session_shape_ok,
            f"session_id={session_log.get('session_id')}, overlay_agents={len(overlay_agents) if isinstance(overlay_agents, list) else 0}",
            f"session log missing required fields: {missing_session_fields}" if missing_session_fields else "session log overlay_agents must be a list",
            failures,
        )
    )

    session_slots: list[int] = []
    complete_agents: list[str] = []
    pending_agents: list[str] = []
    complete_value_count = 0
    expected_value_count = 0
    runtime_surface_errors: list[str] = []
    agent_shape_errors: list[str] = []

    for index, row in enumerate(overlay_agents if isinstance(overlay_agents, list) else []):
        label = f"overlay_agents[{index}]"
        if not isinstance(row, dict):
            agent_shape_errors.append(f"{label} must be an object")
            continue
        session_slots.append(int(row.get("slot_number", 0) or 0))
        missing_agent_fields = [field for field in agent_required_fields if field not in row]
        if missing_agent_fields:
            agent_shape_errors.append(f"{label} missing fields {missing_agent_fields}")
        slot_number = int(row.get("slot_number", 0) or 0)
        display_name = str(row.get("display_name") or "")
        overlay_role = str(row.get("overlay_role") or "")
        if display_map.get(slot_number) and display_name != display_map[slot_number]:
            agent_shape_errors.append(f"{label} display_name must be {display_map[slot_number]}")
        if role_map.get(slot_number) and overlay_role != role_map[slot_number]:
            agent_shape_errors.append(f"{label} overlay_role must be {role_map[slot_number]}")
        if row.get("logging_required") is not True:
            agent_shape_errors.append(f"{label} logging_required must be true")
        runtime_surface = str(row.get("runtime_surface") or "")
        if runtime_surface and runtime_surface not in allowed_runtime_surfaces:
            runtime_surface_errors.append(f"{label} invalid runtime_surface {runtime_surface}")

        row_complete = True
        for field in required_runtime_fields:
            expected_value_count += 1
            if field not in row:
                row_complete = False
                continue
            value = row.get(field)
            if field in complete_runtime_fields:
                if field == "runtime_surface":
                    text = str(value or "").strip()
                    if text in complete_truth_runtime_surfaces:
                        complete_value_count += 1
                    else:
                        row_complete = False
                elif _runtime_value_complete(field, value):
                    complete_value_count += 1
                else:
                    row_complete = False
        if row.get("truth_fields_complete") is not row_complete:
            agent_shape_errors.append(f"{label} truth_fields_complete must be {row_complete}")
        if row_complete:
            complete_agents.append(display_name or label)
        else:
            pending_agents.append(display_name or label)

    roster_ok = sorted(session_slots) == sorted(expected_slots) and not agent_shape_errors and not runtime_surface_errors
    checks.append(
        _check(
            "overlay_roster_alignment",
            roster_ok,
            f"session_slots={sorted(session_slots)}, pending_agents={pending_agents}",
            "; ".join(agent_shape_errors + runtime_surface_errors) or "overlay roster must align with the schema",
            failures,
        )
    )

    shadow_clone_required_fields = schema.get("shadow_clone_session_required_fields", [])
    shadow_clone_name_pattern = str(
        schema.get("shadow_clone_name_pattern")
        or shadow_clone_policy.get("shadow_clone_name_pattern")
        or r"^[A-Za-z][A-Za-z ]* S Clone #[1-9][0-9]*$"
    )
    allowed_shadow_clone_owners = shadow_clone_policy.get("allowed_shadow_clone_owners", [])
    if not isinstance(allowed_shadow_clone_owners, list):
        allowed_shadow_clone_owners = []
    shadow_clone_sessions = session_log.get("shadow_clone_sessions", [])
    shadow_clone_errors: list[str] = []
    shadow_clone_count = 0
    if shadow_clone_sessions is not None and not isinstance(shadow_clone_sessions, list):
        shadow_clone_errors.append("shadow_clone_sessions must be a list when present")
        shadow_clone_sessions = []
    for index, row in enumerate(shadow_clone_sessions if isinstance(shadow_clone_sessions, list) else []):
        label = f"shadow_clone_sessions[{index}]"
        if not isinstance(row, dict):
            shadow_clone_errors.append(f"{label} must be an object")
            continue
        shadow_clone_count += 1
        missing_clone_fields = [field for field in shadow_clone_required_fields if field not in row]
        if missing_clone_fields:
            shadow_clone_errors.append(f"{label} missing fields {missing_clone_fields}")
        clone_name = str(row.get("clone_name") or "")
        if not clone_name or not re.match(shadow_clone_name_pattern, clone_name):
            shadow_clone_errors.append(f"{label} clone_name must match {shadow_clone_name_pattern}")
        owner_main_agent = str(row.get("owner_main_agent") or "")
        if allowed_shadow_clone_owners and owner_main_agent not in allowed_shadow_clone_owners:
            shadow_clone_errors.append(f"{label} owner_main_agent must be one of {allowed_shadow_clone_owners}")
        if row.get("continuity_authority") is not False:
            shadow_clone_errors.append(f"{label} continuity_authority must be false")
        if str(row.get("memory_persistence_claim") or "") != "none":
            shadow_clone_errors.append(f"{label} memory_persistence_claim must be none")
    checks.append(
        _check(
            "shadow_clone_policy",
            not shadow_clone_errors,
            f"shadow_clone_sessions={shadow_clone_count}",
            "; ".join(shadow_clone_errors) or "shadow clone policy must be enforced in the runtime log",
            failures,
        )
    )

    computed_complete = bool(overlay_agents) and len(complete_agents) == len(expected_slots)
    session_truth_complete = bool(session_log.get("session_truth_complete"))
    runtime_truth_status = str(session_log.get("runtime_truth_status") or "")
    logged_required_fields = session_log.get("runtime_truth_required_fields", [])
    completeness_ratio = float(session_log.get("runtime_truth_completion_ratio", 0.0) or 0.0)
    expected_ratio = round((complete_value_count / expected_value_count), 4) if expected_value_count else 0.0
    truth_flags_ok = (
        session_truth_complete == computed_complete
        and runtime_truth_status == ("complete_runtime_truth" if computed_complete else "pending_runtime_truth")
        and runtime_truth_status in truth_status_values
        and list(logged_required_fields) == required_runtime_fields
        and abs(completeness_ratio - expected_ratio) <= 0.0001
    )
    checks.append(
        _check(
            "runtime_truth_flags",
            truth_flags_ok,
            f"session_truth_complete={computed_complete}, completion_ratio={expected_ratio}",
            "runtime truth flags must match computed completeness and required field coverage",
            failures,
        )
    )

    overlay_state = str(session_log.get("overlay_state") or "")
    control_tower_state = str(control_tower.get(control_tower_state_field) or "")
    overlay_state_ok = overlay_state == control_tower_state
    checks.append(
        _check(
            "overlay_state_alignment",
            overlay_state_ok,
            f"overlay_state={overlay_state}",
            f"session log overlay_state must match control tower {control_tower_state_field}={control_tower_state}",
            failures,
        )
    )

    safe_hold_ok = computed_complete or overlay_state in allowed_incomplete_states
    control_tower_hold_ok = computed_complete or control_tower_state in allowed_incomplete_states
    checks.append(
        _check(
            "overlay_truth_gate",
            safe_hold_ok and control_tower_hold_ok,
            f"runtime_truth_complete={computed_complete}, overlay_state={overlay_state}, control_tower_state={control_tower_state}",
            "live overlay state must remain awaiting_thread_boot or packaged_handoff until runtime truth is complete",
            failures,
        )
    )

    payload = {
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "system_id": "v17_runtime_session_validation",
        "pillar": "trinity",
        "overall_status": _status(failures, warnings),
        "checks": checks,
        "metrics": {
            "schema_version": str(schema.get("schema_version") or ""),
            "expected_overlay_slots": expected_slots,
            "session_overlay_slots": sorted(session_slots),
            "required_runtime_fields": required_runtime_fields,
            "complete_runtime_fields": complete_runtime_fields,
            "runtime_truth_complete": computed_complete,
            "complete_agent_count": len(complete_agents),
            "pending_agent_count": len(pending_agents),
            "pending_agents": pending_agents,
            "complete_runtime_value_count": complete_value_count,
            "expected_runtime_value_count": expected_value_count,
            "runtime_truth_completion_ratio": expected_ratio,
            "overlay_state": overlay_state,
            "control_tower_state": control_tower_state,
            "allowed_incomplete_states": sorted(allowed_incomplete_states),
            "shadow_clone_session_count": shadow_clone_count,
        },
        "source_artifacts_checked": [
            args.schema,
            args.session_log,
            args.control_tower,
            args.handoff,
            args.runtime_resolution,
            args.shadow_clone_policy,
        ],
        "failures": failures,
        "warnings": warnings,
        "next_action": "Keep external_live_overlay_state at awaiting_thread_boot or packaged_handoff until every deployed continuity-bearing main agent logs complete requested/offered/selected/resolved/runtime_surface truth.",
        "effective_success": not failures and (not warnings or not args.fail_on_warn),
    }

    latest_json = _repo_path(args.latest_json)
    latest_json.parent.mkdir(parents=True, exist_ok=True)
    latest_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print(f"overall_status={payload['overall_status']}")
    print(f"runtime_truth_complete={payload['metrics']['runtime_truth_complete']}")
    print(f"latest_json={latest_json.relative_to(ROOT)}")
    return 0 if payload["effective_success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
