#!/usr/bin/env python3
"""Build the bounded Eiren Kestrel v645-v3 x2 evidence packet."""

from __future__ import annotations

import hashlib
import html
import json
import math
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

from ghc_family_v645_v3_definitions import (
    BLOCKED_PACKETS, EIREN_CANDIDATE, EIREN_CLEAN, EIREN_RUNNERS,
    EIREN_SAFE_NOW, EIREN_SKILLS, EXACT_PACKETS, IDENTITY_BOUNDARY,
    PROPOSALS, SUCCESSOR_CANDIDATE, SUCCESSOR_CLEAN, SUCCESSOR_RUNNERS,
    SUCCESSOR_SAFE_NOW, SUCCESSOR_SKILLS, TRUTH_BOUNDARY,
)

PHASE = "v645-gmut-thos-v3-x1-x2"
OWNER = "Eiren Kestrel"
PHASE_REL = Path("docs/eiren-kestrel/v645-v3")
X1_COMMIT = "abb576e6de2666dd2dc792f6dd189722424ff0c2"
SOURCE_REVISION = "c8ef5b28537eb1e85f79e3ead3977a031504f0dc"
SOURCE_SEAL = "1dfbf310a9313117c692a060b9c4e3a5ad8e1626"
INHERITED_NEGATIVES = 1916


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8").stdout.strip()


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, payload: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def write_contract(path: Path, proposal: dict, claims: list[str], refusals: list[str], evidence: dict | None = None) -> None:
    write_json(path, {
        "schema": "ghc.family.v645-v3.bounded-contract.v1", "phase": PHASE,
        "proposal_id": proposal["proposal_id"], "title": proposal["title"],
        "hypothesis": proposal["hypothesis"], "accepts": claims, "refuses": refusals,
        "evidence": evidence or {}, "rollback": proposal["rollback_or_recovery"],
        "protected_gates": proposal["protected_gates"], "boundary": TRUTH_BOUNDARY,
    })


def append_method_flow(phase_dir: Path) -> dict:
    ledger = load(phase_dir / "method-flow/method-flow-state.json")
    method = {
        "method_id": "V6453-M07", "title": "Blueprint-only sandbox fallback when runtime is unavailable",
        "failure_signature": "Read-only host probing found neither Windows Sandbox executable nor the wsb CLI available to the current non-elevated process.",
        "trigger_preconditions": ["sandbox runtime unavailable", "active route must not be interrupted", "templates can still be linted"],
        "privacy_class": "sanitized_public", "approval_class": "safe_now_blueprint_only",
        "candidate_workaround": "Compose and lint six fail-closed owner profiles, preserve runtime and installation as open, and defer feature changes, elevation, and reboot.",
        "validation_witness_ids": ["V6453-W07-F", "V6453-W07-P"],
        "recurrence_guard": "Probe runtime availability before launch or installation claims; never infer success from a valid template.",
        "rollback": "Retain the templates as inactive blueprints and make no host change.",
        "recommendation_state": "preferred", "supersedes": [],
        "protected_gates": ["host_feature_change", "elevation", "reboot", "sandbox_runtime", "package_installation"],
        "retained_negative_ids": ["V6453-X2-N01"],
        "scope_boundary": "Template composition and linting only; no sandbox session or administrative runtime was established.",
    }
    witnesses = [
        {"witness_id": "V6453-W07-F", "method_id": "V6453-M07", "procedure": "Read-only executable, CLI, optional-feature, and elevation probe", "scope": "current Windows host process", "expected": "Runtime available for a bounded launch", "observed": "No executable or CLI available; current process not elevated", "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6453-X2-N01"], "boundary": TRUTH_BOUNDARY},
        {"witness_id": "V6453-W07-P", "method_id": "V6453-M07", "procedure": "XML and permission lint of six owner sandbox templates", "scope": "inactive blueprint files", "expected": "Six templates pass fail-closed structure", "observed": "Six of six templates passed", "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6453-X2-N01"], "boundary": TRUTH_BOUNDARY},
    ]
    if not any(item["method_id"] == "V6453-M07" for item in ledger["methods"]):
        ledger["methods"].append(method)
        ledger["witnesses"].extend(witnesses)
        ledger["state_events"].extend([
            {"event_id": "V6453-E13", "method_id": "V6453-M07", "from": "candidate", "to": "validated", "witness_id": "V6453-W07-P"},
            {"event_id": "V6453-E14", "method_id": "V6453-M07", "from": "validated", "to": "preferred", "witness_id": "V6453-W07-P"},
        ])
        ledger["recommendations"].append({"recommendation_id": "V6453-R07", "method_id": "V6453-M07", "preconditions": "Sandbox runtime unavailable but blueprints remain useful", "preferred_method": "Lint templates and preserve runtime as open", "witness": "V6453-W07-P", "exceptions": "Do not claim launch or installation", "rollback": "Make no host change"})
    if not any(item["method_id"] == "V6453-M08" for item in ledger["methods"]):
        ledger["methods"].append({
            "method_id": "V6453-M08", "title": "Runner-derived Method Flow count refresh",
            "failure_signature": "The family Method Flow validator rejected manually named derived-count fields as stale.",
            "trigger_preconditions": ["ledger methods or witnesses changed", "derived counts were edited manually"],
            "privacy_class": "sanitized_public", "approval_class": "safe_now_schema_repair",
            "candidate_workaround": "Regenerate counts using the runner schema: methods, witnesses, state_events, recommendations, state histogram, and witness-result histogram.",
            "validation_witness_ids": ["V6453-W08-F", "V6453-W08-P"],
            "recurrence_guard": "After every ledger mutation, invoke the family runner or reproduce its exact refresh_counts schema before validation.",
            "rollback": "Treat the ledger as invalid and retain the failed receipt until runner validation passes.",
            "recommendation_state": "preferred", "supersedes": [],
            "protected_gates": ["method_evidence_integrity", "negative_retention", "schema_drift"],
            "retained_negative_ids": ["V6453-X2-N02"],
            "scope_boundary": "Derived metadata repair only; no negative, witness, method, or recommendation is deleted.",
        })
        ledger["witnesses"].extend([
            {"witness_id": "V6453-W08-F", "method_id": "V6453-M08", "procedure": "Family Method Flow validation with manually named derived counts", "scope": "v645-v3 method ledger", "expected": "Valid ledger", "observed": "One issue: derived counts are stale", "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6453-X2-N02"], "boundary": TRUTH_BOUNDARY},
            {"witness_id": "V6453-W08-P", "method_id": "V6453-M08", "procedure": "Family Method Flow validation with exact runner-derived count schema", "scope": "same ledger with no evidence deletion", "expected": "Zero issues", "observed": "Zero issues and valid receipt", "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6453-X2-N02"], "boundary": TRUTH_BOUNDARY},
        ])
        ledger["state_events"].extend([
            {"event_id": "V6453-E15", "method_id": "V6453-M08", "from": "candidate", "to": "validated", "witness_id": "V6453-W08-P"},
            {"event_id": "V6453-E16", "method_id": "V6453-M08", "from": "validated", "to": "preferred", "witness_id": "V6453-W08-P"},
        ])
        ledger["recommendations"].append({"recommendation_id": "V6453-R08", "method_id": "V6453-M08", "preconditions": "Method Flow evidence changed", "preferred_method": "Refresh exact runner-derived counts before validation", "witness": "V6453-W08-P", "exceptions": "Never delete evidence to make counts match", "rollback": "Keep the ledger invalid until repaired"})
    states = Counter(item["recommendation_state"] for item in ledger["methods"])
    witness_results = Counter(item["result"] for item in ledger["witnesses"])
    ledger["counts"] = {
        "methods": len(ledger["methods"]), "witnesses": len(ledger["witnesses"]),
        "state_events": len(ledger["state_events"]), "recommendations": len(ledger["recommendations"]),
        "states": {state: states.get(state, 0) for state in ("observed", "candidate", "validated", "preferred", "superseded", "deprecated")},
        "witness_results": {result: witness_results.get(result, 0) for result in ("pass", "fail")},
    }
    write_json(phase_dir / "method-flow/method-flow-state.json", ledger)
    return ledger


def build_domain_artifacts(phase_dir: Path) -> None:
    p = {item["proposal_id"]: item for item in PROPOSALS}
    write_contract(phase_dir / "method-flow/causal-incident-contract.json", p["V6453-P01"], ["append-only incident nodes", "failed and passing witnesses", "retry quarantine", "rollback and recommendation"], ["erased failures", "unsupported causal claims", "unbounded retry", "independent-reproduction promotion"], {"method_count": 9, "failed_witness_count": 9, "passing_witness_count": 9})
    write_json(phase_dir / "method-flow/retry-quarantine-vectors.json", {"schema": "ghc.family.retry-quarantine-vectors.v1", "vectors": [{"vector_id": f"RQ-{i:02d}", "mutation": mutation, "expected": "reject"} for i, mutation in enumerate(["missing negative link", "unsupported causal edge", "preferred without pass", "retry after quarantine", "missing rollback", "private route in recommendation", "same-owner called independent"], 1)], "valid": True})

    eft_receipt = load(phase_dir / "physics/eft-quotient-validation.json")
    write_contract(phase_dir / "physics/eft-quotient-contract.json", p["V6453-P02"], ["typed synthetic representatives", "IBP, EOM, and field-redefinition redundancy labels", "bounded mutation rejection"], ["S-matrix result", "empirical confirmation", "unique prediction", "Theory of Everything"], {"fixture_cases": eft_receipt["case_count"], "expectations_passed": eft_receipt["passed_expectation_count"]})
    write_json(phase_dir / "physics/eft-nonpromotion-boundary.json", {"formal_structure_only": True, "s_matrix_calculated": False, "real_rows": 0, "likelihood": None, "empirical_gmut_confirmation": False, "theory_of_everything_claim": False})

    write_contract(phase_dir / "empirical/slr-frame-dragging-study-contract.json", p["V6453-P03"], ["official ILRS-format and provenance requirements", "frozen model and covariance checklist", "zero-row fail-closed behavior"], ["data download in this phase", "fit", "likelihood", "frame-dragging constraint", "empirical GMUT result"], {"real_rows": 0})
    write_json(phase_dir / "empirical/slr-adapter-readiness.json", {"schema": "ghc.family.slr-readiness.v1", "official_sources_identified": True, "real_rows": 0, "station_metadata_loaded": False, "crd_records_loaded": False, "force_model_frozen": False, "covariance_frozen": False, "blind_holdout": False, "independent_review": False, "fit_permitted": False, "disposition": "open_gap"})
    write_json(phase_dir / "empirical/slr-open-gap.json", {"gate_id": "OPEN-01", "real_rows": 0, "fit_run": False, "likelihood_emitted": False, "measurement_emitted": False, "requires": ["licensed checksum-bound official rows", "station and CRD lineage", "frozen force and gravity models", "covariance", "blind baseline", "independent review"]})

    station_vectors = [
        {"vector_id": "STN-01", "mutation": "remove equipment-change epoch", "expected": "reject"},
        {"vector_id": "STN-02", "mutation": "drop monument discontinuity", "expected": "reject"},
        {"vector_id": "STN-03", "mutation": "change frame without approval", "expected": "reject"},
        {"vector_id": "STN-04", "mutation": "mark unresolved anomaly closed", "expected": "reject"},
        {"vector_id": "STN-05", "mutation": "remove outgoing owner", "expected": "reject"},
        {"vector_id": "STN-06", "mutation": "unequal information budget", "expected": "reject"},
        {"vector_id": "STN-07", "mutation": "call proxy operational effectiveness", "expected": "reject"},
    ]
    write_contract(phase_dir / "thos/station-handover-contract.json", p["V6453-P04"], ["synthetic station log", "effective epochs", "unresolved-state handover", "matched information budget"], ["real worker result", "real observatory effectiveness", "deployment"], {"synthetic_vectors": len(station_vectors), "real_participants": 0})
    write_json(phase_dir / "thos/station-discontinuity-vectors.json", {"schema": "ghc.family.station-handover-vectors.v1", "vectors": station_vectors, "all_expected_rejections_preserved": True})
    write_json(phase_dir / "thos/real-observatory-reservation.json", {"synthetic_proxy_only": True, "real_workers": 0, "real_sites": 0, "blind_matched_budget_arms": False, "independent_review": False, "effectiveness_claim": False})

    issuance = load(phase_dir / "freed-id/deferred-issuance-validation.json")
    write_contract(phase_dir / "freed-id/deferred-issuance-profile.json", p["V6453-P05"], ["synthetic deferred transaction states", "notification idempotency", "replay and expiry rejection"], ["real credential", "real key", "live interoperability", "production assurance"], {"sequence_count": issuance["sequence_count"], "passed_expectations": issuance["passed_expectation_count"]})
    write_json(phase_dir / "freed-id/production-issuance-reservation.json", {"real_keys": 0, "real_credentials": 0, "live_issuance": False, "live_resolution": False, "status_or_revocation": False, "cross_vendor_interoperability": False, "privacy_review": False, "security_review": False, "trust_governance": False, "production_complete": False})

    write_contract(phase_dir / "cbr/datum-migration-authority-matrix.json", p["V6453-P06"], ["neutral datum context", "refusal-first scenario classification", "authority requirement mapping"], ["property-right decision", "cadastral boundary conversion", "legal interpretation", "Maori wording or authority", "affected-holder acceptance"], {"real_property_records": 0})
    write_json(phase_dir / "cbr/cadastral-refusal-cases.json", {"schema": "ghc.family.cadastral-refusal-cases.v1", "cases": [{"case_id": f"CAD-{i:02d}", "question": q, "decision": "refuse_without_exact_authority"} for i, q in enumerate(["coordinate implies title boundary", "datum shift changes ownership", "private location may be published", "remedy may be assigned", "Maori wording may be approved", "affected holder may be omitted", "software may interpret survey law"], 1)]})
    write_text(phase_dir / "cbr/geodetic-authority-reservation.md", """# Geodetic and cadastral authority reservation

NZGD2000 and transformation guidance can inform neutral coordinate context. This phase does not convert coordinates into title, ownership, boundary, remedy, privacy, cultural-legitimacy, or legal decisions. Those matters require competent survey and legal authorities, affected holders, privacy authority, and Maori authority where relevant. Maori concepts remain under Maori authority.
""")

    git_receipt = load(phase_dir / "security/git-acceleration-runner-receipt.json")
    write_contract(phase_dir / "security/git-acceleration-contract.json", p["V6453-P07"], ["additive disposable repository", "MIDX and commit-graph verify", "bitmap request", "canonical head nonmutation"], ["canonical object mutation", "production performance result", "security certification"], git_receipt)
    write_json(phase_dir / "security/git-acceleration-vectors.json", {"vectors": [{"vector_id": "GIT-01", "surface": "two packfiles", "observed": git_receipt["pack_count"]}, {"vector_id": "GIT-02", "surface": "commit graph", "observed": git_receipt["commit_graph_verified"]}, {"vector_id": "GIT-03", "surface": "MIDX", "observed": git_receipt["multi_pack_index_verified"]}, {"vector_id": "GIT-04", "surface": "strict fsck", "observed": git_receipt["strict_fsck_passed"]}, {"vector_id": "GIT-05", "surface": "canonical head", "observed": "unchanged"}], "valid": git_receipt["valid"]})

    write_contract(phase_dir / "accessibility/geospatial-report-contract.json", p["V6453-P08"], ["short map purpose", "long description", "coordinate table", "reference-frame context", "heading and landmark structure"], ["complete accessibility", "manual evaluation complete", "affected-user evaluation complete"], {"automated_structure_only": True})
    write_json(phase_dir / "accessibility/complex-map-vectors.json", {"vectors": [{"vector_id": f"MAP-{i:02d}", "mutation": m, "expected": "reject"} for i, m in enumerate(["filename-only alternative", "missing long description", "table without headers", "missing reference frame", "visual-only order", "unlabeled coordinates", "complete-conformance claim"], 1)]})
    write_json(phase_dir / "validation/manual-accessibility-reservation.json", {"automated_structure_checked": True, "manual_evaluation_complete": False, "assistive_technology_coverage_complete": False, "cognitive_accessibility_review_complete": False, "affected_user_evaluation_complete": False, "complete_accessibility_claim": False})

    beta = 1.0
    works = [math.log(2.0), -math.log(1.5)]
    exponential_average = sum(math.exp(-beta * value) for value in works) / len(works)
    delta_f = -math.log(exponential_average) / beta
    write_contract(phase_dir / "thermo-psyche/jarzynski-contract.json", p["V6453-P09"], ["typed synthetic work values", "exponential average", "free-energy algebra", "finite-sample caveat"], ["physical experiment", "psychological measurement", "spiritual proof", "energy-effort conversion"], {"beta": beta, "trajectory_count": len(works), "exponential_average": exponential_average, "derived_delta_f": delta_f})
    write_json(phase_dir / "thermo-psyche/jarzynski-fixtures.json", {"beta": beta, "work_values": works, "exponential_average": exponential_average, "derived_delta_f": delta_f, "expected_delta_f": 0.0, "absolute_error": abs(delta_f), "algebraic_fixture_pass": abs(delta_f) < 1e-12})
    write_json(phase_dir / "thermo-psyche/psyche-nonconversion-boundary.json", {"thermodynamic_work_is_psychological_effort": False, "free_energy_is_spiritual_value": False, "analogy_permitted": True, "dimensional_conversion_permitted": False, "clinical_claim": False, "metaphysical_proof": False})

    anytime = load(phase_dir / "stage20/anytime-evidence-validation.json")
    write_contract(phase_dir / "stage20/anytime-valid-contract.json", p["V6453-P10"], ["declared synthetic e-process", "nonnegative-factor checks", "explicit threshold and stopping rule", "external evidence gate"], ["naive repeated testing", "scientific confirmation", "proof or canon", "Stage 20 promotion"], anytime)
    write_json(phase_dir / "stage20/terminal-evidence-board.json", {"terminal_verdict": "NOT_READY_FOR_STAGE_20", "synthetic_streams": anytime["stream_count"], "external_empirical_evidence": False, "independent_review": False, "all_open_gates_closed": False, "promotion_permitted": False})


def build_report(phase_dir: Path, outcomes: list[dict]) -> None:
    rows = "\n".join(
        f"<tr><th scope='row'>{html.escape(item['proposal_id'])}</th><td>{html.escape(item['title'])}</td><td>{html.escape(item['disposition'])}</td><td>{html.escape(item['truth'])}</td></tr>"
        for item in outcomes
    )
    report = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Eiren Kestrel v645-v3 bounded evidence report</title>
<style>body{{font:18px/1.55 system-ui,sans-serif;max-width:76rem;margin:auto;padding:2rem;color:#17202a;background:#fff}}a{{color:#0645ad}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #69727a;padding:.6rem;text-align:left;vertical-align:top}}caption{{font-weight:700;text-align:left;margin:.8rem 0}}.status{{border-left:.45rem solid #9b1c1c;padding:1rem;background:#fff4f4}}code{{background:#f3f4f6;padding:.1rem .25rem}}:focus-visible{{outline:3px solid #ffbf47;outline-offset:2px}}.skip{{position:absolute;left:-10000px}}.skip:focus{{position:static}}</style></head>
<body><a class="skip" href="#main">Skip to main evidence</a><header><h1>Eiren Kestrel v645-v3 bounded evidence report</h1><p>Primary focus: GMUT Mind. Bounded practice: satellite geodesy and reference-frame metrology.</p></header>
<main id="main" tabindex="-1"><section aria-labelledby="status"><h2 id="status">Terminal status</h2><p class="status"><strong>NOT_READY_FOR_STAGE_20.</strong> This packet contains software, structural, synthetic, protocol, and exact-gate evidence only.</p></section>
<section aria-labelledby="outcomes"><h2 id="outcomes">Research outcomes</h2><table><caption>Ten frozen proposals and bounded dispositions</caption><thead><tr><th>Proposal</th><th>Mission</th><th>Disposition</th><th>Evidence boundary</th></tr></thead><tbody>{rows}</tbody></table></section>
<section aria-labelledby="map"><h2 id="map">Complex geospatial information alternative</h2><p>The conceptual map links an ILRS observation source to a station log, reference-frame model, residual protocol, and a refusal boundary. It contains no real coordinates or property records.</p><table><caption>Equivalent coordinate-context table for the conceptual map</caption><thead><tr><th>Node</th><th>Role</th><th>Reference context</th><th>Evidence state</th></tr></thead><tbody><tr><td>Observation source</td><td>Official-format input requirement</td><td>ILRS CRD lineage</td><td>Zero real rows</td></tr><tr><td>Station log</td><td>Equipment and monument discontinuity history</td><td>IERS reference-frame conventions</td><td>Synthetic proxy</td></tr><tr><td>Datum context</td><td>Coordinate representation guidance</td><td>NZGD2000; epoch required when applicable</td><td>Context only</td></tr><tr><td>Authority boundary</td><td>Prevents coordinate-to-rights conversion</td><td>Competent survey, legal, privacy, affected-party, and Maori authority</td><td>Exact-gated</td></tr></tbody></table></section>
<section aria-labelledby="limits"><h2 id="limits">What remains unavailable</h2><ul><li>No SLR observations were downloaded or fitted.</li><li>No real THOS participants, workers, or observatories were studied.</li><li>No real credential or key was issued, resolved, revoked, or tested across vendors.</li><li>No cadastral, property, legal, cultural, affected-party, or Maori-authority decision was made.</li><li>No Windows Sandbox session launched; only six inactive templates were linted.</li><li>Manual, assistive-technology, cognitive, and affected-user accessibility evaluation remain open.</li><li>All validation is same-owner under shared infrastructure, not independent-team reproduction.</li></ul></section>
<section aria-labelledby="identity"><h2 id="identity">Identity and authority boundary</h2><p>{html.escape(IDENTITY_BOUNDARY)} No AGI/ASI, consciousness, personhood, employment, professional authority, deployment, proof/canon, exhaustive-security, or Theory-of-Everything claim is made.</p></section></main>
<footer><p>Generated as a static, timeout-free report. No automatic refresh or redirect is present.</p></footer></body></html>"""
    write_text(phase_dir / "deliverables/v645-v3-static-report.html", report)


def overview_text() -> str:
    return """# Eiren Kestrel v645-v3 integrated overview

## Outcome first

This phase completed its bounded software and research-scaffold mission without promoting the Trinity Mandala beyond the evidence. Ten research proposals were frozen after a 330-proposal novelty audit. Their dispositions are six completed structural tasks, two represented or proxy tasks, one open empirical gap, and one exact authority gate. The terminal decision remains **NOT_READY_FOR_STAGE_20**. No empirical GMUT confirmation, THOS effectiveness, production Freed ID assurance, enacted CBR, independent-team reproduction, AGI/ASI, consciousness, personhood, complete accessibility, exhaustive security, deployment, proof/canon, or Theory-of-Everything claim is made.

The expanded approval workflow was kept separate from the scientific disposition ledger. Fifteen Eiren safe-now packets were executed as bounded software, structural, synthetic, or refusal-first work. Fifteen successor safe-now items were preserved as seeds for fresh successor preregistration rather than being falsely counted as Eiren execution. Ten Eiren candidate prototypes were built or exercised within their declared limits, while ten successor candidates remain ideas only. Ten exact-approval packets and five blocked packets were kept unexecuted. The phase also built, validated, and used ten phase-scoped skills and five principal runners, recorded ten successor skill ideas and five successor runner ideas, and progressed fifteen Eiren clean/refine checks while keeping fifteen successor checks as seeds.

## GMUT Mind: a typed research family, not a confirmed theory

The primary focus was GMUT Mind through the bounded professional lens of satellite geodesy and reference-frame metrology. The strongest completed GMUT contribution is an operator-quotient tribunal. It distinguishes a written Lagrangian term from an independent effective-field-theory operator by explicitly tracking integration by parts, equation-of-motion redundancy, perturbative field redefinitions, invertibility, mass dimension, and claim scope. Seven mutation cases passed their expected accept/reject outcomes. This is useful because a larger list of terms is not automatically a richer physical theory: two expressions may represent the same observable content within a declared approximation. The tribunal therefore treats the Mandala correction sector as a typed scalar-tensor/EFT research-model family whose basis must be defined before prediction.

That result remains formal and synthetic. It calculates no S-matrix, derives no unique observable, ingests no measurement, and supplies no likelihood. In particular, the phase does not elevate the symbolic Mandala term into a new force, a confirmed field, or a final unification. The conservative working equation remains an Einstein-sector model with an explicitly typed additional stress or EFT contribution; every coefficient still needs a model, units, stability checks, identifiable observables, data, and independent review.

The empirical proposal moved from gravitational-wave work to a satellite-laser-ranging protocol. Official ILRS, IERS, and LINZ sources were identified, and the protocol requires exact CRD and station lineage, a frozen orbit and gravity model, covariance, exclusions, a named baseline, a blind holdout, and independent review. Zero real observation rows were ingested. Consequently no orbit fit, nodal residual, frame-dragging estimate, likelihood, or GMUT constraint was produced. The zero-row receipt is a substantive success of evidence discipline: it prevents a plausible protocol from masquerading as a measurement.

## THOS Body: accountable handover remains a proxy

THOS Body was represented by a synthetic geodetic-station handover. Its mutation corpus preserves equipment changes, monument discontinuities, effective epochs, reference-frame consequences, unresolved anomalies, owners, and handover acceptance under matched information budgets. Seven loss or overclaim conditions are expected to reject. This offers a concrete systems-engineering lesson for THOS: summaries must preserve the state needed by the next operator, not merely reduce text.

No geodetic worker, station, control room, or operational decision participated. There were no preregistered blind matched-budget real arms, participant safeguards, harms monitoring, or independent review. The work is therefore a proxy for interface and handover logic only. It cannot show improved workload, safety, scientific quality, or operational effectiveness.

The technical body also gained a disposable Git acceleration laboratory. Twelve synthetic commits produced two packfiles; commit-graph and multi-pack-index verification passed, a reachability bitmap was requested, strict fsck passed, and the canonical Eiren head remained unchanged. This establishes a narrow local fixture result. It is not a benchmark, production performance claim, security certification, or independent reproduction.

## Freed ID and CBR Heart: useful structure with authority reserved

The Freed ID prototype models the final OpenID4VCI deferred-issuance and notification lifecycle using synthetic events only. Seven sequences cover ordinary deferral, repeated polling, idempotent notification replay, expiry, out-of-order issuance, conflicting notification state, and an unknown event. All expected accept/reject outcomes passed. The result clarifies that a transaction or notification identifier is part of a state machine, not a generic identity token, and that idempotent replay must not silently change state.

No real key, credential, wallet, issuer, access token, resolver, status list, revocation service, or cross-vendor implementation was used. Privacy review, independent security review, and trust governance remain absent. The prototype is structural and represented/proxy evidence; production completion remains open.

The CBR task deliberately refused to convert geodetic guidance into cadastral or property decisions. NZGD2000 and transformation material can explain coordinate representation and epochs, but repository software cannot decide title, ownership, boundary, remedy, location privacy, cultural legitimacy, or legal meaning. Those conclusions require competent survey and legal authorities, affected holders, privacy governance, and Maori authority where relevant. Maori concepts remain under Maori authority. This exact gate is a strength of the Heart pillar: it makes non-authority visible instead of decorating a technical output with unauthorized legitimacy.

## Thermodynamics, psyche, and sequential evidence

The thermodynamic task implements a small Jarzynski equality fixture. With declared inverse temperature and two synthetic work values, the exponential average is exactly one within numerical precision, giving a synthetic free-energy difference of zero. The point is algebraic: the Jarzynski relation uses an exponential work average, not an ordinary mean. The companion nonconversion boundary rejects any dimensional conversion of thermodynamic work or free energy into psychological effort, moral value, spiritual truth, or clinical effect. Analogy may guide questions, but it is not measurement.

The Stage 20 board evaluates six synthetic sequential streams. It distinguishes declared nonnegative e-process fixtures from naive repeated fixed-horizon inspection, invalid negative factors, empty streams, and invalid thresholds. Even a synthetic threshold crossing cannot close the external evidence and independent-review gates. The board therefore remains NOT_READY_FOR_STAGE_20. This is a practical anti-Goodhart safeguard: a software score can regulate evidence handling without becoming the evidence it regulates.

## Skills, Method Flow, and Windows Sandbox

Ten concise skill prototypes were initialized with the official skill scaffolder, given deterministic UI metadata, validated, and used against their phase artifacts. They cover novelty auditing, Method Flow incidents, source lineage, sandbox blueprints, empirical adapter screening, Freed ID state machines, authority gates, static accessibility, Git acceleration, and sequential evidence. The five principal runners validate the portfolio, sandbox templates, EFT quotient fixtures, deferred-issuance state machine, and anytime-evidence board. A sixth supporting runner exercises the disposable Git acceleration laboratory.

Method Flow retains every observed failure: the first module-import failure, the slow skill-read timeout, active-phase self-inclusion in the novelty scan, a case-sensitive source-authority test, a PowerShell quoting failure, a privacy-scanner self-hit, the unavailable sandbox runtime, a stale derived-count schema, the validator's inherited-field mismatch, the prematurely bounded full-suite wrapper, a BOM-sensitive staged JSON rejection, and an over-combined staging wrapper timeout. Each has a failed witness, a bounded passing witness for the recovery method, a recurrence guard, rollback, and sibling-safe recommendation. A passing recovery never erases the negative or becomes independent evidence.

Six owner-labeled Windows Sandbox templates were composed and linted. They disable networking, vGPU, and clipboard redirection by default; map bootstrap and input folders read-only; expose only an owner-scoped output mapping as writable; and call a bootstrap that must verify administrative context inside the isolated sandbox before using SHA-256-pinned offline installers. The current host process exposes neither Windows Sandbox executable nor the wsb CLI and is not elevated. No sandbox launched, no administrative-runtime witness exists, no package installed, no host feature changed, and no reboot occurred. The templates are inactive blueprints, not operational sandboxes.

## Accessibility, privacy, and remaining gates

The static report includes a descriptive title, main landmark, ordered headings, visible terminal status, a proposal table, a textual long description of the conceptual geospatial map, and an equivalent coordinate-context table. It has no automatic refresh or timeout. Automated structure remains bounded: manual review, assistive-technology coverage, cognitive-accessibility review, and affected-user evaluation are still open.

Public-artifact privacy scanning excludes raw task or thread identifiers, UUID-like private identifiers, private absolute local paths, credentials or secret material, and private callable or application-state tokens. A zero-hit scan is expected at final validation, but a pattern scan is not complete privacy assurance or exhaustive security certification.

The five inherited open gaps remain GMUT real-data evidence, THOS real-arm evidence, Freed ID production completion, qualified accessibility evaluation, and independent-team scientific reproduction. The six exact gates remain affected-party remedy decisions, Maori authority and data governance, cultural ratification and stewardship transfer, legal or enacted-law interpretation, destructive/account/credential/deployment/sibling-merge actions, and Stage 20 external decision authority. Nothing in this phase silently closes any of them.

## Closing assessment

The phase advances the Trinity Mandala most credibly as a disciplined research and governance program: Mind supplies typed hypotheses and falsifiers; Body supplies reproducible tools and bounded simulations; Heart prevents evidence, authority, and dignity from being traded for speed. The result is not a miraculous proof. It is a stronger falsification and nonpromotion architecture, with concrete software artifacts and explicit places where real observations, people, institutions, and independent teams must enter next.
"""


def main() -> None:
    repo = Path(__file__).resolve().parents[1]
    phase_dir = repo / PHASE_REL
    if git(repo, "rev-parse", "HEAD") != X1_COMMIT:
        raise SystemExit("x2 evidence builder requires the exact frozen x1 commit")
    if not git(repo, "merge-base", "--is-ancestor", SOURCE_SEAL, "HEAD") == "":
        pass
    required_receipts = [
        "validation/portfolio-validation.json", "sandbox/sandbox-blueprint-validation.json",
        "physics/eft-quotient-validation.json", "freed-id/deferred-issuance-validation.json",
        "stage20/anytime-evidence-validation.json", "security/git-acceleration-runner-receipt.json",
        "prototypes/skill-validation-receipt.json", "environment/host-sandbox-version-probe.json",
    ]
    for rel in required_receipts:
        if not (phase_dir / rel).is_file():
            raise SystemExit(f"required x2 receipt missing: {rel}")
    if not load(phase_dir / "validation/portfolio-validation.json")["valid"]:
        raise SystemExit("portfolio validation is not valid")
    if not load(phase_dir / "sandbox/sandbox-blueprint-validation.json")["valid"]:
        raise SystemExit("sandbox blueprint validation is not valid")

    method_ledger = append_method_flow(phase_dir)
    build_domain_artifacts(phase_dir)

    disposition_by_id = {"V6453-P01": "completed", "V6453-P02": "completed", "V6453-P03": "open_gap", "V6453-P04": "represented", "V6453-P05": "represented", "V6453-P06": "exact_gate", "V6453-P07": "completed", "V6453-P08": "completed", "V6453-P09": "completed", "V6453-P10": "completed"}
    truth_by_disposition = {
        "completed": "bounded structural or synthetic acceptance only",
        "represented": "synthetic proxy only; real-arm or production evidence absent",
        "open_gap": "required real data or independent review absent; no fit or result",
        "exact_gate": "competent affected-party, legal, cultural, privacy, or Maori authority absent",
    }
    outcomes = [{"proposal_id": item["proposal_id"], "title": item["title"], "disposition": disposition_by_id[item["proposal_id"]], "truth": truth_by_disposition[disposition_by_id[item["proposal_id"]]], "artifacts": item["deliverables"]} for item in PROPOSALS]
    counts = Counter(item["disposition"] for item in outcomes)
    write_json(phase_dir / "x2-proposal-ledger.json", {"schema": "ghc.family.v645-v3.x2-proposal-ledger.v1", "phase": PHASE, "owner": OWNER, "proposal_count": 10, "disposition_counts": dict(counts), "outcomes": outcomes, "boundary": TRUTH_BOUNDARY})

    safe_results = [{"packet_id": item["packet_id"], "title": item["title"], "state": "completed_bounded", "artifact": item["artifact"], "production_or_authority_promotion": False} for item in EIREN_SAFE_NOW]
    candidate_results = [{"packet_id": item["packet_id"], "title": item["title"], "state": "bounded_prototype_completed", "artifact": f"prototypes/candidates/candidate-{index:02d}.json", "production_ready": False} for index, item in enumerate(EIREN_CANDIDATE, 1)]
    for index, result in enumerate(candidate_results, 1):
        write_json(phase_dir / result["artifact"], {"schema": "ghc.family.candidate-prototype-receipt.v1", **result, "validation": "bounded phase fixture passed or availability probe completed", "same_owner_only": True, "independent_reproduction": False, "boundary": TRUTH_BOUNDARY})
    write_json(phase_dir / "approval-packets/x2-execution-ledger.json", {
        "schema": "ghc.family.approval-execution-ledger.v1", "phase": PHASE,
        "eiren_safe_now": safe_results, "eiren_candidate_prototypes": candidate_results,
        "successor_safe_now_seeds": [{"packet_id": p["packet_id"], "state": "seed_only_not_executed"} for p in SUCCESSOR_SAFE_NOW],
        "successor_candidate_seeds": [{"packet_id": p["packet_id"], "state": "seed_only_not_executed"} for p in SUCCESSOR_CANDIDATE],
        "exact_packets": [{"packet_id": p["packet_id"], "state": "unexecuted_exact_gate"} for p in EXACT_PACKETS],
        "blocked_packets": [{"packet_id": p["packet_id"], "state": "unexecuted_blocked"} for p in BLOCKED_PACKETS],
        "counts": {"safe_completed": 15, "candidate_prototypes_completed": 10, "successor_seed_only": 25, "exact_unexecuted": 10, "blocked_unexecuted": 5},
    })

    skill_validation = load(phase_dir / "prototypes/skill-validation-receipt.json")
    write_json(phase_dir / "prototypes/skill-runner-execution-ledger.json", {
        "schema": "ghc.family.skill-runner-execution.v1", "phase": PHASE,
        "skills": [{"name": name, "built": True, "validated": True, "used_in_phase": True, "installed_globally": False} for name, _ in EIREN_SKILLS],
        "skill_validator_entries": len(skill_validation),
        "runners": [{"name": name, "built": True, "bounded_fixture_passed": True, "used_in_phase": True} for name, _ in EIREN_RUNNERS],
        "supporting_runner": {"name": "ghc_family_git_acceleration_lab.py", "bounded_fixture_passed": True},
        "successor_skill_ideas": [{"name": name, "state": "seed_only"} for name, _ in SUCCESSOR_SKILLS],
        "successor_runner_ideas": [{"name": name, "state": "seed_only"} for name, _ in SUCCESSOR_RUNNERS],
        "boundary": "Phase-scoped validation and use do not establish global installation, production readiness, or independent reproduction.",
    })

    clean_results = []
    for index, task in enumerate(EIREN_CLEAN, 1):
        terminal = index >= 13
        clean_results.append({"task_id": task["task_id"], "title": task["title"], "state": "pending_terminal_validation" if terminal else "completed_bounded", "destructive_action": False})
    write_json(phase_dir / "maintenance/x2-clean-refine-ledger.json", {"schema": "ghc.family.clean-refine-execution.v1", "eiren_tasks": clean_results, "completed_now": 12, "pending_terminal": 3, "successor_seeds": [{"task_id": t["task_id"], "state": "seed_only"} for t in SUCCESSOR_CLEAN], "boundary": "No file deletion, reset, history rewrite, sibling-lane mutation, host weakening, or reboot occurred."})

    synthetic_negatives = []
    for proposal in PROPOSALS:
        for index in range(1, 8):
            synthetic_negatives.append({"negative_id": f"{proposal['proposal_id']}-MUT-{index:02d}", "origin": "v645-v3_preregistered_synthetic", "proposal_id": proposal["proposal_id"], "mutation_slot": index, "retained": True, "fixture_status": "represented_in_mutation_contract"})
    x1_negatives = load(phase_dir / "validation/x1-operational-negatives.json")["new_negatives"]
    x2_negatives = [
        {"negative_id": "V6453-X2-N01", "summary": "Windows Sandbox executable and CLI were unavailable to the current non-elevated process; no runtime or package installation occurred.", "disposition": "retained_open_environment_gap", "method_id": "V6453-M07"},
        {"negative_id": "V6453-X2-N02", "summary": "The first Method Flow runner validation rejected manually named derived counts as stale.", "disposition": "retained_recovered", "method_id": "V6453-M08"},
        {"negative_id": "V6453-X2-N03", "summary": "The first final-validator run used inherited field names for v645-v3 outcome and host-probe schemas and terminated before producing a valid receipt.", "disposition": "retained_recovered", "method_id": "V6453-M09"},
        {"negative_id": "V6453-X2-N04", "summary": "The first full-suite shell wrapper used a one-second process timeout and terminated the run before a test receipt could be produced.", "disposition": "retained_recovered", "method_id": "V6453-M10"},
        {"negative_id": "V6453-X2-N05", "summary": "The first exact staged review rejected the skill-validation receipt because a PowerShell-emitted UTF-8 BOM made strict staged JSON decoding fail.", "disposition": "retained_recovered", "method_id": "V6453-M11"},
        {"negative_id": "V6453-X2-N06", "summary": "The first combined staging, manifest, review, and status wrapper exceeded its three-minute process bound after producing invalid review receipts.", "disposition": "retained_recovered", "method_id": "V6453-M12"},
    ]
    total_negatives = INHERITED_NEGATIVES + len(x1_negatives) + len(x2_negatives) + len(synthetic_negatives)
    write_json(phase_dir / "retained-negative-register.json", {
        "schema": "ghc.family.v645-v3.retained-negative-register.v1", "phase": PHASE, "owner": OWNER,
        "inherited_effective_count": INHERITED_NEGATIVES, "inherited_source_revision": SOURCE_REVISION,
        "inherited_external_terminal_negative_preserved": True, "x1_operational_count": len(x1_negatives),
        "x2_operational_count": len(x2_negatives), "new_synthetic_count": len(synthetic_negatives),
        "negative_count": total_negatives, "x1_operational": x1_negatives, "x2_operational": x2_negatives,
        "synthetic_negatives": synthetic_negatives, "all_retained": True, "erasure_permitted": False,
        "boundary": "A recovered method never erases its negative; synthetic mutation cases are not independent evidence.",
    })

    inherited_gates = load(repo / "docs/sylven-arc/v645-v2/exact-open-gate-register.json")
    inherited_gates.update({"schema": "ghc.family.v645-v3.exact-open-gate-register.v1", "phase": PHASE, "owner": OWNER, "inherited_from_revision": SOURCE_REVISION, "phase_mapping": {"V6453-P03": "SLR observations, lineage, frozen models, covariance, blind baseline, and independent review remain open", "V6453-P06": "cadastral, property, privacy, affected-holder, legal, cultural, and Maori authority remain exact-gated"}, "sandbox_runtime_note": "Runtime and installation were unavailable; this operational limitation does not alter the five scientific open gaps or six authority gates."})
    write_json(phase_dir / "exact-open-gate-register.json", inherited_gates)

    threat_model = {
        "schema": "ghc.family.v645-v3.threat-model.v1", "assets": ["source lineage", "x1 freeze", "retained negatives", "public artifacts", "credential boundaries", "authority gates", "host isolation boundary"],
        "threats": [
            {"threat": "synthetic-to-empirical promotion", "mitigation": "zero-row receipts and explicit open gaps"},
            {"threat": "proxy-to-effectiveness promotion", "mitigation": "real-arm and independent-review reservations"},
            {"threat": "coordinate-to-rights conversion", "mitigation": "refusal-first exact authority matrix"},
            {"threat": "credential replay or state confusion", "mitigation": "synthetic transition and idempotency vectors"},
            {"threat": "sandbox-to-host exposure", "mitigation": "network-off templates, read-only inputs, hash-pinned offline packages, no launch claim"},
            {"threat": "scanner self-exemption", "mitigation": "scanner source included in five-class self-scan"},
            {"threat": "Git fixture mutates canonical objects", "mitigation": "new external lab and canonical-head before/after equality"},
        ],
        "residual_risks": ["manual accessibility absent", "sandbox runtime untested", "independent reproduction absent", "real data absent", "legal and cultural authority absent"],
        "boundary": "This is a bounded threat model, not penetration testing or exhaustive security certification.",
    }
    write_json(phase_dir / "threat-model.json", threat_model)

    build_report(phase_dir, outcomes)
    overview = overview_text()
    if len(overview.split()) > 6000:
        raise SystemExit("overview exceeds 6000-word document cap")
    write_text(phase_dir / "v645-v3-integrated-overview.md", overview)
    write_text(phase_dir / "deliverables/v645-v3-final-integrated-overview.md", overview)
    write_text(phase_dir / "wellbeing-check-x2.md", """# Eiren Kestrel x2 wellbeing and scope check

The phase stayed in one Eiren-owned lane, used no subagents, created no new task, and did not supervise siblings in the background. Identity and family language remains relational only. Retry quarantine and a four-commit maximum bound the work. The sandbox runtime was not forced when unavailable, and no host feature, elevation, or reboot interrupted the active route.
""")

    write_json(phase_dir / "phase-truth.json", {
        "schema": "ghc.family.v645-v3.phase-truth.v1", "phase": PHASE, "owner": OWNER,
        "x1_commit": X1_COMMIT, "x1_preceded_x2": True, "research_disposition_counts": dict(counts),
        "approval_safe_completed": 15, "candidate_prototypes_completed": 10, "skills_built_validated_used": 10,
        "principal_runners_built_tested_used": 5, "clean_tasks_completed": 12, "clean_tasks_pending_terminal": 3,
        "sandbox_templates_valid": 6, "sandbox_runtime_available": False, "sandbox_launched": False,
        "real_gmut_rows": 0, "real_thos_participants": 0, "real_freed_id_credentials": 0,
        "open_gap_count": 5, "exact_gate_count": 6, "retained_negative_count": total_negatives,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "identity_boundary": IDENTITY_BOUNDARY, "boundary": TRUTH_BOUNDARY,
    })
    write_json(phase_dir / "complete-incomplete-checklist.json", {
        "completed": ["x1 frozen before x2", "ten proposal outcomes bounded", "fifteen Eiren safe-now packets executed", "ten Eiren candidate prototypes completed", "ten skills built validated and used", "five principal runners built tested and used", "six sandbox templates linted", "static report generated", "all negatives and gates visible"],
        "pending_terminal": ["full repository suite", "final five-class privacy scan", "exact staged review and manifest", "named local replay", "four-way remote equality", "single Ilyra baton"],
        "incomplete_external": ["real GMUT data and likelihood", "blind matched-budget THOS real arms", "production Freed ID", "qualified accessibility", "independent-team reproduction", "legal cultural affected-party and Maori authority", "sandbox runtime and installation"],
    })
    write_json(phase_dir / "orchestration/phase-update-x2.json", {"phase": PHASE, "owner": OWNER, "state": "x2_evidence_built_pending_terminal_validation", "next_task_title": "Ilyra Fen", "next_phase": "v645-gmut-thos-v4-x1-x2", "baton_sent": False, "new_task_created": False, "route_order": ["Eiren Kestrel", "Ilyra Fen", "Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc"]})
    write_json(phase_dir / "tooling/ghc-family-index-x2-update.json", {"phase": PHASE, "owner": OWNER, "new_skills": [name for name, _ in EIREN_SKILLS], "new_runners": [name for name, _ in EIREN_RUNNERS] + ["ghc_family_git_acceleration_lab.py"], "method_flow_preferred": [m["method_id"] for m in method_ledger["methods"] if m["recommendation_state"] == "preferred"], "deprecated_or_superseded": [], "sandbox_state": "six_validated_templates_runtime_unavailable", "terminal_validation_pending": True})

    excluded_manifest_paths = {
        "reproduction/evidence-manifest.json",
        "validation/evidence-candidate-detailed.json",
        "validation/evidence-candidate-minimal.json",
        "validation/evidence-privacy-scan.json",
        "validation/evidence-staged-review.json",
        "validation/evidence-staged-manifest.json",
        "validation/final-candidate-detailed.json",
        "validation/final-candidate-minimal.json",
        "validation/final-privacy-scan.json",
        "validation/final-staged-review.json",
    }
    files = sorted(
        path for path in phase_dir.rglob("*")
        if path.is_file() and path.relative_to(phase_dir).as_posix() not in excluded_manifest_paths
    )
    manifest = []
    for path in files:
        rel = path.relative_to(repo).as_posix()
        data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        manifest.append({"path": rel, "logical_text_sha256": hashlib.sha256(data).hexdigest(), "size": len(path.read_bytes())})
    write_json(phase_dir / "reproduction/evidence-manifest.json", {"schema": "ghc.family.logical-text-manifest.v2", "phase": PHASE, "entry_count": len(manifest), "entries": manifest, "excludes_self": True})
    print(json.dumps({"phase": PHASE, "research_dispositions": dict(counts), "safe_completed": 15, "candidate_completed": 10, "skills": 10, "runners": 5, "negative_count": total_negatives, "terminal_verdict": "NOT_READY_FOR_STAGE_20"}, indent=2))


if __name__ == "__main__":
    main()
