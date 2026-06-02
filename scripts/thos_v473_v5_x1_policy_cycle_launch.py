#!/usr/bin/env python3
"""Build v473 THOS v5 x1 policy-cycle launch artifacts."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v473-thos-v5-x1"
NEXT_PHASE = "v473-thos-v5-x2"
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


def write_artifacts(args: argparse.Namespace) -> list[Path]:
    generated_at = utc_now()
    policy = read_json("v473-thos-v4-x2-summary-use-policy-v1.json")
    handoff = read_json("v473-thos-v4-x2-v5-handoff-v1.json")

    launch_rows = [
        row("arby_launch", "PASS_SHAPE_ONLY", "Arby launched non-ephemeral read-only.", {"pid_recorded": bool(args.arby_pid)}),
        row("aster_launch", "PASS_SHAPE_ONLY", "Aster Vale launched non-ephemeral read-only.", {"pid_recorded": bool(args.aster_pid)}),
        row("watcher_launch", "PASS_SHAPE_ONLY", "Shell-safe watcher wrapper launched for the policy cycle.", {"pid_recorded": bool(args.watcher_pid)}),
        row("policy_inheritance", policy.get("aggregate_status", "OPEN_GAP"), "v4 x2 summary-use policy is inherited for this cycle."),
        row("raw_boundary", "PASS_SHAPE_ONLY", "Raw lane output remains temp-only and unpublished."),
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
            "receipt_json": "docs/trinity-live-traces/v473-thos-v5-x1-cli-lane-completion-notice-v1.json",
            "receipt_md": "docs/trinity-live-traces/v473-thos-v5-x1-cli-lane-completion-notice-v1.md",
            "script": "scripts/thos_cli_lane_watch_launcher.py",
            "timeout_seconds": args.timeout_seconds,
        },
    }
    written: list[Path] = []
    path = ARTIFACT_ROOT / f"{PHASE}-policy-cycle-launch-receipt-v1.json"
    write_json(path, launch)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-policy-cycle-launch-receipt-v1.md",
        f"""
# v473 THOS v5 x1 Policy-Cycle Launch Receipt

Generated UTC: `{generated_at}`

Status: `{launch['aggregate_status']}`

Arby and Aster Vale were launched through the shell-safe watcher flow to test the v4 x2 summary-use policy on a new no-rush CLI cycle.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-policy-cycle-launch-receipt-v1.md")

    handoff_rows = [
        row("launch", launch["aggregate_status"], "Policy-cycle launch receipt is ready."),
        row("previous_handoff", handoff.get("aggregate_status", "OPEN_GAP"), "v4 x2 handoff is inherited."),
        row("completion_pending", "OPEN_GAP", "v5 x2 should synthesize the watcher completion receipt when it lands."),
        row("claim_boundary", "PASS_SHAPE_ONLY", "All GMUT gates remain open."),
    ]
    run_status = {
        "aggregate_status": aggregate(handoff_rows),
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": handoff_rows,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    write_json(path, run_status)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md",
        f"""
# v473 THOS v5 x1 Run Status

Status: `{run_status['aggregate_status']}`

Next expected phase: `{NEXT_PHASE}`

v5 x1 launched a wrapper-backed Arby/Aster policy cycle. Completion synthesis is pending the watcher receipt.

All six GMUT gates remain open.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md")
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description="Write v473 THOS v5 x1 policy-cycle launch artifacts.")
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
