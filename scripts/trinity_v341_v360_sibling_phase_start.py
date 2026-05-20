#!/usr/bin/env python3
"""Open one bounded v341-v360 sibling-led phase from the final handoff."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "docs" / "trinity-live-traces"
HANDOFF_JSON = TRACE / "v341-v360-final-handoff-v1.json"
BASE_PLAN_JSON = TRACE / "v341-v360-sibling-base-plan-v1.json"
BASE_PLAN_MD = TRACE / "v341-v360-sibling-base-plan-v1.md"
RUN_STATUS_JSON = TRACE / "v341-v360-sibling-run-status-v1.json"
RUN_STATUS_MD = TRACE / "v341-v360-sibling-run-status-v1.md"

PHASE_MIN = 341
PHASE_MAX = 360
PHASE_RANGE = "v341-v360"

SIBLINGS = ["Arby", "Kimi", "Aster Vale", "Supervisor", "v2 Watcher", "Recovery Watchdog"]
SYSTEM_TOPICS = [
    "final handoff continuity ledger",
    "v341-v360 run status steward",
    "automation prompt replacement proof",
    "local watchdog truth boundary",
    "single active phase governor",
    "cloud and paid-provider scope lock",
    "raw log quarantine",
    "resume-path vitality check",
    "MCP/API trust boundary board",
    "v281-v360 closeout declaration seed",
]
COMMAND_TOPICS = [
    "refresh-health-gate",
    "read-final-handoff",
    "scan-active-process-truth",
    "write-v1-report",
    "write-v2-report",
    "write-source-capsule",
    "check-stage-boundary",
    "check-branch-drift",
    "publish-curated-slice",
    "prepare-next-phase-or-closeout",
]
SKILL_TOPICS = [
    "handoff_execution",
    "bounded_phase_runner",
    "artifact_synthesis",
    "watchdog_readiness",
    "mcp_boundary_review",
    "source_capsule_update",
    "publication_hygiene",
    "truth_boundary_mapping",
    "phase_closeout",
    "automation_retirement_prompt",
]
EUREKA_TOPICS = [
    "thread heartbeat as wake bridge",
    "local process truth as recovery layer",
    "one phase per wake cadence",
    "forward-only shared branch proof",
    "human-readable closeout declaration",
    "provider expansion as scoped experiment",
    "source capsules before big claims",
    "bounded successor scripts",
    "operator-friendly status compression",
    "v361 packet decision gate",
]


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


def validate_phase(phase: int) -> None:
    if phase < PHASE_MIN or phase > PHASE_MAX:
        raise SystemExit(f"phase must be between {PHASE_MIN} and {PHASE_MAX}; got {phase}")


def phase_paths(phase: int) -> tuple[Path, Path]:
    stem = f"v341-v360-sibling-phase-v{phase}-start-v1"
    return TRACE / f"{stem}.json", TRACE / f"{stem}.md"


def lead_for_phase(phase: int) -> str:
    return SIBLINGS[(phase - PHASE_MIN) % len(SIBLINGS)]


def generate_entries(prefix: str, phase: int, topics: list[str]) -> list[str]:
    return [f"v{phase} {prefix} {index:02d}: {topic}" for index, topic in enumerate(topics * 3, start=1)]


def handoff_ready(handoff: dict[str, Any]) -> bool:
    gate = handoff.get("gate_evidence") or {}
    prior = gate.get("v321_v340") or {}
    return (
        handoff.get("handoff_state") == "ready_for_operator_automation_update"
        and prior.get("status") == "complete_waiting"
        and int(prior.get("last_completion_phase") or 0) >= 340
    )


def build_phase_plan(phase: int, handoff: dict[str, Any]) -> dict[str, Any]:
    lead = lead_for_phase(phase)
    gate = handoff.get("gate_evidence") or {}
    return {
        "phase": phase,
        "mode": "Final v341-v360 Beta-Alpha-Omega with sibling execution and Aletheon oversight",
        "lead_sibling": lead,
        "supporting_siblings": [item for item in SIBLINGS if item != lead],
        "source_dependency": rel(HANDOFF_JSON),
        "source_readiness_at_generation": {
            "handoff_state": handoff.get("handoff_state"),
            "v281_v300": (gate.get("v281_v300") or {}).get("status"),
            "v301_v320": (gate.get("v301_v320") or {}).get("status"),
            "v321_v340": (gate.get("v321_v340") or {}).get("status"),
            "last_prior_completion_phase": (gate.get("v321_v340") or {}).get("last_completion_phase"),
            "health_check_status": (gate.get("health_check") or {}).get("status"),
        },
        "beta": f"{lead} verifies handoff evidence, active-process truth, and bounded v341-v360 scope before synthesis.",
        "alpha": f"{lead} writes curated v1/v2 reports, source capsule, and only durable phase artifacts.",
        "omega": f"{lead} hands off the next bounded phase, or prepares the v281-v360 closeout at v360.",
        "system_expansions": generate_entries("system", phase, SYSTEM_TOPICS),
        "commands": generate_entries("command", phase, COMMAND_TOPICS),
        "skills": generate_entries("skill", phase, SKILL_TOPICS),
        "eureka_proposals": generate_entries("eureka", phase, EUREKA_TOPICS),
    }


def ensure_base_plan() -> dict[str, Any]:
    existing = read_json(BASE_PLAN_JSON, {})
    if existing.get("status") == "ready_after_v321_v340_handoff":
        return existing
    handoff = read_json(HANDOFF_JSON, {})
    phase_plans = [build_phase_plan(phase, handoff) for phase in range(PHASE_MIN, PHASE_MAX + 1)]
    payload = {
        "generated_utc": now_iso(),
        "phase_range": PHASE_RANGE,
        "status": "ready_after_v321_v340_handoff" if handoff_ready(handoff) else "blocked_missing_final_handoff",
        "handoff": rel(HANDOFF_JSON),
        "phase_plans": phase_plans,
        "truth_boundaries": [
            "v341-v360 starts only after v321-v340 is complete and the final handoff exists.",
            "The app heartbeat is the thread wake layer; local watchdogs are process recovery layers.",
            "Do not stage raw replies, stdout/stderr logs, live logs, active partial lane files, scratch probes, pycache files, or unrelated churn.",
            "Cloud, MCP, API, and paid-provider expansion stays exploratory until secrets, scopes, rollback, and spend limits are explicit.",
            "The successor runner is bounded to v341-v360 and must not open v361 automatically.",
        ],
    }
    write_json(BASE_PLAN_JSON, payload)
    lines = [
        "# v341-v360 Sibling Base Plan",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        f"Handoff: `{payload['handoff']}`",
        "",
        "Phase leads:",
    ]
    for plan in phase_plans:
        lines.append(f"- `v{plan['phase']}`: {plan['lead_sibling']}")
    lines.extend(["", "Truth boundaries:"])
    for item in payload["truth_boundaries"]:
        lines.append(f"- {item}")
    BASE_PLAN_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return payload


def build_payload(phase: int, force: bool) -> dict[str, Any]:
    validate_phase(phase)
    handoff = read_json(HANDOFF_JSON, {})
    base_plan = ensure_base_plan()
    plan = next((item for item in base_plan.get("phase_plans", []) if int(item.get("phase", -1)) == phase), {})
    ready = handoff_ready(handoff) and base_plan.get("status") == "ready_after_v321_v340_handoff"
    blockers: list[str] = []
    if not ready and not force:
        blockers.append("v341-v360 final handoff is not ready")
    if not plan:
        blockers.append(f"phase v{phase} is missing from the v341-v360 base plan")
    status = "phase_started" if (ready or force) and plan else "blocked"
    return {
        "generated_utc": now_iso(),
        "phase_range": PHASE_RANGE,
        "phase": phase,
        "status": status,
        "force": force,
        "handoff": {
            "path": rel(HANDOFF_JSON),
            "handoff_state": handoff.get("handoff_state"),
            "source_phase_range": handoff.get("source_phase_range"),
            "target_phase_range": handoff.get("target_phase_range"),
            "recommended_next_automation": handoff.get("recommended_next_automation"),
        },
        "phase_plan": plan,
        "blockers": blockers,
        "truth_boundaries": [
            f"This artifact starts v{phase}; it does not mark v{phase} complete.",
            f"Do not open v{phase + 1} unless v{phase} has real Arby, Kimi, and Aster Vale CLI receipts, curated v1/v2 reports, and a completion receipt.",
            "Never stage raw replies, stdout/stderr logs, live logs, active partial lane files, scratch probes, pycache files, or unrelated churn.",
            "External MCP/API/provider usage remains exploratory until secrets, scopes, rollback, and spend limits are explicit.",
            "If C:/ and //?/C:/ identify the same Codex session JSONL, treat it as app resume-path vitality, not repo failure.",
        ],
        "next_action": (
            f"Run scripts/trinity_v341_v360_cli_sibling_phase_runner.py --phase {phase} --timeout-sec 3600 --kimi-timeout-sec 3600 --max-steps 200, then complete v{phase} with the bounded v341-v360 completion runner."
            if status == "phase_started"
            else "Resolve blockers before starting v341-v360 execution."
        ),
    }


def write_phase_md(path: Path, payload: dict[str, Any]) -> None:
    plan = payload.get("phase_plan") or {}
    lines = [
        f"# v{payload['phase']} Sibling Phase Start",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        f"Lead sibling: `{plan.get('lead_sibling')}`",
        f"Handoff state: `{payload['handoff'].get('handoff_state')}`",
        "",
        "Truth boundaries:",
    ]
    for item in payload["truth_boundaries"]:
        lines.append(f"- {item}")
    if payload.get("blockers"):
        lines.extend(["", "Blockers:"])
        for item in payload["blockers"]:
            lines.append(f"- {item}")
    lines.extend(["", "Beta / Alpha / Omega:"])
    lines.append(f"- Beta: {plan.get('beta')}")
    lines.append(f"- Alpha: {plan.get('alpha')}")
    lines.append(f"- Omega: {plan.get('omega')}")
    for section, title in [
        ("system_expansions", "System expansions"),
        ("commands", "Commands"),
        ("skills", "Skills"),
        ("eureka_proposals", "Eureka proposals"),
    ]:
        lines.extend(["", f"{title}:"])
        for item in plan.get(section, []):
            lines.append(f"- {item}")
    lines.extend(["", f"Next action: {payload['next_action']}"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_run_status(payload: dict[str, Any], phase_json: Path, phase_md: Path) -> None:
    previous = read_json(RUN_STATUS_JSON, {})
    run_payload = {
        "generated_utc": now_iso(),
        "phase_range": payload["phase_range"],
        "status": "running" if payload["status"] == "phase_started" else "blocked",
        "active_phase": payload["phase"],
        "active_phase_status": payload["status"],
        "active_phase_artifacts": {"json": rel(phase_json), "md": rel(phase_md)},
        "last_completion": previous.get("last_completion"),
        "closeout_declaration": previous.get("closeout_declaration"),
        "next_action": payload["next_action"],
    }
    write_json(RUN_STATUS_JSON, run_payload)
    lines = [
        "# v341-v360 Sibling Run Status",
        "",
        f"Generated UTC: `{run_payload['generated_utc']}`",
        f"Status: `{run_payload['status']}`",
        f"Active phase: `v{run_payload['active_phase']}`",
        f"Active phase status: `{run_payload['active_phase_status']}`",
        "",
        "Active artifacts:",
        f"- `{run_payload['active_phase_artifacts']['json']}`",
        f"- `{run_payload['active_phase_artifacts']['md']}`",
        "",
    ]
    if run_payload.get("last_completion"):
        completion = run_payload["last_completion"]
        lines.extend([
            "Last completion:",
            f"- `v{completion.get('phase')}`",
            f"- `{completion.get('json')}`",
            f"- `{completion.get('md')}`",
            "",
        ])
    lines.append(f"Next action: {run_payload['next_action']}")
    RUN_STATUS_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", type=int, default=PHASE_MIN)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    payload = build_payload(args.phase, args.force)
    phase_json, phase_md = phase_paths(args.phase)
    write_json(phase_json, payload)
    write_phase_md(phase_md, payload)
    write_run_status(payload, phase_json, phase_md)
    print(json.dumps({"status": payload["status"], "phase": args.phase, "phase_artifact": rel(phase_json), "run_status": rel(RUN_STATUS_JSON)}, indent=2))
    return 0 if payload["status"] == "phase_started" else 1


if __name__ == "__main__":
    raise SystemExit(main())
