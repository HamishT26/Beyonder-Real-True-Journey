#!/usr/bin/env python3
"""Record Aletheon-led v2 App execution for one v421-v440 phase."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "docs" / "trinity-live-traces"
RUN_STATUS_JSON = TRACE / "v421-v440-sibling-run-status-v1.json"
RUN_STATUS_MD = TRACE / "v421-v440-sibling-run-status-v1.md"
PHASE_MIN = 421
PHASE_MAX = 440
MIN_USEFUL_MINUTES = 60


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def validate_phase(phase: int) -> None:
    if phase < PHASE_MIN or phase > PHASE_MAX:
        raise SystemExit(f"phase must be between {PHASE_MIN} and {PHASE_MAX}; got {phase}")


def start_path(phase: int) -> Path:
    return TRACE / f"v421-v440-sibling-phase-v{phase}-start-v1.json"


def cli_aggregate_path(phase: int) -> Path:
    return TRACE / f"v421-v440-sibling-phase-v{phase}-v1-cli-receipts-v1.json"


def v2_paths(phase: int) -> tuple[Path, Path]:
    stem = TRACE / f"v421-v440-sibling-phase-v{phase}-v2-app-receipt-v1"
    return stem.with_suffix(".json"), stem.with_suffix(".md")


def active_paths(phase: int) -> tuple[Path, Path]:
    stem = TRACE / f"v421-v440-sibling-phase-v{phase}-v2-app-active-v1"
    return stem.with_suffix(".json"), stem.with_suffix(".md")


def ensure_v1_complete(phase: int) -> dict[str, Any]:
    aggregate = read_json(cli_aggregate_path(phase), {})
    if aggregate.get("status") != "v1_cli_receipts_complete":
        raise SystemExit(f"v{phase} v1 CLI receipt aggregate must be complete before v2 starts")
    return aggregate


def write_run_status(phase: int, status: str, active_json: Path, active_md: Path, next_action: str) -> None:
    payload = {
        "generated_utc": now_iso(),
        "phase_range": "v421-v440",
        "status": status,
        "active_phase": phase,
        "active_run": "v2_app_execution",
        "active_phase_status": status,
        "active_phase_artifacts": {"json": rel(active_json), "md": rel(active_md)},
        "last_completion": None,
        "closeout_declaration": None,
        "next_action": next_action,
    }
    write_json(RUN_STATUS_JSON, payload)
    lines = [
        "# v421-v440 Sibling Run Status",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{status}`",
        f"Active phase: `v{phase}`",
        "Active run: `v2_app_execution`",
        "",
        "Active artifacts:",
        f"- `{rel(active_json)}`",
        f"- `{rel(active_md)}`",
        "",
        f"Next action: {next_action}",
    ]
    RUN_STATUS_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def start_v2(phase: int) -> dict[str, Any]:
    validate_phase(phase)
    start = read_json(start_path(phase), {})
    if start.get("status") != "phase_started":
        raise SystemExit(f"v{phase} phase start artifact is missing or not started")
    aggregate = ensure_v1_complete(phase)
    active_json, active_md = active_paths(phase)
    payload = {
        "generated_utc": now_iso(),
        "phase_range": "v421-v440",
        "phase": phase,
        "run": "v2_app_execution",
        "status": "v2_app_run_active",
        "v1_cli_receipts": rel(cli_aggregate_path(phase)),
        "v1_status": aggregate.get("status"),
        "minimum_useful_minutes": MIN_USEFUL_MINUTES,
        "execution_policy": {
            "authority": "Aletheon-led App execution with Parfit, Cicero, and Kierkegaard advisory input when available.",
            "external_policy": "local_first_only",
            "allowed": ["repo/doc/script work", "local validation", "local browser or security inspection", "curated git publication"],
            "not_allowed_without_new_scope": ["Notion writes", "Google Drive writes", "cloud/provider mutation", "paid external actions", "account mutation"],
        },
        "truth_boundaries": [
            "This starts v2; it does not mark v2 complete.",
            "Aletheon must record concrete v2 outcomes before phase completion.",
            "Advisory App siblings do not replace Aletheon publication review.",
        ],
        "next_action": f"After real App-side work and validation, run scripts/trinity_v421_v440_app_phase_runner.py --phase {phase} --complete --summary \"...\" --validation \"...\".",
    }
    write_json(active_json, payload)
    active_md.write_text(
        "\n".join(
            [
                f"# v{phase} v2 App Run Active",
                "",
                f"Generated UTC: `{payload['generated_utc']}`",
                f"Status: `{payload['status']}`",
                f"Minimum useful minutes: `{MIN_USEFUL_MINUTES}`",
                "",
                "Truth boundaries:",
                *[f"- {item}" for item in payload["truth_boundaries"]],
                "",
                f"Next action: {payload['next_action']}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    write_run_status(phase, "v2_app_run_active", active_json, active_md, payload["next_action"])
    return payload


def complete_v2(args: argparse.Namespace) -> dict[str, Any]:
    phase = args.phase
    validate_phase(phase)
    ensure_v1_complete(phase)
    active_json, _ = active_paths(phase)
    active = read_json(active_json, {})
    if active.get("status") != "v2_app_run_active" and not args.force:
        raise SystemExit(f"v{phase} v2 must be started before completion; use --force only for recovery.")
    receipt_json, receipt_md = v2_paths(phase)
    changed_paths = args.changed_path or []
    validations = args.validation or []
    blockers = args.blocker or []
    status = "v2_app_complete" if args.summary and validations and not blockers else "blocked_v2_app_incomplete"
    payload = {
        "generated_utc": now_iso(),
        "phase_range": "v421-v440",
        "phase": phase,
        "run": "v2_app_execution",
        "status": status,
        "summary": args.summary or "",
        "changed_paths": changed_paths,
        "validations": validations,
        "blockers": blockers,
        "external_policy": "local_first_only",
        "spent_external_usd": 0,
        "advisory_siblings": ["Parfit", "Cicero", "Kierkegaard"],
        "truth_boundaries": [
            "This v2 receipt records Aletheon-led App execution, not CLI sibling receipt evidence.",
            "No paid external action or external-service mutation is claimed.",
            "Changed paths are declarative; Git staging checks remain required before commit.",
        ],
        "next_action": f"Complete v{phase} with scripts/trinity_v421_v440_sibling_phase_complete.py --phase {phase} --open-next." if status == "v2_app_complete" else "Resolve v2 blockers before phase completion.",
    }
    write_json(receipt_json, payload)
    lines = [
        f"# v{phase} v2 App Receipt",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        "",
        "Summary:",
        payload["summary"] or "-",
        "",
        "Changed paths:",
        *([f"- `{item}`" for item in changed_paths] or ["- None recorded"]),
        "",
        "Validations:",
        *([f"- {item}" for item in validations] or ["- None recorded"]),
    ]
    if blockers:
        lines.extend(["", "Blockers:", *[f"- {item}" for item in blockers]])
    lines.extend(["", "Truth boundaries:", *[f"- {item}" for item in payload["truth_boundaries"]], "", f"Next action: {payload['next_action']}"])
    receipt_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    write_run_status(phase, payload["status"], receipt_json, receipt_md, payload["next_action"])
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", type=int, required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--start", action="store_true")
    group.add_argument("--complete", action="store_true")
    parser.add_argument("--summary", default="")
    parser.add_argument("--validation", action="append")
    parser.add_argument("--changed-path", action="append")
    parser.add_argument("--blocker", action="append")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    payload = start_v2(args.phase) if args.start else complete_v2(args)
    print(json.dumps({"status": payload["status"], "phase": args.phase, "run": payload["run"]}, indent=2))
    return 0 if payload["status"] in {"v2_app_run_active", "v2_app_complete"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
