#!/usr/bin/env python3
"""Compute the curated V40 stage allowlist against a dirty repo."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path
from typing import Any

from trinity_v40_common import git_head, now_iso, write_json, write_text

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v40-stage-allowlist-v1.json"
OUTPUT_MD = ROOT / "docs" / "trinity-live-traces" / "v40-stage-allowlist-v1.md"

V40_EXPECTED_FILES = [
    "scripts/trinity_v40_common.py",
    "scripts/trinity_v40_runtime_truth_completion.py",
    "scripts/trinity_v40_agent_engine_advanced_probe.py",
    "scripts/trinity_v40_kai_consultation_bridge.py",
    "scripts/trinity_v40_vesper_runtime_bridge.py",
    "scripts/trinity_v40_pillar_bundle.py",
    "scripts/trinity_v40_addition_registry.py",
    "scripts/trinity_v40_git_allowlist.py",
    "scripts/trinity_v40_git_publication_result.py",
    "scripts/publish_v40_omega_surfaces.py",
    "docs/trinity-live-traces/v40-runtime-truth-completion-v1.json",
    "docs/trinity-live-traces/v40-runtime-truth-completion-v1.md",
    "docs/trinity-live-traces/v40-agent-engine-advanced-probe-v1.json",
    "docs/trinity-live-traces/v40-agent-engine-advanced-probe-v1.md",
    "docs/trinity-live-traces/v40-kai-consultation-bridge-v1.json",
    "docs/trinity-live-traces/v40-kai-consultation-bridge-v1.md",
    "docs/trinity-live-traces/v40-vesper-runtime-bridge-v1.json",
    "docs/trinity-live-traces/v40-vesper-runtime-bridge-v1.md",
    "docs/trinity-live-traces/v40-mind-proof-bundle-v1.json",
    "docs/trinity-live-traces/v40-mind-proof-bundle-v1.md",
    "docs/trinity-live-traces/v40-body-proof-bundle-v1.json",
    "docs/trinity-live-traces/v40-body-proof-bundle-v1.md",
    "docs/trinity-live-traces/v40-heart-proof-bundle-v1.json",
    "docs/trinity-live-traces/v40-heart-proof-bundle-v1.md",
    "docs/trinity-live-traces/v40-pillar-bundle-v1.json",
    "docs/trinity-live-traces/v40-pillar-bundle-v1.md",
    "docs/trinity-live-traces/v40-addition-registry-v1.json",
    "docs/trinity-live-traces/v40-addition-registry-v1.md",
    "docs/trinity-live-traces/v40-stage-allowlist-v1.json",
    "docs/trinity-live-traces/v40-stage-allowlist-v1.md",
    "docs/trinity-live-traces/v40-quick-suite-status.json",
    "docs/trinity-live-traces/v40-standard-suite-status.json",
    "docs/trinity-live-traces/v40-deep-suite-status.json",
    "docs/trinity-live-traces/v40-collab-suite-status.json",
    "docs/trinity-live-traces/v40-materialize-l2-status.json",
    "docs/trinity-live-traces/v40-materialize-l3-status.json",
    "docs/trinity-live-traces/v40-materialize-l4-status.json",
    "docs/trinity-live-traces/v40-materialize-l5-status.json",
    "docs/trinity-live-traces/v40-git-publication-result-v1.json",
    "docs/trinity-live-traces/v40-git-publication-result-v1.md",
    "docs/v17-runtime-session-log-latest.json",
    "docs/v17-runtime-truth-resolution-board-v1.json",
    "docs/v17-runtime-session-validation-latest.json",
    "docs/v17-external-establishment-criteria-board-v1.json",
    "docs/v17-external-establishment-validation-latest.json",
    "docs/v17-evidence-first-control-tower-latest.json",
    "docs/v17-evidence-first-control-tower-latest.md",
    "docs/trinity-runtime-model-resolution-v1.json",
    "docs/v40-council-coordination-note-v1.md",
    "docs/v40-omega-closeout-summary-v1.json",
    "docs/v40-omega-continuity-pack-v1.md",
    "docs/v40-omega-handoff-policy-v1.json",
    "docs/v41-beta-closeout-summary-v1.json",
    "docs/v41-beta-continuity-pack-v1.md",
    "docs/v41-beta-handoff-policy-v1.json",
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


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V40 Stage Allowlist",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Current head: `{payload['current_head_sha']}`",
        f"- Dirty path count observed: `{payload['dirty_path_count']}`",
        f"- Curated include count: `{payload['curated_include_count']}`",
        "",
        "## Included V40 Paths",
        "",
    ]
    lines.extend(f"- `{row['path']}` (`present={row['present']}`, `tracked={row['tracked']}`)" for row in payload["v40_expected"])
    lines.extend(["", "## Explicit Exclusions", ""])
    lines.extend(f"- `{row}`" for row in payload["excluded_patterns"])
    if payload.get("background_dirty_sample"):
        lines.extend(["", "## Background Dirty Sample", ""])
        lines.extend(f"- `{row}`" for row in payload["background_dirty_sample"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute the curated V40 stage allowlist.")
    parser.add_argument("--output-json", default=str(OUTPUT_JSON))
    parser.add_argument("--output-md", default=str(OUTPUT_MD))
    args = parser.parse_args()

    dirty_lines = git_status_lines()
    v40_rows = [path_status(path) for path in V40_EXPECTED_FILES]
    curated_include_paths = [row["path"] for row in v40_rows]
    payload = {
        "generated_utc": now_iso(),
        "phase": "v40_omega",
        "current_head_sha": git_head(),
        "curation_rule": "v40_only_curated_stage_set",
        "dirty_path_count": len(dirty_lines),
        "curated_include_count": len(curated_include_paths),
        "v40_expected": v40_rows,
        "curated_include_paths": curated_include_paths,
        "excluded_patterns": EXCLUDED_PATTERNS,
        "background_dirty_sample": dirty_lines[:80],
    }
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
