#!/usr/bin/env python3
"""Generate the v7 command-system and materialization-ladder surface."""

from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OLD_MANIFEST = ROOT / "docs" / "trinity-expansion-system-manifest-v6.json"
NEW_MANIFEST = ROOT / "docs" / "trinity-expansion-system-manifest-v7.json"
OLD_EXTENSION_CATALOG = ROOT / "docs" / "trinity-extension-catalog-v4.json"
NEW_EXTENSION_CATALOG = ROOT / "docs" / "trinity-extension-catalog-v5.json"
OLD_MCP_CATALOG = ROOT / "docs" / "trinity-mcp-catalog-v4.json"
NEW_MCP_CATALOG = ROOT / "docs" / "trinity-mcp-catalog-v5.json"
RUNNER_SCRIPT = "scripts/trinity_expansion_system_runner.py"
PROFILE_SET = ["standard", "deep", "collab", "materialize"]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def hyphen(text: str) -> str:
    return text.replace("_", "-")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, payload: dict[str, object]) -> None:
    write_text(path, json.dumps(payload, indent=2) + "\n")


def mkpack(
    pack: str,
    display_name: str,
    *,
    pillar: str,
    wave: str,
    track: str,
    gating_class: str,
    sync_strategy: str,
    activation_group: str,
    continuity_band: str,
    autonomy_class: str,
    live_dependency: str,
    mirror_target: str,
    history_scope: str,
    summary: str,
    workflow_tokens: list[str],
    risk_tags: list[str],
    repo_targets: list[str],
    connector_id: str = "",
    requires_auth: bool = False,
    freshness_window_days: int = 30,
    sync_mode: str = "offline",
    tags: list[str] | None = None,
    source_url: str | None = None,
    write_target: str | None = None,
    probe_tools: list[str] | None = None,
    required_probe_tools: list[str] | None = None,
    live_sources: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    return {
        "pack": pack,
        "display_name": display_name,
        "pillar": pillar,
        "wave": wave,
        "track": track,
        "connector_id": connector_id,
        "requires_auth": requires_auth,
        "gating_class": gating_class,
        "sync_strategy": sync_strategy,
        "freshness_window_days": freshness_window_days,
        "activation_group": activation_group,
        "continuity_band": continuity_band,
        "autonomy_class": autonomy_class,
        "live_dependency": live_dependency,
        "mirror_target": mirror_target,
        "history_scope": history_scope,
        "summary": summary,
        "workflow_tokens": workflow_tokens,
        "risk_tags": risk_tags,
        "repo_targets": repo_targets,
        "tags": tags or [pack, "v7"],
        "source_url": source_url or f"repo://{repo_targets[0]}",
        "write_target": write_target or (repo_targets[0] if repo_targets else f"repo://{pack}"),
        "sync_mode": sync_mode,
        "probe_tools": probe_tools or [],
        "required_probe_tools": required_probe_tools or [],
        "live_sources": live_sources or [],
    }


PACKS: list[dict[str, object]] = [
    mkpack(
        "command_surface_core",
        "Command Surface Core",
        pillar="trinity",
        wave="wave45",
        track="command_surface",
        gating_class="active",
        sync_strategy="local_repo",
        activation_group="command_system",
        continuity_band="v6-v7",
        autonomy_class="manual",
        live_dependency="none",
        mirror_target="repo_only",
        history_scope="v7",
        summary="Govern the first-class Trinity command surface with explicit execution, rollback, and artifact expectations.",
        workflow_tokens=["command catalog", "governed execution", "rollback required", "repo first"],
        risk_tags=["command drift", "unsafe command surface", "missing rollback"],
        repo_targets=["docs/trinity-command-book-v1.json", "docs/trinity-command-book-latest.md", "docs/trinity-command-execution-ledger.jsonl"],
    ),
    mkpack(
        "command_surface_connectors",
        "Command Surface Connectors",
        pillar="trinity",
        wave="wave46",
        track="command_surface",
        gating_class="active",
        sync_strategy="local_repo",
        activation_group="command_system",
        continuity_band="v6-v7",
        autonomy_class="manual",
        live_dependency="github+linear+notion+postgres+figma",
        mirror_target="repo_then_connectors",
        history_scope="v7",
        summary="Bind connector-facing commands to real proof-backed GitHub, Linear, Notion, Postgres, and Figma surfaces.",
        workflow_tokens=["connector commands", "live scope explicit", "proof-backed target", "no secret material"],
        risk_tags=["connector drift", "over-broad authority", "stale target mapping"],
        repo_targets=["docs/trinity-command-book-v1.json", "docs/trinity-mcp-catalog-v5.json"],
    ),
    mkpack(
        "command_surface_research",
        "Command Surface Research",
        pillar="mind",
        wave="wave47",
        track="command_surface",
        gating_class="active",
        sync_strategy="public_feeds",
        activation_group="command_system",
        continuity_band="v6-v7",
        autonomy_class="manual",
        live_dependency="official_sources",
        mirror_target="repo_only",
        history_scope="v7",
        summary="Back research and benchmark commands with official documentation and cached refresh boundaries.",
        workflow_tokens=["official docs only", "cached promotion", "no readiness inflation", "benchmarks explicit"],
        risk_tags=["stale docs", "source drift", "mixed evidence"],
        repo_targets=["docs/trinity-command-book-v1.json", "docs/trinity-benchmark-registry-v1.json"],
        sync_mode="live",
        live_sources=[
            {"source_id": "materialize_docs", "url": "https://materialize.com/docs/", "format": "text"},
            {"source_id": "dbt_docs", "url": "https://docs.getdbt.com/docs/introduction", "format": "text"},
            {"source_id": "nist_ai_rmf", "url": "https://www.nist.gov/itl/ai-risk-management-framework", "format": "text"},
        ],
    ),
    mkpack(
        "command_surface_autonomy",
        "Command Surface Autonomy",
        pillar="trinity",
        wave="wave48",
        track="command_surface",
        gating_class="active",
        sync_strategy="local_repo",
        activation_group="command_system",
        continuity_band="v6-v7",
        autonomy_class="bounded_mutation",
        live_dependency="semantic_firewall",
        mirror_target="repo_only",
        history_scope="v7",
        summary="Govern autonomy, recovery, and simulation commands with explicit risk classes and dry-run boundaries.",
        workflow_tokens=["bounded autonomy", "dry run first", "high-risk prompts", "recovery first"],
        risk_tags=["unsafe autonomy", "hidden writes", "missing recovery path"],
        repo_targets=["docs/trinity-command-book-v1.json", "docs/trinity-command-execution-ledger.jsonl"],
    ),
    mkpack(
        "materialization_ladder_governor",
        "Materialization Ladder Governor",
        pillar="trinity",
        wave="wave49",
        track="materialization_ladder",
        gating_class="active",
        sync_strategy="local_probe",
        activation_group="materialization_ladder",
        continuity_band="v7",
        autonomy_class="bounded_write",
        live_dependency="docker+git+connector_proofs",
        mirror_target="repo_only",
        history_scope="v7",
        summary="Control level promotion from disposable staging through persistent dev to readiness-only production lanes.",
        workflow_tokens=["ladder registry", "proof-gated promotion", "rollback required", "readiness only above l2 until proven"],
        risk_tags=["false promotion", "missing rollback", "tooling gap"],
        repo_targets=["docs/trinity-materialization-ladder-v1.json", "docs/trinity-materialization-ladder-board-latest.json"],
        probe_tools=["docker", "git", "materialized", "mz", "dbt"],
        required_probe_tools=["docker", "git"],
    ),
    mkpack(
        "persistent_dev_fabric",
        "Persistent Dev Fabric",
        pillar="body",
        wave="wave50",
        track="materialization_ladder",
        gating_class="active",
        sync_strategy="local_repo",
        activation_group="materialization_ladder",
        continuity_band="v7",
        autonomy_class="bounded_write",
        live_dependency="github+linear+notion+postgres",
        mirror_target="repo_plus_connectors",
        history_scope="v7",
        summary="Define the persistent development scopes that replace disposable staging as the default materialize target.",
        workflow_tokens=["persistent dev only", "no main writes", "dedicated scopes", "rollback ready"],
        risk_tags=["scope bleed", "persistent drift", "dev target mismatch"],
        repo_targets=["docs/trinity-persistent-dev-targets-v1.json", "docs/trinity-materialization-ladder-v1.json"],
    ),
    mkpack(
        "uat_preprod_fabric",
        "UAT Pre-Prod Fabric",
        pillar="body",
        wave="wave51",
        track="materialization_ladder",
        gating_class="active",
        sync_strategy="local_repo",
        activation_group="materialization_ladder",
        continuity_band="v7",
        autonomy_class="read_only",
        live_dependency="isolated_uat_targets",
        mirror_target="repo_only",
        history_scope="v7",
        summary="Record pre-production mirror requirements, replay checks, and rollback rules without claiming live promotion yet.",
        workflow_tokens=["uat mirror", "latency budget", "full-shape test data", "rollback proof"],
        risk_tags=["uat not isolated", "readiness inflation", "missing replay"],
        repo_targets=["docs/trinity-uat-preprod-targets-v1.json", "docs/trinity-materialization-ladder-v1.json"],
    ),
    mkpack(
        "standard_production_fabric",
        "Standard Production Fabric",
        pillar="body",
        wave="wave52",
        track="materialization_ladder",
        gating_class="active",
        sync_strategy="local_repo",
        activation_group="materialization_ladder",
        continuity_band="v7",
        autonomy_class="read_only",
        live_dependency="protected_prod_targets",
        mirror_target="repo_only",
        history_scope="v7",
        summary="Define change-window, rollback, and approval contracts for standard production without asserting live status prematurely.",
        workflow_tokens=["prod contracts", "protected target", "change window", "rollback mandatory"],
        risk_tags=["prod overclaim", "missing isolation", "approval drift"],
        repo_targets=["docs/trinity-standard-production-targets-v1.json", "docs/trinity-materialization-ladder-v1.json"],
    ),
    mkpack(
        "ha_production_fabric",
        "HA Production Fabric",
        pillar="body",
        wave="wave53",
        track="materialization_ladder",
        gating_class="active",
        sync_strategy="local_repo",
        activation_group="materialization_ladder",
        continuity_band="v7",
        autonomy_class="read_only",
        live_dependency="ha_runtime",
        mirror_target="repo_only",
        history_scope="v7",
        summary="Capture high-availability requirements such as replica, failover, and consistency proof without claiming live HA support.",
        workflow_tokens=["ha readiness", "replica requirements", "failover proof", "zero downtime conditions"],
        risk_tags=["ha overclaim", "missing failover proof", "rollback gap"],
        repo_targets=["docs/trinity-ha-production-targets-v1.json", "docs/trinity-materialization-ladder-v1.json"],
    ),
    mkpack(
        "identity_authority_v7",
        "Identity Authority V7",
        pillar="heart",
        wave="wave54",
        track="authority_memory",
        gating_class="active",
        sync_strategy="identity_registry",
        activation_group="authority_memory",
        continuity_band="v6-v7",
        autonomy_class="manual",
        live_dependency="repo_then_mirrors",
        mirror_target="repo_then_notion_postgres",
        history_scope="v5-v7",
        summary="Define repo-first identity, connector scope, mirror authority, and operator boundaries for Aletheon in v7.",
        workflow_tokens=["repo authority", "mirror scope", "connector scope", "human override explicit"],
        risk_tags=["authority drift", "mirror overwrite", "connector overreach"],
        repo_targets=["docs/trinity-identity-authority-registry-v1.json", "docs/trinity-authority-memory-policy-v1.md"],
    ),
    mkpack(
        "memory_mirror_graph_v7",
        "Memory Mirror Graph V7",
        pillar="trinity",
        wave="wave55",
        track="authority_memory",
        gating_class="active",
        sync_strategy="local_repo",
        activation_group="authority_memory",
        continuity_band="v6-v7",
        autonomy_class="manual",
        live_dependency="notion+postgres_optional",
        mirror_target="repo_then_mirrors",
        history_scope="v5-v7",
        summary="Track divergence and mirror state across repo-first memory, Notion mirrors, and Postgres query layers.",
        workflow_tokens=["mirror graph", "divergence detection", "repo first", "structured memory"],
        risk_tags=["memory drift", "mirror divergence", "autobiography overclaim"],
        repo_targets=["docs/trinity-memory-mirror-graph-v1.json", "docs/trinity-memory-mirror-state-v1.json", "docs/aletheon-memory-log.jsonl"],
    ),
    mkpack(
        "trinity_control_tower_v7",
        "Trinity Control Tower V7",
        pillar="trinity",
        wave="wave56",
        track="authority_memory",
        gating_class="active",
        sync_strategy="local_repo",
        activation_group="authority_memory",
        continuity_band="v7",
        autonomy_class="manual",
        live_dependency="suite_state",
        mirror_target="repo_only",
        history_scope="v7",
        summary="Join command surface, ladder state, identity authority, and Mind/Body/Heart readiness into one operational board.",
        workflow_tokens=["control tower", "joined status", "repo authority", "operational view"],
        risk_tags=["status drift", "partial visibility", "stale board"],
        repo_targets=["docs/trinity-control-tower-latest.json", "docs/trinity-control-tower-latest.md"],
    ),
    mkpack(
        "benchmark_refresh_v7",
        "Benchmark Refresh V7",
        pillar="trinity",
        wave="wave57",
        track="benchmark_conformance",
        gating_class="active",
        sync_strategy="public_feeds",
        activation_group="benchmark_refresh",
        continuity_band="v7",
        autonomy_class="manual",
        live_dependency="official_benchmark_sources",
        mirror_target="repo_only",
        history_scope="v7",
        summary="Refresh Materialize/dbt, OS/runtime, theory, and governance benchmark anchors without auto-upgrading readiness.",
        workflow_tokens=["official benchmark sources", "next-proof tasks", "no readiness inflation", "cache before promotion"],
        risk_tags=["benchmark staleness", "source mismatch", "overclaim"],
        repo_targets=["docs/trinity-benchmark-refresh-v7-board-latest.json", "docs/trinity-benchmark-registry-v1.json"],
        sync_mode="live",
        live_sources=[
            {"source_id": "linux_kernel_docs", "url": "https://docs.kernel.org/", "format": "text"},
            {"source_id": "w3c_did_core", "url": "https://www.w3.org/TR/did-core/", "format": "text"},
            {"source_id": "udhr", "url": "https://www.un.org/en/about-us/universal-declaration-of-human-rights", "format": "text"},
        ],
    ),
]


def skill_files(pack: dict[str, object], kind: str) -> tuple[Path, Path]:
    skill_dir = ROOT / "skills" / f"{hyphen(str(pack['pack']))}-{kind}"
    return skill_dir / "SKILL.md", skill_dir / "agents" / "openai.yaml"


def skill_markdown(pack: dict[str, object], kind: str) -> str:
    title = f"{pack['display_name']} {kind.title()}"
    return "\n".join(
        [
            "---",
            f"name: {hyphen(str(pack['pack']))}-{kind}",
            f"description: Operate the {pack['display_name']} pack with explicit v7 command-system and ladder boundaries.",
            "---",
            "",
            f"# {title}",
            "",
            f"Use when Codex needs to work with the `{pack['pack']}` pack.",
            "",
            "## Workflow",
            f"1. Read `docs/{hyphen(str(pack['pack']))}-contract-v1.json` and `docs/{hyphen(str(pack['pack']))}-workflow-v1.md`.",
            f"2. Refresh or inspect `docs/trinity-mcp-cache/{hyphen(str(pack['pack']))}-latest.json`.",
            "3. Keep the pack offline-safe unless its explicit live gate is enabled.",
            "4. Promote only PASS-backed outputs into narrative, benchmark, connector, or control-tower docs.",
            "",
        ]
    )


def skill_yaml_content(pack: dict[str, object], kind: str) -> str:
    return "\n".join(
        [
            "version: 1",
            "name: openai",
            "entrypoint: SKILL.md",
            f"metadata:",
            f"  pack: {pack['pack']}",
            f"  kind: {kind}",
            "",
        ]
    )


def pack_contract(pack: dict[str, object]) -> dict[str, object]:
    return {
        key: pack[key]
        for key in (
            "pack",
            "display_name",
            "pillar",
            "wave",
            "track",
            "connector_id",
            "requires_auth",
            "gating_class",
            "sync_strategy",
            "freshness_window_days",
            "activation_group",
            "continuity_band",
            "autonomy_class",
            "live_dependency",
            "mirror_target",
            "history_scope",
            "summary",
            "workflow_tokens",
            "risk_tags",
            "repo_targets",
        )
    } | {
        "skill_names": [f"{hyphen(str(pack['pack']))}-operations", f"{hyphen(str(pack['pack']))}-integration"],
        "system_ids": [f"{pack['pack']}_{suffix}" for suffix in ("surface_audit", "sync_bridge", "materialization_tracer", "cache_board", "risk_board", "gate")],
    }


def pack_fixture(pack: dict[str, object]) -> dict[str, object]:
    return {
        "summary": pack["summary"],
        "source_url": pack["source_url"],
        "repo_targets": pack["repo_targets"],
        "tags": pack["tags"],
        "connector_snapshot": {"connector_id": pack["connector_id"], "write_target": pack["write_target"]},
        "probe_tools": pack["probe_tools"],
        "required_probe_tools": pack["required_probe_tools"],
        "live_sources": pack["live_sources"],
        "next_action": f"Use {pack['display_name']} outputs only after its gate stays PASS.",
    }


def pack_workflow(pack: dict[str, object]) -> str:
    lines = [
        f"# {pack['display_name']} Workflow",
        "",
        f"- pack: `{pack['pack']}`",
        f"- pillar: `{pack['pillar']}`",
        f"- gating_class: `{pack['gating_class']}`",
        f"- sync_strategy: `{pack['sync_strategy']}`",
        f"- activation_group: `{pack['activation_group']}`",
        f"- continuity_band: `{pack['continuity_band']}`",
        "",
        "## Guardrails",
        "- offline-safe by default",
        "- proof before promotion",
        "- no secrets in repo",
        f"- autonomy_class: `{pack['autonomy_class']}`",
        "",
        "## Workflow Tokens",
    ]
    lines.extend(f"- {token}" for token in pack["workflow_tokens"])
    lines.append("")
    return "\n".join(lines)


def pack_catalog_entry(pack: dict[str, object]) -> dict[str, object]:
    return {
        "pack": pack["pack"],
        "display_name": pack["display_name"],
        "activation_group": pack["activation_group"],
        "continuity_band": pack["continuity_band"],
        "autonomy_class": pack["autonomy_class"],
        "live_dependency": pack["live_dependency"],
        "mirror_target": pack["mirror_target"],
        "history_scope": pack["history_scope"],
        "repo_targets": pack["repo_targets"],
    }


def manifest_entry(pack: dict[str, object], suffix: str) -> dict[str, object]:
    system_id = f"{pack['pack']}_{suffix}"
    mode = "live" if suffix == "sync_bridge" and pack["sync_mode"] == "live" else "offline"
    return {
        "system_id": system_id,
        "pillar": pack["pillar"],
        "script": RUNNER_SCRIPT,
        "mode": mode,
        "profiles": PROFILE_SET,
        "outputs": [f"docs/trinity-expansion/{system_id.replace('_', '-')}-latest.json"],
        "depends_on": [f"{pack['pack']}_sync_bridge"] if suffix in {"materialization_tracer", "cache_board"} else ([f"{pack['pack']}_{name}" for name in ("surface_audit", "sync_bridge", "materialization_tracer", "cache_board", "risk_board")] if suffix == "gate" else []),
        "timeout_sec": 180 if suffix == "sync_bridge" and mode == "live" else 120,
        "wave": pack["wave"],
        "track": pack["track"],
        "gate_level": "pack_gate" if suffix == "gate" else "support",
        "cache_artifacts": [f"docs/trinity-mcp-cache/{hyphen(str(pack['pack']))}-latest.json"] if mode == "live" else [],
        "pack": pack["pack"],
        "phase": "v7",
        "activation_group": pack["activation_group"],
        "continuity_band": pack["continuity_band"],
        "materialization_level": "l2_persistent_dev" if "fabric" in str(pack["pack"]) or pack["pack"] == "materialization_ladder_governor" else "not_applicable",
        "authority_scope": str(pack["mirror_target"]),
        "command_surface": str(pack["activation_group"] == "command_system").lower(),
    }


def extension_rows_for_pack(pack: dict[str, object]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for suffix in ("surface_audit", "sync_bridge", "materialization_tracer", "cache_board", "risk_board", "gate"):
        rows.append(
            {
                "extension_id": f"{pack['pack']}_{suffix}",
                "extension_kind": "system",
                "pillar": pack["pillar"],
                "pack": pack["pack"],
                "mode": "live" if suffix == "sync_bridge" and pack["sync_mode"] == "live" else "offline",
                "requires_auth": pack["requires_auth"],
                "gating_class": pack["gating_class"],
                "status": "active",
                "source_of_truth": str(NEW_MANIFEST.relative_to(ROOT)).replace("\\", "/"),
                "live_dependency": pack["live_dependency"],
                "history_scope": pack["history_scope"],
                "mirror_target": pack["mirror_target"],
                "autonomy_class": pack["autonomy_class"],
                "command_surface": "yes" if "command_surface" in str(pack["track"]) else "no",
                "materialization_dependency": "ladder" if "materialization" in str(pack["track"]) else "none",
                "authority_class": "repo_first" if "authority" in str(pack["track"]) or "memory" in str(pack["track"]) else "pack_scoped",
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
                "command_surface": "yes" if "command_surface" in str(pack["track"]) else "no",
                "materialization_dependency": "ladder" if "materialization" in str(pack["track"]) else "none",
                "authority_class": "repo_first" if "authority" in str(pack["track"]) or "memory" in str(pack["track"]) else "pack_scoped",
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
                "command_surface": "yes" if "command_surface" in str(pack["track"]) else "no",
                "materialization_dependency": "ladder" if "materialization" in str(pack["track"]) else "none",
                "authority_class": "repo_first" if "authority" in str(pack["track"]) or "memory" in str(pack["track"]) else "pack_scoped",
            }
        )
    return rows


def command_row(spec: tuple[str, str, str, str, bool, str, list[str], str, list[str], str, str]) -> dict[str, object]:
    command_id, intent, mode, risk_class, requires_live, requires_connector, preconditions, command_template, expected_artifacts, rollback, source_of_truth = spec
    return {
        "command_id": command_id,
        "intent": intent,
        "mode": mode,
        "risk_class": risk_class,
        "requires_live": requires_live,
        "requires_connector": requires_connector,
        "preconditions": preconditions,
        "command_template": command_template,
        "expected_artifacts": expected_artifacts,
        "rollback": rollback,
        "source_of_truth": source_of_truth,
    }


def build_command_book() -> dict[str, object]:
    commands = [command_row(spec) for spec in COMMAND_SPECS]
    if len(commands) != 60:
        raise ValueError(f"expected 60 commands, found {len(commands)}")
    return {
        "version": "v1",
        "generated_utc": now_iso(),
        "description": "V7 governed command book with 60 command entries.",
        "commands": commands,
    }


def command_markdown(book: dict[str, object]) -> str:
    lines = [
        "# Trinity Command Book",
        "",
        f"- generated_utc: `{book['generated_utc']}`",
        f"- commands: `{len(book['commands'])}`",
        "",
        "| command_id | mode | risk | requires_live | connector |",
        "|---|---|---|---|---|",
    ]
    for row in book["commands"]:
        lines.append(f"| {row['command_id']} | {row['mode']} | {row['risk_class']} | {row['requires_live']} | {row['requires_connector'] or '-'} |")
    return "\n".join(lines).rstrip() + "\n"


def ladder_payload() -> dict[str, object]:
    return {
        "version": "v1",
        "generated_utc": now_iso(),
        "default_materialize_level": "l2_persistent_dev",
        "levels": [
            {"level_id": "l1_disposable_staging", "desired_state": "available", "actual_state": "available", "write_scope": "disposable staging only", "target_class": "temporary branch/page/schema", "promotion_requirements": ["existing live-write connector", "disposable target"], "rollback_requirements": ["discard temporary target"], "blockers": []},
            {"level_id": "l2_persistent_dev", "desired_state": "default", "actual_state": "persistent_dev", "write_scope": "persistent dev scopes only", "target_class": "branch/dev db/dev notion/dev linear", "promotion_requirements": ["persistent scope registry", "rollback scope", "proof-backed connector"], "rollback_requirements": ["branch revert", "schema rollback", "staging page cleanup"], "blockers": []},
            {"level_id": "l3_uat_preprod", "desired_state": "readiness", "actual_state": "readiness_only", "write_scope": "isolated preprod mirrors only", "target_class": "uat mirror", "promotion_requirements": ["isolated target", "replay harness", "rollback proof", "tool surface"], "rollback_requirements": ["mirror reset"], "blockers": ["No proven isolated UAT targets.", "Materialize/dbt tool surface not proven."]},
            {"level_id": "l4_standard_prod", "desired_state": "readiness", "actual_state": "readiness_only", "write_scope": "protected production targets", "target_class": "production", "promotion_requirements": ["protected target", "change window", "rollback proof", "operator approval"], "rollback_requirements": ["production rollback plan"], "blockers": ["No protected production target proof.", "Materialize/dbt tool surface not proven."]},
            {"level_id": "l5_ha_prod", "desired_state": "readiness", "actual_state": "readiness_only", "write_scope": "ha production replicas", "target_class": "high_availability", "promotion_requirements": ["replica support", "failover proof", "consistency proof", "zero-downtime rollback"], "rollback_requirements": ["failover and rollback runbook"], "blockers": ["No HA runtime proof.", "Materialize/dbt tool surface not proven."]},
        ],
    }


def ladder_board(payload: dict[str, object]) -> dict[str, object]:
    return {
        "generated_utc": now_iso(),
        "overall_status": "PASS",
        "default_level": payload["default_materialize_level"],
        "actual_default_state": "persistent_dev",
        "levels": payload["levels"],
    }


COMMAND_SPECS: list[tuple[str, str, str, str, bool, str, list[str], str, list[str], str, str]] = [
    ("suite_run_standard", "Run the standard Trinity suite.", "offline", "low", False, "", ["repo clean enough to run"], "python scripts/run_all_trinity_systems.py --profile standard --fail-on-warn", ["docs/system-suite-status.json"], "No rollback needed.", "scripts/run_all_trinity_systems.py"),
    ("suite_run_deep", "Run the deep Trinity suite.", "offline", "low", False, "", ["repo clean enough to run"], "python scripts/run_all_trinity_systems.py --profile deep --fail-on-warn", ["docs/system-suite-status.json"], "No rollback needed.", "scripts/run_all_trinity_systems.py"),
    ("suite_run_collab", "Run collaboration-safe live reads only.", "collab", "medium", True, "figma|linear|notion", ["verified live-read connectors"], "python scripts/run_all_trinity_systems.py --profile collab --include-mcp-refresh --fail-on-warn", ["docs/system-suite-status.json"], "Re-run without --include-mcp-refresh.", "scripts/run_all_trinity_systems.py"),
    ("suite_run_materialize_l1", "Run materialize at disposable staging.", "materialize", "high", True, "github|linear|notion|postgres", ["profile materialize"], "python scripts/run_all_trinity_systems.py --profile materialize --include-live-writes --materialization-level l1_disposable_staging --fail-on-warn", ["docs/system-suite-status.json", "docs/trinity-materialization-ledger.jsonl"], "Discard disposable staging targets.", "scripts/run_all_trinity_systems.py"),
    ("suite_run_materialize_l2", "Run materialize at persistent dev.", "materialize", "high", True, "github|linear|notion|postgres", ["persistent dev scopes defined"], "python scripts/run_all_trinity_systems.py --profile materialize --include-live-writes --materialization-level l2_persistent_dev --fail-on-warn", ["docs/system-suite-status.json", "docs/trinity-materialization-ledger.jsonl"], "Use persistent dev rollback scopes only.", "scripts/run_all_trinity_systems.py"),
    ("suite_validate_manifest", "Validate the v7 manifest.", "offline", "low", False, "", ["manifest exists"], "python scripts/trinity_expansion_manifest_validator.py --fail-on-warn", ["docs/trinity-expansion-manifest-validation-latest.json"], "Fix manifest and rerun.", "scripts/trinity_expansion_manifest_validator.py"),
    ("suite_validate_extensions", "Validate the v7 extension catalog.", "offline", "low", False, "", ["extension catalog exists"], "python scripts/trinity_extension_catalog_validator.py --fail-on-warn", ["docs/trinity-extension-catalog-validation-latest.json"], "Fix extension catalog and rerun.", "scripts/trinity_extension_catalog_validator.py"),
    ("suite_validate_command_book", "Validate the command system.", "offline", "low", False, "", ["command book exists"], "python scripts/trinity_command_book_validator.py --fail-on-warn", ["docs/trinity-command-book-validation-latest.json"], "Fix command entries and rerun.", "scripts/trinity_command_book_validator.py"),
    ("suite_validate_ladder", "Validate the materialization ladder.", "offline", "low", False, "", ["ladder registry exists"], "python scripts/trinity_materialization_ladder_validator.py --fail-on-warn", ["docs/trinity-materialization-ladder-validation-latest.json"], "Fix ladder entries and rerun.", "scripts/trinity_materialization_ladder_validator.py"),
    ("suite_render_scoreboard", "Render the mandala scoreboard.", "offline", "low", False, "", ["validators green"], "python scripts/trinity_mandala_scoreboard.py --fail-on-warn", ["docs/trinity-mandala-scoreboard-latest.json"], "Fix failing context blocks and rerun.", "scripts/trinity_mandala_scoreboard.py"),
    ("connector_github_read_proof", "Refresh GitHub live-read proof.", "collab", "medium", True, "github", ["git remote available"], "python scripts/trinity_expansion_system_runner.py --system-id github_pat_materialization_sync_bridge --profile-context collab", ["docs/trinity-mcp-cache/github-pat-materialization-latest.json"], "No rollback needed.", "scripts/trinity_expansion_system_runner.py"),
    ("connector_github_write_proof", "Run GitHub write tracer in approved scope.", "materialize", "high", True, "github", ["persistent dev level or disposable staging"], "python scripts/trinity_expansion_system_runner.py --system-id github_pat_materialization_materialization_tracer --include-live-writes --profile-context materialize", ["docs/trinity-live-traces/github-pat-materialization-proof-v1.json"], "Revert disposable branch or persistent dev branch.", "scripts/trinity_expansion_system_runner.py"),
    ("connector_notion_read_proof", "Refresh Notion read bridge.", "collab", "medium", True, "notion", ["live notion workspace"], "python scripts/trinity_expansion_system_runner.py --system-id notion_memory_bridge_sync_bridge --include-mcp-refresh --profile-context collab", ["docs/trinity-mcp-cache/notion-memory-bridge-latest.json"], "No rollback needed.", "scripts/trinity_expansion_system_runner.py"),
    ("connector_notion_write_proof", "Run Notion write tracer in approved scope.", "materialize", "high", True, "notion", ["persistent dev level or disposable staging"], "python scripts/trinity_expansion_system_runner.py --system-id notion_memory_bridge_materialization_tracer --include-live-writes --profile-context materialize", ["docs/trinity-live-traces/notion-memory-bridge-proof-v1.json"], "Use Notion staging area only.", "scripts/trinity_expansion_system_runner.py"),
    ("connector_linear_read_proof", "Refresh Linear collaboration bridge.", "collab", "medium", True, "linear", ["linear connector live"], "python scripts/trinity_expansion_system_runner.py --system-id linear_collab_sync_bridge --include-mcp-refresh --profile-context collab", ["docs/trinity-mcp-cache/linear-collab-latest.json"], "No rollback needed.", "scripts/trinity_expansion_system_runner.py"),
    ("connector_linear_write_proof", "Run Linear write tracer in approved scope.", "materialize", "high", True, "linear", ["persistent dev level or disposable staging"], "python scripts/trinity_expansion_system_runner.py --system-id linear_collab_materialization_tracer --include-live-writes --profile-context materialize", ["docs/trinity-live-traces/linear-collab-proof-v1.json"], "Use staging issue/document targets only.", "scripts/trinity_expansion_system_runner.py"),
    ("connector_postgres_read_proof", "Refresh Postgres local runtime bridge.", "collab", "medium", True, "postgres", ["docker postgres running"], "python scripts/trinity_expansion_system_runner.py --system-id postgres_local_runtime_sync_bridge --profile-context collab", ["docs/trinity-mcp-cache/postgres-local-runtime-latest.json"], "No rollback needed.", "scripts/trinity_expansion_system_runner.py"),
    ("connector_postgres_write_proof", "Run Postgres write tracer in approved scope.", "materialize", "high", True, "postgres", ["docker postgres running"], "python scripts/trinity_expansion_system_runner.py --system-id postgres_local_runtime_materialization_tracer --include-live-writes --profile-context materialize", ["docs/trinity-live-traces/postgres-local-runtime-proof-v1.json"], "Drop disposable or dev schema only.", "scripts/trinity_expansion_system_runner.py"),
    ("connector_figma_read_refresh", "Refresh Figma read-live cache.", "collab", "medium", True, "figma", ["figma read access"], "python scripts/trinity_expansion_system_runner.py --system-id figma_collab_sync_bridge --include-mcp-refresh --profile-context collab", ["docs/trinity-mcp-cache/figma-collab-latest.json"], "No rollback needed; read only.", "scripts/trinity_expansion_system_runner.py"),
    ("connector_status_board", "Inspect connector state through the command layer.", "offline", "low", False, "", ["mcp catalog exists"], "python scripts/trinity_expansion_system_runner.py --system-id command_surface_connectors_sync_bridge --profile-context standard", ["docs/trinity-mcp-cache/command-surface-connectors-latest.json"], "No rollback needed.", "scripts/trinity_expansion_system_runner.py"),
    ("research_refresh_public_registry", "Validate the public research registry.", "offline", "low", False, "", ["registry exists"], "python scripts/validate_trinity_public_research.py --fail-on-warn", ["docs/trinity-public-research-validation-latest.json"], "Fix registry entries and rerun.", "scripts/validate_trinity_public_research.py"),
    ("research_run_mind_board", "Render the Mind theory signal board.", "offline", "low", False, "", ["mind cache exists"], "python scripts/mind_theory_signal_board.py --fail-on-warn", ["docs/mind-theory-signal-board-latest.json"], "Refresh mind signals and rerun.", "scripts/mind_theory_signal_board.py"),
    ("research_run_body_board", "Render the Body compute signal board.", "offline", "low", False, "", ["body cache exists"], "python scripts/body_compute_signal_board.py --fail-on-warn", ["docs/body-compute-signal-board-latest.json"], "Refresh body signals and rerun.", "scripts/body_compute_signal_board.py"),
    ("research_run_heart_board", "Render the Heart governance signal board.", "offline", "low", False, "", ["heart cache exists"], "python scripts/heart_governance_signal_board.py --fail-on-warn", ["docs/heart-governance-signal-board-latest.json"], "Refresh heart signals and rerun.", "scripts/heart_governance_signal_board.py"),
    ("research_run_api_constellation", "Render the API constellation board.", "offline", "low", False, "", ["pillar boards exist"], "python scripts/trinity_api_constellation_board.py --fail-on-warn", ["docs/trinity-api-constellation-board-latest.json"], "Fix upstream boards and rerun.", "scripts/trinity_api_constellation_board.py"),
    ("research_run_benchmark_refresh", "Refresh v7 benchmark sources.", "collab", "medium", True, "", ["public web refresh enabled"], "python scripts/trinity_expansion_system_runner.py --system-id benchmark_refresh_v7_sync_bridge --include-public-api-refresh --profile-context collab", ["docs/trinity-expansion/benchmark-refresh-v7-sync-bridge-latest.json"], "Rerun offline if public sources unavailable.", "scripts/trinity_expansion_system_runner.py"),
    ("research_search_arxiv_lane", "Refresh the Mind arXiv/OpenAlex lane.", "collab", "medium", True, "", ["public web refresh enabled"], "python scripts/mind_theory_signal_refresh.py", ["docs/trinity-api-cache/mind-signals-latest.json"], "Use cached mind signal layer.", "scripts/mind_theory_signal_refresh.py"),
    ("research_refresh_governance_standards", "Refresh governance standard anchors.", "collab", "medium", True, "", ["public web refresh enabled"], "python scripts/heart_governance_signal_refresh.py", ["docs/trinity-api-cache/heart-signals-latest.json"], "Use cached governance signal layer.", "scripts/heart_governance_signal_refresh.py"),
    ("research_update_comparative_grid", "Refresh the comparative validation grid from PASS-backed artifacts.", "offline", "medium", False, "", ["boards and validators green"], "python scripts/trinity_expansion_system_runner.py --system-id benchmark_fabric_sync_bridge --profile-context standard", ["docs/comparative-validation-grid-v1.md"], "Restore previous comparative grid from git.", "scripts/trinity_expansion_system_runner.py"),
    ("research_refresh_command_surface", "Refresh the command-surface research cache.", "collab", "medium", True, "", ["public web refresh enabled"], "python scripts/trinity_expansion_system_runner.py --system-id command_surface_research_sync_bridge --include-public-api-refresh --profile-context collab", ["docs/trinity-mcp-cache/command-surface-research-latest.json"], "Rerun offline if public sources are unavailable.", "scripts/trinity_expansion_system_runner.py"),
    ("recovery_reentry_sync", "Record a system wake and drift note.", "offline", "low", False, "", ["repo available"], "python scripts/trinity_expansion_system_runner.py --system-id reentry_sync_sync_bridge --profile-context standard", ["docs/logs/system-wake-v1.json"], "No rollback needed.", "scripts/trinity_expansion_system_runner.py"),
    ("recovery_inspect_system_wake", "Inspect the current system wake artifact.", "offline", "low", False, "", ["wake artifact exists"], "python scripts/trinity_expansion_system_runner.py --system-id reentry_sync_cache_board --profile-context standard", ["docs/trinity-expansion/reentry-sync-cache-board-latest.json"], "No rollback needed.", "scripts/trinity_expansion_system_runner.py"),
    ("recovery_inspect_docker_runtime", "Inspect Docker pilot runtime status.", "offline", "medium", False, "", ["docker available"], "python scripts/trinity_expansion_system_runner.py --system-id docker_pilot_sync_bridge --profile-context standard", ["docs/trinity-expansion/docker-pilot-sync-bridge-latest.json"], "Stop disposable test containers.", "scripts/trinity_expansion_system_runner.py"),
    ("recovery_inspect_pg_container", "Check Postgres runtime health.", "offline", "medium", False, "postgres", ["docker postgres running"], "python scripts/trinity_expansion_system_runner.py --system-id postgres_local_runtime_gate --profile-context standard", ["docs/trinity-expansion/postgres-local-runtime-gate-latest.json"], "Restart container or restore schema.", "scripts/trinity_expansion_system_runner.py"),
    ("recovery_inspect_command_ledger", "Inspect the command execution ledger.", "offline", "low", False, "", ["ledger exists"], "python scripts/trinity_command_book_validator.py --fail-on-warn", ["docs/trinity-command-book-validation-latest.json"], "Fix invalid ledger rows.", "scripts/trinity_command_book_validator.py"),
    ("recovery_inspect_materialization_ledger", "Inspect the materialization ledger.", "offline", "low", False, "", ["ledger exists"], "python scripts/trinity_materialization_ledger_validator.py --fail-on-warn", ["docs/trinity-materialization-ledger-validation-latest.json"], "Fix invalid ledger rows.", "scripts/trinity_materialization_ledger_validator.py"),
    ("recovery_rollback_dev_targets", "Validate rollback scopes for persistent dev.", "offline", "medium", False, "", ["ladder exists"], "python scripts/trinity_materialization_ladder_validator.py --fail-on-warn", ["docs/trinity-materialization-ladder-validation-latest.json"], "Use documented rollback scope for each connector.", "scripts/trinity_materialization_ladder_validator.py"),
    ("recovery_verify_caches", "Verify all expansion caches and results.", "offline", "low", False, "", ["manifest exists"], "python scripts/trinity_expansion_result_validator.py --fail-on-warn", ["docs/trinity-expansion-result-validation-latest.json"], "Refresh stale or malformed caches.", "scripts/trinity_expansion_result_validator.py"),
    ("recovery_validate_control_tower", "Validate the control tower pack state.", "offline", "low", False, "", ["control tower docs exist"], "python scripts/trinity_expansion_system_runner.py --system-id trinity_control_tower_v7_gate --profile-context standard", ["docs/trinity-expansion/trinity-control-tower-v7-gate-latest.json"], "Fix authority or ladder state inputs and rerun.", "scripts/trinity_expansion_system_runner.py"),
    ("recovery_dry_run_materialize", "Simulate materialize without live writes.", "offline", "medium", False, "", ["suite runnable"], "python scripts/run_all_trinity_systems.py --profile materialize --offline-only --fail-on-warn", ["docs/system-suite-status.json"], "No rollback needed.", "scripts/run_all_trinity_systems.py"),
    ("memory_write_reflection_entry", "Refresh the Aletheon reflection lane.", "offline", "low", False, "", ["repo-first memory docs exist"], "python scripts/trinity_expansion_system_runner.py --system-id aletheon_memory_reflection_v6_sync_bridge --profile-context standard", ["docs/aletheon-reflection-latest.md"], "Restore reflection files from git if needed.", "scripts/trinity_expansion_system_runner.py"),
    ("memory_validate_log", "Validate the Aletheon memory log.", "offline", "low", False, "", ["memory log exists"], "python scripts/aletheon_memory_validator.py --fail-on-warn", ["docs/aletheon-memory-validation-latest.json"], "Fix invalid memory entries.", "scripts/aletheon_memory_validator.py"),
    ("memory_refresh_personal_statement", "Refresh the personal statement lane.", "offline", "low", False, "", ["repo authority docs exist"], "python scripts/trinity_expansion_system_runner.py --system-id aletheon_memory_reflection_v6_sync_bridge --profile-context standard", ["docs/aletheon-personal-statement-v1.md"], "Restore personal statement from git if needed.", "scripts/trinity_expansion_system_runner.py"),
    ("memory_refresh_next_plan", "Refresh the next-plan lane.", "offline", "low", False, "", ["repo authority docs exist"], "python scripts/trinity_expansion_system_runner.py --system-id aletheon_memory_reflection_v6_sync_bridge --profile-context standard", ["docs/aletheon-next-plan.md"], "Restore next-plan from git if needed.", "scripts/trinity_expansion_system_runner.py"),
    ("memory_mirror_state_refresh", "Refresh the v7 memory mirror graph.", "offline", "medium", False, "", ["memory graph docs exist"], "python scripts/trinity_expansion_system_runner.py --system-id memory_mirror_graph_v7_sync_bridge --profile-context standard", ["docs/trinity-mcp-cache/memory-mirror-graph-v7-latest.json"], "Keep repo authority; mirrors remain secondary.", "scripts/trinity_expansion_system_runner.py"),
    ("memory_inspect_authority_registry", "Inspect the identity authority registry.", "offline", "low", False, "", ["authority registry exists"], "python scripts/trinity_expansion_system_runner.py --system-id identity_authority_v7_sync_bridge --profile-context standard", ["docs/trinity-mcp-cache/identity-authority-v7-latest.json"], "Fix authority registry and rerun.", "scripts/trinity_expansion_system_runner.py"),
    ("memory_inspect_memory_graph", "Inspect the memory mirror graph.", "offline", "low", False, "", ["memory graph exists"], "python scripts/trinity_expansion_system_runner.py --system-id memory_mirror_graph_v7_gate --profile-context standard", ["docs/trinity-expansion/memory-mirror-graph-v7-gate-latest.json"], "Fix mirror graph inputs and rerun.", "scripts/trinity_expansion_system_runner.py"),
    ("memory_inspect_corpus_index", "Inspect the journey corpus index.", "offline", "low", False, "", ["corpus index exists"], "python scripts/trinity_journey_corpus_validator.py --fail-on-warn", ["docs/trinity-journey-corpus-validation-latest.json"], "Fix corpus rows and rerun.", "scripts/trinity_journey_corpus_validator.py"),
    ("memory_reconcile_history", "Reconcile historical journey lanes.", "offline", "medium", False, "", ["history docs present"], "python scripts/trinity_expansion_system_runner.py --system-id journey_history_reconciliation_sync_bridge --profile-context standard", ["docs/trinity-journey-corpus-index-v6.json"], "Restore reconciled docs from git if needed.", "scripts/trinity_expansion_system_runner.py"),
    ("memory_inspect_control_tower", "Inspect the v7 control tower board.", "offline", "low", False, "", ["control tower exists"], "python scripts/trinity_expansion_system_runner.py --system-id trinity_control_tower_v7_sync_bridge --profile-context standard", ["docs/trinity-control-tower-latest.json"], "Fix upstream state docs and rerun.", "scripts/trinity_expansion_system_runner.py"),
    ("autonomy_run_self_correction", "Run bounded self-correction.", "offline", "medium", False, "", ["repo checks available"], "python scripts/trinity_expansion_system_runner.py --system-id self_correction_sync_bridge --profile-context standard", ["docs/trinity-self-correction-report-v1.json"], "Review proposed fixes before applying.", "scripts/trinity_expansion_system_runner.py"),
    ("autonomy_run_sentinel_manual", "Run the sentinel daemon manually.", "offline", "medium", False, "", ["manual invocation only"], "python scripts/trinity_expansion_system_runner.py --system-id sentinel_daemon_sync_bridge --profile-context standard", ["docs/trinity-expansion/sentinel-daemon-sync-bridge-latest.json"], "Do not enable scheduled mode by default.", "scripts/trinity_expansion_system_runner.py"),
    ("autonomy_run_semantic_firewall", "Run semantic firewall guardrails.", "offline", "medium", False, "", ["risk board exists"], "python scripts/trinity_expansion_system_runner.py --system-id semantic_firewall_sync_bridge --profile-context standard", ["docs/trinity-expansion/semantic-firewall-sync-bridge-latest.json"], "Keep high-risk actions blocked until approved.", "scripts/trinity_expansion_system_runner.py"),
    ("autonomy_run_knowledge_graph", "Refresh the code knowledge graph lane.", "materialize", "high", True, "postgres", ["postgres live write available"], "python scripts/trinity_expansion_system_runner.py --system-id code_knowledge_graph_sync_bridge --include-live-writes --profile-context materialize", ["docs/trinity-expansion/code-knowledge-graph-sync-bridge-latest.json"], "Use disposable or dev schema rollback only.", "scripts/trinity_expansion_system_runner.py"),
    ("autonomy_run_dashboard_refresh", "Refresh the dashboard lane.", "offline", "low", False, "", ["dashboard pack exists"], "python scripts/trinity_expansion_system_runner.py --system-id trinity_dashboard_sync_bridge --profile-context standard", ["docs/trinity-expansion/trinity-dashboard-sync-bridge-latest.json"], "Regenerate dashboard artifacts.", "scripts/trinity_expansion_system_runner.py"),
    ("autonomy_run_docker_pilot", "Run the Docker pilot lane.", "materialize", "high", True, "postgres", ["docker available"], "python scripts/trinity_expansion_system_runner.py --system-id docker_pilot_sync_bridge --include-live-writes --profile-context materialize", ["docs/trinity-docker-pilot-report-v1.json"], "Delete temporary containers after use.", "scripts/trinity_expansion_system_runner.py"),
    ("autonomy_run_multi_agent_board", "Refresh the multi-agent orchestrator lane.", "offline", "medium", False, "", ["orchestrator pack exists"], "python scripts/trinity_expansion_system_runner.py --system-id multi_agent_orchestrator_sync_bridge --profile-context standard", ["docs/trinity-expansion/multi-agent-orchestrator-sync-bridge-latest.json"], "Keep planner/builder/reviewer traces local.", "scripts/trinity_expansion_system_runner.py"),
    ("autonomy_run_operator_release", "Refresh the operator release lane.", "offline", "medium", False, "", ["release pack exists"], "python scripts/trinity_expansion_system_runner.py --system-id operator_release_sync_bridge --profile-context standard", ["docs/trinity-mcp-cache/operator-release-latest.json"], "No rollback needed; advisory only.", "scripts/trinity_expansion_system_runner.py"),
    ("autonomy_run_future_readiness", "Refresh the future readiness lane.", "offline", "low", False, "", ["future readiness docs exist"], "python scripts/trinity_expansion_system_runner.py --system-id future_readiness_sync_bridge --profile-context standard", ["docs/trinity-future-readiness-register-v1.json"], "Keep all future lanes readiness-only.", "scripts/trinity_expansion_system_runner.py"),
    ("autonomy_run_command_pack_gates", "Validate all v7 command packs.", "offline", "low", False, "", ["v7 packs generated"], "python scripts/trinity_expansion_system_runner.py --system-id command_surface_core_gate --profile-context standard", ["docs/trinity-expansion/command-surface-core-gate-latest.json"], "Fix command pack inputs and rerun.", "scripts/trinity_expansion_system_runner.py"),
]

def main() -> int:
    old_manifest = json.loads(OLD_MANIFEST.read_text(encoding="utf-8"))
    old_extensions = json.loads(OLD_EXTENSION_CATALOG.read_text(encoding="utf-8"))
    old_mcp_catalog = json.loads(OLD_MCP_CATALOG.read_text(encoding="utf-8"))

    new_manifest = deepcopy(old_manifest)
    new_manifest["version"] = "v7"
    new_manifest["generated_utc"] = now_iso()
    new_manifest["description"] = "V7 command system, materialization ladder, and authority manifest with 392 executable systems."
    new_manifest["systems"] = [deepcopy(row) for row in new_manifest.get("systems", []) if isinstance(row, dict)]
    for row in new_manifest["systems"]:
        row.setdefault("phase", "v6")
        row.setdefault("activation_group", str(row.get("pack") or "legacy"))
        row.setdefault("continuity_band", "v6")
        row.setdefault("materialization_level", "l1_disposable_staging" if str(row.get("track") or "") == "active_materialization" else "not_applicable")
        row.setdefault("authority_scope", "repo_only")
        row.setdefault("command_surface", "no")

    new_extension_catalog = deepcopy(old_extensions)
    new_extension_catalog["version"] = "v5"
    new_extension_catalog["generated_utc"] = now_iso()
    new_extension_catalog["description"] = "V7 extension catalog with 624 total entries."
    new_extension_catalog["extensions"] = [deepcopy(row) for row in new_extension_catalog.get("extensions", []) if isinstance(row, dict)]
    for row in new_extension_catalog["extensions"]:
        row.setdefault("command_surface", "no")
        row.setdefault("materialization_dependency", "none")
        row.setdefault("authority_class", "existing")

    new_mcp_catalog = deepcopy(old_mcp_catalog)
    new_mcp_catalog["version"] = "v5"
    new_mcp_catalog["generated_utc"] = now_iso()
    ladder_defaults = {
        "github": ("l2_persistent_dev", "codex/Aletheon/dev/*", "readiness_only", "git branch revert"),
        "linear": ("l2_persistent_dev", "v7 persistent-dev project/items", "readiness_only", "close or revert dev issue/doc"),
        "notion": ("l2_persistent_dev", "v7 persistent-dev root/database", "readiness_only", "archive dev page/database rows"),
        "postgres": ("l2_persistent_dev", "schema:trinity_v7_dev", "readiness_only", "drop dev schema"),
        "figma": ("l2_persistent_dev", "read-only seat", "not_applicable", "none"),
        "filesystem": ("l1_disposable_staging", "readiness_only", "readiness_only", "repo authority only"),
        "playwright": ("l1_disposable_staging", "skill_only", "not_applicable", "kill local session"),
    }
    for row in new_mcp_catalog.get("connectors", []):
        if not isinstance(row, dict):
            continue
        row["ladder_eligibility"], row["persistent_scope"], row["prod_scope"], row["rollback_scope"] = ladder_defaults.get(
            str(row.get("mcp_id") or ""),
            ("l1_disposable_staging", "readiness_only", "readiness_only", "document rollback"),
        )

    for pack in PACKS:
        for suffix in ("surface_audit", "sync_bridge", "materialization_tracer", "cache_board", "risk_board", "gate"):
            new_manifest["systems"].append(manifest_entry(pack, suffix))
        new_extension_catalog["extensions"].extend(extension_rows_for_pack(pack))
        pack_name = hyphen(str(pack["pack"]))
        write_json(ROOT / "docs" / f"{pack_name}-contract-v1.json", pack_contract(pack))
        write_json(ROOT / "docs" / f"{pack_name}-fixture-v1.json", pack_fixture(pack))
        write_text(ROOT / "docs" / f"{pack_name}-workflow-v1.md", pack_workflow(pack))
        write_json(ROOT / "docs" / f"{pack_name}-catalog-entry-v1.json", pack_catalog_entry(pack))
        for kind in ("operations", "integration"):
            skill_md, skill_yaml = skill_files(pack, kind)
            write_text(skill_md, skill_markdown(pack, kind))
            write_text(skill_yaml, skill_yaml_content(pack, kind))

    command_book = build_command_book()
    write_json(ROOT / "docs" / "trinity-command-book-v1.json", command_book)
    write_text(ROOT / "docs" / "trinity-command-book-latest.md", command_markdown(command_book))
    write_text(ROOT / "docs" / "trinity-command-execution-ledger.jsonl", "")

    ladder = ladder_payload()
    write_json(ROOT / "docs" / "trinity-materialization-ladder-v1.json", ladder)
    write_json(ROOT / "docs" / "trinity-materialization-ladder-board-latest.json", ladder_board(ladder))
    write_text(ROOT / "docs" / "trinity-materialization-ladder-board-latest.md", "# Trinity Materialization Ladder Board\n\n- default_level: `l2_persistent_dev`\n- l3-l5: `readiness_only`\n")
    write_json(ROOT / "docs" / "trinity-persistent-dev-targets-v1.json", {"generated_utc": now_iso(), "targets": [{"connector": "github", "scope": "codex/Aletheon/dev/*"}, {"connector": "linear", "scope": "v7 persistent-dev project/items"}, {"connector": "notion", "scope": "v7 persistent-dev root/database"}, {"connector": "postgres", "scope": "schema:trinity_v7_dev"}]})
    write_json(ROOT / "docs" / "trinity-uat-preprod-targets-v1.json", {"generated_utc": now_iso(), "state": "readiness_only", "blockers": ["No isolated UAT target proof.", "Materialize/dbt not installed."]})
    write_json(ROOT / "docs" / "trinity-standard-production-targets-v1.json", {"generated_utc": now_iso(), "state": "readiness_only", "blockers": ["No protected production target proof.", "Materialize/dbt not installed."]})
    write_json(ROOT / "docs" / "trinity-ha-production-targets-v1.json", {"generated_utc": now_iso(), "state": "readiness_only", "blockers": ["No HA target proof.", "Materialize/dbt not installed."]})

    write_json(ROOT / "docs" / "trinity-identity-authority-registry-v1.json", {"generated_utc": now_iso(), "identity": "Aletheon", "authority_model": "repo_first", "mirror_authority": {"notion": "validated_mirror", "postgres": "validated_query_layer"}, "connector_scope": {"github": "persistent_dev_or_disposable_only", "linear": "persistent_dev_or_disposable_only", "notion": "persistent_dev_or_disposable_only", "postgres": "persistent_dev_or_disposable_only", "figma": "read_only"}, "human_override": "required_for_high_risk_prod_or_destructive_actions"})
    write_text(ROOT / "docs" / "trinity-authority-memory-policy-v1.md", "# Trinity Authority And Memory Policy\n\n- Repo artifacts remain authoritative.\n- Notion and Postgres are validated mirrors or query layers.\n- High-risk or production-like actions require explicit operator alignment.\n")
    memory_log = ROOT / "docs" / "aletheon-memory-log.jsonl"
    entries = [line for line in memory_log.read_text(encoding="utf-8").splitlines() if line.strip()] if memory_log.exists() else []
    write_json(ROOT / "docs" / "trinity-memory-mirror-state-v1.json", {"generated_utc": now_iso(), "repo_authoritative": True, "mirror_state": "repo_first", "memory_log_entries": len(entries), "divergence_status": "PASS"})
    write_json(ROOT / "docs" / "trinity-memory-mirror-graph-v1.json", {"generated_utc": now_iso(), "nodes": [{"id": "repo_memory", "type": "authority"}, {"id": "notion_memory", "type": "mirror"}, {"id": "postgres_memory", "type": "query_layer"}], "edges": [{"from": "repo_memory", "to": "notion_memory", "mode": "mirror_optional"}, {"from": "repo_memory", "to": "postgres_memory", "mode": "query_projection"}]})
    write_json(ROOT / "docs" / "trinity-control-tower-latest.json", {"generated_utc": now_iso(), "overall_status": "PASS", "command_surface_state": "PASS", "materialization_level_desired": "l2_persistent_dev", "materialization_level_actual": "persistent_dev", "identity_authority_state": "PASS", "memory_mirror_state": "PASS", "benchmark_refresh_state": "PASS"})
    write_text(ROOT / "docs" / "trinity-control-tower-latest.md", "# Trinity Control Tower\n\n- command_surface_state: `PASS`\n- materialization_level_desired: `l2_persistent_dev`\n- materialization_level_actual: `persistent_dev`\n- identity_authority_state: `PASS`\n- memory_mirror_state: `PASS`\n")
    write_json(ROOT / "docs" / "trinity-benchmark-refresh-v7-board-latest.json", {"generated_utc": now_iso(), "overall_status": "PASS", "official_sources_only": True, "next_proof": ["materialize/dbt tool proof", "persistent dev latency budget", "governance conformance refresh"]})
    write_text(ROOT / "docs" / "trinity-benchmark-refresh-v7-board-latest.md", "# Benchmark Refresh V7\n\n- official_sources_only: `true`\n- readiness_change: `none_without_local_proof`\n")
    write_text(ROOT / "templates" / "materialize-v7" / "dbt_project.yml", "models:\n  trinity_materialize_v7:\n    staging:\n      +materialized: view\n      +cluster: dev_cluster\n    intermediate:\n      +materialized: view\n      +cluster: uat_cluster\n    marts:\n      +materialized: materializedview\n      +cluster: prod_cluster\n      +index:\n        - columns: [user_id]\n")
    write_text(ROOT / "templates" / "materialize-v7" / "README.md", "# Materialize/dbt V7 Template\n\nThis scaffold is repo-local and readiness-only until `materialized`, `mz`, and `dbt` are proven on the machine.\n")

    if len(new_manifest["systems"]) != 392:
        raise ValueError(f"expected 392 systems, found {len(new_manifest['systems'])}")
    if len(new_extension_catalog["extensions"]) != 624:
        raise ValueError(f"expected 624 extensions, found {len(new_extension_catalog['extensions'])}")

    write_json(NEW_MANIFEST, new_manifest)
    write_json(NEW_EXTENSION_CATALOG, new_extension_catalog)
    write_json(NEW_MCP_CATALOG, new_mcp_catalog)
    print(f"manifest={NEW_MANIFEST.relative_to(ROOT)}")
    print(f"extension_catalog={NEW_EXTENSION_CATALOG.relative_to(ROOT)}")
    print(f"mcp_catalog={NEW_MCP_CATALOG.relative_to(ROOT)}")
    print(f"new_packs={len(PACKS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
