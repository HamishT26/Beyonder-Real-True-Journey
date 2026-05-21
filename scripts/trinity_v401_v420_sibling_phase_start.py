#!/usr/bin/env python3
"""Open one bounded v401-v420 sibling-led phase."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "docs" / "trinity-live-traces"
HANDOFF_JSON = TRACE / "v401-v420-final-handoff-v1.json"
BASE_PLAN_JSON = TRACE / "v401-v420-sibling-base-plan-v1.json"
BASE_PLAN_MD = TRACE / "v401-v420-sibling-base-plan-v1.md"
RUN_STATUS_JSON = TRACE / "v401-v420-sibling-run-status-v1.json"
RUN_STATUS_MD = TRACE / "v401-v420-sibling-run-status-v1.md"

PHASE_MIN = 401
PHASE_MAX = 420
PHASE_RANGE = "v401-v420"
SIBLINGS = ["Arby", "Kimi", "Aster Vale", "Supervisor", "v2 Watcher", "Recovery Watchdog", "Parfit", "Cicero", "Kierkegaard"]

SYSTEM_TOPICS = [
    "v401-v420 handoff truth",
    "10000-step CLI lane boundary",
    "single active phase governor",
    "raw log quarantine",
    "branch drift proof",
    "watcher freshness gate",
    "source capsule continuity",
    "GMUT hypothesis labeling",
    "Freed ID governance boundary",
    "v420 closeout seed",
]
COMMAND_TOPICS = [
    "refresh-health-gate",
    "read-v401-v420-handoff",
    "scan-live-cli-runner",
    "run-cli-receipt-gate",
    "write-v1-report",
    "write-v2-report",
    "write-source-capsule",
    "check-stage-boundary",
    "check-branch-drift",
    "publish-forward-only",
]
SKILL_TOPICS = [
    "handoff_execution",
    "real_cli_receipt_review",
    "artifact_synthesis",
    "watchdog_readiness",
    "source_capsule_update",
    "publication_hygiene",
    "truth_boundary_mapping",
    "phase_closeout",
    "automation_prompt_stewardship",
    "v420_packet_stop",
]
EUREKA_TOPICS = [
    "heartbeat as observation checkpoint",
    "CLI receipts as sibling proof",
    "10000-step ceiling as generous bound",
    "forward-only shared branch proof",
    "Aletheon as publication approver",
    "bounded successor scripts",
    "source capsules before big claims",
    "operator-friendly status compression",
    "raw transport quarantine",
    "next-packet decision gate",
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
    stem = f"v401-v420-sibling-phase-v{phase}-start-v1"
    return TRACE / f"{stem}.json", TRACE / f"{stem}.md"


def lead_for_phase(phase: int) -> str:
    return SIBLINGS[(phase - PHASE_MIN) % len(SIBLINGS)]


def generate_entries(prefix: str, phase: int, topics: list[str], target_count: int) -> list[str]:
    repeated = (topics * ((target_count // len(topics)) + 1))[:target_count]
    return [f"v{phase} {prefix} {index:02d}: {topic}" for index, topic in enumerate(repeated, start=1)]


def handoff_ready(handoff: dict[str, Any]) -> bool:
    gate = handoff.get("gate_evidence") or {}
    prior_v281_v360 = gate.get("v281_v360") or {}
    prior_v361_v370 = gate.get("v361_v370") or {}
    prior_v371_v400 = gate.get("v371_v400") or {}
    return (
        handoff.get("handoff_state") == "ready_for_v401_v420"
        and prior_v281_v360.get("status") == "complete"
        and prior_v361_v370.get("status") == "complete"
        and prior_v371_v400.get("status") == "complete"
    )


def build_phase_plan(phase: int, handoff: dict[str, Any]) -> dict[str, Any]:
    lead = lead_for_phase(phase)
    return {
        "phase": phase,
        "mode": "v401-v420 CLI Multiplex Beta-Alpha-Omega with sibling execution and Aletheon publication oversight",
        "lead_sibling": lead,
        "supporting_siblings": [item for item in SIBLINGS if item != lead],
        "source_dependency": rel(HANDOFF_JSON),
        "beta": f"{lead} verifies v281-v360 and v361-v370 closeout truth, v401-v420 handoff truth, live runner state, and 10000-step bounded CLI scope.",
        "alpha": f"{lead} produces real CLI receipt evidence, curated v1/v2 reports, and a source capsule without staging raw transport logs.",
        "omega": f"{lead} hands off the next bounded phase, or prepares the v401-v420 closeout at v420.",
        "system_expansions": generate_entries("system", phase, SYSTEM_TOPICS, 30),
        "commands": generate_entries("command", phase, COMMAND_TOPICS, 30),
        "skills": generate_entries("skill", phase, SKILL_TOPICS, 30),
        "eureka_proposals": generate_entries("eureka", phase, EUREKA_TOPICS, 50),
    }


def ensure_base_plan() -> dict[str, Any]:
    existing = read_json(BASE_PLAN_JSON, {})
    if existing.get("status") == "ready_after_v361_v370_closeout":
        return existing
    handoff = read_json(HANDOFF_JSON, {})
    plans = [build_phase_plan(phase, handoff) for phase in range(PHASE_MIN, PHASE_MAX + 1)]
    payload = {
        "generated_utc": now_iso(),
        "phase_range": PHASE_RANGE,
        "status": "ready_after_v371_v400_closeout" if handoff_ready(handoff) else "blocked_missing_v401_v420_handoff",
        "handoff": rel(HANDOFF_JSON),
        "phase_plans": plans,
        "truth_boundaries": [
            "v401-v420 starts only after v281-v360 and v361-v370 closeouts are complete and committed.",
            "The app heartbeat is an observation checkpoint; real CLI lane work may span many wakes.",
            "Request 10000 max useful steps where supported, with effective platform limits recorded instead of assumed.",
            "Do not stage raw replies, stdout/stderr logs, live logs, scratch probes, pycache files, secrets, or unrelated churn.",
            "The successor runner is bounded to v401-v420 and must not open v401 automatically.",
        ],
    }
    write_json(BASE_PLAN_JSON, payload)
    lines = [
        "# v401-v420 Sibling Base Plan",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        f"Handoff: `{payload['handoff']}`",
        "",
        "Phase leads:",
    ]
    for plan in plans:
        lines.append(f"- `v{plan['phase']}`: {plan['lead_sibling']}")
    lines.extend(["", "Truth boundaries:"])
    lines.extend([f"- {item}" for item in payload["truth_boundaries"]])
    BASE_PLAN_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return payload


def build_payload(phase: int, force: bool) -> dict[str, Any]:
    validate_phase(phase)
    handoff = read_json(HANDOFF_JSON, {})
    base_plan = ensure_base_plan()
    plan = next((item for item in base_plan.get("phase_plans", []) if int(item.get("phase", -1)) == phase), {})
    ready = handoff_ready(handoff) and base_plan.get("status") == "ready_after_v371_v400_closeout"
    blockers: list[str] = []
    if not ready and not force:
        blockers.append("v401-v420 final handoff is not ready")
    if not plan:
        blockers.append(f"phase v{phase} is missing from the v401-v420 base plan")
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
        },
        "phase_plan": plan,
        "blockers": blockers,
        "truth_boundaries": [
            f"This artifact starts v{phase}; it does not mark v{phase} complete.",
            "Real CLI receipts are required from Arby, Kimi, and Aster Vale before completion.",
            "Never stage raw replies, stdout/stderr logs, live logs, scratch probes, pycache files, secrets, or unrelated churn.",
            "External MCP/API/provider usage remains exploratory until secrets, scopes, rollback, and spend limits are explicit.",
        ],
        "next_action": (
            f"Run scripts/trinity_v401_v420_cli_sibling_phase_runner.py --phase {phase} --background --timeout-sec 86400 --kimi-timeout-sec 86400 --max-steps 10000."
            if status == "phase_started"
            else "Resolve blockers before starting v401-v420 execution."
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
        "",
        "Truth boundaries:",
        *[f"- {item}" for item in payload["truth_boundaries"]],
        "",
        "Beta / Alpha / Omega:",
        f"- Beta: {plan.get('beta')}",
        f"- Alpha: {plan.get('alpha')}",
        f"- Omega: {plan.get('omega')}",
        "",
        f"Next action: {payload['next_action']}",
    ]
    if payload.get("blockers"):
        lines.extend(["", "Blockers:", *[f"- {item}" for item in payload["blockers"]]])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_run_status(payload: dict[str, Any], phase_json: Path, phase_md: Path) -> None:
    run_payload = {
        "generated_utc": now_iso(),
        "phase_range": payload["phase_range"],
        "status": "running" if payload["status"] == "phase_started" else "blocked",
        "active_phase": payload["phase"],
        "active_phase_status": payload["status"],
        "active_phase_artifacts": {"json": rel(phase_json), "md": rel(phase_md)},
        "last_completion": None,
        "closeout_declaration": None,
        "next_action": payload["next_action"],
    }
    write_json(RUN_STATUS_JSON, run_payload)
    lines = [
        "# v401-v420 Sibling Run Status",
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
        f"Next action: {run_payload['next_action']}",
    ]
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
