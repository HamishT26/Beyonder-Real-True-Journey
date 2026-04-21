#!/usr/bin/env python3
"""Classify V46 dirty files and optionally archive/remove safe untracked junk."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import Any

from trinity_v46_common import ROOT, V46_CLEANUP_BACKUP_ROOT, git_head, git_status_lines, now_iso, write_json, write_text

DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v46-cleanup-classifier-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v46-cleanup-classifier-v1.md"

INTENDED_PREFIXES = (
    "scripts/trinity_v46_",
    "scripts/publish_v46_",
    "docs/trinity-live-traces/v46-",
    "docs/v46-",
    "docs/v47-",
    "docs/trinity-agent-role-contracts/40-",
    "docs/trinity-freed-id-certificates/40-",
    "docs/trinity-agent-memory-ledgers/40-",
    "docs/trinity-agent-reflections/40-",
)
RUNTIME_TRUTH_PATHS = {
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
    if path in RUNTIME_TRUTH_PATHS or any(path.startswith(prefix) for prefix in INTENDED_PREFIXES):
        return "intended_v46_delta"
    if code == "??" and (path.endswith(".pyc") or "__pycache__/" in path or path.startswith(".local-runtime/")):
        return "candidate_archive_then_remove"
    if path.endswith(".pyc") or "__pycache__/" in path:
        return "safe_generated_cache"
    if path.startswith(".local-runtime/"):
        return "candidate_archive_then_remove" if code == "??" else "safe_generated_cache"
    if path.startswith("docs/trinity-live-traces/") or path.startswith("docs/trinity-expansion/") or path.startswith("docs/trinity-mcp-cache/"):
        return "suite_generated_churn"
    if path.startswith("docs/") and ("-latest." in path or path.endswith(".jsonl") or "/logs/" in path or path.endswith("-status.json")):
        return "suite_generated_churn"
    return "preserve_unstaged"


def _backup_and_remove(rel_path: str, backup_root: Path) -> str:
    src = ROOT / rel_path
    if not src.exists():
        return "missing"
    dst = backup_root / rel_path
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        shutil.rmtree(src)
        return "directory_archived_removed"
    shutil.copy2(src, dst)
    src.unlink()
    return "file_archived_removed"


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V46 Cleanup Classifier",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Apply cleanup: `{payload['apply_cleanup']}`",
        f"- Cleanup state: `{payload['v46_cleanup_state']}`",
        f"- Dirty path count: `{payload['dirty_path_count']}`",
        "",
        "## Classification Counts",
        "",
    ]
    lines.extend(f"- `{key}`: `{value}`" for key, value in payload["classification_counts"].items())
    if payload.get("removal_results"):
        lines.extend(["", "## Archived Removals", ""])
        lines.extend(f"- `{row['path']}`: `{row['result']}`" for row in payload["removal_results"])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Classify V46 dirty files.")
    parser.add_argument("--apply", action="store_true", help="Archive and remove safe untracked generated junk.")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()

    rows = []
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
        label = classify(path, code)
        counts[label] += 1
        if len(samples[label]) < 80:
            samples[label].append(path)
        rows.append({"status": code, "path": path, "classification": label})

    removal_results: list[dict[str, str]] = []
    backup_root = V46_CLEANUP_BACKUP_ROOT / now_iso().replace(":", "").replace("+", "")
    if args.apply:
        for row in rows:
            if row["classification"] != "candidate_archive_then_remove":
                continue
            removal_results.append({"path": row["path"], "result": _backup_and_remove(row["path"], backup_root)})

    cleanup_state = "safe_untracked_junk_archived_removed" if args.apply and removal_results else "classified_only_no_deletion_needed"
    if args.apply and counts["candidate_archive_then_remove"] and not removal_results:
        cleanup_state = "cleanup_apply_attempted_no_removals"

    payload = {
        "generated_utc": now_iso(),
        "phase": "v46_omega",
        "overall_status": "PASS",
        "current_head_sha": git_head(),
        "apply_cleanup": bool(args.apply),
        "v46_cleanup_state": cleanup_state,
        "backup_root": str(backup_root) if removal_results else "",
        "dirty_path_count": len(rows),
        "classification_counts": counts,
        "classification_samples": samples,
        "removal_results": removal_results,
        "cleanup_policy": "archive_then_remove_only_untracked_generated_junk_never_reset_tracked_churn",
    }
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
