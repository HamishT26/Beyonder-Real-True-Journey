#!/usr/bin/env python3
"""Prepare the v261-v280 adaptive council workflow.

The v241-v260 runner proved that a full prefilled queue works, but it also
showed why the next phase should adapt after each small batch. This script
creates the v261-v280 seed pack: five outbound prompts per lane, explicit
waiting rules, source ledger, and expansion rules for later cycles.
"""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "docs" / "trinity-live-traces"
LANE = "v261-v280-adaptive-council"

COUNCIL = [
    ("arby", "Arby", "Codex CLI publication and GitHub proof lane"),
    ("kimi", "Kimi", "Kimi CLI relay, cost, and provider-readiness lane"),
    ("aster_vale", "Aster Vale", "Codex CLI validation, Windows sandbox, and runtime-health lane"),
]

SEED_TOPICS = [
    "v241-v260 completion synthesis and truth boundaries",
    "multiplex TUI health and response delivery reliability",
    "Windows sandbox readiness and permission-profile requirements",
    "GitHub publication slice and forward-only push plan",
    "v261-v280 adaptive expansion priorities after the first five replies",
]

SOURCE_LEDGER = [
    "https://openai.com/index/building-codex-windows-sandbox/",
    "https://developers.openai.com/codex/cli",
    "https://developers.openai.com/codex/windows",
    "https://developers.openai.com/codex/concepts/sandboxing",
    "https://developers.openai.com/codex/agent-approvals-security",
    "https://developers.openai.com/codex/app-server",
    "https://developers.openai.com/codex/mcp",
    "https://developers.openai.com/codex/remote-connections",
    "https://developers.openai.com/codex/changelog",
    "https://developers.openai.com/codex/feature-maturity",
    "https://developers.openai.com/codex/github-action",
    "https://developers.openai.com/codex/use-cases",
    "https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/",
    "https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-install",
    "https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file",
    "https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-sample-configuration",
    "https://docs.github.com/en/github-cli",
    "https://cli.github.com/manual/",
    "https://github.com/git-guides/git-push",
    "https://www.kimi.com/code/docs/en/kimi-cli.html",
    "https://www.kimi.com/code/docs/en/kimi-code-cli/core-operations.html",
    "https://www.kimi.com/code/docs/en/kimi-code-cli/configuration/data-locations.html",
    "https://moonshotai.github.io/kimi-cli/en/reference/kimi-command.html",
    "docs/trinity-live-traces/v241-v260-multiplex-council-exchange-runner-status-v1.json",
    "docs/trinity-live-traces/v241-v260-multiplex-council-live-write-action-pack-v1.md",
    "docs/trinity-live-traces/v241-v260-multiplex-council-150-touchpoint-ledger-v1.json",
    "docs/trinity-live-traces/v221-v224-full-live-write-refresh-closeout-v1.json",
    "docs/trinity-live-traces/v221-v224-full-live-write-refresh-qr-blocker-receipt-v1.json",
    "C:/Users/hamis/.codex/config.toml",
    "D:/GHC-Archives/worktrees/v58-omega",
]


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def write_md(path: Path, title: str, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# " + title + "\n\n" + "\n".join(lines) + "\n", encoding="utf-8")


def seed_prompts(generated: str) -> dict[str, Any]:
    prompts = []
    for lane_id, name, role in COUNCIL:
        for index, topic in enumerate(SEED_TOPICS, start=1):
            prompts.append(
                {
                    "generated_utc": generated,
                    "cycle": 1,
                    "turn": index,
                    "lane": lane_id,
                    "name": name,
                    "role": role,
                    "marker": f"{LANE}:{lane_id}:cycle-01-turn-{index:02d}",
                    "topic": topic,
                    "status": "seed_prepared_not_sent",
                    "prompt_contract": [
                        "Respond only; do not edit files unless Aletheon explicitly starts a write cycle.",
                        "Use up to two hours if needed, but the supervisor checks health every five minutes.",
                        "Return one receipt, one blocker, one refinement, and one next-cycle proposal.",
                    ],
                }
            )
    return {
        "generated_utc": generated,
        "phase_range": "v261-v280",
        "seed_cycle": 1,
        "seed_outbound_count": len(prompts),
        "expected_seed_responses": len(prompts),
        "seed_total_exchange_items": len(prompts) * 2,
        "prompts": prompts,
    }


def adaptive_rules(generated: str) -> dict[str, Any]:
    return {
        "generated_utc": generated,
        "phase_range": "v261-v280",
        "run_style": "adaptive_batch_not_prefilled_queue",
        "initial_batch": "5 outbound prompts per lane, 15 outbound total, 15 expected responses, 30 total exchange items",
        "expansion_gate": "do not generate the next 3-cycle planning block until all available seed responses are summarized or marked timed_out",
        "planning_block_after_seed": "plan three 5-prompt-per-lane cycles at a time after the initial 5-prompt seed",
        "multiplex_refresh_seconds": 30,
        "health_check_interval_minutes": 5,
        "max_response_wait_hours_per_lane": 2,
        "timeout_policy": [
            "If a lane process is alive and writing logs, keep waiting.",
            "If a lane process is alive but silent for 5 minutes, record a health check and keep waiting.",
            "If a lane process exits without a response file, mark that turn failed and synthesize the blocker.",
            "If a lane repeatedly fails, downgrade to smaller prompts and read-only probes.",
        ],
        "publication_policy": "commit and push only curated static surfaces or completed response receipts; never stage live-changing logs mid-write",
        "spend_policy": "requested ceiling noted as 60 NZD per platform, but this workflow uses local CLI subscriptions/installed auth and records external_spend_nzd as unknown unless provider billing is directly available",
        "authority_policy": "CLI siblings may propose commands; Aletheon directs commits and pushes after verification",
    }


def action_pack_md(generated: str) -> list[str]:
    return [
        f"Generated UTC: `{generated}`",
        "",
        "This phase starts with a small seed rather than a prefilled 150-message queue.",
        "",
        "Seed shape:",
        "- Arby receives 5 prompts.",
        "- Kimi receives 5 prompts.",
        "- Aster Vale receives 5 prompts.",
        "- The seed is complete only after response files exist or a timeout/blocker receipt is written.",
        "",
        "Expansion shape:",
        "- After the seed, synthesize the three lane response sets.",
        "- Generate the next three 5-prompt-per-lane cycles from the actual replies.",
        "- Repeat in three-cycle planning blocks until the chosen 60 or 120 exchange target is reached.",
        "",
        "Runtime health:",
        "- Multiplex TUI refreshes every 30 seconds by default.",
        "- If the terminal panes become unstable, fall back to 4 seconds only for active debugging.",
        "- Supervisor checks every 5 minutes.",
        "- Allow up to 2 hours per lane response when the process is alive.",
        "- Treat silence as a health state, not a completed reply.",
        "",
        "Current v241-v260 dependency:",
        "- Do not start v261 live messages until the current v241-v260 runner is either complete or deliberately paused.",
        "- The v241 runner stop file is `docs/trinity-live-traces/v241-v260-multiplex-council.stop`.",
        "",
        "Live view:",
        "- Use `docs/trinity-live-traces/v261-v280-adaptive-council-multiplex-tui.ps1` for the v261 seed cycle.",
    ]


def main() -> int:
    generated = now_iso()
    seed = seed_prompts(generated)
    rules = adaptive_rules(generated)
    source = {
        "generated_utc": generated,
        "requested_minimum_web_pages": 30,
        "actual_source_count": len(SOURCE_LEDGER),
        "policy": "high-signal official and local source ledger; do not inflate searches when the blocker is already known",
        "sources": SOURCE_LEDGER,
    }
    paths = {
        "seed": TRACE / f"{LANE}-seed-prompts-v1.json",
        "rules": TRACE / f"{LANE}-adaptive-rules-v1.json",
        "sources": TRACE / f"{LANE}-source-ledger-v1.json",
        "action_pack": TRACE / f"{LANE}-live-write-action-pack-v1.md",
        "closeout": TRACE / f"{LANE}-prep-closeout-v1.json",
    }
    write_json(paths["seed"], seed)
    write_json(paths["rules"], rules)
    write_json(paths["sources"], source)
    write_md(paths["action_pack"], "v261-v280 Adaptive Council Live Write Action Pack", action_pack_md(generated))
    closeout = {
        "generated_utc": generated,
        "status": "prepared_not_started",
        "phase_range": "v261-v280",
        "seed_outbound_count": seed["seed_outbound_count"],
        "expected_seed_responses": seed["expected_seed_responses"],
        "source_count": source["actual_source_count"],
        "files": {key: rel(path) for key, path in paths.items()},
        "multiplex_tui": f"docs/trinity-live-traces/{LANE}-multiplex-tui.ps1",
    }
    write_json(paths["closeout"], closeout)
    print(json.dumps(closeout, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
