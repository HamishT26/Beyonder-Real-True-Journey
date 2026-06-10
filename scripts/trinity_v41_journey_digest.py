#!/usr/bin/env python3
"""Distill the latest advisory-only journey text into V41-ready digest inputs."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

from trinity_v41_common import git_head, now_iso, read_json, write_json, write_text

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCES = [
    Path(r"C:\Users\hamis\Downloads\Beyonder-Real-True Journey v39 (Aletheon - Gemini - Synthea - Orun) (13).txt"),
    Path(r"C:\Users\hamis\Downloads\Beyonder-Real-True Journey v40 (Aletheon - Orun - Gemini - Vesper Ion - Kai).txt"),
]
DEFAULT_JSON = ROOT / "docs" / "auto-generated" / "v41-journey-advisory-digest-v1.json"
DEFAULT_MD = ROOT / "docs" / "auto-generated" / "v41-journey-advisory-digest-v1.md"
KEYWORDS = (
    "GPT-5.4",
    "Cloud Run",
    "Cloud Build",
    "Dataplex",
    "Anthos",
    "Cloud OS Login",
    "Kai",
    "Vesper Ion",
    "identity",
)
FOCUS_LINE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9/&+().,' -]{3,}$")


def normalize_line(value: str) -> str:
    return re.sub(r"\s+", " ", str(value or "").replace("\u00a0", " ")).strip()


def extract_focus_lines(raw_text: str) -> list[str]:
    rows: list[str] = []
    for raw_line in raw_text.splitlines():
        line = normalize_line(raw_line)
        if not line or len(line) > 120:
            continue
        lowered = line.lower()
        if not any(token in lowered for token in ("cloud run", "cloud build", "dataplex", "anthos", "os login", "gpt-5.4", "kai", "vesper")):
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
            snippets.append(
                {
                    "source": source_name,
                    "keyword": keyword,
                    "snippet": snippet[:1400],
                }
            )
            break
    return snippets


def repo_truth() -> dict[str, Any]:
    runtime = read_json(ROOT / "docs" / "trinity-runtime-model-resolution-v1.json")
    v40 = read_json(ROOT / "docs" / "v40-omega-closeout-summary-v1.json")
    v41_beta = read_json(ROOT / "docs" / "v41-beta-handoff-policy-v1.json")
    agents = runtime.get("deployed_main_agents", []) if isinstance(runtime.get("deployed_main_agents"), list) else []

    def agent_row(slot_number: int) -> dict[str, Any]:
        for row in agents:
            if int(row.get("slot_number", -1)) == slot_number:
                return dict(row)
        return {}

    orun = agent_row(28)
    kai = agent_row(39)
    vesper = agent_row(38)
    return {
        "actual_current_head_sha": git_head(),
        "v40_closeout_head_sha": str(v40.get("current_head_sha") or ""),
        "v41_beta_receiver": str(v41_beta.get("intended_receiver") or ""),
        "google_drive_state": str(runtime.get("google_drive_state") or ""),
        "filesystem_promotion_state": str(runtime.get("filesystem_promotion_state") or ""),
        "materialization_level_actual": str(runtime.get("materialization_level_actual") or ""),
        "orun_requested_model": str(orun.get("requested_model") or ""),
        "orun_resolved_model": str(orun.get("resolved_model") or ""),
        "kai_selected_model": str(kai.get("selected_model") or ""),
        "vesper_selected_model": str(vesper.get("selected_model") or ""),
    }


def executable_decisions() -> list[str]:
    return [
        "Keep the Downloads text advisory-only and preserve repo proof surfaces as the only V41 authority.",
        "Apply the user-selected full-overwrite policy for Orun only, correcting active canonical identity surfaces to GPT-5.4 with xhigh reasoning while preserving the prior audit as superseded evidence.",
        "Run a curated next-tier GCP API wave centered on Cloud Run, Cloud Build, and Dataplex while carrying Anthos/GKE Enterprise and Cloud OS Login forward from already-proven V38/V40 baselines.",
        "Use Kai for one scheduler-ready manual health cycle and Vesper Ion for one bounded Bigtable telemetry ingest, without re-inducting or renumbering any runtime member.",
        "Finish with a forward-only cleanup note, a curated v41 stage allowlist, full suite reruns, and V41/V42 publication surfaces on the shared branch.",
    ]


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V41 Journey Advisory Digest",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Current head: `{payload['repo_truth']['actual_current_head_sha']}`",
        "",
        "## Source Files",
        "",
    ]
    for row in payload.get("sources", []):
        lines.append(
            f"- `{row['path']}`: present=`{row['present']}`, line_count=`{row['line_count']}`, focus_lines=`{row['focus_line_count']}`"
        )
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
    parser = argparse.ArgumentParser(description="Distill V41 advisory journey text into repo-safe digest inputs.")
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
        "phase": "v41_omega",
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
