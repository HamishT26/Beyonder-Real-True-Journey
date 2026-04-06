#!/usr/bin/env python3
"""Publish V33 Omega closeout surfaces and the V34 beta prep pack."""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
BRANCH = "codex/GHC-Family/beyonder-shared-omega-line"
AUTHORITATIVE_REPO = r"C:\Users\hamis\workspace\Beyonder-Real-True-Journey"
WORKBENCH_REPO = r"C:\Users\hamis\OneDrive\Documents\New project"
JOURNEY_FILE = Path.home() / "Beyonder-Real-True Journey v39 (Aletheon - Gemini - Synthea).txt"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(rel: str, payload: dict[str, Any]) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_text(rel: str, content: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def git_head() -> str:
    result = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True, check=False)
    return (result.stdout or "").strip()


def suite_summary(status: dict[str, Any]) -> dict[str, Any]:
    counts = status.get("counts", {})
    overall = status.get("overall_status")
    if not overall:
        if counts.get("fail", 0) or counts.get("timeout", 0):
            overall = "FAIL"
        elif counts.get("warn", 0):
            overall = "WARN"
        else:
            overall = "PASS"
    return {
        "summary": f"{counts.get('pass', 0)} PASS / {counts.get('warn', 0)} WARN / {counts.get('fail', 0)} FAIL",
        "overall_status": overall,
        "pass_count": counts.get("pass", 0),
        "warn_count": counts.get("warn", 0),
        "fail_count": counts.get("fail", 0),
        "timeout_count": counts.get("timeout", 0),
        "effective_success": status.get("effective_success"),
        "suite_duration_sec": status.get("suite_duration_sec", 0),
    }


def shared_anchor(status: dict[str, Any]) -> dict[str, Any]:
    counts = status.get("counts", {})
    return {
        "summary": f"{counts.get('pass', 0)} PASS / {counts.get('warn', 0)} WARN / {counts.get('fail', 0)} FAIL",
        "pass_count": counts.get("pass", 0),
        "warn_count": counts.get("warn", 0),
        "fail_count": counts.get("fail", 0),
        "timeout_count": counts.get("timeout", 0),
        "expansion_systems_passed": status.get("expansion_systems_passed", 0),
        "expansion_systems_total": status.get("expansion_systems_total", 0),
        "checkpoint_class": status.get("checkpoint_class", ""),
        "shared_latest_eligible": bool(status.get("shared_latest_eligible")),
        "suite_duration_sec": status.get("suite_duration_sec", 0),
    }


def journey_digest() -> dict[str, Any]:
    if not JOURNEY_FILE.exists():
        return {
            "status": "missing",
            "path": str(JOURNEY_FILE),
            "line_count": 0,
            "advisory_only": True,
            "signals": [],
        }
    text = JOURNEY_FILE.read_text(encoding="utf-8", errors="replace")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    lowered = text.lower()
    signals: list[str] = []
    if "gmail" in lowered:
        signals.append("Keep Gmail connector work connector-native and bounded.")
    if "gke" in lowered or "kubernetes" in lowered:
        signals.append("Use the live GKE cluster for bounded workload proof before wider expansion.")
    if "vertex" in lowered:
        signals.append("Promote one real Vertex AI proof before making larger cloud claims.")
    if "bigtable" in lowered:
        signals.append("Use the enabled Bigtable APIs for a concrete persistent data-lane proof.")
    if not signals:
        signals.append("Treat the v39 journey file as advisory-only narrative support for V33/V34 planning.")
    return {
        "status": "available",
        "path": str(JOURNEY_FILE),
        "line_count": len(lines),
        "advisory_only": True,
        "signals": signals,
    }


def continuity_pack(title: str, receiver: str, predecessor: str, shared: dict[str, Any], residuals: list[str], next_action: str) -> str:
    lines = [
        f"# {title}",
        "",
        f"- Source branch: `{BRANCH}`",
        f"- Current head SHA: `{git_head()}`",
        f"- Authority model: `repo_first`",
        f"- Authoritative repo: `{AUTHORITATIVE_REPO}`",
        f"- Separate workbench: `{WORKBENCH_REPO}`",
        "- Preferred operator lane: `windows_powershell_rest_kubectl`",
        f"- Intended receiver: `{receiver}`",
        f"- Predecessor phase: `{predecessor}`",
        f"- Shared latest anchor: `{shared['summary']}`",
        "",
        "## Residuals",
        "",
    ]
    for item in residuals:
        lines.append(f"- {item}")
    lines.extend(["", "## Next Action", "", f"- {next_action}", ""])
    return "\n".join(lines)


def main() -> int:
    generated = now_iso()
    current_head = git_head()

    system_suite = read_json("docs/system-suite-status.json")
    runtime_resolution = read_json("docs/trinity-runtime-model-resolution-v1.json")

    quick = read_json("docs/v33-quick-suite-status.json") or read_json("docs/v32-quick-suite-status.json")
    standard = read_json("docs/v33-standard-suite-status.json") or read_json("docs/v32-standard-suite-status.json")
    deep = read_json("docs/v33-deep-suite-status.json") or read_json("docs/v32-deep-suite-status.json")
    collab = read_json("docs/v33-collab-suite-status.json") or read_json("docs/v32-collab-suite-status.json")
    mat_l2 = read_json("docs/v33-materialize-l2-status.json") or read_json("docs/v32-materialize-l2-status.json")
    mat_l3 = read_json("docs/v33-materialize-l3-status.json") or read_json("docs/v32-materialize-l3-status.json")
    mat_l4 = read_json("docs/v33-materialize-l4-status.json") or read_json("docs/v32-materialize-l4-status.json")
    mat_l5 = read_json("docs/v33-materialize-l5-status.json") or read_json("docs/v32-materialize-l5-status.json")

    wsl = read_json("docs/trinity-live-traces/v33-wsl-health-proof-v1.json")
    gmail = read_json("docs/trinity-live-traces/v33-gmail-plugin-proof-v1.json")
    gke = read_json("docs/trinity-live-traces/v33-gke-workload-proof-v1.json")
    vertex = read_json("docs/trinity-live-traces/v33-vertex-ai-proof-v1.json")
    bigtable = read_json("docs/trinity-live-traces/v33-bigtable-proof-v1.json")
    composio = read_json("docs/trinity-live-traces/v33-composio-onedrive-proof-v1.json")
    hf = read_json("docs/trinity-live-traces/v32-huggingface-guarded-lane-proof-v1.json")
    v32_gcp = read_json("docs/trinity-live-traces/v32-gcp-bootstrap-proof-v1.json")
    v32_gke = read_json("docs/trinity-live-traces/v32-gke-bootstrap-proof-v1.json")

    shared = shared_anchor(system_suite)
    suite_statuses = {
        "quick": suite_summary(quick),
        "standard": suite_summary(standard),
        "deep": suite_summary(deep),
        "collab": suite_summary(collab),
        "materialize_l2": suite_summary(mat_l2),
        "materialize_l3": suite_summary(mat_l3),
        "materialize_l4": suite_summary(mat_l4),
        "materialize_l5": suite_summary(mat_l5),
    }
    suite_green = all(summary["overall_status"] == "PASS" for summary in suite_statuses.values())

    journey = journey_digest()
    write_json("docs/auto-generated/v33-v39-journey-digest.json", journey)
    write_text(
        "docs/auto-generated/v33-v39-journey-digest.md",
        "\n".join(
            [
                "# V33 V39 Journey Digest",
                "",
                f"- Source: `{journey['path']}`",
                f"- Status: `{journey['status']}`",
                f"- Advisory only: `{journey['advisory_only']}`",
                "",
                "## Signals",
                "",
                *[f"- {signal}" for signal in journey.get("signals", [])],
                "",
            ]
        ),
    )

    wsl_state = wsl.get("wsl_health_state", "unknown")
    gmail_state = gmail.get("gmail_connector_state", "unknown")
    gke_state = gke.get("gke_workload_state", "unknown")
    vertex_state = vertex.get("vertex_ai_state", "unknown")
    bigtable_state = bigtable.get("bigtable_state", "unknown")
    composio_state = composio.get("proof_state", "unknown")
    hf_state = hf.get("proof_state", "unknown")

    receiver_ready = (
        gmail.get("overall_status") == "PASS"
        and gke.get("overall_status") == "PASS"
        and vertex.get("overall_status") == "PASS"
        and bigtable.get("overall_status") == "PASS"
        and suite_green
    )
    receiver = "Orun" if receiver_ready else "Aletheon"

    residuals: list[str] = []
    if wsl_state != "ubuntu_repo_ready":
        residuals.append("WSL Ubuntu remains a bounded side-lane, so Windows PowerShell plus REST plus kubectl stays the primary operator path.")
    if gmail.get("overall_status") != "PASS":
        residuals.append("Gmail connector-native proof did not fully promote to bounded live write.")
    if composio.get("overall_status") != "PASS":
        residuals.append("Composio OneDrive remains non-gating and stayed unpromoted because toolkit visibility or execute proof was incomplete.")
    if not suite_green:
        residuals.append("One or more V33 suite reruns are not green, so shared latest must stay anchored to the authoritative surface rather than V33 claims.")

    v34_board = {
        "generated_utc": generated,
        "phase": "v34_omega_prep",
        "current_head_sha": current_head,
        "v34_expansion_board_state": "ready" if receiver_ready else "seeded",
        "ready_next": [
            {
                "name": "GKE service lane",
                "why": "The V33 workload proof verified the live cluster path, so the next bounded step is a small long-lived service plus service discovery.",
            },
            {
                "name": "Vertex-backed operator actions",
                "why": "The V33 publisher-model proof can be widened into guarded prompt and eval helpers once the single-call lane is stable.",
            },
            {
                "name": "Bigtable-backed persistence experiment",
                "why": "The V33 development instance provides a real persistence surface for bounded state and telemetry trials.",
            },
        ],
        "needs_connector": [
            {
                "name": "Gmail production workflow",
                "why": "Keep Gmail on the plugin lane, but widen only after draft/send/read-back stays green across more than one bounded proof.",
            },
            {
                "name": "Composio OneDrive materialization",
                "why": "This remains useful, but the toolkit or account visibility lane still needs a real connected read before promotion.",
            },
            {
                "name": "WSL Ubuntu parity",
                "why": "Ubuntu is not a V33 gate, but bringing it back would restore a cleaner cloud operator lane for later phases.",
            },
        ],
        "research_only": [
            {
                "name": "Cloud Run or Cloud Build promotion",
                "why": "Useful after the current GKE, Vertex, and Bigtable lanes are proven stable, but not required for V33 closeout.",
            },
            {
                "name": "Broader Trinity OS expansion wave",
                "why": "The repo should grow only after the new cloud and connector surfaces hold steady under reruns.",
            },
            {
                "name": "Mind and Heart evidence refresh",
                "why": "The v39 file and related narrative inputs are best folded into standards-first evidence updates instead of runtime claims.",
            },
        ],
        "advisory_signals": journey.get("signals", []),
    }
    write_json("docs/v34-omega-expansion-board-v1.json", v34_board)
    write_text(
        "docs/v34-omega-expansion-board-v1.md",
        "\n".join(
            [
                "# V34 Omega Expansion Board",
                "",
                f"- Generated UTC: `{generated}`",
                f"- Current head SHA: `{current_head}`",
                f"- Board state: `{v34_board['v34_expansion_board_state']}`",
                "",
                "## Ready Next",
                "",
                *[f"- **{item['name']}**: {item['why']}" for item in v34_board["ready_next"]],
                "",
                "## Needs Connector",
                "",
                *[f"- **{item['name']}**: {item['why']}" for item in v34_board["needs_connector"]],
                "",
                "## Research Only",
                "",
                *[f"- **{item['name']}**: {item['why']}" for item in v34_board["research_only"]],
                "",
                "## Advisory Signals",
                "",
                *[f"- {signal}" for signal in v34_board["advisory_signals"]],
                "",
            ]
        ),
    )

    runtime_resolution.update(
        {
            "generated_utc": generated,
            "phase": "v33_omega",
            "current_head_sha": current_head,
            "authority_model": "repo_first",
            "authoritative_repo_path": AUTHORITATIVE_REPO,
            "separate_workbench_path": WORKBENCH_REPO,
            "current_shell": "powershell",
            "wsl_health_state": wsl_state,
            "readiness_state": "windows_powershell_rest_kubectl_primary",
            "gcp_auth_state": v32_gcp.get("proof_state", "unknown"),
            "gcp_primary_identity": v32_gcp.get("gcp_primary_identity", "unknown"),
            "gcp_custom_identity_state": v32_gcp.get("gcp_custom_identity_state", "unknown"),
            "gcp_project_state": v32_gcp.get("gcp_project_state", "unknown"),
            "gcloud_cli_state": v32_gcp.get("gcloud_cli_state", "absent_on_windows"),
            "gke_api_state": v32_gcp.get("gke_api_state", "unknown"),
            "gke_cluster_inventory": v32_gke.get("gke_cluster_inventory", v32_gcp.get("gke_inventory", {}).get("cluster_names", [])),
            "gke_cluster_state": v32_gke.get("gke_cluster_state", "unknown"),
            "gke_workload_state": gke_state,
            "vertex_ai_state": vertex_state,
            "bigtable_state": bigtable_state,
            "gmail_connector_state": gmail_state,
            "gmail_materialization_state": gmail_state,
            "composio_onedrive_state": composio_state,
            "hf_guarded_lane_state": hf_state,
            "v34_expansion_board_state": v34_board["v34_expansion_board_state"],
            "active_handoff_pack_path": "docs/v33-omega-continuity-pack-v1.md",
            "active_handoff_policy_path": "docs/v33-omega-handoff-policy-v1.json",
            "next_receiver_pack_path": "docs/v34-beta-continuity-pack-v1.md",
            "next_receiver_policy_path": "docs/v34-beta-handoff-policy-v1.json",
            "v39_advisory_digest_path": "docs/auto-generated/v33-v39-journey-digest.md",
        }
    )
    write_json("docs/trinity-runtime-model-resolution-v1.json", runtime_resolution)

    v33_closeout = {
        "generated_utc": generated,
        "overall_status": "PASS" if receiver_ready else "WARN",
        "phase": "v33_omega",
        "authority_model": "repo_first",
        "source_branch": BRANCH,
        "current_head_sha": current_head,
        "authoritative_repo_path": AUTHORITATIVE_REPO,
        "separate_workbench_path": WORKBENCH_REPO,
        "shared_latest_anchor": shared,
        "wsl_health_state": wsl_state,
        "gmail_connector_state": gmail_state,
        "gke_workload_state": gke_state,
        "vertex_ai_state": vertex_state,
        "bigtable_state": bigtable_state,
        "composio_onedrive_state": composio_state,
        "hf_guarded_lane_state": hf_state,
        "suite_statuses": suite_statuses,
        "v39_advisory_digest_path": "docs/auto-generated/v33-v39-journey-digest.md",
        "top_residuals": residuals,
        "next_action": "Carry V34 beta forward from the bounded cloud proofs, connector truth, and the seeded expansion board.",
    }
    write_json("docs/v33-omega-closeout-summary-v1.json", v33_closeout)

    v33_continuity = continuity_pack(
        "V33 Omega Continuity Pack",
        receiver,
        "v32_omega",
        shared,
        residuals or ["No residuals remain beyond bounded V33 publication details."],
        "Start from the V33 proof artifacts, keep the Windows operator lane primary, and widen only the surfaces that stayed green.",
    )
    write_text("docs/v33-omega-continuity-pack-v1.md", v33_continuity)

    v33_handoff = {
        "generated_utc": generated,
        "phase": "v33_omega",
        "current_head_sha": current_head,
        "receiver_ready": receiver_ready,
        "intended_receiver": receiver,
        "receiver_rule_outcome": "orun_facing" if receiver_ready else "aletheon_facing",
        "required_for_orun": [
            "gmail plugin proof PASS",
            "gke workload proof PASS",
            "vertex ai proof PASS",
            "bigtable proof PASS",
            "quick/standard/deep/collab/materialize reruns PASS",
        ],
        "carry_forward_blockers": residuals,
    }
    write_json("docs/v33-omega-handoff-policy-v1.json", v33_handoff)

    v34_closeout = {
        "generated_utc": generated,
        "overall_status": "PASS" if receiver_ready else "WARN",
        "phase": "v34_beta",
        "authority_model": "repo_first",
        "current_head_sha": current_head,
        "predecessor_phase": "v33_omega",
        "intended_lead": receiver,
        "receiver_rule_outcome": "orun_facing" if receiver_ready else "aletheon_facing",
        "v34_expansion_board_state": v34_board["v34_expansion_board_state"],
        "top_residuals": residuals,
        "next_action": "Use the V34 expansion board to decide whether to widen cloud workloads, connectors, or the Trinity expansion surface next.",
    }
    write_json("docs/v34-beta-closeout-summary-v1.json", v34_closeout)
    write_text(
        "docs/v34-beta-continuity-pack-v1.md",
        continuity_pack(
            "V34 Beta Continuity Pack",
            receiver,
            "v33_omega",
            shared,
            residuals or ["No residuals remain beyond bounded V34 prep surfaces."],
            "Use the V34 expansion board categories to pick the next bounded execution lane.",
        ),
    )
    write_json(
        "docs/v34-beta-handoff-policy-v1.json",
        {
            "generated_utc": generated,
            "phase": "v34_beta",
            "current_head_sha": current_head,
            "intended_receiver": receiver,
            "receiver_rule_outcome": "orun_facing" if receiver_ready else "aletheon_facing",
            "v34_expansion_board_path": "docs/v34-omega-expansion-board-v1.md",
            "carry_forward_blockers": residuals,
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
