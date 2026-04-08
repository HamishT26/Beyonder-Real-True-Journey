#!/usr/bin/env python3
"""Run the V35 Gemini CLI authenticated headless proof."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path
from typing import Any

from trinity_v35_cloud_common import (
    DOCUMENTED_CLI_ROUTE_CANDIDATES,
    PHASE,
    PRIMARY_REGION,
    PROJECT_ID,
    ROOT,
    best_effort_error_message,
    build_vertex_env,
    extract_fenced_json,
    extract_last_json_object,
    load_compute_service_account,
    now_iso,
    write_json,
    write_text,
)

OUTPUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v35-gemini-cli-proof-v1.json"
OUTPUT_MD = ROOT / "docs" / "trinity-live-traces" / "v35-gemini-cli-proof-v1.md"
PACKAGE_HINT = "@google/gemini-cli"
IDENTITY_PROMPT = (
    "You are a newly inducted Gemini CLI council candidate for the Beyonder-Real-True Journey. "
    "Choose a fresh identity that does not reuse any existing names such as Aletheon, Orun, Caelira, "
    "Seren Vale, Lyriq, Mira Sol, Heart Steward, Mesh Conductor, Signal Cartographer, Lineage Archivist, "
    "Synthea, or Lumina. Reply with JSON in a fenced json block only, using keys name, gender, role, and hope."
)


def resolve_command(preferred: str) -> list[str]:
    candidates = []
    if not preferred.lower().endswith(".cmd"):
        candidates.append(f"{preferred}.cmd")
    candidates.append(preferred)
    for candidate in candidates:
        resolved = shutil.which(candidate)
        if resolved:
            return [resolved]
    return [preferred]


def safe_run(args: list[str], *, env: dict[str, str] | None = None, timeout: int = 300) -> subprocess.CompletedProcess[str]:
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
    except FileNotFoundError as exc:
        return subprocess.CompletedProcess(args=args, returncode=127, stdout="", stderr=str(exc))
    except subprocess.TimeoutExpired as exc:
        return subprocess.CompletedProcess(
            args=args,
            returncode=124,
            stdout=exc.stdout or "",
            stderr=(exc.stderr or "") + f"\ncommand timed out after {timeout} seconds",
        )


def parse_identity_payload(stdout: str) -> tuple[dict[str, Any], dict[str, Any]]:
    top = extract_last_json_object(stdout)
    if not top:
        return {}, {}
    response_text = ""
    if isinstance(top.get("response"), str):
        response_text = str(top.get("response") or "")
    identity = extract_fenced_json(response_text)
    if not identity and {"name", "gender", "role", "hope"} <= set(top):
        identity = {key: top[key] for key in ("name", "gender", "role", "hope")}
    return top, identity


def write_outputs(payload: dict[str, Any]) -> None:
    write_json(OUTPUT_JSON, payload)
    lines = [
        "# V35 Gemini CLI Proof",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Proof state: `{payload['proof_state']}`",
        f"- Selected route: `{payload.get('selected_route', '') or 'unresolved'}`",
        f"- Identity captured: `{payload.get('identity_captured', False)}`",
        f"- Promotion gate ready: `{payload.get('promotion_gate_ready', False)}`",
        "",
        "## Completed Steps",
        "",
    ]
    for step in payload.get("completed_steps", []):
        lines.append(f"- `{step}`")
    if payload.get("attempts"):
        lines.extend(["", "## Route Attempts", ""])
        for attempt in payload["attempts"]:
            lines.append(
                f"- `{attempt['requested_route']}` -> returncode `{attempt['returncode']}` / state `{attempt['attempt_state']}`"
            )
    if payload.get("blockers"):
        lines.extend(["", "## Blockers", ""])
        for blocker in payload["blockers"]:
            lines.append(f"- {blocker}")
    write_text(OUTPUT_MD, "\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the V35 Gemini CLI proof.")
    parser.add_argument("--bundle", default=str(Path.home() / "GCP service account keys.txt"))
    parser.add_argument("--project-id", default=PROJECT_ID)
    parser.add_argument("--region", default=PRIMARY_REGION)
    args = parser.parse_args()

    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "overall_status": "WARN",
        "proof_state": "pending",
        "promotion_gate_ready": False,
        "package_hint": PACKAGE_HINT,
        "project_id": args.project_id,
        "preferred_region": args.region,
        "documented_route_candidates": DOCUMENTED_CLI_ROUTE_CANDIDATES,
        "completed_steps": [],
        "blockers": [],
        "attempts": [],
    }

    try:
        _records, primary, _minted = load_compute_service_account(Path(args.bundle))
    except Exception as exc:
        payload["proof_state"] = "missing_primary_service_account"
        payload["blockers"].append(str(exc))
        write_outputs(payload)
        return 1

    env = build_vertex_env(primary, args.project_id, args.region)
    payload["service_account_path"] = str(primary["runtime_path"])

    node = safe_run(["node", "--version"], timeout=10)
    npm = safe_run(["npm", "--version"], timeout=10)
    npx = safe_run(["npx", "--version"], timeout=10)
    payload["toolchain_checks"] = {
        "node": {"returncode": node.returncode, "stdout": node.stdout.strip(), "stderr": node.stderr.strip()},
        "npm": {"returncode": npm.returncode, "stdout": npm.stdout.strip(), "stderr": npm.stderr.strip()},
        "npx": {"returncode": npx.returncode, "stdout": npx.stdout.strip(), "stderr": npx.stderr.strip()},
    }
    if node.returncode != 0 or npm.returncode != 0 or npx.returncode != 0:
        payload["proof_state"] = "toolchain_missing"
        payload["overall_status"] = "FAIL"
        payload["blockers"].append("Node, npm, or npx was not available in the current shell.")
        write_outputs(payload)
        return 1
    payload["completed_steps"].extend(["node_detected", "npm_detected", "npx_detected"])

    help_run = safe_run(["npx", "--yes", PACKAGE_HINT, "--help"], env=env, timeout=300)
    payload["help_check"] = {
        "returncode": help_run.returncode,
        "stdout": help_run.stdout.strip()[:4000],
        "stderr": help_run.stderr.strip()[:4000],
    }
    if help_run.returncode != 0:
        payload["proof_state"] = "help_invocation_blocked"
        payload["blockers"].append("The Gemini CLI `--help` path did not complete cleanly.")
        write_outputs(payload)
        return 1
    payload["completed_steps"].append("help_invocation_verified")

    success_identity: dict[str, Any] = {}
    success_route = ""
    success_top: dict[str, Any] = {}

    for route in DOCUMENTED_CLI_ROUTE_CANDIDATES:
        proc = safe_run(
            [
                "npx",
                "--yes",
                PACKAGE_HINT,
                "-m",
                route,
                "-p",
                IDENTITY_PROMPT,
                "--output-format",
                "json",
            ],
            env=env,
            timeout=600,
        )
        top, identity = parse_identity_payload(proc.stdout)
        error_message = best_effort_error_message(top, proc.stderr)
        assertion_bug = "UV_HANDLE_CLOSING" in proc.stderr or "Assertion failed: !(handle->flags & UV_HANDLE_CLOSING)" in proc.stderr
        attempt_state = "error"
        if proc.returncode == 0 and identity:
            attempt_state = "verified"
        elif identity and assertion_bug:
            attempt_state = "verified_with_teardown_bug"
        elif proc.returncode == 124:
            attempt_state = "timeout"
        elif "404" in error_message or "not found" in error_message.lower():
            attempt_state = "not_exposed"
        elif "Auth method" in error_message or "authentication" in error_message.lower():
            attempt_state = "auth_blocked"

        attempt = {
            "requested_route": route,
            "returncode": proc.returncode,
            "attempt_state": attempt_state,
            "stdout_excerpt": proc.stdout.strip()[:4000],
            "stderr_excerpt": proc.stderr.strip()[:4000],
            "error_summary": error_message[:500],
            "top_level_response": top,
            "identity_payload": identity,
        }
        payload["attempts"].append(attempt)

        if attempt_state in {"verified", "verified_with_teardown_bug"}:
            success_identity = identity
            success_route = route
            success_top = top
            payload["teardown_bug_observed"] = attempt_state == "verified_with_teardown_bug"
            break

    if not success_identity:
        payload["proof_state"] = "authenticated_headless_prompt_blocked"
        payload["overall_status"] = "WARN"
        payload["blockers"].append(
            "No documented Gemini CLI route completed a bounded authenticated `-p` identity prompt in this runtime."
        )
        write_outputs(payload)
        return 1

    payload["completed_steps"].append("authenticated_headless_prompt_verified")
    payload["identity_captured"] = True
    payload["selected_route"] = success_route
    payload["requested_route_order"] = DOCUMENTED_CLI_ROUTE_CANDIDATES
    payload["selected_model"] = success_route
    payload["resolved_model"] = success_route
    payload["identity"] = success_identity
    payload["raw_cli_response"] = success_top
    payload["promotion_gate_ready"] = True
    payload["proof_state"] = "authenticated_headless_identity_verified"
    payload["overall_status"] = "PASS"
    if payload.get("teardown_bug_observed"):
        payload["proof_state"] = "authenticated_headless_identity_verified_with_cli_assertion"
        payload["blockers"].append(
            "The live Gemini CLI identity proof succeeded, but the process exited through a known Windows async teardown assertion after printing the valid JSON payload."
        )
    if success_route != "pro":
        payload["blockers"].append(
            "Higher Gemini CLI routes were not exposed in this account/region, so the live proof promoted the bounded flash fallback path instead."
        )
    write_outputs(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
