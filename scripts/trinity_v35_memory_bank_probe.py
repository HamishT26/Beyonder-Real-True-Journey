#!/usr/bin/env python3
"""Run the V35 live Agent Engine / Memory Bank proof."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from trinity_v35_cloud_common import (
    LOCAL_SITE_PACKAGES,
    MEMORY_BANK_REGIONS,
    PHASE,
    PRIMARY_REGION,
    PRIMARY_STAGING_BUCKET,
    PROJECT_ID,
    ROOT,
    TRACE_DIR,
    VERTEX_SERVICE_NAME,
    best_effort_error_message,
    build_vertex_env,
    ensure_service_enabled,
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

OUTPUT_JSON = TRACE_DIR / "v35-memory-bank-proof-v1.json"
OUTPUT_MD = TRACE_DIR / "v35-memory-bank-proof-v1.md"
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
    region: str,
    staging_bucket: str,
) -> dict[str, Any]:
    env = build_vertex_env(
        {"runtime_path": service_account_path},
        project_id,
        region,
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
    "region": {region!r},
    "staging_bucket": {staging_bucket!r},
}}

try:
    import vertexai
    from vertexai import agent_engines

    class V35ProbeAgent:
        def query(self, input: str) -> dict:
            return {{"echo": input, "token": "V35_MEMORY_BANK_OK"}}

    vertexai.init(project={project_id!r}, location={region!r}, staging_bucket={staging_bucket!r})
    remote_app = agent_engines.create(
        agent_engine=V35ProbeAgent(),
        requirements=[],
        display_name="v35-memory-bank-probe",
        description="Bounded V35 Agent Engine proof",
    )
    result["success"] = True
    result["resource_name"] = str(getattr(remote_app, "resource_name", "") or getattr(remote_app, "name", ""))
    result["display_name"] = str(getattr(remote_app, "display_name", "") or "v35-memory-bank-probe")
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


def write_outputs(payload: dict[str, Any]) -> None:
    write_json(OUTPUT_JSON, payload)
    lines = [
        "# V35 Memory Bank Proof",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Proof state: `{payload['proof_state']}`",
        f"- Memory bank state: `{payload.get('memory_bank_state', 'unknown')}`",
        f"- Agent Engine state: `{payload.get('agent_engine_state', 'unknown')}`",
        f"- Selected region: `{payload.get('selected_region', '') or 'unresolved'}`",
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
    write_text(OUTPUT_MD, "\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the V35 Memory Bank proof.")
    parser.add_argument("--bundle", default=str(Path.home() / "GCP service account keys.txt"))
    parser.add_argument("--project-id", default=PROJECT_ID)
    parser.add_argument("--region", default=PRIMARY_REGION)
    args = parser.parse_args()

    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "overall_status": "WARN",
        "proof_state": "pending",
        "memory_bank_state": "pending",
        "agent_engine_state": "pending",
        "promotion_gate_ready": False,
        "project_id": args.project_id,
        "preferred_regions": MEMORY_BANK_REGIONS,
        "preferred_region": args.region,
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
        write_outputs(payload)
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
        write_outputs(payload)
        return 1
    payload["completed_steps"].append("vertex_service_enabled")

    sync_result = run_cmd([sys.executable, "scripts/trinity_memory_bank_sync.py", "--label", "v35-memory-bank"], timeout=900)
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
        write_outputs(payload)
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
        write_outputs(payload)
        return 1
    payload["completed_steps"].append("repo_memory_bank_validator_ran")
    payload["sync_report"] = report_status(SYNC_REPORT)
    payload["validation_report"] = report_status(VALIDATION_REPORT)
    payload["registry_report"] = report_status(REGISTRY_PATH)

    live_probe = run_live_agent_engine_probe(primary["runtime_path"], args.project_id, args.region, PRIMARY_STAGING_BUCKET)
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

    for region in MEMORY_BANK_REGIONS:
        engine_response = google_request("GET", reasoning_engines_url(args.project_id, region), token, timeout=120)
        engine_names = extract_engine_names(engine_response.get("parsed", {}))
        attempt: dict[str, Any] = {
            "region": region,
            "list_status": engine_response["status"],
            "engine_names": engine_names,
        }
        if resource_refs:
            region_refs = [ref for ref in resource_refs if f"/locations/{region}/" in ref and "/operations/" not in ref]
            attempt["resource_refs"] = region_refs
            if region_refs:
                attempt["resource_probe"] = google_request("GET", reasoning_engine_url(region, region_refs[0]), token, timeout=120)
        if engine_names:
            selected_engine = engine_names[0]
            memories = google_request("GET", memories_url(region, selected_engine), token, timeout=120)
            attempt["selected_engine"] = selected_engine
            attempt["memories_status"] = memories["status"]
            attempt["memory_count"] = len(memories.get("parsed", {}).get("memories", [])) if isinstance(memories.get("parsed", {}), dict) else 0
        payload["region_attempts"].append(attempt)

    visible_engines = [
        engine
        for attempt in payload["region_attempts"]
        for engine in attempt.get("engine_names", [])
        if str(engine).strip()
    ]
    payload["visible_reasoning_engines"] = visible_engines

    if live_parsed.get("success") and visible_engines:
        payload["overall_status"] = "PASS"
        payload["proof_state"] = "agent_engine_memory_inventory_read_verified"
        payload["memory_bank_state"] = "live_inventory_read_verified"
        payload["agent_engine_state"] = "inventory_visible"
        payload["promotion_gate_ready"] = True
        payload["selected_region"] = args.region
        payload["selected_agent_engine"] = visible_engines[0]
        payload["completed_steps"].append("agent_engine_inventory_read")
        write_outputs(payload)
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
        payload["blockers"].append(
            "Observed reasoning-engine references: " + ", ".join(resource_refs[:4])
        )
    write_outputs(payload)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
