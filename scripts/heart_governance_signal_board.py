#!/usr/bin/env python3
"""Emit the cached Heart API signal board."""

from __future__ import annotations

import argparse

from trinity_api_common import board_from_cache


def main() -> int:
    parser = argparse.ArgumentParser(description="Emit the cached Heart API signal board.")
    parser.add_argument("--cache", default="docs/trinity-api-cache/heart-signals-latest.json")
    parser.add_argument("--reports-dir", default="docs/trinity-api-board-runs")
    parser.add_argument("--latest-json", default="docs/heart-governance-signal-board-latest.json")
    parser.add_argument("--latest-md", default="docs/heart-governance-signal-board-latest.md")
    parser.add_argument("--fail-on-warn", action="store_true")
    args = parser.parse_args()
    return board_from_cache(
        pillar="heart",
        cache_path=args.cache,
        latest_json=args.latest_json,
        latest_md=args.latest_md,
        reports_dir=args.reports_dir,
        board_title="Heart Governance Signal Board",
        fail_on_warn=args.fail_on_warn,
    )


if __name__ == "__main__":
    raise SystemExit(main())
