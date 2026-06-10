#!/usr/bin/env python3
"""Open one v321-v340 sibling-led phase from the v301-v320 handoff."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "docs" / "trinity-live-traces"
HANDOFF_JSON = TRACE / "v321-v340-sibling-handoff-v1.json"
BASE_PLAN_JSON = TRACE / "v321-v340-sibling-base-plan-v1.json"
BASE_PLAN_MD = TRACE / "v321-v340-sibling-base-plan-v1.md"
RUN_STATUS_JSON = TRACE / "v321-v340-sibling-run-status-v1.json"
RUN_STATUS_MD = TRACE / "v321-v340-sibling-run-status-v1.md"

SIBLINGS = ["Arby", "Kimi", "Aster Vale", "Supervisor", "v2 Watcher", "Recovery Watchdog"]
SYSTEM_TOPICS = [
    "sibling continuity ledger",
    "v1 report synthesis",
    "v2 report synthesis",
    "artifact quality gate",
    "raw log quarantine",
    "resume-path vitality check",
    "lid and sleep resilience note",
    "watchdog stewardship lane",
    "MCP trust boundary board",
    "Aletheon oversight bridge",
]
COMMAND_TOPICS = [
    "count-handoff-evidence",
    "write-v1-report",
    "write-v2-report",
    "compare-sibling-claims",
    "refresh-health",
    "scan-stage-boundary",
    "check-branch-drift",
    "publish-curated",
    "handoff-next-sibling",
    "preserve-truth-note",
]
SKILL_TOPICS = [
    "artifact_synthesis",
    "sibling_handoff",
    "watchdog_readiness",
    "mcp_boundary_review",
    "power_wake_resilience",
    "source_capsule_update",
    "publication_hygiene",
    "truth_boundary_mapping",
    "phase_closeout",
    "v341_seed_preparation",
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


def phase_paths(phase: int) -> tuple[Path, Path]:
    stem = f"v321-v340-sibling-phase-v{phase}-start-v1"
    return TRACE / f"{stem}.json", TRACE / f"{stem}.md"


def lead_for_phase(phase: int) -> str:
    return SIBLINGS[(phase - 321) % len(SIBLINGS)]


def generate_entries(prefix: str, phase: int, topics: list[str]) -> list[str]:
    return [f"v{phase} {prefix} {index:02d}: {topic}" for index, topic in enumerate(topics * 3, start=1)]


def build_phase_plan(phase: int, handoff: dict[str, Any]) -> dict[str, Any]:
    lead = lead_for_phase(phase)
    return {
        "phase": phase,
        "mode": "Sibling-led v1/v2 Beta-Alpha-Omega with Aletheon oversight",
        "lead_sibling": lead,
        "supporting_siblings": [item for item in SIBLINGS if item != lead],
        "source_dependency": rel(HANDOFF_JSON),
        "source_readiness_at_generation": {
            "handoff_status": handoff.get("status"),
            "v301_v320_completion_count": (handoff.get("v301_v320_run") or {}).get("completion_count"),
            "primary_heartbeat": ((handoff.get("health_check") or {}).get("primary_automation_status")),
        },
        "beta": f"{lead} validates v301-v320 evidence, watcher state, and phase boundaries before synthesis.",
        "alpha": f"{lead} writes sibling v1/v2 reports and improves only durable control-plane artifacts.",
        "omega": f"{lead} hands the phase back with truth boundaries, staging limits, and v341 readiness notes.",
        "system_expansions": generate_entries("system", phase, SYSTEM_TOPICS),
        "commands": generate_entries("command", phase, COMMAND_TOPICS),
        "skills": generate_entries("skill", phase, SKILL_TOPICS),
        "eureka_proposals": generate_entries("eureka", phase, [
            "sleep-aware automation cadence",
            "single durable watchdog parent",
            "sibling report artifact protocol",
            "admin-terminal risk split",
            "MCP scope confirmation",
            "copy-paste automation bridge",
            "forward-only publication check",
            "v341 launch seed",
            "operator-friendly status compression",
            "truth-boundary celebration note",
        ]),
    }


def ensure_base_plan() -> dict[str, Any]:
    existing = read_json(BASE_PLAN_JSON, {})
    if existing.get("status") == "ready_after_v301_v320_handoff":
        return existing
    handoff = read_json(HANDOFF_JSON, {})
    phase_plans = [build_phase_plan(phase, handoff) for phase in range(321, 341)]
    payload = {
        "generated_utc": now_iso(),
        "phase_range": "v321-v340",
        "status": "ready_after_v301_v320_handoff" if handoff.get("status") == "handoff_ready" else "blocked_missing_handoff",
        "handoff": rel(HANDOFF_JSON),
        "phase_plans": phase_plans,
        "truth_boundaries": [
            "v321-v340 starts only from the v301-v320 closeout and handoff evidence.",
            "Sibling reports are curated artifacts, not proof of independent external system access.",
            "Do not stage raw replies, stdout/stderr logs, live logs, or scratch health probes.",
            "Keep admin terminals exceptional; ordinary watchdog and phase work stays non-admin.",
        ],
    }
    write_json(BASE_PLAN_JSON, payload)
    lines = [
        "# v321-v340 Sibling Base Plan",
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
    handoff = read_json(HANDOFF_JSON, {})
    base_plan = ensure_base_plan()
    plan = next((item for item in base_plan.get("phase_plans", []) if int(item.get("phase", -1)) == phase), {})
    ready = handoff.get("status") == "handoff_ready" and base_plan.get("status") == "ready_after_v301_v320_handoff"
    blockers: list[str] = []
    if not ready and not force:
        blockers.append("v301-v320 handoff is not ready")
    if not plan:
        blockers.append(f"phase v{phase} is missing from the v321-v340 base plan")
    status = "phase_started" if (ready or force) and plan else "blocked"
    return {
        "generated_utc": now_iso(),
        "phase_range": "v321-v340",
        "phase": phase,
        "status": status,
        "force": force,
        "handoff": {
            "path": rel(HANDOFF_JSON),
            "status": handoff.get("status"),
            "completion_count": (handoff.get("v301_v320_run") or {}).get("completion_count"),
            "repo_head_at_handoff": handoff.get("repo_head_at_handoff"),
        },
        "phase_plan": plan,
        "blockers": blockers,
        "truth_boundaries": [
            f"This artifact starts v{phase}; it does not mark v{phase} complete.",
            f"Do not open v{phase + 1} until v{phase} has sibling v1/v2 reports and a completion receipt.",
            "Never stage raw replies, stdout/stderr logs, live logs, active partial lane files, or scratch health probes.",
            "External MCP/API/provider usage remains exploratory until secrets, scopes, costs, and sandboxes are explicit.",
        ],
        "next_action": (
            f"Execute v{phase} sibling tasks, write v1/v2 reports, complete v{phase}, then decide whether v{phase + 1} can open."
            if status == "phase_started"
            else "Resolve blockers before starting v321-v340 execution."
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
        f"Handoff status: `{payload['handoff'].get('status')}`",
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
        "next_action": payload["next_action"],
    }
    write_json(RUN_STATUS_JSON, run_payload)
    lines = [
        "# v321-v340 Sibling Run Status",
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
    parser.add_argument("--phase", type=int, default=321)
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
