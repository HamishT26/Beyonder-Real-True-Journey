#!/usr/bin/env python3
"""Run available Trinity systems and produce a consolidated markdown report."""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
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
    "deep": "Expanded run (standard + version scan + skill install + curated catalog with soft-fail-network).",
}
BODY_PROFILE_POLICY_PATH = "docs/body-profile-policy-v1.json"


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


def build_commands(
    include_skill_install: bool,
    include_version_scan: bool,
    include_curated_skill_catalog: bool,
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
                        "unzip -l 'Beyonder-Real-True_Journey_v33_Capsule (4).zip' | rg -n 'v29|v30|v31|v32|v33|quantum|trinity|orchestrator|simulation|freed|cosmic' | head -n 40",
                    ],
                ),
            ]
        )

    if include_skill_install:
        commands.append(("local Trinity skill installation", ["bash", "scripts/install_local_skills.sh"]))

    if include_curated_skill_catalog:
        commands.append(("curated skill catalog snapshot", ["python3", SKILL_INSTALLER_LIST, "--format", "json"]))

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
    for name in ("standard", "quick", "deep"):
        lines.append(f"- {name}: {PROFILE_HELP[name]}")
    lines.append("- --quick-mode: legacy alias for --profile quick")
    return "\n".join(lines)


def resolve_profile_settings(args: argparse.Namespace) -> tuple[str, bool, bool, bool, bool, str, str]:
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
    soft_fail_network = args.soft_fail_network
    body_benchmark_mode = args.body_benchmark_mode

    if profile == "deep":
        include_version_scan = True
        include_skill_install = True
        include_curated_skill_catalog = True
        soft_fail_network = True

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
        soft_fail_network,
        profile_source,
        body_benchmark_mode,
    )


def run_command(cmd: list[str], timeout_sec: int) -> tuple[bool, str, bool, float, str, str]:
    started_at = datetime.now(timezone.utc).isoformat()
    start_ts = time.monotonic()
    try:
        proc = subprocess.run(
            cmd,
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
        choices=("standard", "quick", "deep"),
        default="deep",
        help=(
            "Execution profile: deep (default expanded run), standard (base stages), quick (continuity-focused subset), "
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
        quick_mode=(profile == "quick"),
        profile=profile,
        body_benchmark_mode=body_benchmark_mode,
    )

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
        "config": {
            "step_timeout_sec": args.step_timeout_sec,
            "profile": profile,
            "profile_source": profile_source,
            "include_version_scan": include_version_scan,
            "include_skill_install": include_skill_install,
            "include_curated_skill_catalog": include_curated_skill_catalog,
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
