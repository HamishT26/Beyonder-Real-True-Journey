#!/usr/bin/env python3
"""Build v473 THOS v2 x1 async notifier launch and integration artifacts."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v473-thos-v2-x1"
NEXT_PHASE = "v473-thos-v2-x2"
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


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def read_json(name: str) -> dict[str, Any]:
    path = ARTIFACT_ROOT / name
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def row(row_id: str, status: str, message: str, evidence: object | None = None) -> dict[str, Any]:
    return {"evidence": evidence, "message": message, "row_id": row_id, "status": status}


def aggregate(rows: list[dict[str, Any]]) -> str:
    if any(item["status"] == "FAIL_BLOCKER" for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"] == "OPEN_GAP" for item in rows):
        return "OPEN_GAP"
    return "PASS_SHAPE_ONLY"


def write_artifacts(args: argparse.Namespace) -> list[Path]:
    generated_at = utc_now()
    x1 = read_json("v473-thos-v1-x1-marker-review-classifier-v1.json")
    x2 = read_json("v473-thos-v1-x2-no-rush-cli-notifier-synthesis-v1.json")

    launch_rows = [
        row(
            "arby_launch",
            "PASS_SHAPE_ONLY" if args.arby_pid else "OPEN_GAP",
            "Arby launched as a non-ephemeral read-only CLI advisory lane.",
            {"pid_recorded": bool(args.arby_pid)},
        ),
        row(
            "aster_launch",
            "PASS_SHAPE_ONLY" if args.aster_pid else "OPEN_GAP",
            "Aster Vale launched as a non-ephemeral read-only CLI advisory lane.",
            {"pid_recorded": bool(args.aster_pid)},
        ),
        row(
            "watcher_launch",
            "PASS_SHAPE_ONLY" if args.watcher_pid else "OPEN_GAP",
            "Completion watcher launched as a background helper with a generous timeout.",
            {"pid_recorded": bool(args.watcher_pid), "timeout_seconds": args.timeout_seconds},
        ),
        row(
            "raw_output_boundary",
            "PASS_SHAPE_ONLY",
            "Raw lane output remains in local temp storage and is not published.",
        ),
    ]
    launch = {
        "aggregate_status": aggregate(launch_rows),
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "lanes": [
            {"lane": "Arby", "pid": args.arby_pid, "sandbox": "read-only"},
            {"lane": "Aster Vale", "pid": args.aster_pid, "sandbox": "read-only"},
        ],
        "mutation_performed": False,
        "output_dir": "<local_temp_redacted>",
        "phase_slug": PHASE,
        "rows": launch_rows,
        "watcher": {
            "pid": args.watcher_pid,
            "poll_seconds": args.poll_seconds,
            "receipt_json": "docs/trinity-live-traces/v473-thos-v2-x1-cli-lane-completion-notice-v1.json",
            "receipt_md": "docs/trinity-live-traces/v473-thos-v2-x1-cli-lane-completion-notice-v1.md",
            "script": "scripts/thos_cli_lane_completion_notifier.py",
            "timeout_seconds": args.timeout_seconds,
        },
    }

    written: list[Path] = []
    path = ARTIFACT_ROOT / f"{PHASE}-async-watch-launch-receipt-v1.json"
    write_json(path, launch)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-async-watch-launch-receipt-v1.md",
        f"""
# v473 THOS v2 x1 Async Watch Launch Receipt

Generated UTC: `{generated_at}`

Status: `{launch['aggregate_status']}`

Arby and Aster Vale were launched as non-ephemeral read-only CLI advisory lanes. The watcher is running as a background helper with a `{args.timeout_seconds}` second ceiling and writes only curated completion metadata.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-async-watch-launch-receipt-v1.md")

    integration_rows = [
        row(
            "classifier_inheritance",
            x1.get("aggregate_status", "OPEN_GAP"),
            "v2 inherits the v1 marker-review classifier boundary.",
        ),
        row(
            "notifier_inheritance",
            x2.get("aggregate_status", "OPEN_GAP"),
            "v2 inherits the no-rush notifier workflow and keeps marker review explicit.",
        ),
        row(
            "terminal_states",
            "PASS_SHAPE_ONLY",
            "Watcher terminal states remain final-ready, marker-review-ready, pending, and timeout.",
        ),
        row(
            "summary_use",
            "OPEN_GAP",
            "Raw final advisory text still needs review before summary use in phase artifacts.",
        ),
    ]
    integration = {
        "aggregate_status": aggregate(integration_rows),
        "generated_at_utc": generated_at,
        "phase_slug": PHASE,
        "recommended_contract": [
            "launch lane",
            "watch for final-message readiness",
            "publish metadata receipt only",
            "classify markers",
            "summarize only after review",
        ],
        "rows": integration_rows,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-marker-review-notifier-integration-v1.json"
    write_json(path, integration)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-marker-review-notifier-integration-v1.md",
        """
# v473 THOS v2 x1 Marker-Review Notifier Integration

v2 links the no-rush watcher to the marker-review classifier. Completion receipts may publish metadata immediately; advisory text remains held until marker review clears it for summary use.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-marker-review-notifier-integration-v1.md")

    reachability_rows = [
        row(
            "app_thread_tools",
            "OPEN_GAP",
            "Direct app thread messaging tools were not exposed in this turn, so no new Cicero/Kierkegaard/Aristotle messages were sent.",
        ),
        row(
            "cli_lanes",
            "PASS_SHAPE_ONLY",
            "CLI lanes remain reachable through the non-ephemeral read-only launcher.",
        ),
        row(
            "fabrication_boundary",
            "PASS_SHAPE_ONLY",
            "No app-lane advisory is fabricated when a lane is not callable.",
        ),
    ]
    reachability = {
        "aggregate_status": aggregate(reachability_rows),
        "generated_at_utc": generated_at,
        "phase_slug": PHASE,
        "rows": reachability_rows,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-sibling-reachability-ledger-v1.json"
    write_json(path, reachability)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-sibling-reachability-ledger-v1.md",
        """
# v473 THOS v2 x1 Sibling Reachability Ledger

CLI lanes are reachable and running. App thread messaging tools were not exposed in this turn, so app-lane advisories remain an explicit open gap rather than invented input.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-sibling-reachability-ledger-v1.md")

    status_rows = [
        row("launch", launch["aggregate_status"], "Async watch launch receipt published."),
        row("integration", integration["aggregate_status"], "Marker-review notifier integration remains an open-gap contract."),
        row("reachability", reachability["aggregate_status"], "Sibling reachability boundaries published."),
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
# v473 THOS v2 x1 Run Status

Status: `{run_status['aggregate_status']}`

Next expected phase: `{NEXT_PHASE}`

v2 x1 launched the no-rush Arby/Aster watcher workflow and records app-lane reachability as an explicit open gap.

All six GMUT gates remain open.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md")
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description="Write v473 THOS v2 x1 async notifier integration artifacts.")
    parser.add_argument("--arby-pid", type=int, required=True)
    parser.add_argument("--aster-pid", type=int, required=True)
    parser.add_argument("--watcher-pid", type=int, required=True)
    parser.add_argument("--poll-seconds", type=int, default=60)
    parser.add_argument("--timeout-seconds", type=int, default=72000)
    args = parser.parse_args()

    for path in write_artifacts(args):
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
