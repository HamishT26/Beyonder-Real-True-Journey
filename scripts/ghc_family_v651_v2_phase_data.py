#!/usr/bin/env python3
"""Frozen Orin Thale v651-v2 x1 data; no x2 observations live here."""

from __future__ import annotations


PHASE = "v651-v2"
OWNER = "Orin Thale"
PRONOUNS = "they/them"
ROLE = "relational boundary-and-method steward"
HOPE = "keep every surviving claim inspectable, challengeable, and safely retractable"
BRANCH = "codex/GHC-Family/orin-thale-v642-v6-full-tools"
PHASE_ROOT = "docs/orin-thale/v651-v2"

SOURCE_BRANCH = "codex/GHC-Family/sable-rook-full-tools"
SOURCE_HEAD = "ad2b530c2449656b54ac0fee1a1284208c2a6a75"
SOURCE_ORIGIN = "b8d2d25747fcda747f77e6cf788a87e95062de00"
SOURCE_X1 = "1deba4184dfb6d017dff04b11e526a6e3730edb3"
SOURCE_EVIDENCE = "79d6d3675763eb553dc43b64f0e83915c1739655"
SOURCE_CLOSEOUT = "f6c8cd16327ef3c8f474ab94200095ec3620de3a"
PRIOR_FROZEN = 920
INHERITED_NEGATIVES = 6565
STARTUP_NEGATIVES = 9
INHERITED_OPEN_GAPS = 51
INHERITED_EXACT_GATES = 52
PRIMARY_FOCUS = "THOS Body"
BOUNDED_PRACTICE = (
    "software and timed-text localization quality assurance, correction readback, "
    "accessibility fallback, workload control, and shift handover as a synthetic "
    "learning and interface-design lens only"
)

OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]
SOURCE_STATUS_CLASSES = ["current", "stable", "draft", "watch"]
PROTECTED = [
    "empirical_data",
    "real_participants_or_operators",
    "professional_or_operational_authority",
    "production_identity",
    "privacy_complete",
    "exhaustive_security",
    "complete_accessibility",
    "legal_cultural_and_maori_authority",
    "affected_party_acceptance",
    "independent_reproduction",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]


def proposal(number, title, slug, pillar, disposition, sources, mission, novelty):
    if disposition == "open_gap":
        approval = "candidate_empirical_evidence_and_independent_review_required"
        lane = "x2_zero_row_readiness_only"
        gate = "Emit a zero-row receipt and refuse every query, download, ingestion, fit, likelihood, posterior, constraint, or empirical promotion."
    elif disposition == "exact_gate":
        approval = "exact_affected_party_competent_and_maori_authority_required"
        lane = "x2_reservation_matrix_only"
        gate = "Emit reservations only; make no service, remedy, legal, cultural, language-authority, data-governance, or Maori-authority decision."
    elif disposition == "represented":
        approval = "candidate_bounded_synthetic_proxy"
        lane = "x2_synthetic_proxy_only"
        gate = "Reject every preregistered mutation and retain proxy status with zero participant, production, professional, operational, translation, or authority credit."
    else:
        approval = "safe_now_bounded_software_symbolic_formal_or_structural"
        lane = "x2_bounded_owner_local"
        gate = "Reject every preregistered mutation and emit only the declared bounded software, symbolic, formal, numerical, or structural completion."
    return {
        "proposal_id": f"V6512-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar": pillar,
        "mission_surface": mission,
        "hypothesis": f"A bounded {mission} artifact can expose its declared obligations and refusal states without promoting unsupported scientific, operational, identity, accessibility, or authority claims.",
        "null_or_failure_condition": f"The artifact omits a declared {mission} obligation, accepts a preregistered mutation, erases a negative, or promotes a result beyond its evidence lane.",
        "approval_class": approval,
        "execution_lane": lane,
        "official_or_primary_source_needs": sources,
        "concrete_artifacts": [
            f"surfaces/{slug}/contract.json",
            f"surfaces/{slug}/mutation-results.json",
            f"surfaces/{slug}/bounded-receipt.json",
        ],
        "falsifier_or_acceptance_gate": gate,
        "rollback_or_recovery": "Stop the proposal, retain every failed witness, rewrite no history, and leave external, sibling, participant, production, account, credential, and authority state unchanged.",
        "protected_gates": PROTECTED,
        "expected_disposition": disposition,
        "novelty_against_920_frozen_proposals": novelty,
    }


PROPOSALS = [
    proposal(1, "Method Flow Chandy-Lamport marker, process-state, FIFO-channel, in-transit-message, consistent-cut, stable-property, cancellation, teardown, and evidence-credit tribunal", "distributed-snapshot", "THOS Body", "completed", ["SRC-CHANDY-LAMPORT"], "distributed-snapshot consistent-cut control", "No frozen proposal isolates marker initiation, per-process state, FIFO channel capture, in-transit messages, consistent cuts, stable-property scope, cancellation, teardown, and evidence credit."),
    proposal(2, "Sigstore bundle media-type, artifact-digest, verification-material, certificate-identity, inclusion-promise, inclusion-proof, checkpoint, time, offline-boundary, and nontransitive-credit tribunal", "sigstore-bundle", "Freed ID and CBR Heart", "completed", ["SRC-SIGSTORE-BUNDLE"], "Sigstore bundle verification-material structure", "Earlier DSSE, SLSA, in-toto, TUF, and transparency-log work does not isolate the Sigstore bundle media type, artifact binding, certificate identity, proof variants, checkpoints, and offline boundary together."),
    proposal(3, "GMUT Galileon symmetry, derivative-counting, total-derivative variation, loop-correction, heavy-field, counterterm, cutoff, EFT, unit, and observation-firewall board", "galileon-nonrenormalization", "GMUT Mind", "completed", ["SRC-GALILEON"], "Galileon nonrenormalization obligations", "DHOST and scalar-tensor boards exist, but no frozen proposal isolates Galileon symmetry, derivative counting, total-derivative variation, loop and heavy-field qualifications, counterterms, cutoff, and observation refusal."),
    proposal(4, "GMUT Vainshtein radius, branch, source-profile, derivative-interaction, screened-unscreened regime, matching, time-dependence, EFT, unit, and observation-firewall board", "vainshtein-screening", "GMUT Mind", "completed", ["SRC-VAINSHTEIN"], "Vainshtein screening obligations", "No frozen proposal isolates source profiles, branch selection, Vainshtein-radius assumptions, regime matching, time dependence, EFT domain, units, and observation refusal."),
    proposal(5, "GMUT Hubble Source Catalog v3.1 match, visit, source, photometry, quality, variability, selection, checksum, covariance, version-watch, and zero-row likelihood-refusal adapter", "hubble-hsc-zero-row", "GMUT Mind", "open_gap", ["SRC-HUBBLE-HSC"], "Hubble Source Catalog readiness", "No frozen zero-row adapter targets Hubble Source Catalog v3.1 visit-source matching, photometry, quality, variability, selection, version watch, checksum, covariance, and likelihood refusal."),
    proposal(6, "THOS software-localization source-string, translation-memory, terminology, placeholder, plural-select, locale-fallback, bidirectionality, accessibility, correction-readback, workload, and handover proxy", "software-localization", "THOS Body", "represented", ["SRC-W3C-I18N"], "software-localization quality workflow", "No frozen practice proxy isolates source strings, translation-memory and terminology versions, placeholders, plural and select branches, locale fallback, bidirectionality, accessibility, correction readback, workload, and handover."),
    proposal(7, "THOS timed-text localization cue, timecode, overlap, reading-load proxy, line-break, speaker, sound-label, language, late-change, correction-readback, accessibility-fallback, workload, and handover proxy", "timed-text-localization", "THOS Body", "represented", ["SRC-W3C-TIMED-TEXT", "SRC-WAI-CAPTIONS"], "timed-text localization quality workflow", "Earlier caption accessibility audits do not model the localization operations lane of cue timing, overlap, reading-load proxy, line breaks, speaker and sound labels, language, late change, correction, workload, and handover."),
    proposal(8, "Freed ID RFC 8392 CWT claim-key, issuer, subject, audience, numeric-date, token-id, tag, COSE-container, nested-protection, minimization, replay, and nonproduction profile", "cwt-profile", "Freed ID and CBR Heart", "represented", ["SRC-RFC8392"], "CBOR Web Token claim and container profile", "No frozen identity proposal targets RFC 8392 claim keys, NumericDate handling, CWT and COSE tags, nested protection, minimization, replay, and nonproduction boundaries."),
    proposal(9, "Freed ID W3C FedCM draft manifest, config, accounts, client-metadata, assertion, login-status, connected-account, browser-mediation, disconnect, correlation, draft-status, and nonproduction profile", "fedcm-draft", "Freed ID and CBR Heart", "represented", ["SRC-W3C-FEDCM"], "FedCM browser-mediated identity profile", "No frozen identity proposal targets FedCM manifests, endpoints, login status, connected accounts, browser mediation, disconnect, correlation, current draft status, and nonproduction refusal."),
    proposal(10, "CBR localization language-access, disability, translator-contributor privacy, correction, remedy, cultural-expression, terminology stewardship, affected-party, legal, data-governance, and Maori-wording-and-authority matrix", "localization-authority", "Freed ID and CBR Heart", "exact_gate", ["SRC-NZ-LANGUAGE", "SRC-NZ-HRA", "SRC-NZ-PRIVACY", "SRC-TE-MANA-RARAUNGA"], "localization access, remedy, and authority reservation", "No frozen matrix combines localization language access, disability, contributor privacy, correction and remedy, cultural expression, terminology stewardship, affected-party legitimacy, and Maori wording, data, and authority reservations."),
    proposal(11, "ICC.2:2019 iccMAX header, tag-table, offset, length, overlap, spectral-PCS, calculator-element, processing-element, profile-connection-condition, resource-budget, and refusal tribunal", "iccmax-profile", "THOS Body", "completed", ["SRC-ICC2"], "iccMAX profile structural refusal", "No frozen format tribunal targets ICC.2:2019 iccMAX spectral PCS, calculator and processing elements, profile connection conditions, tag bounds, overlap, and resource budgets."),
    proposal(12, "OGC GeoTIFF 1.1 TIFF-tag, GeoKeyDirectory, key-entry, value-offset, model-tiepoint, pixel-scale, transformation, CRS-code, user-defined-parameter, resource-budget, and refusal tribunal", "geotiff-1-1", "THOS Body", "completed", ["SRC-GEOTIFF11"], "GeoTIFF 1.1 structural refusal", "No frozen format tribunal targets GeoTIFF 1.1 GeoKey directories, value indirection, model transforms, CRS codes, user-defined parameters, and bounded refusal."),
    proposal(13, "NTPv4 leap, version, mode, stratum, poll, precision, root-distance, reference-id, era, timestamp-order, origin-binding, kiss-code, extension, resource-budget, and refusal tribunal", "ntpv4", "THOS Body", "completed", ["SRC-RFC5905"], "NTPv4 packet and state refusal", "No frozen protocol tribunal isolates NTPv4 header fields, era handling, four-timestamp binding, kiss codes, extensions, updated-standard watch, and resource budgets."),
    proposal(14, "MQTT 5 fixed-header, remaining-length, packet-type, property-length, duplicate-property, topic-alias, subscription-id, QoS-state, session-expiry, reason-code, resource-budget, and refusal tribunal", "mqtt-5", "THOS Body", "completed", ["SRC-MQTT5"], "MQTT 5 packet and state refusal", "No frozen protocol tribunal isolates MQTT 5 variable-byte lengths, property multiplicity, topic aliases, subscription identifiers, QoS transitions, session expiry, reason codes, and budgets."),
    proposal(15, "Accessible locale-switcher current-language, target-language, native-name, direction, focus, announcement, error-association, persistence, fallback, truncation, zoom, print, and manual-evaluation audit", "accessible-locale-switcher", "THOS Body", "completed", ["SRC-WCAG22", "SRC-W3C-I18N"], "accessible locale-switcher structure", "No frozen accessibility audit isolates locale switcher language identity, native names, direction changes, focus and announcements, error association, persistence, fallback, truncation, zoom, and print together."),
    proposal(16, "Thermo-Psyche Saha ionization equilibrium, partition-function, degeneracy, electron-density, temperature, ionization-energy, LTE-domain, unit, stage-balance, and agency-nonconversion classifier", "saha-nonconversion", "Trinity Mandala bridge", "completed", ["SRC-SAHA"], "Saha ionization nonconversion classification", "No frozen nonconversion classifier isolates thermal ionization equilibrium, partition functions, degeneracy, electron density, temperature, ionization energy, LTE domain, units, stage balance, and agency refusal."),
    proposal(17, "BiCGSTAB shadow-residual, biorthogonality, alpha, omega, breakdown, near-breakdown, preconditioner, true-residual, stagnation, nonfinite, iteration-budget, and refusal tribunal", "bicgstab", "GMUT Mind", "completed", ["SRC-BICGSTAB"], "BiCGSTAB numerical obligation control", "GMRES and other solvers exist, but no frozen numerical tribunal isolates BiCGSTAB shadow residuals, alpha and omega breakdowns, preconditioning, true residual drift, stagnation, nonfinite state, and budgets."),
    proposal(18, "Stage 20 target-trial eligibility, strategy, assignment, time-zero, follow-up, outcome, causal-contrast, immortal-time, cloning, censoring, weighting, sensitivity, and nonpromotion board", "target-trial-nonpromotion", "Trinity Mandala bridge", "completed", ["SRC-TARGET-TRIAL"], "target-trial emulation design obligations", "No frozen Stage 20 board isolates target-trial protocol components, aligned time zero, immortal-time refusal, cloning and censoring, weighting, sensitivity, and terminal nonpromotion."),
    proposal(19, "R-tree minimum-bounding-rectangle, choose-leaf, area-enlargement, split, occupancy, parent-propagation, overlap, range-query, deletion-condense, determinism, resource-budget, and refusal tribunal", "r-tree", "THOS Body", "completed", ["SRC-RTREE"], "R-tree spatial-index obligation control", "No frozen data-structure tribunal isolates R-tree bounding rectangles, leaf choice, split and occupancy rules, parent propagation, overlap, range query, condense deletion, determinism, and budgets."),
    proposal(20, "Wavelet lifting split, predict, update, scaling, boundary-extension, integer-rounding, invertibility, perfect-reconstruction, overflow, nonfinite, level-budget, and refusal tribunal", "wavelet-lifting", "GMUT Mind", "completed", ["SRC-WAVELET-LIFTING"], "wavelet lifting numerical obligation control", "No frozen numerical tribunal isolates lifting split-predict-update steps, scaling, boundary extension, integer rounding, invertibility, perfect reconstruction, overflow, nonfinite state, and level budgets."),
]


def source(source_id, status, kind, title, url, implication):
    return {"source_id": source_id, "status": status, "kind": kind, "title": title, "url": url, "phase_implication": implication}


SOURCES = [
    source("SRC-CHANDY-LAMPORT", "stable", "primary_research", "Distributed Snapshots: Determining Global States of Distributed Systems", "https://doi.org/10.1145/214451.214456", "Supports bounded marker and consistent-cut fixtures only; no production distributed-system assurance."),
    source("SRC-SIGSTORE-BUNDLE", "current", "official_specification", "Sigstore Bundle Format 0.3.2", "https://docs.sigstore.dev/about/bundle/", "Supports synthetic bundle structure only; no signing, network log query, production key, or supply-chain assurance."),
    source("SRC-GALILEON", "stable", "primary_research", "Aspects of Galileon Non-Renormalization", "https://arxiv.org/abs/1606.02295", "Supports typed qualifications and mutations only; no proof for GMUT, ultraviolet completion, or physical claim."),
    source("SRC-VAINSHTEIN", "stable", "primary_research", "Vainshtein mechanism in second-order scalar-tensor theories", "https://arxiv.org/abs/1111.5090", "Supports a typed screening-obligation board only; no screened force, constraint, or empirical result."),
    source("SRC-HUBBLE-HSC", "current", "official_data_documentation", "MAST Hubble Source Catalog version 3.1", "https://archive.stsci.edu/hst/hsc/", "Supports zero-row readiness and version watch only; no query, download, catalog row, fit, or likelihood."),
    source("SRC-W3C-I18N", "current", "official_guidance", "W3C Internationalization Glossary", "https://www.w3.org/TR/i18n-glossary/", "Supplies synthetic localization vocabulary only; no translation competence, linguistic authority, or affected-user result."),
    source("SRC-W3C-TIMED-TEXT", "current", "official_working_group", "W3C Timed Text Working Group", "https://www.w3.org/AudioVideo/TT/", "Supplies synthetic timed-text structure only; no captioning qualification or real media service."),
    source("SRC-WAI-CAPTIONS", "current", "official_accessibility_guidance", "WAI Captions and Subtitles", "https://www.w3.org/WAI/media/av/captions/", "Supports structural caption obligations only; manual and affected-user evaluation remains reserved."),
    source("SRC-RFC8392", "stable", "official_standard", "RFC 8392 CBOR Web Token", "https://www.rfc-editor.org/info/rfc8392/", "Supports synthetic claim and container vectors only; no real token, key, COSE operation, account, or interoperability."),
    source("SRC-W3C-FEDCM", "draft", "official_working_draft", "W3C Federated Credential Management API", "https://www.w3.org/TR/fedcm/", "Supports draft-aware synthetic vectors only; no accounts, browser invocation, network exchange, assertion, or production identity."),
    source("SRC-NZ-LANGUAGE", "current", "official_policy_context", "Language Assistance Services Operational Policy", "https://www.mbie.govt.nz/cross-government-functions/language-assistance-services", "Keeps language-service quality, certification, access, and policy interpretation with competent people and authorities."),
    source("SRC-NZ-HRA", "current", "official_legal_context", "New Zealand Human Rights Act 1993", "https://www.legislation.govt.nz/act/public/1993/0082/latest/whole.html", "Keeps disability, discrimination, service access, and legal interpretation exact-gated."),
    source("SRC-NZ-PRIVACY", "current", "official_legal_context", "New Zealand Privacy Act 2020", "https://www.legislation.govt.nz/act/public/2020/31/en/latest/", "Keeps contributor and user privacy, correction, disclosure, and remedies exact-gated."),
    source("SRC-TE-MANA-RARAUNGA", "current", "maori_authority_context", "Te Mana Raraunga principles of Maori data sovereignty", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Keeps Maori wording, data, governance, and authority under Maori authority; software cannot exercise it."),
    source("SRC-ICC2", "stable", "official_format_specification", "ICC.2:2019 image technology colour management - extensions to architecture, profile format, and data structure", "https://www.color.org/specification/ICC.2-2019.pdf", "Supports disposable synthetic profile fields only; no colour-management conformance or production decoder assurance."),
    source("SRC-GEOTIFF11", "stable", "official_standard", "OGC GeoTIFF Standard 1.1", "https://docs.ogc.org/is/19-008r4/19-008r4.html", "Supports disposable synthetic tag fixtures only; no geospatial correctness, CRS authority, or production conformance."),
    source("SRC-RFC5905", "watch", "official_standard", "RFC 5905 Network Time Protocol Version 4", "https://www.rfc-editor.org/info/rfc5905/", "Supports synthetic packet and state fixtures while retaining published update notices; no network, clock, or security assurance."),
    source("SRC-MQTT5", "stable", "official_standard", "OASIS MQTT Version 5.0", "https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html", "Supports synthetic packet and state fixtures only; no broker, client, network, or interoperability assurance."),
    source("SRC-WCAG22", "stable", "official_accessibility_standard", "Web Content Accessibility Guidelines 2.2", "https://www.w3.org/TR/WCAG22/", "Supports structural obligations only; manual, assistive-technology, linguistic, and affected-user evaluation remains reserved."),
    source("SRC-SAHA", "stable", "primary_research_context", "Saha ionization equation historical primary-paper record", "https://ui.adsabs.harvard.edu/abs/1920PMag...40..472S/abstract", "Supports physical definitions and domain restrictions only; never psyche, agency, value, or participant conversion."),
    source("SRC-BICGSTAB", "stable", "primary_research", "Bi-CGSTAB: A Fast and Smoothly Converging Variant of Bi-CG", "https://doi.org/10.1137/0913035", "Supports bounded numerical fixtures only; no universal convergence, physical-model, or production-solver guarantee."),
    source("SRC-TARGET-TRIAL", "stable", "primary_methods_research", "Using Big Data to Emulate a Target Trial When a Randomized Trial Is Not Available", "https://pmc.ncbi.nlm.nih.gov/articles/PMC4832051/", "Supports design obligations only; zero participants and rows mean no causal, clinical, or Stage 20 claim."),
    source("SRC-RTREE", "stable", "primary_research", "R-trees: a dynamic index structure for spatial searching", "https://doi.org/10.1145/971697.602266", "Supports owner-local synthetic rectangles only; no production index, geospatial truth, durability, or exhaustive performance claim."),
    source("SRC-WAVELET-LIFTING", "stable", "primary_research", "The Lifting Scheme: A Construction of Second Generation Wavelets", "https://doi.org/10.1137/S0036141095289051", "Supports bounded numerical fixtures only; no universal stability, compression, or physical-model guarantee."),
]


REJECTED_COLLISIONS = [
    {"seed": "DHOST degeneracy classifier", "reason": "already frozen as V6461-P02"},
    {"seed": "Osterwalder-Schrader reflection positivity", "reason": "already frozen as V6478-P02"},
    {"seed": "Schwinger-Dyson hierarchy", "reason": "already frozen as V6466-P02"},
    {"seed": "newsroom editorial handover", "reason": "already frozen as V6485-P04"},
    {"seed": "theatre stage management", "reason": "already frozen as V6486-P04"},
    {"seed": "veterinary laboratory accession", "reason": "already frozen as V6465-P04"},
    {"seed": "GNAP identity profile", "reason": "already frozen as V6503-P05"},
    {"seed": "SD-JWT profile", "reason": "already frozen in multiple phases"},
    {"seed": "HTTP Structured Fields", "reason": "already frozen as V6473-P07"},
    {"seed": "GraphQL refusal tribunal", "reason": "already frozen as V6508-P17"},
    {"seed": "regression-discontinuity board", "reason": "already frozen in v647-v8 and v649-v1"},
    {"seed": "instrumental-variable board", "reason": "already frozen as V6481-P10"},
    {"seed": "synthetic-control board", "reason": "already frozen in v648-v2 and v649-v2"},
    {"seed": "Brotli parser tribunal", "reason": "already frozen as V6491-P07"},
    {"seed": "OpenType tribunal", "reason": "already frozen as V6506-P18"},
    {"seed": "GWOSC zero-row adapter", "reason": "already frozen in v646-v8 and v647-v8"},
    {"seed": "eROSITA zero-row adapter", "reason": "already frozen as V6466-P03"},
    {"seed": "observed-remove CRDT tribunal", "reason": "already frozen as V6508-P02"},
    {"seed": "FedCM production integration", "reason": "draft, account, network, privacy, and production gates forbid execution"},
    {"seed": "real localization participants and affected-user evaluation", "reason": "participant, professional, privacy, language, cultural, and affected-party gates remain external"},
]


SAFE_NOW = [f"{p['mission_surface']}: exact contract and protected-gate lint" for p in PROPOSALS] + [f"{p['mission_surface']}: deterministic fixture and refusal receipt" for p in PROPOSALS]

CANDIDATES = [f"{p['mission_surface']}: bounded executable prototype" for p in PROPOSALS] + [
    "distributed snapshot in-transit-message schedule enumerator",
    "Sigstore bundle proof-variant consistency checker",
    "Galileon derivative-counting mutation board",
    "Vainshtein branch and regime-matching checker",
    "Hubble HSC v3.1 zero-row schema adapter",
    "software-localization placeholder and plural replay",
    "timed-text overlap and late-change replay",
    "CWT claim-key and tag transition simulator",
    "FedCM endpoint and correlation-reservation simulator",
    "localization authority noncompensation matrix lint",
]

SKILLS = [f"ghc-family-v651-v2-{p['slug']}" for p in PROPOSALS]

RUNNERS = [
    "ghc_family_v651_v2_method_and_provenance.py",
    "ghc_family_v651_v2_gmut_boards.py",
    "ghc_family_v651_v2_zero_row_and_localization.py",
    "ghc_family_v651_v2_identity_and_authority.py",
    "ghc_family_v651_v2_format_and_protocol.py",
    "ghc_family_v651_v2_accessibility.py",
    "ghc_family_v651_v2_numeric_and_nonconversion.py",
    "ghc_family_v651_v2_stage20.py",
    "ghc_family_v651_v2_portfolios.py",
    "ghc_family_v651_v2_validate.py",
]

CLEAN_FIX_REFINE = [f"{p['mission_surface']}: preserve exact source and outcome vocabulary" for p in PROPOSALS] + [f"{p['mission_surface']}: normalize UTF-8 JSON and compatibility metadata" for p in PROPOSALS]
