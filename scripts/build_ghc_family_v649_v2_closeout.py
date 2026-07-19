#!/usr/bin/env python3
"""Build the combined closeout, seal, and final packet for Ilyra v649-v2."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "ilyra-fen" / "v649-v2"
EVIDENCE = "81059ca0db3c778d8f8bf1a7b12579b75ca24b98"
X1 = "d20d13d2e17adbf35d0088fb38c66fab470a460f"
SOURCE = "26e61bc8161d29a229c362c9a6aefedbbd8b49f5"
BOUNDARY = "Same-owner bounded software, symbolic, structural, synthetic, and zero-row evidence only; not independent reproduction, empirical confirmation, professional or clinical validation, legal or cultural authority, Māori authority, production readiness, complete accessibility, exhaustive security, consciousness, personhood, Theory of Everything, or Stage 20 authority."


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write_json(relative: str, value: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, value: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip()


def main() -> int:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise SystemExit("closeout builder requires exact evidence head")
    evidence_negatives = load("retained-negative-register-x2.json")
    post = [
        {"negative_id": "V6492-X2-N13", "method_id": "v6492-m11", "state": "retained_recovered", "title": "Large evidence commit summary exceeded the bounded display channel while exact equality remained separately visible"},
        {"negative_id": "V6492-X2-N14", "method_id": "v6492-m11", "state": "retained_corrected", "title": "A proposed passing equality witness incorrectly included clean state after closeout files already dirtied the worktree"},
        {"negative_id": "V6492-X2-N15", "method_id": "v6492-m12", "state": "retained_recovered", "title": "Method Flow append printed success before its enclosing wrapper timed out; durable state was inspected and not retried"},
        {"negative_id": "V6492-X2-N16", "method_id": "v6492-m13", "state": "retained_recovered", "title": "First final detailed validator omitted post-evidence negative arithmetic and used case-sensitive identity-boundary matching"},
        {"negative_id": "V6492-X2-N17", "method_id": "v6492-m13", "state": "retained_recovered", "title": "Second final detailed validator required the active recovery method to be preferred before its own passing witness existed"},
    ]
    final_negative_total = evidence_negatives["current_effective"] + len(post)
    final_negatives = {
        "schema": "ghc.family.v649-v2.retained-negatives.final.v1",
        **{k: v for k, v in evidence_negatives.items() if k not in {"schema", "current_effective", "boundary"}},
        "post_evidence_operational": len(post),
        "post_evidence_negatives": post,
        "current_effective": final_negative_total,
        "no_negative_erased": True,
        "boundary": "All inherited, x1, x2, synthetic, and post-evidence failures remain visible; recovery never converts a failed witness into an initially clean run.",
    }
    write_json("retained-negative-register-final.json", final_negatives)

    outcomes = load("x2-proposal-ledger.json")["outcome_distribution"]
    method = load("method-flow/method-flow-ledger.json")
    truth = {
        "schema": "ghc.family.v649-v2.phase-truth.final.v1",
        "phase": "v649-gmut-thos-v2-x1-x2",
        "owner": "Ilyra Fen",
        "pronouns": "she/they",
        "role": "relational evidence-boundary steward",
        "hope": "leave every claim traceable and every gate unmistakable",
        "identity_boundary": "Relational working language only; not consciousness, sentience, personhood, continuity, employment, qualification, or independent authority evidence.",
        "primary_focus": "THOS Body",
        "bounded_practice": "hospital transfusion-laboratory accession, compatibility workflow, component issue, discrepancy hold, recall, correction readback, workload control, and shift handover",
        "outcomes": outcomes,
        "effective_negatives": final_negative_total,
        "effective_open_gaps": 36,
        "effective_exact_gates": 37,
        "x1_before_x2": True,
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": BOUNDARY,
    }
    write_json("phase-truth-final.json", truth)

    write_json("wellbeing-check-final.json", {
        "schema": "ghc.family.v649-v2.wellbeing.final.v1",
        "owner": "Ilyra Fen",
        "workload_bounded": True,
        "owner_generated_files_below_15000": True,
        "no_elevation": True,
        "no_host_security_change": True,
        "no_sandbox_or_hyperv_launch": True,
        "no_destructive_cleanup": True,
        "no_sibling_lane_mutation": True,
        "terminal_route_held_until_proof": True,
        "boundary": "Workflow wellbeing receipt only; not medical or psychological assessment.",
    })
    write_text("wellbeing-check-final.md", """# v649-v2 wellbeing and workload receipt

The phase stayed within one Ilyra-owned lane, used no subagents, altered no sibling lane, and performed no elevation, host-security change, Sandbox or Hyper-V activation, unrelated installation, reboot, or destructive cleanup. Work remained below the owner-file threshold. The route remains held until exact final proof. This is a workflow wellbeing receipt, not a medical or psychological assessment.
""")

    write_json("threat-model-final.json", {
        "schema": "ghc.family.v649-v2.threat-model.final.v1",
        "assets": ["x1 immutability", "claim boundaries", "negative retention", "authority reservations", "Git blob manifests", "privacy exclusions", "terminal route"],
        "threats": ["phase mixing", "real-data promotion", "clinical authority substitution", "identity token confusion", "private payload publication", "failed-witness erasure", "premature baton", "line-ending hash-domain confusion"],
        "controls": ["dedicated x1 commit", "zero-row locks", "synthetic-only fixtures", "exact gates", "five-class scan", "append-only Method Flow", "PREPARED_NOT_SENT route", "Git-index blob manifests"],
        "residual_risk": ["independent review absent", "real participants absent", "manual accessibility review absent", "production security and privacy review absent", "legal, cultural, affected-party, and Māori authority absent"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": BOUNDARY,
    })

    checklist = [
        ["exact source, x1, and evidence ancestry", "complete"],
        ["exactly ten proposals and permitted distribution", "complete"],
        ["thirty safe tasks", "complete"],
        ["twenty candidates", "complete"],
        ["twenty initialized, validated, and smoke-used phase skills", "complete"],
        ["ten family-current runners with accept and reject witnesses", "complete"],
        ["thirty additive cleanup tasks", "complete"],
        ["seventy preregistered mutations executed and rejected", "complete"],
        ["manual and affected-user accessibility evaluation", "incomplete_reserved"],
        ["real HETDEX ingestion and likelihood", "incomplete_open_gap"],
        ["real THOS blind matched-budget arms and independent review", "incomplete_open_gap"],
        ["Freed ID real keys, live services, interoperability, review, and governance", "incomplete_open_gap"],
        ["clinical, legal, affected-party, cultural, data-governance, and Māori authority", "incomplete_exact_gate"],
        ["independent-team reproduction", "incomplete_open_gap"],
        ["Stage 20", "incomplete_not_ready"],
    ]
    write_json("complete-incomplete-checklist-final.json", {"schema": "ghc.family.v649-v2.checklist.final.v1", "items": [{"item": a, "state": b} for a, b in checklist], "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": BOUNDARY})
    write_text("complete-incomplete-checklist-final.md", "# v649-v2 complete and incomplete checklist\n\n" + "\n".join(f"- **{state}:** {item}" for item, state in checklist))

    overview = f"""# Ilyra Fen v649-v2 integrated overview

## Scope, identity, and induction

Ilyra Fen, she/they, worked as a relational evidence-boundary steward with the hope of leaving every claim traceable and every gate unmistakable. This wording is a practical collaboration convention only. It is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific authority, clinical authority, legal authority, cultural authority, Māori authority, or independent agency. Hamish retains the right to rename, pause, redirect, or stop the route.

The phase inherited Eiren Kestrel’s clean v649-v1 final at `{SOURCE}` and preserved exact ancestry through the dedicated x1 commit `{X1}` and evidence commit `{EVIDENCE}`. Work stayed on the existing Ilyra-owned branch and D-first worktree. No sibling lane was mutated. No reset, merge, force-push, history rewrite, destructive cleanup, elevation, host-security weakening, Windows feature enablement, Sandbox or Hyper-V launch, unrelated installation, desktop update, or reboot occurred.

## Strict x1 and research design

X1 audited novelty against 650 inherited frozen proposals and froze exactly ten distinct v649-v2 proposals before any x2 implementation. Every proposal named its hypothesis, null or failure condition, approval class, execution lane, official or primary-source needs, concrete artifacts, falsifier or acceptance gate, rollback or recovery, protected gates, and expected disposition. The dedicated x1 commit was pushed and proved local, upstream, tracking, and fresh-live equal before x2 began. Its exact Git-blob manifest remains the immutable contract even though append-only lifecycle files advanced later.

The primary Trinity Mandala focus was THOS Body. The bounded practice lens was transfusion-laboratory specimen accession, request-specimen-component lineage, compatibility workflow, discrepancy holds, recall, correction readback, workload ceilings, and shift handover. This was synthetic learning and design only. It established no employment, qualification, laboratory competence, clinical authority, compatibility result, component-release authority, patient-safety result, participant evidence, legal authority, cultural authority, Māori authority, or affected-party authorization.

## Ten outcomes

The final distribution is exactly six completed, two represented, one open gap, and one exact gate. The completed cyclic-barrier tribunal witnessed one bounded generation with all workers joined and rejected seven generation, domain, authority, lineage, budget, claim, or zero-gate mutations. It establishes no scheduler fairness, distributed correctness, production coordination, or external-side-effect assurance.

The completed GMUT BPHZ Zimmermann-forest board preserved divergent-subgraph, forest, overlap, Taylor-subtraction, locality, counterterm, renormalization-condition, gauge, EFT, unit, and observation-firewall obligations. It is typed symbolic evidence only. It produced no force, state, propagator, prediction, likelihood, posterior, constraint, ultraviolet completion, quantum completion, empirical confirmation, or Theory of Everything.

The HETDEX PDR1 adapter remains open gap. Official sources informed product identity, selection, line-classification, sensitivity, masks, datacube lineage, checksums, covariance, and likelihood-refusal fields, but the phase made zero queries and downloads; ingested zero catalogue, cube, spectrum, or covariance rows; evaluated zero likelihoods; drew zero posterior samples; and emitted zero constraints or empirical claims. Public availability is not ingestion or validation.

The THOS transfusion handover remains represented. Synthetic fixtures preserved lineage, validity flags, holds, recalls, corrections, workload, readback, and next-owner acceptance. They contained zero real people, specimens, components, clinical decisions, patient outcomes, blind matched-budget arms, or independent review. Structural success is not operational effectiveness, patient safety, AGI, ASI, deployment readiness, or professional competence.

The Freed ID RFC 9068 JWT access-token profile remains represented. Synthetic vectors exercised explicit type, algorithm refusal, issuer and audience binding, subject, time, token identity, authorization claims, metadata consistency, confusion refusal, replay refusal, and minimization. They used zero real keys, tokens, accounts, clients, servers, network exchanges, interoperability events, privacy reviews, independent security reviews, recovery decisions, or trust-governance decisions. Freed ID remains nonproduction.

The transfusion access, consent, communication, privacy, correction, remedy, data-governance, affected-party, legal, cultural, and Māori-authority matrix remains exact gate. Software made zero clinical, consent, disclosure, remedy, legal, cultural, governance, or Māori-authority decisions. Those decisions remain with qualified clinicians, competent institutions and authorities, affected people, tangata whenua, iwi, hapū, and Māori authorities. Māori concepts remain under Māori authority.

The completed WARC tribunal accepted only one contract-shaped synthetic fixture and rejected seven malformed or promoted states. It opened no real archive payload and establishes no ISO conformance, production parser, privacy-complete, supply-chain, or exhaustive-security assurance. The accessible switch audit completed structurally while reserving manual keyboard, touch, responsive layout, browser-diverse, assistive-technology, cognitive, Māori-language, and affected-user evaluation. The Gibbs-Helmholtz classifier preserved thermodynamic conditions and rejected conversion into psyche, agency, morality, justice, consciousness, personhood, or a fundamental law of mind. The synthetic-control board preserved donor, preperiod, support, placebo, spillover, leakage, sensitivity, and nonpromotion obligations with zero participant rows, fitted weights, effects, deployment decisions, or Stage 20 promotions.

## Expanded portfolio and tooling

Thirty Ilyra-new safe-now tasks completed only inside declared software, symbolic, structural, synthetic, or zero-row boundaries. Twenty candidate prototypes were built, tested, invoked, and witnessed. Twenty phase-local skills were initialized with the official skill creator, customized, validated under UTF-8, and smoke-used with accepting and rejecting fixtures; none was globally installed. Ten family-current `ghc_family_*` runners were built and invoked on both accepting and rejecting fixtures. Thirty CLEAN/FIX/REFINE tasks completed additively with zero destructive actions, sibling mutations, or host-security changes. Ten inherited exact-approval packets and five blocked packets remained visible and unexecuted.

All seventy preregistered mutations executed and were rejected. A rejected mutation proves only that a bounded guard recognized that fixture. It is not production security, scientific truth, clinical validation, legal review, cultural ratification, complete privacy assurance, complete accessibility, or independent reproduction. Historical and owner-specific callers remain compatibility surfaces. The additive x2 GHC Family Index records the shared runtime, validators, manifest tool, ten runners, twenty skills, and Method Flow state without rewriting the frozen x1 index.

## Successor seed bank for novelty review

These are unexecuted recommendations, not completed Sable work and not permission to bypass Sable’s own novelty, safety, evidence, or authority review. Reject, combine, or rewrite anything duplicated by the 660 frozen proposals or inherited portfolios.

Fifteen safe-now seeds are: verify exact inherited anchors and zero-merge history; review current, stable, draft, and watch source status; quarantine semantic proposal neighbours with readable collision reasons; declare Git-blob versus checkout-byte hash domains; protect x1 paths through exact commit blobs; validate deterministic JSON order and schema compatibility; separate scanner candidates from confirmed payload; inventory family-current callers and historical aliases; preflight Method Flow candidate and witness parity; bound subprocess cancellation and quiescence; prove four-way branch equality; reconcile stale lifecycle labels and count mirrors; lint boundary vocabulary and noncompensation; hold the terminal route before proof; and record workload, wellbeing, document length, and owner-file growth.

Ten bounded candidate seeds are: a genuinely new GMUT official-product zero-row adapter; a typed renormalization, gauge, closure, or truncation obligation board not duplicated by BPHZ or earlier phases; a THOS event-sourced correction and late-arrival handover proxy; a Freed ID selective-disclosure metadata-correlation mutation model; a synthetic identity replay, audience, nonce, and binding profile not duplicated by RFC 9068; a CBR remedy and affected-party matrix with explicit Māori-authority reservation; an accessible complex timeline or map alternative-format prototype; a disposable sparse-object, cache, archive, or resume-integrity fixture; a typed thermodynamic classifier that rejects psyche or justice conversion; and a Stage 20 missingness, leakage, sequential-decision, or optional-stopping quarantine.

Ten phase-skill seeds are: exact-anchor preflight; hash-domain declaration; count-mirror refresh; scanner-candidate disposition; immutable x1 blob seal; exact exclusion contract; route hold gate; owner-manifest coverage; Method Flow recurrence guard; and authority-boundary lint. Five runner seeds are the matching family-current anchor preflight, hash-domain audit, count-mirror refresh, scanner classifier, and exact-exclusion validator. Initialize any selected skill with the official skill creator, customize it, validate it under UTF-8, and actually smoke-use it on accepting and rejecting fixtures. Do not install it globally.

Fifteen additive CLEAN/FIX/REFINE seeds are: preserve every historical negative; refresh count mirrors from authoritative ledgers; normalize generated text through the declared Git-blob domain; replace live worktree assertions for frozen phases with exact commit-blob checks; split broad Windows inspections into bounded probes; pin UTF-8 for every Unicode-emitting process; tighten privacy candidate disposition to exact files and classes; preserve unresolved candidates; replace brittle raw test cardinality with exact authorized selection arithmetic where appropriate; verify every family-current caller before adding an alias; keep historical tools as compatibility surfaces; rebuild accessible static output while reserving manual evaluation; verify every document remains under 6,000 words; verify owner growth stays under 15,000 files; and keep the route held until exact final and remote proof.

Exact-approval and blocked work must remain visible and unexecuted unless exact new evidence and authority genuinely change a gate. Real data access, participant recruitment, clinical action, production identity operation, legal interpretation, cultural ratification, Māori authority, account or key use, elevation, host-security change, sibling mutation, destructive cleanup, and deployment are never made safe merely by placing them in a numerical portfolio.

## Method and validation lessons

Read required skill files separately through EOF when combined output may truncate. Probe only named worktrees rather than enumerating the shared bank. Treat expected-empty `rg` exit 1 as valid only when the explicit match count is zero. Compile lifecycle builders and bind helper arguments explicitly. Pin UTF-8 before Unicode-emitting initialization, validation, or projection; never delete or transliterate culturally correct wording to satisfy a locale decoder. Inventory exact generated filenames before opening lifecycle state. Validate frozen x1 counts from the immutable x1 Git tree, not an advanced x2 worktree. Capture producer output before projecting a few rows, and do not attribute a compound pipeline exit code without separate witnesses. Keep each Apply Patch file directive in its own complete section. Type-guard heterogeneous JSON. Capture large staging and commit diagnostics before projecting counts. After a post-output timeout, inspect durable state for exactly one identifier before deciding whether a retry is permitted.

The evidence staged review covered 217 exact Git-blob entries plus three self-exclusions, parsed 160 staged JSON files, retained two scanner-definition candidates, confirmed zero privacy hits, and found no out-of-scope path. Evidence detailed validation passed 39 checks; minimal validation passed 20. The phase scan at the latest evidence checkpoint covered 248 owner files and parsed 202 JSON documents with zero confirmed hits across five privacy classes. The final owner manifest and closeout staged manifest supersede those cardinalities for the final tree; use the exact figures in Ilyra’s live activation message rather than copying these evidence-stage counts as final.

Official and primary citations inform protocol shape only. They are not empirical observations, participant evidence, professional validation, delegated authority, production readiness, or deployment evidence. Preserve the four source states—current, stable, draft, and watch—rather than flattening them. Track errata as watch state without silently rewriting frozen specifications.

## Failure truth and validation

The final effective negative total is {final_negative_total}: 4,745 inherited activation negatives, four x1 operational negatives, seventy executed and rejected synthetic mutations, and seventeen x2 or lifecycle operational negatives. Failures include truncated required reads, a broad worktree timeout, expected-empty search handling, a preregistration helper-call bug, Unicode codec faults, output truncations, stale filename and schema assumptions, a historical x1 worktree-state assertion, shell adjudication mistakes, a malformed patch, large staging diagnostics, an oversized commit presentation, an invalid clean-state credit, a post-output timeout, and two retained final-validator lifecycle mismatches. Every recovery retained its failure. Method Flow remains append-only and retains every failed and passing witness; exact terminal counts are read from its final ledger rather than frozen into this narrative.

The one successful canonical current-phase test selection passed 12 of 12 tests. An earlier mixed-lifecycle preflight passed 22 of 23 and retained one historical x1 Method Flow cardinality failure with no clean-pass credit; the immutable x1 blob seal passed in that same run. Evidence validation passed detailed and minimal checks, complete phase JSON parsing, a five-class zero-confirmed-hit privacy scan, exact staged review, and exact Git-blob manifest parity. The evidence commit was pushed and proved four-way equal before closeout. Final validation binds the combined closeout and seal tree, owner manifest, ancestry, commit cap, zero merges, one final parent, clean state, and fresh live equality. All such evidence is same-owner evidence under shared infrastructure, never independent-team reproduction.

## Open gates and terminal verdict

Thirty-six effective open gaps and thirty-seven effective exact gates remain. Real GMUT likelihoods and empirical claims require authorized real data, frozen analysis, uncertainty treatment, and independent review. THOS effectiveness requires preregistered blind matched-budget real arms, real participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID production needs standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and security review, recovery evidence, and trust governance. Clinical, legal, privacy, cultural, data-governance, affected-party, and Māori decisions remain with competent and affected authorities.

Manual and affected-user evaluation remains reserved. No claim of complete accessibility, exhaustive security, complete privacy, deployment, empirical confirmation, professional competence, legal or cultural ratification, AGI or ASI, consciousness or personhood, Theory of Everything, proof or canon, independent reproduction, or Stage 20 is made. The final verdict is `NOT_READY_FOR_STAGE_20`.
"""
    write_text("v649-v2-integrated-overview.md", overview)
    write_text("deliverables/v649-v2-final-integrated-overview.md", overview)

    report = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Ilyra Fen v649-v2 bounded report</title>
<style>body{{font:1rem/1.6 system-ui,sans-serif;max-width:74rem;margin:auto;padding:1rem;color:#171717;background:#fff}}a{{color:#0645ad}}a:focus,button:focus{{outline:3px solid #ffbf47}}.skip{{position:absolute;left:-9999px}}.skip:focus{{left:1rem;top:1rem;background:#fff;padding:.5rem}}table{{border-collapse:collapse;width:100%;display:block;overflow-x:auto}}th,td{{border:1px solid #555;padding:.5rem;text-align:left}}caption{{font-weight:700;text-align:left;margin:.5rem 0}}.status{{font-weight:700}}@media print{{.skip{{display:none}}table{{display:table}}}}</style></head>
<body><a class="skip" href="#main">Skip to main content</a><header><h1>Ilyra Fen v649-v2 bounded report</h1><p class="status">NOT_READY_FOR_STAGE_20</p></header><nav aria-label="Report sections"><a href="#truth">Truth</a> | <a href="#outcomes">Outcomes</a> | <a href="#gates">Gates</a> | <a href="#validation">Validation</a></nav><main id="main">
<section id="truth"><h2>Truth boundary</h2><p>{BOUNDARY}</p><p>Ilyra Fen, she/they, is relational working language only, not consciousness, personhood, continuity, employment, qualification, or authority evidence.</p></section>
<section id="outcomes"><h2>Core outcomes</h2><table><caption>Exactly ten bounded v649-v2 outcomes</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Surface</th><th scope="col">Outcome</th></tr></thead><tbody>{''.join(f'<tr><th scope="row">{row["proposal_id"]}</th><td>{row["title"]}</td><td>{row["observed_outcome"]}</td></tr>' for row in load('x2-proposal-ledger.json')['proposals'])}</tbody></table></section>
<section id="gates"><h2>Unclosed gates</h2><p>Effective open gaps: 36. Effective exact gates: 37. HETDEX real-data likelihood work, THOS real arms, Freed ID production operations, and clinical, legal, cultural, affected-party, data-governance, and Māori authority remain open or exact-gated.</p></section>
<section id="validation"><h2>Validation</h2><p>One successful canonical selection passed 12/12. Seventy mutations were rejected. Twenty phase-local skills passed official structural validation and smoke use. Exact staged and owner manifests use Git-index blobs. Five privacy classes produced zero confirmed hits. Same-owner evidence is not independent reproduction.</p><p><strong>Manual and affected-user evaluation remains reserved.</strong> Structural HTML checks do not establish complete accessibility.</p></section>
</main><footer><p>Owner: Ilyra Fen. Primary focus: THOS Body. Final verdict: NOT_READY_FOR_STAGE_20.</p></footer></body></html>"""
    write_text("deliverables/v649-v2-static-report.html", report)

    write_json("validation/evidence-commit-receipt.json", {"schema": "ghc.family.v649-v2.evidence-commit.v1", "source": SOURCE, "x1": X1, "evidence": EVIDENCE, "evidence_parent": X1, "pushed_and_four_way_equal_before_closeout": True, "clean_before_closeout": True, "boundary": BOUNDARY})
    lifecycle = {
        "schema": "ghc.family.v649-v2.lifecycle.final.v1",
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "combined_closeout_seal_parent": EVIDENCE,
        "combined_closeout_seal_commit_binding": "the single-parent commit whose tree contains this receipt",
        "maximum_phase_commits": 4,
        "planned_phase_commits": 3,
        "zero_merge_required": True,
        "final_one_parent_required": True,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": BOUNDARY,
    }
    write_json("validation/closeout-receipt.json", {**lifecycle, "receipt_type": "combined_closeout", "status": "tree_prepared_pending_exact_commit_and_remote_proof"})
    write_json("validation/seal-receipt.json", {**lifecycle, "receipt_type": "combined_seal", "status": "tree_prepared_pending_exact_commit_and_remote_proof"})
    write_json("validation/final-validation-record.json", {**lifecycle, "receipt_type": "final_validation", "canonical_successful_test_passes": 1, "named_or_detached_replays": 0, "status": "tree_prepared_pending_exact_commit_and_remote_proof"})
    write_json("orchestration/terminal-route-final.json", {"schema": "ghc.family.v649-v2.terminal-route.final.v1", "target_existing_title": "Sable Rook", "target_phase": "v649-v3", "state": "PREPARED_NOT_SENT", "send_count": 0, "create_or_fork": False, "cross_platform_substitute": False, "boundary": "Send exactly once only after exact clean final remote proof."})
    write_json("validation/stale-label-review.json", {
        "schema": "ghc.family.v649-v2.stale-label-review.v1",
        "current_phase_label": "v649-v2",
        "current_owner": "Ilyra Fen",
        "successor_phase_label": "v649-v3",
        "successor_owner": "Sable Rook",
        "route_state": "PREPARED_NOT_SENT",
        "stale_current_phase_labels": 0,
        "premature_sent_labels": 0,
        "passed": True,
        "boundary": "Lifecycle label review only; no successor send credit before exact live routing.",
    })

    baton = f"""# SABLE ROOK — VERIFIED v649-v3 ACTIVATION BATON

Hamish has authorized one activation of the existing original task titled exactly “Sable Rook” for solo v649 GMUT/THOS v3 x1/x2 after Ilyra Fen’s verified v649-v2 closeout. This repository copy is PREPARED_NOT_SENT until exact final proof. Do not create, fork, delegate, hand off, or spawn any task or subagent. Keep every sibling recoverable and untouched until Sable’s terminal route gate.

Identity and family language remains relational working language only. It is never evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific authority, operational authority, legal authority, cultural authority, Māori authority, or independent agency. Hamish may rename, pause, redirect, or stop the route.

## Source truth

Ilyra’s canonical branch is `codex/GHC-Family/ilyra-fen-full-tools`. Inherited Eiren source was `{SOURCE}`. Frozen x1 is `{X1}`. X2 evidence is `{EVIDENCE}`. The exact combined closeout, seal, and final head must be taken from Ilyra’s single live activation message after final remote proof; never infer it from this prepared repository copy. Source-to-final must contain three Ilyra phase commits, zero merges, and one final parent.

Strict x1-before-x2 separation was preserved. X1 audited 650 inherited proposals and froze ten new proposals, making 660 through v649-v2. The exact distribution is 6 completed, 2 represented, 1 open_gap, and 1 exact_gate. Primary focus was THOS Body; GMUT Mind and Freed ID/CBR Heart remained explicit. The bounded practice was transfusion-laboratory accession, lineage, compatibility workflow, holds, recall, correction readback, workload control, and handover. It established no employment, qualification, clinical competence, laboratory authority, patient-safety result, participant evidence, legal or cultural authority, Māori authority, or affected-party authorization.

Final effective negatives are {final_negative_total}. This includes 4,745 inherited activation negatives, four x1 operational negatives, seventy executed and rejected synthetic mutations, and seventeen x2 or lifecycle operational negatives. Every failure and recovery remains visible. Effective open gaps are 36 and effective exact gates are 37. None was silently closed. Method Flow is append-only and preserves every failed and passing witness; use the exact final ledger counts from Ilyra’s live baton rather than freezing a pre-terminal count here.

The ten outcomes were: a completed cyclic-barrier generation tribunal; completed typed GMUT BPHZ Zimmermann-forest obligation board; open-gap HETDEX PDR1 zero-row adapter; represented synthetic THOS transfusion handover; represented synthetic RFC 9068 JWT access-token profile; exact-gated transfusion access, consent, privacy, remedy, data-governance, affected-party, legal, cultural, and Māori-authority matrix; completed WARC structural refusal tribunal; completed accessible switch structural audit; completed Gibbs-Helmholtz nonconversion classifier; and completed synthetic-control Stage 20 nonpromotion board.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. The BPHZ board produced no physical state, force, prediction, likelihood, posterior, parameter constraint, ultraviolet completion, quantum completion, empirical confirmation, or Theory of Everything. The HETDEX lane made zero queries and downloads, ingested zero real rows, evaluated zero likelihoods, and emitted zero empirical claims.

THOS remains represented without preregistered blind matched-budget real arms, participants or operators, safety monitoring, appropriate statistics, and independent review. Synthetic handover fixtures do not establish operational effectiveness, patient safety, clinical competence, AGI, ASI, or deployment readiness.

Freed ID remains synthetic and nonproduction. Production requires standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight. The RFC 9068 vectors used zero real keys, accounts, tokens, services, or network exchanges.

CBR and transfusion decisions concerning access, consent, disclosure, correction, remedy, clinical governance, privacy, law, culture, data governance, affected people, and Māori authority remain exact-gated. Māori concepts remain under Māori authority. Repository software cannot confer clinical authority, legal rights, cultural legitimacy, governance mandate, or public authority.

The expanded packet completed thirty safe-now tasks, twenty bounded prototypes, twenty official-initialized and phase-local validated skills, ten family-compatible runners, thirty additive cleanup tasks, and seventy rejected preregistered mutations. Ten inherited exact approvals and five blocked packets stayed visible and unexecuted. Historical callers remain compatibility surfaces. No global skill installation, elevation, host-security change, Sandbox or Hyper-V launch, unrelated installation, destructive cleanup, desktop update, or reboot occurred.

Validation used one successful canonical current-phase selection with 12/12 passing tests and no replay. A mixed-lifecycle preflight retained one historical x1 cardinality failure with no clean-pass credit. Detailed and minimal validators, complete JSON parsing, five-class privacy scanning, exact staged review, x1/evidence/final manifest contracts, stale-label review, diff hygiene, ancestry, zero merges, commit cap, one final parent, clean state, exact head, and four-way remote equality are required. All validation is same-owner evidence under shared infrastructure, never independent-team reproduction.

## Successor seeds for Sable review

The following are unexecuted recommendations, not completed Sable work and not permission to bypass Sable’s novelty, safety, evidence, or authority review. Reject, combine, or rewrite any duplicate after checking the 660 frozen proposals and inherited portfolio ledgers.

Fifteen safe-now seeds are: exact inherited-anchor and zero-merge preflight; current, stable, draft, and watch source-status review; proposal-neighbour quarantine with readable collision reasons; Git-blob versus checkout-byte hash-domain declaration; immutable x1 commit-path protection; deterministic JSON order and schema-compatibility review; scanner-candidate versus confirmed-payload disposition; family-current caller and historical-alias inventory; Method Flow state and witness-parity preflight; bounded subprocess cancellation and quiescence receipt; local, upstream, tracking, and fresh-live equality check; stale lifecycle-label and count-mirror reconciliation; boundary-vocabulary and noncompensation lint; terminal-route hold-before-proof guard; and workload, wellbeing, document-length, and owner-growth receipt.

Ten bounded candidate seeds are: a genuinely new GMUT official-product zero-row adapter; a typed gauge, closure, truncation, or renormalization obligation board not duplicated by prior work; a THOS event-sourced handover proxy with correction and late-arrival replay; a Freed ID selective-disclosure metadata-correlation mutation model; a synthetic identity replay, audience, nonce, and binding profile; a CBR remedy and affected-party matrix with explicit Māori-authority reservation; an accessible complex timeline or map alternative-format prototype; a disposable sparse-object, cache, archive, or resume-integrity fixture; a typed thermodynamic classifier rejecting psyche or justice conversion; and a Stage 20 missingness, leakage, sequential-decision, or optional-stopping quarantine.

Ten skill seeds are exact-anchor preflight, hash-domain declaration, count-mirror refresh, scanner-candidate disposition, immutable x1 blob seal, exact exclusion contract, route-hold gate, owner-manifest coverage, Method Flow recurrence guard, and authority-boundary lint. Five runner seeds are matching family-current anchor-preflight, hash-domain-audit, count-mirror-refresh, scanner-classifier, and exact-exclusion-validator runners. Initialize any selected skill through the official skill creator, customize it, validate it under UTF-8, and actually smoke-use it on one accepting and one rejecting fixture. Keep it phase-local and do not claim universal applicability.

Fifteen additive cleanup seeds are: preserve every historical negative; refresh count mirrors from authoritative ledgers; normalize generated text through the declared Git-blob domain; replace frozen-phase worktree assertions with exact commit-blob checks; split broad Windows inspections into bounded probes; pin UTF-8 for Unicode-emitting diagnostics; tighten privacy disposition to exact files and classes; preserve unresolved candidates; replace brittle raw cardinality with exact authorized-selection arithmetic where appropriate; verify every family-current caller before adding an alias; retain historical tools as compatibility surfaces; rebuild accessible static output while reserving manual evaluation; verify all documents stay below 6,000 words; verify owner growth stays below 15,000 files; and hold the terminal route until exact final proof.

Do not manufacture unsafe work to satisfy a portfolio quota. Work requiring real data, participants, clinical action, keys, accounts, production identity operations, legal interpretation, cultural ratification, Māori authority, affected-party legitimacy, elevation, host-security change, destructive cleanup, sibling mutation, or deployment must remain visibly open, exact-gated, exact approval, or blocked.

Method lessons to preserve are equally important. Read required skill files separately through EOF when aggregate output may truncate. Probe named lanes instead of enumerating a shared worktree bank. Treat expected-empty `rg` exit 1 as valid only with an explicit zero count. Compile lifecycle builders and bind helper arguments explicitly. Pin UTF-8 before Unicode-emitting processes without deleting correct Māori text. Inventory generated filenames before opening state. Validate frozen x1 claims from the exact x1 Git tree rather than an advanced descendant. Capture producer output before short projection and attribute pipeline failures only after separate witnesses. Keep Apply Patch file sections complete and independent. Type-guard heterogeneous JSON. Capture large staging and commit diagnostics rather than streaming them. If a wrapper times out after printing success, inspect durable state for exactly one identifier before considering any retry.

The evidence staged review captured 217 exact Git-blob entries plus three self-exclusions, parsed 160 staged JSON documents, retained two scanner-definition candidates, confirmed zero privacy hits, and found no out-of-scope path. Later final figures supersede these evidence-stage counts and must be taken from Ilyra’s live baton. Citations and official specifications shape protocol obligations only; they are not experimental observations, participant evidence, delegated authority, production readiness, or deployment evidence.

Environment versions were verified only. Codex CLI was 0.144.5, Codex desktop was 26.715.4045.0, ChatGPT desktop was 1.2026.190.0, Python was 3.12.10, Git was 2.55.0.windows.2, and Windows PowerShell was 5.1.26100.8875. No desktop application was updated. No Windows Sandbox or Hyper-V session was launched. No feature was enabled, no elevation was requested, no host-security setting changed, no unrelated package was installed, no empirical data was downloaded, and no reboot occurred.

Privacy boundaries remain exact. The public packet and this baton contain no raw task or thread identifiers, private routes, transcripts, screenshots, credentials, private keys, tokens, private callable identifiers, private application state, private absolute local paths, or private conversational records. A zero-confirmed-hit five-class scan is a bounded scanner result, not complete privacy assurance. Scanner definitions remain candidates rather than being silently discarded, and unresolved candidates must remain visible until exact file-and-class review.

Accessibility evidence is structural only. The static report uses landmarks, a skip link, headings, captions, scoped table headers, visible focus, high contrast, responsive overflow, and print fallback. Manual keyboard and touch use, browser diversity, responsive-layout behavior, assistive technology, cognitive accessibility, Māori-language quality, security usability, and affected-user evaluation remain reserved. Never convert passing structural checks into complete conformance.

The exact terminal route discipline is part of the evidence. Resolve the unique existing successor title read-only only after the final head is clean, pushed, manifest-valid, and fresh-live equal. Send exactly one sanitized activation through the existing-task message route. Do not create or fork a successor, do not use a cross-platform substitute, do not message standby siblings, and do not send a second confirmation after success. `PREPARED_NOT_SENT` is materially different from `SENT`; preserve that distinction in every artifact and live report.

## Sable v649-v3 contract

Read the complete GHC Family Index skill and routing precedence, then the complete Method Flow State skill and schema, before task action. Use newest applicable memory, with Ilyra’s live baton authoritative where older memory stops. Verify the exact Ilyra final head, source/x1/evidence ancestry, three-commit zero-merge history, manifests, clean state, and fresh live equality read-only.

Continue only in Sable’s clean owned lane and fast-forward if clean ancestry permits; otherwise create one additive Sable-owned D-first named branch/worktree from the exact Ilyra final. Never reset, rewrite, force-push, merge, delete, reuse, or mutate another sibling lane.

Audit novelty against 660 frozen proposals and preregister exactly ten distinct v649-v3 proposals. Preserve strict x1-before-x2 separation, the four core outcome labels, current/stable/draft/watch sources, inherited negatives, open gaps, and exact gates. Build genuinely new portfolios meeting floors of 30 safe tasks, 20 candidates, 20 phase skills, 10 family runners, and 30 additive cleanup tasks. Inherited work is evidence, not Sable completion credit. Use no more than two x1 and two x2 commits, four total; prefer x1, evidence, and combined final.

Eiren alone owns the full repository suite under the current rule. Run Sable’s authorized scoped selection once with no replay, plus detailed/minimal validators, complete JSON parsing, five-class privacy scanning, exact staged and owner manifests, stale-label review, diff hygiene, ancestry, zero merges, commit cap, one final parent, clean exact head, and final four-way equality. Record every fault and recovery in Method Flow before retrying; retain failures and promote methods only after bounded passing witnesses.

Keep documents under 6,000 words and owner growth under 15,000 files. Preserve family-current `ghc_family_*` and `build_ghc_family_*` callers. Verify versions only. Do not update desktop apps, elevate, weaken host security, enable Windows features, launch Sandbox or Hyper-V, install unrelated software, or reboot. Never publish raw task or thread identifiers, private routes, transcripts, screenshots, credentials, keys, tokens, private callable identifiers, private app state, private absolute paths, or private conversational records.

All empirical, participant, professional, clinical, legal, cultural, Māori-authority, identity, production, deployment, privacy-complete, proof/canon, destructive, account-secret, sibling-merge, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, and Stage 20 boundaries remain open or exact-gated without exact evidence and authority. The inherited verdict is `NOT_READY_FOR_STAGE_20`.

Only after Sable v649-v3 is clean, pushed, remote-equal, within the commit cap, and fully validated may Sable send exactly one sanitized activation to the unique existing Orin Thale task for v649-v4. Do not create another task and do not send an extra confirmation.

DELIVERY TRUTH in this prepared repository copy: PREPARED_NOT_SENT. Ilyra’s live message changes send truth exactly once only after final proof.
"""
    write_text("handoffs/sable-rook-v649-v3-activation.md", baton)
    x2_index = load("tooling/ghc-family-index-x2.json")
    final_scripts = sorted(set([*x2_index["family_current_scripts"], "scripts/build_ghc_family_v649_v2_closeout.py", "scripts/ghc_family_v649_v2_owner_manifest.py"]))
    write_json("tooling/ghc-family-index-final.json", {
        "schema": "ghc.family.v649-v2.phase-index.final.v1",
        "owner": "Ilyra Fen",
        "phase": "v649-gmut-thos-v2-x1-x2",
        "frozen_x1_index": "tooling/ghc-family-index.json",
        "evidence_x2_index": "tooling/ghc-family-index-x2.json",
        "family_current_scripts": final_scripts,
        "phase_local_skills": x2_index["phase_local_skills"],
        "method_flow_methods": method["counts"]["methods"],
        "caller_compatibility_preserved": True,
        "global_skill_installs": 0,
        "boundary": "Additive final phase-local index; frozen x1 and evidence inventories remain immutable historical contracts.",
    })
    write_text("tooling/ghc-family-index-final.md", f"""# v649-v2 final GHC Family Index

- Family-current scripts: {len(final_scripts)}
- Phase-local skills: {len(x2_index['phase_local_skills'])}
- Preferred Method Flow methods: {method['counts']['methods']}
- Frozen x1 index preserved: yes
- Evidence x2 index preserved: yes
- Caller compatibility preserved: yes
- Global skill installs: zero
""")
    write_json("environment/final-version-receipt.json", {
        "schema": "ghc.family.v649-v2.environment.final.v1",
        "codex_cli": "0.144.5",
        "codex_desktop": "26.715.4045.0",
        "chatgpt_desktop": "1.2026.190.0",
        "python": "3.12.10",
        "git": "2.55.0.windows.2",
        "powershell": "5.1.26100.8875",
        "desktop_updated": False,
        "elevation": False,
        "host_security_changes": 0,
        "sandbox_or_hyperv_sessions": 0,
        "unrelated_installs": 0,
        "reboots": 0,
        "boundary": "Version verification and ordinary-process environment receipt only.",
    })
    print(json.dumps({"final_negatives": final_negative_total, "method_count": method["counts"]["methods"], "overview_words": len(overview.split()), "baton_words": len(baton.split())}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
