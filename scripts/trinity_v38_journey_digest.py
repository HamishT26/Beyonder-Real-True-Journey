#!/usr/bin/env python3
"""Distill the external v39 journey log into advisory-only V38 inputs."""

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
DEFAULT_JSON = ROOT / "docs" / "auto-generated" / "v38-journey-advisory-digest-v1.json"
DEFAULT_MD = ROOT / "docs" / "auto-generated" / "v38-journey-advisory-digest-v1.md"
API_BOOK_MARKER = "Our New and Shining GHC Family Google Cloud/ChatGPT API Book"
API_LINE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9/&+().,' -]*API(?: [A-Za-z0-9().,' -]+)?$")
KEYWORDS = (
    "Anthos",
    "Cloud OS Login",
    "Kai",
    "Vesper Ion",
    "Agent Engine",
    "Bigtable",
    "Connect Gateway",
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


def normalize_title(value: str) -> str:
    cleaned = re.sub(r"\s+", " ", str(value or "").replace("\u00a0", " ")).strip()
    return cleaned


def extract_api_titles(raw_text: str) -> list[str]:
    if API_BOOK_MARKER not in raw_text:
        return []
    lines = raw_text.splitlines()
    start_index = 0
    for idx, line in enumerate(lines):
        if API_BOOK_MARKER in line:
            start_index = idx + 1
            break

    titles: list[str] = []
    for raw_line in lines[start_index:]:
        stripped = normalize_title(raw_line)
        if not stripped:
            continue
        if stripped.startswith("Message #"):
            break
        if stripped.startswith("TO: ") or stripped.startswith("SUBJECT: "):
            break
        if "http" in stripped.lower():
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
        for idx, line in enumerate(lowered):
            if needle not in line:
                continue
            start = max(0, idx - 1)
            end = min(len(lines), idx + 3)
            snippet = "\n".join(normalize_title(row) for row in lines[start:end]).strip()
            snippets.append({"keyword": keyword, "snippet": snippet[:1400]})
            break
    return snippets


def stale_head_observations() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for rel in (
        ROOT / "docs" / "v37-omega-closeout-summary-v1.json",
        ROOT / "docs" / "v38-beta-handoff-policy-v1.json",
        ROOT / "docs" / "trinity-runtime-model-resolution-v1.json",
    ):
        payload = read_json(rel)
        observed_head = str(payload.get("current_head_sha") or "")
        if observed_head:
            rows.append(
                {
                    "path": str(rel.relative_to(ROOT)).replace("\\", "/"),
                    "current_head_sha": observed_head,
                }
            )
    return rows


def repo_truth() -> dict[str, Any]:
    runtime = read_json(ROOT / "docs" / "trinity-runtime-model-resolution-v1.json")
    return {
        "actual_current_head_sha": git_head(),
        "runtime_phase": str(runtime.get("phase") or ""),
        "google_drive_state": str(runtime.get("google_drive_state") or ""),
        "filesystem_promotion_state": str(runtime.get("filesystem_promotion_state") or ""),
        "materialization_level_actual": str(runtime.get("materialization_level_actual") or ""),
        "stale_head_observations": stale_head_observations(),
    }


def executable_decisions(api_titles: list[str]) -> list[str]:
    return [
        "Keep the v39 text file advisory-only and preserve repo proof surfaces as the only V38 authority.",
        "Refresh all V38 and V39 publications against the actual branch head instead of the stale v37/v38 pack SHA.",
        "Treat Anthos as a fleet-centered GKE Enterprise lane and require a Connect Gateway proof on the existing cluster.",
        "Treat Cloud OS Login as a real VM login proof lane, not just an API-enablement claim.",
        "Reuse Kai through the proven `npx @google/gemini-cli` route rather than requiring a global Gemini installation.",
        "Reuse Vesper Ion through the existing Bigtable durable-memory bridge and ingest V38 telemetry into that proven cloud lane.",
        f"Seed the enterprise API sweep from the parsed V39 API book ({len(api_titles)} titles parsed) while explicitly skipping non-project consumer and domain-scoped surfaces.",
    ]


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V38 Journey Advisory Digest",
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
    lines.extend(["", "## Stale Head Observations", ""])
    stale_rows = payload["repo_truth"].get("stale_head_observations", [])
    if stale_rows:
        lines.extend(
            f"- `{row['path']}` still references `{row['current_head_sha']}`"
            for row in stale_rows
        )
    else:
        lines.append("- none")
    lines.extend(["", "## Keyword Snippets", ""])
    for row in payload["proposal_snippets"]:
        lines.extend([f"### {row['keyword']}", "", row["snippet"], ""])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Distill the external v39 journey text into advisory-only V38 inputs.")
    parser.add_argument("--source", default=str(DEFAULT_SOURCE))
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()

    source = Path(args.source)
    raw_text = source.read_text(encoding="utf-8", errors="replace") if source.exists() else ""
    api_titles = extract_api_titles(raw_text)
    payload = {
        "generated_utc": now_iso(),
        "phase": "v38_omega",
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
