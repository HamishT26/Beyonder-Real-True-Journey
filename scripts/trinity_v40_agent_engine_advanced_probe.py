#!/usr/bin/env python3
"""Verify bounded live Agent Engine session and memory interactions for V40."""

from __future__ import annotations

import argparse
import os
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
    load_compute_service_account,
    primary_identity_fields,
)
from trinity_v40_common import ROOT, now_iso, read_json, to_jsonable, write_json, write_text

OUTPUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v40-agent-engine-advanced-probe-v1.json"
OUTPUT_MD = ROOT / "docs" / "trinity-live-traces" / "v40-agent-engine-advanced-probe-v1.md"
MINIMAL_PROOF = ROOT / "docs" / "trinity-live-traces" / "v39-agent-engine-minimal-probe-v1.json"
OFFICIAL_SOURCES = {
    "agent_engine_deploy_troubleshooting": "https://docs.cloud.google.com/agent-builder/agent-engine/troubleshooting/deploy",
    "memory_bank_overview": "https://docs.cloud.google.com/agent-builder/agent-engine/memory-bank/overview",
}


def _summarize_engine_dump(raw: dict[str, Any]) -> dict[str, Any]:
    api_resource = raw.get("api_resource", {}) if isinstance(raw.get("api_resource"), dict) else {}
    spec = api_resource.get("spec", {}) if isinstance(api_resource.get("spec"), dict) else {}
    package_spec = spec.get("package_spec", {}) if isinstance(spec.get("package_spec"), dict) else {}
    return {
        "api_resource": {
            "name": api_resource.get("name"),
            "display_name": api_resource.get("display_name"),
            "description": api_resource.get("description"),
            "create_time": api_resource.get("create_time"),
            "update_time": api_resource.get("update_time"),
            "spec": {
                "agent_framework": spec.get("agent_framework"),
                "effective_identity": spec.get("effective_identity"),
                "service_account": spec.get("service_account"),
                "package_spec": {
                    "python_version": package_spec.get("python_version"),
                    "pickle_object_gcs_uri": package_spec.get("pickle_object_gcs_uri"),
                    "requirements_gcs_uri": package_spec.get("requirements_gcs_uri"),
                    "dependency_files_gcs_uri": package_spec.get("dependency_files_gcs_uri"),
                },
            },
        }
    }


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V40 Agent Engine Advanced Probe",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Agent Engine advanced state: `{payload['agent_engine_advanced_state']}`",
        f"- Resource name: `{payload.get('resource_name', '') or 'unknown'}`",
        f"- Session name: `{payload.get('session_name', '') or 'not_created'}`",
        f"- Memory name: `{payload.get('memory_name', '') or 'not_created'}`",
        "",
        "## Completed Steps",
        "",
    ]
    lines.extend(f"- `{row}`" for row in payload.get("completed_steps", []))
    if payload.get("blockers"):
        lines.extend(["", "## Blockers", ""])
        lines.extend(f"- {row}" for row in payload["blockers"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify bounded live Agent Engine interactions for V40.")
    parser.add_argument("--bundle", default=str(Path.home() / "GCP service account keys.txt"))
    parser.add_argument("--project-id", default=PROJECT_ID)
    parser.add_argument("--regional-location", default=DEFAULT_REGIONAL_LOCATION)
    parser.add_argument("--model-location", default=DEFAULT_MODEL_LOCATION)
    parser.add_argument("--output-json", default=str(OUTPUT_JSON))
    parser.add_argument("--output-md", default=str(OUTPUT_MD))
    args = parser.parse_args()

    baseline = read_json(MINIMAL_PROOF)
    resource_name = str(baseline.get("resource_name") or "")
    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": "v40_omega",
        "overall_status": "WARN",
        "agent_engine_advanced_state": "pending",
        "resource_name": resource_name,
        "project_id": args.project_id,
        "regional_location": args.regional_location,
        "model_location": args.model_location,
        "staging_bucket": PRIMARY_STAGING_BUCKET,
        "completed_steps": [],
        "blockers": [],
        "official_sources": OFFICIAL_SOURCES,
        "baseline_minimal_probe_path": str(MINIMAL_PROOF.relative_to(ROOT)).replace("\\", "/"),
    }

    if not resource_name:
        payload["overall_status"] = "FAIL"
        payload["agent_engine_advanced_state"] = "blocked_missing_minimal_resource"
        payload["blockers"].append("The V39 minimal Agent Engine proof does not expose a resource name for V40 advanced probing.")
        write_json(Path(args.output_json), payload)
        write_text(Path(args.output_md), markdown(payload))
        return 1

    try:
        _records, primary, minted = load_compute_service_account(Path(args.bundle))
    except Exception as exc:
        payload["overall_status"] = "FAIL"
        payload["agent_engine_advanced_state"] = "blocked_missing_identity"
        payload["blockers"].append(str(exc))
        write_json(Path(args.output_json), payload)
        write_text(Path(args.output_md), markdown(payload))
        return 1

    payload.update(primary_identity_fields(primary, minted))
    payload["service_account_path"] = str(primary["runtime_path"])
    payload["service_account_email"] = str(primary["client_email"])
    payload["completed_steps"].append("mint_compute_default_token")

    token = minted["token"]
    service_state = ensure_service_enabled(args.project_id, token, VERTEX_SERVICE_NAME)
    payload["service_enablement"] = service_state
    if service_state["final_status"] != 200 or service_state["final_state"] != "ENABLED":
        payload["overall_status"] = "FAIL"
        payload["agent_engine_advanced_state"] = "blocked_service_enablement"
        payload["blockers"].append("Vertex AI is not enabled for the V40 Agent Engine advanced probe.")
        write_json(Path(args.output_json), payload)
        write_text(Path(args.output_md), markdown(payload))
        return 1
    payload["completed_steps"].append("vertex_service_enabled")

    payload["staging_bucket_state"] = ensure_staging_bucket(args.project_id, token, PRIMARY_STAGING_BUCKET)
    payload["completed_steps"].append("staging_bucket_verified")

    env = build_vertex_env(
        primary,
        args.project_id,
        regional_location=args.regional_location,
        model_location=args.model_location,
        google_cloud_location=args.model_location,
    )
    if str(LOCAL_SITE_PACKAGES) not in sys.path:
        sys.path.insert(0, str(LOCAL_SITE_PACKAGES))
    os.environ.update(env)

    try:
        import vertexai

        client = vertexai.Client(project=args.project_id, location=args.regional_location)
        engine = client.agent_engines.get(name=resource_name)
        payload["engine_get"] = _summarize_engine_dump(to_jsonable(engine.model_dump()))
        payload["completed_steps"].append("agent_engine_get_verified")

        query_result = engine.query(input="hello from v40 advanced")
        payload["query_result"] = to_jsonable(query_result)
        payload["completed_steps"].append("bounded_query_verified")

        user_id = "v40-agent-engine-user"
        session_op = client.agent_engines.sessions.create(name=resource_name, user_id=user_id)
        payload["session_operation"] = to_jsonable(session_op.model_dump())
        session = session_op.response
        session_name = str(getattr(session, "name", "") or "")
        payload["session_name"] = session_name
        payload["completed_steps"].append("session_create_verified")

        listed_sessions = [to_jsonable(row.model_dump()) for row in client.agent_engines.sessions.list(name=resource_name)]
        payload["listed_sessions"] = listed_sessions
        if not any(str(row.get("name") or "") == session_name for row in listed_sessions):
            raise RuntimeError("The V40 session was created but did not appear in the bounded session listing.")
        payload["completed_steps"].append("session_list_verified")

        memory_op = client.agent_engines.memories.create(
            name=resource_name,
            fact="V40_AGENT_ENGINE_MEMORY_OK",
            scope={"user_id": user_id},
            config={"display_name": "v40-agent-engine-memory", "description": "bounded V40 proof memory"},
        )
        payload["memory_operation"] = to_jsonable(memory_op.model_dump())
        memory = memory_op.response
        memory_name = str(getattr(memory, "name", "") or "")
        payload["memory_name"] = memory_name
        payload["completed_steps"].append("memory_create_verified")

        listed_memories = [to_jsonable(row.model_dump()) for row in client.agent_engines.memories.list(name=resource_name)]
        payload["listed_memories"] = listed_memories
        if not any(str(row.get("name") or "") == memory_name for row in listed_memories):
            raise RuntimeError("The V40 memory was created but did not appear in the bounded memory listing.")
        payload["completed_steps"].append("memory_list_verified")

        retrieved = [to_jsonable(row.model_dump()) for row in client.agent_engines.memories.retrieve(name=resource_name, scope={"user_id": user_id})]
        payload["retrieved_memories"] = retrieved
        if not retrieved:
            raise RuntimeError("The V40 memory retrieval lane returned no memories for the bounded proof scope.")
        payload["completed_steps"].append("memory_retrieve_verified")

        payload["memory_get"] = to_jsonable(client.agent_engines.memories.get(name=memory_name).model_dump())
        payload["completed_steps"].append("memory_get_verified")

        cleanup: dict[str, Any] = {"deleted_memory": False, "deleted_session": False}
        try:
            client.agent_engines.memories.delete(name=memory_name)
            cleanup["deleted_memory"] = True
            payload["completed_steps"].append("memory_cleanup_verified")
        except Exception as exc:
            cleanup["memory_cleanup_error"] = str(exc)
        try:
            client.agent_engines.sessions.delete(name=session_name)
            cleanup["deleted_session"] = True
            payload["completed_steps"].append("session_cleanup_verified")
        except Exception as exc:
            cleanup["session_cleanup_error"] = str(exc)
        payload["cleanup"] = cleanup

        if cleanup.get("deleted_memory") is True and cleanup.get("deleted_session") is True:
            payload["overall_status"] = "PASS"
            payload["agent_engine_advanced_state"] = "live_session_and_memory_verified"
        else:
            payload["overall_status"] = "WARN"
            payload["agent_engine_advanced_state"] = "live_session_and_memory_verified_cleanup_warn"
            if cleanup.get("memory_cleanup_error"):
                payload["blockers"].append(f"memory_cleanup_error={cleanup['memory_cleanup_error']}")
            if cleanup.get("session_cleanup_error"):
                payload["blockers"].append(f"session_cleanup_error={cleanup['session_cleanup_error']}")
    except Exception as exc:
        payload["overall_status"] = "WARN"
        payload["agent_engine_advanced_state"] = "live_advanced_interaction_blocked"
        payload["blockers"].append(str(exc))

    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    return 0 if payload["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
