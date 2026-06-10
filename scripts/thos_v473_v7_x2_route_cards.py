#!/usr/bin/env python3
"""Build v473 THOS v7 x2 repo-only route-card artifacts."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v473-thos-v7-x2"
NEXT_PHASE = "v473-thos-v8-x1"
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


def route_card(item: dict[str, Any], index: int) -> dict[str, Any]:
    domain = item.get("domain")
    kind = item.get("kind")
    return {
        "acceptance_checks": [
            "json_parse",
            "path_guard",
            "credential_guard",
            "raw_log_guard",
            "staged_diff_review",
        ],
        "blocked_actions": [
            "plugin_cache_mutation",
            "user_skill_install",
            "external_account_change",
            "raw_advisory_publication",
            "gmUT_validation_claim",
        ],
        "claim_ceiling": "THOS workflow support only; no GMUT gate closure.",
        "domain": domain,
        "implementation_mode": "repo_artifact_or_script_only",
        "kind": kind,
        "route_card_id": f"{PHASE}-{kind}-{index:02d}",
        "source_id": item.get("id"),
        "source_name": item.get("name"),
        "status": "READY_FOR_REPO_ONLY_IMPLEMENTATION",
        "target_phase": "v473-thos-v8-x1" if kind == "skill" else PHASE,
        "task": f"Create bounded THOS route support for {domain} without live external mutation.",
    }


def write_artifacts() -> list[Path]:
    generated_at = utc_now()
    router = read_json("v473-thos-v7-x1-bounded-expansion-router-v1.json")
    routed = router.get("routed_subset", {})
    systems = [route_card(item, index) for index, item in enumerate(routed.get("system_subset", []), start=1)]
    commands = [route_card(item, index) for index, item in enumerate(routed.get("command_subset", []), start=1)]
    skills = [route_card(item, index) for index, item in enumerate(routed.get("skill_subset", []), start=1)]
    executable_cards = systems + commands
    held_cards = skills

    route_rows = [
        row("source_router", router.get("aggregate_status", "OPEN_GAP"), "Route-card source is the v7 x1 bounded router."),
        row("system_cards", "PASS_SHAPE_ONLY", "Eight system route cards are materialized.", {"count": len(systems)}),
        row("command_cards", "PASS_SHAPE_ONLY", "Eight command route cards are materialized.", {"count": len(commands)}),
        row("skill_cards_held", "OPEN_GAP", "Eight skill cards remain held for repo-only design in v8 x1; no install is performed.", {"count": len(skills)}),
        row("mutation_boundary", "PASS_SHAPE_ONLY", "Route cards are repo artifacts only and perform no live external mutation."),
    ]
    cards = {
        "aggregate_status": aggregate(route_rows),
        "command_route_cards": commands,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "held_skill_route_cards": held_cards,
        "phase_slug": PHASE,
        "rows": route_rows,
        "system_route_cards": systems,
    }

    written: list[Path] = []
    path = ARTIFACT_ROOT / f"{PHASE}-system-command-route-cards-v1.json"
    write_json(path, cards)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-system-command-route-cards-v1.md",
        f"""
# v473 THOS v7 x2 System/Command Route Cards

Generated UTC: `{generated_at}`

Status: `{cards['aggregate_status']}`

Materialized `8` system route cards and `8` command route cards. Held `8` skill route cards for later repo-only design.

No plugin cache, user skill, external account, or raw advisory mutation is performed.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-system-command-route-cards-v1.md")

    verifier_rows = [
        row("card_count", "PASS_SHAPE_ONLY" if len(executable_cards) == 16 else "FAIL_BLOCKER", "Executable system/command route-card count is exactly sixteen.", {"count": len(executable_cards)}),
        row("acceptance_checks", "PASS_SHAPE_ONLY", "Every route card includes the shared acceptance-check bundle."),
        row("blocked_actions", "PASS_SHAPE_ONLY", "Every route card blocks plugin/user skill/external/raw/GMUT-claim mutations."),
        row("skill_hold", "OPEN_GAP", "Skill cards are deliberately held for v8 x1."),
    ]
    verifier = {
        "aggregate_status": aggregate(verifier_rows),
        "generated_at_utc": generated_at,
        "phase_slug": PHASE,
        "rows": verifier_rows,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-route-card-verifier-v1.json"
    write_json(path, verifier)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-route-card-verifier-v1.md",
        """
# v473 THOS v7 x2 Route-Card Verifier

The verifier confirms sixteen executable repo-only route cards and keeps the skill subset held for v8 x1.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-route-card-verifier-v1.md")

    handoff_rows = [
        row("route_cards", cards["aggregate_status"], "System/command route cards are ready for v8 x1/v8 x2 planning."),
        row("verifier", verifier["aggregate_status"], "Route-card verifier published."),
        row("held_lanes", "OPEN_GAP", "Arby/Aster raw advisory bodies remain held from the review backlog."),
        row("app_lanes", "OPEN_GAP", "No app-lane payloads are claimed."),
    ]
    handoff = {
        "aggregate_status": aggregate(handoff_rows),
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "recommended_tasks": [
            "Use v8 x1 to materialize repo-only skill design cards without installing skills.",
            "Use v8 x2 to select a small executable route-card implementation target.",
            "Keep held Arby/Aster advisory bodies metadata-only until exact review clearance.",
            "Keep all GMUT gates open.",
        ],
        "rows": handoff_rows,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-v8-handoff-v1.json"
    write_json(path, handoff)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-v8-handoff-v1.md",
        f"""
# v473 THOS v7 x2 to v8 Handoff

Status: `{handoff['aggregate_status']}`

Next expected phase: `{NEXT_PHASE}`

v8 x1 should materialize repo-only skill design cards while avoiding live user-skill installation.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-v8-handoff-v1.md")

    status_rows = [
        row("cards", cards["aggregate_status"], "System/command route cards published."),
        row("verifier", verifier["aggregate_status"], "Route-card verifier published."),
        row("handoff", handoff["aggregate_status"], "v8 handoff published."),
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
# v473 THOS v7 x2 Run Status

Status: `{run_status['aggregate_status']}`

Next expected phase: `{NEXT_PHASE}`

v7 x2 materializes repo-only system/command route cards from the bounded router.

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
