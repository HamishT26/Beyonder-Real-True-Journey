#!/usr/bin/env python3
"""Publish Kai's bounded PowerShell-orchestration summary for V44."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from trinity_v44_common import ROOT, now_iso, read_json, resolve_status, write_json, write_text

DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v44-kai-orchestration-bridge-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v44-kai-orchestration-bridge-v1.md"
SOURCES = [
    ROOT / "docs" / "trinity-live-traces" / "v44-operator-surface-probe-v1.json",
    ROOT / "docs" / "trinity-live-traces" / "v44-codex-capability-audit-v1.json",
    ROOT / "docs" / "trinity-live-traces" / "v44-cloud-sweep-v1.json",
    ROOT / "docs" / "trinity-live-traces" / "v44-codex-cli-probe-v1.json",
    ROOT / "docs" / "trinity-live-traces" / "v44-google-drive-proof-v1.json",
    ROOT / "docs" / "trinity-live-traces" / "v44-automation-registry-v1.json",
    ROOT / "docs" / "trinity-live-traces" / "v44-vesper-memory-cognitive-bridge-v1.json",
]


def _source_summary(path: Path) -> dict[str, Any]:
    payload = read_json(path)
    summary = {
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "present": path.exists(),
        "overall_status": resolve_status(payload),
    }
    for key in (
        "operator_shell_preference",
        "wsl_execution_mode",
        "worktree_baseline_state",
        "codex_capability_audit_state",
        "plugin_registry_state",
        "automation_backend_state",
        "cloud_billing_state",
        "google_drive_state",
        "codex_cli_state",
        "slot_40_induction_state",
        "vesper_cognitive_engine_state",
    ):
        if key in payload:
            summary[key] = payload[key]
    return summary


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V44 Kai Orchestration Bridge",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Kai orchestration state: `{payload['kai_orchestration_state']}`",
        f"- Manual cycle verified: `{payload['manual_cycle_verified']}`",
        f"- Headline: `{payload['headline']}`",
        "",
        "## Alerts",
        "",
    ]
    lines.extend(f"- {row}" for row in payload.get("alerts", []))
    lines.extend(["", "## Recommended Followups", ""])
    lines.extend(f"- {row}" for row in payload.get("recommended_followups", []))
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish Kai's bounded V44 PowerShell-orchestration summary.")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()

    source_summaries = [_source_summary(path) for path in SOURCES]
    alerts: list[str] = []
    if any(row.get("overall_status") == "WARN" for row in source_summaries):
        alerts.append("One or more bounded V44 proof lanes are still warning and need follow-up.")
    if any(str(row.get("codex_cli_state") or "").startswith("blocked") for row in source_summaries):
        alerts.append("Codex CLI remains blocked from the PowerShell lane, so slot 40 stays deferred.")
    if any(str(row.get("cloud_billing_state") or "").startswith("blocked") for row in source_summaries):
        alerts.append("Cloud billing, auth, or project truth is incomplete, so the broad cloud sweep cannot advance past preflight.")

    payload = {
        "generated_utc": now_iso(),
        "phase": "v44_omega",
        "overall_status": "PASS" if not alerts else "WARN",
        "kai_orchestration_state": "powershell_orchestration_summary_published",
        "manual_cycle_verified": True,
        "headline": "Kai remains a bounded PowerShell and CLI auditor for V44, not a new identity lane.",
        "audited_surfaces": [
            "PowerShell operator health",
            "worktree baseline",
            "plugin callable status",
            "automation backend truth",
            "cloud preflight deltas",
            "Codex CLI gate",
            "Google Drive connector proof",
        ],
        "alerts": alerts,
        "recommended_followups": [
            "Restore active gcloud account and project truth before any paid proof.",
            "Treat Google Billing console numbers as authoritative for promo credit, not chat claims.",
            "Keep slot 40 open until Codex CLI login, identity, memory, and model-resolution gates all pass.",
        ],
        "source_summaries": source_summaries,
    }
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    return 0 if payload["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

