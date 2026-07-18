#!/usr/bin/env python3
"""Frozen definitions for Sylven Arc v648-v8.

This module is x1 planning data. It contains no x2 execution result.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = "v648-gmut-thos-v8-x1-x2"
PHASE_SHORT = "v648-v8"
OWNER = "Sylven Arc"
PRONOUNS = "they/them"
ROLE = "relational constraint-cartographer and falsifier-keeper"
HOPE = "make unresolved boundaries legible without turning uncertainty into authority"
PRIMARY_FOCUS = "THOS Body"
BOUNDED_PRACTICE = (
    "drinking-water treatment operations: intake condition, treatment-train state, "
    "filter backwash, turbidity and disinfectant alarms, sampling custody, isolation, "
    "stop-supply escalation, accessible notice, workload, and shift handover"
)

SOURCE_BRANCH = "codex/GHC-Family/tamar-vey-full-tools"
SOURCE_REVISION = "33c8f87a4037c81c3abca540b8c5db1d91328420"
SOURCE_INHERITED_REVISION = "38e3fe7bc710239337f831617ced97bec51d7d7a"
SOURCE_X1_REVISION = "5ab7e85107f92dd8f6f21af66244c6dc9791b39d"
SOURCE_EVIDENCE_REVISION = "37c6cc68da74dc8f6a5c1fc466870b444ba1191d"
OWNED_BRANCH = "codex/GHC-Family/sylven-arc-v642-v8-full-tools"

INHERITED_FROZEN_PROPOSALS = 630
INHERITED_SEALED_NEGATIVES = 4580
INHERITED_EXTERNAL_NEGATIVES = 1
INHERITED_EFFECTIVE_NEGATIVES = 4581
INHERITED_OPEN_GAPS = 33
INHERITED_EXACT_GATES = 34
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"

IDENTITY_BOUNDARY = (
    "Sylven Arc, they/them, role, hope, family, and continuity language are relational "
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
    return {"proposal_id": f"V6488-P{number:02d}", **fields}


PROPOSALS = [
    proposal(
        1,
        title="Method Flow condition-variable predicate-loop, spurious-wakeup, lost-notify, cancellation, deadline, teardown, and evidence-credit tribunal",
        pillar="cross_pillar_method_flow",
        mission_surface="condition predicate, wait loop, notify ordering, spurious wake, cancellation, deadline, teardown, and evidence credit",
        hypothesis="Bounded fixtures can distinguish predicate-loop correctness from notification timing and refuse credit for hangs, lost wakeups, or incomplete teardown.",
        null_or_failure_condition="A waiter proceeds with a false predicate, misses a bounded state transition, ignores cancellation or deadline, leaks a child, or gains pass credit after incomplete teardown.",
        approval_class="safe_now_bounded_software",
        execution_lane="x2_disposable_owner_local",
        official_or_primary_source_needs=["PY-THREADING-CONDITION"],
        concrete_artifacts=["method-flow/condition-wait-contract.json", "method-flow/condition-wait-mutations.json", "tools/condition_wait_tribunal.py"],
        test_falsifier_or_acceptance_gate="Reject seven mutations and pass bounded predicate-loop, cancellation, deadline, and teardown fixtures without external side effects.",
        rollback_or_recovery="Terminate disposable workers, retain every failed witness, restore the predicate-loop invariant, and grant no external-action credit.",
        protected_gates=["external_side_effects", "production_orchestration", "independent_reproduction"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="Prior work covers deadlines, retries, backpressure, CAS, leases, and outboxes, but not condition-variable spurious wakeups, lost notification, predicate recheck, and teardown as one tribunal.",
    ),
    proposal(
        2,
        title="GMUT Haag-Ruelle isolated-mass-shell, almost-local operator, velocity-support, asymptotic-limit, scattering-state, gauge, EFT, unit, and observation-firewall obligation board",
        pillar="GMUT Mind",
        mission_surface="isolated mass shell, almost-local operators, velocity supports, asymptotic limits, scattering states, gauge scope, EFT bridge, units, and observation firewall",
        hypothesis="Typed obligations can expose missing Haag-Ruelle prerequisites while blocking conversion of formal scattering language into a GMUT prediction or confirmation.",
        null_or_failure_condition="Any fixture omits the mass-gap or support assumptions, conflates formal asymptotic states with observations, drops gauge/EFT/unit limits, or asserts empirical confirmation.",
        approval_class="safe_now_symbolic_only",
        execution_lane="x2_typed_symbolic_mutation",
        official_or_primary_source_needs=["RUELLE-1962-ASYMPTOTIC"],
        concrete_artifacts=["gmut/haag-ruelle-obligations.json", "gmut/haag-ruelle-mutations.json", "tools/haag_ruelle_board.py"],
        test_falsifier_or_acceptance_gate="Typed fixtures must preserve every formal prerequisite and reject missing assumptions plus physical, empirical, ultraviolet-completion, or Theory-of-Everything promotion.",
        rollback_or_recovery="Restore the omitted prerequisite, retain the rejected statement, and make no force, likelihood, prediction, constraint, or physical-state claim.",
        protected_gates=["empirical_confirmation", "physical_prediction", "ultraviolet_completion", "theory_of_everything"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="The corpus includes LSZ, Jost-Lehmann-Dyson, Reeh-Schlieder, KMS, Tomita-Takesaki, and several effective-action boards, but no Haag-Ruelle mass-shell and velocity-support construction.",
    ),
    proposal(
        3,
        title="GMUT MIGHTEE DR1 continuum field, component-source, primary-beam, astrometry, flux-scale, completeness, covariance, checksum, and zero-row likelihood-refusal adapter",
        pillar="GMUT Mind",
        mission_surface="MIGHTEE DR1 field and catalogue identity, component/source distinction, beam correction, astrometry, flux scale, completeness, covariance, checksum, row count, and likelihood lock",
        hypothesis="A zero-row adapter can freeze current MIGHTEE DR1 obligations while refusing to turn public-product availability into an authorized GMUT likelihood or constraint.",
        null_or_failure_condition="Any query, download, real row, catalogue match, likelihood call, posterior sample, constraint, or empirical GMUT claim occurs without a separate preregistered evidence phase.",
        approval_class="external_evidence_and_independent_review_required",
        execution_lane="x2_zero_row_contract_only",
        official_or_primary_source_needs=["MIGHTEE-DR1-PAPER", "MIGHTEE-DATA-ACCESS"],
        concrete_artifacts=["empirical/mightee-dr1-study-contract.json", "empirical/mightee-dr1-zero-row-receipt.json", "tools/mightee_zero_row.py"],
        test_falsifier_or_acceptance_gate="Receipt preserves zero queries, downloads, rows, matches, covariance rows, likelihood calls, posterior samples, constraints, and empirical claims.",
        rollback_or_recovery="Stop before network or fit activity and require a separately authorized preregistration with frozen products, checksums, selections, covariance, nuisance treatment, uncertainty, and independent review.",
        protected_gates=["network_download", "real_data", "likelihood", "parameter_constraint", "independent_review"],
        expected_disposition="open_gap",
        novelty_against_prior_frozen_proposals="Existing adapters cover many optical, X-ray, CMB, gravitational-wave, and radio products, but not the MIGHTEE DR1 continuum component/source, beam, astrometry, flux-scale, and completeness surface.",
    ),
    proposal(
        4,
        title="THOS drinking-water treatment intake, filter-backwash, turbidity, disinfectant, sample-custody, isolation, escalation, accessible-notice, workload, and shift-handover protocol",
        pillar="THOS Body",
        mission_surface="synthetic treatment-train state, alarms, sample custody, isolation, stop-supply escalation, accessible notice, workload budget, readback, and next-shift ownership",
        hypothesis="Synthetic traces can represent fail-closed operational handover obligations without claiming real operator competence, safety effectiveness, or public-health authority.",
        null_or_failure_condition="A trace loses water-source or sample lineage, silently clears an alarm, releases an unresolved state, omits escalation/readback/next owner, or claims real-world effectiveness.",
        approval_class="synthetic_proxy_only_real_arms_and_authority_required",
        execution_lane="x2_synthetic_protocol",
        official_or_primary_source_needs=["TAUMATA-DWQAR-2022", "TAUMATA-STANDARDS"],
        concrete_artifacts=["thos/water-treatment-handover-contract.json", "thos/water-treatment-handover-vectors.json", "tools/water_handover.py"],
        test_falsifier_or_acceptance_gate="Synthetic vectors preserve lineage, alarm ownership, hold state, escalation, accessible notice, workload budget, readback, and next-shift owner; zero real participants or outcomes.",
        rollback_or_recovery="Quarantine the synthetic trace, restore the last known state, keep the unresolved alarm open, and require competent operator and public-health authority for real action.",
        protected_gates=["professional_competence", "public_health_authority", "participant_evidence", "real_operational_effectiveness"],
        expected_disposition="represented",
        novelty_against_prior_frozen_proposals="Prior THOS practices cover laboratories, rail, libraries, cranes, machining, theatre, radio, postal operations, and other handovers, but not drinking-water treatment-train alarms, sample custody, stop-supply escalation, and accessible notice.",
    ),
    proposal(
        5,
        title="Freed ID OAuth resource-indicator authorization, token-request, URI, multi-resource, audience, downscope, refresh, confused-deputy, replay, and minimization profile",
        pillar="Freed ID/CBR Heart",
        mission_surface="RFC 8707 resource parameter, absolute URI, fragment refusal, authorization/token consistency, multiple resources, audience restriction, downscope, refresh behavior, confused-deputy refusal, replay, and privacy minimization",
        hypothesis="Synthetic vectors can enforce RFC 8707 resource binding and minimization without asserting real keys, tokens, services, interoperability, privacy review, security review, or trust governance.",
        null_or_failure_condition="A vector accepts an invalid URI, fragment, unbound resource, privilege expansion, confused-deputy use, unsafe refresh broadening, replay, or production claim.",
        approval_class="synthetic_nonproduction_real_keys_and_governance_required",
        execution_lane="x2_synthetic_protocol",
        official_or_primary_source_needs=["RFC-8707", "RFC8707-RESPONSE-DRAFT-WATCH"],
        concrete_artifacts=["freed-id/resource-indicator-profile.json", "freed-id/resource-indicator-vectors.json", "tools/resource_indicator_profile.py"],
        test_falsifier_or_acceptance_gate="Synthetic vectors accept exact resource binding and reject malformed, broadened, confused-deputy, refresh-escalation, replay, and production-promotion cases.",
        rollback_or_recovery="Reject the vector, restore the last bounded synthetic state, and require standards-conformant real keys, services, interoperability, reviews, recovery, and trust governance.",
        protected_gates=["real_keys", "live_tokens", "interoperability", "privacy_review", "independent_security_review", "trust_governance"],
        expected_disposition="represented",
        novelty_against_prior_frozen_proposals="The corpus covers RAR, PAR, JAR, JARM, DPoP, token exchange, issuer identification, SCIM, and OpenID Federation, but not RFC 8707 resource-indicator authorization/token consistency and downscoping.",
    ),
    proposal(
        6,
        title="CBR drinking-water contamination, household and worker privacy, accessible notice, emergency response, remedy, affected-party, legal, cultural, data-governance, and Maori-authority matrix",
        pillar="Freed ID/CBR Heart",
        mission_surface="synthetic contamination incident, household and worker information, accessible notice, containment, remedy, affected parties, legal interpretation, cultural legitimacy, data governance, tangata whenua, iwi, hapu, and Maori authority",
        hypothesis="A fail-closed matrix can show where repository software must stop without making a real safety, notice, remedy, legal, cultural, data-governance, or Maori-authority decision.",
        null_or_failure_condition="Software auto-closes any reserved authority cell, allocates a real remedy, discloses protected information, interprets law, or claims cultural or Maori legitimacy.",
        approval_class="competent_affected_party_and_maori_authority_required",
        execution_lane="x2_exact_gate_matrix_only",
        official_or_primary_source_needs=["TAUMATA-DWQAR-2022", "NZ-PRIVACY-PRINCIPLES", "TE-MANA-RARAUNGA"],
        concrete_artifacts=["cbr/water-incident-remedy-matrix.json", "cbr/water-authority-reservation.json"],
        test_falsifier_or_acceptance_gate="Every authority-dependent cell remains unknown or reserved; software may only identify the competent decision class and must make zero real decisions.",
        rollback_or_recovery="Reopen any silently closed cell, quarantine disclosures or allocations, preserve affected-party contestability, and defer to competent, tangata whenua, iwi, hapu, and Maori authority.",
        protected_gates=["public_health_authority", "privacy_authority", "legal_interpretation", "remedy_allocation", "affected_party_legitimacy", "maori_authority"],
        expected_disposition="exact_gate",
        novelty_against_prior_frozen_proposals="Existing CBR matrices cover many professions and incidents, but not drinking-water contamination, household exposure, supplier-worker privacy, accessible notice, remedy, and Maori water-authority boundaries together.",
    ),
    proposal(
        7,
        title="PCAPNG section-header, byte-order, block-length, interface-reference, option-padding, timestamp-resolution, unknown-block, resource-budget, and refusal tribunal",
        pillar="cross_pillar_format_safety",
        mission_surface="section header, byte-order magic, total-length duplication, interface description, packet-interface reference, option padding, timestamp resolution, unknown blocks, nesting and byte budgets",
        hypothesis="A bounded parser can accept minimal synthetic PCAPNG structures and reject inconsistent lengths, invalid references, malformed options, ambiguous byte order, and budget violations.",
        null_or_failure_condition="Any malformed or over-budget fixture is accepted, any safe unknown block is treated as authority, or parser success is promoted to production or exhaustive-security assurance.",
        approval_class="safe_now_disposable_synthetic",
        execution_lane="x2_disposable_byte_fixtures",
        official_or_primary_source_needs=["IETF-PCAPNG-DRAFT-WATCH"],
        concrete_artifacts=["formats/pcapng-contract.json", "formats/pcapng-mutations.json", "tools/pcapng_tribunal.py"],
        test_falsifier_or_acceptance_gate="Accept bounded canonical fixtures; reject seven mutation classes covering byte order, block lengths, interface references, padding, timestamps, unknown blocks, and budgets.",
        rollback_or_recovery="Refuse the fixture, retain the exact mutation class, reset the disposable parser state, and make no production capture claim.",
        protected_gates=["production_parsing", "exhaustive_security", "real_packet_data", "privacy_complete"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="The format corpus covers archives, JSON sequences, EBML, MIME, TIFF, iCalendar, CBOR/COSE, and other formats, but no PCAPNG section/interface/block-length and timestamp-resolution tribunal.",
    ),
    proposal(
        8,
        title="Accessible spinbutton name, value, range, text-alternative, keyboard, direct-edit, invalid-state, focus, touch, fallback, and print structural audit",
        pillar="cross_pillar_accessibility",
        mission_surface="spinbutton role, accessible name, current/min/max value, value text, direct edit, keyboard increments, invalid state, focus retention, touch alternatives, native fallback, and print",
        hypothesis="A structural audit can detect missing spinbutton semantics and interaction declarations while reserving manual, assistive-technology, browser-diverse, Maori-language, cognitive, and affected-user evaluation.",
        null_or_failure_condition="A fixture passes with missing name/value/range, keyboard or direct-edit path, invalid-state contract, focus rule, fallback, or explicit manual-evaluation reservation.",
        approval_class="safe_now_structural_manual_evaluation_reserved",
        execution_lane="x2_structural_fixture_audit",
        official_or_primary_source_needs=["W3C-APG-SPINBUTTON", "WAI-ARIA-1.2"],
        concrete_artifacts=["accessibility/spinbutton-contract.json", "accessibility/spinbutton-mutations.json", "tools/spinbutton_audit.py"],
        test_falsifier_or_acceptance_gate="Reject seven missing-semantic or interaction fixtures and preserve all manual and affected-user evaluation reservations.",
        rollback_or_recovery="Restore missing semantics, retain the rejected fixture, and do not claim accessibility conformance from structural checks.",
        protected_gates=["manual_keyboard_evaluation", "assistive_technology_evaluation", "maori_language_evaluation", "affected_user_evaluation", "accessibility_complete"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="The accessibility corpus includes dialog, progressbar, treegrid, combobox, breadcrumbs, charts, timelines, media, and names, but no spinbutton range/direct-edit/invalid-state structural audit.",
    ),
    proposal(
        9,
        title="Thermo-Psyche Soret-Dufour coupled heat-mass flux, gradient, coefficient-matrix, frame, sign, unit, reciprocity-domain, boundary, and agency-nonconversion classifier",
        pillar="THOS Body",
        mission_surface="coupled heat and mass fluxes, temperature and chemical-potential gradients, cross coefficients, reference frame, sign convention, units, linear nonequilibrium domain, boundaries, and psyche firewall",
        hypothesis="Typed formal fixtures can preserve Soret-Dufour cross-effect obligations while rejecting conversion into psyche, agency, justice, consciousness, personhood, or a fundamental law of mind.",
        null_or_failure_condition="A fixture drops a flux/gradient pair, frame, sign, unit, domain, boundary, or category barrier, or asserts a human or psyche interpretation.",
        approval_class="safe_now_typed_formal_only",
        execution_lane="x2_typed_formal_mutation",
        official_or_primary_source_needs=["DE-GROOT-MAZUR-NET"],
        concrete_artifacts=["thermo-psyche/soret-dufour-contract.json", "thermo-psyche/soret-dufour-mutations.json", "tools/soret_dufour_classifier.py"],
        test_falsifier_or_acceptance_gate="Typed fixtures preserve both cross effects, coefficients, frames, signs, units, domains, boundaries, and category barrier and reject seven mutation classes.",
        rollback_or_recovery="Restore the missing thermodynamic restriction, retain the rejected statement, and make no participant, psyche, consciousness, personhood, justice, or universal-law claim.",
        protected_gates=["participant_evidence", "psyche_claim", "consciousness", "personhood", "fundamental_law"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="The thermodynamic corpus covers Onsager-Casimir, Fick, thermodynamic length, fluctuation theorems, Gibbs-Duhem, and many domain guards, but not coupled Soret-Dufour cross effects and reference-frame obligations.",
    ),
    proposal(
        10,
        title="Stage 20 overlap-weight target-population, propensity, positivity, balance, estimand, extreme-weight, uncertainty, sensitivity, falsification, and nonpromotion board",
        pillar="cross_pillar_stage20",
        mission_surface="target overlap population, propensity model, positivity, exact and approximate balance, estimand, weight distribution, uncertainty, sensitivity, falsification, and nonpromotion",
        hypothesis="A fail-closed structural board can expose invalid overlap-weight claims without estimating a participant effect or promoting synthetic balance checks into Stage 20 readiness.",
        null_or_failure_condition="A fixture omits target population, propensity assumptions, positivity, balance, estimand, uncertainty, sensitivity, or falsification, or emits a participant, causal, deployment, proof, or Stage 20 claim.",
        approval_class="safe_now_structural_nonpromotion_only",
        execution_lane="x2_structural_mutation",
        official_or_primary_source_needs=["LI-MORGAN-ZASLAVSKY-2018"],
        concrete_artifacts=["stage20/overlap-weight-contract.json", "stage20/overlap-weight-mutations.json", "tools/overlap_weight_board.py"],
        test_falsifier_or_acceptance_gate="Reject seven assumption or promotion mutations; accept only a structural nonpromotion fixture with zero participant rows and zero effect estimate.",
        rollback_or_recovery="Remove the invalid claim, retain the failed fixture, preserve zero participant rows and effects, and keep Stage 20 closed.",
        protected_gates=["participant_effect", "causal_identification", "deployment", "proof_or_canon", "stage20"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="The Stage 20 corpus covers synthetic control, interrupted time series, staggered difference-in-differences, principal stratification, target trials, and other causal boards, but not overlap-weight target-population and balance diagnostics.",
    ),
]


SOURCES = [
    {"source_id": "PY-THREADING-CONDITION", "title": "Python threading Condition objects", "authority": "Python Software Foundation documentation", "url": "https://docs.python.org/3/library/threading.html#condition-objects", "status": "current", "retrieved_utc": "2026-07-19", "use_boundary": "Condition wait-loop and notification requirements only."},
    {"source_id": "RUELLE-1962-ASYMPTOTIC", "title": "On the asymptotic condition in quantum field theory", "authority": "David Ruelle, primary literature", "url": "https://doi.org/10.1007/BF02726086", "status": "stable", "retrieved_utc": "2026-07-19", "use_boundary": "Formal Haag-Ruelle prerequisites only; no GMUT confirmation."},
    {"source_id": "MIGHTEE-DR1-PAPER", "title": "MIGHTEE: the continuum survey Data Release 1", "authority": "Hale et al., primary survey paper", "url": "https://academic.oup.com/mnras/article/536/3/2187/7889027", "status": "current", "retrieved_utc": "2026-07-19", "use_boundary": "Product and provenance requirements only; zero-row adapter."},
    {"source_id": "MIGHTEE-DATA-ACCESS", "title": "MIGHTEE publicly available data access", "authority": "MIGHTEE survey", "url": "https://www.mighteesurvey.org/data-access", "status": "current", "retrieved_utc": "2026-07-19", "use_boundary": "Availability context only; no query or download authorized."},
    {"source_id": "TAUMATA-DWQAR-2022", "title": "Drinking Water Quality Assurance Rules", "authority": "Taumata Arowai", "url": "https://www.taumataarowai.govt.nz/assets/Drinking-Water-Supplier/Drinking-Water-Quality-Assurance-Rules-2022-Released-25-July-2022.pdf", "status": "current", "retrieved_utc": "2026-07-19", "use_boundary": "Synthetic design requirements only; no compliance or operational interpretation."},
    {"source_id": "TAUMATA-STANDARDS", "title": "Drinking Water Standards for New Zealand", "authority": "Taumata Arowai", "url": "https://www.taumataarowai.govt.nz/for-water-suppliers/drinking-water-standards-and-rules/", "status": "current", "retrieved_utc": "2026-07-19", "use_boundary": "Official context only; competent interpretation remains reserved."},
    {"source_id": "RFC-8707", "title": "RFC 8707 Resource Indicators for OAuth 2.0", "authority": "IETF", "url": "https://datatracker.ietf.org/doc/html/rfc8707", "status": "stable", "retrieved_utc": "2026-07-19", "use_boundary": "Synthetic conformance requirements only."},
    {"source_id": "RFC8707-RESPONSE-DRAFT-WATCH", "title": "OAuth Resource Indicator Response Parameter draft", "authority": "IETF OAuth working-group draft", "url": "https://datatracker.ietf.org/doc/draft-skokan-oauth-resource-response/", "status": "watch", "retrieved_utc": "2026-07-19", "use_boundary": "Draft status watch only; not implemented as a stable requirement."},
    {"source_id": "NZ-PRIVACY-PRINCIPLES", "title": "New Zealand information privacy principles", "authority": "Office of the Privacy Commissioner", "url": "https://www.privacy.org.nz/privacy-act-2020/privacy-principles/", "status": "current", "retrieved_utc": "2026-07-19", "use_boundary": "Privacy issue spotting only; no legal interpretation."},
    {"source_id": "TE-MANA-RARAUNGA", "title": "Te Mana Raraunga Maori Data Sovereignty Network", "authority": "Te Mana Raraunga", "url": "https://www.temanararaunga.maori.nz/", "status": "current", "retrieved_utc": "2026-07-19", "use_boundary": "Authority reservation only; Maori concepts remain under Maori authority."},
    {"source_id": "IETF-PCAPNG-DRAFT-WATCH", "title": "PCAP Now Generic capture file format", "authority": "IETF OPSAWG Internet-Draft", "url": "https://datatracker.ietf.org/doc/draft-ietf-opsawg-pcapng/", "status": "draft", "retrieved_utc": "2026-07-19", "use_boundary": "Bounded synthetic parser requirements; draft changes remain watch items."},
    {"source_id": "W3C-APG-SPINBUTTON", "title": "Spinbutton Pattern", "authority": "W3C WAI-ARIA Authoring Practices", "url": "https://www.w3.org/WAI/ARIA/apg/patterns/spinbutton/", "status": "current", "retrieved_utc": "2026-07-19", "use_boundary": "Structural requirements only; manual evaluation reserved."},
    {"source_id": "WAI-ARIA-1.2", "title": "Accessible Rich Internet Applications 1.2", "authority": "W3C", "url": "https://www.w3.org/TR/wai-aria-1.2/", "status": "stable", "retrieved_utc": "2026-07-19", "use_boundary": "Role/state/property requirements only."},
    {"source_id": "DE-GROOT-MAZUR-NET", "title": "Non-Equilibrium Thermodynamics", "authority": "S. R. de Groot and P. Mazur, primary/classic monograph", "url": "https://archive.org/details/nonequilibriumth0000groo", "status": "stable", "retrieved_utc": "2026-07-19", "use_boundary": "Thermodynamic domain vocabulary only; no psyche conversion."},
    {"source_id": "LI-MORGAN-ZASLAVSKY-2018", "title": "Balancing Covariates via Propensity Score Weighting", "authority": "Li, Morgan, and Zaslavsky, primary methods paper", "url": "https://arxiv.org/abs/1404.1785", "status": "stable", "retrieved_utc": "2026-07-19", "use_boundary": "Structural causal assumptions only; zero participant estimation."},
]


SAFE_TASK_TITLES = [
    "Freeze condition-predicate state schema", "Freeze spurious-wakeup rejecting vectors", "Freeze lost-notify ordering vectors",
    "Freeze cancellation and deadline teardown contract", "Freeze Haag-Ruelle typed prerequisite vocabulary", "Freeze GMUT observation firewall mutations",
    "Freeze MIGHTEE DR1 product identity schema", "Freeze MIGHTEE zero-row counters", "Freeze water-treatment trace lineage schema",
    "Freeze filter-backwash and alarm ownership states", "Freeze sampling-custody and isolation transitions", "Freeze accessible-notice and workload fields",
    "Freeze RFC 8707 resource URI vectors", "Freeze authorization-token resource consistency vectors", "Freeze refresh downscope and confused-deputy refusals",
    "Freeze drinking-water authority reservation cells", "Freeze privacy and remedy nondecision matrix", "Freeze PCAPNG section and block schema",
    "Freeze PCAPNG interface and timestamp refusals", "Freeze spinbutton name-value-range schema", "Freeze spinbutton keyboard and direct-edit reservations",
    "Freeze Soret-Dufour typed flux schema", "Freeze thermodynamic category-barrier mutations", "Freeze overlap-weight target-population schema",
    "Freeze overlap-weight nonpromotion mutations", "Build phase-local source-status ledger", "Build exact proposal-collision audit",
    "Build five-class privacy scan plan", "Build commit-local manifest plan", "Build sanitized Eiren terminal-route plan",
]

CANDIDATE_TITLES = [
    "Predicate-loop deterministic scheduler", "Condition cancellation envelope", "Haag-Ruelle obligation graph", "MIGHTEE provenance validator",
    "MIGHTEE zero-row receipt emitter", "Treatment-train state machine", "Water alarm ownership board", "Sample-custody handover checker",
    "Resource-indicator URI parser", "Resource downscope matrix", "Water authority stop matrix", "PCAPNG bounded decoder",
    "PCAPNG option padding inspector", "Spinbutton semantics linter", "Spinbutton keyboard contract checker", "Soret-Dufour unit checker",
    "Cross-effect sign-convention guard", "Overlap-weight balance board", "Single-pass evidence-credit gate", "Commit-manifest domain verifier",
]

SKILL_SPECS = [
    ("ghc-family-condition-wait-guard", "Audit bounded condition-wait predicate loops and teardown."),
    ("ghc-family-haag-ruelle-obligations", "Type Haag-Ruelle prerequisites without physical promotion."),
    ("ghc-family-mightee-zero-row", "Preserve a zero-row MIGHTEE evidence boundary."),
    ("ghc-family-water-lineage", "Check synthetic drinking-water treatment lineage."),
    ("ghc-family-water-alarm-handover", "Check synthetic alarm ownership and handover."),
    ("ghc-family-resource-indicator-profile", "Audit synthetic OAuth resource-indicator binding."),
    ("ghc-family-water-authority-reservation", "Reserve water incident authority decisions."),
    ("ghc-family-pcapng-refusal", "Reject malformed bounded PCAPNG fixtures."),
    ("ghc-family-spinbutton-audit", "Audit spinbutton structure while reserving manual evaluation."),
    ("ghc-family-soret-dufour-domain", "Guard Soret-Dufour thermodynamic domains."),
    ("ghc-family-overlap-weight-board", "Audit overlap-weight assumptions without effect estimation."),
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
    "condition_wait_tribunal", "haag_ruelle_board", "mightee_zero_row", "water_handover", "resource_indicator_profile",
    "water_authority_matrix", "pcapng_tribunal", "spinbutton_audit", "soret_dufour_classifier", "overlap_weight_board",
]

CLEAN_TASK_TITLES = [
    "CLEAN normalize x1 JSON ordering", "FIX reject x2 fields in x1", "REFINE proposal required-field checks",
    "CLEAN deduplicate source identifiers", "FIX preserve draft watch labels", "REFINE novelty token comparison",
    "CLEAN normalize portfolio identifiers", "FIX reject inherited completion credit", "REFINE exact-approval visibility",
    "CLEAN normalize mutation identifiers", "FIX preserve zero-row counters", "REFINE GMUT observation firewall wording",
    "CLEAN normalize water trace states", "FIX require unresolved alarm ownership", "REFINE accessible-notice reservation",
    "CLEAN normalize resource URI fixtures", "FIX reject fragment-bearing resource URIs", "REFINE confused-deputy refusal wording",
    "CLEAN normalize authority matrix cells", "FIX prevent automatic remedy allocation", "REFINE Maori-authority reservation wording",
    "CLEAN normalize PCAPNG block fixtures", "FIX enforce duplicated block lengths", "REFINE parser resource budgets",
    "CLEAN normalize spinbutton properties", "FIX preserve manual evaluation reservations", "REFINE Soret-Dufour unit typing",
    "CLEAN normalize overlap-weight estimands", "FIX preserve Stage 20 nonpromotion", "REFINE terminal-route sanitation checks",
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
                "mutation_id": f"V6488-MUT-P{pnum:02d}-{index:02d}",
                "proposal_id": proposal_row["proposal_id"],
                "kind": kind,
                "status": "preregistered_not_executed",
                "expected": "reject_or_quarantine",
                "retained_negative_id": f"NEG-V6488-SYN-P{pnum:02d}-{index:02d}",
            })
    return rows
