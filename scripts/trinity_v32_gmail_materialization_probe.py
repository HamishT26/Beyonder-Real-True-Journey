#!/usr/bin/env python3
"""V32 Gmail scope-first materialization proof using the direct Google API fallback."""

from __future__ import annotations

import base64
import json
import time
from datetime import datetime, timezone
from email.mime.text import MIMEText
from pathlib import Path
from typing import Any

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from trinity_v32_runtime_common import (
    load_env_values,
    mask_email,
    now_iso,
    refresh_oauth_token,
    write_json,
    write_text,
)

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v32-gmail-materialization-proof-v1.json"
OUTPUT_MD = ROOT / "docs" / "trinity-live-traces" / "v32-gmail-materialization-proof-v1.md"
REQUIRED_SCOPE_HINTS = {
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
}


def message_raw(to_addr: str, subject: str, body: str) -> dict[str, str]:
    message = MIMEText(body)
    message["to"] = to_addr
    message["from"] = to_addr
    message["subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    return {"raw": raw}


def gmail_service(values: dict[str, str]):
    creds = Credentials(
        None,
        refresh_token=values.get("GOOGLE_REFRESH_TOKEN"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=values.get("GOOGLE_CLIENT_ID"),
        client_secret=values.get("GOOGLE_CLIENT_SECRET"),
        scopes=["https://www.googleapis.com/auth/gmail.modify"],
    )
    return build("gmail", "v1", credentials=creds)


def write_outputs(payload: dict[str, Any]) -> None:
    write_json(OUTPUT_JSON, payload)
    lines = [
        "# V32 Gmail Materialization Proof",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Proof state: `{payload['proof_state']}`",
        f"- Gmail scope state: `{payload.get('gmail_scope_state', 'unknown')}`",
        f"- Path used: `{payload['path_used']}`",
        "",
        "## Steps",
        "",
    ]
    for step in payload.get("completed_steps", []):
        lines.append(f"- Completed: `{step}`")
    for step in payload.get("pending_steps", []):
        lines.append(f"- Pending: `{step}`")
    if payload.get("blocker_code"):
        lines.extend(["", "## Blocker", "", f"- `{payload['blocker_code']}`"])
    write_text(OUTPUT_MD, "\n".join(lines) + "\n")


def main() -> int:
    values = load_env_values()
    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": "v32_omega",
        "overall_status": "WARN",
        "status": "WARN",
        "proof_state": "open_with_blocker",
        "gmail_scope_state": "pending",
        "connector_native_attempted": False,
        "connector_tools_available": False,
        "path_used": "direct_google_api_fallback",
        "attempted_steps": [
            "connector_native_gmail_tools",
            "scope_preflight",
            "google_api_inbox_read",
            "google_api_draft_create",
            "google_api_send_to_self",
            "google_api_readback",
        ],
        "completed_steps": [],
        "pending_steps": [
            "scope_preflight",
            "inbox_read",
            "draft_creation",
            "send_to_self",
            "readback_verification",
        ],
        "notes": [
            "Connector-native Gmail tools are still unavailable in-session, so V32 uses the direct Google API fallback.",
            "V32 adds a scope preflight so Gmail auth blockers are published explicitly before message operations begin.",
        ],
    }

    required = ["GOOGLE_REFRESH_TOKEN", "GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET"]
    missing = [key for key in required if not values.get(key)]
    if missing:
        payload["blocker_code"] = "missing_google_gmail_credentials"
        write_outputs(payload)
        return 1

    token_refresh = refresh_oauth_token(
        values["GOOGLE_REFRESH_TOKEN"],
        values["GOOGLE_CLIENT_ID"],
        values["GOOGLE_CLIENT_SECRET"],
    )
    payload["token_refresh_status"] = token_refresh["status"]
    granted_scopes = set(str(token_refresh.get("parsed", {}).get("scope", "")).split())
    payload["granted_scopes"] = sorted(scope for scope in granted_scopes if scope)
    if granted_scopes and not (granted_scopes & REQUIRED_SCOPE_HINTS):
        payload["gmail_scope_state"] = "missing_required_scope"
        payload["blocker_code"] = "google_refresh_token_missing_gmail_scope"
        write_outputs(payload)
        return 1
    if token_refresh["status"] != 200:
        payload["gmail_scope_state"] = "refresh_failed"
        payload["blocker_code"] = "google_refresh_failed"
        write_outputs(payload)
        return 1

    payload["gmail_scope_state"] = "scope_refresh_succeeded"
    payload["completed_steps"].append("scope_preflight")
    payload["pending_steps"].remove("scope_preflight")

    try:
        service = gmail_service(values)
        profile = service.users().getProfile(userId="me").execute()
        mailbox = str(profile.get("emailAddress", ""))
        payload["mailbox_masked"] = mask_email(mailbox)

        inbox = service.users().messages().list(userId="me", labelIds=["INBOX"], maxResults=5).execute()
        payload["completed_steps"].append("inbox_read")
        payload["pending_steps"].remove("inbox_read")
        payload["inbox_message_count_sample"] = len(inbox.get("messages", []))

        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        subject = f"[V32 TEST] Trinity Gmail Materialization {stamp}"
        body = (
            "This is a bounded V32 Gmail materialization test message.\n\n"
            "Proof path: scope preflight -> inbox read -> draft creation -> send-to-self -> read-back verification."
        )
        raw = message_raw(mailbox, subject, body)
        draft = service.users().drafts().create(userId="me", body={"message": raw}).execute()
        payload["completed_steps"].append("draft_creation")
        payload["pending_steps"].remove("draft_creation")
        payload["draft_id"] = draft.get("id")
        payload["test_subject"] = subject

        sent = service.users().messages().send(userId="me", body=raw).execute()
        payload["completed_steps"].append("send_to_self")
        payload["pending_steps"].remove("send_to_self")
        payload["sent_message_id"] = sent.get("id")

        readback = None
        for _ in range(12):
            result = service.users().messages().list(
                userId="me",
                q=f'in:inbox subject:"{subject}" newer_than:1d',
                maxResults=5,
            ).execute()
            messages = result.get("messages", [])
            if messages:
                readback = messages[0]
                break
            time.sleep(5)

        if readback is None:
            payload["gmail_scope_state"] = "scope_refresh_succeeded"
            payload["blocker_code"] = "gmail_readback_not_found"
            write_outputs(payload)
            return 1

        meta = service.users().messages().get(
            userId="me",
            id=readback["id"],
            format="metadata",
            metadataHeaders=["Subject", "To", "From"],
        ).execute()
        payload["completed_steps"].append("readback_verification")
        payload["pending_steps"].remove("readback_verification")
        payload["readback_message_id"] = meta.get("id")
        payload["readback_thread_id"] = meta.get("threadId")
        payload["overall_status"] = "PASS"
        payload["status"] = "PASS"
        payload["proof_state"] = "bounded_live_write"
        payload["gmail_scope_state"] = "required_scope_verified"
        payload["gmail_materialization_state"] = "bounded_live_write"
        write_outputs(payload)
        return 0
    except HttpError as exc:
        payload["gmail_scope_state"] = "api_http_error"
        payload["blocker_code"] = "gmail_api_http_error"
        payload["http_status"] = getattr(getattr(exc, "resp", None), "status", None)
        payload["error_message"] = str(exc)
        write_outputs(payload)
        return 1
    except Exception as exc:  # pragma: no cover - external auth/API behavior
        error_message = str(exc)
        payload["error_message"] = error_message
        payload["gmail_scope_state"] = "runtime_blocked"
        payload["blocker_code"] = (
            "google_refresh_token_missing_gmail_scope"
            if "invalid_scope" in error_message.lower()
            else "gmail_api_runtime_error"
        )
        write_outputs(payload)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
