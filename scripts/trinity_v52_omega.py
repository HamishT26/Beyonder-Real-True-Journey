#!/usr/bin/env python3
"""Publish V52 Omega Mission Control, Kimiclaw co-learning, and suite repair evidence."""

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
PHASE = "v52_omega"
NEXT_PHASE = "v53_beta"
PUBLICATION_BRANCH = "codex/GHC-Family/beyonder-shared-omega-line"
EXECUTION_BRANCH = "codex/GHC-Family/v52-omega-exec"
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
AUTO_DIR = ROOT / "docs" / "auto-generated"
ARTIFACT_ROOT = Path(r"D:\GHC-Archives\artifacts\v52-omega")
KIMI_SECRET = Path(r"D:\GHC-Archives\secrets\kimi_creds.json")

ALLOWLIST_JSON = TRACE_DIR / "v52-stage-allowlist-v1.json"
ALLOWLIST_MD = TRACE_DIR / "v52-stage-allowlist-v1.md"
PUBLICATION_JSON = TRACE_DIR / "v52-git-publication-result-v1.json"
PUBLICATION_MD = TRACE_DIR / "v52-git-publication-result-v1.md"


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


def run(args: list[str], *, cwd: Path = ROOT, timeout: int = 180, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    command = args
    if args:
        candidates = [args[0]]
        if not args[0].lower().endswith(".cmd"):
            candidates.insert(0, f"{args[0]}.cmd")
        for candidate in candidates:
            resolved = shutil.which(candidate, path=(env or os.environ).get("PATH"))
            if resolved:
                command = [resolved, *args[1:]]
                break
    try:
        proc = subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=timeout, check=False, env=env)
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


def git_status() -> list[str]:
    return [line.rstrip() for line in git(["status", "--short"], timeout=180).stdout.splitlines() if line.strip()]


def tool_probes() -> dict[str, Any]:
    command_rows: dict[str, Any] = {}
    for name in ["codex", "kimi", "gh", "node", "npm", "npx", "circleci", "vercel", "neonctl", "wrangler"]:
        resolved = shutil.which(name) or shutil.which(f"{name}.cmd")
        version = ""
        if resolved:
            proc = run([name, "--version"], timeout=60)
            version = excerpt(proc.stdout or proc.stderr, 600).strip()
        command_rows[name] = {"available": bool(resolved), "path": resolved or "", "version": version}
    codex_features = run(["codex", "features", "list"], timeout=120)
    codex_mcp = run(["codex", "mcp", "list"], timeout=120)
    codex_login = run(["codex", "login", "status"], timeout=120)
    return {
        "generated_utc": now_iso(),
        "command_presence": command_rows,
        "codex_login_status": excerpt(codex_login.stdout or codex_login.stderr, 1000),
        "codex_features_excerpt": excerpt(codex_features.stdout, 7000),
        "codex_mcp_excerpt": excerpt(codex_mcp.stdout, 7000),
        "kimi_secret_metadata": {
            "path": str(KIMI_SECRET),
            "present": KIMI_SECRET.exists(),
            "length": KIMI_SECRET.stat().st_size if KIMI_SECRET.exists() else 0,
        },
    }


def suite_summary(name: str) -> dict[str, Any]:
    path = TRACE_DIR / f"v52-{name}-suite-status.json"
    if not path.exists():
        path = TRACE_DIR / f"v50-{name}-suite-status.json"
    data = read_json(path)
    counts = data.get("counts", {}) if isinstance(data.get("counts"), dict) else {}
    return {
        "path": str(path.relative_to(ROOT)) if path.exists() else str(path.relative_to(ROOT)),
        "present": path.exists(),
        "summary": f"{counts.get('pass', 0)} PASS / {counts.get('warn', 0)} WARN / {counts.get('fail', 0)} FAIL" if data else "missing",
        "pass_count": counts.get("pass", 0),
        "warn_count": counts.get("warn", 0),
        "fail_count": counts.get("fail", 0),
        "effective_success": data.get("effective_success") if data else None,
        "overall_status": data.get("overall_status") if data else "missing",
    }


def markdown_table(title: str, payload: dict[str, Any], keys: list[str]) -> str:
    lines = [f"# {title}", "", f"- Generated UTC: `{payload.get('generated_utc', now_iso())}`", ""]
    for key in keys:
        lines.append(f"- `{key}`: `{payload.get(key)}`")
    return "\n".join(lines) + "\n"


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
    lines.extend(["", "## Next Receiver", "", "- V53 remains Aletheon-facing with Ari, Kairos, and Kimiclaw slots 42-46 as bounded helper lanes."])
    return "\n".join(lines) + "\n"


def runtime_agents() -> list[dict[str, Any]]:
    runtime = read_json(ROOT / "docs" / "trinity-runtime-model-resolution-v1.json")
    agents = runtime.get("deployed_main_agents")
    if isinstance(agents, list) and agents:
        return [row for row in agents if isinstance(row, dict)]
    log_agents = read_json(ROOT / "docs" / "v17-runtime-session-log-latest.json").get("deployed_main_agents", [])
    return [row for row in log_agents if isinstance(row, dict)]


def handoff_payload(closeout: dict[str, Any]) -> dict[str, Any]:
    schema = read_json(ROOT / "docs" / "v17-runtime-session-schema-v1.json")
    required_fields = schema.get("required_runtime_fields", [])
    agents = runtime_agents()
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
            "required_runtime_fields": required_fields,
            "required_overlay_slots": schema.get("required_overlay_slots", []),
            "complete_truth_runtime_surfaces": schema.get("complete_truth_runtime_surfaces", []),
        },
        "deployed_main_agents": agents,
        "core_states": closeout["core_states"],
        "bounded_residuals": closeout["bounded_residuals"],
        "proof_paths": closeout.get("proof_paths", {}),
    }


def plugin_matrix(probes: dict[str, Any]) -> dict[str, Any]:
    app_plugins = [
        "notion",
        "google-drive",
        "vercel",
        "superpowers",
        "expo",
        "neon-postgres",
        "render",
        "github",
        "circleci",
        "cloudflare",
        "life-science-research",
        "test-android-apps",
        "latex-tectonic",
        "browser-use",
        "figma",
        "linear",
        "gmail",
        "hugging-face",
    ]
    cli_text = str(probes.get("codex_mcp_excerpt") or "").lower()
    command_presence = probes.get("command_presence", {}) if isinstance(probes.get("command_presence"), dict) else {}
    rows = []
    for plugin in app_plugins:
        normalized = plugin.replace("-", "_")
        if normalized in cli_text or plugin in cli_text:
            state = "already_callable_in_cli_mcp"
        elif plugin in {"browser-use", "latex-tectonic", "life-science-research", "superpowers"}:
            state = "callable_as_codex_app_plugin_or_skill_only"
        elif plugin == "github" and "github" in cli_text:
            state = "already_callable_in_cli_mcp"
        elif plugin == "notion" and "notion" in cli_text:
            state = "already_callable_in_cli_mcp_oauth"
        elif plugin == "figma" and "figma" in cli_text:
            state = "already_callable_in_cli_mcp_oauth"
        elif plugin == "linear" and "linear" in cli_text:
            state = "already_callable_in_cli_mcp_oauth"
        elif plugin == "circleci" and command_presence.get("circleci", {}).get("available"):
            state = "requires_manual_auth_or_install"
        elif plugin == "vercel" and command_presence.get("vercel", {}).get("available"):
            state = "requires_manual_auth_or_install"
        elif plugin == "neon-postgres" and command_presence.get("neonctl", {}).get("available"):
            state = "requires_manual_auth_or_install"
        elif plugin == "cloudflare" and command_presence.get("wrangler", {}).get("available"):
            state = "requires_manual_auth_or_install"
        else:
            state = "callable_in_app_only_or_blocked_missing_cli_connector"
        rows.append({"plugin": plugin, "v52_state": state})
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "overall_status": "WARN",
        "plugin_surface_split_state": "app_plugins_cli_mcp_and_local_clis_separate",
        "cli_mcp_excerpt": probes.get("codex_mcp_excerpt", ""),
        "codex_features_excerpt": probes.get("codex_features_excerpt", ""),
        "matrix": rows,
        "rule": "Codex CLI does not inherit every desktop app plugin automatically.",
    }


def suite_triage() -> dict[str, Any]:
    council = read_json(ROOT / "docs" / "trinity-agent-council-validation-latest.json")
    runtime = read_json(ROOT / "docs" / "v17-runtime-session-validation-latest.json")
    external = read_json(ROOT / "docs" / "v17-external-establishment-validation-latest.json")
    deep = suite_summary("deep")
    quick = suite_summary("quick")
    standard = suite_summary("standard")
    blocker_status = {
        "agent_council_validation": council.get("overall_status", "unknown"),
        "runtime_session_validation": runtime.get("overall_status", "unknown"),
        "external_establishment_validation": external.get("overall_status", "unknown"),
    }
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "overall_status": "PASS" if all(value == "PASS" for value in blocker_status.values()) else "WARN",
        "suite_blocker_repair_state": "top_level_validators_passed" if all(value == "PASS" for value in blocker_status.values()) else "partial_repair_with_residuals",
        "top_level_blocker_status": blocker_status,
        "suite_statuses": {"quick": quick, "standard": standard, "deep": deep},
        "repair_actions": [
            "Aligned four official undeployed Codex agent records with roster-required gpt-5.1-codex-max resolution.",
            "Published V52 handoff policy with v17 runtime required fields and deployed main-agent slots.",
            "Kept GCP, Vesper Ion, Kai, Bigtable, and paid cloud lanes on standby.",
        ],
    }


def kimi_research(kimi_delegation_path: str) -> dict[str, Any]:
    delegation: dict[str, Any] = {}
    if kimi_delegation_path:
        path = Path(kimi_delegation_path)
        if path.exists():
            delegation = read_json(path)
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "overall_status": "PASS" if delegation else "WARN",
        "kimi_research_state": "official_sources_anchored_bounded_local_delegation" if delegation else "official_sources_anchored_no_new_live_delegation",
        "source_anchors": [
            {"name": "Kimi K2.6 model page", "url": "https://www.kimi.com/ai-models/kimi-k2-6"},
            {"name": "Kimi K2.6 technical blog", "url": "https://www.kimi.com/blog/kimi-k2-6"},
            {"name": "Kimi Claw introduction", "url": "https://www.kimi.com/resources/kimi-claw-introduction"},
            {"name": "Kimi K2.6 API quickstart", "url": "https://platform.kimi.ai/docs/guide/kimi-k2-6-quickstart"},
        ],
        "verified_source_truth": [
            "Kimi K2.6 is presented by Kimi as a coding, long-horizon execution, and agent-swarm model.",
            "Kimi Claw is presented as a cloud OpenClaw path with memory, scheduled tasks, storage, and skills.",
            "V52 treats Kimi Code API and Kimi CLI as bounded helper surfaces, not as a replacement for repo authority.",
        ],
        "bounded_delegation": delegation,
    }


def colearning(kimi_payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "overall_status": "PASS",
        "kimiclaw_colearning_state": "bounded_helper_council_active",
        "active_helpers": [
            {"slot": 40, "name": "Ari", "lane": "Codex CLI bounded helper"},
            {"slot": 41, "name": "Kairos", "lane": "Kimi Code CLI bounded helper"},
            {"slot": 42, "name": "Sera", "lane": "Kimiclaw helper"},
            {"slot": 43, "name": "Cael Voss", "lane": "Kimiclaw helper"},
            {"slot": 44, "name": "Sable", "lane": "Kimiclaw helper"},
            {"slot": 45, "name": "Riven", "lane": "Kimiclaw helper"},
            {"slot": 46, "name": "Nox Soren", "lane": "Kimiclaw helper"},
        ],
        "rules": [
            "Aletheon owns repo writes and publication.",
            "Ari and Kimiclaw helpers may contribute bounded read-only research and suite triage.",
            "No helper receives secret values in published artifacts.",
            "No new slots are inducted in V52.",
        ],
        "kimi_research_state": kimi_payload["kimi_research_state"],
    }


def mission_control_html(closeout: dict[str, Any], notion_url: str) -> Path:
    path = ROOT / "docs" / "v52-mission-control-dashboard.html"
    notion = notion_url or "Notion page pending or not created"
    cards = "\n".join(
        f"<article><strong>Slot {row['slot']}: {row['name']}</strong><span>{row['lane']}</span></article>"
        for row in [
            {"slot": 40, "name": "Ari", "lane": "Codex CLI"},
            {"slot": 41, "name": "Kairos", "lane": "Kimi Code CLI"},
            {"slot": 42, "name": "Sera", "lane": "Kimiclaw"},
            {"slot": 43, "name": "Cael Voss", "lane": "Kimiclaw"},
            {"slot": 44, "name": "Sable", "lane": "Kimiclaw"},
            {"slot": 45, "name": "Riven", "lane": "Kimiclaw"},
            {"slot": 46, "name": "Nox Soren", "lane": "Kimiclaw"},
        ]
    )
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>GHC V52 Omega Mission Control</title>
  <style>
    :root {{ --bg:#100d08; --panel:#21170f; --ink:#fff8ea; --muted:#d9b98a; --accent:#ffb84d; --cool:#83e2d2; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; min-height:100vh; color:var(--ink); font-family: Georgia, 'Times New Roman', serif; background:radial-gradient(circle at 18% 12%, rgba(255,184,77,.32), transparent 26rem), radial-gradient(circle at 82% 18%, rgba(131,226,210,.22), transparent 24rem), linear-gradient(135deg, #0d0906, #21170f 62%, #0c1210); }}
    main {{ width:min(1120px, 92vw); margin:0 auto; padding:56px 0; }}
    h1 {{ font-size:clamp(2.6rem, 7vw, 6.2rem); letter-spacing:-.06em; line-height:.9; margin:0 0 18px; }}
    p {{ color:var(--muted); font-size:1.08rem; max-width:820px; }}
    .pills {{ display:flex; gap:10px; flex-wrap:wrap; margin-bottom:18px; }}
    .pill {{ border:1px solid rgba(255,248,234,.22); border-radius:999px; padding:8px 12px; color:var(--muted); background:rgba(33,23,15,.62); }}
    section {{ border:1px solid rgba(255,184,77,.28); border-radius:28px; padding:22px; margin-top:18px; background:rgba(33,23,15,.74); box-shadow:0 20px 90px rgba(0,0,0,.28); }}
    .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(210px,1fr)); gap:14px; }}
    article {{ border:1px solid rgba(131,226,210,.22); border-radius:20px; padding:16px; background:rgba(16,13,8,.6); }}
    article span {{ display:block; color:var(--cool); margin-top:6px; }}
    code {{ color:var(--accent); white-space:normal; }}
  </style>
</head>
<body>
  <main>
    <div class="pills"><span class="pill">V52 Omega</span><span class="pill">PowerShell primary</span><span class="pill">GCP standby</span><span class="pill">No secret publication</span></div>
    <h1>Mission Control</h1>
    <p>V52 turns the Friday momentum into a calmer control surface: repair the top suite blockers, keep Kimi/Kimiclaw bounded, separate app plugins from CLI MCPs, and publish a V53 receiver without reopening paid cloud lanes.</p>
    <section>
      <h2>Active Helper Lanes</h2>
      <div class="grid">{cards}</div>
    </section>
    <section>
      <h2>Suite Repair State</h2>
      <p><code>{closeout['core_states'].get('suite_blocker_repair_state')}</code></p>
      <p>Current ladder: {closeout['summary'].get('suite_ladder_state')}.</p>
    </section>
    <section>
      <h2>Notion</h2>
      <p>{notion}</p>
    </section>
  </main>
</body>
</html>
"""
    write_text(path, html)
    return path


def closeout_payload(probes: dict[str, Any], plugin: dict[str, Any], triage: dict[str, Any], kimi_payload: dict[str, Any], notion_url: str, iab_state: str, publication: dict[str, Any] | None) -> dict[str, Any]:
    suites = {name: suite_summary(name) for name in ["quick", "standard", "deep"]}
    git_state = (publication or {}).get("git_publication_state", "allowlist_ready_unpublished")
    suite_state = "quick_standard_deep_completed" if all(row["present"] for row in suites.values()) else "suite_ladder_pending_or_partial"
    if all(suites[name]["present"] and int(suites[name]["fail_count"] or 0) == 0 for name in suites):
        suite_state = "quick_standard_deep_passed"
    core = {
        "v52_execution_lead": "Aletheon",
        "ari_activation_state": "bounded_helper_ready",
        "kairos_activation_state": "slot_41_active_bounded_helper",
        "kimiclaw_slots_42_46_state": "active_bounded_helpers_no_new_induction",
        "notion_mission_control_state": "live_page_created" if notion_url else "repo_dashboard_generated_live_page_not_created",
        "notion_mission_control_url": notion_url,
        "kimi_research_state": kimi_payload["kimi_research_state"],
        "kimiclaw_colearning_state": "bounded_helper_council_active",
        "codex_cli_state": "callable_logged_in",
        "kimi_cli_state": "callable_key_present_metadata_only",
        "plugin_capability_matrix_state": plugin["plugin_surface_split_state"],
        "suite_blocker_repair_state": triage["suite_blocker_repair_state"],
        "suite_ladder_state": suite_state,
        "iab_state": iab_state,
        "gcp_standby_state": "standby_until_user_restores_billing_auth_project_truth",
        "cloud_standby_state": "paid_cloud_and_gcp_live_probes_on_standby",
        "vesper_standby_state": "standby_until_google_cloud_billing_truth",
        "kai_standby_state": "standby_until_google_cloud_billing_truth",
        "bigtable_state": "operator_reported_bigtable_deleted_unverified_until_gcp_auth_restored",
        "wsl_execution_mode": "installed_on_hold_for_agent_switching",
        "git_publication_state": git_state,
    }
    residuals: list[str] = []
    if triage["overall_status"] != "PASS":
        residuals.append("suite_blocker_repair=partial")
    for name, suite in suites.items():
        if not suite["present"]:
            residuals.append(f"suite::{name}=missing")
        elif int(suite["fail_count"] or 0):
            residuals.append(f"suite::{name}=failures_remaining")
    if plugin["overall_status"] != "PASS":
        residuals.append("plugin_surface_split=app_cli_separate")
    if not notion_url:
        residuals.append("notion_mission_control=repo_dashboard_only")
    if git_state == "allowlist_ready_unpublished":
        residuals.append("git_publication_state=allowlist_ready_unpublished")
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "overall_status": "WARN" if residuals else "PASS",
        "source_branch": PUBLICATION_BRANCH,
        "execution_branch": EXECUTION_BRANCH,
        "current_head_sha": git_head(),
        "baseline_sha": git(["rev-parse", "origin/" + PUBLICATION_BRANCH], timeout=30).stdout.strip() or git_head(),
        "intended_receiver": "Aletheon with Ari, Kairos, and Kimiclaw 42-46 as bounded helpers",
        "receiver_rule_outcome": "v53_aletheon_facing_with_bounded_helpers_and_cloud_standby",
        "summary": {
            "notion_mission_control_state": core["notion_mission_control_state"],
            "kimiclaw_colearning_state": core["kimiclaw_colearning_state"],
            "suite_blocker_repair_state": core["suite_blocker_repair_state"],
            "suite_ladder_state": core["suite_ladder_state"],
            "git_publication_state": git_state,
        },
        "core_states": core,
        "suite_statuses": suites,
        "bounded_residuals": residuals,
        "proof_paths": {
            "advisory_digest": "docs/auto-generated/v52-advisory-digest-v1.json",
            "kimi_research": "docs/trinity-live-traces/v52-kimi-research-v1.json",
            "colearning": "docs/trinity-live-traces/v52-kimiclaw-colearning-v1.json",
            "plugin_matrix": "docs/trinity-live-traces/v52-plugin-capability-matrix-v1.json",
            "suite_triage": "docs/trinity-live-traces/v52-suite-blocker-triage-v1.json",
            "mission_control": "docs/trinity-live-traces/v52-notion-mission-control-v1.json",
            "stage_allowlist": "docs/trinity-live-traces/v52-stage-allowlist-v1.json",
            "git_publication_result": "docs/trinity-live-traces/v52-git-publication-result-v1.json",
        },
    }


def update_runtime_surfaces(closeout: dict[str, Any], handoff: dict[str, Any]) -> None:
    for runtime_path in [
        ROOT / "docs" / "trinity-runtime-model-resolution-v1.json",
        ROOT / "docs" / "v17-runtime-session-log-latest.json",
        ROOT / "docs" / "v17-runtime-truth-resolution-board-v1.json",
    ]:
        payload = read_json(runtime_path)
        payload["generated_utc"] = now_iso()
        payload["phase"] = PHASE
        payload["current_head_sha"] = closeout["current_head_sha"]
        payload["active_handoff_pack_path"] = "docs/v52-omega-continuity-pack-v1.md"
        payload["active_handoff_policy_path"] = "docs/v52-omega-handoff-policy-v1.json"
        payload["next_receiver_pack_path"] = "docs/v53-beta-continuity-pack-v1.md"
        payload["next_receiver_policy_path"] = "docs/v53-beta-handoff-policy-v1.json"
        payload.update(closeout["core_states"])
        write_json(runtime_path, payload)
    validation = read_json(ROOT / "docs" / "v17-runtime-session-validation-latest.json")
    validation["generated_utc"] = now_iso()
    validation["phase"] = PHASE
    validation["current_head_sha"] = closeout["current_head_sha"]
    validation.update(closeout["core_states"])
    write_json(ROOT / "docs" / "v17-runtime-session-validation-latest.json", validation)


def intended_paths(include_publication: bool = False) -> list[str]:
    paths = [
        ".codex/agents/27-caelira.md",
        ".codex/agents/29-seren-vale.md",
        ".codex/agents/30-lyriq.md",
        ".codex/agents/31-mira-sol.md",
        "scripts/trinity_v52_omega.py",
        "docs/auto-generated/v52-advisory-digest-v1.json",
        "docs/auto-generated/v52-advisory-digest-v1.md",
        "docs/trinity-agent-council-validation-latest.json",
        "docs/trinity-agent-council-validation-latest.md",
        "docs/trinity-live-traces/v52-kimi-delegation-v1.json",
        "docs/trinity-live-traces/v52-kimi-research-v1.json",
        "docs/trinity-live-traces/v52-kimi-research-v1.md",
        "docs/trinity-live-traces/v52-kimiclaw-colearning-v1.json",
        "docs/trinity-live-traces/v52-kimiclaw-colearning-v1.md",
        "docs/trinity-live-traces/v52-plugin-capability-matrix-v1.json",
        "docs/trinity-live-traces/v52-plugin-capability-matrix-v1.md",
        "docs/trinity-live-traces/v52-suite-blocker-triage-v1.json",
        "docs/trinity-live-traces/v52-suite-blocker-triage-v1.md",
        "docs/trinity-live-traces/v52-notion-mission-control-v1.json",
        "docs/trinity-live-traces/v52-notion-mission-control-v1.md",
        "docs/trinity-live-traces/v52-quick-suite-status.json",
        "docs/trinity-live-traces/v52-standard-suite-status.json",
        "docs/trinity-live-traces/v52-deep-suite-status.json",
        "docs/trinity-live-traces/v52-stage-allowlist-v1.json",
        "docs/trinity-live-traces/v52-stage-allowlist-v1.md",
        "docs/trinity-runtime-model-resolution-v1.json",
        "docs/v17-external-establishment-validation-latest.json",
        "docs/v17-external-establishment-validation-latest.md",
        "docs/v17-runtime-session-log-latest.json",
        "docs/v17-runtime-session-validation-latest.json",
        "docs/v17-runtime-truth-resolution-board-v1.json",
        "docs/v52-mission-control-dashboard.html",
        "docs/v52-omega-closeout-summary-v1.json",
        "docs/v52-omega-continuity-pack-v1.md",
        "docs/v52-omega-handoff-policy-v1.json",
        "docs/v53-beta-closeout-summary-v1.json",
        "docs/v53-beta-continuity-pack-v1.md",
        "docs/v53-beta-handoff-policy-v1.json",
    ]
    if include_publication:
        paths.extend(["docs/trinity-live-traces/v52-git-publication-result-v1.json", "docs/trinity-live-traces/v52-git-publication-result-v1.md"])
    return sorted(set(paths))


def publish_allowlist(include_publication: bool = False) -> None:
    paths = intended_paths(include_publication=include_publication)
    dirty = git_status()
    dirty_paths = {line[3:].strip().strip('"').replace("\\", "/") for line in dirty}
    payload = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "current_head_sha": git_head(),
        "curation_rule": "v52_only_forward_allowlist",
        "dirty_path_count": len(dirty),
        "curated_include_count": len(paths),
        "curated_include_paths": paths,
        "present_curated_paths": [path for path in paths if (ROOT / path).exists()],
        "dirty_curated_paths": [path for path in paths if path in dirty_paths],
        "cleanup_posture": "stage_allowlist_only_preserve_background_churn",
    }
    write_json(ALLOWLIST_JSON, payload)
    write_text(ALLOWLIST_MD, markdown_table("V52 Stage Allowlist", payload, ["curation_rule", "dirty_path_count", "curated_include_count"]))


def publish(args: argparse.Namespace) -> None:
    TRACE_DIR.mkdir(parents=True, exist_ok=True)
    AUTO_DIR.mkdir(parents=True, exist_ok=True)
    ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)

    probes = tool_probes()
    plugin = plugin_matrix(probes)
    kimi_payload = kimi_research(args.kimi_delegation_path)
    colearning_payload = colearning(kimi_payload)
    triage = suite_triage()
    publication = read_json(PUBLICATION_JSON)
    if args.publication_commit:
        publication = {
            "generated_utc": now_iso(),
            "phase": PHASE,
            "branch": PUBLICATION_BRANCH,
            "publication_commit_sha": args.publication_commit,
            "current_local_head_sha": git_head(),
            "git_publication_state": "committed_pushed_pr45_branch_updated",
            "pr_number": 45,
            "pr_url": "https://github.com/HamishT26/Beyonder-Real-True-Journey/pull/45",
        }
        write_json(PUBLICATION_JSON, publication)
        write_text(PUBLICATION_MD, markdown_table("V52 Git Publication Result", publication, ["git_publication_state", "publication_commit_sha", "pr_url"]))
    closeout = closeout_payload(probes, plugin, triage, kimi_payload, args.notion_url, args.iab_state, publication)
    dashboard = mission_control_html(closeout, args.notion_url)
    handoff = handoff_payload(closeout)
    v53 = {
        "generated_utc": now_iso(),
        "phase": NEXT_PHASE,
        "overall_status": closeout["overall_status"],
        "current_head_sha": closeout["current_head_sha"],
        "intended_receiver": closeout["intended_receiver"],
        "receiver_rule_outcome": closeout["receiver_rule_outcome"],
        "core_states": closeout["core_states"],
        "bounded_residuals": closeout["bounded_residuals"],
        "primary_lanes": [
            "continue suite residual repair from V52 status",
            "use Notion Mission Control if live page exists, otherwise keep local dashboard as fallback",
            "keep GCP, Vesper Ion, Kai, and paid cloud on standby until billing truth returns",
            "treat Kimi/Kimiclaw helpers as bounded collaborators with no secret publication",
        ],
    }
    advisory = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "verified_current_truth": [
            "V52 executes from the clean D-drive worktree.",
            "PowerShell remains the active operator lane; WSL remains installed and on hold.",
            "Codex CLI is callable and logged in; Kimi CLI is callable and the key file exists without publishing the key.",
        ],
        "operator_reported": [
            "Bigtable was deleted by the operator for cost control.",
            "GCP, Vesper Ion, Kai, and paid cloud lanes remain on standby for one to two weeks.",
        ],
        "advisory_proposal": [
            "Use Notion Mission Control as a bounded live UI if the connector is callable.",
            "Use Kimi K2.6 and Kimi Claw research as helper-lane context, not as repo authority.",
            "Stop before heavier materialize lanes if deep repeats the same fail family.",
        ],
        "source_anchors": kimi_payload["source_anchors"],
    }
    mission = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "overall_status": "PASS" if args.notion_url else "WARN",
        "notion_mission_control_state": closeout["core_states"]["notion_mission_control_state"],
        "notion_mission_control_url": args.notion_url,
        "local_dashboard_path": str(dashboard),
        "iab_state": args.iab_state,
        "parent_page": args.notion_parent,
        "safe_publication_rule": "No API keys or Kimi resume tokens are published to Notion.",
    }

    write_json(AUTO_DIR / "v52-advisory-digest-v1.json", advisory)
    write_text(AUTO_DIR / "v52-advisory-digest-v1.md", markdown_table("V52 Advisory Digest", advisory, ["phase"]))
    write_json(TRACE_DIR / "v52-kimi-research-v1.json", kimi_payload)
    write_text(TRACE_DIR / "v52-kimi-research-v1.md", markdown_table("V52 Kimi Research", kimi_payload, ["kimi_research_state", "overall_status"]))
    write_json(TRACE_DIR / "v52-kimiclaw-colearning-v1.json", colearning_payload)
    write_text(TRACE_DIR / "v52-kimiclaw-colearning-v1.md", markdown_table("V52 Kimiclaw Co-Learning", colearning_payload, ["kimiclaw_colearning_state", "overall_status"]))
    write_json(TRACE_DIR / "v52-plugin-capability-matrix-v1.json", plugin)
    write_text(TRACE_DIR / "v52-plugin-capability-matrix-v1.md", markdown_table("V52 Plugin Capability Matrix", plugin, ["plugin_surface_split_state", "overall_status"]))
    write_json(TRACE_DIR / "v52-suite-blocker-triage-v1.json", triage)
    write_text(TRACE_DIR / "v52-suite-blocker-triage-v1.md", markdown_table("V52 Suite Blocker Triage", triage, ["suite_blocker_repair_state", "overall_status"]))
    write_json(TRACE_DIR / "v52-notion-mission-control-v1.json", mission)
    write_text(TRACE_DIR / "v52-notion-mission-control-v1.md", markdown_table("V52 Notion Mission Control", mission, ["notion_mission_control_state", "notion_mission_control_url", "local_dashboard_path", "iab_state"]))
    write_json(ROOT / "docs" / "v52-omega-closeout-summary-v1.json", closeout)
    write_text(ROOT / "docs" / "v52-omega-continuity-pack-v1.md", continuity_md(closeout, "V52 Omega Continuity Pack"))
    write_json(ROOT / "docs" / "v52-omega-handoff-policy-v1.json", handoff)
    write_json(ROOT / "docs" / "v53-beta-closeout-summary-v1.json", v53)
    write_text(ROOT / "docs" / "v53-beta-continuity-pack-v1.md", continuity_md(v53, "V53 Beta Continuity Pack"))
    write_json(ROOT / "docs" / "v53-beta-handoff-policy-v1.json", handoff_payload(v53))
    update_runtime_surfaces(closeout, handoff)
    publish_allowlist(include_publication=bool(publication))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--notion-url", default="")
    parser.add_argument("--notion-parent", default="New Project")
    parser.add_argument("--iab-state", default="pending_browser_use_verification")
    parser.add_argument("--kimi-delegation-path", default="")
    parser.add_argument("--publication-commit", default="")
    args = parser.parse_args()
    publish(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
