#!/usr/bin/env python3
"""Run the V36 live Agent Engine / Memory Bank proof in us-central1."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from trinity_v36_cloud_common import (
    DEFAULT_MODEL_LOCATION,
    DEFAULT_REGIONAL_LOCATION,
    LEGACY_PRIMARY_REGION,
    LOCAL_SITE_PACKAGES,
    PHASE,
    PRIMARY_STAGING_BUCKET,
    PROJECT_ID,
    ROOT,
    TRACE_DIR,
    VERTEX_SERVICE_NAME,
    best_effort_error_message,
    build_vertex_env,
    ensure_service_enabled,
    ensure_staging_bucket,
    extract_last_json_object,
    extract_reasoning_engine_refs,
    google_request,
    load_compute_service_account,
    memories_url,
    now_iso,
    primary_identity_fields,
    reasoning_engine_url,
    reasoning_engines_url,
    run_cmd,
    write_json,
    write_text,
)

OUTPUT_JSON = TRACE_DIR / "v36-memory-bank-proof-v1.json"
OUTPUT_MD = TRACE_DIR / "v36-memory-bank-proof-v1.md"
SYNC_REPORT = ROOT / "docs" / "trinity-memory-bank-sync-latest.json"
VALIDATION_REPORT = ROOT / "docs" / "trinity-memory-bank-validation-latest.json"
REGISTRY_PATH = ROOT / "docs" / "trinity-memory-bank-registry-v3.json"
OFFICIAL_URLS = {
    "overview": "https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/memory-bank/overview",
    "quickstart": "https://docs.cloud.google.com/agent-builder/agent-engine/memory-bank/quickstart-api",
}


def report_status(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"status": "missing", "path": str(path)}
    parsed = json.loads(path.read_text(encoding="utf-8"))
    return {"status": "present", "path": str(path), "parsed": parsed}


def extract_engine_names(parsed: Any) -> list[str]:
    if not isinstance(parsed, dict):
        return []
    rows = parsed.get("reasoningEngines", [])
    if not isinstance(rows, list):
        return []
    names: list[str] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        name = str(row.get("name") or "").strip()
        if name:
            names.append(name)
    return names


def run_live_agent_engine_probe(
    service_account_path: Path,
    project_id: str,
    regional_location: str,
    staging_bucket: str,
) -> dict[str, Any]:
    env = build_vertex_env(
        {"runtime_path": service_account_path},
        project_id,
        regional_location=regional_location,
        model_location=DEFAULT_MODEL_LOCATION,
        google_cloud_location=regional_location,
    )
    inline = f"""
import json
import sys
import traceback

site_packages = {str(LOCAL_SITE_PACKAGES)!r}
if site_packages and site_packages not in sys.path:
    sys.path.insert(0, site_packages)

result = {{
    "success": False,
    "project_id": {project_id!r},
    "regional_location": {regional_location!r},
    "staging_bucket": {staging_bucket!r},
}}

try:
    import vertexai
    from vertexai import agent_engines

    class V36ProbeAgent:
        def query(self, input: str) -> dict:
            return {{"echo": input, "token": "V36_MEMORY_BANK_OK"}}

    vertexai.init(project={project_id!r}, location={regional_location!r}, staging_bucket={staging_bucket!r})
    remote_app = agent_engines.create(
        agent_engine=V36ProbeAgent(),
        requirements=[],
        display_name="v36-memory-bank-probe",
        description="Bounded V36 Agent Engine proof",
    )
    result["success"] = True
    result["resource_name"] = str(getattr(remote_app, "resource_name", "") or getattr(remote_app, "name", ""))
    result["display_name"] = str(getattr(remote_app, "display_name", "") or "v36-memory-bank-probe")
except Exception as exc:
    result["exception_type"] = exc.__class__.__name__
    result["exception_message"] = str(exc)
    result["traceback"] = traceback.format_exc()[-12000:]

print(json.dumps(result))
"""
    try:
        proc = subprocess.run(
            [sys.executable, "-c", inline],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            timeout=1800,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        proc = subprocess.CompletedProcess(
            args=[sys.executable, "-c", inline],
            returncode=124,
            stdout=exc.stdout or "",
            stderr=(exc.stderr or "") + "\ncommand timed out after 1800 seconds",
        )
    parsed = extract_last_json_object(proc.stdout)
    return {
        "returncode": proc.returncode,
        "stdout": proc.stdout.strip()[-12000:],
        "stderr": proc.stderr.strip()[-12000:],
        "parsed": parsed,
    }


def write_outputs(payload: dict[str, Any], output_json: Path, output_md: Path, phase_label: str) -> None:
    write_json(output_json, payload)
    lines = [
        f"# {phase_label.upper()} Memory Bank Proof",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Proof state: `{payload['proof_state']}`",
        f"- Memory bank state: `{payload.get('memory_bank_state', 'unknown')}`",
        f"- Agent Engine state: `{payload.get('agent_engine_state', 'unknown')}`",
        f"- Regional location: `{payload.get('regional_location', '') or 'unresolved'}`",
        f"- Model location: `{payload.get('model_location', '') or 'unresolved'}`",
        "",
        "## Completed Steps",
        "",
    ]
    for step in payload.get("completed_steps", []):
        lines.append(f"- `{step}`")
    if payload.get("blockers"):
        lines.extend(["", "## Blockers", ""])
        for blocker in payload["blockers"]:
            lines.append(f"- {blocker}")
    write_text(output_md, "\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the V36 Memory Bank proof.")
    parser.add_argument("--bundle", default=str(Path.home() / "GCP service account keys.txt"))
    parser.add_argument("--project-id", default=PROJECT_ID)
    parser.add_argument("--regional-location", default=DEFAULT_REGIONAL_LOCATION)
    parser.add_argument("--model-location", default=DEFAULT_MODEL_LOCATION)
    parser.add_argument("--region", default="", help="Deprecated alias for --regional-location.")
    parser.add_argument("--phase-label", default=PHASE)
    parser.add_argument("--output-json", default=str(OUTPUT_JSON))
    parser.add_argument("--output-md", default=str(OUTPUT_MD))
    args = parser.parse_args()

    regional_location = args.regional_location or args.region or DEFAULT_REGIONAL_LOCATION
    output_json = Path(args.output_json)
    output_md = Path(args.output_md)
    phase_label = str(args.phase_label or PHASE)

    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": phase_label,
        "overall_status": "WARN",
        "proof_state": "pending",
        "memory_bank_state": "pending",
        "agent_engine_state": "pending",
        "promotion_gate_ready": False,
        "project_id": args.project_id,
        "regional_location": regional_location,
        "model_location": args.model_location,
        "legacy_primary_region": LEGACY_PRIMARY_REGION,
        "staging_bucket": PRIMARY_STAGING_BUCKET,
        "official_sources": OFFICIAL_URLS,
        "completed_steps": [],
        "blockers": [],
        "region_attempts": [],
    }

    try:
        _records, primary, minted = load_compute_service_account(Path(args.bundle))
    except Exception as exc:
        payload["proof_state"] = "missing_primary_service_account"
        payload["memory_bank_state"] = "blocked_missing_identity"
        payload["agent_engine_state"] = "blocked_missing_identity"
        payload["blockers"].append(str(exc))
        write_outputs(payload, output_json, output_md, phase_label)
        return 1

    payload.update(primary_identity_fields(primary, minted))
    token = minted["token"]
    payload["completed_steps"].append("mint_primary_token")

    service = ensure_service_enabled(args.project_id, token, VERTEX_SERVICE_NAME)
    payload["service_enablement"] = service
    if service["final_status"] != 200 or service["final_state"] != "ENABLED":
        payload["proof_state"] = "service_enablement_blocked"
        payload["memory_bank_state"] = "blocked_service_enablement"
        payload["agent_engine_state"] = "blocked_service_enablement"
        payload["blockers"].append("Vertex AI did not report `ENABLED` after the bounded service check.")
        write_outputs(payload, output_json, output_md, phase_label)
        return 1
    payload["completed_steps"].append("vertex_service_enabled")

    bucket_state = ensure_staging_bucket(args.project_id, token, PRIMARY_STAGING_BUCKET)
    payload["staging_bucket_state"] = bucket_state
    if bucket_state.get("final_status") != 200:
        payload["proof_state"] = "staging_bucket_blocked"
        payload["memory_bank_state"] = "blocked_staging_bucket"
        payload["agent_engine_state"] = "blocked_staging_bucket"
        payload["blockers"].append("The v36 us-central1 staging bucket could not be verified or created.")
        write_outputs(payload, output_json, output_md, phase_label)
        return 1
    payload["completed_steps"].append("staging_bucket_verified")

    sync_result = run_cmd([sys.executable, "scripts/trinity_memory_bank_sync.py", "--label", "v36-memory-bank"], timeout=900)
    payload["sync_run"] = {
        "returncode": sync_result.returncode,
        "stdout": sync_result.stdout.strip(),
        "stderr": sync_result.stderr.strip(),
    }
    if sync_result.returncode != 0:
        payload["proof_state"] = "repo_memory_bank_sync_blocked"
        payload["memory_bank_state"] = "blocked_repo_sync"
        payload["agent_engine_state"] = "unreached"
        payload["blockers"].append("The repo-side memory-bank sync script did not complete cleanly.")
        write_outputs(payload, output_json, output_md, phase_label)
        return 1
    payload["completed_steps"].append("repo_memory_bank_sync_ran")

    validator_result = run_cmd([sys.executable, "scripts/trinity_memory_bank_validator.py"], timeout=120)
    payload["validator_run"] = {
        "returncode": validator_result.returncode,
        "stdout": validator_result.stdout.strip(),
        "stderr": validator_result.stderr.strip(),
    }
    if validator_result.returncode != 0:
        payload["proof_state"] = "repo_memory_bank_validation_failed"
        payload["memory_bank_state"] = "blocked_repo_validation"
        payload["agent_engine_state"] = "unreached"
        payload["blockers"].append("The repo-side memory-bank validator reported a failure.")
        write_outputs(payload, output_json, output_md, phase_label)
        return 1
    payload["completed_steps"].append("repo_memory_bank_validator_ran")
    payload["sync_report"] = report_status(SYNC_REPORT)
    payload["validation_report"] = report_status(VALIDATION_REPORT)
    payload["registry_report"] = report_status(REGISTRY_PATH)

    live_probe = run_live_agent_engine_probe(primary["runtime_path"], args.project_id, regional_location, PRIMARY_STAGING_BUCKET)
    payload["live_agent_engine_create"] = live_probe
    live_parsed = live_probe.get("parsed", {})
    live_error_text = "\n".join(
        filter(
            None,
            [
                str(live_parsed.get("exception_message") or ""),
                live_probe.get("stderr", ""),
                live_probe.get("stdout", ""),
            ],
        )
    )
    resource_refs = extract_reasoning_engine_refs(live_error_text)
    payload["live_agent_engine_refs"] = resource_refs
    payload["completed_steps"].append("live_agent_engine_create_attempted")

    engine_response = google_request("GET", reasoning_engines_url(args.project_id, regional_location), token, timeout=120)
    engine_names = extract_engine_names(engine_response.get("parsed", {}))
    attempt: dict[str, Any] = {
        "regional_location": regional_location,
        "list_status": engine_response["status"],
        "engine_names": engine_names,
    }
    if resource_refs:
        region_refs = [ref for ref in resource_refs if f"/locations/{regional_location}/" in ref and "/operations/" not in ref]
        attempt["resource_refs"] = region_refs
        if region_refs:
            attempt["resource_probe"] = google_request("GET", reasoning_engine_url(regional_location, region_refs[0]), token, timeout=120)
    if engine_names:
        selected_engine = engine_names[0]
        memories = google_request("GET", memories_url(regional_location, selected_engine), token, timeout=120)
        attempt["selected_engine"] = selected_engine
        attempt["memories_status"] = memories["status"]
        attempt["memory_count"] = len(memories.get("parsed", {}).get("memories", [])) if isinstance(memories.get("parsed", {}), dict) else 0
    payload["region_attempts"].append(attempt)
    payload["visible_reasoning_engines"] = engine_names

    if live_parsed.get("success") and engine_names:
        payload["overall_status"] = "PASS"
        payload["proof_state"] = "agent_engine_memory_inventory_read_verified"
        payload["memory_bank_state"] = "live_inventory_read_verified"
        payload["agent_engine_state"] = "inventory_visible"
        payload["promotion_gate_ready"] = True
        payload["selected_region"] = regional_location
        payload["selected_agent_engine"] = engine_names[0]
        payload["completed_steps"].append("agent_engine_inventory_read")
        write_outputs(payload, output_json, output_md, phase_label)
        return 0

    payload["memory_bank_state"] = "repo_memory_bank_validated_live_start_failed"
    payload["agent_engine_state"] = "live_start_failed"
    payload["proof_state"] = "agent_engine_start_failed_after_upload"
    payload["blockers"].append(
        "The live Agent Engine create path staged successfully enough to attempt startup, but the reasoning engine failed to start and never stabilized into a visible Memory Bank session."
    )
    error_summary = best_effort_error_message(live_parsed, live_probe.get("stderr", ""))
    if error_summary:
        payload["blockers"].append(f"Live Agent Engine error: {error_summary}")
    if resource_refs:
        payload["blockers"].append("Observed reasoning-engine references: " + ", ".join(resource_refs[:4]))
    write_outputs(payload, output_json, output_md, phase_label)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
