#!/usr/bin/env python3
"""Frozen Tamar Vey v651-v3 x1 data; no x2 observations live here."""

from __future__ import annotations


PHASE = "v651-v3"
OWNER = "Tamar Vey"
PRONOUNS = "they/them"
ROLE = "relational evidence-systems cartographer and boundary keeper"
HOPE = "keep decisions legible, failures recoverable, and authority boundaries intact"
BRANCH = "codex/GHC-Family/tamar-vey-full-tools"
PHASE_ROOT = "docs/tamar-vey/v651-v3"

SOURCE_BRANCH = "codex/GHC-Family/orin-thale-v642-v6-full-tools"
SOURCE_HEAD = "7706cd8d92b1911e0cb61542469707baf2ec3ac6"
SOURCE_ORIGIN = "ad2b530c2449656b54ac0fee1a1284208c2a6a75"
SOURCE_X1 = "06c5545a79e992537b6307eb6a68e6d01204144d"
SOURCE_EVIDENCE = "8b3c1bb68852acc52c4554c34f1b6689a7c49efd"
SOURCE_CLOSEOUT = "6e0f088128d099514c3a277a410180edcbbf9b7e"
PRIOR_FROZEN = 940
INHERITED_NEGATIVES = 6690
STARTUP_NEGATIVES = 14
INHERITED_OPEN_GAPS = 52
INHERITED_EXACT_GATES = 53
PRIMARY_FOCUS = "GMUT Mind"
BOUNDED_PRACTICE = (
    "archival-audio preservation and transfer quality assurance, correction readback, "
    "workload control, and shift handover as a synthetic learning and design lens only"
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
        gate = "Emit a zero-row receipt and refuse every query, download, ingestion, likelihood, posterior, constraint, or empirical promotion."
    elif disposition == "exact_gate":
        approval = "exact_affected_party_competent_and_maori_authority_required"
        lane = "x2_reservation_matrix_only"
        gate = "Emit reservations only; make no consent, access, remedy, legal, cultural, data-governance, or Maori-authority decision."
    elif disposition == "represented":
        approval = "candidate_bounded_synthetic_proxy"
        lane = "x2_synthetic_proxy_only"
        gate = "Reject every preregistered mutation and retain proxy status with zero participant, production, professional, operational, identity, or authority credit."
    else:
        approval = "safe_now_bounded_software_symbolic_formal_or_structural"
        lane = "x2_bounded_owner_local"
        gate = "Reject every preregistered mutation and emit only the declared bounded software, symbolic, formal, numerical, or structural completion."
    return {
        "proposal_id": f"V6513-P{number:02d}",
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
        "novelty_against_940_frozen_proposals": novelty,
        "novelty_against_920_frozen_proposals": novelty,
    }


PROPOSALS = [
    proposal(1, "Method Flow Linux RCU read-side critical-section, grace-period, quiescent-state, publication, callback, reclamation, stall, fallback, teardown, and evidence-credit tribunal", "rcu-grace-period", "THOS Body", "completed", ["SRC-LINUX-RCU"], "RCU grace-period and reclamation control", "No frozen proposal isolates RCU read-side sections, quiescent states, grace periods, publication, callback reclamation, stalls, fallback, teardown, and evidence credit."),
    proposal(2, "RFC 9162 Certificate Transparency v2 tree-head, leaf-hash, inclusion-proof, consistency-proof, log-ID, checkpoint, time, experimental-status, offline-boundary, and nontransitive-credit tribunal", "ct-v2", "Freed ID and CBR Heart", "completed", ["SRC-RFC9162"], "Certificate Transparency v2 proof structure", "Earlier transparency work does not isolate RFC 9162 v2 tree heads, leaf hashes, proof variants, log identifiers, checkpoints, time, experimental status, and offline nontransitive credit."),
    proposal(3, "GMUT Israel junction hypersurface, induced-metric, normal-orientation, extrinsic-curvature jump, surface-stress, thin-shell, distribution, sign, boundary, EFT, unit, and observation-firewall board", "israel-junction", "GMUT Mind", "completed", ["SRC-ISRAEL"], "Israel junction and thin-shell obligations", "No frozen GMUT proposal isolates Israel junction hypersurfaces, induced metrics, normal orientation, extrinsic-curvature jumps, surface stress, thin shells, distributions, signs, boundaries, EFT, units, and observation refusal."),
    proposal(4, "GMUT Cartan-Karlhede frame, curvature-derivative, canonicalization, isotropy-group, functional-independence, termination-order, equivalence, coordinate-invariance, degeneracy, EFT, and observation-firewall board", "cartan-karlhede", "GMUT Mind", "completed", ["SRC-CARTAN-KARLHEDE"], "Cartan-Karlhede spacetime-equivalence obligations", "No frozen GMUT proposal isolates Cartan-Karlhede frames, curvature derivatives, canonicalization, isotropy groups, functional independence, termination order, equivalence, coordinate invariance, degeneracy, EFT, and observation refusal."),
    proposal(5, "GMUT HEASARC ROSAT 2RXS catalog schema, provenance, quality, selection, checksum, covariance, nuisance, version-watch, and zero-row likelihood-refusal adapter", "rosat-2rxs-zero-row", "GMUT Mind", "open_gap", ["SRC-HEASARC-2RXS"], "ROSAT 2RXS readiness", "No frozen zero-row adapter targets the HEASARC ROSAT 2RXS catalog with schema, provenance, quality, selection, checksum, covariance, nuisance, version watch, and likelihood refusal."),
    proposal(6, "THOS archival-audio carrier intake, condition, identifier, quarantine, playback-refusal, provenance-minimization, contamination, correction-readback, workload, and shift-handover proxy", "audio-carrier-intake", "THOS Body", "represented", ["SRC-IASA-TC04", "SRC-FADGI-AUDIO"], "archival-audio carrier intake workflow", "No frozen practice proxy isolates archival-audio carrier intake, condition, identifier, quarantine, playback refusal, provenance minimization, contamination, correction, workload, and handover."),
    proposal(7, "THOS archival-audio transfer azimuth, speed, equalization, ADC, level, dropout, file-fixity, metadata, QC-hold, correction-readback, workload, and shift-handover proxy", "audio-transfer-qc", "THOS Body", "represented", ["SRC-IASA-TC04", "SRC-FADGI-AUDIO"], "archival-audio transfer quality workflow", "No frozen practice proxy isolates archival-audio transfer azimuth, speed, equalization, conversion, level, dropout, fixity, metadata, QC hold, correction, workload, and handover."),
    proposal(8, "Freed ID RFC 8707 resource-indicator absolute-URI, fragment-refusal, multiplicity, authorization-request, token-request, audience-restriction, narrowing, mix-up, privacy, and nonproduction profile", "oauth-resource-indicators", "Freed ID and CBR Heart", "represented", ["SRC-RFC8707"], "OAuth resource-indicator profile", "No frozen identity proposal targets RFC 8707 absolute resource URIs, fragment refusal, multiplicity, authorization and token requests, audience restriction, narrowing, mix-up, privacy, and nonproduction boundaries."),
    proposal(9, "Freed ID RFC 6750 bearer header, form-body, query, single-transport, TLS, cache, error, scope, leakage, replay, minimization, update-watch, and nonproduction profile", "oauth-bearer-transport", "Freed ID and CBR Heart", "represented", ["SRC-RFC6750"], "OAuth bearer-token transport profile", "No frozen identity proposal isolates RFC 6750 header, form and query transports, one-method requirement, TLS, cache, error, scope, leakage, replay, minimization, update watch, and nonproduction refusal."),
    proposal(10, "CBR oral-history narrator-agreement, recording-custody, access-embargo, withdrawal-trigger, transcript-return, correction-log, contributor-privacy, cultural-expression, and reserved-authority matrix", "oral-history-authority", "Freed ID and CBR Heart", "exact_gate", ["SRC-NOHANZ", "SRC-NZ-PRIVACY", "SRC-TE-MANA-RARAUNGA"], "oral-history consent, access, remedy, and authority reservation", "No frozen matrix isolates oral-history narrator agreements, recording custody, access embargoes, withdrawal triggers, transcript return, correction logs, contributor privacy, cultural expression, and reserved affected-party, legal, data-governance, and Maori authority."),
    proposal(11, "RFC 3533 Ogg capture-pattern, version, header-type, granule-position, serial, page-sequence, segment-table, lacing, CRC, packet-boundary, resource-budget, and refusal tribunal", "ogg-page", "THOS Body", "completed", ["SRC-RFC3533"], "Ogg page structural refusal", "No frozen format tribunal targets RFC 3533 Ogg page capture, version, flags, granule, serial, sequence, lacing, CRC, packet boundaries, and resource budgets."),
    proposal(12, "EBU Tech 3285 Broadcast Wave RIFF, WAVE, fmt, data, bext, time-reference, originator, coding-history, chunk, padding, size, resource-budget, and refusal tribunal", "broadcast-wave", "THOS Body", "completed", ["SRC-EBU-3285"], "Broadcast Wave structural refusal", "No frozen format tribunal targets EBU Tech 3285 Broadcast Wave RIFF/WAVE, fmt, data, bext, time reference, originator, coding history, chunks, padding, sizes, and budgets."),
    proposal(13, "EBU Tech 3306 RF64 and BW64 ds64, sentinel-size, riffSize, dataSize, sampleCount, table, chunk, padding, overflow, supersession-watch, resource-budget, and refusal tribunal", "rf64-bw64", "THOS Body", "completed", ["SRC-EBU-3306", "SRC-ITU-BS2088"], "RF64 and BW64 structural refusal", "No frozen format tribunal isolates RF64 and BW64 ds64 sizing, sentinel values, counts, tables, overflow, supersession watch, and resource refusal."),
    proposal(14, "Accessible audio-player control-name, play-pause, seek, volume, status, captions, transcript-fallback, keyboard, focus, error, zoom, print, and manual-evaluation audit", "accessible-audio-player", "THOS Body", "completed", ["SRC-WAI-MEDIA", "SRC-WCAG22"], "accessible audio-player structure", "No frozen accessibility audit isolates audio-player control names, play and pause, seek, volume, status, captions and transcript fallback, keyboard, focus, errors, zoom, print, and manual reservations together."),
    proposal(15, "Thermo-Psyche Einstein-solid oscillator, frequency, partition-function, internal-energy, heat-capacity, low-temperature, high-temperature, unit, model-domain, and agency-nonconversion classifier", "einstein-solid", "Trinity Mandala bridge", "completed", ["SRC-EINSTEIN-SOLID"], "Einstein-solid nonconversion classification", "No frozen nonconversion classifier isolates Einstein-solid oscillators, frequency, partition function, energy, heat capacity, temperature limits, units, model domain, and agency refusal."),
    proposal(16, "MINRES Lanczos-basis, tridiagonal, symmetric-indefinite, preconditioner, residual, condition-estimate, breakdown, nonfinite, iteration-budget, unit, and refusal tribunal", "minres", "GMUT Mind", "completed", ["SRC-MINRES"], "MINRES numerical obligation control", "No frozen numerical tribunal isolates MINRES Lanczos and tridiagonal state, symmetric-indefinite domain, preconditioning, residuals, condition, breakdown, nonfinite state, iterations, and units."),
    proposal(17, "Stage 20 entropy-balancing base-weight, moment-constraint, primal, dual, convexity, feasibility, positivity, effective-sample-size, diagnostics, sensitivity, uncertainty, and nonpromotion board", "entropy-balancing", "Trinity Mandala bridge", "completed", ["SRC-ENTROPY-BALANCING"], "entropy-balancing design obligations", "No frozen Stage 20 board isolates entropy-balancing base weights, moment constraints, primal and dual forms, convexity, feasibility, positivity, effective sample size, diagnostics, sensitivity, uncertainty, and terminal nonpromotion."),
    proposal(18, "Quotient-filter fingerprint, quotient, remainder, occupied-bit, continuation-bit, shifted-bit, run, cluster, insertion, deletion, merge, resize, false-positive, resource-budget, and refusal tribunal", "quotient-filter", "THOS Body", "completed", ["SRC-QUOTIENT-FILTER"], "Quotient-filter obligation control", "No frozen data-structure tribunal isolates Quotient-filter fingerprints, quotient and remainder partitioning, metadata bits, runs, clusters, insertion, deletion, merge, resize, false positives, and resource budgets."),
    proposal(19, "Rabin-fingerprint polynomial, modulus, irreducibility, rolling-window, outgoing-byte, incoming-byte, collision, chunk-boundary, seed, minimum-size, maximum-size, resource-budget, and refusal tribunal", "rabin-fingerprint", "THOS Body", "completed", ["SRC-RABIN"], "Rabin rolling-fingerprint obligation control", "No frozen data-structure tribunal isolates Rabin polynomial fingerprints, modulus and irreducibility, rolling updates, collisions, content-defined boundaries, seeds, size bounds, and resource limits."),
    proposal(20, "LT fountain-code degree-distribution, neighbour-selection, symbol-XOR, peeling, ripple, stall, overhead, seed, erasure, reconstruction, resource-budget, and refusal tribunal", "lt-fountain-code", "GMUT Mind", "completed", ["SRC-LT-CODES"], "LT fountain-code obligation control", "No frozen coding tribunal isolates LT degree distributions, neighbour selection, symbol XOR, peeling, ripple and stall, overhead, seeds, erasures, reconstruction, and resource budgets."),
]


def source(source_id, status, kind, title, url, implication):
    return {"source_id": source_id, "status": status, "kind": kind, "title": title, "url": url, "phase_implication": implication}


SOURCES = [
    source("SRC-LINUX-RCU", "current", "official_documentation", "Linux kernel RCU concepts and what is RCU", "https://www.kernel.org/doc/html/next/RCU/whatisRCU.html", "Supports owner-local concurrency fixtures only; no kernel, production, or exhaustive-concurrency assurance."),
    source("SRC-RFC9162", "stable", "official_experimental_specification", "RFC 9162 Certificate Transparency Version 2.0", "https://www.rfc-editor.org/rfc/rfc9162.html", "Supports synthetic proof structures and explicit experimental status only; no live log or certificate assurance."),
    source("SRC-ISRAEL", "stable", "primary_research", "Singular Hypersurfaces and Thin Shells in General Relativity", "https://doi.org/10.1007/BF02710419", "Supports typed junction obligations only; no thin shell, physical state, force, constraint, or empirical result for GMUT."),
    source("SRC-CARTAN-KARLHEDE", "stable", "primary_and_review_research", "On the Equivalence of Spacetimes, the Cartan-Karlhede Algorithm", "https://arxiv.org/abs/2007.04123", "Supports typed equivalence-algorithm obligations only; no classification theorem for GMUT or physical claim."),
    source("SRC-HEASARC-2RXS", "current", "official_data_documentation", "HEASARC ROSAT 2RXS catalog", "https://heasarc.gsfc.nasa.gov/W3Browse/rosat/rass2rxs.html", "Supports zero-row readiness only; no query, download, row, likelihood, posterior, or empirical claim."),
    source("SRC-IASA-TC04", "current", "official_professional_guidance", "IASA TC-04 Guidelines on the Production and Preservation of Digital Audio Objects", "https://www.iasa-web.org/audio-preservation-tc04", "Supplies synthetic preservation vocabulary only; no archival qualification, operational authority, or real-carrier result."),
    source("SRC-FADGI-AUDIO", "watch", "official_guidance", "FADGI Audio Performance Guidelines", "https://www.digitizationguidelines.gov/guidelines/digitize-audioperf.html", "Supports synthetic performance fields while retaining the current tool-support watch; no transfer certification."),
    source("SRC-RFC8707", "stable", "official_standard", "RFC 8707 Resource Indicators for OAuth 2.0", "https://www.rfc-editor.org/rfc/rfc8707.html", "Supports synthetic request vectors only; no account, token, service, or production identity event."),
    source("SRC-RFC6750", "watch", "official_standard", "RFC 6750 OAuth 2.0 Bearer Token Usage", "https://www.rfc-editor.org/info/rfc6750/", "Supports synthetic transport refusal while retaining published update notices; no real bearer token or service."),
    source("SRC-NOHANZ", "current", "affected_practice_guidance", "National Oral History Association of New Zealand ethical practice and key documents", "https://oralhistory.org.nz/index.php/ethics-and-practice/", "Keeps consent, contributor practice, and interpretation with competent people and affected parties."),
    source("SRC-NZ-PRIVACY", "current", "official_legal_context", "New Zealand Privacy Act 2020", "https://www.legislation.govt.nz/act/public/2020/31/en/latest/", "Keeps privacy, correction, access, disclosure, and legal interpretation exact-gated."),
    source("SRC-TE-MANA-RARAUNGA", "current", "maori_authority_context", "Te Mana Raraunga principles of Maori data sovereignty", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Keeps Maori wording, data, governance, and authority under Maori authority; software cannot exercise it."),
    source("SRC-RFC3533", "stable", "official_informational_specification", "RFC 3533 The Ogg Encapsulation Format Version 0", "https://www.rfc-editor.org/info/rfc3533/", "Supports disposable synthetic Ogg pages only; no codec, media, or production parser assurance."),
    source("SRC-EBU-3285", "stable", "official_format_specification", "EBU Tech 3285 Broadcast Wave Format", "https://tech.ebu.ch/publications/tech3285", "Supports synthetic RIFF/WAVE and bext fixtures only; no preservation or format conformance claim."),
    source("SRC-EBU-3306", "watch", "official_format_specification", "EBU Tech 3306 RF64", "https://tech.ebu.ch/publications/tech3306", "Supports synthetic RF64 fixtures while retaining the official supersession notice; no production conformance."),
    source("SRC-ITU-BS2088", "current", "official_standard_context", "ITU-R BS.2088 Long-form file format for programme exchange", "https://www.itu.int/rec/R-REC-BS.2088/en", "Supplies the current superseding context only; no certification or interoperability claim."),
    source("SRC-WAI-MEDIA", "current", "official_accessibility_guidance", "W3C WAI Making Audio and Video Media Accessible", "https://www.w3.org/WAI/media/av/", "Supports structural player obligations only; manual and affected-user evaluation remains reserved."),
    source("SRC-WCAG22", "stable", "official_accessibility_standard", "Web Content Accessibility Guidelines 2.2", "https://www.w3.org/TR/WCAG22/", "Supports structural obligations only; complete accessibility conformance is not claimed."),
    source("SRC-EINSTEIN-SOLID", "stable", "primary_research", "Planck's Theory of Radiation and the Theory of Specific Heat", "https://doi.org/10.1002/andp.19063270110", "Supports physical definitions and limits only; never psyche, agency, value, or participant conversion."),
    source("SRC-MINRES", "stable", "primary_research", "Solution of Sparse Indefinite Systems of Linear Equations", "https://doi.org/10.1137/0712047", "Supports bounded numerical fixtures only; no universal convergence or physical-model guarantee."),
    source("SRC-ENTROPY-BALANCING", "stable", "primary_methods_research", "Entropy Balancing for Causal Effects", "https://doi.org/10.1093/pan/mpr025", "Supports design obligations only; zero rows and units mean no causal, participant, or Stage 20 result."),
    source("SRC-QUOTIENT-FILTER", "stable", "primary_research", "Don't Thrash: How to Cache Your Hash on Flash", "https://doi.org/10.14778/2350229.2350275", "Supports bounded approximate-membership fixtures only; no production performance, storage, or exhaustive guarantee."),
    source("SRC-RABIN", "stable", "primary_technical_report", "Fingerprinting by Random Polynomials", "https://books.google.com/books?id=Emu_tgAACAAJ", "Supports bounded rolling-polynomial fixtures only; collisions and adversarial limits remain explicit."),
    source("SRC-LT-CODES", "stable", "primary_research", "LT Codes", "https://doi.org/10.1109/SFCS.2002.1181950", "Supports bounded erasure-code fixtures only; no network, storage, or universal reliability claim."),
]


REJECTED_COLLISIONS = [
    {"seed": "in-toto and SLSA attestation", "reason": "already frozen as V6477-P01 and related earlier supply-chain proposals"},
    {"seed": "Schwinger-Keldysh contour", "reason": "already frozen as V6462-P02"},
    {"seed": "Peierls bracket", "reason": "already frozen as V6465-P02"},
    {"seed": "Vilkovisky effective action", "reason": "already frozen as V6468-P02"},
    {"seed": "Nielsen identity", "reason": "already frozen as V6471-P02 and V6502-P03; rejected by the first formal v651-v3 audit"},
    {"seed": "ADM constraints", "reason": "already frozen as V6475-P02; rejected by mechanism review"},
    {"seed": "RAR authorization details", "reason": "already frozen as V6486-P05"},
    {"seed": "DPoP proof profile", "reason": "already frozen as V6466-P05"},
    {"seed": "CBOR Sequence parser", "reason": "already frozen as V6501-P12"},
    {"seed": "Parquet parser", "reason": "already frozen as V6502-P12"},
    {"seed": "Debye heat capacity", "reason": "already frozen as V6502-P15"},
    {"seed": "Zstandard frame", "reason": "already frozen as V6482-P07"},
    {"seed": "GWOSC zero-row adapter", "reason": "already frozen in v646-v8 and v647-v8"},
    {"seed": "eROSITA zero-row adapter", "reason": "already frozen as V6466-P03"},
    {"seed": "target-trial emulation", "reason": "already frozen as V6512-P18"},
    {"seed": "regression discontinuity", "reason": "already frozen in v647-v8 and v649-v1"},
    {"seed": "instrumental variables", "reason": "already frozen as V6481-P10"},
    {"seed": "synthetic control", "reason": "already frozen in v648-v2 and v649-v2; rejected by mechanism review"},
    {"seed": "Cuckoo filter", "reason": "already frozen as V6503-P12; rejected by the first formal v651-v3 audit"},
    {"seed": "wavelet lifting", "reason": "already frozen as V6512-P20"},
    {"seed": "R-tree", "reason": "already frozen as V6512-P19"},
    {"seed": "MQTT 5", "reason": "already frozen as V6512-P14"},
    {"seed": "real archival-audio carriers or interviews", "reason": "participant, privacy, professional, cultural, and affected-party gates forbid execution"},
    {"seed": "live OAuth tokens and accounts", "reason": "credential, account, network, privacy, production, and trust-governance gates forbid execution"},
]


SAFE_NOW = [f"{p['mission_surface']}: exact contract and protected-gate lint" for p in PROPOSALS] + [f"{p['mission_surface']}: deterministic fixture and refusal receipt" for p in PROPOSALS]
CANDIDATES = [f"{p['mission_surface']}: bounded executable prototype" for p in PROPOSALS] + [
    "RCU grace-period schedule enumerator", "CT v2 inclusion and consistency proof checker", "Nielsen gauge-parameter mutation board", "ADM constraint-algebra type checker", "ROSAT 2RXS zero-row schema adapter", "archival carrier intake refusal replay", "archival transfer QC hold replay", "OAuth resource-indicator narrowing simulator", "bearer-transport leakage and replay simulator", "oral-history authority noncompensation matrix lint",
]
SKILLS = [f"ghc-family-v651-v3-{p['slug']}" for p in PROPOSALS]
RUNNERS = [
    "ghc_family_v651_v3_method_and_transparency.py", "ghc_family_v651_v3_gmut_boards.py", "ghc_family_v651_v3_zero_row_and_audio.py", "ghc_family_v651_v3_identity_and_authority.py", "ghc_family_v651_v3_audio_formats.py", "ghc_family_v651_v3_accessibility.py", "ghc_family_v651_v3_numeric_and_nonconversion.py", "ghc_family_v651_v3_stage20.py", "ghc_family_v651_v3_portfolios.py", "ghc_family_v651_v3_validate.py",
]
CLEAN_FIX_REFINE = [f"{p['mission_surface']}: preserve exact source and outcome vocabulary" for p in PROPOSALS] + [f"{p['mission_surface']}: normalize UTF-8 JSON and compatibility metadata" for p in PROPOSALS]
