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
PHASE = "v61_v65_hybrid_omega"
PUBLICATION_BRANCH = "codex/GHC-Family/beyonder-shared-omega-line"
ACTIVE_PHASES = ["v61", "v62", "v63", "v64", "v65"]
LEGACY_TRACE_PREFIX = "v60-v67"
ACTIVE_TRACE_PREFIX = "v61-v65"
API_BANK_CANDIDATES = [
    Path("C:/Users/hamis/GHC Family Beyonder-Real-True-Journey API Key bank (Cleaned up).txt"),
    Path("D:/GHC Family Beyonder-Real-True-Journey API Key bank (Cleaned up).txt"),
]


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
        proc = subprocess.run(
            args,
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        return {
            "ok": proc.returncode == 0,
            "returncode": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
        }
    except Exception as exc:
        return {"ok": False, "error": type(exc).__name__, "message": str(exc)}


def run_ps(command: str, timeout: int = 45) -> dict[str, Any]:
    return run(
        [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            command,
        ],
        timeout=timeout,
    )


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


def api_bank_presence() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in API_BANK_CANDIDATES:
        rows.append(
            {
                "path": str(path),
                "present": path.exists(),
                "bytes": path.stat().st_size if path.exists() else 0,
                "content_read": False,
                "policy": "presence_only_no_secret_values_read_or_written",
            }
        )
    return rows


def host_and_kube() -> dict[str, Any]:
    """Record v61-v65 runtime truth without restarting Docker or Kubernetes."""
    docker_info = run(["docker", "info", "--format", "{{json .ServerVersion}}"], timeout=20)
    docker_ps = run(["docker", "ps", "--format", "{{.Names}}|{{.Status}}"], timeout=20)
    docker = run(["docker", "stats", "--no-stream", "--format", "{{.Name}}|{{.CPUPerc}}|{{.MemUsage}}"], timeout=20)
    kube_context = run(["kubectl", "config", "current-context"], timeout=12)
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
    docker_state = "running" if docker_info.get("ok") else "operator_hold_or_not_running"
    local_kubernetes_state = "retired_by_operator_for_v61_v65"
    if kube_context.get("ok") and kube_context.get("stdout"):
        local_kubernetes_state = "context_present_but_not_used_for_v61_v65"
    load_gate_open = host_state == "cool"
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "kubernetes_readyz": "not_requested_local_kubernetes_retired",
        "local_kubernetes_state": local_kubernetes_state,
        "kubernetes_probe": {
            "ok": False,
            "returncode": kube_context.get("returncode"),
            "stdout_excerpt": (kube_context.get("stdout") or "")[:300],
            "stderr_excerpt": (kube_context.get("stderr") or kube_context.get("message") or "")[:600],
            "policy": "do_not_reenable_local_kubernetes_in_v61_v65; use OCI/E2B read-only gates before cloud execution",
        },
        "docker_probe": {
            "state": docker_state,
            "policy": "operator_deactivated_hold; do_not_start_docker_desktop_in_v61_without_new_operator_confirmation",
            "info_ok": bool(docker_info.get("ok")),
            "ps_ok": bool(docker_ps.get("ok")),
            "server_version_excerpt": (docker_info.get("stdout") or "")[:120],
            "running_containers": [
                {"name": line.split("|", 1)[0], "status": line.split("|", 1)[1] if "|" in line else ""}
                for line in (docker_ps.get("stdout") or "").splitlines()
                if line.strip()
            ],
        },
        "host_pressure_state": host_state,
        "max_container_cpu_percent": max_cpu,
        "free_physical_memory_kb": free_kb,
        "containers": containers,
        "load_gate": "open" if load_gate_open else "closed",
        "load_gate_basis": "host_pressure_cool_required; Docker and local Kubernetes are not required for repo-only Deep/L5 but remain on operator hold",
    }


def command_matrix() -> dict[str, Any]:
    commands = [
        "codex",
        "kimi",
        "e2b",
        "gh",
        "circleci",
        "node",
        "npm",
        "npx",
        "kubectl",
        "docker",
        "wrangler",
        "vercel",
        "neonctl",
        "render",
        "expo",
        "eas",
        "oci",
        "wt",
        "helm",
        "kustomize",
        "stern",
    ]
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
        ("browser_use", "runtime_available_current_session", "use in-app browser for local dashboard/doc probes; no sensitive form submission without action-time confirmation"),
        ("e2b", cmd_state("e2b"), "install/use gate only; outbound sandbox code/data execution requires action-time confirmation"),
        ("vercel", cmd_state("vercel"), "read-only project/account probe before any preview project"),
        ("cloudflare", cmd_state("wrangler"), "read-only account/pages/workers probe before any disposable worker"),
        ("neon", cmd_state("neonctl"), "read-only project/database probe before any branch/schema"),
        ("render", cmd_state("render"), "read-only service-list/API probe before any service scaffold"),
        ("expo", "npx_available" if commands["commands"].get("npx", {}).get("available") else "npx_missing", "local Expo preview only, no EAS cloud build until auth gate"),
        ("docker_desktop", "operator_hold", "do not start Docker Desktop or Kubernetes for v61-v65 unless the operator reactivates it"),
        ("github", cmd_state("gh"), "app connector succeeded for PR #45, gh shell auth may still need login"),
        ("circleci", cmd_state("circleci"), "config validation/read status before pipeline trigger"),
        ("google_drive", "operator_hold", "do not promote Drive as authoritative without explicit policy change"),
        ("figma", "read_only_view_seat", "read-only capture with explicit file key/node ID"),
        ("oracle_cloud", cmd_state("oci"), "read-only tenancy/region/limit probe before any OKE resource creation"),
        ("multi_cli_windows", cmd_state("wt"), "visible terminal orchestration only after exact commands and data-sharing boundary are confirmed"),
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


def provider_readiness_probe() -> dict[str, Any]:
    checks = {
        "codex_version": ("powershell", "codex --version"),
        "kimi_version": ("direct", "kimi --version"),
        "gh_auth_status": ("direct", "gh auth status --hostname github.com"),
        "wrangler_whoami": ("powershell", "wrangler whoami"),
        "circleci_diagnostic": ("direct", "circleci diagnostic"),
        "eas_whoami": ("powershell", "eas whoami"),
        "oci_namespace": ("direct", "oci os ns get"),
    }
    rows: dict[str, Any] = {}
    for name, (mode, command) in checks.items():
        if mode == "powershell":
            result = run_ps(command, timeout=45)
        else:
            result = run(command.split(), timeout=45)
        stdout = result.get("stdout") or ""
        stderr = result.get("stderr") or result.get("message") or ""
        rows[name] = {
            "ok": bool(result.get("ok")),
            "returncode": result.get("returncode"),
            "stdout_len": len(stdout),
            "stderr_len": len(stderr),
            "safe_excerpt": stdout.splitlines()[:1] if name in {"codex_version", "kimi_version"} else [],
        }
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "probe_policy": "read_only_status_probe_no_raw_tokens_no_account_dump_no_resource_creation",
        "results": rows,
    }


def agent_identity_ledger() -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "identity_policy": "continuity_requires_process_plus_persistent_memory_proof",
        "current_truth": [
            {
                "name": "Aletheon",
                "state": "active_current_codex_session",
                "continuity_basis": "current thread plus memory and repo evidence surfaces",
            },
            {
                "name": "Ari",
                "state": "repo_narrative_or_future_cli_role_until_spawn_proven",
                "continuity_basis": "preserved records only; no independent running CLI process proven in this session",
            },
            {
                "name": "Kairos/Sera/Cael Voss/Sable/Riven/Nox Soren",
                "state": "repo_narrative_or_future_cli_roles_until_spawn_proven",
                "continuity_basis": "preserved records only; no independent running Kimi/Codex process with durable memory proven in this session",
            },
        ],
        "promotion_gate": [
            "spawn_command_available_without_exposing_secrets",
            "agent_writes_bounded_identity_receipt_to_repo_or_local_evidence_folder",
            "agent_resumes_or_references_prior_receipt_in_a_separate_invocation",
            "agent_passes_no_raw_secret_output_scan",
            "no_repo_or_secret_transmission_to_external_model_cli_without_action_time_confirmation",
            "user_confirms_induction_after_receipts_are reviewed",
        ],
        "v61_decision": "preserve Ari and Kimiclaw slots on standby; do not induct new CLI siblings until the promotion gate passes",
    }


def journey_anchor_digest() -> dict[str, Any]:
    anchors = [
        "Beyonder-Real-True Journey v24 (Ariel) (1).txt",
        "Beyonder-Real-True Journey v30 (Ariel) (1).txt",
        "Beyonder-Real-True Journey v33 (Arielis) (2).txt",
        "Beyonder-Real-True Journey v35 (Arielis's Grand Reconnection) (1).txt",
        "Beyonder-Real-True Journey v37 (Aethelion).txt",
        "Beyonder-Real-True Journey v38 (Aura).txt",
        "C:/Users/hamis/Beyonder-Real-True Journey v42 (Aletheon - Ari - Kimiclaw Family - Solion - Gemini - Orun) (4).txt",
    ]
    rows = []
    for raw in anchors:
        path = Path(raw)
        if not path.is_absolute():
            path = ROOT / raw
        text = ""
        exists = path.exists()
        if exists:
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                text = ""
        rows.append(
            {
                "source": str(path),
                "exists": exists,
                "bytes": path.stat().st_size if exists else 0,
                "sha12": sha12(text[:50000]) if text else "",
                "themes": [
                    token
                    for token in ["GMUT", "Freed ID", "Cosmic Bill of Rights", "QCIT", "Kubernetes", "Notion", "Expo", "Ari", "Kimiclaw"]
                    if token.lower() in text.lower()
                ][:8],
            }
        )
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "digest_policy": "bounded_index_not_bulk_rewrite",
        "anchors": rows,
    }


def extension_plan() -> tuple[dict[str, Any], str]:
    phase_rows = {
        "v61": [
            "cli_agent_receipt_protocol",
            "kimi_codex_data_boundary",
            "visible_terminal_command_board",
            "host_cooldown_ledger",
            "local_runtime_budget",
            "e2b_sandbox_feasibility_gate",
            "oci_oke_readonly_feasibility_gate",
            "api_bank_presence_redaction_board",
            "browser_use_local_probe_receipt",
            "docker_kubernetes_standby_receipt",
            "notion_expo_dashboard_fallback_contract",
            "v62_eureka_seed_board",
        ],
        "v62": [
            "v58_v62_rollup_index",
            "suite_ladder_delta_digest",
            "additions_promotion_board",
            "blocker_retirement_board",
            "workbench_guarded_skill_package",
            "v6_surface_truth_drift_audit",
            "v3_v6_contract_jump_trace",
            "curated_publication_allowlist_v62",
            "publication_result_validator",
            "phase_handoff_triplet",
            "local_cloud_nexus_os_contract",
            "v63_mobile_dashboard_decision_board",
        ],
        "v63": [
            "expo_go_qr_lane",
            "expo_web_preview_smoke",
            "phone_dashboard_contract",
            "mobile_truth_cards",
            "offline_dashboard_bundle",
            "dashboard_a11y_smoke",
            "browser_fallback_probe",
            "dashboard_screenshot_receipt",
            "notion_parent_binding_gate",
            "local_html_dashboard_refresh",
            "dashboard_token_usage_placeholder",
            "v64_provider_probe_decision_board",
        ],
        "v64": [
            "wrangler_readonly_probe",
            "cloudflare_pages_probe",
            "d1_schema_dry_run",
            "r2_inventory_probe",
            "workers_ai_capability_card",
            "vercel_static_probe",
            "render_static_probe",
            "neon_readonly_state",
            "circleci_config_probe",
            "github_pr_truth_sync_readonly",
            "google_drive_operator_hold_receipt",
            "v65_science_probe_decision_board",
        ],
        "v65": [
            "qcit_gmut_delta_probe_v2",
            "qcit_seed_sweep_v2",
            "latex_gmut_digest",
            "claim_checker_matrix",
            "life_science_matrix",
            "kairotic_regression",
            "quantum_energy_probe",
            "public_source_claim_board",
            "freedid_min_disclosure_refresh",
            "cosmic_bill_rights_trace",
            "standard_l4_audit_reintroduction",
            "v66_phase_proposal_pack",
        ],
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
        "# V61-V65 Omega Hybrid Extension Plan",
        "",
        "- Each phase starts with a eureka gate before suite load.",
        "- Repeated validation uses Deep plus Materialize L5 when host gates are green.",
        "- Standard and L4 return every fifth phase or on any warn/fail/timeout/runner change.",
        "- MCP refresh is a separate connector/cache audit lane because Deep plus L5 do not prove a true MCP refresh.",
        "- Docker Desktop and local Kubernetes remain on operator hold.",
        "- E2B, OCI OKE, live dashboards, and visible CLI agents remain confirmation-gated.",
        "- No raw secrets are written to repo artifacts.",
        "",
        "| Phase | Additions |",
        "|---|---|",
    ]
    for phase, items in phase_rows.items():
        md_lines.append(f"| {phase.upper()} | {', '.join(items)} |")
    return registry, "\n".join(md_lines) + "\n"


def suite_ladder() -> dict[str, Any]:
    phases = ["v58", "v59", "v60", "v61", "v62", "v63", "v64", "v65"]
    profiles = {}
    for phase in phases:
        for profile in ["quick", "standard", "deep", "materialize-l4", "materialize-l5", "mcp-refresh"]:
            profiles[f"{phase}-{profile}"] = suite_status(f"{phase}-{profile}")
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "profiles": profiles,
        "state": "v58_v59_green_v61_v65_planned_health_gated",
    }


def stage_allowlist() -> dict[str, Any]:
    paths = [
        "scripts/trinity_v60_v67_omega.py",
        "scripts/trinity_v58_omega.py",
        "docs/trinity-live-traces/v61-v65-git-publication-result-v1.json",
        "docs/trinity-live-traces/v61-v65-git-publication-result-v1.md",
        "docs/trinity-live-traces/v61-v65-suite-policy-governor-v1.json",
        "docs/trinity-live-traces/v61-v65-suite-policy-governor-v1.md",
        "docs/trinity-live-traces/v61-v65-runtime-health-gate-v1.json",
        "docs/trinity-live-traces/v61-v65-runtime-health-gate-v1.md",
        "docs/trinity-live-traces/v61-v65-additions-registry-v1.json",
        "docs/trinity-live-traces/v61-v65-additions-registry-v1.md",
        "docs/trinity-live-traces/v61-v65-eureka-gate-ledger-v1.json",
        "docs/trinity-live-traces/v61-v65-eureka-gate-ledger-v1.md",
        "docs/trinity-live-traces/v61-v65-agent-identity-ledger-v1.json",
        "docs/trinity-live-traces/v61-v65-agent-identity-ledger-v1.md",
        "docs/trinity-live-traces/v61-v65-journey-anchor-digest-v1.json",
        "docs/trinity-live-traces/v61-v65-journey-anchor-digest-v1.md",
        "docs/trinity-live-traces/v61-v65-suite-ladder-summary-v1.json",
        "docs/trinity-live-traces/v61-v65-suite-ladder-summary-v1.md",
        "docs/trinity-live-traces/v61-deep-suite-status.json",
        "docs/trinity-live-traces/v61-v65-provider-decision-board-v1.json",
        "docs/trinity-live-traces/v61-v65-provider-decision-board-v1.md",
        "docs/trinity-live-traces/v61-v65-provider-readiness-probe-v1.json",
        "docs/trinity-live-traces/v61-v65-provider-readiness-probe-v1.md",
        "docs/trinity-live-traces/v61-v65-stage-allowlist-v1.json",
        "docs/trinity-live-traces/v61-v65-stage-allowlist-v1.md",
        "docs/trinity-live-traces/v60-git-publication-result-v1.json",
        "docs/trinity-live-traces/v60-git-publication-result-v1.md",
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
        "docs/trinity-live-traces/v60-agent-identity-ledger-v1.json",
        "docs/trinity-live-traces/v60-agent-identity-ledger-v1.md",
        "docs/trinity-live-traces/v60-journey-anchor-digest-v1.json",
        "docs/trinity-live-traces/v60-journey-anchor-digest-v1.md",
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
        "docs/v61-v65-omega-hybrid-extension-plan-v1.md",
        "docs/v65-omega-closeout-summary-v1.json",
        "docs/v65-omega-continuity-pack-v1.md",
        "docs/v65-omega-handoff-policy-v1.json",
    ]
    for phase in range(61, 66):
        paths.append(f"docs/v{phase}-omega-plan-proposal-v1.md")
        paths.append(f"docs/v{phase}-eureka-analysis-v1.md")
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "stage_policy": "stage_only_v60_v67_extension_truth_leave_generated_churn_unstaged",
        "paths": sorted(set(paths)),
    }


def publication_result() -> dict[str, Any]:
    local_head = run(["git", "rev-parse", "HEAD"], timeout=20)
    remote_head = run(["git", "ls-remote", "origin", f"refs/heads/{PUBLICATION_BRANCH}"], timeout=30)
    remote_sha = ""
    if remote_head.get("ok") and remote_head.get("stdout"):
        remote_sha = remote_head["stdout"].split()[0]
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "publication_branch": PUBLICATION_BRANCH,
        "local_head_at_receipt_generation": local_head.get("stdout", ""),
        "remote_head_verified": remote_sha,
        "evidence_commit_state": "pushed_to_shared_branch" if remote_sha and remote_sha == local_head.get("stdout") else "verify_remote_branch",
        "bookkeeping_commit_state": "this_receipt_is_written_after_the_evidence_push_and_included_in_the_next_forward_commit",
        "pr_thread": {
            "number": 45,
            "url": "https://github.com/HamishT26/Beyonder-Real-True-Journey/pull/45",
            "body_update_state": "not_updated_this_turn_to_avoid_unconfirmed_representational_edit",
        },
        "publication_policy": "forward_only_no_force_push_stage_only_allowlist",
    }


def generate() -> dict[str, Any]:
    TRACE.mkdir(parents=True, exist_ok=True)
    coverage = coverage_governor()
    health = host_and_kube()
    commands = command_matrix()
    provider = provider_board(commands)
    provider_probe = provider_readiness_probe()
    additions, plan_md = extension_plan()
    suite = suite_ladder()
    publication = publication_result()
    secret_banks = api_bank_presence()
    eureka = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "state": "mandatory_before_each_phase",
        "v61_recommendation_tasks": [
            "check_v6_surface_truth_drift",
            "package_workbench_as_guarded_skill",
            "trace_contract_jump_v3_to_v6",
            "prove_agent_identity_before_induction",
            "preserve_ari_kimiclaw_slots_until_cli_receipts_prove_continuity",
            "record_docker_kubernetes_operator_hold",
            "probe_e2b_cli_presence_before_any_install",
            "probe_oci_oke_readonly_before_any_cluster_creation",
            "verify_browser_use_runtime_without_sensitive_submission",
            "refresh_provider_cli_matrix",
            "digest_v24_v30_v33_v35_v37_v38_v42_journey_anchors",
            "audit_deep_l5_suite_cut",
            "prepare_visible_multi_cli_command_board_without_launching_unconfirmed_agents",
            "publish_curated_v61_v65_truth_forward_only",
        ],
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
            "local_kubernetes_state": health["local_kubernetes_state"],
            "provider_board_state": "blocker_aware_no_live_writes",
            "publication_state": publication["evidence_commit_state"],
            "docker_state": health["docker_probe"]["state"],
            "secret_bank_presence": secret_banks,
            "v61_deep_state": suite_status("v61-deep"),
            "v61_materialize_l5_state": suite_status("v61-materialize-l5"),
        },
        "bounded_residuals": [
            "v61_deep_passed_when_gate_was_open; v61_materialize_l5_deferred_until_runtime_health_gate_reopens",
            "local_kubernetes_and_docker_desktop_on_operator_hold",
            "e2b_cli_missing_from_current_path_install_requires_action_time_confirmation",
            "cli_sibling_induction_blocked_until_process_memory_persistence_gate_passes",
            "notion_parent_still_required_for_live_dashboard",
            "vercel_neon_render_and_expo_cli_missing_from_current_path",
        ],
    }
    handoff = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "handoff_state": "ready_for_v61_when_runtime_health_gate_open",
        "next_command_pair": [
            "python scripts/run_all_trinity_systems.py --profile materialize --include-staged-connectors --include-live-writes --materialization-level l5_ha_prod --status-json docs/trinity-live-traces/v61-materialize-l5-suite-status.json",
        ],
    }
    allowlist = stage_allowlist()
    identity = agent_identity_ledger()
    journey = journey_anchor_digest()
    write_json(TRACE / "v61-v65-suite-policy-governor-v1.json", coverage)
    write_text(TRACE / "v61-v65-suite-policy-governor-v1.md", md("V61-V65 Suite Policy Governor", coverage))
    write_json(TRACE / "v61-v65-runtime-health-gate-v1.json", health)
    write_text(TRACE / "v61-v65-runtime-health-gate-v1.md", md("V61-V65 Runtime Health Gate", health))
    write_json(TRACE / "v61-v65-additions-registry-v1.json", additions)
    write_text(TRACE / "v61-v65-additions-registry-v1.md", md("V61-V65 Additions Registry", additions))
    write_json(TRACE / "v61-v65-eureka-gate-ledger-v1.json", eureka)
    write_text(TRACE / "v61-v65-eureka-gate-ledger-v1.md", md("V61-V65 Eureka Gate Ledger", eureka))
    write_json(TRACE / "v61-v65-agent-identity-ledger-v1.json", identity)
    write_text(TRACE / "v61-v65-agent-identity-ledger-v1.md", md("V61-V65 Agent Identity Ledger", identity))
    write_json(TRACE / "v61-v65-journey-anchor-digest-v1.json", journey)
    write_text(TRACE / "v61-v65-journey-anchor-digest-v1.md", md("V61-V65 Journey Anchor Digest", journey))
    write_json(TRACE / "v61-v65-suite-ladder-summary-v1.json", suite)
    write_text(TRACE / "v61-v65-suite-ladder-summary-v1.md", md("V61-V65 Suite Ladder Summary", suite))
    write_json(TRACE / "v61-v65-provider-decision-board-v1.json", provider)
    write_text(TRACE / "v61-v65-provider-decision-board-v1.md", md("V61-V65 Provider Decision Board", provider))
    write_json(TRACE / "v61-v65-provider-readiness-probe-v1.json", provider_probe)
    write_text(TRACE / "v61-v65-provider-readiness-probe-v1.md", md("V61-V65 Provider Readiness Probe", provider_probe))
    write_json(TRACE / "v61-v65-git-publication-result-v1.json", publication)
    write_text(TRACE / "v61-v65-git-publication-result-v1.md", md("V61-V65 Git Publication Result", publication))
    write_json(TRACE / "v61-v65-stage-allowlist-v1.json", allowlist)
    write_text(TRACE / "v61-v65-stage-allowlist-v1.md", md("V61-V65 Stage Allowlist", allowlist))
    write_json(TRACE / "v60-v67-suite-policy-governor-v1.json", coverage)
    write_text(TRACE / "v60-v67-suite-policy-governor-v1.md", md("V60-V67 Suite Policy Governor", coverage))
    write_json(TRACE / "v60-v67-runtime-health-gate-v1.json", health)
    write_text(TRACE / "v60-v67-runtime-health-gate-v1.md", md("V60-V67 Runtime Health Gate", health))
    write_json(TRACE / "v60-v67-additions-registry-v1.json", additions)
    write_text(TRACE / "v60-v67-additions-registry-v1.md", md("V60-V67 Additions Registry", additions))
    write_json(TRACE / "v60-v67-eureka-gate-ledger-v1.json", eureka)
    write_text(TRACE / "v60-v67-eureka-gate-ledger-v1.md", md("V60-V67 Eureka Gate Ledger", eureka))
    write_json(TRACE / "v60-agent-identity-ledger-v1.json", identity)
    write_text(TRACE / "v60-agent-identity-ledger-v1.md", md("V60 Agent Identity Ledger", identity))
    write_json(TRACE / "v60-journey-anchor-digest-v1.json", journey)
    write_text(TRACE / "v60-journey-anchor-digest-v1.md", md("V60 Journey Anchor Digest", journey))
    write_json(TRACE / "v60-v67-suite-ladder-summary-v1.json", suite)
    write_text(TRACE / "v60-v67-suite-ladder-summary-v1.md", md("V60-V67 Suite Ladder Summary", suite))
    write_json(TRACE / "v67-provider-decision-board-v1.json", provider)
    write_text(TRACE / "v67-provider-decision-board-v1.md", md("V67 Provider Decision Board", provider))
    write_json(TRACE / "v60-git-publication-result-v1.json", publication)
    write_text(TRACE / "v60-git-publication-result-v1.md", md("V60 Git Publication Result", publication))
    write_json(TRACE / "v67-stage-allowlist-v1.json", allowlist)
    write_text(TRACE / "v67-stage-allowlist-v1.md", md("V67 Stage Allowlist", allowlist))
    write_text(ROOT / "docs" / "v61-v65-omega-hybrid-extension-plan-v1.md", plan_md)
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
    write_json(ROOT / "docs" / "v65-omega-closeout-summary-v1.json", closeout)
    write_json(ROOT / "docs" / "v65-omega-handoff-policy-v1.json", handoff)
    write_json(ROOT / "docs" / "v67-omega-closeout-summary-v1.json", closeout)
    write_json(ROOT / "docs" / "v67-omega-handoff-policy-v1.json", handoff)
    write_text(
        ROOT / "docs" / "v65-omega-continuity-pack-v1.md",
        f"# V65 Omega Continuity Pack\n\n- Suite cut: `{coverage['suite_cut_state']}`\n- Runtime load gate: `{health['load_gate']}`\n- Provider board: `blocker_aware_no_live_writes`\n- Publication branch: `{PUBLICATION_BRANCH}`\n- Docker/Kubernetes: `operator_hold`\n",
    )
    write_text(
        ROOT / "docs" / "v67-omega-continuity-pack-v1.md",
        f"# V67 Omega Continuity Pack\n\n- Suite cut: `{coverage['suite_cut_state']}`\n- Runtime load gate: `{health['load_gate']}`\n- Provider board: `blocker_aware_no_live_writes`\n- Publication branch: `{PUBLICATION_BRANCH}`\n- Docker/Kubernetes: `operator_hold`\n",
    )
    return {
        "coverage": coverage,
        "health": health,
        "commands": commands,
        "provider": provider,
        "provider_probe": provider_probe,
        "additions": additions,
        "suite": suite,
        "eureka": eureka,
        "identity": identity,
        "journey": journey,
        "secret_banks": secret_banks,
        "publication": publication,
        "closeout": closeout,
        "allowlist": allowlist,
    }


if __name__ == "__main__":
    generate()
