#!/usr/bin/env python3
"""V31 Gmail proof using a direct Google API fallback when connector-native tools are unavailable."""

from __future__ import annotations

import base64
import json
import os
import time
from datetime import datetime, timezone
from email.mime.text import MIMEText
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v31-gmail-materialization-proof-v1.json"
OUTPUT_MD = ROOT / "docs" / "trinity-live-traces" / "v31-gmail-materialization-proof-v1.md"
ENV_CANDIDATES = [
    Path.home() / ".env file.txt",
    Path.home() / "OneDrive" / ".env file.txt",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def mask_email(value: str) -> str:
    if "@" not in value:
        return value[:2] + "***"
    local, domain = value.split("@", 1)
    masked_local = (local[:1] + "***") if local else "***"
    masked_domain = domain[:1] + "***"
    return f"{masked_local}@{masked_domain}"


def load_env() -> None:
    for path in ENV_CANDIDATES:
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            key, value = stripped.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and value and key not in os.environ:
                os.environ[key] = value


def gmail_service():
    creds = Credentials(
        None,
        refresh_token=os.environ.get("GOOGLE_REFRESH_TOKEN"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ.get("GOOGLE_CLIENT_ID"),
        client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
        scopes=["https://www.googleapis.com/auth/gmail.modify"],
    )
    return build("gmail", "v1", credentials=creds)


def message_raw(to_addr: str, subject: str, body: str) -> dict[str, str]:
    message = MIMEText(body)
    message["to"] = to_addr
    message["from"] = to_addr
    message["subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    return {"raw": raw}


def write_outputs(payload: dict[str, object]) -> None:
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# V31 Gmail Materialization Proof",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Proof state: `{payload['proof_state']}`",
        f"- Mailbox: `{payload.get('mailbox_masked', 'unknown')}`",
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
    lines.append("")
    OUTPUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    load_env()
    payload: dict[str, object] = {
        "generated_utc": now_iso(),
        "phase": "v31_omega",
        "overall_status": "WARN",
        "status": "WARN",
        "proof_state": "open_with_blocker",
        "connector_native_required": False,
        "connector_tools_available": False,
        "path_used": "direct_google_api_fallback",
        "attempted_steps": [
            "connector_native_gmail_tools",
            "google_api_inbox_read",
            "google_api_draft_create",
            "google_api_send_to_self",
            "google_api_readback",
        ],
        "completed_steps": [],
        "pending_steps": [
            "inbox_read",
            "draft_creation",
            "send_to_self",
            "readback_verification",
        ],
        "notes": [
            "V31 allows a direct Google API fallback because no connector-native Gmail action surface was callable in-session.",
            "This proof is limited to inbox read, draft creation, one send-to-self test, and read-back verification.",
        ],
    }

    required = ["GOOGLE_REFRESH_TOKEN", "GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET"]
    missing = [key for key in required if not os.environ.get(key)]
    if missing:
        payload["blocker_code"] = "missing_google_gmail_credentials"
        payload["notes"].append("Required Google refresh-token credential material was not available in the current environment.")
        write_outputs(payload)
        return 1

    try:
        service = gmail_service()
        profile = service.users().getProfile(userId="me").execute()
        mailbox = str(profile.get("emailAddress", ""))
        payload["mailbox_masked"] = mask_email(mailbox)

        inbox = service.users().messages().list(
            userId="me",
            labelIds=["INBOX"],
            maxResults=5,
        ).execute()
        payload["completed_steps"].append("inbox_read")
        payload["pending_steps"].remove("inbox_read")
        payload["inbox_message_count_sample"] = len(inbox.get("messages", []))

        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        subject = f"[V31 TEST] Trinity Gmail Materialization {stamp}"
        body = (
            "This is a bounded V31 Gmail materialization test message.\n\n"
            "Proof path: inbox read -> draft creation -> send-to-self -> read-back verification."
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
            payload["blocker_code"] = "gmail_readback_not_found"
            payload["notes"].append("The self-addressed test message was sent but did not appear in the inbox within the polling window.")
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
        payload["gmail_materialization_state"] = "bounded_live_write"
        payload["notes"].append("The Gmail fallback proof completed successfully using the direct Google API path.")
        write_outputs(payload)
        return 0
    except HttpError as exc:
        payload["blocker_code"] = "gmail_api_http_error"
        payload["http_status"] = getattr(getattr(exc, "resp", None), "status", None)
        payload["error_message"] = str(exc)
        payload["notes"].append("The Gmail API fallback path failed with an HTTP error.")
        write_outputs(payload)
        return 1
    except Exception as exc:  # pragma: no cover - external credential and API handling
        error_message = str(exc)
        payload["error_message"] = error_message
        if "invalid_scope" in error_message.lower():
            payload["blocker_code"] = "google_refresh_token_missing_gmail_scope"
            payload["notes"].append("The available Google refresh token is valid for other Google surfaces but does not carry a usable Gmail scope.")
        else:
            payload["blocker_code"] = "gmail_api_runtime_error"
        payload["notes"].append("The Gmail API fallback path failed before proof completion.")
        write_outputs(payload)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
