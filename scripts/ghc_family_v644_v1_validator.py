#!/usr/bin/env python3
"""Detailed standard-library validator for Sable Rook v644-v1."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
from pathlib import Path
from typing import Any


PHASE_REL = "docs/sable-rook/v644-v1"
EXPECTED_DISTRIBUTION = {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}
EXPECTED_SOURCE_STATUS = {"current": 65, "stable": 82, "draft": 8, "watch": 3}
EXPECTED_INHERITED_NEGATIVES = 1063
EXPECTED_X1_NEGATIVES = 4
EXPECTED_SYNTHETIC_NEGATIVES = 70


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def normalized_bytes(path: Path) -> bytes:
    data = path.read_bytes()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return data
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def normalized_sha256(path: Path) -> str:
    return hashlib.sha256(normalized_bytes(path)).hexdigest()


def load_engine(repo: Path):
    path = repo / "scripts/ghc_family_v644_v1_evidence.py"
    spec = importlib.util.spec_from_file_location("ghc_family_v644_v1_evidence_validator", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=repo, text=True, encoding="utf-8").strip()


def validate(repo: Path, phase: Path | None = None, allow_pending_snapshot: bool = False) -> dict[str, Any]:
    repo = repo.resolve()
    phase = (phase or repo / PHASE_REL).resolve()
    engine = load_engine(repo)
    checks: list[dict[str, Any]] = []

    def add(name: str, passed: bool, detail: Any = None) -> None:
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    required_files = [
        "x1-proposals.json", "x2-proposal-ledger.json", "phase-truth.json", "retained-negative-register.json",
        "exact-open-gate-register.json", "threat-model.json", "complete-incomplete-checklist.json",
        "evidence/evidence-ledger.json", "environment/x2-execution-receipt.json",
        "reproduction/x1-content-seal.json", "reproduction/manifest.json", "reproduction/independent-team-gap.json",
        "stage20/domain-veto-evidence-board.json", "tooling/executed-toolchain.json",
        "deliverables/v644-v1-final-integrated-overview.md", "deliverables/v644-v1-boundary-evidence-report.html",
        "accessibility/static-report-receipt.json", "validation/x2-privacy-scan.json",
    ]
    for relative in required_files:
        add(f"required file {relative}", (phase / relative).is_file())

    proposals = load(phase / "x1-proposals.json")
    ledger = load(phase / "x2-proposal-ledger.json")
    truth = load(phase / "phase-truth.json")
    negatives = load(phase / "retained-negative-register.json")
    inherited = load(repo / "docs/ilyra-fen/v643-v8/retained-negative-register.json")
    gates = load(phase / "exact-open-gate-register.json")
    seal = load(phase / "reproduction/x1-content-seal.json")
    manifest = load(phase / "reproduction/manifest.json")
    privacy = load(phase / "validation/x2-privacy-scan.json")
    source_ledger = load(phase / "sources/source-ledger.json")
    board = load(phase / "stage20/domain-veto-evidence-board.json")

    add("phase name", truth.get("phase") == "v644-gmut-thos-v1-x1-x2")
    add("owner", truth.get("owner") == "Sable Rook")
    add("proposal count ten", proposals.get("proposal_count") == 10 == ledger.get("proposal_count"))
    add("prior proposal count 230", proposals.get("prior_frozen_proposal_count") == 230)
    add("truth distribution", truth.get("distribution") == EXPECTED_DISTRIBUTION)
    add("ledger distribution", ledger.get("distribution") == EXPECTED_DISTRIBUTION)
    add("four truth labels only", proposals.get("outcome_classes") == ["completed", "represented", "open_gap", "exact_gate"])
    add("case count 80", ledger.get("case_count") == 80 == truth.get("case_count"))
    add("rejection count 70", ledger.get("rejected_mutation_count") == 70 == truth.get("synthetic_rejection_count"))
    add("primary focus Freed ID/CBR Heart", truth.get("primary_focus") == "Freed ID/CBR Heart")
    add("terminal verdict", truth.get("terminal_verdict") == "NOT_READY_FOR_STAGE_20")
    add("route prepared not sent", truth.get("route_state") == "PREPARED_NOT_SENT" and truth.get("outbound_message_count") == 0)
    add("no successor task created", truth.get("successor_task_count") == 0)
    add("no subagents", truth.get("subagent_count") == 0)
    add("all protected claims false", all(value is False for value in truth.get("protected_claims", {}).values()))
    add("source count 158", source_ledger.get("effective_source_count") == 158)
    add("source status classes preserved", source_ledger.get("effective_status_counts") == EXPECTED_SOURCE_STATUS)
    add("x1 seal commit", seal.get("x1_commit") == engine.X1_COMMIT)
    add("x1 seal 28 entries", seal.get("entry_count") == 28)
    add("x1 seal unchanged", seal.get("all_unchanged") is True)
    for row in seal.get("entries", []):
        add(f"x1 sealed path exists {row.get('repo_path')}", (repo / row.get("repo_path", "")).is_file())
        add(f"x1 sealed hash unchanged {row.get('repo_path')}", row.get("unchanged") is True)

    expected_negative_count = EXPECTED_INHERITED_NEGATIVES + EXPECTED_X1_NEGATIVES + EXPECTED_SYNTHETIC_NEGATIVES + len(engine.X2_OPERATIONAL_NEGATIVES)
    add("negative count exact", negatives.get("negative_count") == expected_negative_count == len(negatives.get("negatives", [])))
    add("negative metadata counts", negatives.get("inherited_count") == EXPECTED_INHERITED_NEGATIVES and negatives.get("x1_operational_count") == EXPECTED_X1_NEGATIVES and negatives.get("new_synthetic_count") == EXPECTED_SYNTHETIC_NEGATIVES)
    add("inherited negatives exact prefix", negatives.get("negatives", [])[:EXPECTED_INHERITED_NEGATIVES] == inherited.get("negatives", []))
    negative_ids = [row.get("negative_id") for row in negatives.get("negatives", [])]
    add("negative IDs unique", len(negative_ids) == len(set(negative_ids)))
    for index, row in enumerate(negatives.get("negatives", [])):
        add(f"negative {index:04d} has ID", bool(row.get("negative_id")))
        add(f"negative {index:04d} retained", row.get("retained") is True)
        add(f"negative {index:04d} external gate open", row.get("external_gate_closed") is not True)

    add("five open gaps", gates.get("open_gap_count") == 5 == len(gates.get("open_gaps", [])))
    add("six exact gates", gates.get("exact_gate_count") == 6 == len(gates.get("exact_gates", [])))
    add("gates visible", gates.get("all_visible") is True and gates.get("none_silently_closed") is True)
    add("Māori gate visible", "Māori" in json.dumps(gates, ensure_ascii=False))
    for row in gates.get("open_gaps", []):
        add(f"open gap remains open {row.get('gate_id')}", row.get("state") == "open")
    for row in gates.get("exact_gates", []):
        add(f"exact gate remains pending {row.get('gate_id')}", row.get("state") == "pending_exact_authority")

    evaluated = engine.evaluate_catalog()
    add("ten fixture groups", len(evaluated) == 10)
    add("eighty fixture rows", sum(len(rows) for rows in evaluated.values()) == 80)
    for pid, rows in evaluated.items():
        add(f"{pid} eight cases", len(rows) == 8)
        for row in rows:
            add(f"fixture matched {row['case_id']}", row.get("matched_expectation") is True)
    add("seventy fixture rejections", sum(not row["accepted"] for rows in evaluated.values() for row in rows) == 70)

    for proposal in proposals.get("proposals", []):
        pid = proposal["proposal_id"]
        ledger_rows = [row for row in ledger.get("proposals", []) if row.get("proposal_id") == pid]
        add(f"{pid} one ledger row", len(ledger_rows) == 1)
        if ledger_rows:
            add(f"{pid} observed outcome", ledger_rows[0].get("outcome") == engine.OBSERVED[pid])
            add(f"{pid} no external claims", ledger_rows[0].get("external_claims_established") == [])
        for relative in proposal.get("deliverables", []):
            add(f"{pid} deliverable {relative}", (phase / relative).is_file())

    add("manifest entry count", manifest.get("entry_count") == len(manifest.get("entries", [])) and manifest.get("entry_count", 0) > 0)
    manifest_paths = [row.get("repo_path") for row in manifest.get("entries", [])]
    add("manifest paths unique", len(manifest_paths) == len(set(manifest_paths)))
    for row in manifest.get("entries", []):
        target = repo / row["repo_path"]
        add(f"manifest path exists {row['repo_path']}", target.is_file())
        add(f"manifest hash {row['repo_path']}", target.is_file() and normalized_sha256(target) == row.get("sha256_lf_normalized"))
    add("same-owner manifest boundary", manifest.get("same_owner_repeatability_only") is True and manifest.get("independent_team_reproduction") is False)
    if allow_pending_snapshot:
        add("pending snapshot explicitly allowed", manifest.get("snapshot_state") in {"pending", "verified"})
    else:
        add("snapshot verified", manifest.get("snapshot_state") == "verified")
        add("same-owner repeatability verified", truth.get("same_owner_repeatability") is True)

    report = (phase / "deliverables/v644-v1-boundary-evidence-report.html").read_text(encoding="utf-8")
    report_fold = report.casefold()
    add("report language", '<html lang="en-nz">' in report_fold)
    add("report title", "sable rook v644-v1" in report_fold)
    add("report terminal verdict", "not_ready_for_stage_20" in report_fold)
    add("report Māori boundary", "māori" in report_fold)
    add("report has no script", "<script" not in report_fold)
    add("report has no iframe", "<iframe" not in report_fold)
    add("report has no event handlers", re.search(r"\son[a-z]+\s*=", report_fold) is None)
    add("report has no javascript URL", "javascript:" not in report_fold)
    add("report has table headers", "<th " in report_fold or "<th>" in report_fold)
    add("report has caption", "<caption>" in report_fold)
    overview = (phase / "deliverables/v644-v1-final-integrated-overview.md").read_text(encoding="utf-8")
    overview_words = len(re.findall(r"\b\w+[\w’-]*\b", overview, flags=re.UNICODE))
    add("overview three-page equivalent", overview_words >= 1200, overview_words)

    add("privacy scan valid", privacy.get("valid") is True)
    add("privacy zero hits", privacy.get("hit_count") == 0)
    add("privacy scanned files", privacy.get("scanned_file_count", 0) > 0)
    add("Stage 20 noncompensatory", board.get("compensation_across_domains_allowed") is False)
    add("all Stage 20 domains veto", all(row.get("decision") == "veto" for row in board.get("vetoes", [])))

    json_files = sorted(phase.rglob("*.json"))
    parse_failures = []
    for path in json_files:
        try:
            load(path)
            add(f"JSON parse {path.relative_to(phase).as_posix()}", True)
        except Exception as exc:
            parse_failures.append(f"{path}: {exc}")
            add(f"JSON parse {path.relative_to(phase).as_posix()}", False, str(exc))

    add("source ancestor", subprocess.run(["git", "merge-base", "--is-ancestor", engine.SOURCE_COMMIT, "HEAD"], cwd=repo).returncode == 0)
    add("source seal ancestor", subprocess.run(["git", "merge-base", "--is-ancestor", engine.SOURCE_SEAL, "HEAD"], cwd=repo).returncode == 0)
    add("x1 ancestor", subprocess.run(["git", "merge-base", "--is-ancestor", engine.X1_COMMIT, "HEAD"], cwd=repo).returncode == 0)
    add("no merge commits since source", int(git(repo, "rev-list", "--merges", f"{engine.SOURCE_COMMIT}..HEAD", "--count")) == 0)

    issues = [row["name"] for row in checks if not row["passed"]]
    return {
        "schema": "ghc.family.v644-v1.detailed-validation.v1", "phase": "v644-gmut-thos-v1-x1-x2",
        "valid": not issues, "checks_passed": len(checks) - len(issues), "checks_total": len(checks), "issues": issues,
        "proposal_count": 10, "distribution": EXPECTED_DISTRIBUTION, "case_count": 80,
        "retained_negative_count": negatives.get("negative_count"), "manifest_entry_count": manifest.get("entry_count"),
        "json_files_parsed": len(json_files) - len(parse_failures), "json_parse_failures": parse_failures,
        "privacy_files_scanned": privacy.get("scanned_file_count"), "privacy_hit_count": privacy.get("hit_count"),
        "overview_word_count": overview_words, "allow_pending_snapshot": allow_pending_snapshot,
        "same_owner_repeatability_only": True, "independent_team_reproduction": False,
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--phase-dir", type=Path)
    parser.add_argument("--allow-pending-snapshot", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    repo = args.repo.resolve()
    phase = args.phase_dir if args.phase_dir and args.phase_dir.is_absolute() else repo / (args.phase_dir or PHASE_REL)
    result = validate(repo, phase, args.allow_pending_snapshot)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        output = args.output if args.output.is_absolute() else repo / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8", newline="\n")
    print(json.dumps({key: result[key] for key in ("valid", "checks_passed", "checks_total", "issues", "retained_negative_count", "manifest_entry_count", "json_files_parsed", "privacy_files_scanned", "privacy_hit_count", "overview_word_count")}, ensure_ascii=False))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
