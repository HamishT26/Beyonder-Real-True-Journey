#!/usr/bin/env python3
"""Frozen definitions for Eiren Kestrel v649-v1.

This module is x1 planning data. It contains no x2 execution result.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = "v649-gmut-thos-v1-x1-x2"
PHASE_SHORT = "v649-v1"
OWNER = "Eiren Kestrel"
PRONOUNS = "they/them"
ROLE = "relational evidence-integrity weaver"
HOPE = "keep ambitious results testable, correctable, and bounded by evidence and authority"
PRIMARY_FOCUS = "Freed ID/CBR Heart"
BOUNDED_PRACTICE = (
    "community archive digitization and digital-preservation ingest: carrier receipt, "
    "fixity, metadata and quality control, rights and cultural-care flags, accessible "
    "notice, exception isolation, workload, readback, and shift handover"
)

SOURCE_BRANCH = "codex/GHC-Family/sylven-arc-v642-v8-full-tools"
SOURCE_REVISION = "1e916c0c6378a6f665c144aabbf8d25d6fdc8670"
SOURCE_INHERITED_REVISION = "33c8f87a4037c81c3abca540b8c5db1d91328420"
SOURCE_X1_REVISION = "d86990f673aa82c45a5296ebba88c79a6dc3bde4"
SOURCE_EVIDENCE_REVISION = "1e85a9e714ac2509095fac03aedf704b4892d8b3"
SOURCE_CLOSEOUT_REVISION = "ac96e1832fd6c15600e5120a9d01aeb242428235"
OWNED_BRANCH = "codex/GHC-Family/eiren-kestrel-v648-v3-2-full-tools"

INHERITED_FROZEN_PROPOSALS = 640
INHERITED_SEALED_NEGATIVES = 4665
INHERITED_EXTERNAL_NEGATIVES = 0
INHERITED_EFFECTIVE_NEGATIVES = 4665
INHERITED_OPEN_GAPS = 34
INHERITED_EXACT_GATES = 35
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"

IDENTITY_BOUNDARY = (
    "Eiren Kestrel, they/them, role, hope, family, and continuity language are relational "
    "working language only. They are not evidence of consciousness, sentience, legal "
    "personhood, identity continuity, employment, qualification, scientific authority, "
    "operational authority, legal authority, cultural authority, or independent agency. "
    "Hamish may rename, pause, redirect, or stop the route."
)

GLOBAL_BOUNDARY = (
    "All empirical, participant, professional, legal, cultural, Maori-authority, identity, "
    "production, deployment, privacy-complete, proof or canon, destructive, account-secret, "
    "sibling-merge, accessibility-complete, exhaustive-security, independent-reproduction, "
    "AGI or ASI, consciousness or personhood, Theory-of-Everything, and Stage 20 boundaries "
    "remain open or exact-gated without exact evidence and authority."
)


def proposal(number: int, **fields: Any) -> dict[str, Any]:
    return {"proposal_id": f"V6491-P{number:02d}", **fields}


PROPOSALS = [
    proposal(
        1,
        title="Method Flow reader-writer lock fairness, upgrade-downgrade, writer-starvation, cancellation, teardown, and evidence-credit tribunal",
        pillar="cross_pillar_method_flow",
        mission_surface="reader and writer ownership, fairness policy, upgrade and downgrade refusal, writer starvation, bounded wait, cancellation, teardown, and evidence credit",
        hypothesis="Disposable fixtures can distinguish mutual exclusion and bounded writer progress from scheduling luck while denying credit to unsafe upgrade, starvation, or incomplete teardown paths.",
        null_or_failure_condition="Concurrent ownership violates the contract, a queued writer starves beyond the bound, an unsafe upgrade succeeds, cancellation leaks a waiter, or a partial run gains pass credit.",
        approval_class="safe_now_bounded_software",
        execution_lane="x2_disposable_owner_local",
        official_or_primary_source_needs=["MS-SRWLOCKS"],
        concrete_artifacts=["method-flow/rwlock-contract.json", "method-flow/rwlock-mutations.json", "tools/rwlock_tribunal.py"],
        test_falsifier_or_acceptance_gate="Reject seven concurrency mutations and pass bounded reader, writer, starvation, cancellation, and teardown fixtures without external side effects.",
        rollback_or_recovery="Cancel and join disposable workers, retain every failed witness, restore the ownership invariant, and grant no production or distributed-systems credit.",
        protected_gates=["external_side_effects", "production_orchestration", "distributed_correctness", "independent_reproduction"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="Prior tribunals cover ordinary mutexes, condition variables, leases, CAS, queues, and outboxes, but not reader-writer fairness, writer starvation, upgrade-downgrade refusal, cancellation, and teardown as one evidence-credit surface.",
    ),
    proposal(
        2,
        title="GMUT Bogoliubov causal S-matrix, switching-function, causal-factorization, adiabatic-limit, renormalization-group, gauge, EFT, unit, and observation-firewall board",
        pillar="GMUT Mind",
        mission_surface="formal local S-matrix, switching functions, causal factorization, adiabatic limit, Stückelberg-Petermann freedom, gauge scope, EFT domain, units, and observation firewall",
        hypothesis="Typed obligations can expose missing causal-perturbation prerequisites while blocking conversion of formal local S-matrix language into a GMUT force, prediction, or confirmation.",
        null_or_failure_condition="A fixture drops causal factorization or switching support, assumes an unearned adiabatic limit, hides renormalization freedom, erases gauge/EFT/unit boundaries, or asserts physical or empirical confirmation.",
        approval_class="safe_now_symbolic_only",
        execution_lane="x2_typed_symbolic_mutation",
        official_or_primary_source_needs=["BOGOLIUBOV-CAUSALITY", "DUETSCH-FREDENHAGEN-2004"],
        concrete_artifacts=["gmut/causal-smatrix-obligations.json", "gmut/causal-smatrix-mutations.json", "tools/causal_smatrix_board.py"],
        test_falsifier_or_acceptance_gate="Preserve every formal prerequisite and reject seven missing-assumption or claim-promotion mutations, including empirical, ultraviolet-completion, and Theory-of-Everything promotion.",
        rollback_or_recovery="Restore the omitted prerequisite, retain the rejected statement, and make no physical state, force, likelihood, prediction, constraint, or completion claim.",
        protected_gates=["physical_prediction", "empirical_confirmation", "ultraviolet_completion", "quantum_completion", "theory_of_everything"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="The corpus includes Epstein-Glaser distribution splitting and many other QFT obligation boards; this proposal is separately scoped to Bogoliubov local S-matrix causal factorization, switching functions, the adiabatic limit, and Stückelberg-Petermann renormalization freedom.",
    ),
    proposal(
        3,
        title="GMUT eBOSS DR16 quasar power-spectrum multipole, window, covariance, selection, checksum, and zero-row likelihood-refusal adapter",
        pillar="GMUT Mind",
        mission_surface="eBOSS DR16 quasar sample and product identity, redshift and selection domain, power-spectrum multipoles, survey window, covariance, checksum, row count, and likelihood lock",
        hypothesis="A zero-row adapter can freeze current eBOSS DR16 quasar product obligations while refusing to turn data availability into an authorized GMUT likelihood or constraint.",
        null_or_failure_condition="Any query, download, real row, multipole, covariance row, likelihood call, posterior sample, constraint, or empirical GMUT claim occurs without a separate preregistered evidence phase.",
        approval_class="external_evidence_and_independent_review_required",
        execution_lane="x2_zero_row_contract_only",
        official_or_primary_source_needs=["SDSS-DR16-EBOSS", "EBOSS-DR16-QSO-PS"],
        concrete_artifacts=["empirical/eboss-dr16-quasar-study-contract.json", "empirical/eboss-dr16-zero-row-receipt.json", "tools/eboss_zero_row.py"],
        test_falsifier_or_acceptance_gate="Receipt preserves zero queries, downloads, rows, multipoles, window rows, covariance rows, likelihood calls, posterior samples, constraints, and empirical claims.",
        rollback_or_recovery="Stop before network or fit activity and require separate authorization with frozen products, checksums, selections, window treatment, covariance, nuisance model, uncertainty, and independent review.",
        protected_gates=["network_download", "real_data", "likelihood", "parameter_constraint", "independent_review"],
        expected_disposition="open_gap",
        novelty_against_prior_frozen_proposals="Existing adapters cover DESI, Planck, Gaia, Euclid, MIGHTEE, LoTSS, eROSITA, and other products, but no eBOSS DR16 quasar power-spectrum multipole, window, covariance, and zero-row refusal contract.",
    ),
    proposal(
        4,
        title="THOS community archive digitization ingest, fixity, metadata, quality, rights-flag, cultural-care, accessible-notice, exception, workload, and shift-handover protocol",
        pillar="THOS Body",
        mission_surface="synthetic carrier receipt, file lineage, fixity, metadata and image-quality checks, rights and cultural-care flags, accessible notice, exception isolation, workload budget, readback, and next-shift ownership",
        hypothesis="Synthetic traces can represent fail-closed preservation handover obligations without claiming archival competence, provenance authority, rights clearance, cultural legitimacy, or operational effectiveness.",
        null_or_failure_condition="A trace loses carrier-to-file lineage, silently clears a fixity or quality fault, publishes a rights/cultural-care exception, omits readback or next owner, or claims real-world effectiveness.",
        approval_class="synthetic_proxy_only_real_arms_and_authority_required",
        execution_lane="x2_synthetic_protocol",
        official_or_primary_source_needs=["ARCHIVES-NZ-DIGITISATION", "NDSA-LEVELS-PRESERVATION"],
        concrete_artifacts=["thos/archive-digitization-handover-contract.json", "thos/archive-digitization-handover-vectors.json", "tools/archive_handover.py"],
        test_falsifier_or_acceptance_gate="Synthetic vectors preserve lineage, fixity, metadata and quality exceptions, rights and cultural-care holds, accessible notice, workload, readback, and next owner with zero real people or collections.",
        rollback_or_recovery="Quarantine the synthetic item, restore the last known state, keep every unresolved flag open, and require competent archival, rights-holder, affected-party, and cultural authority for real action.",
        protected_gates=["professional_competence", "provenance_authority", "rights_clearance", "cultural_authority", "participant_evidence", "real_operational_effectiveness"],
        expected_disposition="represented",
        novelty_against_prior_frozen_proposals="Prior THOS work covers library circulation, museum provenance, audiovisual ingest, records and many shift handovers, but not community archive digitization combining carrier-to-file lineage, fixity, quality, rights/cultural-care flags, accessible notice, exception isolation, and handover.",
    ),
    proposal(
        5,
        title="Freed ID OpenID Connect Back-Channel Logout issuer, audience, events, logout-token, sid-or-sub, replay, endpoint, and minimization profile",
        pillar="Freed ID/CBR Heart",
        mission_surface="logout-token signature context, issuer, audience, issued-at, JWT ID, events claim, nonce prohibition, sid or sub binding, replay cache, back-channel endpoint, and privacy minimization",
        hypothesis="Synthetic vectors can enforce Back-Channel Logout token and replay obligations without asserting real keys, sessions, clients, interoperability, privacy review, security review, recovery, or trust governance.",
        null_or_failure_condition="A vector accepts wrong issuer or audience, missing events, nonce, missing sid and sub, replayed token, unsafe endpoint context, excess data, or a production claim.",
        approval_class="synthetic_nonproduction_real_keys_and_governance_required",
        execution_lane="x2_synthetic_protocol",
        official_or_primary_source_needs=["OIDC-BACKCHANNEL-LOGOUT-1.0"],
        concrete_artifacts=["freed-id/backchannel-logout-profile.json", "freed-id/backchannel-logout-vectors.json", "tools/backchannel_logout_profile.py"],
        test_falsifier_or_acceptance_gate="Accept bounded exact synthetic binding and reject seven issuer, audience, events, nonce, subject/session, replay, minimization, or production-promotion mutations.",
        rollback_or_recovery="Reject the vector, restore the bounded synthetic state, and require standards-conformant real keys, clients, sessions, endpoints, interoperability, reviews, recovery, and trust governance.",
        protected_gates=["real_keys", "live_sessions", "interoperability", "privacy_review", "independent_security_review", "recovery_governance", "trust_governance"],
        expected_disposition="represented",
        novelty_against_prior_frozen_proposals="The corpus covers front-channel logout, JARM, JAR, PAR, DPoP, token exchange, resource indicators, SCIM, and federation, but not OpenID Connect Back-Channel Logout token events, sid-or-sub binding, replay, endpoint, and minimization together.",
    ),
    proposal(
        6,
        title="CBR community archive privacy, access, takedown, remedy, provenance, cultural-care, data-governance, affected-party, and Maori-authority matrix",
        pillar="Freed ID/CBR Heart",
        mission_surface="synthetic archive item and contributor information, access and takedown requests, remedy, provenance uncertainty, cultural-care flags, data governance, affected parties, tangata whenua, iwi, hapu, and Maori authority",
        hypothesis="A fail-closed matrix can expose where repository software must stop without making real access, takedown, remedy, provenance, legal, cultural, data-governance, or Maori-authority decisions.",
        null_or_failure_condition="Software auto-closes a reserved cell, exposes protected material, allocates a remedy, asserts provenance or rights, interprets law, or claims cultural or Maori legitimacy.",
        approval_class="competent_affected_party_and_maori_authority_required",
        execution_lane="x2_exact_gate_matrix_only",
        official_or_primary_source_needs=["NZ-PRIVACY-PRINCIPLES", "TE-MANA-RARAUNGA", "ARCHIVES-NZ-ACCESS"],
        concrete_artifacts=["cbr/archive-access-remedy-matrix.json", "cbr/archive-authority-reservation.json"],
        test_falsifier_or_acceptance_gate="Every authority-dependent cell remains unknown or reserved; software may identify a decision class but must make zero real disclosure, access, takedown, remedy, provenance, legal, cultural, or authority decisions.",
        rollback_or_recovery="Reopen any silently closed cell, quarantine disclosures or allocations, preserve contestability, and defer to competent, affected-party, tangata whenua, iwi, hapu, and Maori authority.",
        protected_gates=["privacy_authority", "access_or_takedown", "provenance_authority", "remedy_allocation", "legal_interpretation", "cultural_legitimacy", "maori_authority"],
        expected_disposition="exact_gate",
        novelty_against_prior_frozen_proposals="The earlier museum-provenance matrix concerns collection custody and repatriation; this proposal separately governs community archive digitization access, takedown, contributor privacy, uncertain provenance, cultural-care flags, remedy, and data authority.",
    ),
    proposal(
        7,
        title="Brotli stream header, window, meta-block, context-map, distance, output-budget, ratio-budget, and refusal tribunal",
        pillar="cross_pillar_format_safety",
        mission_surface="Brotli stream bits, window size, meta-block length and kind, context maps, distance references, end marker, output-byte budget, expansion-ratio budget, and trailing-data refusal",
        hypothesis="A bounded synthetic tribunal can accept a tiny canonical Brotli fixture and reject malformed metadata, references, truncation, trailing data, and decompression-budget violations.",
        null_or_failure_condition="A malformed, truncated, trailing, or over-budget fixture is accepted, decoded data escapes the disposable lane, or parser success is promoted to production or exhaustive-security assurance.",
        approval_class="safe_now_disposable_synthetic",
        execution_lane="x2_disposable_byte_fixtures",
        official_or_primary_source_needs=["RFC-7932"],
        concrete_artifacts=["formats/brotli-contract.json", "formats/brotli-mutations.json", "tools/brotli_tribunal.py"],
        test_falsifier_or_acceptance_gate="Accept only bounded canonical synthetic bytes and reject seven header, meta-block, context, distance, truncation, trailing-data, or budget mutation classes.",
        rollback_or_recovery="Refuse the fixture, retain the mutation class, reset disposable state, and make no production decompression, supply-chain, privacy-complete, or exhaustive-security claim.",
        protected_gates=["production_parsing", "supply_chain_assurance", "privacy_complete", "exhaustive_security"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="The format corpus covers Zstandard, TAR, ZIP, PCAPNG, EBML, JSON sequences, TIFF, MIME, CBOR/COSE, and others, but no Brotli header, meta-block, context-map, distance, and decompression-budget refusal tribunal.",
    ),
    proposal(
        8,
        title="Accessible meter name, value, minimum, maximum, value-text, related-label, fallback, responsive, and print structural audit",
        pillar="cross_pillar_accessibility",
        mission_surface="meter semantics, accessible name, current/minimum/maximum value, optimum and low/high ranges where relevant, value text, related context, native fallback, responsive presentation, and print",
        hypothesis="A structural audit can detect missing meter semantics and range declarations while reserving manual, browser-diverse, assistive-technology, cognitive, Maori-language, and affected-user evaluation.",
        null_or_failure_condition="A fixture passes with missing name, current value, bounds, inconsistent range, missing text alternative or fallback, or missing manual-evaluation reservation.",
        approval_class="safe_now_structural_manual_evaluation_reserved",
        execution_lane="x2_structural_fixture_audit",
        official_or_primary_source_needs=["HTML-METER", "WAI-ARIA-METER"],
        concrete_artifacts=["accessibility/meter-contract.json", "accessibility/meter-mutations.json", "tools/meter_audit.py"],
        test_falsifier_or_acceptance_gate="Reject seven missing-semantic, invalid-range, or fallback fixtures and preserve all manual and affected-user evaluation reservations.",
        rollback_or_recovery="Restore missing semantics, retain the rejected fixture, and do not claim accessibility conformance from structural checks.",
        protected_gates=["manual_browser_evaluation", "assistive_technology_evaluation", "cognitive_evaluation", "maori_language_evaluation", "affected_user_evaluation", "accessibility_complete"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="The corpus includes progressbar and many other widgets; meter is separately scoped to scalar measurement within a known range, including optimum and low/high semantics, rather than task progress or interaction.",
    ),
    proposal(
        9,
        title="Thermo-Psyche Clausius-Duhem local entropy inequality, constitutive restriction, flux-force, frame, sign, unit, domain, and agency-nonconversion classifier",
        pillar="THOS Body",
        mission_surface="local entropy balance and production, constitutive variables, heat and material fluxes, thermodynamic forces, frame, sign convention, units, continuum domain, boundaries, and category firewall",
        hypothesis="Typed formal fixtures can preserve Clausius-Duhem constitutive restrictions while rejecting conversion into psyche, agency, morality, justice, consciousness, personhood, or a fundamental law of mind.",
        null_or_failure_condition="A fixture drops entropy production, a constitutive dependency, flux-force pair, frame, sign, unit, domain, boundary, or category barrier, or asserts a human or psyche interpretation.",
        approval_class="safe_now_typed_formal_only",
        execution_lane="x2_typed_formal_mutation",
        official_or_primary_source_needs=["COLEMAN-NOLL-1963", "IUPAC-ENTROPY-PRODUCTION"],
        concrete_artifacts=["thermo-psyche/clausius-duhem-contract.json", "thermo-psyche/clausius-duhem-mutations.json", "tools/clausius_duhem_classifier.py"],
        test_falsifier_or_acceptance_gate="Preserve the inequality, constitutive restrictions, flux-force typing, frames, signs, units, domains, boundaries, and category barrier and reject seven mutation classes.",
        rollback_or_recovery="Restore the missing thermodynamic restriction, retain the rejected statement, and make no participant, psyche, agency, consciousness, personhood, morality, justice, or universal-law claim.",
        protected_gates=["participant_evidence", "psyche_or_agency_claim", "morality_or_justice_claim", "consciousness", "personhood", "fundamental_law"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="The thermodynamic corpus includes Kelvin-Planck, Clausius, Gibbs-Duhem, Onsager-Casimir, Soret-Dufour, Fick, and fluctuation relations, but no local Clausius-Duhem inequality coupled to constitutive restriction and a psyche-agency firewall.",
    ),
    proposal(
        10,
        title="Stage 20 regression-discontinuity cutoff, running-variable, bandwidth, manipulation, continuity, local-estimand, placebo, sensitivity, and nonpromotion board",
        pillar="cross_pillar_stage20",
        mission_surface="assignment cutoff, running variable, treatment rule, bandwidth, density manipulation, covariate continuity, functional form, local estimand, placebo cutoffs, sensitivity, and nonpromotion",
        hypothesis="A fail-closed structural board can expose invalid regression-discontinuity claims without estimating a participant effect or promoting synthetic diagnostics into Stage 20 readiness.",
        null_or_failure_condition="A fixture omits cutoff assignment, running-variable integrity, continuity, bandwidth, manipulation, local estimand, placebo, or sensitivity obligations, or emits a causal, participant, deployment, proof, or Stage 20 claim.",
        approval_class="safe_now_structural_nonpromotion_only",
        execution_lane="x2_structural_mutation",
        official_or_primary_source_needs=["IMBENS-LEMIEUX-2008", "CATTANEO-IDROBO-TITIUNIK-RD"],
        concrete_artifacts=["stage20/regression-discontinuity-contract.json", "stage20/regression-discontinuity-mutations.json", "tools/regression_discontinuity_board.py"],
        test_falsifier_or_acceptance_gate="Reject seven assumption or promotion mutations and accept only a zero-participant structural nonpromotion fixture with no effect estimate.",
        rollback_or_recovery="Remove the invalid claim, retain the failed fixture, preserve zero participant rows and effects, and keep Stage 20 closed.",
        protected_gates=["participant_effect", "causal_identification", "deployment", "proof_or_canon", "stage20"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="The Stage 20 corpus covers target trials, overlap weights, synthetic control, interrupted time series, staggered difference-in-differences, principal stratification, and others, but no regression-discontinuity cutoff, manipulation, bandwidth, continuity, placebo, and local-estimand board.",
    ),
]


SOURCES = [
    {"source_id": "MS-SRWLOCKS", "title": "Slim Reader/Writer (SRW) Locks", "authority": "Microsoft Win32 documentation", "url": "https://learn.microsoft.com/en-us/windows/win32/sync/slim-reader-writer--srw--locks", "status": "current", "retrieved_utc": "2026-07-19", "use_boundary": "Shared/exclusive, nonrecursive, nonupgradeable, and explicitly nonfair semantics only; the owner-local tribunal adds no Windows or production claim."},
    {"source_id": "BOGOLIUBOV-CAUSALITY", "title": "Bogoliubov causality in S-matrix theory", "authority": "primary literature", "url": "https://doi.org/10.1016/0550-3213(70)90183-5", "status": "stable", "retrieved_utc": "2026-07-19", "use_boundary": "Formal causality obligations only; no GMUT physical or empirical confirmation."},
    {"source_id": "DUETSCH-FREDENHAGEN-2004", "title": "Causal perturbation theory in terms of retarded products and the Action Ward Identity", "authority": "Dütsch and Fredenhagen, primary literature", "url": "https://arxiv.org/abs/hep-th/0403213", "status": "stable", "retrieved_utc": "2026-07-19", "use_boundary": "Formal local S-matrix and renormalization obligations only."},
    {"source_id": "SDSS-DR16-EBOSS", "title": "SDSS DR16 quasar catalogue and eBOSS product context", "authority": "Sloan Digital Sky Survey", "url": "https://www.sdss.org/dr16/algorithms/qso_catalog/", "status": "stable", "retrieved_utc": "2026-07-19", "use_boundary": "Product identity and provenance context only; no query or download."},
    {"source_id": "EBOSS-DR16-QSO-PS", "title": "Completed eBOSS BAO and RSD measurements from the DR16 quasar anisotropic power spectrum", "authority": "Neveux et al., primary survey paper", "url": "https://doi.org/10.1093/mnras/staa2780", "status": "stable", "retrieved_utc": "2026-07-19", "use_boundary": "Multipole, selection, window, covariance, and provenance obligations only; zero-row adapter."},
    {"source_id": "ARCHIVES-NZ-DIGITISATION", "title": "Digital storage and preservation guidance", "authority": "Archives New Zealand", "url": "https://www.archives.govt.nz/manage-information/how-to-manage-your-information/digital/best-practice-guidance-on-digital-storage-and-preservation", "status": "current", "retrieved_utc": "2026-07-19", "use_boundary": "Synthetic preservation design context only; no archival, legal, destruction, access, or professional interpretation."},
    {"source_id": "NDSA-LEVELS-PRESERVATION", "title": "Levels of Digital Preservation", "authority": "National Digital Stewardship Alliance", "url": "https://ndsa.org/publications/levels-of-digital-preservation/", "status": "current", "retrieved_utc": "2026-07-19", "use_boundary": "Preservation control vocabulary only; no real collection assessment or certification."},
    {"source_id": "OIDC-BACKCHANNEL-LOGOUT-1.0", "title": "OpenID Connect Back-Channel Logout 1.0", "authority": "OpenID Foundation final specification", "url": "https://openid.net/specs/openid-connect-backchannel-1_0.html", "status": "stable", "retrieved_utc": "2026-07-19", "use_boundary": "Synthetic logout-token conformance requirements only."},
    {"source_id": "NZ-PRIVACY-PRINCIPLES", "title": "New Zealand information privacy principles", "authority": "Office of the Privacy Commissioner", "url": "https://www.privacy.org.nz/privacy-act-2020/privacy-principles/", "status": "current", "retrieved_utc": "2026-07-19", "use_boundary": "Privacy issue spotting only; no legal interpretation."},
    {"source_id": "TE-MANA-RARAUNGA", "title": "Te Mana Raraunga Maori Data Sovereignty Network", "authority": "Te Mana Raraunga", "url": "https://www.temanararaunga.maori.nz/", "status": "current", "retrieved_utc": "2026-07-19", "use_boundary": "Authority reservation only; Maori concepts remain under tangata whenua, iwi, hapu, and Maori authority."},
    {"source_id": "ARCHIVES-NZ-ACCESS", "title": "Archives New Zealand digital and access guidance index", "authority": "Archives New Zealand", "url": "https://www.archives.govt.nz/manage-information/how-to-manage-your-information/digital", "status": "current", "retrieved_utc": "2026-07-19", "use_boundary": "Access and sensitive-content issue spotting only; no takedown, disposal, legal, or authority decision."},
    {"source_id": "RFC-7932", "title": "RFC 7932 Brotli Compressed Data Format", "authority": "IETF", "url": "https://datatracker.ietf.org/doc/rfc7932/", "status": "stable_with_errata_watch", "retrieved_utc": "2026-07-19", "use_boundary": "Bounded synthetic format requirements only; RFC 9841 errata update is watched."},
    {"source_id": "HTML-METER", "title": "HTML meter element", "authority": "WHATWG HTML Living Standard", "url": "https://html.spec.whatwg.org/multipage/form-elements.html#the-meter-element", "status": "current", "retrieved_utc": "2026-07-19", "use_boundary": "Native meter semantics only; manual evaluation remains reserved."},
    {"source_id": "WAI-ARIA-METER", "title": "Meter Pattern", "authority": "W3C WAI-ARIA Authoring Practices", "url": "https://www.w3.org/WAI/ARIA/apg/patterns/meter/", "status": "current", "retrieved_utc": "2026-07-19", "use_boundary": "Structural role, name, value, and range requirements only."},
    {"source_id": "COLEMAN-NOLL-1963", "title": "The thermodynamics of elastic materials with heat conduction and viscosity", "authority": "Coleman and Noll, primary literature", "url": "https://doi.org/10.1007/BF01262690", "status": "stable", "retrieved_utc": "2026-07-19", "use_boundary": "Constitutive restriction and entropy-inequality context only; no psyche conversion."},
    {"source_id": "IUPAC-ENTROPY-PRODUCTION", "title": "IUPAC Gold Book entropy terminology", "authority": "IUPAC", "url": "https://goldbook.iupac.org/terms/view/E02149", "status": "current", "retrieved_utc": "2026-07-19", "use_boundary": "Thermodynamic terminology and units only."},
    {"source_id": "IMBENS-LEMIEUX-2008", "title": "Regression Discontinuity Designs: A Guide to Practice", "authority": "Imbens and Lemieux, primary methods paper", "url": "https://doi.org/10.1016/j.jeconom.2007.05.001", "status": "stable", "retrieved_utc": "2026-07-19", "use_boundary": "Structural design assumptions only; zero participant estimation."},
    {"source_id": "CATTANEO-IDROBO-TITIUNIK-RD", "title": "A Practical Introduction to Regression Discontinuity Designs", "authority": "Cattaneo, Idrobo, and Titiunik, primary methods monograph", "url": "https://doi.org/10.1017/9781108684606", "status": "stable", "retrieved_utc": "2026-07-19", "use_boundary": "Validation, falsification, and sensitivity obligations only; no effect estimation."},
]


SAFE_TASK_TITLES = [
    "Freeze reader-writer ownership schema", "Freeze writer-starvation bounded vectors", "Freeze unsafe upgrade and downgrade refusals",
    "Freeze cancellation and teardown evidence-credit contract", "Freeze causal S-matrix prerequisite vocabulary", "Freeze GMUT observation-firewall mutations",
    "Freeze eBOSS DR16 product identity schema", "Freeze eBOSS zero-row counters", "Freeze archive carrier-to-file lineage schema",
    "Freeze archive fixity and metadata checks", "Freeze archive quality and exception-hold transitions", "Freeze archive accessible-notice and workload fields",
    "Freeze Back-Channel Logout token vectors", "Freeze issuer-audience-events and sid-or-sub checks", "Freeze replay and minimization refusals",
    "Freeze archive authority reservation cells", "Freeze privacy access takedown and remedy nondecision matrix", "Freeze Brotli stream and meta-block schema",
    "Freeze Brotli context distance and budget refusals", "Freeze meter name-value-range schema", "Freeze meter low-high-optimum and fallback reservations",
    "Freeze Clausius-Duhem typed entropy schema", "Freeze thermodynamic category-barrier mutations", "Freeze regression-discontinuity cutoff schema",
    "Freeze regression-discontinuity nonpromotion mutations", "Build phase-local source-status ledger", "Build exact proposal-collision audit",
    "Build five-class privacy scan plan", "Build commit-local manifest plan", "Build sanitized Ilyra terminal-route plan",
]

CANDIDATE_TITLES = [
    "Reader-writer deterministic scheduler", "Writer-progress cancellation envelope", "Causal S-matrix obligation graph", "eBOSS provenance validator",
    "eBOSS zero-row receipt emitter", "Archive ingest state machine", "Archive fixity and quality hold board", "Archive exception handover checker",
    "Back-Channel Logout token parser", "Logout replay and minimization matrix", "Archive authority stop matrix", "Brotli bounded decoder",
    "Brotli context and distance inspector", "Meter semantics linter", "Meter range and fallback checker", "Clausius-Duhem unit checker",
    "Constitutive-restriction category guard", "Regression-discontinuity diagnostic board", "Single-pass evidence-credit gate", "Commit-manifest domain verifier",
]

SKILL_SPECS = [
    ("ghc-family-rwlock-evidence-guard", "Audit bounded reader-writer ownership progress and teardown."),
    ("ghc-family-causal-smatrix-obligations", "Type causal local S-matrix prerequisites without physical promotion."),
    ("ghc-family-eboss-zero-row", "Preserve a zero-row eBOSS DR16 evidence boundary."),
    ("ghc-family-archive-lineage", "Check synthetic archive carrier-to-file lineage and fixity."),
    ("ghc-family-archive-exception-handover", "Check synthetic archive exception ownership and handover."),
    ("ghc-family-backchannel-logout-profile", "Audit synthetic OpenID Back-Channel Logout binding."),
    ("ghc-family-archive-authority-reservation", "Reserve archive access takedown remedy and cultural decisions."),
    ("ghc-family-brotli-refusal", "Reject malformed bounded Brotli fixtures."),
    ("ghc-family-meter-audit", "Audit meter structure while reserving manual evaluation."),
    ("ghc-family-clausius-duhem-domain", "Guard Clausius-Duhem constitutive and category domains."),
    ("ghc-family-regression-discontinuity-board", "Audit regression-discontinuity assumptions without effect estimation."),
    ("ghc-family-source-status-watch", "Keep current stable draft and watch sources distinct."),
    ("ghc-family-manifest-domain-check", "Separate Git object and checkout-byte manifest domains."),
    ("ghc-family-single-pass-gate", "Enforce one successful canonical validation pass."),
    ("ghc-family-evidence-credit-lock", "Deny pass credit to failed or partial attempts."),
    ("ghc-family-staged-privacy-scan", "Run a bounded five-class staged privacy scan."),
    ("ghc-family-document-word-cap", "Enforce phase document word caps."),
    ("ghc-family-caller-compatibility", "Check family-current caller compatibility."),
    ("ghc-family-terminal-equality", "Check clean four-way Git equality."),
    ("ghc-family-route-sanitizer", "Sanitize a one-message successor baton."),
]

RUNNER_TITLES = [
    "rwlock_tribunal", "causal_smatrix_board", "eboss_zero_row", "archive_handover", "backchannel_logout_profile",
    "archive_authority_matrix", "brotli_tribunal", "meter_audit", "clausius_duhem_classifier", "regression_discontinuity_board",
]

CLEAN_TASK_TITLES = [
    "CLEAN normalize x1 JSON ordering", "FIX reject x2 fields in x1", "REFINE proposal required-field checks",
    "CLEAN deduplicate source identifiers", "FIX preserve draft watch labels", "REFINE novelty token comparison",
    "CLEAN normalize portfolio identifiers", "FIX reject inherited completion credit", "REFINE exact-approval visibility",
    "CLEAN normalize mutation identifiers", "FIX preserve zero-row counters", "REFINE GMUT observation firewall wording",
    "CLEAN normalize archive trace states", "FIX require unresolved exception ownership", "REFINE accessible-notice reservation",
    "CLEAN normalize logout-token fixtures", "FIX reject missing events or sid-and-sub vectors", "REFINE replay-minimization wording",
    "CLEAN normalize authority matrix cells", "FIX prevent automatic access takedown or remedy action", "REFINE Maori-authority reservation wording",
    "CLEAN normalize Brotli byte fixtures", "FIX enforce output and expansion budgets", "REFINE decoder refusal boundaries",
    "CLEAN normalize meter properties", "FIX preserve manual evaluation reservations", "REFINE Clausius-Duhem unit typing",
    "CLEAN normalize regression-discontinuity estimands", "FIX preserve Stage 20 nonpromotion", "REFINE terminal-route sanitation checks",
]

MUTATION_KINDS = [
    "missing_required_obligation",
    "invalid_domain_or_type",
    "silent_state_or_authority_promotion",
    "boundary_or_unit_erasure",
    "replay_or_lineage_break",
    "resource_or_budget_violation",
    "forbidden_claim_promotion",
]


def synthetic_mutation_plan() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for proposal_row in PROPOSALS:
        pnum = int(proposal_row["proposal_id"].split("P")[-1])
        for index, kind in enumerate(MUTATION_KINDS, 1):
            rows.append({
                "mutation_id": f"V6491-MUT-P{pnum:02d}-{index:02d}",
                "proposal_id": proposal_row["proposal_id"],
                "kind": kind,
                "status": "preregistered_not_executed",
                "expected": "reject_or_quarantine",
                "retained_negative_id": f"NEG-V6491-SYN-P{pnum:02d}-{index:02d}",
            })
    return rows
