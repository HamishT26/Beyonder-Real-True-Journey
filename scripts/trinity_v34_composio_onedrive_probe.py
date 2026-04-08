#!/usr/bin/env python3
"""Run the bounded V34 Composio OneDrive visibility lane."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from trinity_v34_cloud_common import PHASE, TRACE_DIR, now_iso, write_json, write_text

ROOT = Path(__file__).resolve().parent.parent
SOURCE_JSON = ROOT / "docs" / "trinity-live-traces" / "v33-composio-onedrive-proof-v1.json"
SOURCE_MD = ROOT / "docs" / "trinity-live-traces" / "v33-composio-onedrive-proof-v1.md"
OUTPUT_JSON = TRACE_DIR / "v34-composio-onedrive-proof-v1.json"
OUTPUT_MD = TRACE_DIR / "v34-composio-onedrive-proof-v1.md"


def write_outputs(payload: dict[str, Any]) -> None:
    write_json(OUTPUT_JSON, payload)
    lines = [
        "# V34 Composio OneDrive Proof",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Proof state: `{payload['proof_state']}`",
        f"- Connected account count: `{payload.get('connected_account_count', 'unknown')}`",
        "",
        "## Notes",
        "",
    ]
    for note in payload.get("notes", []):
        lines.append(f"- {note}")
    if payload.get("blockers"):
        lines.extend(["", "## Blockers", ""])
        for blocker in payload["blockers"]:
            lines.append(f"- {blocker}")
    write_text(OUTPUT_MD, "\n".join(lines) + "\n")


def main() -> int:
    rerun = subprocess.run([sys.executable, "scripts/trinity_v33_composio_onedrive_probe.py"], cwd=ROOT, capture_output=True, text=True, check=False, timeout=300)
    if not SOURCE_JSON.exists():
        payload = {
            "generated_utc": now_iso(),
            "phase": PHASE,
            "overall_status": "FAIL",
            "proof_state": "source_probe_missing",
            "notes": [
                "V34 reuses the bounded OneDrive visibility logic and keeps Composio non-gating.",
            ],
            "blockers": ["The v33 Composio probe did not produce a source artifact."],
            "rerun": {"returncode": rerun.returncode, "stdout": rerun.stdout.strip(), "stderr": rerun.stderr.strip()},
        }
        write_outputs(payload)
        return 1

    payload: dict[str, Any] = json.loads(SOURCE_JSON.read_text(encoding="utf-8"))
    payload["generated_utc"] = now_iso()
    payload["phase"] = PHASE
    payload["source_probe_json"] = str(SOURCE_JSON.relative_to(ROOT)).replace("\\", "/")
    payload["source_probe_md"] = str(SOURCE_MD.relative_to(ROOT)).replace("\\", "/")
    payload["notes"] = [
        "V34 reruns the bounded OneDrive visibility logic and keeps Composio non-gating.",
        "Only safe read-style tool candidates are considered for execute attempts.",
    ]
    payload["rerun"] = {"returncode": rerun.returncode, "stdout": rerun.stdout.strip(), "stderr": rerun.stderr.strip()}
    write_outputs(payload)
    return 0 if payload.get("overall_status") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
