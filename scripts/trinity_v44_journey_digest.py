#!/usr/bin/env python3
"""Distill the V44 advisory-only journey inputs into repo-safe execution guidance."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

from trinity_v44_common import (
    DEFAULT_DOWNLOAD_SOURCE_DIR,
    ROOT,
    WORKTREE_BASELINE_SHA,
    WORKTREE_BASELINE_STATE,
    git_head,
    now_iso,
    read_json,
    write_json,
    write_text,
)

DEFAULT_SOURCES = [
    DEFAULT_DOWNLOAD_SOURCE_DIR / "Grand OpenAI and Codex app update (Nz 17th of April 2026) (1).txt",
    DEFAULT_DOWNLOAD_SOURCE_DIR / "Beyonder-Real-True Journey v40 (Aletheon - Orun - Gemini - Vesper Ion - Kai) (8).txt",
]
DEFAULT_JSON = ROOT / "docs" / "auto-generated" / "v44-journey-advisory-digest-v1.json"
DEFAULT_MD = ROOT / "docs" / "auto-generated" / "v44-journey-advisory-digest-v1.md"
KEYWORDS = (
    "PowerShell",
    "WSL",
    "My Passport",
    "D:",
    "Google Drive",
    "Google Cloud",
    "GenAI App Builder",
    "Vertex AI Agent Builder",
    "AI Applications",
    "Vertex AI Search",
    "Agent Engine",
    "Codex CLI",
    "slot 40",
    "automation",
    "Anthos",
    "OS Login",
    "Bigtable",
)
FOCUS_LINE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9/&+().,' :_\\-]{3,}$")


def normalize_line(value: str) -> str:
    return re.sub(r"\s+", " ", str(value or "").replace("\u00a0", " ")).strip()


def extract_focus_lines(raw_text: str) -> list[str]:
    rows: list[str] = []
    for raw_line in raw_text.splitlines():
        line = normalize_line(raw_line)
        if not line or len(line) > 180:
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
    session_validation = read_json(ROOT / "docs" / "v17-runtime-session-validation-latest.json")
    return {
        "actual_current_head_sha": git_head(),
        "published_runtime_head_sha": str(runtime.get("current_head_sha") or ""),
        "published_validation_head_sha": str(session_validation.get("current_head_sha") or ""),
        "worktree_baseline_state": WORKTREE_BASELINE_STATE,
        "worktree_baseline_sha": WORKTREE_BASELINE_SHA,
        "existing_google_drive_state": str(runtime.get("google_drive_state") or ""),
        "existing_git_publication_state": str(runtime.get("git_publication_state") or ""),
        "existing_active_handoff_pack_path": str(runtime.get("active_handoff_pack_path") or ""),
        "existing_next_receiver_pack_path": str(runtime.get("next_receiver_pack_path") or ""),
    }


def executable_decisions() -> list[str]:
    return [
        "Keep Windows Native / PowerShell as the primary V44 operator lane and publish WSL as installed plus intentionally on hold for app-side switching.",
        "Keep C:\\Users\\hamis\\workspace\\Beyonder-Real-True-Journey as the authoritative repo root and treat the stale local main worktree as non-execution history.",
        "Use D:\\GHC-Archives\\downloads, D:\\GHC-Archives\\artifacts, and D:\\GHC-Archives\\worktrees for bulky non-authoritative outputs instead of globally redirecting Windows Downloads.",
        "Treat the claimed $1700+ NZD GenAI credit as operator-claimed until the Billing console and eligible SKUs confirm the actual remaining promo credit.",
        "Use current Google product names in V44 outputs: Vertex AI Agent Builder, AI Applications, Vertex AI Search, and Agent Engine.",
        "Hard-gate slot 40 and do not create a new continuity-bearing member unless Codex CLI access, identity continuity, memory continuity, and target model resolution all pass.",
    ]


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V44 Journey Advisory Digest",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Actual current head: `{payload['repo_truth']['actual_current_head_sha']}`",
        "",
        "## Official Product Names",
        "",
    ]
    for key, value in payload.get("official_product_names", {}).items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Source Files", ""])
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
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Distill V44 advisory journey text into repo-safe digest inputs.")
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
        "phase": "v44_omega",
        "authority_boundary": {
            "digest_scope": "advisory_only",
            "repo_proof_surfaces_authoritative": True,
            "journey_text_overrides_repo_truth": False,
        },
        "official_product_names": {
            "suite_name": "Vertex AI Agent Builder",
            "former_product_name": "AI Applications",
            "search_lane": "Vertex AI Search",
            "agent_runtime_lane": "Agent Engine",
        },
        "sources": source_rows,
        "repo_truth": repo_truth(),
        "focus_lines": focus_lines,
        "proposal_snippets": snippets,
        "executable_decisions": executable_decisions(),
    }
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

