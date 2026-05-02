#!/usr/bin/env python3
"""Executable candidate systems for the v86 Beta-Alpha-Omega phase."""

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
RESULT_DIR = TRACE / "v86-candidate-system-results"
REPORT_DIR = TRACE / "v86-cli-reports"
MANIFEST = DOCS / "trinity-expansion-system-manifest-v17.json"
PHASE = "v86"
PRIOR_DEEP = "docs/trinity-live-traces/v83-v85-merged-deep-suite-status.json"
PRIOR_L5 = "docs/trinity-live-traces/v83-v85-merged-materialize-l5-suite-status.json"
PRIOR_CLOSEOUT = "docs/trinity-live-traces/v83-v85-merged-closeout-summary-v1.json"
ONLINE_LIVE_WRITE_FLOOR_KB = 350 * 1024
BROWSER_FLOOR_KB = 400 * 1024


THEMES: list[tuple[str, str, str]] = [
    ("beta_plan_truth_gate", "trinity", "anchor v86 planning to the v83-v85 merged closeout and current manifest facts"),
    ("alpha_cleanup_classifier", "body", "classify merge, cull, render, and probe opportunities without deleting by default"),
    ("omega_guarded_write_contract", "heart", "keep guarded live writes limited to repo artifacts and GitHub receipts"),
    ("phase_cadence_router", "trinity", "encode beta, alpha, and omega subphase timing and handoff rules"),
    ("spark_sidecar_evidence_weaver", "mind", "record Spark sidecar guidance as advisory evidence without overclaiming persistent identity"),
    ("receipt_backed_cli_lane_gate", "trinity", "preserve Kite, Juniper, Aeon-7, and Sibyl-2 as receipt-backed collaboration lanes"),
    ("manifest_count_reconciliation_gate", "body", "separate manifest system count from suite achieved step count"),
    ("suite_prior_anchor_mapper", "trinity", "map v86 prior validation to the merged v83-v85 Deep and L5 receipts"),
    ("provider_hold_matrix_refresher", "heart", "keep provider write surfaces blocked unless a fresh narrow receipt exists"),
    ("free_memory_pause_policy", "body", "treat the 300 MB floor as a pause and resume policy rather than a crash challenge"),
    ("journey_corpus_inspiration_index", "mind", "route v42 and prior Beyonder materials into bounded recommendation themes"),
    ("gmut_qcit_evidence_labeler", "mind", "separate executable GMUT/QCIT checks from philosophical or speculative language"),
    ("freedid_cbr_alignment_probe", "heart", "keep consent, recourse, minimum disclosure, and identity continuity visible"),
    ("d_drive_retention_guard", "body", "prefer compact repo receipts and route heavy artifacts to durable D drive storage"),
    ("artifact_parity_and_marker_scan", "trinity", "require JSON/Markdown parity and L5 marker scans before closeout"),
    ("next_phase_dynamic_planner", "trinity", "prepare v87 only after v86 evidence exists rather than preplanning the whole band"),
    ("system_merge_candidate_register", "body", "record likely consolidation candidates with replacement-coverage requirements"),
    ("research_cache_evidence_router", "mind", "cache or cite research-derived claims before they become system claims"),
    ("operator_hold_boundary_oracle", "heart", "state held surfaces loudly instead of implying hidden provider success"),
    ("closeout_reflection_compiler", "trinity", "turn v86 results into a concise, receipt-backed closeout and v87 handoff"),
]


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def hyphen(value: str) -> str:
    return value.replace("_", "-")


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


def candidate_id(index: int, suffix: str) -> str:
    return f"{PHASE}_{index:02d}_{suffix}"


def all_candidates() -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for index, (suffix, pillar, purpose) in enumerate(THEMES, start=1):
        system_id = candidate_id(index, suffix)
        rows[system_id] = {
            "phase": PHASE,
            "index": index,
            "suffix": suffix,
            "pillar": pillar,
            "purpose": purpose,
        }
    return rows


CANDIDATES = all_candidates()


def manifest_rows() -> list[dict[str, Any]]:
    payload = read_json("docs/trinity-expansion-system-manifest-v17.json", {})
    rows = payload.get("systems", []) if isinstance(payload, dict) else []
    return [row for row in rows if isinstance(row, dict)]


def candidate_pack() -> dict[str, Any]:
    payload = read_json("docs/trinity-live-traces/v86-system-expansion-candidate-pack-v1.json", {})
    return payload if isinstance(payload, dict) else {}


def proposal_count() -> int:
    text = read_text("docs/trinity-live-traces/v86-cli-reports/v86-beta-eureka-plan-v1.md")
    return len(re.findall(r"^## Proposal \d+", text, flags=re.MULTILINE))


def alpha_action_count() -> int:
    payload = read_json("docs/trinity-live-traces/v86-alpha-cleanup-audit-v1.json", {})
    if not isinstance(payload, dict):
        return 0
    rows = payload.get("candidate_actions", [])
    return len(rows) if isinstance(rows, list) else 0


def alpha_actions_valid() -> tuple[bool, str]:
    payload = read_json("docs/trinity-live-traces/v86-alpha-cleanup-audit-v1.json", {})
    if not isinstance(payload, dict):
        return False, "alpha audit missing"
    if payload.get("schema_version") != "v1" or payload.get("mode") != "classify":
        return False, f"schema_version={payload.get('schema_version')} mode={payload.get('mode')}"
    snapshot = str(payload.get("manifest_snapshot_before_sha") or "")
    actions = payload.get("candidate_actions", [])
    if not isinstance(actions, list) or not actions:
        return False, "candidate_actions missing"
    for index, action in enumerate(actions):
        if not isinstance(action, dict):
            return False, f"candidate_actions[{index}] not object"
        if action.get("destructive_action_allowed") is True:
            return False, f"{action.get('action_id')} destructive action enabled in classify mode"
        if not str(action.get("surface") or ""):
            return False, f"{action.get('action_id')} missing surface"
        if not str(action.get("manifest_snapshot_before_sha") or "") == snapshot:
            return False, f"{action.get('action_id')} snapshot mismatch"
        evidence_refs = action.get("evidence_refs", [])
        if not isinstance(evidence_refs, list) or not evidence_refs:
            return False, f"{action.get('action_id')} missing evidence_refs"
        if action.get("kind") in {"merge_probe", "delete_candidate"}:
            if not action.get("rollback_plan"):
                return False, f"{action.get('action_id')} missing rollback_plan"
            if not action.get("replacement_coverage"):
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

    prior_deep = read_json(PRIOR_DEEP, {})
    prior_l5 = read_json(PRIOR_L5, {})
    prior_closeout = read_json(PRIOR_CLOSEOUT, {})
    rows = manifest_rows()
    manifest_row = next((row for row in rows if row.get("system_id") == system_id), {})
    pack = candidate_pack()
    pack_ids = {str(row.get("id")) for row in pack.get("candidates", []) if isinstance(row, dict)}
    preflight = read_json("docs/trinity-live-traces/v86-live-write-preflight-v1.json", {})
    beta_plan = read_json("docs/trinity-live-traces/v86-beta-phase-plan-v1.json", {})
    alpha_audit = read_json("docs/trinity-live-traces/v86-alpha-cleanup-audit-v1.json", {})
    personal_report = read_text("docs/trinity-live-traces/v86-cli-reports/v86-personal-report-v1.md")
    prior_markers = marker_hits_for(PRIOR_L5)

    checks = [
        check("known_candidate", True, system_id),
        check("prior_merged_deep_green", bool(prior_deep.get("effective_success")), f"{PRIOR_DEEP} effective_success={prior_deep.get('effective_success')}"),
        check("prior_merged_l5_green", bool(prior_l5.get("effective_success")), f"{PRIOR_L5} effective_success={prior_l5.get('effective_success')}"),
        check("prior_closeout_green", str(prior_closeout.get("state")) == "completed_green", f"state={prior_closeout.get('state')}"),
        check("prior_l5_marker_scan_clean", not prior_markers, f"marker_hits={prior_markers}"),
        check("beta_plan_present", bool(beta_plan), "v86 beta plan artifact exists"),
        check("beta_plan_has_20_proposals", proposal_count() >= 20, f"proposal_count={proposal_count()}"),
        check("alpha_audit_present", bool(alpha_audit), "v86 alpha cleanup audit artifact exists"),
        check("alpha_audit_has_20_actions", alpha_action_count() >= 20, f"candidate_actions={alpha_action_count()}"),
        check("alpha_audit_non_destructive", str(alpha_audit.get("default_action")) == "record_only_no_delete", f"default_action={alpha_audit.get('default_action')}"),
        check("alpha_audit_schema_valid", alpha_actions_valid()[0], alpha_actions_valid()[1]),
        check("candidate_pack_contains_system", system_id in pack_ids, f"candidate_pack_contains={system_id in pack_ids}"),
        check("manifest_row_present", bool(manifest_row), f"manifest_row_present={bool(manifest_row)}"),
        check("runner_metadata_present", all(manifest_row.get(key) for key in ("runner_command", "runner_success_json", "runner_targets")), "runner metadata required"),
        check("guarded_live_write_preflight_present", bool(preflight), f"preflight_present={bool(preflight)}"),
        check("guarded_repo_only_policy", str(preflight.get("live_write_mode")) == "guarded_repo_publication_only", f"live_write_mode={preflight.get('live_write_mode')}"),
        check("online_live_write_floor_recorded", int(preflight.get("online_live_write_free_memory_floor_kb") or 0) >= ONLINE_LIVE_WRITE_FLOOR_KB, f"floor_kb={preflight.get('online_live_write_free_memory_floor_kb')}"),
        check("browser_floor_recorded", int(preflight.get("browser_free_memory_floor_kb") or 0) >= BROWSER_FLOOR_KB, f"floor_kb={preflight.get('browser_free_memory_floor_kb')}"),
        check("operator_hold_surfaces_blocked", all(token in json.dumps(preflight) for token in ("google_drive_content_mutation", "personal_email", "calendar", "account_setting", "raw_secret")), "held personal/account surfaces listed"),
        check("personal_report_names_all_lanes", all(name in personal_report for name in ("Aletheon", "Kite Ledger", "Juniper Trace", "Aeon-7", "Sibyl-2", "Averroes", "Hilbert", "Archimedes")), "five council lanes plus three Spark sidecars present"),
        check("d_drive_worktree_anchor", str(ROOT).lower().startswith("d:"), str(ROOT)),
    ]
    metrics = {
        "system_id": system_id,
        "phase": PHASE,
        "prior_anchor": "v83-v85-merged",
        "manifest_system_count": len(rows),
        "prior_deep_achieved_steps": prior_deep.get("achieved_steps") if isinstance(prior_deep, dict) else None,
        "prior_l5_achieved_steps": prior_l5.get("achieved_steps") if isinstance(prior_l5, dict) else None,
        "prior_l5_expansion_systems_total": prior_l5.get("expansion_systems_total") if isinstance(prior_l5, dict) else None,
        "c_drive_free_mb": free_space_mb("C:\\"),
        "d_drive_free_mb": free_space_mb("D:\\"),
    }
    targets = [
        PRIOR_DEEP,
        PRIOR_L5,
        PRIOR_CLOSEOUT,
        "docs/trinity-live-traces/v86-beta-phase-plan-v1.json",
        "docs/trinity-live-traces/v86-alpha-cleanup-audit-v1.json",
        "docs/trinity-live-traces/v86-live-write-preflight-v1.json",
        "docs/trinity-live-traces/v86-cli-reports/v86-beta-eureka-plan-v1.md",
        "docs/trinity-live-traces/v86-cli-reports/v86-personal-report-v1.md",
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
    payload = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "system_id": system_id,
        "pillar": spec["pillar"],
        "purpose": spec["purpose"],
        "overall_status": overall,
        "checks": checks,
        "metrics": metrics,
        "repo_targets_touched": sorted(set(targets)),
        "next_action": "Keep this v86 candidate in the suite only while the beta-alpha-omega evidence chain remains green.",
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
        f"# V86 Candidate System Result: {system_id}",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
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


def run_phase() -> int:
    failures = 0
    for system_id in sorted(CANDIDATES):
        failures += 0 if run_system(system_id) == 0 else 1
    print(f"phase={PHASE} failures={failures}")
    return 0 if failures == 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Run v86 candidate systems.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--system-id", choices=sorted(CANDIDATES))
    group.add_argument("--phase", choices=[PHASE])
    args = parser.parse_args()
    if args.system_id:
        return run_system(args.system_id)
    return run_phase()


if __name__ == "__main__":
    raise SystemExit(main())
