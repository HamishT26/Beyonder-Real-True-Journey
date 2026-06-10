#!/usr/bin/env python3
"""Run the bounded V38 Agent Engine retry lane."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v38-agent-engine-proof-v1.json"
OUTPUT_MD = ROOT / "docs" / "trinity-live-traces" / "v38-agent-engine-proof-v1.md"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the bounded V38 Agent Engine retry lane.")
    parser.add_argument("--bundle", default=str(Path.home() / "GCP service account keys.txt"))
    parser.add_argument("--project-id", default="gen-lang-client-0020882673")
    parser.add_argument("--regional-location", default="us-central1")
    parser.add_argument("--model-location", default="global")
    parser.add_argument("--output-json", default=str(OUTPUT_JSON))
    parser.add_argument("--output-md", default=str(OUTPUT_MD))
    args = parser.parse_args()

    output_json = Path(args.output_json)
    output_md = Path(args.output_md)
    command = [
        sys.executable,
        "scripts/trinity_v36_memory_bank_probe.py",
        "--bundle",
        args.bundle,
        "--project-id",
        args.project_id,
        "--regional-location",
        args.regional_location,
        "--model-location",
        args.model_location,
        "--phase-label",
        "v38_omega",
        "--output-json",
        str(output_json),
        "--output-md",
        str(output_md),
    ]
    proc = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=3600,
        check=False,
    )

    payload: dict[str, Any] = {}
    if output_json.exists():
        payload = json.loads(output_json.read_text(encoding="utf-8-sig"))
    if not payload:
        payload = {
            "phase": "v38_omega",
            "overall_status": "FAIL",
            "proof_state": "agent_engine_wrapper_failed_before_report",
            "memory_bank_state": "report_missing",
            "agent_engine_state": "report_missing",
            "blockers": ["The V38 Agent Engine probe did not produce a child report."],
        }
    payload["wrapper_invocation"] = {
        "command": command,
        "returncode": proc.returncode,
        "stdout_excerpt": proc.stdout[-4000:],
        "stderr_excerpt": proc.stderr[-2000:],
        "bounded_retry_lane": True,
    }
    write_json(output_json, payload)
    return 0 if proc.returncode == 0 and str(payload.get("overall_status") or "") in {"PASS", "WARN"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
