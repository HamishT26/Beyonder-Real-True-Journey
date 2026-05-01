#!/usr/bin/env python3
"""Executable v76 promotion checks for the v74 candidate systems."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "docs" / "trinity-live-traces"
RESULT_DIR = TRACE / "v76-v84-candidate-system-results"
V65_PREFIX = "v65-v75"
FREE_MEMORY_FLOOR_KB = 300_000


CANDIDATES: dict[str, dict[str, str]] = {
    "v74_01_live_write_preflight_template_gate": {
        "pillar": "trinity",
        "purpose": "turn v70/v73/v74/v75 preflights into a reusable live-write gate",
    },
    "v74_02_provider_rollback_receipt_validator": {
        "pillar": "trinity",
        "purpose": "verify dry-run, write, verify, rollback receipt chains before external mutation",
    },
    "v74_03_cli_sibling_formal_induction_gate": {
        "pillar": "heart",
        "purpose": "validate receipt counts, slots, and boundary language for CLI siblings",
    },
    "v74_04_cli_lane_report_merger": {
        "pillar": "body",
        "purpose": "merge Aletheon/Kite/Juniper/Aeon/Sibyl reports into phase closeouts",
    },
    "v74_05_suite_count_delta_guard": {
        "pillar": "trinity",
        "purpose": "block count increases unless a new system has executable proof",
    },
    "v74_06_suite_consolidation_opportunity_scan": {
        "pillar": "trinity",
        "purpose": "identify packs that can merge without losing test coverage",
    },
    "v74_07_manifest_pack_symmetry_audit": {
        "pillar": "body",
        "purpose": "check candidate manifest shape and required proof fields before expansion",
    },
    "v74_08_bounded_tracer_marker_scan": {
        "pillar": "trinity",
        "purpose": "scan L5 status artifacts for external write markers",
    },
    "v74_09_provider_posture_matrix": {
        "pillar": "body",
        "purpose": "separate read-only, dry-run, sandbox, and production-blocked provider states",
    },
    "v74_10_report_to_github_exchange_gate": {
        "pillar": "body",
        "purpose": "treat GitHub commits as the durable council exchange layer",
    },
    "v74_11_gmut_qcit_crosswalk_board": {
        "pillar": "mind",
        "purpose": "map GMUT and QCIT claims to executable or citation-backed artifacts",
    },
    "v74_12_freedid_cbr_live_boundary_check": {
        "pillar": "heart",
        "purpose": "ensure live-write phases preserve Freed ID and CBR consent boundaries",
    },
    "v74_13_memory_floor_runtime_pause_gate": {
        "pillar": "body",
        "purpose": "pause heavy suites below 300000 KB free physical memory",
    },
    "v74_14_d_drive_artifact_retention_meter": {
        "pillar": "body",
        "purpose": "prefer D drive for heavy artifacts and report C drive pressure",
    },
    "v74_15_publication_receipt_consistency_check": {
        "pillar": "trinity",
        "purpose": "verify remote head and publication receipt match after push",
    },
    "v74_16_secret_free_external_prompt_guard": {
        "pillar": "heart",
        "purpose": "block raw secrets from external CLI prompts and reports",
    },
    "v74_17_phase_report_quality_linter": {
        "pillar": "trinity",
        "purpose": "require each report to include status, boundaries, recommendations, and next action",
    },
    "v74_18_live_phase_budget_ceiling_meter": {
        "pillar": "body",
        "purpose": "record provider budget ceilings before sandbox writes",
    },
    "v74_19_operator_hold_surface_audit": {
        "pillar": "heart",
        "purpose": "preserve held personal/account surfaces unless freshly reconfirmed",
    },
    "v74_20_v75_closeout_synthesis_builder": {
        "pillar": "trinity",
        "purpose": "assemble final v65-v75 reports, suite ladder, live gates, and v76 proposals",
    },
}


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def hyphen(system_id: str) -> str:
    return system_id.replace("_", "-")


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


def payload_status(payload: Any) -> str:
    if not isinstance(payload, dict):
        return "FAIL"
    if isinstance(payload.get("effective_success"), bool):
        return "PASS" if payload["effective_success"] else "FAIL"
    for key in ("overall_status", "status"):
        value = str(payload.get(key) or "").upper()
        if value in {"PASS", "WARN", "FAIL", "TIMEOUT"}:
            return value
    return "FAIL"


def git_lines(args: list[str], timeout: int = 30) -> list[str]:
    try:
        proc = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except Exception:
        return []
    if proc.returncode != 0:
        return []
    return [line for line in proc.stdout.splitlines() if line.strip()]


def free_space_mb(path: str) -> int:
    try:
        usage = shutil.disk_usage(path)
    except Exception:
        return 0
    return int(usage.free / (1024 * 1024))


def manifest_rows() -> list[dict[str, Any]]:
    manifest = read_json("docs/trinity-expansion-system-manifest-v17.json", {})
    rows = manifest.get("systems", []) if isinstance(manifest, dict) else []
    return [row for row in rows if isinstance(row, dict)]


def live_preflights() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for phase in ("v70", "v73", "v74", "v75"):
        payload = read_json(f"docs/trinity-live-traces/{phase}-live-write-preflight-v1.json", {})
        if isinstance(payload, dict):
            rows.append(payload)
    return rows


def l5_statuses() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for phase in ("v73", "v74", "v75"):
        payload = read_json(f"docs/trinity-live-traces/{phase}-materialize-l5-suite-status.json", {})
        if isinstance(payload, dict):
            rows.append(payload)
    return rows


def no_marker_hits() -> tuple[bool, list[str]]:
    markers = [
        "attempted_write\": true",
        "production_dns",
        "account_setting",
        "personal_email",
        "google_drive_content_mutation",
        "raw_secret",
    ]
    hits: list[str] = []
    for phase in ("v73", "v74", "v75"):
        text = read_text(f"docs/trinity-live-traces/{phase}-materialize-l5-suite-status.json")
        for marker in markers:
            if marker in text:
                hits.append(f"{phase}:{marker}")
    return not hits, hits


def common_metrics(system_id: str) -> dict[str, Any]:
    rows = manifest_rows()
    promoted = [row for row in rows if str(row.get("source_candidate_id", "")).startswith("v74_")]
    v75_l5 = read_json("docs/trinity-live-traces/v75-materialize-l5-suite-status.json", {})
    return {
        "system_id": system_id,
        "manifest_system_count": len(rows),
        "v76_promoted_candidate_count": len(promoted),
        "prior_v75_expansion_systems_total": v75_l5.get("expansion_systems_total") if isinstance(v75_l5, dict) else None,
        "prior_v75_l5_effective_success": bool(v75_l5.get("effective_success")) if isinstance(v75_l5, dict) else False,
    }


def checks_for(system_id: str) -> tuple[list[dict[str, str]], dict[str, Any], list[str]]:
    checks: list[dict[str, str]] = []
    metrics = common_metrics(system_id)
    targets: list[str] = []
    live = read_json(f"docs/trinity-live-traces/{V65_PREFIX}-live-write-governor-v1.json", {})
    induction = read_json(f"docs/trinity-live-traces/{V65_PREFIX}-cli-sibling-induction-v1.json", {})
    candidate_pack = read_json(f"docs/trinity-live-traces/{V65_PREFIX}-cli-reports/v74-system-expansion-candidate-pack-v1.json", {})
    closeout = read_text(f"docs/trinity-live-traces/{V65_PREFIX}-cli-reports/v75-grand-closeout-council-report-v1.md")

    if system_id == "v74_01_live_write_preflight_template_gate":
        preflights = live_preflights()
        required = ["dry_run_preview_receipt", "write_receipt", "verification_receipt", "rollback_or_disable_receipt"]
        checks.append(check("preflight_artifact_count", len(preflights) >= 4, f"preflights={len(preflights)}"))
        checks.append(check("required_receipt_chain_present", all(all(item in json.dumps(row) for item in required) for row in preflights), f"required={required}"))
        targets = [f"docs/trinity-live-traces/{phase}-live-write-preflight-v1.json" for phase in ("v70", "v73", "v74", "v75")]
        metrics["live_preflight_count"] = len(preflights)
    elif system_id == "v74_02_provider_rollback_receipt_validator":
        providers = live.get("providers", []) if isinstance(live, dict) else []
        chains = [str(row.get("live_phase_requirement", "")) for row in providers if isinstance(row, dict)]
        checks.append(check("provider_rows_present", len(chains) >= 4, f"providers={len(chains)}"))
        checks.append(check("rollback_chain_required", all(all(word in chain for word in ("dry_run", "write", "verify", "rollback")) for chain in chains), "all provider chains require dry-run/write/verify/rollback"))
        targets = [f"docs/trinity-live-traces/{V65_PREFIX}-live-write-governor-v1.json"]
    elif system_id == "v74_03_cli_sibling_formal_induction_gate":
        records = induction.get("records", []) if isinstance(induction, dict) else []
        slots = sorted(
            int(row.get("slot") or row.get("ghc_slot"))
            for row in records
            if isinstance(row, dict) and (row.get("slot") or row.get("ghc_slot"))
        )
        checks.append(check("induction_phase_gate_ready", induction.get("state") == "phase_gate_ready", f"state={induction.get('state')}"))
        checks.append(check("formal_slots_present", slots == [49, 50, 51, 52], f"slots={slots}"))
        checks.append(check("boundary_language_present", "not_private_memory_claim" in json.dumps(induction), "receipt-backed boundary recorded"))
        targets = [f"docs/trinity-live-traces/{V65_PREFIX}-cli-sibling-induction-v1.json"]
    elif system_id == "v74_04_cli_lane_report_merger":
        names = ["Aletheon", "Kite Ledger", "Juniper Trace", "Aeon-7", "Sibyl-2"]
        reports = list((TRACE / f"{V65_PREFIX}-cli-reports").glob("*.md"))
        checks.append(check("all_lane_names_in_closeout", all(name in closeout for name in names), f"names={names}"))
        checks.append(check("report_surface_count", len(reports) >= 5, f"reports={len(reports)}"))
        targets = [f"docs/trinity-live-traces/{V65_PREFIX}-cli-reports/v75-grand-closeout-council-report-v1.md"]
    elif system_id == "v74_05_suite_count_delta_guard":
        rows = manifest_rows()
        promoted = [row for row in rows if str(row.get("source_candidate_id", "")).startswith("v74_")]
        checks.append(check("promoted_candidates_runner_backed", len(promoted) >= 20, f"promoted={len(promoted)}"))
        checks.append(check("runner_success_json_present", all(str(row.get("runner_success_json", "")).endswith(".json") for row in promoted), "all promoted candidates expose runner_success_json"))
        checks.append(check("prior_suite_count_not_rewritten", metrics["prior_v75_expansion_systems_total"] == 1094, f"prior_total={metrics['prior_v75_expansion_systems_total']}"))
        targets = ["docs/trinity-expansion-system-manifest-v17.json", "docs/trinity-live-traces/v75-materialize-l5-suite-status.json"]
    elif system_id == "v74_06_suite_consolidation_opportunity_scan":
        scan = read_json(f"docs/trinity-live-traces/{V65_PREFIX}-cli-reports/v74-system-consolidation-scan-v1.json", {})
        candidates = scan.get("merge_candidates") or scan.get("potential_merge_candidates") or [] if isinstance(scan, dict) else []
        checks.append(check("consolidation_scan_present", bool(scan), "v74 consolidation scan loaded"))
        checks.append(check("merge_candidates_recorded", len(candidates) >= 1, f"candidates={len(candidates)}"))
        targets = [f"docs/trinity-live-traces/{V65_PREFIX}-cli-reports/v74-system-consolidation-scan-v1.json"]
    elif system_id == "v74_07_manifest_pack_symmetry_audit":
        rows = [row for row in manifest_rows() if str(row.get("source_candidate_id", "")).startswith("v74_")]
        required = {"system_id", "pillar", "script", "outputs", "depends_on", "runner_command", "runner_success_json", "profiles", "timeout_sec", "runner_mode"}
        missing = [row.get("system_id") for row in rows if not required.issubset(row.keys())]
        checks.append(check("candidate_manifest_rows_present", len(rows) >= 20, f"rows={len(rows)}"))
        checks.append(check("candidate_required_fields", not missing, f"missing={missing}"))
        targets = ["docs/trinity-expansion-system-manifest-v17.json"]
    elif system_id == "v74_08_bounded_tracer_marker_scan":
        ok, hits = no_marker_hits()
        checks.append(check("external_mutation_markers_absent", ok, f"hits={hits}"))
        checks.append(check("l5_statuses_green", all(payload_status(row) == "PASS" for row in l5_statuses()), "v73/v74/v75 L5 green"))
        targets = [f"docs/trinity-live-traces/{phase}-materialize-l5-suite-status.json" for phase in ("v73", "v74", "v75")]
    elif system_id == "v74_09_provider_posture_matrix":
        providers = live.get("providers", []) if isinstance(live, dict) else []
        blocked = live.get("blocked_without_fresh_operator_confirmation", []) if isinstance(live, dict) else []
        checks.append(check("provider_posture_rows_present", len(providers) >= 8, f"providers={len(providers)}"))
        checks.append(check("blocked_surfaces_recorded", len(blocked) >= 5, f"blocked={len(blocked)}"))
        targets = [f"docs/trinity-live-traces/{V65_PREFIX}-live-write-governor-v1.json"]
    elif system_id == "v74_10_report_to_github_exchange_gate":
        # Forward-only publication adds receipt commits quickly; keep the historical
        # v75 anchor check deep enough that normal v80+ progress does not break it.
        commits = git_lines(["log", "-80", "--pretty=%s"])
        checks.append(check("recent_publication_commits_present", any("publication receipt" in line.lower() for line in commits), f"commits={commits[:3]}"))
        checks.append(check("v75_closeout_commit_present", any("V75" in line for line in commits), f"searched_commits={len(commits)}"))
        targets = [f"docs/trinity-live-traces/{V65_PREFIX}-git-publication-result-v1.json"]
    elif system_id == "v74_11_gmut_qcit_crosswalk_board":
        paths = ["docs/gmut-observable-map-v2.json", "docs/qcit-coordination-report.json", "docs/quantum-energy-transmutation-report.json"]
        checks.extend(check(f"path_exists:{path}", repo(path).exists(), path) for path in paths)
        targets = paths
    elif system_id == "v74_12_freedid_cbr_live_boundary_check":
        blocked = json.dumps(live.get("blocked_without_fresh_operator_confirmation", []) if isinstance(live, dict) else [])
        checks.append(check("personal_surfaces_blocked", all(token in blocked for token in ("personal_email", "google_drive", "account_setting", "raw_secret")), blocked))
        checks.append(check("freedid_artifacts_present", repo("docs/freed-id-live-path-audit-log.jsonl").exists(), "freed-id audit log present"))
        targets = ["docs/freed-id-live-path-audit-log.jsonl", f"docs/trinity-live-traces/{V65_PREFIX}-live-write-governor-v1.json"]
    elif system_id == "v74_13_memory_floor_runtime_pause_gate":
        health = read_json(f"docs/trinity-live-traces/{V65_PREFIX}-runtime-health-gate-v1.json", {})
        checks.append(check("memory_floor_policy_300000", health.get("free_memory_cool_floor_kb") == FREE_MEMORY_FLOOR_KB, f"floor={health.get('free_memory_cool_floor_kb')}"))
        checks.append(check("load_gate_field_present", "load_gate" in health, f"load_gate={health.get('load_gate')}"))
        targets = [f"docs/trinity-live-traces/{V65_PREFIX}-runtime-health-gate-v1.json"]
    elif system_id == "v74_14_d_drive_artifact_retention_meter":
        d_mb = free_space_mb("D:\\")
        c_mb = free_space_mb("C:\\")
        checks.append(check("d_drive_present", d_mb > 0, f"d_free_mb={d_mb}"))
        checks.append(check("artifact_worktree_on_d_drive", str(ROOT).lower().startswith("d:"), str(ROOT)))
        metrics.update({"c_free_mb": c_mb, "d_free_mb": d_mb})
        targets = ["docs/trinity-storage-posture-summary-v12.json"]
    elif system_id == "v74_15_publication_receipt_consistency_check":
        pub = read_json(f"docs/trinity-live-traces/{V65_PREFIX}-git-publication-result-v1.json", {})
        checks.append(check("publication_receipt_present", bool(pub), "publication result loaded"))
        checks.append(check("receipt_recorded_remote_match_at_generation", bool(pub.get("remote_matches_local")), f"remote_matches_local={pub.get('remote_matches_local')}"))
        targets = [f"docs/trinity-live-traces/{V65_PREFIX}-git-publication-result-v1.json"]
    elif system_id == "v74_16_secret_free_external_prompt_guard":
        allow = read_json(f"docs/trinity-live-traces/{V65_PREFIX}-stage-allowlist-v1.json", {})
        allow_paths = json.dumps(allow)
        blocked_terms = ["API Key bank", "Cleaned up", ".env", "secret", "token bank"]
        checks.append(check("allowlist_excludes_secret_banks", not any(term.lower() in allow_paths.lower() for term in blocked_terms), "secret-bank-like paths excluded from curated allowlist"))
        checks.append(check("live_governor_blocks_secret_transmission", "raw_secret_transmission_to_external_models" in json.dumps(live), "raw secret external transmission blocked"))
        targets = [f"docs/trinity-live-traces/{V65_PREFIX}-stage-allowlist-v1.json", f"docs/trinity-live-traces/{V65_PREFIX}-live-write-governor-v1.json"]
    elif system_id == "v74_17_phase_report_quality_linter":
        required = ["State:", "Page 8 - Recommendations", "Page 9 - Introductions", "boundary", "next"]
        checks.append(check("v75_report_required_sections", all(item.lower() in closeout.lower() for item in required), f"required={required}"))
        checks.append(check("closeout_report_length", len(closeout.splitlines()) >= 120, f"lines={len(closeout.splitlines())}"))
        targets = [f"docs/trinity-live-traces/{V65_PREFIX}-cli-reports/v75-grand-closeout-council-report-v1.md"]
    elif system_id == "v74_18_live_phase_budget_ceiling_meter":
        budget = live.get("budget_policy", {}) if isinstance(live, dict) else {}
        checks.append(check("budget_ceiling_recorded", float(budget.get("ceiling_fraction_per_provider", 1.0)) <= 0.30, f"budget={budget}"))
        checks.append(check("spend_target_not_requirement", bool(budget.get("spend_target_is_ceiling_not_requirement")), f"budget={budget}"))
        targets = [f"docs/trinity-live-traces/{V65_PREFIX}-live-write-governor-v1.json"]
    elif system_id == "v74_19_operator_hold_surface_audit":
        blocked = json.dumps(live.get("blocked_without_fresh_operator_confirmation", []) if isinstance(live, dict) else [])
        checks.append(check("held_personal_surfaces_blocked", all(token in blocked for token in ("google_drive", "personal_email", "calendar", "account_setting")), blocked))
        checks.append(check("google_drive_operator_hold_preserved", "google_drive_content_mutation" in blocked, blocked))
        targets = [f"docs/trinity-live-traces/{V65_PREFIX}-live-write-governor-v1.json"]
    elif system_id == "v74_20_v75_closeout_synthesis_builder":
        closeout_json = read_json("docs/v75-omega-closeout-summary-v1.json", {})
        handoff_json = read_json("docs/v75-omega-handoff-policy-v1.json", {})
        checks.append(check("closeout_json_present", bool(closeout_json), "docs/v75-omega-closeout-summary-v1.json"))
        checks.append(check("handoff_json_present", bool(handoff_json), "docs/v75-omega-handoff-policy-v1.json"))
        checks.append(check("grand_report_present", "V75 Grand Closeout Council Report" in closeout, "grand report loaded"))
        targets = ["docs/v75-omega-closeout-summary-v1.json", "docs/v75-omega-handoff-policy-v1.json", f"docs/trinity-live-traces/{V65_PREFIX}-cli-reports/v75-grand-closeout-council-report-v1.md"]
    else:
        checks.append(check("known_candidate", False, f"unknown system_id={system_id}"))

    pack_candidates = candidate_pack.get("candidates", []) if isinstance(candidate_pack, dict) else []
    checks.append(check("v74_candidate_pack_loaded", len(pack_candidates) >= 20, f"candidates={len(pack_candidates)}"))
    checks.append(check("prior_v75_l5_green", bool(metrics.get("prior_v75_l5_effective_success")), "v75 L5 anchor remains green"))
    return checks, metrics, targets


def run_system(system_id: str) -> int:
    if system_id not in CANDIDATES:
        print(f"unknown system id: {system_id}", flush=True)
        return 2
    checks, metrics, targets = checks_for(system_id)
    overall = "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL"
    payload = {
        "generated_utc": now_iso(),
        "phase": "v76_omega",
        "system_id": system_id,
        "pillar": CANDIDATES[system_id]["pillar"],
        "purpose": CANDIDATES[system_id]["purpose"],
        "overall_status": overall,
        "effective_success": overall == "PASS",
        "checks": checks,
        "metrics": metrics,
        "repo_targets_touched": sorted(set(targets)),
        "next_action": "Keep this promoted candidate in Deep/L5 only if the suite remains green.",
    }
    stem = hyphen(system_id)
    json_path = RESULT_DIR / f"{stem}.json"
    md_path = RESULT_DIR / f"{stem}.md"
    write_json(json_path, payload)
    lines = [
        f"# V76 Candidate System Result: {system_id}",
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
    write_text(md_path, "\n".join(lines).rstrip() + "\n")
    print(f"overall_status={overall}")
    print(f"latest_json={json_path.relative_to(ROOT)}")
    return 0 if overall == "PASS" else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a promoted v76 candidate system.")
    parser.add_argument("--system-id", required=True, choices=sorted(CANDIDATES))
    args = parser.parse_args()
    return run_system(args.system_id)


if __name__ == "__main__":
    raise SystemExit(main())
