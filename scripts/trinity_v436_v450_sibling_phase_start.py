#!/usr/bin/env python3
"""Open one bounded v436-v450 Trinity Hybrid v1/v2 bridge phase."""

from __future__ import annotations

import argparse
import json
from typing import Any

from trinity_v436_v450_bridge_common import (
    HANDOFF_JSON,
    PHASE_MIN,
    PREFIX,
    RUN_STATUS_JSON,
    aggregate_paths,
    build_phase_plan,
    cli_aggregate_complete,
    ensure_base_plan,
    import_legacy_v436_v1,
    now_iso,
    read_json,
    rel,
    start_paths,
    validate_phase,
    write_json,
    write_run_status,
    write_text,
    write_v2_active,
)


def build_start_payload(phase: int, force: bool) -> dict[str, Any]:
    validate_phase(phase)
    handoff = read_json(HANDOFF_JSON, {})
    base_plan = ensure_base_plan()
    plan = next((item for item in base_plan.get("phase_plans", []) if item.get("phase") == phase), build_phase_plan(phase))
    blockers: list[str] = []
    if handoff.get("handoff_state") != "ready_for_v436_v450" and not force:
        blockers.append("v436-v450 final handoff is missing or not ready.")
    return {
        "generated_utc": now_iso(),
        "phase_range": PREFIX,
        "phase": phase,
        "status": "phase_started" if not blockers else "blocked",
        "active_run": "v1_cli_receipts",
        "force": force,
        "handoff": rel(HANDOFF_JSON),
        "phase_plan": plan,
        "blockers": blockers,
        "truth_boundaries": [
            f"This starts v{phase}; it does not complete v1 or v2.",
            "For v436 only, completed legacy v1 CLI receipts may be imported once instead of relaunched.",
            "For v437-v450, Arby, Kimi, and Aster Vale must produce fresh v1 CLI receipts.",
            "Aletheon remains v2 App execution lead and publication approver.",
            "Parfit, Cicero, and Kierkegaard are advisory-only and non-blocking.",
            "Stop at v450 closeout unless Hamish explicitly asks for a fresh v451+ packet.",
        ],
    }


def write_start_md(phase: int, payload: dict[str, Any]) -> None:
    _, start_md = start_paths(phase)
    plan = payload.get("phase_plan") or {}
    lines = [
        f"# v{phase} Sibling Phase Start",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        f"Active run: `{payload['active_run']}`",
        f"Lead sibling: `{plan.get('lead_sibling')}`",
        "",
        "Theme:",
        plan.get("theme", ""),
        "",
        "Beta / Alpha / Omega:",
        f"- Beta: {plan.get('beta')}",
        f"- Alpha: {plan.get('alpha')}",
        f"- Omega: {plan.get('omega')}",
        "",
        "Truth boundaries:",
    ]
    lines.extend([f"- {item}" for item in payload["truth_boundaries"]])
    if payload.get("blockers"):
        lines.extend(["", "Blockers:"])
        lines.extend([f"- {item}" for item in payload["blockers"]])
    write_text(start_md, "\n".join(lines))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", type=int, default=PHASE_MIN)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    payload = build_start_payload(args.phase, args.force)
    previous_status = read_json(RUN_STATUS_JSON, {})
    last_completion = previous_status.get("last_completion")
    start_json, start_md = start_paths(args.phase)
    write_json(start_json, payload)
    write_start_md(args.phase, payload)

    if payload["status"] != "phase_started":
        next_action = "Resolve handoff blockers before launching v436-v450."
        write_run_status(args.phase, "v1_cli_receipts", "blocked", start_json, start_md, next_action, last_completion=last_completion)
        print(json.dumps({"status": "blocked", "phase": args.phase, "start": rel(start_json)}, indent=2))
        return 1

    imported = False
    if args.phase == PHASE_MIN:
        imported_payload = import_legacy_v436_v1()
        imported = bool(imported_payload and imported_payload.get("status") == "v1_cli_receipts_complete")

    if cli_aggregate_complete(args.phase):
        active = write_v2_active(args.phase, imported_v1=imported)
        active_json, active_md = (start_json, start_md)
        # Prefer the v2 active artifact in run-status when v1 is already complete.
        from trinity_v436_v450_bridge_common import v2_active_paths

        active_json, active_md = v2_active_paths(args.phase)
        write_run_status(args.phase, "v2_app_execution", active["status"], active_json, active_md, active["next_action"], last_completion=last_completion)
        status = active["status"]
    else:
        aggregate_json, _ = aggregate_paths(args.phase)
        next_action = (
            f"Run scripts/trinity_v436_v450_cli_sibling_phase_runner.py --phase {args.phase} "
            "--background --timeout-sec 86400 --kimi-timeout-sec 86400 --max-steps 10000."
        )
        write_run_status(args.phase, "v1_cli_receipts", "running", start_json, start_md, next_action, last_completion=last_completion)
        status = "phase_started"

    print(json.dumps({"status": status, "phase": args.phase, "start": rel(start_json)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
