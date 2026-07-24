#!/usr/bin/env python3
"""Frozen Orin Thale v653-v7 x1 data.

This module contains preregistration inputs only. It deliberately contains no
x2 observations, mutation outcomes, completion receipts, or route result.
"""

from __future__ import annotations


PHASE = "v653-v7"
PHASE_ID = "v653-gmut-thos-v7-x1-x2"
OWNER = "Orin Thale"
PRONOUNS = "they/them"
ROLE = "relational boundary-and-method steward"
HOPE = "keep every surviving claim inspectable, challengeable, and retractable"
PHASE_ROOT = "docs/orin-thale/v653-v7"
BRANCH = "codex/GHC-Family/orin-thale-v653-v7-full-tools"

SOURCE_BRANCH = "codex/GHC-Family/caelen-ash-v653-v6-full-tools"
SOURCE_PARENT = "8cfda9ac9ac86d186346b473795e7bfb045effa0"
SOURCE_X1 = "5be148f1171a449550ce73dd524cb866db7632e3"
SOURCE_EVIDENCE = "17dc9cc858ec2366d25b4b85b8bf85f3f792c8db"
SOURCE_HEAD = "c044464ed940093d59a59686efd4faa61853f341"

PRIOR_FROZEN = 1600
INHERITED_NEGATIVES = 10279
EXTERNAL_POST_SEAL_NEGATIVES = 1
ACTIVATION_NEGATIVE_BASELINE = 10280
INHERITED_OPEN_GAPS = 75
INHERITED_EXACT_GATES = 76
INHERITED_METHOD_FLOW_FAILED = 18
INHERITED_METHOD_FLOW_PASSING = 18
PRIMARY_FOCUS = "GMUT Mind"
BOUNDED_PRACTICE = (
    "municipal traffic-signal timing change control, fault isolation, "
    "accessible road-user notice, workload control, correction readback, "
    "and shift handover"
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


SOURCE_SPECS = [
    (
        "SRC-WALD-ZOUPAS",
        "stable",
        "primary_research",
        "A General Definition of Conserved Quantities in General Relativity and Other Theories of Gravity",
        "https://arxiv.org/abs/gr-qc/9911095",
        "Supports asymptotic-charge, boundary-flux, and integrability obligations without establishing a physical charge or observation.",
    ),
    (
        "SRC-REGGE-TEITELBOIM",
        "stable",
        "primary_research",
        "Role of Surface Integrals in the Hamiltonian Formulation of General Relativity",
        "https://doi.org/10.1016/0003-4916(74)90404-7",
        "Supports differentiable-generator and surface-term obligations without solving a physical spacetime.",
    ),
    (
        "SRC-ASHTEKAR-STREUBEL",
        "stable",
        "primary_research",
        "Symplectic Geometry of Radiative Modes and Conserved Quantities at Null Infinity",
        "https://doi.org/10.1098/rspa.1981.0109",
        "Supports radiative phase-space and flux obligations without observational or waveform evidence.",
    ),
    (
        "SRC-GEROCH-MULTIPOLE",
        "stable",
        "primary_research",
        "Multipole Moments. II. Curved Space",
        "https://doi.org/10.1063/1.1665427",
        "Supports conformal-completion and recursive multipole obligations without a measured source.",
    ),
    (
        "SRC-HANSEN-MULTIPOLE",
        "stable",
        "primary_research",
        "Multipole moments of stationary space-times",
        "https://doi.org/10.1063/1.1666501",
        "Supports stationary-spacetime mass and angular-momentum multipole obligations without empirical extraction.",
    ),
    (
        "SRC-BEIG-SCHMIDT",
        "stable",
        "primary_research",
        "Einstein's equations near spatial infinity",
        "https://doi.org/10.1007/BF01211056",
        "Supports hyperboloidal expansion, parity, and logarithmic-translation obligations without a physical solution.",
    ),
    (
        "SRC-FRIEDRICH-CFE",
        "stable",
        "primary_research",
        "On the regular and the asymptotic characteristic initial value problem for Einstein's vacuum field equations",
        "https://doi.org/10.1098/rspa.1981.0167",
        "Supports conformal-field-equation and regular-null-infinity obligations without a global-existence proof for GMUT.",
    ),
    (
        "SRC-WALD-ENTROPY",
        "stable",
        "primary_research",
        "Black Hole Entropy is Noether Charge",
        "https://arxiv.org/abs/gr-qc/9307038",
        "Supports Noether-charge entropy obligations without establishing a GMUT black-hole solution or entropy.",
    ),
    (
        "SRC-JKM-AMBIGUITY",
        "stable",
        "primary_research",
        "On Black Hole Entropy",
        "https://arxiv.org/abs/gr-qc/9312023",
        "Supports ambiguity and boost-invariance obligations without selecting a physical entropy functional.",
    ),
    (
        "SRC-BARNICH-BRANDT",
        "stable",
        "primary_research",
        "Covariant theory of asymptotic symmetries, conservation laws and central charges",
        "https://arxiv.org/abs/hep-th/0111246",
        "Supports reducibility-parameter and surface-charge cohomology obligations without a physical central charge.",
    ),
    (
        "SRC-BROWN-HENNEAUX",
        "stable",
        "primary_research",
        "Central charges in the canonical realization of asymptotic symmetries",
        "https://doi.org/10.1007/BF01211590",
        "Supports boundary-condition, charge-algebra, and central-term obligations without an observed AdS system.",
    ),
    (
        "SRC-SORCE-WALD",
        "stable",
        "primary_research",
        "Gedanken Experiments to Destroy a Black Hole. II. Kerr-Newman Black Holes Cannot be Over-Charged or Over-Spun",
        "https://arxiv.org/abs/1707.05862",
        "Supports first- and second-variational identity obligations without a GMUT stability theorem.",
    ),
    (
        "SRC-BERNAL-SANCHEZ",
        "stable",
        "primary_research",
        "Smoothness of time functions and the metric splitting of globally hyperbolic spacetimes",
        "https://arxiv.org/abs/gr-qc/0401112",
        "Supports temporal-function and smooth-splitting obligations without proving the hypothesis for a physical model.",
    ),
    (
        "SRC-GIT-HASH",
        "current",
        "official_documentation",
        "Git hash function transition",
        "https://git-scm.com/docs/hash-function-transition",
        "Supports object-format transition, mapping, and compatibility fixtures without migrating this repository.",
    ),
    (
        "SRC-SQLITE-STRICT",
        "current",
        "official_documentation",
        "SQLite STRICT Tables",
        "https://sqlite.org/stricttables.html",
        "Supports declared datatype, ANY, coercion, and integrity fixtures without touching a canonical database.",
    ),
    (
        "SRC-OPENMETRICS",
        "current",
        "official_standard",
        "OpenMetrics 1.0 Specification",
        "https://prometheus.io/docs/specs/om/open_metrics_spec/",
        "Supports metric-family and exposition-format fixtures without operating a monitoring service.",
    ),
    (
        "SRC-YAML-122",
        "stable",
        "official_standard",
        "YAML 1.2.2 Specification",
        "https://yaml.org/spec/1.2.2/",
        "Supports bounded stream, document, tag, anchor, and alias fixtures without general parser certification.",
    ),
    (
        "SRC-RFC9114",
        "stable",
        "official_standard",
        "RFC 9114 HTTP/3",
        "https://www.rfc-editor.org/rfc/rfc9114.html",
        "Supports synthetic stream, settings, frame, and refusal fixtures without network operation.",
    ),
    (
        "SRC-OPENTYPE-VAR",
        "current",
        "official_standard",
        "OpenType Font Variations Common Table Formats",
        "https://learn.microsoft.com/en-us/typography/opentype/spec/otvarcommonformats",
        "Supports axis, tuple, delta, and bounds fixtures without certifying a production font.",
    ),
    (
        "SRC-RFC7946",
        "stable",
        "official_standard",
        "RFC 7946 The GeoJSON Format",
        "https://www.rfc-editor.org/rfc/rfc7946.html",
        "Supports bounded geometry, coordinate, and precision fixtures without publishing location data.",
    ),
    (
        "SRC-WCAG22",
        "current",
        "official_recommendation",
        "Web Content Accessibility Guidelines 2.2",
        "https://www.w3.org/TR/WCAG22/",
        "Supports structural process-stepper checks while reserving manual and affected-user evaluation.",
    ),
    (
        "SRC-ONSAGER-MACHLUP",
        "stable",
        "primary_research",
        "Fluctuations and Irreversible Processes",
        "https://doi.org/10.1103/PhysRev.91.1505",
        "Supports a typed path-action domain without conversion into psyche, agency, or consciousness claims.",
    ),
    (
        "SRC-TRANSPORTABILITY",
        "stable",
        "primary_research",
        "A general algorithm for deciding transportability of experimental results",
        "https://doi.org/10.1214/14-STS486",
        "Supports structural selection-diagram and transport-formula obligations without participant evidence.",
    ),
    (
        "SRC-FHWA-SIGNALS",
        "current",
        "official_guidance",
        "FHWA Traffic Signal Timing and Operations Strategies",
        "https://ops.fhwa.dot.gov/arterial_mgmt/tst_ops.htm",
        "Supports synthetic timing-plan and operations vocabulary without conferring traffic-control authority.",
    ),
    (
        "SRC-NZTA-TCD",
        "current",
        "official_guidance",
        "Waka Kotahi Traffic control devices manual",
        "https://www.nzta.govt.nz/resources/traffic-control-devices-manual/",
        "Supports New Zealand traffic-control vocabulary while reserving legal, cultural, road-controlling, and Māori authority.",
    ),
    (
        "SRC-RFC9420",
        "stable",
        "official_standard",
        "RFC 9420 The Messaging Layer Security Protocol",
        "https://www.rfc-editor.org/rfc/rfc9420.html",
        "Supports synthetic group-state and epoch fixtures without keys, messages, service operation, or interoperability.",
    ),
    (
        "SRC-RFC9180",
        "stable",
        "official_standard",
        "RFC 9180 Hybrid Public Key Encryption",
        "https://www.rfc-editor.org/rfc/rfc9180.html",
        "Supports synthetic HPKE mode and context fixtures without real key material or production cryptography.",
    ),
    (
        "SRC-VC-JOSE-COSE",
        "current",
        "official_recommendation",
        "W3C Securing Verifiable Credentials using JOSE and COSE",
        "https://www.w3.org/TR/vc-jose-cose/",
        "Supports synthetic media-type, envelope, and validation fields without credentials, keys, or interoperability.",
    ),
    (
        "SRC-BK18",
        "current",
        "official_data_portal",
        "NASA LAMBDA BICEP and Keck Array Data Products",
        "https://lambda.gsfc.nasa.gov/product/bicepkeck/bicep2_prod_table.html",
        "Defines a zero-query, zero-download readiness boundary; citations are not data rows or likelihood evidence.",
    ),
    (
        "SRC-LOCAL-CONTEXTS",
        "current",
        "affected_community_governance",
        "Local Contexts Labels and Notices",
        "https://localcontexts.org/labels/traditional-knowledge-labels/",
        "Requires community-specific traditional-knowledge, access, use, and governance decisions to remain with authorized communities.",
    ),
    (
        "SRC-MAORI-DATA",
        "current",
        "maori_authority_principles",
        "Principles of Māori Data Sovereignty",
        "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
        "Requires Māori data, place, governance, access, interpretation, and remedy decisions to remain with Māori authorities.",
    ),
]

SOURCES = [source(*spec) for spec in SOURCE_SPECS]


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
            "with no operational, production, professional, interoperability, "
            "privacy-complete, credential, key, or authority credit."
        )
    elif disposition == "open_gap":
        approval = "candidate_real_data_and_independent_review_required"
        lane = "x2_zero_row_readiness_only"
        acceptance = (
            "Emit a zero-row refusal with no query, download, ingest, "
            "calibration, fit, likelihood, posterior, prediction, or empirical promotion."
        )
    else:
        approval = (
            "exact_affected_party_professional_legal_cultural_accessibility_"
            "and_maori_authority_required"
        )
        lane = "x2_reservation_matrix_only"
        acceptance = (
            "Emit unresolved decision rights and reservations only; make no "
            "traffic-control, accessibility-complete, privacy, remedy, legal, "
            "cultural, data-governance, Māori-authority, or affected-party decision."
        )
    return {
        "proposal_id": f"V6537-P{number:02d}",
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
        "novelty_against_1600_frozen_proposals": novelty,
    }


PROPOSAL_SPECS = [
    ("GMUT Wald-Zoupas asymptotic symmetry, presymplectic current, boundary potential, flux, counterterm, integrability, covariance, and observation-firewall board", "wald-zoupas-charge-boundary", "GMUT Mind", "completed", ["SRC-WALD-ZOUPAS"], "No frozen row isolates the Wald-Zoupas boundary-potential, flux, counterterm, and integrability mechanism."),
    ("GMUT Regge-Teitelboim Hamiltonian generator, functional differentiability, constraint, asymptotic falloff, parity, surface term, variation, and observation-firewall board", "regge-teitelboim-surface-generator", "GMUT Mind", "completed", ["SRC-REGGE-TEITELBOIM"], "No frozen row isolates differentiable Hamiltonian generators with parity and surface-term obligations."),
    ("GMUT Ashtekar-Streubel null-infinity radiative phase space, shear, news, symplectic form, BMS generator, flux, degeneracy, and observation-firewall board", "ashtekar-streubel-radiative-phase-space", "GMUT Mind", "completed", ["SRC-ASHTEKAR-STREUBEL"], "No frozen row isolates the Ashtekar-Streubel radiative phase space and BMS flux construction."),
    ("GMUT Geroch-Hansen conformal completion, stationary potential, mass moment, angular-momentum moment, recursion, STF projection, translation, and observation-firewall board", "geroch-hansen-multipole-recursion", "GMUT Mind", "completed", ["SRC-GEROCH-MULTIPOLE", "SRC-HANSEN-MULTIPOLE"], "No frozen row isolates the joint Geroch-Hansen stationary multipole recursion and translation scope."),
    ("GMUT Beig-Schmidt spatial-infinity hyperboloid, radial expansion, mass aspect, parity, logarithmic translation, asymptotic constraint, and observation-firewall board", "beig-schmidt-spatial-infinity", "GMUT Mind", "completed", ["SRC-BEIG-SCHMIDT"], "No frozen row isolates Beig-Schmidt hyperboloidal expansion, parity, and logarithmic-translation obligations."),
    ("GMUT Friedrich conformal Einstein equation, conformal factor, rescaled Weyl tensor, gauge source, hyperbolic reduction, null infinity, regularity, and observation-firewall board", "friedrich-conformal-evolution", "GMUT Mind", "completed", ["SRC-FRIEDRICH-CFE"], "No frozen row isolates Friedrich conformal-field-equation variables and regular-null-infinity obligations."),
    ("GMUT Wald Noether-charge entropy, diffeomorphism-covariant Lagrangian, symplectic potential, Noether current, bifurcation surface, binormal, normalization, and observation-firewall board", "wald-noether-entropy", "GMUT Mind", "completed", ["SRC-WALD-ENTROPY"], "No frozen row isolates Wald entropy as a bifurcation-surface Noether-charge obligation board."),
    ("GMUT Jacobson-Kang-Myers entropy ambiguity, exact-form shift, potential ambiguity, boost invariance, horizon slice, field redefinition, stationarity, and observation-firewall board", "jkm-entropy-ambiguity", "GMUT Mind", "completed", ["SRC-JKM-AMBIGUITY"], "No frozen row isolates the JKM exact-form and boost-invariance ambiguity classes together."),
    ("GMUT Barnich-Brandt reducibility parameter, local BRST cohomology, weakly vanishing current, surface form, characteristic cohomology, central extension, and observation-firewall board", "barnich-brandt-surface-cohomology", "GMUT Mind", "completed", ["SRC-BARNICH-BRANDT"], "No frozen row isolates Barnich-Brandt reducibility parameters and characteristic cohomology for surface charges."),
    ("GMUT Brown-Henneaux boundary condition, asymptotic Killing vector, canonical charge, Poisson bracket, central term, Virasoro copy, normalization, and observation-firewall board", "brown-henneaux-central-charge", "GMUT Mind", "completed", ["SRC-BROWN-HENNEAUX"], "No frozen row isolates Brown-Henneaux boundary conditions, two charge algebras, and central-term normalization."),
    ("GMUT Sorce-Wald first variation, second variation, canonical energy, horizon flux, charge balance, stability assumption, matter condition, and observation-firewall board", "sorce-wald-canonical-energy", "GMUT Mind", "completed", ["SRC-SORCE-WALD"], "No frozen row isolates the Sorce-Wald second-order variational identity and canonical-energy assumptions."),
    ("GMUT Bernal-Sanchez global hyperbolicity, Cauchy hypersurface, temporal function, smooth splitting, lapse, causal curve, level set, and observation-firewall board", "bernal-sanchez-cauchy-splitting", "GMUT Mind", "completed", ["SRC-BERNAL-SANCHEZ"], "No frozen row isolates smooth Cauchy temporal functions and metric splitting as a typed premise board."),
    ("Method Flow child-process heartbeat, stale-heartbeat threshold, exit attribution, descendant quiescence, receipt identity, timeout, and evidence-credit tribunal", "method-flow-heartbeat-supervision", "GMUT Mind", "completed", [], "No frozen row isolates child heartbeat, descendant quiescence, and attributable evidence credit in one supervision tribunal."),
    ("Git SHA-1 and SHA-256 object-format identity, domain separation, compatibility mapping, reference storage, transport boundary, collision refusal, and no-migration tribunal", "git-object-format-transition", "GMUT Mind", "completed", ["SRC-GIT-HASH"], "No frozen row isolates Git dual-object-format identity and mapping while explicitly refusing repository migration."),
    ("SQLite STRICT table declaration, datatype name, ANY, coercion refusal, integrity check, schema version, migration boundary, and path-confinement tribunal", "sqlite-strict-type-tribunal", "GMUT Mind", "completed", ["SRC-SQLITE-STRICT"], "No frozen row isolates STRICT datatype names, ANY behavior, coercion, and integrity checks together."),
    ("OpenMetrics 1.0 metric family, HELP, TYPE, UNIT, label set, sample, timestamp, exemplar, EOF, UTF-8, and resource-budget tribunal", "openmetrics-exposition-tribunal", "GMUT Mind", "completed", ["SRC-OPENMETRICS"], "No frozen row isolates OpenMetrics 1.0 family metadata, exemplar, EOF, and UTF-8 constraints."),
    ("YAML 1.2.2 stream, document, directive, tag, anchor, alias, merge refusal, duplicate-key refusal, depth, node, and expansion-budget tribunal", "yaml122-graph-budget-tribunal", "GMUT Mind", "completed", ["SRC-YAML-122"], "No frozen row isolates YAML 1.2.2 graph identity plus duplicate-key, merge, depth, node, and expansion refusal."),
    ("RFC 9114 HTTP/3 control stream, SETTINGS, frame type, push identifier, critical-stream closure, unknown frame, truncation, and resource-budget tribunal", "http3-control-stream-tribunal", "GMUT Mind", "completed", ["SRC-RFC9114"], "No frozen row isolates HTTP/3 critical control-stream and unknown-frame handling with bounded resources."),
    ("OpenType variable-font fvar axis, avar mapping, gvar tuple, shared point, packed delta, bounds, overflow, and resource-budget tribunal", "opentype-variable-font-tribunal", "GMUT Mind", "completed", ["SRC-OPENTYPE-VAR"], "No frozen row isolates variable-font axis normalization and tuple-delta decoding across fvar, avar, and gvar."),
    ("RFC 7946 GeoJSON object type, coordinates, linear ring, winding interpretation, bbox, CRS refusal, precision, location privacy, and resource-budget tribunal", "geojson-location-boundary", "GMUT Mind", "completed", ["SRC-RFC7946"], "No frozen row isolates GeoJSON structural validity with CRS refusal, precision minimization, and location-privacy boundaries."),
    ("Accessible process-stepper list semantics, current step, completed state, error association, focus order, noncolour cue, responsive fallback, print alternative, and structural audit", "accessible-process-stepper-audit", "THOS Body", "completed", ["SRC-WCAG22"], "No frozen row isolates current-step semantics, error association, responsive fallback, and print alternative for a process stepper."),
    ("Thermo-Psyche Onsager-Machlup path probability, drift, diffusion, action, discretization, boundary condition, normalization, unit, stochastic-domain, and agency-nonconversion classifier", "onsager-machlup-domain-classifier", "GMUT Mind", "completed", ["SRC-ONSAGER-MACHLUP"], "No frozen row isolates the Onsager-Machlup action domain while refusing conversion into agency, psyche, consciousness, or personhood."),
    ("Stage 20 selection diagram, source population, target population, S-admissibility, transport formula, support, uncertainty, sensitivity, value authority, and nonpromotion board", "stage20-transportability-nonpromotion", "GMUT Mind", "completed", ["SRC-TRANSPORTABILITY"], "No frozen row isolates S-admissibility and transport-formula support as a fail-closed Stage 20 control."),
    ("THOS municipal traffic-signal phase, ring, barrier, intergreen, pedestrian interval, conflict monitor, timing-plan amendment, hold, correction readback, workload, and shift-handover proxy", "traffic-signal-timing-handover", "THOS Body", "represented", ["SRC-FHWA-SIGNALS", "SRC-NZTA-TCD"], "No frozen row isolates traffic-signal ring-barrier timing amendment, conflict-monitor hold, and shift handover."),
    ("THOS traffic-signal fault callout, cabinet boundary, site safety, temporary control, diagnostic isolation, repair hold, accessible notice, correction, workload, and shift-handover proxy", "traffic-signal-fault-handover", "THOS Body", "represented", ["SRC-FHWA-SIGNALS", "SRC-NZTA-TCD"], "No frozen row isolates signal-fault diagnostic isolation, temporary-control reservation, accessible notice, and workload handover."),
    ("Freed ID RFC 9420 MLS group identifier, epoch, ratchet tree, proposal, commit, confirmation tag, external sender, metadata minimization, and nonproduction profile", "mls-group-state-profile", "Freed ID/CBR Heart", "represented", ["SRC-RFC9420"], "No frozen row isolates MLS group-state transitions, confirmation, external senders, and metadata minimization."),
    ("Freed ID RFC 9180 HPKE mode, KEM, KDF, AEAD, key schedule, nonce sequence, exporter, context binding, error refusal, and nonproduction profile", "hpke-context-binding-profile", "Freed ID/CBR Heart", "represented", ["SRC-RFC9180"], "No frozen row isolates HPKE context binding, sequence-number nonce derivation, exporter, and refusal semantics."),
    ("Freed ID W3C Verifiable Credential JOSE or COSE media type, typ, cty, issuer-controller binding, key discovery, algorithm, validation order, privacy, and nonproduction profile", "vc-jose-cose-envelope-profile", "Freed ID/CBR Heart", "represented", ["SRC-VC-JOSE-COSE"], "No frozen row isolates the final W3C VC JOSE/COSE media types, envelope validation order, and issuer-controller boundary."),
    ("GMUT NASA LAMBDA BICEP and Keck BK18 bandpower, window, covariance, beam, calibration, foreground nuisance, checksum, schema, zero-row, and likelihood-refusal adapter", "bk18-zero-row-adapter", "GMUT Mind", "open_gap", ["SRC-BK18"], "No frozen row isolates BK18 bandpower, window, covariance, calibration, and foreground requirements as a zero-row likelihood refusal."),
    ("CBR traffic-signal pedestrian and disability access, road-user and worker privacy, location and surveillance data, crash and maintenance record, remedy, affected-party, legal, cultural, data-governance, and Māori-authority reservation", "traffic-authority-reservation", "Freed ID/CBR Heart", "exact_gate", ["SRC-NZTA-TCD", "SRC-LOCAL-CONTEXTS", "SRC-MAORI-DATA"], "No frozen row isolates traffic-signal access, surveillance-location data, crash records, remedy, affected-party governance, and Māori authority in one reservation matrix."),
]

PROPOSALS = [
    proposal(index, *spec) for index, spec in enumerate(PROPOSAL_SPECS, 1)
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

SKILL_IDEAS = [
    ("ghc-family-asymptotic-charge-boundary", "Review asymptotic charge, flux, integrability, and boundary obligations without physical promotion."),
    ("ghc-family-spatial-infinity-multipole-guard", "Review spatial-infinity and stationary multipole assumptions without observational credit."),
    ("ghc-family-conformal-evolution-firewall", "Review conformal-evolution variables and regularity obligations without a global physical theorem."),
    ("ghc-family-noether-entropy-ambiguity-rail", "Review Noether entropy and ambiguity classes without selecting a physical entropy."),
    ("ghc-family-canonical-energy-scope", "Review variational identities and canonical-energy assumptions without a stability claim."),
    ("ghc-family-structured-format-refusal", "Review bounded structured-format parsers and resource refusals without exhaustive-security credit."),
    ("ghc-family-traffic-signal-proxy-boundary", "Review synthetic traffic-signal timing and fault-handover traces without competence or authority."),
    ("ghc-family-mls-hpke-nonproduction", "Review MLS and HPKE synthetic transitions without keys, interoperability, or production credit."),
    ("ghc-family-vc-jose-cose-status-watch", "Review current VC JOSE/COSE envelope status while reserving credentials, keys, and governance."),
    ("ghc-family-traffic-authority-reservation", "Reserve traffic, disability, privacy, remedy, affected-party, legal, cultural, and Māori authority."),
]
SKILL_TASKS = [
    f"Build phase-local review skill {index:02d} named {name} with an explicit nonpromotion boundary."
    for index, (name, _description) in enumerate(SKILL_IDEAS, 1)
]

RUNNER_IDEAS = [
    ("ghc_family_asymptotic_charge_boundary.py", "asymptotic-charge"),
    ("ghc_family_spatial_infinity_multipole_guard.py", "spatial-infinity-multipole"),
    ("ghc_family_conformal_evolution_firewall.py", "conformal-evolution"),
    ("ghc_family_noether_entropy_ambiguity_rail.py", "noether-entropy"),
    ("ghc_family_canonical_energy_scope.py", "canonical-energy"),
    ("ghc_family_structured_format_refusal.py", "structured-format"),
    ("ghc_family_traffic_signal_proxy_boundary.py", "traffic-signal-proxy"),
    ("ghc_family_mls_hpke_nonproduction.py", "mls-hpke"),
    ("ghc_family_vc_jose_cose_status_watch.py", "vc-jose-cose"),
    ("ghc_family_traffic_authority_reservation.py", "traffic-authority"),
]
RUNNER_TASKS = [
    f"Build and invoke family-compatible bounded runner {index:02d} for {surface}."
    for index, (_name, surface) in enumerate(RUNNER_IDEAS, 1)
]

CLEAN_FIX_REFINE_TASKS = [
    f"REFINE-{index:02d}: review {row['slug']} terminology, falsifier, rollback, source status, and protected-gate wording without changing its frozen outcome class."
    for index, row in enumerate(PROPOSALS, 1)
]

X1_NEGATIVES = [
    (
        "V6537-X1-N01",
        "path_discovery_regex_zero_result",
        "The first bounded regex path search returned no skill paths although the exact installed directories existed; it received zero discovery credit.",
        "Use exact declared skill directories and literal-path reads before repository mutation.",
    ),
    (
        "V6537-X1-N02",
        "frozen_index_schema_assumption",
        "The first frozen-index summary assumed prior_rows and new_rows; the actual prior_proposals and new_proposals schema produced no complete audit credit.",
        "Inspect the declared schema, combine the two exact arrays, and audit all 1,600 titles.",
    ),
    (
        "V6537-X1-N03",
        "combined_login_shell_git_probe_timeout",
        "A combined login-shell status and equality probe timed out before attributable evidence and received zero verification credit.",
        "Use isolated no-profile exact HEAD, status, tracking, upstream, and live-remote probes.",
    ),
    (
        "V6537-X1-N04",
        "cold_worktree_combined_probe_timeout",
        "The first combined post-checkout branch, head, and status probe timed out on the cold worktree and received zero lane-verification credit.",
        "Let the single checkout finish, then use isolated bounded exact probes without repeating the mutation.",
    ),
    (
        "V6537-X1-N05",
        "powershell_foreach_pipe_parse_failure",
        "A read-only PowerShell foreach pipeline hit the empty-pipe-element parser error before producing its summary and received zero review credit.",
        "Materialize foreach output in an array before formatting, filtering, or measurement.",
    ),
    (
        "V6537-X1-N06",
        "powershell_foreach_pipe_guard_recurrence",
        "A later manifest-count probe repeated the already-known direct foreach-pipeline pattern before the recurrence guard was applied and received zero review credit.",
        "Apply the guard mechanically: initialize an array, append each bounded row, and pipe only the materialized array.",
    ),
    (
        "V6537-X1-N07",
        "inherited_unique_identifier_count_assumption",
        "The first bounded pre-stage x1 selection passed 21 checks but failed the novelty-count assertion because it expected 1,550 rather than the observed 1,580 unique inherited proposal identifiers; the aggregate received zero pass credit.",
        "Bind the assertion to the audited 1,600-row frozen index: 1,580 unique identifiers and 20 reused identifiers, while preserving all titles and rows.",
    ),
]

REJECTED_COLLISIONS = [
    "A generic BMS-charge proposal was rejected because frozen rows already cover broad asymptotic symmetry; v653-v7 uses the narrower Wald-Zoupas flux and integrability mechanism.",
    "A generic ADM-energy proposal was rejected because frozen rows already cover ADM and boundary-energy surfaces; v653-v7 uses the Regge-Teitelboim differentiability mechanism.",
    "A generic black-hole entropy proposal was rejected because frozen rows cover thermodynamic entropy; v653-v7 isolates Noether-charge and ambiguity mechanisms.",
    "A generic causal-structure proposal was rejected because frozen rows cover causal cones and hyperbolicity; v653-v7 isolates smooth Cauchy temporal splitting.",
    "A generic Prometheus parser proposal was rejected because frozen rows cover broad telemetry; v653-v7 isolates OpenMetrics 1.0 exposition semantics.",
    "A generic YAML parser proposal was rejected because frozen rows cover serialization formats; v653-v7 isolates graph identity and expansion-budget refusals.",
    "A generic TLS proposal was rejected because frozen rows cover transport security; v653-v7 isolates MLS group state and HPKE context binding.",
    "A generic traffic-operations proposal was rejected because frozen rows cover transport incidents; v653-v7 isolates signal ring-barrier timing and controller fault handover.",
    "A generic cosmology adapter was rejected because many frozen rows cover zero-row adapters; v653-v7 isolates the BK18 bandpower-window-covariance interface.",
    "A generic accessibility checklist was rejected because frozen rows cover broad accessibility; v653-v7 isolates process-stepper current-state, error, fallback, and print structure.",
]
