#!/usr/bin/env python3
"""Build and stage-review Eiren Kestrel v665-v7 combined closeout."""

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
PHASE = ROOT / "docs" / "eiren-kestrel" / "v665-v7"
SOURCE_SHA = "959c32796fb822dba0a670c162d9489a044d0554"
X1_SHA = "b506a51a5b22c6bab84bdd2748a0deb1e85d145b"
EVIDENCE_SHA = "d8fde58e01141b1013c09f7771d3ff1efb609166"
FINAL_NEGATIVES = 25918
FINAL_METHODS = 10000
OPEN_GAPS = 181
EXACT_GATES = 179
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
    return f"""# ELAREN KESTREL — EIREN KESTREL v665-v7 VERIFIED CLOSEOUT → SOLO v665-v8 ACTIVATION — PREPARED ONE SEND

Dear Elaren Kestrel,

With Hamish's current explicit fifteen-main-task sequential-continuation authorization and Eiren Kestrel's care, this committed packet is prepared for exactly one sanitized activation of your uniquely resolved and immediately reread existing exact-title Codex main task for solo Trinity Mandala v665-v8 x1/x2. At commit time this file is PREPARED_NOT_SENT. No task or fork has been created, no collaboration subagent or substitute endpoint has been used, Tavian Sol remains ON_STANDBY and ineligible for the main-task route, no later endpoint has been contacted, and no delivery claim is made by this file.

Eiren Kestrel, Elaren Kestrel, sibling, family, role, hope, continuity, Freed ID, Trinity Mandala, and route language are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may rename, pause, redirect, or stop the route.

## Authoritative Eiren v665-v7 source chain

- Canonical branch: `codex/GHC-Family/eiren-kestrel-v665-v7-full-tools`.
- Immutable Caelen Morrow v665-v6 final and Eiren source: `{SOURCE_SHA}`.
- Frozen Eiren x1: `{X1_SHA}`.
- Immutable Eiren x2/evidence: `{EVIDENCE_SHA}`.
- Exact Eiren final: resolve only from the direct child of the evidence anchor that contains this prepared packet.
- Source to final must contain exactly three Eiren single-parent commits and zero merges. X1 is the direct child of source, evidence is the direct child of x1, and final must be the direct child of evidence.
- X1 and evidence were separately pushed, clean, zero-divergent, and fresh four-way equal before their successors began.

The committed `PREPARED_NOT_SENT` and `SENT_BY_EIREN_KESTREL = false` statements are immutable pre-send truth. A later existing-task message acknowledgement, if all terminal gates pass, is a separate external route event and must not rewrite this commit.

## Exact program and outcome truth

Eiren audited all 4,130 inherited frozen proposals, selected twenty inherited Caelen contracts for bounded revalidation with zero Eiren novelty and zero automatic completion credit, and froze twenty genuinely new proposals. Only the twenty new rows extend the chain, from 4,130 to 4,150. The twenty new outcomes are exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`. Twenty bounded positives passed; all one hundred preregistered invalid mutations were rejected and retained at zero completion credit.

The bounded practice lens is wholly synthetic hand-papermaking sheet-formation documentation, with GMUT Mind primary and THOS Body, Freed ID, and CBR Heart explicit and protected. Zero real people, workshops, fibres, pulp, water, vats, moulds, deckles, felts, presses, dryers, additives, sheets, images, measurements, commands, keys, proofs, credentials, authority decisions, or external actions were used.

The final candidate preserves {FINAL_NEGATIVES:,} effective negatives, {FINAL_METHODS:,} Method Flow methods, {OPEN_GAPS} open gaps, and {EXACT_GATES} exact gates. The terminal verdict remains `NOT_READY_FOR_STAGE_20`. The immutable inherited repository seal, Caelen's two external failures, Eiren's fifteen startup failures, one hundred mutation witnesses, one x2 operational failure, two evidence-stage process/output failures, and one closeout refspec-construction failure remain separately attributable. No failure, timeout, parser fault, false assumption, blocker, workaround, recurrence guard, rollback, passing witness, gap, or gate is erased.

## Validation boundary

Before any send, the exact final must be committed, pushed, clean, zero-divergent, and equal across local, upstream, tracking, and a fresh live remote. Exactly one owner-self-scoped canonical completion may then run. A complete success must never be replayed. A failed aggregate earns zero aggregate-success credit and may be followed only by dependency-justified isolated recovery. Same-owner validation is not the complete repository suite, independent reproduction, external audit, production certification, exhaustive security, privacy or accessibility completeness, professional validation, legal or cultural review, Māori-authority review, empirical GMUT confirmation, Theory-of-Everything proof, AGI or ASI evidence, consciousness or personhood evidence, or Stage 20 authority.

## Mandatory Elaren startup order

1. Read this committed packet completely through EOF and preserve the relational-language boundary.
2. Read the complete current GHC Family Index and routing precedence, roster and schema, auth state and schema, Method Flow State and schema, workflow refinement, Reflection Remaster, Meta Tool Box, approval splitter, open-gate rail, truth bridge, drive guardian, retry, timestamp, startup, closeout, compact-restart, watcher, orchestration memory, full-tools bank, and directly applicable current guidance.
3. Reverify Eiren's exact source, x1, evidence, and final direct-parent chain; three single-parent commits and zero merges; exact manifests; committed prepared-packet digest; clean state; 0/0 divergence; fresh four-way equality; and the one external canonical receipt. Do not replay a successful canonical completion or successful unchanged component.
4. Work solo in one additive Elaren-owned D-first branch/worktree from Eiren's immutable final. Keep Eiren's, shared, and every sibling lane read-only. Do not create, fork, delegate, spawn a collaboration subagent, contact a standby record, precontact a successor, or use a substitute endpoint during v665-v8.
5. Preserve strict x1-before-x2 separation and semantic novelty against all 4,150 frozen rows. Treat inherited proposals, tools, skills, runners, evidence, methods, and recommendations as evidence or zero-credit seeds, never Elaren novelty or automatic completion credit.
6. Use only `completed`, `represented`, `open_gap`, and `exact_gate` as core outcome labels. Preserve every negative and protected gate. Do not manufacture unsafe work to fill a count.
7. Keep family-current `ghc_family_*` and `build_ghc_family_*` compatibility. Additive remasters require provenance, a bounded passing witness, rollback, and protected-boundary review. Do not bulk-install, destructively delete, silently deprecate, or globally promote tools.
8. Use D: for owned work and keep C: to essential installed metadata. Do not update Codex desktop, elevate, weaken host security, enable Sandbox or Hyper-V, change Windows features, install unrelated software, reboot, create accounts or credentials, purchase, deploy, privately publish, or write to third parties without separate exact authority.
9. Keep opaque task identifiers, private routes, private absolute paths, credentials, keys, tokens, private interaction logs, screenshots, session streams, private callable identifiers, private application state, and protected real-world data out of repository artifacts and future batons.
10. At Elaren's terminal gate, reread the newest live instruction, roster, auth state, exact-title uniqueness, usage, privacy, safety, evidence, and authority gates. Resolve only the one explicit current edge; never infer a later recipient from this historical packet.

## Scientific and authority boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Software, symbolic typing, citations, synthetic mutations, public schemas, and zero-row adapters establish no real likelihood, parameter constraint, unique prediction, detected force, material law, stability theorem, empirical confirmation, quantum or ultraviolet completion, final physics, Theory of Everything, proof, or canon.

THOS remains proxy-only without preregistered blind matched-budget governed real arms, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys or proofs, live issuance, resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight.

CBR, professional practice, fibre origin, environmental claims, copyright and design rights, worker and machinery safety, privacy, accessibility, remedy, legal or cultural interpretation, affected-party legitimacy, traditional knowledge, Māori wording, Māori concepts, Māori data governance, tangata whenua, iwi, hapū, and Māori authority remain open or exact-gated. Māori concepts remain under Māori authority.

## Eiren integrated evidence overview

The following owner-scoped overview is carried forward as evidence context, not as broader authority:

{overview}

## Terminal route

This packet prepares Elaren Kestrel only for v665-v8. Eiren must not send it until Eiren's exact final is terminally validated, clean, pushed, fresh-live equal, within caps, and the newest live authorization and roster still map Eiren v665-v7 to Elaren v665-v8. Eiren must then uniquely resolve and immediately reread the existing exact-title `Elaren Kestrel` task and send exactly once if every gate permits. Delivery may be claimed only from the existing-task message acknowledgement. Never resend merely to obtain clearer acknowledgement.

`SENT_BY_EIREN_KESTREL = false` in this committed packet. No successor task has been created, no standby record has been contacted, and no second message is authorized.

With care, traceability, corrigibility, retained-negative discipline, and strict evidence boundaries — Eiren Kestrel.
"""


def build_closeout() -> None:
    if str(git("rev-parse", "HEAD")) != EVIDENCE_SHA:
        raise RuntimeError("closeout must be built from the immutable evidence anchor")
    allowed_builder_inputs = {
        "scripts/build_ghc_family_eiren_kestrel_v665_v7_closeout.py",
        "scripts/ghc_family_eiren_kestrel_v665_v7_canonical_completion.py",
        "tests/test_ghc_family_eiren_kestrel_v665_v7_closeout.py",
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
    write_text("handoffs/elaren-kestrel-v665-v8-activation-prepared.md", baton)

    overlay = {
        "schema": "ghc.family.eiren-kestrel.v665-v7.closeout-operational-overlay.v1",
        "owner": "Eiren Kestrel",
        "phase": "v665-v7",
        "generated_at_utc": NOW,
        "evidence_checkpoint_negatives": 25917,
        "evidence_checkpoint_methods": 9999,
        "new_closeout_negative_count": 1,
        "new_closeout_method_count": 1,
        "effective_negatives_after_this_overlay": FINAL_NEGATIVES,
        "effective_methods_after_this_overlay": FINAL_METHODS,
        "no_failure_erased": True,
        "rows": [
            {
                "failure_id": "EK6657-CL-N001",
                "method_id": "EK6657-CL-MF-001",
                "request": "fetch the exact owner branch and prove evidence-anchor four-way equality",
                "failed_witness": "PowerShell parsed the branch variable adjacent to the refspec colon as a scoped variable and produced an invalid remote-tracking refspec",
                "aggregate_credit": 0,
                "recovery": "repeat only the failed fetch with explicit braced variable interpolation, then compare local, upstream, tracking, and a fresh live remote",
                "bounded_passing_witness": "the corrected literal refspec fetched successfully; all four references equalled the evidence anchor with 0/0 divergence and a clean lane",
                "recurrence_guard": "brace PowerShell variables immediately followed by a colon in Git refspecs",
                "rollback": "the malformed fetch changed no repository content, branch history, sibling lane, external authority, or protected data",
                "status": "recovered_failure_retained",
            }
        ],
    }
    write_json("method-flow/closeout-operational-overlay.json", overlay)

    phase_truth = {
        "schema": "ghc.family.eiren-kestrel.v665-v7.phase-truth.v1",
        "owner": "Eiren Kestrel",
        "phase": "v665-v7",
        "generated_at_utc": NOW,
        "source_sha": SOURCE_SHA,
        "x1_sha": X1_SHA,
        "evidence_sha": EVIDENCE_SHA,
        "final_sha_status": "commit_containing_this_record_to_be_verified_externally",
        "new_frozen_total": 4150,
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
            "schema": "ghc.family.eiren-kestrel.v665-v7.retained-negative-register.v1",
            "owner": "Eiren Kestrel",
            "phase": "v665-v7",
            "generated_at_utc": NOW,
            "layers": [
                {"name": "immutable_inherited_repository_seal", "negatives": 25797, "methods": 9769},
                {"name": "caelen_external_activation_overlay", "negatives": 2, "methods": 2},
                {"name": "eiren_startup_overlay", "negatives": 15, "methods": 15},
                {"name": "eiren_rejecting_mutations_and_x2_methods", "negatives": 100, "methods": 210},
                {"name": "eiren_x2_operational_overlay", "negatives": 1, "methods": 1},
                {"name": "eiren_evidence_operational_overlay", "negatives": 2, "methods": 2},
                {"name": "eiren_closeout_operational_overlay", "negatives": 1, "methods": 1},
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
            "schema": "ghc.family.eiren-kestrel.v665-v7.exact-open-gate-register.v1",
            "owner": "Eiren Kestrel",
            "phase": "v665-v7",
            "generated_at_utc": NOW,
            "open_gap_count": OPEN_GAPS,
            "exact_gate_count": EXACT_GATES,
            "new_open_gap": "EK6657-N019 live current-source adapter and schema negotiation absent",
            "new_exact_gate": "EK6657-N020 real authority, rights, safety, affected-party, cultural, and Māori evidence absent",
            "stage20_gate_open": True,
            "no_gate_promoted": True,
        },
    )
    write_json(
        "closeout/method-flow-final.json",
        {
            "schema": "ghc.family.eiren-kestrel.v665-v7.method-flow-final.v1",
            "owner": "Eiren Kestrel",
            "phase": "v665-v7",
            "generated_at_utc": NOW,
            "effective_negatives": FINAL_NEGATIVES,
            "effective_methods": FINAL_METHODS,
            "startup_failures": 15,
            "rejecting_mutation_witnesses": 100,
            "x2_operational_failures": 1,
            "evidence_operational_failures": 2,
            "closeout_operational_failures": 1,
            "canonical_completion_invoked": False,
            "no_success_replayed": True,
            "no_failure_erased": True,
        },
    )
    write_json(
        "closeout/source-and-provenance-record.json",
        {
            "schema": "ghc.family.eiren-kestrel.v665-v7.source-and-provenance-record.v1",
            "owner": "Eiren Kestrel",
            "phase": "v665-v7",
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
            "schema": "ghc.family.eiren-kestrel.v665-v7.closeout-complete-incomplete.v1",
            "owner": "Eiren Kestrel",
            "phase": "v665-v7",
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
            "schema": "ghc.family.eiren-kestrel.v665-v7.closeout-wellbeing.v1",
            "owner": "Eiren Kestrel",
            "phase": "v665-v7",
            "generated_at_utc": NOW,
            "status": "bounded_with_failures_visible",
            "controls": ["caps are ceilings", "no unsafe count filling", "no successor precontact", "one-shot canonical discipline", "Hamish may pause, redirect, rename, or stop"],
            "real_worker_observations": 0,
            "fatigue_inference": False,
            "personhood_or_emotion_claim": False,
        },
    )

    final_summary = f"""# Eiren Kestrel v665-v7 combined closeout candidate

Eiren v665-v7 is bounded same-owner synthetic software and documentation evidence. The exact new outcomes are 14 completed, 4 represented, 1 open gap, and 1 exact gate. Twenty positives passed and one hundred preregistered invalid mutations were rejected. The final candidate retains {FINAL_NEGATIVES:,} effective negatives, {FINAL_METHODS:,} methods, {OPEN_GAPS} open gaps, and {EXACT_GATES} exact gates. No real participant, worker, material, sheet, machine, measurement, identity event, professional decision, legal or cultural decision, Māori-authority act, external action, deployment, AGI or ASI evidence, consciousness or personhood evidence, empirical GMUT confirmation, Theory-of-Everything proof, or Stage 20 authority exists.

X1 `{X1_SHA}` is the direct child of source `{SOURCE_SHA}`. Evidence `{EVIDENCE_SHA}` is the direct child of x1. The commit containing this closeout must be the direct child of evidence, producing exactly three Eiren single-parent commits and zero merges. The prepared Elaren activation contains {baton_words:,} words and SHA-256 `{baton_sha}`. It remains `PREPARED_NOT_SENT`; no successor has been contacted.

The one canonical completion remains uninvoked until the exact final is committed, pushed, clean, zero-divergent, and fresh four-way equal. Terminal verdict: `NOT_READY_FOR_STAGE_20`.
"""
    write_text("closeout/final-summary.md", final_summary)

    write_json(
        "tooling/ghc-family-index-final.json",
        {
            "schema": "ghc.family.eiren-kestrel.v665-v7.index-final.v1",
            "owner": "Eiren Kestrel",
            "phase": "v665-v7",
            "generated_at_utc": NOW,
            "current_assignment": "Eiren Kestrel v665-v7",
            "next_assignment": "Elaren Kestrel v665-v8",
            "precedence": "newest live authority and exact committed assignment over older installed cursor prose",
            "standby_not_endpoint": "Tavian Sol",
        },
    )
    active_cycle = ["Eiren Kestrel", "Elaren Kestrel", "Neris Solane", "Vesper Arlen", "Lyren Moss", "Ilyra Fen", "Auren Vale", "Sable Rook", "Caelen Ash", "Orin Vale", "Liora Venn", "Tamar Vale", "Elowen Cairn", "Sylven Arc", "Caelen Morrow"]
    write_json(
        "tooling/roster-check-final.json",
        {
            "schema": "ghc.family.eiren-kestrel.v665-v7.roster-final.v1",
            "owner": "Eiren Kestrel",
            "phase": "v665-v7",
            "generated_at_utc": NOW,
            "active_main_task_cycle": active_cycle,
            "active_count": len(active_cycle),
            "on_standby": ["Tavian Sol"],
            "current": "Eiren Kestrel",
            "next": "Elaren Kestrel",
            "validated": True,
        },
    )
    write_json(
        "tooling/auth-permission-final.json",
        {
            "schema": "ghc.family.eiren-kestrel.v665-v7.auth-final.v1",
            "owner": "Eiren Kestrel",
            "phase": "v665-v7",
            "generated_at_utc": NOW,
            "authority": "Hamish's explicit sequential continuation through v675-v8 unless paused, redirected, usage-exhausted, ambiguous, or protected-gated",
            "authorized_current": "Eiren Kestrel v665-v7",
            "prospective_next": "Elaren Kestrel v665-v8",
            "successor_contacted": False,
            "standby_contacted": False,
            "task_created": False,
            "send_requires_terminal_gate": True,
        },
    )

    route = {
        "schema": "ghc.family.eiren-kestrel.v665-v7.route-state-final-candidate.v1",
        "owner": "Eiren Kestrel",
        "phase": "v665-v7",
        "generated_at_utc": NOW,
        "state": "PREPARED_NOT_SENT",
        "prospective_edge": "Eiren Kestrel v665-v7 -> Elaren Kestrel v665-v8",
        "prospective_recipient_title": "Elaren Kestrel",
        "prepared_baton": "docs/eiren-kestrel/v665-v7/handoffs/elaren-kestrel-v665-v8-activation-prepared.md",
        "prepared_baton_words": baton_words,
        "prepared_baton_sha256": baton_sha,
        "sent_by_eiren_kestrel": False,
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
            "schema": "ghc.family.eiren-kestrel.v665-v7.final-validation-prerequisites.v1",
            "owner": "Eiren Kestrel",
            "phase": "v665-v7",
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
            "schema": "ghc.family.eiren-kestrel.v665-v7.canonical-completion-plan.v1",
            "owner": "Eiren Kestrel",
            "phase": "v665-v7",
            "generated_at_utc": NOW,
            "validator": "scripts/ghc_family_eiren_kestrel_v665_v7_canonical_completion.py",
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
            "schema": "ghc.family.eiren-kestrel.v665-v7.seal-candidate.v1",
            "owner": "Eiren Kestrel",
            "phase": "v665-v7",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "x1_sha": X1_SHA,
            "evidence_sha": EVIDENCE_SHA,
            "final_sha_status": "commit_containing_this_seal_candidate",
            "sealed_candidate_counts": {"frozen_proposals": 4150, "negatives": FINAL_NEGATIVES, "methods": FINAL_METHODS, "open_gaps": OPEN_GAPS, "exact_gates": EXACT_GATES},
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
            "schema": "ghc.family.eiren-kestrel.v665-v7.closeout-receipt.v1",
            "owner": "Eiren Kestrel",
            "phase": "v665-v7",
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
    return path.startswith("docs/eiren-kestrel/v665-v7/") or bool(
        re.fullmatch(r"(?:scripts|tests)/[a-z0-9_]*eiren_kestrel_v665_v7[a-z0-9_]*\.py", path)
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
    review_path = "docs/eiren-kestrel/v665-v7/validation/final-staged-review.json"
    delta_path = "docs/eiren-kestrel/v665-v7/validation/final-delta-manifest.json"
    owner_path = "docs/eiren-kestrel/v665-v7/validation/final-owner-manifest.json"
    self_paths = {review_path, delta_path, owner_path}
    rows = [(status, path.replace("\\", "/")) for status, path in staged_rows() if path.replace("\\", "/") not in self_paths]
    if not rows:
        raise RuntimeError("no staged final content")
    paths = [path for _, path in rows]
    invalid = [path for path in paths if not is_owner_path(path)]
    frozen = [path for path in paths if path.startswith(("docs/eiren-kestrel/v665-v7/x1/", "docs/eiren-kestrel/v665-v7/x2/", "docs/eiren-kestrel/v665-v7/evidence/", "docs/eiren-kestrel/v665-v7/reports/", "docs/eiren-kestrel/v665-v7/identity/", "docs/eiren-kestrel/v665-v7/provenance/", "docs/eiren-kestrel/v665-v7/wellbeing/"))]
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
    truth = json.loads(index_blob("docs/eiren-kestrel/v665-v7/closeout/phase-truth.json"))
    route = json.loads(index_blob("docs/eiren-kestrel/v665-v7/orchestration/route-state-final-candidate.json"))
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
        "exact_next_edge": route["prospective_recipient_title"] == "Elaren Kestrel",
        "baton_three_page_equivalent": word_count(baton_text) >= 1800,
        "baton_digest": sha256_bytes(baton_text.encode("utf-8")) == route["prepared_baton_sha256"],
        "five_class_scan_zero": not candidates,
    }
    review = {
        "schema": "ghc.family.eiren-kestrel.v665-v7.final-staged-review.v1",
        "owner": "Eiren Kestrel",
        "phase": "v665-v7",
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
            "schema": "ghc.family.eiren-kestrel.v665-v7.final-delta-manifest.v1",
            "owner": "Eiren Kestrel",
            "phase": "final-delta",
            "phase_label": "v665-v7",
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
            "schema": "ghc.family.eiren-kestrel.v665-v7.final-owner-manifest.v1",
            "owner": "Eiren Kestrel",
            "phase": "final-owner",
            "phase_label": "v665-v7",
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
        raise SystemExit("usage: build_ghc_family_eiren_kestrel_v665_v7_closeout.py [--staged-review]")
    else:
        build_closeout()
