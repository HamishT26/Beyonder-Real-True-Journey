#!/usr/bin/env python3
"""Classify V48 cleanup targets and remove only backup-proven generated runtime junk."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import Any

from trinity_v48_common import (
    AUTHORITATIVE_REPO,
    ROOT,
    V48_CLEANUP_BACKUP_ROOT,
    dir_size_bytes,
    ensure_archive_roots,
    git_head,
    git_status_lines,
    git_tracked,
    now_iso,
    write_json,
    write_text,
)

DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v48-cleanup-classifier-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v48-cleanup-classifier-v1.md"

INTENDED_PREFIXES = (
    "scripts/trinity_v48_",
    "scripts/publish_v48_",
    "docs/trinity-live-traces/v48-",
    "docs/auto-generated/v48-",
    "docs/v48-",
    "docs/v49-",
    "docs/trinity-agent-reflections/v48-",
    "templates/v48-control-plane/",
    ".circleci/",
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
        return "intended_v48_delta"
    if code == "??" and (path.startswith(".local-runtime/") or "__pycache__/" in path or path.endswith(".pyc")):
        return "candidate_archive_then_remove"
    if path.endswith(".pyc") or "__pycache__/" in path:
        return "safe_generated_cache"
    if path.startswith("docs/trinity-live-traces/") or path.startswith("docs/trinity-expansion/") or path.startswith("docs/trinity-mcp-cache/"):
        return "suite_generated_churn"
    if path.startswith("docs/") and ("-latest." in path or path.endswith(".jsonl") or "/logs/" in path or path.endswith("-status.json")):
        return "suite_generated_churn"
    return "preserve_unstaged"


def _safe_archive_remove(path: Path, allowed_root: Path, backup_root: Path) -> dict[str, Any]:
    resolved = path.resolve()
    allowed = allowed_root.resolve()
    if resolved != allowed and allowed not in resolved.parents:
        return {"path": str(path), "result": "blocked_outside_allowed_root"}
    if not path.exists():
        return {"path": str(path), "result": "missing"}
    before = dir_size_bytes(path)
    dest = backup_root / path.name
    if dest.exists():
        if dest.is_dir():
            shutil.rmtree(dest)
        else:
            dest.unlink()
    dest.parent.mkdir(parents=True, exist_ok=True)
    if path.is_dir():
        shutil.copytree(path, dest)
        shutil.rmtree(path)
        result = "directory_archived_removed"
    else:
        shutil.copy2(path, dest)
        path.unlink()
        result = "file_archived_removed"
    return {"path": str(path), "backup": str(dest), "bytes_removed": before, "result": result}


def _repo_targets() -> list[dict[str, Any]]:
    targets = [
        {
            "name": "authoritative_local_runtime",
            "path": AUTHORITATIVE_REPO / ".local-runtime",
            "classification": "candidate_archive_then_remove",
            "reason": "untracked generated runtime cache in non-execution C checkout",
            "tracked": bool(git_tracked(".local-runtime", cwd=AUTHORITATIVE_REPO)),
        },
        {
            "name": "v48_local_runtime",
            "path": ROOT / ".local-runtime" / "v48",
            "classification": "preserve_current_phase_runtime",
            "reason": "current phase runtime evidence",
            "tracked": False,
        },
    ]
    for row in targets:
        row["present"] = row["path"].exists()
        row["size_mb"] = round(dir_size_bytes(row["path"]) / (1024 * 1024), 2)
    return targets


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V48 Cleanup Classifier",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Cleanup state: `{payload['local_archive_cleanup_state']}`",
        f"- Dirty path count: `{payload['dirty_path_count']}`",
        f"- Bytes removed: `{payload['bytes_removed']}`",
        "",
        "## Classification Counts",
        "",
    ]
    lines.extend(f"- `{key}`: `{value}`" for key, value in payload["classification_counts"].items())
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Classify and optionally apply V48 cleanup.")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()
    ensure_archive_roots()
    rows = []
    counts = {key: 0 for key in ["intended_v48_delta", "safe_generated_cache", "suite_generated_churn", "candidate_archive_then_remove", "preserve_unstaged"]}
    samples = {key: [] for key in counts}
    for line in git_status_lines():
        code, path = _status_path(line)
        label = classify(path, code)
        counts[label] += 1
        if len(samples[label]) < 80:
            samples[label].append(path)
        rows.append({"status": code, "path": path, "classification": label})
    backup_root = V48_CLEANUP_BACKUP_ROOT / now_iso().replace(":", "").replace("+", "")
    repo_targets = _repo_targets()
    removals: list[dict[str, Any]] = []
    if args.apply:
        for target in repo_targets:
            if target["name"] == "authoritative_local_runtime" and target["present"] and not target["tracked"]:
                removals.append(_safe_archive_remove(target["path"], AUTHORITATIVE_REPO, backup_root / "authoritative-repo"))
    bytes_removed = sum(int(row.get("bytes_removed", 0) or 0) for row in removals)
    state = "generated_runtime_archived_removed" if removals else "classified_only_no_deletion_needed"
    payload = {
        "generated_utc": now_iso(),
        "phase": "v48_omega",
        "overall_status": "PASS",
        "current_head_sha": git_head(),
        "apply_cleanup": bool(args.apply),
        "local_archive_cleanup_state": state,
        "archive_calibration_state": "d_drive_roots_ready_c_repo_runtime_manifested",
        "backup_root": str(backup_root) if removals else "",
        "dirty_path_count": len(rows),
        "classification_counts": counts,
        "classification_samples": samples,
        "cleanup_targets": repo_targets,
        "removal_results": removals,
        "bytes_removed": bytes_removed,
        "mb_removed": round(bytes_removed / (1024 * 1024), 2),
        "cleanup_policy": "backup_then_remove_only_untracked_generated_runtime_never_reset_tracked_churn",
    }
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
