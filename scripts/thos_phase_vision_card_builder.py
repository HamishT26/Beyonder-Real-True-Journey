#!/usr/bin/env python3
"""Build compact phase-start and compact-refresh vision cards."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = REPO_ROOT / "docs" / "trinity-live-traces"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def resolve(path: str | None) -> Path | None:
    if not path:
        return None
    candidate = Path(path)
    return candidate if candidate.is_absolute() else REPO_ROOT / candidate


def read_status(path: str | None) -> dict[str, Any]:
    candidate = resolve(path)
    if candidate is None:
        return {"available": False, "file": None, "status": "not_provided"}
    if not candidate.exists():
        return {"available": False, "file": candidate.name, "status": "missing"}
    try:
        payload = json.loads(candidate.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError:
        return {"available": False, "file": candidate.name, "status": "json_parse_failed"}
    if not isinstance(payload, dict):
        return {"available": False, "file": candidate.name, "status": "not_object"}
    return {
        "available": True,
        "file": candidate.name,
        "status": str(payload.get("overall_status") or payload.get("aggregate_status") or payload.get("status") or "status_missing"),
    }


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    anchors = {
        "previous_closeout": read_status(args.previous_closeout_json),
        "previous_dashboard": read_status(args.previous_dashboard_json),
        "launch_receipt": read_status(args.launch_json),
        "runner_receipt": read_status(args.runner_json),
        "alpha_wait_ledger": read_status(args.alpha_json),
    }
    open_gaps = [f"{name}:{row['status']}" for name, row in anchors.items() if row["available"] and str(row["status"]).startswith("OPEN_GAP")]
    missing = [name for name, row in anchors.items() if not row["available"] and name in {"launch_receipt", "runner_receipt"}]
    return {
        "artifact_type": "phase_start_vision_card",
        "phase_slug": args.phase_slug,
        "generated_utc": utc_now(),
        "overall_status": "PASS_PHASE_START_VISION_CARD" if not missing and not open_gaps else "OPEN_GAP_PHASE_START_VISION_CARD",
        "read_order": [
            "previous x2 closeout",
            "previous phase dashboard",
            "current app runner receipt",
            "current CLI launcher receipt",
            "current alpha wait ledger",
            "current cadence guard before harvest",
        ],
        "current_operating_rules": {
            "all_five_existing_lanes_required_for_x1": True,
            "manual_check_cadence_minutes": 5,
            "work_between_checks": True,
            "node_entrypoint_first_for_cli": True,
            "x2_build_run_test_use": True,
            "ten_approval_candidates_per_phase": True,
            "raw_lane_text_publication": False,
            "duration_is_completion_proof": False,
        },
        "continuity_anchors": anchors,
        "open_gaps": open_gaps,
        "missing_required": missing,
        "trinity_mandala_boundary": {
            "GMUT_Mind": "source-backed and open-gated",
            "THOS_Body": "runner, command, skill, IPC, and sandbox implementation work",
            "Freed_ID_CBR_Heart": "rights and identity framing stays aspirational unless exact legal artifacts exist",
        },
        "publication_boundary": {
            "status_only": True,
            "raw_lane_text_published": False,
            "raw_logs_published": False,
            "credentials_published": False,
            "session_streams_published": False,
            "local_absolute_paths_published": False,
        },
        "claim_boundary": {
            "gmut_gate_state": "open",
            "canon_promotion": "not_claimed",
            "consciousness_or_final_physics_proof": "not_claimed",
        },
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['phase_slug']} Phase Start Vision Card",
        "",
        f"- overall_status: `{payload['overall_status']}`",
        f"- generated_utc: `{payload['generated_utc']}`",
        "",
        "## Read Order",
    ]
    lines.extend(f"- {item}" for item in payload["read_order"])
    lines.extend(["", "## Operating Rules"])
    for key, value in payload["current_operating_rules"].items():
        lines.append(f"- {key}: `{str(value).lower()}`")
    lines.extend(["", "Boundary: status-only vision card; no raw lane text, logs, credentials, session streams, or local absolute paths."])
    lines.append("GMUT, canon, consciousness, and final-physics gates remain open.")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--previous-closeout-json")
    parser.add_argument("--previous-dashboard-json")
    parser.add_argument("--launch-json")
    parser.add_argument("--runner-json")
    parser.add_argument("--alpha-json")
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
