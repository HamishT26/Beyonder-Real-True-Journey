#!/usr/bin/env python3
"""Distill the V43 advisory-only journey inputs into repo-safe execution guidance."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

from trinity_v43_common import git_head, now_iso, read_json, write_json, write_text

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCES = [
    Path(r"C:\Users\hamis\Downloads\Grand OpenAI and Codex app update (Nz 17th of April 2026) (1).txt"),
    Path(r"C:\Users\hamis\Downloads\Beyonder-Real-True Journey v40 (Aletheon - Orun - Gemini - Vesper Ion - Kai) (7).txt"),
]
DEFAULT_JSON = ROOT / "docs" / "auto-generated" / "v43-journey-advisory-digest-v1.json"
DEFAULT_MD = ROOT / "docs" / "auto-generated" / "v43-journey-advisory-digest-v1.md"
KEYWORDS = (
    "WSL",
    "Ubuntu",
    "My Passport",
    "D:",
    "Codex",
    "browser",
    "computer use",
    "plugin",
    "Google Drive",
    "Kai",
    "Vesper",
    "automation",
    "sandbox",
    "Vercel",
    "Anthos",
    "OS Login",
    "GenAI App Builder",
    "Vertex AI Search",
)
FOCUS_LINE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9/&+().,' :_\\-]{3,}$")


def normalize_line(value: str) -> str:
    return re.sub(r"\s+", " ", str(value or "").replace("\u00a0", " ")).strip()


def extract_focus_lines(raw_text: str) -> list[str]:
    rows: list[str] = []
    for raw_line in raw_text.splitlines():
        line = normalize_line(raw_line)
        if not line or len(line) > 160:
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
            snippets.append({"source": source_name, "keyword": keyword, "snippet": snippet[:1600]})
            break
    return snippets


def repo_truth() -> dict[str, Any]:
    runtime = read_json(ROOT / "docs" / "trinity-runtime-model-resolution-v1.json")
    v42 = read_json(ROOT / "docs" / "v42-omega-closeout-summary-v1.json")
    return {
        "actual_current_head_sha": git_head(),
        "published_v42_head_sha": str(v42.get("current_head_sha") or ""),
        "published_runtime_head_sha": str(runtime.get("current_head_sha") or ""),
        "filesystem_promotion_state": str(runtime.get("filesystem_promotion_state") or ""),
        "google_drive_state": str(runtime.get("google_drive_state") or ""),
        "active_handoff_pack_path": str(runtime.get("active_handoff_pack_path") or ""),
        "next_receiver_pack_path": str(runtime.get("next_receiver_pack_path") or ""),
    }


def executable_decisions() -> list[str]:
    return [
        "Keep the Downloads text advisory-only and preserve repo proof surfaces as the only V43 authority.",
        "Treat the missing WSL service binary as the first machine-level blocker, not just a broken Ubuntu distro registration.",
        "Back up the existing Ubuntu ext4.vhdx to D:\\GHC-Ubuntu-Core\\backups before any unregister step.",
        "Keep the authoritative repo on C: and use D: only for the Ubuntu install root plus large archive outputs.",
        "Audit the Codex app update claims separately from direct tool exposure: in-app browser may be claimed, native Windows computer_use stays unsupported here, and Task Scheduler remains authoritative until native automation is actually callable.",
        "Keep Bigtable as Vesper Ion's primary proven memory path unless the bounded V43 cognitive-engine proof becomes queryable and stable.",
    ]


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V43 Journey Advisory Digest",
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
        lines.extend(f"- `{row}`" for row in payload["focus_lines"][:30])
    if payload.get("proposal_snippets"):
        lines.extend(["", "## Keyword Snippets", ""])
        for row in payload["proposal_snippets"]:
            lines.extend([f"### {row['source']} :: {row['keyword']}", "", row["snippet"], ""])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Distill V43 advisory journey text into repo-safe digest inputs.")
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
        "phase": "v43_omega",
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
