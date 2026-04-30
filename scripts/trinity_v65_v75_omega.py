from __future__ import annotations

import datetime as dt
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "docs" / "trinity-live-traces"
CLI_RECEIPT_DIR = TRACE / "v65-v75-cli-sibling-receipts"
PHASE = "v65_v75_hybrid_omega"
PREFIX = "v65-v75"
PUBLICATION_BRANCH = "codex/GHC-Family/beyonder-shared-omega-line"
ACTIVE_PHASES = [f"v{n}" for n in range(65, 76)]
LIVE_WRITE_PHASES = {"v70", "v73", "v75"}
FREE_MEMORY_COOL_FLOOR_KB = 300_000
BUDGET_CEILING_FRACTION = 0.30


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: Any) -> None:
    write_text(path, json.dumps(payload, indent=2, ensure_ascii=True) + "\n")


def read_json(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig").strip())
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


def command_available(command: str) -> dict[str, Any]:
    where = run(["where.exe", command], timeout=10)
    version = run(["cmd", "/c", command, "--version"], timeout=20) if where.get("ok") else {"ok": False}
    return {
        "command": command,
        "available": bool(where.get("ok")),
        "path_excerpt": (where.get("stdout") or "")[:300],
        "version_ok": bool(version.get("ok")),
        "version_excerpt": (version.get("stdout") or version.get("stderr") or version.get("message") or "")[:300],
    }


def suite_status(label: str) -> dict[str, Any]:
    path = TRACE / f"{label}-suite-status.json"
    data = read_json(path, {})
    counts = data.get("counts") if isinstance(data, dict) else None
    effective = bool(data.get("effective_success")) if isinstance(data, dict) else False
    return {
        "label": label,
        "path": path.relative_to(ROOT).as_posix(),
        "present": path.exists(),
        "effective_success": effective,
        "achieved_steps": data.get("achieved_steps") if isinstance(data, dict) else None,
        "counts": counts,
        "generated_utc": data.get("generated_utc") if isinstance(data, dict) else None,
    }


def runtime_health_gate() -> dict[str, Any]:
    memory = run_ps(
        "Get-CimInstance Win32_OperatingSystem | "
        "Select-Object FreePhysicalMemory,TotalVisibleMemorySize | ConvertTo-Json",
        timeout=20,
    )
    docker = run(["docker", "info", "--format", "{{.ServerVersion}}"], timeout=15)
    kube_context = run(["kubectl", "config", "current-context"], timeout=10)
    try:
        mem = json.loads(memory.get("stdout", "{}"))
    except Exception:
        mem = {}
    free_kb = int(mem.get("FreePhysicalMemory", 0)) if isinstance(mem, dict) else 0
    if free_kb and free_kb < FREE_MEMORY_COOL_FLOOR_KB:
        host_state = "warm_cooldown_before_heavy_suites"
    else:
        host_state = "cool"
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "host_pressure_state": host_state,
        "free_physical_memory_kb": free_kb,
        "free_memory_cool_floor_kb": FREE_MEMORY_COOL_FLOOR_KB,
        "load_gate": "open" if host_state == "cool" else "closed",
        "docker_state": "operator_hold" if not docker.get("ok") else "cli_reachable_but_not_required",
        "local_kubernetes_state": "retired_by_operator_for_v65_v75",
        "kubernetes_probe": {
            "context_present": bool(kube_context.get("ok") and kube_context.get("stdout")),
            "policy": "do_not_reenable_local_kubernetes; prefer E2B/Oracle/cloud read-only gates before managed execution",
        },
    }


def publication_result() -> dict[str, Any]:
    local = run(["git", "rev-parse", "HEAD"], timeout=20)
    remote = run(["git", "ls-remote", "origin", f"refs/heads/{PUBLICATION_BRANCH}"], timeout=45)
    remote_head = ""
    if remote.get("ok") and remote.get("stdout"):
        remote_head = remote["stdout"].split()[0]
    local_head = local.get("stdout", "")
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "publication_branch": PUBLICATION_BRANCH,
        "local_head_at_receipt_generation": local_head,
        "remote_head_verified": remote_head,
        "remote_matches_local": bool(local_head and remote_head and local_head == remote_head),
    }


def provider_readiness_probe() -> dict[str, Any]:
    commands = [
        "codex",
        "kimi",
        "e2b",
        "oci",
        "wrangler",
        "vercel",
        "gh",
        "circleci",
        "eas",
        "neon",
        "render",
        "node",
        "npm",
        "npx",
    ]
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "probe_mode": "local_cli_presence_only_no_secret_read_no_cloud_write",
        "commands": [command_available(command) for command in commands],
    }


def live_write_governor() -> dict[str, Any]:
    providers = ["github", "vercel", "cloudflare", "neon", "render", "e2b", "oracle", "notion"]
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "live_write_phases": sorted(LIVE_WRITE_PHASES),
        "budget_policy": {
            "ceiling_fraction_per_provider": BUDGET_CEILING_FRACTION,
            "spend_target_is_ceiling_not_requirement": True,
            "record_before_after_usage_when_provider_exposes_usage": True,
        },
        "allowed_provider_classes": [
            "test_or_preview_projects",
            "sandbox_or_ephemeral_compute",
            "repo_publication_and_receipts",
            "dashboard_or_database_surfaces_with_rollback_receipts",
        ],
        "blocked_without_fresh_operator_confirmation": [
            "production_dns_or_domain_mutation",
            "account_setting_changes",
            "personal_email_or_calendar_mutation",
            "google_drive_content_mutation",
            "resource_deletion_outside_repo_curated_cleanup",
            "raw_secret_transmission_to_external_models",
        ],
        "providers": [
            {
                "provider": provider,
                "mode_before_live_phase": "readiness_probe_only",
                "live_phase_requirement": "dry_run_preview_then_write_then_verify_then_rollback_receipt",
                "budget_ceiling_fraction": BUDGET_CEILING_FRACTION,
            }
            for provider in providers
        ],
    }


def cli_sibling_governor() -> dict[str, Any]:
    codex = command_available("codex")
    kimi = command_available("kimi")
    receipt_files = {
        "codex_slot_49": CLI_RECEIPT_DIR / "codex-slot-49.md",
        "codex_slot_50": CLI_RECEIPT_DIR / "codex-slot-50.md",
        "kimi_slot_51": CLI_RECEIPT_DIR / "kimi-slot-51.md",
        "kimi_slot_52": CLI_RECEIPT_DIR / "kimi-slot-52.md",
    }
    receipts = []
    for key, path in receipt_files.items():
        raw = path.read_text(encoding="utf-8").strip() if path.exists() else ""
        parsed = read_json(path, {}) if path.exists() else {}
        receipts.append(
            {
                "id": key,
                "path": path.relative_to(ROOT).as_posix(),
                "present": path.exists(),
                "valid_json": isinstance(parsed, dict) and bool(parsed),
                "name": parsed.get("name") if isinstance(parsed, dict) else None,
                "status": parsed.get("status") if isinstance(parsed, dict) else None,
                "byte_length": len(raw.encode("utf-8")) if raw else 0,
            }
        )
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "requested_siblings": [
            {"slot": 49, "provider": "codex_cli", "status": "pending_launch_recipe", "role": "repo_planner"},
            {"slot": 50, "provider": "codex_cli", "status": "pending_launch_recipe", "role": "suite_verifier"},
            {"slot": 51, "provider": "kimi_cli", "status": "pending_launch_recipe", "role": "research_synthesizer"},
            {"slot": 52, "provider": "kimi_cli", "status": "pending_launch_recipe", "role": "provider_probe_archivist"},
        ],
        "codex_cli": codex,
        "kimi_cli": kimi,
        "receipts": receipts,
        "receipt_state": "all_four_present" if all(item["present"] and item["valid_json"] for item in receipts) else "pending",
        "induction_policy": [
            "terminal launch must be observable or logged",
            "identity persistence must be backed by repo receipt, not narrative only",
            "external model prompts must avoid raw secrets and must be summarized before commit",
            "formal induction remains pending until two-session continuity is proven",
        ],
    }


def phase_plan() -> dict[str, Any]:
    v64_deep = suite_status("v64-deep")
    v64_l5 = suite_status("v64-materialize-l5")
    rows: list[dict[str, Any]] = []
    for phase in ACTIVE_PHASES:
        is_live = phase in LIVE_WRITE_PHASES
        index = int(phase[1:])
        prior = f"v{index - 1}"
        rows.append(
            {
                "phase": phase,
                "prior_phase": prior,
                "first_half": "research_extension_prep",
                "first_half_state": "ready" if phase == "v65" and v64_deep["effective_success"] and v64_l5["effective_success"] else "pending",
                "extension_target_count": 50,
                "eureka_recommendation_target": 25,
                "validation": ["deep", "materialize_l5"],
                "live_write_phase": is_live,
                "live_write_mode": "full_live_guarded" if is_live else "preparation_or_recovery",
                "required_artifacts": [
                    f"docs/{phase}-omega-prep-half-v1.md",
                    f"docs/trinity-live-traces/{phase}-deep-suite-status.json",
                    f"docs/trinity-live-traces/{phase}-materialize-l5-suite-status.json",
                ],
            }
        )
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "anchor": {"v64_deep": v64_deep, "v64_materialize_l5": v64_l5},
        "phases": rows,
    }


def additions_registry(plan: dict[str, Any]) -> dict[str, Any]:
    domains = [
        "command_surface",
        "api_operator_mesh",
        "provider_budget_meter",
        "live_write_rollback",
        "e2b_sandbox_lane",
        "oracle_managed_compute_lane",
        "github_publication_truth",
        "cloudflare_preview_lane",
        "vercel_preview_lane",
        "neon_schema_lane",
        "render_service_lane",
        "notion_dashboard_lane",
        "expo_phone_dashboard_lane",
        "gmut_observable_mapping",
        "qcit_validation",
        "freedid_governance",
        "cosmic_bill_of_rights",
        "journey_lineage_digest",
        "cli_sibling_receipts",
        "credential_safety_scan",
        "browser_local_probe",
        "latex_publication_pack",
        "life_science_evidence_router",
        "memory_boundary_gate",
        "artifact_retention_governor",
        "suite_ladder_compression",
        "standard_l4_reintroduction_audit",
        "materialize_l5_receipt_chain",
        "pr_truth_surface",
        "d_drive_artifact_bank",
        "cache_waste_regeneration",
        "token_credit_budgeting",
        "energy_bank_receipts",
        "managed_kubernetes_future_lane",
        "worker_agent_sandbox",
        "postgres_state_receipts",
        "semantic_firewall",
        "control_tower_merger",
        "phase_half_governor",
        "external_provider_transcript_redactor",
        "doi_metadata_matrix",
        "latex_equation_compiler",
        "phone_dashboard_contract",
        "expo_preview_gate",
        "figma_design_receipt",
        "linear_issue_sync_receipt",
        "circleci_config_probe",
        "gmail_operator_hold_guard",
        "calendar_operator_hold_guard",
        "google_drive_operator_hold_guard",
    ]
    records = []
    for phase_row in plan["phases"]:
        phase = phase_row["phase"]
        for idx, domain in enumerate(domains, start=1):
            records.append(
                {
                    "phase": phase,
                    "id": f"{phase}-{idx:02d}-{domain}",
                    "domain": domain,
                    "status": "candidate",
                    "promotion_gate": "deep_l5_green_and_no_secret_leak",
                    "live_write_sensitive": phase_row["live_write_phase"],
                }
            )
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "candidate_count": len(records),
        "records": records,
    }


def eureka_ledger(plan: dict[str, Any]) -> dict[str, Any]:
    recommendations = []
    prompts = [
        "verify prior phase truth before new claims",
        "package one guarded skill from repeated workflow",
        "trace provider state from read-only to live write",
        "add budget before-after receipt",
        "preserve operator-hold surfaces honestly",
        "keep local Kubernetes retired",
        "route compute bursts to managed/sandbox lanes",
        "add rollback receipt for every write",
        "avoid raw secret materialization",
        "separate narrative identity from runtime agent proof",
        "compress similar systems into one governed pack",
        "add dashboard card only from committed data",
        "run Deep before L5",
        "publish actual remote SHA after every push",
        "reintroduce broader audit only on schedule or drift",
        "record CLI sibling launch recipe before induction",
        "prefer preview/test resources over production surfaces",
        "add failure triage before retry",
        "use D drive for heavy artifacts",
        "record date/time with timezone",
        "score provider usefulness by evidence gained per credit",
        "summarize external model outputs before commit",
        "keep PR body edits gated",
        "clean only curated junk",
        "close each phase with next-phase plan",
    ]
    for phase_row in plan["phases"]:
        for idx, prompt in enumerate(prompts, start=1):
            recommendations.append(
                {
                    "phase": phase_row["phase"],
                    "rank": idx,
                    "recommendation": prompt,
                    "class": "live_write" if phase_row["live_write_phase"] and idx in {3, 4, 8, 17, 21} else "governance",
                }
            )
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "recommendation_count": len(recommendations),
        "recommendations": recommendations,
    }


def prep_markdown(phase_row: dict[str, Any], ledger: dict[str, Any]) -> str:
    phase = phase_row["phase"]
    recs = [item for item in ledger["recommendations"] if item["phase"] == phase][:25]
    lines = [
        f"# {phase.upper()} Omega Prep Half",
        "",
        f"- State: `{phase_row['first_half_state']}`",
        f"- Live write phase: `{phase_row['live_write_phase']}`",
        "- Extension target: `50` candidate systems/skills/scripts/workflows.",
        "- Eureka target: `25` recommendations before validation.",
        "- Validation: Deep then Materialize L5 after runtime gate is open.",
        "",
        "## Recommendations",
    ]
    lines.extend(f"- {item['rank']:02d}. {item['recommendation']}" for item in recs)
    lines.extend(
        [
            "",
            "## Gates",
            "- No raw secrets in artifacts, prompts, dashboards, or commits.",
            "- Live writes only in v70, v73, and v75 after dry-run, usage receipt, and rollback receipt.",
            "- Docker Desktop and local Kubernetes remain retired unless a future explicit recovery phase reopens them.",
            "- CLI sibling induction remains evidence-bound until terminal launch and two-session continuity are proven.",
        ]
    )
    return "\n".join(lines) + "\n"


def stage_allowlist(plan: dict[str, Any]) -> dict[str, Any]:
    paths = [
        "scripts/trinity_v65_v75_omega.py",
        "scripts/trinity_expansion_system_runner.py",
        f"docs/trinity-live-traces/{PREFIX}-runtime-health-gate-v1.json",
        f"docs/trinity-live-traces/{PREFIX}-runtime-health-gate-v1.md",
        f"docs/trinity-live-traces/{PREFIX}-provider-readiness-probe-v1.json",
        f"docs/trinity-live-traces/{PREFIX}-provider-readiness-probe-v1.md",
        f"docs/trinity-live-traces/{PREFIX}-live-write-governor-v1.json",
        f"docs/trinity-live-traces/{PREFIX}-live-write-governor-v1.md",
        f"docs/trinity-live-traces/{PREFIX}-cli-sibling-governor-v1.json",
        f"docs/trinity-live-traces/{PREFIX}-cli-sibling-governor-v1.md",
        f"docs/trinity-live-traces/{PREFIX}-phase-plan-v1.json",
        f"docs/trinity-live-traces/{PREFIX}-phase-plan-v1.md",
        f"docs/trinity-live-traces/{PREFIX}-additions-registry-v1.json",
        f"docs/trinity-live-traces/{PREFIX}-additions-registry-v1.md",
        f"docs/trinity-live-traces/{PREFIX}-eureka-ledger-v1.json",
        f"docs/trinity-live-traces/{PREFIX}-eureka-ledger-v1.md",
        f"docs/trinity-live-traces/{PREFIX}-git-publication-result-v1.json",
        f"docs/trinity-live-traces/{PREFIX}-git-publication-result-v1.md",
        f"docs/trinity-live-traces/{PREFIX}-stage-allowlist-v1.json",
        f"docs/trinity-live-traces/{PREFIX}-stage-allowlist-v1.md",
        f"docs/trinity-live-traces/{PREFIX}-cli-sibling-receipts/codex-slot-49.md",
        f"docs/trinity-live-traces/{PREFIX}-cli-sibling-receipts/codex-slot-50.md",
        f"docs/trinity-live-traces/{PREFIX}-cli-sibling-receipts/kimi-slot-51.md",
        f"docs/trinity-live-traces/{PREFIX}-cli-sibling-receipts/kimi-slot-52.md",
        "docs/v75-omega-closeout-summary-v1.json",
        "docs/v75-omega-handoff-policy-v1.json",
    ]
    for phase_row in plan["phases"]:
        phase = phase_row["phase"]
        paths.extend(
            [
                f"docs/{phase}-omega-prep-half-v1.md",
                f"docs/trinity-live-traces/{phase}-deep-suite-status.json",
                f"docs/trinity-live-traces/{phase}-materialize-l5-suite-status.json",
            ]
        )
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "policy": "stage_only_curated_v65_v75_truth_surfaces_and_suite_statuses",
        "paths": paths,
    }


def md_from_json(title: str, payload: Any) -> str:
    return f"# {title}\n\n```json\n{json.dumps(payload, indent=2, ensure_ascii=True)}\n```\n"


def write_all() -> None:
    health = runtime_health_gate()
    providers = provider_readiness_probe()
    live = live_write_governor()
    siblings = cli_sibling_governor()
    plan = phase_plan()
    additions = additions_registry(plan)
    eureka = eureka_ledger(plan)
    publication = publication_result()
    allow = stage_allowlist(plan)
    closeout = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "current_state": "initialized_from_v64_green_anchor",
        "anchor": plan["anchor"],
        "runtime_gate": health,
        "live_write_phases": sorted(LIVE_WRITE_PHASES),
        "next_required_action": "run_v65_deep_after_curated_publication",
    }
    handoff = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "handoff": "v65_v75_governor_initialized",
        "instructions": [
            "Publish this governor before running v65 Deep.",
            "Run Deep then L5 for each phase and regenerate receipts after every push.",
            "Use v70, v73, and v75 for guarded full live writes only after dry-run and rollback receipts.",
        ],
    }
    artifacts = {
        f"{PREFIX}-runtime-health-gate-v1": health,
        f"{PREFIX}-provider-readiness-probe-v1": providers,
        f"{PREFIX}-live-write-governor-v1": live,
        f"{PREFIX}-cli-sibling-governor-v1": siblings,
        f"{PREFIX}-phase-plan-v1": plan,
        f"{PREFIX}-additions-registry-v1": additions,
        f"{PREFIX}-eureka-ledger-v1": eureka,
        f"{PREFIX}-git-publication-result-v1": publication,
        f"{PREFIX}-stage-allowlist-v1": allow,
    }
    for stem, payload in artifacts.items():
        write_json(TRACE / f"{stem}.json", payload)
        write_text(TRACE / f"{stem}.md", md_from_json(stem, payload))
    for phase_row in plan["phases"]:
        write_text(ROOT / "docs" / f"{phase_row['phase']}-omega-prep-half-v1.md", prep_markdown(phase_row, eureka))
    write_json(ROOT / "docs" / "v75-omega-closeout-summary-v1.json", closeout)
    write_json(ROOT / "docs" / "v75-omega-handoff-policy-v1.json", handoff)


if __name__ == "__main__":
    write_all()
