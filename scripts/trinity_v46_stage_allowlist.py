#!/usr/bin/env python3
"""Compute the curated V46 publication allowlist."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from trinity_v46_common import ROOT, git_head, git_status_lines, git_tracked, now_iso, write_json, write_text
from trinity_v46_cleanup_classifier import classify

DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v46-stage-allowlist-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v46-stage-allowlist-v1.md"
DEFAULT_NOTE = ROOT / "docs" / "trinity-live-traces" / "v46-git-cleanup-note-v1.md"

INTENDED_V46_PATHS = [
    "scripts/publish_v46_omega_surfaces.py",
    "scripts/trinity_v46_capability_digest.py",
    "scripts/trinity_v46_cleanup_classifier.py",
    "scripts/trinity_v46_cli_slot40_induction.py",
    "scripts/trinity_v46_common.py",
    "scripts/trinity_v46_git_publication_result.py",
    "scripts/trinity_v46_operator_probe.py",
    "scripts/trinity_v46_stage_allowlist.py",
    "docs/trinity-live-traces/v46-app-cli-capability-digest-v1.json",
    "docs/trinity-live-traces/v46-app-cli-capability-digest-v1.md",
    "docs/trinity-live-traces/v46-cleanup-classifier-v1.json",
    "docs/trinity-live-traces/v46-cleanup-classifier-v1.md",
    "docs/trinity-live-traces/v46-codex-cli-slot40-induction-v1.json",
    "docs/trinity-live-traces/v46-codex-cli-slot40-induction-v1.md",
    "docs/trinity-live-traces/v46-git-cleanup-note-v1.md",
    "docs/trinity-live-traces/v46-git-publication-result-v1.json",
    "docs/trinity-live-traces/v46-git-publication-result-v1.md",
    "docs/trinity-live-traces/v46-operator-probe-v1.json",
    "docs/trinity-live-traces/v46-operator-probe-v1.md",
    "docs/trinity-live-traces/v46-plugin-surface-digest-v1.json",
    "docs/trinity-live-traces/v46-plugin-surface-digest-v1.md",
    "docs/trinity-live-traces/v46-quick-suite-status.json",
    "docs/trinity-live-traces/v46-standard-suite-status.json",
    "docs/trinity-live-traces/v46-deep-suite-status.json",
    "docs/trinity-live-traces/v46-slot-40-codex-cli-induction-proof-v1.json",
    "docs/trinity-live-traces/v46-slot-40-codex-cli-induction-proof-v1.md",
    "docs/trinity-live-traces/v46-stage-allowlist-v1.json",
    "docs/trinity-live-traces/v46-stage-allowlist-v1.md",
    "docs/trinity-agent-role-contracts/40-ari-role-contract.json",
    "docs/trinity-freed-id-certificates/40-ari.json",
    "docs/trinity-agent-memory-ledgers/40-ari-memory-log.jsonl",
    "docs/trinity-agent-reflections/40-ari-latest.md",
    "docs/trinity-runtime-model-resolution-v1.json",
    "docs/v17-runtime-session-log-latest.json",
    "docs/v17-runtime-session-validation-latest.json",
    "docs/v17-runtime-truth-resolution-board-v1.json",
    "docs/v46-omega-closeout-summary-v1.json",
    "docs/v46-omega-continuity-pack-v1.md",
    "docs/v46-omega-handoff-policy-v1.json",
    "docs/v46-powershell-operator-note-v1.md",
    "docs/v47-beta-closeout-summary-v1.json",
    "docs/v47-beta-continuity-pack-v1.md",
    "docs/v47-beta-handoff-policy-v1.json",
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
        "# V46 Stage Allowlist",
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
    lines.extend(["", "## Intended Paths", ""])
    lines.extend(f"- `{row['path']}` (`present={row['present']}`, `tracked={row['tracked']}`)" for row in payload["intended_v46_paths"])
    return "\n".join(lines).rstrip() + "\n"


def cleanup_note(payload: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# V46 Git Cleanup Note",
            "",
            f"- Generated UTC: `{payload['generated_utc']}`",
            f"- Active head: `{payload['current_head_sha']}`",
            "- Cleanup posture: `forward_only_allowlist_only`.",
            "- Stage only curated V46 outputs. Leave suite-generated tracked churn unstaged unless it appears in this allowlist.",
            "- Delete only untracked generated junk after D-drive backup through `trinity_v46_cleanup_classifier.py --apply`.",
        ]
    ) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute the curated V46 stage allowlist.")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    parser.add_argument("--cleanup-note", default=str(DEFAULT_NOTE))
    args = parser.parse_args()

    counts = {
        "intended_v46_delta": 0,
        "safe_generated_cache": 0,
        "suite_generated_churn": 0,
        "candidate_archive_then_remove": 0,
        "preserve_unstaged": 0,
    }
    samples = {key: [] for key in counts}
    for line in git_status_lines():
        code, path = _status_path(line)
        label = "intended_v46_delta" if path in set(INTENDED_V46_PATHS) else classify(path, code)
        counts[label] += 1
        if len(samples[label]) < 80:
            samples[label].append(path)

    payload = {
        "generated_utc": now_iso(),
        "phase": "v46_omega",
        "current_head_sha": git_head(),
        "curation_rule": "v46_only_forward_cleanup_stage_set",
        "dirty_path_count": sum(counts.values()),
        "curated_include_count": len(INTENDED_V46_PATHS),
        "intended_v46_paths": [_path_status(path) for path in INTENDED_V46_PATHS],
        "curated_include_paths": INTENDED_V46_PATHS,
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
