#!/usr/bin/env python3
"""Collect V39 Agent Engine forensics for the failed V38 runtime."""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from trinity_v36_cloud_common import (
    DEFAULT_MODEL_LOCATION,
    DEFAULT_REGIONAL_LOCATION,
    LOCAL_SITE_PACKAGES,
    PRIMARY_STAGING_BUCKET,
    PROJECT_ID,
    VERTEX_SERVICE_NAME,
    ensure_service_enabled,
    ensure_staging_bucket,
    load_compute_service_account,
    now_iso,
    primary_identity_fields,
    reasoning_engine_url,
)
from trinity_v32_runtime_common import google_request, write_json, write_text

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v39-agent-engine-forensics-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v39-agent-engine-forensics-v1.md"
V38_PROOF = ROOT / "docs" / "trinity-live-traces" / "v38-agent-engine-proof-v1.json"
PACKAGE_NAMES = ("google-cloud-aiplatform", "pydantic", "cloudpickle")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def package_versions() -> dict[str, Any]:
    global_versions: dict[str, str] = {}
    for name in PACKAGE_NAMES:
        try:
            global_versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            global_versions[name] = "missing"

    local_versions: dict[str, str] = {}
    inline = """
import importlib.metadata as md
import sys
from pathlib import Path
site = Path(sys.argv[1])
if str(site) not in sys.path:
    sys.path.insert(0, str(site))
for name in sys.argv[2:]:
    try:
        print(f"{name}={md.version(name)}")
    except Exception:
        print(f"{name}=missing")
"""
    proc = subprocess.run(
        [sys.executable, "-c", inline, str(LOCAL_SITE_PACKAGES), *PACKAGE_NAMES],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    for line in (proc.stdout or "").splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        local_versions[key.strip()] = value.strip()
    return {
        "global_python": global_versions,
        "local_runtime": local_versions,
        "local_runtime_path": str(LOCAL_SITE_PACKAGES),
        "alignment_ready": all(local_versions.get(name, "missing") != "missing" for name in PACKAGE_NAMES),
    }


def operation_and_resource_state(token: str, regional_location: str, resource_ref: str, operation_ref: str) -> dict[str, Any]:
    return {
        "resource_get": google_request("GET", reasoning_engine_url(regional_location, resource_ref), token, timeout=120),
        "operation_get": google_request("GET", reasoning_engine_url(regional_location, operation_ref), token, timeout=120),
    }


def logging_evidence(token: str, project_id: str, resource_ref: str, operation_ref: str) -> dict[str, Any]:
    filter_text = (
        f'SEARCH("{resource_ref}") OR SEARCH("{operation_ref}") '
        'OR (protoPayload.methodName="google.cloud.aiplatform.v1.ReasoningEngineService.CreateReasoningEngine")'
    )
    body = {
        "resourceNames": [f"projects/{project_id}"],
        "filter": filter_text,
        "orderBy": "timestamp desc",
        "pageSize": 20,
    }
    response = google_request("POST", "https://logging.googleapis.com/v2/entries:list", token, body=body, timeout=120)
    parsed = response.get("parsed", {})
    entries = parsed.get("entries", []) if isinstance(parsed, dict) else []
    simplified = []
    for entry in entries[:10]:
        proto = entry.get("protoPayload", {})
        simplified.append(
            {
                "timestamp": entry.get("timestamp"),
                "severity": entry.get("severity"),
                "log_name": entry.get("logName"),
                "operation": entry.get("operation", {}),
                "resource": entry.get("resource", {}),
                "method_name": proto.get("methodName"),
                "resource_name": proto.get("resourceName"),
                "principal_email": proto.get("authenticationInfo", {}).get("principalEmail"),
                "status": proto.get("status", {}),
                "text_payload": entry.get("textPayload", ""),
                "json_payload": entry.get("jsonPayload", {}),
            }
        )
    return {
        "filter": filter_text,
        "response_status": response["status"],
        "entry_count": len(entries),
        "entries": simplified,
    }


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V39 Agent Engine Forensics",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Recovery state: `{payload['agent_engine_recovery_state']}`",
        f"- Log state: `{payload['agent_engine_log_state']}`",
        f"- Resource ref: `{payload.get('resource_ref', '') or 'missing'}`",
        f"- Operation ref: `{payload.get('operation_ref', '') or 'missing'}`",
        "",
        "## Completed Steps",
        "",
    ]
    lines.extend(f"- `{row}`" for row in payload.get("completed_steps", []))
    lines.extend(["", "## Package Versions", ""])
    lines.append(f"- `global_python`: `{payload.get('package_versions', {}).get('global_python', {})}`")
    lines.append(f"- `local_runtime`: `{payload.get('package_versions', {}).get('local_runtime', {})}`")
    if payload.get("blockers"):
        lines.extend(["", "## Blockers", ""])
        lines.extend(f"- {row}" for row in payload["blockers"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect V39 Agent Engine forensics.")
    parser.add_argument("--bundle", default=str(Path.home() / "GCP service account keys.txt"))
    parser.add_argument("--project-id", default=PROJECT_ID)
    parser.add_argument("--regional-location", default=DEFAULT_REGIONAL_LOCATION)
    parser.add_argument("--model-location", default=DEFAULT_MODEL_LOCATION)
    parser.add_argument("--resource-ref", default="")
    parser.add_argument("--operation-ref", default="")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()

    previous = read_json(V38_PROOF)
    refs = [str(row) for row in previous.get("live_agent_engine_refs", []) if isinstance(row, str)]
    resource_ref = args.resource_ref or next((row for row in refs if "/operations/" not in row), "")
    operation_ref = args.operation_ref or next((row for row in refs if "/operations/" in row), "")

    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": "v39_omega",
        "overall_status": "WARN",
        "agent_engine_recovery_state": "forensics_pending",
        "agent_engine_log_state": "pending",
        "project_id": args.project_id,
        "regional_location": args.regional_location,
        "model_location": args.model_location,
        "resource_ref": resource_ref,
        "operation_ref": operation_ref,
        "staging_bucket": PRIMARY_STAGING_BUCKET,
        "completed_steps": [],
        "blockers": [],
        "package_versions": package_versions(),
        "identity_path": {
            "deploy_identity_mode": "compute_default_submitter_with_default_reasoning_engine_service_agent",
            "custom_service_account_requested": False,
            "iam_service_accounts_act_as_required": False,
        },
    }

    if not resource_ref or not operation_ref:
        payload["overall_status"] = "FAIL"
        payload["agent_engine_recovery_state"] = "missing_v38_references"
        payload["agent_engine_log_state"] = "blocked_missing_refs"
        payload["blockers"].append("The V38 Agent Engine proof did not expose both the reasoning engine resource and operation IDs.")
        write_json(Path(args.output_json), payload)
        write_text(Path(args.output_md), markdown(payload))
        return 1

    try:
        _records, primary, minted = load_compute_service_account(Path(args.bundle))
    except Exception as exc:
        payload["overall_status"] = "FAIL"
        payload["agent_engine_recovery_state"] = "blocked_missing_identity"
        payload["agent_engine_log_state"] = "blocked_missing_identity"
        payload["blockers"].append(str(exc))
        write_json(Path(args.output_json), payload)
        write_text(Path(args.output_md), markdown(payload))
        return 1

    token = minted["token"]
    payload.update(primary_identity_fields(primary, minted))
    payload["service_account_email"] = str(primary["client_email"])
    payload["service_account_path"] = str(primary["runtime_path"])
    payload["completed_steps"].append("mint_compute_default_token")

    payload["service_enablement"] = ensure_service_enabled(args.project_id, token, VERTEX_SERVICE_NAME)
    payload["completed_steps"].append("vertex_service_checked")
    payload["staging_bucket_state"] = ensure_staging_bucket(args.project_id, token, PRIMARY_STAGING_BUCKET)
    payload["completed_steps"].append("staging_bucket_checked")
    payload["operation_state"] = operation_and_resource_state(token, args.regional_location, resource_ref, operation_ref)
    payload["completed_steps"].append("operation_and_resource_fetched")
    payload["logging_evidence"] = logging_evidence(token, args.project_id, resource_ref, operation_ref)
    payload["completed_steps"].append("cloud_logging_evidence_collected")
    payload["fresh_deploy_path_assertion"] = {
        "v39_strategy": "fresh_minimal_subprocess_with_unique_staging_prefix",
        "reused_setup_side_effects_allowed": False,
    }

    operation_error = (
        payload["operation_state"]["operation_get"].get("parsed", {}).get("error", {}).get("message")
        if isinstance(payload["operation_state"]["operation_get"].get("parsed", {}), dict)
        else ""
    )
    resource_status = payload["operation_state"]["resource_get"].get("status")
    alignment_ready = bool(payload["package_versions"].get("alignment_ready"))
    if resource_status == 404 and operation_error:
        payload["agent_engine_recovery_state"] = "forensics_complete_blocker_published"
        payload["agent_engine_log_state"] = "audit_log_verified"
        payload["blockers"].append(str(operation_error))
        if not alignment_ready:
            payload["blockers"].append("One or more required runtime packages are missing from the local runtime site-packages lane.")
    else:
        payload["overall_status"] = "FAIL"
        payload["agent_engine_recovery_state"] = "forensics_incomplete"
        payload["agent_engine_log_state"] = "logging_incomplete"
        payload["blockers"].append("The V39 forensics lane could not verify the expected V38 operation error and log evidence.")

    payload["forensics_summary"] = {
        "resource_status": resource_status,
        "operation_status": payload["operation_state"]["operation_get"].get("status"),
        "operation_error_message": str(operation_error or ""),
        "logging_entry_count": int(payload["logging_evidence"].get("entry_count", 0)),
        "package_alignment_ready": alignment_ready,
    }

    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    return 0 if payload["overall_status"] == "WARN" else 1


if __name__ == "__main__":
    raise SystemExit(main())
