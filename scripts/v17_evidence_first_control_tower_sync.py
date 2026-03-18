#!/usr/bin/env python3
"""Sync v17 evidence-first state into the Trinity control tower."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
STATUS_ORDER = {"PASS": 0, "WARN": 1, "FAIL": 2, "TIMEOUT": 3}


def _repo_path(path_str: str) -> Path:
    resolved = (ROOT / path_str).resolve()
    resolved.relative_to(ROOT)
    return resolved


def _read_json(path_str: str) -> dict[str, Any]:
    return json.loads(_repo_path(path_str).read_text(encoding="utf-8"))


def _status(raw: object) -> str:
    text = str(raw or "").strip().upper()
    if text in STATUS_ORDER:
        return text
    return "FAIL"


def _worst_status(*values: object) -> str:
    statuses = [_status(value) for value in values]
    return max(statuses, key=lambda item: STATUS_ORDER[item])


def _markdown(payload: dict[str, Any]) -> str:
    lines = ["# Trinity Control Tower", ""]
    for key, value in payload.items():
        if key == "generated_utc":
            continue
        lines.append(f"- {key}: `{value}`")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync the v17 evidence-first state into the control tower.")
    parser.add_argument("--control-tower-json", default="docs/trinity-control-tower-latest.json")
    parser.add_argument("--control-tower-md", default="docs/trinity-control-tower-latest.md")
    parser.add_argument("--runtime-validation", default="docs/v17-runtime-session-validation-latest.json")
    parser.add_argument("--runtime-log", default="docs/v17-runtime-session-log-latest.json")
    parser.add_argument("--criteria-validation", default="docs/v17-external-establishment-validation-latest.json")
    parser.add_argument("--standards-validation", default="docs/v17-standards-bridge-validation-latest.json")
    parser.add_argument("--filesystem-gate", default="docs/trinity-expansion/filesystem-scope-governor-gate-latest.json")
    parser.add_argument("--mcp-catalog", default="docs/trinity-mcp-catalog-v11.json")
    parser.add_argument("--reports-dir", default="docs/v17-control-tower-runs")
    args = parser.parse_args()

    control = _read_json(args.control_tower_json)
    runtime_validation = _read_json(args.runtime_validation)
    runtime_log = _read_json(args.runtime_log)
    criteria_validation = _read_json(args.criteria_validation)
    standards_validation = _read_json(args.standards_validation)
    filesystem_gate = _read_json(args.filesystem_gate)
    mcp_catalog = _read_json(args.mcp_catalog)

    connectors = mcp_catalog.get("connectors", [])
    filesystem_connector = next(
        (
            row
            for row in connectors
            if isinstance(row, dict) and str(row.get("mcp_id") or "") == "filesystem"
        ),
        {},
    )
    filesystem_live_write_enabled = bool(filesystem_connector.get("live_write_enabled"))
    filesystem_actual_state = str(filesystem_connector.get("actual_state") or "unknown")
    filesystem_promotion_state = "promoted" if filesystem_live_write_enabled else "blocked"
    overlay_state = str(runtime_log.get("overlay_state") or "unknown")
    runtime_metrics = runtime_validation.get("metrics")
    runtime_truth_complete = bool(
        runtime_metrics.get("runtime_truth_complete")
        if isinstance(runtime_metrics, dict)
        else runtime_validation.get("runtime_truth_complete")
    )

    control["generated_utc"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    control["runtime_session_state"] = str(runtime_validation.get("overall_status") or "FAIL")
    control["runtime_session_overlay_state"] = overlay_state
    control["runtime_truth_complete"] = runtime_truth_complete
    control["external_establishment_criteria_state"] = str(criteria_validation.get("overall_status") or "FAIL")
    control["standards_bridge_state"] = str(standards_validation.get("overall_status") or "FAIL")
    control["filesystem_promotion_state"] = filesystem_promotion_state
    control["filesystem_connector_actual_state"] = filesystem_actual_state
    control["filesystem_gate_state"] = str(filesystem_gate.get("overall_status") or "FAIL")
    control["claim_boundary_state"] = _worst_status(
        criteria_validation.get("overall_status"),
        standards_validation.get("overall_status"),
    )
    control["v17_evidence_first_state"] = _worst_status(
        runtime_validation.get("overall_status"),
        criteria_validation.get("overall_status"),
        standards_validation.get("overall_status"),
        filesystem_gate.get("overall_status"),
    )
    control["external_live_overlay_state"] = overlay_state
    control["overall_status"] = _worst_status(control.get("overall_status"), control["v17_evidence_first_state"])

    control_json = _repo_path(args.control_tower_json)
    control_md = _repo_path(args.control_tower_md)
    reports_dir = _repo_path(args.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    control_json.write_text(json.dumps(control, indent=2) + "\n", encoding="utf-8")
    control_md.write_text(_markdown(control), encoding="utf-8")
    (reports_dir / f"{stamp}-v17-control-tower-sync.json").write_text(json.dumps(control, indent=2) + "\n", encoding="utf-8")
    (reports_dir / f"{stamp}-v17-control-tower-sync.md").write_text(_markdown(control), encoding="utf-8")
    print(f"overall_status={control['overall_status']}")
    print(f"control_tower_json={control_json.relative_to(ROOT)}")
    print(f"control_tower_md={control_md.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
