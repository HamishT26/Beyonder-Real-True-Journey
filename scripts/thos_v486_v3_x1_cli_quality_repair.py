#!/usr/bin/env python3
"""Repair v486 v3 x1 receipts when CLI lanes return handshake stubs."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
PHASE = "v486-gmut-thos-v22-v3-x1"


def now_pair() -> tuple[str, str]:
    utc = dt.datetime.now(dt.UTC).replace(microsecond=0)
    nz = utc.astimezone(dt.timezone(dt.timedelta(hours=12), name="NZST"))
    return utc.isoformat().replace("+00:00", "Z"), nz.isoformat()


def load_json(name: str) -> dict[str, Any]:
    path = TRACE_DIR / name
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def save_json(name: str, payload: dict[str, Any]) -> None:
    (TRACE_DIR / name).write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def save_md(name: str, title: str, bullets: list[str]) -> None:
    lines = [f"# {title}", ""]
    lines.extend(f"- {item}" for item in bullets)
    (TRACE_DIR / name).write_text("\n".join(lines) + "\n", encoding="utf-8")


def lane_name(raw: str) -> str:
    return "Aster Vale" if raw == "AsterVale" else raw


def main() -> int:
    generated_utc, generated_nz = now_pair()
    cli_name = f"{PHASE}-cli-completion-v1.json"
    timing_name = f"{PHASE}-five-lane-timing-v1.json"
    multiplex_name = f"{PHASE}-local-multiplex-tui-app-server-runner-v1.json"
    synthesis_name = f"{PHASE}-synthesis-v1.json"

    cli = load_json(cli_name)
    timing = load_json(timing_name)
    multiplex = load_json(multiplex_name)
    synthesis = load_json(synthesis_name)

    cli_lanes = cli.get("lanes", [])
    quality_lanes: list[dict[str, Any]] = []
    for item in cli_lanes:
        quality_lanes.append(
            {
                "lane": lane_name(str(item.get("lane", ""))),
                "raw_completion_status": item.get("completion_status"),
                "final_message_bytes": item.get("final_message_bytes"),
                "final_message_hash": item.get("final_message_hash"),
                "quality_status": "HANDSHAKE_STUB_NOT_X1_ADVISORY",
                "body_text_published": False,
            }
        )
        item["advisory_quality_status"] = "HANDSHAKE_STUB_NOT_X1_ADVISORY"
        item["completion_status"] = "OPEN_GAP_HANDSHAKE_STUB_RETRY_PENDING"

    cli["aggregate_status"] = "OPEN_GAP_CLI_ADVISORY_STUB_RETRY_PENDING"
    cli["quality_gate"] = {
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "reason": "CLI final-message files contained handshake acknowledgements rather than the requested v3 x1 advisory payload.",
        "retry_summary": [
            "initial attempt returned short handshake stubs",
            "strict task-payload retry did not update final-message files within the 600 second observation window",
            "retry transport remains temp-only and is not treated as completion proof",
        ],
        "publication_boundary": "hashes_byte_counts_and_status_only",
    }
    save_json(cli_name, cli)
    save_md(
        f"{PHASE}-cli-completion-v1.md",
        f"{PHASE} CLI Lane Completion Notice",
        [
            "Status: `OPEN_GAP_CLI_ADVISORY_STUB_RETRY_PENDING`",
            "Arby and Aster Vale were attempted through the existing read-only CLI lanes.",
            "The available final-message files were handshake stubs, not usable x1 advisory payloads.",
            "Raw lane output remains temp-only and unpublished.",
        ],
    )

    for lane in timing.get("lanes", []):
        if lane.get("lane") in {"Arby", "Aster Vale"}:
            lane["status"] = "OPEN_GAP_HANDSHAKE_STUB_RETRY_PENDING"
            lane["completion_type"] = "cli_handshake_stub_not_advisory"
            lane["advisory_quality_status"] = "HANDSHAKE_STUB_NOT_X1_ADVISORY"
    timing["overall_status"] = "OPEN_GAP_THREE_APP_LANES_READY_TWO_CLI_STUBS"
    timing["quality_note"] = "All five lanes were attempted, but Arby/Aster CLI final-message stubs are not counted as completed x1 advisories."
    save_json(timing_name, timing)
    save_md(
        f"{PHASE}-five-lane-timing-v1.md",
        f"{PHASE} Five-Lane Timing Receipt",
        [
            "Status: `OPEN_GAP_THREE_APP_LANES_READY_TWO_CLI_STUBS`",
            "Cicero, Kierkegaard, and Aristotle completed through the local app-server route.",
            "Arby and Aster Vale were attempted, but their CLI outputs are handshake stubs pending retry/continuation.",
            "The 312.832 second foothold remains planning support only, not completion proof.",
        ],
    )

    if multiplex:
        multiplex["overall_status"] = "OPEN_GAP_CLI_ADVISORY_STUB_RETRY_PENDING"
        for lane in multiplex.get("lanes", []):
            if lane.get("lane") in {"Arby", "Aster Vale"}:
                lane["status"] = "OPEN_GAP_HANDSHAKE_STUB_RETRY_PENDING"
        multiplex["operator_note"] = "Status board remains receipt-only and does not expose lane bodies, transport output, local temp paths, image captures, rollout streams, or private auth material."
        save_json(multiplex_name, multiplex)
        save_md(
            f"{PHASE}-local-multiplex-tui-app-server-runner-v1.md",
            f"{PHASE} Local Multiplex TUI App Server Runner",
            [
                "Status: `OPEN_GAP_CLI_ADVISORY_STUB_RETRY_PENDING`",
                "App lanes completed; CLI lanes require advisory-quality continuation.",
                "Receipt-only board: no lane bodies, transport output, local temp paths, image captures, rollout streams, or private auth material.",
            ],
        )

    if synthesis:
        synthesis["overall_status"] = "OPEN_GAP_V486_GMUT_THOS_V22_V3_X1_CLI_STUBS"
        synthesis.setdefault("evidence", {}).setdefault("cli_lanes", {})["status"] = "OPEN_GAP_CLI_ADVISORY_STUB_RETRY_PENDING"
        synthesis.setdefault("evidence", {}).setdefault("multiplex", {})["status"] = "OPEN_GAP_CLI_ADVISORY_STUB_RETRY_PENDING"
        synthesis["boundary_lessons"] = [
            "All five existing lanes were attempted at the v486-gmut-thos-v22-v3-x1 x1 boundary.",
            "The three app-server lanes completed and remain usable for x2 planning.",
            "Arby and Aster Vale CLI final-message files were handshake stubs, so they are not counted as completed advisory payloads.",
            "x2 may proceed with an explicit CLI-open-gap receipt while retry/continuation remains active.",
        ]
        save_json(synthesis_name, synthesis)
        save_md(
            f"{PHASE}-synthesis-v1.md",
            f"{PHASE} Synthesis",
            [
                "Status: `OPEN_GAP_V486_GMUT_THOS_V22_V3_X1_CLI_STUBS`",
                "The app-lane portion completed cleanly.",
                "The CLI-lane portion is attempted but not advisory-complete.",
                "Next x2 should build from app-lane and Aletheon evidence while keeping Arby/Aster retry state open.",
            ],
        )

    quality = {
        "artifact_type": "cli_advisory_quality_gate",
        "phase_slug": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "OPEN_GAP_CLI_ADVISORY_STUB_RETRY_PENDING",
        "lanes": quality_lanes,
        "app_lane_status": "three_app_lanes_completed",
        "allowed_forward_motion": "x2_may_continue_with_explicit_cli_open_gap_receipt",
        "not_completion_proof": [
            "short final-message handshake stubs",
            "soft wait foothold",
            "transport warnings alone",
        ],
        "publication_boundary": {
            "lane_body_text_published": False,
            "raw_transport_published": False,
            "local_temp_paths_published": False,
        },
        "claim_boundary": {
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
        },
    }
    save_json(f"{PHASE}-cli-advisory-quality-gate-v1.json", quality)
    save_md(
        f"{PHASE}-cli-advisory-quality-gate-v1.md",
        f"{PHASE} CLI Advisory Quality Gate",
        [
            "Status: `OPEN_GAP_CLI_ADVISORY_STUB_RETRY_PENDING`",
            "Arby and Aster Vale were attempted, but the available final messages are handshake stubs.",
            "The stubs are not used as x1 advisory completion proof.",
            "x2 can continue from app-lane/Aletheon evidence while CLI retry state remains open.",
        ],
    )
    print(json.dumps({"status": "ok", "phase_slug": PHASE, "quality": quality["overall_status"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
