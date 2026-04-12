#!/usr/bin/env python3
"""Publish the curated V39 addition registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v39-addition-registry-v1.json"
OUTPUT_MD = ROOT / "docs" / "trinity-live-traces" / "v39-addition-registry-v1.md"


def now_iso() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def entries() -> list[dict]:
    return [
        {
            "name": "v39_journey_digest",
            "category": "reusable runtime script",
            "priority": "stretch",
            "purpose": "Absorb the latest journey text into an advisory-only digest without mutating repo truth.",
            "install_or_enablement_path": "scripts/trinity_v39_journey_digest.py",
            "proof_artifact": "docs/auto-generated/v39-journey-advisory-digest-v1.json",
            "rollback_or_cleanup": "delete digest outputs if superseded; no live cloud state created",
        },
        {
            "name": "v39_stage_allowlist",
            "category": "reusable runtime script",
            "priority": "core",
            "purpose": "Freeze the curated V39 stage set and keep unrelated dirty churn out of the publication lane.",
            "install_or_enablement_path": "scripts/trinity_v39_git_allowlist.py",
            "proof_artifact": "docs/trinity-live-traces/v39-stage-allowlist-v1.json",
            "rollback_or_cleanup": "regenerate if the curated file set changes",
        },
        {
            "name": "agent_engine_forensics_lane",
            "category": "GCP API or managed service",
            "priority": "core",
            "purpose": "Pull operation state, Cloud Logging evidence, package alignment, and staging state for the failed Agent Engine runtime.",
            "install_or_enablement_path": "scripts/trinity_v39_agent_engine_forensics.py",
            "proof_artifact": "docs/trinity-live-traces/v39-agent-engine-forensics-v1.json",
            "rollback_or_cleanup": "none; read-only diagnostics only",
        },
        {
            "name": "agent_engine_minimal_probe_lane",
            "category": "GCP API or managed service",
            "priority": "core",
            "purpose": "Deploy a fresh minimal Agent Engine with pinned requirements and a unique staging prefix, then verify list/get/query.",
            "install_or_enablement_path": "scripts/trinity_v39_agent_engine_minimal_probe.py",
            "proof_artifact": "docs/trinity-live-traces/v39-agent-engine-minimal-probe-v1.json",
            "rollback_or_cleanup": "delete the fresh minimal reasoning engine only if it becomes healthy and later needs cleanup",
        },
        {
            "name": "kai_consultation_bridge",
            "category": "local tool or CLI",
            "priority": "core",
            "purpose": "Use the proven Gemini CLI route to analyze V39 recovery artifacts and emit bounded machine-readable recommendations.",
            "install_or_enablement_path": "scripts/trinity_v39_kai_consultation_bridge.py",
            "proof_artifact": "docs/trinity-live-traces/v39-kai-consultation-bridge-v1.json",
            "rollback_or_cleanup": "none; bounded CLI execution only",
        },
        {
            "name": "vesper_runtime_bridge",
            "category": "GCP API or managed service",
            "priority": "core",
            "purpose": "Extend Vesper Ion's Bigtable durable-memory bridge with V39 runtime telemetry and read-back verification.",
            "install_or_enablement_path": "scripts/trinity_v39_vesper_runtime_bridge.py",
            "proof_artifact": "docs/trinity-live-traces/v39-vesper-runtime-bridge-v1.json",
            "rollback_or_cleanup": "delete the V39 Bigtable table if the runtime bridge is intentionally retired",
        },
        {
            "name": "pillar_bundle_publisher",
            "category": "reusable runtime script",
            "priority": "core",
            "purpose": "Publish explicit Mind, Body, and Heart V39 proof bundles with PASS/WARN/FAIL posture.",
            "install_or_enablement_path": "scripts/trinity_v39_pillar_bundle.py",
            "proof_artifact": "docs/trinity-live-traces/v39-pillar-bundle-v1.json",
            "rollback_or_cleanup": "replace with a fresh bundle on later phases; no external side effects",
        },
        {
            "name": "v39_surface_publisher",
            "category": "reusable runtime script",
            "priority": "core",
            "purpose": "Update runtime truth and publish the V39 Omega closeout plus the V40 Beta handoff pack.",
            "install_or_enablement_path": "scripts/publish_v39_omega_surfaces.py",
            "proof_artifact": "docs/v39-omega-closeout-summary-v1.json",
            "rollback_or_cleanup": "re-run after suite or git state changes",
        },
    ]


def markdown(payload: dict) -> str:
    lines = [
        "# V39 Addition Registry",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        "",
        "## Entries",
        "",
    ]
    for row in payload["entries"]:
        lines.append(f"- `{row['name']}` [{row['category']}, {row['priority']}]: {row['purpose']}")
        lines.append(f"  proof: `{row['proof_artifact']}`")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish the curated V39 addition registry.")
    parser.add_argument("--output-json", default=str(OUTPUT_JSON))
    parser.add_argument("--output-md", default=str(OUTPUT_MD))
    args = parser.parse_args()

    payload = {
        "generated_utc": now_iso(),
        "phase": "v39_omega",
        "overall_status": "PASS",
        "addition_registry_state": "published",
        "entries": entries(),
    }
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    print(f"addition_registry={args.output_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
