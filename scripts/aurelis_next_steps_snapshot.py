#!/usr/bin/env python3
"""Generate an actionable next-3-steps snapshot from Aurelis memory entries."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_LOG = ROOT / "docs" / "aurelis-memory-log.jsonl"
DEFAULT_OUT = ROOT / "docs" / "aurelis-next-steps.md"


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


def build_snapshot(entries: list[dict]) -> str:
    if not entries:
        return "# Aurelis Next 3 Steps\n\nNo memory entries yet.\n"

    latest = entries[-1]
    recent = entries[-3:]

    # Step 1: continue the explicitly declared next step
    step1 = latest.get("next_step", "Run one validated micro-upgrade and record continuity.")

    # Step 2: build from recent progress themes
    themes = [e.get("progress_snapshot", "") for e in recent if e.get("progress_snapshot")]
    if any("query" in t.lower() for t in themes):
        step2 = "Run `scripts/aurelis_memory_query.py --contains \"continue\" --limit 5` and capture continuity anchors."
    else:
        step2 = "Run `scripts/aurelis_memory_summary.py --take 5` to refresh the session-state rollup."

    # Step 3: enforce cadence loop
    step3 = "Append a fresh entry via `scripts/aurelis_memory_update.py` after execution, then regenerate summary + next-steps snapshot."

    lines = [
        "# Aurelis Next 3 Steps",
        "",
        f"Generated from latest entry: `{latest.get('timestamp_utc', 'n/a')}`",
        "",
        "1. " + step1,
        "2. " + step2,
        "3. " + step3,
        "",
        "## Context anchors",
    ]

    for i, e in enumerate(recent, start=1):
        lines.append(f"- Entry {i}: {e.get('progress_snapshot', 'n/a')}")

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    p = argparse.ArgumentParser(description="Generate Aurelis next-3-steps snapshot")
    p.add_argument("--input", default=str(DEFAULT_LOG))
    p.add_argument("--out", default=str(DEFAULT_OUT))
    args = p.parse_args()

    entries = load_entries(Path(args.input))
    out_text = build_snapshot(entries)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(out_text)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
