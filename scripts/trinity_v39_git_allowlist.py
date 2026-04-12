#!/usr/bin/env python3
"""Compute the curated V39 stage allowlist against a dirty repo."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v39-stage-allowlist-v1.json"
OUTPUT_MD = ROOT / "docs" / "trinity-live-traces" / "v39-stage-allowlist-v1.md"

BASELINE_V38_FILES = [
    "scripts/publish_v38_omega_surfaces.py",
    "scripts/trinity_v38_agent_engine_probe.py",
    "scripts/trinity_v38_enterprise_api_sweep.py",
    "scripts/trinity_v38_environment_probe.py",
    "scripts/trinity_v38_fleet_anthos_probe.py",
    "scripts/trinity_v38_journey_digest.py",
    "scripts/trinity_v38_kai_bridge_probe.py",
    "scripts/trinity_v38_os_login_probe.py",
    "scripts/trinity_v38_vesper_ingest_probe.py",
    "scripts/trinity_v38_windows_operator_probe.py",
    "docs/auto-generated/v38-journey-advisory-digest-v1.json",
    "docs/auto-generated/v38-journey-advisory-digest-v1.md",
    "docs/trinity-live-traces/v38-agent-engine-proof-v1.json",
    "docs/trinity-live-traces/v38-agent-engine-proof-v1.md",
    "docs/trinity-live-traces/v38-enterprise-api-sweep-v1.json",
    "docs/trinity-live-traces/v38-enterprise-api-sweep-v1.md",
    "docs/trinity-live-traces/v38-environment-proof-v1.json",
    "docs/trinity-live-traces/v38-environment-proof-v1.md",
    "docs/trinity-live-traces/v38-fleet-anthos-proof-v1.json",
    "docs/trinity-live-traces/v38-fleet-anthos-proof-v1.md",
    "docs/trinity-live-traces/v38-kai-bridge-proof-v1-proof-refresh-snapshot.json",
    "docs/trinity-live-traces/v38-kai-bridge-proof-v1-status-snapshot.json",
    "docs/trinity-live-traces/v38-kai-bridge-proof-v1.json",
    "docs/trinity-live-traces/v38-kai-bridge-proof-v1.md",
    "docs/trinity-live-traces/v38-os-login-proof-v1.json",
    "docs/trinity-live-traces/v38-os-login-proof-v1.md",
    "docs/trinity-live-traces/v38-slot-39-gemini-cli-proof-v1.json",
    "docs/trinity-live-traces/v38-slot-39-gemini-cli-proof-v1.md",
    "docs/trinity-live-traces/v38-vesper-bigtable-ingest-proof-v1.json",
    "docs/trinity-live-traces/v38-vesper-bigtable-ingest-proof-v1.md",
    "docs/trinity-live-traces/v38-windows-operator-proof-v1.json",
    "docs/trinity-live-traces/v38-windows-operator-proof-v1.md",
    "docs/v38-collab-suite-status.json",
    "docs/v38-council-coordination-note-v1.md",
    "docs/v38-deep-suite-status.json",
    "docs/v38-materialize-l2-status.json",
    "docs/v38-materialize-l3-status.json",
    "docs/v38-materialize-l4-status.json",
    "docs/v38-materialize-l5-status.json",
    "docs/v38-omega-closeout-summary-v1.json",
    "docs/v38-omega-continuity-pack-v1.md",
    "docs/v38-omega-handoff-policy-v1.json",
    "docs/v38-quick-suite-status.json",
    "docs/v38-standard-suite-status.json",
    "docs/v39-beta-closeout-summary-v1.json",
    "docs/v39-beta-continuity-pack-v1.md",
    "docs/v39-beta-handoff-policy-v1.json",
]

V39_EXPECTED_FILES = [
    "scripts/trinity_v39_agent_engine_forensics.py",
    "scripts/trinity_v39_agent_engine_minimal_probe.py",
    "scripts/trinity_v39_kai_consultation_bridge.py",
    "scripts/trinity_v39_vesper_runtime_bridge.py",
    "scripts/trinity_v39_pillar_bundle.py",
    "scripts/trinity_v39_addition_registry.py",
    "scripts/trinity_v39_git_allowlist.py",
    "scripts/trinity_v39_git_publication_result.py",
    "scripts/trinity_v39_journey_digest.py",
    "scripts/publish_v39_omega_surfaces.py",
    "docs/auto-generated/v39-journey-advisory-digest-v1.json",
    "docs/auto-generated/v39-journey-advisory-digest-v1.md",
    "docs/trinity-live-traces/v39-stage-allowlist-v1.json",
    "docs/trinity-live-traces/v39-stage-allowlist-v1.md",
    "docs/trinity-live-traces/v39-agent-engine-forensics-v1.json",
    "docs/trinity-live-traces/v39-agent-engine-forensics-v1.md",
    "docs/trinity-live-traces/v39-agent-engine-minimal-probe-v1.json",
    "docs/trinity-live-traces/v39-agent-engine-minimal-probe-v1.md",
    "docs/trinity-live-traces/v39-kai-consultation-bridge-v1.json",
    "docs/trinity-live-traces/v39-kai-consultation-bridge-v1.md",
    "docs/trinity-live-traces/v39-vesper-runtime-bridge-v1.json",
    "docs/trinity-live-traces/v39-vesper-runtime-bridge-v1.md",
    "docs/trinity-live-traces/v39-pillar-bundle-v1.json",
    "docs/trinity-live-traces/v39-pillar-bundle-v1.md",
    "docs/trinity-live-traces/v39-mind-proof-bundle-v1.json",
    "docs/trinity-live-traces/v39-mind-proof-bundle-v1.md",
    "docs/trinity-live-traces/v39-body-proof-bundle-v1.json",
    "docs/trinity-live-traces/v39-body-proof-bundle-v1.md",
    "docs/trinity-live-traces/v39-heart-proof-bundle-v1.json",
    "docs/trinity-live-traces/v39-heart-proof-bundle-v1.md",
    "docs/trinity-live-traces/v39-addition-registry-v1.json",
    "docs/trinity-live-traces/v39-addition-registry-v1.md",
    "docs/trinity-live-traces/v39-quick-suite-status.json",
    "docs/trinity-live-traces/v39-standard-suite-status.json",
    "docs/trinity-live-traces/v39-deep-suite-status.json",
    "docs/trinity-live-traces/v39-collab-suite-status.json",
    "docs/trinity-live-traces/v39-materialize-l2-status.json",
    "docs/trinity-live-traces/v39-materialize-l3-status.json",
    "docs/trinity-live-traces/v39-materialize-l4-status.json",
    "docs/trinity-live-traces/v39-materialize-l5-status.json",
    "docs/trinity-live-traces/v39-git-publication-result-v1.json",
    "docs/trinity-live-traces/v39-git-publication-result-v1.md",
    "docs/v39-council-coordination-note-v1.md",
    "docs/v39-omega-closeout-summary-v1.json",
    "docs/v39-omega-continuity-pack-v1.md",
    "docs/v39-omega-handoff-policy-v1.json",
    "docs/v40-beta-closeout-summary-v1.json",
    "docs/v40-beta-continuity-pack-v1.md",
    "docs/v40-beta-handoff-policy-v1.json",
    "docs/trinity-runtime-model-resolution-v1.json",
]

EXCLUDED_PATTERNS = [
    "__pycache__/",
    "docs/*-latest.json",
    "docs/*-latest.md",
    "docs/trinity-mcp-cache/",
    "docs/trinity-expansion/",
    "docs/trinity-agent-private-chats-",
    "docs/trinity-agent-memory-ledgers/",
]


def now_iso() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def git_head() -> str:
    proc = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    return (proc.stdout or "").strip()


def git_status_lines() -> list[str]:
    proc = subprocess.run(
        ["git", "-C", str(ROOT), "status", "--short"],
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    return [line.rstrip() for line in (proc.stdout or "").splitlines() if line.strip()]


def _is_tracked(rel_path: str) -> bool:
    proc = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "--error-unmatch", rel_path],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    return proc.returncode == 0


def path_status(rel_path: str) -> dict[str, Any]:
    path = ROOT / rel_path
    return {
        "path": rel_path,
        "present": path.exists(),
        "tracked": _is_tracked(rel_path),
    }


def write_json_file(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_text_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V39 Stage Allowlist",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Current head: `{payload['current_head_sha']}`",
        f"- Dirty path count observed: `{payload['dirty_path_count']}`",
        f"- Curated include count: `{payload['curated_include_count']}`",
        "",
        "## Included Baseline V38 Prerequisites",
        "",
    ]
    lines.extend(f"- `{row['path']}` (`present={row['present']}`, `tracked={row['tracked']}`)" for row in payload["baseline_v38"])
    lines.extend(["", "## Included V39 Paths", ""])
    lines.extend(f"- `{row['path']}` (`present={row['present']}`, `tracked={row['tracked']}`)" for row in payload["v39_expected"])
    lines.extend(["", "## Explicit Exclusions", ""])
    lines.extend(f"- `{row}`" for row in payload["excluded_patterns"])
    if payload.get("background_dirty_sample"):
        lines.extend(["", "## Background Dirty Sample", ""])
        lines.extend(f"- `{row}`" for row in payload["background_dirty_sample"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute the curated V39 stage allowlist.")
    parser.add_argument("--output-json", default=str(OUTPUT_JSON))
    parser.add_argument("--output-md", default=str(OUTPUT_MD))
    args = parser.parse_args()

    dirty_lines = git_status_lines()
    baseline_rows = [path_status(path) for path in BASELINE_V38_FILES]
    v39_rows = [path_status(path) for path in V39_EXPECTED_FILES]
    curated_include_paths = [row["path"] for row in [*baseline_rows, *v39_rows]]

    payload = {
        "generated_utc": now_iso(),
        "phase": "v39_omega",
        "current_head_sha": git_head(),
        "curation_rule": "baseline_v38_prerequisites_plus_v39_only",
        "dirty_path_count": len(dirty_lines),
        "curated_include_count": len(curated_include_paths),
        "baseline_v38": baseline_rows,
        "v39_expected": v39_rows,
        "curated_include_paths": curated_include_paths,
        "excluded_patterns": EXCLUDED_PATTERNS,
        "background_dirty_sample": dirty_lines[:80],
    }
    write_json_file(Path(args.output_json), payload)
    write_text_file(Path(args.output_md), markdown(payload))
    print(f"allowlist={args.output_json}")
    print(f"curated_include_count={len(curated_include_paths)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
