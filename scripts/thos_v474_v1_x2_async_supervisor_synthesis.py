#!/usr/bin/env python3
"""Build v474 THOS v1 x2 async supervisor synthesis artifacts."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v474-thos-v1-x2"
SOURCE_PHASE = "v474-thos-v1-x1"
NEXT_PHASE = "v474-thos-v2-x1"
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

APP_ADVISORIES = [
    {
        "lane": "Cicero",
        "status": "ADVISORY_RECEIVED",
        "themes": [
            "explicit watcher state machine",
            "summary-only receipts",
            "bounded reason-coded retries",
            "observed/notified/reviewed/published distinction",
            "strict GMUT claim ceiling",
        ],
    },
    {
        "lane": "Kierkegaard",
        "status": "ADVISORY_RECEIVED",
        "themes": [
            "no-rush lanes as bounded care, not proof",
            "supervision as status awareness",
            "retry transport/runtime failures only",
            "privacy and marker-review stop conditions",
            "workflow reliability only",
        ],
    },
    {
        "lane": "Aristotle",
        "status": "ADVISORY_RECEIVED",
        "themes": [
            "watcher/runtime split",
            "async completion receipt fields",
            "negative validation for raw publication",
            "exact staged publication pipeline",
            "no GMUT gate effect",
        ],
    },
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def temp_dir_metadata() -> list[dict[str, Any]]:
    temp_root = Path(os.environ.get("TEMP", "."))
    dirs = sorted(temp_root.glob(f"{SOURCE_PHASE}-*"), key=lambda p: p.stat().st_mtime if p.exists() else 0, reverse=True)
    snapshots: list[dict[str, Any]] = []
    for directory in dirs[:3]:
        files = []
        for child in sorted(directory.glob("*")):
            if child.is_file():
                files.append(
                    {
                        "name": child.name,
                        "size_bytes": child.stat().st_size,
                    }
                )
        snapshots.append(
            {
                "file_count": len(files),
                "files": files,
                "path": "<local_temp_redacted>",
            }
        )
    return snapshots


def row(row_id: str, status: str, message: str, evidence: object | None = None) -> dict[str, Any]:
    return {"evidence": evidence, "message": message, "row_id": row_id, "status": status}


def aggregate(rows: list[dict[str, Any]]) -> str:
    if any(item["status"] == "FAIL_BLOCKER" for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"].startswith("OPEN_GAP") for item in rows):
        return "OPEN_GAP"
    return "PASS_SHAPE_ONLY"


def build_artifacts() -> list[Path]:
    generated_at = utc_now()
    launch = read_json(ARTIFACT_ROOT / f"{SOURCE_PHASE}-no-rush-cli-lane-runtime-launch-v1.json")
    completion = read_json(ARTIFACT_ROOT / f"{SOURCE_PHASE}-cli-lane-completion-notice-v1.json")
    temp_snapshot = temp_dir_metadata()

    watcher_status = "COMPLETION_NOTICE_PRESENT" if completion else "COMPLETION_NOTICE_PENDING"
    launch_status = launch.get("aggregate_status", "MISSING")
    lane_launches = [
        {
            "lane": lane.get("lane"),
            "launcher_returncode": lane.get("launcher_returncode"),
            "execution_status": lane.get("launcher_summary", {}).get("execution_status"),
            "pid_recorded": bool(lane.get("launcher_summary", {}).get("pid")),
            "sandbox": lane.get("launcher_summary", {}).get("sandbox"),
            "ephemeral_flag_used": lane.get("launcher_summary", {}).get("ephemeral_flag_used"),
        }
        for lane in launch.get("lanes", [])
    ]

    receipt_schema = {
        "required_fields": [
            "lane",
            "run_id",
            "start_time_utc",
            "end_time_utc",
            "process_exit_observed",
            "final_message_status",
            "raw_text_retained_temp_only",
            "marker_review_status",
            "redaction_status",
            "summary_ready",
            "retry_reason_code",
            "gmUT_gate_effect",
        ],
        "allowed_status_flow": [
            "not_started",
            "running",
            "process_exit_observed",
            "final_message_ready",
            "marker_review_pending",
            "summary_ready",
            "receipt_curated",
            "timeout_open_gap",
            "failed_with_reason",
        ],
    }

    rows = [
        row(
            "source_launch",
            "PASS_SHAPE_ONLY" if launch_status == "PASS_SHAPE_ONLY_ASYNC_RUNNING" else "OPEN_GAP_SOURCE_LAUNCH",
            "v474 v1 x1 launch receipt is available and summary-only.",
            {"launch_status": launch_status, "lanes": lane_launches},
        ),
        row(
            "cli_completion",
            "OPEN_GAP_COMPLETION_PENDING" if not completion else "PASS_SHAPE_ONLY",
            "CLI completion receipt is pending unless the watcher has produced its summary-only notice.",
            {"watcher_status": watcher_status},
        ),
        row(
            "app_advisory_synthesis",
            "PASS_SHAPE_ONLY",
            "Cicero, Kierkegaard, and Aristotle advisories were synthesized into a stricter supervisor schema.",
            {"advisory_count": len(APP_ADVISORIES)},
        ),
        row(
            "raw_boundary",
            "PASS_SHAPE_ONLY",
            "Only temp metadata and curated receipts are used; raw lane bodies remain unpublished.",
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "The supervisor schema improves THOS workflow hygiene only and does not close GMUT gates.",
        ),
    ]

    synthesis = {
        "aggregate_status": aggregate(rows),
        "app_advisories": APP_ADVISORIES,
        "completion_receipt_status": watcher_status,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "receipt_schema": receipt_schema,
        "recommended_next_tasks": [
            "Implement a repo-only receipt classifier that separates process exit from final-message readiness.",
            "Add reason-coded retry rows for transport failure, timeout, marker review, and user pause.",
            "Keep completion notices summary-only until an exact marker-review clearance packet is present.",
            "Use expected-fail fixtures for raw-output publication attempts.",
        ],
        "rows": rows,
        "source_phase": SOURCE_PHASE,
        "temp_output_metadata": temp_snapshot,
    }

    completion_message = (
        "v1 x2 records a stricter async-supervisor schema and carries CLI completion as marker-review work."
        if completion
        else "v1 x2 records a stricter async-supervisor schema and keeps CLI completion pending as an open gap until the watcher produces a marker-safe completion notice."
    )

    run_status = {
        "aggregate_status": synthesis["aggregate_status"],
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": [
            row("synthesis", synthesis["aggregate_status"], "Async supervisor synthesis was generated."),
            row("next_phase", "PASS_SHAPE_ONLY", "Next expected phase is v474 THOS v2 x1."),
        ],
    }

    written: list[Path] = []
    synthesis_json = ARTIFACT_ROOT / f"{PHASE}-async-supervisor-synthesis-v1.json"
    write_json(synthesis_json, synthesis)
    written.append(synthesis_json)
    synthesis_md = ARTIFACT_ROOT / f"{PHASE}-async-supervisor-synthesis-v1.md"
    write_md(
        synthesis_md,
        f"""
# v474 THOS v1 x2 Async Supervisor Synthesis

Generated UTC: `{generated_at}`

Status: `{synthesis['aggregate_status']}`

v474 v1 x2 synthesizes the no-rush CLI launch receipt with Cicero, Kierkegaard, and Aristotle advisories. The main upgrade is a stricter async receipt model: process exit, final-message readiness, marker review, summary readiness, and publication are separate states.

Completion receipt status: `{watcher_status}`

Raw Arby/Aster lane bodies remain temp-only and unpublished.

All six GMUT gates remain open.
""",
    )
    written.append(synthesis_md)
    status_json = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    write_json(status_json, run_status)
    written.append(status_json)
    status_md = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md"
    write_md(
        status_md,
        f"""
# v474 THOS v1 x2 Run Status

Status: `{run_status['aggregate_status']}`

Next expected phase: `{NEXT_PHASE}`

{completion_message}

All six GMUT gates remain open.
""",
    )
    written.append(status_md)
    return written


def main() -> int:
    for path in build_artifacts():
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
