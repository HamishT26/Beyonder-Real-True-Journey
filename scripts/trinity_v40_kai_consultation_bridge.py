#!/usr/bin/env python3
"""Use Kai's proven Gemini CLI route to analyze V40 proof surfaces."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

from trinity_v36_cloud_common import (
    DEFAULT_MODEL_LOCATION,
    DEFAULT_REGIONAL_LOCATION,
    PROJECT_ID,
    ROOT,
    build_vertex_env,
    extract_fenced_json,
    extract_last_json_object,
    load_compute_service_account,
    now_iso,
    write_json,
    write_text,
)

PACKAGE_HINT = "@google/gemini-cli"
OUTPUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v40-kai-consultation-bridge-v1.json"
OUTPUT_MD = ROOT / "docs" / "trinity-live-traces" / "v40-kai-consultation-bridge-v1.md"

DEFAULT_SOURCES = [
    ROOT / "docs" / "trinity-live-traces" / "v40-agent-engine-advanced-probe-v1.json",
    ROOT / "docs" / "trinity-live-traces" / "v40-runtime-truth-completion-v1.json",
    ROOT / "docs" / "trinity-live-traces" / "v40-pillar-bundle-v1.json",
    ROOT / "docs" / "trinity-live-traces" / "v40-quick-suite-status.json",
    ROOT / "docs" / "trinity-live-traces" / "v40-standard-suite-status.json",
    ROOT / "docs" / "trinity-live-traces" / "v40-deep-suite-status.json",
    ROOT / "docs" / "trinity-live-traces" / "v40-collab-suite-status.json",
    ROOT / "docs" / "trinity-live-traces" / "v40-materialize-l2-status.json",
    ROOT / "docs" / "trinity-live-traces" / "v40-materialize-l3-status.json",
    ROOT / "docs" / "trinity-live-traces" / "v40-materialize-l4-status.json",
    ROOT / "docs" / "trinity-live-traces" / "v40-materialize-l5-status.json",
]


def resolve_command(preferred: str) -> list[str]:
    candidates = [preferred]
    if not preferred.lower().endswith(".cmd"):
        candidates.insert(0, f"{preferred}.cmd")
    for candidate in candidates:
        resolved = shutil.which(candidate)
        if resolved:
            return [resolved]
    return [preferred]


def safe_run(args: list[str], *, env: dict[str, str] | None = None, timeout: int = 600) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            [*resolve_command(args[0]), *args[1:]],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        return subprocess.CompletedProcess(
            args=args,
            returncode=124,
            stdout=exc.stdout or "",
            stderr=(exc.stderr or "") + f"\ncommand timed out after {timeout} seconds",
        )
    except FileNotFoundError as exc:
        return subprocess.CompletedProcess(args=args, returncode=127, stdout="", stderr=str(exc))


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def summarize_source(path: Path) -> dict[str, Any]:
    payload = read_json(path)
    summary = {
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "present": path.exists(),
        "overall_status": str(payload.get("overall_status") or ""),
    }
    for key in (
        "agent_engine_advanced_state",
        "agent_engine_minimal_probe_state",
        "runtime_truth_complete",
        "runtime_truth_completion_ratio",
        "complete_agent_count",
        "pending_agent_count",
        "pillar_bundle_state",
        "counts",
        "blockers",
        "suite_duration_sec",
    ):
        if key in payload:
            summary[key] = payload[key]
    return summary


def kai_prompt(source_summaries: list[dict[str, Any]]) -> str:
    return (
        "You are Kai, the already-promoted Gemini CLI consultation lane for Beyonder-Real-True Journey. "
        "Review the bounded V40 summaries below and return fenced JSON only with keys "
        "`name`, `phase`, `consultation_state`, `headline`, `recommended_next_steps`, `residual_risks`, and `confidence`. "
        "Keep the response concrete, brief, and restricted to V40 pillar promotion, runtime truth, Agent Engine advanced interaction, and regression-safe publication.\n\n"
        f"Summaries:\n{json.dumps(source_summaries, indent=2)}"
    )


def parse_kai_response(stdout: str) -> tuple[dict[str, Any], dict[str, Any]]:
    top = extract_last_json_object(stdout)
    if isinstance(top, dict) and top.get("consultation_state"):
        return top, top
    response_text = str(top.get("response") or "")
    parsed = extract_fenced_json(response_text)
    return top, parsed


def write_outputs(payload: dict[str, Any], output_json: Path, output_md: Path) -> None:
    write_json(output_json, payload)
    lines = [
        "# V40 Kai Consultation Bridge",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Kai consultation state: `{payload['kai_consultation_state']}`",
        f"- Selected model: `{payload.get('selected_model', '') or 'unknown'}`",
        "",
        "## Completed Steps",
        "",
    ]
    lines.extend(f"- `{row}`" for row in payload.get("completed_steps", []))
    if payload.get("blockers"):
        lines.extend(["", "## Blockers", ""])
        lines.extend(f"- {row}" for row in payload["blockers"])
    write_text(output_md, "\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the bounded Kai V40 consultation bridge.")
    parser.add_argument("--bundle", default=str(Path.home() / "GCP service account keys.txt"))
    parser.add_argument("--project-id", default=PROJECT_ID)
    parser.add_argument("--regional-location", default=DEFAULT_REGIONAL_LOCATION)
    parser.add_argument("--model-location", default=DEFAULT_MODEL_LOCATION)
    parser.add_argument("--model-route", default="pro")
    parser.add_argument("--output-json", default=str(OUTPUT_JSON))
    parser.add_argument("--output-md", default=str(OUTPUT_MD))
    args = parser.parse_args()

    output_json = Path(args.output_json)
    output_md = Path(args.output_md)
    source_summaries = [summarize_source(path) for path in DEFAULT_SOURCES]
    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": "v40_omega",
        "overall_status": "WARN",
        "kai_consultation_state": "pending",
        "completed_steps": [],
        "blockers": [],
        "source_summaries": source_summaries,
    }

    try:
        _records, primary, _minted = load_compute_service_account(Path(args.bundle))
    except Exception as exc:
        payload["overall_status"] = "FAIL"
        payload["kai_consultation_state"] = "blocked_missing_identity"
        payload["blockers"].append(str(exc))
        write_outputs(payload, output_json, output_md)
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
        "stdout": help_run.stdout[:1200],
        "stderr": help_run.stderr[:1200],
    }
    if help_run.returncode != 0:
        payload["overall_status"] = "FAIL"
        payload["kai_consultation_state"] = "cli_unavailable"
        payload["blockers"].append("Gemini CLI help invocation failed in the V40 Kai consultation bridge.")
        write_outputs(payload, output_json, output_md)
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
            kai_prompt(source_summaries),
            "--output-format",
            "json",
        ],
        env=env,
        timeout=900,
    )
    top_level, kai_ack = parse_kai_response(kai_run.stdout)
    payload["kai_response"] = {
        "returncode": kai_run.returncode,
        "stdout_excerpt": kai_run.stdout[:4000],
        "stderr_excerpt": kai_run.stderr[:1200],
        "top_level": top_level,
        "ack": kai_ack,
    }
    stats = top_level.get("stats", {}) if isinstance(top_level, dict) else {}
    model_names = list((stats.get("models") or {}).keys()) if isinstance(stats, dict) else []
    if model_names:
        payload["selected_model"] = model_names[0]
    payload["kai_ack_captured"] = bool(kai_ack)
    payload["teardown_bug_observed"] = "Assertion failed:" in (kai_run.stderr or "")
    if not kai_ack:
        payload["overall_status"] = "FAIL"
        payload["kai_consultation_state"] = "ack_missing"
        payload["blockers"].append("Kai did not return a bounded JSON consultation for the V40 proof lane.")
        write_outputs(payload, output_json, output_md)
        return 1

    payload["kai_consultation_state"] = str(kai_ack.get("consultation_state") or "consultation_verified")
    payload["recommendations"] = kai_ack
    payload["overall_status"] = "PASS"
    payload["completed_steps"].extend(
        [
            "kai_consultation_prompt_executed",
            "kai_consultation_ack_verified",
            "headless_bridge_execution_verified",
        ]
    )
    write_outputs(payload, output_json, output_md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
