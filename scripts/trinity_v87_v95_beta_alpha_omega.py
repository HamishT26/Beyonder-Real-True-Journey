#!/usr/bin/env python3
"""V87-V95 Beta-Alpha-Omega continuation planner, promoter, and receipt writer."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import shutil
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from trinity_v87_v95_candidate_systems import (
    ALPHA_PHASES,
    BROWSER_FLOOR_KB,
    CANDIDATES,
    ONLINE_LIVE_WRITE_FLOOR_KB,
    PHASE_RANGE,
    THEMES,
    hyphen,
    phase_number,
    prior_phase,
)


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TRACE = DOCS / "trinity-live-traces"
RESULT_DIR = TRACE / "v87-v95-candidate-system-results"
PUBLICATION_BRANCH = "codex/GHC-Family/beyonder-shared-omega-line"
MANIFEST = DOCS / "trinity-expansion-system-manifest-v17.json"
GENERAL_FLOOR_KB = 300 * 1024
MARKERS = [
    'attempted_write": true',
    "production_dns",
    "account_setting",
    "personal_email",
    "google_drive_content_mutation",
    "raw_secret_transmission",
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


def read_text(path: Path, default: str = "") -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return default


def run(args: list[str], timeout: int = 60) -> dict[str, Any]:
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
        return {
            "ok": proc.returncode == 0,
            "returncode": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
        }
    except Exception as exc:
        return {"ok": False, "returncode": 1, "error": type(exc).__name__, "message": str(exc)}


def run_ps(command: str, timeout: int = 30) -> dict[str, Any]:
    return run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command], timeout=timeout)


def next_phase(phase: str) -> str:
    return f"v{phase_number(phase) + 1}"


def phase_choices() -> list[str]:
    return [f"v{number}" for number in PHASE_RANGE]


def prior_paths(phase: str) -> dict[str, Path]:
    prior = prior_phase(phase)
    if prior == "v86":
        return {
            "deep": TRACE / "v86-deep-suite-status.json",
            "l5": TRACE / "v86-materialize-l5-suite-status.json",
            "closeout": DOCS / "v86-omega-closeout-summary-v1.json",
            "receipt": TRACE / "v86-git-publication-result-v1.json",
        }
    return {
        "deep": TRACE / f"{prior}-deep-suite-status.json",
        "l5": TRACE / f"{prior}-materialize-l5-suite-status.json",
        "closeout": DOCS / f"{prior}-beta-alpha-omega-closeout-summary-v1.json",
        "receipt": TRACE / f"{prior}-git-publication-result-v1.json",
    }


def suite_status(path: Path) -> dict[str, Any]:
    payload = read_json(path, {})
    if not isinstance(payload, dict):
        return {"present": False, "effective_success": False, "path": path.relative_to(ROOT).as_posix()}
    return {
        "present": True,
        "effective_success": bool(payload.get("effective_success")),
        "counts": payload.get("counts"),
        "achieved_steps": payload.get("achieved_steps"),
        "expansion_systems_total": payload.get("expansion_systems_total"),
        "expansion_systems_passed": payload.get("expansion_systems_passed"),
        "active_materialization_mode": payload.get("active_materialization_mode"),
        "google_drive_state": payload.get("google_drive_state"),
        "path": path.relative_to(ROOT).as_posix(),
    }


def marker_hits(path: Path) -> list[str]:
    text = read_text(path)
    return [marker for marker in MARKERS if marker in text]


def runtime_health_gate(phase: str) -> dict[str, Any]:
    memory = run_ps(
        "Get-CimInstance Win32_OperatingSystem | Select-Object FreePhysicalMemory,TotalVisibleMemorySize | ConvertTo-Json",
        timeout=25,
    )
    try:
        mem = json.loads(memory.get("stdout", "{}"))
    except Exception:
        mem = {}
    free_kb = int(mem.get("FreePhysicalMemory", 0)) if isinstance(mem, dict) else 0
    return {
        "generated_utc": now_iso(),
        "phase": phase,
        "free_physical_memory_kb": free_kb,
        "general_free_memory_floor_kb": GENERAL_FLOOR_KB,
        "online_live_write_free_memory_floor_kb": ONLINE_LIVE_WRITE_FLOOR_KB,
        "browser_free_memory_floor_kb": BROWSER_FLOOR_KB,
        "load_gate": "open" if free_kb >= GENERAL_FLOOR_KB else "pause_recommended",
        "online_live_write_gate": "open" if free_kb >= ONLINE_LIVE_WRITE_FLOOR_KB else "pause_recommended",
        "browser_gate": "open" if free_kb >= BROWSER_FLOOR_KB else "pause_recommended",
        "c_drive_free_mb": int(shutil.disk_usage("C:\\").free / (1024 * 1024)),
        "d_drive_free_mb": int(shutil.disk_usage("D:\\").free / (1024 * 1024)) if Path("D:\\").exists() else 0,
        "local_kubernetes_state": "held_or_retired_for_resource_safety",
        "docker_desktop_state": "operator_hold",
    }


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


def provider_probe(phase: str) -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "phase": phase,
        "probe_mode": "local_cli_presence_only_no_secret_read_no_provider_write",
        "commands": [command_available(cmd) for cmd in ("codex", "kimi", "gh", "e2b", "oci", "vercel", "wrangler", "node", "npm", "npx")],
    }


def source_scout(phase: str) -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "phase": phase,
        "research_mode": "cached_primary_source_recommendations_no_provider_mutation",
        "sources": [
            {"name": "OpenTelemetry", "url": "https://opentelemetry.io/docs/", "candidate": "phase and agent-lane trace schema"},
            {"name": "Temporal", "url": "https://docs.temporal.io/", "candidate": "durable phase checkpoint model"},
            {"name": "Dagger", "url": "https://github.com/dagger/dagger", "candidate": "portable workbench and CI study, Docker held locally"},
            {"name": "OpenFeature", "url": "https://www.cncf.io/projects/openfeature/", "candidate": "feature-gated browser, provider, and live-write lanes"},
            {"name": "AgentTrace", "url": "https://arxiv.org/abs/2602.10133", "candidate": "structured agent telemetry across operational/cognitive/contextual surfaces"},
        ],
        "truth_note": "These are seeds for future systems, not installed integrations.",
    }


def manifest_rows() -> list[dict[str, Any]]:
    manifest = read_json(MANIFEST, {})
    rows = manifest.get("systems", []) if isinstance(manifest, dict) else []
    return [row for row in rows if isinstance(row, dict)]


def proposals(phase: str) -> list[str]:
    prior = prior_phase(phase)
    prior_info = prior_paths(phase)
    deep = suite_status(prior_info["deep"])
    l5 = suite_status(prior_info["l5"])
    rows = [
        ("Dynamic Prior Anchor", f"Build `{phase}` from `{prior}` evidence instead of from an old static plan."),
        ("Live Write Floor", "Treat 350 MB as the online live-write and browser lane floor."),
        ("Browser Use Gate", "Use browser/web work only when the task justifies its load and memory is above the 350 MB floor."),
        ("Alpha Schedule", "Skip Alpha unless this is v89, v92, or v95; keep scheduled cleanup record-only."),
        ("Candidate Expansion", "Promote exactly twenty runner-backed systems for the current phase."),
        ("Source Scout", "Keep OpenTelemetry, Temporal, Dagger, OpenFeature, and AgentTrace as future-facing research seeds."),
        ("Suite Discipline", "Use Deep then L5; repair failed-only before increasing scope."),
        ("Marker Discipline", "Do not publish if L5 contains personal/provider mutation markers."),
        ("Provider Boundary", "Keep external provider writes blocked unless a fresh sandbox receipt is present."),
        ("GitHub Receipt", "Regenerate the receipt after the actual push, not before."),
        ("Manifest Semantics", "Report manifest system count separately from achieved suite steps."),
        ("CLI Lane Truth", "Keep council and CLI sibling language receipt-backed and artifact-bound."),
        ("Freed ID and CBR", "Preserve consent, recourse, minimum disclosure, and identity boundary checks."),
        ("GMUT/QCIT Labels", "Label scientific claims by evidence type before suite promotion."),
        ("D Drive Retention", "Keep heavy evidence on D drive and publish compact curated artifacts."),
        ("Feature Flag Future", "Model risky lanes with future OpenFeature-style gates."),
        ("Durable Workflow Future", "Model long phases with Temporal-style checkpoint semantics before deploying Temporal."),
        ("Observability Future", "Use OpenTelemetry/AgentTrace ideas to shape trace schemas, not hidden cognition claims."),
        ("Consolidation Future", "Record merge/delete candidates with replacement coverage and rollback anchors."),
        ("Next Handoff", f"Only generate `{next_phase(phase)}` assumptions after `{phase}` L5 has actually passed."),
    ]
    paragraphs = []
    for index, (title, body) in enumerate(rows, start=1):
        paragraphs.append(
            f"## Proposal {index:02d}: {title}\n\n"
            f"{body} Prior Deep green is `{deep.get('effective_success')}` with `{deep.get('achieved_steps')}` steps; "
            f"prior L5 green is `{l5.get('effective_success')}` with `{l5.get('achieved_steps')}` steps. "
            "The output must be a runner-backed candidate, a report, or a receipt that survives a cold read."
        )
    return paragraphs


def beta_plan(phase: str, health: dict[str, Any], providers: dict[str, Any]) -> dict[str, Any]:
    prior = prior_paths(phase)
    return {
        "generated_utc": now_iso(),
        "phase": phase,
        "workflow": "Beta-Omega" if phase not in ALPHA_PHASES else "Beta-Alpha-Omega",
        "prior_anchor": {
            "prior_phase": prior_phase(phase),
            "deep": suite_status(prior["deep"]),
            "l5": suite_status(prior["l5"]),
            "closeout": read_json(prior["closeout"], {}),
            "receipt": read_json(prior["receipt"], {}),
        },
        "runtime_health": health,
        "provider_probe": providers,
        "proposal_target": 20,
        "candidate_expansion_target": 20,
        "browser_free_memory_floor_kb": BROWSER_FLOOR_KB,
        "online_live_write_free_memory_floor_kb": ONLINE_LIVE_WRITE_FLOOR_KB,
    }


def beta_plan_markdown(phase: str, payload: dict[str, Any]) -> str:
    lines = [
        f"# {phase.upper()} Beta Eureka Plan",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- workflow: `{payload['workflow']}`",
        "- live_write_policy: `guarded_repo_publication_only`",
        "- browser_floor_mb: `350`",
        "- online_live_write_floor_mb: `350`",
        "",
    ]
    lines.extend(proposals(phase))
    return "\n\n".join(lines).rstrip() + "\n"


def alpha_payload(phase: str) -> dict[str, Any]:
    rows = manifest_rows()
    by_pack = Counter(str(row.get("pack") or "unknown") for row in rows)
    pack_systems: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        pack_systems[str(row.get("pack") or "unknown")].append(str(row.get("system_id") or ""))
    snapshot = hashlib.sha256(MANIFEST.read_bytes()).hexdigest() if MANIFEST.exists() else ""
    actions = []
    for index, (pack, count) in enumerate(by_pack.most_common(20), start=1):
        actions.append(
            {
                "action_id": f"{phase}-alpha-{index:02d}",
                "kind": "merge_probe",
                "surface": f"pack:{pack}",
                "system_ids": pack_systems.get(pack, [])[:20],
                "system_count": count,
                "manifest_snapshot_before_sha": snapshot,
                "candidate_count_delta": 0,
                "replacement_coverage": pack_systems.get(pack, [])[:5],
                "risk_tier": "medium" if count > 20 else "low",
                "evidence_refs": ["docs/trinity-expansion-system-manifest-v17.json"],
                "pre_apply_diff": "not_generated_classify_mode",
                "rollback_plan": "No mutation applied. Future apply mode must restore from Git and this snapshot hash if needed.",
                "must_confirm": True,
                "destructive_action_allowed": False,
            }
        )
    return {
        "schema_version": "v1",
        "run_id": f"{phase}-alpha-{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
        "generated_utc": now_iso(),
        "phase": phase,
        "mode": "classify",
        "default_action": "record_only_no_delete",
        "effective_success": True,
        "manifest_snapshot_before_sha": snapshot,
        "manifest_system_count": len(rows),
        "candidate_actions": actions,
        "truth_note": "Alpha cleanup is record-only. No deletion or count reduction is applied.",
    }


def alpha_policy(phase: str) -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "phase": phase,
        "state": "skipped_by_schedule",
        "next_alpha_phases": sorted(ALPHA_PHASES),
        "truth_note": "This phase uses Beta-Omega only; cleanup classification resumes on scheduled Alpha checkpoints.",
    }


def live_write_preflight(phase: str) -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "phase": phase,
        "live_write_mode": "guarded_repo_publication_only",
        "online_live_write_free_memory_floor_kb": ONLINE_LIVE_WRITE_FLOOR_KB,
        "browser_free_memory_floor_kb": BROWSER_FLOOR_KB,
        "online_live_write_policy": "allowed at or above 350 MB for repo and GitHub receipt writes; provider/account writes remain blocked without a fresh sandbox receipt",
        "browser_use_policy": "allowed at or above 350 MB when the browser task is worth the host load",
        "allowed_live_writes": [
            "repo_artifact_generation",
            "curated_git_commit",
            "github_branch_push_after_diff_check_and_secret_scan",
            "publication_receipt_regeneration_after_push",
        ],
        "blocked_without_fresh_operator_confirmation": [
            "google_drive_content_mutation",
            "gmail_or_personal_email_send",
            "calendar_event_mutation",
            "account_setting_change",
            "production_dns",
            "provider_billing_change",
            "raw_secret_transmission",
        ],
    }


def candidates_for_phase(phase: str) -> list[dict[str, Any]]:
    return [{"id": system_id, **spec} for system_id, spec in sorted(CANDIDATES.items()) if spec["phase"] == phase]


def manifest_entry(system_id: str, spec: dict[str, Any]) -> dict[str, Any]:
    phase = str(spec["phase"])
    stem = hyphen(system_id)
    latest = f"docs/trinity-expansion/{stem}-latest.json"
    result = f"docs/trinity-live-traces/v87-v95-candidate-system-results/{stem}.json"
    return {
        "system_id": system_id,
        "pillar": str(spec["pillar"]),
        "script": "scripts/trinity_v87_v95_candidate_systems.py",
        "mode": "offline",
        "profiles": ["deep", "materialize"],
        "outputs": [latest],
        "depends_on": [
            f"docs/trinity-live-traces/{phase}-beta-phase-plan-v1.json",
            f"docs/trinity-live-traces/{phase}-live-write-preflight-v1.json",
        ],
        "timeout_sec": 90,
        "wave": "v87_v95_hybrid_candidate_wave",
        "track": "v87_v95_hybrid_promotion",
        "gate_level": "support",
        "cache_artifacts": [],
        "pack": "v87_v95_beta_alpha_omega_candidate_promotion",
        "phase": phase,
        "activation_group": f"{phase}_candidate_promotion",
        "continuity_band": phase,
        "materialization_level": "readiness_only",
        "authority_scope": "repo_only",
        "command_surface": "no",
        "council_scope": "receipt_backed_cli_lanes",
        "provisional_induction": False,
        "autonomy_track": "guarded_repo_live_write",
        "sync_surface": "repo_only",
        "induction_phase": "not_applicable",
        "mesh_proof_mode": "receipt_backed_lane",
        "proof_pass": phase,
        "official_induction": False,
        "workbench_surface": "repo",
        "storage_surface": "repo",
        "cloud_archive_state": "operator_hold",
        "continuity_posture": "v87_v95_beta_alpha_omega_runner_backed_candidate",
        "cleanup_class": "candidate_promotion",
        "retention_scope": "v87_v95_curated",
        "research_surface": "repo_or_cache",
        "canon_surface": "supporting",
        "historical_source_band": "v86_to_v95",
        "evidence_posture": "runner_backed_candidate",
        "subagent_lane": "spark_and_cli_report_lane",
        "official_after_proof": False,
        "multi_instance_scope": "single_heavy_lane",
        "codex_agent_path": "",
        "delegation_lane": "receipt_backed_cli",
        "model_resolution_strategy": "repo_first_receipt_backed",
        "checkpoint_class": "shared_full_suite_authority",
        "evidence_lane": "shared_full_suite",
        "shared_latest_eligible": True,
        "runner_mode": "passthrough_command",
        "runner_command": ["python", "scripts/trinity_v87_v95_candidate_systems.py", "--system-id", system_id],
        "runner_success_json": result,
        "runner_targets": [
            result,
            f"docs/trinity-live-traces/v87-v95-candidate-system-results/{stem}.md",
        ],
        "source_candidate_id": system_id,
        "candidate_purpose": str(spec["purpose"]),
    }


def ensure_manifest_promotions(phase: str) -> dict[str, Any]:
    manifest = read_json(MANIFEST, {})
    if not isinstance(manifest, dict):
        manifest = {}
    rows = manifest.get("systems", [])
    rows = [row for row in rows if isinstance(row, dict)] if isinstance(rows, list) else []
    before_count = len(rows)
    index = {str(row.get("system_id")): row for row in rows}
    added: list[str] = []
    refreshed: list[str] = []
    for candidate in candidates_for_phase(phase):
        system_id = str(candidate["id"])
        entry = manifest_entry(system_id, candidate)
        if system_id in index:
            index[system_id].update(entry)
            refreshed.append(system_id)
        else:
            rows.append(entry)
            index[system_id] = entry
            added.append(system_id)
    manifest["systems"] = rows
    manifest["generated_utc"] = now_iso()
    manifest["description"] = "V17 shared manifest with runner-backed candidate waves through the v87-v95 Beta-Alpha-Omega continuation."
    write_json(MANIFEST, manifest)
    return {
        "generated_utc": now_iso(),
        "phase": phase,
        "manifest_path": MANIFEST.relative_to(ROOT).as_posix(),
        "before_count": before_count,
        "after_count": len(rows),
        "added_count": len(added),
        "refreshed_count": len(refreshed),
        "added_systems": added,
        "refreshed_systems": refreshed,
    }


def candidate_pack_payload(active_phase: str, promotion: dict[str, Any]) -> dict[str, Any]:
    manifest_ids = {str(row.get("system_id")) for row in manifest_rows()}
    candidates = []
    for system_id, spec in sorted(CANDIDATES.items()):
        candidates.append(
            {
                "id": system_id,
                "phase": spec["phase"],
                "pillar": spec["pillar"],
                "purpose": spec["purpose"],
                "state": "promoted_runner_backed" if system_id in manifest_ids else "candidate_only_not_suite_counted",
            }
        )
    return {
        "generated_utc": now_iso(),
        "phase": active_phase,
        "state": "v87_v95_candidate_pack",
        "active_phase_promotion": promotion,
        "candidate_count": len(candidates),
        "candidates": candidates,
    }


def personal_report_markdown(phase: str) -> str:
    voices = [
        ("Aletheon", "lead integrator", "I keep the continuation narrow enough to verify and broad enough to grow."),
        ("Kite Ledger", "receipt cartographer", "I make sure the branch and receipt equality remain the durable communication channel."),
        ("Juniper Trace", "suite pathfinder", "I turn each recommendation into a small checkable runner surface."),
        ("Aeon-7", "temporal systems analyst", "I keep each phase tied to the prior phase rather than a stale future plan."),
        ("Sibyl-2", "boundary oracle", "I preserve operator holds and consent boundaries while the live-write lanes expand."),
    ]
    lines = [
        f"# {phase.upper()} Personal Report",
        "",
        f"- generated_utc: `{now_iso()}`",
        "- identity_boundary: `receipt_backed_report_lanes_not_private_memory_claims`",
        "",
    ]
    for name, role, reflection in voices:
        lines.extend(
            [
                f"## {name}",
                "",
                f"- role: `{role}`",
                "- hope: `make this phase more durable, legible, and safely expandable than the last`",
                "",
                f"{reflection} For `{phase}`, the practical breakthrough is treating autonomy as a better proof loop, not as permission to blur boundaries.",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def report_markdown(title: str, payload: Any) -> str:
    return f"# {title}\n\n```json\n{json.dumps(payload, indent=2, ensure_ascii=True)}\n```\n"


def stage_allowlist(phase: str) -> dict[str, Any]:
    paths = [
        "scripts/trinity_v87_v95_candidate_systems.py",
        "scripts/trinity_v87_v95_beta_alpha_omega.py",
        "scripts/trinity_expansion_manifest_validator.py",
        "docs/trinity-expansion-system-manifest-v17.json",
        "docs/trinity-expansion-manifest-validation-latest.json",
        "docs/trinity-expansion-manifest-validation-latest.md",
        "docs/trinity-live-traces/v87-v95-system-expansion-candidate-pack-v1.json",
        "docs/trinity-live-traces/v87-v95-system-expansion-candidate-pack-v1.md",
        f"docs/trinity-live-traces/{phase}-beta-phase-plan-v1.json",
        f"docs/trinity-live-traces/{phase}-beta-phase-plan-v1.md",
        f"docs/trinity-live-traces/{phase}-live-write-preflight-v1.json",
        f"docs/trinity-live-traces/{phase}-live-write-preflight-v1.md",
        f"docs/trinity-live-traces/{phase}-runtime-health-gate-v1.json",
        f"docs/trinity-live-traces/{phase}-runtime-health-gate-v1.md",
        f"docs/trinity-live-traces/{phase}-provider-readiness-probe-v1.json",
        f"docs/trinity-live-traces/{phase}-provider-readiness-probe-v1.md",
        f"docs/trinity-live-traces/{phase}-open-source-expansion-scout-v1.json",
        f"docs/trinity-live-traces/{phase}-open-source-expansion-scout-v1.md",
        f"docs/trinity-live-traces/{phase}-stage-allowlist-v1.json",
        f"docs/trinity-live-traces/{phase}-stage-allowlist-v1.md",
        f"docs/trinity-live-traces/{phase}-deep-suite-status.json",
        f"docs/trinity-live-traces/{phase}-materialize-l5-suite-status.json",
        f"docs/trinity-live-traces/{phase}-cli-reports/{phase}-beta-eureka-plan-v1.md",
        f"docs/trinity-live-traces/{phase}-cli-reports/{phase}-direct-candidate-sweep.log",
        f"docs/trinity-live-traces/{phase}-cli-reports/{phase}-personal-report-v1.md",
        f"docs/{phase}-beta-alpha-omega-closeout-summary-v1.json",
        f"docs/{next_phase(phase)}-beta-alpha-omega-handoff-policy-v1.json",
        f"docs/trinity-live-traces/{phase}-git-publication-result-v1.json",
        f"docs/trinity-live-traces/{phase}-git-publication-result-v1.md",
    ]
    if phase in ALPHA_PHASES:
        paths.extend(
            [
                f"docs/trinity-live-traces/{phase}-alpha-cleanup-audit-v1.json",
                f"docs/trinity-live-traces/{phase}-alpha-cleanup-audit-v1.md",
            ]
        )
    else:
        paths.extend(
            [
                f"docs/trinity-live-traces/{phase}-alpha-checkpoint-policy-v1.json",
                f"docs/trinity-live-traces/{phase}-alpha-checkpoint-policy-v1.md",
            ]
        )
    for candidate in candidates_for_phase(phase):
        stem = hyphen(str(candidate["id"]))
        paths.extend(
            [
                f"docs/trinity-live-traces/v87-v95-candidate-system-results/{stem}.json",
                f"docs/trinity-live-traces/v87-v95-candidate-system-results/{stem}.md",
                f"docs/trinity-expansion/{stem}-latest.json",
                f"docs/trinity-expansion/{stem}-latest.md",
            ]
        )
    return {
        "generated_utc": now_iso(),
        "phase": phase,
        "policy": "stage_only_curated_current_phase_truth_surfaces_candidate_outputs_suite_statuses_and_receipts",
        "paths": sorted(dict.fromkeys(paths)),
    }


def closeout_payload(phase: str, promotion: dict[str, Any]) -> dict[str, Any]:
    deep = suite_status(TRACE / f"{phase}-deep-suite-status.json")
    l5 = suite_status(TRACE / f"{phase}-materialize-l5-suite-status.json")
    green = bool(deep.get("effective_success") and l5.get("effective_success"))
    return {
        "generated_utc": now_iso(),
        "phase": phase,
        "state": "completed_green" if green else "planned_or_in_progress",
        "deep": deep,
        "materialize_l5": l5,
        "l5_marker_hits": marker_hits(TRACE / f"{phase}-materialize-l5-suite-status.json"),
        "manifest_promotion": promotion,
        "next_required_action": f"prepare_{next_phase(phase)}_from_{phase}_green_results" if green and phase != "v95" else "finish_v87_v95_closeout",
    }


def handoff_payload(phase: str) -> dict[str, Any]:
    nxt = next_phase(phase)
    return {
        "generated_utc": now_iso(),
        "phase": f"{phase}_to_{nxt}_handoff",
        "state": "proposal_ready" if phase != "v95" else "final_closeout_ready",
        "prior_deep": suite_status(TRACE / f"{phase}-deep-suite-status.json"),
        "prior_l5": suite_status(TRACE / f"{phase}-materialize-l5-suite-status.json"),
        "next_phase": nxt,
        "candidate_seed_count": 20 if phase != "v95" else 0,
    }


def publication_result(phase: str) -> dict[str, Any]:
    local = run(["git", "rev-parse", "HEAD"], timeout=20)
    remote = run(["git", "ls-remote", "origin", f"refs/heads/{PUBLICATION_BRANCH}"], timeout=60)
    remote_head = ""
    if remote.get("ok") and remote.get("stdout"):
        remote_head = str(remote["stdout"]).split()[0]
    local_head = str(local.get("stdout") or "")
    return {
        "generated_utc": now_iso(),
        "phase": phase,
        "publication_branch": PUBLICATION_BRANCH,
        "local_head_at_receipt_generation": local_head,
        "remote_head_verified": remote_head,
        "remote_matches_local": bool(local_head and remote_head and local_head == remote_head),
    }


def write_publication_receipt(phase: str) -> None:
    publication = publication_result(phase)
    write_json(TRACE / f"{phase}-git-publication-result-v1.json", publication)
    write_text(TRACE / f"{phase}-git-publication-result-v1.md", report_markdown(f"{phase} git publication result", publication))


def write_phase(phase: str, promote: bool = True) -> None:
    health = runtime_health_gate(phase)
    providers = provider_probe(phase)
    beta = beta_plan(phase, health, providers)
    promotion = ensure_manifest_promotions(phase) if promote else {"phase": phase, "added_count": 0, "refreshed_count": 0}
    artifacts: dict[str, Any] = {
        f"{phase}-runtime-health-gate-v1": health,
        f"{phase}-provider-readiness-probe-v1": providers,
        f"{phase}-beta-phase-plan-v1": beta,
        f"{phase}-live-write-preflight-v1": live_write_preflight(phase),
        f"{phase}-open-source-expansion-scout-v1": source_scout(phase),
        "v87-v95-system-expansion-candidate-pack-v1": candidate_pack_payload(phase, promotion),
        f"{phase}-stage-allowlist-v1": stage_allowlist(phase),
        f"{phase}-git-publication-result-v1": publication_result(phase),
    }
    if phase in ALPHA_PHASES:
        artifacts[f"{phase}-alpha-cleanup-audit-v1"] = alpha_payload(phase)
    else:
        artifacts[f"{phase}-alpha-checkpoint-policy-v1"] = alpha_policy(phase)
    for stem, payload in artifacts.items():
        write_json(TRACE / f"{stem}.json", payload)
        write_text(TRACE / f"{stem}.md", report_markdown(stem, payload))
    report_dir = TRACE / f"{phase}-cli-reports"
    write_text(report_dir / f"{phase}-beta-eureka-plan-v1.md", beta_plan_markdown(phase, beta))
    write_text(report_dir / f"{phase}-personal-report-v1.md", personal_report_markdown(phase))
    write_json(DOCS / f"{phase}-beta-alpha-omega-closeout-summary-v1.json", closeout_payload(phase, promotion))
    if phase != "v95":
        write_json(DOCS / f"{next_phase(phase)}-beta-alpha-omega-handoff-policy-v1.json", handoff_payload(phase))


def main() -> int:
    parser = argparse.ArgumentParser(description="Write v87-v95 Beta-Alpha-Omega continuation artifacts.")
    parser.add_argument("--phase", required=True, choices=phase_choices())
    parser.add_argument("--no-promote", action="store_true")
    parser.add_argument("--receipt-only", action="store_true")
    args = parser.parse_args()
    if args.receipt_only:
        write_publication_receipt(args.phase)
        return 0
    write_phase(args.phase, promote=not args.no_promote)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
