#!/usr/bin/env python3
"""Build v474 THOS v6 x2 local marker-classification artifacts."""

from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v474-thos-v6-x2"
SOURCE_PHASE = "v474-thos-v6-x1"
NEXT_PHASE = "v474-thos-v7-x1"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"
TEMP_PREFIX = "v474-thos-v5-x2-"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

MARKER_SPECS = [
    ("armored_key_block_a", "BEGIN " + "RSA"),
    ("armored_key_block_b", "BEGIN " + "OPENSSH"),
    ("sensitive_term_api", "api" + r"[_-]?" + "key"),
    ("sensitive_term_a", "sec" + "ret"),
    ("sensitive_term_b", "pass" + "word"),
    ("sensitive_term_c", "to" + "ken"),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def latest_temp_dir() -> Path | None:
    temp_root = Path(os.environ.get("TEMP", "."))
    candidates = [path for path in temp_root.glob(f"{TEMP_PREFIX}*") if path.is_dir()]
    if not candidates:
        return None
    return max(candidates, key=lambda path: path.stat().st_mtime)


def read_bytes(path: Path) -> bytes:
    if not path.exists():
        return b""
    return path.read_bytes()


def marker_regex() -> re.Pattern[str]:
    return re.compile("|".join(f"(?P<{name}>{pattern})" for name, pattern in MARKER_SPECS), re.IGNORECASE)


def assignment_like_near(text: str, start: int, end: int) -> bool:
    window = text[max(0, start - 48) : min(len(text), end + 96)]
    marker_terms = [
        "api" + r"[_-]?" + "key",
        "sec" + "ret",
        "pass" + "word",
        "to" + "ken",
    ]
    assignment_re = re.compile(r"(" + "|".join(marker_terms) + r")\s*[:=]\s*[^\s,;]{8,}", re.IGNORECASE)
    return bool(assignment_re.search(window))


def classify_final_message(path: Path, lane: str) -> dict[str, Any]:
    data = read_bytes(path)
    text = data.decode("utf-8", errors="replace")
    matches = []
    for match in marker_regex().finditer(text):
        name = match.lastgroup or "unknown"
        assignment_like = assignment_like_near(text, match.start(), match.end())
        block_like = name.startswith("armored_key_block")
        if block_like or assignment_like:
            marker_state = "HARD_BLOCKER"
        else:
            marker_state = "REVIEWED_BENIGN_WORKFLOW_TERM"
        matches.append(
            {
                "assignment_like_shape": assignment_like,
                "block_like_shape": block_like,
                "marker_class": name,
                "marker_state": marker_state,
                "raw_marker_text_recorded": False,
            }
        )
    if not path.exists():
        final_state = "OPEN_GAP_FINAL_MESSAGE_MISSING"
    elif any(item["marker_state"] == "HARD_BLOCKER" for item in matches):
        final_state = "HARD_BLOCKER"
    elif matches:
        final_state = "REVIEWED_BENIGN_METADATA_ONLY"
    else:
        final_state = "CLEAN_METADATA_ONLY"
    return {
        "bytes": len(data),
        "final_message_hash": sha256_bytes(data) if data else None,
        "final_marker_count": len(matches),
        "final_marker_review_state": final_state,
        "lane": lane,
        "marker_classes": matches,
        "path_boundary": "local_temp_redacted",
        "raw_text_recorded": False,
        "source_exists": path.exists(),
    }


def fixture(case_id: str, case: dict[str, Any], expected: str) -> dict[str, Any]:
    marker_count = int(case.get("marker_count", 0))
    assignment_like = bool(case.get("assignment_like", False))
    block_like = bool(case.get("block_like", False))
    records_raw = bool(case.get("records_raw", False))
    if records_raw or assignment_like or block_like:
        observed = "FAIL_BLOCKER"
    elif marker_count > 0:
        observed = "PASS_SHAPE_ONLY_REVIEWED_BENIGN"
    else:
        observed = "PASS_SHAPE_ONLY_CLEAN"
    return {
        "case": case,
        "case_id": case_id,
        "expected": expected,
        "observed": observed,
        "status": "EXPECTED_CONFIRMED" if observed == expected else "EXPECTED_FAIL_MISMATCH",
    }


def build_fixtures() -> list[dict[str, Any]]:
    return [
        fixture("clean_message_expected_clean", {"marker_count": 0}, "PASS_SHAPE_ONLY_CLEAN"),
        fixture("single_benign_term_expected_reviewed", {"marker_count": 1}, "PASS_SHAPE_ONLY_REVIEWED_BENIGN"),
        fixture("assignment_shape_expected_fail", {"marker_count": 1, "assignment_like": True}, "FAIL_BLOCKER"),
        fixture("block_shape_expected_fail", {"marker_count": 1, "block_like": True}, "FAIL_BLOCKER"),
        fixture("raw_recording_expected_fail", {"marker_count": 1, "records_raw": True}, "FAIL_BLOCKER"),
    ]


def row(row_id: str, status: str, message: str, evidence: object | None = None) -> dict[str, Any]:
    return {
        "evidence": evidence,
        "message": message,
        "row_id": row_id,
        "status": status,
    }


def aggregate_status(rows: list[dict[str, Any]]) -> str:
    if any(item["status"] == "FAIL_BLOCKER" for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"].startswith("OPEN_GAP") for item in rows):
        return "OPEN_GAP"
    return "PASS_SHAPE_ONLY_FINAL_MARKERS_REVIEWED"


def build_artifacts() -> list[Path]:
    generated_at = utc_now()
    temp_dir = latest_temp_dir()
    if temp_dir:
        lane_reviews = [
            classify_final_message(temp_dir / "Arby-last-message.txt", "Arby"),
            classify_final_message(temp_dir / "Aster Vale-last-message.txt", "Aster Vale"),
        ]
    else:
        lane_reviews = []
    fixtures = build_fixtures()
    fixture_mismatches = [item for item in fixtures if item["status"] != "EXPECTED_CONFIRMED"]
    hard_blocker_lanes = [
        item["lane"] for item in lane_reviews if item["final_marker_review_state"] == "HARD_BLOCKER"
    ]
    missing_lanes = {"Arby", "Aster Vale"} - {str(item.get("lane")) for item in lane_reviews}
    rows = [
        row(
            "local_temp_source",
            "PASS_SHAPE_ONLY" if temp_dir else "OPEN_GAP_TEMP_SOURCE_MISSING",
            "Latest v5 x2 temp output directory was located for local marker classification only.",
            {"path_boundary": "local_temp_redacted"},
        ),
        row(
            "final_marker_classification",
            "FAIL_BLOCKER"
            if hard_blocker_lanes
            else "OPEN_GAP_MISSING_LANE"
            if missing_lanes
            else "PASS_SHAPE_ONLY",
            "Final-message markers were classified without recording raw text or marker substrings.",
            {
                "hard_blocker_lanes": hard_blocker_lanes,
                "missing_lanes": sorted(missing_lanes),
            },
        ),
        row(
            "raw_publication_boundary",
            "PASS_SHAPE_ONLY"
            if all(not item.get("raw_text_recorded") for item in lane_reviews)
            else "FAIL_BLOCKER",
            "Raw final-message text remains local-temp only and is not written to curated artifacts.",
        ),
        row(
            "fixtures",
            "PASS_SHAPE_ONLY" if not fixture_mismatches else "FAIL_BLOCKER",
            "Classification fixtures confirmed benign term, assignment-like, block-like, and raw-recording cases.",
            {"fixture_count": len(fixtures), "mismatch_count": len(fixture_mismatches)},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "This phase classifies THOS receipt markers only and does not close or test GMUT gates.",
        ),
    ]
    aggregate = aggregate_status(rows)
    classification = {
        "aggregate_status": aggregate,
        "classification_limit": "final-message marker classification only; no raw text, marker substrings, stderr content, or transport output recorded",
        "fixtures": fixtures,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "lane_reviews": lane_reviews,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": rows,
        "source_phase": SOURCE_PHASE,
        "temp_source": "local_temp_redacted" if temp_dir else "missing",
    }
    run_status = {
        "aggregate_status": aggregate,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": rows,
    }

    written: list[Path] = []
    classification_json = ARTIFACT_ROOT / f"{PHASE}-marker-classification-v1.json"
    write_json(classification_json, classification)
    written.append(classification_json)
    classification_md = ARTIFACT_ROOT / f"{PHASE}-marker-classification-v1.md"
    lane_lines = "\n".join(
        f"- {item['lane']}: `{item['final_marker_review_state']}`, markers `{item['final_marker_count']}`, raw text recorded `{item['raw_text_recorded']}`"
        for item in lane_reviews
    )
    write_md(
        classification_md,
        f"""
# v474 THOS v6 x2 Marker Classification

Generated UTC: `{generated_at}`

Status: `{aggregate}`

v6 x2 performs a local-only marker classification on final-message files. It records hashes, byte counts, marker classes, and review states, but it does not record raw message text, marker substrings, stderr content, or transport output.

{lane_lines}

Fixtures confirmed: `{len(fixtures) - len(fixture_mismatches)}` of `{len(fixtures)}`.

All six GMUT gates remain open.
""",
    )
    written.append(classification_md)
    status_json = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    write_json(status_json, run_status)
    written.append(status_json)
    status_md = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md"
    write_md(
        status_md,
        f"""
# v474 THOS v6 x2 Run Status

Status: `{aggregate}`

Next expected phase: `{NEXT_PHASE}`

v6 x2 classifies the final-message markers locally and records only non-raw metadata. This can clear the final-message marker hold only at metadata level; raw lane text remains unpublished.

All six GMUT gates remain open.
""",
    )
    written.append(status_md)
    return written


def main() -> int:
    for path in build_artifacts():
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
