#!/usr/bin/env python3
"""Frozen Lyren Moss v653-v2 x1 data.

This module contains preregistration inputs only. It deliberately contains no
x2 observations, mutation outcomes, completion receipts, or route result.
"""

from __future__ import annotations


PHASE = "v653-v2"
PHASE_ID = "v653-gmut-thos-v2-x1-x2"
OWNER = "Lyren Moss"
PRONOUNS = "they/them"
ROLE = "boundary-lantern and evidence gardener"
HOPE = (
    "turn uncertainty into kind, inspectable paths without mistaking "
    "representation for reality"
)
PHASE_ROOT = "docs/lyren-moss/v653-v2"
BRANCH = "codex/GHC-Family/lyren-moss-v653-v2-full-tools"

SOURCE_BRANCH = "codex/GHC-Family/vesper-arlen-v653-v1-full-tools"
SOURCE_PARENT = "3b955da5070d8b73bbfc23acbbaac541c57cb1bc"
SOURCE_X1 = "9e03d9c0cbcfb4ff22e1b5df2ae143c59a1432ac"
SOURCE_EVIDENCE = "d62dc135c61fa2a7d7bbe383aa50f2d221bbe95a"
SOURCE_HEAD = "97989717f8447ef2fa09a37a92c76617dea30874"

PRIOR_FROZEN = 1450
INHERITED_NEGATIVES = 9441
INHERITED_OPEN_GAPS = 70
INHERITED_EXACT_GATES = 71
INHERITED_METHOD_FLOW_FAILED = 18
INHERITED_METHOD_FLOW_PASSING = 18
PRIMARY_FOCUS = "GMUT Mind"
BOUNDED_PRACTICE = (
    "research-model verification and accessible scientific-assurance handover"
)

OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]
SOURCE_STATUS_CLASSES = ["current", "stable", "draft", "watch"]
PROTECTED_GATES = [
    "real_empirical_data",
    "participant_or_operator_evidence",
    "professional_qualification_or_review",
    "production_identity_and_interoperability",
    "privacy_complete",
    "exhaustive_security",
    "complete_accessibility",
    "legal_cultural_and_maori_authority",
    "affected_party_acceptance_and_remedy",
    "independent_team_reproduction",
    "agi_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]


def source(source_id, status, kind, title, url, implication):
    return {
        "source_id": source_id,
        "status": status,
        "kind": kind,
        "title": title,
        "url": url,
        "phase_implication": implication,
    }


SOURCES = [
    source(
        "SRC-EINSTEIN-LANGEVIN",
        "stable",
        "primary_manuscript",
        "On the semiclassical Einstein-Langevin equation",
        "https://arxiv.org/abs/gr-qc/9811070",
        "Supports a stochastic-source and noise-kernel ledger only, not a measured fluctuation or semiclassical-gravity confirmation.",
    ),
    source(
        "SRC-MUKHANOV-SASAKI",
        "stable",
        "primary_review",
        "Theory of cosmological perturbations",
        "https://doi.org/10.1016/0370-1573(92)90044-Z",
        "Supports gauge-invariant scalar-mode bookkeeping without a power-spectrum or cosmological inference.",
    ),
    source(
        "SRC-DELTA-N",
        "stable",
        "primary_manuscript",
        "The inflationary prediction for primordial non-gaussianity",
        "https://arxiv.org/abs/astro-ph/0504045",
        "Supports a separate-universe derivative contract only, not inflationary or observational confirmation.",
    ),
    source(
        "SRC-KUNDT",
        "stable",
        "primary_paper",
        "The plane-fronted gravitational waves",
        "https://doi.org/10.1007/BF01328918",
        "Supports nonexpanding null-congruence and chart obligations without identifying a physical spacetime.",
    ),
    source(
        "SRC-BRINKMANN-ROSEN",
        "stable",
        "primary_manuscript",
        "Rosen coordinates in plane wave spacetimes",
        "https://arxiv.org/abs/1705.09533",
        "Supports a bounded Brinkmann-Rosen coordinate-map fixture with an explicit caustic-domain refusal.",
    ),
    source(
        "SRC-PLEBANSKI-DEMIANSKI",
        "stable",
        "primary_paper",
        "Rotating, charged, and uniformly accelerating mass in general relativity",
        "https://doi.org/10.1016/0003-4916(76)90240-2",
        "Supports parameter and root-order bookkeeping without a new solution or source interpretation.",
    ),
    source(
        "SRC-MAJUMDAR",
        "stable",
        "primary_paper",
        "A class of exact solutions of Einstein's field equations",
        "https://doi.org/10.1103/PhysRev.72.390",
        "Supports harmonic-potential and extremal-balance obligations only.",
    ),
    source(
        "SRC-EGUCHI-HANSON",
        "stable",
        "primary_paper",
        "Asymptotically flat self-dual solutions to Euclidean gravity",
        "https://doi.org/10.1007/BF00759271",
        "Supports bolt, identification, orientation, and regularity bookkeeping without a physical instanton claim.",
    ),
    source(
        "SRC-GODEL",
        "stable",
        "primary_paper",
        "An Example of a New Type of Cosmological Solutions of Einstein's Field Equations of Gravitation",
        "https://doi.org/10.1103/RevModPhys.21.447",
        "Supports a rotating-dust and chronology-reservation ledger without cosmological promotion.",
    ),
    source(
        "SRC-C-METRIC",
        "stable",
        "primary_paper",
        "Uniformly accelerating charged mass in general relativity",
        "https://doi.org/10.1103/PhysRevD.2.1359",
        "Supports root, axis, deficit, and acceleration-horizon obligations only.",
    ),
    source(
        "SRC-ADIABATIC",
        "stable",
        "primary_paper",
        "Adiabatic regularization of the energy-momentum tensor of a quantized field in homogeneous spaces",
        "https://doi.org/10.1103/PhysRevD.9.341",
        "Supports subtraction-order and ultraviolet bookkeeping without a renormalized observable claim.",
    ),
    source(
        "SRC-ZETA",
        "stable",
        "primary_paper",
        "Zeta function regularization of path integrals in curved spacetime",
        "https://doi.org/10.1007/BF01626516",
        "Supports analytic-continuation and determinant reservations without a physical effective-action result.",
    ),
    source(
        "SRC-TRACE-ANOMALY",
        "stable",
        "primary_paper",
        "Trace anomalies and the Hawking effect",
        "https://doi.org/10.1016/0550-3213(77)90410-2",
        "Supports curvature-invariant and scheme-dependence bookkeeping only.",
    ),
    source(
        "SRC-SCHWARZSCHILD-STATES",
        "stable",
        "primary_paper",
        "Vacuum polarization in Schwarzschild spacetime",
        "https://doi.org/10.1103/PhysRevD.21.2185",
        "Supports bounded state-selector, horizon, flux, and asymptotic-condition fixtures without measured radiation.",
    ),
    source(
        "SRC-PENROSE-LIMIT",
        "stable",
        "primary_manuscript",
        "Penrose limits and spacetime singularities",
        "https://arxiv.org/abs/hep-th/0312029",
        "Supports a null-geodesic scaling and profile-matrix contract without reconstruction or universality credit.",
    ),
    source(
        "SRC-MELVIN",
        "stable",
        "primary_paper",
        "Pure magnetic and electric geons",
        "https://doi.org/10.1103/PhysRev.139.B244",
        "Supports a magnetic-flux-tube metric and regular-axis ledger without an astrophysical field claim.",
    ),
    source(
        "SRC-NARIAI",
        "stable",
        "primary_paper",
        "On a new cosmological solution of Einstein's field equations of gravitation",
        "https://doi.org/10.1023/A:1026602724948",
        "Supports a product-spacetime and extremal-limit reservation without cosmological confirmation.",
    ),
    source(
        "SRC-DAFNY",
        "current",
        "official_tool_documentation",
        "Dafny Reference Manual",
        "https://dafny.org/latest/DafnyRef/DafnyRef",
        "Supports bounded contract and verification-condition fixtures, not deployed-software verification.",
    ),
    source(
        "SRC-WHY3",
        "current",
        "official_tool_documentation",
        "Why3 documentation",
        "https://why3.org/doc/",
        "Supports finite theories, transformations, drivers, and proof-session fixtures only.",
    ),
    source(
        "SRC-FRAMA-C",
        "current",
        "official_tool_documentation",
        "Frama-C publications and ACSL/WP manuals",
        "https://frama-c.com/html/publications.html",
        "Supports bounded ACSL and weakest-precondition fixtures without C-program assurance promotion.",
    ),
    source(
        "SRC-MAUDE",
        "current",
        "official_tool_documentation",
        "The Maude system manual",
        "https://maude.cs.illinois.edu/maude1/manual/maude-manual-html/maude-manual_61.html",
        "Supports finite equations, rewrite rules, and search fixtures only.",
    ),
    source(
        "SRC-K",
        "current",
        "official_project_documentation",
        "K Framework documentation",
        "https://kframework.org/docs/",
        "Supports bounded configuration, rewrite, and reachability fixtures without language-implementation certification.",
    ),
    source(
        "SRC-ISABELLE",
        "current",
        "official_tool_documentation",
        "Isabelle documentation",
        "https://isabelle.in.tum.de/documentation.html",
        "Supports a finite HOL theory and explicit unproved-goal refusal only.",
    ),
    source(
        "SRC-COMPCERT",
        "current",
        "official_tool_documentation",
        "CompCert user and reference manuals",
        "https://compcert.org/man/",
        "Supports a represented semantic-preservation handover; toolchain, source language, target, and external assumptions stay explicit.",
    ),
    source(
        "SRC-SAIL",
        "current",
        "official_project_repository",
        "Sail instruction-set architecture specification language",
        "https://github.com/rems-project/sail",
        "Supports a represented ISA-model fixture only; hardware, generated prover model, and implementation agreement remain gated.",
    ),
    source(
        "SRC-EAT",
        "current",
        "official_rfc",
        "RFC 9711 Entity Attestation Token",
        "https://www.rfc-editor.org/info/rfc9711/",
        "Supports synthetic claims, profiles, and submodules only, with no real device, key, verifier, or appraisal policy.",
    ),
    source(
        "SRC-ERS",
        "stable",
        "official_rfc",
        "RFC 4998 Evidence Record Syntax",
        "https://www.rfc-editor.org/info/rfc4998/",
        "Supports synthetic archive-timestamp and renewal structures without a real archive, signature, trust, or non-repudiation decision.",
    ),
    source(
        "SRC-JWS",
        "current",
        "official_rfc",
        "RFC 7797 JSON Web Signature Unencoded Payload Option",
        "https://www.rfc-editor.org/info/rfc7797/",
        "Supports synthetic header and signing-input vectors only, with no production key or interoperability event.",
    ),
    source(
        "SRC-KOA",
        "current",
        "official_data_portal",
        "Keck Observatory Archive User Guide",
        "https://koa.ipac.caltech.edu/UserGuide/",
        "Identifies an official archive boundary; x2 must make no query, download, ingest, calibration, fit, likelihood, posterior, or empirical claim.",
    ),
    source(
        "SRC-TE-TAURA-WHIRI",
        "current",
        "maori_language_authority_guidance",
        "Te Taura Whiri best-practice translation guidelines",
        "https://en.tetaurawhiri.govt.nz/translation-guidelines",
        "Reserves te reo Māori translation quality, provenance, and certified-language expertise to appropriate people and authorities.",
    ),
    source(
        "SRC-WCAG22",
        "current",
        "official_recommendation",
        "Web Content Accessibility Guidelines 2.2",
        "https://www.w3.org/TR/WCAG22/",
        "Supports structural accessibility reservations only; manual and affected-user evaluation remain open.",
    ),
    source(
        "SRC-MAORI-DATA",
        "current",
        "maori_authority_guidance",
        "Principles of Māori Data Sovereignty",
        "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
        "Keeps Māori data, language, interpretation, governance, and remedy with Māori authorities.",
    ),
]


def proposal(number, title, slug, pillar, disposition, source_ids, novelty):
    if disposition == "completed":
        approval = "safe_now_bounded_symbolic_or_software"
        lane = "x2_owner_local_synthetic"
        acceptance = (
            "Reject all five frozen mutations and emit only the declared "
            "symbolic, structural, or software contract."
        )
    elif disposition == "represented":
        approval = "candidate_bounded_proxy"
        lane = "x2_synthetic_proxy_only"
        acceptance = (
            "Reject all five frozen mutations and retain represented status "
            "with no operational, production, professional, privacy-complete, "
            "or authority credit."
        )
    elif disposition == "open_gap":
        approval = "candidate_real_data_and_independent_review_required"
        lane = "x2_zero_row_readiness_only"
        acceptance = (
            "Emit a zero-row refusal with no query, download, ingest, "
            "calibration, fit, likelihood, posterior, prediction, or empirical "
            "promotion."
        )
    else:
        approval = (
            "exact_affected_party_legal_cultural_accessibility_and_maori_"
            "authority_required"
        )
        lane = "x2_reservation_matrix_only"
        acceptance = (
            "Emit unresolved decision rights and reservations only; make no "
            "operational, legal, cultural, Māori-authority, affected-party, "
            "accessibility-complete, remedy, or governance decision."
        )
    return {
        "proposal_id": f"V6532-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar": pillar,
        "hypothesis": (
            f"A bounded {slug.replace('-', ' ')} contract can make its "
            "obligations machine-checkable without crossing a protected gate."
        ),
        "null_or_failure_condition": (
            "Any required field is absent, a frozen mutation passes, a failed "
            "witness is erased, or the artifact promotes beyond its evidence lane."
        ),
        "approval_class": approval,
        "execution_lane": lane,
        "official_or_primary_source_needs": source_ids,
        "concrete_artifacts": [
            f"surfaces/{slug}/contract.json",
            f"surfaces/{slug}/mutation-results.json",
            f"surfaces/{slug}/bounded-receipt.json",
        ],
        "falsifier_or_acceptance_gate": acceptance,
        "rollback_or_recovery": (
            "Stop the proposal, retain the failure with zero credit, rewrite no "
            "history, and leave external, sibling, participant, production, "
            "professional, legal, cultural, and authority state unchanged."
        ),
        "protected_gates": PROTECTED_GATES,
        "expected_disposition": disposition,
        "novelty_against_1450_frozen_proposals": novelty,
    }


PROPOSAL_SPECS = [
    ("GMUT Einstein-Langevin stochastic source, noise kernel, dissipation, influence action, metric perturbation, correlation, validity domain, and observation firewall", "einstein-langevin-noise-kernel", "GMUT Mind", "completed", ["SRC-EINSTEIN-LANGEVIN"], "No frozen row isolates the Einstein-Langevin stochastic source, noise kernel, dissipation, and validity-domain contract."),
    ("GMUT Mukhanov-Sasaki gauge-invariant scalar, conformal time, pump field, canonical mode, Wronskian normalization, power-spectrum reservation, and observation firewall", "mukhanov-sasaki-mode", "GMUT Mind", "completed", ["SRC-MUKHANOV-SASAKI"], "No frozen row isolates the Mukhanov-Sasaki canonical mode, pump field, Wronskian normalization, and spectrum reservation."),
    ("GMUT delta-N separate-universe initial flat slice, final uniform-density slice, e-fold derivative, field fluctuation, non-Gaussian coefficient, scale reservation, and observation firewall", "delta-n-separate-universe", "GMUT Mind", "completed", ["SRC-DELTA-N"], "No frozen row isolates delta-N slice selection, e-fold derivatives, and non-Gaussian coefficient obligations."),
    ("GMUT Kundt nonexpanding null congruence, shear, twist, affine coordinate, transverse metric, profile function, invariant subclass, and observation firewall", "kundt-null-congruence", "GMUT Mind", "completed", ["SRC-KUNDT"], "No frozen row isolates Kundt nonexpansion, transverse profile, affine chart, and invariant-subclass obligations."),
    ("GMUT Brinkmann-Rosen plane-wave coordinate map, transverse zweibein, profile matrix, polarization, geodesic deviation, caustic chart boundary, and observation firewall", "brinkmann-rosen-map", "GMUT Mind", "completed", ["SRC-BRINKMANN-ROSEN"], "No frozen row isolates the Brinkmann-Rosen zweibein map, profile relation, and caustic chart refusal."),
    ("GMUT Plebański-Demiański acceleration, rotation, NUT parameter, electric charge, magnetic charge, cosmological constant, root ordering, and observation firewall", "plebanski-demianski-roots", "GMUT Mind", "completed", ["SRC-PLEBANSKI-DEMIANSKI"], "No frozen row isolates the full Plebański-Demiański parameter and root-order contract."),
    ("GMUT Majumdar-Papapetrou conformastatic potential, extremal charge-mass balance, harmonic source, multicentre horizon, strut absence, coincidence boundary, and observation firewall", "majumdar-papapetrou-balance", "GMUT Mind", "completed", ["SRC-MAJUMDAR"], "No frozen row isolates conformastatic harmonic balance, multicentre horizons, and coincidence boundaries."),
    ("GMUT Eguchi-Hanson self-dual curvature, bolt, radial range, angular identification, asymptotic lens space, regularity, orientation, and observation firewall", "eguchi-hanson-bolt", "GMUT Mind", "completed", ["SRC-EGUCHI-HANSON"], "No frozen row isolates Eguchi-Hanson bolt regularity, angular identification, orientation, and asymptotic lens-space obligations."),
    ("GMUT Gödel universe rotating dust, cosmological constant, tetrad scale, homogeneity, chronology horizon, closed timelike curve, causal reservation, and observation firewall", "godel-chronology-ledger", "GMUT Mind", "completed", ["SRC-GODEL"], "No frozen row isolates Gödel rotating-dust parameters, chronology horizon, and closed-timelike-curve reservation."),
    ("GMUT C-metric accelerating black-hole roots, conformal factor, axis segments, conical deficit, acceleration horizon, coordinate patch, and observation firewall", "c-metric-axis-roots", "GMUT Mind", "completed", ["SRC-C-METRIC"], "No frozen row isolates C-metric root ordering, axis segments, conical deficit, and acceleration-horizon obligations."),
    ("GMUT adiabatic regularization WKB frequency, derivative order, mode subtraction, stress tensor, ultraviolet term, state dependence, truncation boundary, and observation firewall", "adiabatic-regularization", "GMUT Mind", "completed", ["SRC-ADIABATIC"], "No frozen row isolates adiabatic derivative order, WKB mode subtraction, state dependence, and truncation refusal."),
    ("GMUT spectral-zeta determinant eigenvalue spectrum, Mellin transform, analytic continuation, heat trace, renormalization scale, zero mode, phase reservation, and observation firewall", "spectral-zeta-determinant", "GMUT Mind", "completed", ["SRC-ZETA"], "No frozen row isolates spectral-zeta analytic continuation, determinant zero modes, scale, and phase reservations."),
    ("GMUT conformal trace anomaly curvature invariants, Euler density, Weyl square, total derivative, scheme dependence, stress-tensor trace, and observation firewall", "conformal-trace-anomaly", "GMUT Mind", "completed", ["SRC-TRACE-ANOMALY"], "No frozen row isolates trace-anomaly invariant decomposition, total-derivative ambiguity, and scheme dependence."),
    ("GMUT Schwarzschild Boulware, Hartle-Hawking, and Unruh quantum states, horizon regularity, flux direction, temperature, asymptotic condition, state selector, and observation firewall", "schwarzschild-quantum-states", "GMUT Mind", "completed", ["SRC-SCHWARZSCHILD-STATES"], "No frozen row isolates the three Schwarzschild quantum-state selectors, horizon regularity, flux, and asymptotic conditions."),
    ("GMUT Penrose plane-wave limit null geodesic, adapted coordinates, scaling map, profile matrix, affine parameter, conjugate point, reconstruction boundary, and observation firewall", "penrose-plane-wave-limit", "GMUT Mind", "completed", ["SRC-PENROSE-LIMIT"], "No frozen row isolates the Penrose scaling map, profile matrix, conjugate-point domain, and reconstruction refusal."),
    ("GMUT Melvin magnetic universe flux tube, axial field, conformal factor, field strength, regular axis, radial circumference, asymptotic reservation, and observation firewall", "melvin-magnetic-universe", "GMUT Mind", "completed", ["SRC-MELVIN"], "No frozen row isolates Melvin flux-tube field strength, conformal factor, axis regularity, and asymptotic reservation."),
    ("GMUT Nariai product spacetime two-sphere radius, two-dimensional de Sitter factor, cosmological constant, horizon pair, perturbation mode, extremal-limit reservation, and observation firewall", "nariai-product-spacetime", "GMUT Mind", "completed", ["SRC-NARIAI"], "No frozen row isolates Nariai product factors, horizon pair, perturbation mode, and extremal-limit boundary."),
    ("THOS Dafny method contract, precondition, postcondition, loop invariant, decreases clause, frame condition, ghost state, counterexample, and nonpromotion board", "dafny-method-contract", "THOS Body", "completed", ["SRC-DAFNY"], "No frozen row isolates Dafny decreases, framing, ghost state, and counterexample obligations."),
    ("THOS Why3 theory, logic declaration, program contract, verification condition, transformation, prover driver, proof session, unknown result, and nonpromotion board", "why3-proof-session", "THOS Body", "completed", ["SRC-WHY3"], "No frozen row isolates Why3 transformations, prover drivers, proof sessions, and unknown-result refusal."),
    ("THOS Frama-C ACSL and WP function contract, assigns clause, loop invariant, memory model, weakest precondition, prover result, alarm, and nonpromotion board", "frama-c-acsl-wp", "THOS Body", "completed", ["SRC-FRAMA-C"], "No frozen row isolates ACSL assigns, WP memory models, prover results, and alarm obligations."),
    ("THOS Maude rewriting-logic module, equation, rewrite rule, membership, strategy boundary, search state, reachability claim, and nonpromotion board", "maude-rewriting-logic", "THOS Body", "completed", ["SRC-MAUDE"], "No frozen row isolates Maude equations, membership, rewrite search, and reachability-claim boundaries."),
    ("THOS K Framework configuration, cell, rewrite rule, strictness, reachability claim, symbolic execution, side condition, backend boundary, and nonpromotion board", "k-framework-reachability", "THOS Body", "completed", ["SRC-K"], "No frozen row isolates K cells, strictness, reachability rules, symbolic side conditions, and backend boundaries."),
    ("THOS Isabelle/HOL theory, locale, definition, lemma, proof context, simplifier rule, code equation, unproved-goal refusal, and nonpromotion board", "isabelle-hol-theory", "THOS Body", "completed", ["SRC-ISABELLE"], "No frozen row isolates Isabelle locales, proof contexts, simplifier rules, code equations, and unproved-goal refusal."),
    ("THOS CompCert source program, verified compiler pass, semantic preservation theorem, target assembly, external assumption, unsupported construct, and professional-review proxy", "compcert-preservation-proxy", "THOS Body", "represented", ["SRC-COMPCERT"], "No frozen row isolates a CompCert pass-and-assumption handover while retaining represented professional-review status."),
    ("THOS Sail ISA specification, bitvector type, instruction clause, decode pattern, execution effect, generated prover model, implementation gap, and professional-review proxy", "sail-isa-proxy", "THOS Body", "represented", ["SRC-SAIL"], "No frozen row isolates Sail decode and execution clauses, generated-model scope, and implementation-gap reservations."),
    ("Freed ID Entity Attestation Token claim, profile, submodule, nonce, freshness, verifier policy, detached appraisal, and nonproduction profile", "eat-claim-profile", "Freed ID/CBR Heart", "represented", ["SRC-EAT"], "No frozen row isolates RFC 9711 EAT profiles, submodules, freshness, and detached-appraisal boundaries."),
    ("Freed ID RFC 4998 Evidence Record Syntax archive timestamp, digest algorithm, reduced hash tree, archive-time-stamp sequence, renewal, validation data, and nonproduction profile", "ers-archive-timestamp", "Freed ID/CBR Heart", "represented", ["SRC-ERS"], "No frozen row isolates Evidence Record Syntax reduced hash trees, timestamp chains, renewal, and validation-data obligations."),
    ("Freed ID JWS unencoded payload protected header, b64 false parameter, critical list, signing input, payload octet, detached transport, verification refusal, and nonproduction profile", "jws-unencoded-payload", "Freed ID/CBR Heart", "represented", ["SRC-JWS"], "No frozen row isolates RFC 7797 b64=false critical-header, octet signing-input, and detached-payload refusal obligations."),
    ("GMUT Keck Observatory Archive KOAID, instrument mode, observing night, exposure duration, spectral format, calibration association, proprietary-release boundary, and zero-row likelihood-refusal adapter", "keck-archive-zero-row", "GMUT Mind", "open_gap", ["SRC-KOA"], "No frozen row isolates the Keck KOAID, observing-night, spectral-format, calibration-association, and proprietary-release zero-row contract."),
    ("CBR formal-assurance report te reo Māori terminology, mathematical notation, screen-reader wording, dialect and iwi usage, translator provenance, community review, correction, withdrawal, affected-user evaluation, and Māori-language-authority reservation", "maori-assurance-report-authority", "Freed ID/CBR Heart", "exact_gate", ["SRC-TE-TAURA-WHIRI", "SRC-WCAG22", "SRC-MAORI-DATA"], "No frozen row isolates te reo Māori formal-assurance terminology, mathematical and screen-reader wording, translator provenance, correction, withdrawal, affected-user evaluation, and Māori-language authority."),
]


PROPOSALS = [
    proposal(index, *spec)
    for index, spec in enumerate(PROPOSAL_SPECS, 1)
]

MUTATION_KINDS = [
    "drop_required_field",
    "cross_bind_source_or_identifier",
    "invert_or_weaken_boundary",
    "inject_unsupported_promotion",
    "erase_failure_or_rollback",
]

SAFE_NOW_TASKS = [
    f"Execute the bounded contract, five frozen mutations, and receipt for {row['proposal_id']} without crossing {row['execution_lane']}."
    for row in PROPOSALS
]
SAFE_TASKS = SAFE_NOW_TASKS

CANDIDATE_TASKS = [
    f"Prepare a nonpromotional extension plan for {row['proposal_id']} without crossing {row['execution_lane']}."
    for row in PROPOSALS
]

SKILL_TASKS = [
    f"Build phase-local review skill {index:02d} for {row['slug']} with an explicit nonpromotion boundary."
    for index, row in enumerate(PROPOSALS[:10], 1)
]

SKILL_IDEAS = [
    (
        f"ghc-family-v653-v2-{row['slug']}-review",
        f"Review {row['slug']} contracts, mutation evidence, and nonpromotion boundaries.",
    )
    for row in PROPOSALS[:10]
]

RUNNER_TASKS = [
    f"Build and invoke family-compatible bounded runner {index:02d} for {row['slug']}."
    for index, row in enumerate(PROPOSALS[:10], 1)
]

RUNNER_IDEAS = [
    (f"ghc_family_v653_v2_runner_{index:02d}.py", row["slug"])
    for index, row in enumerate(PROPOSALS[:10], 1)
]

CLEAN_FIX_REFINE_TASKS = [
    f"REFINE-{index:02d}: review {row['slug']} terminology, falsifier, rollback, and protected-gate wording without changing its frozen outcome class."
    for index, row in enumerate(PROPOSALS, 1)
]

X1_NEGATIVES = [
    ("V6532-X1-N01", "login_shell_baton_metadata_timeout", "The first login-shell baton metadata and read probe timed out without usable output.", "Use non-login PowerShell with exact literal paths, file APIs, and bounded numbered chunks through EOF."),
    ("V6532-X1-N02", "login_shell_get_item_timeout", "A second login-shell Get-Item probe also timed out without usable output.", "Keep later filesystem reads non-login and bounded, and verify the final line explicitly."),
    ("V6532-X1-N03", "thread_list_limit_200_schema_error", "A task-list call assumed an unsupported limit argument of 200 and was rejected.", "Inspect the callable schema and invoke the task-list tool with its supported empty request."),
    ("V6532-X1-N04", "thread_list_limit_100_schema_error", "A second task-list call repeated the unsupported limit assumption with 100 and was rejected.", "Promote the schema-inspected empty request and do not replay unsupported pagination arguments."),
    ("V6532-X1-N05", "powershell_backslash_regex_error", "A candidate-registration probe treated a lone backslash as a regular expression and failed before proving uniqueness.", "Use literal string replacement for path normalization and exact branch-path tuple comparison."),
    ("V6532-X1-N06", "whole_worktree_inventory_display_truncation", "The first whole 207-worktree display was truncated and earned no complete inventory-review credit.", "Use a bounded programmatic inventory that reports counts, duplicates, missing paths, locked or prunable rows, and named-owner rows."),
    ("V6532-X1-N07", "post_worktree_combined_audit_timeout", "A broad combined audit after the 51,008-file checkout timed out and earned no clean-state credit.", "Audit the exact path, registration, branch, head, lock and process state separately, then use bounded tracked, staged, and untracked clean probes."),
    ("V6532-X1-N08", "powershell_hashset_overload_and_timeout", "The first semantic Jaccard audit used an invalid HashSet constructor, emitted repeated overload errors, and timed out.", "Use the builder-matching token function in a bounded read-only Python audit and print only the nearest row per proposal."),
    ("V6532-X1-N09", "frozen_index_proposals_key_assumption", "A frozen-index probe assumed a proposals key and attempted to slice a dictionary, raising KeyError.", "Inspect top-level key names and value types before indexing the frozen-chain schema."),
    ("V6532-X1-N10", "frozen_index_items_assumption", "A follow-up probe assumed proposal arrays were dictionaries and called items, raising AttributeError.", "Use the confirmed list schema and bounded numeric indexing before running the successful novelty audit."),
    ("V6532-X1-N11", "source_final_receipt_filename_assumption", "A source-receipt probe assumed a final-validation-record filename that does not exist and stopped before the intended bounded inventory completed.", "Discover exact lifecycle filenames with rg --files, then read only the confirmed final-validation protocol and manifest paths."),
    ("V6532-X1-N12", "source_evidence_manifest_filename_recurrence", "A later source-manifest probe again guessed an evidence-staged-manifest filename and stopped after one successful read.", "Promote exact rg --files discovery as a recurrence guard, then read evidence-candidate-manifest and the other confirmed paths only."),
    ("V6532-X1-N13", "workflow_messaging_enum_mismatch", "The first workflow refinement used a route-specific codex_route string instead of the schema's exact existing_task_only_after_terminal_gate enum and returned needs_refinement.", "Use the exact schema enum for messaging while retaining the exact Ilyra Fen title and one-send constraint in the terminal successor and live-overlay fields."),
    ("V6532-X1-N14", "combined_probe_exit_misattribution", "A combined staged review labeled the final no-hit git-grep exit code as the earlier git-diff-check exit code and falsely displayed DiffCheckExit 1.", "Capture each command exit immediately in its own variable and treat git-grep exit 1 as the expected no-match state rather than a diff failure."),
]

REJECTED_COLLISIONS = [
    "OAuth Device Authorization was rejected because frozen row V6503-P06 already covers the same RFC 8628 device-code, user-code, verification-URI, polling, expiry, and abuse mechanism.",
    "ACME Renewal Information was rejected because frozen row V6521-P21 already covers the same certificate identifier, suggested window, retry, fallback, and replacement mechanism.",
    "Cartan-Karlhede, GHP, Raychaudhuri, Bondi-Sachs, Iyer-Wald, Einstein-Cartan, BSSN, Ashtekar-Barbero, Bel-Robinson, GHY, Brown-York, Isaacson, Horndeski, Vainshtein, DHOST, and Galileon were rejected after exact frozen-mechanism review.",
    "TLA+, Promela, Petri nets, CSP, CRDT, UPPAAL, PRISM, Event-B, Alloy, ioco, mCRL2, NuSMV, Z, VDM, LOTOS, and CEGAR were rejected where frozen formal-method rows already exist.",
    "HPKE, OHTTP, CWT, RATS, SD-JWT, MLS, Privacy Pass, OPAQUE, VOPRF, ML-KEM, SCRAM, Kerberos FAST, and X.509 proxy certificates were rejected where frozen identity or cryptographic mechanisms already exist.",
    "DESI, Euclid, LHAASO, IceCube, CHIME/FRB, Rubin, LoTSS, EHT, Suzaku, MeerKAT, Hubble, and MAST were rejected where frozen zero-row adapters already cover those archives or facilities.",
]
