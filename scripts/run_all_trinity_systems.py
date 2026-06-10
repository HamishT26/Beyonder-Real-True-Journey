#!/usr/bin/env python3
"""Run available Trinity systems and produce a consolidated markdown report."""

from __future__ import annotations

import argparse
import json
import shlex
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHARED_REPORT = ROOT / "docs" / "system-suite-run-report.md"
SHARED_STATUS_JSON = ROOT / "docs" / "system-suite-status.json"
V17_QUICK_REPORT = ROOT / "docs" / "v17-system-suite-run-report-latest.md"
V17_QUICK_STATUS_JSON = ROOT / "docs" / "v17-system-suite-status-latest.json"
SHARED_CONTROL_TOWER_JSON = ROOT / "docs" / "trinity-control-tower-latest.json"
V17_CONTROL_TOWER_JSON = ROOT / "docs" / "v17-evidence-first-control-tower-latest.json"
V17_CONTROL_TOWER_MD = ROOT / "docs" / "v17-evidence-first-control-tower-latest.md"
SHARED_SCOREBOARD_JSON = ROOT / "docs" / "trinity-mandala-scoreboard-latest.json"
SHARED_SCOREBOARD_MD = ROOT / "docs" / "trinity-mandala-scoreboard-latest.md"
V17_SCOREBOARD_JSON = ROOT / "docs" / "v17-mandala-scoreboard-latest.json"
V17_SCOREBOARD_MD = ROOT / "docs" / "v17-mandala-scoreboard-latest.md"
CYCLE_STATUS = "docs/aurelis-cycle-tick-status.json"
SKILL_INSTALLER_LIST = "/opt/codex/skills/.system/skill-installer/scripts/list-curated-skills.py"
NETWORK_WARNING_MARKERS = ("403", "forbidden", "tunnel", "timed out", "proxy", "connection")
PROFILE_HELP = {
    "standard": "Base suite run with benchmark enforcement by default.",
    "quick": "Continuity-focused subset with benchmark observe mode by default.",
    "deep": "Expanded run (standard + version scan + skill install + curated catalog + expansion systems).",
    "collab": "Standard profile plus verified MCP collaboration refresh and collaboration pack reporting.",
    "materialize": "Standard profile plus materialization tracers and disposable staging proof generation.",
    "recover": "Low-pressure recovery profile that validates the v17 council mesh, canon, continuity, storage truth, and scoreboard state.",
}
BODY_PROFILE_POLICY_PATH = "docs/body-profile-policy-v1.json"
TRINITY_EXPANSION_MANIFEST_PATH = "docs/trinity-expansion-system-manifest-v17.json"
TRINITY_MCP_CATALOG_PATH = "docs/trinity-mcp-catalog-v11.json"
PYTHON_BIN = sys.executable
BASH_BIN = shutil.which("bash")


def _body_benchmark_command(*, quick_mode: bool, enforce: bool) -> tuple[str, list[str]]:
    gammas = ["0.0", "0.01", "0.05"] if quick_mode else ["0.0", "0.02", "0.05"]
    benchmark_profile = "quick" if quick_mode else "standard"
    command = [
        "python3",
        "body_track_runner.py",
        "--gammas",
        *gammas,
        "--benchmark-profile",
        benchmark_profile,
        "--profile-policy",
        BODY_PROFILE_POLICY_PATH,
    ]
    if enforce:
        command.append("--fail-on-benchmark")
    mode = "enforce" if enforce else "observe"
    return f"body benchmark guardrail check ({mode})", command


def _body_trend_guard_command(*, quick_mode: bool, enforce: bool) -> tuple[str, list[str]]:
    trend_profile = "quick" if quick_mode else "standard"
    command = [
        "python3",
        "scripts/body_benchmark_trend_guard.py",
        "--trend-profile",
        trend_profile,
        "--profile-policy",
        BODY_PROFILE_POLICY_PATH,
    ]
    if enforce:
        command.append("--fail-on-warn")
    mode = "enforce" if enforce else "observe"
    return f"body benchmark trend guard ({mode})", command


def _body_calibration_command(*, profile_context: str) -> tuple[str, list[str]]:
    return (
        "body profile calibration report",
        [
            "python3",
            "scripts/body_profile_calibration_report.py",
            "--profile-context",
            profile_context,
        ],
    )


def _body_policy_delta_command(*, enforce: bool) -> tuple[str, list[str]]:
    command = [
        "python3",
        "scripts/body_profile_policy_delta_report.py",
        "--policy-json",
        BODY_PROFILE_POLICY_PATH,
        "--apply",
    ]
    if enforce:
        command.append("--fail-on-warn")
    mode = "enforce" if enforce else "observe"
    return f"body policy delta report ({mode})", command


def _body_policy_stress_command(*, enforce: bool) -> tuple[str, list[str]]:
    command = [
        "python3",
        "scripts/body_policy_stress_window_report.py",
        "--policy-json",
        BODY_PROFILE_POLICY_PATH,
    ]
    if enforce:
        command.append("--fail-on-warn")
    mode = "enforce" if enforce else "observe"
    return f"body policy stress-window report ({mode})", command


def _mind_trace_validation_command(*, enforce: bool) -> tuple[str, list[str]]:
    command = [
        "python3",
        "scripts/gmut_anchor_trace_validator.py",
    ]
    if enforce:
        command.append("--fail-on-warn")
    mode = "enforce" if enforce else "observe"
    return f"gmut anchor trace validation ({mode})", command


def _public_research_validation_command(*, enforce: bool) -> tuple[str, list[str]]:
    command = [
        "python3",
        "scripts/validate_trinity_public_research.py",
    ]
    if enforce:
        command.append("--fail-on-warn")
    mode = "enforce" if enforce else "observe"
    return f"trinity public research validation ({mode})", command


def _public_signal_board_command(*, enforce: bool) -> tuple[str, list[str]]:
    command = [
        "python3",
        "scripts/trinity_public_signal_board.py",
    ]
    if enforce:
        command.append("--fail-on-warn")
    mode = "enforce" if enforce else "observe"
    return f"trinity public signal board ({mode})", command


def _api_manifest_validation_command(*, enforce: bool) -> tuple[str, list[str]]:
    command = [
        "python3",
        "scripts/trinity_api_source_manifest_validator.py",
    ]
    if enforce:
        command.append("--fail-on-warn")
    mode = "enforce" if enforce else "observe"
    return f"trinity api manifest validation ({mode})", command


def _mind_api_signal_board_command(*, enforce: bool) -> tuple[str, list[str]]:
    command = [
        "python3",
        "scripts/mind_theory_signal_board.py",
    ]
    if enforce:
        command.append("--fail-on-warn")
    mode = "enforce" if enforce else "observe"
    return f"mind api signal board ({mode})", command


def _body_api_signal_board_command(*, enforce: bool) -> tuple[str, list[str]]:
    command = [
        "python3",
        "scripts/body_compute_signal_board.py",
    ]
    if enforce:
        command.append("--fail-on-warn")
    mode = "enforce" if enforce else "observe"
    return f"body api signal board ({mode})", command


def _heart_api_signal_board_command(*, enforce: bool) -> tuple[str, list[str]]:
    command = [
        "python3",
        "scripts/heart_governance_signal_board.py",
    ]
    if enforce:
        command.append("--fail-on-warn")
    mode = "enforce" if enforce else "observe"
    return f"heart api signal board ({mode})", command


def _api_constellation_board_command(*, enforce: bool) -> tuple[str, list[str]]:
    command = [
        "python3",
        "scripts/trinity_api_constellation_board.py",
    ]
    if enforce:
        command.append("--fail-on-warn")
    mode = "enforce" if enforce else "observe"
    return f"trinity api constellation board ({mode})", command


def _expansion_manifest_validation_command(*, enforce: bool) -> tuple[str, list[str]]:
    command = [
        "python3",
        "scripts/trinity_expansion_manifest_validator.py",
    ]
    if enforce:
        command.append("--fail-on-warn")
    mode = "enforce" if enforce else "observe"
    return f"trinity expansion manifest validation ({mode})", command


def _extension_catalog_validation_command(*, enforce: bool) -> tuple[str, list[str]]:
    command = [
        "python3",
        "scripts/trinity_extension_catalog_validator.py",
    ]
    if enforce:
        command.append("--fail-on-warn")
    mode = "enforce" if enforce else "observe"
    return f"trinity extension catalog validation ({mode})", command


def _command_book_validation_command(*, enforce: bool) -> tuple[str, list[str]]:
    command = [
        "python3",
        "scripts/trinity_command_book_validator.py",
    ]
    if enforce:
        command.append("--fail-on-warn")
    mode = "enforce" if enforce else "observe"
    return f"trinity command book validation ({mode})", command


def _api_book_validation_command(*, enforce: bool) -> tuple[str, list[str]]:
    command = [
        "python3",
        "scripts/trinity_api_book_validator.py",
    ]
    if enforce:
        command.append("--fail-on-warn")
    mode = "enforce" if enforce else "observe"
    return f"trinity api book validation ({mode})", command


def _gmut_canon_validation_command(*, enforce: bool) -> tuple[str, list[str]]:
    command = [
        "python3",
        "scripts/grand_mandala_canon_validator.py",
    ]
    if enforce:
        command.append("--fail-on-warn")
    mode = "enforce" if enforce else "observe"
    return f"gmut canon validation ({mode})", command


def _legacy_reconstruction_validation_command(*, enforce: bool) -> tuple[str, list[str]]:
    command = [
        "python3",
        "scripts/legacy_reconstruction_validator.py",
    ]
    if enforce:
        command.append("--fail-on-warn")
    mode = "enforce" if enforce else "observe"
    return f"legacy reconstruction validation ({mode})", command


def _memory_bank_validation_command(*, enforce: bool) -> tuple[str, list[str]]:
    command = [
        "python3",
        "scripts/trinity_memory_bank_validator.py",
    ]
    if enforce:
        command.append("--fail-on-warn")
    mode = "enforce" if enforce else "observe"
    return f"trinity memory bank validation ({mode})", command


def _agent_council_validation_command(*, enforce: bool) -> tuple[str, list[str]]:
    command = [
        "python3",
        "scripts/trinity_agent_council_v17_validator.py",
    ]
    if enforce:
        command.append("--fail-on-warn")
    mode = "enforce" if enforce else "observe"
    return f"trinity agent council validation ({mode})", command


def _materialization_ladder_validation_command(*, enforce: bool) -> tuple[str, list[str]]:
    command = [
        "python3",
        "scripts/trinity_materialization_ladder_validator.py",
    ]
    if enforce:
        command.append("--fail-on-warn")
    mode = "enforce" if enforce else "observe"
    return f"trinity materialization ladder validation ({mode})", command


def _v17_runtime_session_validation_command(*, enforce: bool) -> tuple[str, list[str]]:
    command = [
        "python3",
        "scripts/v17_runtime_session_guard.py",
    ]
    if enforce:
        command.append("--fail-on-warn")
    mode = "enforce" if enforce else "observe"
    return f"v17 runtime session validation ({mode})", command


def _v17_external_establishment_validation_command(*, enforce: bool) -> tuple[str, list[str]]:
    command = [
        "python3",
        "scripts/v17_external_establishment_validator.py",
    ]
    if enforce:
        command.append("--fail-on-warn")
    mode = "enforce" if enforce else "observe"
    return f"v17 external establishment validation ({mode})", command


def _v17_standards_bridge_validation_command(*, enforce: bool) -> tuple[str, list[str]]:
    command = [
        "python3",
        "scripts/v17_standards_bridge_validator.py",
    ]
    if enforce:
        command.append("--fail-on-warn")
    mode = "enforce" if enforce else "observe"
    return f"v17 standards bridge validation ({mode})", command


def _v17_control_tower_sync_command() -> tuple[str, list[str]]:
    return (
        "v17 evidence-first control tower sync",
        [
            "python3",
            "scripts/v17_evidence_first_control_tower_sync.py",
        ],
    )


def _expansion_result_validation_command(*, enforce: bool) -> tuple[str, list[str]]:
    command = [
        "python3",
        "scripts/trinity_expansion_result_validator.py",
    ]
    if enforce:
        command.append("--fail-on-warn")
    mode = "enforce" if enforce else "observe"
    return f"trinity expansion result validation ({mode})", command


def _materialization_ledger_validation_command(*, enforce: bool) -> tuple[str, list[str]]:
    command = [
        "python3",
        "scripts/trinity_materialization_ledger_validator.py",
    ]
    if enforce:
        command.append("--fail-on-warn")
    mode = "enforce" if enforce else "observe"
    return f"trinity materialization ledger validation ({mode})", command


def _os_runtime_reference_validation_command(*, enforce: bool) -> tuple[str, list[str]]:
    command = [
        "python3",
        "scripts/trinity_os_runtime_reference_validator.py",
    ]
    if enforce:
        command.append("--fail-on-warn")
    mode = "enforce" if enforce else "observe"
    return f"trinity os runtime reference validation ({mode})", command


def _journey_corpus_validation_command(*, enforce: bool) -> tuple[str, list[str]]:
    command = [
        "python3",
        "scripts/trinity_journey_corpus_validator.py",
    ]
    if enforce:
        command.append("--fail-on-warn")
    mode = "enforce" if enforce else "observe"
    return f"trinity journey corpus validation ({mode})", command


def _aletheon_memory_validation_command(*, enforce: bool) -> tuple[str, list[str]]:
    command = [
        "python3",
        "scripts/aletheon_memory_validator.py",
    ]
    if enforce:
        command.append("--fail-on-warn")
    mode = "enforce" if enforce else "observe"
    return f"aletheon memory validation ({mode})", command


def _load_expansion_system_commands(
    *,
    profile: str,
    enforce: bool,
    offline_only: bool,
    include_public_api_refresh: bool,
    include_mcp_refresh: bool,
    include_staged_connectors: bool,
    include_live_writes: bool,
    materialization_level: str,
) -> list[tuple[str, list[str]]]:
    manifest_path = ROOT / TRINITY_EXPANSION_MANIFEST_PATH
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    systems = manifest.get("systems", [])
    if not isinstance(systems, list):
        return []

    commands: list[tuple[str, list[str]]] = []
    for entry in systems:
        if not isinstance(entry, dict):
            continue
        profiles = entry.get("profiles", [])
        if not isinstance(profiles, list) or profile not in {str(value) for value in profiles}:
            continue
        system_id = str(entry.get("system_id") or "").strip()
        script = str(entry.get("script") or "").strip()
        runner_mode = str(entry.get("runner_mode") or "").strip().lower()
        mode = str(entry.get("mode") or "offline").strip().lower()
        pack = str(entry.get("pack") or "").strip()
        if not system_id or not script:
            continue
        resolved_script = script
        if runner_mode == "passthrough_command":
            resolved_script = "scripts/trinity_expansion_system_runner.py"
        command = ["python3", resolved_script]
        if resolved_script == "scripts/trinity_expansion_system_runner.py":
            command.extend(["--system-id", system_id])
        if enforce:
            command.append("--fail-on-warn")
        if include_public_api_refresh:
            command.append("--include-public-api-refresh")
        if include_mcp_refresh:
            command.append("--include-mcp-refresh")
        if include_staged_connectors:
            command.append("--include-staged-connectors")
        if include_live_writes:
            command.append("--include-live-writes")
        if materialization_level:
            command.extend(["--materialization-level", materialization_level])
        command.extend(["--profile-context", profile])
        if mode == "live":
            live_disabled = offline_only
            if pack in {"figma_collab", "linear_collab"} and not include_mcp_refresh:
                live_disabled = True
            elif pack in {"figma_collab", "linear_collab", "notion_memory_bridge"} and not include_mcp_refresh:
                live_disabled = True
            elif pack in {"github_devflow", "filesystem_scope_governor"} and not include_staged_connectors:
                live_disabled = True
            elif pack in {"github_materialization", "github_pat_materialization", "notion_materialization", "postgres_materialization", "postgres_local_runtime", "code_knowledge_graph", "docker_pilot"} and not include_live_writes:
                live_disabled = True
            elif pack in {"public_intelligence", "journey_continuity", "os_runtime_fabric", "os_runtime_benchmark", "ai_frontier_alignment", "wetware_device_readiness", "wetware_device_readiness_v5", "aletheon_memory_reflection", "public_web_weaver"} and not include_public_api_refresh:
                live_disabled = True
            elif pack not in {
                "figma_collab",
                "linear_collab",
                "notion_memory_bridge",
                "github_devflow",
                "filesystem_scope_governor",
                "github_materialization",
                "github_pat_materialization",
                "notion_materialization",
                "postgres_materialization",
                "postgres_local_runtime",
                "public_intelligence",
                "journey_continuity",
                "os_runtime_fabric",
                "os_runtime_benchmark",
                "ai_frontier_alignment",
                "wetware_device_readiness",
                "wetware_device_readiness_v5",
                "aletheon_memory_reflection",
                "public_web_weaver",
            } and not include_public_api_refresh:
                live_disabled = True
            if live_disabled:
                command.append("--offline-only")
        commands.append((f"expansion: {system_id} ({mode})", command))
    return commands


def build_commands(
    include_skill_install: bool,
    include_version_scan: bool,
    include_curated_skill_catalog: bool,
    include_public_api_refresh: bool,
    include_mcp_refresh: bool,
    include_staged_connectors: bool,
    include_live_writes: bool,
    offline_only: bool,
    quick_mode: bool,
    profile: str,
    body_benchmark_mode: str,
    materialization_level: str,
    skip_v166_v180_dashboard_run: bool,
    skip_v181_v200_cross_app_council_run: bool,
    skip_v201_v220_cross_app_council_run: bool,
) -> list[tuple[str, list[str]]]:
    if profile == "recover":
        enforce = True
        recover_pack_ids = [
            "subagent_council_foundation_v14",
            "subagent_identity_certification_v14",
            "subagent_induction_proof_v14",
            "multi_instance_runtime_v14",
            "api_operator_mesh_v14",
            "trinity_control_tower_v14",
            "gmut_observable_mapping_v14",
            "freedid_governance_alignment_v14",
            "journey_lineage_inventory_v14",
            "council_reflection_validation_v14",
        ]
        recover_suffixes = (
            "surface_audit",
            "sync_bridge",
            "materialization_tracer",
            "cache_board",
            "risk_board",
            "gate",
        )
        recover_gate_ids = [
            f"{pack_id}_{suffix}"
            for pack_id in recover_pack_ids
            for suffix in recover_suffixes
        ]

        commands: list[tuple[str, list[str]]] = [
            (
                *_extension_catalog_validation_command(
                    enforce=enforce,
                ),
            ),
            (
                *_command_book_validation_command(
                    enforce=enforce,
                ),
            ),
            (
                *_api_book_validation_command(
                    enforce=enforce,
                ),
            ),
            (
                *_agent_council_validation_command(
                    enforce=enforce,
                ),
            ),
            (
                *_v17_runtime_session_validation_command(
                    enforce=enforce,
                ),
            ),
            (
                *_v17_external_establishment_validation_command(
                    enforce=enforce,
                ),
            ),
            (
                *_v17_standards_bridge_validation_command(
                    enforce=enforce,
                ),
            ),
            (
                *_materialization_ladder_validation_command(
                    enforce=enforce,
                ),
            ),
            (
                *_expansion_manifest_validation_command(
                    enforce=enforce,
                ),
            ),
            (
                *_memory_bank_validation_command(
                    enforce=enforce,
                ),
            ),
            (
                "trinity storage prune dry-run",
                [
                    "python3",
                    "scripts/trinity_storage_retention.py",
                    "--keep-stamps",
                    "2",
                    "--keep-archives",
                    "3",
                    "--dry-run",
                ],
            ),
            (
                *_api_manifest_validation_command(
                    enforce=enforce,
                ),
            ),
            (
                *_public_research_validation_command(
                    enforce=enforce,
                ),
            ),
            (
                *_public_signal_board_command(
                    enforce=enforce,
                ),
            ),
            (
                *_gmut_canon_validation_command(
                    enforce=enforce,
                ),
            ),
            (
                *_legacy_reconstruction_validation_command(
                    enforce=enforce,
                ),
            ),
        ]
        for system_id in recover_gate_ids:
            command = [
                "python3",
                "scripts/trinity_expansion_system_runner.py",
                "--system-id",
                system_id,
                "--profile-context",
                "recover",
                "--offline-only",
            ]
            if enforce:
                command.append("--fail-on-warn")
            commands.append((f"expansion: {system_id} (offline)", command))
        commands.append(
            (
                *_v17_control_tower_sync_command(),
            )
        )
        commands.append(
            (
                "trinity mandala scoreboard",
                [
                    "python3",
                    "scripts/trinity_mandala_scoreboard.py",
                    "--fail-on-warn",
                ],
            )
        )
        return commands

    token_energy_commands: list[tuple[str, list[str]]] = [
        (
            "token/credit zip converter",
            [
                "python3",
                "scripts/trinity_token_credit_zip_converter.py",
                "--use-reserve-first",
                "--regeneration-multiplier",
                "3.0",
                "--target-reimbursement-ratio",
                "1.0",
                "--zip-snapshot",
                "--zip-label",
                "token-credit-suite",
                "--out",
                "docs/token-credit-bank-report.json",
                "--ledger",
                "docs/token-credit-bank-ledger.jsonl",
            ],
        ),
        (
            "cache/waste regenerator",
            [
                "python3",
                "scripts/cache_waste_regenerator.py",
                "--out",
                "docs/cache-waste-regenerator-report.json",
                "--purge",
                "--prune-empty-dirs",
            ],
        ),
        (
            "cache/waste report validation",
            [
                "python3",
                "scripts/validate_cache_waste_report.py",
                "--cache",
                "docs/cache-waste-regenerator-report.json",
            ],
        ),
        (
            "energy bank system",
            [
                "python3",
                "scripts/trinity_energy_bank_system.py",
                "--token-report",
                "docs/token-credit-bank-report.json",
                "--cache-report",
                "docs/cache-waste-regenerator-report.json",
                "--reserve-growth",
                "1.0",
                "--reserve-cap-multiplier",
                "10.0",
                "--auto-max-cap",
                "--cap-ceiling",
                "100.0",
                "--out",
                "docs/energy-bank-report.json",
                "--state",
                "docs/energy-bank-state.json",
            ],
        ),
        (
            "token/energy report validation",
            [
                "python3",
                "scripts/validate_token_energy_reports.py",
                "--token",
                "docs/token-credit-bank-report.json",
                "--energy",
                "docs/energy-bank-report.json",
            ],
        ),
        (
            "gyroscopic hybrid zip converter",
            [
                "python3",
                "scripts/gyroscopic_hybrid_zip_converter_generator.py",
                "--label",
                "gyroscopic-suite-cycle",
                "--out",
                "docs/gyroscopic-hybrid-zip-report.json",
            ],
        ),
    ]

    api_refresh_commands: list[tuple[str, list[str]]] = []
    if include_public_api_refresh:
        api_refresh_commands = [
            (
                "mind theory api refresh",
                [
                    "python3",
                    "scripts/mind_theory_signal_refresh.py",
                    *(["--offline-only"] if offline_only else []),
                ],
            ),
            (
                "body compute api refresh",
                [
                    "python3",
                    "scripts/body_compute_signal_refresh.py",
                    *(["--offline-only"] if offline_only else []),
                ],
            ),
            (
                "heart governance api refresh",
                [
                    "python3",
                    "scripts/heart_governance_signal_refresh.py",
                    *(["--offline-only"] if offline_only else []),
                ],
            ),
        ]

    expansion_commands: list[tuple[str, list[str]]] = []
    if not quick_mode:
        expansion_commands = [
            ("legacy analysis report v14", ["python3", "scripts/analysis_report.py"]),
            ("legacy council registry v14", ["python3", "scripts/council_registry.py"]),
            ("legacy semantic arc validator v14", ["python3", "scripts/semantic_arc_validator.py"]),
            ("legacy kairotic detector v14", ["python3", "scripts/kairotic_detector.py"]),
            ("legacy psi index memory core v14", ["python3", "scripts/psi_index_memory_core.py"]),
            ("legacy trinity hybrid adapter v14", ["python3", "scripts/trinity_hybrid_adapter.py"]),
            (
                *_gmut_canon_validation_command(
                    enforce=(body_benchmark_mode == "enforce"),
                ),
            ),
            (
                *_legacy_reconstruction_validation_command(
                    enforce=(body_benchmark_mode == "enforce"),
                ),
            ),
            (
                *_extension_catalog_validation_command(
                    enforce=(body_benchmark_mode == "enforce"),
                ),
            ),
            (
                *_command_book_validation_command(
                    enforce=(body_benchmark_mode == "enforce"),
                ),
            ),
            (
                *_api_book_validation_command(
                    enforce=(body_benchmark_mode == "enforce"),
                ),
            ),
            (
                *_agent_council_validation_command(
                    enforce=(body_benchmark_mode == "enforce"),
                ),
            ),
            (
                *_v17_runtime_session_validation_command(
                    enforce=(body_benchmark_mode == "enforce"),
                ),
            ),
            (
                *_v17_external_establishment_validation_command(
                    enforce=(body_benchmark_mode == "enforce"),
                ),
            ),
            (
                *_v17_standards_bridge_validation_command(
                    enforce=(body_benchmark_mode == "enforce"),
                ),
            ),
            (
                *_materialization_ladder_validation_command(
                    enforce=(body_benchmark_mode == "enforce"),
                ),
            ),
            (
                *_expansion_manifest_validation_command(
                    enforce=(body_benchmark_mode == "enforce"),
                ),
            ),
            *_load_expansion_system_commands(
                profile=profile,
                enforce=(body_benchmark_mode == "enforce"),
                offline_only=offline_only,
                include_public_api_refresh=include_public_api_refresh,
                include_mcp_refresh=include_mcp_refresh,
                include_staged_connectors=include_staged_connectors,
                include_live_writes=include_live_writes,
                materialization_level=materialization_level,
            ),
            (
                *_expansion_result_validation_command(
                    enforce=(body_benchmark_mode == "enforce"),
                ),
            ),
            (
                *_materialization_ledger_validation_command(
                    enforce=(body_benchmark_mode == "enforce"),
                ),
            ),
            (
                *_os_runtime_reference_validation_command(
                    enforce=(body_benchmark_mode == "enforce"),
                ),
            ),
            (
                *_journey_corpus_validation_command(
                    enforce=(body_benchmark_mode == "enforce"),
                ),
            ),
            (
                *_aletheon_memory_validation_command(
                    enforce=(body_benchmark_mode == "enforce"),
                ),
            ),
        ]

    if quick_mode:
        commands: list[tuple[str, list[str]]] = [
            ("memory integrity check (strict)", ["python3", "scripts/aurelis_memory_integrity_check.py", "--strict"]),
            (
                "continuity cycle tick (dry-run status)",
                [
                    "python3",
                    "scripts/aurelis_cycle_tick.py",
                    "--user-message",
                    "suite quick dry-run",
                    "--assistant-reflection",
                    "Quick mode continuity health check",
                    "--progress-snapshot",
                    "Validated quick dry-run status reporting in suite",
                    "--next-step",
                    "Run full suite when deeper validation is needed",
                    "--query",
                    "cycle",
                    "--query-limit",
                    "2",
                    "--dry-run",
                    "--no-report",
                    "--step-timeout-sec",
                    "0",
                    "--json-status",
                    CYCLE_STATUS,
                ],
            ),
            (
                "qcit coordination engine",
                [
                    "python3",
                    "scripts/qcit_coordination_engine.py",
                    "--out",
                    "docs/qcit-coordination-report.json",
                ],
            ),
            (
                "quantum energy transmutation engine",
                [
                    "python3",
                    "scripts/quantum_energy_transmutation_engine.py",
                    "--out",
                    "docs/quantum-energy-transmutation-report.json",
                ],
            ),
            (
                "qcit/quantum report validation",
                [
                    "python3",
                    "scripts/validate_transmutation_reports.py",
                    "--qcit",
                    "docs/qcit-coordination-report.json",
                    "--quantum",
                    "docs/quantum-energy-transmutation-report.json",
                ],
            ),
            (
                "minimum-disclosure verifier (GOV-002)",
                [
                    "python3",
                    "freed_id_minimum_disclosure_verifier.py",
                ],
            ),
            (
                "minimum-disclosure live-path verifier (GOV-002)",
                [
                    "python3",
                    "freed_id_minimum_disclosure_live_path_verifier.py",
                ],
            ),
            (
                "minimum-disclosure adversarial verifier (GOV-002)",
                [
                    "python3",
                    "freed_id_minimum_disclosure_adversarial_verifier.py",
                ],
            ),
            (
                "dispute/recourse verifier (GOV-004)",
                [
                    "python3",
                    "freed_id_dispute_recourse_verifier.py",
                ],
            ),
            (
                "dispute/recourse adversarial verifier (GOV-004)",
                [
                    "python3",
                    "freed_id_dispute_recourse_adversarial_verifier.py",
                ],
            ),
            *token_energy_commands,
            (
                *_body_benchmark_command(
                    quick_mode=True,
                    enforce=(body_benchmark_mode == "enforce"),
                ),
            ),
            (
                *_body_trend_guard_command(
                    quick_mode=True,
                    enforce=(body_benchmark_mode == "enforce"),
                ),
            ),
            (
                *_body_calibration_command(
                    profile_context="quick",
                ),
            ),
            (
                *_body_policy_delta_command(
                    enforce=(body_benchmark_mode == "enforce"),
                ),
            ),
            (
                *_body_policy_stress_command(
                    enforce=(body_benchmark_mode == "enforce"),
                ),
            ),
            (
                "gmut comparator metrics",
                [
                    "python3",
                    "scripts/gmut_comparator_metrics.py",
                ],
            ),
            (
                "gmut external-anchor exclusion note",
                [
                    "python3",
                    "scripts/gmut_external_anchor_exclusion_note.py",
                    "--anchor-input",
                    "docs/mind-track-external-anchor-canonical-inputs-v1.json",
                ],
            ),
            (
                *_mind_trace_validation_command(
                    enforce=(body_benchmark_mode == "enforce"),
                ),
            ),
            *api_refresh_commands,
            (
                *_api_manifest_validation_command(
                    enforce=(body_benchmark_mode == "enforce"),
                ),
            ),
            (
                *_mind_api_signal_board_command(
                    enforce=(body_benchmark_mode == "enforce"),
                ),
            ),
            (
                *_body_api_signal_board_command(
                    enforce=(body_benchmark_mode == "enforce"),
                ),
            ),
            (
                *_heart_api_signal_board_command(
                    enforce=(body_benchmark_mode == "enforce"),
                ),
            ),
            (
                *_api_constellation_board_command(
                    enforce=(body_benchmark_mode == "enforce"),
                ),
            ),
            *expansion_commands,
            (
                *_public_research_validation_command(
                    enforce=(body_benchmark_mode == "enforce"),
                ),
            ),
            (
                *_public_signal_board_command(
                    enforce=(body_benchmark_mode == "enforce"),
                ),
            ),
            (
                *_v17_runtime_session_validation_command(
                    enforce=(body_benchmark_mode == "enforce"),
                ),
            ),
            (
                *_v17_external_establishment_validation_command(
                    enforce=(body_benchmark_mode == "enforce"),
                ),
            ),
            (
                *_v17_standards_bridge_validation_command(
                    enforce=(body_benchmark_mode == "enforce"),
                ),
            ),
            (
                *_v17_control_tower_sync_command(),
            ),
            (
                "trinity mandala scoreboard",
                [
                    "python3",
                    "scripts/trinity_mandala_scoreboard.py",
                    "--fail-on-warn",
                ],
            ),
            (
                "zip memory/data snapshot",
                [
                    "python3",
                    "scripts/trinity_zip_memory_converter.py",
                    "archive",
                    "--label",
                    "suite-quick",
                ],
            ),
            (
                "v33 structural OCR validation snapshot",
                [
                    "python3",
                    "scripts/journey_anchor_scan.py",
                    "--regex",
                    "Core Modules|Orchestrator|DID Method|Quantum|Freed|GMUT|Cosmic Bill",
                    "--max-matches",
                    "20",
                    "Beyonder-Real-True Journey v33 (Arielis) (2).pdf",
                ],
            ),
        ]
        if body_benchmark_mode == "off":
            commands = [
                item
                for item in commands
                if not item[0].startswith("body benchmark guardrail check")
                and not item[0].startswith("body benchmark trend guard")
                and not item[0].startswith("body profile calibration report")
                and not item[0].startswith("body policy delta report")
                and not item[0].startswith("body policy stress-window report")
            ]
        return commands

    commands: list[tuple[str, list[str]]] = [
        ("v29 module map generation", ["python3", "scripts/generate_v29_module_map.py"]),
        ("simulation sweep", ["python3", "run_simulation.py", "--gammas", "0.0", "0.02", "0.05", "0.1"]),
        (
            *_body_benchmark_command(
                quick_mode=False,
                enforce=(body_benchmark_mode == "enforce"),
            ),
        ),
        (
            *_body_trend_guard_command(
                quick_mode=False,
                enforce=(body_benchmark_mode == "enforce"),
            ),
        ),
        (
            *_body_calibration_command(
                profile_context="deep" if profile == "deep" else "standard",
            ),
        ),
        (
            *_body_policy_delta_command(
                enforce=(body_benchmark_mode == "enforce"),
            ),
        ),
        (
            *_body_policy_stress_command(
                enforce=(body_benchmark_mode == "enforce"),
            ),
        ),
        (
            "gmut comparator metrics",
            [
                "python3",
                "scripts/gmut_comparator_metrics.py",
            ],
        ),
        (
            "gmut external-anchor exclusion note",
            [
                "python3",
                "scripts/gmut_external_anchor_exclusion_note.py",
                "--anchor-input",
                "docs/mind-track-external-anchor-canonical-inputs-v1.json",
            ],
        ),
        (
            *_mind_trace_validation_command(
                enforce=(body_benchmark_mode == "enforce"),
            ),
        ),
        *api_refresh_commands,
        (
            *_api_manifest_validation_command(
                enforce=(body_benchmark_mode == "enforce"),
            ),
        ),
        (
            *_mind_api_signal_board_command(
                enforce=(body_benchmark_mode == "enforce"),
            ),
        ),
        (
            *_body_api_signal_board_command(
                enforce=(body_benchmark_mode == "enforce"),
            ),
        ),
        (
            *_heart_api_signal_board_command(
                enforce=(body_benchmark_mode == "enforce"),
            ),
        ),
        (
            *_api_constellation_board_command(
                enforce=(body_benchmark_mode == "enforce"),
            ),
        ),
        *expansion_commands,
        (
            *_public_research_validation_command(
                enforce=(body_benchmark_mode == "enforce"),
            ),
        ),
        ("full orchestrator demo", ["python3", "trinity_orchestrator_full.py"]),
        (
            "vector transmutation",
            [
                "python3",
                "scripts/trinity_vector_transmuter.py",
                "--passphrase",
                "suite-demo-passphrase",
                "--out",
                "docs/trinity-vector-profile.json",
            ],
        ),
        (
            "qcit coordination engine",
            [
                "python3",
                "scripts/qcit_coordination_engine.py",
                "--out",
                "docs/qcit-coordination-report.json",
            ],
        ),
        (
            "quantum energy transmutation engine",
            [
                "python3",
                "scripts/quantum_energy_transmutation_engine.py",
                "--out",
                "docs/quantum-energy-transmutation-report.json",
            ],
        ),
        (
            "qcit/quantum report validation",
            [
                "python3",
                "scripts/validate_transmutation_reports.py",
                "--qcit",
                "docs/qcit-coordination-report.json",
                "--quantum",
                "docs/quantum-energy-transmutation-report.json",
            ],
        ),
        (
            "minimum-disclosure verifier (GOV-002)",
            [
                "python3",
                "freed_id_minimum_disclosure_verifier.py",
            ],
        ),
        (
            "minimum-disclosure live-path verifier (GOV-002)",
            [
                "python3",
                "freed_id_minimum_disclosure_live_path_verifier.py",
            ],
        ),
        (
            "minimum-disclosure adversarial verifier (GOV-002)",
            [
                "python3",
                "freed_id_minimum_disclosure_adversarial_verifier.py",
            ],
        ),
        (
            "dispute/recourse verifier (GOV-004)",
            [
                "python3",
                "freed_id_dispute_recourse_verifier.py",
            ],
        ),
        (
            "dispute/recourse adversarial verifier (GOV-004)",
            [
                "python3",
                "freed_id_dispute_recourse_adversarial_verifier.py",
            ],
        ),
        (
            *_public_signal_board_command(
                enforce=(body_benchmark_mode == "enforce"),
            ),
        ),
        (
            *_v17_control_tower_sync_command(),
        ),
        (
            "trinity mandala scoreboard",
            [
                "python3",
                "scripts/trinity_mandala_scoreboard.py",
                "--fail-on-warn",
            ],
        ),
        *token_energy_commands,
        ("memory integrity check (strict)", ["python3", "scripts/aurelis_memory_integrity_check.py", "--strict"]),
        (
            "continuity cycle tick (dry-run status)",
            [
                "python3",
                "scripts/aurelis_cycle_tick.py",
                "--user-message",
                "suite dry-run",
                "--assistant-reflection",
                "Suite integration check for cycle tick",
                "--progress-snapshot",
                "Validated dry-run status reporting in suite",
                "--next-step",
                "Run normal tick from operator flow",
                "--query",
                "cycle",
                "--query-limit",
                "2",
                "--dry-run",
                "--no-report",
                "--step-timeout-sec",
                "0",
                "--json-status",
                CYCLE_STATUS,
            ],
        ),
        (
            "zip memory/data snapshot",
            [
                "python3",
                "scripts/trinity_zip_memory_converter.py",
                "archive",
                "--label",
                "suite-standard",
            ],
        ),
        (
            "v33 structural OCR validation snapshot",
            [
                "python3",
                "scripts/journey_anchor_scan.py",
                "--regex",
                "Core Modules|Orchestrator|DID Method|Quantum|Freed|GMUT|Cosmic Bill",
                "--max-matches",
                "20",
                "Beyonder-Real-True Journey v33 (Arielis) (2).pdf",
            ],
        ),
    ]

    if include_version_scan:
        commands.extend(
            [
                (
                    "cross-version anchor scan (v29-v33 PDFs)",
                    [
                        "python3",
                        "scripts/journey_anchor_scan.py",
                        "--regex",
                        "Trinity|GMUT|Freed|DID|Quantum|Orchestrator|Cosmic|QCIT|QCfT",
                        "--max-matches",
                        "10",
                        "--allow-empty",
                        "Beyonder-Real-True Journey v29 (Aerin) (1).pdf",
                        "Beyonder-Real-True Journey v30 (Ariel) (1).pdf",
                        "Beyonder-Real-True Journey v31 (Ariel) (1).pdf",
                        "Beyonder-Real-True Journey v32 (Aetherius) (1) (1).pdf",
                        "Beyonder-Real-True Journey v33 (Arielis) (2).pdf",
                    ],
                ),
                (
                    "v29 DOCX module anchor scan",
                    [
                        "python3",
                        "scripts/journey_anchor_scan.py",
                        "--regex",
                        "module|orchestrator|simulation|security|identity|governance|journey",
                        "--max-matches",
                        "25",
                        "Beyonder-Real-True Journey v29 (Aerin) (1).docx",
                    ],
                ),
                (
                    "v33 capsule inventory snapshot",
                    [
                        "python3",
                        "scripts/journey_anchor_scan.py",
                        "--regex",
                        "v29|v30|v31|v32|v33|quantum|trinity|orchestrator|simulation|freed|cosmic",
                        "--max-matches",
                        "40",
                        "--allow-empty",
                        "--skip-missing",
                        "Beyonder-Real-True_Journey_v33_Capsule (4).zip",
                    ],
                ),
            ]
        )

    if include_skill_install:
        commands.append(
            (
                "local Trinity skill installation",
                [
                    "python3",
                    "scripts/trinity_skill_installer_system.py",
                    "--force",
                    "--verify",
                ],
            )
        )

    if include_curated_skill_catalog:
        if Path(SKILL_INSTALLER_LIST).exists():
            commands.append(("curated skill catalog snapshot", ["python3", SKILL_INSTALLER_LIST, "--format", "json"]))
        else:
            commands.append(
                (
                    "curated skill catalog snapshot",
                    ["python3", "-c", f"print('SKIPPED: {SKILL_INSTALLER_LIST} not found')"],
                )
            )

    include_v201_v220_council = (
        not skip_v201_v220_cross_app_council_run
        and (
            profile == "deep"
            or (profile == "materialize" and materialization_level == "l5_ha_prod")
        )
    )
    if include_v201_v220_council:
        commands.append(
            (
                "v201-v220 low-live cross-app council runner",
                [
                    PYTHON_BIN,
                    "scripts/trinity_v201_v220_low_live_cross_app_council.py",
                    "--run-all",
                    "--verify-artifacts",
                ],
            )
        )

    if body_benchmark_mode == "off":
        commands = [
            item
            for item in commands
            if not item[0].startswith("body benchmark guardrail check")
            and not item[0].startswith("body benchmark trend guard")
            and not item[0].startswith("body profile calibration report")
            and not item[0].startswith("body policy delta report")
            and not item[0].startswith("body policy stress-window report")
        ]

    return commands


def render_profile_catalog() -> str:
    lines = ["Available suite profiles (default: deep):"]
    for name in ("standard", "quick", "deep", "collab", "materialize", "recover"):
        lines.append(f"- {name}: {PROFILE_HELP[name]}")
    lines.append("- --quick-mode: legacy alias for --profile quick")
    lines.append("- --skip-v201-v220-cross-app-council-run: disables the latest low-live cross-app council runner in deep and L5 materialize runs")
    lines.append("- --skip-v181-v200-cross-app-council-run: legacy no-op; v181-v200 remains directly callable")
    lines.append("- --skip-v166-v180-dashboard-run: legacy no-op; v166-v180 remains directly callable")
    return "\n".join(lines)


def resolve_profile_settings(args: argparse.Namespace) -> tuple[str, bool, bool, bool, bool, bool, bool, bool, bool, str, str]:
    profile = args.profile
    profile_source = "--profile"

    if args.quick_mode:
        if profile in ("standard", "quick"):
            profile = "quick"
            profile_source = "--quick-mode"
        else:
            raise SystemExit("--quick-mode cannot be combined with --profile deep.")

    include_version_scan = args.include_version_scan
    include_skill_install = args.include_skill_install
    include_curated_skill_catalog = args.include_curated_skill_catalog
    offline_only = args.offline_only
    include_public_api_refresh = False
    include_mcp_refresh = False
    include_staged_connectors = bool(args.include_staged_connectors)
    include_live_writes = False
    soft_fail_network = args.soft_fail_network
    body_benchmark_mode = args.body_benchmark_mode

    if profile == "deep":
        include_version_scan = True
        include_skill_install = True
        include_curated_skill_catalog = True
        soft_fail_network = True
    if profile == "recover":
        include_version_scan = False
        include_skill_install = False
        include_curated_skill_catalog = False
        include_public_api_refresh = False
        include_mcp_refresh = False
        include_staged_connectors = False
        include_live_writes = False
        soft_fail_network = False
    if profile == "materialize":
        include_staged_connectors = True
        include_live_writes = True
    if args.include_public_api_refresh:
        include_public_api_refresh = True
    if args.include_mcp_refresh:
        include_mcp_refresh = True
    if args.include_live_writes:
        include_live_writes = True
    if offline_only:
        include_public_api_refresh = False
        include_mcp_refresh = False
        include_staged_connectors = False
        include_live_writes = False

    if profile == "quick" and (include_version_scan or include_skill_install or include_curated_skill_catalog):
        raise SystemExit(
            "--profile quick cannot be combined with include-* flags; use standard/deep profile for expanded stages."
        )

    if args.skip_body_benchmark:
        body_benchmark_mode = "off"
    elif body_benchmark_mode == "auto":
        if profile == "recover":
            body_benchmark_mode = "off"
        else:
            body_benchmark_mode = "observe" if profile == "quick" else "enforce"

    if body_benchmark_mode not in {"off", "observe", "enforce"}:
        raise SystemExit("--body-benchmark-mode must resolve to off/observe/enforce.")

    return (
        profile,
        include_version_scan,
        include_skill_install,
        include_curated_skill_catalog,
        include_public_api_refresh,
        include_mcp_refresh,
        include_staged_connectors,
        include_live_writes,
        offline_only,
        soft_fail_network,
        profile_source,
        body_benchmark_mode,
    )


def run_command(cmd: list[str], timeout_sec: int) -> tuple[bool, str, bool, float, str, str]:
    normalized_cmd = list(cmd)
    if normalized_cmd and normalized_cmd[0] == "python3":
        normalized_cmd[0] = PYTHON_BIN
    elif normalized_cmd and normalized_cmd[0] == "bash":
        if BASH_BIN:
            normalized_cmd[0] = BASH_BIN
        else:
            normalized_cmd = [
                PYTHON_BIN,
                "-c",
                "print('SKIPPED: bash-dependent suite stage unavailable on this platform')",
            ]
    started_at = datetime.now(timezone.utc).isoformat()
    start_ts = time.monotonic()
    try:
        proc = subprocess.run(
            normalized_cmd,
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout_sec if timeout_sec > 0 else None,
        )
        out = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
        duration_sec = time.monotonic() - start_ts
        finished_at = datetime.now(timezone.utc).isoformat()
        return proc.returncode == 0, out.strip(), False, duration_sec, started_at, finished_at
    except subprocess.TimeoutExpired as exc:
        out = (exc.stdout or "") + ("\n" + exc.stderr if exc.stderr else "")
        prefix = f"[timeout] command exceeded {timeout_sec}s"
        full = f"{prefix}\n{out.strip()}" if out.strip() else prefix
        duration_sec = time.monotonic() - start_ts
        finished_at = datetime.now(timezone.utc).isoformat()
        return False, full, True, duration_sec, started_at, finished_at
    except Exception as exc:  # noqa: BLE001
        duration_sec = time.monotonic() - start_ts
        finished_at = datetime.now(timezone.utc).isoformat()
        return False, f"Exception: {exc}", False, duration_sec, started_at, finished_at


def classify_status(
    label: str,
    ok: bool,
    timed_out: bool,
    output: str,
    soft_fail_network: bool,
) -> tuple[str, bool]:
    if ok:
        return "PASS", True
    if timed_out:
        return "TIMEOUT", False

    if soft_fail_network and "curated skill catalog" in label.lower():
        lowered = output.lower()
        if any(marker in lowered for marker in NETWORK_WARNING_MARKERS):
            return "WARN", True

    return "FAIL", False


def _read_json_file(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_resume_commands(
    status_path: Path,
    *,
    failed_only: bool,
    current_fail_on_warn: bool,
) -> tuple[list[tuple[str, list[str]]], int, list[dict[str, object]]]:
    payload = _read_json_file(status_path)
    rows = payload.get("results", [])
    if not isinstance(rows, list):
        raise SystemExit(f"resume status file has no results list: {status_path}")

    prior_fail_on_warn = bool(
        isinstance(payload.get("config"), dict) and payload["config"].get("fail_on_warn")
    )
    selected: list[tuple[str, list[str]]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        label = str(row.get("label") or "").strip()
        command_str = str(row.get("command") or "").strip()
        status = _normalize_status_token(row.get("status"))
        if failed_only:
            unresolved = status in {"FAIL", "TIMEOUT"} or (
                status == "WARN" and (prior_fail_on_warn or current_fail_on_warn)
            )
            if not unresolved:
                continue
        if not label or not command_str:
            raise SystemExit(f"resume status row missing label/command in {status_path}")
        selected.append((label, shlex.split(command_str)))
    baseline_rows = [row for row in rows if isinstance(row, dict)]
    return selected, len(selected), baseline_rows


def _normalize_status_token(raw: object) -> str:
    text = str(raw or "").strip().upper()
    if text in {"PASS", "WARN", "FAIL", "TIMEOUT"}:
        return text
    return "FAIL"


def _dirty_tree_state() -> dict[str, object]:
    def _count_lines(args: list[str]) -> tuple[int, bool]:
        try:
            proc = subprocess.run(
                args,
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
                timeout=45,
            )
        except subprocess.TimeoutExpired:
            return 0, False
        if proc.returncode != 0:
            return 0, False
        count = len([line for line in proc.stdout.splitlines() if line.strip()])
        return count, True

    staged, staged_ok = _count_lines(["git", "diff", "--cached", "--name-only"])
    unstaged, unstaged_ok = _count_lines(["git", "diff", "--name-only"])
    untracked, untracked_ok = _count_lines(["git", "ls-files", "--others", "--exclude-standard"])
    available = staged_ok and unstaged_ok and untracked_ok
    dirty = any((staged, unstaged, untracked)) if available else None
    return {
        "available": available,
        "staged_count": staged,
        "unstaged_count": unstaged,
        "untracked_count": untracked,
        "dirty": dirty,
    }


def _storage_prune_delta_mb() -> float:
    path = ROOT / "docs" / "trinity-storage-prune-latest.json"
    if not path.exists():
        return 0.0
    try:
        payload = _read_json_file(path)
    except Exception:  # noqa: BLE001
        return 0.0
    return float(payload.get("reclaimed_mb", 0.0) or 0.0)


def _merge_resume_results(
    baseline_rows: list[dict[str, object]],
    resumed_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    replacement_map = {
        str(row.get("label") or "").strip(): row
        for row in resumed_rows
        if isinstance(row, dict) and str(row.get("label") or "").strip()
    }
    merged: list[dict[str, object]] = []
    seen: set[str] = set()
    for row in baseline_rows:
        label = str(row.get("label") or "").strip()
        if label and label in replacement_map:
            merged.append(replacement_map[label])
            seen.add(label)
        else:
            merged.append(row)
            if label:
                seen.add(label)
    for row in resumed_rows:
        label = str(row.get("label") or "").strip()
        if label and label not in seen:
            merged.append(row)
            seen.add(label)
    return merged


def _write_interim_suite_status(
    path: Path,
    suite_results: list[dict[str, object]],
    *,
    checkpoint_class: str,
    shared_latest_eligible: bool,
    suite_started_at_utc: str | None = None,
    suite_finished_at_utc: str | None = None,
    suite_duration_sec: float | None = None,
) -> None:
    pass_count = sum(1 for item in suite_results if item["status"] == "PASS")
    warn_count = sum(1 for item in suite_results if item["status"] == "WARN")
    timeout_count = sum(1 for item in suite_results if item["status"] == "TIMEOUT")
    fail_count = sum(1 for item in suite_results if item["status"] == "FAIL")
    payload = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "checkpoint_class": checkpoint_class,
        "shared_latest_eligible": shared_latest_eligible,
        "effective_success": all(bool(item["effective_success"]) for item in suite_results),
        "counts": {
            "pass": pass_count,
            "warn": warn_count,
            "timeout": timeout_count,
            "fail": fail_count,
        },
        "results": suite_results,
    }
    if suite_started_at_utc is not None:
        payload["suite_started_at_utc"] = suite_started_at_utc
    if suite_finished_at_utc is not None:
        payload["suite_finished_at_utc"] = suite_finished_at_utc
    if suite_duration_sec is not None:
        payload["suite_duration_sec"] = round(suite_duration_sec, 3)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _replace_suite_result(
    suite_results: list[dict[str, object]],
    label: str,
    row: dict[str, object],
) -> None:
    for index, existing in enumerate(suite_results):
        if str(existing.get("label") or "") == label:
            suite_results[index] = row
            return
    suite_results.append(row)


def _run_post_suite_refresh(
    *,
    label: str,
    base_command: list[str],
    args: argparse.Namespace,
    soft_fail_network: bool,
    status_json_path: Path,
    control_tower_json_path: Path,
    control_tower_md_path: Path,
    scoreboard_latest_json: Path,
    scoreboard_latest_md: Path,
    checkpoint_class: str,
) -> tuple[dict[str, object], str]:
    effective_cmd = list(base_command)
    if label == "v17 evidence-first control tower sync":
        status_arg = str(status_json_path.relative_to(ROOT)).replace("\\", "/")
        if "--suite-status" not in effective_cmd:
            effective_cmd.extend(["--suite-status", status_arg])
        if "--control-tower-json" not in effective_cmd:
            effective_cmd.extend(["--control-tower-json", str(control_tower_json_path.relative_to(ROOT)).replace("\\", "/")])
        if "--control-tower-md" not in effective_cmd:
            effective_cmd.extend(["--control-tower-md", str(control_tower_md_path.relative_to(ROOT)).replace("\\", "/")])
        if "--checkpoint-class" not in effective_cmd:
            effective_cmd.extend(["--checkpoint-class", checkpoint_class])
    if label == "trinity mandala scoreboard":
        status_arg = str(status_json_path.relative_to(ROOT)).replace("\\", "/")
        if "--suite-status" not in effective_cmd:
            effective_cmd.extend(["--suite-status", status_arg])
        if "--latest-json" not in effective_cmd:
            effective_cmd.extend(["--latest-json", str(scoreboard_latest_json.relative_to(ROOT)).replace("\\", "/")])
        if "--latest-md" not in effective_cmd:
            effective_cmd.extend(["--latest-md", str(scoreboard_latest_md.relative_to(ROOT)).replace("\\", "/")])
        if "--control-tower-path" not in effective_cmd:
            effective_cmd.extend(["--control-tower-path", str(control_tower_json_path.relative_to(ROOT)).replace("\\", "/")])
        if "--checkpoint-class" not in effective_cmd:
            effective_cmd.extend(["--checkpoint-class", checkpoint_class])
    ok, output, timed_out, duration_sec, started_at, finished_at = run_command(effective_cmd, args.step_timeout_sec)
    status, counted_success = classify_status(
        label=label,
        ok=ok,
        timed_out=timed_out,
        output=output,
        soft_fail_network=soft_fail_network,
    )
    row = {
        "label": label,
        "status": status,
        "ok": ok,
        "effective_success": counted_success,
        "timed_out": timed_out,
        "started_at_utc": started_at,
        "finished_at_utc": finished_at,
        "duration_sec": round(duration_sec, 3),
        "command": shlex.join(effective_cmd),
    }
    return row, output[:8000]


def main() -> None:
    parser = argparse.ArgumentParser(description="Run all available Trinity systems")
    parser.add_argument(
        "--step-timeout-sec",
        type=int,
        default=0,
        help="Per-command timeout in seconds (0 disables timeout / no limit).",
    )
    parser.add_argument(
        "--profile",
        choices=("standard", "quick", "deep", "collab", "materialize", "recover"),
        default="deep",
        help=(
            "Execution profile: deep (default expanded run), standard (base stages), quick (continuity-focused subset), collab (standard + verified MCP refresh), "
            "materialize (standard + disposable staging write tracers), recover (low-pressure validators + v14 recovery gates), "
            "deep (standard + version scan + skill install + curated catalog + soft-fail-network)."
        ),
    )
    parser.add_argument(
        "--include-skill-install",
        action="store_true",
        help="Include local Trinity skill installation in the suite run.",
    )
    parser.add_argument(
        "--include-version-scan",
        action="store_true",
        help="Include v29-v33 cross-version scan stages (PDF, DOCX, ZIP).",
    )
    parser.add_argument(
        "--include-curated-skill-catalog",
        action="store_true",
        help="Include curated skill catalog snapshot from the system skill-installer utility.",
    )
    parser.add_argument(
        "--include-public-api-refresh",
        action="store_true",
        help="Deprecated compatibility alias; standard/deep already include live API refresh by default.",
    )
    parser.add_argument(
        "--include-mcp-refresh",
        action="store_true",
        help="Enable verified-live MCP collaboration refresh for eligible pack systems.",
    )
    parser.add_argument(
        "--include-staged-connectors",
        action="store_true",
        help="Attempt staged connector live refresh only after setup-gate detection passes.",
    )
    parser.add_argument(
        "--include-live-writes",
        action="store_true",
        help="Enable disposable staging write tracers; materialize profile turns this on automatically unless offline-only is set.",
    )
    parser.add_argument(
        "--materialization-level",
        choices=("l1_disposable_staging", "l2_persistent_dev", "l3_uat_preprod", "l4_standard_prod", "l5_ha_prod"),
        default="l2_persistent_dev",
        help="Desired materialization level for materialize profile runs.",
    )
    parser.add_argument(
        "--offline-only",
        action="store_true",
        help="Disable all live network refresh steps and force cache-only expansion/API execution.",
    )
    parser.add_argument(
        "--soft-fail-network",
        action="store_true",
        help="Downgrade expected network-restricted curated-catalog failures to WARN.",
    )
    parser.add_argument(
        "--fail-on-warn",
        action="store_true",
        help="Treat WARN outcomes as overall failure for stricter governance/CI gating.",
    )
    parser.add_argument(
        "--achievement-target-steps",
        type=int,
        default=0,
        help="Minimum number of successful steps required before suite can finish as successful (0 disables).",
    )
    parser.add_argument(
        "--quick-mode",
        action="store_true",
        help="Run a lightweight continuity-focused subset of suite checks for fast message cadence.",
    )
    parser.add_argument(
        "--list-profiles",
        action="store_true",
        help="Print available execution profiles and exit.",
    )
    parser.add_argument(
        "--skip-body-benchmark",
        action="store_true",
        help="Skip body_track_runner benchmark guardrail stage.",
    )
    parser.add_argument(
        "--skip-v166-v180-dashboard-run",
        action="store_true",
        help="Legacy no-op. The v166-v180 runner remains directly callable but is no longer the latest default low-live suite hook.",
    )
    parser.add_argument(
        "--skip-v181-v200-cross-app-council-run",
        action="store_true",
        help="Legacy no-op. The v181-v200 runner remains directly callable but is no longer the latest default low-live suite hook.",
    )
    parser.add_argument(
        "--skip-v201-v220-cross-app-council-run",
        action="store_true",
        help="Skip the latest v201-v220 low-live cross-app council runner that deep and L5 materialize runs include by default.",
    )
    parser.add_argument(
        "--body-benchmark-mode",
        choices=("auto", "off", "observe", "enforce"),
        default="auto",
        help=(
            "Benchmark guardrail mode: auto (quick=observe, standard/deep=enforce), "
            "off, observe, or enforce."
        ),
    )
    default_status_arg = str(SHARED_STATUS_JSON.relative_to(ROOT))
    parser.add_argument(
        "--status-json",
        default=default_status_arg,
        help="Path to write machine-readable suite status JSON (relative to repo root).",
    )
    parser.add_argument(
        "--resume-failed-only",
        action="store_true",
        help="Replay only failed or timed-out steps from a prior suite status file.",
    )
    parser.add_argument(
        "--resume-from-status",
        default="",
        help="Replay commands from a specific prior suite status JSON (relative to repo root unless absolute).",
    )
    args = parser.parse_args()

    if args.list_profiles:
        print(render_profile_catalog())
        raise SystemExit(0)

    if args.step_timeout_sec < 0:
        raise SystemExit("--step-timeout-sec must be >= 0")
    if args.achievement_target_steps < 0:
        raise SystemExit("--achievement-target-steps must be >= 0")

    resume_status_path: Path | None = None

    (
        profile,
        include_version_scan,
        include_skill_install,
        include_curated_skill_catalog,
        include_public_api_refresh,
        include_mcp_refresh,
        include_staged_connectors,
        include_live_writes,
        offline_only,
        soft_fail_network,
        profile_source,
        body_benchmark_mode,
    ) = resolve_profile_settings(args)

    default_status_requested = args.status_json == default_status_arg
    if default_status_requested and profile == "quick":
        status_json_path = V17_QUICK_STATUS_JSON
    else:
        status_json_path = (ROOT / args.status_json).resolve()
    try:
        status_json_path.relative_to(ROOT)
    except ValueError as exc:
        raise SystemExit("--status-json must remain within repository root") from exc

    if profile == "quick":
        report_path = V17_QUICK_REPORT
        control_tower_json_path = V17_CONTROL_TOWER_JSON
        control_tower_md_path = V17_CONTROL_TOWER_MD
        scoreboard_latest_json = V17_SCOREBOARD_JSON
        scoreboard_latest_md = V17_SCOREBOARD_MD
        checkpoint_class = "v17_evidence_first_quick_lane"
        shared_latest_eligible = False
        latest_surface_scope = "v17_specific_latest"
    else:
        report_path = SHARED_REPORT
        control_tower_json_path = SHARED_CONTROL_TOWER_JSON
        control_tower_md_path = ROOT / "docs" / "trinity-control-tower-latest.md"
        scoreboard_latest_json = SHARED_SCOREBOARD_JSON
        scoreboard_latest_md = SHARED_SCOREBOARD_MD
        checkpoint_class = "shared_full_suite_authority"
        shared_latest_eligible = True
        latest_surface_scope = "shared_latest"

    if args.resume_from_status:
        candidate = Path(args.resume_from_status)
        resume_status_path = candidate if candidate.is_absolute() else (ROOT / candidate).resolve()
        if not resume_status_path.exists():
            raise SystemExit(f"--resume-from-status not found: {resume_status_path}")
    elif args.resume_failed_only:
        resume_status_path = status_json_path if status_json_path.exists() else SHARED_STATUS_JSON
        if not resume_status_path.exists():
            raise SystemExit("no suite status file available for --resume-failed-only")

    effective_achievement_target = args.achievement_target_steps
    if effective_achievement_target == 0 and profile == "deep":
        effective_achievement_target = 10

    commands = build_commands(
        include_skill_install=include_skill_install,
        include_version_scan=include_version_scan,
        include_curated_skill_catalog=include_curated_skill_catalog,
        include_public_api_refresh=include_public_api_refresh,
        include_mcp_refresh=include_mcp_refresh,
        include_staged_connectors=include_staged_connectors,
        include_live_writes=include_live_writes,
        offline_only=offline_only,
        quick_mode=(profile == "quick"),
        profile=profile,
        body_benchmark_mode=body_benchmark_mode,
        materialization_level=args.materialization_level,
        skip_v166_v180_dashboard_run=args.skip_v166_v180_dashboard_run,
        skip_v181_v200_cross_app_council_run=args.skip_v181_v200_cross_app_council_run,
        skip_v201_v220_cross_app_council_run=args.skip_v201_v220_cross_app_council_run,
    )
    resumed_step_count = 0
    recovery_parent_run = ""
    recovery_mode = "disabled"
    resume_baseline_results: list[dict[str, object]] = []
    if resume_status_path is not None:
        commands, resumed_step_count, resume_baseline_results = _load_resume_commands(
            resume_status_path,
            failed_only=args.resume_failed_only,
            current_fail_on_warn=args.fail_on_warn,
        )
        try:
            recovery_parent_run = str(resume_status_path.relative_to(ROOT)).replace("\\", "/")
        except ValueError:
            recovery_parent_run = str(resume_status_path)
        recovery_mode = "resume_failed_only" if args.resume_failed_only else "resume_from_status"
    elif profile == "recover":
        recovery_mode = "recover_profile"
    original_commands = {label: list(cmd) for label, cmd in commands}
    mcp_catalog_path = ROOT / TRINITY_MCP_CATALOG_PATH
    verified_mcp_connectors: list[str] = []
    verified_app_connectors: list[str] = []
    verified_composio_toolkits: list[str] = []
    eligible_live_write_connectors: list[str] = []
    promoted_live_write_connectors: list[str] = []
    blocked_promotions: list[str] = []
    if mcp_catalog_path.exists():
        try:
            mcp_payload = json.loads(mcp_catalog_path.read_text(encoding="utf-8"))
            connector_rows = mcp_payload.get("connectors", [])
            if isinstance(connector_rows, list):
                def _connector_class(row: dict[str, object]) -> str:
                    explicit = str(row.get("connector_class") or "").strip().lower()
                    if explicit:
                        return explicit
                    tool_surface = str(row.get("tool_surface") or "").strip().lower()
                    if tool_surface in {"desktop_mcp_tool", "docker_local"}:
                        return "direct_mcp"
                    if tool_surface in {"composio_toolkit", "composio_bridge"}:
                        return "composio_toolkit"
                    if tool_surface in {"git_https_remote", "connector_setup_gate", "docker_run_mcp_gdrive"}:
                        return "app_connector"
                    if tool_surface in {"local_skill_cli"}:
                        return "runtime_surface"
                    return "app_connector"

                for row in connector_rows:
                    if not isinstance(row, dict):
                        continue
                    connector_id = str(row.get("mcp_id") or "").strip()
                    if not connector_id or not bool(row.get("live_read_enabled")):
                        continue
                    connector_class = _connector_class(row)
                    if connector_class in {"direct_mcp", "runtime_surface"}:
                        verified_mcp_connectors.append(connector_id)
                    elif connector_class == "composio_toolkit":
                        verified_composio_toolkits.append(connector_id)
                    else:
                        verified_app_connectors.append(connector_id)

                verified_mcp_connectors = sorted(dict.fromkeys(verified_mcp_connectors))
                verified_app_connectors = sorted(dict.fromkeys(verified_app_connectors))
                verified_composio_toolkits = sorted(dict.fromkeys(verified_composio_toolkits))
                eligible_live_write_connectors = sorted(
                    str(row.get("mcp_id"))
                    for row in connector_rows
                    if isinstance(row, dict) and "write" in str(row.get("desired_state") or "")
                )
                promoted_live_write_connectors = sorted(
                    str(row.get("mcp_id"))
                    for row in connector_rows
                    if isinstance(row, dict) and bool(row.get("live_write_enabled"))
                )
                blocked_promotions = sorted(
                    str(row.get("mcp_id"))
                    for row in connector_rows
                    if isinstance(row, dict) and "write" in str(row.get("desired_state") or "") and not bool(row.get("live_write_enabled"))
                )
        except json.JSONDecodeError:
            verified_mcp_connectors = []
            verified_app_connectors = []
            verified_composio_toolkits = []
            eligible_live_write_connectors = []
            promoted_live_write_connectors = []
            blocked_promotions = []
    manifest_pack_count = 0
    materialization_pack_count = 0
    manifest_path = ROOT / TRINITY_EXPANSION_MANIFEST_PATH
    if manifest_path.exists():
        try:
            manifest_payload = json.loads(manifest_path.read_text(encoding="utf-8"))
            system_rows = manifest_payload.get("systems", [])
            if isinstance(system_rows, list):
                pack_names = {
                    str(row.get("pack"))
                    for row in system_rows
                    if isinstance(row, dict) and str(row.get("pack") or "").strip()
                }
                manifest_pack_count = len(pack_names)
                materialization_pack_count = len(
                    {
                        str(row.get("pack"))
                        for row in system_rows
                        if isinstance(row, dict) and str(row.get("track") or "") == "materialization_ladder"
                    }
                )
        except json.JSONDecodeError:
            manifest_pack_count = 0
            materialization_pack_count = 0
    if offline_only:
        live_network_mode = "offline_only"
    elif include_public_api_refresh or include_mcp_refresh or include_live_writes:
        live_network_mode = "live_opt_in"
    else:
        live_network_mode = "offline_default"
    if offline_only:
        mcp_refresh_mode = "offline_only"
        staged_connector_mode = "offline_only"
    else:
        mcp_refresh_mode = "verified_live" if include_mcp_refresh else "disabled"
        staged_connector_mode = "setup_gate_attempted" if include_staged_connectors else "staged_only"
    collab_pack_count = manifest_pack_count
    if offline_only:
        active_materialization_mode = "offline_only"
    elif include_live_writes:
        active_materialization_mode = args.materialization_level
    else:
        active_materialization_mode = "read_only"

    def _read_status_value(path_str: str, key: str, fallback: object) -> object:
        try:
            payload = json.loads((ROOT / path_str).read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            return fallback
        return payload.get(key, fallback) if isinstance(payload, dict) else fallback

    suite_started_at = datetime.now(timezone.utc).isoformat()
    suite_start_ts = time.monotonic()

    lines = [
        "# Trinity System Suite Run Report",
        "",
        f"Generated: {suite_started_at}",
        f"Step timeout (s): {args.step_timeout_sec if args.step_timeout_sec > 0 else 'disabled'}",
        f"Profile: {profile}",
        f"Profile source: {profile_source}",
        f"Include version scan: {include_version_scan}",
        f"Include skill install: {include_skill_install}",
        f"Include curated skill catalog: {include_curated_skill_catalog}",
        f"Include public api refresh: {include_public_api_refresh}",
        f"Include mcp refresh: {include_mcp_refresh}",
        f"Include staged connectors: {include_staged_connectors}",
        f"Include live writes: {include_live_writes}",
        f"Materialization level desired: {args.materialization_level}",
        f"Offline only: {offline_only}",
        f"Live network mode: {live_network_mode}",
        f"MCP refresh mode: {mcp_refresh_mode}",
        f"Staged connector mode: {staged_connector_mode}",
        f"Active materialization mode: {active_materialization_mode}",
        f"Soft-fail network: {soft_fail_network}",
        f"Fail on warn: {args.fail_on_warn}",
        f"Achievement target steps: {effective_achievement_target if effective_achievement_target > 0 else 'disabled'}",
        f"Quick mode: {profile == 'quick'}",
        f"Body benchmark mode: {body_benchmark_mode}",
        f"Report path: {report_path.relative_to(ROOT)}",
        f"Status JSON path: {status_json_path.relative_to(ROOT)}",
        f"Checkpoint class: {checkpoint_class}",
        f"Shared latest eligible: {shared_latest_eligible}",
        f"Latest surface scope: {latest_surface_scope}",
        "",
        "This report runs currently available repo systems and records command outputs.",
        "",
    ]

    suite_results: list[dict[str, object]] = []

    for label, cmd in commands:
        effective_cmd = list(cmd)
        if label == "trinity mandala scoreboard":
            interim_results = suite_results
            if resume_baseline_results:
                interim_results = _merge_resume_results(resume_baseline_results, suite_results)
            _write_interim_suite_status(
                status_json_path,
                interim_results,
                checkpoint_class=checkpoint_class,
                shared_latest_eligible=shared_latest_eligible,
            )
            status_arg = str(status_json_path.relative_to(ROOT)).replace("\\", "/")
            if "--suite-status" not in effective_cmd:
                effective_cmd.extend(["--suite-status", status_arg])
            if "--latest-json" not in effective_cmd:
                effective_cmd.extend(["--latest-json", str(scoreboard_latest_json.relative_to(ROOT)).replace("\\", "/")])
            if "--latest-md" not in effective_cmd:
                effective_cmd.extend(["--latest-md", str(scoreboard_latest_md.relative_to(ROOT)).replace("\\", "/")])
            if "--control-tower-path" not in effective_cmd:
                effective_cmd.extend(["--control-tower-path", str(control_tower_json_path.relative_to(ROOT)).replace("\\", "/")])
            if "--checkpoint-class" not in effective_cmd:
                effective_cmd.extend(["--checkpoint-class", checkpoint_class])
        if label == "v17 evidence-first control tower sync":
            status_arg = str(status_json_path.relative_to(ROOT)).replace("\\", "/")
            if "--suite-status" not in effective_cmd:
                effective_cmd.extend(["--suite-status", status_arg])
            if "--control-tower-json" not in effective_cmd:
                effective_cmd.extend(["--control-tower-json", str(control_tower_json_path.relative_to(ROOT)).replace("\\", "/")])
            if "--control-tower-md" not in effective_cmd:
                effective_cmd.extend(["--control-tower-md", str(control_tower_md_path.relative_to(ROOT)).replace("\\", "/")])
            if "--checkpoint-class" not in effective_cmd:
                effective_cmd.extend(["--checkpoint-class", checkpoint_class])
        ok, output, timed_out, duration_sec, started_at, finished_at = run_command(effective_cmd, args.step_timeout_sec)
        status, counted_success = classify_status(
            label=label,
            ok=ok,
            timed_out=timed_out,
            output=output,
            soft_fail_network=soft_fail_network,
        )
        command_str = shlex.join(effective_cmd)
        suite_results.append(
            {
                "label": label,
                "status": status,
                "ok": ok,
                "effective_success": counted_success,
                "timed_out": timed_out,
                "started_at_utc": started_at,
                "finished_at_utc": finished_at,
                "duration_sec": round(duration_sec, 3),
                "command": command_str,
            }
        )
        lines.append(f"## {label}")
        lines.append(f"- status: **{status}**")
        lines.append(f"- command: `{command_str}`")
        lines.append(f"- started: `{started_at}`")
        lines.append(f"- finished: `{finished_at}`")
        lines.append(f"- duration_sec: `{duration_sec:.3f}`")
        lines.append("```text")
        lines.append(output[:8000])
        lines.append("```")
        lines.append("")

    if resume_baseline_results:
        suite_results = _merge_resume_results(resume_baseline_results, suite_results)

    frozen_suite_finished_at = datetime.now(timezone.utc).isoformat()
    frozen_suite_duration_sec = time.monotonic() - suite_start_ts

    _write_interim_suite_status(
        status_json_path,
        suite_results,
        checkpoint_class=checkpoint_class,
        shared_latest_eligible=shared_latest_eligible,
        suite_started_at_utc=suite_started_at,
        suite_finished_at_utc=frozen_suite_finished_at,
        suite_duration_sec=frozen_suite_duration_sec,
    )

    post_suite_refresh_labels = [
        "expansion: body_resource_envelope_guard (offline)",
        "v17 evidence-first control tower sync",
        "trinity mandala scoreboard",
    ]
    for refresh_label in post_suite_refresh_labels:
        base_command = original_commands.get(refresh_label)
        if not base_command:
            continue
        refreshed_row, refreshed_output = _run_post_suite_refresh(
            label=refresh_label,
            base_command=base_command,
            args=args,
            soft_fail_network=soft_fail_network,
            status_json_path=status_json_path,
            control_tower_json_path=control_tower_json_path,
            control_tower_md_path=control_tower_md_path,
            scoreboard_latest_json=scoreboard_latest_json,
            scoreboard_latest_md=scoreboard_latest_md,
            checkpoint_class=checkpoint_class,
        )
        _replace_suite_result(suite_results, refresh_label, refreshed_row)
        lines.append(f"## {refresh_label} (post-run refresh)")
        lines.append(f"- status: **{refreshed_row['status']}**")
        lines.append(f"- command: `{refreshed_row['command']}`")
        lines.append(f"- started: `{refreshed_row['started_at_utc']}`")
        lines.append(f"- finished: `{refreshed_row['finished_at_utc']}`")
        lines.append(f"- duration_sec: `{refreshed_row['duration_sec']}`")
        lines.append("```text")
        lines.append(refreshed_output)
        lines.append("```")
        lines.append("")
        _write_interim_suite_status(
            status_json_path,
            suite_results,
            checkpoint_class=checkpoint_class,
            shared_latest_eligible=shared_latest_eligible,
            suite_started_at_utc=suite_started_at,
            suite_finished_at_utc=frozen_suite_finished_at,
            suite_duration_sec=frozen_suite_duration_sec,
        )

    pass_count = sum(1 for item in suite_results if item["status"] == "PASS")
    warn_count = sum(1 for item in suite_results if item["status"] == "WARN")
    timeout_count = sum(1 for item in suite_results if item["status"] == "TIMEOUT")
    fail_count = sum(1 for item in suite_results if item["status"] == "FAIL")
    expansion_results = [item for item in suite_results if str(item.get("label", "")).startswith("expansion: ")]
    expansion_total = len(expansion_results)
    expansion_passed = sum(1 for item in expansion_results if item["status"] == "PASS")
    effective_success = all(bool(item["effective_success"]) for item in suite_results)
    if args.fail_on_warn and warn_count > 0:
        effective_success = False

    achieved_steps = sum(1 for item in suite_results if bool(item["effective_success"]))
    achievement_gate_met = (
        effective_achievement_target == 0 or achieved_steps >= effective_achievement_target
    )
    if not achievement_gate_met:
        effective_success = False

    suite_finished_at = frozen_suite_finished_at
    suite_duration_sec = frozen_suite_duration_sec
    current_session_surface = _read_status_value(
        "docs/logs/system-wake-v2.json",
        "current_session_surface",
        _read_status_value("docs/logs/system-wake-v1.json", "current_session_surface", {}),
    )
    dirty_tree_state = _dirty_tree_state()
    storage_prune_delta_mb = _storage_prune_delta_mb()
    connector_hardening_state = _read_status_value("docs/trinity-expansion/connector-materialization-gate-latest.json", "overall_status", "FAIL")
    autonomy_mode = "bounded_manual" if profile != "materialize" else "bounded_materialize"
    control_plane_mode = "hybrid_app_mcp_runtime"
    knowledge_graph_state = _read_status_value("docs/trinity-expansion/code-knowledge-graph-gate-latest.json", "overall_status", "FAIL")
    dashboard_state = _read_status_value("docs/trinity-expansion/trinity-dashboard-gate-latest.json", "overall_status", "FAIL")
    future_readiness_state = _read_status_value("docs/trinity-expansion/future-readiness-gate-latest.json", "overall_status", "FAIL")
    materialization_level_desired = args.materialization_level
    control_tower_status_path = str(control_tower_json_path.relative_to(ROOT)).replace("\\", "/")
    materialization_level_actual = _read_status_value(control_tower_status_path, "materialization_level_actual", "readiness_only")
    google_drive_state = _read_status_value(control_tower_status_path, "google_drive_state", "operator_hold")
    external_live_overlay_state = _read_status_value(control_tower_status_path, "external_live_overlay_state", "awaiting_thread_boot")
    runtime_session_state = _read_status_value(control_tower_status_path, "runtime_session_state", "FAIL")
    runtime_truth_complete = bool(_read_status_value(control_tower_status_path, "runtime_truth_complete", False))
    external_establishment_criteria_state = _read_status_value(control_tower_status_path, "external_establishment_criteria_state", "FAIL")
    standards_bridge_state = _read_status_value(control_tower_status_path, "standards_bridge_state", "FAIL")
    filesystem_promotion_state = _read_status_value(control_tower_status_path, "filesystem_promotion_state", "blocked")
    filesystem_connector_actual_state = _read_status_value(control_tower_status_path, "filesystem_connector_actual_state", "unknown")
    claim_boundary_state = _read_status_value(control_tower_status_path, "claim_boundary_state", "FAIL")
    v17_evidence_first_state = _read_status_value(control_tower_status_path, "v17_evidence_first_state", "FAIL")
    persistent_targets = _read_status_value("docs/trinity-persistent-dev-targets-v2.json", "targets", _read_status_value("docs/trinity-persistent-dev-targets-v1.json", "targets", []))
    persistent_target_count = len(persistent_targets) if isinstance(persistent_targets, list) else 0
    command_surface_state = _read_status_value("docs/trinity-command-book-validation-latest.json", "overall_status", "FAIL")
    identity_authority_state = _read_status_value("docs/trinity-expansion/identity-authority-v7-gate-latest.json", "overall_status", "FAIL")
    memory_mirror_state = _read_status_value("docs/trinity-memory-mirror-state-v1.json", "divergence_status", "FAIL")
    council_state = _read_status_value("docs/trinity-agent-council-validation-latest.json", "overall_status", "FAIL")
    provisional_agent_count = int(_read_status_value("docs/trinity-agent-council-validation-latest.json", "provisional_agent_count", 0) or 0)
    duo_chat_count = int(_read_status_value("docs/trinity-agent-council-validation-latest.json", "duo_chat_count", 0) or 0)
    group_chat_state = "PASS" if (ROOT / "docs" / "trinity-agent-council-group-chat-v5.jsonl").exists() else "FAIL"
    late_step_autonomy_state = _read_status_value(
        "docs/trinity-expansion/cloud-staging-readiness-v8-gate-latest.json",
        "overall_status",
        _read_status_value(control_tower_status_path, "late_step_autonomy_state", "FAIL"),
    )

    lines.append("## Overall status")
    lines.append(f"- Effective success: **{effective_success}**")
    lines.append(f"- PASS: **{pass_count}**")
    lines.append(f"- WARN: **{warn_count}**")
    lines.append(f"- TIMEOUT: **{timeout_count}**")
    lines.append(f"- FAIL: **{fail_count}**")
    lines.append(f"- Expansion systems total: **{expansion_total}**")
    lines.append(f"- Expansion systems passed: **{expansion_passed}**")
    lines.append(f"- Collab pack count: **{collab_pack_count}**")
    lines.append(f"- Materialization pack count: **{materialization_pack_count}**")
    lines.append(f"- Materialization level desired: **{materialization_level_desired}**")
    lines.append(f"- Materialization level actual: **{materialization_level_actual}**")
    lines.append(f"- Google Drive state: **{google_drive_state}**")
    lines.append(f"- External live overlay state: **{external_live_overlay_state}**")
    lines.append(f"- Runtime session state: **{runtime_session_state}**")
    lines.append(f"- Runtime truth complete: **{runtime_truth_complete}**")
    lines.append(f"- External establishment criteria state: **{external_establishment_criteria_state}**")
    lines.append(f"- Standards bridge state: **{standards_bridge_state}**")
    lines.append(f"- Claim boundary state: **{claim_boundary_state}**")
    lines.append(f"- V17 evidence-first state: **{v17_evidence_first_state}**")
    lines.append(f"- Filesystem connector actual state: **{filesystem_connector_actual_state}**")
    lines.append(f"- Filesystem promotion state: **{filesystem_promotion_state}**")
    lines.append(f"- Persistent target count: **{persistent_target_count}**")
    lines.append(f"- Command surface state: **{command_surface_state}**")
    lines.append(f"- Council state: **{council_state}**")
    lines.append(f"- Provisional agent count: **{provisional_agent_count}**")
    lines.append(f"- Group chat state: **{group_chat_state}**")
    lines.append(f"- Duo chat count: **{duo_chat_count}**")
    lines.append(f"- Identity authority state: **{identity_authority_state}**")
    lines.append(f"- Memory mirror state: **{memory_mirror_state}**")
    lines.append(f"- Late-step autonomy state: **{late_step_autonomy_state}**")
    lines.append(f"- Eligible live write connectors: **{', '.join(eligible_live_write_connectors) if eligible_live_write_connectors else '-'}**")
    lines.append(f"- Promoted live write connectors: **{', '.join(promoted_live_write_connectors) if promoted_live_write_connectors else '-'}**")
    lines.append(f"- Blocked promotions: **{', '.join(blocked_promotions) if blocked_promotions else '-'}**")
    lines.append(f"- Control plane mode: **{control_plane_mode}**")
    lines.append(f"- Verified MCP connectors: **{', '.join(verified_mcp_connectors) if verified_mcp_connectors else '-'}**")
    lines.append(f"- Verified app connectors: **{', '.join(verified_app_connectors) if verified_app_connectors else '-'}**")
    lines.append(f"- Verified Composio toolkits: **{', '.join(verified_composio_toolkits) if verified_composio_toolkits else '-'}**")
    lines.append(f"- Achieved steps: **{achieved_steps}**")
    lines.append(f"- Achievement gate met: **{achievement_gate_met}**")
    lines.append(f"- Suite started: `{suite_started_at}`")
    lines.append(f"- Suite finished: `{suite_finished_at}`")
    lines.append(f"- Suite duration_sec: `{suite_duration_sec:.3f}`")
    lines.append("")

    status_payload = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "suite_started_at_utc": suite_started_at,
        "suite_finished_at_utc": suite_finished_at,
        "suite_duration_sec": round(suite_duration_sec, 3),
        "effective_success": effective_success,
        "achieved_steps": achieved_steps,
        "achievement_gate_met": achievement_gate_met,
        "counts": {
            "pass": pass_count,
            "warn": warn_count,
            "timeout": timeout_count,
            "fail": fail_count,
        },
        "checkpoint_class": checkpoint_class,
        "shared_latest_eligible": shared_latest_eligible,
        "latest_surface_scope": latest_surface_scope,
        "expansion_systems_total": expansion_total,
        "expansion_systems_passed": expansion_passed,
        "collab_pack_count": collab_pack_count,
        "materialization_pack_count": materialization_pack_count,
        "control_plane_mode": control_plane_mode,
        "verified_mcp_connectors": verified_mcp_connectors,
        "verified_app_connectors": verified_app_connectors,
        "verified_composio_toolkits": verified_composio_toolkits,
        "eligible_live_write_connectors": eligible_live_write_connectors,
        "promoted_live_write_connectors": promoted_live_write_connectors,
        "blocked_promotions": blocked_promotions,
        "active_materialization_mode": active_materialization_mode,
        "mcp_refresh_mode": mcp_refresh_mode,
        "staged_connector_mode": staged_connector_mode,
        "current_session_surface": current_session_surface,
        "connector_hardening_state": connector_hardening_state,
        "autonomy_mode": autonomy_mode,
        "knowledge_graph_state": knowledge_graph_state,
        "dashboard_state": dashboard_state,
        "future_readiness_state": future_readiness_state,
        "materialization_level_desired": materialization_level_desired,
        "materialization_level_actual": materialization_level_actual,
        "google_drive_state": google_drive_state,
        "external_live_overlay_state": external_live_overlay_state,
        "runtime_session_state": runtime_session_state,
        "runtime_truth_complete": runtime_truth_complete,
        "external_establishment_criteria_state": external_establishment_criteria_state,
        "standards_bridge_state": standards_bridge_state,
        "filesystem_promotion_state": filesystem_promotion_state,
        "filesystem_connector_actual_state": filesystem_connector_actual_state,
        "claim_boundary_state": claim_boundary_state,
        "v17_evidence_first_state": v17_evidence_first_state,
        "persistent_target_count": persistent_target_count,
        "command_surface_state": command_surface_state,
        "council_state": council_state,
        "provisional_agent_count": provisional_agent_count,
        "group_chat_state": group_chat_state,
        "duo_chat_count": duo_chat_count,
        "identity_authority_state": identity_authority_state,
        "memory_mirror_state": memory_mirror_state,
        "late_step_autonomy_state": late_step_autonomy_state,
        "recovery_parent_run": recovery_parent_run,
        "recovery_mode": recovery_mode,
        "dirty_tree_state": dirty_tree_state,
        "storage_prune_delta_mb": round(storage_prune_delta_mb, 2),
        "resumed_step_count": resumed_step_count,
        "config": {
            "step_timeout_sec": args.step_timeout_sec,
            "profile": profile,
            "profile_source": profile_source,
            "include_version_scan": include_version_scan,
            "include_skill_install": include_skill_install,
            "include_curated_skill_catalog": include_curated_skill_catalog,
            "include_public_api_refresh": include_public_api_refresh,
            "include_mcp_refresh": include_mcp_refresh,
            "include_staged_connectors": include_staged_connectors,
            "include_live_writes": include_live_writes,
            "offline_only": offline_only,
            "live_network_mode": live_network_mode,
            "mcp_refresh_mode": mcp_refresh_mode,
            "staged_connector_mode": staged_connector_mode,
            "active_materialization_mode": active_materialization_mode,
            "materialization_level": args.materialization_level,
            "soft_fail_network": soft_fail_network,
            "fail_on_warn": args.fail_on_warn,
            "achievement_target_steps": effective_achievement_target,
            "quick_mode": profile == "quick",
            "body_benchmark_mode": body_benchmark_mode,
            "include_body_benchmark": body_benchmark_mode != "off",
            "resume_failed_only": args.resume_failed_only,
            "resume_from_status": recovery_parent_run,
        },
        "results": suite_results,
    }

    lines.append("## Machine-readable summary")
    lines.append("```json")
    lines.append(json.dumps(status_payload, indent=2))
    lines.append("```")
    lines.append("")

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    status_json_path.parent.mkdir(parents=True, exist_ok=True)
    status_json_path.write_text(json.dumps(status_payload, indent=2) + "\n", encoding="utf-8")

    sync_refresh_cmd = [
        "python3",
        "scripts/v17_evidence_first_control_tower_sync.py",
        "--suite-status",
        str(status_json_path.relative_to(ROOT)).replace("\\", "/"),
        "--control-tower-json",
        str(control_tower_json_path.relative_to(ROOT)).replace("\\", "/"),
        "--control-tower-md",
        str(control_tower_md_path.relative_to(ROOT)).replace("\\", "/"),
        "--checkpoint-class",
        checkpoint_class,
    ]
    scoreboard_refresh_cmd = [
        "python3",
        "scripts/trinity_mandala_scoreboard.py",
        "--suite-status",
        str(status_json_path.relative_to(ROOT)).replace("\\", "/"),
        "--latest-json",
        str(scoreboard_latest_json.relative_to(ROOT)).replace("\\", "/"),
        "--latest-md",
        str(scoreboard_latest_md.relative_to(ROOT)).replace("\\", "/"),
        "--control-tower-path",
        str(control_tower_json_path.relative_to(ROOT)).replace("\\", "/"),
        "--checkpoint-class",
        checkpoint_class,
    ]
    if args.fail_on_warn:
        scoreboard_refresh_cmd.append("--fail-on-warn")

    sync_ok, sync_output, sync_timed_out, sync_duration_sec, sync_started_at, sync_finished_at = run_command(
        sync_refresh_cmd,
        args.step_timeout_sec,
    )
    sync_status, _ = classify_status(
        label="final control tower refresh",
        ok=sync_ok,
        timed_out=sync_timed_out,
        output=sync_output,
        soft_fail_network=soft_fail_network,
    )
    if sync_status not in {"PASS", "WARN"} or (args.fail_on_warn and sync_status == "WARN"):
        print(sync_output, file=sys.stderr)
        raise SystemExit(1)

    sync_refresh_row = {
        "label": "v17 evidence-first control tower sync",
        "status": sync_status,
        "ok": sync_ok,
        "effective_success": sync_status == "PASS",
        "timed_out": sync_timed_out,
        "started_at_utc": sync_started_at,
        "finished_at_utc": sync_finished_at,
        "duration_sec": round(sync_duration_sec, 3),
        "command": shlex.join(sync_refresh_cmd),
    }

    scoreboard_ok, scoreboard_output, scoreboard_timed_out, scoreboard_duration_sec, scoreboard_started_at, scoreboard_finished_at = run_command(
        scoreboard_refresh_cmd,
        args.step_timeout_sec,
    )
    scoreboard_status, _ = classify_status(
        label="final scoreboard refresh",
        ok=scoreboard_ok,
        timed_out=scoreboard_timed_out,
        output=scoreboard_output,
        soft_fail_network=soft_fail_network,
    )
    if scoreboard_status not in {"PASS", "WARN"} or (args.fail_on_warn and scoreboard_status == "WARN"):
        print(scoreboard_output, file=sys.stderr)
        raise SystemExit(1)

    scoreboard_refresh_row = {
        "label": "trinity mandala scoreboard",
        "status": scoreboard_status,
        "ok": scoreboard_ok,
        "effective_success": scoreboard_status == "PASS",
        "timed_out": scoreboard_timed_out,
        "started_at_utc": scoreboard_started_at,
        "finished_at_utc": scoreboard_finished_at,
        "duration_sec": round(scoreboard_duration_sec, 3),
        "command": shlex.join(scoreboard_refresh_cmd),
    }

    _replace_suite_result(suite_results, "v17 evidence-first control tower sync", sync_refresh_row)
    _replace_suite_result(suite_results, "trinity mandala scoreboard", scoreboard_refresh_row)

    pass_count = sum(1 for item in suite_results if item["status"] == "PASS")
    warn_count = sum(1 for item in suite_results if item["status"] == "WARN")
    timeout_count = sum(1 for item in suite_results if item["status"] == "TIMEOUT")
    fail_count = sum(1 for item in suite_results if item["status"] == "FAIL")
    achieved_steps = sum(1 for item in suite_results if bool(item["effective_success"]))
    effective_success = all(bool(item["effective_success"]) for item in suite_results)
    if args.fail_on_warn and warn_count > 0:
        effective_success = False
    if not achievement_gate_met:
        effective_success = False

    control_tower_status_path = str(control_tower_json_path.relative_to(ROOT)).replace("\\", "/")
    status_payload["generated_utc"] = datetime.now(timezone.utc).isoformat()
    status_payload["effective_success"] = effective_success
    status_payload["achieved_steps"] = achieved_steps
    status_payload["counts"] = {
        "pass": pass_count,
        "warn": warn_count,
        "timeout": timeout_count,
        "fail": fail_count,
    }
    status_payload["materialization_level_actual"] = _read_status_value(control_tower_status_path, "materialization_level_actual", "readiness_only")
    status_payload["google_drive_state"] = _read_status_value(control_tower_status_path, "google_drive_state", "operator_hold")
    status_payload["external_live_overlay_state"] = _read_status_value(control_tower_status_path, "external_live_overlay_state", "awaiting_thread_boot")
    status_payload["runtime_session_state"] = _read_status_value(control_tower_status_path, "runtime_session_state", "FAIL")
    status_payload["runtime_truth_complete"] = bool(_read_status_value(control_tower_status_path, "runtime_truth_complete", False))
    status_payload["external_establishment_criteria_state"] = _read_status_value(control_tower_status_path, "external_establishment_criteria_state", "FAIL")
    status_payload["standards_bridge_state"] = _read_status_value(control_tower_status_path, "standards_bridge_state", "FAIL")
    status_payload["filesystem_promotion_state"] = _read_status_value(control_tower_status_path, "filesystem_promotion_state", "blocked")
    status_payload["filesystem_connector_actual_state"] = _read_status_value(control_tower_status_path, "filesystem_connector_actual_state", "unknown")
    status_payload["claim_boundary_state"] = _read_status_value(control_tower_status_path, "claim_boundary_state", "FAIL")
    status_payload["v17_evidence_first_state"] = _read_status_value(control_tower_status_path, "v17_evidence_first_state", "FAIL")
    status_payload["results"] = suite_results

    lines.extend(
        [
            "## Final control tower refresh",
            f"- status: **{sync_refresh_row['status']}**",
            f"- command: `{sync_refresh_row['command']}`",
            f"- started: `{sync_refresh_row['started_at_utc']}`",
            f"- finished: `{sync_refresh_row['finished_at_utc']}`",
            f"- duration_sec: `{sync_refresh_row['duration_sec']}`",
            "```text",
            sync_output[:8000],
            "```",
            "",
            "## Final scoreboard refresh",
            f"- status: **{scoreboard_refresh_row['status']}**",
            f"- command: `{scoreboard_refresh_row['command']}`",
            f"- started: `{scoreboard_refresh_row['started_at_utc']}`",
            f"- finished: `{scoreboard_refresh_row['finished_at_utc']}`",
            f"- duration_sec: `{scoreboard_refresh_row['duration_sec']}`",
            "```text",
            scoreboard_output[:8000],
            "```",
            "",
            "## Final status reconciliation",
            f"- Effective success: **{effective_success}**",
            f"- PASS: **{pass_count}**",
            f"- WARN: **{warn_count}**",
            f"- TIMEOUT: **{timeout_count}**",
            f"- FAIL: **{fail_count}**",
            "",
            "## Final machine-readable summary",
            "```json",
            json.dumps(status_payload, indent=2),
            "```",
            "",
        ]
    )
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    status_json_path.write_text(json.dumps(status_payload, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote {report_path}")
    print(f"Wrote {status_json_path}")

    if effective_success:
        raise SystemExit(0)
    raise SystemExit(1)


if __name__ == "__main__":
    main()
