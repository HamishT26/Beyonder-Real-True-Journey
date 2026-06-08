#!/usr/bin/env python3
"""Verify a CLI sibling prompt template before launch without publishing the prompt body."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
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

REQUIRED_PHRASES = [
    "read-only",
    "Minimum 4,000 words",
    "at least 12 concrete items",
    "FINAL MESSAGE READY",
    "Do not include credentials",
]


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def heading_present(text: str, heading: str) -> bool:
    lines = [line.strip().lstrip("\ufeff") for line in text.splitlines()]
    return heading in lines


def phrase_present(text: str, phrase: str) -> bool:
    return phrase.lower() in text.lower()


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    prompt_path = Path(args.prompt_template)
    text = prompt_path.read_text(encoding="utf-8")
    headings = [{"heading": heading, "present": heading_present(text, heading)} for heading in REQUIRED_HEADINGS]
    phrases = [{"phrase": phrase, "present": phrase_present(text, phrase)} for phrase in REQUIRED_PHRASES]
    open_gaps = [
        f"missing_heading:{row['heading']}" for row in headings if not row["present"]
    ] + [f"missing_phrase:{row['phrase']}" for row in phrases if not row["present"]]
    if "{lane}" not in text:
        open_gaps.append("missing_lane_placeholder")
    if len(text.split()) < args.minimum_prompt_words:
        open_gaps.append("prompt_template_too_short")
    return {
        "artifact_type": "cli_prompt_contract_verifier",
        "phase_slug": args.phase_slug,
        "generated_utc": utc_now(),
        "overall_status": "PASS_CLI_PROMPT_CONTRACT" if not open_gaps else "OPEN_GAP_CLI_PROMPT_CONTRACT",
        "prompt_template_name": prompt_path.name,
        "prompt_template_sha256": sha256_text(text),
        "prompt_template_word_count": len(text.split()),
        "minimum_prompt_words": args.minimum_prompt_words,
        "headings": headings,
        "phrases": phrases,
        "lane_placeholder_present": "{lane}" in text,
        "open_gaps": open_gaps,
        "publication_boundary": {
            "prompt_body_published": False,
            "local_absolute_path_published": False,
            "raw_lane_text_published": False,
            "credentials_published": False,
        },
        "claim_boundary": {
            "gmut_gate_state": "open",
            "canon_promotion": "not_claimed",
        },
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['phase_slug']} CLI Prompt Contract Verifier",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: `{payload['overall_status']}`",
        f"- prompt_template_name: `{payload['prompt_template_name']}`",
        f"- prompt_template_word_count: `{payload['prompt_template_word_count']}`",
        f"- minimum_prompt_words: `{payload['minimum_prompt_words']}`",
        f"- lane_placeholder_present: `{payload['lane_placeholder_present']}`",
        "",
        "Headings:",
    ]
    for row in payload["headings"]:
        lines.append(f"- {row['heading']}: `{row['present']}`")
    lines.extend(["", "Required phrases:"])
    for row in payload["phrases"]:
        lines.append(f"- {row['phrase']}: `{row['present']}`")
    lines.extend(["", "Open gaps:"])
    if payload["open_gaps"]:
        lines.extend(f"- `{gap}`" for gap in payload["open_gaps"])
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "Publication boundary: prompt body, local absolute path, raw lane text, and credentials are not published.",
            "",
            "Claim boundary: GMUT and canon gates remain open.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--prompt-template", required=True)
    parser.add_argument("--minimum-prompt-words", type=int, default=160)
    parser.add_argument("--receipt-json", required=True)
    parser.add_argument("--receipt-md", required=True)
    args = parser.parse_args()

    payload = build_payload(args)
    write_json(Path(args.receipt_json), payload)
    write_md(Path(args.receipt_md), payload)
    print(json.dumps({"status": payload["overall_status"], "phase_slug": args.phase_slug}, indent=2))
    return 0 if not payload["open_gaps"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
