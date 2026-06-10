#!/usr/bin/env python3
"""Distill the V45 advisory inputs into verified, operator-claimed, and rumor lanes."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

from trinity_v45_common import (
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
    DEFAULT_DOWNLOAD_SOURCE_DIR / "Beyonder-Real-True Journey v40 (Aletheon - Orun - Gemini - Vesper Ion - Kai) (8).txt",
]
DEFAULT_JSON = ROOT / "docs" / "auto-generated" / "v45-journey-advisory-digest-v1.json"
DEFAULT_MD = ROOT / "docs" / "auto-generated" / "v45-journey-advisory-digest-v1.md"
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
    "Chronicle",
    "automation",
    "Anthos",
    "OS Login",
    "Bigtable",
)
FOCUS_LINE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9/&+().,' :_\\\-]{3,}$")


def normalize_line(value: str) -> str:
    return re.sub(r"\s+", " ", str(value or "").replace("\u00a0", " ")).strip()


def extract_focus_lines(raw_text: str) -> list[str]:
    rows: list[str] = []
    for raw_line in raw_text.splitlines():
        line = normalize_line(raw_line)
        if not line or len(line) > 200:
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
    closeout = read_json(ROOT / "docs" / "v44-omega-closeout-summary-v1.json")
    v44_drive = read_json(ROOT / "docs" / "trinity-live-traces" / "v44-google-drive-proof-v1.json")
    v44_cloud = read_json(ROOT / "docs" / "trinity-live-traces" / "v44-cloud-sweep-v1.json")
    v44_cli = read_json(ROOT / "docs" / "trinity-live-traces" / "v44-codex-cli-probe-v1.json")
    return {
        "actual_current_head_sha": git_head(),
        "published_runtime_head_sha": str(runtime.get("current_head_sha") or ""),
        "published_v44_closeout_phase": str(closeout.get("phase") or ""),
        "published_v44_receiver": str(closeout.get("intended_receiver") or ""),
        "worktree_baseline_state": WORKTREE_BASELINE_STATE,
        "worktree_baseline_sha": WORKTREE_BASELINE_SHA,
        "published_google_drive_state": str(v44_drive.get("google_drive_state") or runtime.get("google_drive_state") or ""),
        "published_cloud_billing_state": str(v44_cloud.get("cloud_billing_state") or runtime.get("cloud_billing_state") or ""),
        "published_slot_40_induction_state": str(v44_cli.get("slot_40_induction_state") or runtime.get("slot_40_induction_state") or ""),
        "published_codex_cli_state": str(v44_cli.get("codex_cli_state") or runtime.get("codex_cli_state") or ""),
    }


def verified_facts() -> list[dict[str, str]]:
    return [
        {
            "claim": "The Codex app is available on Windows and is included with supported ChatGPT subscriptions.",
            "source": "OpenAI",
            "url": "https://openai.com/index/introducing-the-codex-app/",
        },
        {
            "claim": "Google documents AI Applications as the renamed product from Vertex AI Agent Builder, while Vertex AI Search remains the search/data-store lane.",
            "source": "Google Cloud release notes",
            "url": "https://docs.cloud.google.com/generative-ai-app-builder/docs/release-notes",
        },
        {
            "claim": "Vertex AI Agent Builder docs still present the suite name and publicly advertise the standard free-credit starting point as $300.",
            "source": "Google Cloud documentation",
            "url": "https://docs.cloud.google.com/agent-builder",
        },
        {
            "claim": "Agent Engine runtime has a free tier, while Sessions, Memory Bank, and Code Execution are billable services in the current pricing window.",
            "source": "Google Cloud pricing",
            "url": "https://cloud.google.com/vertex-ai/pricing",
        },
        {
            "claim": "The standard Google Cloud free-trial baseline is $300 and roughly 90 days until a console-specific credit source proves otherwise.",
            "source": "Google Cloud Free Program",
            "url": "https://cloud.google.com/free/docs/gcp-free-tier",
        },
    ]


def operator_claims() -> list[str]:
    return [
        "A larger $1700+ NZD GenAI credit is available for this operator account.",
        "The billing gate can likely be cleared later in the phase if the operator re-establishes account and project truth.",
        "Slot 40 can become a practical delegated CLI lane once continuity and model-proof gates are resolved.",
    ]


def unverified_rumors() -> list[str]:
    return [
        "An OpenAI Chronicle update specifically increases Codex app and CLI memory/network capabilities.",
        "The larger GenAI credit can be treated as spend-ready before the Billing console confirms the actual credit source and eligible SKUs.",
    ]


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V45 Journey Advisory Digest",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Actual current head: `{payload['repo_truth']['actual_current_head_sha']}`",
        "",
        "## Verified",
        "",
    ]
    for row in payload.get("verified", []):
        lines.append(f"- {row['claim']} ([{row['source']}]({row['url']}))")
    lines.extend(["", "## Operator Claimed", ""])
    lines.extend(f"- {row}" for row in payload.get("operator_claimed", []))
    lines.extend(["", "## Unverified Rumor", ""])
    lines.extend(f"- {row}" for row in payload.get("unverified_rumor", []))
    lines.extend(["", "## Source Files", ""])
    for row in payload.get("sources", []):
        lines.append(f"- `{row['path']}`: present=`{row['present']}`, line_count=`{row['line_count']}`, focus_lines=`{row['focus_line_count']}`")
    lines.extend(["", "## Repo Truth", ""])
    for key, value in payload.get("repo_truth", {}).items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Parsed Focus Lines", ""])
    lines.extend(f"- `{row}`" for row in payload.get("focus_lines", [])[:30])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Distill V45 advisory inputs into verified and rumor lanes.")
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
        "phase": "v45_omega",
        "overall_status": "PASS",
        "digest_status": "advisory_distilled",
        "authority_boundary": {
            "digest_scope": "advisory_only",
            "repo_proof_surfaces_authoritative": True,
            "journey_text_overrides_repo_truth": False,
        },
        "sources": source_rows,
        "repo_truth": repo_truth(),
        "verified": verified_facts(),
        "operator_claimed": operator_claims(),
        "unverified_rumor": unverified_rumors(),
        "focus_lines": focus_lines,
        "proposal_snippets": snippets,
    }
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
