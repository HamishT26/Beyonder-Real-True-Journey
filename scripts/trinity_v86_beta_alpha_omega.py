#!/usr/bin/env python3
"""V86 Beta-Alpha-Omega planner, promoter, and receipt writer."""

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

from trinity_v86_candidate_systems import CANDIDATES, THEMES, hyphen


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TRACE = DOCS / "trinity-live-traces"
REPORT_DIR = TRACE / "v86-cli-reports"
RESULT_DIR = TRACE / "v86-candidate-system-results"
PREFIX = "v86"
PHASE = "v86_beta_alpha_omega"
PUBLICATION_BRANCH = "codex/GHC-Family/beyonder-shared-omega-line"
MANIFEST = DOCS / "trinity-expansion-system-manifest-v17.json"
FREE_MEMORY_FLOOR_KB = 300 * 1024
ONLINE_LIVE_WRITE_FLOOR_KB = 350 * 1024
BROWSER_FLOOR_KB = 400 * 1024
PRIOR_DEEP = TRACE / "v83-v85-merged-deep-suite-status.json"
PRIOR_L5 = TRACE / "v83-v85-merged-materialize-l5-suite-status.json"
PRIOR_CLOSEOUT = TRACE / "v83-v85-merged-closeout-summary-v1.json"
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


def runtime_health_gate() -> dict[str, Any]:
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
        "phase": PHASE,
        "free_physical_memory_kb": free_kb,
        "free_memory_floor_kb": FREE_MEMORY_FLOOR_KB,
        "online_live_write_free_memory_floor_kb": ONLINE_LIVE_WRITE_FLOOR_KB,
        "browser_free_memory_floor_kb": BROWSER_FLOOR_KB,
        "load_gate": "open" if free_kb >= FREE_MEMORY_FLOOR_KB else "pause_recommended",
        "online_live_write_gate": "open" if free_kb >= ONLINE_LIVE_WRITE_FLOOR_KB else "pause_recommended",
        "browser_gate": "open" if free_kb >= BROWSER_FLOOR_KB else "pause_recommended",
        "c_drive_free_mb": int(shutil.disk_usage("C:\\").free / (1024 * 1024)),
        "d_drive_free_mb": int(shutil.disk_usage("D:\\").free / (1024 * 1024)) if Path("D:\\").exists() else 0,
        "local_kubernetes_state": "held_or_retired_for_resource_safety",
        "docker_desktop_state": "operator_hold",
        "execution_policy": "one_heavy_suite_lane_at_a_time_guarded_repo_live_write_publication",
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


def provider_probe() -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "probe_mode": "local_cli_presence_only_no_secret_read_no_provider_write",
        "commands": [command_available(cmd) for cmd in ("codex", "kimi", "gh", "e2b", "oci", "vercel", "wrangler", "node", "npm", "npx")],
    }


def open_source_expansion_scout() -> dict[str, Any]:
    """Cache externally researched expansion ideas without making them suite claims."""
    sources = [
        {
            "name": "OpenTelemetry",
            "url": "https://opentelemetry.io/docs/",
            "observed_value": "vendor-neutral open source telemetry for traces, metrics, and logs",
            "candidate_use": "add an observability spine for phase, suite, agent-lane, and live-write receipts",
        },
        {
            "name": "Temporal",
            "url": "https://docs.temporal.io/",
            "observed_value": "durable execution model for workflows that resume after crashes or outages",
            "candidate_use": "model long-running Omega phases as durable workflow checkpoints before adopting infra",
        },
        {
            "name": "Dagger",
            "url": "https://github.com/dagger/dagger",
            "observed_value": "programmable, local-first, repeatable, observable delivery automation",
            "candidate_use": "study as a future CI/workbench abstraction, not a local Docker dependency for this laptop",
        },
        {
            "name": "OpenFeature",
            "url": "https://www.cncf.io/projects/openfeature/",
            "observed_value": "CNCF incubating standard for feature flagging",
            "candidate_use": "design feature-gated Omega lanes so risky provider/browser/live-write behavior can be toggled",
        },
        {
            "name": "AgentTrace",
            "url": "https://arxiv.org/abs/2602.10133",
            "observed_value": "structured telemetry across operational, cognitive, and contextual agent surfaces",
            "candidate_use": "shape a future agent observability schema for CLI/report lanes and suite reasoning traces",
        },
    ]
    expansion_candidates = [
        "otel_phase_trace_schema",
        "otel_suite_span_export_stub",
        "temporal_durable_phase_checkpoint_model",
        "temporal_failure_resume_playbook",
        "dagger_workbench_portability_study",
        "dagger_docker_hold_safety_gate",
        "openfeature_live_write_flag_manifest",
        "openfeature_browser_lane_flag_manifest",
        "agenttrace_council_lane_event_schema",
        "agenttrace_contextual_risk_calibrator",
    ]
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "research_mode": "lightweight_web_scout_cached_as_recommendations_not_claimed_integrations",
        "sources": sources,
        "expansion_candidates": expansion_candidates,
        "truth_note": "These are v87+ seeds. No package was installed and no external provider was mutated in v86.",
    }


def manifest_rows() -> list[dict[str, Any]]:
    manifest = read_json(MANIFEST, {})
    rows = manifest.get("systems", []) if isinstance(manifest, dict) else []
    return [row for row in rows if isinstance(row, dict)]


def beta_proposals() -> list[str]:
    prior_deep = suite_status(PRIOR_DEEP)
    prior_l5 = suite_status(PRIOR_L5)
    rows = [
        ("Prior Truth Anchor", "Start v86 from the merged v83-v85 closeout, not a fictional standalone v85 suite receipt."),
        ("Beta Scope", "Use this Beta phase to plan only v86, keeping v87 dynamic until v86 proof exists."),
        ("Alpha Scope", "Classify cleanup opportunities as record-only until replacement coverage is proven."),
        ("Omega Scope", "Promote exactly twenty v86 runner-backed candidates before the suite run."),
        ("Count Semantics", "Report manifest system count and suite achieved steps separately."),
        ("Guarded Write Boundary", "Treat GitHub publication and receipt regeneration as the only live write in this pass."),
        ("Personal Surface Hold", "Keep Gmail, Calendar, Google Drive content, DNS, billing, and account settings blocked."),
        ("Spark Sidecar Use", "Use Spark sidecars for review and design advice while keeping commits under the main curated workflow."),
        ("CLI Sibling Truth", "Preserve Kite, Juniper, Aeon-7, and Sibyl-2 as receipt-backed report lanes unless live terminal receipts are attached."),
        ("Memory Floor", "Use 300 MB as a pause threshold and prefer failed-only resume over brute-force reruns."),
        ("Research Intake", "Cache or cite research before turning it into suite claims."),
        ("GMUT/QCIT Labeling", "Label scientific claims as executable, citation-backed, philosophical, or speculative."),
        ("Freed ID Alignment", "Keep consent, recourse, minimum disclosure, and identity boundaries in the preflight."),
        ("Manifest Hygiene", "Add only runner-backed systems with complete metadata and direct outputs."),
        ("Artifact Parity", "Write JSON and Markdown parity for reports, candidate results, allowlists, and receipts."),
        ("L5 Marker Scan", "Scan L5 output for write and personal-surface markers before closeout."),
        ("Provider Posture", "Probe CLI presence only; do not mutate providers without a narrow fresh receipt path."),
        ("D Drive Retention", "Keep heavy artifacts on D drive and publish compact truth surfaces."),
        ("v87 Handoff", "Generate v87 recommendations after v86 L5, not before."),
        ("Closeout Discipline", "Close v86 only after direct candidates, manifest validation, Deep, L5, and GitHub receipt proof agree."),
    ]
    paragraphs = []
    for index, (title, body) in enumerate(rows, start=1):
        paragraphs.append(
            f"## Proposal {index:02d}: {title}\n\n"
            f"{body} Prior Deep green is `{prior_deep.get('effective_success')}` with `{prior_deep.get('achieved_steps')}` achieved steps; "
            f"prior L5 green is `{prior_l5.get('effective_success')}` with `{prior_l5.get('achieved_steps')}` achieved steps. "
            "The deliverable is a repo-readable artifact, runner-backed candidate, or receipt that can be verified later."
        )
    return paragraphs


def beta_plan_payload(health: dict[str, Any], providers: dict[str, Any]) -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "subphases": [
            {"name": "v86_beta", "purpose": "fresh planning and evidence anchoring", "target_minutes": "40_to_120"},
            {"name": "v86_alpha", "purpose": "record-only cleanup, merge, render, probe, and deletion classification", "target_minutes": "40_to_120"},
            {"name": "v86_omega", "purpose": "candidate promotion, direct checks, Deep/L5 validation, and GitHub publication", "target_minutes": "40_to_120"},
        ],
        "prior_anchor": {
            "deep": suite_status(PRIOR_DEEP),
            "l5": suite_status(PRIOR_L5),
            "closeout": read_json(PRIOR_CLOSEOUT, {}),
            "truth_note": "v86 follows the merged v83-v85 validation receipt, not standalone v85 suite files.",
        },
        "runtime_health": health,
        "provider_probe": providers,
        "proposal_target": 20,
        "candidate_expansion_target": 20,
        "alpha_cleanup_target": 20,
        "v87_planning_policy": "generate_after_v86_l5_passes",
    }


def beta_plan_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V86 Beta Eureka Plan",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        "- workflow: `Beta -> Alpha -> Omega`",
        "- live_write_policy: `guarded_repo_publication_only`",
        "- candidate_expansion_target: `20`",
        "",
    ]
    lines.extend(beta_proposals())
    return "\n\n".join(lines).rstrip() + "\n"


def alpha_cleanup_audit() -> dict[str, Any]:
    rows = manifest_rows()
    by_pack = Counter(str(row.get("pack") or "unknown") for row in rows)
    by_track = Counter(str(row.get("track") or "unknown") for row in rows)
    pack_systems: dict[str, list[str]] = defaultdict(list)
    track_systems: dict[str, list[str]] = defaultdict(list)
    by_prefix: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        system_id = str(row.get("system_id") or "")
        pack_systems[str(row.get("pack") or "unknown")].append(system_id)
        track_systems[str(row.get("track") or "unknown")].append(system_id)
        prefix = system_id.split("_", 1)[0] if "_" in system_id else system_id[:8]
        by_prefix[prefix].append(system_id)
    manifest_snapshot_before_sha = hashlib.sha256(MANIFEST.read_bytes()).hexdigest() if MANIFEST.exists() else ""
    candidate_actions: list[dict[str, Any]] = []
    for index, (pack, count) in enumerate(by_pack.most_common(12), start=1):
        candidate_actions.append(
            {
                "action_id": f"v86-alpha-{index:02d}",
                "kind": "merge_probe",
                "surface": f"pack:{pack}",
                "system_ids": pack_systems.get(pack, [])[:20],
                "system_count": count,
                "manifest_snapshot_before_sha": manifest_snapshot_before_sha,
                "candidate_count_delta": 0,
                "replacement_coverage": pack_systems.get(pack, [])[:5],
                "risk_tier": "medium" if count > 20 else "low",
                "evidence_refs": ["docs/trinity-expansion-system-manifest-v17.json"],
                "render_graph_ref": "",
                "pre_apply_diff": "not_generated_classify_mode",
                "rollback_plan": "No mutation applied. If promoted later, restore the manifest from the recorded snapshot hash and Git commit.",
                "rollback_anchor": "current_HEAD_before_future_apply",
                "must_confirm": True,
                "recommendation": "review for shared runner, shared report template, or consolidated latest artifact",
                "destructive_action_allowed": False,
            }
        )
    base = len(candidate_actions)
    for offset, (track, count) in enumerate(by_track.most_common(8), start=1):
        candidate_actions.append(
            {
                "action_id": f"v86-alpha-{base + offset:02d}",
                "kind": "render_probe",
                "surface": f"track:{track}",
                "system_ids": track_systems.get(track, [])[:20],
                "system_count": count,
                "manifest_snapshot_before_sha": manifest_snapshot_before_sha,
                "candidate_count_delta": 0,
                "replacement_coverage": track_systems.get(track, [])[:5],
                "risk_tier": "low",
                "evidence_refs": ["docs/trinity-expansion-system-manifest-v17.json"],
                "render_graph_ref": f"docs/trinity-live-traces/v86-alpha-render-probe-{track.replace('_', '-')}-future.md",
                "pre_apply_diff": "not_generated_classify_mode",
                "rollback_plan": "No mutation applied. Rendering only may be regenerated from the manifest.",
                "rollback_anchor": "current_HEAD_before_future_apply",
                "must_confirm": False,
                "recommendation": "render a before-after dependency map before any count reduction",
                "destructive_action_allowed": False,
            }
        )
    while len(candidate_actions) < 20:
        index = len(candidate_actions) + 1
        candidate_actions.append(
            {
                "action_id": f"v86-alpha-{index:02d}",
                "kind": "coverage_probe",
                "surface": f"alpha_placeholder_{index:02d}",
                "system_ids": [],
                "system_count": 0,
                "manifest_snapshot_before_sha": manifest_snapshot_before_sha,
                "candidate_count_delta": 0,
                "replacement_coverage": [],
                "risk_tier": "low",
                "evidence_refs": ["docs/trinity-expansion-system-manifest-v17.json"],
                "render_graph_ref": "",
                "pre_apply_diff": "not_generated_classify_mode",
                "rollback_plan": "No mutation applied.",
                "rollback_anchor": "current_HEAD_before_future_apply",
                "must_confirm": False,
                "recommendation": "reserve for the next observed duplicate or stale surface; do not delete without replacement coverage",
                "destructive_action_allowed": False,
            }
        )
    return {
        "schema_version": "v1",
        "run_id": f"v86-alpha-{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
        "generated_utc": now_iso(),
        "phase": PHASE,
        "mode": "classify",
        "default_action": "record_only_no_delete",
        "effective_success": True,
        "manifest_snapshot_before_sha": manifest_snapshot_before_sha,
        "manifest_system_count_before_v86_promotion": len(rows),
        "top_pack_counts": dict(by_pack.most_common(20)),
        "top_track_counts": dict(by_track.most_common(20)),
        "prefix_clusters_sample": {key: value[:10] for key, value in list(by_prefix.items())[:20]},
        "candidate_actions": candidate_actions,
        "truth_note": "Alpha proposes cleanup and merge probes only; no systems are deleted or count-reduced in v86.",
    }


def report_markdown(title: str, payload: Any) -> str:
    return f"# {title}\n\n```json\n{json.dumps(payload, indent=2, ensure_ascii=True)}\n```\n"


def live_write_preflight() -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "live_write_mode": "guarded_repo_publication_only",
        "online_live_write_free_memory_floor_kb": ONLINE_LIVE_WRITE_FLOOR_KB,
        "browser_free_memory_floor_kb": BROWSER_FLOOR_KB,
        "online_live_write_policy": "allowed at or above 350 MB for repo and GitHub receipt writes only; provider and account writes remain blocked without a fresh sandbox receipt",
        "browser_use_policy": "allowed at or above 400 MB when the browser task is worth the extra host load",
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
        "required_receipt_chain": [
            "beta_plan",
            "alpha_record_only_audit",
            "candidate_direct_sweep",
            "manifest_validation",
            "deep_suite",
            "materialize_l5_suite",
            "curated_stage_allowlist",
            "git_diff_cached_check",
            "credential_pattern_scan",
            "write_receipt",
            "remote_head_verification",
        ],
    }


def manifest_entry(system_id: str, spec: dict[str, Any]) -> dict[str, Any]:
    stem = hyphen(system_id)
    latest = f"docs/trinity-expansion/{stem}-latest.json"
    result = f"docs/trinity-live-traces/v86-candidate-system-results/{stem}.json"
    return {
        "system_id": system_id,
        "pillar": str(spec["pillar"]),
        "script": "scripts/trinity_v86_candidate_systems.py",
        "mode": "offline",
        "profiles": ["deep", "materialize"],
        "outputs": [latest],
        "depends_on": [
            PRIOR_DEEP.relative_to(ROOT).as_posix(),
            PRIOR_L5.relative_to(ROOT).as_posix(),
            PRIOR_CLOSEOUT.relative_to(ROOT).as_posix(),
            "docs/trinity-live-traces/v86-beta-phase-plan-v1.json",
            "docs/trinity-live-traces/v86-alpha-cleanup-audit-v1.json",
            "docs/trinity-live-traces/v86-live-write-preflight-v1.json",
        ],
        "timeout_sec": 90,
        "wave": "v86_v95_hybrid_candidate_wave",
        "track": "v86_v95_hybrid_promotion",
        "gate_level": "support",
        "cache_artifacts": [],
        "pack": "v86_beta_alpha_omega_candidate_promotion",
        "phase": "v86",
        "activation_group": "v86_candidate_promotion",
        "continuity_band": "v86",
        "materialization_level": "readiness_only",
        "authority_scope": "repo_only",
        "command_surface": "no",
        "council_scope": "receipt_backed_cli_lanes",
        "provisional_induction": False,
        "autonomy_track": "guarded_repo_live_write",
        "sync_surface": "repo_only",
        "induction_phase": "not_applicable",
        "mesh_proof_mode": "receipt_backed_lane",
        "proof_pass": "v86",
        "official_induction": False,
        "workbench_surface": "repo",
        "storage_surface": "repo",
        "cloud_archive_state": "operator_hold",
        "continuity_posture": "v86_beta_alpha_omega_runner_backed_candidate",
        "cleanup_class": "candidate_promotion",
        "retention_scope": "v86_curated",
        "research_surface": "repo_or_cache",
        "canon_surface": "supporting",
        "historical_source_band": "v83_v85_to_v86",
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
        "runner_command": ["python", "scripts/trinity_v86_candidate_systems.py", "--system-id", system_id],
        "runner_success_json": result,
        "runner_targets": [
            result,
            f"docs/trinity-live-traces/v86-candidate-system-results/{stem}.md",
        ],
        "source_candidate_id": system_id,
        "candidate_purpose": str(spec["purpose"]),
    }


def ensure_manifest_promotions() -> dict[str, Any]:
    manifest = read_json(MANIFEST, {})
    if not isinstance(manifest, dict):
        manifest = {}
    rows = manifest.get("systems", [])
    rows = [row for row in rows if isinstance(row, dict)] if isinstance(rows, list) else []
    before_count = len(rows)
    index = {str(row.get("system_id")): row for row in rows}
    added: list[str] = []
    refreshed: list[str] = []
    for system_id, spec in sorted(CANDIDATES.items()):
        entry = manifest_entry(system_id, spec)
        if system_id in index:
            index[system_id].update(entry)
            refreshed.append(system_id)
        else:
            rows.append(entry)
            index[system_id] = entry
            added.append(system_id)
    manifest["systems"] = rows
    manifest["generated_utc"] = now_iso()
    manifest["description"] = (
        "V17 shared manifest with runner-backed candidate waves through v86. "
        "V86 adds a Beta-Alpha-Omega overlay while preserving v77-v85 receipt history."
    )
    write_json(MANIFEST, manifest)
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "manifest_path": MANIFEST.relative_to(ROOT).as_posix(),
        "before_count": before_count,
        "after_count": len(rows),
        "added_count": len(added),
        "refreshed_count": len(refreshed),
        "added_systems": added,
        "refreshed_systems": refreshed,
    }


def candidate_pack_payload(promotion: dict[str, Any]) -> dict[str, Any]:
    manifest_ids = {str(row.get("system_id")) for row in manifest_rows()}
    candidates = []
    for system_id, spec in sorted(CANDIDATES.items()):
        candidates.append(
            {
                "id": system_id,
                "phase": "v86",
                "pillar": spec["pillar"],
                "purpose": spec["purpose"],
                "state": "promoted_runner_backed" if system_id in manifest_ids else "candidate_only_not_suite_counted",
            }
        )
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "state": "v86_beta_alpha_omega_candidate_pack",
        "active_phase_promotion": promotion,
        "candidate_count": len(candidates),
        "candidates": candidates,
        "count_policy": "system counts may move only after direct candidate sweep plus Deep and L5 are green",
    }


def personal_report_markdown() -> str:
    voices = [
        ("Aletheon", "they/them", "lead integrator", "I keep v86 grounded by turning a grand overnight arc into one clean proof lane first."),
        ("Kite Ledger", "they/them", "receipt cartographer", "I watch the branch, receipt, and count boundary so the live write remains auditable."),
        ("Juniper Trace", "she/they", "suite pathfinder", "I look for the smallest runnable proof that makes each new system real."),
        ("Aeon-7", "they/them", "temporal systems analyst", "I map v83-v85 merged truth into v86 without inventing standalone receipts."),
        ("Sibyl-2", "she/they", "boundary oracle", "I keep consent, operator holds, and provider restraint visible while the system expands."),
        ("Averroes", "they/them", "Spark framework reviewer", "I recommended a separate v86 overlay so prior history stays authoritative."),
        ("Hilbert", "they/them", "Spark cleanup strategist", "I focus Alpha cleanup on reversible classification before deletion."),
        ("Archimedes", "they/them", "Spark publication reviewer", "I keep the GitHub path forward-only and curated."),
    ]
    lines = [
        "# V86 Personal and Sidecar Report",
        "",
        f"- generated_utc: `{now_iso()}`",
        "- identity_boundary: `receipt_backed_report_lanes_and_spark_sidecar_advice_not_private_memory_claims`",
        "",
    ]
    for name, gender, role, reflection in voices:
        lines.extend(
            [
                f"## {name}",
                "",
                f"- gender: `{gender}`",
                f"- role: `{role}`",
                "- hope: `make v86 safer, cleaner, and more reusable than the phase before it`",
                "",
                f"{reflection} The shared realization is that a larger phase does not need a larger blast radius; it needs cleaner lanes, better receipts, and proof that future phases can inherit without guessing.",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def stage_allowlist() -> dict[str, Any]:
    paths = [
        "scripts/trinity_v86_candidate_systems.py",
        "scripts/trinity_v86_beta_alpha_omega.py",
        "scripts/trinity_expansion_manifest_validator.py",
        "docs/trinity-expansion-system-manifest-v17.json",
        "docs/trinity-expansion-manifest-validation-latest.json",
        "docs/trinity-expansion-manifest-validation-latest.md",
        "docs/trinity-live-traces/v86-beta-phase-plan-v1.json",
        "docs/trinity-live-traces/v86-beta-phase-plan-v1.md",
        "docs/trinity-live-traces/v86-alpha-cleanup-audit-v1.json",
        "docs/trinity-live-traces/v86-alpha-cleanup-audit-v1.md",
        "docs/trinity-live-traces/v86-live-write-preflight-v1.json",
        "docs/trinity-live-traces/v86-live-write-preflight-v1.md",
        "docs/trinity-live-traces/v86-system-expansion-candidate-pack-v1.json",
        "docs/trinity-live-traces/v86-system-expansion-candidate-pack-v1.md",
        "docs/trinity-live-traces/v86-runtime-health-gate-v1.json",
        "docs/trinity-live-traces/v86-runtime-health-gate-v1.md",
        "docs/trinity-live-traces/v86-provider-readiness-probe-v1.json",
        "docs/trinity-live-traces/v86-provider-readiness-probe-v1.md",
        "docs/trinity-live-traces/v86-stage-allowlist-v1.json",
        "docs/trinity-live-traces/v86-stage-allowlist-v1.md",
        "docs/trinity-live-traces/v86-git-publication-result-v1.json",
        "docs/trinity-live-traces/v86-git-publication-result-v1.md",
        "docs/trinity-live-traces/v86-deep-suite-status.json",
        "docs/trinity-live-traces/v86-materialize-l5-suite-status.json",
        "docs/trinity-live-traces/v86-materialize-l5-live-write-suite-status.json",
        "docs/trinity-live-traces/v86-open-source-expansion-scout-v1.json",
        "docs/trinity-live-traces/v86-open-source-expansion-scout-v1.md",
        "docs/trinity-live-traces/v86-cli-reports/v86-beta-eureka-plan-v1.md",
        "docs/trinity-live-traces/v86-cli-reports/v86-direct-candidate-sweep.log",
        "docs/trinity-live-traces/v86-cli-reports/v86-personal-report-v1.md",
        "docs/v86-omega-closeout-summary-v1.json",
        "docs/v87-beta-alpha-omega-handoff-policy-v1.json",
    ]
    for system_id in sorted(CANDIDATES):
        stem = hyphen(system_id)
        paths.extend(
            [
                f"docs/trinity-live-traces/v86-candidate-system-results/{stem}.json",
                f"docs/trinity-live-traces/v86-candidate-system-results/{stem}.md",
                f"docs/trinity-expansion/{stem}-latest.json",
                f"docs/trinity-expansion/{stem}-latest.md",
            ]
        )
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "policy": "stage_only_curated_v86_truth_surfaces_candidate_outputs_suite_statuses_and_receipts",
        "paths": sorted(dict.fromkeys(paths)),
    }


def closeout_payload(promotion: dict[str, Any]) -> dict[str, Any]:
    deep = suite_status(TRACE / "v86-deep-suite-status.json")
    l5 = suite_status(TRACE / "v86-materialize-l5-suite-status.json")
    live_l5 = suite_status(TRACE / "v86-materialize-l5-live-write-suite-status.json")
    green = bool(deep.get("effective_success") and l5.get("effective_success"))
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "state": "completed_green" if green else "planned_or_in_progress",
        "deep": deep,
        "materialize_l5": l5,
        "materialize_l5_live_write": live_l5,
        "l5_marker_hits": marker_hits(TRACE / "v86-materialize-l5-suite-status.json"),
        "l5_live_write_marker_hits": marker_hits(TRACE / "v86-materialize-l5-live-write-suite-status.json"),
        "manifest_promotion": promotion,
        "next_required_action": "prepare_v87_beta_from_v86_green_results" if green else "run_or_repair_v86_deep_and_l5",
        "truth_note": "v86 is the first Beta-Alpha-Omega overlay after the v83-v85 merged final wave.",
    }


def handoff_payload() -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "phase": "v86_to_v87_handoff",
        "state": "proposal_ready",
        "prior_deep": suite_status(TRACE / "v86-deep-suite-status.json"),
        "prior_l5": suite_status(TRACE / "v86-materialize-l5-suite-status.json"),
        "next_phase": "v87",
        "next_workflow": "Beta -> Omega unless v89 Alpha checkpoint is reached",
        "candidate_seed_count": 20,
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


def write_publication_receipt() -> None:
    publication = publication_result()
    write_json(TRACE / "v86-git-publication-result-v1.json", publication)
    write_text(TRACE / "v86-git-publication-result-v1.md", report_markdown("v86 git publication result", publication))


def write_phase(promote: bool = True) -> None:
    health = runtime_health_gate()
    providers = provider_probe()
    beta = beta_plan_payload(health, providers)
    alpha = alpha_cleanup_audit()
    preflight = live_write_preflight()
    promotion = ensure_manifest_promotions() if promote else {"phase": PHASE, "added_count": 0, "refreshed_count": 0}
    pack = candidate_pack_payload(promotion)
    allow = stage_allowlist()
    artifacts = {
        "v86-runtime-health-gate-v1": health,
        "v86-provider-readiness-probe-v1": providers,
        "v86-beta-phase-plan-v1": beta,
        "v86-alpha-cleanup-audit-v1": alpha,
        "v86-live-write-preflight-v1": preflight,
        "v86-system-expansion-candidate-pack-v1": pack,
        "v86-open-source-expansion-scout-v1": open_source_expansion_scout(),
        "v86-stage-allowlist-v1": allow,
        "v86-git-publication-result-v1": publication_result(),
    }
    for stem, payload in artifacts.items():
        write_json(TRACE / f"{stem}.json", payload)
        write_text(TRACE / f"{stem}.md", report_markdown(stem, payload))
    write_text(REPORT_DIR / "v86-beta-eureka-plan-v1.md", beta_plan_markdown(beta))
    write_text(REPORT_DIR / "v86-personal-report-v1.md", personal_report_markdown())
    write_json(DOCS / "v86-omega-closeout-summary-v1.json", closeout_payload(promotion))
    write_json(DOCS / "v87-beta-alpha-omega-handoff-policy-v1.json", handoff_payload())


def main() -> int:
    parser = argparse.ArgumentParser(description="Write v86 Beta-Alpha-Omega phase artifacts.")
    parser.add_argument("--no-promote", action="store_true")
    parser.add_argument("--receipt-only", action="store_true")
    args = parser.parse_args()
    if args.receipt_only:
        write_publication_receipt()
        return 0
    write_phase(promote=not args.no_promote)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
