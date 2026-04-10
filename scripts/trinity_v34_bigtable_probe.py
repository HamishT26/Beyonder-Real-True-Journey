#!/usr/bin/env python3
"""Run a bounded V34 Bigtable persistence proof using the existing dev instance."""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from trinity_v34_cloud_common import (
    BIGTABLE_SERVICE_NAMES,
    PHASE,
    PROJECT_ID,
    PRIMARY_REGION,
    ensure_service_enabled,
    load_primary_service_account,
    mask_email,
    now_iso,
    write_json,
    write_text,
)

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v34-bigtable-proof-v1.json"
OUTPUT_MD = ROOT / "docs" / "trinity-live-traces" / "v34-bigtable-proof-v1.md"
SITE_PACKAGES = ROOT / ".local-runtime" / "site-packages"
DEFAULT_INSTANCE_ID = "beyonder-v33-dev"
DEFAULT_CLUSTER_ID = "beyonder-v33-dev-cluster"
DEFAULT_APP_PROFILE_ID = "v34-omega-app"
DEFAULT_TABLE_ID = "v34_omega_persistence"
DEFAULT_COLUMN_FAMILY = "cf1"


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
        "# V34 Bigtable Proof",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Proof state: `{payload['proof_state']}`",
        f"- Bigtable state: `{payload.get('bigtable_state', 'unknown')}`",
        f"- Primary identity: `{payload.get('primary_identity', '') or 'unknown'}`",
        f"- Selected cluster: `{payload.get('selected_cluster_id', '') or 'unresolved'}`",
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
    parser = argparse.ArgumentParser(description="Run the bounded V34 Bigtable persistence proof.")
    parser.add_argument("--bundle", default=str(Path.home() / "GCP service account keys.txt"))
    parser.add_argument("--project-id", default=PROJECT_ID)
    parser.add_argument("--region", default=PRIMARY_REGION)
    parser.add_argument("--instance-id", default=DEFAULT_INSTANCE_ID)
    parser.add_argument("--cluster-id", default=DEFAULT_CLUSTER_ID)
    parser.add_argument("--app-profile-id", default=DEFAULT_APP_PROFILE_ID)
    parser.add_argument("--table-id", default=DEFAULT_TABLE_ID)
    args = parser.parse_args()

    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": PHASE,
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
        "row_rounds": 2,
    }

    try:
        _bundle, primary, minted = load_primary_service_account(Path(args.bundle))
    except Exception as exc:
        payload["proof_state"] = "missing_primary_service_account"
        payload["bigtable_state"] = "blocked_missing_identity"
        payload["blockers"].append(str(exc))
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

    service_results = [ensure_service_enabled(args.project_id, token, service_name) for service_name in BIGTABLE_SERVICE_NAMES]
    payload["service_enablement"] = service_results
    if not all(result["final_status"] == 200 and result["final_state"] == "ENABLED" for result in service_results):
        payload["proof_state"] = "service_enablement_blocked"
        payload["bigtable_state"] = "blocked_service_enablement"
        payload["blockers"].append("One or more Bigtable APIs did not report `ENABLED` after the bounded enablement pass.")
        write_outputs(payload)
        return 1
    payload["completed_steps"].append("bigtable_services_enabled")

    client = Client(project=args.project_id, credentials=credentials, admin=True)
    instance = client.instance(args.instance_id)
    if not instance.exists():
        payload["proof_state"] = "instance_missing"
        payload["bigtable_state"] = "blocked_instance_missing"
        payload["blockers"].append("The expected development Bigtable instance does not exist.")
        write_outputs(payload)
        return 1
    instance.reload()
    payload["instance_state"] = str(instance.state)
    payload["completed_steps"].append("instance_ready")

    clusters, failed_locations = instance.list_clusters()
    cluster_ids = [cluster.cluster_id for cluster in clusters]
    payload["cluster_inventory"] = {"cluster_ids": cluster_ids, "failed_locations": list(failed_locations)}
    selected_cluster_id = args.cluster_id if args.cluster_id in cluster_ids else (cluster_ids[0] if cluster_ids else "")
    payload["selected_cluster_id"] = selected_cluster_id
    if not selected_cluster_id:
        payload["proof_state"] = "cluster_missing_after_instance_ready"
        payload["bigtable_state"] = "blocked_cluster_missing"
        payload["blockers"].append("No usable cluster was found inside the development Bigtable instance.")
        write_outputs(payload)
        return 1
    payload["completed_steps"].append("cluster_ready")

    app_profile = instance.app_profile(
        args.app_profile_id,
        routing_policy_type=enums.RoutingPolicyType.SINGLE,
        description="V34 omega bounded app profile",
        cluster_id=selected_cluster_id,
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

    row_prefix = f"v34-bigtable-{int(time.time())}"
    row_specs = [
        (f"{row_prefix}-a".encode("utf-8"), "round-1"),
        (f"{row_prefix}-b".encode("utf-8"), "round-2"),
    ]
    payload["row_keys"] = [spec[0].decode("utf-8") for spec in row_specs]
    payload["row_values"] = {}

    for row_key, round_name in row_specs:
        row = table.direct_row(row_key)
        row.set_cell(DEFAULT_COLUMN_FAMILY, b"status", b"v34-bigtable-ok")
        row.set_cell(DEFAULT_COLUMN_FAMILY, b"round", round_name.encode("utf-8"))
        row.commit()
    payload["completed_steps"].append("rows_written")

    fresh_table = instance.table(args.table_id, app_profile_id=args.app_profile_id)
    for row_key, round_name in row_specs:
        read_back = fresh_table.read_row(row_key)
        status_value = cell_value_to_text(read_back, DEFAULT_COLUMN_FAMILY, b"status") if read_back is not None else ""
        round_value = cell_value_to_text(read_back, DEFAULT_COLUMN_FAMILY, b"round") if read_back is not None else ""
        payload["row_values"][row_key.decode("utf-8")] = {
            "row_found": read_back is not None,
            "status": status_value,
            "round": round_value,
        }
        if read_back is None or status_value != "v34-bigtable-ok" or round_value != round_name:
            payload["proof_state"] = "row_readback_blocked"
            payload["bigtable_state"] = "blocked_row_readback"
            payload["blockers"].append("One of the bounded Bigtable rows was not recovered cleanly after the write.")
            write_outputs(payload)
            return 1
    payload["completed_steps"].append("row_readback_verified")

    for row_key, _ in row_specs:
        delete_row = fresh_table.direct_row(row_key)
        delete_row.delete()
        delete_row.commit()
        if fresh_table.read_row(row_key) is not None:
            payload["proof_state"] = "row_delete_blocked"
            payload["bigtable_state"] = "blocked_row_delete"
            payload["blockers"].append("One of the bounded Bigtable rows remained visible after the delete cycle.")
            write_outputs(payload)
            return 1
    payload["completed_steps"].append("row_delete_verified")

    payload["overall_status"] = "PASS"
    payload["proof_state"] = "two_row_persistence_verified"
    payload["bigtable_state"] = "development_instance_verified"
    write_outputs(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
