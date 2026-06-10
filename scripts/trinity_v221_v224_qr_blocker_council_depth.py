#!/usr/bin/env python3
"""Record the v221-v224 QR blocker and deepen council lane receipts."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "docs" / "trinity-live-traces"
LANE = "v221-v224-full-live-write-refresh"
LANE_LOGS = TRACE / f"{LANE}-lane-logs"
ASTERR = LANE_LOGS / "aster-vale-codex-consultation.txt"
KIMI_INFO = LANE_LOGS / "kimi-cli-info.txt"
ARBY_RECEIPT = LANE_LOGS / "arby-codex-consultation.txt"
CLOSEOUT = TRACE / f"{LANE}-closeout-v1.json"
REMOTE = TRACE / f"{LANE}-remote-control-retry-receipt-v1.json"
VERIFICATION = TRACE / f"{LANE}-artifact-verification-v1.json"


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_md(path: Path, title: str, lines: list[str]) -> None:
    path.write_text("# " + title + "\n\n" + "\n".join(lines) + "\n", encoding="utf-8")


def text_head(path: Path, limit: int = 1800) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")[:limit]


def build_touchpoint_plan(generated: str) -> dict[str, Any]:
    lanes = [
        ("arby", "Arby", "publication receipts, allowlist truth, forward-only release risk"),
        ("kimi", "Kimi", "Kimi/Kimicode CLI relay prep, provider readiness, Lumina artifact boundary"),
        ("aster_vale", "Aster Vale", "validation, sandbox safety, remote-control/multiplex hardening"),
    ]
    turns = []
    topics = [
        "remote-control blocker truth",
        "multiplex stdout visibility",
        "Cloudflare postponed state",
        "Codex Windows sandbox implications",
        "official source ledger extraction",
        "GMUT claim-boundary hygiene",
        "Thermo/Psyche law candidate board",
        "unsolved-problem crosswalk",
        "operator_hold provider matrix",
        "v121-v141 live-write readiness",
        "dashboard marker integrity",
        "lane-log freshness",
        "secret/token non-retention",
        "forward-only publication",
        "skill-loader cleanup backlog",
        "agent-role schema cleanup",
        "Kimi relay packet design",
        "Aster verification recommendations",
        "Arby allowlist recommendations",
        "v241-v260 launchpad priorities",
    ]
    for lane_id, name, role in lanes:
        for index, topic in enumerate(topics, start=1):
            turns.append(
                {
                    "generated_utc": generated,
                    "lane": lane_id,
                    "name": name,
                    "turn": index,
                    "topic": topic,
                    "instruction": (
                        f"{name} should provide one evidence receipt, one risk, and one "
                        f"v241-v260 recommendation for {topic}; role focus: {role}."
                    ),
                    "status": "planned_or_file_backed",
                }
            )
    return {
        "generated_utc": generated,
        "touchpoints_per_lane": 20,
        "lane_count": len(lanes),
        "total_touchpoints": len(turns),
        "execution_policy": "file_backed_council_depth_until_remote_control_is_unblocked",
        "turns": turns,
    }


def main() -> int:
    generated = now_iso()
    remote = read_json(REMOTE, {})
    closeout = read_json(CLOSEOUT, {})
    verification = read_json(VERIFICATION, {})
    blocker = {
        "generated_utc": generated,
        "status": "remote_control_qr_postponed",
        "operator_observation": "Screenshots showed malformed agent role TOML warnings, plugin sync Cloudflare challenge text, and remote-control enrollment 404 responses.",
        "actions_taken": [
            "stopped the supervised remote-control process started for this probe",
            "replaced active C:/Users/hamis/.codex/config.toml MCP section from cleaned project config",
            "removed Cloudflare plugin and MCP references from active config",
            "normalized malformed Windows paths in duplicate role TOML files",
            "preserved canonical Markdown role files and disabled duplicate malformed TOML files",
        ],
        "remaining_blockers": [
            "remote-control server enrollment returns HTTP 404 from chatgpt.com remote-control endpoint",
            "featured plugin cache refresh still hits a Cloudflare/JavaScript challenge outside local control",
            "some global skills still need YAML frontmatter repair, but they do not block the local dashboard",
            "a visible window launch is not proof of a successful phone pairing handshake",
        ],
        "decision": "postpone QR pairing and continue through dashboard plus multiplex stdout lane logs",
        "token_policy": "no_qr_or_pairing_token_stored",
        "remote_receipt_before_update": remote,
    }
    council = build_touchpoint_plan(generated)
    synthesis = {
        "generated_utc": generated,
        "arby": {
            "status": "consultation_timed_out_or_missing",
            "receipt": rel(ARBY_RECEIPT) if ARBY_RECEIPT.exists() else None,
            "next": "use file-backed Arby touchpoints until CLI noise is reduced",
        },
        "kimi": {
            "status": "kimi_info_empty_or_timed_out",
            "receipt": rel(KIMI_INFO) if KIMI_INFO.exists() else None,
            "next": "keep Kimi relay prep as queued-safe and non-yolo",
        },
        "aster_vale": {
            "status": "read_only_codex_consultation_completed",
            "receipt": rel(ASTERR) if ASTERR.exists() else None,
            "high_signal_excerpt": text_head(ASTERR),
        },
    }

    closeout.update(
        {
            "remote_control_supervised_launch_state": "qr_pairing_postponed_blocked_by_remote_enrollment_404",
            "qr_pairing_status": "postponed",
            "council_depth_policy": "20_touchpoints_per_lane_file_backed_until_qr_unblocked",
            "council_depth_touchpoints": council["total_touchpoints"],
            "remote_control_blocker_receipt": f"docs/trinity-live-traces/{LANE}-qr-blocker-receipt-v1.json",
            "effective_success": bool(verification.get("effective_success", closeout.get("effective_success", False))),
        }
    )
    verification.update(
        {
            "remote_control_pairing_verified": False,
            "remote_control_pairing_status": "postponed_blocked_by_remote_enrollment_404",
            "council_depth_touchpoint_plan_present": True,
        }
    )

    write_json(TRACE / f"{LANE}-qr-blocker-receipt-v1.json", blocker)
    write_json(TRACE / f"{LANE}-council-depth-touchpoint-plan-v1.json", council)
    write_json(TRACE / f"{LANE}-cli-consultation-synthesis-v1.json", synthesis)
    write_json(CLOSEOUT, closeout)
    write_json(VERIFICATION, verification)
    write_md(
        TRACE / f"{LANE}-qr-blocker-receipt-v1.md",
        "v221-v224 QR Blocker Receipt",
        [
            "- QR pairing status: `postponed`",
            "- Main blocker: remote-control enrollment returns `HTTP 404 Not Found`.",
            "- Local fix completed: duplicate malformed `.toml` role files disabled; canonical `.md` role files preserved.",
            "- Cloudflare state: removed/postponed in active Codex config.",
            "- Continue today through the dashboard and multiplex stdout lanes.",
        ],
    )
    write_md(
        TRACE / f"{LANE}-council-depth-touchpoint-plan-v1.md",
        "Council Depth Touchpoint Plan",
        [
            "- Arby: 20 file-backed touchpoints focused on publication and allowlist truth.",
            "- Kimi: 20 file-backed touchpoints focused on Kimi CLI relay readiness and Lumina boundaries.",
            "- Aster Vale: 20 file-backed touchpoints focused on validation and remote-control hardening.",
            "- External spend: `0 NZD`.",
            "- Provider mutations: `none`.",
        ],
    )
    print(json.dumps({"blocker": blocker["status"], "touchpoints": council["total_touchpoints"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
