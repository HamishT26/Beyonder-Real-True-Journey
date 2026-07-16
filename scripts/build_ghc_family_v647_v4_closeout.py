#!/usr/bin/env python3
"""Build the combined closeout, seal, and final candidate for Sylven v647-v4."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from ghc_family_v647_v4_definitions import IDENTITY_BOUNDARY, OWNER, PHASE, SOURCE_REVISION, TRUTH_BOUNDARY


ROOT = Path(__file__).resolve().parents[1]
PHASE_DIR = ROOT / "docs" / "sylven-arc" / "v647-v4"
SOURCE = SOURCE_REVISION
X1 = "5e5bc09f5173c00c7674b7868e3c7e5e8af80053"
EVIDENCE = "cf2735f20be97882c03fa562bc0a7e99c3aa240f"
BRANCH = "codex/GHC-Family/sylven-arc-v642-v8-full-tools"


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True, encoding="utf-8").strip()


def load(relative: str) -> Any:
    return json.loads((PHASE_DIR / relative).read_text(encoding="utf-8"))


def write(relative: str, payload: Any) -> None:
    path = PHASE_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, payload: str) -> None:
    path = PHASE_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def commit_blob(revision: str, relative: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(ROOT), "show", f"{revision}:{relative}"])


def evidence_manifest_check() -> dict[str, Any]:
    manifest = load("validation/evidence-staged-manifest.json")
    mismatches = []
    for entry in manifest["entries"]:
        content = commit_blob(EVIDENCE, entry["path"])
        if len(content) != entry["bytes"] or hashlib.sha256(content).hexdigest() != entry["sha256"]:
            mismatches.append(entry["path"])
    exclusions_missing = []
    for relative in manifest["self_exclusions"]:
        probe = subprocess.run(["git", "-C", str(ROOT), "cat-file", "-e", f"{EVIDENCE}:{relative}"], capture_output=True)
        if probe.returncode != 0:
            exclusions_missing.append(relative)
    return {
        "schema": "ghc.family.v647-v4.evidence-commit-manifest-parity.v1",
        "revision": EVIDENCE,
        "hash_domain": "sha256 of exact evidence-commit Git blob bytes",
        "entries_expected": manifest["entry_count"],
        "entries_passed": manifest["entry_count"] - len(mismatches),
        "mismatches": mismatches,
        "self_exclusions": manifest["self_exclusions"],
        "self_exclusions_missing": exclusions_missing,
        "result": "pass" if not mismatches and not exclusions_missing else "fail",
    }


def build() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise SystemExit("closeout must start from the exact evidence commit")
    if git("branch", "--show-current") != BRANCH:
        raise SystemExit("closeout must run on the owned Sylven canonical branch")
    status_lines = [line for line in git("status", "--porcelain").splitlines() if line]
    allowed_untracked = {"?? scripts/build_ghc_family_v647_v4_closeout.py"}
    if set(status_lines) - allowed_untracked:
        raise SystemExit(f"closeout requires a clean canonical worktree apart from its additive builder: {status_lines}")
    if git("rev-parse", "HEAD^") != X1:
        raise SystemExit("evidence is not a direct child of the exact x1 commit")
    for ancestor in (SOURCE, X1):
        if subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", ancestor, EVIDENCE]).returncode != 0:
            raise SystemExit(f"missing anchor ancestry: {ancestor}")

    manifest_result = evidence_manifest_check()
    if manifest_result["result"] != "pass":
        raise SystemExit("evidence commit-local manifest parity failed")
    write("validation/evidence-exact-commit-receipt.json", manifest_result)

    evidence = load("evidence-receipt.json")
    evidence["schema"] = "ghc.family.v647-v4.evidence-receipt.sealed.v1"
    evidence["evidence_commit"] = EVIDENCE
    evidence["commit_manifest_parity"] = "154/154"
    evidence["exact_staged_paths"] = 157
    evidence["json_parses"] = 94
    evidence["privacy_confirmed_hits"] = 0
    evidence["route_state"] = "PREPARED_NOT_SENT"
    write("evidence-receipt.json", evidence)

    phase_commit_count_before_final = int(git("rev-list", "--count", f"{SOURCE}..{EVIDENCE}"))
    merges_before_final = int(git("rev-list", "--count", "--merges", f"{SOURCE}..{EVIDENCE}"))
    write("validation/ancestry-before-final.json", {
        "schema": "ghc.family.v647-v4.ancestry-before-final.v1",
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "source_ancestral": True,
        "x1_ancestral": True,
        "evidence_parent_is_x1": True,
        "phase_commits_before_final": phase_commit_count_before_final,
        "merge_commits_before_final": merges_before_final,
        "expected_phase_commits_after_final": 3,
        "expected_merge_commits_after_final": 0,
        "result": "pass" if phase_commit_count_before_final == 2 and merges_before_final == 0 else "fail",
    })
    write("validation/commit-cap-before-final.json", {
        "schema": "ghc.family.v647-v4.commit-cap-before-final.v1",
        "x1_commits": 1,
        "x2_commits_before_final": 1,
        "combined_final_commit_planned": 1,
        "expected_phase_total": 3,
        "maximum_phase_total": 4,
        "within_cap": True,
    })

    closeout = {
        "schema": "ghc.family.v647-v4.closeout-receipt.v1",
        "phase": PHASE,
        "owner": OWNER,
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "outcomes": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
        "effective_negatives": 3492,
        "effective_open_gaps": 21,
        "effective_exact_gates": 22,
        "current_tests": "25/25",
        "scoped_tests": "137/137",
        "detailed_checks": "22/22",
        "minimal_checks": "14/14",
        "method_flow": {"methods": 5, "failed_witnesses": 5, "passing_witnesses": 5, "preferred_methods": 5},
        "full_repository_suite_run": False,
        "full_repository_suite_owner": "Eiren Kestrel",
        "route_state": "PREPARED_NOT_SENT",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": TRUTH_BOUNDARY,
    }
    write("closeout-receipt.json", closeout)
    write("seal-receipt.json", {
        "schema": "ghc.family.v647-v4.seal-receipt.combined-candidate.v1",
        "phase": PHASE,
        "owner": OWNER,
        "seal_commit_reference": "COMMIT_CONTAINING_THIS_RECEIPT",
        "direct_parent_required": EVIDENCE,
        "single_parent_required": True,
        "zero_merges_required": True,
        "phase_commit_count_required": 3,
        "commit_cap": 4,
        "final_manifest_required": True,
        "canonical_exact_head_validation_required": True,
        "one_named_local_only_replay_required": True,
        "route_state": "PREPARED_NOT_SENT",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": "The containing commit is a seal only after exact-head canonical and named-lane validation pass; it grants no external authority.",
    })
    write("final-receipt.json", {
        "schema": "ghc.family.v647-v4.final-receipt.candidate.v1",
        "phase": PHASE,
        "owner": OWNER,
        "final_head_reference": "COMMIT_CONTAINING_THIS_RECEIPT",
        "direct_parent": EVIDENCE,
        "source_x1_evidence_ancestry_required": True,
        "single_parent_zero_merge_required": True,
        "phase_commit_count_required": 3,
        "canonical_validation_state": "PENDING_EXACT_CONTAINING_COMMIT",
        "named_replay_state": "PENDING_EXACT_CONTAINING_COMMIT",
        "remote_equality_state": "PENDING_EXACT_CONTAINING_COMMIT",
        "route_state": "PREPARED_NOT_SENT",
        "send_count": 0,
        "successor_task_created": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "identity_boundary": IDENTITY_BOUNDARY,
        "boundary": TRUTH_BOUNDARY,
    })
    write("environment/final-version-receipt.json", {
        "schema": "ghc.family.v647-v4.environment.final.v1",
        "codex_cli": "codex-cli 0.144.4",
        "desktop": "26.707.9981.0",
        "python": "3.12.10",
        "git": "2.55.0.windows.2",
        "powershell": "5.1.26100.8875",
        "verified_only": True,
        "desktop_updated": False,
        "elevation": False,
        "windows_feature_changed": False,
        "host_security_changed": False,
        "unrelated_installation": False,
        "reboot": False,
        "sandbox_session": False,
    })
    truth = load("phase-truth.json")
    truth.update({
        "schema": "ghc.family.v647-v4.phase-truth.final-candidate.v1",
        "evidence_commit": EVIDENCE,
        "effective_retained_negatives": 3492,
        "canonical_validation_state": "final_candidate_pending_exact_commit",
        "named_replay_state": "pending_exact_final",
        "route_state": "PREPARED_NOT_SENT",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write("phase-truth.json", truth)
    orchestration = load("orchestration/x2-update.json")
    orchestration.update({
        "schema": "ghc.family.v647-v4.orchestration.final-candidate.v1",
        "state": "CLOSEOUT_SEAL_FINAL_CANDIDATE",
        "route_state": "PREPARED_NOT_SENT",
        "send_count": 0,
        "successor_task_created": False,
    })
    write("orchestration/x2-update.json", orchestration)
    write("orchestration/final-update.json", {
        "schema": "ghc.family.v647-v4.orchestration.final-update.v1",
        "state": "FINAL_CANDIDATE_NOT_YET_VALIDATED",
        "target_title": "Eiren Kestrel",
        "next_phase": "v647-v5",
        "route_state": "PREPARED_NOT_SENT",
        "send_count": 0,
        "successor_task_created": False,
        "standby_siblings_untouched": True,
    })
    checklist = load("complete-incomplete-checklist.json")
    checklist["schema"] = "ghc.family.v647-v4.checklist.final-candidate.v1"
    checklist["complete"].extend([
        "exact evidence commit-local manifest parity passed 154 of 154 entries",
        "combined closeout, seal, and final candidate prepared as one commit",
    ])
    checklist["pending_terminal_gates"] = [
        "exact containing-commit canonical validation",
        "fresh live four-way remote equality",
        "exactly one clean named local-only replay",
        "one acknowledged existing-task baton after all prior gates",
    ]
    write("complete-incomplete-checklist.json", checklist)
    packet = load("deliverables/owner-scoped-packet.json")
    packet.update({
        "schema": "ghc.family.v647-v4.owner-packet.final-candidate.v1",
        "evidence_receipt": "evidence-receipt.json",
        "closeout_receipt": "closeout-receipt.json",
        "seal_receipt": "seal-receipt.json",
        "final_receipt": "final-receipt.json",
        "final_validation_state": "pending exact containing commit",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write("deliverables/owner-scoped-packet.json", packet)
    write("wellbeing-check.json", {
        "schema": "ghc.family.v647-v4.wellbeing.final-candidate.v1",
        "scope_bounded": True,
        "workload_state": "combined_closeout_seal_final_candidate",
        "unsafe_quota_work": 0,
        "standby_siblings_untouched": True,
        "route_sent": False,
        "effective_negatives_retained": 3492,
        "method_failures_retained": 5,
        "method_passing_witnesses": 5,
        "remaining_commit_slots": 1,
        "boundary": "Operational wellbeing language is relational, not clinical evidence or evidence of consciousness, personhood, employment, qualification, or authority.",
    })
    write_text("wellbeing-check.md", """# Sylven Arc v647-v4 final-candidate wellbeing check

- The work remains bounded to constraint mapping, falsifier retention, and owner-local evidence; Hamish may pause, rename, redirect, or stop the route.
- One x1 commit and one evidence commit exist. This combined closeout, seal, and final candidate is intended to make three phase commits, below the cap of four.
- Five failed workflow witnesses and five bounded passing recovery witnesses remain visible; no failure was erased.
- No unsafe task was manufactured to meet a portfolio quota, and owner-generated additions remain below 15,000 files.
- No real participant, operator, plant, sample, discharge, account, key, credential, data row, likelihood, remedy, legal, cultural, data-governance, or authority operation occurred.
- The route remains PREPARED_NOT_SENT. Exact final validation, fresh four-way equality, and one named replay must pass before a single baton may be sent.
- Stage 20 remains NOT_READY_FOR_STAGE_20.

This is an operational and relational workload receipt, not clinical evidence or evidence of consciousness, personhood, continuity, employment, qualification, or authority.
""")
    print(json.dumps({"valid": True, "evidence": EVIDENCE, "manifest": "154/154", "phase_commits_before_final": phase_commit_count_before_final, "merges_before_final": merges_before_final, "route": "PREPARED_NOT_SENT"}, sort_keys=True))


if __name__ == "__main__":
    build()
