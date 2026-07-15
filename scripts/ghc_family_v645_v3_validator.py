#!/usr/bin/env python3
"""Validate Eiren Kestrel v645-v3 without promoting bounded evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


PHASE = "v645-gmut-thos-v3-x1-x2"
PHASE_REL = Path("docs/eiren-kestrel/v645-v3")
SOURCE = "c8ef5b28537eb1e85f79e3ead3977a031504f0dc"
SOURCE_SEAL = "1dfbf310a9313117c692a060b9c4e3a5ad8e1626"
X1_COMMIT = "abb576e6de2666dd2dc792f6dd189722424ff0c2"
EXPECTED = {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}
TOOLS = [
    "scripts/build_ghc_family_v645_v3_preregistration.py",
    "scripts/ghc_family_v645_v3_definitions.py",
    "scripts/ghc_family_v645_v3_x1_review.py",
    "scripts/build_ghc_family_v645_v3_evidence.py",
    "scripts/ghc_family_anytime_evidence_board.py",
    "scripts/ghc_family_deferred_issuance_state_machine.py",
    "scripts/ghc_family_eft_quotient_validator.py",
    "scripts/ghc_family_git_acceleration_lab.py",
    "scripts/ghc_family_sandbox_blueprint_linter.py",
    "scripts/ghc_family_v645_v3_portfolio_validator.py",
    "scripts/ghc_family_v645_v3_staged_review.py",
    "scripts/ghc_family_v645_v3_manifest.py",
    "scripts/ghc_family_v645_v3_validator.py",
    "tests/test_ghc_family_v645_v3_x1.py",
    "tests/test_ghc_family_v645_v3.py",
]


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def git(repo: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=check,
    )
    return result.stdout.strip()


def ancestor(repo: Path, older: str, newer: str = "HEAD") -> bool:
    return subprocess.run(
        ["git", "-C", str(repo), "merge-base", "--is-ancestor", older, newer],
        capture_output=True,
    ).returncode == 0


def logical_text_hash(path: Path) -> str:
    return hashlib.sha256(path.read_text(encoding="utf-8").encode("utf-8")).hexdigest()


def privacy_scan(repo: Path, files: list[Path]) -> dict[str, Any]:
    delegation = "codex" + "_delegation"
    route = "source" + "_thread_id"
    patterns = {
        "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "delegation_markup": re.compile(rf"<(?:{delegation}|{route})>", re.I),
        "private_local_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
        "private_uri": re.compile(r"\b(?:app|plugin)://", re.I),
        "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']"),
    }
    hits: list[dict[str, str]] = []
    scanned = 0
    for path in files:
        if path.suffix.lower() not in {".json", ".md", ".html", ".txt", ".py", ".ps1", ".in"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        scanned += 1
        for label, pattern in patterns.items():
            if pattern.search(text):
                hits.append({"path": path.relative_to(repo).as_posix(), "pattern_class": label})
    return {
        "files_scanned": scanned,
        "pattern_classes": sorted(patterns),
        "hit_count": len(hits),
        "hits": hits,
        "valid": not hits and scanned > 0,
        "boundary": "Five-class scanning is bounded pattern evidence, not exhaustive privacy or security assurance.",
    }


def validate(repo: Path, *, mode: str, expected_head: str | None, require_clean: bool) -> dict[str, Any]:
    repo = repo.resolve()
    phase = repo / PHASE_REL
    proposals = load(phase / "x1-proposals.json")
    ledger = load(phase / "x2-proposal-ledger.json")
    approvals = load(phase / "approval-packets/x2-execution-ledger.json")
    skills = load(phase / "prototypes/skill-runner-execution-ledger.json")
    clean = load(phase / "maintenance/x2-clean-refine-ledger.json")
    negatives = load(phase / "retained-negative-register.json")
    gates = load(phase / "exact-open-gate-register.json")
    truth = load(phase / "phase-truth.json")
    method = load(phase / "method-flow/method-flow-state.json")
    method_receipt = load(phase / "method-flow/runner-validation.json")
    sandbox = load(phase / "sandbox/sandbox-blueprint-validation.json")
    host = load(phase / "environment/host-sandbox-version-probe.json")
    sources = load(phase / "sources/source-ledger.json")
    manifest = load(phase / "reproduction/evidence-manifest.json")
    checklist = load(phase / "complete-incomplete-checklist.json")
    board = load(phase / "stage20/terminal-evidence-board.json")

    owner_files = sorted(path for path in phase.rglob("*") if path.is_file())
    owner_files.extend(repo / rel for rel in TOOLS if (repo / rel).is_file())
    owner_files = sorted(set(owner_files))
    json_files = [path for path in owner_files if path.suffix.lower() == ".json"]
    json_issues: list[str] = []
    for path in json_files:
        try:
            load(path)
        except Exception as exc:  # pragma: no cover - diagnostic receipt
            json_issues.append(f"{path.relative_to(repo).as_posix()}:{type(exc).__name__}")
    privacy = privacy_scan(repo, owner_files)

    manifest_issues: list[str] = []
    for row in manifest["entries"]:
        path = repo / row["path"]
        if not path.is_file() or logical_text_hash(path) != row["logical_text_sha256"]:
            manifest_issues.append(row["path"])

    disposition = Counter(row["disposition"] for row in ledger["outcomes"])
    source_states = Counter(row["status"] for row in sources["sources"])
    method_states = Counter(row["recommendation_state"] for row in method["methods"])
    witness_states = Counter(row["result"] for row in method["witnesses"])
    report = (phase / "deliverables/v645-v3-static-report.html").read_text(encoding="utf-8")
    overview = (phase / "deliverables/v645-v3-final-integrated-overview.md").read_text(encoding="utf-8")
    head = git(repo, "rev-parse", "HEAD")
    branch = git(repo, "branch", "--show-current")
    status = git(repo, "status", "--porcelain=v1", "--untracked-files=all") if require_clean else ""
    merge_count = int(git(repo, "rev-list", "--merges", f"{SOURCE}..HEAD", "--count"))

    checks: dict[str, bool] = {
        "phase_identity": proposals["phase"] == ledger["phase"] == PHASE,
        "proposals_exactly_10": proposals["proposal_count"] == 10 == len(proposals["proposals"]),
        "novelty_audited_against_330": proposals["prior_frozen_proposal_count"] == 330,
        "outcomes_exactly_10": ledger["proposal_count"] == 10 == len(ledger["outcomes"]),
        "distribution_6_2_1_1": dict(disposition) == EXPECTED == ledger["disposition_counts"],
        "outcome_vocabulary": set(disposition) <= set(EXPECTED),
        "safe_now_15_completed": len(approvals["eiren_safe_now"]) == 15 and approvals["counts"]["safe_completed"] == 15 and all(row["state"] == "completed_bounded" for row in approvals["eiren_safe_now"]),
        "candidate_10_completed": len(approvals["eiren_candidate_prototypes"]) == 10 and approvals["counts"]["candidate_prototypes_completed"] == 10 and all(row["state"] == "bounded_prototype_completed" for row in approvals["eiren_candidate_prototypes"]),
        "successor_packet_seeds_25": len(approvals["successor_safe_now_seeds"]) == 15 and len(approvals["successor_candidate_seeds"]) == 10 and approvals["counts"]["successor_seed_only"] == 25,
        "exact_10_unexecuted": len(approvals["exact_packets"]) == 10 and approvals["counts"]["exact_unexecuted"] == 10 and all(row["state"] == "unexecuted_exact_gate" for row in approvals["exact_packets"]),
        "blocked_5_unexecuted": len(approvals["blocked_packets"]) == 5 and approvals["counts"]["blocked_unexecuted"] == 5 and all(row["state"] == "unexecuted_blocked" for row in approvals["blocked_packets"]),
        "skills_10_built_used": len(skills["skills"]) == 10 and all(row["built"] and row["validated"] and row["used_in_phase"] for row in skills["skills"]),
        "runners_5_built_used": len(skills["runners"]) == 5 and all(row["built"] and row["bounded_fixture_passed"] and row["used_in_phase"] for row in skills["runners"]),
        "successor_skill_runner_seeds": len(skills["successor_skill_ideas"]) == 10 and len(skills["successor_runner_ideas"]) == 5,
        "clean_tasks_exactly_15": len(clean["eiren_tasks"]) == 15,
        "successor_clean_seeds_15": len(clean["successor_seeds"]) == 15,
        "sandbox_blueprints_6_valid": sandbox["template_count"] == sandbox["valid_count"] == 6 and sandbox["valid"],
        "sandbox_runtime_truthful": host["windows_sandbox_executable_available"] is False and host["windows_sandbox_cli_available"] is False and truth["sandbox_runtime_available"] is False and truth["sandbox_launched"] is False,
        "negatives_exact_1998": negatives["negative_count"] == 1998 == negatives["inherited_effective_count"] + negatives["x1_operational_count"] + negatives["x2_operational_count"] + negatives["new_synthetic_count"],
        "negative_components": negatives["inherited_effective_count"] == 1916 and negatives["x1_operational_count"] == 6 and negatives["x2_operational_count"] == 6 and negatives["new_synthetic_count"] == 70,
        "negative_retention": negatives["all_retained"] and not negatives["erasure_permitted"],
        "open_gaps_5": gates["open_gap_count"] == 5 == len(gates["open_gaps"]),
        "exact_gates_6": gates["exact_gate_count"] == 6 == len(gates["exact_gates"]),
        "gates_visible": gates["all_visible"] and gates["none_silently_closed"],
        "method_flow_12_balanced": len(method["methods"]) == 12 and len(method["witnesses"]) == 24 and witness_states == {"fail": 12, "pass": 12},
        "method_flow_preferred": method_states == {"preferred": 12},
        "method_flow_runner_valid": method_receipt["valid"] and method_receipt["issue_count"] == 0,
        "source_vocabulary": set(source_states) <= {"current", "stable", "draft", "watch"} and sum(source_states.values()) == sources["source_count"] == 19,
        "real_counts_zero": truth["real_gmut_rows"] == truth["real_thos_participants"] == truth["real_freed_id_credentials"] == 0,
        "terminal_not_ready": truth["terminal_verdict"] == board["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "report_structure": '<html lang="en">' in report and 'href="#main"' in report and '<main id="main"' in report and ":focus-visible" in report and "NOT_READY_FOR_STAGE_20" in report,
        "report_no_auto_refresh": "http-equiv=\"refresh\"" not in report.lower(),
        "overview_1500_to_6000_words": 1500 <= len(overview.split()) <= 6000,
        "checklist_both_sides": bool(checklist["completed"]) and bool(checklist["incomplete_external"]),
        "manifest_count": manifest["entry_count"] == len(manifest["entries"]) > 0,
        "manifest_logical_parity": not manifest_issues,
        "json_parse_zero_issues": not json_issues,
        "privacy_five_class_zero_hits": privacy["valid"] and len(privacy["pattern_classes"]) == 5,
        "owner_files_under_15000": len(owner_files) < 15000,
        "source_ancestral": ancestor(repo, SOURCE),
        "source_seal_ancestral": ancestor(repo, SOURCE_SEAL),
        "x1_ancestral": ancestor(repo, X1_COMMIT),
        "zero_merges": merge_count == 0,
        "named_eiren_branch": branch.startswith("codex/GHC-Family/eiren-kestrel-"),
        "expected_head": expected_head is None or head == expected_head,
        "clean_when_required": not require_clean or not status,
    }
    minimal_names = [
        "proposals_exactly_10", "distribution_6_2_1_1", "safe_now_15_completed",
        "candidate_10_completed", "skills_10_built_used", "runners_5_built_used",
        "negatives_exact_1998", "negative_retention", "open_gaps_5", "exact_gates_6",
        "method_flow_runner_valid", "terminal_not_ready", "manifest_logical_parity",
        "json_parse_zero_issues", "privacy_five_class_zero_hits", "source_ancestral",
        "source_seal_ancestral", "x1_ancestral", "zero_merges", "expected_head",
        "clean_when_required",
    ]
    selected = {name: checks[name] for name in minimal_names} if mode == "minimal" else checks
    issues = [name for name, passed in selected.items() if not passed]
    return {
        "schema": f"ghc.family.v645-v3.{mode}-validation.v1",
        "phase": PHASE,
        "mode": mode,
        "valid": not issues,
        "checks_passed": sum(selected.values()),
        "checks_total": len(selected),
        "checks": selected,
        "issues": issues,
        "head": head,
        "expected_head": expected_head,
        "branch": branch,
        "owner_file_count": len(owner_files),
        "json_files_parsed": len(json_files),
        "json_issues": json_issues,
        "privacy": privacy,
        "manifest_entries": manifest["entry_count"],
        "manifest_issues": manifest_issues,
        "overview_word_count": len(overview.split()),
        "same_owner_repeatability_only": True,
        "independent_team_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": "Repository validation cannot establish empirical truth, participant benefit, production identity assurance, legal or cultural authority, exhaustive security, complete accessibility, or independent reproduction.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--mode", choices=["detailed", "minimal"], default="detailed")
    parser.add_argument("--expected-head")
    parser.add_argument("--require-clean", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--privacy-output", type=Path)
    args = parser.parse_args()
    result = validate(args.repo, mode=args.mode, expected_head=args.expected_head, require_clean=args.require_clean)
    repo = args.repo.resolve()
    if args.output:
        write_json(args.output if args.output.is_absolute() else repo / args.output, result)
    if args.privacy_output:
        write_json(args.privacy_output if args.privacy_output.is_absolute() else repo / args.privacy_output, result["privacy"])
    print(json.dumps({key: result[key] for key in ("valid", "mode", "checks_passed", "checks_total", "issues", "json_files_parsed", "owner_file_count")}, ensure_ascii=False))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
