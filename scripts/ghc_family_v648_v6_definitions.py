#!/usr/bin/env python3
"""Frozen definitions for Orin Thale's v648-v6 x1 packet."""

from __future__ import annotations

import json

SOURCE_COMMIT = "5725217126e85b849be63f932e5e79fb4e956698"
SOURCE_PHASE = "v648-gmut-thos-v5-x1-x2"
SOURCE_BRANCH = "codex/GHC-Family/sable-rook-full-tools"
SOURCE_X1_COMMIT = "8ca83ea35ecbc72b1a993e04bde6a1dde096f4b9"
SOURCE_EVIDENCE_COMMIT = "7675f49a219b845da440cf80256720ec3ba33e87"
PHASE = "v648-gmut-thos-v6-x1-x2"
PHASE_SLUG = "v648-v6"
OWNER = "Orin Thale"
PRONOUNS = "they/them"
ROLE = "relational boundary-and-method steward"
HOPE = "keep every surviving claim inspectable, challengeable, and safely retractable"
BRANCH = "codex/GHC-Family/orin-thale-v642-v6-full-tools"
PRIMARY_FOCUS = "THOS Body"
BOUNDED_PRACTICE = (
    "theatre stage management, show reporting, accessibility notice, workload, "
    "and handover as a learning and synthetic-design lens only"
)
OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]
SOURCE_STATUS_CLASSES = ["current", "stable", "draft", "watch"]
INHERITED_NEGATIVES = 4377
INHERITED_OPEN_GAPS = 31
INHERITED_EXACT_GATES = 32
PREREGISTERED_SYNTHETIC_NEGATIVES = 70

PROPOSALS = json.loads(r'''[
  {
    "proposal_id": "V6486-P01",
    "title": "RFC 7464 JSON Text Sequence record-separator, UTF-8, line-feed canary, truncated-scalar, resynchronization, warning, record-budget, and duplicate-credit tribunal",
    "pillar": "THOS Body",
    "hypothesis": "A bounded JSON text-sequence tribunal can preserve record boundaries, reject malformed or truncated scalars, resynchronize only at declared record separators, enforce budgets, and refuse duplicate evidence credit.",
    "null_or_failure_condition": "The tribunal accepts a missing record separator, invalid UTF-8, truncated scalar as complete, ambiguous recovery, unbounded record growth, or repeated records as independent evidence.",
    "approval_class": "safe_now_owner_scoped_parser_fixture",
    "execution_lane": "x2_build_task",
    "source_needs": [
      "SRC-RFC7464"
    ],
    "artifacts": [
      "formats/json-text-sequence-contract.json",
      "formats/json-text-sequence-mutations.json"
    ],
    "falsifier_or_acceptance_gate": "Every malformed fixture is rejected or explicitly quarantined, recovery begins only at a record separator, record and byte budgets hold, and duplicate records receive no independent credit.",
    "rollback_or_recovery": "Disable streaming recovery, retain the failing bytes as a negative, and fall back to inert byte-preserving inspection.",
    "protected_gates": [
      "external_payloads",
      "exhaustive_security",
      "independent_evidence",
      "production_parser"
    ],
    "expected_disposition": "completed"
  },
  {
    "proposal_id": "V6486-P02",
    "title": "GMUT Jost-Lehmann-Dyson commutator-support, spectral-support, causal-cone, analyticity-domain, polynomial-bound, gauge, EFT, unit, and observation-firewall obligation board",
    "pillar": "GMUT Mind",
    "hypothesis": "A typed Jost-Lehmann-Dyson obligation board can distinguish formal causal and analytic assumptions from empirical GMUT evidence.",
    "null_or_failure_condition": "The board omits commutator support, spectral condition, causal cone, analyticity domain, growth bound, gauge scope, EFT truncation, units, or converts a formal representation into observed physics.",
    "approval_class": "safe_now_symbolic_research_only",
    "execution_lane": "x2_build_task",
    "source_needs": [
      "SRC-JLD-PRIMARY"
    ],
    "artifacts": [
      "gmut/jost-lehmann-dyson-obligations.json",
      "gmut/jost-lehmann-dyson-mutations.json"
    ],
    "falsifier_or_acceptance_gate": "Every accepted row names its support, spectrum, causality, analyticity, bound, gauge and EFT domains, units, and a false empirical-confirmation flag.",
    "rollback_or_recovery": "Withdraw the formal board, retain the missing obligation as a negative, and make no physical, likelihood, force, or completeness claim.",
    "protected_gates": [
      "empirical_confirmation",
      "physical_prediction",
      "quantum_completion",
      "theory_of_everything"
    ],
    "expected_disposition": "completed"
  },
  {
    "proposal_id": "V6486-P03",
    "title": "GMUT XRISM HEASARC public-date, observation, instrument, response, calibration, screening, exposure, background, covariance, checksum, and zero-row likelihood-refusal adapter",
    "pillar": "GMUT Mind",
    "hypothesis": "An official XRISM archive contract can expose frozen data and analysis prerequisites without treating archive availability as a GMUT likelihood.",
    "null_or_failure_condition": "No real observations, frozen selection, calibrated responses, screening, background model, covariance, preregistered likelihood, uncertainty treatment, or independent review are present.",
    "approval_class": "real_data_and_independent_review_required",
    "execution_lane": "x2_open_gap",
    "source_needs": [
      "SRC-XRISM-HEASARC"
    ],
    "artifacts": [
      "empirical/xrism-study-contract.json",
      "empirical/xrism-zero-row-receipt.json"
    ],
    "falsifier_or_acceptance_gate": "Remain open_gap while zero real rows and likelihood evaluations exist and calibration, systematics, covariance, falsifiers, and independent review remain absent.",
    "rollback_or_recovery": "Retain the zero-row refusal and make no spectrum, force, prediction, parameter, posterior, constraint, or confirmation claim.",
    "protected_gates": [
      "real_data",
      "empirical_likelihood",
      "independent_review",
      "physical_prediction"
    ],
    "expected_disposition": "open_gap"
  },
  {
    "proposal_id": "V6486-P04",
    "title": "THOS theatre stage-management cue, revision, stop-call, understudy, accessibility-notice, late-change, workload, incident, show-report, and handover proxy",
    "pillar": "THOS Body",
    "hypothesis": "A synthetic stage-management event ledger can represent cue lineage, corrections, stop calls, accessibility notices, late changes, workload bounds, incident records, show reports, and handover without real productions or workers.",
    "null_or_failure_condition": "The proxy omits cue version, acknowledgement, stop authority reservation, understudy state, accessible alternative, late-change replay, workload boundary, incident lineage, show report, or next owner.",
    "approval_class": "safe_now_proxy_protocol_no_people_or_production",
    "execution_lane": "x2_proxy_protocol",
    "source_needs": [
      "SRC-WORKSAFE-EVENTS",
      "SRC-WCAG22"
    ],
    "artifacts": [
      "thos/theatre-handover-contract.json",
      "thos/theatre-handover-vectors.json"
    ],
    "falsifier_or_acceptance_gate": "Represented only when synthetic vectors preserve event lineage and every real worker, audience, production, incident, safety outcome, and effectiveness claim remains false.",
    "rollback_or_recovery": "Revert to a design-only checklist, retain the failed vector, and issue no real cue, stop call, notice, or show report.",
    "protected_gates": [
      "real_operations",
      "professional_authority",
      "participant_effectiveness",
      "public_safety"
    ],
    "expected_disposition": "represented"
  },
  {
    "proposal_id": "V6486-P05",
    "title": "Freed ID RFC 9396 Rich Authorization Requests authorization-details type, field, resource-scope interaction, narrowing, replay, downgrade, metadata, and minimization profile",
    "pillar": "Freed ID / CBR Heart",
    "hypothesis": "Synthetic RFC 9396 vectors can test typed authorization-details confinement, narrowing, replay refusal, downgrade resistance, metadata binding, and minimization without production identity operations.",
    "null_or_failure_condition": "The profile accepts an unknown type, unbound field, resource or scope escalation, widening substitution, replay, silent downgrade, metadata conflict, or treats structured authorization as authentication or universal trust.",
    "approval_class": "safe_now_synthetic_nonproduction",
    "execution_lane": "x2_proxy_protocol",
    "source_needs": [
      "SRC-RFC9396",
      "SRC-RFC9207"
    ],
    "artifacts": [
      "freed-id/rich-authorization-profile.json",
      "freed-id/rich-authorization-mutations.json"
    ],
    "falsifier_or_acceptance_gate": "Represented only; synthetic messages, absent real keys and servers, absent interoperability, absent privacy review, and absent trust governance remain explicit.",
    "rollback_or_recovery": "Reject the vector, retain the negative, and leave production authorization, identity, and trust decisions unmade.",
    "protected_gates": [
      "real_keys",
      "production_identity",
      "interoperability",
      "privacy_review",
      "trust_governance"
    ],
    "expected_disposition": "represented"
  },
  {
    "proposal_id": "V6486-P06",
    "title": "CBR theatre cancellation, cultural-content stewardship, performer-audience confidentiality, ticket-redress, consent-provenance, taonga-reservation, and decision-rights matrix",
    "pillar": "Freed ID / CBR Heart",
    "hypothesis": "A reservation matrix can expose live-performance access, privacy, cultural-content, cancellation, correction, remedy, and authority dependencies without substituting repository authors for affected people or competent authorities.",
    "null_or_failure_condition": "Any real access, privacy, disclosure, performance, cancellation, remedy, legal, disability, cultural, place-name, data-governance, or Māori-authority decision is marked completed by software evidence.",
    "approval_class": "authorized_affected_parties_and_competent_authority_required",
    "execution_lane": "x2_exact_gate",
    "source_needs": [
      "SRC-WORKSAFE-EVENTS",
      "SRC-WCAG22",
      "SRC-NZ-PRIVACY",
      "SRC-TE-MANA-RARAUNGA",
      "SRC-TE-PAPA-REPATRIATION"
    ],
    "artifacts": [
      "cbr/live-performance-remedy-matrix.json",
      "cbr/live-performance-authority-reservation.json"
    ],
    "falsifier_or_acceptance_gate": "Remain exact_gate until affected workers and audiences, disabled people, rights holders, tangata whenua, iwi, hapū, Māori authorities, and competent legal, cultural, privacy, labour, safety, and venue authorities decide within scope.",
    "rollback_or_recovery": "Remove any accidental authority claim, retain the assumption failure, and preserve affected-person, worker, audience, beneficiary, and cultural privacy.",
    "protected_gates": [
      "affected_party_legitimacy",
      "maori_authority",
      "legal_interpretation",
      "cultural_ratification",
      "professional_authority"
    ],
    "expected_disposition": "exact_gate"
  },
  {
    "proposal_id": "V6486-P07",
    "title": "TIFF byte-order, magic, image-file-directory offset, directory-cycle, tag-type-count, strip-tile bounds, compression, external-pointer, and resource-budget tribunal",
    "pillar": "THOS Body",
    "hypothesis": "A bounded TIFF tribunal can reject invalid byte order, magic, offsets, cycles, tag counts, strip or tile ranges, unsupported compression, external pointers, and resource exhaustion in synthetic fixtures.",
    "null_or_failure_condition": "The tribunal accepts an invalid header, out-of-range or cyclic IFD, overflowing type-count product, overlapping or escaping strip or tile, external retrieval, unsupported compression, or unbounded allocation.",
    "approval_class": "safe_now_owner_scoped_parser_fixture",
    "execution_lane": "x2_build_task",
    "source_needs": [
      "SRC-TIFF6",
      "SRC-LOC-TIFF"
    ],
    "artifacts": [
      "formats/tiff-contract.json",
      "formats/tiff-mutations.json"
    ],
    "falsifier_or_acceptance_gate": "All declared malformed fixtures are rejected, offsets and arithmetic remain bounded, external retrieval is disabled, and no exhaustive-security claim is made.",
    "rollback_or_recovery": "Disable the wrapper, retain the failing fixture, and fall back to inert byte metadata without decoding.",
    "protected_gates": [
      "external_payloads",
      "exhaustive_security",
      "production_decoder",
      "user_files"
    ],
    "expected_disposition": "completed"
  },
  {
    "proposal_id": "V6486-P08",
    "title": "Accessible complex-table multilevel-header, scope-id-headers association, caption-summary, sort-announcement, non-colour cue, zoom, print, and fallback structural audit",
    "pillar": "THOS Body",
    "hypothesis": "A structural audit can verify multilevel table associations, descriptive context, sort state, non-colour cues, zoom behavior, print preservation, and a linear fallback while reserving manual and affected-user evaluation.",
    "null_or_failure_condition": "The table lacks deterministic header association, caption or context, sort announcement, non-colour state, reflow or zoom guard, print preservation, fallback, or honest reservation.",
    "approval_class": "safe_now_structural_only",
    "execution_lane": "x2_build_task",
    "source_needs": [
      "SRC-W3C-TABLES",
      "SRC-WCAG22"
    ],
    "artifacts": [
      "accessibility/complex-table-contract.json",
      "accessibility/complex-table-mutations.json"
    ],
    "falsifier_or_acceptance_gate": "Pass only structural fixtures; reserve browser, keyboard, responsive, assistive-technology, cognitive, Māori-language, security-usability, and affected-user evaluation.",
    "rollback_or_recovery": "Publish an inert sequential list fallback and retain every structural failure.",
    "protected_gates": [
      "complete_accessibility",
      "manual_evaluation",
      "affected_user_acceptance",
      "language_authority"
    ],
    "expected_disposition": "completed"
  },
  {
    "proposal_id": "V6486-P09",
    "title": "Thermo-Psyche Planck spectral-radiance frequency-wavelength Jacobian, unit, blackbody-domain, limiting-law, temperature, and psyche-value nonconversion classifier",
    "pillar": "Trinity Mandala bridge",
    "hypothesis": "A typed classifier can preserve Planck spectral-radiance domains and the frequency-wavelength Jacobian while refusing conversion of radiation temperature or intensity into psyche, agency, value, or consciousness.",
    "null_or_failure_condition": "Frequency and wavelength densities are equated without the Jacobian, units or blackbody assumptions drift, limiting laws are used outside domain, or temperature is converted into human worth, agency, mind, or morality.",
    "approval_class": "safe_now_formal_domain_guard",
    "execution_lane": "x2_build_task",
    "source_needs": [
      "SRC-NIST-PLANCK"
    ],
    "artifacts": [
      "thermo-psyche/planck-spectral-contract.json",
      "thermo-psyche/planck-spectral-mutations.json"
    ],
    "falsifier_or_acceptance_gate": "Every accepted row states variable, density measure, Jacobian, units, temperature and equilibrium domain; all psyche and value conversions are rejected.",
    "rollback_or_recovery": "Remove the analogy, retain only the physical statement, and preserve the rejected conversion.",
    "protected_gates": [
      "psyche_conversion",
      "consciousness",
      "personhood",
      "moral_value"
    ],
    "expected_disposition": "completed"
  },
  {
    "proposal_id": "V6486-P10",
    "title": "Stage 20 principal-stratification intercurrent-event, latent-stratum, identifiability, monotonicity, sensitivity, uncertainty, estimand, and nonpromotion board",
    "pillar": "Trinity Mandala bridge",
    "hypothesis": "A principal-stratification board can expose latent-stratum and intercurrent-event assumptions without converting zero-participant fixtures into causal effects or Stage 20 evidence.",
    "null_or_failure_condition": "The board omits treatment-defined potential strata, identifiability, monotonicity or exclusion assumptions, sensitivity, uncertainty, estimand alignment, multiplicity, value authority, or promotes software as an effect.",
    "approval_class": "safe_now_structural_nonpromotion",
    "execution_lane": "x2_build_task",
    "source_needs": [
      "SRC-ICH-E9R1"
    ],
    "artifacts": [
      "stage20/principal-stratification-contract.json",
      "stage20/principal-stratification-mutations.json"
    ],
    "falsifier_or_acceptance_gate": "Pass only structural protocol fixtures; real outcomes, credible assumptions, safety monitoring, value authority, and independent review remain absent.",
    "rollback_or_recovery": "Retain the failed fixture and keep causal-effect, participant-effect, and Stage 20 claims false.",
    "protected_gates": [
      "real_participants",
      "causal_effect",
      "value_authority",
      "independent_review",
      "stage20"
    ],
    "expected_disposition": "completed"
  }
]''')
SOURCES = json.loads(r'''[
  {
    "source_id": "SRC-LIVE-REQUEST",
    "title": "Hamish current v648-v6 activation and committed Sable baton",
    "url": null,
    "status": "current",
    "kind": "live_authority",
    "implication": "Controls solo ownership, no replay, x1-before-x2, four-commit cap, platform exclusions, privacy, and terminal route."
  },
  {
    "source_id": "SRC-RFC7464",
    "title": "RFC 7464 JSON Text Sequences",
    "url": "https://www.rfc-editor.org/info/rfc7464/",
    "status": "stable",
    "kind": "official_standard",
    "implication": "Defines record-separator framed UTF-8 JSON text sequences; it does not establish safe parsing for all inputs."
  },
  {
    "source_id": "SRC-JLD-PRIMARY",
    "title": "Bros and Epstein on Jost-Lehmann-Dyson representation and causality",
    "url": "https://doi.org/10.1016/j.physletb.2016.10.080",
    "status": "stable",
    "kind": "primary_research",
    "implication": "Supports formal causal and analytic obligations only, not empirical GMUT evidence."
  },
  {
    "source_id": "SRC-XRISM-HEASARC",
    "title": "NASA HEASARC XRISM Archive",
    "url": "https://heasarc.gsfc.nasa.gov/docs/xrism/archive/",
    "status": "current",
    "kind": "official_data",
    "implication": "Exposes an official archive surface and prerequisites, not a GMUT likelihood or observation used here."
  },
  {
    "source_id": "SRC-WORKSAFE-EVENTS",
    "title": "WorkSafe New Zealand managing risks at events",
    "url": "https://www.worksafe.govt.nz/topic-and-industry/event-management/managing-risks-at-events/",
    "status": "current",
    "kind": "official_authority",
    "implication": "Supplies general event-risk obligations; software fixtures confer no safety or workplace authority."
  },
  {
    "source_id": "SRC-RFC9396",
    "title": "RFC 9396 OAuth 2.0 Rich Authorization Requests",
    "url": "https://www.rfc-editor.org/info/rfc9396/",
    "status": "stable",
    "kind": "official_standard",
    "implication": "Defines authorization_details syntax and processing; synthetic vectors are not production authorization evidence."
  },
  {
    "source_id": "SRC-RFC9207",
    "title": "RFC 9207 OAuth 2.0 Authorization Server Issuer Identification",
    "url": "https://www.rfc-editor.org/info/rfc9207/",
    "status": "stable",
    "kind": "official_standard",
    "implication": "Provides an adjacent issuer-binding obligation without proving identity, authentication, or trust."
  },
  {
    "source_id": "SRC-OAUTH21-DRAFT",
    "title": "IETF OAuth 2.1 Authorization Framework draft",
    "url": "https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/",
    "status": "draft",
    "kind": "official_draft",
    "implication": "A live draft is monitored as work in progress and not flattened into settled authority."
  },
  {
    "source_id": "SRC-TIFF6",
    "title": "TIFF Revision 6.0 specification",
    "url": "https://www.itu.int/itudoc/itu-t/com16/tiff-fx/docs/tiff6.html",
    "status": "stable",
    "kind": "official_specification_copy",
    "implication": "Defines TIFF headers, IFDs, fields, strips and tiles for bounded structural fixtures."
  },
  {
    "source_id": "SRC-LOC-TIFF",
    "title": "Library of Congress TIFF format description",
    "url": "https://www.loc.gov/preservation/digital/formats/fdd/fdd000022.shtml",
    "status": "stable",
    "kind": "official_format_description",
    "implication": "Supplies preservation and format context without providing exhaustive decoder security."
  },
  {
    "source_id": "SRC-W3C-TABLES",
    "title": "W3C WAI Tables Tutorial",
    "url": "https://www.w3.org/WAI/tutorials/tables/",
    "status": "current",
    "kind": "official_guidance",
    "implication": "Supports structural table association patterns while manual and affected-user evaluation remain reserved."
  },
  {
    "source_id": "SRC-WCAG22",
    "title": "Web Content Accessibility Guidelines 2.2",
    "url": "https://www.w3.org/TR/WCAG22/",
    "status": "stable",
    "kind": "official_standard",
    "implication": "Structural checks cover only declared obligations and cannot close manual or affected-user evaluation."
  },
  {
    "source_id": "SRC-NIST-PLANCK",
    "title": "NIST Technical Note 910-8 radiance temperature and Planck law",
    "url": "https://nvlpubs.nist.gov/nistpubs/Legacy/TN/nbstechnicalnote910-8.pdf",
    "status": "stable",
    "kind": "primary_official_reference",
    "implication": "Supports physical radiance definitions and units only, never a psyche or value conversion."
  },
  {
    "source_id": "SRC-ICH-E9R1",
    "title": "ICH E9(R1) estimands and sensitivity analysis training material",
    "url": "https://database.ich.org/sites/default/files/E9%28R1%29%20Training%20Material%20-%20PDF_0.pdf",
    "status": "stable",
    "kind": "official_guideline",
    "implication": "Identifies intercurrent-event and estimand obligations; it is not participant evidence or Stage 20 authority."
  },
  {
    "source_id": "SRC-NZ-PRIVACY",
    "title": "New Zealand Privacy Commissioner obligations guidance",
    "url": "https://www.privacy.org.nz/responsibilities/your-obligations/",
    "status": "current",
    "kind": "official_authority",
    "implication": "Real privacy, correction, harm, disclosure, and remedy decisions require competent human authority and affected-person consideration."
  },
  {
    "source_id": "SRC-TE-MANA-RARAUNGA",
    "title": "Te Mana Raraunga principles of Māori data sovereignty",
    "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
    "status": "stable",
    "kind": "primary_authority_source",
    "implication": "Māori data and concepts remain under Māori governance; software confers no Māori authority."
  },
  {
    "source_id": "SRC-TE-PAPA-REPATRIATION",
    "title": "Te Papa domestic repatriation programme",
    "url": "https://www.tepapa.govt.nz/about/repatriation/domestic-repatriation",
    "status": "current",
    "kind": "primary_authority_context",
    "implication": "Demonstrates authority and relationship dependencies around cultural material without delegating them to this phase."
  },
  {
    "source_id": "SRC-OPENAI-CODEX",
    "title": "OpenAI Codex official repository and package channel",
    "url": "https://github.com/openai/codex",
    "status": "watch",
    "kind": "official_package",
    "implication": "CLI version status may be observed, but this phase performs no application update."
  },
  {
    "source_id": "SRC-OPENAI-CODEX-APP",
    "title": "OpenAI Codex app announcement",
    "url": "https://openai.com/index/introducing-the-codex-app/",
    "status": "current",
    "kind": "official_product",
    "implication": "Confirms the app surface; the installed desktop build is verified locally and not updated."
  }
]''')
SAFE_TASKS = json.loads(r'''[
  "Verify Sable source, x1, evidence, parent-count, zero-merge, clean, and live-remote anchors",
  "Ingest four inherited external post-final negatives without rewriting Sable's sealed count",
  "Record D-first capacity and fast-forward-only Orin lane continuity",
  "Audit all 610 frozen proposal titles and substantive neighbors with collision reasons",
  "Build the four-state official and primary source ledger without status flattening",
  "Freeze exactly ten proposals without x2 outcomes or completion claims",
  "Build immutable x1 Git-blob separation and staged-path receipts",
  "Run five-class privacy scanning with scanner-definition quarantine",
  "Record every timeout, no-match, parsing error, false assumption, and recovery",
  "Build and validate Method Flow fail/pass witness parity",
  "Refresh the phase-scoped GHC Family Index without global churn",
  "Run Reflection-Remaster as an additive audit and record reviewed-current disposition",
  "Freeze the JSON text-sequence parser tribunal plan",
  "Freeze the Jost-Lehmann-Dyson symbolic obligation plan",
  "Freeze the XRISM zero-row likelihood-refusal plan",
  "Freeze the theatre handover proxy plan",
  "Freeze the RFC 9396 synthetic authorization profile plan",
  "Freeze the live-performance CBR authority reservation plan",
  "Freeze the TIFF bounded parser tribunal plan",
  "Freeze the complex-table structural audit plan",
  "Freeze the Planck spectral-domain classifier plan",
  "Freeze the principal-stratification nonpromotion board plan",
  "Freeze 70 proposal-linked synthetic mutations without executing them",
  "Preserve inherited exact-approval and blocked packets as unexecuted",
  "Measure owner-generated file growth independently from inherited baseline",
  "Verify local and official Codex versions without updating software",
  "Record Sandbox and Hyper-V as excluded and untouched",
  "Reserve one successful canonical scoped pass and prohibit replay",
  "Preserve caller compatibility for family-current scripts and skills",
  "Keep terminal Tamar route prepared but unsent until exact final proof"
]''')
CANDIDATE_TASKS = json.loads(r'''[
  "JSON text-sequence boundary and recovery prototype",
  "JSON text-sequence byte and record budget prototype",
  "Jost-Lehmann-Dyson support-domain obligation prototype",
  "Jost-Lehmann-Dyson observation-firewall prototype",
  "XRISM schema and checksum prerequisite prototype",
  "XRISM zero-row likelihood refusal prototype",
  "Theatre cue revision and acknowledgement prototype",
  "Theatre stop-call authority-reservation prototype",
  "Theatre workload and handover prototype",
  "RFC 9396 type and field confinement prototype",
  "RFC 9396 narrowing and replay prototype",
  "Live-performance access and privacy reservation prototype",
  "TIFF header and IFD cycle prototype",
  "TIFF offset arithmetic and resource-budget prototype",
  "Complex-table multilevel association prototype",
  "Complex-table sort and fallback prototype",
  "Planck frequency-wavelength Jacobian prototype",
  "Planck psyche-value nonconversion prototype",
  "Principal-stratification identifiability prototype",
  "Stage 20 principal-stratification nonpromotion prototype"
]''')
SKILL_IDEAS = json.loads(r'''[
  "ghc-family-v648-v6-json-sequence-tribunal",
  "ghc-family-v648-v6-json-sequence-budget",
  "ghc-family-v648-v6-jld-obligation-board",
  "ghc-family-v648-v6-jld-observation-firewall",
  "ghc-family-v648-v6-xrism-refusal",
  "ghc-family-v648-v6-theatre-cue-lineage",
  "ghc-family-v648-v6-theatre-handover",
  "ghc-family-v648-v6-rich-authorization",
  "ghc-family-v648-v6-rich-authorization-minimization",
  "ghc-family-v648-v6-live-performance-reservation",
  "ghc-family-v648-v6-tiff-tribunal",
  "ghc-family-v648-v6-tiff-budget",
  "ghc-family-v648-v6-complex-table-association",
  "ghc-family-v648-v6-complex-table-fallback",
  "ghc-family-v648-v6-planck-domain",
  "ghc-family-v648-v6-planck-nonconversion",
  "ghc-family-v648-v6-principal-stratification",
  "ghc-family-v648-v6-stage20-nonpromotion",
  "ghc-family-v648-v6-method-flow-recovery",
  "ghc-family-v648-v6-terminal-proof"
]''')
RUNNER_IDEAS = json.loads(r'''[
  "ghc_family_v648_v6_json_sequence.py",
  "ghc_family_v648_v6_jld_obligations.py",
  "ghc_family_v648_v6_xrism_refusal.py",
  "ghc_family_v648_v6_theatre_handover.py",
  "ghc_family_v648_v6_rich_authorization.py",
  "ghc_family_v648_v6_tiff_tribunal.py",
  "ghc_family_v648_v6_accessibility_audit.py",
  "ghc_family_v648_v6_domain_guards.py",
  "ghc_family_v648_v6_portfolio.py",
  "build_ghc_family_v648_v6_closeout.py"
]''')
CLEANUP_TASKS = json.loads(r'''[
  "Normalize v648-v6 JSON ordering and UTF-8 output only",
  "Add explicit outcome vocabulary validation",
  "Add explicit source-status vocabulary validation",
  "Add exact proposal-count assertion",
  "Add exact frozen-chain count assertion",
  "Add source and lifecycle ancestry assertions",
  "Add zero-merge and final-parent assertions",
  "Add x1 and x2 contamination guards",
  "Add Git-blob versus checkout-byte domain labels",
  "Add five privacy class labels",
  "Add scanner-definition disposition",
  "Add document word-cap checks",
  "Add owner-file threshold measurement",
  "Add source citation not-observation flags",
  "Add same-owner and independent-reproduction separation",
  "Add Sandbox and Hyper-V no-action receipts",
  "Add desktop no-update receipt",
  "Add no-cross-platform-send receipt",
  "Add no-task and no-subagent receipt",
  "Add terminal route prepared-not-sent state",
  "Add accessibility manual-evaluation reservation",
  "Add Māori-language and authority reservation",
  "Add real-data and likelihood refusal fields",
  "Add participant and operator absence fields",
  "Add production identity absence fields",
  "Add exhaustive-security nonclaim fields",
  "Add rollback and recovery fields to every prototype",
  "Add protected-gate parity checks",
  "Add exact staged-path allowlist checks",
  "Add final remote-equality proof fields"
]''')
X1_OPERATIONAL_NEGATIVES = json.loads(r'''[
  {
    "negative_id": "V6486-X1-N01",
    "category": "comparison_literal_fault",
    "failed": "A source-equality wrapper compared tab-separated divergence output against a single-quoted escape literal and falsely rejected valid zero divergence.",
    "recovery": "Parse the two divergence values as integers and require both to equal zero.",
    "passing": "The corrected read-only proof showed local, upstream, tracking, and fresh live remote equal with zero divergence.",
    "recurrence_guard": "Never compare native tab output to an escaped single-quoted literal; parse fields."
  },
  {
    "negative_id": "V6486-X1-N02",
    "category": "hash_domain_assumption",
    "failed": "The first predecessor manifest audit compared declared checkout-byte counts with raw Git-blob sizes and falsely reported mismatches.",
    "recovery": "Verify Git blob identity in the blob domain and treat checkout bytes as a separately labelled working-tree domain.",
    "passing": "All predecessor lifecycle path sets and Git blob identities matched with the declared self-exclusions.",
    "recurrence_guard": "Do not mix filtered checkout byte counts with raw Git object byte sizes."
  },
  {
    "negative_id": "V6486-X1-N03",
    "category": "unbounded_status_output",
    "failed": "Fast-forward output emitted a very large inherited change summary that was truncated and therefore earned no proof credit.",
    "recovery": "Run compact exact head, branch, clean, divergence, tracking, and live-remote probes after the successful fast-forward and push.",
    "passing": "The compact proof established the Orin branch clean and four-way equal at Sable's exact final head.",
    "recurrence_guard": "Suppress or separate inherited change summaries; validate state with compact exact probes."
  },
  {
    "negative_id": "V6486-X1-N04",
    "category": "memory_registry_no_match",
    "failed": "The exact current-memory registry search returned no v648-v5 or v648-v6 continuity entry.",
    "recovery": "Retain the no-match and use the live activation, committed baton, and exact Git evidence as current authority.",
    "passing": "No continuity credit was inferred from memory silence; the current live and Git evidence controlled.",
    "recurrence_guard": "Treat exact-current memory absence as absence, not proof or contradiction."
  },
  {
    "negative_id": "V6486-X1-N05",
    "category": "parallel_read_timeout",
    "failed": "A four-way parallel source-read wrapper used a ten-second bound and timed out before returning attributable evidence.",
    "recovery": "Use bounded no-profile probes with a longer allowance and smaller output surfaces.",
    "passing": "The exact lane state and required source files were subsequently read successfully without mutation.",
    "recurrence_guard": "Do not bind multiple PowerShell startup-heavy reads to a ten-second aggregate timeout."
  },
  {
    "negative_id": "V6486-X1-N06",
    "category": "semantic_seed_collision",
    "failed": "The first novelty seed batch collided with frozen TAR/PAX, Schwinger-Dyson, Fermi-LAT, museum-repatriation, JAR, data-table, Gibbs-Duhem, and transportability proposals.",
    "recovery": "Retain the collisions, inspect exact semantic neighbors, and replace them with different mechanisms and domains.",
    "passing": "The surviving ten titles remained below the lexical threshold and received manual neighbor review against all 610 frozen proposals.",
    "recurrence_guard": "Treat plausible novelty as a hypothesis until both lexical and substantive neighbor audits pass."
  },
  {
    "negative_id": "V6486-X1-N07",
    "category": "broad_regex_false_neighbor",
    "failed": "A second seed batch collided with Git bundle, Peierls, Euclid, PNG, treegrid, and Joule-Thomson proposals, while a broad JWST or MAST alternation also matched unrelated master and remaster text.",
    "recovery": "Reject the collided seeds and use exact-token and proposal-title-domain searches before manual semantic review.",
    "passing": "Exact-token review separated false lexical hits from real semantic neighbors and yielded a bounded distinct set.",
    "recurrence_guard": "Use word-bounded exact identifiers and frozen proposal titles, not broad substrings, for novelty evidence."
  },
  {
    "negative_id": "V6486-X1-N08",
    "category": "truncated_scaffold_copy",
    "failed": "A tool-output copy of the predecessor preregistration builder was truncated before patching and produced a syntax-invalid untracked scaffold.",
    "recovery": "Replace only the owner-created untracked scaffold with a compact x1-specific builder and preflight it from the local file.",
    "passing": "The replacement builder compiled from the complete local file and preserved the definitions, test, and x1-only worktree boundary.",
    "recurrence_guard": "Never use display-truncated command output as source-file content; build compact successors or read bounded complete sections."
  },
  {
    "negative_id": "V6486-X1-N09",
    "category": "threshold_proposal_collision",
    "failed": "The first complete x1 generator preflight refused V6486-P06 at the exact 0.50 lexical threshold against the earlier telecommunications-outage authority matrix.",
    "recovery": "Retain the refusal and narrow the title to theatre cancellation, cultural-content stewardship, performer-audience confidentiality, ticket redress, consent provenance, taonga reservation, and decision rights without weakening its gates.",
    "passing": "The revised title passed the frozen-corpus threshold while the proposal body retained all affected-party, legal, disability, cultural, privacy, and Māori-authority reservations.",
    "recurrence_guard": "Do not rely on a generic authority-matrix title; expose the phase-specific mechanism while preserving the full gate body."
  },
  {
    "negative_id": "V6486-X1-N10",
    "category": "mechanical_owner_origin_drift",
    "failed": "The first x1 suite expected Sable's successor-origin label even though the generated v648-v6 packet correctly used Orin's owner label.",
    "recovery": "Correct only the owner-origin assertion to orin_v648_v6_new and rerun the bounded x1 suite.",
    "passing": "The corrected assertion matches every generated portfolio and package row attributed to Orin's new v648-v6 work.",
    "recurrence_guard": "Audit owner, slug, branch, and origin tokens independently after mechanical phase-number replacement."
  },
  {
    "negative_id": "V6486-X1-N11",
    "category": "premature_aggregate_rerun",
    "failed": "A broad x1 rerun followed the owner-origin correction before the new Method Flow pass witness and manifest refresh, producing expected lifecycle-parity and stale-hash failures.",
    "recovery": "Withhold aggregate credit, complete the pending Method Flow lifecycle, validate and summarize it, regenerate the manifest, and only then retry.",
    "passing": "The Method Flow ledger and exact x1 manifest were refreshed before the next aggregate attempt.",
    "recurrence_guard": "After any Method Flow or covered-file mutation, refresh lifecycle receipts and the exact manifest before a broad validation attempt."
  },
  {
    "negative_id": "V6486-X1-N12",
    "category": "inline_staged_review_parser_fault",
    "failed": "An inline PowerShell staged-review command failed to parse an embedded quote-bearing privacy regex before Git staging ran.",
    "recovery": "Use a dedicated UTF-8 Python runner with explicit staged-blob, manifest, JSON, diff-hygiene, and scanner-definition domains.",
    "passing": "The dedicated staged-review runner completed exact Git-index path, JSON, privacy, and diff-hygiene checks.",
    "recurrence_guard": "Do not embed quote-bearing privacy regexes inside a PowerShell inline Python string."
  },
  {
    "negative_id": "V6486-X1-N13",
    "category": "staged_diff_hygiene_failure",
    "failed": "The dedicated staged review reached git diff --cached --check, which rejected an extra blank line at EOF in the new runner.",
    "recovery": "Trim only the extra trailing blank line, preserve one final newline, regenerate covered hashes, and restage the exact surface.",
    "passing": "The corrected runner and exact staged surface passed diff hygiene in the dedicated review.",
    "recurrence_guard": "Run diff hygiene on every new runner before awarding staged-review credit."
  }
]''')
