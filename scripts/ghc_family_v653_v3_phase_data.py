#!/usr/bin/env python3
"""Frozen Ilyra Fen v653-v3 x1 data.

This module contains preregistration inputs only. It deliberately contains no
x2 observations, mutation outcomes, completion receipts, or route result.
"""

from __future__ import annotations


PHASE = "v653-v3"
PHASE_ID = "v653-gmut-thos-v3-x1-x2"
OWNER = "Ilyra Fen"
PRONOUNS = "she/they"
ROLE = "relational evidence-boundary steward"
HOPE = "leave every claim traceable and every gate unmistakable"
PHASE_ROOT = "docs/ilyra-fen/v653-v3"
BRANCH = "codex/GHC-Family/ilyra-fen-v653-v3-full-tools"

SOURCE_BRANCH = "codex/GHC-Family/lyren-moss-v653-v2-full-tools"
SOURCE_PARENT = "97989717f8447ef2fa09a37a92c76617dea30874"
SOURCE_X1 = "90cc4cff205fef8b7fe0fb1218083e9ced14f146"
SOURCE_EVIDENCE = "6728c0e6d2a5b16a56f08b80e60fdbfe36818427"
SOURCE_HEAD = "c25e70eaae7c338a22ee64270ab574768835b227"

PRIOR_FROZEN = 1480
INHERITED_NEGATIVES = 9608
INHERITED_OPEN_GAPS = 71
INHERITED_EXACT_GATES = 72
INHERITED_METHOD_FLOW_FAILED = 17
INHERITED_METHOD_FLOW_PASSING = 17
PRIMARY_FOCUS = "THOS Body"
BOUNDED_PRACTICE = (
    "safety-critical software assurance, counterexample triage, proof review, "
    "rollback, and release handover"
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
        "SRC-STUECKELBERG-PETERMANN",
        "stable",
        "primary_review",
        "Perturbative algebraic quantum field theory and the renormalization groups",
        "https://arxiv.org/abs/0901.2038",
        "Supports a finite-renormalization group contract without a physical parameter, prediction, or empirical claim.",
    ),
    source(
        "SRC-DIMREG",
        "stable",
        "primary_paper",
        "Regularization and renormalization of gauge fields",
        "https://doi.org/10.1016/0550-3213(72)90279-9",
        "Supports dimension, pole, scale, and scheme bookkeeping without validating a physical model.",
    ),
    source(
        "SRC-KINOSHITA",
        "stable",
        "primary_paper",
        "Mass singularities of Feynman amplitudes",
        "https://doi.org/10.1063/1.1703797",
        "Supports a degenerate-state cancellation obligation without an inclusive-rate calculation.",
    ),
    source(
        "SRC-LEE-NAUENBERG",
        "stable",
        "primary_paper",
        "Degenerate systems and mass singularities",
        "https://doi.org/10.1103/PhysRev.133.B1549",
        "Supports initial and final degeneracy bookkeeping without an empirical cross section.",
    ),
    source(
        "SRC-BLOCH-NORDSIECK",
        "stable",
        "primary_paper",
        "Note on the radiation field of the electron",
        "https://doi.org/10.1103/PhysRev.52.54",
        "Supports soft-emission exponentiation obligations without a measured spectrum.",
    ),
    source(
        "SRC-SYMANZIK",
        "stable",
        "primary_paper",
        "Continuum limit and improved action in lattice theories",
        "https://doi.org/10.1016/0550-3213(83)90468-6",
        "Supports an irrelevant-operator and lattice-spacing ledger without continuum or numerical evidence.",
    ),
    source(
        "SRC-HAAG",
        "stable",
        "primary_review",
        "Haag's theorem in renormalised quantum field theories",
        "https://arxiv.org/abs/1602.00662",
        "Supports an interaction-picture assumption firewall without proving a new theorem.",
    ),
    source(
        "SRC-COLEMAN-WEINBERG",
        "stable",
        "primary_paper",
        "Radiative corrections as the origin of spontaneous symmetry breaking",
        "https://doi.org/10.1103/PhysRevD.7.1888",
        "Supports scale, gauge, loop-order, and extremum obligations without a physical vacuum claim.",
    ),
    source(
        "SRC-PAULI-JORDAN",
        "stable",
        "primary_reference",
        "The Quantum Theory of Fields, Volume I: Foundations",
        "https://doi.org/10.1017/CBO9781139644167",
        "Supports a commutator-distribution and causal-support ledger without a measured propagator.",
    ),
    source(
        "SRC-GELL-MANN-LOW",
        "stable",
        "primary_paper",
        "Bound states in quantum field theory",
        "https://doi.org/10.1103/PhysRev.84.350",
        "Supports an adiabatic switching and vacuum-normalization contract without a physical S-matrix result.",
    ),
    source(
        "SRC-RENORMALON",
        "stable",
        "primary_review",
        "Renormalons",
        "https://arxiv.org/abs/hep-ph/9807443",
        "Supports Borel-plane ambiguity and power-correction bookkeeping without a resummation or observable.",
    ),
    source(
        "SRC-DE-DONDER-WEYL",
        "stable",
        "primary_review",
        "On field theoretic generalizations of a Poisson algebra",
        "https://arxiv.org/abs/hep-th/9903225",
        "Supports covariant polymomentum and multisymplectic obligations without a physical field solution.",
    ),
    source(
        "SRC-LUSCHER",
        "stable",
        "primary_paper",
        "Volume dependence of the energy spectrum in massive quantum field theories",
        "https://doi.org/10.1007/BF01211589",
        "Supports finite-volume quantization and elastic-domain reservations without a lattice measurement.",
    ),
    source(
        "SRC-LEAN",
        "current",
        "official_documentation",
        "The Lean Language Reference",
        "https://lean-lang.org/doc/reference/latest/",
        "Supports elaborator, kernel, declaration, and trust-boundary fixtures only.",
    ),
    source(
        "SRC-AGDA",
        "current",
        "official_documentation",
        "Agda termination checking",
        "https://agda.readthedocs.io/en/stable/language/termination-checking.html",
        "Supports termination, positivity, postulate, and trust-boundary fixtures only.",
    ),
    source(
        "SRC-FSTAR",
        "current",
        "official_documentation",
        "Proof-Oriented Programming in F*",
        "https://fstar-lang.org/tutorial/book/intro.html",
        "Supports effects, preconditions, postconditions, weakest-precondition, SMT, and extraction boundaries only.",
    ),
    source(
        "SRC-SPARK",
        "current",
        "official_documentation",
        "Introduction to SPARK flow analysis",
        "https://learn.adacore.com/courses/intro-to-spark/chapters/02_Flow_Analysis.html",
        "Supports flow, contract, proof-level, and unproved-obligation fixtures only.",
    ),
    source(
        "SRC-CBMC",
        "current",
        "official_documentation",
        "CBMC training material",
        "https://model-checking.github.io/cbmc-training/",
        "Supports bounded unwinding, assertion, and counterexample obligations only.",
    ),
    source(
        "SRC-SEAHORN",
        "current",
        "official_documentation",
        "SeaHorn verification framework",
        "https://seahorn.github.io/",
        "Supports LLVM and constrained-Horn-clause boundary fixtures only.",
    ),
    source(
        "SRC-ALIVE2",
        "current",
        "official_repository",
        "Alive2 LLVM translation validation",
        "https://github.com/AliveToolkit/alive2",
        "Supports source-target refinement and counterexample obligations without compiler certification.",
    ),
    source(
        "SRC-SAW",
        "current",
        "official_documentation",
        "Software Analysis Workbench introduction",
        "https://saw.galois.com/intro/",
        "Supports Cryptol, symbolic-execution, equivalence, and solver-boundary fixtures only.",
    ),
    source(
        "SRC-BOOGIE",
        "current",
        "official_repository",
        "Boogie intermediate verification language",
        "https://github.com/boogie-org/boogie",
        "Supports procedure-contract, verification-condition, and solver-result fixtures only.",
    ),
    source(
        "SRC-VIPER",
        "current",
        "official_research_site",
        "Viper verification infrastructure",
        "https://www.pm.inf.ethz.ch/research/viper.html",
        "Supports permission, heap, inhale, exhale, and backend-boundary fixtures only.",
    ),
    source(
        "SRC-LIQUID-HASKELL",
        "current",
        "official_documentation",
        "LiquidHaskell specifications",
        "https://ucsd-progsys.github.io/liquidhaskell/specifications/",
        "Supports refinement, measure, qualifier, termination, and solver-boundary fixtures only.",
    ),
    source(
        "SRC-ASPA-PROFILE",
        "draft",
        "official_active_draft",
        "A Profile for Autonomous System Provider Authorization",
        "https://datatracker.ietf.org/doc/html/draft-ietf-sidrops-aspa-profile",
        "Supports a draft-only object-profile proxy; draft status forbids production or interoperability credit.",
    ),
    source(
        "SRC-ASPA-VERIFY",
        "draft",
        "official_active_draft",
        "BGP AS_PATH Verification Based on Autonomous System Provider Authorization Objects",
        "https://datatracker.ietf.org/doc/draft-ietf-sidrops-aspa-verification/",
        "Supports a draft path-verification proxy with no live routing or operator evidence.",
    ),
    source(
        "SRC-ACME-STAR",
        "stable",
        "official_standard",
        "RFC 8739: Support for Short-Term, Automatically Renewed Certificates in ACME",
        "https://www.rfc-editor.org/rfc/rfc8739.html",
        "Supports a synthetic STAR lifecycle proxy without keys, accounts, issuance, or network exchange.",
    ),
    source(
        "SRC-SUIT",
        "stable",
        "official_standard",
        "RFC 9124: A Manifest Information Model for Firmware Updates in IoT Devices",
        "https://www.rfc-editor.org/rfc/rfc9124.html",
        "Supports a synthetic information-model proxy without firmware, device, signature, or deployment evidence.",
    ),
    source(
        "SRC-SEL4",
        "current",
        "official_project_evidence",
        "seL4 proofs and assumptions",
        "https://sel4.systems/Verification/assumptions.html",
        "Supports a proof-artifact and assumption-boundary proxy without independent professional review.",
    ),
    source(
        "SRC-MISRA",
        "current",
        "official_guidance",
        "MISRA Compliance:2020",
        "https://www.misra.org.uk/app/uploads/2021/06/MISRA-Compliance-2020.pdf",
        "Supports a compliance, deviation, and review-evidence proxy without professional certification.",
    ),
    source(
        "SRC-ATLAS",
        "current",
        "official_data_documentation",
        "ATLAS Open Data research datasets",
        "https://opendata.atlas.cern/docs/data/for_research/evgen_data",
        "Supports a zero-row schema and refusal adapter only; no data are queried, downloaded, or analyzed.",
    ),
    source(
        "SRC-ATLAS-SYSTEMATICS",
        "current",
        "official_data_documentation",
        "ATLAS Open Data systematics documentation",
        "https://opendata.atlas.cern/docs/documentation/systematics",
        "Supports nuisance and systematic-obligation fields without a likelihood or physical constraint.",
    ),
    source(
        "SRC-FAA-SOFTWARE",
        "current",
        "official_regulator_guidance",
        "FAA airborne software and airworthiness guidance",
        "https://www.faa.gov/aircraft/air_cert/design_approvals/air_software/software_regs",
        "Supports explicit professional and regulatory reservation; it confers no approval or qualification.",
    ),
    source(
        "SRC-WCAG22",
        "stable",
        "official_standard",
        "Web Content Accessibility Guidelines 2.2",
        "https://www.w3.org/TR/WCAG22/",
        "Supports structural accessibility fields while manual and affected-user evaluation remain reserved.",
    ),
    source(
        "SRC-MAORI-DATA",
        "current",
        "maori_authority_principles",
        "Principles of Māori Data Sovereignty",
        "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
        "Requires Māori authority and data-governance decisions to remain outside repository software.",
    ),
    source(
        "SRC-TE-TAURA-WHIRI",
        "current",
        "official_language_guidance",
        "Te Taura Whiri translation guidelines",
        "https://en.tetaurawhiri.govt.nz/translation-guidelines",
        "Supports a language-authority reservation without claiming translator or community approval.",
    ),
]


def proposal(number, title, slug, pillar, disposition, source_ids, novelty):
    if disposition == "completed":
        approval = "safe_now_bounded_symbolic_or_software"
        lane = "x2_owner_local_synthetic"
        acceptance = (
            "Reject all five frozen mutations and emit only the declared "
            "symbolic, structural, or owner-local software contract."
        )
    elif disposition == "represented":
        approval = "candidate_bounded_proxy"
        lane = "x2_synthetic_proxy_only"
        acceptance = (
            "Reject all five frozen mutations and retain represented status "
            "with no operational, production, professional, privacy-complete, "
            "interoperability, or authority credit."
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
            "exact_affected_party_professional_legal_cultural_accessibility_"
            "and_maori_authority_required"
        )
        lane = "x2_reservation_matrix_only"
        acceptance = (
            "Emit unresolved decision rights and reservations only; make no "
            "operational, professional, legal, cultural, Māori-authority, "
            "affected-party, accessibility-complete, remedy, or governance decision."
        )
    return {
        "proposal_id": f"V6533-P{number:02d}",
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
        "novelty_against_1480_frozen_proposals": novelty,
    }


PROPOSAL_SPECS = [
    ("GMUT Stueckelberg-Petermann finite-renormalization map, local counterterm, composition law, scale, scheme, field redefinition, causal support, and observation firewall", "stueckelberg-petermann-finite-renormalization", "GMUT Mind", "completed", ["SRC-STUECKELBERG-PETERMANN"], "Distinct from inherited causal-factorization rows because this surface isolates the finite-renormalization group action and counterterm composition law."),
    ("GMUT dimensional-regularization continuation dimension, epsilon pole, mass scale, tensor continuation, gamma-matrix reservation, subtraction scheme, limit order, and observation firewall", "dimensional-regularization-contract", "GMUT Mind", "completed", ["SRC-DIMREG"], "Distinct from inherited cutoff and regulator rows because it isolates complex-dimension continuation, pole structure, and scheme-dependent limit order."),
    ("GMUT Kinoshita-Lee-Nauenberg degenerate initial and final state, inclusive sum, mass singularity, regulator cancellation, resolution criterion, perturbative order, and observation firewall", "kln-degenerate-state-cancellation", "GMUT Mind", "completed", ["SRC-KINOSHITA", "SRC-LEE-NAUENBERG"], "Distinct from inherited regulator rows because it isolates inclusive cancellation across both initial and final degenerate-state sums."),
    ("GMUT Bloch-Nordsieck soft-emission exponentiation, infrared resolution, virtual-real cancellation, charge trajectory, energy cutoff, inclusive probability, and observation firewall", "bloch-nordsieck-exponentiation", "GMUT Mind", "completed", ["SRC-BLOCH-NORDSIECK"], "Distinct from inherited Weinberg soft-factor rows because it isolates all-orders soft-photon exponentiation and inclusive resolution."),
    ("GMUT Symanzik lattice effective action, lattice spacing, irrelevant operator, improvement coefficient, symmetry, continuum extrapolation, truncation order, and observation firewall", "symanzik-lattice-improvement", "GMUT Mind", "completed", ["SRC-SYMANZIK"], "Distinct from inherited lattice and effective-action rows because it isolates cutoff-error operator improvement by powers of lattice spacing."),
    ("GMUT Haag interaction-picture theorem assumptions, unitary equivalence, vacuum, representation, equal-time field, domain, renormalized-theory reservation, and observation firewall", "haag-interaction-picture-theorem", "GMUT Mind", "completed", ["SRC-HAAG"], "Distinct from inherited Haag-Kastler and scattering rows because it isolates the interaction-picture unitary-equivalence obstruction and its assumptions."),
    ("GMUT Coleman-Weinberg effective potential, loop order, renormalization scale, gauge dependence, extremum condition, stability reservation, field domain, and observation firewall", "coleman-weinberg-effective-potential", "GMUT Mind", "completed", ["SRC-COLEMAN-WEINBERG"], "Distinct from inherited spontaneous-symmetry and gauge-fixing rows because it isolates radiative extrema, scale choice, and gauge-dependent potential obligations."),
    ("GMUT Pauli-Jordan commutator distribution, causal support, mass shell, sign convention, equal-time condition, spacelike vanishing, distributional test function, and observation firewall", "pauli-jordan-commutator-distribution", "GMUT Mind", "completed", ["SRC-PAULI-JORDAN"], "Distinct from inherited propagator and microcausality rows because it isolates the causal commutator distribution and equal-time normalization as one typed contract."),
    ("GMUT Gell-Mann-Low adiabatic switching, vacuum overlap, time ordering, normalization denominator, switching limit, degeneracy reservation, asymptotic boundary, and observation firewall", "gell-mann-low-adiabatic-switching", "GMUT Mind", "completed", ["SRC-GELL-MANN-LOW"], "Distinct from inherited Bogoliubov local-S-matrix rows because it isolates the normalized adiabatic switching quotient and vacuum-overlap refusal."),
    ("GMUT renormalon Borel-plane singularity, factorial growth, ambiguity prescription, operator-power correction, scale, ultraviolet-infrared class, scheme dependence, and observation firewall", "renormalon-borel-singularity", "GMUT Mind", "completed", ["SRC-RENORMALON"], "Distinct from inherited Borel-Ecalle resurgence rows because it isolates renormalon pole classes and their operator-power ambiguity bookkeeping."),
    ("GMUT De Donder-Weyl covariant Hamiltonian, polymomentum, multisymplectic form, Hamilton-Jacobi equation, Legendre map, degeneracy, spacetime covariance, and observation firewall", "de-donder-weyl-covariant-hamiltonian", "GMUT Mind", "completed", ["SRC-DE-DONDER-WEYL"], "Distinct from inherited hypersurface Hamilton-Jacobi rows because it isolates covariant polymomenta, multisymplectic structure, and the field-theoretic Legendre map."),
    ("GMUT Luescher finite-volume quantization, box size, two-particle energy, phase shift, partial wave, elastic domain, exponential correction, and observation firewall", "luscher-finite-volume-quantization", "GMUT Mind", "completed", ["SRC-LUSCHER"], "Distinct from inherited finite-volume and lattice rows because it isolates two-body level-to-phase-shift quantization with explicit elastic-domain refusal."),
    ("THOS Lean 4 parser, elaborator, metavariable, declaration environment, kernel proof term, trusted code base, axiom inventory, and nonpromotion board", "lean4-elaborator-kernel-boundary", "THOS Body", "completed", ["SRC-LEAN"], "No frozen row isolates Lean 4 elaboration from kernel checking while retaining explicit axiom and trusted-code boundaries."),
    ("THOS Agda termination checker, positivity checker, sized type, postulate, rewrite rule, unsafe option, coverage, and nonpromotion board", "agda-termination-positivity-boundary", "THOS Body", "completed", ["SRC-AGDA"], "No frozen row isolates Agda termination, positivity, postulate, rewrite, and unsafe-option obligations."),
    ("THOS F-star effect, precondition, postcondition, weakest precondition, SMT query, admitted fact, extraction boundary, and nonpromotion board", "fstar-effect-wp-boundary", "THOS Body", "completed", ["SRC-FSTAR"], "No frozen row isolates F* effectful weakest-precondition generation, admitted facts, SMT reliance, and extraction scope."),
    ("THOS SPARK Ada data flow, dependency contract, initialization, run-time check, proof level, unproved obligation, review boundary, and nonpromotion board", "spark-ada-flow-proof-level", "THOS Body", "completed", ["SRC-SPARK"], "No frozen row isolates SPARK flow analysis, proof levels, run-time checks, and unproved-obligation handover."),
    ("THOS CBMC unwinding bound, assertion, assumption, memory model, nondeterminism, solver result, unwinding assertion, and nonpromotion board", "cbmc-bounded-unwinding-contract", "THOS Body", "completed", ["SRC-CBMC"], "No frozen row isolates CBMC bounded completeness, unwinding assertions, nondeterminism, and solver-result scope."),
    ("THOS SeaHorn LLVM translation, constrained Horn clause, invariant, memory abstraction, solver result, counterexample, unsupported instruction, and nonpromotion board", "seahorn-chc-llvm-boundary", "THOS Body", "completed", ["SRC-SEAHORN"], "No frozen row isolates SeaHorn LLVM-to-CHC translation, invariant scope, memory abstraction, and unsupported-instruction refusal."),
    ("THOS Alive2 source and target LLVM, refinement relation, undefined behavior, poison, memory model, timeout, counterexample, and nonpromotion board", "alive2-llvm-refinement-boundary", "THOS Body", "completed", ["SRC-ALIVE2"], "No frozen row isolates Alive2 translation-validation refinement, poison and undefined behavior, timeout, and counterexample obligations."),
    ("THOS SAW Cryptol specification, symbolic execution, override, proof script, solver backend, equivalence claim, uninterpreted boundary, and nonpromotion board", "saw-cryptol-symbolic-equivalence", "THOS Body", "completed", ["SRC-SAW"], "No frozen row isolates SAW and Cryptol symbolic equivalence, override, solver, and uninterpreted-boundary obligations."),
    ("THOS Boogie procedure, requires, ensures, modifies, invariant, verification condition, solver outcome, counterexample, and nonpromotion board", "boogie-ivl-verification-condition", "THOS Body", "completed", ["SRC-BOOGIE"], "No frozen row isolates Boogie intermediate-language procedure contracts and generated verification-condition outcomes."),
    ("THOS Viper permission, heap location, inhale, exhale, fold, unfold, backend result, counterexample, and nonpromotion board", "viper-permission-logic-boundary", "THOS Body", "completed", ["SRC-VIPER"], "No frozen row isolates Viper permission accounting, inhale-exhale semantics, predicate folding, and backend-result boundaries."),
    ("THOS LiquidHaskell refinement, measure, qualifier, termination metric, SMT theory, proof combinator, unchecked escape, and nonpromotion board", "liquidhaskell-refinement-boundary", "THOS Body", "completed", ["SRC-LIQUID-HASKELL"], "No frozen row isolates LiquidHaskell refinement measures, qualifier inference, termination, SMT scope, and unchecked escapes."),
    ("Freed ID draft RPKI ASPA customer-provider object, provider set, AFI limit, signature chain, path verification, unknown state, draft status, and nonproduction profile", "rpki-aspa-draft-profile", "Freed ID/CBR Heart", "represented", ["SRC-ASPA-PROFILE", "SRC-ASPA-VERIFY"], "Distinct from inherited RPKI origin-validation rows because it isolates draft ASPA provider authorization and AS_PATH verification states."),
    ("Freed ID ACME STAR short-term certificate, recurrent order, delegation, validity window, cancellation, renewal, account binding, and nonproduction profile", "acme-star-renewal-profile", "Freed ID/CBR Heart", "represented", ["SRC-ACME-STAR"], "Distinct from inherited base ACME and renewal-information rows because it isolates RFC 8739 recurrent short-term certificate delegation and cancellation."),
    ("Freed ID SUIT manifest component identifier, dependency resolution, digest, sequence number, condition, directive, severable field, and nonproduction profile", "suit-manifest-information-model", "Freed ID/CBR Heart", "represented", ["SRC-SUIT"], "No frozen row isolates the SUIT information model's component, condition, directive, dependency, and severability obligations."),
    ("THOS seL4 proof artifact, theorem scope, C refinement, binary assumption, trusted toolchain, configuration, omitted property, and professional-review proxy", "sel4-proof-assumption-proxy", "THOS Body", "represented", ["SRC-SEL4"], "No frozen row isolates seL4 proof-scope and assumption handover as a represented professional-review proxy."),
    ("THOS MISRA C guideline category, compliance plan, deviation permit, enforcement method, evidence record, tool qualification, reviewer role, and professional-review proxy", "misra-c-compliance-proxy", "THOS Body", "represented", ["SRC-MISRA"], "No frozen row isolates MISRA compliance-plan, deviation, enforcement, evidence, tool, and reviewer obligations as a proxy."),
    ("GMUT ATLAS Open Data event, generator weight, object definition, fiducial selection, systematic variation, covariance, checksum, and zero-row likelihood-refusal adapter", "atlas-open-data-zero-row-adapter", "GMUT Mind", "open_gap", ["SRC-ATLAS", "SRC-ATLAS-SYSTEMATICS"], "No frozen row isolates an ATLAS Open Data event-and-systematics adapter with an explicit zero-query, zero-download, zero-row likelihood refusal."),
    ("CBR safety-critical proof-artifact disclosure, worker defect report, accessible counterexample, proprietary boundary, incident remedy, affected-party review, legal and cultural authority, and Māori-authority reservation", "safety-proof-disclosure-authority", "Freed ID/CBR Heart", "exact_gate", ["SRC-FAA-SOFTWARE", "SRC-WCAG22", "SRC-MAORI-DATA", "SRC-TE-TAURA-WHIRI"], "No frozen row isolates proof-disclosure, worker-reporting, accessible counterexample, proprietary limits, remedy, and Māori-authority decision rights in one reservation matrix."),
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
    f"Prepare and bounded-test a nonpromotional extension for {row['proposal_id']} without crossing {row['execution_lane']}."
    for row in PROPOSALS
]

SKILL_TASKS = [
    f"Build phase-local review skill {index:02d} for {row['slug']} with an explicit nonpromotion boundary."
    for index, row in enumerate(PROPOSALS[12:23], 1)
]

SKILL_IDEAS = [
    ("ghc-family-finite-renormalization-contract", "Review finite-renormalization maps, composition laws, and observation firewalls."),
    ("ghc-family-infrared-cancellation-ledger", "Review KLN and Bloch-Nordsieck cancellation and resolution obligations."),
    ("ghc-family-lattice-improvement-boundary", "Review Symanzik improvement terms and continuum-claim boundaries."),
    ("ghc-family-proof-kernel-trust-boundary", "Separate elaborator, proof term, kernel, axiom, solver, and trusted-code claims."),
    ("ghc-family-bounded-model-completeness-guard", "Keep bounded model checking distinct from unbounded proof."),
    ("ghc-family-translation-refinement-contract", "Review source-target refinement, undefined behavior, and counterexamples."),
    ("ghc-family-permission-logic-boundary", "Review permission and heap-accounting obligations without deployment promotion."),
    ("ghc-family-draft-status-watch", "Fail closed when draft standards change or are promoted prematurely."),
    ("ghc-family-zero-row-collider-adapter", "Enforce zero-query and zero-row likelihood refusal for collider data adapters."),
    ("ghc-family-proof-disclosure-authority-rail", "Reserve disclosure, remedy, professional, affected-party, and Māori authority."),
]

RUNNER_TASKS = [
    f"Build and invoke family-compatible bounded runner {index:02d} for {surface}."
    for index, (_name, surface) in enumerate(
        [
            ("finite", "finite-renormalization"),
            ("infrared", "infrared-cancellation"),
            ("kernel", "proof-kernel-trust"),
            ("bounded", "bounded-model-completeness"),
            ("refinement", "translation-refinement"),
            ("permission", "permission-logic"),
            ("draft", "draft-status-watch"),
            ("zero-row", "zero-row-collider"),
            ("disclosure", "proof-disclosure-authority"),
            ("freeze", "x1-x2-freeze-integrity"),
        ],
        1,
    )
]

RUNNER_IDEAS = [
    ("ghc_family_finite_renormalization_guard.py", "finite-renormalization"),
    ("ghc_family_infrared_cancellation_guard.py", "infrared-cancellation"),
    ("ghc_family_proof_kernel_trust_guard.py", "proof-kernel-trust"),
    ("ghc_family_bounded_model_completeness_guard.py", "bounded-model-completeness"),
    ("ghc_family_translation_refinement_guard.py", "translation-refinement"),
    ("ghc_family_permission_logic_guard.py", "permission-logic"),
    ("ghc_family_draft_status_watch.py", "draft-status-watch"),
    ("ghc_family_zero_row_collider_guard.py", "zero-row-collider"),
    ("ghc_family_proof_disclosure_authority_guard.py", "proof-disclosure-authority"),
    ("ghc_family_x1_x2_freeze_integrity.py", "x1-x2-freeze-integrity"),
]

CLEAN_FIX_REFINE_TASKS = [
    f"REFINE-{index:02d}: review {row['slug']} terminology, falsifier, rollback, source status, and protected-gate wording without changing its frozen outcome class."
    for index, row in enumerate(PROPOSALS, 1)
]

X1_NEGATIVES = [
    (
        "V6533-X1-N01",
        "combined_induction_source_skill_memory_probe_timeout",
        "The first combined induction probe timed out after partial read-only output and earned no source, skill, or memory evidence credit.",
        "Split source, skill, routing, schema, baton, and memory reads into bounded literal-path probes; verify each exact endpoint and retain the timeout.",
    ),
    (
        "V6533-X1-N02",
        "x1_lifecycle_receipts_stale_after_first_index_add",
        "The first read-only staged validation after adding the three lifecycle receipts found their staged-path and JSON counts stale; it received zero pass credit.",
        "Stage the receipt paths, refresh the three self-excluded receipts once against the complete index, restage them, and only then run the unchanged read-only validator.",
    ),
    (
        "V6533-X1-N03",
        "accessible_reservation_exact_sentence_split",
        "The first isolated x1 test run found that a line break split the required manual-and-affected-user accessibility reservation sentence; the run received zero pass credit.",
        "Keep the required reservation sentence contiguous in the static report, preserve the surrounding boundary wording, and rerun only the scoped x1 test module.",
    ),
    (
        "V6533-X1-N04",
        "powershell_question_mark_wildcard_untracked_misclassification",
        "A final-review wrapper used -like '??*', where question marks are wildcards, and falsely classified every staged-add row as untracked; it received zero clean-state credit.",
        "Use the exact porcelain prefix test StartsWith('?? ') and keep staged, unstaged, and untracked classifications separate.",
    ),
]

REJECTED_COLLISIONS = [
    "A 2PI or Cornwall-Jackiw-Tomboulis effective-action row was rejected because the frozen chain already contains that mechanism.",
    "A Nielsen-identity gauge-dependence row was rejected because the frozen chain already isolates that mechanism.",
    "A Weinberg soft-factor row was rejected because the frozen chain already contains soft-graviton factorization.",
    "A Goldstone-theorem row was rejected because the frozen chain already contains spontaneous-symmetry and Goldstone obligations.",
    "A background-field split-symmetry row was rejected because the frozen chain already contains that mechanism.",
    "A COSE countersignature row was rejected because the frozen chain already contains countersignature and detached-signature profiles.",
    "A generic field-redefinition equivalence row was rejected because inherited equivalence-theorem mechanisms overlap it.",
    "An ACME Renewal Information row was rejected because the frozen chain already contains ARI; RFC 8739 STAR remains mechanism-distinct.",
]
