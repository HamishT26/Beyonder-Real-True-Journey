#!/usr/bin/env python3
"""Write status-only quality gates for Codex CLI advisory lane artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REQUIRED_HEADINGS = [
    "COMMAND PROPOSALS (10+)",
    "SYSTEM EXPANSION PROPOSALS (10+)",
    "SKILL OR MICRO-WORKFLOW PROPOSALS (10+)",
    "EUREKA TASKS (10+)",
    "RISKS AND BLOCKERS",
    "X2 BUILD PRIORITIES",
]

HEADING_ALIASES = {
    "COMMAND PROPOSALS (10+)": ["COMMAND PROPOSALS"],
    "SYSTEM EXPANSION PROPOSALS (10+)": ["SYSTEM EXPANSION PROPOSALS"],
    "SKILL OR MICRO-WORKFLOW PROPOSALS (10+)": ["SKILL OR MICRO-WORKFLOW PROPOSALS"],
    "EUREKA TASKS (10+)": ["EUREKA TASKS"],
}

SENSITIVE_RE = re.compile(
    "|".join(
        [
            r"BEGIN (?:RSA|OPENSSH|PRIVATE) KEY",
            r"\b(?:sk|ghp|xoxb)_[A-Za-z0-9_-]{10,}",
            r"\b[A-Z]:\\Users\\",
            r"\b[A-Z]:\\GHC-Archives\\",
            r"session(?:_|-)?jsonl",
            r"Screenshot 20\d\d",
        ]
    ),
    re.IGNORECASE,
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def count_words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def count_numbered_items(text: str) -> int:
    return len(re.findall(r"(?m)^\s*(?:\d+[\.)]|[-*])\s+", text))


def heading_variants(heading: str) -> list[str]:
    return [heading, *HEADING_ALIASES.get(heading, [])]


def find_heading(text: str, heading: str) -> re.Match[str] | None:
    for variant in heading_variants(heading):
        heading_re = re.compile(rf"(?im)^\s*#*\s*{re.escape(variant)}\s*:?\s*$")
        match = heading_re.search(text)
        if match:
            return match
    return None


def has_heading(text: str, heading: str) -> bool:
    return find_heading(text, heading) is not None


def category_item_count(text: str, heading: str) -> int:
    match = find_heading(text, heading)
    if not match:
        return 0
    next_heading = re.search(r"(?m)^\s*#*\s*[A-Z][A-Z0-9 /&()+-]{5,}\s*:?\s*$", text[match.end() :])
    section = text[match.end() : match.end() + next_heading.start()] if next_heading else text[match.end() :]
    return count_numbered_items(section)


def lane_quality(output_dir: Path, lane: str, minimum_words: int, minimum_items_per_category: int) -> dict[str, Any]:
    path = output_dir / f"{lane}-last-message.txt"
    text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
    headings = {heading: has_heading(text, heading) for heading in REQUIRED_HEADINGS}
    category_counts = {
        heading: category_item_count(text, heading)
        for heading in REQUIRED_HEADINGS[:4]
    }
    marker_hits = len(SENSITIVE_RE.findall(text))
    words = count_words(text)
    numbered_items = count_numbered_items(text)
    missing_headings = [heading for heading, present in headings.items() if not present]
    shallow_categories = [
        heading for heading, count in category_counts.items() if count < minimum_items_per_category
    ]
    passes = (
        bool(text)
        and words >= minimum_words
        and not missing_headings
        and not shallow_categories
        and marker_hits == 0
    )
    return {
        "lane": lane,
        "completion_status": "FINAL_MESSAGE_READY" if text else "WAITING_FOR_FINAL_MESSAGE",
        "quality_status": "PASS_ELABORATION_GATE" if passes else "OPEN_GAP_ELABORATION_REPAIR_NEEDED",
        "final_message_bytes": path.stat().st_size if path.exists() else 0,
        "final_message_hash": sha256_text(text) if text else None,
        "word_count": words,
        "line_count": len(text.splitlines()) if text else 0,
        "numbered_or_bullet_item_count": numbered_items,
        "minimum_words": minimum_words,
        "minimum_items_per_category": minimum_items_per_category,
        "required_headings_present": headings,
        "category_item_counts": category_counts,
        "missing_required_headings": missing_headings,
        "shallow_required_categories": shallow_categories,
        "sensitive_or_path_marker_count": marker_hits,
        "raw_output_boundary": "temp_only_not_published",
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['phase_slug']} CLI Elaboration Quality Gate",
        "",
        f"Generated UTC: `{payload['generated_at_utc']}`",
        f"Status: `{payload['aggregate_status']}`",
        f"Output boundary: `{payload['raw_output_boundary']}`",
        "",
        "Lane quality:",
    ]
    for lane in payload["lanes"]:
        lines.append(
            f"- {lane['lane']}: `{lane['quality_status']}`, words `{lane['word_count']}`, "
            f"items `{lane['numbered_or_bullet_item_count']}`, missing headings `{len(lane['missing_required_headings'])}`, "
            f"shallow categories `{len(lane['shallow_required_categories'])}`"
        )
    lines.extend(
        [
            "",
            "This gate records status-only metrics, hashes, counts, and category coverage. It does not publish raw lane text.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Gate CLI lane artifacts for elaboration without publishing raw text.")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--lane", action="append", required=True)
    parser.add_argument("--minimum-words", type=int, default=2200)
    parser.add_argument("--minimum-items-per-category", type=int, default=10)
    parser.add_argument("--receipt-json", required=True)
    parser.add_argument("--receipt-md", required=True)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    lanes = [
        lane_quality(output_dir, lane, args.minimum_words, args.minimum_items_per_category)
        for lane in args.lane
    ]
    all_pass = all(lane["quality_status"] == "PASS_ELABORATION_GATE" for lane in lanes)
    payload: dict[str, Any] = {
        "artifact_type": "cli_elaboration_quality_gate",
        "phase_slug": args.phase_slug,
        "generated_at_utc": utc_now(),
        "aggregate_status": "PASS_ALL_CLI_LANES_ELABORATE" if all_pass else "OPEN_GAP_CLI_ELABORATION_REPAIR_NEEDED",
        "lanes": lanes,
        "raw_output_boundary": "temp_only_not_published",
        "mutation_performed": False,
    }
    write_json(Path(args.receipt_json), payload)
    write_md(Path(args.receipt_md), payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
