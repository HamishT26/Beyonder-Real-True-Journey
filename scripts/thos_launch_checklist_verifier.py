#!/usr/bin/env python3
"""Verify the THOS/GMUT five-lane launch checklist from curated receipts."""

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
    "advisory_body_published",
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
    "unfiltered_transport_published",
}

LOCAL_PATH_RE = re.compile(r"(?:[A-Za-z]:\\|\\\\\?\\|/mnt/[A-Za-z]/)", re.IGNORECASE)


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def receipt_path(value: str | None) -> Path | None:
    if not value:
        return None
    path = Path(value)
    if path.is_absolute():
        return path
    return TRACE_DIR / value


def read_json(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {"available": False, "reason": "not_provided"}
    if not path.exists():
        return {"available": False, "reason": "missing", "file": path.name}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"available": False, "reason": "json_error", "file": path.name}
    if not isinstance(payload, dict):
        return {"available": False, "reason": "not_object", "file": path.name}
    payload["_receipt_file"] = path.name
    payload["_available"] = True
    return payload


def nested(payload: dict[str, Any], *keys: str) -> Any:
    current: Any = payload
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current


def status(payload: dict[str, Any]) -> str:
    return str(payload.get("overall_status") or payload.get("aggregate_status") or payload.get("status") or "")


def is_pass(payload: dict[str, Any], expected: str | None = None) -> bool:
    if not payload.get("_available"):
        return False
    current = status(payload)
    if expected:
        return current == expected
    return current.startswith("PASS_")


def walk_values(value: Any, prefix: str = "") -> list[tuple[str, Any]]:
    rows: list[tuple[str, Any]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_prefix = f"{prefix}.{key}" if prefix else str(key)
            rows.extend(walk_values(child, child_prefix))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            rows.extend(walk_values(child, f"{prefix}[{index}]"))
    else:
        rows.append((prefix, value))
    return rows


def publication_gaps(name: str, payload: dict[str, Any]) -> list[str]:
    gaps: list[str] = []
    if not payload.get("_available"):
        return gaps
    for path, value in walk_values(payload):
        key = path.rsplit(".", 1)[-1]
        if key in FORBIDDEN_TRUE_KEYS and value is True:
            gaps.append(f"{name}:forbidden_publication_true:{path}")
        if isinstance(value, str) and LOCAL_PATH_RE.search(value):
            gaps.append(f"{name}:local_absolute_path_string:{path}")
    return gaps


def add_check(checks: list[dict[str, Any]], name: str, passed: bool, detail: str) -> None:
    checks.append({"name": name, "passed": bool(passed), "detail": detail})


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    receipts = {
        "five_lane_launch": read_json(receipt_path(args.five_lane_launch)),
        "app_runner": read_json(receipt_path(args.app_runner)),
        "prompt_contract": read_json(receipt_path(args.prompt_contract)),
        "heading_contract": read_json(receipt_path(args.heading_contract)),
        "cli_launcher": read_json(receipt_path(args.cli_launcher)),
        "productive_wait": read_json(receipt_path(args.productive_wait)),
        "app_redactor": read_json(receipt_path(args.app_redactor)),
        "exposure_guard": read_json(receipt_path(args.exposure_guard)),
    }

    checks: list[dict[str, Any]] = []
    add_check(
        checks,
        "five_lane_launch_passed",
        is_pass(receipts["five_lane_launch"]),
        status(receipts["five_lane_launch"]) or "missing",
    )
    add_check(
        checks,
        "app_background_watch_started",
        is_pass(receipts["app_runner"], "PASS_BACKGROUND_WATCH_STARTED")
        or nested(receipts["five_lane_launch"], "app_runner_status") == "PASS_BACKGROUND_WATCH_STARTED",
        status(receipts["app_runner"]) or str(nested(receipts["five_lane_launch"], "app_runner_status") or "missing"),
    )
    add_check(
        checks,
        "cli_prompt_contract_passed",
        is_pass(receipts["prompt_contract"], "PASS_CLI_PROMPT_CONTRACT")
        or nested(receipts["five_lane_launch"], "cli_prompt_contract_status") == "PASS_CLI_PROMPT_CONTRACT",
        status(receipts["prompt_contract"]) or str(nested(receipts["five_lane_launch"], "cli_prompt_contract_status") or "missing"),
    )
    add_check(
        checks,
        "cli_heading_contract_passed",
        is_pass(receipts["heading_contract"], "PASS_CLI_HEADING_CONTRACT")
        or nested(receipts["five_lane_launch"], "cli_heading_contract_status") == "PASS_CLI_HEADING_CONTRACT",
        status(receipts["heading_contract"]) or str(nested(receipts["five_lane_launch"], "cli_heading_contract_status") or "missing"),
    )
    add_check(
        checks,
        "cli_launcher_passed",
        is_pass(receipts["cli_launcher"], "PASS_CMD_BRIDGE_CLI_LANES_LAUNCHED")
        or nested(receipts["five_lane_launch"], "cli_runner_status") == "PASS_CMD_BRIDGE_CLI_LANES_LAUNCHED",
        status(receipts["cli_launcher"]) or str(nested(receipts["five_lane_launch"], "cli_runner_status") or "missing"),
    )
    add_check(
        checks,
        "productive_wait_passed",
        is_pass(receipts["productive_wait"], "PASS_PRODUCTIVE_WAIT_RECEIPT_VERIFIER"),
        status(receipts["productive_wait"]) or "missing",
    )
    wait_checks = receipts["productive_wait"].get("checks") if isinstance(receipts["productive_wait"].get("checks"), dict) else {}
    add_check(
        checks,
        "productive_wait_all_checks_true",
        bool(wait_checks) and all(value is True for value in wait_checks.values()),
        "all productive-wait subchecks true" if wait_checks else "missing subchecks",
    )
    add_check(
        checks,
        "manual_babysitting_disabled",
        nested(receipts["five_lane_launch"], "manual_polling_before_gate") is False
        and nested(receipts["cli_launcher"], "launch_policy", "manual_babysitting_required") is False,
        "manual polling before gate false and CLI babysitting false",
    )
    add_check(
        checks,
        "watchers_supervise_until_gate",
        nested(receipts["five_lane_launch"], "watchers_supervise_until_gate") is True
        or nested(receipts["app_runner"], "cadence_policy", "background_watch_allows_productive_waiting") is True,
        "watcher supervision recorded",
    )
    add_check(
        checks,
        "work_while_waiting_required",
        nested(receipts["five_lane_launch"], "work_while_waiting_required") is True
        and nested(receipts["app_runner"], "policy", "work_while_waiting_required") is True,
        "productive work while waiting required",
    )
    add_check(
        checks,
        "duration_not_completion_proof",
        nested(receipts["five_lane_launch"], "duration_is_completion_proof") is False
        and nested(receipts["cli_launcher"], "launch_policy", "duration_is_completion_proof") is False,
        "duration is not used as completion proof",
    )
    add_check(
        checks,
        "no_new_threads_or_old_spawn",
        nested(receipts["app_runner"], "policy", "new_threads_created") is False
        and nested(receipts["app_runner"], "policy", "old_style_spawn_used") is False,
        "existing app lanes only",
    )
    if args.app_redactor:
        add_check(
            checks,
            "app_redactor_passed",
            is_pass(receipts["app_redactor"], "PASS_APP_THREAD_REDACTION_GUARD"),
            status(receipts["app_redactor"]) or "missing",
        )
    if args.exposure_guard:
        add_check(
            checks,
            "exposure_guard_passed",
            is_pass(receipts["exposure_guard"], "PASS_EXPOSURE_GUARD"),
            status(receipts["exposure_guard"]) or "missing",
        )

    open_gaps = [row["name"] for row in checks if not row["passed"]]
    for name, payload in receipts.items():
        for gap in publication_gaps(name, payload):
            open_gaps.append(gap)

    return {
        "artifact_type": "launch_checklist_verifier",
        "phase_slug": args.phase_slug,
        "generated_utc": utc_now(),
        "overall_status": "PASS_LAUNCH_CHECKLIST" if not open_gaps else "OPEN_GAP_LAUNCH_CHECKLIST",
        "checks": checks,
        "open_gaps": open_gaps,
        "inputs": {
            key: payload.get("_receipt_file") if payload.get("_available") else payload.get("reason", "missing")
            for key, payload in receipts.items()
        },
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
        f"# {payload['phase_slug']} Launch Checklist Verifier",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: `{payload['overall_status']}`",
        "",
        "Checks:",
    ]
    for row in payload["checks"]:
        lines.append(f"- {row['name']}: `{row['passed']}` ({row['detail']})")
    lines.extend(["", "Open gaps:"])
    if payload["open_gaps"]:
        lines.extend(f"- `{gap}`" for gap in payload["open_gaps"])
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "Boundary: status-only receipts; no raw lane text, raw logs, prompt bodies, local absolute paths, screenshots, credentials, or session streams.",
            "",
            "Claim boundary: GMUT and canon gates remain open; duration is not completion proof.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--five-lane-launch", required=True)
    parser.add_argument("--app-runner", required=True)
    parser.add_argument("--prompt-contract", required=True)
    parser.add_argument("--heading-contract", required=True)
    parser.add_argument("--cli-launcher", required=True)
    parser.add_argument("--productive-wait", required=True)
    parser.add_argument("--app-redactor")
    parser.add_argument("--exposure-guard")
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
