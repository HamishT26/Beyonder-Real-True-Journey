#!/usr/bin/env python3
"""Run the V42 curated API and telemetry automation wave."""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from trinity_v32_runtime_common import PROJECT_ID
from trinity_v36_cloud_common import (
    DEFAULT_REGIONAL_LOCATION,
    best_effort_error_message,
    ensure_service_enabled,
    load_primary_service_account,
)
from trinity_v38_fleet_anthos_probe import KUBECONFIG_PATH, kubectl_path
from trinity_v38_windows_operator_probe import build_gcloud_env, ensure_operator_lane
from trinity_v42_common import now_iso, read_json, safe_run, write_json, write_text

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v42-api-automation-wave-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v42-api-automation-wave-v1.md"
BUILD_CONFIG = ROOT / ".local-runtime" / "v42" / "cloudbuild-v42.yaml"
DEFAULT_CLOUD_RUN_SERVICE = "beyonder-v42-cloudrun-probe"
DEFAULT_MEMBERSHIP = "beyonder-v32-autopilot-dev"
DEFAULT_MEMBERSHIP_LOCATION = "australia-southeast1"
V42_MARKER = "V42_OMEGA_TELEMETRY_OK"

CURATED_SERVICES = (
    "logging.googleapis.com",
    "monitoring.googleapis.com",
    "cloudscheduler.googleapis.com",
    "pubsub.googleapis.com",
    "eventarc.googleapis.com",
    "workflows.googleapis.com",
)
SUPPORT_SERVICES = (
    "run.googleapis.com",
    "cloudbuild.googleapis.com",
    "dataplex.googleapis.com",
    "artifactregistry.googleapis.com",
    "serviceusage.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "compute.googleapis.com",
    "container.googleapis.com",
    "connectgateway.googleapis.com",
    "gkeconnect.googleapis.com",
    "gkehub.googleapis.com",
    "oslogin.googleapis.com",
    "aiplatform.googleapis.com",
    "bigtable.googleapis.com",
    "bigtableadmin.googleapis.com",
    "iam.googleapis.com",
    "iamcredentials.googleapis.com",
)
ALL_SERVICES = tuple(dict.fromkeys((*CURATED_SERVICES, *SUPPORT_SERVICES)))
OFFICIAL_SOURCES = {
    "cloud_run": "https://cloud.google.com/run/docs",
    "cloud_build": "https://cloud.google.com/build/docs/build-config-file-schema",
    "dataplex": "https://cloud.google.com/dataplex/docs",
}


def _json_from_stdout(stdout: str) -> Any:
    text = str(stdout or "").strip()
    if not text:
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {}


def _carry_forward_state(path: Path, key: str) -> dict[str, Any]:
    payload = read_json(path)
    return {
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "overall_status": str(payload.get("overall_status") or ""),
        key: str(payload.get(key) or ""),
    }


def _operator_env(bundle: str) -> tuple[dict[str, Any], str, dict[str, str]]:
    operator = ensure_operator_lane(bundle, bootstrap=True)
    gcloud_path = str(operator.get("gcloud_path") or "")
    env = build_gcloud_env()
    return operator, gcloud_path, env


def _service_inventory(project_id: str, bundle: str) -> dict[str, Any]:
    _records, primary, minted = load_primary_service_account(Path(bundle))
    token = minted["token"]
    results: list[dict[str, Any]] = []
    enabled: list[str] = []
    already_enabled: list[str] = []
    failed: list[dict[str, str]] = []
    skipped: list[dict[str, str]] = []
    for service_name in ALL_SERVICES:
        result = ensure_service_enabled(project_id, token, service_name)
        if result.get("enable_attempted") and result.get("final_state") != "ENABLED":
            for _ in range(6):
                time.sleep(5)
                result = ensure_service_enabled(project_id, token, service_name)
                if result.get("final_state") == "ENABLED":
                    break
        results.append(result)
        final_state = str(result.get("final_state") or "")
        initial_state = str(result.get("initial_state") or "")
        final_status = int(result.get("final_status") or 0)
        if final_status == 200 and final_state == "ENABLED":
            if initial_state == "ENABLED":
                already_enabled.append(service_name)
            else:
                enabled.append(service_name)
            continue
        failed.append(
            {
                "service_name": service_name,
                "reason": best_effort_error_message(result.get("raw_enable_response", {}), ""),
            }
        )
    return {
        "primary_identity": str(primary.get("client_email") or ""),
        "service_account_path": str(primary.get("runtime_path") or ""),
        "token_expiry_utc": str(minted.get("expiry_utc") or ""),
        "results": results,
        "enabled": enabled,
        "already_enabled": already_enabled,
        "skipped": skipped,
        "failed": failed,
    }


def _cloud_run_probe(gcloud_path: str, env: dict[str, str], *, project_id: str, regional_location: str, service_name: str) -> dict[str, Any]:
    deploy = safe_run(
        [
            gcloud_path,
            "run",
            "deploy",
            service_name,
            "--image",
            "us-docker.pkg.dev/cloudrun/container/hello",
            "--region",
            regional_location,
            "--project",
            project_id,
            "--allow-unauthenticated",
            "--min-instances",
            "0",
            "--max-instances",
            "1",
            "--port",
            "8080",
            "--labels",
            "phase=v42omega,marker=v42cloud",
            "--quiet",
            "--format=json",
        ],
        env=env,
        timeout=1800,
    )
    deploy_parsed = _json_from_stdout(deploy.stdout)
    describe = safe_run(
        [
            gcloud_path,
            "run",
            "services",
            "describe",
            service_name,
            "--region",
            regional_location,
            "--project",
            project_id,
            "--format=json",
        ],
        env=env,
        timeout=300,
    )
    describe_parsed = _json_from_stdout(describe.stdout)
    url = str(describe_parsed.get("status", {}).get("url") or describe_parsed.get("uri") or deploy_parsed.get("status", {}).get("url") or "").strip()
    http_probe: dict[str, Any] = {"url": url, "status_code": 0, "body_excerpt": "", "ok": False}
    if url:
        for _ in range(4):
            try:
                with urllib.request.urlopen(url, timeout=30) as response:
                    body = response.read().decode("utf-8", errors="replace")
                    http_probe = {
                        "url": url,
                        "status_code": response.status,
                        "body_excerpt": body[:600],
                        "ok": response.status == 200,
                    }
                    break
            except urllib.error.HTTPError as exc:
                body = exc.read().decode("utf-8", errors="replace")
                http_probe = {
                    "url": url,
                    "status_code": exc.code,
                    "body_excerpt": body[:600],
                    "ok": False,
                }
            except Exception as exc:  # noqa: BLE001
                http_probe = {"url": url, "status_code": 0, "body_excerpt": str(exc)[:600], "ok": False}
            time.sleep(5)
    labels = describe_parsed.get("metadata", {}).get("labels", {}) if isinstance(describe_parsed.get("metadata", {}), dict) else {}
    overall_ok = deploy.returncode == 0 and describe.returncode == 0 and bool(http_probe.get("ok"))
    return {
        "cloud_run_state": "minimal_workload_verified" if overall_ok else "deployment_blocked",
        "service_name": service_name,
        "deterministic_marker": labels.get("marker", ""),
        "deploy": {
            "returncode": deploy.returncode,
            "stdout_excerpt": deploy.stdout[-3000:],
            "stderr_excerpt": deploy.stderr[-2000:],
            "parsed": deploy_parsed,
        },
        "describe": {
            "returncode": describe.returncode,
            "stdout_excerpt": describe.stdout[-3000:],
            "stderr_excerpt": describe.stderr[-2000:],
            "parsed": describe_parsed,
        },
        "http_probe": http_probe,
    }


def _write_build_config(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(
            [
                "steps:",
                "- name: gcr.io/cloud-builders/gcloud",
                "  entrypoint: bash",
                "  args:",
                "  - -lc",
                f"  - echo {V42_MARKER}",
                "options:",
                "  logging: CLOUD_LOGGING_ONLY",
                "timeout: 600s",
                "",
            ]
        ),
        encoding="utf-8",
    )


def _cloud_build_probe(gcloud_path: str, env: dict[str, str], *, project_id: str, regional_location: str) -> dict[str, Any]:
    _write_build_config(BUILD_CONFIG)
    submit = safe_run(
        [
            gcloud_path,
            "builds",
            "submit",
            "--no-source",
            "--config",
            str(BUILD_CONFIG),
            "--region",
            regional_location,
            "--project",
            project_id,
            "--quiet",
            "--format=json",
        ],
        env=env,
        timeout=2400,
    )
    submit_parsed = _json_from_stdout(submit.stdout)
    build_id = str(submit_parsed.get("metadata", {}).get("build", {}).get("id") or submit_parsed.get("id") or "").strip()
    describe_parsed: Any = {}
    describe = None
    if build_id:
        describe = safe_run(
            [
                gcloud_path,
                "builds",
                "describe",
                build_id,
                "--region",
                regional_location,
                "--project",
                project_id,
                "--format=json",
            ],
            env=env,
            timeout=300,
        )
        describe_parsed = _json_from_stdout(describe.stdout)
    status = str(describe_parsed.get("status") or submit_parsed.get("status") or "").upper()
    overall_ok = submit.returncode == 0 and status == "SUCCESS"
    return {
        "cloud_build_state": "minimal_run_verified" if overall_ok else "build_blocked",
        "build_id": build_id,
        "deterministic_marker": V42_MARKER,
        "submit": {
            "returncode": submit.returncode,
            "stdout_excerpt": submit.stdout[-3000:],
            "stderr_excerpt": submit.stderr[-2000:],
            "parsed": submit_parsed,
        },
        "describe": {
            "returncode": -1 if describe is None else describe.returncode,
            "stdout_excerpt": "" if describe is None else describe.stdout[-3000:],
            "stderr_excerpt": "" if describe is None else describe.stderr[-2000:],
            "parsed": describe_parsed,
        },
    }


def _dataplex_probe(gcloud_path: str, env: dict[str, str], *, project_id: str, regional_location: str) -> dict[str, Any]:
    lakes = safe_run(
        [
            gcloud_path,
            "dataplex",
            "lakes",
            "list",
            "--location",
            regional_location,
            "--project",
            project_id,
            "--format=json",
        ],
        env=env,
        timeout=300,
    )
    parsed = _json_from_stdout(lakes.stdout)
    overall_ok = lakes.returncode == 0 and isinstance(parsed, list)
    return {
        "dataplex_state": "control_plane_verified" if overall_ok else "control_plane_blocked",
        "lake_count": len(parsed) if isinstance(parsed, list) else 0,
        "list": {
            "returncode": lakes.returncode,
            "stdout_excerpt": lakes.stdout[-3000:],
            "stderr_excerpt": lakes.stderr[-2000:],
            "parsed": parsed,
        },
    }


def _gke_telemetry_probe(gcloud_path: str, env: dict[str, str], *, project_id: str, membership_name: str, membership_location: str) -> dict[str, Any]:
    KUBECONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    env_with_kube = dict(env)
    env_with_kube["KUBECONFIG"] = str(KUBECONFIG_PATH)
    gateway = safe_run(
        [
            gcloud_path,
            "container",
            "fleet",
            "memberships",
            "get-credentials",
            membership_name,
            "--location",
            membership_location,
            "--project",
            project_id,
        ],
        env=env_with_kube,
        timeout=1800,
    )
    kubectl = kubectl_path()
    job_name = f"v42-telemetry-{int(time.time())}"
    marker = f"{V42_MARKER}::{job_name}"
    create = safe_run(
        [
            kubectl,
            "--kubeconfig",
            str(KUBECONFIG_PATH),
            "create",
            "job",
            job_name,
            "--image=busybox:1.36",
            "--",
            "sh",
            "-lc",
            f"echo {marker}",
        ],
        env=env_with_kube,
        timeout=300,
    )
    wait = safe_run(
        [
            kubectl,
            "--kubeconfig",
            str(KUBECONFIG_PATH),
            "wait",
            "--for=condition=complete",
            f"job/{job_name}",
            "--timeout=180s",
        ],
        env=env_with_kube,
        timeout=240,
    )
    logs = safe_run(
        [kubectl, "--kubeconfig", str(KUBECONFIG_PATH), "logs", f"job/{job_name}"],
        env=env_with_kube,
        timeout=300,
    )
    job_get = safe_run(
        [kubectl, "--kubeconfig", str(KUBECONFIG_PATH), "get", "job", job_name, "-o", "json"],
        env=env_with_kube,
        timeout=300,
    )
    pod_get = safe_run(
        [kubectl, "--kubeconfig", str(KUBECONFIG_PATH), "get", "pods", "-l", f"job-name={job_name}", "-o", "json"],
        env=env_with_kube,
        timeout=300,
    )
    job_json = _json_from_stdout(job_get.stdout)
    pod_json = _json_from_stdout(pod_get.stdout)
    job_status = job_json.get("status", {}) if isinstance(job_json, dict) else {}
    pod_items = pod_json.get("items", []) if isinstance(pod_json, dict) else []
    pod_item = pod_items[0] if isinstance(pod_items, list) and pod_items else {}
    pod_status = pod_item.get("status", {}) if isinstance(pod_item, dict) else {}
    pod_spec = pod_item.get("spec", {}) if isinstance(pod_item, dict) else {}
    pod_containers = pod_spec.get("containers", []) if isinstance(pod_spec, dict) else []
    container = pod_containers[0] if isinstance(pod_containers, list) and pod_containers else {}
    container_args = container.get("args", []) if isinstance(container, dict) else []
    marker_in_logs = marker in logs.stdout
    marker_in_args = marker in " ".join(str(arg) for arg in container_args)
    job_complete = wait.returncode == 0 and int(job_status.get("succeeded") or 0) >= 1
    pod_succeeded = str(pod_status.get("phase") or "") == "Succeeded"
    cleanup = safe_run(
        [kubectl, "--kubeconfig", str(KUBECONFIG_PATH), "delete", "job", job_name, "--ignore-not-found=true"],
        env=env_with_kube,
        timeout=300,
    )
    overall_ok = (
        gateway.returncode == 0
        and create.returncode == 0
        and wait.returncode == 0
        and job_get.returncode == 0
        and pod_get.returncode == 0
        and job_complete
        and pod_succeeded
        and (marker_in_logs or marker_in_args)
    )
    return {
        "gke_telemetry_state": "marker_job_verified" if overall_ok else "marker_job_blocked",
        "membership_name": membership_name,
        "membership_location": membership_location,
        "job_name": job_name,
        "deterministic_marker": marker,
        "marker_evidence_mode": (
            "logs_and_spec"
            if marker_in_logs and marker_in_args
            else "logs"
            if marker_in_logs
            else "job_spec_args"
            if marker_in_args
            else "missing"
        ),
        "job_completion_state": "completed" if job_complete else "incomplete",
        "pod_phase": str(pod_status.get("phase") or ""),
        "gateway": {
            "returncode": gateway.returncode,
            "stdout_excerpt": gateway.stdout[-2000:],
            "stderr_excerpt": gateway.stderr[-2000:],
        },
        "create": {
            "returncode": create.returncode,
            "stdout_excerpt": create.stdout[-2000:],
            "stderr_excerpt": create.stderr[-2000:],
        },
        "wait": {
            "returncode": wait.returncode,
            "stdout_excerpt": wait.stdout[-2000:],
            "stderr_excerpt": wait.stderr[-2000:],
        },
        "logs": {
            "returncode": logs.returncode,
            "stdout_excerpt": logs.stdout[-2000:],
            "stderr_excerpt": logs.stderr[-2000:],
        },
        "job_get": {
            "returncode": job_get.returncode,
            "stdout_excerpt": job_get.stdout[-2000:],
            "stderr_excerpt": job_get.stderr[-1200:],
            "parsed": job_json,
        },
        "pod_get": {
            "returncode": pod_get.returncode,
            "stdout_excerpt": pod_get.stdout[-2000:],
            "stderr_excerpt": pod_get.stderr[-1200:],
            "parsed": pod_json,
        },
        "cleanup": {
            "returncode": cleanup.returncode,
            "stdout_excerpt": cleanup.stdout[-1200:],
            "stderr_excerpt": cleanup.stderr[-1200:],
        },
    }


def _markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V42 API Automation Wave",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- API ascendancy state: `{payload['api_ascendancy_state']}`",
        f"- Cloud Run state: `{payload['cloud_run_state']}`",
        f"- Cloud Build state: `{payload['cloud_build_state']}`",
        f"- Dataplex state: `{payload['dataplex_state']}`",
        f"- GKE telemetry state: `{payload['gke_telemetry_state']}`",
        "",
        "## Service Enablement",
        "",
        f"- enabled: `{len(payload['service_enablement']['enabled'])}`",
        f"- already_enabled: `{len(payload['service_enablement']['already_enabled'])}`",
        f"- failed: `{len(payload['service_enablement']['failed'])}`",
        "",
        "## Carry-Forward Baselines",
        "",
    ]
    for key, row in payload.get("carry_forward_baselines", {}).items():
        state_value = ""
        for candidate_key, candidate_value in row.items():
            if candidate_key not in {"path", "overall_status"}:
                state_value = str(candidate_value)
                break
        lines.append(f"- `{key}`: `{row.get('overall_status', '')}` / `{state_value}`")
    if payload.get("blockers"):
        lines.extend(["", "## Blockers", ""])
        lines.extend(f"- {row}" for row in payload["blockers"])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the V42 curated API and telemetry automation wave.")
    parser.add_argument("--bundle", default=str(Path.home() / "GCP service account keys.txt"))
    parser.add_argument("--project-id", default=PROJECT_ID)
    parser.add_argument("--regional-location", default=DEFAULT_REGIONAL_LOCATION)
    parser.add_argument("--cloud-run-service", default=DEFAULT_CLOUD_RUN_SERVICE)
    parser.add_argument("--membership-name", default=DEFAULT_MEMBERSHIP)
    parser.add_argument("--membership-location", default=DEFAULT_MEMBERSHIP_LOCATION)
    parser.add_argument("--scheduled", action="store_true")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()

    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": "v42_omega",
        "overall_status": "WARN",
        "execution_mode": "scheduled" if args.scheduled else "manual",
        "api_ascendancy_state": "pending",
        "cloud_run_state": "pending",
        "cloud_build_state": "pending",
        "dataplex_state": "pending",
        "gke_telemetry_state": "pending",
        "project_id": args.project_id,
        "regional_location": args.regional_location,
        "official_sources": OFFICIAL_SOURCES,
        "completed_steps": [],
        "blockers": [],
        "carry_forward_baselines": {
            "anthos": _carry_forward_state(ROOT / "docs" / "trinity-live-traces" / "v38-fleet-anthos-proof-v1.json", "anthos_state"),
            "cloud_os_login": _carry_forward_state(ROOT / "docs" / "trinity-live-traces" / "v38-os-login-proof-v1.json", "os_login_state"),
            "agent_engine": _carry_forward_state(ROOT / "docs" / "trinity-live-traces" / "v40-agent-engine-advanced-probe-v1.json", "agent_engine_advanced_state"),
            "kai_v41": _carry_forward_state(ROOT / "docs" / "trinity-live-traces" / "v41-kai-health-monitor-proof-v1.json", "kai_health_monitor_state"),
            "vesper_v41": _carry_forward_state(ROOT / "docs" / "trinity-live-traces" / "v41-vesper-telemetry-bridge-proof-v1.json", "vesper_telemetry_ingest_state"),
        },
    }

    operator, gcloud_path, env = _operator_env(args.bundle)
    payload["windows_operator_dependency"] = {
        "overall_status": str(operator.get("overall_status") or ""),
        "windows_operator_lane_state": str(operator.get("windows_operator_lane_state") or ""),
        "gcloud_path": gcloud_path,
    }
    payload["completed_steps"].append("windows_operator_lane_reused")

    service_inventory = _service_inventory(args.project_id, args.bundle)
    payload["service_enablement"] = service_inventory
    payload["completed_steps"].append("service_enablement_inventory_completed")
    if service_inventory["failed"]:
        payload["blockers"].append("One or more V42 services could not be enabled or re-verified.")

    cloud_run = _cloud_run_probe(gcloud_path, env, project_id=args.project_id, regional_location=args.regional_location, service_name=args.cloud_run_service)
    payload["cloud_run"] = cloud_run
    payload["cloud_run_state"] = cloud_run["cloud_run_state"]
    if cloud_run["cloud_run_state"] == "minimal_workload_verified":
        payload["completed_steps"].append("cloud_run_minimal_workload_verified")
    else:
        payload["blockers"].append("Cloud Run did not complete the bounded V42 proof.")

    cloud_build = _cloud_build_probe(gcloud_path, env, project_id=args.project_id, regional_location=args.regional_location)
    payload["cloud_build"] = cloud_build
    payload["cloud_build_state"] = cloud_build["cloud_build_state"]
    if cloud_build["cloud_build_state"] == "minimal_run_verified":
        payload["completed_steps"].append("cloud_build_minimal_run_verified")
    else:
        payload["blockers"].append("Cloud Build did not complete the bounded V42 proof.")

    dataplex = _dataplex_probe(gcloud_path, env, project_id=args.project_id, regional_location=args.regional_location)
    payload["dataplex"] = dataplex
    payload["dataplex_state"] = dataplex["dataplex_state"]
    if dataplex["dataplex_state"] == "control_plane_verified":
        payload["completed_steps"].append("dataplex_control_plane_verified")
    else:
        payload["blockers"].append("Dataplex control-plane verification did not complete cleanly.")

    gke_probe = _gke_telemetry_probe(
        gcloud_path,
        env,
        project_id=args.project_id,
        membership_name=args.membership_name,
        membership_location=args.membership_location,
    )
    payload["gke_telemetry"] = gke_probe
    payload["gke_telemetry_state"] = gke_probe["gke_telemetry_state"]
    if gke_probe["gke_telemetry_state"] == "marker_job_verified":
        payload["completed_steps"].append("gke_marker_job_verified")
    else:
        payload["blockers"].append("The bounded GKE telemetry job did not complete with the deterministic V42 marker.")

    ok = not payload["blockers"]
    payload["overall_status"] = "PASS" if ok else "WARN"
    payload["api_ascendancy_state"] = "curated_wave_verified" if ok else "curated_wave_bounded_with_residuals"
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), _markdown(payload))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
