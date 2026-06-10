#!/usr/bin/env python3
"""Persist a bounded V44 Google Drive connector proof into repo-local artifacts."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from trinity_v44_common import ROOT, now_iso, write_json, write_text

DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v44-google-drive-proof-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v44-google-drive-proof-v1.md"


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V44 Google Drive Proof",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Google Drive state: `{payload['google_drive_state']}`",
        f"- Cloud drive mesh state: `{payload['cloud_drive_mesh_state']}`",
        f"- Profile email: `{payload.get('profile_email', '') or 'unknown'}`",
        f"- Shared drives observed: `{payload.get('shared_drive_count', 0)}`",
        f"- Write mode: `{payload.get('write_mode', '') or 'none'}`",
        "",
    ]
    if payload.get("created_file_id"):
        lines.extend(
            [
                "## Created Artifact",
                "",
                f"- `created_file_id`: `{payload['created_file_id']}`",
                f"- `created_file_name`: `{payload.get('created_file_name', '')}`",
                f"- `created_file_mime_type`: `{payload.get('created_file_mime_type', '')}`",
                f"- `created_file_url`: `{payload.get('created_file_url', '')}`",
                "",
            ]
        )
    if payload.get("blockers"):
        lines.extend(["## Blockers", ""])
        lines.extend(f"- {row}" for row in payload["blockers"])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Persist a bounded V44 Google Drive connector proof.")
    parser.add_argument("--profile-email", default="")
    parser.add_argument("--profile-name", default="")
    parser.add_argument("--shared-drive-count", type=int, default=0)
    parser.add_argument("--drive-label", default="")
    parser.add_argument("--write-mode", default="")
    parser.add_argument("--created-file-id", default="")
    parser.add_argument("--created-file-name", default="")
    parser.add_argument("--created-file-mime-type", default="")
    parser.add_argument("--created-file-url", default="")
    parser.add_argument("--metadata-readable", action="store_true")
    parser.add_argument("--blocker", action="append", default=[])
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()

    blockers = [item for item in args.blocker if item]
    proof_ok = bool(args.profile_email and args.metadata_readable and not blockers)
    google_drive_state = "bounded_connector_verified" if proof_ok else "operator_hold"
    payload = {
        "generated_utc": now_iso(),
        "phase": "v44_omega",
        "overall_status": "PASS" if proof_ok else "WARN",
        "google_drive_state": google_drive_state,
        "cloud_drive_mesh_state": "google_drive_callable" if proof_ok else "google_drive_blocked",
        "profile_email": args.profile_email,
        "profile_name": args.profile_name,
        "shared_drive_count": args.shared_drive_count,
        "drive_label": args.drive_label,
        "write_mode": args.write_mode,
        "created_file_id": args.created_file_id,
        "created_file_name": args.created_file_name,
        "created_file_mime_type": args.created_file_mime_type,
        "created_file_url": args.created_file_url,
        "metadata_readable": args.metadata_readable,
        "blockers": blockers,
    }
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    return 0 if proof_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

