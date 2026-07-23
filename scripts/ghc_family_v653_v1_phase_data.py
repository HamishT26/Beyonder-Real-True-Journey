#!/usr/bin/env python3
"""Frozen Vesper Arlen v653-v1 x1 data.

This module contains preregistration inputs only. It deliberately contains no
x2 observations, mutation outcomes, completion receipts, or route result.
"""

from __future__ import annotations


PHASE = "v653-v1"
PHASE_ID = "v653-gmut-thos-v1-x1-x2"
OWNER = "Vesper Arlen"
PRONOUNS = "they/them"
ROLE = "corrigible systems-verification cartographer"
HOPE = (
    "make formal obligations and human authority boundaries legible without "
    "converting symbolic, synthetic, or same-owner evidence into proof"
)
PHASE_ROOT = "docs/vesper-arlen/v653-v1"
BRANCH = "codex/GHC-Family/vesper-arlen-v653-v1-full-tools"

SOURCE_BRANCH = "codex/GHC-Family/neris-solane-v652-v8-full-tools"
SOURCE_PARENT = "c39461888fa4db827616214f11c893fc6b0d40a3"
SOURCE_X1 = "6e5c0e6fbe1bc569bd2eb8971629f2125f1c1984"
SOURCE_EVIDENCE = "b9e3c008492f6ed6235dc60e77282acc71aa736d"
SOURCE_HEAD = "3b955da5070d8b73bbfc23acbbaac541c57cb1bc"

PRIOR_FROZEN = 1420
INHERITED_NEGATIVES = 9268
INHERITED_OPEN_GAPS = 69
INHERITED_EXACT_GATES = 70
INHERITED_METHOD_FLOW_FAILED = 20
INHERITED_METHOD_FLOW_PASSING = 20
PRIMARY_FOCUS = "THOS Body"
BOUNDED_PRACTICE = (
    "formal verification and emergency-communications assurance handover"
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
        "SRC-HADAMARD",
        "stable",
        "primary_manuscript",
        "On the global Hadamard parametrix in QFT and the signed squared geodesic distance",
        "https://arxiv.org/abs/2107.04903",
        "Supports a local singular-structure and domain ledger only, not a new state, propagator, or observation.",
    ),
    source(
        "SRC-DEWITT",
        "stable",
        "primary_paper",
        "Dynamical Theory in Curved Spaces. I",
        "https://doi.org/10.1103/RevModPhys.29.377",
        "Supports a bounded heat-kernel coefficient and asymptotic-domain ledger without renormalized-physics credit.",
    ),
    source(
        "SRC-KALUZA-KLEIN",
        "stable",
        "primary_record",
        "Zum Unitätsproblem der Physik",
        "https://ui.adsabs.harvard.edu/abs/1921SPAW.......966K/abstract",
        "Supports circle-reduction bookkeeping only; no physical extra dimension is established.",
    ),
    source(
        "SRC-LTB",
        "stable",
        "primary_paper",
        "Spherically Symmetrical Models in General Relativity",
        "https://doi.org/10.1093/mnras/107.5-6.410",
        "Supports an exact dust-solution obligation board without observational or cosmological promotion.",
    ),
    source(
        "SRC-PENROSE-INEQUALITY",
        "stable",
        "primary_paper",
        "The inverse mean curvature flow and the Riemannian Penrose inequality",
        "https://projecteuclid.org/journals/journal-of-differential-geometry/volume-59/issue-3/The-inverse-mean-curvature-flow-and-the-Riemannian-Penrose-inequality/10.4310/jdg/1090349447.full",
        "Supports a theorem-assumption ledger only; this phase proves no new inequality.",
    ),
    source(
        "SRC-WHEELER-DEWITT",
        "stable",
        "primary_paper",
        "Quantum Theory of Gravity. I. The Canonical Theory",
        "https://doi.org/10.1103/PhysRev.160.1113",
        "Supports canonical constraint and factor-ordering reservations without quantum-gravity confirmation.",
    ),
    source(
        "SRC-KODAMA",
        "stable",
        "primary_paper",
        "Conserved Energy Flux for the Spherically Symmetric System and the Back Reaction Problem",
        "https://doi.org/10.1143/PTP.63.1217",
        "Supports a spherical current and trapping-horizon obligation ledger only.",
    ),
    source(
        "SRC-GAUSSIAN-NULL",
        "stable",
        "primary_manuscript",
        "Near Horizon Geometry and the Einstein Equations",
        "https://arxiv.org/abs/0705.4214",
        "Supports Gaussian-null coordinate and near-horizon bookkeeping without existence or uniqueness credit.",
    ),
    source(
        "SRC-SACHS",
        "stable",
        "primary_paper",
        "Gravitational Waves in General Relativity. VI. The Outgoing Radiation Condition",
        "https://doi.org/10.1098/rspa.1961.0202",
        "Supports a screen-space optical and Jacobi-map ledger without measured lensing evidence.",
    ),
    source(
        "SRC-NEWMAN-JANIS",
        "stable",
        "primary_paper",
        "Note on the Kerr Spinning-Particle Metric",
        "https://doi.org/10.1063/1.1704350",
        "Supports an algorithm-step and reality-condition ledger without authorizing solution generation claims.",
    ),
    source(
        "SRC-PETROV-SPECIALITY",
        "stable",
        "primary_manuscript",
        "Making use of geometrical invariants in black hole collisions",
        "https://arxiv.org/abs/gr-qc/0003031",
        "Supports invariant-ratio and degeneracy bookkeeping without classifying any observed spacetime.",
    ),
    source(
        "SRC-ERNST",
        "stable",
        "primary_paper",
        "New Formulation of the Axially Symmetric Gravitational Field Problem",
        "https://doi.org/10.1103/PhysRev.167.1175",
        "Supports stationary-axisymmetric potential obligations only.",
    ),
    source(
        "SRC-GEROCH",
        "stable",
        "primary_paper",
        "A Method for Generating Solutions of Einstein's Equations",
        "https://doi.org/10.1063/1.1665427",
        "Supports reduced-potential and transformation bookkeeping without a new solution claim.",
    ),
    source(
        "SRC-TAUB-NUT",
        "stable",
        "primary_paper",
        "Empty-Space Generalization of the Schwarzschild Metric",
        "https://doi.org/10.1063/1.1704014",
        "Supports parameter, fibre, patch, and causal-pathology reservations only.",
    ),
    source(
        "SRC-VAIDYA",
        "stable",
        "primary_record",
        "The Gravitational Field of a Radiating Star",
        "https://ui.adsabs.harvard.edu/abs/1951PMIA....33..264V/abstract",
        "Supports a null-fluid mass-function obligation board without astrophysical inference.",
    ),
    source(
        "SRC-MCVITTIE",
        "stable",
        "primary_record",
        "The mass-particle in an expanding universe",
        "https://ui.adsabs.harvard.edu/abs/1933MNRAS..93..325M/abstract",
        "Supports a metric-domain and no-accretion-assumption ledger without cosmological confirmation.",
    ),
    source(
        "SRC-ROBINSON-TRAUTMAN",
        "stable",
        "primary_paper",
        "Spherical Gravitational Waves",
        "https://doi.org/10.1103/PhysRevLett.4.431",
        "Supports null-congruence and parabolic-evolution obligations only.",
    ),
    source(
        "SRC-MCRL2",
        "current",
        "official_tool_documentation",
        "mCRL2 language and PBES documentation",
        "https://mcrl2.org/web/user_manual/language_reference/pbes.html",
        "Supports finite process and fixed-point fixtures, not deployed-system verification.",
    ),
    source(
        "SRC-NUSMV",
        "current",
        "official_tool_documentation",
        "NuSMV User Manual",
        "https://nusmv.fbk.eu/user-manual.html",
        "Supports finite transition-system, CTL, LTL, and counterexample fixtures only.",
    ),
    source(
        "SRC-Z",
        "current",
        "official_standard",
        "ISO/IEC 13568:2002 Z formal specification notation",
        "https://www.iso.org/standard/21573.html",
        "Supports syntax, typing, schema, and semantic obligation bookkeeping only.",
    ),
    source(
        "SRC-VDM",
        "current",
        "official_project_documentation",
        "The VDM languages",
        "https://www.overturetool.org/languages/",
        "Supports bounded state, invariant, precondition, and operation fixtures only.",
    ),
    source(
        "SRC-LOTOS",
        "current",
        "official_standard",
        "ISO 8807:1989 LOTOS",
        "https://www.iso.org/standard/16258.html",
        "Supports finite behavioural and synchronization contracts without conformance certification.",
    ),
    source(
        "SRC-CEGAR",
        "stable",
        "primary_paper",
        "Counterexample-Guided Abstraction Refinement",
        "https://doi.org/10.1007/10722167_15",
        "Supports a bounded spurious-counterexample and refinement loop only.",
    ),
    source(
        "SRC-BOWTIE",
        "current",
        "official_regulator_guidance",
        "UK Civil Aviation Authority Bowtie guidance",
        "https://www.caa.co.uk/safety-initiatives/working-with-industry/bowtie/",
        "Supports a represented barrier map only; professional risk review remains gated.",
    ),
    source(
        "SRC-LOPA",
        "current",
        "official_professional_body_guidance",
        "CCPS Layer of Protection Analysis overview",
        "https://www.aiche.org/ccps/resources/tools/lopa",
        "Supports a represented single cause-consequence worksheet only; no quantitative safety decision follows.",
    ),
    source(
        "SRC-SCRAM",
        "current",
        "official_rfc",
        "RFC 7677 SCRAM-SHA-256 and SCRAM-SHA-256-PLUS",
        "https://www.rfc-editor.org/info/rfc7677/",
        "Supports synthetic field and transcript vectors only, with no real credential or interoperability event.",
    ),
    source(
        "SRC-KERBEROS-FAST",
        "current",
        "official_rfc",
        "RFC 6113 A Generalized Framework for Kerberos Pre-Authentication",
        "https://www.rfc-editor.org/info/rfc6113/",
        "Supports synthetic armor, request, response, and downgrade fields only.",
    ),
    source(
        "SRC-PROXY-CERT",
        "current",
        "official_rfc",
        "RFC 3820 Internet X.509 PKI Proxy Certificate Profile",
        "https://www.rfc-editor.org/info/rfc3820/",
        "Supports synthetic path-length and policy fields only, with no real keys or trust decision.",
    ),
    source(
        "SRC-MEERKAT-ARCHIVE",
        "current",
        "official_data_portal",
        "MeerKAT Telescope Data Archive Portal",
        "https://archive-gw-1.kat.ac.za/",
        "Identifies the official archive boundary; x2 must make no query, download, ingest, calibration, fit, or empirical claim.",
    ),
    source(
        "SRC-MEERKAT-UPDATE",
        "current",
        "official_facility_notice",
        "MeerKAT Telescope Data Archive Portal Update",
        "https://www.sarao.ac.za/news/meerkat-telescope-data-archive-portal-update/",
        "Supports provenance and archive-status fields for a zero-row adapter only.",
    ),
    source(
        "SRC-NEMA-EMA",
        "current",
        "official_technical_standard",
        "Emergency Mobile Alert protocols for User Agencies TS 06/26",
        "https://www.civildefence.govt.nz/guidance-training/guidelines/technical-standards/0626-emergency-mobile-alert-protocols-for-user-agencies",
        "Supplies the current official alerting boundary; this phase makes no operational or legal decision.",
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
        "Keeps Māori data rights, language, interpretation, and governance with Māori authorities.",
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
        "proposal_id": f"V6531-P{number:02d}",
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
        "novelty_against_1420_frozen_proposals": novelty,
    }


PROPOSAL_SPECS = [
    ("GMUT Hadamard parametrix world function, Van Vleck determinant, transport coefficients, wavefront domain, coincidence limit, state subtraction, and observation firewall", "hadamard-parametrix", "GMUT Mind", "completed", ["SRC-HADAMARD"], "No frozen row isolates the Hadamard local singular structure, transport hierarchy, coincidence limit, and state-subtraction boundary."),
    ("GMUT DeWitt-Schwinger proper time, heat kernel, Seeley-DeWitt coefficient, coincidence limit, asymptotic order, renormalization scale, and observation firewall", "dewitt-schwinger-heat-kernel", "GMUT Mind", "completed", ["SRC-DEWITT"], "No frozen row isolates the DeWitt-Schwinger proper-time coefficient hierarchy and asymptotic renormalization boundary."),
    ("GMUT Kaluza-Klein circle fibre, cylinder condition, metric decomposition, gauge field, radion, Fourier mode, compactification scale, and observation firewall", "kaluza-klein-circle-reduction", "GMUT Mind", "completed", ["SRC-KALUZA-KLEIN"], "No frozen row isolates circle-fibre reduction, radion, Fourier modes, and compactification-scale obligations."),
    ("GMUT Lemaître-Tolman-Bondi dust shell, areal radius, mass function, energy function, bang-time function, shell crossing, centre regularity, and observation firewall", "ltb-dust-ledger", "GMUT Mind", "completed", ["SRC-LTB"], "No frozen row isolates LTB shell functions, bang time, shell crossing, and centre regularity."),
    ("GMUT Riemannian Penrose inequality asymptotic end, outermost minimal surface, ADM mass, inverse mean curvature, weak flow, rigidity reservation, and observation firewall", "riemannian-penrose-inequality", "GMUT Mind", "completed", ["SRC-PENROSE-INEQUALITY"], "No frozen row isolates the Riemannian Penrose assumptions, weak inverse-mean-curvature flow, and rigidity reservation."),
    ("GMUT Wheeler-DeWitt superspace, three-metric, Hamiltonian constraint, DeWitt supermetric, factor ordering, inner product, time problem, and observation firewall", "wheeler-dewitt-constraint", "GMUT Mind", "completed", ["SRC-WHEELER-DEWITT"], "No frozen row isolates the Wheeler-DeWitt superspace constraint, factor ordering, inner product, and time problem."),
    ("GMUT Kodama vector spherical orbit space, areal-radius gradient, conserved current, Misner-Sharp relation, trapping horizon, surface-gravity reservation, and observation firewall", "kodama-current-ledger", "GMUT Mind", "completed", ["SRC-KODAMA"], "No frozen row isolates Kodama-current construction and its trapping-horizon and surface-gravity reservations."),
    ("GMUT Gaussian null coordinate horizon section, affine radial coordinate, null generator, shift one-form, transverse metric, residual gauge, near-horizon limit, and observation firewall", "gaussian-null-coordinates", "GMUT Mind", "completed", ["SRC-GAUSSIAN-NULL"], "No frozen row isolates Gaussian-null chart data, residual gauge, and near-horizon limiting obligations."),
    ("GMUT Sachs optical screen space, Jacobi map, deformation matrix, expansion, shear, twist, conjugate point, distance reservation, and observation firewall", "sachs-optical-jacobi-map", "GMUT Mind", "completed", ["SRC-SACHS"], "No frozen row isolates the screen-space Jacobi map, optical deformation matrix, and distance reservation."),
    ("GMUT Newman-Janis null tetrad, complex coordinate step, reality slice, transformed metric, integrability, source stress reservation, algorithm boundary, and observation firewall", "newman-janis-algorithm", "GMUT Mind", "completed", ["SRC-NEWMAN-JANIS"], "No frozen row isolates Newman-Janis complexification, reality-slice, and source-stress reservations."),
    ("GMUT Petrov scalar invariants I and J, Weyl eigenvalue, discriminant, speciality index, tetrad invariance, degeneracy, numerical tolerance, and observation firewall", "petrov-speciality-invariants", "GMUT Mind", "completed", ["SRC-PETROV-SPECIALITY"], "No frozen row isolates the I-J discriminant and speciality-index numerical-degeneracy contract."),
    ("GMUT Ernst stationary axisymmetry, Killing reduction, complex potential, twist potential, elliptic equation, axis regularity, asymptotic boundary, and observation firewall", "ernst-potential-ledger", "GMUT Mind", "completed", ["SRC-ERNST"], "No frozen row isolates Ernst potential construction, axis regularity, and asymptotic-boundary obligations."),
    ("GMUT Geroch two-Killing reduction, orbit metric, scalar potential, twist, hidden symmetry, transformation parameter, reconstruction, and observation firewall", "geroch-solution-transform", "GMUT Mind", "completed", ["SRC-GEROCH"], "No frozen row isolates the Geroch reduced-potential transformation and reconstruction boundary."),
    ("GMUT Taub-NUT mass parameter, NUT charge, fibre periodicity, Misner string, coordinate patch, closed timelike curve, causal reservation, and observation firewall", "taub-nut-boundary", "GMUT Mind", "completed", ["SRC-TAUB-NUT"], "No frozen row isolates Taub-NUT fibre patches, Misner-string handling, and causal reservations."),
    ("GMUT Vaidya null fluid, advanced or retarded coordinate, mass function, null stress tensor, energy-condition sign, apparent horizon, matching reservation, and observation firewall", "vaidya-null-fluid", "GMUT Mind", "completed", ["SRC-VAIDYA"], "No frozen row isolates the Vaidya mass derivative, null-fluid sign, apparent horizon, and matching boundary."),
    ("GMUT McVittie scale factor, central mass, no-accretion condition, isotropic radius, fluid pressure, singular surface, horizon classification, and observation firewall", "mcvittie-expanding-mass", "GMUT Mind", "completed", ["SRC-MCVITTIE"], "No frozen row isolates McVittie no-accretion, singular-surface, and horizon-classification obligations."),
    ("GMUT Robinson-Trautman shear-free null congruence, expansion, twist condition, transverse metric, parabolic equation, mass aspect, asymptotic limit, and observation firewall", "robinson-trautman-flow", "GMUT Mind", "completed", ["SRC-ROBINSON-TRAUTMAN"], "No frozen row isolates Robinson-Trautman parabolic evolution and asymptotic-limit reservations."),
    ("THOS mCRL2 process equation, data sort, action, communication, linear process, modal mu calculus, PBES, state budget, and nonpromotion board", "mcrl2-process-algebra", "THOS Body", "completed", ["SRC-MCRL2"], "No frozen row isolates mCRL2 process equations, linearization, modal formulae, and PBES obligations."),
    ("THOS NuSMV module, state variable, initial condition, transition relation, fairness, CTL property, LTL property, counterexample, and nonpromotion board", "nusmv-symbolic-model", "THOS Body", "completed", ["SRC-NUSMV"], "No frozen row isolates NuSMV transition, fairness, CTL, LTL, and counterexample semantics."),
    ("THOS Z notation schema, declaration, predicate, state invariant, operation schema, precondition, schema calculus, type boundary, and nonpromotion board", "z-schema-contract", "THOS Body", "completed", ["SRC-Z"], "No frozen row isolates Z schemas, operation preconditions, schema calculus, and type boundaries."),
    ("THOS VDM state, type invariant, precondition, postcondition, operation, explicit function, implicit function, proof obligation, and nonpromotion board", "vdm-state-contract", "THOS Body", "completed", ["SRC-VDM"], "No frozen row isolates VDM state, explicit and implicit definitions, and proof-obligation boundaries."),
    ("THOS LOTOS process, event gate, behaviour expression, choice, synchronization, hiding, data type, observational trace, and nonpromotion board", "lotos-behaviour-contract", "THOS Body", "completed", ["SRC-LOTOS"], "No frozen row isolates LOTOS gate events, synchronization, hiding, abstract data, and observable traces."),
    ("THOS CEGAR concrete system, abstraction map, abstract property, counterexample, feasibility check, spurious trace, refinement, termination reservation, and nonpromotion board", "cegar-refinement-loop", "THOS Body", "completed", ["SRC-CEGAR"], "No frozen row isolates the concrete-abstraction counterexample-feasibility-refinement loop and termination reservation."),
    ("THOS Bowtie hazard, top event, threat, preventive barrier, consequence, recovery barrier, escalation factor, control owner, and professional-review proxy", "bowtie-barrier-map", "THOS Body", "represented", ["SRC-BOWTIE"], "No frozen row isolates a Bowtie threat-to-consequence barrier map while explicitly reserving professional control review."),
    ("THOS LOPA cause-consequence scenario, initiating event, enabling condition, independent protection layer, probability of failure on demand, conditional modifier, residual risk, and professional-review proxy", "lopa-protection-layer", "THOS Body", "represented", ["SRC-LOPA"], "No frozen row isolates LOPA independence, layer-credit, conditional-modifier, and residual-risk reservations."),
    ("Freed ID SCRAM SHA-256 username, nonce, salt, iteration count, channel binding, client proof, server signature, transcript, and nonproduction profile", "scram-sha256-profile", "Freed ID/CBR Heart", "represented", ["SRC-SCRAM"], "No frozen row isolates SCRAM-SHA-256 nonce, salted transcript, channel-binding, proof, and server-signature fields."),
    ("Freed ID Kerberos FAST armor, armor key, inner request, outer request, strengthen key, finished checksum, downgrade policy, replay nonce, and nonproduction profile", "kerberos-fast-profile", "Freed ID/CBR Heart", "represented", ["SRC-KERBEROS-FAST"], "No frozen row isolates Kerberos FAST armor, inner-outer binding, strengthen-key, finished-checksum, and downgrade obligations."),
    ("Freed ID X.509 proxy certificate issuer, subject, proxy path length, proxy policy, key usage, validity interval, chain verification, delegation boundary, and nonproduction profile", "x509-proxy-certificate", "Freed ID/CBR Heart", "represented", ["SRC-PROXY-CERT"], "No frozen row isolates RFC 3820 proxy path-length, policy, delegation, and chain obligations."),
    ("GMUT MeerKAT science-archive observation, proposal provenance, target, frequency setup, visibility product, calibration lineage, quality flag, checksum, covariance, and zero-row likelihood-refusal adapter", "meerkat-zero-row-adapter", "GMUT Mind", "open_gap", ["SRC-MEERKAT-ARCHIVE", "SRC-MEERKAT-UPDATE"], "No frozen row isolates the MeerKAT archive visibility-product and calibration-lineage zero-row contract."),
    ("CBR emergency mobile alert hazard authority, geotargeting, message language, accessibility alternative, delivery limitation, correction, appeal, affected-party review, iwi and hapū data governance, and Māori-authority reservation", "emergency-alert-authority-matrix", "Freed ID/CBR Heart", "exact_gate", ["SRC-NEMA-EMA", "SRC-WCAG22", "SRC-MAORI-DATA"], "No frozen row isolates Emergency Mobile Alert authority, accessibility alternatives, correction, affected-party review, and Māori data-governance reservations."),
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
        f"ghc-family-v653-v1-{row['slug']}-review",
        f"Review {row['slug']} contracts, mutation evidence, and nonpromotion boundaries.",
    )
    for row in PROPOSALS[:10]
]

RUNNER_TASKS = [
    f"Build and invoke family-compatible bounded runner {index:02d} for {row['slug']}."
    for index, row in enumerate(PROPOSALS[:10], 1)
]

RUNNER_IDEAS = [
    (
        f"ghc_family_v653_v1_runner_{index:02d}.py",
        row["slug"],
    )
    for index, row in enumerate(PROPOSALS[:10], 1)
]

CLEAN_FIX_REFINE_TASKS = [
    f"REFINE-{index:02d}: review {row['slug']} terminology, falsifier, rollback, and protected-gate wording without changing its frozen outcome class."
    for index, row in enumerate(PROPOSALS, 1)
]

X1_NEGATIVES = [
    ("V6531-X1-N01", "whole_baton_display_truncation", "The first whole-file baton display was truncated before EOF and earned no read credit.", "Read numbered bounded chunks, verify the final line, and compare the working file to the exact Git blob."),
    ("V6531-X1-N02", "powershell_foreach_pipeline_parse", "A PowerShell probe piped a bare foreach statement and failed with an empty-pipe parser error before any Git command ran.", "Materialize foreach output in an array before piping it."),
    ("V6531-X1-N03", "owner_manifest_working_bytes_assumption", "The first owner-manifest audit incorrectly compared working_bytes with filtered Git-blob length and reported twelve false mismatches.", "Use the committed owner-manifest contract: exact path coverage, exclusions, and Git-blob identity."),
    ("V6531-X1-N04", "hashtable_subexpression_parse", "A source-target probe embedded statement lists in a hashtable expression and failed to parse before Git ran.", "Compute command exit states in separate variables before constructing the object."),
    ("V6531-X1-N05", "worktree_add_wrapper_timeout", "The additive worktree wrapper timed out while the checkout and a read-only remote child continued.", "Inspect the target, branch, exact head, registration, and surviving process before any retry."),
    ("V6531-X1-N06", "post_timeout_combined_audit_timeout", "The first combined post-timeout worktree audit also exceeded its wrapper and earned no state-verification credit.", "Use short exact filesystem, process, head, branch, and clean-state probes."),
    ("V6531-X1-N07", "git_inspection_blocked_by_orphan", "A direct Git head, branch, and status inspection timed out while an orphaned read-only git remote child remained.", "Identify the dead-parent child, stop only that owned orphan, then rerun bounded Git plumbing."),
    ("V6531-X1-N08", "windows_path_separator_registration_assumption", "The first registration check compared backslash and forward-slash paths literally and falsely reported the lane unregistered.", "Normalize path separators or match the exact worktree basename and branch tuple."),
    ("V6531-X1-N09", "whole_frozen_index_serialization_overload", "A schema probe serialized the full 1,420-row index and produced an overlarge truncated display with no complete review credit.", "Select top-level counts and bounded rows instead of serializing the whole index."),
    ("V6531-X1-N10", "powershell_foreach_pipeline_recurrence", "A later line-count probe repeated the bare-foreach pipeline parse failure.", "Promote the array-materialization method as a recurrence guard and use it for every later loop pipeline."),
    ("V6531-X1-N11", "windows_rg_wildcard_path", "An rg command placed Windows wildcards inside absolute path arguments and failed with an invalid filename error.", "Search directories with rg -g include globs instead of wildcard path arguments."),
    ("V6531-X1-N12", "premature_x2_scaffold_creation", "A mechanical clone created untracked x2 scripts and tests before the x1 freeze gate.", "Delete only the new untracked Vesper scaffolds, retain the failure, and recreate them only after x1 is committed, pushed, clean, and remote-equal."),
    ("V6531-X1-N13", "per_file_git_validator_timeout", "The combined stage-and-validate wrapper timed out while the x1 validator spawned repeated per-file Git subprocesses; the attempt earned zero credit.", "Replace per-path Git reads with one staged-index map and one git cat-file --batch stream, then regenerate receipts against the same intended x1 scope."),
    ("V6531-X1-N14", "orphan_exit_race", "A read-only validator process exited between orphan inspection and the attempted targeted stop, producing a no-such-process recovery race.", "Recheck process existence after inspection and treat an already-exited owned process as quiescent without retrying a stop."),
]

REJECTED_COLLISIONS = [
    "Cartan-Karlhede collided with a frozen Cartan-Karlhede equivalence board.",
    "Geroch-Held-Penrose collided with a frozen GHP calculus board.",
    "Raychaudhuri collided with a frozen focusing board.",
    "Bondi-Sachs collided with a frozen asymptotic-news board.",
    "Iyer-Wald collided with a frozen covariant phase-space board.",
    "Einstein-Cartan collided with a frozen torsion board.",
    "BSSN collided with a frozen conformal-evolution board.",
    "Ashtekar-Barbero collided with a frozen canonical-variable board.",
    "Bel-Robinson collided with a frozen superenergy board.",
    "Gibbons-Hawking-York collided with a frozen boundary-action board.",
    "Brown-York collided with a frozen quasilocal-stress board.",
    "Isaacson collided with a frozen high-frequency averaging board.",
    "Horndeski, Vainshtein, DHOST, and Galileon each collided with frozen mechanism-specific boards.",
    "TLA+, Promela, Petri nets, CSP, CRDT, UPPAAL, PRISM, Event-B, Alloy, and ioco each collided with frozen formal-method rows.",
    "HPKE, OHTTP, CWT, RATS, SD-JWT, MLS, Privacy Pass, OPAQUE, VOPRF, and ML-KEM each collided with frozen identity or cryptographic rows.",
    "DESI, Euclid, LHAASO, IceCube, CHIME/FRB, Rubin, LoTSS, EHT, and Suzaku each collided with frozen zero-row data adapters.",
]
