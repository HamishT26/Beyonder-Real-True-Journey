#!/usr/bin/env python3
"""Run the bounded V43 GMUT/QCIT experiment bundle."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from trinity_v43_common import ROOT, now_iso, safe_run, write_json, write_text

OUTPUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v43-gmut-lab-bundle-v1.json"
OUTPUT_MD = ROOT / "docs" / "trinity-live-traces" / "v43-gmut-lab-bundle-v1.md"
STEPS = [
    ("qcit_coordination", ["python", "scripts/qcit_coordination_engine.py"]),
    ("quantum_energy_transmutation", ["python", "scripts/quantum_energy_transmutation_engine.py"]),
    ("validate_transmutation_reports", ["python", "scripts/validate_transmutation_reports.py"]),
    ("kairotic_detector", ["python", "scripts/kairotic_detector.py"]),
    ("trinity_energy_bank", ["python", "scripts/trinity_energy_bank_system.py"]),
]


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V43 GMUT Lab Bundle",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- GMUT experiment state: `{payload['gmut_experiment_state']}`",
        f"- Execution mode: `{payload['execution_mode']}`",
        "",
        "## Steps",
        "",
    ]
    for row in payload.get("steps", []):
        lines.append(f"- `{row['step_id']}`: status=`{row['status']}`, returncode=`{row['returncode']}`")
    if payload.get("blockers"):
        lines.extend(["", "## Blockers", ""])
        lines.extend(f"- {row}" for row in payload["blockers"])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the bounded V43 GMUT/QCIT experiment bundle.")
    parser.add_argument("--scheduled", action="store_true")
    parser.add_argument("--output-json", default=str(OUTPUT_JSON))
    parser.add_argument("--output-md", default=str(OUTPUT_MD))
    args = parser.parse_args()

    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": "v43_omega",
        "overall_status": "WARN",
        "gmut_experiment_state": "pending",
        "execution_mode": "scheduled" if args.scheduled else "manual",
        "steps": [],
        "completed_steps": [],
        "blockers": [],
        "marker": f"V43_GMUT_LAB_OK::{now_iso()}",
    }

    all_ok = True
    for step_id, command in STEPS:
        proc = safe_run(command, timeout=1800)
        status = "PASS" if proc.returncode == 0 else "FAIL"
        payload["steps"].append(
            {
                "step_id": step_id,
                "command": " ".join(command),
                "status": status,
                "returncode": proc.returncode,
                "stdout_excerpt": proc.stdout[-2000:],
                "stderr_excerpt": proc.stderr[-1200:],
            }
        )
        if proc.returncode == 0:
            payload["completed_steps"].append(f"{step_id}_verified")
        else:
            all_ok = False
            payload["blockers"].append(f"{step_id} failed with returncode={proc.returncode}")

    payload["overall_status"] = "PASS" if all_ok else "WARN"
    payload["gmut_experiment_state"] = "bundle_verified" if all_ok else "bundle_blocked"
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
