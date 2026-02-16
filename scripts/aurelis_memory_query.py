#!/usr/bin/env python3
"""Query Aurelis memory log (JSONL) with simple filters."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_LOG = ROOT / "docs" / "aurelis-memory-log.jsonl"


def load_entries(path: Path) -> list[dict]:
    if not path.exists():
        return []
    entries = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return entries


def matches(entry: dict, contains: str | None) -> bool:
    if not contains:
        return True
    needle = contains.lower()
    hay = " ".join([
        str(entry.get("user_message", "")),
        str(entry.get("assistant_reflection", "")),
        str(entry.get("progress_snapshot", "")),
        str(entry.get("next_step", "")),
    ]).lower()
    return needle in hay


def main() -> None:
    p = argparse.ArgumentParser(description="Query Aurelis memory log")
    p.add_argument("--input", default=str(DEFAULT_LOG))
    p.add_argument("--contains", help="Filter entries containing this text")
    p.add_argument("--limit", type=int, default=5, help="Max number of entries to print")
    p.add_argument("--json", action="store_true", help="Print raw JSON lines")
    args = p.parse_args()

    entries = load_entries(Path(args.input))
    filtered = [e for e in entries if matches(e, args.contains)]
    if args.limit > 0:
        filtered = filtered[-args.limit:]

    if args.json:
        for e in filtered:
            print(json.dumps(e, ensure_ascii=False))
        return

    if not filtered:
        print("No matching entries.")
        return

    for i, e in enumerate(filtered, start=1):
        print(f"[{i}] {e.get('timestamp_utc', 'n/a')} | {e.get('nzdt_context', 'n/a')}")
        print(f"  user_message: {e.get('user_message', 'n/a')}")
        print(f"  progress_snapshot: {e.get('progress_snapshot', 'n/a')}")
        print(f"  next_step: {e.get('next_step', 'n/a')}")


if __name__ == "__main__":
    main()
