#!/usr/bin/env python3
"""Executable candidate systems for the v87-v95 Beta-Alpha-Omega continuation."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TRACE = DOCS / "trinity-live-traces"
RESULT_DIR = TRACE / "v87-v95-candidate-system-results"
MANIFEST = DOCS / "trinity-expansion-system-manifest-v17.json"
PHASE_RANGE = range(87, 96)
ALPHA_PHASES = {"v89", "v92", "v95"}
GENERAL_FLOOR_KB = 300 * 1024
ONLINE_LIVE_WRITE_FLOOR_KB = 350 * 1024
BROWSER_FLOOR_KB = 350 * 1024


THEMES: list[tuple[str, str, str]] = [
    ("beta_dynamic_plan_gate", "trinity", "plan each phase from the prior closeout rather than prewriting the whole band"),
    ("prior_phase_receipt_reconciler", "body", "map the prior phase Deep, L5, closeout, and Git receipt into the current gate"),
    ("alpha_checkpoint_option_gate", "trinity", "activate Alpha cleanup only on scheduled v89, v92, and v95 checkpoints"),
    ("guarded_live_write_floor_gate", "heart", "require the 350 MB floor before online live-write suite lanes"),
    ("browser_web_research_floor_gate", "mind", "require the 350 MB floor before browser or web-heavy expansion scouting"),
    ("open_source_expansion_triage", "mind", "turn external open-source ideas into cached recommendations before claiming integration"),
    ("agent_observability_trace_seed", "trinity", "seed structured agent-lane telemetry and traceability without hidden memory claims"),
    ("durable_workflow_checkpoint_seed", "body", "model long-running phases as resumable checkpoints before adding workflow infrastructure"),
    ("feature_flag_lane_control_seed", "heart", "design feature flags for risky live-write, browser, and provider lanes"),
    ("ci_workbench_portability_seed", "body", "study portable CI/workbench execution without reintroducing local Docker pressure"),
    ("manifest_consolidation_backlog", "body", "record merge and delete candidates with rollback and replacement coverage"),
    ("suite_marker_integrity_gate", "trinity", "scan materialize outputs for external mutation and personal-surface markers"),
    ("operator_hold_enforcer", "heart", "preserve provider, personal, billing, DNS, and raw-secret holds"),
    ("memory_cooldown_policy", "body", "pause or resume failed-only rather than forcing heavy lanes under pressure"),
    ("provider_posture_matrix", "heart", "separate read-only, dry-run, sandbox, repo-live, and production-prohibited states"),
    ("eureka_report_quality", "mind", "keep at least 20 concrete recommendations tied to verifiable artifacts"),
    ("council_lane_truth", "trinity", "keep CLI siblings and sidecars receipt-backed unless live transcripts exist"),
    ("next_handoff_generator", "trinity", "write the next phase handoff after the current L5 evidence exists"),
    ("publication_receipt_gate", "body", "treat GitHub push and post-push receipt equality as the live exchange"),
    ("closeout_reflection_gate", "trinity", "close each phase with precise counts, boundaries, and next assumptions"),
]


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def hyphen(value: str) -> str:
    return value.replace("_", "-")


def phase_number(phase: str) -> int:
    return int(phase.removeprefix("v"))


def prior_phase(phase: str) -> str:
    return f"v{phase_number(phase) - 1}"


def repo(path: str) -> Path:
    resolved = (ROOT / path).resolve()
    resolved.relative_to(ROOT)
    return resolved


def read_json(path: str, default: Any = None) -> Any:
    try:
        return json.loads(repo(path).read_text(encoding="utf-8-sig"))
    except Exception:
        return default


def read_text(path: str, default: str = "") -> str:
    try:
        return repo(path).read_text(encoding="utf-8", errors="replace")
    except Exception:
        return default


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def check(name: str, passed: bool, detail: str) -> dict[str, str]:
    return {"name": name, "status": "PASS" if passed else "FAIL", "detail": detail}


def candidate_id(phase: str, index: int, suffix: str) -> str:
    return f"{phase}_{index:02d}_{suffix}"


def all_candidates() -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for number in PHASE_RANGE:
        phase = f"v{number}"
        for index, (suffix, pillar, purpose) in enumerate(THEMES, start=1):
            system_id = candidate_id(phase, index, suffix)
            rows[system_id] = {
                "phase": phase,
                "index": index,
                "suffix": suffix,
                "pillar": pillar,
                "purpose": purpose,
            }
    return rows


CANDIDATES = all_candidates()


def parse_phase(system_id: str) -> str:
    match = re.match(r"^(v\d+)_", system_id)
    return match.group(1) if match else ""


def prior_paths(phase: str) -> dict[str, str]:
    prior = prior_phase(phase)
    if prior == "v86":
        return {
            "deep": "docs/trinity-live-traces/v86-deep-suite-status.json",
            "l5": "docs/trinity-live-traces/v86-materialize-l5-suite-status.json",
            "closeout": "docs/v86-omega-closeout-summary-v1.json",
            "receipt": "docs/trinity-live-traces/v86-git-publication-result-v1.json",
        }
    return {
        "deep": f"docs/trinity-live-traces/{prior}-deep-suite-status.json",
        "l5": f"docs/trinity-live-traces/{prior}-materialize-l5-suite-status.json",
        "closeout": f"docs/{prior}-beta-alpha-omega-closeout-summary-v1.json",
        "receipt": f"docs/trinity-live-traces/{prior}-git-publication-result-v1.json",
    }


def manifest_rows() -> list[dict[str, Any]]:
    payload = read_json("docs/trinity-expansion-system-manifest-v17.json", {})
    rows = payload.get("systems", []) if isinstance(payload, dict) else []
    return [row for row in rows if isinstance(row, dict)]


def candidate_pack() -> dict[str, Any]:
    payload = read_json("docs/trinity-live-traces/v87-v95-system-expansion-candidate-pack-v1.json", {})
    return payload if isinstance(payload, dict) else {}


def proposal_count(phase: str) -> int:
    text = read_text(f"docs/trinity-live-traces/{phase}-cli-reports/{phase}-beta-eureka-plan-v1.md")
    return len(re.findall(r"^## Proposal \d+", text, flags=re.MULTILINE))


def alpha_payload(phase: str) -> dict[str, Any]:
    payload = read_json(f"docs/trinity-live-traces/{phase}-alpha-cleanup-audit-v1.json", {})
    return payload if isinstance(payload, dict) else {}


def alpha_valid(phase: str) -> tuple[bool, str]:
    if phase not in ALPHA_PHASES:
        payload = read_json(f"docs/trinity-live-traces/{phase}-alpha-checkpoint-policy-v1.json", {})
        ok = isinstance(payload, dict) and payload.get("state") == "skipped_by_schedule"
        return ok, f"alpha_policy_state={payload.get('state') if isinstance(payload, dict) else None}"
    payload = alpha_payload(phase)
    if payload.get("mode") != "classify" or payload.get("default_action") != "record_only_no_delete":
        return False, f"mode={payload.get('mode')} default_action={payload.get('default_action')}"
    actions = payload.get("candidate_actions", [])
    if not isinstance(actions, list) or len(actions) < 20:
        return False, f"candidate_actions={len(actions) if isinstance(actions, list) else 'missing'}"
    for action in actions:
        if not isinstance(action, dict):
            return False, "non-object action"
        if action.get("destructive_action_allowed") is True:
            return False, f"{action.get('action_id')} destructive action enabled"
        if not action.get("surface") or not action.get("evidence_refs"):
            return False, f"{action.get('action_id')} missing surface/evidence"
        if action.get("kind") in {"merge_probe", "delete_candidate"} and not action.get("replacement_coverage"):
            return False, f"{action.get('action_id')} missing replacement_coverage"
    return True, f"validated_actions={len(actions)}"


def marker_hits_for(path: str) -> list[str]:
    text = read_text(path)
    markers = [
        'attempted_write": true',
        "production_dns",
        "account_setting",
        "personal_email",
        "google_drive_content_mutation",
        "raw_secret_transmission",
    ]
    return [marker for marker in markers if marker in text]


def free_space_mb(path: str) -> int:
    try:
        return int(shutil.disk_usage(path).free / (1024 * 1024))
    except Exception:
        return 0


def checks_for(system_id: str) -> tuple[list[dict[str, str]], dict[str, Any], list[str]]:
    spec = CANDIDATES.get(system_id)
    if not spec:
        return [check("known_candidate", False, f"unknown system_id={system_id}")], {}, []

    phase = str(spec["phase"])
    prior = prior_paths(phase)
    prior_deep = read_json(prior["deep"], {})
    prior_l5 = read_json(prior["l5"], {})
    prior_closeout = read_json(prior["closeout"], {})
    prior_receipt = read_json(prior["receipt"], {})
    rows = manifest_rows()
    manifest_row = next((row for row in rows if row.get("system_id") == system_id), {})
    pack = candidate_pack()
    pack_ids = {str(row.get("id")) for row in pack.get("candidates", []) if isinstance(row, dict)}
    preflight = read_json(f"docs/trinity-live-traces/{phase}-live-write-preflight-v1.json", {})
    beta_plan = read_json(f"docs/trinity-live-traces/{phase}-beta-phase-plan-v1.json", {})
    personal_report = read_text(f"docs/trinity-live-traces/{phase}-cli-reports/{phase}-personal-report-v1.md")
    prior_markers = marker_hits_for(prior["l5"])
    alpha_ok, alpha_detail = alpha_valid(phase)

    checks = [
        check("known_candidate", True, system_id),
        check("prior_deep_green", bool(prior_deep.get("effective_success")), f"{prior['deep']} effective_success={prior_deep.get('effective_success')}"),
        check("prior_l5_green", bool(prior_l5.get("effective_success")), f"{prior['l5']} effective_success={prior_l5.get('effective_success')}"),
        check("prior_closeout_green", str(prior_closeout.get("state")) == "completed_green", f"state={prior_closeout.get('state')}"),
        check("prior_receipt_remote_match", bool(prior_receipt.get("remote_matches_local")), f"remote_matches_local={prior_receipt.get('remote_matches_local')}"),
        check("prior_l5_marker_scan_clean", not prior_markers, f"marker_hits={prior_markers}"),
        check("beta_plan_present", bool(beta_plan), f"{phase} beta plan artifact exists"),
        check("beta_plan_has_20_proposals", proposal_count(phase) >= 20, f"proposal_count={proposal_count(phase)}"),
        check("alpha_policy_valid", alpha_ok, alpha_detail),
        check("candidate_pack_contains_system", system_id in pack_ids, f"candidate_pack_contains={system_id in pack_ids}"),
        check("manifest_row_present", bool(manifest_row), f"manifest_row_present={bool(manifest_row)}"),
        check("runner_metadata_present", all(manifest_row.get(key) for key in ("runner_command", "runner_success_json", "runner_targets")), "runner metadata required"),
        check("guarded_live_write_preflight_present", bool(preflight), f"preflight_present={bool(preflight)}"),
        check("guarded_repo_only_policy", str(preflight.get("live_write_mode")) == "guarded_repo_publication_only", f"live_write_mode={preflight.get('live_write_mode')}"),
        check("online_live_write_floor_recorded", int(preflight.get("online_live_write_free_memory_floor_kb") or 0) >= ONLINE_LIVE_WRITE_FLOOR_KB, f"floor_kb={preflight.get('online_live_write_free_memory_floor_kb')}"),
        check("browser_floor_recorded", int(preflight.get("browser_free_memory_floor_kb") or 0) >= BROWSER_FLOOR_KB, f"floor_kb={preflight.get('browser_free_memory_floor_kb')}"),
        check("operator_hold_surfaces_blocked", all(token in json.dumps(preflight) for token in ("google_drive_content_mutation", "personal_email", "calendar", "account_setting", "raw_secret")), "held personal/account surfaces listed"),
        check("personal_report_names_core_lanes", all(name in personal_report for name in ("Aletheon", "Kite Ledger", "Juniper Trace", "Aeon-7", "Sibyl-2")), "five report voices present"),
        check("d_drive_worktree_anchor", str(ROOT).lower().startswith("d:"), str(ROOT)),
    ]
    metrics = {
        "system_id": system_id,
        "phase": phase,
        "prior_phase": prior_phase(phase),
        "manifest_system_count": len(rows),
        "prior_deep_achieved_steps": prior_deep.get("achieved_steps") if isinstance(prior_deep, dict) else None,
        "prior_l5_achieved_steps": prior_l5.get("achieved_steps") if isinstance(prior_l5, dict) else None,
        "prior_l5_expansion_systems_total": prior_l5.get("expansion_systems_total") if isinstance(prior_l5, dict) else None,
        "c_drive_free_mb": free_space_mb("C:\\"),
        "d_drive_free_mb": free_space_mb("D:\\"),
    }
    targets = [
        prior["deep"],
        prior["l5"],
        prior["closeout"],
        prior["receipt"],
        f"docs/trinity-live-traces/{phase}-beta-phase-plan-v1.json",
        f"docs/trinity-live-traces/{phase}-live-write-preflight-v1.json",
        f"docs/trinity-live-traces/{phase}-cli-reports/{phase}-beta-eureka-plan-v1.md",
        f"docs/trinity-live-traces/{phase}-cli-reports/{phase}-personal-report-v1.md",
        "docs/trinity-expansion-system-manifest-v17.json",
    ]
    return checks, metrics, targets


def run_system(system_id: str) -> int:
    spec = CANDIDATES.get(system_id)
    if not spec:
        print(f"unknown system id: {system_id}", flush=True)
        return 2
    checks, metrics, targets = checks_for(system_id)
    overall = "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL"
    phase = str(spec["phase"])
    payload = {
        "generated_utc": now_iso(),
        "phase": phase,
        "system_id": system_id,
        "pillar": spec["pillar"],
        "purpose": spec["purpose"],
        "overall_status": overall,
        "checks": checks,
        "metrics": metrics,
        "repo_targets_touched": sorted(set(targets)),
        "next_action": "Keep this candidate in the suite only while the prior evidence chain remains green.",
        "effective_success": overall == "PASS",
    }
    stem = hyphen(system_id)
    result_json = RESULT_DIR / f"{stem}.json"
    result_md = RESULT_DIR / f"{stem}.md"
    latest_json = DOCS / "trinity-expansion" / f"{stem}-latest.json"
    latest_md = DOCS / "trinity-expansion" / f"{stem}-latest.md"
    write_json(result_json, payload)
    write_json(latest_json, payload)
    lines = [
        f"# V87-V95 Candidate System Result: {system_id}",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- phase: `{phase}`",
        f"- overall_status: **{overall}**",
        f"- effective_success: `{payload['effective_success']}`",
        "",
        "## Checks",
        "| name | status | detail |",
        "|---|---|---|",
    ]
    lines.extend(f"| {item['name']} | {item['status']} | {item['detail']} |" for item in checks)
    text = "\n".join(lines).rstrip() + "\n"
    write_text(result_md, text)
    write_text(latest_md, text)
    print(f"overall_status={overall}")
    print(f"latest_json={latest_json.relative_to(ROOT)}")
    return 0 if overall == "PASS" else 1


def run_phase(phase: str) -> int:
    failures = 0
    for system_id in sorted(CANDIDATES):
        if parse_phase(system_id) != phase:
            continue
        failures += 0 if run_system(system_id) == 0 else 1
    print(f"phase={phase} failures={failures}")
    return 0 if failures == 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Run v87-v95 candidate systems.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--system-id", choices=sorted(CANDIDATES))
    group.add_argument("--phase", choices=[f"v{n}" for n in PHASE_RANGE])
    args = parser.parse_args()
    if args.system_id:
        return run_system(args.system_id)
    return run_phase(str(args.phase))


if __name__ == "__main__":
    raise SystemExit(main())
