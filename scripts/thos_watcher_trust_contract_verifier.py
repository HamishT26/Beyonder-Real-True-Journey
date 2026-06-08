#!/usr/bin/env python3
"""Verify the THOS no-babysitting watcher-trust contract from curated receipts."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = REPO_ROOT / "docs" / "trinity-live-traces"
LOCAL_PATH_RE = re.compile(r"(?:[A-Za-z]:\\|\\\\\?\\|/mnt/[A-Za-z]/)", re.IGNORECASE)

FORBIDDEN_TRUE_KEYS = {
    "credentials_published",
    "local_absolute_path_published",
    "local_absolute_paths_published",
    "matched_text_published",
    "prompt_body_published",
    "raw_lane_text_published",
    "raw_logs_published",
    "raw_transport_published",
    "screenshot_published",
    "screenshots_published",
    "session_stream_published",
    "session_streams_published",
}


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def resolve_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    repo_relative = REPO_ROOT / path
    if repo_relative.exists():
        return repo_relative
    return TRACE_DIR / value


def resolve_output_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    if len(path.parts) == 1:
        return TRACE_DIR / path
    return REPO_ROOT / path


def read_json(value: str) -> dict[str, Any]:
    path = resolve_path(value)
    if not path.exists():
        return {"_available": False, "_receipt_file": path.name, "_reason": "missing"}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"_available": False, "_receipt_file": path.name, "_reason": "json_error"}
    if not isinstance(payload, dict):
        return {"_available": False, "_receipt_file": path.name, "_reason": "not_object"}
    payload["_available"] = True
    payload["_receipt_file"] = path.name
    return payload


def status(payload: dict[str, Any]) -> str:
    return str(payload.get("overall_status") or payload.get("aggregate_status") or payload.get("status") or "")


def nested(payload: dict[str, Any], *keys: str) -> Any:
    current: Any = payload
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current


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
    gaps: list[str] = []
    if not payload.get("_available"):
        return gaps
    for path, value in walk(payload):
        key = path.rsplit(".", 1)[-1]
        if key in FORBIDDEN_TRUE_KEYS and value is True:
            gaps.append(f"{name}:forbidden_publication_true:{path}")
        if isinstance(value, str) and LOCAL_PATH_RE.search(value):
            gaps.append(f"{name}:local_absolute_path_string:{path}")
    return gaps


def add_check(checks: list[dict[str, Any]], name: str, passed: bool, detail: str) -> None:
    checks.append({"name": name, "passed": bool(passed), "detail": detail})


def write_md(path: Path, receipt: dict[str, Any]) -> None:
    lines = [
        f"# {receipt['phase_slug']} Watcher Trust Contract Verifier",
        "",
        f"Generated UTC: `{receipt['generated_utc']}`",
        "",
        f"Status: `{receipt['overall_status']}`",
        "",
        "## Checks",
        "",
    ]
    for check in receipt["checks"]:
        mark = "PASS" if check["passed"] else "BLOCK"
        lines.append(f"- `{mark}` {check['name']}: {check['detail']}")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This verifier reads curated status receipts only. It does not inspect raw sibling output, raw logs, session streams, screenshots, credentials, or private dumps.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--wait-plan-json", required=True)
    parser.add_argument("--cadence-json", required=True)
    parser.add_argument("--closeout-json", required=True)
    parser.add_argument("--receipt-json", required=True)
    parser.add_argument("--receipt-md", required=True)
    args = parser.parse_args()

    wait_plan = read_json(args.wait_plan_json)
    cadence = read_json(args.cadence_json)
    closeout = read_json(args.closeout_json)

    checks: list[dict[str, Any]] = []
    for name, payload in (("wait_plan", wait_plan), ("cadence", cadence), ("closeout", closeout)):
        add_check(checks, f"{name}_available", bool(payload.get("_available")), str(payload.get("_receipt_file")))

    add_check(
        checks,
        "wait_plan_productive_status",
        status(wait_plan).startswith("PASS_X1_WAIT_TASKS") or status(wait_plan).startswith("PASS_PRODUCTIVE_WAIT"),
        status(wait_plan) or "missing_status",
    )
    add_check(
        checks,
        "manual_polling_disabled_before_gate",
        nested(wait_plan, "supervision_policy", "manual_status_check_before_gate") is False,
        "manual_status_check_before_gate=false required",
    )
    add_check(
        checks,
        "cadence_gate_passed",
        status(cadence) == "PASS_STATUS_CHECK_ALLOWED" and bool(cadence.get("status_check_allowed")),
        status(cadence) or "missing_status",
    )
    add_check(
        checks,
        "closeout_no_babysitting",
        nested(closeout, "repair_summary", "manual_babysitting_before_x1_gate") is False,
        "manual_babysitting_before_x1_gate=false required",
    )

    gaps: list[str] = []
    for name, payload in (("wait_plan", wait_plan), ("cadence", cadence), ("closeout", closeout)):
        gaps.extend(publication_gaps(name, payload))
    add_check(checks, "publication_boundary", not gaps, "; ".join(gaps) if gaps else "no raw/private publication markers")

    overall = "PASS_WATCHER_TRUST_CONTRACT" if all(row["passed"] for row in checks) else "OPEN_GAP_WATCHER_TRUST_CONTRACT"
    receipt = {
        "artifact_type": "watcher_trust_contract_verifier",
        "phase_slug": args.phase_slug,
        "generated_utc": utc_now(),
        "overall_status": overall,
        "checks": checks,
        "publication_boundary": {
            "status_only": True,
            "raw_lane_text_published": False,
            "raw_logs_published": False,
            "session_streams_published": False,
            "screenshots_published": False,
            "credentials_published": False,
            "local_absolute_paths_published": False,
        },
    }

    json_path = resolve_output_path(args.receipt_json)
    md_path = resolve_output_path(args.receipt_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_md(md_path, receipt)
    print(json.dumps({"status": overall, "phase_slug": args.phase_slug}, indent=2))
    return 0 if overall.startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
