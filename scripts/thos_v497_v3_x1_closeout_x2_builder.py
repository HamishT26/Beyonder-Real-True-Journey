#!/usr/bin/env python3
"""Build v497 v3 x1 closeout and v497 v3 x2 artifacts after the one-hour gate."""

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
        "task": "Cadence-first harvest runner hardening",
        "build_use": "Convert the self-correction into a runner invariant: cadence guard must pass before any status harvest.",
        "validation": "Closeout receipts show guard-first ordering and no early manual lane status decisions.",
    },
    {
        "task": "Arby prompt transport hardening",
        "build_use": "Carry the single-line structure-repair prompt pattern into future CLI repair lanes.",
        "validation": "Future repair launch receipts record no newline-truncated heading contract.",
    },
    {
        "task": "Five-lane closeout synthesis card",
        "build_use": "Fuse app-lane completion, CLI quality gates, source ledgers, and one-hour maturity into a single closeout artifact.",
        "validation": "All five lanes status-accounted; raw lane text and app transport remain unpublished.",
    },
    {
        "task": "Watcher trust policy fixture",
        "build_use": "Make watcher/notifier supervision explicit in each x1/x2 boundary artifact.",
        "validation": "Manual status checks before approved marks are recorded as false or self-corrected.",
    },
    {
        "task": "THOS command proposal queue",
        "build_use": "Transform x1 command proposals into receiver-safe diagnostics, guards, and source-ledger command candidates.",
        "validation": "Each candidate declares scope, mutation boundary, and pass/fail signal.",
    },
    {
        "task": "System expansion queue",
        "build_use": "Map watcher spans, guardrails, provenance, and identity-assurance ideas into THOS body modules.",
        "validation": "No plugin-cache, user-skill, or external account mutation is required.",
    },
    {
        "task": "Skill and micro-workflow candidate queue",
        "build_use": "Draft repo-scoped skill candidates for cadence ordering, CLI elaboration gating, and source-to-build traceability.",
        "validation": "Candidates remain documentation/receipt level until exact user-skill approval.",
    },
    {
        "task": "Freed ID/CBR assurance bridge",
        "build_use": "Keep identity work aligned to consent, assurance, credentials, privacy, recourse, and non-authoritarian governance.",
        "validation": "No identity proof, metaphysical proof, or rights-canon closure is claimed.",
    },
    {
        "task": "GMUT open-gate rubric",
        "build_use": "Sort GMUT work into source-backed, simulation-ready, comparator-needed, or speculative buckets.",
        "validation": "No final physics, consciousness, empirical, or canon claims appear in x2 artifacts.",
    },
    {
        "task": "v497 v4 x1 launch readiness",
        "build_use": "Prepare the next x1 prompts and watcher rules so all five lanes start with explicit structure from the beginning.",
        "validation": "v497 v4 x1 launch remains blocked until v497 v3 x2 publication is validated.",
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


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(path: Path, title: str, bullets: list[str]) -> None:
    lines = [f"# {title}", ""]
    lines.extend(f"- {item}" for item in bullets)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def require_pass(payload: dict[str, Any], label: str) -> None:
    if payload.get("overall_status") != "PASS_STATUS_CHECK_ALLOWED":
        raise SystemExit(f"{label} must be PASS_STATUS_CHECK_ALLOWED before closeout")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build v497 v3 x1 closeout and v497 v3 x2 synthesis artifacts.")
    parser.add_argument("--source-x1-slug", default="v497-gmut-thos-v33-v3-x1")
    parser.add_argument("--x2-slug", default="v497-gmut-thos-v33-v3-x2")
    parser.add_argument("--next-x1-slug", default="v497-gmut-thos-v33-v4-x1")
    args = parser.parse_args()

    generated_utc, generated_nz = now_pair()
    closeout_gate = read_json(f"{args.source_x1_slug}-one-hour-closeout-gate-v1.json")
    require_pass(closeout_gate, "one-hour closeout gate")
    x2_prep_gate = read_json(f"{args.x2_slug}-10-minute-prep-cadence-gate-v1.json")
    require_pass(x2_prep_gate, "x2 10-minute prep gate")
    first_status = read_json(f"{args.source_x1_slug}-first-status-synthesis-after-repair-v1.json")
    wait_ledger = read_json(f"{args.source_x1_slug}-productive-wait-source-reflection-ledger-v1.json")

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
            "cli_lanes": first_status.get("cli_lanes", []),
            "app_lanes": first_status.get("app_lanes", {}),
        },
        "source_and_reflection": {
            "search_queries_completed": wait_ledger.get("search_queries_completed", 0),
            "reflection_task_count": wait_ledger.get("reflection_task_count", 0),
        },
        "phase_transition": {
            "next_phase": args.x2_slug,
            "x2_allowed_after_publication": True,
        },
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
        "source_groups_reused": wait_ledger.get("source_groups", []),
        "x1_eureka_wait_tasks": wait_ledger.get("eureka_wait_tasks", []),
        "prep_boundary": {
            "minimum_10_minute_x2_prep_required": True,
            "minimum_10_minute_x2_prep_status": x2_prep_gate.get("overall_status"),
            "minimum_10_minute_x2_prep_elapsed_seconds": x2_prep_gate.get("elapsed_seconds"),
            "status_check_before_prep_mark_allowed": False,
        },
    }
    build_matrix = {
        "artifact_type": "x2_build_run_test_use_matrix",
        "phase_slug": args.x2_slug,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_X2_BUILD_MATRIX_READY",
        "tasks": X2_TASKS,
        "trinity_mapping": {
            "GMUT_Mind": ["GMUT open-gate rubric"],
            "THOS_Body": [
                "Cadence-first harvest runner hardening",
                "Arby prompt transport hardening",
                "Five-lane closeout synthesis card",
                "Watcher trust policy fixture",
                "THOS command proposal queue",
                "System expansion queue",
                "v497 v4 x1 launch readiness",
            ],
            "Freed_ID_CBR_Heart": ["Freed ID/CBR assurance bridge", "Skill and micro-workflow candidate queue"],
        },
    }
    build_receipt = {
        "artifact_type": "x2_build_run_test_use_receipt",
        "phase_slug": args.x2_slug,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_X2_BUILD_RUN_TEST_USE_PROGRESS",
        "built": [
            "one-hour x1 closeout synthesis",
            "x2 preparation synthesis",
            "10-task x2 build/run/test/use matrix",
            "next v497 v4 x1 readiness roadmap",
            "publication validation plan",
        ],
        "tested": [
            "script compile required before commit",
            "JSON parse required before commit",
            "sensitive/raw/path guard required before commit",
            "remote-equals-local verification required after push",
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
            "Launch all five existing lanes at v497 v4 x1 only after v497 v3 x2 validation and publication.",
            "Use strict heading contracts from the first prompt.",
            "Use cadence guard first and harvest second.",
            "Keep watchers/notifiers supervising until approved marks.",
            "Carry x2 build matrix tasks into the next x1 prompts.",
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
    write_md(TRACE_DIR / f"{args.source_x1_slug}-one-hour-closeout-synthesis-v1.md", f"{args.source_x1_slug} One-Hour Closeout Synthesis", [
        f"Status: `{closeout['overall_status']}`",
        f"Next phase: `{args.x2_slug}`",
        "All five lanes are status-accounted; raw lane text and app transport remain unpublished.",
    ])
    write_md(TRACE_DIR / f"{args.x2_slug}-prep-synthesis-v1.md", f"{args.x2_slug} Prep Synthesis", [
        f"Status: `{x2_prep['overall_status']}`",
        "X2 build uses x1 closeout evidence, source groups, and eureka wait tasks.",
    ])
    write_md(TRACE_DIR / f"{args.x2_slug}-build-run-test-use-matrix-v1.md", f"{args.x2_slug} Build Run Test Use Matrix", [
        f"Status: `{build_matrix['overall_status']}`",
        "Task count: `10`",
    ])
    write_md(TRACE_DIR / f"{args.x2_slug}-build-run-test-use-receipt-v1.md", f"{args.x2_slug} Build Run Test Use Receipt", [
        f"Status: `{build_receipt['overall_status']}`",
        "Built closeout, prep, matrix, roadmap, and validation artifacts.",
    ])
    write_md(TRACE_DIR / f"{args.x2_slug}-next-x1-readiness-roadmap-v1.md", f"{args.x2_slug} Next x1 Readiness Roadmap", [
        f"Status: `{roadmap['overall_status']}`",
        f"Next x1: `{args.next_x1_slug}`",
    ])
    write_md(TRACE_DIR / f"{args.x2_slug}-publication-validation-plan-v1.md", f"{args.x2_slug} Publication Validation Plan", [
        f"Status: `{validation['overall_status']}`",
        "Exact publication only.",
    ])
    print(json.dumps({"status": "ok", "outputs": len(outputs) * 2}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
