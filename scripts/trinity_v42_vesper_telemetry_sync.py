#!/usr/bin/env python3
"""Write bounded V42 telemetry into Vesper Ion's proven Bigtable bridge and mirror to Agent Engine when healthy."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

from trinity_v36_cloud_common import (
    DEFAULT_MODEL_LOCATION,
    DEFAULT_REGIONAL_LOCATION,
    LOCAL_SITE_PACKAGES,
    PROJECT_ID,
    build_vertex_env,
    ensure_service_enabled,
    load_compute_service_account,
    load_primary_service_account,
    primary_identity_fields,
)
from trinity_v37_slot38_memory_bridge import ensure_v37_bigtable_imports
from trinity_v42_common import ROOT, now_iso, read_json, to_jsonable, write_json, write_text

DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v42-vesper-telemetry-sync-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v42-vesper-telemetry-sync-v1.md"
DEFAULT_INSTANCE_ID = "beyonder-v37-slot38-dev"
DEFAULT_TABLE_ID = "v42_omega_runtime"
DEFAULT_COLUMN_FAMILY = "cf1"
SERVICE_NAMES = ("bigtableadmin.googleapis.com", "bigtable.googleapis.com")
TELEMETRY_SOURCES = (
    "docs/trinity-live-traces/v42-api-automation-wave-v1.json",
    "docs/trinity-live-traces/v42-kai-automation-bridge-v1.json",
    "docs/trinity-live-traces/v42-gmut-lab-bundle-v1.json",
    "docs/trinity-live-traces/v42-wsl-codex-probe-v1.json",
    "docs/trinity-live-traces/v42-filesystem-promotion-proof-v1.json",
    "docs/trinity-live-traces/v40-agent-engine-advanced-probe-v1.json",
)


def _summary(rel_path: str) -> dict[str, Any]:
    path = ROOT / rel_path
    payload = read_json(path)
    summary = {
        "path": rel_path,
        "present": path.exists(),
        "overall_status": str(payload.get("overall_status") or ""),
    }
    for key in (
        "api_ascendancy_state",
        "cloud_run_state",
        "cloud_build_state",
        "dataplex_state",
        "gke_telemetry_state",
        "kai_automation_state",
        "gmut_experiment_state",
        "wsl_codex_selector_state",
        "filesystem_promotion_state",
        "agent_engine_advanced_state",
    ):
        if key in payload:
            summary[key] = payload[key]
    return summary


def _agent_engine_memory_mirror(bundle_path: Path, resource_name: str, telemetry: dict[str, Any]) -> dict[str, Any]:
    _records, primary, _minted = load_compute_service_account(bundle_path)
    env = build_vertex_env(
        primary,
        PROJECT_ID,
        regional_location=DEFAULT_REGIONAL_LOCATION,
        model_location=DEFAULT_MODEL_LOCATION,
        google_cloud_location=DEFAULT_MODEL_LOCATION,
    )
    if str(LOCAL_SITE_PACKAGES) not in sys.path:
        sys.path.insert(0, str(LOCAL_SITE_PACKAGES))
    os.environ.update(env)

    import vertexai

    client = vertexai.Client(project=PROJECT_ID, location=DEFAULT_REGIONAL_LOCATION)
    user_id = "v42-vesper-sync-user"
    fact = json.dumps({"marker": "V42_VESPER_SYNC_OK", "source_count": len(telemetry.get("sources", []))}, sort_keys=True)
    memory_op = client.agent_engines.memories.create(
        name=resource_name,
        fact=fact,
        scope={"user_id": user_id},
        config={"display_name": "v42-vesper-sync-memory", "description": "bounded V42 Vesper sync mirror"},
    )
    memory = memory_op.response
    memory_name = str(getattr(memory, "name", "") or "")
    listed = [to_jsonable(row.model_dump()) for row in client.agent_engines.memories.list(name=resource_name)]
    retrieved = [to_jsonable(row.model_dump()) for row in client.agent_engines.memories.retrieve(name=resource_name, scope={"user_id": user_id})]
    got = to_jsonable(client.agent_engines.memories.get(name=memory_name).model_dump()) if memory_name else {}
    cleanup: dict[str, Any] = {"deleted_memory": False}
    if memory_name:
        try:
            client.agent_engines.memories.delete(name=memory_name)
            cleanup["deleted_memory"] = True
        except Exception as exc:  # noqa: BLE001
            cleanup["delete_error"] = str(exc)
    return {
        "state": "verified" if memory_name and retrieved else "bounded_secondary_blocked",
        "memory_name": memory_name,
        "operation": to_jsonable(memory_op.model_dump()),
        "listed_memories": listed,
        "retrieved_memories": retrieved,
        "memory_get": got,
        "cleanup": cleanup,
    }


def _markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V42 Vesper Telemetry Sync",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Vesper telemetry state: `{payload['vesper_telemetry_ingest_state']}`",
        f"- Agent Engine mirror state: `{payload.get('agent_engine_memory_mirror_state', '') or 'skipped'}`",
        f"- Instance: `{payload.get('instance_id', '') or 'unknown'}`",
        f"- Table: `{payload.get('table_id', '') or 'unknown'}`",
        f"- Row key: `{payload.get('row_key', '') or 'unknown'}`",
        "",
        "## Completed Steps",
        "",
    ]
    lines.extend(f"- `{row}`" for row in payload.get("completed_steps", []))
    if payload.get("blockers"):
        lines.extend(["", "## Blockers", ""])
        lines.extend(f"- {row}" for row in payload["blockers"])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Write bounded V42 telemetry into Vesper's proven Bigtable bridge.")
    parser.add_argument("--bundle", default=str(Path.home() / "GCP service account keys.txt"))
    parser.add_argument("--project-id", default=PROJECT_ID)
    parser.add_argument("--instance-id", default=DEFAULT_INSTANCE_ID)
    parser.add_argument("--table-id", default=DEFAULT_TABLE_ID)
    parser.add_argument("--scheduled", action="store_true")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()

    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": "v42_omega",
        "overall_status": "WARN",
        "execution_mode": "scheduled" if args.scheduled else "manual",
        "vesper_telemetry_ingest_state": "pending",
        "agent_engine_memory_mirror_state": "skipped",
        "project_id": args.project_id,
        "instance_id": args.instance_id,
        "table_id": args.table_id,
        "completed_steps": [],
        "blockers": [],
        "telemetry": {
            "generated_utc": now_iso(),
            "sources": [_summary(rel_path) for rel_path in TELEMETRY_SOURCES],
        },
    }

    try:
        _records, primary, minted = load_primary_service_account(Path(args.bundle))
    except Exception as exc:
        payload["overall_status"] = "FAIL"
        payload["vesper_telemetry_ingest_state"] = "blocked_missing_identity"
        payload["blockers"].append(str(exc))
        write_json(Path(args.output_json), payload)
        write_text(Path(args.output_md), _markdown(payload))
        return 1

    token = minted["token"]
    payload.update(primary_identity_fields(primary, minted))
    payload["service_account_path"] = str(primary["runtime_path"])
    payload["completed_steps"].append("mint_primary_token")

    service_results = [ensure_service_enabled(args.project_id, token, service_name) for service_name in SERVICE_NAMES]
    payload["service_enablement"] = service_results
    if not all(result["final_status"] == 200 and result["final_state"] == "ENABLED" for result in service_results):
        payload["overall_status"] = "FAIL"
        payload["vesper_telemetry_ingest_state"] = "blocked_service_enablement"
        payload["blockers"].append("Bigtable services are not fully enabled for the V42 Vesper telemetry bridge.")
        write_json(Path(args.output_json), payload)
        write_text(Path(args.output_md), _markdown(payload))
        return 1
    payload["completed_steps"].append("bigtable_services_enabled")

    try:
        Client, _enums, MaxVersionsGCRule, service_account = ensure_v37_bigtable_imports()
        payload["completed_steps"].append("bigtable_client_ready")
    except Exception as exc:
        payload["overall_status"] = "FAIL"
        payload["vesper_telemetry_ingest_state"] = "blocked_client_unavailable"
        payload["blockers"].append(str(exc))
        write_json(Path(args.output_json), payload)
        write_text(Path(args.output_md), _markdown(payload))
        return 1

    from google.auth.transport.requests import Request  # type: ignore

    credentials = service_account.Credentials.from_service_account_info(
        primary["info"],
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    credentials.refresh(Request())
    client = Client(project=args.project_id, credentials=credentials, admin=True)

    instance = client.instance(args.instance_id)
    if not instance.exists():
        payload["overall_status"] = "FAIL"
        payload["vesper_telemetry_ingest_state"] = "blocked_proven_instance_missing"
        payload["blockers"].append(
            f"The proven Vesper Bigtable instance `{args.instance_id}` does not exist and V42 will not create a replacement instance."
        )
        write_json(Path(args.output_json), payload)
        write_text(Path(args.output_md), _markdown(payload))
        return 1
    payload["completed_steps"].append("proven_instance_verified")

    table = instance.table(args.table_id)
    if not table.exists():
        table.create(column_families={DEFAULT_COLUMN_FAMILY: MaxVersionsGCRule(1)})
        payload["table_created"] = True
    else:
        payload["table_created"] = False
    payload["completed_steps"].append("v42_runtime_table_ready")

    row_key = f"v42::telemetry::{now_iso()}".encode("utf-8")
    payload["row_key"] = row_key.decode("utf-8")
    row = table.direct_row(row_key)
    row.set_cell(DEFAULT_COLUMN_FAMILY, b"summary", json.dumps(payload["telemetry"], sort_keys=True))
    row.set_cell(DEFAULT_COLUMN_FAMILY, b"phase", b"v42_omega")
    row.set_cell(DEFAULT_COLUMN_FAMILY, b"source_prefix", b"v42::telemetry")
    row.commit()
    payload["completed_steps"].append("telemetry_row_written")

    readback = table.read_row(row_key)
    if readback is None:
        payload["overall_status"] = "FAIL"
        payload["vesper_telemetry_ingest_state"] = "blocked_readback_missing"
        payload["blockers"].append("The V42 telemetry row was written but could not be read back from the Vesper Bigtable bridge.")
        write_json(Path(args.output_json), payload)
        write_text(Path(args.output_md), _markdown(payload))
        return 1

    family_cells = getattr(readback, "cells", {}).get(DEFAULT_COLUMN_FAMILY, {})
    summary_cells = family_cells.get(b"summary", [])
    summary_value = summary_cells[0].value.decode("utf-8", errors="replace") if summary_cells else ""
    payload["readback_verified"] = bool(summary_value)
    payload["readback_summary_excerpt"] = summary_value[:2000]
    payload["completed_steps"].append("telemetry_row_readback_verified")
    payload["vesper_telemetry_ingest_state"] = "bigtable_v42_prefix_verified"

    agent_engine = read_json(ROOT / "docs" / "trinity-live-traces" / "v40-agent-engine-advanced-probe-v1.json")
    resource_name = str(agent_engine.get("resource_name") or "")
    if str(agent_engine.get("agent_engine_advanced_state") or "") == "live_session_and_memory_verified" and resource_name:
        try:
            mirror = _agent_engine_memory_mirror(Path(args.bundle), resource_name, payload["telemetry"])
            payload["agent_engine_memory_mirror"] = mirror
            payload["agent_engine_memory_mirror_state"] = str(mirror.get("state") or "bounded_secondary_blocked")
            if payload["agent_engine_memory_mirror_state"] == "verified":
                payload["completed_steps"].append("agent_engine_memory_mirror_verified")
            else:
                payload["blockers"].append("Agent Engine remained a bounded secondary mirror and did not complete the V42 telemetry mirror cleanly.")
        except Exception as exc:  # noqa: BLE001
            payload["agent_engine_memory_mirror_state"] = "bounded_secondary_blocked"
            payload["blockers"].append(f"agent_engine_memory_mirror_error={exc}")

    payload["overall_status"] = "PASS"
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), _markdown(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
