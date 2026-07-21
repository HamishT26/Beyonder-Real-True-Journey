#!/usr/bin/env python3
"""Frozen Sylven Arc v651-v4 x1 data; no x2 observations live here."""

from __future__ import annotations


PHASE = "v651-v4"
OWNER = "Sylven Arc"
PRONOUNS = "they/them"
ROLE = "relational constraint-cartographer and falsifier-keeper"
HOPE = "keep uncertainty visible without turning it into authority"
BRANCH = "codex/GHC-Family/sylven-arc-v642-v8-full-tools"
PHASE_ROOT = "docs/sylven-arc/v651-v4"

SOURCE_BRANCH = "codex/GHC-Family/tamar-vey-full-tools"
SOURCE_HEAD = "3ec09ba3dfc019fd9def1e58eb4943b18bcc7def"
SOURCE_ORIGIN = "7706cd8d92b1911e0cb61542469707baf2ec3ac6"
SOURCE_X1 = "111e53d75eaa3560b48c3573507552b9ddb5ddfc"
SOURCE_EVIDENCE = "449f3a29402459a66838cbf1cc8a3b110c145162"
SOURCE_CLOSEOUT = "5b46077beb30019d5904c7d6d8fac5202c00ab82"
PRIOR_FROZEN = 960
INHERITED_NEGATIVES = 6824
STARTUP_NEGATIVES = 15
INHERITED_OPEN_GAPS = 53
INHERITED_EXACT_GATES = 54
PRIMARY_FOCUS = "THOS Body"
BOUNDED_PRACTICE = (
    "commercial-refrigeration service intake, refrigerant identification, isolation, recovery, "
    "leak-check refusal, cold-room alarms, workload control, and shift handover as a synthetic learning and design lens only"
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
        "proposal_id": f"V6514-P{number:02d}",
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
        "novelty_against_960_frozen_proposals": novelty,
        "novelty_against_940_frozen_proposals": novelty,
        "novelty_against_920_frozen_proposals": novelty,
    }


PROPOSALS = [
    proposal(1, "Method Flow POSIX robust-mutex owner-death, EOWNERDEAD, consistency-repair, not-recoverable, process-shared, teardown, and evidence-credit tribunal", "robust-mutex", "THOS Body", "completed", ["SRC-POSIX-ROBUST"], "robust-mutex recovery control", "No frozen proposal isolates POSIX robust-mutex owner death, EOWNERDEAD acquisition, consistency repair, not-recoverable state, process sharing, teardown, and evidence credit."),
    proposal(2, "Method Flow Linux UNIX-domain SCM_RIGHTS descriptor, SCM_CREDENTIALS peer, ancillary-barrier, truncation, resource-limit, EOF, teardown, and evidence-credit tribunal", "unix-ancillary", "THOS Body", "completed", ["SRC-LINUX-UNIX"], "UNIX-domain ancillary-message control", "No frozen proposal isolates UNIX-domain descriptor and credential transfer, ancillary barriers, truncation, resource limits, EOF, teardown, and bounded evidence credit."),
    proposal(3, "GMUT Geroch-Held-Penrose null-direction, spin-weight, boost-weight, weighted-derivative, commutator, tetrad-rescaling, curvature-scalar, gauge, EFT, unit, and observation-firewall board", "ghp-calculus", "GMUT Mind", "completed", ["SRC-GHP"], "Geroch-Held-Penrose obligation control", "No frozen GMUT proposal isolates GHP weighted quantities, derivative operators, commutators, tetrad rescaling, curvature scalars, gauge, EFT, units, and observation refusal."),
    proposal(4, "GMUT BSSN conformal-metric, conformal-factor, trace-free-curvature, connection-function, algebraic-constraint, gauge-driver, hyperbolicity, boundary, EFT, unit, and observation-firewall board", "bssn-system", "GMUT Mind", "completed", ["SRC-BSSN"], "BSSN evolution-system obligation control", "No frozen GMUT proposal isolates BSSN conformal variables, connection functions, algebraic constraints, gauge drivers, hyperbolicity, boundaries, EFT, units, and observation refusal."),
    proposal(5, "GMUT LOFAR LoTSS DR2 source-catalog schema, mosaic, flux-scale, association, completeness, selection, checksum, covariance, nuisance, version-watch, and zero-row likelihood-refusal adapter", "lotss-dr2-zero-row", "GMUT Mind", "open_gap", ["SRC-LOTSS-DR2"], "LoTSS DR2 zero-row readiness", "No frozen zero-row adapter targets LOFAR LoTSS DR2 mosaics and source catalogs with flux scale, association, completeness, selection, checksum, covariance, nuisance, version watch, and likelihood refusal."),
    proposal(6, "THOS commercial-refrigeration service intake, equipment-identity, refrigerant-identification, isolation, recovery-cylinder, leak-check-refusal, correction-readback, workload, and shift-handover proxy", "refrigeration-service", "THOS Body", "represented", ["SRC-UNEP-REFRIG", "SRC-NZ-EPA-SGG"], "commercial-refrigeration service workflow", "No frozen practice proxy isolates refrigeration service intake, equipment and refrigerant identity, isolation, recovery cylinders, leak-check refusal, correction readback, workload, and handover."),
    proposal(7, "THOS cold-room temperature-alarm, sensor-verification, door-seal, defrost, product-segregation, escalation, accessible-notice, correction-readback, workload, and shift-handover proxy", "cold-room-handover", "THOS Body", "represented", ["SRC-MPI-COLD-STORES", "SRC-UNEP-REFRIG"], "cold-room alarm and handover workflow", "No frozen practice proxy isolates cold-room alarms, sensor verification, door seals, defrost, product segregation, escalation, accessible notice, correction readback, workload, and handover."),
    proposal(8, "Freed ID ECDSA RDFC-1.0 versus JCS canonicalization, P-256 and P-384 multikey, raw-signature encoding, key-format rejection, and synthetic test-vector profile", "ecdsa-data-integrity", "Freed ID and CBR Heart", "represented", ["SRC-W3C-ECDSA"], "ECDSA canonicalization and encoding profile", "Earlier generic data-integrity work does not isolate the final W3C ECDSA cryptosuite algorithms, canonicalization-path selection, curve-specific multikey encoding, raw-signature encoding, key-format rejection, and nonproduction test vectors."),
    proposal(9, "Freed ID OpenID FAPI 2.0 Message Signing JAR, JARM, signed-introspection, ID-token, algorithm, key, audience, replay, retention-minimization, and nonproduction profile", "fapi2-message-signing", "Freed ID and CBR Heart", "represented", ["SRC-OIDF-FAPI2-MS"], "FAPI 2.0 Message Signing profile", "No frozen identity proposal targets the September 2025 final FAPI 2.0 Message Signing combination of JAR, JARM, signed introspection, ID tokens, algorithms, key binding, audience, replay, and retention minimization."),
    proposal(10, "CBR refrigeration leak, food-loss, worker-and-customer privacy, accessible-notice, remedy, environmental-harm, affected-party, legal, cultural, data-governance, and Maori-authority matrix", "refrigeration-authority", "Freed ID and CBR Heart", "exact_gate", ["SRC-NZ-EPA-SGG", "SRC-MPI-COLD-STORES", "SRC-NZ-PRIVACY", "SRC-TE-MANA-RARAUNGA"], "refrigeration incident, remedy, and authority reservation", "No frozen matrix isolates refrigeration leaks, food loss, worker and customer privacy, accessible notice, remedy, environmental harm, affected parties, law, culture, data governance, and Maori authority."),
    proposal(11, "RFC 1950 zlib CMF, FLG, compression-method, window, preset-dictionary, FCHECK, Adler-32, truncation, trailing-data, resource-budget, and refusal tribunal", "zlib-frame", "THOS Body", "completed", ["SRC-RFC1950"], "zlib structural refusal", "No frozen format tribunal targets RFC 1950 CMF and FLG fields, window size, preset dictionaries, FCHECK, Adler-32, truncation, trailing data, and resource budgets."),
    proposal(12, "POSIX pax extended-header length, keyword, precedence, path, linkpath, size, time, ustar-fallback, traversal, special-entry, resource-budget, and refusal tribunal", "pax-archive", "THOS Body", "completed", ["SRC-POSIX-PAX"], "pax archive structural refusal", "No frozen archive tribunal targets POSIX pax extended-header lengths, keyword precedence, path and linkpath, sizes, times, ustar fallback, traversal, special entries, and resource budgets."),
    proposal(13, "Cap'n Proto segment-table, word-alignment, struct-pointer, list-pointer, far-pointer, landing-pad, traversal-limit, packing, canonicalization, resource-budget, and refusal tribunal", "capnproto-encoding", "THOS Body", "completed", ["SRC-CAPNPROTO"], "Cap'n Proto structural refusal", "No frozen serialization tribunal targets Cap'n Proto segment tables, word alignment, pointer types, landing pads, traversal limits, packing, canonicalization, and resource budgets."),
    proposal(14, "Accessible drag-and-drop file-upload label, keyboard-alternative, browse-control, accepted-type, queue, progress, cancel, error, status, focus, noncolour, and manual-evaluation audit", "accessible-file-upload", "THOS Body", "completed", ["SRC-WCAG22-DRAG", "SRC-WAI-UPLOAD"], "accessible file-upload structure", "No frozen accessibility audit isolates drag-and-drop upload labels, non-drag keyboard alternatives, browse controls, accepted types, queues, progress, cancellation, errors, status, focus, and manual reservations."),
    proposal(15, "Thermo-Psyche Langmuir adsorption site, coverage, pressure, equilibrium-constant, monolayer, saturation, temperature-domain, unit, model-assumption, and agency-nonconversion classifier", "langmuir-nonconversion", "Trinity Mandala bridge", "completed", ["SRC-LANGMUIR"], "Langmuir adsorption nonconversion", "No frozen nonconversion classifier isolates Langmuir sites, coverage, pressure, equilibrium constants, monolayer saturation, temperature domain, units, model assumptions, and agency refusal."),
    proposal(16, "LSQR Golub-Kahan bidiagonalization, alpha, beta, damping, residual, normal-residual, condition-estimate, breakdown, nonfinite, iteration-budget, unit, and refusal tribunal", "lsqr", "GMUT Mind", "completed", ["SRC-LSQR"], "LSQR numerical obligation control", "No frozen numerical tribunal isolates LSQR Golub-Kahan state, damping, residual and normal residual, condition estimates, breakdown, nonfinite state, iterations, and units."),
    proposal(17, "Stage 20 structural-nested-mean-model blip-function, treatment-model, g-estimation, sequential-exchangeability, consistency, positivity, nuisance-model, diagnostic, sensitivity, uncertainty, and nonpromotion board", "snmm-g-estimation", "Trinity Mandala bridge", "completed", ["SRC-SNMM"], "structural nested mean model obligations", "No frozen Stage 20 board isolates structural nested mean-model blip functions, treatment models, g-estimation, sequential exchangeability, consistency, positivity, nuisance models, diagnostics, sensitivity, uncertainty, and nonpromotion."),
    proposal(18, "Elias-Fano monotone-sequence high-bits, low-bits, select, predecessor, universe-bound, duplicate-policy, encoding-choice, overflow, resource-budget, and refusal tribunal", "elias-fano", "THOS Body", "completed", ["SRC-ELIAS-FANO"], "Elias-Fano obligation control", "No frozen succinct-structure tribunal isolates Elias-Fano high and low bit partitions, select, predecessor, universe bounds, duplicates, encoding choice, overflow, and resource budgets."),
    proposal(19, "Golomb-Rice quotient, remainder, unary-prefix, parameter, signed-mapping, truncation, prefix-budget, decode-bound, malformed-code, resource-budget, and refusal tribunal", "golomb-rice", "THOS Body", "completed", ["SRC-GOLOMB"], "Golomb-Rice obligation control", "No frozen coding tribunal isolates Golomb-Rice quotient and remainder coding, unary prefixes, parameters, signed mapping, truncation, prefix and decode bounds, malformed codes, and resource budgets."),
    proposal(20, "LZ4 frame magic, descriptor, block-mode, block-size, content-size, dictionary-ID, header-checksum, block-checksum, content-checksum, skippable-frame, resource-budget, and refusal tribunal", "lz4-frame", "THOS Body", "completed", ["SRC-LZ4"], "LZ4 frame structural refusal", "No frozen format tribunal targets LZ4 frame magic, descriptors, block modes and sizes, content size, dictionary IDs, checksums, skippable frames, and resource budgets."),
]


def source(source_id, status, kind, title, url, implication):
    return {"source_id": source_id, "status": status, "kind": kind, "title": title, "url": url, "phase_implication": implication}


SOURCES = [
    source("SRC-POSIX-ROBUST", "current", "official_standard", "POSIX.1-2024 robust mutex rationale and interfaces", "https://pubs.opengroup.org/onlinepubs/9799919799/xrat/V4_xsh_chap01.html", "Supports disposable owner-local robust-mutex models only; no production concurrency assurance."),
    source("SRC-LINUX-UNIX", "current", "primary_system_documentation", "Linux unix(7) local IPC and ancillary messages", "https://man7.org/linux/man-pages/man7/unix.7.html", "Supports disposable local socket fixtures only; no production IPC, privilege, or exhaustive-security assurance."),
    source("SRC-GHP", "stable", "primary_research", "A space-time calculus based on pairs of null directions", "https://doi.org/10.1063/1.1666410", "Supports typed GHP obligations only; no force, state, likelihood, constraint, empirical result, or physical authority."),
    source("SRC-BSSN", "stable", "primary_research", "On the numerical integration of Einstein's field equations", "https://arxiv.org/abs/gr-qc/9810065", "Supports typed BSSN obligations only; no stable evolution theorem or empirical GMUT result."),
    source("SRC-LOTSS-DR2", "current", "official_data_documentation", "LOFAR Surveys LoTSS DR2 release", "https://lofar-surveys.org/dr2_release.html", "Supports zero-row schema readiness only; no query, download, row, likelihood, posterior, constraint, or empirical claim."),
    source("SRC-UNEP-REFRIG", "current", "official_practice_guidance", "UNEP OzonAction refrigerant management", "https://www.unep.org/ozonaction/refrigerant-management", "Supplies synthetic service vocabulary only; no technician competence, safety result, or operational authority."),
    source("SRC-NZ-EPA-SGG", "current", "official_legal_context", "New Zealand EPA synthetic greenhouse gases", "https://www.epa.govt.nz/industry-areas/emissions-trading-scheme/industries-in-the-emissions-trading-scheme/synthetic-greenhouse-gases/", "Keeps emissions, best-practice, enforcement, and legal interpretation external and exact-gated."),
    source("SRC-MPI-COLD-STORES", "current", "official_practice_context", "MPI food safety for cold and dry stores", "https://www.mpi.govt.nz/food-business/transport-storage-and-wharves/food-safety-cold-dry-stores-animal-material-depots/", "Supplies synthetic cold-room vocabulary only; no food-safety compliance, operational outcome, or authority."),
    source("SRC-W3C-ECDSA", "current", "official_recommendation", "W3C Data Integrity ECDSA Cryptosuites v1.0", "https://www.w3.org/TR/vc-di-ecdsa/", "Supports synthetic vectors only; no real key, proof, credential, status, interoperability, or production identity event."),
    source("SRC-OIDF-FAPI2-MS", "current", "official_final_specification", "OpenID FAPI 2.0 Message Signing", "https://openid.net/specs/fapi-message-signing-2_0-final.html", "Supports synthetic message vectors only; no real client, key, token, service, non-repudiation decision, or production event."),
    source("SRC-NZ-PRIVACY", "current", "official_legal_context", "New Zealand Privacy Act 2020", "https://www.legislation.govt.nz/act/public/2020/31/en/latest/", "Keeps privacy, correction, access, disclosure, and legal interpretation exact-gated."),
    source("SRC-TE-MANA-RARAUNGA", "current", "maori_authority_context", "Te Mana Raraunga principles of Maori data sovereignty", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Keeps Maori wording, data, governance, and authority under Maori authority; software cannot exercise it."),
    source("SRC-RFC1950", "stable", "official_informational_specification", "RFC 1950 ZLIB Compressed Data Format", "https://www.rfc-editor.org/info/rfc1950", "Supports disposable synthetic streams only; no production decompressor or exhaustive-security assurance."),
    source("SRC-POSIX-PAX", "current", "official_standard", "POSIX.1-2024 pax utility and interchange formats", "https://pubs.opengroup.org/onlinepubs/9799919799/utilities/pax.html", "Supports disposable synthetic archives only; no extraction authority or production parser assurance."),
    source("SRC-CAPNPROTO", "current", "primary_format_specification", "Cap'n Proto encoding specification", "https://capnproto.org/encoding.html", "Supports disposable byte fixtures only; no schema, interoperability, production, or exhaustive-security assurance."),
    source("SRC-WCAG22-DRAG", "current", "official_accessibility_guidance", "W3C Understanding WCAG 2.2 Dragging Movements", "https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html", "Supports structural non-drag alternatives only; manual and affected-user evaluation remains reserved."),
    source("SRC-WAI-UPLOAD", "current", "official_accessibility_technique", "W3C WAI ariaNotify file-upload progress technique", "https://www.w3.org/WAI/WCAG21/Techniques/aria/ARIA27", "Supports structural status obligations only; complete accessibility conformance is not claimed."),
    source("SRC-LANGMUIR", "stable", "primary_research", "The Adsorption of Gases on Plane Surfaces", "https://doi.org/10.1021/ja02242a004", "Supports physical model definitions only; never psyche, agency, justice, participant, or consciousness conversion."),
    source("SRC-LSQR", "stable", "primary_research", "LSQR: An Algorithm for Sparse Linear Equations and Sparse Least Squares", "https://web.stanford.edu/class/cme324/paige-saunders2.pdf", "Supports bounded numerical fixtures only; no universal convergence or physical-model guarantee."),
    source("SRC-SNMM", "stable", "primary_methods_research", "Structural Nested Models and G-estimation", "https://doi.org/10.1214/14-STS493", "Supports typed design obligations only; zero participants and rows mean no causal, treatment, or Stage 20 result."),
    source("SRC-ELIAS-FANO", "stable", "primary_research", "On the number of bits required to implement an associative memory", "https://doi.org/10.1016/S0022-0000(74)80011-4", "Supports bounded monotone-sequence fixtures only; no production storage or universal performance claim."),
    source("SRC-GOLOMB", "stable", "primary_research", "Run-Length Encodings", "https://doi.org/10.1109/TIT.1966.1053907", "Supports bounded coding fixtures only; no universal compression or adversarial guarantee."),
    source("SRC-LZ4", "current", "primary_format_specification", "LZ4 Frame Format", "https://github.com/lz4/lz4/blob/dev/doc/lz4_Frame_format.md", "Supports disposable synthetic frames only; no production decompressor or exhaustive-security assurance."),
]


REJECTED_COLLISIONS = [
    {"seed": "in-toto and SLSA attestation", "reason": "already frozen as V6477-P01 and related earlier supply-chain proposals"},
    {"seed": "Schwinger-Keldysh contour", "reason": "already frozen as V6462-P02"},
    {"seed": "Peierls bracket", "reason": "already frozen as V6465-P02"},
    {"seed": "Vilkovisky effective action", "reason": "already frozen as V6468-P02"},
    {"seed": "Nielsen identity", "reason": "already frozen as V6471-P02 and V6502-P03; rejected by the first formal v651-v4 audit"},
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
    {"seed": "Cuckoo filter", "reason": "already frozen as V6503-P12; rejected by the first formal v651-v4 audit"},
    {"seed": "wavelet lifting", "reason": "already frozen as V6512-P20"},
    {"seed": "R-tree", "reason": "already frozen as V6512-P19"},
    {"seed": "MQTT 5", "reason": "already frozen as V6512-P14"},
    {"seed": "Fermi-LAT 4FGL-DR4 adapter", "reason": "already frozen as V6484-P03"},
    {"seed": "drinking-water laboratory workflow", "reason": "already frozen as V6463-P04 and later treatment workflows"},
    {"seed": "OAuth protected-resource metadata", "reason": "already frozen as V6477-P05 and V6501-P08"},
    {"seed": "W3C generic Data Integrity profile", "reason": "already frozen as V6498-P08; v651-v4 narrows to the final ECDSA cryptosuite"},
    {"seed": "accessible carousel", "reason": "already frozen as V6468-P08"},
    {"seed": "Debye heat capacity", "reason": "already frozen as V6502-P15"},
    {"seed": "regression discontinuity", "reason": "already frozen as V6478-P10 and V6491-P10"},
    {"seed": "Cuckoo filter", "reason": "already frozen as V6503-P12"},
    {"seed": "Reed-Solomon coding", "reason": "already frozen as V6501-P19"},
    {"seed": "BLAKE3", "reason": "already frozen as V6502-P20"},
    {"seed": "real refrigeration systems, refrigerants, food, workers, customers, or incidents", "reason": "participant, privacy, professional, safety, environmental, legal, and affected-party gates forbid execution"},
    {"seed": "live OAuth tokens and accounts", "reason": "credential, account, network, privacy, production, and trust-governance gates forbid execution"},
]


SAFE_NOW = [f"{p['mission_surface']}: exact contract and protected-gate lint" for p in PROPOSALS] + [f"{p['mission_surface']}: deterministic fixture and refusal receipt" for p in PROPOSALS]
CANDIDATES = [f"{p['mission_surface']}: bounded executable prototype" for p in PROPOSALS] + [
    "robust-mutex owner-death state enumerator", "UNIX ancillary truncation checker", "GHP weight-operator mutation board", "BSSN algebraic-constraint checker", "LoTSS DR2 zero-row schema adapter", "refrigeration intake refusal replay", "cold-room alarm handover replay", "ECDSA cryptosuite vector simulator", "FAPI message-retention minimization checker", "refrigeration authority noncompensation matrix lint",
]
SKILLS = [f"ghc-family-v651-v4-{p['slug']}" for p in PROPOSALS]
RUNNERS = [
    "ghc_family_v651_v4_method_and_ipc.py", "ghc_family_v651_v4_gmut_boards.py", "ghc_family_v651_v4_zero_row_and_refrigeration.py", "ghc_family_v651_v4_identity_and_authority.py", "ghc_family_v651_v4_formats.py", "ghc_family_v651_v4_accessibility.py", "ghc_family_v651_v4_numeric_and_nonconversion.py", "ghc_family_v651_v4_stage20.py", "ghc_family_v651_v4_portfolios.py", "ghc_family_v651_v4_validate.py",
]
CLEAN_FIX_REFINE = [f"{p['mission_surface']}: preserve exact source and outcome vocabulary" for p in PROPOSALS] + [f"{p['mission_surface']}: normalize UTF-8 JSON and compatibility metadata" for p in PROPOSALS]
