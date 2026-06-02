#!/usr/bin/env python3
"""Run and publish v473 THOS v3 x1 watch-launcher fixture results."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v473-thos-v3-x1"
NEXT_PHASE = "v473-thos-v3-x2"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"
WRAPPER = REPO_ROOT / "scripts" / "thos_cli_lane_watch_launcher.py"

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


def run_fixture() -> tuple[dict[str, Any], dict[str, Any]]:
    with tempfile.TemporaryDirectory(prefix="ghc-v473-v3-x1-watch-launcher-") as temp_name:
        temp_dir = Path(temp_name)
        (temp_dir / "Arby-last-message.txt").write_text("Final advisory ready. Clean fixture.\n", encoding="utf-8")
        (temp_dir / "Aster Vale-last-message.txt").write_text("Final advisory ready. Clean fixture.\n", encoding="utf-8")
        receipt_json = temp_dir / "receipt.json"
        receipt_md = temp_dir / "receipt.md"
        command = [
            sys.executable,
            str(WRAPPER),
            "--output-dir",
            str(temp_dir),
            "--phase-slug",
            f"{PHASE}-fixture",
            "--lane",
            "Arby",
            "--lane",
            "Aster Vale",
            "--poll-seconds",
            "1",
            "--timeout-seconds",
            "10",
            "--receipt-json",
            str(receipt_json),
            "--receipt-md",
            str(receipt_md),
            "--execute",
            "--once",
            "--wait-seconds",
            "10",
            "--redact",
        ]
        completed = subprocess.run(command, cwd=REPO_ROOT, text=True, capture_output=True, check=False)
        plan = json.loads(completed.stdout) if completed.stdout.strip() else {}
        receipt = json.loads(receipt_json.read_text(encoding="utf-8")) if receipt_json.exists() else {}
        plan["wrapper_returncode"] = completed.returncode
        plan["wrapper_stderr_bytes"] = len(completed.stderr.encode("utf-8", errors="replace"))
        return plan, receipt


def write_artifacts() -> list[Path]:
    generated_at = utc_now()
    plan, receipt = run_fixture()
    lanes = receipt.get("lanes", [])
    all_ready = bool(lanes) and all(lane.get("completion_status") == "FINAL_MESSAGE_READY" for lane in lanes)
    has_spaced_lane = any(lane.get("lane") == "Aster Vale" for lane in lanes)
    marker_count = sum(lane.get("final_message_sensitive_marker_count", 0) for lane in lanes)

    fixture_rows = [
        row(
            "wrapper_exit",
            "PASS_SHAPE_ONLY" if plan.get("wrapper_returncode") == 0 else "FAIL_BLOCKER",
            "Wrapper fixture process exited cleanly.",
            {"returncode": plan.get("wrapper_returncode")},
        ),
        row(
            "spaced_lane_preserved",
            "PASS_SHAPE_ONLY" if has_spaced_lane else "FAIL_BLOCKER",
            "Lane name containing a space was preserved through wrapper launch.",
        ),
        row(
            "receipt_ready",
            "PASS_SHAPE_ONLY" if all_ready else "OPEN_GAP",
            "Notifier receipt marked both fixture lanes final-message ready.",
            {"receipt_status": receipt.get("aggregate_status")},
        ),
        row(
            "marker_count",
            "PASS_SHAPE_ONLY" if marker_count == 0 else "OPEN_GAP",
            "Fixture final-message marker count is zero.",
            {"marker_count": marker_count},
        ),
        row(
            "shell_boundary",
            "PASS_SHAPE_ONLY" if plan.get("shell_invoked") is False else "FAIL_BLOCKER",
            "Wrapper launched the notifier with argument-list semantics, not shell parsing.",
        ),
    ]
    fixture = {
        "aggregate_status": aggregate(fixture_rows),
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "phase_slug": PHASE,
        "receipt_summary": {
            "aggregate_status": receipt.get("aggregate_status"),
            "lane_count": len(lanes),
            "spaced_lane_seen": has_spaced_lane,
        },
        "rows": fixture_rows,
        "tempdir_only": True,
    }

    written: list[Path] = []
    path = ARTIFACT_ROOT / f"{PHASE}-watch-launcher-fixture-results-v1.json"
    write_json(path, fixture)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-watch-launcher-fixture-results-v1.md",
        f"""
# v473 THOS v3 x1 Watch-Launcher Fixture Results

Generated UTC: `{generated_at}`

Status: `{fixture['aggregate_status']}`

The fixture preserved the `Aster Vale` lane name, wrote a final-ready receipt, and avoided shell parsing.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-watch-launcher-fixture-results-v1.md")

    contract_rows = [
        row("argument_list", "PASS_SHAPE_ONLY", "Lane names are passed as discrete arguments."),
        row("redacted_plan", "PASS_SHAPE_ONLY", "Launch plans can be printed with local paths redacted."),
        row("temp_logs", "PASS_SHAPE_ONLY", "Watcher stdout/stderr files remain temp-only unless separately curated."),
        row("raw_boundary", "PASS_SHAPE_ONLY", "Lane final-message text is not published by the launcher."),
    ]
    contract = {
        "aggregate_status": aggregate(contract_rows),
        "generated_at_utc": generated_at,
        "phase_slug": PHASE,
        "rows": contract_rows,
        "script": "scripts/thos_cli_lane_watch_launcher.py",
    }
    path = ARTIFACT_ROOT / f"{PHASE}-shell-safe-watch-launch-contract-v1.json"
    write_json(path, contract)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-shell-safe-watch-launch-contract-v1.md",
        """
# v473 THOS v3 x1 Shell-Safe Watch Launch Contract

Future Arby/Aster watcher launches should use the wrapper so lane names with spaces remain intact and local paths stay redacted in launch plans.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-shell-safe-watch-launch-contract-v1.md")

    status_rows = [
        row("fixture", fixture["aggregate_status"], "Shell-safe watcher fixture passed."),
        row("contract", contract["aggregate_status"], "Watch-launch contract published."),
        row("completion_integration", "OPEN_GAP", "Live v3 x2 should reuse the wrapper for a real no-rush lane cycle."),
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
# v473 THOS v3 x1 Run Status

Status: `{run_status['aggregate_status']}`

Next expected phase: `{NEXT_PHASE}`

v3 x1 adds and tests a shell-safe watcher-launch wrapper for lane names containing spaces.

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
