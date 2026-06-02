#!/usr/bin/env python3
"""Build v473 THOS v6 x1 held-lane review backlog artifacts."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v473-thos-v6-x1"
NEXT_PHASE = "v473-thos-v6-x2"
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


def backlog_item(decision: dict[str, Any]) -> dict[str, Any] | None:
    if decision.get("action") == "ALLOW_METADATA_SUMMARY":
        return None
    return {
        "allowed_current_use": "metadata_counts_hashes_only",
        "blocked_current_use": "raw_text_or_advisory_summary",
        "final_message_hash": decision.get("final_message_hash"),
        "lane": decision.get("lane"),
        "marker_count": decision.get("marker_count"),
        "review_need": "manual_or_classifier_clearance",
        "source_status": decision.get("action"),
    }


def write_artifacts() -> list[Path]:
    generated_at = utc_now()
    completion = read_json("v473-thos-v5-x2-policy-cycle-completion-v1.json")
    decisions = completion.get("decisions", [])
    backlog = [item for item in (backlog_item(decision) for decision in decisions) if item]
    lanes = [item["lane"] for item in backlog]

    backlog_rows = [
        row("source_completion", completion.get("aggregate_status", "OPEN_GAP"), "Backlog source is the v5 x2 policy-cycle completion artifact."),
        row("held_lanes", "OPEN_GAP" if backlog else "PASS_SHAPE_ONLY", "Held lanes require review before raw-text or advisory-summary use.", {"lanes": lanes}),
        row("metadata_boundary", "PASS_SHAPE_ONLY", "Only metadata counts, byte sizes, and hashes may be used before review clearance."),
        row("claim_boundary", "PASS_SHAPE_ONLY", "Backlog status does not affect GMUT gates."),
    ]
    backlog_payload = {
        "aggregate_status": aggregate(backlog_rows),
        "backlog": backlog,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "phase_slug": PHASE,
        "rows": backlog_rows,
    }
    written: list[Path] = []
    path = ARTIFACT_ROOT / f"{PHASE}-held-lane-review-backlog-v1.json"
    write_json(path, backlog_payload)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-held-lane-review-backlog-v1.md",
        f"""
# v473 THOS v6 x1 Held-Lane Review Backlog

Generated UTC: `{generated_at}`

Status: `{backlog_payload['aggregate_status']}`

Held lanes: `{', '.join(lanes) if lanes else 'none'}`

Until cleared, only metadata counts and hashes may be used.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-held-lane-review-backlog-v1.md")

    protocol_rows = [
        row("intake", "PASS_SHAPE_ONLY", "Create one backlog row per held lane from policy decisions."),
        row("review", "OPEN_GAP" if backlog else "PASS_SHAPE_ONLY", "A held lane needs separate review clearance before summary use."),
        row("publication", "PASS_SHAPE_ONLY", "Publish only counts, hashes, statuses, and review decisions."),
        row("reuse", "PASS_SHAPE_ONLY", "Apply this protocol to later wrapper-backed cycles."),
    ]
    protocol = {
        "aggregate_status": aggregate(protocol_rows),
        "generated_at_utc": generated_at,
        "phase_slug": PHASE,
        "protocol_steps": [
            "read completion receipt metadata",
            "apply summary-use policy",
            "create held-lane backlog rows",
            "withhold raw advisory summary",
            "publish only safe metadata and next action",
        ],
        "rows": protocol_rows,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-review-backlog-protocol-v1.json"
    write_json(path, protocol)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-review-backlog-protocol-v1.md",
        """
# v473 THOS v6 x1 Review Backlog Protocol

The protocol converts held policy decisions into explicit review backlog rows and keeps raw advisory text out of publication.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-review-backlog-protocol-v1.md")

    status_rows = [
        row("backlog", backlog_payload["aggregate_status"], "Held-lane backlog published."),
        row("protocol", protocol["aggregate_status"], "Review backlog protocol published."),
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
# v473 THOS v6 x1 Run Status

Status: `{run_status['aggregate_status']}`

Next expected phase: `{NEXT_PHASE}`

v6 x1 publishes a held-lane review backlog and protocol for summary-use clearance.

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
