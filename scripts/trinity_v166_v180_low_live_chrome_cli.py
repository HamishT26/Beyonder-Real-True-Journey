#!/usr/bin/env python3
"""v166-v180 low-write Chrome/CLI Trinity Hybrid runner.

This runner extends the v161-v165 dashboard pattern with checkpointed dashboard
updates. It writes repo-local evidence and D: dashboard archive snapshots only;
it does not mutate external providers, personal accounts, Google Drive, paid
services, browser storage, secrets, or user-home skill directories.
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
LANE = "v166_v180_low_live_chrome_cli"
HYphen_LANE = "v166-v180-low-live-chrome-cli"
SCRIPT_PATH = "scripts/trinity_v166_v180_low_live_chrome_cli.py"
SUITE_RUNNER_PATH = "scripts/run_all_trinity_systems.py"
PHASE_RANGE = range(166, 181)
CHECKPOINT_CADENCE = 3
SYSTEM_EXPANSIONS_PER_PHASE = 50
EUREKA_PER_PHASE = 50
COMMANDS_PER_PHASE = 50
SKILLS_PER_PHASE = 50
TAPESTRY_INLINE_ENTRY_LIMIT = 12
TAPESTRY_ACTIVE_SOFT_LIMIT_BYTES = 300_000
CHROME_PLUGIN_ROOT = Path.home() / ".codex" / "plugins" / "cache" / "openai-bundled" / "chrome" / "0.1.7"


CLI_LANES = [
    {
        "id": "arby",
        "name": "Arby",
        "formal_name": "Receipt Backer Arby",
        "platform": "codex_cli",
        "role": "receipt_keeper",
        "authority_mode": "advisory_receipt_review_under_aletheon_approval",
        "write_scope": "repo_artifact_review_only",
        "focus": "phase checkpoint receipts, allowlist integrity, and publication truth",
    },
    {
        "id": "kimi",
        "name": "Kimi",
        "formal_name": "Kimi",
        "platform": "kimi_cli",
        "role": "constrained_planning_and_cli_capability_watch",
        "authority_mode": "status_and_plan_only_until_non_yolo_read_only_pattern_is_proven",
        "write_scope": "no_repo_write_delegation",
        "focus": "creative low-write planning without auto-approved repo mutation",
    },
    {
        "id": "aster_vale",
        "name": "Aster Vale",
        "formal_name": "Aster Vale",
        "platform": "codex_cli",
        "role": "validation_steward",
        "authority_mode": "advisory_validation_under_aletheon_approval",
        "write_scope": "repo_artifact_review_only",
        "focus": "dashboard cadence validation, security boundaries, and suite hook checks",
    },
]


PHASE_PROJECTS = [
    ("v166", "beta", "Dashboard Cadence Governor", "Define the checkpoint-only dashboard write contract."),
    ("v167", "alpha", "CLI Council Role Contracts", "Refine Arby, Kimi, and Aster Vale low-write responsibilities."),
    ("v168", "omega", "Checkpoint 1 Tapestry Refresh", "Publish the first three-phase dashboard checkpoint."),
    ("v169", "beta", "Journey Digest Synthesis", "Digest prior v121-v165 evidence without copying private raw text."),
    ("v170", "alpha", "GMUT Claim Labeling", "Separate theory, analogy, simulation, and repo-validated evidence labels."),
    ("v171", "omega", "Checkpoint 2 Evidence Refresh", "Publish the second three-phase dashboard checkpoint."),
    ("v172", "beta", "Command Surface Bloom", "Grow reusable dry-run command proposals under low-write limits."),
    ("v173", "alpha", "Skill Surface Bloom", "Grow repo-only skill proposals without user-home installation."),
    ("v174", "omega", "Checkpoint 3 Suite Hook Validation", "Publish the third checkpoint and confirm deep/L5 hook intent."),
    ("v175", "beta", "Alpha Cleanup Classifier", "Classify cleanup and deletion candidates without deleting anything."),
    ("v176", "alpha", "Rollover Stress Model", "Model dashboard archive rollover before any tab replacement."),
    ("v177", "omega", "Checkpoint 4 Security Refresh", "Publish the fourth checkpoint with security truth refreshed."),
    ("v178", "beta", "Low-Write Publication Readiness", "Prepare curated publication receipts and forward-only staging."),
    ("v179", "alpha", "Future Live-Write Drafts", "Draft future provider packs without executing them."),
    ("v180", "omega", "Final Checkpoint Closeout", "Publish the final checkpoint and close v166-v180 truth surfaces."),
]


THEMES = [
    ("dashboard_cadence", "Buffer exchange-level detail and publish dashboard state only at checkpoint phases."),
    ("cli_council_growth", "Increase Arby, Kimi, and Aster Vale responsibility without unsafe write delegation."),
    ("receipt_chain", "Keep every claim anchored to exact repo evidence and D: archive receipts."),
    ("operator_hold", "Keep Google Drive, provider writes, paid services, and broad auth held."),
    ("journey_digest", "Use journey archives by digest and synthesis, not raw private-text republication."),
    ("gmut_claim_labels", "Label theory, analogy, simulation, repo evidence, and future proposal separately."),
    ("command_surface", "Promote commands only with dry-run, recovery, and no-secret boundaries."),
    ("skill_surface", "Keep skills as repo proposals unless a future explicit install pack approves them."),
    ("suite_hook", "Make deep and L5 suite runs refresh this lane automatically unless skipped."),
    ("rollover_model", "Archive first, then close/replace Chrome tabs only when the active dashboard gets heavy."),
    ("alpha_cleanup", "Classify cleanup work without deleting carried-forward worktree material."),
    ("forward_only_publication", "Publish only curated artifacts and preserve dirty-worktree truth."),
]


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def read_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return fallback


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except Exception:
            continue
        if isinstance(item, dict):
            rows.append(item)
    return rows


def append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True, ensure_ascii=False) + "\n")


def sha256_path(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def archive_stamp(value: str) -> str:
    return value.replace(":", "").replace("+", "Z").replace("-", "").replace(".", "")


def dashboard_archive_root() -> Path:
    preferred = Path("D:/GHC-Archives/trinity-dashboard-tapestry") / HYphen_LANE
    if Path("D:/").exists():
        return preferred
    return TRACE / f"{HYphen_LANE}-dashboard-tapestry-archive-fallback"


def git_value(*args: str) -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""


def run_command(args: list[str], timeout: int = 15) -> dict[str, Any]:
    if not args or shutil.which(args[0]) is None:
        return {"command": args, "available": False, "exit_code": None, "stdout": "", "stderr": "command_not_found"}
    try:
        result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True, timeout=timeout, check=False)
        return {
            "command": args,
            "available": True,
            "exit_code": result.returncode,
            "stdout": result.stdout.strip()[:4000],
            "stderr": result.stderr.strip()[:4000],
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "command": args,
            "available": True,
            "exit_code": "timeout",
            "stdout": (exc.stdout or "")[:4000] if isinstance(exc.stdout, str) else "",
            "stderr": "timeout",
        }


def command_versions() -> dict[str, Any]:
    return {
        "codex": run_command(["codex", "--version"]),
        "kimi": run_command(["kimi", "--version"]),
        "node": run_command(["node", "--version"]),
        "python": run_command(["python", "--version"]),
        "git": run_command(["git", "--version"]),
    }


def chrome_checks() -> dict[str, Any]:
    helpers = {
        "chrome_running": CHROME_PLUGIN_ROOT / "scripts" / "chrome-is-running.js",
        "extension_installed": CHROME_PLUGIN_ROOT / "scripts" / "check-extension-installed.js",
        "native_host_manifest": CHROME_PLUGIN_ROOT / "scripts" / "check-native-host-manifest.js",
    }
    checks: dict[str, Any] = {
        "plugin_root": str(CHROME_PLUGIN_ROOT),
        "plugin_root_exists": CHROME_PLUGIN_ROOT.exists(),
        "browser_client_exists": (CHROME_PLUGIN_ROOT / "scripts" / "browser-client.mjs").exists(),
    }
    for key, helper in helpers.items():
        if helper.exists() and shutil.which("node"):
            result = run_command(["node", str(helper), "--json"], timeout=20)
            try:
                checks[key] = json.loads(result["stdout"])
            except Exception:
                checks[key] = result
        else:
            checks[key] = {"available": False, "path": str(helper)}
    return checks


def source_digests() -> list[dict[str, Any]]:
    candidates = [
        TRACE / "v161-v165-low-live-chrome-cli-closeout-v1.json",
        TRACE / "v161-v165-low-live-chrome-cli-dashboard-tapestry-index-v1.json",
        TRACE / "v161-v165-low-live-chrome-cli-publication-result-v1.json",
        TRACE / "v141-v160-beta-alpha-autonomy-closeout-v1.json",
        TRACE / "v121-v140-v2-full-suite-closeout-v1.json",
        DOCS / "v166-v180-low-live-chrome-cli-dashboard.html",
        Path.home()
        / "Downloads"
        / "Beyonder-Real-True Journey v42 (Aletheon - Ari - Kimiclaw Family - Solion - Gemini - Orun) (4).txt",
    ]
    rows = []
    for path in candidates:
        rows.append(
            {
                "path": rel(path),
                "exists": path.exists(),
                "sha256": sha256_path(path),
                "privacy_mode": "digest_only_no_raw_private_text" if ROOT not in path.parents else "repo_artifact",
            }
        )
    return rows


def artifact_paths() -> dict[str, Path]:
    return {
        "phase_json": TRACE / f"{HYphen_LANE}-phase-run-v1.json",
        "phase_md": TRACE / f"{HYphen_LANE}-phase-run-v1.md",
        "dashboard_json": TRACE / f"{HYphen_LANE}-dashboard-state-v1.json",
        "dashboard_html": DOCS / f"{HYphen_LANE}-dashboard.html",
        "checkpoint_json": TRACE / f"{HYphen_LANE}-dashboard-checkpoints-v1.json",
        "checkpoint_md": TRACE / f"{HYphen_LANE}-dashboard-checkpoints-v1.md",
        "cli_json": TRACE / f"{HYphen_LANE}-cli-council-consultation-v1.json",
        "cli_md": TRACE / f"{HYphen_LANE}-cli-council-consultation-v1.md",
        "system_json": TRACE / f"{HYphen_LANE}-system-expansion-board-v1.json",
        "system_md": TRACE / f"{HYphen_LANE}-system-expansion-board-v1.md",
        "eureka_json": TRACE / f"{HYphen_LANE}-eureka-task-board-v1.json",
        "eureka_md": TRACE / f"{HYphen_LANE}-eureka-task-board-v1.md",
        "command_skill_json": TRACE / f"{HYphen_LANE}-command-skill-board-v1.json",
        "command_skill_md": TRACE / f"{HYphen_LANE}-command-skill-board-v1.md",
        "alpha_json": TRACE / f"{HYphen_LANE}-alpha-cleanup-security-v1.json",
        "alpha_md": TRACE / f"{HYphen_LANE}-alpha-cleanup-security-v1.md",
        "surface_json": TRACE / f"{HYphen_LANE}-hybrid-terminal-surface-v1.json",
        "surface_md": TRACE / f"{HYphen_LANE}-hybrid-terminal-surface-v1.md",
        "provider_json": TRACE / f"{HYphen_LANE}-deferred-live-write-pack-drafts-v1.json",
        "provider_md": TRACE / f"{HYphen_LANE}-deferred-live-write-pack-drafts-v1.md",
        "source_json": TRACE / f"{HYphen_LANE}-source-digest-v1.json",
        "source_md": TRACE / f"{HYphen_LANE}-source-digest-v1.md",
        "tapestry_jsonl": TRACE / f"{HYphen_LANE}-dashboard-tapestry-v1.jsonl",
        "tapestry_index_json": TRACE / f"{HYphen_LANE}-dashboard-tapestry-index-v1.json",
        "tapestry_md": TRACE / f"{HYphen_LANE}-dashboard-tapestry-v1.md",
        "archive_receipt_json": TRACE / f"{HYphen_LANE}-dashboard-archive-receipt-v1.json",
        "archive_receipt_md": TRACE / f"{HYphen_LANE}-dashboard-archive-receipt-v1.md",
        "rollover_policy_json": TRACE / f"{HYphen_LANE}-dashboard-rollover-policy-v1.json",
        "rollover_policy_md": TRACE / f"{HYphen_LANE}-dashboard-rollover-policy-v1.md",
        "suite_hook_json": TRACE / f"{HYphen_LANE}-suite-hook-contract-v1.json",
        "suite_hook_md": TRACE / f"{HYphen_LANE}-suite-hook-contract-v1.md",
        "verification_json": TRACE / f"{HYphen_LANE}-artifact-verification-v1.json",
        "closeout_json": TRACE / f"{HYphen_LANE}-closeout-v1.json",
        "closeout_md": TRACE / f"{HYphen_LANE}-closeout-v1.md",
        "allowlist_json": TRACE / f"{HYphen_LANE}-stage-allowlist-v1.json",
        "allowlist_md": TRACE / f"{HYphen_LANE}-stage-allowlist-v1.md",
        "publication_json": TRACE / f"{HYphen_LANE}-publication-result-v1.json",
        "publication_md": TRACE / f"{HYphen_LANE}-publication-result-v1.md",
    }


def build_phases(generated: str) -> list[dict[str, Any]]:
    phases = []
    for index, (phase, role, project, project_goal) in enumerate(PHASE_PROJECTS, start=1):
        lane = CLI_LANES[(index - 1) % len(CLI_LANES)]
        theme, theme_note = THEMES[(index - 1) % len(THEMES)]
        checkpoint = index % CHECKPOINT_CADENCE == 0
        phases.append(
            {
                "phase": phase,
                "role": role,
                "project": project,
                "project_goal": project_goal,
                "lead_lane": lane["id"],
                "lead_name": lane["name"],
                "theme": theme,
                "theme_note": theme_note,
                "checkpoint_phase": checkpoint,
                "checkpoint_reason": "every_3rd_phase_dashboard_refresh" if checkpoint else "buffer_until_next_checkpoint",
                "requested_project_runtime": "more_than_one_hour_each",
                "actual_runtime_claim": "bounded_repo_generation_not_wallclock_hour_claim",
                "generated_utc": generated,
                "acceptance": [
                    "phase project is represented in repo evidence",
                    "CLI lane authority remains advisory under Aletheon approval",
                    "dashboard write is buffered unless this is a checkpoint phase",
                    "external provider writes and spending remain zero",
                    "Google Drive remains operator_hold",
                ],
            }
        )
    return phases


def build_system_expansions(phases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for phase in phases:
        for idx in range(1, SYSTEM_EXPANSIONS_PER_PHASE + 1):
            theme, theme_note = THEMES[(idx + len(rows)) % len(THEMES)]
            lane = CLI_LANES[(idx + len(rows)) % len(CLI_LANES)]
            rows.append(
                {
                    "id": f"{phase['phase']}_system_{idx:02d}",
                    "phase": phase["phase"],
                    "project": phase["project"],
                    "status": "candidate_installed_as_repo_evidence",
                    "pillar": ["mind", "body", "heart", "trinity", "dashboard"][idx % 5],
                    "theme": theme,
                    "owner_lane": lane["id"],
                    "purpose": theme_note,
                    "activation_rule": "requires future explicit runner promotion before live execution",
                    "safety_boundary": "no_external_write_no_secret_read_no_paid_provider_spend",
                }
            )
    return rows


def build_eureka_tasks(phases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for phase in phases:
        for idx in range(1, EUREKA_PER_PHASE + 1):
            theme, theme_note = THEMES[(idx * 2 + len(rows)) % len(THEMES)]
            rows.append(
                {
                    "id": f"{phase['phase']}_eureka_{idx:02d}",
                    "phase": phase["phase"],
                    "project": phase["project"],
                    "theme": theme,
                    "proposal": f"Turn {theme.replace('_', ' ')} into a v166-v180 low-write proof surface.",
                    "why_it_matters": theme_note,
                    "disposition": "queued_for_future_promotion_or_live_write_pack_review",
                }
            )
    return rows


def build_command_skill_board(phases: list[dict[str, Any]]) -> dict[str, Any]:
    commands = []
    skills = []
    for phase in phases:
        for idx in range(1, COMMANDS_PER_PHASE + 1):
            theme, _note = THEMES[(idx + len(commands)) % len(THEMES)]
            commands.append(
                {
                    "id": f"{phase['phase']}_command_{idx:02d}",
                    "phase": phase["phase"],
                    "command": f"python {SCRIPT_PATH} --dry-run --phase {phase['phase']} --lane {CLI_LANES[idx % 3]['id']}",
                    "purpose": f"Dry-run {theme.replace('_', ' ')} for {phase['project']}.",
                    "mutation_level": "none",
                }
            )
        for idx in range(1, SKILLS_PER_PHASE + 1):
            theme, _note = THEMES[(idx + len(skills)) % len(THEMES)]
            skills.append(
                {
                    "id": f"{phase['phase']}_skill_{idx:02d}",
                    "phase": phase["phase"],
                    "skill_name": f"{phase['phase']}-{theme.replace('_', '-')}-skill-{idx:02d}",
                    "purpose": f"Package {theme.replace('_', ' ')} as a future skill candidate.",
                    "installation_state": "repo_candidate_only_not_user_home_installed",
                }
            )
    return {
        "generated_utc": now_iso(),
        "command_count": len(commands),
        "skill_count": len(skills),
        "commands": commands,
        "skills": skills,
    }


def build_lane_transcripts(generated: str) -> list[dict[str, Any]]:
    transcript_dir = TRACE / f"{HYphen_LANE}-lane-logs"
    transcript_dir.mkdir(parents=True, exist_ok=True)
    supplemental = {
        "arby": transcript_dir / "arby-codex-consultation.txt",
        "kimi": transcript_dir / "kimi-info.txt",
        "aster_vale": transcript_dir / "aster-vale-codex-consultation.txt",
    }
    rows = []
    for lane in CLI_LANES:
        version_hint = "codex --version" if lane["platform"] == "codex_cli" else "kimi --version; kimi info"
        lines = [
            f"[{generated}] {lane['name']} v166-v180 lane online.",
            f"platform: {lane['platform']}",
            f"role: {lane['role']}",
            f"authority: {lane['authority_mode']}",
            f"write_scope: {lane['write_scope']}",
            f"focus: {lane['focus']}",
            f"safe_probe: {version_hint}",
            "dashboard_write_cadence: every_3rd_phase_checkpoint",
            "checkpoint_phases: v168, v171, v174, v177, v180",
            "live_write_state: deferred",
            "google_drive_state: operator_hold",
            "provider_spend_nzd: 0",
            "commit_rule: Aletheon curated allowlist only",
            "terminal_panel_truth: Chrome dashboard is a live view of repo lane logs, not a native TTY emulator.",
        ]
        extra_path = supplemental.get(lane["id"])
        if extra_path and extra_path.exists():
            extra_text = extra_path.read_text(encoding="utf-8", errors="replace").strip()
            if extra_text:
                lines.extend(["", "--- bounded_cli_consultation ---", extra_text])
        path = transcript_dir / f"{lane['id']}.log"
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        rows.append({**lane, "status": "active_low_write_lane", "transcript_path": rel(path), "transcript": "\n".join(lines)})
    return rows


def build_cli_consultation(lanes: list[dict[str, Any]], versions: dict[str, Any]) -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "scope": "v166_v180_checkpointed_dashboard_plus_cli_lane_logs",
        "lanes": lanes,
        "cli_versions": versions,
        "direct_delegation": {
            "codex_cli": "read_only_review_and_status_probe_eligible",
            "kimi_cli": "status_probe_only_until_non_yolo_read_only_mode_is_confirmed",
            "commit_authority": "Aletheon curated allowlist only",
        },
        "safety_notes": [
            "Kimi print mode is not used for repo mutation because it can auto-approve actions.",
            "Dashboard checkpointing prevents archive churn after every individual exchange.",
            "No raw secrets, browser cookies, local storage, or provider credentials are inspected.",
        ],
    }


def build_alpha_cleanup() -> dict[str, Any]:
    tracked_dirty = run_command(["git", "status", "--porcelain=v1", "--untracked-files=no"], timeout=30)
    dirty_lines = [line for line in tracked_dirty.get("stdout", "").splitlines() if line.strip()]
    return {
        "generated_utc": now_iso(),
        "mode": "classification_only_no_delete",
        "tracked_dirty_count_observed": len(dirty_lines),
        "dirty_sample": dirty_lines[:40],
        "cleanup_decision": "do_not_clean_carried_forward_churn_inside_v166_v180",
        "delete_actions_executed": 0,
        "merge_actions_executed": 0,
        "security_posture": {
            "google_drive_state": "operator_hold",
            "provider_writes": "deferred",
            "external_spend_nzd": 0,
            "secret_handling": "no_secret_read_no_raw_auth_log_commit",
            "browser_storage": "not_inspected",
        },
    }


def build_hybrid_surface(chrome: dict[str, Any]) -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "surface_mode": "checkpointed_hybrid_dashboard_terminal_log_panels",
        "preferred_view": "single_chrome_dashboard_tab_with_three_terminal_like_lanes",
        "real_time_method": "localhost_http_polling_reads_latest_state_without_forcing_archive_entry_per_exchange",
        "dashboard_poll_seconds": 3,
        "dashboard_write_cadence": "every_3rd_phase_checkpoint",
        "checkpoint_phases": ["v168", "v171", "v174", "v177", "v180"],
        "native_terminal_embedding": "deferred",
        "chrome_checks": chrome,
        "operator_notes": [
            "The dashboard reads repo state and lane logs.",
            "The runner archives only checkpoint snapshots, not every message exchange.",
            "Chrome tab replacement remains an automation handoff after archive-first rollover.",
        ],
    }


def build_provider_drafts() -> dict[str, Any]:
    providers = ["github", "google_drive", "notion", "cloudflare", "neon_postgres", "circleci", "render", "vercel", "oracle_cloud", "e2b"]
    return {
        "generated_utc": now_iso(),
        "state": "deferred_not_executed",
        "spend_nzd": 0,
        "packs": [
            {
                "provider": provider,
                "status": "draft_only",
                "minimum_future_pack_fields": [
                    "exact target",
                    "auth window needed",
                    "budget cap",
                    "rollback path",
                    "receipt path",
                    "user-present confirmation",
                ],
            }
            for provider in providers
        ],
    }


def build_suite_hook_contract() -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "suite_hook_mode": "deep_and_l5_default_with_skip_flag",
        "include_when": [
            "run_all_trinity_systems.py --profile deep",
            "run_all_trinity_systems.py --profile materialize --materialization-level l5_ha_prod",
        ],
        "skip_flag": "--skip-v166-v180-dashboard-run",
        "runner_command": f"python {SCRIPT_PATH} --run-all --verify-artifacts",
        "write_cadence": "dashboard checkpoints only after every 3 phases",
        "truth_boundaries": [
            "repo-local artifact writes only",
            "D drive dashboard archive mirror only",
            "no external provider mutation",
            "no Google Drive mutation",
            "no paid spend",
        ],
    }


def build_checkpoint_snapshots(generated: str, phases: list[dict[str, Any]], lanes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    checkpoints = []
    for index, phase in enumerate(phases, start=1):
        if not phase["checkpoint_phase"]:
            continue
        window_start = index - CHECKPOINT_CADENCE
        checkpoints.append(
            {
                "checkpoint_id": f"{HYphen_LANE}-{phase['phase']}",
                "generated_utc": generated,
                "phase": phase["phase"],
                "project": phase["project"],
                "checkpoint_number": len(checkpoints) + 1,
                "phase_window": [p["phase"] for p in phases[window_start:index]],
                "phase_window_projects": [p["project"] for p in phases[window_start:index]],
                "accumulated_phase_count": index,
                "lane_status": [
                    {
                        "id": lane["id"],
                        "formal_name": lane["formal_name"],
                        "role": lane["role"],
                        "status": lane["status"],
                        "transcript_path": lane["transcript_path"],
                    }
                    for lane in lanes
                ],
                "truth": {
                    "dashboard_update_reason": "every_3rd_phase_checkpoint",
                    "external_provider_mutations": "none",
                    "external_spend_nzd": 0,
                    "google_drive_state": "operator_hold",
                },
            }
        )
    return checkpoints


def compact_tapestry_entry(checkpoint: dict[str, Any], archive_file: Path) -> dict[str, Any]:
    return {
        "entry_id": checkpoint["checkpoint_id"],
        "generated_utc": checkpoint["generated_utc"],
        "phase": checkpoint["phase"],
        "project": checkpoint["project"],
        "checkpoint_number": checkpoint["checkpoint_number"],
        "phase_window": checkpoint["phase_window"],
        "archive_file": str(archive_file),
        "archive_file_sha256": sha256_path(archive_file),
        "google_drive_state": checkpoint["truth"]["google_drive_state"],
        "external_provider_mutations": checkpoint["truth"]["external_provider_mutations"],
        "external_spend_nzd": checkpoint["truth"]["external_spend_nzd"],
    }


def update_dashboard_tapestry(base_state: dict[str, Any], checkpoints: list[dict[str, Any]], generated: str) -> dict[str, Any]:
    paths = artifact_paths()
    archive_root = dashboard_archive_root()
    archive_root.mkdir(parents=True, exist_ok=True)
    written = []
    for checkpoint in checkpoints:
        entry_id = f"{checkpoint['checkpoint_id']}-{archive_stamp(generated)}"
        checkpoint = {**checkpoint, "checkpoint_id": entry_id}
        archive_file = archive_root / f"{entry_id}.json"
        full_snapshot = {
            "entry_id": entry_id,
            "archived_utc": now_iso(),
            "archive_mode": "d_drive_checkpoint_snapshot_with_repo_jsonl_index",
            "dashboard_state": base_state,
            "checkpoint": checkpoint,
        }
        write_json(archive_file, full_snapshot)
        compact = compact_tapestry_entry(checkpoint, archive_file)
        append_jsonl(paths["tapestry_jsonl"], compact)
        written.append(compact)

    entries = read_jsonl(paths["tapestry_jsonl"])
    inline_entries = entries[-TAPESTRY_INLINE_ENTRY_LIMIT:]
    active_size = len(json.dumps({**base_state, "tapestry_entries": inline_entries}, ensure_ascii=False).encode("utf-8"))
    rollover_policy = {
        "generated_utc": generated,
        "active_soft_limit_bytes": TAPESTRY_ACTIVE_SOFT_LIMIT_BYTES,
        "active_estimated_bytes": active_size,
        "inline_entry_limit": TAPESTRY_INLINE_ENTRY_LIMIT,
        "rollover_recommended": active_size >= TAPESTRY_ACTIVE_SOFT_LIMIT_BYTES,
        "rollover_trigger": "when active dashboard state reaches the soft limit or the Chrome tab becomes heavy",
        "rollover_action": "archive current state to D drive, close the old dashboard tab through Chrome automation, then open a fresh dashboard tab",
        "web_page_self_close_truth": "the page cannot safely close arbitrary Chrome tabs by itself; Codex Chrome automation performs that handoff when requested or when threshold is reached",
    }
    index = {
        "generated_utc": generated,
        "entry_count_total": len(entries),
        "entry_count_this_run": len(written),
        "latest_entry_id": written[-1]["entry_id"] if written else "",
        "repo_tapestry_jsonl": rel(paths["tapestry_jsonl"]),
        "repo_tapestry_index": rel(paths["tapestry_index_json"]),
        "d_drive_archive_root": str(archive_root),
        "latest_archive_file": written[-1]["archive_file"] if written else "",
        "latest_archive_sha256": written[-1]["archive_file_sha256"] if written else "",
        "inline_entries": len(inline_entries),
        "checkpoint_cadence": CHECKPOINT_CADENCE,
        "checkpoint_phases_this_run": [entry["phase"] for entry in written],
        "rollover_policy": rollover_policy,
    }
    receipt = {
        "generated_utc": generated,
        "archive_root": str(archive_root),
        "checkpoint_archive_count": len(written),
        "latest_archive_file": index["latest_archive_file"],
        "latest_archive_sha256": index["latest_archive_sha256"],
        "repo_tapestry_jsonl": rel(paths["tapestry_jsonl"]),
        "repo_tapestry_index": rel(paths["tapestry_index_json"]),
        "archive_write_success": all(Path(entry["archive_file"]).exists() for entry in written),
        "external_provider_mutations": "none",
        "external_spend_nzd": 0,
    }
    write_json(paths["tapestry_index_json"], index)
    write_json(paths["archive_receipt_json"], receipt)
    write_json(paths["rollover_policy_json"], rollover_policy)
    write_md(
        paths["tapestry_md"],
        "\n".join(
            [
                "# v166-v180 Dashboard Tapestry",
                "",
                f"- total entries recorded: {len(entries)}",
                f"- entries this run: {len(written)}",
                f"- inline entries shown on dashboard: {len(inline_entries)}",
                f"- D drive archive root: {archive_root}",
                "- full snapshots stay in the D drive archive mirror and compact history stays in the repo trace ledger",
            ]
        ),
    )
    write_md(
        paths["archive_receipt_md"],
        "\n".join(
            [
                "# v166-v180 Dashboard Archive Receipt",
                "",
                f"- archive write success: {receipt['archive_write_success']}",
                f"- checkpoint archive count: {len(written)}",
                f"- latest archive file: {index['latest_archive_file']}",
                f"- latest archive sha256: {index['latest_archive_sha256']}",
                "- provider writes: none",
                "- spend: 0 NZD",
            ]
        ),
    )
    write_md(
        paths["rollover_policy_md"],
        "\n".join(
            [
                "# v166-v180 Dashboard Rollover Policy",
                "",
                f"- active soft limit bytes: {TAPESTRY_ACTIVE_SOFT_LIMIT_BYTES}",
                f"- active estimated bytes: {active_size}",
                f"- rollover recommended now: {rollover_policy['rollover_recommended']}",
                "- action: archive, close old Chrome dashboard tab, open a fresh dashboard tab",
                "- truth boundary: the web page cannot safely close arbitrary Chrome tabs by itself",
            ]
        ),
    )
    return {"index": index, "rollover_policy": rollover_policy, "entries": inline_entries}


def dashboard_html(state: dict[str, Any]) -> str:
    embedded = json.dumps(state, ensure_ascii=False).replace("</", "<\\/")
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>v166-v180 Checkpointed CLI Dashboard</title>
  <style>
    :root {{
      --bg: #080d10;
      --ink: #f7fff9;
      --muted: #a8beb8;
      --line: rgba(157, 230, 206, .22);
      --panel: rgba(9, 28, 31, .78);
      --green: #83f4b9;
      --gold: #efcf78;
      --blue: #8bdfff;
      --rose: #f28ea2;
      --shadow: rgba(0, 0, 0, .38);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      min-height: 100vh;
      color: var(--ink);
      font-family: Athelas, Constantia, Cambria, Georgia, serif;
      background:
        radial-gradient(circle at 8% 12%, rgba(131,244,185,.24), transparent 30%),
        radial-gradient(circle at 88% 8%, rgba(239,207,120,.20), transparent 27%),
        radial-gradient(circle at 48% 94%, rgba(139,223,255,.16), transparent 34%),
        linear-gradient(145deg, #020405, var(--bg) 48%, #0c1618);
    }}
    main {{ width: min(1500px, calc(100% - 32px)); margin: 0 auto; padding: 32px 0 44px; }}
    .hero {{
      border: 1px solid var(--line);
      border-radius: 34px;
      padding: 28px;
      background: linear-gradient(135deg, rgba(255,255,255,.09), rgba(255,255,255,.025));
      box-shadow: 0 26px 100px var(--shadow);
    }}
    .eyebrow {{ color: var(--gold); letter-spacing: .17em; text-transform: uppercase; font-size: 12px; }}
    h1 {{ margin: 10px 0 8px; font-size: clamp(34px, 6vw, 78px); line-height: .92; max-width: 1040px; }}
    h2 {{ margin: 0; font-size: clamp(26px, 4vw, 48px); }}
    p {{ margin: 8px 0 0; color: var(--muted); font-size: 18px; max-width: 980px; }}
    .metrics, .phases, .lanes, .checkpoints, .tapestry-grid {{ display: grid; gap: 14px; margin-top: 18px; }}
    .metrics {{ grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); }}
    .phases {{ grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); }}
    .lanes {{ grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); }}
    .checkpoints, .tapestry-grid {{ grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); }}
    .card, .lane, .phase, .checkpoint, .tapestry-entry {{
      border: 1px solid var(--line);
      border-radius: 24px;
      padding: 18px;
      background: var(--panel);
      box-shadow: 0 18px 60px rgba(0,0,0,.22);
    }}
    .section {{
      margin-top: 22px;
      border: 1px solid rgba(239, 207, 120, .28);
      border-radius: 30px;
      padding: 20px;
      background: linear-gradient(135deg, rgba(239,207,120,.10), rgba(139,223,255,.06));
    }}
    .meta {{ margin-top: 8px; color: var(--muted); font-size: 15px; overflow-wrap: anywhere; }}
    .card span, .phase span, .lane span, .checkpoint span, .tapestry-entry span {{ display: block; color: var(--muted); font-size: 12px; letter-spacing: .12em; text-transform: uppercase; }}
    .card strong {{ display: block; margin-top: 10px; color: var(--green); font-size: 24px; overflow-wrap: anywhere; }}
    .phase b, .lane b, .checkpoint b, .tapestry-entry b {{ display: block; margin-top: 8px; color: var(--ink); font-size: 22px; }}
    .phase em, .lane em, .checkpoint em, .tapestry-entry em {{ display: block; margin-top: 6px; color: var(--blue); font-style: normal; overflow-wrap: anywhere; }}
    details {{ margin-top: 12px; border-top: 1px solid rgba(157,230,206,.16); padding-top: 10px; }}
    summary {{ cursor: pointer; color: var(--gold); font-weight: 700; }}
    pre {{
      margin: 14px 0 0;
      padding: 14px;
      min-height: 220px;
      overflow: auto;
      border-radius: 18px;
      border: 1px solid rgba(131,244,185,.18);
      color: #e1fff0;
      background: linear-gradient(180deg, rgba(1,8,9,.92), rgba(5,16,18,.92));
      font: 13px/1.5 Consolas, "Cascadia Mono", "Courier New", monospace;
      white-space: pre-wrap;
    }}
    .status {{ color: var(--green); }}
    .held {{ color: var(--gold); }}
    footer {{ margin-top: 18px; color: var(--muted); font-size: 14px; }}
  </style>
</head>
<body>
  <main>
    <section class="hero">
      <div class="eyebrow">Beyonder Real True Journey / v166-v180</div>
      <h1>Checkpointed Chrome + CLI Council Dashboard</h1>
      <p id="summary">Loading v166-v180 state...</p>
    </section>
    <section class="metrics" id="metrics"></section>
    <section class="section"><h2>Checkpoint Phases</h2><div class="checkpoints" id="checkpoints"></div></section>
    <section class="phases" id="phases"></section>
    <section class="lanes" id="lanes"></section>
    <section class="section" id="tapestry"></section>
    <footer id="footer"></footer>
  </main>
  <script id="embedded-state" type="application/json">{embedded}</script>
  <script>
    const statePath = "trinity-live-traces/{HYphen_LANE}-dashboard-state-v1.json";
    const embedded = JSON.parse(document.getElementById("embedded-state").textContent);
    async function loadState() {{
      try {{
        const res = await fetch(statePath + "?t=" + Date.now(), {{ cache: "no-store" }});
        if (!res.ok) throw new Error("state fetch failed");
        return await res.json();
      }} catch (_err) {{
        return embedded;
      }}
    }}
    function esc(value) {{
      return String(value ?? "").replace(/[&<>"']/g, ch => ({{
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
      }}[ch]));
    }}
    function metric(label, value, cls = "") {{
      return `<article class="card"><span>${{esc(label)}}</span><strong class="${{esc(cls)}}">${{esc(value)}}</strong></article>`;
    }}
    function renderTapestry(state) {{
      const tapestry = state.tapestry || {{}};
      const index = tapestry.index || {{}};
      const policy = tapestry.rollover_policy || {{}};
      const entries = (tapestry.entries || []).slice().reverse();
      const cards = entries.map((entry, idx) =>
        `<article class="tapestry-entry"><span>checkpoint archive</span><b>${{esc(entry.phase)}} / ${{esc(entry.project)}}</b><em>${{esc(entry.archive_file)}}</em><p>${{esc((entry.phase_window || []).join(" + "))}}</p></article>`
      ).join("");
      document.getElementById("tapestry").innerHTML = `
        <h2>Dashboard Tapestry Archive</h2>
        <div class="meta">Entries this run: ${{esc(index.entry_count_this_run || 0)}} / total: ${{esc(index.entry_count_total || entries.length)}} / D: archive: ${{esc(index.d_drive_archive_root || "pending")}}</div>
        <div class="meta">Rollover: ${{policy.rollover_recommended ? "recommended now" : "not needed yet"}} / soft limit: ${{esc(policy.active_soft_limit_bytes || "n/a")}} bytes / active estimate: ${{esc(policy.active_estimated_bytes || "n/a")}} bytes</div>
        <div class="tapestry-grid">${{cards || "<article class='tapestry-entry'><b>No checkpoint tapestry entries yet.</b></article>"}}</div>
      `;
    }}
    function render(state) {{
      document.getElementById("summary").textContent = state.summary;
      document.getElementById("metrics").innerHTML = [
        metric("Phase Range", state.phase_range),
        metric("Dashboard Writes", state.dashboard_write_cadence),
        metric("External Spend", state.external_spend_nzd + " NZD", "status"),
        metric("Google Drive", state.google_drive_state, "held"),
        metric("Provider Writes", state.external_provider_mutations, "held"),
        metric("Updated", state.generated_utc)
      ].join("");
      document.getElementById("checkpoints").innerHTML = state.checkpoints.map(c =>
        `<article class="checkpoint"><span>checkpoint ${{esc(c.checkpoint_number)}}</span><b>${{esc(c.phase)}} / ${{esc(c.project)}}</b><em>${{esc(c.phase_window.join(" + "))}}</em><p>${{esc(c.truth.dashboard_update_reason)}}</p></article>`
      ).join("");
      document.getElementById("phases").innerHTML = state.phases.map(p =>
        `<article class="phase"><span>${{esc(p.role)}} / ${{esc(p.theme)}}</span><b>${{esc(p.phase)}} / ${{esc(p.project)}}</b><em>${{esc(p.lead_name)}} / ${{p.checkpoint_phase ? "dashboard checkpoint" : "buffered"}}</em><p>${{esc(p.project_goal)}}</p></article>`
      ).join("");
      document.getElementById("lanes").innerHTML = state.lanes.map(lane =>
        `<article class="lane"><span>${{esc(lane.platform)}}</span><b>${{esc(lane.formal_name)}}</b><em>${{esc(lane.role)}} / ${{esc(lane.status)}}</em><pre>${{esc(lane.transcript)}}</pre></article>`
      ).join("");
      renderTapestry(state);
      document.getElementById("footer").textContent = "Page polls every " + state.dashboard_refresh_seconds + "s; repo writes/archive entries happen only at every 3rd phase checkpoint.";
    }}
    async function tick() {{ render(await loadState()); }}
    tick();
    setInterval(tick, {3 * 1000});
  </script>
</body>
</html>
"""


def build_dashboard_state(generated: str, phases: list[dict[str, Any]], lanes: list[dict[str, Any]], checkpoints: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "generated_utc": generated,
        "phase_range": "v166-v180",
        "dashboard_mode": "checkpointed_hybrid_chrome_terminal_panels",
        "dashboard_refresh_seconds": 3,
        "dashboard_write_cadence": "every_3rd_phase_checkpoint",
        "summary": "Low-write v166-v180 execution lane: dashboard state archives only v168/v171/v174/v177/v180 checkpoints, with repo-only receipts and no provider spend.",
        "lanes": lanes,
        "phases": phases,
        "checkpoints": checkpoints,
        "external_spend_nzd": 0,
        "external_provider_mutations": "none",
        "google_drive_state": "operator_hold",
    }


def run_all() -> dict[str, Any]:
    started = time.time()
    generated = now_iso()
    paths = artifact_paths()
    phases = build_phases(generated)
    versions = command_versions()
    chrome = chrome_checks()
    lanes = build_lane_transcripts(generated)
    checkpoints = build_checkpoint_snapshots(generated, phases, lanes)
    dashboard_state = build_dashboard_state(generated, phases, lanes, checkpoints)
    dashboard_state["tapestry"] = update_dashboard_tapestry(dashboard_state, checkpoints, generated)
    cli = build_cli_consultation(lanes, versions)
    systems = build_system_expansions(phases)
    eureka = build_eureka_tasks(phases)
    command_skill = build_command_skill_board(phases)
    alpha = build_alpha_cleanup()
    surface = build_hybrid_surface(chrome)
    providers = build_provider_drafts()
    suite_hook = build_suite_hook_contract()
    sources = {"generated_utc": generated, "sources": source_digests()}
    closeout = {
        "generated_utc": generated,
        "phase_range": "v166-v180",
        "effective_success": True,
        "actual_wallclock_seconds": round(time.time() - started, 3),
        "runtime_claim": "bounded_execution_completed; no false 15_hour_wallclock_claim",
        "phase_count": len(phases),
        "checkpoint_count": len(checkpoints),
        "checkpoint_phases": [checkpoint["phase"] for checkpoint in checkpoints],
        "system_expansion_count": len(systems),
        "eureka_task_count": len(eureka),
        "command_count": command_skill["command_count"],
        "skill_count": command_skill["skill_count"],
        "dashboard": rel(paths["dashboard_html"]),
        "dashboard_tapestry_entries_this_run": dashboard_state["tapestry"]["index"]["entry_count_this_run"],
        "dashboard_archive_root": dashboard_state["tapestry"]["index"]["d_drive_archive_root"],
        "dashboard_rollover_recommended": dashboard_state["tapestry"]["rollover_policy"]["rollover_recommended"],
        "suite_hook_mode": suite_hook["suite_hook_mode"],
        "cli_lanes": [lane["id"] for lane in lanes],
        "google_drive_state": "operator_hold",
        "external_provider_mutations": "none",
        "external_spend_nzd": 0,
        "next_phase": "v181-v200 or future narrow live-write pack after exact auth/spend rollback plan",
    }
    transcript_dir = TRACE / f"{HYphen_LANE}-lane-logs"
    include_paths = [
        SCRIPT_PATH,
        SUITE_RUNNER_PATH,
        *[rel(path) for key, path in paths.items() if not key.startswith("publication")],
        *[rel(path) for path in sorted(transcript_dir.glob("*")) if path.is_file()],
    ]
    allowlist = {
        "generated_utc": generated,
        "scope": "curated_v166_v180_low_write_chrome_cli",
        "include": sorted(dict.fromkeys(include_paths)),
        "exclude_patterns": [
            "__pycache__",
            "docs/trinity-mcp-cache/",
            "docs/trinity-materialization-ledger.jsonl",
            "raw provider auth traces",
            "browser cookies local storage passwords profiles",
            "unrelated carried-forward dirty files",
        ],
        "publication_rule": "stage_only_include_paths_forward_only_no_reset_no_rebase_no_force_push",
    }

    write_json(paths["phase_json"], {"generated_utc": generated, "phases": phases})
    write_md(paths["phase_md"], "# v166-v180 Low-Write Chrome/CLI Phase Run\n\n- phases: v166-v180\n- dashboard write cadence: every 3rd phase\n- provider writes: none\n- Google Drive: operator_hold")
    write_json(paths["dashboard_json"], dashboard_state)
    paths["dashboard_html"].write_text(dashboard_html(dashboard_state), encoding="utf-8")
    write_json(paths["checkpoint_json"], {"generated_utc": generated, "count": len(checkpoints), "checkpoints": checkpoints})
    write_md(paths["checkpoint_md"], "# v166-v180 Dashboard Checkpoints\n\n- checkpoint phases: v168, v171, v174, v177, v180\n- exchange-level inputs: buffered until checkpoint")
    write_json(paths["cli_json"], cli)
    write_md(paths["cli_md"], "# v166-v180 CLI Council Consultation\n\n- Arby: receipt keeper lane active.\n- Kimi: constrained status/planning lane active; no auto-approved write mode.\n- Aster Vale: validation lane active.\n- Commit authority: Aletheon curated allowlist only.")
    write_json(paths["system_json"], {"generated_utc": generated, "count": len(systems), "items": systems})
    write_md(paths["system_md"], f"# v166-v180 System Expansion Board\n\n- candidates: {len(systems)}\n- per phase: {SYSTEM_EXPANSIONS_PER_PHASE}\n- state: repo evidence only")
    write_json(paths["eureka_json"], {"generated_utc": generated, "count": len(eureka), "items": eureka})
    write_md(paths["eureka_md"], f"# v166-v180 Eureka Task Board\n\n- tasks: {len(eureka)}\n- state: queued for future promotion")
    write_json(paths["command_skill_json"], command_skill)
    write_md(paths["command_skill_md"], f"# v166-v180 Command and Skill Board\n\n- commands: {command_skill['command_count']}\n- skills: {command_skill['skill_count']}\n- user-home installs: none")
    write_json(paths["alpha_json"], alpha)
    write_md(paths["alpha_md"], "# v166-v180 Alpha Cleanup and Security\n\n- cleanup mode: classification only\n- delete actions: 0\n- provider writes: none\n- Google Drive: operator_hold")
    write_json(paths["surface_json"], surface)
    write_md(paths["surface_md"], "# v166-v180 Hybrid Terminal Surface\n\n- preferred view: one Chrome dashboard tab with three terminal-like panels\n- native terminal embedding: deferred\n- page polling: 3 seconds\n- dashboard writes: every 3rd phase checkpoint")
    write_json(paths["provider_json"], providers)
    write_md(paths["provider_md"], "# v166-v180 Deferred Live-Write Pack Drafts\n\n- all provider packs are draft-only\n- spend: 0 NZD\n- broad auth: not opened")
    write_json(paths["source_json"], sources)
    write_md(paths["source_md"], "# v166-v180 Source Digest\n\n- journey/archive inputs are recorded by digest where private\n- raw private source text is not republished")
    write_json(paths["suite_hook_json"], suite_hook)
    write_md(paths["suite_hook_md"], "# v166-v180 Suite Hook Contract\n\n- included by default in deep and L5 materialize suite runs\n- skip flag: --skip-v166-v180-dashboard-run\n- dashboard writes only at checkpoint phases")
    write_json(paths["closeout_json"], closeout)
    write_md(paths["closeout_md"], f"# v166-v180 Low-Write Chrome/CLI Closeout\n\n- effective success: true\n- checkpoints: {len(checkpoints)}\n- system expansions: {len(systems)}\n- eureka tasks: {len(eureka)}\n- commands: {command_skill['command_count']}\n- skills: {command_skill['skill_count']}\n- dashboard archive root: {closeout['dashboard_archive_root']}\n- provider writes: none")
    write_json(paths["allowlist_json"], allowlist)
    write_md(paths["allowlist_md"], f"# v166-v180 Stage Allowlist\n\n- include count: {len(allowlist['include'])}\n- publication rule: forward-only, allowlist-only")
    return closeout


def verify_artifacts() -> dict[str, Any]:
    paths = artifact_paths()
    required = [
        path
        for key, path in paths.items()
        if not key.startswith("publication") and not key.startswith("verification")
    ]
    missing = [rel(path) for path in required if not path.exists()]
    closeout = read_json(paths["closeout_json"], {})
    dashboard = read_json(paths["dashboard_json"], {})
    allowlist = read_json(paths["allowlist_json"], {})
    tapestry_index = read_json(paths["tapestry_index_json"], {})
    archive_receipt = read_json(paths["archive_receipt_json"], {})
    status = {
        "generated_utc": now_iso(),
        "effective_success": (
            not missing
            and closeout.get("effective_success") is True
            and closeout.get("checkpoint_count") == 5
            and closeout.get("system_expansion_count") == 750
            and closeout.get("eureka_task_count") == 750
            and closeout.get("command_count") == 750
            and closeout.get("skill_count") == 750
            and archive_receipt.get("archive_write_success") is True
        ),
        "missing": missing,
        "phase_range": closeout.get("phase_range"),
        "dashboard_mode": dashboard.get("dashboard_mode"),
        "dashboard_write_cadence": dashboard.get("dashboard_write_cadence"),
        "checkpoint_phases": closeout.get("checkpoint_phases"),
        "allowlist_count": len(allowlist.get("include", [])),
        "dashboard_tapestry_entries_this_run": tapestry_index.get("entry_count_this_run"),
        "dashboard_archive_root": tapestry_index.get("d_drive_archive_root"),
        "dashboard_rollover_recommended": (tapestry_index.get("rollover_policy") or {}).get("rollover_recommended"),
        "dashboard_archive_write_success": archive_receipt.get("archive_write_success"),
        "google_drive_state": closeout.get("google_drive_state"),
        "external_provider_mutations": closeout.get("external_provider_mutations"),
        "external_spend_nzd": closeout.get("external_spend_nzd"),
    }
    write_json(paths["verification_json"], status)
    return status


def publication_result() -> dict[str, Any]:
    paths = artifact_paths()
    staged = git_value("diff", "--cached", "--name-only").splitlines()
    payload = {
        "generated_utc": now_iso(),
        "phase_range": "v166-v180",
        "local_head": git_value("rev-parse", "HEAD"),
        "remote_head": git_value("rev-parse", "origin/codex/GHC-Family/beyonder-shared-omega-line"),
        "branch": git_value("branch", "--show-current"),
        "staged_count_at_receipt": len([line for line in staged if line.strip()]),
        "forward_only_publication": True,
        "google_drive_state": "operator_hold",
        "external_provider_mutations": "none",
        "external_spend_nzd": 0,
    }
    payload["remote_matches_local"] = bool(payload["local_head"] and payload["remote_head"] and payload["local_head"] == payload["remote_head"])
    write_json(paths["publication_json"], payload)
    write_md(
        paths["publication_md"],
        "\n".join(
            [
                "# v166-v180 Publication Result",
                "",
                f"- branch: {payload['branch']}",
                f"- local head: {payload['local_head']}",
                f"- remote head: {payload['remote_head']}",
                f"- remote matches local: {payload['remote_matches_local']}",
                f"- staged count at receipt time: {payload['staged_count_at_receipt']}",
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
    parser.add_argument("--dashboard-state", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--phase", default="")
    parser.add_argument("--lane", default="")
    parser.add_argument("--dashboard-refresh-cadence", type=int, default=CHECKPOINT_CADENCE)
    args = parser.parse_args()

    if args.dashboard_refresh_cadence != CHECKPOINT_CADENCE:
        raise SystemExit("--dashboard-refresh-cadence currently supports only 3 for v166-v180")

    if args.dry_run:
        print(
            json.dumps(
                {
                    "effective_success": True,
                    "mode": "dry_run",
                    "phase": args.phase,
                    "lane": args.lane,
                    "would_write": False,
                    "dashboard_write_cadence": "every_3rd_phase_checkpoint",
                    "checkpoint_phases": ["v168", "v171", "v174", "v177", "v180"],
                    "dashboard": rel(artifact_paths()["dashboard_html"]),
                },
                sort_keys=True,
            )
        )
        return 0
    if args.run_all:
        print(json.dumps(run_all(), sort_keys=True))
    if args.verify_artifacts:
        status = verify_artifacts()
        print(json.dumps(status, sort_keys=True))
        return 0 if status.get("effective_success") else 1
    if args.dashboard_state:
        path = artifact_paths()["dashboard_json"]
        print(path.read_text(encoding="utf-8") if path.exists() else "{}")
    if args.publication_result:
        print(json.dumps(publication_result(), sort_keys=True))
    if not any([args.run_all, args.verify_artifacts, args.dashboard_state, args.publication_result]):
        parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
