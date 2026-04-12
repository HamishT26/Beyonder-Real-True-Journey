#!/usr/bin/env python3
"""Run the V38 bounded Cloud OS Login proof on a minimal Linux VM."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

from trinity_v32_runtime_common import PROJECT_ID, google_request
from trinity_v36_cloud_common import ensure_service_enabled, load_primary_service_account, now_iso, write_json, write_text
from trinity_v38_windows_operator_probe import build_gcloud_env, ensure_operator_lane

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v38-os-login-proof-v1.json"
OUTPUT_MD = ROOT / "docs" / "trinity-live-traces" / "v38-os-login-proof-v1.md"
DEFAULT_VM = "beyonder-v38-oslogin-dev"
DEFAULT_ZONE = "australia-southeast1-a"
SERVICE_NAMES = ["compute.googleapis.com", "oslogin.googleapis.com"]


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


def instance_url(project_id: str, zone: str, vm_name: str) -> str:
    return f"https://compute.googleapis.com/compute/v1/projects/{project_id}/zones/{zone}/instances/{vm_name}"


def instance_probe(project_id: str, zone: str, vm_name: str, token: str) -> dict[str, Any]:
    return google_request("GET", instance_url(project_id, zone, vm_name), token, timeout=240)


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V38 OS Login Proof",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- OS Login state: `{payload['os_login_state']}`",
        f"- VM name: `{payload['vm_name']}`",
        f"- Zone: `{payload['zone']}`",
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
    parser = argparse.ArgumentParser(description="Run the V38 bounded Cloud OS Login proof.")
    parser.add_argument("--bundle", default=str(Path.home() / "GCP service account keys.txt"))
    parser.add_argument("--project-id", default=PROJECT_ID)
    parser.add_argument("--vm-name", default=DEFAULT_VM)
    parser.add_argument("--zone", default=DEFAULT_ZONE)
    parser.add_argument("--output-json", default=str(OUTPUT_JSON))
    parser.add_argument("--output-md", default=str(OUTPUT_MD))
    args = parser.parse_args()

    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": "v38_omega",
        "project_id": args.project_id,
        "vm_name": args.vm_name,
        "zone": args.zone,
        "overall_status": "WARN",
        "os_login_state": "pending",
        "completed_steps": [],
        "blockers": [],
    }

    try:
        _records, primary, minted = load_primary_service_account(Path(args.bundle))
    except Exception as exc:
        payload["overall_status"] = "FAIL"
        payload["os_login_state"] = "blocked_missing_identity"
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
        payload["os_login_state"] = "blocked_service_enablement"
        payload["blockers"].append("Compute Engine or Cloud OS Login is not fully enabled.")
        write_json(Path(args.output_json), payload)
        write_text(Path(args.output_md), markdown(payload))
        return 1
    payload["completed_steps"].append("os_login_services_enabled")

    operator = ensure_operator_lane(args.bundle, bootstrap=True)
    payload["windows_operator_dependency"] = {
        "overall_status": operator.get("overall_status"),
        "windows_operator_lane_state": operator.get("windows_operator_lane_state"),
        "gcloud_path": operator.get("gcloud_path"),
    }
    if operator.get("overall_status") != "PASS":
        payload["overall_status"] = "FAIL"
        payload["os_login_state"] = "blocked_operator_lane"
        payload["blockers"].extend(str(row) for row in operator.get("blockers", []))
        write_json(Path(args.output_json), payload)
        write_text(Path(args.output_md), markdown(payload))
        return 1
    payload["completed_steps"].append("windows_operator_lane_reused")

    env = build_gcloud_env()
    gcloud_path = str(operator.get("gcloud_path") or "gcloud")

    describe = run(
        [gcloud_path, "compute", "instances", "describe", args.vm_name, "--zone", args.zone, "--project", args.project_id, "--format=json"],
        env=env,
        timeout=300,
    )
    payload["instance_describe"] = {
        "returncode": describe.returncode,
        "stdout_excerpt": describe.stdout[:2000],
        "stderr_excerpt": describe.stderr[-2000:],
    }
    if describe.returncode != 0:
        create = run(
            [
                gcloud_path,
                "compute",
                "instances",
                "create",
                args.vm_name,
                "--project",
                args.project_id,
                "--zone",
                args.zone,
                "--machine-type",
                "e2-micro",
                "--image-family",
                "debian-12",
                "--image-project",
                "debian-cloud",
                "--metadata",
                "enable-oslogin=TRUE",
                "--service-account",
                payload["primary_identity"],
                "--scopes",
                "cloud-platform",
                "--quiet",
            ],
            env=env,
            timeout=1800,
        )
        payload["instance_create"] = {
            "returncode": create.returncode,
            "stdout_excerpt": create.stdout[-3000:],
            "stderr_excerpt": create.stderr[-3000:],
        }
        if create.returncode != 0:
            payload["overall_status"] = "FAIL"
            payload["os_login_state"] = "blocked_vm_create_failed"
            payload["blockers"].append("The bounded OS Login VM create attempt failed.")
            write_json(Path(args.output_json), payload)
            write_text(Path(args.output_md), markdown(payload))
            return 1
        payload["completed_steps"].append("os_login_vm_created")

    probe = instance_probe(args.project_id, args.zone, args.vm_name, token)
    payload["instance_probe_status"] = probe["status"]
    parsed = probe.get("parsed", {}) if isinstance(probe.get("parsed", {}), dict) else {}
    metadata = parsed.get("metadata", {}) if isinstance(parsed.get("metadata"), dict) else {}
    metadata_items = metadata.get("items", []) if isinstance(metadata.get("items"), list) else []
    enable_oslogin = next((row.get("value") for row in metadata_items if isinstance(row, dict) and str(row.get("key") or "") == "enable-oslogin"), "")
    payload["instance_metadata"] = {"enable_oslogin": enable_oslogin, "status": str(parsed.get("status") or "")}
    if probe["status"] != 200:
        payload["overall_status"] = "FAIL"
        payload["os_login_state"] = "blocked_vm_visibility"
        payload["blockers"].append("The OS Login VM is not visible from the Compute Engine API.")
        write_json(Path(args.output_json), payload)
        write_text(Path(args.output_md), markdown(payload))
        return 1
    payload["completed_steps"].append("os_login_vm_visible")

    if str(enable_oslogin).upper() != "TRUE":
        payload["overall_status"] = "FAIL"
        payload["os_login_state"] = "blocked_instance_metadata"
        payload["blockers"].append("The instance metadata does not report enable-oslogin=TRUE.")
        write_json(Path(args.output_json), payload)
        write_text(Path(args.output_md), markdown(payload))
        return 1
    payload["completed_steps"].append("os_login_metadata_verified")

    profile = run([gcloud_path, "compute", "os-login", "describe-profile", "--project", args.project_id, "--format=json"], env=env, timeout=300)
    payload["os_login_profile"] = {
        "returncode": profile.returncode,
        "stdout_excerpt": profile.stdout[:2000],
        "stderr_excerpt": profile.stderr[-2000:],
    }
    if profile.returncode == 0:
        payload["completed_steps"].append("os_login_profile_described")

    ssh = run(
        [
            gcloud_path,
            "compute",
            "ssh",
            args.vm_name,
            "--project",
            args.project_id,
            "--zone",
            args.zone,
            "--command",
            "echo V38_OSLOGIN_OK && hostname",
            "--quiet",
        ],
        env=env,
        timeout=900,
    )
    payload["ssh_attempt"] = {
        "returncode": ssh.returncode,
        "stdout_excerpt": ssh.stdout[-3000:],
        "stderr_excerpt": ssh.stderr[-3000:],
    }
    if ssh.returncode != 0:
        payload["overall_status"] = "WARN"
        payload["os_login_state"] = "bounded_metadata_verified_ssh_blocked"
        payload["blockers"].append("Cloud OS Login metadata is valid, but the real SSH session did not complete cleanly.")
        write_json(Path(args.output_json), payload)
        write_text(Path(args.output_md), markdown(payload))
        return 1

    payload["completed_steps"].append("os_login_ssh_verified")
    payload["overall_status"] = "PASS"
    payload["os_login_state"] = "ssh_verified"
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
