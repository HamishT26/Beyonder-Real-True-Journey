#!/usr/bin/env python3
"""Create a compact status-only continuity index for the omega v2 line."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]

ANCHOR_PATTERNS = {
    "journey_docs": [
        "docs/journey-context/*Beyonder-Real-True*Journey*v49*",
        "docs/journey-context/*Beyonder-Real-True*Journey*v48*",
        "docs/journey-context/*Beyonder-Real-True*Journey*v47*",
        "docs/trinity-journey-corpus-runs/*Journey*v49*",
        "docs/trinity-journey-corpus-runs/*Journey*v48*",
        "docs/trinity-journey-corpus-runs/*Journey*v47*",
    ],
    "current_phase": [
        "docs/trinity-live-traces/v504-gmut-thos-v40-v5-x1-closeout-v1.*",
        "docs/trinity-live-traces/v504-gmut-thos-v40-v5-x2-prep-start-v1.*",
        "docs/trinity-live-traces/v504-gmut-thos-v40-v5-x2-phase-dashboard-receipt-v1.*",
        "docs/trinity-live-traces/v504-gmut-thos-v40-v5-x2-latest-essential-runner-map-v1.*",
    ],
    "branch_and_ipc": [
        "docs/trinity-live-traces/v504-gmut-thos-v40-v4-x2-omega-line-v2-branch-creation-receipt-v1.*",
        "docs/trinity-live-traces/v504-gmut-thos-v40-v4-x2-ghc-multiplex-ipc-bus-manifest-v1.*",
        "docs/trinity-live-traces/v504-gmut-thos-v40-v4-x2-grand-vision-card-v1.*",
    ],
    "approval_packets": [
        "docs/trinity-live-traces/v504-gmut-thos-v40-v4-x2-v506-v515-approval-tapestry-v1.md",
        "docs/trinity-live-traces/v504-gmut-thos-v40-v5-x2-approval-candidates-v1.*",
    ],
    "essential_scripts": [
        "scripts/ghc_multiplex_ipc_bus.py",
        "scripts/thos_latest_essential_runner_map.py",
        "scripts/thos_phase_dashboard_receipt.py",
        "scripts/thos_x2_build_use_acceptance_runner.py",
        "scripts/thos_phase_advance_gate_verifier.py",
    ],
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def repo_relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def collect(patterns: list[str], limit: int) -> list[dict[str, Any]]:
    found: dict[str, Path] = {}
    for pattern in patterns:
        for path in REPO_ROOT.glob(pattern):
            if path.is_file():
                found[repo_relative(path)] = path
    rows = []
    for key in sorted(found):
        path = found[key]
        rows.append(
            {
                "path": key,
                "file": path.name,
                "size_bytes": path.stat().st_size,
            }
        )
    return rows[:limit]


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    sections = {
        name: collect(patterns, args.per_section_limit)
        for name, patterns in ANCHOR_PATTERNS.items()
    }
    missing_sections = [name for name, rows in sections.items() if not rows]
    return {
        "artifact_type": "omega_v2_continuity_index",
        "phase_slug": args.phase_slug,
        "generated_utc": utc_now(),
        "overall_status": "PASS_OMEGA_V2_CONTINUITY_INDEX" if not missing_sections else "OPEN_GAP_OMEGA_V2_CONTINUITY_INDEX",
        "source_branch": "codex/GHC-Family/beyonder-shared-omega-line",
        "target_branch": "codex/GHC-Family/beyonder-shared-omega-line-v2",
        "missing_sections": missing_sections,
        "sections": sections,
        "read_order": [
            "grand_vision_card",
            "latest_phase_closeout",
            "latest_x2_prep_start",
            "latest_phase_dashboard",
            "latest_essential_runner_map",
            "approval_candidates",
            "ipc_bus_manifest",
        ],
        "selection_boundary": {
            "curated_index_only": True,
            "does_not_copy_raw_archives": True,
            "does_not_delete_or_rewrite_history": True,
            "status_only_publication": True,
        },
        "publication_boundary": {
            "status_only": True,
            "raw_lane_text_published": False,
            "raw_logs_published": False,
            "session_streams_published": False,
            "screenshots_published": False,
            "credentials_published": False,
            "local_absolute_paths_published": False,
        },
        "claim_boundary": {
            "gmut_gate_state": "open",
            "canon_promotion": "not_claimed",
            "consciousness_or_final_physics_proof": "not_claimed",
        },
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['phase_slug']} Omega v2 Continuity Index",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: `{payload['overall_status']}`",
        f"- source_branch: `{payload['source_branch']}`",
        f"- target_branch: `{payload['target_branch']}`",
        "",
        "## Read Order",
    ]
    lines.extend(f"- `{item}`" for item in payload["read_order"])
    for name, rows in payload["sections"].items():
        lines.extend(["", f"## {name}"])
        if rows:
            for row in rows:
                lines.append(f"- `{row['path']}` ({row['size_bytes']} bytes)")
        else:
            lines.append("- none found")
    lines.extend(["", "Missing sections:"])
    if payload["missing_sections"]:
        lines.extend(f"- `{item}`" for item in payload["missing_sections"])
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "Boundary: curated index only; no raw archive copy, no history rewrite, no raw lane text, logs, screenshots, credentials, session streams, or local absolute paths.",
            "",
            "GMUT, canon, consciousness, and final-physics gates remain open.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--per-section-limit", type=int, default=24)
    parser.add_argument("--receipt-json", required=True)
    parser.add_argument("--receipt-md", required=True)
    args = parser.parse_args()

    payload = build_payload(args)
    write_json(Path(args.receipt_json), payload)
    write_md(Path(args.receipt_md), payload)
    print(json.dumps({"status": payload["overall_status"], "phase_slug": args.phase_slug}, indent=2))
    return 0 if not payload["missing_sections"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
