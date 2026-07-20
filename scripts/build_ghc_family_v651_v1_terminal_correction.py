#!/usr/bin/env python3
"""Build the additive Sable Rook v651-v1 terminal correction."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import build_ghc_family_v651_v1_closeout as b
import ghc_family_v651_v1_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
SOURCE = d.SOURCE_HEAD
EVIDENCE = b.EVIDENCE
CLOSEOUT = b.CLOSEOUT
EFFECTIVE_NEGATIVES = 6563


def run(*args: str) -> str:
    env = os.environ.copy()
    env.update({"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"})
    result = subprocess.run(list(args), cwd=REPO, check=True, capture_output=True, text=True, encoding="utf-8", env=env)
    return result.stdout.strip()


def git(*args: str) -> str:
    return run("git", *args)


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return path


def write_text(relative: str, payload: str) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def status_paths() -> list[str]:
    raw = subprocess.check_output(["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"], cwd=REPO)
    return sorted({row[3:].replace("\\", "/") for row in raw.decode("utf-8").split("\0") if len(row) > 3})


def changed_paths(base: str) -> list[str]:
    committed = set(filter(None, git("diff", "--name-only", f"{base}..HEAD").splitlines()))
    return sorted(committed | set(status_paths()))


def prospective_bytes(path: Path) -> bytes:
    raw = path.read_bytes()
    if b"\0" not in raw:
        raw = raw.replace(b"\r\n", b"\n")
    return raw


def build_manifests() -> dict[str, int]:
    exclusions = [
        f"{d.PHASE_ROOT}/validation/final-owner-manifest.json",
        f"{d.PHASE_ROOT}/validation/final-owner-privacy.json",
        f"{d.PHASE_ROOT}/validation/final-delta-manifest.json",
        f"{d.PHASE_ROOT}/validation/final-delta-privacy.json",
        f"{d.PHASE_ROOT}/validation/correction-staged-manifest.json",
        f"{d.PHASE_ROOT}/validation/correction-staged-review.json",
        f"{d.PHASE_ROOT}/validation/correction-staged-privacy.json",
    ]
    definitions = {
        "scripts/build_ghc_family_v651_v1_closeout.py",
        "scripts/build_ghc_family_v651_v1_terminal_correction.py",
        "scripts/validate_ghc_family_v651_v1_final.py",
        f"{d.PHASE_ROOT}/validation/final-owner-privacy.json",
        f"{d.PHASE_ROOT}/validation/final-delta-privacy.json",
        f"{d.PHASE_ROOT}/validation/correction-staged-privacy.json",
    }

    owner_paths = changed_paths(SOURCE)
    owner_entries = [b.hash_entry(path) for path in owner_paths if path not in exclusions and (REPO / path).is_file()]
    owner_privacy = b.privacy_scan(owner_paths, definitions, "ghc.family.v651-v1.final-owner-privacy.correction.v1")
    write_json("validation/final-owner-privacy.json", owner_privacy)
    write_json("validation/final-owner-manifest.json", {
        "schema": "ghc.family.v651-v1.final-owner-manifest.correction.v1",
        "hash_domain": "git_path_filtered_blob",
        "source_head": SOURCE,
        "closeout_head": CLOSEOUT,
        "entry_count": len(owner_entries),
        "entries": owner_entries,
        "self_exclusions": exclusions,
        "coverage_contract": "source-to-terminal-correction changed paths",
    })

    delta_paths = changed_paths(EVIDENCE)
    delta_entries = [b.hash_entry(path) for path in delta_paths if path not in exclusions and (REPO / path).is_file()]
    delta_privacy = b.privacy_scan(delta_paths, definitions, "ghc.family.v651-v1.final-delta-privacy.correction.v1")
    write_json("validation/final-delta-privacy.json", delta_privacy)
    write_json("validation/final-delta-manifest.json", {
        "schema": "ghc.family.v651-v1.final-delta-manifest.correction.v1",
        "hash_domain": "git_path_filtered_blob",
        "evidence_head": EVIDENCE,
        "closeout_head": CLOSEOUT,
        "entry_count": len(delta_entries),
        "entries": delta_entries,
        "self_exclusions": exclusions,
        "coverage_contract": "evidence-to-terminal-correction changed paths",
    })

    correction_manifest_rel = f"{d.PHASE_ROOT}/validation/correction-staged-manifest.json"
    correction_review_rel = f"{d.PHASE_ROOT}/validation/correction-staged-review.json"
    correction_privacy_rel = f"{d.PHASE_ROOT}/validation/correction-staged-privacy.json"
    correction_paths = status_paths()
    correction_privacy = b.privacy_scan(correction_paths, definitions, "ghc.family.v651-v1.correction-staged-privacy.v1")
    write_json("validation/correction-staged-privacy.json", correction_privacy)
    correction_paths = status_paths()
    correction_privacy = b.privacy_scan(correction_paths, definitions, "ghc.family.v651-v1.correction-staged-privacy.v1")
    write_json("validation/correction-staged-privacy.json", correction_privacy)
    correction_paths = status_paths()
    entries = []
    for relative in correction_paths:
        if relative in {correction_manifest_rel, correction_review_rel}:
            continue
        raw = prospective_bytes(REPO / relative)
        entries.append({"path": relative, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw), "hash_domain": "prospective_normalized_git_blob_bytes"})
    write_json("validation/correction-staged-review.json", {
        "schema": "ghc.family.v651-v1.correction-staged-review.v1",
        "lifecycle": "terminal_correction",
        "closeout_head": CLOSEOUT,
        "intended_path_count": len(entries) + 2,
        "content_entry_count_before_review": len(entries),
        "self_exclusions": [correction_manifest_rel],
        "privacy_receipt": correction_privacy_rel,
        "privacy_confirmed_hits": correction_privacy["confirmed_hit_count"],
        "x1_immutable": True,
        "evidence_immutable": True,
        "closeout_immutable": True,
        "expected_phase_commits": 4,
        "terminal_route": "PREPARED_NOT_SENT",
    })
    review_raw = prospective_bytes(ROOT / "validation/correction-staged-review.json")
    entries.append({"path": correction_review_rel, "sha256": hashlib.sha256(review_raw).hexdigest(), "bytes": len(review_raw), "hash_domain": "prospective_normalized_git_blob_bytes"})
    write_json("validation/correction-staged-manifest.json", {
        "schema": "ghc.family.v651-v1.correction-staged-manifest.v1",
        "closeout_head": CLOSEOUT,
        "entries": sorted(entries, key=lambda row: row["path"]),
        "entry_count": len(entries),
        "self_exclusions": [correction_manifest_rel],
        "covered_path_count": len(entries) + 1,
    })

    hits = owner_privacy["confirmed_hit_count"] + delta_privacy["confirmed_hit_count"] + correction_privacy["confirmed_hit_count"]
    if hits:
        raise RuntimeError(f"terminal correction privacy scans found {hits} confirmed hits")
    return {
        "owner_paths": len(owner_paths),
        "owner_entries": len(owner_entries),
        "delta_paths": len(delta_paths),
        "delta_entries": len(delta_entries),
        "correction_paths": len(correction_paths),
        "correction_entries": len(entries),
    }


def build() -> None:
    if git("rev-parse", "HEAD") != CLOSEOUT:
        raise RuntimeError("terminal correction must begin at the immutable combined closeout head")
    method_counts = load("method-flow/method-flow-state.json")["counts"]
    if method_counts["methods"] != 16 or method_counts["witness_results"] != {"fail": 20, "pass": 18}:
        raise RuntimeError("terminal correction Method Flow counts drift")

    write_text("deliverables/final-integrated-overview.md", b.integrated_overview())
    write_text("deliverables/final-static-report.html", b.static_report())
    write_text("handoffs/orin-thale-v651-v2-activation.md", b.successor_baton())
    write_text("wellbeing/final-wellbeing-check.md", """# Sable Rook v651-v1 final wellbeing and workload check

Work stayed inside one owner lane, four phase commits, the 15,000-owner-file threshold, and bounded software, symbolic, structural, synthetic, or reservation evidence. Twenty failures remain visible beside eighteen bounded passing recovery witnesses; none was erased. The fourth commit is an additive terminal correction for commit-lifecycle, hash-domain, stale-label, and validation-wrapper assumptions, not a history rewrite. No participant recruitment, aviation operation, production identity operation, sibling mutation, elevation, host-security weakening, Sandbox or Hyper-V activation, unrelated installation, desktop update, or reboot occurred. The route remains pausable, corrigible, and held before proof. This is workflow care, not a consciousness, personhood, continuity, employment, qualification, health, or authority claim.
""")

    truth = load("final/phase-truth.json")
    truth.update({
        "closeout_head": CLOSEOUT,
        "final_head_binding": "terminal_correction_commit_containing_this_record",
        "phase_commit_count": 4,
        "effective_negatives": EFFECTIVE_NEGATIVES,
        "negative_breakdown": {"inherited": d.INHERITED_NEGATIVES, "x1_operational": 5, "x2_operational": 15, "executed_rejected_synthetic": 100},
        "terminal_correction_reason": "Make the closeout manifest test explicit across commit domains, bind prospective audits to their declared normalized Git-blob domain, keep stale-label review out of opaque hashes, and retain each wrapper or sequencing failure before canonical validation.",
    })
    write_json("final/phase-truth.json", truth)

    negatives = load("final/retained-negative-register.json")
    if not any(row["negative_id"] == "V6511-X2-N14" for row in negatives["owner_operational_entries"]):
        negatives["owner_operational_entries"].append({
            "negative_id": "V6511-X2-N14",
            "disposition": "retained",
            "failure": "The committed closeout manifest test used working status as its only evidence domain and would falsely fail after commit.",
            "recovery": "The corrected test preserves staged status precommit and uses the immutable evidence-to-closeout diff postcommit; the status-only assumption keeps zero terminal-test credit.",
        })
    if not any(row["negative_id"] == "V6511-X2-N15" for row in negatives["owner_operational_entries"]):
        negatives["owner_operational_entries"].append({
            "negative_id": "V6511-X2-N15",
            "disposition": "retained",
            "failure": "The correction precommit selection ran 47 tests and failed one because historical closeout manifest hashes were compared with successor working-tree bytes.",
            "recovery": "The historical manifest test now resolves both coverage and content from the immutable closeout commit; the failed aggregate keeps zero validation credit.",
        })
    additions = [
        ("V6511-X2-N16", "A precommit wrapper compared raw checkout bytes with prospective normalized Git-blob manifests and falsely reported hash mismatches after all other aggregate checks passed.", "A bounded witness reproduced the declared CRLF-to-LF prospective hash domain and granted the failed aggregate zero precommit credit."),
        ("V6511-X2-N17", "A helper inspection appended a literal scripts/*.py path and returned a Windows path-syntax error after partial output.", "Exact LiteralPath reads exposed the prospective-byte helpers without wildcard expansion; the recurrence keeps zero search credit."),
        ("V6511-X2-N18", "The Method Flow summary writer reached console output and then raised a CP1252 UnicodeEncodeError on Māori text.", "The same summary command completed with UTF-8 standard streams pinned; the failed emission keeps zero summary credit."),
        ("V6511-X2-N19", "A narrow hash-domain recovery probe ran before rebuilding four later-mutated Method Flow files and therefore retained twelve manifest-entry mismatches.", "The method witness separated 28 domain recoveries from the four known later mutations and reserved aggregate credit until a full rebuild."),
        ("V6511-X2-N20", "An exact staged stale-label probe used raw digit substrings and falsely flagged 6557 and 6558 inside SHA-256 values after all substantive index checks passed.", "Field-aware and prose-boundary patterns found zero semantic stale labels while excluding opaque hashes by construction; the failed staged aggregate keeps zero review credit."),
    ]
    for negative_id, failure, recovery in additions:
        if not any(row["negative_id"] == negative_id for row in negatives["owner_operational_entries"]):
            negatives["owner_operational_entries"].append({"negative_id": negative_id, "disposition": "retained", "failure": failure, "recovery": recovery})
    negatives.update({"effective": EFFECTIVE_NEGATIVES, "x2_operational_count": 15, "method_failed_witnesses": 20, "method_passing_witnesses": 18})
    write_json("final/retained-negative-register.json", negatives)

    closeout = load("final/closeout-receipt.json")
    closeout.update({"closeout_head": CLOSEOUT, "final_head_binding": "terminal_correction_commit_containing_this_record", "expected_phase_commits": 4, "terminal_correction": "dual_state_manifest_test_and_lifecycle_anchor_update", "effective_negatives": EFFECTIVE_NEGATIVES})
    write_json("final/closeout-receipt.json", closeout)
    seal = load("final/seal-candidate-receipt.json")
    seal.update({"closeout_head": CLOSEOUT, "head_binding": "terminal_correction_commit_containing_this_record", "direct_parent_required": CLOSEOUT, "expected_phase_commits": 4})
    write_json("final/seal-candidate-receipt.json", seal)
    contract = load("final/final-validation-contract.json")
    contract.update({"expected_head": "terminal_correction_commit_containing_this_record", "expected_parent": CLOSEOUT, "closeout_head": CLOSEOUT, "expected_phase_commits": 4})
    write_json("final/final-validation-contract.json", contract)
    write_json("final/terminal-correction-receipt.json", {
        "schema": "ghc.family.v651-v1.terminal-correction.v1",
        "closeout_head": CLOSEOUT,
        "final_head_binding": "commit_containing_this_record",
        "reason": "Correct commit-lifecycle, historical-blob, prospective hash-domain, stale-label, and wrapper-sequencing assumptions before canonical validation.",
        "phase_commit_count": 4,
        "authorized_commit_cap": 4,
        "history_rewritten": False,
        "x1_changed": False,
        "evidence_changed": False,
        "outcomes_changed": False,
        "terminal_route": "PREPARED_NOT_SENT",
    })

    run(sys.executable, str(b.INDEX_RUNNER), "--repo", str(REPO), "--skill-root", str(Path.home() / ".codex" / "skills"), "--out-dir", str(ROOT / "tooling/correction-index"), "--phase", d.PHASE, "--owner", d.OWNER)
    manifests = build_manifests()
    print(json.dumps({"phase": d.PHASE, "state": "terminal_correction_built_not_committed", "effective_negatives": EFFECTIVE_NEGATIVES, "method_failures": 20, "method_passes": 18, **manifests, "privacy_hits": 0}, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    build()
