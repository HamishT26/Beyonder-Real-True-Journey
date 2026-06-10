#!/usr/bin/env python3
"""Compute the curated V47 publication allowlist."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from trinity_v47_cleanup_classifier import classify
from trinity_v47_common import ROOT, git_head, git_status_lines, git_tracked, now_iso, write_json, write_text

DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v47-stage-allowlist-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v47-stage-allowlist-v1.md"
DEFAULT_NOTE = ROOT / "docs" / "trinity-live-traces" / "v47-git-cleanup-note-v1.md"
INTENDED_V47_PATHS = [
    "scripts/publish_v47_omega_surfaces.py",
    "scripts/trinity_v47_ari_colearning_probe.py",
    "scripts/trinity_v47_cleanup_classifier.py",
    "scripts/trinity_v47_codex_home_hygiene.py",
    "scripts/trinity_v47_common.py",
    "scripts/trinity_v47_git_publication_result.py",
    "scripts/trinity_v47_memory_capability_digest.py",
    "scripts/trinity_v47_operator_probe.py",
    "scripts/trinity_v47_stage_allowlist.py",
    "docs/trinity-agent-reflections/v47-aletheon-reflection-v1.md",
    "docs/trinity-agent-reflections/v47-ari-reflection-v1.md",
    "docs/trinity-live-traces/v47-ari-colearning-proof-v1.json",
    "docs/trinity-live-traces/v47-ari-colearning-proof-v1.md",
    "docs/trinity-live-traces/v47-cleanup-classifier-v1.json",
    "docs/trinity-live-traces/v47-cleanup-classifier-v1.md",
    "docs/trinity-live-traces/v47-codex-home-hygiene-v1.json",
    "docs/trinity-live-traces/v47-codex-home-hygiene-v1.md",
    "docs/trinity-live-traces/v47-codex-memory-capability-digest-v1.json",
    "docs/trinity-live-traces/v47-codex-memory-capability-digest-v1.md",
    "docs/trinity-live-traces/v47-deep-suite-status.json",
    "docs/trinity-live-traces/v47-git-cleanup-note-v1.md",
    "docs/trinity-live-traces/v47-git-publication-result-v1.json",
    "docs/trinity-live-traces/v47-git-publication-result-v1.md",
    "docs/trinity-live-traces/v47-operator-probe-v1.json",
    "docs/trinity-live-traces/v47-operator-probe-v1.md",
    "docs/trinity-live-traces/v47-plugin-surface-digest-v1.json",
    "docs/trinity-live-traces/v47-plugin-surface-digest-v1.md",
    "docs/trinity-live-traces/v47-quick-suite-status.json",
    "docs/trinity-live-traces/v47-stage-allowlist-v1.json",
    "docs/trinity-live-traces/v47-stage-allowlist-v1.md",
    "docs/trinity-live-traces/v47-standard-suite-status.json",
    "docs/trinity-runtime-model-resolution-v1.json",
    "docs/v17-runtime-session-log-latest.json",
    "docs/v17-runtime-session-validation-latest.json",
    "docs/v17-runtime-truth-resolution-board-v1.json",
    "docs/v47-omega-closeout-summary-v1.json",
    "docs/v47-omega-continuity-pack-v1.md",
    "docs/v47-omega-handoff-policy-v1.json",
    "docs/v47-powershell-operator-note-v1.md",
    "docs/v48-beta-closeout-summary-v1.json",
    "docs/v48-beta-continuity-pack-v1.md",
    "docs/v48-beta-handoff-policy-v1.json",
]


def _status_path(line: str) -> tuple[str, str]:
    code = line[:2].strip() or "?"
    path = line[3:].strip()
    if path.startswith('"') and path.endswith('"'):
        path = path[1:-1]
    return code, path.replace("\\", "/")


def _path_status(path: str) -> dict[str, Any]:
    return {"path": path, "present": (ROOT / path).exists(), "tracked": git_tracked(path)}


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V47 Stage Allowlist",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Current head: `{payload['current_head_sha']}`",
        f"- Dirty path count: `{payload['dirty_path_count']}`",
        f"- Curated include count: `{payload['curated_include_count']}`",
        "",
        "## Classification Counts",
        "",
    ]
    lines.extend(f"- `{key}`: `{value}`" for key, value in payload["classification_counts"].items())
    return "\n".join(lines).rstrip() + "\n"


def cleanup_note(payload: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# V47 Git Cleanup Note",
            "",
            f"- Generated UTC: `{payload['generated_utc']}`",
            f"- Active head: `{payload['current_head_sha']}`",
            "- Cleanup posture: `forward_only_allowlist_only`.",
            "- Stage only curated V47 outputs. Leave tracked suite churn unstaged unless allowlisted.",
            "- Delete only untracked/generated junk after D-drive backup.",
        ]
    ) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute the curated V47 stage allowlist.")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    parser.add_argument("--cleanup-note", default=str(DEFAULT_NOTE))
    args = parser.parse_args()
    intended = set(INTENDED_V47_PATHS)
    counts = {key: 0 for key in ["intended_v47_delta", "safe_generated_cache", "suite_generated_churn", "candidate_archive_then_remove", "preserve_unstaged"]}
    samples = {key: [] for key in counts}
    for line in git_status_lines():
        code, path = _status_path(line)
        label = "intended_v47_delta" if path in intended else classify(path, code)
        counts[label] += 1
        if len(samples[label]) < 80:
            samples[label].append(path)
    payload = {
        "generated_utc": now_iso(),
        "phase": "v47_omega",
        "current_head_sha": git_head(),
        "curation_rule": "v47_only_forward_cleanup_stage_set",
        "dirty_path_count": sum(counts.values()),
        "curated_include_count": len(INTENDED_V47_PATHS),
        "intended_v47_paths": [_path_status(path) for path in INTENDED_V47_PATHS],
        "curated_include_paths": INTENDED_V47_PATHS,
        "classification_counts": counts,
        "classification_samples": samples,
        "cleanup_posture": "forward_only_allowlist_only",
    }
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    write_text(Path(args.cleanup_note), cleanup_note(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
