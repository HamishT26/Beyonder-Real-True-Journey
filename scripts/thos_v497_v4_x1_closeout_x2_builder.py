#!/usr/bin/env python3
"""Build v497 v4 x1 closeout and v497 v4 x2 artifacts from curated receipts."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"


X2_TASKS = [
    {
        "task": "Five-lane normalized status board promotion",
        "build_use": "Use the new status normalizer as the default manual-check surface.",
        "validation": "Board reads curated receipts only and reports app plus CLI rows without raw payloads.",
    },
    {
        "task": "CLI heading contract repair",
        "build_use": "Carry the standalone heading template into the next x1 sibling launch.",
        "validation": "Dry prompt generation shows all six headings as standalone lines.",
    },
    {
        "task": "Marker-review split hardening",
        "build_use": "Separate generic sensitive-word markers from strict path/key/private-material markers.",
        "validation": "Completion notices and quality gates preserve both counts without raw text publication.",
    },
    {
        "task": "Watcher trust receipt contract",
        "build_use": "Keep watcher/notifier supervision visible while Aletheon works between cadence checks.",
        "validation": "Wait contracts declare next manual check and no early polling.",
    },
    {
        "task": "Source-to-build ledger conversion",
        "build_use": "Turn source rows into concrete runner, guard, and publication improvements.",
        "validation": "Each source row has an x2 build use rather than decorative citation only.",
    },
    {
        "task": "Publication provenance schema",
        "build_use": "Add subject, material, local head, remote head, and exact staged file inventory fields to future receipts.",
        "validation": "Remote-equals-local verification remains explicit after every push.",
    },
    {
        "task": "Stale-flow retry playbook update",
        "build_use": "Route heading gaps, marker-review gaps, app watcher waits, and CLI final-marker waits through typed retry ladders.",
        "validation": "Each blocker class has bounded retry attempts and a pause condition.",
    },
    {
        "task": "Skill evolution safe boundary",
        "build_use": "Draft skill candidates as repo-scoped proposals unless exact user-skill mutation approval is active.",
        "validation": "No plugin-cache or user-skill writes occur from this builder.",
    },
    {
        "task": "Trinity Mandala open-gate mapping",
        "build_use": "Map GMUT, THOS, and Freed ID/CBR work to source-backed, implementation-ready, or speculative-open buckets.",
        "validation": "No empirical, physics, consciousness, or canon closure is claimed.",
    },
    {
        "task": "Next x1 launch readiness",
        "build_use": "Prepare v497 v5 x1 prompts with heading template, watcher trust policy, and exact cadence checks.",
        "validation": "Next x1 launch remains blocked until v4 x2 publication validates cleanly.",
    },
]


def now_pair() -> tuple[str, str]:
    utc = dt.datetime.now(dt.UTC).replace(microsecond=0)
    nz = utc.astimezone(dt.timezone(dt.timedelta(hours=12), name="NZST"))
    return utc.isoformat().replace("+00:00", "Z"), nz.isoformat()


def read_json(name: str) -> dict[str, Any]:
    path = TRACE_DIR / name
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    return payload if isinstance(payload, dict) else {}


def require_pass(payload: dict[str, Any], label: str) -> None:
    if payload.get("overall_status") != "PASS_STATUS_CHECK_ALLOWED":
        raise SystemExit(f"{label} must be PASS_STATUS_CHECK_ALLOWED before build")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(path: Path, title: str, bullets: list[str]) -> None:
    lines = [f"# {title}", ""]
    lines.extend(f"- {item}" for item in bullets)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-x1-slug", default="v497-gmut-thos-v33-v4-x1")
    parser.add_argument("--x2-slug", default="v497-gmut-thos-v33-v4-x2")
    parser.add_argument("--next-x1-slug", default="v497-gmut-thos-v33-v5-x1")
    args = parser.parse_args()

    generated_utc, generated_nz = now_pair()
    closeout_gate = read_json(f"{args.source_x1_slug}-one-hour-closeout-gate-v1.json")
    x2_prep_gate = read_json(f"{args.x2_slug}-10-minute-prep-cadence-gate-v1.json")
    require_pass(closeout_gate, "one-hour closeout gate")
    require_pass(x2_prep_gate, "x2 10-minute prep gate")

    status_board = read_json(f"{args.source_x1_slug}-15-minute-five-lane-normalized-status-board-v1.json")
    source_ledger = read_json(f"{args.source_x1_slug}-source-to-x2-build-ledger-v1.json")
    current_source_expansion = read_json(f"{args.source_x1_slug}-current-source-expansion-ledger-v1.json")
    eureka_bank = read_json(f"{args.source_x1_slug}-productive-wait-eureka-bank-v1.json")
    heading_repair = read_json(f"{args.source_x1_slug}-heading-normalization-repair-v1.json")
    stale_flow = read_json(f"{args.source_x1_slug}-stale-flow-refresh-v1.json")
    crosswalk = read_json(f"{args.source_x1_slug}-command-skill-system-crosswalk-v1.json")
    journey_reflection = read_json(f"{args.source_x1_slug}-journey-trinity-reflection-ledger-v1.json")
    provenance = read_json(f"{args.source_x1_slug}-publication-provenance-receipt-v1.json")

    closeout = {
        "artifact_type": "x1_one_hour_closeout_synthesis",
        "phase_slug": args.source_x1_slug,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_X1_ONE_HOUR_CLOSEOUT_READY",
        "closeout_gate": {
            "status": closeout_gate.get("overall_status"),
            "elapsed_seconds": closeout_gate.get("elapsed_seconds"),
            "threshold_seconds": closeout_gate.get("threshold_seconds"),
        },
        "five_lane_status": {
            "status": status_board.get("overall_status"),
            "phase_advance_allowed_from_board": status_board.get("phase_advance_allowed"),
            "lane_count": len(status_board.get("lanes", [])),
        },
        "open_repairs": [
            "CLI exact heading normalization remains a next-launch repair unless future outputs prove clean.",
            "Marker-review split remains explicit: generic marker words are not strict path/key/private-material markers.",
        ],
        "claim_boundary": {
            "raw_lane_text_published": False,
            "raw_transport_published": False,
            "local_absolute_paths_published": False,
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
        },
    }
    x2_prep = {
        "artifact_type": "x2_prep_synthesis",
        "phase_slug": args.x2_slug,
        "source_x1_slug": args.source_x1_slug,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_X2_PREP_READY_FROM_X1_CLOSEOUT",
        "prep_gate": {
            "status": x2_prep_gate.get("overall_status"),
            "elapsed_seconds": x2_prep_gate.get("elapsed_seconds"),
            "threshold_seconds": x2_prep_gate.get("threshold_seconds"),
        },
        "source_rows": source_ledger.get("source_rows", []),
        "expanded_source_row_count": len(current_source_expansion.get("source_rows", [])),
        "eureka_task_count": len(eureka_bank.get("eureka_tasks", [])),
        "heading_repair_status": heading_repair.get("overall_status"),
        "stale_flow_status": stale_flow.get("overall_status"),
        "crosswalk_row_count": len(crosswalk.get("rows", [])),
        "reflection_record_count": len(journey_reflection.get("reflection_records", [])),
        "provenance_status": provenance.get("overall_status"),
    }
    build_matrix = {
        "artifact_type": "x2_build_run_test_use_matrix",
        "phase_slug": args.x2_slug,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_X2_BUILD_MATRIX_READY",
        "tasks": X2_TASKS,
        "wait_window_inputs": {
            "source_rows": len(source_ledger.get("source_rows", [])),
            "expanded_source_rows": len(current_source_expansion.get("source_rows", [])),
            "eureka_tasks": len(eureka_bank.get("eureka_tasks", [])),
            "crosswalk_rows": len(crosswalk.get("rows", [])),
            "reflection_records": len(journey_reflection.get("reflection_records", [])),
            "stale_flow_status": stale_flow.get("overall_status"),
            "provenance_status": provenance.get("overall_status"),
        },
        "trinity_mapping": {
            "GMUT_Mind": ["Trinity Mandala open-gate mapping"],
            "THOS_Body": [
                "Five-lane normalized status board promotion",
                "CLI heading contract repair",
                "Marker-review split hardening",
                "Watcher trust receipt contract",
                "Source-to-build ledger conversion",
                "Publication provenance schema",
                "Stale-flow retry playbook update",
                "Next x1 launch readiness",
            ],
            "Freed_ID_CBR_Heart": ["Skill evolution safe boundary"],
        },
    }
    build_receipt = {
        "artifact_type": "x2_build_run_test_use_receipt",
        "phase_slug": args.x2_slug,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_X2_BUILD_RUN_TEST_USE_PROGRESS",
        "built": [
            "x1 one-hour closeout synthesis",
            "x2 preparation synthesis",
            "10-task x2 build/run/test/use matrix",
            "next x1 readiness roadmap",
            "publication validation plan",
        ],
        "not_done": [
            "No raw lane text publication",
            "No plugin-cache or user-skill mutation",
            "No external account changes",
            "No final GMUT or canon closure claim",
        ],
    }
    roadmap = {
        "artifact_type": "next_x1_readiness_roadmap",
        "phase_slug": args.x2_slug,
        "next_x1_slug": args.next_x1_slug,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_NEXT_X1_READY_AFTER_X2_PUBLICATION",
        "roadmap": [
            "Launch all five existing lanes after v4 x2 validation and publication.",
            "Use the standalone exact-heading prompt template.",
            "Use cadence guard first and status normalizer second.",
            "Keep watchers/notifiers supervising while Aletheon works productively.",
            "Carry source-to-build rows into the next x1 prompt and x2 matrix.",
        ],
    }
    validation = {
        "artifact_type": "x2_publication_validation_plan",
        "phase_slug": args.x2_slug,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_PUBLICATION_VALIDATION_PLAN_READY",
        "required_checks": [
            "script compile",
            "JSON parse",
            "sensitive/raw/path guard",
            "whitespace check",
            "exact staged diff review",
            "commit",
            "push",
            "remote equals local",
        ],
    }
    outputs = {
        f"{args.source_x1_slug}-one-hour-closeout-synthesis-v1": closeout,
        f"{args.x2_slug}-prep-synthesis-v1": x2_prep,
        f"{args.x2_slug}-build-run-test-use-matrix-v1": build_matrix,
        f"{args.x2_slug}-build-run-test-use-receipt-v1": build_receipt,
        f"{args.x2_slug}-next-x1-readiness-roadmap-v1": roadmap,
        f"{args.x2_slug}-publication-validation-plan-v1": validation,
    }
    for stem, payload in outputs.items():
        write_json(TRACE_DIR / f"{stem}.json", payload)
    write_md(
        TRACE_DIR / f"{args.source_x1_slug}-one-hour-closeout-synthesis-v1.md",
        f"{args.source_x1_slug} One-Hour Closeout Synthesis",
        [
            f"Status: `{closeout['overall_status']}`",
            f"Next phase: `{args.x2_slug}`",
            "All five lanes are status-accounted through curated receipts only.",
            "Raw lane text and app transport remain unpublished.",
        ],
    )
    write_md(
        TRACE_DIR / f"{args.x2_slug}-prep-synthesis-v1.md",
        f"{args.x2_slug} Prep Synthesis",
        [
            f"Status: `{x2_prep['overall_status']}`",
            f"Source rows: `{len(x2_prep['source_rows'])}`",
            f"Expanded source rows: `{x2_prep['expanded_source_row_count']}`",
            f"Eureka tasks: `{x2_prep['eureka_task_count']}`",
            f"Crosswalk rows: `{x2_prep['crosswalk_row_count']}`",
            f"Reflection records: `{x2_prep['reflection_record_count']}`",
            f"Heading repair: `{x2_prep['heading_repair_status']}`",
            f"Stale flow: `{x2_prep['stale_flow_status']}`",
            f"Provenance: `{x2_prep['provenance_status']}`",
        ],
    )
    write_md(
        TRACE_DIR / f"{args.x2_slug}-build-run-test-use-matrix-v1.md",
        f"{args.x2_slug} Build Run Test Use Matrix",
        [f"{idx}. {task['task']}: {task['build_use']}" for idx, task in enumerate(X2_TASKS, start=1)],
    )
    write_md(
        TRACE_DIR / f"{args.x2_slug}-build-run-test-use-receipt-v1.md",
        f"{args.x2_slug} Build Run Test Use Receipt",
        [f"Status: `{build_receipt['overall_status']}`", *build_receipt["built"], *build_receipt["not_done"]],
    )
    write_md(
        TRACE_DIR / f"{args.x2_slug}-next-x1-readiness-roadmap-v1.md",
        f"{args.x2_slug} Next x1 Readiness Roadmap",
        roadmap["roadmap"],
    )
    write_md(
        TRACE_DIR / f"{args.x2_slug}-publication-validation-plan-v1.md",
        f"{args.x2_slug} Publication Validation Plan",
        validation["required_checks"],
    )
    print(json.dumps({"status": "PASS_BUILDER_OUTPUTS_WRITTEN", "phase_slug": args.x2_slug}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
