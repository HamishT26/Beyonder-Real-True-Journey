#!/usr/bin/env python3
"""Build v473 THOS v8 x2 closure audit and v474 handoff artifacts."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v473-thos-v8-x2"
NEXT_PHASE = "v474-thos-v1-x1"
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

PHASE_ARTIFACTS = [
    "v473-thos-v3-x2-wrapper-live-completion-synthesis-v1.json",
    "v473-thos-v4-x2-summary-use-policy-v1.json",
    "v473-thos-v5-x2-policy-cycle-completion-v1.json",
    "v473-thos-v6-x2-thos-30-30-30-expansion-queue-v1.json",
    "v473-thos-v7-x2-system-command-route-cards-v1.json",
    "v473-thos-v8-x1-repo-only-skill-design-cards-v1.json",
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


def artifact_summary() -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    for name in PHASE_ARTIFACTS:
        data = read_json(name)
        summaries.append(
            {
                "aggregate_status": data.get("aggregate_status", "MISSING"),
                "artifact": name,
                "exists": bool(data),
                "phase_slug": data.get("phase_slug"),
            }
        )
    return summaries


def write_artifacts() -> list[Path]:
    generated_at = utc_now()
    summaries = artifact_summary()
    missing = [item["artifact"] for item in summaries if not item["exists"]]
    open_artifacts = [item["artifact"] for item in summaries if item["aggregate_status"] == "OPEN_GAP"]

    closure_rows = [
        row("artifact_inventory", "PASS_SHAPE_ONLY" if not missing else "FAIL_BLOCKER", "Required v473 THOS milestone artifacts are present.", {"missing": missing}),
        row("open_gaps", "OPEN_GAP" if open_artifacts else "PASS_SHAPE_ONLY", "Several artifacts intentionally carry open gaps for marker review, app payloads, and install approval.", {"open_count": len(open_artifacts)}),
        row("raw_boundary", "PASS_SHAPE_ONLY", "Raw CLI lane output, transport logs, session material, visual captures, and credential material remain unpublished."),
        row("install_boundary", "PASS_SHAPE_ONLY", "No user skill or plugin-cache installation was performed."),
        row("claim_boundary", "PASS_SHAPE_ONLY", "All GMUT gates remain open and THOS evidence does not validate GMUT."),
    ]
    closure = {
        "aggregate_status": aggregate(closure_rows),
        "artifact_summaries": summaries,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "phase_slug": PHASE,
        "rows": closure_rows,
    }
    written: list[Path] = []
    path = ARTIFACT_ROOT / f"{PHASE}-closure-audit-v1.json"
    write_json(path, closure)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-closure-audit-v1.md",
        f"""
# v473 THOS v8 x2 Closure Audit

Generated UTC: `{generated_at}`

Status: `{closure['aggregate_status']}`

v473 THOS produced watcher, summary-use, review-backlog, 30-30-30 queue, route-card, and repo-only skill-design artifacts. Open gaps remain intentional: marker review, app-lane payloads, and install approval.

All six GMUT gates remain open.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-closure-audit-v1.md")

    handoff_rows = [
        row("next_phase", "PASS_SHAPE_ONLY", "Next expected phase is v474 THOS v1 x1.", {"next_phase": NEXT_PHASE}),
        row("priority_1", "OPEN_GAP", "Review backlog remains uncleared for Arby/Aster held lanes."),
        row("priority_2", "OPEN_GAP", "App-lane advisories remain unavailable and should be retried without fabrication."),
        row("priority_3", "OPEN_GAP", "Skill installation remains out of scope without exact approval."),
        row("priority_4", "PASS_SHAPE_ONLY", "Use repo-only route cards as the next implementation substrate."),
    ]
    handoff = {
        "aggregate_status": aggregate(handoff_rows),
        "generated_at_utc": generated_at,
        "gmUT_gates_open": GMUT_GATES,
        "next_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "recommended_tasks": [
            "v474 v1 x1: route one small repo-only implementation slice from the v7/v8 route cards.",
            "Retry app-lane collection once, but keep no-payload states explicit.",
            "Keep held Arby/Aster lane bodies metadata-only until exact review clearance.",
            "Do not mutate user skills, plugin cache, external accounts, or raw logs without exact approval.",
        ],
        "rows": handoff_rows,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-v474-handoff-v1.json"
    write_json(path, handoff)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-v474-handoff-v1.md",
        f"""
# v473 THOS v8 x2 to v474 Handoff

Status: `{handoff['aggregate_status']}`

Next expected phase: `{NEXT_PHASE}`

v474 should start with a small repo-only implementation slice selected from the route-card artifacts, while preserving the marker-review and install-approval boundaries.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-v474-handoff-v1.md")

    status_rows = [
        row("closure", closure["aggregate_status"], "v473 THOS closure audit published."),
        row("handoff", handoff["aggregate_status"], "v474 handoff published."),
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
# v473 THOS v8 x2 Run Status

Status: `{run_status['aggregate_status']}`

Next expected phase: `{NEXT_PHASE}`

v8 x2 closes the v473 THOS sequence with an audit and handoff. This is not goal completion; the broader v490 objective remains active.

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
