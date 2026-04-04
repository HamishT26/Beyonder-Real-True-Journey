#!/usr/bin/env python3
"""Write the bounded V32 Hugging Face guarded-lane proof surface."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from trinity_v32_runtime_common import now_iso, write_json, write_text

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v32-huggingface-guarded-lane-proof-v1.json"
OUTPUT_MD = ROOT / "docs" / "trinity-live-traces" / "v32-huggingface-guarded-lane-proof-v1.md"


def write_outputs(payload: dict[str, Any]) -> None:
    write_json(OUTPUT_JSON, payload)
    lines = [
        "# V32 Hugging Face Guarded Lane Proof",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Proof state: `{payload['proof_state']}`",
        f"- Authenticated user: `{payload.get('authenticated_user', 'unknown')}`",
        f"- Hardware: `{payload.get('execution_probe_flavor', 'unknown')}`",
        f"- Spend guard: `{payload.get('spend_guard', 'unknown')}`",
        "",
        "## Notes",
        "",
    ]
    for note in payload.get("notes", []):
        lines.append(f"- {note}")
    write_text(OUTPUT_MD, "\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Write the V32 Hugging Face guarded-lane proof.")
    parser.add_argument("--authenticated-user", required=True)
    parser.add_argument("--overall-status", default="PASS")
    parser.add_argument("--proof-state", default="live_execution_proven")
    parser.add_argument("--read-surface-status", default="PASS")
    parser.add_argument("--execution-probe-status", default="PASS")
    parser.add_argument("--execution-probe-flavor", default="cpu-basic")
    parser.add_argument("--job-id", required=True)
    parser.add_argument("--job-stage", required=True)
    parser.add_argument("--job-log-excerpt", default="")
    parser.add_argument("--spend-guard", default="single_smoke_job_cpu_basic")
    parser.add_argument("--cost-posture", default="bounded_credit_spend")
    parser.add_argument("--notes", action="append", default=[])
    args = parser.parse_args()

    payload = {
        "generated_utc": now_iso(),
        "phase": "v32_omega",
        "overall_status": args.overall_status,
        "proof_state": args.proof_state,
        "authenticated_user": args.authenticated_user,
        "read_surface_status": args.read_surface_status,
        "execution_probe_status": args.execution_probe_status,
        "execution_probe_flavor": args.execution_probe_flavor,
        "execution_probe_path": "hf_jobs.uv",
        "job_id": args.job_id,
        "job_stage": args.job_stage,
        "job_log_excerpt": args.job_log_excerpt,
        "spend_guard": args.spend_guard,
        "cost_posture": args.cost_posture,
        "notes": args.notes
        or [
            "V32 keeps Hugging Face execution live but guarded with a single bounded smoke job and explicit spend posture.",
            "This lane remains a premium execution fallback even if native GCP execution grows later.",
        ],
    }
    write_outputs(payload)
    return 0 if args.overall_status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
