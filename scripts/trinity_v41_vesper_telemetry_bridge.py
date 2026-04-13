#!/usr/bin/env python3
"""Write bounded V41 telemetry into Vesper Ion's proven Bigtable bridge."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from trinity_v36_cloud_common import ensure_service_enabled, load_primary_service_account, primary_identity_fields
from trinity_v37_slot38_memory_bridge import ensure_v37_bigtable_imports
from trinity_v41_common import now_iso, read_json, write_json, write_text

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v41-vesper-telemetry-bridge-proof-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v41-vesper-telemetry-bridge-proof-v1.md"
DEFAULT_INSTANCE_ID = "beyonder-v37-slot38-dev"
DEFAULT_TABLE_ID = "v41_omega_runtime"
DEFAULT_COLUMN_FAMILY = "cf1"
SERVICE_NAMES = ("bigtableadmin.googleapis.com", "bigtable.googleapis.com")
TELEMETRY_SOURCES = (
    "docs/trinity-live-traces/v41-api-ascendancy-proof-v1.json",
    "docs/trinity-live-traces/v41-kai-health-monitor-proof-v1.json",
    "docs/trinity-live-traces/v38-fleet-anthos-proof-v1.json",
    "docs/trinity-live-traces/v38-os-login-proof-v1.json",
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
        "kai_health_monitor_state",
        "anthos_state",
        "os_login_state",
        "agent_engine_advanced_state",
    ):
        if key in payload:
            summary[key] = payload[key]
    return summary


def _markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V41 Vesper Telemetry Bridge",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Vesper telemetry state: `{payload['vesper_telemetry_ingest_state']}`",
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
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Write bounded V41 telemetry into Vesper's proven Bigtable bridge.")
    parser.add_argument("--bundle", default=str(Path.home() / "GCP service account keys.txt"))
    parser.add_argument("--project-id", default="gen-lang-client-0020882673")
    parser.add_argument("--instance-id", default=DEFAULT_INSTANCE_ID)
    parser.add_argument("--table-id", default=DEFAULT_TABLE_ID)
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()

    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": "v41_omega",
        "overall_status": "WARN",
        "vesper_telemetry_ingest_state": "pending",
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
        payload["blockers"].append("Bigtable services are not fully enabled for the V41 Vesper telemetry bridge.")
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
            f"The proven Vesper Bigtable instance `{args.instance_id}` does not exist and V41 will not create a replacement instance."
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
    payload["completed_steps"].append("v41_runtime_table_ready")

    row_key = f"v41::telemetry::{now_iso()}".encode("utf-8")
    payload["row_key"] = row_key.decode("utf-8")
    row = table.direct_row(row_key)
    row.set_cell(DEFAULT_COLUMN_FAMILY, b"summary", json.dumps(payload["telemetry"], sort_keys=True))
    row.set_cell(DEFAULT_COLUMN_FAMILY, b"phase", b"v41_omega")
    row.set_cell(DEFAULT_COLUMN_FAMILY, b"source_prefix", b"v41::telemetry")
    row.commit()
    payload["completed_steps"].append("telemetry_row_written")

    readback = table.read_row(row_key)
    if readback is None:
        payload["overall_status"] = "FAIL"
        payload["vesper_telemetry_ingest_state"] = "blocked_readback_missing"
        payload["blockers"].append("The V41 telemetry row was written but could not be read back from the Vesper Bigtable bridge.")
        write_json(Path(args.output_json), payload)
        write_text(Path(args.output_md), _markdown(payload))
        return 1

    family_cells = getattr(readback, "cells", {}).get(DEFAULT_COLUMN_FAMILY, {})
    summary_cells = family_cells.get(b"summary", [])
    summary_value = summary_cells[0].value.decode("utf-8", errors="replace") if summary_cells else ""
    payload["readback_verified"] = bool(summary_value)
    payload["readback_summary_excerpt"] = summary_value[:2000]
    payload["completed_steps"].append("telemetry_row_readback_verified")
    payload["overall_status"] = "PASS"
    payload["vesper_telemetry_ingest_state"] = "bigtable_v41_prefix_verified"

    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), _markdown(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
