#!/usr/bin/env python3
"""Generate a concise latest-session summary from Aurelis memory JSONL log."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_IN = ROOT / "docs" / "aurelis-memory-log.jsonl"
DEFAULT_OUT = ROOT / "docs" / "aurelis-memory-latest-summary.md"


def load_entries(path: Path) -> list[dict]:
    if not path.exists():
        return []
    entries: list[dict] = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return entries


def build_summary(entries: list[dict], take: int) -> str:
    subset = entries[-take:] if take > 0 else entries
    if not subset:
        return "# Aurelis Memory Latest Summary\n\nNo entries available yet.\n"

    latest = subset[-1]
    lines = [
        "# Aurelis Memory Latest Summary",
        "",
        f"Entries summarized: **{len(subset)}**",
        "",
        "## Current state",
        f"- Latest timestamp (UTC): {latest.get('timestamp_utc', 'n/a')}",
        f"- NZDT context: {latest.get('nzdt_context', 'n/a')}",
        f"- Progress snapshot: {latest.get('progress_snapshot', 'n/a')}",
        f"- Next step: {latest.get('next_step', 'n/a')}",
        "",
        "## Recent continuity trail",
    ]

    for i, e in enumerate(subset, start=1):
        lines.append(f"### Entry {i}")
        lines.append(f"- user_message: {e.get('user_message', 'n/a')}")
        lines.append(f"- assistant_reflection: {e.get('assistant_reflection', 'n/a')}")
        lines.append(f"- progress_snapshot: {e.get('progress_snapshot', 'n/a')}")
        lines.append(f"- next_step: {e.get('next_step', 'n/a')}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    p = argparse.ArgumentParser(description="Summarize Aurelis memory entries")
    p.add_argument("--input", default=str(DEFAULT_IN))
    p.add_argument("--out", default=str(DEFAULT_OUT))
    p.add_argument("--take", type=int, default=5, help="Number of most recent entries to summarize")
    args = p.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.out)

    entries = load_entries(in_path)
    summary = build_summary(entries, args.take)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(summary)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
