#!/usr/bin/env python3
"""Validate GMUT/THOS v1-v8 x1/x2 phase sequence transitions."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


PHASE_RE = re.compile(r"^v(?P<major>\d+)-gmut-thos-v(?P<cycle>\d+)-v(?P<version>\d+)-x(?P<x>[12])$")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def parse_phase(slug: str) -> dict[str, int] | None:
    match = PHASE_RE.match(slug)
    if not match:
        return None
    return {key: int(value) for key, value in match.groupdict().items()}


def expected_next(current: dict[str, int]) -> dict[str, int]:
    if current["x"] == 1:
        return {
            "major": current["major"],
            "cycle": current["cycle"],
            "version": current["version"],
            "x": 2,
        }
    if current["version"] < 8:
        return {
            "major": current["major"],
            "cycle": current["cycle"],
            "version": current["version"] + 1,
            "x": 1,
        }
    return {
        "major": current["major"] + 1,
        "cycle": current["cycle"] + 1,
        "version": 1,
        "x": 1,
    }


def format_phase(parts: dict[str, int]) -> str:
    return f"v{parts['major']}-gmut-thos-v{parts['cycle']}-v{parts['version']}-x{parts['x']}"


def build_report(current_slug: str, next_slug: str) -> dict[str, object]:
    current = parse_phase(current_slug)
    proposed = parse_phase(next_slug)
    rows = []
    if current is None:
        rows.append({"row_id": "current_slug_parse", "status": "FAIL_BLOCKER", "evidence": current_slug})
    else:
        rows.append({"row_id": "current_slug_parse", "status": "PASS", "evidence": current_slug})
    if proposed is None:
        rows.append({"row_id": "next_slug_parse", "status": "FAIL_BLOCKER", "evidence": next_slug})
    else:
        rows.append({"row_id": "next_slug_parse", "status": "PASS", "evidence": next_slug})

    expected_slug = None
    if current is not None and proposed is not None:
        expected = expected_next(current)
        expected_slug = format_phase(expected)
        rows.append(
            {
                "row_id": "next_slug_matches_expected_sequence",
                "status": "PASS" if proposed == expected else "FAIL_BLOCKER",
                "evidence": f"expected={expected_slug}; proposed={next_slug}",
            }
        )
    failed = [row for row in rows if row["status"] != "PASS"]
    return {
        "artifact_type": "thos_phase_sequence_guard_report",
        "current_phase_slug": current_slug,
        "proposed_next_phase_slug": next_slug,
        "expected_next_phase_slug": expected_slug,
        "generated_utc": utc_now(),
        "overall_status": "PASS_PHASE_SEQUENCE_GUARD" if not failed else "FAIL_PHASE_SEQUENCE_BLOCKER",
        "rows": rows,
        "mutation_performed": False,
        "raw_lane_text_published": False,
        "raw_transport_published": False,
        "gmut_gate_state": "all_gmut_gates_remain_open",
        "canon_promotion": "not_claimed",
    }


def write_md(report: dict[str, object], path: str) -> None:
    lines = [
        "# THOS Phase Sequence Guard",
        "",
        f"- Status: `{report['overall_status']}`",
        f"- Current phase: `{report['current_phase_slug']}`",
        f"- Proposed next phase: `{report['proposed_next_phase_slug']}`",
        f"- Expected next phase: `{report['expected_next_phase_slug']}`",
        "- Mutation performed: `false`",
        "",
        "## Rows",
        "",
    ]
    for row in report["rows"]:  # type: ignore[assignment]
        lines.append(f"- `{row['row_id']}`: `{row['status']}` - {row['evidence']}")
    lines.extend(
        [
            "",
            "Claim boundary: this guard validates sequence shape only. It does not start the next phase, contact lanes, validate GMUT, or promote canon.",
            "",
        ]
    )
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a GMUT/THOS phase transition.")
    parser.add_argument("--current-phase", required=True)
    parser.add_argument("--next-phase", required=True)
    parser.add_argument("--receipt-json")
    parser.add_argument("--receipt-md")
    args = parser.parse_args()

    report = build_report(args.current_phase, args.next_phase)
    if args.receipt_json:
        Path(args.receipt_json).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if args.receipt_md:
        write_md(report, args.receipt_md)
    print(json.dumps(report, indent=2))
    return 0 if report["overall_status"] == "PASS_PHASE_SEQUENCE_GUARD" else 1


if __name__ == "__main__":
    raise SystemExit(main())
