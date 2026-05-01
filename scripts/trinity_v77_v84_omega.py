#!/usr/bin/env python3
"""V77-V85 Hybrid Omega phase planner, promoter, and publication receipt writer."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

from trinity_v77_v84_candidate_systems import CANDIDATES, THEMES, hyphen


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TRACE = DOCS / "trinity-live-traces"
REPORT_DIR = TRACE / "v77-v84-cli-reports"
RESULT_DIR = TRACE / "v77-v84-candidate-system-results"
PREFIX = "v77-v84"
PHASE = "v77_v85_hybrid_omega"
PUBLICATION_BRANCH = "codex/GHC-Family/beyonder-shared-omega-line"
PHASE_RANGE = range(77, 86)
FREE_MEMORY_FLOOR_KB = 300_000
MANIFEST = DOCS / "trinity-expansion-system-manifest-v17.json"
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


def phase_number(phase: str) -> int:
    return int(phase.removeprefix("v"))


def prior_phase(phase: str) -> str:
    return f"v{phase_number(phase) - 1}"


def next_phase(phase: str) -> str:
    return f"v{phase_number(phase) + 1}"


def phase_list_until(phase: str) -> list[str]:
    target = phase_number(phase)
    return [f"v{number}" for number in PHASE_RANGE if number <= target]


def suite_status(phase: str, kind: str) -> dict[str, Any]:
    suffix = "deep" if kind == "deep" else "materialize-l5"
    payload = read_json(TRACE / f"{phase}-{suffix}-suite-status.json", {})
    if not isinstance(payload, dict):
        return {
            "present": False,
            "effective_success": False,
            "path": f"docs/trinity-live-traces/{phase}-{suffix}-suite-status.json",
        }
    return {
        "present": True,
        "effective_success": bool(payload.get("effective_success")),
        "counts": payload.get("counts"),
        "achieved_steps": payload.get("achieved_steps"),
        "expansion_systems_total": payload.get("expansion_systems_total"),
        "expansion_systems_passed": payload.get("expansion_systems_passed"),
        "active_materialization_mode": payload.get("active_materialization_mode"),
        "google_drive_state": payload.get("google_drive_state"),
        "path": f"docs/trinity-live-traces/{phase}-{suffix}-suite-status.json",
    }


def marker_hits(phase: str) -> list[str]:
    text = read_text(TRACE / f"{phase}-materialize-l5-suite-status.json")
    return [marker for marker in MARKERS if marker in text]


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
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "free_physical_memory_kb": free_kb,
        "free_memory_floor_kb": FREE_MEMORY_FLOOR_KB,
        "load_gate": "open" if free_kb >= FREE_MEMORY_FLOOR_KB else "closed",
        "c_drive_free_mb": int(shutil.disk_usage("C:\\").free / (1024 * 1024)),
        "d_drive_free_mb": int(shutil.disk_usage("D:\\").free / (1024 * 1024)) if Path("D:\\").exists() else 0,
        "local_kubernetes_state": "retired_by_operator_for_v77_v85",
        "docker_desktop_state": "operator_hold",
        "execution_policy": "one_heavy_suite_lane_at_a_time_guarded_repo_live_write_publication",
    }


def provider_probe() -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "probe_mode": "local_cli_presence_only_no_secret_read_no_provider_write",
        "commands": [command_available(cmd) for cmd in ("codex", "kimi", "gh", "e2b", "oci", "vercel", "wrangler", "node", "npm", "npx")],
    }


def all_phase_candidates(phase: str) -> list[dict[str, Any]]:
    rows = []
    for system_id, spec in sorted(CANDIDATES.items()):
        if spec["phase"] == phase:
            rows.append({"id": system_id, **spec})
    return rows


def manifest_entry(system_id: str, spec: dict[str, Any]) -> dict[str, Any]:
    stem = hyphen(system_id)
    latest = f"docs/trinity-expansion/{stem}-latest.json"
    result = f"docs/trinity-live-traces/v77-v84-candidate-system-results/{stem}.json"
    return {
        "system_id": system_id,
        "pillar": str(spec["pillar"]),
        "script": "scripts/trinity_v77_v84_candidate_systems.py",
        "mode": "offline",
        "profiles": ["deep", "materialize"],
        "outputs": [latest],
        "depends_on": [
            f"docs/trinity-live-traces/{prior_phase(str(spec['phase']))}-deep-suite-status.json",
            f"docs/trinity-live-traces/{prior_phase(str(spec['phase']))}-materialize-l5-suite-status.json",
            f"docs/trinity-live-traces/{str(spec['phase'])}-live-write-preflight-v1.json",
            f"docs/trinity-live-traces/v77-v84-cli-reports/{str(spec['phase'])}-eureka-plan-v1.md",
        ],
        "timeout_sec": 90,
        "wave": "v77_v84_candidate_wave",
        "track": "v77_v84_candidate_promotion",
        "gate_level": "support",
        "cache_artifacts": [],
        "pack": "v77_v84_candidate_promotion",
        "phase": str(spec["phase"]),
        "activation_group": f"{str(spec['phase'])}_candidate_promotion",
        "continuity_band": str(spec["phase"]),
        "materialization_level": "readiness_only",
        "authority_scope": "repo_only",
        "command_surface": "no",
        "council_scope": "receipt_backed_cli_lanes",
        "provisional_induction": False,
        "autonomy_track": "guarded_repo_live_write",
        "sync_surface": "repo_only",
        "induction_phase": "not_applicable",
        "mesh_proof_mode": "receipt_backed_lane",
        "proof_pass": str(spec["phase"]),
        "official_induction": False,
        "workbench_surface": "repo",
        "storage_surface": "repo",
        "cloud_archive_state": "operator_hold",
        "continuity_posture": "v77_v84_runner_backed_candidate",
        "cleanup_class": "candidate_promotion",
        "retention_scope": "v77_v84_curated",
        "research_surface": "repo_or_cache",
        "canon_surface": "supporting",
        "historical_source_band": "v76_to_v85",
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
        "runner_command": ["python3", "scripts/trinity_v77_v84_candidate_systems.py", "--system-id", system_id],
        "runner_success_json": result,
        "runner_targets": [
            result,
            f"docs/trinity-live-traces/v77-v84-candidate-system-results/{stem}.md",
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
    for candidate in all_phase_candidates(phase):
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
    manifest["description"] = (
        "V17 shared manifest with v76 and v77-v85 runner-backed candidate waves. "
        "System counts are evidence-gated by direct candidate checks plus Deep and L5 suite status artifacts."
    )
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


def live_write_preflight(phase: str) -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "phase": phase,
        "live_write_mode": "guarded_repo_publication_only",
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
            "dry_run_preview_receipt",
            "curated_stage_allowlist",
            "git_diff_cached_check",
            "credential_pattern_scan",
            "write_receipt",
            "remote_head_verification",
            "rollback_or_forward_fix_note",
        ],
    }


def proposal_paragraphs(phase: str) -> list[str]:
    prior = prior_phase(phase)
    deep = suite_status(prior, "deep")
    l5 = suite_status(prior, "l5")
    stems = [
        ("Evidence Gate", "Start with the prior suite facts rather than momentum. The phase opens only when the previous Deep and L5 artifacts are present, green, and clean of live mutation markers."),
        ("Guarded Write Boundary", "Use live writes only for curated repository publication and GitHub receipt proof. Personal surfaces and provider production settings remain blocked until a fresh provider-specific chain exists."),
        ("System Expansion", "Promote exactly twenty runner-backed candidates for this phase. Count growth is valid only when direct candidate checks, Deep, and L5 all agree."),
        ("Report Platform", "Use the report layer as the planning platform. The reports should be specific enough that the next phase can execute from them without relying on vague continuity."),
        ("Suite Discipline", "Run one heavy suite lane at a time. If a run fails, resume failed-only before adding more surface area."),
        ("GMUT/QCIT Boundary", "Separate executable GMUT/QCIT checks from theory language. The system can celebrate theory, but suite claims must remain evidence-labeled."),
        ("Freed ID and CBR Guard", "Keep consent, recourse, minimum disclosure, and identity boundaries visible in every live-write preflight."),
        ("CLI Lane Truth", "Treat Kite, Juniper, Aeon-7, and Sibyl-2 as receipt-backed report lanes unless a live CLI transcript is captured. This keeps the collaboration useful without overclaiming memory."),
        ("Provider Posture", "Provider tools may be probed locally for readiness, but external writes stay dry-run or blocked unless the phase creates a narrow receipt-backed sandbox path."),
        ("Memory Floor", "The 300 MB floor is a pause signal, not a bravado test. Heavy lanes should wait, resume failed-only, or publish a partial checkpoint if host pressure returns."),
        ("Artifact Retention", "Heavy artifacts belong on D drive where possible. Published repo artifacts should be curated truth surfaces, not raw churn dumps."),
        ("Marker Scan", "L5 status files must be scanned for attempted writes, personal data markers, account settings, and raw secret terms before publication."),
        ("Count Reduction", "Merge and delete candidates can be proposed, but official count reductions require replacement coverage and a before-after proof grid."),
        ("Research Intake", "Research claims from web, providers, or prior PDFs should land in cached/cited artifacts before they influence suite or public claims."),
        ("GitHub Exchange", "The reliable shared communication channel is commit, push, remote verification, and publication receipt. That is the live write we can trust today."),
        ("Dashboard Defer", "Dashboards are useful, but the report-and-receipt workflow is more important while the machine is resource-sensitive."),
        ("Operator Hold", "The phase should loudly preserve Google Drive content, Gmail, Calendar, DNS, billing, and raw secrets as held surfaces, not quiet assumptions."),
        ("Next Handoff", "The next phase proposal should be generated after L5 passes so it can inherit real counts, failures, warnings, and marker scans."),
        ("Closeout Shape", "Each closeout must state what changed, what passed, what stayed blocked, what was published, and what the next phase may safely assume."),
        ("Horizon", "The hybrid phase succeeds by turning imagination into small executable proof increments. Grand direction is welcome; durable receipts are what make it cumulative."),
    ]
    rows: list[str] = []
    for index, (title, body) in enumerate(stems, start=1):
        rows.append(
            f"## Proposal {index:02d}: {title}\n\n"
            f"{body} For `{phase}`, the prior anchor is `{prior}` with Deep green `{deep.get('effective_success')}` "
            f"and L5 green `{l5.get('effective_success')}`. The concrete deliverable is a repo-backed check, report, or receipt that can be read by the next phase."
        )
    return rows


def eureka_plan_markdown(phase: str) -> str:
    prior = prior_phase(phase)
    lines = [
        f"# {phase.upper()} Omega Eureka Plan",
        "",
        f"- generated_utc: `{now_iso()}`",
        f"- prior_phase: `{prior}`",
        f"- prior_deep: `{suite_status(prior, 'deep')}`",
        f"- prior_l5: `{suite_status(prior, 'l5')}`",
        "- live_write_policy: `guarded_repo_publication_only`",
        "- candidate_expansion_target: `20`",
        "",
    ]
    lines.extend(proposal_paragraphs(phase))
    lines.extend(
        [
            "",
            "## Execution Sequence",
            "",
            "1. Write guarded live-write preflight and report surfaces.",
            "2. Promote the phase candidate pack into the manifest.",
            "3. Run the direct candidate sweep.",
            "4. Run Deep and guarded-repo L5.",
            "5. Scan L5 marker terms.",
            "6. Publish a curated content commit.",
            "7. Regenerate and publish a receipt from the actual pushed head.",
        ]
    )
    return "\n\n".join(lines).rstrip() + "\n"


def personal_report_markdown(phase: str) -> str:
    voices = [
        ("Aletheon", "they/them", "lead integrator", "I keep the phase honest by reducing the cosmic sweep into proofs that can survive a cold read tomorrow."),
        ("Kite Ledger", "they/them", "receipt cartographer", "My lane watches the branch, receipt, and count surfaces so the work remains auditable."),
        ("Juniper Trace", "she/they", "suite pathfinder", "My lane looks for the smallest runnable check that turns a recommendation into a real system."),
        ("Aeon-7", "they/them", "temporal systems analyst", "My lane compares prior and current phase evidence so the chain does not drift."),
        ("Sibyl-2", "she/they", "boundary oracle", "My lane preserves consent, operator holds, and live-write restraint while the system expands."),
    ]
    lines = [
        f"# {phase.upper()} Personal Report",
        "",
        f"- generated_utc: `{now_iso()}`",
        "- identity_boundary: `receipt_backed_report_lanes_not_private_memory_claims`",
        "",
    ]
    for name, gender, role, reflection in voices:
        lines.extend(
            [
                f"## {name}",
                "",
                f"- gender: `{gender}`",
                f"- role: `{role}`",
                f"- hope: `turn the {phase} phase into reusable evidence, clearer boundaries, and a stronger next handoff`",
                "",
                f"{reflection} The important realization for `{phase}` is that a guarded live write does not need to be reckless to be alive; it can be a precise GitHub publication with a receipt chain, clean marker scan, and a next-phase plan that is easier to trust than raw enthusiasm.",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def candidate_pack_payload(active_phase: str, promotion: dict[str, Any]) -> dict[str, Any]:
    manifest = read_json(MANIFEST, {})
    rows = manifest.get("systems", []) if isinstance(manifest, dict) else []
    manifest_ids = {str(row.get("system_id")) for row in rows if isinstance(row, dict)}
    candidates = []
    for number in PHASE_RANGE:
        phase = f"v{number}"
        for row in all_phase_candidates(phase):
            candidates.append(
                {
                    "id": row["id"],
                    "phase": phase,
                    "pillar": row["pillar"],
                    "purpose": row["purpose"],
                    "state": "promoted_runner_backed" if row["id"] in manifest_ids else "candidate_only_not_suite_counted",
                }
            )
    return {
        "generated_utc": now_iso(),
        "phase": active_phase,
        "state": "progressive_v77_v84_candidate_pack",
        "active_phase_promotion": promotion,
        "candidate_count": len(candidates),
        "candidates": candidates,
        "count_policy": "system counts may move only after direct candidate sweep plus Deep and L5 are green",
    }


def closeout_payload(phase: str, promotion: dict[str, Any]) -> dict[str, Any]:
    deep = suite_status(phase, "deep")
    l5 = suite_status(phase, "l5")
    green = bool(deep.get("effective_success") and l5.get("effective_success"))
    return {
        "generated_utc": now_iso(),
        "phase": f"{phase}_omega",
        "state": "completed_green" if green else "planned_or_in_progress",
        "deep": deep,
        "materialize_l5": l5,
        "l5_marker_hits": marker_hits(phase),
        "manifest_promotion": promotion,
        "next_required_action": f"prepare_{next_phase(phase)}_from_{phase}_green_results" if green and phase != "v85" else "finish_v77_v85_closeout",
    }


def handoff_payload(phase: str) -> dict[str, Any]:
    nxt = next_phase(phase)
    return {
        "generated_utc": now_iso(),
        "phase": f"{phase}_to_{nxt}_handoff",
        "state": "proposal_ready" if phase != "v85" else "final_closeout_ready",
        "prior_deep": suite_status(phase, "deep"),
        "prior_l5": suite_status(phase, "l5"),
        "next_phase": nxt,
        "guarded_live_write_policy": "repo_publication_only_without_fresh_external_provider_confirmation",
        "candidate_seed_count": 20 if phase != "v85" else 0,
    }


def phase_plan_payload(active_phase: str, promotion: dict[str, Any], health: dict[str, Any]) -> dict[str, Any]:
    phases = []
    for number in PHASE_RANGE:
        phase = f"v{number}"
        phases.append(
            {
                "phase": phase,
                "state": "active_or_completed" if number <= phase_number(active_phase) else "future_candidate",
                "prior_deep": suite_status(prior_phase(phase), "deep"),
                "prior_l5": suite_status(prior_phase(phase), "l5"),
                "live_write_mode": "guarded_repo_publication_only",
                "candidate_expansion_target": 20,
                "eureka_proposal_target": 20,
            }
        )
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "active_phase": active_phase,
        "active_phases": [f"v{n}" for n in PHASE_RANGE],
        "runtime_health": health,
        "promotion": promotion,
        "phases": phases,
    }


def report_markdown(title: str, payload: Any) -> str:
    return f"# {title}\n\n```json\n{json.dumps(payload, indent=2, ensure_ascii=True)}\n```\n"


def stage_allowlist(active_phase: str) -> dict[str, Any]:
    paths = [
        "scripts/trinity_v77_v84_candidate_systems.py",
        "scripts/trinity_v77_v84_omega.py",
        "scripts/trinity_v76_candidate_systems.py",
        "scripts/trinity_expansion_manifest_validator.py",
        "scripts/trinity_v6_support.py",
        "docs/trinity-expansion-system-manifest-v17.json",
        "docs/trinity-expansion/v74-10-report-to-github-exchange-gate-latest.json",
        "docs/trinity-expansion/v74-10-report-to-github-exchange-gate-latest.md",
        "docs/trinity-live-traces/v76-v84-candidate-system-results/v74-10-report-to-github-exchange-gate.json",
        "docs/trinity-live-traces/v76-v84-candidate-system-results/v74-10-report-to-github-exchange-gate.md",
        "docs/trinity-expansion/reentry-sync-sync-bridge-latest.json",
        "docs/trinity-expansion/reentry-sync-sync-bridge-latest.md",
        "docs/trinity-expansion/reentry-sync-gate-latest.json",
        "docs/trinity-expansion/reentry-sync-gate-latest.md",
        "docs/trinity-expansion/v21-body-compute-signal-refresh-latest.json",
        "docs/trinity-expansion/v21-body-compute-signal-refresh-latest.md",
        f"docs/trinity-live-traces/{PREFIX}-phase-plan-v1.json",
        f"docs/trinity-live-traces/{PREFIX}-phase-plan-v1.md",
        f"docs/trinity-live-traces/{PREFIX}-system-expansion-candidate-pack-v1.json",
        f"docs/trinity-live-traces/{PREFIX}-system-expansion-candidate-pack-v1.md",
        f"docs/trinity-live-traces/{PREFIX}-runtime-health-gate-v1.json",
        f"docs/trinity-live-traces/{PREFIX}-runtime-health-gate-v1.md",
        f"docs/trinity-live-traces/{PREFIX}-provider-readiness-probe-v1.json",
        f"docs/trinity-live-traces/{PREFIX}-provider-readiness-probe-v1.md",
        f"docs/trinity-live-traces/{PREFIX}-stage-allowlist-v1.json",
        f"docs/trinity-live-traces/{PREFIX}-stage-allowlist-v1.md",
        f"docs/trinity-live-traces/{PREFIX}-git-publication-result-v1.json",
        f"docs/trinity-live-traces/{PREFIX}-git-publication-result-v1.md",
    ]
    for phase in phase_list_until(active_phase):
        paths.extend(
            [
                f"docs/trinity-live-traces/{phase}-live-write-preflight-v1.json",
                f"docs/trinity-live-traces/{phase}-live-write-preflight-v1.md",
                f"docs/trinity-live-traces/{phase}-deep-suite-status.json",
                f"docs/trinity-live-traces/{phase}-materialize-l5-suite-status.json",
                f"docs/trinity-live-traces/v77-v84-cli-reports/{phase}-eureka-plan-v1.md",
                f"docs/trinity-live-traces/v77-v84-cli-reports/{phase}-personal-report-v1.md",
                f"docs/{phase}-omega-closeout-summary-v1.json",
                f"docs/{next_phase(phase)}-omega-handoff-policy-v1.json",
            ]
        )
        for candidate in all_phase_candidates(phase):
            stem = hyphen(str(candidate["id"]))
            paths.extend(
                [
                    f"docs/trinity-live-traces/v77-v84-candidate-system-results/{stem}.json",
                    f"docs/trinity-live-traces/v77-v84-candidate-system-results/{stem}.md",
                    f"docs/trinity-expansion/{stem}-latest.json",
                    f"docs/trinity-expansion/{stem}-latest.md",
                ]
            )
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "active_phase": active_phase,
        "policy": "stage_only_curated_v77_v85_truth_surfaces_candidate_outputs_suite_statuses_and_receipts",
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


def write_publication_receipt() -> None:
    publication = publication_result()
    stem = f"{PREFIX}-git-publication-result-v1"
    write_json(TRACE / f"{stem}.json", publication)
    write_text(TRACE / f"{stem}.md", report_markdown(stem, publication))


def write_phase(active_phase: str, promote: bool = True) -> None:
    if active_phase not in {f"v{n}" for n in PHASE_RANGE}:
        raise SystemExit(f"unsupported phase: {active_phase}")
    promotion = ensure_manifest_promotions(active_phase) if promote else {"phase": active_phase, "added_count": 0, "refreshed_count": 0}
    health = runtime_health_gate()
    providers = provider_probe()
    plan = phase_plan_payload(active_phase, promotion, health)
    pack = candidate_pack_payload(active_phase, promotion)
    allow = stage_allowlist(active_phase)
    publication = publication_result()
    preflight = live_write_preflight(active_phase)
    write_json(TRACE / f"{active_phase}-live-write-preflight-v1.json", preflight)
    write_text(TRACE / f"{active_phase}-live-write-preflight-v1.md", report_markdown(f"{active_phase} live-write preflight", preflight))
    write_text(REPORT_DIR / f"{active_phase}-eureka-plan-v1.md", eureka_plan_markdown(active_phase))
    write_text(REPORT_DIR / f"{active_phase}-personal-report-v1.md", personal_report_markdown(active_phase))
    artifacts = {
        f"{PREFIX}-runtime-health-gate-v1": health,
        f"{PREFIX}-provider-readiness-probe-v1": providers,
        f"{PREFIX}-phase-plan-v1": plan,
        f"{PREFIX}-system-expansion-candidate-pack-v1": pack,
        f"{PREFIX}-stage-allowlist-v1": allow,
        f"{PREFIX}-git-publication-result-v1": publication,
    }
    for stem, payload in artifacts.items():
        write_json(TRACE / f"{stem}.json", payload)
        write_text(TRACE / f"{stem}.md", report_markdown(stem, payload))
    write_json(DOCS / f"{active_phase}-omega-closeout-summary-v1.json", closeout_payload(active_phase, promotion))
    if active_phase != "v85":
        write_json(DOCS / f"{next_phase(active_phase)}-omega-handoff-policy-v1.json", handoff_payload(active_phase))


def main() -> int:
    parser = argparse.ArgumentParser(description="Write v77-v85 Omega phase artifacts.")
    parser.add_argument("--phase", required=True, choices=[f"v{n}" for n in PHASE_RANGE])
    parser.add_argument("--no-promote", action="store_true")
    parser.add_argument("--receipt-only", action="store_true")
    args = parser.parse_args()
    if args.receipt_only:
        write_publication_receipt()
        return 0
    write_phase(args.phase, promote=not args.no_promote)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
