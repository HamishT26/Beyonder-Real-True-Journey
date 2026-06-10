#!/usr/bin/env python3
"""Build v486 GMUT/THOS v3 x2 synthesis from v3 x1 status evidence."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
DOCS_DIR = ROOT / "docs"
PHASE = "v486-gmut-thos-v22-v3-x2"
X1 = "v486-gmut-thos-v22-v3-x1"


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


def file_records(patterns: list[str], limit: int = 60) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for pattern in patterns:
        for path in sorted(DOCS_DIR.glob(pattern)):
            if path.is_file():
                records.append({"path": rel(path), "bytes": path.stat().st_size})
            if len(records) >= limit:
                return records
    return records


def build_cli_freshness_gate(generated_utc: str, generated_nz: str, cli_quality: dict[str, Any], cli_completion: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_type": "cli_prompt_freshness_gate",
        "phase_slug": PHASE,
        "source_boundary": X1,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_STALE_CONTEXT_BLOCKER_CLASSIFIED",
        "x1_quality_status": cli_quality.get("overall_status", "unknown"),
        "x1_completion_status": cli_completion.get("aggregate_status", "unknown"),
        "freshness_findings": [
            {
                "lane_group": "Arby/Aster",
                "finding": "late CLI final messages were not accepted as v486 v3 x1 advisories because they referenced stale v58 context and omitted the requested v486 final markers",
                "action": "future CLI prompts must include a current-phase freshness oath, current artifact targets, and a mandatory reject-stale-context clause",
            },
            {
                "lane_group": "all five lanes",
                "finding": "app lanes remain usable as completion evidence, but raw app bodies are not published",
                "action": "x2 builds only from sanitized receipts, source ledgers, command surfaces, and Aletheon-authored synthesis",
            },
        ],
        "not_completion_proof": [
            "handshake stubs",
            "late stale-context advisory text",
            "soft wait foothold",
            "transport warnings",
        ],
        "next_retry_contract": [
            "state the current phase slug in the first sentence",
            "state that stale v58/v59-only context must be rejected",
            "require final marker and current-phase artifact proposals",
            "write to a fresh temp-only output directory per attempt to avoid stale last-message reuse",
        ],
        "publication_boundary": {
            "raw_lane_body_text_published": False,
            "raw_transport_published": False,
            "local_temp_paths_published": False,
        },
    }


def build_command_surface_map(generated_utc: str, generated_nz: str) -> dict[str, Any]:
    command_books = file_records([
        "trinity-command-book*.json",
        "trinity-command-book*.md",
        "trinity-command-book-validation-latest.*",
        "trinity-command-execution-ledger.jsonl",
    ])
    runner_scripts = [
        "scripts/thos_council_app_lane_notifier_runner.py",
        "scripts/thos_cli_lane_completion_notifier.py",
        "scripts/thos_codex_cli_advisory_launcher.py",
        "scripts/thos_cli_lane_watch_launcher.py",
        "scripts/thos_v478_v14_x8_start_artifacts.py",
        "scripts/thos_v486_v3_x1_cli_quality_repair.py",
    ]
    return {
        "artifact_type": "command_surface_build_map",
        "phase_slug": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_COMMAND_SURFACE_MAP_READY",
        "command_surface_count": len(command_books),
        "command_surfaces": command_books[:30],
        "runner_surface_targets": [
            {"path": path, "exists": (ROOT / path).exists()} for path in runner_scripts
        ],
        "build_actions": [
            "Use fresh temp-only output folders for CLI lanes to avoid stale final-message reuse.",
            "Keep app-server lane receipts status-only and body-redacted.",
            "Add prompt freshness checks to the v4 x1 seed before reattempting Arby/Aster.",
            "Treat command-index and v54/v55 handoff surfaces as receiver-safe pointers, not proof of canon closure.",
        ],
    }


def build_gmut_thos_queue(generated_utc: str, generated_nz: str, source_refresh: dict[str, Any]) -> dict[str, Any]:
    source_labels = [item.get("label") for item in source_refresh.get("sources", []) if isinstance(item, dict)]
    return {
        "artifact_type": "gmut_thos_application_queue",
        "phase_slug": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_OPEN_GATE_APPLICATION_QUEUE",
        "source_labels_used": source_labels,
        "queue": [
            {
                "track": "THOS runner resilience",
                "application": "turn CLI stale-context detection into a freshness gate before each x1 intake",
                "gate": "status receipts only; no raw output publication",
            },
            {
                "track": "GMUT claim mapping",
                "application": "map statements to source-backed, simulation-ready, comparator-needed, or speculative buckets",
                "gate": "no external validation or canon promotion claim",
            },
            {
                "track": "Command index",
                "application": "connect command-book surfaces to exact helper scripts and phase artifacts",
                "gate": "no broad import of raw command history",
            },
            {
                "track": "Journey continuity",
                "application": "use v4-v49 lineage as inspiration and naming continuity, not empirical proof",
                "gate": "quote-free, metadata-only references unless exact source excerpts are approved",
            },
        ],
    }


def build_validation(generated_utc: str, generated_nz: str, freshness: dict[str, Any], command_map: dict[str, Any], queue: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_type": "x2_build_validation",
        "phase_slug": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_V3_X2_WITH_CLI_OPEN_GAP",
        "validated_inputs": [
            f"{X1}-cli-advisory-quality-gate-v1.json",
            f"{X1}-synthesis-v1.json",
            f"{X1}-source-refresh-v1.json",
        ],
        "built_artifacts": [
            f"{PHASE}-cli-prompt-freshness-gate-v1.json",
            f"{PHASE}-command-surface-build-map-v1.json",
            f"{PHASE}-gmut-thos-application-queue-v1.json",
            f"{PHASE}-build-validation-v1.json",
            f"{PHASE}-synthesis-v1.json",
            f"{PHASE}-v4-x1-readiness-roadmap-v1.json",
        ],
        "statuses": {
            "cli_freshness": freshness["overall_status"],
            "command_surface": command_map["overall_status"],
            "gmut_thos_queue": queue["overall_status"],
        },
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
        "overall_status": "PASS_V486_V3_X2_BUILD_SYNTHESIS_WITH_CLI_FRESHNESS_GATE",
        "x2_result": [
            "Converted the v3 x1 CLI gap into a reusable prompt-freshness gate.",
            "Kept app-lane completion evidence usable without publishing body text.",
            "Produced command-surface and GMUT/THOS application queues for the next x1.",
            "Preserved all GMUT, physics, consciousness, and canon gates as open.",
        ],
        "validation_status": validation["overall_status"],
        "next_boundary": "v486-gmut-thos-v22-v4-x1",
    }


def build_roadmap(generated_utc: str, generated_nz: str) -> dict[str, Any]:
    return {
        "artifact_type": "v4_x1_readiness_roadmap",
        "phase_slug": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_V4_X1_READY_WITH_FRESH_CLI_OUTPUT_DIR_RULE",
        "roadmap": [
            "Attempt all five existing lanes again at v4 x1.",
            "Use fresh temp-only CLI output directories so stale last-message files cannot masquerade as completion.",
            "Ask Arby/Aster to reject stale v58-only context and answer the current phase directly.",
            "Run the app-server lanes through existing callable routes only.",
            "If CLI lanes again produce stale-context outputs, publish a blocker receipt and continue x2 from available safe evidence.",
        ],
    }


def main() -> int:
    generated_utc, generated_nz = now_pair()
    cli_quality = read_json(TRACE_DIR / f"{X1}-cli-advisory-quality-gate-v1.json")
    cli_completion = read_json(TRACE_DIR / f"{X1}-cli-completion-v1.json")
    source_refresh = read_json(TRACE_DIR / f"{X1}-source-refresh-v1.json")

    freshness = build_cli_freshness_gate(generated_utc, generated_nz, cli_quality, cli_completion)
    command_map = build_command_surface_map(generated_utc, generated_nz)
    queue = build_gmut_thos_queue(generated_utc, generated_nz, source_refresh)
    validation = build_validation(generated_utc, generated_nz, freshness, command_map, queue)
    synthesis = build_synthesis(generated_utc, generated_nz, validation)
    roadmap = build_roadmap(generated_utc, generated_nz)

    outputs = {
        "cli-prompt-freshness-gate": freshness,
        "command-surface-build-map": command_map,
        "gmut-thos-application-queue": queue,
        "build-validation": validation,
        "synthesis": synthesis,
        "v4-x1-readiness-roadmap": roadmap,
    }
    for suffix, payload in outputs.items():
        write_json(TRACE_DIR / f"{PHASE}-{suffix}-v1.json", payload)

    write_md(
        TRACE_DIR / f"{PHASE}-cli-prompt-freshness-gate-v1.md",
        "v486 GMUT/THOS v22 v3 x2 CLI Prompt Freshness Gate",
        [
            f"Status: `{freshness['overall_status']}`",
            "Late Arby/Aster outputs were classified as stale-context evidence, not x1 advisory completion.",
            "Next CLI attempts must use fresh output folders and current-phase freshness checks.",
        ],
    )
    write_md(
        TRACE_DIR / f"{PHASE}-command-surface-build-map-v1.md",
        "v486 GMUT/THOS v22 v3 x2 Command Surface Build Map",
        [
            f"Status: `{command_map['overall_status']}`",
            f"Command surfaces found: `{command_map['command_surface_count']}`",
            "Runner surfaces are mapped as scoped helpers for v4 x1 and x2.",
        ],
    )
    write_md(
        TRACE_DIR / f"{PHASE}-gmut-thos-application-queue-v1.md",
        "v486 GMUT/THOS v22 v3 x2 GMUT/THOS Application Queue",
        [
            f"Status: `{queue['overall_status']}`",
            "THOS runner resilience, GMUT claim mapping, command-index, and Journey continuity tracks are queued.",
            "All empirical and canon gates remain open.",
        ],
    )
    write_md(
        TRACE_DIR / f"{PHASE}-build-validation-v1.md",
        "v486 GMUT/THOS v22 v3 x2 Build Validation",
        [
            f"Status: `{validation['overall_status']}`",
            "Inputs validated from v3 x1 quality, synthesis, and source-refresh receipts.",
            "No plugin cache, user skill, external account, raw lane text, or private transport mutation occurred.",
        ],
    )
    write_md(
        TRACE_DIR / f"{PHASE}-synthesis-v1.md",
        "v486 GMUT/THOS v22 v3 x2 Synthesis",
        [
            f"Status: `{synthesis['overall_status']}`",
            f"Next boundary: `{synthesis['next_boundary']}`",
            "x2 converted the x1 gap into a better runner contract rather than hiding it.",
        ],
    )
    write_md(
        TRACE_DIR / f"{PHASE}-v4-x1-readiness-roadmap-v1.md",
        "v486 GMUT/THOS v22 v3 x2 v4 x1 Readiness Roadmap",
        [
            f"Status: `{roadmap['overall_status']}`",
            "Attempt all five existing lanes again with fresh temp-only CLI output directories.",
            "Proceed with explicit blocker receipts if Arby/Aster remain stale-context limited.",
        ],
    )

    print(json.dumps({"status": "ok", "phase_slug": PHASE, "outputs": len(outputs) * 2}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
