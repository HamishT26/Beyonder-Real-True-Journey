#!/usr/bin/env python3
"""Verify the V38 fleet-centered Anthos and Connect Gateway lane."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

from trinity_v32_runtime_common import PROJECT_ID, google_request
from trinity_v36_cloud_common import ensure_service_enabled, load_primary_service_account, now_iso, write_json, write_text
from trinity_v38_windows_operator_probe import build_gcloud_env, ensure_operator_lane

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v38-fleet-anthos-proof-v1.json"
OUTPUT_MD = ROOT / "docs" / "trinity-live-traces" / "v38-fleet-anthos-proof-v1.md"
DEFAULT_CLUSTER = "beyonder-v32-autopilot-dev"
DEFAULT_MEMBERSHIP = "beyonder-v32-autopilot-dev-membership"
DEFAULT_REGION = "australia-southeast1"
KUBECONFIG_PATH = ROOT / ".local-runtime" / "kubeconfig" / "v38-fleet-gateway.yaml"
SERVICE_NAMES = [
    "container.googleapis.com",
    "connectgateway.googleapis.com",
    "gkeconnect.googleapis.com",
    "gkehub.googleapis.com",
]


def run(args: list[str], *, env: dict[str, str] | None = None, timeout: int = 1800) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            args,
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        return subprocess.CompletedProcess(
            args=args,
            returncode=124,
            stdout=(exc.stdout or "") if isinstance(exc.stdout, str) else "",
            stderr=((exc.stderr or "") if isinstance(exc.stderr, str) else "") + f"\ncommand timed out after {timeout} seconds",
        )


def kubectl_path() -> str:
    return shutil.which("kubectl") or str(Path(r"C:\Program Files\Docker\Docker\resources\bin\kubectl.exe"))


def describe_clusters(project_id: str, token: str) -> dict[str, Any]:
    return google_request(
        "GET",
        f"https://container.googleapis.com/v1/projects/{project_id}/locations/-/clusters",
        token,
        timeout=240,
    )


def list_memberships(project_id: str, token: str) -> dict[str, Any]:
    return google_request(
        "GET",
        f"https://gkehub.googleapis.com/v1/projects/{project_id}/locations/-/memberships",
        token,
        timeout=240,
    )


def cluster_resource_match(membership: dict[str, Any], cluster_name: str, location: str) -> bool:
    endpoint = membership.get("endpoint", {}) if isinstance(membership.get("endpoint"), dict) else {}
    gke_cluster = endpoint.get("gkeCluster", {}) if isinstance(endpoint.get("gkeCluster"), dict) else {}
    resource_link = str(gke_cluster.get("resourceLink") or "")
    haystack = resource_link.lower()
    return cluster_name.lower() in haystack and location.lower() in haystack


def location_flag(cluster: dict[str, Any]) -> list[str]:
    location = str(cluster.get("location") or "")
    location_type = str(cluster.get("locationType") or "").upper()
    if location_type == "ZONE":
        return ["--zone", location]
    return ["--region", location]


def membership_name_from_resource(resource_name: str) -> str:
    return str(resource_name or "").rsplit("/", 1)[-1]


def membership_location_from_resource(resource_name: str) -> str:
    parts = str(resource_name or "").split("/")
    try:
        index = parts.index("locations")
    except ValueError:
        return "global"
    return parts[index + 1] if index + 1 < len(parts) else "global"


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V38 Fleet Anthos Proof",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Anthos state: `{payload['anthos_state']}`",
        f"- Fleet state: `{payload['gke_fleet_state']}`",
        f"- Connect Gateway state: `{payload['connect_gateway_state']}`",
        f"- Membership: `{payload.get('membership_name', '') or 'unresolved'}`",
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
    parser = argparse.ArgumentParser(description="Verify the V38 fleet-centered Anthos and Connect Gateway lane.")
    parser.add_argument("--bundle", default=str(Path.home() / "GCP service account keys.txt"))
    parser.add_argument("--project-id", default=PROJECT_ID)
    parser.add_argument("--cluster", default=DEFAULT_CLUSTER)
    parser.add_argument("--membership", default=DEFAULT_MEMBERSHIP)
    parser.add_argument("--output-json", default=str(OUTPUT_JSON))
    parser.add_argument("--output-md", default=str(OUTPUT_MD))
    args = parser.parse_args()

    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": "v38_omega",
        "project_id": args.project_id,
        "cluster_name": args.cluster,
        "overall_status": "WARN",
        "anthos_state": "pending",
        "gke_fleet_state": "pending",
        "connect_gateway_state": "pending",
        "completed_steps": [],
        "blockers": [],
    }

    try:
        _records, primary, minted = load_primary_service_account(Path(args.bundle))
    except Exception as exc:
        payload["overall_status"] = "FAIL"
        payload["anthos_state"] = "blocked_missing_identity"
        payload["gke_fleet_state"] = "blocked_missing_identity"
        payload["connect_gateway_state"] = "blocked_missing_identity"
        payload["blockers"].append(str(exc))
        write_json(Path(args.output_json), payload)
        write_text(Path(args.output_md), markdown(payload))
        return 1

    token = minted["token"]
    payload["primary_identity"] = str(primary["client_email"])
    payload["service_account_path"] = str(primary["runtime_path"])
    payload["completed_steps"].append("mint_primary_token")

    service_results = [ensure_service_enabled(args.project_id, token, service_name) for service_name in SERVICE_NAMES]
    payload["service_enablement"] = service_results
    if not all(result["final_status"] == 200 and result["final_state"] == "ENABLED" for result in service_results):
        payload["overall_status"] = "FAIL"
        payload["anthos_state"] = "blocked_service_enablement"
        payload["gke_fleet_state"] = "blocked_service_enablement"
        payload["connect_gateway_state"] = "blocked_service_enablement"
        payload["blockers"].append("The container, fleet, or Connect services did not reach ENABLED state.")
        write_json(Path(args.output_json), payload)
        write_text(Path(args.output_md), markdown(payload))
        return 1
    payload["completed_steps"].append("fleet_services_enabled")

    operator = ensure_operator_lane(args.bundle, bootstrap=True)
    payload["windows_operator_dependency"] = {
        "overall_status": operator.get("overall_status"),
        "windows_operator_lane_state": operator.get("windows_operator_lane_state"),
        "gcloud_path": operator.get("gcloud_path"),
    }
    if operator.get("overall_status") != "PASS":
        payload["overall_status"] = "FAIL"
        payload["anthos_state"] = "blocked_operator_lane"
        payload["gke_fleet_state"] = "blocked_operator_lane"
        payload["connect_gateway_state"] = "blocked_operator_lane"
        payload["blockers"].extend(str(row) for row in operator.get("blockers", []))
        write_json(Path(args.output_json), payload)
        write_text(Path(args.output_md), markdown(payload))
        return 1
    payload["completed_steps"].append("windows_operator_lane_reused")

    cluster_response = describe_clusters(args.project_id, token)
    payload["cluster_inventory_status"] = cluster_response["status"]
    clusters = cluster_response.get("parsed", {}).get("clusters", []) if cluster_response["status"] == 200 else []
    target_cluster = next((row for row in clusters if isinstance(row, dict) and str(row.get("name") or "") == args.cluster), None)
    if target_cluster is None:
        payload["overall_status"] = "FAIL"
        payload["anthos_state"] = "blocked_cluster_visibility"
        payload["gke_fleet_state"] = "blocked_cluster_visibility"
        payload["connect_gateway_state"] = "blocked_cluster_visibility"
        payload["blockers"].append(f"The target cluster `{args.cluster}` is not visible from the Container API.")
        write_json(Path(args.output_json), payload)
        write_text(Path(args.output_md), markdown(payload))
        return 1
    payload["cluster_probe"] = {
        "location": str(target_cluster.get("location") or ""),
        "locationType": str(target_cluster.get("locationType") or ""),
        "status": str(target_cluster.get("status") or ""),
        "selfLink": str(target_cluster.get("selfLink") or ""),
    }
    payload["completed_steps"].append("target_cluster_visible")

    memberships_before = list_memberships(args.project_id, token)
    memberships = memberships_before.get("parsed", {}).get("resources", []) if memberships_before["status"] == 200 else []
    matched_membership = next(
        (
            row
            for row in memberships
            if isinstance(row, dict) and cluster_resource_match(row, args.cluster, str(target_cluster.get("location") or ""))
        ),
        None,
    )

    env = build_gcloud_env()
    env["KUBECONFIG"] = str(KUBECONFIG_PATH)
    gcloud_path = str(operator.get("gcloud_path") or "gcloud")
    gcloud_bin = str(Path(gcloud_path).parent)
    env["PATH"] = f"{gcloud_bin}{os.pathsep}{env.get('PATH', '')}" if env.get("PATH") else gcloud_bin
    if matched_membership is None:
        register = run(
            [
                gcloud_path,
                "container",
                "clusters",
                "update",
                args.cluster,
                *location_flag(target_cluster),
                "--project",
                args.project_id,
                "--enable-fleet",
                "--quiet",
            ],
            env=env,
            timeout=3600,
        )
        payload["fleet_registration_attempt"] = {
            "command": register.args,
            "returncode": register.returncode,
            "stdout_excerpt": register.stdout[-4000:],
            "stderr_excerpt": register.stderr[-3000:],
        }
        if register.returncode == 0:
            payload["completed_steps"].append("cluster_enable_fleet_attempted")
        memberships_after = list_memberships(args.project_id, token)
        payload["membership_inventory_after_status"] = memberships_after["status"]
        memberships = memberships_after.get("parsed", {}).get("resources", []) if memberships_after["status"] == 200 else []
        matched_membership = next(
            (
                row
                for row in memberships
                if isinstance(row, dict) and cluster_resource_match(row, args.cluster, str(target_cluster.get("location") or ""))
            ),
            None,
        )

    if matched_membership is None:
        payload["overall_status"] = "FAIL"
        payload["anthos_state"] = "fleet_centered_anthos_blocked"
        payload["gke_fleet_state"] = "blocked_membership_missing"
        payload["connect_gateway_state"] = "blocked_membership_missing"
        payload["blockers"].append("Fleet membership was not visible for the target cluster after the bounded registration attempt.")
        write_json(Path(args.output_json), payload)
        write_text(Path(args.output_md), markdown(payload))
        return 1

    payload["membership_name"] = membership_name_from_resource(str(matched_membership.get("name") or ""))
    payload["membership_resource"] = str(matched_membership.get("name") or "")
    payload["membership_location"] = membership_location_from_resource(payload["membership_resource"])
    payload["membership_state"] = str(matched_membership.get("state", {}).get("code") or "")
    payload["completed_steps"].append("fleet_membership_verified")

    gateway = run(
        [
            gcloud_path,
            "container",
            "fleet",
            "memberships",
            "get-credentials",
            payload["membership_name"],
            "--location",
            payload["membership_location"],
            "--project",
            args.project_id,
        ],
        env=env,
        timeout=1800,
    )
    payload["connect_gateway_credentials"] = {
        "returncode": gateway.returncode,
        "stdout_excerpt": gateway.stdout[-3000:],
        "stderr_excerpt": gateway.stderr[-3000:],
        "kubeconfig_path": str(KUBECONFIG_PATH),
    }
    if gateway.returncode != 0:
        payload["overall_status"] = "FAIL"
        payload["anthos_state"] = "fleet_centered_anthos_verified"
        payload["gke_fleet_state"] = "membership_verified"
        payload["connect_gateway_state"] = "blocked_gateway_credentials"
        payload["blockers"].append("Connect Gateway credentials could not be generated for the fleet membership.")
        write_json(Path(args.output_json), payload)
        write_text(Path(args.output_md), markdown(payload))
        return 1
    payload["completed_steps"].append("connect_gateway_credentials_fetched")

    kubectl = kubectl_path()
    kubectl_run = run([kubectl, "--kubeconfig", str(KUBECONFIG_PATH), "get", "namespaces"], env=env, timeout=600)
    payload["connect_gateway_kubectl"] = {
        "returncode": kubectl_run.returncode,
        "stdout_excerpt": kubectl_run.stdout[-4000:],
        "stderr_excerpt": kubectl_run.stderr[-3000:],
    }
    if kubectl_run.returncode != 0:
        payload["overall_status"] = "FAIL"
        payload["anthos_state"] = "fleet_centered_anthos_verified"
        payload["gke_fleet_state"] = "membership_verified"
        payload["connect_gateway_state"] = "gateway_credentials_created_kubectl_failed"
        payload["blockers"].append("kubectl could not read namespaces through the Connect Gateway kubeconfig.")
        write_json(Path(args.output_json), payload)
        write_text(Path(args.output_md), markdown(payload))
        return 1

    payload["completed_steps"].append("connect_gateway_kubectl_verified")
    payload["overall_status"] = "PASS"
    payload["anthos_state"] = "fleet_centered_anthos_verified"
    payload["gke_fleet_state"] = "membership_verified"
    payload["connect_gateway_state"] = "kubectl_access_verified"
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
