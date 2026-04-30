#!/usr/bin/env python3
"""V76 to V84 Hybrid Omega phase surfaces and candidate promotion."""

from __future__ import annotations

import datetime as dt
import json
import os
import shutil
import subprocess
from copy import deepcopy
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TRACE = DOCS / "trinity-live-traces"
REPORT_DIR = TRACE / "v76-v84-cli-reports"
RESULT_DIR = TRACE / "v76-v84-candidate-system-results"
PHASE = "v76_v84_hybrid_omega"
PREFIX = "v76-v84"
PUBLICATION_BRANCH = "codex/GHC-Family/beyonder-shared-omega-line"
ACTIVE_PHASES = [f"v{n}" for n in range(76, 85)]
LIVE_WRITE_PHASES = {f"v{n}" for n in range(78, 85)}
FREE_MEMORY_FLOOR_KB = 300_000
MANIFEST = DOCS / "trinity-expansion-system-manifest-v17.json"
V74_PACK = TRACE / "v65-v75-cli-reports" / "v74-system-expansion-candidate-pack-v1.json"


NEXT_CANDIDATES = [
    ("v76_01_phase_ledger_entry_gate", "trinity", "require each phase to start from branch, head, receipt, suite, live-write, and memory-floor facts"),
    ("v76_02_candidate_promotion_receipt_index", "trinity", "index promoted candidates, runner paths, and latest outputs before suite count movement"),
    ("v76_03_live_write_escalation_schedule_guard", "heart", "keep v76 and v77 bounded while v78-v84 require guarded live preflight receipts"),
    ("v76_04_cli_lane_report_digest_compiler", "body", "compact lane reports into a phase report without reopening heavy terminals"),
    ("v76_05_manifest_output_path_collision_guard", "body", "detect new systems that would overwrite existing latest outputs"),
    ("v76_06_suite_profile_delta_matrix", "trinity", "record which systems participate in Deep, L5, and future standard profiles"),
    ("v76_07_operator_hold_label_enforcer", "heart", "label held personal/account surfaces in every live-write preflight"),
    ("v76_08_git_receipt_one_step_lag_explainer", "trinity", "preserve the one-step publication receipt pattern explicitly"),
    ("v76_09_candidate_result_markdown_parity_check", "body", "ensure every JSON candidate result has a matching readable markdown surface"),
    ("v76_10_gmut_qcit_evidence_labeler", "mind", "label GMUT/QCIT claims as executable, citation-backed, philosophical, or open speculation"),
    ("v76_11_freedid_consent_surface_map", "heart", "map Freed ID and CBR consent boundaries onto live phase decisions"),
    ("v76_12_d_drive_heavy_artifact_router", "body", "keep heavy phase artifacts on D drive while preserving curated repo outputs"),
    ("v76_13_memory_floor_event_log", "body", "record when suites begin below, near, or safely above the 300 MB floor"),
    ("v76_14_external_provider_mode_labeler", "body", "separate read-only, dry-run, sandbox, and production-prohibited provider modes"),
    ("v76_15_report_truth_label_taxonomy", "trinity", "tag reports as executable proof, receipt-backed reflection, operator hold, sandbox proposal, or philosophy"),
    ("v76_16_phase_closeout_minimum_fields_gate", "trinity", "require status, boundaries, changes, validation, risks, and next action in closeouts"),
    ("v76_17_suite_artifact_marker_diff", "trinity", "diff live-write marker hits between L5 status artifacts"),
    ("v76_18_candidate_merge_safety_fixture", "body", "require replacement coverage before reducing official system counts"),
    ("v76_19_provider_budget_snapshot_stub", "body", "record free-trial and budget ceilings without requiring spend"),
    ("v76_20_v77_handoff_question_board", "trinity", "prepare the concrete questions v77 must answer before execution"),
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
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return default


def run(args: list[str], timeout: int = 45) -> dict[str, Any]:
    try:
        proc = subprocess.run(
            args,
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
        )
        return {"ok": proc.returncode == 0, "stdout": proc.stdout.strip(), "stderr": proc.stderr.strip(), "returncode": proc.returncode}
    except Exception as exc:
        return {"ok": False, "error": type(exc).__name__, "message": str(exc)}


def run_ps(command: str, timeout: int = 30) -> dict[str, Any]:
    return run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command], timeout=timeout)


def hyphen(value: str) -> str:
    return value.replace("_", "-")


def command_available(command: str) -> dict[str, Any]:
    where = run(["where.exe", command], timeout=10)
    version = run([command, "--version"], timeout=20) if where.get("ok") else {"ok": False}
    return {
        "command": command,
        "available": bool(where.get("ok")),
        "path_excerpt": str(where.get("stdout") or "")[:220],
        "version_ok": bool(version.get("ok")),
        "version_excerpt": str(version.get("stdout") or version.get("stderr") or version.get("message") or "")[:220],
    }


def suite_status(label: str) -> dict[str, Any]:
    path = TRACE / f"{label}-suite-status.json"
    data = read_json(path, {})
    return {
        "label": label,
        "path": path.relative_to(ROOT).as_posix(),
        "present": path.exists(),
        "effective_success": bool(data.get("effective_success")) if isinstance(data, dict) else False,
        "achieved_steps": data.get("achieved_steps") if isinstance(data, dict) else None,
        "counts": data.get("counts") if isinstance(data, dict) else None,
        "expansion_systems_total": data.get("expansion_systems_total") if isinstance(data, dict) else None,
        "expansion_systems_passed": data.get("expansion_systems_passed") if isinstance(data, dict) else None,
        "generated_utc": data.get("generated_utc") if isinstance(data, dict) else None,
    }


def runtime_health_gate() -> dict[str, Any]:
    memory = run_ps(
        "Get-CimInstance Win32_OperatingSystem | Select-Object FreePhysicalMemory,TotalVisibleMemorySize | ConvertTo-Json",
        timeout=20,
    )
    try:
        mem = json.loads(memory.get("stdout", "{}"))
    except Exception:
        mem = {}
    free_kb = int(mem.get("FreePhysicalMemory", 0)) if isinstance(mem, dict) else 0
    c_free = int(shutil.disk_usage("C:\\").free / (1024 * 1024)) if Path("C:\\").exists() else 0
    d_free = int(shutil.disk_usage("D:\\").free / (1024 * 1024)) if Path("D:\\").exists() else 0
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "free_physical_memory_kb": free_kb,
        "free_memory_floor_kb": FREE_MEMORY_FLOOR_KB,
        "load_gate": "open" if free_kb >= FREE_MEMORY_FLOOR_KB else "closed",
        "c_drive_free_mb": c_free,
        "d_drive_free_mb": d_free,
        "local_kubernetes_state": "retired_by_operator_for_v76_v84",
        "docker_desktop_state": "operator_hold",
        "execution_policy": "one_heavy_lane_at_a_time_with_cli_lanes_as_receipt_backed_reports",
    }


def provider_probe() -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "probe_mode": "local_cli_presence_only_no_secret_read_no_cloud_write",
        "commands": [command_available(cmd) for cmd in ("codex", "kimi", "gh", "e2b", "oci", "vercel", "wrangler", "node", "npm", "npx")],
    }


def load_v74_candidates() -> list[dict[str, str]]:
    payload = read_json(V74_PACK, {})
    rows = payload.get("candidates", []) if isinstance(payload, dict) else []
    return [row for row in rows if isinstance(row, dict) and str(row.get("id", "")).startswith("v74_")]


def manifest_entry(candidate: dict[str, str]) -> dict[str, Any]:
    system_id = str(candidate["id"])
    output = f"docs/trinity-expansion/{hyphen(system_id)}-latest.json"
    result = f"docs/trinity-live-traces/v76-v84-candidate-system-results/{hyphen(system_id)}.json"
    return {
        "system_id": system_id,
        "pillar": str(candidate.get("pillar") or "trinity"),
        "script": "scripts/trinity_v76_candidate_systems.py",
        "mode": "offline",
        "profiles": ["deep", "materialize"],
        "outputs": [output],
        "depends_on": [
            "docs/trinity-live-traces/v65-v75-cli-reports/v74-system-expansion-candidate-pack-v1.json",
            "docs/trinity-live-traces/v65-v75-cli-reports/v75-grand-closeout-council-report-v1.md",
            "docs/trinity-live-traces/v75-materialize-l5-suite-status.json",
        ],
        "timeout_sec": 90,
        "wave": "v76_promoted_candidate_wave",
        "track": "v76_candidate_promotion",
        "gate_level": "support",
        "cache_artifacts": [],
        "pack": "v76_candidate_promotion",
        "phase": "v76",
        "activation_group": "v76_candidate_promotion",
        "continuity_band": "v76",
        "materialization_level": "readiness_only",
        "authority_scope": "repo_only",
        "command_surface": "no",
        "council_scope": "receipt_backed_cli_lanes",
        "provisional_induction": False,
        "autonomy_track": "bounded",
        "sync_surface": "repo_only",
        "induction_phase": "not_applicable",
        "mesh_proof_mode": "receipt_backed_lane",
        "proof_pass": "v76",
        "official_induction": False,
        "workbench_surface": "repo",
        "storage_surface": "repo",
        "cloud_archive_state": "operator_hold",
        "continuity_posture": "v76_runner_backed_candidate",
        "cleanup_class": "candidate_promotion",
        "retention_scope": "v76_v84_curated",
        "research_surface": "repo_or_cache",
        "canon_surface": "supporting",
        "historical_source_band": "v65_to_v76",
        "evidence_posture": "runner_backed_candidate",
        "subagent_lane": "cli_report_lane",
        "official_after_proof": False,
        "multi_instance_scope": "single_heavy_lane",
        "codex_agent_path": "",
        "delegation_lane": "receipt_backed_cli",
        "model_resolution_strategy": "repo_first_receipt_backed",
        "checkpoint_class": "shared_full_suite_authority",
        "evidence_lane": "shared_full_suite",
        "shared_latest_eligible": True,
        "runner_mode": "passthrough_command",
        "runner_command": ["python3", "scripts/trinity_v76_candidate_systems.py", "--system-id", system_id],
        "runner_success_json": result,
        "runner_targets": [
            result,
            f"docs/trinity-live-traces/v76-v84-candidate-system-results/{hyphen(system_id)}.md",
        ],
        "source_candidate_id": system_id,
        "candidate_purpose": str(candidate.get("purpose") or ""),
    }


def ensure_manifest_promotions() -> dict[str, Any]:
    manifest = read_json(MANIFEST, {})
    rows = manifest.get("systems", []) if isinstance(manifest, dict) else []
    rows = [row for row in rows if isinstance(row, dict)]
    before_count = len(rows)
    candidates = load_v74_candidates()
    index = {str(row.get("system_id")): row for row in rows}
    added: list[str] = []
    refreshed: list[str] = []
    for candidate in candidates:
        entry = manifest_entry(candidate)
        system_id = entry["system_id"]
        if system_id in index:
            index[system_id].update(entry)
            refreshed.append(system_id)
        else:
            rows.append(entry)
            added.append(system_id)
    manifest["systems"] = rows
    manifest["generated_utc"] = now_iso()
    manifest["description"] = (
        "V17 shared manifest with the v76 runner-backed promotion of the 20 v74 candidate systems. "
        "Official suite counts move only after Deep and L5 status artifacts prove the expansion."
    )
    write_json(MANIFEST, manifest)
    return {
        "generated_utc": now_iso(),
        "manifest_path": MANIFEST.relative_to(ROOT).as_posix(),
        "before_count": before_count,
        "after_count": len(rows),
        "added_count": len(added),
        "refreshed_count": len(refreshed),
        "added_systems": added,
        "refreshed_systems": refreshed,
        "promotion_rule": "runner_backed_first_suite_count_after_green_deep_and_l5",
    }


def phase_plan(manifest_promotion: dict[str, Any]) -> dict[str, Any]:
    phases: list[dict[str, Any]] = []
    for phase in ACTIVE_PHASES:
        index = int(phase[1:])
        prior = f"v{index - 1}"
        phases.append(
            {
                "phase": phase,
                "live_write_phase": phase in LIVE_WRITE_PHASES,
                "planning_policy": "plan_only_after_prior_l5_green" if phase != "v76" else "start_from_v75_green_anchor",
                "suite_policy": "deep_then_l5",
                "first_half_focus": "promote_runner_backed_candidates" if phase == "v76" else "derive_from_prior_phase_results",
                "prior_deep": suite_status(f"{prior}-deep"),
                "prior_l5": suite_status(f"{prior}-materialize-l5"),
                "candidate_expansion_target": 20,
                "eureka_recommendation_target": 20,
            }
        )
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "active_phases": ACTIVE_PHASES,
        "live_write_phases": sorted(LIVE_WRITE_PHASES),
        "bounded_phases": ["v76", "v77"],
        "anchor": {
            "v75_deep": suite_status("v75-deep"),
            "v75_l5": suite_status("v75-materialize-l5"),
            "latest_pushed_commit": run(["git", "rev-parse", "HEAD"], timeout=20).get("stdout", ""),
        },
        "manifest_promotion": manifest_promotion,
        "phases": phases,
    }


def eureka_ledger() -> dict[str, Any]:
    recommendations = [
        "Start v76 with a phase ledger before every suite.",
        "Promote exactly the v74 candidate pack before inventing fresh count movement.",
        "Keep v76 and v77 bounded; do not perform provider writes.",
        "Treat v78-v84 live writes as guarded tracer/preflight phases unless explicit sandbox receipts exist.",
        "Require every candidate system to have runner_command and runner_success_json.",
        "Require markdown parity for every JSON proof artifact.",
        "Keep CLI siblings receipt-backed, not private-memory-overclaimed.",
        "Scan L5 artifacts for external mutation markers after every live phase.",
        "Keep Google Drive, Gmail, Calendar, account settings, and DNS on operator-hold without fresh confirmation.",
        "Add suite-count delta guards before official count claims.",
        "Permit count reduction only after replacement coverage passes.",
        "Record provider posture as read-only, dry-run, sandbox, or production-prohibited.",
        "Use GitHub publication receipts as the durable council exchange layer.",
        "Keep one heavy lane at a time until managed cloud compute is proven.",
        "Use D drive as the heavy-artifact home and curated repo files as publication truth.",
        "Separate executable proof, receipt-backed reflection, sandbox proposal, and philosophy labels.",
        "Keep GMUT/QCIT/Freed ID claims mapped to evidence categories.",
        "Refresh v77 planning only after v76 L5 status is green.",
        "Stage only the v76-v84 allowlist; leave generated churn unstaged.",
        "Regenerate publication receipt from the actual pushed content commit.",
    ]
    return {
        "generated_utc": now_iso(),
        "phase": "v76_omega",
        "target_count": 20,
        "recommendations": [{"id": f"v76_eureka_{idx:02d}", "recommendation": text} for idx, text in enumerate(recommendations, start=1)],
    }


def system_expansion_pack(manifest_promotion: dict[str, Any]) -> dict[str, Any]:
    promoted = load_v74_candidates()
    return {
        "generated_utc": now_iso(),
        "phase": "v76_omega",
        "state": "v74_candidates_promoted_and_v77_candidates_seeded",
        "promoted_candidates": promoted,
        "next_candidate_seed_pack": [
            {"id": cid, "pillar": pillar, "state": "candidate_only_not_suite_counted", "purpose": purpose}
            for cid, pillar, purpose in NEXT_CANDIDATES
        ],
        "manifest_promotion": manifest_promotion,
        "count_policy": "counts may increase only after Deep and L5 status files prove promoted systems pass",
    }


def phase_ledger(health: dict[str, Any], plan: dict[str, Any], manifest_promotion: dict[str, Any]) -> str:
    head = run(["git", "rev-parse", "--short", "HEAD"], timeout=20).get("stdout", "")
    branch = run(["git", "branch", "--show-current"], timeout=20).get("stdout", "")
    lines = [
        "# V76 Omega Phase Ledger",
        "",
        f"- generated_utc: `{now_iso()}`",
        f"- branch: `{branch}`",
        f"- head: `{head}`",
        f"- v75 deep green: `{plan['anchor']['v75_deep']['effective_success']}`",
        f"- v75 L5 green: `{plan['anchor']['v75_l5']['effective_success']}`",
        f"- memory free KB: `{health['free_physical_memory_kb']}`",
        f"- memory floor KB: `{FREE_MEMORY_FLOOR_KB}`",
        f"- local Kubernetes: `{health['local_kubernetes_state']}`",
        f"- Docker Desktop: `{health['docker_desktop_state']}`",
        f"- promoted v74 candidates added: `{manifest_promotion['added_count']}`",
        f"- promoted v74 candidates refreshed: `{manifest_promotion['refreshed_count']}`",
        f"- live-write policy: `v76 and v77 bounded; v78-v84 guarded only`",
        "",
        "## Next Action",
        "",
        "Run v76 Deep, then v76 Materialize L5. Only after both are green should v77 planning become authoritative.",
    ]
    return "\n".join(lines).rstrip() + "\n"


def v77_plan_markdown(plan: dict[str, Any], expansion: dict[str, Any]) -> str:
    v76_deep = suite_status("v76-deep")
    v76_l5 = suite_status("v76-materialize-l5")
    next_candidates = expansion["next_candidate_seed_pack"][:20]
    lines = [
        "# V77 Omega Plan Proposal",
        "",
        f"- generated_utc: `{now_iso()}`",
        f"- v76 deep green: `{v76_deep['effective_success']}`",
        f"- v76 L5 green: `{v76_l5['effective_success']}`",
        f"- v76 deep counts: `{v76_deep['counts']}`",
        f"- v76 L5 counts: `{v76_l5['counts']}`",
        "- live-write state: `bounded; no provider writes`",
        "- expansion posture: `20 v74 candidates promoted and suite-proven; 20 v76 candidates seeded but not suite-counted`",
        "",
        "## V77 Focus",
        "",
        "V77 should turn the best v76 seed candidates into a smaller second promotion wave only after their runner paths and pass criteria are written. The first target should be quality and consolidation rather than raw count growth: phase ledger gates, markdown parity, output collision checks, and truth-label taxonomy.",
        "",
        "## Candidate Seeds For V77",
        "",
    ]
    for item in next_candidates:
        lines.append(f"- `{item['id']}` ({item['pillar']}): {item['purpose']}")
    lines.extend(
        [
            "",
            "## Execution Order",
            "",
            "1. Promote only the candidates that can be made executable in a bounded local runner.",
            "2. Run direct candidate sweeps before any suite.",
            "3. Run v77 Deep.",
            "4. Run v77 bounded Materialize L5.",
            "5. Publish the content commit, regenerate publication receipt from the actual pushed head, then publish the receipt.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def report_markdown(title: str, payload: Any) -> str:
    return f"# {title}\n\n```json\n{json.dumps(payload, indent=2, ensure_ascii=True)}\n```\n"


def stage_allowlist(plan: dict[str, Any]) -> dict[str, Any]:
    paths = [
        "scripts/trinity_v76_candidate_systems.py",
        "scripts/trinity_v76_v84_omega.py",
        "scripts/trinity_expansion_manifest_validator.py",
        "scripts/trinity_expansion_system_runner.py",
        "docs/trinity-expansion-system-manifest-v17.json",
        f"docs/trinity-live-traces/{PREFIX}-runtime-health-gate-v1.json",
        f"docs/trinity-live-traces/{PREFIX}-runtime-health-gate-v1.md",
        f"docs/trinity-live-traces/{PREFIX}-provider-readiness-probe-v1.json",
        f"docs/trinity-live-traces/{PREFIX}-provider-readiness-probe-v1.md",
        f"docs/trinity-live-traces/{PREFIX}-phase-plan-v1.json",
        f"docs/trinity-live-traces/{PREFIX}-phase-plan-v1.md",
        f"docs/trinity-live-traces/{PREFIX}-eureka-ledger-v1.json",
        f"docs/trinity-live-traces/{PREFIX}-eureka-ledger-v1.md",
        f"docs/trinity-live-traces/{PREFIX}-system-expansion-candidate-pack-v1.json",
        f"docs/trinity-live-traces/{PREFIX}-system-expansion-candidate-pack-v1.md",
        f"docs/trinity-live-traces/{PREFIX}-stage-allowlist-v1.json",
        f"docs/trinity-live-traces/{PREFIX}-stage-allowlist-v1.md",
        f"docs/trinity-live-traces/{PREFIX}-git-publication-result-v1.json",
        f"docs/trinity-live-traces/{PREFIX}-git-publication-result-v1.md",
        f"docs/trinity-live-traces/{PREFIX}-cli-reports/v76-phase-ledger-v1.md",
        f"docs/trinity-live-traces/{PREFIX}-cli-reports/v76-eureka-plan-v1.md",
        f"docs/trinity-live-traces/{PREFIX}-cli-reports/v77-phase-plan-proposal-v1.md",
        "docs/v76-omega-closeout-summary-v1.json",
        "docs/v76-omega-handoff-policy-v1.json",
        "docs/v77-omega-handoff-policy-v1.json",
        "docs/trinity-live-traces/v76-deep-suite-status.json",
        "docs/trinity-live-traces/v76-materialize-l5-suite-status.json",
    ]
    for candidate in load_v74_candidates():
        system_id = str(candidate["id"])
        paths.extend(
            [
                f"docs/trinity-live-traces/v76-v84-candidate-system-results/{hyphen(system_id)}.json",
                f"docs/trinity-live-traces/v76-v84-candidate-system-results/{hyphen(system_id)}.md",
                f"docs/trinity-expansion/{hyphen(system_id)}-latest.json",
                f"docs/trinity-expansion/{hyphen(system_id)}-latest.md",
            ]
        )
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "policy": "stage_only_curated_v76_v84_truth_surfaces_candidate_outputs_and_suite_statuses",
        "paths": sorted(dict.fromkeys(paths)),
    }


def publication_result() -> dict[str, Any]:
    local = run(["git", "rev-parse", "HEAD"], timeout=20)
    remote = run(["git", "ls-remote", "origin", f"refs/heads/{PUBLICATION_BRANCH}"], timeout=60)
    remote_head = ""
    if remote.get("ok") and remote.get("stdout"):
        remote_head = str(remote["stdout"]).split()[0]
    local_head = str(local.get("stdout") or "")
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "publication_branch": PUBLICATION_BRANCH,
        "local_head_at_receipt_generation": local_head,
        "remote_head_verified": remote_head,
        "remote_matches_local": bool(local_head and remote_head and local_head == remote_head),
    }


def write_all() -> None:
    manifest_promotion = ensure_manifest_promotions()
    health = runtime_health_gate()
    providers = provider_probe()
    plan = phase_plan(manifest_promotion)
    eureka = eureka_ledger()
    expansion = system_expansion_pack(manifest_promotion)
    allow = stage_allowlist(plan)
    publication = publication_result()
    v76_deep = suite_status("v76-deep")
    v76_l5 = suite_status("v76-materialize-l5")
    v76_green = bool(v76_deep["effective_success"] and v76_l5["effective_success"])
    closeout = {
        "generated_utc": now_iso(),
        "phase": "v76_omega",
        "state": "completed_green" if v76_green else "initialized_pending_deep_and_l5",
        "v75_anchor": plan["anchor"],
        "v76_deep": v76_deep,
        "v76_materialize_l5": v76_l5,
        "manifest_promotion": manifest_promotion,
        "next_required_action": "prepare_v77_from_v76_green_results" if v76_green else "run_v76_deep_then_v76_materialize_l5",
    }
    handoff = {
        "generated_utc": now_iso(),
        "phase": "v76_to_v77_handoff",
        "policy": "v77 plan becomes authoritative only after v76 L5 green",
        "carry_forward": [
            "20 v74 candidates are now runner-backed.",
            "20 v76 candidates are seeded but not suite-counted.",
            "v78-v84 remain guarded live-write phases only.",
        ],
    }
    v77_handoff = {
        "generated_utc": now_iso(),
        "phase": "v77_omega",
        "state": "proposal_ready" if v76_green else "blocked_until_v76_green",
        "entry_requirements": {
            "v76_deep_green": v76_deep["effective_success"],
            "v76_l5_green": v76_l5["effective_success"],
            "bounded_live_write_policy": "no external provider writes for v77",
        },
        "candidate_seed_count": len(expansion["next_candidate_seed_pack"]),
        "recommended_first_promotions": [item["id"] for item in expansion["next_candidate_seed_pack"][:6]],
    }
    artifacts = {
        f"{PREFIX}-runtime-health-gate-v1": health,
        f"{PREFIX}-provider-readiness-probe-v1": providers,
        f"{PREFIX}-phase-plan-v1": plan,
        f"{PREFIX}-eureka-ledger-v1": eureka,
        f"{PREFIX}-system-expansion-candidate-pack-v1": expansion,
        f"{PREFIX}-stage-allowlist-v1": allow,
        f"{PREFIX}-git-publication-result-v1": publication,
    }
    for stem, payload in artifacts.items():
        write_json(TRACE / f"{stem}.json", payload)
        write_text(TRACE / f"{stem}.md", report_markdown(stem, payload))
    write_text(REPORT_DIR / "v76-phase-ledger-v1.md", phase_ledger(health, plan, manifest_promotion))
    write_text(REPORT_DIR / "v76-eureka-plan-v1.md", report_markdown("V76 Eureka Plan", eureka))
    write_text(REPORT_DIR / "v77-phase-plan-proposal-v1.md", v77_plan_markdown(plan, expansion))
    write_json(DOCS / "v76-omega-closeout-summary-v1.json", closeout)
    write_json(DOCS / "v76-omega-handoff-policy-v1.json", handoff)
    write_json(DOCS / "v77-omega-handoff-policy-v1.json", v77_handoff)


if __name__ == "__main__":
    write_all()
