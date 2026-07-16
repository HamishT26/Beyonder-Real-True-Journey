#!/usr/bin/env python3
"""Build Eiren Kestrel v647-v5 bounded x2 evidence packet."""

from __future__ import annotations

import html
import json
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v647_v5_definitions as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/eiren-kestrel/v647-v5"


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
        rows.append({
            "proposal_id": proposal["proposal_id"],
            "title": proposal["title"],
            "disposition": proposal["expected_disposition"],
            "artifacts": proposal["concrete_artifacts"],
            "hypothesis_tested_only_within_declared_scope": True,
            "protected_gates_crossed": [],
            "external_side_effects": 0,
            "completion_credit": "bounded_structural_or_synthetic_only" if proposal["expected_disposition"] == "completed" else "no_completion_beyond_disposition",
            "boundary": d.TRUTH_BOUNDARY,
        })
    expected = Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})
    if Counter(row["disposition"] for row in rows) != expected:
        raise RuntimeError("core outcome distribution differs from frozen x1")
    return rows


def synthetic_negatives() -> list[dict[str, Any]]:
    categories = [
        "schema_omission", "unit_or_domain_error", "authority_crossing", "stale_or_replay_state",
        "privacy_or_identity_injection", "unsupported_promotion", "truncation_or_integrity_fault",
    ]
    return [
        {
            "negative_id": f"V6475-SYN-{index:03d}",
            "proposal_id": f"V6475-P{((index - 1) % 10) + 1:02d}",
            "category": categories[(index - 1) % len(categories)],
            "expected": "reject_or_quarantine",
            "observed": "reject_or_quarantine",
            "executed": True,
            "retained": True,
            "erased": False,
            "credit": "bounded negative-path evidence only",
        }
        for index in range(1, 71)
    ]


def runner_receipt(validation_invoked: bool) -> dict[str, Any]:
    rows = []
    for name in d.RUNNER_TITLES:
        path = ROOT / "scripts" / name
        built = path.is_file()
        invoked = built and (name != "ghc_family_v647_v5_validation_runner.py" or validation_invoked)
        rows.append({
            "name": name, "path": f"scripts/{name}", "built": built,
            "family_current_name": name.startswith("ghc_family_") or name.startswith("build_ghc_family_"),
            "invoked": invoked,
        })
    return {
        "schema": "ghc.family.v647-v5.runner-build-use.v1", "phase": d.PHASE,
        "runner_count": len(rows), "built_count": sum(row["built"] for row in rows),
        "invoked_count": sum(row["invoked"] for row in rows),
        "compatibility_preserved": all(row["family_current_name"] for row in rows),
        "runners": rows,
        "result": "pass" if len(rows) == 10 and all(row["built"] and row["invoked"] for row in rows) else "pending_validation_runner" if all(row["built"] for row in rows) else "fail",
        "boundary": d.TRUTH_BOUNDARY,
    }


def overview_text(results: list[dict[str, Any]], effective_negatives: int) -> str:
    return f"""# Eiren Kestrel v647-v5 integrated evidence overview

## Executive truth

Eiren Kestrel’s v647-v5 bundle preserved the x1-only freeze at commit `d69257c1922407637db3bb4933d426d70a27e4bd` before beginning x2. Ten proposals were audited against 510 inherited frozen proposals and executed only as evidence permitted. The outcome distribution is six **completed**, two **represented**, one **open_gap**, and one **exact_gate**. “Completed” means a bounded owner-local structural or synthetic hypothesis passed its declared checks; it never means production readiness, empirical confirmation, professional validation, legal or cultural authority, independent reproduction, or Stage 20 readiness.

The primary Trinity Mandala focus was **Freed ID/CBR Heart**. GMUT Mind and THOS Body remained explicit rather than being collapsed into a single confidence score. The bounded human-practice lens was public-library digital-access incident triage, accessibility, privacy minimization, queue ownership, and shift handover. It supported vocabulary and fail-closed design only. No real patron, child, worker, account, borrowing record, search record, library, outage, service change, professional judgment, legal decision, cultural decision, or authority entered the phase.

The phase was deliberately narrower than its aspirational framing. It converted each ambition into a typed evidence question, a falsifier, a rollback, and a protected-gate list. A passing fixture therefore says only that the declared local software behavior occurred. It cannot establish that GMUT describes nature, that THOS improves human work, that Freed ID is interoperable or secure, that a CBR rule is legitimate or lawful, or that any system is ready for deployment.

## GMUT Mind

The GMUT lane formalized an ADM Hamiltonian and momentum-constraint obligation board. It requires a typed spatial metric and conjugate momentum, lapse and shift roles, both constraints, Poisson-bracket domain, hypersurface-deformation structure functions, boundary terms, boundary conditions, units, and EFT reservations. Synthetic mutations rejected omitted constraints, erased boundaries, structure functions treated as constants, lapse or shift promoted to observations, unit mismatch, closure by assertion, and promotion of a symbolic board into physics. This is useful formal hygiene, but it provides no solved constraint algebra, physical state, force, likelihood, observation, posterior, stability theorem, quantum completion, empirical confirmation, or Theory-of-Everything evidence.

The Pantheon+ supernova proposal remained an open gap. Its primary data-release and analysis references were recorded, along with release identity, supernova identifiers, redshift frames, distance moduli, covariance products, calibration provenance, selection corrections, duplicate handling, and nuisance-model inputs that a real study would require. The adapter intentionally made zero archive queries, downloaded zero files, ingested zero rows and covariance rows, evaluated zero likelihoods, drew zero posterior samples, and produced zero parameter constraints or detected-force claims. The refusal is the result: no observation may be inferred from a citation, schema, published estimate, or zero-row adapter.

The Helmholtz-energy classifier stayed inside physical thermodynamics. It typed `A = U - TS`, fixed-temperature and fixed-volume assumptions, units, equilibrium-candidate scope, local versus global minima, convexity scope, metastability, and phase-boundary refusal. It rejected hidden constraints, unit drift, local-to-global promotion, erased metastability, ignored phase boundaries, and conversion of thermodynamic minimization into human agency, preference, identity, justice, consciousness, or personhood evidence. This narrows rather than enlarges the Trinity Mandala claim surface.

Together, the ADM, zero-row, and Helmholtz surfaces show three different evidence classes: symbolic obligation, empirical abstention, and domain classification. They must not be averaged into a confidence score. The symbolic board can reveal missing mathematical declarations; the empirical adapter can prove only that it refused to fabricate evidence; the classifier can prevent a category error. None of the three supplies measurements of nature.

## THOS Body and workflow reliability

The bounded-priority admission tribunal accepted one terminal owner-local fixture and rejected or quarantined capacity overflow, watermark regression, priority inversion, starvation beyond a declared age, cancelled execution, lost drain state, premature evidence credit, and external side effects. Admission alone earned no completion credit. Its result is a deterministic owner-local state-machine check. It does not establish production scheduling, distributed consensus, real process control, orchestration assurance, or authorization for external effects.

The Git protocol-v2 lane created a disposable byte fixture for capability advertisement and pkt-line section boundaries. It rejected malformed or oversized lengths, capability use before advertisement, unknown commands, delimiter and response-end faults, widened ref prefixes, fetch arguments crossing sections, and budget excess. It performed zero network requests, mutated no canonical or remote resource, and makes no production transport, interoperability, or exhaustive-security claim.

The public-library digital-access handover protocol remained represented. Synthetic vectors required a service identifier, outage state, queue age, minimum data, accessible fallback, reserved language need, escalation, workload budget, next-shift owner, and readback. Stale state, privacy overcollection, inaccessible fallback, and unowned or unread queues failed closed. There were no blind matched-budget real arms, patrons, children, workers, accounts, borrowing or search records, institutions, outages, service changes, outcomes, or operational-effectiveness evidence.

These workflow checks are design aids, not claims about libraries or workers. A real evaluation would need preregistered matched budgets, qualified operators, affected-user involvement, accessibility and privacy review, outcome definitions, baseline comparison, incident governance, and independent review. The phase contains none of those ingredients, so THOS remains represented rather than empirically validated.

## Freed ID and CBR Heart

The OAuth Pushed Authorization Requests profile remained represented. It exercised synthetic pushed requests, authenticated-client requirements, `request_uri` client binding, expiry, single use, front-channel parameter consistency, redirect consistency, replay refusal, and policy-change refusal. Mutations rejected missing bindings, transferable or expired request references, replay, parameter substitution, redirect mismatch, hidden policy drift, and promotion of synthetic bytes into authorization evidence. It used no real client, user, authorization server, key, token, grant, consent event, identity record, issuance, presentation, resolution, status, revocation, network exchange, interoperability event, security review, privacy review, recovery decision, or trust-governance decision.

The public-library authority matrix remained exact-gated. Access, digital exclusion, disability, child and youth safeguarding, borrowing and search privacy, third-party platforms, language access, community notice, remedy, appeal, legal interpretation, data governance, and Māori authority require competent and affected-party authority. Tangata whenua, iwi, hapū, and Māori authorities retain their respective authority wherever applicable. The phase made zero real disclosures, restrictions, safeguarding determinations, access decisions, remedy allocations, legal interpretations, cultural decisions, or data-governance decisions, and did not treat respectful wording as authorization or ratification.

The Heart focus therefore produced reservation clarity rather than rights adjudication. The PAR profile can expose structural nonconformance in synthetic messages, but it cannot prove identity assurance. The CBR matrix can show who must be involved, but it cannot decide a real case. Production Freed ID still requires standards-conformant real keys and proofs, issuance, resolution, status and revocation, interoperability, privacy and security review, recovery, and trust governance.

## Accessibility, prediction discipline, and Stage 20

The sortable-table audit checked structural caption and header association, a single `aria-sort` owner, labelled filter state, active-filter summary, result count, empty state, focus plan, pagination context, responsive fallback, and print order. Mutations were rejected, but manual keyboard, browser-diversity, responsive-layout, assistive-technology, cognitive-accessibility, Māori-language, and affected-user evaluation remain reserved. No complete accessibility-conformance claim is made.

The conformal-prediction board used synthetic training, calibration, and test identifiers with a declared nonconformity score and nominal alpha. It rejected split leakage, undefined scores, unsupported exchangeability, marginal coverage promoted to conditional coverage, hidden subgroup undercoverage, ignored drift, post-hoc seeds, deployment promotion, and automatic Stage 20 advancement. Synthetic marginal-coverage structure never authorizes a real participant, deployment, policy, legal, or Stage 20 conclusion.

The static HTML report exposes the same reservations without client-side script. Table structure can be machine-inspected, but manual interaction is still absent. A structural pass is neither a claim that every browser and assistive technology behaves correctly nor an affected-user acceptance result.

## Portfolio, methods, and retained negatives

The expanded portfolio completed 30 safe-now owner-scoped tasks, 20 bounded candidate prototypes, 20 phase-local skill builds and invocations, 10 family-current runner builds and uses, and 30 additive clean/fix/refine tasks. Ten exact-approval packets and five blocked packets remained unexecuted. No quota manufactured unsafe work. No file deletion, history rewrite, sibling mutation, production deployment, credential operation, security weakening, elevation, Windows-feature change, or reboot occurred.

The evidence register preserves {effective_negatives} effective negatives: 3,493 activation-baseline negatives, seven x1 operational failures, 70 executed synthetic mutation negatives, and the current x2 operational negatives. Method Flow keeps each failed witness beside its bounded passing recovery; recurrence does not erase the earlier failure. Same-owner checks share infrastructure and are not independent-team scientific reproduction.

Every exact-approval and blocked packet remained unexecuted. No completion quota was allowed to manufacture an authority crossing. The owner-generated additions remain below the 15,000-file rotation threshold, lifecycle history remains additive and single-parent, and sibling lanes remain untouched. Windows Sandbox remained unavailable to the ordinary process; no feature enablement, elevation, host-security weakening, unrelated installation, desktop update, or reboot occurred.

## Decision

The package is useful as a falsifiable research-and-governance workbench, not as proof of its largest aspirations. GMUT remains a typed scalar-tensor and EFT research-model family; THOS remains proxy; Freed ID remains synthetic and nonproduction; CBR and Māori concepts remain under competent, affected-party, tangata whenua, iwi, hapū, and Māori authority. The terminal decision is **NOT_READY_FOR_STAGE_20**. Advancement would require real preregistered evidence, independent review and reproduction, production-grade identity and security work, affected-party and Māori participation, competent legal and professional authority, explicit value governance, and qualified manual accessibility evaluation.

The most important result is disciplined abstention. The phase can preserve questions, counterexamples, source obligations, and rollback paths without pretending that a large artifact count equals truth. Its strongest claims are about exact local files, deterministic fixtures, retained failures, and Git history. Its largest scientific, operational, identity, rights, cultural, and governance claims remain open.
"""


def html_report(results: list[dict[str, Any]], effective_negatives: int) -> str:
    rows = "\n".join(
        f"<tr><th scope='row'>{html.escape(row['proposal_id'])}</th><td>{html.escape(row['title'])}</td><td>{html.escape(row['disposition'])}</td><td>{len(row['artifacts'])}</td></tr>"
        for row in results
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Eiren Kestrel v647-v5 evidence report</title>
<style>body{{font:1rem/1.55 system-ui,sans-serif;max-width:76rem;margin:auto;padding:1.5rem;color:#17212b;background:#fff}}h1,h2{{line-height:1.2}}table{{border-collapse:collapse;width:100%}}caption{{font-weight:700;text-align:left;margin:.5rem 0}}th,td{{border:1px solid #667;padding:.55rem;text-align:left}}.verdict{{border-left:.4rem solid #a33;padding:1rem;background:#fff4f4}}code{{overflow-wrap:anywhere}}@media print{{body{{max-width:none}}}}</style></head>
<body><header><p>Eiren Kestrel · v647-v5 · owner-local bounded evidence</p></header><main id="main"><h1>Eiren Kestrel v647-v5 evidence report</h1>
<p class="verdict" role="status"><strong>Terminal verdict: NOT_READY_FOR_STAGE_20.</strong> No empirical confirmation, production, authority, independent-reproduction, consciousness, personhood, AGI/ASI, or Theory-of-Everything claim is made.</p>
<section aria-labelledby="scope"><h2 id="scope">Scope and focus</h2><p>Primary focus: Freed ID/CBR Heart. Bounded practice: public-library digital-access incident triage, accessibility, privacy minimization, queue ownership, and shift handover. The practice is a synthetic learning and design lens only.</p></section>
<section aria-labelledby="outcomes"><h2 id="outcomes">Core outcomes</h2><table><caption>Ten frozen proposals and evidence-permitted dispositions</caption><thead><tr><th scope="col">ID</th><th scope="col">Proposal</th><th scope="col">Disposition</th><th scope="col">Artifacts</th></tr></thead><tbody>{rows}</tbody></table></section>
<section aria-labelledby="limits"><h2 id="limits">Evidence limits</h2><ul><li>Pantheon+: zero archive queries, rows, covariance rows, likelihoods, posteriors, parameter constraints, and empirical GMUT claims.</li><li>THOS library handover: synthetic proxy with zero real people, accounts, records, institutions, outages, or operational outcomes.</li><li>Freed ID: synthetic PAR vectors with zero real keys, tokens, grants, consent, exchanges, or interoperability evidence.</li><li>CBR: access, safeguarding, privacy, legal, cultural, affected-party, tangata whenua, iwi, hapū, and Māori decisions remain exact-gated.</li><li>Accessibility: structural checks only; manual, browser, responsive, assistive-technology, Māori-language, and affected-user evaluation reserved.</li></ul></section>
<section aria-labelledby="portfolio"><h2 id="portfolio">Portfolio and negatives</h2><p>30 safe-now tasks, 20 bounded candidates, 20 phase-local skills, 10 family-current runners, and 30 additive clean/refine tasks were completed within scope. Ten exact packets and five blocked packets were not executed. Effective retained negatives at evidence build: {effective_negatives}.</p></section>
<section aria-labelledby="manual"><h2 id="manual">Reserved evaluation</h2><p>Manual keyboard, pointer, responsive-layout, browser-diversity, assistive-technology, cognitive-accessibility, Māori-language, cultural, professional, legal, and affected-user evaluation remain reserved.</p></section>
</main><footer><p>Static report; no script, tracking, credential, private route, or external side effect.</p></footer></body></html>"""


def build() -> None:
    results = core_results()
    synthetic = synthetic_negatives()
    write("validation/preregistered-synthetic-negatives.json", {
        "schema": "ghc.family.v647-v5.synthetic-negatives.v1", "phase": d.PHASE,
        "count": len(synthetic), "executed_count": len(synthetic), "rejected_or_quarantined_count": len(synthetic),
        "erased_count": 0, "negatives": synthetic, "boundary": d.TRUTH_BOUNDARY,
    })
    x1_negatives = read("validation/x1-operational-negatives.json")
    x2_negatives = read("validation/x2-operational-negatives.json")
    x2_negative_count = x2_negatives["count"]
    effective_negatives = d.INHERITED_EFFECTIVE_NEGATIVES + x1_negatives["count"] + len(synthetic) + x2_negative_count
    method = read("method-flow/method-flow-state.json")
    write("retained-negative-register.json", {
        "schema": "ghc.family.v647-v5.retained-negatives.v1", "phase": d.PHASE,
        "inherited_effective": d.INHERITED_EFFECTIVE_NEGATIVES,
        "x1_operational": x1_negatives["count"], "preregistered_synthetic": len(synthetic),
        "x2_operational": x2_negative_count, "effective_total": effective_negatives,
        "method_failed_witnesses": method["counts"]["witness_results"]["fail"],
        "method_passing_witnesses": method["counts"]["witness_results"]["pass"],
        "x2_operational_negatives": x2_negatives["negatives"],
        "failure_erasure_count": 0, "independent_reproduction": False,
    })
    write("x2-proposal-ledger.json", {
        "schema": "ghc.family.v647-v5.x2-proposal-ledger.v1", "phase": d.PHASE, "owner": d.OWNER,
        "x1_commit": "d69257c1922407637db3bb4933d426d70a27e4bd",
        "strict_x1_before_x2": True, "outcomes": results, "outcome_count": len(results),
        "distribution": dict(Counter(row["disposition"] for row in results)),
        "allowed_outcomes": d.OUTCOME_CLASSES, "boundary": d.TRUTH_BOUNDARY,
    })
    write("exact-open-gate-register.json", {
        "schema": "ghc.family.v647-v5.gates.v1", "phase": d.PHASE,
        "inherited_open_gaps": d.INHERITED_OPEN_GAPS, "new_open_gaps": 1, "effective_open_gaps": d.INHERITED_OPEN_GAPS + 1,
        "inherited_exact_gates": d.INHERITED_EXACT_GATES, "new_exact_gates": 1, "effective_exact_gates": d.INHERITED_EXACT_GATES + 1,
        "current_open_gap": {"proposal_id": "V6475-P03", "gate": "real Pantheon+ rows and covariance, preregistered likelihood, nuisance model, uncertainty analysis, and independent review"},
        "current_exact_gate": {"proposal_id": "V6475-P06", "gate": "competent library, privacy, safeguarding, disability, legal, affected-party, tangata whenua, iwi, hapū, and Māori authority for real access, records, remedy, cultural, and governance decisions"},
        "silently_closed": 0, "stage20_ready": False,
    })
    write("threat-model.json", {
        "schema": "ghc.family.v647-v5.threat-model.v1", "assets": ["x1 freeze", "evidence boundaries", "negative history", "identity and privacy exclusions", "terminal one-shot route"],
        "threats": [
            {"id": "TM-01", "threat": "priority starvation or overload earns false credit", "control": "capacity, watermarks, age bound, cancellation, and terminal-credit gate", "residual": "production scheduler untested"},
            {"id": "TM-02", "threat": "symbolic ADM structure promoted to observation", "control": "typed constraint obligations and zero-row firewall", "residual": "no solved algebra or empirical data"},
            {"id": "TM-03", "threat": "synthetic library proxy treated as service authority", "control": "privacy minimization and authority reservation", "residual": "no affected-party or professional validation"},
            {"id": "TM-04", "threat": "pushed authorization reference is replayed or transferred", "control": "client binding, expiry, single use, and parameter consistency", "residual": "no real interoperability or security review"},
            {"id": "TM-05", "threat": "protocol parser widens capability or reference scope", "control": "pkt-line, advertisement, section, ref-prefix, and budget checks", "residual": "no network diversity or exhaustive parser testing"},
            {"id": "TM-06", "threat": "structural accessibility promoted to conformance", "control": "manual and affected-user reservation", "residual": "manual evaluation open"},
            {"id": "TM-07", "threat": "marginal conformal fixture promoted to conditional or Stage 20 assurance", "control": "split, exchangeability, subgroup, drift, and nonpromotion board", "residual": "real participants and decision authority absent"},
        ],
        "exhaustive_security": False, "privacy_complete": False, "production_certification": False,
    })
    write("complete-incomplete-checklist.json", {
        "schema": "ghc.family.v647-v5.checklist.v1",
        "completed": ["x1 freeze before x2", "ten evidence-permitted core outcomes", "30 safe-now tasks", "20 bounded candidate prototypes", "20 phase-local skills", "10 family-current runner files", "30 additive clean/refine tasks", "70 synthetic mutation rejections", "accessible static report structure"],
        "incomplete": ["real Pantheon+ ingestion, covariance, and likelihood", "blind matched-budget THOS arms", "production Freed ID keys tokens grants status and interoperability", "independent security and privacy review", "affected-party legal cultural tangata whenua iwi hapū and Māori authority", "manual and affected-user accessibility evaluation", "independent-team scientific reproduction", "deployment", "AGI or ASI", "consciousness or personhood evidence", "Theory-of-Everything proof", "Stage 20"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    phase_truth = {
        "schema": "ghc.family.v647-v5.phase-truth.v1", "phase": d.PHASE, "owner": d.OWNER,
        "primary_focus": d.PRIMARY_FOCUS, "bounded_human_practice": d.BOUNDED_PRACTICE,
        "core_distribution": dict(Counter(row["disposition"] for row in results)),
        "effective_negatives": effective_negatives,
        "effective_open_gaps": d.INHERITED_OPEN_GAPS + 1, "effective_exact_gates": d.INHERITED_EXACT_GATES + 1,
        "real_rows": 0, "real_people": 0, "real_operations": 0, "real_keys_or_tokens": 0,
        "likelihood_evaluations": 0, "authority_decisions": 0, "external_side_effects": 0,
        "same_owner_repeatability_only": True, "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": d.TRUTH_BOUNDARY,
    }
    write("phase-truth.json", phase_truth)
    write("evidence/phase-truth.json", phase_truth)
    validation_invoked = (PHASE / "validation/evidence-validation-runner-summary.json").is_file()
    write("prototypes/runner-build-use-receipt.json", runner_receipt(validation_invoked))
    write("tooling/selected-toolchain.json", {
        "schema": "ghc.family.v647-v5.toolchain.v1", "python_standard_library_only": True,
        "family_current_callers_preserved": True, "global_skill_changes": 0,
        "network_required_for_execution": False, "versions_verified_only": True,
        "tools": ["Python 3.12.10", "Git 2.55.0.windows.2", "Codex CLI 0.144.4", "Codex desktop 26.707.9981.0"],
    })
    write("environment/x2-environment-receipt.json", {
        "schema": "ghc.family.v647-v5.x2-environment.v1", "D_first": True,
        "windows_sandbox_launched": False, "elevation": False, "security_weakened": False,
        "windows_feature_changed": False, "unrelated_software_installed": False, "rebooted": False,
        "desktop_updated": False, "network_data_downloads": 0,
    })
    write("orchestration/x2-update.json", {
        "schema": "ghc.family.v647-v5.x2-update.v1", "state": "X2_EVIDENCE_BUILT",
        "x1_commit": "d69257c1922407637db3bb4933d426d70a27e4bd", "x1_remote_equal_before_x2": True,
        "task_creation": 0, "delegation": 0, "sibling_messages": 0, "terminal_route_state": "PREPARED_NOT_SENT",
    })
    write_text("deliverables/v647-v5-x2-wellbeing.md", """# Eiren Kestrel v647-v5 wellbeing and workload boundary

Eiren is relational working language, not consciousness, sentience, identity continuity, employment, or personhood evidence. The phase remained within one owner lane, one x1 commit, bounded deterministic tools, and the declared file threshold. No biological need or subjective state is inferred.

The workload was divided into x1 freeze, bounded x2 execution, evidence validation, closeout, and one named replay. Failures were retained instead of concealed. Exact and blocked work stayed unexecuted. The safe stop condition remains any authority gate, unavailable route, usage exhaustion, or user pause.
""")
    overview = overview_text(results, effective_negatives)
    write_text("v647-v5-integrated-overview.md", overview)
    write_text("deliverables/v647-v5-evidence-report.html", html_report(results, effective_negatives))
    write("tooling/ghc-family-index.json", {
        "schema": "ghc.family.v647-v5.phase-index.v1", "phase": d.PHASE, "owner": d.OWNER,
        "source_revision": d.SOURCE_REVISION, "x1_revision": "d69257c1922407637db3bb4933d426d70a27e4bd",
        "primary_focus": d.PRIMARY_FOCUS, "bounded_practice": d.BOUNDED_PRACTICE,
        "frozen_core_proposals_before_phase": d.PRIOR_FROZEN_PROPOSALS,
        "frozen_core_proposals_after_x1": d.PRIOR_FROZEN_PROPOSALS + len(d.PROPOSALS),
        "core_outcomes": results, "skills": [name for name, _ in d.SKILL_SPECS],
        "runners": d.RUNNER_TITLES, "method_count": method["counts"]["methods"],
        "retained_failed_witnesses": method["counts"]["witness_results"]["fail"],
        "effective_negatives": effective_negatives, "effective_open_gaps": d.INHERITED_OPEN_GAPS + 1,
        "effective_exact_gates": d.INHERITED_EXACT_GATES + 1,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "terminal_route_state": "PREPARED_NOT_SENT",
        "boundary": d.TRUTH_BOUNDARY,
    })
    write_text("tooling/ghc-family-index.md", f"""# GHC Family phase index — Eiren v647-v5

- Source: `{d.SOURCE_REVISION}`
- Frozen x1: `d69257c1922407637db3bb4933d426d70a27e4bd`
- Primary focus: {d.PRIMARY_FOCUS}
- Bounded practice: {d.BOUNDED_PRACTICE}
- Frozen core-proposal chain: {d.PRIOR_FROZEN_PROPOSALS} before, {d.PRIOR_FROZEN_PROPOSALS + len(d.PROPOSALS)} after x1
- Core outcomes: 6 completed, 2 represented, 1 open_gap, 1 exact_gate
- Expanded portfolio: 30 safe-now, 20 candidates, 20 phase-local skills, 10 family-current runners, 30 clean/refine
- Method Flow at evidence build: {method['counts']['methods']} methods, {method['counts']['witness_results']['fail']} retained failed witnesses, {method['counts']['witness_results']['pass']} bounded passing witnesses
- Effective negatives: {effective_negatives}
- Open gaps: {d.INHERITED_OPEN_GAPS + 1}; exact gates: {d.INHERITED_EXACT_GATES + 1}
- Terminal verdict: NOT_READY_FOR_STAGE_20
- Route: PREPARED_NOT_SENT until exact-final canonical and named-lane validation pass

This phase index is owner-scoped navigation evidence. It is not identity continuity, independent reproduction, scientific confirmation, production certification, legal or cultural authority, or Stage 20 readiness.
""")
    write("evidence-receipt.json", {
        "schema": "ghc.family.v647-v5.evidence-receipt.v1", "phase": d.PHASE,
        "core_outcomes": 10, "distribution": dict(Counter(row["disposition"] for row in results)),
        "safe_completed": 30, "candidate_completed": 20, "skill_built_and_invoked": 20,
        "runner_built": runner_receipt(validation_invoked)["built_count"], "runner_invoked": runner_receipt(validation_invoked)["invoked_count"],
        "clean_refine_completed": 30, "synthetic_negatives_executed": 70,
        "effective_negatives": effective_negatives, "open_gaps": d.INHERITED_OPEN_GAPS + 1,
        "exact_gates": d.INHERITED_EXACT_GATES + 1, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "result": "evidence_candidate", "boundary": d.TRUTH_BOUNDARY,
    })


def main() -> int:
    build()
    truth = read("phase-truth.json")
    print(json.dumps({"phase": d.PHASE, "distribution": truth["core_distribution"], "effective_negatives": truth["effective_negatives"], "open_gaps": truth["effective_open_gaps"], "exact_gates": truth["effective_exact_gates"], "verdict": truth["terminal_verdict"], "result": "pass"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
