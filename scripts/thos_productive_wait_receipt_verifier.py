#!/usr/bin/env python3
"""Verify that a phase launch has an explicit productive-wait contract."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = REPO_ROOT / "docs" / "trinity-live-traces"


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"available": False}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"available": False, "parse_status": "json_error"}
    return payload if isinstance(payload, dict) else {"available": False, "parse_status": "not_object"}


def receipt_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    repo_relative = REPO_ROOT / path
    if repo_relative.exists():
        return repo_relative
    return TRACE_DIR / value


def truthy(payload: dict[str, Any], *keys: str) -> bool:
    current: Any = payload
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return False
        current = current[key]
    return current is True


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    launch_path = receipt_path(args.launch_receipt)
    wait_path = receipt_path(args.wait_plan)
    launch = read_json(launch_path)
    wait_plan = read_json(wait_path)

    wait_gate = wait_plan.get("wait_gate") if isinstance(wait_plan.get("wait_gate"), dict) else {}
    launch_policy = launch.get("launch_policy") if isinstance(launch.get("launch_policy"), dict) else {}
    has_next_check = bool(launch.get("next_manual_status_check_not_before_utc")) or bool(
        wait_gate.get("manual_status_check_not_before_utc")
    )
    manual_polling_disabled = launch.get("manual_polling_before_gate") is False or (
        launch_policy.get("manual_babysitting_required") is False and has_next_check
    )
    supervised_until_gate = launch.get("watchers_supervise_until_gate") is True or (
        launch_policy.get("manual_babysitting_required") is False and has_next_check
    )
    work_while_waiting_required = (
        launch.get("work_while_waiting_required") is True
        or truthy(launch, "policy", "work_while_waiting_required")
        or bool(wait_plan.get("productive_tasks"))
    )
    duration_is_not_completion_proof = launch.get("duration_is_completion_proof") is False or (
        launch_policy.get("duration_is_completion_proof") is False
    )

    checks = {
        "launch_receipt_available": bool(launch.get("artifact_type")),
        "wait_plan_available": bool(wait_plan.get("artifact_type")),
        "manual_polling_disabled": manual_polling_disabled,
        "watchers_supervise_until_gate": supervised_until_gate,
        "work_while_waiting_required": work_while_waiting_required,
        "duration_is_not_completion_proof": duration_is_not_completion_proof,
        "wait_plan_has_gate": isinstance(wait_plan.get("wait_gate"), dict),
    }
    open_gaps = [key for key, passed in checks.items() if not passed]
    return {
        "artifact_type": "productive_wait_receipt_verifier",
        "phase_slug": args.phase_slug,
        "generated_utc": utc_now(),
        "overall_status": "PASS_PRODUCTIVE_WAIT_RECEIPT_VERIFIER" if not open_gaps else "OPEN_GAP_PRODUCTIVE_WAIT_CONTRACT",
        "checks": checks,
        "open_gaps": open_gaps,
        "inputs": {
            "launch_receipt": launch_path.name,
            "wait_plan": wait_path.name,
        },
        "publication_boundary": {
            "raw_lane_text_published": False,
            "raw_logs_published": False,
            "local_absolute_paths_published": False,
        },
        "claim_boundary": {
            "gmut_gate_state": "open",
            "canon_promotion": "not_claimed",
        },
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['phase_slug']} Productive Wait Receipt Verifier",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: `{payload['overall_status']}`",
        "",
        "Checks:",
    ]
    for key, value in payload["checks"].items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "Open gaps:"])
    if payload["open_gaps"]:
        for gap in payload["open_gaps"]:
            lines.append(f"- `{gap}`")
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "Publication boundary: status only; no raw lane text, raw logs, local absolute paths, screenshots, credentials, or private dumps.",
            "",
            "Claim boundary: GMUT and canon gates remain open.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify productive waiting is explicitly recorded for a phase launch.")
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--launch-receipt", required=True)
    parser.add_argument("--wait-plan", required=True)
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
