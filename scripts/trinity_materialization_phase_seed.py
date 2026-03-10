#!/usr/bin/env python3
"""Seed the Trinity active materialization phase artifacts."""

from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


PACKS = [
    {
        "pack": "github_materialization",
        "display_name": "GitHub Materialization",
        "pillar": "trinity",
        "wave": "wave15",
        "track": "active_materialization",
        "connector_id": "github",
        "requires_auth": True,
        "gating_class": "staged_setup_gate",
        "sync_strategy": "staged_connector",
        "workflow_tokens": [
            "materialize profile only",
            "disposable branch tracer",
            "read handshake before write",
            "never target main",
        ],
        "risk_tags": ["token exposure", "branch mutation", "repo drift"],
        "repo_targets": [
            "docs/trinity-mcp-catalog-v2.json",
            "docs/trinity-materialization-ledger.jsonl",
            "docs/system-suite-status.json",
        ],
        "skill_desc": "Operate the GitHub Materialization pack with disposable write tracers and explicit promotion proof boundaries.",
        "fixture": {
            "summary": "GitHub materialization stays staged until auth, tool surface, safe read handshake, and disposable write tracer all pass.",
            "source_url": "https://api.github.com/repos/HamishT26/Beyonder-Real-True-Journey",
            "tags": ["github", "materialization", "staged_setup_gate"],
            "next_action": "Keep GitHub staged until auth, tool surface, read handshake, and disposable write tracer all pass.",
            "repo_targets": [
                "docs/trinity-mcp-catalog-v2.json",
                "docs/trinity-materialization-ledger.jsonl",
            ],
            "connector_snapshot": {
                "tool_surface": "public_rest_plus_optional_auth",
                "write_target": "disposable branch + docs/trinity-live-test.md",
                "branch_policy": "never target main",
            },
        },
    },
    {
        "pack": "filesystem_materialization",
        "display_name": "Filesystem Materialization",
        "pillar": "trinity",
        "wave": "wave16",
        "track": "active_materialization",
        "connector_id": "filesystem",
        "requires_auth": True,
        "gating_class": "staged_setup_gate",
        "sync_strategy": "staged_connector",
        "workflow_tokens": [
            "materialize profile only",
            "scoped connector required",
            "local shell is not mcp promotion",
            "write tracer must stay disposable",
        ],
        "risk_tags": ["scope overreach", "filesystem mutation", "connector confusion"],
        "repo_targets": [
            "docs/trinity-mcp-catalog-v2.json",
            "docs/trinity-materialization-ledger.jsonl",
        ],
        "skill_desc": "Operate the Filesystem Materialization pack with explicit connector/tool-surface proof boundaries.",
        "fixture": {
            "summary": "Filesystem materialization is blocked until a distinct scoped connector surface exists; local shell access does not count.",
            "source_url": "connector://filesystem/setup-gate",
            "tags": ["filesystem", "materialization", "staged_setup_gate"],
            "next_action": "Keep Filesystem staged until a verified connector surface and a disposable tracer both exist.",
            "repo_targets": [
                "docs/trinity-mcp-catalog-v2.json",
                "docs/trinity-materialization-ledger.jsonl",
            ],
            "connector_snapshot": {
                "tool_surface": "connector_setup_gate",
                "write_target": "scoped disposable sandbox only",
                "note": "Local shell access is not MCP promotion.",
            },
        },
    },
    {
        "pack": "notion_materialization",
        "display_name": "Notion Materialization",
        "pillar": "heart",
        "wave": "wave17",
        "track": "active_materialization",
        "connector_id": "notion",
        "requires_auth": True,
        "gating_class": "staged_setup_gate",
        "sync_strategy": "staged_connector",
        "workflow_tokens": [
            "materialize profile only",
            "token and read handshake first",
            "disposable staging page only",
            "no secrets in repo",
        ],
        "risk_tags": ["token exposure", "workspace mutation", "knowledge drift"],
        "repo_targets": [
            "docs/trinity-mcp-catalog-v2.json",
            "docs/trinity-materialization-ledger.jsonl",
        ],
        "skill_desc": "Operate the Notion Materialization pack with staged page and database tracers and explicit credential gates.",
        "fixture": {
            "summary": "Notion materialization remains staged until token, safe read handshake, and disposable page or database tracer all pass.",
            "source_url": "https://www.notion.so/help/guides/what-is-notion",
            "tags": ["notion", "materialization", "staged_setup_gate"],
            "next_action": "Keep Notion staged until token, read handshake, and disposable tracer all pass.",
            "repo_targets": [
                "docs/trinity-mcp-catalog-v2.json",
                "docs/trinity-materialization-ledger.jsonl",
            ],
            "connector_snapshot": {
                "tool_surface": "connector_setup_gate",
                "write_target": "disposable staging page/database",
                "auth_state": "token_required",
            },
        },
    },
    {
        "pack": "postgres_materialization",
        "display_name": "Postgres Materialization",
        "pillar": "body",
        "wave": "wave18",
        "track": "active_materialization",
        "connector_id": "postgres",
        "requires_auth": True,
        "gating_class": "staged_setup_gate",
        "sync_strategy": "staged_connector",
        "workflow_tokens": [
            "materialize profile only",
            "dsn and read handshake first",
            "disposable test schema only",
            "no production mutation",
        ],
        "risk_tags": ["dsn exposure", "schema mutation", "data drift"],
        "repo_targets": [
            "docs/trinity-mcp-catalog-v2.json",
            "docs/trinity-materialization-ledger.jsonl",
        ],
        "skill_desc": "Operate the Postgres Materialization pack with disposable schema tracers and explicit DSN gates.",
        "fixture": {
            "summary": "Postgres materialization remains staged until DSN, safe read handshake, and disposable schema tracer all pass.",
            "source_url": "https://www.postgresql.org/docs/current/index.html",
            "tags": ["postgres", "materialization", "staged_setup_gate"],
            "next_action": "Keep Postgres staged until DSN, read handshake, and disposable schema tracer all pass.",
            "repo_targets": [
                "docs/trinity-mcp-catalog-v2.json",
                "docs/trinity-materialization-ledger.jsonl",
            ],
            "connector_snapshot": {
                "tool_surface": "connector_setup_gate",
                "write_target": "disposable test schema/table",
                "auth_state": "dsn_required",
            },
        },
    },
    {
        "pack": "os_runtime_fabric",
        "display_name": "OS Runtime Fabric",
        "pillar": "body",
        "wave": "wave19",
        "track": "os_runtime",
        "connector_id": "",
        "requires_auth": False,
        "gating_class": "active",
        "sync_strategy": "public_feeds",
        "workflow_tokens": [
            "official sources only",
            "cache-backed by default",
            "no auto-promotion of claims",
            "pattern registry first",
        ],
        "risk_tags": ["vendor bias", "staleness", "pattern overreach"],
        "repo_targets": [
            "docs/trinity-os-runtime-reference-registry-v1.json",
            "docs/comparative-validation-grid-v1.md",
            "docs/grand-unified-narrative-brief.md",
        ],
        "skill_desc": "Operate the OS Runtime Fabric pack from official operating-system and runtime references with cache-backed pattern boards.",
        "fixture": {
            "summary": "Official OS/runtime reference fabric curated from Linux, WSL, FreeBSD, Android, Apple, systemd, Docker, and Kubernetes sources.",
            "source_url": "https://docs.kernel.org/",
            "tags": ["os_runtime", "official_sources", "active"],
            "next_action": "Refresh official-source runtime patterns before promoting any architectural comparison language.",
            "repo_targets": [
                "docs/trinity-os-runtime-reference-registry-v1.json",
                "docs/comparative-validation-grid-v1.md",
                "docs/grand-unified-narrative-brief.md",
            ],
            "seed_records": [
                {
                    "source_id": "linux_kernel_docs",
                    "record_id": "linux-kernel-docs",
                    "signal_type": "os_runtime_pattern",
                    "title": "Linux kernel documentation",
                    "published_at": "2026-03-07",
                    "source_url": "https://docs.kernel.org/",
                    "summary": "Reference corpus for Linux kernel subsystems, interfaces, and operational patterns.",
                    "metrics": {"os_family": "linux", "layer": "kernel"},
                    "tags": ["linux", "kernel", "official"],
                    "repo_relevance": {"targets": ["docs/trinity-os-runtime-reference-registry-v1.json", "docs/comparative-validation-grid-v1.md"]}
                },
                {
                    "source_id": "wsl_docs",
                    "record_id": "wsl-docs",
                    "signal_type": "os_runtime_pattern",
                    "title": "Windows Subsystem for Linux documentation",
                    "published_at": "2026-03-07",
                    "source_url": "https://learn.microsoft.com/en-us/windows/wsl/",
                    "summary": "Reference corpus for Windows-hosted Linux interop and developer workflow design.",
                    "metrics": {"os_family": "windows", "layer": "interop"},
                    "tags": ["windows", "wsl", "official"],
                    "repo_relevance": {"targets": ["docs/trinity-os-runtime-reference-registry-v1.json", "docs/grand-unified-narrative-brief.md"]}
                },
                {
                    "source_id": "freebsd_handbook",
                    "record_id": "freebsd-handbook",
                    "signal_type": "os_runtime_pattern",
                    "title": "FreeBSD Handbook",
                    "published_at": "2026-03-07",
                    "source_url": "https://docs.freebsd.org/en/books/handbook/",
                    "summary": "Operational reference for FreeBSD system administration, networking, storage, and release practices.",
                    "metrics": {"os_family": "freebsd", "layer": "system"},
                    "tags": ["freebsd", "handbook", "official"],
                    "repo_relevance": {"targets": ["docs/trinity-os-runtime-reference-registry-v1.json"]}
                }
            ],
            "live_sources": [
                {"source_id": "linux_kernel_docs", "url": "https://docs.kernel.org/", "title": "Linux kernel docs", "summary": "Live Linux kernel docs availability check.", "tags": ["linux", "kernel"], "repo_targets": ["docs/trinity-os-runtime-reference-registry-v1.json"]},
                {"source_id": "wsl_docs", "url": "https://learn.microsoft.com/en-us/windows/wsl/", "title": "WSL docs", "summary": "Live WSL docs availability check.", "tags": ["windows", "wsl"], "repo_targets": ["docs/trinity-os-runtime-reference-registry-v1.json"]},
                {"source_id": "freebsd_handbook", "url": "https://docs.freebsd.org/en/books/handbook/", "title": "FreeBSD handbook", "summary": "Live FreeBSD handbook availability check.", "tags": ["freebsd"], "repo_targets": ["docs/trinity-os-runtime-reference-registry-v1.json"]},
                {"source_id": "aosp_architecture", "url": "https://source.android.com/docs/core/architecture", "title": "AOSP architecture", "summary": "Live Android architecture docs availability check.", "tags": ["android", "aosp"], "repo_targets": ["docs/trinity-os-runtime-reference-registry-v1.json"]},
                {"source_id": "apple_platform_security", "url": "https://support.apple.com/guide/security/welcome/web", "title": "Apple Platform Security", "summary": "Live Apple platform security docs availability check.", "tags": ["apple", "security"], "repo_targets": ["docs/trinity-os-runtime-reference-registry-v1.json"]},
                {"source_id": "systemd_docs", "url": "https://www.freedesktop.org/software/systemd/man/latest/systemd.html", "title": "systemd docs", "summary": "Live systemd docs availability check.", "tags": ["systemd"], "repo_targets": ["docs/trinity-os-runtime-reference-registry-v1.json"]},
                {"source_id": "docker_overview", "url": "https://docs.docker.com/get-started/docker-overview/", "title": "Docker overview", "summary": "Live Docker docs availability check.", "tags": ["docker"], "repo_targets": ["docs/trinity-os-runtime-reference-registry-v1.json"]},
                {"source_id": "kubernetes_concepts", "url": "https://kubernetes.io/docs/concepts/", "title": "Kubernetes concepts", "summary": "Live Kubernetes docs availability check.", "tags": ["kubernetes"], "repo_targets": ["docs/trinity-os-runtime-reference-registry-v1.json"]}
            ]
        },
    },
    {
        "pack": "wetware_device_readiness",
        "display_name": "Wetware Device Readiness",
        "pillar": "heart",
        "wave": "wave20",
        "track": "wetware_readiness",
        "connector_id": "",
        "requires_auth": False,
        "gating_class": "active",
        "sync_strategy": "local_repo",
        "workflow_tokens": [
            "device-ready only",
            "no live biometric ingestion",
            "explicit consent boundary",
            "non-clinical advisory only",
        ],
        "risk_tags": ["privacy overreach", "health inference", "device mismatch"],
        "repo_targets": [
            "docs/grand-unified-narrative-brief.md",
            "docs/comparative-validation-grid-v1.md",
            "docs/trinity-materialization-ledger.jsonl",
        ],
        "skill_desc": "Operate the Wetware Device Readiness pack with device-ready schemas, adapters, and continuity boards while keeping live biometrics out of scope.",
        "fixture": {
            "summary": "Device-ready wetware pack covering schemas, adapters, continuity rituals, and operator safeguards without live biometric ingestion.",
            "source_url": "repo://wetware/device-readiness",
            "tags": ["wetware", "device_ready", "active"],
            "next_action": "Keep wetware work device-ready and consent-bound until a separate live-data governance phase exists.",
            "repo_targets": [
                "docs/grand-unified-narrative-brief.md",
                "docs/comparative-validation-grid-v1.md",
                "docs/trinity-materialization-ledger.jsonl",
            ],
            "seed_records": [
                {
                    "source_id": "wetware_schema",
                    "record_id": "wetware-schema",
                    "signal_type": "device_readiness_pattern",
                    "title": "Wetware schema boundary",
                    "published_at": "2026-03-07",
                    "source_url": "repo://wetware/schema",
                    "summary": "Schema boundary for future wearable and biometrics adapters with explicit consent and non-clinical scope.",
                    "metrics": {"device_ready": True, "live_ingestion": False},
                    "tags": ["wetware", "schema", "device_ready"],
                    "repo_relevance": {"targets": ["docs/comparative-validation-grid-v1.md", "docs/grand-unified-narrative-brief.md"]}
                }
            ]
        },
    },
]

SUFFIXES = [
    ("surface_audit", "offline"),
    ("sync_bridge", "live"),
    ("materialization_tracer", "live"),
    ("cache_board", "offline"),
    ("risk_board", "offline"),
    ("gate", "offline"),
]


def build_manifest_v4() -> None:
    manifest_v3 = json.loads((ROOT / "docs/trinity-expansion-system-manifest-v3.json").read_text(encoding="utf-8"))
    manifest_v4 = deepcopy(manifest_v3)
    manifest_v4["version"] = "v4"
    manifest_v4["generated_utc"] = NOW
    manifest_v4["description"] = "Active materialization Trinity expansion manifest for 170 executable systems."

    for entry in manifest_v4.get("systems", []):
        if isinstance(entry, dict):
            profiles = entry.get("profiles", [])
            if isinstance(profiles, list) and "materialize" not in profiles:
                entry["profiles"] = profiles + ["materialize"]

    for pack in PACKS:
        for suffix, default_mode in SUFFIXES:
            pack_name = pack["pack"]
            system_id = f"{pack_name}_{suffix}"
            hyphen_pack = pack_name.replace("_", "-")
            gate_level = "support"
            if suffix == "surface_audit":
                depends_on = [f"docs/{hyphen_pack}-contract-v1.json", f"docs/{hyphen_pack}-fixture-v1.json"]
            elif suffix == "sync_bridge":
                depends_on = [f"{pack_name}_surface_audit"]
            elif suffix == "materialization_tracer":
                depends_on = [f"{pack_name}_sync_bridge"]
            elif suffix == "cache_board":
                depends_on = [f"{pack_name}_sync_bridge", "docs/trinity-mcp-cache-schema-v2.json"]
            elif suffix == "risk_board":
                depends_on = [f"{pack_name}_surface_audit"]
            else:
                depends_on = [
                    f"{pack_name}_surface_audit",
                    f"{pack_name}_sync_bridge",
                    f"{pack_name}_materialization_tracer",
                    f"{pack_name}_cache_board",
                    f"{pack_name}_risk_board",
                ]
                gate_level = "pack_gate"

            cache_artifacts = [f"docs/trinity-mcp-cache/{hyphen_pack}-latest.json"]
            if suffix == "materialization_tracer":
                cache_artifacts.append("docs/trinity-materialization-ledger.jsonl")
            if pack_name == "os_runtime_fabric":
                cache_artifacts.append("docs/trinity-os-runtime-reference-registry-v1.json")

            mode = default_mode
            if suffix in {"surface_audit", "cache_board", "risk_board", "gate"}:
                mode = "offline"
            if pack_name == "wetware_device_readiness" and suffix == "sync_bridge":
                mode = "offline"

            manifest_v4["systems"].append(
                {
                    "system_id": system_id,
                    "pillar": pack["pillar"],
                    "script": f"scripts/{system_id}.py",
                    "mode": mode,
                    "profiles": ["standard", "deep", "collab", "materialize"],
                    "outputs": [f"docs/trinity-expansion/{system_id.replace('_', '-')}-latest.json"],
                    "depends_on": depends_on,
                    "timeout_sec": 90,
                    "wave": pack["wave"],
                    "track": pack["track"],
                    "gate_level": gate_level,
                    "cache_artifacts": sorted(set(cache_artifacts)),
                    "pack": pack_name,
                }
            )

    write_json(ROOT / "docs/trinity-expansion-system-manifest-v4.json", manifest_v4)


def build_extension_catalog_v2() -> None:
    ext_v1 = json.loads((ROOT / "docs/trinity-extension-catalog-v1.json").read_text(encoding="utf-8"))
    ext_v2 = deepcopy(ext_v1)
    ext_v2["version"] = "v2"
    ext_v2["generated_utc"] = NOW
    ext_v2["description"] = "Extension catalog for the Trinity active materialization phase with 180 total extensions."
    for entry in ext_v2.get("extensions", []):
        if isinstance(entry, dict) and entry.get("extension_kind") == "system":
            entry["source_of_truth"] = "docs/trinity-expansion-system-manifest-v4.json"

    for pack in PACKS:
        pack_name = pack["pack"]
        hyphen_pack = pack_name.replace("_", "-")
        status = "active" if pack["gating_class"] == "active" else pack["gating_class"]
        for suffix, default_mode in SUFFIXES:
            mode = default_mode
            if suffix in {"surface_audit", "cache_board", "risk_board", "gate"}:
                mode = "offline"
            if pack_name == "wetware_device_readiness" and suffix == "sync_bridge":
                mode = "offline"
            ext_v2["extensions"].append(
                {
                    "extension_id": f"{pack_name}_{suffix}",
                    "extension_kind": "system",
                    "pillar": pack["pillar"],
                    "pack": pack_name,
                    "mode": mode,
                    "requires_auth": pack["requires_auth"],
                    "gating_class": pack["gating_class"],
                    "status": status,
                    "source_of_truth": "docs/trinity-expansion-system-manifest-v4.json",
                }
            )

        for suffix in ("operations", "integration"):
            skill_id = f"{hyphen_pack}-{suffix}"
            ext_v2["extensions"].append(
                {
                    "extension_id": skill_id,
                    "extension_kind": "skill",
                    "pillar": pack["pillar"],
                    "pack": pack_name,
                    "mode": "offline",
                    "requires_auth": False,
                    "gating_class": pack["gating_class"],
                    "status": "active",
                    "source_of_truth": f"skills/{skill_id}/SKILL.md",
                }
            )

        for artifact in (
            f"docs/{hyphen_pack}-contract-v1.json",
            f"docs/{hyphen_pack}-fixture-v1.json",
            f"docs/{hyphen_pack}-workflow-v1.md",
            f"docs/{hyphen_pack}-catalog-entry-v1.json",
        ):
            ext_v2["extensions"].append(
                {
                    "extension_id": artifact,
                    "extension_kind": "artifact",
                    "pillar": pack["pillar"],
                    "pack": pack_name,
                    "mode": "offline",
                    "requires_auth": False,
                    "gating_class": pack["gating_class"],
                    "status": "active",
                    "source_of_truth": artifact,
                }
            )

    write_json(ROOT / "docs/trinity-extension-catalog-v2.json", ext_v2)


def build_mcp_catalog_v2() -> None:
    mcp_v1 = json.loads((ROOT / "docs/trinity-mcp-catalog-v1.json").read_text(encoding="utf-8"))
    desired_state_map = {
        "figma": "verified_live_read",
        "linear": "verified_live_write",
        "playwright": "skill_only",
        "github": "verified_live_write",
        "filesystem": "verified_live_write",
        "notion": "verified_live_write",
        "slack": "staged_setup_gate",
        "google_workspace": "staged_setup_gate",
        "postgres": "verified_live_write",
    }
    blockers_map = {
        "figma": ["Figma seat is View; write actions stay disabled in this phase."],
        "linear": ["Live write promotion requires disposable issue, comment, and document tracer proof."],
        "playwright": ["No direct Playwright MCP tool surface is exposed in-session."],
        "github": ["No GitHub token or gh auth is exposed on this machine.", "No disposable tracer proof exists yet."],
        "filesystem": ["No distinct scoped filesystem connector or tool surface is exposed."],
        "notion": ["No Notion token is exposed.", "No safe read handshake is available."],
        "slack": ["No Slack token is exposed."],
        "google_workspace": ["No Google Workspace credentials are exposed."],
        "postgres": ["No Postgres DSN is exposed.", "No disposable schema tracer proof exists yet."],
    }
    v2 = {"version": "v2", "generated_utc": NOW, "connectors": []}
    for entry in mcp_v1.get("connectors", []):
        if not isinstance(entry, dict):
            continue
        connector_id = str(entry.get("mcp_id") or "")
        actual_state = {
            "figma": "verified_live_read",
            "linear": "verified_live_read",
            "playwright": "skill_only",
        }.get(connector_id, str(entry.get("status") or "absent"))
        row = deepcopy(entry)
        row.update(
            {
                "desired_state": desired_state_map.get(connector_id, str(entry.get("status") or "absent")),
                "actual_state": actual_state,
                "live_read_enabled": connector_id in {"figma", "linear"},
                "live_write_enabled": False,
                "promotion_evidence": [],
                "blockers": blockers_map.get(connector_id, []),
            }
        )
        v2["connectors"].append(row)
    write_json(ROOT / "docs/trinity-mcp-catalog-v2.json", v2)


def build_cache_schema_v2() -> None:
    write_json(
        ROOT / "docs/trinity-mcp-cache-schema-v2.json",
        {
            "version": "v2",
            "required_fields": [
                "generated_utc",
                "integration_id",
                "auth_state",
                "status",
                "desired_state",
                "actual_state",
                "live_read_enabled",
                "live_write_enabled",
                "promotion_evidence",
                "blockers",
                "records",
                "repo_targets_touched",
                "next_action",
            ],
            "allowed_status": [
                "active",
                "verified_live",
                "verified_live_read",
                "verified_live_write",
                "skill_only",
                "staged_setup_gate",
                "seeded",
                "blocked",
            ],
            "record_required_fields": [
                "source_id",
                "record_id",
                "signal_type",
                "title",
                "published_at",
                "source_url",
                "summary",
                "metrics",
                "tags",
                "repo_targets",
            ],
        },
    )


def build_supporting_docs() -> None:
    ledger = ROOT / "docs/trinity-materialization-ledger.jsonl"
    if not ledger.exists():
        ledger.parent.mkdir(parents=True, exist_ok=True)
        ledger.write_text("", encoding="utf-8")
    write_json(
        ROOT / "docs/trinity-materialization-ledger-schema-v1.json",
        {
            "version": "v1",
            "required_fields": [
                "connector_id",
                "operation",
                "target",
                "mode",
                "result",
                "timestamp",
                "evidence_artifact",
            ],
            "allowed_results": ["PASS", "WARN", "FAIL", "SKIP", "BLOCKED"],
        },
    )
    write_json(
        ROOT / "docs/trinity-os-runtime-reference-registry-v1.json",
        {
            "version": "v1",
            "generated_utc": NOW,
            "description": "Official-source operating system and runtime reference registry for the OS Runtime Fabric pack.",
            "sources": [
                {"source_id": "linux_kernel_docs", "os_family": "linux", "layer": "kernel", "publisher": "Linux Kernel Documentation", "url": "https://docs.kernel.org/", "published_at": "2026-03-07", "pattern": "Kernel subsystem and interface reference", "trinity_target": "body"},
                {"source_id": "wsl_docs", "os_family": "windows", "layer": "interop", "publisher": "Microsoft Learn", "url": "https://learn.microsoft.com/en-us/windows/wsl/", "published_at": "2026-03-07", "pattern": "Windows-Linux interoperability and developer environment guidance", "trinity_target": "body"},
                {"source_id": "freebsd_handbook", "os_family": "freebsd", "layer": "system", "publisher": "FreeBSD Documentation Project", "url": "https://docs.freebsd.org/en/books/handbook/", "published_at": "2026-03-07", "pattern": "Operational system handbook and release discipline", "trinity_target": "body"},
                {"source_id": "aosp_architecture", "os_family": "android", "layer": "platform", "publisher": "Android Open Source Project", "url": "https://source.android.com/docs/core/architecture", "published_at": "2026-03-07", "pattern": "Platform architecture and service-layer patterns", "trinity_target": "body"},
                {"source_id": "apple_platform_security", "os_family": "apple", "layer": "security", "publisher": "Apple", "url": "https://support.apple.com/guide/security/welcome/web", "published_at": "2026-03-07", "pattern": "Platform security and trusted-execution reference", "trinity_target": "heart"},
                {"source_id": "systemd_docs", "os_family": "linux", "layer": "service_manager", "publisher": "freedesktop.org", "url": "https://www.freedesktop.org/software/systemd/man/latest/systemd.html", "published_at": "2026-03-07", "pattern": "Service management, supervision, and lifecycle orchestration", "trinity_target": "body"},
                {"source_id": "docker_overview", "os_family": "container", "layer": "runtime", "publisher": "Docker", "url": "https://docs.docker.com/get-started/docker-overview/", "published_at": "2026-03-07", "pattern": "Container runtime, packaging, and delivery model", "trinity_target": "body"},
                {"source_id": "kubernetes_concepts", "os_family": "distributed", "layer": "orchestration", "publisher": "Kubernetes", "url": "https://kubernetes.io/docs/concepts/", "published_at": "2026-03-07", "pattern": "Cluster orchestration, control-plane, and workload lifecycle concepts", "trinity_target": "trinity"},
            ],
        },
    )


def build_pack_files() -> None:
    for pack in PACKS:
        pack_name = pack["pack"]
        hyphen_pack = pack_name.replace("_", "-")
        system_ids = [f"{pack_name}_{suffix}" for suffix, _ in SUFFIXES]
        for system_id in system_ids:
            (ROOT / f"scripts/{system_id}.py").write_text(
                "#!/usr/bin/env python3\n"
                f'"""Trinity expansion system wrapper: {system_id}."""\n\n'
                "from trinity_expansion_system_runner import run_named_system\n\n\n"
                "if __name__ == \"__main__\":\n"
                f"    raise SystemExit(run_named_system(\"{system_id}\"))\n",
                encoding="utf-8",
            )

        contract = {
            "pack": pack_name,
            "display_name": pack["display_name"],
            "pillar": pack["pillar"],
            "wave": pack["wave"],
            "track": pack["track"],
            "connector_id": pack["connector_id"],
            "requires_auth": pack["requires_auth"],
            "gating_class": pack["gating_class"],
            "sync_strategy": pack["sync_strategy"],
            "freshness_window_days": 30,
            "cache_artifact": f"docs/trinity-mcp-cache/{hyphen_pack}-latest.json",
            "workflow_tokens": pack["workflow_tokens"],
            "risk_tags": pack["risk_tags"],
            "repo_targets": pack["repo_targets"],
            "skill_names": [f"{hyphen_pack}-operations", f"{hyphen_pack}-integration"],
            "system_ids": system_ids,
        }
        write_json(ROOT / f"docs/{hyphen_pack}-contract-v1.json", contract)
        write_json(ROOT / f"docs/{hyphen_pack}-fixture-v1.json", pack["fixture"])
        workflow = (
            f"# {pack['display_name']} Workflow\n\n"
            f"- pack: `{pack_name}`\n"
            f"- pillar: `{pack['pillar']}`\n"
            f"- gating_class: `{pack['gating_class']}`\n"
            f"- sync_strategy: `{pack['sync_strategy']}`\n\n"
            "## Guardrails\n"
            + "\n".join(f"- {token}" for token in pack["workflow_tokens"])
            + "\n\n## Operating notes\n"
            + "\n".join(
                [
                    "- offline-safe by default",
                    "- cache-backed artifacts remain the source of suite continuity",
                    "- promotion requires proof artifacts, not narrative intent",
                    "- disposable staging targets only for any live write path",
                ]
            )
            + "\n"
        )
        (ROOT / f"docs/{hyphen_pack}-workflow-v1.md").write_text(workflow, encoding="utf-8")
        write_json(
            ROOT / f"docs/{hyphen_pack}-catalog-entry-v1.json",
            {
                "pack": pack_name,
                "display_name": pack["display_name"],
                "extension_count": 12,
                "systems": system_ids,
                "skills": [f"{hyphen_pack}-operations", f"{hyphen_pack}-integration"],
                "artifacts": [
                    f"docs/{hyphen_pack}-contract-v1.json",
                    f"docs/{hyphen_pack}-fixture-v1.json",
                    f"docs/{hyphen_pack}-workflow-v1.md",
                    f"docs/{hyphen_pack}-catalog-entry-v1.json",
                ],
                "cache_artifact": f"docs/trinity-mcp-cache/{hyphen_pack}-latest.json",
                "connector_id": pack["connector_id"],
                "gating_class": pack["gating_class"],
            },
        )

        for suffix in ("operations", "integration"):
            skill_id = f"{hyphen_pack}-{suffix}"
            skill_dir = ROOT / "skills" / skill_id
            (skill_dir / "agents").mkdir(parents=True, exist_ok=True)
            title = f"{pack['display_name']} {'Operations' if suffix == 'operations' else 'Integration'}"
            prompt = (
                f"Run the {pack_name} pack, validate its cache-backed outputs, and keep the promotion boundary explicit."
                if suffix == "operations"
                else f"Integrate {pack_name} outputs into the Trinity suite without widening connector authority beyond proven boundaries."
            )
            (skill_dir / "SKILL.md").write_text(
                f"---\nname: {skill_id}\ndescription: {pack['skill_desc']}\n---\n\n"
                f"# {title}\n\n"
                f"Use when Codex needs to work with the `{pack_name}` pack.\n\n"
                "## Workflow\n"
                f"1. Read `docs/{hyphen_pack}-contract-v1.json` and `docs/{hyphen_pack}-workflow-v1.md`.\n"
                f"2. Refresh or inspect `docs/trinity-mcp-cache/{hyphen_pack}-latest.json`.\n"
                f"3. Keep the pack {'device-ready and write-free' if pack_name == 'wetware_device_readiness' else 'offline-safe unless its explicit live gate is enabled'}.\n"
                "4. Promote only PASS-backed outputs into narrative, comparison, or orchestration docs.\n",
                encoding="utf-8",
            )
            (skill_dir / "agents/openai.yaml").write_text(
                "interface:\n"
                f"  display_name: \"{title}\"\n"
                f"  short_description: \"{pack['display_name']} {suffix}.\"\n"
                f"  default_prompt: \"{prompt}\"\n",
                encoding="utf-8",
            )


def main() -> None:
    build_manifest_v4()
    build_extension_catalog_v2()
    build_mcp_catalog_v2()
    build_cache_schema_v2()
    build_supporting_docs()
    build_pack_files()
    print("Seeded Trinity active materialization phase artifacts.")


if __name__ == "__main__":
    main()
