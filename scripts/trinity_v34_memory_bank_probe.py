#!/usr/bin/env python3
"""Run the bounded V34 Agent Engine / Memory Bank proof."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from trinity_v34_cloud_common import (
    MEMORY_BANK_REGIONS,
    PHASE,
    PROJECT_ID,
    ROOT,
    TRACE_DIR,
    VERTEX_SERVICE_NAME,
    ensure_service_enabled,
    google_request,
    load_primary_service_account,
    mask_email,
    now_iso,
    run_cmd,
    write_json,
    write_text,
)

OUTPUT_JSON = TRACE_DIR / "v34-memory-bank-proof-v1.json"
OUTPUT_MD = TRACE_DIR / "v34-memory-bank-proof-v1.md"
SYNC_REPORT = ROOT / "docs" / "trinity-memory-bank-sync-latest.json"
VALIDATION_REPORT = ROOT / "docs" / "trinity-memory-bank-validation-latest.json"
REGISTRY_PATH = ROOT / "docs" / "trinity-memory-bank-registry-v3.json"
OFFICIAL_URLS = {
    "overview": "https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/memory-bank/overview",
    "quickstart": "https://docs.cloud.google.com/agent-builder/agent-engine/memory-bank/quickstart-api",
}


def reasoning_engines_url(project_id: str, region: str) -> str:
    return f"https://{region}-aiplatform.googleapis.com/v1beta1/projects/{project_id}/locations/{region}/reasoningEngines?pageSize=20"


def memories_url(region: str, engine_name: str) -> str:
    return f"https://{region}-aiplatform.googleapis.com/v1beta1/{engine_name}/memories?pageSize=20"


def write_outputs(payload: dict[str, Any]) -> None:
    write_json(OUTPUT_JSON, payload)
    lines = [
        "# V34 Memory Bank Proof",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Proof state: `{payload['proof_state']}`",
        f"- Memory bank state: `{payload.get('memory_bank_state', 'unknown')}`",
        f"- Agent Engine state: `{payload.get('agent_engine_state', 'unknown')}`",
        f"- Selected region: `{payload.get('selected_region', '') or 'unresolved'}`",
        f"- Selected Agent Engine: `{payload.get('selected_agent_engine', '') or 'unresolved'}`",
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the bounded V34 Memory Bank proof.")
    parser.add_argument("--bundle", default=str(Path.home() / "GCP service account keys.txt"))
    parser.add_argument("--project-id", default=PROJECT_ID)
    args = parser.parse_args()

    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "overall_status": "WARN",
        "proof_state": "pending",
        "memory_bank_state": "pending",
        "agent_engine_state": "pending",
        "project_id": args.project_id,
        "official_sources": OFFICIAL_URLS,
        "preferred_regions": MEMORY_BANK_REGIONS,
        "completed_steps": [],
        "blockers": [],
        "region_attempts": [],
    }

    try:
        _bundle, primary, minted = load_primary_service_account(Path(args.bundle))
    except Exception as exc:
        payload["proof_state"] = "missing_primary_service_account"
        payload["memory_bank_state"] = "blocked_missing_identity"
        payload["agent_engine_state"] = "blocked_missing_identity"
        payload["blockers"].append(str(exc))
        write_outputs(payload)
        return 1

    token = minted["token"]
    payload["primary_identity"] = mask_email(primary["client_email"])
    payload["completed_steps"].append("mint_primary_token")

    service = ensure_service_enabled(args.project_id, token, VERTEX_SERVICE_NAME)
    payload["service_enablement"] = service
    if service["final_status"] != 200 or service["final_state"] != "ENABLED":
        payload["proof_state"] = "service_enablement_blocked"
        payload["memory_bank_state"] = "blocked_service_enablement"
        payload["agent_engine_state"] = "blocked_service_enablement"
        payload["blockers"].append("Vertex AI service usage did not report `ENABLED` after the bounded enablement pass.")
        write_outputs(payload)
        return 1
    payload["completed_steps"].append("vertex_service_enabled")

    sync_result = run_cmd([sys.executable, "scripts/trinity_memory_bank_sync.py", "--label", "v34-memory-bank"], timeout=900)
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

    engine_names: list[str] = []
    selected_region = ""
    for region in MEMORY_BANK_REGIONS:
        engine_response = google_request("GET", reasoning_engines_url(args.project_id, region), token, timeout=120)
        attempt = {
            "region": region,
            "list_status": engine_response["status"],
            "engine_names": extract_engine_names(engine_response.get("parsed", {})),
        }
        if engine_response["status"] == 200 and attempt["engine_names"]:
            engine_name = attempt["engine_names"][0]
            memory_response = google_request("GET", memories_url(region, engine_name), token, timeout=120)
            attempt["selected_engine"] = engine_name
            attempt["memories_status"] = memory_response["status"]
            attempt["memory_count"] = len(memory_response.get("parsed", {}).get("memories", [])) if isinstance(memory_response.get("parsed", {}), dict) else 0
            attempt["memory_response_excerpt"] = json.dumps(memory_response.get("parsed", {}), indent=2)[:1200]
            payload["region_attempts"].append(attempt)
            if memory_response["status"] == 200:
                selected_region = region
                engine_names = attempt["engine_names"]
                payload["selected_region"] = region
                payload["selected_agent_engine"] = engine_name
                payload["memory_inventory"] = {
                    "memory_count": attempt["memory_count"],
                    "status": memory_response["status"],
                }
                payload["completed_steps"].append("agent_engine_inventory_read")
                payload["completed_steps"].append("memory_inventory_read")
                payload["memory_bank_state"] = "live_inventory_read_verified"
                payload["agent_engine_state"] = "inventory_visible"
                payload["proof_state"] = "agent_engine_memory_inventory_read_verified"
                payload["overall_status"] = "PASS"
                write_outputs(payload)
                return 0
            payload["blockers"].append(f"Agent Engine inventory was visible in {region}, but memory inventory read returned HTTP {memory_response['status']}.")
            selected_region = region
            engine_names = attempt["engine_names"]
            break
        payload["region_attempts"].append(attempt)
        if engine_response["status"] != 200:
            payload["blockers"].append(f"Reasoning Engine inventory returned HTTP {engine_response['status']} in {region}.")

    payload["selected_region"] = selected_region
    payload["visible_reasoning_engines"] = engine_names
    payload["memory_bank_state"] = "repo_memory_bank_validated"

    if engine_names:
        payload["agent_engine_state"] = "inventory_visible_memory_read_blocked"
        payload["proof_state"] = "memory_bank_read_blocked"
    else:
        payload["agent_engine_state"] = "not_materialized_in_session"
        payload["proof_state"] = "memory_bank_blocked_missing_reasoning_engine"
        payload["blockers"].append(
            "The repo-side Memory Bank proof passed, but no live Agent Engine instance was visible for Memory Bank inventory in-session."
        )

    write_outputs(payload)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
