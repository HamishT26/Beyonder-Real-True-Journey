#!/usr/bin/env python3
"""Create a compact status-only dashboard from THOS/GMUT phase gate receipts."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_json(path: str | None) -> dict[str, Any]:
    if not path:
        return {}
    candidate = Path(path)
    if not candidate.exists():
        return {"_missing": True, "_receipt_file": candidate.name}
    payload = json.loads(candidate.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        return {"_invalid": True, "_receipt_file": candidate.name}
    payload["_receipt_file"] = candidate.name
    return payload


def status(payload: dict[str, Any]) -> str:
    if payload.get("_missing"):
        return "MISSING"
    if payload.get("_invalid"):
        return "INVALID"
    return str(payload.get("overall_status") or payload.get("aggregate_status") or payload.get("status") or "UNKNOWN")


def boundary_safe(payload: dict[str, Any]) -> bool:
    boundary = payload.get("publication_boundary")
    if not isinstance(boundary, dict):
        return True
    sensitive = [
        "raw_lane_text_published",
        "raw_logs_published",
        "prompt_body_published",
        "session_streams_published",
        "screenshots_published",
        "credentials_published",
        "local_absolute_paths_published",
    ]
    return all(boundary.get(key) is False for key in sensitive if key in boundary)


def lane_counts(five_lane: dict[str, Any]) -> dict[str, int]:
    counts = {"app": 0, "cli": 0}
    for row in five_lane.get("lanes", []):
        surface = str(row.get("surface") or "")
        if surface in counts:
            counts[surface] += 1
    return counts


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['phase_slug']} Phase Dashboard Receipt",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: `{payload['overall_status']}`",
        f"- phase_advance_allowed: `{payload['phase_advance_allowed']}`",
        f"- app_lane_count: `{payload['lane_counts']['app']}`",
        f"- cli_lane_count: `{payload['lane_counts']['cli']}`",
        "",
        "## Gate Summary",
    ]
    for gate in payload["gates"]:
        lines.append(f"- {gate['name']}: `{gate['status']}` from `{gate['receipt']}`")
    lines.extend(["", "Open gaps:"])
    lines.extend(f"- `{gap}`" for gap in payload["open_gaps"]) if payload["open_gaps"] else lines.append("- none")
    lines.extend(
        [
            "",
            "Boundary: status-only dashboard; no raw lane text, prompts, logs, screenshots, credentials, session streams, or local absolute paths.",
            "",
            "Claim boundary: GMUT and canon gates remain open; duration is not completion proof.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--app-gate-json", required=True)
    parser.add_argument("--cli-quality-json", required=True)
    parser.add_argument("--marker-review-json", required=True)
    parser.add_argument("--five-lane-json", required=True)
    parser.add_argument("--exposure-json", required=True)
    parser.add_argument("--classifier-json", required=True)
    parser.add_argument("--phase-advance-json", required=True)
    parser.add_argument("--closeout-json", required=True)
    parser.add_argument("--next-prep-json", required=True)
    parser.add_argument("--receipt-json", required=True)
    parser.add_argument("--receipt-md", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    receipts = {
        "app_gate": read_json(args.app_gate_json),
        "cli_quality": read_json(args.cli_quality_json),
        "marker_review": read_json(args.marker_review_json),
        "five_lane": read_json(args.five_lane_json),
        "exposure": read_json(args.exposure_json),
        "classifier": read_json(args.classifier_json),
        "phase_advance": read_json(args.phase_advance_json),
        "closeout": read_json(args.closeout_json),
        "next_prep": read_json(args.next_prep_json),
    }
    gates = [
        {"name": name, "status": status(payload), "receipt": str(payload.get("_receipt_file", "missing"))}
        for name, payload in receipts.items()
    ]
    expected_prefixes = {
        "app_gate": "PASS_APP_LANE_COMPLETION_GATE",
        "cli_quality": "PASS_",
        "marker_review": "PASS_MARKER_REVIEW_LEDGER",
        "five_lane": "PASS_FIVE_LANE_READY",
        "exposure": "PASS_EXPOSURE_GUARD",
        "classifier": "PASS_PHASE_ARTIFACT_CLASSIFIER",
        "phase_advance": "PASS_PHASE_ADVANCE_GATE",
        "closeout": "PASS_",
        "next_prep": "PASS_",
    }
    open_gaps = []
    for name, payload in receipts.items():
        gate_status = status(payload)
        prefix = expected_prefixes[name]
        if prefix.endswith("_"):
            if not gate_status.startswith(prefix):
                open_gaps.append(f"{name}:{gate_status}")
        elif gate_status != prefix:
            open_gaps.append(f"{name}:{gate_status}")
        if not boundary_safe(payload):
            open_gaps.append(f"{name}:publication_boundary")
    phase_advance_allowed = receipts["phase_advance"].get("phase_advance_allowed") is True and not open_gaps
    payload: dict[str, Any] = {
        "artifact_type": "phase_dashboard_receipt",
        "phase_slug": args.phase_slug,
        "generated_utc": utc_now(),
        "overall_status": "PASS_PHASE_DASHBOARD_RECEIPT" if phase_advance_allowed else "OPEN_GAP_PHASE_DASHBOARD_RECEIPT",
        "phase_advance_allowed": phase_advance_allowed,
        "lane_counts": lane_counts(receipts["five_lane"]),
        "gates": gates,
        "open_gaps": open_gaps,
        "publication_boundary": {
            "status_only": True,
            "raw_lane_text_published": False,
            "raw_logs_published": False,
            "prompt_body_published": False,
            "session_streams_published": False,
            "screenshots_published": False,
            "credentials_published": False,
            "local_absolute_paths_published": False,
        },
        "claim_boundary": {
            "gmut_gate_state": "open",
            "canon_promotion": "not_claimed",
            "duration_is_completion_proof": False,
        },
    }
    write_json(Path(args.receipt_json), payload)
    write_md(Path(args.receipt_md), payload)
    print(json.dumps({"status": payload["overall_status"], "phase_slug": args.phase_slug}, indent=2))
    return 0 if phase_advance_allowed else 1


if __name__ == "__main__":
    raise SystemExit(main())
