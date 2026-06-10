#!/usr/bin/env python3
"""Ingest bounded V38 telemetry into Vesper Ion's proven Bigtable bridge."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from trinity_v36_cloud_common import ensure_service_enabled, load_primary_service_account, now_iso, primary_identity_fields, write_json, write_text
from trinity_v37_slot38_memory_bridge import ensure_v37_bigtable_imports

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v38-vesper-bigtable-ingest-proof-v1.json"
OUTPUT_MD = ROOT / "docs" / "trinity-live-traces" / "v38-vesper-bigtable-ingest-proof-v1.md"
DEFAULT_INSTANCE_ID = "beyonder-v37-slot38-dev"
DEFAULT_TABLE_ID = "v38_omega_ingest"
DEFAULT_COLUMN_FAMILY = "cf1"
SERVICE_NAMES = ["bigtableadmin.googleapis.com", "bigtable.googleapis.com"]
TELEMETRY_SOURCES = [
    "docs/trinity-live-traces/v38-windows-operator-proof-v1.json",
    "docs/trinity-live-traces/v38-environment-proof-v1.json",
    "docs/trinity-live-traces/v38-enterprise-api-sweep-v1.json",
    "docs/trinity-live-traces/v38-fleet-anthos-proof-v1.json",
    "docs/trinity-live-traces/v38-os-login-proof-v1.json",
]


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def build_telemetry() -> dict[str, Any]:
    telemetry: dict[str, Any] = {"generated_utc": now_iso(), "sources": []}
    for rel in TELEMETRY_SOURCES:
        path = ROOT / rel
        payload = read_json(path)
        summary = {
            "path": rel,
            "present": path.exists(),
            "overall_status": str(payload.get("overall_status") or ""),
        }
        for key in (
            "windows_operator_lane_state",
            "codex_environment_state",
            "enterprise_api_sweep_state",
            "anthos_state",
            "gke_fleet_state",
            "connect_gateway_state",
            "os_login_state",
        ):
            if key in payload:
                summary[key] = payload[key]
        telemetry["sources"].append(summary)
    return telemetry


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V38 Vesper Bigtable Ingest Proof",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Ingest state: `{payload['vesper_bigtable_ingest_state']}`",
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
    parser = argparse.ArgumentParser(description="Ingest bounded V38 telemetry into the proven Vesper Ion Bigtable bridge.")
    parser.add_argument("--bundle", default=str(Path.home() / "GCP service account keys.txt"))
    parser.add_argument("--project-id", default="gen-lang-client-0020882673")
    parser.add_argument("--instance-id", default=DEFAULT_INSTANCE_ID)
    parser.add_argument("--table-id", default=DEFAULT_TABLE_ID)
    parser.add_argument("--output-json", default=str(OUTPUT_JSON))
    parser.add_argument("--output-md", default=str(OUTPUT_MD))
    args = parser.parse_args()

    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": "v38_omega",
        "overall_status": "WARN",
        "vesper_bigtable_ingest_state": "pending",
        "project_id": args.project_id,
        "instance_id": args.instance_id,
        "table_id": args.table_id,
        "completed_steps": [],
        "blockers": [],
        "telemetry": build_telemetry(),
    }

    try:
        _records, primary, minted = load_primary_service_account(Path(args.bundle))
    except Exception as exc:
        payload["overall_status"] = "FAIL"
        payload["vesper_bigtable_ingest_state"] = "blocked_missing_identity"
        payload["blockers"].append(str(exc))
        write_json(Path(args.output_json), payload)
        write_text(Path(args.output_md), markdown(payload))
        return 1

    token = minted["token"]
    payload.update(primary_identity_fields(primary, minted))
    payload["service_account_path"] = str(primary["runtime_path"])
    payload["completed_steps"].append("mint_primary_token")

    service_results = [ensure_service_enabled(args.project_id, token, service_name) for service_name in SERVICE_NAMES]
    payload["service_enablement"] = service_results
    if not all(result["final_status"] == 200 and result["final_state"] == "ENABLED" for result in service_results):
        payload["overall_status"] = "FAIL"
        payload["vesper_bigtable_ingest_state"] = "blocked_service_enablement"
        payload["blockers"].append("Bigtable services are not fully enabled for the V38 Vesper ingest lane.")
        write_json(Path(args.output_json), payload)
        write_text(Path(args.output_md), markdown(payload))
        return 1
    payload["completed_steps"].append("bigtable_services_enabled")

    try:
        Client, _enums, MaxVersionsGCRule, service_account = ensure_v37_bigtable_imports()
        payload["completed_steps"].append("bigtable_client_ready")
    except Exception as exc:
        payload["overall_status"] = "FAIL"
        payload["vesper_bigtable_ingest_state"] = "blocked_client_unavailable"
        payload["blockers"].append(str(exc))
        write_json(Path(args.output_json), payload)
        write_text(Path(args.output_md), markdown(payload))
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
        payload["vesper_bigtable_ingest_state"] = "blocked_proven_instance_missing"
        payload["blockers"].append(
            f"The proven Vesper Bigtable instance `{args.instance_id}` does not exist and V38 will not create a replacement instance."
        )
        write_json(Path(args.output_json), payload)
        write_text(Path(args.output_md), markdown(payload))
        return 1
    payload["completed_steps"].append("proven_instance_verified")

    table = instance.table(args.table_id)
    if not table.exists():
        table.create(column_families={DEFAULT_COLUMN_FAMILY: MaxVersionsGCRule(1)})
        payload["table_created"] = True
    else:
        payload["table_created"] = False
    payload["completed_steps"].append("v38_ingest_table_ready")

    row_key = f"v38::{now_iso()}".encode("utf-8")
    row_key_text = row_key.decode("utf-8")
    row = table.direct_row(row_key)
    row.set_cell(DEFAULT_COLUMN_FAMILY, b"summary", json.dumps(payload["telemetry"], sort_keys=True))
    row.set_cell(DEFAULT_COLUMN_FAMILY, b"phase", "v38_omega")
    row.commit()
    payload["row_key"] = row_key_text
    payload["completed_steps"].append("telemetry_row_written")

    readback = table.read_row(row_key)
    if readback is None:
        payload["overall_status"] = "FAIL"
        payload["vesper_bigtable_ingest_state"] = "blocked_readback_missing"
        payload["blockers"].append("The telemetry row was written but could not be read back from the Vesper Bigtable bridge.")
        write_json(Path(args.output_json), payload)
        write_text(Path(args.output_md), markdown(payload))
        return 1

    family_cells = getattr(readback, "cells", {}).get(DEFAULT_COLUMN_FAMILY, {})
    summary_cells = family_cells.get(b"summary", [])
    summary_value = summary_cells[0].value.decode("utf-8", errors="replace") if summary_cells else ""
    payload["readback_verified"] = bool(summary_value)
    payload["readback_summary_excerpt"] = summary_value[:2000]
    payload["completed_steps"].append("telemetry_row_readback_verified")
    payload["overall_status"] = "PASS"
    payload["vesper_bigtable_ingest_state"] = "bigtable_ingest_verified"

    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
