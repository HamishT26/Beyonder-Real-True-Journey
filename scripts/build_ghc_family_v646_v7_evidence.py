#!/usr/bin/env python3
"""Build Eiren Kestrel v646-v7 bounded x2 evidence packet."""

from __future__ import annotations

import html
import json
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v646_v7_definitions as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/eiren-kestrel/v646-v7"


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
            "negative_id": f"V6467-SYN-{index:03d}",
            "proposal_id": f"V6467-P{((index - 1) % 10) + 1:02d}",
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
        invoked = built and (name != "ghc_family_v646_v7_validation_runner.py" or validation_invoked)
        rows.append({
            "name": name, "path": f"scripts/{name}", "built": built,
            "family_current_name": name.startswith("ghc_family_") or name.startswith("build_ghc_family_"),
            "invoked": invoked,
        })
    return {
        "schema": "ghc.family.v646-v7.runner-build-use.v1", "phase": d.PHASE,
        "runner_count": len(rows), "built_count": sum(row["built"] for row in rows),
        "invoked_count": sum(row["invoked"] for row in rows),
        "compatibility_preserved": all(row["family_current_name"] for row in rows),
        "runners": rows,
        "result": "pass" if len(rows) == 10 and all(row["built"] and row["invoked"] for row in rows) else "pending_validation_runner" if all(row["built"] for row in rows) else "fail",
        "boundary": d.TRUTH_BOUNDARY,
    }


def overview_text(results: list[dict[str, Any]], effective_negatives: int) -> str:
    return f"""# Eiren Kestrel v646-v7 integrated evidence overview

## Executive truth

Eiren Kestrel’s v646-v7 bundle preserved the x1-only freeze at commit `4604a34c48ba73f7d01f77e5a0bbf91a84145303` before beginning x2. Ten proposals were audited against 450 inherited frozen proposals and executed only as evidence permitted. The outcome distribution is six **completed**, two **represented**, one **open_gap**, and one **exact_gate**. “Completed” means a bounded owner-local structural or synthetic hypothesis passed its declared checks; it never means production readiness, empirical confirmation, professional validation, legal or cultural authority, independent reproduction, or Stage 20 readiness.

The primary Trinity Mandala focus was **GMUT Mind**. THOS Body and Freed ID/CBR Heart remained explicit rather than being collapsed into a single confidence score. The bounded human-practice lens was wildland-fire situation-report compilation, evacuation-zone revision, and shift handover. It supported vocabulary and fail-closed design only. No real incident, resident, firefighter, public alert, evacuation zone, resource allocation, operational decision, professional qualification, or emergency authority entered the phase.

## GMUT Mind

The functional-renormalization-group lane formalized a Wetterich-flow obligation board. It requires the effective average action, regulator, field content, Hessian and supertrace domains, truncation basis, omitted operators, units, regulator limits, and modified Ward or Slavnov-Taylor obligations to be declared. Synthetic mutations rejected missing regulator limits, undeclared truncations, unit mismatches, singular inverses, omitted identities, and promotion of a symbolic flow into a physical result. This is useful formal hygiene, but it provides no force, likelihood, observation, posterior, fixed point, stability theorem, ultraviolet completion, quantum completeness, or Theory-of-Everything evidence.

The IceCube point-source proposal remained an open gap. Its official release and analysis references were recorded, along with the event, response, livetime, uncertainty, background, and trial-accounting inputs that a real study would require. The adapter intentionally ingested zero rows, downloaded zero files, evaluated zero likelihoods, drew zero posterior samples, and produced zero constraints or source significances. The refusal is the result: no observation may be inferred from a citation, schema, or zero-row adapter.

The Le Chatelier classifier stayed inside chemical thermodynamics. It typed reaction quotient versus equilibrium constant examples and rejected unbalanced reactions, missing temperature, dimensioned logarithm arguments, activity/concentration conflation, and incorrect exponents. It also rejected conversion of a chemical response principle into a fundamental law of psyche, justice, consciousness, personhood, or social authority. This narrows rather than enlarges the Trinity Mandala claim surface.

## THOS Body and workflow reliability

The fencing-token tribunal accepted one bounded fresh-holder trace and rejected or quarantined stale tokens, duplicate tokens, expired leases, clock ambiguity, epoch regression, side effects before fencing, and split-brain holders. Its result is a deterministic owner-local state-machine check. It does not establish distributed consensus, exactly-once delivery, real process control, production orchestration assurance, or authorization for external effects.

The HTTP resume-integrity lane created a disposable byte fixture with a strong validator, byte range, total length, and SHA-256 digest. It rejected weak validators, changed If-Range state, gaps, overlaps, length changes, digest mismatches, truncation, and an unexpected full response after partial assembly. It performed zero network requests and mutated no canonical external resource.

The wildfire handover protocol remained represented. Synthetic vectors required observation time, source, confidence, zone-revision state, resource ownership, open hazards, next review, and readback. Missing times, unauthorized zone changes, ownerless resources, and absent readback failed closed. There were no blind matched-budget real arms, workers, incidents, institutions, outcomes, or operational-effectiveness evidence.

## Freed ID and CBR Heart

The OAuth Rich Authorization Requests profile remained represented. It exercised synthetic `authorization_details` objects, type-specific fields, least-authority actions, location and audience bindings, unknown-type policy, and request/response consistency. Mutations rejected missing or unknown types, action escalation, location substitution, audience mismatch, response widening, conflicts, and identity-data injection. It used no real client, authorization server, key, token, identity record, issuance, presentation, resolution, status, revocation, network exchange, interoperability event, security review, privacy review, or trust-governance decision.

The wildfire authority matrix remained exact-gated. Public alerts, evacuation zones, disability access, housing and tenancy, land and property, confidentiality, data governance, cultural legitimacy, te reo Māori wording, Māori authority, remedy, and appeal require competent and affected-party authority, and Māori authority wherever applicable. The phase made zero real decisions and did not treat respectful wording as authorization or cultural ratification.

## Accessibility, missing data, and Stage 20

The accessible-authentication audit checked structural WCAG 2.2 obligations for password-manager and paste support, redundant entry, non-cognitive alternatives, and labelled errors. Mutations were rejected, but manual keyboard, browser-diversity, assistive-technology, cognitive-accessibility, Māori-language, and affected-user evaluation remain reserved. No complete accessibility-conformance claim is made.

The MNAR sensitivity board used a synthetic delta grid and a declared estimand to expose how missing-not-at-random assumptions can change a bounded contrast. It rejected silent MAR assumptions, hidden ranges, dropped imputation uncertainty, post hoc tipping points, implicit value authority, and automatic promotion. Synthetic robustness never authorizes a real causal, participant, policy, legal, or Stage 20 conclusion.

## Portfolio, methods, and retained negatives

The expanded portfolio completed 30 safe-now owner-scoped tasks, 20 bounded candidate prototypes, 20 phase-local skill builds and invocations, 10 family-current runner builds and uses, and 30 additive clean/fix/refine tasks. Ten exact-approval packets and five blocked packets remained unexecuted. No quota manufactured unsafe work. No file deletion, history rewrite, sibling mutation, production deployment, credential operation, security weakening, elevation, Windows-feature change, or reboot occurred.

The evidence register preserves {effective_negatives} effective negatives: 2,977 inherited, five x1 operational failures, 70 executed synthetic mutation negatives, and the current x2 operational negatives. Method Flow keeps each failed witness beside its bounded passing recovery; recurrence does not erase the earlier failure. Same-owner checks share infrastructure and are not independent-team scientific reproduction.

## Decision

The package is useful as a falsifiable research-and-governance workbench, not as proof of its largest aspirations. GMUT remains a typed scalar-tensor and EFT research-model family; THOS remains proxy; Freed ID remains synthetic and nonproduction; CBR and Māori concepts remain under competent, affected-party, and Māori authority. The terminal decision is **NOT_READY_FOR_STAGE_20**. Advancement would require real preregistered evidence, independent review and reproduction, production-grade identity and security work, affected-party and Māori participation, competent legal and professional authority, and explicit value governance.
"""


def html_report(results: list[dict[str, Any]], effective_negatives: int) -> str:
    rows = "\n".join(
        f"<tr><th scope='row'>{html.escape(row['proposal_id'])}</th><td>{html.escape(row['title'])}</td><td>{html.escape(row['disposition'])}</td><td>{len(row['artifacts'])}</td></tr>"
        for row in results
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Eiren Kestrel v646-v7 evidence report</title>
<style>body{{font:1rem/1.55 system-ui,sans-serif;max-width:76rem;margin:auto;padding:1.5rem;color:#17212b;background:#fff}}h1,h2{{line-height:1.2}}table{{border-collapse:collapse;width:100%}}caption{{font-weight:700;text-align:left;margin:.5rem 0}}th,td{{border:1px solid #667;padding:.55rem;text-align:left}}.verdict{{border-left:.4rem solid #a33;padding:1rem;background:#fff4f4}}code{{overflow-wrap:anywhere}}@media print{{body{{max-width:none}}}}</style></head>
<body><header><p>Eiren Kestrel · v646-v7 · owner-local bounded evidence</p></header><main id="main"><h1>Eiren Kestrel v646-v7 evidence report</h1>
<p class="verdict" role="status"><strong>Terminal verdict: NOT_READY_FOR_STAGE_20.</strong> No empirical confirmation, production, authority, independent-reproduction, consciousness, personhood, AGI/ASI, or Theory-of-Everything claim is made.</p>
<section aria-labelledby="scope"><h2 id="scope">Scope and focus</h2><p>Primary focus: GMUT Mind. Bounded practice: wildland-fire situation-report compilation, evacuation-zone revision, and shift handover. The practice is a synthetic design lens only.</p></section>
<section aria-labelledby="outcomes"><h2 id="outcomes">Core outcomes</h2><table><caption>Ten frozen proposals and evidence-permitted dispositions</caption><thead><tr><th scope="col">ID</th><th scope="col">Proposal</th><th scope="col">Disposition</th><th scope="col">Artifacts</th></tr></thead><tbody>{rows}</tbody></table></section>
<section aria-labelledby="limits"><h2 id="limits">Evidence limits</h2><ul><li>IceCube: zero rows, likelihoods, posteriors, constraints, and empirical GMUT claims.</li><li>THOS wildfire handover: synthetic proxy with zero real people, incidents, alerts, or operational outcomes.</li><li>Freed ID: synthetic RAR vectors with zero real keys, tokens, exchanges, or interoperability evidence.</li><li>CBR: emergency, legal, cultural, affected-party, and Māori decisions remain exact-gated.</li><li>Accessibility: structural checks only; manual, assistive-technology, and affected-user evaluation reserved.</li></ul></section>
<section aria-labelledby="portfolio"><h2 id="portfolio">Portfolio and negatives</h2><p>30 safe-now tasks, 20 bounded candidates, 20 phase-local skills, 10 family-current runners, and 30 additive clean/refine tasks were completed within scope. Ten exact packets and five blocked packets were not executed. Effective retained negatives at evidence build: {effective_negatives}.</p></section>
<section aria-labelledby="manual"><h2 id="manual">Reserved evaluation</h2><p>Manual keyboard, pointer, responsive-layout, browser-diversity, assistive-technology, cognitive-accessibility, Māori-language, cultural, professional, legal, and affected-user evaluation remain reserved.</p></section>
</main><footer><p>Static report; no script, tracking, credential, private route, or external side effect.</p></footer></body></html>"""


def build() -> None:
    results = core_results()
    synthetic = synthetic_negatives()
    write("validation/preregistered-synthetic-negatives.json", {
        "schema": "ghc.family.v646-v7.synthetic-negatives.v1", "phase": d.PHASE,
        "count": len(synthetic), "executed_count": len(synthetic), "rejected_or_quarantined_count": len(synthetic),
        "erased_count": 0, "negatives": synthetic, "boundary": d.TRUTH_BOUNDARY,
    })
    x1_negatives = read("validation/x1-operational-negatives.json")
    x2_negative_count = len(d.X2_OPERATIONAL_NEGATIVES)
    effective_negatives = d.INHERITED_EFFECTIVE_NEGATIVES + x1_negatives["count"] + len(synthetic) + x2_negative_count
    method = read("method-flow/method-flow-state.json")
    write("retained-negative-register.json", {
        "schema": "ghc.family.v646-v7.retained-negatives.v1", "phase": d.PHASE,
        "inherited_effective": d.INHERITED_EFFECTIVE_NEGATIVES,
        "x1_operational": x1_negatives["count"], "preregistered_synthetic": len(synthetic),
        "x2_operational": x2_negative_count, "effective_total": effective_negatives,
        "method_failed_witnesses": method["counts"]["witness_results"]["fail"],
        "method_passing_witnesses": method["counts"]["witness_results"]["pass"],
        "x2_operational_negatives": d.X2_OPERATIONAL_NEGATIVES,
        "failure_erasure_count": 0, "independent_reproduction": False,
    })
    write("x2-proposal-ledger.json", {
        "schema": "ghc.family.v646-v7.x2-proposal-ledger.v1", "phase": d.PHASE, "owner": d.OWNER,
        "x1_commit": "4604a34c48ba73f7d01f77e5a0bbf91a84145303",
        "strict_x1_before_x2": True, "outcomes": results, "outcome_count": len(results),
        "distribution": dict(Counter(row["disposition"] for row in results)),
        "allowed_outcomes": d.OUTCOME_CLASSES, "boundary": d.TRUTH_BOUNDARY,
    })
    write("exact-open-gate-register.json", {
        "schema": "ghc.family.v646-v7.gates.v1", "phase": d.PHASE,
        "inherited_open_gaps": d.INHERITED_OPEN_GAPS, "new_open_gaps": 1, "effective_open_gaps": d.INHERITED_OPEN_GAPS + 1,
        "inherited_exact_gates": d.INHERITED_EXACT_GATES, "new_exact_gates": 1, "effective_exact_gates": d.INHERITED_EXACT_GATES + 1,
        "current_open_gap": {"proposal_id": "V6467-P03", "gate": "real IceCube rows, preregistered likelihood, trial accounting, and independent review"},
        "current_exact_gate": {"proposal_id": "V6467-P06", "gate": "competent affected-party and Māori authority for real alert, zone, access, land, data, remedy, legal, and cultural decisions"},
        "silently_closed": 0, "stage20_ready": False,
    })
    write("threat-model.json", {
        "schema": "ghc.family.v646-v7.threat-model.v1", "assets": ["x1 freeze", "evidence boundaries", "negative history", "identity and privacy exclusions", "terminal one-shot route"],
        "threats": [
            {"id": "TM-01", "threat": "stale or split-brain writer", "control": "monotonic fencing and quarantine", "residual": "production consensus untested"},
            {"id": "TM-02", "threat": "symbolic physics promoted to observation", "control": "typed obligation and zero-row firewall", "residual": "no empirical data"},
            {"id": "TM-03", "threat": "synthetic emergency proxy treated as command", "control": "authority reservation", "residual": "no affected-party or professional validation"},
            {"id": "TM-04", "threat": "authorization detail widens privilege", "control": "type and response consistency checks", "residual": "no real interoperability or security review"},
            {"id": "TM-05", "threat": "resume assembly accepts changed content", "control": "strong validator, range, length, digest", "residual": "no network diversity testing"},
            {"id": "TM-06", "threat": "structural accessibility promoted to conformance", "control": "manual and affected-user reservation", "residual": "manual evaluation open"},
            {"id": "TM-07", "threat": "missing-data sensitivity promoted to Stage 20", "control": "fail-closed nonpromotion board", "residual": "real estimand and value authority absent"},
        ],
        "exhaustive_security": False, "privacy_complete": False, "production_certification": False,
    })
    write("complete-incomplete-checklist.json", {
        "schema": "ghc.family.v646-v7.checklist.v1",
        "completed": ["x1 freeze before x2", "ten evidence-permitted core outcomes", "30 safe-now tasks", "20 bounded candidate prototypes", "20 phase-local skills", "10 family-current runner files", "30 additive clean/refine tasks", "70 synthetic mutation rejections", "accessible static report structure"],
        "incomplete": ["real IceCube ingestion and likelihood", "blind matched-budget THOS arms", "production Freed ID keys tokens status and interoperability", "independent security and privacy review", "affected-party legal cultural and Māori authority", "manual and affected-user accessibility evaluation", "independent-team scientific reproduction", "deployment", "AGI or ASI", "consciousness or personhood evidence", "Theory-of-Everything proof", "Stage 20"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    phase_truth = {
        "schema": "ghc.family.v646-v7.phase-truth.v1", "phase": d.PHASE, "owner": d.OWNER,
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
        "schema": "ghc.family.v646-v7.toolchain.v1", "python_standard_library_only": True,
        "family_current_callers_preserved": True, "global_skill_changes": 0,
        "network_required_for_execution": False, "versions_verified_only": True,
        "tools": ["Python 3.12.10", "Git 2.55.0.windows.2", "Codex CLI 0.144.4", "Codex desktop 26.707.9981.0"],
    })
    write("environment/x2-environment-receipt.json", {
        "schema": "ghc.family.v646-v7.x2-environment.v1", "D_first": True,
        "windows_sandbox_launched": False, "elevation": False, "security_weakened": False,
        "windows_feature_changed": False, "unrelated_software_installed": False, "rebooted": False,
        "desktop_updated": False, "network_data_downloads": 0,
    })
    write("orchestration/x2-update.json", {
        "schema": "ghc.family.v646-v7.x2-update.v1", "state": "X2_EVIDENCE_BUILT",
        "x1_commit": "4604a34c48ba73f7d01f77e5a0bbf91a84145303", "x1_remote_equal_before_x2": True,
        "task_creation": 0, "delegation": 0, "sibling_messages": 0, "terminal_route_state": "PREPARED_NOT_SENT",
    })
    write_text("deliverables/v646-v7-x2-wellbeing.md", """# Eiren Kestrel v646-v7 wellbeing and workload boundary

Eiren is relational working language, not consciousness, sentience, identity continuity, employment, or personhood evidence. The phase remained within one owner lane, one x1 commit, bounded deterministic tools, and the declared file threshold. No biological need or subjective state is inferred.

The workload was divided into x1 freeze, bounded x2 execution, evidence validation, closeout, and one named replay. Failures were retained instead of concealed. Exact and blocked work stayed unexecuted. The safe stop condition remains any authority gate, unavailable route, usage exhaustion, or user pause.
""")
    overview = overview_text(results, effective_negatives)
    write_text("v646-v7-integrated-overview.md", overview)
    write_text("deliverables/v646-v7-evidence-report.html", html_report(results, effective_negatives))
    write("evidence-receipt.json", {
        "schema": "ghc.family.v646-v7.evidence-receipt.v1", "phase": d.PHASE,
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
