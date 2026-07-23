#!/usr/bin/env python3
"""Frozen Elaren Kestrel v652-v7 x1 data.

This module contains preregistration inputs only.  It deliberately contains no
x2 observations, mutation outcomes, completion receipts, or route result.
"""

from __future__ import annotations


PHASE = "v652-v7"
PHASE_ID = "v652-gmut-thos-v7-x1-x2"
OWNER = "Elaren Kestrel"
PRONOUNS = "they/them"
ROLE = "evidence-boundary steward and formal-method cartographer"
HOPE = (
    "make mathematically ambitious work easier to falsify while keeping every "
    "human, empirical, cultural, and production boundary unmistakable"
)
PHASE_ROOT = "docs/elaren-kestrel/v652-v7"
BRANCH = "codex/GHC-Family/elaren-kestrel-v649-v8-full-tools"

SOURCE_BRANCH = "codex/GHC-Family/tavian-sol-v652-v6-cli"
SOURCE_HEAD = "0fe800ea74d17f984497b496cd0ce2253ade9066"
SOURCE_X1 = "9e5074cd42a0fdcbc342980c1960c15a30abe28f"
SOURCE_EVIDENCE = "58b0ecfd1af72ba4cdee5657a87275747bbcbe0a"
SOURCE_CLOSEOUT = "bdb02fbe63e189700b915e18c45bc00b80e5aaeb"
SOURCE_CORRECTION_1 = "6c6e491e5f1163979879865ce820ea718ed94084"
SOURCE_CORRECTION_2 = "276839c87de60f44843df3f01fb1af7b411aa664"
SOURCE_PARENT = "ad2a2e472c8e859296e62f1d2d6ce1f9f2b2b584"

PRIOR_FROZEN = 1360
INHERITED_NEGATIVES = 8917
INHERITED_OPEN_GAPS = 67
INHERITED_EXACT_GATES = 68
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
    source("SRC-HORNDESKI", "stable", "primary_paper", "Second-order scalar-tensor field equations in a four-dimensional space", "https://www.osti.gov/biblio/4212566", "Supports a symbolic four-sector obligation ledger; it is not empirical confirmation."),
    source("SRC-ATIYAH-SINGER", "stable", "primary_paper", "The index of elliptic operators III", "https://annals.math.princeton.edu/1968/87-3/p05", "Supports an ellipticity and index bookkeeping contract only."),
    source("SRC-CALLAN-HARVEY", "stable", "primary_paper", "Anomalies and fermion zero modes on strings and domain walls", "https://doi.org/10.1016/0550-3213(85)90489-4", "Supports a synthetic anomaly-inflow consistency board only."),
    source("SRC-WESS-ZUMINO", "stable", "primary_paper", "Consequences of anomalous Ward identities", "https://cds.cern.ch/record/486885", "Supports formal consistency relations, not a new physical anomaly claim."),
    source("SRC-TEUKOLSKY", "stable", "primary_paper", "Perturbations of a rotating black hole", "https://www.osti.gov/biblio/4318110", "Supports typed perturbation variables and boundary reservations only."),
    source("SRC-CHANDRASEKHAR", "stable", "primary_paper", "On the equations governing the perturbations of the Schwarzschild black hole", "https://doi.org/10.1098/rspa.1975.0066", "Supports a symbolic intertwining-map contract, not a new black-hole solution."),
    source("SRC-FEFFERMAN-GRAHAM", "stable", "author_manuscript", "The ambient metric", "https://arxiv.org/abs/0710.0919", "Supports asymptotic-expansion bookkeeping with explicit obstruction reservations."),
    source("SRC-ISOLATED-HORIZON", "stable", "primary_manuscript", "Generic isolated horizons and their applications", "https://arxiv.org/abs/gr-qc/0006006", "Supports a bounded null-boundary obligation ledger."),
    source("SRC-DYNAMICAL-HORIZON", "stable", "primary_manuscript", "Dynamical horizons and their properties", "https://arxiv.org/abs/gr-qc/0207080", "Supports a bounded flux-law structure without observational promotion."),
    source("SRC-ADT", "stable", "primary_manuscript", "Conserved charges in extended theories of gravity", "https://arxiv.org/abs/1010.1711", "Supports a background-charge accounting contract only."),
    source("SRC-HAWKING-MASS", "stable", "primary_paper", "Gravitational radiation in an expanding universe", "https://www.osti.gov/biblio/4501833", "Supports quasilocal-mass inputs and assumption reservations."),
    source("SRC-PLEBANSKI", "stable", "primary_paper", "On the separation of Einsteinian substructures", "https://doi.org/10.1063/1.523215", "Supports a BF and simplicity-constraint ledger with sector reservations."),
    source("SRC-BCJ", "stable", "primary_manuscript", "New relations for gauge-theory amplitudes", "https://arxiv.org/abs/0805.3993", "Supports symbolic color-kinematics identities and a loop reservation."),
    source("SRC-FIERZ-PAULI", "stable", "primary_paper", "On relativistic wave equations for particles of arbitrary spin in an electromagnetic field", "https://doi.org/10.1098/rspa.1939.0140", "Supports a free-field constraint ledger; no massive-gravity empirical claim follows."),
    source("SRC-CELESTIAL", "stable", "primary_manuscript", "A conformal basis for flat space amplitudes", "https://arxiv.org/abs/1705.01027", "Supports Mellin-basis bookkeeping only."),
    source("SRC-MEMORY", "stable", "primary_manuscript", "Gravitational memory, BMS supertranslations and soft theorems", "https://arxiv.org/abs/1411.5745", "Supports a symbolic memory-observable ledger without detector data."),
    source("SRC-RELATIONAL", "stable", "primary_manuscript", "Partial observables", "https://arxiv.org/abs/gr-qc/0110035", "Supports a relational-observable contract without ontology or consciousness claims."),
    source("SRC-TLA", "current", "authoritative_author_site", "The Temporal Logic of Actions", "https://lamport.org/pubs/lamport-actions.pdf", "Supports finite formal-specification witnesses, not deployed-system assurance."),
    source("SRC-SPIN", "current", "official_tool_documentation", "SPIN model checker manual", "https://spinroot.com/spin/Man/Manual.html", "Supports bounded synthetic Promela and LTL witnesses only."),
    source("SRC-PETRI", "stable", "primary_monograph", "Communication with automata", "https://link.springer.com/book/10.1007/978-3-642-06721-3", "Supports structural place-transition invariants only."),
    source("SRC-CSP", "stable", "primary_paper", "Communicating sequential processes", "https://dl.acm.org/doi/10.1145/359576.359585", "Supports trace and refusal-set modeling without operational deployment credit."),
    source("SRC-CRDT", "stable", "primary_report", "A comprehensive study of convergent and commutative replicated data types", "https://inria.hal.science/inria-00555588", "Supports a finite join-semilattice convergence board only."),
    source("SRC-FAULT-TREE", "current", "official_handbook", "Fault Tree Handbook with Aerospace Applications", "https://extapps.ksc.nasa.gov/reliability/Documents/Fault_Tree_Handbook_with_Aerospace_Applications_August_2002.pdf", "Supports qualitative synthetic cut-set analysis without certified reliability."),
    source("SRC-SIMPLEX", "stable", "primary_paper", "The Simplex architecture for safe on-line control system upgrades", "https://doi.org/10.1109/ACC.1998.703255", "Supports a represented runtime-assurance handover proxy only."),
    source("SRC-STPA", "current", "official_handbook", "STPA Handbook", "https://psas.scripts.mit.edu/home/books-and-handbooks/", "Supports a represented synthetic hazard-analysis proxy; no professional safety review."),
    source("SRC-PASETO", "draft", "internet_draft", "PASETO v3 and v4 draft specification", "https://www.ietf.org/archive/id/draft-paragon-paseto-rfc-01.html", "Draft/watch material supports a nonproduction syntax profile only."),
    source("SRC-PRIVACY-PASS-ARCH", "current", "official_rfc", "RFC 9576 Privacy Pass Architecture", "https://www.rfc-editor.org/rfc/rfc9576.html", "Supports a nonproduction role and context profile with privacy reservations."),
    source("SRC-PRIVACY-PASS-HTTP", "current", "official_rfc", "RFC 9577 Privacy Pass HTTP Authentication Scheme", "https://www.rfc-editor.org/rfc/rfc9577.html", "Supports synthetic token-challenge and redemption fields only."),
    source("SRC-SPAKE2", "current", "official_rfc", "RFC 9382 SPAKE2", "https://www.rfc-editor.org/rfc/rfc9382.html", "Supports a nonproduction transcript-binding profile; real keys and interoperability remain gated."),
    source("SRC-EHT-DATA", "current", "official_data_portal", "Event Horizon Telescope data products", "https://eventhorizontelescope.org/for-astronomers/data", "Identifies the official data boundary; this phase performs no download or fit."),
    source("SRC-EHT-CAL", "stable", "primary_collaboration_paper", "First M87 Event Horizon Telescope Results III: Data Processing and Calibration", "https://arxiv.org/abs/1906.11240", "Defines visibility and calibration provenance fields for a zero-row adapter."),
    source("SRC-NZ-AIA", "current", "official_government_guidance", "Algorithm Impact Assessment toolkit", "https://data.govt.nz/toolkit/data-ethics/government-algorithm-transparency-and-accountability/algorithm-impact-assessment-toolkit", "Supports notice and contestability prompts without making legal decisions."),
    source("SRC-MAORI-DATA", "current", "maori_authority_guidance", "Indigenous Data Sovereignty, AI and Algorithms", "https://www.temanararaunga.maori.nz/indigenous-data-sovereignty-ai-algorithms", "Keeps Māori data and algorithmic authority with Māori authorities."),
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
        "proposal_id": f"V6527-P{number:02d}",
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
        "novelty_against_1360_frozen_proposals": novelty,
    }


PROPOSAL_SPECS = [
    ("GMUT Horndeski four-sector Lagrangian, derivative self-coupling, second-order field equations, degeneracy boundary, stability reservation, unit ledger, and observation firewall", "horndeski-four-sector", "GMUT Mind", "completed", ["SRC-HORNDESKI"], "No frozen row isolates the four Horndeski sectors together with second-order and stability reservations."),
    ("GMUT Atiyah-Singer elliptic operator, principal symbol, index, kernel, cokernel, characteristic class, compactness boundary, unit ledger, and observation firewall", "atiyah-singer-index", "GMUT Mind", "completed", ["SRC-ATIYAH-SINGER"], "No frozen row binds ellipticity, analytic index, topological index, and compactness as one contract."),
    ("GMUT Callan-Harvey bulk current, Chern-Simons term, boundary chiral mode, descent relation, orientation, regulator reservation, and observation firewall", "callan-harvey-inflow", "GMUT Mind", "completed", ["SRC-CALLAN-HARVEY"], "No frozen row isolates bulk-boundary anomaly inflow and its orientation and regulator boundaries."),
    ("GMUT Wess-Zumino variation algebra, anomaly functional, local counterterm, cohomology class, gauge parameter, regulator reservation, and observation firewall", "wess-zumino-consistency", "GMUT Mind", "completed", ["SRC-WESS-ZUMINO"], "No frozen row isolates the consistency commutator and counterterm/cohomology distinction."),
    ("GMUT Teukolsky master variable, spin weight, null tetrad, separability, radial and angular equations, source term, boundary reservation, and observation firewall", "teukolsky-master", "GMUT Mind", "completed", ["SRC-TEUKOLSKY"], "No frozen row isolates the spin-weighted master-variable and tetrad/separability obligations."),
    ("GMUT Chandrasekhar Regge-Wheeler potential, Teukolsky variable, intertwining map, normalization, frequency domain, boundary reservation, and observation firewall", "chandrasekhar-intertwiner", "GMUT Mind", "completed", ["SRC-CHANDRASEKHAR"], "Earlier RWZ rows do not isolate the Chandrasekhar intertwining map and normalization boundary."),
    ("GMUT Fefferman-Graham radial coordinate, boundary metric, asymptotic expansion, obstruction term, conformal anomaly reservation, counterterm, and observation firewall", "fefferman-graham-expansion", "GMUT Mind", "completed", ["SRC-FEFFERMAN-GRAHAM"], "No frozen row isolates radial expansion order, obstruction, counterterm, and anomaly reservation."),
    ("GMUT isolated-horizon null normal, expansion condition, intrinsic connection, surface-gravity class, area charge, boundary reservation, and observation firewall", "isolated-horizon", "GMUT Mind", "completed", ["SRC-ISOLATED-HORIZON"], "No frozen row isolates weakly isolated null-boundary equivalence classes and intrinsic connection data."),
    ("GMUT dynamical-horizon spacelike foliation, marginal surface, area flux, shear flux, matter flux, signature-transition reservation, and observation firewall", "dynamical-horizon", "GMUT Mind", "completed", ["SRC-DYNAMICAL-HORIZON"], "No frozen row isolates spacelike marginal foliations and separate shear and matter flux terms."),
    ("GMUT Abbott-Deser-Tekin background Killing vector, linearized curvature, conserved current, antisymmetric potential, asymptotic charge, and observation firewall", "abbott-deser-tekin", "GMUT Mind", "completed", ["SRC-ADT"], "No frozen row isolates ADT background symmetry, linearized current, potential, and asymptotic charge."),
    ("GMUT Hawking quasilocal mass, surface area, null expansions, normalization, topology, monotonicity assumptions, foliation reservation, and observation firewall", "hawking-quasilocal-mass", "GMUT Mind", "completed", ["SRC-HAWKING-MASS"], "No frozen row isolates Hawking mass inputs with topology, foliation, and monotonicity reservations."),
    ("GMUT Plebanski BF two-form, connection curvature, simplicity constraint, sector choice, orientation, reality-condition reservation, and observation firewall", "plebanski-bf", "GMUT Mind", "completed", ["SRC-PLEBANSKI"], "No frozen row isolates the BF action, simplicity constraint, sector choice, orientation, and reality boundary."),
    ("GMUT color-kinematics cubic graph, color Jacobi, kinematic Jacobi, generalized-gauge freedom, double-copy map, loop reservation, and observation firewall", "color-kinematics", "GMUT Mind", "completed", ["SRC-BCJ"], "No frozen row isolates paired color and kinematic Jacobi identities with generalized-gauge freedom."),
    ("GMUT Fierz-Pauli symmetric tensor, kinetic operator, mass term, trace constraint, divergence constraint, ghost reservation, unit ledger, and observation firewall", "fierz-pauli", "GMUT Mind", "completed", ["SRC-FIERZ-PAULI"], "No frozen row isolates the free symmetric-tensor mass term with trace, divergence, and ghost reservations."),
    ("GMUT celestial amplitude Mellin transform, conformal dimension, celestial coordinate, Lorentz covariance, soft current, inversion reservation, and observation firewall", "celestial-amplitude", "GMUT Mind", "completed", ["SRC-CELESTIAL"], "No frozen row isolates the Mellin conformal basis and inversion boundary for amplitudes."),
    ("GMUT gravitational-memory early shear, late shear, news integral, detector displacement, gauge frame, nonlinear-contribution reservation, and observation firewall", "gravitational-memory", "GMUT Mind", "completed", ["SRC-MEMORY"], "Bondi and soft rows do not isolate a falsifiable early/late memory and detector-displacement ledger."),
    ("GMUT relational observable, clock field, reference field, gauge orbit, complete observable, locality reservation, quantum-correction reservation, and observation firewall", "relational-observable", "GMUT Mind", "completed", ["SRC-RELATIONAL"], "No frozen row isolates partial/complete observables with clock/reference fields and locality reservations."),
    ("THOS TLA action relation, state variable, invariant, temporal liveness, fairness assumption, stuttering, finite-model boundary, and nonpromotion board", "tla-action-model", "THOS Body", "completed", ["SRC-TLA"], "No frozen row isolates TLA actions, stuttering, fairness, invariant, and liveness as a bounded board."),
    ("THOS Promela channel, process interleaving, atomic region, LTL claim, never claim, partial-order reduction, state-budget boundary, and nonpromotion board", "promela-spin", "THOS Body", "completed", ["SRC-SPIN"], "No frozen row isolates Promela interleavings and SPIN reduction and never-claim obligations."),
    ("THOS Petri-net place, transition, incidence matrix, marking, reachability, siphon, trap, boundedness, and nonpromotion board", "petri-net", "THOS Body", "completed", ["SRC-PETRI"], "No frozen row isolates incidence, marking, reachability, siphon, trap, and boundedness together."),
    ("THOS CSP trace, refusal set, divergence, failures-divergences refinement, hiding, synchronization, finite-state boundary, and nonpromotion board", "csp-refinement", "THOS Body", "completed", ["SRC-CSP"], "No frozen row isolates failures-divergences refinement with hiding and synchronization."),
    ("THOS CRDT join-semilattice, inflation, merge, causal context, concurrent update, convergence, tombstone budget, and nonpromotion board", "crdt-semilattice", "THOS Body", "completed", ["SRC-CRDT"], "Earlier OR-set rows do not isolate the general state-based join-semilattice convergence contract."),
    ("THOS fault-tree top event, basic event, AND and OR gates, minimal cut set, common-cause reservation, probability unit, and nonpromotion board", "fault-tree", "THOS Body", "completed", ["SRC-FAULT-TREE"], "No frozen row isolates fault-tree logic, minimal cut sets, common causes, and probability-unit reservation."),
    ("THOS Simplex advanced controller, safety controller, decision module, recoverable region, switch latency, workload, and handover proxy", "simplex-runtime-assurance", "THOS Body", "represented", ["SRC-SIMPLEX"], "No frozen row isolates the three-part Simplex switching contract and recoverable-region boundary."),
    ("THOS STPA loss, system hazard, control action, process model, unsafe control action, causal scenario, review authority, and handover proxy", "stpa-hazard-analysis", "THOS Body", "represented", ["SRC-STPA"], "No frozen row isolates the full STPA loss-to-causal-scenario chain as a proxy."),
    ("Freed ID PASETO version, purpose, protocol header, payload, footer, implicit assertion, nonce, key separation, and nonproduction profile", "paseto-profile", "Freed ID and CBR Heart", "represented", ["SRC-PASETO"], "No frozen row isolates PASETO version/purpose separation and implicit-assertion binding."),
    ("Freed ID Privacy Pass token type, challenge, nonce, issuance context, authenticator input, redemption context, unlinkability reservation, and nonproduction profile", "privacy-pass-profile", "Freed ID and CBR Heart", "represented", ["SRC-PRIVACY-PASS-ARCH", "SRC-PRIVACY-PASS-HTTP"], "No frozen row isolates Privacy Pass issuance/redemption context separation and token challenge."),
    ("Freed ID SPAKE2 group, identities, password scalar, masking points, confirmation, transcript binding, side-channel reservation, and nonproduction profile", "spake2-profile", "Freed ID and CBR Heart", "represented", ["SRC-SPAKE2"], "No frozen row isolates SPAKE2 masking points, identity binding, confirmation, and transcript fields."),
    ("GMUT Event Horizon Telescope visibility amplitude, closure phase, station metadata, calibration provenance, covariance, imaging prior, and zero-row likelihood-refusal adapter", "eht-zero-row", "GMUT Mind", "open_gap", ["SRC-EHT-DATA", "SRC-EHT-CAL"], "No frozen adapter targets EHT visibility and closure quantities with station and calibration provenance."),
    ("CBR algorithmic-impact notice, affected-party standing, explanation, contest, remedy, audit access, beneficiary privacy, iwi, hapū, and Māori-authority reservation", "algorithmic-impact-authority", "Freed ID and CBR Heart", "exact_gate", ["SRC-NZ-AIA", "SRC-MAORI-DATA"], "No frozen gate isolates algorithmic notice, contest, remedy, beneficiary privacy, and Māori algorithmic authority together."),
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

SKILL_IDEAS = [
    ("ghc-family-horndeski-sector-audit", "Audit symbolic Horndeski sector and derivative-order obligations."),
    ("ghc-family-anomaly-inflow-audit", "Audit bulk-boundary anomaly-inflow and consistency ledgers."),
    ("ghc-family-horizon-flux-audit", "Audit isolated/dynamical horizon boundary and flux fields."),
    ("ghc-family-perturbation-intertwiner-audit", "Audit Teukolsky and Chandrasekhar map obligations."),
    ("ghc-family-formal-model-audit", "Audit TLA, Promela, Petri, CSP, and CRDT finite-model boundaries."),
    ("ghc-family-runtime-assurance-audit", "Audit Simplex and STPA proxy/nonpromotion boundaries."),
    ("ghc-family-identity-protocol-audit", "Audit PASETO, Privacy Pass, and SPAKE2 nonproduction profiles."),
    ("ghc-family-eht-zero-row-audit", "Audit EHT zero-row refusal and provenance requirements."),
    ("ghc-family-algorithmic-authority-audit", "Audit notice, contest, remedy, privacy, and authority reservations."),
    ("ghc-family-v652-v7-lifecycle-audit", "Audit x1/x2 separation, manifests, privacy, ancestry, and route state."),
]

RUNNER_IDEAS = [
    ("ghc_family_horndeski_sector_audit.py", "horndeski-four-sector"),
    ("ghc_family_anomaly_inflow_audit.py", "wess-zumino-consistency"),
    ("ghc_family_horizon_flux_audit.py", "dynamical-horizon"),
    ("ghc_family_perturbation_intertwiner_audit.py", "chandrasekhar-intertwiner"),
    ("ghc_family_formal_model_audit.py", "tla-action-model"),
    ("ghc_family_runtime_assurance_audit.py", "simplex-runtime-assurance"),
    ("ghc_family_identity_protocol_audit.py", "privacy-pass-profile"),
    ("ghc_family_eht_zero_row_audit.py", "eht-zero-row"),
    ("ghc_family_algorithmic_authority_audit.py", "algorithmic-impact-authority"),
    ("ghc_family_v652_v7_validation_runner.py", "phase-validation"),
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
    ("V6527-X1-N01", "combined_skill_inventory_timeout", "The combined skill-directory inventory exceeded its bounded wrapper and returned no usable output.", "Use exact known skill paths and bounded reads."),
    ("V6527-X1-N02", "broad_tavian_manifest_search_timeout", "A broad multi-root manifest-total search exceeded its bounded wrapper.", "Use the exact committed validator and manifest contract files."),
    ("V6527-X1-N03", "windows_wildcard_path_error", "A narrowed native search passed a wildcard as a literal Windows path and failed with operating-system error 123.", "Use rg include globs with -g instead of wildcard path arguments."),
    ("V6527-X1-N04", "guessed_method_flow_filename", "The first truth probe guessed a nonexistent Method Flow state filename.", "Enumerate the exact phase Method Flow directory before parsing its terminal ledger."),
    ("V6527-X1-N05", "frozen_chain_schema_assumption", "The first novelty probe assumed a generic rows key and reported zero inherited proposals.", "Read prior_proposals and new_proposals from the exact frozen-chain schema."),
    ("V6527-X1-N06", "candidate_collision_screen", "Ten attractive candidate mechanisms collided with frozen Einstein-Cartan, BSSN, Raychaudhuri, GHY, Palatini, Iyer-Wald, soft-graviton, SD-JWT, OpenID4VP, or GWOSC rows.", "Retain the rejected candidates and freeze only mechanism-distinct replacements."),
    ("V6527-X1-N07", "combined_repository_inventory_timeout", "A combined phase/script/test/status inventory exceeded its bounded wrapper.", "Split exact Git state from bounded rg file inventories."),
    ("V6527-X1-N08", "quick_validator_help_probe", "The skill quick-validator does not implement --help and treated it as a skill path, returning SKILL.md not found.", "Invoke quick_validate.py only with an exact initialized skill directory."),
    ("V6527-X1-N09", "guessed_witness_filenames", "A Method Flow example read guessed witness filenames ending in fail/pass rather than failed/passing.", "Enumerate the exact requests directory before reading witnesses."),
    ("V6527-X1-N10", "inherited_identifier_uniqueness_assumption", "The first x1 build required global uniqueness of inherited proposal identifiers and stopped when it found twenty v6513 identifiers reused twice in otherwise title-distinct historical rows.", "Preserve all 1,360 inherited rows byte-for-byte, bind novelty to row title and reported nearest identifier, and disclose the historical identifier multiplicity without rewriting history."),
    ("V6527-X1-N11", "workflow_policy_schema_lag", "The first workflow-refinement run returned three policy errors because the request used a zero baton minimum, a newer C-drive wording, and the live-authorized new-main-task route that the installed runner does not model.", "Align noncontroversial baton and storage fields, preserve the runner's remaining new-task policy mismatch as needs_refinement, and bind the live activation separately without claiming the older tool validated task creation."),
    ("V6527-X1-N12", "multi_hunk_patch_context_rejection", "The first combined workflow-policy correction patch was rejected atomically because one context block did not match its current ordering.", "Read exact current lines and apply smaller reviewed hunks; grant no credit to the rejected patch."),
    ("V6527-X1-N13", "version_receipt_private_path_hit", "The first exact staged privacy scan found one private-absolute-path hit in the environment version receipt because the Python command label serialized its executable path.", "Keep the observed version output but reduce command labels to executable basenames and public argument labels."),
    ("V6527-X1-N14", "non_fail_fast_staged_validation_wrapper", "The combined staged-validation wrapper continued after the first privacy-blocked validator and invoked the same blocked state twice more; all three invocations earned zero credit.", "Run staged validation fail-fast after isolating the first sanitized finding, and do not chain later lifecycle steps behind a failing validator."),
]

REJECTED_COLLISIONS = [
    "Einstein-Cartan torsion mechanism collided with V6524-P13.",
    "BSSN evolution mechanism collided with V6514-P04.",
    "Raychaudhuri congruence mechanism collided with V6522-P08.",
    "Gibbons-Hawking-York mechanism collided with V6522-P06.",
    "Palatini first-order mechanism collided with V6522-P07.",
    "Iyer-Wald charge mechanism collided with V6481-P02.",
    "Soft-graviton mechanism collided with V6518-P04.",
    "SD-JWT mechanism collided with V6443-P05.",
    "OpenID4VP mechanism collided with V6511-P09.",
    "GWOSC data adapter mechanism collided with V6468-P03.",
]
