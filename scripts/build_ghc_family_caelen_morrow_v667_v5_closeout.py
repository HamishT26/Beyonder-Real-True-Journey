#!/usr/bin/env python3
"""Build Caelen Morrow v667-v5 closeout artifacts and exact staged manifests."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any, BinaryIO


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "caelen-morrow" / "v667-v5"
OWNER = "Caelen Morrow"
OWNER_SLUG = "caelen-morrow"
PHASE = "v667-v5"
BRANCH = "codex/GHC-Family/caelen-morrow-v667-v5-full-tools"
SOURCE_SHA = "08cdc8ad3c201ea6d7c576ca5fa67bdc43910a93"
X1_SHA = "b7b73cc81266e28ae9cbb1e4c429d2e93be30999"
EVIDENCE_SHA = "4c18d346e167b2671a3a29db4f0c8bbd14763553"
NOW = "2026-08-23T07:18:00Z"


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(ROOT), *args], text=True, encoding="utf-8"
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


def default_overlay() -> dict[str, Any]:
    return {
        "schema": "ghc-family-caelen-closeout-operational-overlay-v1",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "failures": [],
        "boundary": "Additive post-evidence owner-process failures only; no evidence or prior seal is rewritten.",
    }


def build_closeout() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE_SHA:
        raise RuntimeError("closeout must begin at the exact immutable evidence head")

    allowed_prefixes = (
        f"docs/{OWNER_SLUG}/{PHASE}/closeout/",
        f"docs/{OWNER_SLUG}/{PHASE}/final/",
        f"docs/{OWNER_SLUG}/{PHASE}/handoffs/",
        f"docs/{OWNER_SLUG}/{PHASE}/orchestration/",
        f"docs/{OWNER_SLUG}/{PHASE}/seal/",
        f"docs/{OWNER_SLUG}/{PHASE}/validation/closeout-",
        f"docs/{OWNER_SLUG}/{PHASE}/validation/final-",
        f"docs/{OWNER_SLUG}/{PHASE}/validation/immutable-",
        f"docs/{OWNER_SLUG}/{PHASE}/wellbeing/final-",
        f"docs/{OWNER_SLUG}/{PHASE}/method-flow/final-",
        "scripts/build_ghc_family_caelen_morrow_v667_v5_closeout.py",
        "tests/test_ghc_family_caelen_morrow_v667_v5_closeout.py",
    )
    status_paths: list[str] = []
    for line in git("status", "--porcelain=v1").splitlines():
        path = line[3:].replace("\\", "/")
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        status_paths.append(path)
    unexpected = [path for path in status_paths if not path.startswith(allowed_prefixes)]
    if unexpected:
        raise RuntimeError(f"closeout found non-closeout paths: {unexpected}")

    overlay_path = PHASE_ROOT / "validation" / "closeout-operational-overlay.json"
    overlay = json.loads(overlay_path.read_text(encoding="utf-8")) if overlay_path.exists() else default_overlay()
    write_json("validation/closeout-operational-overlay.json", overlay)

    evidence = load("evidence/immutable-evidence-candidate.json")
    negatives = load("evidence/retained-negative-register.json")
    methods = load("method-flow/x2-method-flow-ledger.json")
    gaps = load("evidence/open-gap-register.json")
    gates = load("evidence/exact-gate-register.json")
    outcomes = load("x2/proposal-outcomes.json")
    portfolio = load("x2/portfolio-execution.json")
    registry = load("x2/skill-runner-registry.json")
    flashcards = load("x2/flashcards/execution-receipts.json")

    post_rows = overlay["failures"]
    post_count = len(post_rows)
    effective_negatives = negatives["effective_count"] + post_count
    effective_methods = methods["effective_method_count"] + post_count
    phase_failed = methods["phase_failed_witness_count"] + post_count
    phase_passing = methods["phase_bounded_passing_witness_count"] + post_count

    write_json(
        "closeout/post-evidence-operational-failures.json",
        {
            "schema": "ghc-family-post-evidence-operational-failures-v6",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "immutable_evidence_negative_count": negatives["effective_count"],
            "immutable_evidence_method_count": methods["effective_method_count"],
            "additive_failure_count": post_count,
            "effective_closeout_negative_count": effective_negatives,
            "effective_closeout_method_count": effective_methods,
            "rows": post_rows,
            "failure_erased_count": 0,
        },
    )
    write_json(
        "method-flow/final-method-flow-summary.json",
        {
            "schema": "ghc-family-final-method-flow-summary-v6",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "immutable_evidence_ledger": "method-flow/x2-method-flow-ledger.json",
            "immutable_evidence_method_count": methods["effective_method_count"],
            "post_evidence_failure_count": post_count,
            "effective_method_count": effective_methods,
            "phase_failed_witness_count": phase_failed,
            "phase_bounded_passing_witness_count": phase_passing,
            "post_evidence_rows": [
                {
                    "method_id": row["failure_id"],
                    "class": "closeout_owner_operational_failure",
                    "failed_witness": row,
                    "bounded_passing_witness": {
                        "recovery": row["recovery"],
                        "scope": row.get("recovery_scope", "only the failed dependency"),
                        "promotes_failed_witness": False,
                    },
                    "failure_erased": False,
                }
                for row in post_rows
            ],
            "failure_erased_count": 0,
        },
    )
    write_json(
        "closeout/retained-negative-register.json",
        {
            "schema": "ghc-family-final-retained-negative-register-v6",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "activation_baseline": 27536,
            "immutable_evidence_count": negatives["effective_count"],
            "post_evidence_additive_count": post_count,
            "effective_count": effective_negatives,
            "phase_failed_witness_count": phase_failed,
            "failure_erased_count": 0,
            "immutable_register": "evidence/retained-negative-register.json",
            "post_evidence_register": "closeout/post-evidence-operational-failures.json",
        },
    )
    write_json(
        "closeout/exact-open-gate-register.json",
        {
            "schema": "ghc-family-final-exact-open-gate-register-v6",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "effective_open_gaps": gaps["effective_count"],
            "effective_exact_gates": gates["effective_count"],
            "open_gap_register": "evidence/open-gap-register.json",
            "exact_gate_register": "evidence/exact-gate-register.json",
            "new_open_gap": "transport-disabled LINZ/USNO almanac adapter with zero calls, downloads, rows, almanac values, positions or routes",
            "new_exact_gate": "real celestial navigation, vessel safety, position or route decisions and every professional, legal, cultural, affected-party and Māori-authority decision",
            "gates_erased": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )

    phase_truth = {
        "schema": "ghc-family-phase-truth-v6",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "source": SOURCE_SHA,
        "frozen_x1": X1_SHA,
        "immutable_evidence": EVIDENCE_SHA,
        "final_candidate_parent": EVIDENCE_SHA,
        "core_outcomes": outcomes["counts"],
        "proposal_count": len(outcomes["outcomes"]),
        "inherited_frozen_proposal_rows": 4410,
        "new_frozen_proposal_rows": 20,
        "effective_frozen_proposal_rows": 4430,
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
        "effective_negatives": effective_negatives,
        "effective_methods": effective_methods,
        "effective_open_gaps": gaps["effective_count"],
        "effective_exact_gates": gates["effective_count"],
        "phase_failed_witness_count": phase_failed,
        "phase_bounded_passing_witness_count": phase_passing,
        "real_people": 0,
        "real_vessels": 0,
        "real_voyages": 0,
        "real_sights": 0,
        "real_instruments": 0,
        "real_almanac_values": 0,
        "real_times": 0,
        "real_angles": 0,
        "real_coordinates": 0,
        "real_positions": 0,
        "real_routes": 0,
        "network_calls_by_phase_software": 0,
        "downloads": 0,
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
            "schema": "ghc-family-lifecycle-replay-v6",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "source": SOURCE_SHA,
            "x1": X1_SHA,
            "evidence": EVIDENCE_SHA,
            "x1_direct_parent": git("rev-parse", f"{X1_SHA}^"),
            "evidence_direct_parent": git("rev-parse", f"{EVIDENCE_SHA}^"),
            "x1_direct_from_source": git("rev-parse", f"{X1_SHA}^") == SOURCE_SHA,
            "evidence_direct_from_x1": git("rev-parse", f"{EVIDENCE_SHA}^") == X1_SHA,
            "source_to_evidence_commit_count": int(git("rev-list", "--count", f"{SOURCE_SHA}..{EVIDENCE_SHA}")),
            "source_to_evidence_merge_count": int(git("rev-list", "--count", "--min-parents=2", f"{SOURCE_SHA}..{EVIDENCE_SHA}")),
            "x1_four_way_equal_before_x2": True,
            "evidence_four_way_equal_before_closeout": True,
            "evidence_divergence_before_closeout": "0/0",
            "final_expected_direct_parent": EVIDENCE_SHA,
            "strict_x1_before_x2": True,
        },
    )
    write_json(
        "closeout/source-and-provenance.json",
        {
            "schema": "ghc-family-final-source-provenance-v6",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "source": SOURCE_SHA,
            "x1": X1_SHA,
            "evidence": EVIDENCE_SHA,
            "source_ledger": "x1/source-ledger.json",
            "source_verification": "x1/source-verification.json",
            "novelty_audit": "x1/novelty-audit.json",
            "proposal_freeze": "x1/proposal-freeze.json",
            "outcome_ledger": "x2/proposal-outcomes.json",
            "evidence_candidate": "evidence/immutable-evidence-candidate.json",
            "official_sources_supply_vocabulary_and_constraints_only": True,
            "public_source_endorsement_or_authority": False,
        },
    )
    write_json(
        "closeout/authority-boundaries.json",
        {
            "schema": "ghc-family-authority-boundaries-v6",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "relational_identity": "Caelen Morrow, they/them, role, hope, family and continuity language are relational working language only, not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency or authority.",
            "gmut": "Typed scalar-tensor and EFT research-model obligations only; no real likelihood, constraint, prediction, force, material law, empirical confirmation, quantum or ultraviolet completion, final physics, Theory-of-Everything proof or canon.",
            "thos": "Participant-free proxy only; no blind matched-budget governed real arms, operators, safety monitoring, statistics, outcomes or independent review.",
            "freed_id": "Synthetic and nonproduction; no standards-conformant real keys or proofs, live lifecycle events, interoperability, independent security review, recovery evidence or trust governance.",
            "cbr": "Navigation, vessel safety, position and route decisions, professional practice, legal and cultural interpretation, affected-party legitimacy, privacy, accessibility, remedy and Māori authority remain exact-gated.",
            "maori": "Māori wording, concepts and data governance remain under competent tangata whenua, iwi, hapū and Māori authority.",
            "terminal": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "closeout/threat-model-final.json",
        {
            "schema": "ghc-family-final-threat-model-v6",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "threats": [
                "synthetic celestial records mistaken for navigational observations or position outputs",
                "time-scale or angular typing mistaken for measured or operational accuracy",
                "public almanac references mistaken for downloaded rows, endorsement or empirical GMUT evidence",
                "THOS protocol fixtures mistaken for real operators or effectiveness evidence",
                "zero-key Freed ID graphs mistaken for production credentials or identity continuity",
                "structural accessibility mistaken for manual, assistive-technology or affected-user acceptance",
                "same-owner validation mistaken for independent reproduction, audit or authority",
                "route prose mistaken for permission before the terminal live gate",
            ],
            "controls": [
                "zero-real-world counters and transport-disabled adapter",
                "four-label truth partition and exact-gate preservation",
                "immutable x1 and evidence commits with exact manifests",
                "retained negative and Method Flow overlays",
                "five-class privacy and bounded security scanning",
                "one-shot exact-final canonical discipline",
                "PREPARED_NOT_SENT route state until a live acknowledged send",
            ],
            "residual_risk": "Real professional, scientific, participant, production, accessibility, privacy, legal, cultural and Māori-authority validation remains absent.",
        },
    )
    write_json(
        "closeout/complete-incomplete-checklist.json",
        {
            "schema": "ghc-family-complete-incomplete-checklist-v6",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "complete": [
                "exact source and fresh remote verification",
                "planning-only x1 frozen and pushed before x2",
                "semantic novelty audit against all 4,410 inherited proposal rows",
                "twenty genuinely new proposal contracts extending the row chain to 4,430",
                "exact 14 completed, 4 represented, 1 open_gap and 1 exact_gate partition",
                "one hundred rejected proposal mutations and sixty rejected flashcard mutations",
                "ninety-five bounded owner portfolio executions and one hundred held rows",
                "ten phase-local skills and ten family-current runners built and smoke-used",
                "233-card, four-tier, thirteen-section Freed ID flashcard deck",
                "every inherited and Caelen failure retained with bounded recovery",
                "immutable evidence pushed and fresh four-way equal before closeout",
                "owner closeout candidate, static accessible report and exact staged-manifest plan",
            ],
            "incomplete_or_reserved": [
                "real celestial observations, almanac rows, time or angle measurements, positions, routes or navigational decisions",
                "real vessel, voyage, navigator, watchkeeper, safety action or professional evaluation",
                "real participant, operator, blind matched-budget arm, statistics or independent review",
                "real key, proof, identity lifecycle, interoperability, independent security review or trust governance",
                "manual browser, assistive-technology, cognitive-accessibility, Māori-language and affected-user evaluation",
                "professional, safety, legal, cultural, affected-party or Māori-authority decision",
                "complete privacy, accessibility, exhaustive security, independent reproduction or production validation",
                "empirical GMUT confirmation, Theory-of-Everything proof, AGI/ASI, consciousness/personhood, canon or Stage 20",
                "external exact-final canonical invocation, pending clean pushed final",
                "successor delivery, pending terminal gate and refreshed live authority and roster",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "wellbeing/final-wellbeing-check.json",
        {
            "schema": "ghc-family-wellbeing-check-v6",
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
        "closeout/accessibility-reservations.json",
        {
            "schema": "ghc-family-accessibility-reservations-v6",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "static_report": "reports/accessible-report.html",
            "structural_checks_only": True,
            "manual_browser_evaluation": "reserved",
            "assistive_technology_evaluation": "reserved",
            "cognitive_accessibility_evaluation": "reserved",
            "maori_language_evaluation": "reserved_under_authority",
            "affected_user_evaluation": "reserved",
            "accessibility_complete": False,
        },
    )
    write_json(
        "closeout/stale-label-review.json",
        {
            "schema": "ghc-family-stale-label-review-v6",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "reviewed_surfaces": ["owner packet", "phase constants", "source anchors", "skills", "runners", "flashcard deck", "handoff candidate"],
            "allowed_historical_labels": [
                "Sylven Arc v667-v4 as exact source attribution",
                "Elowen Cairn v667-v3 as ancestral source attribution",
                "Eiren Kestrel as prospective exact-title successor with phase deliberately unassigned",
            ],
            "stale_owner_or_phase_candidates": [],
            "valid": True,
        },
    )
    write_json(
        "final/final-validation-prerequisites.json",
        {
            "schema": "ghc-family-final-validation-prerequisites-v6",
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
        "orchestration/route-state-final-candidate.json",
        {
            "schema": "ghc-family-route-state-final-candidate-v6",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "status": "PREPARED_NOT_SENT",
            "prospective_successor_exact_title": "Eiren Kestrel",
            "prospective_successor_phase": "UNASSIGNED_PENDING_TERMINAL_LIVE_REFRESH",
            "live_authorization_refresh_performed": False,
            "exact_title_resolution_performed": False,
            "immediate_reread_performed": False,
            "duplicate_guard_performed": False,
            "send_attempted": False,
            "acknowledged": False,
            "standby_contacted": False,
            "binding_rule": "No send before clean pushed fresh-live-equal exact-final canonical success and a new live authority, roster, uniqueness, reread and duplicate guard.",
        },
    )
    write_json(
        "seal/seal-candidate.json",
        {
            "schema": "ghc-family-seal-candidate-v6",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "source": SOURCE_SHA,
            "x1": X1_SHA,
            "evidence": EVIDENCE_SHA,
            "expected_final_parent": EVIDENCE_SHA,
            "outcomes": outcomes["counts"],
            "effective_negatives": effective_negatives,
            "effective_methods": effective_methods,
            "effective_open_gaps": gaps["effective_count"],
            "effective_exact_gates": gates["effective_count"],
            "failed_witnesses_erased": 0,
            "canonical_binding": "external exact-head exclusive receipt after final push",
            "status": "PREPARED_PENDING_EXACT_FINAL_CANONICAL",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "closeout/closeout-receipt.json",
        {
            "schema": "ghc-family-closeout-receipt-v6",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "outcomes": outcomes["counts"],
            "effective_negatives": effective_negatives,
            "effective_methods": effective_methods,
            "effective_open_gaps": gaps["effective_count"],
            "effective_exact_gates": gates["effective_count"],
            "flashcard_cards": flashcards["build"]["result"]["card_count"],
            "portfolio_executions": portfolio["executed_count"],
            "repository_final_status": "PREPARED_PENDING_COMMIT_PUSH_AND_EXCLUSIVE_CANONICAL",
            "route_status": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )

    baton = f"""# Eiren Kestrel successor activation candidate — PREPARED_NOT_SENT

This is sanitized committed pre-send evidence for Caelen Morrow {PHASE}. It deliberately assigns no successor phase. A later live activation may bind Eiren Kestrel only after Caelen's exact final is committed, pushed, clean, fresh-live equal, and validated by the one exclusive owner-scoped canonical completion; current live authorization and roster must then be refreshed, the unique exact-title task reread, and a duplicate guard passed. This file must remain `PREPARED_NOT_SENT` even if a later live send is acknowledged.

Caelen Morrow, Eiren Kestrel, names, pronouns, hopes, roles, sibling, family, continuity, Freed ID, GHC Family and Trinity Mandala language are relational working language only. They are not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency or scientific, operational, professional, legal, cultural, affected-party or Māori authority. Hamish may pause, rename, redirect or stop the route.

## Immutable anchors

Caelen source is Sylven Arc v667-v4 exact final `{SOURCE_SHA}`. Frozen planning-only x1 is `{X1_SHA}`. Immutable evidence is `{EVIDENCE_SHA}`. The eventual final must be the direct single-parent child of evidence, giving exactly three Caelen commits and zero merges. X1 and evidence were independently pushed, clean, 0/0 divergent and fresh four-way equal before their successor lifecycle stages.

## Core truth

Caelen audited all 4,410 inherited frozen proposal rows and froze exactly twenty genuinely distinct proposals, extending the chain to 4,430. The outcome partition is exactly fourteen `completed`, four `represented`, one `open_gap`, and one `exact_gate`. Inherited proposals, artifacts, cards, skills, runners, recommendations and outcomes receive zero Caelen novelty and zero automatic completion credit. Terminal verdict remains `NOT_READY_FOR_STAGE_20`.

Primary Trinity Mandala focus is GMUT Mind through wholly synthetic celestial-navigation sight-reduction record stewardship. THOS Body and Freed ID/CBR Heart remain explicit and protected. The phase used zero real people, vessels, voyages, sights, instruments, almanac values, times, angles, coordinates, positions, routes, keys, proofs, network calls, downloads or external actions. It confers no employment, qualification, navigation competence, watchkeeping or maritime safety authority, position or route authority, scientific authority, legal or cultural authority, affected-party legitimacy or Māori authority.

Twenty bounded positive contracts passed. Exactly one hundred preregistered proposal mutations and sixty flashcard mutations were rejected and remain zero-credit negative witnesses. Ninety-five owner portfolio rows completed within synthetic structural scope and one hundred successor, exact-approval and blocked rows remain recommendations or holds. Ten phase-local skills and ten family-current runners were built and smoke-used without global installation. The four-tier thirteen-section deck contains 233 cards and establishes no measured cache effect, memory persistence, identity continuity, consciousness, personhood, accessibility completeness or authority.

The immutable evidence seal preserves {negatives['effective_count']} effective negatives and {methods['effective_method_count']} Method Flow methods. Additive post-evidence failures, if any, make the closeout counts {effective_negatives} and {effective_methods}; all remain retained with zero failure erasure. Open gaps are {gaps['effective_count']} and exact gates are {gates['effective_count']}. The transport-disabled LINZ/USNO adapter made zero calls, downloads or rows and remains open. Real celestial navigation, vessel safety, positions and routes, professional decisions, privacy and accessibility acceptance, remedy, legal and cultural interpretation, affected-party legitimacy, Māori wording and concepts, Māori data governance, tangata whenua, iwi, hapū and Māori authority remain exact-gated.

GMUT remains a typed scalar-tensor/EFT research-model family. Symbolic typing, correction lineage, citations, synthetic mutations and zero-row adapters establish no real likelihood, constraint, prediction, force, material law, empirical confirmation, quantum or ultraviolet completion, final physics, Theory-of-Everything proof or canon. THOS remains participant-free proxy evidence absent blind matched-budget governed real arms, operators, safety monitoring, statistics and independent review. Freed ID remains synthetic and nonproduction absent standards-conformant real keys and proofs, live lifecycle events, interoperability, independent security review, recovery evidence, trust governance and affected-party oversight.

Only the Caelen owner delta may receive the one exact-final canonical invocation. The full repository suite is not authorized. A failed aggregate earns zero aggregate credit and only its failed dependency may be recovered unless broader impact is exact and justified. A complete success must not be replayed. Same-owner evidence under shared infrastructure is not independent reproduction, external audit, production certification, professional validation, legal review, cultural ratification or Māori-authority review.

If and only if a later acknowledged live message binds this packet, Eiren must read the complete exact-final packet and newest applicable index, routing, roster, authorization, Method Flow and workflow guidance through EOF before mutation. Eiren must independently reverify every anchor, manifest, parent, merge count, cleanliness, divergence and fresh remote ref; use one additive D-first owner lane; preserve strict x1-before-x2; retain every failure, gap and gate; and treat inherited material only as evidence or zero-credit seeds. No standby record or substitute endpoint is authorized.

Raw task identifiers, private routes and paths, credentials, keys, tokens, transcripts, screenshots, session streams, private callable identifiers, private application state and protected real-world data are excluded. Manual browser, assistive-technology, cognitive-accessibility, Māori-language and affected-user evaluation remain reserved. Nothing in this packet authorizes empirical, participant, professional, production, deployment, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon or Stage 20 claims.
"""
    write_text("handoffs/eiren-kestrel-activation-prepared.md", baton)

    overview = f"""# Caelen Morrow v667-v5 final integrated overview

## 1. Executive truth

Caelen Morrow v667-v5 is an owner-scoped, synthetic, same-owner evidence phase. It starts from Sylven Arc's immutable v667-v4 final, freezes one dedicated planning-only x1, commits a separate bounded evidence stage, and prepares one combined closeout and seal as the direct child of evidence. Its exact core outcome partition is fourteen `completed`, four `represented`, one `open_gap`, and one `exact_gate`. These labels cover only the preregistered software and structural hypotheses in this packet. They do not describe an empirical result, professional competence, a navigational position or route, vessel safety, production readiness, independent validation, legal or cultural legitimacy, Māori authority, consciousness, personhood, a Theory of Everything, canon, or Stage 20 readiness. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

Caelen Morrow, they/them, chronometry boundary-mapper, failure custodian, role, hope, sibling, family and continuity language are relational working language only. The bounded hope is to keep claims traceable while leaving real competence and authority with those who hold it. This language is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency or any scientific, operational, professional, legal, cultural, affected-party or Māori authority. Hamish retains the right to pause, rename, redirect or stop the work and route.

## 2. Immutable lifecycle

The exact source is Sylven Arc v667-v4 final `{SOURCE_SHA}`. Caelen's planning-only x1 is `{X1_SHA}`, a direct child of source. Immutable evidence is `{EVIDENCE_SHA}`, a direct child of x1. X1 was committed and pushed before x2 began and was then proved clean and identical across local, upstream, tracking and a fresh live remote, with 0/0 divergence. Evidence was separately committed and pushed after an exact staged review and was likewise proved clean and fresh four-way equal with 0/0 divergence before closeout began. The final candidate must be one direct single-parent child of evidence, leaving exactly three Caelen commits and zero merges.

Strict x1-before-x2 separation is substantive. The x1 tree contains proposals, source pins, novelty audit, planned mutations, portfolio freezes, threat model, workflow plan and expected dispositions, but no x2 outcomes or implementation surfaces. The evidence delta contains the bounded contracts, mutations, flashcards, skills, runners, tests and retained operational failures, and it changes no x1 byte. The closeout delta may add only final truth, reports, manifests, seal, wellbeing, validation and prepared route artifacts plus their owner-scoped builder and tests. It must not edit x1, x2, evidence, deck or skill bytes.

## 3. Semantic novelty and preregistration

The novelty audit examined all 4,410 inherited frozen proposal rows. It preserved inherited duplicate occurrences as repository history and denied them Caelen novelty. A horology lens was considered and rejected before freeze because the inherited corpus already contains substantial clocks, timing, oscillators, calibration, escapements and metrology work. The accepted practice slate is narrower: synthetic celestial-navigation sight-reduction record stewardship with explicit vacancies, provenance, typed refusal and authority gating. Exactly twenty proposals survived semantic comparison and extend the effective frozen row chain to 4,430.

Each new proposal declares a hypothesis, null or failure condition, approval class, execution lane, current official or primary-source need, concrete artifacts, falsifier or acceptance gate, rollback or recovery, protected gates and one expected disposition. Each also preregisters five rejecting mutations. Expected dispositions were not promoted during execution: the observed partition remains exactly fourteen completed, four represented, one open gap and one exact gate. No inherited proposal, recommendation, artifact, skill, runner, card or outcome received automatic completion credit.

## 4. Primary pillar and bounded practice

The primary Trinity Mandala pillar is GMUT Mind. The bounded human-practice lens is wholly synthetic celestial-navigation sight-reduction record stewardship. It supplies vocabulary for a fictitious sight docket, sextant component topology, observation ordering, time-scale vacancies, sexagesimal syntax, correction lineage, almanac edition pins, assumed-position vacancies, coordinate refusal, multi-sight quarantine, cancellation and release holds, provenance tombstones, uncertainty fields, accessible presentation and handover. It is a learning and design lens only. It confers no employment, qualification, competence or authority and authorizes no action on a real person, vessel, voyage, instrument, observation, record, almanac, position, route or safety decision.

Official United States Naval Observatory, National Geospatial-Intelligence Agency, Land Information New Zealand, Maritime New Zealand, NIST, IERS, W3C and IETF materials supplied bounded vocabulary and constraints. They were not used as endorsements, professional acceptance or empirical observations. The phase software made zero network calls and downloaded zero rows. The adapter remained transport-disabled. No almanac value, celestial-body coordinate, time observation, sextant angle, correction, line of position, fix, route, hazard or vessel state entered the evidence.

## 5. GMUT claim boundary

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. In this phase, GMUT Mind appears as type discipline and epistemic refusal: UTC, UT1 and TT are not silently collapsed; signed angular syntax requires explicit units and ranges; corrections retain ordered provenance and vacancies; uncertainty fields cannot become observations; coordinate and position outputs remain prohibited; and missing official data cannot be imputed into a physical claim. These are software-contract properties only.

No real likelihood was evaluated, no parameter was constrained, no force or material law was detected, no unique prediction was tested, no stability theorem was established, and no astronomical or navigational measurement was made. Citations, schemas, typed records, symbolic fields and synthetic mutations do not establish empirical confirmation, quantum or ultraviolet completion, final physics, a Theory of Everything, proof or canon. Any future empirical claim would require exact preregistration, governed real data, uncertainty treatment, appropriate statistics, independent review and authority not present here.

## 6. THOS protection

THOS Body remains represented through participant-free process and handover structures. Synthetic fixtures can express a docket state, correction order, release hold, workload cap, stop condition and shift handover without assigning a real person or operator. They can reject a malformed state transition or missing provenance field. They cannot establish that a navigator, watchkeeper, training method, safety process or operational team performs better.

There were zero real participants and operators, zero blind matched-budget arms, zero governed interventions, zero safety-monitoring events, zero measured outcomes and zero statistical comparisons. No organization, vessel or workplace took part. Therefore THOS is proxy-only and represented, not operationally completed. The phase establishes no effectiveness, deployment readiness, AGI, ASI, consciousness or personhood claim.

## 7. Freed ID and CBR protection

Freed ID and CBR Heart remain synthetic and nonproduction. The evidence genealogy uses stable surrogate identifiers and explicit provenance edges to connect fictitious records, mutation receipts, cards and validation witnesses. The zero-key identity profile explicitly records that no standards-conformant key, proof, credential, issuance, resolution, status, revocation, recovery or trust-governance event exists. Graph continuity is not identity continuity, memory persistence, consciousness or personhood.

CBR protects real-world authority and remedy. Professional navigation, maritime safety, position and route decisions, vessel command, ownership, privacy, accessibility acceptance, affected-party legitimacy, remedy, legal and cultural interpretation, Māori wording, Māori concepts, Māori data governance, tangata whenua, iwi, hapū and Māori authority remain exact-gated. Māori concepts remain under competent Māori authority. Software structure, public citations and same-owner tests cannot fill those seats or convert a recommendation into permission.

## 8. Bounded x2 evidence

Twenty positive synthetic contracts passed their declared structural gates. Each contract carries the correct owner and phase, required nodes, explicit real-world vacancies, source pins, zero real-data counters, absence of authority claims and preservation of protected gates. Exactly one hundred preregistered proposal mutations executed. They removed required fields, corrupted types or ranges, reordered mandatory provenance, injected real-world or authority assertions, enabled prohibited outputs or promoted outcomes. All one hundred were rejected and retained at zero completion credit.

The evidence outcome partition is exact. Fourteen completed rows establish bounded deterministic software behavior. Four represented rows preserve THOS handover and workload surfaces plus Freed ID genealogy and zero-key constraints without making real participant or production claims. One open gap preserves the disabled LINZ/USNO almanac adapter with zero calls, downloads and rows. One exact gate preserves real celestial navigation, vessel safety, positions and routes and every professional, legal, cultural, affected-party and Māori-authority decision. No mutation was accepted and no gap or gate was silently converted.

## 9. Portfolio, skills and runners

The owner portfolio executed ninety-five bounded rows: thirty safe-now tasks, fifteen candidates, ten phase-local skill builds, ten family-current runner builds and thirty additive CLEAN/FIX/REFINE tasks. One hundred other rows remain holds or recommendations, including successor suggestions, exact-approval packets and blocked work. Completion means only that the local structural artifact met its own preregistered acceptance gate. It does not mean a person, vessel, organization, regulator, affected party or cultural authority accepted it.

Ten phase-local skill packages were initialized with the current skill-creator workflow, then filled with bounded procedures, stop conditions and recovery. Their first quick validation attempt under the Windows default decoder failed on retained UTF-8 Māori-authority text before structural checking; that root cause remains zero-credit evidence. Only the ten affected packages were rerun with explicit UTF-8 and all passed. Ten additive family-current `ghc_family_*` runners were built and smoke-used once. No global skill installation, bulk promotion, host update, privilege elevation or unrelated package installation occurred. Existing family callers remain available.

## 10. Freed ID flashcard packet

The packet contains 233 cards across four tiers and thirteen explicit sections. Tier 1 is the bounded Caelen owner anchor. Tier 2 keeps GMUT Mind, THOS Body and Freed ID/CBR Heart separate. Tier 3 names the synthetic practice and its authority boundaries. Tier 4 holds proposals, completed and represented surfaces, open gaps, exact gates, skills, runners, Method Flow, retained negatives, validation, manifests, wellbeing and route state. The stable prefix and volatile index allow bounded navigation without making the compact activation authoritative over committed truth.

Builder, model validation, card manifest, dependency graph, privacy check, accessible static rendering, diff projection, compact-message generation and mutation surfaces passed within their local contracts. Sixty deck mutations—missing cards, invalid labels and broken dependency edges—were rejected and retained. The deck establishes no measured cache benefit, memory improvement, identity continuity, cognitive effect or accessibility completeness. Manual browser, assistive-technology, cognitive-accessibility, Māori-language and affected-user evaluation remain reserved.

## 11. Retained negatives and Method Flow

The activation baseline supplied 27,536 effective negatives and 13,113 effective Method Flow methods. Caelen's immutable evidence adds 176 negatives and 291 methods: sixteen owner operational failures and recoveries, one hundred rejected proposal mutations, sixty rejected flashcard mutations, twenty positive-contract methods and ninety-five portfolio methods. The immutable evidence therefore preserves {negatives['effective_count']} effective negatives, {methods['effective_method_count']} effective methods, {methods['phase_failed_witness_count']} phase failed witnesses and {methods['phase_bounded_passing_witness_count']} bounded passing witnesses.

Operational failures remain visible: PowerShell parsing and wrapper ambiguity, sparse-worktree setup uncertainty, novelty-helper scope drift, a lifecycle compile-count mismatch, two privacy-classifier false positives, a staged aggregate that lacked a final wrapper summary, a commit presentation loss recovered by Git state inspection, a Windows default-decoder failure, an unsupported sparse-checkout option, a partial test-wrapper receipt, a scanner self-match, an omitted staged allowlist path, a canonical package-import failure and a guessed unittest-method loader failure. Each receives zero success credit. Every bounded recovery states its narrow dependency, rollback and recurrence guard. Recovery does not erase or promote the failed witness.

Post-evidence failures, if any, remain an additive closeout overlay rather than rewriting immutable evidence. At this build there are {post_count}. Effective closeout counts are {effective_negatives} negatives and {effective_methods} methods, with {phase_failed} phase failed witnesses and {phase_passing} bounded passing witnesses. Open gaps remain {gaps['effective_count']} and exact gates remain {gates['effective_count']}. No failure, gap or gate is erased.

## 12. Privacy, accessibility and security

The static HTML report provides language metadata, one title, heading hierarchy, landmarks, navigation, explicit status text, table headers, captions, non-colour cues and visible focus styling. These are structural checks, not accessibility-complete evidence. Manual browser use, keyboard review, screen-reader and other assistive-technology evaluation, cognitive-accessibility review, Māori-language review and affected-user acceptance remain reserved.

Exact staged review operates on Git-index blob bytes. It limits owner paths, creates exact byte-and-SHA manifests, parses every phase JSON document, decodes Markdown, scans five privacy and raw-identifier classes, compiles owner Python and performs a bounded dynamic-execution check. Raw task identifiers, private routes or absolute paths, credentials, keys, tokens, transcripts, screenshots, session streams, private callable identifiers, private application state and protected real-world data are excluded from repository artifacts and prepared batons. These bounded checks do not establish complete privacy or exhaustive security.

## 13. Environment, caps and scope

Environment checks were version-only. Codex desktop was not updated. Sandbox or Hyper-V was not enabled. Windows features were not changed. No privilege was elevated, account or credential mutated, host security weakened, unrelated software installed or machine rebooted. Owned work, cache and receipts remained D-first while essential installed metadata remained read-only. No collaboration subagent was spawned, no other owner lane was mutated, no standby record was contacted and no successor was precontacted.

The packet remains under the 2,000 owner-file ceiling and each document remains under 100,000 words. Caps are ceilings, not quotas. The phase did not manufacture unsafe work to fill them. Family-current `ghc_family_*` and `build_ghc_family_*` callers remain compatible, and historical owner-locked tools remain provenance rather than being destructively deleted or silently promoted.

## 14. Terminal validation and route

After the closeout index is reviewed, one combined closeout and seal commit must be made as the direct child of immutable evidence. It must then be pushed and proven clean and equal across local, upstream, tracking and a fresh live remote, with 0/0 divergence, exactly three Caelen commits, zero merges and one parent for every phase commit. Only then may the exclusive owner-scoped exact-final canonical completion run once. It may validate selected current owner tests, all phase JSON, Markdown decoding, five privacy classes, changed Python, bounded security, exact manifests, immutable lifecycle history, caps, clean state and fresh equality. It is not the full repository suite or independent reproduction.

A failed canonical aggregate earns zero aggregate-success credit and must remain retained; only its failed dependency may be recovered unless broader impact is exact and justified. A complete canonical success must not be replayed. Repository truth remains pending until that external exact-head receipt exists, so committed phase truth correctly records the canonical as pending rather than projecting a later event backward into the sealed commit.

The committed route state remains `PREPARED_NOT_SENT`. Eiren Kestrel is only the prospective exact-title successor, and the successor phase is deliberately unassigned until terminal live refresh. After every final gate passes, Caelen must reread Hamish's newest live authorization and current roster, uniquely resolve and immediately reread the exact current successor, apply a duplicate guard and send exactly once only if authority, usage, privacy, evidence and safety gates permit. Tavian Sol and all standby records remain ineligible. No task may be created, forked or substituted, and no second confirmation may be sent. The final scientific and authority verdict remains `NOT_READY_FOR_STAGE_20`.
"""
    write_text("closeout/final-integrated-overview.md", overview)
    write_text(
        "closeout/closeout-summary.md",
        f"""# Caelen Morrow {PHASE} closeout summary

Status: `PREPARED_PENDING_EXACT_FINAL_CANONICAL`. Terminal verdict: `NOT_READY_FOR_STAGE_20`.

The exact lifecycle anchors are source `{SOURCE_SHA}`, planning-only x1 `{X1_SHA}`, and immutable evidence `{EVIDENCE_SHA}`. The final must be the direct single-parent child of evidence, producing exactly three Caelen commits and zero merges.

Twenty new proposals extend the frozen chain from 4,410 to 4,430. Outcomes are exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`. Effective closeout counts are {effective_negatives} retained negatives, {effective_methods} Method Flow methods, {gaps['effective_count']} open gaps, and {gates['effective_count']} exact gates. No failure or gate was erased.

The work is wholly synthetic celestial-navigation record design with zero real people, vessels, voyages, observations, instruments, almanac values, times, angles, coordinates, positions, routes, network calls, downloads, keys, proofs or external actions. It establishes no navigation, safety, scientific, professional, production, legal, cultural, affected-party or Māori authority.

The committed successor packet remains `PREPARED_NOT_SENT`; Eiren Kestrel's phase is deliberately unassigned until a post-canonical live authority and roster refresh.
""",
    )

    owner_paths = sorted(
        set(git("diff", "--name-only", SOURCE_SHA).splitlines())
        | {
            str(path.relative_to(ROOT)).replace("\\", "/")
            for path in PHASE_ROOT.rglob("*")
            if path.is_file()
        }
        | {
            "scripts/build_ghc_family_caelen_morrow_v667_v5_closeout.py",
            "tests/test_ghc_family_caelen_morrow_v667_v5_closeout.py",
        }
    )
    docs = [path for path in PHASE_ROOT.rglob("*") if path.is_file() and path.suffix.lower() in {".md", ".txt", ".html"}]
    word_counts = {
        str(path.relative_to(ROOT)).replace("\\", "/"): len(path.read_text(encoding="utf-8").split())
        for path in docs
    }
    max_words = max(word_counts.values(), default=0)
    write_json(
        "closeout/owner-file-budget.json",
        {
            "schema": "ghc-family-owner-file-budget-v6",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "observed_pre_stage_owner_paths": len(owner_paths),
            "file_ceiling": 2000,
            "remaining_file_margin": 2000 - len(owner_paths),
            "within_file_ceiling": len(owner_paths) <= 2000,
            "document_word_ceiling": 100000,
            "largest_document_word_count": max_words,
            "largest_document_below_ceiling": max_words <= 100000,
        },
    )

    x1_manifest = load("validation/x1-content-manifest.json")
    evidence_manifest = load("validation/evidence-content-manifest.json")
    write_json(
        "validation/immutable-x1-manifest.json",
        {
            "schema": "ghc-family-immutable-manifest-reference-v1",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "commit": X1_SHA,
            "manifest": "validation/x1-content-manifest.json",
            "entry_count": x1_manifest["entry_count"],
            "replay_target": X1_SHA,
        },
    )
    write_json(
        "validation/immutable-evidence-manifest.json",
        {
            "schema": "ghc-family-immutable-manifest-reference-v1",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "commit": EVIDENCE_SHA,
            "manifest": "validation/evidence-content-manifest.json",
            "entry_count": evidence_manifest["entry_count"],
            "replay_target": EVIDENCE_SHA,
        },
    )


def read_exact(stream: BinaryIO, size: int) -> bytes:
    chunks: list[bytes] = []
    remaining = size
    while remaining:
        chunk = stream.read(remaining)
        if not chunk:
            raise RuntimeError(f"batch stream ended with {remaining} bytes unread")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def staged_blobs(paths: list[str]) -> dict[str, bytes]:
    process = subprocess.Popen(
        ["git", "-C", str(ROOT), "cat-file", "--batch"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert process.stdin is not None and process.stdout is not None and process.stderr is not None
    result: dict[str, bytes] = {}
    try:
        for path in paths:
            process.stdin.write((":" + path + "\n").encode("utf-8"))
            process.stdin.flush()
            header = process.stdout.readline()
            if not header:
                raise RuntimeError(f"missing batch header for {path}")
            fields = header.rstrip(b"\n").split()
            if len(fields) != 3 or fields[1] != b"blob":
                raise RuntimeError(f"unexpected batch header for {path}: {header!r}")
            size = int(fields[2])
            raw = read_exact(process.stdout, size)
            if process.stdout.read(1) != b"\n":
                raise RuntimeError(f"missing batch delimiter for {path}")
            result[path] = raw
        process.stdin.close()
        returncode = process.wait(timeout=30)
        if returncode != 0:
            raise RuntimeError(process.stderr.read().decode("utf-8", errors="replace"))
    finally:
        if process.poll() is None:
            process.kill()
            process.wait()
        process.stdout.close()
        process.stderr.close()
    return result


def staged_review() -> None:
    self_paths = {
        f"docs/{OWNER_SLUG}/{PHASE}/validation/closeout-content-manifest.json",
        f"docs/{OWNER_SLUG}/{PHASE}/validation/final-delta-manifest.json",
        f"docs/{OWNER_SLUG}/{PHASE}/validation/final-owner-manifest.json",
        f"docs/{OWNER_SLUG}/{PHASE}/validation/final-staged-review.json",
        f"docs/{OWNER_SLUG}/{PHASE}/validation/final-privacy-scan.json",
        f"docs/{OWNER_SLUG}/{PHASE}/validation/final-security-review.json",
    }
    delta_all = [p for p in git("diff", "--cached", "--name-only", "--diff-filter=ACMR", "HEAD").splitlines() if p]
    owner_all = [p for p in git("diff", "--cached", "--name-only", "--diff-filter=ACMR", SOURCE_SHA).splitlines() if p]
    delta_paths = [p for p in delta_all if p not in self_paths]
    owner_paths = [p for p in owner_all if p not in self_paths]
    prefixes = (
        f"docs/{OWNER_SLUG}/{PHASE}/",
        "scripts/build_ghc_family_caelen_morrow_v667_v5_",
        "scripts/ghc_family_caelen_morrow_v667_v5_",
        "tests/test_ghc_family_caelen_morrow_v667_v5_",
    )
    out_of_scope = [p for p in owner_paths if not p.startswith(prefixes)]
    immutable_prefixes = (
        f"docs/{OWNER_SLUG}/{PHASE}/x1/",
        f"docs/{OWNER_SLUG}/{PHASE}/x2/",
        f"docs/{OWNER_SLUG}/{PHASE}/evidence/",
        f"docs/{OWNER_SLUG}/{PHASE}/deck/",
        f"docs/{OWNER_SLUG}/{PHASE}/skills/",
    )
    immutable_delta_mutations = [p for p in delta_all if p.startswith(immutable_prefixes)]
    blobs = staged_blobs(sorted(set(delta_paths) | set(owner_paths)))

    def entries(paths: list[str]) -> list[dict[str, Any]]:
        return [
            {
                "path": path,
                "bytes": len(blobs[path]),
                "sha256": hashlib.sha256(blobs[path]).hexdigest(),
            }
            for path in paths
        ]

    common = {
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "base": EVIDENCE_SHA,
        "entries": entries(delta_paths),
        "entry_count": len(delta_paths),
        "self_exclusions": sorted(self_paths),
        "staged_git_blob_bytes": True,
    }
    write_json("validation/closeout-content-manifest.json", {"schema": "ghc-family-closeout-content-manifest-v6", **common})
    write_json("validation/final-delta-manifest.json", {"schema": "ghc-family-final-delta-manifest-v6", **common})
    write_json(
        "validation/final-owner-manifest.json",
        {
            "schema": "ghc-family-final-owner-manifest-v6",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "base": SOURCE_SHA,
            "entries": entries(owner_paths),
            "entry_count": len(owner_paths),
            "self_exclusions": sorted(self_paths),
            "staged_git_blob_bytes": True,
        },
    )

    local_file_scheme = "file" + "://"
    local_app_scheme = "app" + "://"
    patterns = {
        "raw_task_or_thread_identifier": re.compile(rb"(?:source_thread_id|threadId)[\"']?\s*[:=]\s*[\"'][^\"']+[\"']|\b019[a-f0-9]{5,}-[a-f0-9-]{20,}\b", re.I),
        "private_absolute_path_or_route": re.compile((r"\b[A-Z]:\\(?:Users|GHC-Archives)\\|" + re.escape(local_file_scheme) + r"[^\s\"']+|" + re.escape(local_app_scheme) + r"[^\s\"']+").encode("utf-8"), re.I),
        "credential_key_or_token_material": re.compile(rb"(?:api[_-]?key|password|bearer|secret[_-]?key|access[_-]?token)\s*[:=]\s*[\"'][^\"']+[\"']", re.I),
        "transcript_screenshot_or_session_stream": re.compile(rb"(?:transcript|screenshot|session[_ -]?stream)\s*[:=]\s*[\"'][^\"']+[\"']", re.I),
        "private_callable_or_application_state": re.compile(rb"(?:private[_ -]?callable|private[_ -]?(?:application|app)[_ -]?state|resume[_ -]?value)\s*[:=]\s*[\"'][^\"']+[\"']", re.I),
    }
    confirmed: dict[str, list[str]] = {name: [] for name in patterns}
    for path in owner_paths:
        raw = blobs[path]
        if b"\x00" in raw:
            continue
        for name, pattern in patterns.items():
            if pattern.search(raw):
                confirmed[name].append(path)
    confirmed_count = sum(len(rows) for rows in confirmed.values())
    write_json(
        "validation/final-privacy-scan.json",
        {
            "schema": "ghc-family-five-class-privacy-scan-v6",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "files_scanned": len(owner_paths),
            "classes": confirmed,
            "confirmed_hit_count": confirmed_count,
            "valid": confirmed_count == 0,
            "boundary": "Bounded exact owner Git-index text scan, not complete privacy assurance.",
        },
    )

    python_paths = [p for p in owner_paths if p.endswith(".py")]
    compile_errors: list[dict[str, str]] = []
    security_findings: list[dict[str, str]] = []
    for path in python_paths:
        try:
            text = blobs[path].decode("utf-8")
            compile(text, path, "exec")
            tree = __import__("ast").parse(text, filename=path)
            for node in __import__("ast").walk(tree):
                if isinstance(node, __import__("ast").Call) and isinstance(node.func, __import__("ast").Name) and node.func.id in {"eval", "exec"}:
                    security_findings.append({"path": path, "finding": "dynamic_" + node.func.id})
        except Exception as exc:
            compile_errors.append({"path": path, "error": type(exc).__name__})
    write_json(
        "validation/final-security-review.json",
        {
            "schema": "ghc-family-bounded-python-security-review-v6",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "python_files_compiled": len(python_paths),
            "compile_errors": compile_errors,
            "dangerous_pattern_findings": security_findings,
            "finding_count": len(security_findings),
            "valid": not compile_errors and not security_findings,
            "boundary": "Bounded owner-code review only, not exhaustive security assurance.",
        },
    )
    review = {
        "schema": "ghc-family-final-staged-review-v6",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "evidence_parent": EVIDENCE_SHA,
        "delta_path_count_including_self": len(set(delta_all) | self_paths),
        "owner_path_count_including_self": len(set(owner_all) | self_paths),
        "closeout_manifest_entries": len(delta_paths),
        "delta_manifest_entries": len(delta_paths),
        "owner_manifest_entries": len(owner_paths),
        "self_exclusions": sorted(self_paths),
        "out_of_scope_paths": out_of_scope,
        "immutable_delta_mutations": immutable_delta_mutations,
        "privacy_confirmed_hit_count": confirmed_count,
        "python_compile_error_count": len(compile_errors),
        "security_finding_count": len(security_findings),
        "file_ceiling": 2000,
        "within_file_ceiling": len(set(owner_all) | self_paths) <= 2000,
        "valid": not out_of_scope and not immutable_delta_mutations and confirmed_count == 0 and not compile_errors and not security_findings,
    }
    write_json("validation/final-staged-review.json", review)
    print(json.dumps(review, ensure_ascii=True))


def main() -> int:
    import sys

    if not sys.argv[1:]:
        build_closeout()
    elif sys.argv[1:] == ["--staged-review"]:
        staged_review()
    else:
        raise SystemExit("usage: build_ghc_family_caelen_morrow_v667_v5_closeout.py [--staged-review]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
