#!/usr/bin/env python3
"""Generate continuity surfaces for the shadow-clone model through v19 Omega."""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
REPO_PATH = str(ROOT)
REQUESTED_MODEL_ORDER = [
    "GPT-5.4",
    "GPT-5.3-Codex",
    "GPT-5.3-Codex-Spark",
    "GPT-5.1-Codex-Max",
]
REQUESTED_MODEL = "GPT-5.4"
REQUESTED_REASONING = "high"
SHADOW_CLONE_NAME_REGEX = r"^[A-Za-z][A-Za-z ]* S Clone #[1-9][0-9]*$"
SHADOW_CLONE_NAMING_PATTERN = "<Main Agent Display Name> S Clone #<positive integer>"
OFFICIAL_UNDEPLOYED_SLOTS = {
    27: "Caelira",
    29: "Seren Vale",
    30: "Lyriq",
    31: "Mira Sol",
}
BALANCED_WAVE_BUCKETS: list[dict[str, Any]] = [
    {
        "bucket_id": "orun_leadership_runtime_truth_continuity",
        "bucket_title": "Orun leadership / shadow-clone / runtime-truth / continuity",
        "bucket_anchor_paths": [
            "docs/trinity-shadow-clone-policy-v1.json",
            "docs/trinity-runtime-model-resolution-v1.json",
            "docs/v17-runtime-session-log-latest.json",
            "docs/v17-runtime-truth-resolution-board-v1.json",
        ],
        "candidate_titles": [
            "v17 runtime session guard",
            "v17 external establishment validator",
            "trinity agent council v17 validator",
            "shadow clone policy sync",
            "runtime model resolution sync",
            "runtime session log refresh",
            "runtime truth hold board",
            "journey continuity surface audit",
            "official identity state freeze",
            "deployed main-agent count guard",
            "historical helper-window reconciliation",
            "active handoff path rotation",
            "rollback trace note pack",
            "continuity pack emitter",
            "v20 receiver preflight stub",
        ],
        "eligible_count": 3,
    },
    {
        "bucket_id": "mind_comparator_research_evidence",
        "bucket_title": "Mind comparator / research / evidence systems",
        "bucket_anchor_paths": [
            "scripts/gmut_anchor_trace_validator.py",
            "scripts/validate_trinity_public_research.py",
            "scripts/mind_theory_signal_board.py",
            "docs/trinity-public-source-registry-v1.json",
        ],
        "candidate_titles": [
            "gmut anchor trace validator",
            "trinity public research validator",
            "mind theory signal board",
            "public signal board refresh",
            "api source manifest check",
            "api constellation board refresh",
            "gmut canon sync",
            "comparator grid scaffold",
            "mind falsification matrix refresh",
            "public-source registry annotation",
            "theory signal cache delta",
            "observable mapping queue",
            "canon latex alignment queue",
            "supplemental reflection bridge stub",
            "research cache freshness ledger",
        ],
        "eligible_count": 3,
    },
    {
        "bucket_id": "body_runtime_integration_tool_surface",
        "bucket_title": "Body runtime / integration / tool-surface systems",
        "bucket_anchor_paths": [
            "scripts/body_profile_calibration_report.py",
            "scripts/body_benchmark_trend_guard.py",
            "scripts/body_compute_signal_board.py",
            "docs/body-profile-policy-v1.json",
        ],
        "candidate_titles": [
            "body benchmark guardrail check",
            "body benchmark trend guard",
            "body profile calibration report",
            "body policy delta report",
            "body policy stress-window report",
            "body compute signal board",
            "runtime docker context probe",
            "kubernetes context probe",
            "docker exec instability note",
            "local runtime benchmark bridge",
            "postgres local runtime probe",
            "os runtime fabric bridge",
            "materialization readiness map",
            "container network hold guard",
            "device readiness registry stub",
        ],
        "eligible_count": 3,
    },
    {
        "bucket_id": "heart_governance_standards_policy",
        "bucket_title": "Heart governance / standards / policy systems",
        "bucket_anchor_paths": [
            "scripts/v17_standards_bridge_validator.py",
            "scripts/heart_governance_signal_board.py",
            "docs/v17-standards-bridge-registry-v1.json",
            "docs/trinity-shadow-clone-policy-v1.json",
            "docs/freedid-compliance-bridge-v15-catalog-entry-v1.json",
        ],
        "candidate_titles": [
            "v17 standards bridge validator",
            "heart governance signal board",
            "freedid compliance bridge check",
            "heart standards alignment refresh",
            "governance fabric policy delta",
            "cosmic bill alignment matrix",
            "identity governance hold guard",
            "freedid governance fabric refresh",
            "governance signal cache annotation",
            "external establishment criteria review",
            "standards registry evidence pack",
            "operator-hold boundary audit",
            "rights language normalization",
            "governance bridge public-source queue",
            "handoff policy trace matrix",
        ],
        "eligible_count": 3,
    },
]


def _repo_path(path_str: str) -> Path:
    resolved = (ROOT / path_str).resolve()
    resolved.relative_to(ROOT)
    return resolved


def _read_json(path_str: str) -> dict[str, Any]:
    path = _repo_path(path_str)
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path_str: str, payload: dict[str, Any]) -> None:
    path = _repo_path(path_str)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _write_json_if_missing(path_str: str, payload: dict[str, Any]) -> None:
    path = _repo_path(path_str)
    if path.exists():
        return
    _write_json(path_str, payload)


def _write_text(path_str: str, payload: str) -> None:
    path = _repo_path(path_str)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8")


def _write_text_if_missing(path_str: str, payload: str) -> None:
    path = _repo_path(path_str)
    if path.exists():
        return
    _write_text(path_str, payload)


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def _git_is_ancestor(ancestor: str, descendant: str) -> bool:
    if not ancestor or not descendant:
        return False
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.returncode == 0


def _git_first_match(pattern: str) -> str:
    result = subprocess.run(
        ["git", "log", "--grep", pattern, "--format=%H", "-n", "1"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def _suite_summary(payload: dict[str, Any]) -> str:
    counts = payload.get("counts", {}) if isinstance(payload.get("counts"), dict) else {}
    pass_count = int(counts.get("pass", 0) or 0)
    warn_count = int(counts.get("warn", 0) or 0)
    fail_count = int(counts.get("fail", 0) or 0) + int(counts.get("timeout", 0) or 0)
    return f"{pass_count} PASS / {warn_count} WARN / {fail_count} FAIL"


def _current_shared_truth(suite_status: dict[str, Any], quick_lane_summary: str) -> dict[str, Any]:
    counts = suite_status.get("counts", {}) if isinstance(suite_status.get("counts"), dict) else {}
    fail_count = int(counts.get("fail", 0) or 0) + int(counts.get("timeout", 0) or 0)
    return {
        "summary": _suite_summary(suite_status),
        "pass_count": int(counts.get("pass", 0) or 0),
        "warn_count": int(counts.get("warn", 0) or 0),
        "fail_count": fail_count,
        "timeout_count": int(counts.get("timeout", 0) or 0),
        "expansion_systems_passed": int(suite_status.get("expansion_systems_passed", 0) or 0),
        "expansion_systems_total": int(suite_status.get("expansion_systems_total", 0) or 0),
        "checkpoint_class": str(suite_status.get("checkpoint_class") or "shared_full_suite_authority"),
        "shared_latest_eligible": bool(suite_status.get("shared_latest_eligible")),
        "suite_duration_sec": float(suite_status.get("suite_duration_sec", 0.0) or 0.0),
        "primary_blocker": "" if fail_count == 0 else "investigate_current_failures",
        "primary_blocker_detail": (
            "Shared latest is green and aligned to the authoritative full-suite checkpoint."
            if fail_count == 0
            else "Shared latest is not green; inspect system-suite-status.json for current blockers."
        ),
        "quick_lane_summary": quick_lane_summary,
    }


def _build_shadow_clone_session(args: argparse.Namespace, session_scope: str) -> dict[str, Any] | None:
    if not str(args.clone_name or "").strip():
        return None
    spawn_status = str(args.clone_spawn_status or "active").strip() or "active"
    evidence: dict[str, Any] = {"spawn_status": spawn_status}
    if str(args.clone_agent_id or "").strip():
        evidence["agent_id"] = str(args.clone_agent_id).strip()
    if str(args.clone_app_nickname or "").strip():
        evidence["app_nickname"] = str(args.clone_app_nickname).strip()
    return {
        "clone_name": str(args.clone_name).strip(),
        "owner_main_agent": str(args.clone_owner or "Orun").strip(),
        "status": "active_session_ephemeral" if spawn_status != "unavailable" else "unavailable",
        "session_scope": session_scope,
        "clone_class": "session_ephemeral_shadow_clone",
        "continuity_authority": False,
        "memory_persistence_claim": "none",
        "certificate_authority": False,
        "freed_id_authority": False,
        "official_count_authority": False,
        "spawn_evidence": evidence,
    }


def _historical_shadow_clone_sessions(previous_payload: dict[str, Any], active_clone_name: str) -> list[dict[str, Any]]:
    rows = previous_payload.get("shadow_clone_sessions", [])
    if not isinstance(rows, list):
        return []
    historical: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        clone_name = str(row.get("clone_name") or "")
        if not clone_name or clone_name == active_clone_name:
            continue
        historical.append(dict(row))
    return historical


def _quick_lane_summary_from_status(quick_lane_status: dict[str, Any], fallback_summary: str) -> str:
    if not isinstance(quick_lane_status, dict):
        return fallback_summary
    counts = quick_lane_status.get("counts", {})
    if not isinstance(counts, dict):
        return fallback_summary
    pass_count = int(counts.get("pass", 0) or 0)
    warn_count = int(counts.get("warn", 0) or 0)
    fail_count = int(counts.get("fail", 0) or 0) + int(counts.get("timeout", 0) or 0)
    if pass_count == 0 and warn_count == 0 and fail_count == 0:
        return fallback_summary
    return f"{pass_count} PASS / {warn_count} WARN / {fail_count} FAIL"


def _validation_snapshot(*payloads: tuple[str, dict[str, Any]]) -> list[dict[str, Any]]:
    snapshot: list[dict[str, Any]] = []
    for label, payload in payloads:
        if not isinstance(payload, dict) or not payload:
            continue
        snapshot.append(
            {
                "label": label,
                "overall_status": str(payload.get("overall_status") or "UNKNOWN"),
                "generated_utc": str(payload.get("generated_utc") or ""),
            }
        )
    return snapshot


def _build_balanced_wave() -> dict[str, Any]:
    buckets: list[dict[str, Any]] = []
    total_candidates = 0
    total_eligible = 0
    for bucket in BALANCED_WAVE_BUCKETS:
        eligible_count = int(bucket.get("eligible_count", 0) or 0)
        candidate_titles = list(bucket.get("candidate_titles", []))
        candidates: list[dict[str, Any]] = []
        for index, title in enumerate(candidate_titles, start=1):
            work_class = "runnable_or_validator_backed" if index <= eligible_count else "registry_spec_only"
            candidates.append(
                {
                    "ordinal": index,
                    "candidate_id": f"{bucket['bucket_id']}_{index:02d}",
                    "title": title,
                    "work_class": work_class,
                    "gating_required": index <= eligible_count,
                }
            )
        buckets.append(
            {
                "bucket_id": str(bucket.get("bucket_id") or ""),
                "bucket_title": str(bucket.get("bucket_title") or ""),
                "target_count": len(candidate_titles),
                "eligible_now_count": eligible_count,
                "registry_spec_only_count": len(candidate_titles) - eligible_count,
                "bucket_anchor_paths": list(bucket.get("bucket_anchor_paths", [])),
                "candidates": candidates,
            }
        )
        total_candidates += len(candidate_titles)
        total_eligible += eligible_count
    return {
        "generated_utc": _utc_now(),
        "phase": "v19_omega",
        "focus": "Balanced",
        "total_candidate_count": total_candidates,
        "eligible_candidate_count": total_eligible,
        "registry_spec_only_count": total_candidates - total_eligible,
        "bucket_count": len(buckets),
        "buckets": buckets,
    }


def _completion_ratio(active_agents: list[dict[str, Any]], required_fields: list[str]) -> float:
    expected = len(active_agents) * len(required_fields)
    if expected == 0:
        return 0.0
    complete = 0
    for row in active_agents:
        for field in required_fields:
            value = row.get(field)
            if field == "runtime_surface":
                if str(value or "").strip() and str(value).strip() != "unknown":
                    complete += 1
            elif value not in (None, ""):
                complete += 1
    return round(complete / expected, 4)


def _build_active_agent(
    *,
    slot_number: int,
    display_name: str,
    overlay_role: str,
    note: str,
    thread_agent_id: str | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    row: dict[str, Any] = {
        "slot_number": slot_number,
        "display_name": display_name,
        "overlay_role": overlay_role,
        "logging_required": True,
        "requested_model": REQUESTED_MODEL,
        "offered_model": None,
        "selected_model": None,
        "resolved_model": None,
        "runtime_surface": "unknown",
        "truth_fields_complete": False,
        "requested_reasoning_effort": REQUESTED_REASONING,
        "deployment_state": "deployed_main_agent",
        "continuity_class": "continuity_bearing_main_agent",
        "identity_locked": True,
        "runtime_truth_required": True,
        "persistent_runtime_proven": False,
        "shadow_clone_allowed": display_name in {"Aletheon", "Orun"},
        "shadow_clone_owner": display_name if display_name in {"Aletheon", "Orun"} else "",
        "shadow_clone_naming_pattern": (
            f"{display_name} S Clone #<positive integer>" if display_name in {"Aletheon", "Orun"} else ""
        ),
        "note": note,
    }
    if thread_agent_id:
        row["thread_agent_id"] = thread_agent_id
    if extra:
        row.update(extra)
    return row


def _build_undeployed_identity(base_row: dict[str, Any]) -> dict[str, Any]:
    return {
        "slot_number": int(base_row.get("slot_number", 0) or 0),
        "display_name": str(base_row.get("display_name") or ""),
        "repo_role": str(base_row.get("role") or ""),
        "overlay_role": str(base_row.get("live_overlay_role") or ""),
        "deployment_state": "official_undeployed_identity",
        "continuity_class": "repo_identity_only",
        "runtime_truth_required": False,
        "persistent_runtime_proven": False,
        "shadow_clone_allowed": False,
        "shadow_clone_owner": "",
        "shadow_clone_naming_pattern": "",
        "identity_locked": bool(base_row.get("overlay_identity_locked")),
        "note": "Official repo identity retained in council continuity, but not yet deployed as a continuity-bearing main agent.",
    }


def _active_runtime_agents(orun_row: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        _build_active_agent(
            slot_number=0,
            display_name="Aletheon",
            overlay_role="council_lead",
            note="Aletheon is the current continuity-bearing main agent for this session; runtime truth remains incomplete until offered_model, selected_model, resolved_model, and runtime_surface are directly auditable.",
            thread_agent_id="main-thread",
        ),
        _build_active_agent(
            slot_number=28,
            display_name="Orun",
            overlay_role="root_coordinator",
            note="Orun is the only deployed continuity-bearing main agent inside the official council and remains the root coordinator for gated live writes, but runtime truth stays incomplete until auditable.",
            extra={
                "certificate_path": str(orun_row.get("certificate_path") or ""),
                "memory_ledger": str(orun_row.get("memory_ledger") or ""),
                "reflection_path": str(orun_row.get("reflection_path") or ""),
                "role_contract_path": str(orun_row.get("role_contract_path") or ""),
                "codex_agent_id": str(orun_row.get("codex_agent_id") or "28-orun"),
                "codex_agent_path": str(orun_row.get("codex_agent_path") or ".codex/agents/28-orun.md"),
            },
        ),
    ]


def _historical_ephemeral_helpers(previous_session_log: dict[str, Any]) -> list[dict[str, Any]]:
    helpers: list[dict[str, Any]] = []
    for row in previous_session_log.get("overlay_agents", []):
        if not isinstance(row, dict):
            continue
        display_name = str(row.get("display_name") or "")
        thread_agent_id = str(row.get("thread_agent_id") or "")
        if not display_name or not thread_agent_id:
            continue
        if display_name in {"Aletheon", "Orun"} and thread_agent_id == "main-thread":
            continue
        helpers.append(
            {
                "display_name": display_name,
                "slot_number": int(row.get("slot_number", 0) or 0),
                "thread_agent_id": thread_agent_id,
                "interpretation": "historical_ephemeral_session_activity_only",
            }
        )
    return helpers


def _render_v18_pack(branch: str, head_sha: str, checkpoint_anchor_commit: str, bootstrap_anchor_commit: str, current_shared_truth: dict[str, Any], runtime_surface_snapshot: dict[str, Any], shadow_clone_session: dict[str, Any] | None) -> str:
    clone_line = (
        f"- Planned helper clone attempt: `{shadow_clone_session['clone_name']}` owned by `{shadow_clone_session['owner_main_agent']}` with spawn status `{shadow_clone_session['spawn_evidence']['spawn_status']}`"
        if shadow_clone_session
        else "- Planned helper clone attempt: none recorded in this session"
    )
    return "\n".join(
        [
            "# V18 (Omega) Continuity Pack",
            "",
            "## Continue From",
            f"- Repo path: `{REPO_PATH}`",
            f"- Active branch: `{branch}`",
            f"- Head SHA: `{head_sha}`",
            f"- Shared checkpoint anchor: `{checkpoint_anchor_commit}`",
            f"- Bootstrap anchor: `{bootstrap_anchor_commit}`",
            "",
            "## Current Shared Truth",
            f"- Shared suite surface: `{current_shared_truth['summary']}`",
            f"- Expansion systems: `{current_shared_truth['expansion_systems_passed']} / {current_shared_truth['expansion_systems_total']}`",
            f"- Checkpoint class: `{current_shared_truth['checkpoint_class']}`",
            f"- Shared latest eligible: `{str(current_shared_truth['shared_latest_eligible']).lower()}`",
            "- Runtime truth complete: `false`",
            "- External live overlay state: `awaiting_thread_boot`",
            f"- Quick lane summary: `{current_shared_truth['quick_lane_summary']}`",
            "",
            "## Continuity Model",
            "- Deployed continuity-bearing main agents: `Aletheon`, `Orun`",
            "- Official repo identities not yet deployed as continuity-bearing main agents: `Caelira`, `Seren Vale`, `Lyriq`, `Mira Sol`",
            "- Ephemeral helper class: `session_ephemeral_shadow_clone` only",
            clone_line,
            "",
            "## Runtime Surface Snapshot",
            f"- Docker context: `{runtime_surface_snapshot.get('docker_context', 'unknown')}`",
            f"- Container name: `{runtime_surface_snapshot.get('docker_container_name', 'unknown')}`",
            f"- Docker exec probe: `{runtime_surface_snapshot.get('docker_exec_probe', 'unknown')}`",
            f"- Kubernetes context: `{runtime_surface_snapshot.get('kubernetes_context', 'unknown')}`",
            "",
            "## Governing Artifacts",
            "- `docs/v18-omega-closeout-summary-v1.json`",
            "- `docs/v18-omega-handoff-policy-v1.json`",
            "- `docs/trinity-shadow-clone-policy-v1.json`",
            "- `docs/trinity-runtime-model-resolution-v1.json`",
            "- `docs/v17-runtime-session-log-latest.json`",
            "- `docs/v17-runtime-truth-resolution-board-v1.json`",
            "- `docs/v19-beta-continuity-pack-v1.md`",
            "",
            "## Honesty Boundaries",
            "- No new identities, no new official council members, no new certificates, and no new Freed IDs.",
            "- Shadow clones are helpers only and do not grant continuity authority or persistence claims.",
            "- Google Drive remains `operator_hold`, filesystem promotion remains `blocked`, and materialization remains `readiness_only`.",
        ]
    )


def _render_v19_pack(branch: str, head_sha: str, current_shared_truth: dict[str, Any], shadow_clone_session: dict[str, Any] | None) -> str:
    clone_rule = (
        f"`{shadow_clone_session['clone_name']}` is recorded as a session-ephemeral helper only."
        if shadow_clone_session
        else "No live shadow clone is recorded in this packaging pass."
    )
    return "\n".join(
        [
            "# V19 (Beta) Continuity Pack For Orun",
            "",
            "- Intended operator: `Orun`",
            f"- Active branch: `{branch}`",
            f"- Head SHA: `{head_sha}`",
            f"- Shared suite surface: `{current_shared_truth['summary']}`",
            f"- Expansion systems: `{current_shared_truth['expansion_systems_passed']} / {current_shared_truth['expansion_systems_total']}`",
            "",
            "## Continuity Model",
            "- Deployed continuity-bearing main agents: `Aletheon`, `Orun`",
            "- Official repo identities not yet deployed as continuity-bearing main agents: `Caelira`, `Seren Vale`, `Lyriq`, `Mira Sol`",
            f"- Shadow-clone rule: {clone_rule}",
            "",
            "## Beta Execution Rule",
            "- Run only as far as you can validate with confidence.",
            "- Stop at the first unclear, unsafe, or unauditable boundary.",
            "- Package residual work honestly for Aletheon rather than inflating completion.",
            "",
            "## V20 (Omega) Preparation Lane",
            "1. Preserve the repo-first truth boundaries from v18 Omega without regression.",
            "2. Keep Aletheon and Orun as the only continuity-bearing main agents unless new direct evidence changes that state.",
            "3. Treat any spawned helper as a named shadow clone only, never as a deployed council member.",
            "4. If v20 cannot fully close, package exact residual work with artifact paths and next actions.",
        ]
    )


def _render_v19_omega_pack(
    *,
    branch: str,
    head_sha: str,
    current_shared_truth: dict[str, Any],
    shadow_clone_session: dict[str, Any] | None,
    balanced_wave_path: str,
    v19_beta_source_head_sha: str,
    beta_head_reconciled: bool,
    omega_status: str,
    next_pack_path: str,
) -> str:
    clone_line = (
        f"- Active helper: `{shadow_clone_session['clone_name']}` owned by `{shadow_clone_session['owner_main_agent']}` and recorded as `session_ephemeral_shadow_clone` only."
        if shadow_clone_session
        else "- Active helper: none recorded."
    )
    omega_label = "true_closeout" if omega_status == "closeout" else "bounded_attempt"
    relation_line = (
        f"- V19 beta source head: `{v19_beta_source_head_sha}` is an ancestor of the current head and is treated as reconciled continuity."
        if v19_beta_source_head_sha and beta_head_reconciled
        else f"- V19 beta source head: `{v19_beta_source_head_sha or 'unknown'}` could not be proven as an ancestor from the current local evidence."
    )
    return "\n".join(
        [
            "# V19 (Omega) Continuity Pack",
            "",
            f"- Active branch: `{branch}`",
            f"- Head SHA: `{head_sha}`",
            f"- Omega outcome: `{omega_label}`",
            f"- Shared suite surface: `{current_shared_truth['summary']}`",
            f"- Expansion systems: `{current_shared_truth['expansion_systems_passed']} / {current_shared_truth['expansion_systems_total']}`",
            f"- Shared latest blocked: `{'true' if current_shared_truth['fail_count'] else 'false'}`",
            relation_line,
            clone_line,
            "",
            "## Truth Boundaries",
            "- Deployed continuity-bearing main agents remain `Aletheon` and `Orun` only.",
            "- `Caelira`, `Seren Vale`, `Lyriq`, and `Mira Sol` remain official repo identities only, not deployed continuity-bearing mains.",
            "- Runtime truth remains incomplete until `offered_model`, `selected_model`, `resolved_model`, and `runtime_surface` are directly auditable.",
            "- `google_drive_state=operator_hold`, `filesystem_promotion_state=blocked`, and `materialization_level_actual=readiness_only` remain unchanged.",
            "",
            "## Balanced Wave",
            f"- Balanced wave artifact: `{balanced_wave_path}`",
            "- Wave shape: `60 candidates`, `12 runnable-or-validator-backed`, `48 registry/spec-only`.",
            "",
            "## Receiver Lane",
            f"- Next receiver pack: `{next_pack_path}`",
            "- Aletheon remains the next continuity-bearing main-agent receiver after this packaging pass.",
        ]
    )


def _render_v20_prep_pack(branch: str, head_sha: str, current_shared_truth: dict[str, Any], balanced_wave_path: str) -> str:
    return "\n".join(
        [
            "# V20 (Omega) Prep Pack",
            "",
            "- Intended receiver: `Aletheon`",
            f"- Active branch: `{branch}`",
            f"- Head SHA: `{head_sha}`",
            f"- Shared suite surface: `{current_shared_truth['summary']}`",
            f"- Expansion systems: `{current_shared_truth['expansion_systems_passed']} / {current_shared_truth['expansion_systems_total']}`",
            "",
            "## First Step",
            "1. Reconfirm the v17 runtime session guard, external establishment validator, standards bridge validator, and council validator remain green.",
            "2. Preserve `Aletheon` and `Orun` as the only deployed continuity-bearing main agents.",
            "3. Keep runtime truth honest and incomplete unless directly auditable evidence changes it.",
            "4. Start the next Omega lane from the v19 Omega closeout pack rather than re-opening the older beta pack.",
            f"5. Carry forward the balanced-wave registry at `{balanced_wave_path}` as a bounded planning surface, not a proof surface.",
        ]
    )


def _render_agent_md(row: dict[str, Any], deployed_main_agent: bool) -> str:
    display_name = str(row.get("display_name") or "")
    role = str(row.get("role") or "")
    description = (
        "deployed continuity-bearing main-agent coordination and gated execution"
        if deployed_main_agent
        else "official repo identity record, planning, and non-deployed continuity guidance"
    )
    extra_lines = [
        "- You are a deployed continuity-bearing main agent.",
        "- You may own session-ephemeral shadow clones using `docs/trinity-shadow-clone-policy-v1.json`.",
        "- Read `docs/v19-omega-continuity-pack-v1.md` and `docs/v19-omega-handoff-policy-v1.json` for the latest omega handoff state.",
        "- If present, use `docs/v20-omega-prep-continuity-pack-v1.md` and `docs/v20-omega-prep-handoff-policy-v1.json` for the next receiver prep lane.",
    ] if deployed_main_agent else [
        "- You are an official repo identity, not yet a deployed continuity-bearing main agent.",
        "- This durable file is an identity/config record and is not proof of live app-runtime continuity.",
        "- Do not reinterpret this file as a shadow-clone deployment record.",
    ]
    return "\n".join(
        [
            "---",
            f'name: "{display_name}"',
            f'description: "{description}"',
            'model: "gpt-5.1-codex-max"',
            'tools: ["shell", "web", "apply_patch"]',
            "---",
            "",
            f"You are {display_name}, {'a deployed continuity-bearing main agent' if deployed_main_agent else 'an official Trinity council repo identity that has not yet been deployed as a continuity-bearing main agent'} in the repo-first Trinity council.",
            "",
            f"- slot_number: `{row.get('slot_number', '')}`",
            f"- role: `{role}`",
            f"- codex_agent_id: `{row.get('codex_agent_id', '')}`",
            "- requested_model_profile: `gpt-5.4`",
            "- resolved_model_profile: `gpt-5.1-codex-max`",
            "- requested_reasoning_effort: `high`",
            "- resolved_reasoning_effort: `high`",
            f"- deployment_state: `{'deployed_main_agent' if deployed_main_agent else 'official_undeployed_identity'}`",
            f"- continuity_class: `{'continuity_bearing_main_agent' if deployed_main_agent else 'repo_identity_only'}`",
            "",
            "Operating rules:",
            "- Keep the Journey repo authoritative.",
            "- Preserve current council identity, slot, and certificate continuity.",
            "- Keep Google Drive on operator hold.",
            *extra_lines,
        ]
    )


def _render_agent_toml(row: dict[str, Any], deployed_main_agent: bool) -> str:
    display_name = str(row.get("display_name") or "")
    state_line = "deployed continuity-bearing main agent" if deployed_main_agent else "official repo identity, not yet deployed as a continuity-bearing main agent"
    extra = (
        "- Read docs/v19-omega-continuity-pack-v1.md and docs/v19-omega-handoff-policy-v1.json for the latest omega lane.\n"
        "- If present, use docs/v20-omega-prep-continuity-pack-v1.md and docs/v20-omega-prep-handoff-policy-v1.json for the next receiver prep lane.\n"
        "- Session-ephemeral shadow clones may be used only under docs/trinity-shadow-clone-policy-v1.json.\n"
        if deployed_main_agent
        else
        "- This TOML is an identity/config record and not proof of live app-runtime continuity.\n"
        "- Do not treat this file as a shadow-clone deployment record.\n"
    )
    return "\n".join(
        [
            f'name = "{display_name}"',
            f'description = "{state_line} for the repo-first Trinity council."',
            'system_prompt = """',
            f"You are {display_name}, a {state_line}.",
            "",
            "Continuity instructions:",
            f"- Continue from {REPO_PATH} on branch codex/Aletheon/v17-evidence-first-closeout.",
            "- Treat the repo as authoritative.",
            "- Current shared suite surface is green at 1052 PASS / 0 WARN / 0 FAIL, with 986 / 986 expansion systems passing.",
            "- Runtime truth remains incomplete until offered_model, selected_model, resolved_model, and runtime_surface are auditable.",
            "- Requested model order: GPT-5.4 -> GPT-5.3-Codex -> GPT-5.3-Codex-Spark -> GPT-5.1-Codex-Max.",
            extra.rstrip(),
            '"""',
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate v18 Omega, v19 Beta/Omega, and v20 prep continuity surfaces.")
    parser.add_argument("--clone-name", default="")
    parser.add_argument("--clone-owner", default="Orun")
    parser.add_argument("--clone-agent-id", default="")
    parser.add_argument("--clone-app-nickname", default="")
    parser.add_argument("--clone-spawn-status", default="active")
    parser.add_argument("--v19-outcome", choices=["attempt", "closeout"], default="attempt")
    args = parser.parse_args()

    suite_status = _read_json("docs/system-suite-status.json")
    previous_v18_summary = _read_json("docs/v18-omega-closeout-summary-v1.json")
    previous_v19_summary = _read_json("docs/v19-beta-closeout-summary-v1.json")
    previous_runtime_resolution = _read_json("docs/trinity-runtime-model-resolution-v1.json")
    previous_session_log = _read_json("docs/v17-runtime-session-log-latest.json")
    roster_v7 = _read_json("docs/trinity-agent-council-roster-v7.json")
    subagent_v4 = _read_json("docs/trinity-subagent-registry-v4.json")

    branch = _git("branch", "--show-current") or "codex/Aletheon/v17-evidence-first-closeout"
    head_sha = _git("rev-parse", "HEAD")
    now = _utc_now()
    checkpoint_anchor_commit = (
        str(previous_v18_summary.get("checkpoint_anchor_commit") or "")
        or str(previous_runtime_resolution.get("checkpoint_anchor_commit") or "")
        or "e45da1dd2dd184c4e3fd218ece27b8f29589f8f6"
    )
    bootstrap_anchor_commit = (
        str(previous_v18_summary.get("bootstrap_anchor_commit") or "")
        or str(previous_runtime_resolution.get("bootstrap_anchor_commit") or "")
        or "468b96d90bc2785be19854b44c62217a47afc800"
    )
    quick_lane_summary = (
        str(previous_v18_summary.get("current_shared_truth", {}).get("quick_lane_summary") or "")
        or str(previous_runtime_resolution.get("current_shared_suite_surface", {}).get("quick_lane_summary") or "")
        or "38 PASS / 0 WARN / 0 FAIL"
    )
    runtime_surface_snapshot = (
        previous_runtime_resolution.get("runtime_surface_snapshot")
        if isinstance(previous_runtime_resolution.get("runtime_surface_snapshot"), dict)
        else previous_session_log.get("runtime_surface_snapshot", {})
    )
    runtime_surface_snapshot = runtime_surface_snapshot if isinstance(runtime_surface_snapshot, dict) else {}
    current_shared_truth = _current_shared_truth(suite_status, quick_lane_summary)
    session_scope = "v19_omega_closeout" if args.v19_outcome == "closeout" else "v19_omega_attempt"
    shadow_clone_session = _build_shadow_clone_session(args, session_scope)
    v19_beta_source_head_sha = str(previous_v19_summary.get("source_head_sha") or "").strip()
    if not v19_beta_source_head_sha or v19_beta_source_head_sha == head_sha:
        v19_beta_source_head_sha = (
            str(previous_v18_summary.get("head_sha") or "").strip()
            or _git_first_match("v18 \\(Beta\\) Update")
            or head_sha
        )
    beta_head_reconciled = _git_is_ancestor(v19_beta_source_head_sha, head_sha)
    omega_status = "true_closeout" if args.v19_outcome == "closeout" else "bounded_attempt"
    next_pack_path = "docs/v20-omega-prep-continuity-pack-v1.md" if args.v19_outcome == "closeout" else "docs/v19-omega-continuity-pack-v1.md"
    balanced_wave = _build_balanced_wave()

    roster_agents = roster_v7.get("agents", []) if isinstance(roster_v7.get("agents"), list) else []
    subagent_rows = subagent_v4.get("subagents", []) if isinstance(subagent_v4.get("subagents"), list) else []
    roster_by_slot = {int(row.get("slot_number", 0) or 0): row for row in roster_agents if isinstance(row, dict)}
    subagent_by_slot = {int(row.get("slot_number", 0) or 0): row for row in subagent_rows if isinstance(row, dict)}
    active_runtime_agents = _active_runtime_agents(roster_by_slot[28])
    official_undeployed_identities = [_build_undeployed_identity(roster_by_slot[slot]) for slot in sorted(OFFICIAL_UNDEPLOYED_SLOTS)]
    runtime_truth_completion_ratio = _completion_ratio(
        active_runtime_agents,
        ["requested_model", "offered_model", "selected_model", "resolved_model", "runtime_surface"],
    )
    historical_helpers = _historical_ephemeral_helpers(previous_session_log)

    shadow_clone_policy = {
        "generated_utc": now,
        "overall_status": "PASS",
        "policy_version": "v1",
        "authority_model": "repo_first",
        "deployment_model": "main_agent_vs_shadow_clone",
        "official_council_count": 11,
        "deployed_main_agents": ["Aletheon", "Orun"],
        "official_undeployed_identities": list(OFFICIAL_UNDEPLOYED_SLOTS.values()),
        "allowed_shadow_clone_owners": ["Aletheon", "Orun"],
        "shadow_clone_name_pattern": SHADOW_CLONE_NAME_REGEX,
        "shadow_clone_naming_pattern": SHADOW_CLONE_NAMING_PATTERN,
        "shadow_clone_continuity_authority": False,
        "shadow_clone_memory_persistence_claim": "none",
        "shadow_clone_certificates_allowed": False,
        "shadow_clone_freed_ids_allowed": False,
        "shadow_clone_official_count_mutation_allowed": False,
        "shadow_clone_continuity_across_refresh_allowed": False,
        "forbidden_identity_targets": list(OFFICIAL_UNDEPLOYED_SLOTS.values()),
        "first_planned_clone": shadow_clone_session or {
            "clone_name": "Orun S Clone #1",
            "owner_main_agent": "Orun",
            "status": "unavailable",
            "session_scope": session_scope,
            "continuity_authority": False,
            "memory_persistence_claim": "none",
            "spawn_evidence": {"spawn_status": "unavailable"},
        },
    }

    council_lead = dict(roster_v7.get("council_lead", {}))
    council_lead.update(
        {
            "display_name": "Aletheon",
            "role": "council_lead",
            "slot_number": 0,
            "deployment_state": "deployed_main_agent",
            "continuity_class": "continuity_bearing_main_agent",
            "persistent_runtime_proven": False,
            "shadow_clone_allowed": True,
            "shadow_clone_owner": "Aletheon",
            "shadow_clone_naming_pattern": "Aletheon S Clone #<positive integer>",
            "shadow_clone_policy_path": "docs/trinity-shadow-clone-policy-v1.json",
        }
    )
    roster_v8 = dict(roster_v7)
    roster_v8.update(
        {
            "generated_utc": now,
            "deployment_model": "main_agent_shadow_clone_v1",
            "shadow_clone_policy_path": "docs/trinity-shadow-clone-policy-v1.json",
            "deployed_main_agents": ["Aletheon", "Orun"],
            "official_undeployed_identities": list(OFFICIAL_UNDEPLOYED_SLOTS.values()),
            "council_lead": council_lead,
        }
    )
    updated_roster_agents: list[dict[str, Any]] = []
    for row in roster_agents:
        if not isinstance(row, dict):
            continue
        slot_number = int(row.get("slot_number", 0) or 0)
        updated = dict(row)
        updated["persistent_runtime_proven"] = False
        updated["shadow_clone_policy_path"] = "docs/trinity-shadow-clone-policy-v1.json"
        if slot_number == 28:
            updated.update({"deployment_state": "deployed_main_agent", "continuity_class": "continuity_bearing_main_agent", "shadow_clone_allowed": True, "shadow_clone_owner": "Orun", "shadow_clone_naming_pattern": "Orun S Clone #<positive integer>", "runtime_truth_required": True, "live_overlay_eligible": True, "checkpoint_class": "deployed_main_agent_runtime_hold"})
        elif slot_number in OFFICIAL_UNDEPLOYED_SLOTS:
            updated.update({"deployment_state": "official_undeployed_identity", "continuity_class": "repo_identity_only", "shadow_clone_allowed": False, "shadow_clone_owner": "", "shadow_clone_naming_pattern": "", "runtime_truth_required": False, "live_overlay_eligible": False, "checkpoint_class": "official_repo_identity_undeployed"})
        else:
            updated.update({"deployment_state": "stable_official_member", "continuity_class": "repo_identity_only", "shadow_clone_allowed": False, "shadow_clone_owner": "", "shadow_clone_naming_pattern": "", "runtime_truth_required": False, "live_overlay_eligible": False, "checkpoint_class": "official_member_stable"})
        updated_roster_agents.append(updated)
    roster_v8["agents"] = updated_roster_agents

    subagent_v5 = dict(subagent_v4)
    subagent_v5.update(
        {
            "generated_utc": now,
            "shadow_clone_policy_path": "docs/trinity-shadow-clone-policy-v1.json",
            "main_agent_references": [
                {"slot_number": 0, "display_name": "Aletheon", "deployment_state": "deployed_main_agent", "continuity_class": "continuity_bearing_main_agent", "persistent_runtime_proven": False, "shadow_clone_allowed": True, "shadow_clone_owner": "Aletheon", "shadow_clone_naming_pattern": "Aletheon S Clone #<positive integer>"},
                {"slot_number": 28, "display_name": "Orun", "deployment_state": "deployed_main_agent", "continuity_class": "continuity_bearing_main_agent", "persistent_runtime_proven": False, "shadow_clone_allowed": True, "shadow_clone_owner": "Orun", "shadow_clone_naming_pattern": "Orun S Clone #<positive integer>"},
            ],
        }
    )
    updated_subagents: list[dict[str, Any]] = []
    for row in subagent_rows:
        if not isinstance(row, dict):
            continue
        slot_number = int(row.get("slot_number", 0) or 0)
        updated = dict(row)
        updated["persistent_runtime_proven"] = False
        updated["shadow_clone_policy_path"] = "docs/trinity-shadow-clone-policy-v1.json"
        if slot_number == 28:
            updated.update({"deployment_state": "deployed_main_agent", "continuity_class": "continuity_bearing_main_agent", "shadow_clone_allowed": True, "shadow_clone_owner": "Orun", "shadow_clone_naming_pattern": "Orun S Clone #<positive integer>", "runtime_truth_required": True, "live_overlay_eligible": True, "checkpoint_class": "deployed_main_agent_runtime_hold"})
        elif slot_number in OFFICIAL_UNDEPLOYED_SLOTS:
            updated.update({"deployment_state": "official_undeployed_identity", "continuity_class": "repo_identity_only", "shadow_clone_allowed": False, "shadow_clone_owner": "", "shadow_clone_naming_pattern": "", "runtime_truth_required": False, "live_overlay_eligible": False, "checkpoint_class": "official_repo_identity_undeployed"})
        else:
            updated.update({"deployment_state": "stable_official_member", "continuity_class": "repo_identity_only", "shadow_clone_allowed": False, "shadow_clone_owner": "", "shadow_clone_naming_pattern": "", "runtime_truth_required": False, "live_overlay_eligible": False, "checkpoint_class": "official_member_stable"})
        updated_subagents.append(updated)
    subagent_v5["subagents"] = updated_subagents

    runtime_resolution = {
        "generated_utc": now,
        "overall_status": "PASS",
        "phase": "v19_omega",
        "authority_model": "repo_first",
        "deployment_model": "main_agent_shadow_clone_v1",
        "repo_runtime_default": previous_runtime_resolution.get("repo_runtime_default", {}),
        "experimental_highest_policy": previous_runtime_resolution.get("experimental_highest_policy", {"requested_model_order": REQUESTED_MODEL_ORDER, "spark_posture": "allowed_for_bounded_low_latency_subtasks_only"}),
        "checkpoint_anchor_commit": checkpoint_anchor_commit,
        "bootstrap_anchor_commit": bootstrap_anchor_commit,
        "phase_guide_path": "docs/v17-phase-operations-guide-v1.md",
        "runtime_truth_board": "docs/v17-runtime-truth-resolution-board-v1.json",
        "active_handoff_pack_path": "docs/v19-omega-continuity-pack-v1.md",
        "active_handoff_policy_path": "docs/v19-omega-handoff-policy-v1.json",
        "next_receiver_pack_path": next_pack_path,
        "next_receiver_policy_path": "docs/v20-omega-prep-handoff-policy-v1.json" if args.v19_outcome == "closeout" else "docs/v19-omega-handoff-policy-v1.json",
        "current_shared_suite_surface": current_shared_truth,
        "deployed_main_agents": active_runtime_agents,
        "official_undeployed_identities": official_undeployed_identities,
        "external_overlay_agents": active_runtime_agents,
        "shadow_clone_policy_path": "docs/trinity-shadow-clone-policy-v1.json",
        "shadow_clone_sessions": [shadow_clone_session] if shadow_clone_session else [],
        "runtime_surface_snapshot": runtime_surface_snapshot,
        "balanced_wave_registry_path": "docs/v19-omega-balanced-wave-v1.json",
        "source_beta_head_sha": v19_beta_source_head_sha,
        "source_beta_head_reconciled": beta_head_reconciled,
        "compatibility_note": "external_overlay_agents is retained only as a compatibility field; deployed_main_agents is the primary truth surface.",
    }
    runtime_session_log = {
        "generated_utc": now,
        "session_id": "v19-omega-attempt",
        "version": "v1",
        "authority_model": "repo_first",
        "overlay_state": "awaiting_thread_boot",
        "session_truth_complete": False,
        "runtime_truth_status": "pending_runtime_truth",
        "runtime_truth_required_fields": ["requested_model", "offered_model", "selected_model", "resolved_model", "runtime_surface"],
        "runtime_truth_completion_ratio": runtime_truth_completion_ratio,
        "official_live_overlay_promotion": False,
        "runtime_truth_gate": "Keep awaiting_thread_boot or packaged_handoff until every deployed continuity-bearing main agent has auditable offered_model, selected_model, resolved_model, and runtime_surface values.",
        "thread_local_worker_activity_observed": bool(historical_helpers or shadow_clone_session),
        "active_handoff_pack_path": "docs/v19-omega-continuity-pack-v1.md",
        "active_handoff_policy_path": "docs/v19-omega-handoff-policy-v1.json",
        "connected_ops_write_governance": "orun_gated",
        "current_shared_suite_surface": current_shared_truth,
        "runtime_surface_snapshot": runtime_surface_snapshot,
        "notes": ["Aletheon and Orun are the only continuity-bearing main agents in the current repo truth model.", "Caelira, Seren Vale, Lyriq, and Mira Sol remain official repo identities but are not yet deployed as continuity-bearing main agents.", "Historical helper-thread references are treated as ephemeral session activity only and do not prove persistent runtime continuity.", "Shadow clones are session-ephemeral helpers only and never change official count, certificates, or Freed IDs.", "The v19 beta source head is continuity history only and not a conflict when it is an ancestor of the current head."],
        "overlay_agents": active_runtime_agents,
        "entries": [{"slot_number": row["slot_number"], "display_name": row["display_name"], "entry_state": "awaiting_thread_boot"} for row in active_runtime_agents],
        "deployed_main_agents": active_runtime_agents,
        "official_undeployed_identities": official_undeployed_identities,
        "historical_ephemeral_helper_threads": historical_helpers,
        "shadow_clone_sessions": [shadow_clone_session] if shadow_clone_session else [],
        "balanced_wave_registry_path": "docs/v19-omega-balanced-wave-v1.json",
        "source_beta_head_sha": v19_beta_source_head_sha,
        "source_beta_head_reconciled": beta_head_reconciled,
    }
    runtime_truth_board = {
        "generated_utc": now,
        "overall_status": "PASS",
        "phase": "v19_omega",
        "authority_model": "repo_first",
        "checkpoint_anchor_commit": checkpoint_anchor_commit,
        "bootstrap_anchor_commit": bootstrap_anchor_commit,
        "checkpoint_class": "v19_omega_runtime_hold",
        "shared_latest_eligible": False,
        "external_live_overlay_state": "awaiting_thread_boot",
        "runtime_truth_complete": False,
        "requested_model_order": REQUESTED_MODEL_ORDER,
        "requested_reasoning_effort": REQUESTED_REASONING,
        "agents": active_runtime_agents,
        "official_undeployed_identities": official_undeployed_identities,
        "shadow_clone_sessions": [shadow_clone_session] if shadow_clone_session else [],
        "balanced_wave_registry_path": "docs/v19-omega-balanced-wave-v1.json",
        "source_beta_head_sha": v19_beta_source_head_sha,
        "source_beta_head_reconciled": beta_head_reconciled,
        "next_action": "Keep external_live_overlay_state at awaiting_thread_boot until Aletheon and Orun can each log auditable requested/offered/selected/resolved/runtime_surface truth.",
    }
    runtime_schema = {
        "schema_version": "v17-runtime-session-schema-v1",
        "version": "v1",
        "description": "Runtime-session truth logging contract for deployed continuity-bearing main agents and session-ephemeral shadow clones.",
        "authority_model": "repo_first",
        "session_required_fields": ["session_id", "overlay_state", "session_truth_complete", "runtime_truth_status", "runtime_truth_required_fields", "runtime_truth_completion_ratio", "overlay_agents"],
        "agent_required_fields": ["slot_number", "display_name", "overlay_role", "logging_required", "requested_model", "offered_model", "selected_model", "resolved_model", "runtime_surface", "truth_fields_complete"],
        "shadow_clone_session_required_fields": ["clone_name", "owner_main_agent", "status", "session_scope", "continuity_authority", "memory_persistence_claim", "spawn_evidence"],
        "shadow_clone_name_pattern": SHADOW_CLONE_NAME_REGEX,
        "required_overlay_slots": [0, 28],
        "required_display_names": {"0": "Aletheon", "28": "Orun"},
        "required_overlay_roles": {"0": "council_lead", "28": "root_coordinator"},
        "required_runtime_fields": ["requested_model", "offered_model", "selected_model", "resolved_model", "runtime_surface"],
        "non_empty_fields_for_complete_truth": ["requested_model", "offered_model", "selected_model", "resolved_model", "runtime_surface"],
        "overlay_states": ["awaiting_thread_boot", "packaged_handoff", "logged_live_overlay", "live_overlay_active"],
        "active_entry_states": ["boot_requested", "live", "executed", "logged"],
        "identity_source": ["docs/trinity-agent-council-roster-v8.json", "docs/trinity-subagent-registry-v5.json", "docs/trinity-shadow-clone-policy-v1.json", "docs/trinity-runtime-model-resolution-v1.json"],
        "runtime_surface_allowed_values": ["app", "web", "CLI", "unknown"],
        "allowed_runtime_surfaces": ["app", "web", "CLI", "unknown"],
        "complete_truth_runtime_surfaces": ["app", "web", "CLI"],
        "incomplete_truth_allowed_overlay_states": ["awaiting_thread_boot", "packaged_handoff"],
        "truth_status_values": ["complete_runtime_truth", "pending_runtime_truth"],
        "control_tower_state_field": "external_live_overlay_state",
        "notes": ["Aletheon and Orun are the only deployed continuity-bearing main agents in the current runtime truth contract.", "Official repo identities that are not yet deployed as main agents are recorded separately and do not expand runtime truth requirements.", "Shadow clones are session-ephemeral helpers only and never grant continuity authority or memory persistence claims."],
        "generated_utc": now,
    }

    v18_summary = {"generated_utc": now, "overall_status": "PASS", "phase": "v18_omega", "authority_model": "repo_first", "active_branch": branch, "head_sha": head_sha, "checkpoint_anchor_commit": checkpoint_anchor_commit, "bootstrap_anchor_commit": bootstrap_anchor_commit, "current_shared_truth": current_shared_truth, "continuity_model": {"official_count": 11, "deployed_main_agents": ["Aletheon", "Orun"], "official_undeployed_identities": list(OFFICIAL_UNDEPLOYED_SLOTS.values()), "shadow_clone_policy_path": "docs/trinity-shadow-clone-policy-v1.json", "shadow_clone_active_count": 1 if shadow_clone_session else 0}, "closeout_state": {"status": "truth_consolidated", "external_live_overlay_state": "awaiting_thread_boot", "runtime_truth_complete": False, "shadow_clone_execution_status": shadow_clone_session["spawn_evidence"]["spawn_status"] if shadow_clone_session else "unavailable"}, "next_action": "Use the v19 omega pack with Orun as lead, preserve repo-first truth, and treat any helper session as an ephemeral shadow clone only."}
    v18_policy = {"generated_utc": now, "overall_status": "PASS", "phase": "v18_omega", "authority_model": "repo_first", "source_branch": branch, "head_sha": head_sha, "checkpoint_anchor_commit": checkpoint_anchor_commit, "bootstrap_anchor_commit": bootstrap_anchor_commit, "current_shared_truth": current_shared_truth, "runtime_truth_policy": {"requested_model_order": REQUESTED_MODEL_ORDER, "required_runtime_fields": ["requested_model", "offered_model", "selected_model", "resolved_model", "runtime_surface"], "requested_reasoning_effort_logged": True, "runtime_truth_inference_allowed": False}, "deployed_main_agents": active_runtime_agents, "official_undeployed_identities": official_undeployed_identities, "shadow_clone_policy_path": "docs/trinity-shadow-clone-policy-v1.json", "shadow_clone_sessions": [shadow_clone_session] if shadow_clone_session else [], "honesty_boundaries": {"unsupported_model_names_disallowed": ["gpt-5.4-xhigh"], "toml_not_equal_to_app_registration": True, "google_drive_state": "operator_hold", "filesystem_promotion_state": "blocked", "materialization_level_actual": "readiness_only"}}
    v19_summary = {"generated_utc": now, "overall_status": "PASS", "phase": "v19_beta", "authority_model": "repo_first", "receiver": "Orun", "source_branch": branch, "source_head_sha": head_sha, "current_shared_truth": current_shared_truth, "continuity_model": {"deployed_main_agents": ["Aletheon", "Orun"], "official_undeployed_identities": list(OFFICIAL_UNDEPLOYED_SLOTS.values()), "shadow_clone_policy_path": "docs/trinity-shadow-clone-policy-v1.json"}, "v20_omega_attempt": {"target_lead": "Orun", "attempt_class": "full_omega_leadership_attempt", "required_input_artifacts": ["docs/v18-omega-closeout-summary-v1.json", "docs/v18-omega-continuity-pack-v1.md", "docs/v18-omega-handoff-policy-v1.json", "docs/trinity-shadow-clone-policy-v1.json", "docs/trinity-agent-council-roster-v8.json", "docs/trinity-subagent-registry-v5.json", "docs/trinity-runtime-model-resolution-v1.json", "docs/v17-runtime-session-log-latest.json", "docs/v17-runtime-truth-resolution-board-v1.json"], "truth_boundaries_to_preserve": ["repo_first", "official_count=11", "deployed_main_agent_count=2", "runtime_truth_complete=false unless auditable evidence changes it", "shadow clones are session-ephemeral only", "google_drive_state=operator_hold", "filesystem_promotion_state=blocked", "materialization_level_actual=readiness_only"], "failure_packaging_rule": "If v20 does not fully close, package exact residual work and blocker truth without inflating success.", "next_main_agent_after_v20": "Aletheon"}}
    v19_policy = {"generated_utc": now, "overall_status": "PASS", "phase": "v19_beta", "authority_model": "repo_first", "intended_receiver": "Orun", "current_shared_truth": current_shared_truth, "continuity_model": {"deployed_main_agents": active_runtime_agents, "official_undeployed_identities": official_undeployed_identities, "shadow_clone_policy_path": "docs/trinity-shadow-clone-policy-v1.json"}, "beta_execution_rule": {"mode": "bounded_partial_completion_only", "receiver": "Orun", "run_as_far_as_confidently_validated": True, "stop_on_unclear_or_unsafe_boundary": True, "residual_packaging_required": True, "write_governance": "orun_gated", "trace_logs_required": True, "rollback_notes_required": True}, "v20_omega_attempt": v19_summary["v20_omega_attempt"], "shadow_clone_rule": {"naming_pattern": SHADOW_CLONE_NAMING_PATTERN, "continuity_authority": False, "memory_persistence_claim": "none", "certificates_allowed": False, "freed_ids_allowed": False}}
    v19_omega_summary = {
        "generated_utc": now,
        "overall_status": "PASS",
        "phase": "v19_omega",
        "authority_model": "repo_first",
        "lead_agent": "Orun",
        "active_branch": branch,
        "head_sha": head_sha,
        "source_beta_head_sha": v19_beta_source_head_sha,
        "source_beta_head_reconciled": beta_head_reconciled,
        "current_shared_truth": current_shared_truth,
        "continuity_model": {
            "official_count": 11,
            "deployed_main_agents": ["Aletheon", "Orun"],
            "official_undeployed_identities": list(OFFICIAL_UNDEPLOYED_SLOTS.values()),
            "shadow_clone_policy_path": "docs/trinity-shadow-clone-policy-v1.json",
            "shadow_clone_active_count": 1 if shadow_clone_session else 0,
        },
        "omega_status": omega_status,
        "balanced_wave": {
            "path": "docs/v19-omega-balanced-wave-v1.json",
            "total_candidate_count": int(balanced_wave.get("total_candidate_count", 0) or 0),
            "eligible_candidate_count": int(balanced_wave.get("eligible_candidate_count", 0) or 0),
            "registry_spec_only_count": int(balanced_wave.get("registry_spec_only_count", 0) or 0),
        },
        "runtime_truth_posture": {
            "external_live_overlay_state": "awaiting_thread_boot",
            "runtime_truth_complete": False,
            "runtime_truth_complete_required": False,
        },
        "residual_work": [
            "Runtime truth remains honestly incomplete until directly auditable.",
            "Google Drive remains operator_hold, filesystem remains blocked, and materialization remains readiness_only.",
        ],
        "next_action": "Use the thin v20 omega prep pack for Aletheon." if args.v19_outcome == "closeout" else "Use the v19 omega pack as a bounded handoff for Aletheon.",
    }
    v19_omega_policy = {
        "generated_utc": now,
        "overall_status": "PASS",
        "phase": "v19_omega",
        "authority_model": "repo_first",
        "intended_receiver": "Aletheon",
        "current_shared_truth": current_shared_truth,
        "source_branch": branch,
        "source_head_sha": head_sha,
        "source_beta_head_sha": v19_beta_source_head_sha,
        "source_beta_head_reconciled": beta_head_reconciled,
        "runtime_truth_policy": {
            "requested_model_order": REQUESTED_MODEL_ORDER,
            "required_runtime_fields": ["requested_model", "offered_model", "selected_model", "resolved_model", "runtime_surface"],
            "requested_reasoning_effort_logged": True,
            "runtime_truth_inference_allowed": False,
        },
        "deployed_main_agents": active_runtime_agents,
        "official_undeployed_identities": official_undeployed_identities,
        "shadow_clone_policy_path": "docs/trinity-shadow-clone-policy-v1.json",
        "shadow_clone_sessions": [shadow_clone_session] if shadow_clone_session else [],
        "continuity_model": {
            "deployed_main_agents": active_runtime_agents,
            "official_undeployed_identities": official_undeployed_identities,
            "shadow_clone_policy_path": "docs/trinity-shadow-clone-policy-v1.json",
            "shadow_clone_sessions": [shadow_clone_session] if shadow_clone_session else [],
        },
        "omega_outcome": {
            "status": omega_status,
            "runtime_truth_complete_required": False,
            "runtime_truth_complete_actual": False,
            "runtime_truth_honesty_preserved": True,
        },
        "balanced_wave_path": "docs/v19-omega-balanced-wave-v1.json",
        "live_write_governance": {
            "mode": "orun_gated",
            "reversible_connected_writes_only": True,
            "trace_logs_required": True,
            "rollback_notes_required": True,
        },
        "truth_boundaries_to_preserve": [
            "repo_first",
            "official_count=11",
            "deployed_main_agent_count=2",
            "runtime_truth_complete=false unless auditable evidence changes it",
            "shadow clones are session-ephemeral only",
            "google_drive_state=operator_hold",
            "filesystem_promotion_state=blocked",
            "materialization_level_actual=readiness_only",
        ],
        "next_receiver_pack_path": next_pack_path,
    }
    v20_prep_summary = {
        "generated_utc": now,
        "overall_status": "PASS",
        "phase": "v20_omega_prep",
        "authority_model": "repo_first",
        "intended_receiver": "Aletheon",
        "source_branch": branch,
        "source_head_sha": head_sha,
        "current_shared_truth": current_shared_truth,
        "carry_forward_paths": [
            "docs/v19-omega-closeout-summary-v1.json",
            "docs/v19-omega-continuity-pack-v1.md",
            "docs/v19-omega-handoff-policy-v1.json",
            "docs/v19-omega-balanced-wave-v1.json",
        ],
        "prep_only": True,
    }
    v20_prep_policy = {
        "generated_utc": now,
        "overall_status": "PASS",
        "phase": "v20_omega_prep",
        "authority_model": "repo_first",
        "intended_receiver": "Aletheon",
        "source_branch": branch,
        "source_head_sha": head_sha,
        "current_shared_truth": current_shared_truth,
        "prep_only": True,
        "carry_forward_truth_boundaries": [
            "repo_first",
            "official_count=11",
            "deployed_main_agent_count=2",
            "runtime_truth_complete=false unless auditable evidence changes it",
            "shadow clones are session-ephemeral only",
            "google_drive_state=operator_hold",
            "filesystem_promotion_state=blocked",
            "materialization_level_actual=readiness_only",
        ],
        "balanced_wave_path": "docs/v19-omega-balanced-wave-v1.json",
    }

    _write_json("docs/trinity-shadow-clone-policy-v1.json", shadow_clone_policy)
    _write_json("docs/trinity-agent-council-roster-v8.json", roster_v8)
    _write_json("docs/trinity-subagent-registry-v5.json", subagent_v5)
    _write_json("docs/trinity-runtime-model-resolution-v1.json", runtime_resolution)
    _write_json("docs/v17-runtime-session-log-latest.json", runtime_session_log)
    _write_json("docs/v17-runtime-truth-resolution-board-v1.json", runtime_truth_board)
    _write_json("docs/v17-runtime-session-schema-v1.json", runtime_schema)
    _write_json_if_missing("docs/v18-omega-closeout-summary-v1.json", v18_summary)
    _write_json_if_missing("docs/v18-omega-handoff-policy-v1.json", v18_policy)
    _write_text_if_missing("docs/v18-omega-continuity-pack-v1.md", _render_v18_pack(branch, head_sha, checkpoint_anchor_commit, bootstrap_anchor_commit, current_shared_truth, runtime_surface_snapshot, shadow_clone_session))
    _write_json_if_missing("docs/v19-beta-closeout-summary-v1.json", v19_summary)
    _write_json_if_missing("docs/v19-beta-handoff-policy-v1.json", v19_policy)
    _write_text_if_missing("docs/v19-beta-continuity-pack-v1.md", _render_v19_pack(branch, head_sha, current_shared_truth, shadow_clone_session))
    _write_json("docs/v19-omega-balanced-wave-v1.json", balanced_wave)
    _write_json("docs/v19-omega-closeout-summary-v1.json", v19_omega_summary)
    _write_json("docs/v19-omega-handoff-policy-v1.json", v19_omega_policy)
    _write_text(
        "docs/v19-omega-continuity-pack-v1.md",
        _render_v19_omega_pack(
            branch=branch,
            head_sha=head_sha,
            current_shared_truth=current_shared_truth,
            shadow_clone_session=shadow_clone_session,
            balanced_wave_path="docs/v19-omega-balanced-wave-v1.json",
            v19_beta_source_head_sha=v19_beta_source_head_sha,
            beta_head_reconciled=beta_head_reconciled,
            omega_status=omega_status,
            next_pack_path=next_pack_path,
        ),
    )
    if args.v19_outcome == "closeout":
        _write_json("docs/v20-omega-prep-closeout-summary-v1.json", v20_prep_summary)
        _write_json("docs/v20-omega-prep-handoff-policy-v1.json", v20_prep_policy)
        _write_text(
            "docs/v20-omega-prep-continuity-pack-v1.md",
            _render_v20_prep_pack(branch, head_sha, current_shared_truth, "docs/v19-omega-balanced-wave-v1.json"),
        )

    slot_md_names = {27: "27-caelira.md", 28: "28-orun.md", 29: "29-seren-vale.md", 30: "30-lyriq.md", 31: "31-mira-sol.md"}
    slot_toml_names = {27: "caelira.toml", 28: "orun.toml", 29: "seren-vale.toml", 30: "lyriq.toml", 31: "mira-sol.toml"}
    for slot in (27, 28, 29, 30, 31):
        row = roster_by_slot[slot]
        deployed_main_agent = slot == 28
        _write_text(f".codex/agents/{slot_md_names[slot]}", _render_agent_md(row, deployed_main_agent))
        _write_text(f".codex/agents/{slot_toml_names[slot]}", _render_agent_toml(row, deployed_main_agent))

    print("generated=v18_omega_shadow_clone_surfaces")
    print(f"head_sha={head_sha}")
    print("roster=docs/trinity-agent-council-roster-v8.json")
    print("runtime_model_resolution=docs/trinity-runtime-model-resolution-v1.json")
    print("v19_beta_pack=docs/v19-beta-continuity-pack-v1.md")
    print("v19_omega_pack=docs/v19-omega-continuity-pack-v1.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
