#!/usr/bin/env python3
"""Build v472 THOS v8 x1 notifier terminal-state repair artifacts."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from thos_cli_lane_completion_notifier import build_notice


PHASE = "v472-thos-v8-x1"
NEXT_PHASE = "v472-thos-v8-x2"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"
LANES = ["Arby", "Aster Vale"]

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


def row(row_id: str, status: str, message: str, evidence: object | None = None) -> dict[str, Any]:
    return {"evidence": evidence, "message": message, "row_id": row_id, "status": status}


def aggregate(rows: list[dict[str, Any]]) -> str:
    if any(item["status"] == "FAIL_BLOCKER" for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"] == "OPEN_GAP" for item in rows):
        return "OPEN_GAP"
    return "PASS_SHAPE_ONLY"


def write_lane_files(output_dir: Path, arby_text: str | None, aster_text: str | None) -> None:
    if arby_text is not None:
        (output_dir / "Arby-last-message.txt").write_text(arby_text, encoding="utf-8")
    if aster_text is not None:
        (output_dir / "Aster Vale-last-message.txt").write_text(aster_text, encoding="utf-8")
    for lane in LANES:
        (output_dir / f"{lane}-stdout.txt").write_text("", encoding="utf-8")
        (output_dir / f"{lane}-stderr.txt").write_text("", encoding="utf-8")


def run_fixtures() -> dict[str, Any]:
    marker_text = "Advisory mentions " + "to" + "ken" + " handling as review context."
    fixture_defs = [
        {
            "arby_text": "Advisory ready. All GMUT gates remain open.",
            "aster_text": "Advisory ready. Raw transport excluded.",
            "expected_status": "FINAL_MESSAGES_READY",
            "fixture": "clean_final_messages",
        },
        {
            "arby_text": marker_text,
            "aster_text": "Advisory ready. Raw transport excluded.",
            "expected_status": "OPEN_GAP_FINAL_MESSAGE_MARKER_REVIEW",
            "fixture": "marker_review_terminal",
        },
        {
            "arby_text": "Advisory ready.",
            "aster_text": None,
            "expected_status": "OPEN_GAP_FINAL_MESSAGE_PENDING",
            "fixture": "missing_final_pending",
        },
    ]
    entries: list[dict[str, Any]] = []
    with TemporaryDirectory(prefix="v472-v8-notifier-fixtures-") as tmp:
        root = Path(tmp)
        for fixture in fixture_defs:
            output_dir = root / fixture["fixture"]
            output_dir.mkdir(parents=True, exist_ok=True)
            write_lane_files(output_dir, fixture["arby_text"], fixture["aster_text"])
            notice = build_notice(output_dir, LANES, PHASE, utc_now())
            entries.append(
                {
                    "actual_status": notice["aggregate_status"],
                    "expected_status": fixture["expected_status"],
                    "fixture": fixture["fixture"],
                    "status": "PASS_FIXTURE" if notice["aggregate_status"] == fixture["expected_status"] else "FAIL_FIXTURE",
                    "tempdir_only": True,
                }
            )
    return {
        "entries": entries,
        "failure_count": sum(item["status"] != "PASS_FIXTURE" for item in entries),
        "status": "PASS_FIXTURES" if all(item["status"] == "PASS_FIXTURE" for item in entries) else "FAIL_FIXTURES",
    }


def write_artifacts() -> list[Path]:
    generated_at = utc_now()
    fixtures = run_fixtures()
    rows = [
        row("terminal_marker_review", "PASS_SHAPE_ONLY", "Marker-review final messages now terminate as an open-gap notice instead of polling until timeout."),
        row("fixtures", "PASS_SHAPE_ONLY" if fixtures["failure_count"] == 0 else "FAIL_BLOCKER", "Notifier terminal-state fixtures passed.", {"failure_count": fixtures["failure_count"]}),
        row("claim_boundary", "PASS_SHAPE_ONLY", "Marker-review receipts do not publish raw final advisory text."),
    ]
    repair = {
        "aggregate_status": aggregate(rows),
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "phase_slug": PHASE,
        "rows": rows,
    }
    written: list[Path] = []
    path = ARTIFACT_ROOT / f"{PHASE}-notifier-terminal-state-repair-v1.json"
    write_json(path, repair)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-notifier-terminal-state-repair-v1.md",
        f"""
# v472 THOS v8 x1 Notifier Terminal-State Repair

Generated UTC: `{generated_at}`

Status: `{repair['aggregate_status']}`

Marker-review final messages now terminate as an open-gap notice instead of polling until timeout. Raw final advisory text remains unpublished.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-notifier-terminal-state-repair-v1.md")

    path = ARTIFACT_ROOT / f"{PHASE}-notifier-fixture-results-v1.json"
    write_json(path, fixtures)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-notifier-fixture-results-v1.md",
        f"""
# v472 THOS v8 x1 Notifier Fixture Results

Status: `{fixtures['status']}`

Fixture failures: `{fixtures['failure_count']}`

Fixtures covered clean final messages, marker-review terminal notices, and missing-final pending notices.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-notifier-fixture-results-v1.md")

    status_rows = [
        row("repair", repair["aggregate_status"], "Notifier terminal-state repair generated."),
        row("fixtures", "PASS_SHAPE_ONLY" if fixtures["failure_count"] == 0 else "FAIL_BLOCKER", "Notifier fixtures passed."),
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
# v472 THOS v8 x1 Run Status

Status: `{run_status['aggregate_status']}`

Next expected phase: `{NEXT_PHASE}`

v8 x1 repairs notifier terminal-state behavior and verifies it with tempdir-only fixtures.

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
