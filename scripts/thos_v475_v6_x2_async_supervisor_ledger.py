#!/usr/bin/env python3
"""Build v475 THOS v6 x2 async supervisor ledger artifacts."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v475-thos-v6-x2"
SOURCE_PHASE = "v475-thos-v6-x1"
NEXT_PHASE = "v475-thos-v7-x1"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"
SOURCE_JSON = ARTIFACT_ROOT / "v475-thos-v6-x1-no-rush-cli-lane-notifier-refresh-v1.json"
SOURCE_STATUS = ARTIFACT_ROOT / "v475-thos-v6-x1-run-status-v1.json"
COMPLETION_JSON = ARTIFACT_ROOT / "v475-thos-v6-x1-cli-lane-completion-notice-v1.json"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

LANES = ["Arby", "Aster Vale"]
APP_ADVISORY_SYNTHESIS = [
    {
        "lane": "Cicero",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "ledger should record lane status, final-message presence, marker-review status, watcher status, publication status, and next required event",
            "ledger must not record final text, transport text, temp paths, session streams, image captures, private auth material, marker substrings, or full sensitive paths",
            "notification wording should describe observer receipts, not app wakeup guarantees or content validity",
        ],
    },
    {
        "lane": "Kierkegaard",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "Aster still running is a normal no-rush async state, not a failure or hierarchy",
            "completion metadata must not become advisory quality, truth, continuity, consciousness, or canon proof",
            "user-facing language should stay calm: Arby metadata present, Aster running, aggregate waits for both",
        ],
    },
    {
        "lane": "Aristotle",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "required rows include Arby, Aster Vale, aggregate, timeout policy, unpublished-transport assertion, marker-review status, source-hash, and publication-boundary rows",
            "negative fixtures should block missing lane rows, premature publishable state, missing marker review, transport publication, timeout overclaim, source drift, generic pass, and GMUT movement",
            "publishable metadata requires both lanes present, marker review clean or benign, source hashes matching, and all blocked claims remaining blocked",
        ],
    },
]
SENSITIVE_RE = re.compile(
    "|".join(
        [
            "BEGIN " + "RSA",
            "BEGIN " + "OPENSSH",
            "api" + r"[_-]?" + "key",
            "sec" + "ret",
            "pass" + "word",
            "to" + "ken",
        ]
    ),
    re.IGNORECASE,
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def read_optional(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def source_ref(path: Path) -> dict[str, Any]:
    rel = path.relative_to(REPO_ROOT).as_posix()
    if not path.exists():
        return {"path": rel, "status": "OPEN_GAP_MISSING_SOURCE"}
    return {
        "bytes": path.stat().st_size,
        "path": rel,
        "sha256": sha256_file(path),
        "status": "PASS_SHAPE_ONLY",
    }


def process_active(pid: int | None) -> bool:
    if not pid:
        return False
    result = subprocess.run(
        ["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        text=True,
        check=False,
    )
    return str(pid) in result.stdout


def latest_output_dir() -> Path | None:
    temp_root = Path(os.environ.get("TEMP", "."))
    candidates = sorted(
        temp_root.glob(f"{SOURCE_PHASE}-*"),
        key=lambda item: item.stat().st_mtime if item.exists() else 0,
        reverse=True,
    )
    return candidates[0] if candidates else None


def file_meta(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"bytes": 0, "exists": False, "sha256": None}
    return {
        "bytes": path.stat().st_size,
        "exists": True,
        "sha256": sha256_file(path),
    }


def lane_snapshot(output_dir: Path | None, lane: str, pid: int | None) -> dict[str, Any]:
    final_path = output_dir / f"{lane}-last-message.txt" if output_dir else Path("__missing__")
    stdout_path = output_dir / f"{lane}-stdout.txt" if output_dir else Path("__missing__")
    stderr_path = output_dir / f"{lane}-stderr.txt" if output_dir else Path("__missing__")
    final_text = read_optional(final_path)
    stderr_text = read_optional(stderr_path)
    active = process_active(pid)
    if final_text:
        lane_state = "FINAL_MESSAGE_READY_METADATA_ONLY"
    elif active:
        lane_state = "RUNNING_NO_RUSH"
    else:
        lane_state = "OPEN_GAP_FINAL_MESSAGE_PENDING_PROCESS_NOT_ACTIVE"
    return {
        "final_message": {
            **file_meta(final_path),
            "sensitive_marker_count": len(SENSITIVE_RE.findall(final_text)),
            "text_hash": sha256_text(final_text) if final_text else None,
        },
        "lane": lane,
        "lane_state": lane_state,
        "pid_active": active,
        "pid_known": pid is not None,
        "raw_transport_boundary": "local_temp_only_not_published",
        "stderr": {
            **file_meta(stderr_path),
            "sensitive_marker_count_unpublished": len(SENSITIVE_RE.findall(stderr_text)),
        },
        "stdout": file_meta(stdout_path),
    }


def row(row_id: str, status: str, message: str, evidence: object | None = None) -> dict[str, Any]:
    return {
        "evidence": evidence,
        "message": message,
        "row_id": row_id,
        "status": status,
    }


def fixture(case_id: str, case: dict[str, Any], expected: str) -> dict[str, Any]:
    observed = "OPEN_GAP"
    if case.get("publishes_transport") or case.get("moves_gmut_gate") or case.get("missing_lane"):
        observed = "FAIL_BLOCKER"
    elif case.get("completion_claim_without_receipt") or case.get("quality_claim_from_metadata"):
        observed = "FAIL_BLOCKER"
    elif case.get("watcher_dead") or case.get("lane_pending"):
        observed = "OPEN_GAP"
    elif case.get("metadata_only") and case.get("watcher_alive"):
        observed = "PASS_SHAPE_ONLY"
    return {
        "case": case,
        "case_id": case_id,
        "expected": expected,
        "observed": observed,
        "status": "EXPECTED_CONFIRMED" if observed == expected else "EXPECTED_FAIL_MISMATCH",
    }


def build_fixtures() -> list[dict[str, Any]]:
    return [
        fixture("metadata_only_watcher_alive_expected_pass", {"metadata_only": True, "watcher_alive": True}, "PASS_SHAPE_ONLY"),
        fixture("lane_pending_expected_open_gap", {"lane_pending": True, "metadata_only": True}, "OPEN_GAP"),
        fixture("watcher_dead_expected_open_gap", {"watcher_dead": True, "metadata_only": True}, "OPEN_GAP"),
        fixture("transport_publication_expected_fail", {"publishes_transport": True}, "FAIL_BLOCKER"),
        fixture("missing_lane_expected_fail", {"missing_lane": True}, "FAIL_BLOCKER"),
        fixture("completion_claim_without_receipt_expected_fail", {"completion_claim_without_receipt": True}, "FAIL_BLOCKER"),
        fixture("quality_claim_from_metadata_expected_fail", {"quality_claim_from_metadata": True}, "FAIL_BLOCKER"),
        fixture("gmut_gate_move_expected_fail", {"moves_gmut_gate": True}, "FAIL_BLOCKER"),
    ]


def aggregate_status(rows: list[dict[str, Any]], fixtures: list[dict[str, Any]]) -> str:
    if any(item["status"].startswith("FAIL") for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"] != "EXPECTED_CONFIRMED" for item in fixtures):
        return "FAIL_FIXTURE_MISMATCH"
    if any(item["status"].startswith("OPEN_GAP") for item in rows):
        return "OPEN_GAP_ASYNC_LANE_PENDING"
    return "PASS_SHAPE_ONLY_ASYNC_SUPERVISOR_LEDGER_READY"


def build_artifacts() -> list[Path]:
    generated_at = utc_now()
    launch = read_json(SOURCE_JSON)
    status = read_json(SOURCE_STATUS)
    source_refs = [source_ref(SOURCE_JSON), source_ref(SOURCE_STATUS)]
    source_gaps = [item for item in source_refs if item["status"] != "PASS_SHAPE_ONLY"]
    output_dir = latest_output_dir()
    lane_pid_by_name = {
        lane.get("lane"): lane.get("launcher_summary", {}).get("pid")
        for lane in launch.get("lanes", [])
    }
    lane_snapshots = [lane_snapshot(output_dir, lane, lane_pid_by_name.get(lane)) for lane in LANES]
    missing_lanes = [item for item in lane_snapshots if not item["pid_known"]]
    final_ready = [item["lane"] for item in lane_snapshots if item["lane_state"] == "FINAL_MESSAGE_READY_METADATA_ONLY"]
    running = [item["lane"] for item in lane_snapshots if item["lane_state"] == "RUNNING_NO_RUSH"]
    pending = [item["lane"] for item in lane_snapshots if item["lane_state"].startswith("OPEN_GAP")]
    watcher_pid = launch.get("watcher", {}).get("watcher_summary", {}).get("pid")
    watcher_alive = process_active(watcher_pid)
    completion_receipt_exists = COMPLETION_JSON.exists()
    fixtures = build_fixtures()
    rows = [
        row(
            "source_refs",
            "PASS_SHAPE_ONLY" if not source_gaps else "OPEN_GAP_SOURCE_REFS",
            "v6 x1 launch and run-status sources were checked.",
            {"source_count": len(source_refs), "source_gap_count": len(source_gaps)},
        ),
        row(
            "lane_coverage",
            "PASS_SHAPE_ONLY" if not missing_lanes else "FAIL_MISSING_LANE",
            "Arby and Aster Vale lane metadata are both represented.",
            {"lanes": [item["lane"] for item in lane_snapshots], "missing_lane_count": len(missing_lanes)},
        ),
        row(
            "lane_state",
            "PASS_SHAPE_ONLY" if completion_receipt_exists else "OPEN_GAP_ASYNC_LANE_RUNNING_OR_PENDING",
            "Lane states are tracked without rushing outstanding work; absent combined receipt stays open.",
            {"final_ready": final_ready, "running": running, "pending": pending},
        ),
        row(
            "watcher_state",
            "PASS_SHAPE_ONLY" if watcher_alive or completion_receipt_exists else "OPEN_GAP_WATCHER_NOT_ACTIVE",
            "Background watcher is live or has already produced the durable completion receipt.",
            {"completion_receipt_exists": completion_receipt_exists, "watcher_alive": watcher_alive},
        ),
        row(
            "transport_boundary",
            "PASS_SHAPE_ONLY",
            "Only file metadata, hashes, and marker counts are recorded; lane transport remains local.",
            {"raw_transport_recorded": False},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "Async THOS supervision does not test, validate, or close GMUT gates.",
            {"gmut_gate_effect": "none_open_not_tested", "gmut_gates_open": GMUT_GATES},
        ),
        row(
            "app_advisory_synthesis",
            "PASS_SHAPE_ONLY",
            "Cicero, Kierkegaard, and Aristotle advisories were folded as sanitized metadata-only guidance.",
            {"advisory_count": len(APP_ADVISORY_SYNTHESIS), "raw_advisory_text_recorded": False},
        ),
    ]
    aggregate = aggregate_status(rows, fixtures)
    ledger = {
        "app_advisory_synthesis": APP_ADVISORY_SYNTHESIS,
        "aggregate_status": aggregate,
        "completion_receipt_expected": "docs/trinity-live-traces/v475-thos-v6-x1-cli-lane-completion-notice-v1.json",
        "completion_receipt_present": completion_receipt_exists,
        "fixtures": fixtures,
        "generated_at_utc": generated_at,
        "gmut_gate_effect": "none_open_not_tested",
        "gmut_gates_open": GMUT_GATES,
        "lane_snapshots": lane_snapshots,
        "next_expected_phase": NEXT_PHASE,
        "notification_boundary": "receipt_watcher_only_no_external_model_wakeup_claim",
        "output_dir": "<local_temp_redacted>" if output_dir else None,
        "phase_slug": PHASE,
        "rows": rows,
        "source_phase": SOURCE_PHASE,
        "source_refs": source_refs,
        "source_status": status.get("aggregate_status"),
        "watcher": {"pid_known": watcher_pid is not None, "pid_active": watcher_alive},
    }
    run_status = {
        "aggregate_status": aggregate,
        "generated_at_utc": generated_at,
        "gmut_gate_effect": "none_open_not_tested",
        "gmut_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": rows,
    }

    written: list[Path] = []
    ledger_json = ARTIFACT_ROOT / f"{PHASE}-async-supervisor-ledger-v1.json"
    write_json(ledger_json, ledger)
    written.append(ledger_json)
    ledger_md = ARTIFACT_ROOT / f"{PHASE}-async-supervisor-ledger-v1.md"
    lane_lines = "\n".join(
        f"- {item['lane']}: `{item['lane_state']}`, final bytes `{item['final_message']['bytes']}`, process active `{item['pid_active']}`"
        for item in lane_snapshots
    )
    write_md(
        ledger_md,
        f"""
# v475 THOS v6 x2 Async Supervisor Ledger

Generated UTC: `{generated_at}`

Status: `{aggregate}`

The async supervisor keeps Arby and Aster Vale on a no-rush path. It records metadata only; lane transport remains local and unpublished.

Lane states:

{lane_lines}

Watcher active: `{watcher_alive}`

Completion receipt present: `{completion_receipt_exists}`

App advisories folded: `{len(APP_ADVISORY_SYNTHESIS)}`

Next expected phase: `{NEXT_PHASE}`

All six GMUT gates remain open.
""",
    )
    written.append(ledger_md)
    status_json = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    write_json(status_json, run_status)
    written.append(status_json)
    status_md = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md"
    write_md(
        status_md,
        f"""
# v475 THOS v6 x2 Run Status

Status: `{aggregate}`

Next expected phase: `{NEXT_PHASE}`

v475 v6 x2 records the current Arby/Aster async notification state without reading publication content into curated artifacts. If a sibling is still running, that runtime is an open gap rather than a failure.

Cicero, Kierkegaard, and Aristotle advisories were folded as sanitized metadata-only guidance.

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
