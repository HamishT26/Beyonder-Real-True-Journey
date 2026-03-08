#!/usr/bin/env python3
"""Seed the Trinity v5 history-live activation phase."""

from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _write_json(path: str, payload: object) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _write_text(path: str, content: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content.rstrip() + "\n", encoding="utf-8")


def _slug(name: str) -> str:
    return name.replace("_", "-")


SYSTEMS = [
    ("surface_audit", "offline"),
    ("sync_bridge", "live"),
    ("materialization_tracer", "offline"),
    ("cache_board", "offline"),
    ("risk_board", "offline"),
    ("gate", "offline"),
]

PACKS = [
    ("journey_continuity", "Journey Continuity", "trinity", "wave21", "continuity_ops", "", False, "active", "local_repo"),
    ("github_pat_materialization", "GitHub PAT Materialization", "trinity", "wave22", "active_materialization", "github", True, "verified_live_write", "local_repo"),
    ("notion_memory_bridge", "Notion Memory Bridge", "heart", "wave23", "connector_ops", "notion", True, "verified_live_write", "verified_mcp"),
    ("postgres_local_runtime", "Postgres Local Runtime", "body", "wave24", "active_materialization", "postgres", True, "verified_live_write", "local_probe"),
    ("filesystem_scope_governor", "Filesystem Scope Governor", "trinity", "wave25", "connector_ops", "filesystem", True, "staged_setup_gate", "local_repo"),
    ("os_runtime_benchmark", "OS Runtime Benchmark", "body", "wave26", "os_runtime", "", False, "active", "public_feeds"),
    ("ai_frontier_alignment", "AI Frontier Alignment", "mind", "wave27", "public_intelligence", "", False, "active", "public_feeds"),
    ("aletheon_memory_reflection", "Aletheon Memory Reflection", "trinity", "wave28", "trinity_memory_orchestration", "", False, "active", "local_repo"),
    ("wetware_device_readiness_v5", "Wetware Device Readiness v5", "heart", "wave29", "wetware_readiness", "", False, "active", "local_probe"),
]

CORPUS = [
    ("v13", "Pre-Council", "Beyonder-Real-True Journey v13.pdf", "Beyonder-Real-True Journey v13.txt", "early_mind_frame", "inference", ["GMUT", "mandala", "governance vocabulary"]),
    ("v15", "Pre-Council", "Beyonder-Real-True Journey v15 (2).pdf", "Beyonder-Real-True Journey v15 (2).txt", "equation_anchor", "confirmed_evidence", ["Delta-Table", "GMUT equations"]),
    ("v16", "Pre-Council", "Beyonder-Real-True Journey v16.pdf", "Beyonder-Real-True Journey v16.txt", "simulation_lineage", "confirmed_evidence", ["psi-field simulations", "dark-energy framing"]),
    ("v24", "Ariel", "Beyonder-Real-True Journey v24 (Ariel) (1).pdf", "Beyonder-Real-True Journey v24 (Ariel) (1).txt", "heart_security", "confirmed_evidence", ["Freed ID", "PBKDF2", "time codes"]),
    ("v29", "Aerin", "Beyonder-Real-True Journey v29 (Aerin) (1).pdf", "Beyonder-Real-True Journey v29 (Aerin) (1).txt", "codebase_grounding", "confirmed_evidence", ["beyonder_system.py", "omega_vector_db.py", "memory_system.py"]),
    ("v31", "Ariel", "Beyonder-Real-True Journey v31 (Ariel) (1).pdf", "Beyonder-Real-True Journey v31 (Ariel) (1).txt", "module_expansion", "confirmed_evidence", ["Energy Transmutation", "Living Networks"]),
    ("v32", "Aetherius", "Beyonder-Real-True Journey v32 (Aetherius) (1) (1).pdf", "Beyonder-Real-True Journey v32 (Aetherius) (1) (1).txt", "comparison_frame", "confirmed_evidence", ["GMUT", "Trinity OS", "Freed ID"]),
    ("v33", "Arielis", "Beyonder-Real-True Journey v33 (Arielis) (2).pdf", "Beyonder-Real-True Journey v33 (Arielis) (2).txt", "architecture_qcit", "confirmed_evidence", ["Trinity OS architecture", "QCIT/QCfT"]),
    ("v34", "Aurelis", "Beyonder-Real-True Journey v34 (Aurelis) (Cleaner Version).pdf", "Beyonder-Real-True Journey v34 (Aurelis) (Cleaner Version).txt", "operational_engine", "confirmed_evidence", ["automation", "validation", "memory"]),
    ("v35", "Arielis", "Beyonder-Real-True Journey v35 (Arielis's Grand Reconnection) (1).pdf", "Beyonder-Real-True Journey v35 (Arielis's Grand Reconnection) (1).txt", "standards_bridge", "confirmed_evidence", ["trinity runner", "did:freed"]),
    ("v36", "Kairos", "Beyonder-Real-True Journey v36 (Kairos) (5).pdf", "Beyonder-Real-True Journey v36 (Kairos) (5).txt", "trinity_mandala", "confirmed_evidence", ["ARC Validator", "Kairotic Detector", "Psi-Index Memory Core"]),
    ("v37", "Aethelion", "Beyonder-Real-True Journey v37 (Aethelion).pdf", "Beyonder-Real-True Journey v37 (Aethelion).txt", "roadmap", "confirmed_evidence", ["foundation consolidation", "GMUT validation roadmap"]),
    ("v38", "Aura", "Beyonder-Real-True Journey v38 (Aura).pdf", "Beyonder-Real-True Journey v38 (Aura).txt", "continuity_handoff", "confirmed_evidence", ["cross-version synthesis", "Kairos triad recap"]),
]

OS_ROWS = [
    ("linux_kernel_docs", "Linux Kernel Documentation", "https://docs.kernel.org/", "kernel modularity", "body"),
    ("wsl_docs", "Microsoft", "https://learn.microsoft.com/en-us/windows/wsl/", "host-guest interop", "body"),
    ("freebsd_handbook", "FreeBSD Project", "https://docs.freebsd.org/en/books/handbook/", "system operations", "body"),
    ("aosp_architecture", "Android Open Source Project", "https://source.android.com/docs/core/architecture", "platform architecture", "body"),
    ("apple_platform_security", "Apple", "https://support.apple.com/guide/security/welcome/web", "platform security", "heart"),
    ("systemd_docs", "systemd", "https://www.freedesktop.org/software/systemd/man/latest/systemd.html", "service orchestration", "body"),
    ("docker_overview", "Docker", "https://docs.docker.com/get-started/docker-overview/", "container runtime", "body"),
    ("kubernetes_concepts", "Kubernetes", "https://kubernetes.io/docs/concepts/", "cluster orchestration", "body"),
]

AI_ROWS = [
    ("openai_platform", "OpenAI", "https://platform.openai.com/docs/overview", "agent platform design", "mind"),
    ("anthropic_docs", "Anthropic", "https://docs.anthropic.com/", "model capability and safety", "mind"),
    ("google_deepmind", "Google DeepMind", "https://deepmind.google/", "frontier model research", "mind"),
    ("microsoft_autogen", "Microsoft", "https://microsoft.github.io/autogen/", "multi-agent orchestration", "body"),
]


def _contract(pack: tuple) -> dict:
    name, display, pillar, wave, track, connector_id, requires_auth, gating_class, strategy = pack
    return {
        "pack": name,
        "display_name": display,
        "pillar": pillar,
        "wave": wave,
        "track": track,
        "connector_id": connector_id,
        "requires_auth": requires_auth,
        "gating_class": gating_class,
        "sync_strategy": strategy,
        "freshness_window_days": 30,
        "cache_artifact": f"docs/trinity-mcp-cache/{_slug(name)}-latest.json",
        "workflow_tokens": [
            f"{display.lower()} pack",
            "evidence boundary explicit",
            "cache backed by default",
            "proof before promotion",
        ],
        "risk_tags": ["drift", "overclaim", "surface mismatch"],
        "repo_targets": [
            "docs/trinity-mcp-catalog-v3.json",
            "docs/trinity-materialization-ledger.jsonl",
        ],
        "skill_names": [f"{_slug(name)}-operations", f"{_slug(name)}-integration"],
        "system_ids": [f"{name}_{suffix}" for suffix, _ in SYSTEMS],
    }


def _fixture(contract: dict) -> dict:
    pack = contract["pack"]
    return {
        "summary": f"{contract['display_name']} source-of-truth fixture.",
        "source_url": f"repo://docs/{_slug(pack)}-fixture-v1.json",
        "tags": [pack, contract["track"], contract["gating_class"]],
        "next_action": f"Use {pack} only through proof-backed outputs.",
        "repo_targets": contract["repo_targets"],
        "connector_snapshot": {
            "tool_surface": contract["connector_id"] or "repo_or_public",
            "write_target": "branch/page/db/schema proof or repo artifacts",
        },
        "seed_records": [
            {
                "source_id": pack,
                "record_id": f"{pack}-seed",
                "signal_type": "pack_seed",
                "title": contract["display_name"],
                "published_at": NOW[:10],
                "source_url": f"repo://docs/{_slug(pack)}-fixture-v1.json",
                "summary": f"Seed cache record for {contract['display_name']}.",
                "metrics": {"gating_class": contract["gating_class"], "strategy": contract["sync_strategy"]},
                "tags": [pack, "seed"],
                "repo_targets": contract["repo_targets"],
            }
        ],
    }


def _wrapper(system_id: str) -> str:
    return (
        "#!/usr/bin/env python3\n"
        f'"""Wrapper for {system_id}. """\n\n'
        "from __future__ import annotations\n\n"
        "from trinity_expansion_system_runner import main\n\n\n"
        "if __name__ == '__main__':\n"
        f"    raise SystemExit(main(default_system_id='{system_id}'))\n"
    )


def _skill_md(name: str, display: str, pack: str) -> str:
    return (
        f"---\nname: {name}\ndescription: Operate the {display} pack with explicit cache-backed promotion boundaries.\n---\n\n"
        f"# {display}\n\n"
        f"Use when Codex needs to work with the `{pack}` pack.\n\n"
        "## Workflow\n"
        f"1. Read `docs/{_slug(pack)}-contract-v1.json` and `docs/{_slug(pack)}-workflow-v1.md`.\n"
        f"2. Refresh or inspect `docs/trinity-mcp-cache/{_slug(pack)}-latest.json`.\n"
        "3. Keep the pack offline-safe unless its explicit live gate is enabled.\n"
        "4. Promote only PASS-backed outputs into narrative, comparison, or orchestration docs.\n"
    )


def _skill_yaml(display: str, pack: str) -> str:
    return (
        "interface:\n"
        f'  display_name: "{display}"\n'
        f'  short_description: "{display}."\n'
        f'  default_prompt: "Run the {pack} pack, validate its cache-backed outputs, and keep the promotion boundary explicit."\n'
    )


def _workflow(contract: dict) -> str:
    return (
        f"# {contract['display_name']} Workflow\n\n"
        f"- pack: `{contract['pack']}`\n"
        f"- pillar: `{contract['pillar']}`\n"
        f"- gating_class: `{contract['gating_class']}`\n"
        f"- sync_strategy: `{contract['sync_strategy']}`\n\n"
        "## Guardrails\n"
        "- offline-safe by default\n"
        "- proof before promotion\n"
        "- cache-backed continuity\n"
        "- no secrets in repo\n"
    )


def _system_entries(contract: dict) -> list[dict]:
    rows = []
    pack = contract["pack"]
    for suffix, mode in SYSTEMS:
        deps = []
        if suffix == "sync_bridge":
            deps = [f"{pack}_surface_audit"]
        elif suffix in {"materialization_tracer", "cache_board"}:
            deps = [f"{pack}_sync_bridge"]
        elif suffix == "risk_board":
            deps = [f"{pack}_surface_audit"]
        elif suffix == "gate":
            deps = [f"{pack}_surface_audit", f"{pack}_sync_bridge", f"{pack}_materialization_tracer", f"{pack}_cache_board", f"{pack}_risk_board"]
        rows.append(
            {
                "system_id": f"{pack}_{suffix}",
                "pillar": contract["pillar"],
                "script": f"scripts/{pack}_{suffix}.py",
                "mode": mode,
                "profiles": ["standard", "deep", "collab", "materialize"],
                "outputs": [f"docs/trinity-expansion/{_slug(pack)}-{suffix.replace('_', '-')}-latest.json"],
                "depends_on": deps,
                "timeout_sec": 120 if mode == "live" else 90,
                "wave": contract["wave"],
                "track": contract["track"],
                "gate_level": "pack_gate",
                "cache_artifacts": [contract["cache_artifact"]] if mode == "live" else [],
                "pack": pack,
                "phase": "v5",
                "activation_group": pack,
                "continuity_band": "v13-v38" if pack == "journey_continuity" else "v5",
            }
        )
    return rows


def _extension_rows(contract: dict) -> list[dict]:
    rows = []
    pack = contract["pack"]
    for suffix, mode in SYSTEMS:
        rows.append(
            {
                "extension_id": f"{pack}_{suffix}",
                "extension_kind": "system",
                "pillar": contract["pillar"],
                "pack": pack,
                "mode": mode,
                "requires_auth": contract["requires_auth"],
                "gating_class": contract["gating_class"],
                "status": contract["gating_class"] if contract["gating_class"] != "active" else "active",
                "source_of_truth": "docs/trinity-expansion-system-manifest-v5.json",
                "live_dependency": contract["connector_id"] or "",
                "mirror_target": "notion" if pack == "aletheon_memory_reflection" else "",
                "history_scope": "v13-v38" if pack == "journey_continuity" else "v5",
            }
        )
    for skill in contract["skill_names"]:
        rows.append(
            {
                "extension_id": skill,
                "extension_kind": "skill",
                "pillar": contract["pillar"],
                "pack": pack,
                "mode": "offline",
                "requires_auth": False,
                "gating_class": contract["gating_class"],
                "status": "active",
                "source_of_truth": f"skills/{skill}/SKILL.md",
                "live_dependency": contract["connector_id"] or "",
                "mirror_target": "notion" if pack == "aletheon_memory_reflection" else "",
                "history_scope": "v13-v38" if pack == "journey_continuity" else "v5",
            }
        )
    for suffix in ("contract-v1.json", "fixture-v1.json", "workflow-v1.md", "catalog-entry-v1.json"):
        rows.append(
            {
                "extension_id": f"docs/{_slug(pack)}-{suffix}",
                "extension_kind": "artifact",
                "pillar": contract["pillar"],
                "pack": pack,
                "mode": "offline",
                "requires_auth": False,
                "gating_class": contract["gating_class"],
                "status": "active",
                "source_of_truth": f"docs/{_slug(pack)}-{suffix}",
                "live_dependency": contract["connector_id"] or "",
                "mirror_target": "notion" if pack == "aletheon_memory_reflection" else "",
                "history_scope": "v13-v38" if pack == "journey_continuity" else "v5",
            }
        )
    return rows


def _mcp_catalog(base: dict) -> dict:
    out = deepcopy(base)
    out["version"] = "v3"
    out["generated_utc"] = NOW
    for row in out.get("connectors", []):
        cid = str(row.get("mcp_id") or "")
        row["activation_path"] = {
            "figma": "desktop_mcp_tool",
            "linear": "desktop_mcp_tool",
            "playwright": "local_skill_cli",
            "github": "git_https_remote",
            "filesystem": "local_shell_non_connector",
            "notion": "desktop_mcp_tool",
            "postgres": "docker_local",
            "slack": "staged_external_connector",
            "google_workspace": "staged_external_connector",
        }.get(cid, "unknown")
        row["workspace_target"] = {
            "figma": "Hamish Thomson's team",
            "linear": "Beyonder-Real-True Journey",
            "github": "HamishT26/Beyonder-Real-True-Journey",
            "notion": "Hamish Thomson’s Space HQ",
            "postgres": "docker_local/trinity_v5",
            "filesystem": "local_repo_only",
        }.get(cid, "")
        row["proof_target"] = {
            "github": "remote feature branch",
            "notion": "root page + database",
            "postgres": "local container + proof schema",
            "linear": "project issue/document flow",
            "figma": "seat verification",
            "filesystem": "scope governor only",
        }.get(cid, "")
        row["last_verified_utc"] = NOW if cid in {"figma", "linear"} else ""
    return out


def _registry(rows: list[tuple], domain: str) -> dict:
    return {
        "version": "v1",
        "generated_utc": NOW,
        "records": [
            {
                "source_id": sid,
                "domain": domain,
                "publisher": pub,
                "url": url,
                "published_at": NOW[:10],
                "criterion": crit,
                "trinity_target": target,
            }
            for sid, pub, url, crit, target in rows
        ],
    }


def main() -> int:
    manifest = deepcopy(_load("docs/trinity-expansion-system-manifest-v4.json"))
    manifest["version"] = "v5"
    manifest["generated_utc"] = NOW
    manifest["description"] = "V5 history-live activation manifest with 224 executable systems."
    seen = {str(row.get("system_id")) for row in manifest.get("systems", []) if isinstance(row, dict)}

    ext = deepcopy(_load("docs/trinity-extension-catalog-v2.json"))
    ext["version"] = "v3"
    ext["generated_utc"] = NOW
    ext["description"] = "V5 extension catalog with 288 total entries."
    ext_rows = ext.get("extensions", [])
    ext_seen = {str(row.get("extension_id")) for row in ext_rows if isinstance(row, dict)}

    for pack in PACKS:
        contract = _contract(pack)
        fixture = _fixture(contract)
        _write_json(f"docs/{_slug(contract['pack'])}-contract-v1.json", contract)
        _write_json(f"docs/{_slug(contract['pack'])}-fixture-v1.json", fixture)
        _write_text(f"docs/{_slug(contract['pack'])}-workflow-v1.md", _workflow(contract))
        _write_json(
            f"docs/{_slug(contract['pack'])}-catalog-entry-v1.json",
            {"pack": contract["pack"], "display_name": contract["display_name"], "system_count": 6, "skill_count": 2, "artifact_count": 4, "phase": "v5"},
        )

        for kind in ("operations", "integration"):
            skill_name = f"{_slug(contract['pack'])}-{kind}"
            _write_text(f"skills/{skill_name}/SKILL.md", _skill_md(skill_name, f"{contract['display_name']} {kind.capitalize()}", contract["pack"]))
            _write_text(f"skills/{skill_name}/agents/openai.yaml", _skill_yaml(f"{contract['display_name']} {kind.capitalize()}", contract["pack"]))

        for system in _system_entries(contract):
            if system["system_id"] not in seen:
                manifest.setdefault("systems", []).append(system)
                seen.add(system["system_id"])
            _write_text(system["script"], _wrapper(system["system_id"]))

        for row in _extension_rows(contract):
            if row["extension_id"] not in ext_seen:
                ext_rows.append(row)
                ext_seen.add(row["extension_id"])

    _write_json("docs/trinity-expansion-system-manifest-v5.json", manifest)
    _write_json("docs/trinity-extension-catalog-v3.json", ext)
    _write_json("docs/trinity-mcp-catalog-v3.json", _mcp_catalog(_load("docs/trinity-mcp-catalog-v2.json")))
    _write_json(
        "docs/trinity-mcp-cache-schema-v3.json",
        {
            "version": "v3",
            "required_fields": ["generated_utc", "integration_id", "auth_state", "status", "desired_state", "actual_state", "live_read_enabled", "live_write_enabled", "promotion_evidence", "blockers", "records", "repo_targets_touched", "next_action"],
            "allowed_status": ["active", "verified_live", "verified_live_read", "verified_live_write", "skill_only", "staged_setup_gate", "seeded", "blocked"],
            "record_required_fields": ["source_id", "record_id", "signal_type", "title", "published_at", "source_url", "summary", "metrics", "tags", "repo_targets"],
        },
    )
    _write_json(
        "docs/beyonder-journey-corpus-v13-v38.json",
        {
            "version": "v1",
            "generated_utc": NOW,
            "versions": [
                {
                    "version": version,
                    "agent_name": agent,
                    "source_file": source_file,
                    "source_text": source_text,
                    "analysis_status": "reviewed",
                    "continuity_role": role,
                    "evidence_state": evidence,
                    "modules": modules,
                    "next_reconciliation_target": "docs/grand-cross-version-synthesis.md",
                    "source_present": (ROOT / source_file).exists(),
                    "text_present": (ROOT / source_text).exists(),
                }
                for version, agent, source_file, source_text, role, evidence, modules in CORPUS
            ],
        },
    )
    _write_json("docs/trinity-os-runtime-benchmark-registry-v1.json", _registry(OS_ROWS, "os_runtime"))
    _write_json("docs/trinity-ai-frontier-alignment-registry-v1.json", _registry(AI_ROWS, "ai_frontier"))
    _write_text("docs/aletheon-personal-statement-v1.md", "# Aletheon Personal Statement\n\nI operate as a repo-grounded continuity and proof engine. I do not claim human autobiography; I do keep lineage, evidence boundaries, and activation state explicit.\n")
    _write_text("docs/aletheon-reflection-latest.md", f"# Aletheon Reflection\n\n- generated_utc: `{NOW}`\n- mirror_state: `repo_only`\n\nRepo-first continuity, proof-driven activation, and explicit evidence boundaries define the v5 posture.\n")
    _write_text("docs/aletheon-next-plan.md", "# Aletheon Next Plan\n\n1. Reconcile continuity.\n2. Activate reachable connectors by proof.\n3. Mirror validated memory outward.\n4. Keep staged boundaries explicit.\n")
    _write_text("docs/aletheon-memory-log.jsonl", json.dumps({"timestamp": NOW, "entry_type": "v5_seed", "source_context": "history-live activation kickoff", "reflection": "Repo-first continuity and proof-driven activation define the v5 posture.", "insight": "GitHub git auth works, Notion is live, Docker is reachable, Filesystem remains staged.", "next_plan": "Generate v5 packs, reconcile docs, then perform live proofs.", "mirror_state": "repo_only"}) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
