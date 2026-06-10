#!/usr/bin/env python3
"""Verify and summarize an x2 build/use phase from curated receipts only."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_TRUE_KEYS = {
    "credentials_published",
    "local_absolute_paths_published",
    "prompt_body_published",
    "raw_lane_text_published",
    "raw_logs_published",
    "raw_transport_published",
    "screenshots_published",
    "session_streams_published",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def resolve(path: str) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else REPO_ROOT / candidate


def read_json(path: str) -> dict[str, Any]:
    candidate = resolve(path)
    if not candidate.exists():
        return {"_available": False, "_file": candidate.name, "_reason": "missing"}
    try:
        payload = json.loads(candidate.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"_available": False, "_file": candidate.name, "_reason": "json_error"}
    if not isinstance(payload, dict):
        return {"_available": False, "_file": candidate.name, "_reason": "not_object"}
    payload["_available"] = True
    payload["_file"] = candidate.name
    return payload


def status(payload: dict[str, Any]) -> str:
    return str(payload.get("overall_status") or payload.get("aggregate_status") or payload.get("status") or "")


def walk(value: Any, prefix: str = "") -> list[tuple[str, Any]]:
    rows: list[tuple[str, Any]] = []
    if isinstance(value, dict):
        for key, item in value.items():
            rows.extend(walk(item, f"{prefix}.{key}" if prefix else str(key)))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            rows.extend(walk(item, f"{prefix}[{index}]"))
    else:
        rows.append((prefix, value))
    return rows


def publication_gaps(name: str, payload: dict[str, Any]) -> list[str]:
    gaps = []
    for path, value in walk(payload):
        key = path.rsplit(".", 1)[-1]
        if key in FORBIDDEN_TRUE_KEYS and value is True:
            gaps.append(f"{name}:{path}")
    return gaps


def build_payload(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any]]:
    receipts = {
        "implementation": read_json(args.implementation_json),
        "source_ipc": read_json(args.source_ipc_json),
        "fast_read": read_json(args.fast_read_json),
        "watcher_audit": read_json(args.watcher_audit_json),
        "runtime_foothold": read_json(args.runtime_foothold_json),
        "closeout": read_json(args.closeout_json),
        "handoff": read_json(args.handoff_json),
        "classifier": read_json(args.classifier_json),
        "exposure": read_json(args.exposure_json),
        "no_overclaim": read_json(args.no_overclaim_json),
    }
    expected_prefixes = {
        "implementation": "PASS_",
        "source_ipc": "PASS_",
        "fast_read": "PASS_",
        "watcher_audit": "PASS_",
        "runtime_foothold": "PASS_",
        "closeout": "PASS_",
        "handoff": "PASS_",
        "classifier": "PASS_PHASE_ARTIFACT_CLASSIFIER",
        "exposure": "PASS_EXPOSURE_GUARD",
        "no_overclaim": "PASS_NO_OVERCLAIM_GUARD",
    }
    checks = []
    open_gaps = []
    for name, payload in receipts.items():
        receipt_status = status(payload)
        available = payload.get("_available") is True
        expected = expected_prefixes[name]
        passed = available and (receipt_status == expected if not expected.endswith("_") else receipt_status.startswith(expected))
        checks.append({"name": name, "passed": passed, "status": receipt_status, "receipt": payload.get("_file")})
        if not passed:
            open_gaps.append(f"{name}:{receipt_status or payload.get('_reason', 'missing')}")
        open_gaps.extend(publication_gaps(name, payload))
    gate = {
        "artifact_type": "x2_phase_advance_gate_verifier",
        "phase_slug": args.phase_slug,
        "next_phase_slug": args.next_phase_slug,
        "generated_utc": utc_now(),
        "overall_status": "PASS_X2_PHASE_ADVANCE_GATE" if not open_gaps else "OPEN_GAP_X2_PHASE_ADVANCE_GATE",
        "phase_advance_allowed": not open_gaps,
        "checks": checks,
        "open_gaps": open_gaps,
        "publication_boundary": {
            "status_only": True,
            "raw_lane_text_published": False,
            "raw_logs_published": False,
            "prompt_body_published": False,
            "screenshots_published": False,
            "credentials_published": False,
            "session_streams_published": False,
            "local_absolute_paths_published": False,
        },
        "claim_boundary": {
            "gmut_gate_state": "open",
            "canon_promotion": "not_claimed",
            "consciousness_or_final_physics_proof": "not_claimed",
            "duration_is_completion_proof": False,
        },
    }
    dashboard = {
        "artifact_type": "x2_phase_dashboard_receipt",
        "phase_slug": args.phase_slug,
        "next_phase_slug": args.next_phase_slug,
        "generated_utc": utc_now(),
        "overall_status": "PASS_X2_PHASE_DASHBOARD_RECEIPT" if not open_gaps else "OPEN_GAP_X2_PHASE_DASHBOARD_RECEIPT",
        "phase_advance_allowed": not open_gaps,
        "gate_receipt": Path(args.gate_json).name,
        "status_rows": checks,
        "build_summary": [
            "x2 implementation ledger",
            "source-ledger-to-IPC mapping",
            "omega v2 fast-read pack",
            "no-babysitting watcher audit",
            "runtime foothold ledger",
            "next x1 launch handoff",
        ],
        "publication_boundary": gate["publication_boundary"],
        "claim_boundary": gate["claim_boundary"],
    }
    return gate, dashboard


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, payload: dict[str, Any]) -> None:
    title = payload["artifact_type"].replace("_", " ").title()
    lines = [
        f"# {payload['phase_slug']} {title}",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: `{payload['overall_status']}`",
        f"- phase_advance_allowed: `{str(payload['phase_advance_allowed']).lower()}`",
        f"- next_phase_slug: `{payload['next_phase_slug']}`",
        "",
        "## Status Rows",
    ]
    for row in payload.get("checks", payload.get("status_rows", [])):
        lines.append(f"- {row['name']}: `{row['passed']}` ({row['status']}) from `{row['receipt']}`")
    if payload.get("open_gaps"):
        lines.extend(["", "## Open Gaps"])
        lines.extend(f"- `{gap}`" for gap in payload["open_gaps"])
    lines.extend(
        [
            "",
            "Boundary: status-only x2 gate/dashboard; no raw lane text, logs, prompt bodies, screenshots, credentials, session streams, or local absolute paths.",
            "",
            "GMUT, canon, consciousness, and final-physics gates remain open.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--next-phase-slug", required=True)
    parser.add_argument("--implementation-json", required=True)
    parser.add_argument("--source-ipc-json", required=True)
    parser.add_argument("--fast-read-json", required=True)
    parser.add_argument("--watcher-audit-json", required=True)
    parser.add_argument("--runtime-foothold-json", required=True)
    parser.add_argument("--closeout-json", required=True)
    parser.add_argument("--handoff-json", required=True)
    parser.add_argument("--classifier-json", required=True)
    parser.add_argument("--exposure-json", required=True)
    parser.add_argument("--no-overclaim-json", required=True)
    parser.add_argument("--gate-json", required=True)
    parser.add_argument("--gate-md", required=True)
    parser.add_argument("--dashboard-json", required=True)
    parser.add_argument("--dashboard-md", required=True)
    args = parser.parse_args()

    gate, dashboard = build_payload(args)
    write_json(Path(args.gate_json), gate)
    write_md(Path(args.gate_md), gate)
    write_json(Path(args.dashboard_json), dashboard)
    write_md(Path(args.dashboard_md), dashboard)
    print(json.dumps({"status": gate["overall_status"], "dashboard_status": dashboard["overall_status"]}, indent=2))
    return 0 if gate["phase_advance_allowed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
