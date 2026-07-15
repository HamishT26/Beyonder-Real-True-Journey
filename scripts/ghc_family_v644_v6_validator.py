#!/usr/bin/env python3
"""Validate the Ilyra Fen v644-v6 packet under the non-Eiren scoped rule."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


PHASE = "v644-gmut-thos-v6-x1-x2"
PHASE_REL = Path("docs/ilyra-fen/v644-v6")
X1_COMMIT = "b8c667052b3fc9bb2f2aafe10b9b1410e9cd77ab"
EVIDENCE_COMMIT = "198540dd2e581365457c5c9db13c0e3b399dae8b"
EXPECTED_DISTRIBUTION = {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}
ALLOWED_OUTCOMES = set(EXPECTED_DISTRIBUTION)
OWNER_TOOLS = [
    "scripts/build_ghc_family_v644_v6_preregistration.py",
    "scripts/ghc_family_v644_v6_x1_definitions.py",
    "scripts/ghc_family_obligation_tribunals.py",
    "scripts/ghc_family_v644_v6_model.py",
    "scripts/ghc_family_v644_v6_evidence.py",
    "scripts/ghc_family_v644_v6_validator.py",
    "tests/test_ghc_family_v644_v6_x1.py",
    "tests/test_ghc_family_v644_v6.py",
]


def git(repo: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=check,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip()


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def logical_sha256(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def commit_blob(repo: Path, commit: str, relative: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(repo), "show", f"{commit}:{relative}"],
        check=True,
        capture_output=True,
    ).stdout


def batch_commit_blobs(repo: Path, specs: list[str]) -> dict[str, bytes]:
    specs = list(dict.fromkeys(specs))
    completed = subprocess.run(
        ["git", "-C", str(repo), "cat-file", "--batch"],
        input="".join(f"{spec}\n" for spec in specs).encode("utf-8"),
        check=True,
        capture_output=True,
    )
    stream = io.BytesIO(completed.stdout)
    result: dict[str, bytes] = {}
    for spec in specs:
        header = stream.readline().decode("utf-8").strip().split()
        if len(header) != 3 or header[1] != "blob":
            raise ValueError(f"missing Git blob for {spec}")
        size = int(header[2])
        result[spec] = stream.read(size)
        stream.read(1)
    return result


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def privacy_scan(repo: Path, files: list[Path]) -> dict[str, Any]:
    delegation_name = "codex" + "_delegation"
    source_name = "source" + "_thread_id"
    patterns = {
        "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "delegation_markup": re.compile(rf"<(?:{delegation_name}|{source_name})>", re.I),
        "private_local_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
        "private_uri": re.compile(r"\b(?:app|plugin)://", re.I),
        "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']"),
    }
    hits: list[dict[str, str]] = []
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(repo).as_posix()
        for label, pattern in patterns.items():
            if pattern.search(text):
                hits.append({"path": rel, "pattern_class": label})
    return {
        "files_scanned": len(files),
        "pattern_classes": sorted(patterns),
        "hits": hits,
        "hit_count": len(hits),
        "valid": not hits,
        "boundary": "Bounded public-artifact pattern scanning is not exhaustive privacy or security assurance.",
    }


def validate(
    repo: Path,
    *,
    mode: str = "detailed",
    stage: str = "evidence",
    expected_head: str | None = None,
    require_clean: bool = False,
) -> dict[str, Any]:
    repo = repo.resolve()
    phase = repo / PHASE_REL
    proposals = load(phase / "x1-proposals.json")
    ledger = load(phase / "x2-proposal-ledger.json")
    negatives = load(phase / "retained-negative-register.json")
    gates = load(phase / "exact-open-gate-register.json")
    evidence = load(phase / "evidence/evidence-ledger.json")
    truth = load(phase / "phase-truth.json")
    sources = load(phase / "sources/source-ledger.json")
    method = load(phase / "method-flow/method-flow-state.json")
    method_validation = load(phase / "method-flow/runner-validation.json")
    manifest = load(phase / "reproduction/evidence-manifest.json")
    checklist = load(phase / "complete-incomplete-checklist.json")
    report = (phase / "deliverables/v644-v6-boundary-evidence-report.html").read_text(encoding="utf-8")
    overview = (phase / "deliverables/v644-v6-final-integrated-overview.md").read_text(encoding="utf-8")

    owner_files = sorted(item for item in phase.rglob("*") if item.is_file())
    owner_files.extend(repo / rel for rel in OWNER_TOOLS if (repo / rel).is_file())
    json_files = [item for item in owner_files if item.suffix.lower() == ".json"]
    json_issues: list[str] = []
    for path in json_files:
        try:
            load(path)
        except Exception as exc:  # pragma: no cover - receipt path
            json_issues.append(f"{path.relative_to(repo).as_posix()}: {type(exc).__name__}")
    privacy = privacy_scan(repo, owner_files)

    logical_specs = [
        f"{EVIDENCE_COMMIT}:{PHASE_REL.as_posix()}/{row['path']}"
        for row in manifest["entries"]
    ] if stage != "evidence" else []
    committed_manifest_path = phase / "reproduction/committed-evidence-manifest.json"
    committed_manifest = load(committed_manifest_path) if committed_manifest_path.is_file() else None
    committed_specs = [
        f"{committed_manifest['target']}:{row['path']}" for row in committed_manifest["entries"]
    ] if committed_manifest else []
    batch = batch_commit_blobs(repo, logical_specs + committed_specs) if logical_specs or committed_specs else {}

    manifest_mismatches = []
    for row in manifest["entries"]:
        path = phase / row["path"]
        if stage == "evidence":
            observed = logical_sha256(path) if path.is_file() else "missing"
        else:
            data = batch[f"{EVIDENCE_COMMIT}:{PHASE_REL.as_posix()}/{row['path']}"]
            observed = hashlib.sha256(data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")).hexdigest()
        if observed != row["logical_lf_sha256"]:
            manifest_mismatches.append(row["path"])

    committed_manifest_mismatches: list[str] = []
    if committed_manifest:
        for row in committed_manifest["entries"]:
            data = batch[f"{committed_manifest['target']}:{row['path']}"]
            if hashlib.sha256(data).hexdigest() != row["sha256"]:
                committed_manifest_mismatches.append(row["path"])

    disposition = Counter(row["observed_disposition"] for row in ledger["rows"])
    method_states = Counter(row["recommendation_state"] for row in method["methods"])
    candidate_method_ids = sorted(
        row["method_id"] for row in method["methods"] if row["recommendation_state"] == "candidate"
    )
    current_head = git(repo, "rev-parse", "HEAD")
    branch = git(repo, "branch", "--show-current")
    status = git(repo, "status", "--porcelain=v1", "--untracked-files=all") if require_clean else ""
    x1_ancestor = subprocess.run(
        ["git", "-C", str(repo), "merge-base", "--is-ancestor", X1_COMMIT, "HEAD"],
        capture_output=True,
    ).returncode == 0

    checks: dict[str, bool] = {
        "phase_schema": proposals["phase"] == PHASE,
        "proposal_count_10": proposals["proposal_count"] == 10 == ledger["proposal_count"],
        "allowed_outcomes_only": set(disposition) <= ALLOWED_OUTCOMES,
        "distribution_6_2_1_1": dict(disposition) == EXPECTED_DISTRIBUTION,
        "mutation_cases_70": ledger["total_case_count"] == 70,
        "mutation_matches_70": ledger["total_matched_count"] == 70,
        "deliverables_present": all((phase / rel).is_file() for row in ledger["rows"] for rel in row["deliverables"]),
        "inherited_effective_negatives_1495": negatives["inherited_effective_count"] == 1495,
        "retained_negatives_1575_or_more": negatives["negative_count"] >= 1575,
        "negative_count_exact": negatives["negative_count"] == len(negatives["negatives"]),
        "negative_ids_unique": not negatives["duplicate_negative_ids"],
        "all_negatives_retained": negatives["all_retained"] and not negatives["erasure_permitted"],
        "post_final_negatives_present": all(f"V6445-VALID-N{i:02d}" in {row["negative_id"] for row in negatives["negatives"]} for i in range(1, 8)),
        "open_gaps_5": gates["open_gap_count"] == 5 == len(gates["open_gaps"]),
        "exact_gates_6": gates["exact_gate_count"] == 6 == len(gates["exact_gates"]),
        "gates_visible": gates["all_visible"] and gates["none_silently_closed"],
        "protected_claims_false": all(value is False for value in evidence["protected_claims"].values()),
        "real_external_counts_zero": all(value == 0 for value in evidence["real_or_external_counts"].values()),
        "terminal_not_ready": evidence["terminal_verdict"] == truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "route_prepared_not_sent": truth["route_state"] == "ACTIVE_SOLO; PREPARED_NOT_SENT" and truth["outbound_message_count"] == 0,
        "successor_task_count_zero": truth["successor_task_count"] == 0,
        "source_count_208": sources["effective_source_count"] == 208,
        "source_status_vocabulary": set(sources["effective_status_counts"]) <= {"current", "stable", "draft", "watch"},
        "source_collisions_zero": not sources["duplicate_added_titles"] and not sources["duplicate_added_urls"],
        "method_schema": method["schema"] == "ghc.family.method-flow-state.v1",
        "method_count_9_or_more": len(method["methods"]) >= 9,
        "method_validation_clean": method_validation["valid"] and method_validation["issue_count"] == 0,
        "method_only_one_candidate_before_final": method_states["candidate"] <= 1,
        "method_final_named_lane_candidate_frozen": stage != "final" or candidate_method_ids == ["V6446-M01"],
        "report_skip_link": 'href="#main"' in report,
        "report_unique_main": report.count('<main id="main"') == 1,
        "report_focus_visible": ":focus-visible" in report,
        "report_figure_role": 'role="img"' in report,
        "report_figure_title_description": "distribution-title" in report and "distribution-desc" in report,
        "report_figcaption": "<figcaption>" in report,
        "report_long_description": 'id="distribution-long"' in report,
        "report_underlying_data": "Underlying disposition data" in report,
        "report_terminal_boundary": "NOT_READY_FOR_STAGE_20" in report,
        "overview_three_page_equivalent": len(overview.split()) >= 1200,
        "checklist_has_complete_and_incomplete": bool(checklist["complete"]) and bool(checklist["incomplete"]),
        "manifest_entries_present": manifest["entry_count"] == len(manifest["entries"]) > 0,
        "manifest_lf_parity": not manifest_mismatches,
        "manifest_same_owner_only": manifest["same_owner_repeatability_only"] and not manifest["independent_team_reproduction"],
        "committed_manifest_present": committed_manifest is not None,
        "committed_manifest_parity": committed_manifest is not None and not committed_manifest_mismatches,
        "json_parse_zero_issues": not json_issues,
        "privacy_zero_hits": privacy["valid"],
        "owner_files_under_15000": len(owner_files) < 15000,
        "x1_commit_ancestral": x1_ancestor,
        "named_branch_not_detached": bool(branch),
        "ilyra_owned_branch": branch.startswith("codex/GHC-Family/ilyra-fen"),
        "head_matches_expected": expected_head is None or current_head == expected_head,
        "clean_when_required": not require_clean or not status,
        "full_repository_suite_not_claimed": "full-repository" not in truth.get("validation_class", ""),
    }

    lifecycle_requirements = {
        "evidence": [],
        "closeout": ["closeout-receipt.json"],
        "seal": ["closeout-receipt.json", "seal-receipt.json"],
        "final": ["closeout-receipt.json", "seal-receipt.json", "final-validation-record.json"],
    }
    for rel in lifecycle_requirements[stage]:
        checks[f"lifecycle_{rel}"] = (phase / rel).is_file()

    minimal_names = [
        "proposal_count_10", "allowed_outcomes_only", "distribution_6_2_1_1",
        "mutation_matches_70", "negative_ids_unique", "all_negatives_retained",
        "open_gaps_5", "exact_gates_6", "protected_claims_false",
        "terminal_not_ready", "route_prepared_not_sent", "method_validation_clean",
        "manifest_lf_parity", "json_parse_zero_issues", "privacy_zero_hits",
        "x1_commit_ancestral", "named_branch_not_detached", "head_matches_expected",
        "clean_when_required", "owner_files_under_15000",
    ]
    selected = {name: checks[name] for name in minimal_names} if mode == "minimal" else checks
    issues = [name for name, passed in selected.items() if not passed]
    return {
        "schema": f"ghc.family.v644-v6.{mode}-validation.v1",
        "phase": PHASE,
        "stage": stage,
        "mode": mode,
        "valid": not issues,
        "checks_passed": sum(selected.values()),
        "checks_total": len(selected),
        "checks": selected,
        "issues": issues,
        "current_head": current_head,
        "expected_head": expected_head,
        "branch": branch,
        "require_clean": require_clean,
        "owner_file_count": len(owner_files),
        "json_files_parsed": len(json_files),
        "json_issues": json_issues,
        "privacy": privacy,
        "manifest_entries": manifest["entry_count"],
        "manifest_mismatches": manifest_mismatches,
        "committed_manifest_entries": committed_manifest["entry_count"] if committed_manifest else 0,
        "committed_manifest_mismatches": committed_manifest_mismatches,
        "method_states": dict(method_states),
        "candidate_method_ids": candidate_method_ids,
        "same_owner_repeatability_only": True,
        "independent_reproduction": False,
        "full_repository_suite_run": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": "Validation is scoped to recent round-robin and v644-v6 evidence; it is not exhaustive assurance or independent reproduction.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--mode", choices=["detailed", "minimal"], default="detailed")
    parser.add_argument("--stage", choices=["evidence", "closeout", "seal", "final"], default="evidence")
    parser.add_argument("--expected-head")
    parser.add_argument("--require-clean", action="store_true")
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    result = validate(
        args.repo,
        mode=args.mode,
        stage=args.stage,
        expected_head=args.expected_head,
        require_clean=args.require_clean,
    )
    if args.receipt:
        write_json(args.repo.resolve() / args.receipt, result)
    print(json.dumps({key: result[key] for key in ("phase", "stage", "mode", "valid", "checks_passed", "checks_total", "issues", "json_files_parsed", "owner_file_count")}, ensure_ascii=False))
    if not result["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
