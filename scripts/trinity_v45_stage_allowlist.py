#!/usr/bin/env python3
"""Compute the curated V45 stage allowlist and forward-only cleanup note."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from trinity_v45_common import git_head, git_status_lines, git_tracked, now_iso, write_json, write_text

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v45-stage-allowlist-v1.json"
OUTPUT_MD = ROOT / "docs" / "trinity-live-traces" / "v45-stage-allowlist-v1.md"
CLEANUP_NOTE = ROOT / "docs" / "trinity-live-traces" / "v45-git-cleanup-note-v1.md"

INTENDED_V45_PATHS = [
    "scripts/publish_v45_omega_surfaces.py",
    "scripts/trinity_v45_cloud_research_digest.py",
    "scripts/trinity_v45_codex_cli_slot40_probe.py",
    "scripts/trinity_v45_codex_home_repair.py",
    "scripts/trinity_v45_common.py",
    "scripts/trinity_v45_git_publication_result.py",
    "scripts/trinity_v45_journey_digest.py",
    "scripts/trinity_v45_operator_surface_probe.py",
    "scripts/trinity_v45_stage_allowlist.py",
    "docs/auto-generated/v45-journey-advisory-digest-v1.json",
    "docs/auto-generated/v45-journey-advisory-digest-v1.md",
    "docs/trinity-live-traces/v45-cloud-research-digest-v1.json",
    "docs/trinity-live-traces/v45-cloud-research-digest-v1.md",
    "docs/trinity-live-traces/v45-codex-cli-slot40-probe-v1.json",
    "docs/trinity-live-traces/v45-codex-cli-slot40-probe-v1.md",
    "docs/trinity-live-traces/v45-codex-home-repair-v1.json",
    "docs/trinity-live-traces/v45-codex-home-repair-v1.md",
    "docs/trinity-live-traces/v45-git-cleanup-note-v1.md",
    "docs/trinity-live-traces/v45-git-publication-result-v1.json",
    "docs/trinity-live-traces/v45-git-publication-result-v1.md",
    "docs/trinity-live-traces/v45-operator-surface-probe-v1.json",
    "docs/trinity-live-traces/v45-operator-surface-probe-v1.md",
    "docs/trinity-live-traces/v45-quick-suite-status.json",
    "docs/trinity-live-traces/v45-standard-suite-status.json",
    "docs/trinity-live-traces/v45-deep-suite-status.json",
    "docs/trinity-live-traces/v45-stage-allowlist-v1.json",
    "docs/trinity-live-traces/v45-stage-allowlist-v1.md",
    "docs/trinity-runtime-model-resolution-v1.json",
    "docs/v17-runtime-session-log-latest.json",
    "docs/v17-runtime-session-validation-latest.json",
    "docs/v17-runtime-truth-resolution-board-v1.json",
    "docs/v45-omega-closeout-summary-v1.json",
    "docs/v45-omega-continuity-pack-v1.md",
    "docs/v45-omega-handoff-policy-v1.json",
    "docs/v45-powershell-operator-note-v1.md",
    "docs/v46-beta-closeout-summary-v1.json",
    "docs/v46-beta-continuity-pack-v1.md",
    "docs/v46-beta-handoff-policy-v1.json",
]

LATEST_STATE_PREFIXES = (
    "docs/trinity-expansion/",
    "docs/trinity-mcp-cache/",
    "docs/trinity-agent-private-chats-",
    "docs/trinity-agent-memory-ledgers/",
    "docs/trinity-live-traces/",
)
NOISE_PREFIXES = ("__pycache__/", ".local-runtime/")


def classify_dirty_path(path: str, intended: set[str]) -> str:
    if path in intended:
        return "intended_v45_delta"
    if path.endswith(".pyc") or any(path.startswith(prefix) for prefix in NOISE_PREFIXES):
        return "non_stage_noise"
    if any(path.startswith(prefix) for prefix in LATEST_STATE_PREFIXES):
        return "carried_forward_dirty_latest_state_churn"
    if path.startswith("docs/") and ("-latest." in path or path.endswith(".jsonl") or "/logs/" in path or path.endswith("-status.json")):
        return "carried_forward_dirty_latest_state_churn"
    return "non_stage_noise"


def path_status(rel_path: str) -> dict[str, Any]:
    path = ROOT / rel_path
    return {"path": rel_path, "present": path.exists(), "tracked": git_tracked(rel_path)}


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V45 Stage Allowlist",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Current head: `{payload['current_head_sha']}`",
        f"- Dirty path count observed: `{payload['dirty_path_count']}`",
        f"- Intended V45 count: `{payload['curated_include_count']}`",
        f"- Carried-forward latest-state churn: `{payload['classification_counts']['carried_forward_dirty_latest_state_churn']}`",
        f"- Non-stage noise: `{payload['classification_counts']['non_stage_noise']}`",
        "",
        "## Intended V45 Paths",
        "",
    ]
    lines.extend(f"- `{row['path']}` (`present={row['present']}`, `tracked={row['tracked']}`)" for row in payload["intended_v45_paths"])
    return "\n".join(lines).rstrip() + "\n"


def cleanup_note(payload: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# V45 Git Cleanup Note",
            "",
            f"- Generated UTC: `{payload['generated_utc']}`",
            f"- Active branch head at note time: `{payload['current_head_sha']}`",
            "- Cleanup posture: `forward_only`.",
            "- Publication posture: stage only the curated V45 allowlist and leave unrelated dirty latest-state churn untouched.",
            "- The dirty C: checkout remains non-execution history until manual reconciliation.",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute the curated V45 stage allowlist.")
    parser.add_argument("--output-json", default=str(OUTPUT_JSON))
    parser.add_argument("--output-md", default=str(OUTPUT_MD))
    parser.add_argument("--cleanup-note", default=str(CLEANUP_NOTE))
    args = parser.parse_args()

    dirty_lines = git_status_lines()
    dirty_paths: list[str] = []
    for line in dirty_lines:
        path = line[3:].strip()
        if path.startswith('"') and path.endswith('"'):
            path = path[1:-1]
        if path:
            dirty_paths.append(path.replace("\\", "/"))

    intended = set(INTENDED_V45_PATHS)
    classification_counts = {
        "intended_v45_delta": 0,
        "carried_forward_dirty_latest_state_churn": 0,
        "non_stage_noise": 0,
    }
    classification_samples: dict[str, list[str]] = {key: [] for key in classification_counts}
    for path in dirty_paths:
        label = classify_dirty_path(path, intended)
        classification_counts[label] += 1
        if len(classification_samples[label]) < 80:
            classification_samples[label].append(path)

    payload = {
        "generated_utc": now_iso(),
        "phase": "v45_omega",
        "current_head_sha": git_head(),
        "curation_rule": "v45_only_forward_cleanup_stage_set",
        "dirty_path_count": len(dirty_paths),
        "curated_include_count": len(INTENDED_V45_PATHS),
        "intended_v45_paths": [path_status(path) for path in INTENDED_V45_PATHS],
        "curated_include_paths": list(INTENDED_V45_PATHS),
        "classification_counts": classification_counts,
        "classification_samples": classification_samples,
        "cleanup_posture": "forward_only",
    }
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    write_text(Path(args.cleanup_note), cleanup_note(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
