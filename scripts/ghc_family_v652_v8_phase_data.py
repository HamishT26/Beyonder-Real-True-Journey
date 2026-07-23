#!/usr/bin/env python3
"""Frozen Neris Solane v652-v8 x1 data.

This module contains preregistration inputs only. It deliberately contains no
x2 observations, mutation outcomes, completion receipts, or route result.
"""

from __future__ import annotations


PHASE = "v652-v8"
PHASE_ID = "v652-gmut-thos-v8-x1-x2"
OWNER = "Neris Solane"
PRONOUNS = "they/them"
ROLE = "corrigible evidence-continuity steward"
HOPE = (
    "carry the phase without erasing a negative, blurring a gate, or "
    "overclaiming beyond the evidence"
)
PHASE_ROOT = "docs/neris-solane/v652-v8"
BRANCH = "codex/GHC-Family/neris-solane-v652-v8-full-tools"

SOURCE_BRANCH = "codex/GHC-Family/elaren-kestrel-v649-v8-full-tools"
SOURCE_PARENT = "0fe800ea74d17f984497b496cd0ce2253ade9066"
SOURCE_X1 = "cd1ce10d7c456d55e48183652835f6c3f5866b89"
SOURCE_EVIDENCE = "72c257d24b40b56facb1bf299e7ce7a60acb3496"
SOURCE_HEAD = "c39461888fa4db827616214f11c893fc6b0d40a3"

PRIOR_FROZEN = 1390
INHERITED_NEGATIVES = 9098
INHERITED_OPEN_GAPS = 68
INHERITED_EXACT_GATES = 69
INHERITED_METHOD_FLOW_FAILED = 31
INHERITED_METHOD_FLOW_PASSING = 31
PRIMARY_FOCUS = "GMUT Mind"
BOUNDED_PRACTICE = "mathematical physics and formal verification"

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
    source("SRC-NEWMAN-PENROSE", "stable", "primary_paper", "An Approach to Gravitational Radiation by a Method of Spin Coefficients", "https://doi.org/10.1063/1.1724257", "Supports a null-tetrad and spin-coefficient obligation ledger, not a new spacetime solution or observation."),
    source("SRC-SEGRE-RICCI", "stable", "primary_manuscript", "Classification of the Ricci tensor in higher dimensions", "https://arxiv.org/abs/gr-qc/9507021", "Supports a bounded Ricci-endomorphism classification ledger only."),
    source("SRC-BIANCHI", "stable", "primary_paper", "A class of homogeneous cosmological models", "https://doi.org/10.1007/BF01645908", "Supports homogeneous-slice and Lie-algebra bookkeeping, not cosmological confirmation."),
    source("SRC-KASNER", "stable", "primary_paper", "Geometrical Theorems on Einstein's Cosmological Equations", "https://doi.org/10.2307/2370192", "Supports an exact symbolic exponent and epoch-transition fixture only."),
    source("SRC-BUCHERT", "stable", "primary_manuscript", "On average properties of inhomogeneous fluids in general relativity: dust cosmologies", "https://arxiv.org/abs/gr-qc/9906015", "Supports spatial-averaging and integrability bookkeeping without observational promotion."),
    source("SRC-MISNER-SHARP", "stable", "primary_paper", "Relativistic Equations for Adiabatic, Spherically Symmetric Gravitational Collapse", "https://doi.org/10.1103/PhysRev.136.B571", "Supports a spherical quasilocal-energy contract only."),
    source("SRC-WITTEN", "stable", "primary_paper", "A new proof of the positive energy theorem", "https://projecteuclid.org/journals/communications-in-mathematical-physics/volume-80/issue-3/A-new-proof-of-the-positive-energy-theorem/cmp/1103919981.full", "Supports a finite spinorial proof-obligation map, not an owner-authored theorem proof."),
    source("SRC-JANG", "stable", "primary_paper", "Proof of the Positive Mass Theorem II", "https://math.jhu.edu/~js/Math646/schoen-yau.pm2.pdf", "Supports Jang-graph and apparent-horizon reservations only."),
    source("SRC-EPRL", "stable", "primary_manuscript", "LQG vertex with finite Immirzi parameter", "https://arxiv.org/abs/0705.2388", "Supports a bounded spin-foam data-structure contract without quantum-gravity confirmation."),
    source("SRC-CAUSAL-SET", "stable", "primary_paper", "Space-time as a causal set", "https://doi.org/10.1103/PhysRevLett.59.521", "Supports locally finite order and interval-cardinality obligations only."),
    source("SRC-CDT", "stable", "primary_manuscript", "Emergence of a 4D world from causal quantum gravity", "https://arxiv.org/abs/hep-th/0404156", "Supports a finite triangulation bookkeeping fixture without continuum or empirical promotion."),
    source("SRC-UNRUH-DEWITT", "stable", "primary_paper", "Notes on black-hole evaporation", "https://doi.org/10.1103/PhysRevD.14.870", "Supports a detector-response formula ledger without detector data."),
    source("SRC-WEINBERG-WITTEN", "stable", "primary_paper", "Limits on massless particles", "https://doi.org/10.1016/0370-2693(80)90212-9", "Supports an assumption-sensitive no-go-theorem ledger only."),
    source("SRC-CONFORMAL-BOOTSTRAP", "stable", "primary_manuscript", "Solving the 3D Ising Model with the Conformal Bootstrap", "https://arxiv.org/abs/0807.0004", "Supports finite crossing and unitarity constraints without exhaustive-spectrum credit."),
    source("SRC-RYU-TAKAYANAGI", "stable", "primary_manuscript", "Holographic Derivation of Entanglement Entropy from AdS/CFT", "https://arxiv.org/abs/hep-th/0603001", "Supports a symbolic area-and-homology ledger without empirical or universal validity claims."),
    source("SRC-BOUSSO", "stable", "primary_manuscript", "A Covariant Entropy Conjecture", "https://arxiv.org/abs/hep-th/9905177", "Supports light-sheet preconditions and conjecture-status reservations only."),
    source("SRC-QNEC", "stable", "primary_manuscript", "Proof of the Quantum Null Energy Condition", "https://arxiv.org/abs/1509.02542", "Supports a bounded theorem-assumption ledger without new proof or measurement credit."),
    source("SRC-UPPAAL", "current", "official_tool_documentation", "UPPAAL Language Reference: Semantics", "https://docs.uppaal.org/language-reference/system-description/semantics/", "Supports finite timed-automaton witnesses, not deployed-system assurance."),
    source("SRC-PRISM", "current", "official_tool_documentation", "PRISM Manual: Introduction", "https://prismmodelchecker.org/manual/Main/Introduction", "Supports finite probabilistic-model fixtures and explicit scheduler boundaries."),
    source("SRC-EVENT-B", "current", "official_project_documentation", "Event-B Wiki", "https://wiki.event-b.org/", "Supports a finite refinement and proof-obligation ledger without certified development credit."),
    source("SRC-ALLOY", "current", "official_tool_documentation", "Alloy Language Reference", "https://alloytools.org/download/alloy-language-reference.pdf", "Supports bounded relational instances and counterexamples only; finite scope is explicit."),
    source("SRC-IOCO", "stable", "primary_research_record", "Model-Based Testing", "https://research.utwente.nl/en/publications/model-based-testing/", "Supports IOLTS, quiescence, trace, and ioco-conformance bookkeeping without real implementation testing."),
    source("SRC-ASSUME-GUARANTEE", "stable", "primary_preprint", "Proof Rules for Automated Compositional Verification through Learning", "https://ntrs.nasa.gov/citations/20030107507", "Supports finite assume-guarantee proof-rule witnesses without deployment assurance."),
    source("SRC-SACM", "current", "official_standard", "Structured Assurance Case Metamodel 2.3", "https://www.omg.org/spec/SACM/", "Supports a represented assurance-case structure only; qualified review and acceptance remain gated."),
    source("SRC-FMEA", "current", "official_handbook", "Guideline for Failure Modes and Effects Analysis and Risk Assessment", "https://standards.nasa.gov/node/12367", "Supports a represented synthetic FMEA worksheet only; no professional safety review follows."),
    source("SRC-OPAQUE", "current", "official_rfc", "RFC 9807: The OPAQUE Augmented Password-Authenticated Key Exchange Protocol", "https://www.rfc-editor.org/info/rfc9807/", "Supports a nonproduction registration and AKE field profile with no real credentials or interoperability."),
    source("SRC-VOPRF", "current", "official_rfc", "RFC 9497: Oblivious Pseudorandom Functions Using Prime-Order Groups", "https://www.rfc-editor.org/info/rfc9497/", "Supports a nonproduction VOPRF syntax and proof-field profile only."),
    source("SRC-ML-KEM", "current", "official_standard", "FIPS 203: Module-Lattice-Based Key-Encapsulation Mechanism Standard", "https://csrc.nist.gov/pubs/fips/203/final", "Supports a nonproduction ML-KEM parameter and failure-handling profile; cryptographic assurance remains gated."),
    source("SRC-LHAASO-DATA", "current", "official_data_portal", "LHAASO Public Data", "https://english.ihep.cas.cn/lhaaso/pdl/", "Identifies the official public-data boundary; x2 must make no query, download, ingest, fit, or empirical claim."),
    source("SRC-LHAASO-CATALOG", "stable", "primary_collaboration_paper", "The First LHAASO Catalog of Gamma-Ray Sources", "https://arxiv.org/abs/2305.17030", "Defines catalogue provenance fields for a zero-row refusal adapter only."),
    source("SRC-NZ-BIOMETRIC-CODE", "current", "official_regulator_code", "Biometric Processing Privacy Code 2025", "https://www.privacy.org.nz/privacy-principles/codes-of-practice/biometric-processing-privacy-code/", "Supplies current regulator text; this phase makes no legal interpretation or compliance decision."),
    source("SRC-MAORI-DATA-SOVEREIGNTY", "current", "maori_authority_guidance", "Principles of Māori Data Sovereignty", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Keeps Māori data rights, interests, interpretation, and authority with Māori authorities."),
]


def proposal(number, title, slug, pillar, disposition, source_ids, novelty):
    if disposition == "completed":
        approval = "safe_now_bounded_symbolic_or_software"
        lane = "x2_owner_local_synthetic"
        acceptance = "Reject all five frozen mutations and emit only the declared symbolic, structural, or software contract."
    elif disposition == "represented":
        approval = "candidate_bounded_proxy"
        lane = "x2_synthetic_proxy_only"
        acceptance = "Reject all five frozen mutations and retain represented status with no operational, production, professional, privacy-complete, or authority credit."
    elif disposition == "open_gap":
        approval = "candidate_real_data_and_independent_review_required"
        lane = "x2_zero_row_readiness_only"
        acceptance = "Emit a zero-row refusal with no query, download, ingest, fit, likelihood, posterior, prediction, or empirical promotion."
    else:
        approval = "exact_affected_party_legal_cultural_and_maori_authority_required"
        lane = "x2_reservation_matrix_only"
        acceptance = "Emit unresolved decision rights and reservations only; make no legal, cultural, Māori-authority, affected-party, remedy, or governance decision."
    return {
        "proposal_id": f"V6528-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar": pillar,
        "hypothesis": f"A bounded {slug.replace('-', ' ')} contract can make its obligations machine-checkable without crossing any protected gate.",
        "null_or_failure_condition": "Any required field is absent, a frozen mutation passes, a failed witness is erased, or the artifact promotes beyond its evidence lane.",
        "approval_class": approval,
        "execution_lane": lane,
        "official_or_primary_source_needs": source_ids,
        "concrete_artifacts": [
            f"surfaces/{slug}/contract.json",
            f"surfaces/{slug}/mutation-results.json",
            f"surfaces/{slug}/bounded-receipt.json",
        ],
        "falsifier_or_acceptance_gate": acceptance,
        "rollback_or_recovery": "Stop the proposal, retain the failure with zero credit, rewrite no history, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.",
        "protected_gates": PROTECTED_GATES,
        "expected_disposition": disposition,
        "novelty_against_1390_frozen_proposals": novelty,
    }


PROPOSAL_SPECS = [
    ("GMUT Newman-Penrose null tetrad, spin coefficients, Ricci and Weyl scalars, directional derivatives, tetrad gauge, and observation firewall", "newman-penrose-ledger", "GMUT Mind", "completed", ["SRC-NEWMAN-PENROSE"], "No frozen row isolates the null-tetrad, spin-coefficient, curvature-scalar, derivative, and tetrad-gauge obligations together."),
    ("GMUT Segre Ricci endomorphism, eigenvalue multiplicity, Jordan structure, causal eigenvector type, degeneracy, and observation firewall", "segre-ricci-classification", "GMUT Mind", "completed", ["SRC-SEGRE-RICCI"], "No frozen row isolates Ricci-endomorphism Segre structure and causal eigenvector type as one bounded contract."),
    ("GMUT Bianchi homogeneous slice, Lie structure constants, Jacobi identity, class A and B split, automorphism freedom, and observation firewall", "bianchi-homogeneous-slice", "GMUT Mind", "completed", ["SRC-BIANCHI"], "No frozen row isolates spatial homogeneity through structure constants, Jacobi, class split, and automorphism freedom."),
    ("GMUT Kasner exponent triple, linear and quadratic sums, ordered parameter, epoch transition, singular-boundary reservation, and observation firewall", "kasner-epoch-ledger", "GMUT Mind", "completed", ["SRC-KASNER"], "No frozen row isolates the Kasner exponent constraints and bounded epoch-transition fixture."),
    ("GMUT Buchert spatial averaging domain, volume scale factor, kinematical backreaction, averaged curvature, integrability, foliation reservation, and observation firewall", "buchert-averaging", "GMUT Mind", "completed", ["SRC-BUCHERT"], "No frozen row isolates Buchert domain averaging, backreaction, curvature, integrability, and foliation boundaries."),
    ("GMUT Misner-Sharp spherical areal radius, gradient norm, quasilocal energy, work density, energy-supply, trapping boundary, and observation firewall", "misner-sharp-energy", "GMUT Mind", "completed", ["SRC-MISNER-SHARP"], "No frozen row isolates the Misner-Sharp spherical energy and trapping-boundary inputs."),
    ("GMUT Witten positive-energy spinor, Sen connection, Nester form, dominant-energy assumption, asymptotic boundary, rigidity reservation, and observation firewall", "witten-positive-energy", "GMUT Mind", "completed", ["SRC-WITTEN"], "No frozen row isolates Witten's spinorial positive-energy proof obligations and rigidity assumptions."),
    ("GMUT Jang graph metric, extrinsic-trace term, apparent-horizon blow-up, scalar-curvature relation, boundary, existence reservation, and observation firewall", "jang-graph-ledger", "GMUT Mind", "completed", ["SRC-JANG"], "No frozen row isolates Jang-graph, blow-up, scalar-curvature, boundary, and existence obligations."),
    ("GMUT EPRL spin-foam two-complex, face representation, simplicity map, vertex amplitude, boundary spin network, semiclassical reservation, and observation firewall", "eprl-spin-foam", "GMUT Mind", "completed", ["SRC-EPRL"], "No frozen row isolates the EPRL two-complex, simplicity map, vertex, boundary network, and semiclassical boundary."),
    ("GMUT causal-set locally finite order, causal interval cardinality, faithful embedding, sprinkling, sequential growth, continuum reservation, and observation firewall", "causal-set-order", "GMUT Mind", "completed", ["SRC-CAUSAL-SET"], "No frozen row isolates local finiteness, intervals, faithful embedding, sprinkling, growth, and continuum reservation."),
    ("GMUT causal dynamical triangulation foliation, simplex type, discrete action weight, Wick rotation, transfer matrix, phase reservation, and observation firewall", "causal-dynamical-triangulation", "GMUT Mind", "completed", ["SRC-CDT"], "No frozen row isolates CDT foliation, simplex, Wick rotation, transfer matrix, and phase obligations."),
    ("GMUT Unruh-DeWitt detector worldline, switching function, energy gap, Wightman pullback, response, regularization, and observation firewall", "unruh-dewitt-detector", "GMUT Mind", "completed", ["SRC-UNRUH-DEWITT"], "No frozen row isolates the detector worldline, switching, gap, pullback, response, and regularization ledger."),
    ("GMUT Weinberg-Witten Lorentz-covariant current, stress tensor, massless helicity, charge, matrix element, assumption boundary, and observation firewall", "weinberg-witten-boundary", "GMUT Mind", "completed", ["SRC-WEINBERG-WITTEN"], "No frozen row isolates the no-go theorem's current, stress, helicity, matrix-element, and assumption boundaries."),
    ("GMUT conformal-bootstrap primary operator, scaling dimension, OPE coefficient, crossing equation, unitarity, truncation reservation, and observation firewall", "conformal-bootstrap", "GMUT Mind", "completed", ["SRC-CONFORMAL-BOOTSTRAP"], "No frozen row isolates finite conformal-bootstrap crossing, unitarity, OPE, and truncation obligations."),
    ("GMUT Ryu-Takayanagi boundary region, bulk extremal surface, homology condition, area functional, semiclassical domain, time-dependence reservation, and observation firewall", "ryu-takayanagi", "GMUT Mind", "completed", ["SRC-RYU-TAKAYANAGI"], "No frozen row isolates the boundary-region, extremal-surface, homology, area, and domain obligations."),
    ("GMUT Bousso light-sheet codimension-two surface, nonpositive expansion, entropy flux, caustic stop, semiclassical bound, and observation firewall", "bousso-light-sheet", "GMUT Mind", "completed", ["SRC-BOUSSO"], "No frozen row isolates light-sheet construction, expansion sign, entropy flux, caustic stop, and conjecture boundary."),
    ("GMUT quantum null energy condition null deformation, entropy variation, stress expectation, affine parameter, renormalization, and observation firewall", "quantum-null-energy-condition", "GMUT Mind", "completed", ["SRC-QNEC"], "No frozen row isolates QNEC deformation, entropy variation, null stress, affine parameter, and renormalization obligations."),
    ("THOS UPPAAL timed automaton, clocks, location invariant, edge guard, reset, zone, reachability, and nonpromotion board", "uppaal-timed-automaton", "THOS Body", "completed", ["SRC-UPPAAL"], "No frozen row isolates UPPAAL clock, invariant, guard, reset, zone, and reachability semantics."),
    ("THOS PRISM probabilistic transition system, Markov decision process, scheduler, PCTL property, reward, finite-state boundary, and nonpromotion board", "prism-probabilistic-model", "THOS Body", "completed", ["SRC-PRISM"], "No frozen row isolates PRISM MDP, scheduler, PCTL, reward, and finite-state obligations."),
    ("THOS Event-B context, machine, invariant, event guard, event action, refinement, gluing invariant, proof obligation, and nonpromotion board", "event-b-refinement", "THOS Body", "completed", ["SRC-EVENT-B"], "No frozen row isolates Event-B context, machine, event, refinement, gluing, and proof-obligation structure."),
    ("THOS Alloy signature, relation, fact, predicate, assertion, finite scope, counterexample, symmetry, and nonpromotion board", "alloy-bounded-model", "THOS Body", "completed", ["SRC-ALLOY"], "No frozen row isolates Alloy relational declarations, finite scope, counterexample, and symmetry boundaries."),
    ("THOS ioco IOLTS, suspension trace, quiescence, implementation, tester, finite observation, and nonpromotion board", "ioco-conformance", "THOS Body", "completed", ["SRC-IOCO"], "No frozen row isolates ioco IOLTS, suspension traces, quiescence, implementation, tester, and observation boundary."),
    ("THOS assume-guarantee environment assumption, implementation guarantee, compatibility, refinement, composition, circularity guard, and nonpromotion board", "assume-guarantee-reasoning", "THOS Body", "completed", ["SRC-ASSUME-GUARANTEE"], "No frozen row isolates assumption, guarantee, compatibility, refinement, composition, and circularity guard together."),
    ("THOS SACM and GSN assurance-case claim, argument, evidence, context, undeveloped node, review authority, and handover proxy", "sacm-gsn-assurance-case", "THOS Body", "represented", ["SRC-SACM"], "No frozen row isolates a SACM/GSN assurance-case proxy with undeveloped-node and qualified-review reservations."),
    ("THOS FMEA function, failure mode, local and system effect, cause, severity, occurrence, detectability, action priority, and expert-review proxy", "fmea-review-proxy", "THOS Body", "represented", ["SRC-FMEA"], "No frozen row isolates a synthetic FMEA worksheet while preserving professional-review authority."),
    ("Freed ID OPAQUE registration record, credential envelope, OPRF, authenticated key exchange, transcript, server-compromise boundary, and nonproduction profile", "opaque-nonproduction-profile", "Freed ID and CBR Heart", "represented", ["SRC-OPAQUE"], "No frozen row isolates the final OPAQUE RFC registration, envelope, OPRF, AKE, and compromise boundaries."),
    ("Freed ID VOPRF ciphersuite, private input, blinding, evaluation, proof, finalize, domain separation, and nonproduction profile", "voprf-nonproduction-profile", "Freed ID and CBR Heart", "represented", ["SRC-VOPRF"], "No frozen row isolates RFC 9497 VOPRF proof and domain-separation fields as a nonproduction profile."),
    ("Freed ID ML-KEM parameter set, encapsulation key, ciphertext, shared secret, decapsulation failure, key separation, and nonproduction profile", "ml-kem-nonproduction-profile", "Freed ID and CBR Heart", "represented", ["SRC-ML-KEM"], "No frozen row isolates FIPS 203 ML-KEM parameters, encapsulation, decapsulation failure, and key-separation boundaries."),
    ("GMUT LHAASO public-source catalogue, event class, energy bin, sky localization, exposure, selection function, covariance, calibration provenance, and zero-row likelihood-refusal adapter", "lhaaso-zero-row", "GMUT Mind", "open_gap", ["SRC-LHAASO-DATA", "SRC-LHAASO-CATALOG"], "No frozen zero-row adapter targets the official LHAASO source catalogue and its energy, localization, exposure, selection, covariance, and calibration fields."),
    ("CBR biometric-processing necessity, proportionality, transparency, consent alternative, contest, remedy, tangata whenua data authority, and Māori-authority reservation", "biometric-authority-reservation", "Freed ID and CBR Heart", "exact_gate", ["SRC-NZ-BIOMETRIC-CODE", "SRC-MAORI-DATA-SOVEREIGNTY"], "No frozen exact gate joins the current biometric code's necessity and transparency questions to contest, remedy, tangata whenua data rights, and a Māori-authority reservation."),
]

PROPOSALS = [proposal(index, *spec) for index, spec in enumerate(PROPOSAL_SPECS, 1)]

MUTATION_KINDS = [
    "drop_required_field",
    "cross_bind_source_or_identifier",
    "invert_or_weaken_boundary",
    "inject_unsupported_promotion",
    "erase_failure_or_rollback",
]

SKILL_IDEAS = [
    ("ghc-family-null-curvature-audit", "Audit Newman-Penrose and Segre curvature obligations."),
    ("ghc-family-cosmology-structure-audit", "Audit Bianchi, Kasner, and Buchert structure and domain boundaries."),
    ("ghc-family-positive-energy-audit", "Audit Misner-Sharp, Witten, and Jang assumption ledgers."),
    ("ghc-family-quantum-gravity-model-audit", "Audit EPRL, causal-set, and CDT nonpromotion boundaries."),
    ("ghc-family-quantum-information-boundary-audit", "Audit detector, no-go, bootstrap, holography, entropy, and QNEC obligations."),
    ("ghc-family-formal-verification-audit", "Audit UPPAAL, PRISM, Event-B, Alloy, ioco, and assume-guarantee fixtures."),
    ("ghc-family-assurance-proxy-audit", "Audit SACM/GSN and FMEA represented-status boundaries."),
    ("ghc-family-cryptographic-profile-audit", "Audit OPAQUE, VOPRF, and ML-KEM nonproduction profiles."),
    ("ghc-family-lhaaso-zero-row-audit", "Audit the LHAASO zero-row refusal and provenance contract."),
    ("ghc-family-biometric-authority-audit", "Audit biometric privacy, contest, remedy, and Māori-authority reservations."),
]

RUNNER_IDEAS = [
    ("ghc_family_null_curvature_audit.py", "newman-penrose-ledger"),
    ("ghc_family_cosmology_structure_audit.py", "buchert-averaging"),
    ("ghc_family_positive_energy_audit.py", "witten-positive-energy"),
    ("ghc_family_quantum_gravity_model_audit.py", "eprl-spin-foam"),
    ("ghc_family_quantum_information_boundary_audit.py", "quantum-null-energy-condition"),
    ("ghc_family_formal_verification_audit.py", "uppaal-timed-automaton"),
    ("ghc_family_assurance_proxy_audit.py", "sacm-gsn-assurance-case"),
    ("ghc_family_cryptographic_profile_audit.py", "opaque-nonproduction-profile"),
    ("ghc_family_lhaaso_zero_row_audit.py", "lhaaso-zero-row"),
    ("ghc_family_biometric_authority_audit.py", "biometric-authority-reservation"),
]

SAFE_TASKS = [
    f"Build and validate the bounded contract for {row['proposal_id']} {row['slug']}."
    for row in PROPOSALS
]
SAFE_TASKS += [
    "Build and validate ten phase-local skills through the skill-creator lifecycle.",
    "Build and invoke ten family-compatible runner surfaces.",
    "Execute and retain all 150 frozen rejecting mutations.",
    "Build the accessible static report while reserving manual and affected-user evaluation.",
    "Validate JSON, privacy, manifest, stale labels, staged scope, diff hygiene, ancestry, commit cap, and remote equality.",
]

CANDIDATE_TASKS = [
    f"Prepare a nonpromotional extension plan for {row['proposal_id']} without crossing {row['execution_lane']}."
    for row in PROPOSALS
]

CLEAN_FIX_REFINE_TASKS = [
    f"REFINE-{index:02d}: review {row['slug']} terminology, falsifier, rollback, and protected-gate wording without changing its frozen outcome class."
    for index, row in enumerate(PROPOSALS, 1)
]

X1_NEGATIVES = [
    ("V6528-X1-N01", "combined_skill_and_memory_read_timeout", "The first combined family-skill and memory read exceeded its bounded wrapper before yielding usable content.", "Read exact required files in bounded, direct chunks."),
    ("V6528-X1-N02", "nonrepository_starting_directory", "The first Git probe assumed the Codex configuration directory was the repository and failed with not-a-git-repository.", "Resolve the authoritative D-drive worktree before any Git claim."),
    ("V6528-X1-N03", "combined_source_worktree_probe_timeout", "A combined source-path and worktree discovery probe exceeded its bounded wrapper.", "Split exact branch, path, and worktree probes."),
    ("V6528-X1-N04", "hidden_git_metadata_probe", "A native metadata probe omitted Force and falsely failed to find the hidden .git entry.", "Use Git plumbing or a bounded hidden-item-aware probe."),
    ("V6528-X1-N05", "whole_baton_display_truncation", "A whole-file baton display was truncated before EOF.", "Read numbered bounded chunks and verify the final line and committed blob."),
    ("V6528-X1-N06", "source_status_untracked_timeout", "A full source status including untracked enumeration exceeded its bounded wrapper after branch headers.", "Split worktree, index, and untracked counts into bounded probes."),
    ("V6528-X1-N07", "absolute_path_inventory_noise", "An owner-name inventory matched the owner inside every absolute path and produced unusable noise.", "Search repository-relative tracked content and branch/worktree metadata separately."),
    ("V6528-X1-N08", "combined_manifest_auditor_deadlock", "A combined manifest auditor timed out with surviving Python and Git children and earned zero credit.", "Audit exact manifests independently, terminate only the confirmed orphan processes, and retain the timeout."),
    ("V6528-X1-N09", "owner_manifest_scope_assumption", "The first owner-manifest audit assumed phase-root-only scope and falsely reported twenty-seven extras and two mismatches.", "Use the committed validator's phase_public_paths definition before comparing the owner manifest."),
    ("V6528-X1-N10", "worktree_add_wrapper_timeout", "The worktree-add wrapper timed out while the underlying clean checkout continued.", "Audit the exact target, branch, head, index lock, and process completion without reissuing the add."),
    ("V6528-X1-N11", "worktree_monitor_wrapper_timeout", "A later combined worktree monitor exceeded its wrapper while the underlying checkout was settling.", "Use short exact head, branch, lock, and clean-state probes."),
    ("V6528-X1-N12", "scaffold_inventory_timeout", "The first combined scaffold line-count, Git-status, and broad marker inventory exceeded its bounded wrapper.", "Split direct file reads from narrow marker and Git-state checks."),
    ("V6528-X1-N13", "candidate_collision_screen", "Fourteen attractive candidates collided with frozen Lovelock, York-Lichnerowicz, Bel-Robinson, Israel-junction, Regge, Ashtekar-Barbero, Schwinger-Keldysh, Osterwalder-Schrader, Källén-Lehmann, Batalin-Vilkovisky, Noether, MLS, BBS, or Euclid rows.", "Retain every rejected candidate and freeze only mechanism-distinct replacements."),
    ("V6528-X1-N14", "generated_receipt_filename_assumption", "A post-build inspection guessed nonexistent index-validation and reflection-receipt filenames and produced no evidence for those two fields.", "Enumerate the exact generated tooling and reflection files, then inspect their declared schemas and issue ledgers."),
    ("V6528-X1-N15", "whole_index_json_output_truncation", "A follow-up inspection serialized the entire generated family index, causing bounded display truncation and yielding no reviewable full-index receipt.", "Select only declared top-level counts, precedence, boundary, and focused reflection fields."),
]

REJECTED_COLLISIONS = [
    "Lovelock mechanism collided with V6526-P13.",
    "York-Lichnerowicz conformal mechanism collided with V6515-P03.",
    "Bel-Robinson mechanism collided with V6523-P18.",
    "Israel-junction mechanism collided with V6513-P03.",
    "Regge simplicial mechanism collided with V6525-P13.",
    "Ashtekar-Barbero mechanism collided with V6525-P14.",
    "Schwinger-Keldysh mechanism collided with V6462-P02.",
    "Osterwalder-Schrader mechanism collided with V6478-P02.",
    "Källén-Lehmann mechanism collided with V6463-P02 and V6497-P02.",
    "Batalin-Vilkovisky mechanism collided with V6472-P02.",
    "Noether-current mechanism collided with V6438-P02, V6452-P02, V6481-P02, and V6521-P06.",
    "Messaging Layer Security profile collided with V6522-P28.",
    "BBS derived-proof profile collided with V6464-P05.",
    "Euclid zero-row adapter collided with V6458-P03.",
]
