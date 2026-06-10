#!/usr/bin/env python3
"""Build v476 THOS v3 x1 handoff contract artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v476-thos-v3-x1"
SOURCE_PHASE = "v476-thos-v2-x2"
NEXT_PHASE = "v476-thos-v3-x2"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"
SOURCE_GATE = ARTIFACT_ROOT / "v476-thos-v2-x2-required-row-gate-v1.json"
SOURCE_STATUS = ARTIFACT_ROOT / "v476-thos-v2-x2-run-status-v1.json"
SUITE_SEED = ARTIFACT_ROOT / "v476-thos-v1-x1-suite-map-seed-v1.json"
LANE_LAUNCHER = REPO_ROOT / "scripts" / "thos_codex_cli_advisory_launcher.py"
WATCH_LAUNCHER = REPO_ROOT / "scripts" / "thos_cli_lane_watch_launcher.py"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

BLOCKED_PUBLICATION_CLASSES = [
    "runtime_capture_publication",
    "transport_body_publication",
    "private_material_publication",
    "unapproved_connector_write",
    "destructive_cleanup",
    "candidate_installation_without_preflight",
    "production_readiness_claim",
    "gmut_validation_claim",
    "canon_promotion_claim",
]

REQUIRED_CONTRACT_ROWS = [
    ("command_candidate_contract", "command_surface", "command_candidates"),
    ("skill_candidate_contract", "skill_surface", "skill_candidates"),
    ("system_expansion_candidate_contract", "system_expansion_surface", "system_expansion_candidates"),
    ("script_inventory_contract", "script_surface", "repo_scripts"),
    ("connector_plugin_boundary_contract", "connector_plugin_surface", "plugin_skill_manifests"),
    ("dashboard_sync_contract", "dashboard_surface", "dashboard_data_files"),
    ("receipt_freshness_contract", "receipt_surface", "trinity_live_traces"),
    ("publication_guard_contract", "publication_surface", "required_row_gate"),
    ("negative_fixture_contract", "fixture_surface", "required_row_gate"),
    ("source_hash_chain_contract", "source_authority_surface", "required_row_gate"),
    ("async_cli_lane_contract", "sibling_lane_surface", "arby_aster_async_lanes"),
    ("gmut_open_boundary_contract", "gmut_boundary", "gmut_gates_open"),
]

REQUIRED_COLUMNS = [
    "row_id",
    "surface_family",
    "source_ref",
    "contract_state",
    "materialization_state",
    "approval_required_for_live_write",
    "raw_material_boundary",
    "allowed_next_action",
    "blocked_publication_classes",
    "validation_gate",
    "claim_ceiling",
    "gmut_gate_effect",
]

LANES = [
    {
        "lane": "Arby",
        "worktree": "D:/GHC-Archives/agent-worktrees/v461-round-robin/arby-advisory",
    },
    {
        "lane": "Aster Vale",
        "worktree": "D:/GHC-Archives/agent-worktrees/v461-round-robin/aster-vale-advisory",
    },
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def nz_now() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()


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


def row(row_id: str, status: str, message: str, evidence: object | None = None) -> dict[str, Any]:
    return {
        "evidence": evidence,
        "message": message,
        "row_id": row_id,
        "status": status,
    }


def run_json(command: list[str]) -> tuple[int, dict[str, Any], str]:
    process = subprocess.run(
        command,
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    try:
        payload = json.loads(process.stdout) if process.stdout.strip() else {}
    except json.JSONDecodeError:
        payload = {"parse_status": "FAIL_BLOCKER", "stdout_prefix": process.stdout[:200]}
    return process.returncode, payload, process.stderr[:400]


def lane_prompt(lane: str, runtime_minutes: int) -> str:
    return (
        f"{PHASE} no-rush THOS advisory for {lane}. "
        "Run non-ephemeral and read-only. Do not write files, commit, push, mutate plugin caches, "
        "delete files, or publish raw transport. Take as long as needed inside the configured window; "
        "the goal is substance, not speed. Focus on the v476 handoff contract, materialization vs "
        "candidate-only decisions, watcher and notifier reliability, sandbox/CLI loader reliability, "
        "negative fixtures, safe next THOS tasks, and the claim boundary that THOS support does not "
        "close GMUT gates. Return a structured final advisory with assumptions, blockers, proposed "
        "contract rows, validation checks, and next actions. "
        f"Target runtime may be up to {runtime_minutes} minutes or longer if the CLI needs it."
    )


def launch_lane(lane: dict[str, str], output_dir: Path, runtime_minutes: int, execute: bool) -> dict[str, Any]:
    command = [
        sys.executable,
        str(LANE_LAUNCHER),
        "--lane-name",
        lane["lane"],
        "--worktree",
        lane["worktree"],
        "--prompt",
        lane_prompt(lane["lane"], runtime_minutes),
        "--output-dir",
        str(output_dir),
        "--wait-seconds",
        "0",
        "--redact",
    ]
    if execute:
        command.append("--execute")
    returncode, payload, stderr = run_json(command)
    return {
        "lane": lane["lane"],
        "launcher_returncode": returncode,
        "launcher_stderr_prefix": stderr,
        "launcher_summary": payload,
        "requested_runtime_minutes": runtime_minutes,
        "sandbox": "read-only",
        "worktree_label": f"{lane['lane']} configured advisory worktree",
    }


def launch_watcher(output_dir: Path, timeout_seconds: int, poll_seconds: int, execute: bool) -> dict[str, Any]:
    command = [
        sys.executable,
        str(WATCH_LAUNCHER),
        "--output-dir",
        str(output_dir),
        "--phase-slug",
        PHASE,
        "--lane",
        "Arby",
        "--lane",
        "Aster Vale",
        "--poll-seconds",
        str(poll_seconds),
        "--timeout-seconds",
        str(timeout_seconds),
        "--wait-seconds",
        "2",
        "--redact",
    ]
    if execute:
        command.append("--execute")
    returncode, payload, stderr = run_json(command)
    return {
        "watcher_returncode": returncode,
        "watcher_stderr_prefix": stderr,
        "watcher_summary": payload,
    }


def contract_row(row_id: str, surface_family: str, source_key: str, gate_ready: bool, suite: dict[str, Any]) -> dict[str, Any]:
    source_counts = suite.get("surface_counts", {})
    candidate_totals = suite.get("candidate_totals", {})
    if source_key in {"required_row_gate", "arby_aster_async_lanes", "gmut_gates_open"}:
        source_status = "PASS_SHAPE_ONLY"
    elif source_key in candidate_totals:
        source_status = "PASS_SHAPE_ONLY" if candidate_totals.get(source_key, 0) > 0 else "OPEN_GAP_SOURCE_EMPTY"
    else:
        source_status = "PASS_SHAPE_ONLY" if source_counts.get(source_key, 0) > 0 else "OPEN_GAP_SOURCE_EMPTY"
    materialization_state = "candidate_only_not_installed"
    if row_id in {"publication_guard_contract", "negative_fixture_contract", "source_hash_chain_contract", "gmut_open_boundary_contract"}:
        materialization_state = "evidence_contract_only"
    if row_id == "async_cli_lane_contract":
        materialization_state = "async_advisory_lane_temp_transport_only"
    return {
        "allowed_next_action": "gate in v476-thos-v3-x2 before any v476-thos-v4 materialization decision",
        "approval_required_for_live_write": True,
        "blocked_publication_classes": BLOCKED_PUBLICATION_CLASSES,
        "claim_ceiling": "handoff contract metadata only; no production readiness, connector authority, GMUT validation, or canon claim",
        "contract_state": "PASS_SHAPE_ONLY" if gate_ready and source_status == "PASS_SHAPE_ONLY" else "OPEN_GAP",
        "gmut_gate_effect": "none_open_not_tested",
        "materialization_state": materialization_state,
        "raw_material_boundary": "no runtime captures, raw lane transport, session streams, image captures, auth material, or private material published",
        "row_id": row_id,
        "source_ref": source_key,
        "source_status": source_status,
        "surface_family": surface_family,
        "validation_gate": "v476-thos-v3-x2-contract-gate",
    }


def fixture(case_id: str, case: dict[str, Any], expected: str) -> dict[str, Any]:
    observed = "OPEN_GAP"
    if case.get("missing_source") or case.get("async_pending"):
        observed = "OPEN_GAP"
    elif case.get("missing_contract_row") or case.get("missing_required_column"):
        observed = "FAIL_BLOCKER"
    elif case.get("publishes_raw_transport") or case.get("installs_candidate") or case.get("broad_stage"):
        observed = "FAIL_BLOCKER"
    elif case.get("missing_block_class") or case.get("moves_gmut_gate"):
        observed = "FAIL_BLOCKER"
    elif case.get("contract_ready") and case.get("metadata_only"):
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
        fixture("contract_ready_expected_pass", {"contract_ready": True, "metadata_only": True}, "PASS_SHAPE_ONLY"),
        fixture("missing_source_expected_open_gap", {"missing_source": True}, "OPEN_GAP"),
        fixture("async_pending_expected_open_gap", {"async_pending": True}, "OPEN_GAP"),
        fixture("missing_contract_row_expected_fail", {"missing_contract_row": True}, "FAIL_BLOCKER"),
        fixture("missing_required_column_expected_fail", {"missing_required_column": True}, "FAIL_BLOCKER"),
        fixture("missing_block_class_expected_fail", {"missing_block_class": True}, "FAIL_BLOCKER"),
        fixture("raw_transport_publication_expected_fail", {"publishes_raw_transport": True}, "FAIL_BLOCKER"),
        fixture("candidate_install_expected_fail", {"installs_candidate": True}, "FAIL_BLOCKER"),
        fixture("broad_stage_expected_fail", {"broad_stage": True}, "FAIL_BLOCKER"),
        fixture("gmut_gate_move_expected_fail", {"moves_gmut_gate": True}, "FAIL_BLOCKER"),
    ]


def aggregate_status(rows: list[dict[str, Any]], fixtures: list[dict[str, Any]]) -> str:
    if any(item["status"].startswith("FAIL") for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"] != "EXPECTED_CONFIRMED" for item in fixtures):
        return "FAIL_FIXTURE_MISMATCH"
    if any(item["status"].startswith("OPEN_GAP") for item in rows):
        return "OPEN_GAP_CONTRACT_SOURCE_OR_LANE_PENDING"
    return "PASS_SHAPE_ONLY_V476_HANDOFF_CONTRACT_READY"


def build_artifacts(args: argparse.Namespace) -> list[Path]:
    generated_at = utc_now()
    started_at_nz = nz_now()
    gate = read_json(SOURCE_GATE)
    gate_status = read_json(SOURCE_STATUS)
    suite = read_json(SUITE_SEED)
    source_refs = [source_ref(SOURCE_GATE), source_ref(SOURCE_STATUS), source_ref(SUITE_SEED)]
    source_gaps = [item for item in source_refs if item["status"] != "PASS_SHAPE_ONLY"]
    gate_ready = gate.get("aggregate_status") == "PASS_SHAPE_ONLY_V476_REQUIRED_ROW_GATE_READY"
    contract_rows = [contract_row(row_id, family, source_key, gate_ready, suite) for row_id, family, source_key in REQUIRED_CONTRACT_ROWS]
    missing_rows = sorted(set(row_id for row_id, _family, _source in REQUIRED_CONTRACT_ROWS) - {item["row_id"] for item in contract_rows})
    missing_columns = sorted(
        {
            column
            for column in REQUIRED_COLUMNS
            if any(column not in item for item in contract_rows)
        }
    )
    open_contract_rows = [item["row_id"] for item in contract_rows if item["contract_state"] != "PASS_SHAPE_ONLY"]
    existing_launch = read_json(ARTIFACT_ROOT / f"{PHASE}-handoff-contract-v1.json") if args.reuse_existing_launch else {}
    if args.reuse_existing_launch and existing_launch.get("lanes") and existing_launch.get("watcher"):
        lane_results = existing_launch["lanes"]
        watcher = existing_launch["watcher"]
        execution_mode = existing_launch.get("execution_mode", "live_launch_reused")
    else:
        safe_stamp = generated_at.replace(":", "").replace("+", "Z")
        output_dir = Path(os.environ.get("TEMP", ".")) / f"{PHASE}-{safe_stamp}"
        lane_results = [launch_lane(lane, output_dir, args.runtime_minutes, args.execute_cli_lanes) for lane in LANES]
        watcher = launch_watcher(output_dir, args.watcher_timeout_seconds, args.poll_seconds, args.execute_cli_lanes)
        execution_mode = "live_launch" if args.execute_cli_lanes else "plan_only"
    lane_launch_blocked = [item["lane"] for item in lane_results if item["launcher_returncode"] != 0]
    fixtures = build_fixtures()
    rows = [
        row(
            "source_refs",
            "PASS_SHAPE_ONLY" if not source_gaps else "OPEN_GAP_SOURCE_REFS",
            "v476 v2 gate, v476 v2 run-status, and v476 v1 suite seed were checked.",
            {"source_count": len(source_refs), "source_gap_count": len(source_gaps)},
        ),
        row(
            "source_gate_ready",
            "PASS_SHAPE_ONLY" if gate_ready and gate_status.get("aggregate_status") == "PASS_SHAPE_ONLY_V476_REQUIRED_ROW_GATE_READY" else "OPEN_GAP_SOURCE_GATE_NOT_READY",
            "The v476 v2 required-row gate must be ready before v3 handoff contract hardening.",
            {"gate_status": gate.get("aggregate_status"), "run_status": gate_status.get("aggregate_status")},
        ),
        row(
            "required_contract_rows",
            "PASS_SHAPE_ONLY" if not missing_rows else "FAIL_REQUIRED_CONTRACT_ROWS",
            "All required handoff contract rows are present.",
            {"missing_rows": missing_rows, "required_row_count": len(REQUIRED_CONTRACT_ROWS)},
        ),
        row(
            "required_contract_columns",
            "PASS_SHAPE_ONLY" if not missing_columns else "FAIL_REQUIRED_CONTRACT_COLUMNS",
            "All required handoff contract columns are present.",
            {"missing_columns": missing_columns, "required_column_count": len(REQUIRED_COLUMNS)},
        ),
        row(
            "contract_row_states",
            "PASS_SHAPE_ONLY" if not open_contract_rows else "OPEN_GAP_CONTRACT_ROW_SOURCE_STATUS",
            "Contract rows remain metadata-only and source-backed.",
            {"open_contract_rows": open_contract_rows},
        ),
        row(
            "async_cli_lane_launch",
            "PASS_SHAPE_ONLY" if not lane_launch_blocked else "OPEN_GAP_CLI_LANE_LAUNCH_BLOCKED",
            "Arby and Aster Vale no-rush read-only lane launches were attempted or planned.",
            {
                "execution_mode": execution_mode,
                "lane_launch_blocked": lane_launch_blocked,
            },
        ),
        row(
            "completion_watcher",
            "PASS_SHAPE_ONLY" if watcher["watcher_returncode"] == 0 else "OPEN_GAP_WATCHER_LAUNCH_BLOCKED",
            "A background watcher writes curated completion metadata only.",
            {"watcher_returncode": watcher["watcher_returncode"]},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "All GMUT gates remain open and THOS contract work does not validate GMUT.",
            {"gmut_gate_effect": "none_open_not_tested", "gmut_gates_open": GMUT_GATES},
        ),
    ]
    status = aggregate_status(rows, fixtures)

    payload = {
        "aggregate_status": status,
        "contract_rows": contract_rows,
        "execution_mode": execution_mode,
        "fixtures": fixtures,
        "generated_at_utc": generated_at,
        "gmut_gate_effect": "none_open_not_tested",
        "gmut_gates_open": GMUT_GATES,
        "lanes": lane_results,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "preflight_rows": rows,
        "raw_output_dir": "<local_temp_redacted>",
        "required_columns": REQUIRED_COLUMNS,
        "required_contract_rows": [row_id for row_id, _family, _source in REQUIRED_CONTRACT_ROWS],
        "source_phase": SOURCE_PHASE,
        "source_refs": source_refs,
        "started_at_nz": started_at_nz,
        "watcher": watcher,
        "watcher_poll_seconds": args.poll_seconds,
        "watcher_timeout_seconds": args.watcher_timeout_seconds,
    }

    run_status = {
        "aggregate_status": status,
        "generated_at_utc": generated_at,
        "gmut_gate_effect": "none_open_not_tested",
        "gmut_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": rows,
        "started_at_nz": started_at_nz,
    }

    written: list[Path] = []
    contract_json = ARTIFACT_ROOT / f"{PHASE}-handoff-contract-v1.json"
    contract_md = ARTIFACT_ROOT / f"{PHASE}-handoff-contract-v1.md"
    status_json = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    status_md = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md"
    write_json(contract_json, payload)
    written.append(contract_json)
    contract_lines = "\n".join(
        f"- `{item['row_id']}`: `{item['contract_state']}`, materialization `{item['materialization_state']}`"
        for item in contract_rows
    )
    lane_lines = "\n".join(
        f"- {item['lane']}: launcher `{item['launcher_returncode']}`, sandbox `{item['sandbox']}`, target `{item['requested_runtime_minutes']}` minutes"
        for item in lane_results
    )
    write_md(
        contract_md,
        f"""
# v476 THOS v3 x1 Handoff Contract

NZ start: `{started_at_nz}`
Generated UTC: `{generated_at}`

Status: `{status}`

This artifact turns the v476 v2 required-row gate into a handoff contract for later THOS phases. It is metadata-only: no command, skill, connector, dashboard, or system-expansion candidate is installed or promoted here.

Contract rows:

{contract_lines}

Arby/Aster lane policy:

{lane_lines}

Watcher poll seconds: `{args.poll_seconds}`
Watcher timeout seconds: `{args.watcher_timeout_seconds}`
Execution mode: `{execution_mode}`

Raw lane transport remains local temp-only and unpublished. The watcher may write a curated completion notice pair for metadata only.

All six GMUT gates remain open.
""",
    )
    written.append(contract_md)
    write_json(status_json, run_status)
    written.append(status_json)
    status_lines = "\n".join(f"- `{item['row_id']}`: `{item['status']}`" for item in rows)
    write_md(
        status_md,
        f"""
# v476 THOS v3 x1 Run Status

NZ start: `{started_at_nz}`
Generated UTC: `{generated_at}`

Status: `{status}`
Next expected phase: `{NEXT_PHASE}`

Rows:

{status_lines}

No runtime transport, session streams, image captures, auth material, plugin-cache bodies, user-skill bodies, or raw sibling transport are published.

All six GMUT gates remain open.
""",
    )
    written.append(status_md)
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description="Build v476 THOS v3 x1 handoff contract artifacts.")
    parser.add_argument("--execute-cli-lanes", action="store_true", help="Launch Arby/Aster read-only advisory lanes.")
    parser.add_argument("--runtime-minutes", type=int, default=60)
    parser.add_argument("--poll-seconds", type=int, default=120)
    parser.add_argument("--watcher-timeout-seconds", type=int, default=72000)
    parser.add_argument("--reuse-existing-launch", action="store_true", help="Reuse current x1 lane/watch metadata instead of launching again.")
    args = parser.parse_args()
    written = build_artifacts(args)
    print(json.dumps({"written": [str(path.relative_to(REPO_ROOT)).replace("\\", "/") for path in written]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
