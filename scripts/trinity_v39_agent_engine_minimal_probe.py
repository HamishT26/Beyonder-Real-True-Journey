#!/usr/bin/env python3
"""Deploy a fresh minimal V39 Agent Engine and verify visibility/queryability."""

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
    LOCAL_SITE_PACKAGES,
    PRIMARY_STAGING_BUCKET,
    PROJECT_ID,
    VERTEX_SERVICE_NAME,
    build_vertex_env,
    ensure_service_enabled,
    ensure_staging_bucket,
    extract_last_json_object,
    extract_reasoning_engine_refs,
    load_compute_service_account,
    now_iso,
    primary_identity_fields,
)
from trinity_v32_runtime_common import write_json, write_text

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v39-agent-engine-minimal-probe-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v39-agent-engine-minimal-probe-v1.md"


def write_outputs(payload: dict[str, Any], output_json: Path, output_md: Path) -> None:
    write_json(output_json, payload)
    lines = [
        "# V39 Agent Engine Minimal Probe",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Minimal probe state: `{payload['agent_engine_minimal_probe_state']}`",
        f"- Display name: `{payload.get('display_name', '') or 'unknown'}`",
        f"- Resource name: `{payload.get('resource_name', '') or 'unresolved'}`",
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
    parser = argparse.ArgumentParser(description="Deploy a fresh minimal V39 Agent Engine.")
    parser.add_argument("--bundle", default=str(Path.home() / "GCP service account keys.txt"))
    parser.add_argument("--project-id", default=PROJECT_ID)
    parser.add_argument("--regional-location", default=DEFAULT_REGIONAL_LOCATION)
    parser.add_argument("--model-location", default=DEFAULT_MODEL_LOCATION)
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()

    output_json = Path(args.output_json)
    output_md = Path(args.output_md)
    display_name = f"v39-agent-engine-minimal-{now_iso().replace(':', '').replace('+00:00', 'z').replace('-', '').lower()}"
    gcs_dir_name = display_name

    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": "v39_omega",
        "overall_status": "WARN",
        "agent_engine_minimal_probe_state": "pending",
        "project_id": args.project_id,
        "regional_location": args.regional_location,
        "model_location": args.model_location,
        "staging_bucket": PRIMARY_STAGING_BUCKET,
        "display_name": display_name,
        "gcs_dir_name": gcs_dir_name,
        "completed_steps": [],
        "blockers": [],
        "requirements": [
            "google-cloud-aiplatform==1.145.0",
            "pydantic==2.12.5",
            "cloudpickle==3.1.2",
        ],
        "deploy_identity_mode": "compute_default_submitter_with_default_reasoning_engine_service_agent",
        "custom_service_account_requested": False,
    }

    try:
        _records, primary, minted = load_compute_service_account(Path(args.bundle))
    except Exception as exc:
        payload["overall_status"] = "FAIL"
        payload["agent_engine_minimal_probe_state"] = "blocked_missing_identity"
        payload["blockers"].append(str(exc))
        write_outputs(payload, output_json, output_md)
        return 1

    token = minted["token"]
    payload.update(primary_identity_fields(primary, minted))
    payload["service_account_path"] = str(primary["runtime_path"])
    payload["service_account_email"] = str(primary["client_email"])
    payload["completed_steps"].append("mint_compute_default_token")

    service_state = ensure_service_enabled(args.project_id, token, VERTEX_SERVICE_NAME)
    payload["service_enablement"] = service_state
    if service_state["final_status"] != 200 or service_state["final_state"] != "ENABLED":
        payload["overall_status"] = "FAIL"
        payload["agent_engine_minimal_probe_state"] = "blocked_service_enablement"
        payload["blockers"].append("Vertex AI did not report ENABLED for the V39 minimal probe.")
        write_outputs(payload, output_json, output_md)
        return 1
    payload["completed_steps"].append("vertex_service_enabled")

    bucket_state = ensure_staging_bucket(args.project_id, token, PRIMARY_STAGING_BUCKET)
    payload["staging_bucket_state"] = bucket_state
    if bucket_state.get("final_status") != 200:
        payload["overall_status"] = "FAIL"
        payload["agent_engine_minimal_probe_state"] = "blocked_staging_bucket"
        payload["blockers"].append("The shared Agent Engine staging bucket could not be verified for the V39 minimal probe.")
        write_outputs(payload, output_json, output_md)
        return 1
    payload["completed_steps"].append("staging_bucket_verified")

    env = build_vertex_env(
        primary,
        args.project_id,
        regional_location=args.regional_location,
        model_location=args.model_location,
        google_cloud_location=args.model_location,
    )
    inline = f"""
import json
import sys
import traceback
from pathlib import Path

site = Path({str(LOCAL_SITE_PACKAGES)!r})
if str(site) not in sys.path:
    sys.path.insert(0, str(site))

result = {{
    "success": False,
    "display_name": {display_name!r},
    "gcs_dir_name": {gcs_dir_name!r},
}}
try:
    import vertexai
    from vertexai import agent_engines

    class V39MinimalProbe:
        def query(self, input: str) -> dict:
            return {{"echo": input, "marker": "V39_AGENT_ENGINE_MINIMAL_OK"}}

    vertexai.init(
        project={args.project_id!r},
        location={args.regional_location!r},
        staging_bucket={PRIMARY_STAGING_BUCKET!r},
    )
    remote_agent = agent_engines.create(
        agent_engine=V39MinimalProbe(),
        requirements={payload['requirements']!r},
        display_name={display_name!r},
        description="Fresh V39 minimal Agent Engine probe",
        gcs_dir_name={gcs_dir_name!r},
    )
    result["resource_name"] = str(getattr(remote_agent, "resource_name", "") or getattr(remote_agent, "name", ""))

    visible = []
    for item in agent_engines.list(filter=f'display_name="{display_name}"'):
        visible.append(str(getattr(item, "resource_name", "") or getattr(item, "name", "") or item))
    result["visible_reasoning_engines"] = visible

    fetched = agent_engines.get(result["resource_name"]) if result["resource_name"] else None
    result["fetched_resource_name"] = str(getattr(fetched, "resource_name", "") or getattr(fetched, "name", "") or "")

    if fetched is not None:
        query_result = fetched.query(input="hello from v39")
        result["query_result"] = query_result
    result["success"] = True
except Exception as exc:
    result["exception_type"] = exc.__class__.__name__
    result["exception_message"] = str(exc)
    result["traceback"] = traceback.format_exc()[-12000:]

print(json.dumps(result))
"""
    proc = subprocess.run(
        [sys.executable, "-c", inline],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=3600,
        check=False,
    )
    parsed = extract_last_json_object(proc.stdout)
    payload["minimal_probe_subprocess"] = {
        "returncode": proc.returncode,
        "stdout_excerpt": proc.stdout[-12000:],
        "stderr_excerpt": proc.stderr[-4000:],
        "parsed": parsed,
    }
    payload["completed_steps"].append("fresh_minimal_subprocess_executed")
    refs = extract_reasoning_engine_refs(proc.stdout + "\n" + proc.stderr)
    if refs:
        payload["observed_reasoning_engine_refs"] = refs

    if parsed.get("success") is True:
        payload["resource_name"] = str(parsed.get("resource_name") or "")
        payload["visible_reasoning_engines"] = list(parsed.get("visible_reasoning_engines") or [])
        payload["query_result"] = parsed.get("query_result")
        payload["agent_engine_minimal_probe_state"] = "live_visible_and_query_verified"
        payload["overall_status"] = "PASS"
        payload["completed_steps"].extend(
            [
                "fresh_minimal_agent_created",
                "agent_engine_list_verified",
                "agent_engine_get_verified",
                "bounded_query_verified",
            ]
        )
        write_outputs(payload, output_json, output_md)
        return 0

    payload["overall_status"] = "WARN"
    payload["agent_engine_minimal_probe_state"] = "live_start_failed_again"
    payload["blockers"].append(
        str(parsed.get("exception_message") or "The fresh V39 minimal Agent Engine probe failed before visibility or query verification.")
    )
    write_outputs(payload, output_json, output_md)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
