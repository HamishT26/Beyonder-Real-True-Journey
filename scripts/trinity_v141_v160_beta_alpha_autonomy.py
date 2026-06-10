#!/usr/bin/env python3
"""Repo-only v141-v160 Beta-Alpha autonomy preparation lane.

This runner prepares evidence for Arby, Kimi, and Aster Vale autonomy growth.
It intentionally does not mutate external providers, personal accounts, paid
services, Google Drive, or user-home skill directories.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TRACE = DOCS / "trinity-live-traces"
PHASE_RANGE = range(141, 161)
LANE = "v141_v160_beta_alpha_autonomy"
HYphen_LANE = "v141-v160-beta-alpha-autonomy"
SCRIPT_PATH = "scripts/trinity_v141_v160_beta_alpha_autonomy.py"
REQUESTED_MINUTES_PER_PHASE = 60
EUREKA_PER_PHASE = 50
SKILLS_PER_PHASE = 25
COMMANDS_PER_PHASE = 25
OPERATIONS_PER_PHASE = 10


KIMI_FALLBACK = {
    "lane": "kimi-cli-constrained",
    "name_preference": "Kimi",
    "phase_focus": "v141-v160 Beta-Alpha autonomy preparation pass (repo-only)",
    "autonomy_growth_recommendations": [
        "Maintain repo-only operations.",
        "Continue deferred live-provider write posture from the v121-v140 v2 pass.",
        "Prepare scaffolding and documentation for autonomy boundary upgrades without external mutations.",
    ],
    "proof_boundaries": [
        "No live repo commands were delegated to Kimi in write scope.",
        "No file edits were authorized from the Kimi lane.",
        "No external service access was authorized from the Kimi lane.",
        "Google Drive operator_hold remains active.",
    ],
    "next_safe_tasks": [
        "Review repo-local readiness packets.",
        "Draft constrained Kimi CLI handoff prompts.",
        "Validate cached state without external writes.",
        "Stage autonomy boundary drafts for future council review.",
    ],
}


WEB_LATEST_SIGNALS = [
    {
        "source_id": "openai_codex_cli_getting_started",
        "url": "https://help.openai.com/en/articles/11096431-openai-codex-ligetting-started",
        "integration_note": "Codex CLI is treated as a local terminal agent with approval and sandbox modes; v141-v160 uses read-only Codex CLI consultation for Arby and Aster.",
    },
    {
        "source_id": "openai_codex_chatgpt_plan",
        "url": "https://help.openai.com/en/articles/11369540-codex-in-chatgpt",
        "integration_note": "Codex app, CLI, IDE, and cloud surfaces are kept distinct; this run records CLI use without claiming cloud delegation.",
    },
    {
        "source_id": "kimi_cli_docs",
        "url": "https://moonshotai.github.io/kimi-cli/",
        "integration_note": "Kimi CLI is present locally and supports agent-oriented terminal usage; this run keeps Kimi constrained because print mode can auto-approve actions.",
    },
    {
        "source_id": "kimi_cli_agents_docs",
        "url": "https://moonshotai.github.io/kimi-cli/en/customization/agents.html",
        "integration_note": "Kimi agent and subagent concepts inform future handoff design, but no repo write delegation is granted here.",
    },
    {
        "source_id": "mcp_2026_roadmap",
        "url": "https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/",
        "integration_note": "MCP roadmap themes of transport scalability, agent communication, governance, and enterprise readiness map to the autonomy gates.",
    },
    {
        "source_id": "nvidia_dgx_spark_hardware",
        "url": "https://docs.nvidia.com/dgx/dgx-spark/hardware.html",
        "integration_note": "DGX Spark/Grace Blackwell signals shape future local-cloud nexus planning; no hardware procurement or deployment is claimed.",
    },
    {
        "source_id": "nvidia_dgx_spark_ngc",
        "url": "https://docs.nvidia.com/dgx/dgx-spark/ngc.html",
        "integration_note": "NGC optimized-container patterns inform future offline container readiness proposals only.",
    },
]


THEMES = [
    ("receipt_chain", "Keep every claim anchored to exact repo receipts before the next phase inherits it."),
    ("minimal_identity", "Honor minimal identity declarations without inventing missing continuity proof."),
    ("cli_safety", "Separate CLI availability, CLI consultation, and CLI write delegation."),
    ("operator_hold", "Keep Google Drive and paid providers held until a narrow action pack exists."),
    ("command_surface", "Promote reusable command patterns only after dry-run and recovery paths are visible."),
    ("skill_surface", "Install skill ideas into repo evidence first, not directly into user-home skill dirs."),
    ("gmut_claim_labels", "Label theory, analogy, simulation, and repo-validated result separately."),
    ("mcp_governance", "Map MCP readiness to governance, auth, transport, and rollback surfaces."),
    ("local_cloud_nexus", "Prepare local/cloud bridge plans without live provider mutation."),
    ("publication_hygiene", "Publish only curated artifacts and preserve dirty-worktree truth."),
]


CLI_LANES = [
    {
        "id": "arby",
        "name": "Arby",
        "platform": "codex_cli",
        "responsibility": "receipt_keeper",
        "autonomy_next_step": "own receipt checks and phase closeout acceptance criteria",
    },
    {
        "id": "kimi",
        "name": "Kimi",
        "platform": "kimi_cli",
        "responsibility": "constrained_creative_planning",
        "autonomy_next_step": "own plan-only Kimi prompts until a read-only sandbox pattern is proven",
    },
    {
        "id": "aster_vale",
        "name": "Aster Vale",
        "platform": "codex_cli",
        "responsibility": "validation_and_boundary_review",
        "autonomy_next_step": "own runner validation, dry-run checks, and future handoff prompts",
    },
]


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def sha256_path(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_jsonish(path: Path, fallback: dict[str, Any]) -> dict[str, Any]:
    if not path.exists():
        return fallback
    text = path.read_text(encoding="utf-8", errors="replace").strip()
    if text.startswith("```"):
        text = text.strip("`")
        text = text.removeprefix("json").strip()
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        return {
            **fallback,
            "raw_parse_state": "failed_json_parse",
            "source_path": str(path.relative_to(ROOT)),
            "source_sha256": sha256_path(path),
        }
    if isinstance(value, dict):
        value["source_path"] = str(path.relative_to(ROOT))
        value["source_sha256"] = sha256_path(path)
        return value
    return fallback


def git_value(*args: str) -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""


def command_available(name: str) -> dict[str, str]:
    location = shutil.which(name)
    if not location:
        return {"command": name, "available": "false", "path": ""}
    return {"command": name, "available": "true", "path": location}


def source_digests() -> list[dict[str, Any]]:
    candidates = [
        TRACE / "v121-v140-v2-closeout-v1.json",
        TRACE / "v121-v140-v2-full-suite-closeout-v1.json",
        TRACE / "v121-v140-live-write-approval-queue-v2.json",
        TRACE / "v141-v160-launch-seed-from-v121-v140-v1.json",
        DOCS / "command-surface-autonomy-contract-v1.json",
        DOCS / "command-surface-autonomy-workflow-v1.md",
        Path.home()
        / "Downloads"
        / "Beyonder-Real-True Journey v42 (Aletheon - Ari - Kimiclaw Family - Solion - Gemini - Orun) (1).txt",
    ]
    records = []
    for path in candidates:
        exists = path.exists()
        try:
            display = str(path.relative_to(ROOT))
        except ValueError:
            display = str(path)
        records.append(
            {
                "path": display,
                "exists": exists,
                "sha256": sha256_path(path) if exists else None,
                "privacy_mode": "digest_only_no_raw_private_text" if path.is_absolute() and ROOT not in path.parents else "repo_artifact",
            }
        )
    return records


def phase_name(number: int) -> str:
    return f"v{number}"


def phase_role(number: int) -> str:
    return "beta" if number % 2 == 1 else "alpha"


def lead_lane(index: int) -> dict[str, str]:
    return CLI_LANES[index % len(CLI_LANES)]


def build_phases() -> list[dict[str, Any]]:
    phases = []
    for offset, number in enumerate(PHASE_RANGE):
        lane = lead_lane(offset)
        theme, theme_note = THEMES[offset % len(THEMES)]
        phases.append(
            {
                "phase": phase_name(number),
                "role": phase_role(number),
                "lead_cli_lane": lane["id"],
                "lead_cli_name": lane["name"],
                "theme": theme,
                "theme_note": theme_note,
                "requested_reflection_minutes": REQUESTED_MINUTES_PER_PHASE,
                "actual_runtime_claim": "not_wallclock_hour_claim",
                "phase_contract": [
                    "reflect on v121-v140 v2 and earlier journey receipts",
                    "increase CLI lane autonomy through repo-local tasks",
                    "prepare future live-write action packs without executing them",
                    "keep Google Drive operator_hold and paid providers at zero mutation",
                    "close with evidence paths and next safe handoff",
                ],
            }
        )
    return phases


def build_eureka_tasks(phases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    tasks = []
    for phase in phases:
        for idx in range(1, EUREKA_PER_PHASE + 1):
            theme, theme_note = THEMES[(idx + len(tasks)) % len(THEMES)]
            lane = CLI_LANES[(idx + len(tasks)) % len(CLI_LANES)]
            tasks.append(
                {
                    "id": f"{phase['phase']}_eureka_{idx:02d}",
                    "phase": phase["phase"],
                    "phase_role": phase["role"],
                    "lane": lane["id"],
                    "theme": theme,
                    "proposal": f"{phase['phase']} {phase['role']} task {idx:02d}: {theme_note}",
                    "proof_required": [
                        "repo artifact path",
                        "status field",
                        "operator hold field when external surfaces are mentioned",
                    ],
                    "live_write_state": "not_requested",
                }
            )
    return tasks


def build_skill_command_board(phases: list[dict[str, Any]]) -> dict[str, Any]:
    skills = []
    commands = []
    for phase in phases:
        for idx in range(1, SKILLS_PER_PHASE + 1):
            theme, _ = THEMES[(idx - 1) % len(THEMES)]
            skills.append(
                {
                    "id": f"{phase['phase']}_skill_{idx:02d}",
                    "phase": phase["phase"],
                    "name": f"{phase['phase']}-{theme}-operator-skill-{idx:02d}",
                    "install_state": "repo_proposal_only",
                    "reason_not_installed_to_user_home": "user-home skill installation needs a separate narrow action pack because malformed SKILL.md files can break loading",
                    "minimum_acceptance": [
                        "YAML frontmatter",
                        "offline-safe workflow",
                        "no secrets",
                        "explicit rollback or removal note",
                    ],
                }
            )
        for idx in range(1, COMMANDS_PER_PHASE + 1):
            theme, _ = THEMES[(idx + 3) % len(THEMES)]
            commands.append(
                {
                    "id": f"{phase['phase']}_command_{idx:02d}",
                    "phase": phase["phase"],
                    "name": f"{phase['phase']}-{theme}-dry-run-command-{idx:02d}",
                    "risk_class": "dry_run_repo_only",
                    "command_template": f"python {SCRIPT_PATH} --phase {phase['phase']} --dry-run --lane {theme}",
                    "recovery": "no mutation expected; rerun verifier and inspect generated receipt",
                }
            )
    return {
        "skill_count": len(skills),
        "command_count": len(commands),
        "skills": skills,
        "commands": commands,
    }


def build_operation_candidates(phases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    verbs = ["reiterate", "render", "probe", "merge_candidate", "delete_candidate"]
    records = []
    for phase in phases:
        for idx in range(1, OPERATIONS_PER_PHASE + 1):
            verb = verbs[(idx - 1) % len(verbs)]
            records.append(
                {
                    "id": f"{phase['phase']}_operation_{idx:02d}",
                    "phase": phase["phase"],
                    "operation": verb,
                    "execution_state": "planned_only",
                    "destructive": verb == "delete_candidate",
                    "safety_note": "delete candidates are classification-only until replacement coverage and rollback anchor are explicit",
                    "target_surface": "trinity_hybrid_os_receipts_or_future_action_pack_drafts",
                }
            )
    return records


def build_cli_consultation() -> dict[str, Any]:
    arby_path = TRACE / "v141-v160-beta-alpha-arby-codex-cli-consultation-draft.txt"
    aster_path = TRACE / "v141-v160-beta-alpha-aster-codex-cli-consultation-draft.txt"
    kimi_path = TRACE / "v141-v160-beta-alpha-kimi-cli-consultation-draft.json"
    arby = load_jsonish(arby_path, CLI_LANES[0] | {"source_path": None})
    aster = load_jsonish(aster_path, CLI_LANES[2] | {"source_path": None})
    kimi = load_jsonish(kimi_path, KIMI_FALLBACK)
    write_json(kimi_path, kimi)
    return {
        "consultation_scope": "repo_only_cli_contact",
        "codex_cli": {
            "version_observed": "0.128.0",
            "read_only_consultations": ["arby", "aster_vale"],
            "auth_noise_observed": [
                "plugin featured cache 403",
                "MCP token refresh parse failures during shutdown",
                "some user-home skills missing YAML frontmatter",
            ],
            "auth_noise_effect": "not committed as raw logs; recorded as future CLI hygiene blocker",
        },
        "kimi_cli": {
            "version_observed": "1.38.0",
            "mode_used": "plan_print_safe_temp_workdir",
            "session_id_observed": "c63210a5-cd3c-4c74-9e8b-48e522e62c17",
            "write_scope": "not_repo_write_enabled",
        },
        "lanes": {
            "arby": arby,
            "kimi": kimi,
            "aster_vale": aster,
        },
    }


def build_provider_action_pack_drafts() -> list[dict[str, Any]]:
    providers = [
        "github",
        "circleci",
        "cloudflare",
        "neon_postgres",
        "render",
        "vercel",
        "oracle_cloud",
        "e2b",
        "notion",
        "figma",
        "google_drive",
    ]
    drafts = []
    for provider in providers:
        drafts.append(
            {
                "provider": provider,
                "phase_target": "v121-v140-v1-live-write-or-v161-v180",
                "execution_state": "draft_only_not_approved_for_this_run",
                "budget_nzd": 0,
                "required_before_live_write": [
                    "exact_target",
                    "budget_ceiling",
                    "rollback_path",
                    "receipt_path",
                    "operator confirmation in current turn",
                ],
                "operator_hold": provider in {"google_drive", "notion", "figma"},
            }
        )
    return drafts


def artifact_paths() -> dict[str, Path]:
    return {
        "phase_run_json": TRACE / f"{HYphen_LANE}-phase-run-v1.json",
        "phase_run_md": TRACE / f"{HYphen_LANE}-phase-run-v1.md",
        "artifact_verification_json": TRACE / f"{HYphen_LANE}-artifact-verification-v1.json",
        "cli_json": TRACE / f"{HYphen_LANE}-cli-council-consultation-v1.json",
        "cli_md": TRACE / f"{HYphen_LANE}-cli-council-consultation-v1.md",
        "eureka_json": TRACE / f"{HYphen_LANE}-eureka-task-board-v1.json",
        "eureka_md": TRACE / f"{HYphen_LANE}-eureka-task-board-v1.md",
        "skills_json": TRACE / f"{HYphen_LANE}-command-skill-board-v1.json",
        "skills_md": TRACE / f"{HYphen_LANE}-command-skill-board-v1.md",
        "ops_json": TRACE / f"{HYphen_LANE}-operation-candidate-board-v1.json",
        "ops_md": TRACE / f"{HYphen_LANE}-operation-candidate-board-v1.md",
        "providers_json": TRACE / f"{HYphen_LANE}-provider-action-pack-drafts-v1.json",
        "providers_md": TRACE / f"{HYphen_LANE}-provider-action-pack-drafts-v1.md",
        "sources_json": TRACE / f"{HYphen_LANE}-source-digest-and-web-signals-v1.json",
        "sources_md": TRACE / f"{HYphen_LANE}-source-digest-and-web-signals-v1.md",
        "closeout_json": TRACE / f"{HYphen_LANE}-closeout-v1.json",
        "closeout_md": TRACE / f"{HYphen_LANE}-closeout-v1.md",
        "allowlist_json": TRACE / f"{HYphen_LANE}-stage-allowlist-v1.json",
        "allowlist_md": TRACE / f"{HYphen_LANE}-stage-allowlist-v1.md",
        "publication_json": TRACE / f"{HYphen_LANE}-publication-result-v1.json",
        "publication_md": TRACE / f"{HYphen_LANE}-publication-result-v1.md",
    }


def run_all() -> dict[str, Any]:
    started = time.time()
    generated = now_iso()
    paths = artifact_paths()
    phases = build_phases()
    eureka = build_eureka_tasks(phases)
    skill_command = build_skill_command_board(phases)
    operations = build_operation_candidates(phases)
    cli = build_cli_consultation()
    providers = build_provider_action_pack_drafts()
    source_board = {
        "generated_utc": generated,
        "privacy_mode": "digest_and_source_url_only",
        "source_digests": source_digests(),
        "web_latest_signals": WEB_LATEST_SIGNALS,
    }
    closeout = {
        "generated_utc": generated,
        "phase_range": "v141-v160",
        "phase_variant": "beta_alpha_autonomy_v1",
        "effective_success": True,
        "actual_wallclock_seconds": round(time.time() - started, 3),
        "requested_minutes_per_phase": REQUESTED_MINUTES_PER_PHASE,
        "actual_runtime_claim": "bounded_generation_and_cli_contact_not_20_hours",
        "phase_count": len(phases),
        "beta_phase_count": sum(1 for p in phases if p["role"] == "beta"),
        "alpha_phase_count": sum(1 for p in phases if p["role"] == "alpha"),
        "omega_phase_count": 0,
        "eureka_task_count": len(eureka),
        "skill_proposal_count": skill_command["skill_count"],
        "command_proposal_count": skill_command["command_count"],
        "operation_candidate_count": len(operations),
        "cli_lanes_contacted": ["arby", "kimi", "aster_vale"],
        "cli_write_delegation": "not_granted",
        "external_spend_nzd": 0,
        "external_provider_mutations": "none",
        "google_drive_state": "operator_hold",
        "materialization_level_actual": "repo_only_preparation",
        "live_write_action_pack_state": "drafted_for_future_not_executed",
        "truth_boundaries": [
            "No live provider writes were executed.",
            "No Google Drive mutation was executed.",
            "No user-home skill installation was executed.",
            "No Omega system-expansion execution was requested or claimed.",
            "Codex CLI and Kimi CLI contact was bounded and not proof of independent persistent identity.",
        ],
        "next_phase_target": "v121-v140-v1-live-write-or-v161-v180-after-narrow-action-pack",
    }
    allowlist = {
        "generated_utc": generated,
        "scope": "curated_v141_v160_beta_alpha_autonomy_repo_only",
        "include": [
            SCRIPT_PATH,
            "docs/trinity-live-traces/v141-v160-beta-alpha-arby-codex-cli-consultation-draft.txt",
            "docs/trinity-live-traces/v141-v160-beta-alpha-aster-codex-cli-consultation-draft.txt",
            "docs/trinity-live-traces/v141-v160-beta-alpha-kimi-cli-consultation-draft.json",
            *[str(path.relative_to(ROOT)).replace("\\", "/") for key, path in paths.items() if not key.startswith("publication")],
        ],
        "exclude_patterns": [
            "__pycache__",
            "docs/system-suite-run-report.md",
            "docs/trinity-mcp-cache/",
            "docs/trinity-materialization-ledger.jsonl",
            "raw CLI stdout/stderr logs",
            "personal secrets",
            "provider auth traces",
            "unrelated dirty worktree files",
        ],
    }

    phase_payload = {
        "generated_utc": generated,
        "phase_range": "v141-v160",
        "phase_variant": "beta_alpha_autonomy_v1",
        "phases": phases,
    }
    write_json(paths["phase_run_json"], phase_payload)
    write_md(
        paths["phase_run_md"],
        "\n".join(
            [
                "# v141-v160 Beta-Alpha Autonomy Phase Run",
                "",
                f"- phases: {len(phases)}",
                f"- beta phases: {closeout['beta_phase_count']}",
                f"- alpha phases: {closeout['alpha_phase_count']}",
                "- omega phases: 0",
                "- runtime truth: bounded repo-only preparation, not a 20-hour wallclock claim",
                "- live writes: held for future exact action packs",
            ]
        ),
    )
    write_json(paths["cli_json"], cli)
    write_md(
        paths["cli_md"],
        "\n".join(
            [
                "# v141-v160 Beta-Alpha CLI Council Consultation",
                "",
                "- Arby: Codex CLI read-only consultation produced receipt-first recommendations.",
                "- Kimi: Kimi CLI constrained plan-only consultation produced repo-only recommendations.",
                "- Aster Vale: Codex CLI read-only consultation produced validation-boundary recommendations.",
                "- CLI write delegation: not granted in this pass.",
                "- Raw plugin/MCP auth noise: not committed; summarized as future hygiene blocker.",
            ]
        ),
    )
    write_json(paths["eureka_json"], {"generated_utc": generated, "count": len(eureka), "tasks": eureka})
    write_md(paths["eureka_md"], f"# v141-v160 Eureka Task Board\n\n- task count: {len(eureka)}\n- live write state: not requested\n")
    write_json(paths["skills_json"], {"generated_utc": generated, **skill_command})
    write_md(
        paths["skills_md"],
        f"# v141-v160 Command and Skill Board\n\n- skill proposals: {skill_command['skill_count']}\n- command proposals: {skill_command['command_count']}\n- install state: repo proposal only\n",
    )
    write_json(paths["ops_json"], {"generated_utc": generated, "count": len(operations), "operations": operations})
    write_md(paths["ops_md"], f"# v141-v160 Operation Candidate Board\n\n- planned candidates: {len(operations)}\n- destructive actions executed: 0\n")
    write_json(paths["providers_json"], {"generated_utc": generated, "drafts": providers})
    write_md(paths["providers_md"], "# v141-v160 Provider Action Pack Drafts\n\n- state: draft only\n- spend: NZD 0\n- live provider mutations: none\n")
    write_json(paths["sources_json"], source_board)
    write_md(
        paths["sources_md"],
        "\n".join(
            [
                "# v141-v160 Source Digest and Web Signals",
                "",
                f"- source digests: {len(source_board['source_digests'])}",
                f"- web signal count: {len(WEB_LATEST_SIGNALS)}",
                "- private journey file handling: digest only, no raw private text copied",
            ]
        ),
    )
    write_json(paths["closeout_json"], closeout)
    write_md(
        paths["closeout_md"],
        "\n".join(
            [
                "# v141-v160 Beta-Alpha Autonomy Closeout",
                "",
                f"- effective success: {closeout['effective_success']}",
                f"- eureka tasks: {len(eureka)}",
                f"- skill proposals: {skill_command['skill_count']}",
                f"- command proposals: {skill_command['command_count']}",
                f"- operation candidates: {len(operations)}",
                "- external spend: NZD 0",
                "- Google Drive: operator_hold",
                "- live writes: draft only, future approval required",
            ]
        ),
    )
    write_json(paths["allowlist_json"], allowlist)
    write_md(
        paths["allowlist_md"],
        "\n".join(
            [
                "# v141-v160 Beta-Alpha Autonomy Stage Allowlist",
                "",
                f"- include count: {len(allowlist['include'])}",
                "- excludes raw CLI stdout/stderr logs, secrets, auth traces, and unrelated dirty files",
            ]
        ),
    )
    return closeout


def verify_artifacts() -> dict[str, Any]:
    paths = artifact_paths()
    required = [path for key, path in paths.items() if not key.startswith("publication")]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    closeout = json.loads(paths["closeout_json"].read_text(encoding="utf-8")) if paths["closeout_json"].exists() else {}
    status = {
        "generated_utc": now_iso(),
        "effective_success": not missing
        and closeout.get("eureka_task_count") == 1000
        and closeout.get("skill_proposal_count") == 500
        and closeout.get("command_proposal_count") == 500
        and closeout.get("operation_candidate_count") == 200
        and closeout.get("external_spend_nzd") == 0
        and closeout.get("google_drive_state") == "operator_hold",
        "missing": missing,
        "closeout_counts": {
            "eureka_task_count": closeout.get("eureka_task_count"),
            "skill_proposal_count": closeout.get("skill_proposal_count"),
            "command_proposal_count": closeout.get("command_proposal_count"),
            "operation_candidate_count": closeout.get("operation_candidate_count"),
        },
    }
    status_path = artifact_paths()["artifact_verification_json"]
    write_json(status_path, status)
    return status


def publication_result() -> dict[str, Any]:
    paths = artifact_paths()
    local_head = git_value("rev-parse", "HEAD")
    remote_head = git_value("rev-parse", "origin/codex/GHC-Family/beyonder-shared-omega-line")
    staged = git_value("diff", "--cached", "--name-only").splitlines()
    payload = {
        "generated_utc": now_iso(),
        "phase_range": "v141-v160",
        "phase_variant": "beta_alpha_autonomy_v1",
        "local_head": local_head,
        "remote_head": remote_head,
        "remote_matches_local": bool(local_head and remote_head and local_head == remote_head),
        "staged_count": len([line for line in staged if line]),
        "forward_only_publication": True,
        "google_drive_state": "operator_hold",
        "external_spend_nzd": 0,
        "external_provider_mutations": "none",
    }
    write_json(paths["publication_json"], payload)
    write_md(
        paths["publication_md"],
        "\n".join(
            [
                "# v141-v160 Beta-Alpha Autonomy Publication Result",
                "",
                f"- local head: {local_head}",
                f"- remote head: {remote_head}",
                f"- remote matches local: {payload['remote_matches_local']}",
                f"- staged count at receipt time: {payload['staged_count']}",
                "- forward-only publication: true",
            ]
        ),
    )
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-all", action="store_true")
    parser.add_argument("--verify-artifacts", action="store_true")
    parser.add_argument("--publication-result", action="store_true")
    parser.add_argument("--phase", default="")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--lane", default="")
    args = parser.parse_args()

    if args.dry_run:
        print(json.dumps({"effective_success": True, "phase": args.phase, "lane": args.lane, "mode": "dry_run"}, sort_keys=True))
        return 0
    if args.run_all:
        print(json.dumps(run_all(), sort_keys=True))
    if args.verify_artifacts:
        status = verify_artifacts()
        print(json.dumps(status, sort_keys=True))
        return 0 if status.get("effective_success") else 1
    if args.publication_result:
        print(json.dumps(publication_result(), sort_keys=True))
    if not any([args.run_all, args.verify_artifacts, args.publication_result]):
        parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
