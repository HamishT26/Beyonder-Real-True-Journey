#!/usr/bin/env python3
"""Create and validate the bounded V32 GKE Autopilot lane."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

from trinity_v32_runtime_common import (
    DEFAULT_GCP_KEY_BUNDLE,
    PRIMARY_CLUSTER,
    PRIMARY_NAMESPACE,
    PRIMARY_REGION,
    PROJECT_ID,
    google_request,
    load_gcp_service_accounts,
    mask_email,
    mint_access_token,
    now_iso,
    run_cmd,
    temp_file,
    temp_kubeconfig,
    windows_kubectl,
    write_json,
    write_text,
    wsl_probe,
)

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v32-gke-bootstrap-proof-v1.json"
OUTPUT_MD = ROOT / "docs" / "trinity-live-traces" / "v32-gke-bootstrap-proof-v1.md"


def clusters_url(project_id: str, region: str) -> str:
    return f"https://container.googleapis.com/v1/projects/{project_id}/locations/{region}/clusters"


def cluster_url(project_id: str, region: str, cluster_name: str) -> str:
    return f"{clusters_url(project_id, region)}/{cluster_name}"


def operation_url(name_or_url: str) -> str:
    if name_or_url.startswith("http://") or name_or_url.startswith("https://"):
        return name_or_url
    return f"https://container.googleapis.com/v1/{name_or_url}"


def ensure_cluster(project_id: str, region: str, cluster_name: str, token: str, create_cluster: bool) -> dict[str, Any]:
    probe = google_request("GET", cluster_url(project_id, region, cluster_name), token)
    if probe["status"] == 200:
        return {"status": "exists", "cluster": probe.get("parsed", {}), "http_status": 200}
    if not create_cluster:
        return {"status": "missing", "cluster": {}, "http_status": probe["status"]}
    create = google_request(
        "POST",
        clusters_url(project_id, region),
        token,
        body={
            "cluster": {
                "name": cluster_name,
                "location": region,
                "autopilot": {"enabled": True},
                "releaseChannel": {"channel": "REGULAR"},
                "resourceLabels": {"phase": "v32omega", "managed_by": "codex"},
            }
        },
        timeout=120,
    )
    return {
        "status": "creating" if create["status"] in {200, 201} else "blocked",
        "operation": create.get("parsed", {}),
        "http_status": create["status"],
        "error": create.get("parsed", {}),
    }


def poll_operation(name: str, token: str, *, timeout_seconds: int = 1800, sleep_seconds: int = 20) -> dict[str, Any]:
    deadline = time.time() + timeout_seconds
    last: dict[str, Any] = {}
    while time.time() < deadline:
        last = google_request("GET", operation_url(name), token, timeout=90)
        parsed = last.get("parsed", {})
        status = str(parsed.get("status", ""))
        if last["status"] == 200 and status == "DONE":
            return last
        time.sleep(sleep_seconds)
    return last


def kubectl_json(kubectl_path: str, kubeconfig: Path, args: list[str], timeout: int = 120) -> dict[str, Any]:
    result = run_cmd([kubectl_path, "--kubeconfig", str(kubeconfig), *args], timeout=timeout)
    parsed: Any = {}
    if result.stdout.strip():
        try:
            parsed = json.loads(result.stdout)
        except json.JSONDecodeError:
            parsed = {"raw_stdout": result.stdout.strip()}
    return {
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "parsed": parsed,
    }


def write_outputs(payload: dict[str, Any]) -> None:
    write_json(OUTPUT_JSON, payload)
    lines = [
        "# V32 GKE Bootstrap Proof",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Proof state: `{payload['proof_state']}`",
        f"- Cluster: `{payload.get('cluster_name', '') or 'unknown'}`",
        f"- Region: `{payload.get('region', '') or 'unknown'}`",
        f"- Primary identity: `{payload.get('primary_identity', '') or 'unknown'}`",
        f"- Gcloud CLI state: `{payload.get('gcloud_cli_state', 'unknown')}`",
        f"- Kubectl path: `{payload.get('kubectl_client_path', '') or 'missing'}`",
        "",
        "## Steps",
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
    parser = argparse.ArgumentParser(description="Create and validate the bounded V32 GKE cluster.")
    parser.add_argument("--bundle", default=str(DEFAULT_GCP_KEY_BUNDLE))
    parser.add_argument("--project-id", default=PROJECT_ID)
    parser.add_argument("--region", default=PRIMARY_REGION)
    parser.add_argument("--cluster-name", default=PRIMARY_CLUSTER)
    parser.add_argument("--namespace", default=PRIMARY_NAMESPACE)
    parser.add_argument("--create-cluster", action="store_true")
    args = parser.parse_args()

    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": "v32_omega",
        "overall_status": "WARN",
        "proof_state": "pending",
        "project_id": args.project_id,
        "region": args.region,
        "cluster_name": args.cluster_name,
        "namespace": args.namespace,
        "completed_steps": [],
        "blockers": [],
    }

    bundle = load_gcp_service_accounts(Path(args.bundle))
    records = {row["alias"]: row for row in bundle["records"]}
    primary = records.get("compute_default") or records.get("app_engine_default")
    if primary is None:
        payload["proof_state"] = "missing_primary_service_account"
        payload["blockers"].append("No primary GCP bootstrap identity was available.")
        write_outputs(payload)
        return 1

    minted = mint_access_token(primary["info"])
    token = minted["token"]
    payload["primary_identity"] = mask_email(primary["client_email"])
    payload["completed_steps"].append("mint_primary_token")

    inventory = google_request("GET", clusters_url(args.project_id, args.region), token)
    payload["cluster_inventory_status"] = inventory["status"]
    if inventory["status"] == 200:
        payload["completed_steps"].append("cluster_inventory")
        payload["gke_cluster_inventory"] = [row.get("name", "") for row in inventory.get("parsed", {}).get("clusters", [])]
    else:
        payload["proof_state"] = "inventory_blocked"
        payload["blockers"].append(f"GKE regional cluster inventory failed with HTTP {inventory['status']}.")
        write_outputs(payload)
        return 1

    cluster_state = ensure_cluster(args.project_id, args.region, args.cluster_name, token, args.create_cluster)
    payload["cluster_bootstrap"] = cluster_state
    if cluster_state["status"] == "blocked":
        payload["proof_state"] = "cluster_create_blocked"
        payload["blockers"].append(f"GKE cluster creation failed with HTTP {cluster_state['http_status']}.")
        write_outputs(payload)
        return 1
    if cluster_state["status"] == "creating":
        payload["completed_steps"].append("cluster_create_requested")
        operation_name = str(cluster_state["operation"].get("selfLink") or cluster_state["operation"].get("name", ""))
        if not operation_name:
            payload["proof_state"] = "cluster_create_operation_missing"
            payload["blockers"].append("Cluster create call returned without an operation name.")
            write_outputs(payload)
            return 1
        operation = poll_operation(operation_name, token)
        payload["operation_result"] = operation
        if operation.get("status") != 200 or str(operation.get("parsed", {}).get("status", "")) != "DONE":
            payload["proof_state"] = "cluster_create_timeout"
            payload["blockers"].append("Cluster creation did not reach DONE within the bounded polling window.")
            write_outputs(payload)
            return 1
        payload["completed_steps"].append("cluster_create_completed")
    else:
        payload["completed_steps"].append("cluster_exists")

    cluster_probe = google_request("GET", cluster_url(args.project_id, args.region, args.cluster_name), token)
    payload["cluster_probe_status"] = cluster_probe["status"]
    cluster = cluster_probe.get("parsed", {}) if cluster_probe["status"] == 200 else {}
    payload["cluster_details"] = {
        "status": cluster.get("status", ""),
        "endpoint": cluster.get("endpoint", ""),
        "release_channel": cluster.get("releaseChannel", {}).get("channel", ""),
        "autopilot_enabled": bool(cluster.get("autopilot", {}).get("enabled")),
        "location": cluster.get("location", ""),
    }
    if cluster_probe["status"] != 200 or str(cluster.get("status", "")) not in {"RUNNING", "RECONCILING"}:
        payload["proof_state"] = "cluster_not_ready"
        payload["blockers"].append("Cluster did not report a ready control plane after bootstrap.")
        write_outputs(payload)
        return 1
    payload["completed_steps"].append("cluster_readback")

    wsl = wsl_probe()
    payload["wsl_probe"] = wsl
    payload["gcloud_cli_state"] = (
        "wsl_shell_reachable_gcloud_not_yet_installed"
        if wsl["readiness"] == "ubuntu_shell_ready"
        else "blocked_wsl_launch_timeout"
        if wsl["readiness"] == "ubuntu_launch_timeout"
        else "blocked_wsl_launch_failed"
    )
    kubectl_path = windows_kubectl()
    payload["kubectl_client_path"] = kubectl_path
    if not kubectl_path:
        payload["proof_state"] = "kubectl_missing"
        payload["blockers"].append("Windows kubectl fallback is not available.")
        write_outputs(payload)
        return 1
    payload["completed_steps"].append("kubectl_client_detected")

    ca_data = str(cluster.get("masterAuth", {}).get("clusterCaCertificate", ""))
    endpoint = str(cluster.get("endpoint", ""))
    if not ca_data or not endpoint:
        payload["proof_state"] = "cluster_auth_material_missing"
        payload["blockers"].append("Cluster endpoint or CA bundle was missing from the readback payload.")
        write_outputs(payload)
        return 1

    kubeconfig = temp_kubeconfig(endpoint, ca_data, token, namespace=args.namespace)
    payload["kubeconfig_path"] = str(kubeconfig)

    nodes = kubectl_json(kubectl_path, kubeconfig, ["get", "nodes", "-o", "json"], timeout=240)
    pods = kubectl_json(kubectl_path, kubeconfig, ["get", "pods", "-A", "-o", "json"], timeout=240)
    payload["kubectl_nodes"] = {
        "returncode": nodes["returncode"],
        "item_count": len(nodes.get("parsed", {}).get("items", [])) if isinstance(nodes.get("parsed"), dict) else None,
        "stderr": nodes["stderr"],
    }
    payload["kubectl_pods"] = {
        "returncode": pods["returncode"],
        "item_count": len(pods.get("parsed", {}).get("items", [])) if isinstance(pods.get("parsed"), dict) else None,
        "stderr": pods["stderr"],
    }
    if nodes["returncode"] != 0 or pods["returncode"] != 0:
        payload["proof_state"] = "kubectl_validation_blocked"
        payload["blockers"].append("Windows kubectl fallback could not read nodes and pods from the cluster.")
        write_outputs(payload)
        return 1
    payload["completed_steps"].append("kubectl_cluster_reads")

    namespace_probe = run_cmd(
        [kubectl_path, "--kubeconfig", str(kubeconfig), "get", "namespace", args.namespace, "-o", "json"],
        timeout=120,
    )
    if namespace_probe.returncode != 0:
        namespace_create = run_cmd(
            [kubectl_path, "--kubeconfig", str(kubeconfig), "create", "namespace", args.namespace],
            timeout=120,
        )
        payload["namespace_create"] = {
            "returncode": namespace_create.returncode,
            "stdout": namespace_create.stdout.strip(),
            "stderr": namespace_create.stderr.strip(),
        }
        if namespace_create.returncode != 0:
            payload["proof_state"] = "namespace_create_blocked"
            payload["blockers"].append("Cluster reads succeeded, but namespace creation did not.")
            write_outputs(payload)
            return 1
    payload["completed_steps"].append("namespace_ready")

    configmap_yaml = "\n".join(
        [
            "apiVersion: v1",
            "kind: ConfigMap",
            "metadata:",
            "  name: v32-omega-smoke",
            f"  namespace: {args.namespace}",
            "data:",
            f"  generated_utc: \"{now_iso()}\"",
            "  lane: \"v32-omega\"",
            "",
        ]
    )
    configmap_path = temp_file("v32-omega-smoke-", ".yaml", configmap_yaml)
    apply = run_cmd(
        [kubectl_path, "--kubeconfig", str(kubeconfig), "apply", "-f", str(configmap_path)],
        timeout=120,
    )
    verify = kubectl_json(
        kubectl_path,
        kubeconfig,
        ["get", "configmap", "v32-omega-smoke", "-n", args.namespace, "-o", "json"],
        timeout=120,
    )
    payload["configmap_apply"] = {
        "returncode": apply.returncode,
        "stdout": apply.stdout.strip(),
        "stderr": apply.stderr.strip(),
    }
    payload["configmap_verify"] = {
        "returncode": verify["returncode"],
        "stderr": verify["stderr"],
        "name": verify.get("parsed", {}).get("metadata", {}).get("name", "") if isinstance(verify.get("parsed"), dict) else "",
    }
    if apply.returncode != 0 or verify["returncode"] != 0:
        payload["proof_state"] = "smoke_workload_blocked"
        payload["blockers"].append("Cluster namespace exists, but the smoke ConfigMap did not verify cleanly.")
        write_outputs(payload)
        return 1
    payload["completed_steps"].append("smoke_configmap_verified")

    payload["overall_status"] = "PASS"
    payload["proof_state"] = "cluster_bootstrap_validated_windows_kubectl_fallback"
    payload["gke_cluster_state"] = "cluster_ready"
    write_outputs(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
