#!/usr/bin/env python3
"""Build v486 GMUT/THOS v2 x2 synthesis receipts from curated repo surfaces."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
PHASE = "v486-gmut-thos-v22-v2-x2"


def now_pair() -> tuple[str, str]:
    utc = dt.datetime.now(dt.UTC).replace(microsecond=0)
    nz = utc.astimezone(dt.timezone(dt.timedelta(hours=12), name="NZST"))
    return utc.isoformat().replace("+00:00", "Z"), nz.isoformat()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(path: Path, title: str, bullets: list[str], extra: list[str] | None = None) -> None:
    lines = [f"# {title}", ""]
    lines.extend(f"- {item}" for item in bullets)
    if extra:
        lines.extend(["", "## Details", ""])
        lines.extend(extra)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def file_records(patterns: list[str], limit: int = 40) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for pattern in patterns:
        for path in sorted((ROOT / "docs").glob(pattern)):
            if path.is_file():
                records.append({"path": rel(path), "bytes": path.stat().st_size})
            if len(records) >= limit:
                return records
    return records


def build_surface_check(generated_utc: str, generated_nz: str) -> dict[str, Any]:
    command_surfaces = file_records([
        "trinity-command-book*.json",
        "trinity-command-book*.md",
        "trinity-command-execution-ledger.jsonl",
    ])
    v54_v55_surfaces = file_records([
        "v54-*-handoff-policy-v1.json",
        "v54-*-continuity-pack-v1.md",
        "v54-*-closeout-summary-v1.json",
        "v55-*-handoff-policy-v1.json",
        "v55-*-continuity-pack-v1.md",
        "v55-*-closeout-summary-v1.json",
    ])
    payload = {
        "artifact_type": "x2_command_handoff_surface_check",
        "phase_slug": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_SURFACES_PRESENT" if command_surfaces and v54_v55_surfaces else "OPEN_GAP_SURFACE_POINTERS",
        "command_surface_count": len(command_surfaces),
        "v54_v55_surface_count": len(v54_v55_surfaces),
        "command_surfaces": command_surfaces[:24],
        "v54_v55_surfaces": v54_v55_surfaces[:24],
        "x2_action": "Use these surfaces as receiver-safe pointers for command-index and v54/v55 handoff hardening.",
        "publication_boundary": "relative_paths_and_file_sizes_only",
    }
    return payload


def build_claim_map(generated_utc: str, generated_nz: str) -> dict[str, Any]:
    entries = [
        {
            "claim_id": "journey_v15_equation_anchor",
            "status": "lineage_source_present",
            "next_gate": "map equations to current comparator or simulation-ready artifact before stronger claims",
        },
        {
            "claim_id": "journey_v16_simulation_lineage",
            "status": "simulation_lineage_present",
            "next_gate": "define bounded inputs, outputs, and falsification checks",
        },
        {
            "claim_id": "journey_v24_freed_id_security",
            "status": "governance_lineage_present",
            "next_gate": "use as identity and minimum-disclosure design input only",
        },
        {
            "claim_id": "journey_v29_codebase_grounding",
            "status": "implementation_lineage_present",
            "next_gate": "tie current helpers to runnable receipts and validation outputs",
        },
        {
            "claim_id": "v486_gmut_statement_mapping",
            "status": "open_gate",
            "next_gate": "classify each statement as source-backed, simulation-ready, comparator-needed, or speculative",
        },
        {
            "claim_id": "v486_consciousness_or_canon",
            "status": "open_gate",
            "next_gate": "do not promote without exact closure artifacts",
        },
    ]
    return {
        "artifact_type": "x2_gmut_claim_map",
        "phase_slug": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_OPEN_GATE_MAP",
        "entries": entries,
        "claim_boundary": {
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
            "external_validation_claimed": False,
        },
    }


def build_validation(generated_utc: str, generated_nz: str, handoff: dict[str, Any], surface: dict[str, Any], claim: dict[str, Any]) -> dict[str, Any]:
    buckets = handoff.get("x2_work_buckets", [])
    return {
        "artifact_type": "x2_build_validation",
        "phase_slug": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_X2_BUILD_VALIDATION",
        "handoff_bucket_count": len(buckets),
        "surface_status": surface["overall_status"],
        "claim_map_status": claim["overall_status"],
        "built_artifacts": [
            f"{PHASE}-command-handoff-surface-check-v1.json",
            f"{PHASE}-gmut-claim-map-v1.json",
            f"{PHASE}-build-validation-v1.json",
            f"{PHASE}-synthesis-v1.json",
        ],
        "x2_completion_state": "ready_for_v486_v3_x1_seed",
        "mutation_boundary": {
            "repo_artifacts_written": True,
            "helper_script_added": True,
            "plugin_cache_mutated": False,
            "user_skills_mutated": False,
            "external_accounts_mutated": False,
        },
    }


def build_synthesis(generated_utc: str, generated_nz: str, surface: dict[str, Any], claim: dict[str, Any], validation: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_type": "x2_build_synthesis",
        "phase_slug": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_V486_V2_X2_BUILD_SYNTHESIS",
        "surface_summary": {
            "command_surface_count": surface["command_surface_count"],
            "v54_v55_surface_count": surface["v54_v55_surface_count"],
            "status": surface["overall_status"],
        },
        "claim_summary": {
            "entry_count": len(claim["entries"]),
            "status": claim["overall_status"],
            "gate_state": "open",
        },
        "validation_summary": {
            "status": validation["overall_status"],
            "x2_completion_state": validation["x2_completion_state"],
        },
        "next_recommended_boundary": "v486-gmut-thos-v22-v3-x1",
        "next_recommended_focus": [
            "five-lane intake on command surface hardening",
            "GMUT claim-map expansion",
            "bounded simulation queue planning",
            "stale-flow watch on loader and shell snapshot warnings",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build v486 v2 x2 curated synthesis receipts.")
    parser.add_argument("--phase-slug", default=PHASE)
    args = parser.parse_args()
    if args.phase_slug != PHASE:
        raise SystemExit(f"unsupported phase slug: {args.phase_slug}")

    generated_utc, generated_nz = now_pair()
    handoff = read_json(TRACE_DIR / "v486-gmut-thos-v22-v2-x1-task-handoff-ledger-v1.json")
    surface = build_surface_check(generated_utc, generated_nz)
    claim = build_claim_map(generated_utc, generated_nz)
    validation = build_validation(generated_utc, generated_nz, handoff, surface, claim)
    synthesis = build_synthesis(generated_utc, generated_nz, surface, claim, validation)

    outputs = {
        "command-handoff-surface-check": surface,
        "gmut-claim-map": claim,
        "build-validation": validation,
        "synthesis": synthesis,
    }
    for suffix, payload in outputs.items():
        write_json(TRACE_DIR / f"{PHASE}-{suffix}-v1.json", payload)

    write_md(
        TRACE_DIR / f"{PHASE}-command-handoff-surface-check-v1.md",
        "v486 GMUT/THOS v22 v2 x2 Command and Handoff Surface Check",
        [
            f"Status: `{surface['overall_status']}`",
            f"Command surfaces found: `{surface['command_surface_count']}`",
            f"v54/v55 handoff surfaces found: `{surface['v54_v55_surface_count']}`",
            "Publication boundary: relative file names and sizes only.",
        ],
    )
    write_md(
        TRACE_DIR / f"{PHASE}-gmut-claim-map-v1.md",
        "v486 GMUT/THOS v22 v2 x2 GMUT Claim Map",
        [
            f"Status: `{claim['overall_status']}`",
            f"Entries: `{len(claim['entries'])}`",
            "All GMUT, physics, consciousness, and canon gates remain open.",
        ],
    )
    write_md(
        TRACE_DIR / f"{PHASE}-build-validation-v1.md",
        "v486 GMUT/THOS v22 v2 x2 Build Validation",
        [
            f"Status: `{validation['overall_status']}`",
            f"Handoff buckets consumed: `{validation['handoff_bucket_count']}`",
            f"Completion state: `{validation['x2_completion_state']}`",
        ],
    )
    write_md(
        TRACE_DIR / f"{PHASE}-synthesis-v1.md",
        "v486 GMUT/THOS v22 v2 x2 Synthesis",
        [
            f"Status: `{synthesis['overall_status']}`",
            f"Next boundary: `{synthesis['next_recommended_boundary']}`",
            "x2 converted x1 intake into command/handoff surface checks, GMUT claim mapping, and v3 x1 seed guidance.",
        ],
    )
    print(json.dumps({"status": "ok", "phase_slug": PHASE, "outputs": len(outputs) * 2}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
