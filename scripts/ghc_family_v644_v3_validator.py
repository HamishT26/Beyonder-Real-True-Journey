#!/usr/bin/env python3
"""Detailed, standard-library validator for Tamar Vey v644-v3."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

from ghc_family_v644_v3_evidence import (
    PHASE,
    SOURCE_HEAD,
    SOURCE_SEAL,
    X1_COMMIT,
    normalized_sha256,
    stable_manifest_paths,
)
from ghc_family_v644_v3_model import SPECS, all_cases, evaluate_record


PHASE_REL = Path("docs/tamar-vey/v644-v3")
EXPECTED_DISTRIBUTION = {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}
EXPECTED_SOURCE_STATUS = {"current": 78, "stable": 86, "draft": 8, "watch": 3}
EXPECTED_INHERITED_NEGATIVES = 1220
EXPECTED_X1_NEGATIVES = 6
EXPECTED_SYNTHETIC_NEGATIVES = 70


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git(repo: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args], cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, encoding="utf-8", errors="replace", check=False,
    )
    if check and result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result.stdout.strip()


def is_ancestor(repo: Path, ancestor: str, descendant: str = "HEAD") -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=repo, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False,
    ).returncode == 0


def validate(
    repo: Path,
    phase: Path | None = None,
    allow_pending_snapshot: bool = False,
    expected_head: str | None = None,
) -> dict[str, Any]:
    repo = repo.resolve()
    phase = (phase or repo / PHASE_REL).resolve()
    checks: list[dict[str, Any]] = []

    def add(name: str, passed: bool, detail: Any = None) -> None:
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    required = [
        "x1-proposals.json", "x2-proposal-ledger.json", "phase-truth.json",
        "retained-negative-register.json", "exact-open-gate-register.json",
        "complete-incomplete-checklist.json", "threat-model.json",
        "evidence/evidence-ledger.json", "environment/x2-execution-receipt.json",
        "reproduction/x1-content-seal.json", "reproduction/manifest.json",
        "reproduction/independent-team-gap.json", "stage20/domain-veto-evidence-board.json",
        "tooling/executed-toolchain.json", "deliverables/v644-v3-final-integrated-overview.md",
        "deliverables/v644-v3-boundary-evidence-report.html",
        "accessibility/static-report-receipt.json", "validation/x2-privacy-scan.json",
    ]
    for relative in required:
        add(f"required file {relative}", (phase / relative).is_file())

    proposals = load(phase / "x1-proposals.json")
    ledger = load(phase / "x2-proposal-ledger.json")
    truth = load(phase / "phase-truth.json")
    negatives = load(phase / "retained-negative-register.json")
    inherited = load(repo / "docs/orin-thale/v644-v2/retained-negative-register.json")
    gates = load(phase / "exact-open-gate-register.json")
    seal = load(phase / "reproduction/x1-content-seal.json")
    manifest = load(phase / "reproduction/manifest.json")
    privacy = load(phase / "validation/x2-privacy-scan.json")
    sources = load(phase / "sources/source-ledger.json")
    board = load(phase / "stage20/domain-veto-evidence-board.json")
    checklist = load(phase / "complete-incomplete-checklist.json")

    add("phase identity", truth.get("phase") == PHASE and truth.get("owner") == "Tamar Vey")
    add("proposal count ten", proposals.get("proposal_count") == 10 == ledger.get("proposal_count"))
    add("prior proposal count 250", proposals.get("prior_frozen_proposal_count") == 250)
    add("four outcome labels", proposals.get("outcome_classes") == ["completed", "represented", "open_gap", "exact_gate"])
    add("truth distribution", truth.get("proposal_distribution") == EXPECTED_DISTRIBUTION)
    add("ledger distribution", ledger.get("distribution") == EXPECTED_DISTRIBUTION)
    add("eighty cases", ledger.get("total_case_count") == 80 == truth.get("case_count"))
    add("seventy synthetic negatives", ledger.get("synthetic_negative_count") == 70 == truth.get("synthetic_negative_count"))
    add("primary focus GMUT Mind", truth.get("primary_focus") == "GMUT Mind")
    add("terminal verdict", truth.get("terminal_verdict") == "NOT_READY_FOR_STAGE_20")
    add("route prepared not sent", truth.get("route_state") == "PREPARED_NOT_SENT" and truth.get("outbound_message_count") == 0)
    add("no successor or subagent", truth.get("successor_task_count") == 0 and truth.get("subagent_count") == 0)
    add("protected claims false", bool(truth.get("protected_claims")) and all(value is False for value in truth["protected_claims"].values()))
    add("owned packet complete, Stage 20 false", checklist.get("owned_evidence_packet_complete") is True and checklist.get("stage20_ready") is False)

    add("source count 175", sources.get("effective_source_count") == 175)
    add("source status classes", sources.get("effective_status_counts") == EXPECTED_SOURCE_STATUS)
    add("eleven new sources", sources.get("added_source_count") == 11)
    add("source labels nonduplicated", not sources.get("duplicate_added_titles") and not sources.get("duplicate_added_urls"))

    add("x1 seal commit", seal.get("x1_commit") == X1_COMMIT)
    add("x1 seal 27 entries", seal.get("file_count") == 27 == len(seal.get("entries", [])))
    add("x1 seal reports unchanged", seal.get("all_current_blobs_unchanged") is True)
    for row in seal.get("entries", []):
        path = row.get("path", "")
        current_oid = git(repo, "rev-parse", f"HEAD:{path}", check=False)
        add(f"x1 path exists {path}", (repo / path).is_file())
        add(f"x1 blob immutable {path}", row.get("blob_unchanged") is True and current_oid == row.get("x1_blob_oid"))

    x2_ops = negatives.get("x2_operational_count", 0)
    expected_negative_count = EXPECTED_INHERITED_NEGATIVES + EXPECTED_X1_NEGATIVES + EXPECTED_SYNTHETIC_NEGATIVES + x2_ops
    rows = negatives.get("negatives", [])
    add("negative count exact", negatives.get("negative_count") == expected_negative_count == len(rows))
    add("negative component counts", negatives.get("inherited_count") == EXPECTED_INHERITED_NEGATIVES and negatives.get("x1_operational_count") == EXPECTED_X1_NEGATIVES and negatives.get("new_synthetic_count") == EXPECTED_SYNTHETIC_NEGATIVES)
    add("inherited negatives exact prefix", rows[:EXPECTED_INHERITED_NEGATIVES] == inherited.get("negatives", []))
    ids = [row.get("negative_id") for row in rows]
    add("negative IDs unique", len(ids) == len(set(ids)) and all(ids))
    for index, row in enumerate(rows):
        add(f"negative {index:04d} retained", row.get("retained") is True)

    add("five open gaps", gates.get("open_gap_count") == 5 == len(gates.get("open_gaps", [])))
    add("six exact gates", gates.get("exact_gate_count") == 6 == len(gates.get("exact_gates", [])))
    add("gates visible", gates.get("all_visible") is True and gates.get("none_silently_closed") is True)
    add("Māori authority gate visible", "Māori" in json.dumps(gates, ensure_ascii=False))
    for row in gates.get("open_gaps", []):
        add(f"open gap {row.get('gate_id')}", row.get("state") == "open")
    for row in gates.get("exact_gates", []):
        add(f"exact gate {row.get('gate_id')}", row.get("state") == "pending_exact_authority")

    case_sets = all_cases()
    add("ten case groups", len(case_sets) == 10 == len(SPECS))
    add("eighty case rows", sum(1 + len(item["mutations"]) for item in case_sets.values()) == 80)
    rejected = 0
    for proposal_id, case_set in case_sets.items():
        control = case_set["control"]
        add(f"{proposal_id} control outcome", control["evaluation"]["decision"] == SPECS[proposal_id]["outcome"])
        add(f"{proposal_id} control reproducible", evaluate_record(proposal_id, control["record"]) == control["evaluation"])
        add(f"{proposal_id} seven mutations", len(case_set["mutations"]) == 7)
        for mutation in case_set["mutations"]:
            is_rejected = mutation["evaluation"]["decision"] == "rejected" and mutation.get("retained") is True
            rejected += int(is_rejected)
            add(f"mutation {mutation['negative_id']} rejected", is_rejected)
    add("seventy mutations rejected", rejected == 70)

    proposal_map = {item["proposal_id"]: item for item in proposals.get("proposals", [])}
    ledger_map = {item["proposal_id"]: item for item in ledger.get("proposals", [])}
    add("proposal IDs align", set(proposal_map) == set(ledger_map) == set(SPECS))
    for proposal_id, proposal in proposal_map.items():
        add(f"{proposal_id} observed outcome", ledger_map.get(proposal_id, {}).get("outcome") == SPECS[proposal_id]["outcome"])
        for relative in proposal.get("deliverables", []):
            add(f"{proposal_id} deliverable {relative}", (phase / relative).is_file())

    manifest_rows = manifest.get("entries", [])
    expected_manifest_paths = [path.relative_to(repo).as_posix() for path in stable_manifest_paths()]
    actual_manifest_paths = [row.get("path") for row in manifest_rows]
    add("manifest count exact", manifest.get("entry_count") == len(manifest_rows) == len(expected_manifest_paths))
    add("manifest paths exact", actual_manifest_paths == expected_manifest_paths)
    manifest_mismatches = []
    for row in manifest_rows:
        target = repo / row.get("path", "")
        passed = target.is_file() and normalized_sha256(target) == row.get("sha256_lf_normalized")
        if not passed:
            manifest_mismatches.append(row.get("path"))
        add(f"manifest hash {row.get('path')}", passed)
    add("manifest same-owner boundary", manifest.get("same_owner_repeatability_only") is True and manifest.get("independent_team_reproduction") is False)
    if allow_pending_snapshot:
        add("snapshot state pending allowed", manifest.get("snapshot_state") in {"pending", "verified"})
    else:
        add("snapshot state verified", manifest.get("snapshot_state") == "verified")
        add("same-owner repeatability verified", truth.get("same_owner_repeatability") is True)

    report = (phase / "deliverables/v644-v3-boundary-evidence-report.html").read_text(encoding="utf-8")
    folded = report.casefold()
    add("report language", '<html lang="en">' in folded)
    add("report skip link", 'href="#main"' in folded and 'id="main"' in folded)
    add("report terminal verdict", "not_ready_for_stage_20" in folded)
    add("report Māori boundary", "māori" in folded)
    add("report no active script", "<script" not in folded and "<iframe" not in folded and "javascript:" not in folded and re.search(r"\son[a-z]+\s*=", folded) is None)
    add("report table semantics", "<caption>" in folded and 'scope="col"' in folded and 'scope="row"' in folded)
    overview = (phase / "deliverables/v644-v3-final-integrated-overview.md").read_text(encoding="utf-8")
    overview_words = len(re.findall(r"\b\w+[\w’'-]*\b", overview, flags=re.UNICODE))
    add("overview three-page equivalent", overview_words >= 1200, overview_words)
    add("privacy valid", privacy.get("valid") is True and privacy.get("hit_count") == 0 and privacy.get("scanned_file_count", 0) > 0)
    add("Stage 20 noncompensatory", board.get("compensation_across_domains_allowed") is False)
    add("all Stage 20 domains veto", all(row.get("decision") == "veto" for row in board.get("vetoes", [])))

    json_files = sorted(phase.rglob("*.json"))
    json_issues: list[str] = []
    for path in json_files:
        try:
            load(path)
            add(f"JSON parse {path.relative_to(phase).as_posix()}", True)
        except Exception as exc:  # pragma: no cover - defensive receipt path
            json_issues.append(f"{path.relative_to(phase).as_posix()}: {exc}")
            add(f"JSON parse {path.relative_to(phase).as_posix()}", False, str(exc))

    head = git(repo, "rev-parse", "HEAD")
    add("source ancestor", is_ancestor(repo, SOURCE_HEAD))
    add("source seal ancestor", is_ancestor(repo, SOURCE_SEAL))
    add("x1 ancestor", is_ancestor(repo, X1_COMMIT))
    add("zero merges since source", int(git(repo, "rev-list", "--merges", f"{SOURCE_HEAD}..HEAD", "--count")) == 0)
    if expected_head:
        add("exact expected head", head == expected_head, {"expected": expected_head, "actual": head})

    issues = [row["name"] for row in checks if not row["passed"]]
    return {
        "schema": "ghc.family.v644-v3.detailed-validation.v1",
        "phase": PHASE,
        "valid": not issues,
        "checks_passed": len(checks) - len(issues),
        "checks_total": len(checks),
        "issues": issues,
        "current_head": head,
        "expected_head": expected_head,
        "proposal_distribution": EXPECTED_DISTRIBUTION,
        "retained_negative_count": negatives.get("negative_count"),
        "manifest_entries": manifest.get("entry_count"),
        "manifest_mismatch_count": len(manifest_mismatches),
        "json_files_parsed": len(json_files) - len(json_issues),
        "json_parse_issues": json_issues,
        "privacy_files_scanned": privacy.get("scanned_file_count"),
        "privacy_hit_count": privacy.get("hit_count"),
        "overview_word_count": overview_words,
        "x1_content_unchanged": seal.get("all_current_blobs_unchanged") is True,
        "allow_pending_snapshot": allow_pending_snapshot,
        "same_owner_repeatability_only": True,
        "independent_team_reproduction": False,
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--phase-dir", type=Path)
    parser.add_argument("--allow-pending-snapshot", action="store_true")
    parser.add_argument("--expected-head")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    repo = args.repo.resolve()
    phase = args.phase_dir if args.phase_dir and args.phase_dir.is_absolute() else repo / (args.phase_dir or PHASE_REL)
    result = validate(repo, phase, args.allow_pending_snapshot, args.expected_head)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        output = args.output if args.output.is_absolute() else repo / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8", newline="\n")
    summary_keys = (
        "valid", "checks_passed", "checks_total", "issues", "retained_negative_count",
        "manifest_entries", "manifest_mismatch_count", "json_files_parsed", "privacy_files_scanned",
        "privacy_hit_count", "overview_word_count", "x1_content_unchanged",
    )
    print(json.dumps({key: result[key] for key in summary_keys}, ensure_ascii=False))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
