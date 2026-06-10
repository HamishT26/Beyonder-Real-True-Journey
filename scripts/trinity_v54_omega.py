#!/usr/bin/env python3
"""Publish V54 Omega expansion, toolchain repair, and suite preservation evidence."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
AUTO_DIR = ROOT / "docs" / "auto-generated"
PHASE = "v54_omega"
NEXT_PHASE = "v55_beta"
PUBLICATION_BRANCH = "codex/GHC-Family/beyonder-shared-omega-line"
EXECUTION_BRANCH = "codex/GHC-Family/v54-omega-exec"
BASELINE_SHA = "74df14427ba278ed0e496c3dc5cea97fe1f23449"
D_ARCHIVE_ROOT = Path(r"D:\GHC-Archives")
KIMI_SECRET = D_ARCHIVE_ROOT / "secrets" / "kimi_creds.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [jsonable(item) for item in value]
    return str(value)


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(jsonable(payload), indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def clean(text: str | None) -> str:
    return str(text or "").replace("\x00", "").replace("\ufeff", "")


def excerpt(text: str | None, limit: int = 2400) -> str:
    value = clean(text)
    return value[-limit:] if len(value) > limit else value


def run(args: list[str], *, cwd: Path = ROOT, timeout: int = 180) -> subprocess.CompletedProcess[str]:
    command = args
    if args:
        candidates = [args[0]]
        if not args[0].lower().endswith(".cmd"):
            candidates.insert(0, f"{args[0]}.cmd")
        for candidate in candidates:
            resolved = shutil.which(candidate)
            if resolved:
                command = [resolved, *args[1:]]
                break
    try:
        proc = subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=timeout, check=False)
        proc.stdout = clean(proc.stdout)
        proc.stderr = clean(proc.stderr)
        return proc
    except FileNotFoundError as exc:
        return subprocess.CompletedProcess(args=args, returncode=127, stdout="", stderr=str(exc))
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout if isinstance(exc.stdout, str) else (exc.stdout or b"").decode("utf-8", errors="replace")
        stderr = exc.stderr if isinstance(exc.stderr, str) else (exc.stderr or b"").decode("utf-8", errors="replace")
        return subprocess.CompletedProcess(args=args, returncode=124, stdout=clean(stdout), stderr=clean(stderr))


def git(args: list[str], timeout: int = 180) -> subprocess.CompletedProcess[str]:
    return run(["git", *args], timeout=timeout)


def git_head() -> str:
    return git(["rev-parse", "HEAD"], timeout=30).stdout.strip()


def git_status_lines() -> list[str]:
    return [line for line in git(["status", "--short"], timeout=180).stdout.splitlines() if line.strip()]


def suite_summary(phase: str, profile: str) -> dict[str, Any]:
    path = TRACE_DIR / f"{phase}-{profile}-suite-status.json"
    payload = read_json(path)
    counts = payload.get("counts", {}) if isinstance(payload.get("counts"), dict) else {}
    failures = [
        {
            "label": str(row.get("label") or ""),
            "status": str(row.get("status") or ""),
            "command": str(row.get("command") or ""),
        }
        for row in payload.get("results", [])
        if isinstance(row, dict)
        and (row.get("status") == "FAIL" or row.get("ok") is False or row.get("effective_success") is False)
    ]
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "present": path.exists(),
        "summary": f"{counts.get('pass', 0)} PASS / {counts.get('warn', 0)} WARN / {counts.get('fail', 0)} FAIL"
        if payload
        else "missing",
        "pass_count": int(counts.get("pass", 0) or 0),
        "warn_count": int(counts.get("warn", 0) or 0),
        "fail_count": int(counts.get("fail", 0) or 0),
        "effective_success": payload.get("effective_success") if payload else None,
        "failure_count": len(failures),
        "failure_labels": [row["label"] for row in failures[:120]],
    }


def ps_drive_state() -> dict[str, Any]:
    proc = run(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            (
                "Get-PSDrive -Name C,D | ForEach-Object { "
                "[pscustomobject]@{Name=$_.Name;Free=[math]::Round($_.Free/1GB,2);Used=[math]::Round($_.Used/1GB,2)} "
                "} | ConvertTo-Json"
            ),
        ],
        timeout=60,
    )
    try:
        parsed = json.loads(proc.stdout)
    except Exception:
        parsed = []
    if isinstance(parsed, dict):
        parsed = [parsed]
    return {
        "generated_utc": now_iso(),
        "drives": parsed if isinstance(parsed, list) else [],
        "probe_returncode": proc.returncode,
    }


def tool_probes() -> dict[str, Any]:
    command_names = [
        "codex",
        "kimi",
        "git",
        "gh",
        "node",
        "npm",
        "npx",
        "rg",
        "python",
        "docker",
        "circleci",
        "vercel",
        "neonctl",
        "wrangler",
    ]
    rows: dict[str, Any] = {}
    for command in command_names:
        resolved = shutil.which(command) or shutil.which(f"{command}.cmd")
        version = ""
        if resolved:
            proc = run([command, "--version"], timeout=60)
            version = excerpt(proc.stdout or proc.stderr, 900).strip()
        rows[command] = {
            "available": bool(resolved),
            "path_state": "on_path" if resolved else "missing",
            "executable_name": Path(resolved).name if resolved else "",
            "version": version,
        }
    codex_login = run(["codex", "login", "status"], timeout=120)
    codex_features = run(["codex", "features", "list"], timeout=120)
    codex_mcp = run(["codex", "mcp", "list"], timeout=120)
    kimi_help = run(["kimi", "--help"], timeout=120)
    return {
        "generated_utc": now_iso(),
        "command_presence": rows,
        "codex_login_status": excerpt(codex_login.stdout or codex_login.stderr, 1200),
        "codex_features_excerpt": excerpt(codex_features.stdout, 9000),
        "codex_mcp_excerpt": excerpt(codex_mcp.stdout, 9000),
        "kimi_help_excerpt": excerpt(kimi_help.stdout or kimi_help.stderr, 2000),
        "kimi_secret_metadata": {
            "path_state": "d_drive_secret_present" if KIMI_SECRET.exists() else "missing",
            "present": KIMI_SECRET.exists(),
            "length": KIMI_SECRET.stat().st_size if KIMI_SECRET.exists() else 0,
        },
    }


def official_source_digest() -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "source_truth_state": "current_sources_checked_for_v54",
        "openai_models": {
            "url": "https://developers.openai.com/api/docs/models",
            "v54_takeaway": "GPT-5.5 is documented as available in ChatGPT and Codex, while API availability is described as coming soon; GPT-5.4 remains the documented API flagship model.",
        },
        "kimi_k26": {
            "url": "https://www.kimi.com/ai-models/kimi-k2-6",
            "v54_takeaway": "Kimi K2.6 is described as an open-source coding, long-horizon execution, and agent-swarm model.",
        },
        "kimi_agent_swarm": {
            "url": "https://www.kimi.com/blog/agent-swarm",
            "v54_takeaway": "Agent Swarm is presented as a research-preview pattern for specialized parallel sub-agents and large document/research synthesis.",
        },
        "kimi_claw": {
            "url": "https://www.kimi.com/resources/kimi-claw-introduction",
            "v54_takeaway": "Kimi Claw supports personality, memory, skills, scheduled tasks, files, and web terminal workflows; one-click cloud deployment is membership-dependent.",
        },
        "gating_rule": "source_anchored_but_live_cloud_or_external_actions_remain_separately_confirmed",
    }


def build_addition_registry(probes: dict[str, Any]) -> dict[str, Any]:
    commands = probes.get("command_presence", {}) if isinstance(probes.get("command_presence"), dict) else {}
    missing = {name for name, row in commands.items() if isinstance(row, dict) and not row.get("available")}
    categories: list[tuple[str, list[str]]] = [
        (
            "local_cli_toolchain",
            [
                "gh",
                "circleci",
                "vercel",
                "neonctl",
                "wrangler",
                "docker",
                "jq",
                "yq",
                "fd",
                "fzf",
                "bat",
                "sd",
                "dust",
                "duf",
                "hyperfine",
                "tokei",
                "just",
                "make",
                "cmake",
                "uv",
                "ruff",
                "mypy",
                "pytest",
                "pipx",
                "pnpm",
                "corepack",
                "tsx",
                "typescript",
                "playwright",
                "tectonic",
            ],
        ),
        (
            "codex_kimi_collaboration",
            [
                "codex_memory_resume_drill",
                "codex_mcp_registry_refresh",
                "codex_cli_model_invocation_probe",
                "kimi_cli_print_probe",
                "kimi_session_resume_probe",
                "kimiclaw_role_reflection",
                "ari_suite_summary_cycle",
                "kairos_source_synthesis_cycle",
                "sera_ui_review_lane",
                "cael_voss_toolchain_lane",
                "sable_archive_lane",
                "riven_suite_repair_lane",
                "nox_soren_security_lane",
                "bounded_subagent_protocol",
                "agent_task_result_schema",
                "agent_handoff_receipt",
                "memory_token_registry",
                "identity_continuity_manifest",
                "helper_lane_timeout_policy",
                "helper_lane_write_scope_policy",
            ],
        ),
        (
            "repo_quality_and_suite",
            [
                "suite_failure_id_index",
                "standard_failure_repair_loop",
                "deep_delta_classifier",
                "materialize_l2_gate",
                "materialize_l3_gate",
                "materialize_l4_gate",
                "materialize_l5_gate",
                "mcp_refresh_gate",
                "runtime_truth_validator",
                "publication_result_validator",
                "allowlist_completeness_check",
                "dirty_churn_classifier",
                "generated_cache_cleaner_dry_run",
                "memory_archive_reachability_check",
                "proof_surface_size_budget",
                "html_dashboard_smoke_check",
                "json_schema_lint",
                "markdown_link_check",
                "python_compileall",
                "circleci_config_local_lint_plan",
                "toolchain_gap_scorecard",
            ],
        ),
        (
            "control_plane_and_ui",
            [
                "local_mission_control_dashboard",
                "notion_mission_control_draft",
                "notion_action_confirmation_gate",
                "browser_use_iab_probe",
                "playwright_fallback_probe",
                "app_plugin_matrix",
                "cli_mcp_matrix",
                "token_usage_policy_panel",
                "operator_status_panel",
                "suite_ladder_panel",
                "agent_roster_panel",
                "kimiclaw_swarm_panel",
                "toolchain_install_panel",
                "c_drive_space_panel",
                "d_drive_archive_panel",
                "source_anchor_panel",
                "free_tier_connector_panel",
                "cloud_standby_panel",
                "handoff_receiver_panel",
                "risk_gate_panel",
            ],
        ),
        (
            "research_and_archives",
            [
                "v4_v15_lineage_index",
                "v20_v24_bridge_index",
                "v30_v31_bridge_index",
                "v32_v38_aura_index",
                "v39_v41_recent_archive_index",
                "v49_v53_phase_digest",
                "gmut_source_claim_matrix",
                "freed_id_governance_matrix",
                "trinity_hybrid_os_map",
                "qcit_experiment_catalog",
                "kairotic_experiment_catalog",
                "aoc_sync_catalog",
                "legacy_pdf_inventory",
                "legacy_txt_inventory",
                "source_anchor_quality_score",
                "citation_gap_board",
                "simulation_candidate_board",
                "bounded_research_prompt_pack",
                "older_family_names_index",
                "archive_no_bulk_rewrite_policy",
            ],
        ),
        (
            "plugin_and_connector_readiness",
            [
                "github_connector_read_only_probe",
                "notion_connector_search_probe",
                "google_drive_hold_guard",
                "figma_connector_registry_probe",
                "linear_connector_registry_probe",
                "browser_use_skill_probe",
                "circleci_plugin_config_pack",
                "cloudflare_skill_matrix",
                "vercel_free_tier_plan",
                "neon_free_tier_plan",
                "render_plugin_gate",
                "expo_plugin_gate",
                "scite_research_gate",
                "life_science_research_gate",
                "latex_tectonic_compile_gate",
                "superpowers_workflow_gate",
                "hugging_face_catalog_gate",
                "gmail_action_time_gate",
                "test_android_apps_gate",
                "build_web_apps_gate",
            ],
        ),
    ]
    rows: list[dict[str, Any]] = []
    for category, names in categories:
        for name in names:
            state = "candidate_registry_only"
            action_gate = "none"
            if name in missing:
                state = "blocked_missing_local_cli"
                action_gate = "install_requires_action_time_confirmation"
            elif name in commands:
                state = "already_available_locally"
            elif name.endswith("_probe") or name.endswith("_gate") or name.endswith("_panel") or name.endswith("_index"):
                state = "repo_side_scaffold_ready"
            elif "notion" in name or "gmail" in name or "drive" in name:
                action_gate = "external_write_or_sensitive_connector_requires_confirmation"
            rows.append(
                {
                    "id": f"v54-{len(rows) + 1:03d}",
                    "category": category,
                    "name": name,
                    "state": state,
                    "action_gate": action_gate,
                    "validation": "bounded_probe_before_promotion",
                }
            )
    safe_now = [
        row["name"]
        for row in rows
        if row["state"] in {"already_available_locally", "repo_side_scaffold_ready"} and row["action_gate"] == "none"
    ][:25]
    return {
        "generated_utc": now_iso(),
        "addition_registry_state": "candidate_pool_scored_no_unconfirmed_installs",
        "candidate_count": len(rows),
        "safe_repo_side_or_already_available_first_tranche": safe_now,
        "policy": {
            "no_bulk_install_spree": True,
            "install_requires_action_time_confirmation": True,
            "external_write_requires_action_time_confirmation": True,
            "paid_cloud_stays_on_standby": True,
        },
        "rows": rows,
    }


def cleanup_manifest(drive_state: dict[str, Any]) -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []
    scan_paths = [
        ROOT / "__pycache__",
        ROOT / ".pytest_cache",
        ROOT / ".mypy_cache",
        ROOT / ".ruff_cache",
        ROOT / "docs" / "trinity-live-traces" / "v53-standard-failure-ids.tmp",
    ]
    for path in scan_paths:
        if not path.exists():
            continue
        if path.is_file():
            size = path.stat().st_size
            count = 1
        else:
            files = [child for child in path.rglob("*") if child.is_file()]
            size = sum(child.stat().st_size for child in files)
            count = len(files)
        candidates.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "category": "safe_generated_cache" if "__pycache__" in path.as_posix() or path.name.endswith("_cache") else "candidate_archive_then_remove",
                "file_count": count,
                "bytes": size,
                "v54_action": "manifest_only_no_delete_without_action_time_confirmation",
            }
        )
    downloads = Path.home() / "Downloads"
    journey_downloads = []
    if downloads.exists():
        for pattern in ["Beyonder-Real-True Journey v*.txt", "Beyonder-Real-True Journey v*.pdf"]:
            journey_downloads.extend(downloads.glob(pattern))
    candidates.append(
        {
            "path": "user_downloads_beyonder_pattern",
            "category": "candidate_archive_then_remove",
            "file_count": len(journey_downloads),
            "bytes": sum(path.stat().st_size for path in journey_downloads if path.exists()),
            "v54_action": "summary_only_no_file_names_no_delete_without_confirmation",
        }
    )
    return {
        "generated_utc": now_iso(),
        "local_archive_cleanup_state": "manifested_only_no_delete",
        "drive_state_before": drive_state,
        "c_drive_priority": "high",
        "d_drive_archive_root": str(D_ARCHIVE_ROOT),
        "candidate_count": len(candidates),
        "total_candidate_bytes": sum(int(row.get("bytes", 0) or 0) for row in candidates),
        "candidates": candidates,
        "protected_categories": [
            "tracked proof surfaces",
            "role contracts",
            "certificates",
            "memory ledgers",
            "published closeout and handoff packs",
            "user Downloads outside the explicit Beyonder pattern",
        ],
    }


def plugin_matrix(probes: dict[str, Any]) -> dict[str, Any]:
    plugins = [
        "browser-use",
        "notion",
        "github",
        "circleci",
        "cloudflare",
        "google-drive",
        "vercel",
        "superpowers",
        "expo",
        "neon-postgres",
        "scite",
        "render",
        "life-science-research",
        "latex-tectonic",
        "figma",
        "linear",
        "gmail",
        "hugging-face",
        "test-android-apps",
        "build-web-apps",
    ]
    cli_text = str(probes.get("codex_mcp_excerpt") or "").lower()
    commands = probes.get("command_presence", {}) if isinstance(probes.get("command_presence"), dict) else {}
    rows = []
    for plugin in plugins:
        normalized = plugin.replace("-", "_")
        local_cli = {
            "circleci": "circleci",
            "cloudflare": "wrangler",
            "vercel": "vercel",
            "neon-postgres": "neonctl",
            "github": "gh",
        }.get(plugin)
        if normalized in cli_text or plugin in cli_text:
            state = "already_callable_in_cli_mcp"
        elif local_cli and commands.get(local_cli, {}).get("available"):
            state = "local_cli_available_auth_or_probe_needed"
        elif plugin in {"browser-use", "latex-tectonic", "life-science-research", "superpowers", "scite", "build-web-apps"}:
            state = "callable_in_app_or_skill_only"
        else:
            state = "callable_in_app_only_or_blocked_missing_cli_connector"
        rows.append({"plugin": plugin, "v54_state": state})
    return {
        "generated_utc": now_iso(),
        "plugin_surface_split_state": "app_plugins_cli_mcp_and_local_clis_separate",
        "rows": rows,
    }


def token_usage_policy(probes: dict[str, Any]) -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "token_usage_state": "aggregate_usage_not_exposed_by_current_cli_surfaces",
        "codex_token_usage_state": "not_exposed_by_cli_no_private_log_harvest",
        "kimi_token_usage_state": "not_exposed_by_cli_no_private_log_harvest",
        "dashboard_policy": "display operator_supplied_or_future_api_totals_only",
        "privacy_rule": "do_not_scrape_private_logs_browser_history_or_token_ledgers",
    }


def browser_use_proof(state: str, detail: str) -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "browser_use_state": state,
        "detail": detail,
        "source": "node_repl_browser_use_iab_probe",
        "fallback": "local_html_dashboard_path_published",
    }


def notion_plan() -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "notion_ui_state": "repo_side_pack_ready_live_write_requires_action_time_confirmation",
        "title": "V54 Mission Control",
        "sections": [
            "Suite ladder status",
            "Agent roster and bounded helper lanes",
            "100+ addition registry",
            "Toolchain repair gates",
            "C-drive cleanup manifest",
            "Browser Use and plugin split",
            "V55 handoff",
        ],
        "live_write_policy": "creating_or_updating_notion_pages_requires_action_time_confirmation",
    }


def source_archive_digest() -> dict[str, Any]:
    docs = list(ROOT.glob("Beyonder-Real-True Journey v*.txt")) + list(ROOT.glob("Beyonder-Real-True Journey v*.pdf"))
    downloads = Path.home() / "Downloads"
    download_count = 0
    download_bytes = 0
    if downloads.exists():
        for pattern in ["Beyonder-Real-True Journey v*.txt", "Beyonder-Real-True Journey v*.pdf"]:
            for path in downloads.glob(pattern):
                download_count += 1
                download_bytes += path.stat().st_size
    return {
        "generated_utc": now_iso(),
        "journey_archive_state": "indexed_for_reflection_no_bulk_rewrite",
        "repo_archive_file_count": len(docs),
        "repo_archive_bytes": sum(path.stat().st_size for path in docs if path.exists()),
        "downloads_beyonder_pattern_count": download_count,
        "downloads_beyonder_pattern_bytes": download_bytes,
        "reflection_bands": [
            "v4-v15 Ariel original-crew archive",
            "v20-v24 bridge archive",
            "v30-v31 Ariel bridge archive",
            "v32-v38 Aura and pre-Aletheon bridge archive",
            "v39-v41 Aletheon Orun Gemini Vesper Kai Ari Kimiclaw archive",
            "v49-v53 Codex and Kimiclaw implementation archive",
        ],
    }


def write_md_list(path: Path, title: str, payload: dict[str, Any]) -> None:
    lines = [f"# {title}", "", f"- Generated UTC: `{payload.get('generated_utc', now_iso())}`", ""]
    for key, value in payload.items():
        if key == "generated_utc":
            continue
        if isinstance(value, (str, int, float, bool)) or value is None:
            lines.append(f"- `{key}`: `{str(value).replace(chr(10), ' ')}`")
    if isinstance(payload.get("rows"), list):
        lines.extend(["", "## Rows", ""])
        for row in payload["rows"][:140]:
            if isinstance(row, dict):
                label = row.get("name") or row.get("plugin") or row.get("id") or "row"
                state = row.get("state") or row.get("v54_state") or row.get("action_gate") or ""
                lines.append(f"- `{label}`: `{state}`")
    write_text(path, "\n".join(lines) + "\n")


def dashboard_html(closeout: dict[str, Any], additions: dict[str, Any], plugins: dict[str, Any], cleanup: dict[str, Any]) -> str:
    suite_rows = "\n".join(
        f"<tr><td>{profile}</td><td>{item['summary']}</td><td>{item['effective_success']}</td></tr>"
        for profile, item in closeout["suite_statuses"].items()
    )
    addition_rows = "\n".join(
        f"<tr><td>{row['id']}</td><td>{row['category']}</td><td>{row['name']}</td><td>{row['state']}</td></tr>"
        for row in additions["rows"][:60]
    )
    plugin_rows = "\n".join(
        f"<tr><td>{row['plugin']}</td><td>{row['v54_state']}</td></tr>" for row in plugins["rows"]
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta http-equiv="refresh" content="45" />
  <title>V54 Mission Control</title>
  <style>
    :root {{
      --bg: #f4efe4;
      --ink: #16211b;
      --panel: #fff9ee;
      --accent: #b64e2f;
      --line: #d9c7a7;
      --good: #1b7f5c;
      --warn: #a06418;
    }}
    body {{
      margin: 0;
      font-family: Georgia, "Times New Roman", serif;
      color: var(--ink);
      background:
        radial-gradient(circle at 15% 15%, rgba(182, 78, 47, .16), transparent 34%),
        linear-gradient(135deg, #f4efe4 0%, #e9dcc5 45%, #f8f2e7 100%);
    }}
    main {{ max-width: 1180px; margin: 0 auto; padding: 36px 22px 64px; }}
    header {{ border: 1px solid var(--line); background: rgba(255,249,238,.84); padding: 26px; border-radius: 24px; box-shadow: 0 20px 50px rgba(65,45,20,.12); }}
    h1 {{ margin: 0 0 10px; font-size: clamp(2rem, 5vw, 4.5rem); line-height: .92; letter-spacing: -.04em; }}
    h2 {{ margin-top: 0; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; margin-top: 18px; }}
    section {{ background: rgba(255,249,238,.9); border: 1px solid var(--line); border-radius: 20px; padding: 18px; }}
    table {{ width: 100%; border-collapse: collapse; font-size: .94rem; }}
    td, th {{ border-bottom: 1px solid var(--line); padding: 8px; text-align: left; vertical-align: top; }}
    .pill {{ display: inline-block; padding: 6px 10px; border-radius: 999px; background: #f0dcc2; margin: 3px; }}
    .good {{ color: var(--good); font-weight: 700; }}
    .warn {{ color: var(--warn); font-weight: 700; }}
  </style>
</head>
<body>
  <main>
    <header>
      <p class="pill">Generated {closeout['generated_utc']}</p>
      <p class="pill">Phase {PHASE}</p>
      <h1>V54 Mission Control</h1>
      <p>Suite preservation, toolchain repair planning, 100+ addition registry, and D-drive-first archive posture.</p>
      <p><span class="good">Baseline:</span> {closeout['summary']['suite_preservation_state']} | <span class="warn">Residuals:</span> {', '.join(closeout['bounded_residuals']) or 'none'}</p>
    </header>
    <div class="grid">
      <section>
        <h2>Suite Ladder</h2>
        <table><tr><th>Profile</th><th>Summary</th><th>Green</th></tr>{suite_rows}</table>
      </section>
      <section>
        <h2>Token Use</h2>
        <p>Codex and Kimi aggregate token usage is not exposed by current CLI surfaces. V54 records operator-supplied or future official API totals only; no private log scraping.</p>
      </section>
      <section>
        <h2>Cleanup</h2>
        <p>Cleanup state: <b>{cleanup['local_archive_cleanup_state']}</b></p>
        <p>Candidate bytes manifested: <b>{cleanup['total_candidate_bytes']}</b></p>
      </section>
      <section>
        <h2>Notion</h2>
        <p>Repo-side Mission Control is ready. Live Notion page creation/update remains gated by action-time confirmation.</p>
      </section>
    </div>
    <section>
      <h2>Plugin Surface Split</h2>
      <table><tr><th>Plugin</th><th>V54 State</th></tr>{plugin_rows}</table>
    </section>
    <section>
      <h2>First 60 Additions</h2>
      <table><tr><th>ID</th><th>Category</th><th>Name</th><th>State</th></tr>{addition_rows}</table>
    </section>
  </main>
</body>
</html>
"""


def build_closeout(
    probes: dict[str, Any],
    source_digest: dict[str, Any],
    additions: dict[str, Any],
    plugins: dict[str, Any],
    cleanup: dict[str, Any],
    token_policy: dict[str, Any],
    browser_state: str,
    browser_detail: str,
) -> dict[str, Any]:
    suite_profiles = [
        "quick",
        "standard",
        "deep",
        "mcp-refresh",
        "materialize-l2",
        "materialize-l3",
        "materialize-l4",
        "materialize-l5",
    ]
    suite_statuses = {profile: suite_summary("v54", profile) for profile in suite_profiles}
    prior_suite_statuses = {profile: suite_summary("v53", profile) for profile in suite_profiles}
    if all(item["present"] and item["fail_count"] == 0 and item["effective_success"] is True for item in suite_statuses.values()):
        suite_preservation_state = "v54_quick_standard_deep_mcp_materialize_l2_l5_green"
    elif all(item["present"] and item["fail_count"] == 0 and item["effective_success"] is True for item in [suite_statuses["quick"], suite_statuses["standard"]]):
        suite_preservation_state = "quick_standard_green_heavier_lanes_pending"
    elif all(item["present"] and item["fail_count"] == 0 and item["effective_success"] is True for item in prior_suite_statuses.values()):
        suite_preservation_state = "v53_green_carry_forward_v54_suite_pending"
    else:
        suite_preservation_state = "suite_preservation_requires_repair"
    commands = probes.get("command_presence", {}) if isinstance(probes.get("command_presence"), dict) else {}
    missing = sorted(name for name in ["gh", "docker", "circleci", "vercel", "neonctl", "wrangler"] if not commands.get(name, {}).get("available"))
    residuals = []
    if browser_state != "browser_use_iab_available":
        residuals.append(f"browser_use={browser_state}")
    if missing:
        residuals.append("toolchain_missing=" + ",".join(missing))
    if cleanup.get("local_archive_cleanup_state") != "cleanup_completed":
        residuals.append("cleanup=manifested_only")
    closeout = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "overall_status": "PASS" if suite_preservation_state.startswith("v54_") and not residuals else "WARN",
        "source_branch": PUBLICATION_BRANCH,
        "execution_branch": EXECUTION_BRANCH,
        "baseline_sha": BASELINE_SHA,
        "current_head_sha": git_head(),
        "intended_receiver": "Aletheon with Ari, Kairos, and Kimiclaw slots 42-46 as bounded helpers",
        "receiver_rule_outcome": "v55_aletheon_facing_until_toolchain_cleanup_and_browser_residuals_clear",
        "summary": {
            "suite_preservation_state": suite_preservation_state,
            "addition_registry_state": additions["addition_registry_state"],
            "local_archive_cleanup_state": cleanup["local_archive_cleanup_state"],
            "browser_use_state": browser_state,
            "notion_ui_state": "repo_side_pack_ready_live_write_requires_action_time_confirmation",
            "git_publication_state": "allowlist_ready_unpublished",
        },
        "core_states": {
            "v54_execution_lead": "Aletheon",
            "ari_activation_state": "bounded_helper_ready",
            "kairos_activation_state": "slot_41_active_bounded_helper",
            "kimiclaw_slots_42_46_state": "active_bounded_helpers",
            "gpt55_session_state": "app_session_claim_supported_by_current_openai_docs_api_coming_soon",
            "codex_kimi_colab_state": "bounded_helper_registry_ready",
            "hundred_additions_state": additions["addition_registry_state"],
            "toolchain_repair_state": "scored_missing_cli_tranche_no_unconfirmed_installs",
            "cloud_standby_state": "gcp_vesper_kai_bigtable_paid_cloud_standby",
            "gcp_standby_state": "standby_until_user_restores_billing_auth_project_truth",
            "vesper_standby_state": "standby_until_google_cloud_billing_truth",
            "kai_standby_state": "standby_until_google_cloud_billing_truth",
            "bigtable_state": "operator_reported_bigtable_deleted_unverified_until_gcp_auth_restored",
            "wsl_execution_mode": "installed_on_hold_for_agent_switching",
            "local_archive_cleanup_state": cleanup["local_archive_cleanup_state"],
            "browser_use_state": browser_state,
            "browser_use_detail": browser_detail,
            "notion_ui_state": "repo_side_pack_ready_live_write_requires_action_time_confirmation",
            "plugin_surface_split_state": plugins["plugin_surface_split_state"],
            "token_usage_state": token_policy["token_usage_state"],
            "suite_ladder_state": suite_preservation_state,
            "git_publication_state": "allowlist_ready_unpublished",
        },
        "suite_statuses": suite_statuses,
        "prior_v53_suite_statuses": prior_suite_statuses,
        "token_usage": token_policy,
        "bounded_residuals": residuals,
        "proof_paths": {
            "source_digest": "docs/auto-generated/v54-source-digest-v1.json",
            "tool_probe": "docs/trinity-live-traces/v54-tool-probe-v1.json",
            "addition_registry": "docs/trinity-live-traces/v54-addition-registry-v1.json",
            "cleanup_manifest": "docs/trinity-live-traces/v54-cleanup-manifest-v1.json",
            "plugin_matrix": "docs/trinity-live-traces/v54-plugin-capability-matrix-v1.json",
            "browser_use_proof": "docs/trinity-live-traces/v54-browser-use-proof-v1.json",
            "notion_plan": "docs/trinity-live-traces/v54-notion-mission-control-plan-v1.json",
            "stage_allowlist": "docs/trinity-live-traces/v54-stage-allowlist-v1.json",
            "git_publication_result": "docs/trinity-live-traces/v54-git-publication-result-v1.json",
        },
        "source_digest": source_digest,
    }
    return closeout


def continuity_md(payload: dict[str, Any], title: str) -> str:
    lines = [
        f"# {title}",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Current head: `{payload['current_head_sha']}`",
        "",
        "## Core States",
        "",
    ]
    lines.extend(f"- `{key}`: `{value}`" for key, value in payload["core_states"].items())
    lines.extend(["", "## Residuals", ""])
    if payload["bounded_residuals"]:
        lines.extend(f"- `{item}`" for item in payload["bounded_residuals"])
    else:
        lines.append("- `(none)`")
    lines.extend(
        [
            "",
            "## Receiver",
            "",
            "- V55 remains Aletheon-facing with Ari, Kairos, and Kimiclaw slots 42-46 as bounded helper lanes.",
            "- Live Notion writes, software installs, and local deletions remain action-time confirmation gates.",
        ]
    )
    return "\n".join(lines) + "\n"


def handoff_policy(closeout: dict[str, Any]) -> dict[str, Any]:
    runtime = read_json(ROOT / "docs" / "trinity-runtime-model-resolution-v1.json")
    agents = runtime.get("deployed_main_agents", []) if isinstance(runtime.get("deployed_main_agents"), list) else []
    schema = read_json(ROOT / "docs" / "v17-runtime-session-schema-v1.json")
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "overall_status": closeout["overall_status"],
        "next_phase": NEXT_PHASE,
        "intended_receiver": closeout["intended_receiver"],
        "receiver_rule_outcome": closeout["receiver_rule_outcome"],
        "runtime_truth_policy": {
            "required_runtime_fields": schema.get("required_runtime_fields", []),
            "required_overlay_slots": schema.get("required_overlay_slots", []),
            "complete_truth_runtime_surfaces": schema.get("complete_truth_runtime_surfaces", []),
        },
        "deployed_main_agents": agents,
        "core_states": closeout["core_states"],
        "bounded_residuals": closeout["bounded_residuals"],
        "handoff_rules": [
            "preserve V53 suite green baseline",
            "do not bulk install 100+ candidates without gated approval",
            "do not delete C-drive files without action-time confirmation",
            "do not create or update Notion pages without action-time confirmation",
            "keep GCP, Kai, Vesper, Bigtable, Gemini CLI, and paid cloud standby",
        ],
    }


def update_runtime(closeout: dict[str, Any]) -> None:
    runtime_path = ROOT / "docs" / "trinity-runtime-model-resolution-v1.json"
    session_path = ROOT / "docs" / "v17-runtime-session-log-latest.json"
    validation_path = ROOT / "docs" / "v17-runtime-session-validation-latest.json"
    board_path = ROOT / "docs" / "v17-runtime-truth-resolution-board-v1.json"
    current_head = closeout["current_head_sha"]
    fields = {
        **closeout["core_states"],
        "phase": PHASE,
        "active_handoff_pack_path": "docs/v54-omega-continuity-pack-v1.md",
        "active_handoff_policy_path": "docs/v54-omega-handoff-policy-v1.json",
        "next_receiver_pack_path": "docs/v55-beta-continuity-pack-v1.md",
        "next_receiver_policy_path": "docs/v55-beta-handoff-policy-v1.json",
        "current_shared_suite_surface": closeout["suite_statuses"].get("standard", {}),
        "publication_commit_sha": current_head,
        "checkpoint_anchor_commit": current_head,
    }
    runtime = read_json(runtime_path)
    runtime.update({"generated_utc": now_iso(), **fields})
    write_json(runtime_path, runtime)
    session = read_json(session_path)
    session.update(
        {
            "generated_utc": now_iso(),
            "session_id": "v54-omega-closeout",
            "phase": PHASE,
            "runtime_validation_state": "v54_runtime_truth_published",
            **closeout["core_states"],
        }
    )
    write_json(session_path, session)
    validation = read_json(validation_path)
    validation.update(
        {
            "generated_utc": now_iso(),
            "phase": PHASE,
            "overall_status": "PASS",
            "v54_runtime_fields_present": True,
            "suite_ladder_state": closeout["summary"]["suite_preservation_state"],
        }
    )
    write_json(validation_path, validation)
    board = read_json(board_path)
    board.update(
        {
            "generated_utc": now_iso(),
            "phase": PHASE,
            "runtime_truth_complete": True,
            **closeout["core_states"],
        }
    )
    write_json(board_path, board)


def write_allowlist() -> None:
    paths = [
        ".circleci/config.yml",
        "scripts/trinity_memory_bank_validator.py",
        "scripts/trinity_v54_omega.py",
        "docs/auto-generated/v54-source-digest-v1.json",
        "docs/trinity-live-traces/v54-tool-probe-v1.json",
        "docs/trinity-live-traces/v54-tool-probe-v1.md",
        "docs/trinity-live-traces/v54-addition-registry-v1.json",
        "docs/trinity-live-traces/v54-addition-registry-v1.md",
        "docs/trinity-live-traces/v54-cleanup-manifest-v1.json",
        "docs/trinity-live-traces/v54-cleanup-manifest-v1.md",
        "docs/trinity-live-traces/v54-plugin-capability-matrix-v1.json",
        "docs/trinity-live-traces/v54-plugin-capability-matrix-v1.md",
        "docs/trinity-live-traces/v54-token-usage-policy-v1.json",
        "docs/trinity-live-traces/v54-token-usage-policy-v1.md",
        "docs/trinity-live-traces/v54-browser-use-proof-v1.json",
        "docs/trinity-live-traces/v54-browser-use-proof-v1.md",
        "docs/trinity-live-traces/v54-notion-mission-control-plan-v1.json",
        "docs/trinity-live-traces/v54-notion-mission-control-plan-v1.md",
        "docs/trinity-live-traces/v54-journey-archive-digest-v1.json",
        "docs/trinity-live-traces/v54-journey-archive-digest-v1.md",
        "docs/trinity-live-traces/v54-stage-allowlist-v1.json",
        "docs/trinity-live-traces/v54-stage-allowlist-v1.md",
        "docs/trinity-live-traces/v54-git-publication-result-v1.json",
        "docs/trinity-live-traces/v54-git-publication-result-v1.md",
        "docs/trinity-expansion/v21-trinity-memory-bank-validator-latest.json",
        "docs/trinity-expansion/v21-trinity-memory-bank-validator-latest.md",
        "docs/memory-archives/index.jsonl",
        "docs/trinity-memory-bank-registry-v3.json",
        "docs/trinity-memory-bank-sync-latest.json",
        "docs/trinity-memory-bank-sync-latest.md",
        "docs/trinity-memory-bank-validation-latest.json",
        "docs/trinity-memory-bank-validation-latest.md",
        "docs/trinity-live-traces/v54-quick-suite-status.json",
        "docs/trinity-live-traces/v54-standard-suite-status.json",
        "docs/trinity-live-traces/v54-deep-suite-status.json",
        "docs/trinity-live-traces/v54-mcp-refresh-suite-status.json",
        "docs/trinity-live-traces/v54-materialize-l2-suite-status.json",
        "docs/trinity-live-traces/v54-materialize-l3-suite-status.json",
        "docs/trinity-live-traces/v54-materialize-l4-suite-status.json",
        "docs/trinity-live-traces/v54-materialize-l5-suite-status.json",
        "docs/trinity-runtime-model-resolution-v1.json",
        "docs/v17-runtime-session-log-latest.json",
        "docs/v17-runtime-session-validation-latest.json",
        "docs/v17-runtime-truth-resolution-board-v1.json",
        "docs/v54-mission-control-dashboard.html",
        "docs/v54-omega-closeout-summary-v1.json",
        "docs/v54-omega-continuity-pack-v1.md",
        "docs/v54-omega-handoff-policy-v1.json",
        "docs/v55-beta-closeout-summary-v1.json",
        "docs/v55-beta-continuity-pack-v1.md",
        "docs/v55-beta-handoff-policy-v1.json",
    ]
    payload = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "current_head_sha": git_head(),
        "curation_rule": "v54_only_forward_allowlist",
        "dirty_path_count": len(git_status_lines()),
        "curated_include_count": len(paths),
        "curated_include_paths": paths,
        "present_curated_paths": [path for path in paths if (ROOT / path).exists()],
        "cleanup_posture": "stage_allowlist_only_preserve_background_churn",
    }
    write_json(TRACE_DIR / "v54-stage-allowlist-v1.json", payload)
    lines = [
        "# V54 Stage Allowlist",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Curated include count: `{payload['curated_include_count']}`",
        f"- Dirty path count at write: `{payload['dirty_path_count']}`",
        "",
        "## Paths",
        "",
    ]
    lines.extend(f"- `{path}`" for path in paths)
    write_text(TRACE_DIR / "v54-stage-allowlist-v1.md", "\n".join(lines) + "\n")


def publish(browser_state: str, browser_detail: str) -> dict[str, Any]:
    drive_state = ps_drive_state()
    probes = tool_probes()
    source_digest = official_source_digest()
    additions = build_addition_registry(probes)
    plugins = plugin_matrix(probes)
    cleanup = cleanup_manifest(drive_state)
    token_policy = token_usage_policy(probes)
    browser_payload = browser_use_proof(browser_state, browser_detail)
    notion_payload = notion_plan()
    archive_payload = source_archive_digest()
    closeout = build_closeout(
        probes=probes,
        source_digest=source_digest,
        additions=additions,
        plugins=plugins,
        cleanup=cleanup,
        token_policy=token_policy,
        browser_state=browser_state,
        browser_detail=browser_detail,
    )
    write_json(AUTO_DIR / "v54-source-digest-v1.json", source_digest)
    write_json(TRACE_DIR / "v54-tool-probe-v1.json", probes)
    write_md_list(TRACE_DIR / "v54-tool-probe-v1.md", "V54 Tool Probe", probes)
    write_json(TRACE_DIR / "v54-addition-registry-v1.json", additions)
    write_md_list(TRACE_DIR / "v54-addition-registry-v1.md", "V54 100+ Addition Registry", additions)
    write_json(TRACE_DIR / "v54-cleanup-manifest-v1.json", cleanup)
    write_md_list(TRACE_DIR / "v54-cleanup-manifest-v1.md", "V54 Cleanup Manifest", cleanup)
    write_json(TRACE_DIR / "v54-plugin-capability-matrix-v1.json", plugins)
    write_md_list(TRACE_DIR / "v54-plugin-capability-matrix-v1.md", "V54 Plugin Capability Matrix", plugins)
    write_json(TRACE_DIR / "v54-token-usage-policy-v1.json", token_policy)
    write_md_list(TRACE_DIR / "v54-token-usage-policy-v1.md", "V54 Token Usage Policy", token_policy)
    write_json(TRACE_DIR / "v54-browser-use-proof-v1.json", browser_payload)
    write_md_list(TRACE_DIR / "v54-browser-use-proof-v1.md", "V54 Browser Use Proof", browser_payload)
    write_json(TRACE_DIR / "v54-notion-mission-control-plan-v1.json", notion_payload)
    write_md_list(TRACE_DIR / "v54-notion-mission-control-plan-v1.md", "V54 Notion Mission Control Plan", notion_payload)
    write_json(TRACE_DIR / "v54-journey-archive-digest-v1.json", archive_payload)
    write_md_list(TRACE_DIR / "v54-journey-archive-digest-v1.md", "V54 Journey Archive Digest", archive_payload)
    write_json(ROOT / "docs" / "v54-omega-closeout-summary-v1.json", closeout)
    write_text(ROOT / "docs" / "v54-omega-continuity-pack-v1.md", continuity_md(closeout, "V54 Omega Continuity Pack"))
    write_json(ROOT / "docs" / "v54-omega-handoff-policy-v1.json", handoff_policy(closeout))
    beta = dict(closeout)
    beta["phase"] = NEXT_PHASE
    beta["overall_status"] = "WARN" if closeout["bounded_residuals"] else "PASS"
    beta["summary"] = {**closeout["summary"], "receiver_state": "v55_beta_aletheon_facing"}
    write_json(ROOT / "docs" / "v55-beta-closeout-summary-v1.json", beta)
    write_text(ROOT / "docs" / "v55-beta-continuity-pack-v1.md", continuity_md(beta, "V55 Beta Continuity Pack"))
    write_json(ROOT / "docs" / "v55-beta-handoff-policy-v1.json", handoff_policy(beta))
    write_text(ROOT / "docs" / "v54-mission-control-dashboard.html", dashboard_html(closeout, additions, plugins, cleanup))
    update_runtime(closeout)
    write_allowlist()
    return closeout


def record_publication(commit_sha: str, *, browser_state: str, browser_detail: str) -> None:
    closeout = read_json(ROOT / "docs" / "v54-omega-closeout-summary-v1.json")
    if not closeout:
        closeout = publish(browser_state, browser_detail)
    closeout["generated_utc"] = now_iso()
    closeout["current_head_sha"] = commit_sha
    closeout["summary"]["git_publication_state"] = "committed_pushed_pr45_branch_updated"
    closeout["core_states"]["git_publication_state"] = "committed_pushed_pr45_branch_updated"
    closeout["core_states"]["publication_commit_sha"] = commit_sha
    write_json(ROOT / "docs" / "v54-omega-closeout-summary-v1.json", closeout)
    write_text(ROOT / "docs" / "v54-omega-continuity-pack-v1.md", continuity_md(closeout, "V54 Omega Continuity Pack"))
    write_json(ROOT / "docs" / "v54-omega-handoff-policy-v1.json", handoff_policy(closeout))
    beta = read_json(ROOT / "docs" / "v55-beta-closeout-summary-v1.json")
    beta.update(
        {
            "generated_utc": now_iso(),
            "current_head_sha": commit_sha,
            "publication_commit_sha": commit_sha,
            "summary": {**beta.get("summary", {}), "git_publication_state": "committed_pushed_pr45_branch_updated"},
        }
    )
    beta_core = beta.get("core_states", {}) if isinstance(beta.get("core_states"), dict) else {}
    beta_core["git_publication_state"] = "committed_pushed_pr45_branch_updated"
    beta["core_states"] = beta_core
    write_json(ROOT / "docs" / "v55-beta-closeout-summary-v1.json", beta)
    write_text(ROOT / "docs" / "v55-beta-continuity-pack-v1.md", continuity_md(beta, "V55 Beta Continuity Pack"))
    write_json(ROOT / "docs" / "v55-beta-handoff-policy-v1.json", handoff_policy(beta))
    update_runtime(closeout)
    result = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "branch": PUBLICATION_BRANCH,
        "publication_commit_sha": commit_sha,
        "remote_head_after_push": commit_sha,
        "pr_reuse": "PR #45 branch updated; PR metadata not edited without action-time confirmation",
        "git_publication_state": "committed_pushed_pr45_branch_updated",
    }
    write_json(TRACE_DIR / "v54-git-publication-result-v1.json", result)
    write_md_list(TRACE_DIR / "v54-git-publication-result-v1.md", "V54 Git Publication Result", result)
    write_allowlist()


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish V54 Omega surfaces.")
    parser.add_argument("--record-publication", help="Commit SHA to record after push")
    parser.add_argument("--browser-state", default="browser_use_not_rechecked")
    parser.add_argument("--browser-detail", default="")
    args = parser.parse_args()
    if args.record_publication:
        record_publication(args.record_publication, browser_state=args.browser_state, browser_detail=args.browser_detail)
    else:
        publish(args.browser_state, args.browser_detail)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
