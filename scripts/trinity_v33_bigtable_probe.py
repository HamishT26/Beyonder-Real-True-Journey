#!/usr/bin/env python3
"""Run the bounded V33 Bigtable proof using the official Python client."""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from trinity_v32_runtime_common import (
    DEFAULT_GCP_KEY_BUNDLE,
    LOCAL_RUNTIME,
    PRIMARY_REGION,
    PROJECT_ID,
    google_request,
    load_gcp_service_accounts,
    mask_email,
    now_iso,
    write_json,
    write_text,
)

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v33-bigtable-proof-v1.json"
OUTPUT_MD = ROOT / "docs" / "trinity-live-traces" / "v33-bigtable-proof-v1.md"
SITE_PACKAGES = LOCAL_RUNTIME / "site-packages"
SERVICE_NAMES = ["bigtableadmin.googleapis.com", "bigtable.googleapis.com"]
DEFAULT_INSTANCE_ID = "beyonder-v33-dev"
DEFAULT_CLUSTER_ID = "beyonder-v33-dev-cluster"
DEFAULT_APP_PROFILE_ID = "v33-omega-app"
DEFAULT_TABLE_ID = "v33_omega_smoke"
DEFAULT_COLUMN_FAMILY = "cf1"


def service_url(project_id: str, service_name: str) -> str:
    return f"https://serviceusage.googleapis.com/v1/projects/{project_id}/services/{service_name}"


def ensure_service_enabled(project_id: str, token: str, service_name: str) -> dict[str, Any]:
    initial = google_request("GET", service_url(project_id, service_name), token, timeout=60)
    initial_state = str(initial.get("parsed", {}).get("state", "UNKNOWN"))
    enable_attempted = False
    enable_response: dict[str, Any] | None = None
    final = initial
    if initial_state != "ENABLED":
        enable_attempted = True
        enable_response = google_request("POST", f"{service_url(project_id, service_name)}:enable", token, body={}, timeout=120)
        final = google_request("GET", service_url(project_id, service_name), token, timeout=60)
    return {
        "service_name": service_name,
        "initial_status": initial["status"],
        "initial_state": initial_state,
        "enable_attempted": enable_attempted,
        "enable_status": None if enable_response is None else enable_response["status"],
        "final_status": final["status"],
        "final_state": str(final.get("parsed", {}).get("state", "UNKNOWN")),
    }


def ensure_bigtable_imports() -> tuple[Any, Any, Any, Any]:
    SITE_PACKAGES.mkdir(parents=True, exist_ok=True)
    if str(SITE_PACKAGES) not in sys.path:
        sys.path.insert(0, str(SITE_PACKAGES))
    try:
        from google.cloud.bigtable.client import Client
        from google.cloud.bigtable import enums
        from google.cloud.bigtable.column_family import MaxVersionsGCRule
        from google.oauth2 import service_account
        return Client, enums, MaxVersionsGCRule, service_account
    except Exception:
        install = subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--disable-pip-version-check",
                "--target",
                str(SITE_PACKAGES),
                "google-cloud-bigtable>=2.28.1",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=300,
            check=False,
        )
        if install.returncode != 0:
            raise RuntimeError(f"google-cloud-bigtable install failed: {install.stderr.strip()}")
        from google.cloud.bigtable.client import Client
        from google.cloud.bigtable import enums
        from google.cloud.bigtable.column_family import MaxVersionsGCRule
        from google.oauth2 import service_account
        return Client, enums, MaxVersionsGCRule, service_account


def choose_zone(project_id: str, token: str, region: str) -> dict[str, Any]:
    response = google_request(
        "GET",
        f"https://compute.googleapis.com/compute/v1/projects/{project_id}/zones",
        token,
        timeout=90,
    )
    items = response.get("parsed", {}).get("items", []) if response["status"] == 200 else []
    candidates = [
        zone
        for zone in items
        if isinstance(zone, dict)
        and str(zone.get("region", "")).endswith(f"/regions/{region}")
        and str(zone.get("status", "")) == "UP"
    ]
    candidates.sort(key=lambda zone: str(zone.get("name", "")))
    return {
        "http_status": response["status"],
        "zone_names": [str(zone.get("name", "")) for zone in candidates],
        "selected_zone": str(candidates[0].get("name", "")) if candidates else "",
    }


def cell_value_to_text(row: Any, family: str, column: bytes) -> str:
    cells = getattr(row, "cells", {})
    family_cells = cells.get(family, {})
    column_cells = family_cells.get(column, [])
    if not column_cells:
        return ""
    return column_cells[0].value.decode("utf-8", errors="replace")


def write_outputs(payload: dict[str, Any]) -> None:
    write_json(OUTPUT_JSON, payload)
    lines = [
        "# V33 Bigtable Proof",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Proof state: `{payload['proof_state']}`",
        f"- Bigtable state: `{payload.get('bigtable_state', 'unknown')}`",
        f"- Primary identity: `{payload.get('primary_identity', '') or 'unknown'}`",
        f"- Selected zone: `{payload.get('selected_zone', '') or 'unresolved'}`",
        f"- Instance: `{payload.get('instance_id', '') or 'unknown'}`",
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
    parser = argparse.ArgumentParser(description="Run the bounded V33 Bigtable proof.")
    parser.add_argument("--bundle", default=str(DEFAULT_GCP_KEY_BUNDLE))
    parser.add_argument("--project-id", default=PROJECT_ID)
    parser.add_argument("--region", default=PRIMARY_REGION)
    parser.add_argument("--instance-id", default=DEFAULT_INSTANCE_ID)
    parser.add_argument("--cluster-id", default=DEFAULT_CLUSTER_ID)
    parser.add_argument("--app-profile-id", default=DEFAULT_APP_PROFILE_ID)
    parser.add_argument("--table-id", default=DEFAULT_TABLE_ID)
    args = parser.parse_args()

    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": "v33_omega",
        "overall_status": "WARN",
        "proof_state": "pending",
        "bigtable_state": "pending",
        "project_id": args.project_id,
        "region": args.region,
        "instance_id": args.instance_id,
        "cluster_id": args.cluster_id,
        "app_profile_id": args.app_profile_id,
        "table_id": args.table_id,
        "completed_steps": [],
        "blockers": [],
    }

    bundle = load_gcp_service_accounts(Path(args.bundle))
    records = {row["alias"]: row for row in bundle["records"]}
    primary = records.get("compute_default") or records.get("app_engine_default")
    if primary is None:
        payload["proof_state"] = "missing_primary_service_account"
        payload["bigtable_state"] = "blocked_missing_identity"
        payload["blockers"].append("No primary GCP service account was available for the Bigtable probe.")
        write_outputs(payload)
        return 1

    try:
        Client, enums, MaxVersionsGCRule, service_account = ensure_bigtable_imports()
        payload["completed_steps"].append("bigtable_client_ready")
    except Exception as exc:
        payload["proof_state"] = "bigtable_client_unavailable"
        payload["bigtable_state"] = "blocked_client_unavailable"
        payload["blockers"].append(str(exc))
        write_outputs(payload)
        return 1

    from google.auth.transport.requests import Request  # type: ignore

    credentials = service_account.Credentials.from_service_account_info(
        primary["info"],
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    credentials.refresh(Request())
    token = credentials.token or ""
    payload["primary_identity"] = mask_email(primary["client_email"])
    payload["completed_steps"].append("mint_primary_token")

    service_results = [ensure_service_enabled(args.project_id, token, service_name) for service_name in SERVICE_NAMES]
    payload["service_enablement"] = service_results
    if not all(result["final_status"] == 200 and result["final_state"] == "ENABLED" for result in service_results):
        payload["proof_state"] = "service_enablement_blocked"
        payload["bigtable_state"] = "blocked_service_enablement"
        payload["blockers"].append("One or more Bigtable APIs did not report `ENABLED` after the bounded enablement pass.")
        write_outputs(payload)
        return 1
    payload["completed_steps"].append("bigtable_services_enabled")

    zone_probe = choose_zone(args.project_id, token, args.region)
    payload["zone_probe"] = zone_probe
    selected_zone = zone_probe["selected_zone"]
    payload["selected_zone"] = selected_zone
    if zone_probe["http_status"] != 200 or not selected_zone:
        payload["proof_state"] = "zone_resolution_blocked"
        payload["bigtable_state"] = "blocked_zone_resolution"
        payload["blockers"].append("A usable zone in australia-southeast1 could not be resolved from the Compute API.")
        write_outputs(payload)
        return 1
    payload["completed_steps"].append("zone_resolved")

    client = Client(project=args.project_id, credentials=credentials, admin=True)
    instance = client.instance(
        args.instance_id,
        display_name=args.instance_id,
        instance_type=enums.Instance.Type.DEVELOPMENT,
        labels={"phase": "v33omega", "managed_by": "codex"},
    )

    instance_created = False
    if not instance.exists():
        cluster = instance.cluster(
            args.cluster_id,
            location_id=selected_zone,
            default_storage_type=enums.StorageType.SSD,
        )
        operation = instance.create(clusters=[cluster])
        operation.result(timeout=1800)
        instance_created = True
    instance.reload()
    payload["instance_created"] = instance_created
    payload["instance_state"] = str(instance.state)
    payload["completed_steps"].append("instance_ready")

    clusters, failed_locations = instance.list_clusters()
    payload["cluster_inventory"] = {
        "cluster_ids": [cluster.cluster_id for cluster in clusters],
        "failed_locations": list(failed_locations),
    }
    cluster_ids = {cluster.cluster_id for cluster in clusters}
    if args.cluster_id not in cluster_ids:
        payload["proof_state"] = "cluster_missing_after_instance_ready"
        payload["bigtable_state"] = "blocked_cluster_missing"
        payload["blockers"].append("The expected Bigtable cluster was not present after instance readiness.")
        write_outputs(payload)
        return 1
    payload["completed_steps"].append("cluster_ready")

    app_profile = instance.app_profile(
        args.app_profile_id,
        routing_policy_type=enums.RoutingPolicyType.SINGLE,
        description="V33 omega bounded app profile",
        cluster_id=args.cluster_id,
        allow_transactional_writes=True,
    )
    app_profile_created = False
    if not app_profile.exists():
        app_profile = app_profile.create(ignore_warnings=True)
        app_profile_created = True
    else:
        app_profile.reload()
    payload["app_profile_created"] = app_profile_created
    payload["completed_steps"].append("app_profile_ready")

    table = instance.table(args.table_id, app_profile_id=args.app_profile_id)
    table_created = False
    if not table.exists():
        table.create(column_families={DEFAULT_COLUMN_FAMILY: MaxVersionsGCRule(1)})
        table_created = True
    payload["table_created"] = table_created
    payload["completed_steps"].append("table_ready")

    row_key = f"v33-smoke-{int(time.time())}".encode("utf-8")
    row = table.direct_row(row_key)
    row.set_cell(DEFAULT_COLUMN_FAMILY, b"status", b"v33-bigtable-ok")
    row.commit()
    payload["completed_steps"].append("row_written")

    read_back = table.read_row(row_key)
    value = cell_value_to_text(read_back, DEFAULT_COLUMN_FAMILY, b"status") if read_back is not None else ""
    payload["row_readback"] = {
        "row_found": read_back is not None,
        "value": value,
    }
    if read_back is None or value != "v33-bigtable-ok":
        payload["proof_state"] = "row_readback_blocked"
        payload["bigtable_state"] = "blocked_row_readback"
        payload["blockers"].append("The V33 smoke row was not recovered cleanly from Bigtable after the write.")
        write_outputs(payload)
        return 1
    payload["completed_steps"].append("row_readback_verified")

    delete_row = table.direct_row(row_key)
    delete_row.delete()
    delete_row.commit()
    deleted = table.read_row(row_key)
    payload["row_delete_check"] = {"deleted": deleted is None}
    if deleted is not None:
        payload["proof_state"] = "row_delete_blocked"
        payload["bigtable_state"] = "blocked_row_delete"
        payload["blockers"].append("The V33 smoke row remained visible after the delete cycle.")
        write_outputs(payload)
        return 1
    payload["completed_steps"].append("row_delete_verified")

    payload["overall_status"] = "PASS"
    payload["proof_state"] = "development_instance_table_row_cycle_verified"
    payload["bigtable_state"] = "development_instance_verified"
    write_outputs(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
