#!/usr/bin/env python3
"""Redact app thread identifiers from curated app-lane JSON receipts."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


THREAD_ID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE)
REDACTED = "<redacted_app_thread_id>"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def redact_value(value: Any) -> tuple[Any, int]:
    if isinstance(value, dict):
        redactions = 0
        result: dict[str, Any] = {}
        for key, item in value.items():
            if key == "thread_id" and isinstance(item, str) and item != REDACTED:
                if THREAD_ID_RE.match(item):
                    result[key] = REDACTED
                    redactions += 1
                    continue
            new_item, count = redact_value(item)
            result[key] = new_item
            redactions += count
        return result, redactions
    if isinstance(value, list):
        redactions = 0
        result = []
        for item in value:
            new_item, count = redact_value(item)
            result.append(new_item)
            redactions += count
        return result, redactions
    return value, 0


def process_file(path: Path, execute: bool) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    redacted_payload, redactions = redact_value(payload)
    if execute and redactions:
        path.write_text(json.dumps(redacted_payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    return {
        "file": path.name,
        "redactions_needed": redactions,
        "redactions_applied": redactions if execute else 0,
        "execute": execute,
        "status": "PASS_REDACTED" if execute and redactions else "PASS_NO_REDACTION_NEEDED" if not redactions else "OPEN_GAP_REDACTION_NEEDED",
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['phase_slug']} App Receipt Thread Redaction",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['overall_status']}`",
        f"Execute: `{str(payload['execute']).lower()}`",
        "",
        "Files:",
    ]
    for row in payload["files"]:
        lines.append(
            f"- {row['file']}: `{row['status']}`, needed `{row['redactions_needed']}`, applied `{row['redactions_applied']}`"
        )
    lines.extend(
        [
            "",
            "This helper redacts app thread identifiers only. It does not publish raw app transport.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--input", action="append", required=True)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--receipt-json", required=True)
    parser.add_argument("--receipt-md", required=True)
    args = parser.parse_args()

    rows = [process_file(Path(item), args.execute) for item in args.input]
    open_gaps = [row for row in rows if str(row["status"]).startswith("OPEN_GAP")]
    payload: dict[str, Any] = {
        "artifact_type": "app_receipt_thread_redaction",
        "phase_slug": args.phase_slug,
        "generated_utc": utc_now(),
        "overall_status": "PASS_APP_THREAD_REDACTION_GUARD" if not open_gaps else "OPEN_GAP_APP_THREAD_REDACTION_REQUIRED",
        "execute": args.execute,
        "files": rows,
        "raw_transport_published": False,
        "claim_boundary": {
            "gmut_gate_state": "open",
            "canon_promotion": "not_claimed",
        },
    }
    write_json(Path(args.receipt_json), payload)
    write_md(Path(args.receipt_md), payload)
    print(json.dumps({"status": payload["overall_status"], "phase_slug": args.phase_slug}, indent=2))
    return 0 if not open_gaps else 1


if __name__ == "__main__":
    raise SystemExit(main())
