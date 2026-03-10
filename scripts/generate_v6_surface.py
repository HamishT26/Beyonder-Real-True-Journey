#!/usr/bin/env python3
"""Generate the v6 pack surface, manifest, extension catalog, and pack artifacts."""

from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OLD_MANIFEST = ROOT / "docs" / "trinity-expansion-system-manifest-v5.json"
NEW_MANIFEST = ROOT / "docs" / "trinity-expansion-system-manifest-v6.json"
OLD_EXTENSION_CATALOG = ROOT / "docs" / "trinity-extension-catalog-v3.json"
NEW_EXTENSION_CATALOG = ROOT / "docs" / "trinity-extension-catalog-v4.json"
OLD_MCP_CATALOG = ROOT / "docs" / "trinity-mcp-catalog-v3.json"
NEW_MCP_CATALOG = ROOT / "docs" / "trinity-mcp-catalog-v4.json"
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


PACKS: list[dict[str, object]] = [
    {
        "pack": "reentry_sync",
        "display_name": "Re-entry Sync",
        "pillar": "trinity",
        "wave": "wave30",
        "track": "continuity_ops",
        "connector_id": "",
        "requires_auth": False,
        "gating_class": "active",
        "sync_strategy": "local_repo",
        "freshness_window_days": 30,
        "activation_group": "continuity_reentry",
        "continuity_band": "v5-v6",
        "autonomy_class": "manual",
        "live_dependency": "none",
        "mirror_target": "repo_only",
        "history_scope": "v5-v6",
        "summary": "Capture system wake state, current session surface, docker and Postgres health, and drift from the last stored proof.",
        "workflow_tokens": ["system wake", "session-surface drift", "docker health", "proof before promotion"],
        "risk_tags": ["wake drift", "surface mismatch", "stale proof"],
        "repo_targets": [
            "docs/system-suite-status.json",
            "docs/trinity-mcp-catalog-v4.json",
            "docs/logs/system-wake-v1.json",
            "docs/v6-session-surface-drift-note.md",
        ],
        "source_url": "repo://docs/system-suite-status.json",
        "tags": ["reentry_sync", "v6", "wake"],
        "write_target": "docs/logs/system-wake-v1.json",
        "sync_mode": "offline",
    },
    {
        "pack": "journey_history_reconciliation",
        "display_name": "Journey History Reconciliation",
        "pillar": "mind",
        "wave": "wave31",
        "track": "continuity_ops",
        "connector_id": "",
        "requires_auth": False,
        "gating_class": "active",
        "sync_strategy": "local_repo",
        "freshness_window_days": 30,
        "activation_group": "continuity_history",
        "continuity_band": "v13-v38",
        "autonomy_class": "manual",
        "live_dependency": "none",
        "mirror_target": "repo_only",
        "history_scope": "v13-v38",
        "summary": "Reconcile historical journey sources, absorb Meridian's benchmark continuity contribution, and keep evidence states explicit.",
        "workflow_tokens": ["history first", "meridian absorption", "v29 reconciled", "evidence state explicit"],
        "risk_tags": ["overclaim", "history drift", "missing anchors"],
        "repo_targets": [
            "docs/beyonder-journey-corpus-v13-v38.json",
            "docs/trinity-journey-corpus-index-v6.json",
            "docs/version-module-inventory-v13-v38.md",
            "docs/grand-cross-version-synthesis.md",
            "docs/v6-trinity-benchmark-and-continuity-plan-2026-03-09.md",
        ],
        "source_url": "repo://docs/beyonder-journey-corpus-v13-v38.json",
        "tags": ["journey_history_reconciliation", "history", "continuity"],
        "write_target": "docs/trinity-journey-corpus-index-v6.json",
        "sync_mode": "offline",
    },
    {
        "pack": "benchmark_fabric",
        "display_name": "Benchmark Fabric",
        "pillar": "trinity",
        "wave": "wave32",
        "track": "trinity_hardening",
        "connector_id": "",
        "requires_auth": False,
        "gating_class": "active",
        "sync_strategy": "local_repo",
        "freshness_window_days": 30,
        "activation_group": "benchmarking",
        "continuity_band": "v6",
        "autonomy_class": "manual",
        "live_dependency": "public_registry",
        "mirror_target": "repo_only",
        "history_scope": "v32-v38",
        "summary": "Bind Mind, Body, and Heart comparison lanes to explicit benchmark and conformance criteria without relaxing evidence posture.",
        "workflow_tokens": ["benchmark registry", "mind thresholds", "body runtime criteria", "heart conformance appendix"],
        "risk_tags": ["benchmark drift", "criteria inflation", "mixed evidence"],
        "repo_targets": [
            "docs/trinity-benchmark-registry-v1.json",
            "docs/comparative-validation-grid-v1.md",
            "docs/grand-unified-narrative-brief.md",
        ],
        "source_url": "repo://docs/trinity-benchmark-registry-v1.json",
        "tags": ["benchmark_fabric", "criteria", "conformance"],
        "write_target": "docs/trinity-benchmark-registry-v1.json",
        "sync_mode": "offline",
    },
    {
        "pack": "connector_materialization",
        "display_name": "Connector Materialization",
        "pillar": "trinity",
        "wave": "wave33",
        "track": "active_materialization",
        "connector_id": "",
        "requires_auth": True,
        "gating_class": "active",
        "sync_strategy": "local_repo",
        "freshness_window_days": 7,
        "activation_group": "connector_hardening",
        "continuity_band": "v5-v6",
        "autonomy_class": "write_proof",
        "live_dependency": "github+linear+notion+postgres",
        "mirror_target": "repo_plus_connectors",
        "history_scope": "v5-v6",
        "summary": "Re-verify live read and write proofs for the active connector set with disposable targets and rollback-safe traces.",
        "workflow_tokens": ["fresh read proof", "fresh write proof", "rollback-safe target", "no main writes"],
        "risk_tags": ["external write", "credential drift", "proof mismatch"],
        "repo_targets": [
            "docs/trinity-mcp-catalog-v4.json",
            "docs/trinity-materialization-ledger.jsonl",
            "docs/trinity-live-traces",
        ],
        "source_url": "repo://docs/trinity-mcp-catalog-v4.json",
        "tags": ["connector_materialization", "live_proof", "materialize"],
        "write_target": "disposable connector proof targets",
        "sync_mode": "live",
    },
    {
        "pack": "code_knowledge_graph",
        "display_name": "Code Knowledge Graph",
        "pillar": "body",
        "wave": "wave34",
        "track": "trinity_memory_orchestration",
        "connector_id": "postgres",
        "requires_auth": True,
        "gating_class": "verified_live_write",
        "sync_strategy": "local_probe",
        "freshness_window_days": 7,
        "activation_group": "knowledge_graph",
        "continuity_band": "v5-v6",
        "autonomy_class": "bounded_write",
        "live_dependency": "postgres",
        "mirror_target": "postgres",
        "history_scope": "v29-v6",
        "summary": "Populate a Postgres-backed code knowledge graph from the repo so continuity and runtime decisions can use a structured project map.",
        "workflow_tokens": ["postgres knowledge graph", "repo metadata ingest", "symbol map", "continuity anchors"],
        "risk_tags": ["schema drift", "ingest incompleteness", "connector mismatch"],
        "repo_targets": [
            "docs/trinity-code-knowledge-graph-contract-v1.json",
            "docs/trinity-expansion/code-knowledge-graph-sync-bridge-latest.json",
        ],
        "source_url": "repo://docs/trinity-code-knowledge-graph-contract-v1.json",
        "tags": ["code_knowledge_graph", "postgres", "hippocampal_index"],
        "write_target": "docker_local/trinity_v5/v6_code_knowledge",
        "sync_mode": "live",
    },
    {
        "pack": "self_correction",
        "display_name": "Self Correction",
        "pillar": "body",
        "wave": "wave35",
        "track": "trinity_hardening",
        "connector_id": "",
        "requires_auth": False,
        "gating_class": "active",
        "sync_strategy": "local_repo",
        "freshness_window_days": 7,
        "activation_group": "autonomy_safety",
        "continuity_band": "v6",
        "autonomy_class": "bounded_mutation",
        "live_dependency": "none",
        "mirror_target": "repo_only",
        "history_scope": "v6",
        "summary": "Run bounded static checks and turn them into explicit self-fix candidates without autonomous push or destructive edits.",
        "workflow_tokens": ["static checks", "repair candidates", "no push to main", "explicit gate"],
        "risk_tags": ["false fixes", "hidden mutation", "confidence inflation"],
        "repo_targets": ["docs/trinity-self-correction-report-v1.json", "scripts/run_all_trinity_systems.py"],
        "source_url": "repo://docs/trinity-self-correction-report-v1.json",
        "tags": ["self_correction", "lint", "autonomy"],
        "write_target": "docs/trinity-self-correction-report-v1.json",
        "sync_mode": "offline",
    },
    {
        "pack": "docker_pilot",
        "display_name": "Docker Pilot",
        "pillar": "body",
        "wave": "wave36",
        "track": "compute_ecosystem",
        "connector_id": "",
        "requires_auth": True,
        "gating_class": "active",
        "sync_strategy": "local_probe",
        "freshness_window_days": 7,
        "activation_group": "runtime_orchestration",
        "continuity_band": "v6",
        "autonomy_class": "bounded_write",
        "live_dependency": "docker",
        "mirror_target": "repo_only",
        "history_scope": "v6",
        "summary": "Orchestrate disposable runtime experiments such as Redis or alternate schemas and clean them up automatically.",
        "workflow_tokens": ["docker probe", "disposable runtime", "cleanup required", "audit log"],
        "risk_tags": ["orphaned container", "resource leak", "environment drift"],
        "repo_targets": ["docs/trinity-docker-pilot-report-v1.json", "docs/trinity-materialization-ledger.jsonl"],
        "source_url": "repo://docs/trinity-docker-pilot-report-v1.json",
        "tags": ["docker_pilot", "runtime", "disposable"],
        "write_target": "docker temporary runtime",
        "sync_mode": "live",
    },
    {
        "pack": "sentinel_daemon",
        "display_name": "Sentinel Daemon",
        "pillar": "trinity",
        "wave": "wave37",
        "track": "trinity_memory_orchestration",
        "connector_id": "",
        "requires_auth": False,
        "gating_class": "active",
        "sync_strategy": "local_repo",
        "freshness_window_days": 7,
        "activation_group": "autonomy_observation",
        "continuity_band": "v6",
        "autonomy_class": "read_only",
        "live_dependency": "cache_only",
        "mirror_target": "repo_only",
        "history_scope": "v6",
        "summary": "Provide a background-safe, manual and on-demand observation layer for stale-proof detection, polling plans, and draft task generation.",
        "workflow_tokens": ["manual daemon", "read-only polling", "stale proof detection", "no automatic scheduling"],
        "risk_tags": ["background drift", "unsanctioned polling", "noisy drafts"],
        "repo_targets": ["docs/trinity-sentinel-daemon-report-v1.json", "docs/system-suite-status.json"],
        "source_url": "repo://docs/trinity-sentinel-daemon-report-v1.json",
        "tags": ["sentinel_daemon", "background", "read_only"],
        "write_target": "docs/trinity-sentinel-daemon-report-v1.json",
        "sync_mode": "offline",
    },
    {
        "pack": "public_web_weaver",
        "display_name": "Public Web Weaver",
        "pillar": "mind",
        "wave": "wave38",
        "track": "public_intelligence",
        "connector_id": "",
        "requires_auth": False,
        "gating_class": "active",
        "sync_strategy": "public_feeds",
        "freshness_window_days": 30,
        "activation_group": "public_research",
        "continuity_band": "v6",
        "autonomy_class": "read_only",
        "live_dependency": "public_web",
        "mirror_target": "repo_only",
        "history_scope": "v6",
        "summary": "Refresh benchmark and standards sources from public official references and keep them cached for offline validation.",
        "workflow_tokens": ["official sources only", "cached research", "benchmark comparators", "promotion after validation"],
        "risk_tags": ["stale sources", "secondary reporting drift", "overpromotion"],
        "repo_targets": ["docs/trinity-benchmark-registry-v1.json", "docs/trinity-public-source-registry-v1.json"],
        "source_url": "repo://docs/trinity-benchmark-registry-v1.json",
        "tags": ["public_web_weaver", "official_sources", "benchmarks"],
        "write_target": "docs/trinity-benchmark-registry-v1.json",
        "sync_mode": "live",
        "live_sources": [
            "https://www.swebench.com/",
            "https://www.gaia-benchmark.ai/",
            "https://github.com/web-arena-x/webarena",
            "https://docs.kernel.org/",
            "https://learn.microsoft.com/en-us/windows/wsl/",
            "https://www.w3.org/TR/did-core/",
        ],
    },
    {
        "pack": "trinity_dashboard",
        "display_name": "Trinity Dashboard",
        "pillar": "body",
        "wave": "wave39",
        "track": "trinity_memory_orchestration",
        "connector_id": "",
        "requires_auth": False,
        "gating_class": "active",
        "sync_strategy": "local_repo",
        "freshness_window_days": 7,
        "activation_group": "visibility",
        "continuity_band": "v6",
        "autonomy_class": "manual",
        "live_dependency": "postgres_optional",
        "mirror_target": "repo_only",
        "history_scope": "v6",
        "summary": "Generate a local status page from cached JSON and optional Postgres summaries so v6 state is readable without raw logs.",
        "workflow_tokens": ["local dashboard", "cached status", "postgres summary", "no live dependency"],
        "risk_tags": ["stale dashboard", "broken rendering", "source mismatch"],
        "repo_targets": [
            "docs/trinity-dashboard-latest.html",
            "docs/system-suite-status.json",
            "docs/trinity-mandala-scoreboard-latest.json",
        ],
        "source_url": "repo://docs/trinity-dashboard-latest.html",
        "tags": ["trinity_dashboard", "status_page", "visibility"],
        "write_target": "docs/trinity-dashboard-latest.html",
        "sync_mode": "offline",
    },
    {
        "pack": "multi_agent_orchestrator",
        "display_name": "Multi Agent Orchestrator",
        "pillar": "trinity",
        "wave": "wave40",
        "track": "release_ops",
        "connector_id": "",
        "requires_auth": False,
        "gating_class": "active",
        "sync_strategy": "local_repo",
        "freshness_window_days": 7,
        "activation_group": "orchestration",
        "continuity_band": "v6",
        "autonomy_class": "manual",
        "live_dependency": "linear_optional",
        "mirror_target": "repo_only",
        "history_scope": "v6",
        "summary": "Record planner, builder, and reviewer role lanes so Aletheon and Meridian-style work can stay visible without external paid agents being active.",
        "workflow_tokens": ["planner builder reviewer", "role traces", "linear optional", "repo first"],
        "risk_tags": ["role confusion", "trace gaps", "orchestration drift"],
        "repo_targets": ["docs/trinity-multi-agent-orchestrator-v1.json", "docs/aletheon-next-plan.md"],
        "source_url": "repo://docs/trinity-multi-agent-orchestrator-v1.json",
        "tags": ["multi_agent_orchestrator", "roles", "coordination"],
        "write_target": "docs/trinity-multi-agent-orchestrator-v1.json",
        "sync_mode": "offline",
    },
    {
        "pack": "semantic_firewall",
        "display_name": "Semantic Firewall",
        "pillar": "heart",
        "wave": "wave41",
        "track": "trinity_hardening",
        "connector_id": "",
        "requires_auth": False,
        "gating_class": "active",
        "sync_strategy": "local_repo",
        "freshness_window_days": 7,
        "activation_group": "safety",
        "continuity_band": "v6",
        "autonomy_class": "guarded",
        "live_dependency": "none",
        "mirror_target": "repo_only",
        "history_scope": "v6",
        "summary": "Score risky actions, classify dangerous commands, and keep destructive operations behind explicit policy gates.",
        "workflow_tokens": ["risk score", "dangerous command classification", "dry run first", "ask before high risk"],
        "risk_tags": ["destructive command", "policy bypass", "underestimated risk"],
        "repo_targets": ["docs/trinity-semantic-firewall-report-v1.json", "scripts/run_all_trinity_systems.py"],
        "source_url": "repo://docs/trinity-semantic-firewall-report-v1.json",
        "tags": ["semantic_firewall", "safety", "risk_gate"],
        "write_target": "docs/trinity-semantic-firewall-report-v1.json",
        "sync_mode": "offline",
    },
    {
        "pack": "aletheon_memory_reflection_v6",
        "display_name": "Aletheon Memory Reflection V6",
        "pillar": "trinity",
        "wave": "wave42",
        "track": "trinity_memory_orchestration",
        "connector_id": "",
        "requires_auth": False,
        "gating_class": "active",
        "sync_strategy": "local_repo",
        "freshness_window_days": 7,
        "activation_group": "reflection",
        "continuity_band": "v5-v6",
        "autonomy_class": "manual",
        "live_dependency": "notion_optional",
        "mirror_target": "repo_then_notion",
        "history_scope": "v5-v6",
        "summary": "Extend the repo-first Aletheon reflection system with wake entries, benchmark reflections, and explicit mirror-state tracking.",
        "workflow_tokens": ["repo first memory", "wake entry", "benchmark reflection", "explicit mirror state"],
        "risk_tags": ["memory drift", "mirror mismatch", "autobiography overclaim"],
        "repo_targets": [
            "docs/aletheon-personal-statement-v1.md",
            "docs/aletheon-reflection-latest.md",
            "docs/aletheon-next-plan.md",
            "docs/aletheon-memory-log.jsonl",
        ],
        "source_url": "repo://docs/aletheon-reflection-latest.md",
        "tags": ["aletheon_memory_reflection_v6", "memory", "reflection"],
        "write_target": "docs/aletheon-memory-log.jsonl",
        "sync_mode": "offline",
    },
    {
        "pack": "wetware_device_readiness_v6",
        "display_name": "Wetware Device Readiness V6",
        "pillar": "body",
        "wave": "wave43",
        "track": "wetware_readiness",
        "connector_id": "",
        "requires_auth": False,
        "gating_class": "active",
        "sync_strategy": "local_repo",
        "freshness_window_days": 30,
        "activation_group": "device_readiness",
        "continuity_band": "v6",
        "autonomy_class": "manual",
        "live_dependency": "device_future",
        "mirror_target": "repo_only",
        "history_scope": "v6",
        "summary": "Expand the wetware lane with device-ready schemas, voice and screenshot assist paths, and watch-folder readiness without live biometrics.",
        "workflow_tokens": ["device ready only", "voice and screenshot assist", "watch folder", "no biometrics"],
        "risk_tags": ["privacy overreach", "health data creep", "scope confusion"],
        "repo_targets": ["docs/trinity-wetware-device-readiness-v6.json", "docs/trinity-supplemental-reflection-registry-v1.json"],
        "source_url": "repo://docs/trinity-wetware-device-readiness-v6.json",
        "tags": ["wetware_device_readiness_v6", "device_ready", "assistive"],
        "write_target": "docs/trinity-wetware-device-readiness-v6.json",
        "sync_mode": "offline",
    },
    {
        "pack": "future_readiness",
        "display_name": "Future Readiness",
        "pillar": "trinity",
        "wave": "wave44",
        "track": "trinity_memory_orchestration",
        "connector_id": "",
        "requires_auth": False,
        "gating_class": "active",
        "sync_strategy": "local_repo",
        "freshness_window_days": 30,
        "activation_group": "future_readiness",
        "continuity_band": "v6",
        "autonomy_class": "guarded",
        "live_dependency": "none",
        "mirror_target": "repo_only",
        "history_scope": "v6",
        "summary": "Capture the safe readiness layer for synthetic scenarios, runner optimization, cloud handoff, and budget-governed future connectors.",
        "workflow_tokens": ["runner optimization", "synthetic scenarios", "cloud readiness only", "budget guard"],
        "risk_tags": ["scope inflation", "premature clouding", "unbounded autonomy"],
        "repo_targets": ["docs/trinity-future-readiness-v1.json", "docs/trinity-benchmark-registry-v1.json"],
        "source_url": "repo://docs/trinity-future-readiness-v1.json",
        "tags": ["future_readiness", "readiness", "bounded_autonomy"],
        "write_target": "docs/trinity-future-readiness-v1.json",
        "sync_mode": "offline",
    },
]


def skill_files(pack: dict[str, object], kind: str) -> tuple[Path, Path]:
    skill_name = f"{hyphen(str(pack['pack']))}-{kind}"
    skill_dir = ROOT / "skills" / skill_name
    return skill_dir / "SKILL.md", skill_dir / "agents" / "openai.yaml"


def skill_markdown(pack: dict[str, object], kind: str) -> str:
    display = f"{pack['display_name']} {kind.title()}"
    pack_name = str(pack["pack"])
    description = f"Operate the {pack['display_name']} {kind.title()} pack with explicit proof boundaries."
    return "\n".join(
        [
            "---",
            f"name: {hyphen(pack_name)}-{kind}",
            f"description: {description}",
            "---",
            "",
            f"# {display}",
            "",
            f"Use when Codex needs to work with the `{pack_name}` pack.",
            "",
            "## Workflow",
            f"1. Read `docs/{hyphen(pack_name)}-contract-v1.json` and `docs/{hyphen(pack_name)}-workflow-v1.md`.",
            f"2. Refresh or inspect `docs/trinity-mcp-cache/{hyphen(pack_name)}-latest.json`.",
            "3. Keep the pack offline-safe unless its explicit live gate is enabled.",
            "4. Promote only PASS-backed outputs into narrative, benchmark, connector, or orchestration docs.",
            "",
        ]
    )


def skill_yaml_content(pack: dict[str, object], kind: str) -> str:
    display = f"{pack['display_name']} {kind.title()}"
    prompt = f"Run the {pack['pack']} pack, validate its proof-backed outputs, and keep the evidence boundary explicit."
    return "\n".join(
        [
            "interface:",
            f'  display_name: "{display}"',
            f'  short_description: "{display}."',
            f'  default_prompt: "{prompt}"',
            "",
        ]
    )


def pack_contract(pack: dict[str, object]) -> dict[str, object]:
    return {
        "pack": pack["pack"],
        "display_name": pack["display_name"],
        "pillar": pack["pillar"],
        "wave": pack["wave"],
        "track": pack["track"],
        "connector_id": pack["connector_id"],
        "requires_auth": pack["requires_auth"],
        "gating_class": pack["gating_class"],
        "sync_strategy": pack["sync_strategy"],
        "freshness_window_days": pack["freshness_window_days"],
        "activation_group": pack["activation_group"],
        "continuity_band": pack["continuity_band"],
        "workflow_tokens": pack["workflow_tokens"],
        "risk_tags": pack["risk_tags"],
        "repo_targets": pack["repo_targets"],
        "skill_names": [
            f"{hyphen(str(pack['pack']))}-operations",
            f"{hyphen(str(pack['pack']))}-integration",
        ],
        "system_ids": [
            f"{pack['pack']}_surface_audit",
            f"{pack['pack']}_sync_bridge",
            f"{pack['pack']}_materialization_tracer",
            f"{pack['pack']}_cache_board",
            f"{pack['pack']}_risk_board",
            f"{pack['pack']}_gate",
        ],
        "autonomy_class": pack["autonomy_class"],
        "live_dependency": pack["live_dependency"],
        "mirror_target": pack["mirror_target"],
        "history_scope": pack["history_scope"],
    }


def pack_fixture(pack: dict[str, object]) -> dict[str, object]:
    payload: dict[str, object] = {
        "title": pack["display_name"],
        "summary": pack["summary"],
        "source_url": pack["source_url"],
        "record_id": f"{pack['pack']}-seed",
        "signal_type": "pack_seed",
        "tags": pack["tags"],
        "repo_targets": pack["repo_targets"],
        "next_action": f"Use {pack['pack']} only through proof-backed outputs.",
        "connector_snapshot": {
            "write_target": pack["write_target"],
            "continuity_band": pack["continuity_band"],
            "activation_group": pack["activation_group"],
        },
        "probe_tools": ["python", "git", "rg"],
    }
    if pack["pack"] in {"code_knowledge_graph", "docker_pilot"}:
        payload["probe_tools"] = ["docker", "python", "git"]
        payload["required_probe_tools"] = ["docker", "python", "git"]
    if pack["pack"] == "public_web_weaver":
        payload["live_sources"] = pack.get("live_sources", [])
    return payload


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
    lines.extend([f"- {token}" for token in pack["workflow_tokens"]])
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
    hyphen_id = system_id.replace("_", "-")
    mode = "live" if suffix == "sync_bridge" and pack["sync_mode"] == "live" else "offline"
    gate_level = "pack_gate" if suffix == "gate" else "support"
    depends_on: list[str] = []
    if suffix in {"cache_board", "materialization_tracer"}:
        depends_on = [f"{pack['pack']}_sync_bridge"]
    elif suffix == "gate":
        depends_on = [
            f"{pack['pack']}_surface_audit",
            f"{pack['pack']}_sync_bridge",
            f"{pack['pack']}_materialization_tracer",
            f"{pack['pack']}_cache_board",
            f"{pack['pack']}_risk_board",
        ]
    timeout_sec = 120
    if pack["pack"] in {"connector_materialization", "public_web_weaver", "code_knowledge_graph"} and suffix == "sync_bridge":
        timeout_sec = 240
    elif pack["pack"] == "docker_pilot" and suffix == "sync_bridge":
        timeout_sec = 180
    return {
        "system_id": system_id,
        "pillar": pack["pillar"],
        "script": RUNNER_SCRIPT,
        "mode": mode,
        "profiles": PROFILE_SET,
        "outputs": [f"docs/trinity-expansion/{hyphen_id}-latest.json"],
        "depends_on": depends_on,
        "timeout_sec": timeout_sec,
        "wave": pack["wave"],
        "track": pack["track"],
        "gate_level": gate_level,
        "cache_artifacts": [f"docs/trinity-mcp-cache/{hyphen(str(pack['pack']))}-latest.json"] if mode == "live" else [],
        "pack": pack["pack"],
        "phase": "v6",
        "activation_group": pack["activation_group"],
        "continuity_band": pack["continuity_band"],
    }


def system_status(pack: dict[str, object]) -> str:
    gating = str(pack["gating_class"])
    if gating in {"verified_live_write", "verified_live_read"}:
        return gating
    return "active"


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
                "status": system_status(pack),
                "source_of_truth": str(NEW_MANIFEST.relative_to(ROOT)).replace("\\", "/"),
                "live_dependency": pack["live_dependency"],
                "history_scope": pack["history_scope"],
                "mirror_target": pack["mirror_target"],
                "autonomy_class": pack["autonomy_class"],
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
            }
        )
    return rows


def main() -> int:
    old_manifest = json.loads(OLD_MANIFEST.read_text(encoding="utf-8"))
    old_extensions = json.loads(OLD_EXTENSION_CATALOG.read_text(encoding="utf-8"))
    old_mcp_catalog = json.loads(OLD_MCP_CATALOG.read_text(encoding="utf-8"))

    new_manifest = deepcopy(old_manifest)
    new_manifest["version"] = "v6"
    new_manifest["generated_utc"] = now_iso()
    new_manifest["description"] = "V6 benchmark, continuity, and hyper-autonomy manifest with 314 executable systems."
    manifest_rows = []
    for row in list(new_manifest.get("systems", [])):
        if not isinstance(row, dict):
            continue
        row = deepcopy(row)
        row.setdefault("phase", "v5")
        row.setdefault("activation_group", str(row.get("pack") or "legacy"))
        row.setdefault("continuity_band", "v5")
        manifest_rows.append(row)
    new_manifest["systems"] = manifest_rows

    new_extension_catalog = deepcopy(old_extensions)
    new_extension_catalog["version"] = "v4"
    new_extension_catalog["generated_utc"] = now_iso()
    new_extension_catalog["description"] = "V6 extension catalog with 468 total entries."
    extension_rows = []
    for row in list(new_extension_catalog.get("extensions", [])):
        if not isinstance(row, dict):
            continue
        row = deepcopy(row)
        row.setdefault("live_dependency", "existing_surface")
        row.setdefault("history_scope", "v5")
        row.setdefault("mirror_target", "repo_only")
        row.setdefault("autonomy_class", "existing")
        extension_rows.append(row)
    new_extension_catalog["extensions"] = extension_rows

    new_mcp_catalog = deepcopy(old_mcp_catalog)
    new_mcp_catalog["version"] = "v4"
    new_mcp_catalog["generated_utc"] = now_iso()

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
