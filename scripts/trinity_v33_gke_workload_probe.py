#!/usr/bin/env python3
"""Run a bounded V33 workload proof on the existing GKE Autopilot cluster."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

from trinity_v32_runtime_common import (
    DEFAULT_GCP_KEY_BUNDLE,
    PRIMARY_CLUSTER,
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
)

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v33-gke-workload-proof-v1.json"
OUTPUT_MD = ROOT / "docs" / "trinity-live-traces" / "v33-gke-workload-proof-v1.md"
DEFAULT_NAMESPACE = "v33-omega"
DEFAULT_JOB_NAME = "v33-omega-smoke"
DEFAULT_DEPLOYMENT_NAME = "v33-omega-probe"


def cluster_url(project_id: str, region: str, cluster_name: str) -> str:
    return f"https://container.googleapis.com/v1/projects/{project_id}/locations/{region}/clusters/{cluster_name}"


def kubectl_json(kubectl_path: str, kubeconfig: Path, args: list[str], timeout: int = 180) -> dict[str, Any]:
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


def kubectl_text(kubectl_path: str, kubeconfig: Path, args: list[str], timeout: int = 180) -> dict[str, Any]:
    result = run_cmd([kubectl_path, "--kubeconfig", str(kubeconfig), *args], timeout=timeout)
    return {
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def ensure_namespace(kubectl_path: str, kubeconfig: Path, namespace: str) -> dict[str, Any]:
    existing = kubectl_text(kubectl_path, kubeconfig, ["get", "namespace", namespace, "-o", "name"], timeout=90)
    if existing["returncode"] == 0:
        return {"status": "exists", **existing}
    created = kubectl_text(kubectl_path, kubeconfig, ["create", "namespace", namespace], timeout=90)
    if created["returncode"] == 0:
        return {"status": "created", **created}
    return {"status": "blocked", **created}


def write_outputs(payload: dict[str, Any]) -> None:
    write_json(OUTPUT_JSON, payload)
    lines = [
        "# V33 GKE Workload Proof",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Proof state: `{payload['proof_state']}`",
        f"- Cluster: `{payload.get('cluster_name', '') or 'unknown'}`",
        f"- Namespace: `{payload.get('namespace', '') or 'unknown'}`",
        f"- Primary identity: `{payload.get('primary_identity', '') or 'unknown'}`",
        f"- GKE workload state: `{payload.get('gke_workload_state', 'unknown')}`",
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
    parser = argparse.ArgumentParser(description="Run a bounded V33 workload on the existing GKE cluster.")
    parser.add_argument("--bundle", default=str(DEFAULT_GCP_KEY_BUNDLE))
    parser.add_argument("--project-id", default=PROJECT_ID)
    parser.add_argument("--region", default=PRIMARY_REGION)
    parser.add_argument("--cluster-name", default=PRIMARY_CLUSTER)
    parser.add_argument("--namespace", default=DEFAULT_NAMESPACE)
    parser.add_argument("--job-name", default=DEFAULT_JOB_NAME)
    parser.add_argument("--deployment-name", default=DEFAULT_DEPLOYMENT_NAME)
    parser.add_argument("--skip-deployment", action="store_true")
    args = parser.parse_args()

    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": "v33_omega",
        "overall_status": "WARN",
        "proof_state": "pending",
        "gke_workload_state": "pending",
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
        payload["gke_workload_state"] = "blocked_missing_identity"
        payload["blockers"].append("No primary GCP service account was available for the V33 workload probe.")
        write_outputs(payload)
        return 1

    minted = mint_access_token(primary["info"])
    token = minted["token"]
    payload["primary_identity"] = mask_email(primary["client_email"])
    payload["completed_steps"].append("mint_primary_token")

    cluster_probe = google_request("GET", cluster_url(args.project_id, args.region, args.cluster_name), token, timeout=90)
    payload["cluster_probe_status"] = cluster_probe["status"]
    cluster = cluster_probe.get("parsed", {}) if cluster_probe["status"] == 200 else {}
    if cluster_probe["status"] != 200:
        payload["proof_state"] = "cluster_readback_blocked"
        payload["gke_workload_state"] = "blocked_cluster_readback"
        payload["blockers"].append(f"Cluster readback failed with HTTP {cluster_probe['status']}.")
        write_outputs(payload)
        return 1
    payload["completed_steps"].append("cluster_readback")

    cluster_status = str(cluster.get("status", ""))
    if cluster_status not in {"RUNNING", "RECONCILING"}:
        payload["proof_state"] = "cluster_not_ready"
        payload["gke_workload_state"] = "blocked_cluster_not_ready"
        payload["blockers"].append(f"Cluster status was `{cluster_status or 'unknown'}` instead of `RUNNING` or `RECONCILING`.")
        write_outputs(payload)
        return 1

    kubectl_path = windows_kubectl()
    payload["kubectl_client_path"] = kubectl_path
    if not kubectl_path:
        payload["proof_state"] = "kubectl_missing"
        payload["gke_workload_state"] = "blocked_kubectl_missing"
        payload["blockers"].append("Windows kubectl is not available for the bounded GKE proof.")
        write_outputs(payload)
        return 1
    payload["completed_steps"].append("kubectl_detected")

    ca_data = str(cluster.get("masterAuth", {}).get("clusterCaCertificate", ""))
    endpoint = str(cluster.get("endpoint", ""))
    if not ca_data or not endpoint:
        payload["proof_state"] = "cluster_auth_material_missing"
        payload["gke_workload_state"] = "blocked_cluster_auth_material_missing"
        payload["blockers"].append("Cluster endpoint or CA bundle was missing from the cluster readback payload.")
        write_outputs(payload)
        return 1

    kubeconfig = temp_kubeconfig(endpoint, ca_data, token, namespace=args.namespace)
    payload["kubeconfig_path"] = str(kubeconfig)

    namespace_result = ensure_namespace(kubectl_path, kubeconfig, args.namespace)
    payload["namespace_result"] = namespace_result
    if namespace_result["status"] == "blocked":
        payload["proof_state"] = "namespace_blocked"
        payload["gke_workload_state"] = "blocked_namespace"
        payload["blockers"].append("The V33 namespace could not be read or created.")
        write_outputs(payload)
        return 1
    payload["completed_steps"].append("namespace_ready")

    marker = f"V33_GKE_WORKLOAD_OK_{int(time.time())}"
    job_yaml = "\n".join(
        [
            "apiVersion: batch/v1",
            "kind: Job",
            "metadata:",
            f"  name: {args.job_name}",
            f"  namespace: {args.namespace}",
            "spec:",
            "  ttlSecondsAfterFinished: 600",
            "  backoffLimit: 0",
            "  template:",
            "    spec:",
            "      restartPolicy: Never",
            "      containers:",
            "      - name: smoke",
            "        image: busybox:1.36",
            "        terminationMessagePolicy: File",
            "        command:",
            "        - sh",
            "        - -lc",
            f"        - echo {marker} >/dev/termination-log; echo {marker}; sleep 2; echo V33_GKE_JOB_DONE",
            "        resources:",
            "          requests:",
            "            cpu: 250m",
            "            memory: 256Mi",
            "          limits:",
            "            cpu: 250m",
            "            memory: 256Mi",
            "",
        ]
    )
    job_manifest = temp_file("v33-gke-job-", ".yaml", job_yaml)
    payload["job_manifest"] = str(job_manifest)

    run_cmd([kubectl_path, "--kubeconfig", str(kubeconfig), "delete", "job", args.job_name, "-n", args.namespace, "--ignore-not-found=true"], timeout=90)
    apply_job = kubectl_text(kubectl_path, kubeconfig, ["apply", "-f", str(job_manifest)], timeout=120)
    payload["job_apply"] = apply_job
    if apply_job["returncode"] != 0:
        payload["proof_state"] = "job_apply_blocked"
        payload["gke_workload_state"] = "blocked_job_apply"
        payload["blockers"].append("The bounded V33 smoke job could not be applied to the cluster.")
        write_outputs(payload)
        return 1
    payload["completed_steps"].append("job_applied")

    job_wait = kubectl_text(
        kubectl_path,
        kubeconfig,
        ["wait", "--for=condition=complete", f"job/{args.job_name}", "-n", args.namespace, "--timeout=600s"],
        timeout=720,
    )
    payload["job_wait"] = job_wait
    if job_wait["returncode"] != 0:
        payload["proof_state"] = "job_completion_blocked"
        payload["gke_workload_state"] = "blocked_job_completion"
        payload["blockers"].append("The bounded V33 smoke job did not reach completion within the wait window.")
        write_outputs(payload)
        return 1
    payload["completed_steps"].append("job_completed")

    job_pods = kubectl_json(
        kubectl_path,
        kubeconfig,
        ["get", "pods", "-n", args.namespace, "-l", f"job-name={args.job_name}", "-o", "json"],
        timeout=180,
    )
    logs = kubectl_text(kubectl_path, kubeconfig, ["logs", f"job/{args.job_name}", "-n", args.namespace], timeout=180)
    pod_items = job_pods.get("parsed", {}).get("items", []) if isinstance(job_pods.get("parsed"), dict) else []
    pod_name = ""
    termination_message = ""
    terminated_reason = ""
    terminated_exit_code: int | None = None
    if pod_items:
        pod_name = str(pod_items[0].get("metadata", {}).get("name", ""))
        statuses = pod_items[0].get("status", {}).get("containerStatuses", [])
        if statuses:
            terminated = statuses[0].get("state", {}).get("terminated", {})
            termination_message = str(terminated.get("message", ""))
            terminated_reason = str(terminated.get("reason", ""))
            if "exitCode" in terminated:
                try:
                    terminated_exit_code = int(terminated.get("exitCode"))
                except Exception:
                    terminated_exit_code = None
    payload["job_pods"] = {
        "returncode": job_pods["returncode"],
        "count": len(pod_items),
        "stderr": job_pods["stderr"],
        "pod_name": pod_name,
        "termination_message": termination_message,
        "terminated_reason": terminated_reason,
        "terminated_exit_code": terminated_exit_code,
    }
    payload["job_logs"] = logs
    log_marker_verified = logs["returncode"] == 0 and marker in logs["stdout"]
    termination_marker_verified = marker in termination_message and terminated_reason == "Completed" and terminated_exit_code == 0
    payload["job_log_marker_verified"] = log_marker_verified
    payload["job_termination_marker_verified"] = termination_marker_verified
    if job_pods["returncode"] != 0 or not (log_marker_verified or termination_marker_verified):
        payload["proof_state"] = "job_log_marker_missing"
        payload["gke_workload_state"] = "blocked_job_logs"
        payload["blockers"].append("The smoke job completed, but neither pod logs nor the pod termination message exposed the expected deterministic marker.")
        write_outputs(payload)
        return 1
    payload["completed_steps"].append("job_logs_verified")

    payload["deployment_attempted"] = not args.skip_deployment
    if not args.skip_deployment:
        deployment_yaml = "\n".join(
            [
                "apiVersion: apps/v1",
                "kind: Deployment",
                "metadata:",
                f"  name: {args.deployment_name}",
                f"  namespace: {args.namespace}",
                "spec:",
                "  replicas: 2",
                "  selector:",
                "    matchLabels:",
                f"      app: {args.deployment_name}",
                "  template:",
                "    metadata:",
                "      labels:",
                f"        app: {args.deployment_name}",
                "    spec:",
                "      containers:",
                "      - name: pause",
                "        image: registry.k8s.io/pause:3.9",
                "        resources:",
                "          requests:",
                "            cpu: 250m",
                "            memory: 256Mi",
                "          limits:",
                "            cpu: 250m",
                "            memory: 256Mi",
                "",
            ]
        )
        deployment_manifest = temp_file("v33-gke-deploy-", ".yaml", deployment_yaml)
        payload["deployment_manifest"] = str(deployment_manifest)
        run_cmd([kubectl_path, "--kubeconfig", str(kubeconfig), "delete", "deployment", args.deployment_name, "-n", args.namespace, "--ignore-not-found=true"], timeout=90)
        deploy_apply = kubectl_text(kubectl_path, kubeconfig, ["apply", "-f", str(deployment_manifest)], timeout=120)
        deploy_rollout = kubectl_text(
            kubectl_path,
            kubeconfig,
            ["rollout", "status", f"deployment/{args.deployment_name}", "-n", args.namespace, "--timeout=300s"],
            timeout=360,
        )
        deploy_read = kubectl_json(
            kubectl_path,
            kubeconfig,
            ["get", "deployment", args.deployment_name, "-n", args.namespace, "-o", "json"],
            timeout=180,
        )
        payload["deployment_apply"] = deploy_apply
        payload["deployment_rollout"] = deploy_rollout
        payload["deployment_read"] = {
            "returncode": deploy_read["returncode"],
            "stderr": deploy_read["stderr"],
            "replicas": deploy_read.get("parsed", {}).get("status", {}).get("replicas") if isinstance(deploy_read.get("parsed"), dict) else None,
            "ready_replicas": deploy_read.get("parsed", {}).get("status", {}).get("readyReplicas") if isinstance(deploy_read.get("parsed"), dict) else None,
        }
        if deploy_apply["returncode"] == 0 and deploy_rollout["returncode"] == 0 and deploy_read["returncode"] == 0:
            payload["completed_steps"].append("optional_deployment_ready")
            payload["optional_deployment_state"] = "ready"
        else:
            payload["optional_deployment_state"] = "warn"
            payload.setdefault("notes", []).append("The optional 2-replica deployment did not fully verify; the smoke job remains the gating proof.")

    cleanup_results = {
        "job_delete": kubectl_text(kubectl_path, kubeconfig, ["delete", "job", args.job_name, "-n", args.namespace, "--ignore-not-found=true"], timeout=120),
    }
    if not args.skip_deployment:
        cleanup_results["deployment_delete"] = kubectl_text(
            kubectl_path,
            kubeconfig,
            ["delete", "deployment", args.deployment_name, "-n", args.namespace, "--ignore-not-found=true"],
            timeout=120,
        )
    payload["cleanup"] = cleanup_results
    payload["completed_steps"].append("ephemeral_cleanup_attempted")

    payload["overall_status"] = "PASS"
    payload["proof_state"] = "bounded_job_verified"
    payload["gke_workload_state"] = "job_verified"
    if payload.get("optional_deployment_state") == "ready":
        payload["proof_state"] = "bounded_job_and_optional_deployment_verified"
        payload["gke_workload_state"] = "job_and_optional_deployment_verified"
    write_outputs(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
