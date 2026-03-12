#!/usr/bin/env python3
"""Prune non-authoritative timestamped Trinity run artifacts."""

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
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
]


def prune_dir(path: Path, keep_stamps: int) -> dict[str, object]:
    grouped: dict[str, list[Path]] = defaultdict(list)
    for child in path.iterdir():
        if not child.is_file():
            continue
        match = STAMP_RE.match(child.name)
        if not match:
            continue
        grouped[match.group("stamp")].append(child)

    kept = sorted(grouped.keys(), reverse=True)[:keep_stamps]
    deleted_files = 0
    reclaimed_bytes = 0
    for stamp, files in grouped.items():
        if stamp in kept:
            continue
        for file_path in files:
            try:
                reclaimed_bytes += file_path.stat().st_size
            except OSError:
                pass
            file_path.unlink(missing_ok=True)
            deleted_files += 1

    return {
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "kept_stamps": kept,
        "deleted_files": deleted_files,
        "reclaimed_mb": round(reclaimed_bytes / (1024 * 1024), 2),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Prune old timestamped Trinity run artifacts.")
    parser.add_argument("--keep-stamps", type=int, default=2)
    args = parser.parse_args()

    rows: list[dict[str, object]] = []
    total_deleted = 0
    total_reclaimed = 0.0
    for run_dir in RUN_DIRS:
        if not run_dir.exists():
            continue
        row = prune_dir(run_dir, max(args.keep_stamps, 1))
        rows.append(row)
        total_deleted += int(row["deleted_files"])
        total_reclaimed += float(row["reclaimed_mb"])

    print(f"deleted_files={total_deleted}")
    print(f"reclaimed_mb={round(total_reclaimed, 2)}")
    for row in rows:
        print(f"{row['path']}: deleted={row['deleted_files']} reclaimed_mb={row['reclaimed_mb']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
