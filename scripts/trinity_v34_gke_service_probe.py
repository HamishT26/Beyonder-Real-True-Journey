#!/usr/bin/env python3
"""Run a bounded V34 GKE service proof on the existing Autopilot cluster."""

from __future__ import annotations

import argparse
import json
import subprocess
import time
import urllib.request
from pathlib import Path
from typing import Any

from trinity_v32_runtime_common import PRIMARY_CLUSTER
from trinity_v34_cloud_common import (
    PHASE,
    PRIMARY_REGION,
    PROJECT_ID,
    ROOT,
    ensure_namespace,
    google_request,
    kubectl_json,
    kubectl_text,
    load_primary_service_account,
    now_iso,
    run_cmd,
    temp_file,
    temp_kubeconfig,
    windows_kubectl,
    write_json,
    write_text,
)

OUTPUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v34-gke-service-proof-v1.json"
OUTPUT_MD = ROOT / "docs" / "trinity-live-traces" / "v34-gke-service-proof-v1.md"
DEFAULT_NAMESPACE = "v34-omega"
DEFAULT_DEPLOYMENT_NAME = "v34-omega-web"
DEFAULT_SERVICE_NAME = "v34-omega-web"
PORT_FORWARD_PORT = 18080


def cluster_url(project_id: str, region: str, cluster_name: str) -> str:
    return f"https://container.googleapis.com/v1/projects/{project_id}/locations/{region}/clusters/{cluster_name}"


def write_outputs(payload: dict[str, Any]) -> None:
    write_json(OUTPUT_JSON, payload)
    lines = [
        "# V34 GKE Service Proof",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Proof state: `{payload['proof_state']}`",
        f"- GKE service state: `{payload.get('gke_service_state', 'unknown')}`",
        f"- Cluster: `{payload.get('cluster_name', '') or 'unknown'}`",
        f"- Namespace: `{payload.get('namespace', '') or 'unknown'}`",
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


def http_fetch(url: str, timeout: int = 10) -> dict[str, Any]:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            body = response.read().decode("utf-8", errors="replace")
            return {"status": response.status, "body": body[:2000]}
    except Exception as exc:
        return {"status": 0, "body": "", "error": str(exc)}


def wait_for_port_forward(
    kubectl_path: str,
    kubeconfig: Path,
    namespace: str,
    service_name: str,
) -> tuple[subprocess.Popen[str] | None, dict[str, Any]]:
    process = subprocess.Popen(
        [
            kubectl_path,
            "--kubeconfig",
            str(kubeconfig),
            "port-forward",
            f"svc/{service_name}",
            f"{PORT_FORWARD_PORT}:80",
            "-n",
            namespace,
        ],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    for _ in range(20):
        if process.poll() is not None:
            stdout, stderr = process.communicate(timeout=5)
            return None, {"returncode": process.returncode, "stdout": stdout.strip(), "stderr": stderr.strip()}
        time.sleep(1)
        probe = http_fetch(f"http://127.0.0.1:{PORT_FORWARD_PORT}/", timeout=2)
        if probe.get("status") == 200:
            return process, probe
    stdout = ""
    stderr = ""
    if process.poll() is not None:
        stdout, stderr = process.communicate(timeout=5)
    else:
        process.terminate()
        try:
            stdout, stderr = process.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate(timeout=10)
    return None, {"returncode": process.returncode, "stdout": stdout.strip(), "stderr": stderr.strip()}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the bounded V34 GKE service proof.")
    parser.add_argument("--bundle", default=str(Path.home() / "GCP service account keys.txt"))
    parser.add_argument("--project-id", default=PROJECT_ID)
    parser.add_argument("--region", default=PRIMARY_REGION)
    parser.add_argument("--cluster-name", default=PRIMARY_CLUSTER)
    parser.add_argument("--namespace", default=DEFAULT_NAMESPACE)
    parser.add_argument("--deployment-name", default=DEFAULT_DEPLOYMENT_NAME)
    parser.add_argument("--service-name", default=DEFAULT_SERVICE_NAME)
    args = parser.parse_args()

    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "overall_status": "WARN",
        "proof_state": "pending",
        "gke_service_state": "pending",
        "project_id": args.project_id,
        "region": args.region,
        "cluster_name": args.cluster_name,
        "namespace": args.namespace,
        "completed_steps": [],
        "blockers": [],
    }

    try:
        _bundle, primary, minted = load_primary_service_account(Path(args.bundle))
    except Exception as exc:
        payload["proof_state"] = "missing_primary_service_account"
        payload["gke_service_state"] = "blocked_missing_identity"
        payload["blockers"].append(str(exc))
        write_outputs(payload)
        return 1

    token = minted["token"]
    payload["primary_identity"] = primary["client_email"]
    payload["completed_steps"].append("mint_primary_token")

    cluster_probe = google_request("GET", cluster_url(args.project_id, args.region, args.cluster_name), token, timeout=90)
    payload["cluster_probe_status"] = cluster_probe["status"]
    cluster = cluster_probe.get("parsed", {}) if cluster_probe["status"] == 200 else {}
    if cluster_probe["status"] != 200:
        payload["proof_state"] = "cluster_readback_blocked"
        payload["gke_service_state"] = "blocked_cluster_readback"
        payload["blockers"].append(f"Cluster readback failed with HTTP {cluster_probe['status']}.")
        write_outputs(payload)
        return 1
    payload["completed_steps"].append("cluster_readback")

    cluster_status = str(cluster.get("status", ""))
    if cluster_status not in {"RUNNING", "RECONCILING"}:
        payload["proof_state"] = "cluster_not_ready"
        payload["gke_service_state"] = "blocked_cluster_not_ready"
        payload["blockers"].append(f"Cluster status was `{cluster_status or 'unknown'}` instead of `RUNNING` or `RECONCILING`.")
        write_outputs(payload)
        return 1

    kubectl_path = windows_kubectl()
    payload["kubectl_client_path"] = kubectl_path
    if not kubectl_path:
        payload["proof_state"] = "kubectl_missing"
        payload["gke_service_state"] = "blocked_kubectl_missing"
        payload["blockers"].append("Windows kubectl is not available for the bounded GKE proof.")
        write_outputs(payload)
        return 1
    payload["completed_steps"].append("kubectl_detected")

    ca_data = str(cluster.get("masterAuth", {}).get("clusterCaCertificate", ""))
    endpoint = str(cluster.get("endpoint", ""))
    if not ca_data or not endpoint:
        payload["proof_state"] = "cluster_auth_material_missing"
        payload["gke_service_state"] = "blocked_cluster_auth_material_missing"
        payload["blockers"].append("Cluster endpoint or CA bundle was missing from the cluster readback payload.")
        write_outputs(payload)
        return 1

    kubeconfig = temp_kubeconfig(endpoint, ca_data, token, namespace=args.namespace)
    payload["kubeconfig_path"] = str(kubeconfig)

    namespace_result = ensure_namespace(kubectl_path, kubeconfig, args.namespace)
    payload["namespace_result"] = namespace_result
    if namespace_result["status"] == "blocked":
        payload["proof_state"] = "namespace_blocked"
        payload["gke_service_state"] = "blocked_namespace"
        payload["blockers"].append("The V34 namespace could not be read or created.")
        write_outputs(payload)
        return 1
    payload["completed_steps"].append("namespace_ready")

    manifest = "\n".join(
        [
            "apiVersion: apps/v1",
            "kind: Deployment",
            "metadata:",
            f"  name: {args.deployment_name}",
            f"  namespace: {args.namespace}",
            "spec:",
            "  replicas: 1",
            "  selector:",
            "    matchLabels:",
            f"      app: {args.deployment_name}",
            "  template:",
            "    metadata:",
            "      labels:",
            f"        app: {args.deployment_name}",
            "    spec:",
            "      containers:",
            "      - name: web",
            "        image: nginx:1.27-alpine",
            "        ports:",
            "        - containerPort: 80",
            "        readinessProbe:",
            "          httpGet:",
            "            path: /",
            "            port: 80",
            "          initialDelaySeconds: 3",
            "          periodSeconds: 5",
            "        livenessProbe:",
            "          httpGet:",
            "            path: /",
            "            port: 80",
            "          initialDelaySeconds: 10",
            "          periodSeconds: 10",
            "        resources:",
            "          requests:",
            "            cpu: 250m",
            "            memory: 256Mi",
            "          limits:",
            "            cpu: 250m",
            "            memory: 256Mi",
            "---",
            "apiVersion: v1",
            "kind: Service",
            "metadata:",
            f"  name: {args.service_name}",
            f"  namespace: {args.namespace}",
            "spec:",
            "  selector:",
            f"    app: {args.deployment_name}",
            "  ports:",
            "  - name: http",
            "    port: 80",
            "    targetPort: 80",
            "",
        ]
    )
    manifest_path = temp_file("v34-gke-service-", ".yaml", manifest)
    payload["manifest_path"] = str(manifest_path)

    run_cmd([kubectl_path, "--kubeconfig", str(kubeconfig), "delete", "deployment", args.deployment_name, "-n", args.namespace, "--ignore-not-found=true"], timeout=120)
    run_cmd([kubectl_path, "--kubeconfig", str(kubeconfig), "delete", "service", args.service_name, "-n", args.namespace, "--ignore-not-found=true"], timeout=120)

    apply_result = kubectl_text(kubectl_path, kubeconfig, ["apply", "-f", str(manifest_path)], timeout=180)
    payload["apply_result"] = apply_result
    if apply_result["returncode"] != 0:
        payload["proof_state"] = "service_apply_blocked"
        payload["gke_service_state"] = "blocked_service_apply"
        payload["blockers"].append("The bounded V34 deployment/service manifest could not be applied.")
        write_outputs(payload)
        return 1
    payload["completed_steps"].append("service_manifest_applied")

    rollout = kubectl_text(
        kubectl_path,
        kubeconfig,
        ["rollout", "status", f"deployment/{args.deployment_name}", "-n", args.namespace, "--timeout=600s"],
        timeout=720,
    )
    payload["deployment_rollout"] = rollout
    if rollout["returncode"] != 0:
        payload["proof_state"] = "deployment_rollout_blocked"
        payload["gke_service_state"] = "blocked_rollout"
        payload["blockers"].append("The bounded V34 deployment did not roll out successfully.")
        write_outputs(payload)
        return 1
    payload["completed_steps"].append("deployment_ready")

    deployment_read = kubectl_json(
        kubectl_path,
        kubeconfig,
        ["get", "deployment", args.deployment_name, "-n", args.namespace, "-o", "json"],
        timeout=180,
    )
    payload["deployment_read"] = {
        "returncode": deployment_read["returncode"],
        "stderr": deployment_read["stderr"],
        "replicas": deployment_read.get("parsed", {}).get("status", {}).get("replicas", 0) if isinstance(deployment_read.get("parsed"), dict) else 0,
        "ready_replicas": deployment_read.get("parsed", {}).get("status", {}).get("readyReplicas", 0) if isinstance(deployment_read.get("parsed"), dict) else 0,
    }
    if deployment_read["returncode"] != 0 or payload["deployment_read"]["ready_replicas"] < 1:
        payload["proof_state"] = "deployment_not_ready"
        payload["gke_service_state"] = "blocked_ready_replicas"
        payload["blockers"].append("The deployment did not expose a ready replica after rollout.")
        write_outputs(payload)
        return 1
    payload["completed_steps"].append("ready_replicas_verified")

    endpoints = kubectl_json(kubectl_path, kubeconfig, ["get", "endpoints", args.service_name, "-n", args.namespace, "-o", "json"], timeout=180)
    subsets = endpoints.get("parsed", {}).get("subsets", []) if isinstance(endpoints.get("parsed"), dict) else []
    addresses = 0
    for subset in subsets:
        if isinstance(subset, dict):
            addresses += len(subset.get("addresses", []))
    payload["endpoints_read"] = {
        "returncode": endpoints["returncode"],
        "stderr": endpoints["stderr"],
        "address_count": addresses,
    }
    if endpoints["returncode"] != 0 or addresses < 1:
        payload["proof_state"] = "service_endpoints_blocked"
        payload["gke_service_state"] = "blocked_service_endpoints"
        payload["blockers"].append("The Service did not expose a ready endpoint set.")
        write_outputs(payload)
        return 1
    payload["completed_steps"].append("service_endpoints_verified")

    port_forward_process, probe = wait_for_port_forward(kubectl_path, kubeconfig, args.namespace, args.service_name)
    payload["http_probe"] = probe
    if port_forward_process is None or probe.get("status") != 200 or "nginx" not in probe.get("body", "").lower():
        payload["proof_state"] = "service_http_probe_blocked"
        payload["gke_service_state"] = "blocked_http_probe"
        payload["blockers"].append("The port-forward HTTP probe did not return the expected nginx response.")
        write_outputs(payload)
        return 1
    payload["completed_steps"].append("service_http_probe_verified")

    if port_forward_process is not None:
        port_forward_process.terminate()
        try:
            stdout, stderr = port_forward_process.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            port_forward_process.kill()
            stdout, stderr = port_forward_process.communicate(timeout=10)
        payload["port_forward_cleanup"] = {
            "returncode": port_forward_process.returncode,
            "stdout": stdout.strip(),
            "stderr": stderr.strip(),
        }

    cleanup_deployment = kubectl_text(kubectl_path, kubeconfig, ["delete", "deployment", args.deployment_name, "-n", args.namespace, "--ignore-not-found=true"], timeout=180)
    cleanup_service = kubectl_text(kubectl_path, kubeconfig, ["delete", "service", args.service_name, "-n", args.namespace, "--ignore-not-found=true"], timeout=180)
    payload["cleanup"] = {"deployment_delete": cleanup_deployment, "service_delete": cleanup_service}
    payload["completed_steps"].append("service_cleanup_attempted")

    payload["overall_status"] = "PASS"
    payload["proof_state"] = "bounded_service_ready_verified"
    payload["gke_service_state"] = "service_ready_verified"
    write_outputs(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
