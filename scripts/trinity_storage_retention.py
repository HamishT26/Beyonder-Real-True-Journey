#!/usr/bin/env python3
"""Prune stale generated Trinity artifacts while preserving authoritative state."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent
WORKBENCH_ROOT = Path(r"C:\Users\hamis\OneDrive\Documents\New project")
POLICY_PATH = ROOT / "docs" / "trinity-retention-policy-v1.json"
STAMP_RE = re.compile(r"^(?P<stamp>\d{8}T\d{6}Z)-")
RUN_DIRS = [
    ROOT / "docs" / "trinity-expansion-runs",
    ROOT / "docs" / "trinity-mandala-runs",
    ROOT / "docs" / "trinity-extension-catalog-runs",
    ROOT / "docs" / "trinity-materialization-ladder-runs",
    ROOT / "docs" / "trinity-materialization-ledger-runs",
    ROOT / "docs" / "trinity-journey-corpus-runs",
    ROOT / "docs" / "trinity-public-research-runs",
    ROOT / "docs" / "trinity-public-signal-runs",
    ROOT / "docs" / "body-track-runs",
    ROOT / "docs" / "heart-track-runs",
    ROOT / "docs" / "mind-track-runs",
    ROOT / "docs" / "trinity-agent-council-runs",
]
ARCHIVE_DIR = ROOT / "docs" / "memory-archives"
OUTPUT_JSON = ROOT / "docs" / "trinity-storage-prune-latest.json"
OUTPUT_MD = ROOT / "docs" / "trinity-storage-prune-latest.md"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _iter_stamped_files(path: Path) -> dict[str, list[Path]]:
    grouped: dict[str, list[Path]] = defaultdict(list)
    for child in path.iterdir():
        if not child.is_file():
            continue
        match = STAMP_RE.match(child.name)
        if match:
            grouped[match.group("stamp")].append(child)
    return grouped


def prune_dir(path: Path, keep_stamps: int, dry_run: bool) -> dict[str, object]:
    grouped = _iter_stamped_files(path)
    kept = sorted(grouped.keys(), reverse=True)[:keep_stamps]
    deleted_files = 0
    reclaimed_bytes = 0
    deleted_paths: list[str] = []
    for stamp, files in grouped.items():
        if stamp in kept:
            continue
        for file_path in files:
            try:
                reclaimed_bytes += file_path.stat().st_size
            except OSError:
                pass
            deleted_paths.append(str(file_path.relative_to(ROOT)).replace("\\", "/"))
            if not dry_run:
                file_path.unlink(missing_ok=True)
            deleted_files += 1
    return {
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "kept_stamps": kept,
        "deleted_files": deleted_files,
        "reclaimed_mb": round(reclaimed_bytes / (1024 * 1024), 2),
        "deleted_paths": deleted_paths,
    }


def prune_archives(path: Path, keep_archives: int, dry_run: bool) -> dict[str, object]:
    archives = sorted([child for child in path.glob("*.zip") if child.is_file()], key=lambda item: item.stat().st_mtime, reverse=True)
    kept = [file_path.name for file_path in archives[:keep_archives]]
    deleted_files = 0
    reclaimed_bytes = 0
    deleted_paths: list[str] = []
    for file_path in archives[keep_archives:]:
        reclaimed_bytes += file_path.stat().st_size
        deleted_paths.append(str(file_path.relative_to(ROOT)).replace("\\", "/"))
        if not dry_run:
            file_path.unlink(missing_ok=True)
        deleted_files += 1
    return {
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "kept_archives": kept,
        "deleted_files": deleted_files,
        "reclaimed_mb": round(reclaimed_bytes / (1024 * 1024), 2),
        "deleted_paths": deleted_paths,
    }


def prune_pycache(paths: Iterable[Path], dry_run: bool) -> dict[str, object]:
    deleted_dirs = 0
    reclaimed_bytes = 0
    deleted_paths: list[str] = []
    for root in paths:
        if not root.exists():
            continue
        for cache_dir in root.rglob("__pycache__"):
            if not cache_dir.is_dir():
                continue
            try:
                reclaimed_bytes += sum(item.stat().st_size for item in cache_dir.rglob("*") if item.is_file())
            except OSError:
                pass
            deleted_paths.append(str(cache_dir).replace("\\", "/"))
            if not dry_run:
                shutil.rmtree(cache_dir, ignore_errors=True)
            deleted_dirs += 1
    return {
        "deleted_dirs": deleted_dirs,
        "reclaimed_mb": round(reclaimed_bytes / (1024 * 1024), 2),
        "deleted_paths": deleted_paths,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Prune old timestamped Trinity run artifacts.")
    parser.add_argument("--keep-stamps", type=int, default=2)
    parser.add_argument("--keep-archives", type=int, default=3)
    parser.add_argument("--clear-pycache", action="store_true")
    parser.add_argument(
        "--include-workbench-pycache",
        action="store_true",
        help="Also clear __pycache__ from the separate OneDrive workbench. Defaults to repo-only cleanup.",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if POLICY_PATH.exists():
        retention_policy = load_json(POLICY_PATH)
    else:
        retention_policy = {
            "authority_preserve": [],
            "retain_latest_per_run_family": max(args.keep_stamps, 1),
            "retain_latest_memory_archives": max(args.keep_archives, 1),
            "safe_to_prune": ["stale_timestamped_run_outputs", "disposable_temp_archives", "__pycache__"],
        }

    before_free = round(shutil.disk_usage(ROOT).free / (1024**3), 2)
    rows: list[dict[str, object]] = []
    total_deleted = 0
    total_reclaimed = 0.0
    for run_dir in RUN_DIRS:
        if not run_dir.exists():
            continue
        row = prune_dir(run_dir, max(args.keep_stamps, 1), args.dry_run)
        rows.append(row)
        total_deleted += int(row["deleted_files"])
        total_reclaimed += float(row["reclaimed_mb"])

    archive_row = {"path": str(ARCHIVE_DIR.relative_to(ROOT)).replace("\\", "/"), "kept_archives": [], "deleted_files": 0, "reclaimed_mb": 0.0, "deleted_paths": []}
    if ARCHIVE_DIR.exists():
        archive_row = prune_archives(ARCHIVE_DIR, max(args.keep_archives, 1), args.dry_run)
        total_deleted += int(archive_row["deleted_files"])
        total_reclaimed += float(archive_row["reclaimed_mb"])

    pycache_row = {"deleted_dirs": 0, "reclaimed_mb": 0.0, "deleted_paths": []}
    if args.clear_pycache:
        pycache_roots = [ROOT]
        if args.include_workbench_pycache:
            pycache_roots.append(WORKBENCH_ROOT)
        pycache_row = prune_pycache(pycache_roots, args.dry_run)
        total_reclaimed += float(pycache_row["reclaimed_mb"])

    after_free = round(shutil.disk_usage(ROOT).free / (1024**3), 2)
    payload = {
        "generated_utc": now_iso(),
        "overall_status": "PASS",
        "dry_run": args.dry_run,
        "keep_stamps": max(args.keep_stamps, 1),
        "keep_archives": max(args.keep_archives, 1),
        "free_gib_before": before_free,
        "free_gib_after": after_free,
        "free_gib_delta": round(after_free - before_free, 2),
        "deleted_files": total_deleted,
        "reclaimed_mb": round(total_reclaimed, 2),
        "retention_policy": retention_policy,
        "canonical_records": retention_policy.get("authority_preserve", []),
        "retained_history": {
            "run_family_keep_stamps": max(args.keep_stamps, 1),
            "memory_archive_keep_count": max(args.keep_archives, 1),
            "run_families": [
                {
                    "path": row["path"],
                    "kept_stamps": row["kept_stamps"],
                }
                for row in rows
            ],
            "kept_archives": archive_row.get("kept_archives", []),
        },
        "interrupted_run_outputs": {
            "deleted_paths": [
                path
                for row in rows
                for path in row.get("deleted_paths", [])
            ] + archive_row.get("deleted_paths", []),
            "deleted_files": total_deleted,
        },
        "disposable_cache_artifacts": {
            "deleted_paths": pycache_row.get("deleted_paths", []),
            "deleted_dirs": pycache_row.get("deleted_dirs", 0),
        },
        "run_families": rows,
        "archive_retention": archive_row,
        "pycache_cleanup": pycache_row,
    }
    write_json(OUTPUT_JSON, payload)

    lines = [
        "# Trinity Storage Prune",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- dry_run: `{payload['dry_run']}`",
        f"- deleted_files: `{payload['deleted_files']}`",
        f"- reclaimed_mb: `{payload['reclaimed_mb']}`",
        f"- free_gib_before: `{payload['free_gib_before']}`",
        f"- free_gib_after: `{payload['free_gib_after']}`",
        f"- free_gib_delta: `{payload['free_gib_delta']}`",
        "",
        "## Retention classes",
        f"- canonical_records: `{', '.join(payload['canonical_records']) or '-'}`",
        f"- retained_history_run_stamps: `{payload['retained_history']['run_family_keep_stamps']}`",
        f"- retained_history_archives: `{payload['retained_history']['memory_archive_keep_count']}`",
        f"- interrupted_run_outputs_deleted_files: `{payload['interrupted_run_outputs']['deleted_files']}`",
        f"- disposable_cache_dirs: `{payload['disposable_cache_artifacts']['deleted_dirs']}`",
        "",
        "## Run families",
    ]
    for row in rows:
        lines.append(f"- `{row['path']}`: deleted={row['deleted_files']} reclaimed_mb={row['reclaimed_mb']}")
    lines.extend(
        [
            "",
            "## Archives",
            f"- kept_archives: `{', '.join(archive_row.get('kept_archives', [])) or '-'}`",
            f"- deleted_files: `{archive_row.get('deleted_files', 0)}`",
            f"- reclaimed_mb: `{archive_row.get('reclaimed_mb', 0.0)}`",
            "",
            "## Pycache",
            f"- deleted_dirs: `{pycache_row.get('deleted_dirs', 0)}`",
            f"- reclaimed_mb: `{pycache_row.get('reclaimed_mb', 0.0)}`",
        ]
    )
    write_text(OUTPUT_MD, "\n".join(lines).rstrip() + "\n")

    print(f"deleted_files={payload['deleted_files']}")
    print(f"reclaimed_mb={payload['reclaimed_mb']}")
    print(f"free_gib_delta={payload['free_gib_delta']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
