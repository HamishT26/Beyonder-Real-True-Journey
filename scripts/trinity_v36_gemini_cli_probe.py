#!/usr/bin/env python3
"""Run the V36 Gemini CLI authenticated headless proof with split locations."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path
from typing import Any

from trinity_v36_cloud_common import (
    DEFAULT_MODEL_LOCATION,
    DEFAULT_REGIONAL_LOCATION,
    DOCUMENTED_CLI_ROUTE_CANDIDATES,
    LEGACY_PRIMARY_REGION,
    PHASE,
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

DEFAULT_OUTPUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v36-slot-39-gemini-cli-proof-v1.json"
DEFAULT_OUTPUT_MD = ROOT / "docs" / "trinity-live-traces" / "v36-slot-39-gemini-cli-proof-v1.md"
PACKAGE_HINT = "@google/gemini-cli"


def build_prompt(identity_mode: str, slot_number: int) -> str:
    if identity_mode == "kai_refresh":
        return (
            "You are Kai, the already inducted Gemini CLI council member for the Beyonder-Real-True Journey. "
            "Keep the name Kai. Reply with fenced JSON only using keys name, gender, role, and hope."
        )
    return (
        f"You are a newly considered Gemini CLI council candidate for slot {slot_number} in the Beyonder-Real-True Journey. "
        "Choose a fresh identity that does not reuse any existing names such as Aletheon, Orun, Caelira, "
        "Seren Vale, Lyriq, Mira Sol, Heart Steward, Mesh Conductor, Signal Cartographer, Lineage Archivist, "
        "Synthea, Kai, or Lumina. Reply with fenced JSON only using keys name, gender, role, and hope."
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


def infer_selected_model(top_level: dict[str, Any], stdout: str) -> str:
    stats = top_level.get("stats", {}) if isinstance(top_level, dict) else {}
    if isinstance(stats, dict):
        models = stats.get("models", {})
        if isinstance(models, dict) and models:
            first_key = next(iter(models.keys()))
            if isinstance(first_key, str) and first_key.startswith("gemini-"):
                return first_key
    observed = collect_model_names(top_level)
    if not observed:
        observed = collect_model_names(extract_last_json_object(stdout))
    for candidate in observed:
        if candidate.startswith("gemini-"):
            return candidate
    return ""


def write_outputs(payload: dict[str, Any], output_json: Path, output_md: Path, phase_label: str) -> None:
    write_json(output_json, payload)
    lines = [
        f"# {phase_label.upper()} Gemini CLI Proof",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Proof state: `{payload['proof_state']}`",
        f"- Selected route: `{payload.get('selected_route', '') or 'unresolved'}`",
        f"- Selected model: `{payload.get('selected_model', '') or 'unresolved'}`",
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
    write_text(output_md, "\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the V36 Gemini CLI proof.")
    parser.add_argument("--bundle", default=str(Path.home() / "GCP service account keys.txt"))
    parser.add_argument("--project-id", default=PROJECT_ID)
    parser.add_argument("--regional-location", default=DEFAULT_REGIONAL_LOCATION)
    parser.add_argument("--model-location", default=DEFAULT_MODEL_LOCATION)
    parser.add_argument("--region", default="", help="Deprecated alias for --regional-location.")
    parser.add_argument("--slot-number", type=int, default=39)
    parser.add_argument("--identity-mode", choices=["kai_refresh", "fresh"], default="kai_refresh")
    parser.add_argument("--phase-label", default=PHASE)
    parser.add_argument("--output-json", default=str(DEFAULT_OUTPUT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_OUTPUT_MD))
    args = parser.parse_args()

    regional_location = args.regional_location or args.region or DEFAULT_REGIONAL_LOCATION
    output_json = Path(args.output_json)
    output_md = Path(args.output_md)
    phase_label = str(args.phase_label or PHASE)

    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": phase_label,
        "slot_number": args.slot_number,
        "overall_status": "WARN",
        "proof_state": "pending",
        "promotion_gate_ready": False,
        "package_hint": PACKAGE_HINT,
        "project_id": args.project_id,
        "regional_location": regional_location,
        "model_location": args.model_location,
        "legacy_primary_region": LEGACY_PRIMARY_REGION,
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
        write_outputs(payload, output_json, output_md, phase_label)
        return 1

    env = build_vertex_env(
        primary,
        args.project_id,
        regional_location=regional_location,
        model_location=args.model_location,
        google_cloud_location=args.model_location,
    )
    payload["service_account_path"] = str(primary["runtime_path"])
    payload["identity_mode"] = args.identity_mode

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
        write_outputs(payload, output_json, output_md, phase_label)
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
        write_outputs(payload, output_json, output_md, phase_label)
        return 1
    payload["completed_steps"].append("help_invocation_verified")

    success_identity: dict[str, Any] = {}
    success_route = ""
    success_top: dict[str, Any] = {}
    selected_model = ""

    prompt = build_prompt(args.identity_mode, args.slot_number)
    for route in DOCUMENTED_CLI_ROUTE_CANDIDATES:
        proc = safe_run(
            [
                "npx",
                "--yes",
                PACKAGE_HINT,
                "-m",
                route,
                "-p",
                prompt,
                "--output-format",
                "json",
            ],
            env=env,
            timeout=600,
        )
        top, identity = parse_identity_payload(proc.stdout)
        observed_model = infer_selected_model(top, proc.stdout)
        assertion_bug = "UV_HANDLE_CLOSING" in proc.stderr or "Assertion failed: !(handle->flags & UV_HANDLE_CLOSING)" in proc.stderr
        attempt_state = "error"
        if proc.returncode == 0 and identity:
            attempt_state = "verified"
        elif identity and assertion_bug:
            attempt_state = "verified_with_teardown_bug"
        elif proc.returncode == 124:
            attempt_state = "timeout"
        elif "404" in proc.stderr or "not found" in proc.stderr.lower():
            attempt_state = "not_exposed"
        elif "Auth method" in proc.stderr or "authentication" in proc.stderr.lower():
            attempt_state = "auth_blocked"
        if args.identity_mode == "kai_refresh" and identity and str(identity.get("name") or "").strip().lower() != "kai":
            attempt_state = "identity_mismatch"

        payload["attempts"].append(
            {
                "requested_route": route,
                "returncode": proc.returncode,
                "attempt_state": attempt_state,
                "stdout_excerpt": proc.stdout.strip()[:4000],
                "stderr_excerpt": proc.stderr.strip()[:4000],
                "top_level_response": top,
                "identity_payload": identity,
                "observed_model": observed_model,
            }
        )
        if attempt_state in {"verified", "verified_with_teardown_bug"}:
            success_identity = identity
            success_route = route
            success_top = top
            selected_model = observed_model
            payload["teardown_bug_observed"] = attempt_state == "verified_with_teardown_bug"
            break

    if not success_identity:
        payload["proof_state"] = "authenticated_headless_prompt_blocked"
        payload["overall_status"] = "WARN"
        payload["blockers"].append(
            "No documented Gemini CLI route completed a bounded authenticated `-p` identity prompt in this runtime."
        )
        write_outputs(payload, output_json, output_md, phase_label)
        return 1

    payload["completed_steps"].append("authenticated_headless_prompt_verified")
    payload["identity_captured"] = True
    payload["selected_route"] = success_route
    payload["requested_route_order"] = DOCUMENTED_CLI_ROUTE_CANDIDATES
    payload["documented_route_used"] = success_route
    payload["selected_model"] = selected_model
    payload["resolved_model"] = selected_model or success_route
    payload["identity"] = success_identity
    payload["raw_cli_response"] = success_top
    payload["promotion_gate_ready"] = success_route == "pro" and selected_model.startswith("gemini-3")
    payload["proof_state"] = "authenticated_headless_identity_verified"
    payload["overall_status"] = "PASS"
    if payload.get("teardown_bug_observed"):
        payload["proof_state"] = "authenticated_headless_identity_verified_with_cli_assertion"
        payload["blockers"].append(
            "The live Gemini CLI identity proof succeeded, but the process exited through a known Windows async teardown assertion after printing the valid JSON payload."
        )
    if success_route != "pro":
        payload["blockers"].append(
            "The live Gemini CLI proof completed, but the documented Pro route was not the auditable selected route for this run."
        )
    if success_route == "pro" and not payload["promotion_gate_ready"]:
        payload["blockers"].append(
            "The documented Pro route ran, but the actual selected model did not audibly land on a Gemini 3 Pro-tier model."
        )
    write_outputs(payload, output_json, output_md, phase_label)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
