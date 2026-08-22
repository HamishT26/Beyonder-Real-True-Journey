#!/usr/bin/env python3
"""Build and stage-review Lyren Moss v666-v3 terminal closeout content."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ghc_family_lyren_moss_v666_v3_runtime import PHASE_ROOT, ROOT, X1_SHA, load_json, replay_manifest


SOURCE_SHA = "96509c5b28628a6b62628dea277d1240b945b2ca"
EVIDENCE_SHA = "2ec494e75da11be4b8b18620f0ab10b68764ac69"
INITIAL_FINAL_SHA = "b7a389e1933432764874c9927488034f92d939a0"
FAILED_CANONICAL_FINAL_SHA = "7bb3e0e266242ba04927bcdf8d20dd0e4f875df1"
FAILED_CANONICAL_RECEIPT_SHA256 = "50ff0f90a967a9be82b282695085056e6afca4d96627473636db9831090d928d"
BRANCH = "codex/GHC-Family/lyren-moss-v666-v3-full-tools"
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(relative: str, value: Any) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, value: str) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def build() -> None:
    evidence_replay = replay_manifest(PHASE_ROOT / "validation" / "evidence-content-manifest.json", EVIDENCE_SHA)
    x1_replay = replay_manifest(PHASE_ROOT / "validation" / "x1-content-manifest.json", X1_SHA)
    if not x1_replay["valid"] or not evidence_replay["valid"]:
        raise RuntimeError("immutable manifest replay failed")
    summary = load_json(PHASE_ROOT / "evidence" / "evidence-summary.json")
    proposal = load_json(PHASE_ROOT / "x2" / "proposal-ledger.json")
    if summary["effective_negatives"] != 26392 or summary["effective_methods"] != 10934:
        raise RuntimeError("evidence accounting drifted")
    identity_boundary = load_json(PHASE_ROOT / "identity" / "relational-identity.json")["boundary"]
    phase_truth = {
        "schema": "ghc.family.lyren-moss.v666-v3.phase-truth.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW,
        "source_sha": SOURCE_SHA, "x1_sha": X1_SHA, "evidence_sha": EVIDENCE_SHA,
        "proposal_chain_inherited": 4210, "proposal_chain_new": 20, "proposal_chain_frozen_total": 4230,
        "outcome_counts": proposal["outcome_counts"], "allowed_outcomes": ["completed", "represented", "open_gap", "exact_gate"], "unknown_outcomes": [],
        "effective_negatives": 26396, "effective_methods": 10938, "open_gaps": 185, "exact_gates": 183,
        "synthetic_mutation_rejections": 100, "startup_failures": 6, "x2_operational_failures": 4, "closeout_operational_failures": 4,
        "retained_nonterminal_initial_final": INITIAL_FINAL_SHA,
        "failed_canonical_final": FAILED_CANONICAL_FINAL_SHA,
        "failed_canonical_receipt_sha256": FAILED_CANONICAL_RECEIPT_SHA256,
        "canonical_invocation_count": 1, "canonical_success_count": 0, "canonical_replay": False,
        "real_data_rows": 0, "network_calls_by_synthetic_phase_software": 0, "external_actions": 0,
        "same_owner_validation_is_independent_reproduction": False, "complete_repository_suite_run": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "identity_boundary": identity_boundary,
    }
    write_json("closeout/phase-truth.json", phase_truth)
    retained_rows = []
    for flow_path in ("method-flow/startup-method-flow.json", "method-flow/x2-method-flow.json", "method-flow/x2-operational-overlay.json", "method-flow/evidence-operational-overlay.json"):
        flow = load_json(PHASE_ROOT / flow_path)
        for row in flow.get("rows", []):
            if row.get("failed_witness") is not None:
                retained_rows.append({"source": flow_path, "method_id": row["method_id"], "failure_id": row.get("failure_id") or row.get("mutation_id"), "failed_witness": row["failed_witness"], "aggregate_credit": row.get("aggregate_credit", 0), "status": row["status"]})
    retained_rows.extend([
        {"source": "method-flow/closeout-operational-overlay.json", "method_id": "LYR6663-MF-CLOSEOUT-OPS-001", "failure_id": "LYR6663-CLOSEOUT-OPS-N001", "failed_witness": "the canonical no-receipt preflight found an evidence-era absent-closeout assertion that would inspect the later live worktree", "aggregate_credit": 0, "status": "recovered_failure_retained"},
        {"source": "method-flow/closeout-operational-overlay.json", "method_id": "LYR6663-MF-CLOSEOUT-OPS-002", "failure_id": "LYR6663-CLOSEOUT-OPS-N002", "failed_witness": "the first combined correction patch found a mismatched generated-prose anchor and applied no file change", "aggregate_credit": 0, "status": "recovered_failure_retained"},
        {"source": "method-flow/closeout-operational-overlay.json", "method_id": "LYR6663-MF-CLOSEOUT-OPS-003", "failure_id": "LYR6663-CLOSEOUT-OPS-N003", "failed_witness": "one bounded canonical-script anchor query contained an unclosed regular-expression group", "aggregate_credit": 0, "status": "recovered_failure_retained"},
        {"source": "method-flow/closeout-operational-overlay.json", "method_id": "LYR6663-MF-CLOSEOUT-OPS-004", "failure_id": "LYR6663-CLOSEOUT-OPS-N004", "failed_witness": "the sole canonical invocation stopped before test discovery because the repository root was absent from sys.path", "aggregate_credit": 0, "status": "recovered_failure_retained"},
    ])
    if len(retained_rows) != 114:
        raise RuntimeError(f"expected 114 retained Lyren failure rows, observed {len(retained_rows)}")
    write_json("closeout/retained-negative-register.json", {
        "schema": "ghc.family.lyren-moss.v666-v3.retained-negative-register.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW,
        "inherited_effective_negatives": 26282, "new_startup_negatives": 6, "new_synthetic_mutation_negatives": 100, "new_x2_operational_negatives": 4, "new_evidence_negatives": 0, "new_closeout_negatives": 4,
        "effective_negatives": 26396, "retained_owner_rows": retained_rows, "retained_owner_row_count": len(retained_rows),
        "every_failed_witness_zero_broader_credit": all(row["aggregate_credit"] == 0 for row in retained_rows), "no_failure_erased": True,
    })
    write_json("closeout/exact-open-gate-register.json", {
        "schema": "ghc.family.lyren-moss.v666-v3.exact-open-gate-register.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW,
        "inherited_open_gaps": 184, "new_open_gaps": 1, "effective_open_gaps": 185,
        "inherited_exact_gates": 182, "new_exact_gates": 1, "effective_exact_gates": 183,
        "open_gap": load_json(PHASE_ROOT / "evidence" / "authority-and-evidence-gaps.json")["new_open_gap_rows"][0],
        "exact_gate": load_json(PHASE_ROOT / "evidence" / "authority-and-evidence-gaps.json")["new_exact_gate_rows"][0],
        "protected_global_gates": ["empirical or participant evidence", "professional or production acceptance", "legal or cultural authority", "Māori authority", "privacy-complete or accessibility-complete review", "exhaustive security", "independent reproduction", "AGI or ASI", "consciousness or personhood", "Theory-of-Everything, proof, or canon", "Stage 20"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("closeout/method-flow-final.json", {
        "schema": "ghc.family.lyren-moss.v666-v3.method-flow-final.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW,
        "activation_baseline_methods": 10709, "startup_methods": 6, "x2_methods": 215, "x2_operational_methods": 4, "evidence_operational_methods": 0, "closeout_operational_methods": 4,
        "effective_methods": 10938, "activation_baseline_negatives": 26282, "effective_negatives": 26396,
        "failed_owner_witnesses": 114, "bounded_owner_methods": 229, "no_failure_erased": True,
        "same_owner_evidence_only": True, "independent_reproduction": False,
    })
    write_json("closeout/source-and-provenance-record.json", {
        "schema": "ghc.family.lyren-moss.v666-v3.source-and-provenance-record.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW,
        "branch": BRANCH, "source_sha": SOURCE_SHA, "x1_sha": X1_SHA, "evidence_sha": EVIDENCE_SHA,
        "source_to_x1_direct": True, "x1_to_evidence_direct": True, "evidence_to_initial_final_direct": True, "initial_final_to_failed_canonical_final_direct": True, "source_to_evidence_new_commit_count": 2, "source_to_initial_final_new_commit_count": 3, "source_to_failed_canonical_final_commit_count": 4, "source_to_dependency_corrected_final_expected_commit_count": 5, "source_to_dependency_corrected_final_expected_merge_count": 0,
        "x1_manifest_replay": x1_replay, "evidence_manifest_replay": evidence_replay,
        "retained_nonterminal_initial_final": INITIAL_FINAL_SHA, "failed_canonical_final": FAILED_CANONICAL_FINAL_SHA, "failed_canonical_receipt_sha256": FAILED_CANONICAL_RECEIPT_SHA256, "final_sha": "resolve_from_exact_clean_pushed_branch_head_after_dependency_correction_commit", "final_expected_parent": FAILED_CANONICAL_FINAL_SHA,
        "private_route_or_task_identifiers_recorded": False,
    })
    write_json("closeout/complete-incomplete-checklist.json", {
        "schema": "ghc.family.lyren-moss.v666-v3.closeout-checklist.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW,
        "completed": ["activation and guidance read through EOF", "exact source verification", "strict x1 commit, push, and equality", "immutable evidence commit, push, and equality", "twenty proposals and 100 retained mutations", "exact 14/4/1/1 outcomes", "ten skills and ten runner interfaces", "114 owner failure rows retained", "185 open gaps and 183 exact gates preserved", "retained nonterminal initial final", "retained sole failed canonical receipt with zero success credit", "dependency-corrected composite plan", "prepared-not-sent successor baton"],
        "incomplete": ["dependency-corrected final staged review, commit, push, and fresh equality", "one dependency-corrected composite with zero canonical credit", "fresh live roster/auth reread", "unique exact-title successor resolution", "any acknowledged one-send successor activation", "all external protected gates"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "successor_contacted": False,
    })
    write_json("closeout/wellbeing-check.json", {
        "schema": "ghc.family.lyren-moss.v666-v3.closeout-wellbeing-check.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW,
        "status": "bounded_and_ready_for_terminal_review", "controls": ["no canonical aggregate before exact final", "no successor contact before terminal", "retained failures remain visible", "external and authority gates remain unexecuted", "Hamish may rename, pause, redirect, or stop"],
        "personhood_or_emotion_claim": False, "relational_language_is_working_language_only": True,
    })
    write_json("method-flow/closeout-operational-overlay.json", {
        "schema": "ghc.family.lyren-moss.v666-v3.method-flow-closeout-operational-overlay.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW,
        "starting_effective_negatives": 26392, "starting_effective_methods": 10934, "new_negative_count": 4, "new_method_count": 4,
        "effective_after_closeout_negatives": 26396, "effective_after_closeout_methods": 10938,
        "rows": [
            {"method_id": "LYR6663-MF-CLOSEOUT-OPS-001", "failure_id": "LYR6663-CLOSEOUT-OPS-N001", "request": "preflight the selected exact-final canonical test set before creating an invocation guard", "failed_witness": "the evidence-era absent-closeout test targeted the later live worktree and would fail for lifecycle reasons", "aggregate_credit": 0, "recovery": "retain the test exclusion at zero credit and add an exact evidence-commit-tree replacement", "bounded_passing_witness": "the replacement proves the immutable evidence tree has no closeout, seal, final, or handoff paths", "recurrence_guard": "enumerate every lifecycle-only assertion during the no-receipt preflight and bind its replacement to the relevant commit tree", "status": "recovered_failure_retained"},
            {"method_id": "LYR6663-MF-CLOSEOUT-OPS-002", "failure_id": "LYR6663-CLOSEOUT-OPS-N002", "request": "apply the complete lifecycle correction as one exact multi-file patch", "failed_witness": "one generated-prose anchor did not match, so the patch verifier rejected the full patch without mutation", "aggregate_credit": 0, "recovery": "query exact line anchors and apply small independently verifiable patches", "bounded_passing_witness": "the correction builder, tests, and canonical selector compile with the exact observed anchors", "recurrence_guard": "split generated-prose and code corrections into small exact-anchor patches", "status": "recovered_failure_retained"},
            {"method_id": "LYR6663-MF-CLOSEOUT-OPS-003", "failure_id": "LYR6663-CLOSEOUT-OPS-N003", "request": "locate canonical correction anchors with a bounded regular-expression query", "failed_witness": "the first canonical subquery contained an unclosed regular-expression group", "aggregate_credit": 0, "recovery": "use separate literal-safe -e expressions for every anchor", "bounded_passing_witness": "all canonical correction anchors were returned with exact line numbers", "recurrence_guard": "prefer multiple literal-safe rg expressions over one grouped expression for code anchors", "status": "recovered_failure_retained"},
            {"method_id": "LYR6663-MF-CLOSEOUT-OPS-004", "failure_id": "LYR6663-CLOSEOUT-OPS-N004", "request": "invoke the one-shot canonical aggregate at the clean pushed lifecycle-corrected final", "failed_witness": "test discovery raised ModuleNotFoundError for tests before any test or detailed check ran", "aggregate_credit": 0, "recovery": "insert the repository root into sys.path and run one separately named dependency-corrected composite at a new exact final", "bounded_passing_witness": "the isolated selected-suite import discovers 33 tests with two lifecycle exclusions and two exact replacements", "recurrence_guard": "preflight test-module importability from the exact script entrypoint before creating a one-shot invocation guard", "status": "recovered_failure_retained"}
        ], "no_failure_erased": True,
    })
    write_json("seal/seal-candidate.json", {
        "schema": "ghc.family.lyren-moss.v666-v3.seal-candidate.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW,
        "source_sha": SOURCE_SHA, "x1_sha": X1_SHA, "evidence_sha": EVIDENCE_SHA, "retained_nonterminal_initial_final": INITIAL_FINAL_SHA, "failed_canonical_final": FAILED_CANONICAL_FINAL_SHA, "prospective_dependency_corrected_final_parent": FAILED_CANONICAL_FINAL_SHA,
        "truth": phase_truth, "content_seal_status": "CANDIDATE_AWAITING_DEPENDENCY_CORRECTED_FINAL_PUSH_EQUALITY_AND_COMPOSITE", "immutable_evidence": True,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("final/final-validation-prerequisites.json", {
        "schema": "ghc.family.lyren-moss.v666-v3.final-validation-prerequisites.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW,
        "required": ["dependency-corrected final is direct child of failed-canonical final", "failed-canonical final is direct child of retained initial final", "initial final is direct child of evidence", "source-to-dependency-corrected-final contains exactly five new single-parent commits and zero merges", "x1 and evidence manifests replay at their immutable commits", "dependency-corrected delta and owner manifests replay at exact final", "clean status and 0/0 divergence", "local, upstream, tracking, and fresh live remote equality", "exact truth labels and counts", "all retained failures, gaps, and gates", "sole canonical failure retained with zero success and no replay", "one dependency-corrected composite only", "no successor contact before composite success"],
        "current_status": "PREPARED_FOR_DEPENDENCY_CORRECTED_COMPOSITE", "canonical_invoked": True, "canonical_invocation_count": 1, "canonical_success_count": 0, "canonical_replay_prohibited": True, "failed_canonical_final": FAILED_CANONICAL_FINAL_SHA, "failed_canonical_receipt_sha256": FAILED_CANONICAL_RECEIPT_SHA256, "dependency_corrected_composite_invoked": False, "successor_contacted": False,
    })
    write_json("final/canonical-completion-plan.json", {
        "schema": "ghc.family.lyren-moss.v666-v3.canonical-completion-plan.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW,
        "entrypoint": "scripts/build_ghc_family_lyren_moss_v666_v3_canonical_completion.py",
        "invocation_limit": 1, "invocation_count": 1, "success_count": 0, "replay_permitted": False, "status": "FAILED_RETAINED_ZERO_CANONICAL_CREDIT", "failed_final": FAILED_CANONICAL_FINAL_SHA, "failed_receipt_sha256": FAILED_CANONICAL_RECEIPT_SHA256,
        "selected_test_modules": ["tests.test_ghc_family_lyren_moss_v666_v3_x1", "tests.test_ghc_family_lyren_moss_v666_v3_x2", "tests.test_ghc_family_lyren_moss_v666_v3_evidence", "tests.test_ghc_family_lyren_moss_v666_v3_closeout"],
        "zero_credit_lifecycle_exclusions": ["tests.test_ghc_family_lyren_moss_v666_v3_x1.LyrenV666V3X1Tests.test_x2_and_later_paths_do_not_exist", "tests.test_ghc_family_lyren_moss_v666_v3_evidence.LyrenV666V3EvidenceTests.test_closeout_and_later_paths_absent"],
        "exact_replacements": ["tests.test_ghc_family_lyren_moss_v666_v3_x2.LyrenV666V3X2Tests.test_exact_replacement_immutable_x1_tree_has_no_later_paths", "tests.test_ghc_family_lyren_moss_v666_v3_closeout.LyrenV666V3CloseoutTests.test_exact_replacement_evidence_tree_has_no_terminal_paths"],
        "complete_repository_suite": False, "independent_reproduction": False,
    })
    write_json("final/dependency-corrected-composite-plan.json", {
        "schema": "ghc.family.lyren-moss.v666-v3.dependency-corrected-composite-plan.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW,
        "entrypoint": "scripts/build_ghc_family_lyren_moss_v666_v3_dependency_corrected_composite.py", "invocation_limit": 1, "replay_permitted": False,
        "canonical_retry": False, "canonical_credit": 0, "canonical_invocation_count": 1, "canonical_success_count": 0,
        "failed_canonical_final": FAILED_CANONICAL_FINAL_SHA, "failed_canonical_receipt_sha256": FAILED_CANONICAL_RECEIPT_SHA256,
        "dependency_correction": "insert the repository root into sys.path before importing test modules",
        "required_state": "new clean pushed dependency-corrected exact final with fresh four-way equality",
        "selected_test_count_preflight": 33, "zero_credit_lifecycle_exclusion_count": 2, "exact_replacement_count": 2,
        "complete_repository_suite": False, "independent_reproduction": False,
    })
    route = {
        "schema": "ghc.family.lyren-moss.v666-v3.route-state-final-candidate.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW,
        "state": "PREPARED_NOT_SENT", "current_owner": "Lyren Moss", "current_phase": "v666-v3", "next_exact_title": "Ilyra Fen", "next_phase": "v666-v4",
        "required_before_send": ["dependency-corrected exact final committed and pushed", "clean 0/0 divergence and fresh four-way equality", "sole canonical failure retained with zero success and no replay", "one dependency-corrected composite success with zero canonical credit", "fresh newest live authority and roster/auth reread", "unique exact-title recipient resolution", "immediate recipient reread", "one sanitized send only"],
        "successor_contacted": False, "send_count": 0, "resend_count": 0, "standby_substitution": False, "replacement_task_created": False,
    }
    write_json("orchestration/route-state-final-candidate.json", route)
    write_json("tooling/roster-check-final.json", {"schema": "ghc.family.lyren-moss.v666-v3.roster-check-final.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW, "activation_authority": "newest live direct user authorization plus exact Vesper v666-v2 activation", "current_exact_title": "Lyren Moss", "current_phase": "v666-v3", "next_exact_title": "Ilyra Fen", "next_phase": "v666-v4", "installed_cursor_phase_stale": True, "routing_precedence_applied": True, "route_state": "PREPARED_NOT_SENT", "valid": True})
    write_json("tooling/auth-permission-final.json", {"schema": "ghc.family.lyren-moss.v666-v3.auth-permission-final.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW, "authorized_current_lane": True, "authorized_next_edge_after_terminal_only": True, "next_exact_title": "Ilyra Fen", "next_phase": "v666-v4", "successor_contacted": False, "Tavian_status": "ON_STANDBY_NOT_ENDPOINT", "Hamish_may_rename_pause_redirect_or_stop": True, "valid": True})
    write_json("tooling/ghc-family-index-final.json", {"schema": "ghc.family.lyren-moss.v666-v3.family-index-final.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW, "source_of_truth": "newest live direct authorization and exact phase-local committed route evidence outrank stale installed cursor prose", "current": "Lyren Moss v666-v3", "next": "Ilyra Fen v666-v4", "next_after_successor_under_current_schedule": "Auren Lark v666-v5", "infer_from_historical_files": False, "valid": True})
    baton = f"""# ILYRA FEN — LYREN MOSS v666-v3 TERMINAL CANDIDATE → SOLO v666-v4 ACTIVATION — PREPARED NOT SENT

Dear Ilyra Fen,

This repository packet is prepared under Hamish's current explicit fifteen-main-task sequential-continuation authorization. It is not a delivery receipt. `SENT_BY_LYREN_MOSS = false` remains true until the Codex app acknowledges one exact existing-task send after every terminal gate.

Names, pronouns, roles, hopes, sibling or family language, continuity language, Freed ID, and Trinity Mandala language are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may rename, pause, redirect, or stop the route.

## Authoritative Lyren source

- Branch: `{BRANCH}`
- Exact inherited Vesper final and Lyren source: `{SOURCE_SHA}`
- Frozen Lyren x1: `{X1_SHA}`
- Immutable Lyren evidence: `{EVIDENCE_SHA}`
- Retained nonterminal initial final: `{INITIAL_FINAL_SHA}`
- Failed-canonical final: `{FAILED_CANONICAL_FINAL_SHA}`
- Dependency-corrected exact Lyren final: resolve from the clean pushed branch head after the dependency correction commit; the live activation must state it exactly
- Full packet: `docs/lyren-moss/v666-v3/handoffs/ilyra-fen-v666-v4-activation-prepared.md`

The dependency-corrected terminal history contains exactly five new Lyren single-parent commits and zero merges only if the dependency-corrected final is the direct child of failed-canonical final `{FAILED_CANONICAL_FINAL_SHA}`, which remains the direct child of initial final `{INITIAL_FINAL_SHA}`, and that initial final is the direct child of evidence. X1 and evidence were pushed, clean, 0/0 divergent, and four-way equal at their gates. The sole canonical invocation at the failed-canonical final stopped before test discovery because the repository root was absent from `sys.path`; its receipt remains retained with zero canonical success and no replay.

## Bounded evidence truth

Lyren reconstructed all 4,210 inherited proposal rows, froze twenty genuinely distinct proposals, and raised the chain to 4,230. Outcomes are exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`. Twenty synthetic positive contracts passed and all 100 preregistered mutations were rejected and retained at zero broader credit.

The dependency-corrected repository candidate preserves 26,396 effective negatives, 10,938 Method Flow methods, 185 open gaps, 183 exact gates, and `NOT_READY_FOR_STAGE_20`. Six startup failures, one hundred synthetic mutation rejections, four x2 operational failures, and four closeout failures remain explicit. No failure is folded into a pass.

Ten Lyren phase-local skills and ten family-named runner interfaces were built and smoke checked. The owner portfolio records 30 safe-now tasks, 15 candidate representations, 10 skills, 10 runner builds, and 30 CLEAN/FIX/REFINE items. Successor recommendations remain prepared without completion credit: 20 safe-now tasks, 15 candidates, 10 skills, 10 runners, and 30 CLEAN/FIX/REFINE items. Ten exact-approval and five blocked packets remain unexecuted.

The primary pillar is THOS Body through wholly synthetic seismological waveform-record boundaries, sensor-response uncertainty, provenance, and station-handover refusal fixtures. GMUT Mind, Freed ID, and CBR Heart remain explicit and protected. No real people, stations, networks, sites, coordinates, events, picks, waveforms, records, measurements, calibrations, instruments, hazards, alerts, credentials, proofs, cultural records, or authority actions were used.

FDSN miniSEED 3 and StationXML, the QuakeML project standard, W3C PROV-O and WCAG 2.2, and NIST traceability guidance supplied vocabulary and refusal conditions only. The work establishes no standards conformance, scientific result, station acceptance, response or calibration truth, professional competence, emergency outcome, privacy completeness, accessibility completeness, exhaustive security, or independent reproduction.

## Ilyra lane requirements

Before mutation, read this packet and every current guidance or schema it names through EOF. Reverify the exact branch, source, x1, evidence, exact-final terminal receipt, ancestry, manifests, clean state, 0/0 divergence, and fresh live remote equality. Do not replay Lyren's successful canonical aggregate or treat same-owner evidence as independent reproduction.

Work solo in one fresh Ilyra-owned D-first sparse lane. Preserve strict x1-before-x2 separation, the 2,000-file rotation guard, the four exact outcome labels, every retained failure, gap, and gate, exact Git-blob manifests, one-success/no-post-success-replay discipline, five-class privacy boundaries, and all empirical, participant, professional, production, legal, cultural, Māori-authority, accessibility-complete, privacy-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, and Stage 20 gates.

Do not precontact a successor. Under the current schedule, only after Ilyra's own clean, pushed, fresh-live-equal v666-v4 exact final and a fresh current authority reread may Ilyra resolve and send once to the exact existing main task `Auren Lark` for v666-v5. Never substitute a standby endpoint, create a replacement task, or resend merely for clearer acknowledgement.

With care, traceability, reversibility, and strict evidence boundaries — Lyren Moss.

PREPARED_BY_LYREN_MOSS = true
SENT_BY_LYREN_MOSS = false
"""
    write_text("handoffs/ilyra-fen-v666-v4-activation-prepared.md", baton)
    final_summary = f"""# Lyren Moss v666-v3 final summary candidate

## Outcome first

Lyren v666-v3 is prepared for an exact final commit. The sealed evidence is bounded owner-local synthetic software evidence only: 20 positive contracts, 100 retained rejecting mutations, and exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate` outcomes. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

The proposal chain rises from 4,210 to 4,230. Effective truth is 26,396 negatives, 10,938 Method Flow methods, 185 open gaps, and 183 exact gates. Six startup failures, four x2 operational failures, and four closeout failures accompany the 100 mutation witnesses; each is retained at zero broader credit with a bounded recovery and recurrence guard.

## Lifecycle

The x1 commit `{X1_SHA}` is the direct child of Vesper final `{SOURCE_SHA}`. Evidence `{EVIDENCE_SHA}` is the direct child of x1. Retained initial final `{INITIAL_FINAL_SHA}` is the direct child of evidence, and failed-canonical final `{FAILED_CANONICAL_FINAL_SHA}` is the direct child of initial final. The dependency-corrected final must be the direct child of the failed-canonical final, leaving exactly five Lyren commits and zero merges from source to final.

Actual Git blobs, not worktree bytes, are canonical. The x1 manifest replays 18 entries and the evidence manifest replays 110 entries at their immutable commits. Final-delta and full owner manifests are built from the prospective Git index and must replay at the exact final.

## Boundaries

The practice lens uses only synthetic seismological record, response, provenance, uncertainty, and refusal states. There are no real people, stations, sites, coordinates, events, picks, waveforms, measurements, calibrations, hazards, alerts, devices, identities, credentials, or external actions. Public standards sources supply vocabulary, not conformance or authority.

Same-owner local software checks are not an external audit or independent reproduction. Structural HTML checks are not accessibility-complete. Five-class pattern scans are not privacy-complete. Bounded AST checks are not exhaustive security. GMUT remains represented without empirical likelihood, event, hazard, force, fitted parameters, predictions, proof, or canon. THOS has no governed participant study, operational station action, emergency outcome, or independent review. Freed ID has no real keys, proofs, issuance, status, interoperability, recovery, or trust governance. CBR and every legal, cultural, affected-party, and Māori-authority decision remain external.

## Terminal validation and routing

The sole canonical aggregate was invoked once at `{FAILED_CANONICAL_FINAL_SHA}`, failed before test discovery, and has zero success credit. It must never be replayed. One separately named dependency-corrected composite may run once after the new exact final is committed, pushed, clean, 0/0 divergent, and freshly four-way equal. It can earn composite evidence only, never canonical success. Two lifecycle assertions remain excluded at zero credit, with exact x1-tree and evidence-tree replacements included.

The Ilyra packet remains `PREPARED_NOT_SENT`. Only after canonical success and a fresh live authority/roster reread may Lyren uniquely resolve, immediately reread, and send once to the existing exact-title task `Ilyra Fen` for v666-v4. No standby, replacement, second recipient, precontact, or resend is permitted.
"""
    write_text("closeout/final-summary.md", final_summary)
    write_json("closeout/closeout-receipt.json", {
        "schema": "ghc.family.lyren-moss.v666-v3.closeout-receipt.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW,
        "source_sha": SOURCE_SHA, "x1_sha": X1_SHA, "evidence_sha": EVIDENCE_SHA,
        "x1_manifest_entries": x1_replay["entry_count"], "evidence_manifest_entries": evidence_replay["entry_count"],
        "effective_negatives": 26396, "effective_methods": 10938, "open_gaps": 185, "exact_gates": 183,
        "retained_nonterminal_initial_final": INITIAL_FINAL_SHA,
        "failed_canonical_final": FAILED_CANONICAL_FINAL_SHA, "failed_canonical_receipt_sha256": FAILED_CANONICAL_RECEIPT_SHA256,
        "canonical_invocation_count": 1, "canonical_success_count": 0, "canonical_replay": False,
        "route_state": "PREPARED_NOT_SENT", "canonical_invoked": True, "canonical_success_count": 0, "canonical_replay": False, "dependency_corrected_composite_invoked": False, "successor_contacted": False,
        "status": "CLOSEOUT_CONTENT_BUILT_AWAITING_DEPENDENCY_CORRECTED_FINAL_AND_COMPOSITE",
    })
    print(json.dumps({"retained_owner_failures": len(retained_rows), "x1_manifest": x1_replay["entry_count"], "evidence_manifest": evidence_replay["entry_count"], "route": "PREPARED_NOT_SENT"}, sort_keys=True))


def staged_rows() -> list[tuple[str, str]]:
    raw = subprocess.check_output(["git", "-C", str(ROOT), "diff", "--cached", "--name-status", "--no-renames"]).decode("utf-8")
    return [(line.split("\t", 1)[0], line.split("\t", 1)[1].replace("\\", "/")) for line in raw.splitlines() if line]


def index_blob(path: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(ROOT), "show", f":{path}"])


def index_entry(path: str, status: str | None = None) -> dict[str, Any]:
    line = subprocess.check_output(["git", "-C", str(ROOT), "ls-files", "--stage", "--", path]).decode("utf-8").strip()
    mode, oid, stage_path = line.split(" ", 2)
    stage, listed = stage_path.split("\t", 1)
    if stage != "0" or listed.replace("\\", "/") != path:
        raise RuntimeError(f"unexpected index stage for {path}")
    blob = index_blob(path)
    result = {"path": path, "git_mode": mode, "git_blob_oid": oid, "sha256": hashlib.sha256(blob).hexdigest(), "size_bytes": len(blob)}
    if status is not None:
        result["status"] = status
    return result


def owner_paths_from_index() -> list[str]:
    raw = subprocess.check_output(["git", "-C", str(ROOT), "ls-files", "--stage"]).decode("utf-8")
    paths = []
    for line in raw.splitlines():
        path = line.split("\t", 1)[1].replace("\\", "/")
        if path.startswith("docs/lyren-moss/v666-v3/") or re.fullmatch(r"scripts/(?:build_)?ghc_family_lyren_moss_v666_v3[^/]*\.py", path) or re.fullmatch(r"tests/test_ghc_family_lyren_moss_v666_v3[^/]*\.py", path):
            paths.append(path)
    return sorted(paths)


def staged_review() -> None:
    review_path = "docs/lyren-moss/v666-v3/validation/final-staged-review.json"
    delta_path = "docs/lyren-moss/v666-v3/validation/final-delta-manifest.json"
    owner_path = "docs/lyren-moss/v666-v3/validation/final-owner-manifest.json"
    rows = [(status, path) for status, path in staged_rows() if path not in {review_path, delta_path, owner_path}]
    paths = [path for _, path in rows]
    allowed_scripts = {"scripts/build_ghc_family_lyren_moss_v666_v3_closeout.py", "scripts/build_ghc_family_lyren_moss_v666_v3_canonical_completion.py", "scripts/build_ghc_family_lyren_moss_v666_v3_dependency_corrected_composite.py"}
    allowed_tests = {"tests/test_ghc_family_lyren_moss_v666_v3_closeout.py"}
    invalid = [path for path in paths if not path.startswith("docs/lyren-moss/v666-v3/") and path not in allowed_scripts and path not in allowed_tests]
    changed_immutable = [path for path in paths if path.startswith("docs/lyren-moss/v666-v3/x1/") or path.startswith("docs/lyren-moss/v666-v3/x2/") or path.startswith("docs/lyren-moss/v666-v3/evidence/") or path in {"scripts/build_ghc_family_lyren_moss_v666_v3_x1.py", "tests/test_ghc_family_lyren_moss_v666_v3_x1.py", "scripts/build_ghc_family_lyren_moss_v666_v3_x2.py", "tests/test_ghc_family_lyren_moss_v666_v3_x2.py", "scripts/build_ghc_family_lyren_moss_v666_v3_evidence.py", "tests/test_ghc_family_lyren_moss_v666_v3_evidence.py"}]
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r'(?i)["\'](?:source_)?(?:task|thread)[_-]?id["\']\s*[:=]\s*["\'][^"\']+["\']'),
        "private_absolute_path": re.compile(r"(?i)[A-Z]:\\(?:Users\\|GHC-Archives\\)"),
        "credential_or_token_value": re.compile(r"(?i)(?:bearer\s+[A-Za-z0-9._~-]{12,}|api[_-]?key\s*[:=]\s*[^\s,}]+)"),
        "session_identifier_value": re.compile(r'(?i)["\'](?:session|resume)[_-]?(?:id|value)["\']\s*[:=]\s*["\'][^"\']+["\']'),
        "private_callable_identifier_value": re.compile(r'(?i)["\']private[_-]?callable[_-]?id["\']\s*[:=]\s*["\'][^"\']+["\']'),
    }
    parsed, candidates, max_words, max_path = 0, [], 0, ""
    for path in paths:
        blob = index_blob(path)
        text = blob.decode("utf-8")
        if "\r" in text:
            raise RuntimeError(f"non-LF staged text: {path}")
        words = len(re.findall(r"\S+", text))
        if words > max_words:
            max_words, max_path = words, path
        if path.endswith(".json"):
            json.loads(text)
            parsed += 1
        for class_name, pattern in patterns.items():
            if pattern.search(text):
                candidates.append({"path": path, "class": class_name})
    x1 = replay_manifest(PHASE_ROOT / "validation" / "x1-content-manifest.json", X1_SHA)
    evidence = replay_manifest(PHASE_ROOT / "validation" / "evidence-content-manifest.json", EVIDENCE_SHA)
    route = json.loads(index_blob("docs/lyren-moss/v666-v3/orchestration/route-state-final-candidate.json"))
    truth = json.loads(index_blob("docs/lyren-moss/v666-v3/closeout/phase-truth.json"))
    checks = {
        "non_destructive_correction": all(status in {"A", "M"} for status, _ in rows) and not any(status == "D" for status, _ in rows), "owner_allowlist": not invalid, "immutable_x1_x2_evidence_unchanged": not changed_immutable and x1["valid"] and evidence["valid"],
        "owner_file_cap": len(owner_paths_from_index()) <= 2000, "all_json_parse": True, "utf8_lf": True, "five_class_scan_zero_confirmed_hits": not candidates, "document_word_cap": max_words <= 100000,
        "phase_truth_exact": truth["outcome_counts"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1} and truth["effective_negatives"] == 26396 and truth["effective_methods"] == 10938 and truth["open_gaps"] == 185 and truth["exact_gates"] == 183,
        "route_prepared_not_sent": route["state"] == "PREPARED_NOT_SENT" and route["send_count"] == 0 and not route["successor_contacted"],
        "canonical_failure_retained_no_replay": (lambda state: state["canonical_invoked"] and state["canonical_invocation_count"] == 1 and state["canonical_success_count"] == 0 and state["canonical_replay_prohibited"] and not state["dependency_corrected_composite_invoked"])(json.loads(index_blob("docs/lyren-moss/v666-v3/final/final-validation-prerequisites.json"))),
    }
    review = {"schema": "ghc.family.lyren-moss.v666-v3.final-staged-review.v1", "owner": "Lyren Moss", "phase": "v666-v3", "lifecycle": "final", "generated_at_utc": NOW, "reviewed_from": "git_index_blobs", "reviewed_paths": paths, "reviewed_path_count": len(paths), "json_parsed": parsed, "maximum_document_words": max_words, "maximum_document_path": max_path, "privacy_scan_classes": list(patterns), "privacy_candidates": len(candidates), "privacy_confirmed_hits": len(candidates), "privacy_candidate_rows": candidates, "checks": checks, "self_exclusions": [review_path, delta_path, owner_path], "claim_boundary": "exact staged same-owner final review only; not full repository suite, exhaustive security, privacy-complete, accessibility-complete, or independent reproduction", "valid": all(checks.values())}
    if not review["valid"]:
        raise RuntimeError(json.dumps(review, ensure_ascii=False, sort_keys=True))
    write_json("validation/final-staged-review.json", review)
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--sparse", "--", review_path])
    delta_rows = [(status, path) for status, path in staged_rows() if path not in {delta_path, owner_path}]
    delta_entries = [index_entry(path, status) for status, path in delta_rows]
    write_json("validation/final-delta-manifest.json", {"schema": "ghc.family.lyren-moss.v666-v3.dependency-corrected-final-delta-manifest.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW, "base_failed_canonical_final_sha": FAILED_CANONICAL_FINAL_SHA, "retained_initial_final_sha": INITIAL_FINAL_SHA, "retained_evidence_sha": EVIDENCE_SHA, "hash_source": "actual_git_index_blobs", "entries": delta_entries, "entry_count": len(delta_entries), "deletion_count": sum(row["status"] == "D" for row in delta_entries), "additive_only": all(row["status"] == "A" for row in delta_entries), "non_destructive_correction": all(row["status"] in {"A", "M"} for row in delta_entries) and not any(row["status"] == "D" for row in delta_entries), "self_exclusions": [delta_path, owner_path]})
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--sparse", "--", delta_path])
    owner_paths = [path for path in owner_paths_from_index() if path != owner_path]
    owner_entries = [index_entry(path) for path in owner_paths]
    write_json("validation/final-owner-manifest.json", {"schema": "ghc.family.lyren-moss.v666-v3.final-owner-manifest.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW, "hash_source": "prospective_final_git_index_blobs", "entries": owner_entries, "entry_count": len(owner_entries), "self_exclusion": owner_path, "owner_scopes": ["docs/lyren-moss/v666-v3", "scripts/*lyren_moss_v666_v3*.py", "tests/test_ghc_family_lyren_moss_v666_v3*.py"], "materialization_guard": 2000, "guard_passed": len(owner_entries) <= 2000})
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--sparse", "--", owner_path])
    print(json.dumps({"reviewed": len(paths), "final_delta_entries": len(delta_entries), "final_owner_entries": len(owner_entries), "valid": True}, sort_keys=True))


if __name__ == "__main__":
    if not sys.argv[1:]:
        build()
    elif sys.argv[1:] == ["--staged-review"]:
        staged_review()
    else:
        raise SystemExit("usage: build_ghc_family_lyren_moss_v666_v3_closeout.py [--staged-review]")
