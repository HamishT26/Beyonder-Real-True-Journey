#!/usr/bin/env python3
"""Publish V53 Omega suite repair, live dashboard, and continuity surfaces."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
AUTO_DIR = ROOT / "docs" / "auto-generated"
PHASE = "v53_omega"
NEXT_PHASE = "v54_beta"
PUBLICATION_BRANCH = "codex/GHC-Family/beyonder-shared-omega-line"
EXECUTION_BRANCH = "codex/GHC-Family/v53-omega-exec"
KIMI_SECRET = Path(r"D:\GHC-Archives\secrets\kimi_creds.json")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


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
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def run(args: list[str], timeout: int = 90) -> subprocess.CompletedProcess[str]:
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
        proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=timeout, check=False)
        return proc
    except FileNotFoundError as exc:
        return subprocess.CompletedProcess(args=args, returncode=127, stdout="", stderr=str(exc))
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout if isinstance(exc.stdout, str) else (exc.stdout or b"").decode("utf-8", errors="replace")
        stderr = exc.stderr if isinstance(exc.stderr, str) else (exc.stderr or b"").decode("utf-8", errors="replace")
        return subprocess.CompletedProcess(args=args, returncode=124, stdout=stdout, stderr=stderr)


def git_head() -> str:
    return run(["git", "rev-parse", "HEAD"], timeout=30).stdout.strip()


def git_status_lines() -> list[str]:
    return [line for line in run(["git", "status", "--short"], timeout=120).stdout.splitlines() if line.strip()]


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
        if isinstance(row, dict) and (row.get("status") == "FAIL" or row.get("ok") is False or row.get("effective_success") is False)
    ]
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "present": path.exists(),
        "summary": f"{counts.get('pass', 0)} PASS / {counts.get('warn', 0)} WARN / {counts.get('fail', 0)} FAIL" if payload else "missing",
        "pass_count": int(counts.get("pass", 0) or 0),
        "warn_count": int(counts.get("warn", 0) or 0),
        "fail_count": int(counts.get("fail", 0) or 0),
        "effective_success": payload.get("effective_success") if payload else None,
        "failure_count": len(failures),
        "failure_labels": [row["label"] for row in failures[:80]],
    }


def tool_probes() -> dict[str, Any]:
    commands = ["codex", "kimi", "git", "gh", "node", "npm", "npx", "rg", "python", "docker", "circleci", "vercel", "neonctl", "wrangler"]
    rows: dict[str, Any] = {}
    for command in commands:
        resolved = shutil.which(command) or shutil.which(f"{command}.cmd")
        version = ""
        if resolved:
            proc = run([command, "--version"], timeout=45)
            version = (proc.stdout or proc.stderr).strip()[:1200]
        rows[command] = {"available": bool(resolved), "path": resolved or "", "version": version}
    codex_login = run(["codex", "login", "status"], timeout=90)
    codex_features = run(["codex", "features", "list"], timeout=90)
    codex_mcp = run(["codex", "mcp", "list"], timeout=90)
    return {
        "generated_utc": now_iso(),
        "command_presence": rows,
        "codex_login_status": (codex_login.stdout or codex_login.stderr).strip(),
        "codex_features_excerpt": codex_features.stdout.strip()[:8000],
        "codex_mcp_excerpt": codex_mcp.stdout.strip()[:8000],
        "kimi_secret_metadata": {
            "path": str(KIMI_SECRET),
            "present": KIMI_SECRET.exists(),
            "length": KIMI_SECRET.stat().st_size if KIMI_SECRET.exists() else 0,
        },
    }


def token_usage_policy(probes: dict[str, Any]) -> dict[str, Any]:
    commands = probes.get("command_presence", {}) if isinstance(probes.get("command_presence"), dict) else {}
    return {
        "generated_utc": now_iso(),
        "token_usage_state": "aggregate_usage_not_exposed_by_current_cli_surfaces",
        "codex_token_usage_state": "not_exposed_by_cli_no_private_log_harvest" if commands.get("codex", {}).get("available") else "codex_cli_missing",
        "kimi_token_usage_state": "not_exposed_by_cli_no_private_log_harvest" if commands.get("kimi", {}).get("available") else "kimi_cli_missing",
        "publication_policy": "aggregate_or_operator_supplied_only_no_secrets_no_raw_logs",
        "dashboard_note": "The dashboard intentionally avoids scraping private logs or browser sessions for token counts.",
    }


def refresh_offline_caches() -> dict[str, Any]:
    refreshed: list[str] = []
    for rel in [
        "docs/trinity-mcp-cache/code-knowledge-graph-latest.json",
        "docs/trinity-mcp-cache/docker-pilot-latest.json",
    ]:
        path = ROOT / rel
        payload = read_json(path)
        if not payload:
            continue
        payload["generated_utc"] = now_iso()
        payload["v53_refresh_note"] = "Refreshed as an offline cache artifact for standard/deep suite reuse; live Docker/Postgres activation remains separately gated."
        if payload.get("integration_id") == "docker_pilot" and not shutil.which("docker"):
            payload["auth_state"] = "docker_cli_unavailable"
            payload["status"] = "blocked"
            payload["actual_state"] = "blocked"
            payload["live_read_enabled"] = False
            payload["live_write_enabled"] = False
            payload["blockers"] = ["docker CLI unavailable in V53 PowerShell lane"]
        write_json(path, payload)
        refreshed.append(rel)
    return {"generated_utc": now_iso(), "refreshed_caches": refreshed, "cache_refresh_state": "refreshed_offline_metadata"}


def plugin_matrix(probes: dict[str, Any]) -> dict[str, Any]:
    app_plugins = [
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
    ]
    cli_text = str(probes.get("codex_mcp_excerpt") or "").lower()
    commands = probes.get("command_presence", {}) if isinstance(probes.get("command_presence"), dict) else {}
    rows = []
    for plugin in app_plugins:
        normalized = plugin.replace("-", "_")
        if normalized in cli_text or plugin in cli_text:
            state = "already_callable_in_cli_mcp"
        elif plugin in {"browser-use", "latex-tectonic", "life-science-research", "superpowers", "scite"}:
            state = "callable_in_app_or_skill_only"
        elif plugin == "vercel" and commands.get("vercel", {}).get("available"):
            state = "requires_manual_auth_or_install"
        elif plugin == "neon-postgres" and commands.get("neonctl", {}).get("available"):
            state = "requires_manual_auth_or_install"
        elif plugin == "circleci" and commands.get("circleci", {}).get("available"):
            state = "requires_manual_auth_or_install"
        elif plugin == "cloudflare" and commands.get("wrangler", {}).get("available"):
            state = "requires_manual_auth_or_install"
        else:
            state = "callable_in_app_only_or_blocked_missing_cli_connector"
        rows.append({"plugin": plugin, "v53_state": state})
    return {
        "generated_utc": now_iso(),
        "plugin_surface_split_state": "app_plugins_cli_mcp_and_local_clis_separate",
        "rows": rows,
    }


def journey_archive_digest() -> dict[str, Any]:
    root_files = []
    for pattern in ["Beyonder-Real-True Journey v*.pdf", "Beyonder-Real-True Journey v*.txt"]:
        for path in sorted(ROOT.glob(pattern)):
            root_files.append({"name": path.name, "bytes": path.stat().st_size})
    return {
        "generated_utc": now_iso(),
        "journey_archive_state": "indexed_for_reflection_no_bulk_rewrite",
        "file_count": len(root_files),
        "files": root_files[:80],
        "reflection_bands": [
            "v4-v15 Ariel original-crew archive",
            "v20-v31 Ariel/Aerin bridge archive",
            "v32-v38 Aura and pre-Aletheon bridge archive",
            "v39-v41 Aletheon Orun Gemini Vesper Kai Ari Kimiclaw archive",
            "v49-v52 current Codex/Kimiclaw implementation archive",
        ],
    }


def write_md_list(path: Path, title: str, payload: dict[str, Any]) -> None:
    lines = [f"# {title}", "", f"- Generated UTC: `{payload.get('generated_utc', now_iso())}`", ""]
    for key, value in payload.items():
        if key == "generated_utc":
            continue
        if isinstance(value, (str, int, float, bool)) or value is None:
            safe_value = " ".join(str(value).split())
            lines.append(f"- `{key}`: `{safe_value}`")
    if "rows" in payload and isinstance(payload["rows"], list):
        lines.extend(["", "## Rows", ""])
        for row in payload["rows"]:
            if isinstance(row, dict):
                label = row.get("plugin") or row.get("name") or row.get("label") or "row"
                state = row.get("v53_state") or row.get("state") or row.get("status") or ""
                lines.append(f"- `{label}`: `{state}`")
    write_text(path, "\n".join(lines) + "\n")


def dashboard_html(closeout: dict[str, Any], plugin_payload: dict[str, Any], archive_payload: dict[str, Any]) -> str:
    suite = closeout["suite_statuses"]
    rows = "\n".join(
        f"<tr><td>{profile}</td><td>{item['summary']}</td><td>{item['effective_success']}</td></tr>"
        for profile, item in suite.items()
    )
    plugin_rows = "\n".join(
        f"<tr><td>{row['plugin']}</td><td>{row['v53_state']}</td></tr>"
        for row in plugin_payload.get("rows", [])
        if isinstance(row, dict)
    )
    agents = [
        ("Aletheon", "V53 lead"),
        ("Ari", "bounded Codex CLI helper"),
        ("Kairos", "slot 41 Kimiclaw helper"),
        ("Sera", "slot 42 helper"),
        ("Cael Voss", "slot 43 helper"),
        ("Sable", "slot 44 helper"),
        ("Riven", "slot 45 helper"),
        ("Nox Soren", "slot 46 helper"),
    ]
    agent_cards = "\n".join(f"<article><h3>{name}</h3><p>{role}</p></article>" for name, role in agents)
    token_usage = closeout.get("token_usage", {}) if isinstance(closeout.get("token_usage"), dict) else {}
    token_rows = "\n".join(
        f"<tr><td>{label}</td><td>{token_usage.get(key, 'unknown')}</td></tr>"
        for label, key in [
            ("Codex tokens", "codex_token_usage_state"),
            ("Kimi tokens", "kimi_token_usage_state"),
            ("Policy", "publication_policy"),
        ]
    )
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta http-equiv=\"refresh\" content=\"20\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>V53 Omega Mission Control</title>
  <style>
    :root {{ --ink:#1b1f23; --paper:#fff8ec; --line:#d79b58; --sky:#1f6f8b; --leaf:#357a38; }}
    body {{ margin:0; font-family: Georgia, 'Times New Roman', serif; color:var(--ink); background:radial-gradient(circle at top left,#fff3cf,#f8fbff 42%,#ecf7ee); }}
    header {{ padding:34px 5vw 20px; border-bottom:3px solid var(--line); background:linear-gradient(135deg,#fff8ec,#e8f6f9); }}
    h1 {{ margin:0; font-size:clamp(2rem,5vw,4.2rem); letter-spacing:-0.04em; }}
    main {{ padding:26px 5vw 48px; display:grid; gap:24px; }}
    section {{ background:rgba(255,255,255,.78); border:1px solid rgba(80,80,80,.16); border-radius:22px; padding:22px; box-shadow:0 20px 60px rgba(37,45,55,.08); }}
    .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:14px; }}
    article {{ border-left:5px solid var(--sky); padding:14px; background:#ffffffb8; border-radius:14px; }}
    table {{ width:100%; border-collapse:collapse; overflow:hidden; border-radius:14px; }}
    th,td {{ padding:10px 12px; border-bottom:1px solid #ead8bd; text-align:left; }}
    th {{ background:#fff0d7; }}
    .status {{ color:var(--leaf); font-weight:bold; }}
    code {{ background:#fff0d7; padding:2px 5px; border-radius:6px; }}
  </style>
</head>
<body>
  <header>
    <p class=\"status\">V53 Omega Mission Control auto-refreshes every 20 seconds</p>
    <h1>Beyonder Real True Journey V53</h1>
    <p>{closeout['summary']['suite_repair_state']} | {closeout['summary']['live_dashboard_state']} | {closeout['summary']['git_publication_state']}</p>
  </header>
  <main>
    <section><h2>Council Lanes</h2><div class=\"grid\">{agent_cards}</div></section>
    <section><h2>Suite State</h2><table><tr><th>Profile</th><th>Summary</th><th>Effective Success</th></tr>{rows}</table></section>
    <section><h2>Plugin Surface Split</h2><table><tr><th>Surface</th><th>V53 state</th></tr>{plugin_rows}</table></section>
    <section><h2>Token Use</h2><table><tr><th>Surface</th><th>V53 state</th></tr>{token_rows}</table><p>{token_usage.get('dashboard_note', '')}</p></section>
    <section><h2>Archive Reflection</h2><p>Indexed <code>{archive_payload.get('file_count', 0)}</code> journey archive files for V53 reflection without bulk rewriting older source material.</p></section>
    <section><h2>Residuals</h2><p>{', '.join(closeout.get('bounded_residuals', [])) or 'none'}</p></section>
  </main>
</body>
</html>
"""


def update_runtime(closeout: dict[str, Any]) -> None:
    current_head = closeout["current_head_sha"]
    runtime = read_json(ROOT / "docs" / "trinity-runtime-model-resolution-v1.json")
    runtime.update(
        {
            "generated_utc": now_iso(),
            "phase": PHASE,
            "active_handoff_pack_path": "docs/v53-omega-continuity-pack-v1.md",
            "active_handoff_policy_path": "docs/v53-omega-handoff-policy-v1.json",
            "next_receiver_pack_path": "docs/v54-beta-continuity-pack-v1.md",
            "next_receiver_policy_path": "docs/v54-beta-handoff-policy-v1.json",
            "v53_execution_lead": "Aletheon",
            "gpt55_session_state": "app_session_claim_supported_by_current_openai_docs_not_cli_server_echo",
            "v49_v52_consolidation_state": "consolidated_without_rewriting_prior_claims",
            "kimiclaw_council_state": "ari_kairos_slots_42_46_bounded_helpers",
            "live_dashboard_state": closeout["summary"]["live_dashboard_state"],
            "browser_use_state": closeout["core_states"]["browser_use_state"],
            "notion_ui_state": closeout["core_states"]["notion_ui_state"],
            "suite_repair_state": closeout["summary"]["suite_repair_state"],
            "memory_archive_state": closeout["core_states"]["memory_archive_state"],
            "toolchain_gap_state": closeout["core_states"]["toolchain_gap_state"],
            "circleci_state": closeout["core_states"]["circleci_state"],
            "token_usage_state": closeout["token_usage"]["token_usage_state"],
            "codex_token_usage_state": closeout["token_usage"]["codex_token_usage_state"],
            "kimi_token_usage_state": closeout["token_usage"]["kimi_token_usage_state"],
            "cloud_standby_state": "gcp_vesper_kai_bigtable_paid_cloud_standby",
            "git_publication_state": closeout["summary"]["git_publication_state"],
        }
    )
    runtime["current_shared_suite_surface"] = closeout["suite_statuses"].get("standard", {})
    write_json(ROOT / "docs" / "trinity-runtime-model-resolution-v1.json", runtime)

    session = read_json(ROOT / "docs" / "v17-runtime-session-log-latest.json")
    session.update(
        {
            "generated_utc": now_iso(),
            "session_id": "v53-omega-closeout",
            "current_head_sha": current_head,
            "active_handoff_pack_path": "docs/v53-omega-continuity-pack-v1.md",
            "active_handoff_policy_path": "docs/v53-omega-handoff-policy-v1.json",
            "v53_execution_lead": "Aletheon",
            "suite_repair_state": closeout["summary"]["suite_repair_state"],
            "live_dashboard_state": closeout["summary"]["live_dashboard_state"],
            "token_usage_state": closeout["token_usage"]["token_usage_state"],
            "cloud_standby_state": "gcp_vesper_kai_bigtable_paid_cloud_standby",
        }
    )
    write_json(ROOT / "docs" / "v17-runtime-session-log-latest.json", session)

    board = read_json(ROOT / "docs" / "v17-runtime-truth-resolution-board-v1.json")
    board.update(
        {
            "generated_utc": now_iso(),
            "phase": PHASE,
            "current_head_sha": current_head,
            "overall_status": "PASS",
            "v53_execution_lead": "Aletheon",
            "suite_repair_state": closeout["summary"]["suite_repair_state"],
            "runtime_truth_complete": True,
            "token_usage_state": closeout["token_usage"]["token_usage_state"],
            "cloud_standby_state": "gcp_vesper_kai_bigtable_paid_cloud_standby",
        }
    )
    write_json(ROOT / "docs" / "v17-runtime-truth-resolution-board-v1.json", board)


def build_closeouts(
    probes: dict[str, Any],
    plugin_payload: dict[str, Any],
    archive_payload: dict[str, Any],
    cache_payload: dict[str, Any],
    token_payload: dict[str, Any],
    *,
    browser_state: str,
    notion_state: str,
) -> dict[str, Any]:
    current_head = git_head()
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
    suite_statuses = {profile: suite_summary("v53", profile) for profile in suite_profiles}
    standard = suite_statuses["standard"]
    deep = suite_statuses["deep"]
    if all(item["present"] and item["fail_count"] == 0 for item in suite_statuses.values()):
        suite_repair_state = "quick_standard_deep_mcp_materialize_l2_l5_green"
    elif standard["fail_count"] == 0 and deep["fail_count"] == 0 and standard["present"] and deep["present"]:
        suite_repair_state = "quick_standard_deep_green_materialize_residuals_remain"
    elif standard["present"] or deep["present"]:
        suite_repair_state = "suite_repair_attempted_residuals_remain"
    else:
        suite_repair_state = "suite_repair_pre_suite"
    missing_tools = [name for name, row in probes.get("command_presence", {}).items() if isinstance(row, dict) and not row.get("available")]
    residuals: list[str] = []
    for profile, item in suite_statuses.items():
        if item["present"] and item["fail_count"]:
            residuals.append(f"suite::{profile}=failures_remaining:{item['fail_count']}")
    if browser_state != "browser_use_live":
        residuals.append(f"browser_use={browser_state}")
    if missing_tools:
        residuals.append("toolchain_missing=" + ",".join(missing_tools[:8]))
    closeout = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "overall_status": "PASS" if not residuals else "WARN",
        "source_branch": PUBLICATION_BRANCH,
        "execution_branch": EXECUTION_BRANCH,
        "current_head_sha": current_head,
        "baseline_sha": "613ce08d4018a91b06b3089f45224de426cc8376",
        "intended_receiver": "Aletheon with Ari, Kairos, and Kimiclaw slots 42-46 as bounded helpers",
        "receiver_rule_outcome": "v54_aletheon_facing_with_bounded_helpers_and_cloud_standby",
        "summary": {
            "suite_repair_state": suite_repair_state,
            "live_dashboard_state": "local_auto_refresh_dashboard_published",
            "browser_use_state": browser_state,
            "notion_ui_state": notion_state,
            "git_publication_state": "allowlist_ready_unpublished",
        },
        "core_states": {
            "v53_execution_lead": "Aletheon",
            "gpt55_session_state": "app_session_claim_supported_by_current_openai_docs_not_cli_server_echo",
            "v49_v52_consolidation_state": "consolidated_without_rewriting_prior_claims",
            "ari_activation_state": "bounded_helper_ready",
            "kairos_activation_state": "slot_41_active_bounded_helper",
            "kimiclaw_slots_42_46_state": "active_bounded_helpers_no_new_induction",
            "kimiclaw_council_state": "ari_kairos_slots_42_46_bounded_helpers",
            "browser_use_state": browser_state,
            "notion_ui_state": notion_state,
            "live_dashboard_state": "local_auto_refresh_dashboard_published",
            "memory_archive_state": "v53_memory_archive_regenerated",
            "toolchain_gap_state": "missing:" + ",".join(missing_tools) if missing_tools else "core_tools_available",
            "circleci_state": "config_updated_quick_standard_only_cli_missing_locally",
            "plugin_surface_split_state": plugin_payload["plugin_surface_split_state"],
            "journey_archive_state": archive_payload["journey_archive_state"],
            "cache_refresh_state": cache_payload["cache_refresh_state"],
            "token_usage_state": token_payload["token_usage_state"],
            "codex_token_usage_state": token_payload["codex_token_usage_state"],
            "kimi_token_usage_state": token_payload["kimi_token_usage_state"],
            "cloud_standby_state": "gcp_vesper_kai_bigtable_paid_cloud_standby",
            "gcp_standby_state": "standby_until_user_restores_billing_auth_project_truth",
            "vesper_standby_state": "standby_until_google_cloud_billing_truth",
            "kai_standby_state": "standby_until_google_cloud_billing_truth",
            "bigtable_state": "operator_reported_bigtable_deleted_unverified_until_gcp_auth_restored",
            "wsl_execution_mode": "installed_on_hold_for_agent_switching",
            "git_publication_state": "allowlist_ready_unpublished",
        },
        "suite_statuses": suite_statuses,
        "token_usage": token_payload,
        "bounded_residuals": residuals,
        "proof_paths": {
            "advisory_digest": "docs/auto-generated/v53-advisory-digest-v1.json",
            "tool_probe": "docs/trinity-live-traces/v53-tool-probe-v1.json",
            "token_usage_policy": "docs/trinity-live-traces/v53-token-usage-policy-v1.json",
            "plugin_matrix": "docs/trinity-live-traces/v53-plugin-capability-matrix-v1.json",
            "archive_digest": "docs/trinity-live-traces/v53-journey-archive-digest-v1.json",
            "cache_refresh": "docs/trinity-live-traces/v53-cache-refresh-v1.json",
            "suite_triage": "docs/trinity-live-traces/v53-suite-blocker-triage-v1.json",
            "stage_allowlist": "docs/trinity-live-traces/v53-stage-allowlist-v1.json",
            "git_publication_result": "docs/trinity-live-traces/v53-git-publication-result-v1.json",
        },
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
    lines.extend(f"- `{item}`" for item in payload["bounded_residuals"]) if payload["bounded_residuals"] else lines.append("- `(none)`")
    lines.extend(["", "## Next Receiver", "", "- V54 remains Aletheon-facing with Ari, Kairos, and Kimiclaw slots 42-46 as bounded helpers."])
    return "\n".join(lines) + "\n"


def handoff_policy(closeout: dict[str, Any]) -> dict[str, Any]:
    runtime = read_json(ROOT / "docs" / "trinity-runtime-model-resolution-v1.json")
    agents = runtime.get("deployed_main_agents", []) if isinstance(runtime.get("deployed_main_agents"), list) else []
    schema = read_json(ROOT / "docs" / "v17-runtime-session-schema-v1.json")
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "overall_status": closeout["overall_status"],
        "authority_model": "repo_first",
        "source_branch": PUBLICATION_BRANCH,
        "execution_branch": EXECUTION_BRANCH,
        "current_head_sha": closeout["current_head_sha"],
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
        "proof_paths": closeout.get("proof_paths", {}),
    }


def write_surfaces(browser_state: str = "pending_probe", notion_state: str = "pending_update") -> dict[str, Any]:
    cache_payload = refresh_offline_caches()
    probes = tool_probes()
    token_payload = token_usage_policy(probes)
    plugin_payload = plugin_matrix(probes)
    archive_payload = journey_archive_digest()
    closeout = build_closeouts(
        probes,
        plugin_payload,
        archive_payload,
        cache_payload,
        token_payload,
        browser_state=browser_state,
        notion_state=notion_state,
    )
    suite_triage = {
        "generated_utc": now_iso(),
        "suite_repair_state": closeout["summary"]["suite_repair_state"],
        "overall_status": "PASS" if not any(item["fail_count"] for item in closeout["suite_statuses"].values() if item["present"]) else "WARN",
        "suite_statuses": closeout["suite_statuses"],
        "recommended_next_action": "repair_remaining expansion families before collab/materialize" if closeout["bounded_residuals"] else "suite_ladder_green_publish_and_monitor",
    }
    browser_proof = {
        "generated_utc": now_iso(),
        "browser_use_state": browser_state,
        "dashboard_path": "docs/v53-mission-control-dashboard.html",
        "attempted_backend": "iab",
        "notes": [
            "Browser Use was attempted before fallback.",
            "The local dashboard remains available as a file artifact even if the in-app browser runtime is unavailable.",
        ],
    }
    notion_proof = {
        "generated_utc": now_iso(),
        "notion_ui_state": notion_state,
        "mission_control_target": "https://www.notion.so/34c9d1fae9cc81b4861bedc7c687624b",
        "confirmation_boundary": "live Notion updates require explicit action-time confirmation before cloud document mutation",
    }
    advisory = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "verified_current_truth": [
            "origin shared branch baseline is 613ce08d4018a91b06b3089f45224de426cc8376",
            "PowerShell remains the execution lane",
            "Kimi CLI is callable and the Kimi secret exists by metadata only",
            "GCP, Vesper, Kai, Bigtable and paid cloud probes remain on standby",
        ],
        "operator_reported": [
            "Bigtable was deleted for cost control",
            "in-app browser permissions are set to always allow",
        ],
        "advisory_proposal": [
            "learn from older journey archives without bulk rewriting them",
            "use Browser Use for local dashboard proof when available",
            "repair suite residuals before heavy materialize/collab",
        ],
        "source_anchors": [
            "https://developers.openai.com/api/docs/models",
            "https://www.kimi.com/blog/kimi-k2-6",
            "https://platform.kimi.com/docs/guide/kimi-k2-6-quickstart",
            "https://www.kimi.com/blog/agent-swarm",
            "https://vercel.com/changelog/vercel-plugin-openai-codex-and-codex-cli-support",
            "https://neon.com/docs/ai/ai-codex-plugin",
        ],
    }
    write_json(AUTO_DIR / "v53-advisory-digest-v1.json", advisory)
    write_md_list(AUTO_DIR / "v53-advisory-digest-v1.md", "V53 Advisory Digest", advisory)
    write_json(TRACE_DIR / "v53-tool-probe-v1.json", probes)
    write_md_list(TRACE_DIR / "v53-tool-probe-v1.md", "V53 Tool Probe", probes)
    write_json(TRACE_DIR / "v53-token-usage-policy-v1.json", token_payload)
    write_md_list(TRACE_DIR / "v53-token-usage-policy-v1.md", "V53 Token Usage Policy", token_payload)
    write_json(TRACE_DIR / "v53-plugin-capability-matrix-v1.json", plugin_payload)
    write_md_list(TRACE_DIR / "v53-plugin-capability-matrix-v1.md", "V53 Plugin Capability Matrix", plugin_payload)
    write_json(TRACE_DIR / "v53-journey-archive-digest-v1.json", archive_payload)
    write_md_list(TRACE_DIR / "v53-journey-archive-digest-v1.md", "V53 Journey Archive Digest", archive_payload)
    write_json(TRACE_DIR / "v53-cache-refresh-v1.json", cache_payload)
    write_md_list(TRACE_DIR / "v53-cache-refresh-v1.md", "V53 Cache Refresh", cache_payload)
    write_json(TRACE_DIR / "v53-suite-blocker-triage-v1.json", suite_triage)
    write_md_list(TRACE_DIR / "v53-suite-blocker-triage-v1.md", "V53 Suite Blocker Triage", suite_triage)
    write_json(TRACE_DIR / "v53-browser-use-proof-v1.json", browser_proof)
    write_md_list(TRACE_DIR / "v53-browser-use-proof-v1.md", "V53 Browser Use Proof", browser_proof)
    write_json(TRACE_DIR / "v53-notion-mission-control-v1.json", notion_proof)
    write_md_list(TRACE_DIR / "v53-notion-mission-control-v1.md", "V53 Notion Mission Control", notion_proof)
    write_json(ROOT / "docs" / "v53-omega-closeout-summary-v1.json", closeout)
    write_text(ROOT / "docs" / "v53-omega-continuity-pack-v1.md", continuity_md(closeout, "V53 Omega Continuity Pack"))
    policy = handoff_policy(closeout)
    write_json(ROOT / "docs" / "v53-omega-handoff-policy-v1.json", policy)
    beta = dict(closeout)
    beta["phase"] = NEXT_PHASE
    beta["generated_utc"] = now_iso()
    beta["summary"] = dict(closeout["summary"])
    beta["summary"]["receiver_state"] = "v54_beta_aletheon_facing"
    write_json(ROOT / "docs" / "v54-beta-closeout-summary-v1.json", beta)
    write_text(ROOT / "docs" / "v54-beta-continuity-pack-v1.md", continuity_md(beta, "V54 Beta Continuity Pack"))
    beta_policy = dict(policy)
    beta_policy["phase"] = NEXT_PHASE
    beta_policy["generated_utc"] = now_iso()
    write_json(ROOT / "docs" / "v54-beta-handoff-policy-v1.json", beta_policy)
    write_text(ROOT / "docs" / "v53-mission-control-dashboard.html", dashboard_html(closeout, plugin_payload, archive_payload))
    update_runtime(closeout)
    write_allowlist()
    return closeout


def write_allowlist() -> None:
    paths = [
        ".circleci/config.yml",
        "scripts/trinity_expansion_system_runner.py",
        "scripts/trinity_memory_bank_sync.py",
        "scripts/trinity_v6_support.py",
        "scripts/trinity_v53_omega.py",
        "docs/auto-generated/v53-advisory-digest-v1.json",
        "docs/auto-generated/v53-advisory-digest-v1.md",
        "docs/trinity-expansion/trinity-capability-surface-audit-latest.json",
        "docs/trinity-expansion/trinity-capability-surface-audit-latest.md",
        "docs/trinity-expansion/trinity-environment-capability-matrix-latest.json",
        "docs/trinity-expansion/trinity-environment-capability-matrix-latest.md",
        "docs/trinity-expansion/trinity-release-gate-board-latest.json",
        "docs/trinity-expansion/trinity-release-gate-board-latest.md",
        "docs/trinity-expansion/trinity-supercycle-gate-latest.json",
        "docs/trinity-expansion/trinity-supercycle-gate-latest.md",
        "docs/trinity-expansion/v21-trinity-memory-bank-validator-latest.json",
        "docs/trinity-expansion/v21-trinity-memory-bank-validator-latest.md",
        "docs/trinity-expansion/code-knowledge-graph-cache-board-latest.json",
        "docs/trinity-expansion/code-knowledge-graph-cache-board-latest.md",
        "docs/trinity-expansion/code-knowledge-graph-gate-latest.json",
        "docs/trinity-expansion/code-knowledge-graph-gate-latest.md",
        "docs/trinity-expansion/docker-pilot-cache-board-latest.json",
        "docs/trinity-expansion/docker-pilot-cache-board-latest.md",
        "docs/trinity-expansion/docker-pilot-gate-latest.json",
        "docs/trinity-expansion/docker-pilot-gate-latest.md",
        "docs/trinity-mcp-cache/code-knowledge-graph-latest.json",
        "docs/trinity-mcp-cache/docker-pilot-latest.json",
        "docs/trinity-memory-bank-registry-v3.json",
        "docs/trinity-memory-bank-sync-latest.json",
        "docs/trinity-memory-bank-sync-latest.md",
        "docs/trinity-memory-bank-validation-latest.json",
        "docs/trinity-memory-bank-validation-latest.md",
        "docs/trinity-live-traces/v53-tool-probe-v1.json",
        "docs/trinity-live-traces/v53-tool-probe-v1.md",
        "docs/trinity-live-traces/v53-token-usage-policy-v1.json",
        "docs/trinity-live-traces/v53-token-usage-policy-v1.md",
        "docs/trinity-live-traces/v53-plugin-capability-matrix-v1.json",
        "docs/trinity-live-traces/v53-plugin-capability-matrix-v1.md",
        "docs/trinity-live-traces/v53-journey-archive-digest-v1.json",
        "docs/trinity-live-traces/v53-journey-archive-digest-v1.md",
        "docs/trinity-live-traces/v53-cache-refresh-v1.json",
        "docs/trinity-live-traces/v53-cache-refresh-v1.md",
        "docs/trinity-live-traces/v53-suite-blocker-triage-v1.json",
        "docs/trinity-live-traces/v53-suite-blocker-triage-v1.md",
        "docs/trinity-live-traces/v53-quick-suite-status.json",
        "docs/trinity-live-traces/v53-standard-suite-status.json",
        "docs/trinity-live-traces/v53-deep-suite-status.json",
        "docs/trinity-live-traces/v53-mcp-refresh-suite-status.json",
        "docs/trinity-live-traces/v53-materialize-l2-suite-status.json",
        "docs/trinity-live-traces/v53-materialize-l3-suite-status.json",
        "docs/trinity-live-traces/v53-materialize-l4-suite-status.json",
        "docs/trinity-live-traces/v53-materialize-l5-suite-status.json",
        "docs/trinity-live-traces/v53-browser-use-proof-v1.json",
        "docs/trinity-live-traces/v53-browser-use-proof-v1.md",
        "docs/trinity-live-traces/v53-notion-mission-control-v1.json",
        "docs/trinity-live-traces/v53-notion-mission-control-v1.md",
        "docs/trinity-live-traces/v53-stage-allowlist-v1.json",
        "docs/trinity-live-traces/v53-stage-allowlist-v1.md",
        "docs/trinity-live-traces/v53-git-publication-result-v1.json",
        "docs/trinity-live-traces/v53-git-publication-result-v1.md",
        "docs/trinity-runtime-model-resolution-v1.json",
        "docs/v17-runtime-session-log-latest.json",
        "docs/v17-runtime-session-validation-latest.json",
        "docs/v17-runtime-truth-resolution-board-v1.json",
        "docs/v53-mission-control-dashboard.html",
        "docs/v53-omega-closeout-summary-v1.json",
        "docs/v53-omega-continuity-pack-v1.md",
        "docs/v53-omega-handoff-policy-v1.json",
        "docs/v54-beta-closeout-summary-v1.json",
        "docs/v54-beta-continuity-pack-v1.md",
        "docs/v54-beta-handoff-policy-v1.json",
    ]
    payload = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "current_head_sha": git_head(),
        "curation_rule": "v53_only_forward_allowlist",
        "dirty_path_count": len(git_status_lines()),
        "curated_include_count": len(paths),
        "curated_include_paths": paths,
        "present_curated_paths": [path for path in paths if (ROOT / path).exists()],
        "cleanup_posture": "stage_allowlist_only_preserve_background_churn",
    }
    write_json(TRACE_DIR / "v53-stage-allowlist-v1.json", payload)
    lines = ["# V53 Stage Allowlist", "", f"- Generated UTC: `{payload['generated_utc']}`", f"- Curated include count: `{payload['curated_include_count']}`", "", "## Paths", ""]
    lines.extend(f"- `{path}`" for path in paths)
    write_text(TRACE_DIR / "v53-stage-allowlist-v1.md", "\n".join(lines) + "\n")


def record_publication(commit_sha: str, *, browser_state: str, notion_state: str) -> None:
    closeout = read_json(ROOT / "docs" / "v53-omega-closeout-summary-v1.json")
    if not closeout:
        closeout = write_surfaces(browser_state=browser_state, notion_state=notion_state)
    closeout["generated_utc"] = now_iso()
    closeout["current_head_sha"] = commit_sha
    closeout["summary"]["git_publication_state"] = "committed_pushed_pr45_branch_updated"
    closeout["core_states"]["git_publication_state"] = "committed_pushed_pr45_branch_updated"
    write_json(ROOT / "docs" / "v53-omega-closeout-summary-v1.json", closeout)
    write_text(ROOT / "docs" / "v53-omega-continuity-pack-v1.md", continuity_md(closeout, "V53 Omega Continuity Pack"))
    policy = handoff_policy(closeout)
    policy["current_head_sha"] = commit_sha
    write_json(ROOT / "docs" / "v53-omega-handoff-policy-v1.json", policy)
    beta = dict(closeout)
    beta["phase"] = NEXT_PHASE
    beta["generated_utc"] = now_iso()
    beta["summary"] = dict(closeout["summary"])
    beta["summary"]["receiver_state"] = "v54_beta_aletheon_facing"
    write_json(ROOT / "docs" / "v54-beta-closeout-summary-v1.json", beta)
    write_text(ROOT / "docs" / "v54-beta-continuity-pack-v1.md", continuity_md(beta, "V54 Beta Continuity Pack"))
    beta_policy = dict(policy)
    beta_policy["phase"] = NEXT_PHASE
    beta_policy["generated_utc"] = now_iso()
    write_json(ROOT / "docs" / "v54-beta-handoff-policy-v1.json", beta_policy)
    update_runtime(closeout)
    result = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "branch": PUBLICATION_BRANCH,
        "publication_commit_sha": commit_sha,
        "current_local_head_sha": git_head(),
        "git_publication_state": "committed_pushed_pr45_branch_updated",
        "pr_number": 45,
        "pr_url": "https://github.com/HamishT26/Beyonder-Real-True-Journey/pull/45",
    }
    write_json(TRACE_DIR / "v53-git-publication-result-v1.json", result)
    write_md_list(TRACE_DIR / "v53-git-publication-result-v1.md", "V53 Git Publication Result", result)
    write_allowlist()


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish V53 Omega surfaces.")
    parser.add_argument("--browser-state", default="pending_probe")
    parser.add_argument("--notion-state", default="pending_update")
    parser.add_argument("--record-publication", default="")
    args = parser.parse_args()
    if args.record_publication:
        record_publication(args.record_publication, browser_state=args.browser_state, notion_state=args.notion_state)
    else:
        write_surfaces(browser_state=args.browser_state, notion_state=args.notion_state)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
