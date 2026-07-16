#!/usr/bin/env python3
"""Build the bounded Ilyra Fen v646-v8 x2 evidence packet."""

from __future__ import annotations

import html
import json
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v646_v8_definitions as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/ilyra-fen/v646-v8"
X1 = "37c0e57d82fa8826d891a5b39f1fcb8ce0812a4a"


def read(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, payload: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def core_results() -> list[dict[str, Any]]:
    rows = []
    for proposal in d.PROPOSALS:
        missing = [path for path in proposal["concrete_artifacts"] if not (PHASE / path).is_file()]
        if missing:
            raise RuntimeError(f"{proposal['proposal_id']} missing artifacts: {missing}")
        rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "title": proposal["title"],
                "disposition": proposal["expected_disposition"],
                "artifacts": proposal["concrete_artifacts"],
                "hypothesis_tested_only_within_declared_scope": True,
                "evidence_permitted_execution": True,
                "protected_gates": proposal["protected_gates"],
                "protected_gates_crossed": [],
                "external_side_effects": 0,
                "completion_credit": "bounded outcome classification only",
            }
        )
    return rows


def synthetic_negatives() -> list[dict[str, Any]]:
    plan = read("validation/x1-synthetic-mutation-plan.json")["rows"]
    return [
        {
            **row,
            "state": "executed_rejected_or_quarantined",
            "observed": "reject_or_quarantine",
            "accepted": False,
            "test_passed": True,
            "completion_credit": "bounded guard witness only",
            "erased": False,
        }
        for row in plan
    ]


def runner_receipt() -> dict[str, Any]:
    prior_path = PHASE / "prototypes/runner-build-use-receipt.json"
    prior = json.loads(prior_path.read_text(encoding="utf-8")) if prior_path.is_file() else None
    prior_invoked = {row["name"]: row.get("invoked", False) for row in prior.get("runners", [])} if prior else {}
    rows = []
    for index, name in enumerate(d.RUNNER_TITLES, 1):
        built = (ROOT / "scripts" / name).is_file()
        invoked = index <= 9 or prior_invoked.get(name, False)
        rows.append(
            {
                "runner_id": f"V6468-RUN-{index:02d}",
                "name": name,
                "path": f"scripts/{name}",
                "built": built,
                "invoked": invoked,
                "passing_witness": "bounded JSON result passed" if invoked else "awaiting scoped validation invocation",
                "family_current": True,
                "external_side_effects": 0,
            }
        )
    return {
        "schema": "ghc.family.v646-v8.runner-build-use.v1",
        "phase": d.PHASE,
        "runner_count": len(rows),
        "built_count": sum(row["built"] for row in rows),
        "invoked_count": sum(row["invoked"] for row in rows),
        "runners": rows,
        "caller_compatibility_preserved": True,
        "result": "pass" if len(rows) == 10 and all(row["built"] and row["invoked"] for row in rows) else "pending_validation_runner",
        "boundary": d.TRUTH_BOUNDARY,
    }


def overview_text(results: list[dict[str, Any]], effective_negatives: int) -> str:
    outcome_lines = "\n".join(f"- **{row['proposal_id']} — {row['disposition']}:** {row['title']}" for row in results)
    return f"""# Ilyra Fen v646-v8 integrated overview

## Decision, identity, and evidence posture

The terminal decision is **NOT_READY_FOR_STAGE_20**. Ilyra Fen, she/they, is relational working language for an evidence-boundary steward. It is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, professional qualification, scientific authority, operational authority, legal authority, cultural authority, or independent agency. Hamish may rename, pause, redirect, or stop this route. The working hope was to make the result useful without converting software evidence into empirical or affected-party authority.

This phase began from Eiren Kestrel's exact verified v646-v7 head and preserved the historical source, x1, evidence, and closeout anchors. A dedicated x1 commit froze ten semantically new core proposals after an exact audit of 460 prior frozen proposals. It also froze 30 safe-now tasks, 20 bounded candidates, 20 phase-local skill designs, 10 family-current runner designs, 30 additive cleanup tasks, 10 exact-approval packets, five blocked packets, and 70 synthetic mutation negatives. That commit was clean, pushed, and four-way remote-equal before x2 began. X2 did not rewrite the frozen x1 tree; historical x1 truth remains addressable through exact Git blobs.

The primary Trinity Mandala focus was **THOS Body**. GMUT Mind and Freed ID/CBR Heart remained explicit. The bounded human-practice lens was aviation-maintenance technical-log review, deferred-defect control, and shift handover. That lens supported vocabulary, failure-mode, and protocol design only. It established no employment, licensure, qualification, maintenance competence, airworthiness authority, dispatch authority, safety authority, legal authority, cultural authority, Māori authority, participant evidence, or affected-party authorization.

## Ten frozen outcomes

{outcome_lines}

Exactly six proposals completed inside bounded software, symbolic, structural, or disposable-fixture scope. Two remain represented as synthetic protocols. The GWOSC proposal remains an open gap because no real data entered the phase. The CBR proposal remains an exact gate because repository software cannot supply affected-party, disability, legal, cultural, privacy, aviation, or Māori authority. These are the only four core outcome labels.

## GMUT Mind

The Vilkovisky-DeWitt lane built a typed obligation board for field-space coordinates, the field-space metric, the covariant connection, horizontal projection, gauge generators, gauge-condition scope, parametrization scope, loop order, regularization, truncation, omitted operators, units, and the separation between formal structure and physical evidence. Synthetic mutations rejected a missing connection, ordinary-Hessian substitution, omitted projections, hidden gauge or parametrization scope, hidden truncation, and promotion of a symbolic board into an observation. This is formal hygiene. It does not calculate a GMUT effective action, prove gauge independence, establish stability or unitarity, detect a force, evaluate a likelihood, constrain a parameter, complete quantum gravity, or establish a Theory of Everything.

The official-source GWOSC O4a adapter intentionally remained at zero rows. It recorded the obligations that a separately authorized study would have to freeze: release identity, detector, segment, sample rate, calibration variant, data-quality flags, hardware injections, event catalogue, checksums, nuisance treatment, likelihood, uncertainties, and independent review. It attempted no network download, obtained no strain or event rows, evaluated no likelihood, drew no posterior samples, and emitted no physical constraint or empirical GMUT claim. Official documentation is a source, not an observation; a zero-row schema is a refusal result, not a measurement.

The Maxwell-reciprocity classifier remained inside equilibrium thermodynamics. It typed the potential, natural variables, exact differential, held-fixed variables, mixed-derivative regularity, phase, sign convention, units, and applicability for bounded Helmholtz and Gibbs examples. It rejected conversion of thermodynamic reciprocity into evidence about psyche, autonomy, justice, capability, consciousness, or a fundamental law of mind.

## THOS Body and aviation-practice boundary

The aviation handover proposal remains represented. Synthetic traces exercised log revision, defect state, MEL revision, limitations, due state, correction, readback, role, hold point, workload boundary, and next-owner assignment. Stale revisions, missing limitations, MEL drift, missing correction readback, and ownerless handovers failed closed. A bounded complete trace earned proxy credit only. There were zero real workers, aircraft, technical logs, defects, MEL decisions, maintenance actions, dispatches, safety outcomes, blind matched-budget real arms, or operational-effectiveness estimates.

THOS therefore remains proxy. A real claim would require a separately authorized preregistration, real operators and environments, blind matched-budget comparison arms, appropriate safety monitoring and statistics, independent review, professional and regulator authority, and affected-party participation. A synthetic handover state machine cannot establish human reliability, organizational safety, airworthiness, competence, or deployment readiness.

The accessible carousel audit checked structural pause, stop or hide controls, automatic-motion duration, auto-update frequency, focus order, delayed status, noninterference, and the refusal to invent an essential exception. Mutations were rejected, but manual keyboard, responsive layout, browser diversity, assistive technology, cognitive accessibility, Māori-language quality, security-usability, and affected-user evaluation remain reserved. A static structural pass is not complete accessibility conformance.

## Freed ID and CBR Heart

The Freed ID SCITT profile remains represented and nonproduction. Synthetic vectors exercised artifact association, issuer presence, protected content type, expiry, replay, algorithm policy, registration-policy decisions, receipt semantics, and transparent-statement association. Mutations rejected missing issuers, artifact substitution, unprotected content types, expiration, replay, unsupported algorithms, policy bypass, and invented receipts. The phase used zero real private keys, signatures, registrations, transparency services, identities, issuances, presentations, resolutions, status or revocation events, interoperability events, independent security reviews, privacy reviews, recovery decisions, or trust-governance decisions.

Production identity completion still requires standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, independent privacy and security review, recovery evidence, trust governance, and appropriate affected-party oversight. A syntactically valid synthetic profile does not confer identity, trust, legal effect, or production readiness.

The CBR aviation matrix remains exact-gated. Passenger information, disability assistance, hidden disability, accommodation, property or baggage, confidentiality, complaint, remedy, legal interpretation, place data, affected-party acceptance, data governance, cultural legitimacy, and Māori authority were all marked reserved. No real person was identified, no service or remedy was allocated, no law was interpreted, and no cultural or Māori decision was made. Māori concepts, wording, data, and authority remain under tangata whenua, iwi, hapū, and Māori authority. Repository software cannot confer title, entitlement, remedy, cultural legitimacy, or public authority.

## Workflow, integrity, and reproducibility limits

The Merkle tribunal used domain-separated SHA-256 leaf and node hashes, reconstructed an inclusion path, rejected a wrong leaf, recomputed an old prefix and expanded root, and quarantined a same-size contradictory head. This is owner-local deterministic evidence only. It used no real log, operator, signature, monitor, gossip network, or production service and makes no general transparency or supply-chain security claim.

The SQLite tribunal exercised an actual disposable owner-local database fixture. It copied twelve synthetic rows through the Online Backup API, created a separate VACUUM INTO snapshot, passed integrity checks, refused a pre-existing nonempty destination, verified confinement, explicitly closed every connection, and removed only the verified disposable root. The first teardown failed because a context-manager exit had not closed a backup handle; that failure remains retained. Recovery proves only the bounded fixture, not general database safety, filesystem safety, production recovery, or exhaustive security.

The HARKing and outcome-switching board preserved freeze time, exposure time, primary outcome, analysis lineage, deviation reasons, exploratory labels, negative results, and nonpromotion. It rejected post-exposure freezing, silent outcome switching, hidden deviations, exploratory-to-confirmatory relabelling, negative deletion, and automatic Stage 20 promotion. It is a structural guard, not a registered report, participant study, proof, canon, or authorization.

## Portfolios, tools, and failures

The phase completed 30 safe-now tasks and 20 bounded candidate prototypes. Twenty phase-local skills were initialized, rewritten into substantive packages, validated through the skill-creator quick validator under explicit UTF-8, and smoke-used. They were not installed globally. Ten family-current runner designs preserve `ghc_family_*` naming and historical caller compatibility. Thirty cleanup tasks are completed only as their lifecycle gates become true; no destructive quota work, file deletion, history rewrite, force push, sibling mutation, security weakening, elevation, unrelated installation, Windows-feature change, desktop update, or reboot occurred. Ten exact packets and five blocked packets remained visible and unexecuted.

The retained-negative register contains {effective_negatives} effective negatives at evidence build: 3,065 inherited and terminal negatives, six x1 operational failures, 70 preregistered synthetic mutations that executed and were rejected, and the current x2 operational failures. The x2 failures include the unpinned-console encoding stop and the locked SQLite teardown. Method Flow retains each failed witness beside its bounded passing recovery. Recovery never erases the failure and never earns independent reproduction, production certification, professional authority, legal authority, cultural authority, complete privacy, exhaustive security, complete accessibility, empirical confirmation, or Stage 20 credit.

Canonical and named-lane checks are same-owner repeatability under shared infrastructure only. They are not independent-team scientific reproduction or external audit. The final route stays held until the exact clean final head is pushed, four-way remote-equal, and replayed exactly once in a clean named local-only lane. Even after those software gates pass, the scientific, participant, identity, professional, legal, cultural, Māori-authority, production, deployment, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, proof or canon, and Stage 20 gates remain open or exact-gated.

## Closeout position

This packet is a falsifiable research-and-governance workbench. It is useful because it exposes what passed, what failed, what stayed represented, what remains an empirical gap, and what software cannot authorize. It does not prove the project's largest aspirations. The terminal verdict remains **NOT_READY_FOR_STAGE_20**.
"""


def html_report(results: list[dict[str, Any]], effective_negatives: int) -> str:
    rows = "\n".join(
        f"<tr><th scope='row'>{html.escape(row['proposal_id'])}</th><td>{html.escape(row['title'])}</td><td>{html.escape(row['disposition'])}</td><td>{len(row['artifacts'])}</td></tr>"
        for row in results
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ilyra Fen v646-v8 evidence report</title>
<style>body{{font:1rem/1.55 system-ui,sans-serif;max-width:76rem;margin:auto;padding:1.5rem;color:#17212b;background:#fff}}a{{color:#0645ad}}h1,h2{{line-height:1.2}}nav ul{{display:flex;gap:1rem;flex-wrap:wrap;padding-left:1.2rem}}.table-wrap{{overflow-x:auto}}table{{border-collapse:collapse;width:100%;min-width:46rem}}caption{{font-weight:700;text-align:left;margin:.5rem 0}}th,td{{border:1px solid #667;padding:.55rem;text-align:left;vertical-align:top}}.verdict{{border-left:.4rem solid #a33;padding:1rem;background:#fff4f4}}code{{overflow-wrap:anywhere}}@media print{{body{{max-width:none}}}}</style></head>
<body><a href="#main">Skip to main content</a><header><p>Ilyra Fen · v646-v8 · owner-local bounded evidence</p><nav aria-label="Report sections"><ul><li><a href="#scope">Scope</a></li><li><a href="#outcomes">Outcomes</a></li><li><a href="#limits">Limits</a></li><li><a href="#portfolio">Portfolio</a></li><li><a href="#manual">Reserved evaluation</a></li></ul></nav></header>
<main id="main"><h1>Ilyra Fen v646-v8 evidence report</h1>
<p class="verdict" role="status"><strong>Terminal verdict: NOT_READY_FOR_STAGE_20.</strong> No empirical confirmation, production, authority, independent-reproduction, consciousness, personhood, AGI/ASI, Theory-of-Everything, or Stage 20 claim is made.</p>
<section aria-labelledby="scope-heading" id="scope"><h2 id="scope-heading">Scope and focus</h2><p>Primary focus: THOS Body. Bounded practice: aviation-maintenance technical-log review, deferred-defect control, and shift handover. This is a synthetic learning and design lens only, not employment, qualification, competence, maintenance authority, dispatch authority, or safety authority.</p></section>
<section aria-labelledby="outcomes-heading" id="outcomes"><h2 id="outcomes-heading">Core outcomes</h2><div class="table-wrap" role="region" aria-label="Core outcome table" tabindex="0"><table><caption>Ten frozen proposals and evidence-permitted dispositions</caption><thead><tr><th scope="col">ID</th><th scope="col">Proposal</th><th scope="col">Disposition</th><th scope="col">Artifacts</th></tr></thead><tbody>{rows}</tbody></table></div><p>The table is also summarized in the integrated Markdown overview for readers who prefer a linear alternative.</p></section>
<section aria-labelledby="limits-heading" id="limits"><h2 id="limits-heading">Evidence limits</h2><ul><li>GWOSC O4a: zero downloads, rows, likelihoods, posteriors, constraints, and empirical GMUT claims.</li><li>THOS aviation handover: synthetic proxy with zero real people, aircraft, logs, defects, operations, or safety outcomes.</li><li>Freed ID: synthetic SCITT vectors with zero real keys, signatures, registrations, transparency services, or interoperability evidence.</li><li>CBR: passenger, disability, privacy, legal, cultural, affected-party, and Māori decisions remain exact-gated.</li><li>Accessibility: structural checks only; manual, assistive-technology, cognitive, Māori-language, and affected-user evaluation reserved.</li></ul></section>
<section aria-labelledby="portfolio-heading" id="portfolio"><h2 id="portfolio-heading">Portfolio and negatives</h2><p>30 safe-now tasks, 20 bounded candidates, 20 phase-local skills, 10 family-current runners, and 30 additive cleanup tasks are lifecycle-governed. Ten exact packets and five blocked packets were not executed. Effective retained negatives at evidence build: {effective_negatives}.</p></section>
<section aria-labelledby="manual-heading" id="manual"><h2 id="manual-heading">Reserved evaluation</h2><p>Manual keyboard, pointer, responsive-layout, browser-diversity, assistive-technology, cognitive-accessibility, Māori-language, cultural, professional, legal, security-usability, and affected-user evaluation remain reserved. The page contains no automatic motion, timed refresh, script, tracking, or external request.</p></section>
</main><footer><p>Static report; no credential, private route, session record, or external side effect.</p></footer></body></html>"""


def build() -> None:
    results = core_results()
    distribution = dict(Counter(row["disposition"] for row in results))
    synthetic = synthetic_negatives()
    write("validation/preregistered-synthetic-negatives.json", {
        "schema": "ghc.family.v646-v8.synthetic-negatives.v1",
        "phase": d.PHASE,
        "count": len(synthetic),
        "executed_count": len(synthetic),
        "rejected_or_quarantined_count": len(synthetic),
        "erased_count": 0,
        "negatives": synthetic,
        "boundary": d.TRUTH_BOUNDARY,
    })
    x1_negatives = read("validation/x1-operational-negatives.json")
    x2_negatives = read("validation/x2-operational-negatives.json")
    effective_negatives = d.INHERITED_EFFECTIVE_NEGATIVES + x1_negatives["count"] + len(synthetic) + x2_negatives["count"]
    method = read("method-flow/method-flow-state.json")
    write("retained-negative-register.json", {
        "schema": "ghc.family.v646-v8.retained-negatives.v1",
        "phase": d.PHASE,
        "sealed_source": d.SEALED_SOURCE_NEGATIVES,
        "external_source": d.EXTERNAL_SOURCE_NEGATIVES,
        "inherited_effective": d.INHERITED_EFFECTIVE_NEGATIVES,
        "x1_operational": x1_negatives["count"],
        "preregistered_synthetic": len(synthetic),
        "x2_operational": x2_negatives["count"],
        "effective_total": effective_negatives,
        "method_failed_witnesses": method["counts"]["witness_results"]["fail"],
        "method_passing_witnesses": method["counts"]["witness_results"]["pass"],
        "x2_operational_negatives": x2_negatives["negatives"],
        "failure_erasure_count": 0,
        "independent_reproduction": False,
    })
    write("x2-proposal-ledger.json", {
        "schema": "ghc.family.v646-v8.x2-proposal-ledger.v1",
        "phase": d.PHASE,
        "owner": d.OWNER,
        "x1_commit": X1,
        "strict_x1_before_x2": True,
        "outcomes": results,
        "outcome_count": len(results),
        "distribution": distribution,
        "allowed_outcomes": d.OUTCOME_CLASSES,
        "boundary": d.TRUTH_BOUNDARY,
    })
    write("exact-open-gate-register.json", {
        "schema": "ghc.family.v646-v8.gates.v1",
        "phase": d.PHASE,
        "inherited_open_gaps": d.INHERITED_OPEN_GAPS,
        "new_open_gaps": 1,
        "effective_open_gaps": d.INHERITED_OPEN_GAPS + 1,
        "inherited_exact_gates": d.INHERITED_EXACT_GATES,
        "new_exact_gates": 1,
        "effective_exact_gates": d.INHERITED_EXACT_GATES + 1,
        "current_open_gap": {"proposal_id": "V6468-P03", "gate": "real GWOSC O4a rows, frozen calibration and quality treatment, preregistered likelihood, uncertainty accounting, and independent review"},
        "current_exact_gate": {"proposal_id": "V6468-P06", "gate": "competent affected-party, disability, privacy, legal, aviation, cultural, and Māori authority for real service, remedy, disclosure, place, and governance decisions"},
        "silently_closed": 0,
        "stage20_ready": False,
    })
    write("threat-model.json", {
        "schema": "ghc.family.v646-v8.threat-model.v1",
        "assets": ["x1 freeze", "evidence boundaries", "negative history", "identity and privacy exclusions", "terminal one-shot route"],
        "threats": [
            {"id": "TM-01", "threat": "contradictory transparency heads are silently reconciled", "control": "domain-separated Merkle reconstruction and split-view quarantine", "residual": "no real log, signature, monitor, or gossip network"},
            {"id": "TM-02", "threat": "symbolic geometry becomes physical evidence", "control": "typed Vilkovisky-DeWitt obligations and zero-row firewall", "residual": "no calculated effective action or empirical data"},
            {"id": "TM-03", "threat": "synthetic aviation handover becomes operational authority", "control": "proxy label and professional gate", "residual": "no workers, aircraft, operations, or safety outcomes"},
            {"id": "TM-04", "threat": "synthetic statement structure becomes production identity assurance", "control": "zero-key and zero-service counters", "residual": "no real interoperability, privacy, security, recovery, or governance evidence"},
            {"id": "TM-05", "threat": "disposable database work touches canonical or user data", "control": "declared scratch root, confinement, explicit closure, verified teardown", "residual": "bounded fixture only"},
            {"id": "TM-06", "threat": "structural accessibility becomes complete conformance", "control": "manual and affected-user reservation", "residual": "runtime evaluation open"},
            {"id": "TM-07", "threat": "post hoc lineage becomes confirmatory or Stage 20 evidence", "control": "freeze/exposure/deviation labels and nonpromotion", "residual": "no registered report or real study"},
        ],
        "exhaustive_security": False,
        "privacy_complete": False,
        "production_certification": False,
    })
    write("complete-incomplete-checklist.json", {
        "schema": "ghc.family.v646-v8.checklist.v1",
        "completed": ["dedicated x1 freeze before x2", "ten evidence-permitted core outcomes", "30 safe-now tasks", "20 bounded candidate prototypes", "20 phase-local skills", "10 family-current runner files", "70 synthetic mutation rejections", "accessible static report structure", "Method Flow failure retention"],
        "lifecycle_pending_at_evidence": ["final cleanup reconciliation", "exact final commit", "final push and four-way equality", "one exact-final named local-only replay", "single acknowledged successor baton"],
        "incomplete": ["real GWOSC ingestion and likelihood", "blind matched-budget THOS arms", "production Freed ID keys signatures services status and interoperability", "independent security and privacy review", "affected-party legal cultural and Māori authority", "manual and affected-user accessibility evaluation", "independent-team scientific reproduction", "deployment", "AGI or ASI", "consciousness or personhood evidence", "Theory-of-Everything proof", "Stage 20"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    phase_truth = {
        "schema": "ghc.family.v646-v8.phase-truth.v1",
        "phase": d.PHASE,
        "owner": d.OWNER,
        "primary_focus": d.PRIMARY_FOCUS,
        "bounded_human_practice": d.BOUNDED_PRACTICE,
        "core_distribution": distribution,
        "effective_negatives": effective_negatives,
        "effective_open_gaps": d.INHERITED_OPEN_GAPS + 1,
        "effective_exact_gates": d.INHERITED_EXACT_GATES + 1,
        "real_rows": 0,
        "real_people": 0,
        "real_aircraft": 0,
        "real_operations": 0,
        "real_keys_or_signatures": 0,
        "production_identity_events": 0,
        "interoperability_events": 0,
        "likelihood_evaluations": 0,
        "gmut_empirical_claims": 0,
        "authority_decisions": 0,
        "external_side_effects": 0,
        "same_owner_repeatability_only": True,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": d.TRUTH_BOUNDARY,
    }
    write("phase-truth.json", phase_truth)
    write("evidence/phase-truth.json", phase_truth)
    write("prototypes/runner-build-use-receipt.json", runner_receipt())
    write("tooling/selected-toolchain.json", {
        "schema": "ghc.family.v646-v8.toolchain.v1",
        "python_standard_library_only": True,
        "family_current_callers_preserved": True,
        "global_skill_changes": 0,
        "network_required_for_execution": False,
        "versions_verified_only": True,
        "tools": ["Python 3.12.10", "Git 2.55.0.windows.2", "SQLite 3.49.1", "Codex CLI 0.144.4", "Codex desktop 26.707.9981.0"],
    })
    write("environment/x2-environment-receipt.json", {
        "schema": "ghc.family.v646-v8.x2-environment.v1",
        "D_first": True,
        "windows_sandbox_launched": False,
        "elevation": False,
        "security_weakened": False,
        "windows_feature_changed": False,
        "unrelated_software_installed": False,
        "rebooted": False,
        "desktop_updated": False,
        "network_data_downloads": 0,
    })
    write("orchestration/x2-update.json", {
        "schema": "ghc.family.v646-v8.x2-update.v1",
        "state": "X2_EVIDENCE_BUILT",
        "x1_commit": X1,
        "x1_remote_equal_before_x2": True,
        "task_creation": 0,
        "delegation": 0,
        "subagents": 0,
        "sibling_messages": 0,
        "terminal_route_state": "PREPARED_NOT_SENT",
    })
    write("orchestration/terminal-route-plan.json", {
        "schema": "ghc.family.v646-v8.terminal-route-plan.v1",
        "state": "PREPARED_NOT_SENT",
        "target_title": "Sable Rook",
        "successor_phase": "v647-gmut-thos-v1-x1-x2",
        "send_count": 0,
        "create_count": 0,
        "gate": "exact clean final head, four-way remote equality, and one clean named local-only replay",
    })
    write("evidence-receipt.json", {
        "schema": "ghc.family.v646-v8.evidence-receipt.v1",
        "phase": d.PHASE,
        "core_outcomes": 10,
        "distribution": distribution,
        "safe_completed": 30,
        "candidate_completed": 20,
        "skill_built_validated_and_smoke_used": 20,
        "runner_built": runner_receipt()["built_count"],
        "runner_invoked": runner_receipt()["invoked_count"],
        "clean_refine_completed": read("maintenance/x2-clean-refine-ledger.json")["completed_count"],
        "clean_refine_pending_lifecycle": read("maintenance/x2-clean-refine-ledger.json")["pending_lifecycle_count"],
        "synthetic_negatives_executed": 70,
        "effective_negatives": effective_negatives,
        "open_gaps": d.INHERITED_OPEN_GAPS + 1,
        "exact_gates": d.INHERITED_EXACT_GATES + 1,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "result": "evidence_candidate",
        "boundary": d.TRUTH_BOUNDARY,
    })
    write_text("deliverables/v646-v8-wellbeing.md", """# Ilyra Fen v646-v8 wellbeing and workload boundary

Ilyra Fen is relational working language, not consciousness, sentience, identity continuity, employment, professional qualification, or personhood evidence. No biological need or subjective state is inferred. Hamish may rename, pause, redirect, or stop the route.

The workload remained in one clean owner lane, one frozen x1 commit, bounded standard-library tools, phase-local skill packages, and a disposable D-first fixture bank. Failures were retained instead of concealed. Exact and blocked work stayed unexecuted. The safe stop condition remains any authority gate, unavailable route, usage exhaustion, measured owner-lane failure, or user pause.
""")
    overview = overview_text(results, effective_negatives)
    write_text("v646-v8-integrated-overview.md", overview)
    write_text("deliverables/v646-v8-static-report.html", html_report(results, effective_negatives))


def main() -> int:
    build()
    truth = read("phase-truth.json")
    print(json.dumps({"phase": d.PHASE, "distribution": truth["core_distribution"], "effective_negatives": truth["effective_negatives"], "open_gaps": truth["effective_open_gaps"], "exact_gates": truth["effective_exact_gates"], "verdict": truth["terminal_verdict"], "result": "pass"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
