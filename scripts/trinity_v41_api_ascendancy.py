#!/usr/bin/env python3
"""Run the V41 curated API ascendancy wave and bounded cloud proofs."""

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
from trinity_v38_windows_operator_probe import build_gcloud_env, ensure_operator_lane
from trinity_v41_common import now_iso, read_json, safe_run, write_json, write_text

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v41-api-ascendancy-proof-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v41-api-ascendancy-proof-v1.md"
BUILD_CONFIG = ROOT / ".local-runtime" / "v41" / "cloudbuild-minimal.yaml"

CORE_SERVICES = (
    "run.googleapis.com",
    "cloudbuild.googleapis.com",
    "dataplex.googleapis.com",
)
CURATED_SERVICES = (
    "run.googleapis.com",
    "cloudbuild.googleapis.com",
    "dataplex.googleapis.com",
    "artifactregistry.googleapis.com",
    "serviceusage.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "compute.googleapis.com",
    "container.googleapis.com",
    "gkeconnect.googleapis.com",
    "gkehub.googleapis.com",
    "oslogin.googleapis.com",
    "aiplatform.googleapis.com",
    "bigtable.googleapis.com",
    "bigtableadmin.googleapis.com",
    "iam.googleapis.com",
    "iamcredentials.googleapis.com",
)
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
    for service_name in CURATED_SERVICES:
        result = ensure_service_enabled(project_id, token, service_name)
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


def _cloud_run_probe(
    gcloud_path: str,
    env: dict[str, str],
    *,
    project_id: str,
    regional_location: str,
    service_name: str,
) -> dict[str, Any]:
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
            "phase=v41omega,managed_by=codex",
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
    url = str(
        describe_parsed.get("status", {}).get("url")
        or describe_parsed.get("uri")
        or deploy_parsed.get("status", {}).get("url")
        or ""
    ).strip()
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
                http_probe = {
                    "url": url,
                    "status_code": 0,
                    "body_excerpt": str(exc)[:600],
                    "ok": False,
                }
            time.sleep(5)
    overall_ok = deploy.returncode == 0 and describe.returncode == 0 and bool(http_probe.get("ok"))
    return {
        "cloud_run_state": "minimal_workload_verified" if overall_ok else "deployment_blocked",
        "service_name": service_name,
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
                "  - echo V41_CLOUD_BUILD_OK",
                "options:",
                "  logging: CLOUD_LOGGING_ONLY",
                "timeout: 600s",
                "",
            ]
        ),
        encoding="utf-8",
    )


def _cloud_build_probe(
    gcloud_path: str,
    env: dict[str, str],
    *,
    project_id: str,
    regional_location: str,
) -> dict[str, Any]:
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


def _dataplex_probe(
    gcloud_path: str,
    env: dict[str, str],
    *,
    project_id: str,
    regional_location: str,
) -> dict[str, Any]:
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


def _markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V41 API Ascendancy Proof",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- API ascendancy state: `{payload['api_ascendancy_state']}`",
        f"- Cloud Run state: `{payload['cloud_run_state']}`",
        f"- Cloud Build state: `{payload['cloud_build_state']}`",
        f"- Dataplex state: `{payload['dataplex_state']}`",
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
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the V41 curated API ascendancy wave.")
    parser.add_argument("--bundle", default=str(Path.home() / "GCP service account keys.txt"))
    parser.add_argument("--project-id", default=PROJECT_ID)
    parser.add_argument("--regional-location", default=DEFAULT_REGIONAL_LOCATION)
    parser.add_argument("--cloud-run-service", default="beyonder-v41-cloudrun-probe")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()

    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": "v41_omega",
        "overall_status": "WARN",
        "api_ascendancy_state": "pending",
        "cloud_run_state": "pending",
        "cloud_build_state": "pending",
        "dataplex_state": "pending",
        "project_id": args.project_id,
        "regional_location": args.regional_location,
        "official_sources": OFFICIAL_SOURCES,
        "completed_steps": [],
        "blockers": [],
        "deferred_expansions": [
            "service_agent_role_grants_deferred",
            "alternate_account_service_account_expansion_deferred",
        ],
        "carry_forward_baselines": {
            "anthos": _carry_forward_state(ROOT / "docs" / "trinity-live-traces" / "v38-fleet-anthos-proof-v1.json", "anthos_state"),
            "cloud_os_login": _carry_forward_state(ROOT / "docs" / "trinity-live-traces" / "v38-os-login-proof-v1.json", "os_login_state"),
            "agent_engine": _carry_forward_state(ROOT / "docs" / "trinity-live-traces" / "v40-agent-engine-advanced-probe-v1.json", "agent_engine_advanced_state"),
        },
    }

    service_enablement = _service_inventory(args.project_id, args.bundle)
    payload["service_enablement"] = service_enablement
    payload["completed_steps"].append("service_enablement_inventory_completed")
    core_failures = [row for row in service_enablement["failed"] if row["service_name"] in CORE_SERVICES]
    if core_failures:
        payload["overall_status"] = "FAIL"
        payload["api_ascendancy_state"] = "blocked_core_service_enablement"
        payload["cloud_run_state"] = "service_enablement_blocked"
        payload["cloud_build_state"] = "service_enablement_blocked"
        payload["dataplex_state"] = "service_enablement_blocked"
        payload["blockers"].extend(
            f"{row['service_name']}: {row['reason'] or 'enablement failed'}" for row in core_failures
        )
        write_json(Path(args.output_json), payload)
        write_text(Path(args.output_md), _markdown(payload))
        return 1

    operator, gcloud_path, env = _operator_env(args.bundle)
    payload["windows_operator_dependency"] = {
        "overall_status": str(operator.get("overall_status") or ""),
        "windows_operator_lane_state": str(operator.get("windows_operator_lane_state") or ""),
        "gcloud_path": gcloud_path,
    }
    if str(operator.get("overall_status") or "") != "PASS" or not gcloud_path:
        payload["overall_status"] = "FAIL"
        payload["api_ascendancy_state"] = "blocked_windows_operator_lane"
        payload["blockers"].append("The bounded Windows operator lane did not reach a reusable PASS state.")
        write_json(Path(args.output_json), payload)
        write_text(Path(args.output_md), _markdown(payload))
        return 1
    payload["completed_steps"].append("windows_operator_lane_reused")

    cloud_run = _cloud_run_probe(
        gcloud_path,
        env,
        project_id=args.project_id,
        regional_location=args.regional_location,
        service_name=args.cloud_run_service,
    )
    payload["cloud_run"] = cloud_run
    payload["cloud_run_state"] = cloud_run["cloud_run_state"]
    if cloud_run["cloud_run_state"] == "minimal_workload_verified":
        payload["completed_steps"].append("cloud_run_minimal_workload_verified")
    else:
        payload["blockers"].append("Cloud Run minimal workload proof did not complete cleanly.")

    cloud_build = _cloud_build_probe(
        gcloud_path,
        env,
        project_id=args.project_id,
        regional_location=args.regional_location,
    )
    payload["cloud_build"] = cloud_build
    payload["cloud_build_state"] = cloud_build["cloud_build_state"]
    if cloud_build["cloud_build_state"] == "minimal_run_verified":
        payload["completed_steps"].append("cloud_build_minimal_run_verified")
    else:
        payload["blockers"].append("Cloud Build minimal run proof did not complete cleanly.")

    dataplex = _dataplex_probe(
        gcloud_path,
        env,
        project_id=args.project_id,
        regional_location=args.regional_location,
    )
    payload["dataplex"] = dataplex
    payload["dataplex_state"] = dataplex["dataplex_state"]
    if dataplex["dataplex_state"] == "control_plane_verified":
        payload["completed_steps"].append("dataplex_control_plane_verified")
    else:
        payload["blockers"].append("Dataplex control-plane list probe did not complete cleanly.")

    all_core_verified = (
        payload["cloud_run_state"] == "minimal_workload_verified"
        and payload["cloud_build_state"] == "minimal_run_verified"
        and payload["dataplex_state"] == "control_plane_verified"
    )
    extra_failures = [row for row in service_enablement["failed"] if row["service_name"] not in CORE_SERVICES]
    if all_core_verified and not extra_failures:
        payload["overall_status"] = "PASS"
        payload["api_ascendancy_state"] = "curated_wave_verified"
    elif all_core_verified:
        payload["overall_status"] = "WARN"
        payload["api_ascendancy_state"] = "curated_wave_verified_with_noncore_failures"
    else:
        payload["overall_status"] = "WARN"
        payload["api_ascendancy_state"] = "curated_wave_bounded"

    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), _markdown(payload))
    return 0 if payload["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
