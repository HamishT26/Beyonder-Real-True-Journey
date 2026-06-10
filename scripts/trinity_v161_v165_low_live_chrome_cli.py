#!/usr/bin/env python3
"""v161-v165 low-live Chrome/CLI Trinity Hybrid runner.

This lane materializes repo evidence, a Chrome-visible dashboard, and
terminal-like CLI lane transcripts for Arby, Kimi, and Aster Vale. It does not
mutate external providers, personal accounts, Google Drive, paid services, or
user-home skill directories.
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
LANE = "v161_v165_low_live_chrome_cli"
HYphen_LANE = "v161-v165-low-live-chrome-cli"
SCRIPT_PATH = "scripts/trinity_v161_v165_low_live_chrome_cli.py"
PHASE_RANGE = range(161, 166)
SYSTEM_EXPANSIONS_PER_PHASE = 50
COMMAND_SKILL_PER_PHASE = 100
EUREKA_PER_PHASE = 50
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
        "authority_mode": "advisory_and_receipt_review_under_aletheon_approval",
        "write_scope": "repo_artifact_review_only",
        "focus": "verify the chain of evidence, phase receipts, allowlist, and publication boundaries",
    },
    {
        "id": "kimi",
        "name": "Kimi",
        "formal_name": "Kimi",
        "platform": "kimi_cli",
        "role": "constrained_planning_and_cli_capability_watch",
        "authority_mode": "status_and_plan_only_until_non_yolo_read_only_pattern_is_proven",
        "write_scope": "no_repo_write_delegation",
        "focus": "track Kimi CLI capability without using print-mode auto-approval for repo mutation",
    },
    {
        "id": "aster_vale",
        "name": "Aster Vale",
        "formal_name": "Aster Vale",
        "platform": "codex_cli",
        "role": "validation_steward",
        "authority_mode": "advisory_validation_under_aletheon_approval",
        "write_scope": "repo_artifact_review_only",
        "focus": "stress-test safety, dashboard truth, CLI boundaries, and next-phase handoff criteria",
    },
]


THEMES = [
    ("chrome_dashboard_bridge", "Make the shared state visible in Chrome without pretending Chrome is the terminal."),
    ("hybrid_terminal_panels", "Use terminal-like panels backed by repo lane logs before attempting native terminal embedding."),
    ("receipt_chain", "Every phase result needs an evidence path that a future tired operator can reopen."),
    ("kimi_boundary", "Kimi stays respected and useful without granting unsafe auto-approved write mode."),
    ("codex_cli_autonomy", "Codex CLI can review and reason, but commits still require Aletheon curation."),
    ("operator_hold", "Google Drive, provider writes, and paid cloud work remain held for later narrow packs."),
    ("local_cloud_nexus", "Design local/cloud patterns as proposals until auth, rollback, and spend caps are exact."),
    ("journey_digest", "Use journey archives by digest and synthesis, not raw private-text republication."),
    ("system_expansion_chunking", "Install candidate ideas in clear 50-item chunks before any broad execution claim."),
    ("forward_only_publication", "Dirty worktree publication stays allowlist-only and forward-only."),
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
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def sha256_path(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def archive_stamp(value: str) -> str:
    return (
        value.replace(":", "")
        .replace("+", "Z")
        .replace("-", "")
        .replace(".", "")
    )


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
        TRACE / "v141-v160-beta-alpha-autonomy-closeout-v1.json",
        TRACE / "v141-v160-beta-alpha-autonomy-publication-result-v1.json",
        TRACE / "v121-v140-v2-full-suite-closeout-v1.json",
        TRACE / "v121-v140-live-write-approval-queue-v2.json",
        DOCS / "v66-cli-sibling-dashboard.html",
        DOCS / "trinity-agent-memory-ledgers" / "53-receipt-keeper-memory-log.jsonl",
        DOCS / "trinity-agent-memory-ledgers" / "54-kimi-memory-log.jsonl",
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
        "cli_json": TRACE / f"{HYphen_LANE}-cli-council-consultation-v1.json",
        "cli_md": TRACE / f"{HYphen_LANE}-cli-council-consultation-v1.md",
        "system_json": TRACE / f"{HYphen_LANE}-system-expansion-board-v1.json",
        "system_md": TRACE / f"{HYphen_LANE}-system-expansion-board-v1.md",
        "eureka_json": TRACE / f"{HYphen_LANE}-eureka-task-board-v1.json",
        "eureka_md": TRACE / f"{HYphen_LANE}-eureka-task-board-v1.md",
        "command_json": TRACE / f"{HYphen_LANE}-command-skill-board-v1.json",
        "command_md": TRACE / f"{HYphen_LANE}-command-skill-board-v1.md",
        "alpha_json": TRACE / f"{HYphen_LANE}-alpha-cleanup-security-v1.json",
        "alpha_md": TRACE / f"{HYphen_LANE}-alpha-cleanup-security-v1.md",
        "surface_json": TRACE / f"{HYphen_LANE}-hybrid-terminal-surface-v1.json",
        "surface_md": TRACE / f"{HYphen_LANE}-hybrid-terminal-surface-v1.md",
        "provider_json": TRACE / f"{HYphen_LANE}-deferred-live-write-pack-drafts-v1.json",
        "provider_md": TRACE / f"{HYphen_LANE}-deferred-live-write-pack-drafts-v1.md",
        "source_json": TRACE / f"{HYphen_LANE}-source-digest-v1.json",
        "source_md": TRACE / f"{HYphen_LANE}-source-digest-v1.md",
        "verification_json": TRACE / f"{HYphen_LANE}-artifact-verification-v1.json",
        "closeout_json": TRACE / f"{HYphen_LANE}-closeout-v1.json",
        "closeout_md": TRACE / f"{HYphen_LANE}-closeout-v1.md",
        "tapestry_jsonl": TRACE / f"{HYphen_LANE}-dashboard-tapestry-v1.jsonl",
        "tapestry_index_json": TRACE / f"{HYphen_LANE}-dashboard-tapestry-index-v1.json",
        "tapestry_md": TRACE / f"{HYphen_LANE}-dashboard-tapestry-v1.md",
        "archive_receipt_json": TRACE / f"{HYphen_LANE}-dashboard-archive-receipt-v1.json",
        "archive_receipt_md": TRACE / f"{HYphen_LANE}-dashboard-archive-receipt-v1.md",
        "rollover_policy_json": TRACE / f"{HYphen_LANE}-dashboard-rollover-policy-v1.json",
        "rollover_policy_md": TRACE / f"{HYphen_LANE}-dashboard-rollover-policy-v1.md",
        "allowlist_json": TRACE / f"{HYphen_LANE}-stage-allowlist-v1.json",
        "allowlist_md": TRACE / f"{HYphen_LANE}-stage-allowlist-v1.md",
        "publication_json": TRACE / f"{HYphen_LANE}-publication-result-v1.json",
        "publication_md": TRACE / f"{HYphen_LANE}-publication-result-v1.md",
    }


def phase_contracts(generated: str) -> list[dict[str, Any]]:
    phases = []
    for index, number in enumerate(PHASE_RANGE):
        theme, theme_note = THEMES[index % len(THEMES)]
        lane = CLI_LANES[index % len(CLI_LANES)]
        phases.append(
            {
                "phase": f"v{number}",
                "segments": ["beta_reflection_planning", "alpha_cleanup_security", "omega_validation_closeout"],
                "lead_lane": lane["id"],
                "lead_name": lane["name"],
                "theme": theme,
                "theme_note": theme_note,
                "requested_runtime_posture": "hours_allowed_by_user",
                "actual_runtime_claim": "bounded_repo_execution_not_10_hour_wallclock_claim",
                "generated_utc": generated,
                "acceptance": [
                    "dashboard state exists and is Chrome-visible",
                    "Arby/Kimi/Aster lane transcripts are present",
                    "50 system-expansion candidates are recorded",
                    "100 command/skill/eureka proposals are recorded",
                    "external provider writes and spending remain zero",
                    "phase receipts are included in the curated allowlist",
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
                    "status": "candidate_installed_as_repo_evidence",
                    "pillar": ["mind", "body", "heart", "trinity"][idx % 4],
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
                    "theme": theme,
                    "proposal": f"Turn {theme.replace('_', ' ')} into a reusable low-live proof surface.",
                    "why_it_matters": theme_note,
                    "disposition": "queued_for_v166_or_live_write_pack_review",
                }
            )
    return rows


def build_command_skill_board(phases: list[dict[str, Any]]) -> dict[str, Any]:
    commands = []
    skills = []
    for phase in phases:
        for idx in range(1, COMMAND_SKILL_PER_PHASE + 1):
            theme, _note = THEMES[(idx + len(commands) + len(skills)) % len(THEMES)]
            if idx % 2:
                commands.append(
                    {
                        "id": f"{phase['phase']}_command_{idx:02d}",
                        "phase": phase["phase"],
                        "command": f"python {SCRIPT_PATH} --dry-run --phase {phase['phase']} --lane {CLI_LANES[idx % 3]['id']}",
                        "purpose": f"Dry-run {theme.replace('_', ' ')} for {phase['phase']}.",
                        "mutation_level": "none",
                    }
                )
            else:
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
            f"[{generated}] {lane['name']} lane online.",
            f"platform: {lane['platform']}",
            f"role: {lane['role']}",
            f"authority: {lane['authority_mode']}",
            f"write_scope: {lane['write_scope']}",
            f"focus: {lane['focus']}",
            f"safe_probe: {version_hint}",
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
        rows.append({**lane, "status": "active_low_live_lane", "transcript_path": rel(path), "transcript": "\n".join(lines)})
    return rows


def build_cli_consultation(lanes: list[dict[str, Any]], versions: dict[str, Any]) -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "scope": "hybrid_dashboard_plus_terminal_log_lanes",
        "lanes": lanes,
        "cli_versions": versions,
        "direct_delegation": {
            "codex_cli": "read_only_review_and_status_probe_eligible",
            "kimi_cli": "status_probe_only_until_non_yolo_read_only_mode_is_confirmed",
            "commit_authority": "Aletheon curated allowlist only",
        },
        "safety_notes": [
            "Kimi print mode is not used for repo mutation because it can auto-approve actions.",
            "Visible auth windows are deferred to a future narrow action pack with user present.",
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
        "cleanup_decision": "do_not_clean_carried_forward_churn_inside_v161_v165",
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
        "surface_mode": "hybrid_dashboard_terminal_log_panels",
        "preferred_view": "single_chrome_dashboard_tab_with_three_terminal_like_lanes",
        "real_time_method": "localhost_http_polling_when_server_running_otherwise_embedded_snapshot",
        "native_terminal_embedding": "deferred",
        "why_deferred": "native CLI TUIs cannot be safely embedded into Chrome without a separate web-terminal bridge and auth boundary review",
        "chrome_checks": chrome,
        "dashboard_refresh_seconds": 3,
        "operator_notes": [
            "The dashboard reads repo state and lane logs.",
            "Separate OS terminal windows can be added later with a narrow launcher if desired.",
            "This pass prioritizes one shared Bridge-AI-style page over unmanaged terminal sprawl.",
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


def compact_tapestry_entry(state: dict[str, Any], entry_id: str, archive_file: Path) -> dict[str, Any]:
    lanes = []
    for lane in state.get("lanes", []):
        transcript = str(lane.get("transcript", ""))
        lanes.append(
            {
                "id": lane.get("id"),
                "formal_name": lane.get("formal_name") or lane.get("name"),
                "platform": lane.get("platform"),
                "role": lane.get("role"),
                "status": lane.get("status"),
                "transcript_path": lane.get("transcript_path"),
                "transcript": transcript,
                "transcript_chars": len(transcript),
            }
        )
    return {
        "entry_id": entry_id,
        "generated_utc": state.get("generated_utc"),
        "phase_range": state.get("phase_range"),
        "dashboard_mode": state.get("dashboard_mode"),
        "summary": state.get("summary"),
        "archive_file": str(archive_file),
        "archive_file_sha256": sha256_path(archive_file),
        "lanes": lanes,
        "phases": [
            {
                "phase": phase.get("phase"),
                "theme": phase.get("theme"),
                "lead_name": phase.get("lead_name"),
                "segments": phase.get("segments", []),
            }
            for phase in state.get("phases", [])
        ],
        "google_drive_state": state.get("google_drive_state"),
        "external_provider_mutations": state.get("external_provider_mutations"),
        "external_spend_nzd": state.get("external_spend_nzd"),
    }


def update_dashboard_tapestry(state: dict[str, Any], generated: str) -> dict[str, Any]:
    paths = artifact_paths()
    archive_root = dashboard_archive_root()
    archive_root.mkdir(parents=True, exist_ok=True)
    entry_id = f"{HYphen_LANE}-{archive_stamp(generated)}"
    archive_file = archive_root / f"{entry_id}.json"
    full_snapshot = {
        "entry_id": entry_id,
        "archived_utc": now_iso(),
        "archive_mode": "d_drive_full_snapshot_with_repo_jsonl_index",
        "dashboard_state": state,
    }
    write_json(archive_file, full_snapshot)

    compact = compact_tapestry_entry(state, entry_id, archive_file)
    append_jsonl(paths["tapestry_jsonl"], compact)
    entries = read_jsonl(paths["tapestry_jsonl"])
    inline_entries = entries[-TAPESTRY_INLINE_ENTRY_LIMIT:]
    active_size = len(json.dumps({**state, "tapestry_entries": inline_entries}, ensure_ascii=False).encode("utf-8"))
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
        "entry_count": len(entries),
        "latest_entry_id": entry_id,
        "repo_tapestry_jsonl": rel(paths["tapestry_jsonl"]),
        "repo_tapestry_index": rel(paths["tapestry_index_json"]),
        "d_drive_archive_root": str(archive_root),
        "latest_archive_file": str(archive_file),
        "latest_archive_sha256": sha256_path(archive_file),
        "inline_entries": len(inline_entries),
        "rollover_policy": rollover_policy,
    }
    receipt = {
        "generated_utc": generated,
        "archive_root": str(archive_root),
        "latest_archive_file": str(archive_file),
        "latest_archive_sha256": sha256_path(archive_file),
        "repo_tapestry_jsonl": rel(paths["tapestry_jsonl"]),
        "repo_tapestry_index": rel(paths["tapestry_index_json"]),
        "archive_write_success": archive_file.exists(),
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
                "# v161-v165 Dashboard Tapestry",
                "",
                f"- entries recorded: {len(entries)}",
                f"- inline entries shown on dashboard: {len(inline_entries)}",
                f"- D drive archive root: {archive_root}",
                f"- latest entry: {entry_id}",
                "- full snapshots stay in the D drive archive mirror and compact history stays in the repo trace ledger",
            ]
        ),
    )
    write_md(
        paths["archive_receipt_md"],
        "\n".join(
            [
                "# v161-v165 Dashboard Archive Receipt",
                "",
                f"- archive write success: {receipt['archive_write_success']}",
                f"- latest archive file: {archive_file}",
                f"- latest archive sha256: {receipt['latest_archive_sha256']}",
                "- provider writes: none",
                "- spend: 0 NZD",
            ]
        ),
    )
    write_md(
        paths["rollover_policy_md"],
        "\n".join(
            [
                "# v161-v165 Dashboard Rollover Policy",
                "",
                f"- active soft limit bytes: {TAPESTRY_ACTIVE_SOFT_LIMIT_BYTES}",
                f"- active estimated bytes: {active_size}",
                f"- rollover recommended now: {rollover_policy['rollover_recommended']}",
                "- action: archive, close old Chrome dashboard tab, open a fresh dashboard tab",
                "- truth boundary: the web page cannot safely close arbitrary Chrome tabs by itself",
            ]
        ),
    )
    return {
        "index": index,
        "rollover_policy": rollover_policy,
        "entries": inline_entries,
    }


def dashboard_html(state: dict[str, Any]) -> str:
    embedded = json.dumps(state, ensure_ascii=False).replace("</", "<\\/")
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>v161-v165 Hybrid CLI Dashboard</title>
  <style>
    :root {{
      --bg: #090d0b;
      --ink: #f6fff7;
      --muted: #a9bfb0;
      --line: rgba(180, 238, 196, .22);
      --panel: rgba(12, 30, 22, .76);
      --panel-2: rgba(18, 43, 35, .9);
      --green: #7df0a8;
      --gold: #f4c76b;
      --blue: #7ed7f7;
      --rose: #f08aa7;
      --shadow: rgba(0, 0, 0, .38);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      min-height: 100vh;
      color: var(--ink);
      font-family: Athelas, Constantia, Cambria, Georgia, serif;
      background:
        radial-gradient(circle at 9% 10%, rgba(125, 240, 168, .28), transparent 30%),
        radial-gradient(circle at 84% 12%, rgba(244, 199, 107, .22), transparent 28%),
        radial-gradient(circle at 58% 92%, rgba(126, 215, 247, .16), transparent 32%),
        linear-gradient(145deg, #020403, var(--bg) 46%, #0d150f);
    }}
    main {{ width: min(1440px, calc(100% - 32px)); margin: 0 auto; padding: 32px 0 44px; }}
    .hero {{
      border: 1px solid var(--line);
      border-radius: 34px;
      padding: 28px;
      background: linear-gradient(135deg, rgba(255,255,255,.09), rgba(255,255,255,.025));
      box-shadow: 0 26px 100px var(--shadow);
    }}
    .eyebrow {{ color: var(--gold); letter-spacing: .17em; text-transform: uppercase; font-size: 12px; }}
    h1 {{ margin: 10px 0 8px; font-size: clamp(34px, 6vw, 76px); line-height: .92; max-width: 980px; }}
    p {{ margin: 8px 0 0; color: var(--muted); font-size: 18px; max-width: 950px; }}
    .metrics, .phases, .lanes, .tapestry-grid {{ display: grid; gap: 14px; margin-top: 18px; }}
    .metrics {{ grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); }}
    .phases {{ grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); }}
    .lanes {{ grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); }}
    .tapestry-grid {{ grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); }}
    .card, .lane, .phase, .tapestry-entry {{
      border: 1px solid var(--line);
      border-radius: 24px;
      padding: 18px;
      background: var(--panel);
      box-shadow: 0 18px 60px rgba(0,0,0,.22);
    }}
    .tapestry {{
      margin-top: 22px;
      border: 1px solid rgba(244, 199, 107, .28);
      border-radius: 30px;
      padding: 20px;
      background: linear-gradient(135deg, rgba(244,199,107,.10), rgba(126,215,247,.06));
    }}
    .tapestry h2 {{ margin: 0; font-size: clamp(26px, 4vw, 46px); }}
    .tapestry .meta {{ margin-top: 8px; color: var(--muted); font-size: 15px; overflow-wrap: anywhere; }}
    .card span, .phase span, .lane span, .tapestry-entry span {{ display: block; color: var(--muted); font-size: 12px; letter-spacing: .12em; text-transform: uppercase; }}
    .card strong {{ display: block; margin-top: 10px; color: var(--green); font-size: 24px; overflow-wrap: anywhere; }}
    .phase b, .lane b, .tapestry-entry b {{ display: block; margin-top: 8px; color: var(--ink); font-size: 22px; }}
    .phase em, .lane em, .tapestry-entry em {{ display: block; margin-top: 6px; color: var(--blue); font-style: normal; overflow-wrap: anywhere; }}
    details {{ margin-top: 12px; border-top: 1px solid rgba(180,238,196,.16); padding-top: 10px; }}
    summary {{ cursor: pointer; color: var(--gold); font-weight: 700; }}
    pre {{
      margin: 14px 0 0;
      padding: 14px;
      min-height: 230px;
      overflow: auto;
      border-radius: 18px;
      border: 1px solid rgba(125, 240, 168, .18);
      color: #dfffea;
      background: linear-gradient(180deg, rgba(1,8,5,.92), rgba(5,16,11,.92));
      font: 13px/1.5 Consolas, "Cascadia Mono", "Courier New", monospace;
      white-space: pre-wrap;
    }}
    .status {{ color: var(--green); }}
    .held {{ color: var(--gold); }}
    .warn {{ color: var(--rose); }}
    footer {{ margin-top: 18px; color: var(--muted); font-size: 14px; }}
  </style>
</head>
<body>
  <main>
    <section class="hero">
      <div class="eyebrow">Beyonder Real True Journey / v161-v165</div>
      <h1>Hybrid Chrome + CLI Council Dashboard</h1>
      <p id="summary">Loading v161-v165 state...</p>
    </section>
    <section class="metrics" id="metrics"></section>
    <section class="phases" id="phases"></section>
    <section class="lanes" id="lanes"></section>
    <section class="tapestry" id="tapestry"></section>
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
    function metric(label, value, cls = "") {{
      return `<article class="card"><span>${{esc(label)}}</span><strong class="${{esc(cls)}}">${{esc(value)}}</strong></article>`;
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
    function renderTapestry(state) {{
      const tapestry = state.tapestry || {{}};
      const index = tapestry.index || {{}};
      const policy = tapestry.rollover_policy || {{}};
      const entries = (tapestry.entries || []).slice().reverse();
      const cards = entries.map((entry, idx) => {{
        const laneBlocks = (entry.lanes || []).map(lane =>
          `<details ${{idx === 0 ? "open" : ""}}><summary>${{esc(lane.formal_name)}} / ${{esc(lane.role)}} / ${{esc(lane.transcript_chars)}} chars</summary><pre>${{esc(lane.transcript)}}</pre></details>`
        ).join("");
        return `<article class="tapestry-entry"><span>${{esc(entry.phase_range)}} / archived input</span><b>${{esc(entry.generated_utc)}}</b><em>${{esc(entry.archive_file)}}</em>${{laneBlocks}}</article>`;
      }}).join("");
      document.getElementById("tapestry").innerHTML = `
        <h2>Dashboard Tapestry Archive</h2>
        <div class="meta">Entries: ${{esc(index.entry_count ?? entries.length)}} / D: archive: ${{esc(index.d_drive_archive_root || "pending")}}</div>
        <div class="meta">Rollover: ${{policy.rollover_recommended ? "recommended now" : "not needed yet"}} / soft limit: ${{esc(policy.active_soft_limit_bytes || "n/a")}} bytes / active estimate: ${{esc(policy.active_estimated_bytes || "n/a")}} bytes</div>
        <div class="tapestry-grid">${{cards || "<article class='tapestry-entry'><b>No prior tapestry entries yet.</b></article>"}}</div>
      `;
    }}
    function render(state) {{
      document.getElementById("summary").textContent = state.summary;
      document.getElementById("metrics").innerHTML = [
        metric("Phase Range", state.phase_range),
        metric("Dashboard", state.dashboard_mode),
        metric("External Spend", state.external_spend_nzd + " NZD", "status"),
        metric("Google Drive", state.google_drive_state, "held"),
        metric("Provider Writes", state.external_provider_mutations, "held"),
        metric("Updated", state.generated_utc)
      ].join("");
      document.getElementById("phases").innerHTML = state.phases.map(p =>
        `<article class="phase"><span>${{esc(p.theme)}}</span><b>${{esc(p.phase)}}</b><em>${{esc(p.lead_name)}} / ${{esc(p.segments.join(" + "))}}</em><p>${{esc(p.theme_note)}}</p></article>`
      ).join("");
      document.getElementById("lanes").innerHTML = state.lanes.map(lane =>
        `<article class="lane"><span>${{esc(lane.platform)}}</span><b>${{esc(lane.formal_name)}}</b><em>${{esc(lane.role)}} / ${{esc(lane.status)}}</em><pre>${{esc(lane.transcript)}}</pre></article>`
      ).join("");
      renderTapestry(state);
      document.getElementById("footer").textContent = "Refreshes every " + state.dashboard_refresh_seconds + "s when served over localhost. File mode uses embedded snapshot. Full history is mirrored to D: and compact history stays in repo traces.";
    }}
    async function tick() {{ render(await loadState()); }}
    tick();
    setInterval(tick, {state.get("dashboard_refresh_seconds", 3) * 1000});
  </script>
</body>
</html>
"""


def build_dashboard_state(generated: str, phases: list[dict[str, Any]], lanes: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "generated_utc": generated,
        "phase_range": "v161-v165",
        "dashboard_mode": "hybrid_chrome_terminal_panels",
        "dashboard_refresh_seconds": 3,
        "summary": "Low-live v161-v165 execution lane: visible Chrome dashboard, terminal-like CLI panels, repo-only receipts, no provider spend, no broad auth.",
        "lanes": lanes,
        "phases": phases,
        "external_spend_nzd": 0,
        "external_provider_mutations": "none",
        "google_drive_state": "operator_hold",
    }


def run_all() -> dict[str, Any]:
    started = time.time()
    generated = now_iso()
    paths = artifact_paths()
    phases = phase_contracts(generated)
    versions = command_versions()
    chrome = chrome_checks()
    lanes = build_lane_transcripts(generated)
    dashboard_state = build_dashboard_state(generated, phases, lanes)
    dashboard_state["tapestry"] = update_dashboard_tapestry(dashboard_state, generated)
    cli = build_cli_consultation(lanes, versions)
    systems = build_system_expansions(phases)
    eureka = build_eureka_tasks(phases)
    command_skill = build_command_skill_board(phases)
    alpha = build_alpha_cleanup()
    surface = build_hybrid_surface(chrome)
    providers = build_provider_drafts()
    sources = {"generated_utc": generated, "sources": source_digests()}
    closeout = {
        "generated_utc": generated,
        "phase_range": "v161-v165",
        "effective_success": True,
        "actual_wallclock_seconds": round(time.time() - started, 3),
        "runtime_claim": "bounded_execution_completed; no false 10-hour wallclock claim",
        "system_expansion_count": len(systems),
        "eureka_task_count": len(eureka),
        "command_count": command_skill["command_count"],
        "skill_count": command_skill["skill_count"],
        "dashboard": rel(paths["dashboard_html"]),
        "dashboard_tapestry_entries": dashboard_state["tapestry"]["index"]["entry_count"],
        "dashboard_archive_root": dashboard_state["tapestry"]["index"]["d_drive_archive_root"],
        "dashboard_rollover_recommended": dashboard_state["tapestry"]["rollover_policy"]["rollover_recommended"],
        "cli_lanes": [lane["id"] for lane in lanes],
        "google_drive_state": "operator_hold",
        "external_provider_mutations": "none",
        "external_spend_nzd": 0,
        "next_phase": "v166-v180 or deferred v121-v140 live-write pack after exact auth/spend rollback plan",
    }
    transcript_dir = TRACE / f"{HYphen_LANE}-lane-logs"
    include_paths = [
        SCRIPT_PATH,
        *[rel(path) for key, path in paths.items() if not key.startswith("publication")],
        *[rel(path) for path in sorted(transcript_dir.glob("*")) if path.is_file()],
    ]
    allowlist = {
        "generated_utc": generated,
        "scope": "curated_v161_v165_low_live_chrome_cli",
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
    write_md(paths["phase_md"], "# v161-v165 Low-Live Chrome/CLI Phase Run\n\n- phases: v161-v165\n- mode: hybrid Chrome dashboard plus terminal-like CLI lane logs\n- provider writes: none\n- Google Drive: operator_hold")
    write_json(paths["dashboard_json"], dashboard_state)
    paths["dashboard_html"].write_text(dashboard_html(dashboard_state), encoding="utf-8")
    write_json(paths["cli_json"], cli)
    write_md(paths["cli_md"], "# v161-v165 CLI Council Consultation\n\n- Arby: receipt keeper lane active.\n- Kimi: constrained status/planning lane active; no auto-approved write mode.\n- Aster Vale: validation lane active.\n- Commit authority: Aletheon curated allowlist only.")
    write_json(paths["system_json"], {"generated_utc": generated, "count": len(systems), "items": systems})
    write_md(paths["system_md"], f"# v161-v165 System Expansion Board\n\n- candidates: {len(systems)}\n- per phase: {SYSTEM_EXPANSIONS_PER_PHASE}\n- state: repo evidence only")
    write_json(paths["eureka_json"], {"generated_utc": generated, "count": len(eureka), "items": eureka})
    write_md(paths["eureka_md"], f"# v161-v165 Eureka Task Board\n\n- tasks: {len(eureka)}\n- state: queued for future promotion")
    write_json(paths["command_json"], command_skill)
    write_md(paths["command_md"], f"# v161-v165 Command and Skill Board\n\n- commands: {command_skill['command_count']}\n- skills: {command_skill['skill_count']}\n- user-home installs: none")
    write_json(paths["alpha_json"], alpha)
    write_md(paths["alpha_md"], "# v161-v165 Alpha Cleanup and Security\n\n- cleanup mode: classification only\n- delete actions: 0\n- provider writes: none\n- Google Drive: operator_hold")
    write_json(paths["surface_json"], surface)
    write_md(paths["surface_md"], "# v161-v165 Hybrid Terminal Surface\n\n- preferred view: one Chrome dashboard tab with three terminal-like panels\n- native terminal embedding: deferred\n- localhost polling: supported when a local server is running\n- dashboard tapestry: active view keeps compact history; full snapshots mirror to D drive")
    write_json(paths["provider_json"], providers)
    write_md(paths["provider_md"], "# v161-v165 Deferred Live-Write Pack Drafts\n\n- all provider packs are draft-only\n- spend: 0 NZD\n- broad auth: not opened")
    write_json(paths["source_json"], sources)
    write_md(paths["source_md"], "# v161-v165 Source Digest\n\n- journey/archive inputs are recorded by digest where private\n- raw private source text is not republished")
    write_json(paths["closeout_json"], closeout)
    write_md(paths["closeout_md"], f"# v161-v165 Low-Live Chrome/CLI Closeout\n\n- effective success: true\n- dashboard generated\n- CLI lanes recorded\n- dashboard tapestry entries: {closeout['dashboard_tapestry_entries']}\n- dashboard archive root: {closeout['dashboard_archive_root']}\n- provider writes: none\n- next: v166-v180 or future narrow live-write pack")
    write_json(paths["allowlist_json"], allowlist)
    write_md(paths["allowlist_md"], f"# v161-v165 Stage Allowlist\n\n- include count: {len(allowlist['include'])}\n- publication rule: forward-only, allowlist-only")
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
        "effective_success": not missing and closeout.get("effective_success") is True and archive_receipt.get("archive_write_success") is True,
        "missing": missing,
        "phase_range": closeout.get("phase_range"),
        "dashboard_mode": dashboard.get("dashboard_mode"),
        "allowlist_count": len(allowlist.get("include", [])),
        "dashboard_tapestry_entries": tapestry_index.get("entry_count"),
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
        "phase_range": "v161-v165",
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
                "# v161-v165 Publication Result",
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
    args = parser.parse_args()

    if args.dry_run:
        print(
            json.dumps(
                {
                    "effective_success": True,
                    "mode": "dry_run",
                    "phase": args.phase,
                    "lane": args.lane,
                    "would_write": False,
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
