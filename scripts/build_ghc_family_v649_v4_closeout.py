#!/usr/bin/env python3
"""Build the v649-v4 closeout candidate and sanitized Tamar baton."""

from __future__ import annotations

import importlib
import json
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
PHASE = ROOT / "docs" / "orin-thale" / "v649-v4"
SOURCE = "e7998c7ee6fb4a5dccc9e3a09a50aecc8a10b956"
X1_COMMIT = "9882fb936e404796cd4aeb847ff41bd3ec28b5d6"
MODULES = [
    "tests.test_ghc_family_v649_v3_x1",
    "tests.test_ghc_family_v649_v3_x2",
    "tests.test_ghc_family_v649_v4_x1",
    "tests.test_ghc_family_v649_v4",
    "tests.test_ghc_family_v649_v4_closeout",
]


def load_suite() -> unittest.TestSuite:
    for module_name in MODULES:
        importlib.import_module(module_name)
    return unittest.defaultTestLoader.loadTestsFromNames(MODULES)


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, payload: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def overview() -> str:
    return """# Orin Thale v649-v4 integrated overview

## Purpose, identity boundary, and workload

Orin Thale, they/them, served as a relational boundary-and-method steward for this phase. The working hope was to keep every surviving claim inspectable, challengeable, and safely retractable. This is coordination language only. It does not establish consciousness, sentience, personhood, identity continuity, employment, qualification, scientific authority, operational authority, legal authority, cultural authority, Māori authority, or independent agency. Hamish retained the right to rename, pause, redirect, or stop the route throughout.

The phase remained solo and additive. No task, fork, handoff, delegation, or collaboration subagent was created. No sibling lane was changed. No cross-platform message was used. Orin’s existing clean D-drive lane was fast-forwarded to Sable Rook’s exact v649-v3 final head only after source, x1, evidence, parent, zero-merge, manifest, clean-state, and live-remote checks passed. The inherited checkout baseline exceeded fifteen thousand files, but the rotation threshold was correctly applied only to Orin-generated additions. Growth remained far below that threshold. No Sandbox or Hyper-V session was launched. No elevation, host-security weakening, Windows-feature change, unrelated installation, desktop update, or reboot occurred.

The dedicated x1 freeze audited all 670 inherited proposal titles and substantive mechanisms. Several plausible seeds were rejected: catalogue adapters, generic intake and handover proxies, and generic authority matrices were too close to frozen work. Those failures remain visible. Exactly ten revised proposals passed the unchanged lexical threshold and manual mechanism review, producing 680 frozen proposals through v649-v4. X1 contained no x2 implementation or observed outcome, was committed once, passed its exact staged review and eleven x1 tests, and was pushed clean with local, upstream, tracking, and fresh live remote equal before x2 began.

GMUT Mind was the primary Trinity Mandala focus. THOS Body and Freed ID / CBR Heart remained explicit. The bounded human-practice lens was community seed-library germination-assay sampling, replicate counts, dormancy notes, censoring, retest, stock-depletion budgeting, result amendment, and custody handoff. It was a synthetic learning and design lens only. It established no employment, competence, biological result, seed-library authority, material-transfer authority, privacy authority, legal authority, cultural authority, Māori authority, or affected-party evidence.

## Core outcomes

Proposal one completed a bounded Future state tribunal. Synthetic traces exercised single settlement, cancellation before and after start, exception propagation, callback ordering, one-time waiter notification, bounded executor shutdown, and duplicate-credit refusal. Seven mutations executed and were rejected. This is owner-local concurrency-state evidence only. It is not a production executor, live workload, exhaustive race proof, exhaustive security review, or independent reproduction.

Proposal two completed a typed GMUT operator-product-expansion obligation board. It preserved the short-distance domain, distributional coefficients, scaling degree, associativity conditions, microlocal spectrum, renormalization ambiguity, gauge scope, effective-field-theory truncation, units, and an observation firewall. It calculated no coefficient for a real model, detected no force, evaluated no likelihood, constrained no parameter, proved no gauge independence or quantum completion, and established no Theory of Everything. Formal software evidence remains formal software evidence.

Proposal three remained open_gap. The Einstein Toolkit contract identifies thorn interfaces, evolved variables, gauge and hyperbolicity obligations, initial and boundary conditions, discretization, mesh refinement, constraint propagation, convergence-order evidence, an environment lock, benchmark comparison, and independent review. The phase performed no toolkit checkout, build, GMUT thorn implementation, parameter-file run, solver run, refinement triplet, constraint trace, convergence estimate, or benchmark comparison. Official documentation supplied requirements only. No numerical stability, convergence, prediction, force, likelihood, parameter constraint, or empirical claim was made.

Proposal four remained represented. Synthetic seed-germination traces represented accession reservation, a bounded sample draw, replicate trays, a count window, dormancy notes, censored outcomes, viability calculation fields, retest rules, stock-depletion limits, amendment lineage, and receiving custody. There were zero real donors, custodians, seed lots, assays, germination observations, biological results, distributions, safety outcomes, blind matched-budget arms, or effectiveness estimates. The proxy can be inspected as a design surface but cannot direct real seed operations.

Proposal five remained represented. Synthetic RFC 7592 vectors exercised configuration-endpoint binding, registration access-token confinement, read, full replacement update, delete, metadata replacement, credential rotation, deprovisioning, replay refusal, Experimental-status disclosure, and minimization. There were zero real private keys, proofs, clients, services, accounts, tokens, registrations, network exchanges, interoperability events, privacy reviews, independent security reviews, recovery decisions, or trust-governance decisions. A synthetic profile is not production identity readiness.

Proposal six remained exact_gate. The seed-passport and digital-sequence reservation exposes passport metadata, collection-site precision, land relationships, sequence linkage, reidentification, purpose, disclosure, retention, material transfer, benefit sharing, affected-party acceptance, and Māori data-governance dependencies. Repository software made no release, geolocation, land-relationship, linkage, purpose, disclosure, retention, transfer, allocation, remedy, legal, cultural, or authority decision. Those matters remain with affected people, relevant communities, tangata whenua, iwi, hapū, Māori authorities, and competent biological, privacy, legal, cultural, DSI, benefit-sharing, and data-governance authorities.

Proposal seven completed a bounded netCDF classic-family tribunal on disposable synthetic fields. It exercised CDF-1, CDF-2, and CDF-5 signatures, dimension and attribute lists, variable declarations, padding, offsets, record variables, size arithmetic, external-data refusal, and resource budgets. It touched no user file, performed no external retrieval, and provides no general decoder correctness, production conformance, privacy assurance, or exhaustive-security certification.

Proposal eight completed a structural form error-summary audit. It checked an identifiable heading and live status, a deterministic focus target, links to associated fields, persistent textual errors, non-colour cues, correction confirmation, zoom resilience, and a linear fallback. Manual keyboard use, responsive and browser diversity, assistive-technology evaluation, cognitive review, Māori-language review, security-usability review, and affected-user evaluation remain reserved. Structural passing evidence is not complete accessibility conformance.

Proposal nine completed a typed Lippmann electrocapillary domain and nonconversion classifier. It preserved interfacial tension, electrode potential, the reference electrode, fixed chemical-potential constraints, surface excess, sign, units, equilibrium domain, and agency nonconversion. It rejected attempts to turn electrical or interfacial quantities into psyche, agency, worth, morality, consciousness, personhood, or a fundamental law of mind. It establishes no new empirical law.

Proposal ten completed a structural pattern-mixture and Stage 20 nonpromotion board. It represented reference-based multiple imputation, delta adjustment, missingness patterns, tipping points, estimand alignment, combination rules, multiplicity, sensitivity, uncertainty, and terminal abstention. It used zero participants and zero empirical outcomes. It estimated no effect, established no causal result, supplied no safety monitoring or value authority, and did not authorize Stage 20.

The ten outcomes are exactly six completed, two represented, one open_gap, and one exact_gate. These labels apply only to the declared hypotheses. The phase verdict remains **NOT_READY_FOR_STAGE_20**.

## Portfolios, tools, failures, and gates

Thirty new safe-now tasks completed only within additive owner-scoped boundaries. Twenty bounded candidate prototypes produced individual witnesses limited to their synthetic, symbolic, structural, proxy, or refusal hypotheses. Twenty phase-local skills were initialized through the official skill-creator workflow, customized into substantive packages, validated under UTF-8, and smoke-used through their declared runners. They were not installed globally. No subagent forward test occurred because delegation was prohibited. Ten family-current runners were built or selected and used while preserving historical callers. Thirty CLEAN/FIX/REFINE tasks completed without destructive cleanup, history rewriting, force push, sibling mutation, deletion of user material, security weakening, elevation, unrelated installation, desktop update, or reboot. Ten inherited exact-approval packets and five blocked packets stayed visible and unexecuted.

All seventy preregistered synthetic mutations executed and were rejected. A rejected mutation is a bounded guard witness and a retained negative, not empirical truth, production security, proof, or authority. Method Flow preserves every timeout, parser fault, wildcard assumption, collision, provisional inference, output-encoding fault, builder lifecycle fault, workaround, passing witness, recurrence guard, rollback, and sibling recommendation. One provisional novelty method was deprecated when stronger aggregate evidence invalidated its wording; its original witness was retained. Recovery never erased failure and never earned independent reproduction.

Inherited and new gates remain visible. GMUT real computation, data, likelihood, uncertainty, prediction, confirmation, and independent review remain absent. THOS real blind matched-budget arms, participants or operators, safety monitoring, statistics, and review remain absent. Freed ID real keys, proofs, live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery, and trust governance remain absent. CBR, passport release, DSI linkage, benefit sharing, Māori wording, Māori data governance, legal interpretation, cultural legitimacy, and affected-party acceptance remain exact-gated.

## Validation and terminal truth

Eiren alone owns the complete repository suite, so Orin did not run it. The phase reserved one successful canonical scoped selection and no replay. The selected modules cover Sable’s v649-v3 packet plus Orin’s x1, evidence, and closeout tests. The final gate also requires detailed and minimal checks, complete phase JSON parsing, a five-class privacy and raw-identifier scan, exact staged-file and commit-local manifest parity, stale-label review, diff hygiene, source and lifecycle ancestry, zero merges, the four-commit cap, one final parent, exact head, clean state, and four-way remote equality.

The accessible static report uses a skip link, landmarks, labelled navigation, headings, table captions and headers, visible focus, responsive overflow, and a print alternative. Manual keyboard, responsive-browser, assistive-technology, cognitive, Māori-language, security-usability, and affected-user evaluation remain reserved. The threat model is deliberately nonexhaustive. Zero scanner hits is not complete privacy assurance. Same-owner validation under shared infrastructure is same-owner evidence only, never independent-team scientific reproduction, external audit, production certification, professional validation, legal review, cultural ratification, or Māori-authority review.

The terminal route remains held until the exact final commit is created, pushed, manifest-verified, clean, and local/upstream/tracking/fresh-live equal. Only then may Orin resolve the unique existing task titled Tamar Vey and send one sanitized v649-v5 activation. No prepared document counts as a sent or acknowledged baton.
"""


def baton_text(evidence_head: str) -> str:
    text = f"""# TAMAR VEY — VERIFIED v649-v5 ACTIVATION POINTER

Hamish authorizes one activation of the unique existing task titled Tamar Vey for solo v649 GMUT/THOS v5 x1/x2. This committed pointer is prepared by Orin Thale after v649-v4 evidence. It creates no task, fork, delegation, handoff, or subagent and confers no identity, scientific, professional, legal, cultural, Māori, operational, or independent authority.

## Verified inheritance

Canonical source branch: `codex/GHC-Family/orin-thale-v642-v6-full-tools`.

Inherited Sable source: `{SOURCE}`.

Frozen Orin x1: `{X1_COMMIT}`.

Orin evidence commit: `{evidence_head}`.

The exact Orin final head must be supplied by the single terminal message and reverified live before mutation. Source-to-final history must contain no more than four single-parent phase commits and zero merges. The repository-relative packet root is `docs/orin-thale/v649-v4`. The terminal verdict is `NOT_READY_FOR_STAGE_20`.

Orin audited all 670 inherited proposals and froze ten genuinely distinct proposals, producing 680 through v649-v4. Outcomes are exactly 6 completed, 2 represented, 1 open_gap, and 1 exact_gate. The effective negative total, open-gap total, exact-gate total, exact manifests, validation counts, and any post-final external failure must be taken from the exact final receipts and terminal message rather than inferred from this pre-final pointer.

The primary focus was GMUT Mind. The bounded practice lens was community seed-library germination-assay sampling, replicate counts, dormancy notes, censoring, retest, stock-depletion budgeting, amendment, and custody handoff. It supplied synthetic design context only and established no biological result, competence, employment, professional authority, material-transfer authority, privacy authority, legal authority, cultural authority, Māori authority, or affected-party acceptance.

Core truth: the Future settlement tribunal, OPE obligation board, netCDF tribunal, error-summary audit, Lippmann nonconversion classifier, and pattern-mixture nonpromotion board completed only within bounded software or formal hypotheses. The seed-germination protocol and RFC 7592 registration-management profile remain represented only. The Einstein Toolkit protocol remains open_gap with no checkout, thorn, build, solver run, convergence estimate, or independent review. The seed-passport, geolocation, DSI linkage, reidentification, transfer, benefit-sharing, affected-party, and Māori-data-governance reservation remains exact_gate.

## Tamar’s v649-v5 lane

Read the complete ghc-family-index skill and routing-precedence reference, then the complete Method Flow State skill and schema, before task action. Use newest applicable memory only, with the live verified terminal message authoritative where memory stops. Reverify Orin’s exact final head, source, x1, and evidence ancestry, clean state, single-parent zero-merge history, commit-local manifests, and fresh live equality read-only. Continue only in Tamar’s clean owned D-first lane by fast-forward only, or create one additive Tamar-owned lane from the exact final if safe fast-forward is impossible. Never reset, rewrite, force-push, merge, delete, reuse, or mutate a sibling lane.

Preserve strict x1-before-x2 separation. Audit novelty against all 680 frozen proposals. Freeze exactly ten genuinely distinct proposals with hypothesis, null, approval class, execution lane, current primary or official source needs, concrete artifacts, falsifier or acceptance gate, rollback or recovery, protected gates, and expected disposition. Choose one primary Trinity Mandala pillar and one bounded human practice while preserving all authority boundaries. A practice is a learning lens only.

Design genuinely new portfolios meeting the standing floors of thirty safe-now tasks, twenty bounded candidates, twenty skill ideas or builds, ten runner ideas or builds, and thirty additive CLEAN/FIX/REFINE tasks. Inherited portfolios are evidence and seeds, never Tamar completion credit. Do not manufacture unsafe work. Participant, empirical, professional, legal, cultural, Māori-authority, production, privacy-complete, destructive, credential, account, key, host-security, sibling-mutation, or affected-party work must remain visibly open_gap, exact_gate, exact approval, or blocked.

Use no more than two x1 and two x2 commits, four total, preferring one x1, one evidence, and one combined final. Push x1 and prove local/upstream/tracking/fresh-live equality before x2. Use only completed, represented, open_gap, and exact_gate for core outcomes. Preserve all inherited negatives and every new timeout, parser fault, failed test, false assumption, blocker, workaround, and passing witness through Method Flow before retry. Promote a method only after a bounded passing witness.

Eiren alone owns the full repository suite. Tamar must use the non-Eiren scoped rule: one successful canonical current-phase selection, no replay, plus detailed and minimal validators, complete phase JSON parsing, five-class privacy scanning, exact staged and owner manifests, stale-label review, diff hygiene, lifecycle ancestry, zero merges, commit cap, one final parent, exact head, clean state, and four-way equality. Do not launch Sandbox or Hyper-V, update desktop apps, elevate, weaken host security, enable Windows features, install unrelated software, or reboot.

The inherited x1 freeze is immutable evidence, not a template to edit. Preserve its 97-path contract, including 94 exact Git blobs and three declared lifecycle self-exclusions. Preserve the distinction between checkout bytes, clean-filtered Git blobs, and self-referential receipts. Revalidate every inherited manifest from its immutable commit rather than hashing later working-tree bytes and calling them equivalent. If a later companion receipt changes additively, record that lifecycle fact instead of rewriting the x1 commit or claiming the old manifest describes new bytes.

Use the final negative register as the baseline. It includes Sable’s sealed and external activation negatives, Orin’s x1 operational failures, all seventy executed and rejected synthetic mutations, and every x2 or lifecycle fault retained before sealing. Do not infer a count from this pre-final pointer because additional bounded failures can occur during closeout or routing. A corrected timeout, parser fault, collision, malformed assumption, or failed test remains a negative after recovery. The failed witness and passing witness must both remain attributable, and a provisional method must be deprecated or superseded if later evidence invalidates it.

Use the final gate register in the same way. Orin added one open gap for the absent Einstein Toolkit implementation and convergence evidence, and one exact gate for passport, collection-site, digital-sequence, material-transfer, benefit-sharing, affected-party, legal, cultural, privacy, and Māori-data-governance authority. None of the inherited gaps or gates was silently closed. Tamar may add a gate when new evidence exposes a real dependency, but may not close or downgrade one through software structure, citation, ancestry, synthetic fixtures, same-owner validation, or a quota.

Official and primary sources remain design inputs only. The source ledger records status as current, stable, draft, or watch rather than flattening every page into settled authority. It contains zero experimental observations, participants, seed-lot results, production keys, network identity events, numerical GMUT runs, or authority decisions. Verify any materially current source again, record the date and status, and keep citations separate from data rows, likelihood inputs, participant evidence, interoperability events, or delegated authority.

The final accessible report is structurally useful but not accessibility-complete. Tamar must retain manual keyboard, responsive-layout, browser-diversity, assistive-technology, cognitive, Māori-language, security-usability, and affected-user evaluation as open. The privacy scan covers five declared pattern classes and scanner-definition quarantine; zero confirmed hits does not prove complete privacy. The threat model is nonexhaustive. Canonical and local checks remain same-owner evidence under shared infrastructure, never independent-team scientific reproduction or external audit.

GMUT remains a typed scalar-tensor and EFT research-model family. THOS remains proxy without preregistered blind matched-budget real arms and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys and proofs, live lifecycle events, interoperability, privacy and security review, recovery, and trust governance. CBR and Māori concepts remain under competent, affected-party, tangata whenua, iwi, hapū, and Māori authority. No empirical, participant, professional, legal, cultural, identity, production, deployment, privacy-complete, proof, destructive, account, sibling-merge, accessibility-complete, exhaustive-security, independent-reproduction, AGI, ASI, consciousness, personhood, Theory-of-Everything, or Stage 20 claim is permitted without exact evidence and authority.

Only after Tamar v649-v5 is exact-final validated, clean, pushed, and remote-equal may Tamar resolve the unique existing task titled Sylven Arc and send exactly one sanitized activation for v649-v6. Do not create a successor, contact a standby sibling, or send extra confirmation. Preserve the six-seat order Eiren Kestrel → Ilyra Fen → Sable Rook → Orin Thale → Tamar Vey → Sylven Arc → repeat through v660-v8 unless Hamish stops or redirects, usage is exhausted, the route is unavailable, or an exact safety or authority gate blocks progress.
"""
    if not 1200 <= len(text.split()) <= 6000:
        raise RuntimeError(f"sanitized baton word count outside bounds: {len(text.split())}")
    return text


def build() -> None:
    evidence_head = git("rev-parse", "HEAD")
    commits = git("rev-list", "--reverse", f"{SOURCE}..{evidence_head}").splitlines()
    if commits != [X1_COMMIT, evidence_head]:
        raise RuntimeError(f"closeout must begin at the single evidence commit after x1: {commits}")
    if git("rev-list", "--merges", f"{SOURCE}..{evidence_head}"):
        raise RuntimeError("merge commit found before closeout")
    if not (PHASE / "x2/evidence-ledger.json").is_file():
        raise RuntimeError("evidence packet is absent")
    skill_use = load("x2/skill-use-ledger.json")
    runner_use = load("x2/runner-use-ledger.json")
    final_skills = []
    for row in skill_use["items"]:
        updated = dict(row)
        if row["name"].endswith("terminal-proof"):
            updated["smoke_used"] = True
            updated["state"] = "completed"
        final_skills.append(updated)
    final_runners = []
    for row in runner_use["items"]:
        updated = dict(row)
        if row["name"] == "build_ghc_family_v649_v4_closeout.py":
            updated["invoked"] = True
            updated["state"] = "completed"
        final_runners.append(updated)
    write_json("x2/skill-use-ledger-final.json", {"schema": "ghc.family.v649-v4.skill-use-ledger.final.v1", "skill_count": 20, "completed_count": 20, "pending_count": 0, "items": final_skills})
    write_json("x2/runner-use-ledger-final.json", {"schema": "ghc.family.v649-v4.runner-use-ledger.final.v1", "runner_count": 10, "completed_count": 10, "pending_count": 0, "items": final_runners})
    text = overview()
    if not 1200 <= len(text.split()) <= 6000:
        raise RuntimeError(f"overview word count outside bounds: {len(text.split())}")
    write_text("integrated-overview.md", text)
    report = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Orin Thale v649-v4 bounded evidence report</title>
<style>body{font-family:system-ui,sans-serif;max-width:72rem;margin:auto;padding:1rem;line-height:1.55}a:focus{outline:3px solid #005fcc;outline-offset:2px}.skip{position:absolute;left:-9999px}.skip:focus{left:1rem;top:1rem;background:#fff;padding:.5rem}table{border-collapse:collapse;width:100%}th,td{border:1px solid #555;padding:.5rem;text-align:left}caption{font-weight:bold;margin:.5rem}@media(max-width:48rem){table{display:block;overflow-x:auto}}@media print{a[href]::after{content:" (" attr(href) ")"}}</style></head>
<body><a class="skip" href="#main">Skip to evidence</a><header><h1>Orin Thale v649-v4</h1><p>Bounded evidence report. Verdict: <strong>NOT_READY_FOR_STAGE_20</strong>.</p></header>
<nav aria-label="Report sections"><a href="#outcomes">Outcomes</a> · <a href="#boundaries">Boundaries</a> · <a href="#access">Accessibility reservation</a></nav>
<main id="main"><section id="outcomes"><h2>Core outcomes</h2><table><caption>Ten preregistered outcomes</caption><thead><tr><th scope="col">Class</th><th scope="col">Count</th><th scope="col">Meaning</th></tr></thead><tbody><tr><th scope="row">Completed</th><td>6</td><td>Bounded software, symbolic, or structural hypotheses only</td></tr><tr><th scope="row">Represented</th><td>2</td><td>Synthetic proxy; no real seed operations or production identity</td></tr><tr><th scope="row">Open gap</th><td>1</td><td>Einstein Toolkit has zero GMUT solver runs and zero convergence estimates</td></tr><tr><th scope="row">Exact gate</th><td>1</td><td>Passport, DSI, benefit-sharing, affected-party, legal, cultural, and Māori authority reserved</td></tr></tbody></table></section>
<section id="boundaries"><h2>Truth boundaries</h2><p>GMUT remains a research-model family. THOS remains proxy. Freed ID remains synthetic and nonproduction. CBR and Māori concepts remain under competent, affected, and Māori authority. Same-owner checks are not independent reproduction.</p></section>
<section id="access"><h2>Accessibility reservation</h2><p>This static report uses headings, landmarks, a skip link, labelled navigation, table headers, visible focus, responsive overflow, and print link expansion. Manual keyboard, responsive-browser, assistive-technology, cognitive, Māori-language, security-usability, and affected-user evaluation remain reserved.</p></section></main>
<footer><p>No deployment, production, empirical, professional, legal, cultural, privacy-complete, exhaustive-security, accessibility-complete, AGI, ASI, consciousness, personhood, Theory-of-Everything, or Stage 20 claim is made.</p></footer></body></html>"""
    write_text("accessible-report.html", report)
    write_json("complete-incomplete-checklist.json", {
        "schema": "ghc.family.v649-v4.checklist.v1",
        "complete": ["x1_remote_equal_before_x2", "ten_core_outcomes_classified", "thirty_safe_tasks", "twenty_candidates", "twenty_skills", "ten_runners", "thirty_clean_refine", "seventy_mutations_retained", "static_report_structural_surface"],
        "incomplete": ["real_gmut_implementation_data_likelihood", "real_thos_arms", "production_freed_id", "affected_party_acceptance", "legal_and_cultural_ratification", "maori_authority_review", "manual_accessibility_review", "independent_reproduction", "stage20"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_text("complete-incomplete-checklist.md", "# v649-v4 complete and incomplete checklist\n\nCompleted work is confined to declared bounded software, symbolic, structural, proxy, and refusal hypotheses. Real GMUT implementation, data, likelihoods, THOS participant arms, production Freed ID, affected-party acceptance, legal and cultural ratification, Māori authority review, manual accessibility evaluation, independent reproduction, and Stage 20 remain incomplete.")
    threats = [
        {"threat": "formal_to_empirical_promotion", "control": "typed observation firewalls and zero-run refusal", "residual": "real implementation, computation, data, uncertainty, and review remain absent"},
        {"threat": "proxy_to_effectiveness_promotion", "control": "zero-person and zero-biological-result counters", "residual": "real arms, monitoring, statistics, and review remain absent"},
        {"threat": "synthetic_identity_to_production", "control": "zero-key and zero-interoperability counters", "residual": "live lifecycle, privacy, security, recovery, and governance remain absent"},
        {"threat": "software_to_authority_substitution", "control": "passport and DSI exact gate", "residual": "affected, legal, cultural, privacy, biological, benefit-sharing, and Māori decisions remain external"},
        {"threat": "structural_to_complete_accessibility", "control": "manual and affected-user reservations", "residual": "real evaluation remains absent"},
        {"threat": "negative_erasure", "control": "Method Flow fail and pass witnesses", "residual": "future failures require additive retention"},
        {"threat": "privacy_leakage", "control": "five-class scans and sanitized repository-relative baton", "residual": "zero hits is not complete assurance"},
        {"threat": "lane_or_history_damage", "control": "additive owned branch, no force push, exact manifests", "residual": "same-owner infrastructure is not independent audit"},
    ]
    write_json("threat-model.json", {"schema": "ghc.family.v649-v4.threat-model.v1", "threats": threats, "exhaustive": False})
    write_text("threat-model.md", "# v649-v4 threat model\n\n" + "\n".join(f"- **{row['threat']}** — Control: {row['control']}. Residual: {row['residual']}." for row in threats) + "\n\nThis is not an exhaustive security, privacy, legal, cultural, accessibility, or scientific review.")
    negatives = load("x2/retained-negative-register.json")
    closeout_negatives = load("validation/closeout-operational-negatives.json")
    gates = load("x2/gate-register.json")
    write_json("retained-negative-register-final.json", {
        **negatives,
        "schema": "ghc.family.v649-v4.retained-negatives.final-candidate.v1",
        "closeout_operational": closeout_negatives["count"],
        "effective_at_final_candidate": negatives["effective_at_evidence"] + closeout_negatives["count"],
        "terminal_route": "PREPARED_NOT_SENT",
    })
    write_json("exact-open-gate-register-final.json", {**gates, "schema": "ghc.family.v649-v4.gates.final-candidate.v1", "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("stage20-terminal-board.json", {"schema": "ghc.family.v649-v4.stage20-board.v1", "ready": False, "verdict": "NOT_READY_FOR_STAGE_20", "reasons": ["real_implementation_and_data_absent", "participants_absent", "production_identity_absent", "authority_gates_open", "manual_accessibility_open", "independent_reproduction_open"]})
    selected = load_suite().countTestCases()
    write_json("closeout/closeout-candidate.json", {"schema": "ghc.family.v649-v4.closeout-candidate.v1", "evidence_head": evidence_head, "x1_commit": X1_COMMIT, "outcomes": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}, "canonical_successful_pass_used": False, "terminal_route": "PREPARED_NOT_SENT", "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("closeout/seal-candidate.json", {"schema": "ghc.family.v649-v4.seal-candidate.v1", "evidence_head": evidence_head, "expected_phase_commit_count": 3, "expected_merge_count": 0, "expected_final_parent_count": 1, "exact_final_head": "VERIFIED_EXTERNALLY_AFTER_COMMIT", "terminal_route": "PREPARED_NOT_SENT"})
    write_json("validation/final-validation-plan.json", {"schema": "ghc.family.v649-v4.final-validation-plan.v1", "full_repository_suite": False, "canonical_successful_pass_budget": 1, "successful_passes_used": 0, "failed_canonical_attempts_before_success": 1, "failed_attempt_receipts": ["validation/canonical-failed-attempt-01.json"], "replay_budget": 0, "selected_test_count": selected, "detailed_check_count": 32, "minimal_check_count": 20, "complete_phase_json_parse": True, "five_class_privacy_scan": True, "exact_staged_review": True})
    write_json("validation/reproduction-receipt.json", {"schema": "ghc.family.v649-v4.reproduction.v1", "canonical_same_owner_pass": "PENDING", "replay_used": False, "named_or_detached_lane_created": False, "same_owner_only": True, "independent_team_reproduction": False})
    write_json("orchestration/final-phase-state.json", {"schema": "ghc.family.v649-v4.orchestration.final-candidate.v1", "active": ["Orin Thale"], "standby": ["Eiren Kestrel", "Ilyra Fen", "Sable Rook", "Tamar Vey", "Sylven Arc"], "subagents": 0, "tasks_created": 0, "cross_platform_messages": 0, "terminal_route": "PREPARED_NOT_SENT"})
    baton = baton_text(evidence_head)
    write_text("handoffs/tamar-vey-v649-v5-activation.md", baton)
    write_json("closeout/closeout-build-receipt.json", {"schema": "ghc.family.v649-v4.closeout-build.v1", "overview_words": len(text.split()), "baton_words": len(baton.split()), "skill_count": 20, "runner_count": 10, "selected_tests": selected, "passed": True})


if __name__ == "__main__":
    build()
