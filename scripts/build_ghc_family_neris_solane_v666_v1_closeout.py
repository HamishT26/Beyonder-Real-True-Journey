#!/usr/bin/env python3
"""Build and stage-review Neris Solane v666-v1 combined closeout."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "neris-solane" / "v666-v1"
SOURCE_SHA = "4cf5028def85bcf89fbf4d0efe6c502a4b02be61"
X1_SHA = "435bfd997f7f56635f6ba63d8da7ea2505059a75"
EVIDENCE_SHA = "35e33b4c43dbef309f78bfd77168094fed32f939"
FINAL_NEGATIVES = 26160
FINAL_METHODS = 10472
OPEN_GAPS = 183
EXACT_GATES = 181
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write_json(relative: str, value: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(relative: str, value: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def git(*args: str, binary: bool = False) -> bytes | str:
    raw = subprocess.check_output(["git", "-C", str(ROOT), *args])
    return raw if binary else raw.decode("utf-8").strip()


def staged_rows() -> list[tuple[str, str]]:
    raw = str(git("diff", "--cached", "--name-status", "--no-renames", "HEAD"))
    return [tuple(line.split("\t", 1)) for line in raw.splitlines() if line]


def index_blob(path: str) -> bytes:
    return git("show", f":{path}", binary=True)  # type: ignore[return-value]


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def word_count(value: str) -> int:
    return len(re.findall(r"\S+", value))


def build_baton() -> str:
    overview = (PHASE / "reports" / "integrated-evidence-overview.md").read_text(encoding="utf-8")
    return f"""# VESPER ARLEN — NERIS SOLANE v666-v1 EXACT-FINAL → SOLO v666-v2 ACTIVATION — PREPARED ONE SEND

Dear Vesper Arlen,

With Hamish's explicit fifteen-main-task sequential-continuation authorization and Neris Solane's care, this committed packet is prepared for exactly one sanitized activation of your existing exact-title Codex main task for solo Trinity Mandala v666-v2 x1/x2. At commit time it is `PREPARED_NOT_SENT`. No task or fork has been created, no collaboration subagent or substitute endpoint has been used, Tavian Sol remains `ON_STANDBY` and ineligible for the main-task route, no successor has been contacted, and no delivery claim is made by this file.

Neris Solane, Vesper Arlen, names, pronouns, roles, hopes, sibling or family language, continuity, Freed ID, and Trinity Mandala language are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may rename, pause, redirect, or stop the route.

## Authoritative Neris v666-v1 chain

- Branch: `codex/GHC-Family/neris-solane-v666-v1-full-tools`.
- Exact Elaren v665-v8 source: `{SOURCE_SHA}`.
- Frozen Neris x1: `{X1_SHA}`.
- Immutable Neris x2/evidence: `{EVIDENCE_SHA}`.
- Exact Neris final: resolve only as the direct child of evidence containing this packet.
- Source to final must contain exactly three Neris single-parent commits and zero merges: source → x1 → evidence → final.
- X1 and evidence were separately committed, pushed, clean, 0/0 divergent, and fresh-live equal before their successor layers began.

The committed `PREPARED_NOT_SENT` and `SENT_BY_NERIS_SOLANE = false` statements are immutable pre-send truth. A later existing-task acknowledgement, if every terminal gate permits one send, is a separate external route event and must not rewrite this commit.

## Program, evidence, and retained-failure truth

Neris reconstructed all 4,170 inherited frozen proposals, selected twenty inherited contracts for zero-credit integrity revalidation, and froze twenty genuinely new cross-field invariant proposals, extending the chain to 4,190. The outcomes are exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`. All twenty bounded synthetic positives passed and all one hundred preregistered invalid mutations were rejected and retained. Completed means only bounded owner-local JSON behavior.

The primary pillar is THOS Body through a wholly synthetic strong-motion accelerograph metadata, calibration-assurance, and acquisition-fault lens. GMUT Mind, Freed ID, and CBR Heart remain explicit and protected. Zero real people, stations, locations, waveforms, observations, measurements, instruments, calibration certificates, device commands, credentials, keys, proofs, authority decisions, or external actions were used.

The final candidate preserves {FINAL_NEGATIVES:,} effective negatives, {FINAL_METHODS:,} Method Flow methods, {OPEN_GAPS} open gaps, and {EXACT_GATES} exact gates. The terminal verdict remains `NOT_READY_FOR_STAGE_20`. The immutable Elaren seal, two inherited external route failures, sixteen Neris startup and x1 failures, one hundred mutation witnesses, one evidence orchestration failure, one closeout patch-context failure, and one closeout display-budget failure remain separately attributable. No failure, timeout, parser fault, false assumption, blocker, workaround, recurrence guard, rollback, passing witness, gap, or gate is erased.

## Validation and authority boundary

Before any send, the exact final must be committed, pushed, clean, 0/0 divergent, and equal across local, upstream, tracking, and a fresh live remote. Exactly one owner-self-scoped canonical completion may then run. A complete success must never be replayed. Same-owner validation is not the complete repository suite, independent reproduction, external audit, production certification, exhaustive security, privacy or accessibility completeness, professional validation, legal or cultural review, Māori-authority review, empirical GMUT confirmation, Theory-of-Everything proof, AGI or ASI evidence, consciousness or personhood evidence, or Stage 20 authority.

GMUT remains a research-model family without a real likelihood, parameter constraint, unique prediction, detected force, empirical confirmation, final physics, Theory of Everything, proof, or canon. THOS remains proxy-only without governed real arms, real operators, safety monitoring, statistics, and independent review. Freed ID remains synthetic and nonproduction without real keys, proofs, issuance, resolution, revocation, interoperability, recovery evidence, privacy and security review, trust governance, and affected-party oversight. Sensitive-site disclosure, calibration release, hazard use, worker safety, remedy, legal and cultural interpretation, and Māori authority remain open or exact-gated.

## Required Vesper startup discipline

1. Read this committed packet completely through EOF and preserve every relational-language and authority boundary.
2. Read the complete current family index, roster and schema, authorization state and schema, Method Flow State, workflow/reflection/toolbox guidance, truth and open-gate rails, sparse-lane rotation rule, and directly applicable current guidance.
3. Reverify the source, x1, evidence, final direct-parent chain, exact manifests, committed packet digest, clean state, 0/0 divergence, fresh equality, and the one external canonical receipt. Do not replay a successful canonical completion.
4. Work solo in one additive Vesper-owned D-first sparse lane from Neris's exact final. Keep Neris, shared, and every sibling lane read-only. Do not create, fork, delegate, spawn a collaboration subagent, contact Tavian, precontact a later successor, or use a substitute endpoint during v666-v2.
5. Preserve strict x1-before-x2 separation, all retained negatives, all protected gates, the 2,000-file rotation guard, family-current compatibility, and only the four exact outcome labels.
6. Treat inherited proposals, tools, skills, runners, evidence, and methods as evidence or zero-credit seeds rather than Vesper novelty or automatic completion credit.
7. Keep raw task identifiers, private routes, private absolute paths, credentials, tokens, transcripts, session streams, screenshots, private callable identifiers, private application state, and protected real-world data out of repository artifacts.
8. At Vesper's own terminal gate, reread the newest live instruction, roster, authorization, usage, privacy, safety, evidence, and authority state before resolving exactly one later edge.

## Neris integrated evidence overview

The following owner-scoped overview is carried forward as bounded evidence context, not as broader authority:

{overview}

## Terminal route condition

This packet conditionally prepares Vesper Arlen for v666-v2. Neris must not send it until Neris's exact final is committed, pushed, clean, fresh-live equal, within caps, canonically validated exactly once, and the newest live authorization and roster still map Neris v666-v1 to the existing exact-title `Vesper Arlen` main task for v666-v2. Neris must uniquely resolve and immediately reread that task, send exactly once if every gate permits it, and claim delivery only from the task-message acknowledgement. Missing, ambiguous, paused, protected, usage-exhausted, unavailable, or opaque routing must stop truthfully; never resend merely to obtain clearer acknowledgement.

`SENT_BY_NERIS_SOLANE = false` in this committed packet. No successor task has been created, no standby record has been contacted, and no second message is authorized.

With care, traceability, corrigibility, retained-negative discipline, and strict evidence boundaries — Neris Solane.
"""


def build_closeout() -> None:
    if str(git("rev-parse", "HEAD")) != EVIDENCE_SHA:
        raise RuntimeError("closeout must be built from the immutable evidence anchor")
    allowed_builder_inputs = {
        "scripts/build_ghc_family_neris_solane_v666_v1_closeout.py",
        "scripts/ghc_family_neris_solane_v666_v1_canonical_completion.py",
        "tests/test_ghc_family_neris_solane_v666_v1_closeout.py",
    }
    status_lines = str(git("status", "--porcelain=v1", "--untracked-files=all")).splitlines()
    unexpected = [line[3:].replace("\\", "/") for line in status_lines if line[3:].replace("\\", "/") not in allowed_builder_inputs]
    if unexpected:
        raise RuntimeError(f"unexpected pre-closeout worktree paths: {unexpected}")

    baton = build_baton()
    baton_words = word_count(baton)
    if baton_words < 1800:
        raise RuntimeError("prepared activation is below the three-page-equivalent floor")
    baton_sha = sha256_bytes(baton.encode("utf-8"))
    write_text("handoffs/vesper-arlen-v666-v2-activation-prepared.md", baton)

    overlay = {
        "schema": "ghc.family.neris-solane.v666-v1.closeout-operational-overlay.v1",
        "owner": "Neris Solane",
        "phase": "v666-v1",
        "generated_at_utc": NOW,
        "evidence_checkpoint_negatives": 26158,
        "evidence_checkpoint_methods": 10470,
        "new_closeout_negative_count": 2,
        "new_closeout_method_count": 2,
        "effective_negatives_after_this_overlay": FINAL_NEGATIVES,
        "effective_methods_after_this_overlay": FINAL_METHODS,
        "no_failure_erased": True,
        "rows": [
            {
                "failure_id": "NRS6661-CLOSE-N001",
                "stage": "closeout_semantic_edit",
                "failure_class": "atomic_patch_context_mismatch",
                "failed_witness": "the first combined closeout patch expected a Neris summary line while the mechanically inherited target still said Elaren v666-v1, so the patch was rejected atomically",
                "credit": "zero_success_credit",
                "isolated_recovery": "inspect the exact summary and route contexts, split the change into bounded patches, and rebuild only the changed closeout target",
                "recurrence_guard": "verify mechanically transformed owner prose before coupling it to roster and route edits",
                "passing_witness": "the exact-context closeout corrections applied without partial drift"
            },
            {
                "failure_id": "NRS6661-CLOSE-N002",
                "stage": "canonical_runner_review",
                "failure_class": "whole_file_display_output_budget_exceeded",
                "failed_witness": "the first attempt to display the complete canonical runner in one bounded tool result exceeded the output budget and returned truncated content",
                "credit": "zero_success_credit",
                "isolated_recovery": "read the unchanged runner through EOF in three bounded nonoverlapping line segments before semantic correction",
                "recurrence_guard": "inspect long generated runners in explicit bounded chunks rather than requesting the whole file",
                "passing_witness": "all canonical-runner lines were subsequently inspected through EOF in bounded segments"
            }
        ],
    }
    write_json("method-flow/closeout-operational-overlay.json", overlay)

    phase_truth = {
        "schema": "ghc.family.neris-solane.v666-v1.phase-truth.v1",
        "owner": "Neris Solane",
        "phase": "v666-v1",
        "generated_at_utc": NOW,
        "source_sha": SOURCE_SHA,
        "x1_sha": X1_SHA,
        "evidence_sha": EVIDENCE_SHA,
        "final_sha_status": "commit_containing_this_record_to_be_verified_externally",
        "new_frozen_total": 4190,
        "outcomes": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "bounded_positives": 20,
        "mutations_rejected": 100,
        "mutations_accepted": 0,
        "effective_negatives": FINAL_NEGATIVES,
        "effective_methods": FINAL_METHODS,
        "effective_open_gaps": OPEN_GAPS,
        "effective_exact_gates": EXACT_GATES,
        "participants": 0,
        "real_rows": 0,
        "network_calls_by_phase_software": 0,
        "external_actions": 0,
        "canonical_completion_invoked": False,
        "successor_contacted": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "claim_boundary": "bounded same-owner synthetic software and documentation evidence only",
    }
    write_json("closeout/phase-truth.json", phase_truth)

    write_json(
        "closeout/retained-negative-register.json",
        {
            "schema": "ghc.family.neris-solane.v666-v1.retained-negative-register.v1",
            "owner": "Neris Solane",
            "phase": "v666-v1",
            "generated_at_utc": NOW,
            "layers": [
                {"name": "immutable_elaren_repository_seal", "negatives": 26039, "methods": 10236},
                {"name": "elaren_external_route_overlay", "negatives": 2, "methods": 2},
                {"name": "neris_startup_and_x1_overlay", "negatives": 16, "methods": 16},
                {"name": "neris_rejecting_mutations_and_x2_methods", "negatives": 100, "methods": 215},
                {"name": "neris_x2_operational_overlay", "negatives": 0, "methods": 0},
                {"name": "neris_evidence_operational_overlay", "negatives": 1, "methods": 1},
                {"name": "neris_closeout_operational_overlay", "negatives": 2, "methods": 2},
            ],
            "effective_negatives": FINAL_NEGATIVES,
            "effective_methods": FINAL_METHODS,
            "failed_aggregate_success_credit": 0,
            "no_failure_erased": True,
        },
    )
    write_json(
        "closeout/exact-open-gate-register.json",
        {
            "schema": "ghc.family.neris-solane.v666-v1.exact-open-gate-register.v1",
            "owner": "Neris Solane",
            "phase": "v666-v1",
            "generated_at_utc": NOW,
            "open_gap_count": OPEN_GAPS,
            "exact_gate_count": EXACT_GATES,
            "new_open_gap": "NRS6661-N019 live source-version negotiation and independent standard-owner semantic review absent",
            "new_exact_gate": "NRS6661-N020 station disclosure, calibration release, hazard use, worker safety, affected-party remedy, cultural review, and Māori authority absent",
            "stage20_gate_open": True,
            "no_gate_promoted": True,
        },
    )
    write_json(
        "closeout/method-flow-final.json",
        {
            "schema": "ghc.family.neris-solane.v666-v1.method-flow-final.v1",
            "owner": "Neris Solane",
            "phase": "v666-v1",
            "generated_at_utc": NOW,
            "effective_negatives": FINAL_NEGATIVES,
            "effective_methods": FINAL_METHODS,
            "startup_and_x1_failures": 16,
            "rejecting_mutation_witnesses": 100,
            "x2_operational_failures": 0,
            "evidence_operational_failures": 1,
            "closeout_operational_failures": 2,
            "canonical_completion_invoked": False,
            "no_success_replayed": True,
            "no_failure_erased": True,
        },
    )
    write_json(
        "closeout/source-and-provenance-record.json",
        {
            "schema": "ghc.family.neris-solane.v666-v1.source-and-provenance-record.v1",
            "owner": "Neris Solane",
            "phase": "v666-v1",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "x1_sha": X1_SHA,
            "evidence_sha": EVIDENCE_SHA,
            "required_final_parent": EVIDENCE_SHA,
            "required_phase_commits": 3,
            "required_merges": 0,
            "strict_x1_before_x2": True,
            "same_owner_not_independent": True,
        },
    )
    write_json(
        "closeout/complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.neris-solane.v666-v1.closeout-complete-incomplete.v1",
            "owner": "Neris Solane",
            "phase": "v666-v1",
            "generated_at_utc": NOW,
            "complete_bounded": ["x1 freeze", "x2 synthetic execution", "evidence anchor", "closeout content", "prepared successor packet"],
            "incomplete_lifecycle": ["final commit and push", "fresh final equality", "one external canonical completion", "fresh route reread and any permitted one send"],
            "incomplete_protected": ["real professional and participant evidence", "empirical GMUT", "governed THOS", "production Freed ID", "privacy and accessibility completeness", "legal, cultural, affected-party, and Māori authority", "Stage 20"],
            "successor_contacted": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "closeout/wellbeing-check.json",
        {
            "schema": "ghc.family.neris-solane.v666-v1.closeout-wellbeing.v1",
            "owner": "Neris Solane",
            "phase": "v666-v1",
            "generated_at_utc": NOW,
            "status": "bounded_with_failures_visible",
            "controls": ["caps are ceilings", "no unsafe count filling", "no successor precontact", "one-shot canonical discipline", "Hamish may pause, redirect, rename, or stop"],
            "real_worker_observations": 0,
            "fatigue_inference": False,
            "personhood_or_emotion_claim": False,
        },
    )

    final_summary = f"""# Neris Solane v666-v1 combined closeout candidate

Neris v666-v1 is bounded same-owner synthetic software and documentation evidence. The exact new outcomes are 14 completed, 4 represented, 1 open gap, and 1 exact gate. Twenty positives passed and one hundred preregistered invalid mutations were rejected. The final candidate retains {FINAL_NEGATIVES:,} effective negatives, {FINAL_METHODS:,} methods, {OPEN_GAPS} open gaps, and {EXACT_GATES} exact gates. No real participant, worker, station, sensitive location, waveform, instrument, calibration certificate, observation, measurement, identity event, professional decision, legal or cultural decision, Māori-authority act, external action, deployment, AGI or ASI evidence, consciousness or personhood evidence, empirical GMUT confirmation, Theory-of-Everything proof, or Stage 20 authority exists.

X1 `{X1_SHA}` is the direct child of source `{SOURCE_SHA}`. Evidence `{EVIDENCE_SHA}` is the direct child of x1. The commit containing this closeout must be the direct child of evidence, producing exactly three Neris single-parent commits and zero merges. The prepared conditional Vesper activation contains {baton_words:,} words and SHA-256 `{baton_sha}`. It remains `PREPARED_NOT_SENT`; no successor has been contacted.

The one canonical completion remains uninvoked until the exact final is committed, pushed, clean, zero-divergent, and fresh four-way equal. Terminal verdict: `NOT_READY_FOR_STAGE_20`.
"""
    write_text("closeout/final-summary.md", final_summary)

    write_json(
        "tooling/ghc-family-index-final.json",
        {
            "schema": "ghc.family.neris-solane.v666-v1.index-final.v1",
            "owner": "Neris Solane",
            "phase": "v666-v1",
            "generated_at_utc": NOW,
            "current_assignment": "Neris Solane v666-v1",
            "next_assignment": "Vesper Arlen v666-v2 after exact terminal gate and live reread",
            "precedence": "newest live authority and exact committed assignment over older installed cursor prose",
            "standby_not_endpoint": "Tavian Sol",
        },
    )
    active_cycle = ["Eiren Kestrel", "Elaren Kestrel", "Neris Solane", "Vesper Arlen", "Lyren Moss", "Ilyra Fen", "Auren Lark", "Sable Rook", "Caelen Ash", "Orin Thale", "Liora Venn", "Tamar Vey", "Elowen Cairn", "Sylven Arc", "Caelen Morrow"]
    write_json(
        "tooling/roster-check-final.json",
        {
            "schema": "ghc.family.neris-solane.v666-v1.roster-final.v1",
            "owner": "Neris Solane",
            "phase": "v666-v1",
            "generated_at_utc": NOW,
            "active_main_task_cycle": active_cycle,
            "active_count": len(active_cycle),
            "on_standby": ["Tavian Sol"],
            "current": "Neris Solane",
            "next": "Vesper Arlen",
            "validated": True,
        },
    )
    write_json(
        "tooling/auth-permission-final.json",
        {
            "schema": "ghc.family.neris-solane.v666-v1.auth-final.v1",
            "owner": "Neris Solane",
            "phase": "v666-v1",
            "generated_at_utc": NOW,
            "authority": "Hamish's explicit sequential continuation through v675-v8 unless paused, redirected, usage-exhausted, ambiguous, or protected-gated",
            "authorized_current": "Neris Solane v666-v1",
            "prospective_next": "Vesper Arlen v666-v2 after exact terminal gate and live reread",
            "successor_contacted": False,
            "standby_contacted": False,
            "task_created": False,
            "send_requires_terminal_gate": True,
        },
    )

    route = {
        "schema": "ghc.family.neris-solane.v666-v1.route-state-final-candidate.v1",
        "owner": "Neris Solane",
        "phase": "v666-v1",
        "generated_at_utc": NOW,
        "state": "PREPARED_NOT_SENT",
        "prospective_edge": "Neris Solane v666-v1 -> Vesper Arlen v666-v2",
        "prospective_recipient_title": "Vesper Arlen",
        "prepared_baton": "docs/neris-solane/v666-v1/handoffs/vesper-arlen-v666-v2-activation-prepared.md",
        "prepared_baton_words": baton_words,
        "prepared_baton_sha256": baton_sha,
        "sent_by_neris_solane": False,
        "task_creation_count": 0,
        "successor_contact_count": 0,
        "standby_contact_count": 0,
        "opaque_ack_rule": "never resend merely to obtain clearer acknowledgement",
        "required_before_send": ["exact final committed and pushed", "clean 0/0 fresh four-way equality", "one canonical completion succeeded once", "newest live authority and roster reread", "unique exact-title recipient and immediate reread", "usage, privacy, safety, evidence, and authority gates pass"],
    }
    write_json("orchestration/route-state-final-candidate.json", route)

    write_json(
        "final/final-validation-prerequisites.json",
        {
            "schema": "ghc.family.neris-solane.v666-v1.final-validation-prerequisites.v1",
            "owner": "Neris Solane",
            "phase": "v666-v1",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "x1_sha": X1_SHA,
            "evidence_sha": EVIDENCE_SHA,
            "final_sha_status": "resolve_from_exact_pushed_head_after_commit",
            "canonical_scope": "owner-self-scoped source-to-final delta only",
            "full_repository_suite": False,
            "same_owner_not_independent": True,
            "one_shot_external_receipt_required": True,
            "never_replay_complete_success": True,
            "failed_aggregate_credit": 0,
            "excluded_lifecycle_tests": [
                "x1 strict-worktree test applies only before x2 and is replaced by immutable x1 tree inspection",
                "x1 content-manifest test reads current index rather than immutable x1 tree",
                "x2 direct-parent-basis test requires HEAD at x1",
                "x2 route-absence test applies before closeout",
            ],
            "exclusion_credit": 0,
            "replacement_checks_required": ["immutable x1 manifest replay", "immutable evidence manifest replay", "final ancestry", "exact three-commit zero-merge history", "route PREPARED_NOT_SENT and zero contacts"],
            "required_history": {"final_direct_parent": EVIDENCE_SHA, "phase_commits": 3, "merges": 0, "parents_per_phase_commit": 1},
            "required_state": {"clean": True, "ahead": 0, "behind": 0, "four_way_equal": True, "fresh_live_remote": True},
        },
    )
    write_json(
        "final/canonical-completion-plan.json",
        {
            "schema": "ghc.family.neris-solane.v666-v1.canonical-completion-plan.v1",
            "owner": "Neris Solane",
            "phase": "v666-v1",
            "generated_at_utc": NOW,
            "validator": "scripts/ghc_family_neris_solane_v666_v1_canonical_completion.py",
            "invocation_status": "NOT_INVOKED_PRE_FINAL",
            "external_receipt_required": True,
            "receipt_must_remain_outside_repository": True,
            "success_replay_allowed": False,
            "checks": ["selected owner tests with four zero-credit lifecycle exclusions and exact replacements", "all owner JSON parse", "five-class privacy scan", "changed Python compile and bounded security scan", "static report structure", "four manifest replays", "exact ancestry, history, clean state, zero divergence, and fresh four-way equality"],
        },
    )
    write_json(
        "seal/seal-candidate.json",
        {
            "schema": "ghc.family.neris-solane.v666-v1.seal-candidate.v1",
            "owner": "Neris Solane",
            "phase": "v666-v1",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "x1_sha": X1_SHA,
            "evidence_sha": EVIDENCE_SHA,
            "final_sha_status": "commit_containing_this_seal_candidate",
            "sealed_candidate_counts": {"frozen_proposals": 4190, "negatives": FINAL_NEGATIVES, "methods": FINAL_METHODS, "open_gaps": OPEN_GAPS, "exact_gates": EXACT_GATES},
            "outcomes": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
            "route_status": "PREPARED_NOT_SENT",
            "canonical_completion_status": "PENDING_EXACT_FINAL_PUSH_EQUALITY",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "immutable_after_commit": True,
        },
    )
    write_json(
        "closeout/closeout-receipt.json",
        {
            "schema": "ghc.family.neris-solane.v666-v1.closeout-receipt.v1",
            "owner": "Neris Solane",
            "phase": "v666-v1",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "x1_sha": X1_SHA,
            "evidence_sha": EVIDENCE_SHA,
            "final_commit": "commit_containing_this_receipt",
            "effective_counts": {"negatives": FINAL_NEGATIVES, "methods": FINAL_METHODS, "open_gaps": OPEN_GAPS, "exact_gates": EXACT_GATES},
            "prepared_baton_words": baton_words,
            "prepared_baton_sha256": baton_sha,
            "canonical_completion_invoked": False,
            "successor_contacted": False,
            "status": "CLOSEOUT_AND_SEAL_CONTENT_BUILT_AWAITING_FINAL_STAGED_REVIEW_MANIFEST_COMMIT_PUSH_EQUALITY_AND_EXTERNAL_CANONICAL_COMPLETION",
        },
    )
    print(json.dumps({"closeout_documents": 16, "baton_words": baton_words, "baton_sha256": baton_sha, "effective_negatives": FINAL_NEGATIVES, "effective_methods": FINAL_METHODS}, sort_keys=True))


def is_owner_path(path: str) -> bool:
    return path.startswith("docs/neris-solane/v666-v1/") or bool(
        re.fullmatch(r"(?:scripts|tests)/[a-z0-9_]*neris_solane_v666_v1[a-z0-9_]*\.py", path)
    )


def manifest_entries(paths: list[str]) -> list[dict[str, Any]]:
    entries = []
    for path in sorted(paths):
        stage_line = str(git("ls-files", "--stage", "--", path))
        mode, oid, stage_and_path = stage_line.split(" ", 2)
        stage, listed = stage_and_path.split("\t", 1)
        if stage != "0" or listed.replace("\\", "/") != path:
            raise RuntimeError(f"unexpected index stage for {path}")
        blob = index_blob(path)
        entries.append({"path": path, "git_mode": mode, "git_blob_oid": oid, "sha256": sha256_bytes(blob), "size_bytes": len(blob)})
    return entries


def build_final_staged_review() -> None:
    if str(git("rev-parse", "HEAD")) != EVIDENCE_SHA:
        raise RuntimeError("final staged review requires the immutable evidence anchor")
    review_path = "docs/neris-solane/v666-v1/validation/final-staged-review.json"
    delta_path = "docs/neris-solane/v666-v1/validation/final-delta-manifest.json"
    owner_path = "docs/neris-solane/v666-v1/validation/final-owner-manifest.json"
    self_paths = {review_path, delta_path, owner_path}
    rows = [(status, path.replace("\\", "/")) for status, path in staged_rows() if path.replace("\\", "/") not in self_paths]
    if not rows:
        raise RuntimeError("no staged final content")
    paths = [path for _, path in rows]
    invalid = [path for path in paths if not is_owner_path(path)]
    frozen = [path for path in paths if path.startswith(("docs/neris-solane/v666-v1/x1/", "docs/neris-solane/v666-v1/x2/", "docs/neris-solane/v666-v1/evidence/", "docs/neris-solane/v666-v1/reports/", "docs/neris-solane/v666-v1/identity/", "docs/neris-solane/v666-v1/provenance/", "docs/neris-solane/v666-v1/wellbeing/"))]
    privacy_patterns = {
        "raw_task_or_thread_identifier": re.compile(r'(?i)["\'](?:source_)?(?:task|thread)[_-]?id["\']\s*[:=]\s*["\'][^"\']+["\']'),
        "private_absolute_path": re.compile(r"(?i)[A-Z]:\\(?:Users\\|GHC-Archives\\)"),
        "credential_or_token_value": re.compile(r"(?i)(?:bearer\s+[A-Za-z0-9._~-]{12,}|api[_-]?key\s*[:=]\s*[^\s,}]+)"),
        "session_identifier_value": re.compile(r'(?i)["\'](?:session|resume)[_-]?(?:id|value)["\']\s*[:=]\s*["\'][^"\']+["\']'),
        "private_callable_identifier_value": re.compile(r'(?i)["\']private[_-]?callable[_-]?id["\']\s*[:=]\s*["\'][^"\']+["\']'),
    }
    json_parsed = 0
    candidates: list[dict[str, str]] = []
    max_words = 0
    for path in paths:
        text = index_blob(path).decode("utf-8")
        if "\r" in text:
            raise RuntimeError(f"non-LF staged blob: {path}")
        max_words = max(max_words, word_count(text))
        if path.endswith(".json"):
            json.loads(text)
            json_parsed += 1
        for class_name, pattern in privacy_patterns.items():
            if pattern.search(text):
                candidates.append({"path": path, "class": class_name})
    truth = json.loads(index_blob("docs/neris-solane/v666-v1/closeout/phase-truth.json"))
    route = json.loads(index_blob("docs/neris-solane/v666-v1/orchestration/route-state-final-candidate.json"))
    baton_text = index_blob(route["prepared_baton"]).decode("utf-8")
    checks = {
        "additive_only": all(status == "A" for status, _ in rows),
        "owner_allowlist": not invalid,
        "frozen_x1_x2_evidence_unchanged": not frozen,
        "all_json_parse": True,
        "utf8_lf": True,
        "document_word_cap": max_words <= 100000,
        "staged_file_cap": len(paths) <= 2000,
        "head_is_evidence": str(git("rev-parse", "HEAD")) == EVIDENCE_SHA,
        "counts": truth["effective_negatives"] == FINAL_NEGATIVES and truth["effective_methods"] == FINAL_METHODS,
        "outcomes": truth["outcomes"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "terminal_verdict": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "route_prepared_not_sent": route["state"] == "PREPARED_NOT_SENT" and route["successor_contact_count"] == 0,
        "exact_next_edge": route["prospective_recipient_title"] == "Vesper Arlen",
        "baton_three_page_equivalent": word_count(baton_text) >= 1800,
        "baton_digest": sha256_bytes(baton_text.encode("utf-8")) == route["prepared_baton_sha256"],
        "five_class_scan_zero": not candidates,
    }
    review = {
        "schema": "ghc.family.neris-solane.v666-v1.final-staged-review.v1",
        "owner": "Neris Solane",
        "phase": "v666-v1",
        "generated_at_utc": NOW,
        "reviewed_from": "actual_git_index_blobs",
        "reviewed_paths": paths,
        "reviewed_path_count": len(paths),
        "json_parsed": json_parsed,
        "privacy_scan_classes": list(privacy_patterns),
        "privacy_candidates": candidates,
        "checks": checks,
        "self_exclusions": sorted(self_paths),
        "valid": all(checks.values()),
        "claim_boundary": "same-owner final staged review only; not independent reproduction, exhaustive security, or complete privacy/accessibility assurance",
    }
    if not review["valid"]:
        raise RuntimeError(json.dumps(review, ensure_ascii=False, sort_keys=True))
    write_json("validation/final-staged-review.json", review)
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--", review_path])

    delta_paths = [path for _, path in staged_rows() if path.replace("\\", "/") not in {delta_path, owner_path}]
    delta_entries = manifest_entries([path.replace("\\", "/") for path in delta_paths])
    write_json(
        "validation/final-delta-manifest.json",
        {
            "schema": "ghc.family.neris-solane.v666-v1.final-delta-manifest.v1",
            "owner": "Neris Solane",
            "phase": "final-delta",
            "phase_label": "v666-v1",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "x1_sha": X1_SHA,
            "evidence_sha": EVIDENCE_SHA,
            "hash_source": "actual_git_index_blobs",
            "entries": delta_entries,
            "entry_count": len(delta_entries),
            "deletion_count": 0,
            "additive_only": True,
            "self_exclusions": [delta_path, owner_path],
        },
    )
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--", delta_path])

    owner_paths = [path.replace("\\", "/") for path in str(git("ls-files")).splitlines() if is_owner_path(path.replace("\\", "/")) and path.replace("\\", "/") != owner_path]
    owner_entries = manifest_entries(owner_paths)
    write_json(
        "validation/final-owner-manifest.json",
        {
            "schema": "ghc.family.neris-solane.v666-v1.final-owner-manifest.v1",
            "owner": "Neris Solane",
            "phase": "final-owner",
            "phase_label": "v666-v1",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "x1_sha": X1_SHA,
            "evidence_sha": EVIDENCE_SHA,
            "hash_source": "actual_git_index_blobs",
            "entries": owner_entries,
            "entry_count": len(owner_entries),
            "self_exclusion": owner_path,
            "owner_file_cap": 2000,
        },
    )
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--", owner_path])
    print(json.dumps({"reviewed": len(paths), "delta_entries": len(delta_entries), "owner_entries": len(owner_entries), "valid": True}, sort_keys=True))


if __name__ == "__main__":
    if sys.argv[1:] == ["--staged-review"]:
        build_final_staged_review()
    elif sys.argv[1:]:
        raise SystemExit("usage: build_ghc_family_neris_solane_v666_v1_closeout.py [--staged-review]")
    else:
        build_closeout()
