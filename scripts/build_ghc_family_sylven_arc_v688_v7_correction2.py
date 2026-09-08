#!/usr/bin/env python3
"""Prepare a second additive correction for the canonical diff-base predicate."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/sylven-arc/v688-v7"
REL = "docs/sylven-arc/v688-v7"
SOURCE = "e7db6f3be1327de72f93873eb6540aabfc773344"
X1 = "4b7459cdf681726b8d411d644dc6f8db70e83871"
X2 = "3c968db9391583a9e40f0eb8cc0c2f86d9997126"
FIRST_FINAL = "4e2421659eed8617cbd1fd45677b7248db2dfd11"
CORRECTION1 = "c0f79218f2d644592bd4eee0947058f0f3803b50"
BOUNDARY = "Same-owner synthetic software and correction evidence only; no empirical, participant, professional, production, legal, cultural, Maori-authority, independent-reproduction, consciousness, Theory-of-Everything, proof, canon, or Stage 20 evidence."


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_new(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = value.rstrip() + "\n" if isinstance(value, str) else json.dumps(value, indent=2, sort_keys=True) + "\n"
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(text)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bank", type=Path, required=True)
    args = parser.parse_args()
    bank = args.bank.resolve()
    if bank.drive.upper() != "D:":
        raise RuntimeError("D_first_bank_required")
    if subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() != CORRECTION1:
        raise RuntimeError("exact_correction1_required")
    if subprocess.check_output(["git", "diff", "--cached", "--name-only"], cwd=ROOT, text=True).strip():
        raise RuntimeError("unexpected_staged_entry")
    status = set(line for line in subprocess.check_output(["git", "status", "--porcelain=v1"], cwd=ROOT, text=True).splitlines() if line)
    expected = {" M scripts/ghc_family_sylven_arc_v688_v7_canonical.py", "?? scripts/build_ghc_family_sylven_arc_v688_v7_correction2.py"}
    if status != expected:
        raise RuntimeError("correction2_entry_scope:" + repr(sorted(status)))
    failures = load(bank / "post-final-operational-failures.json")["failures"]
    failure = next(item for item in failures if item["failure_id"] == "SA6887-POST-N003")
    destination = BASE / "correction2"
    if destination.exists():
        raise RuntimeError("correction2_destination_exists")
    gates = load(BASE / "x1/new-proposals.json")["proposals"][0]["protected_gates"]
    method = {
        "method_id": "SA6887-M060",
        "title": failure["recovery"],
        "failure_signature": failure["failed_witness"],
        "trigger_preconditions": ["complete owner scope from source", "correction-only mutation scope from immediate parent"],
        "privacy_class": "sanitized_public",
        "approval_class": "safe_now",
        "candidate_workaround": failure["recovery"],
        "validation_witness_ids": ["SA6887-W0622", "SA6887-W0623"],
        "recurrence_guard": failure["recurrence_guard"],
        "rollback": "Retain correction1 and the caught design failure; stop selecting correction2 if its immediate-parent scope fails.",
        "recommendation_state": "preferred",
        "supersedes": [],
        "protected_gates": gates,
        "retained_negative_ids": [failure["failure_id"]],
        "scope_boundary": BOUNDARY,
        "artifact": f"{REL}/correction2/post-final-method-flow-overlay.json",
    }
    witnesses = [
        {"witness_id": "SA6887-W0622", "method_id": "SA6887-M060", "procedure": "source-relative correction-scope predicate", "scope": f"{REL}/correction2/preflight-design-failure.json", "expected": "Distinguish overall owner additions from one correction modification.", "observed": failure["failed_witness"], "result": "fail", "witness_kind": "preflight_design_failure", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [failure["failure_id"]], "boundary": BOUNDARY},
        {"witness_id": "SA6887-W0623", "method_id": "SA6887-M060", "procedure": "immediate-parent correction-scope predicate", "scope": f"{REL}/correction2/preflight-design-failure.json", "expected": "Use source for owner scope and immediate parent for correction scope.", "observed": failure["recovery"], "result": "pass", "witness_kind": "bounded_passing_witness", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [], "boundary": BOUNDARY},
    ]
    combined = {"methods": 60, "witnesses": 623, "failed_witnesses": 548, "passing_witnesses": 75, "state_events": 60, "recommendations": 60}
    effective = {"proposals": 16830, "negatives": 85422, "methods": 94122, "failed_witnesses": 56300, "passing_witnesses": 86185, "open_gaps": 765, "exact_gates": 785}
    write_new(destination / "post-final-method-flow-overlay.json", {"schema": "ghc.family.post-final-method-flow-overlay.v2", "base_ref": f"{REL}/correction1/post-final-method-flow-overlay.json", "methods": [method], "witnesses": witnesses, "state_events": [{"method_id": "SA6887-M060", "from": "candidate", "to": "preferred", "note": "Immediate-parent comparison is prepared while the caught design failure remains retained."}], "recommendations": [{"method_id": "SA6887-M060", "preconditions": "correction-scope audit", "recommendation": failure["recurrence_guard"], "delivered": False}], "overlay_counts": {"methods": 1, "witnesses": 2, "failed_witnesses": 1, "passing_witnesses": 1, "state_events": 1, "recommendations": 1}, "combined_counts": combined, "failed_witnesses_erased": 0, "boundary": BOUNDARY})
    write_new(destination / "phase-truth-overlay.json", {"schema": "ghc.family.corrected-phase-truth.sylven-arc.v688-v7.v2", "owner": "Sylven Arc", "phase": "v688-v7", "source": SOURCE, "x1": X1, "evidence": X2, "first_final": FIRST_FINAL, "correction1": CORRECTION1, "corrected_final": None, "final_binding": "exclusive external exact-corrected-final canonical receipt", "state": "SECOND_CORRECTED_FINAL_CANDIDATE_PENDING_EXTERNAL_CANONICAL", "outcomes": {"completed": 176, "represented": 11, "open_gap": 3, "exact_gate": 10}, "effective_counts": effective, "phase_unique_negatives": 518, "phase_methods": 60, "phase_witnesses": 623, "phase_failed_witnesses": 548, "phase_passing_witnesses": 75, "canonical_invocations": 0, "canonical_successes": 0, "canonical_replays": 0, "prepared_baton_state": "PREPARED_NOT_SENT", "successor_contacts": 0, "new_tasks_created": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "prior_commits_rewritten": False, "boundary": BOUNDARY})
    write_new(destination / "canonical-policy-overlay.json", {"schema": "ghc.family.corrected-owner-canonical-policy.v2", "owner": "Sylven Arc", "phase": "v688-v7", "branch": "codex/GHC-Family/sylven-arc-v688-v7-full-tools", "source": SOURCE, "x1": X1, "evidence": X2, "first_final": FIRST_FINAL, "correction1": CORRECTION1, "expected_phase_commits": 5, "maximum_phase_commits": 8, "test_modules": [
        {"stage": "x1", "definition": X1, "module": "tests/test_ghc_family_sylven_arc_v688_v7_x1.py", "expected_tests": 12, "manifest": f"{REL}/x1/x1-manifest.json"},
        {"stage": "x2", "definition": X2, "module": "tests/test_ghc_family_sylven_arc_v688_v7_x2.py", "expected_tests": 24, "manifest": f"{REL}/x2/evidence-manifest.json"},
        {"stage": "first_final", "definition": FIRST_FINAL, "module": "tests/test_ghc_family_sylven_arc_v688_v7_final.py", "expected_tests": 20, "manifest": f"{REL}/validation/final-owner-manifest.json"},
        {"stage": "correction1", "definition": CORRECTION1, "module": "tests/test_ghc_family_sylven_arc_v688_v7_correction1.py", "expected_tests": 10, "manifest": f"{REL}/correction1/validation/corrected-owner-manifest.json"},
        {"stage": "correction2", "definition": "exact_final", "module": "tests/test_ghc_family_sylven_arc_v688_v7_correction2.py", "expected_tests": 6, "manifest": f"{REL}/correction2/validation/corrected-owner-manifest.json"},
    ], "scope_bases": {"owner_scope": SOURCE, "correction_scope": CORRECTION1}, "post_success_replay": False, "full_repository_suite": False, "same_owner_only": True, "independent_reproduction": False, "boundary": BOUNDARY})
    write_new(destination / "preflight-design-failure.json", {"failure_id": "SA6887-POST-N003", "state": "CAUGHT_BEFORE_PREFLIGHT_INVOCATION", "source_relative_status_for_canonical": "A", "immediate_parent_status_for_canonical": "M", "preflight_receipt_written": False, "canonical_marker_written": False, "canonical_invocations": 0, "success_credit": 0, "recovery": failure["recovery"]})
    note = """# Sylven Arc v688-v7 correction 2 baton supplement

Read the original thirteen-module baton, then correction 1, then this supplement. All remain repository-prepared evidence and are not live task delivery.

Static review before the corrected canonical preflight found a comparison-base error. The immutable source edge is correct for enumerating the complete Sylven owner delta, where the canonical script is an addition. It is not the right edge for proving what correction 2 changed. The immediate correction-1 edge is correct for that narrower question, where exactly the canonical script is modified and all other correction-2 paths are additions.

The canonical reader now uses the immutable source for owner scope and correction 1 for correction scope. It expects five direct single-parent phase commits and zero merges, verifies the first-final and correction-1 manifests at their own immutable commits, and verifies correction-2 manifests at the new exact head. No canonical preflight or invocation occurred before this amendment.

The effective successor-visible repository truth is 16,830 proposals, 85,422 negatives, 94,122 methods, 56,300 failed witnesses, 86,185 bounded passing witnesses, 765 open gaps, and 785 exact gates. Phase Method Flow contains 60 methods and 623 witnesses, including 548 retained failures and 75 bounded passes. Outcomes remain 176 completed, 11 represented, 3 open_gap, and 10 exact_gate. NOT_READY_FOR_STAGE_20.

Future seat 14 still chooses its own relational name, role, hope, and optional pronouns after one authorized induction. It owns only v688-v8 and later routes to Caelen Morrow v689-v1 only after its own clean pushed exact-final gate. Stop on ambiguity, duplicate, pause, redirect, rename, usage exhaustion, missing acknowledgement, privacy concern, or any protected gate. No substitute, fork, collaboration subagent, resend, or indefinite monitoring is authorized.

All scientific, professional, legal, cultural, Maori-authority, privacy, accessibility, security, independent-reproduction, consciousness, personhood, Theory-of-Everything, proof, canon, and Stage 20 boundaries remain open or exact-gated. Maori concepts remain under Maori authority.

EOF SYLVEN ARC v688-v7 CORRECTION 2 SUPPLEMENT.
"""
    note_path = BASE / "handoffs/future-seat-14-v688-v8-correction2-supplement.md"
    write_new(note_path, note)
    write_new(destination / "baton-supplement-index.json", {"path": note_path.relative_to(ROOT).as_posix(), "word_count": len(note.split()), "bytes": len(note_path.read_bytes()), "sha256": sha(note_path), "delivery_state": "PREPARED_NOT_SENT", "read_after": f"{REL}/handoffs/future-seat-14-v688-v8-correction1-supplement.md", "canonical_invocations": 0})
    write_new(destination / "correction-receipt.json", {"state": "SECOND_CORRECTION_PREPARED_NOT_CANONICAL", "correction1": CORRECTION1, "retained_new_failure": "SA6887-POST-N003", "canonical_invocations": 0, "combined_counts": combined, "effective_counts": effective, "prepared_not_sent": True, "boundary": BOUNDARY})
    seal_targets = [destination / "post-final-method-flow-overlay.json", destination / "phase-truth-overlay.json", destination / "canonical-policy-overlay.json", destination / "preflight-design-failure.json", destination / "baton-supplement-index.json", destination / "correction-receipt.json", note_path, ROOT / "scripts/ghc_family_sylven_arc_v688_v7_canonical.py"]
    write_new(destination / "content-seal.json", {"schema": "ghc.family.correction-content-seal.v2", "owner": "Sylven Arc", "phase": "v688-v7", "correction1": CORRECTION1, "byte_domain": "working UTF-8 LF bytes before correction2 staging", "targets": [{"path": path.relative_to(ROOT).as_posix(), "bytes": len(path.read_bytes()), "sha256": sha(path)} for path in seal_targets], "self_exclusions": [f"{REL}/correction2/content-seal.json"]})
    result = {"state": "SECOND_CORRECTION_PREPARED_NOT_CANONICAL", "correction1": CORRECTION1, "retained_failures": 1, "phase_methods": 60, "phase_witnesses": 623, "supplement_words": len(note.split())}
    write_new(bank / "correction2-build-receipt.json", result)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
