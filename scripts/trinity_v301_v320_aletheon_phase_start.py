#!/usr/bin/env python3
"""Open a single Aletheon-led v301-v320 phase from the proven gate."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "docs" / "trinity-live-traces"
GATE_JSON = TRACE / "v301-v320-start-gate-status-v1.json"
BASE_PLAN_JSON = TRACE / "v301-v320-aletheon-base-plan-v1.json"
GLOBAL_V2_SYNTHESIS = TRACE / "v281-v300-double-trinity-global-v2-synthesis-v1.json"
REACTIVATION_PACKET = TRACE / "aletheon-reactivation-packet-v1.json"
RUN_STATUS_JSON = TRACE / "v301-v320-aletheon-run-status-v1.json"
RUN_STATUS_MD = TRACE / "v301-v320-aletheon-run-status-v1.md"


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def phase_output_paths(phase: int) -> tuple[Path, Path]:
    stem = f"v301-v320-aletheon-phase-v{phase}-start-v1"
    return TRACE / f"{stem}.json", TRACE / f"{stem}.md"


def phase_plan(base_plan: dict[str, Any], phase: int) -> dict[str, Any]:
    for item in base_plan.get("phase_plans", []):
        if int(item.get("phase", -1)) == phase:
            return item
    return {}


def build_payload(phase: int, force: bool) -> dict[str, Any]:
    gate = read_json(GATE_JSON, {})
    base_plan = read_json(BASE_PLAN_JSON, {})
    global_v2 = read_json(GLOBAL_V2_SYNTHESIS, {})
    reactivation = read_json(REACTIVATION_PACKET, {})
    ready = bool(gate.get("ready"))
    plan = phase_plan(base_plan, phase)
    status = "phase_started" if ready or force else "blocked_by_start_gate"
    blockers = []
    if not ready and not force:
        blockers.append("v301-v320 start gate is not ready")
    if not plan:
        blockers.append(f"phase v{phase} is missing from the base plan")
        status = "blocked_missing_phase_plan"
    return {
        "generated_utc": now_iso(),
        "phase_range": "v301-v320",
        "phase": phase,
        "status": status,
        "force": force,
        "gate": {
            "path": rel(GATE_JSON),
            "ready": gate.get("ready"),
            "valid_responses": gate.get("valid_responses"),
            "expected_responses": gate.get("expected_responses"),
            "complete_phases": gate.get("complete_phases"),
            "expected_phases": gate.get("expected_phases"),
            "global_v2_complete": (gate.get("global_v2") or {}).get("complete"),
        },
        "source_proof": {
            "global_v2_synthesis": rel(GLOBAL_V2_SYNTHESIS),
            "global_v2_status": global_v2.get("status"),
            "valid_v1_responses": global_v2.get("valid_v1_responses"),
            "reactivation_packet": rel(REACTIVATION_PACKET),
            "reactivation_status": reactivation.get("status"),
        },
        "phase_plan": plan,
        "blockers": blockers,
        "truth_boundaries": [
            f"This artifact starts v{phase}; it does not mark v{phase} complete.",
            f"Do not open v{phase + 1} until v{phase} has a completion receipt and curated handoff.",
            "Do not stage raw lane replies, live logs, stderr/stdout, or health-probe scratch files.",
            "Keep Administrator terminals for explicit elevated tasks only; normal phase work should use non-admin runners.",
        ],
        "next_action": (
            f"Execute v{phase} tasks, write a v{phase} completion receipt, then decide whether v{phase + 1} can open."
            if status == "phase_started"
            else "Resolve blockers before opening v301-v320 execution."
        ),
    }


def write_phase_md(path: Path, payload: dict[str, Any]) -> None:
    plan = payload.get("phase_plan") or {}
    lines = [
        f"# v{payload['phase']} Aletheon Phase Start",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        f"Gate ready: `{payload['gate']['ready']}`",
        f"Source proof: `{payload['gate']['valid_responses']}/{payload['gate']['expected_responses']}` responses, global v2 `{payload['gate']['global_v2_complete']}`",
        "",
        "Truth boundaries:",
    ]
    for item in payload["truth_boundaries"]:
        lines.append(f"- {item}")
    if payload.get("blockers"):
        lines.extend(["", "Blockers:"])
        for item in payload["blockers"]:
            lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "Beta / Alpha / Omega:",
            f"- Beta: {plan.get('beta')}",
            f"- Alpha: {plan.get('alpha')}",
            f"- Omega: {plan.get('omega')}",
            "",
            "System expansions:",
        ]
    )
    for item in plan.get("system_expansions", []):
        lines.append(f"- {item}")
    lines.append("")
    lines.append("Commands:")
    for item in plan.get("commands", []):
        lines.append(f"- {item}")
    lines.append("")
    lines.append("Skills:")
    for item in plan.get("skills", []):
        lines.append(f"- {item}")
    lines.append("")
    lines.append("Eureka proposals:")
    for item in plan.get("eureka_proposals", []):
        lines.append(f"- {item}")
    lines.extend(["", f"Next action: {payload['next_action']}"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_run_status(payload: dict[str, Any], phase_json: Path, phase_md: Path) -> None:
    previous_status = read_json(RUN_STATUS_JSON, {})
    run_payload = {
        "generated_utc": now_iso(),
        "phase_range": payload["phase_range"],
        "status": "running" if payload["status"] == "phase_started" else "blocked",
        "active_phase": payload["phase"],
        "active_phase_status": payload["status"],
        "active_phase_artifacts": {
            "json": rel(phase_json),
            "md": rel(phase_md),
        },
        "next_action": payload["next_action"],
    }
    if previous_status.get("last_completion"):
        run_payload["last_completion"] = previous_status["last_completion"]
    write_json(RUN_STATUS_JSON, run_payload)
    lines = [
        "# v301-v320 Aletheon Run Status",
        "",
        f"Generated UTC: `{run_payload['generated_utc']}`",
        f"Status: `{run_payload['status']}`",
        f"Active phase: `v{run_payload['active_phase']}`",
        f"Active phase status: `{run_payload['active_phase_status']}`",
        "",
        "Artifacts:",
        f"- `{run_payload['active_phase_artifacts']['json']}`",
        f"- `{run_payload['active_phase_artifacts']['md']}`",
        "",
    ]
    if run_payload.get("last_completion"):
        completion = run_payload["last_completion"]
        lines.extend(
            [
                "Last completion:",
                f"- `v{completion.get('phase')}`",
                f"- `{completion.get('json')}`",
                f"- `{completion.get('md')}`",
                "",
            ]
        )
    lines.append(f"Next action: {run_payload['next_action']}")
    RUN_STATUS_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", type=int, default=301)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    payload = build_payload(args.phase, args.force)
    phase_json, phase_md = phase_output_paths(args.phase)
    write_json(phase_json, payload)
    write_phase_md(phase_md, payload)
    write_run_status(payload, phase_json, phase_md)
    print(
        json.dumps(
            {
                "status": payload["status"],
                "phase": args.phase,
                "phase_artifact": rel(phase_json),
                "run_status": rel(RUN_STATUS_JSON),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
