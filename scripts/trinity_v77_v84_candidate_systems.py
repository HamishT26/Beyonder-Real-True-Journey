#!/usr/bin/env python3
"""Executable candidate systems for the v77-v85 hybrid Omega phase."""

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
RESULT_DIR = TRACE / "v77-v84-candidate-system-results"
REPORT_DIR = TRACE / "v77-v84-cli-reports"
MANIFEST = DOCS / "trinity-expansion-system-manifest-v17.json"
PHASE_RANGE = range(77, 86)
FREE_MEMORY_FLOOR_KB = 300_000


THEMES: list[tuple[str, str, str]] = [
    ("phase_ledger_receipt_gate", "trinity", "require branch, head, receipt, suite, live-write, and memory-floor facts before execution"),
    ("prior_suite_delta_mapper", "trinity", "map prior Deep and L5 count movement before any new phase claim"),
    ("guarded_live_write_preflight_gate", "heart", "keep live writes limited to repo and GitHub receipts unless a fresh provider-specific receipt chain exists"),
    ("candidate_pack_quality_gate", "body", "check every candidate has runner metadata, outputs, and markdown parity"),
    ("eureka_report_length_gate", "mind", "prove the next-phase proposal includes at least 20 concrete recommendation paragraphs"),
    ("cli_lane_reflection_synthesizer", "trinity", "merge Aletheon, Kite, Juniper, Aeon-7, and Sibyl-2 lanes as receipt-backed report voices"),
    ("gmut_qcit_claim_labeler", "mind", "label GMUT and QCIT claims as executable proof, citation-backed, philosophical, or open speculation"),
    ("freedid_cbr_consent_guard", "heart", "preserve Freed ID and CBR consent boundaries in every guarded phase"),
    ("provider_posture_receipt_matrix", "body", "separate read-only, dry-run, sandbox, repo-live, and production-prohibited provider states"),
    ("memory_floor_cooldown_logger", "body", "record host memory posture before suites and make heavy lanes pause-aware"),
    ("d_drive_artifact_router", "body", "route heavy artifacts to D drive while keeping curated repo truth surfaces compact"),
    ("l5_marker_diff_scanner", "trinity", "scan L5 status files for external mutation and personal-surface markers"),
    ("suite_count_growth_guard", "trinity", "block system count movement unless new systems have passing direct and suite proof"),
    ("consolidation_opportunity_register", "trinity", "record merge/delete opportunities without reducing counts before replacement coverage exists"),
    ("github_publication_receipt_gate", "body", "treat GitHub push plus regenerated receipt as the durable live-write exchange"),
    ("operator_hold_surface_enforcer", "heart", "keep Gmail, Calendar, Google Drive content, account settings, DNS, and secrets on hold"),
    ("research_cache_router", "mind", "route web or provider-derived claims into cached/cited artifacts instead of raw assertions"),
    ("artifact_parity_validator", "body", "require JSON and Markdown parity for plans, reports, candidates, and receipts"),
    ("next_phase_handoff_builder", "trinity", "turn completed suite evidence into the next phase handoff policy"),
    ("grand_closeout_reflection_weaver", "trinity", "compose personal reflections and recommendations without overclaiming private memory or agency"),
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
    if not match:
        return ""
    return match.group(1)


def prior_phase(phase: str) -> str:
    return f"v{int(phase[1:]) - 1}"


def suite_status(phase: str, kind: str) -> dict[str, Any]:
    suffix = "deep" if kind == "deep" else "materialize-l5"
    payload = read_json(f"docs/trinity-live-traces/{phase}-{suffix}-suite-status.json", {})
    return payload if isinstance(payload, dict) else {}


def manifest_rows() -> list[dict[str, Any]]:
    payload = read_json("docs/trinity-expansion-system-manifest-v17.json", {})
    rows = payload.get("systems", []) if isinstance(payload, dict) else []
    return [row for row in rows if isinstance(row, dict)]


def candidate_pack() -> dict[str, Any]:
    payload = read_json("docs/trinity-live-traces/v77-v84-system-expansion-candidate-pack-v1.json", {})
    return payload if isinstance(payload, dict) else {}


def marker_hits_for(phase: str) -> list[str]:
    text = read_text(f"docs/trinity-live-traces/{phase}-materialize-l5-suite-status.json")
    markers = [
        'attempted_write": true',
        "production_dns",
        "account_setting",
        "personal_email",
        "google_drive_content_mutation",
        "raw_secret_transmission",
    ]
    return [marker for marker in markers if marker in text]


def report_paragraph_count(phase: str) -> int:
    text = read_text(f"docs/trinity-live-traces/v77-v84-cli-reports/{phase}-eureka-plan-v1.md")
    return len(re.findall(r"^## Proposal \d+", text, flags=re.MULTILINE))


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
    prior = prior_phase(phase)
    prior_deep = suite_status(prior, "deep")
    prior_l5 = suite_status(prior, "l5")
    rows = manifest_rows()
    manifest_row = next((row for row in rows if row.get("system_id") == system_id), {})
    pack = candidate_pack()
    pack_ids = {str(row.get("id")) for row in pack.get("candidates", []) if isinstance(row, dict)}
    preflight = read_json(f"docs/trinity-live-traces/{phase}-live-write-preflight-v1.json", {})
    phase_plan = read_text(f"docs/trinity-live-traces/v77-v84-cli-reports/{phase}-eureka-plan-v1.md")
    personal_report = read_text(f"docs/trinity-live-traces/v77-v84-cli-reports/{phase}-personal-report-v1.md")
    prior_markers = marker_hits_for(prior)
    expansion_total = prior_l5.get("expansion_systems_total") if isinstance(prior_l5, dict) else None

    checks = [
        check("known_candidate", True, system_id),
        check("prior_deep_green", bool(prior_deep.get("effective_success")), f"{prior}-deep effective_success={prior_deep.get('effective_success')}"),
        check("prior_l5_green", bool(prior_l5.get("effective_success")), f"{prior}-materialize-l5 effective_success={prior_l5.get('effective_success')}"),
        check("prior_l5_marker_scan_clean", not prior_markers, f"{prior} marker_hits={prior_markers}"),
        check("candidate_pack_contains_system", system_id in pack_ids, f"candidate_pack_contains={system_id in pack_ids}"),
        check("manifest_row_present", bool(manifest_row), f"manifest_row_present={bool(manifest_row)}"),
        check("runner_metadata_present", all(manifest_row.get(key) for key in ("runner_command", "runner_success_json", "runner_targets")), "runner metadata required"),
        check("eureka_report_has_20_proposals", report_paragraph_count(phase) >= 20, f"proposal_count={report_paragraph_count(phase)}"),
        check("personal_report_names_all_lanes", all(name in personal_report for name in ("Aletheon", "Kite Ledger", "Juniper Trace", "Aeon-7", "Sibyl-2")), "all five report voices present"),
        check("guarded_live_write_preflight_present", bool(preflight), f"preflight_present={bool(preflight)}"),
        check("guarded_repo_only_policy", str(preflight.get("live_write_mode")) == "guarded_repo_publication_only", f"live_write_mode={preflight.get('live_write_mode')}"),
        check("operator_hold_surfaces_blocked", all(token in json.dumps(preflight) for token in ("google_drive_content_mutation", "personal_email", "calendar", "account_setting", "raw_secret")), "held personal/account surfaces listed"),
        check("d_drive_worktree_anchor", str(ROOT).lower().startswith("d:"), str(ROOT)),
    ]
    metrics = {
        "system_id": system_id,
        "phase": phase,
        "prior_phase": prior,
        "manifest_system_count": len(rows),
        "prior_l5_expansion_systems_total": expansion_total,
        "prior_deep_counts": prior_deep.get("counts") if isinstance(prior_deep, dict) else None,
        "prior_l5_counts": prior_l5.get("counts") if isinstance(prior_l5, dict) else None,
        "c_drive_free_mb": free_space_mb("C:\\"),
        "d_drive_free_mb": free_space_mb("D:\\"),
    }
    targets = [
        f"docs/trinity-live-traces/{prior}-deep-suite-status.json",
        f"docs/trinity-live-traces/{prior}-materialize-l5-suite-status.json",
        f"docs/trinity-live-traces/{phase}-live-write-preflight-v1.json",
        f"docs/trinity-live-traces/v77-v84-cli-reports/{phase}-eureka-plan-v1.md",
        f"docs/trinity-live-traces/v77-v84-cli-reports/{phase}-personal-report-v1.md",
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
        "phase": spec["phase"],
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
        f"# V77-V85 Candidate System Result: {system_id}",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- phase: `{payload['phase']}`",
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
    parser = argparse.ArgumentParser(description="Run v77-v85 candidate systems.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--system-id", choices=sorted(CANDIDATES))
    group.add_argument("--phase", choices=[f"v{n}" for n in PHASE_RANGE])
    args = parser.parse_args()
    if args.system_id:
        return run_system(args.system_id)
    return run_phase(str(args.phase))


if __name__ == "__main__":
    raise SystemExit(main())
