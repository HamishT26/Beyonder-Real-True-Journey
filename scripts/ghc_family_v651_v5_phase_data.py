#!/usr/bin/env python3
"""Frozen Eiren Kestrel v651-v5 x1 data; no x2 observations live here."""

from __future__ import annotations


PHASE = "v651-v5"
OWNER = "Eiren Kestrel"
PRONOUNS = "she/they"
ROLE = "relational evidence-boundary integrator"
HOPE = "make each advance useful without letting confidence outrun evidence"
BRANCH = "codex/GHC-Family/eiren-kestrel-v648-v3-2-full-tools"
PHASE_ROOT = "docs/eiren-kestrel/v651-v5"

SOURCE_BRANCH = "codex/GHC-Family/sylven-arc-v642-v8-full-tools"
SOURCE_HEAD = "d5c9a16b3efb76a138944d97211bc0a3b7bcd716"
SOURCE_ORIGIN = "3ec09ba3dfc019fd9def1e58eb4943b18bcc7def"
SOURCE_X1 = "5607827833a4c60b0708ce543ef0d32e0afdbe9f"
SOURCE_EVIDENCE = "26b7fbcf3cc4381b2434ecbf4485d8b2dfb96a2c"
SOURCE_CLOSEOUT = "d5c9a16b3efb76a138944d97211bc0a3b7bcd716"
PRIOR_FROZEN = 980
INHERITED_NEGATIVES = 6948
STARTUP_NEGATIVES = 19
INHERITED_OPEN_GAPS = 54
INHERITED_EXACT_GATES = 55
PRIMARY_FOCUS = "GMUT Mind"
BOUNDED_PRACTICE = (
    "commercial-greenhouse climate control, fertigation exception review, chemical and biosecurity refusal, "
    "workload control, correction readback, and shift handover as a synthetic learning and design lens only"
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
        gate = "Emit a query-free zero-row receipt and refuse every download, ingestion, likelihood, posterior, constraint, or empirical promotion."
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
        "proposal_id": f"V6515-P{number:02d}",
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
        "novelty_against_980_frozen_proposals": novelty,
        "novelty_against_960_frozen_proposals": novelty,
        "novelty_against_940_frozen_proposals": novelty,
        "novelty_against_920_frozen_proposals": novelty,
    }


PROPOSALS = [
    proposal(1, "Method Flow Linux io_uring submission-queue, completion-queue, user-data correlation, cancellation, multishot, timeout, queue-depth, teardown, and evidence-credit tribunal", "io-uring-lifecycle", "THOS Body", "completed", ["SRC-IO-URING"], "io_uring lifecycle and cancellation control", "No frozen proposal isolates io_uring submission and completion queues, user-data correlation, cancellation, multishot completion, timeouts, queue depth, teardown, and bounded evidence credit."),
    proposal(2, "Method Flow Chase-Lev work-stealing deque owner-bottom, thief-top, resize, last-item race, memory-order, empty-state, bounded-retry, teardown, and evidence-credit tribunal", "chase-lev-deque", "THOS Body", "completed", ["SRC-CHASE-LEV"], "Chase-Lev work-stealing deque control", "No frozen proposal isolates Chase-Lev owner-bottom and thief-top operations, resizing, the last-item race, memory ordering, empty state, bounded retry, teardown, and evidence credit."),
    proposal(3, "GMUT York-Lichnerowicz conformal-metric, transverse-traceless split, mean-curvature, Hamiltonian-constraint, momentum-constraint, ellipticity, boundary, gauge, EFT, unit, and observation-firewall board", "york-lichnerowicz", "GMUT Mind", "completed", ["SRC-YORK-LICHNEROWICZ"], "York-Lichnerowicz constraint obligation control", "No frozen GMUT proposal isolates the York-Lichnerowicz conformal metric, transverse-traceless split, mean curvature, Hamiltonian and momentum constraints, ellipticity, boundaries, gauge, EFT, units, and observation refusal."),
    proposal(4, "GMUT Regge-Wheeler-Zerilli odd-parity, even-parity, spherical-harmonic, master-variable, potential, horizon-boundary, infinity-boundary, source, gauge, EFT, unit, and observation-firewall board", "regge-wheeler-zerilli", "GMUT Mind", "completed", ["SRC-REGGE-WHEELER", "SRC-ZERILLI"], "Regge-Wheeler-Zerilli obligation control", "No frozen GMUT proposal isolates paired odd and even Schwarzschild perturbations, master variables, potentials, horizon and infinity boundaries, source terms, gauge, EFT, units, and observation refusal."),
    proposal(5, "GMUT NASA Roman WFI prelaunch archive, product-level, calibration-context, quality, selection, covariance, checksum, availability-watch, version-watch, query-free, and zero-row likelihood-refusal adapter", "roman-wfi-zero-row", "GMUT Mind", "open_gap", ["SRC-ROMAN-MAST"], "Roman WFI prelaunch zero-row readiness", "No frozen zero-row adapter targets the prelaunch Roman WFI archive and product levels with calibration context, quality, selection, covariance, checksum, availability and version watch, query-free execution, and likelihood refusal."),
    proposal(6, "THOS commercial-greenhouse temperature, humidity, carbon-dioxide, vent, heating, sensor-exception, alarm, accessible-notice, correction-readback, workload, and shift-handover proxy", "greenhouse-climate-handover", "THOS Body", "represented", ["SRC-WORKSAFE-HORTICULTURE"], "greenhouse climate-control and handover workflow", "No frozen practice proxy isolates greenhouse climate variables, vents, heating, sensor exceptions, alarms, accessible notices, correction readback, workload, and shift handover."),
    proposal(7, "THOS commercial-greenhouse fertigation water-batch, nutrient-batch, chemical-inventory, safety-data-sheet, dosing-refusal, spill-isolation, crop-hold, biosecurity-escalation, workload, and shift-handover proxy", "greenhouse-fertigation-handover", "THOS Body", "represented", ["SRC-WORKSAFE-HAZSUB", "SRC-MPI-BIOSECURITY"], "greenhouse fertigation exception and handover workflow", "No frozen practice proxy isolates greenhouse fertigation batch identity, chemical inventory and safety data sheets, dosing refusal, spill isolation, crop holds, biosecurity escalation, workload, and handover."),
    proposal(8, "Freed ID W3C ECDSA-SD base-proof, selective-pointer, HMAC-label-map, mandatory-disclosure, derived-proof, proof-value-component, curve-and-key refusal, unlinkability-boundary, and synthetic-vector profile", "ecdsa-sd-profile", "Freed ID and CBR Heart", "represented", ["SRC-W3C-ECDSA"], "ECDSA-SD selective-disclosure profile", "Earlier ECDSA canonicalization and BBS derived-proof work does not isolate ECDSA-SD base and derived proofs, selective pointers, HMAC label maps, mandatory disclosure, proof-value components, curve refusal, and its distinct unlinkability boundary."),
    proposal(9, "Freed ID RFC 8693 OAuth token-exchange grant, subject-token, actor-token, token-type, delegation, impersonation, resource, audience, scope, issued-token-type, replay, minimization, and nonproduction profile", "oauth-token-exchange", "Freed ID and CBR Heart", "represented", ["SRC-RFC8693"], "OAuth token-exchange profile", "No frozen identity proposal targets RFC 8693 subject and actor token exchange, token types, delegation versus impersonation, resource, audience, scope, issued-token type, replay, and minimization."),
    proposal(10, "CBR greenhouse worker-and-seasonal-worker privacy, crop-and-site data, chemical-incident disclosure, water-and-environmental harm, accessible-notice, remedy, affected-party, legal, cultural, Maori-data-governance, and Maori-authority matrix", "greenhouse-authority", "Freed ID and CBR Heart", "exact_gate", ["SRC-WORKSAFE-HAZSUB", "SRC-NZ-PRIVACY", "SRC-TE-MANA-RARAUNGA"], "greenhouse incident, remedy, and authority reservation", "No frozen matrix isolates greenhouse worker and seasonal-worker privacy, crop and site data, chemical incident disclosure, water and environmental harm, accessible notice, remedy, affected parties, law, culture, Maori data governance, and Maori authority."),
    proposal(11, "System-V ELF magic, class, data-encoding, machine, entry-point, program-header, section-header, offset, size, segment, string-table, resource-budget, and refusal tribunal", "elf-structure", "THOS Body", "completed", ["SRC-ELF-GABI"], "ELF structural refusal", "No frozen format tribunal targets ELF magic, class, data encoding, machine, entry point, program and section headers, offsets, sizes, segments, string tables, and resource budgets."),
    proposal(12, "Snappy framing stream-identifier, chunk-type, little-endian-length, compressed-chunk, uncompressed-chunk, masked-CRC32C, skippable-chunk, unskippable-chunk, truncation, output-budget, and refusal tribunal", "snappy-framing", "THOS Body", "completed", ["SRC-SNAPPY"], "Snappy framing structural refusal", "No frozen format tribunal targets the Snappy stream identifier, chunk types and lengths, compressed and uncompressed chunks, masked CRC32C, skippable and unskippable chunks, truncation, and output budgets."),
    proposal(13, "bzip2 stream-magic, block-size, block-header, end-marker, combined-CRC, Burrows-Wheeler, run-length, Huffman-table, truncation, concatenation, output-and-ratio-budget, and refusal tribunal", "bzip2-stream", "THOS Body", "completed", ["SRC-BZIP2"], "bzip2 structural refusal", "No frozen format tribunal targets bzip2 stream magic, block size and markers, combined CRC, Burrows-Wheeler, run-length and Huffman structure, truncation, concatenation, and output and ratio budgets."),
    proposal(14, "Accessible date-picker input, choose-button, dialog-name, month-year-live-region, calendar-grid, selected-date, today-state, roving-focus, keyboard, escape, error, fallback, print, and manual-evaluation audit", "accessible-date-picker", "THOS Body", "completed", ["SRC-WAI-DATEPICKER"], "accessible date-picker structure", "No frozen accessibility audit isolates date-picker input and button naming, dialog and live-region semantics, calendar grid, selected and today states, roving focus, keyboard and escape behavior, errors, fallback, print, and manual reservations."),
    proposal(15, "Thermo-Psyche Brunauer-Emmett-Teller multilayer-adsorption, relative-pressure, monolayer-capacity, C-constant, linear-region, saturation, temperature, unit, model-assumption, and agency-nonconversion classifier", "bet-nonconversion", "Trinity Mandala bridge", "completed", ["SRC-BET"], "BET adsorption nonconversion", "No frozen nonconversion classifier isolates BET multilayer adsorption, relative pressure, monolayer capacity, the C constant, linear-region selection, saturation, temperature, units, model assumptions, and agency refusal."),
    proposal(16, "TFQMR non-Hermitian-system, transpose-free recurrence, quasi-minimization, residual-estimate, true-residual-check, breakdown, nonfinite, preconditioner, iteration-budget, unit, and refusal tribunal", "tfqmr", "GMUT Mind", "completed", ["SRC-TFQMR"], "TFQMR numerical obligation control", "No frozen numerical tribunal isolates TFQMR non-Hermitian systems, transpose-free recurrence, quasi-minimization, estimated versus true residual, breakdown, nonfinite state, preconditioning, iteration budgets, and units."),
    proposal(17, "Stage 20 causal-forest honesty, sample-splitting, unconfoundedness, overlap, conditional-effect, nuisance-model, heterogeneity, calibration, subgroup, uncertainty, interpretation, and nonpromotion board", "causal-forest", "Trinity Mandala bridge", "completed", ["SRC-CAUSAL-FOREST"], "causal-forest obligation control", "No frozen Stage 20 board isolates causal-forest honesty, sample splitting, unconfoundedness, overlap, conditional effects, nuisance models, heterogeneity, calibration, subgroup analysis, uncertainty, interpretation, and nonpromotion."),
    proposal(18, "Adaptive Radix Tree node-type, prefix-compression, optimistic-path, child-index, growth, shrink, insertion, deletion, lookup, key-byte, memory-bound, and refusal tribunal", "adaptive-radix-tree", "THOS Body", "completed", ["SRC-ART"], "adaptive radix tree obligation control", "No frozen data-structure tribunal isolates adaptive radix tree node types, prefix compression, optimistic paths, child indexing, growth and shrink transitions, insertion, deletion, lookup, key bytes, and memory bounds."),
    proposal(19, "Range asymmetric-numeral-system state, frequency-table, cumulative-interval, encode-step, decode-step, reverse-order, renormalization, normalization, underflow, overflow, stream-budget, and refusal tribunal", "rans", "THOS Body", "completed", ["SRC-RANS"], "range asymmetric numeral system control", "No frozen coding tribunal isolates rANS state, frequency and cumulative tables, encode and decode steps, reverse order, renormalization, normalization, underflow, overflow, and stream budgets."),
    proposal(20, "Netpbm PNM magic, PBM, PGM, PPM, ASCII, binary, width, height, maxval, whitespace, comment, sample-depth, trailing-data, pixel-and-output-budget, and refusal tribunal", "netpbm-pnm", "THOS Body", "completed", ["SRC-NETPBM"], "Netpbm PNM structural refusal", "No frozen image-format tribunal targets the Netpbm PNM family, PBM, PGM and PPM variants, ASCII and binary encodings, dimensions, maxval, whitespace and comments, sample depth, trailing data, and pixel and output budgets."),
]


def source(source_id, status, kind, title, url, implication):
    return {"source_id": source_id, "status": status, "kind": kind, "title": title, "url": url, "phase_implication": implication}


SOURCES = [
    source("SRC-IO-URING", "current", "official_system_documentation", "Linux io_uring userspace API and manual pages", "https://man7.org/linux/man-pages/man7/io_uring.7.html", "Supports disposable state fixtures only; no Linux execution, production I/O, cancellation authority, or exhaustive-security assurance."),
    source("SRC-CHASE-LEV", "stable", "primary_research", "Dynamic Circular Work-Stealing Deque", "https://doi.org/10.1145/1073970.1073974", "Supports bounded deque state and race fixtures only; no production scheduler or lock-free correctness proof."),
    source("SRC-YORK-LICHNEROWICZ", "stable", "primary_research", "Gravitational Degrees of Freedom and the Initial-Value Problem", "https://doi.org/10.1103/PhysRevLett.26.1656", "Supports typed constraint obligations only; no physical initial data, solution theorem, prediction, or empirical GMUT result."),
    source("SRC-REGGE-WHEELER", "stable", "primary_research", "Stability of a Schwarzschild Singularity", "https://doi.org/10.1103/PhysRev.108.1063", "Supports typed odd-parity obligations only; no physical perturbation state, stability theorem extension, waveform, or observation."),
    source("SRC-ZERILLI", "stable", "primary_research", "Effective Potential for Even-Parity Regge-Wheeler Gravitational Perturbation Equations", "https://doi.org/10.1103/PhysRevLett.24.737", "Supports typed even-parity obligations only; no physical perturbation state, waveform, likelihood, or observation."),
    source("SRC-ROMAN-MAST", "current", "official_data_documentation", "MAST Roman mission, products, and prelaunch status", "https://archive.stsci.edu/missions-and-data/roman", "Supports query-free zero-row prelaunch readiness only; no archive query, science row, likelihood, posterior, constraint, or empirical claim."),
    source("SRC-WORKSAFE-HORTICULTURE", "current", "official_practice_context", "WorkSafe horticulture safety improvement findings", "https://www.worksafe.govt.nz/about-us/news-and-media/worksafe-drives-horticulture-safety-improvements/", "Supplies synthetic greenhouse risk vocabulary only; no worker, site, competence, compliance, incident, or effectiveness evidence."),
    source("SRC-WORKSAFE-HAZSUB", "current", "official_practice_guidance", "WorkSafe hazardous-substance learning for agriculture and horticulture", "https://www.worksafe.govt.nz/about-us/news-and-media/new-learning-modules-for-hazardous-substances-in-agriculture/", "Supplies synthetic inventory, safety-data-sheet, risk, emergency, and worker-involvement vocabulary only; no operational or legal decision."),
    source("SRC-MPI-BIOSECURITY", "current", "official_practice_context", "MPI New Zealand biosecurity guidance", "https://www.mpi.govt.nz/biosecurity", "Keeps pest, disease, crop, containment, response, and biosecurity decisions external to repository software."),
    source("SRC-W3C-ECDSA", "current", "official_recommendation", "W3C Data Integrity ECDSA Cryptosuites v1.0", "https://www.w3.org/TR/vc-di-ecdsa/", "Supports synthetic selective-disclosure vectors only; no real key, proof, credential, lifecycle, interoperability, privacy review, or production identity event."),
    source("SRC-RFC8693", "stable", "official_standards_track_specification", "RFC 8693 OAuth 2.0 Token Exchange", "https://www.rfc-editor.org/rfc/rfc8693.html", "Supports synthetic message vectors only; no real subject, actor, key, token, account, network exchange, delegation decision, or trust governance."),
    source("SRC-NZ-PRIVACY", "current", "official_legal_context", "New Zealand Privacy Act 2020", "https://www.legislation.govt.nz/act/public/2020/0031/latest/versions.aspx", "Keeps collection, access, correction, use, disclosure, remedy, and legal interpretation exact-gated."),
    source("SRC-TE-MANA-RARAUNGA", "current", "maori_authority_context", "Te Mana Raraunga principles of Maori data sovereignty", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Keeps Maori wording, data, governance, benefit, consent, and authority under Maori authority; software cannot exercise it."),
    source("SRC-ELF-GABI", "stable", "official_abi_specification", "System V Generic ABI ELF specification", "https://refspecs.linuxfoundation.org/elf/gabi41.pdf", "Supports disposable synthetic headers and tables only; no loader, execution, production parser, or exhaustive-security assurance."),
    source("SRC-SNAPPY", "current", "primary_format_specification", "Google Snappy framing format", "https://github.com/google/snappy/blob/main/framing_format.txt", "Supports disposable synthetic frames only; no production decompressor or exhaustive-security assurance."),
    source("SRC-BZIP2", "current", "primary_format_documentation", "bzip2 and libbzip2 1.0.8 manual", "https://sourceware.org/bzip2/manual/manual.html", "Supports disposable synthetic streams only; no production decompressor, recovery guarantee, or exhaustive-security assurance."),
    source("SRC-WAI-DATEPICKER", "current", "official_accessibility_guidance", "WAI-ARIA Authoring Practices date-picker dialog example", "https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/examples/datepicker-dialog/", "Supports structural semantics only; manual keyboard, browser, assistive-technology, cognitive, Maori-language, and affected-user evaluation remains reserved."),
    source("SRC-BET", "stable", "primary_research", "Adsorption of Gases in Multimolecular Layers", "https://doi.org/10.1021/ja01269a023", "Supports physical adsorption-model definitions only; never psyche, agency, justice, participant, consciousness, or personhood conversion."),
    source("SRC-TFQMR", "stable", "primary_research", "A Transpose-Free Quasi-Minimal Residual Algorithm for Non-Hermitian Linear Systems", "https://doi.org/10.1137/0914029", "Supports bounded numerical fixtures only; no universal convergence, physical-model correctness, or empirical result."),
    source("SRC-CAUSAL-FOREST", "stable", "primary_methods_research", "Estimation and Inference of Heterogeneous Treatment Effects using Random Forests", "https://doi.org/10.1080/01621459.2017.1319839", "Supports typed design obligations only; zero participants and rows mean no causal effect, subgroup conclusion, treatment decision, or Stage 20 result."),
    source("SRC-ART", "stable", "primary_research", "The Adaptive Radix Tree: ARTful Indexing for Main-Memory Databases", "https://doi.org/10.1109/ICDE.2013.6544812", "Supports bounded tree-state fixtures only; no production index, concurrent correctness proof, or universal-performance guarantee."),
    source("SRC-RANS", "stable", "primary_research", "Asymmetric Numeral Systems", "https://arxiv.org/abs/0902.0271", "Supports bounded entropy-coding fixtures only; no production codec, encryption, error-correction, or universal-performance guarantee."),
    source("SRC-NETPBM", "current", "primary_format_specification", "Netpbm PNM format", "https://netpbm.sourceforge.net/doc/pnm.html", "Supports disposable synthetic images only; no user-image decoding, production parser, or exhaustive-security assurance."),
]


REJECTED_COLLISIONS = [
    {"seed": "hazard-pointer reclamation", "reason": "already frozen as V6504-P01"},
    {"seed": "epoch-based reclamation", "reason": "already frozen as V6496-P01"},
    {"seed": "Linux RCU", "reason": "already frozen as V6513-P01"},
    {"seed": "BBS derived proofs", "reason": "already frozen as V6464-P05"},
    {"seed": "GNAP grants", "reason": "already frozen as V6503-P05"},
    {"seed": "OpenID4VP", "reason": "already frozen in V6442-P05, V6465-P05, and V6511-P09"},
    {"seed": "OpenID4VCI", "reason": "already frozen in V6448-P05 and V6457-P05"},
    {"seed": "FAPI 2.0 Message Signing", "reason": "already frozen as V6514-P09"},
    {"seed": "FLAC frame parsing", "reason": "already frozen as V6505-P14"},
    {"seed": "Apache Avro object containers", "reason": "already frozen as V6505-P12"},
    {"seed": "MessagePack", "reason": "already frozen as V6502-P11"},
    {"seed": "CBOR Sequence", "reason": "already frozen as V6501-P12"},
    {"seed": "WARC", "reason": "already frozen as V6492-P07"},
    {"seed": "XZ", "reason": "already frozen as V6504-P12"},
    {"seed": "Brotli", "reason": "already frozen as V6491-P07"},
    {"seed": "regression discontinuity", "reason": "already frozen as V6478-P10 and V6491-P10"},
    {"seed": "proximal causal inference", "reason": "already frozen as V6483-P10"},
    {"seed": "principal stratification", "reason": "already frozen as V6486-P10"},
    {"seed": "synthetic control", "reason": "already frozen as V6482-P10 and V6492-P10"},
    {"seed": "LoTSS DR2 zero-row adapter", "reason": "already frozen as V6482-P03 and V6514-P05"},
    {"seed": "theatre stage-management practice", "reason": "already frozen as V6486-P04 and related authority work"},
    {"seed": "drinking-water treatment practice", "reason": "already frozen in V6488-P04 and earlier water workflows"},
    {"seed": "real greenhouse workers, crops, chemicals, sites, incidents, or decisions", "reason": "participant, privacy, professional, safety, environmental, legal, cultural, and affected-party gates forbid execution"},
    {"seed": "live identity keys, proofs, tokens, accounts, or services", "reason": "credential, account, network, privacy, production, security-review, and trust-governance gates forbid execution"},
]


SAFE_NOW = [f"{p['mission_surface']}: exact contract and protected-gate lint" for p in PROPOSALS] + [f"{p['mission_surface']}: deterministic fixture and refusal receipt" for p in PROPOSALS]
CANDIDATES = [f"{p['mission_surface']}: bounded executable prototype" for p in PROPOSALS] + [
    "io_uring completion-correlation state simulator", "Chase-Lev last-item race enumerator", "York-Lichnerowicz typed constraint checker", "Regge-Wheeler-Zerilli parity and boundary mutation board", "Roman WFI prelaunch zero-row availability adapter", "greenhouse climate-alarm handover replay", "greenhouse fertigation refusal replay", "ECDSA-SD pointer and label-map vector simulator", "OAuth token-exchange delegation and target checker", "greenhouse authority noncompensation matrix lint",
]
SKILLS = [f"ghc-family-v651-v5-{p['slug']}" for p in PROPOSALS]
RUNNERS = [
    "ghc_family_v651_v5_method_and_concurrency.py", "ghc_family_v651_v5_gmut_boards.py", "ghc_family_v651_v5_zero_row_and_greenhouse.py", "ghc_family_v651_v5_identity_and_authority.py", "ghc_family_v651_v5_formats.py", "ghc_family_v651_v5_accessibility.py", "ghc_family_v651_v5_numeric_and_nonconversion.py", "ghc_family_v651_v5_stage20.py", "ghc_family_v651_v5_portfolios.py", "ghc_family_v651_v5_validate.py",
]
CLEAN_FIX_REFINE = [f"{p['mission_surface']}: preserve exact source and outcome vocabulary" for p in PROPOSALS] + [f"{p['mission_surface']}: normalize UTF-8 JSON and compatibility metadata" for p in PROPOSALS]
