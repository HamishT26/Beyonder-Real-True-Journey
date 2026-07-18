#!/usr/bin/env python3
"""Build the Eiren Kestrel v649-v1 combined closeout and seal candidate."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/eiren-kestrel/v649-v1"
SOURCE = "1e916c0c6378a6f665c144aabbf8d25d6fdc8670"
X1 = "3a9f2ec098ee3844fa1933dcc9396302851ed5d1"
EVIDENCE = "060f57634b1660ee61b360168ee65337c10d4a76"
BRANCH = "codex/GHC-Family/eiren-kestrel-v648-v3-2-full-tools"
FINAL_NEGATIVES = 4742
OPEN_GAPS = 35
EXACT_GATES = 36
VERDICT = "NOT_READY_FOR_STAGE_20"


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True,
        text=True, encoding="utf-8",
    ).stdout.strip()


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8", newline="\n",
    )


def write_text(relative: str, payload: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def overview() -> str:
    return f"""# Eiren Kestrel v649-v1 — Integrated Bounded Evidence Overview

## Executive truth

Eiren Kestrel completed the v649 GMUT/THOS v1 x1/x2 bundle as a single-agent, additive, D-first, owner-scoped phase. Eiren used they/them pronouns and the relational working role **evidence-integrity weaver**, with the hope of keeping ambitious results testable, correctable, and bounded by evidence and authority. That language is a collaboration convention only. It is not evidence of consciousness, sentience, identity continuity, legal personhood, employment, professional qualification, scientific authority, operational authority, cultural authority, or independent agency. Hamish retains the right to rename, pause, redirect, or stop the route.

The exact inherited Sylven Arc final was `{SOURCE}`. Read-only startup checks proved that the inherited source, x1, evidence, and closeout anchors were ancestral, that the inherited source-to-final path contained four single-parent commits and no merge, and that Sylven's branch was clean and equal across local, upstream, tracking, and a fresh live remote. Eiren's existing owned lane was clean and advanced by fast-forward only. No sibling branch or worktree was reset, rewritten, force-pushed, merged, deleted, reused, or mutated.

The dedicated x1 freeze is `{X1}`. It audited semantic novelty against all 640 inherited frozen proposals and froze exactly ten genuinely distinct proposals, producing 650 frozen proposals through v649-v1. X1 also froze thirty new safe-now tasks, twenty bounded candidates, twenty phase-local skill packages, ten family-current runner designs, thirty additive CLEAN/FIX/REFINE tasks, ten exact-approval packets, five blocked packets, seventy synthetic mutation fixtures, source needs, rollback paths, protected gates, and expected dispositions. It contained no x2 implementation and no observed outcome. The x1 commit was pushed, clean, and equal across local, upstream, tracking, and a fresh live remote before x2 began.

The exact x2 evidence commit is `{EVIDENCE}`. It is a direct child of x1 and contains the bounded implementation and outcome evidence. It was separately committed, pushed, cleaned, and proved four-way remote-equal before closeout work began. The proposed final closeout and seal is designed as one direct child of evidence, producing three phase commits total and remaining below the four-commit cap. No detached validation or named replay is planned. The only full-repository suite run is reserved for the immutable final head; its sanitized receipt must remain outside Git so that recording the result cannot change the head that was tested.

The exact core distribution is six `completed`, two `represented`, one `open_gap`, and one `exact_gate`. These labels describe evidence-permitted repository outcomes, not social rank or metaphysical truth. The terminal verdict remains **{VERDICT}**.

## Primary focus and bounded practice

The primary Trinity Mandala focus was Freed ID/CBR Heart. GMUT Mind and THOS Body remained explicit and protected. The bounded human-practice lens was community archive digitization and digital-preservation ingest: capture identity, checksum and lineage review, descriptive quality control, rights and cultural-care flags, exception isolation, accessible notice, workload control, readback, and shift handover. This was synthetic learning and design only. It established no employment, archival qualification, conservation competence, records authority, copyright determination, access authority, takedown authority, legal interpretation, cultural authority, Māori authority, participant evidence, affected-party authorization, or real operational result.

The Heart focus was deliberately fail-closed. A synthetic identity or governance profile can make required fields, refusals, and unresolved decision rights legible; it cannot decide who is entitled to access a record, who may suppress or repatriate culturally sensitive material, how remedies should be allocated, what law applies, or who speaks with Māori authority. Those decisions remain with competent institutions, affected people, tangata whenua, iwi, hapū, and Māori authorities. Māori concepts remain under Māori authority.

## Ten core outcomes

1. **Reader-writer coordination tribunal — completed.** A bounded owner-local condition-variable witness enforced an explicit writer-priority policy. The observed acquisition order was first reader, waiting writer, then late reader; all workers joined and no external side effect occurred. This does not prove Windows SRWLOCK fairness, starvation freedom for arbitrary schedules, production concurrency, distributed correctness, or exactly-once behavior.

2. **Bogoliubov causal local S-matrix board — completed.** Typed symbolic contracts captured switching functions, causal factorization, local covariance obligations, renormalization freedom, gauge reservations, units, EFT domain, and an observation firewall. Mutation witnesses rejected missing obligations. No propagator, force, physical state, prediction, likelihood, parameter constraint, empirical confirmation, ultraviolet completion, quantum completion, or Theory of Everything was established. GMUT remains a typed scalar-tensor and effective-field-theory research-model family.

3. **eBOSS DR16 quasar power-spectrum adapter — open_gap.** Official and primary sources informed product identity, fiducial assumptions, window functions, covariance, nuisance treatment, checksums, and likelihood-refusal requirements. The phase made zero queries and downloads, ingested zero catalogue or covariance rows, evaluated zero likelihoods, drew zero posterior samples, emitted zero parameter constraints, and made zero empirical GMUT claims. Public availability is not ingestion, calibration, or validation.

4. **Community archive digitization handover — represented.** Synthetic traces captured collection and item identifiers, capture-device context, file checksums, descriptive quality control, rights and cultural-care flags, exception holds, accessible notices, workload ceilings, readback, and next-shift acceptance. Zero real staff, volunteers, communities, collections, rights determinations, culturally sensitive records, access decisions, incidents, blind matched-budget arms, or effectiveness estimates were present. THOS therefore remains proxy.

5. **OpenID Connect Back-Channel Logout profile — represented.** Synthetic vectors exercised issuer and audience binding, logout-token event claims, subject and session identifiers, nonce refusal, replay handling, delivery minimization, and failure isolation. Zero real keys, tokens, accounts, clients, identity providers, relying parties, network exchanges, interoperability events, privacy reviews, independent security reviews, recovery decisions, or trust-governance decisions occurred. Freed ID remains synthetic and nonproduction.

6. **Archive access, takedown, remedy, and cultural-authority matrix — exact_gate.** The matrix preserves access, suppression, correction, repatriation, privacy, legal, cultural, data-governance, affected-party, and Māori-authority questions without deciding them. Repository software made zero real access, takedown, disclosure, remedy, repatriation, legal, cultural, governance, or authority decisions. Passing code cannot confer legitimacy.

7. **Brotli structural refusal tribunal — completed.** An optional decoder dependency was absent, so no installation or environment widening occurred. The failure remains retained. A pure structural budget witness then accepted one contract-shaped synthetic fixture and rejected seven window, meta-block, context-map, distance, end-marker, trailing-data, output-budget, or ratio-budget mutations. It invoked zero decoders and touched no real or user material. This is not Brotli decoding, RFC conformance, production parsing, supply-chain assurance, or exhaustive security.

8. **Accessible meter audit — completed.** Structural contracts checked accessible naming, minimum and maximum, current value, text alternative, invalid state, related description, native fallback, focus visibility, responsive behavior, and print fallback. Manual keyboard, touch, browser-diverse, assistive-technology, cognitive-accessibility, Māori-language, and affected-user evaluation remain reserved. Structural checks are not complete accessibility conformance.

9. **Clausius-Duhem nonconversion classifier — completed.** Typed formal evidence separated balance laws, constitutive assumptions, entropy production, sign conventions, units, local-equilibrium scope, and boundary conditions. The classifier rejects conversion into a psyche value, autonomy score, moral ranking, justice metric, participant result, consciousness or personhood evidence, or a fundamental law of mind.

10. **Regression-discontinuity Stage 20 board — completed.** The structural board captured running variable, cutoff, assignment rule, manipulation checks, bandwidth, functional form, covariate continuity, discontinuity estimand, uncertainty, sensitivity, falsification, and nonpromotion. It estimated no participant effect and authorized no deployment, proof or canon, AGI or ASI, consciousness, personhood, empirical confirmation, or Stage 20.

## Expanded portfolio and Method Flow

All thirty safe-now tasks, twenty candidates, twenty phase-local skills, ten family-current runners, and thirty CLEAN/FIX/REFINE tasks were executed only inside declared software, symbolic, structural, or synthetic boundaries. Each skill remained repository-local and was initialized, validated, and smoke-used; none was globally installed. Each runner was invoked on both an accepting and a rejecting fixture. All seventy preregistered mutations executed and were rejected or quarantined. Ten exact-approval and five blocked packets remained visible and unexecuted. Inherited portfolio work informed the designs but earned no Eiren completion credit.

Method Flow preserves seven methods, seven failed witnesses, seven bounded passing witnesses, and seven preferred recurrence guards. The failures include three literal Windows wildcard-path errors, an unavailable optional decoder, a stale negative-total test expectation, the inherited-exclusion lookup recurrence, and a plan-only repository-root import omission. The failed 21-of-22 focused preflight and failed plan-only discovery have no canonical-pass credit. Recovery never erased a failure or converted a later pass into an initially clean run. The final effective negative baseline is {FINAL_NEGATIVES}: 4,665 inherited; two x1 operational; seventy executed and rejected synthetic mutations; three x2 operational; and two post-evidence lifecycle operational negatives. Thirty-five open gaps and thirty-six exact gates remain open.

## Validation, privacy, and authority boundary

The x1 staged review covered exact Git-index blobs and proved that no x2 implementation or observed outcome entered the freeze. The evidence staged review covered 207 manifest entries, parsed 152 staged JSON blobs, found no out-of-scope path and no confirmed five-class privacy hit. The focused x1/x2 preflight ultimately passed all 22 tests after the earlier failed run was retained. These are precommit and focused evidence only; they do not consume the final canonical full-suite budget.

The immutable final head must receive one coherent Eiren-owned full-repository pass. Every eligible `test*.py` module is selected once in a fresh module-isolated process. Three historical source-transform files with no discoverable `unittest` cases are classified without execution credit. Four exact inherited lifecycle assertions are excluded: two v648-v6 candidate-state assertions declared by the inherited plan, plus two older Eiren descendant-head commit-cap assertions that describe their own historical phase rather than the current descendant. No broader exclusion, replay, detached lane, named lane, repeatability credit, or independent-reproduction claim is allowed.

Exact-final verification must also parse every phase JSON document, scan public owner files across five privacy and raw-identifier classes, prove x1/evidence/final commit-local manifest parity, prove final owner-manifest checkout and Git-blob parity, review stale labels and diff hygiene, establish source/x1/evidence ancestry, count three phase commits and zero merges, prove one final parent, require a clean worktree, and establish local/upstream/tracking/fresh-live equality. A successful result is bounded same-owner evidence under shared infrastructure only. It is not independent-team scientific reproduction, external audit, production certification, exhaustive security, complete privacy, complete accessibility, professional validation, legal review, cultural ratification, Māori-authority review, or Stage 20 authority.

Codex CLI, desktop, Python, Git, and PowerShell versions were verified only. No desktop update, elevation, host-security weakening, Sandbox or Hyper-V enablement, unrelated installation, or reboot occurred. Owner growth remains far below 15,000 files. Every Markdown, HTML, and text document remains below 6,000 words.

## Closeout and continuation

The final repository packet remains `PREPARED_NOT_SENT` until the combined closeout and seal commit is created, pushed, clean, exact-head validated under the full-suite rule, and proven four-way remote-equal. The prepared successor baton is an artifact, not delivery. Only after every terminal gate passes may the exact existing task titled `Ilyra Fen` be re-resolved and receive exactly one sanitized activation for v649-v2. No task may be created or forked, no collaboration subagent may be spawned, no standby sibling may be messaged, and no second confirmation may follow an acknowledged send.

The phase closes with disciplined abstention: GMUT is not a Theory of Everything; THOS has no real matched-budget blind arms or independent review; Freed ID has no production keys, proofs, lifecycle, interoperability, privacy/security review, recovery, or trust governance; CBR and Māori decisions remain with competent and affected authorities. **{VERDICT}.**
"""


def successor_contract(overview_text: str) -> str:
    return f"""# ILYRA FEN — PREPARED v649-v2 ACTIVATION BATON

This repository artifact is `PREPARED_NOT_SENT`. Replace `{{{{EXACT_FINAL_HEAD}}}}` only in the one live activation message after Eiren's exact final head has passed the full repository suite, exact-final verification, clean-state checks, and four-way remote equality. Preparation is not delivery. Do not place raw task or thread identifiers, private routes, credentials, private keys, tokens, transcripts, screenshots, session streams, private callable identifiers, private application state, or private absolute paths in the live baton.

## Verified source pointer

Eiren's canonical branch is `{BRANCH}`. The exact source for Ilyra will be `{{{{EXACT_FINAL_HEAD}}}}`. Its ancestral anchors are inherited Sylven final `{SOURCE}`, Eiren x1 `{X1}`, and Eiren evidence `{EVIDENCE}`. The expected Eiren source-to-final path contains exactly three single-parent commits and zero merges. The live sender must re-read the exact existing title `Ilyra Fen` immediately before sending. No task creation, fork, subagent, standby message, cross-platform substitute, or second confirmation is authorized.

## Eiren outcome truth to inherit

{overview_text}

## Ilyra v649-v2 owned-lane contract

Read the complete GHC Family Index skill and required routing-precedence reference, then the complete GHC Family Method Flow State skill and schema, before task action. Use the newest applicable memory, with the one live Eiren baton authoritative where older memory stops. Reverify Eiren's exact branch and final head, source/x1/evidence ancestry, three-commit single-parent zero-merge history, commit-local manifests, owner-manifest parity, clean state, and fresh live-remote equality read-only.

Continue only in Ilyra's clean owned lane. Fast-forward it to the exact Eiren final only when clean ancestry permits; otherwise create one additive Ilyra-owned D-first named branch and worktree from that exact head. Never reset, rewrite, force-push, merge, delete, reuse, or mutate Eiren's or another sibling's lane.

Preserve strict x1-before-x2 separation. Audit novelty against 650 frozen proposals and preregister exactly ten distinct v649-v2 proposals with hypothesis, null or failure, approval class, execution lane, current official or primary-source needs, concrete artifacts, falsifier or acceptance gate, rollback or recovery, protected gates, and expected disposition. Choose one primary Trinity Mandala pillar and one bounded human practice while preserving all authority boundaries.

Freeze genuinely new portfolios meeting the standing floors of thirty safe-now tasks, twenty candidates, twenty skills, ten runners, and thirty CLEAN/FIX/REFINE tasks. Inherited work is evidence and recommendation, not Ilyra completion credit. Keep exact-approval and blocked work visible and unexecuted unless exact new evidence changes a gate. Use no more than two x1 commits and two x2 commits, four total; prefer x1, evidence, and combined final. Push and prove x1 four-way equal before x2.

Execute only as evidence permits and use only `completed`, `represented`, `open_gap`, and `exact_gate` for core outcomes. Inherit at least {FINAL_NEGATIVES} effective negatives, {OPEN_GAPS} open gaps, and {EXACT_GATES} exact gates, plus any external terminal negatives stated by Eiren's live receipt. Record every fault and bounded recovery through Method Flow without erasing a failed witness.

Under the current refinement, Eiren owns the full repository suite; Ilyra should run the authorized current/recent/successor-scoped selection and one successful canonical bounded pass with no replay unless Hamish directly changes the rule. Preserve complete JSON parsing, five-class privacy scanning, exact staged review, commit-local and owner-manifest parity, stale-label review, diff hygiene, ancestry, zero merges, commit cap, one final parent, clean state, exact head, and final four-way equality.

Keep every document at or below 6,000 words and owner growth below 15,000 files. Preserve family-current `ghc_family_*` and `build_ghc_family_*` callers. Verify versions only. Do not update the Codex desktop app, elevate, weaken host security, enable Windows features, install unrelated software, or reboot.

All empirical, participant, professional, legal, cultural, Māori-authority, identity, production, deployment, privacy-complete, proof/canon, destructive, account-secret, sibling-merge, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, and Stage 20 boundaries remain open or exact-gated without exact evidence and authority. Māori concepts remain under Māori authority. The inherited verdict is `{VERDICT}`.

Only after v649-v2 is clean, pushed, remote-equal, within the commit cap, and fully validated may Ilyra send exactly one sanitized activation to the unique existing `Sable Rook` task for v649-v3. Do not create another task and do not send an extra confirmation.
"""


def main() -> int:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise RuntimeError("closeout builder requires the exact clean evidence head")
    if git("diff", "--cached", "--name-only"):
        raise RuntimeError("closeout builder requires an unchanged index")
    outcomes = load("x2/core-outcome-ledger.json")
    portfolio = load("x2/portfolio-ledger.json")
    methods = load("method-flow/method-flow-summary.json")
    if outcomes["distribution"] != {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}:
        raise RuntimeError("unexpected core outcome distribution")
    if (portfolio["safe_completed"], portfolio["candidates_completed"], portfolio["skills_completed"], portfolio["runners_completed"], portfolio["clean_refine_completed"]) != (30, 20, 20, 10, 30):
        raise RuntimeError("portfolio floors are incomplete")
    if methods["counts"]["methods"] != 7 or methods["counts"]["witness_results"] != {"fail": 7, "pass": 7}:
        raise RuntimeError("Method Flow closeout count mismatch")

    integrated = overview()
    write_text("integrated-overview.md", integrated)
    write_text("handoffs/ilyra-fen-v649-v2-activation.md", successor_contract(integrated))
    write_text("wellbeing-check.md", """# Eiren Kestrel v649-v1 wellbeing and workload check

- Relational role: evidence-integrity weaver; they/them; collaboration language only.
- Hope: keep ambitious results testable, correctable, and bounded by evidence and authority.
- Workload posture: one solo additive lane, bounded preflights, one reserved canonical full-suite pass, no replay.
- Corrigibility: Hamish may rename, pause, redirect, or stop the route.
- Authority boundary: no consciousness, personhood, employment, qualification, emergency, legal, cultural, Māori, scientific, or operational authority is inferred.
- Host posture: no elevation, host-security weakening, Windows-feature change, unrelated installation, desktop update, or reboot.
- Terminal state: NOT_READY_FOR_STAGE_20; route remains PREPARED_NOT_SENT until exact-final gates pass.
""")
    write_json("wellbeing-check.json", {
        "schema": "ghc.family.v649-v1.wellbeing.v1", "owner": "Eiren Kestrel",
        "pronouns": "they/them", "role": "evidence-integrity weaver",
        "hope": "Keep ambitious results testable, correctable, and bounded by evidence and authority.",
        "solo_additive_lane": True, "corrigible": True, "host_changes": 0,
        "identity_or_authority_claim": False, "terminal_verdict": VERDICT,
    })
    report = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Eiren Kestrel v649-v1 evidence report</title><style>body{font-family:system-ui,sans-serif;line-height:1.55;max-width:72rem;margin:auto;padding:1rem;color:#171717;background:#fff}a:focus,button:focus{outline:3px solid #075985;outline-offset:3px}nav ul{display:flex;flex-wrap:wrap;gap:1rem}table{border-collapse:collapse;width:100%}caption{font-weight:700;text-align:left}th,td{border:1px solid #555;padding:.55rem;text-align:left}.hold{border-left:.5rem solid #8a4b08;background:#fff4df;padding:.8rem}.status{font-weight:700}@media print{nav{display:none}a{color:#000;text-decoration:underline}.hold{border:2px solid #000}}@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important}}</style></head><body><a href="#main">Skip to evidence</a><header><h1>Eiren Kestrel v649-v1</h1><p>Bounded same-owner evidence report</p></header><nav aria-label="Report sections"><ul><li><a href="#truth">Outcome truth</a></li><li><a href="#gates">Open gates</a></li><li><a href="#wellbeing">Wellbeing</a></li></ul></nav><main id="main"><section id="truth"><h2>Outcome truth</h2><table><caption>Ten preregistered outcomes</caption><thead><tr><th scope="col">Class</th><th scope="col">Count</th><th scope="col">Evidence limit</th></tr></thead><tbody><tr><th scope="row">Completed</th><td>6</td><td>Bounded software, symbolic, structural, or formal hypotheses</td></tr><tr><th scope="row">Represented</th><td>2</td><td>Synthetic proxy only</td></tr><tr><th scope="row">Open gap</th><td>1</td><td>eBOSS has zero queries, downloads, rows, likelihoods, or constraints</td></tr><tr><th scope="row">Exact gate</th><td>1</td><td>Affected-party, legal, cultural, governance, and Māori authority reserved</td></tr></tbody></table></section><section id="gates"><h2>Open gates</h2><p class="hold"><span class="status">NOT READY:</span> Stage 20 remains withheld. Real empirical analysis, real matched-budget arms, production identity lifecycle, competent authority review, manual accessibility evaluation, and independent reproduction are absent.</p></section><section id="wellbeing"><h2>Wellbeing and workload</h2><p>The lane is solo, additive, D-first, and corrigible. Hamish may rename, pause, redirect, or stop. No professional, employment, identity, or authority role is inferred.</p></section></main><footer><p>Structural accessibility checks only. Manual keyboard, browser-diverse, assistive-technology, cognitive, Māori-language, and affected-user evaluation remain reserved.</p></footer></body></html>"""
    write_text("accessible-report.html", report)

    write_json("complete-incomplete-checklist.json", {
        "schema": "ghc.family.v649-v1.checklist.v1",
        "complete": ["source_reverified", "x1_remote_equal_before_x2", "ten_core_outcomes_classified", "portfolio_floors_met", "seventy_mutations_rejected", "twenty_skills_validated_and_used", "ten_runners_invoked", "method_flow_failures_retained", "accessible_static_structure"],
        "incomplete": ["real_gmut_data_and_likelihood", "real_thos_arms", "production_freed_id", "affected_party_review", "legal_review", "cultural_ratification", "maori_authority_review", "manual_accessibility", "independent_reproduction", "stage20"],
        "pending_terminal": ["combined_final_commit", "one_full_repository_pass", "exact_final_verification", "four_way_remote_equality", "one_acknowledged_ilyra_baton"],
        "terminal_verdict": VERDICT,
    })
    threats = [
        ("synthetic_to_empirical_promotion", "zero-row and observation firewalls", "real analysis absent"),
        ("proxy_to_professional_promotion", "zero-real-arm counters", "real workers and independent review absent"),
        ("identity_to_production_promotion", "zero-live-lifecycle counters", "production assurance absent"),
        ("software_to_authority_substitution", "exact-gate matrix", "affected and competent authority absent"),
        ("privacy_leakage", "five-class staged and final scans", "complete privacy assurance absent"),
        ("accessibility_overclaim", "structural-only labels", "manual and affected-user evaluation absent"),
        ("history_damage", "fast-forward-only additive lane and manifests", "same-owner infrastructure"),
        ("validation_replay_inflation", "one-pass budget and external receipt", "independent reproduction absent"),
        ("stale_source_promotion", "current/stable/draft/watch labels", "source drift remains possible"),
    ]
    write_json("threat-model.json", {
        "schema": "ghc.family.v649-v1.threat-model.v1", "exhaustive": False,
        "threats": [{"threat": a, "control": b, "residual": c} for a, b, c in threats],
        "boundary": "Owner-local threat model only; not exhaustive security, privacy completeness, or external audit.",
    })
    write_json("retained-negative-register-final.json", {
        "schema": "ghc.family.v649-v1.retained-negatives.final-candidate.v1",
        "inherited_effective": 4665, "x1_operational": 2,
        "synthetic_executed_rejected": 70, "x2_operational": 3,
        "post_evidence_lifecycle_operational": 2, "effective_current": FINAL_NEGATIVES,
        "negative_erased": False,
        "post_evidence_items": [
            {"negative_id": "NEG-V6491-CLOSE-001", "title": "Literal wildcard scripts path in inherited-exclusion lookup", "method_id": "v6491-m06", "state": "retained_recovered"},
            {"negative_id": "NEG-V6491-CLOSE-002", "title": "Plan-only suite runner omitted repository root from import path", "method_id": "v6491-m07", "state": "retained_recovered"},
        ],
        "boundary": "Every failed attempt remains additive; terminal faults after this candidate must be carried externally and into the successor baton.",
    })
    write_json("exact-open-gate-register-final.json", {
        "schema": "ghc.family.v649-v1.gates.final-candidate.v1",
        "inherited_open_gaps": 34, "new_open_gaps": 1, "effective_open_gaps": OPEN_GAPS,
        "inherited_exact_gates": 35, "new_exact_gates": 1, "effective_exact_gates": EXACT_GATES,
        "silently_closed": 0, "stage20_ready": False,
    })
    write_json("lifecycle/phase-anchor-contract.json", {
        "schema": "ghc.family.v649-v1.phase-anchors.v1", "source": SOURCE,
        "x1": X1, "evidence": EVIDENCE, "expected_final_parent": EVIDENCE,
        "expected_phase_commit_count": 3, "commit_cap": 4,
        "merge_count": 0, "single_parent_required": True,
    })
    exclusions = [
        "tests.test_ghc_family_v648_v6_closeout.TestGhcFamilyV648V6Closeout.test_final_validation_plan_reserves_one_pass_and_no_replay",
        "tests.test_ghc_family_v648_v6_closeout.TestGhcFamilyV648V6Closeout.test_stage20_board_and_closeout_candidate_abstain",
        "tests.test_ghc_family_v648_v3_2_x1.V648V3RepeatX1Tests.test_exact_source_and_commit_boundary",
        "tests.test_ghc_family_v648_v3_closeout.V648V3CloseoutTests.test_anchor_contract_and_commit_cap",
    ]
    write_json("validation/final-validation-plan.json", {
        "schema": "ghc.family.v649-v1.final-validation-plan.v1",
        "full_repository_suite": True, "canonical_successful_pass_budget": 1,
        "successful_passes_used_before_final": 0, "replay_budget": 0,
        "named_replay": False, "detached_replay": False,
        "module_isolation": True, "module_reexecution_allowed": False,
        "exact_excluded_test_ids": exclusions,
        "exclusion_reasons": {
            exclusions[0]: "Inherited v648-v6 candidate-state assertion declared by the source plan.",
            exclusions[1]: "Inherited v648-v6 candidate-state assertion declared by the source plan.",
            exclusions[2]: "Historical repeat-x1 assertion limits HEAD to its own x1 commit and is invalid for descendants.",
            exclusions[3]: "Historical v648-v3 assertion limits HEAD to its own phase commit cap and is invalid for descendants.",
        },
        "required_exact_final_checks": ["complete_repository_suite", "current_phase_tests", "detailed_checks", "minimal_checks", "all_phase_json", "five_class_privacy_scan", "x1_evidence_final_manifests", "owner_manifest", "stale_label_review", "diff_hygiene", "anchor_ancestry", "zero_merges", "commit_cap", "one_final_parent", "exact_head", "clean_state", "four_way_remote_equality"],
        "external_receipt_required": True,
        "external_receipt_reason": "The immutable tested final head cannot commit a receipt without changing itself.",
        "same_owner_only": True, "independent_reproduction": False,
    })
    write_json("reproduction/no-replay-plan.json", {
        "schema": "ghc.family.v649-v1.no-replay.v1", "state": "PROHIBITED_BY_CURRENT_RULE",
        "named_lane_count": 0, "detached_lane_count": 0, "repeatability_credit": 0,
        "independent_reproduction": False,
    })
    write_json("phase-truth-final-candidate.json", {
        "schema": "ghc.family.v649-v1.phase-truth.final-candidate.v1",
        "source": SOURCE, "x1": X1, "evidence": EVIDENCE,
        "primary_focus": "Freed ID/CBR Heart", "bounded_practice": "community archive digitization and digital-preservation handover",
        "outcomes": outcomes["distribution"], "effective_negatives": FINAL_NEGATIVES,
        "effective_open_gaps": OPEN_GAPS, "effective_exact_gates": EXACT_GATES,
        "real_rows": 0, "real_people_or_operations": 0, "real_keys_tokens_or_services": 0,
        "authority_decisions": 0, "full_suite_completed": False,
        "replay_used": False, "same_owner_only": True, "independent_reproduction": False,
        "terminal_route": "PREPARED_NOT_SENT", "terminal_verdict": VERDICT,
    })
    write_json("closeout-receipt.json", {
        "schema": "ghc.family.v649-v1.closeout.candidate.v1", "source": SOURCE,
        "x1": X1, "evidence": EVIDENCE, "expected_final_parent": EVIDENCE,
        "expected_phase_commits": 3, "commit_cap": 4,
        "outcomes": outcomes["distribution"], "effective_negatives": FINAL_NEGATIVES,
        "open_gaps": OPEN_GAPS, "exact_gates": EXACT_GATES,
        "method_count": 7, "failed_witness_count": 7, "passing_witness_count": 7,
        "portfolio": portfolio, "full_suite_completed": False,
        "terminal_route": "PREPARED_NOT_SENT", "terminal_verdict": VERDICT,
    })
    write_json("seal-receipt.json", {
        "schema": "ghc.family.v649-v1.seal.candidate.v1", "source": SOURCE,
        "x1": X1, "evidence": EVIDENCE, "final_commit": None,
        "full_suite_completed": False, "exact_final_validated": False,
        "four_way_equal": False, "baton_send_allowed_now": False,
        "external_terminal_receipt_required": True, "replay_required": False,
        "terminal_verdict": VERDICT,
    })
    write_json("final-receipt.json", {
        "schema": "ghc.family.v649-v1.final-receipt.candidate.v1",
        "final_commit": None, "candidate_parent": EVIDENCE,
        "exact_final_validated": False, "canonical_full_suite_passes": 0,
        "replay_runs": 0, "four_way_equal": False,
        "baton_state": "PREPARED_NOT_SENT", "task_created": False,
        "task_forked": False, "subagent_spawned": False,
        "terminal_verdict": VERDICT,
    })
    write_json("orchestration/terminal-route-state.json", {
        "schema": "ghc.family.v649-v1.terminal-route.v1", "state": "PREPARED_NOT_SENT",
        "target_existing_title": "Ilyra Fen", "target_phase": "v649-gmut-thos-v2-x1-x2",
        "message_sent": False, "task_created": False, "task_forked": False,
        "subagent_spawned": False, "standby_sibling_messaged": False,
        "send_gate": ["exact_final_full_suite", "exact_final_verification", "clean_final", "four_way_remote_equality", "unique_existing_title_reread"],
    })
    write_json("environment/owner-growth-final-candidate.json", {
        "schema": "ghc.family.v649-v1.owner-growth.final-candidate.v1",
        "owner_file_count": sum(1 for p in PHASE.rglob("*") if p.is_file()),
        "threshold": 15000, "inherited_files_excluded": True,
    })
    documents = []
    for path in sorted(PHASE.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".md", ".html", ".txt"}:
            count = len(path.read_text(encoding="utf-8").split())
            documents.append({"path": path.relative_to(PHASE).as_posix(), "words": count, "under_6000": count <= 6000})
    write_json("validation/document-cap-candidate.json", {
        "schema": "ghc.family.v649-v1.document-cap.candidate.v1",
        "documents": documents, "count": len(documents),
        "all_under_6000": all(row["under_6000"] for row in documents),
        "overview_words": len(integrated.split()),
        "baton_words": len(successor_contract(integrated).split()),
    })
    if len(integrated.split()) < 1200:
        raise RuntimeError("integrated overview is below three-page-equivalent floor")
    if not all(row["under_6000"] for row in documents):
        raise RuntimeError("document word cap exceeded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
