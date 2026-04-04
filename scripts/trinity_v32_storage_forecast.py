#!/usr/bin/env python3
"""Forecast local storage pressure before the memory-bank watch band trips."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from statistics import median
from typing import Any

from trinity_v32_runtime_common import now_iso, write_json, write_text

ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = ROOT / "docs" / "memory-archives" / "index.jsonl"
PRUNE_PATH = ROOT / "docs" / "trinity-storage-prune-latest.json"
OUTPUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v32-storage-forecast-proof-v1.json"
OUTPUT_MD = ROOT / "docs" / "trinity-live-traces" / "v32-storage-forecast-proof-v1.md"
WATCH_GIB = 4.0
CRITICAL_GIB = 2.0


def read_index_sizes() -> list[float]:
    sizes: list[float] = []
    if not INDEX_PATH.exists():
        return sizes
    for line in INDEX_PATH.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        try:
            row = json.loads(stripped)
        except json.JSONDecodeError:
            continue
        archive_rel = str(row.get("archive", ""))
        if not archive_rel:
            continue
        archive_path = ROOT / archive_rel
        if archive_path.exists():
            sizes.append(round(archive_path.stat().st_size / (1024 * 1024), 2))
    return sizes


def write_outputs(payload: dict[str, Any]) -> None:
    write_json(OUTPUT_JSON, payload)
    lines = [
        "# V32 Storage Forecast",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Pressure class: `{payload['storage_pressure_class']}`",
        f"- Free GiB: `{payload['free_gib']}`",
        f"- Headroom to watch band GiB: `{payload['watch_headroom_gib']}`",
        f"- Estimated additional archives until watch: `{payload['estimated_additional_archives_until_watch']}`",
        "",
        "## Recommendations",
        "",
    ]
    for item in payload.get("recommendations", []):
        lines.append(f"- {item}")
    write_text(OUTPUT_MD, "\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Forecast Trinity storage pressure.")
    parser.add_argument("--watch-gib", type=float, default=WATCH_GIB)
    parser.add_argument("--critical-gib", type=float, default=CRITICAL_GIB)
    args = parser.parse_args()

    disk = shutil.disk_usage(ROOT)
    free_gib = round(disk.free / (1024**3), 2)
    sizes = read_index_sizes()
    median_archive_mb = round(median(sizes[-20:]), 2) if sizes else 0.0
    headroom_gib = round(max(free_gib - args.watch_gib, 0.0), 2)
    if free_gib < args.critical_gib:
        pressure = "critical"
    elif free_gib < args.watch_gib:
        pressure = "watch"
    else:
        pressure = "healthy"
    estimated_archives = 0
    if median_archive_mb > 0 and headroom_gib > 0:
        estimated_archives = int((headroom_gib * 1024) // median_archive_mb)

    prune_generated = ""
    if PRUNE_PATH.exists():
        try:
            prune_generated = str(json.loads(PRUNE_PATH.read_text(encoding="utf-8")).get("generated_utc", ""))
        except json.JSONDecodeError:
            prune_generated = ""

    payload = {
        "generated_utc": now_iso(),
        "phase": "v32_omega",
        "overall_status": "PASS" if pressure == "healthy" else "WARN",
        "storage_pressure_class": pressure,
        "free_gib": free_gib,
        "watch_headroom_gib": headroom_gib,
        "critical_gib": args.critical_gib,
        "watch_gib": args.watch_gib,
        "median_archive_mb_last_20": median_archive_mb,
        "estimated_additional_archives_until_watch": estimated_archives,
        "archive_count_indexed": len(sizes),
        "latest_prune_generated_utc": prune_generated,
        "recommendations": [
            "Run the bounded session-closeout wrapper before free space falls into the watch band.",
            "Keep workbench cleanup opt-in and preserve repo-first authority during prune cycles.",
            "Prefer mirroring archives and proof outputs to OneDrive or GCS instead of shifting repo truth files.",
        ],
    }
    write_outputs(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
