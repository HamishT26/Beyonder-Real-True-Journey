#!/usr/bin/env python3
"""Shared helpers for V32 cloud, connector, and closeout scripts."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from google.auth.transport.requests import Request
from google.oauth2 import service_account

ROOT = Path(__file__).resolve().parent.parent
LOCAL_RUNTIME = ROOT / ".local-runtime"
DEFAULT_GCP_KEY_BUNDLE = Path.home() / "GCP service account keys.txt"
DEFAULT_ENV_CANDIDATES = [
    Path.home() / ".env file.txt",
    Path.home() / "OneDrive" / ".env file.txt",
]
PROJECT_ID = "gen-lang-client-0020882673"
PRIMARY_REGION = "australia-southeast1"
PRIMARY_CLUSTER = "beyonder-v32-autopilot-dev"
PRIMARY_NAMESPACE = "v32-omega"
ARTIFACT_REPOSITORY = "beyonder-v32"
PRIMARY_BUCKET_PREFIX = f"beyonder-v32-primary-mirror-{PROJECT_ID}"
DEFAULT_SECRET_IDS = [
    "beyonder-v32-runtime-config",
    "beyonder-v32-connector-config",
    "beyonder-v32-cloud-bootstrap",
]
KUBECTL_FALLBACK = Path(r"C:\Program Files\Docker\Docker\resources\bin\kubectl.exe")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def load_env_values() -> dict[str, str]:
    values: dict[str, str] = {}
    for path in DEFAULT_ENV_CANDIDATES:
        if not path.exists():
            continue
        for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
            stripped = raw.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            key, value = stripped.split("=", 1)
            parsed = value.strip()
            if len(parsed) >= 2 and parsed[0] == parsed[-1] and parsed[0] in "\"'":
                parsed = parsed[1:-1]
            values[key.strip()] = parsed
    for key, value in os.environ.items():
        if key not in values:
            values[key] = value
    return values


def mask_email(value: str) -> str:
    if "@" not in value:
        return value[:2] + "***"
    local, domain = value.split("@", 1)
    masked_local = f"{local[:1]}***" if local else "***"
    masked_domain = f"{domain[:1]}***" if domain else "***"
    return f"{masked_local}@{masked_domain}"


def repo_rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def run_cmd(args: list[str], timeout: int = 30) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            args,
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout if isinstance(exc.stdout, str) else (exc.stdout or b"").decode("utf-8", errors="replace")
        stderr = exc.stderr if isinstance(exc.stderr, str) else (exc.stderr or b"").decode("utf-8", errors="replace")
        return subprocess.CompletedProcess(
            args=args,
            returncode=124,
            stdout=stdout or "",
            stderr=(stderr or "") + f"\ncommand timed out after {timeout} seconds",
        )


def windows_kubectl() -> str:
    resolved = shutil.which("kubectl")
    if resolved:
        return resolved
    if KUBECTL_FALLBACK.exists():
        return str(KUBECTL_FALLBACK)
    return ""


def wsl_probe() -> dict[str, Any]:
    status = run_cmd(["wsl.exe", "--status"], timeout=10)
    listing = run_cmd(["wsl.exe", "-l", "-v"], timeout=10)
    smoke = run_cmd(
        ["wsl.exe", "-d", "Ubuntu", "-e", "sh", "-lc", "echo WSL_READY"],
        timeout=15,
    )
    if smoke.returncode == 0 and "WSL_READY" in (smoke.stdout or ""):
        readiness = "ubuntu_shell_ready"
    elif smoke.returncode == 124:
        readiness = "ubuntu_launch_timeout"
    else:
        readiness = "ubuntu_launch_failed"
    return {
        "status_returncode": status.returncode,
        "status_stdout": (status.stdout or "").strip(),
        "status_stderr": (status.stderr or "").strip(),
        "list_returncode": listing.returncode,
        "list_stdout": (listing.stdout or "").strip(),
        "list_stderr": (listing.stderr or "").strip(),
        "smoke_returncode": smoke.returncode,
        "smoke_stdout": (smoke.stdout or "").strip(),
        "smoke_stderr": (smoke.stderr or "").strip(),
        "readiness": readiness,
    }


def _parse_json_objects(raw: str) -> list[dict[str, Any]]:
    decoder = json.JSONDecoder()
    index = 0
    objects: list[dict[str, Any]] = []
    text = raw.strip()
    while index < len(text):
        while index < len(text) and text[index].isspace():
            index += 1
        if index >= len(text):
            break
        try:
            obj, end = decoder.raw_decode(text, index)
        except json.JSONDecodeError:
            index += 1
            continue
        if isinstance(obj, dict):
            objects.append(obj)
        index = end
    return objects


def service_account_alias(info: dict[str, Any]) -> str:
    email = str(info.get("client_email", "")).lower()
    if email.endswith("compute@developer.gserviceaccount.com"):
        return "compute_default"
    if email.endswith("@appspot.gserviceaccount.com"):
        return "app_engine_default"
    if "beyonder-real-journey-1@" in email:
        return "beyonder_real_journey_1"
    safe = email.replace("@", "_at_").replace(".", "_").replace("-", "_")
    return safe or "service_account"


def load_gcp_service_accounts(bundle_path: Path = DEFAULT_GCP_KEY_BUNDLE) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    runtime_dir = LOCAL_RUNTIME / "gcp-service-accounts"
    runtime_dir.mkdir(parents=True, exist_ok=True)
    if not bundle_path.exists():
        return {"bundle_path": str(bundle_path), "runtime_dir": str(runtime_dir), "records": records}
    payloads = _parse_json_objects(bundle_path.read_text(encoding="utf-8", errors="replace"))
    for info in payloads:
        if info.get("type") != "service_account" or not info.get("client_email"):
            continue
        alias = service_account_alias(info)
        runtime_path = runtime_dir / f"{alias}.json"
        runtime_path.write_text(json.dumps(info, indent=2) + "\n", encoding="utf-8")
        records.append(
            {
                "alias": alias,
                "client_email": str(info["client_email"]),
                "project_id": str(info.get("project_id") or PROJECT_ID),
                "private_key_id": str(info.get("private_key_id", "")),
                "runtime_path": runtime_path,
                "info": info,
            }
        )
    return {"bundle_path": str(bundle_path), "runtime_dir": str(runtime_dir), "records": records}


def mint_access_token(info: dict[str, Any], scopes: list[str] | None = None) -> dict[str, Any]:
    scope_list = scopes or ["https://www.googleapis.com/auth/cloud-platform"]
    credentials = service_account.Credentials.from_service_account_info(info, scopes=scope_list)
    credentials.refresh(Request())
    expiry = credentials.expiry.astimezone(timezone.utc).replace(microsecond=0).isoformat() if credentials.expiry else ""
    return {
        "token": credentials.token or "",
        "expiry_utc": expiry,
        "scopes": scope_list,
    }


def google_request(
    method: str,
    url: str,
    token: str,
    *,
    body: dict[str, Any] | None = None,
    raw_body: bytes | None = None,
    headers: dict[str, str] | None = None,
    timeout: int = 60,
) -> dict[str, Any]:
    req_headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    if headers:
        req_headers.update(headers)
    data = raw_body
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        req_headers.setdefault("Content-Type", "application/json")
    request = urllib.request.Request(url, data=data, headers=req_headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            content = response.read()
            text = content.decode("utf-8", errors="replace")
            try:
                parsed = json.loads(text) if text else {}
            except json.JSONDecodeError:
                parsed = {"raw_body": text}
            return {
                "status": response.status,
                "body_text": text,
                "parsed": parsed,
                "headers": dict(response.headers.items()),
            }
    except urllib.error.HTTPError as exc:
        content = exc.read()
        text = content.decode("utf-8", errors="replace")
        try:
            parsed = json.loads(text) if text else {}
        except json.JSONDecodeError:
            parsed = {"raw_body": text}
        return {
            "status": exc.code,
            "body_text": text,
            "parsed": parsed,
            "headers": dict(exc.headers.items()) if exc.headers else {},
        }
    except urllib.error.URLError as exc:
        return {
            "status": 0,
            "body_text": "",
            "parsed": {"error": str(exc)},
            "headers": {},
        }


def refresh_oauth_token(refresh_token: str, client_id: str, client_secret: str) -> dict[str, Any]:
    payload = urllib.parse.urlencode(
        {
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        "https://oauth2.googleapis.com/token",
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
            return {"status": response.status, "parsed": data}
    except urllib.error.HTTPError as exc:
        text = exc.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            parsed = {"raw_body": text}
        return {"status": exc.code, "parsed": parsed}


def temp_kubeconfig(server: str, ca_data_b64: str, token: str, namespace: str = PRIMARY_NAMESPACE) -> Path:
    runtime_dir = LOCAL_RUNTIME / "kube"
    runtime_dir.mkdir(parents=True, exist_ok=True)
    path = runtime_dir / "v32-kubeconfig.yaml"
    content = "\n".join(
        [
            "apiVersion: v1",
            "kind: Config",
            "clusters:",
            "- cluster:",
            f"    certificate-authority-data: {ca_data_b64}",
            f"    server: https://{server}",
            "  name: v32-gke",
            "contexts:",
            "- context:",
            "    cluster: v32-gke",
            f"    namespace: {namespace}",
            "    user: v32-token-user",
            "  name: v32-gke",
            f"current-context: v32-gke",
            "users:",
            "- name: v32-token-user",
            "  user:",
            f"    token: {token}",
            "",
        ]
    )
    path.write_text(content, encoding="utf-8")
    return path


def temp_file(prefix: str, suffix: str, content: str) -> Path:
    runtime_dir = LOCAL_RUNTIME / "temp"
    runtime_dir.mkdir(parents=True, exist_ok=True)
    fd, raw_path = tempfile.mkstemp(prefix=prefix, suffix=suffix, dir=runtime_dir)
    os.close(fd)
    path = Path(raw_path)
    path.write_text(content, encoding="utf-8")
    return path
