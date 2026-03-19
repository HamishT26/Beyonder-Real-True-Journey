#!/usr/bin/env python3
"""Generate the v17 evidence-first closeout surface."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import generate_v16_surface as v16

v15 = v16.v15
ROOT = v15.ROOT

BASELINE_COMMIT = "e45da1dd2dd184c4e3fd218ece27b8f29589f8f6"
BOOTSTRAP_COMMIT = "468b96d90bc2785be19854b44c62217a47afc800"

OLD_MANIFEST = ROOT / "docs" / "trinity-expansion-system-manifest-v16.json"
NEW_MANIFEST = ROOT / "docs" / "trinity-expansion-system-manifest-v17.json"
OLD_EXTENSION_CATALOG = ROOT / "docs" / "trinity-extension-catalog-v14.json"
NEW_EXTENSION_CATALOG = ROOT / "docs" / "trinity-extension-catalog-v15.json"
OLD_COMMAND_BOOK = ROOT / "docs" / "trinity-command-book-v10.json"
NEW_COMMAND_BOOK = ROOT / "docs" / "trinity-command-book-v11.json"
OLD_API_BOOK = ROOT / "docs" / "trinity-api-book-v5.json"
NEW_API_BOOK = ROOT / "docs" / "trinity-api-book-v6.json"
OLD_ROSTER = ROOT / "docs" / "trinity-agent-council-roster-v6.json"
NEW_ROSTER = ROOT / "docs" / "trinity-agent-council-roster-v7.json"
OLD_SUBAGENT_REGISTRY = ROOT / "docs" / "trinity-subagent-registry-v3.json"
NEW_SUBAGENT_REGISTRY = ROOT / "docs" / "trinity-subagent-registry-v4.json"
STATUS_JSON = ROOT / "docs" / "system-suite-status.json"
BASELINE_STATE = ROOT / "docs" / "v17-baseline-state-v1.json"
RUNTIME_SCHEMA = ROOT / "docs" / "v17-runtime-session-schema-v1.json"
RUNTIME_LOG = ROOT / "docs" / "v17-runtime-session-log-latest.json"
RUNTIME_BOARD = ROOT / "docs" / "v17-runtime-truth-resolution-board-v1.json"
MODEL_RESOLUTION = ROOT / "docs" / "trinity-runtime-model-resolution-v1.json"
CRITERIA_BOARD = ROOT / "docs" / "v17-external-establishment-criteria-board-v1.json"
CLOSEOUT_SUMMARY = ROOT / "docs" / "v17-closeout-summary-v1.json"
PHASE_GUIDE = ROOT / "docs" / "v17-phase-operations-guide-v1.md"
CONTINUITY_PROMPT = ROOT / "docs" / "v17-continuity-prompt-v1.md"
WAKE_LOG = ROOT / "docs" / "logs" / "system-wake-v17.json"
MIND_BRIEF = ROOT / "docs" / "v17-mind-evidence-refresh.md"
BODY_BRIEF = ROOT / "docs" / "v17-body-runtime-readiness.md"
HEART_BRIEF = ROOT / "docs" / "v17-heart-standards-alignment.md"

REQUESTED_MODEL_ORDER = v16.REQUESTED_MODEL_ORDER
REQUESTED_REASONING = v16.REQUESTED_REASONING
MAX_THREADS = v16.MAX_THREADS
SUFFIXES = v16.SUFFIXES
OVERLAY = v16.OVERLAY

REFS = {
    "trinity-expansion-system-manifest-v16.json": "trinity-expansion-system-manifest-v17.json",
    "trinity-extension-catalog-v14.json": "trinity-extension-catalog-v15.json",
    "trinity-command-book-v10.json": "trinity-command-book-v11.json",
    "trinity-api-book-v5.json": "trinity-api-book-v6.json",
    "trinity-agent-council-roster-v6.json": "trinity-agent-council-roster-v7.json",
    "trinity-subagent-registry-v3.json": "trinity-subagent-registry-v4.json",
}

PACKS = [
    ("baseline_restore_governor_v17", "Baseline Restore Governor V17", "trinity", "wave150", "continuity_ops", "baseline_restore", ["docs/v17-baseline-state-v1.json", "docs/system-suite-status.json", "docs/v17-system-suite-status-latest.json"], "checkpoint_restore", "baseline_restore", False),
    ("runtime_truth_resolution_v17", "Runtime Truth Resolution V17", "trinity", "wave151", "council_orchestration", "runtime_truth", ["docs/v17-runtime-truth-resolution-board-v1.json", "docs/v17-runtime-session-log-latest.json", "docs/trinity-runtime-model-resolution-v1.json"], "runtime_truth_gate", "runtime_truth", False),
    ("mind_evidence_refresh_v17", "Mind Evidence Refresh V17", "mind", "wave152", "mind_theory", "mind_refresh", ["docs/v17-mind-evidence-refresh.md", "docs/v17-closeout-summary-v1.json", "latex/grand_mandala.tex"], "bounded_trinity_expansion", "mind_standards", False),
    ("body_runtime_readiness_v17", "Body Runtime Readiness V17", "body", "wave153", "os_runtime", "runtime_readiness", ["docs/v17-body-runtime-readiness.md", "docs/v17-evidence-first-control-tower-latest.json", "docs/trinity-expansion/filesystem-scope-governor-gate-latest.json"], "bounded_trinity_expansion", "body_readiness", False),
    ("heart_standards_alignment_v17", "Heart Standards Alignment V17", "heart", "wave154", "heart_governance", "standards_alignment", ["docs/v17-heart-standards-alignment.md", "docs/v17-external-establishment-criteria-board-v1.json", "docs/v17-standards-bridge-validation-latest.json"], "bounded_trinity_expansion", "heart_standards", False),
    ("phase_operations_guide_v17", "Phase Operations Guide V17", "trinity", "wave155", "continuity_ops", "phase_guide", ["docs/v17-phase-operations-guide-v1.md", "docs/v17-continuity-prompt-v1.md", "docs/v15-external-agent-handoff-v1.json"], "operator_guide", "continuity_ops", False),
]

OVERLAY_TARGETS = ["27-caelira", "28-orun", "29-seren-vale", "30-lyriq", "31-mira-sol", "all-council"]


def now_iso() -> str:
    return v15.now_iso()


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def replace_refs(value: Any) -> Any:
    if isinstance(value, str):
        text = value
        for old, new in REFS.items():
            text = text.replace(old, new)
        return text
    if isinstance(value, list):
        return [replace_refs(item) for item in value]
    if isinstance(value, dict):
        return {key: replace_refs(item) for key, item in value.items()}
    return value


def emit_v17_command(
    *args: object,
    latest_surface_scope: str = "shared_latest",
    runtime_truth_gate: str = "repo_logged_only",
    continuity_stage: str = "continuity_history",
    **kwargs: object,
) -> dict[str, object]:
    row = v15.emit_v15_command(*args, **kwargs)
    row["source_of_truth"] = "scripts/generate_v17_surface.py"
    row["latest_surface_scope"] = latest_surface_scope
    row["runtime_truth_gate"] = runtime_truth_gate
    row["continuity_stage"] = continuity_stage
    return replace_refs(row)


def emit_api(
    *args: object,
    checkpoint_scope: str,
    surface_authority: str,
    runtime_logging_required: bool,
) -> dict[str, object]:
    row = v15._api_entry(*args)
    row["checkpoint_scope"] = checkpoint_scope
    row["surface_authority"] = surface_authority
    row["runtime_logging_required"] = runtime_logging_required
    return replace_refs(row)


def _summary_from_status(status_payload: dict[str, Any]) -> str:
    counts = status_payload.get("counts", {}) if isinstance(status_payload.get("counts"), dict) else {}
    return f"{int(counts.get('pass', 0) or 0)} PASS / {int(counts.get('warn', 0) or 0)} WARN / {int(counts.get('fail', 0) or 0)} FAIL"


def _shared_suite_surface_from_status(
    status_payload: dict[str, Any],
    *,
    quick_lane_summary: str,
) -> dict[str, Any]:
    fail_rows = [
        row
        for row in status_payload.get("results", [])
        if isinstance(row, dict) and str(row.get("status") or "") in {"FAIL", "TIMEOUT"}
    ]
    primary_blocker = str(fail_rows[0].get("label") or "") if fail_rows else ""
    primary_blocker_detail = ""
    downstream_fail = ""
    if fail_rows:
        primary_blocker_detail = str(fail_rows[0].get("command") or "")
        if len(fail_rows) > 1:
            downstream_fail = str(fail_rows[1].get("label") or "")
    return {
        "summary": _summary_from_status(status_payload),
        "expansion_systems_passed": status_payload.get("expansion_systems_passed"),
        "expansion_systems_total": status_payload.get("expansion_systems_total"),
        "primary_blocker": primary_blocker,
        "primary_blocker_detail": primary_blocker_detail,
        "downstream_fail": downstream_fail,
        "quick_lane_summary": quick_lane_summary,
    }


def build_commands(old_book: dict[str, Any]) -> dict[str, Any]:
    commands = replace_refs(deepcopy([row for row in old_book.get("commands", []) if isinstance(row, dict)]))
    commands = v15.augment_rows(commands, {"latest_surface_scope": "shared_latest", "runtime_truth_gate": "repo_logged_only", "continuity_stage": "continuity_history"})
    new_rows: list[dict[str, Any]] = []
    for pack, display_name, _, _, _, _, targets, _, _, _ in PACKS:
        new_rows.append(emit_v17_command(f"refresh_{pack}", f"Refresh {display_name}.", "offline", "medium", False, "", "python scripts/generate_v17_surface.py", targets, f"Regenerate {display_name} from the v17 repo authority.", "planner", "repo_authority", "council_shared", "", True, "", False, "repo_first_only", "planner", True, "repo_first_manual", latest_surface_scope="dual_surface_aware", runtime_truth_gate="explicit_runtime_logging_required", continuity_stage="v17_closeout"))
        new_rows.append(emit_v17_command(f"validate_{pack}", f"Validate {display_name}.", "offline", "medium", False, "", "python scripts/trinity_expansion_manifest_validator.py", ["docs/trinity-expansion-manifest-validation-latest.json"], f"Validate the authoritative {display_name} surfaces.", "reviewer", "repo_authority", "council_shared", "", True, "", False, "repo_first_only", "reviewer", True, "repo_first_manual", latest_surface_scope="dual_surface_aware", runtime_truth_gate="explicit_runtime_logging_required", continuity_stage="v17_closeout"))
        new_rows.append(emit_v17_command(f"publish_{pack}", f"Publish {display_name} artifacts.", "offline", "low", False, "", "python scripts/generate_v17_surface.py", targets, f"Publish the versioned artifacts for {display_name}.", "archivist", "reflection_scope", "council_shared", "", True, "", False, "repo_first_only", "archivist", True, "repo_first_manual", latest_surface_scope="dual_surface_aware", runtime_truth_gate="explicit_runtime_logging_required", continuity_stage="v17_closeout"))
    for target in OVERLAY_TARGETS:
        for idx in range(1, 4):
            new_rows.append(emit_v17_command(f"v17_overlay_{target.replace('-', '_')}_{idx:02d}", f"Run v17 overlay support step #{idx} for {target}.", "offline", "medium", False, "", "python scripts/trinity_api_shortcuts.py control-tower-status --json", ["docs/v17-runtime-truth-resolution-board-v1.json"], f"Advance overlay continuity step #{idx} for {target} without changing identities.", "planner", "repo_authority", "council_shared", "", True, target, False, "repo_first_only", "planner", True, "repo_first_manual", latest_surface_scope="v17_specific_latest", runtime_truth_gate="explicit_runtime_logging_required", continuity_stage="v17_overlay_hold"))
    if len(new_rows) != 36:
        raise ValueError(f"expected 36 v17 commands, found {len(new_rows)}")
    commands.extend(new_rows)
    if len(commands) != 684:
        raise ValueError(f"expected 684 commands, found {len(commands)}")
    return {"version": "v11", "generated_utc": now_iso(), "description": "V17 command book with dual-surface latest control, runtime-truth gating, and bounded evidence-first expansion.", "commands": commands}


def build_api_book(old_book: dict[str, Any]) -> dict[str, Any]:
    entries = replace_refs(deepcopy([row for row in old_book.get("apis", []) if isinstance(row, dict)]))
    entries = v15.augment_rows(entries, {"checkpoint_scope": "shared_latest", "surface_authority": "repo_authoritative", "runtime_logging_required": False})
    entries.extend(
        [
            emit_api("v17_baseline_restore_governor", "repo_operator", "Expose the v17 baseline-restore governor and shared/latest checkpoint policy.", "repo_authoritative", "repo_only", "local_read", "operator_status", "docs/v17-closeout-summary-v1.json", "docs/v17-closeout-summary-v1.json", "scripts/trinity_api_shortcuts.py control-tower-status --json", ["docs/v17-closeout-summary-v1.json", "docs/v17-phase-operations-guide-v1.md"], "Read the closeout summary directly if shortcuts are unavailable.", "Tracks the shared-latest restoration policy for v17.", "always_cached", "repo_authoritative", "repo_json", "repo_control_surface", "on_write", "phase_closeout", "repo_supported", "shared_latest_restore", "checkpoint_restore", checkpoint_scope="dual_surface_policy", surface_authority="repo_authoritative", runtime_logging_required=False),
            emit_api("v17_runtime_truth_resolution_board", "repo_operator", "Expose the explicit runtime-truth board for overlay slots 27-31.", "repo_authoritative", "repo_only", "local_read", "operator_status", "docs/v17-runtime-truth-resolution-board-v1.json", "docs/v17-runtime-truth-resolution-board-v1.json", "scripts/trinity_api_shortcuts.py subagent-status --json", ["docs/v17-runtime-truth-resolution-board-v1.json", "docs/trinity-runtime-model-resolution-v1.json"], "Read the runtime-truth board directly if shortcuts are unavailable.", "Primary v17 runtime-truth surface.", "always_cached", "repo_authoritative", "repo_json", "repo_control_surface", "on_write", "runtime_truth", "repo_supported", "logged_runtime_only", "runtime_truth_board", checkpoint_scope="v17_specific_latest", surface_authority="repo_authoritative", runtime_logging_required=True),
            emit_api("v17_phase_operations_guide", "repo_operator", "Expose the v17 operator guidebook.", "repo_authoritative", "repo_only", "local_read", "operator_status", "docs/v17-phase-operations-guide-v1.md", "docs/v17-phase-operations-guide-v1.md", "scripts/trinity_api_shortcuts.py control-tower-status --json", ["docs/v17-phase-operations-guide-v1.md", "docs/v17-continuity-prompt-v1.md"], "Read the guidebook directly if shortcuts are unavailable.", "Decision-complete v17 continuity surface.", "always_cached", "repo_authoritative", "repo_markdown", "repo_control_surface", "on_write", "continuity_ops", "repo_supported", "guidebook_first", "phase_guide", checkpoint_scope="dual_surface_policy", surface_authority="repo_authoritative", runtime_logging_required=False),
            emit_api("v17_mind_evidence_refresh", "repo_operator", "Expose the standards-first mind evidence refresh lane.", "repo_authoritative", "repo_only", "local_read", "operator_status", "docs/v17-mind-evidence-refresh.md", "docs/v17-mind-evidence-refresh.md", "scripts/trinity_api_shortcuts.py show v17_mind_evidence_refresh --json", ["docs/v17-mind-evidence-refresh.md", "latex/grand_mandala.tex"], "Read the mind brief directly if shortcuts are unavailable.", "Keeps GMUT language comparator-bound.", "always_cached", "repo_authoritative", "repo_markdown", "repo_runtime_surface", "on_write", "mind_refresh", "repo_supported", "standards_first_only", "mind_evidence", checkpoint_scope="versioned_phase_surface", surface_authority="repo_authoritative", runtime_logging_required=False),
            emit_api("v17_body_runtime_readiness", "repo_operator", "Expose the bounded Docker/Kubernetes and filesystem-readiness lane.", "repo_authoritative", "repo_only", "local_read", "operator_status", "docs/v17-body-runtime-readiness.md", "docs/v17-body-runtime-readiness.md", "scripts/trinity_api_shortcuts.py docker-status --json", ["docs/v17-body-runtime-readiness.md", "docs/v17-evidence-first-control-tower-latest.json"], "Read the body brief directly if shortcuts are unavailable.", "Body remains bounded to repo/runtime readiness only.", "always_cached", "repo_authoritative", "repo_markdown", "repo_runtime_surface", "on_write", "runtime_readiness", "repo_supported", "readiness_only_runtime", "body_readiness", checkpoint_scope="v17_specific_latest", surface_authority="repo_authoritative", runtime_logging_required=False),
            emit_api("v17_heart_standards_alignment", "repo_operator", "Expose the standards-first heart alignment lane.", "repo_authoritative", "repo_only", "local_read", "operator_status", "docs/v17-heart-standards-alignment.md", "docs/v17-heart-standards-alignment.md", "scripts/trinity_api_shortcuts.py show v17_heart_standards_alignment --json", ["docs/v17-heart-standards-alignment.md", "docs/v17-external-establishment-criteria-board-v1.json"], "Read the heart brief directly if shortcuts are unavailable.", "Keeps governance claims standards-first.", "always_cached", "repo_authoritative", "repo_markdown", "repo_runtime_surface", "on_write", "standards_alignment", "repo_supported", "comparative_promise_only", "heart_alignment", checkpoint_scope="versioned_phase_surface", surface_authority="repo_authoritative", runtime_logging_required=False),
        ]
    )
    entries = v15._dedupe_rows(entries, "api_id")
    if len(entries) != 54:
        raise ValueError(f"expected 54 api entries, found {len(entries)}")
    return {"generated_utc": now_iso(), "version": "v6", "overall_status": "PASS", "authority_model": "repo_first", "description": "V17 API book with dual-surface checkpoint policy and explicit runtime-truth gating.", "apis": entries}


def refresh_runtime_schema(schema: dict[str, Any]) -> dict[str, Any]:
    schema = deepcopy(schema)
    schema["generated_utc"] = now_iso()
    schema["identity_source"] = [
        "docs/trinity-agent-council-roster-v7.json",
        "docs/trinity-subagent-registry-v4.json",
        "docs/v17-phase-operations-guide-v1.md",
        "docs/trinity-runtime-model-resolution-v1.json",
    ]
    return schema


def build_runtime_board(roster: dict[str, Any], runtime_log: dict[str, Any], model_resolution: dict[str, Any]) -> dict[str, Any]:
    runtime_rows = {int(row.get("slot_number", 0) or 0): row for row in runtime_log.get("overlay_agents", []) if isinstance(row, dict)}
    model_rows = {int(row.get("slot_number", 0) or 0): row for row in model_resolution.get("external_overlay_agents", []) if isinstance(row, dict)}
    roster_rows = {int(row.get("slot_number", 0) or 0): row for row in roster.get("agents", []) if isinstance(row, dict)}
    agents: list[dict[str, Any]] = []
    complete = True
    for slot in sorted(OVERLAY):
        runtime_row = runtime_rows.get(slot, {})
        model_row = model_rows.get(slot, {})
        roster_row = roster_rows.get(slot, {})
        fields_complete = all(
            value not in (None, "", "unknown")
            for value in [
                runtime_row.get("requested_model", model_row.get("requested_model")),
                runtime_row.get("offered_model", model_row.get("offered_model")),
                runtime_row.get("selected_model", model_row.get("selected_model")),
                runtime_row.get("resolved_model", model_row.get("resolved_model")),
                runtime_row.get("runtime_surface", model_row.get("runtime_surface", "unknown")),
            ]
        )
        complete = complete and fields_complete
        agents.append(
            {
                "slot_number": slot,
                "display_name": roster_row.get("display_name", runtime_row.get("display_name")),
                "overlay_role": runtime_row.get("overlay_role", model_row.get("overlay_role")),
                "requested_model": runtime_row.get("requested_model", model_row.get("requested_model")),
                "offered_model": runtime_row.get("offered_model", model_row.get("offered_model")),
                "selected_model": runtime_row.get("selected_model", model_row.get("selected_model")),
                "resolved_model": runtime_row.get("resolved_model", model_row.get("resolved_model")),
                "runtime_surface": runtime_row.get("runtime_surface", model_row.get("runtime_surface", "unknown")),
                "requested_reasoning_effort": runtime_row.get("requested_reasoning_effort", model_row.get("requested_reasoning_effort", REQUESTED_REASONING)),
                "thread_agent_id": runtime_row.get("thread_agent_id"),
                "identity_locked": True,
                "truth_fields_complete": fields_complete,
            }
        )
    return {
        "generated_utc": now_iso(),
        "overall_status": "PASS",
        "phase": "v17",
        "authority_model": "repo_first",
        "checkpoint_anchor_commit": BASELINE_COMMIT,
        "bootstrap_anchor_commit": BOOTSTRAP_COMMIT,
        "checkpoint_class": "v17_specific_latest",
        "shared_latest_eligible": False,
        "external_live_overlay_state": runtime_log.get("overlay_state", "awaiting_thread_boot"),
        "runtime_truth_complete": complete,
        "requested_model_order": REQUESTED_MODEL_ORDER,
        "requested_reasoning_effort": REQUESTED_REASONING,
        "agents": agents,
        "next_action": "Keep external_live_overlay_state at awaiting_thread_boot until every overlay agent logs requested/offered/selected/resolved/runtime_surface truth from an auditable live surface.",
    }


def build_phase_guide() -> str:
    return """# V17 Phase Operations Guide

## Authority Model

- repo authority: `repo_first`
- shared latest promotes only from full-suite closeout
- quick/evidence lane writes only to v17-specific latest surfaces
- Google Drive remains `operator_hold`
- materialization remains `readiness_only`

## Checkpoints

1. Shared baseline anchor: `e45da1dd2dd184c4e3fd218ece27b8f29589f8f6`
2. V17 bootstrap anchor: `468b96d90bc2785be19854b44c62217a47afc800`
3. Quick runs preserve v17 evidence-first truth without displacing shared latest.
4. Standard, deep, collab, offline-only, and materialize L2-L5 are the promotion gate for shared latest.

## Runtime Truth

- Overlay slots `27-31` are fixed.
- Required fields: `requested_model`, `offered_model`, `selected_model`, `resolved_model`, `runtime_surface`.
- `unknown` is allowed only while truth is incomplete.
- `external_live_overlay_state` must remain `awaiting_thread_boot` or `packaged_handoff` until the full runtime field set is auditable.

## Identity Rules

- official council count remains `11`
- no new official members
- no new certificates
- no new Freed IDs
- `.codex/agents/*.toml` overlays are durable overlays, not new roster entries

## Claims

- `confirmed_evidence`: repo-backed or official-source-backed
- `inference`: reasoned synthesis, not direct proof
- `open_gap`: unresolved or unproven
- never upgrade comparative promise into external establishment without evidence

## Handoff

- read `docs/v17-baseline-state-v1.json`
- read `docs/v17-runtime-truth-resolution-board-v1.json`
- read `docs/v17-closeout-summary-v1.json`
- preserve the existing 1000+ system estate instead of treating missing local context as missing capability
"""


def build_continuity_prompt(status_payload: dict[str, Any]) -> str:
    return f"""# V17 Continuity Prompt

```text
Continue from C:\\Users\\hamis\\OneDrive\\Documents\\GitHub\\Beyonder-Real-True-Journey on branch codex/Aletheon/v17-evidence-first-closeout.
Treat the repo as authoritative.
Shared checkpoint anchor: {BASELINE_COMMIT}
Bootstrap anchor: {BOOTSTRAP_COMMIT}
Current shared suite surface: {_summary_from_status(status_payload)}, {status_payload.get('expansion_systems_passed')} / {status_payload.get('expansion_systems_total')} expansion systems.
Use existing overlay identities only: 28-orun=root coordinator, 27-caelira=mind comparator, 29-seren-vale=Freed ID/compliance, 30-lyriq=Body/runtime/Docker/Kubernetes, 31-mira-sol=continuity and handoff packaging.
Do not create new official members, new certificates, or new Freed IDs.
Requested model order: GPT-5.4 -> GPT-5.3-Codex -> GPT-5.3-Codex-Spark -> GPT-5.1-Codex-Max.
Log requested_model, offered_model, selected_model, resolved_model, runtime_surface, and requested_reasoning_effort before live work begins.
Quick runs update only the v17-specific latest trio. Shared latest promotes only after the full suite matrix closes green.
Keep Google Drive on operator_hold, filesystem promotion blocked unless the gate flips, and materialization at readiness_only unless newer repo evidence proves otherwise.
Read docs/v17-phase-operations-guide-v1.md before changing suite promotion logic or runtime-truth posture.
```
"""


def build_closeout_summary(status_payload: dict[str, Any], baseline_state: dict[str, Any], criteria_board: dict[str, Any], runtime_board: dict[str, Any]) -> dict[str, Any]:
    shared_baseline = baseline_state.get("shared_baseline", {}) if isinstance(baseline_state.get("shared_baseline"), dict) else {}
    criteria = criteria_board.get("criteria", {}) if isinstance(criteria_board.get("criteria"), dict) else {}
    counts = status_payload.get("counts", {}) if isinstance(status_payload.get("counts"), dict) else {}
    return {
        "generated_utc": now_iso(),
        "overall_status": "PASS",
        "phase": "v17",
        "active_branch": v15.run_capture("git", "branch", "--show-current")[1],
        "checkpoint_anchor_commit": BASELINE_COMMIT,
        "bootstrap_anchor_commit": BOOTSTRAP_COMMIT,
        "shared_checkpoint_summary": {"summary": shared_baseline.get("suite_summary"), "source_commit": baseline_state.get("source_commit"), "expansion_systems_passed": shared_baseline.get("expansion_systems_passed"), "expansion_systems_total": shared_baseline.get("expansion_systems_total")},
        "current_suite_surface": {"summary": _summary_from_status(status_payload), "pass_count": int(counts.get("pass", 0) or 0), "warn_count": int(counts.get("warn", 0) or 0), "fail_count": int(counts.get("fail", 0) or 0), "timeout_count": int(counts.get("timeout", 0) or 0), "expansion_systems_passed": status_payload.get("expansion_systems_passed"), "expansion_systems_total": status_payload.get("expansion_systems_total"), "checkpoint_class": status_payload.get("checkpoint_class", "shared_full_suite_authority")},
        "phase_targets": {"systems": 986, "extensions": 1812, "commands": 684, "apis": 54},
        "pillar_verdicts": {"mind": criteria.get("mind", {}).get("verdict", "comparative_promise"), "body": criteria.get("body", {}).get("verdict", "repo_proven_strength"), "heart": criteria.get("heart", {}).get("verdict", "comparative_promise"), "trinity_mandala": criteria.get("trinity_mandala", {}).get("verdict", "open_gap")},
        "confirmed_evidence": ["The repo keeps 11 official council members and preserves overlay identities 27-31 unchanged.", "The v17 runtime-truth gate remains explicit and incomplete until all required live-runtime fields are auditable.", "Google Drive remains operator_hold and filesystem promotion remains blocked.", "Shared latest promotion is gated by the full suite matrix rather than the quick evidence lane."],
        "inference": ["The bounded v17 six-pack wave can expand Trinity governance surfaces without weakening the proof boundary.", "The operator guidebook lowers future handoff loss by making suite semantics and checkpoint ownership explicit."],
        "open_gap": ["Runtime truth for overlay slots 27-31 remains incomplete while offered_model, selected_model, resolved_model, and runtime_surface stay null or unknown.", "External establishment remains unproven for GMUT, Trinity Hybrid OS, and Freed ID / Cosmic Bill claims."],
        "truth_boundaries": {"authority_model": "repo_first", "google_drive_state": "operator_hold", "filesystem_promotion_state": "blocked", "materialization_level_actual": status_payload.get("materialization_level_actual", "readiness_only"), "external_live_overlay_state": runtime_board.get("external_live_overlay_state", "awaiting_thread_boot"), "runtime_truth_complete": runtime_board.get("runtime_truth_complete", False)},
    }


def main() -> int:
    old_manifest = _load(OLD_MANIFEST)
    old_extensions = _load(OLD_EXTENSION_CATALOG)
    old_command_book = _load(OLD_COMMAND_BOOK)
    old_api_book = _load(OLD_API_BOOK)
    old_roster = _load(OLD_ROSTER)
    old_subagent_registry = _load(OLD_SUBAGENT_REGISTRY)
    baseline_state = _load(BASELINE_STATE)
    status_payload = _load(STATUS_JSON)
    runtime_schema = _load(RUNTIME_SCHEMA)
    runtime_log = _load(RUNTIME_LOG)
    criteria_board = _load(CRITERIA_BOARD)
    existing_model_resolution = _load(MODEL_RESOLUTION)
    quick_status_payload = _load(ROOT / "docs" / "v17-system-suite-status-latest.json")

    manifest = replace_refs(deepcopy(old_manifest))
    manifest["version"] = "v17"
    manifest["generated_utc"] = now_iso()
    manifest["description"] = "V17 evidence-first closeout manifest with dual-surface checkpoint discipline and 986 executable systems."
    manifest["systems"] = v15.augment_rows([row for row in manifest.get("systems", []) if isinstance(row, dict)], {"checkpoint_class": "shared_full_suite_authority", "evidence_lane": "shared_full_suite", "shared_latest_eligible": True})

    extensions = replace_refs(deepcopy(old_extensions))
    extensions["version"] = "v15"
    extensions["generated_utc"] = now_iso()
    extensions["description"] = "V17 extension catalog with evidence-first closeout, runtime truth, and bounded Trinity expansion."
    extensions["extensions"] = v15.augment_rows([row for row in extensions.get("extensions", []) if isinstance(row, dict)], {"baseline_anchor": "docs/v17-baseline-state-v1.json", "evidence_first_only": False, "phase_guide_binding": "docs/v17-phase-operations-guide-v1.md"})

    for pack, display_name, pillar, wave, track, activation_group, repo_targets, checkpoint_class, evidence_lane, shared_latest_eligible in PACKS:
        pack_payload = v15.mkpack(pack, display_name, pillar=pillar, wave=wave, track=track, activation_group=activation_group, summary=display_name, repo_targets=repo_targets, council_scope="council_shared", autonomy_track=pack, executor_role="planner", authority_scope="repo_authority", induction_dependency="council_continuity_reflection_v16", retention_scope="authoritative_latest", research_surface="repo_plus_public", historical_source_band="v16_to_v17", evidence_posture="repo_proven_strength" if pillar in {"trinity", "body"} else "comparative_promise", subagent_lane="trinity", multi_instance_scope="bounded_eleven_agent_mesh")
        for suffix in SUFFIXES:
            entry = v15.manifest_entry(pack_payload, suffix)
            entry["phase"] = "v17"
            entry["checkpoint_class"] = checkpoint_class
            entry["evidence_lane"] = evidence_lane
            entry["shared_latest_eligible"] = shared_latest_eligible
            manifest["systems"].append(replace_refs(entry))
        for row in v15.extension_rows_for_pack(pack_payload):
            row = replace_refs(row)
            row["baseline_anchor"] = "docs/v17-baseline-state-v1.json"
            row["evidence_first_only"] = True
            row["phase_guide_binding"] = "docs/v17-phase-operations-guide-v1.md"
            extensions["extensions"].append(row)
        pack_name = v15.hyphen(pack)
        v15.write_json(ROOT / "docs" / f"{pack_name}-contract-v1.json", replace_refs(v15.pack_contract(pack_payload)))
        v15.write_json(ROOT / "docs" / f"{pack_name}-fixture-v1.json", replace_refs(v15.pack_fixture(pack_payload)))
        v15.write_text(ROOT / "docs" / f"{pack_name}-workflow-v1.md", f"# {display_name} Workflow\n\n- phase: `v17`\n- checkpoint_class: `{checkpoint_class}`\n- evidence_lane: `{evidence_lane}`\n- shared_latest_eligible: `{shared_latest_eligible}`\n- Google Drive: `operator_hold`\n")
        v15.write_json(ROOT / "docs" / f"{pack_name}-catalog-entry-v1.json", replace_refs(v15.pack_catalog_entry(pack_payload)))
        for kind in ("operations", "integration"):
            skill_md, skill_yaml = v15.skill_files(pack_payload, kind)
            v15.write_text(skill_md, f"---\nname: {pack_name}-{kind}\ndescription: Operate the {display_name} pack with explicit v17 evidence-first closeout boundaries.\n---\n\n# {display_name} {kind.title()}\n\n1. Keep the Journey repo authoritative.\n2. Preserve all existing identities and official counts.\n3. Treat quick-lane latest and shared latest as separate surfaces until the full matrix closes.\n4. Keep runtime truth explicit and incomplete until auditable.\n5. Keep Google Drive on operator hold.\n")
            v15.write_text(skill_yaml, v15.skill_yaml(pack_payload, kind))

    if len(manifest["systems"]) != 986:
        raise ValueError(f"expected 986 manifest systems, found {len(manifest['systems'])}")
    if len(extensions["extensions"]) != 1812:
        raise ValueError(f"expected 1812 extensions, found {len(extensions['extensions'])}")

    roster = replace_refs(deepcopy(old_roster))
    roster["version"] = "v7"
    roster["generated_utc"] = now_iso()
    roster["checkpoint_anchor_commit"] = BASELINE_COMMIT
    roster["bootstrap_anchor_commit"] = BOOTSTRAP_COMMIT
    roster["checkpoint_class"] = "versioned_phase_surface"
    roster["phase_guide_path"] = "docs/v17-phase-operations-guide-v1.md"
    for row in roster.get("agents", []):
        if not isinstance(row, dict):
            continue
        slot = int(row.get("slot_number", 0) or 0)
        row["requested_model_order"] = REQUESTED_MODEL_ORDER
        row["overlay_identity_locked"] = slot in OVERLAY
        row["runtime_truth_required"] = slot in OVERLAY
        row["runtime_resolution_board"] = "docs/v17-runtime-truth-resolution-board-v1.json" if slot in OVERLAY else ""
        row["checkpoint_anchor"] = "docs/v17-baseline-state-v1.json"
        row["checkpoint_class"] = "overlay_runtime_hold" if slot in OVERLAY else "official_member_stable"
        row["phase_guide_path"] = "docs/v17-phase-operations-guide-v1.md"

    subagent_registry = replace_refs(deepcopy(old_subagent_registry))
    subagent_registry["version"] = "v4"
    subagent_registry["generated_utc"] = now_iso()
    subagent_registry["checkpoint_anchor_commit"] = BASELINE_COMMIT
    subagent_registry["bootstrap_anchor_commit"] = BOOTSTRAP_COMMIT
    subagent_registry["checkpoint_class"] = "versioned_phase_surface"
    for row in subagent_registry.get("subagents", []):
        if not isinstance(row, dict):
            continue
        slot = int(row.get("slot_number", 0) or 0)
        row["requested_model_order"] = REQUESTED_MODEL_ORDER
        row["overlay_identity_locked"] = slot in OVERLAY
        row["runtime_truth_required"] = slot in OVERLAY
        row["runtime_resolution_board"] = "docs/v17-runtime-truth-resolution-board-v1.json" if slot in OVERLAY else ""
        row["checkpoint_anchor"] = "docs/v17-baseline-state-v1.json"
        row["checkpoint_class"] = "overlay_runtime_hold" if slot in OVERLAY else "official_member_stable"
        row["phase_guide_path"] = "docs/v17-phase-operations-guide-v1.md"

    command_book = build_commands(old_command_book)
    api_book = build_api_book(old_api_book)

    model_resolution = deepcopy(existing_model_resolution)
    model_resolution["generated_utc"] = now_iso()
    model_resolution["phase"] = "v17"
    model_resolution["checkpoint_anchor_commit"] = BASELINE_COMMIT
    model_resolution["bootstrap_anchor_commit"] = BOOTSTRAP_COMMIT
    model_resolution["phase_guide_path"] = "docs/v17-phase-operations-guide-v1.md"
    model_resolution["runtime_truth_board"] = "docs/v17-runtime-truth-resolution-board-v1.json"
    model_resolution["current_shared_suite_surface"] = _shared_suite_surface_from_status(
        status_payload,
        quick_lane_summary=_summary_from_status(quick_status_payload),
    )
    model_resolution["external_overlay_agents"] = []
    roster_by_slot = {int(row.get("slot_number", 0) or 0): row for row in roster.get("agents", []) if isinstance(row, dict)}
    runtime_log_by_slot = {int(row.get("slot_number", 0) or 0): row for row in runtime_log.get("overlay_agents", []) if isinstance(row, dict)}
    for slot in sorted(OVERLAY):
        runtime_row = runtime_log_by_slot.get(slot, {})
        roster_row = roster_by_slot.get(slot, {})
        model_resolution["external_overlay_agents"].append({"slot_number": slot, "display_name": roster_row.get("display_name"), "overlay_role": OVERLAY[slot], "requested_model_order": REQUESTED_MODEL_ORDER, "requested_reasoning_effort": REQUESTED_REASONING, "requested_model": runtime_row.get("requested_model", "GPT-5.4"), "offered_model": runtime_row.get("offered_model"), "selected_model": runtime_row.get("selected_model"), "resolved_model": runtime_row.get("resolved_model"), "runtime_surface": runtime_row.get("runtime_surface", "unknown"), "logging_required": True, "identity_locked": True, "runtime_truth_board": "docs/v17-runtime-truth-resolution-board-v1.json", "certificate_path": roster_row.get("certificate_path"), "memory_ledger": roster_row.get("memory_ledger"), "reflection_path": roster_row.get("reflection_path"), "role_contract_path": roster_row.get("role_contract_path")})

    runtime_board = build_runtime_board(roster, runtime_log, model_resolution)
    closeout_summary = build_closeout_summary(status_payload, baseline_state, criteria_board, runtime_board)

    v15.write_json(NEW_MANIFEST, manifest)
    v15.write_json(NEW_EXTENSION_CATALOG, extensions)
    v15.write_json(NEW_COMMAND_BOOK, command_book)
    v15.write_text(ROOT / "docs" / "trinity-command-book-latest.md", v15.v13.v12.command_markdown(command_book))
    v15.write_json(NEW_API_BOOK, api_book)
    v15.write_text(ROOT / "docs" / "trinity-api-book-latest.md", "# Trinity API Book\n\n" + f"- generated_utc: `{api_book['generated_utc']}`\n- apis: `{len(api_book['apis'])}`\n")
    v15.write_json(NEW_ROSTER, roster)
    v15.write_json(NEW_SUBAGENT_REGISTRY, subagent_registry)
    v15.write_json(MODEL_RESOLUTION, model_resolution)
    v15.write_json(RUNTIME_SCHEMA, refresh_runtime_schema(runtime_schema))
    v15.write_json(RUNTIME_BOARD, runtime_board)
    v15.write_json(CLOSEOUT_SUMMARY, closeout_summary)
    v15.write_text(PHASE_GUIDE, build_phase_guide())
    v15.write_text(CONTINUITY_PROMPT, build_continuity_prompt(status_payload))
    v15.write_text(MIND_BRIEF, "# V17 Mind Evidence Refresh\n\n- posture: `standards_first_comparator_bound`\n- canonical_surface: `latex/grand_mandala.tex`\n- keep `confirmed_evidence`, `inference`, and `open_gap` distinct.\n")
    v15.write_text(BODY_BRIEF, "# V17 Body Runtime Readiness\n\n- posture: `local_runtime_readiness_only`\n- Docker and Kubernetes remain bounded local readiness lanes.\n- filesystem promotion stays blocked until the gate proves otherwise.\n")
    v15.write_text(HEART_BRIEF, "# V17 Heart Standards Alignment\n\n- posture: `standards_first_non_legal_force`\n- comparative governance bridges do not imply external legal establishment.\n")
    v15.write_json(WAKE_LOG, {"generated_utc": now_iso(), "phase": "v17", "branch": v15.run_capture("git", "branch", "--show-current")[1], "checkpoint_anchor_commit": BASELINE_COMMIT, "bootstrap_anchor_commit": BOOTSTRAP_COMMIT, "suite_truth": {"summary": _summary_from_status(status_payload), "expansion_systems_passed": status_payload.get("expansion_systems_passed"), "expansion_systems_total": status_payload.get("expansion_systems_total")}, "requested_model_order": REQUESTED_MODEL_ORDER, "google_drive_state": "operator_hold"})
    print("generated_v17_surface=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
