#!/usr/bin/env python3
"""Classify V47 dirty files and safely archive/remove only generated untracked junk."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import Any

from trinity_v47_common import ROOT, V47_CLEANUP_BACKUP_ROOT, git_head, git_status_lines, now_iso, write_json, write_text

DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v47-cleanup-classifier-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v47-cleanup-classifier-v1.md"
INTENDED_PREFIXES = (
    "scripts/trinity_v47_",
    "scripts/publish_v47_",
    "docs/trinity-live-traces/v47-",
    "docs/v47-",
    "docs/v48-",
    "docs/trinity-agent-reflections/v47-",
)
RUNTIME_TRUTH = {
    "docs/trinity-runtime-model-resolution-v1.json",
    "docs/v17-runtime-session-log-latest.json",
    "docs/v17-runtime-session-validation-latest.json",
    "docs/v17-runtime-truth-resolution-board-v1.json",
}


def _status_path(line: str) -> tuple[str, str]:
    code = line[:2].strip() or "?"
    path = line[3:].strip()
    if path.startswith('"') and path.endswith('"'):
        path = path[1:-1]
    return code, path.replace("\\", "/")


def classify(path: str, code: str) -> str:
    if path in RUNTIME_TRUTH or any(path.startswith(prefix) for prefix in INTENDED_PREFIXES):
        return "intended_v47_delta"
    if code == "??" and (path.endswith(".pyc") or "__pycache__/" in path or path.startswith(".local-runtime/")):
        return "candidate_archive_then_remove"
    if path.endswith(".pyc") or "__pycache__/" in path:
        return "safe_generated_cache"
    if path.startswith("docs/trinity-live-traces/") or path.startswith("docs/trinity-expansion/") or path.startswith("docs/trinity-mcp-cache/"):
        return "suite_generated_churn"
    if path.startswith("docs/") and ("-latest." in path or path.endswith(".jsonl") or "/logs/" in path or path.endswith("-status.json")):
        return "suite_generated_churn"
    return "preserve_unstaged"


def _remove(rel_path: str, backup_root: Path) -> str:
    src = ROOT / rel_path
    if not src.exists():
        return "missing"
    dest = backup_root / rel_path
    dest.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(src, dest)
        shutil.rmtree(src)
        return "directory_archived_removed"
    shutil.copy2(src, dest)
    src.unlink()
    return "file_archived_removed"


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V47 Cleanup Classifier",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Cleanup state: `{payload['v47_cleanup_state']}`",
        f"- Dirty path count: `{payload['dirty_path_count']}`",
        "",
        "## Classification Counts",
        "",
    ]
    lines.extend(f"- `{key}`: `{value}`" for key, value in payload["classification_counts"].items())
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Classify V47 dirty files.")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()
    rows = []
    counts = {key: 0 for key in ["intended_v47_delta", "safe_generated_cache", "suite_generated_churn", "candidate_archive_then_remove", "preserve_unstaged"]}
    samples = {key: [] for key in counts}
    for line in git_status_lines():
        code, path = _status_path(line)
        label = classify(path, code)
        counts[label] += 1
        if len(samples[label]) < 80:
            samples[label].append(path)
        rows.append({"status": code, "path": path, "classification": label})
    backup_root = V47_CLEANUP_BACKUP_ROOT / now_iso().replace(":", "").replace("+", "")
    removals = []
    if args.apply:
        for row in rows:
            if row["classification"] == "candidate_archive_then_remove":
                removals.append({"path": row["path"], "result": _remove(row["path"], backup_root)})
    payload = {
        "generated_utc": now_iso(),
        "phase": "v47_omega",
        "overall_status": "PASS",
        "current_head_sha": git_head(),
        "apply_cleanup": bool(args.apply),
        "v47_cleanup_state": "safe_untracked_junk_archived_removed" if removals else "classified_only_no_deletion_needed",
        "backup_root": str(backup_root) if removals else "",
        "dirty_path_count": len(rows),
        "classification_counts": counts,
        "classification_samples": samples,
        "removal_results": removals,
        "cleanup_policy": "archive_then_remove_only_untracked_generated_junk_never_reset_tracked_churn",
    }
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
