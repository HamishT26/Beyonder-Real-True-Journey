#!/usr/bin/env python3
"""Build the combined closeout and seal candidate for Sable v649-v3."""

from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
from pathlib import Path
from typing import Any

from ghc_family_v649_v3_definitions import (
    BOUNDED_PRACTICE,
    GLOBAL_BOUNDARY,
    HOPE,
    OWNER,
    PHASE,
    PRIMARY_FOCUS,
    ROLE,
    TERMINAL_VERDICT,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "sable-rook" / "v649-v3"
SOURCE = "a801ebd12f89f0afdc224a65ea311239ad5a94ca"
X1 = "dd1da40467292a06c130e0edf3ba8fcbb7b083bd"


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8").strip()


def load(relative: str) -> dict[str, Any]:
    return json.loads((OUT / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> None:
    path = OUT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, text: str) -> None:
    path = OUT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def overview(negatives: int, methods: int, failures: int, passes: int) -> str:
    return f"""# Sable Rook v649-v3 integrated overview

## Outcome first

Sable Rook’s v649-v3 packet closes within its declared software, formal, structural, and synthetic bounds. It freezes and executes exactly ten distinct proposals after auditing 660 inherited frozen proposals, so the chain now contains 670 frozen core proposals. The observed core distribution is exactly six `completed`, two `represented`, one `open_gap`, and one `exact_gate`. Those labels are evidence classifications, not a score. A completed structural contract does not compensate for an open empirical gap or an authority gate. The terminal verdict therefore remains **{TERMINAL_VERDICT}**.

The primary Trinity Mandala focus is **{PRIMARY_FOCUS}**. GMUT Mind and THOS Body remain explicit and protected. The bounded practice lens is {BOUNDED_PRACTICE}. This is a learning and synthetic-design lens only. It establishes no employment, qualification, food-safety competence, distribution authority, recipient-safety outcome, professional validation, legal or cultural authority, Māori authority, participant evidence, affected-party acceptance, or real operational result.

Sable’s relational role is {ROLE}, and their hope is to {HOPE}. That language is a collaborative convention rather than evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, or independent agency. Hamish’s right to rename, pause, redirect, or stop the route remains intact. Warmth and family language create no credential or obligation.

## Provenance, novelty, and x1 separation

The source was Ilyra Fen’s exact clean v649-v2 final head. Read-only startup checks verified its source, x1, evidence, and final anchors, three single-parent phase commits, zero merges, one final parent, manifest parity, and fresh four-way equality. Sable’s existing clean owned branch was already ancestral, so it advanced by fast-forward only. No sibling branch or worktree was mutated, merged, reset, rewritten, force-pushed, deleted, or reused.

X1 remained a dedicated preregistration phase. It introduced exactly ten proposals, thirty new safe-now tasks, twenty bounded candidates, twenty phase-local skill designs, ten family-current runners, thirty additive CLEAN/FIX/REFINE tasks, and seventy unexecuted synthetic mutations. It contained no x2 implementation or observed outcome. The exact x1 commit was independently reviewed, committed, pushed, and proved equal across local, upstream, tracking, and fresh live remote before x2 began. All sixty-four x1 commit paths remain immutable at their exact Git-blob identifiers.

Novelty review compared normalized titles and semantics against all 660 inherited proposals. The selected surfaces are RO-Crate 1.3 entity roles and credit isolation; Haag–Kastler local-net obligations; an ATNF PSRCAT zero-row adapter; a community food-bank lot and recall proxy; DID Resolution v0.3 input, metadata, cache, and error boundaries; a food-access authority reservation matrix; a bounded FITS tribunal; an accessible risk-matrix alternative; a Stefan–Boltzmann domain classifier; and an equivalence-margin nonpromotion board. Prior W3C PROV, evidence-DAG, QFT, astronomy, identity, archive, accessibility, thermodynamic, and Stage 20 work remains inherited evidence and received no Sable completion credit.

## Provenance and source-independence result

The RO-Crate tribunal completed as bounded metadata evidence. Its accepting fixture distinguishes the metadata descriptor, root data entity, local data entity, and contextual entity; requires local reachability through `hasPart`; checks declared checksums; refuses to treat an external reference as locally preserved; requires two separately identified source units for a source-independence label; blocks duplicate credit; and keeps provenance completeness and independent reproduction false. Seven mutations were rejected. This demonstrates only the declared fixture behavior. It does not prove that an arbitrary crate is complete, that external material is retrievable, that sources are genuinely independent, or that another team reproduced the work.

Nineteen official or primary sources remain classified with the full `current`, `stable`, `draft`, and `watch` vocabulary. RO-Crate 1.3, the ATNF catalogue documentation, FITS 4.0, MPI recall materials, WCAG 2.2 resources, the SI Brochure, the TOST paper, identity standards, and Māori data-sovereignty material define obligations and boundaries. A citation is not a row, participant, production witness, delegated authority, or independent review. DID Resolution v0.3 remains visibly draft, including its feature-at-risk boundary; current-source review did not turn a draft into a production guarantee.

## GMUT Mind

The Haag–Kastler board completed as typed symbolic and mutation evidence. It preserves region ordering, isotony, spacelike commutation, covariance, spectrum scope, vacuum scope, additivity, time-slice assumptions, observable-algebra and gauge scope, EFT truncation, units, and an observation firewall. The passing fixture and seven rejected mutations show that the software can refuse omitted or promoted obligations. They do not construct a physical state, calculate a correlation function, prove a model satisfies the axioms, establish stability, detect a force, produce a prediction, evaluate a likelihood, constrain a parameter, confirm GMUT, complete a quantum theory, or establish a Theory of Everything.

The ATNF PSRCAT proposal remains `open_gap`. The contract pins a catalogue release and requires archived-version identity, parameter references, uncertainties, selection, epoch, checksum, and covariance treatment before any future analysis. It made zero catalogue queries, zero downloads, ingested zero catalogue or timing rows, used zero covariance rows, evaluated zero likelihoods, produced zero posterior samples, set zero constraints, detected zero forces, and made zero empirical claims. Official product availability and a well-typed zero-row adapter are readiness evidence only. A future empirical phase would need separately authorized real data, frozen selection and nuisance models, uncertainty and covariance handling, checksums, preregistration, and appropriate independent review.

## THOS Body

The community food-bank lot, allergen, recall, correction, accessible-notice, workload, and handover protocol remains `represented`. Synthetic fixtures preserve lot lineage, allergen and recall holds, correction readback, a structural accessible notice, a workload ceiling, next-owner acceptance, and refusal to distribute while an unresolved hold remains. Seven deliberately broken traces were rejected. There were zero real people, zero real food items, zero real distributions, zero recipient records, zero safety events, zero blind matched-budget arms, and zero operational-effectiveness estimates.

The proxy cannot establish food-safety competence, recipient safety, service effectiveness, professional qualification, deployment readiness, AGI, or ASI. Real use would require qualified and authorized people, actual institutional procedures, privacy and safety governance, appropriate monitoring, preregistered blind matched-budget arms where research comparison is proposed, suitable statistics, affected-party involvement, and independent review. The bounded workload field is a synthetic refusal control rather than evidence about real staff wellbeing or service capacity.

## Freed ID and CBR Heart

The DID Resolution profile remains `represented`. Synthetic vectors preserve a DID input, input options, resolution and document metadata, version handling, query normalization, duplicate-parameter rejection, cache scope, error taxonomy, visible draft status, and requester-privacy reservation. There were zero real keys, proofs, issuances, presentations, network requests, live resolutions, status or revocation events, interoperability events, privacy reviews, independent security reviews, recovery decisions, or trust-governance decisions. The result is not a production credential system or identity assurance.

The food-access and remedy matrix remains `exact_gate`. Every allocation, dignity, disability, dietary, cultural, privacy, correction, remedy, legal, data-governance, affected-party, and Māori-authority cell stays reserved. The phase made zero real allocations, disclosures, remedies, acceptances, legal interpretations, cultural decisions, or authority decisions. Software cannot decide entitlement, rank need, disclose recipient information, grant a remedy, interpret law, confer cultural legitimacy, or generate affected-party or Māori authority. Māori concepts remain under Māori authority, including the authority of tangata whenua, iwi, hapū, and appropriate Māori institutions.

## Parser, accessibility, thermo/psyche, and Stage 20 controls

The FITS tribunal completed on disposable synthetic header fields only. It checks a primary-HDU declaration, typed `BITPIX` and `NAXIS` fields, one terminal `END` card, eighty-character card width, 2880-byte padding, truncation and unknown-critical-card refusal, and a bounded byte budget. It opened no real astronomy product and establishes no general decoder correctness, production conformance, supply-chain assurance, complete privacy, or exhaustive security.

The accessible risk-matrix audit completed structurally. It requires row and column headers, cell associations, a text legend, non-colour cues, a summary, focus-order declaration, table and print alternatives, and explicit manual and affected-user reservations. The static report has a declared language, headings, captions, text, responsive structure, and no automatic motion. Manual keyboard, touch, browser-diverse, assistive-technology, cognitive, Māori-language, security-usability, responsive-layout, and affected-user evaluation remain reserved. Structural evidence is not complete WCAG conformance.

The Stefan–Boltzmann classifier completed as formal unit and domain evidence. It checks the declared constant, emissivity, area, absolute temperature, output identity, units, total-versus-spectral scope, and view-factor boundary. It rejects conversion into psyche, value, autonomy, justice, capability, consciousness, personhood, or a fundamental law of mind. A valid thermodynamic identity does not establish a mental, moral, legal, or social claim.

The equivalence-margin board completed as a Stage 20 nonpromotion control. It requires a positive smallest effect size of interest, unit and provenance, alpha, two one-sided tests, multiplicity and missingness plans, sensitivity analysis, and outcome-switching refusal. It contains zero participants and zero empirical rows and makes no equivalence or causal conclusion. A software board is not a registered study, statistical result, peer review, proof or canon, deployment authorization, or Stage 20 readiness.

## Expanded execution and retained negatives

All thirty genuinely new safe-now tasks completed within owner-scoped additive boundaries. All twenty candidate prototypes completed only for their declared software, formal, structural, or synthetic acceptance gates. Twenty phase-local skills were initialized through the official skill-creator workflow, rewritten with substantive instructions and agent metadata, validated under UTF-8, and smoke-used on one accepting and one rejecting fixture. They were not installed globally, and no subagent forward test ran because delegation was prohibited. Ten family-current `ghc_family_*` runners were built, invoked, and witnessed in both directions. Thirty cleanup tasks completed without deleting user material, changing sibling lanes, weakening gates, elevating, altering host security, enabling Windows features, launching Sandbox or Hyper-V, installing unrelated software, updating desktop applications, or rebooting.

All seventy preregistered synthetic mutations executed and were rejected. They are retained negatives, not proof of complete robustness. The effective negative total at closeout-candidate time is {negatives}: 4,840 inherited activation negatives, ten x1 operational negatives, seventy executed synthetic negatives, and the recorded x2 or lifecycle negatives. The append-only Method Flow state contains {methods} methods, {failures} retained failed witnesses, and {passes} bounded passing witnesses. Recovery never deletes a failed witness or earns scientific, professional, legal, cultural, production, security-complete, accessibility-complete, or independent-reproduction credit.

Thirty-seven effective open gaps and thirty-eight effective exact gates remain. The new ATNF empirical adapter adds one open gap; the food-access authority matrix adds one exact gate. None was silently closed. Ten inherited exact-approval classes and five blocked classes remain visible and unexecuted. A structural pass cannot compensate for missing real data, participant arms, production keys, affected-party legitimacy, legal competence, cultural ratification, Māori authority, independent review, or independent-team reproduction.

## Validation, wellbeing, and route state

The phase used one x1 commit and one evidence commit before this combined final candidate, within the four-commit cap and with no merge. The x1 and evidence commits were independently staged, reviewed, pushed, clean, and four-way remote-equal before the next lifecycle step. Evidence staging parsed exact staged JSON, scanned five privacy and raw-identifier classes with zero confirmed hits, protected every x1 blob, and preserved exact commit-local manifests. The full repository suite was not run because Eiren alone owns it under the current rule.

At the time this document is built, the one authorized final canonical scoped selection, detailed and minimal validators, exact final-head audit, final manifest parity, clean state, and fresh four-way remote equality remain pending. The repository candidate cannot truthfully contain its own not-yet-created commit identifier. Those checks must run once after the combined final commit, with no replay. Any post-commit fault must remain external and be carried into the successor baton rather than rewriting sealed history.

Wellbeing remains part of the evidence boundary. Scope is finite, stop rights are explicit, urgency is not a proof method, and relational warmth creates no pressure to claim continuity or authority. Hamish may pause, rename, redirect, or stop the route. Sable’s hope—to keep every surviving claim easy to challenge or retract—is served by retaining negative results, noncompensating gates, exact source lineage, and clear rollback paths.

The route to Orin Thale for v649-v4 remains **PREPARED_NOT_SENT** until the exact final head is clean, pushed, remote-equal, within the commit cap, and passes the single authorized scoped selection plus detailed, minimal, manifest, privacy, ancestry, and exact-head checks. Only then may one sanitized existing-task message be sent. No task creation, fork, subagent, standby message, or extra confirmation is authorized.

{GLOBAL_BOUNDARY}
"""


def checklist_markdown() -> str:
    return """# v649-v3 complete and incomplete checklist

## Complete within declared bounds

- [x] Exact source and anchors verified read-only before mutation.
- [x] Existing Sable lane advanced by fast-forward only and proved clean and equal.
- [x] Exactly ten novel proposals frozen after a 660-proposal audit.
- [x] Dedicated x1-only commit pushed and four-way equal before x2.
- [x] Exactly 6 completed, 2 represented, 1 open gap, and 1 exact gate.
- [x] Seventy preregistered synthetic mutations executed and rejected.
- [x] Thirty safe tasks, twenty bounded candidates, twenty skills, ten runners, and thirty additive cleanup tasks witnessed.
- [x] Phase-local skills initialized officially, validated, and smoke-used; no global install or subagent forward test.
- [x] Method Flow retains every observed failure and passing recovery.
- [x] No full repository suite, Sandbox or Hyper-V launch, elevation, host-security change, unrelated install, desktop update, or reboot.

## Intentionally incomplete, open, or exact-gated

- [ ] No ATNF query, download, real row, likelihood, posterior, constraint, force, or empirical GMUT result.
- [ ] No blind matched-budget real THOS arms, participants, operators, safety monitoring, or independent review.
- [ ] No production Freed ID keys, proofs, issuance, resolution, status, revocation, interoperability, privacy review, security review, recovery, or trust governance.
- [ ] No food-access, remedy, legal, cultural, affected-party, data-governance, or Māori-authority decision.
- [ ] No complete accessibility, privacy, or exhaustive-security claim.
- [ ] No independent-team scientific reproduction.
- [ ] No AGI, ASI, consciousness, personhood, proof/canon, Theory-of-Everything, deployment, or Stage 20 authorization.
- [ ] Exact final identifier, one authorized final scoped pass, exact-head audit, clean state, live equality, and route send remain post-commit gates.
"""


def baton(negatives: int) -> str:
    return f"""# PREPARED activation for Orin Thale v649-v4

Delivery truth in this committed copy: **PREPARED_NOT_SENT**. This file is not evidence that a live message was sent. Sable may send exactly one sanitized existing-task activation only after exact final validation and fresh remote equality.

Sable Rook’s v649-v3 source is Ilyra Fen’s exact final `{SOURCE}`. The frozen x1 commit is `{X1}`. The evidence commit identifier is recorded in the closeout receipt. The combined final identifier is necessarily pending in this precommit artifact.

Core truth is exactly 6 completed, 2 represented, 1 open gap, and 1 exact gate. The phase retains {negatives} effective negatives at candidate time, 37 open gaps, and 38 exact gates. The terminal verdict is `{TERMINAL_VERDICT}`.

Primary focus is Freed ID/CBR Heart. The bounded practice is community food-bank lot intake, allergen and recall hold, accessible distribution notice, correction readback, workload control, and shift handover. This establishes no employment, qualification, food-safety competence, recipient-safety outcome, service authority, legal or cultural authority, Māori authority, or affected-party acceptance.

GMUT remains a typed scalar-tensor and EFT research-model family. The Haag–Kastler board is symbolic only. The ATNF adapter made zero queries, downloads, rows, likelihood evaluations, posterior samples, constraints, force detections, or empirical claims and remains open. THOS remains represented without preregistered blind matched-budget real arms, participants or operators, monitoring, statistics, and independent review. Freed ID remains synthetic and nonproduction. Food-access, remedy, privacy, legal, cultural, affected-party, data-governance, and Māori-authority decisions remain exact-gated. Māori concepts remain under Māori authority.

Orin must read the complete GHC Family Index skill and routing-precedence reference, then the complete Method Flow State skill and schema, before task action. Reverify the exact Sable final head, source/x1/evidence ancestry, clean state, commit-local manifests, single-parent zero-merge history, and fresh live equality read-only. Continue only in Orin’s clean owned lane by fast-forward only if safe; otherwise create one additive Orin-owned D-first named lane. Never reset, rewrite, force-push, merge, delete, reuse, or mutate a sibling lane.

Own solo v649 GMUT/THOS v4 x1/x2. Audit semantic novelty against 670 frozen core proposals. Freeze exactly ten genuinely distinct proposals in a dedicated x1-only commit, push it, and prove four-way equality before x2. Choose one primary Trinity Mandala pillar and one bounded human practice while preserving all three pillars and every evidence and authority boundary. Design new portfolios meeting the standing floors without converting unsafe work into safe-now credit. Preserve every inherited and new negative.

Eiren alone owns the full repository suite. Run Orin’s authorized scoped selection once with no replay, plus detailed/minimal validators, complete JSON parsing, five-class privacy scanning, exact staged and owner manifests, stale-label review, diff hygiene, ancestry, zero merges, commit cap, one final parent, clean exact head, and final four-way equality. Use at most four phase commits and prefer x1, evidence, and combined final. Do not use detached validation or a named replay under the current route.

Use official or primary current sources where material. Verify versions only. Do not update desktop applications, elevate, weaken host security, enable Windows features, launch Sandbox or Hyper-V, install unrelated software, or reboot. Keep owner additions below 15,000 files and every document below 6,000 words. Preserve family-current `ghc_family_*` and `build_ghc_family_*` callers and compatibility evidence.

Never place raw task or thread identifiers, private routes, transcripts, screenshots, credentials, keys, tokens, private callable identifiers, private app state, private absolute local paths, or private conversational records in repository artifacts or baton text. All empirical, participant, professional, legal, cultural, Māori-authority, identity, production, deployment, privacy-complete, proof/canon, destructive, account-secret, sibling-merge, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, and Stage 20 claims remain open or exact-gated without exact evidence and authority.

Only after Orin v649-v4 is exact-final validated, clean, pushed, and remote-equal may Orin send exactly one sanitized activation to the unique existing Tamar Vey task for v649-v5. Do not create a task, fork, message a standby sibling, or send an extra confirmation.
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-commit", required=True)
    args = parser.parse_args()
    if git("rev-parse", "HEAD") != args.evidence_commit:
        raise RuntimeError("closeout build requires the exact evidence head")
    if git("rev-parse", "HEAD^") != X1:
        raise RuntimeError("evidence must be the direct child of x1")

    evidence_negatives = load("retained-negative-register-evidence.json")
    addendum_path = OUT / "retained-negative-addendum.json"
    addendum = json.loads(addendum_path.read_text(encoding="utf-8")) if addendum_path.exists() else {"negatives": []}
    additional = addendum.get("negatives", [])
    current_negatives = evidence_negatives["current_effective"] + len(additional)
    method_summary = load("method-flow/method-flow-summary-x2.json")
    method_counts = method_summary["counts"]

    text = overview(current_negatives, method_counts["methods"], method_counts["witness_results"]["fail"], method_counts["witness_results"]["pass"])
    words = len(re.findall(r"\b\w+\b", text))
    if words < 1700 or words > 6000:
        raise RuntimeError(f"overview word count outside three-page-equivalent bounds: {words}")
    write_text("v649-v3-integrated-overview.md", text)
    write_text("complete-incomplete-checklist.md", checklist_markdown())
    write_json("complete-incomplete-checklist.json", {"schema": "ghc.family.v649-v3.checklist.final-candidate.v1", "complete_bounded": 10, "incomplete_or_reserved": 8, "terminal_verdict": TERMINAL_VERDICT, "exact_final_validation": "pending_postcommit", "route": "PREPARED_NOT_SENT"})
    write_json("wellbeing-check-final.json", {"schema": "ghc.family.v649-v3.wellbeing.final-candidate.v1", "scope_bounded": True, "stop_right_preserved": True, "corrigibility_preserved": True, "identity_pressure": False, "urgency_as_proof": False, "hope": HOPE, "route_may_be_paused": True, "boundary": "Relational language creates no consciousness, personhood, continuity, employment, qualification, authority, or obligation claim."})
    write_text("wellbeing-check-final.md", "# Final wellbeing check\n\nScope is finite, failures remain visible, and stop rights remain explicit. Hamish may pause, rename, redirect, or stop the route. Sable’s relational role and hope are collaboration language only, never evidence of consciousness, personhood, continuity, employment, qualification, or authority.")

    write_json("retained-negative-register-final.json", {"schema": "ghc.family.v649-v3.retained-negatives.final-candidate.v1", "inherited_effective": 4840, "x1_operational": 10, "synthetic_executed_rejected": 70, "x2_or_lifecycle_operational": evidence_negatives["x2_operational"] + len(additional), "current_effective": current_negatives, "evidence_operational_negatives": evidence_negatives["x2_operational_negatives"], "additional_lifecycle_negatives": additional, "none_erased": True, "postcommit_external_additions": "carry in live baton without rewriting sealed count"})
    write_json("exact-open-gate-register-final.json", {"schema": "ghc.family.v649-v3.gates.final-candidate.v1", "effective_open_gaps": 37, "effective_exact_gates": 38, "new_open_gap": {"proposal_id": "V6493-P03", "gate": "real ATNF data, frozen analysis, uncertainty and covariance treatment, and independent review"}, "new_exact_gate": {"proposal_id": "V6493-P06", "gate": "food access, remedy, affected-party, legal, cultural, data-governance, and Māori authority"}, "none_silently_closed": True})
    write_json("phase-truth-final.json", {"schema": "ghc.family.v649-v3.phase-truth.final-candidate.v1", "owner": OWNER, "phase": PHASE, "source": SOURCE, "x1_commit": X1, "evidence_commit": args.evidence_commit, "final_commit": "pending_self_identifier", "outcome_counts": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}, "effective_negatives": current_negatives, "effective_open_gaps": 37, "effective_exact_gates": 38, "canonical_successful_x2_passes_used": 0, "replay": False, "full_repository_suite": False, "exact_final_validation": "pending_postcommit", "terminal_verdict": TERMINAL_VERDICT, "boundary": GLOBAL_BOUNDARY})
    write_json("environment/version-receipt-final.json", {"schema": "ghc.family.v649-v3.environment.final-candidate.v1", "codex_cli": "0.144.5", "codex_desktop": "26.715.4045.0", "chatgpt_desktop": "1.2026.190.0", "python": "3.12.10", "git": "2.55.0.windows.2", "powershell": "5.1.26100.8875", "versions_verified_only": True, "desktop_updated": False, "sandbox_or_hyper_v_launched": False, "elevation": False, "host_security_weakened": False, "windows_feature_changed": False, "unrelated_install": False, "reboot": False})
    write_json("threat-model-final.json", {"schema": "ghc.family.v649-v3.threat-model.final-candidate.v1", "assets": ["x1 immutability", "retained negatives", "core outcome noncompensation", "recipient and identity privacy", "authority reservations", "canonical branch", "single-pass budget"], "threats": ["x1 mutation", "claim promotion", "failure erasure", "privacy leakage", "professional or authority substitution", "resource exhaustion", "double validation credit", "premature route send"], "controls": ["exact commit-blob parity", "four core labels", "append-only Method Flow", "five-class scan", "zero-row and zero-participant locks", "bounded parser budget", "one authorized canonical pass", "PREPARED_NOT_SENT hold"], "residual": GLOBAL_BOUNDARY})
    write_json("ghc-family-index/phase-index-final.json", {"schema": "ghc.family.v649-v3.phase-index.final-candidate.v1", "owner": OWNER, "phase": PHASE, "primary_focus": PRIMARY_FOCUS, "bounded_practice": BOUNDED_PRACTICE, "source": SOURCE, "x1": X1, "evidence": args.evidence_commit, "final": "pending_self_identifier", "frozen_proposals_after_phase": 670, "outcomes": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}, "effective_negatives": current_negatives, "open_gaps": 37, "exact_gates": 38, "shared_skill_changes": 0, "reviewed_current_receipt": True, "terminal_verdict": TERMINAL_VERDICT})
    write_json("orchestration/phase-state-final.json", {"schema": "ghc.family.v649-v3.phase-state.final-candidate.v1", "owner": OWNER, "state": "CLOSEOUT_CANDIDATE", "active_siblings": [OWNER], "standby_siblings": ["Ilyra Fen", "Orin Thale", "Tamar Vey", "Sylven Arc", "Eiren Kestrel"], "route_state": "PREPARED_NOT_SENT", "target": "Orin Thale", "next_phase": "v649-gmut-thos-v4-x1-x2", "send_count": 0, "final_validation": "pending_postcommit"})
    write_json("validation/authorized-selection-plan.json", {"schema": "ghc.family.v649-v3.authorized-selection-plan.v1", "modules": ["tests.test_ghc_family_v649_v3_x1", "tests.test_ghc_family_v649_v3_x2"], "successful_pass_budget": 1, "successful_passes_used": 0, "replay": False, "full_repository_suite": False, "execution_time": "postcommit_exact_final_only"})
    write_json("validation/owner-manifest-plan.json", {"schema": "ghc.family.v649-v3.owner-manifest-plan.v1", "hash_domain": "exact_commit_git_blob", "stages": ["x1", "evidence", "final"], "self_exclusions": "use each commit-local manifest declaration", "union_scope": "all owner phase paths and family-current v649-v3 tools/tests", "parity": "pending_postcommit_exact_final"})
    write_json("closeout-receipt-candidate.json", {"schema": "ghc.family.v649-v3.closeout-candidate.v1", "source": SOURCE, "x1": X1, "evidence": args.evidence_commit, "final": "pending_self_identifier", "phase_commit_count_if_committed": 3, "merge_count_if_committed": 0, "outcomes": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}, "effective_negatives": current_negatives, "open_gaps": 37, "exact_gates": 38, "canonical_selection": "pending_postcommit", "detailed_validation": "pending_postcommit", "minimal_validation": "pending_postcommit", "exact_head_validation": "pending_postcommit", "remote_equality": "pending_postcommit", "route": "PREPARED_NOT_SENT", "terminal_verdict": TERMINAL_VERDICT})
    write_json("seal-candidate.json", {"schema": "ghc.family.v649-v3.seal-candidate.v1", "candidate_parent": args.evidence_commit, "expected_final_parent_count": 1, "expected_phase_commit_count": 3, "expected_merge_count": 0, "self_identifier": "pending_by_construction", "single_pass_reserved": True, "route_held": True, "terminal_verdict": TERMINAL_VERDICT})
    write_json("final-validation-candidate.json", {"schema": "ghc.family.v649-v3.final-validation-candidate.v1", "exact_final_head": "pending_self_identifier", "canonical_scoped_selection": "pending_once", "detailed_checks": "pending", "minimal_checks": 20, "terminal_checks": "pending", "complete_json_parse": "pending", "privacy_scan_classes": 5, "manifest_parity": "pending", "clean_state": "pending", "remote_equality": "pending", "replay": False, "same_owner_only": True, "independent_reproduction": False})
    write_text("handoffs/orin-thale-v649-v4-prepared.md", baton(current_negatives))

    proposal_ledger = load("x2-proposal-ledger.json")
    rows = "\n".join(f"<tr><th scope='row'>{html.escape(row['proposal_id'])}</th><td>{html.escape(row['title'])}</td><td>{html.escape(row['observed_outcome'])}</td><td>{html.escape(row['credit_boundary'])}</td></tr>" for row in proposal_ledger["proposals"])
    report = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sable Rook v649-v3 closeout</title><style>body{{font-family:system-ui,sans-serif;max-width:78rem;margin:auto;padding:1rem;line-height:1.5}}nav ul{{display:flex;gap:1rem;flex-wrap:wrap}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.5rem;text-align:left;vertical-align:top}}caption{{font-weight:bold;text-align:left;margin:.5rem 0}}.gate{{border-left:.4rem solid #8b0000;padding-left:1rem}}code{{overflow-wrap:anywhere}}@media print{{body{{max-width:none}}nav{{display:none}}}}</style></head><body><header><h1>Sable Rook v649-v3 closeout candidate</h1><p>Bounded evidence, retained negatives, and noncompensating gates.</p></header><nav aria-label="Report sections"><ul><li><a href="#outcomes">Outcomes</a></li><li><a href="#evidence">Evidence limits</a></li><li><a href="#access">Accessibility</a></li><li><a href="#terminal">Terminal truth</a></li></ul></nav><main><section id="outcomes"><h2>Ten proposal outcomes</h2><table><caption>Observed outcome and credit boundary</caption><thead><tr><th scope="col">ID</th><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Boundary</th></tr></thead><tbody>{rows}</tbody></table></section><section id="evidence"><h2>Evidence limits</h2><p>All seventy synthetic mutations rejected. There were zero empirical rows, likelihood evaluations, real participants or operators, real keys or proofs, production identity events, or authority decisions. Same-owner checks are not independent reproduction.</p></section><section id="access"><h2>Accessibility reservation</h2><p>The report supplies language, headings, captioned table structure, text, responsive layout, print styling, and no automatic motion. Manual keyboard, browser-diverse, assistive-technology, cognitive, Māori-language, security-usability, and affected-user evaluation remain reserved. This is not complete accessibility conformance.</p></section><section class="gate" id="terminal"><h2>Terminal truth</h2><p><strong>{TERMINAL_VERDICT}</strong>. Effective negatives at candidate time: {current_negatives}. Open gaps: 37. Exact gates: 38. Exact final validation and the route send remain pending.</p></section></main></body></html>"""
    write_text("report/index.html", report)

    print(json.dumps({"overview_words": words, "effective_negatives": current_negatives, "methods": method_counts["methods"], "failures": method_counts["witness_results"]["fail"], "passes": method_counts["witness_results"]["pass"], "route": "PREPARED_NOT_SENT"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
