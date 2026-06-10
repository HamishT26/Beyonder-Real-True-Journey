#!/usr/bin/env python3
"""Publish the bounded V44 Vesper memory and Agent Engine bridge truth."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from trinity_v44_common import ROOT, now_iso, read_json, write_json, write_text

DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v44-vesper-memory-cognitive-bridge-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v44-vesper-memory-cognitive-bridge-v1.md"


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V44 Vesper Memory And Cognitive Bridge",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Bigtable primary state: `{payload['bigtable_primary_state']}`",
        f"- Vesper telemetry state: `{payload['vesper_telemetry_ingest_state']}`",
        f"- Vesper cognitive engine state: `{payload['vesper_cognitive_engine_state']}`",
        f"- Agent Engine state: `{payload['agent_engine_state']}`",
        "",
        "## Completed Steps",
        "",
    ]
    lines.extend(f"- `{row}`" for row in payload.get("completed_steps", []))
    if payload.get("blockers"):
        lines.extend(["", "## Blockers", ""])
        lines.extend(f"- {row}" for row in payload["blockers"])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish the bounded V44 Vesper memory and Agent Engine bridge truth.")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()

    cloud = read_json(ROOT / "docs" / "trinity-live-traces" / "v44-cloud-sweep-v1.json")
    blockers: list[str] = []
    if str(cloud.get("cloud_billing_state") or "").startswith("blocked"):
        blockers.append("Cloud billing, account, or project truth is incomplete, so V44 did not run billable Vesper proofs.")

    payload = {
        "generated_utc": now_iso(),
        "phase": "v44_omega",
        "overall_status": "PASS" if not blockers else "WARN",
        "bigtable_primary_state": "carry_forward_primary_lane_preserved",
        "vesper_telemetry_ingest_state": "preflight_blocked_carry_forward_only" if blockers else "bounded_probe_required",
        "vesper_cognitive_engine_state": "blocked_preflight_incomplete" if blockers else "bounded_probe_required",
        "agent_engine_state": "blocked_preflight_incomplete" if blockers else "bounded_probe_required",
        "ai_applications_state": str(cloud.get("ai_applications_state") or "blocked_preflight_incomplete"),
        "vertex_ai_search_state": str(cloud.get("vertex_ai_search_state") or "blocked_preflight_incomplete"),
        "agent_engine_cost_posture": "runtime_free_tier_with_sessions_memory_and_code_execution_bounded_billable",
        "completed_steps": [
            "bigtable_primary_lane_preserved_by_policy",
            "agent_engine_bounded_cost_posture_published",
        ],
        "blockers": blockers,
    }
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    return 0 if payload["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

