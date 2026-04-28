from __future__ import annotations

import datetime as dt
import hashlib
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "docs" / "trinity-live-traces"
PHASE = "v60_v67_hybrid_omega"
PUBLICATION_BRANCH = "codex/GHC-Family/beyonder-shared-omega-line"


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: Any) -> None:
    write_text(path, json.dumps(payload, indent=2, ensure_ascii=True) + "\n")


def read_json(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def run(args: list[str], timeout: int = 45) -> dict[str, Any]:
    try:
        proc = subprocess.run(args, cwd=ROOT, text=True, capture_output=True, timeout=timeout, check=False)
        return {
            "ok": proc.returncode == 0,
            "returncode": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
        }
    except Exception as exc:
        return {"ok": False, "error": type(exc).__name__, "message": str(exc)}


def sha12(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()[:12]


def md(title: str, payload: Any) -> str:
    return f"# {title}\n\n```json\n{json.dumps(payload, indent=2, ensure_ascii=True)}\n```\n"


def suite_status(name: str) -> dict[str, Any]:
    path = TRACE / f"{name}-suite-status.json"
    data = read_json(path, {})
    counts = data.get("counts", {}) if isinstance(data, dict) else {}
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "present": path.exists(),
        "effective_success": bool(data.get("effective_success", False)) if isinstance(data, dict) else False,
        "summary": f"{counts.get('pass', 0)} PASS / {counts.get('warn', 0)} WARN / {counts.get('fail', 0)} FAIL",
    }


def suite_labels(path: Path) -> set[str]:
    data = read_json(path, {})
    if not isinstance(data, dict):
        return set()
    return {str(item.get("label")) for item in data.get("results", []) if item.get("label")}


def coverage_governor() -> dict[str, Any]:
    v58_standard = suite_labels(TRACE / "v58-standard-suite-status.json")
    v58_deep = suite_labels(TRACE / "v58-deep-suite-status.json")
    v59_deep = suite_labels(TRACE / "v59-deep-suite-status.json")
    v58_l4 = suite_labels(TRACE / "v58-materialize-l4-suite-status.json")
    v58_l5 = suite_labels(TRACE / "v58-materialize-l5-suite-status.json")
    v59_l5 = suite_labels(TRACE / "v59-materialize-l5-suite-status.json")
    misses = {
        "standard_missing_from_v58_deep": sorted(v58_standard - v58_deep),
        "standard_missing_from_v59_deep": sorted(v58_standard - v59_deep),
        "l4_missing_from_v58_l5": sorted(v58_l4 - v58_l5),
        "v58_l5_missing_from_v59_l5": sorted(v58_l5 - v59_l5),
    }
    approved = all(len(value) == 0 for value in misses.values())
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "suite_cut_state": "approved_deep_plus_l5_repeated_pair" if approved else "blocked_reintroduce_full_ladder",
        "basis": {
            "v58_standard_labels": len(v58_standard),
            "v58_deep_labels": len(v58_deep),
            "v59_deep_labels": len(v59_deep),
            "v58_l4_labels": len(v58_l4),
            "v58_l5_labels": len(v58_l5),
            "v59_l5_labels": len(v59_l5),
            "missing_counts": {key: len(value) for key, value in misses.items()},
        },
        "policy": {
            "repeat_pair": ["deep", "materialize_l5"],
            "skip_by_default": ["standard", "materialize_l4"],
            "separate_mcp_policy": "not_covered_by_deep_plus_l5",
            "audit_cadence": "run_standard_l4_every_fifth_phase_or_on_any_warn_fail_timeout_or_runner_change",
            "mcp_cadence": "run_true_mcp_refresh_every_third_phase_or_on_connector_auth_cache_catalog_change",
            "immediate_fallback": "if_deep_or_l5_warns_or_fails_run_standard_then_l4_before_advancing",
        },
        "sample_missing_labels": {key: value[:10] for key, value in misses.items()},
    }


def host_and_kube() -> dict[str, Any]:
    readyz = run(["kubectl", "--context", "docker-desktop", "get", "--raw=/readyz"], timeout=45)
    docker = run(["docker", "stats", "--no-stream", "--format", "{{.Name}}|{{.CPUPerc}}|{{.MemUsage}}"], timeout=45)
    memory = run(
        [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            "(Get-CimInstance Win32_OperatingSystem | Select-Object FreePhysicalMemory,TotalVisibleMemorySize | ConvertTo-Json -Compress)",
        ],
        timeout=45,
    )
    containers: list[dict[str, Any]] = []
    max_cpu = 0.0
    if docker.get("ok"):
        for line in docker["stdout"].splitlines():
            parts = line.split("|")
            if len(parts) != 3:
                continue
            try:
                cpu = float(parts[1].replace("%", "").strip())
            except ValueError:
                cpu = 0.0
            max_cpu = max(max_cpu, cpu)
            containers.append({"name": parts[0], "cpu_percent": cpu, "memory": parts[2]})
    try:
        mem = json.loads(memory.get("stdout", "{}"))
    except Exception:
        mem = {}
    free_kb = int(mem.get("FreePhysicalMemory", 0)) if isinstance(mem, dict) else 0
    host_state = "cool"
    if max_cpu >= 300 or free_kb < 300_000:
        host_state = "hot_pause_heavy_suites"
    elif max_cpu >= 150 or free_kb < 500_000:
        host_state = "warm_cooldown_before_heavy_suites"
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "kubernetes_readyz": "ok" if readyz.get("stdout") == "ok" else "not_ok",
        "kubernetes_probe": {
            "ok": bool(readyz.get("ok")),
            "returncode": readyz.get("returncode"),
            "stderr_excerpt": (readyz.get("stderr") or readyz.get("message") or "")[:600],
        },
        "host_pressure_state": host_state,
        "max_container_cpu_percent": max_cpu,
        "free_physical_memory_kb": free_kb,
        "containers": containers,
        "load_gate": "open" if readyz.get("stdout") == "ok" and host_state == "cool" else "closed",
    }


def command_matrix() -> dict[str, Any]:
    commands = ["gh", "circleci", "node", "npm", "npx", "kubectl", "docker", "wrangler", "vercel", "neonctl", "render", "expo", "eas", "oci", "helm", "kustomize", "stern"]
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "commands": {cmd: {"available": bool(shutil.which(cmd)), "path": shutil.which(cmd) or ""} for cmd in commands},
        "secret_policy": "raw_values_never_written",
    }


def provider_board(commands: dict[str, Any]) -> dict[str, Any]:
    def cmd_state(cmd: str) -> str:
        return "cli_available_read_gate_next" if commands["commands"].get(cmd, {}).get("available") else "missing_cli_or_path"

    lanes = [
        ("notion", "blocked_missing_parent", "provide shared parent page or data source ID"),
        ("browser_use", "blocked_kernel_assets_missing", "repair kernel asset path then retry local dashboard/doc probe"),
        ("vercel", cmd_state("vercel"), "read-only project/account probe before any preview project"),
        ("cloudflare", cmd_state("wrangler"), "read-only account/pages/workers probe before any disposable worker"),
        ("neon", cmd_state("neonctl"), "read-only project/database probe before any branch/schema"),
        ("render", cmd_state("render"), "read-only service-list/API probe before any service scaffold"),
        ("expo", "npx_available" if commands["commands"].get("npx", {}).get("available") else "npx_missing", "local Expo preview only, no EAS cloud build until auth gate"),
        ("github", cmd_state("gh"), "app connector succeeded for PR #45, gh shell auth may still need login"),
        ("circleci", cmd_state("circleci"), "config validation/read status before pipeline trigger"),
        ("google_drive", "operator_hold", "do not promote Drive as authoritative without explicit policy change"),
        ("figma", "read_only_view_seat", "read-only capture with explicit file key/node ID"),
    ]
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "lanes": [
            {
                "provider": provider,
                "state": state,
                "next_allowed_action": action,
                "live_write_enabled": False,
                "secret_policy": "raw_values_never_written",
            }
            for provider, state, action in lanes
        ],
    }


def extension_plan() -> tuple[dict[str, Any], str]:
    phase_rows = {
        "v60": ["notion_parent_binding_gate", "notion_block_mapper", "notion_write_receipt_schema", "api_surface_proof_index", "connector_permission_matrix", "workbench_truth_precedence_v2", "browser_kernel_repair_probe", "v60_deep_l5_packet"],
        "v61": ["helm_presence_probe", "kustomize_presence_probe", "stern_log_probe", "kubectx_guard", "one_node_restart_watch", "host_cooldown_ledger", "docker_compose_profile_guard", "local_runtime_budget"],
        "v62": ["v58_v62_rollup_index", "suite_ladder_delta_digest", "additions_promotion_board", "blocker_retirement_board", "v63_decision_board", "publication_allowlist_v62", "publication_result_validator", "closeout_handoff_triplet"],
        "v63": ["expo_go_qr_lane", "expo_web_preview_smoke", "phone_dashboard_contract", "mobile_truth_cards", "offline_dashboard_bundle", "dashboard_a11y_smoke", "browser_fallback_probe", "dashboard_screenshot_receipt"],
        "v64": ["wrangler_readonly_probe", "cloudflare_pages_probe", "d1_schema_dry_run", "r2_inventory_probe", "workers_ai_capability_card", "vercel_static_probe", "render_static_probe", "neon_readonly_state"],
        "v65": ["qcit_gmut_delta_probe_v2", "qcit_seed_sweep_v2", "latex_gmut_digest", "claim_checker_matrix", "life_science_matrix", "kairotic_regression", "quantum_energy_probe", "public_source_claim_board"],
        "v66": ["freedid_min_disclosure_refresh", "cosmic_bill_rights_trace", "google_drive_hold_receipt", "secret_fingerprint_audit", "github_pr_truth_sync", "linear_phase_record", "circleci_config_probe", "figma_capture_gate"],
        "v67": ["v60_v67_additions_registry", "eureka_gate_ledger", "suite_policy_governor_v2", "curated_stage_allowlist_v67", "git_publication_result_v67", "omega_continuity_pack_v67", "hybrid_dashboard_v67", "v68_decision_board"],
    }
    registry = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "additions_total": sum(len(items) for items in phase_rows.values()),
        "policy": "evidence_first_no_secret_no_unconfirmed_install",
        "phases": [
            {
                "phase": phase,
                "eureka_gate": "mandatory",
                "suite_pair": "deep_plus_l5_when_load_gate_open",
                "audit_lane": "standard_l4_every_fifth_phase_or_failure; mcp_every_third_phase_or_connector_change",
                "additions": items,
            }
            for phase, items in phase_rows.items()
        ],
    }
    md_lines = [
        "# V60-V67 Omega Hybrid Extension Plan",
        "",
        "- Each phase starts with a eureka gate before suite load.",
        "- Repeated validation uses Deep plus Materialize L5 when Kubernetes and host gates are green.",
        "- Standard and L4 return every fifth phase or on any warn/fail/timeout/runner change.",
        "- MCP refresh is a separate connector/cache audit lane because Deep plus L5 do not prove a true MCP refresh.",
        "- No raw secrets are written to repo artifacts.",
        "",
        "| Phase | Additions |",
        "|---|---|",
    ]
    for phase, items in phase_rows.items():
        md_lines.append(f"| {phase.upper()} | {', '.join(items)} |")
    return registry, "\n".join(md_lines) + "\n"


def suite_ladder() -> dict[str, Any]:
    phases = ["v58", "v59", "v60", "v61", "v62", "v63", "v64", "v65", "v66", "v67"]
    profiles = {}
    for phase in phases:
        for profile in ["quick", "standard", "deep", "materialize-l4", "materialize-l5", "mcp-refresh"]:
            profiles[f"{phase}-{profile}"] = suite_status(f"{phase}-{profile}")
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "profiles": profiles,
        "state": "v58_v59_green_v60_v67_planned_health_gated",
    }


def stage_allowlist() -> dict[str, Any]:
    paths = [
        "scripts/trinity_v60_v67_omega.py",
        "scripts/trinity_v58_omega.py",
        "docs/v60-v67-omega-hybrid-extension-plan-v1.md",
        "docs/v67-omega-closeout-summary-v1.json",
        "docs/v67-omega-continuity-pack-v1.md",
        "docs/v67-omega-handoff-policy-v1.json",
        "docs/trinity-live-traces/v58-suite-coverage-policy-v1.json",
        "docs/trinity-live-traces/v58-suite-coverage-policy-v1.md",
        "docs/trinity-live-traces/v60-v67-additions-registry-v1.json",
        "docs/trinity-live-traces/v60-v67-additions-registry-v1.md",
        "docs/trinity-live-traces/v60-v67-eureka-gate-ledger-v1.json",
        "docs/trinity-live-traces/v60-v67-eureka-gate-ledger-v1.md",
        "docs/trinity-live-traces/v60-v67-suite-ladder-summary-v1.json",
        "docs/trinity-live-traces/v60-v67-suite-ladder-summary-v1.md",
        "docs/trinity-live-traces/v60-v67-suite-policy-governor-v1.json",
        "docs/trinity-live-traces/v60-v67-suite-policy-governor-v1.md",
        "docs/trinity-live-traces/v60-v67-runtime-health-gate-v1.json",
        "docs/trinity-live-traces/v60-v67-runtime-health-gate-v1.md",
        "docs/trinity-live-traces/v67-provider-decision-board-v1.json",
        "docs/trinity-live-traces/v67-provider-decision-board-v1.md",
        "docs/trinity-live-traces/v67-stage-allowlist-v1.json",
        "docs/trinity-live-traces/v67-stage-allowlist-v1.md",
    ]
    for phase in range(60, 68):
        paths.append(f"docs/v{phase}-omega-plan-proposal-v1.md")
        paths.append(f"docs/v{phase}-eureka-analysis-v1.md")
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "stage_policy": "stage_only_v60_v67_extension_truth_leave_generated_churn_unstaged",
        "paths": sorted(set(paths)),
    }


def generate() -> dict[str, Any]:
    TRACE.mkdir(parents=True, exist_ok=True)
    coverage = coverage_governor()
    health = host_and_kube()
    commands = command_matrix()
    provider = provider_board(commands)
    additions, plan_md = extension_plan()
    suite = suite_ladder()
    eureka = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "state": "mandatory_before_each_phase",
        "phases": [
            {
                "phase": phase["phase"],
                "gate": "eureka_before_suite_load",
                "next_move": f"Execute {phase['phase']} only when runtime health gate is open.",
                "additions_count": len(phase["additions"]),
            }
            for phase in additions["phases"]
        ],
    }
    closeout = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "overall_status": "WARN",
        "summary": {
            "suite_cut_state": coverage["suite_cut_state"],
            "runtime_load_gate": health["load_gate"],
            "provider_board_state": "blocker_aware_no_live_writes",
            "publication_state": "pending",
        },
        "bounded_residuals": [
            "v60_v67_heavy_suites_not_run_until_runtime_health_gate_opens",
            "notion_parent_still_required_for_live_dashboard",
            "browser_use_kernel_assets_still_require_repair",
        ],
    }
    handoff = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "handoff_state": "ready_for_v60_when_runtime_health_gate_open",
        "next_command_pair": [
            "python scripts/run_all_trinity_systems.py --profile deep --status-json docs/trinity-live-traces/v60-deep-suite-status.json",
            "python scripts/run_all_trinity_systems.py --profile materialize --include-staged-connectors --include-live-writes --materialization-level l5_ha_prod --status-json docs/trinity-live-traces/v60-materialize-l5-suite-status.json",
        ],
    }
    allowlist = stage_allowlist()
    write_json(TRACE / "v60-v67-suite-policy-governor-v1.json", coverage)
    write_text(TRACE / "v60-v67-suite-policy-governor-v1.md", md("V60-V67 Suite Policy Governor", coverage))
    write_json(TRACE / "v60-v67-runtime-health-gate-v1.json", health)
    write_text(TRACE / "v60-v67-runtime-health-gate-v1.md", md("V60-V67 Runtime Health Gate", health))
    write_json(TRACE / "v60-v67-additions-registry-v1.json", additions)
    write_text(TRACE / "v60-v67-additions-registry-v1.md", md("V60-V67 Additions Registry", additions))
    write_json(TRACE / "v60-v67-eureka-gate-ledger-v1.json", eureka)
    write_text(TRACE / "v60-v67-eureka-gate-ledger-v1.md", md("V60-V67 Eureka Gate Ledger", eureka))
    write_json(TRACE / "v60-v67-suite-ladder-summary-v1.json", suite)
    write_text(TRACE / "v60-v67-suite-ladder-summary-v1.md", md("V60-V67 Suite Ladder Summary", suite))
    write_json(TRACE / "v67-provider-decision-board-v1.json", provider)
    write_text(TRACE / "v67-provider-decision-board-v1.md", md("V67 Provider Decision Board", provider))
    write_json(TRACE / "v67-stage-allowlist-v1.json", allowlist)
    write_text(TRACE / "v67-stage-allowlist-v1.md", md("V67 Stage Allowlist", allowlist))
    write_text(ROOT / "docs" / "v60-v67-omega-hybrid-extension-plan-v1.md", plan_md)
    for phase in additions["phases"]:
        write_text(
            ROOT / "docs" / f"{phase['phase']}-eureka-analysis-v1.md",
            f"# {phase['phase'].upper()} Eureka Analysis\n\n- Gate: `mandatory_before_suite_load`\n- Suite pair: `deep_plus_l5_when_health_green`\n- Additions: `{len(phase['additions'])}`\n",
        )
        write_text(
            ROOT / "docs" / f"{phase['phase']}-omega-plan-proposal-v1.md",
            f"# {phase['phase'].upper()} Omega Plan Proposal\n\n- Additions: {', '.join(phase['additions'])}\n- Validation: Deep plus Materialize L5 when runtime health gate is open.\n- Audit: Standard and L4 every fifth phase or on any failure family; MCP refresh every third phase or on connector/cache changes.\n",
        )
    write_json(ROOT / "docs" / "v67-omega-closeout-summary-v1.json", closeout)
    write_json(ROOT / "docs" / "v67-omega-handoff-policy-v1.json", handoff)
    write_text(
        ROOT / "docs" / "v67-omega-continuity-pack-v1.md",
        f"# V67 Omega Continuity Pack\n\n- Suite cut: `{coverage['suite_cut_state']}`\n- Runtime load gate: `{health['load_gate']}`\n- Provider board: `blocker_aware_no_live_writes`\n- Publication branch: `{PUBLICATION_BRANCH}`\n",
    )
    return {
        "coverage": coverage,
        "health": health,
        "commands": commands,
        "provider": provider,
        "additions": additions,
        "suite": suite,
        "eureka": eureka,
        "closeout": closeout,
        "allowlist": allowlist,
    }


if __name__ == "__main__":
    generate()
