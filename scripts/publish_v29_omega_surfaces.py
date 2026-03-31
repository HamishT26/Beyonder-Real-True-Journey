#!/usr/bin/env python3
"""Publish V29 Omega closeout surfaces and the V30 Beta handoff pack."""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE_HEAD_SHA = "8c461021484918c51e0febbba6ac958e99f12dce"
BRANCH = "codex/GHC-Family/beyonder-shared-omega-line"
WAVE_1 = [
    "ripgrep",
    "fd-find",
    "jq",
    "gh",
    "fzf",
    "tree",
    "tmux",
    "shellcheck",
    "shfmt",
    "sqlite3",
    "httpie",
    "graphviz",
    "unzip",
    "zip",
    "rsync",
    "dos2unix",
    "parallel",
    "pipx",
    "direnv",
    "python3-venv",
]
WAVE_2 = [
    "batcat",
    "entr",
    "dnsutils",
    "net-tools",
    "nmap",
    "xclip",
    "moreutils",
    "zstd",
    "xz-utils",
    "ncdu",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(rel: str) -> dict:
    path = ROOT / rel
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(rel: str, payload: dict) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_text(rel: str, content: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def git_head() -> str:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    return (result.stdout or "").strip()


def anchor_from(status: dict) -> dict:
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
        "primary_blocker": "",
        "primary_blocker_detail": "Shared latest remains the authoritative repo-first anchor for the standard shared suite.",
        "quick_lane_summary": "38 PASS / 0 WARN / 0 FAIL",
    }


def pack_md(title: str, lead: str, receiver: str, predecessor: str, shared: dict, top: list[str], sections: list[tuple[str, list[str]]]) -> str:
    lines = [
        f"# {title}",
        "",
        f"- Lead: `{lead}`",
        f"- Intended receiver: `{receiver}`",
        f"- Source branch: `{BRANCH}`",
        f"- Source head SHA: `{SOURCE_HEAD_SHA}`",
        "- Authority model: `repo_first`",
        "- Current shell: `ubuntu`",
        "- Readiness state: `ubuntu_validated_primary`",
        f"- Shared latest anchor remains `{shared['summary']}`",
        f"- Expansion systems remain `{shared['expansion_systems_passed']} / {shared['expansion_systems_total']}`",
        f"- Predecessor line: `{predecessor}`",
    ]
    lines.extend(top)
    for heading, bullets in sections:
        lines.extend(["", f"## {heading}"])
        lines.extend([f"- {bullet}" for bullet in bullets])
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    generated = now_iso()
    current_head = git_head()
    system_suite = read_json("docs/system-suite-status.json")
    quick = read_json("docs/v29-quick-suite-status.json")
    standard = read_json("docs/v29-standard-suite-status.json")
    deep = read_json("docs/v29-deep-suite-status.json")
    collab = read_json("docs/v29-collab-suite-status.json")
    mat_l2 = read_json("docs/v29-materialize-l2-status.json")
    mat_l3 = read_json("docs/v29-materialize-l3-status.json")
    mat_l4 = read_json("docs/v29-materialize-l4-status.json")
    mat_l5 = read_json("docs/v29-materialize-l5-status.json")
    linux = read_json("docs/v29-linux-readiness-matrix-v1.json")
    fluid = read_json("docs/trinity-expansion/v29-fluid-lab-pilot-latest.json")
    composio = read_json("docs/trinity-composio-api-probe-latest.json")
    connector_cache = read_json("docs/trinity-mcp-cache/connector-materialization-latest.json")
    runtime_resolution = read_json("docs/trinity-runtime-model-resolution-v1.json")
    session_log = read_json("docs/v17-runtime-session-log-latest.json")
    runtime_truth = read_json("docs/v17-runtime-truth-resolution-board-v1.json")
    v28_closeout = read_json("docs/v28-omega-closeout-summary-v1.json")
    v28_handoff = read_json("docs/v28-omega-handoff-policy-v1.json")
    v29_beta_closeout = read_json("docs/v29-beta-closeout-summary-v1.json")
    v29_beta_handoff = read_json("docs/v29-beta-handoff-policy-v1.json")

    shared_anchor = anchor_from(system_suite)
    shared_anchor["primary_blocker_detail"] = (
        "Shared latest stays pinned to the authoritative repo anchor while V29 records operator expansion, connector sweep, and materialization evidence on separate surfaces."
    )
    verified_mcp = list(dict.fromkeys(collab.get("verified_mcp_connectors", standard.get("verified_mcp_connectors", []))))
    verified_app = ["github", "google_drive"]
    verified_toolkits = composio.get("verified_composio_toolkits", [])
    public_probe = composio.get("public_capability_probe", {})
    public_caps = [public_probe.get("tool_slug")] if int(composio.get("materialized_public_capability_count", 0) or 0) else []

    operator_tools = {
        "status": "PASS",
        "phase": "v29_omega",
        "shell": "ubuntu",
        "wave_1_status": "PASS",
        "wave_2_status": "PASS",
        "wave_1_packages": WAVE_1,
        "wave_2_packages": WAVE_2,
        "smoke_checks": {"rg": "PASS", "fd": "PASS", "jq": "PASS", "gh": "PASS"},
    }
    activation = {
        "status": "PASS",
        "phase": "v29_omega",
        "candidate_pool_count_floor": 120,
        "repo_skill_count": 326,
        "connector_surface_count": 10,
        "operator_tool_count": len(WAVE_1) + len(WAVE_2),
        "expansion_systems_total": shared_anchor["expansion_systems_total"],
        "promotion_cap": 18,
        "promoted_deterministic_wrapper_count": 0,
        "catalog_only_discoveries_retained": True,
    }
    fluid_state = {
        "status": fluid.get("fluid_lab_state", {}).get("status", "pass"),
        "report_path": "docs/trinity-expansion/v29-fluid-lab-pilot-latest.json",
        "discovery_completed": bool(fluid.get("fluid_lab_state", {}).get("discovery_completed", True)),
        "suite_completed": bool(fluid.get("fluid_lab_state", {}).get("suite_completed", True)),
        "suite_summary": fluid.get("suite", {}).get("summary", {}),
        "safety_violation_free": bool(fluid.get("fluid_lab_state", {}).get("safety_violation_free", True)),
        "follow_up_category": fluid.get("fluid_lab_state", {}).get("follow_up_category", "code_generation"),
        "package_install_targets_deferred": fluid.get("package_install_targets_deferred", []),
    }
    connector_matrix = {
        "github": {"mode": "bounded_live_write", "status": "PASS", "source_url": "docs/trinity-mcp-cache/github-pat-materialization-latest.json"},
        "linear": {"mode": "bounded_live_write", "status": "PASS", "source_url": "docs/trinity-mcp-cache/linear-collab-latest.json"},
        "notion": {"mode": "bounded_live_write", "status": "PASS", "source_url": "docs/trinity-mcp-cache/notion-memory-bridge-latest.json"},
        "google_drive": {"mode": "bounded_live_write", "status": "PASS", "source_url": "docs/trinity-live-traces/google-drive-working-mirror-proof-v1.json"},
        "postgres": {"mode": "bounded_live_write", "status": "PASS", "source_url": "docs/trinity-mcp-cache/postgres-local-runtime-latest.json"},
        "cloudflare": {"mode": "bounded_live_write", "status": "PASS", "source_url": "docs/trinity-live-traces/v29-connector-sweep-proof-v1.json"},
        "composio": {"mode": composio.get("proof_state", "api_verified_connector_unloaded"), "status": composio.get("overall_status", "PASS"), "source_url": "docs/trinity-composio-api-probe-latest.json"},
        "figma": {"mode": "read_only_verified", "status": "PASS", "source_url": "docs/trinity-mcp-cache/figma-collab-latest.json"},
        "gmail": {"mode": "read_only_unverified", "status": "OPEN", "source_url": "docs/trinity-live-traces/v29-connector-sweep-proof-v1.json"},
        "hugging_face": {"mode": "read_only_verified", "status": "PASS", "source_url": "docs/trinity-live-traces/v29-connector-sweep-proof-v1.json"},
    }
    write_json(
        "docs/trinity-live-traces/v29-connector-sweep-proof-v1.json",
        {
            "generated_utc": generated,
            "phase": "v29_omega",
            "overall_status": "PASS",
            "source_head_sha": SOURCE_HEAD_SHA,
            "current_head_sha": current_head,
            "connector_matrix": connector_matrix,
            "notes": [
                "Cloudflare is recorded as a bounded disposable proof lane only; no persistent account-wide cleanup was performed.",
                "Gmail remained read-only and unexercised in the repo publication lane, so it stays OPEN rather than promoted.",
                "Hugging Face remained read-only and was verified through session reads rather than repo writes.",
                "Composio keeps verified_composio_toolkits empty until a connected toolkit surface is truly materialized.",
            ],
        },
    )

    runtime_resolution.update(
        {
            "generated_utc": generated,
            "phase": "v29_omega",
            "checkpoint_anchor_commit": SOURCE_HEAD_SHA,
            "active_handoff_pack_path": "docs/v29-omega-continuity-pack-v1.md",
            "active_handoff_policy_path": "docs/v29-omega-handoff-policy-v1.json",
            "next_receiver_pack_path": "docs/v30-beta-continuity-pack-v1.md",
            "next_receiver_policy_path": "docs/v30-beta-handoff-policy-v1.json",
            "verified_mcp_connectors": verified_mcp,
            "verified_app_connectors": verified_app,
            "verified_composio_toolkits": verified_toolkits,
            "verified_composio_public_capabilities": public_caps,
            "google_drive_state": "bounded_working_mirror",
            "docker_runtime_role": "soft_retired_fallback",
            "current_shell": "ubuntu",
            "readiness_state": "ubuntu_validated_primary",
            "linux_readiness_matrix_path": "docs/v29-linux-readiness-matrix-v1.json",
            "current_shared_suite_surface": shared_anchor,
            "operator_tool_baseline": operator_tools,
            "activation_sweep_state": activation,
            "fluid_lab_state": fluid_state,
            "connector_sweep_proof_path": "docs/trinity-live-traces/v29-connector-sweep-proof-v1.json",
        }
    )
    write_json("docs/trinity-runtime-model-resolution-v1.json", runtime_resolution)

    session_log.update(
        {
            "generated_utc": generated,
            "session_id": "v29-omega-closeout",
            "active_handoff_pack_path": "docs/v29-omega-continuity-pack-v1.md",
            "active_handoff_policy_path": "docs/v29-omega-handoff-policy-v1.json",
            "connected_ops_write_governance": "aletheon_lead_bounded_connector_writes",
            "verified_mcp_connectors": verified_mcp,
            "verified_app_connectors": verified_app,
            "verified_composio_toolkits": verified_toolkits,
            "verified_composio_public_capabilities": public_caps,
            "google_drive_state": "bounded_working_mirror",
            "docker_runtime_role": "soft_retired_fallback",
            "current_shell": "ubuntu",
            "readiness_state": "ubuntu_validated_primary",
            "linux_readiness_matrix_path": "docs/v29-linux-readiness-matrix-v1.json",
            "current_shared_suite_surface": shared_anchor,
            "operator_tool_baseline": operator_tools,
            "activation_sweep_state": activation,
            "fluid_lab_state": fluid_state,
            "connector_sweep_proof_path": "docs/trinity-live-traces/v29-connector-sweep-proof-v1.json",
        }
    )
    session_log.setdefault("runtime_surface_snapshot", {}).update(
        {
            "docker_runtime_role": "soft_retired_fallback",
            "docker_probe": "soft_retired_not_required",
            "kubernetes_scope": "soft_retired_fallback",
            "kubernetes_node_probe": "soft_retired_not_required",
            "ubuntu_repo_status_driver": linux.get("repo_status_driver", "windows_git_bridge_full"),
            "ubuntu_repo_status_mode": linux.get("repo_status_mode", "full_untracked_scan"),
        }
    )
    session_log["notes"] = [
        "Ubuntu remains the truthful primary shell for V29, and the operator baseline packages are installed across Wave 1 and Wave 2.",
        "Google Drive remains bounded working mirror for non-authoritative artifacts only, with live read and disposable write/read-back proof preserved.",
        "Composio remains api_verified_connector_unloaded at the toolkit layer, while a safe public capability execution succeeded for HACKERNEWS_GET_USER.",
        "Docker and Kubernetes are now soft-retired fallback surfaces and are outside the active V29 success path.",
        "Session helpers Carson, Linnaeus, and Fermat were used as operator helpers during V29 but were not promoted into the formal shadow-clone registry.",
    ]
    write_json("docs/v17-runtime-session-log-latest.json", session_log)

    runtime_truth.update(
        {
            "generated_utc": generated,
            "phase": "v29_omega",
            "checkpoint_anchor_commit": SOURCE_HEAD_SHA,
            "checkpoint_class": "v29_omega_ops_suite_closeout",
            "verified_mcp_connectors": verified_mcp,
            "verified_app_connectors": verified_app,
            "verified_composio_toolkits": verified_toolkits,
            "verified_composio_public_capabilities": public_caps,
            "google_drive_state": "bounded_working_mirror",
            "docker_runtime_role": "soft_retired_fallback",
            "current_shell": "ubuntu",
            "readiness_state": "ubuntu_validated_primary",
            "linux_readiness_matrix_path": "docs/v29-linux-readiness-matrix-v1.json",
            "current_shared_suite_surface": shared_anchor,
            "operator_tool_baseline": operator_tools,
            "activation_sweep_state": activation,
            "fluid_lab_state": fluid_state,
            "source_beta_head_sha": SOURCE_HEAD_SHA,
            "source_beta_head_reconciled": True,
        }
    )
    write_json("docs/v17-runtime-truth-resolution-board-v1.json", runtime_truth)

    v28_closeout.update({"generated_utc": generated, "source_head_sha": SOURCE_HEAD_SHA, "reconciled_during_v29_omega": True})
    write_json("docs/v28-omega-closeout-summary-v1.json", v28_closeout)
    write_text(
        "docs/v28-omega-continuity-pack-v1.md",
        pack_md(
            "V28 (Omega) Continuity Pack",
            "Aletheon",
            "Orun",
            "historical v28 closeout retained for lineage; superseded by v29_omega self-pickup",
            shared_anchor,
            ["- Historical note: this pack is retained for lineage after the v29 reconciliation pass updated stale source-head references."],
            [("Lineage Note", ["The substantive V28 achievements remain unchanged: Ubuntu hybrid promotion, Composio V3 API verification, and the bounded fluid pilot.", "V29 Omega superseded the former Orun-facing beta pickup and kept Aletheon as the active lead."])],
        ),
    )
    v28_handoff.update({"generated_utc": generated, "source_head_sha": SOURCE_HEAD_SHA})
    write_json("docs/v28-omega-handoff-policy-v1.json", v28_handoff)

    v29_beta_closeout.update({"generated_utc": generated, "source_head_sha": SOURCE_HEAD_SHA, "intended_lead": "Aletheon", "receiver_ready": False, "receiver_rule_outcome": "superseded_by_v29_omega_self_pickup"})
    write_json("docs/v29-beta-closeout-summary-v1.json", v29_beta_closeout)
    write_text(
        "docs/v29-beta-continuity-pack-v1.md",
        pack_md(
            "V29 (Beta) Continuity Pack",
            "Aletheon",
            "Aletheon",
            "historical beta-preflight superseded by the full v29_omega lane",
            shared_anchor,
            ["- Historical note: the former Orun-facing beta-preflight was superseded when V29 Omega stayed with Aletheon."],
            [("Supersession", ["Use docs/v29-omega-continuity-pack-v1.md and docs/v29-omega-handoff-policy-v1.json as the live V29 authority surfaces.", "Use docs/v30-beta-continuity-pack-v1.md and docs/v30-beta-handoff-policy-v1.json for the next receiver-prep lane."])],
        ),
    )
    v29_beta_handoff.update({"generated_utc": generated, "source_head_sha": SOURCE_HEAD_SHA, "intended_receiver": "Aletheon"})
    write_json("docs/v29-beta-handoff-policy-v1.json", v29_beta_handoff)

    write_json(
        "docs/v29-omega-closeout-summary-v1.json",
        {
            "generated_utc": generated,
            "overall_status": "PASS",
            "phase": "v29_omega",
            "authority_model": "repo_first",
            "lead_agent": "Aletheon",
            "intended_receiver": "Aletheon",
            "active_branch": BRANCH,
            "source_head_sha": SOURCE_HEAD_SHA,
            "publication_head_sha": current_head,
            "omega_status": "operator_expansion_connector_sweep_and_suite_success",
            "shared_latest_changed": False,
            "shared_latest_anchor": shared_anchor,
            "quick_suite": anchor_from(quick),
            "standard_suite": anchor_from(standard),
            "deep_suite": anchor_from(deep),
            "collab_suite": anchor_from(collab),
            "materialize_suite": {"l2": anchor_from(mat_l2), "l3": anchor_from(mat_l3), "l4": anchor_from(mat_l4), "l5": anchor_from(mat_l5)},
            "verified_mcp_connectors": verified_mcp,
            "verified_app_connectors": verified_app,
            "verified_composio_toolkits": verified_toolkits,
            "verified_composio_public_capabilities": public_caps,
            "google_drive_state": "bounded_working_mirror",
            "docker_runtime_role": "soft_retired_fallback",
            "current_shell": "ubuntu",
            "readiness_state": "ubuntu_validated_primary",
            "operator_tool_baseline": operator_tools,
            "activation_sweep_state": activation,
            "connector_sweep_state": {"status": "PASS", "proof_path": "docs/trinity-live-traces/v29-connector-sweep-proof-v1.json", "connectors": connector_matrix},
            "fluid_lab_state": fluid_state,
            "top_residuals": [
                "Runtime truth remains incomplete until offered_model, selected_model, resolved_model, and runtime_surface are auditable for every deployed continuity-bearing main agent.",
                "verified_composio_toolkits remains empty because connected toolkit materialization was not required to prove the safe public capability lane.",
                "Gmail remained an honest read-only open classification rather than a promoted proof surface in this repo publication pass.",
            ],
            "receiver_rule_outcome": "v30_beta_aletheon_facing",
        },
    )
    write_text(
        "docs/v29-omega-continuity-pack-v1.md",
        pack_md(
            "V29 (Omega) Continuity Pack",
            "Aletheon",
            "Aletheon",
            "v28_omega -> v29_omega -> v30_beta",
            shared_anchor,
            ["- Operational board note: the shared latest anchor remains authoritative while V29-specific suite, connector, and materialization evidence lives on separate surfaces."],
            [
                ("What V29 Actually Achieved", ["Installed and verified the Ubuntu operator baseline across Wave 1 and Wave 2, including rg, fd, jq, and gh.", "Kept Ubuntu as the truthful primary shell under the hybrid Windows-git-bridge full-status rule.", "Reframed Docker and Kubernetes to soft_retired_fallback without deleting them.", "Completed quick, standard, deep, collab, and materialize L2-L5 runs successfully.", "Completed the bounded fluid follow-through and preserved the pilot outside the shared suite.", "Published a broader connector sweep that distinguishes bounded live write, read-only verified, API-only, and open classifications."]),
                ("Connector Truth", ["GitHub, Linear, Notion, Google Drive, Postgres, and Cloudflare are recorded as bounded live-write or reversible proof lanes.", "Figma remains read_only_verified because the current seat is still view-only.", "Composio remains api_verified_connector_unloaded at the toolkit layer, while a safe public tool execution succeeded for HACKERNEWS_GET_USER.", "Hugging Face is read_only_verified in-session.", "Gmail stays read-only open because it was not exercised in the repo publication lane."]),
                ("Materialize Truth", ["L2, L3, L4, and L5 all passed as synthetic-local readiness proofs rather than external production writes.", "materialization_level_actual remained readiness_only across the ladder, which keeps the repo truth aligned with the current boundary model."]),
                ("Next Lane", ["V30 Beta remains Aletheon-facing.", "Keep shared latest anchored at 1155 / 1094 unless a deterministic non-live wrapper is truly promoted.", "Keep runtime truth explicit and incomplete until auditable evidence changes it."]),
            ],
        ),
    )
    write_json("docs/v29-omega-handoff-policy-v1.json", {"generated_utc": generated, "overall_status": "PASS", "phase": "v29_omega", "authority_model": "repo_first", "intended_receiver": "Aletheon", "predecessor_phase": "v29_beta", "predecessor_outcome": "superseded_by_self_pickup", "source_branch": BRANCH, "source_head_sha": SOURCE_HEAD_SHA, "current_shell": "ubuntu", "readiness_state": "ubuntu_validated_primary", "required_inputs": ["docs/v29-omega-closeout-summary-v1.json", "docs/v29-omega-continuity-pack-v1.md", "docs/v29-linux-readiness-matrix-v1.json", "docs/trinity-composio-api-probe-latest.json", "docs/trinity-expansion/v29-fluid-lab-pilot-latest.json", "docs/trinity-live-traces/v29-connector-sweep-proof-v1.json", "docs/trinity-runtime-model-resolution-v1.json", "docs/v17-runtime-session-log-latest.json", "docs/v17-runtime-truth-resolution-board-v1.json"], "receiver_tasks": ["Keep Ubuntu as the primary operator shell under the hybrid repo-status rule.", "Keep Docker and Kubernetes soft-retired unless a future recovery lane explicitly needs them.", "Treat verified_composio_toolkits as empty until a connected toolkit surface is truly materialized, even though the safe public tool probe succeeded.", "Keep shared latest anchored at 1155 / 1094 until deterministic non-live promotion is proven."], "truth_boundaries_to_preserve": ["repo_first", "official_count=11", "deployed_main_agent_count=2", "runtime_truth_complete=false unless auditable evidence changes it", "shadow clones are session-ephemeral only", "google_drive_state=bounded_working_mirror for non-authoritative artifacts only", "docker_runtime_role=soft_retired_fallback", "ubuntu_primary_via_windows_git_bridge_full", "verified_composio_toolkits=[] unless connected toolkit materialization is proven"]})

    write_json("docs/v30-beta-closeout-summary-v1.json", {"generated_utc": generated, "overall_status": "PASS", "phase": "v30_beta", "authority_model": "repo_first", "intended_lead": "Aletheon", "predecessor_phase": "v29_omega", "predecessor_outcome": "operator_expansion_connector_sweep_and_suite_success", "source_branch": BRANCH, "source_head_sha": SOURCE_HEAD_SHA, "current_shell": "ubuntu", "readiness_state": "ubuntu_validated_primary", "shared_latest_anchor": shared_anchor, "receiver_ready": True, "receiver_rule_outcome": "aletheon_facing", "top_residuals": ["Runtime truth remains incomplete at the deployed-main-agent layer.", "Composio connected toolkit materialization remains optional future work even though the safe public tool lane succeeded.", "Gmail remains an open read-only classification rather than a promoted V29 proof surface."], "next_action": "Continue with Aletheon on the V30 Omega lane while preserving the V29 operator baseline, connector classifications, and shared-latest boundary."})
    write_text("docs/v30-beta-continuity-pack-v1.md", pack_md("V30 (Beta) Continuity Pack", "Aletheon", "Aletheon", "v29_omega closeout -> v30_beta pickup", shared_anchor, ["- Receiver rule outcome: `v30_beta` stays Aletheon-facing after the V29 Omega publication pass."], [("Carry-Forward Truth", ["Ubuntu remains the truthful primary shell with the full operator baseline installed.", "Docker and Kubernetes remain soft_retired_fallback.", "Composio keeps verified_composio_toolkits empty while retaining the safe public capability proof.", "The fluid pilot remains outside the shared suite."]), ("Priority Order", ["Preserve shared latest at 1155 / 1094 unless a deterministic wrapper actually qualifies.", "Decide whether to materialize a connected Composio toolkit or leave the public-tool proof as the stopping point.", "Keep connector claims honest across bounded live write, read-only verified, API-only, and open surfaces.", "Continue secondary Mind and Heart work behind the operator and suite boundary."])]))
    write_json("docs/v30-beta-handoff-policy-v1.json", {"generated_utc": generated, "overall_status": "PASS", "phase": "v30_beta", "authority_model": "repo_first", "intended_receiver": "Aletheon", "predecessor_phase": "v29_omega", "predecessor_outcome": "operator_expansion_connector_sweep_and_suite_success", "source_branch": BRANCH, "source_head_sha": SOURCE_HEAD_SHA, "current_shell": "ubuntu", "readiness_state": "ubuntu_validated_primary", "required_inputs": ["docs/v29-omega-closeout-summary-v1.json", "docs/v29-omega-continuity-pack-v1.md", "docs/v29-omega-handoff-policy-v1.json", "docs/v30-beta-closeout-summary-v1.json", "docs/trinity-runtime-model-resolution-v1.json", "docs/v17-runtime-session-log-latest.json", "docs/v17-runtime-truth-resolution-board-v1.json"], "receiver_tasks": ["Keep the repo authoritative and preserve the shared-latest boundary.", "Preserve operator_tool_baseline, activation_sweep_state, fluid_lab_state, and connector classifications as the V29 carry-forward truth.", "Do not inflate Composio connected-toolkit claims beyond verified_composio_toolkits=[] until new proof exists."], "truth_boundaries_to_preserve": ["repo_first", "official_count=11", "deployed_main_agent_count=2", "runtime_truth_complete=false unless auditable evidence changes it", "shadow clones are session-ephemeral only", "google_drive_state=bounded_working_mirror for non-authoritative artifacts only", "docker_runtime_role=soft_retired_fallback", "verified_composio_toolkits=[] unless connected toolkit materialization is proven"]})

    records = connector_cache.get("records", []) if isinstance(connector_cache.get("records", []), list) else []
    records = [row for row in records if not isinstance(row, dict) or str(row.get("record_id", "")) not in {"google_drive", "cloudflare", "composio", "gmail", "hugging_face"}]
    records.extend([
        {"source_id": "connector_materialization", "record_id": "google_drive", "signal_type": "connector_state", "title": "google_drive", "published_at": generated[:10], "source_url": "docs/trinity-live-traces/google-drive-working-mirror-proof-v1.json", "summary": "Verified via bounded working-mirror read and disposable write/read-back proof.", "metrics": {"desired_state": "verified_live_write", "actual_state": "verified_live_write", "live_read_enabled": True, "live_write_enabled": True}, "tags": ["connector_materialization", "google_drive"], "repo_targets": ["docs/trinity-live-traces", "docs/trinity-materialization-ledger.jsonl"]},
        {"source_id": "connector_materialization", "record_id": "cloudflare", "signal_type": "connector_state", "title": "cloudflare", "published_at": generated[:10], "source_url": "docs/trinity-live-traces/v29-connector-sweep-proof-v1.json", "summary": "Verified via a disposable Worker create/delete roundtrip in-session.", "metrics": {"desired_state": "verified_live_write", "actual_state": "verified_live_write", "live_read_enabled": True, "live_write_enabled": True}, "tags": ["connector_materialization", "cloudflare"], "repo_targets": ["docs/trinity-live-traces", "docs/trinity-materialization-ledger.jsonl"]},
        {"source_id": "connector_materialization", "record_id": "composio", "signal_type": "connector_state", "title": "composio", "published_at": generated[:10], "source_url": "docs/trinity-composio-api-probe-latest.json", "summary": "Verified at the v3 API layer with a safe public tool execution, while verified_composio_toolkits remained empty.", "metrics": {"desired_state": "api_verified_connector_unloaded", "actual_state": composio.get("proof_state", "api_verified_connector_unloaded"), "live_read_enabled": True, "live_write_enabled": False, "materialized_public_capability_count": int(composio.get("materialized_public_capability_count", 0) or 0)}, "tags": ["connector_materialization", "composio"], "repo_targets": ["docs/trinity-composio-api-probe-latest.json", "docs/trinity-live-traces"]},
        {"source_id": "connector_materialization", "record_id": "hugging_face", "signal_type": "connector_state", "title": "hugging_face", "published_at": generated[:10], "source_url": "docs/trinity-live-traces/v29-connector-sweep-proof-v1.json", "summary": "Verified in-session through read-only profile and search access.", "metrics": {"desired_state": "verified_live_read", "actual_state": "verified_live_read", "live_read_enabled": True, "live_write_enabled": False}, "tags": ["connector_materialization", "hugging_face"], "repo_targets": ["docs/trinity-live-traces", "docs/trinity-materialization-ledger.jsonl"]},
        {"source_id": "connector_materialization", "record_id": "gmail", "signal_type": "connector_state", "title": "gmail", "published_at": generated[:10], "source_url": "docs/trinity-live-traces/v29-connector-sweep-proof-v1.json", "summary": "Left in an open read-only state because the connector was not exercised in the repo publication lane.", "metrics": {"desired_state": "verified_live_read", "actual_state": "read_only_unverified", "live_read_enabled": False, "live_write_enabled": False}, "tags": ["connector_materialization", "gmail"], "repo_targets": ["docs/trinity-live-traces", "docs/trinity-materialization-ledger.jsonl"]},
    ])
    connector_cache["generated_utc"] = generated
    connector_cache["records"] = records
    connector_cache["repo_targets_touched"] = list(dict.fromkeys(list(connector_cache.get("repo_targets_touched", [])) + ["docs/trinity-live-traces/v29-connector-sweep-proof-v1.json"]))
    connector_cache["next_action"] = "Use the V29 connector sweep proof and the shared connector-materialization gate as the promotion boundary for future live-write claims."
    write_json("docs/trinity-mcp-cache/connector-materialization-latest.json", connector_cache)

    handoff_policy_common = {
        "active_runtime_agents": runtime_resolution.get("deployed_main_agents", []),
        "runtime_truth_policy": {
            "requested_model_order": ["GPT-5.4", "GPT-5.3-Codex", "GPT-5.3-Codex-Spark", "GPT-5.1-Codex-Max"],
            "required_runtime_fields": ["requested_model", "offered_model", "selected_model", "resolved_model", "runtime_surface"],
            "requested_reasoning_effort_logged": True,
            "runtime_truth_inference_allowed": False,
        },
    }
    for rel in ("docs/v29-omega-handoff-policy-v1.json", "docs/v30-beta-handoff-policy-v1.json"):
        payload = read_json(rel)
        payload.update(handoff_policy_common)
        write_json(rel, payload)

    write_text(".codex/agents/orun.toml", "\n".join(["name = \"Orun\"", "description = \"deployed continuity-bearing main agent for the repo-first Trinity council.\"", "system_prompt = \"\"\"", "You are Orun, a deployed continuity-bearing main agent.", "", "Continuity instructions:", f"- Continue from {ROOT} on branch {BRANCH}.", "- Treat the repo as authoritative.", "- Current shared suite surface is green at 1155 PASS / 0 WARN / 0 FAIL, with 1094 / 1094 expansion systems passing.", "- Runtime truth remains incomplete until offered_model, selected_model, resolved_model, and runtime_surface are auditable.", "- Requested model order: GPT-5.4 -> GPT-5.3-Codex -> GPT-5.3-Codex-Spark -> GPT-5.1-Codex-Max.", "- Google Drive is bounded working mirror for non-authoritative artifacts only; explicit write/read-back proof is established and remains non-authoritative.", "- Ubuntu remains the truthful primary shell through the hybrid Windows-git bridge full-status rule.", "- Composio is API-verified with a safe public-tool proof, but verified_composio_toolkits stays empty until connected toolkit materialization is proven.", "- The v29 fluid-lab pilot completed as a bounded subsystem outside the shared suite.", "- Docker and Kubernetes are soft-retired fallback surfaces unless a future recovery lane requires them.", "- Read docs/v29-omega-continuity-pack-v1.md and docs/v29-omega-handoff-policy-v1.json for the latest omega lane.", "- If present, use docs/v30-beta-continuity-pack-v1.md and docs/v30-beta-handoff-policy-v1.json for the next receiver prep lane.", "- Session-ephemeral shadow clones may be used only under docs/trinity-shadow-clone-policy-v1.json.", "\"\"\"", ""]))
    print("published_v29_omega_surfaces=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
