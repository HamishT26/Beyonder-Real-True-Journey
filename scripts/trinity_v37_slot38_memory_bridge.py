#!/usr/bin/env python3
"""Run V37 slot-38 durable-memory proofs across bounded backend modes."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from trinity_v32_runtime_common import google_request, run_cmd
from trinity_v33_bigtable_probe import choose_zone, cell_value_to_text
from trinity_v36_cloud_common import (
    DEFAULT_MODEL_LOCATION,
    DEFAULT_REGIONAL_LOCATION,
    PROJECT_ID,
    ROOT,
    ensure_service_enabled,
    load_primary_service_account,
    now_iso,
    primary_identity_fields,
    write_json,
    write_text,
)

DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v37-slot-38-memory-bridge-proof-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v37-slot-38-memory-bridge-proof-v1.md"
BIGTABLE_SITE_PACKAGES = ROOT / ".local-runtime" / "bigtable-site-packages"
BIGTABLE_SERVICE_NAMES = [
    "bigtableadmin.googleapis.com",
    "bigtable.googleapis.com",
    "compute.googleapis.com",
]
OFFICIAL_SOURCES = {
    "agent_builder_locations": "https://docs.cloud.google.com/agent-builder/locations",
    "bigtable_instances": "https://cloud.google.com/bigtable/docs/instances-clusters-nodes",
    "bigtable_python_client": "https://cloud.google.com/python/docs/reference/bigtable/latest",
}


def ensure_v37_bigtable_imports() -> tuple[Any, Any, Any, Any]:
    BIGTABLE_SITE_PACKAGES.mkdir(parents=True, exist_ok=True)
    if str(BIGTABLE_SITE_PACKAGES) not in sys.path:
        sys.path.insert(0, str(BIGTABLE_SITE_PACKAGES))
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
                "--upgrade",
                "--disable-pip-version-check",
                "--target",
                str(BIGTABLE_SITE_PACKAGES),
                "google-cloud-bigtable>=2.28.1",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=600,
            check=False,
        )
        if install.returncode != 0:
            raise RuntimeError(f"google-cloud-bigtable install failed: {install.stderr.strip()}")
        if str(BIGTABLE_SITE_PACKAGES) not in sys.path:
            sys.path.insert(0, str(BIGTABLE_SITE_PACKAGES))
        from google.cloud.bigtable.client import Client
        from google.cloud.bigtable import enums
        from google.cloud.bigtable.column_family import MaxVersionsGCRule
        from google.oauth2 import service_account
        return Client, enums, MaxVersionsGCRule, service_account


def write_outputs(payload: dict[str, Any], output_json: Path, output_md: Path) -> None:
    write_json(output_json, payload)
    lines = [
        "# V37 Slot 38 Memory Bridge Proof",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Slot number: `{payload['slot_number']}`",
        f"- Memory mode: `{payload['memory_mode']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Proof state: `{payload['proof_state']}`",
        f"- Durable memory state: `{payload.get('durable_memory_state', 'unknown')}`",
        f"- Promotion gate ready: `{payload.get('promotion_gate_ready', False)}`",
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
    write_text(output_md, "\n".join(lines) + "\n")


def run_agent_engine_mode(args: argparse.Namespace) -> dict[str, Any]:
    child_json = ROOT / "docs" / "trinity-live-traces" / f"v37-slot-{args.slot_number}-agent-engine-proof-v1.json"
    child_md = ROOT / "docs" / "trinity-live-traces" / f"v37-slot-{args.slot_number}-agent-engine-proof-v1.md"
    command = [
        sys.executable,
        "scripts/trinity_v36_memory_bank_probe.py",
        "--bundle",
        args.bundle,
        "--project-id",
        args.project_id,
        "--regional-location",
        args.regional_location,
        "--model-location",
        args.model_location,
        "--phase-label",
        "v37_omega",
        "--output-json",
        str(child_json),
        "--output-md",
        str(child_md),
    ]
    proc = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=3600,
        check=False,
    )
    report: dict[str, Any] = {}
    if child_json.exists():
        report = json.loads(child_json.read_text(encoding="utf-8-sig"))
    promotion_ready = bool(report.get("promotion_gate_ready"))
    blockers = [str(item) for item in report.get("blockers", [])] if isinstance(report.get("blockers"), list) else []
    return {
        "overall_status": "PASS" if promotion_ready else ("FAIL" if proc.returncode else "WARN"),
        "proof_state": str(report.get("proof_state") or ("agent_engine_subprocess_failed" if proc.returncode else "agent_engine_incomplete")),
        "durable_memory_state": str(report.get("memory_bank_state") or "agent_engine_unresolved"),
        "promotion_gate_ready": promotion_ready,
        "completed_steps": ["agent_engine_probe_executed"],
        "blockers": blockers,
        "child_proof_path": str(child_json),
        "child_proof_md_path": str(child_md),
        "child_process": {
            "returncode": proc.returncode,
            "stdout_excerpt": proc.stdout[-3000:],
            "stderr_excerpt": proc.stderr[-2000:],
        },
        "child_report": report,
    }


def run_bigtable_mode(args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "overall_status": "WARN",
        "proof_state": "pending",
        "durable_memory_state": "pending",
        "promotion_gate_ready": False,
        "completed_steps": [],
        "blockers": [],
        "official_sources": OFFICIAL_SOURCES,
    }
    sync_run = run_cmd([sys.executable, "scripts/trinity_memory_bank_sync.py", "--label", f"v37-slot-{args.slot_number}-memory"], timeout=1800)
    payload["repo_sync_run"] = {"returncode": sync_run.returncode, "stdout": sync_run.stdout[-2000:], "stderr": sync_run.stderr[-2000:]}
    if sync_run.returncode == 0:
        payload["completed_steps"].append("repo_memory_bank_sync_ran")

    validator_run = run_cmd([sys.executable, "scripts/trinity_memory_bank_validator.py"], timeout=300)
    payload["repo_validator_run"] = {"returncode": validator_run.returncode, "stdout": validator_run.stdout[-2000:], "stderr": validator_run.stderr[-2000:]}
    if validator_run.returncode == 0:
        payload["completed_steps"].append("repo_memory_bank_validator_ran")

    try:
        _records, primary, minted = load_primary_service_account(Path(args.bundle))
    except Exception as exc:
        payload["overall_status"] = "FAIL"
        payload["proof_state"] = "missing_primary_service_account"
        payload["durable_memory_state"] = "blocked_missing_identity"
        payload["blockers"].append(str(exc))
        return payload

    payload.update(primary_identity_fields(primary, minted))
    token = minted["token"]
    payload["completed_steps"].append("mint_primary_token")

    service_results = [ensure_service_enabled(args.project_id, token, service_name) for service_name in BIGTABLE_SERVICE_NAMES]
    payload["service_enablement"] = service_results
    if not all(result["final_status"] == 200 and result["final_state"] == "ENABLED" for result in service_results):
        payload["overall_status"] = "FAIL"
        payload["proof_state"] = "bigtable_service_enablement_blocked"
        payload["durable_memory_state"] = "blocked_service_enablement"
        payload["blockers"].append("One or more Bigtable or Compute APIs did not report ENABLED.")
        return payload
    payload["completed_steps"].append("bigtable_services_enabled")

    zone_probe = choose_zone(args.project_id, token, args.regional_location)
    payload["zone_probe"] = zone_probe
    selected_zone = str(zone_probe.get("selected_zone") or "")
    if not selected_zone:
        payload["overall_status"] = "FAIL"
        payload["proof_state"] = "zone_resolution_blocked"
        payload["durable_memory_state"] = "blocked_zone_resolution"
        payload["blockers"].append(f"No usable zone was resolved inside `{args.regional_location}` for the Bigtable backend.")
        return payload
    payload["selected_zone"] = selected_zone
    payload["completed_steps"].append("zone_resolved")

    try:
        Client, enums, MaxVersionsGCRule, service_account = ensure_v37_bigtable_imports()
        payload["completed_steps"].append("bigtable_client_ready")
    except Exception as exc:
        payload["overall_status"] = "FAIL"
        payload["proof_state"] = "bigtable_client_unavailable"
        payload["durable_memory_state"] = "blocked_client_unavailable"
        payload["blockers"].append(str(exc))
        return payload

    from google.auth.transport.requests import Request  # type: ignore

    credentials = service_account.Credentials.from_service_account_info(
        primary["info"],
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    credentials.refresh(Request())
    client = Client(project=args.project_id, credentials=credentials, admin=True)

    instance = client.instance(
        args.instance_id,
        display_name=args.instance_id,
        instance_type=enums.Instance.Type.DEVELOPMENT,
        labels={"phase": "v37omega", "managed_by": "codex", "slot": str(args.slot_number)},
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
    cluster_ids = [cluster.cluster_id for cluster in clusters]
    payload["cluster_inventory"] = {"cluster_ids": cluster_ids, "failed_locations": list(failed_locations)}
    selected_cluster_id = args.cluster_id if args.cluster_id in cluster_ids else (cluster_ids[0] if cluster_ids else "")
    if not selected_cluster_id:
        payload["overall_status"] = "FAIL"
        payload["proof_state"] = "cluster_missing_after_instance_ready"
        payload["durable_memory_state"] = "blocked_cluster_missing"
        payload["blockers"].append("No usable cluster was found inside the V37 Bigtable instance.")
        return payload
    payload["selected_cluster_id"] = selected_cluster_id
    payload["completed_steps"].append("cluster_ready")

    app_profile = instance.app_profile(
        args.app_profile_id,
        routing_policy_type=enums.RoutingPolicyType.SINGLE,
        description=f"V37 slot {args.slot_number} durable memory proof",
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
        table.create(column_families={"cf1": MaxVersionsGCRule(1)})
        table_created = True
    payload["table_created"] = table_created
    payload["completed_steps"].append("table_ready")

    row_key = f"v37-slot-{args.slot_number}-{int(time.time())}".encode("utf-8")
    row = table.direct_row(row_key)
    row.set_cell("cf1", b"status", b"v37-bigtable-ok")
    row.set_cell("cf1", b"slot", str(args.slot_number).encode("utf-8"))
    row.set_cell("cf1", b"phase", b"v37_omega")
    row.commit()
    payload["completed_steps"].append("row_written")

    fresh_table = instance.table(args.table_id, app_profile_id=args.app_profile_id)
    read_back = fresh_table.read_row(row_key)
    status_value = cell_value_to_text(read_back, "cf1", b"status") if read_back is not None else ""
    slot_value = cell_value_to_text(read_back, "cf1", b"slot") if read_back is not None else ""
    phase_value = cell_value_to_text(read_back, "cf1", b"phase") if read_back is not None else ""
    payload["row_readback"] = {
        "row_found": read_back is not None,
        "status": status_value,
        "slot": slot_value,
        "phase": phase_value,
    }
    if read_back is None or status_value != "v37-bigtable-ok" or slot_value != str(args.slot_number) or phase_value != "v37_omega":
        payload["overall_status"] = "FAIL"
        payload["proof_state"] = "row_readback_blocked"
        payload["durable_memory_state"] = "blocked_row_readback"
        payload["blockers"].append("The bounded Bigtable row was not recovered cleanly after the write.")
        return payload
    payload["completed_steps"].append("row_readback_verified")

    delete_row = fresh_table.direct_row(row_key)
    delete_row.delete()
    delete_row.commit()
    deleted = fresh_table.read_row(row_key)
    payload["row_delete_check"] = {"deleted": deleted is None}
    if deleted is not None:
        payload["overall_status"] = "FAIL"
        payload["proof_state"] = "row_delete_blocked"
        payload["durable_memory_state"] = "blocked_row_delete"
        payload["blockers"].append("The bounded Bigtable row remained visible after the delete cycle.")
        return payload
    payload["completed_steps"].append("row_delete_verified")

    payload["overall_status"] = "PASS"
    payload["proof_state"] = "bigtable_row_cycle_verified"
    payload["durable_memory_state"] = "bigtable_live_write_read_delete_verified"
    payload["promotion_gate_ready"] = True
    return payload


def run_cloud_sql_mode() -> dict[str, Any]:
    return {
        "overall_status": "WARN",
        "proof_state": "cloud_sql_lane_not_implemented",
        "durable_memory_state": "not_attempted",
        "promotion_gate_ready": False,
        "completed_steps": [],
        "blockers": [
            "The Cloud SQL durable-memory lane is recognized by the V37 bridge interface but is not yet implemented in-repo.",
            "V37 continues on the proven Bigtable fallback path for live write/read-back durability.",
        ],
        "official_sources": OFFICIAL_SOURCES,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run bounded V37 slot-38 durable-memory proofs.")
    parser.add_argument("--bundle", default=str(Path.home() / "GCP service account keys.txt"))
    parser.add_argument("--project-id", default=PROJECT_ID)
    parser.add_argument("--regional-location", default=DEFAULT_REGIONAL_LOCATION)
    parser.add_argument("--model-location", default=DEFAULT_MODEL_LOCATION)
    parser.add_argument("--slot-number", type=int, default=38)
    parser.add_argument("--memory-mode", choices=["agent_engine", "bigtable", "cloud_sql"], default="agent_engine")
    parser.add_argument("--instance-id", default="beyonder-v37-slot38-dev")
    parser.add_argument("--cluster-id", default="beyonder-v37-slot38-dev-cluster")
    parser.add_argument("--app-profile-id", default="v37-slot38-app")
    parser.add_argument("--table-id", default="v37_slot38_memory")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()

    output_json = Path(args.output_json)
    output_md = Path(args.output_md)
    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": "v37_omega",
        "slot_number": args.slot_number,
        "memory_mode": args.memory_mode,
        "project_id": args.project_id,
        "regional_location": args.regional_location,
        "model_location": args.model_location,
        "overall_status": "WARN",
        "proof_state": "pending",
        "durable_memory_state": "pending",
        "promotion_gate_ready": False,
        "completed_steps": [],
        "blockers": [],
    }

    mode_payload: dict[str, Any]
    if args.memory_mode == "agent_engine":
        mode_payload = run_agent_engine_mode(args)
    elif args.memory_mode == "bigtable":
        mode_payload = run_bigtable_mode(args)
    else:
        mode_payload = run_cloud_sql_mode()

    payload.update(mode_payload)
    write_outputs(payload, output_json, output_md)
    return 0 if payload.get("promotion_gate_ready") else (1 if payload.get("overall_status") == "FAIL" else 0)


if __name__ == "__main__":
    raise SystemExit(main())
