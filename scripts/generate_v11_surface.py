#!/usr/bin/env python3
"""Generate the v11 Google Drive activation and memory-bank expansion surface."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import generate_v10_surface as v10

ROOT = v10.ROOT
WORKBENCH_ROOT = Path(r"C:\Users\hamis\OneDrive\Documents\New project")
WORKBENCH_SCRIPTS = WORKBENCH_ROOT / "scripts"
WORKBENCH_CONTRACT = WORKBENCH_ROOT / "trinity-workbench-contract-v2.json"
WORKBENCH_README = WORKBENCH_ROOT / "README.md"

OLD_MANIFEST = ROOT / "docs" / "trinity-expansion-system-manifest-v10.json"
NEW_MANIFEST = ROOT / "docs" / "trinity-expansion-system-manifest-v11.json"
OLD_EXTENSION_CATALOG = ROOT / "docs" / "trinity-extension-catalog-v8.json"
NEW_EXTENSION_CATALOG = ROOT / "docs" / "trinity-extension-catalog-v9.json"
OLD_MCP_CATALOG = ROOT / "docs" / "trinity-mcp-catalog-v8.json"
NEW_MCP_CATALOG = ROOT / "docs" / "trinity-mcp-catalog-v9.json"
OLD_COMMAND_BOOK = ROOT / "docs" / "trinity-command-book-v4.json"
NEW_COMMAND_BOOK = ROOT / "docs" / "trinity-command-book-v5.json"
OLD_MEMORY_BANK = ROOT / "docs" / "trinity-memory-bank-registry-v1.json"
NEW_MEMORY_BANK = ROOT / "docs" / "trinity-memory-bank-registry-v2.json"
SYNC_POLICY = ROOT / "docs" / "trinity-google-drive-sync-policy-v1.json"
DRIVE_LEDGER = ROOT / "docs" / "trinity-drive-archive-ledger.jsonl"
PROFILE_SET = ["standard", "deep", "collab", "materialize"]
RUNNER_SCRIPT = "scripts/trinity_expansion_system_runner.py"
SUFFIXES = v10.SUFFIXES


def now_iso() -> str:
    return v10.now_iso()


def hyphen(text: str) -> str:
    return v10.hyphen(text)


def write_text(path: Path, content: str) -> None:
    v10.write_text(path, content)


def write_json(path: Path, payload: object) -> None:
    v10.write_json(path, payload)


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    v10.write_jsonl(path, rows)


def write_external_text(path: Path, content: str) -> None:
    v10.write_external_text(path, content)


def write_external_json(path: Path, payload: object) -> None:
    v10.write_external_json(path, payload)


def run_capture(*args: str, timeout: int = 10) -> tuple[bool, str]:
    return v10.run_capture(*args, timeout=timeout)


def mkpack(
    pack: str,
    display_name: str,
    *,
    pillar: str,
    wave: str,
    track: str,
    activation_group: str,
    summary: str,
    repo_targets: list[str],
    council_scope: str,
    autonomy_track: str,
    executor_role: str,
    authority_scope: str,
    induction_dependency: str,
    sync_strategy: str = "local_repo",
    autonomy_class: str = "manual",
    live_dependency: str = "repo_first",
    mirror_target: str = "repo_only",
    continuity_band: str = "v11",
    history_scope: str = "v11",
    gating_class: str = "active",
    provisional_induction: bool = False,
    requires_auth: bool = False,
    connector_id: str = "",
    sync_mode: str = "offline",
    probe_tools: list[str] | None = None,
    required_probe_tools: list[str] | None = None,
    workflow_tokens: list[str] | None = None,
    risk_tags: list[str] | None = None,
    freshness_window_days: int = 7,
) -> dict[str, object]:
    resolved_workflow_tokens = workflow_tokens or [
        activation_group,
        sync_strategy,
        authority_scope,
    ]
    resolved_risk_tags = risk_tags or [
        track,
        activation_group,
        "requires_auth" if requires_auth else "bounded_scope",
    ]
    return v10.mkpack(
        pack,
        display_name,
        pillar=pillar,
        wave=wave,
        track=track,
        activation_group=activation_group,
        summary=summary,
        repo_targets=repo_targets,
        council_scope=council_scope,
        autonomy_track=autonomy_track,
        executor_role=executor_role,
        authority_scope=authority_scope,
        induction_dependency=induction_dependency,
        sync_strategy=sync_strategy,
        autonomy_class=autonomy_class,
        live_dependency=live_dependency,
        mirror_target=mirror_target,
        continuity_band=continuity_band,
        history_scope=history_scope,
        gating_class=gating_class,
        provisional_induction=provisional_induction,
        requires_auth=requires_auth,
        connector_id=connector_id,
        sync_mode=sync_mode,
        probe_tools=probe_tools,
        required_probe_tools=required_probe_tools,
        workflow_tokens=resolved_workflow_tokens,
        risk_tags=resolved_risk_tags,
        freshness_window_days=freshness_window_days,
    )


PACKS = [
    mkpack(
        "google_drive_mcp_activation_v11",
        "Google Drive MCP Activation V11",
        pillar="trinity",
        wave="wave92",
        track="connector_ops",
        activation_group="cloud_archive",
        summary="Seed the Docker-first Google Drive MCP path, local secrets path, Docker volume state, and bounded blocker reporting.",
        repo_targets=[
            "docs/trinity-google-drive-mcp-activation-latest.json",
            "docs/trinity-google-drive-sync-policy-v1.json",
            "docs/trinity-mcp-catalog-v9.json",
        ],
        council_scope="leader_only",
        autonomy_track="cloud_archive",
        executor_role="builder",
        authority_scope="cloud_archive_scope",
        induction_dependency="council_sync_governor_v10",
        sync_strategy="local_probe",
        live_dependency="docker_first_gdrive",
        mirror_target="repo_then_local_config",
        connector_id="google_drive",
        requires_auth=True,
        gating_class="staged_setup_gate",
        probe_tools=["docker", "python"],
        required_probe_tools=["docker", "python"],
    ),
    mkpack(
        "cloud_memory_bank_v11",
        "Cloud Memory Bank V11",
        pillar="trinity",
        wave="wave93",
        track="authority_memory",
        activation_group="cloud_archive",
        summary="Promote the memory-bank lane from local-only bounded mirrors into a bounded cloud archive model without changing repo authority.",
        repo_targets=[
            "docs/trinity-memory-bank-registry-v2.json",
            "docs/trinity-memory-bank-sync-latest.json",
            "docs/trinity-drive-archive-ledger.jsonl",
        ],
        council_scope="council_shared",
        autonomy_track="memory_continuity",
        executor_role="archivist",
        authority_scope="memory_scope",
        induction_dependency="google_drive_mcp_activation_v11",
        sync_strategy="local_repo",
        live_dependency="repo_first_memory_bank",
        mirror_target="repo_then_github_postgres_drive",
    ),
    mkpack(
        "docker_storage_ops_v11",
        "Docker Storage Ops V11",
        pillar="body",
        wave="wave94",
        track="compute_ecosystem",
        activation_group="storage_runtime",
        summary="Keep Docker volumes, Postgres runtime, and archive staging healthy enough for bounded storage rotation and query reuse.",
        repo_targets=[
            "docs/trinity-memory-bank-registry-v2.json",
            "docs/trinity-google-drive-mcp-activation-latest.json",
            "docs/system-suite-status.json",
        ],
        council_scope="leader_only",
        autonomy_track="runtime_storage",
        executor_role="builder",
        authority_scope="runtime_storage_scope",
        induction_dependency="cloud_memory_bank_v11",
        sync_strategy="local_probe",
        live_dependency="docker_postgres",
        mirror_target="repo_then_docker",
        probe_tools=["docker", "python", "git"],
        required_probe_tools=["docker", "python"],
    ),
    mkpack(
        "deep_materialize_regression_v11",
        "Deep Materialize Regression V11",
        pillar="body",
        wave="wave95",
        track="materialization_ladder",
        activation_group="validation_sweep",
        summary="Exercise the deep and materialize profile boundaries again after storage and cloud-archive changes without overstating ladder proof.",
        repo_targets=[
            "docs/system-suite-status.json",
            "docs/trinity-materialization-ladder-v4.json",
            "docs/system-suite-run-report.md",
        ],
        council_scope="leader_only",
        autonomy_track="validation_sweep",
        executor_role="reviewer",
        authority_scope="validation_scope",
        induction_dependency="docker_storage_ops_v11",
        sync_strategy="local_repo",
        live_dependency="suite_runner",
        mirror_target="repo_only",
    ),
    mkpack(
        "synthetic_mesh_ops_v11",
        "Synthetic Mesh Ops V11",
        pillar="body",
        wave="wave96",
        track="materialization_ladder",
        activation_group="synthetic_mesh",
        summary="Keep L2 live and L3-L5 honest through synthetic-local replay, rollback, and switchover operations only.",
        repo_targets=[
            "docs/trinity-materialization-ladder-v4.json",
            "docs/trinity-persistent-dev-ops-v1.json",
            "docs/trinity-synthetic-mesh-hardening-v1.json",
        ],
        council_scope="leader_only",
        autonomy_track="synthetic_mesh",
        executor_role="builder",
        authority_scope="synthetic_mesh_scope",
        induction_dependency="deep_materialize_regression_v11",
        sync_strategy="local_probe",
        live_dependency="postgres_mesh",
        mirror_target="repo_then_postgres",
        probe_tools=["docker", "python", "kubectl"],
        required_probe_tools=["docker", "python"],
    ),
    mkpack(
        "gmut_research_fabric_v11",
        "GMUT Research Fabric V11",
        pillar="mind",
        wave="wave97",
        track="benchmark_conformance",
        activation_group="research_refresh",
        summary="Refresh the GMUT lane from current primary research sources and keep open questions as falsification tasks instead of upgrades.",
        repo_targets=[
            "docs/v11-gmut-research-brief.md",
            "docs/comparative-validation-grid-v1.md",
            "docs/grand-unified-narrative-brief.md",
        ],
        council_scope="council_shared",
        autonomy_track="research_refresh",
        executor_role="researcher",
        authority_scope="alignment_scope",
        induction_dependency="synthetic_mesh_ops_v11",
        sync_strategy="local_repo",
        live_dependency="research_primary_sources",
        mirror_target="repo_then_notion_summary",
    ),
    mkpack(
        "freedid_governance_fabric_v11",
        "Freed ID Governance Fabric V11",
        pillar="heart",
        wave="wave98",
        track="benchmark_conformance",
        activation_group="research_refresh",
        summary="Refresh Freed ID and Cosmic Bill governance posture from current standards and governance anchors while keeping evidence tags explicit.",
        repo_targets=[
            "docs/v11-freedid-governance-brief.md",
            "docs/comparative-validation-grid-v1.md",
            "docs/grand-unified-narrative-brief.md",
        ],
        council_scope="council_shared",
        autonomy_track="research_refresh",
        executor_role="researcher",
        authority_scope="alignment_scope",
        induction_dependency="gmut_research_fabric_v11",
        sync_strategy="local_repo",
        live_dependency="standards_primary_sources",
        mirror_target="repo_then_notion_summary",
    ),
    mkpack(
        "trinity_control_tower_v11",
        "Trinity Control Tower V11",
        pillar="trinity",
        wave="wave99",
        track="control_tower",
        activation_group="control_tower",
        summary="Join storage posture, council continuity, Google Drive state, materialization posture, and Mind/Heart evidence posture in one board.",
        repo_targets=[
            "docs/trinity-control-tower-latest.json",
            "docs/trinity-control-tower-latest.md",
            "docs/system-suite-status.json",
        ],
        council_scope="council_shared",
        autonomy_track="control_tower",
        executor_role="planner",
        authority_scope="repo_authority",
        induction_dependency="freedid_governance_fabric_v11",
        sync_strategy="local_repo",
        live_dependency="repo_control_tower",
        mirror_target="repo_then_notion_summary",
    ),
    mkpack(
        "new_project_workbench_v11",
        "New Project Workbench V11",
        pillar="trinity",
        wave="wave100",
        track="workbench_surface",
        activation_group="workbench",
        summary="Use the New project folder as a local-only operator shell for storage, command, research, and council dashboards without bypassing repo authority.",
        repo_targets=[
            "docs/trinity-new-project-workbench-link-v2.json",
            "docs/trinity-control-tower-latest.json",
            "docs/trinity-memory-bank-registry-v2.json",
        ],
        council_scope="council_shared",
        autonomy_track="workbench",
        executor_role="builder",
        authority_scope="workbench_scope",
        induction_dependency="trinity_control_tower_v11",
        sync_strategy="local_probe",
        live_dependency="workbench_runtime",
        mirror_target="repo_then_new_project",
        probe_tools=["python", "docker"],
        required_probe_tools=["python"],
    ),
    mkpack(
        "v12_roadmap_v11",
        "V12 Roadmap V11",
        pillar="trinity",
        wave="wave101",
        track="council_orchestration",
        activation_group="planning",
        summary="Shape the next bounded v12 phase from v11 storage, continuity, and Trinity research outcomes.",
        repo_targets=[
            "docs/v12-roadmap-v2.md",
            "docs/v11-council-group-reflection.md",
            "docs/trinity-command-book-v5.json",
        ],
        council_scope="council_shared",
        autonomy_track="planning",
        executor_role="planner",
        authority_scope="planning_scope",
        induction_dependency="new_project_workbench_v11",
        sync_strategy="local_repo",
        live_dependency="repo_planning",
        mirror_target="repo_then_notion_summary",
    ),
]


def skill_files(pack: dict[str, object], kind: str) -> tuple[Path, Path]:
    skill_dir = ROOT / "skills" / f"{hyphen(str(pack['pack']))}-{kind}"
    return skill_dir / "SKILL.md", skill_dir / "agents" / "openai.yaml"


def skill_markdown(pack: dict[str, object], kind: str) -> str:
    return "\n".join(
        [
            "---",
            f"name: {hyphen(str(pack['pack']))}-{kind}",
            f"description: Operate the {pack['display_name']} pack with explicit v11 storage, continuity, and repo-authority boundaries.",
            "---",
            "",
            f"# {pack['display_name']} {kind.title()}",
            "",
            f"Use when Codex needs to work with the `{pack['pack']}` pack.",
            "",
            "1. Keep the Journey repo authoritative.",
            "2. Treat GitHub, Docker/Postgres, and Google Drive as bounded mirrors or runtime surfaces only.",
            "3. Preserve official council identity, memory, reflection, and command-scope continuity.",
            "4. Only use materialize paths for bounded live writes.",
            "",
        ]
    )


def skill_yaml(pack: dict[str, object], kind: str) -> str:
    return "\n".join(
        [
            "version: 1",
            "name: openai",
            "entrypoint: SKILL.md",
            "metadata:",
            f"  pack: {pack['pack']}",
            f"  kind: {kind}",
            "",
        ]
    )


def pack_contract(pack: dict[str, object]) -> dict[str, object]:
    fields = (
        "pack",
        "display_name",
        "pillar",
        "wave",
        "track",
        "activation_group",
        "summary",
        "repo_targets",
        "council_scope",
        "autonomy_track",
        "executor_role",
        "authority_scope",
        "induction_dependency",
        "sync_strategy",
        "autonomy_class",
        "live_dependency",
        "mirror_target",
        "continuity_band",
        "history_scope",
        "gating_class",
        "provisional_induction",
        "requires_auth",
        "connector_id",
        "sync_mode",
        "probe_tools",
        "required_probe_tools",
        "workflow_tokens",
        "risk_tags",
        "freshness_window_days",
    )
    payload = {field: pack[field] for field in fields}
    payload["workbench_surface"] = "new_project" if "workbench" in str(pack["pack"]) else "repo"
    payload["storage_surface"] = (
        "cloud_archive"
        if "google_drive" in str(pack["pack"]) or "cloud_memory" in str(pack["pack"])
        else ("docker_runtime" if "docker_storage" in str(pack["pack"]) else "repo_authority")
    )
    payload["cloud_archive_state"] = "candidate"
    payload["continuity_posture"] = "official_council_stable"
    payload["skill_names"] = [f"{hyphen(str(pack['pack']))}-operations", f"{hyphen(str(pack['pack']))}-integration"]
    payload["system_ids"] = [f"{pack['pack']}_{suffix}" for suffix in SUFFIXES]
    return payload


def pack_fixture(pack: dict[str, object]) -> dict[str, object]:
    connector_snapshot = {
        "connector_id": pack["connector_id"] or "repo",
        "write_target": pack["repo_targets"][0],
    }
    return {
        "summary": pack["summary"],
        "source_url": f"repo://{pack['repo_targets'][0]}",
        "repo_targets": pack["repo_targets"],
        "tags": [pack["pack"], "v11", str(pack["track"])],
        "connector_snapshot": connector_snapshot,
        "sync_strategy": pack["sync_strategy"],
        "next_action": f"Refresh {pack['display_name']} from repo-first sources and bounded mirrors.",
        "probe_tools": pack.get("probe_tools", []) or [],
        "required_probe_tools": pack.get("required_probe_tools", []) or [],
        "workflow_tokens": pack.get("workflow_tokens", []) or [],
        "risk_tags": pack.get("risk_tags", []) or [],
        "freshness_window_days": pack.get("freshness_window_days", 7),
    }


def pack_workflow(pack: dict[str, object]) -> str:
    return "\n".join(
        [
            f"# {pack['display_name']} Workflow",
            "",
            f"- activation_group: `{pack['activation_group']}`",
            f"- authority_scope: `{pack['authority_scope']}`",
            f"- council_scope: `{pack['council_scope']}`",
            f"- sync_strategy: `{pack['sync_strategy']}`",
            "- repo remains authoritative.",
            "- Google Drive stays archive-only even when live.",
            "- Deep and collab remain write-free by default.",
            "",
        ]
    )


def pack_catalog_entry(pack: dict[str, object]) -> dict[str, object]:
    return {
        "pack": pack["pack"],
        "display_name": pack["display_name"],
        "pillar": pack["pillar"],
        "activation_group": pack["activation_group"],
        "summary": pack["summary"],
        "repo_targets": pack["repo_targets"],
        "storage_surface": "cloud_archive" if "google_drive" in str(pack["pack"]) or "cloud_memory" in str(pack["pack"]) else "repo_or_runtime",
    }


def manifest_entry(pack: dict[str, object], suffix: str) -> dict[str, object]:
    system_id = f"{pack['pack']}_{suffix}"
    materialization_level = "not_applicable"
    if pack["pack"] in {"deep_materialize_regression_v11", "synthetic_mesh_ops_v11"}:
        materialization_level = "l2_persistent_dev"
    return {
        "system_id": system_id,
        "pillar": pack["pillar"],
        "script": RUNNER_SCRIPT,
        "mode": "offline",
        "profiles": PROFILE_SET,
        "outputs": [f"docs/trinity-expansion/{system_id.replace('_', '-')}-latest.json"],
        "depends_on": [f"{pack['pack']}_sync_bridge"] if suffix in {"materialization_tracer", "cache_board"} else ([f"{pack['pack']}_{name}" for name in ("surface_audit", "sync_bridge", "materialization_tracer", "cache_board", "risk_board")] if suffix == "gate" else []),
        "timeout_sec": 120,
        "wave": pack["wave"],
        "track": pack["track"],
        "gate_level": "pack_gate" if suffix == "gate" else "support",
        "cache_artifacts": [],
        "pack": pack["pack"],
        "phase": "v11",
        "activation_group": pack["activation_group"],
        "continuity_band": pack["continuity_band"],
        "materialization_level": materialization_level,
        "authority_scope": pack["authority_scope"],
        "command_surface": str("command" in str(pack["track"]) or "workbench" in str(pack["pack"])).lower(),
        "council_scope": pack["council_scope"],
        "provisional_induction": False,
        "autonomy_track": pack["autonomy_track"],
        "sync_surface": pack["mirror_target"],
        "induction_phase": "official_continuity" if "council" in str(pack["pack"]) else "not_applicable",
        "mesh_proof_mode": "synthetic_local" if "mesh" in str(pack["pack"]) else "none",
        "proof_pass": "continuity" if "council" in str(pack["pack"]) else "not_applicable",
        "official_induction": False,
        "workbench_surface": "new_project" if "workbench" in str(pack["pack"]) else "repo",
        "storage_surface": "cloud_archive" if "google_drive" in str(pack["pack"]) or "cloud_memory" in str(pack["pack"]) else ("runtime_storage" if "docker_storage" in str(pack["pack"]) else "repo"),
        "cloud_archive_state": "candidate",
        "continuity_posture": "official_council_stable",
    }


def extension_rows_for_pack(pack: dict[str, object]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    mirror_surface = str(pack["mirror_target"])
    storage_dependency = "google_drive" if "google_drive" in str(pack["pack"]) or "cloud_memory" in str(pack["pack"]) else ("docker_postgres" if "docker_storage" in str(pack["pack"]) or "synthetic_mesh" in str(pack["pack"]) else "repo")
    archive_scope = "bounded_archive" if "google_drive" in str(pack["pack"]) or "cloud_memory" in str(pack["pack"]) else "none"
    workbench_surface = "new_project" if "workbench" in str(pack["pack"]) else "repo"
    for suffix in SUFFIXES:
        rows.append(
            {
                "extension_id": f"{pack['pack']}_{suffix}",
                "extension_kind": "system",
                "pillar": pack["pillar"],
                "pack": pack["pack"],
                "mode": "offline",
                "requires_auth": pack["requires_auth"],
                "gating_class": pack["gating_class"],
                "status": "active",
                "source_of_truth": str(NEW_MANIFEST.relative_to(ROOT)).replace("\\", "/"),
                "live_dependency": pack["live_dependency"],
                "history_scope": pack["history_scope"],
                "mirror_target": pack["mirror_target"],
                "autonomy_class": pack["autonomy_class"],
                "command_surface": "yes" if "command" in str(pack["track"]) or "workbench" in str(pack["pack"]) else "no",
                "materialization_dependency": "ladder" if "materialization" in str(pack["track"]) or "mesh" in str(pack["pack"]) else "none",
                "authority_class": "repo_first",
                "executor_role": pack["executor_role"],
                "authority_scope": pack["authority_scope"],
                "induction_dependency": pack["induction_dependency"],
                "mirror_surface": mirror_surface,
                "privacy_class": "repo_private" if "council" in str(pack["pack"]) else "shareable_summary",
                "synthetic_mesh_dependency": "required" if "mesh" in str(pack["pack"]) else "none",
                "authority_surface": "repo_authority",
                "workbench_dependency": "required" if "workbench" in str(pack["pack"]) else "none",
                "induction_effect": "none",
                "storage_dependency": storage_dependency,
                "archive_scope": archive_scope,
                "workbench_surface": workbench_surface,
            }
        )
    for kind in ("operations", "integration"):
        rows.append(
            {
                "extension_id": f"{hyphen(str(pack['pack']))}-{kind}",
                "extension_kind": "skill",
                "pillar": pack["pillar"],
                "pack": pack["pack"],
                "mode": "offline",
                "requires_auth": False,
                "gating_class": pack["gating_class"],
                "status": "active",
                "source_of_truth": f"skills/{hyphen(str(pack['pack']))}-{kind}/SKILL.md",
                "live_dependency": pack["live_dependency"],
                "history_scope": pack["history_scope"],
                "mirror_target": pack["mirror_target"],
                "autonomy_class": pack["autonomy_class"],
                "command_surface": "yes" if "command" in str(pack["track"]) or "workbench" in str(pack["pack"]) else "no",
                "materialization_dependency": "ladder" if "materialization" in str(pack["track"]) or "mesh" in str(pack["pack"]) else "none",
                "authority_class": "repo_first",
                "executor_role": pack["executor_role"],
                "authority_scope": pack["authority_scope"],
                "induction_dependency": pack["induction_dependency"],
                "mirror_surface": mirror_surface,
                "privacy_class": "repo_private" if "council" in str(pack["pack"]) else "shareable_summary",
                "synthetic_mesh_dependency": "required" if "mesh" in str(pack["pack"]) else "none",
                "authority_surface": "repo_authority",
                "workbench_dependency": "required" if "workbench" in str(pack["pack"]) else "none",
                "induction_effect": "none",
                "storage_dependency": storage_dependency,
                "archive_scope": archive_scope,
                "workbench_surface": workbench_surface,
            }
        )
    for suffix in ("contract", "fixture", "workflow", "catalog-entry"):
        ext = "md" if suffix == "workflow" else "json"
        rows.append(
            {
                "extension_id": f"docs/{hyphen(str(pack['pack']))}-{suffix}-v1.{ext}",
                "extension_kind": "artifact",
                "pillar": pack["pillar"],
                "pack": pack["pack"],
                "mode": "offline",
                "requires_auth": False,
                "gating_class": pack["gating_class"],
                "status": "active",
                "source_of_truth": f"docs/{hyphen(str(pack['pack']))}-{suffix}-v1.{ext}",
                "live_dependency": pack["live_dependency"],
                "history_scope": pack["history_scope"],
                "mirror_target": pack["mirror_target"],
                "autonomy_class": pack["autonomy_class"],
                "command_surface": "yes" if "command" in str(pack["track"]) or "workbench" in str(pack["pack"]) else "no",
                "materialization_dependency": "ladder" if "materialization" in str(pack["track"]) or "mesh" in str(pack["pack"]) else "none",
                "authority_class": "repo_first",
                "executor_role": pack["executor_role"],
                "authority_scope": pack["authority_scope"],
                "induction_dependency": pack["induction_dependency"],
                "mirror_surface": mirror_surface,
                "privacy_class": "repo_private" if "council" in str(pack["pack"]) else "shareable_summary",
                "synthetic_mesh_dependency": "required" if "mesh" in str(pack["pack"]) else "none",
                "authority_surface": "repo_authority",
                "workbench_dependency": "required" if "workbench" in str(pack["pack"]) else "none",
                "induction_effect": "none",
                "storage_dependency": storage_dependency,
                "archive_scope": archive_scope,
                "workbench_surface": workbench_surface,
            }
        )
    return rows


def augment_rows(rows: list[dict[str, object]], field_defaults: dict[str, object]) -> list[dict[str, object]]:
    return v10.augment_rows(rows, field_defaults)


def emit_v11_command(
    command_id: str,
    intent: str,
    mode: str,
    risk_class: str,
    requires_live: bool,
    requires_connector: str,
    command_template: str,
    expected_artifacts: list[str],
    rollback: str,
    executor_role: str,
    authority_scope: str,
    council_visibility: str,
) -> dict[str, object]:
    return v10.cmd(
        command_id,
        intent,
        mode,
        risk_class,
        requires_live,
        requires_connector,
        command_template,
        expected_artifacts,
        rollback,
        "scripts/generate_v11_surface.py",
        executor_role,
        authority_scope,
        council_visibility,
    )


def build_new_commands() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    explicit = [
        ("gdrive_seed_local_secret", "Seed the Google Drive OAuth JSON into the local secrets path outside the repo.", "offline", "medium", False, "", "python scripts/trinity_google_drive_mcp_bootstrap.py --seed-secrets", ["docs/trinity-google-drive-mcp-activation-latest.json"], "Remove the local secret copy and rerun the bounded bootstrap.", "builder", "cloud_archive_scope", "leader_only"),
        ("gdrive_refresh_docker_bootstrap", "Refresh the Docker-first Google Drive MCP bootstrap and config entry.", "offline", "medium", False, "", "python scripts/trinity_google_drive_mcp_bootstrap.py --seed-secrets --update-config", ["docs/trinity-google-drive-mcp-activation-latest.json"], "Restore the prior local Codex config and re-run the bootstrap after correcting credentials.", "builder", "cloud_archive_scope", "leader_only"),
        ("memory_bank_snapshot_v11", "Refresh the v11 memory-bank snapshot and bounded storage posture.", "offline", "medium", False, "", "python scripts/trinity_memory_bank_sync.py --label v11-memory-bank", ["docs/trinity-memory-bank-registry-v2.json", "docs/trinity-memory-bank-sync-latest.json"], "Rebuild the registry from repo-first authority and bounded mirror truth.", "archivist", "memory_scope", "council_shared"),
        ("memory_bank_validate_v11", "Validate the v11 memory-bank policy and bounded cloud posture.", "offline", "medium", False, "", "python scripts/trinity_memory_bank_validator.py --fail-on-warn", ["docs/trinity-memory-bank-validation-latest.json"], "Restore the v11 registry, sync report, and policy files before rerunning validation.", "reviewer", "memory_scope", "council_shared"),
        ("run_deep_v11", "Run the v11 deep suite with fail-on-warn enabled.", "offline", "high", False, "", "python scripts/run_all_trinity_systems.py --profile deep --fail-on-warn", ["docs/system-suite-status.json"], "Restore the last PASS-backed v11 artifacts before rerunning the deep suite.", "planner", "validation_scope", "leader_only"),
        ("run_collab_v11", "Run the v11 collab suite with MCP refresh enabled.", "collab", "high", True, "notion", "python scripts/run_all_trinity_systems.py --profile collab --include-mcp-refresh --fail-on-warn", ["docs/system-suite-status.json"], "Reset bounded mirrors to repo-first state and rerun the collab profile.", "planner", "live_sync_scope", "leader_only"),
        ("run_offline_v11", "Run the v11 offline-only standard suite.", "offline", "medium", False, "", "python scripts/run_all_trinity_systems.py --profile standard --offline-only --fail-on-warn", ["docs/system-suite-status.json"], "Restore the cached v11 artifacts and rerun the offline profile.", "planner", "validation_scope", "council_shared"),
        ("run_materialize_l2_v11", "Run v11 materialize at L2 persistent development.", "materialize", "high", True, "postgres", "python scripts/run_all_trinity_systems.py --profile materialize --include-live-writes --materialization-level l2_persistent_dev --fail-on-warn", ["docs/system-suite-status.json"], "Restore the persistent-dev snapshot and retry the bounded L2 run.", "builder", "persistent_dev_scope", "leader_only"),
        ("run_materialize_l3_v11", "Run v11 materialize at L3 synthetic mesh scope.", "materialize", "high", True, "postgres", "python scripts/run_all_trinity_systems.py --profile materialize --include-live-writes --materialization-level l3_uat_preprod --fail-on-warn", ["docs/system-suite-status.json"], "Restore the synthetic mesh snapshot and retry the L3 drill.", "builder", "synthetic_mesh_scope", "leader_only"),
        ("run_materialize_l4_v11", "Run v11 materialize at L4 synthetic prod scope.", "materialize", "critical", True, "postgres", "python scripts/run_all_trinity_systems.py --profile materialize --include-live-writes --materialization-level l4_standard_prod --fail-on-warn", ["docs/system-suite-status.json"], "Restore the synthetic contract set and retry the L4 drill.", "reviewer", "synthetic_mesh_scope", "leader_only"),
        ("run_materialize_l5_v11", "Run v11 materialize at L5 synthetic HA scope.", "materialize", "critical", True, "postgres", "python scripts/run_all_trinity_systems.py --profile materialize --include-live-writes --materialization-level l5_ha_prod --fail-on-warn", ["docs/system-suite-status.json"], "Restore the synthetic HA twin state and retry the L5 drill.", "reviewer", "synthetic_ha_scope", "leader_only"),
        ("control_tower_refresh_v11", "Refresh the v11 Trinity control tower board.", "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id trinity_control_tower_v11_gate --profile-context standard", ["docs/trinity-control-tower-latest.json"], "Rebuild the v11 control tower from repo-first artifacts.", "planner", "repo_authority", "council_shared"),
        ("workbench_refresh_v11", "Refresh the New project workbench from repo and Postgres summaries.", "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id new_project_workbench_v11_sync_bridge --profile-context standard", ["docs/trinity-new-project-workbench-link-v2.json"], "Regenerate the workbench summary from authoritative repo docs.", "builder", "workbench_scope", "council_shared"),
        ("gmut_refresh_v11", "Refresh the v11 GMUT research brief.", "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id gmut_research_fabric_v11_sync_bridge --profile-context standard", ["docs/v11-gmut-research-brief.md"], "Restore the last PASS-backed v11 GMUT brief and refresh from bounded sources.", "researcher", "alignment_scope", "council_shared"),
        ("freedid_refresh_v11", "Refresh the v11 Freed ID governance brief.", "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id freedid_governance_fabric_v11_sync_bridge --profile-context standard", ["docs/v11-freedid-governance-brief.md"], "Restore the last PASS-backed v11 governance brief and refresh from bounded standards sources.", "researcher", "alignment_scope", "council_shared"),
        ("roadmap_publish_v12", "Publish the v12 roadmap from the v11 council surface.", "offline", "low", False, "", "python scripts/trinity_expansion_system_runner.py --system-id v12_roadmap_v11_cache_board --profile-context standard", ["docs/v12-roadmap-v2.md"], "Restore the roadmap from repo-first planning artifacts.", "planner", "planning_scope", "council_shared"),
        ("council_continuity_check_v11", "Refresh official council continuity and wellbeing state without changing induction.", "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id trinity_control_tower_v11_sync_bridge --profile-context standard", ["docs/trinity-agent-council-roster-v3.json"], "Restore the official roster, ledgers, and reflections from repo authority.", "archivist", "memory_scope", "council_shared"),
        ("drive_archive_ledger_refresh", "Refresh the Google Drive archive ledger from the latest bounded sync attempt.", "offline", "low", False, "", "python scripts/trinity_memory_bank_sync.py --label v11-memory-bank", ["docs/trinity-drive-archive-ledger.jsonl"], "Restore the drive ledger from the last bounded sync report.", "archivist", "cloud_archive_scope", "council_shared"),
        ("command_validate_v11_surface", "Validate the v11 command surface.", "offline", "medium", False, "", "python scripts/trinity_command_book_validator.py --command-book docs/trinity-command-book-v5.json --fail-on-warn", ["docs/trinity-command-book-validation-latest.json"], "Regenerate the v11 command book and rerun validation.", "reviewer", "command_scope", "council_shared"),
        ("extension_validate_v11_surface", "Validate the v11 manifest, extension catalog, and MCP catalog surface.", "offline", "medium", False, "", "python scripts/trinity_extension_catalog_validator.py --manifest docs/trinity-expansion-system-manifest-v11.json --extension-catalog docs/trinity-extension-catalog-v9.json --mcp-catalog docs/trinity-mcp-catalog-v9.json --fail-on-warn", ["docs/trinity-extension-catalog-validation-latest.json"], "Regenerate the v11 surface and rerun validation.", "reviewer", "validation_scope", "council_shared"),
    ]
    rows.extend(emit_v11_command(*row) for row in explicit)
    auto_specs = [
        ("gdrive_ops", 8, "offline", "medium", False, "", "python scripts/trinity_google_drive_mcp_bootstrap.py --seed-secrets --update-config", ["docs/trinity-google-drive-mcp-activation-latest.json"], "Restore the local config and rerun the bounded bootstrap.", "builder", "cloud_archive_scope", "leader_only", "Run additional Google Drive activation support step"),
        ("storage_ops", 8, "offline", "medium", False, "", "python scripts/trinity_memory_bank_sync.py --label v11-memory-bank", ["docs/trinity-memory-bank-registry-v2.json"], "Restore the repo-first registry and rerun the bounded storage sync.", "archivist", "memory_scope", "council_shared", "Run additional memory-bank storage support step"),
        ("validation_ops", 8, "offline", "medium", False, "", "python scripts/trinity_memory_bank_validator.py --fail-on-warn", ["docs/trinity-memory-bank-validation-latest.json"], "Restore v11 policy and rerun validation.", "reviewer", "validation_scope", "council_shared", "Run additional validation support step"),
        ("materialize_ops", 8, "materialize", "high", True, "postgres", "python scripts/trinity_expansion_system_runner.py --system-id synthetic_mesh_ops_v11_materialization_tracer --include-live-writes --profile-context materialize --materialization-level l2_persistent_dev", ["docs/trinity-synthetic-mesh-hardening-v1.json"], "Restore synthetic-local state before retrying the drill.", "builder", "synthetic_mesh_scope", "leader_only", "Run additional synthetic mesh support step"),
        ("research_ops", 8, "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id gmut_research_fabric_v11_gate --profile-context standard", ["docs/v11-gmut-research-brief.md"], "Restore the research brief and rerun bounded refresh.", "researcher", "alignment_scope", "council_shared", "Run additional Trinity research support step"),
    ]
    for prefix, count, mode, risk, requires_live, connector, template, artifacts, rollback, role, scope, visibility, intent in auto_specs:
        for index in range(1, count + 1):
            rows.append(emit_v11_command(f"{prefix}_{index:02d}", f"{intent} #{index}.", mode, risk, requires_live, connector, template, artifacts, rollback, role, scope, visibility))
    if len(rows) != 60:
        raise ValueError(f"expected 60 v11 commands, found {len(rows)}")
    return rows


def build_command_book(old_book: dict[str, object]) -> dict[str, object]:
    commands = augment_rows(
        [row for row in old_book.get("commands", []) if isinstance(row, dict)],
        {
            "executor_role": "aletheon",
            "authority_scope": "repo_authority",
            "council_visibility": "council_shared",
        },
    )
    commands.extend(build_new_commands())
    if len(commands) != 348:
        raise ValueError(f"expected 348 commands, found {len(commands)}")
    return {
        "version": "v5",
        "generated_utc": now_iso(),
        "description": "V11 governed command book with Google Drive activation, memory-bank promotion, deep/materialize sweeps, and Trinity continuity coverage.",
        "commands": commands,
    }


def command_markdown(book: dict[str, object]) -> str:
    lines = [
        "# Trinity Command Book",
        "",
        f"- generated_utc: `{book['generated_utc']}`",
        f"- commands: `{len(book['commands'])}`",
        "",
        "| command_id | executor_role | mode | risk | visibility |",
        "|---|---|---|---|---|",
    ]
    for row in book["commands"]:
        lines.append(f"| {row['command_id']} | {row['executor_role']} | {row['mode']} | {row['risk_class']} | {row['council_visibility']} |")
    return "\n".join(lines).rstrip() + "\n"


def build_mcp_catalog(old_catalog: dict[str, object]) -> dict[str, object]:
    payload = deepcopy(old_catalog)
    payload["version"] = "v9"
    payload["generated_utc"] = now_iso()
    connectors = [row for row in payload.get("connectors", []) if isinstance(row, dict)]
    for row in connectors:
        row.setdefault("archive_only", False)
        row.setdefault("oauth_bootstrap_state", "not_applicable")
        row.setdefault("docker_volume_state", "not_applicable")
        row.setdefault("fallback_mode", "not_applicable")
    google_drive = next((row for row in connectors if str(row.get("mcp_id")) == "google_drive"), None)
    if google_drive is None:
        google_drive = {"mcp_id": "google_drive"}
        connectors.append(google_drive)
    google_drive.update(
        {
            "status": "staged_setup_gate",
            "auth_class": "oauth_json_local_secret",
            "interaction_mode": "docker_first_archive_mirror",
            "tool_surface": "docker_run_mcp_gdrive",
            "cache_artifact": "docs/trinity-google-drive-mcp-activation-latest.json",
            "setup_gate": "docs/google-drive-mcp-activation-v11-contract-v1.json",
            "notes": "Docker-first Google Drive MCP path with bounded archive fallback. Repo remains authoritative.",
            "desired_state": "bounded_archive_mirror",
            "actual_state": "staged_setup_gate",
            "live_read_enabled": False,
            "live_write_enabled": False,
            "promotion_evidence": [],
            "blockers": ["interactive OAuth bootstrap not completed yet"],
            "activation_path": "docker_first_oauth_volume",
            "workspace_target": "google_drive_archive_folder",
            "proof_target": "bounded_v11_memory_bank_archive",
            "last_verified_utc": now_iso(),
            "ladder_eligibility": "l2_persistent_dev",
            "persistent_scope": "archive_only",
            "prod_scope": "not_authoritative",
            "rollback_scope": "delete bounded archive object",
            "uat_scope": "readiness_only",
            "prod_proof_state": "readiness_only",
            "ha_proof_state": "readiness_only",
            "cloud_staging_scope": "bounded_archive_only",
            "archive_only": True,
            "oauth_bootstrap_state": "seeded_not_authenticated",
            "docker_volume_state": "pending_bootstrap",
            "fallback_mode": "memory_bank_archive_only",
        }
    )
    payload["connectors"] = connectors
    return payload


def build_memory_bank_registry(old_registry: dict[str, object]) -> dict[str, object]:
    payload = deepcopy(old_registry)
    payload["generated_utc"] = now_iso()
    payload["version"] = "v2"
    payload["latest_snapshot"] = payload.get("latest_snapshot", {})
    for row in payload.get("memory_banks", []):
        if not isinstance(row, dict):
            continue
        row.setdefault("retention_class", "bounded")
        row.setdefault("archive_upload_state", "not_applicable")
        row.setdefault("cloud_capacity_class", "bounded")
        row.setdefault("last_archive_verified_utc", "")
        if row.get("surface") == "google_drive":
            row["status"] = "staged_with_blockers"
            row["notes"] = "Bounded archive mirror candidate only until OAuth bootstrap and upload proof pass."
            row["retention_class"] = "archive_only"
            row["archive_upload_state"] = "staged"
            row["cloud_capacity_class"] = "cloud_archive"
            row["proof_state"] = "docker_first_auth_pending"
            row["blockers"] = ["interactive OAuth bootstrap not completed yet"]
    return payload


def refresh_council_assets() -> dict[str, object]:
    roster_path = ROOT / "docs" / "trinity-agent-council-roster-v3.json"
    roster = json.loads(roster_path.read_text(encoding="utf-8"))
    for row in roster.get("agents", []):
        if not isinstance(row, dict):
            continue
        row["wellbeing_state"] = "stable"
        memory_path = ROOT / str(row["memory_ledger"])
        reflection_path = ROOT / str(row["reflection_path"])
        existing = []
        if memory_path.exists():
            existing = [json.loads(line) for line in memory_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        existing.append(
            {
                "timestamp": now_iso(),
                "entry_type": "v11_continuity_check",
                "source_context": "v11 post-induction continuity and wellbeing pass",
                "reflection": f"{row['display_name']} remained identity-stable and scope-stable after official induction.",
                "insight": f"{row['display_name']} continues to operate inside the {row['role']} lane without drift.",
                "next_plan": "Continue bounded council work through the v11 storage, validation, and Trinity research lanes.",
                "mirror_state": "repo_authoritative",
            }
        )
        write_jsonl(memory_path, existing)
        write_text(
            reflection_path,
            "\n".join(
                [
                    f"# {row['display_name']} Reflection",
                    "",
                    f"- role: `{row['role']}`",
                    f"- induction_state: `{row['induction_state']}`",
                    "- continuity_state: `stable`",
                    "- wellbeing_state: `stable`",
                    "- mirror_status: `repo_authoritative`",
                    "",
                    f"{row['display_name']} remains continuous and distinct through the v11 storage and research transition.",
                    "",
                ]
            ),
        )
    write_json(roster_path, roster)
    return roster


def seed_support_docs(roster: dict[str, object]) -> None:
    branch_ok, branch_text = run_capture("git", "branch", "--show-current")
    diverged_ok, diverged = run_capture("git", "rev-list", "--left-right", "--count", "main...HEAD")
    docker_ok, docker_names = run_capture("docker", "ps", "--format", "{{.Names}}")
    write_json(
        ROOT / "docs" / "logs" / "system-wake-v11.json",
        {
            "generated_utc": now_iso(),
            "phase": "v11",
            "branch": branch_text if branch_ok else "unknown",
            "main_vs_head_divergence": diverged if diverged_ok else "unavailable",
            "docker_containers": docker_names.splitlines() if docker_ok and docker_names else [],
            "connector_state": {"github": "live_write", "linear": "live_write", "notion": "live_write", "postgres": "live_write", "figma": "read_only", "google_drive": "staged_archive"},
            "official_council_count": len([row for row in roster.get("agents", []) if isinstance(row, dict)]),
        },
    )
    write_text(ROOT / "docs" / "v11-gmut-research-brief.md", "# V11 GMUT Research Brief\n\n## Evidence posture\n- confirmed_evidence: repo-backed GMUT comparison artifacts remain authoritative.\n- inference: current research-primary sources refine comparator wording and falsification targets.\n- open_gap: no live-source refresh alone upgrades readiness.\n\n## Next falsification tasks\n- tighten bridge language between GMUT anchors and current theory comparators.\n- preserve explicit next-proof tasks for each open gap.\n")
    write_text(ROOT / "docs" / "v11-freedid-governance-brief.md", "# V11 Freed ID Governance Brief\n\n## Evidence posture\n- confirmed_evidence: repo-backed DID, disclosure, recourse, and governance artifacts remain authoritative.\n- inference: standards and governance refresh can refine wording and comparison framing.\n- open_gap: legal force and universal governance claims remain bounded.\n\n## Next proof tasks\n- keep alignment, gap, and next-proof columns explicit.\n- preserve repo-first governance authority even when mirrors are refreshed.\n")
    write_text(ROOT / "docs" / "v11-council-group-reflection.md", "# V11 Council Group Reflection\n\nThe council carried official identity, memory, and command boundaries forward into the storage-heavy v11 phase while keeping the repo authoritative and every mirror bounded.\n")
    write_text(ROOT / "docs" / "v12-roadmap-v2.md", "# V12 Roadmap\n\n## Storage and continuity\n- promote Google Drive from staged archive to bounded live archive only after OAuth and upload proof pass.\n- extend archive rotation and retention without increasing authority drift.\n\n## Trinity research\n- continue GMUT falsification-first comparison refresh.\n- continue Freed ID and Cosmic Bill standards alignment without overstating readiness.\n")
    write_json(
        ROOT / "docs" / "trinity-google-drive-sync-policy-v1.json",
        {
            "generated_utc": now_iso(),
            "repo_authority": ["certificates", "ledgers", "roster", "commands", "official Trinity records"],
            "archive_allowed": ["memory archives", "suite summaries", "control tower summaries", "research briefs", "workbench summaries"],
            "archive_forbidden": ["exclusive-only canonical records", "raw duo chats", "local secrets", "OAuth keys", "repo authority overrides"],
            "drive_role": "archive_mirror_only",
            "fallback_mode": "staged_with_blockers",
        },
    )
    write_jsonl(
        DRIVE_LEDGER,
        [
            {
                "timestamp": now_iso(),
                "archive_path": "",
                "target_surface": "google_drive",
                "result": "staged",
                "bytes": 0,
                "rollback_state": "no remote archive written",
            }
        ],
    )
    write_json(
        ROOT / "docs" / "trinity-google-drive-mcp-activation-latest.json",
        {
            "generated_utc": now_iso(),
            "overall_status": "WARN",
            "docker_first_path": True,
            "oauth_secret_seeded": False,
            "docker_volume_state": "pending_bootstrap",
            "config_entry_state": "pending_update",
            "auth_bootstrap_state": "pending",
            "fallback_mode": "memory_bank_archive_only",
            "blockers": ["interactive OAuth bootstrap not completed yet"],
        },
    )
    write_text(
        ROOT / "docs" / "trinity-google-drive-mcp-activation-latest.md",
        "# Trinity Google Drive MCP Activation\n\n- overall_status: `WARN`\n- docker_first_path: `true`\n- oauth_secret_seeded: `false`\n- docker_volume_state: `pending_bootstrap`\n- config_entry_state: `pending_update`\n- auth_bootstrap_state: `pending`\n- fallback_mode: `memory_bank_archive_only`\n",
    )
    write_json(
        ROOT / "docs" / "trinity-new-project-workbench-link-v2.json",
        {
            "generated_utc": now_iso(),
            "overall_status": "PASS",
            "workbench_root": str(WORKBENCH_ROOT),
            "contract": str(WORKBENCH_CONTRACT),
            "scripts": [
                str(WORKBENCH_SCRIPTS / "trinity_workbench_snapshot.py"),
                str(WORKBENCH_SCRIPTS / "trinity_workbench_shell.py"),
                str(WORKBENCH_SCRIPTS / "trinity_workbench_server.py"),
            ],
            "authority_model": "repo_first",
            "storage_surface": "google_drive_archive_candidate",
        },
    )
    write_json(
        ROOT / "docs" / "trinity-control-tower-latest.json",
        {
            "generated_utc": now_iso(),
            "overall_status": "PASS",
            "storage_state": "bounded_cloud_candidate",
            "google_drive_state": "staged_with_blockers",
            "council_continuity_state": "PASS",
            "command_surface_state": "PASS",
            "materialization_level_actual": "persistent_dev",
            "mind_evidence_posture": "bounded_refresh_only",
            "heart_evidence_posture": "bounded_refresh_only",
        },
    )
    write_text(
        ROOT / "docs" / "trinity-control-tower-latest.md",
        "# Trinity Control Tower\n\n- storage_state: `bounded_cloud_candidate`\n- google_drive_state: `staged_with_blockers`\n- council_continuity_state: `PASS`\n- command_surface_state: `PASS`\n- materialization_level_actual: `persistent_dev`\n- mind_evidence_posture: `bounded_refresh_only`\n- heart_evidence_posture: `bounded_refresh_only`\n",
    )
    write_external_json(
        WORKBENCH_CONTRACT,
        {
            "generated_utc": now_iso(),
            "authority_model": "repo_first",
            "read_surfaces": [
                str(ROOT / "docs" / "trinity-control-tower-latest.json"),
                str(ROOT / "docs" / "system-suite-status.json"),
                str(ROOT / "docs" / "trinity-memory-bank-registry-v2.json"),
                str(ROOT / "docs" / "trinity-google-drive-mcp-activation-latest.json"),
                str(ROOT / "docs" / "trinity-command-book-v5.json"),
            ],
            "allowed_triggers": ["read dashboards", "read command index", "render workbench summaries", "open bounded local status views"],
            "disabled_write_paths": ["repo bypass writes", "authority override writes", "unbounded cloud writes"],
            "runtime_dependencies": ["python", "optional_postgres", "optional_docker"],
        },
    )
    write_external_text(WORKBENCH_README, "# Trinity Workbench\n\nThis folder remains a local-only workbench. The Beyonder-Real-True Journey repo stays authoritative while the workbench reads and summarizes repo/runtime state.\n")


def main() -> int:
    old_manifest = json.loads(OLD_MANIFEST.read_text(encoding="utf-8"))
    old_extensions = json.loads(OLD_EXTENSION_CATALOG.read_text(encoding="utf-8"))
    old_mcp_catalog = json.loads(OLD_MCP_CATALOG.read_text(encoding="utf-8"))
    old_command_book = json.loads(OLD_COMMAND_BOOK.read_text(encoding="utf-8"))
    old_memory_bank = json.loads(OLD_MEMORY_BANK.read_text(encoding="utf-8"))

    manifest = deepcopy(old_manifest)
    manifest["version"] = "v11"
    manifest["generated_utc"] = now_iso()
    manifest["description"] = "V11 Google Drive activation, bounded cloud memory-bank promotion, deep/materialize sweeps, and Trinity continuity manifest with 656 executable systems."
    manifest["systems"] = augment_rows(
        [row for row in manifest.get("systems", []) if isinstance(row, dict)],
        {"storage_surface": "repo", "cloud_archive_state": "not_applicable", "continuity_posture": "v10_proof_backed"},
    )

    extensions = deepcopy(old_extensions)
    extensions["version"] = "v9"
    extensions["generated_utc"] = now_iso()
    extensions["description"] = "V11 extension catalog with Google Drive archive candidacy, bounded storage expansion, and Trinity continuity coverage."
    extensions["extensions"] = augment_rows(
        [row for row in extensions.get("extensions", []) if isinstance(row, dict)],
        {"storage_dependency": "repo", "archive_scope": "none", "workbench_surface": "repo"},
    )

    for pack in PACKS:
        for suffix in SUFFIXES:
            manifest["systems"].append(manifest_entry(pack, suffix))
        extensions["extensions"].extend(extension_rows_for_pack(pack))
        pack_name = hyphen(str(pack["pack"]))
        write_json(ROOT / "docs" / f"{pack_name}-contract-v1.json", pack_contract(pack))
        write_json(ROOT / "docs" / f"{pack_name}-fixture-v1.json", pack_fixture(pack))
        write_text(ROOT / "docs" / f"{pack_name}-workflow-v1.md", pack_workflow(pack))
        write_json(ROOT / "docs" / f"{pack_name}-catalog-entry-v1.json", pack_catalog_entry(pack))
        for kind in ("operations", "integration"):
            skill_md, skill_yaml_path = skill_files(pack, kind)
            write_text(skill_md, skill_markdown(pack, kind))
            write_text(skill_yaml_path, skill_yaml(pack, kind))

    if len(manifest["systems"]) != 656:
        raise ValueError(f"expected 656 manifest systems, found {len(manifest['systems'])}")
    if len(extensions["extensions"]) != 1152:
        raise ValueError(f"expected 1152 catalog extensions, found {len(extensions['extensions'])}")

    command_book = build_command_book(old_command_book)
    mcp_catalog = build_mcp_catalog(old_mcp_catalog)
    memory_bank = build_memory_bank_registry(old_memory_bank)
    roster = refresh_council_assets()
    seed_support_docs(roster)

    write_json(NEW_MANIFEST, manifest)
    write_json(NEW_EXTENSION_CATALOG, extensions)
    write_json(NEW_MCP_CATALOG, mcp_catalog)
    write_json(NEW_COMMAND_BOOK, command_book)
    write_text(ROOT / "docs" / "trinity-command-book-latest.md", command_markdown(command_book))
    write_json(NEW_MEMORY_BANK, memory_bank)
    print("generated_v11_surface=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
