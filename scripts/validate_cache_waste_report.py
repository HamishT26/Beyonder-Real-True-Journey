#!/usr/bin/env python3
"""Validate cache/waste regenerator reports.

Ensures the cache regenerator output schema remains stable and that purge
accounting is internally consistent before downstream reserve-bank ingestion.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_OUTPUT_KEYS = {
    "reclaimed_bytes": (0.0, None),
    "reclaimed_tokens": (0.0, None),
    "reclaimed_credits": (0.0, None),
    "reclaimed_energy_units": (0.0, None),
    "purged_bytes": (0.0, None),
    "purged_count": (0.0, None),
    "skipped_tracked_purge_count": (0.0, None),
}


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"missing report: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid json: {path}: {exc}") from exc


def check_numeric_outputs(outputs: dict) -> None:
    if not isinstance(outputs, dict):
        raise SystemExit("cache-regenerator: outputs must be an object")
    for key, (min_v, max_v) in REQUIRED_OUTPUT_KEYS.items():
        if key not in outputs:
            raise SystemExit(f"cache-regenerator: missing outputs.{key}")
        value = outputs[key]
        if not isinstance(value, (int, float)):
            raise SystemExit(f"cache-regenerator: outputs.{key} must be numeric")
        fval = float(value)
        if min_v is not None and fval < min_v:
            raise SystemExit(f"cache-regenerator: outputs.{key} must be >= {min_v}")
        if max_v is not None and fval > max_v:
            raise SystemExit(f"cache-regenerator: outputs.{key} must be <= {max_v}")


def check_items(outputs: dict) -> None:
    items = outputs.get("items")
    if not isinstance(items, list):
        raise SystemExit("cache-regenerator: outputs.items must be a list")

    purged_count = 0
    purged_bytes = 0
    skipped_tracked = 0
    reclaimed_bytes = 0
    for item in items:
        if not isinstance(item, dict):
            raise SystemExit("cache-regenerator: each outputs.items entry must be an object")
        for key in ("path", "bytes", "purged", "tracked", "purge_skipped_reason"):
            if key not in item:
                raise SystemExit(f"cache-regenerator: item missing key '{key}'")
        if not isinstance(item["path"], str) or not item["path"].strip():
            raise SystemExit("cache-regenerator: item.path must be a non-empty string")
        if not isinstance(item["bytes"], (int, float)) or float(item["bytes"]) < 0:
            raise SystemExit("cache-regenerator: item.bytes must be a non-negative number")
        if not isinstance(item["purged"], bool):
            raise SystemExit("cache-regenerator: item.purged must be boolean")
        if not isinstance(item["tracked"], bool):
            raise SystemExit("cache-regenerator: item.tracked must be boolean")
        if not isinstance(item["purge_skipped_reason"], str):
            raise SystemExit("cache-regenerator: item.purge_skipped_reason must be a string")

        if item["purge_skipped_reason"] and not item["tracked"]:
            raise SystemExit("cache-regenerator: purge_skipped_reason set for non-tracked item")
        if item["purge_skipped_reason"] == "tracked_path" and item["purged"]:
            raise SystemExit("cache-regenerator: tracked_path-skipped item cannot also be purged")

        reclaimed_bytes += int(item["bytes"])
        if item["purged"]:
            purged_count += 1
            purged_bytes += int(item["bytes"])
        if item["purge_skipped_reason"] == "tracked_path":
            skipped_tracked += 1

    if reclaimed_bytes != int(outputs["reclaimed_bytes"]):
        raise SystemExit("cache-regenerator: reclaimed_bytes does not match sum(item.bytes)")
    if purged_count != int(outputs["purged_count"]):
        raise SystemExit("cache-regenerator: purged_count does not match purged items")
    if purged_bytes != int(outputs["purged_bytes"]):
        raise SystemExit("cache-regenerator: purged_bytes does not match sum(bytes where purged=true)")
    if skipped_tracked != int(outputs["skipped_tracked_purge_count"]):
        raise SystemExit("cache-regenerator: skipped_tracked_purge_count does not match items")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate cache/waste regenerator report")
    parser.add_argument("--cache", default="docs/cache-waste-regenerator-report.json")
    args = parser.parse_args()

    report = load_json(Path(args.cache))
    outputs = report.get("outputs")
    check_numeric_outputs(outputs)
    check_items(outputs)
    print("validated cache-waste regenerator report")


if __name__ == "__main__":
    main()

