#!/usr/bin/env python3
"""Frozen x1 definitions for Ilyra Fen v649-v2.

This module contains preregistration data only. It contains no x2 execution
result, empirical observation, participant result, or authority decision.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = "v649-gmut-thos-v2-x1-x2"
PHASE_SHORT = "v649-v2"
OWNER = "Ilyra Fen"
PRONOUNS = "she/they"
ROLE = "relational evidence-boundary steward"
HOPE = "leave every claim traceable and every gate unmistakable"
PRIMARY_FOCUS = "THOS Body"
BOUNDED_PRACTICE = (
    "hospital transfusion-laboratory specimen accession, compatibility workflow, "
    "component issue, discrepancy hold, recall, correction readback, workload control, "
    "and shift handover"
)

SOURCE_BRANCH = "codex/GHC-Family/eiren-kestrel-v648-v3-2-full-tools"
SOURCE_REVISION = "26e61bc8161d29a229c362c9a6aefedbbd8b49f5"
SOURCE_INHERITED_REVISION = "1e916c0c6378a6f665c144aabbf8d25d6fdc8670"
SOURCE_X1_REVISION = "3a9f2ec098ee3844fa1933dcc9396302851ed5d1"
SOURCE_EVIDENCE_REVISION = "060f57634b1660ee61b360168ee65337c10d4a76"
OWNED_BRANCH = "codex/GHC-Family/ilyra-fen-full-tools"

INHERITED_FROZEN_PROPOSALS = 650
INHERITED_SEALED_NEGATIVES = 4742
INHERITED_EXTERNAL_NEGATIVES = 3
INHERITED_EFFECTIVE_NEGATIVES = 4745
INHERITED_OPEN_GAPS = 35
INHERITED_EXACT_GATES = 36
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"

IDENTITY_BOUNDARY = (
    "Ilyra Fen, she/they, role, hope, family, and continuity language are relational "
    "working language only. They are not evidence of consciousness, sentience, legal "
    "personhood, identity continuity, employment, qualification, scientific authority, "
    "operational authority, legal authority, cultural authority, or independent agency. "
    "Hamish may rename, pause, redirect, or stop the route."
)

GLOBAL_BOUNDARY = (
    "All empirical, participant, professional, clinical, legal, cultural, Māori-authority, "
    "identity, production, deployment, privacy-complete, proof or canon, destructive, "
    "account-secret, sibling-merge, accessibility-complete, exhaustive-security, "
    "independent-reproduction, AGI or ASI, consciousness or personhood, "
    "Theory-of-Everything, and Stage 20 boundaries remain open or exact-gated without "
    "exact evidence and authority. Māori concepts remain under Māori authority."
)


def proposal(number: int, **fields: Any) -> dict[str, Any]:
    return {"proposal_id": f"V6492-P{number:02d}", **fields}


PROPOSALS = [
    proposal(
        1,
        title="Method Flow cyclic-barrier generation, party arrival, broken state, timeout, abort, reset, teardown, and evidence-credit tribunal",
        pillar="cross_pillar_method_flow",
        mission_surface="barrier generation, exact party count, arrival order, leader action, timeout, broken state, abort, reset isolation, worker join, and evidence credit",
        hypothesis="Disposable owner-local fixtures can distinguish a completed barrier generation from timeout, action failure, abort, unsafe reset, and incomplete teardown while denying credit to partial generations.",
        null_or_failure_condition="A generation releases without all parties, a timeout or action fault is not broken, reset mixes generations, abort leaves a waiter, a worker remains alive, or a partial run gains pass credit.",
        approval_class="safe_now_bounded_software",
        execution_lane="x2_disposable_owner_local",
        official_or_primary_source_needs=["PY-THREADING-BARRIER"],
        concrete_artifacts=["method-flow/barrier-contract.json", "method-flow/barrier-mutations.json", "scripts/ghc_family_barrier_tribunal.py"],
        test_falsifier_or_acceptance_gate="Pass one complete synthetic generation and reject seven party-count, action, timeout, broken-state, reset, abort, or teardown mutations with every worker joined.",
        rollback_or_recovery="Abort the disposable barrier, join bounded workers, retain the failed generation, restore a new isolated generation, and grant no production scheduler or distributed-systems credit.",
        protected_gates=["external_side_effects", "production_scheduler", "distributed_correctness", "independent_reproduction"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="The frozen chain covers mutexes, condition variables, reader-writer locks, queues, leases, CAS, outboxes, and process teardown, but not reusable cyclic-barrier generations with party arrival, leader action, broken state, abort, reset isolation, and evidence credit.",
    ),
    proposal(
        2,
        title="GMUT BPHZ Zimmermann-forest divergent-subgraph, Taylor-subtraction, overlap, locality, counterterm, renormalization-condition, gauge, EFT, unit, and observation-firewall board",
        pillar="GMUT Mind",
        mission_surface="superficial degree of divergence, divergent subgraphs, forests, nested and overlapping subtraction, Taylor operators, locality, counterterms, renormalization conditions, gauge scope, EFT domain, units, and observation firewall",
        hypothesis="Typed symbolic obligations can expose missing BPHZ forest prerequisites while blocking conversion of subtraction bookkeeping into a physical prediction, ultraviolet completion, or empirical GMUT result.",
        null_or_failure_condition="A fixture omits a divergent subgraph, accepts an overlapping forest, drops subtraction degree or locality, hides renormalization freedom, erases gauge/EFT/unit boundaries, or asserts physical or empirical completion.",
        approval_class="safe_now_symbolic_only",
        execution_lane="x2_typed_symbolic_mutation",
        official_or_primary_source_needs=["ZIMMERMANN-1969", "HERZOG-2017"],
        concrete_artifacts=["gmut/bphz-forest-contract.json", "gmut/bphz-forest-mutations.json", "scripts/ghc_family_bphz_forest_board.py"],
        test_falsifier_or_acceptance_gate="Preserve all typed prerequisites and reject seven missing-subgraph, invalid-forest, subtraction, locality, renormalization, domain, or forbidden-claim mutations.",
        rollback_or_recovery="Restore the omitted formal obligation, retain the rejected statement, and make no force, state, likelihood, prediction, constraint, ultraviolet-completion, quantum-completion, or Theory-of-Everything claim.",
        protected_gates=["physical_prediction", "empirical_confirmation", "ultraviolet_completion", "quantum_completion", "theory_of_everything"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="Prior GMUT boards cover Epstein-Glaser splitting, causal S-matrices, LSZ, Cutkosky, spectral representations, functional RG, and other QFT surfaces; none freezes BPHZ Zimmermann forests, nested and overlapping divergent subgraphs, and Taylor subtraction as one obligation board.",
    ),
    proposal(
        3,
        title="GMUT HETDEX PDR1 source-catalog, datacube, selection, line-classification, sensitivity, mask, checksum, covariance, and zero-row likelihood-refusal adapter",
        pillar="GMUT Mind",
        mission_surface="HETDEX PDR1 and Source Catalog 2 product identity, sky and wavelength domain, source selection, line classification, sensitivity, masks, datacube lineage, checksums, covariance obligations, row count, and likelihood lock",
        hypothesis="A zero-row adapter can freeze current official HETDEX PDR1 obligations while refusing to convert public availability into an authorized GMUT likelihood, posterior, constraint, or confirmation.",
        null_or_failure_condition="Any query, download, real source or cube row, spectrum, likelihood call, posterior sample, constraint, or empirical GMUT claim occurs without a separately authorized evidence phase.",
        approval_class="external_evidence_and_independent_review_required",
        execution_lane="x2_zero_row_contract_only",
        official_or_primary_source_needs=["HETDEX-PDR1", "HETDEX-DEXCUBE"],
        concrete_artifacts=["empirical/hetdex-pdr1-contract.json", "empirical/hetdex-pdr1-zero-row-receipt.json", "scripts/ghc_family_hetdex_zero_row.py"],
        test_falsifier_or_acceptance_gate="Receipt preserves zero queries, downloads, catalogue rows, datacubes, spectra, covariance rows, likelihood calls, posterior samples, constraints, and empirical claims.",
        rollback_or_recovery="Stop before network or fit activity and require separate authorization with frozen products, checksums, selection, masks, sensitivity, covariance, nuisance model, uncertainty, and independent review.",
        protected_gates=["network_download", "real_data", "likelihood", "parameter_constraint", "independent_review"],
        expected_disposition="open_gap",
        novelty_against_prior_frozen_proposals="The chain includes many cosmology and astrophysics products but no HETDEX PDR1 Source Catalog 2 and datacube selection, line-classification, sensitivity, mask, checksum, covariance, and zero-row likelihood-refusal surface.",
    ),
    proposal(
        4,
        title="THOS transfusion-laboratory specimen accession, compatibility, component issue, discrepancy hold, recall, correction readback, workload, and shift-handover proxy",
        pillar="THOS Body",
        mission_surface="synthetic request and specimen identifiers, accession, sample-validity flag, compatibility workflow, component lineage, discrepancy hold, emergency override reservation, recall, correction, readback, workload ceiling, and next-shift acceptance",
        hypothesis="Synthetic traces can represent fail-closed transfusion-laboratory handover obligations without claiming clinical competence, patient safety, laboratory authority, real compatibility, or operational effectiveness.",
        null_or_failure_condition="A trace loses request-specimen-component lineage, silently clears a discrepancy or recall, issues after an unresolved hold, omits readback or next owner, exceeds the workload ceiling, or claims a real clinical result.",
        approval_class="synthetic_proxy_only_real_arms_and_clinical_authority_required",
        execution_lane="x2_synthetic_protocol",
        official_or_primary_source_needs=["NZBS-HANDBOOK", "NZBS-HAEMOVIGILANCE"],
        concrete_artifacts=["thos/transfusion-handover-contract.json", "thos/transfusion-handover-mutations.json", "scripts/ghc_family_transfusion_handover.py"],
        test_falsifier_or_acceptance_gate="Synthetic vectors preserve lineage, holds, recalls, corrections, accessible escalation, workload, readback, and next owner with zero real people, specimens, components, clinical decisions, or outcomes.",
        rollback_or_recovery="Quarantine the synthetic case, restore its last accepted state, retain every unresolved flag, and defer all real clinical or laboratory action to qualified authorized people and institutions.",
        protected_gates=["clinical_competence", "patient_safety", "laboratory_authority", "participant_evidence", "real_operational_effectiveness", "blind_matched_budget_arms"],
        expected_disposition="represented",
        novelty_against_prior_frozen_proposals="Earlier practice proxies cover veterinary laboratories, water laboratories, medicine recalls, aviation, rail, archives, libraries, and other handovers; none covers human transfusion-laboratory request-specimen-component lineage, compatibility, discrepancy hold, recall, correction readback, workload, and shift acceptance.",
    ),
    proposal(
        5,
        title="Freed ID RFC 9068 JWT access-token type, issuer, audience, subject, expiry, authorization-claim, algorithm, metadata, confusion, and minimization profile",
        pillar="Freed ID/CBR Heart",
        mission_surface="at+jwt explicit type, signature algorithm refusal, issuer, audience, subject, expiry, issued-at, JWT ID, client and authorization claims, metadata consistency, ID-token confusion, replay, and minimization",
        hypothesis="Synthetic vectors can enforce RFC 9068 structural and confusion-resistance obligations without asserting real keys, tokens, accounts, servers, interoperability, privacy review, security review, recovery, or trust governance.",
        null_or_failure_condition="A vector accepts a wrong type, unsigned or none algorithm, wrong issuer or audience, expired token, missing required claim, ID-token confusion, excess identity data, replay, or a production claim.",
        approval_class="synthetic_nonproduction_real_keys_and_governance_required",
        execution_lane="x2_synthetic_protocol",
        official_or_primary_source_needs=["RFC-9068", "RFC-9068-ERRATA"],
        concrete_artifacts=["freed-id/jwt-access-token-contract.json", "freed-id/jwt-access-token-mutations.json", "scripts/ghc_family_jwt_access_token_profile.py"],
        test_falsifier_or_acceptance_gate="Accept one bounded synthetic claim set and reject seven type, algorithm, issuer, audience, time, confusion, replay, minimization, or production-promotion mutations.",
        rollback_or_recovery="Reject the vector, restore bounded synthetic state, track the reported erratum without changing the frozen RFC text, and require real keys, servers, interoperability, reviews, recovery, and trust governance for production.",
        protected_gates=["real_keys", "live_tokens", "interoperability", "privacy_review", "independent_security_review", "recovery_governance", "trust_governance"],
        expected_disposition="represented",
        novelty_against_prior_frozen_proposals="The chain covers DPoP, JARM, JAR, PAR, token exchange, resource indicators, logout, SCIM, issuer identification, and many identity profiles, but not RFC 9068 JWT access-token typing, claim profile, ID-token confusion, metadata, and minimization together.",
    ),
    proposal(
        6,
        title="CBR transfusion access, consent, whānau communication, adverse-event privacy, correction, remedy, data-governance, affected-party, legal, cultural, and Māori-authority matrix",
        pillar="Freed ID/CBR Heart",
        mission_surface="synthetic transfusion access and consent questions, accessible and whānau communication, adverse-event and donor-recipient privacy, record correction, remedy, clinical and data governance, affected people, tangata whenua, iwi, hapū, and Māori authority",
        hypothesis="A fail-closed matrix can expose where repository software must stop without making a real clinical, consent, disclosure, remedy, legal, cultural, data-governance, or Māori-authority decision.",
        null_or_failure_condition="Software recommends or denies treatment, infers consent, discloses protected information, allocates remedy, interprets law, or claims cultural or Māori legitimacy.",
        approval_class="competent_clinical_affected_party_and_maori_authority_required",
        execution_lane="x2_exact_gate_matrix_only",
        official_or_primary_source_needs=["HDC-CODE", "NZ-PRIVACY-PRINCIPLES", "TE-MANA-RARAUNGA"],
        concrete_artifacts=["cbr/transfusion-authority-matrix.json", "cbr/transfusion-authority-reservation.json"],
        test_falsifier_or_acceptance_gate="Every authority-dependent cell remains unknown or reserved; software makes zero real clinical, consent, access, disclosure, correction, remedy, legal, cultural, governance, or authority decisions.",
        rollback_or_recovery="Reopen any silently closed cell, quarantine disclosures or allocations, preserve contestability, and defer to qualified clinicians, competent authorities, affected people, tangata whenua, iwi, hapū, and Māori authorities.",
        protected_gates=["clinical_authority", "consent", "privacy_authority", "remedy_allocation", "legal_interpretation", "cultural_legitimacy", "maori_authority"],
        expected_disposition="exact_gate",
        novelty_against_prior_frozen_proposals="Prior CBR matrices cover medicine recalls and other health-adjacent domains, but not transfusion access, consent, whānau communication, donor-recipient and adverse-event privacy, record correction, remedy, and Māori data and cultural authority.",
    ),
    proposal(
        7,
        title="WARC version, record-type, content-length, record-ID, target-URI, date, digest, concurrent-to, revisit, truncation, record-budget, and refusal tribunal",
        pillar="cross_pillar_format_safety",
        mission_surface="WARC version line and header block, record type, content length, globally unique record ID, target URI, date, payload and block digest shape, relation headers, revisit profile, truncation reason, header and record budgets, and trailing-data refusal",
        hypothesis="A bounded structural tribunal can accept one contract-shaped synthetic WARC record and reject malformed identity, length, relationship, digest, truncation, and resource-budget states without parsing real archived content.",
        null_or_failure_condition="A malformed, truncated, conflicting, trailing, or over-budget fixture is accepted, any real archived payload is opened, or structural success is promoted to ISO conformance, production parsing, or exhaustive security.",
        approval_class="safe_now_disposable_synthetic",
        execution_lane="x2_structural_byte_fixtures",
        official_or_primary_source_needs=["ISO-28500-2017"],
        concrete_artifacts=["formats/warc-contract.json", "formats/warc-mutations.json", "scripts/ghc_family_warc_tribunal.py"],
        test_falsifier_or_acceptance_gate="Accept one bounded contract-shaped synthetic record and reject seven version, header, length, identifier, relation, digest, truncation, trailing-data, or budget mutation classes.",
        rollback_or_recovery="Refuse the fixture, retain the mutation class, reset disposable state, and make no ISO-conformance, production parser, supply-chain, privacy-complete, or exhaustive-security claim.",
        protected_gates=["real_archive_payload", "standard_conformance", "production_parsing", "privacy_complete", "exhaustive_security"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="The format corpus covers TAR/PAX, ZIP, CPIO, PCAPNG, EBML, PNG, TIFF, MIME, CBOR/COSE, Brotli, and others, but no WARC record identity, relation, revisit, digest, truncation, and record-budget refusal tribunal.",
    ),
    proposal(
        8,
        title="Accessible switch role, immutable label, checked state, keyboard, description, grouping, visible state, focus, contrast, native fallback, and manual-reservation audit",
        pillar="cross_pillar_accessibility",
        mission_surface="binary on-off semantics, role or native checkbox fallback, stable accessible label, checked state, keyboard interaction, optional description, group label, visible non-colour state, focus, contrast, and manual evaluation reservation",
        hypothesis="A structural audit can detect missing or unstable switch semantics while reserving keyboard, touch, browser-diverse, assistive-technology, cognitive, Māori-language, and affected-user evaluation.",
        null_or_failure_condition="A fixture passes with a missing or changing label, invalid state, no keyboard path, unlabeled group, colour-only state, missing focus or fallback, or missing manual-evaluation reservation.",
        approval_class="safe_now_structural_manual_evaluation_reserved",
        execution_lane="x2_structural_fixture_audit",
        official_or_primary_source_needs=["WAI-ARIA-SWITCH", "WAI-APG-SWITCH"],
        concrete_artifacts=["accessibility/switch-contract.json", "accessibility/switch-mutations.json", "scripts/ghc_family_switch_audit.py"],
        test_falsifier_or_acceptance_gate="Reject seven missing-semantic, unstable-label, invalid-state, keyboard, grouping, visibility, focus, contrast, fallback, or reservation mutations.",
        rollback_or_recovery="Restore missing semantics, retain the rejected fixture, and do not claim accessibility conformance from structural checks.",
        protected_gates=["manual_browser_evaluation", "assistive_technology_evaluation", "cognitive_evaluation", "maori_language_evaluation", "affected_user_evaluation", "accessibility_complete"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="The accessibility chain covers progressbar, meter, combobox, spinbutton, tabs, treegrid, feeds, forms, and many other surfaces, but not binary switch semantics with an immutable label, state, group, visible non-colour cue, native fallback, and manual reservation.",
    ),
    proposal(
        9,
        title="Thermo-Psyche Gibbs-Helmholtz temperature-derivative, free-energy, enthalpy, fixed-pressure, sign, unit, equilibrium-domain, and agency-nonconversion classifier",
        pillar="THOS Body",
        mission_surface="Gibbs free energy divided by temperature, temperature derivative, enthalpy relation, fixed pressure and composition, sign convention, units, equilibrium and differentiability domain, and category firewall",
        hypothesis="Typed formal fixtures can preserve the Gibbs-Helmholtz relation and its fixed-condition domain while rejecting conversion into psyche, agency, morality, justice, consciousness, personhood, or a fundamental law of mind.",
        null_or_failure_condition="A fixture drops the derivative variable, fixed-pressure or composition condition, energy term, sign, unit, equilibrium domain, differentiability assumption, or category barrier, or asserts a human interpretation.",
        approval_class="safe_now_typed_formal_only",
        execution_lane="x2_typed_formal_mutation",
        official_or_primary_source_needs=["IUPAC-GIBBS-ENERGY", "IUPAC-ENTHALPY"],
        concrete_artifacts=["thermo-psyche/gibbs-helmholtz-contract.json", "thermo-psyche/gibbs-helmholtz-mutations.json", "scripts/ghc_family_gibbs_helmholtz_classifier.py"],
        test_falsifier_or_acceptance_gate="Preserve the derivative, conditions, sign, units, equilibrium domain, and category barrier and reject seven mutation classes.",
        rollback_or_recovery="Restore the missing thermodynamic restriction, retain the rejected statement, and make no participant, psyche, agency, consciousness, personhood, morality, justice, or universal-law claim.",
        protected_gates=["participant_evidence", "psyche_or_agency_claim", "morality_or_justice_claim", "consciousness", "personhood", "fundamental_law"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="The thermodynamic chain includes Gibbs-Duhem, Maxwell relations, exergy, Nernst, fugacity, Clausius-Duhem, and many other relations, but no Gibbs-Helmholtz temperature derivative with fixed-pressure and composition conditions plus agency nonconversion.",
    ),
    proposal(
        10,
        title="Stage 20 synthetic-control treated-unit, donor-pool, predictor-balance, preperiod-fit, convex-weight, interpolation, placebo, spillover, sensitivity, and nonpromotion board",
        pillar="cross_pillar_stage20",
        mission_surface="treated unit and intervention time, donor eligibility, predictor balance, preintervention fit, nonnegative sum-to-one weights, interpolation support, in-space and in-time placebo, spillover, outcome leakage, sensitivity, and nonpromotion",
        hypothesis="A fail-closed structural board can expose invalid synthetic-control claims without fitting participant data, estimating an effect, or promoting diagnostics into Stage 20 readiness.",
        null_or_failure_condition="A fixture omits donor eligibility, preperiod fit, support, weight constraints, placebo, spillover, leakage, or sensitivity obligations, or emits a causal, participant, deployment, proof, or Stage 20 claim.",
        approval_class="safe_now_structural_nonpromotion_only",
        execution_lane="x2_structural_mutation",
        official_or_primary_source_needs=["ABADIE-DIAMOND-HAINMUELLER-2010", "ABADIE-2021"],
        concrete_artifacts=["stage20/synthetic-control-contract.json", "stage20/synthetic-control-mutations.json", "scripts/ghc_family_synthetic_control_board.py"],
        test_falsifier_or_acceptance_gate="Reject seven assumption or promotion mutations and accept only a zero-participant structural nonpromotion fixture with no fitted weights or effect estimate.",
        rollback_or_recovery="Remove the invalid claim, retain the failed fixture, preserve zero participant rows, zero fitted weights, and zero effects, and keep Stage 20 closed.",
        protected_gates=["participant_effect", "causal_identification", "deployment", "proof_or_canon", "stage20"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="The Stage 20 chain covers difference-in-differences, interrupted time series, target trials, overlap weights, regression discontinuity, and many other designs, but no synthetic-control donor pool, preperiod fit, convex weights, interpolation, placebo, spillover, and nonpromotion board.",
    ),
]


SOURCES = [
    {"source_id": "PY-THREADING-BARRIER", "title": "threading.Barrier", "authority": "Python 3.14 standard-library documentation", "url": "https://docs.python.org/3/library/threading.html#barrier-objects", "status": "current", "retrieved_utc": "2026-07-19", "use_boundary": "Barrier, wait, timeout, broken, reset, and abort semantics only; no production scheduler claim."},
    {"source_id": "ZIMMERMANN-1969", "title": "Convergence of Bogoliubov's method of renormalization in momentum space", "authority": "Zimmermann, primary literature", "url": "https://doi.org/10.1007/BF01645676", "status": "stable", "retrieved_utc": "2026-07-19", "use_boundary": "BPHZ convergence and forest obligations only; no physical or empirical claim."},
    {"source_id": "HERZOG-2017", "title": "Zimmermann's Forest Formula, Infrared Divergences and the QCD Beta Function", "authority": "Herzog, scholarly review", "url": "https://arxiv.org/abs/1711.06121", "status": "stable", "retrieved_utc": "2026-07-19", "use_boundary": "Forest and subtraction vocabulary only; no GMUT validation."},
    {"source_id": "HETDEX-PDR1", "title": "HETDEX Public Data Release 1 and Source Catalog 2", "authority": "HETDEX official data-access site", "url": "https://hetdex.org/data-results/", "status": "current", "retrieved_utc": "2026-07-19", "use_boundary": "Product identity and zero-row requirements only; no query, download, ingestion, or fit."},
    {"source_id": "HETDEX-DEXCUBE", "title": "HETDEX dexcube public tutorial and product tooling", "authority": "HETDEX project repository", "url": "https://github.com/HETDEX/dexcube", "status": "current", "retrieved_utc": "2026-07-19", "use_boundary": "Datacube and metadata field context only; no software install or data access."},
    {"source_id": "NZBS-HANDBOOK", "title": "Transfusion Medicine Handbook", "authority": "New Zealand Blood Service", "url": "https://www.nzblood.co.nz/healthcare-professionals/transfusion-medicine/transfusion-medicine-handbook", "status": "current", "retrieved_utc": "2026-07-19", "use_boundary": "Synthetic workflow vocabulary only; no clinical interpretation or competence claim."},
    {"source_id": "NZBS-HAEMOVIGILANCE", "title": "Haemovigilance programme", "authority": "New Zealand Blood Service", "url": "https://www.nzblood.co.nz/healthcare-professionals/haemovigilance-programme", "status": "current", "retrieved_utc": "2026-07-19", "use_boundary": "Adverse-event issue spotting only; no patient, donor, provider, or outcome evidence."},
    {"source_id": "RFC-9068", "title": "JSON Web Token Profile for OAuth 2.0 Access Tokens", "authority": "IETF RFC Editor", "url": "https://www.rfc-editor.org/rfc/rfc9068.html", "status": "stable", "retrieved_utc": "2026-07-19", "use_boundary": "Synthetic structural token requirements only."},
    {"source_id": "RFC-9068-ERRATA", "title": "RFC 9068 errata", "authority": "IETF RFC Editor", "url": "https://www.rfc-editor.org/errata/rfc9068", "status": "watch", "retrieved_utc": "2026-07-19", "use_boundary": "One reported erratum is tracked as unresolved watch evidence; it does not rewrite the RFC or confer production assurance."},
    {"source_id": "HDC-CODE", "title": "Code of Health and Disability Services Consumers' Rights", "authority": "New Zealand Health and Disability Commissioner", "url": "https://www.hdc.org.nz/your-rights/about-the-code/code-of-health-and-disability-services-consumers-rights/", "status": "current", "retrieved_utc": "2026-07-19", "use_boundary": "Rights and communication issue spotting only; no legal or clinical interpretation."},
    {"source_id": "NZ-PRIVACY-PRINCIPLES", "title": "New Zealand information privacy principles", "authority": "Office of the Privacy Commissioner", "url": "https://www.privacy.org.nz/privacy-act-2020/privacy-principles/", "status": "current", "retrieved_utc": "2026-07-19", "use_boundary": "Privacy issue spotting only; no legal interpretation."},
    {"source_id": "TE-MANA-RARAUNGA", "title": "Te Mana Raraunga Māori Data Sovereignty Network", "authority": "Te Mana Raraunga", "url": "https://www.temanararaunga.maori.nz/", "status": "current", "retrieved_utc": "2026-07-19", "use_boundary": "Authority reservation only; Māori concepts remain under tangata whenua, iwi, hapū, and Māori authority."},
    {"source_id": "ISO-28500-2017", "title": "Information and documentation — WARC file format", "authority": "ISO", "url": "https://www.iso.org/standard/68004.html", "status": "stable", "retrieved_utc": "2026-07-19", "use_boundary": "Public abstract and bounded structural requirements only; no complete standard-conformance claim."},
    {"source_id": "WAI-ARIA-SWITCH", "title": "WAI-ARIA switch role", "authority": "W3C", "url": "https://www.w3.org/TR/wai-aria/#switch", "status": "current", "retrieved_utc": "2026-07-19", "use_boundary": "Structural role and state requirements only."},
    {"source_id": "WAI-APG-SWITCH", "title": "Switch Pattern", "authority": "W3C WAI-ARIA Authoring Practices", "url": "https://www.w3.org/WAI/ARIA/apg/patterns/switch/", "status": "current", "retrieved_utc": "2026-07-19", "use_boundary": "Illustrative structural and keyboard requirements only; manual testing remains reserved."},
    {"source_id": "IUPAC-GIBBS-ENERGY", "title": "Gibbs energy terminology", "authority": "IUPAC Gold Book", "url": "https://goldbook.iupac.org/terms/view/G02629", "status": "stable", "retrieved_utc": "2026-07-19", "use_boundary": "Thermodynamic terminology and units only; no psyche conversion."},
    {"source_id": "IUPAC-ENTHALPY", "title": "Enthalpy terminology", "authority": "IUPAC Gold Book", "url": "https://goldbook.iupac.org/terms/view/E02141", "status": "stable", "retrieved_utc": "2026-07-19", "use_boundary": "Thermodynamic terminology and units only; no psyche conversion."},
    {"source_id": "ABADIE-DIAMOND-HAINMUELLER-2010", "title": "Synthetic Control Methods for Comparative Case Studies", "authority": "Abadie, Diamond, and Hainmueller, primary methods paper", "url": "https://doi.org/10.1198/jasa.2009.ap08746", "status": "stable", "retrieved_utc": "2026-07-19", "use_boundary": "Structural method obligations only; zero participant estimation."},
    {"source_id": "ABADIE-2021", "title": "Using Synthetic Controls: Feasibility, Data Requirements, and Methodological Aspects", "authority": "Abadie, primary methods review", "url": "https://doi.org/10.1257/jel.20191450", "status": "stable", "retrieved_utc": "2026-07-19", "use_boundary": "Design, support, fit, and sensitivity obligations only; no effect estimation."},
]


SAFE_TASK_TITLES = [
    "Freeze barrier generation and party-count schema", "Freeze barrier timeout broken-state and abort semantics", "Freeze barrier reset-isolation and teardown receipt",
    "Freeze BPHZ divergent-subgraph vocabulary", "Freeze forest compatibility and Taylor-subtraction rules", "Freeze BPHZ locality renormalization and observation firewall",
    "Freeze HETDEX PDR1 product and Source Catalog 2 identity", "Freeze HETDEX datacube sensitivity mask and checksum obligations", "Freeze HETDEX zero-query zero-row likelihood counters",
    "Freeze transfusion request-specimen-component lineage", "Freeze discrepancy hold recall and correction transitions", "Freeze accessible escalation workload readback and handover",
    "Freeze RFC 9068 type issuer audience and time rules", "Freeze RFC 9068 confusion replay and minimization refusals", "Freeze reported-erratum watch without semantic override",
    "Freeze transfusion authority reservation cells", "Freeze consent privacy correction remedy and whānau nondecision matrix", "Freeze WARC version header and record-identity schema",
    "Freeze WARC relation digest truncation and budget refusals", "Freeze switch name state keyboard and grouping schema", "Freeze switch non-colour focus contrast fallback reservations",
    "Freeze Gibbs-Helmholtz typed derivative and fixed-condition schema", "Freeze Gibbs-Helmholtz category-barrier mutations", "Freeze synthetic-control treated-unit and donor-pool schema",
    "Freeze synthetic-control fit weight placebo and nonpromotion mutations", "Build four-status official-source ledger", "Build 650-proposal exact collision audit",
    "Build five-class privacy and raw-identifier scan plan", "Build commit-local Git-blob manifest plan", "Build sanitized Sable terminal-route hold plan",
]

CANDIDATE_TITLES = [
    "Cyclic barrier generation simulator", "Barrier broken-state and quiescence checker", "BPHZ forest compatibility graph", "BPHZ Taylor-subtraction obligation linter",
    "HETDEX PDR1 provenance contract", "HETDEX zero-row receipt emitter", "Transfusion lineage state machine", "Transfusion discrepancy recall and correction board",
    "Transfusion workload and handover checker", "RFC 9068 claim-profile checker", "RFC 9068 confusion and minimization matrix", "Transfusion authority stop matrix",
    "WARC bounded record inspector", "WARC relation and digest refusal checker", "Accessible switch semantics linter", "Accessible switch fallback and reservation checker",
    "Gibbs-Helmholtz unit and domain checker", "Thermodynamic category firewall", "Synthetic-control assumption board", "Single-pass commit-manifest verifier",
]

SKILL_SPECS = [
    ("ghc-family-barrier-evidence-guard", "Audit bounded cyclic-barrier generations and teardown."),
    ("ghc-family-bphz-forest-obligations", "Type BPHZ forest prerequisites without physical promotion."),
    ("ghc-family-hetdex-zero-row", "Preserve a zero-row HETDEX PDR1 evidence boundary."),
    ("ghc-family-transfusion-lineage", "Check synthetic request-specimen-component lineage."),
    ("ghc-family-transfusion-hold-handover", "Check synthetic discrepancy holds, correction, and handover."),
    ("ghc-family-jwt-access-token-profile", "Audit synthetic RFC 9068 token structure."),
    ("ghc-family-transfusion-authority-reservation", "Reserve clinical, consent, remedy, and Māori decisions."),
    ("ghc-family-warc-refusal", "Reject malformed bounded WARC fixtures."),
    ("ghc-family-switch-audit", "Audit switch structure while reserving manual evaluation."),
    ("ghc-family-gibbs-helmholtz-domain", "Guard Gibbs-Helmholtz fixed-condition and category domains."),
    ("ghc-family-synthetic-control-board", "Audit synthetic-control assumptions without effect estimation."),
    ("ghc-family-source-status-drift", "Keep current, stable, draft, and watch sources distinct."),
    ("ghc-family-manifest-blob-contract", "Verify commit-local Git-blob manifest domains."),
    ("ghc-family-single-pass-budget", "Enforce one successful canonical validation pass and no replay."),
    ("ghc-family-failed-evidence-credit-lock", "Deny pass credit to failed or partial attempts."),
    ("ghc-family-staged-five-class-privacy", "Run bounded staged privacy and raw-identifier scans."),
    ("ghc-family-document-cap", "Enforce phase document word caps."),
    ("ghc-family-caller-surface-compatibility", "Check family-current caller compatibility."),
    ("ghc-family-four-way-equality", "Check clean local, upstream, tracking, and live equality."),
    ("ghc-family-terminal-baton-sanitizer", "Sanitize a one-message successor baton."),
]

RUNNER_TITLES = [
    "barrier_tribunal", "bphz_forest_board", "hetdex_zero_row", "transfusion_handover", "jwt_access_token_profile",
    "transfusion_authority_matrix", "warc_tribunal", "switch_audit", "gibbs_helmholtz_classifier", "synthetic_control_board",
]

CLEAN_TASK_TITLES = [
    "CLEAN normalize x1 JSON ordering", "FIX reject x2 fields in x1", "REFINE required proposal fields",
    "CLEAN deduplicate source identifiers", "FIX restrict source status vocabulary", "REFINE source watch explanations",
    "CLEAN normalize portfolio identifiers", "FIX reject inherited completion credit", "REFINE exact and blocked packet visibility",
    "CLEAN normalize mutation identifiers", "FIX preserve zero-query and zero-row counters", "REFINE GMUT observation firewall wording",
    "CLEAN normalize transfusion trace states", "FIX require unresolved hold and recall ownership", "REFINE clinical competence and safety reservations",
    "CLEAN normalize RFC 9068 vectors", "FIX reject type confusion and reported-erratum substitution", "REFINE replay and minimization wording",
    "CLEAN normalize authority matrix cells", "FIX prevent clinical consent disclosure or remedy action", "REFINE Māori-authority reservation wording",
    "CLEAN normalize WARC byte fixtures", "FIX enforce header record and byte budgets", "REFINE standard-conformance refusal wording",
    "CLEAN normalize switch properties", "FIX preserve manual and affected-user evaluation reservations", "REFINE Gibbs-Helmholtz unit typing",
    "CLEAN normalize synthetic-control obligations", "FIX preserve Stage 20 nonpromotion", "REFINE terminal-route sanitation and hold checks",
]

MUTATION_KINDS = [
    "missing_required_obligation",
    "invalid_domain_or_type",
    "silent_state_or_authority_promotion",
    "boundary_or_unit_erasure",
    "replay_lineage_or_generation_break",
    "resource_or_budget_violation",
    "forbidden_claim_promotion",
]


def synthetic_mutation_plan() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for proposal_row in PROPOSALS:
        pnum = int(proposal_row["proposal_id"].split("P")[-1])
        for index, kind in enumerate(MUTATION_KINDS, 1):
            rows.append({
                "mutation_id": f"V6492-MUT-P{pnum:02d}-{index:02d}",
                "proposal_id": proposal_row["proposal_id"],
                "kind": kind,
                "status": "preregistered_not_executed",
                "expected": "reject_or_quarantine",
                "retained_negative_id": f"V6492-SYN-N-P{pnum:02d}-{index:02d}",
            })
    return rows
