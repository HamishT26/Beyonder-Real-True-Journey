#!/usr/bin/env python3
"""Distill the latest advisory-only journey text into V42-safe digest inputs."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

from trinity_v42_common import git_head, now_iso, read_json, write_json, write_text

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCES = [
    Path(r"C:\Users\hamis\Downloads\Beyonder-Real-True Journey v40 (Aletheon - Orun - Gemini - Vesper Ion - Kai) (2).txt"),
]
DEFAULT_JSON = ROOT / "docs" / "auto-generated" / "v42-journey-advisory-digest-v1.json"
DEFAULT_MD = ROOT / "docs" / "auto-generated" / "v42-journey-advisory-digest-v1.md"
KEYWORDS = (
    "WSL",
    "Ubuntu",
    "Cloud Run",
    "Cloud Build",
    "Dataplex",
    "Anthos",
    "OS Login",
    "Kai",
    "Vesper Ion",
    "Agent Engine",
    "automation",
)
FOCUS_LINE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9/&+().,' :_-]{3,}$")


def normalize_line(value: str) -> str:
    return re.sub(r"\s+", " ", str(value or "").replace("\u00a0", " ")).strip()


def extract_focus_lines(raw_text: str) -> list[str]:
    rows: list[str] = []
    for raw_line in raw_text.splitlines():
        line = normalize_line(raw_line)
        if not line or len(line) > 140:
            continue
        lowered = line.lower()
        if not any(token.lower() in lowered for token in KEYWORDS):
            continue
        if not FOCUS_LINE_RE.match(line):
            continue
        if line not in rows:
            rows.append(line)
    return rows


def extract_keyword_snippets(source_name: str, raw_text: str) -> list[dict[str, str]]:
    lines = raw_text.splitlines()
    lowered = [line.lower() for line in lines]
    snippets: list[dict[str, str]] = []
    for keyword in KEYWORDS:
        needle = keyword.lower()
        for index, line in enumerate(lowered):
            if needle not in line:
                continue
            start = max(0, index - 1)
            end = min(len(lines), index + 3)
            snippet = "\n".join(normalize_line(row) for row in lines[start:end]).strip()
            snippets.append({"source": source_name, "keyword": keyword, "snippet": snippet[:1400]})
            break
    return snippets


def repo_truth() -> dict[str, Any]:
    runtime = read_json(ROOT / "docs" / "trinity-runtime-model-resolution-v1.json")
    v41 = read_json(ROOT / "docs" / "v41-omega-closeout-summary-v1.json")
    v42_beta = read_json(ROOT / "docs" / "v42-beta-closeout-summary-v1.json")
    return {
        "actual_current_head_sha": git_head(),
        "published_v41_head_sha": str(v41.get("current_head_sha") or ""),
        "published_v42_beta_head_sha": str(v42_beta.get("current_head_sha") or ""),
        "windows_operator_lane_state": str(runtime.get("windows_operator_lane_state") or ""),
        "filesystem_promotion_state": str(runtime.get("filesystem_promotion_state") or ""),
        "google_drive_state": str(runtime.get("google_drive_state") or ""),
        "materialization_level_actual": str(runtime.get("materialization_level_actual") or ""),
        "active_handoff_pack_path": str(runtime.get("active_handoff_pack_path") or ""),
        "next_receiver_pack_path": str(runtime.get("next_receiver_pack_path") or ""),
    }


def executable_decisions() -> list[str]:
    return [
        "Keep the Downloads text advisory-only and preserve repo proof surfaces as the only V42 authority.",
        "Treat WSL itself as healthy until a concrete Ubuntu-side regression appears; focus V42 on Codex binding and selector truth.",
        "Only promote filesystem_promotion_state if a Codex-backed WSL cycle is proven end to end against the authoritative repo.",
        "Carry forward the green V40/V41 cloud baselines and add a bounded telemetry delta across logging, monitoring, scheduler, pubsub, eventarc, and workflows.",
        "Create recurring twice-daily automation lanes only where the entrypoint is safe, deterministic, and proof-backed.",
    ]


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V42 Journey Advisory Digest",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Actual current head: `{payload['repo_truth']['actual_current_head_sha']}`",
        "",
        "## Source Files",
        "",
    ]
    for row in payload.get("sources", []):
        lines.append(f"- `{row['path']}`: present=`{row['present']}`, line_count=`{row['line_count']}`, focus_lines=`{row['focus_line_count']}`")
    lines.extend(["", "## Repo Truth", ""])
    for key, value in payload.get("repo_truth", {}).items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Executable Decisions", ""])
    lines.extend(f"- {row}" for row in payload.get("executable_decisions", []))
    if payload.get("focus_lines"):
        lines.extend(["", "## Parsed Focus Lines", ""])
        lines.extend(f"- `{row}`" for row in payload["focus_lines"][:24])
    if payload.get("proposal_snippets"):
        lines.extend(["", "## Keyword Snippets", ""])
        for row in payload["proposal_snippets"]:
            lines.extend([f"### {row['source']} :: {row['keyword']}", "", row["snippet"], ""])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Distill V42 advisory journey text into repo-safe digest inputs.")
    parser.add_argument("--source", action="append")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()

    sources = [Path(item) for item in args.source] if args.source else list(DEFAULT_SOURCES)
    source_rows: list[dict[str, Any]] = []
    focus_lines: list[str] = []
    snippets: list[dict[str, str]] = []
    for source in sources:
        raw_text = source.read_text(encoding="utf-8", errors="replace") if source.exists() else ""
        extracted_focus = extract_focus_lines(raw_text)
        for line in extracted_focus:
            if line not in focus_lines:
                focus_lines.append(line)
        snippets.extend(extract_keyword_snippets(source.name, raw_text))
        source_rows.append(
            {
                "path": str(source),
                "present": source.exists(),
                "line_count": len(raw_text.splitlines()) if raw_text else 0,
                "focus_line_count": len(extracted_focus),
            }
        )

    payload = {
        "generated_utc": now_iso(),
        "phase": "v42_omega",
        "authority_boundary": {
            "digest_scope": "advisory_only",
            "repo_proof_surfaces_authoritative": True,
            "journey_text_overrides_repo_truth": False,
        },
        "sources": source_rows,
        "repo_truth": repo_truth(),
        "focus_lines": focus_lines,
        "proposal_snippets": snippets,
        "executable_decisions": executable_decisions(),
    }
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    print(f"journey_digest={args.output_json}")
    print(f"focus_lines={len(focus_lines)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
