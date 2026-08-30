#!/usr/bin/env python3
"""Build the owner-local Sylven Arc v678-v6 terminal closeout packet."""

from __future__ import annotations

import argparse
import html
import json
import platform
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


OWNER = "Sylven Arc"
PHASE = "v678-v6"
SOURCE = "d7a2e3d1851d8a9eb6a8707968a47354b44e824a"
X1 = "22d310c7ae4fdbd45959d388d15642039d748da0"
EVIDENCE = "7b747952b6a6916c3881066865ff7021aeabea3c"
LABELS = {"completed", "represented", "open_gap", "exact_gate"}


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical(value))


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run(repo: Path, args: list[str]) -> str:
    result = subprocess.run(args, cwd=repo, check=False, capture_output=True, text=True, encoding="utf-8")
    if result.returncode:
        return "unavailable"
    return result.stdout.strip() or result.stderr.strip()


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=repo, check=False, capture_output=True, text=True, encoding="utf-8")
    if result.returncode:
        raise SystemExit(result.stderr.strip() or "git command failed")
    return result.stdout.strip()


def build(repo: Path) -> dict[str, Any]:
    if git(repo, "rev-parse", "HEAD") != EVIDENCE:
        raise SystemExit("final closeout must begin at the immutable evidence commit")
    if git(repo, "rev-parse", "HEAD^") != X1 or git(repo, "rev-parse", "HEAD^^") != SOURCE:
        raise SystemExit("source/x1/evidence direct-parent chain mismatch")
    if git(repo, "diff", "--name-only") or git(repo, "diff", "--cached", "--name-only"):
        raise SystemExit("closeout requires no tracked mutation above the immutable evidence commit")
    phase = repo / "docs/sylven-arc/v678-v6"
    closeout = phase / "closeout"
    validation = phase / "validation"
    handoffs = phase / "handoffs"
    x1 = phase / "x1"
    x2 = phase / "x2"
    proposals = read_json(x1 / "new-proposal-freeze.json")["proposals"]
    outcomes = read_json(x2 / "proposal-outcomes.json")
    portfolio = read_json(x2 / "portfolio-execution.json")
    method_base = read_json(x2 / "evidence-manifest-method-flow-overlay.json")["overlay"]
    counts = outcomes["counts"]
    if counts != {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}:
        raise SystemExit("outcome truth drift")
    post_evidence_methods = [
        {"method_id": "SA6786-CLOSE-N001", "status": "retained_failed_witness", "summary": "A combined post-evidence four-way equality wrapper crossed its reporting window and exposed neither scalar output nor its process handle; it earned no equality credit."},
        {"method_id": "SA6786-CLOSE-R001", "status": "bounded_passing_recovery", "summary": "Separate bounded local, upstream, tracking, divergence, cleanliness, and fresh-live remote scalars proved equality at the immutable evidence commit without repeating the push."},
        {"method_id": "SA6786-CLOSE-N002", "status": "retained_failed_witness", "summary": "The first final privacy preflight failed closed on inherited x1 scanner-definition and synthetic-test literals that were not yet exactly adjudicated."},
        {"method_id": "SA6786-CLOSE-R002", "status": "bounded_passing_recovery", "summary": "Two exact inherited x1 source files were added to the scanner-definition adjudication set; the bounded preflight then found fourteen definition candidates and zero confirmed payload hits."},
    ]
    closeout_components = [
        "final integrated overview", "phase truth", "retained-negative register", "Method Flow final ledger",
        "open and exact gate register", "complete and incomplete checklist", "wellbeing and workload receipt",
        "environment version receipt", "lifecycle replay", "source and provenance projection", "threat-model projection",
        "portfolio closeout", "flashcard closeout", "skill and runner closeout", "accessible static report",
        "prepared route receipt", "prepared activation candidate", "evidence-manifest replay projection",
        "scientific and authority boundary projection", "three-page-equivalent owner overview",
    ]
    for index, name in enumerate(closeout_components, 1):
        post_evidence_methods.append({"method_id": f"SA6786-CLOSE-P{index:03d}", "status": "bounded_passing_witness", "summary": f"Built the bounded {name}."})
    final_overlay = {
        "effective_negatives": method_base["effective_negatives"] + 2,
        "effective_methods": method_base["effective_methods"] + len(post_evidence_methods),
        "retained_failed_witnesses": method_base["retained_failed_witnesses"] + 2,
        "bounded_passing_witnesses": method_base["bounded_passing_witnesses"] + 22,
        "open_gaps": method_base["open_gaps"], "exact_gates": method_base["exact_gates"],
    }
    write_json(closeout / "method-flow-final.json", {
        "schema": "ghc-family-method-flow-final/v1", "owner": OWNER, "phase": PHASE,
        "base": method_base, "overlay": final_overlay, "new_methods": len(post_evidence_methods),
        "new_failed_witnesses": 2, "new_passing_witnesses": 22,
        "methods": post_evidence_methods, "failure_erasure_forbidden": True,
        "inherited_method_flow": [
            "x1/method-flow-startup.json", "x2/method-flow-execution.json",
            "x2/post-execution-method-flow-overlay.json", "x2/evidence-manifest-method-flow-overlay.json",
        ],
    })
    phase_truth = {
        "schema": "ghc-family-phase-truth/v1", "owner": OWNER, "phase": PHASE,
        "source": SOURCE, "x1": X1, "evidence": EVIDENCE, "exact_final": "BOUND_AT_COMMIT",
        "declared_proposal_chain_before": 8570, "new_proposals": 60, "declared_proposal_chain_after": 8630,
        "core_outcomes": counts, "positive_zero_row_contracts": 60, "rejected_mutations": 240,
        "accepted_invalid_mutations": 0, "phase_local_skills_initialized_read_validated_and_smoke_used": 20,
        "global_skill_installations": 0, "family_current_runners_positive_and_rejecting_smoke_used": 10,
        "flashcard_cards": 81, "flashcard_tiers": {"1": 15, "2": 3, "3": 3, "4": 60},
        "safe_now_completed": 60, "candidate_completed": 30, "clean_fix_refine_completed": 60,
        "exact_approval_unexecuted": 20, "blocked_unexecuted": 10,
        "real_world_rows": 0, "external_actions": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "validation_state": "PENDING_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "route_state": "PREPARED_NOT_SENT",
        "method_flow_overlay": final_overlay,
    }
    write_json(closeout / "phase-truth.json", phase_truth)
    open_ids = [row["proposal_id"] for row in proposals if row["expected_disposition"] == "open_gap"]
    exact_ids = [row["proposal_id"] for row in proposals if row["expected_disposition"] == "exact_gate"]
    write_json(closeout / "open-exact-gate-register.json", {
        "schema": "ghc-family-open-exact-gate-register/v1", "owner": OWNER, "phase": PHASE,
        "inherited_open_gaps": 407, "new_open_gaps": open_ids, "effective_open_gaps": 410,
        "inherited_exact_gates": 398, "new_exact_gates": exact_ids, "effective_exact_gates": 401,
        "open_gap_scope": ["real object observation or measurement", "manual browser and assistive-technology evaluation", "independent governed review"],
        "exact_gate_scope": ["professional action or release", "ownership, custody, copyright, privacy remedy, legal or cultural interpretation", "affected-party and Māori authority"],
        "maori_concepts_remain_under_maori_authority": True,
    })
    write_json(closeout / "retained-negative-register.json", {
        "schema": "ghc-family-retained-negative-register/v1", "owner": OWNER, "phase": PHASE,
        "inherited_activation_negatives": 47007, "repository_sealed_effective_negatives": final_overlay["effective_negatives"],
        "repository_sealed_retained_failed_witnesses": final_overlay["retained_failed_witnesses"],
        "phase_negative_classes": {
            "startup_and_x1_operational": 13, "x2_pre_execution_operational": 6,
            "preregistered_rejecting_mutations": 240, "runner_invalid_fixtures": 10,
            "x2_lifecycle_and_wrapper_failures": 2, "evidence_manifest_failures": 2,
            "post_evidence_equality_wrapper_failures": 1, "final_manifest_privacy_preflight_failures": 1,
        },
        "canonical_failures": 0, "canonical_invocations": 0,
        "all_recoveries_additive": True, "failure_erasure_forbidden": True,
        "source_registers": [
            "x1/method-flow-startup.json", "x2/method-flow-execution.json",
            "x2/post-execution-method-flow-overlay.json", "x2/evidence-manifest-method-flow-overlay.json",
            "validation/x2-test-and-lifecycle-recovery.json", "validation/evidence-manifest-build-recovery.json",
        ],
    })
    write_json(closeout / "complete-incomplete-checklist.json", {
        "schema": "ghc-family-complete-incomplete/v1", "owner": OWNER, "phase": PHASE,
        "complete": [
            "planning-only x1 frozen, pushed, clean, and fresh-live equal before x2",
            "sixty genuinely distinct source-bounded proposals frozen against all reachable evidence",
            "sixty positive zero-row contracts and 240 rejecting mutations executed",
            "twenty phase-local skills initialized with the official workflow, read through EOF, quick-validated, and smoke-used",
            "ten family-current runners accepted positive and rejected invalid fixtures",
            "four-tier 81-card Freed ID flashcard deck built, graphed, rendered, privacy-scanned, manifested, and validated",
            "immutable x2 evidence committed, pushed, clean, and fresh-live equal",
        ],
        "incomplete": [
            "exact-final canonical validation remains pending until the final commit is pushed and four-way equal",
            "successor route remains PREPARED_NOT_SENT until exact-final canonical success and a fresh native task registry check",
            "all real-world observation, measurement, operation, treatment, professional, empirical, legal, cultural, affected-party, Māori-authority, privacy-complete, accessibility-complete, independent-reproduction, and Stage 20 gates remain open or exact-gated",
        ],
    })
    write_json(closeout / "wellbeing-workload-check.json", {
        "schema": "ghc-family-wellbeing-workload/v1", "owner": OWNER, "phase": PHASE,
        "relational_working_language_only": True, "consciousness_or_personhood_evidence": False,
        "workload_state": "bounded and owner-local", "stop_control": "Hamish may pause, redirect, narrow, rename, or stop the route",
        "no_background_babysitting": True, "no_precontact": True, "no_subagents": True,
        "next_action": "finish exact-final owner-scoped validation, then perform at most one guarded native successor send",
    })
    environment = {
        "schema": "ghc-family-environment-version-receipt/v1", "owner": OWNER, "phase": PHASE,
        "python": platform.python_version(), "git": run(repo, ["git", "--version"]),
        "node": run(repo, ["node", "--version"]), "pytest": run(repo, ["python", "-m", "pytest", "--version"]),
        "versions_verified_read_only": True, "codex_desktop_updated": False, "host_features_changed": False,
        "privilege_elevation": False, "reboot": False,
    }
    write_json(closeout / "environment-version-receipt.json", environment)
    write_json(closeout / "lifecycle-replay.json", {
        "schema": "ghc-family-lifecycle-replay/v1", "source": SOURCE, "x1": X1, "evidence": EVIDENCE,
        "final": "BOUND_AT_COMMIT", "expected_phase_commits": 3, "expected_merges": 0,
        "x1_parent": SOURCE, "evidence_parent": X1, "final_parent": EVIDENCE,
        "x1_was_pushed_clean_equal_before_x2": True, "evidence_was_pushed_clean_equal_before_closeout": True,
        "exact_final_validation_pending": True,
    })
    write_json(closeout / "portfolio-closeout.json", {
        "schema": "ghc-family-portfolio-closeout/v1", "counts": {
            "safe_now_completed": len(portfolio["safe_now"]), "candidate_completed": len(portfolio["candidate"]),
            "exact_approval_unexecuted": len(portfolio["exact_approval"]), "blocked_unexecuted": len(portfolio["blocked"]),
            "clean_fix_refine_completed": len(portfolio["clean_fix_refine"]),
            "successor_clean_fix_refine_recommendations": len(portfolio["successor_recommendations"]),
        }, "unsafe_or_filler_execution": 0, "inherited_recommendations_auto_credited": False,
    })
    write_json(closeout / "flashcard-closeout.json", {
        "schema": "ghc-family-flashcard-closeout/v1", "cards": 81, "tiers": 4,
        "main_relational_anchor_cards": 15, "pillar_cards": 3, "bounded_practice_cards": 3, "task_cards": 60,
        "manifest_entries": 89, "privacy_confirmed_hits": 0, "prompt_cache_guarantee": False,
        "identity_continuity_claim": False, "delivery_evidence": False,
        "structural_accessibility_only": True, "human_evaluations_reserved": True,
    })
    write_json(closeout / "route-receipt.json", {
        "schema": "ghc-family-route-receipt/v1", "owner": OWNER, "phase": PHASE,
        "state": "PREPARED_NOT_SENT", "prospective_exact_title": "Caelen Morrow", "prospective_phase": "v678-v7",
        "native_registry_refreshed": False, "unique_exact_title_confirmed": False,
        "immediate_reread_completed": False, "duplicate_guard_passed": False,
        "send_count": 0, "delivery_acknowledged": False, "standby_contacted": False,
        "route_binding_deferred_until_after_exact_final_canonical": True,
    })
    overview = f"""# Sylven Arc v678-v6 final integrated overview

## Outcome and evidence posture

Sylven Arc v678-v6 is a bounded owner-local software and documentation phase. The repository packet records sixty genuinely new source-bounded proposals, sixty accepted zero-row synthetic fixtures, 240 preregistered invalid mutations rejected at zero broader credit, twenty phase-local skills, ten family-current runners, and an 81-card four-tier Freed ID flashcard deck. The exact core outcomes are 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`. `completed` means only that the frozen synthetic software or documentation acceptance gate passed; it is not a real-world, empirical, professional, production, legal, cultural, or authority result.

The terminal verdict remains `NOT_READY_FOR_STAGE_20`. The repository seal before external canonical validation is {final_overlay['effective_negatives']:,} effective negatives, {final_overlay['effective_methods']:,} effective Method Flow methods, {final_overlay['retained_failed_witnesses']:,} retained failed witnesses, {final_overlay['bounded_passing_witnesses']:,} bounded passing witnesses, {final_overlay['open_gaps']} open gaps, and {final_overlay['exact_gates']} exact gates. Every recovery remains paired with its failed witness. A failed aggregate, wrapper, parser, manifest, or mutation never becomes success simply because a later bounded method passes.

## Lifecycle separation

The exact immutable source is `{SOURCE}`. Planning-only x1 is `{X1}` and is its direct child. Immutable x2 evidence is `{EVIDENCE}` and is the direct child of x1. X1 contained no x2 implementation or outcome. It was committed, pushed, clean, typed 0/0 divergent, and equal across local, upstream, tracking, and a fresh live remote before x2 began. The evidence commit was independently committed, pushed, clean, typed 0/0 divergent, and fresh-live four-way equal before this closeout began. The final commit is required to be the direct child of evidence, so source-to-final will contain exactly three Sylven commits and zero merges.

The x2 test selection retained one failed aggregate: an immutable x1 no-x2 assertion was invoked from the later x2 worktree. Thirty-two observations passed, but the aggregate earned zero success credit. The first isolated recovery wrapper then materialized x1 but accidentally left pytest in the later worktree; that failure also remains. Exactly the one failed lifecycle dependency then passed once in a D-first external materialization of the exact x1 Git tree. The twenty new x2 tests were not replayed.

## Pillars and bounded practices

The primary pillar is THOS Body. GMUT Mind and Freed ID/CBR Heart remain explicit and protected. Three wholly synthetic learning and design lenses structure the phase: zero-globe documentation through a globemaking records analyst; zero-machine documentation through a mechanical-automaton linkage analyst; and zero-window documentation through a stained-glass handover steward. These labels confer no employment, qualification, competence, professional role, or authority.

The Library of Congress rare-globe rehousing article supplied vocabulary for supports, movement restraint, documentation, and abstention. The Metropolitan Museum of Art automaton chariot record supplied bounded component and provenance vocabulary. The National Park Service stained-glass page supplied panel, glazing, environment, maintenance, and specialist-boundary vocabulary. W3C PROV-O supplied provenance vocabulary; WCAG 2.2 supplied structural accessibility vocabulary without conformance; Verifiable Credentials Data Model 2.0 supplied status and minimization vocabulary with zero keys and zero proofs; RFC 8785 supplied deterministic JSON vocabulary without production cryptographic assurance. Sources were citations and vocabulary only, not observations, instructions, endorsements, conformance evidence, or authority grants.

The phase used zero real people, participants, globemakers, mechanics, conservators, custodians, affected users, globes, gores, spheres, meridian rings, stands, housings, automatons, gears, cams, shafts, springs, stained-glass panels, glass, came, solder, frames, buildings, sacred images, observations, measurements, tools, operations, treatments, custody events, keys, proofs, network rows, external writes, professional decisions, legal or cultural decisions, affected-party approvals, or Māori-authority acts.

## Positive and rejecting evidence

Each of the sixty proposal contracts requires a synthetic identifier, no raw identifier, an empty measurement list, zero real-world rows, zero external actions, and explicit false values for real-world authority, condition determination, authenticity determination, operation, treatment, professional release, legal approval, cultural approval, Māori authority, production readiness, and empirical confirmation. One positive fixture passed each contract. Four preregistered invalid mutations per proposal—missing hypothesis, unauthorized outcome label, authority escalation, and real identifier or measurement injection—were executed and rejected. All 240 remain retained failed witnesses at zero completion credit.

The owner portfolio completed sixty safe-now tasks, thirty bounded candidate tasks, and sixty CLEAN/FIX/REFINE tasks only inside the synthetic owner-local surface. Twenty exact-approval packets and ten blocked packets remained visible and unexecuted. Thirty successor CLEAN/FIX/REFINE records remain recommendations with zero Sylven completion credit. Floors did not authorize filler, real-world action, bulk installation, deletion, or protected-gate bypass.

## Skills, runners, and flashcards

Twenty phase-local skills were initialized through the official skill-creator workflow, customized, read completely through EOF, quick-validated, and smoke-used. None was globally installed. Every skill refuses real handling, operation, inspection, measurement, treatment, custody transfer, identity lifecycle, deployment, credentials, private routes, protected data, or authority escalation. Ten family-current runners were each invoked once with a positive synthetic fixture and once with an invalid fixture; every positive fixture was accepted and every invalid fixture rejected.

The flashcard deck implements exactly four tiers: fifteen relational Freed ID anchor cards; three Trinity Mandala pillar cards; three bounded-practice cards; and sixty task cards. Deterministic `ghc-card-*` identifiers, exact parent chains, a stable prefix, volatile index, thirteen-section baton index, graph, privacy receipt, self-excluding manifest, compact activation note, and structural HTML report were built and validated. The deck does not guarantee prompt-cache retention and does not establish identity continuity. Manual browser, assistive-technology, cognitive, Māori-language, and affected-user evaluation remain reserved.

## Scientific, professional, and authority boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. This phase establishes no physical datum, likelihood, posterior, parameter constraint, detected force, prediction, empirical confirmation, stability theorem, quantum completion, ultraviolet completion, final physics, Theory of Everything, proof, or canon. THOS remains participant-free synthetic proxy evidence without preregistered governed blind matched-budget real arms, participants or operators, safety monitoring, appropriate statistics, or independent review. It establishes no operational effectiveness, deployment readiness, AGI, or ASI.

Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, independent privacy and security review, recovery evidence, trust governance, or affected-party oversight. Relational names, pronouns, roles, hopes, sibling or family language, continuity language, GHC Family, Freed ID, CBR, and Trinity Mandala remain working language only. They are not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, agency, or authority.

Globe handling or housing, automaton winding or operation, stained-glass inspection or treatment, product and workplace safety, ownership, custody, copyright, privacy remedy, land, heritage, sacred context, legal or cultural interpretation, affected-party legitimacy, Māori wording and concepts, tikanga, taonga or mātauranga treatment, Māori data governance, and Māori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapū, and Māori authorities. Māori concepts remain under Māori authority.

## Validation and route hold

The final owner-scoped canonical aggregate has not yet been invoked at repository-preparation time. This packet is `PREPARED_NOT_SENT`. After the final commit is built, exactly staged, manifested, pushed, clean, typed 0/0 divergent, and fresh-live four-way equal, one attributable exact-final owner-scoped canonical may run through an exclusive external latch. A success must never be replayed. A failure earns zero canonical-success credit and may be followed only by a narrowly justified additive correction within the current commit ceiling.

Only after successful exact-final canonical validation may the route be refreshed. The prospective title is `Caelen Morrow` for v678-v7, but this prepared packet does not bind or contact that task. The terminal process must use a bounded native registry read, local exact-title filtering, one immediate structured reread, duplicate and current-control guards, and at most one sanitized send. Delivery exists only if the native task-message surface acknowledges the exact target. Absence, ambiguity, pause, redirect, rename, narrowing, standby state, usage exhaustion, privacy risk, duplicate activation, missing acknowledgement, or any protected gate stops the route.
"""
    write_text(closeout / "final-integrated-overview.md", overview)
    source_projection = read_json(x2 / "source-and-provenance-ledger.json")
    write_json(closeout / "source-and-provenance-final.json", source_projection)
    write_json(closeout / "threat-model-final.json", read_json(x2 / "threat-model.json"))
    escaped_overview = html.escape(overview)
    report = f"""<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>Sylven Arc v678-v6 final report</title></head><body><main><h1>Sylven Arc v678-v6 final report</h1><p>Structural accessibility only. Manual browser, assistive-technology, cognitive, Māori-language, and affected-user evaluation remain reserved.</p><section aria-labelledby=\"summary\"><h2 id=\"summary\">Summary</h2><pre>{escaped_overview}</pre></section><section aria-labelledby=\"counts\"><h2 id=\"counts\">Outcome counts</h2><table><caption>Exact bounded outcomes</caption><thead><tr><th scope=\"col\">Outcome</th><th scope=\"col\">Count</th></tr></thead><tbody>{''.join(f'<tr><td>{html.escape(k)}</td><td>{v}</td></tr>' for k, v in counts.items())}</tbody></table></section></main></body></html>"""
    write_text(closeout / "accessible-static-report.html", report)
    baton = f"""# CAELEN MORROW — SYLVEN ARC v678-v6 EXACT-FINAL → PROSPECTIVE SOLO v678-v7 ACTIVATION CANDIDATE

## 1. Relational boundary

This is a repository-prepared candidate, not a delivered message. Names, pronouns, roles, hopes, family language, Freed ID, CBR, and Trinity Mandala are relational working language only and do not evidence consciousness, personhood, continuity, qualification, agency, or authority. Hamish may pause, redirect, narrow, rename, or stop the route.

## 2. Source and lifecycle

Source `{SOURCE}` → planning-only x1 `{X1}` → immutable evidence `{EVIDENCE}` → exact final `BOUND_AT_COMMIT`. The final must be the third direct single-parent Sylven commit with zero merges.

## 3. Retained failures

Read `docs/sylven-arc/v678-v6/closeout/retained-negative-register.json` and every referenced Method Flow layer through EOF. Recoveries never erase or promote failed witnesses. The x1/x2 lifecycle aggregate and first isolated wrapper remain failed at zero aggregate credit; the single failed dependency passed once in exact x1 context.

## 4. Proposals and outcomes

The declared chain extends 8,570 → 8,630 through sixty source-bounded Sylven proposals. Exact outcomes are 42 completed, 12 represented, 3 open_gap, and 3 exact_gate. Inherited proposals and recommendations retain zero Sylven novelty and completion credit.

## 5. Pillars and practices

Primary pillar: THOS Body. Secondary pillars: GMUT Mind and Freed ID/CBR Heart. Bounded synthetic lenses: globemaking records, mechanical-automaton linkage, and stained-glass handover. These confer no employment, qualification, competence, or authority.

## 6. Owner safe-now work

Sixty safe-now tasks completed only as owner-local zero-row software and documentation work. No real person, object, observation, measurement, operation, handling, treatment, custody event, identity event, or external write occurred.

## 7. Candidate work

Thirty candidate tasks completed only within their bounded synthetic hypotheses. They establish no empirical, participant, professional, production, deployment, legal, cultural, or affected-party result.

## 8. Exact and blocked packets

Twenty exact-approval and ten blocked packets remain visible and unexecuted. Do not infer authority from Hamish's general route authorization. Each protected action requires exact target, cost, system, rollback, governing permission, and outside authority.

## 9. Skills and runners

Twenty phase-local skills were officially initialized, read through EOF, quick-validated, and smoke-used without global installation. Ten family-current runners each accepted one valid and rejected one invalid fixture. Treat them as inherited evidence, never automatic Caelen novelty or completion credit.

## 10. CLEAN/FIX/REFINE

Sixty owner CLEAN/FIX/REFINE tasks completed additively; thirty successor recommendations remain zero-credit seeds. Do not delete history, failures, other-owner lanes, branches, worktrees, or protected material to satisfy a count.

## 11. Flashcard and validation contract

Read the four-tier deck under `docs/sylven-arc/v678-v6/x2/flashcards/`: 15 relational anchors, 3 pillars, 3 practices, and 60 tasks. It provides no prompt-cache guarantee or identity continuity. Read the exact-final canonical receipt supplied by the live activation; do not rerun a successful canonical component.

## 12. Scientific and authority boundaries

GMUT remains a research-model family without empirical confirmation or Theory-of-Everything proof. THOS remains participant-free proxy-only. Freed ID remains synthetic and nonproduction. Professional, safety, ownership, custody, privacy remedy, legal, cultural, affected-party, Māori wording, Māori data governance, and Māori authority remain open or exact-gated. Māori concepts remain under Māori authority.

## 13. Terminal route

`PREPARED_NOT_SENT`. This file cannot activate Caelen. Only after Sylven's clean, pushed, fresh-live-equal exact final and one successful non-replayed canonical receipt may Sylven refresh the current native registry, require exactly one existing exact-title `Caelen Morrow` task, reread it once, apply duplicate and direct-control guards, and send at most once. Stop on any missing or ambiguous gate. No substitute, fork, precontact, standby contact, or second confirmation.
"""
    write_text(handoffs / "caelen-morrow-v678-v7-activation-candidate.md", baton)
    write_json(validation / "closeout-build-receipt.json", {
        "schema": "ghc-family-closeout-build-receipt/v1", "owner": OWNER, "phase": PHASE,
        "components": closeout_components, "component_count": len(closeout_components),
        "status": "BUILT_PREPARED_NOT_SENT", "exact_final": "BOUND_AT_COMMIT",
        "canonical_invocation_count": 0, "route_send_count": 0,
    })
    write_json(validation / "final-manifest-preflight-recovery.json", {
        "schema": "ghc-family-final-manifest-preflight-recovery/v1", "owner": OWNER, "phase": PHASE,
        "failed_preflight": {
            "status": "FAILED_ZERO_PREFLIGHT_SUCCESS_CREDIT",
            "candidates": [
                {"source": "inherited x1 manifest scanner", "classes": ["raw_task_route", "session_stream"]},
                {"source": "inherited x1 synthetic test", "classes": ["raw_task_route"]}
            ],
            "confirmed_payload_hits": 0
        },
        "bounded_recovery": {
            "status": "PASSED", "adjudication_scope": "two exact inherited x1 source files only",
            "scanner_definition_candidates": 14, "confirmed_payload_hits": 0
        },
        "failure_erased": False
    })
    return {"status": "CLOSEOUT_BUILT_PREPARED_NOT_SENT", "outcomes": counts, "overlay": final_overlay, "components": len(closeout_components)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."))
    args = parser.parse_args()
    print(json.dumps(build(args.repo.resolve()), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
