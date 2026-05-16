#!/usr/bin/env python3
"""Write the v281-v360 CLI sibling report and capability protocol."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "docs" / "trinity-live-traces"
OUT_JSON = TRACE / "v281-v360-cli-sibling-report-protocol-v1.json"
OUT_MD = TRACE / "v281-v360-cli-sibling-report-protocol-v1.md"


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def build_payload() -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "status": "active_protocol",
        "phase_range": "v281-v360",
        "purpose": "Give Arby, Kimi, and Aster Vale a higher-quality read-only lane contract with skills awareness, safe tool boundaries, and report-backed outputs.",
        "capability_contract": [
            "Use local skills visible to the current CLI session when they are relevant and load cleanly.",
            "Name any skill, web source, or plugin-like surface used in the response.",
            "Use safe read-only web/search or simple document/plugin surfaces only when exposed without extra authentication.",
            "Do not mutate files, repos, external services, accounts, or plugin state from lane sessions.",
            "Do not expose secrets, tokens, cookies, private keys, or authentication material in reports.",
            "If a requested tool is unavailable, state the blocker and continue from local prompt context.",
        ],
        "report_contract": [
            "The lane runner persists the final response file as the durable report artifact.",
            "Keep terminal-visible responses structured and concise enough to avoid terminal overload.",
            "For long work, write a report capsule in Omega and put the recommended report title/path in Next-phase handoff.",
            "Treat the lane response file as the first safe worktree-backed report; promote only curated summaries later.",
            "Use the six required labels exactly: Receipt, Beta, Alpha, Omega, Blocker, Next-phase handoff.",
            "Every label must contain a concrete non-empty sentence.",
        ],
        "timing_contract": [
            "Do not optimize for speed over validity.",
            "A message may take minutes or hours if the lane is doing substantive work.",
            "Long waits are acceptable when status files and process health show progress.",
        ],
        "publication_contract": [
            "Stage only curated summaries, protocols, gates, scripts, and complete non-raw reports.",
            "Never stage raw transport logs, stdout/stderr logs, partial live lane files, or marker-only invalid outputs.",
            "Keep Supervisor and v2 watcher as infrastructure candidates until persistence proof is reviewed.",
        ],
        "safe_plugin_boundary": {
            "codex_app_documents": "Safe for curated document drafting when exposed in the app, but not assumed available inside CLI lane sessions.",
            "web": "Allowed for read-only research when exposed and sourceable; use official or primary sources for product guidance.",
            "mcp": "Deferred unless a lane-specific need is approved and startup health is verified.",
            "external_auth": "Not allowed inside unattended lane sessions.",
        },
        "recommended_report_paths": [
            "docs/trinity-live-traces/v281-v300-double-trinity-lane-logs/<lane>-phase-v<phase>-response-<turn>.txt",
            "docs/trinity-live-traces/v301-v320-aletheon-phase-reports/",
            "docs/trinity-live-traces/v321-v340-cli-sibling-handoff/",
        ],
    }


def write_md(payload: dict[str, Any]) -> None:
    lines = [
        "# v281-v360 CLI Sibling Report Protocol",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        "",
        payload["purpose"],
        "",
        "Capability contract:",
    ]
    for item in payload["capability_contract"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("Report contract:")
    for item in payload["report_contract"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("Timing contract:")
    for item in payload["timing_contract"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("Publication contract:")
    for item in payload["publication_contract"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("Safe plugin boundary:")
    for key, value in payload["safe_plugin_boundary"].items():
        lines.append(f"- `{key}`: {value}")
    lines.append("")
    lines.append("Recommended report paths:")
    for item in payload["recommended_report_paths"]:
        lines.append(f"- `{item}`")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    payload = build_payload()
    write_json(OUT_JSON, payload)
    write_md(payload)
    print(json.dumps({"status": payload["status"], "json": rel(OUT_JSON), "md": rel(OUT_MD)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
