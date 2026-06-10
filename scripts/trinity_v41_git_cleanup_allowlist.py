#!/usr/bin/env python3
"""Compute the curated V41 stage allowlist and forward-only cleanup note."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from trinity_v41_common import git_head, git_status_lines, git_tracked, now_iso, write_json, write_text

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v41-stage-allowlist-v1.json"
OUTPUT_MD = ROOT / "docs" / "trinity-live-traces" / "v41-stage-allowlist-v1.md"
CLEANUP_NOTE = ROOT / "docs" / "trinity-live-traces" / "v41-git-cleanup-note-v1.md"
ACCIDENTAL_MERGE_SHA = "2531562ec3"

INTENDED_V41_PATHS = [
    ".codex/agents/28-orun.md",
    ".codex/agents/orun.toml",
    "scripts/publish_v41_omega_surfaces.py",
    "scripts/trinity_agent_council_v15_validator.py",
    "scripts/trinity_agent_council_v16_validator.py",
    "scripts/trinity_api_book_validator.py",
    "scripts/trinity_v41_api_ascendancy.py",
    "scripts/trinity_v41_common.py",
    "scripts/trinity_v41_git_cleanup_allowlist.py",
    "scripts/trinity_v41_git_publication_result.py",
    "scripts/trinity_v41_journey_digest.py",
    "scripts/trinity_v41_kai_health_monitor.py",
    "scripts/trinity_v41_vesper_telemetry_bridge.py",
    "scripts/v17_evidence_first_control_tower_sync.py",
    "docs/auto-generated/v41-journey-advisory-digest-v1.json",
    "docs/auto-generated/v41-journey-advisory-digest-v1.md",
    "docs/trinity-agent-role-contracts/28-orun-role-contract.json",
    "docs/trinity-api-book-latest.md",
    "docs/trinity-api-book-v6.json",
    "docs/trinity-api-book-validation-latest.json",
    "docs/trinity-api-book-validation-latest.md",
    "docs/trinity-live-traces/v41-api-ascendancy-proof-v1.json",
    "docs/trinity-live-traces/v41-api-ascendancy-proof-v1.md",
    "docs/trinity-live-traces/v41-git-publication-result-v1.json",
    "docs/trinity-live-traces/v41-git-publication-result-v1.md",
    "docs/trinity-live-traces/v41-kai-health-monitor-proof-v1.json",
    "docs/trinity-live-traces/v41-kai-health-monitor-proof-v1.md",
    "docs/trinity-live-traces/v41-orun-identity-reclaim-proof-v1.json",
    "docs/trinity-live-traces/v41-orun-identity-reclaim-proof-v1.md",
    "docs/trinity-live-traces/v41-pillar-bundle-v1.json",
    "docs/trinity-live-traces/v41-pillar-bundle-v1.md",
    "docs/trinity-live-traces/v41-quick-suite-status.json",
    "docs/trinity-live-traces/v41-standard-suite-status.json",
    "docs/trinity-live-traces/v41-deep-suite-status.json",
    "docs/trinity-live-traces/v41-collab-suite-status.json",
    "docs/trinity-live-traces/v41-materialize-l2-status.json",
    "docs/trinity-live-traces/v41-materialize-l3-status.json",
    "docs/trinity-live-traces/v41-materialize-l4-status.json",
    "docs/trinity-live-traces/v41-materialize-l5-status.json",
    "docs/trinity-live-traces/v41-git-cleanup-note-v1.md",
    "docs/trinity-live-traces/v41-stage-allowlist-v1.json",
    "docs/trinity-live-traces/v41-stage-allowlist-v1.md",
    "docs/trinity-live-traces/v41-vesper-telemetry-bridge-proof-v1.json",
    "docs/trinity-live-traces/v41-vesper-telemetry-bridge-proof-v1.md",
    "docs/trinity-runtime-model-resolution-v1.json",
    "docs/v17-evidence-first-control-tower-latest.json",
    "docs/v17-evidence-first-control-tower-latest.md",
    "docs/v17-external-establishment-criteria-board-v1.json",
    "docs/v17-external-establishment-validation-latest.json",
    "docs/v17-runtime-session-log-latest.json",
    "docs/v17-runtime-session-validation-latest.json",
    "docs/v17-runtime-truth-resolution-board-v1.json",
    "docs/v41-beta-closeout-summary-v1.json",
    "docs/v41-beta-continuity-pack-v1.md",
    "docs/v41-beta-handoff-policy-v1.json",
    "docs/v41-omega-closeout-summary-v1.json",
    "docs/v41-omega-continuity-pack-v1.md",
    "docs/v41-omega-handoff-policy-v1.json",
    "docs/v42-beta-closeout-summary-v1.json",
    "docs/v42-beta-continuity-pack-v1.md",
    "docs/v42-beta-handoff-policy-v1.json",
]

LATEST_STATE_PREFIXES = (
    "docs/trinity-expansion/",
    "docs/trinity-mcp-cache/",
    "docs/trinity-agent-private-chats-",
    "docs/trinity-agent-memory-ledgers/",
    "docs/trinity-live-traces/",
)
NOISE_PREFIXES = (
    "__pycache__/",
    ".local-runtime/",
)


def classify_dirty_path(path: str, intended: set[str]) -> str:
    if path in intended:
        return "intended_v41_delta"
    if path.endswith(".pyc") or any(path.startswith(prefix) for prefix in NOISE_PREFIXES):
        return "non_stage_noise"
    if any(path.startswith(prefix) for prefix in LATEST_STATE_PREFIXES):
        return "carried_forward_dirty_latest_state_churn"
    if path.startswith("docs/") and (
        "-latest." in path
        or path.endswith(".jsonl")
        or "/logs/" in path
        or path.endswith("-status.json")
    ):
        return "carried_forward_dirty_latest_state_churn"
    return "non_stage_noise"


def path_status(rel_path: str) -> dict[str, Any]:
    path = ROOT / rel_path
    return {
        "path": rel_path,
        "present": path.exists(),
        "tracked": git_tracked(rel_path),
    }


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V41 Stage Allowlist",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Current head: `{payload['current_head_sha']}`",
        f"- Dirty path count observed: `{payload['dirty_path_count']}`",
        f"- Intended v41 count: `{payload['curated_include_count']}`",
        f"- Carried-forward latest-state churn: `{payload['classification_counts']['carried_forward_dirty_latest_state_churn']}`",
        f"- Non-stage noise: `{payload['classification_counts']['non_stage_noise']}`",
        "",
        "## Intended V41 Paths",
        "",
    ]
    lines.extend(
        f"- `{row['path']}` (`present={row['present']}`, `tracked={row['tracked']}`)"
        for row in payload["intended_v41_paths"]
    )
    lines.extend(["", "## Dirty Classification Samples", ""])
    for label in ("intended_v41_delta", "carried_forward_dirty_latest_state_churn", "non_stage_noise"):
        lines.append(f"### {label}")
        lines.append("")
        sample = payload["classification_samples"].get(label, [])
        if sample:
            lines.extend(f"- `{row}`" for row in sample)
        else:
            lines.append("- `(none)`")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def cleanup_note(payload: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# V41 Git Cleanup Note",
            "",
            f"- Generated UTC: `{payload['generated_utc']}`",
            f"- Active branch head at note time: `{payload['current_head_sha']}`",
            f"- Accidental merge retained as historical context: `{ACCIDENTAL_MERGE_SHA}`",
            "- Cleanup posture: `forward_only`.",
            "- History repair actions intentionally skipped: `git reset`, `git rebase`, and merge rewrite were not used.",
            "- Publication posture: only the curated V41 allowlist should be staged, committed, pushed, and used for PR updates.",
            "- The large dirty tree is treated as carried-forward latest-state churn plus non-stage noise unless a path is explicitly named in the V41 allowlist.",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute the curated V41 stage allowlist.")
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

    intended = set(INTENDED_V41_PATHS)
    classification_counts = {
        "intended_v41_delta": 0,
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
        "phase": "v41_omega",
        "current_head_sha": git_head(),
        "curation_rule": "v41_only_forward_cleanup_stage_set",
        "dirty_path_count": len(dirty_paths),
        "curated_include_count": len(INTENDED_V41_PATHS),
        "intended_v41_paths": [path_status(path) for path in INTENDED_V41_PATHS],
        "curated_include_paths": list(INTENDED_V41_PATHS),
        "classification_counts": classification_counts,
        "classification_samples": classification_samples,
        "accidental_merge_sha": ACCIDENTAL_MERGE_SHA,
        "cleanup_posture": "forward_only",
    }
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    write_text(Path(args.cleanup_note), cleanup_note(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
