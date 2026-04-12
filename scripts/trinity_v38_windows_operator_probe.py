#!/usr/bin/env python3
"""Verify or bootstrap the Windows operator lane for V38 Omega."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

from trinity_v36_cloud_common import load_compute_service_account
from trinity_v32_runtime_common import PROJECT_ID, now_iso, write_json, write_text

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v38-windows-operator-proof-v1.json"
OUTPUT_MD = ROOT / "docs" / "trinity-live-traces" / "v38-windows-operator-proof-v1.md"
GCLOUD_CONFIG_DIR = ROOT / ".local-runtime" / "gcloud" / "v38"
KNOWN_GCLOUD_PATHS = [
    Path(r"C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"),
    Path(r"C:\Program Files\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"),
    Path.home() / "AppData" / "Local" / "Google" / "Cloud SDK" / "google-cloud-sdk" / "bin" / "gcloud.cmd",
]
KNOWN_PLUGIN_PATHS = [
    Path(r"C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin\gke-gcloud-auth-plugin.exe"),
    Path(r"C:\Program Files\Google\Cloud SDK\google-cloud-sdk\bin\gke-gcloud-auth-plugin.exe"),
    Path.home() / "AppData" / "Local" / "Google" / "Cloud SDK" / "google-cloud-sdk" / "bin" / "gke-gcloud-auth-plugin.exe",
]
WINGET_ARGS = [
    "winget",
    "install",
    "--id",
    "Google.CloudSDK",
    "--exact",
    "--accept-package-agreements",
    "--accept-source-agreements",
    "--silent",
    "--disable-interactivity",
]
CHOCO_ARGS = [
    "choco",
    "install",
    "gcloudsdk",
    "-y",
]
REQUIRED_BASE_TOOLS = ("kubectl", "ssh", "node", "npm", "npx")


def run(
    args: list[str],
    *,
    env: dict[str, str] | None = None,
    timeout: int = 600,
) -> subprocess.CompletedProcess[str]:
    try:
        proc = subprocess.run(
            args,
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        proc.stdout = (proc.stdout or "").replace("\x00", "")
        proc.stderr = (proc.stderr or "").replace("\x00", "")
        return proc
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout if isinstance(exc.stdout, str) else (exc.stdout or b"").decode("utf-8", errors="replace")
        stderr = exc.stderr if isinstance(exc.stderr, str) else (exc.stderr or b"").decode("utf-8", errors="replace")
        return subprocess.CompletedProcess(
            args=args,
            returncode=124,
            stdout=(stdout or "").replace("\x00", ""),
            stderr=((stderr or "").replace("\x00", "") + f"\ncommand timed out after {timeout} seconds").strip(),
        )


def command_status(name: str) -> dict[str, Any]:
    resolved = shutil.which(name)
    return {
        "name": name,
        "present": bool(resolved),
        "path": resolved or "",
    }


def find_gcloud() -> str:
    resolved = shutil.which("gcloud")
    if resolved:
        return resolved
    for path in KNOWN_GCLOUD_PATHS:
        if path.exists():
            return str(path)
    return ""


def find_gke_plugin() -> str:
    resolved = shutil.which("gke-gcloud-auth-plugin")
    if resolved:
        return resolved
    for path in KNOWN_PLUGIN_PATHS:
        if path.exists():
            return str(path)
    return ""


def build_gcloud_env() -> dict[str, str]:
    env = dict(os.environ)
    GCLOUD_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    env["CLOUDSDK_CONFIG"] = str(GCLOUD_CONFIG_DIR)
    return env


def activate_service_account(gcloud_path: str, env: dict[str, str], payload: dict[str, Any], bundle: str) -> None:
    _records, primary, _minted = load_compute_service_account(Path(bundle))
    payload["service_account_path"] = str(primary["runtime_path"])
    payload["service_account_email"] = str(primary["client_email"])

    auth = run(
        [
            gcloud_path,
            "auth",
            "activate-service-account",
            str(primary["client_email"]),
            f"--key-file={primary['runtime_path']}",
            f"--project={PROJECT_ID}",
            "--quiet",
        ],
        env=env,
        timeout=300,
    )
    payload["gcloud_auth"] = {
        "returncode": auth.returncode,
        "stdout": auth.stdout[-2000:],
        "stderr": auth.stderr[-2000:],
    }
    if auth.returncode == 0:
        payload["completed_steps"].append("gcloud_service_account_activated")
    else:
        payload["blockers"].append("gcloud could not activate the compute-default service account.")
        return

    set_project = run(
        [gcloud_path, "config", "set", "project", PROJECT_ID],
        env=env,
        timeout=120,
    )
    payload["gcloud_set_project"] = {
        "returncode": set_project.returncode,
        "stdout": set_project.stdout[-1200:],
        "stderr": set_project.stderr[-1200:],
    }
    if set_project.returncode == 0:
        payload["completed_steps"].append("gcloud_project_set")
    else:
        payload["blockers"].append("gcloud could not set the active project for V38.")

    active = run(
        [gcloud_path, "auth", "list", "--format=json"],
        env=env,
        timeout=120,
    )
    parsed: Any = []
    if active.returncode == 0:
        try:
            parsed = json.loads(active.stdout or "[]")
        except json.JSONDecodeError:
            parsed = []
    payload["gcloud_auth_list"] = {
        "returncode": active.returncode,
        "parsed": parsed,
        "stderr": active.stderr[-1200:],
    }


def ensure_plugin(gcloud_path: str, env: dict[str, str], payload: dict[str, Any]) -> None:
    plugin_path = find_gke_plugin()
    if plugin_path:
        payload["gke_gcloud_auth_plugin_path"] = plugin_path
        payload["completed_steps"].append("gke_gcloud_auth_plugin_detected")
        return

    plugin_env = dict(env)
    bundled_python = run([gcloud_path, "components", "copy-bundled-python"], env=env, timeout=600)
    payload["gcloud_bundled_python"] = {
        "returncode": bundled_python.returncode,
        "stdout": bundled_python.stdout[-1200:],
        "stderr": bundled_python.stderr[-1200:],
    }
    bundled_python_path = (bundled_python.stdout or "").strip().splitlines()[-1].strip() if bundled_python.returncode == 0 else ""
    if bundled_python_path:
        plugin_env["CLOUDSDK_PYTHON"] = bundled_python_path

    install = run(
        [gcloud_path, "components", "install", "gke-gcloud-auth-plugin", "--quiet"],
        env=plugin_env,
        timeout=1800,
    )
    payload["gcloud_plugin_install"] = {
        "returncode": install.returncode,
        "stdout": install.stdout[-4000:],
        "stderr": install.stderr[-4000:],
    }
    plugin_path = find_gke_plugin()
    if install.returncode == 0 and plugin_path:
        payload["gke_gcloud_auth_plugin_path"] = plugin_path
        payload["completed_steps"].append("gke_gcloud_auth_plugin_installed")
        return
    payload["blockers"].append("The gke-gcloud-auth-plugin component is still unavailable after the bounded install attempt.")


def write_outputs(payload: dict[str, Any], output_json: Path, output_md: Path) -> None:
    write_json(output_json, payload)
    lines = [
        "# V38 Windows Operator Proof",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Operator lane state: `{payload['windows_operator_lane_state']}`",
        f"- Gcloud path: `{payload.get('gcloud_path', '') or 'missing'}`",
        f"- GKE auth plugin path: `{payload.get('gke_gcloud_auth_plugin_path', '') or 'missing'}`",
        "",
        "## Base Tools",
        "",
    ]
    for row in payload.get("base_tools", []):
        lines.append(f"- `{row['name']}`: `{row['path'] or 'missing'}`")
    lines.extend(["", "## Completed Steps", ""])
    lines.extend([f"- `{step}`" for step in payload.get("completed_steps", [])])
    if payload.get("blockers"):
        lines.extend(["", "## Blockers", ""])
        lines.extend([f"- {row}" for row in payload["blockers"]])
    write_text(output_md, "\n".join(lines) + "\n")


def ensure_gcloud(payload: dict[str, Any], *, bootstrap: bool) -> str:
    gcloud_path = find_gcloud()
    if gcloud_path:
        payload["completed_steps"].append("gcloud_detected")
        return gcloud_path
    if not bootstrap:
        payload["blockers"].append("gcloud is missing and bootstrap was not requested.")
        return ""

    payload["install_attempts"] = []
    if shutil.which("winget"):
        winget = run(WINGET_ARGS, timeout=3600)
        payload["install_attempts"].append(
            {
                "tool": "winget",
                "returncode": winget.returncode,
                "stdout": winget.stdout[-3000:],
                "stderr": winget.stderr[-3000:],
            }
        )
        gcloud_path = find_gcloud()
        if gcloud_path:
            payload["completed_steps"].append("gcloud_installed_via_winget")
            return gcloud_path

    if shutil.which("choco"):
        choco = run(CHOCO_ARGS, timeout=3600)
        payload["install_attempts"].append(
            {
                "tool": "choco",
                "returncode": choco.returncode,
                "stdout": choco.stdout[-3000:],
                "stderr": choco.stderr[-3000:],
            }
        )
        gcloud_path = find_gcloud()
        if gcloud_path:
            payload["completed_steps"].append("gcloud_installed_via_choco")
            return gcloud_path

    payload["blockers"].append("gcloud remained unavailable after the bounded Windows bootstrap attempts.")
    return ""


def probe_gcloud(gcloud_path: str, env: dict[str, str], payload: dict[str, Any]) -> None:
    version = run([gcloud_path, "--version"], env=env, timeout=120)
    payload["gcloud_version"] = {
        "returncode": version.returncode,
        "stdout": version.stdout[-2000:],
        "stderr": version.stderr[-1200:],
    }
    if version.returncode == 0:
        payload["completed_steps"].append("gcloud_version_verified")
    else:
        payload["blockers"].append("gcloud exists but `gcloud --version` did not complete cleanly.")


def ensure_operator_lane(bundle: str, *, bootstrap: bool = True) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": "v38_omega",
        "overall_status": "WARN",
        "windows_operator_lane_state": "pending",
        "completed_steps": [],
        "blockers": [],
        "base_tools": [command_status(name) for name in REQUIRED_BASE_TOOLS],
    }

    missing = [row["name"] for row in payload["base_tools"] if not row["present"]]
    if missing:
        payload["blockers"].append(f"Required Windows tools are missing: {', '.join(missing)}.")

    gcloud_path = ensure_gcloud(payload, bootstrap=bootstrap)
    payload["gcloud_path"] = gcloud_path
    if not gcloud_path:
        payload["windows_operator_lane_state"] = "blocked_gcloud_missing"
        payload["overall_status"] = "FAIL"
        return payload

    env = build_gcloud_env()
    probe_gcloud(gcloud_path, env, payload)
    activate_service_account(gcloud_path, env, payload, bundle)
    ensure_plugin(gcloud_path, env, payload)

    if payload["blockers"]:
        payload["windows_operator_lane_state"] = (
            "gcloud_ready_plugin_blocked"
            if gcloud_path and payload.get("gcloud_auth", {}).get("returncode") == 0
            else "blocked_operator_bootstrap"
        )
        payload["overall_status"] = "FAIL"
        return payload

    payload["windows_operator_lane_state"] = "gcloud_ready"
    payload["overall_status"] = "PASS"
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify or bootstrap the Windows operator lane for V38.")
    parser.add_argument("--bundle", default=str(Path.home() / "GCP service account keys.txt"))
    parser.add_argument("--no-bootstrap", action="store_true")
    parser.add_argument("--output-json", default=str(OUTPUT_JSON))
    parser.add_argument("--output-md", default=str(OUTPUT_MD))
    args = parser.parse_args()

    payload = ensure_operator_lane(args.bundle, bootstrap=not args.no_bootstrap)
    write_outputs(payload, Path(args.output_json), Path(args.output_md))
    return 0 if payload["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
