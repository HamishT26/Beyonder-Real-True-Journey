#!/usr/bin/env python3
"""Run a bounded Google Drive working-mirror proof for Trinity surfaces."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
from typing import Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ENV_FILE = Path.home() / ".env file.txt"
DEFAULT_CLIENT_SECRET = Path.home() / ".codex" / "secrets" / "google-drive-mcp" / "gcp-oauth.keys.json"
DEFAULT_OUT = ROOT / "docs" / "trinity-live-traces" / "google-drive-working-mirror-proof-v1.json"
SCOPES = ["https://www.googleapis.com/auth/drive"]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_env_file(path: Path) -> tuple[list[str], dict[str, str]]:
    rows: list[str] = []
    values: dict[str, str] = {}
    if not path.exists():
        return rows, values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip("\n")
        rows.append(line)
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        parsed = value.strip()
        if len(parsed) >= 2 and ((parsed[0] == parsed[-1] == '"') or (parsed[0] == parsed[-1] == "'")):
            parsed = parsed[1:-1]
        values[key.strip()] = parsed
    return rows, values


def persist_refresh_token(path: Path, rows: list[str], refresh_token: str) -> None:
    output: list[str] = []
    replaced = False
    for row in rows:
        stripped = row.strip()
        if stripped.startswith("GOOGLE_REFRESH_TOKEN="):
            output.append(f"GOOGLE_REFRESH_TOKEN={refresh_token}")
            replaced = True
        else:
            output.append(row)
    if not replaced:
        output.append(f"GOOGLE_REFRESH_TOKEN={refresh_token}")
    path.write_text("\n".join(output) + "\n", encoding="utf-8")


def load_client_config(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    installed = payload.get("installed")
    if not isinstance(installed, dict):
        raise ValueError(f"installed app config missing in {path}")
    return installed


def build_credentials(env_values: dict[str, str], client_config: dict[str, Any]) -> Credentials | None:
    refresh_token = env_values.get("GOOGLE_REFRESH_TOKEN", "").strip()
    if not refresh_token:
        return None
    return Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri=str(client_config["token_uri"]),
        client_id=str(client_config["client_id"]),
        client_secret=str(client_config["client_secret"]),
        scopes=SCOPES,
    )


def interactive_credentials(client_secret_file: Path) -> Credentials:
    flow = InstalledAppFlow.from_client_secrets_file(str(client_secret_file), SCOPES)
    return flow.run_local_server(
        host="localhost",
        port=0,
        open_browser=True,
        authorization_prompt_message="Please authorize Google Drive access in the opened browser window.",
        success_message="Google Drive authorization captured. You can close this window and return to Codex.",
        access_type="offline",
        prompt="consent",
    )


def ensure_credentials(
    *,
    env_file: Path,
    env_rows: list[str],
    env_values: dict[str, str],
    client_secret_file: Path,
    interactive_auth: bool,
    persist_token: bool,
) -> tuple[Credentials, str, bool]:
    client_config = load_client_config(client_secret_file)
    creds = build_credentials(env_values, client_config)
    if creds is not None:
        try:
            creds.refresh(Request())
            return creds, "refresh_token", False
        except Exception:
            if not interactive_auth:
                raise
    if not interactive_auth:
        raise RuntimeError("interactive auth disabled and refresh-token path failed")
    creds = interactive_credentials(client_secret_file)
    if persist_token and creds.refresh_token:
        persist_refresh_token(env_file, env_rows, creds.refresh_token)
        return creds, "interactive_refresh_token", True
    return creds, "interactive_access_token_only", False


def resolve_folder(service: Any, folder_name: str, fallback_file_name: str) -> tuple[dict[str, Any], str]:
    folder_name_escaped = folder_name.replace("'", "\\'")
    folder_query = (
        "mimeType='application/vnd.google-apps.folder' and trashed=false and "
        f"name='{folder_name_escaped}'"
    )
    folder_resp = service.files().list(
        q=folder_query,
        fields="files(id,name,modifiedTime,parents,webViewLink)",
        orderBy="modifiedTime desc",
        pageSize=10,
    ).execute()
    folders = folder_resp.get("files", [])
    if folders:
        return folders[0], "exact_folder_name"

    fallback_name_escaped = fallback_file_name.replace("'", "\\'")
    fallback_query = f"trashed=false and name='{fallback_name_escaped}'"
    fallback_resp = service.files().list(
        q=fallback_query,
        fields="files(id,name,parents,modifiedTime,webViewLink)",
        orderBy="modifiedTime desc",
        pageSize=5,
    ).execute()
    files = fallback_resp.get("files", [])
    if not files:
        raise RuntimeError(f"unable to resolve folder '{folder_name}' or fallback file '{fallback_file_name}'")
    parents = files[0].get("parents") or []
    if not parents:
        raise RuntimeError(f"fallback file '{fallback_file_name}' has no parent folder metadata")
    folder = service.files().get(
        fileId=parents[0],
        fields="id,name,modifiedTime,parents,webViewLink",
    ).execute()
    return folder, "fallback_file_parent"


def upload_and_readback(service: Any, folder: dict[str, Any], label: str) -> dict[str, Any]:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    content = (
        "# Trinity Google Drive Working-Mirror Proof\n\n"
        f"- generated_utc: {now_iso()}\n"
        f"- proof_label: {label}\n"
        "- purpose: bounded working mirror disposable artifact\n"
    )
    media = MediaIoBaseUpload(BytesIO(content.encode("utf-8")), mimetype="text/markdown", resumable=False)
    body = {"name": f"{label}-{stamp}.md", "parents": [folder["id"]]}
    created = service.files().create(
        body=body,
        media_body=media,
        fields="id,name,parents,webViewLink,webContentLink,mimeType,size",
    ).execute()
    fetched = service.files().get(
        fileId=created["id"],
        fields="id,name,parents,webViewLink,webContentLink,mimeType,size",
    ).execute()
    fetched_bytes = service.files().get_media(fileId=created["id"]).execute()
    fetched_text = fetched_bytes.decode("utf-8")
    return {
        "artifact_id": created["id"],
        "artifact_name": created["name"],
        "artifact_url": created.get("webViewLink", ""),
        "artifact_download_url": created.get("webContentLink", ""),
        "artifact_size": fetched.get("size"),
        "artifact_content_matches": fetched_text == content,
        "artifact_parent_ids": fetched.get("parents", []),
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a bounded Google Drive working-mirror proof.")
    parser.add_argument("--env-file", default=str(DEFAULT_ENV_FILE))
    parser.add_argument("--client-secret-file", default=str(DEFAULT_CLIENT_SECRET))
    parser.add_argument("--folder-name", default="Project Vision")
    parser.add_argument("--fallback-file-name", default="trinity_os_architecture.md")
    parser.add_argument("--label", default="v27-drive-proof")
    parser.add_argument("--interactive-auth", action="store_true")
    parser.add_argument("--persist-refresh-token", action="store_true")
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    args = parser.parse_args()

    env_file = Path(args.env_file)
    client_secret_file = Path(args.client_secret_file)
    out_path = Path(args.out)

    env_rows, env_values = load_env_file(env_file)
    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "overall_status": "PASS",
        "proof_state": "pending",
        "folder_name_requested": args.folder_name,
        "fallback_file_name": args.fallback_file_name,
        "refresh_token_present_before_run": bool(env_values.get("GOOGLE_REFRESH_TOKEN", "").strip()),
    }

    try:
        creds, auth_mode, refresh_persisted = ensure_credentials(
            env_file=env_file,
            env_rows=env_rows,
            env_values=env_values,
            client_secret_file=client_secret_file,
            interactive_auth=args.interactive_auth,
            persist_token=args.persist_refresh_token,
        )
        service = build("drive", "v3", credentials=creds)
        folder, resolution = resolve_folder(service, args.folder_name, args.fallback_file_name)
        artifact = upload_and_readback(service, folder, args.label)
        payload.update(
            {
                "proof_state": "working_mirror_verified",
                "auth_mode": auth_mode,
                "refresh_token_persisted": refresh_persisted,
                "folder_resolution": resolution,
                "folder_id": folder["id"],
                "folder_name": folder["name"],
                "folder_url": folder.get("webViewLink", ""),
                **artifact,
                "blockers": [],
            }
        )
    except Exception as exc:
        payload.update(
            {
                "overall_status": "WARN",
                "proof_state": "blocked",
                "blockers": [str(exc)],
            }
        )

    write_json(out_path, payload)
    print(json.dumps({"overall_status": payload["overall_status"], "proof_state": payload["proof_state"], "out": str(out_path)}))
    return 0 if payload["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
