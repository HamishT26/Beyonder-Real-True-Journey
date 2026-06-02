#!/usr/bin/env python3
"""Build v473 THOS v7 x1 bounded queue-routing artifacts."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v473-thos-v7-x1"
NEXT_PHASE = "v473-thos-v7-x2"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

PRIORITY_DOMAINS = [
    "watcher",
    "launcher",
    "receipt",
    "review",
    "summary",
    "backlog",
    "validation",
    "remote-verify",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(name: str) -> dict[str, Any]:
    path = ARTIFACT_ROOT / name
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def row(row_id: str, status: str, message: str, evidence: object | None = None) -> dict[str, Any]:
    return {"evidence": evidence, "message": message, "row_id": row_id, "status": status}


def aggregate(rows: list[dict[str, Any]]) -> str:
    if any(item["status"] == "FAIL_BLOCKER" for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"] == "OPEN_GAP" for item in rows):
        return "OPEN_GAP"
    return "PASS_SHAPE_ONLY"


def select_items(items: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for domain in PRIORITY_DOMAINS:
        for item in items:
            if item.get("domain") == domain:
                selected.append(item)
                break
        if len(selected) == limit:
            break
    return selected


def routed_item(item: dict[str, Any], phase_slot: str) -> dict[str, Any]:
    return {
        "domain": item.get("domain"),
        "id": item.get("id"),
        "kind": item.get("kind"),
        "name": item.get("name"),
        "phase_slot": phase_slot,
        "route_status": "READY_FOR_REPO_ONLY_IMPLEMENTATION",
        "safe_scope": item.get("safe_scope"),
        "summary": item.get("summary"),
    }


def write_artifacts() -> list[Path]:
    generated_at = utc_now()
    queue = read_json("v473-thos-v6-x2-thos-30-30-30-expansion-queue-v1.json")
    systems = select_items(queue.get("system_expansions", []), 8)
    commands = select_items(queue.get("commands", []), 8)
    skills = select_items(queue.get("skills", []), 8)
    routed = {
        "command_subset": [routed_item(item, "v7-x2-command") for item in commands],
        "skill_subset": [routed_item(item, "v8-x1-skill") for item in skills],
        "system_subset": [routed_item(item, "v7-x2-system") for item in systems],
    }
    total_selected = sum(len(items) for items in routed.values())

    routing_rows = [
        row("source_queue", queue.get("aggregate_status", "OPEN_GAP"), "Routing source is the v6 x2 30-30-30 design queue."),
        row("bounded_subset", "PASS_SHAPE_ONLY", "Twenty-four items were selected for bounded repo-only implementation routing.", {"selected": total_selected}),
        row("install_boundary", "OPEN_GAP", "No plugin cache, user skill, or external account mutation is performed by routing."),
        row("claim_boundary", "PASS_SHAPE_ONLY", "Routing supports THOS workflow only and does not affect GMUT gates."),
    ]
    routing = {
        "aggregate_status": aggregate(routing_rows),
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "phase_slug": PHASE,
        "priority_domains": PRIORITY_DOMAINS,
        "routed_subset": routed,
        "rows": routing_rows,
    }

    written: list[Path] = []
    path = ARTIFACT_ROOT / f"{PHASE}-bounded-expansion-router-v1.json"
    write_json(path, routing)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-bounded-expansion-router-v1.md",
        f"""
# v473 THOS v7 x1 Bounded Expansion Router

Generated UTC: `{generated_at}`

Status: `{routing['aggregate_status']}`

Selected `24` repo-only implementation candidates from the v6 x2 30-30-30 queue.

No plugin cache, user skill, or external account mutation is performed here.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-bounded-expansion-router-v1.md")

    execution_rows = [
        row("v7_x2_systems", "PASS_SHAPE_ONLY", "System and command subsets should be handled in v7 x2.", {"system_count": len(systems), "command_count": len(commands)}),
        row("v8_x1_skills", "OPEN_GAP", "Skill subset is held for later repo-only design or a separate exact approval for installation.", {"skill_count": len(skills)}),
        row("held_lanes", "OPEN_GAP", "Held Arby/Aster advisory bodies remain unavailable for content summary."),
    ]
    execution = {
        "aggregate_status": aggregate(execution_rows),
        "generated_at_utc": generated_at,
        "phase_slug": PHASE,
        "rows": execution_rows,
        "safe_execution_order": [
            "v7 x2: repo-only system and command route cards",
            "v8 x1: repo-only skill design route cards",
            "future exact approval only: user skill or plugin cache install",
        ],
    }
    path = ARTIFACT_ROOT / f"{PHASE}-safe-execution-order-v1.json"
    write_json(path, execution)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-safe-execution-order-v1.md",
        """
# v473 THOS v7 x1 Safe Execution Order

v7 x2 should implement repo-only route cards for the selected system and command items. Skill installation remains out of scope without a separate exact approval.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-safe-execution-order-v1.md")

    status_rows = [
        row("routing", routing["aggregate_status"], "Bounded expansion router published."),
        row("execution_order", execution["aggregate_status"], "Safe execution order published."),
    ]
    run_status = {
        "aggregate_status": aggregate(status_rows),
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": status_rows,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    write_json(path, run_status)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md",
        f"""
# v473 THOS v7 x1 Run Status

Status: `{run_status['aggregate_status']}`

Next expected phase: `{NEXT_PHASE}`

v7 x1 routes the v6 x2 30-30-30 queue into a bounded repo-only implementation subset.

All six GMUT gates remain open.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md")
    return written


def main() -> int:
    for path in write_artifacts():
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
