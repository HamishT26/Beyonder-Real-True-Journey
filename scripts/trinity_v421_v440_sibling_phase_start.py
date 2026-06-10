#!/usr/bin/env python3
"""Open one bounded v421-v440 Trinity Hybrid v1/v2 phase."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "docs" / "trinity-live-traces"
HANDOFF_JSON = TRACE / "v421-v440-final-handoff-v1.json"
BASE_PLAN_JSON = TRACE / "v421-v440-sibling-base-plan-v1.json"
BASE_PLAN_MD = TRACE / "v421-v440-sibling-base-plan-v1.md"
RUN_STATUS_JSON = TRACE / "v421-v440-sibling-run-status-v1.json"
RUN_STATUS_MD = TRACE / "v421-v440-sibling-run-status-v1.md"
PREVIOUS_CLOSEOUT = TRACE / "v401-v420-closeout-declaration-v1.json"

PHASE_MIN = 421
PHASE_MAX = 440
PHASE_RANGE = "v421-v440"
PLAN_VERSION = 1
V2_MIN_USEFUL_MINUTES = 60
SIBLINGS = [
    "Arby",
    "Kimi",
    "Aster Vale",
    "Supervisor",
    "v2 Watcher",
    "Recovery Watchdog",
    "Parfit",
    "Cicero",
    "Kierkegaard",
]

SYSTEM_TOPICS = [
    "v401-v420 closeout truth",
    "two-pass v1/v2 phase governor",
    "single active run guard",
    "20-minute heartbeat observer",
    "Goal Mode bounded focus contract",
    "CLI receipt gate",
    "App v2 implementation receipt",
    "local-first external policy",
    "multiplex observability boundary",
    "branch drift proof",
    "raw log quarantine",
    "source capsule continuity",
    "curated publication hygiene",
    "v440 stop boundary",
]
COMMAND_TOPICS = [
    "refresh-health-gate",
    "read-v421-v440-handoff",
    "scan-live-v1-runner",
    "run-v1-cli-receipt-gate",
    "start-v2-app-run",
    "complete-v2-app-receipt",
    "write-source-capsule",
    "write-v1-report",
    "write-v2-report",
    "check-stage-boundary",
    "check-branch-drift",
    "publish-forward-only",
    "verify-remote-equals-local",
    "seed-next-phase",
]
SKILL_TOPICS = [
    "handoff_execution",
    "cli_receipt_review",
    "app_v2_execution",
    "artifact_synthesis",
    "watchdog_readiness",
    "source_capsule_update",
    "publication_hygiene",
    "truth_boundary_mapping",
    "goal_mode_contracting",
    "terminal_multiplex_stewardship",
    "external_scope_governance",
    "phase_closeout",
    "advisory_synthesis",
    "next_phase_task_refinement",
]
EUREKA_TOPICS = [
    "v1 proves sibling receipt truth before v2 acts",
    "v2 performs only local-first App execution by default",
    "20-minute heartbeats observe instead of interrupt",
    "Goal Mode focuses work but does not expand authority",
    "multiplex panes are visibility surfaces, not repo authority",
    "forward-only publication protects shared history",
    "curated staging beats broad dirty-tree cleanup",
    "source capsules keep claims anchored",
    "late app advice seeds later work without blocking gates",
    "v440 closeout stops the packet without v441 launch",
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
    stem = f"v421-v440-sibling-phase-v{phase}-start-v1"
    return TRACE / f"{stem}.json", TRACE / f"{stem}.md"


def lead_for_phase(phase: int) -> str:
    return SIBLINGS[(phase - PHASE_MIN) % len(SIBLINGS)]


def generate_entries(prefix: str, phase: int, topics: list[str], target_count: int) -> list[str]:
    repeated = (topics * ((target_count // len(topics)) + 1))[:target_count]
    return [f"v{phase} {prefix} {index:02d}: {topic}" for index, topic in enumerate(repeated, start=1)]


def handoff_ready(handoff: dict[str, Any]) -> bool:
    previous = read_json(PREVIOUS_CLOSEOUT, {})
    return (
        handoff.get("handoff_state") == "ready_for_v421_v440"
        and handoff.get("target_phase_range") == PHASE_RANGE
        and previous.get("status") == "v401_v420_complete"
        and 420 in (previous.get("v401_v420_completed_phases") or [])
    )


def build_phase_plan(phase: int, handoff: dict[str, Any]) -> dict[str, Any]:
    lead = lead_for_phase(phase)
    next_phase = phase + 1 if phase < PHASE_MAX else None
    phase_goal = (
        f"Complete v{phase} v1 CLI receipts, then complete v{phase} v2 App execution and open v{next_phase}."
        if next_phase
        else "Complete v440 v1/v2, write v421-v440 closeout, and stop without opening v441."
    )
    omega = (
        f"{lead} hands off v{next_phase} after both gates pass."
        if next_phase
        else f"{lead} closes v421-v440 at v440 without v441 launch."
    )
    return {
        "phase": phase,
        "mode": "v421-v440 Trinity Hybrid v1/v2 Beta-Alpha-Omega",
        "plan_version": PLAN_VERSION,
        "lead_sibling": lead,
        "supporting_siblings": [item for item in SIBLINGS if item != lead],
        "source_dependency": rel(HANDOFF_JSON),
        "phase_runs": {
            "v1": "Arby, Kimi, and Aster Vale produce valid CLI receipt evidence.",
            "v2": "Aletheon leads App-side local-first execution with Parfit, Cicero, and Kierkegaard advisory input when available.",
        },
        "beta": f"{lead} verifies closeout truth, active-run identity, terminal root, and v1/v2 boundary for v{phase}.",
        "alpha": f"{lead} coordinates v1 receipt evidence, v2 local-first App execution, reports, and publication hygiene.",
        "omega": omega,
        "goal_mode": {
            "enabled": True,
            "packet_goal": "Complete v421-v440 as 20 numbered phases with v1 CLI receipts and v2 App execution for each phase.",
            "phase_goal": phase_goal,
            "slash_goal_policy": "Use Goal Mode as a bounded focus contract; never collapse phases or bypass receipt gates.",
        },
        "heartbeat": {
            "minutes": 20,
            "policy": "Observe active work, refresh durable state, and avoid duplicate launch or interruption.",
        },
        "external_policy": {
            "default": "local_first_only",
            "allowed": ["repo inspection", "local scripts", "local browser probing", "GitHub publication already covered by git remote", "Codex Security style local checks"],
            "requires_new_scope": ["Notion writes", "Google Drive writes", "cloud/provider mutation", "paid external actions", "account mutation"],
        },
        "terminal_profile": {
            "required_root": "D:\\GHC-Archives\\worktrees\\v58-omega",
            "shell": "PowerShell",
            "authority": "Integrated PowerShell is authoritative; multiplex/TUI panes are observability unless explicitly promoted.",
        },
        "advisory_refinement": {
            "advisors": ["Parfit", "Cicero", "Kierkegaard"],
            "status": "advisory_only",
            "proposal_target_eureka_tasks": 100,
            "late_reply_policy": "Late advisory replies can seed later phases, but cannot block or replace v1/v2 gates.",
        },
        "system_expansions": generate_entries("system", phase, SYSTEM_TOPICS, 40),
        "commands": generate_entries("command", phase, COMMAND_TOPICS, 40),
        "skills": generate_entries("skill", phase, SKILL_TOPICS, 40),
        "eureka_proposals": generate_entries("eureka", phase, EUREKA_TOPICS, 100),
    }


def ensure_base_plan() -> dict[str, Any]:
    existing = read_json(BASE_PLAN_JSON, {})
    if existing.get("status") == "ready_after_v401_v420_closeout" and existing.get("plan_version") == PLAN_VERSION:
        return existing
    handoff = read_json(HANDOFF_JSON, {})
    plans = [build_phase_plan(phase, handoff) for phase in range(PHASE_MIN, PHASE_MAX + 1)]
    ready = handoff_ready(handoff)
    payload = {
        "generated_utc": now_iso(),
        "phase_range": PHASE_RANGE,
        "plan_version": PLAN_VERSION,
        "status": "ready_after_v401_v420_closeout" if ready else "blocked_missing_v421_v440_handoff",
        "handoff": rel(HANDOFF_JSON),
        "numbered_phase_count": PHASE_MAX - PHASE_MIN + 1,
        "phase_run_count": (PHASE_MAX - PHASE_MIN + 1) * 2,
        "phase_plans": plans,
        "truth_boundaries": [
            "v421-v440 starts only from the committed v401-v420 closeout.",
            "Each numbered phase has a v1 CLI gate and v2 App execution gate.",
            "Heartbeats are observation checkpoints and must not duplicate active work.",
            "Goal Mode is a focus contract, not permission to skip validation.",
            "Local-first external policy is active until a new explicit scope says otherwise.",
            "Do not stage raw replies, stdout/stderr logs, live logs, scratch probes, pycache files, secrets, or unrelated churn.",
            "Stop after v440 closeout and do not open v441.",
        ],
    }
    write_json(BASE_PLAN_JSON, payload)
    lines = [
        "# v421-v440 Sibling Base Plan",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        f"Numbered phases: `{payload['numbered_phase_count']}`",
        f"Phase-runs: `{payload['phase_run_count']}`",
        "",
        "Phase leads:",
    ]
    lines.extend([f"- `v{plan['phase']}`: {plan['lead_sibling']}" for plan in plans])
    lines.extend(["", "Truth boundaries:", *[f"- {item}" for item in payload["truth_boundaries"]]])
    BASE_PLAN_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return payload


def build_payload(phase: int, force: bool) -> dict[str, Any]:
    validate_phase(phase)
    handoff = read_json(HANDOFF_JSON, {})
    base_plan = ensure_base_plan()
    plan = next((item for item in base_plan.get("phase_plans", []) if int(item.get("phase", -1)) == phase), {})
    ready = handoff_ready(handoff) and base_plan.get("status") == "ready_after_v401_v420_closeout"
    blockers: list[str] = []
    if not ready and not force:
        blockers.append("v421-v440 handoff is not ready from v401-v420 closeout")
    if not plan:
        blockers.append(f"phase v{phase} is missing from the v421-v440 base plan")
    status = "phase_started" if (ready or force) and plan else "blocked"
    return {
        "generated_utc": now_iso(),
        "phase_range": PHASE_RANGE,
        "phase": phase,
        "status": status,
        "active_run": "v1_cli_receipts",
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
            f"This artifact starts v{phase}; it does not mark v{phase} v1 or v2 complete.",
            "Real v1 CLI receipts are required from Arby, Kimi, and Aster Vale before v2 starts.",
            "Aletheon-led v2 App execution requires its own durable receipt before phase completion.",
            "Integrated PowerShell must stay rooted at D:\\GHC-Archives\\worktrees\\v58-omega before runner or git actions.",
            "Goal Mode guides bounded work but does not authorize duplicate runners or cross-phase collapse.",
            "External services remain local-first/read-only unless a fresh explicit scope says otherwise.",
        ],
        "next_action": (
            f"Run scripts/trinity_v421_v440_cli_sibling_phase_runner.py --phase {phase} --background --timeout-sec 86400 --kimi-timeout-sec 86400 --max-steps 10000."
            if status == "phase_started"
            else "Resolve blockers before starting v421-v440 execution."
        ),
    }


def write_phase_md(path: Path, payload: dict[str, Any]) -> None:
    plan = payload.get("phase_plan") or {}
    lines = [
        f"# v{payload['phase']} Sibling Phase Start",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        f"Active run: `{payload['active_run']}`",
        f"Lead sibling: `{plan.get('lead_sibling')}`",
        "",
        "Beta / Alpha / Omega:",
        f"- Beta: {plan.get('beta')}",
        f"- Alpha: {plan.get('alpha')}",
        f"- Omega: {plan.get('omega')}",
        "",
        "Truth boundaries:",
        *[f"- {item}" for item in payload["truth_boundaries"]],
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
        "active_run": payload["active_run"],
        "active_phase_status": payload["status"],
        "active_phase_artifacts": {"json": rel(phase_json), "md": rel(phase_md)},
        "last_completion": None,
        "closeout_declaration": None,
        "next_action": payload["next_action"],
    }
    write_json(RUN_STATUS_JSON, run_payload)
    lines = [
        "# v421-v440 Sibling Run Status",
        "",
        f"Generated UTC: `{run_payload['generated_utc']}`",
        f"Status: `{run_payload['status']}`",
        f"Active phase: `v{run_payload['active_phase']}`",
        f"Active run: `{run_payload['active_run']}`",
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
