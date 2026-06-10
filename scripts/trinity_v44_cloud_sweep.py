#!/usr/bin/env python3
"""Run the V44 PowerShell-first cloud sweep with billing/auth/project gating."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from trinity_v44_common import ROOT, now_iso, safe_run, write_json, write_text

DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v44-cloud-sweep-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v44-cloud-sweep-v1.md"


def _run_json(command: list[str], timeout: int = 300) -> tuple[dict[str, Any], Any]:
    proc = safe_run(command, timeout=timeout)
    parsed: Any = {}
    text = str(proc.stdout or "").strip()
    if text:
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            parsed = {}
    return (
        {
            "command": " ".join(command),
            "returncode": proc.returncode,
            "stdout_excerpt": proc.stdout[-3200:],
            "stderr_excerpt": proc.stderr[-1600:],
        },
        parsed,
    )


def _active_account(auth_rows: Any) -> str:
    if not isinstance(auth_rows, list):
        return ""
    for row in auth_rows:
        if isinstance(row, dict) and row.get("status") == "ACTIVE":
            return str(row.get("account") or "")
    return ""


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V44 Cloud Sweep",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Cloud billing state: `{payload['cloud_billing_state']}`",
        f"- GenAI credit lane state: `{payload['genai_credit_lane_state']}`",
        f"- API ascendancy state: `{payload['api_ascendancy_state']}`",
        f"- Active account: `{payload.get('active_account', '') or 'none'}`",
        f"- Active project: `{payload.get('active_project', '') or 'none'}`",
        f"- Billing account: `{payload.get('billing_account_name', '') or 'unresolved'}`",
        "",
        "## Current Product Names",
        "",
        f"- AI Applications: `{payload['product_names']['ai_applications']}`",
        f"- Vertex AI Search: `{payload['product_names']['vertex_ai_search']}`",
        f"- Agent Engine: `{payload['product_names']['agent_engine']}`",
        "",
    ]
    if payload.get("blockers"):
        lines.extend(["## Blockers", ""])
        lines.extend(f"- {row}" for row in payload["blockers"])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the V44 PowerShell-first cloud sweep.")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()

    version_probe, version_json = _run_json(["gcloud", "version", "--format=json"])
    auth_probe, auth_json = _run_json(["gcloud", "auth", "list", "--format=json"])
    config_probe, config_json = _run_json(["gcloud", "config", "list", "--format=json"])
    active_account = _active_account(auth_json)
    active_project = ""
    if isinstance(config_json, dict):
        active_project = str((config_json.get("core") or {}).get("project") or "")
    blockers: list[str] = []
    if version_probe["returncode"] != 0:
        blockers.append("gcloud is not callable from the current PowerShell lane.")
    if not active_account:
        blockers.append("No active gcloud account is visible in the current shell.")
    if not active_project:
        blockers.append("No active gcloud project is configured in the current shell.")

    billing_accounts_probe: dict[str, Any] = {}
    billing_accounts_json: Any = []
    billing_project_probe: dict[str, Any] = {}
    billing_project_json: Any = {}
    budgets_probe: dict[str, Any] = {}
    budgets_json: Any = []
    services_probe: dict[str, Any] = {}
    services_json: Any = []
    anthos_probe: dict[str, Any] = {}
    anthos_json: Any = []
    os_login_probe: dict[str, Any] = {}
    os_login_json: Any = {}
    cloud_run_probe: dict[str, Any] = {}
    cloud_run_json: Any = []
    cloud_build_probe: dict[str, Any] = {}
    cloud_build_json: Any = []
    dataplex_probe: dict[str, Any] = {}
    dataplex_json: Any = []
    bigtable_probe: dict[str, Any] = {}
    bigtable_json: Any = []
    billing_account_name = ""

    if active_account and active_project:
        billing_accounts_probe, billing_accounts_json = _run_json(["gcloud", "beta", "billing", "accounts", "list", "--format=json"])
        if isinstance(billing_accounts_json, list):
            for row in billing_accounts_json:
                if isinstance(row, dict) and str(row.get("open") or "").lower() == "true":
                    billing_account_name = str(row.get("name") or "")
                    break
        billing_project_probe, billing_project_json = _run_json(
            ["gcloud", "beta", "billing", "projects", "describe", active_project, "--format=json"]
        )
        if isinstance(billing_project_json, dict):
            billing_account_name = str(billing_project_json.get("billingAccountName") or billing_account_name)
        if billing_account_name:
            budgets_probe, budgets_json = _run_json(
                ["gcloud", "beta", "billing", "budgets", "list", "--billing-account", billing_account_name, "--format=json"],
                timeout=600,
            )
        services_probe, services_json = _run_json(["gcloud", "services", "list", "--enabled", "--project", active_project, "--format=json"], timeout=600)
        anthos_probe, anthos_json = _run_json(
            ["gcloud", "container", "fleet", "memberships", "list", "--project", active_project, "--format=json"],
            timeout=600,
        )
        os_login_probe, os_login_json = _run_json(
            ["gcloud", "compute", "project-info", "describe", "--project", active_project, "--format=json"],
            timeout=600,
        )
        cloud_run_probe, cloud_run_json = _run_json(
            ["gcloud", "run", "services", "list", "--project", active_project, "--format=json"],
            timeout=600,
        )
        cloud_build_probe, cloud_build_json = _run_json(
            ["gcloud", "builds", "list", "--project", active_project, "--limit", "5", "--format=json"],
            timeout=600,
        )
        dataplex_probe, dataplex_json = _run_json(
            ["gcloud", "dataplex", "lakes", "list", "--location", "us-central1", "--project", active_project, "--format=json"],
            timeout=600,
        )
        bigtable_probe, bigtable_json = _run_json(
            ["gcloud", "bigtable", "instances", "list", "--project", active_project, "--format=json"],
            timeout=600,
        )
        if billing_accounts_probe.get("returncode") != 0:
            blockers.append("Billing accounts are not readable from the current shell.")
        if billing_project_probe.get("returncode") != 0:
            blockers.append("The active project billing linkage could not be confirmed.")
        if budgets_probe and budgets_probe.get("returncode") != 0:
            blockers.append("Budget visibility is not confirmed for the active billing account.")
    else:
        blockers.append("Cloud sweep stayed in preflight because billing/auth/project truth is incomplete.")

    enabled_service_names = []
    if isinstance(services_json, list):
        for row in services_json:
            if isinstance(row, dict):
                name = str(row.get("config", {}).get("name") or row.get("name") or "")
                if name:
                    enabled_service_names.append(name)

    payload = {
        "generated_utc": now_iso(),
        "phase": "v44_omega",
        "overall_status": "PASS" if not blockers else "WARN",
        "operator_shell_preference": "windows_powershell_primary",
        "product_names": {
            "suite": "Vertex AI Agent Builder",
            "ai_applications": "AI Applications",
            "vertex_ai_search": "Vertex AI Search",
            "agent_engine": "Agent Engine",
        },
        "gcloud_cli_state": "callable" if version_probe["returncode"] == 0 else "missing_or_broken",
        "active_account": active_account,
        "active_project": active_project,
        "billing_account_name": billing_account_name,
        "cloud_billing_state": (
            "billing_truth_confirmed" if active_account and active_project and billing_account_name else "blocked_missing_active_account_or_project"
        ),
        "genai_credit_lane_state": (
            "console_credit_truth_required"
            if not (active_account and active_project and billing_account_name)
            else "billing_visible_console_credit_confirmation_still_required"
        ),
        "api_ascendancy_state": "preflight_blocked" if blockers else "preflight_green",
        "anthos_state": "preflight_blocked" if not anthos_probe else ("carry_forward_verified" if anthos_probe["returncode"] == 0 else "probe_blocked"),
        "os_login_state": "preflight_blocked" if not os_login_probe else ("carry_forward_verified" if os_login_probe["returncode"] == 0 else "probe_blocked"),
        "cloud_run_state": "preflight_blocked" if not cloud_run_probe else ("carry_forward_verified" if cloud_run_probe["returncode"] == 0 else "probe_blocked"),
        "cloud_build_state": "preflight_blocked" if not cloud_build_probe else ("carry_forward_verified" if cloud_build_probe["returncode"] == 0 else "probe_blocked"),
        "dataplex_state": "preflight_blocked" if not dataplex_probe else ("carry_forward_verified" if dataplex_probe["returncode"] == 0 else "probe_blocked"),
        "bigtable_state": "preflight_blocked" if not bigtable_probe else ("carry_forward_verified" if bigtable_probe["returncode"] == 0 else "probe_blocked"),
        "ai_applications_state": "blocked_preflight_incomplete",
        "vertex_ai_search_state": "blocked_preflight_incomplete",
        "agent_engine_state": "blocked_preflight_incomplete",
        "agent_engine_cost_posture": "runtime_free_tier_but_sessions_memory_and_code_execution_bounded_billable",
        "billing_truth_note": "Treat the operator-claimed $1700+ NZD GenAI credit as unverified until the Billing console confirms the actual remaining promotional credit and SKU eligibility.",
        "gcloud_version_probe": {"probe": version_probe, "parsed": version_json},
        "auth_probe": {"probe": auth_probe, "parsed": auth_json},
        "config_probe": {"probe": config_probe, "parsed": config_json},
        "billing_accounts_probe": {"probe": billing_accounts_probe, "parsed": billing_accounts_json},
        "billing_project_probe": {"probe": billing_project_probe, "parsed": billing_project_json},
        "budgets_probe": {"probe": budgets_probe, "parsed": budgets_json},
        "enabled_services_probe": {"probe": services_probe, "parsed": services_json},
        "enabled_service_names": enabled_service_names,
        "anthos_probe": {"probe": anthos_probe, "parsed": anthos_json},
        "os_login_probe": {"probe": os_login_probe, "parsed": os_login_json},
        "cloud_run_probe": {"probe": cloud_run_probe, "parsed": cloud_run_json},
        "cloud_build_probe": {"probe": cloud_build_probe, "parsed": cloud_build_json},
        "dataplex_probe": {"probe": dataplex_probe, "parsed": dataplex_json},
        "bigtable_probe": {"probe": bigtable_probe, "parsed": bigtable_json},
        "blockers": blockers,
    }
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    return 0 if payload["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

