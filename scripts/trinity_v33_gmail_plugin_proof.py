#!/usr/bin/env python3
"""Write the bounded V33 Gmail connector proof from in-session plugin results."""

from __future__ import annotations

import argparse
from pathlib import Path

from trinity_v32_runtime_common import now_iso, write_json, write_text

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v33-gmail-plugin-proof-v1.json"
OUTPUT_MD = ROOT / "docs" / "trinity-live-traces" / "v33-gmail-plugin-proof-v1.md"


def main() -> int:
    parser = argparse.ArgumentParser(description="Record the V33 Gmail plugin proof.")
    parser.add_argument("--profile-email", required=True)
    parser.add_argument("--search-query", required=True)
    parser.add_argument("--search-count", type=int, default=0)
    parser.add_argument("--draft-id", default="")
    parser.add_argument("--sent-message-id", default="")
    parser.add_argument("--readback-message-id", default="")
    parser.add_argument("--subject", default="")
    parser.add_argument("--status", choices=["pass", "warn"], default="pass")
    args = parser.parse_args()

    draft_created = bool(args.draft_id)
    send_verified = bool(args.sent_message_id)
    readback_verified = bool(args.readback_message_id)
    if draft_created and send_verified and readback_verified and args.status == "pass":
        gmail_state = "bounded_live_write"
        overall_status = "PASS"
        proof_state = "connector_live_write_verified"
    else:
        gmail_state = "read_verified_write_blocked"
        overall_status = "WARN"
        proof_state = "connector_read_verified_write_blocked"

    payload = {
        "generated_utc": now_iso(),
        "phase": "v33_omega",
        "overall_status": overall_status,
        "proof_state": proof_state,
        "gmail_connector_state": gmail_state,
        "profile_email": args.profile_email,
        "search_query": args.search_query,
        "search_count": args.search_count,
        "draft_created": draft_created,
        "send_verified": send_verified,
        "readback_verified": readback_verified,
        "draft_id": args.draft_id,
        "sent_message_id": args.sent_message_id,
        "readback_message_id": args.readback_message_id,
        "subject": args.subject,
        "path_used": "gmail_plugin_connector_native",
        "notes": [
            "V33 uses the connected Gmail plugin as the primary Gmail lane.",
            "This artifact records connector-native read, draft, send, and read-back results.",
        ],
        "blockers": [] if overall_status == "PASS" else ["Connector-native Gmail read succeeded, but draft/send/read-back did not fully complete."],
    }
    write_json(OUTPUT_JSON, payload)

    lines = [
        "# V33 Gmail Plugin Proof",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Proof state: `{payload['proof_state']}`",
        f"- Gmail connector state: `{payload['gmail_connector_state']}`",
        f"- Profile email: `{payload['profile_email']}`",
        f"- Search query: `{payload['search_query']}`",
        f"- Search result count: `{payload['search_count']}`",
        f"- Draft ID: `{payload['draft_id'] or 'missing'}`",
        f"- Sent message ID: `{payload['sent_message_id'] or 'missing'}`",
        f"- Readback message ID: `{payload['readback_message_id'] or 'missing'}`",
    ]
    if payload["blockers"]:
        lines.extend(["", "## Blockers", ""])
        for blocker in payload["blockers"]:
            lines.append(f"- {blocker}")
    write_text(OUTPUT_MD, "\n".join(lines) + "\n")
    return 0 if overall_status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
