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
REPORT = ROOT / "docs" / "system-suite-run-report.md"
STATUS_JSON = ROOT / "docs" / "system-suite-status.json"
CYCLE_STATUS = "docs/aurelis-cycle-tick-status.json"
SKILL_INSTALLER_LIST = "/opt/codex/skills/.system/skill-installer/scripts/list-curated-skills.py"
NETWORK_WARNING_MARKERS = ("403", "forbidden", "tunnel", "timed out", "proxy", "connection")
PROFILE_HELP = {
    "standard": "Base suite run with benchmark enforcement by default.",
    "quick": "Continuity-focused subset with benchmark observe mode by default.",
    "deep": "Expanded run (standard + version scan + skill install + curated catalog + expansion systems).",
    "collab": "Standard profile plus verified MCP collaboration refresh and collaboration pack reporting.",
    "materialize": "Standard profile plus materialization tracers and disposable staging proof generation.",
}
BODY_PROFILE_POLICY_PATH = "docs/body-profile-policy-v1.json"
TRINITY_EXPANSION_MANIFEST_PATH = "docs/trinity-expansion-system-manifest-v4.json"
TRINITY_MCP_CATALOG_PATH = "docs/trinity-mcp-catalog-v2.json"
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


def _load_expansion_system_commands(
    *,
    profile: str,
    enforce: bool,
    offline_only: bool,
    include_public_api_refresh: bool,
    include_mcp_refresh: bool,
    include_staged_connectors: bool,
    include_live_writes: bool,
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
        mode = str(entry.get("mode") or "offline").strip().lower()
        pack = str(entry.get("pack") or "").strip()
        if not system_id or not script:
            continue
        command = ["python3", script]
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
        command.extend(["--profile-context", profile])
        if mode == "live":
            live_disabled = offline_only
            if pack in {"figma_collab", "linear_collab"} and not include_mcp_refresh:
                live_disabled = True
            elif pack == "github_devflow" and not include_staged_connectors:
                live_disabled = True
            elif pack == "public_intelligence" and not include_public_api_refresh:
                live_disabled = True
            elif pack not in {"figma_collab", "linear_collab", "github_devflow", "public_intelligence"} and not include_public_api_refresh:
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
) -> list[tuple[str, list[str]]]:
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
            (
                *_extension_catalog_validation_command(
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
                    "bash",
                    "-lc",
                    "strings -n 8 'Beyonder-Real-True Journey v33 (Arielis) (2).pdf' | rg -n 'Core Modules|Orchestrator|DID Method|Quantum|Freed|GMUT|Cosmic Bill' | head -n 20",
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
                "bash",
                "-lc",
                "strings -n 8 'Beyonder-Real-True Journey v33 (Arielis) (2).pdf' | rg -n 'Core Modules|Orchestrator|DID Method|Quantum|Freed|GMUT|Cosmic Bill' | head -n 20",
            ],
        ),
    ]

    if include_version_scan:
        commands.extend(
            [
                (
                    "cross-version anchor scan (v29-v33 PDFs)",
                    [
                        "bash",
                        "-lc",
                        "for f in 'Beyonder-Real-True Journey v29 (Aerin) (1).pdf' 'Beyonder-Real-True Journey v30 (Ariel) (1).pdf' 'Beyonder-Real-True Journey v31 (Ariel) (1).pdf' 'Beyonder-Real-True Journey v32 (Aetherius) (1) (1).pdf' 'Beyonder-Real-True Journey v33 (Arielis) (2).pdf'; do echo \"=== $f ===\"; strings -n 8 \"$f\" | rg -n 'Trinity|GMUT|Freed|DID|Quantum|Orchestrator|Cosmic|QCIT|QCfT' | head -n 10 || true; done",
                    ],
                ),
                (
                    "v29 DOCX module anchor scan",
                    [
                        "bash",
                        "-lc",
                        "unzip -p 'Beyonder-Real-True Journey v29 (Aerin) (1).docx' word/document.xml | tr -d '\\r' | rg -n 'module|orchestrator|simulation|security|identity|governance|journey' | head -n 25",
                    ],
                ),
                (
                    "v33 capsule inventory snapshot",
                    [
                        "bash",
                        "-lc",
                        "if [ -f 'Beyonder-Real-True_Journey_v33_Capsule (4).zip' ]; then unzip -l 'Beyonder-Real-True_Journey_v33_Capsule (4).zip' | rg -n 'v29|v30|v31|v32|v33|quantum|trinity|orchestrator|simulation|freed|cosmic' | head -n 40; else echo 'SKIPPED: Beyonder-Real-True_Journey_v33_Capsule (4).zip not found'; fi",
                    ],
                ),
            ]
        )

    if include_skill_install:
        commands.append(("local Trinity skill installation", ["bash", "scripts/install_local_skills.sh"]))

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
    for name in ("standard", "quick", "deep", "collab", "materialize"):
        lines.append(f"- {name}: {PROFILE_HELP[name]}")
    lines.append("- --quick-mode: legacy alias for --profile quick")
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
    if profile in {"collab", "materialize"}:
        include_mcp_refresh = True
    if profile == "materialize":
        include_staged_connectors = True
        include_live_writes = True

    # Live API refresh is default for standard/deep unless explicitly offline-only.
    if profile in {"standard", "deep", "collab", "materialize"}:
        include_public_api_refresh = True
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
        choices=("standard", "quick", "deep", "collab", "materialize"),
        default="deep",
        help=(
            "Execution profile: deep (default expanded run), standard (base stages), quick (continuity-focused subset), collab (standard + verified MCP refresh), "
            "materialize (standard + disposable staging write tracers), deep (standard + version scan + skill install + curated catalog + soft-fail-network)."
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
        "--body-benchmark-mode",
        choices=("auto", "off", "observe", "enforce"),
        default="auto",
        help=(
            "Benchmark guardrail mode: auto (quick=observe, standard/deep=enforce), "
            "off, observe, or enforce."
        ),
    )
    parser.add_argument(
        "--status-json",
        default=str(STATUS_JSON.relative_to(ROOT)),
        help="Path to write machine-readable suite status JSON (relative to repo root).",
    )
    args = parser.parse_args()

    if args.list_profiles:
        print(render_profile_catalog())
        raise SystemExit(0)

    if args.step_timeout_sec < 0:
        raise SystemExit("--step-timeout-sec must be >= 0")
    if args.achievement_target_steps < 0:
        raise SystemExit("--achievement-target-steps must be >= 0")

    status_json_path = (ROOT / args.status_json).resolve()
    try:
        status_json_path.relative_to(ROOT)
    except ValueError as exc:
        raise SystemExit("--status-json must remain within repository root") from exc

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
    )
    mcp_catalog_path = ROOT / TRINITY_MCP_CATALOG_PATH
    verified_mcp_connectors: list[str] = []
    eligible_live_write_connectors: list[str] = []
    promoted_live_write_connectors: list[str] = []
    blocked_promotions: list[str] = []
    if mcp_catalog_path.exists():
        try:
            mcp_payload = json.loads(mcp_catalog_path.read_text(encoding="utf-8"))
            connector_rows = mcp_payload.get("connectors", [])
            if isinstance(connector_rows, list):
                verified_mcp_connectors = sorted(
                    str(row.get("mcp_id"))
                    for row in connector_rows
                    if isinstance(row, dict) and bool(row.get("live_read_enabled"))
                )
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
            eligible_live_write_connectors = []
            promoted_live_write_connectors = []
            blocked_promotions = []
    if offline_only:
        live_network_mode = "offline_only"
    elif profile in {"standard", "deep", "collab", "materialize"}:
        live_network_mode = "live_default"
    elif include_public_api_refresh:
        live_network_mode = "live_opt_in"
    else:
        live_network_mode = "offline_default"
    if offline_only:
        mcp_refresh_mode = "offline_only"
        staged_connector_mode = "offline_only"
    else:
        mcp_refresh_mode = "verified_live" if include_mcp_refresh else "disabled"
        staged_connector_mode = "setup_gate_attempted" if include_staged_connectors else "staged_only"
    collab_pack_count = 9
    materialization_pack_count = 6
    if offline_only:
        active_materialization_mode = "offline_only"
    elif include_live_writes:
        active_materialization_mode = "disposable_staging"
    else:
        active_materialization_mode = "read_only"

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
        f"Status JSON path: {status_json_path.relative_to(ROOT)}",
        "",
        "This report runs currently available repo systems and records command outputs.",
        "",
    ]

    suite_results: list[dict[str, object]] = []

    for label, cmd in commands:
        ok, output, timed_out, duration_sec, started_at, finished_at = run_command(cmd, args.step_timeout_sec)
        status, counted_success = classify_status(
            label=label,
            ok=ok,
            timed_out=timed_out,
            output=output,
            soft_fail_network=soft_fail_network,
        )
        command_str = shlex.join(cmd)
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

    suite_finished_at = datetime.now(timezone.utc).isoformat()
    suite_duration_sec = time.monotonic() - suite_start_ts

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
    lines.append(f"- Eligible live write connectors: **{', '.join(eligible_live_write_connectors) if eligible_live_write_connectors else '-'}**")
    lines.append(f"- Promoted live write connectors: **{', '.join(promoted_live_write_connectors) if promoted_live_write_connectors else '-'}**")
    lines.append(f"- Blocked promotions: **{', '.join(blocked_promotions) if blocked_promotions else '-'}**")
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
        "expansion_systems_total": expansion_total,
        "expansion_systems_passed": expansion_passed,
        "collab_pack_count": collab_pack_count,
        "materialization_pack_count": materialization_pack_count,
        "verified_mcp_connectors": verified_mcp_connectors,
        "eligible_live_write_connectors": eligible_live_write_connectors,
        "promoted_live_write_connectors": promoted_live_write_connectors,
        "blocked_promotions": blocked_promotions,
        "active_materialization_mode": active_materialization_mode,
        "mcp_refresh_mode": mcp_refresh_mode,
        "staged_connector_mode": staged_connector_mode,
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
            "soft_fail_network": soft_fail_network,
            "fail_on_warn": args.fail_on_warn,
            "achievement_target_steps": effective_achievement_target,
            "quick_mode": profile == "quick",
            "body_benchmark_mode": body_benchmark_mode,
            "include_body_benchmark": body_benchmark_mode != "off",
        },
        "results": suite_results,
    }

    lines.append("## Machine-readable summary")
    lines.append("```json")
    lines.append(json.dumps(status_payload, indent=2))
    lines.append("```")
    lines.append("")

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    status_json_path.parent.mkdir(parents=True, exist_ok=True)
    status_json_path.write_text(json.dumps(status_payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {REPORT}")
    print(f"Wrote {status_json_path}")

    if effective_success:
        raise SystemExit(0)
    raise SystemExit(1)


if __name__ == "__main__":
    main()
