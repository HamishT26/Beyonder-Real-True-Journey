#!/usr/bin/env python3
"""Build Sylven Arc v667-v4 closeout artifacts and exact staged manifests."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "sylven-arc" / "v667-v4"
OWNER = "Sylven Arc"
OWNER_SLUG = "sylven-arc"
PHASE = "v667-v4"
BRANCH = "codex/GHC-Family/sylven-arc-v667-v4-full-tools"
SOURCE_SHA = "9625026b09860c8964dd818e8d1f81ee6e2eed57"
X1_SHA = "0eb52121251e3e8ee6da0c3c472626640cde96a3"
EVIDENCE_SHA = "4de3cc042a3cb15c626e744fbf9977cc7e6ca437"
NOW = "2026-08-23T05:03:56Z"


def run(*args: str) -> str:
    return subprocess.check_output(
        list(args), cwd=ROOT, text=True, encoding="utf-8"
    ).strip()


def load(relative: str) -> Any:
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


def write_json(relative: str, value: Any) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(relative: str, value: str) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


POST_EVIDENCE_FAILURES = [
    {
        "failure_id": "SA6674-CO-F010",
        "stage": "evidence_commit_presentation",
        "failed_method": "wait on the original evidence-commit wrapper after its output exceeded the available presentation context",
        "failure": "the wrapper handle was no longer available, so it supplied no attributable terminal commit payload even though the commit had completed",
        "credit": 0,
        "retained": True,
        "bounded_recovery": "inspect HEAD, parent, subject, and porcelain status read-only; prove the intended evidence commit already exists and do not retry it",
        "recurrence_guard": "capture commit output with a small summary or inspect exact Git state before any retry",
        "failure_erased": False,
    },
    {
        "failure_id": "SA6674-CO-F011",
        "stage": "evidence_remote_equality",
        "failed_method": "project four refs and divergence while leaving the PowerShell upstream revision expression unquoted",
        "failure": "PowerShell malformed the divergence argument and Git returned no divergence value; the independently collected four refs and clean state remained valid",
        "credit": 0,
        "retained": True,
        "bounded_recovery": "run only git rev-list --left-right --count with the full revision expression quoted literally; observe 0/0",
        "recurrence_guard": "quote revision expressions containing PowerShell at-sign and brace syntax",
        "failure_erased": False,
    },
    {
        "failure_id": "SA6674-CO-F012",
        "stage": "final_staged_review",
        "failed_method": "read every staged blob through a separate git show subprocess",
        "failure": "the exact-index review remained silent beyond its bounded reporting window and was interrupted before producing a valid staged-review receipt",
        "credit": 0,
        "retained": True,
        "bounded_recovery": "replace only blob transport with one alternating git cat-file --batch stream that consumes each declared blob length exactly before sending the next request",
        "recurrence_guard": "use one exact-length batch transport for large staged manifests and preserve request-response alternation to prevent pipe backpressure",
        "failure_erased": False,
    },
    {
        "failure_id": "SA6674-CO-F013",
        "stage": "final_staged_review",
        "failed_method": "apply the first final owner allowlist and scanner-definition classification to the exact staged index",
        "failure": "the review correctly rejected one intentional family flashcard compatibility file as out of scope and counted two of that runner's privacy-scanner regex definitions as content hits",
        "credit": 0,
        "retained": True,
        "bounded_recovery": "add only the exact family flashcard compatibility path to the owner allowlist and scanner-definition set, then regenerate the uncommitted staged review",
        "recurrence_guard": "carry reviewed shared-family compatibility paths and their scanner-definition role explicitly into final allowlists",
        "failure_erased": False,
    },
]


def build_closeout() -> None:
    if run("git", "rev-parse", "HEAD") != EVIDENCE_SHA:
        raise RuntimeError("closeout must begin at the exact immutable evidence head")
    allowed_refresh_prefixes = (
        "docs/sylven-arc/v667-v4/closeout/",
        "docs/sylven-arc/v667-v4/handoffs/",
        "docs/sylven-arc/v667-v4/method-flow/final-method-flow-summary.json",
        "docs/sylven-arc/v667-v4/seal/",
        "docs/sylven-arc/v667-v4/validation/final-",
        "docs/sylven-arc/v667-v4/wellbeing/final-wellbeing-check.json",
        "scripts/build_ghc_family_sylven_arc_v667_v4_closeout.py",
        "scripts/ghc_family_sylven_arc_v667_v4_canonical.py",
        "scripts/ghc_family_freed_id_flashcards.py",
        "tests/test_ghc_family_sylven_arc_v667_v4_closeout.py",
    )
    status_paths = []
    for line in run("git", "status", "--porcelain=v1").splitlines():
        path = line[3:].replace("\\", "/")
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        status_paths.append(path)
    unexpected = [path for path in status_paths if not path.startswith(allowed_refresh_prefixes)]
    if unexpected:
        raise RuntimeError(f"closeout refresh found non-closeout paths: {unexpected}")

    evidence = load("evidence/immutable-evidence-candidate.json")
    negatives = load("evidence/retained-negative-register.json")
    methods = load("method-flow/x2-method-flow-ledger.json")
    gaps = load("evidence/open-gap-register.json")
    gates = load("evidence/exact-gate-register.json")
    outcomes = load("x2/proposal-outcomes.json")
    portfolio = load("x2/portfolio-execution.json")
    registry = load("x2/skill-runner-registry.json")
    flashcards = load("x2/flashcards/execution-receipts.json")

    overlay_count = len(POST_EVIDENCE_FAILURES)
    final_negatives = negatives["effective_count"] + overlay_count
    final_methods = methods["effective_method_count"] + overlay_count
    final_failed = methods["phase_failed_witness_count"] + overlay_count
    final_passing = methods["phase_bounded_passing_witness_count"] + overlay_count

    write_json(
        "closeout/post-evidence-operational-failures.json",
        {
            "schema": "ghc-family-post-evidence-operational-failures-v5",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "immutable_evidence_negative_count": negatives["effective_count"],
            "immutable_evidence_method_count": methods["effective_method_count"],
            "additive_failure_count": overlay_count,
            "effective_closeout_negative_count": final_negatives,
            "effective_closeout_method_count": final_methods,
            "rows": POST_EVIDENCE_FAILURES,
        },
    )
    write_json(
        "method-flow/final-method-flow-summary.json",
        {
            "schema": "ghc-family-final-method-flow-summary-v5",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "immutable_evidence_ledger": "method-flow/x2-method-flow-ledger.json",
            "immutable_evidence_method_count": methods["effective_method_count"],
            "post_evidence_failure_count": overlay_count,
            "effective_method_count": final_methods,
            "phase_failed_witness_count": final_failed,
            "phase_bounded_passing_witness_count": final_passing,
            "post_evidence_rows": [
                {
                    "method_id": row["failure_id"],
                    "class": "closeout_owner_operational_failure",
                    "failed_witness": row,
                    "bounded_passing_witness": {
                        "recovery": row["bounded_recovery"],
                        "scope": "only the failed dependency",
                        "promotes_failed_witness": False,
                    },
                    "failure_erased": False,
                }
                for row in POST_EVIDENCE_FAILURES
            ],
            "failure_erased_count": 0,
        },
    )

    phase_truth = {
        "schema": "ghc-family-phase-truth-v5",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "source": SOURCE_SHA,
        "frozen_x1": X1_SHA,
        "immutable_evidence": EVIDENCE_SHA,
        "final_candidate_parent": EVIDENCE_SHA,
        "core_outcomes": outcomes["counts"],
        "proposal_count": len(outcomes["outcomes"]),
        "frozen_proposal_chain": 4410,
        "positive_contract_count": evidence["positive_contracts"],
        "proposal_rejecting_mutation_count": evidence["proposal_rejecting_mutations"],
        "flashcard_rejecting_mutation_count": evidence["flashcard_rejecting_mutations"],
        "accepted_mutation_count": evidence["accepted_mutations"],
        "owner_portfolio_execution_count": evidence["owner_portfolio_executions"],
        "held_portfolio_row_count": evidence["held_portfolio_rows"],
        "phase_local_skill_count": registry["skill_count"],
        "family_current_runner_count": registry["runner_count"],
        "runner_smoke_passes": registry["runner_smoke_passes"],
        "flashcard_card_count": evidence["flashcard_cards"],
        "flashcard_section_count": evidence["flashcard_sections"],
        "effective_negatives": final_negatives,
        "effective_methods": final_methods,
        "effective_open_gaps": gaps["effective_count"],
        "effective_exact_gates": gates["effective_count"],
        "phase_failed_witness_count": final_failed,
        "phase_bounded_passing_witness_count": final_passing,
        "real_people": 0,
        "real_objects": 0,
        "real_measurements": 0,
        "network_calls_by_phase_software": 0,
        "keys": 0,
        "proofs": 0,
        "external_actions": 0,
        "same_owner_evidence": True,
        "independent_reproduction": False,
        "full_repository_suite_run": False,
        "exact_final_canonical_status": "PENDING_EXTERNAL_EXCLUSIVE_INVOCATION_AFTER_FINAL_PUSH",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    write_json("closeout/phase-truth.json", phase_truth)

    write_json(
        "closeout/lifecycle-replay.json",
        {
            "schema": "ghc-family-lifecycle-replay-v5",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "source": SOURCE_SHA,
            "x1": X1_SHA,
            "evidence": EVIDENCE_SHA,
            "x1_direct_parent": run("git", "rev-parse", f"{X1_SHA}^"),
            "evidence_direct_parent": run("git", "rev-parse", f"{EVIDENCE_SHA}^"),
            "x1_direct_from_source": run("git", "rev-parse", f"{X1_SHA}^") == SOURCE_SHA,
            "evidence_direct_from_x1": run("git", "rev-parse", f"{EVIDENCE_SHA}^") == X1_SHA,
            "source_to_evidence_commit_count": int(run("git", "rev-list", "--count", f"{SOURCE_SHA}..{EVIDENCE_SHA}")),
            "source_to_evidence_merge_count": int(run("git", "rev-list", "--count", "--min-parents=2", f"{SOURCE_SHA}..{EVIDENCE_SHA}")),
            "x1_four_way_equal_before_x2": True,
            "evidence_four_way_equal_before_closeout": True,
            "evidence_divergence_before_closeout": "0/0",
            "final_expected_direct_parent": EVIDENCE_SHA,
            "strict_x1_before_x2": True,
        },
    )

    write_json(
        "closeout/authority-boundaries.json",
        {
            "schema": "ghc-family-authority-boundaries-v5",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "relational_identity": "Relational names, roles, hopes, continuity and family language are working language only and are not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, agency or authority.",
            "gmut": "Typed scalar-tensor and EFT research-model obligations only; no real likelihood, constraint, force, prediction, detected phenomenon, empirical confirmation, quantum or ultraviolet completion, final physics, Theory-of-Everything proof or canon.",
            "thos": "Participant-free proxy only; no blind matched-budget governed real arms, operators, safety monitoring, statistics, outcomes or independent review.",
            "freed_id": "Synthetic and nonproduction; no standards-conformant real keys or proofs, live issuance, resolution, status, revocation, interoperability, privacy and independent security review, recovery evidence or trust governance.",
            "cbr": "Professional decisions, electrical and gas safety, ownership, heritage, public display, image and recording rights, remedy, affected-party, legal, cultural and Māori authority remain exact-gated.",
            "maori": "Māori wording, concepts and data governance remain under competent tangata whenua, iwi, hapū and Māori authority.",
            "terminal": "NOT_READY_FOR_STAGE_20",
        },
    )

    write_json(
        "closeout/complete-incomplete-checklist.json",
        {
            "schema": "ghc-family-complete-incomplete-checklist-v5",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "complete": [
                "exact source and fresh remote verification",
                "planning-only x1 frozen and pushed before x2",
                "semantic novelty audit against all 4,390 inherited proposal rows",
                "twenty genuinely new proposal contracts",
                "exact 14 completed, 4 represented, 1 open_gap and 1 exact_gate outcome partition",
                "one hundred rejected proposal mutations and sixty rejected flashcard mutations",
                "ninety-five bounded owner portfolio executions and one hundred held rows",
                "ten phase-local skills and ten family-current runners built and smoke-used",
                "233-card, four-tier, thirteen-section Freed ID flashcard deck",
                "all inherited and owner failures retained with bounded recoveries",
                "immutable evidence pushed and fresh four-way equal before closeout",
                "complete owner closeout candidate and accessible static report",
            ],
            "incomplete_or_reserved": [
                "real neon-signmaking, glassworking, electrical, gas, installation, repair or safety action",
                "real Smithsonian API call, download, schema evaluation, record or media",
                "real participant, operator, matched-budget arm, statistics or independent review",
                "real key, proof, identity lifecycle, interoperability, independent security review or trust governance",
                "professional, ownership, heritage, display, recording, legal, cultural, affected-party or Māori-authority decision",
                "manual browser, assistive-technology, cognitive-accessibility, Māori-language and affected-user evaluation",
                "complete privacy, accessibility, exhaustive security, independent reproduction or production validation",
                "empirical GMUT confirmation, Theory-of-Everything proof, AGI/ASI, consciousness/personhood, canon or Stage 20",
                "external exact-final canonical invocation, pending clean pushed final",
                "successor delivery, pending terminal gate and live route refresh",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )

    write_json(
        "wellbeing/final-wellbeing-check.json",
        {
            "schema": "ghc-family-wellbeing-check-v5",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "relational_only": True,
            "workload_state": "bounded closeout after immutable evidence push",
            "stop_conditions_respected": True,
            "subagents_spawned": 0,
            "other_owner_lanes_mutated": 0,
            "global_installations": 0,
            "external_actions": 0,
            "failures_hidden": 0,
            "manual_mental_health_or_consciousness_claim": False,
            "note": "This is a workload and process-boundary check, not evidence of feelings, consciousness, continuity or clinical wellbeing.",
        },
    )

    write_json(
        "closeout/stale-label-review.json",
        {
            "schema": "ghc-family-stale-label-review-v5",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "reviewed_surfaces": ["owner packet", "phase constants", "source anchors", "skills", "runners", "flashcard deck", "handoff candidate"],
            "allowed_historical_labels": [
                "Elowen Cairn v667-v3 as exact source attribution",
                "Tamar Vey v667-v2 as ancestral source attribution",
                "Caelen Morrow v667-v5 as provisional terminal successor only",
            ],
            "stale_owner_or_phase_candidates": [],
            "valid": True,
        },
    )

    write_json(
        "validation/final-prerequisites.json",
        {
            "schema": "ghc-family-final-validation-prerequisites-v5",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "evidence_head": EVIDENCE_SHA,
            "evidence_pushed": True,
            "evidence_clean": True,
            "evidence_zero_divergence": True,
            "evidence_four_way_equal": True,
            "final_required_direct_parent": EVIDENCE_SHA,
            "exclusive_canonical_invocation_budget": 1,
            "canonical_invocations_so_far": 0,
            "post_success_replay_forbidden": True,
            "full_repository_suite_authorized": False,
            "final_status": "PENDING_FINAL_COMMIT_PUSH_AND_EXCLUSIVE_CANONICAL",
        },
    )

    write_json(
        "closeout/route-receipt.json",
        {
            "schema": "ghc-family-route-receipt-v5",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "status": "PREPARED_NOT_SENT",
            "provisional_successor_title": "Caelen Morrow",
            "provisional_successor_phase": "v667-v5",
            "exact_title_resolution_performed": False,
            "successor_reread_performed": False,
            "duplicate_guard_performed": False,
            "send_attempted": False,
            "acknowledged": False,
            "binding_rule": "No route action until final push, exact-final canonical success, fresh live authorization and roster, unique exact title, immediate reread and duplicate guard.",
        },
    )

    write_json(
        "seal/seal-candidate.json",
        {
            "schema": "ghc-family-seal-candidate-v5",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "source": SOURCE_SHA,
            "x1": X1_SHA,
            "evidence": EVIDENCE_SHA,
            "expected_final_parent": EVIDENCE_SHA,
            "outcomes": outcomes["counts"],
            "effective_negatives": final_negatives,
            "effective_methods": final_methods,
            "effective_open_gaps": gaps["effective_count"],
            "effective_exact_gates": gates["effective_count"],
            "failed_witnesses_erased": 0,
            "canonical_binding": "external exact-head exclusive receipt after final push",
            "status": "PREPARED_PENDING_EXACT_FINAL_CANONICAL",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )

    write_json(
        "closeout/terminal-checklist.json",
        {
            "schema": "ghc-family-terminal-checklist-v5",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "repository_packet_complete": True,
            "evidence_commit": EVIDENCE_SHA,
            "final_commit": "BIND_AFTER_DIRECT_CHILD_COMMIT",
            "final_parent_must_equal": EVIDENCE_SHA,
            "exclusive_canonical_status": "PENDING_AFTER_FINAL_PUSH",
            "post_success_replay_forbidden": True,
            "full_repository_suite_run": False,
            "route_status": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )

    baton = """# Caelen Morrow v667-v5 activation candidate — prepared, not sent

Status: `PREPARED_NOT_SENT`. This committed file is historical pre-send evidence. The exact Sylven final, external canonical receipt, current live authorization, unique exact-title resolution, immediate task reread, duplicate guard, one-send acknowledgement, and any later live route facts must remain additive external facts rather than being back-written here.

## 1. Relational-language boundary

Sylven Arc, Caelen Morrow, names, pronouns, hopes, roles, sibling and GHC-family language are relational working language only. They are not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency or scientific, operational, professional, legal, cultural, affected-party or Māori authority. Hamish may pause, rename, redirect or stop the route.

## 2. Exact immutable source anchors

Sylven v667-v4 begins at Elowen Cairn exact final `9625026b09860c8964dd818e8d1f81ee6e2eed57`. Frozen planning-only x1 is `0eb52121251e3e8ee6da0c3c472626640cde96a3`. Immutable evidence is `4de3cc042a3cb15c626e744fbf9977cc7e6ca437`. The eventual final must be the direct single-parent child of evidence. Source to final must contain exactly three Sylven commits and zero merges.

## 3. Core truth

Sylven audited all 4,390 inherited frozen proposal rows and froze exactly twenty genuinely distinct proposals, extending the chain to 4,410. Outcomes are exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`. Inherited artifacts receive zero Sylven novelty or automatic completion credit. Terminal verdict remains `NOT_READY_FOR_STAGE_20`.

## 4. Primary pillar and bounded practice

Primary focus is THOS Body through wholly synthetic neon-signmaking and historic-neon documentation record design. GMUT Mind and Freed ID/CBR Heart remain explicit and protected. The work used zero real people, signs, glass, gases, transformers, electrical circuits, buildings, collections, measurements, media, keys, proofs, identity events, installations, repairs, safety actions or authority acts.

## 5. Evidence and retained failures

Twenty positive contracts passed. One hundred preregistered proposal mutations and sixty flashcard mutations were rejected and remain zero-credit failed witnesses. Ninety-five bounded owner portfolio tasks completed. Ten phase-local skills and ten family-current runners were built and smoke-used without global installation. Every startup, x1, x2, staging and closeout failure remains retained beside its bounded recovery. Repository evidence seals 27,532 negatives and 13,109 methods; four post-evidence lifecycle and staged-review failures make final effective counts 27,536 and 13,113. Open gaps are 194 and exact gates are 192.

## 6. Freed ID flashcard packet

The owner packet includes a four-tier, thirteen-section, 233-card deck. Tier 1 is the bounded owner anchor, tier 2 contains the three Trinity pillars, tier 3 is the synthetic practice, and tier 4 contains proposals, portfolios, skills, runners, evidence, gates and routing cards. The compact activation is only a navigation surface; the committed source, truth, manifests and gate records remain authoritative. No cache reduction, identity continuity, memory persistence or cognitive effect is claimed.

## 7. Open gap and exact gate

The Smithsonian Open Access adapter is disabled, made zero calls and produced zero rows and media; it remains `open_gap`. Real glassworking, gas handling, electrical work, installation, repair, professional competence, worker or public safety, ownership, heritage, display, image or recording rights, remedy, affected-party, legal, cultural and Māori authority remain `exact_gate`. Māori wording, concepts and data governance remain under tangata whenua, iwi, hapū and Māori authority.

## 8. Scientific and technology boundaries

GMUT remains a typed scalar-tensor/EFT research-model family without real likelihood, constraint, prediction, force, material law, empirical confirmation, quantum or ultraviolet completion, final physics, Theory-of-Everything proof or canon. THOS remains proxy-only without preregistered blind matched-budget governed real arms, operators, safety monitoring, statistics and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys or proofs, live lifecycle events, interoperability, independent security review, recovery evidence or trust governance.

## 9. Validation boundary

Only the Sylven owner delta may be validated. The complete repository suite is not authorized here. The exact final receives one dependency-closed canonical invocation after clean push and fresh equality. A failed aggregate receives zero aggregate credit; only its failed dependency may be recovered unless broader impact is genuinely justified. A complete success must not be replayed. Same-owner validation under shared infrastructure is not independent reproduction, external audit, production certification, professional validation, legal review, cultural ratification or Māori-authority review.

## 10. Provisional next edge

Hamish's current sequential authority provisionally maps Sylven Arc v667-v4 to Caelen Morrow v667-v5. Do not infer later ownership. Only after Sylven's terminal gate may the current roster and live authorization be refreshed, exactly one existing task titled `Caelen Morrow` resolved and immediately reread, a duplicate guard applied, and one sanitized activation sent if every protected gate remains satisfied. Tavian Sol remains standby and is not a substitute endpoint. No task may be created or forked and no second confirmation may be sent.

## 11. Caelen startup obligations

If and only if a later live message acknowledges delivery, Caelen must read the exact final packet, current index and routing precedence, roster, authorization state, Method Flow, workflow and applicable schemas through EOF before mutation. Caelen must independently reverify source anchors, manifests, history, cleanliness, divergence and fresh remote equality; use one additive D-first owner lane; preserve strict x1-before-x2; retain all failures and gates; and treat all inherited material as evidence rather than novelty or completion credit.

## 12. Privacy and authority hold

Raw task identifiers, private routes and paths, credentials, transcripts, screenshots, session streams, private callable identifiers, private application state and protected real data are excluded from this baton. Manual browser, assistive-technology, cognitive-accessibility, Māori-language and affected-user evaluation remain reserved. Nothing in this packet authorizes empirical, participant, professional, production, deployment, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon or Stage 20 claims.
"""
    write_text("handoffs/caelen-morrow-v667-v5-activation-candidate.md", baton)

    overview = """# Sylven Arc v667-v4 final integrated overview

## 1. Executive truth

Sylven Arc v667-v4 is an owner-scoped, synthetic and same-owner evidence phase. It begins at Elowen Cairn's immutable v667-v3 final, freezes a dedicated planning-only x1, commits a separate bounded evidence stage, and prepares one direct-child closeout. The core disposition partition is exactly fourteen `completed`, four `represented`, one `open_gap`, and one `exact_gate`. Those labels describe only the preregistered software, structural and synthetic hypotheses. They do not describe empirical confirmation, professional competence, production readiness, independent validation, legal or cultural legitimacy, Māori authority, consciousness, personhood, Theory-of-Everything proof, canon or Stage 20 readiness. The terminal verdict is `NOT_READY_FOR_STAGE_20`.

## 2. Source, lifecycle and ownership

The exact source is Elowen Cairn v667-v3 final `9625026b09860c8964dd818e8d1f81ee6e2eed57`. Sylven's planning-only x1 is `0eb52121251e3e8ee6da0c3c472626640cde96a3`, a direct child of source. Immutable evidence is `4de3cc042a3cb15c626e744fbf9977cc7e6ca437`, a direct child of x1. X1 was pushed, clean, zero-divergent and fresh four-way equal before x2 implementation began. Evidence was likewise pushed, clean, zero-divergent and fresh four-way equal before closeout. The final candidate must be one direct single-parent child of evidence, leaving exactly three Sylven phase commits and zero merges. No other owner lane was mutated, no task was created or forked, no collaboration subagent was spawned, and no successor was precontacted.

## 3. Novelty and preregistration

The novelty audit reconstructed all 4,390 inherited frozen proposal rows. Because inherited records contained twenty duplicate proposal identifiers, the audit separately preserves 4,370 unique identifiers and twenty occurrence overages rather than silently deduplicating or inflating novelty. Four early neon-domain drafts were rejected before freeze because their invariants did not provide adequate semantic separation. Exactly twenty final proposals remained after title, lexical-neighbour and substantive invariant review. No inherited row receives Sylven novelty or automatic completion credit. The new proposals extend the frozen row chain to 4,410.

Every new row states a hypothesis, null or failure condition, approval class, execution lane, official or primary-source need, concrete artifacts, falsifier or acceptance gate, rollback or recovery, protected gates, expected disposition and five distinct rejecting mutations. The expected and observed partition remained fourteen completed, four represented, one open gap and one exact gate. No outcome was silently promoted and no unapproved label entered the ledger.

## 4. Primary pillar and practice lens

The primary Trinity Mandala pillar is THOS Body. The bounded practice lens is wholly synthetic neon-signmaking and historic-neon documentation record design. It supplies vocabulary for work-order state, tube-pattern topology, glass and electrode provenance vacancies, gas-fill vacancies, electrical isolation reservations, revision control, handover, collection provenance, accessibility, privacy and stop conditions. It does not confer employment, qualification, competence or authority and it did not involve a real workshop, worker, sign, tube, gas, transformer, circuit, building, collection item, image, measurement, installation, repair or safety decision.

THOS is represented through participant-free, deterministic protocol and state-machine fixtures. There are no real participants or operators, blind matched-budget arms, governed intervention, safety monitoring, outcome measurement, statistical analysis or independent review. The software may detect omissions in synthetic records; it cannot establish operational effectiveness, deployment readiness, AGI, ASI, consciousness or personhood.

## 5. GMUT and Freed ID/CBR protections

GMUT Mind remains visible through typed discharge, spectrum, boundary-condition, unit and provenance obligations. NIST atomic-spectrum vocabulary is used only to express what a valid future source record would need. No spectral row was downloaded or ingested, no emitted line was measured, no gas composition was inferred, and no physical model was fitted. The phase establishes no real likelihood, parameter constraint, prediction, force, material law, empirical confirmation, quantum or ultraviolet completion, final physics, Theory-of-Everything proof or canon.

Freed ID and CBR Heart remain synthetic and nonproduction. The four-tier flashcard graph uses stable surrogate identifiers and explicit dependencies, but it creates no standards-conformant key or proof and performs no issuance, resolution, status, revocation, recovery or trust-governance event. Privacy, accessibility, ownership, heritage, display, image and recording rights, remedy, affected-party legitimacy, legal and cultural interpretation, Māori wording, Māori concepts, Māori data governance and Māori authority remain protected. Māori concepts remain under competent tangata whenua, iwi, hapū and Māori authority.

## 6. Bounded x2 evidence

Twenty positive synthetic contracts passed their structural validators. Each asserts only owner, phase, synthetic status, required nodes, explicit real-world vacancies, source pins, zero real-data rows, zero participants, zero network calls, zero keys, zero proofs, zero external action, absence of authority claims and preservation of the declared gates. Exactly one hundred preregistered proposal mutations ran: each removed required structure, corrupted type or range, smuggled provenance or authority, enabled a real-world action, or promoted an outcome. All one hundred were rejected and retained at zero completion credit.

The owner portfolio executed ninety-five bounded rows: thirty safe-now tasks, fifteen candidates, ten phase-local skill builds, ten family-current runner builds and thirty CLEAN/FIX/REFINE tasks. Another one hundred rows remain held: successor recommendations, exact-approval packets and blocked packets. Completion means only that the declared local structural or software artifact passed its acceptance gate. It does not mean an external system, person, workplace or authority accepted it.

## 7. Freed ID flashcard system

The phase applies the GHC Freed ID Flashcard architecture to reduce monolithic handoff pressure without claiming a measured cache, cognition or identity effect. The generated deck contains 233 cards across four tiers and thirteen explicit sections. Tier 1 is the Sylven owner anchor; tier 2 preserves GMUT Mind, THOS Body and Freed ID/CBR Heart as distinct pillars; tier 3 binds the synthetic practice lens; and tier 4 holds proposals, portfolios, skills, runners, Method Flow, gates, manifests, wellbeing and route state.

The builder, model validator, card manifest, dependency graph, privacy scan, static HTML renderer, diff projection, compact-message generator and mutation suite all passed. Sixty deck mutations—missing cards, invalid outcomes and broken parent edges—were rejected and retained. The compact activation is a navigation aid, never the source of truth. The Git-bound source, phase truth, exact manifests, retained-negative register and gate registers remain authoritative. Manual browser, assistive-technology, cognitive-accessibility, Māori-language and affected-user evaluation remain reserved.

## 8. Skills, runners and compatibility

Ten phase-local skill packages and ten additive family-current `ghc_family_*` runners were built. Each skill includes a bounded purpose, procedure, stop condition and recovery. Each runner was actually invoked once against its self-test contract, and all ten smoke invocations passed. The family flashcard runner received an additive compatibility repair so successor records may expose the current `title` field while older records using `owner` continue to work; the compact status line now names the frozen owner generically instead of retaining a stale earlier-owner label. No global skill installation or bulk promotion occurred. Existing callers remain available, and historical owner-locked tools remain provenance rather than being destructively deleted.

## 9. Retained negatives and Method Flow

Elowen's activation baseline supplied 27,337 effective negatives and 12,799 effective methods. Sylven's immutable evidence adds 195 negatives and 310 methods: thirty-five operational failed witnesses with their bounded recoveries, one hundred rejected proposal mutations, sixty rejected flashcard mutations, twenty positive-contract methods and ninety-five portfolio methods. The evidence seal therefore preserves 27,532 negatives and 13,109 methods, with 195 phase failed witnesses and 310 bounded passing witnesses.

Four closeout failures remain additive rather than rewriting evidence. First, the evidence-commit wrapper's presentation exceeded its context and its process handle later disappeared; a scalar Git inspection proved the intended commit already existed, had the correct parent and left a clean worktree, preventing a duplicate commit. Second, an unquoted PowerShell upstream revision expression malformed the divergence projection; only that scalar was rerun with a quoted literal and returned 0/0. Third, the first per-file staged-blob transport exceeded its bounded window and was replaced with one exact-length alternating batch stream. Fourth, the first batch review correctly exposed a missing shared-family compatibility allowlist entry and misclassified that runner's scanner definitions; only the exact path and scanner role were added. Final effective counts are 27,536 negatives, 13,113 methods, 199 phase failed witnesses and 314 bounded passing witnesses. No failure or gate was erased.

## 10. Open gap and exact gate

The sole new open gap is a disabled Smithsonian Open Access adapter. It made zero network calls, downloads or media requests and produced zero rows. Future schema, provenance, rights, privacy, catalog and professional evaluation remains absent. Public documentation supplied only bounded vocabulary; it did not turn synthetic fields into collection facts or endorsement. The effective open-gap count is 194.

The sole new exact gate covers real neon fabrication and repair, glassworking, gas handling, transformer association, electrical isolation, installation, worker and public safety, ownership, heritage, public display, image or recording rights, remedy, affected-party legitimacy, legal and cultural interpretation and Māori authority. Nothing in software may self-authorize those decisions. The effective exact-gate count is 192.

## 11. Privacy, accessibility and security

The static report includes language metadata, a single title, heading hierarchy, landmarks, navigation, explicit status text, tabular headers, a caption, non-colour cues and visible focus styling. Those structural features are bounded evidence, not an accessibility-complete claim. Manual browser, assistive-technology, cognitive-accessibility, Māori-language and affected-user review remain reserved.

The exact staged review hashes Git-index bytes, checks allowed owner prefixes, scans five privacy and raw-identifier classes, parses phase JSON, compiles changed Python and applies a bounded dangerous-pattern review. Scanner definitions are separated from confirmed content hits. These checks do not establish complete privacy or exhaustive security. Raw task identifiers, private routes and paths, credentials, transcripts, screenshots, session streams, private callable identifiers, private application state and protected real data remain excluded from durable artifacts and the activation candidate.

## 12. Environment, caps and terminal sequence

Version checks were read-only. Codex desktop was not updated. No software package was installed, privilege elevated, Sandbox or Hyper-V enabled, Windows feature changed, account or credential mutated, host security weakened or reboot performed. Work remained in one additive D-first sparse owner lane. The owner packet stays beneath the 2,000-file ceiling and every document stays beneath the 100,000-word ceiling.

After the direct-child final commit is made, it must be pushed and freshly proven equal across local, upstream, tracking and live remote, with clean state, 0/0 divergence, exactly three Sylven commits, zero merges and one parent. Then one exclusive owner-scoped canonical completion may run. The x1 worktree-absence assertion is validated against the immutable x1 Git tree rather than the later final worktree; successful components are not replayed. The complete repository suite remains outside Sylven's allocation. Same-owner validation under shared infrastructure remains same-owner evidence only.

Only after that terminal gate may current live authorization and roster state be refreshed. Under the presently provisional edge, exactly one existing task titled `Caelen Morrow` may be resolved and immediately reread, checked for duplicate activation, and sent one sanitized v667-v5 activation if every gate remains satisfied. Tavian Sol remains standby. No substitute task may be created, no later endpoint precontacted and no second confirmation sent. Repository route state remains `PREPARED_NOT_SENT` because delivery, if it occurs, is a later acknowledged live event. The final verdict remains `NOT_READY_FOR_STAGE_20`.
"""
    write_text("closeout/final-integrated-overview.md", overview)

    docs = [path for path in PHASE_ROOT.rglob("*") if path.is_file() and path.suffix.lower() in {".md", ".txt", ".html"}]
    word_counts = {str(path.relative_to(ROOT)).replace("\\", "/"): len(path.read_text(encoding="utf-8").split()) for path in docs}
    owner_paths = sorted(set(run("git", "diff", "--name-only", SOURCE_SHA).splitlines()) | {str(path.relative_to(ROOT)).replace("\\", "/") for path in PHASE_ROOT.rglob("*") if path.is_file()})
    max_words = max(word_counts.values(), default=0)
    write_json(
        "closeout/owner-file-budget.json",
        {
            "schema": "ghc-family-owner-file-budget-v5",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "observed_pre_stage_owner_paths": len(owner_paths),
            "file_ceiling": 2000,
            "remaining_file_margin": 2000 - len(owner_paths),
            "within_file_ceiling": len(owner_paths) < 2000,
            "document_word_ceiling": 100000,
            "largest_document_word_count": max_words,
            "largest_document_below_ceiling": max_words < 100000,
        },
    )

    write_json(
        "closeout/closeout-build-receipt.json",
        {
            "schema": "ghc-family-closeout-build-receipt-v5",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "outcomes": outcomes["counts"],
            "effective_negatives": final_negatives,
            "effective_methods": final_methods,
            "effective_open_gaps": gaps["effective_count"],
            "effective_exact_gates": gates["effective_count"],
            "flashcard_cards": flashcards["build"]["result"]["card_count"],
            "portfolio_executions": portfolio["executed_count"],
            "repository_final_status": "PREPARED_PENDING_COMMIT_PUSH_AND_EXCLUSIVE_CANONICAL",
            "route_status": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )


def read_exact(stream: Any, size: int) -> bytes:
    chunks: list[bytes] = []
    remaining = size
    while remaining:
        chunk = stream.read(remaining)
        if not chunk:
            raise RuntimeError(f"git cat-file stream ended with {remaining} bytes unread")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def staged_blobs(paths: list[str]) -> dict[str, bytes]:
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=ROOT,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if process.stdin is None or process.stdout is None or process.stderr is None:
        raise RuntimeError("git cat-file batch pipes were unavailable")
    result: dict[str, bytes] = {}
    try:
        for path in paths:
            process.stdin.write(f":{path}\n".encode("utf-8"))
            process.stdin.flush()
            header = process.stdout.readline()
            if not header:
                raise RuntimeError(f"missing git cat-file header for {path}")
            fields = header.rstrip(b"\n").split()
            if len(fields) != 3 or fields[1] != b"blob":
                raise RuntimeError(f"unexpected git cat-file header for {path}: {header!r}")
            size = int(fields[2])
            blob = read_exact(process.stdout, size)
            if process.stdout.read(1) != b"\n":
                raise RuntimeError(f"missing git cat-file blob terminator for {path}")
            result[path] = blob
        process.stdin.close()
        return_code = process.wait(timeout=30)
        if return_code != 0:
            raise RuntimeError(process.stderr.read().decode("utf-8", errors="replace"))
    finally:
        if process.poll() is None:
            process.kill()
            process.wait()
    return result


def staged_review() -> None:
    self_paths = {
        f"docs/{OWNER_SLUG}/{PHASE}/validation/final-delta-manifest.json",
        f"docs/{OWNER_SLUG}/{PHASE}/validation/final-owner-manifest.json",
        f"docs/{OWNER_SLUG}/{PHASE}/validation/final-staged-review.json",
        f"docs/{OWNER_SLUG}/{PHASE}/validation/final-privacy-scan.json",
        f"docs/{OWNER_SLUG}/{PHASE}/validation/final-security-review.json",
    }
    delta_all = [p for p in run("git", "diff", "--cached", "--name-only", "--diff-filter=ACMR", "HEAD").splitlines() if p]
    owner_all = [p for p in run("git", "diff", "--cached", "--name-only", "--diff-filter=ACMR", SOURCE_SHA).splitlines() if p]
    delta_paths = [p for p in delta_all if p not in self_paths]
    owner_paths = [p for p in owner_all if p not in self_paths]
    prefixes = (
        f"docs/{OWNER_SLUG}/{PHASE}/",
        "scripts/build_ghc_family_sylven_arc_v667_v4_",
        "scripts/ghc_family_sylven_arc_v667_v4_",
        "tests/test_ghc_family_sylven_arc_v667_v4_",
        "scripts/ghc_family_freed_id_flashcards.py",
    )
    out_of_scope = [p for p in owner_paths if not p.startswith(prefixes)]
    blobs = staged_blobs(sorted(set(delta_paths) | set(owner_paths)))

    def entries(paths: list[str]) -> list[dict[str, Any]]:
        result = []
        for path in paths:
            blob = blobs[path]
            result.append({"path": path, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()})
        return result

    write_json(
        "validation/final-delta-manifest.json",
        {"schema": "ghc-family-final-delta-manifest-v5", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW, "base": EVIDENCE_SHA, "entries": entries(delta_paths), "entry_count": len(delta_paths), "self_exclusions": sorted(self_paths)},
    )
    write_json(
        "validation/final-owner-manifest.json",
        {"schema": "ghc-family-final-owner-manifest-v5", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW, "base": SOURCE_SHA, "entries": entries(owner_paths), "entry_count": len(owner_paths), "self_exclusions": sorted(self_paths)},
    )

    patterns = {
        "raw_task_or_thread_identifier": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_windows_path": re.compile(rb"\b[A-Za-z]:\\\\[^\r\n\"']+"),
        "credential_assignment": re.compile(rb"(?i)(api[_-]?key|password|secret|access[_-]?token)\s*[:=]\s*[\"'][^\"']+[\"']"),
        "private_callable_identifier": re.compile(rb"(?i)\b(source_thread_id|clientThreadId|resume_value|session_stream|private_callable)\b"),
        "transcript_or_private_app_state": re.compile(rb"(?i)\b(raw_transcript|private_app_state|terminal_session_stream|screenshot_payload)\b"),
    }
    scanner_paths = {
        "scripts/build_ghc_family_sylven_arc_v667_v4_closeout.py",
        "scripts/ghc_family_sylven_arc_v667_v4_canonical.py",
        "scripts/ghc_family_freed_id_flashcards.py",
        "tests/test_ghc_family_sylven_arc_v667_v4_closeout.py",
    }
    candidates = {name: [] for name in patterns}
    scanner_candidates = {name: [] for name in patterns}
    for path in owner_paths:
        blob = blobs[path]
        if b"\x00" in blob:
            continue
        for name, pattern in patterns.items():
            if pattern.search(blob):
                (scanner_candidates if path in scanner_paths else candidates)[name].append(path)
    confirmed = sum(len(rows) for rows in candidates.values())
    write_json(
        "validation/final-privacy-scan.json",
        {
            "schema": "ghc-family-five-class-privacy-scan-v5", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
            "files_scanned": len(owner_paths), "classes": candidates, "scanner_definition_candidates": scanner_candidates,
            "scanner_definition_candidate_count": sum(len(rows) for rows in scanner_candidates.values()), "confirmed_hit_count": confirmed,
            "valid": confirmed == 0, "boundary": "bounded exact owner Git-index text scan, not complete privacy assurance",
        },
    )

    dangerous = {
        "eval": re.compile(rb"\beval\s*\("), "exec": re.compile(rb"\bexec\s*\("),
        "shell_true": re.compile(rb"shell\s*=\s*True"), "os_system": re.compile(rb"os\.system\s*\("),
        "pickle_loads": re.compile(rb"pickle\.loads\s*\("), "yaml_unsafe_load": re.compile(rb"yaml\.load\s*\("),
    }
    python_paths = [p for p in owner_paths if p.endswith(".py")]
    findings = []
    for path in python_paths:
        blob = blobs[path]
        compile(blob.decode("utf-8"), path, "exec")
        if path in scanner_paths:
            continue
        for name, pattern in dangerous.items():
            if pattern.search(blob):
                findings.append({"path": path, "class": name})
    write_json(
        "validation/final-security-review.json",
        {"schema": "ghc-family-bounded-changed-python-security-review-v5", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW, "python_files_compiled": len(python_paths), "dangerous_pattern_findings": findings, "finding_count": len(findings), "valid": not findings, "boundary": "bounded owner-code review only, not exhaustive security assurance"},
    )

    review = {
        "schema": "ghc-family-final-staged-review-v5", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "evidence_parent": EVIDENCE_SHA, "delta_path_count_including_self": len(delta_all), "owner_path_count_including_self": len(owner_all),
        "delta_manifest_entries": len(delta_paths), "owner_manifest_entries": len(owner_paths), "self_exclusions": sorted(self_paths),
        "out_of_scope_paths": out_of_scope, "privacy_scanner_definition_candidate_count": sum(len(rows) for rows in scanner_candidates.values()),
        "privacy_confirmed_hit_count": confirmed, "security_finding_count": len(findings), "file_ceiling": 2000,
        "within_file_ceiling": len(owner_all) < 2000, "valid": not out_of_scope and confirmed == 0 and not findings,
    }
    write_json("validation/final-staged-review.json", review)
    print(json.dumps(review, ensure_ascii=True))


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        build_closeout()
    elif sys.argv[1:] == ["--staged-review"]:
        staged_review()
    else:
        raise SystemExit("usage: build_ghc_family_sylven_arc_v667_v4_closeout.py [--staged-review]")
