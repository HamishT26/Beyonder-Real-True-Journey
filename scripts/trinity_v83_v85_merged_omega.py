#!/usr/bin/env python3
"""Merged v83-v85 Omega planner and closeout for one 60-system final wave."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from trinity_v77_v84_candidate_systems import CANDIDATES, hyphen
from trinity_v77_v84_omega import (
    DOCS,
    ROOT,
    TRACE,
    eureka_plan_markdown,
    ensure_manifest_promotions,
    live_write_preflight,
    marker_hits,
    now_iso,
    personal_report_markdown,
    provider_probe,
    publication_result,
    report_markdown,
    runtime_health_gate,
    stage_allowlist,
    suite_status,
    write_json,
    write_text,
)


PHASES = ["v83", "v84", "v85"]
ANCHOR_PHASE = "v82"
STEM = "v83-v85-merged"
PREFIX = "v77-v84"
PUBLICATION_BRANCH = "codex/GHC-Family/beyonder-shared-omega-line"


def read_json(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return default


def phase_candidates(phase: str) -> list[dict[str, Any]]:
    rows = []
    for system_id, spec in sorted(CANDIDATES.items()):
        if spec["phase"] == phase:
            rows.append({"id": system_id, **spec})
    return rows


def merged_plan_payload(promotions: list[dict[str, Any]]) -> dict[str, Any]:
    total_added = sum(int(row.get("added_count", 0)) for row in promotions)
    total_refreshed = sum(int(row.get("refreshed_count", 0)) for row in promotions)
    final_wave_count = sum(len(phase_candidates(phase)) for phase in PHASES)
    return {
        "generated_utc": now_iso(),
        "phase": "v83_v85_merged_omega",
        "state": "planned_or_in_progress",
        "phases": PHASES,
        "anchor_phase": ANCHOR_PHASE,
        "validation_mode": "single_combined_deep_and_l5_after_all_promotions",
        "suite_status_paths": {
            "deep": f"docs/trinity-live-traces/{STEM}-deep-suite-status.json",
            "l5": f"docs/trinity-live-traces/{STEM}-materialize-l5-suite-status.json",
        },
        "direct_sweep_logs": [
            f"docs/trinity-live-traces/{PREFIX}-cli-reports/{phase}-direct-candidate-sweep.log"
            for phase in PHASES
        ],
        "candidate_expansion_target": 60,
        "eureka_proposal_target": 60,
        "merged_final_wave_candidate_count": final_wave_count,
        "promotions": promotions,
        "promotion_added_count": total_added,
        "promotion_refreshed_count": total_refreshed,
        "guarded_live_write_policy": "repo_publication_only_without_fresh_external_provider_confirmation",
        "operator_hold_surfaces": [
            "google_drive_content_mutation",
            "gmail_or_personal_email_send",
            "calendar_event_mutation",
            "account_setting_change",
            "production_dns",
            "provider_billing_change",
            "raw_secret_transmission",
        ],
        "truth_note": (
            "v83, v84, and v85 are intentionally merged after v82. "
            "No separate v83 or v84 suite receipt is claimed; one combined Deep "
            "and one combined L5 validate the full 60-system promotion."
        ),
    }


def merged_closeout_payload() -> dict[str, Any]:
    deep = read_json(TRACE / f"{STEM}-deep-suite-status.json", {})
    l5 = read_json(TRACE / f"{STEM}-materialize-l5-suite-status.json", {})
    deep_green = bool(isinstance(deep, dict) and deep.get("effective_success"))
    l5_green = bool(isinstance(l5, dict) and l5.get("effective_success"))
    marker_text_hits = []
    if (TRACE / f"{STEM}-materialize-l5-suite-status.json").exists():
        text = (TRACE / f"{STEM}-materialize-l5-suite-status.json").read_text(encoding="utf-8", errors="replace")
        markers = [
            'attempted_write": true',
            "production_dns",
            "account_setting",
            "personal_email",
            "google_drive_content_mutation",
            "raw_secret_transmission",
        ]
        marker_text_hits = [marker for marker in markers if marker in text]
    return {
        "generated_utc": now_iso(),
        "phase": "v83_v85_merged_omega",
        "state": "completed_green" if deep_green and l5_green and not marker_text_hits else "planned_or_in_progress",
        "phases": PHASES,
        "anchor_phase": ANCHOR_PHASE,
        "merged_final_wave_candidate_count": sum(len(phase_candidates(phase)) for phase in PHASES),
        "merged_final_wave_system_ids": [
            str(candidate["id"])
            for phase in PHASES
            for candidate in phase_candidates(phase)
        ],
        "deep": {
            "present": bool(deep),
            "effective_success": deep_green,
            "counts": deep.get("counts") if isinstance(deep, dict) else None,
            "achieved_steps": deep.get("achieved_steps") if isinstance(deep, dict) else None,
            "expansion_systems_total": deep.get("expansion_systems_total") if isinstance(deep, dict) else None,
            "expansion_systems_passed": deep.get("expansion_systems_passed") if isinstance(deep, dict) else None,
        },
        "l5": {
            "present": bool(l5),
            "effective_success": l5_green,
            "counts": l5.get("counts") if isinstance(l5, dict) else None,
            "achieved_steps": l5.get("achieved_steps") if isinstance(l5, dict) else None,
            "expansion_systems_total": l5.get("expansion_systems_total") if isinstance(l5, dict) else None,
            "expansion_systems_passed": l5.get("expansion_systems_passed") if isinstance(l5, dict) else None,
        },
        "l5_marker_hits": marker_text_hits,
        "next_required_action": "publish_merged_v83_v85_receipt" if deep_green and l5_green and not marker_text_hits else "finish_merged_v83_v85_validation",
        "truth_note": "This is one merged validation receipt for all 60 v83-v85 candidates.",
    }


def merged_allowlist_payload() -> dict[str, Any]:
    paths = [
        "scripts/trinity_v83_v85_merged_omega.py",
        "scripts/trinity_v77_v84_candidate_systems.py",
        "scripts/trinity_v77_v84_omega.py",
        "scripts/trinity_v76_candidate_systems.py",
        "scripts/trinity_expansion_manifest_validator.py",
        "scripts/trinity_v6_support.py",
        "docs/trinity-expansion-system-manifest-v17.json",
        f"docs/trinity-live-traces/{STEM}-superphase-plan-v1.json",
        f"docs/trinity-live-traces/{STEM}-superphase-plan-v1.md",
        f"docs/trinity-live-traces/{STEM}-closeout-summary-v1.json",
        f"docs/trinity-live-traces/{STEM}-closeout-summary-v1.md",
        f"docs/trinity-live-traces/{STEM}-stage-allowlist-v1.json",
        f"docs/trinity-live-traces/{STEM}-stage-allowlist-v1.md",
        f"docs/trinity-live-traces/{STEM}-deep-suite-status.json",
        f"docs/trinity-live-traces/{STEM}-materialize-l5-suite-status.json",
        f"docs/trinity-live-traces/{PREFIX}-phase-plan-v1.json",
        f"docs/trinity-live-traces/{PREFIX}-phase-plan-v1.md",
        f"docs/trinity-live-traces/{PREFIX}-system-expansion-candidate-pack-v1.json",
        f"docs/trinity-live-traces/{PREFIX}-system-expansion-candidate-pack-v1.md",
        f"docs/trinity-live-traces/{PREFIX}-runtime-health-gate-v1.json",
        f"docs/trinity-live-traces/{PREFIX}-runtime-health-gate-v1.md",
        f"docs/trinity-live-traces/{PREFIX}-provider-readiness-probe-v1.json",
        f"docs/trinity-live-traces/{PREFIX}-provider-readiness-probe-v1.md",
    ]
    for phase in PHASES:
        paths.extend(
            [
                f"docs/trinity-live-traces/{phase}-live-write-preflight-v1.json",
                f"docs/trinity-live-traces/{phase}-live-write-preflight-v1.md",
                f"docs/trinity-live-traces/{PREFIX}-cli-reports/{phase}-eureka-plan-v1.md",
                f"docs/trinity-live-traces/{PREFIX}-cli-reports/{phase}-personal-report-v1.md",
                f"docs/trinity-live-traces/{PREFIX}-cli-reports/{phase}-direct-candidate-sweep.log",
            ]
        )
        for candidate in phase_candidates(phase):
            stem = hyphen(str(candidate["id"]))
            paths.extend(
                [
                    f"docs/trinity-live-traces/{PREFIX}-candidate-system-results/{stem}.json",
                    f"docs/trinity-live-traces/{PREFIX}-candidate-system-results/{stem}.md",
                    f"docs/trinity-expansion/{stem}-latest.json",
                    f"docs/trinity-expansion/{stem}-latest.md",
                ]
            )
    return {
        "generated_utc": now_iso(),
        "phase": "v83_v85_merged_omega",
        "policy": "stage_only_merged_v83_v85_truth_surfaces_candidate_outputs_suite_statuses_and_receipts",
        "paths": sorted(dict.fromkeys(paths)),
    }


def write_merged_plan() -> None:
    promotions = []
    for phase in PHASES:
        promotions.append(ensure_manifest_promotions(phase))
        preflight = live_write_preflight(phase)
        write_json(TRACE / f"{phase}-live-write-preflight-v1.json", preflight)
        write_text(TRACE / f"{phase}-live-write-preflight-v1.md", report_markdown(f"{phase} live-write preflight", preflight))
        write_text(TRACE / f"{PREFIX}-cli-reports/{phase}-eureka-plan-v1.md", eureka_plan_markdown(phase))
        write_text(TRACE / f"{PREFIX}-cli-reports/{phase}-personal-report-v1.md", personal_report_markdown(phase))

    plan = merged_plan_payload(promotions)
    allow = merged_allowlist_payload()
    health = runtime_health_gate()
    providers = provider_probe()
    phase_plan = {
        "generated_utc": now_iso(),
        "phase": "v77_v85_hybrid_omega",
        "active_phase": "v83_v85_merged",
        "active_phases": [f"v{number}" for number in range(77, 86)],
        "runtime_health": health,
        "provider_probe": providers,
        "merged_superphase": plan,
    }
    all_candidates = [{"id": system_id, **spec} for system_id, spec in sorted(CANDIDATES.items())]
    pack = {
        "generated_utc": now_iso(),
        "phase": "v83_v85_merged_omega",
        "state": "merged_60_candidate_pack_with_cumulative_v77_v85_context",
        "candidate_count": len(all_candidates),
        "merged_final_wave_candidate_count": sum(len(phase_candidates(phase)) for phase in PHASES),
        "candidates": all_candidates,
        "count_policy": (
            "all 60 v83-v85 candidates are validated by one combined Deep and one combined L5 after promotion; "
            "the cumulative v77-v85 candidate list remains present so earlier runner-backed systems continue to pass."
        ),
    }
    closeout = merged_closeout_payload()
    write_json(TRACE / f"{STEM}-superphase-plan-v1.json", plan)
    write_text(TRACE / f"{STEM}-superphase-plan-v1.md", report_markdown(f"{STEM} superphase plan", plan))
    write_json(TRACE / f"{STEM}-stage-allowlist-v1.json", allow)
    write_text(TRACE / f"{STEM}-stage-allowlist-v1.md", report_markdown(f"{STEM} stage allowlist", allow))
    write_json(TRACE / f"{STEM}-closeout-summary-v1.json", closeout)
    write_text(TRACE / f"{STEM}-closeout-summary-v1.md", report_markdown(f"{STEM} closeout summary", closeout))
    write_json(TRACE / f"{PREFIX}-runtime-health-gate-v1.json", health)
    write_text(TRACE / f"{PREFIX}-runtime-health-gate-v1.md", report_markdown(f"{PREFIX}-runtime-health-gate-v1", health))
    write_json(TRACE / f"{PREFIX}-provider-readiness-probe-v1.json", providers)
    write_text(TRACE / f"{PREFIX}-provider-readiness-probe-v1.md", report_markdown(f"{PREFIX}-provider-readiness-probe-v1", providers))
    write_json(TRACE / f"{PREFIX}-phase-plan-v1.json", phase_plan)
    write_text(TRACE / f"{PREFIX}-phase-plan-v1.md", report_markdown(f"{PREFIX}-phase-plan-v1", phase_plan))
    write_json(TRACE / f"{PREFIX}-system-expansion-candidate-pack-v1.json", pack)
    write_text(TRACE / f"{PREFIX}-system-expansion-candidate-pack-v1.md", report_markdown(f"{PREFIX}-system-expansion-candidate-pack-v1", pack))


def write_closeout() -> None:
    closeout = merged_closeout_payload()
    write_json(TRACE / f"{STEM}-closeout-summary-v1.json", closeout)
    write_text(TRACE / f"{STEM}-closeout-summary-v1.md", report_markdown(f"{STEM} closeout summary", closeout))


def write_receipt() -> None:
    receipt = publication_result()
    receipt["phase"] = "v83_v85_merged_omega"
    write_json(TRACE / f"{STEM}-git-publication-result-v1.json", receipt)
    write_text(TRACE / f"{STEM}-git-publication-result-v1.md", report_markdown(f"{STEM} git publication result", receipt))


def main() -> int:
    parser = argparse.ArgumentParser(description="Write merged v83-v85 Omega artifacts.")
    parser.add_argument("--mode", choices=["plan", "closeout", "receipt"], default="plan")
    args = parser.parse_args()
    if args.mode == "plan":
        write_merged_plan()
    elif args.mode == "closeout":
        write_closeout()
    else:
        write_receipt()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
