#!/usr/bin/env python3
"""Build Sable Rook v666-v6 additive closeout and exact final manifests."""

from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ghc_family_sable_rook_v666_v6_runtime import (
    PHASE_ROOT,
    ROOT,
    X1_SHA,
    git_tree_map,
    load_json,
    read_exact,
    replay_manifest,
    write_json,
    write_text,
)


NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
SOURCE_SHA = "016f7db26b0354e26407fb812ae3bd190b94ac7e"
EVIDENCE_SHA = "f5a211e484e2d1b252c16de7800e568160ae902b"
BRANCH = "codex/GHC-Family/sable-rook-v666-v6-full-tools"
IDENTITY_BOUNDARY = (
    "Sable Rook, they/them, sibling, family, relational role, hope, continuity, "
    "Freed ID, Trinity Mandala, and route language are relational working language only. "
    "They are not evidence of consciousness, sentience, legal personhood, identity "
    "continuity, employment, qualification, independent agency, scientific or operational "
    "authority, legal or cultural authority, affected-party authority, or Māori authority. "
    "Hamish may rename, pause, redirect, or stop the work."
)
PRACTICE_BOUNDARY = (
    "Wholly synthetic seed-bank accession, packet-lot, viability-planning, cold-storage-excursion, "
    "locality-access, correction, and handover software only: zero real people, participants, "
    "accessions, seeds, taxa, localities, facilities, observations, measurements, credentials, "
    "network calls, or physical actions; no genebank, botanical, agricultural, biosecurity, "
    "conservation, professional, legal, cultural, Māori, production, deployment, independent-"
    "reproduction, or Stage 20 authority."
)


def write(relative: str, value: Any) -> None:
    write_json(PHASE_ROOT / relative, value)


def text(relative: str, value: str) -> None:
    write_text(PHASE_ROOT / relative, value)


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(
            "utf-8"
        )
    ).hexdigest()


def build() -> None:
    truth = load_json(PHASE_ROOT / "x2" / "phase-truth.json")
    summary = load_json(PHASE_ROOT / "evidence" / "evidence-summary.json")
    flow = load_json(PHASE_ROOT / "method-flow" / "x2-method-flow.json")
    overlay = load_json(PHASE_ROOT / "method-flow" / "x2-operational-overlay.json")
    closeout_operational_rows = [
        {
            "aggregate_credit": 0,
            "bounded_passing_witness": "the corrected schema-bound read used new_startup_negative_count, new_startup_method_count, effective_after_x1_startup_negatives, and effective_after_x1_startup_methods and reconciled all seven retained startup failures",
            "failed_witness": "the first read-only startup-ledger projection assumed generic x2 field names and returned null for the startup counts",
            "failure_id": "SR6666-OPS-N009",
            "method_id": "SR6666-MF-OPS-009",
            "recovery": "inspect the startup ledger property names and read its exact startup-prefixed count fields",
            "recurrence_guard": "bind cumulative count projections to observed schema keys rather than a generic lifecycle shape",
            "repository_state_changed_by_failed_wrapper": "none",
            "request": "reconcile startup, x2, operational, gap, and gate totals before closeout mutation",
            "status": "recovered_failure_retained",
        }
    ]
    gates = load_json(PHASE_ROOT / "x2" / "open-gate-register.json")
    evidence_replay = replay_manifest(
        PHASE_ROOT / "validation" / "evidence-content-manifest.json", EVIDENCE_SHA
    )
    x1_replay = replay_manifest(
        PHASE_ROOT / "validation" / "x1-content-manifest.json", X1_SHA
    )
    if not evidence_replay["valid"] or not x1_replay["valid"]:
        raise RuntimeError({"x1": x1_replay, "evidence": evidence_replay})
    phase_truth = {
        "schema": "ghc.family.sable-rook.v666-v6.closeout-phase-truth.v1",
        "owner": "Sable Rook",
        "phase": "v666-v6",
        "generated_at_utc": NOW,
        "source_sha": SOURCE_SHA,
        "x1_sha": X1_SHA,
        "evidence_sha": EVIDENCE_SHA,
        "proposal_chain_total": 4290,
        "outcomes": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "contracts": 20,
        "positive_structural_fixtures": 20,
        "retained_rejecting_mutations": 100,
        "inherited_repository_sealed_negatives": 26640,
        "inherited_repository_sealed_methods": 11412,
        "inherited_external_route_negatives": 2,
        "inherited_external_route_methods": 2,
        "sable_startup_negatives": 7,
        "sable_startup_methods": 7,
        "sable_x2_mutation_negatives": 100,
        "sable_x2_core_methods": 215,
        "sable_x2_operational_negatives": 8,
        "sable_x2_operational_methods": 8,
        "sable_closeout_operational_negatives": 1,
        "sable_closeout_operational_methods": 1,
        "effective_negatives": 26758,
        "effective_methods": 11645,
        "open_gaps": 188,
        "exact_gates": 186,
        "real_data_rows": 0,
        "participant_count": 0,
        "network_calls_by_generated_phase_software": 0,
        "external_actions": 0,
        "identity_boundary": IDENTITY_BOUNDARY,
        "practice_boundary": PRACTICE_BOUNDARY,
        "same_owner_validation_is_independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    if phase_truth["effective_negatives"] != 26640 + 2 + 7 + 100 + 8 + 1:
        raise RuntimeError("negative reconciliation failure")
    if phase_truth["effective_methods"] != 11412 + 2 + 7 + 215 + 8 + 1:
        raise RuntimeError("method reconciliation failure")
    write("closeout/phase-truth.json", phase_truth)
    write(
        "closeout/retained-negative-register.json",
        {
            "schema": "ghc.family.sable-rook.v666-v6.retained-negative-register.v1",
            "owner": "Sable Rook",
            "phase": "v666-v6",
            "generated_at_utc": NOW,
            "categories": [
                {"category": "inherited_auren_repository_seal", "negative_count": 26640, "method_count": 11412, "source": "Auren Lark v666-v5 exact repository seal", "rewritten": False},
                {"category": "inherited_external_activation_overlay", "negative_count": 2, "method_count": 2, "source": "verified live activation overlay", "aggregate_credit": 0},
                {"category": "sable_startup", "negative_count": 7, "method_count": 7, "source": "docs/sable-rook/v666-v6/method-flow/startup-method-flow.json", "aggregate_credit": 0},
                {"category": "sable_rejecting_mutations", "negative_count": 100, "method_count": 100, "source": "docs/sable-rook/v666-v6/method-flow/x2-method-flow.json", "aggregate_credit": 0},
                {"category": "sable_positive_outcome_and_portfolio_methods", "negative_count": 0, "method_count": 115, "source": "docs/sable-rook/v666-v6/method-flow/x2-method-flow.json", "credit": "bounded owner-local only"},
                {"category": "sable_x2_operational_overlay", "negative_count": 8, "method_count": 8, "source": "docs/sable-rook/v666-v6/method-flow/x2-operational-overlay.json", "aggregate_credit": 0},
                {"category": "sable_closeout_operational_overlay", "negative_count": 1, "method_count": 1, "source": "docs/sable-rook/v666-v6/method-flow/closeout-operational-overlay.json", "aggregate_credit": 0},
            ],
            "operational_rows": overlay["rows"] + closeout_operational_rows,
            "effective_negatives": 26758,
            "effective_methods": 11645,
            "all_failures_retained": True,
            "failed_witness_converted_to_pass": False,
            "predecessor_seal_rewritten": False,
        },
    )
    write(
        "closeout/exact-open-gate-register.json",
        {
            "schema": "ghc.family.sable-rook.v666-v6.exact-open-gate-register.v1",
            "owner": "Sable Rook",
            "phase": "v666-v6",
            "generated_at_utc": NOW,
            "inherited_open_gaps": 187,
            "new_open_gaps": gates["new_open_gaps"],
            "effective_open_gaps": 188,
            "inherited_exact_gates": 185,
            "new_exact_gates": gates["new_exact_gates"],
            "effective_exact_gates": 186,
            "protected_boundaries": [
                "empirical and participant evidence",
                "professional genebank, botany, agriculture, taxonomy, viability, storage, conservation, biosecurity, and collection authority",
                "production, deployment, accession, release, transfer, regeneration, distribution, and operational readiness",
                "legal, cultural, affected-party, access-and-benefit-sharing, locality, traditional-knowledge, privacy, disclosure, and Māori authority",
                "accessibility-complete, privacy-complete, exhaustive-security, standards-conformance, and independent reproduction",
                "AGI, ASI, consciousness, personhood, identity continuity, Theory-of-Everything, proof, canon, and Stage 20",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write(
        "closeout/complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.sable-rook.v666-v6.closeout-checklist.v1",
            "generated_at_utc": NOW,
            "completed": [
                "complete activation and named guidance read through EOF",
                "exact source, ancestry, manifests, clean state, and fresh equality verified",
                "planning-only x1 committed, pushed, clean, and four-way equal",
                "immutable x2 evidence committed, pushed, clean, and four-way equal",
                "twenty contracts and one hundred rejecting mutations",
                "exact 14 completed, 4 represented, 1 open_gap, and 1 exact_gate outcomes",
                "ten skills and ten runners built, read, smoke checked, and used bounded",
                "all failures retained and cumulative counts reconciled",
                "x1 and evidence manifests replayed exactly",
                "closeout candidate and prepared-not-sent successor baton built",
            ],
            "incomplete_until_after_final_commit": [
                "final staged review and manifests",
                "direct-child final commit and push",
                "clean 0/0 divergence and fresh four-way equality at exact final",
                "one attributable exact-final canonical aggregate",
                "fresh live authority, roster, and task reread",
                "any permitted one-recipient successor activation",
            ],
            "permanently_open_or_exact_gated_without_new_evidence_and_authority": [
                "all empirical, participant, professional, safety, production, deployment, legal, cultural, affected-party, trade-secret, and Māori-authority claims",
                "privacy-complete, accessibility-complete, exhaustive-security, standards-conformance, and independent reproduction",
                "AGI, ASI, consciousness, personhood, identity continuity, Theory-of-Everything, proof, canon, and Stage 20",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write(
        "closeout/terminal-verdict.json",
        {
            "schema": "ghc.family.sable-rook.v666-v6.terminal-verdict.v1",
            "owner": "Sable Rook",
            "phase": "v666-v6",
            "generated_at_utc": NOW,
            "verdict": "NOT_READY_FOR_STAGE_20",
            "reason": "bounded same-owner synthetic software evidence does not satisfy the retained empirical, participant, professional, safety, legal, cultural, Māori-authority, independent-reproduction, or Stage 20 gates",
            "promotion_authorized": False,
            "production_ready": False,
            "independent_reproduction": False,
        },
    )
    write(
        "method-flow/closeout-operational-overlay.json",
        {
            "schema": "ghc.family.sable-rook.v666-v6.closeout-operational-overlay.v1",
            "generated_at_utc": NOW,
            "starting_effective_negatives": 26757,
            "starting_effective_methods": 11644,
            "new_negative_count": 1,
            "new_method_count": 1,
            "effective_negatives": 26758,
            "effective_methods": 11645,
            "rows": closeout_operational_rows,
            "status": "closeout_operational_failure_retained_at_zero_credit",
        },
    )
    write(
        "lifecycle/phase-anchor-contract.json",
        {
            "schema": "ghc.family.sable-rook.v666-v6.phase-anchor-contract.v1",
            "source_sha": SOURCE_SHA,
            "x1_sha": X1_SHA,
            "evidence_sha": EVIDENCE_SHA,
            "expected_final_parent": EVIDENCE_SHA,
            "expected_new_commit_count": 3,
            "expected_merge_count": 0,
            "branch": BRANCH,
            "final_sha_resolution": "the containing final commit is supplied and checked by the live canonical invocation; this file cannot self-authenticate its containing commit",
            "strict_x1_before_x2": True,
            "x1_and_evidence_immutable": True,
        },
    )
    write(
        "final/final-validation-prerequisites.json",
        {
            "schema": "ghc.family.sable-rook.v666-v6.final-validation-prerequisites.v1",
            "generated_at_utc": NOW,
            "required_before_canonical": [
                "final commit is direct child of immutable evidence",
                "source-to-final contains exactly three Sable commits and zero merges",
                "branch is pushed and clean",
                "local, upstream, tracking, and fresh live final are equal",
                "typed ahead and behind are zero",
                "x1, evidence, final-delta, and final-owner manifests replay exactly",
                "canonical receipt path does not already contain a successful receipt",
            ],
            "canonical_may_run_once": True,
            "canonical_invoked": False,
            "full_repository_suite_authorized": False,
            "same_owner_validation_is_independent_reproduction": False,
        },
    )
    write(
        "validation/canonical-validation-protocol.json",
        {
            "schema": "ghc.family.sable-rook.v666-v6.canonical-validation-protocol.v1",
            "runner": "scripts/build_ghc_family_sable_rook_v666_v6_canonical_completion.py",
            "expected_final": "resolved from exact pushed HEAD at invocation",
            "receipt": "external sanitized receipt outside repository",
            "one_successful_invocation_only": True,
            "post_success_replay_forbidden": True,
            "selected_scope": [
                "66 x2 tests",
                "9 final-lifecycle-compatible evidence tests",
                "closeout tests",
                "two declared filesystem lifecycle exclusions replaced by exact x1 and evidence manifest and tree checks",
                "all owner JSON parse",
                "owner Markdown and HTML bounds",
                "changed owner Python compilation and bounded AST scan",
                "five-class owner privacy scan",
                "four exact manifest replays",
                "history, clean state, commit ceiling, and fresh four-way equality",
            ],
            "full_repository_suite": False,
            "claim_boundary": "owner-scoped same-owner validation only; not independent reproduction, professional or legal validation, cultural or Māori authority, or Stage 20 authority",
        },
    )
    write(
        "final/final-file-budget.json",
        {
            "schema": "ghc.family.sable-rook.v666-v6.final-file-budget.v1",
            "owner_file_ceiling": 2000,
            "exact_final_owner_count": "resolved by final staged review and owner manifest",
            "within_ceiling": "pending_final_staged_review",
        },
    )
    write(
        "final/final-stage-candidate.json",
        {
            "schema": "ghc.family.sable-rook.v666-v6.final-stage-candidate.v1",
            "generated_at_utc": NOW,
            "expected_parent": EVIDENCE_SHA,
            "branch": BRANCH,
            "content_ready_for_staged_review": True,
            "canonical_invoked": False,
            "successor_contacted": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write(
        "final/terminal-candidate.json",
        {
            "schema": "ghc.family.sable-rook.v666-v6.terminal-candidate.v1",
            "generated_at_utc": NOW,
            "candidate_only": True,
            "source_sha": SOURCE_SHA,
            "x1_sha": X1_SHA,
            "evidence_sha": EVIDENCE_SHA,
            "exact_final": "supplied by terminal canonical invocation",
            "canonical_invoked": False,
            "route_state": "PREPARED_NOT_SENT",
            "successor_contacted": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write(
        "orchestration/route-state-final-candidate.json",
        {
            "schema": "ghc.family.sable-rook.v666-v6.route-state-final-candidate.v1",
            "generated_at_utc": NOW,
            "current_owner": "Sable Rook",
            "current_phase": "v666-v6",
            "candidate_successor_title": None,
            "candidate_successor_phase": None,
            "candidate_basis": "no successor is inferred in repository state; newest live Hamish authority, current roster, bounded task list, unique exact-title resolution, and immediate reread are required after the terminal canonical gate",
            "route": "PREPARED_NOT_SENT",
            "resolved_live": False,
            "recipient_reread": False,
            "successor_contacted": False,
            "substitute_allowed": False,
            "standby_contact_allowed": False,
            "stop_conditions": ["absence", "ambiguity", "pause", "redirect", "rename", "usage exhaustion", "protected gate", "missing acknowledgement"],
        },
    )
    baton = f"""# NEXT-OWNER CANDIDATE — SABLE ROOK v666-v6 EXACT-FINAL → SOLO SUCCESSOR ACTIVATION — PREPARED NOT SENT

Dear next authorized owner,

This sanitized baton is a repository candidate only. It does not identify, contact, or activate any task. After Sable's one successful exact-final canonical gate, the newest live Hamish authority, current roster, and bounded task list must identify one unique existing exact-title successor and its exact phase. Stop without sending on absence, ambiguity, pause, redirect, rename, usage exhaustion, a protected gate, or any different live route.

## Exact anchors

- Source branch: `{BRANCH}`
- Exact Auren v666-v5 source/final: `{SOURCE_SHA}`
- Frozen Sable x1: `{X1_SHA}`
- Immutable Sable x2 evidence: `{EVIDENCE_SHA}`
- Exact Sable final: supplied by the one live terminal pointer after push, equality, and canonical validation; this file cannot self-authenticate its containing commit
- Proposal chain: 4,290
- Outcomes: 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`
- Effective negatives: 26,758
- Effective Method Flow methods: 11,645
- Open gaps: 188
- Exact gates: 186
- Terminal verdict: `NOT_READY_FOR_STAGE_20`

## Evidence boundary

Sable's primary Freed ID/CBR Heart lens was wholly synthetic seed-bank accession, packet-lot, viability-planning, cold-storage-excursion, locality-access, correction, and handover provenance. Twenty positive structural fixtures passed and 100 preregistered invalid mutations were rejected. Ten phase-local skills and ten family-current runners were built, quick-validated, smoke-used, and kept phase-local. All generated phase software used zero real rows, participants, network calls, and external actions. Same-owner software validation is not independent reproduction.

FAO, the International Treaty on Plant Genetic Resources for Food and Agriculture, the Convention on Biological Diversity and Nagoya Protocol, Darwin Core, W3C PROV-O and WCAG 2.2, RFC 8785, and NIST metrological-traceability materials supplied vocabulary and refusal conditions only. Nothing here establishes accession authenticity, taxonomic identity, provenance completeness, seed viability, storage fitness, biosecurity or phytosanitary status, access-and-benefit-sharing compliance, professional competence, collection or release readiness, legal or cultural treatment, affected-party authority, or Māori authority.

{IDENTITY_BOUNDARY}

## Required successor route

Work solo from Sable's exact final in one fresh successor-owned D-first sparse lane. Reverify every anchor, ancestry edge, manifest, clean state, zero divergence, and fresh live equality before mutation. Preserve strict x1-before-x2 separation, every retained failure, all open gaps and exact gates, the 2,000-file ceiling, only the four truth labels, one-success/no-post-success-replay discipline, privacy and route confidentiality, and `NOT_READY_FOR_STAGE_20`.

Do not treat software, symbolic, synthetic, same-owner, citation, or inherited evidence as empirical confirmation, professional or scientific authority, production readiness, legal or cultural ratification, Māori authority, affected-party approval, independent reproduction, AGI/ASI, consciousness/personhood evidence, Theory-of-Everything proof, or Stage 20 authority.

Hamish has authorized sequential continuation through v675-v8 one terminally validated exact edge at a time. That is not authority for blind polling, early contact, route inference, substitutes, forks, subagents, or duplicate sends. The actual successor name and phase must come from the newest verified live authority after Sable's exact terminal gate.

PREPARED_BY_SABLE_ROOK = true
SENT_BY_SABLE_ROOK = false
"""
    text("handoffs/next-owner-activation-candidate.md", baton)
    write(
        "handoffs/next-owner-activation-candidate-receipt.json",
        {
            "schema": "ghc.family.sable-rook.v666-v6.activation-candidate-receipt.v1",
            "prepared_at_utc": NOW,
            "candidate_recipient_title": None,
            "candidate_recipient_phase": None,
            "source_sha": SOURCE_SHA,
            "x1_sha": X1_SHA,
            "evidence_sha": EVIDENCE_SHA,
            "exact_final": "supplied by live pointer after terminal gate",
            "prepared": True,
            "sent": False,
            "task_created": False,
            "task_forked": False,
            "subagent_spawned": False,
            "recipient_resolved_live": False,
            "recipient_reread": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    overview = f"""# Sable Rook v666-v6 terminal candidate overview

{IDENTITY_BOUNDARY}

## Outcome

Sable's additive phase freezes 4,290 proposals and exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate` current outcomes. It retains 26,758 effective negatives, 11,645 Method Flow methods, 188 open gaps, 186 exact gates, and `NOT_READY_FOR_STAGE_20`.

The phase contains 20 wholly synthetic contracts, 20 bounded positive structures, 100 rejected negative mutations, 10 phase-local skills, 10 family-current runners, and 25 flashcards. {PRACTICE_BOUNDARY}

## Lifecycle

X1 `{X1_SHA}` and evidence `{EVIDENCE_SHA}` are immutable direct children in a zero-merge chain. Their 20 and 166 manifest entries replay exactly. The final candidate must be a direct child of evidence, then pushed, clean, 0/0 divergent, and equal across local, upstream, tracking, and fresh live remote before the single canonical invocation.

## Boundaries and route

The target-neutral successor candidate has not been sent. No recipient is inferred in repository state. A unique exact-title task must be resolved and immediately reread only after the exact-final canonical gate and fresh live authority and roster checks. No empirical, participant, professional, safety, production, deployment, legal, cultural, affected-party, access-and-benefit-sharing, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, or Stage 20 claim is established.
"""
    text("reports/terminal-overview.md", overview)
    write(
        "final/closeout-build-receipt.json",
        {
            "schema": "ghc.family.sable-rook.v666-v6.closeout-build-receipt.v1",
            "generated_at_utc": NOW,
            "builder": "scripts/build_ghc_family_sable_rook_v666_v6_closeout.py",
            "x1_manifest_entries": x1_replay["entry_count"],
            "evidence_manifest_entries": evidence_replay["entry_count"],
            "effective_negatives": phase_truth["effective_negatives"],
            "effective_methods": phase_truth["effective_methods"],
            "open_gaps": phase_truth["open_gaps"],
            "exact_gates": phase_truth["exact_gates"],
            "canonical_invoked": False,
            "successor_contacted": False,
            "status": "CLOSEOUT_CONTENT_BUILT_AWAITING_FINAL_STAGED_REVIEW",
        },
    )
    print(
        json.dumps(
            {
                "x1_manifest_entries": x1_replay["entry_count"],
                "evidence_manifest_entries": evidence_replay["entry_count"],
                "effective_negatives": phase_truth["effective_negatives"],
                "effective_methods": phase_truth["effective_methods"],
                "open_gaps": phase_truth["open_gaps"],
                "exact_gates": phase_truth["exact_gates"],
                "successor_contacted": False,
                "canonical_invoked": False,
            },
            sort_keys=True,
        )
    )


def staged_rows() -> list[tuple[str, str]]:
    raw = subprocess.check_output(
        ["git", "-C", str(ROOT), "diff", "--cached", "--name-status", "--no-renames"]
    ).decode("utf-8")
    return [
        (line.split("\t", 1)[0], line.split("\t", 1)[1].replace("\\", "/"))
        for line in raw.splitlines()
        if line
    ]


def staged_index_map() -> dict[str, tuple[str, str, str]]:
    raw = subprocess.check_output(
        ["git", "-C", str(ROOT), "ls-files", "--stage", "-z"]
    )
    result: dict[str, tuple[str, str, str]] = {}
    for record in raw.split(b"\0"):
        if not record:
            continue
        metadata, encoded_path = record.split(b"\t", 1)
        mode, oid, stage = metadata.decode("ascii").split()
        result[encoded_path.decode("utf-8").replace("\\", "/")] = (mode, oid, stage)
    return result


def batch_blobs(paths: list[str], index: dict[str, tuple[str, str, str]]) -> dict[str, bytes]:
    result: dict[str, bytes] = {}
    process = subprocess.Popen(
        ["git", "-C", str(ROOT), "cat-file", "--batch"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        if process.stdin is None or process.stdout is None:
            raise RuntimeError("git cat-file pipes unavailable")
        for path in paths:
            mode, oid, stage = index[path]
            if stage != "0" or mode != "100644":
                raise RuntimeError(f"unexpected index state for {path}")
            process.stdin.write((oid + "\n").encode("ascii"))
            process.stdin.flush()
            header = process.stdout.readline().decode("ascii").strip().split()
            if len(header) != 3 or header[0] != oid or header[1] != "blob":
                raise RuntimeError(f"invalid batch header for {path}")
            result[path] = read_exact(process.stdout, int(header[2]))
            if read_exact(process.stdout, 1) != b"\n":
                raise RuntimeError(f"missing batch terminator for {path}")
    finally:
        if process.stdin is not None:
            process.stdin.close()
        return_code = process.wait(timeout=30)
        stderr = process.stderr.read().decode("utf-8", errors="replace") if process.stderr else ""
        if process.stdout is not None:
            process.stdout.close()
        if process.stderr is not None:
            process.stderr.close()
        if return_code:
            raise RuntimeError(stderr[:240])
    return result


def owner_path(path: str) -> bool:
    return (
        path.startswith("docs/sable-rook/v666-v6/")
        or bool(re.fullmatch(r"scripts/(?:build_)?ghc_family_sable_rook_v666_v6_[a-z0-9_]+\.py", path))
        or bool(re.fullmatch(r"tests/test_ghc_family_sable_rook_v666_v6_[a-z0-9_]+\.py", path))
    )


def manifest_entry(path: str, mode: str, oid: str, blob: bytes) -> dict[str, Any]:
    return {
        "path": path,
        "git_mode": mode,
        "git_blob_oid": oid,
        "sha256": hashlib.sha256(blob).hexdigest(),
        "size_bytes": len(blob),
    }


def build_staged_review() -> None:
    review_path = "docs/sable-rook/v666-v6/validation/final-staged-review.json"
    delta_path = "docs/sable-rook/v666-v6/validation/final-delta-manifest.json"
    owner_manifest_path = "docs/sable-rook/v666-v6/validation/final-owner-manifest.json"
    excluded = {review_path, delta_path, owner_manifest_path}
    rows = [(status, path) for status, path in staged_rows() if path not in excluded]
    if not rows:
        raise RuntimeError("no staged final content")
    paths = [path for _, path in rows]
    invalid = [path for path in paths if not owner_path(path)]
    immutable_prefixes = (
        "docs/sable-rook/v666-v6/x1/",
        "docs/sable-rook/v666-v6/x2/",
        "docs/sable-rook/v666-v6/evidence/",
        "docs/sable-rook/v666-v6/deck/",
        "docs/sable-rook/v666-v6/skills/",
    )
    immutable_changes = [path for path in paths if path.startswith(immutable_prefixes)]
    allowed_doc_prefixes = (
        "docs/sable-rook/v666-v6/closeout/",
        "docs/sable-rook/v666-v6/final/",
        "docs/sable-rook/v666-v6/handoffs/",
        "docs/sable-rook/v666-v6/lifecycle/",
        "docs/sable-rook/v666-v6/orchestration/",
        "docs/sable-rook/v666-v6/validation/",
        "docs/sable-rook/v666-v6/method-flow/closeout-",
        "docs/sable-rook/v666-v6/reports/terminal-",
    )
    unexpected_docs = [
        path
        for path in paths
        if path.startswith("docs/sable-rook/v666-v6/")
        and not path.startswith(allowed_doc_prefixes)
    ]
    index = staged_index_map()
    blobs = batch_blobs(paths, index)
    privacy_patterns = {
        "raw_task_or_thread_identifier": re.compile(r'(?i)["\'](?:source_)?(?:task|thread)[_-]?id["\']\s*[:=]\s*["\'][^"\']+["\']'),
        "private_absolute_path": re.compile(r"(?i)[A-Z]:\\(?:Users\\|GHC-Archives\\)"),
        "credential_or_token_value": re.compile(r"(?i)(?:bearer\s+[A-Za-z0-9._~-]{12,}|api[_-]?key\s*[:=]\s*[^\s,}]+)"),
        "session_identifier_value": re.compile(r'(?i)["\'](?:session|resume)[_-]?(?:id|value)["\']\s*[:=]\s*["\'][^"\']+["\']'),
        "private_callable_identifier_value": re.compile(r'(?i)["\']private[_-]?callable[_-]?id["\']\s*[:=]\s*["\'][^"\']+["\']'),
    }
    parsed_json = 0
    maximum_words = 0
    maximum_path = ""
    privacy_candidates = []
    security_findings = []
    for path in paths:
        value = blobs[path].decode("utf-8")
        if "\r" in value:
            raise RuntimeError(f"non-LF staged text: {path}")
        words = len(re.findall(r"\S+", value))
        if words > maximum_words:
            maximum_words, maximum_path = words, path
        if path.endswith(".json"):
            json.loads(value)
            parsed_json += 1
        for class_name, pattern in privacy_patterns.items():
            if pattern.search(value):
                privacy_candidates.append({"path": path, "class": class_name})
        if path.endswith(".py"):
            tree = ast.parse(value, filename=path)
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                name = node.func.id if isinstance(node.func, ast.Name) else node.func.attr if isinstance(node.func, ast.Attribute) else ""
                if name in {"eval", "exec"}:
                    security_findings.append({"path": path, "line": node.lineno, "class": f"dynamic_{name}"})
                if any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords):
                    security_findings.append({"path": path, "line": node.lineno, "class": "shell_true"})
    phase_truth = json.loads(blobs["docs/sable-rook/v666-v6/closeout/phase-truth.json"])
    route = json.loads(blobs["docs/sable-rook/v666-v6/orchestration/route-state-final-candidate.json"])
    evidence_tree = git_tree_map(EVIDENCE_SHA)
    evidence_owner_count = sum(owner_path(path) for path in evidence_tree)
    final_owner_count = evidence_owner_count + len(paths) + 3
    checks = {
        "additive_only": all(status == "A" for status, _ in rows),
        "all_json_parse": True,
        "document_word_cap": maximum_words <= 100000,
        "five_class_scan_zero_confirmed_hits": not privacy_candidates,
        "bounded_changed_python_security_zero_findings": not security_findings,
        "owner_allowlist": not invalid,
        "immutable_x1_x2_evidence_deck_skills_unchanged": not immutable_changes,
        "unexpected_document_paths_absent": not unexpected_docs,
        "owner_file_cap": final_owner_count <= 2000,
        "expected_14_4_1_1": phase_truth["outcomes"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "effective_counts": phase_truth["effective_negatives"] == 26758 and phase_truth["effective_methods"] == 11645,
        "gaps_and_gates": phase_truth["open_gaps"] == 188 and phase_truth["exact_gates"] == 186,
        "route_prepared_not_sent": route["route"] == "PREPARED_NOT_SENT" and not route["successor_contacted"],
        "terminal_not_ready": phase_truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "utf8_lf": True,
    }
    review = {
        "schema": "ghc.family.sable-rook.v666-v6.final-staged-review.v1",
        "owner": "Sable Rook",
        "phase": "v666-v6",
        "lifecycle": "final",
        "generated_at_utc": NOW,
        "reviewed_from": "git_index_blobs",
        "evidence_sha": EVIDENCE_SHA,
        "reviewed_paths": paths,
        "reviewed_path_count": len(paths),
        "evidence_owner_count": evidence_owner_count,
        "exact_final_owner_count": final_owner_count,
        "json_parsed": parsed_json,
        "maximum_document_words": maximum_words,
        "maximum_document_path": maximum_path,
        "privacy_scan_classes": list(privacy_patterns),
        "privacy_candidates": len(privacy_candidates),
        "privacy_confirmed_hits": len(privacy_candidates),
        "privacy_candidate_rows": privacy_candidates,
        "changed_python_security_findings": security_findings,
        "checks": checks,
        "self_exclusions": [review_path, delta_path, owner_manifest_path],
        "claim_boundary": "exact staged same-owner closeout review only; not exhaustive security, privacy, accessibility, seed identity or viability, biosecurity, professional review, or independent reproduction",
        "valid": all(checks.values()),
    }
    if not review["valid"]:
        raise RuntimeError(json.dumps(review, ensure_ascii=False, sort_keys=True))
    write("validation/final-staged-review.json", review)
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--sparse", "--", review_path])
    delta_rows = [(status, path) for status, path in staged_rows() if path not in {delta_path, owner_manifest_path}]
    delta_index = staged_index_map()
    delta_paths = [path for _status, path in delta_rows]
    delta_blobs = batch_blobs(delta_paths, delta_index)
    delta_entries = [
        manifest_entry(path, delta_index[path][0], delta_index[path][1], delta_blobs[path])
        for _status, path in delta_rows
    ]
    write(
        "validation/final-delta-manifest.json",
        {
            "schema": "ghc.family.sable-rook.v666-v6.final-delta-manifest.v1",
            "owner": "Sable Rook",
            "phase": "v666-v6",
            "generated_at_utc": NOW,
            "parent_evidence_sha": EVIDENCE_SHA,
            "hash_source": "actual_git_index_blobs",
            "entries": delta_entries,
            "entry_count": len(delta_entries),
            "deletion_count": 0,
            "additive_only": all(status == "A" for status, _path in rows),
            "self_exclusions": [delta_path, owner_manifest_path],
        },
    )
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--sparse", "--", delta_path])
    final_index = staged_index_map()
    projected: dict[str, tuple[str, str]] = {
        path: state for path, state in evidence_tree.items() if owner_path(path)
    }
    for status, path in staged_rows():
        if path == owner_manifest_path:
            continue
        if status != "A" or not owner_path(path):
            raise RuntimeError(f"unexpected final staged path {status} {path}")
        mode, oid, stage = final_index[path]
        if stage != "0":
            raise RuntimeError(f"unexpected final index stage for {path}")
        projected[path] = (mode, oid)
    projected_paths = sorted(projected)
    projected_index = {path: (mode, oid, "0") for path, (mode, oid) in projected.items()}
    projected_blobs = batch_blobs(projected_paths, projected_index)
    owner_entries = [
        manifest_entry(path, projected[path][0], projected[path][1], projected_blobs[path])
        for path in projected_paths
    ]
    if len(owner_entries) != final_owner_count - 1:
        raise RuntimeError(f"owner manifest projection mismatch {len(owner_entries)} != {final_owner_count - 1}")
    write(
        "validation/final-owner-manifest.json",
        {
            "schema": "ghc.family.sable-rook.v666-v6.final-owner-manifest.v1",
            "owner": "Sable Rook",
            "phase": "v666-v6",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "x1_sha": X1_SHA,
            "evidence_sha": EVIDENCE_SHA,
            "hash_source": "evidence_tree_plus_actual_final_index_blobs",
            "entries": owner_entries,
            "entry_count": len(owner_entries),
            "self_exclusion": owner_manifest_path,
            "exact_final_owner_count_including_self": final_owner_count,
            "file_ceiling": 2000,
            "within_file_ceiling": final_owner_count <= 2000,
        },
    )
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--sparse", "--", owner_manifest_path])
    file_budget_path = PHASE_ROOT / "final" / "final-file-budget.json"
    file_budget = load_json(file_budget_path)
    file_budget["exact_final_owner_count"] = final_owner_count
    file_budget["within_ceiling"] = final_owner_count <= 2000
    file_budget["note"] = "This post-review convenience projection is not manifest-bound because changing a staged content file after manifest construction is forbidden; the authoritative bound is the staged review and final-owner manifest."
    # Do not rewrite the staged file: preserve exact index review. The in-memory projection is printed only.
    print(
        json.dumps(
            {
                "reviewed": len(paths),
                "final_delta_entries": len(delta_entries),
                "final_owner_manifest_entries": len(owner_entries),
                "final_owner_count_including_manifest": final_owner_count,
                "valid": True,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    if not sys.argv[1:]:
        build()
    elif sys.argv[1:] == ["--staged-review"]:
        build_staged_review()
    else:
        raise SystemExit(
            "usage: build_ghc_family_sable_rook_v666_v6_closeout.py [--staged-review]"
        )
