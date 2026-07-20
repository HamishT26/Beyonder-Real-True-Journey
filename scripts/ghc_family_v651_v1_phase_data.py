#!/usr/bin/env python3
"""Frozen Sable Rook v651-v1 x1 data; no x2 observations live here."""

from __future__ import annotations


PHASE = "v651-v1"
OWNER = "Sable Rook"
PRONOUNS = "they/them"
ROLE = "relational evidence-and-reproducibility steward"
HOPE = "make every surviving claim easy to challenge or retract"
BRANCH = "codex/GHC-Family/sable-rook-full-tools"
PHASE_ROOT = "docs/sable-rook/v651-v1"

SOURCE_BRANCH = "codex/GHC-Family/ilyra-fen-full-tools"
SOURCE_HEAD = "b8d2d25747fcda747f77e6cf788a87e95062de00"
SOURCE_ORIGIN = "f566d4b67bce4457cf5207f5409bbaa3427428a0"
SOURCE_X1 = "d8726faad1ae416ef31f98a8744901eeedfe3c56"
SOURCE_EVIDENCE = "325c410a16241cd8fa21706f82ab2bfd8ed47531"
SOURCE_ORIGINAL_FINAL = "4dc0a911415cc19b871008cb903e03605a7bfca5"
SOURCE_PRIOR_CORRECTION = "549e39d8020955188cdf49618a1e60ce4df205ba"
PRIOR_FROZEN = 900
INHERITED_NEGATIVES = 6443
INHERITED_OPEN_GAPS = 50
INHERITED_EXACT_GATES = 51
PRIMARY_FOCUS = "GMUT Mind"
BOUNDED_PRACTICE = (
    "airport baggage reconciliation and aircraft ground deicing or anti-icing "
    "amendment, hold, correction-readback, workload control, and shift handover "
    "as a synthetic learning and interface-design lens only"
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
        gate = "Emit reservations only; make no operational, remedy, legal, cultural, data-governance, or Maori-authority decision."
    elif disposition == "represented":
        approval = "candidate_bounded_synthetic_proxy"
        lane = "x2_synthetic_proxy_only"
        gate = "Reject every preregistered mutation and retain proxy status with zero participant, production, professional, operational, or authority credit."
    else:
        approval = "safe_now_bounded_software_symbolic_formal_or_structural"
        lane = "x2_bounded_owner_local"
        gate = "Reject every preregistered mutation and emit only the declared bounded software, symbolic, formal, numerical, or structural completion."
    return {
        "proposal_id": f"V6511-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar": pillar,
        "mission_surface": mission,
        "hypothesis": f"A bounded {mission} artifact can expose declared obligations while refusing unsupported scientific, operational, identity, or authority promotion.",
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
        "rollback_or_recovery": "Stop the proposal, retain every failed witness, rewrite no history, and leave external, sibling, participant, production, and authority state unchanged.",
        "protected_gates": PROTECTED,
        "expected_disposition": disposition,
        "novelty_against_900_frozen_proposals": novelty,
    }


PROPOSALS = [
    proposal(1, "Method Flow two-phase-commit coordinator, participant, prepare, presumed-abort, heuristic-outcome, durable-log, cancellation, teardown, and evidence-credit tribunal", "two-phase-commit", "THOS Body", "completed", ["SRC-CONSENSUS-COMMIT"], "two-phase commit lifecycle and recovery control", "Distributed transaction topics exist, but no frozen title isolates prepare votes, presumed abort, heuristic outcomes, durable recovery, cancellation, teardown, and evidence credit together."),
    proposal(2, "DSSE pre-authentication-encoding, payload-type, detached-payload, signature-threshold, key-identity, envelope, nontransitive-credit, and refusal tribunal", "dsse-envelope", "Freed ID and CBR Heart", "completed", ["SRC-DSSE"], "DSSE envelope and pre-authentication encoding", "Earlier SLSA and in-toto work does not isolate DSSE pre-authentication encoding, payload-type confusion, detached payloads, threshold policy, and nontransitive evidence credit."),
    proposal(3, "GMUT Lee-Wick complex-pole, contour-prescription, pinch, negative-metric, cutting, truncation, EFT, unit, and observation-firewall board", "lee-wick-board", "GMUT Mind", "completed", ["SRC-LEE-WICK"], "Lee-Wick complex-pole obligations", "No frozen GMUT board isolates complex poles, contour prescriptions, pinches, negative-metric states, cutting obligations, EFT truncation, and observation refusal."),
    proposal(4, "GMUT worldline proper-time, gauge-fixing, zero-mode, spin-factor, boundary-condition, measure, truncation, EFT, unit, and observation-firewall board", "worldline-board", "GMUT Mind", "completed", ["SRC-WORLDLINE"], "worldline formalism obligations", "No frozen GMUT board isolates worldline proper time, gauge fixing, zero modes, spin factors, boundary conditions, measures, EFT truncation, and observation refusal."),
    proposal(5, "GMUT ALMA Science Archive calibrated-measurement-set, product-lineage, quality, calibration, selection, checksum, covariance, and zero-row likelihood-refusal adapter", "alma-zero-row", "GMUT Mind", "open_gap", ["SRC-ALMA"], "ALMA calibrated-product readiness", "No frozen zero-row adapter targets ALMA calibrated measurement sets, restoration lineage, quality and calibration state, selection, checksums, covariance, and likelihood refusal."),
    proposal(6, "THOS airport baggage tag, flight, container, custody, reconciliation, rush-bag, dangerous-goods hold, correction-readback, workload, and shift-handover proxy", "baggage-reconciliation", "THOS Body", "represented", ["SRC-IATA-BAGGAGE"], "airport baggage reconciliation workflow", "No frozen practice proxy isolates baggage tag, flight and container lineage, custody change, reconciliation, rush-bag state, dangerous-goods hold, workload, correction, and handover."),
    proposal(7, "THOS aircraft ground deicing and anti-icing fluid, weather, holdover-time, inspection, dispatch-boundary, amendment, correction-readback, workload, and handover proxy", "ground-deicing", "THOS Body", "represented", ["SRC-FAA-DEICING"], "aircraft ground deicing workflow", "No frozen practice proxy isolates fluid and weather state, holdover-time estimates, inspection, dispatch boundary, amendment, correction readback, workload, and handover."),
    proposal(8, "Freed ID OpenID CIBA backchannel-request, auth-req-id, poll, ping, push, binding-message, expiry, replay, minimization, and nonproduction profile", "openid-ciba", "Freed ID and CBR Heart", "represented", ["SRC-CIBA"], "OpenID CIBA backchannel authentication", "No frozen identity title covers CIBA backchannel request acknowledgement, auth_req_id, poll, ping and push modes, binding messages, expiry, replay, and minimization."),
    proposal(9, "Freed ID OpenID4VP 1.0 DCQL, nonce, response-mode, transaction-data, holder-binding, redirect, replay, minimization, and nonproduction profile", "openid4vp-dcql", "Freed ID and CBR Heart", "represented", ["SRC-OPENID4VP"], "OpenID4VP DCQL presentation exchange", "No frozen identity title covers final OpenID4VP 1.0 DCQL queries, transaction-data binding, response modes, nonce, redirect, holder binding, replay, and minimization."),
    proposal(10, "CBR airport baggage and ground-deicing disability access, passenger-worker privacy, property, dangerous-goods disclosure, remedy, affected-party, legal, cultural, data-governance, and Maori-authority matrix", "airport-authority", "Freed ID and CBR Heart", "exact_gate", ["SRC-NZ-HRA", "SRC-NZ-PRIVACY", "SRC-TE-MANA-RARAUNGA"], "airport access, privacy, remedy, and authority reservation", "No frozen matrix combines baggage and deicing access, passenger and worker privacy, property, dangerous-goods disclosure, remedy, affected-party legitimacy, and Maori data-authority reservations."),
    proposal(11, "PE-COFF DOS-stub, signature, COFF-header, optional-header, section-table, RVA, offset, size, overlap, certificate-table, resource-budget, and refusal tribunal", "pe-coff", "THOS Body", "completed", ["SRC-PE-COFF"], "PE and COFF structural refusal", "No frozen format tribunal isolates the DOS stub, PE signature, COFF and optional headers, section and RVA mapping, overlap, certificate table, and resource budgets."),
    proposal(12, "Mach-O magic, fat-slice, CPU-binding, load-command, segment, section, offset, code-signature, resource-budget, and refusal tribunal", "mach-o", "THOS Body", "completed", ["SRC-MACHO"], "Mach-O structural refusal", "No frozen format tribunal isolates thin and fat magic, slice bounds, CPU binding, load commands, segments, sections, offsets, code-signature region, and resource budgets."),
    proposal(13, "Accessible swimlane diagram name, lane, actor, order, dependency, non-colour cue, text-table alternative, focus, print, responsive, and manual-evaluation audit", "accessible-swimlane", "THOS Body", "completed", ["SRC-WCAG22", "SRC-WAI-COMPLEX"], "accessible swimlane diagram structure", "No frozen accessibility audit isolates swimlane actors and lanes, order and dependencies, non-colour cues, text-table alternatives, focus, print, and responsive reservations."),
    proposal(14, "Thermo-Psyche Wien-displacement spectral-representation, peak-variable, wavelength-frequency Jacobian, temperature, constant, unit, physical-domain, and agency-nonconversion classifier", "wien-nonconversion", "Trinity Mandala bridge", "completed", ["SRC-NIST-WIEN"], "Wien displacement nonconversion classification", "Planck-law work exists, but no frozen classifier isolates representation-dependent spectral peaks, wavelength-frequency Jacobians, displacement constants, units, and agency refusal."),
    proposal(15, "GMRES Arnoldi-basis, Hessenberg, Krylov, restart, preconditioner, residual, orthogonality, stagnation, nonfinite, iteration-budget, and refusal tribunal", "gmres", "GMUT Mind", "completed", ["SRC-GMRES"], "GMRES numerical obligation control", "No frozen numerical tribunal isolates GMRES Arnoldi and Hessenberg structure, restarts, preconditioning, residuals, orthogonality loss, stagnation, nonfinite state, and budgets."),
    proposal(16, "Stage 20 model-X-knockoff exchangeability, antisymmetry, covariate-distribution, FDR, threshold, dependence, leakage, subgroup, uncertainty, and nonpromotion board", "model-x-knockoff", "Trinity Mandala bridge", "completed", ["SRC-MODELX"], "model-X knockoff design obligations", "No frozen Stage 20 board isolates model-X exchangeability, antisymmetric statistics, covariate-distribution assumptions, FDR thresholds, dependence, leakage, subgroup, uncertainty, and nonpromotion."),
    proposal(17, "OpenAPI 3.2 document, path, operation, reference, schema-dialect, streaming-media, security, example, cycle, depth, resource-budget, and refusal tribunal", "openapi-3-2", "THOS Body", "completed", ["SRC-OPENAPI32"], "OpenAPI 3.2 structural refusal", "No frozen tribunal targets OpenAPI 3.2 paths, operations, references, schema dialects, streaming media, security declarations, examples, cycles, depth, and budgets."),
    proposal(18, "X.509 certification-path trust-anchor, basic-constraints, name-constraints, policy, key-usage, time, algorithm, revocation-state, critical-extension, and refusal tribunal", "x509-path", "Freed ID and CBR Heart", "completed", ["SRC-RFC5280"], "X.509 path structural obligation control", "No frozen tribunal isolates trust anchors, path validation, basic and name constraints, policies, key usage, time, algorithm, revocation state, critical extensions, and refusal."),
    proposal(19, "Uptane 2.1 root, targets, snapshot, timestamp, director, image-repository, threshold, freeze, rollback, mix-and-match, resource-budget, and refusal tribunal", "uptane-2-1", "THOS Body", "completed", ["SRC-UPTANE21"], "Uptane 2.1 metadata refusal", "TUF and supply-chain work exists, but no frozen tribunal isolates current Uptane 2.1 director and image repositories, role thresholds, freeze, rollback, mix-and-match, and bounded refusal."),
    proposal(20, "Nix derivation input-closure, output-spec, store-path, fixed-output, content-address, impurity, substitution, reproducibility-boundary, nontransitive-credit, and refusal tribunal", "nix-derivation", "THOS Body", "completed", ["SRC-NIX-DERIVATION"], "Nix derivation structural refusal", "No frozen tribunal isolates Nix derivation inputs and outputs, store paths, fixed and content addressing, impurity, substitution, reproducibility boundary, and nontransitive credit."),
]


def source(source_id, status, kind, title, url, implication):
    return {"source_id": source_id, "status": status, "kind": kind, "title": title, "url": url, "phase_implication": implication}


SOURCES = [
    source("SRC-CONSENSUS-COMMIT", "stable", "primary_research", "Consensus on Transaction Commit", "https://arxiv.org/abs/cs/0408036", "Supports bounded atomic-commit state distinctions only; no production transaction assurance."),
    source("SRC-DSSE", "current", "official_specification", "Dead Simple Signing Envelope protocol", "https://github.com/secure-systems-lab/dsse/blob/master/protocol.md", "Supports synthetic envelopes only; no real keys, signatures, PKI, or supply-chain assurance."),
    source("SRC-LEE-WICK", "stable", "primary_research", "A new formulation of Lee-Wick quantum field theory", "https://arxiv.org/abs/1703.04584", "Supports a typed controversy-aware obligation board only; no unitarity proof or physical claim."),
    source("SRC-WORLDLINE", "stable", "primary_research", "Perturbative Quantum Field Theory in the String-Inspired Formalism", "https://arxiv.org/abs/hep-th/0101036", "Supports typed worldline obligations only; no physical state or empirical result."),
    source("SRC-ALMA", "current", "official_data_documentation", "NRAO Science Ready Data Products for ALMA", "https://science.nrao.edu/srdp/science-ready-data-products-srdp-for-alma", "Supports a zero-row readiness contract only; no query, download, restoration, or ingestion occurs."),
    source("SRC-IATA-BAGGAGE", "current", "official_industry_standard_context", "IATA Baggage Tracking and Resolution 753", "https://www.iata.org/en/programs/ops-infra/baggage/baggage-tracking/", "Supplies synthetic baggage-state vocabulary only; no airline, airport, safety, or operational authority."),
    source("SRC-FAA-DEICING", "current", "official_aviation_guidance", "FAA Aircraft Ground Deicing", "https://www.faa.gov/other_visit/aviation_industry/airline_operators/airline_safety/deicing", "Supplies synthetic deicing vocabulary only; no dispatch, airworthiness, or safety authority."),
    source("SRC-CIBA", "stable", "official_final_specification", "OpenID Connect Client-Initiated Backchannel Authentication Core 1.0", "https://openid.net/specs/openid-client-initiated-backchannel-authentication-core-1_0.html", "Supports synthetic request vectors only; no accounts, tokens, keys, authentication, or interoperability."),
    source("SRC-OPENID4VP", "current", "official_final_specification", "OpenID for Verifiable Presentations 1.0 Final", "https://openid.net/specs/openid-4-verifiable-presentations-1_0-final.html", "Supports synthetic presentation vectors only; no credentials, wallets, keys, proofs, or interoperability."),
    source("SRC-NZ-HRA", "current", "official_legal_context", "New Zealand Human Rights Act 1993", "https://www.legislation.govt.nz/act/public/1993/0082/latest/whole.html", "Keeps disability access, discrimination, and legal interpretation exact-gated."),
    source("SRC-NZ-PRIVACY", "current", "official_legal_context", "New Zealand Privacy Act 2020", "https://www.legislation.govt.nz/act/public/2020/0031/latest/whole.html", "Keeps passenger and worker privacy, disclosure, remedies, and legal interpretation exact-gated."),
    source("SRC-TE-MANA-RARAUNGA", "current", "maori_authority_context", "Te Mana Raraunga principles of Maori data sovereignty", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Keeps Maori data governance under Maori authority; software cannot exercise it."),
    source("SRC-PE-COFF", "current", "official_format_specification", "Microsoft Portable Executable and Common Object File Format", "https://learn.microsoft.com/en-us/windows/win32/debug/pe-format", "Supports disposable synthetic byte fixtures only; no execution or production binary assurance."),
    source("SRC-MACHO", "stable", "official_platform_documentation", "Apple Overview of the Mach-O Executable Format", "https://developer.apple.com/library/archive/documentation/Performance/Conceptual/CodeFootprint/Articles/MachOOverview.html", "Supports synthetic structure fixtures only; no execution, signing, or Apple-platform certification."),
    source("SRC-WCAG22", "stable", "official_accessibility_standard", "Web Content Accessibility Guidelines 2.2", "https://www.w3.org/TR/WCAG22/", "Supports structural obligations only, not complete accessibility conformance."),
    source("SRC-WAI-COMPLEX", "current", "official_accessibility_guidance", "WAI alternative content for complex information and tasks", "https://www.w3.org/WAI/WCAG2/supplemental/patterns/o7p02-alternative-content/", "Supports a structural alternative-content contract; manual and affected-user evaluation remains reserved."),
    source("SRC-NIST-WIEN", "stable", "official_scientific_reference", "NIST optical-radiation measurements: Wien displacement law", "https://nvlpubs.nist.gov/nistpubs/Legacy/TN/nbstechnicalnote910-8.pdf", "Supports thermodynamic definitions only, never psyche, autonomy, justice, or agency conversion."),
    source("SRC-GMRES", "stable", "primary_research", "GMRES: A Generalized Minimal Residual Algorithm", "https://doi.org/10.1137/0907058", "Supports bounded numerical fixtures only; no universal convergence or physical-model guarantee."),
    source("SRC-MODELX", "stable", "primary_research", "Panning for Gold: Model-X Knockoffs", "https://arxiv.org/abs/1610.02351", "Supports design obligations only; no participant discovery, FDR guarantee for this phase, or Stage 20 authority."),
    source("SRC-OPENAPI32", "current", "official_specification", "OpenAPI Specification 3.2.0", "https://spec.openapis.org/oas/v3.2.0.html", "Supports synthetic structural fixtures only; no deployed API or security assurance."),
    source("SRC-RFC5280", "stable", "official_standard", "RFC 5280 Internet X.509 PKI Certificate and CRL Profile", "https://www.rfc-editor.org/rfc/rfc5280.html", "Supports synthetic path-state fixtures only; no real trust anchor, certificate, revocation, or security review."),
    source("SRC-UPTANE21", "current", "official_standard", "Uptane Standard for Design and Implementation 2.1.0", "https://uptane.org/docs/latest/standard/uptane-standard", "Supports synthetic metadata fixtures only; no vehicle, repository, key, update, or security certification."),
    source("SRC-NIX-DERIVATION", "current", "official_reference_manual", "Nix 2.34.8 Store Derivation and Deriving Path", "https://releases.nixos.org/nix/nix-2.34.8/manual/store/derivation/index.html", "Supports synthetic derivation fixtures only; no Nix installation, build, substitution, or reproducibility certification."),
]


REJECTED_COLLISIONS = [
    {"seed": "Seeley-DeWitt heat-kernel board", "reason": "already frozen in v647-v3"},
    {"seed": "Cutkosky cutting board", "reason": "already frozen in v648-v4"},
    {"seed": "Nielsen identity board", "reason": "already frozen in v647-v1 and v650-v2"},
    {"seed": "Kallen-Lehmann spectral board", "reason": "already frozen"},
    {"seed": "LSZ reduction board", "reason": "already frozen"},
    {"seed": "Gaia public-data adapter", "reason": "already frozen in v645-v7"},
    {"seed": "Euclid public-data adapter", "reason": "already frozen"},
    {"seed": "railway handover proxy", "reason": "multiple frozen railway practice lanes exist"},
    {"seed": "OpenID Federation profile", "reason": "multiple frozen federation profiles exist"},
    {"seed": "WebAssembly tribunal", "reason": "already frozen in v647-v8"},
    {"seed": "ZIP64 tribunal", "reason": "already frozen in v649-v8"},
    {"seed": "Clapeyron classifier", "reason": "already frozen"},
    {"seed": "Parquet tribunal", "reason": "already frozen in v650-v2"},
    {"seed": "SPDX tribunal", "reason": "already frozen in v650-v2"},
    {"seed": "SCIM profile", "reason": "already frozen"},
    {"seed": "PKCE profile", "reason": "already frozen"},
    {"seed": "Anderson acceleration tribunal", "reason": "already frozen in v650-v1"},
    {"seed": "conformal-prediction board", "reason": "already frozen in v647-v5"},
    {"seed": "NetCDF tribunal", "reason": "already frozen"},
    {"seed": "HDF5 tribunal", "reason": "already frozen"},
]


SAFE_NOW = [
    f"{p['mission_surface']}: exact contract and protected-gate lint" for p in PROPOSALS
] + [f"{p['mission_surface']}: deterministic fixture and refusal receipt" for p in PROPOSALS]

CANDIDATES = [
    f"{p['mission_surface']}: bounded executable prototype" for p in PROPOSALS
] + [
    "two-phase-commit crash-point schedule enumerator",
    "DSSE payload-type confusion rejector",
    "Lee-Wick contour-obligation mutation board",
    "worldline zero-mode and boundary-condition checker",
    "ALMA zero-row calibration-lineage adapter",
    "baggage reconciliation late-event replay",
    "ground-deicing holdover amendment replay",
    "OpenID CIBA mode-transition simulator",
    "OpenID4VP DCQL minimization checker",
    "airport authority noncompensation matrix lint",
]

SKILLS = [f"ghc-family-v651-v1-{p['slug']}-audit" for p in PROPOSALS]

RUNNERS = [
    "ghc_family_v651_v1_method_and_provenance.py",
    "ghc_family_v651_v1_gmut_boards.py",
    "ghc_family_v651_v1_zero_row_and_thos.py",
    "ghc_family_v651_v1_identity_and_authority.py",
    "ghc_family_v651_v1_binary_tribunals.py",
    "ghc_family_v651_v1_accessibility.py",
    "ghc_family_v651_v1_numeric_and_nonconversion.py",
    "ghc_family_v651_v1_stage20.py",
    "ghc_family_v651_v1_portfolios.py",
    "ghc_family_v651_v1_validate.py",
]

CLEAN_FIX_REFINE = [
    f"{p['mission_surface']}: preserve exact source and outcome vocabulary" for p in PROPOSALS
] + [f"{p['mission_surface']}: normalize UTF-8 JSON and compatibility metadata" for p in PROPOSALS]
