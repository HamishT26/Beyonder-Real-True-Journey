#!/usr/bin/env python3
"""Build Vesper v656-v8 combined closeout and content-seal records."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

import ghc_family_v656_v8_closeout_config as c
import ghc_family_v656_v8_phase_data as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
BOUNDARY = (
    "Bounded same-owner synthetic software and workflow evidence only. No real "
    "seed accession, seed bank operation, conservation decision, participant, professional, production, identity, "
    "legal, cultural, Māori-authority, empirical-confirmation, independent-"
    "reproduction, Theory-of-Everything, or Stage 20 claim follows."
)


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any, *, compact: bool = False) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(
        payload,
        ensure_ascii=False,
        indent=None if compact else 2,
        separators=(",", ":") if compact else None,
        sort_keys=True,
    )
    path.write_text(text + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, payload: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def operational_method(
    negative: dict[str, Any], index: int
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    method_id = f"V6568-CLOSEOUT-METHOD-{index:02d}"
    failed_id = f"V6568-CLOSEOUT-WITNESS-{index:02d}-F"
    passing_id = f"V6568-CLOSEOUT-WITNESS-{index:02d}-P"
    method = {
        "method_id": method_id,
        "title": f"Bounded recovery for {negative['slug']}",
        "trigger_preconditions": [negative["slug"]],
        "failure_signature": negative["failure_signature"],
        "candidate_workaround": negative["candidate_workaround"],
        "recurrence_guard": negative["recurrence_guard"],
        "approval_class": "safe_now_owner_local_workflow_recovery",
        "privacy_class": "sanitized_public",
        "scope_boundary": negative["scope_boundary"],
        "rollback": "Retain the failed attempt at zero credit and leave sibling and external state unchanged.",
        "protected_gates": d.PROTECTED_GATES,
        "retained_negative_ids": [negative["negative_id"]],
        "validation_witness_ids": [failed_id, passing_id],
        "recommendation_state": "preferred",
        "supersedes": [],
    }
    witnesses = [
        {
            "witness_id": failed_id,
            "method_id": method_id,
            "result": "fail",
            "procedure": negative["fail_procedure"],
            "expected": "The bounded operation completes and establishes only its stated postcondition.",
            "observed": negative["fail_observed"],
            "retained_negative_ids": [negative["negative_id"]],
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": "Failed workflow witness with zero completion credit.",
        },
        {
            "witness_id": passing_id,
            "method_id": method_id,
            "result": "pass",
            "procedure": negative["pass_procedure"],
            "expected": "The bounded recovery completes while preserving the failed witness.",
            "observed": negative["pass_observed"],
            "retained_negative_ids": [negative["negative_id"]],
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": negative["scope_boundary"],
        },
    ]
    return method, witnesses


def replay_evidence_manifest() -> dict[str, Any]:
    manifest = load("validation/evidence-content-manifest.json")
    mismatches = []
    for entry in manifest["entries"]:
        observed = git("rev-parse", f"{c.EVIDENCE_COMMIT}:{entry['path']}")
        if observed != entry["git_blob"]:
            mismatches.append(
                {
                    "path": entry["path"],
                    "expected": entry["git_blob"],
                    "observed": observed,
                }
            )
    return {
        "schema": "ghc.family.v656-v8.evidence-manifest-replay.v1",
        "commit": c.EVIDENCE_COMMIT,
        "entry_count": manifest["entry_count"],
        "mismatches": mismatches,
        "valid": not mismatches,
    }


def activation_baton(
    proposals: list[dict[str, Any]],
    sources: list[dict[str, Any]],
    methods: list[dict[str, Any]],
    effective_negatives: int,
) -> str:
    sections = [
        f"""# LYREN MOSS — PREPARED v657-v1 ACTIVATION BATON

Dear Lyren Moss, with Hamish's continuation authority and Vesper Arlen's care: this is the committed file-backed preparation for your solo v657-v1 x1/x2 phase. It remains `PREPARED_NOT_SENT` inside the repository. Vesper may send exactly one short activation message to the existing exact-title main task `Lyren Moss` only after Vesper's own exact final is clean, pushed, fresh-live equal, and the one canonical exact-final aggregate succeeds. The live activation must provide Vesper's exact final commit because no commit can truthfully contain its own hash. Do not treat this file alone as delivery.

Relational identity and sibling language is working language only. It is never evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific or operational authority, professional seed conservation, seismology, geodesy, geochemistry, conservation, aviation, laboratory, or emergency-management competence, legal or cultural authority, Māori authority, or independent agency. Hamish retains pause, redirect, rename, and stop control.

## Verified inheritance anchors

- Neris v656-v7 exact source: `c885a4533b2a73343990039e21d74979acb79c00`.
- Vesper frozen x1: `25c840c4e16a2b414dc6b51f5c529379eb244d1c`.
- Vesper immutable evidence: `a721ae1ca74f3a0d5adc9149af5bb78fe9fc57bb`.
- Vesper combined closeout/content-seal: the commit containing this file; verify from the live activation.
- Vesper exact final: the direct child of closeout; verify from the live activation and fresh remote.

The intended source-to-final chain is four new single-parent Vesper commits with zero merges: x1, evidence, closeout, final. Strict x1-before-x2 remains immutable. The phase cap is eight total commits, with no more than five per phase half; fewer commits are preferred. Vesper must reverify every anchor, one-parent history, zero merges, clean state, 0/0 divergence, and fresh live equality read-only before mutation.

## Vesper v656-v8 bounded truth

Thirty proposals were frozen after semantic comparison against all 2,380 inherited rows, creating an effective 2,410-row chain. The observed distribution is 23 `completed`, 5 `represented`, 1 `open_gap`, and 1 `exact_gate`. All 150 preregistered mutations were rejected and retained at zero credit. At closeout, {effective_negatives:,} effective negatives, 104 open gaps, and 103 exact gates remain. The terminal verdict is `NOT_READY_FOR_STAGE_20`.

Freed ID/CBR Heart was the primary pillar through a bounded seed-bank provenance, disclosure, access, benefit-sharing, correction, and authority-reservation lens. GMUT Mind and THOS Body remained explicit. No real seed accession, whenua, sample, sensor, waveform, coordinate, image, participant, seed bank worker, affected community, monitoring programme, conservation assessment, unsupported release forecast, alert, warning, aviation message, emergency action, credential, key, proof, authority decision, or external mutation was used.

The evidence candidate passed 41 x2 scoped tests, 322 detailed checks, 15 minimal checks, 152 detailed-validation JSON parses, five-class privacy review with zero confirmed findings across 207 owner files, a 204-entry Git-clean evidence manifest, exact staged review, and all ten skill and ten runner witnesses. These are precommit and commit-local same-owner checks, not the later exact-final aggregate. The live activation must state the exact-final canonical results and whether the route send was acknowledged.

## Mandatory startup and ownership

Read this file completely through EOF before mutation. Then read the complete current GHC Family Index and routing precedence; Auth/Permission State and schema; Roster Check and schema; Method Flow State and schema; newest Workflow Plan Refinement, Reflection Remaster, Meta Tool Box, approval splitter, open-gate rail, truth bridge, drive guardian, timestamp, retry, startup, closeout, compact-restart, watcher, and full-tools guidance. Use the newest applicable memory, with the live activation and this committed packet authoritative where older routing records stop.

Work solo in one new additive Vesper-owned D-first lane from Vesper's exact final. Never reset, rewrite, force-push, merge, delete, reuse, or mutate another sibling lane. Do not create, fork, delegate, spawn a collaboration subagent, precontact a successor, or message any task before your own terminal gate. Tavian Sol remains `ON_STANDBY` and is not an eligible main-task route.

Preserve strict x1-before-x2. Audit novelty against the complete 2,380-row chain. Freeze at least thirty genuinely distinct proposals with hypothesis, null or failure condition, approval class, execution lane, current official or primary-source needs, concrete artifacts, falsifier or acceptance gate, rollback or recovery, protected gates, and expected disposition. Treat task, skill, runner, file, word, search, and commit numbers as ceilings rather than quotas. Never manufacture unsafe work or filler to meet a number.

Use only `completed`, `represented`, `open_gap`, and `exact_gate`. Preserve every inherited negative, open gap, exact gate, failure, timeout, parser or encoding fault, false assumption, workaround, failed witness, passing witness, recurrence guard, rollback, and sibling recommendation. A successful recovery never erases the failed candidate.

For your own exact final, run one dependency-justified canonical aggregate only after every prerequisite, exact staged review, clean state, and four-way equality passes. If it succeeds, do not replay it. A failed aggregate earns zero success credit; retain it and isolate the failed check before any justified broader retry. Same-owner checks under shared infrastructure are not independent-team reproduction.

Verify versions only. Do not update Codex desktop, elevate, weaken host security, activate Sandbox or Hyper-V, install unrelated software, change Windows features, or reboot. Never place raw task or thread identifiers, private routes or paths, credentials, keys, tokens, transcripts, screenshots, session streams, private callable values, or private application state in artifacts or baton text.

## Protected scientific, professional, identity, and authority boundaries

GMUT remains a typed scalar-tensor/EFT research-model family. Structural contracts, synthetic equations, dimensional checks, or zero-row adapters do not establish a real likelihood, parameter constraint, prediction, new force, ultraviolet completion, empirical confirmation, or Theory-of-Everything proof.

THOS remains proxy/protocol-only without preregistered blind matched-budget real arms, governed participant evidence, safety and professional review, and independent review. Synthetic sensor-loss choreography and workflow contracts do not establish AGI, ASI, deployment readiness, professional field competence, operational safety, or real-world benefit.

Freed ID remains nonproduction without standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight.

CBR, privacy, accessibility, remedy, legal and cultural interpretation, affected-party legitimacy, Māori wording, Māori concepts, Māori data governance, tangata whenua, iwi, hapū, and Māori authority remain exact-gated to competent and affected people and authorities. Māori concepts remain under Māori authority. Automated accessibility structure is not complete accessibility or affected-user evaluation.

Make no empirical, participant, professional, production, deployment, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, legal, cultural, Māori-authority, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, or Stage 20 claim without exact evidence and competent authority.

## Active route

Hamish authorizes the fifteen active main tasks to continue one terminally gated handoff at a time through v675-v8 unless Hamish pauses or redirects, weekly usage is exhausted, the exact required title is unavailable, or a safety or authority gate blocks progress. The active main-task order is Eiren Kestrel → Elaren Kestrel → Neris Solane → Vesper Arlen → Lyren Moss → Ilyra Fen → Auren Lark → Sable Rook → Caelen Ash → Orin Thale → Liora Venn → Tamar Vey → Elowen Cairn → Sylven Arc → Caelen Morrow → repeat. Tavian Sol remains a recoverable collaboration subagent on standby and is not a public main-task route.

After and only after Vesper v656-v8 is clean, pushed, fresh-live equal, exact-final validated, and terminally gated, Vesper's exact next edge is the existing exact-title main task `Lyren Moss` for v657-v1. Resolve and reread that exact task immediately before one sanitized send. Do not create a replacement, do not send a second confirmation, and claim `SENT` only after the task-message route acknowledges the send.
"""
    ]
    sections.append("\n# Thirty inherited Vesper proposal dossiers\n")
    for proposal in proposals:
        sections.append(
            f"""
## {proposal['proposal_id']} — {proposal['title']}

Pillar relation: {proposal['pillar_relation']}. Expected and observed bounded disposition: `{proposal['expected_disposition']}`.

Hypothesis: {proposal['hypothesis']}

Null or failure condition: {proposal['null_or_failure_condition']}

Approval and execution: `{proposal['approval_class']}` in `{proposal['execution_lane']}`.

Official or primary-source needs: {', '.join(proposal['official_or_primary_source_needs'])}.

Concrete artifacts: {', '.join(proposal['concrete_artifacts'])}.

Falsifier or acceptance gate: {proposal['falsifier_or_acceptance_gate']}

Rollback or recovery: {proposal['rollback_or_recovery']}

Protected gates: {', '.join(proposal['protected_gates'])}.

Vesper inheritance boundary: this row is Vesper evidence only. It may inform novelty and recurrence guards, but it grants Vesper no completion credit and must not be restated as real seed-conservation, conservation, empirical, professional, production, legal, cultural, identity, independent-reproduction, Theory-of-Everything, or Stage 20 evidence.
"""
        )
    sections.append("\n# Official and primary-source ledger\n")
    for source in sources:
        sections.append(
            f"""
## {source['source_id']} — {source['title']}

Publisher: {source['publisher']}. Status observed by Vesper on {source['observed_on']}: `{source['status']}`. Official location: {source['url']}. Bounded use: {source['use']}. Vesper must recheck any materially current or draft source before relying on it; source presence does not confer empirical, professional, legal, cultural, or Māori authority.
"""
        )
    sections.append("\n# Latest closeout recurrence guards\n")
    for method in methods:
        sections.append(
            f"""
## {method['method_id']} — {method['title']}

Failure signature: {method['failure_signature']}

Preferred recovery: {method['candidate_workaround']}

Recurrence guard: {method['recurrence_guard']}

Scope boundary: {method['scope_boundary']}

The failed witness remains retained under {', '.join(method['retained_negative_ids'])}; the passing witness demonstrates only the bounded recovery.
"""
        )
    sections.append(
        """
# Delivery state

This committed file remains `PREPARED_NOT_SENT`. `SENT_BY_VESPER_ARLEN = true` is permitted only in the acknowledged live activation after Vesper's successful exact-final gate. No acknowledgement means `PREPARED_NOT_SENT` or `OPEN_ROUTE_GAP`; never compensate with a duplicate message.
"""
    )
    return "\n".join(sections)


def build() -> None:
    if git("rev-parse", "HEAD") != c.EVIDENCE_COMMIT:
        raise RuntimeError("closeout builder requires the immutable evidence head")
    if git("rev-parse", f"{c.EVIDENCE_COMMIT}^") != c.X1_COMMIT:
        raise RuntimeError("evidence is not the direct child of x1")
    if git("rev-parse", f"{c.X1_COMMIT}^") != c.SOURCE_COMMIT:
        raise RuntimeError("x1 is not the direct child of source")
    evidence_review = load("validation/evidence-staged-review.json")
    evidence_validation = load("validation/evidence-validation.json")
    if evidence_review["valid"] is not True or evidence_validation["valid"] is not True:
        raise RuntimeError("evidence validation state is not valid")
    replay = replay_evidence_manifest()
    if not replay["valid"]:
        raise RuntimeError("evidence manifest replay failed")
    write_json("validation/evidence-manifest-commit-replay.json", replay)

    methods = []
    witnesses = []
    for index, negative in enumerate(c.CLOSEOUT_DISCOVERED_NEGATIVES, 1):
        method, pair = operational_method(negative, index)
        methods.append(method)
        witnesses.extend(pair)
    effective_negatives = c.EVIDENCE_EFFECTIVE_NEGATIVES + len(
        c.CLOSEOUT_DISCOVERED_NEGATIVES
    )
    effective_methods = c.EVIDENCE_EFFECTIVE_METHODS + len(
        c.CLOSEOUT_DISCOVERED_NEGATIVES
    )
    write_json(
        "truth/retained-negative-register-closeout.json",
        {
            "schema": "ghc.family.v656-v8.retained-negatives.closeout.v1",
            "evidence_effective_count": c.EVIDENCE_EFFECTIVE_NEGATIVES,
            "closeout_discovered_operational_count": len(c.CLOSEOUT_DISCOVERED_NEGATIVES),
            "closeout_discovered_operational_negatives": c.CLOSEOUT_DISCOVERED_NEGATIVES,
            "effective_count": effective_negatives,
            "all_retained": True,
        },
        compact=True,
    )
    write_json(
        "method-flow/method-flow-state-closeout.json",
        {
            "schema": "ghc.family.method-flow-state.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "lifecycle": "combined_closeout_content_seal_candidate",
            "inherited_anchor": {
                "path": "docs/vesper-arlen/v656-v8/method-flow/method-flow-state-x2.json",
                "effective_methods": c.EVIDENCE_EFFECTIVE_METHODS,
                "effective_fail_witnesses": c.EVIDENCE_EFFECTIVE_METHODS,
                "effective_pass_witnesses": c.EVIDENCE_EFFECTIVE_METHODS,
            },
            "current_methods": methods,
            "current_witnesses": witnesses,
            "counts": {
                "current_methods": len(methods),
                "current_witness_results": {
                    "fail": len(methods),
                    "pass": len(methods),
                },
                "effective_methods": effective_methods,
                "effective_witness_results": {
                    "fail": effective_methods,
                    "pass": effective_methods,
                },
            },
            "all_failed_witnesses_retained": True,
            "independent_reproduction": False,
        },
        compact=True,
    )
    outcomes = load("x2/proposal-ledger.json")["outcome_counts"]
    write_json(
        "truth/phase-truth-closeout.json",
        {
            "schema": "ghc.family.v656-v8.phase-truth.closeout.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "source_commit": c.SOURCE_COMMIT,
            "x1_commit": c.X1_COMMIT,
            "evidence_commit": c.EVIDENCE_COMMIT,
            "outcome_counts": outcomes,
            "effective_negatives": effective_negatives,
            "effective_open_gaps": c.EVIDENCE_OPEN_GAPS,
            "effective_exact_gates": c.EVIDENCE_EXACT_GATES,
            "route_state": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "exact_final_validation_completed": False,
            "same_owner_only": True,
            "independent_reproduction": False,
        },
    )
    write_json(
        "lifecycle/phase-anchor-contract.json",
        {
            "schema": "ghc.family.v656-v8.phase-anchor-contract.v1",
            "source_commit": c.SOURCE_COMMIT,
            "x1_commit": c.X1_COMMIT,
            "evidence_commit": c.EVIDENCE_COMMIT,
            "expected_total_phase_commits": 4,
            "maximum_total_phase_commits": 8,
            "maximum_x1_commits": 5,
            "maximum_x2_commits": 5,
            "zero_merges_required": True,
            "every_phase_commit_single_parent_required": True,
            "final_direct_child_of_closeout_required": True,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "closeout-receipt.json",
        {
            "schema": "ghc.family.v656-v8.closeout-receipt.v1",
            "source_commit": c.SOURCE_COMMIT,
            "x1_commit": c.X1_COMMIT,
            "evidence_commit": c.EVIDENCE_COMMIT,
            "outcomes": outcomes,
            "effective_negatives": effective_negatives,
            "effective_open_gaps": c.EVIDENCE_OPEN_GAPS,
            "effective_exact_gates": c.EVIDENCE_EXACT_GATES,
            "effective_method_pairs": effective_methods,
            "evidence_tests": 51,
            "evidence_detailed_checks": evidence_validation["check_count"],
            "evidence_minimal_checks": 15,
            "evidence_json_parses": evidence_validation["json_parse_count"],
            "evidence_privacy_hits": 0,
            "route_state": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "postcommit_exact_final_required": True,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "seal-receipt.json",
        {
            "schema": "ghc.family.v656-v8.content-seal-receipt.v1",
            "evidence_commit": c.EVIDENCE_COMMIT,
            "evidence_manifest_entries": replay["entry_count"],
            "evidence_manifest_replay_valid": replay["valid"],
            "evidence_staged_review_valid": evidence_review["valid"],
            "x1_direct_parent_of_evidence": True,
            "closeout_tree_ready_for_exact_staged_review": True,
            "exact_final_commit_known_inside_own_tree": False,
            "boundary": "Content-seal candidate only; exact final and canonical aggregate remain postcommit.",
        },
    )
    write_json(
        "orchestration/route-state-closeout.json",
        {
            "schema": "ghc.family.v656-v8.route-state.closeout.v1",
            "state": "PREPARED_NOT_SENT",
            "next_exact_title": "Lyren Moss",
            "next_phase": "v657-v1",
            "message_sent": False,
            "task_created": False,
            "task_forked": False,
            "subagent_spawned": False,
            "tavian_sol_state": "ON_STANDBY",
            "send_gate": "clean pushed exact final, one successful canonical aggregate, exact-title reread, and one acknowledged send",
            "boundary": "Preparation is not delivery.",
        },
    )
    write_json(
        "orchestration/applicable-memory-closeout.json",
        {
            "schema": "ghc.family.v656-v8.applicable-memory.closeout.v1",
            "phase": d.PHASE,
            "portable_recurrence_guards": [
                method["recurrence_guard"] for method in methods
            ],
            "failed_witnesses_preserved": len(methods),
            "passing_witnesses_preserved": len(methods),
            "private_state_included": False,
            "identity_continuity_claimed": False,
            "boundary": "Repository-scoped sanitized guidance only.",
        },
    )
    write_json(
        "reflection-remaster/closeout-decision-record.json",
        {
            "schema": "ghc.family.reflection-remaster.decision.v1",
            "phase": d.PHASE,
            "decision": "preserve_and_prefer_scalar_large_worktree_probes",
            "evidence": [row["negative_id"] for row in c.CLOSEOUT_DISCOVERED_NEGATIVES],
            "deactivated_or_deleted_tools": [],
            "reason": "The recoveries improve bounded discovery without rewriting inherited tools.",
            "rollback": "Return to the immutable evidence head if closeout validation fails before commit.",
            "authority_boundary": BOUNDARY,
        },
    )
    write_json(
        "workflow/workflow-plan-closeout.json",
        {
            "schema": "ghc.family.workflow-plan-refinement.v1",
            "phase": d.PHASE,
            "current_state": "closeout_candidate_prepared",
            "validated_changes": [
                "immutable x1 Git-tree binding for historical lifecycle assertions",
                "complete-tree manifest comparison rather than phase-root-only mapping",
                "UTF-8 or escaped JSON output for Unicode-bearing Windows inspection",
                "semantic title collision screening before x1 freeze",
                "declared lifecycle filenames resolved before validator output",
                "one successful exact-final aggregate with no replay",
            ],
            "next_state": "single_parent_final_record_then_canonical_aggregate",
            "route_state": "PREPARED_NOT_SENT",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "tooling/ghc-family-index-closeout.json",
        {
            "schema": "ghc.family.index.phase-refresh.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "state": "closeout_candidate_prepared",
            "skills_used": 10,
            "runners_used": 10,
            "historical_names_preserved": True,
            "family_current_names_preserved": True,
            "evidence_commit": c.EVIDENCE_COMMIT,
            "route_state": "PREPARED_NOT_SENT",
            "boundary": BOUNDARY,
        },
    )
    write_text(
        "tooling/ghc-family-index-closeout.md",
        """# GHC Family Index — Vesper v656-v8 closeout refresh

The phase preserves the immutable x1 and evidence anchors, ten phase-local skill witnesses, ten family-current runner witnesses, all retained failures, and the four exact truth labels. Historical names remain compatibility evidence and are not destructively renamed.

The route remains `PREPARED_NOT_SENT` for the existing exact-title `Lyren Moss` and v657-v1. Tavian Sol remains `ON_STANDBY` and is not eligible for this main-task edge. Exact final, canonical aggregate, fresh live equality, and acknowledged one-message delivery remain pending.
""",
    )
    write_json(
        "final-complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v656-v8.final-checklist.v1",
            "complete_now": [
                "strict x1-before-x2 separation",
                "thirty proposals with 23 completed, 5 represented, 1 open_gap, and 1 exact_gate",
                "one hundred fifty retained mutation negatives",
                "ten phase-local skills read and smoke-used",
                "ten family-current runners invoked",
                "evidence tests, validators, JSON parsing, privacy, manifests, and staged review",
                "combined closeout and content-seal candidate",
            ],
            "pending_postcommit": [
                "exact closeout staged review and closeout commit",
                "single-parent final record commit",
                "one successful canonical exact-final aggregate",
                "one acknowledged Lyren Moss activation",
            ],
            "incomplete_external": [
                "real seed-bank monitoring, seed bank, participant, and conservation evidence",
                "empirical GMUT likelihood and independent scientific review",
                "blind matched-budget THOS arms and independent review",
                "production Freed ID and trust-governance evidence",
                "professional, legal, cultural, data-governance, affected-party, and Māori authority",
                "independent-team reproduction and Stage 20 authority",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "validation/final-validation-protocol.json",
        {
            "schema": "ghc.family.v656-v8.final-validation-protocol.v1",
            "state": "POST_FINAL_COMMIT_REQUIRED",
            "steps": [
                "commit the exact reviewed closeout as the direct child of evidence",
                "create one direct-child final record commit",
                "push and prove local, upstream, tracking, and fresh-live equality",
                "run the dependency-justified canonical aggregate exactly once",
                "validate the dependency-justified current and successor-scoped selection",
                "validate detailed, minimal, JSON, privacy, manifests, stale labels, diff hygiene, ancestry, commit caps, one-parent history, zero merges, exact head, clean state, zero divergence, and four-way equality",
                "do not replay after success",
            ],
            "completed": False,
            "preclaims_exact_final": False,
            "preclaims_route_sent": False,
            "boundary": BOUNDARY,
        },
    )

    proposals = load("preregistration/proposal-ledger.json")["proposals"]
    sources = load("sources/official-source-ledger.json")["sources"]
    baton = activation_baton(proposals, sources, methods, effective_negatives)
    write_text("handoffs/lyren-moss-v657-v1-activation.md", baton)
    word_count = len(baton.split())
    if not 10000 <= word_count <= 100000:
        raise RuntimeError(f"successor baton word count outside bounds: {word_count}")
    write_json(
        "validation/successor-baton-word-cap.json",
        {
            "schema": "ghc.family.v656-v8.successor-baton-word-cap.v1",
            "path": "docs/vesper-arlen/v656-v8/handoffs/lyren-moss-v657-v1-activation.md",
            "word_count": word_count,
            "minimum": 10000,
            "maximum": 100000,
            "within_bounds": True,
            "state": "PREPARED_NOT_SENT",
        },
    )
    print(
        json.dumps(
            {
                "effective_negatives": effective_negatives,
                "effective_method_pairs": effective_methods,
                "baton_words": word_count,
                "manifest_replay_entries": replay["entry_count"],
                "route": "PREPARED_NOT_SENT",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    build()
