#!/usr/bin/env python3
"""Publish the V45 cloud research-only digest until billing truth is restored."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from trinity_v45_common import ROOT, now_iso, safe_run, write_json, write_text

DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v45-cloud-research-digest-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v45-cloud-research-digest-v1.md"


def _probe(command: list[str]) -> dict[str, Any]:
    proc = safe_run(command, cwd=ROOT, timeout=180)
    return {
        "command": " ".join(command),
        "returncode": proc.returncode,
        "stdout_excerpt": proc.stdout[-2400:],
        "stderr_excerpt": proc.stderr[-1200:],
    }


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V45 Cloud Research Digest",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Cloud activation mode: `{payload['cloud_activation_mode']}`",
        f"- gcloud auth state: `{payload['gcloud_auth_state']}`",
        f"- gcloud project state: `{payload['gcloud_project_state']}`",
        f"- Billing console credit state: `{payload['billing_console_credit_state']}`",
        f"- Credit claim state: `{payload['credit_claim_state']}`",
        "",
        "## Official Product Names",
        "",
    ]
    for key, value in payload.get("official_product_names", {}).items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Activation Sequence", ""])
    lines.extend(f"- {row}" for row in payload.get("activation_sequence", []))
    lines.extend(["", "## Search / Agent Use Cases", ""])
    lines.extend(f"- {row}" for row in payload.get("research_use_cases", []))
    lines.extend(["", "## Source Anchors", ""])
    lines.extend(f"- {row['claim']} ([{row['source']}]({row['url']}))" for row in payload.get("verified_external_facts", []))
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish the V45 cloud research-only digest.")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()

    gcloud_auth = _probe(["gcloud", "auth", "list"])
    gcloud_config = _probe(["gcloud", "config", "list"])

    auth_probe_text = f"{gcloud_auth['stdout_excerpt']}\n{gcloud_auth['stderr_excerpt']}"
    auth_state = "no_active_account" if "No credentialed accounts." in auth_probe_text else "active_or_unknown"
    project_state = "no_active_project" if "project" not in gcloud_config["stdout_excerpt"].lower() else "active_or_unknown"
    cloud_activation_mode = "research_only_until_billing_truth" if auth_state == "no_active_account" or project_state == "no_active_project" else "manual_gate_ready"

    payload = {
        "generated_utc": now_iso(),
        "phase": "v45_omega",
        "overall_status": "WARN",
        "cloud_activation_mode": cloud_activation_mode,
        "gcloud_auth_state": auth_state,
        "gcloud_project_state": project_state,
        "billing_console_credit_state": "console_confirmation_required",
        "credit_claim_state": "operator_claim_unverified",
        "vertex_ai_credit_research_state": "bounded_research_ready",
        "kai_activation_state": "standby_waiting_for_billing_truth",
        "vesper_activation_state": "standby_waiting_for_billing_truth",
        "official_product_names": {
            "suite_name": "Vertex AI Agent Builder",
            "console_product_name": "AI Applications",
            "search_lane": "Vertex AI Search",
            "runtime_lane": "Agent Engine",
        },
        "activation_sequence": [
            "gcloud auth",
            "active project",
            "billing account plus budgets plus alerts",
            "Billing console credit capture",
            "read-only API and billing truth capture",
            "bounded low-cost AI Applications / Vertex AI Search proof",
            "bounded Agent Engine secondary proof",
        ],
        "research_use_cases": [
            "Use Vertex AI Search for bounded grounded-answer flows over operator-selected corpora.",
            "Prefer Google Drive-backed ingestion only if connector auth and Drive control are ready; otherwise fall back to Cloud Storage, then Bigtable-backed research surfaces.",
            "Keep Bigtable as the proven primary memory lane until Agent Engine runtime plus Sessions plus Memory Bank are stable and queryable.",
            "Treat Agent Engine runtime free tier separately from billable Sessions, Memory Bank, and Code Execution so v45 research does not overstate free usage.",
            "Keep Kai and Vesper Ion on standby until active account, project, and billing truth are restored.",
        ],
        "verified_external_facts": [
            {
                "claim": "Google documents AI Applications as the renamed product from Vertex AI Agent Builder.",
                "source": "Google Cloud release notes",
                "url": "https://docs.cloud.google.com/generative-ai-app-builder/docs/release-notes",
            },
            {
                "claim": "Vertex AI Agent Builder docs still present the suite name and the standard free-credit starting point as $300.",
                "source": "Google Cloud documentation",
                "url": "https://docs.cloud.google.com/agent-builder",
            },
            {
                "claim": "Agent Engine runtime has a monthly free tier, while Sessions, Memory Bank, and Code Execution are priced services.",
                "source": "Google Cloud pricing",
                "url": "https://cloud.google.com/vertex-ai/pricing",
            },
            {
                "claim": "The standard Google Cloud free-trial baseline remains $300 and about 90 days unless the billing console shows a different account-specific credit source.",
                "source": "Google Cloud Free Program",
                "url": "https://cloud.google.com/free/docs/gcp-free-tier",
            },
        ],
        "gcloud_auth_probe": gcloud_auth,
        "gcloud_config_probe": gcloud_config,
    }
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    return 1 if cloud_activation_mode == "research_only_until_billing_truth" else 0


if __name__ == "__main__":
    raise SystemExit(main())
