#!/usr/bin/env python3
"""Frozen x1 definitions for Sable Rook v647-v7.

Importing this module performs no I/O and grants no x2 completion credit.
"""

from __future__ import annotations

from typing import Any


PHASE = "v647-gmut-thos-v7-x1-x2"
PHASE_SHORT = "v647-v7"
OWNER = "Sable Rook"
SLUG = "sable-rook"
PRONOUNS = "they/them"
ROLE = "evidence-and-reproducibility steward"
HOPE = "make every surviving claim easy to challenge, reproduce within its evidence class, or retract"
PRIMARY_FOCUS = "THOS Body"
BOUNDED_PRACTICE = "building-inspection record amendment, defect hold and reinspection, accessible notice, and shift handover"

SOURCE_PHASE = "v647-gmut-thos-v6-x1-x2"
SOURCE_BRANCH = "codex/GHC-Family/ilyra-fen-full-tools"
SOURCE_REVISION = "c02273291edcbe408f28647495183e9ed4641995"
SOURCE_INHERITED_REVISION = "3c4fa7ba58362ae39a5aa009fe9a899acc092301"
SOURCE_X1_REVISION = "650e9f0e6d17118cf8b2389adf2a984cfc63cf08"
SOURCE_EVIDENCE_REVISION = "400f5af29759a624bf4f095b50b4c7468e3a25b9"
PRIOR_FROZEN_PROPOSALS = 530
INHERITED_EFFECTIVE_NEGATIVES = 3669
PREREGISTERED_SYNTHETIC_NEGATIVES = 70
INHERITED_OPEN_GAPS = 23
INHERITED_EXACT_GATES = 24
OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]

IDENTITY_BOUNDARY = (
    "Sable Rook, they/them, is relational working language for an evidence-and-reproducibility steward. "
    "It is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, "
    "professional qualification, scientific authority, operational authority, legal authority, cultural authority, "
    "or independent agency. Hamish may rename, pause, redirect, or stop the work."
)
TRUTH_BOUNDARY = (
    "GMUT remains a typed scalar-tensor and effective-field-theory research-model family; THOS remains represented; "
    "Freed ID remains synthetic and nonproduction; CBR, building safety, accessibility, privacy, remedy, legal, "
    "cultural, affected-party, and Māori concepts remain under competent, affected-party, tangata whenua, iwi, hapū, "
    "and Māori authority. No empirical confirmation, Theory of Everything, AGI or ASI, consciousness, personhood, "
    "deployment, privacy-complete, exhaustive-security, independent-reproduction, accessibility-complete, "
    "professional, proof or canon, or Stage 20 claim is made."
)


def proposal(
    index: int,
    title: str,
    mission: str,
    hypothesis: str,
    failure: str,
    approval: str,
    lane: str,
    sources: list[str],
    artifacts: list[str],
    gate: str,
    recovery: str,
    protected: list[str],
    expected: str,
    novelty: str,
) -> dict[str, Any]:
    return {
        "proposal_id": f"V6477-P{index:02d}",
        "title": title,
        "mission_surface": mission,
        "hypothesis": hypothesis,
        "null_or_failure": failure,
        "approval_class": approval,
        "execution_lane": lane,
        "current_primary_or_official_source_needs": sources,
        "concrete_artifacts": artifacts,
        "test_falsifier_or_acceptance_gate": gate,
        "rollback_or_recovery": recovery,
        "protected_gates": protected,
        "expected_disposition": expected,
        "novelty_against_530_frozen_proposals": novelty,
    }


PROPOSALS = [
    proposal(
        1,
        "SLSA and in-toto subject-material digest, predicate-type, builder-boundary, and nontransitive evidence-credit tribunal",
        "attestation subject, materials, digests, predicate type, builder identity boundary, dependency edge, source independence, duplicate quarantine, and completion-credit isolation",
        "Bounded fixtures can reject digest drift, ambiguous subjects, foreign predicates, cyclic materials, duplicate attestations, and inherited completion credit without claiming complete provenance.",
        "A digest mismatch passes, duplicate or cyclic evidence gains independent credit, builder identity is treated as authority, or inherited artifacts become Sable completion credit without a fresh witness.",
        "safe_now_owner_scoped_workflow",
        "x2_build_task",
        ["V6477-S01", "V6477-S02"],
        ["provenance/attestation-contract.json", "provenance/attestation-mutations.json"],
        "Seven synthetic mutations must fail closed while one bounded valid fixture preserves exact digest and dependency semantics.",
        "Quarantine the disputed edge or attestation, retain the failure, recompute only disposable fixture digests, and keep provenance-complete and independent-source claims false.",
        ["canonical_evidence", "source_independence", "completion_credit", "production_attestation", "sibling_lane"],
        "completed",
        "The corpus has manifests, evidence DAGs, transparency logs, and supply-chain receipts, but no core title combines SLSA/in-toto subject and material semantics with nontransitive completion-credit isolation.",
    ),
    proposal(
        2,
        "GMUT Picard-Lefschetz contour, thimble, intersection-number, Stokes-wall, convergence, and reality obligation board",
        "canonical GMUT scalar-tensor/EFT scaffold, complexified fields, action convention, integration cycle, critical point, downward thimble, upward cycle, intersection number, Stokes wall, convergence, units, covariance, conservation, stability, identifiability, and observation firewall",
        "A typed symbolic board can expose contour-deformation and saddle obligations while retaining canonical units, covariance, conservation, stability, and identifiability boundaries.",
        "Orientation or sign conventions disappear, intersection numbers are invented, Stokes jumps are ignored, convergence is asserted globally, units drift, conservation is bypassed, or notation becomes a physical prediction.",
        "safe_now_symbolic_research_only",
        "x2_build_task",
        ["V6477-S03", "V6477-S04"],
        ["gmut/picard-lefschetz-obligations.json", "gmut/picard-lefschetz-mutations.json"],
        "Fixtures must type every contour, thimble, intersection, Stokes, unit, covariance, conservation, stability, identifiability, and nonpromotion obligation.",
        "Retain the failed obligation, restore declared conventions and the canonical scaffold, and make no likelihood, force, prediction, constraint, completion, or Theory-of-Everything claim.",
        ["empirical_confirmation", "physical_stability", "likelihood", "quantum_completion", "theory_of_everything"],
        "completed",
        "Earlier boards cover BRST, BV, functional RG, Schwinger-Keldysh, Vilkovisky-DeWitt, Barnes-Rivers, and spectral obligations, not Picard-Lefschetz thimbles and Stokes transitions.",
    ),
    proposal(
        3,
        "GMUT SPT-3G D1 bandpower, beam, window, calibration, covariance, nuisance, and zero-row likelihood-refusal protocol",
        "official release identity, spectrum family, bandpower schema, multipole bins, window functions, beam, calibration, covariance, foreground nuisance, checksum, frozen likelihood contract, and zero-row refusal",
        "A zero-row adapter can freeze current official SPT-3G D1 obligations while refusing to turn documentation or published results into GMUT observations, likelihoods, or constraints.",
        "The phase downloads rows, copies published bandpowers as observations, invents covariance or nuisance values, evaluates a likelihood, samples a posterior, or emits a physical constraint.",
        "real_data_access_and_independent_review_required",
        "x2_open_gap",
        ["V6477-S05", "V6477-S06"],
        ["empirical/spt3g-d1-study-contract.json", "empirical/spt3g-d1-zero-row-receipt.json"],
        "The receipt must preserve zero downloads, real rows, covariance rows, likelihood calls, posterior samples, parameter constraints, force claims, and empirical GMUT claims.",
        "Stop before data access or fitting and require separately authorized preregistration, frozen products, covariance, nuisance models, uncertainty treatment, baselines, and independent review.",
        ["network_data_access", "real_data", "likelihood", "posterior", "parameter_constraint", "empirical_confirmation", "independent_review"],
        "open_gap",
        "The 530-title corpus contains other cosmology releases and zero-row adapters but no SPT-3G D1 bandpower, beam, window, calibration, and covariance protocol.",
    ),
    proposal(
        4,
        "THOS building-inspection record amendment, defect hold, reinspection, correction-readback, accessible-notice, and shift-handover proxy",
        "synthetic consent token, inspection revision, defect code, hold state, evidence pointer, reinspection condition, amendment reason, correction readback, accessible notice, workload budget, escalation, and next-owner handover",
        "Synthetic event traces can expose stale inspection state, lost amendments, premature hold release, inaccessible notice, missing readback, and unowned handover without using real people, properties, or authorities.",
        "A fixture identifies a real person or property, changes a real consent or notice, releases a real hold, breaks matched budgets, or claims THOS effectiveness or professional competence.",
        "safe_now_proxy_protocol_no_people_or_operations",
        "x2_proxy_protocol",
        ["V6477-S07", "V6477-S08", "V6477-S09"],
        ["thos/building-inspection-handover-contract.json", "thos/building-inspection-handover-vectors.json"],
        "Unsafe traces must fail, and the packet must record zero real people, properties, consents, inspections, notices, authorities, matched-budget arms, outcomes, or effectiveness estimates.",
        "Withdraw operational language, retain rejected traces, minimize synthetic fields, and defer decisions to authorized building, accessibility, privacy, affected-party, legal, cultural, and Māori processes.",
        ["real_people", "real_property", "professional_authority", "public_safety", "deployment", "privacy_complete", "effectiveness"],
        "represented",
        "Prior handover proxies cover aviation, seismology, weather, health, and other practices, but no core title centers building-inspection amendment, defect hold, reinspection, and accessible notice.",
    ),
    proposal(
        5,
        "Freed ID OAuth protected-resource metadata, authorization-server binding, signed-metadata precedence, cache, downgrade, and privacy profile",
        "resource identifier, authorization servers, bearer methods, scopes supported, signed metadata, precedence, issuer and audience binding, cache freshness, redirect and downgrade refusal, metadata correlation, and privacy reservation",
        "Synthetic RFC 9728 vectors can enforce bounded protected-resource metadata structure and precedence without asserting real identity, authorization, keys, interoperability, or production readiness.",
        "Resource or issuer binding is absent, unsigned metadata overrides a valid signed object, cache expiry is ignored, redirects widen trust, downgrade passes, or synthetic values become authorization evidence.",
        "safe_now_synthetic_nonproduction",
        "x2_proxy_protocol",
        ["V6477-S11", "V6477-S12", "V6477-S13"],
        ["freed-id/oauth-resource-metadata-profile.json", "freed-id/oauth-resource-metadata-mutations.json"],
        "Vectors must reject binding, precedence, freshness, redirect, downgrade, scope, correlation, and production-promotion faults while retaining zero real accounts, keys, tokens, or servers.",
        "Reject the synthetic metadata, retain the vector, disclose no real identity data, and require conforming systems, real keys, live exchanges, interoperability, privacy/security review, recovery, and trust governance.",
        ["real_identity", "real_authorization", "real_keys", "real_tokens", "interoperability", "production"],
        "represented",
        "The corpus includes OAuth RAR, JAR, PAR, DPoP, token exchange, HAIP, and federation profiles, but no core proposal centered on RFC 9728 protected-resource metadata precedence and binding.",
    ),
    proposal(
        6,
        "CBR building-safety access, tenant impact, disability, privacy, remedy, legal, cultural, and Māori-authority matrix",
        "inspection access, occupancy impact, disability access, language, tenant and owner interests, location and evidence privacy, notice, response, remedy, appeal, legal interpretation, place data, affected parties, data governance, and Māori authority",
        "A refusal-first matrix can expose unresolved access, privacy, remedy, legal, cultural, and authority questions without deciding a real inspection, property right, notice, remedy, or cultural meaning.",
        "The matrix identifies a real person or property, authorizes access, decides occupancy or title, allocates remedy, interprets law or tikanga, asserts Māori authority, or treats public guidance as delegated case authority.",
        "authorized_affected_parties_and_competent_authority_required",
        "x2_exact_gate",
        ["V6477-S07", "V6477-S08", "V6477-S09", "V6477-S10"],
        ["cbr/building-authority-reservation.json", "cbr/building-remedy-matrix.json"],
        "Repository software must stop at unknown or reserved; only competent building, disability, privacy, tenancy, legal, affected-party, tangata whenua, iwi, hapū, and Māori authorities can close their gates.",
        "Stop before access, notice, occupancy, disclosure, cultural, data-governance, legal, property, or remedy conclusions; minimize data and route only through authorized external processes.",
        ["affected_party_authority", "disability_access", "privacy", "legal_interpretation", "maori_authority", "data_governance", "remedy_decision"],
        "exact_gate",
        "Earlier authority matrices cover weather, aviation, museums, emergency alerts, and other services, but none centers building inspection access, tenant impact, disability, privacy, and remedy authority.",
    ),
    proposal(
        7,
        "DNS wire-format label, compression-pointer cycle, bounds, section-count, EDNS-size, and refusal tribunal",
        "header, section counts, label length, total name length, compression pointer, backward-target policy, cycle and hop budget, record bounds, trailing bytes, EDNS payload size, truncation, and refusal",
        "A disposable DNS-wire tribunal can reject malformed and cyclic synthetic packets without performing network resolution or claiming a production DNS parser or exhaustive security.",
        "An oversized label, pointer cycle, out-of-bounds offset, inconsistent section count, truncated record, or budget breach passes; a network query occurs; or a fixture touches canonical state.",
        "safe_now_disposable_synthetic_only",
        "x2_build_task",
        ["V6477-S14", "V6477-S15", "V6477-S16"],
        ["tooling/dns-wire-contract.json", "tooling/dns-wire-mutations.json"],
        "Disposable fixtures must cover one bounded valid message plus exactly seven retained label, pointer, bounds, count, EDNS, truncation, and promotion faults.",
        "Discard only the disposable packet, retain each discrepancy, restore a bounded parser state, and keep resolver, interoperability, privacy, and exhaustive-security claims false.",
        ["network_resolution", "canonical_evidence", "sibling_lane", "production_parser", "interoperability", "exhaustive_security"],
        "completed",
        "The corpus has framing and archive tribunals including PNG, TAR, ZIP, HTTP, and OCI, but no core title centered on DNS compression-pointer cycles, section counts, and EDNS size.",
    ),
    proposal(
        8,
        "Accessible virtualized-feed position, busy-state, focus, update-throttling, pause, and export-alternative structural audit",
        "feed label, article identity, position and set size, busy state, focus persistence, insertion and removal, update frequency, pause control, nonvirtual fallback, export alternative, responsive and print order",
        "A structural audit can reject incoherent virtualization and focus semantics while reserving qualified manual keyboard, browser, assistive-technology, responsive, cognitive, language, and affected-user evaluation.",
        "Position or set size contradicts order, busy state is lost, focus vanishes, updates cannot pause, fallback or export loses data, or structural evidence becomes complete accessibility conformance.",
        "safe_now_structural_only",
        "x2_build_task",
        ["V6477-S09", "V6477-S17", "V6477-S18"],
        ["accessibility/virtualized-feed-contract.json", "accessibility/virtualized-feed-mutations.json"],
        "Fixtures must cover position, set size, busy state, focus, update throttling, pause, fallback, export, responsive and print alternatives, plus explicit manual reservations.",
        "Mark the structure incomplete, retain failures, restore coherent state and focus, and require qualified manual browser, assistive-technology, responsive, cognitive, Māori-language, and affected-user evaluation.",
        ["accessibility_complete", "runtime_browser", "assistive_technology", "responsive_evaluation", "maori_language", "affected_user_acceptance"],
        "completed",
        "Prior accessibility titles cover tables, charts, treegrids, carousels, timelines, maps, forms, and feeds only as supporting patterns, not a core virtualized-feed state and export audit.",
    ),
    proposal(
        9,
        "Thermo/Psyche fugacity, activity-coefficient, standard-state, chemical-potential, ideal-limit, and agency-nonconversion classifier",
        "chemical potential, fugacity, reference pressure, activity, activity coefficient, standard state, temperature, phase, ideal-gas limit, dimensions, logarithm domain, and category barrier",
        "A typed classifier can validate bounded fugacity and activity relations while rejecting conversion into psyche, autonomy, justice, capability, consciousness, or personhood claims.",
        "The standard state disappears, dimensional logarithms pass, phase or temperature scope drifts, the ideal limit is misstated, or fugacity becomes a psychological or moral quantity.",
        "safe_now_symbolic_only",
        "x2_build_task",
        ["V6477-S19", "V6477-S20"],
        ["thermo-psyche/fugacity-contract.json", "thermo-psyche/fugacity-mutations.json"],
        "Fixtures must enforce standard state, dimensions, domain, ideal limit, phase scope, chemical-potential relation, and a hard psyche and agency category barrier.",
        "Restore the physical thermodynamic domain and explicit standard state, retain the rejection, and require independently valid human theory, measures, authority, and participant evidence before human inference.",
        ["participant_inference", "psyche_claim", "agency_claim", "justice_claim", "consciousness", "fundamental_law"],
        "completed",
        "Earlier titles cover chemical potential, Gibbs-Duhem, Maxwell relations, phase rules, and other identities, but no core title centers fugacity, activity coefficient, standard state, and ideal-limit nonconversion.",
    ),
    proposal(
        10,
        "Stage 20 Rosenbaum hidden-bias gamma, matched-set sensitivity, outcome-model, value-authority, and nonpromotion board",
        "observational design, matched set, treatment assignment odds, hidden-bias gamma, sharp null, test statistic, sensitivity interval, observed-covariate assumptions, outcome-model separation, subgroup, decision authority, and abstention",
        "A fail-closed structural board can preserve hidden-bias sensitivity obligations and quarantine promotion when design, matching, gamma interpretation, model scope, subgroup behavior, or authority is absent.",
        "Gamma is treated as measured confounding, matching defects disappear, outcome models substitute for design, subgroup failures vanish, a value judgment is automated, or Stage 20 advances.",
        "safe_now_structural_only",
        "x2_build_task",
        ["V6477-S21", "V6477-S22"],
        ["stage20/rosenbaum-sensitivity-contract.json", "stage20/rosenbaum-sensitivity-mutations.json"],
        "Mutations must reject gamma overinterpretation, missing design assumptions, broken matched sets, outcome-model substitution, subgroup erasure, authority substitution, and Stage 20 promotion.",
        "Withdraw affected evidence credit, retain assumptions and failures, require preregistered analysis and independent review, and abstain from causal, policy, or Stage 20 promotion.",
        ["stage20", "participant_evidence", "causal_claim", "decision_authority", "independent_reproduction"],
        "completed",
        "Prior Stage 20 boards cover HARKing, covariate shift, optional stopping, missingness, leakage, multiplicity, and registered reports, not Rosenbaum gamma sensitivity and value-authority nonpromotion.",
    ),
]


SOURCES = [
    {"source_id": "V6477-S01", "title": "SLSA Specification v1.2", "url": "https://slsa.dev/spec/v1.2/", "publisher": "SLSA", "status": "current", "source_class": "official_specification", "use": "supply-chain provenance vocabulary and level boundaries only"},
    {"source_id": "V6477-S02", "title": "in-toto Attestation Framework v1.2", "url": "https://github.com/in-toto/attestation/blob/main/spec/README.md", "publisher": "in-toto", "status": "current", "source_class": "official_specification", "use": "subject predicate and statement structure only"},
    {"source_id": "V6477-S03", "title": "Analytic Continuation Of Chern-Simons Theory", "url": "https://arxiv.org/abs/1001.2933", "publisher": "Edward Witten", "status": "stable", "source_class": "primary_research", "use": "Picard-Lefschetz contour and thimble provenance only"},
    {"source_id": "V6477-S04", "title": "Lefschetz-thimble techniques for path integrals", "url": "https://arxiv.org/abs/1512.08039", "publisher": "Tanizaki and collaborators", "status": "stable", "source_class": "primary_research", "use": "Stokes and saddle obligation context only"},
    {"source_id": "V6477-S05", "title": "South Pole Telescope public data releases", "url": "https://pole.uchicago.edu/public/Data%20Releases.html", "publisher": "South Pole Telescope", "status": "current", "source_class": "official_data_release", "use": "zero-row release provenance only"},
    {"source_id": "V6477-S06", "title": "SPT-3G D1 TT TE EE data release", "url": "https://pole.uchicago.edu/public/data/camphuis25/index.html", "publisher": "South Pole Telescope", "status": "current", "source_class": "official_data_release", "use": "bandpower beam window covariance obligations only; no rows imported"},
    {"source_id": "V6477-S07", "title": "Building Act 2004", "url": "https://www.legislation.govt.nz/act/public/2004/0072/latest/whole.html", "publisher": "New Zealand Legislation", "status": "current", "source_class": "official_legislation", "use": "authority reservation and notice vocabulary; no legal interpretation"},
    {"source_id": "V6477-S08", "title": "Issuing notices to fix", "url": "https://www.building.govt.nz/building-officials/guides-for-building-officials/issuing-notices-to-fix", "publisher": "MBIE Building Performance", "status": "current", "source_class": "official_guidance", "use": "record and hold-point context only"},
    {"source_id": "V6477-S09", "title": "Web Content Accessibility Guidelines 2.2", "url": "https://www.w3.org/TR/WCAG22/", "publisher": "W3C", "status": "stable", "source_class": "official_standard", "use": "structural accessibility reservation context"},
    {"source_id": "V6477-S10", "title": "Principles of Māori Data Sovereignty", "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "publisher": "Te Mana Raraunga", "status": "current", "source_class": "maori_authority_source", "use": "authority and data-governance gate; never delegated authority"},
    {"source_id": "V6477-S11", "title": "RFC 9728 OAuth 2.0 Protected Resource Metadata", "url": "https://www.rfc-editor.org/rfc/rfc9728.html", "publisher": "IETF RFC Editor", "status": "stable", "source_class": "official_standard", "use": "synthetic protected-resource metadata structure"},
    {"source_id": "V6477-S12", "title": "RFC 8414 OAuth 2.0 Authorization Server Metadata", "url": "https://www.rfc-editor.org/rfc/rfc8414.html", "publisher": "IETF RFC Editor", "status": "stable", "source_class": "official_standard", "use": "metadata and signed-object relationship context"},
    {"source_id": "V6477-S13", "title": "RFC 8707 Resource Indicators for OAuth 2.0", "url": "https://www.rfc-editor.org/rfc/rfc8707.html", "publisher": "IETF RFC Editor", "status": "stable", "source_class": "official_standard", "use": "resource and audience binding context"},
    {"source_id": "V6477-S14", "title": "RFC 1035 Domain Names Implementation and Specification", "url": "https://www.rfc-editor.org/rfc/rfc1035.html", "publisher": "IETF RFC Editor", "status": "stable", "source_class": "official_standard", "use": "DNS wire label and compression structure"},
    {"source_id": "V6477-S15", "title": "RFC 9267 DNS Resource Record Processing Anti-Patterns", "url": "https://www.rfc-editor.org/rfc/rfc9267.html", "publisher": "IETF RFC Editor", "status": "stable", "source_class": "official_standard", "use": "pointer and bounds failure context"},
    {"source_id": "V6477-S16", "title": "RFC 6891 Extension Mechanisms for DNS", "url": "https://www.rfc-editor.org/rfc/rfc6891.html", "publisher": "IETF RFC Editor", "status": "stable", "source_class": "official_standard", "use": "EDNS payload size obligations"},
    {"source_id": "V6477-S17", "title": "ARIA Authoring Practices Feed Pattern", "url": "https://www.w3.org/WAI/ARIA/apg/patterns/feed/", "publisher": "W3C Web Accessibility Initiative", "status": "current", "source_class": "official_guidance", "use": "feed focus and navigation reservations"},
    {"source_id": "V6477-S18", "title": "WAI-ARIA 1.2", "url": "https://www.w3.org/TR/wai-aria-1.2/", "publisher": "W3C", "status": "stable", "source_class": "official_standard", "use": "feed article position and busy-state semantics"},
    {"source_id": "V6477-S19", "title": "IUPAC Gold Book fugacity", "url": "https://goldbook.iupac.org/terms/view/F02543", "publisher": "IUPAC", "status": "current", "source_class": "official_terminology", "use": "fugacity definition and physical domain"},
    {"source_id": "V6477-S20", "title": "IUPAC Gold Book activity coefficient", "url": "https://goldbook.iupac.org/terms/view/A00116", "publisher": "IUPAC", "status": "current", "source_class": "official_terminology", "use": "activity coefficient and standard-state context"},
    {"source_id": "V6477-S21", "title": "Sensitivity to Hidden Bias", "url": "https://doi.org/10.1007/978-1-4757-3692-2_4", "publisher": "Paul R. Rosenbaum", "status": "stable", "source_class": "primary_research", "use": "matched observational sensitivity framework"},
    {"source_id": "V6477-S22", "title": "Sensitivity Analyses Informed by Tests for Bias in Observational Studies", "url": "https://doi.org/10.1111/biom.13558", "publisher": "Paul R. Rosenbaum", "status": "stable", "source_class": "primary_research", "use": "hidden-bias sensitivity and design limitations"},
]


SAFE_TASK_TITLES = [
    "Reconcile the 530-proposal chain into one Sable v647-v7 frozen index",
    "Quarantine exact and bounded semantic neighbors for all ten Sable proposals",
    "Audit twenty-two sources inside current stable draft or watch vocabulary",
    "Keep citation documentation observation and data classes noncompensating",
    "Retain the first bounded skill-read timeout before recovery credit",
    "Seal x1-only intended paths against x2 implementation and outcome bytes",
    "Adjudicate five privacy and raw-identifier classes on exact staged blobs",
    "Record THOS Body focus and building-practice nonauthority boundaries",
    "Measure only new Sable files against the fifteen-thousand-file threshold",
    "Capture v647-v7 verify-only Codex ChatGPT Python Git and PowerShell versions",
    "Keep Windows Sandbox unavailable state read-only and fail closed",
    "Guard the four permitted core outcome labels and expected distribution",
    "Carry twenty-three open gaps and twenty-four exact gates without closure",
    "Reconcile the 3669-negative activation baseline and every new failure",
    "Hold the Orin route at PREPARED_NOT_SENT until exact-final proof",
    "Specify in-toto subject material digest and credit-isolation fixtures",
    "Specify Picard-Lefschetz contour thimble and Stokes obligations",
    "Specify SPT-3G D1 zero-row calibration and covariance refusal",
    "Specify building-inspection amendment hold and handover states",
    "Specify OAuth protected-resource metadata precedence vectors",
    "Specify building access privacy remedy and authority reservations",
    "Specify DNS compression pointer bounds and EDNS fixtures",
    "Specify virtualized-feed focus pause and export alternatives",
    "Specify fugacity standard-state and nonconversion fixtures",
    "Specify Rosenbaum hidden-bias and Stage 20 abstention fixtures",
    "Specify accessible static-report landmarks and manual reservations",
    "Enforce deterministic JSON ordering UTF-8 LF and one terminal newline",
    "Declare Git-blob Git-index clean-filter and checkout-byte hash domains",
    "Preserve family-current callers and historical aliases additively",
    "Emit workload wellbeing corrigibility and user-stop receipts",
]

CANDIDATE_TITLES = [
    "In-toto subject-material digest mismatch quarantine prototype",
    "SLSA builder-boundary and nontransitive evidence-credit prototype",
    "Picard-Lefschetz thimble orientation and intersection prototype",
    "Picard-Lefschetz Stokes-wall convergence and observation-firewall prototype",
    "SPT-3G D1 release beam window and checksum prototype",
    "SPT-3G D1 covariance nuisance and zero-row refusal prototype",
    "Building-inspection amendment defect-hold and reinspection prototype",
    "Building accessible-notice correction-readback and handover prototype",
    "OAuth protected-resource signed-metadata precedence prototype",
    "OAuth resource binding cache downgrade and correlation prototype",
    "Building access disability privacy and remedy reservation prototype",
    "Māori building-data and place-context authority reservation prototype",
    "DNS label section-count and record-bounds prototype",
    "DNS compression-cycle EDNS-budget and truncation prototype",
    "Virtualized-feed position busy-state and focus prototype",
    "Virtualized-feed update pause fallback and export prototype",
    "Fugacity standard-state dimension and ideal-limit prototype",
    "Fugacity activity chemical-potential and agency-barrier prototype",
    "Rosenbaum matched-set gamma and design-assumption prototype",
    "Rosenbaum subgroup value-authority and nonpromotion prototype",
]

SKILL_SPECS = [
    ("ghc-family-in-toto-credit-isolation", "Audit attestation digests dependencies and nontransitive evidence credit"),
    ("ghc-family-picard-lefschetz-obligations", "Audit contour thimble Stokes and nonpromotion obligations"),
    ("ghc-family-spt3g-d1-zero-row", "Preserve a zero-row SPT-3G D1 study boundary"),
    ("ghc-family-building-inspection-handover", "Audit synthetic inspection amendment hold and shift handover"),
    ("ghc-family-oauth-resource-metadata", "Audit synthetic OAuth protected-resource metadata and precedence"),
    ("ghc-family-building-authority-reservation", "Reserve building access remedy legal and Māori authority gates"),
    ("ghc-family-dns-wire-tribunal", "Audit disposable DNS wire-format and compression fixtures"),
    ("ghc-family-virtualized-feed-audit", "Audit feed position focus pause and alternative structure"),
    ("ghc-family-fugacity-domain-guard", "Keep fugacity and activity reasoning inside thermodynamics"),
    ("ghc-family-rosenbaum-nonpromotion", "Guard hidden-bias sensitivity from Stage 20 promotion"),
    ("ghc-family-530-neighbor-quarantine", "Audit semantic novelty against 530 frozen proposals"),
    ("ghc-family-source-seal-ancestry-v7", "Verify exact source anchors and single-parent ancestry"),
    ("ghc-family-hash-domain-declaration-v7", "Separate Git blob index clean-filter and checkout-byte evidence"),
    ("ghc-family-x1-immutable-surface-v7", "Seal x1 plans against later implementation drift"),
    ("ghc-family-scanner-payload-adjudication-v5", "Separate scanner candidates from confirmed payload hits"),
    ("ghc-family-explicit-json-output-v2", "Require explicit JSON filenames for validation outputs"),
    ("ghc-family-method-single-failure-promotion", "Promote a recovery only after a retained failure and passing witness"),
    ("ghc-family-named-replay-one-shot-v5", "Keep the exact-final replay local upstream-free and single-run"),
    ("ghc-family-route-hold-four-way-v4", "Hold one baton until four-way equality and replay proof"),
    ("ghc-family-building-accessibility-reservation", "Reserve manual affected-user and authority review for building outputs"),
]

RUNNER_TITLES = [
    "ghc_family_in_toto_provenance_tribunal.py",
    "ghc_family_picard_lefschetz_obligations.py",
    "ghc_family_spt3g_d1_zero_row.py",
    "ghc_family_building_inspection_handover.py",
    "ghc_family_oauth_resource_metadata.py",
    "ghc_family_dns_wire_tribunal.py",
    "ghc_family_virtualized_feed_audit.py",
    "ghc_family_fugacity_domain_guard.py",
    "ghc_family_rosenbaum_nonpromotion.py",
    "ghc_family_v647_v7_validation_runner.py",
]

CLEAN_TASK_TITLES = [
    "Refresh v647-v7 count mirrors only from authoritative ledgers",
    "Preserve every inherited and new negative as an additive row",
    "Normalize new Sable text in the prospective Git-blob domain",
    "Keep x1 blob seals independent of Windows checkout line endings",
    "Use bounded no-profile reads after the retained short-wrapper timeout",
    "Quote or resolve every PowerShell revision expression before Git use",
    "Use built-in deterministic JSON without installing optional utilities",
    "Pin UTF-8 before every Unicode-emitting child process",
    "Review five privacy classes only across exact intended paths",
    "Keep every scanner candidate visible until exact adjudication",
    "Refresh lifecycle manifests after each authorized document change",
    "Keep manifest self-exclusions explicit minimal and counted",
    "Verify every family-current caller before adding a wrapper",
    "Retain historical tools as compatibility evidence",
    "Rebuild the accessible static report with fallback and export paths",
    "Reserve qualified manual keyboard browser and assistive-technology evaluation for v647-v7 outputs",
    "Verify every phase document remains below six thousand words",
    "Verify new Sable file growth remains below fifteen thousand",
    "Check source x1 evidence and final ancestry as separate assertions",
    "Check the four-commit cap and zero-merge phase history",
    "Check the final commit has exactly one parent",
    "Check local upstream tracking and fresh live remote equality",
    "Prove the v647-v7 named replay remains local upstream-free and remote-absent",
    "Keep inherited exact and blocked packets visible and unexecuted",
    "Keep SPT network real-row and likelihood counters at zero",
    "Keep Freed ID real-key token and server counters at zero",
    "Keep THOS real-person property and authority counters at zero",
    "Keep v647-v7 CBR legal cultural remedy and Māori decision counters at zero",
    "Refresh the phase-scoped GHC Family Index at every lifecycle boundary",
    "Hold the terminal route until canonical and named-replay proof",
]

X1_OPERATIONAL_NEGATIVES = [
    {
        "negative_id": "V6477-X1-N01",
        "failure": "The first complete skill-creator instruction read exceeded a ten-second shell wrapper and returned no content.",
        "recovery": "Retain the timeout, use a no-profile sixty-second wrapper, and read the unchanged skill and required reference completely.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6477-X1-N02",
        "failure": "The first normalized portfolio audit stopped on four exact inherited title collisions before proposal-packet materialization.",
        "recovery": "Retain the collision witness, rewrite only the four Sable labels without changing their gates, and rerun the unchanged audit to zero collisions.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6477-X1-N03",
        "failure": "A stale-label ripgrep probe passed a PowerShell-style wildcard as a literal Windows path and ended with an invalid-filename error.",
        "recovery": "Retain the partial output and error, enumerate matching files with rg --files, then pass exact paths to the unchanged stale-label search.",
        "result": "retained_then_recovered",
    },
]
