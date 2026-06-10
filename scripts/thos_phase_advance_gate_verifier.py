#!/usr/bin/env python3
"""Verify a phase can advance using curated THOS/GMUT status receipts only."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = REPO_ROOT / "docs" / "trinity-live-traces"

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

LOCAL_PATH_RE = re.compile(r"(?:[A-Za-z]:\\|\\\\\?\\|/mnt/[A-Za-z]/)", re.IGNORECASE)


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def resolve_receipt(value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    repo_relative = REPO_ROOT / path
    if repo_relative.exists():
        return repo_relative
    return TRACE_DIR / value


def read_json(value: str) -> dict[str, Any]:
    path = resolve_receipt(value)
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


def lane_quality_ready(quality: dict[str, Any]) -> bool:
    if not status(quality).startswith("PASS"):
        return False
    lanes = quality.get("lanes")
    return isinstance(lanes, list) and len(lanes) >= 2 and all(
        row.get("completion_status") == "FINAL_MESSAGE_READY"
        and row.get("quality_status") == "PASS_ELABORATION_GATE"
        and int(row.get("sensitive_or_path_marker_count") or 0) == 0
        and not row.get("missing_required_headings")
        for row in lanes
        if isinstance(row, dict)
    )


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    receipts = {
        "cadence": read_json(args.cadence_json),
        "app_gate": read_json(args.app_gate_json),
        "cli_quality": read_json(args.cli_quality_json),
        "marker_review": read_json(args.marker_review_json),
        "five_lane": read_json(args.five_lane_json),
        "classifier": read_json(args.classifier_json),
        "exposure": read_json(args.exposure_json),
        "closeout": read_json(args.closeout_json),
        "next_prep": read_json(args.next_prep_json),
    }
    checks: list[dict[str, Any]] = []
    add_check(checks, "cadence_passed", status(receipts["cadence"]) == "PASS_STATUS_CHECK_ALLOWED", status(receipts["cadence"]))
    add_check(checks, "app_gate_passed", status(receipts["app_gate"]) == "PASS_APP_LANE_COMPLETION_GATE", status(receipts["app_gate"]))
    add_check(checks, "cli_quality_passed", lane_quality_ready(receipts["cli_quality"]), status(receipts["cli_quality"]))
    add_check(checks, "marker_review_passed", status(receipts["marker_review"]) == "PASS_MARKER_REVIEW_LEDGER", status(receipts["marker_review"]))
    add_check(checks, "five_lane_ready", status(receipts["five_lane"]) == "PASS_FIVE_LANE_READY", status(receipts["five_lane"]))
    add_check(checks, "phase_advance_allowed", nested(receipts["five_lane"], "phase_advance_allowed") is True, str(nested(receipts["five_lane"], "phase_advance_allowed")))
    add_check(checks, "classifier_passed", status(receipts["classifier"]) == "PASS_PHASE_ARTIFACT_CLASSIFIER", status(receipts["classifier"]))
    add_check(checks, "exposure_passed", status(receipts["exposure"]) == "PASS_EXPOSURE_GUARD", status(receipts["exposure"]))
    add_check(checks, "closeout_passed", status(receipts["closeout"]).startswith("PASS_"), status(receipts["closeout"]))
    add_check(checks, "next_prep_passed", status(receipts["next_prep"]).startswith("PASS_"), status(receipts["next_prep"]))
    add_check(
        checks,
        "gmut_and_canon_gates_open",
        nested(receipts["closeout"], "claim_boundary", "gmut_gate_state") == "open"
        and nested(receipts["closeout"], "claim_boundary", "canon_promotion") == "not_claimed",
        "open/not_claimed",
    )

    open_gaps = [row["name"] for row in checks if not row["passed"]]
    for name, payload in receipts.items():
        open_gaps.extend(publication_gaps(name, payload))

    return {
        "artifact_type": "phase_advance_gate_verifier",
        "phase_slug": args.phase_slug,
        "generated_utc": utc_now(),
        "overall_status": "PASS_PHASE_ADVANCE_GATE" if not open_gaps else "OPEN_GAP_PHASE_ADVANCE_GATE",
        "checks": checks,
        "open_gaps": open_gaps,
        "phase_advance_allowed": not open_gaps,
        "inputs": {name: payload.get("_receipt_file") for name, payload in receipts.items()},
        "publication_boundary": {
            "status_only": True,
            "raw_lane_text_published": False,
            "raw_logs_published": False,
            "prompt_body_published": False,
            "local_absolute_paths_published": False,
            "credentials_published": False,
            "screenshots_published": False,
            "session_streams_published": False,
        },
        "claim_boundary": {
            "gmut_gate_state": "open",
            "canon_promotion": "not_claimed",
            "duration_is_completion_proof": False,
        },
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['phase_slug']} Phase Advance Gate Verifier",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: `{payload['overall_status']}`",
        f"- phase_advance_allowed: `{payload['phase_advance_allowed']}`",
        "",
        "Checks:",
    ]
    for row in payload["checks"]:
        lines.append(f"- {row['name']}: `{row['passed']}` ({row['detail']})")
    lines.extend(["", "Open gaps:"])
    lines.extend(f"- `{gap}`" for gap in payload["open_gaps"]) if payload["open_gaps"] else lines.append("- none")
    lines.extend(
        [
            "",
            "Publication boundary: status only; no raw lane text, raw logs, prompt bodies, local absolute paths, credentials, screenshots, or session streams.",
            "",
            "Claim boundary: GMUT and canon gates remain open; duration is not completion proof.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--cadence-json", required=True)
    parser.add_argument("--app-gate-json", required=True)
    parser.add_argument("--cli-quality-json", required=True)
    parser.add_argument("--marker-review-json", required=True)
    parser.add_argument("--five-lane-json", required=True)
    parser.add_argument("--classifier-json", required=True)
    parser.add_argument("--exposure-json", required=True)
    parser.add_argument("--closeout-json", required=True)
    parser.add_argument("--next-prep-json", required=True)
    parser.add_argument("--receipt-json", required=True)
    parser.add_argument("--receipt-md", required=True)
    args = parser.parse_args()

    payload = build_payload(args)
    write_json(Path(args.receipt_json), payload)
    write_md(Path(args.receipt_md), payload)
    print(json.dumps({"status": payload["overall_status"], "phase_slug": args.phase_slug}, indent=2))
    return 0 if not payload["open_gaps"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
