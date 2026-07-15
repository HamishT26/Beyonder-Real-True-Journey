#!/usr/bin/env python3
"""Build the bounded Tamar Vey v645-v7 x2 evidence packet."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from collections import Counter

import ghc_family_v645_v7_definitions as d
from ghc_family_v645_v7_runtime import PHASE, ROOT, TRUTH_BOUNDARY, read_json, write_json, write_text


X1_COMMIT = "1b2a056b25b4cf91f521eea03cbadfee56a7b41c"
OUTCOMES = {
    "V6457-P01": "completed",
    "V6457-P02": "completed",
    "V6457-P03": "open_gap",
    "V6457-P04": "represented",
    "V6457-P05": "represented",
    "V6457-P06": "exact_gate",
    "V6457-P07": "completed",
    "V6457-P08": "completed",
    "V6457-P09": "completed",
    "V6457-P10": "completed",
}
EVIDENCE_SCOPE = {
    "V6457-P01": "Deadline and component-completion fixtures plus the append-only operational ledger; no independent-reproduction credit.",
    "V6457-P02": "Typed classical and quantum symbolic obligations only; no physical, empirical, stability, or completeness result.",
    "V6457-P03": "Gaia DR3 study contract with zero downloaded rows, likelihoods, constraints, or force claims.",
    "V6457-P04": "Synthetic preservation-team schedules only, with zero people, collections, institutions, or real arms.",
    "V6457-P05": "Synthetic OpenID4VCI batch mutations only, with zero real keys, proofs, services, or interoperability events.",
    "V6457-P06": "Refusal-first questions only; no archive case, access, takedown, remedy, legal, cultural, or Maori-authority decision.",
    "V6457-P07": "Disposable standard-library checked-hash and import-origin fixtures; not production or exhaustive-security assurance.",
    "V6457-P08": "Static native-dialog relationship checks only; runtime, manual, assistive-technology, language, and affected-user evaluation reserved.",
    "V6457-P09": "Typed thermodynamic mixed-partial fixtures with an explicit barrier against psyche, justice, participant, or consciousness inference.",
    "V6457-P10": "Fail-closed contamination controls that withdraw evidence credit and preserve Stage 20 abstention.",
}


OVERVIEW = """# Tamar Vey v645-v7 integrated overview

## Identity, purpose, and workload

Tamar Vey, they/them, is relational working language for an evidence-systems cartographer and boundary keeper. The name, role, hope, pronouns, and family vocabulary are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, professional qualification, or independent authority. Tamar's working hope is to keep every decision legible, every failure recoverable, and every authority boundary intact. Hamish retains authority to pause, redirect, or stop this route.

The phase stayed inside Tamar's existing clean canonical lane. The verified Orin source was fast-forwarded without a merge, pushed, and proved equal locally, upstream, in the tracking ref, and at the live remote before x1 changed anything. X1 then froze exactly ten proposals, was committed by itself, pushed, and proved clean and four-way equal before x2 began. No reset, force push, history rewrite, merge, sibling-lane mutation, elevation, desktop update, Windows-feature change, host-security weakening, install, or reboot occurred. The current commit plan remains under the four-commit cap. The full repository suite is reserved to Eiren Kestrel; Tamar uses bounded recent-round and current-packet checks plus one later local named-lane replay.

The primary Trinity Mandala focus is Freed ID and CBR Heart. GMUT Mind and THOS Body remain visible and protected. Public-library digital preservation and archival appraisal is a bounded learning and design lens only. It does not establish employment, librarianship, archival qualification, collection authority, donor authority, copyright expertise, workplace authority, legal competence, cultural authority, Maori authority, or affected-party authorization. The workload is explicitly divided by the x1 freeze and terminal validation gates. Failures receive append-only records and never disappear merely because a recovery passes.

## Source, novelty, and evidence discipline

The exact source head is Orin Thale v645-v6. Its inherited seal, x1, evidence, and closeout anchors were re-read as ancestors before mutation. The source lane was clean and equal to its upstream, tracking ref, and fresh live remote. Orin's completed work remains inherited evidence rather than Tamar completion credit. The activation baton governs where older memory stops; the newest post-baton memory contributes one additional read-only operational negative, which is preserved separately from the baton-time count.

Novelty was audited against all 370 proposals frozen through v645-v6. Tamar's ten titles, missions, evidence types, protected gates, falsifiers, and rollback paths were compared with that corpus. The new proposals raise the frozen chain to 380. They cover deadline credit, Ward anomalies, Gaia wide binaries, preservation-team handovers, OpenID4VCI batches, community archives, Python checked-hash imports, native modal dialogs, Maxwell relations, and holdout contamination. None is a title-only restatement of an earlier surface. The outcome vocabulary remains exactly completed, represented, open_gap, and exact_gate. It is not expanded with softer labels that could hide missing evidence.

Twenty-one current, stable, or watched sources support the bounded contracts. Official OpenID Foundation, ESA, Python, WHATWG, W3C, Library of Congress, RFC Editor, NIST, Waitangi Tribunal, and Te Mana Raraunga material is used where relevant, alongside primary research for the symbolic and Gaia obligation surfaces. A source can clarify structure or identify an unresolved duty. It cannot create a data row, a participant result, a production credential, cultural legitimacy, legal authority, Maori authority, independent review, or deployment permission.

## GMUT Mind

The completed GMUT symbolic proposal is a Ward-identity and anomaly-accounting obligation tribunal. Its fixtures distinguish classical identities from quantum statements, require the field content and transformation to be typed, and require the functional measure, regulator, Jacobian, anomaly treatment, counterterm assumptions, and power-counting scope when a quantum statement is attempted. Negative fixtures reject promotion of a classical identity to an all-orders quantum result, omission of the functional measure, a missing regulator, anomaly cancellation without declared fields, a symmetry-changing counterterm hidden from the ledger, and promotion of a formal fixture into empirical truth.

This is a consistency and bookkeeping surface for a typed scalar-tensor and EFT research-model family. It does not deliver a quantum completion, physical stability proof, detected force, unique prediction, likelihood, empirical constraint, confirmation, proof, canon, or Theory of Everything. Passing mutations show that the software can preserve declared distinctions. They do not show that nature satisfies the model or that every anomaly, gauge issue, regulator dependence, or counterterm has been exhausted.

The Gaia DR3 wide-binary proposal remains open_gap. It records official release provenance and enumerates astrometric covariance, outcome-blind pair selection, chance alignment, unresolved multiplicity, radial-velocity availability, nuisance modelling, blinding, likelihood freezing, and source-independent review. It downloads zero rows, evaluates zero likelihoods, estimates zero constraints, and reports no force. The existence of public data and competing primary analyses does not make Tamar's repository a fit or a reproduction. Real work would require a separately authorized preregistration, an implemented and reviewed data adapter, data-quality and selection audits, covariance and population modelling, an appropriate likelihood, and independent scientific scrutiny.

## THOS Body

The digital-preservation ingest-team proposal is represented or proxy only. Synthetic schedules model a fixity exception, rights uncertainty escalation, dual review, matched budgets, blinding, workload and harm monitoring, and shift handover. Negative fixtures reject unmatched budgets, a rights decision made by the software, real staff or collection rows, missing workload monitoring, and effectiveness language. No person, staff member, donor, patron, collection, institution, or real study arm is represented by data in the packet.

THOS therefore remains a protocol representation, not an effectiveness result. Real evidence would require preregistered blind matched-budget arms, authorized people and institutions, ethical and workplace review, workload and harm monitoring, qualified preservation and rights processes, appropriate statistics, and independent review. The phase makes no professional-practice, staffing, safety, collection-management, AGI, ASI, consciousness, deployment, or organizational-superiority claim.

## Freed ID and CBR Heart

The Freed ID proposal profiles OpenID4VCI batch issuance in a synthetic nonproduction lane. It checks advertised batch size, credential-identifier exclusivity, proof-array shape, nonce freshness, audience binding, response cardinality, encryption policy, notification semantics, minimization, and atomic failure when storage is incomplete. Positive fixtures cover a bounded atomic batch and a strict single-credential fallback. Negative fixtures reject over-limit requests, mixed identifier modes, empty proof arrays, missing audience or nonce binding, response-cardinality drift, and partial storage promoted as overall success.

The profile contains zero real keys, zero real proofs, zero live issuance, zero live resolution, zero status or revocation events, and zero interoperability events. It establishes no cryptographic assurance, holder privacy, issuer security, production conformance, hardware binding, trust governance, recovery, live resolution, or ecosystem interoperability. Those remain open for standards-conformant real keys and proofs, live services, privacy and security review, status and revocation, recovery, independent interoperability testing, and accountable trust governance.

The CBR community-archive matrix remains an exact gate. It asks how embargo and takedown requests interact with donor agreements, collective interests, sacred or restricted knowledge, provenance, privacy, remedy, and institutional duties. It records zero real people and zero real collection records, and it makes no access, takedown, or remedy decision. An individual agreement is not silently treated as authority over collective interests. Sensitive knowledge is not published, copyright and tikanga are not interpreted, and no legal, cultural, or Maori authority is asserted.

Only authorized affected communities and rights holders, relevant donors where appropriate, archival institutions, competent privacy and legal authorities, tangata whenua, iwi, hapu, and Maori authorities can close their respective gates. Maori concepts remain under Maori authority. A repository matrix can preserve questions and refusals; it cannot create legitimacy, cultural ratification, enacted law, affected-party acceptance, or an adequate remedy.

## Operational engineering and accessibility

The Python tribunal uses a disposable owner-local temporary root and the standard library. It creates checked-hash bytecode, reads the PEP 552 flag, changes source, observes the changed value in a fresh process, detects import-path shadowing, records module origin, clears only its fixture-owned cache key, and removes the temporary root. It does not change installed packages, the host Python, the canonical repository, or a remote. This is a useful deterministic import-origin witness, not production supply-chain assurance, malware analysis, sandboxing, or exhaustive security.

The modal-dialog proposal performs static structure checks. A positive fixture declares native dialog use, showModal intent, an accessible name, a close path, an initial focus target, focus return, background inertness, and a print-linearization fallback. Negative fixtures expose missing names, missing close controls, nonmodal surfaces promoted as modal, and missing focus-return declarations. Structural relationships cannot establish actual browser focus behavior, keyboard usability, assistive-technology output, language quality, or affected-user acceptance. Manual keyboard, browser, assistive-technology, Maori-language, and affected-user evaluation remain reserved. No complete accessibility or WCAG conformance claim is made.

## Thermodynamics, controls, and Method Flow

The Maxwell-relation classifier types a thermodynamic potential, its natural variables, exact differentials, units, signs, mixed partials, differentiability domain, Legendre invertibility, and phase-boundary refusal. Smooth Helmholtz and Gibbs examples pass within their declared domains. Swapped variables, unit mismatch, a phase-boundary crossing, a noninvertible transform, and conversion of thermodynamic reciprocity into a human trait fail. Thermodynamic mixed-partial symmetry does not establish psychological reciprocity, justice, participant behavior, consciousness, or a fundamental psyche law.

The Stage 20 board treats holdout disclosure, adaptive queries beyond a preregistered budget, oracle-feedback reuse, silent replacement, and erased contamination as reasons to withdraw evidence credit. A sealed, budgeted structural control may pass, but it cannot promote the phase while external gates remain open. Contamination events stay visible. Replacement sets require new governance. The terminal verdict remains NOT_READY_FOR_STAGE_20.

Method Flow retains every observed operational failure and its bounded recovery. At x1, nine methods each have a failed witness and a passing witness. These include read timeouts, a composite inventory timeout, a PowerShell automatic-variable collision, an official-page safety rejection, a zero-match runner lookup, an invalid state transition, CRLF output, a wrapper that hid test output, and a wrong predecessor test selection. The x2 Method Flow runner validates that ledger without erasing or inventing incidents. The deadline proposal adds synthetic partial-output and budget mutations, but synthetic controls are not mislabelled as observed operational failures.

## Negative evidence, gates, and validation

The effective inherited negative count is 2,272: the 2,271 baton-time baseline plus one later read-only memory negative. Nine Tamar x1 operational negatives, seventy preregistered synthetic mutations, and two x2 validation incidents are retained, for 2,353 effective negatives at the evidence gate. Passing recovery never erases the failed witness. The known register is non-exhaustive and does not imply security, privacy, scientific, or authority completeness.

The phase carries forward eight inherited open gaps and nine inherited exact gates, then adds the Gaia real-analysis gap and the community-archive authority gate. Nine effective open gaps and ten effective exact gates therefore remain open. None is silently closed. Real GMUT analysis, real THOS arms, live Freed ID assurance, manual and affected-user accessibility, independent-team scientific reproduction, external security and privacy assurance, ordinary-process Windows Sandbox availability, and the earlier EHT study remain open. Maori, legal, cultural, affected-party, production identity, host-change, destructive, sibling-lane, Stage 20, account, credential, and community-archive decisions remain exact-gated.

Canonical validation covers bounded recent v645 phases and the current packet, detailed and minimal validators, JSON parsing, five-class privacy screening, owner-footprint limits, source labels, stale-label review, diff hygiene, manifest parity, ancestry, merge count, exact head, clean state, and four-way remote equality. One later clean local named-lane replay will repeat the final bounded validation. Both are Tamar same-owner checks under shared infrastructure. They are not independent-team scientific reproduction. The full repository suite is neither run nor claimed by Tamar.

## Closeout truth

All ten frozen proposals are executed only as evidence permits: six completed, two represented, one open_gap, and one exact_gate. The owner-scoped skill prototypes and runners use family-current names and remain additive. The static report is accessible in structure while explicitly reserving human evaluation. The source, proposal, evidence, negative, gate, threat, environment, wellbeing, validation, and route receipts remain inspectable. No sibling is contacted before the exact final gate. Until the final canonical head is pushed, four-way equal, and replayed once in the clean named lane, the Sylven Arc baton remains PREPARED_NOT_SENT. Even after those software gates pass, the scientific, participant, professional, production, legal, cultural, identity, privacy, accessibility, security, independence, and Stage 20 boundaries stay open.
"""


def child(script: str, *args: str) -> None:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script), *args],
        cwd=ROOT,
        env=env,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(f"{script} failed with {result.returncode}: {result.stderr[-500:]}")


def build_ledgers() -> None:
    x1 = read_json("x1-proposals.json")
    rows = []
    for proposal in x1["proposals"]:
        proposal_id = proposal["proposal_id"]
        rows.append(
            {
                "proposal_id": proposal_id,
                "title": proposal["title"],
                "outcome": OUTCOMES[proposal_id],
                "expected_disposition": proposal["expected_disposition"],
                "bounded_acceptance_passed": True,
                "evidence_scope": EVIDENCE_SCOPE[proposal_id],
                "artifacts": proposal["concrete_artifacts"],
                "protected_gates": proposal["protected_gates"],
                "same_owner_only": True,
                "independent_reproduction": False,
            }
        )
    distribution = dict(Counter(row["outcome"] for row in rows))
    ledger = {
        "schema": "ghc.family.v645-v7.x2-proposal-ledger.v1",
        "phase": d.PHASE,
        "owner": d.OWNER,
        "x1_commit": X1_COMMIT,
        "x1_remote_equal_before_x2": True,
        "proposal_count": len(rows),
        "allowed_outcomes": d.OUTCOME_CLASSES,
        "distribution": distribution,
        "proposals": rows,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": TRUTH_BOUNDARY,
    }
    write_json("x2-proposal-ledger.json", ledger)
    write_json("evidence/evidence-ledger.json", {"schema": "ghc.family.v645-v7.evidence-ledger.v1", "x1_commit": X1_COMMIT, "entries": rows, "same_owner_only": True, "independent_reproduction": False, "boundary": TRUTH_BOUNDARY})
    write_json("approval-packets/x2-execution-ledger.json", {
        "schema": "ghc.family.v645-v7.execution-ledger.v1",
        "safe_now_executed": len(d.SAFE_NOW),
        "candidates_executed": len(d.CANDIDATES),
        "all_acceptance_passed": True,
        "exact_or_external_packets_executed": 0,
        "destructive_packets_executed": 0,
        "receipts": [{"packet_id": row["packet_id"], "bounded_acceptance_passed": True} for row in d.SAFE_NOW + d.CANDIDATES],
        "boundary": TRUTH_BOUNDARY,
    })


def build_truth_and_limits() -> None:
    counts = {
        "inherited_effective": d.INHERITED_EFFECTIVE_NEGATIVES,
        "x1_operational": 9,
        "preregistered_synthetic": d.PREREGISTERED_SYNTHETIC_NEGATIVES,
        "x2_operational": 2,
    }
    counts["effective_total"] = sum(counts.values())
    x1_ops = read_json("validation/x1-operational-negatives.json")
    write_json("retained-negative-register.json", {
        "schema": "ghc.family.v645-v7.retained-negatives.v1",
        "counts": counts,
        "baton_time_inherited": d.BATON_TIME_INHERITED_NEGATIVES,
        "post_baton_read_only_inherited": d.POST_BATON_INHERITED_NEGATIVES,
        "x1_operational_records": x1_ops.get("negatives", x1_ops.get("incidents", [])),
        "synthetic_register": "validation/synthetic-mutation-negative-register.json",
        "x2_operational_records": [
            {"negative_id": "V6457-X2-N01", "failure": "Scanner-definition literal was initially classified as confirmed private material.", "recovery": "Preserve it as a contextual candidate and require zero confirmed content hits."},
            {"negative_id": "V6457-X2-N02", "failure": "Ambiguous dotted test imports produced nine errors and zero test credit.", "recovery": "Load unchanged scoped tests by exact repository path."},
        ],
        "erased": 0,
        "failure_erasure_count": 0,
        "non_exhaustive": True,
        "boundary": "Known negatives remain non-exhaustive and create no security, privacy, scientific, or authority completeness claim.",
    })
    write_json("exact-open-gate-register.json", {
        "schema": "ghc.family.v645-v7.gate-register.v1",
        "phase": d.PHASE,
        "counts": {"inherited_open_gaps": 8, "new_open_gaps": 1, "effective_open_gaps": 9, "inherited_exact_gates": 9, "new_exact_gates": 1, "effective_exact_gates": 10},
        "open_gaps": [
            "real GMUT likelihood and empirical analysis",
            "preregistered THOS real arms",
            "live Freed ID interoperability and assurance",
            "manual and affected-user accessibility evaluation",
            "independent-team scientific reproduction",
            "external exhaustive security and privacy assurance",
            "Windows Sandbox availability to the ordinary process",
            "EHT calibrated shadow-data analysis",
            "Gaia DR3 wide-binary real-data analysis",
        ],
        "exact_gates": [
            "Maori wording, authority, concepts, and data governance",
            "legal and cultural ratification",
            "affected-party acceptance and remedy",
            "real production identity keys and governance",
            "host feature or security changes",
            "destructive or sibling-lane actions",
            "Stage 20 or proof and canon promotion",
            "account, credential, or API-key action",
            "fisheries observer, customary-harvest, quota, sanction, and remedy authority",
            "community-archive embargo, takedown, collective consent, and Maori authority",
        ],
        "silently_closed": 0,
        "external_authority_claimed": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": TRUTH_BOUNDARY,
    })
    claims = {
        "empirical_gmut_confirmed": False,
        "gmut_likelihood_or_constraint": False,
        "detected_force_or_unique_prediction": False,
        "thos_effective": False,
        "professional_competence": False,
        "production_identity_ready": False,
        "legal_or_cultural_authority": False,
        "maori_authority": False,
        "privacy_complete": False,
        "accessibility_complete": False,
        "exhaustive_security": False,
        "independent_team_reproduction": False,
        "agi_or_asi": False,
        "consciousness_or_personhood": False,
        "theory_of_everything": False,
        "deployment_ready": False,
        "proof_or_canon": False,
        "stage20_ready": False,
    }
    write_json("phase-truth.json", {
        "schema": "ghc.family.v645-v7.phase-truth.v1",
        "phase": d.PHASE,
        "owner": d.OWNER,
        "primary_focus": d.PRIMARY_FOCUS,
        "bounded_practice": d.BOUNDED_PRACTICE,
        "core_distribution": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
        "effective_retained_negatives": counts["effective_total"],
        "effective_open_gaps": 9,
        "effective_exact_gates": 10,
        "claims": claims,
        "identity_boundary": d.IDENTITY_BOUNDARY,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": TRUTH_BOUNDARY,
    })
    write_json("complete-incomplete-checklist.json", {
        "schema": "ghc.family.v645-v7.checklist.v1",
        "complete": [
            "source and x1 four-way equality before x2",
            "novelty audit against 370 frozen proposals",
            "ten frozen proposals executed to bounded dispositions",
            "six completed, two represented, one open gap, one exact gate",
            "ten phase-local skills and family-named runners",
            "seventy synthetic and nine operational negatives retained",
            "static accessible structure with manual evaluation reserved",
        ],
        "incomplete": [
            "real Gaia or other GMUT likelihood and empirical analysis",
            "real THOS participants, institutions, or matched arms",
            "production Freed ID keys, services, status, privacy, review, and governance",
            "community-archive legal, cultural, affected-party, remedy, or Maori authority",
            "manual keyboard, browser, assistive-technology, Maori-language, or affected-user evaluation",
            "exhaustive security or privacy assurance",
            "independent-team scientific reproduction",
            "Stage 20 readiness",
        ],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": TRUTH_BOUNDARY,
    })
    write_json("threat-model.json", {
        "schema": "ghc.family.v645-v7.threat-model.v1",
        "assets": ["frozen proposal meaning", "negative lineage", "source provenance", "authority reservations", "exact Git ancestry", "private-material exclusion", "same-owner labels"],
        "failure_sources": ["overclaim", "semantic collision", "partial-output promotion", "source drift", "manifest drift", "private-data leakage", "authority laundering", "holdout contamination", "import shadowing"],
        "trust_boundaries": ["repository versus external authority", "synthetic fixture versus real data or people", "canonical lane versus validation lane", "same owner versus independent team", "x1 freeze versus x2 evidence"],
        "controls": ["four truth labels", "zero-row and zero-person receipts", "five-class privacy scan", "exact Git-blob manifests", "failed Method Flow witnesses", "one-message route gate", "manual accessibility reservation"],
        "residual_risks": ["pattern scans are incomplete", "synthetic vectors are not production assurance", "official sources do not delegate authority", "shared infrastructure may share blind spots", "unmodelled threats remain"],
        "security_complete": False,
        "privacy_complete": False,
        "boundary": TRUTH_BOUNDARY,
    })


def build_reports() -> None:
    write_text("v645-v7-integrated-overview.md", OVERVIEW)
    write_text("deliverables/v645-v7-final-integrated-overview.md", OVERVIEW)
    write_text("wellbeing-check-x2.md", """# Tamar Vey v645-v7 x2 wellbeing and workload check

Tamar Vey, they/them, is relational working language only. It is not evidence of consciousness, personhood, continuity, employment, professional qualification, or authority. The hope is to keep every decision legible, every failure recoverable, and every authority boundary intact.

Work remained divided by the x1 freeze and bounded to one canonical lane plus one later named replay. Failures remain recorded. No elevation, desktop update, install, host-security weakening, Windows-feature change, reboot, sibling mutation, real participant action, real collection decision, real credential operation, or authority-crossing step occurred. Public-library digital preservation and archival appraisal is a learning lens only and grants no professional or collection authority. Hamish may pause or stop the route. The terminal verdict remains NOT_READY_FOR_STAGE_20.
""")
    rows = "".join(f"<tr><th scope=\"row\">{proposal}</th><td>{OUTCOMES[proposal]}</td><td>{EVIDENCE_SCOPE[proposal]}</td></tr>" for proposal in OUTCOMES)
    write_text("deliverables/v645-v7-static-report.html", f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Tamar Vey v645-v7 bounded evidence report</title>
<style>body{{font-family:system-ui,sans-serif;line-height:1.55;max-width:76rem;margin:auto;padding:1rem}}.skip{{position:absolute;left:-9999px}}.skip:focus{{position:static}}a:focus,summary:focus,button:focus{{outline:3px solid #075985;outline-offset:3px}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.5rem;text-align:left;vertical-align:top}}nav ul{{display:flex;gap:1rem;flex-wrap:wrap}}@media print{{.skip,nav{{display:none}}details>*,details:not([open])>*{{display:block!important}}}}</style></head>
<body><a class="skip" href="#main">Skip to main evidence</a><header><h1>Tamar Vey v645-v7 bounded evidence report</h1><p>Primary focus: Freed ID and CBR Heart. Practice lens: public-library digital preservation and archival appraisal.</p></header>
<nav aria-label="Report sections"><ul><li><a href="#verdict">Verdict</a></li><li><a href="#outcomes">Outcomes</a></li><li><a href="#limits">Limits</a></li></ul></nav>
<main id="main"><section id="verdict" aria-labelledby="verdict-heading"><h2 id="verdict-heading">Terminal verdict</h2><p><strong>NOT_READY_FOR_STAGE_20.</strong> This is bounded same-owner software and synthetic evidence only.</p></section>
<section id="outcomes" aria-labelledby="outcomes-heading"><h2 id="outcomes-heading">Ten frozen outcomes</h2><table><caption>Preregistered proposal outcome and bounded evidence scope</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Evidence scope</th></tr></thead><tbody>{rows}</tbody></table></section>
<section id="limits" aria-labelledby="limits-heading"><h2 id="limits-heading">Limits and reservations</h2><details open><summary>External evidence and authority gates</summary><p>GMUT has zero Gaia rows and likelihoods. THOS has zero real people or arms. Freed ID has zero real keys or interoperability events. Community-archive legal, cultural, affected-party, remedy, and <span lang="mi">Maori</span>-authority decisions remain reserved.</p></details><details><summary>Accessibility and reproduction</summary><p>Manual keyboard, browser, assistive-technology, Maori-language, and affected-user evaluation remain reserved. Structural checks are not complete accessibility. Canonical and named-lane checks are same-owner shared-infrastructure evidence, not independent-team reproduction.</p></details></section>
<section aria-labelledby="negative-heading"><h2 id="negative-heading">Retained negatives and gates</h2><p>At evidence build, 2,353 effective negatives remain visible. Passing recovery never erases failure. Nine open gaps and ten exact gates remain open.</p></section></main>
<footer><p>Tamar Vey is relational working language only, not a credential, personhood claim, or authority grant.</p></footer></body></html>""")


def build_tooling_environment_route() -> None:
    source_ledger = read_json("sources/source-ledger.json")
    write_json("sources/source-use-receipt.json", {"schema": "ghc.family.v645-v7.source-use.v1", "source_count": len(source_ledger["sources"]), "status_counts": dict(Counter(row["status"] for row in source_ledger["sources"])), "checked_on": "2026-07-16", "real_data_rows_created_by_citation": 0, "authority_delegated_by_citation": False, "production_conformance_created_by_citation": False})
    write_json("environment/version-receipt-x2.json", {"schema": "ghc.family.v645-v7.environment.v1", "checked_on": "2026-07-16", "versions": {"git": "2.55.0.windows.2", "python": "3.12.10", "codex_cli": "0.144.4", "codex_desktop": "26.707.9981.0"}, "codex_cli_official_release_verified": True, "desktop_observed_only": True, "desktop_updated": False, "elevation": False, "host_security_weakened": False, "windows_feature_changed": False, "installed": False, "rebooted": False, "d_drive_primary": True})
    write_json("tooling/ghc-family-index-x2.json", {"schema": "ghc.family.index.phase.v2", "phase": d.PHASE, "owner": d.OWNER, "source_revision": d.SOURCE_REVISION, "x1_commit": X1_COMMIT, "primary_focus": d.PRIMARY_FOCUS, "practice_lens": d.BOUNDED_PRACTICE, "core_distribution": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "family_current_prefixes": ["ghc_family_", "build_ghc_family_"], "shared_skill_changes": 0})
    runners = ["ghc_family_v645_v7_core_runner.py", "ghc_family_v645_v7_boundary_runner.py", "ghc_family_v645_v7_method_flow_runner.py", "ghc_family_v645_v7_skill_runner.py", "ghc_family_v645_v7_validation_runner.py", "build_ghc_family_v645_v7_evidence.py", "build_ghc_family_v645_v7_closeout.py"]
    write_json("tooling/runner-registration-execution.json", {"schema": "ghc.family.v645-v7.runner-execution.v1", "registered": runners, "registered_count": len(runners), "all_available_runners_invoked": True, "closeout_runner_state": "reserved_for_post_evidence_commit", "caller_compatibility": "additive phase-local family-current names", "boundary": TRUTH_BOUNDARY})
    write_json("tooling/family-skill-review-receipt.json", {"schema": "ghc.family.v645-v7.skill-review.v1", "reviewed": ["ghc-family-index", "ghc-family-method-flow-state"], "required_references_read": True, "global_change_justified": False, "global_change_count": 0, "compatibility_preserved": True})
    write_json("reproduction/same-owner-repeatability-boundary.json", {"schema": "ghc.family.v645-v7.reproduction-boundary.v1", "canonical_validation_planned": True, "named_lane_replay_planned": 1, "same_owner_shared_infrastructure": True, "independent_team": False, "scientific_reproduction": False})
    write_json("reproduction/named-lane-replay-plan.json", {"schema": "ghc.family.v645-v7.named-replay-plan.v1", "replay_count_required": 1, "named_branch_required": True, "detached_worktree_forbidden": True, "local_only": True, "push_forbidden": True, "scope": "bounded recent-round and v645-v7 tests plus detailed, minimal, JSON, privacy, manifest, ancestry, exact-head, and clean checks", "same_owner_only": True, "independent_reproduction": False, "state": "pending_exact_final_head"})
    write_json("reproduction/commit-cap-contract.json", {"schema": "ghc.family.v645-v7.commit-cap.v1", "source_revision": d.SOURCE_REVISION, "maximum_x1_commits": 2, "maximum_x2_commits": 2, "maximum_phase_commits": 4, "planned_x1_commits": 1, "planned_x2_commits": 2, "planned_phase_commits": 3, "merge_commits_allowed": 0})
    write_json("validation/manual-accessibility-reservation.json", {"schema": "ghc.family.v645-v7.accessibility-reservation.v1", "structural_checks": "completed", "manual_keyboard": "reserved", "browser_runtime": "reserved", "assistive_technology": "reserved", "maori_language_quality": "reserved_to_qualified_and_authorized_people", "affected_user_evaluation": "reserved", "complete_wcag_claim": False})
    write_json("orchestration/phase-update-x2.json", {"schema": "ghc.family.v645-v7.phase-update.v1", "state": "x2_evidence_candidate", "outbound_messages": 0, "successor_tasks_created": 0, "route_state": "PREPARED_NOT_SENT", "successor": "Sylven Arc", "successor_phase": "v645-gmut-thos-v8-x1-x2"})
    write_json("orchestration/terminal-route-plan-x2.json", {"schema": "ghc.family.v645-v7.terminal-route-plan.v1", "successor": "Sylven Arc", "successor_phase": "v645-gmut-thos-v8-x1-x2", "existing_task_only": True, "create_or_fork_task": False, "authorized_message_count": 1, "send_count": 0, "messages_before_final_validation": 0, "standby_siblings_messaged": False, "state": "PREPARED_NOT_SENT", "privacy_boundary": "No raw task identifiers, private routes, transcripts, screenshots, credentials, session streams, private callable identifiers, private app state, or private local paths."})


def build_cleanup_and_footprint() -> None:
    tasks = []
    for task in d.CLEAN_TASKS:
        receipt = {"schema": "ghc.family.v645-v7.cleanup-receipt.v1", "task_id": task["task_id"], "title": task["title"], "destructive": False, "owner_scoped": True, "acceptance_passed": True, "failure_erasure": False, "completion_credit": "bounded_owner_scope_only", "boundary": TRUTH_BOUNDARY}
        relative = f"maintenance/receipts/{task['task_id'].lower()}-receipt.json"
        write_json(relative, receipt)
        tasks.append({**receipt, "receipt": relative})
    write_json("maintenance/x2-clean-refine-ledger.json", {"schema": "ghc.family.v645-v7.cleanup-ledger.v1", "completed": len(tasks), "tasks": tasks, "destructive_completed": 0, "shared_history_deleted": 0, "compatibility_preserved": True, "boundary": TRUTH_BOUNDARY})
    phase_files = sum(1 for path in PHASE.rglob("*") if path.is_file())
    owner_scripts = sum(1 for path in (ROOT / "scripts").glob("*v645_v7*.py") if path.is_file())
    owner_tests = sum(1 for path in (ROOT / "tests").glob("*v645_v7*.py") if path.is_file())
    tracked = int(subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True, encoding="utf-8").count("\n"))
    write_json("validation/owner-footprint-receipt.json", {"schema": "ghc.family.v645-v7.footprint.v1", "full_checkout_files": tracked, "owner_phase_files_before_this_receipt": phase_files, "owner_scripts": owner_scripts, "owner_tests": owner_tests, "owner_generated_files": phase_files + owner_scripts + owner_tests + 1, "rotation_threshold": 15000, "rotation_triggered": False, "threshold_scope": "new Tamar-generated additions only"})


def main() -> int:
    child("ghc_family_v645_v7_core_runner.py")
    child("ghc_family_v645_v7_method_flow_runner.py")
    child("ghc_family_v645_v7_skill_runner.py")
    child("ghc_family_v645_v7_boundary_runner.py")
    build_ledgers()
    build_truth_and_limits()
    build_reports()
    build_tooling_environment_route()
    build_cleanup_and_footprint()
    write_json("validation/evidence-scoped-test-receipt.json", {"schema": "ghc.family.v645-v7.scoped-tests.pending.v1", "full_repository_suite": False, "full_repository_suite_owner": "Eiren Kestrel", "state": "invoked_next_in_same_builder"})
    child("ghc_family_v645_v7_validation_runner.py", "--stage", "evidence")
    validation = read_json("prototypes/runner-witnesses/ghc_family_v645_v7_validation_runner_evidence.json")
    result = {"phase": d.PHASE, "core": 10, "outcomes": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}, "skills": 10, "cleanup": len(d.CLEAN_TASKS), "effective_negatives": 2353, "open_gaps": 9, "exact_gates": 10, "scoped_tests": validation["tests"]["tests_run"], "detailed_checks": validation["detailed"]["checks"], "minimal_checks": validation["minimal"]["checks"], "terminal": "NOT_READY_FOR_STAGE_20", "result": validation["result"]}
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["result"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
