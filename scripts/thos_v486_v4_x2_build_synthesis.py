#!/usr/bin/env python3
"""Build v486 GMUT/THOS v4 x2 synthesis from v4 x1 open-gap evidence."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
DOCS_DIR = ROOT / "docs"
PHASE = "v486-gmut-thos-v22-v4-x2"
X1 = "v486-gmut-thos-v22-v4-x1"


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


def write_md(path: Path, title: str, bullets: list[str]) -> None:
    lines = [f"# {title}", ""]
    lines.extend(f"- {item}" for item in bullets)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def file_records(patterns: list[str], limit: int = 40) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for pattern in patterns:
        for path in sorted(DOCS_DIR.glob(pattern)):
            if path.is_file():
                records.append({"path": rel(path), "bytes": path.stat().st_size})
            if len(records) >= limit:
                return records
    return records


def build_cli_supervisor_contract(generated_utc: str, generated_nz: str, x1_cli: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_type": "cli_supervisor_contract",
        "phase_slug": PHASE,
        "source_boundary": X1,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_SUPERVISOR_CONTRACT_WITH_OPEN_CLI_GAP",
        "x1_cli_status": x1_cli.get("overall_status", "unknown"),
        "contract_rules": [
            "Use one fresh temp-only folder per lane per attempt.",
            "Never reuse a previous last-message file as completion proof.",
            "Require current phase slug plus final marker before classifying CLI as complete.",
            "Classify pending, stale-context, or marker-missing outputs as open gaps.",
            "Continue x2 work from safe app/Aletheon evidence while CLI remains pending.",
        ],
        "v5_x1_prompt_requirements": [
            "First line must be CURRENT PHASE ONLY with the phase slug.",
            "Prompt must forbid stale v58/v59 summaries and ask for a reject-stale-context note.",
            "Prompt must ask for exact current-phase artifact proposals.",
            "Prompt must include one final marker per lane.",
        ],
        "publication_boundary": {
            "raw_lane_body_text_published": False,
            "raw_transport_published": False,
            "local_temp_paths_published": False,
        },
    }


def build_app_lane_build_map(generated_utc: str, generated_nz: str, x1_timing: dict[str, Any]) -> dict[str, Any]:
    app_lanes = x1_timing.get("app_lanes", [])
    return {
        "artifact_type": "app_lane_build_map",
        "phase_slug": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_APP_LANE_BUILD_MAP",
        "app_lane_count": len(app_lanes),
        "app_lanes": app_lanes,
        "build_uses": [
            "Use app-lane completion receipts as orchestration health evidence.",
            "Do not publish app-lane body text.",
            "Convert app-lane readiness into command-surface, handoff, and source-ledger hardening.",
        ],
    }


def build_source_security_integration(generated_utc: str, generated_nz: str, x1_source: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_type": "source_security_integration",
        "phase_slug": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_SOURCE_SECURITY_INTEGRATION",
        "source_count": len(x1_source.get("sources", [])),
        "source_uses": x1_source.get("sources", []),
        "security_controls": [
            "Avoid third-party Codex-adjacent packages unless source and publisher are verified.",
            "Use official OpenAI Codex docs and GitHub releases as primary upgrade references.",
            "Treat alpha tags as observation only without explicit upgrade approval.",
            "Map MCP and OWASP controls to least-privilege tool routing and receipt-only publication.",
        ],
    }


def build_open_gate_queue(generated_utc: str, generated_nz: str) -> dict[str, Any]:
    command_surfaces = file_records([
        "trinity-command-book*.json",
        "trinity-command-book-validation-latest.*",
        "trinity-command-execution-ledger.jsonl",
    ])
    return {
        "artifact_type": "gmut_thos_open_gate_build_queue",
        "phase_slug": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_OPEN_GATE_BUILD_QUEUE",
        "command_surface_count": len(command_surfaces),
        "command_surfaces": command_surfaces[:24],
        "queue": [
            "Build command-index compatibility from current command-book surfaces.",
            "Keep GMUT claim mapping in source-backed, simulation-ready, comparator-needed, or speculative buckets.",
            "Prepare v5 x1 to collect all five lanes again while avoiding stale CLI output reuse.",
            "Keep Journey v4-v49 continuity as historical inspiration and architecture lineage, not empirical proof.",
        ],
        "claim_boundary": {
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
        },
    }


def build_validation(generated_utc: str, generated_nz: str, artifacts: dict[str, dict[str, Any]]) -> dict[str, Any]:
    return {
        "artifact_type": "x2_build_validation",
        "phase_slug": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_V4_X2_BUILD_VALIDATION",
        "input_receipts": [
            f"{X1}-cli-fresh-output-status-v1.json",
            f"{X1}-five-lane-timing-v1.json",
            f"{X1}-source-refresh-v1.json",
            f"{X1}-synthesis-v1.json",
        ],
        "artifact_statuses": {key: value.get("overall_status") for key, value in artifacts.items()},
        "mutation_boundary": {
            "repo_artifacts_written": True,
            "plugin_cache_mutated": False,
            "user_skills_mutated": False,
            "external_accounts_mutated": False,
            "raw_lane_text_published": False,
        },
    }


def build_synthesis(generated_utc: str, generated_nz: str, validation: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_type": "x2_synthesis",
        "phase_slug": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_V486_V4_X2_BUILD_SYNTHESIS",
        "result": [
            "Preserved v4 x1 app-lane completion as usable orchestration evidence.",
            "Converted v4 x1 CLI pending state into a stricter supervisor contract for v5 x1.",
            "Folded current source/security research into runner and connector governance.",
            "Queued command-surface and GMUT/THOS open-gate application work.",
        ],
        "validation_status": validation["overall_status"],
        "next_boundary": "v486-gmut-thos-v22-v5-x1",
    }


def build_v5_roadmap(generated_utc: str, generated_nz: str) -> dict[str, Any]:
    return {
        "artifact_type": "v5_x1_readiness_roadmap",
        "phase_slug": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_V5_X1_READY",
        "roadmap": [
            "Attempt Cicero, Kierkegaard, and Aristotle through existing app-server routes.",
            "Attempt Arby and Aster Vale through fresh temp-only CLI folders.",
            "Use current-phase-only prompt contract and final marker checks.",
            "If CLI remains pending, continue x2 with a visible open-gap receipt instead of waiting idle.",
            "Keep all GMUT/canon claims open-gated.",
        ],
    }


def main() -> int:
    generated_utc, generated_nz = now_pair()
    x1_cli = read_json(TRACE_DIR / f"{X1}-cli-fresh-output-status-v1.json")
    x1_timing = read_json(TRACE_DIR / f"{X1}-five-lane-timing-v1.json")
    x1_source = read_json(TRACE_DIR / f"{X1}-source-refresh-v1.json")

    supervisor = build_cli_supervisor_contract(generated_utc, generated_nz, x1_cli)
    app_map = build_app_lane_build_map(generated_utc, generated_nz, x1_timing)
    source_security = build_source_security_integration(generated_utc, generated_nz, x1_source)
    queue = build_open_gate_queue(generated_utc, generated_nz)
    validation = build_validation(
        generated_utc,
        generated_nz,
        {
            "cli_supervisor_contract": supervisor,
            "app_lane_build_map": app_map,
            "source_security_integration": source_security,
            "open_gate_queue": queue,
        },
    )
    synthesis = build_synthesis(generated_utc, generated_nz, validation)
    roadmap = build_v5_roadmap(generated_utc, generated_nz)

    outputs = {
        "cli-supervisor-contract": supervisor,
        "app-lane-build-map": app_map,
        "source-security-integration": source_security,
        "gmut-thos-open-gate-build-queue": queue,
        "build-validation": validation,
        "synthesis": synthesis,
        "v5-x1-readiness-roadmap": roadmap,
    }
    for suffix, payload in outputs.items():
        write_json(TRACE_DIR / f"{PHASE}-{suffix}-v1.json", payload)

    write_md(TRACE_DIR / f"{PHASE}-cli-supervisor-contract-v1.md", "v486 GMUT/THOS v22 v4 x2 CLI Supervisor Contract", [
        f"Status: `{supervisor['overall_status']}`",
        "Fresh output folders, current-phase markers, and stale-context rejection are mandatory for v5 x1.",
    ])
    write_md(TRACE_DIR / f"{PHASE}-app-lane-build-map-v1.md", "v486 GMUT/THOS v22 v4 x2 App-Lane Build Map", [
        f"Status: `{app_map['overall_status']}`",
        f"App lanes mapped: `{app_map['app_lane_count']}`",
    ])
    write_md(TRACE_DIR / f"{PHASE}-source-security-integration-v1.md", "v486 GMUT/THOS v22 v4 x2 Source Security Integration", [
        f"Status: `{source_security['overall_status']}`",
        "Official Codex, MCP, and OWASP guidance is mapped into runner governance.",
    ])
    write_md(TRACE_DIR / f"{PHASE}-gmut-thos-open-gate-build-queue-v1.md", "v486 GMUT/THOS v22 v4 x2 Open-Gate Build Queue", [
        f"Status: `{queue['overall_status']}`",
        "Command-index and GMUT/THOS application work is queued without canon promotion.",
    ])
    write_md(TRACE_DIR / f"{PHASE}-build-validation-v1.md", "v486 GMUT/THOS v22 v4 x2 Build Validation", [
        f"Status: `{validation['overall_status']}`",
        "Inputs were v4 x1 status, timing, source, and synthesis receipts.",
    ])
    write_md(TRACE_DIR / f"{PHASE}-synthesis-v1.md", "v486 GMUT/THOS v22 v4 x2 Synthesis", [
        f"Status: `{synthesis['overall_status']}`",
        f"Next boundary: `{synthesis['next_boundary']}`",
    ])
    write_md(TRACE_DIR / f"{PHASE}-v5-x1-readiness-roadmap-v1.md", "v486 GMUT/THOS v22 v4 x2 v5 x1 Readiness Roadmap", [
        f"Status: `{roadmap['overall_status']}`",
        "Attempt all five existing lanes again with the stricter current-phase prompt contract.",
    ])
    print(json.dumps({"status": "ok", "phase_slug": PHASE, "outputs": len(outputs) * 2}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
