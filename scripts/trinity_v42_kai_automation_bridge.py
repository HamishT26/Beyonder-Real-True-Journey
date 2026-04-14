#!/usr/bin/env python3
"""Run one bounded V42 Kai automation consultation cycle on the proven Gemini CLI lane."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from trinity_v36_cloud_common import (
    DEFAULT_MODEL_LOCATION,
    DEFAULT_REGIONAL_LOCATION,
    PROJECT_ID,
    build_vertex_env,
    extract_fenced_json,
    extract_last_json_object,
    load_compute_service_account,
)
from trinity_v42_common import ROOT, now_iso, read_json, safe_run, write_json, write_text

DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v42-kai-automation-bridge-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v42-kai-automation-bridge-v1.md"
PACKAGE_HINT = "@google/gemini-cli"


def _source_summary(path: Path) -> dict[str, Any]:
    payload = read_json(path)
    summary = {
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "present": path.exists(),
        "overall_status": str(payload.get("overall_status") or ""),
    }
    for key in (
        "api_ascendancy_state",
        "cloud_run_state",
        "cloud_build_state",
        "dataplex_state",
        "gke_telemetry_state",
        "wsl_codex_selector_state",
        "filesystem_promotion_state",
        "gmut_experiment_state",
        "agent_engine_advanced_state",
    ):
        if key in payload:
            summary[key] = payload[key]
    return summary


def _kai_prompt(source_summaries: list[dict[str, Any]]) -> str:
    return (
        "You are Kai, the already-proven Gemini CLI runtime lane for Beyonder-Real-True Journey. "
        "Review the bounded V42 automation and runtime summaries below and return fenced JSON only with keys "
        "`name`, `phase`, `kai_automation_state`, `headline`, `automation_lanes`, `alerts`, `recommended_followups`, and `confidence`. "
        "Stay concrete and do not invent extra capabilities.\n\n"
        f"Summaries:\n{json.dumps(source_summaries, indent=2)}"
    )


def _parse_kai(stdout: str) -> tuple[dict[str, Any], dict[str, Any], str]:
    top = extract_last_json_object(stdout)
    parsed: dict[str, Any] = {}
    if isinstance(top, dict) and top.get("kai_automation_state"):
        parsed = top
    else:
        parsed = extract_fenced_json(str(top.get("response") or "")) if isinstance(top, dict) else {}
        if not parsed:
            parsed = extract_fenced_json(stdout)
    selected_model = ""
    stats = top.get("stats", {}) if isinstance(top, dict) else {}
    if isinstance(stats, dict):
        models = stats.get("models", {})
        if isinstance(models, dict) and models:
            selected_model = str(next(iter(models.keys())))
    if not selected_model and isinstance(top, dict):
        selected_model = str(top.get("model") or top.get("resolved_model") or "")
    return top, parsed, selected_model


def _markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V42 Kai Automation Bridge",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Kai automation state: `{payload['kai_automation_state']}`",
        f"- Selected model: `{payload.get('selected_model', '') or 'unresolved'}`",
        f"- Manual cycle verified: `{payload.get('manual_cycle_verified', False)}`",
        "",
        "## Completed Steps",
        "",
    ]
    lines.extend(f"- `{row}`" for row in payload.get("completed_steps", []))
    if payload.get("blockers"):
        lines.extend(["", "## Blockers", ""])
        lines.extend(f"- {row}" for row in payload["blockers"])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one bounded V42 Kai automation cycle.")
    parser.add_argument("--bundle", default=str(Path.home() / "GCP service account keys.txt"))
    parser.add_argument("--project-id", default=PROJECT_ID)
    parser.add_argument("--regional-location", default=DEFAULT_REGIONAL_LOCATION)
    parser.add_argument("--model-location", default=DEFAULT_MODEL_LOCATION)
    parser.add_argument("--model-route", default="pro")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()

    sources = [
        ROOT / "docs" / "trinity-live-traces" / "v42-api-automation-wave-v1.json",
        ROOT / "docs" / "trinity-live-traces" / "v42-wsl-codex-probe-v1.json",
        ROOT / "docs" / "trinity-live-traces" / "v42-filesystem-promotion-proof-v1.json",
        ROOT / "docs" / "trinity-live-traces" / "v42-gmut-lab-bundle-v1.json",
        ROOT / "docs" / "trinity-live-traces" / "v40-agent-engine-advanced-probe-v1.json",
    ]
    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": "v42_omega",
        "overall_status": "WARN",
        "kai_automation_state": "pending",
        "manual_cycle_verified": False,
        "completed_steps": [],
        "blockers": [],
        "source_summaries": [_source_summary(path) for path in sources],
    }

    try:
        _records, primary, _minted = load_compute_service_account(Path(args.bundle))
    except Exception as exc:
        payload["overall_status"] = "FAIL"
        payload["kai_automation_state"] = "blocked_missing_identity"
        payload["blockers"].append(str(exc))
        write_json(Path(args.output_json), payload)
        write_text(Path(args.output_md), _markdown(payload))
        return 1

    env = build_vertex_env(
        primary,
        args.project_id,
        regional_location=args.regional_location,
        model_location=args.model_location,
        google_cloud_location=args.model_location,
    )

    help_run = safe_run(["npx", "--yes", PACKAGE_HINT, "--help"], env=env, timeout=180)
    payload["help_check"] = {
        "returncode": help_run.returncode,
        "stdout_excerpt": help_run.stdout[:1200],
        "stderr_excerpt": help_run.stderr[:1200],
    }
    if help_run.returncode != 0:
        payload["overall_status"] = "FAIL"
        payload["kai_automation_state"] = "cli_unavailable"
        payload["blockers"].append("Gemini CLI help invocation failed in the V42 Kai automation bridge.")
        write_json(Path(args.output_json), payload)
        write_text(Path(args.output_md), _markdown(payload))
        return 1
    payload["completed_steps"].append("gemini_cli_help_verified")

    kai_run = safe_run(
        [
            "npx",
            "--yes",
            PACKAGE_HINT,
            "-m",
            args.model_route,
            "-p",
            _kai_prompt(payload["source_summaries"]),
            "--output-format",
            "json",
        ],
        env=env,
        timeout=900,
    )
    top_level, kai_ack, selected_model = _parse_kai(kai_run.stdout)
    payload["kai_response"] = {
        "returncode": kai_run.returncode,
        "stdout_excerpt": kai_run.stdout[:4000],
        "stderr_excerpt": kai_run.stderr[:1200],
        "top_level": top_level,
        "ack": kai_ack,
    }
    payload["selected_model"] = selected_model
    if kai_run.returncode != 0 or not kai_ack:
        payload["overall_status"] = "FAIL"
        payload["kai_automation_state"] = "ack_missing"
        payload["blockers"].append("Kai did not return a bounded JSON automation acknowledgement.")
        write_json(Path(args.output_json), payload)
        write_text(Path(args.output_md), _markdown(payload))
        return 1

    payload["manual_cycle_verified"] = True
    payload["kai_automation_state"] = str(kai_ack.get("kai_automation_state") or "manual_cycle_verified")
    payload["kai_summary"] = kai_ack
    payload["overall_status"] = "PASS"
    payload["completed_steps"].extend(
        [
            "kai_automation_prompt_executed",
            "kai_automation_ack_verified",
            "verified_headless_bridge_execution",
        ]
    )
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), _markdown(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
