#!/usr/bin/env python3
"""Run the V43 bounded cloud carry-forward proof on top of the green V42 baselines."""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from trinity_v32_runtime_common import PROJECT_ID
from trinity_v36_cloud_common import DEFAULT_REGIONAL_LOCATION, ensure_service_enabled, load_primary_service_account
from trinity_v38_windows_operator_probe import build_gcloud_env, ensure_operator_lane
from trinity_v43_common import ROOT, now_iso, read_json, safe_run, write_json, write_text

DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v43-cloud-carry-forward-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v43-cloud-carry-forward-v1.md"
BUILD_CONFIG = ROOT / ".local-runtime" / "v43" / "cloudbuild-v43.yaml"
DEFAULT_CLOUD_RUN_SERVICE = "beyonder-v42-cloudrun-probe"
CURATED_SERVICES = (
    "logging.googleapis.com",
    "monitoring.googleapis.com",
    "cloudscheduler.googleapis.com",
    "pubsub.googleapis.com",
    "eventarc.googleapis.com",
    "workflows.googleapis.com",
    "run.googleapis.com",
    "cloudbuild.googleapis.com",
    "dataplex.googleapis.com",
    "gkehub.googleapis.com",
    "gkeconnect.googleapis.com",
    "connectgateway.googleapis.com",
    "oslogin.googleapis.com",
    "discoveryengine.googleapis.com",
)
OFFICIAL_SOURCES = {
    "cloud_run": "https://cloud.google.com/run/docs",
    "cloud_build": "https://cloud.google.com/build/docs/build-config-file-schema",
    "dataplex": "https://cloud.google.com/dataplex/docs",
    "connect_gateway": "https://docs.cloud.google.com/kubernetes-engine/enterprise/multicluster-management/gateway/setup",
    "os_login": "https://docs.cloud.google.com/compute/docs/oslogin",
}


def _json_from_stdout(stdout: str) -> Any:
    text = str(stdout or "").strip()
    if not text:
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {}


def _service_inventory(bundle: str) -> dict[str, Any]:
    _records, primary, minted = load_primary_service_account(Path(bundle))
    token = minted["token"]
    enabled: list[str] = []
    already_enabled: list[str] = []
    failed: list[dict[str, str]] = []
    results: list[dict[str, Any]] = []
    for service_name in CURATED_SERVICES:
        result = ensure_service_enabled(PROJECT_ID, token, service_name)
        results.append(result)
        final_state = str(result.get("final_state") or "")
        initial_state = str(result.get("initial_state") or "")
        final_status = int(result.get("final_status") or 0)
        if final_status == 200 and final_state == "ENABLED":
            if initial_state == "ENABLED":
                already_enabled.append(service_name)
            else:
                enabled.append(service_name)
        else:
            failed.append(
                {
                    "service_name": service_name,
                    "reason": str(result.get("raw_enable_response") or result.get("error") or "enable_failed"),
                }
            )
    return {
        "primary_identity": str(primary.get("client_email") or ""),
        "service_account_path": str(primary.get("runtime_path") or ""),
        "token_expiry_utc": str(minted.get("expiry_utc") or ""),
        "results": results,
        "enabled": enabled,
        "already_enabled": already_enabled,
        "skipped": [],
        "failed": failed,
    }


def _operator_env(bundle: str) -> tuple[dict[str, Any], str, dict[str, str]]:
    operator = ensure_operator_lane(bundle, bootstrap=True)
    gcloud_path = str(operator.get("gcloud_path") or "")
    return operator, gcloud_path, build_gcloud_env()


def _cloud_run_probe(gcloud_path: str, env: dict[str, str], *, regional_location: str, service_name: str) -> dict[str, Any]:
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
            PROJECT_ID,
            "--format=json",
        ],
        env=env,
        timeout=300,
    )
    describe_parsed = _json_from_stdout(describe.stdout)
    url = str(describe_parsed.get("status", {}).get("url") or describe_parsed.get("uri") or "").strip()
    http_probe: dict[str, Any] = {"url": url, "status_code": 0, "body_excerpt": "", "ok": False}
    if url:
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                body = response.read().decode("utf-8", errors="replace")
                http_probe = {
                    "url": url,
                    "status_code": response.status,
                    "body_excerpt": body[:600],
                    "ok": response.status == 200,
                }
        except urllib.error.HTTPError as exc:
            http_probe = {"url": url, "status_code": exc.code, "body_excerpt": exc.read().decode("utf-8", errors="replace")[:600], "ok": False}
        except Exception as exc:  # noqa: BLE001
            http_probe = {"url": url, "status_code": 0, "body_excerpt": str(exc)[:600], "ok": False}
    overall_ok = describe.returncode == 0 and bool(http_probe.get("ok"))
    return {
        "cloud_run_state": "carry_forward_verified" if overall_ok else "probe_blocked",
        "service_name": service_name,
        "describe": {
            "returncode": describe.returncode,
            "stdout_excerpt": describe.stdout[-2400:],
            "stderr_excerpt": describe.stderr[-1600:],
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
                "  - echo V43_CLOUD_BUILD_OK",
                "options:",
                "  logging: CLOUD_LOGGING_ONLY",
                "timeout: 600s",
                "",
            ]
        ),
        encoding="utf-8",
    )


def _cloud_build_probe(gcloud_path: str, env: dict[str, str], *, regional_location: str) -> dict[str, Any]:
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
            PROJECT_ID,
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
                PROJECT_ID,
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
            "stdout_excerpt": submit.stdout[-2400:],
            "stderr_excerpt": submit.stderr[-1600:],
            "parsed": submit_parsed,
        },
        "describe": {
            "returncode": -1 if describe is None else describe.returncode,
            "stdout_excerpt": "" if describe is None else describe.stdout[-2400:],
            "stderr_excerpt": "" if describe is None else describe.stderr[-1600:],
            "parsed": describe_parsed,
        },
    }


def _dataplex_probe(gcloud_path: str, env: dict[str, str], *, regional_location: str) -> dict[str, Any]:
    lakes = safe_run(
        [
            gcloud_path,
            "dataplex",
            "lakes",
            "list",
            "--location",
            regional_location,
            "--project",
            PROJECT_ID,
            "--format=json",
        ],
        env=env,
        timeout=300,
    )
    parsed = _json_from_stdout(lakes.stdout)
    return {
        "dataplex_state": "control_plane_verified" if lakes.returncode == 0 else "probe_blocked",
        "lake_count": len(parsed) if isinstance(parsed, list) else 0,
        "list": {
            "returncode": lakes.returncode,
            "stdout_excerpt": lakes.stdout[-2400:],
            "stderr_excerpt": lakes.stderr[-1600:],
            "parsed": parsed,
        },
    }


def _anthos_probe(gcloud_path: str, env: dict[str, str]) -> dict[str, Any]:
    memberships = safe_run(
        [
            gcloud_path,
            "container",
            "fleet",
            "memberships",
            "list",
            "--project",
            PROJECT_ID,
            "--format=json",
        ],
        env=env,
        timeout=300,
    )
    parsed = _json_from_stdout(memberships.stdout)
    return {
        "anthos_state": "carry_forward_verified" if memberships.returncode == 0 else "probe_blocked",
        "membership_count": len(parsed) if isinstance(parsed, list) else 0,
        "list": {
            "returncode": memberships.returncode,
            "stdout_excerpt": memberships.stdout[-2400:],
            "stderr_excerpt": memberships.stderr[-1600:],
            "parsed": parsed,
        },
    }


def _os_login_probe(gcloud_path: str, env: dict[str, str]) -> dict[str, Any]:
    info = safe_run(
        [
            gcloud_path,
            "compute",
            "project-info",
            "describe",
            "--project",
            PROJECT_ID,
            "--format=json",
        ],
        env=env,
        timeout=300,
    )
    parsed = _json_from_stdout(info.stdout)
    items = parsed.get("commonInstanceMetadata", {}).get("items", []) if isinstance(parsed, dict) else []
    os_login_enabled = None
    for row in items:
        if isinstance(row, dict) and str(row.get("key") or "") == "enable-oslogin":
            os_login_enabled = str(row.get("value") or "")
            break
    return {
        "os_login_state": "carry_forward_verified" if info.returncode == 0 else "probe_blocked",
        "enable_oslogin_value": os_login_enabled,
        "describe": {
            "returncode": info.returncode,
            "stdout_excerpt": info.stdout[-2400:],
            "stderr_excerpt": info.stderr[-1600:],
        },
    }


def _markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V43 Cloud Carry-Forward",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- API ascendancy state: `{payload['api_ascendancy_state']}`",
        f"- Windows operator lane state: `{payload['windows_operator_lane_state']}`",
        f"- Anthos state: `{payload['anthos_state']}`",
        f"- OS Login state: `{payload['os_login_state']}`",
        f"- Cloud Run state: `{payload['cloud_run_state']}`",
        f"- Cloud Build state: `{payload['cloud_build_state']}`",
        f"- Dataplex state: `{payload['dataplex_state']}`",
        "",
        "## Service Inventory",
        "",
        f"- enabled: `{len(payload.get('service_inventory', {}).get('enabled', []))}`",
        f"- already_enabled: `{len(payload.get('service_inventory', {}).get('already_enabled', []))}`",
        f"- failed: `{len(payload.get('service_inventory', {}).get('failed', []))}`",
        "",
    ]
    if payload.get("blockers"):
        lines.extend(["## Blockers", ""])
        lines.extend(f"- {row}" for row in payload["blockers"])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the bounded V43 cloud carry-forward proof.")
    parser.add_argument("--bundle", default=str(Path.home() / "GCP service account keys.txt"))
    parser.add_argument("--regional-location", default=DEFAULT_REGIONAL_LOCATION)
    parser.add_argument("--cloud-run-service", default=DEFAULT_CLOUD_RUN_SERVICE)
    parser.add_argument("--scheduled", action="store_true")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()

    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": "v43_omega",
        "overall_status": "WARN",
        "execution_mode": "scheduled" if args.scheduled else "manual",
        "api_ascendancy_state": "pending",
        "windows_operator_lane_state": "pending",
        "anthos_state": "pending",
        "os_login_state": "pending",
        "cloud_run_state": "pending",
        "cloud_build_state": "pending",
        "dataplex_state": "pending",
        "official_sources": OFFICIAL_SOURCES,
        "blockers": [],
    }

    service_inventory = _service_inventory(args.bundle)
    payload["service_inventory"] = service_inventory
    if service_inventory.get("failed"):
        payload["blockers"].append("One or more V43 services could not be enabled or re-verified.")

    operator, gcloud_path, env = _operator_env(args.bundle)
    payload["windows_operator_lane_state"] = str(operator.get("windows_operator_lane_state") or "gcloud_ready")

    anthos = _anthos_probe(gcloud_path, env)
    payload["anthos_probe"] = anthos
    payload["anthos_state"] = anthos["anthos_state"]
    payload["anthos_membership_count"] = anthos["membership_count"]
    if anthos["anthos_state"] != "carry_forward_verified":
        payload["blockers"].append("Anthos or fleet membership listing did not complete cleanly.")

    os_login = _os_login_probe(gcloud_path, env)
    payload["os_login_probe"] = os_login
    payload["os_login_state"] = os_login["os_login_state"]
    payload["os_login_enabled_value"] = os_login["enable_oslogin_value"]
    if os_login["os_login_state"] != "carry_forward_verified":
        payload["blockers"].append("OS Login metadata query did not complete cleanly.")

    cloud_run = _cloud_run_probe(gcloud_path, env, regional_location=args.regional_location, service_name=args.cloud_run_service)
    payload["cloud_run_probe"] = cloud_run
    payload["cloud_run_state"] = cloud_run["cloud_run_state"]
    payload["cloud_run_service_name"] = cloud_run["service_name"]
    payload["cloud_run_http_probe"] = cloud_run["http_probe"]
    if cloud_run["cloud_run_state"] != "carry_forward_verified":
        payload["blockers"].append("Cloud Run did not complete the bounded V43 carry-forward probe.")

    cloud_build = _cloud_build_probe(gcloud_path, env, regional_location=args.regional_location)
    payload["cloud_build_probe"] = cloud_build
    payload["cloud_build_state"] = cloud_build["cloud_build_state"]
    payload["cloud_build_id"] = cloud_build["build_id"]
    if cloud_build["cloud_build_state"] != "minimal_run_verified":
        payload["blockers"].append("Cloud Build did not complete the bounded V43 carry-forward probe.")

    dataplex = _dataplex_probe(gcloud_path, env, regional_location=args.regional_location)
    payload["dataplex_probe"] = dataplex
    payload["dataplex_state"] = dataplex["dataplex_state"]
    payload["dataplex_lake_count"] = dataplex["lake_count"]
    if dataplex["dataplex_state"] != "control_plane_verified":
        payload["blockers"].append("Dataplex did not complete the bounded V43 control-plane probe.")

    payload["api_ascendancy_state"] = "carry_forward_verified" if not payload["blockers"] else "carry_forward_verified_with_residuals"
    payload["overall_status"] = "PASS" if not payload["blockers"] else "WARN"
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), _markdown(payload))
    return 0 if payload["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
