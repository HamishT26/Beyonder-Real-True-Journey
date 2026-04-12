#!/usr/bin/env python3
"""Distill the latest external journey text into advisory-only V39 inputs."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE = Path(
    r"C:\Users\hamis\Downloads\Beyonder-Real-True Journey v39 (Aletheon - Gemini - Synthea - Orun) (12).txt"
)
DEFAULT_JSON = ROOT / "docs" / "auto-generated" / "v39-journey-advisory-digest-v1.json"
DEFAULT_MD = ROOT / "docs" / "auto-generated" / "v39-journey-advisory-digest-v1.md"
API_BOOK_MARKER = "Current enabled GCP APIs"
API_LINE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9/&+().,' -]{3,}$")
KEYWORDS = (
    "Agent Engine",
    "Kai",
    "Vesper Ion",
    "Anthos",
    "Cloud OS Login",
    "Bigtable",
    "Vertex AI",
    "Beyonder-Real-True Journey",
)


def now_iso() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def git_head() -> str:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    return (result.stdout or "").strip()


def normalize_line(value: str) -> str:
    return re.sub(r"\s+", " ", str(value or "").replace("\u00a0", " ")).strip()


def extract_api_titles(raw_text: str) -> list[str]:
    lines = raw_text.splitlines()
    start_index = 0
    for index, line in enumerate(lines):
        if API_BOOK_MARKER.lower() in line.lower():
            start_index = index + 1
            break

    titles: list[str] = []
    for raw_line in lines[start_index:]:
        stripped = normalize_line(raw_line)
        if not stripped:
            continue
        if stripped.startswith("Message #") or stripped.startswith("TO: ") or stripped.startswith("SUBJECT: "):
            break
        if "http" in stripped.lower():
            continue
        if "api" not in stripped.lower():
            continue
        if not API_LINE_RE.match(stripped):
            continue
        if stripped not in titles:
            titles.append(stripped)
    return titles


def extract_keyword_snippets(raw_text: str) -> list[dict[str, str]]:
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
            snippets.append({"keyword": keyword, "snippet": snippet[:1400]})
            break
    return snippets


def repo_truth() -> dict[str, Any]:
    runtime = read_json(ROOT / "docs" / "trinity-runtime-model-resolution-v1.json")
    v38_closeout = read_json(ROOT / "docs" / "v38-omega-closeout-summary-v1.json")
    v39_beta = read_json(ROOT / "docs" / "v39-beta-handoff-policy-v1.json")
    return {
        "actual_current_head_sha": git_head(),
        "runtime_phase": str(runtime.get("phase") or ""),
        "v38_closeout_present": bool(v38_closeout),
        "v39_beta_present": bool(v39_beta),
        "google_drive_state": str(runtime.get("google_drive_state") or ""),
        "filesystem_promotion_state": str(runtime.get("filesystem_promotion_state") or ""),
        "materialization_level_actual": str(runtime.get("materialization_level_actual") or ""),
        "v38_agent_engine_state": str(v38_closeout.get("core_states", {}).get("agent_engine_state") or ""),
        "v39_beta_intended_lead": str(v39_beta.get("intended_lead") or ""),
    }


def executable_decisions(api_titles: list[str]) -> list[str]:
    return [
        "Keep the journey text advisory-only and preserve repo proof surfaces as the only V39 authority.",
        "Keep V39 Aletheon-led even though the current local v39-beta pack still points at Orun from the V38 publication logic.",
        "Treat Agent Engine recovery as the primary blocker-clearance lane and only promote it if a fresh minimal runtime becomes visible and queryable.",
        "Use Kai for bounded CLI analysis of Agent Engine forensics and Vesper Ion for Bigtable-backed V39 telemetry without replacing the proven durable-memory baseline.",
        "Keep Gmail and Google Drive non-gating during V39 and preserve existing operator-hold and blocked filesystem-promotion truths unless the implementation genuinely changes them.",
        f"Seed the curated V39 additions from the parsed advisory API/material set ({len(api_titles)} candidate titles) without letting the digest override repo proof.",
    ]


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V39 Journey Advisory Digest",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Source file: `{payload['source_file']}`",
        f"- Source present: `{payload['source_file_present']}`",
        f"- Actual current head: `{payload['repo_truth']['actual_current_head_sha']}`",
        f"- Parsed API titles: `{payload['parsed_api_title_count']}`",
        "",
        "## Executable Decisions",
        "",
    ]
    lines.extend(f"- {row}" for row in payload["executable_decisions"])
    lines.extend(["", "## Repo Truth", ""])
    repo_truth = payload["repo_truth"]
    for key in (
        "runtime_phase",
        "google_drive_state",
        "filesystem_promotion_state",
        "materialization_level_actual",
        "v38_agent_engine_state",
        "v39_beta_intended_lead",
    ):
        lines.append(f"- `{key}`: `{repo_truth.get(key, '')}`")
    lines.extend(["", "## Keyword Snippets", ""])
    for row in payload["proposal_snippets"]:
        lines.extend([f"### {row['keyword']}", "", row["snippet"], ""])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Distill the external V39 journey text into advisory-only inputs.")
    parser.add_argument("--source", default=str(DEFAULT_SOURCE))
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()

    source = Path(args.source)
    raw_text = source.read_text(encoding="utf-8", errors="replace") if source.exists() else ""
    api_titles = extract_api_titles(raw_text)
    payload = {
        "generated_utc": now_iso(),
        "phase": "v39_omega",
        "source_file": str(source),
        "source_file_present": source.exists(),
        "repo_truth": repo_truth(),
        "parsed_api_titles": api_titles,
        "parsed_api_title_count": len(api_titles),
        "proposal_snippets": extract_keyword_snippets(raw_text),
        "executable_decisions": executable_decisions(api_titles),
        "authority_boundary": {
            "digest_scope": "advisory_only",
            "mutates_historical_claims": False,
            "repo_proof_surfaces_authoritative": True,
        },
    }
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    print(f"journey_digest={args.output_json}")
    print(f"parsed_api_titles={len(api_titles)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
