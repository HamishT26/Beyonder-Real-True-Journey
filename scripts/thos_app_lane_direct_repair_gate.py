#!/usr/bin/env python3
"""Create a status-only app lane gate from a successful redacted notifier receipt.

This handles the case where the wrapper/launcher receipt timed out, but a
direct existing-thread notifier run later produced a complete, redacted lane
receipt. It does not read or publish advisory text.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = REPO_ROOT / "docs" / "trinity-live-traces"
REMOTE_REF = "origin/codex/GHC-Family/beyonder-shared-omega-line"


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def nz_now() -> str:
    utc = dt.datetime.now(dt.UTC).replace(microsecond=0)
    return utc.astimezone(dt.timezone(dt.timedelta(hours=12), name="NZST")).isoformat()


def git_text(args: list[str]) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=30,
        check=False,
    )
    return proc.stdout.strip() if proc.returncode == 0 else "unavailable"


def read_json(path: str) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} did not contain a JSON object")
    return payload


def receipt_name(path: str) -> str:
    return Path(path).name


def status(payload: dict[str, Any]) -> str:
    return str(payload.get("overall_status") or payload.get("aggregate_status") or payload.get("status") or "")


def lane_summary(lanes: list[Any]) -> tuple[list[dict[str, Any]], list[str]]:
    rows: list[dict[str, Any]] = []
    gaps: list[str] = []
    for item in lanes:
        if not isinstance(item, dict):
            gaps.append("lane:not_object")
            continue
        lane = str(item.get("lane") or "unknown")
        completion = item.get("turn_completion") if isinstance(item.get("turn_completion"), dict) else {}
        row = {
            "lane": lane,
            "overall_status": item.get("overall_status"),
            "duration_seconds": item.get("duration_seconds"),
            "read_status": (item.get("read") or {}).get("status") if isinstance(item.get("read"), dict) else None,
            "resume_status": (item.get("resume") or {}).get("status") if isinstance(item.get("resume"), dict) else None,
            "turn_status": (item.get("turn_start") or {}).get("status") if isinstance(item.get("turn_start"), dict) else "not_started",
            "completion_status": completion.get("status", "not_waited"),
        }
        rows.append(row)
        if row["overall_status"] != "completed" or row["completion_status"] != "completed":
            gaps.append(f"{lane}:not_completed")
    return rows, gaps


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    notifier = read_json(args.notifier_json)
    redactor = read_json(args.redactor_json)
    runner = read_json(args.runner_json) if args.runner_json else {}
    launcher = read_json(args.launcher_json) if args.launcher_json else {}

    expected_lanes = [part.strip() for part in args.lanes.split(",") if part.strip()]
    rows, gaps = lane_summary(notifier.get("lanes", []))
    completed_lanes = {row["lane"] for row in rows if row.get("completion_status") == "completed"}
    for lane in expected_lanes:
        if lane not in completed_lanes:
            gaps.append(f"{lane}:missing")

    notifier_pass = status(notifier) == "PASS"
    redactor_pass = status(redactor) == "PASS_APP_THREAD_REDACTION_GUARD"
    if not notifier_pass:
        gaps.append(f"notifier:{status(notifier) or 'missing'}")
    if not redactor_pass:
        gaps.append(f"redactor:{status(redactor) or 'missing'}")

    runner_status = status(runner) or "not_supplied"
    launcher_status = status(launcher) or "not_supplied"
    wrapper_repair_notes = []
    if runner_status and not runner_status.startswith("PASS"):
        wrapper_repair_notes.append(f"runner_layer_prior_status:{runner_status}")
    if launcher_status and not launcher_status.startswith("PASS"):
        wrapper_repair_notes.append(f"launcher_layer_prior_status:{launcher_status}")

    overall_status = "PASS_APP_LANE_COMPLETION_GATE" if not gaps else "OPEN_GAP_APP_LANE_COMPLETION_REQUIRED"
    return {
        "artifact_type": "council_app_lane_completion_gate",
        "phase_slug": args.phase_slug,
        "generated_utc": utc_now(),
        "generated_nz": nz_now(),
        "mode": "notify_direct_repair",
        "overall_status": overall_status,
        "local_head_at_gate": git_text(["rev-parse", "HEAD"]),
        "remote_head_at_gate": git_text(["rev-parse", REMOTE_REF]),
        "drift_at_gate": git_text(["rev-list", "--left-right", "--count", f"HEAD...{REMOTE_REF}"]),
        "expected_lanes": expected_lanes,
        "gate_inputs": {
            "completion_notifier_receipt": receipt_name(args.notifier_json),
            "completion_notifier_status": status(notifier),
            "redactor_receipt": receipt_name(args.redactor_json),
            "redactor_status": status(redactor),
            "runner_receipt": receipt_name(args.runner_json) if args.runner_json else None,
            "runner_status": runner_status,
            "watch_launcher_receipt": receipt_name(args.launcher_json) if args.launcher_json else None,
            "watch_launcher_status": launcher_status,
        },
        "lanes": rows,
        "open_gaps": sorted(set(gaps)),
        "wrapper_repair_notes": wrapper_repair_notes,
        "phase_advance_rule": {
            "all_app_lanes_required": True,
            "all_cli_lanes_required": True,
            "duration_is_completion_proof": False,
            "next_phase_allowed": overall_status == "PASS_APP_LANE_COMPLETION_GATE",
        },
        "publication_boundary": {
            "advisory_body_published": False,
            "auth_material_published": False,
            "image_captures_published": False,
            "local_absolute_paths_published": False,
            "raw_transport_published": False,
        },
        "claim_boundary": {
            "scope": "THOS app-lane completion gating only",
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
        },
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['phase_slug']} App Lane Direct Repair Gate",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: `{payload['overall_status']}`",
        f"- mode: `{payload['mode']}`",
        f"- completion_notifier_status: `{payload['gate_inputs']['completion_notifier_status']}`",
        f"- redactor_status: `{payload['gate_inputs']['redactor_status']}`",
        f"- phase_advance_allowed: `{payload['phase_advance_rule']['next_phase_allowed']}`",
        "",
        "## Lane Summary",
    ]
    for lane in payload["lanes"]:
        lines.append(
            f"- {lane['lane']}: `{lane.get('overall_status')}`, read `{lane.get('read_status')}`, "
            f"resume `{lane.get('resume_status')}`, turn `{lane.get('turn_status')}`, "
            f"completion `{lane.get('completion_status')}`."
        )
    lines.extend(["", "## Wrapper Repair Notes"])
    if payload["wrapper_repair_notes"]:
        lines.extend(f"- `{note}`" for note in payload["wrapper_repair_notes"])
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "Boundary: status only; no advisory body, raw transport, credentials, screenshots, or local absolute paths.",
            "",
            "Claim boundary: GMUT and canon gates remain open; duration is not completion proof.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--lanes", default="Cicero,Kierkegaard,Aristotle")
    parser.add_argument("--notifier-json", required=True)
    parser.add_argument("--redactor-json", required=True)
    parser.add_argument("--runner-json")
    parser.add_argument("--launcher-json")
    parser.add_argument("--receipt-json", required=True)
    parser.add_argument("--receipt-md", required=True)
    args = parser.parse_args()

    payload = build_payload(args)
    write_json(Path(args.receipt_json), payload)
    write_md(Path(args.receipt_md), payload)
    print(json.dumps({"status": payload["overall_status"], "phase_slug": args.phase_slug}, indent=2))
    return 0 if payload["overall_status"].startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
