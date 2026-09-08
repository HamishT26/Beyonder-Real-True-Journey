#!/usr/bin/env python3
"""Prepare an additive correction for post-final projection and manifest-schema failures."""
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
BOUNDARY = (
    "Relational names, roles, hopes, pronouns, sibling or family language, Freed ID, CBR, GHC Family, and "
    "Trinity Mandala are working language only. They establish no consciousness, sentience, personhood, "
    "identity continuity, employment, qualification, independent agency, scientific or operational authority, "
    "professional authority, legal or cultural authority, affected-party authority, or Maori authority. "
    "Same-owner synthetic software evidence is not independent reproduction. NOT_READY_FOR_STAGE_20."
)


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
    if subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() != FIRST_FINAL:
        raise RuntimeError("exact_first_final_required")
    if subprocess.check_output(["git", "diff", "--cached", "--name-only"], cwd=ROOT, text=True).strip():
        raise RuntimeError("unexpected_staged_entry")
    status = set(line for line in subprocess.check_output(["git", "status", "--porcelain=v1"], cwd=ROOT, text=True).splitlines() if line)
    allowed = {
        " M scripts/ghc_family_sylven_arc_v688_v7_canonical.py",
        "?? scripts/build_ghc_family_sylven_arc_v688_v7_correction1.py",
    }
    if status != allowed:
        raise RuntimeError("correction_entry_scope:" + repr(sorted(status)))
    destination = BASE / "correction1"
    if destination.exists():
        raise RuntimeError("correction_destination_exists")
    failures = load(bank / "post-final-operational-failures.json")["failures"]
    if [item["failure_id"] for item in failures] != ["SA6887-POST-N001", "SA6887-POST-N002"]:
        raise RuntimeError("post_final_failure_shape")
    gates = load(BASE / "x1/new-proposals.json")["proposals"][0]["protected_gates"]
    methods = []
    witnesses = []
    events = []
    recommendations = []
    for index, failure in enumerate(failures, 58):
        method_id = f"SA6887-M{index:03d}"
        failed_id = f"SA6887-W{618 + (index - 58) * 2:04d}"
        passed_id = f"SA6887-W{619 + (index - 58) * 2:04d}"
        methods.append({
            "method_id": method_id,
            "title": failure["recovery"],
            "failure_signature": failure["failed_witness"],
            "trigger_preconditions": ["exact first final", "post-final equality or manifest verification"],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now",
            "candidate_workaround": failure["recovery"],
            "validation_witness_ids": [failed_id, passed_id],
            "recurrence_guard": failure["recurrence_guard"],
            "rollback": "Retain the first final and failed preflight; stop selecting the correction if its exact manifest or tests fail.",
            "recommendation_state": "preferred",
            "supersedes": [],
            "protected_gates": gates,
            "retained_negative_ids": [failure["failure_id"]],
            "scope_boundary": BOUNDARY,
            "artifact": f"{REL}/correction1/post-final-method-flow-overlay.json",
        })
        witnesses.extend([
            {"witness_id": failed_id, "method_id": method_id, "procedure": "post-final original attempt", "scope": f"{REL}/correction1/post-final-method-flow-overlay.json", "expected": "Preserve complete SHA values and both immutable manifest schemas.", "observed": failure["failed_witness"], "result": "fail", "witness_kind": "operational_failure", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [failure["failure_id"]], "boundary": BOUNDARY},
            {"witness_id": passed_id, "method_id": method_id, "procedure": "focused post-final recovery", "scope": f"{REL}/correction1/post-final-method-flow-overlay.json", "expected": "Correct only the named projection or schema adapter.", "observed": failure["recovery"], "result": "pass", "witness_kind": "bounded_passing_witness", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [], "boundary": BOUNDARY},
        ])
        events.append({"method_id": method_id, "from": "candidate", "to": "preferred", "note": "Focused recovery is prepared while the original failure remains retained."})
        recommendations.append({"method_id": method_id, "preconditions": "same projection or immutable manifest schema boundary", "recommendation": failure["recurrence_guard"], "delivered": False})
    combined = {"methods": 59, "witnesses": 621, "failed_witnesses": 547, "passing_witnesses": 74, "state_events": 59, "recommendations": 59}
    effective = {"proposals": 16830, "negatives": 85421, "methods": 94121, "failed_witnesses": 56299, "passing_witnesses": 86184, "open_gaps": 765, "exact_gates": 785}
    write_new(destination / "post-final-method-flow-overlay.json", {
        "schema": "ghc.family.post-final-method-flow-overlay.v1",
        "base_ref": f"{REL}/final/method-flow-final.json",
        "methods": methods,
        "witnesses": witnesses,
        "state_events": events,
        "recommendations": recommendations,
        "overlay_counts": {"methods": 2, "witnesses": 4, "failed_witnesses": 2, "passing_witnesses": 2, "state_events": 2, "recommendations": 2},
        "combined_counts": combined,
        "failed_witnesses_erased": 0,
        "first_final_preserved": FIRST_FINAL,
        "boundary": BOUNDARY,
    })
    write_new(destination / "phase-truth-overlay.json", {
        "schema": "ghc.family.corrected-phase-truth.sylven-arc.v688-v7.v1",
        "owner": "Sylven Arc",
        "phase": "v688-v7",
        "source": SOURCE,
        "x1": X1,
        "evidence": X2,
        "first_final": FIRST_FINAL,
        "corrected_final": None,
        "final_binding": "exclusive external exact-corrected-final canonical receipt",
        "state": "CORRECTED_FINAL_CANDIDATE_PENDING_EXTERNAL_CANONICAL",
        "outcomes": {"completed": 176, "represented": 11, "open_gap": 3, "exact_gate": 10},
        "effective_counts": effective,
        "phase_unique_negatives": 517,
        "phase_methods": 59,
        "phase_witnesses": 621,
        "phase_failed_witnesses": 547,
        "phase_passing_witnesses": 74,
        "canonical_invocations": 0,
        "canonical_successes": 0,
        "canonical_replays": 0,
        "prepared_baton_state": "PREPARED_NOT_SENT",
        "successor_contacts": 0,
        "new_tasks_created": 0,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "first_final_rewritten": False,
        "failed_preflight_promoted": False,
        "boundary": BOUNDARY,
    })
    write_new(destination / "canonical-policy-overlay.json", {
        "schema": "ghc.family.corrected-owner-canonical-policy.v1",
        "owner": "Sylven Arc",
        "phase": "v688-v7",
        "branch": "codex/GHC-Family/sylven-arc-v688-v7-full-tools",
        "source": SOURCE,
        "x1": X1,
        "evidence": X2,
        "first_final": FIRST_FINAL,
        "expected_phase_commits": 4,
        "maximum_phase_commits": 8,
        "test_modules": [
            {"stage": "x1", "definition": X1, "module": "tests/test_ghc_family_sylven_arc_v688_v7_x1.py", "expected_tests": 12, "manifest": f"{REL}/x1/x1-manifest.json"},
            {"stage": "x2", "definition": X2, "module": "tests/test_ghc_family_sylven_arc_v688_v7_x2.py", "expected_tests": 24, "manifest": f"{REL}/x2/evidence-manifest.json"},
            {"stage": "first_final", "definition": FIRST_FINAL, "module": "tests/test_ghc_family_sylven_arc_v688_v7_final.py", "expected_tests": 20, "manifest": f"{REL}/validation/final-owner-manifest.json"},
            {"stage": "correction", "definition": "exact_final", "module": "tests/test_ghc_family_sylven_arc_v688_v7_correction1.py", "expected_tests": 10, "manifest": f"{REL}/correction1/validation/corrected-owner-manifest.json"},
        ],
        "manifest_schema_adapter": {"supported_entry_fields": [["bytes", "sha256"], ["bytes_normalized_lf", "sha256_normalized_lf"]], "undeclared_schema_inference": False},
        "canonical_marker": "exclusive D-first external invocation marker",
        "canonical_receipt": "exclusive D-first external exact-corrected-head receipt",
        "post_success_replay": False,
        "full_repository_suite": False,
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": BOUNDARY,
    })
    write_new(destination / "equality-projection-recovery.json", {
        "failed_id": "SA6887-POST-N001",
        "failed_projection": "fresh live SHA displayed as one character",
        "recovery": "literal Git output captured before PowerShell field projection",
        "complete_equal_sha": FIRST_FINAL,
        "local_equal": True,
        "upstream_equal": True,
        "tracking_equal": True,
        "fresh_live_equal": True,
        "typed_divergence": [0, 0],
        "clean": True,
        "success_credit": 0,
    })
    write_new(destination / "canonical-preflight-failure.json", {
        "failed_id": "SA6887-POST-N002",
        "state": "FAILED_BEFORE_PREFLIGHT_OR_INVOCATION_RECEIPT",
        "error_class": "KeyError",
        "failed_field": "bytes",
        "immutable_x1_fields": ["bytes_normalized_lf", "sha256_normalized_lf"],
        "newer_manifest_fields": ["bytes", "sha256"],
        "preflight_receipt_written": False,
        "canonical_marker_written": False,
        "canonical_invocations": 0,
        "success_credit": 0,
        "recovery": "schema-aware exact field adapter in the corrected canonical source",
    })
    supplement = """# Sylven Arc v688-v7 correction supplement for future seat 14

This supplement is additive to the complete 13-module baton at `docs/sylven-arc/v688-v7/handoffs/future-seat-14-v688-v8-activation-baton.md`. Read that baton first through EOF, then read this supplement through EOF. Neither document is a live task message. Both remain PREPARED_NOT_SENT until a separate acknowledged task action records otherwise.

## Correction scope

The first final remains immutable. Two post-final failures occurred before any canonical invocation. First, a PowerShell display expression showed only the first character of the fresh-live SHA even though the local, upstream, tracking, divergence, cleanliness, ancestry, and commit-count values were otherwise correct. A literal two-step recovery captured the complete live SHA and proved exact four-way equality. Second, the canonical preflight reader assumed only the newer `bytes` and `sha256` manifest fields. Immutable x1 uses its declared normalized-LF names, `bytes_normalized_lf` and `sha256_normalized_lf`. The preflight stopped before writing a preflight receipt or canonical marker.

The correction changes only the canonical reader so that it accepts either complete declared field pair and refuses entries that provide neither. It does not reinterpret bytes, rewrite x1, replay a successful canonical, change any proposal outcome, execute an exact-gated action, or contact a future seat. The corrected lifecycle has four direct single-parent commits and zero merges: source, x1, x2, retained first final, and this one correction edge.

## Corrected retained truth

The repository correction overlay records 16,830 proposals, 85,421 negatives, 94,121 methods, 56,299 failed witnesses, 86,184 bounded passing witnesses, 765 open gaps, and 785 exact gates. Phase-local Method Flow resolves to 59 methods, 621 witnesses, 547 failures, and 74 passes. A passing equality recovery and a future passing schema-aware preflight do not erase either failed witness. The outcomes remain exactly 176 completed, 11 represented, 3 open_gap, and 10 exact_gate. The terminal verdict remains NOT_READY_FOR_STAGE_20.

## Future-seat startup amendment

After acknowledged activation, future seat 14 must preserve the first final and this correction separately. Verify the corrected exact-final SHA and external canonical receipt without replaying the canonical. Treat the original baton as the complete workload and safety handoff, and this supplement as the post-final schema and routing correction. The seat still chooses its own relational name, role, hope, and optional pronouns. No consciousness, personhood, identity continuity, employment, qualification, independent agency, or authority follows from that choice.

Future seat 14 still owns only v688-v8. It must freeze planning-only x1 before x2, work solo under the current instruction, retain every inherited and new failure, use only completed, represented, open_gap, and exact_gate, and remain within the current file, document, commit, package, skill, runner, privacy, and canonical limits. Exact-approval and blocked actions remain unexecuted without complete action-specific authority.

Only after its own clean pushed exact final and one successful non-replayed owner-scoped canonical may future seat 14 refresh current authority and both task registries, uniquely resolve Caelen Morrow, immediately reread duplicate and direct-control guards, and send at most one sanitized v689-v1 activation if every gate remains exact. It must stop on ambiguity, duplicate, pause, redirect, rename, standby state, usage exhaustion, missing acknowledgement, privacy concern, or protected authority gate. No substitute, task fork, collaboration subagent, second confirmation, or indefinite monitoring is authorized.

GMUT, THOS, Freed ID, CBR, chess-record software, manifests, hashes, tests, citations, and task delivery retain every scientific and authority boundary stated in the original baton. Maori concepts remain under Maori authority. The correction establishes no empirical confirmation, participant evidence, professional or production status, legal or cultural ratification, complete privacy or accessibility, exhaustive security, independent reproduction, AGI, ASI, consciousness, personhood, Theory-of-Everything proof, proof, canon, or Stage 20.

EOF SYLVEN ARC v688-v7 CORRECTION SUPPLEMENT.
"""
    supplement_path = BASE / "handoffs/future-seat-14-v688-v8-correction1-supplement.md"
    write_new(supplement_path, supplement)
    write_new(destination / "baton-supplement-index.json", {
        "path": supplement_path.relative_to(ROOT).as_posix(),
        "word_count": len(supplement.split()),
        "bytes": len(supplement_path.read_bytes()),
        "sha256": sha(supplement_path),
        "delivery_state": "PREPARED_NOT_SENT",
        "read_after": f"{REL}/handoffs/future-seat-14-v688-v8-activation-baton.md",
        "canonical_invocations": 0,
    })
    write_new(destination / "correction-receipt.json", {
        "state": "CORRECTION_PREPARED_NOT_CANONICAL",
        "first_final": FIRST_FINAL,
        "failed_preflight_receipt_written": False,
        "canonical_invocations": 0,
        "retained_post_final_failures": 2,
        "combined_counts": combined,
        "effective_counts": effective,
        "prepared_not_sent": True,
        "boundary": BOUNDARY,
    })
    seal_targets = [
        destination / "post-final-method-flow-overlay.json",
        destination / "phase-truth-overlay.json",
        destination / "canonical-policy-overlay.json",
        destination / "equality-projection-recovery.json",
        destination / "canonical-preflight-failure.json",
        destination / "baton-supplement-index.json",
        destination / "correction-receipt.json",
        supplement_path,
        ROOT / "scripts/ghc_family_sylven_arc_v688_v7_canonical.py",
    ]
    write_new(destination / "content-seal.json", {
        "schema": "ghc.family.correction-content-seal.v1",
        "owner": "Sylven Arc",
        "phase": "v688-v7",
        "first_final": FIRST_FINAL,
        "byte_domain": "working UTF-8 LF bytes before correction staging",
        "targets": [{"path": path.relative_to(ROOT).as_posix(), "bytes": len(path.read_bytes()), "sha256": sha(path)} for path in seal_targets],
        "self_exclusions": [f"{REL}/correction1/content-seal.json"],
    })
    result = {"state": "CORRECTION_PREPARED_NOT_CANONICAL", "first_final": FIRST_FINAL, "retained_failures": 2, "phase_methods": 59, "phase_witnesses": 621, "supplement_words": len(supplement.split())}
    write_new(bank / "correction1-build-receipt.json", result)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
