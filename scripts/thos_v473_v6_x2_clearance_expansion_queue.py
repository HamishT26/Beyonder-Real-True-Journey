#!/usr/bin/env python3
"""Build v473 THOS v6 x2 clearance and expansion queue artifacts."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v473-thos-v6-x2"
NEXT_PHASE = "v473-thos-v7-x1"
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

DOMAINS = [
    "watcher",
    "launcher",
    "receipt",
    "review",
    "summary",
    "backlog",
    "scheduler",
    "sandbox",
    "staging",
    "validation",
    "app-lane",
    "cli-lane",
    "github",
    "drive",
    "powershell",
    "skill-surface",
    "command-surface",
    "artifact",
    "handoff",
    "claim-boundary",
    "gmUT-support",
    "thos-runtime",
    "mcp-routing",
    "plugin-boundary",
    "quota-ledger",
    "worktree",
    "diff-review",
    "json-parse",
    "whitespace",
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


def expansion_rows(prefix: str, kind: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, domain in enumerate(DOMAINS, start=1):
        rows.append(
            {
                "domain": domain,
                "id": f"{prefix}-{index:02d}",
                "implementation_status": "DESIGN_READY_NOT_INSTALLED",
                "kind": kind,
                "name": f"{domain}-{kind}-v473",
                "safe_scope": "repo_artifact_or_script_only",
                "summary": f"Advance {domain} reliability through a bounded THOS {kind} proposal.",
            }
        )
    return rows


def clearance_row(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "clearance_status": "NOT_CLEARED",
        "current_allowed_use": item.get("allowed_current_use"),
        "current_blocked_use": item.get("blocked_current_use"),
        "final_message_hash": item.get("final_message_hash"),
        "lane": item.get("lane"),
        "marker_count": item.get("marker_count"),
        "required_clearance_artifact": "future_exact_review_summary_or_classifier_clearance",
        "review_need": item.get("review_need"),
    }


def write_artifacts() -> list[Path]:
    generated_at = utc_now()
    backlog = read_json("v473-thos-v6-x1-held-lane-review-backlog-v1.json")
    held = [clearance_row(item) for item in backlog.get("backlog", [])]
    systems = expansion_rows("system", "system-expansion")
    commands = expansion_rows("command", "command")
    skills = expansion_rows("skill", "skill")

    clearance_rows = [
        row("backlog_source", backlog.get("aggregate_status", "OPEN_GAP"), "Clearance source is v6 x1 held-lane backlog metadata."),
        row("held_lanes", "OPEN_GAP" if held else "PASS_SHAPE_ONLY", "Held lanes remain uncleared until a separate exact review artifact exists.", {"held_count": len(held)}),
        row("raw_boundary", "PASS_SHAPE_ONLY", "No raw final advisory text is read, summarized, or published."),
        row("claim_boundary", "PASS_SHAPE_ONLY", "Clearance status does not affect GMUT gates."),
    ]
    clearance = {
        "aggregate_status": aggregate(clearance_rows),
        "clearance_rows": held,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "phase_slug": PHASE,
        "rows": clearance_rows,
    }

    written: list[Path] = []
    path = ARTIFACT_ROOT / f"{PHASE}-held-lane-clearance-ledger-v1.json"
    write_json(path, clearance)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-held-lane-clearance-ledger-v1.md",
        f"""
# v473 THOS v6 x2 Held-Lane Clearance Ledger

Generated UTC: `{generated_at}`

Status: `{clearance['aggregate_status']}`

Held lanes remain uncleared: `{', '.join(item['lane'] for item in held) if held else 'none'}`.

No raw final advisory text was read or published.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-held-lane-clearance-ledger-v1.md")

    expansion_rows_status = [
        row("system_expansions", "PASS_SHAPE_ONLY", "Thirty THOS system-expansion proposals are defined.", {"count": len(systems)}),
        row("commands", "PASS_SHAPE_ONLY", "Thirty THOS command proposals are defined.", {"count": len(commands)}),
        row("skills", "PASS_SHAPE_ONLY", "Thirty THOS skill proposals are defined.", {"count": len(skills)}),
        row("install_boundary", "OPEN_GAP", "The queue is design-ready only; no plugin cache or user skill install is performed in this phase."),
    ]
    expansion = {
        "aggregate_status": aggregate(expansion_rows_status),
        "commands": commands,
        "generated_at_utc": generated_at,
        "phase_slug": PHASE,
        "rows": expansion_rows_status,
        "skills": skills,
        "system_expansions": systems,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-thos-30-30-30-expansion-queue-v1.json"
    write_json(path, expansion)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-thos-30-30-30-expansion-queue-v1.md",
        f"""
# v473 THOS v6 x2 30-30-30 Expansion Queue

Generated UTC: `{generated_at}`

Status: `{expansion['aggregate_status']}`

Defined: `30` system-expansion proposals, `30` command proposals, and `30` skill proposals.

The queue is design-ready only; no plugin cache or user skill install is performed here.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-thos-30-30-30-expansion-queue-v1.md")

    handoff_rows = [
        row("clearance", clearance["aggregate_status"], "Held lanes remain uncleared and metadata-only."),
        row("expansion_queue", expansion["aggregate_status"], "30-30-30 THOS queue is ready for v7 routing."),
        row("app_lanes", "OPEN_GAP", "App-lane advisory payloads are still unavailable in this phase."),
    ]
    handoff = {
        "aggregate_status": aggregate(handoff_rows),
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "recommended_tasks": [
            "Route the 30-30-30 queue into a smaller executable v7 subset.",
            "Do not install skill or plugin-cache changes without a new exact approval packet.",
            "Keep held lanes metadata-only until a future exact review artifact clears them.",
            "Continue wrapper-backed CLI cycles only through curated receipts.",
        ],
        "rows": handoff_rows,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-v7-handoff-v1.json"
    write_json(path, handoff)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-v7-handoff-v1.md",
        f"""
# v473 THOS v6 x2 to v7 Handoff

Status: `{handoff['aggregate_status']}`

Next expected phase: `{NEXT_PHASE}`

v7 should route the 30-30-30 design queue into a bounded executable subset while keeping held lanes metadata-only.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-v7-handoff-v1.md")

    status_rows = [
        row("clearance", clearance["aggregate_status"], "Held-lane clearance ledger published."),
        row("queue", expansion["aggregate_status"], "30-30-30 expansion queue published."),
        row("handoff", handoff["aggregate_status"], "v7 handoff published."),
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
# v473 THOS v6 x2 Run Status

Status: `{run_status['aggregate_status']}`

Next expected phase: `{NEXT_PHASE}`

v6 x2 publishes held-lane clearance status and a 30-30-30 THOS expansion queue.

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
