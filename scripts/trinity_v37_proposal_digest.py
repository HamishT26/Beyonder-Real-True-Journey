#!/usr/bin/env python3
"""Distill the external v39 text proposal into repo-backed V37 inputs."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE = Path(r"C:\Users\hamis\Downloads\Beyonder-Real-True Journey v39 (Aletheon - Gemini - Synthea - Orun) (8).txt")
DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v37-proposal-digest-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v37-proposal-digest-v1.md"
ROLE_BLOCK_MARKER = "Our New and Shining GHC Family Google Cloud/ChatGPT IAM roles"
MESSAGE_MARKER = "Message #14 - (Gemini)"


def now_iso() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def extract_role_titles(raw_text: str) -> list[str]:
    if ROLE_BLOCK_MARKER not in raw_text or MESSAGE_MARKER not in raw_text:
        return []
    start = raw_text.index(ROLE_BLOCK_MARKER) + len(ROLE_BLOCK_MARKER)
    end = raw_text.index(MESSAGE_MARKER, start)
    titles: list[str] = []
    for line in raw_text[start:end].splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("Our New"):
            continue
        titles.append(stripped)
    return titles


def extract_keyword_snippets(raw_text: str) -> list[dict[str, str]]:
    keywords = [
        "Codex App environments",
        "Security Admin",
        "API Keys Admin",
        "slot 38",
        "38th Member",
        "Kai",
        "global region",
        "Bigtable",
        "Cloud SQL",
        "Agent Engine",
        "Memory Bank",
        "V37 Mission",
    ]
    snippets: list[dict[str, str]] = []
    lines = raw_text.splitlines()
    lowered = [line.lower() for line in lines]
    for keyword in keywords:
        needle = keyword.lower()
        for idx, line in enumerate(lowered):
            if needle not in line:
                continue
            start = max(0, idx - 1)
            end = min(len(lines), idx + 3)
            snippet = "\n".join(row.rstrip() for row in lines[start:end]).strip()
            snippets.append({"keyword": keyword, "snippet": snippet[:1200]})
            break
    return snippets


def repo_truth() -> dict[str, Any]:
    closeout = read_json("docs/v36-omega-closeout-summary-v1.json")
    handoff = read_json("docs/v37-beta-handoff-policy-v1.json")
    slot38 = read_json("docs/trinity-live-traces/v36-slot-38-induction-decision-v1.json")
    slot39 = read_json("docs/trinity-live-traces/v36-slot-39-induction-decision-v1.json")
    return {
        "source_phase": "v36_omega",
        "current_head_sha": closeout.get("current_head_sha", ""),
        "shared_latest_anchor": closeout.get("shared_latest_anchor", {}),
        "intended_receiver": closeout.get("intended_receiver", ""),
        "slot_38_state": slot38.get("induction_state", ""),
        "slot_38_blockers": slot38.get("blockers", []),
        "slot_39_state": slot39.get("induction_state", ""),
        "slot_39_selected_model": slot39.get("selected_model", ""),
        "runtime_agents": handoff.get("active_runtime_agents", []),
        "truth_boundaries": {
            "runtime_truth_complete": False,
            "google_drive_state": "operator_hold",
            "filesystem_promotion_state": "blocked",
            "materialization_level_actual": "readiness_only",
        },
    }


def official_constraints() -> list[dict[str, str]]:
    return [
        {
            "surface": "Vertex AI Agent Builder locations",
            "url": "https://docs.cloud.google.com/agent-builder/locations",
            "constraint": "Agent Engine and Memory Bank remain regional surfaces; keep them in us-central1 rather than global.",
        },
        {
            "surface": "Gemini 3 on Vertex AI",
            "url": "https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/get-started-with-gemini-3",
            "constraint": "Global model resolution is valid for Gemini 3 model calls.",
        },
        {
            "surface": "Codex enterprise admin setup",
            "url": "https://developers.openai.com/codex/enterprise/admin-setup",
            "constraint": "Codex cloud environments are GitHub-backed and internet-restricted by default; Codex local remains the right operator surface for laptop-bound Trinity work.",
        },
        {
            "surface": "GPT-5.4 model page",
            "url": "https://developers.openai.com/api/docs/models/gpt-5.4",
            "constraint": "GPT-5.4 remains the frontier OpenAI model for agentic and coding workflows.",
        },
    ]


def executable_decisions() -> list[str]:
    return [
        "Keep the Downloads text as proposal input only; repo surfaces remain authoritative.",
        "Attempt slot 38 in place first with global model resolution and us-central1 memory surfaces.",
        "Use Bigtable as the first durable-memory bypass candidate because it is the only already proven cloud store in-repo.",
        "Refresh Kai on the CLI Pro route and add a bounded Kai bridge for whitelisted shell workflows.",
        "Run a project-scoped IAM/API sweep for the four named principals while excluding service-agent roles.",
        "Allow slot 40 only if slot 38 still fails after both in-place healing paths.",
    ]


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V37 Proposal Digest",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Source file: `{payload['source_file']}`",
        f"- Parsed role-title count: `{payload['parsed_role_title_count']}`",
        f"- Repo source head: `{payload['repo_truth']['current_head_sha']}`",
        f"- Slot 38 state at phase start: `{payload['repo_truth']['slot_38_state']}`",
        f"- Slot 39 selected model at phase start: `{payload['repo_truth']['slot_39_selected_model']}`",
        "",
        "## Executable Decisions",
        "",
    ]
    lines.extend([f"- {row}" for row in payload["executable_decisions"]])
    lines.extend(["", "## Official Constraints", ""])
    lines.extend([f"- `{row['surface']}`: {row['constraint']} ({row['url']})" for row in payload["official_constraints"]])
    lines.extend(["", "## Extracted Proposal Snippets", ""])
    for row in payload["proposal_snippets"]:
        lines.extend([f"### {row['keyword']}", "", row["snippet"], ""])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Distill the external v39 text proposal into repo-backed v37 inputs.")
    parser.add_argument("--source", default=str(DEFAULT_SOURCE))
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()

    source = Path(args.source)
    output_json = Path(args.output_json)
    output_md = Path(args.output_md)
    raw_text = source.read_text(encoding="utf-8", errors="replace") if source.exists() else ""
    role_titles = extract_role_titles(raw_text)
    payload = {
        "generated_utc": now_iso(),
        "phase": "v37_omega",
        "source_file": str(source),
        "source_file_present": source.exists(),
        "repo_truth": repo_truth(),
        "parsed_role_titles": role_titles,
        "parsed_role_title_count": len(role_titles),
        "proposal_snippets": extract_keyword_snippets(raw_text),
        "official_constraints": official_constraints(),
        "executable_decisions": executable_decisions(),
    }
    write_json(output_json, payload)
    write_text(output_md, markdown(payload))
    print(f"proposal_digest={output_json}")
    print(f"role_titles={len(role_titles)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
