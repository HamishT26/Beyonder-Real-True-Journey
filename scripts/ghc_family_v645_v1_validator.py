#!/usr/bin/env python3
"""Validate Tamar Vey v645-v1 under the non-Eiren scoped rule."""

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


PHASE = "v645-gmut-thos-v1-x1-x2"
PHASE_REL = Path("docs/tamar-vey/v645-v1")
X1_COMMIT = "1fa214f0d8ca832ae41045234489bd3e1637f287"
SOURCE_REVISION = "a6c869a44eb7d3fe32ba80bc64964aa7903531c2"
EXPECTED_DISTRIBUTION = {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}
ALLOWED_OUTCOMES = set(EXPECTED_DISTRIBUTION)
OWNER_TOOLS = [
    "scripts/build_ghc_family_v645_v1_preregistration.py",
    "scripts/ghc_family_v645_v1_x1_definitions.py",
    "scripts/ghc_family_git_lfs_boundary.py",
    "scripts/ghc_family_method_flow_state.py",
    "scripts/ghc_family_v645_v1_model.py",
    "scripts/ghc_family_v645_v1_x1_staged_review.py",
    "scripts/ghc_family_v645_v1_staged_review.py",
    "scripts/ghc_family_v645_v1_evidence.py",
    "scripts/ghc_family_v645_v1_final_manifest.py",
    "scripts/ghc_family_v645_v1_validator.py",
    "tests/test_ghc_family_v645_v1_x1.py",
    "tests/test_ghc_family_v645_v1.py",
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


def batch_commit_blobs(repo: Path, specs: list[str]) -> dict[str, bytes]:
    specs = list(dict.fromkeys(specs))
    if not specs:
        return {}
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
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def is_ancestor(repo: Path, ancestor: str, descendant: str = "HEAD") -> bool:
    return subprocess.run(
        ["git", "-C", str(repo), "merge-base", "--is-ancestor", ancestor, descendant],
        capture_output=True,
    ).returncode == 0


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
        "boundary": "Five-class public-artifact scanning is bounded and is not exhaustive privacy or security assurance.",
    }


def committed_manifest_result(repo: Path, path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"present": False, "target": None, "entry_count": 0, "mismatches": [], "ancestral": False}
    manifest = load(path)
    target = manifest["target"]
    specs = [f"{target}:{row['path']}" for row in manifest["entries"]]
    blobs = batch_commit_blobs(repo, specs)
    mismatches = []
    for row, spec in zip(manifest["entries"], specs, strict=True):
        data = blobs[spec]
        if hashlib.sha256(data).hexdigest() != row["sha256"] or len(data) != row["bytes"]:
            mismatches.append(row["path"])
    return {
        "present": True,
        "target": target,
        "entry_count": manifest["entry_count"],
        "mismatches": mismatches,
        "ancestral": is_ancestor(repo, target),
    }


def staged_manifest_result(repo: Path, path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"present": False, "entry_count": 0, "excluded_count": 0, "mismatches": []}
    manifest = load(path)
    specs = [f":{row['path']}" for row in manifest["entries"]]
    blobs = batch_commit_blobs(repo, specs)
    mismatches = []
    for row, spec in zip(manifest["entries"], specs, strict=True):
        data = blobs[spec]
        if hashlib.sha256(data).hexdigest() != row["sha256"] or len(data) != row["bytes"]:
            mismatches.append(row["path"])
    return {
        "present": True,
        "entry_count": manifest["entry_count"],
        "excluded_count": len(manifest["excluded_self_referential_receipts"]),
        "mismatches": mismatches,
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
    access = load(phase / "validation/generated-content-accessibility-audit.json")
    manual_access = load(phase / "validation/manual-accessibility-reservation.json")
    report = (phase / "deliverables/v645-v1-static-report.html").read_text(encoding="utf-8")
    overview = (phase / "deliverables/v645-v1-final-integrated-overview.md").read_text(encoding="utf-8")

    owner_files = sorted(item for item in phase.rglob("*") if item.is_file())
    owner_files.extend(repo / rel for rel in OWNER_TOOLS if (repo / rel).is_file())
    owner_files = sorted(set(owner_files))
    json_files = [item for item in owner_files if item.suffix.lower() == ".json"]
    json_issues: list[str] = []
    for path in json_files:
        try:
            load(path)
        except Exception as exc:  # pragma: no cover - diagnostic receipt
            json_issues.append(f"{path.relative_to(repo).as_posix()}: {type(exc).__name__}")
    privacy = privacy_scan(repo, owner_files)

    committed_evidence = committed_manifest_result(repo, phase / "reproduction/committed-evidence-manifest.json")
    committed_closeout = committed_manifest_result(repo, phase / "reproduction/committed-closeout-manifest.json")
    final_staged = staged_manifest_result(repo, phase / "reproduction/final-staged-manifest.json")
    manifest_mismatches: list[str] = []
    if stage == "evidence" or not committed_evidence["present"]:
        for row in manifest["entries"]:
            path = phase / row["path"]
            observed = logical_sha256(path) if path.is_file() else "missing"
            if observed != row["logical_lf_sha256"]:
                manifest_mismatches.append(row["path"])
    else:
        target = committed_evidence["target"]
        specs = [f"{target}:{PHASE_REL.as_posix()}/{row['path']}" for row in manifest["entries"]]
        blobs = batch_commit_blobs(repo, specs)
        for row, spec in zip(manifest["entries"], specs, strict=True):
            observed = hashlib.sha256(
                blobs[spec].replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            ).hexdigest()
            if observed != row["logical_lf_sha256"]:
                manifest_mismatches.append(row["path"])

    disposition = Counter(row["observed_disposition"] for row in ledger["rows"])
    method_states = Counter(row["recommendation_state"] for row in method["methods"])
    method_ids = {row["method_id"] for row in method["methods"]}
    negative_ids = {row["negative_id"] for row in negatives["negatives"]}
    current_head = git(repo, "rev-parse", "HEAD")
    branch = git(repo, "branch", "--show-current")
    status = git(repo, "status", "--porcelain=v1", "--untracked-files=all") if require_clean else ""
    merge_count = int(git(repo, "rev-list", "--merges", f"{SOURCE_REVISION}..HEAD", "--count"))

    checks: dict[str, bool] = {
        "phase_schema": proposals["phase"] == PHASE == ledger["phase"],
        "proposal_count_10": proposals["proposal_count"] == 10 == ledger["proposal_count"] == len(ledger["rows"]),
        "prior_frozen_proposals_310": proposals["prior_frozen_proposal_count"] == 310,
        "allowed_outcomes_only": set(disposition) <= ALLOWED_OUTCOMES,
        "distribution_6_2_1_1": dict(disposition) == EXPECTED_DISTRIBUTION,
        "mutation_cases_70": ledger["total_case_count"] == 70,
        "mutation_matches_70": ledger["total_matched_count"] == 70,
        "deliverables_present": all((phase / rel).is_file() for row in ledger["rows"] for rel in row["deliverables"]),
        "inherited_effective_negatives_1750": negatives["inherited_effective_count"] == 1750,
        "retained_negatives_exact": negatives["negative_count"] == len(negatives["negatives"]),
        "negative_components_exact": negatives["negative_count"] == (
            negatives["inherited_effective_count"]
            + negatives["x1_operational_count"]
            + negatives["x2_operational_count"]
            + negatives["new_synthetic_count"]
        ),
        "x1_operational_negatives_6": negatives["x1_operational_count"] == 6,
        "x2_operational_negatives_retained": negatives["x2_operational_count"] >= 4,
        "synthetic_negatives_70": negatives["new_synthetic_count"] == 70,
        "negative_ids_unique": not negatives["duplicate_negative_ids"],
        "all_negatives_retained": negatives["all_retained"] and not negatives["erasure_permitted"],
        "new_operational_negatives_present": {"REPRO-V6451-X2-N01", "REPRO-V6451-X2-N02", "REPRO-V6451-X2-N03", "REPRO-V6451-X2-N04"} <= negative_ids,
        "open_gaps_5": gates["open_gap_count"] == 5 == len(gates["open_gaps"]),
        "exact_gates_6": gates["exact_gate_count"] == 6 == len(gates["exact_gates"]),
        "gates_visible": gates["all_visible"] and gates["none_silently_closed"],
        "protected_claims_false": all(value is False for value in evidence["protected_claims"].values()),
        "real_external_counts_zero": all(value == 0 for value in evidence["real_or_external_counts"].values()),
        "terminal_not_ready": evidence["terminal_verdict"] == truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "route_prepared_not_sent": truth["route_state"] == "ACTIVE_SOLO; PREPARED_NOT_SENT" and truth["outbound_message_count"] == 0,
        "successor_task_count_zero": truth["successor_task_count"] == 0,
        "heart_primary_focus": truth["primary_focus"] == "Freed ID/CBR Heart",
        "bounded_fund_governance_practice": truth["bounded_practice"] == "public-interest fund administration and fiduciary governance",
        "source_count_225": sources["effective_source_count"] == 225,
        "source_status_vocabulary": set(sources["effective_status_counts"]) <= {"current", "stable", "draft", "watch"},
        "source_collisions_zero": not sources["duplicate_added_titles"] and not sources["duplicate_added_urls"],
        "method_schema": method["schema"] == "ghc.family.method-flow-state.v1",
        "method_count_10_or_more": len(method["methods"]) >= 10,
        "method_m10_retained": "v6451-m10" in method_ids,
        "method_all_current_preferred": all(row["recommendation_state"] == "preferred" for row in method["methods"]),
        "method_no_candidate": method_states["candidate"] == 0,
        "method_validation_clean": method_validation["valid"] and method_validation["issue_count"] == 0,
        "report_skip_link": 'href="#main"' in report,
        "report_unique_main": report.count('<main id="main"') == 1,
        "report_focus_visible": ":focus-visible" in report,
        "report_figure_accessible": 'role="img"' in report and "distribution-title" in report and "distribution-desc" in report,
        "report_underlying_data": "Underlying disposition data" in report,
        "report_no_pseudo_content_semantics": "::before" not in report and "::after" not in report,
        "report_terminal_boundary": "NOT_READY_FOR_STAGE_20" in report,
        "accessibility_structure_bounded": access["structural_checks_pass"] and not access["complete_accessibility"],
        "manual_accessibility_reserved": bool(manual_access["reserved"]) and not manual_access["completed"] and not manual_access["complete_accessibility"],
        "overview_three_page_equivalent": len(overview.split()) >= 1200,
        "checklist_has_complete_and_incomplete": bool(checklist["complete"]) and bool(checklist["incomplete"]),
        "manifest_entries_present": manifest["entry_count"] == len(manifest["entries"]) > 0,
        "manifest_lf_parity": not manifest_mismatches,
        "manifest_same_owner_only": manifest["same_owner_repeatability_only"] and not manifest["independent_team_reproduction"],
        "committed_evidence_present_when_required": stage == "evidence" or committed_evidence["present"],
        "committed_evidence_parity_when_required": stage == "evidence" or (not committed_evidence["mismatches"] and committed_evidence["ancestral"]),
        "committed_closeout_present_when_required": stage in {"evidence", "closeout"} or committed_closeout["present"],
        "committed_closeout_parity_when_required": stage in {"evidence", "closeout"} or (not committed_closeout["mismatches"] and committed_closeout["ancestral"]),
        "final_staged_manifest_present_when_required": stage != "final" or final_staged["present"],
        "final_staged_manifest_parity_when_required": stage != "final" or (not final_staged["mismatches"] and final_staged["entry_count"] > 0),
        "json_parse_zero_issues": not json_issues,
        "privacy_five_classes_zero_hits": privacy["valid"] and len(privacy["pattern_classes"]) == 5,
        "owner_files_under_15000": len(owner_files) < 15000,
        "source_revision_ancestral": is_ancestor(repo, SOURCE_REVISION),
        "x1_commit_ancestral": is_ancestor(repo, X1_COMMIT),
        "zero_merges_since_source": merge_count == 0,
        "named_branch_not_detached": bool(branch),
        "tamar_owned_branch": branch.startswith("codex/GHC-Family/tamar-vey-"),
        "head_matches_expected": expected_head is None or current_head == expected_head,
        "clean_when_required": not require_clean or not status,
        "full_repository_suite_not_run": truth["full_repository_suite_run"] is False,
    }

    lifecycle_requirements = {
        "evidence": [],
        "closeout": ["closeout-receipt.json", "reproduction/committed-evidence-manifest.json"],
        "seal": ["closeout-receipt.json", "seal-receipt.json", "reproduction/committed-closeout-manifest.json"],
        "final": ["closeout-receipt.json", "seal-receipt.json", "final-validation-record.json", "reproduction/final-staged-manifest.json"],
    }
    for rel in lifecycle_requirements[stage]:
        checks[f"lifecycle_{rel.replace('/', '_')}"] = (phase / rel).is_file()

    minimal_names = [
        "proposal_count_10",
        "allowed_outcomes_only",
        "distribution_6_2_1_1",
        "mutation_matches_70",
        "negative_ids_unique",
        "all_negatives_retained",
        "open_gaps_5",
        "exact_gates_6",
        "protected_claims_false",
        "terminal_not_ready",
        "route_prepared_not_sent",
        "method_validation_clean",
        "manifest_lf_parity",
        "json_parse_zero_issues",
        "privacy_five_classes_zero_hits",
        "x1_commit_ancestral",
        "zero_merges_since_source",
        "named_branch_not_detached",
        "head_matches_expected",
        "clean_when_required",
    ]
    selected = {name: checks[name] for name in minimal_names} if mode == "minimal" else checks
    issues = [name for name, passed in selected.items() if not passed]
    return {
        "schema": f"ghc.family.v645-v1.{mode}-validation.v1",
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
        "committed_evidence": committed_evidence,
        "committed_closeout": committed_closeout,
        "final_staged_manifest": final_staged,
        "method_states": dict(method_states),
        "same_owner_repeatability_only": True,
        "independent_reproduction": False,
        "full_repository_suite_run": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": "Validation is scoped to recent round-robin and v645-v1 evidence; it is not exhaustive assurance or independent reproduction.",
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
    print(json.dumps({key: result[key] for key in (
        "phase", "stage", "mode", "valid", "checks_passed", "checks_total", "issues",
        "json_files_parsed", "owner_file_count",
    )}, ensure_ascii=False))
    if not result["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
