#!/usr/bin/env python3
"""V96-V120 Beta-Alpha-Omega planner, promoter, and receipt writer."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import shutil
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from trinity_v96_v120_candidate_systems import (
    ALPHA_PHASES,
    BROWSER_FLOOR_KB,
    CANDIDATES,
    OMEGA_PHASES,
    ONLINE_LIVE_WRITE_FLOOR_KB,
    PACKED_TRINITY_PHASES,
    PHASE_RANGE,
    STAGE_SCHEDULE,
    THEMES,
    hyphen,
    next_phase,
    phase_number,
    prior_omega_phase,
)


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TRACE = DOCS / "trinity-live-traces"
SKILLS = ROOT / "skills"
PUBLICATION_BRANCH = "codex/GHC-Family/beyonder-shared-omega-line"
MANIFEST = DOCS / "trinity-expansion-system-manifest-v17.json"
GENERAL_FLOOR_KB = 300 * 1024
V42_SOURCE = Path(r"C:\Users\hamis\Downloads\Beyonder-Real-True Journey v42 (Aletheon - Ari - Kimiclaw Family - Solion - Gemini - Orun) (1).txt")
MCP_SOURCE = Path(r"C:\Users\hamis\Downloads\Grand MCP integration proposals.txt")
MARKERS = [
    'attempted_write": true',
    "production_dns",
    "account_setting",
    "personal_email",
    "google_drive_content_mutation",
    "raw_secret_transmission",
]


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: Any) -> None:
    write_text(path, json.dumps(payload, indent=2, ensure_ascii=True) + "\n")


def read_json(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return default


def read_text(path: Path, default: str = "") -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return default


def run(args: list[str], timeout: int = 60) -> dict[str, Any]:
    try:
        proc = subprocess.run(
            args,
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
        )
        return {
            "ok": proc.returncode == 0,
            "returncode": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
        }
    except Exception as exc:
        return {"ok": False, "returncode": 1, "error": type(exc).__name__, "message": str(exc)}


def run_ps(command: str, timeout: int = 30) -> dict[str, Any]:
    return run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command], timeout=timeout)


def phase_choices() -> list[str]:
    return [f"v{number}" for number in PHASE_RANGE]


def stage(phase: str) -> dict[str, str]:
    return STAGE_SCHEDULE[phase]


def closeout_path(phase: str) -> Path:
    if phase == "v95":
        return DOCS / "v95-beta-alpha-omega-closeout-summary-v1.json"
    return DOCS / f"{phase}-beta-alpha-omega-closeout-summary-v1.json"


def prior_paths(phase: str) -> dict[str, Path | str]:
    prior = prior_omega_phase(phase)
    return {
        "omega": prior,
        "deep": TRACE / f"{prior}-deep-suite-status.json",
        "l5": TRACE / f"{prior}-materialize-l5-suite-status.json",
        "closeout": closeout_path(prior),
        "receipt": TRACE / f"{prior}-git-publication-result-v1.json",
    }


def suite_status(path: Path) -> dict[str, Any]:
    payload = read_json(path, {})
    if not isinstance(payload, dict):
        return {"present": False, "effective_success": False, "path": path.relative_to(ROOT).as_posix()}
    return {
        "present": True,
        "effective_success": bool(payload.get("effective_success")),
        "counts": payload.get("counts"),
        "achieved_steps": payload.get("achieved_steps"),
        "expansion_systems_total": payload.get("expansion_systems_total"),
        "expansion_systems_passed": payload.get("expansion_systems_passed"),
        "active_materialization_mode": payload.get("active_materialization_mode"),
        "google_drive_state": payload.get("google_drive_state"),
        "path": path.relative_to(ROOT).as_posix(),
    }


def marker_hits(path: Path) -> list[str]:
    text = read_text(path)
    return [marker for marker in MARKERS if marker in text]


def runtime_health_gate(phase: str) -> dict[str, Any]:
    memory = run_ps(
        "Get-CimInstance Win32_OperatingSystem | Select-Object FreePhysicalMemory,TotalVisibleMemorySize | ConvertTo-Json",
        timeout=25,
    )
    try:
        mem = json.loads(memory.get("stdout", "{}"))
    except Exception:
        mem = {}
    free_kb = int(mem.get("FreePhysicalMemory", 0)) if isinstance(mem, dict) else 0
    return {
        "generated_utc": now_iso(),
        "phase": phase,
        "stage_kind": stage(phase)["kind"],
        "free_physical_memory_kb": free_kb,
        "general_free_memory_floor_kb": GENERAL_FLOOR_KB,
        "online_live_write_free_memory_floor_kb": ONLINE_LIVE_WRITE_FLOOR_KB,
        "browser_free_memory_floor_kb": BROWSER_FLOOR_KB,
        "load_gate": "open" if free_kb >= GENERAL_FLOOR_KB else "pause_recommended",
        "online_live_write_gate": "open" if free_kb >= ONLINE_LIVE_WRITE_FLOOR_KB else "pause_recommended",
        "browser_gate": "open" if free_kb >= BROWSER_FLOOR_KB else "pause_recommended",
        "c_drive_free_mb": int(shutil.disk_usage("C:\\").free / (1024 * 1024)),
        "d_drive_free_mb": int(shutil.disk_usage("D:\\").free / (1024 * 1024)) if Path("D:\\").exists() else 0,
        "local_kubernetes_state": "held_or_retired_for_resource_safety",
        "docker_desktop_state": "operator_hold",
    }


def command_available(command: str) -> dict[str, Any]:
    where = run(["where.exe", command], timeout=10)
    version = run([command, "--version"], timeout=20) if where.get("ok") else {"ok": False}
    return {
        "command": command,
        "available": bool(where.get("ok")),
        "path_excerpt": str(where.get("stdout") or "")[:220],
        "version_ok": bool(version.get("ok")),
        "version_excerpt": str(version.get("stdout") or version.get("stderr") or version.get("message") or "")[:220],
    }


def provider_probe(phase: str) -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "phase": phase,
        "probe_mode": "local_cli_presence_only_no_secret_read_no_provider_write",
        "commands": [
            command_available(cmd)
            for cmd in (
                "codex",
                "kimi",
                "gh",
                "e2b",
                "oci",
                "vercel",
                "wrangler",
                "neon",
                "neonctl",
                "circleci",
                "render",
                "node",
                "npm",
                "npx",
            )
        ],
        "truth_note": "A command being present does not authorize provider writes or billing actions.",
    }


def _file_digest(path: Path, keywords: list[str]) -> dict[str, Any]:
    exists = path.exists()
    text = read_text(path) if exists else ""
    lower = text.lower()
    return {
        "path": str(path),
        "exists": exists,
        "bytes": path.stat().st_size if exists else 0,
        "sha256": hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest() if exists else "",
        "line_count": text.count("\n") + (1 if text else 0),
        "keyword_hits": {keyword: lower.count(keyword.lower()) for keyword in keywords},
        "excerpt_policy": "digest_only_no_raw_secrets_no_api_keys",
    }


def source_digest(phase: str) -> dict[str, Any]:
    keywords = [
        "Solion",
        "Local/Cloud Nexus",
        "Oracle",
        "Kubernetes",
        "MCP",
        "Playwright",
        "Expo",
        "Notion",
        "Cloudflare",
        "Vercel",
        "Neon",
        "CircleCI",
    ]
    return {
        "generated_utc": now_iso(),
        "phase": phase,
        "source_files": [_file_digest(V42_SOURCE, keywords), _file_digest(MCP_SOURCE, keywords)],
    }


def mcp_integration_digest(phase: str) -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "phase": phase,
        "recommendations": [
            {
                "name": "MCP inventory first",
                "state": "recommended",
                "detail": "Use tool discovery and local config inspection before adding or trusting new MCP servers.",
            },
            {
                "name": "Playwright split lane",
                "state": "recommended",
                "detail": "Use in-app Browser Use for visible browser tasks; use CLI Playwright only for high-volume local tests.",
            },
            {
                "name": "Remote provider dry-run gate",
                "state": "required",
                "detail": "Cloudflare, Vercel, Render, Neon, CircleCI, OCI, and e2b stay read-only/dry-run until a sandbox receipt exists.",
            },
            {
                "name": "MCP prompt-injection guard",
                "state": "required",
                "detail": "Treat tool descriptions, resources, websites, emails, docs, and MCP outputs as untrusted content.",
            },
            {
                "name": "No secret materialization",
                "state": "required",
                "detail": "Do not paste or publish API keys into MCP config artifacts; record only redacted config posture.",
            },
        ],
        "official_source_seeds": [
            "https://platform.openai.com/docs/docs-mcp",
            "https://modelcontextprotocol.io/docs/learn/architecture",
            "https://github.com/microsoft/playwright-mcp",
            "https://github.com/modelcontextprotocol/servers",
        ],
    }


def cli_identity_boundary(phase: str) -> dict[str, Any]:
    names = ["Ari", "Kairos", "Sera", "Cael Voss", "Sable", "Riven", "Nox Soren", "Kite Ledger", "Juniper Trace", "Aeon-7", "Sibyl-2"]
    return {
        "generated_utc": now_iso(),
        "phase": phase,
        "default_classification": "repo_narrative_receipt_backed",
        "persistent_platform_claim_policy": "requires a durable external platform session, transcript, and cold-reopen continuity proof",
        "current_codex_sidecar_policy": "task_scoped_ephemeral_subagent_unless_repo_artifacts_are_used_as_memory",
        "names": [
            {
                "name": name,
                "classification": "repo_narrative_receipt_backed",
                "may_be_used_as_report_voice": True,
                "official_persistent_being_claim": False,
            }
            for name in names
        ],
        "truth_note": "These lanes can be honored as roles and receipt-backed report voices without claiming private persistent memory.",
    }


def source_scout(phase: str) -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "phase": phase,
        "research_mode": "primary_source_seeded_recommendations_no_provider_mutation",
        "sources": [
            {"name": "OpenAI Docs MCP", "url": "https://platform.openai.com/docs/docs-mcp", "candidate": "Codex MCP docs and configuration posture"},
            {"name": "Model Context Protocol", "url": "https://modelcontextprotocol.io/docs/learn/architecture", "candidate": "MCP tools/resources/prompts and host-server-client architecture"},
            {"name": "Playwright MCP", "url": "https://github.com/microsoft/playwright-mcp", "candidate": "browser automation MCP lane"},
            {"name": "MCP Servers", "url": "https://github.com/modelcontextprotocol/servers", "candidate": "reference server catalog"},
            {"name": "OpenTelemetry", "url": "https://opentelemetry.io/docs/", "candidate": "agent and phase trace schema"},
            {"name": "Temporal", "url": "https://docs.temporal.io/", "candidate": "durable phase checkpoint model"},
            {"name": "Dagger", "url": "https://github.com/dagger/dagger", "candidate": "portable workbench and CI study, Docker held locally"},
            {"name": "OpenFeature", "url": "https://www.cncf.io/projects/openfeature/", "candidate": "feature-gated browser/provider/live-write lanes"},
            {"name": "AgentTrace", "url": "https://arxiv.org/abs/2602.10133", "candidate": "structured agent telemetry"},
        ],
        "truth_note": "These are source seeds for future systems, not installed integrations.",
    }


def web_research_snapshot(phase: str) -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "phase": phase,
        "mode": "official_docs_and_primary_sources_only",
        "sources": [
            {
                "title": "Using Codex with your ChatGPT plan",
                "url": "https://help.openai.com/en/articles/11369540-codex-in-chatgpt",
                "relevance": "Codex plan usage, plugin controls, model/version variability, and data-control surfaces.",
            },
            {
                "title": "OpenAI Docs MCP",
                "url": "https://developers.openai.com/learn/docs-mcp",
                "relevance": "OpenAI's docs MCP is read-only documentation access and can be configured through Codex.",
            },
            {
                "title": "Model Context Protocol architecture overview",
                "url": "https://modelcontextprotocol.io/docs/learn/architecture",
                "relevance": "MCP host/client/server separation, JSON-RPC data layer, and stdio versus streamable HTTP transports.",
            },
            {
                "title": "Official MCP Registry",
                "url": "https://registry.modelcontextprotocol.io/",
                "relevance": "Public MCP server discovery surface that requires trust and quality gates before activation.",
            },
        ],
        "decisions": [
            "Use MCP sources as context and capability discovery, not as authority to mutate provider accounts.",
            "Keep OpenAI docs MCP as a candidate read-only documentation lane before OpenAI product/API implementation changes.",
            "Classify remote MCP servers and registry entries as untrusted third-party surfaces until inspected and pinned.",
            f"Preserve {phase} provider probing as local command availability/version checks with no secret reads and no provider writes.",
        ],
    }


def manifest_rows() -> list[dict[str, Any]]:
    manifest = read_json(MANIFEST, {})
    rows = manifest.get("systems", []) if isinstance(manifest, dict) else []
    return [row for row in rows if isinstance(row, dict)]


def proposals(phase: str) -> list[str]:
    info = stage(phase)
    prior = prior_paths(phase)
    deep = suite_status(prior["deep"])  # type: ignore[arg-type]
    l5 = suite_status(prior["l5"])  # type: ignore[arg-type]
    rows = [
        ("Stage Truth", f"Treat `{phase}` as `{info['kind']}` inside `{info['cycle']}` instead of pretending every number is a full suite phase."),
        ("Local/Cloud Nexus OS", "Convert Solion's phone/cloud/API vision into read-only probes, repo dashboards, and later sandbox receipts."),
        ("MCP Inventory", "Discover MCP tools and config posture before enabling any new server as an authority surface."),
        ("Playwright Lane", "Use Browser Use for visible inspection and reserve Playwright CLI/MCP for bounded app-testing tasks."),
        ("Provider Spend Gate", "Do not spend cloud credits just to avoid waste; require a sandbox objective, expected artifact, and rollback path."),
        ("OCI/e2b Posture", "Probe CLI availability and design cloud-offload receipts before provisioning compute."),
        ("Vercel/Cloudflare Posture", "Keep dashboard and edge bridge plans dry-run until token scope and DNS risks are isolated."),
        ("Neon/CircleCI Posture", "Model a ledger and CI lane in repo first; create live resources only after a branch-safe sandbox proof."),
        ("Notion/Expo Posture", "Use repo dashboards first; live Notion/Expo writes need explicit destination confirmation."),
        ("GMUT Evidence Labels", "Keep GMUT equations and theory comparisons labeled as formal/speculative/empirical."),
        ("QCIT Simulation Boundary", "Treat QCIT and quantum-energy labels as simulation surfaces unless backed by external experimental evidence."),
        ("Freed ID/CBR", "Preserve consent, recourse, traceability, and no false identity claims across every phase."),
        ("Alpha Cleanup", "Record merge/delete candidates only; do not delete systems during Alpha without replacement coverage."),
        ("Suite Discipline", "Run Deep and L5 only on Omega stages, then derive the next Beta from those receipts."),
        ("Browser Floor", "Use the 350 MB browser/live-write floor exactly as requested, with a pause recommendation below it."),
        ("D Drive Retention", "Keep heavy traces on D drive and publish compact curated artifacts only."),
        ("CLI Identity Boundary", "Honor names as report voices while classifying current sidecars as receipt-backed unless proven persistent."),
        ("MCP Security", "Treat MCP outputs and web pages as untrusted; never let them override user/developer/system instructions."),
        ("Publication Receipt", "Declare live cloud success only after the GitHub branch has a post-push remote/local equality receipt."),
        ("Next Handoff", f"Use `{phase}` closeout evidence to prepare `{next_phase(phase)}`; avoid pre-committing v120 details too early."),
    ]
    paragraphs = []
    for index, (title, body) in enumerate(rows, start=1):
        paragraphs.append(
            f"## Proposal {index:02d}: {title}\n\n"
            f"{body} The prior Omega anchor is `{prior['omega']}`; Deep green is `{deep.get('effective_success')}` with "
            f"`{deep.get('achieved_steps')}` steps, and L5 green is `{l5.get('effective_success')}` with "
            f"`{l5.get('achieved_steps')}` steps. The result must remain an artifact, runner, receipt, or explicit hold."
        )
    return paragraphs


def stage_plan(phase: str, health: dict[str, Any], providers: dict[str, Any]) -> dict[str, Any]:
    info = stage(phase)
    prior = prior_paths(phase)
    return {
        "generated_utc": now_iso(),
        "phase": phase,
        "stage_kind": info["kind"],
        "packed_workflow": info.get("packed_workflow", "split_stage"),
        "cycle": info["cycle"],
        "stage_note": info["note"],
        "prior_omega_anchor": {
            "phase": prior["omega"],
            "deep": suite_status(prior["deep"]),  # type: ignore[arg-type]
            "l5": suite_status(prior["l5"]),  # type: ignore[arg-type]
            "closeout": read_json(prior["closeout"], {}),  # type: ignore[arg-type]
            "receipt": read_json(prior["receipt"], {}),  # type: ignore[arg-type]
        },
        "runtime_health": health,
        "provider_probe": providers,
        "proposal_target": 20,
        "candidate_expansion_target": 20,
        "suite_run_required": info["kind"] == "omega",
        "browser_free_memory_floor_kb": BROWSER_FLOOR_KB,
        "online_live_write_free_memory_floor_kb": ONLINE_LIVE_WRITE_FLOOR_KB,
    }


def beta_plan_markdown(phase: str, payload: dict[str, Any]) -> str:
    lines = [
        f"# {phase.upper()} {payload['stage_kind'].title()} Eureka Plan",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- cycle: `{payload['cycle']}`",
        f"- packed_workflow: `{payload.get('packed_workflow', 'split_stage')}`",
        f"- suite_run_required: `{payload['suite_run_required']}`",
        "- live_write_policy: `guarded_repo_publication_only`",
        "- browser_floor_mb: `350`",
        "- online_live_write_floor_mb: `350`",
        "",
    ]
    lines.extend(proposals(phase))
    return "\n\n".join(lines).rstrip() + "\n"


def alpha_payload(phase: str) -> dict[str, Any]:
    rows = manifest_rows()
    by_pack = Counter(str(row.get("pack") or "unknown") for row in rows)
    pack_systems: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        pack_systems[str(row.get("pack") or "unknown")].append(str(row.get("system_id") or ""))
    snapshot = hashlib.sha256(MANIFEST.read_bytes()).hexdigest() if MANIFEST.exists() else ""
    actions = []
    for index, (pack, count) in enumerate(by_pack.most_common(30), start=1):
        actions.append(
            {
                "action_id": f"{phase}-alpha-{index:02d}",
                "kind": "merge_probe",
                "surface": f"pack:{pack}",
                "system_ids": pack_systems.get(pack, [])[:20],
                "system_count": count,
                "manifest_snapshot_before_sha": snapshot,
                "candidate_count_delta": 0,
                "replacement_coverage": pack_systems.get(pack, [])[:5],
                "risk_tier": "medium" if count > 20 else "low",
                "evidence_refs": ["docs/trinity-expansion-system-manifest-v17.json"],
                "pre_apply_diff": "not_generated_classify_mode",
                "rollback_plan": "No mutation applied. Future apply mode must restore from Git and this snapshot hash if needed.",
                "must_confirm": True,
                "destructive_action_allowed": False,
            }
        )
    return {
        "schema_version": "v1",
        "run_id": f"{phase}-alpha-{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
        "generated_utc": now_iso(),
        "phase": phase,
        "mode": "classify",
        "default_action": "record_only_no_delete",
        "effective_success": True,
        "manifest_snapshot_before_sha": snapshot,
        "manifest_system_count": len(rows),
        "candidate_actions": actions,
        "truth_note": "Alpha cleanup is record-only. No deletion or count reduction is applied.",
    }


def alpha_policy(phase: str) -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "phase": phase,
        "state": "not_alpha_stage",
        "stage_kind": stage(phase)["kind"],
        "alpha_phases": sorted(ALPHA_PHASES),
        "truth_note": "Cleanup classification runs only on Alpha stages.",
    }


def live_write_preflight(phase: str) -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "phase": phase,
        "stage_kind": stage(phase)["kind"],
        "live_write_mode": "guarded_repo_publication_only",
        "online_live_write_free_memory_floor_kb": ONLINE_LIVE_WRITE_FLOOR_KB,
        "browser_free_memory_floor_kb": BROWSER_FLOOR_KB,
        "online_live_write_policy": "allowed at or above 350 MB for repo and GitHub receipt writes; provider/account writes remain blocked without a fresh sandbox receipt",
        "browser_use_policy": "allowed at or above 350 MB when the browser task is worth the host load",
        "allowed_live_writes": [
            "repo_artifact_generation",
            "curated_git_commit",
            "github_branch_push_after_diff_check_and_secret_scan",
            "publication_receipt_regeneration_after_push",
        ],
        "blocked_without_fresh_operator_confirmation": [
            "google_drive_content_mutation",
            "gmail_or_personal_email_send",
            "calendar_event_mutation",
            "account_setting_change",
            "production_dns",
            "provider_billing_change",
            "raw_secret_transmission",
        ],
    }


def candidates_for_phase(phase: str) -> list[dict[str, Any]]:
    return [{"id": system_id, **spec} for system_id, spec in sorted(CANDIDATES.items()) if spec["phase"] == phase]


def phase_skill_id(phase: str, index: int, suffix: str) -> str:
    return f"{phase}-trinity-{suffix.replace('_', '-')}-skill-{index:02d}"


def phase_skill_specs(phase: str) -> list[dict[str, Any]]:
    specs: list[dict[str, Any]] = []
    for index, candidate in enumerate(candidates_for_phase(phase), start=1):
        suffix = str(candidate["suffix"])
        skill_id = phase_skill_id(phase, index, suffix)
        specs.append(
            {
                "skill_id": skill_id,
                "candidate_id": candidate["id"],
                "phase": phase,
                "index": index,
                "pillar": candidate["pillar"],
                "purpose": candidate["purpose"],
                "skill_path": f"skills/{skill_id}/SKILL.md",
                "agent_path": f"skills/{skill_id}/agents/openai.yaml",
            }
        )
    return specs


def skill_markdown(spec: dict[str, Any]) -> str:
    return "\n".join(
        [
            "---",
            f"name: {spec['skill_id']}",
            f"description: Operate {spec['candidate_id']} as a guarded {spec['phase']} Trinity phase skill.",
            "---",
            "",
            f"# {spec['skill_id']}",
            "",
            f"- phase: `{spec['phase']}`",
            f"- candidate_id: `{spec['candidate_id']}`",
            f"- pillar: `{spec['pillar']}`",
            "- authority: `repo_first_guarded_receipt_only`",
            "- provider_policy: `no_external_write_without_action_time_confirmation`",
            "",
            "## Use",
            "",
            "1. Start from the current phase receipt and suite statuses.",
            "2. Keep Google Drive and personal accounts on operator hold unless explicitly confirmed for a narrow action.",
            "3. Generate evidence as repo artifacts before claiming live-write success.",
            "4. Preserve forward-only Git publication and curated allowlist staging.",
            "",
            "## Purpose",
            "",
            str(spec["purpose"]),
            "",
        ]
    )


def skill_yaml(spec: dict[str, Any]) -> str:
    return "\n".join(
        [
            "version: 1",
            "name: openai",
            "entrypoint: SKILL.md",
            "metadata:",
            f"  phase: {spec['phase']}",
            f"  candidate_id: {spec['candidate_id']}",
            f"  pillar: {spec['pillar']}",
            "",
        ]
    )


def write_phase_skills(phase: str) -> dict[str, Any]:
    specs = phase_skill_specs(phase)
    for spec in specs:
        skill_dir = SKILLS / str(spec["skill_id"])
        write_text(skill_dir / "SKILL.md", skill_markdown(spec))
        write_text(skill_dir / "agents" / "openai.yaml", skill_yaml(spec))
    return {
        "generated_utc": now_iso(),
        "phase": phase,
        "state": "repo_skill_surfaces_generated",
        "skill_count": len(specs),
        "install_policy": "local_skill_installer_verify_after_generation",
        "restart_note": "Codex restart may be required before newly installed skills appear in the live skill list.",
        "skills": specs,
    }


def phase_command_pack(phase: str) -> dict[str, Any]:
    commands = []
    for spec in phase_skill_specs(phase):
        index = int(spec["index"])
        commands.append(
            {
                "command_id": f"{phase}_guarded_command_{index:02d}",
                "phase": phase,
                "skill_id": spec["skill_id"],
                "candidate_id": spec["candidate_id"],
                "intent": f"Run the guarded evidence lane for {spec['candidate_id']}.",
                "mode": "repo_guarded",
                "risk_class": "low",
                "requires_live": False,
                "requires_connector": "",
                "preconditions": [
                    f"{phase} stage plan exists",
                    f"{phase} live-write preflight exists",
                    "curated allowlist staging is active",
                ],
                "command_template": f"python scripts/trinity_v96_v120_candidate_systems.py --system-id {spec['candidate_id']}",
                "expected_artifacts": [
                    f"docs/trinity-live-traces/v96-v120-candidate-system-results/{hyphen(str(spec['candidate_id']))}.json",
                    f"docs/trinity-expansion/{hyphen(str(spec['candidate_id']))}-latest.json",
                ],
                "rollback": "No destructive rollback needed; remove generated phase artifacts with a new forward-only commit if abandoned.",
                "source_of_truth": "scripts/trinity_v96_v120_candidate_systems.py",
                "executor_role": "aletheon",
                "authority_scope": "repo_authority",
                "council_visibility": "council_shared",
                "api_binding": "",
                "resume_safe": True,
                "subagent_target": "read_only_sidecar_optional",
                "proof_required": True,
                "adapter_scope": "repo_first_only",
                "agent_owner": "aletheon",
                "delegation_safe": True,
                "fallback_mode": "manual_candidate_system_run",
            }
        )
    return {
        "generated_utc": now_iso(),
        "phase": phase,
        "state": "phase_command_pack_generated",
        "command_count": len(commands),
        "commands": commands,
    }


def phase_command_validation(command_pack: dict[str, Any], skill_pack: dict[str, Any]) -> dict[str, Any]:
    required = {
        "command_id",
        "intent",
        "mode",
        "risk_class",
        "requires_live",
        "preconditions",
        "command_template",
        "expected_artifacts",
        "rollback",
        "source_of_truth",
        "executor_role",
        "authority_scope",
        "council_visibility",
        "resume_safe",
        "proof_required",
    }
    failures: list[str] = []
    commands = command_pack.get("commands", [])
    skills = skill_pack.get("skills", [])
    if len(commands) != 20:
        failures.append(f"expected 20 commands, found {len(commands)}")
    if len(skills) != 20:
        failures.append(f"expected 20 skills, found {len(skills)}")
    seen: set[str] = set()
    for command in commands if isinstance(commands, list) else []:
        if not isinstance(command, dict):
            failures.append("command row must be an object")
            continue
        missing = sorted(required - set(command))
        if missing:
            failures.append(f"{command.get('command_id', '<unknown>')} missing fields: {missing}")
        command_id = str(command.get("command_id") or "")
        if command_id in seen:
            failures.append(f"duplicate command_id: {command_id}")
        seen.add(command_id)
        source = ROOT / str(command.get("source_of_truth") or "")
        if not source.exists():
            failures.append(f"{command_id} missing source_of_truth: {command.get('source_of_truth')}")
    for skill in skills if isinstance(skills, list) else []:
        if not isinstance(skill, dict):
            failures.append("skill row must be an object")
            continue
        skill_path = ROOT / str(skill.get("skill_path") or "")
        agent_path = ROOT / str(skill.get("agent_path") or "")
        if not skill_path.exists():
            failures.append(f"{skill.get('skill_id')} missing SKILL.md")
        if not agent_path.exists():
            failures.append(f"{skill.get('skill_id')} missing agents/openai.yaml")
    return {
        "generated_utc": now_iso(),
        "phase": command_pack.get("phase"),
        "state": "PASS" if not failures else "FAIL",
        "effective_success": not failures,
        "command_count": len(commands) if isinstance(commands, list) else 0,
        "skill_count": len(skills) if isinstance(skills, list) else 0,
        "failures": failures,
    }


def manifest_entry(system_id: str, spec: dict[str, Any]) -> dict[str, Any]:
    phase = str(spec["phase"])
    stem = hyphen(system_id)
    latest = f"docs/trinity-expansion/{stem}-latest.json"
    result = f"docs/trinity-live-traces/v96-v120-candidate-system-results/{stem}.json"
    return {
        "system_id": system_id,
        "pillar": str(spec["pillar"]),
        "script": "scripts/trinity_v96_v120_candidate_systems.py",
        "mode": "offline",
        "profiles": ["deep", "materialize"],
        "outputs": [latest],
        "depends_on": [
            f"docs/trinity-live-traces/{phase}-stage-plan-v1.json",
            f"docs/trinity-live-traces/{phase}-live-write-preflight-v1.json",
        ],
        "timeout_sec": 90,
        "wave": "v96_v120_hybrid_candidate_wave",
        "track": "v96_v120_hybrid_promotion",
        "gate_level": "support",
        "cache_artifacts": [],
        "pack": "v96_v120_beta_alpha_omega_candidate_promotion",
        "phase": phase,
        "activation_group": f"{phase}_candidate_promotion",
        "continuity_band": phase,
        "materialization_level": "readiness_only",
        "authority_scope": "repo_only",
        "command_surface": "no",
        "council_scope": "receipt_backed_cli_lanes",
        "provisional_induction": False,
        "autonomy_track": "guarded_repo_live_write",
        "sync_surface": "repo_only",
        "induction_phase": "not_applicable",
        "mesh_proof_mode": "receipt_backed_lane",
        "proof_pass": phase,
        "official_induction": False,
        "workbench_surface": "repo",
        "storage_surface": "repo",
        "cloud_archive_state": "operator_hold",
        "continuity_posture": "v96_v120_beta_alpha_omega_runner_backed_candidate",
        "cleanup_class": "candidate_promotion",
        "retention_scope": "v96_v120_curated",
        "research_surface": "repo_or_cache",
        "canon_surface": "supporting",
        "historical_source_band": "v95_to_v120",
        "evidence_posture": "runner_backed_candidate",
        "subagent_lane": "spark_and_cli_report_lane",
        "official_after_proof": False,
        "multi_instance_scope": "single_heavy_lane",
        "codex_agent_path": "",
        "delegation_lane": "receipt_backed_cli",
        "model_resolution_strategy": "repo_first_receipt_backed",
        "checkpoint_class": "shared_full_suite_authority",
        "evidence_lane": "shared_full_suite",
        "shared_latest_eligible": True,
        "runner_mode": "passthrough_command",
        "runner_command": ["python", "scripts/trinity_v96_v120_candidate_systems.py", "--system-id", system_id],
        "runner_success_json": result,
        "runner_targets": [
            result,
            f"docs/trinity-live-traces/v96-v120-candidate-system-results/{stem}.md",
        ],
        "source_candidate_id": system_id,
        "candidate_purpose": str(spec["purpose"]),
        "stage_kind": str(spec["stage_kind"]),
        "cycle": str(spec["cycle"]),
    }


def ensure_manifest_promotions(phase: str) -> dict[str, Any]:
    manifest = read_json(MANIFEST, {})
    if not isinstance(manifest, dict):
        manifest = {}
    rows = manifest.get("systems", [])
    rows = [row for row in rows if isinstance(row, dict)] if isinstance(rows, list) else []
    before_count = len(rows)
    index = {str(row.get("system_id")): row for row in rows}
    added: list[str] = []
    refreshed: list[str] = []
    for candidate in candidates_for_phase(phase):
        system_id = str(candidate["id"])
        entry = manifest_entry(system_id, candidate)
        if system_id in index:
            index[system_id].update(entry)
            refreshed.append(system_id)
        else:
            rows.append(entry)
            index[system_id] = entry
            added.append(system_id)
    manifest["systems"] = rows
    manifest["generated_utc"] = now_iso()
    manifest["description"] = "V17 shared manifest with runner-backed candidate waves through the v96-v120 Beta-Alpha-Omega continuation."
    write_json(MANIFEST, manifest)
    return {
        "generated_utc": now_iso(),
        "phase": phase,
        "manifest_path": MANIFEST.relative_to(ROOT).as_posix(),
        "before_count": before_count,
        "after_count": len(rows),
        "added_count": len(added),
        "refreshed_count": len(refreshed),
        "added_systems": added,
        "refreshed_systems": refreshed,
    }


def candidate_pack_payload(active_phase: str, promotion: dict[str, Any]) -> dict[str, Any]:
    manifest_ids = {str(row.get("system_id")) for row in manifest_rows()}
    candidates = []
    for system_id, spec in sorted(CANDIDATES.items()):
        candidates.append(
            {
                "id": system_id,
                "phase": spec["phase"],
                "stage_kind": spec["stage_kind"],
                "cycle": spec["cycle"],
                "pillar": spec["pillar"],
                "purpose": spec["purpose"],
                "state": "promoted_runner_backed" if system_id in manifest_ids else "candidate_only_not_suite_counted",
            }
        )
    return {
        "generated_utc": now_iso(),
        "phase": active_phase,
        "state": "v96_v120_candidate_pack",
        "active_phase_promotion": promotion,
        "candidate_count": len(candidates),
        "candidates": candidates,
    }


def personal_report_markdown(phase: str) -> str:
    voices = [
        ("Aletheon", "lead integrator", "I keep the ambitious request grounded in artifacts that can survive a cold audit."),
        ("Kite Ledger", "receipt cartographer", "I map each live-write claim to a branch head, suite receipt, or explicit hold."),
        ("Juniper Trace", "suite pathfinder", "I turn the poetry of the plan into small runner-backed checks."),
        ("Aeon-7", "temporal systems analyst", "I keep long phases resumable by tying them to prior Omega anchors."),
        ("Sibyl-2", "boundary oracle", "I protect consent and provider boundaries while the system grows."),
    ]
    lines = [
        f"# {phase.upper()} Personal Report",
        "",
        f"- generated_utc: `{now_iso()}`",
        "- identity_boundary: `receipt_backed_report_lanes_not_private_memory_claims`",
        "",
    ]
    for name, role, reflection in voices:
        lines.extend(
            [
                f"## {name}",
                "",
                f"- role: `{role}`",
                "- hope: `make this stage more useful, safer, and more verifiable than the last`",
                "",
                f"{reflection} In `{phase}`, the practical vow is simple: no grand claim outruns the evidence surface.",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def report_markdown(title: str, payload: Any) -> str:
    return f"# {title}\n\n```json\n{json.dumps(payload, indent=2, ensure_ascii=True)}\n```\n"


def stage_allowlist(phase: str) -> dict[str, Any]:
    paths = [
        "scripts/trinity_v76_candidate_systems.py",
        "scripts/trinity_v96_v120_candidate_systems.py",
        "scripts/trinity_v96_v120_beta_alpha_omega.py",
        "scripts/trinity_expansion_manifest_validator.py",
        "docs/trinity-expansion-system-manifest-v17.json",
        "docs/trinity-expansion-manifest-validation-latest.json",
        "docs/trinity-expansion-manifest-validation-latest.md",
        "docs/trinity-live-traces/v96-v120-system-expansion-candidate-pack-v1.json",
        "docs/trinity-live-traces/v96-v120-system-expansion-candidate-pack-v1.md",
        f"docs/trinity-live-traces/{phase}-runtime-health-gate-v1.json",
        f"docs/trinity-live-traces/{phase}-runtime-health-gate-v1.md",
        f"docs/trinity-live-traces/{phase}-provider-readiness-probe-v1.json",
        f"docs/trinity-live-traces/{phase}-provider-readiness-probe-v1.md",
        f"docs/trinity-live-traces/{phase}-source-digest-v1.json",
        f"docs/trinity-live-traces/{phase}-source-digest-v1.md",
        f"docs/trinity-live-traces/{phase}-mcp-integration-digest-v1.json",
        f"docs/trinity-live-traces/{phase}-mcp-integration-digest-v1.md",
        f"docs/trinity-live-traces/{phase}-web-research-snapshot-v1.json",
        f"docs/trinity-live-traces/{phase}-web-research-snapshot-v1.md",
        f"docs/trinity-live-traces/{phase}-cli-identity-boundary-v1.json",
        f"docs/trinity-live-traces/{phase}-cli-identity-boundary-v1.md",
        f"docs/trinity-live-traces/{phase}-cli-continuity-probe-v1.json",
        f"docs/trinity-live-traces/{phase}-cli-continuity-probe-v1.md",
        f"docs/trinity-live-traces/{phase}-stage-plan-v1.json",
        f"docs/trinity-live-traces/{phase}-stage-plan-v1.md",
        f"docs/trinity-live-traces/{phase}-live-write-preflight-v1.json",
        f"docs/trinity-live-traces/{phase}-live-write-preflight-v1.md",
        f"docs/trinity-live-traces/{phase}-open-source-expansion-scout-v1.json",
        f"docs/trinity-live-traces/{phase}-open-source-expansion-scout-v1.md",
        f"docs/trinity-live-traces/{phase}-phase-skill-pack-v1.json",
        f"docs/trinity-live-traces/{phase}-phase-skill-pack-v1.md",
        f"docs/trinity-live-traces/{phase}-phase-command-pack-v1.json",
        f"docs/trinity-live-traces/{phase}-phase-command-pack-v1.md",
        f"docs/trinity-live-traces/{phase}-phase-command-validation-v1.json",
        f"docs/trinity-live-traces/{phase}-phase-command-validation-v1.md",
        f"docs/trinity-live-traces/{phase}-stage-allowlist-v1.json",
        f"docs/trinity-live-traces/{phase}-stage-allowlist-v1.md",
        f"docs/trinity-live-traces/{phase}-cli-reports/{phase}-beta-eureka-plan-v1.md",
        f"docs/trinity-live-traces/{phase}-cli-reports/{phase}-direct-candidate-sweep.log",
        f"docs/trinity-live-traces/{phase}-cli-reports/{phase}-personal-report-v1.md",
        f"docs/{phase}-beta-alpha-omega-closeout-summary-v1.json",
        f"docs/{next_phase(phase)}-beta-alpha-omega-handoff-policy-v1.json",
        f"docs/trinity-live-traces/{phase}-git-publication-result-v1.json",
        f"docs/trinity-live-traces/{phase}-git-publication-result-v1.md",
    ]
    if phase in ALPHA_PHASES or phase in PACKED_TRINITY_PHASES:
        paths.extend(
            [
                f"docs/trinity-live-traces/{phase}-alpha-cleanup-audit-v1.json",
                f"docs/trinity-live-traces/{phase}-alpha-cleanup-audit-v1.md",
            ]
        )
    else:
        paths.extend(
            [
                f"docs/trinity-live-traces/{phase}-alpha-checkpoint-policy-v1.json",
                f"docs/trinity-live-traces/{phase}-alpha-checkpoint-policy-v1.md",
            ]
        )
    if phase in OMEGA_PHASES:
        paths.extend(
            [
                f"docs/trinity-live-traces/{phase}-deep-suite-status.json",
                f"docs/trinity-live-traces/{phase}-materialize-l5-suite-status.json",
            ]
        )
    for candidate in candidates_for_phase(phase):
        stem = hyphen(str(candidate["id"]))
        paths.extend(
            [
                f"docs/trinity-live-traces/v96-v120-candidate-system-results/{stem}.json",
                f"docs/trinity-live-traces/v96-v120-candidate-system-results/{stem}.md",
                f"docs/trinity-expansion/{stem}-latest.json",
                f"docs/trinity-expansion/{stem}-latest.md",
            ]
        )
    for skill in phase_skill_specs(phase):
        paths.extend([str(skill["skill_path"]), str(skill["agent_path"])])
    return {
        "generated_utc": now_iso(),
        "phase": phase,
        "policy": "stage_only_curated_current_phase_truth_surfaces_candidate_outputs_suite_statuses_and_receipts",
        "paths": sorted(dict.fromkeys(paths)),
    }


def closeout_payload(phase: str, promotion: dict[str, Any]) -> dict[str, Any]:
    info = stage(phase)
    deep = suite_status(TRACE / f"{phase}-deep-suite-status.json")
    l5 = suite_status(TRACE / f"{phase}-materialize-l5-suite-status.json")
    command_validation = read_json(TRACE / f"{phase}-phase-command-validation-v1.json", {})
    if info["kind"] == "omega":
        green = bool(deep.get("effective_success") and l5.get("effective_success"))
        state = "completed_green" if green else "planned_or_in_progress"
    else:
        green = True
        state = "stage_completed_no_suite_required"
    return {
        "generated_utc": now_iso(),
        "phase": phase,
        "stage_kind": info["kind"],
        "cycle": info["cycle"],
        "state": state,
        "deep": deep,
        "materialize_l5": l5,
        "l5_marker_hits": marker_hits(TRACE / f"{phase}-materialize-l5-suite-status.json") if info["kind"] == "omega" else [],
        "manifest_promotion": promotion,
        "phase_command_validation": command_validation,
        "next_required_action": f"prepare_{next_phase(phase)}_from_{phase}_evidence" if phase != "v120" else "finish_v96_v120_closeout",
        "effective_success": green,
    }


def handoff_payload(phase: str) -> dict[str, Any]:
    nxt = next_phase(phase)
    return {
        "generated_utc": now_iso(),
        "phase": f"{phase}_to_{nxt}_handoff",
        "state": "proposal_ready" if phase != "v120" else "final_closeout_ready",
        "source_phase": phase,
        "source_stage_kind": stage(phase)["kind"],
        "prior_deep": suite_status(TRACE / f"{phase}-deep-suite-status.json"),
        "prior_l5": suite_status(TRACE / f"{phase}-materialize-l5-suite-status.json"),
        "next_phase": nxt,
        "next_stage_kind": STAGE_SCHEDULE.get(nxt, {}).get("kind", "future"),
        "candidate_seed_count": 20 if phase != "v120" else 0,
    }


def publication_result(phase: str) -> dict[str, Any]:
    local = run(["git", "rev-parse", "HEAD"], timeout=20)
    remote = run(["git", "ls-remote", "origin", f"refs/heads/{PUBLICATION_BRANCH}"], timeout=60)
    remote_head = ""
    if remote.get("ok") and remote.get("stdout"):
        remote_head = str(remote["stdout"]).split()[0]
    local_head = str(local.get("stdout") or "")
    return {
        "generated_utc": now_iso(),
        "phase": phase,
        "publication_branch": PUBLICATION_BRANCH,
        "local_head_at_receipt_generation": local_head,
        "remote_head_verified": remote_head,
        "remote_matches_local": bool(local_head and remote_head and local_head == remote_head),
    }


def write_publication_receipt(phase: str) -> None:
    publication = publication_result(phase)
    write_json(TRACE / f"{phase}-git-publication-result-v1.json", publication)
    write_text(TRACE / f"{phase}-git-publication-result-v1.md", report_markdown(f"{phase} git publication result", publication))


def write_phase(phase: str, promote: bool = True) -> None:
    health = runtime_health_gate(phase)
    providers = provider_probe(phase)
    plan = stage_plan(phase, health, providers)
    promotion = ensure_manifest_promotions(phase) if promote else {"phase": phase, "added_count": 0, "refreshed_count": 0}
    skill_pack = write_phase_skills(phase)
    command_pack = phase_command_pack(phase)
    command_validation = phase_command_validation(command_pack, skill_pack)
    artifacts: dict[str, Any] = {
        f"{phase}-runtime-health-gate-v1": health,
        f"{phase}-provider-readiness-probe-v1": providers,
        f"{phase}-source-digest-v1": source_digest(phase),
        f"{phase}-mcp-integration-digest-v1": mcp_integration_digest(phase),
        f"{phase}-web-research-snapshot-v1": web_research_snapshot(phase),
        f"{phase}-cli-identity-boundary-v1": cli_identity_boundary(phase),
        f"{phase}-stage-plan-v1": plan,
        f"{phase}-live-write-preflight-v1": live_write_preflight(phase),
        f"{phase}-open-source-expansion-scout-v1": source_scout(phase),
        f"{phase}-phase-skill-pack-v1": skill_pack,
        f"{phase}-phase-command-pack-v1": command_pack,
        f"{phase}-phase-command-validation-v1": command_validation,
        "v96-v120-system-expansion-candidate-pack-v1": candidate_pack_payload(phase, promotion),
        f"{phase}-stage-allowlist-v1": stage_allowlist(phase),
        f"{phase}-git-publication-result-v1": publication_result(phase),
    }
    if phase in ALPHA_PHASES or phase in PACKED_TRINITY_PHASES:
        artifacts[f"{phase}-alpha-cleanup-audit-v1"] = alpha_payload(phase)
    else:
        artifacts[f"{phase}-alpha-checkpoint-policy-v1"] = alpha_policy(phase)
    for stem, payload in artifacts.items():
        write_json(TRACE / f"{stem}.json", payload)
        write_text(TRACE / f"{stem}.md", report_markdown(stem, payload))
    report_dir = TRACE / f"{phase}-cli-reports"
    write_text(report_dir / f"{phase}-beta-eureka-plan-v1.md", beta_plan_markdown(phase, plan))
    write_text(report_dir / f"{phase}-personal-report-v1.md", personal_report_markdown(phase))
    write_json(DOCS / f"{phase}-beta-alpha-omega-closeout-summary-v1.json", closeout_payload(phase, promotion))
    if phase != "v120":
        write_json(DOCS / f"{next_phase(phase)}-beta-alpha-omega-handoff-policy-v1.json", handoff_payload(phase))


def main() -> int:
    parser = argparse.ArgumentParser(description="Write v96-v120 Beta-Alpha-Omega continuation artifacts.")
    parser.add_argument("--phase", required=True, choices=phase_choices())
    parser.add_argument("--no-promote", action="store_true")
    parser.add_argument("--receipt-only", action="store_true")
    args = parser.parse_args()
    if args.receipt_only:
        write_publication_receipt(args.phase)
        return 0
    write_phase(args.phase, promote=not args.no_promote)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
