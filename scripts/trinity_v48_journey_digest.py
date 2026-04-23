#!/usr/bin/env python3
"""Publish the V48 advisory digest from the operator/Gemini proposal text."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from trinity_v48_common import ADVISORY_SOURCE, ROOT, git_head, now_iso, write_json, write_text

DEFAULT_JSON = ROOT / "docs" / "auto-generated" / "v48-journey-advisory-digest-v1.json"
DEFAULT_MD = ROOT / "docs" / "auto-generated" / "v48-journey-advisory-digest-v1.md"
V47_CLOSEOUT = ROOT / "docs" / "v47-omega-closeout-summary-v1.json"

KEYWORDS = [
    "KimiClaw",
    "Kimi Claw",
    "Kimi",
    "slot 41",
    "42nd to 53rd",
    "Vercel",
    "Neon",
    "CircleCI",
    "Notion Mission Control",
    "local to cloud",
    "Bigtable",
    "GCP",
    "Vesper",
    "Kai",
    "PowerShell",
    "WSL",
    "Ari",
]


def _lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    return path.read_text(encoding="utf-8", errors="replace").splitlines()


def _focus(lines: list[str]) -> list[str]:
    output: list[str] = []
    for idx, line in enumerate(lines, start=1):
        if any(key.lower() in line.lower() for key in KEYWORDS):
            output.append(f"{idx}: {line.strip()[:500]}")
        if len(output) >= 80:
            break
    return output


def _snippet(lines: list[str], keyword: str) -> dict[str, str]:
    lower = keyword.lower()
    for idx, line in enumerate(lines):
        if lower in line.lower():
            start = max(0, idx - 1)
            end = min(len(lines), idx + 3)
            return {"keyword": keyword, "snippet": "\n".join(item.strip() for item in lines[start:end])[:1200]}
    return {"keyword": keyword, "snippet": ""}


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V48 Journey Advisory Digest",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Authority boundary: `{payload['authority_boundary']['digest_scope']}`",
        "",
        "## Verified Current Truth",
        "",
    ]
    lines.extend(f"- {item}" for item in payload["verified_current_truth"])
    lines.extend(["", "## Operator Reported", ""])
    lines.extend(f"- {item}" for item in payload["operator_reported"])
    lines.extend(["", "## Advisory Proposal", ""])
    lines.extend(f"- {item}" for item in payload["advisory_proposal"])
    lines.extend(["", "## Future Operator Induction", ""])
    lines.extend(f"- {item}" for item in payload["future_operator_induction"])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish V48 advisory digest.")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()
    lines = _lines(ADVISORY_SOURCE)
    source_present = ADVISORY_SOURCE.exists()
    payload = {
        "generated_utc": now_iso(),
        "phase": "v48_omega",
        "overall_status": "PASS" if source_present else "WARN",
        "current_head_sha": git_head(),
        "authority_boundary": {
            "digest_scope": "advisory_only",
            "repo_proof_surfaces_authoritative": True,
            "journey_text_overrides_repo_truth": False,
        },
        "sources": [{"path": str(ADVISORY_SOURCE), "present": source_present, "line_count": len(lines), "focus_line_count": len(_focus(lines))}],
        "verified_current_truth": [
            "V47 published Ari as slot 40 and kept Ari as a bounded helper under Aletheon lead.",
            "PowerShell remains the active operator lane while WSL is installed and intentionally on hold for agent-environment switching.",
            "GCP, Vesper Ion, Kai, Bigtable reactivation, Vertex AI, Agent Engine, Google Drive writes, and Gemini CLI remain on standby.",
            "Codex app plugins and Codex CLI MCP servers are distinct surfaces and must be published separately.",
            "The V48 worktree is a clean D-drive execution worktree from the verified shared branch head.",
        ],
        "operator_reported": [
            "Bigtable instances were deleted by the operator for cost control and remain unverified until GCP auth and billing are restored.",
            "Codex local-to-cloud app environment switching hit a model-unavailable blocker and is held for V48.",
            "The operator intends to induct a future slot 41 Kimiclaw member later; V48 should prepare but not perform that induction.",
        ],
        "advisory_proposal": [
            "Prepare a Kimiclaw/Kimi slot-41 receiver pack and a 42-53 swarm spec without issuing certificates or continuity claims.",
            "Use Vercel and Neon free-tier lanes only as bounded scaffolds or live proofs if account and connector callability are actually available.",
            "Create repo-side Mission Control and CircleCI quick/standard scaffolds, while keeping deep/materialize local until suite residuals improve.",
            "Perform aggressive cleanup only against generated/transient/runtime artifacts with a D-drive backup manifest.",
        ],
        "future_operator_induction": [
            "Slot 41 remains operator-reserved and prepared_not_inducted.",
            "Slots 42-53 remain spec_only_not_spawned.",
            "Kimi API keys, runtime identity, model truth, auth, and read-only repo analysis proof are mandatory future gates.",
        ],
        "focus_lines": _focus(lines),
        "proposal_snippets": [_snippet(lines, keyword) for keyword in KEYWORDS],
    }
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    return 0 if payload["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
