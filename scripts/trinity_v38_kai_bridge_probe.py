#!/usr/bin/env python3
"""Bounded Kai-led bridge for V38 whitelisted headless shell workflows."""

from __future__ import annotations

import argparse
import json
import os
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
    collect_model_names,
    extract_fenced_json,
    extract_last_json_object,
    load_compute_service_account,
    now_iso,
    write_json,
    write_text,
)

PACKAGE_HINT = "@google/gemini-cli"
DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v38-kai-bridge-proof-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v38-kai-bridge-proof-v1.md"
SCRUBBED_EXECUTION_ENV_KEYS = (
    "GOOGLE_APPLICATION_CREDENTIALS",
    "GOOGLE_CLOUD_PROJECT",
    "GOOGLE_CLOUD_LOCATION",
    "GOOGLE_GENAI_USE_VERTEXAI",
    "VERTEX_LOCATION",
)


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


def command_plan(operation: str) -> list[list[str]]:
    if operation == "status":
        return [
            ["git", "status", "--short", "--branch"],
            ["python", "scripts/v17_runtime_session_guard.py", "--fail-on-warn"],
        ]
    if operation == "quick":
        return [["python", "scripts/run_all_trinity_systems.py", "--profile", "quick", "--step-timeout-sec", "0", "--fail-on-warn"]]
    if operation == "standard":
        return [["python", "scripts/run_all_trinity_systems.py", "--profile", "standard", "--step-timeout-sec", "0", "--fail-on-warn"]]
    if operation == "deep":
        return [["python", "scripts/run_all_trinity_systems.py", "--profile", "deep", "--step-timeout-sec", "0", "--fail-on-warn"]]
    if operation == "proof-refresh":
        return [
            [
                "python",
                "scripts/trinity_v36_gemini_cli_probe.py",
                "--phase-label",
                "v38_omega",
                "--output-json",
                "docs/trinity-live-traces/v38-slot-39-gemini-cli-proof-v1.json",
                "--output-md",
                "docs/trinity-live-traces/v38-slot-39-gemini-cli-proof-v1.md",
            ]
        ]
    raise ValueError(f"Unsupported Kai bridge operation: {operation}")


def status_source_for(operation: str) -> str:
    if operation == "quick":
        return "docs/v17-system-suite-status-latest.json"
    if operation in {"standard", "deep"}:
        return "docs/system-suite-status.json"
    if operation == "proof-refresh":
        return "docs/trinity-live-traces/v38-slot-39-gemini-cli-proof-v1.json"
    return "docs/v17-runtime-session-validation-latest.json"


def kai_prompt(operation: str) -> str:
    return (
        "You are Kai, the already inducted Gemini CLI council member for the Beyonder-Real-True Journey. "
        f"Acknowledge the bounded whitelisted operation `{operation}`. "
        "Return fenced JSON only with keys name, operation, safety, and next_action. "
        "This is the V38 Anthos Ascendancy phase and the response must stay concise and auditable."
    )


def parse_kai_response(stdout: str) -> tuple[dict[str, Any], dict[str, Any], str]:
    top = extract_last_json_object(stdout)
    response_text = str(top.get("response") or "")
    parsed = extract_fenced_json(response_text)
    models = collect_model_names(top)
    selected_model = ""
    for candidate in models:
        if candidate.startswith("gemini-"):
            selected_model = candidate
            break
    if not selected_model and isinstance(top.get("stats"), dict):
        stats_models = top["stats"].get("models", {})
        if isinstance(stats_models, dict) and stats_models:
            selected_model = str(next(iter(stats_models.keys())))
    return top, parsed, selected_model


def write_outputs(payload: dict[str, Any], output_json: Path, output_md: Path) -> None:
    write_json(output_json, payload)
    lines = [
        "# V38 Kai Bridge Proof",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Operation: `{payload['operation']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Selected model: `{payload.get('selected_model', '') or 'unresolved'}`",
        f"- Kai ack captured: `{payload.get('kai_ack_captured', False)}`",
        "",
        "## Completed Steps",
        "",
    ]
    lines.extend([f"- `{row}`" for row in payload.get("completed_steps", [])])
    if payload.get("blockers"):
        lines.extend(["", "## Blockers", ""])
        lines.extend([f"- {row}" for row in payload["blockers"]])
    write_text(output_md, "\n".join(lines) + "\n")


def command_execution_env(operation: str, bridge_env: dict[str, str]) -> tuple[dict[str, str], list[str]]:
    """Keep Kai's own proof lane on Vertex auth while local workflows run without credential leakage."""
    if operation == "proof-refresh":
        return bridge_env, []

    env = dict(os.environ)
    removed: list[str] = []
    for key in SCRUBBED_EXECUTION_ENV_KEYS:
        if key in env:
            removed.append(key)
            env.pop(key, None)
    return env, removed


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the bounded Kai V38 headless bridge.")
    parser.add_argument("--bundle", default=str(Path.home() / "GCP service account keys.txt"))
    parser.add_argument("--project-id", default=PROJECT_ID)
    parser.add_argument("--regional-location", default=DEFAULT_REGIONAL_LOCATION)
    parser.add_argument("--model-location", default=DEFAULT_MODEL_LOCATION)
    parser.add_argument("--operation", choices=["status", "quick", "standard", "deep", "proof-refresh"], default="status")
    parser.add_argument("--model-route", default="pro")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--status-snapshot", default="")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()

    output_json = Path(args.output_json)
    output_md = Path(args.output_md)
    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": "v38_omega",
        "operation": args.operation,
        "overall_status": "WARN",
        "completed_steps": [],
        "blockers": [],
        "command_runs": [],
    }

    try:
        _records, primary, _minted = load_compute_service_account(Path(args.bundle))
    except Exception as exc:
        payload["overall_status"] = "FAIL"
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
    payload["service_account_path"] = str(primary["runtime_path"])

    help_run = safe_run(["npx", "--yes", PACKAGE_HINT, "--help"], env=env, timeout=180)
    payload["help_check"] = {
        "returncode": help_run.returncode,
        "stdout": help_run.stdout[:1200],
        "stderr": help_run.stderr[:1200],
    }
    if help_run.returncode != 0:
        payload["overall_status"] = "FAIL"
        payload["blockers"].append("Gemini CLI help invocation failed inside the Kai bridge.")
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
            kai_prompt(args.operation),
            "--output-format",
            "json",
        ],
        env=env,
        timeout=600,
    )
    top_level, kai_ack, selected_model = parse_kai_response(kai_run.stdout)
    payload["kai_response"] = {
        "returncode": kai_run.returncode,
        "stdout_excerpt": kai_run.stdout[:4000],
        "stderr_excerpt": kai_run.stderr[:1200],
        "top_level": top_level,
        "ack": kai_ack,
    }
    payload["selected_model"] = selected_model
    payload["kai_ack_captured"] = bool(kai_ack)
    payload["teardown_bug_observed"] = "Assertion failed:" in (kai_run.stderr or "")
    if not kai_ack:
        payload["overall_status"] = "FAIL"
        payload["blockers"].append("Kai did not return a bounded JSON acknowledgement for the requested operation.")
        write_outputs(payload, output_json, output_md)
        return 1
    if kai_run.returncode != 0 and not payload["teardown_bug_observed"]:
        payload["overall_status"] = "FAIL"
        payload["blockers"].append("Kai returned a non-zero exit code before the bounded bridge could be trusted.")
        write_outputs(payload, output_json, output_md)
        return 1
    payload["completed_steps"].append("kai_acknowledgement_verified")

    planned_commands = command_plan(args.operation)
    payload["planned_commands"] = planned_commands
    command_env, removed_env_keys = command_execution_env(args.operation, env)
    if args.operation == "proof-refresh":
        payload["command_execution_env_mode"] = "bridge_vertex"
    else:
        payload["command_execution_env_mode"] = "scrubbed_local" if removed_env_keys else "local_process_env"
    payload["command_execution_removed_env_keys"] = removed_env_keys
    if args.execute:
        for command in planned_commands:
            proc = safe_run(command, env=command_env, timeout=7200 if args.operation in {"standard", "deep"} else 1800)
            payload["command_runs"].append(
                {
                    "command": command,
                    "returncode": proc.returncode,
                    "stdout_excerpt": proc.stdout[-4000:],
                    "stderr_excerpt": proc.stderr[-2000:],
                }
            )
            if proc.returncode != 0:
                payload["overall_status"] = "FAIL"
                payload["blockers"].append(f"Command failed: {' '.join(command)}")
                write_outputs(payload, output_json, output_md)
                return 1
        payload["completed_steps"].append("whitelisted_commands_executed")
    else:
        payload["completed_steps"].append("execution_skipped")

    status_source = ROOT / status_source_for(args.operation)
    snapshot_path = Path(args.status_snapshot) if args.status_snapshot else output_json.with_name(f"{output_json.stem}-{args.operation}-snapshot.json")
    if status_source.exists():
        snapshot_path.parent.mkdir(parents=True, exist_ok=True)
        snapshot_path.write_text(status_source.read_text(encoding="utf-8-sig"), encoding="utf-8")
        payload["status_snapshot_path"] = str(snapshot_path)
        payload["status_snapshot_source"] = str(status_source)
        payload["completed_steps"].append("status_snapshot_copied")

    payload["overall_status"] = "PASS"
    write_outputs(payload, output_json, output_md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
