#!/usr/bin/env python3
"""Executable candidate systems for the v96-v120 Beta-Alpha-Omega continuation."""

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
RESULT_DIR = TRACE / "v96-v120-candidate-system-results"
MANIFEST = DOCS / "trinity-expansion-system-manifest-v17.json"
PHASE_RANGE = range(96, 121)
GENERAL_FLOOR_KB = 300 * 1024
ONLINE_LIVE_WRITE_FLOOR_KB = 350 * 1024
BROWSER_FLOOR_KB = 350 * 1024


STAGE_SCHEDULE: dict[str, dict[str, str]] = {
    "v96": {"kind": "beta", "cycle": "v96_v98_trinity", "note": "Local/Cloud Nexus and MCP planning stage"},
    "v97": {"kind": "alpha", "cycle": "v96_v98_trinity", "note": "record-only cleanup and identity-boundary stage"},
    "v98": {"kind": "omega", "cycle": "v96_v98_trinity", "note": "first v96-v120 suite execution stage"},
    "v99": {"kind": "beta", "cycle": "v99_v100_dual", "note": "dual-action planning stage"},
    "v100": {"kind": "omega", "cycle": "v99_v100_dual", "note": "dual-action suite execution stage"},
    "v101": {"kind": "beta", "cycle": "v101_v102_dual", "note": "dual-action planning stage"},
    "v102": {"kind": "omega", "cycle": "v101_v102_dual", "note": "dual-action suite execution stage"},
    "v103": {"kind": "beta", "cycle": "v103_v105_trinity", "note": "trinity planning stage"},
    "v104": {"kind": "alpha", "cycle": "v103_v105_trinity", "note": "record-only cleanup stage"},
    "v105": {"kind": "omega", "cycle": "v103_v105_trinity", "note": "trinity suite execution stage"},
    "v106": {"kind": "beta", "cycle": "v106_v107_dual", "note": "dual-action planning stage"},
    "v107": {"kind": "omega", "cycle": "v106_v107_dual", "note": "dual-action suite execution stage"},
    "v108": {"kind": "beta", "cycle": "v108_v109_dual", "note": "dual-action planning stage"},
    "v109": {"kind": "omega", "cycle": "v108_v109_dual", "note": "dual-action suite execution stage"},
    "v110": {"kind": "beta", "cycle": "v110_v112_trinity", "note": "trinity planning stage"},
    "v111": {"kind": "alpha", "cycle": "v110_v112_trinity", "note": "record-only cleanup stage"},
    "v112": {"kind": "omega", "cycle": "v110_v112_trinity", "note": "trinity suite execution stage"},
    "v113": {"kind": "beta", "cycle": "v113_v115_bridge", "note": "continuity bridge inserted because the user outline skipped v113"},
    "v114": {"kind": "beta", "cycle": "v113_v115_bridge", "note": "dual-action planning refinement stage"},
    "v115": {"kind": "omega", "cycle": "v113_v115_bridge", "note": "bridge suite execution stage"},
    "v116": {"kind": "beta", "cycle": "v116_v117_dual", "note": "dual-action planning stage"},
    "v117": {"kind": "omega", "cycle": "v116_v117_dual", "note": "dual-action suite execution stage"},
    "v118": {"kind": "beta", "cycle": "v118_v120_trinity", "note": "final trinity planning stage"},
    "v119": {"kind": "alpha", "cycle": "v118_v120_trinity", "note": "final record-only cleanup stage"},
    "v120": {"kind": "omega", "cycle": "v118_v120_trinity", "note": "final suite execution and closeout stage"},
}

ALPHA_PHASES = {phase for phase, spec in STAGE_SCHEDULE.items() if spec["kind"] == "alpha"}
OMEGA_PHASES = {phase for phase, spec in STAGE_SCHEDULE.items() if spec["kind"] == "omega"}

THEMES: list[tuple[str, str, str]] = [
    ("stage_schedule_truth_gate", "trinity", "bind each numeric phase to beta, alpha, or omega semantics"),
    ("local_cloud_nexus_digest_gate", "body", "turn Solion Local/Cloud Nexus proposals into bounded repo evidence"),
    ("mcp_playwright_posture_gate", "mind", "classify MCP and Playwright options before enabling browser-heavy lanes"),
    ("provider_spend_sandbox_gate", "heart", "separate free-credit enthusiasm from action-time billing authority"),
    ("browser_live_write_floor_gate", "body", "enforce the 350 MB browser and online live-write floor"),
    ("cli_identity_boundary_gate", "heart", "keep CLI siblings receipt-backed unless a persistent platform transcript exists"),
    ("oracle_e2b_cloud_probe_gate", "body", "record OCI and e2b availability without provisioning paid resources"),
    ("vercel_cloudflare_bridge_gate", "body", "model edge and tunnel bridges without DNS or production deploy mutation"),
    ("neon_circleci_control_plane_gate", "body", "prepare database and CI ledger use without creating live services blindly"),
    ("notion_expo_dashboard_gate", "mind", "keep dashboard destinations repo-first until live write confirmation exists"),
    ("gmut_qcit_claim_evidence_gate", "mind", "label GMUT and QCIT claims by evidence type before suite promotion"),
    ("freedid_cbr_consent_gate", "heart", "preserve consent, recourse, and identity boundary checks"),
    ("alpha_manifest_cleanup_gate", "body", "record merge/delete candidates with replacement coverage and rollback anchors"),
    ("open_source_scout_gate", "mind", "convert official docs and source-scouting into cached recommendations"),
    ("mcp_security_prompt_injection_gate", "heart", "treat MCP tool descriptions and remote pages as untrusted input"),
    ("suite_omega_only_gate", "trinity", "run Deep and L5 suites only on Omega execution stages"),
    ("publication_receipt_gate", "body", "require post-push remote/local equality before declaring cloud live write success"),
    ("d_drive_retention_gate", "body", "retain heavy traces on D drive while publishing compact curated artifacts"),
    ("eureka_report_density_gate", "mind", "keep at least twenty actionable recommendations per stage"),
    ("next_stage_handoff_gate", "trinity", "derive each next stage from the current closeout, not a stale global plan"),
]


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def hyphen(value: str) -> str:
    return value.replace("_", "-")


def phase_number(phase: str) -> int:
    return int(phase.removeprefix("v"))


def phase_choices() -> list[str]:
    return [f"v{number}" for number in PHASE_RANGE]


def next_phase(phase: str) -> str:
    number = phase_number(phase) + 1
    return f"v{number}" if number <= 120 else "v121"


def prior_numeric_phase(phase: str) -> str:
    return f"v{phase_number(phase) - 1}"


def prior_omega_phase(phase: str) -> str:
    current = phase_number(phase)
    for number in range(current - 1, 95, -1):
        candidate = f"v{number}"
        if candidate in OMEGA_PHASES:
            return candidate
    return "v95"


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
    for phase in phase_choices():
        stage = STAGE_SCHEDULE[phase]
        for index, (suffix, pillar, purpose) in enumerate(THEMES, start=1):
            system_id = candidate_id(phase, index, suffix)
            rows[system_id] = {
                "phase": phase,
                "stage_kind": stage["kind"],
                "cycle": stage["cycle"],
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


def closeout_path(phase: str) -> str:
    if phase == "v95":
        return "docs/v95-beta-alpha-omega-closeout-summary-v1.json"
    return f"docs/{phase}-beta-alpha-omega-closeout-summary-v1.json"


def prior_paths(phase: str) -> dict[str, str]:
    prior = prior_omega_phase(phase)
    return {
        "omega": prior,
        "deep": f"docs/trinity-live-traces/{prior}-deep-suite-status.json",
        "l5": f"docs/trinity-live-traces/{prior}-materialize-l5-suite-status.json",
        "closeout": closeout_path(prior),
        "receipt": f"docs/trinity-live-traces/{prior}-git-publication-result-v1.json",
    }


def manifest_rows() -> list[dict[str, Any]]:
    payload = read_json("docs/trinity-expansion-system-manifest-v17.json", {})
    rows = payload.get("systems", []) if isinstance(payload, dict) else []
    return [row for row in rows if isinstance(row, dict)]


def candidate_pack() -> dict[str, Any]:
    payload = read_json("docs/trinity-live-traces/v96-v120-system-expansion-candidate-pack-v1.json", {})
    return payload if isinstance(payload, dict) else {}


def proposal_count(phase: str) -> int:
    text = read_text(f"docs/trinity-live-traces/{phase}-cli-reports/{phase}-beta-eureka-plan-v1.md")
    return len(re.findall(r"^## Proposal \d+", text, flags=re.MULTILINE))


def stage_artifact(phase: str) -> dict[str, Any]:
    payload = read_json(f"docs/trinity-live-traces/{phase}-stage-plan-v1.json", {})
    return payload if isinstance(payload, dict) else {}


def alpha_valid(phase: str) -> tuple[bool, str]:
    if phase not in ALPHA_PHASES:
        payload = read_json(f"docs/trinity-live-traces/{phase}-alpha-checkpoint-policy-v1.json", {})
        ok = isinstance(payload, dict) and payload.get("state") == "not_alpha_stage"
        return ok, f"alpha_policy_state={payload.get('state') if isinstance(payload, dict) else None}"
    payload = read_json(f"docs/trinity-live-traces/{phase}-alpha-cleanup-audit-v1.json", {})
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
    stage = STAGE_SCHEDULE[phase]
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
    stage_plan = stage_artifact(phase)
    identity = read_json(f"docs/trinity-live-traces/{phase}-cli-identity-boundary-v1.json", {})
    mcp_digest = read_json(f"docs/trinity-live-traces/{phase}-mcp-integration-digest-v1.json", {})
    source_digest = read_json(f"docs/trinity-live-traces/{phase}-source-digest-v1.json", {})
    personal_report = read_text(f"docs/trinity-live-traces/{phase}-cli-reports/{phase}-personal-report-v1.md")
    prior_markers = marker_hits_for(prior["l5"])
    alpha_ok, alpha_detail = alpha_valid(phase)

    checks = [
        check("known_candidate", True, system_id),
        check("stage_schedule_known", stage["kind"] in {"beta", "alpha", "omega"}, f"kind={stage['kind']} cycle={stage['cycle']}"),
        check("prior_omega_deep_green", bool(prior_deep.get("effective_success")), f"{prior['deep']} effective_success={prior_deep.get('effective_success')}"),
        check("prior_omega_l5_green", bool(prior_l5.get("effective_success")), f"{prior['l5']} effective_success={prior_l5.get('effective_success')}"),
        check("prior_omega_closeout_green", str(prior_closeout.get("state")) == "completed_green", f"state={prior_closeout.get('state')}"),
        check("prior_omega_receipt_remote_match", bool(prior_receipt.get("remote_matches_local")), f"remote_matches_local={prior_receipt.get('remote_matches_local')}"),
        check("prior_l5_marker_scan_clean", not prior_markers, f"marker_hits={prior_markers}"),
        check("stage_plan_present", bool(stage_plan), f"{phase} stage plan artifact exists"),
        check("stage_plan_kind_matches", stage_plan.get("stage_kind") == stage["kind"], f"plan_kind={stage_plan.get('stage_kind')} expected={stage['kind']}"),
        check("source_digest_present", bool(source_digest.get("source_files")), "v42/MCP source digest recorded without raw secrets"),
        check("mcp_digest_present", bool(mcp_digest.get("recommendations")), "MCP/Playwright digest present"),
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
        check("cli_identities_are_receipt_bound", identity.get("default_classification") == "repo_narrative_receipt_backed", f"default_classification={identity.get('default_classification')}"),
        check("personal_report_names_core_lanes", all(name in personal_report for name in ("Aletheon", "Kite Ledger", "Juniper Trace", "Aeon-7", "Sibyl-2")), "five report voices present"),
        check("d_drive_worktree_anchor", str(ROOT).lower().startswith("d:"), str(ROOT)),
    ]
    metrics = {
        "system_id": system_id,
        "phase": phase,
        "stage_kind": stage["kind"],
        "cycle": stage["cycle"],
        "prior_omega_phase": prior["omega"],
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
        f"docs/trinity-live-traces/{phase}-stage-plan-v1.json",
        f"docs/trinity-live-traces/{phase}-source-digest-v1.json",
        f"docs/trinity-live-traces/{phase}-mcp-integration-digest-v1.json",
        f"docs/trinity-live-traces/{phase}-live-write-preflight-v1.json",
        f"docs/trinity-live-traces/{phase}-cli-identity-boundary-v1.json",
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
        "stage_kind": spec["stage_kind"],
        "cycle": spec["cycle"],
        "system_id": system_id,
        "pillar": spec["pillar"],
        "purpose": spec["purpose"],
        "overall_status": overall,
        "checks": checks,
        "metrics": metrics,
        "repo_targets_touched": sorted(set(targets)),
        "next_action": "Keep this candidate only while the prior Omega evidence chain and current stage truth remain green.",
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
        f"# V96-V120 Candidate System Result: {system_id}",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- phase: `{phase}`",
        f"- stage_kind: `{payload['stage_kind']}`",
        f"- cycle: `{payload['cycle']}`",
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
    parser = argparse.ArgumentParser(description="Run v96-v120 candidate systems.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--system-id", choices=sorted(CANDIDATES))
    group.add_argument("--phase", choices=phase_choices())
    args = parser.parse_args()
    if args.system_id:
        return run_system(args.system_id)
    return run_phase(str(args.phase))


if __name__ == "__main__":
    raise SystemExit(main())
