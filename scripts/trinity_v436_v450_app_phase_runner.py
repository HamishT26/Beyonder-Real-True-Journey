#!/usr/bin/env python3
"""Record Aletheon-led v2 App execution for one v436-v450 bridge phase."""

from __future__ import annotations

import argparse
import json
from typing import Any

from trinity_v436_v450_bridge_common import (
    PREFIX,
    cli_aggregate_complete,
    now_iso,
    read_json,
    rel,
    start_paths,
    v2_active_paths,
    v2_receipt_paths,
    validate_phase,
    write_json,
    write_run_status,
    write_text,
    write_v2_active,
)


def start_v2(phase: int) -> dict[str, Any]:
    validate_phase(phase)
    start_json, _ = start_paths(phase)
    start = read_json(start_json, {})
    if start.get("status") != "phase_started":
        raise SystemExit(f"v{phase} phase start artifact is missing or not started")
    if not cli_aggregate_complete(phase):
        raise SystemExit(f"v{phase} v1 CLI receipt aggregate must be complete before v2 starts")
    active = write_v2_active(phase, imported_v1=phase == 436)
    active_json, active_md = v2_active_paths(phase)
    write_run_status(phase, "v2_app_execution", active["status"], active_json, active_md, active["next_action"])
    return active


def complete_v2(args: argparse.Namespace) -> dict[str, Any]:
    phase = args.phase
    validate_phase(phase)
    if not cli_aggregate_complete(phase):
        raise SystemExit(f"v{phase} v1 CLI receipt aggregate must be complete before v2 completes")
    active_json, _ = v2_active_paths(phase)
    active = read_json(active_json, {})
    if active.get("status") != "v2_app_run_active" and not args.force:
        raise SystemExit(f"v{phase} v2 must be started before completion; use --force only for recovery.")

    changed_paths = args.changed_path or []
    validations = args.validation or []
    blockers = args.blocker or []
    status = "v2_app_complete" if args.summary and validations and not blockers else "blocked_v2_app_incomplete"
    receipt_json, receipt_md = v2_receipt_paths(phase)
    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase_range": PREFIX,
        "phase": phase,
        "run": "v2_app_execution",
        "status": status,
        "summary": args.summary or "",
        "changed_paths": changed_paths,
        "validations": validations,
        "blockers": blockers,
        "external_policy": "local_first_only",
        "spent_external_usd": 0,
        "advisory_siblings": ["Parfit", "Cicero", "Kierkegaard"],
        "helper_lanes": ["Supervisor", "v2 Watcher", "Recovery Watchdog"],
        "truth_boundaries": [
            "This v2 receipt records Aletheon-led App execution, not CLI sibling receipt evidence.",
            "No paid external action or external-service mutation is claimed.",
            "Changed paths are declarative; Git staging checks remain required before commit.",
            "Advisory App siblings remain non-blocking unless a future durable tool promotes them.",
        ],
        "next_action": (
            f"Complete v{phase} with scripts/trinity_v436_v450_sibling_phase_complete.py --phase {phase} --open-next."
            if status == "v2_app_complete"
            else "Resolve v2 blockers before phase completion."
        ),
    }
    write_json(receipt_json, payload)
    lines = [
        f"# v{phase} v2 App Receipt",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        "",
        "Summary:",
        payload["summary"] or "-",
        "",
        "Changed paths:",
    ]
    lines.extend([f"- `{item}`" for item in changed_paths] or ["- None recorded"])
    lines.extend(["", "Validations:"])
    lines.extend([f"- {item}" for item in validations] or ["- None recorded"])
    if blockers:
        lines.extend(["", "Blockers:"])
        lines.extend([f"- {item}" for item in blockers])
    lines.extend(["", "Truth boundaries:"])
    lines.extend([f"- {item}" for item in payload["truth_boundaries"]])
    lines.extend(["", f"Next action: {payload['next_action']}"])
    write_text(receipt_md, "\n".join(lines))
    write_run_status(phase, "v2_app_execution", payload["status"], receipt_json, receipt_md, payload["next_action"])
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", type=int, required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--start", action="store_true")
    group.add_argument("--complete", action="store_true")
    parser.add_argument("--summary", default="")
    parser.add_argument("--validation", action="append")
    parser.add_argument("--changed-path", action="append")
    parser.add_argument("--blocker", action="append")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    payload = start_v2(args.phase) if args.start else complete_v2(args)
    print(json.dumps({"status": payload["status"], "phase": args.phase, "run": payload["run"]}, indent=2))
    return 0 if payload["status"] in {"v2_app_run_active", "v2_app_complete"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
