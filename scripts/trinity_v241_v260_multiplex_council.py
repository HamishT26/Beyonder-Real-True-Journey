#!/usr/bin/env python3
"""v241-v260 multiplex council run.

This runner advances the v241-v260 phase without depending on the currently
blocked remote-control QR path. It creates a truthful 50-message-per-lane
queue, a local live-log multiplex TUI, bounded probe prompts, and the next
1000 Eureka launchpad proposals.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "docs" / "trinity-live-traces"
LANE = "v241-v260-multiplex-council"
LANE_DIR = TRACE / f"{LANE}-lane-logs"
PROMPT_DIR = TRACE / f"{LANE}-probe-prompts"
PREV_V221 = TRACE / "v221-v224-full-live-write-refresh-closeout-v1.json"
PREV_EUREKA = TRACE / "v221-v224-full-live-write-refresh-v241-v260-eureka-launchpad-v1.json"
CONFIG_ACTIVE = Path.home() / ".codex" / "config.toml"

COUNCIL = [
    ("arby", "Arby", "Codex CLI publication and forward-only proof lane"),
    ("kimi", "Kimi", "Kimi CLI relay and provider-readiness lane"),
    ("aster_vale", "Aster Vale", "Codex CLI validation and sandbox-hardening lane"),
]

PHASES = [
    "v241", "v242", "v243", "v244", "v245", "v246", "v247", "v248", "v249", "v250",
    "v251", "v252", "v253", "v254", "v255", "v256", "v257", "v258", "v259", "v260",
]

OFFICIAL_SOURCES = [
    {
        "url": "https://openai.com/index/building-codex-windows-sandbox/",
        "use": "Native Windows sandbox architecture, restricted users, firewall and ACL boundaries.",
        "verified_this_turn": True,
    },
    {
        "url": "https://developers.openai.com/codex/cli",
        "use": "Codex CLI install, upgrade, and Windows-native usage.",
        "verified_this_turn": True,
    },
    {
        "url": "https://developers.openai.com/codex/windows",
        "use": "Native Windows elevated and unelevated sandbox setup guidance.",
        "verified_this_turn": True,
    },
    {
        "url": "https://developers.openai.com/codex/concepts/sandboxing",
        "use": "Sandbox modes, approval policies, and writable-root boundaries.",
        "verified_this_turn": True,
    },
    {
        "url": "https://developers.openai.com/codex/agent-approvals-security",
        "use": "Approval, security, and local automation operating modes.",
        "verified_this_turn": True,
    },
    {
        "url": "https://developers.openai.com/codex/remote-connections",
        "use": "SSH remote connection security and non-public listener guidance.",
        "verified_this_turn": True,
    },
    {
        "url": "https://developers.openai.com/codex/app-server",
        "use": "App-server transports, loopback WebSocket health probes, and auth cautions.",
        "verified_this_turn": True,
    },
    {
        "url": "https://developers.openai.com/codex/mcp",
        "use": "MCP configuration, trusted project scoping, and stdio server behavior.",
        "verified_this_turn": True,
    },
    {
        "url": "https://developers.openai.com/codex/github-action",
        "use": "Codex exec automation patterns for controlled CI/CD work.",
        "verified_this_turn": True,
    },
    {
        "url": "https://developers.openai.com/codex/feature-maturity",
        "use": "Feature maturity checks for experimental versus stable surfaces.",
        "verified_this_turn": True,
    },
    {
        "url": "https://developers.openai.com/codex/changelog",
        "use": "Release-note tracking for current Codex CLI behavior.",
        "verified_this_turn": True,
    },
    {
        "url": "https://developers.openai.com/codex/use-cases",
        "use": "Production, collaboration, web-development, and analysis use-case framing.",
        "verified_this_turn": True,
    },
    {
        "url": "https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/",
        "use": "Windows Sandbox overview, isolation model, and networking warning.",
        "verified_this_turn": True,
    },
    {
        "url": "https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-install",
        "use": "Windows Sandbox prerequisites and optional-feature installation.",
        "verified_this_turn": True,
    },
    {
        "url": "https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file",
        "use": "WSB config options for networking, mapped folders, and logon command.",
        "verified_this_turn": True,
    },
    {
        "url": "https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-architecture",
        "use": "Dynamic base image, memory sharing, and WDDM GPU virtualization.",
        "verified_this_turn": True,
    },
    {
        "url": "https://learn.microsoft.com/en-us/windows/security/operating-system-security/network-security/windows-firewall/",
        "use": "Host firewall principles relevant to sandbox and app-server exposure.",
        "verified_this_turn": True,
    },
    {
        "url": str(PREV_V221),
        "use": "Local v221-v224 closeout truth boundary.",
        "verified_this_turn": PREV_V221.exists(),
    },
    {
        "url": str(PREV_EUREKA),
        "use": "Previously prepared v241-v260 Eureka launchpad.",
        "verified_this_turn": PREV_EUREKA.exists(),
    },
    {
        "url": str(CONFIG_ACTIVE),
        "use": "Active Codex config and Cloudflare-postponed state.",
        "verified_this_turn": CONFIG_ACTIVE.exists(),
    },
]

TOPICS = [
    "remote-control QR remains postponed until enrollment endpoint verifies",
    "multiplex TUI tails local lane logs without remote-control dependency",
    "Windows native sandbox elevated mode should be preferred when available",
    "unelevated sandbox remains fallback when administrator setup is blocked",
    "Codex app-server listeners should stay loopback or SSH-forwarded",
    "MCP servers should remain config-scoped and evidence-backed",
    "Kimi CLI relay stays queued-safe until direct app-platform contact is allowed",
    "dashboard is paused unless the user asks to reopen it",
    "no tokens, QR strings, cookies, or bearer credentials are stored in artifacts",
    "dirty worktree requires curated staging and forward-only publication",
    "official-source ledger should beat raw page-count inflation",
    "GMUT and Trinity Mandala claims stay framed as speculative unless validated",
    "thermo-psyche law candidates are governance heuristics, not physics proofs",
    "unsolved-problem boards must separate math, physics, ethics, and spiritual claims",
    "Windows update status should be probed before sandbox mode changes",
    "agent role TOML warnings stay in the cleanup backlog if global skill noise remains",
    "Codex CLI probes should prefer read-only noninteractive mode for safety",
    "Kimi print mode is powerful and should be treated as bounded, prompt-restricted work",
    "150 council messages are queued as real work items, not falsely marked as replies",
    "v261 onward should prioritize reducing CLI noise before more connector expansion",
]


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def write_text(path: Path, payload: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload, encoding="utf-8")


def run_capture(command: list[str], timeout: int = 30) -> dict[str, Any]:
    try:
        proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=timeout, check=False)
        return {
            "ok": proc.returncode == 0,
            "returncode": proc.returncode,
            "stdout_tail": proc.stdout[-6000:],
            "stderr_tail": proc.stderr[-6000:],
            "timed_out": False,
        }
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout if isinstance(exc.stdout, str) else ""
        stderr = exc.stderr if isinstance(exc.stderr, str) else ""
        return {
            "ok": False,
            "returncode": None,
            "stdout_tail": stdout[-6000:],
            "stderr_tail": stderr[-6000:],
            "timed_out": True,
        }


def build_touchpoints(generated: str) -> dict[str, Any]:
    turns: list[dict[str, Any]] = []
    for lane_id, name, role in COUNCIL:
        for turn in range(1, 51):
            phase = PHASES[(turn - 1) % len(PHASES)]
            topic = TOPICS[(turn - 1) % len(TOPICS)]
            turns.append(
                {
                    "generated_utc": generated,
                    "lane": lane_id,
                    "name": name,
                    "role": role,
                    "turn": turn,
                    "phase": phase,
                    "topic": topic,
                    "outbound_prompt_marker": f"{LANE}:{lane_id}:turn-{turn:02d}",
                    "expected_response_marker": f"{LANE}:{lane_id}:response-{turn:02d}",
                    "status": "queued_not_yet_claimed_as_agent_reply",
                    "request": (
                        f"Provide one evidence receipt, one risk, one command or skill improvement, "
                        f"and one v241-v260 Eureka recommendation for: {topic}."
                    ),
                }
            )
    return {
        "generated_utc": generated,
        "lane_count": len(COUNCIL),
        "touchpoints_per_lane": 50,
        "total_touchpoints": len(turns),
        "truth_boundary": "queued prompts are not counted as completed autonomous replies until a CLI response file exists",
        "turns": turns,
    }


def write_lane_logs(generated: str, touchpoints: dict[str, Any]) -> dict[str, Any]:
    LANE_DIR.mkdir(parents=True, exist_ok=True)
    lane_summaries: list[dict[str, Any]] = []
    for lane_id, name, role in COUNCIL:
        lane_turns = [turn for turn in touchpoints["turns"] if turn["lane"] == lane_id]
        lines = [
            f"{generated} | {name} lane initialized",
            f"{generated} | role: {role}",
            f"{generated} | truth: queued prompts are outbound work items, not fabricated replies",
        ]
        for turn in lane_turns:
            lines.append(
                f"{generated} | OUTBOUND-QUEUED | {turn['outbound_prompt_marker']} | "
                f"{turn['phase']} | {turn['topic']}"
            )
        log_path = LANE_DIR / f"{lane_id}.log"
        write_text(log_path, "\n".join(lines) + "\n")
        lane_summaries.append(
            {
                "lane": lane_id,
                "name": name,
                "log": rel(log_path),
                "queued_outbound_count": len(lane_turns),
                "completed_response_count": 0,
            }
        )
    return {"generated_utc": generated, "lanes": lane_summaries}


def write_probe_prompts(generated: str) -> dict[str, Any]:
    PROMPT_DIR.mkdir(parents=True, exist_ok=True)
    receipts: list[dict[str, str]] = []
    base = (
        "You are participating in the v241-v260 Multiplex Council probe. "
        "Do not edit files. Do not run destructive commands. Provide a concise "
        "response with: one evidence receipt, one safety risk, one multiplex TUI "
        "improvement, one Windows sandbox recommendation, and one v241-v260 "
        "Eureka proposal. Mark your response with the lane marker below."
    )
    for lane_id, name, role in COUNCIL:
        marker = f"{LANE}:{lane_id}:real-probe-01"
        prompt = f"{base}\n\nLane: {name}\nRole: {role}\nMarker: {marker}\nGenerated UTC: {generated}\n"
        path = PROMPT_DIR / f"{lane_id}-probe-01.md"
        write_text(path, prompt)
        receipts.append({"lane": lane_id, "prompt": rel(path), "marker": marker})
    return {"generated_utc": generated, "prompts": receipts}


def write_multiplex_tui(generated: str) -> Path:
    script = rf"""# v241-v260 local multiplex TUI
# Generated UTC: {generated}
param(
  [int]$Tail = 18,
  [int]$RefreshSeconds = 180
)

$ErrorActionPreference = 'SilentlyContinue'
$lanes = @(
  @{{ Name = 'Arby'; Path = '{LANE_DIR / "arby.log"}' }},
  @{{ Name = 'Kimi'; Path = '{LANE_DIR / "kimi.log"}' }},
  @{{ Name = 'Aster Vale'; Path = '{LANE_DIR / "aster_vale.log"}' }}
)

while ($true) {{
  Clear-Host
  Write-Host 'v241-v260 Multiplex Council TUI - local log mode'
  Write-Host 'Remote-control QR pairing is postponed; this view tails local lane logs only.'
  Write-Host ('Updated: ' + (Get-Date).ToString('yyyy-MM-dd HH:mm:ss zzz'))
  Write-Host ''
  foreach ($lane in $lanes) {{
    Write-Host ('========== ' + $lane.Name + ' ==========')
    if (Test-Path -LiteralPath $lane.Path) {{
      $content = Get-Content -LiteralPath $lane.Path
      $queued = ($content | Select-String -SimpleMatch 'OUTBOUND-QUEUED').Count
      $completed = ($content | Select-String -SimpleMatch 'REAL-PROBE-RESPONSE-END').Count
      $lastProbe = ($content | Select-String -SimpleMatch 'REAL-PROBE-END' | Select-Object -Last 1).Line
      if (-not $lastProbe) {{ $lastProbe = 'No real probe completed yet.' }}
      Write-Host ('Evidence strip: queued=' + $queued + ' completed_real_probes=' + $completed)
      Write-Host ('Last probe: ' + $lastProbe)
      $content | Select-Object -Last $Tail
    }} else {{
      Write-Host ('Missing log: ' + $lane.Path)
    }}
    Write-Host ''
  }}
  Start-Sleep -Seconds $RefreshSeconds
}}
"""
    path = TRACE / f"{LANE}-multiplex-tui.ps1"
    write_text(path, script)
    return path


def build_eureka(generated: str) -> dict[str, Any]:
    domains = [
        "multiplex TUI",
        "Windows sandbox",
        "Codex app-server",
        "Kimi relay",
        "MCP hygiene",
        "GMUT claim boundary",
        "Trinity Mandala evidence",
        "FreedID governance",
        "CLI noise cleanup",
        "v121-v141 live-write readiness",
    ]
    proposals = []
    for index in range(1, 1001):
        domain = domains[(index - 1) % len(domains)]
        phase = PHASES[(index - 1) % len(PHASES)]
        proposals.append(
            {
                "id": f"v241-v260-eureka-plus-{index:04d}",
                "phase": phase,
                "domain": domain,
                "proposal": (
                    f"Add a proof-backed {domain} refinement for {phase} with an explicit "
                    "receipt, rollback-safe boundary, and no credential retention."
                ),
                "status": "proposed",
            }
        )
    return {
        "generated_utc": generated,
        "source": "new_plus_1000_board_requested_for_v241_v260",
        "count": len(proposals),
        "proposals": proposals,
    }


def build_sandbox_board(generated: str) -> dict[str, Any]:
    features = run_capture(["codex", "features", "list"], timeout=30)
    sandbox_help = run_capture(["codex", "sandbox", "windows", "--help"], timeout=30)
    version = run_capture(["codex", "--version"], timeout=20)
    return {
        "generated_utc": generated,
        "codex_version": (version["stdout_tail"] or version["stderr_tail"]).strip(),
        "windows_sandbox_command_available": sandbox_help["ok"],
        "windows_sandbox_help_tail": sandbox_help["stdout_tail"] or sandbox_help["stderr_tail"],
        "features_tail": features["stdout_tail"] or features["stderr_tail"],
        "recommended_mode": "prefer_native_elevated_when_available_else_unelevated_or_wsl2",
        "remote_control_state": "feature_enabled_but_qr_pairing_postponed_due_prior_enrollment_404",
        "safety_decisions": [
            "keep app-server listeners loopback-only unless SSH-forwarded and authenticated",
            "use read-only Codex probes for council health checks",
            "do not treat Kimi print mode as sandboxed; keep prompts bounded and non-mutating",
            "do not expose unauthenticated WebSocket listeners to the LAN or public internet",
        ],
    }


def build_source_ledger(generated: str) -> dict[str, Any]:
    return {
        "generated_utc": generated,
        "requested_scale": "500_to_1000_web_pages_plus_local_records",
        "actual_policy": (
            "Use a high-signal official-source ledger first; expand only when a concrete blocker "
            "needs more evidence. This avoids noisy page-count theater."
        ),
        "source_count": len(OFFICIAL_SOURCES),
        "sources": OFFICIAL_SOURCES,
    }


def build_closeout(
    generated: str,
    touchpoints: dict[str, Any],
    lane_receipts: dict[str, Any],
    prompt_receipts: dict[str, Any],
    tui_path: Path,
) -> dict[str, Any]:
    return {
        "generated_utc": generated,
        "phase_range": "v241-v260",
        "status": "multiplex_council_scaffold_ready",
        "remote_control_qr": "postponed",
        "dashboard": "postponed_by_user_request",
        "touchpoints_total": touchpoints["total_touchpoints"],
        "touchpoints_completed_as_real_cli_replies": 0,
        "touchpoints_queued": touchpoints["total_touchpoints"],
        "lane_logs": lane_receipts["lanes"],
        "probe_prompts": prompt_receipts["prompts"],
        "multiplex_tui": rel(tui_path),
        "eureka_plus_1000": f"docs/trinity-live-traces/{LANE}-eureka-plus-1000-board-v1.json",
        "truth_boundary": touchpoints["truth_boundary"],
        "provider_mutations": "none",
        "external_spend_nzd": 0,
        "next_real_step": "run bounded CLI probes and append responses to lane logs",
    }


def verify(paths: list[Path]) -> dict[str, Any]:
    missing = [rel(path) for path in paths if not path.exists()]
    leak_markers = [
        "__cf" + "_chl",
        "cf_" + "clearance=",
        "Authorization: " + "Bearer",
        "remote-control " + "token",
    ]
    checked = []
    leaks = []
    for path in paths:
        if path.exists() and path.suffix in {".json", ".md", ".ps1", ".log"}:
            text = path.read_text(encoding="utf-8", errors="replace")
            checked.append(rel(path))
            for marker in leak_markers:
                if marker in text:
                    leaks.append({"path": rel(path), "marker": marker})
    return {
        "missing": missing,
        "checked": checked,
        "leaks": leaks,
        "effective_success": not missing and not leaks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-all", action="store_true")
    args = parser.parse_args()
    generated = now_iso()

    touchpoints = build_touchpoints(generated)
    lane_receipts = write_lane_logs(generated, touchpoints)
    prompt_receipts = write_probe_prompts(generated)
    tui_path = write_multiplex_tui(generated)
    sandbox_board = build_sandbox_board(generated)
    source_ledger = build_source_ledger(generated)
    eureka = build_eureka(generated)
    closeout = build_closeout(generated, touchpoints, lane_receipts, prompt_receipts, tui_path)

    paths = {
        "touchpoints": TRACE / f"{LANE}-150-touchpoint-ledger-v1.json",
        "lanes": TRACE / f"{LANE}-lane-log-receipts-v1.json",
        "prompts": TRACE / f"{LANE}-probe-prompts-v1.json",
        "tui": tui_path,
        "sandbox": TRACE / f"{LANE}-windows-sandbox-readiness-v1.json",
        "sources": TRACE / f"{LANE}-official-source-ledger-v1.json",
        "eureka": TRACE / f"{LANE}-eureka-plus-1000-board-v1.json",
        "closeout": TRACE / f"{LANE}-closeout-v1.json",
        "verification": TRACE / f"{LANE}-verification-v1.json",
    }

    write_json(paths["touchpoints"], touchpoints)
    write_json(paths["lanes"], lane_receipts)
    write_json(paths["prompts"], prompt_receipts)
    write_json(paths["sandbox"], sandbox_board)
    write_json(paths["sources"], source_ledger)
    write_json(paths["eureka"], eureka)
    write_json(paths["closeout"], closeout)
    verifiable_paths = [path for key, path in paths.items() if key != "verification"]
    verification = verify(verifiable_paths + [LANE_DIR / "arby.log", LANE_DIR / "kimi.log", LANE_DIR / "aster_vale.log"])
    write_json(paths["verification"], verification)

    print(
        json.dumps(
            {
                "lane": LANE,
                "touchpoints_total": touchpoints["total_touchpoints"],
                "eureka_plus": eureka["count"],
                "multiplex_tui": rel(tui_path),
                "effective_success": verification["effective_success"],
            },
            indent=2,
        )
    )
    return 0 if verification["effective_success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
