#!/usr/bin/env python3
"""Frozen Caelen Ash v653-v6 x1 data.

This module contains preregistration inputs only. It deliberately contains no
x2 observations, mutation outcomes, completion receipts, or route result.
"""

from __future__ import annotations


PHASE = "v653-v6"
PHASE_ID = "v653-gmut-thos-v6-x1-x2"
OWNER = "Caelen Ash"
PRONOUNS = "they/them"
ROLE = "relational evidence-boundary cartographer"
HOPE = (
    "make difficult claims inspectable, preserve uncertainty, and leave a safer route"
)
PHASE_ROOT = "docs/caelen-ash/v653-v6"
BRANCH = "codex/GHC-Family/caelen-ash-v653-v6-full-tools"

SOURCE_BRANCH = "codex/GHC-Family/sable-rook-v653-v5-full-tools"
SOURCE_PARENT = "78a34e98758362bae231eaec1f4a8b08b9f787dc"
SOURCE_X1 = "5447659a7d2bb0bb82b6f9ac3e374cf48086a550"
SOURCE_EVIDENCE = "927bf9ae397778942125748646439a6f508783c8"
SOURCE_HEAD = "8cfda9ac9ac86d186346b473795e7bfb045effa0"

PRIOR_FROZEN = 1570
INHERITED_NEGATIVES = 10110
EXTERNAL_POST_SEAL_NEGATIVES = 1
ACTIVATION_NEGATIVE_BASELINE = 10111
INHERITED_OPEN_GAPS = 74
INHERITED_EXACT_GATES = 75
INHERITED_METHOD_FLOW_FAILED = 15
INHERITED_METHOD_FLOW_PASSING = 15
PRIMARY_FOCUS = "THOS Body"
BOUNDED_PRACTICE = (
    "public-library audiovisual-preservation intake, carrier-risk logging, "
    "transfer-QC correction, accessible notice, workload control, and shift handover"
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
        "SRC-IASA-TC04",
        "current",
        "official_guidance",
        "IASA-TC 04 Guidelines on the Production and Preservation of Digital Audio Objects",
        "https://www.iasa-web.org/tc04/audio-preservation",
        "Supports declared audio signal-chain, format, provenance, and quality-control fields without custody, transfer authority, or a real preservation result.",
    ),
    (
        "SRC-IASA-TC05",
        "current",
        "official_guidance",
        "IASA-TC 05 Handling and Storage of Audio and Video Carriers",
        "https://www.iasa-web.org/iasa-publications",
        "Supports carrier identification, handling, cleaning, storage, and escalation fields without professional competence or permission to handle an item.",
    ),
    (
        "SRC-IASA-TC06",
        "watch",
        "official_guidance_in_revision",
        "IASA-TC 06 Guidelines for the Preservation of Video Recordings",
        "https://www.iasa-web.org/tc06/guidelines-preservation-video-recordings",
        "Supports source-class, signal, target, and retain-as-acquired fields while preserving the official work-in-progress status and all real-transfer gates.",
    ),
    (
        "SRC-FADGI-ADC",
        "watch",
        "official_guidance",
        "FADGI Audio Analog-to-Digital Converter Performance Testing",
        "https://www.digitizationguidelines.gov/guidelines/digitize-audioperf-highquality.html",
        "Supports test-signal, level, noise, distortion, channel, and result fields; the ended ADCTest support is retained and no equipment certification is claimed.",
    ),
    (
        "SRC-EBU-R128",
        "current",
        "official_standard",
        "EBU R 128 Loudness Normalisation and Permitted Maximum Level of Audio Signals",
        "https://tech.ebu.ch/publications/r128",
        "Supports programme-loudness, loudness-range, true-peak, gating, and version fields without broadcast compliance or a real measured programme.",
    ),
    (
        "SRC-ITU-BS1770",
        "current",
        "official_standard",
        "ITU-R BS.1770-5 Algorithms to measure audio programme loudness and true-peak audio level",
        "https://www.itu.int/rec/R-REC-BS.1770-5-202311-I/en",
        "Supports channel weighting, gating, loudness, true-peak, and algorithm-version fields without a real signal measurement or standards certification.",
    ),
    (
        "SRC-PBCORE-21",
        "current",
        "official_schema",
        "PBCore 2.1 XML Schema and Elements",
        "https://pbcore.org/xsd",
        "Supports description, instantiation, essence-track, identifier, relation, and extension fields without cataloguing authority or real collection metadata.",
    ),
    (
        "SRC-RFC9043",
        "stable",
        "official_standard",
        "RFC 9043 FFV1 Video Coding Format Versions 0, 1, and 3",
        "https://www.rfc-editor.org/rfc/rfc9043.html",
        "Supports bitstream-version, slice, checksum, error-status, and conformance fixtures without encoding or validating a real preservation master.",
    ),
    (
        "SRC-FADGI-RDD48",
        "current",
        "official_application_specification",
        "FADGI MXF Application Specification AS-07 using SMPTE RDD 48",
        "https://www.digitizationguidelines.gov/guidelines/MXF_app_spec.html",
        "Supports operational-pattern, partition, essence, index, metadata, amendment, and errata fields without producing or certifying an MXF file.",
    ),
    (
        "SRC-FADGI-VIDEO-PROPS",
        "current",
        "official_guidance",
        "FADGI Significant Properties for Digital Video",
        "https://www.digitizationguidelines.gov/guidelines/FADGI-SignificantPropertiesDigitalVideo2024.pdf",
        "Supports property, source, transformation, risk, verification, and uncertainty fields without declaring preservation significance for a real collection.",
    ),
    (
        "SRC-MEDIACONCH",
        "current",
        "official_software_documentation",
        "MediaConch implementation and policy checker",
        "https://mediaarea.net/MediaConch/Documentation/HowToUse",
        "Supports a synthetic policy-rule and implementation-check receipt without a real file, exhaustive conformance, or independent validation.",
    ),
    (
        "SRC-FADGI-BORN-DIGITAL",
        "stable",
        "official_guidance",
        "FADGI Creating and Archiving Born Digital Video",
        "https://www.digitizationguidelines.gov/guidelines/FADGI_BDV_p1_20141202.pdf",
        "Supports creator-to-archive handoff, source-file, metadata, fixity, storage, and migration fields without accepting or preserving a real deposit.",
    ),
    (
        "SRC-HAAGERUP-STANDARD-FORM",
        "stable",
        "primary_paper",
        "The standard form of von Neumann algebras",
        "https://doi.org/10.7146/math.scand.a-11606",
        "Supports Hilbert-space, natural-cone, modular-conjugation, uniqueness, and covariance typing without identifying an empirical GMUT state.",
    ),
    (
        "SRC-TAKESAKI-EXPECTATION",
        "stable",
        "primary_paper",
        "Conditional expectations in von Neumann algebras",
        "https://doi.org/10.1016/0022-1236(72)90004-3",
        "Supports subalgebra, faithful normal state, modular invariance, expectation, and preservation obligations without a physical coarse-graining result.",
    ),
    (
        "SRC-ARAKI-SHIRAISHI-CCR",
        "stable",
        "primary_paper",
        "On quasifree states of the canonical commutation relations",
        "https://doi.org/10.2977/prims/1195193785",
        "Supports covariance form, CCR positivity, representation, cyclic vector, and quasifree-state typing without an observed field state.",
    ),
    (
        "SRC-POWERS-STORMER",
        "stable",
        "primary_paper",
        "Free states of the canonical anticommutation relations",
        "https://www.mathnet.ru/eng/mat598",
        "Supports positive-operator square-root distance and trace-norm inequality fixtures without empirical distinguishability or a GMUT bound.",
    ),
    (
        "SRC-ROTATED-PETZ",
        "stable",
        "primary_paper",
        "Strengthened monotonicity of relative entropy via pinched Petz recovery map",
        "https://arxiv.org/abs/1507.00303",
        "Supports channel, recovery-map, relative-entropy remainder, fidelity, and equality-scope typing without a physical information-recovery result.",
    ),
    (
        "SRC-LIEB-CONVEX-TRACE",
        "stable",
        "primary_paper",
        "Convex trace functions and the Wigner-Yanase-Dyson conjecture",
        "https://doi.org/10.1016/0001-8708(73)90011-X",
        "Supports matrix-domain, exponent, trace-functional, convexity or concavity, and domain-condition fixtures without an empirical thermodynamic claim.",
    ),
    (
        "SRC-FREDENHAGEN-JORSS",
        "stable",
        "primary_paper",
        "Conformal Haag-Kastler nets, pointlike localized fields and the existence of operator product expansions",
        "https://doi.org/10.1007/BF02099249",
        "Supports net, modular construction, pointlike field, test-function, and OPE-existence obligations in its stated conformal scope without constructing GMUT.",
    ),
    (
        "SRC-SORKIN-GREEN",
        "stable",
        "primary_paper",
        "From Green Function to Quantum Field",
        "https://arxiv.org/abs/1703.00610",
        "Supports retarded-Green-function, commutator, positive spectral part, Wightman function, purity, and region-scope typing without selecting a physical vacuum.",
    ),
    (
        "SRC-KAY-WALD",
        "stable",
        "primary_paper",
        "Theorems on the uniqueness and thermal properties of stationary nonsingular quasifree states on spacetimes with a bifurcate Killing horizon",
        "https://doi.org/10.1016/0370-1573(91)90015-E",
        "Supports stationarity, nonsingularity, quasifree, horizon, uniqueness, KMS, and nonexistence-scope fields without asserting a GMUT state.",
    ),
    (
        "SRC-ROBERTS-NET-COHOMOLOGY",
        "stable",
        "primary_chapter",
        "Net Cohomology and Its Applications to Field Theory",
        "https://doi.org/10.1007/978-3-7091-8598-8_17",
        "Supports poset, net, one-cocycle, coboundary, localization, and sector-obstruction typing without identifying a physical charge sector.",
    ),
    (
        "SRC-BGL-MODULAR-LOCALIZATION",
        "stable",
        "primary_paper",
        "Modular Localization and Wigner Particles",
        "https://doi.org/10.1142/S0129055X02001387",
        "Supports positive-energy representation, wedge, real standard subspace, isotony, and localization-region fields without observing a particle.",
    ),
    (
        "SRC-RFC7521",
        "stable",
        "official_standard",
        "RFC 7521 Assertion Framework for OAuth 2.0 Client Authentication and Authorization Grants",
        "https://www.rfc-editor.org/rfc/rfc7521.html",
        "Supports assertion type, issuer, subject, audience, validity, replay, and processing fixtures without a live authorization service.",
    ),
    (
        "SRC-RFC8747",
        "stable",
        "official_standard",
        "RFC 8747 Proof-of-Possession Key Semantics for CBOR Web Tokens",
        "https://www.rfc-editor.org/rfc/rfc8747.html",
        "Supports confirmation claim, COSE key, encrypted key, key identifier, possession, and recipient fixtures without real keys or proof of control.",
    ),
    (
        "SRC-RFC9052",
        "stable",
        "official_standard",
        "RFC 9052 CBOR Object Signing and Encryption Structures",
        "https://www.rfc-editor.org/rfc/rfc9052.html",
        "Supports protected and unprotected headers, external data, signature or recipient structure, and parsing refusals without production cryptography.",
    ),
    (
        "SRC-RFC9053",
        "stable",
        "official_standard",
        "RFC 9053 CBOR Object Signing and Encryption Algorithms",
        "https://www.rfc-editor.org/rfc/rfc9053.html",
        "Supports algorithm identifier, key type, curve or mode, parameter, and implementation-requirement fixtures without real key material or security assurance.",
    ),
    (
        "SRC-OAUTH21",
        "draft",
        "official_active_draft",
        "The OAuth 2.1 Authorization Framework draft-ietf-oauth-v2-1-15",
        "https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/",
        "Supports a draft-only consolidated authorization profile and fail-closed version watch without production deployment, interoperability, or final-standard status.",
    ),
    (
        "SRC-GAIA-DR4",
        "watch",
        "official_upcoming_release",
        "ESA Gaia Data Release 4 scenario and content",
        "https://www.cosmos.esa.int/web/gaia/dr4",
        "Supports forthcoming-release, expected table, data-level, reference-epoch, and zero-row refusal fields; it provides no released DR4 rows.",
    ),
    (
        "SRC-GAIA-ARCHIVE",
        "current",
        "official_archive",
        "ESA Gaia Archive",
        "https://gea.esac.esa.int/archive/",
        "Supports archive identity and a DR4-in-preparation state with zero DR4 query, download, or row evidence.",
    ),
    (
        "SRC-LOCAL-CONTEXTS",
        "current",
        "indigenous_authority_guidance",
        "Local Contexts Traditional Knowledge, Biocultural, and Collections Care tools",
        "https://localcontexts.org/labels/about-the-labels/",
        "Requires community-specific provenance, protocol, permission, care, and authority decisions to remain with the relevant communities.",
    ),
    (
        "SRC-MAORI-DATA",
        "current",
        "maori_authority_principles",
        "Principles of Māori Data Sovereignty",
        "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
        "Requires Māori data, taonga, whakapapa, governance, access, interpretation, and remedy decisions to remain with Māori authorities.",
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
            "with no operational, production, professional, privacy-complete, "
            "interoperability, credential, key, or authority credit."
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
            "description, access, playback, transfer, takedown, return, "
            "repatriation, legal, cultural, Māori-authority, affected-party, "
            "accessibility-complete, remedy, or governance decision."
        )
    return {
        "proposal_id": f"V6536-P{number:02d}",
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
        "novelty_against_1570_frozen_proposals": novelty,
    }


PROPOSAL_SPECS = [
    ("THOS IASA-TC 04 audio source carrier, playback chain, analogue path, converter, sample format, file format, checksum, provenance, quality-control exception, and transfer-authority firewall", "iasa-tc04-audio-signal-chain", "THOS Body", "completed", ["SRC-IASA-TC04"], "No frozen row isolates the TC 04 source-to-digital audio signal chain with provenance, checksum, and transfer-authority refusal."),
    ("THOS IASA-TC 05 audiovisual carrier identity, composition, condition, handling, cleaning, enclosure, orientation, climate, hazard, escalation, and professional-reservation board", "iasa-tc05-carrier-risk-board", "THOS Body", "completed", ["SRC-IASA-TC05"], "No frozen row isolates TC 05 carrier handling, storage, condition, and escalation as a bounded audiovisual risk contract."),
    ("THOS IASA-TC 06 video source class, carrier, signal interface, playback dependency, target encoding, wrapper, timecode, error, retain-as-acquired copy, revision watch, and transfer-authority firewall", "iasa-tc06-video-preservation-profile", "THOS Body", "completed", ["SRC-IASA-TC06"], "No frozen row isolates the TC 06 video source-class and retain-as-acquired boundary while preserving its in-revision status."),
    ("THOS FADGI audio ADC test signal, level, frequency response, noise, distortion, crosstalk, channel, sample format, uncertainty, ended-tool-support flag, and noncertification board", "fadgi-adc-performance-board", "THOS Body", "completed", ["SRC-FADGI-ADC"], "No frozen row isolates FADGI ADC performance metrics while explicitly retaining the ended ADCTest support state."),
    ("THOS EBU R 128 programme loudness, loudness range, maximum true peak, gating, target, tolerance, measurement version, exception, correction lineage, and nonbroadcast-compliance board", "ebu-r128-loudness-ledger", "THOS Body", "completed", ["SRC-EBU-R128"], "No frozen row isolates the current R 128 target, tolerance, range, true-peak, gating, and correction lineage in one ledger."),
    ("THOS ITU-R BS.1770-5 input channel, prefilter, weighting, block energy, absolute gate, relative gate, integrated loudness, true peak, algorithm version, and nonmeasurement board", "itu-bs1770-algorithm-board", "THOS Body", "completed", ["SRC-ITU-BS1770"], "No frozen row isolates BS.1770-5 channel weighting, two-stage gating, loudness, and true-peak algorithm fields."),
    ("THOS PBCore 2.1 description document, asset type, identifier, title, relation, instantiation, media type, essence track, annotation, extension, version, and cataloguing-authority firewall", "pbcore21-av-metadata-profile", "THOS Body", "completed", ["SRC-PBCORE-21"], "No frozen row isolates PBCore 2.1 description, instantiation, and essence-track relations with an explicit cataloguing-authority firewall."),
    ("THOS RFC 9043 FFV1 version, coder type, colorspace, bit depth, slice geometry, slice CRC, error status, configuration record, wrapper relation, decoder refusal, and nonconformance board", "ffv1-rfc9043-bitstream-profile", "THOS Body", "completed", ["SRC-RFC9043"], "No frozen row isolates RFC 9043 FFV1 version, slice, CRC, configuration-record, and decoder-refusal obligations."),
    ("THOS FADGI AS-07 SMPTE RDD 48 MXF operational pattern, partition, header metadata, essence container, index, timecode, amendment, errata, validator, and noncertification board", "fadgi-rdd48-mxf-profile", "THOS Body", "completed", ["SRC-FADGI-RDD48"], "No frozen row isolates the AS-07 RDD 48 application profile together with amendment, errata, and validator-version boundaries."),
    ("THOS FADGI digital-video significant property, source context, property category, transformation, risk, measurement method, verification, tolerance, uncertainty, decision owner, and nonselection board", "fadgi-video-significant-properties", "THOS Body", "completed", ["SRC-FADGI-VIDEO-PROPS"], "No frozen row isolates the 2024 FADGI significant-properties decision fields for digital video without selecting values for a real collection."),
    ("THOS MediaConch policy identifier, implementation rule, field path, operator, expected value, synthetic fixture, result, report version, false-positive review, and nonconformance board", "mediaconch-policy-checker-receipt", "THOS Body", "completed", ["SRC-MEDIACONCH"], "No frozen row isolates a MediaConch policy-versus-implementation synthetic receipt with false-positive and exhaustive-conformance boundaries."),
    ("THOS FADGI born-digital-video creator file, recording context, codec, wrapper, metadata, fixity, transfer package, storage copy, migration trigger, handoff, and noncustody board", "fadgi-born-digital-handoff", "THOS Body", "completed", ["SRC-FADGI-BORN-DIGITAL"], "No frozen row isolates the born-digital creator-to-archive video handoff with fixity, storage, migration, and noncustody fields."),
    ("GMUT Haagerup standard-form von Neumann algebra, faithful representation, natural cone, modular conjugation, center action, automorphism implementer, uniqueness unitary, scope, and observation firewall", "haagerup-standard-form-ledger", "GMUT Mind", "completed", ["SRC-HAAGERUP-STANDARD-FORM"], "No frozen row isolates Haagerup standard-form uniqueness, natural cone, conjugation, and automorphism implementation together."),
    ("GMUT Takesaki conditional-expectation algebra inclusion, faithful normal state, modular automorphism invariance, expectation map, bimodule property, state preservation, uniqueness, failure, and observation firewall", "takesaki-expectation-invariance", "GMUT Mind", "completed", ["SRC-TAKESAKI-EXPECTATION"], "No frozen row isolates the Takesaki modular-invariance criterion for a state-preserving conditional expectation."),
    ("GMUT Araki-Shiraishi quasifree CCR real space, symplectic form, covariance form, positivity, Weyl relation, quasifree functional, GNS representation, cyclic vector, equivalence scope, and observation firewall", "araki-shiraishi-quasifree-ccr", "GMUT Mind", "completed", ["SRC-ARAKI-SHIRAISHI-CCR"], "No frozen row isolates Araki-Shiraishi quasifree CCR covariance, positivity, representation, and equivalence obligations."),
    ("GMUT Powers-Størmer positive trace-class operator pair, square root, Hilbert-Schmidt distance, trace norm, inequality direction, finiteness, equality scope, counterexample mutation, and observation firewall", "powers-stormer-trace-inequality", "GMUT Mind", "completed", ["SRC-POWERS-STORMER"], "No frozen row isolates the Powers-Størmer square-root Hilbert-Schmidt versus trace-norm inequality as a typed falsifiable contract."),
    ("GMUT pinched rotated-Petz channel, input state pair, output support, recovery map, rotation parameter, weighting measure, relative-entropy loss, fidelity remainder, equality scope, and observation firewall", "rotated-petz-recovery-remainder", "GMUT Mind", "completed", ["SRC-ROTATED-PETZ"], "No frozen row isolates the universal rotated or pinched Petz recovery remainder for strengthened data processing."),
    ("GMUT Lieb convex-trace positive matrix pair, exponent range, perturbation operator, trace functional, convexity-or-concavity direction, domain, endpoint, mutation, and observation firewall", "lieb-convex-trace-domain", "GMUT Mind", "completed", ["SRC-LIEB-CONVEX-TRACE"], "No frozen row isolates the Lieb convex trace functional with exponent-domain and direction checks."),
    ("GMUT Fredenhagen-Jörß conformal Haag-Kastler net, interval algebra, vacuum, modular construction, pointlike field, test function, energy bound, OPE existence, scope, and observation firewall", "fredenhagen-jorss-pointlike-fields", "GMUT Mind", "completed", ["SRC-FREDENHAGEN-JORSS"], "No frozen row isolates the Fredenhagen-Jörß modular construction of pointlike fields and OPE existence from a conformal net."),
    ("GMUT Sorkin retarded Green function, Pauli-Jordan operator, positive spectral part, Wightman function, commutator, positivity, purity condition, bounded region, non-Hadamard caveat, and observation firewall", "sorkin-green-function-state", "GMUT Mind", "completed", ["SRC-SORKIN-GREEN"], "No frozen row isolates the Sorkin Green-function-to-Wightman positive spectral prescription with purity and region caveats."),
    ("GMUT Kay-Wald globally hyperbolic spacetime, bifurcate Killing horizon, isometry, quasifree state, stationarity, nonsingularity, Hadamard condition, uniqueness, KMS implication, nonexistence scope, and observation firewall", "kay-wald-horizon-state-scope", "GMUT Mind", "completed", ["SRC-KAY-WALD"], "No frozen row isolates Kay-Wald uniqueness, thermal implication, and nonexistence scope for stationary horizon states."),
    ("GMUT Roberts net-cohomology spacetime-region poset, local net, one-simplex, one-cocycle, path product, coboundary, localization, equivalence class, sector obstruction, and observation firewall", "roberts-net-cohomology-ledger", "GMUT Mind", "completed", ["SRC-ROBERTS-NET-COHOMOLOGY"], "No frozen row isolates Roberts one-cocycles on a local-net poset as a sector-obstruction ledger."),
    ("GMUT Brunetti-Guido-Longo positive-energy Poincaré representation, wedge, boost, reflection, Tomita operator, real standard subspace, intersection region, isotony, continuous-spin scope, and observation firewall", "bgl-modular-localization", "GMUT Mind", "completed", ["SRC-BGL-MODULAR-LOCALIZATION"], "No frozen row isolates BGL one-particle modular localization, wedge real subspaces, isotony, and continuous-spin scope."),
    ("Freed ID RFC 7521 OAuth assertion framework client-authentication versus authorization-grant role, assertion parameter, token-endpoint transport, extension specification, processing order, unsupported-assertion error, profile dependency, and nonproduction boundary", "rfc7521-oauth-assertion-profile", "Freed ID/CBR Heart", "represented", ["SRC-RFC7521"], "No frozen row isolates the abstract RFC 7521 assertion-framework roles, transport parameters, extension obligations, and errors rather than a concrete JWT or SAML assertion profile."),
    ("Freed ID RFC 8747 CWT confirmation claim, COSE key, encrypted key, key identifier, recipient, possession method, privacy exposure, key lookup, mismatch refusal, and nonproduction profile", "rfc8747-cwt-confirmation-profile", "Freed ID/CBR Heart", "represented", ["SRC-RFC8747"], "No frozen row isolates RFC 8747 CWT confirmation-method alternatives and proof-of-possession mismatch refusal."),
    ("Freed ID RFC 9052 COSE message type, protected header bytes, unprotected map, payload, external additional data, signature or recipient structure, duplicate-label refusal, and nonproduction profile", "rfc9052-cose-structure-profile", "Freed ID/CBR Heart", "represented", ["SRC-RFC9052"], "No frozen row isolates RFC 9052 protected-byte preservation, external data, message structures, and duplicate-header refusals."),
    ("Freed ID RFC 9053 COSE algorithm identifier, key type, curve or mode, parameter, implementation requirement, nonce or IV, tag or signature, invalid combination refusal, and nonproduction profile", "rfc9053-cose-algorithm-profile", "Freed ID/CBR Heart", "represented", ["SRC-RFC9053"], "No frozen row isolates RFC 9053 algorithm-to-key and parameter compatibility with implementation-requirement status."),
    ("Freed ID draft OAuth 2.1 authorization endpoint, token endpoint, authorization code, PKCE requirement, redirect URI, refresh-token rotation, bearer-token transport, removed flow, draft version, and nonproduction profile", "oauth21-draft-consolidation-watch", "Freed ID/CBR Heart", "represented", ["SRC-OAUTH21"], "No frozen row isolates the current OAuth 2.1 draft as a consolidated, version-watched, explicitly nonfinal profile."),
    ("GMUT ESA Gaia DR4 forthcoming release, archive identity, expected table, data level, reference epoch, release-status check, schema watch, query refusal, download refusal, zero rows, and likelihood-refusal adapter", "gaia-dr4-zero-row-adapter", "GMUT Mind", "open_gap", ["SRC-GAIA-DR4", "SRC-GAIA-ARCHIVE"], "No frozen row isolates the forthcoming Gaia DR4 release state as a zero-query, zero-download, zero-row adapter with an explicit schema watch."),
    ("CBR audiovisual-recording description, access, playback, transfer, digitization, sacred-or-restricted content, notice, takedown, return, repatriation, taonga and mātauranga provenance, remedy, affected-party review, iwi and hapū governance, and Māori-authority reservation", "av-cultural-authority-rail", "Freed ID/CBR Heart", "exact_gate", ["SRC-LOCAL-CONTEXTS", "SRC-MAORI-DATA"], "No frozen row isolates audiovisual description, playback, transfer, restricted content, takedown, return, repatriation, taonga, mātauranga, iwi and hapū governance, and Māori authority in one reservation matrix."),
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

SKILL_TASKS = [
    f"Build phase-local review skill {index:02d} for {surface} with an explicit nonpromotion boundary."
    for index, surface in enumerate(
        [
            "audiovisual carrier risk",
            "audio signal-chain provenance",
            "loudness and true-peak algorithms",
            "PBCore metadata boundaries",
            "FFV1 and MXF preservation profiles",
            "digital-video significant properties",
            "operator-algebra typed claims",
            "modular-localization scope",
            "identity standard-status watch",
            "audiovisual cultural authority",
        ],
        1,
    )
]

SKILL_IDEAS = [
    ("ghc-family-av-carrier-risk-guard", "Review carrier identity, condition, handling, storage, and escalation without custody or professional authority."),
    ("ghc-family-audio-signal-chain-ledger", "Review source-to-digital signal-chain, provenance, checksum, and QC fields without real transfer credit."),
    ("ghc-family-loudness-algorithm-boundary", "Review R 128 and BS.1770 versioned loudness and true-peak fields without broadcast compliance."),
    ("ghc-family-pbcore-metadata-rail", "Review PBCore description, instantiation, and essence-track relations without cataloguing authority."),
    ("ghc-family-av-container-profile-watch", "Review FFV1 and AS-07 profile, amendment, errata, and validator-version fields without conformance certification."),
    ("ghc-family-video-significant-properties-rail", "Review property, transformation, risk, verification, and uncertainty fields without deciding significance for a real collection."),
    ("ghc-family-operator-algebra-typing-guard", "Review standard form, expectation, quasifree, recovery, and trace-function hypotheses without empirical promotion."),
    ("ghc-family-modular-localization-scope", "Review net, cohomology, horizon-state, and modular-localization scope without identifying a physical sector or state."),
    ("ghc-family-identity-standard-status-watch", "Fail closed on OAuth draft status and all credential, key, interoperability, privacy, and production promotions."),
    ("ghc-family-av-cultural-authority-rail", "Reserve description, access, playback, transfer, takedown, return, repatriation, taonga, mātauranga, iwi, hapū, and Māori authority."),
]

RUNNER_TASKS = [
    f"Build and invoke family-compatible bounded runner {index:02d} for {surface}."
    for index, surface in enumerate(
        [
            "av-carrier-risk",
            "audio-signal-chain",
            "loudness-algorithm",
            "pbcore-metadata",
            "av-container-profile",
            "video-significant-properties",
            "operator-algebra-typing",
            "modular-localization",
            "identity-status-watch",
            "av-cultural-authority",
        ],
        1,
    )
]

RUNNER_IDEAS = [
    ("ghc_family_av_carrier_risk_guard.py", "av-carrier-risk"),
    ("ghc_family_audio_signal_chain_guard.py", "audio-signal-chain"),
    ("ghc_family_loudness_algorithm_guard.py", "loudness-algorithm"),
    ("ghc_family_pbcore_metadata_guard.py", "pbcore-metadata"),
    ("ghc_family_av_container_profile_guard.py", "av-container-profile"),
    ("ghc_family_video_significant_properties_guard.py", "video-significant-properties"),
    ("ghc_family_operator_algebra_typing_guard.py", "operator-algebra-typing"),
    ("ghc_family_modular_localization_guard.py", "modular-localization"),
    ("ghc_family_identity_standard_status_watch.py", "identity-status-watch"),
    ("ghc_family_av_cultural_authority_guard.py", "av-cultural-authority"),
]

CLEAN_FIX_REFINE_TASKS = [
    f"REFINE-{index:02d}: review {row['slug']} terminology, falsifier, rollback, source status, and protected-gate wording without changing its frozen outcome class."
    for index, row in enumerate(PROPOSALS, 1)
]

X1_NEGATIVES = [
    (
        "V6536-X1-N01",
        "memory_registry_search_timeout",
        "The first bounded memory-registry text search timed out before a coherent continuity result and received zero review credit.",
        "Narrow memory lookup to directly indexed current-sibling terms and exact pointed files.",
    ),
    (
        "V6536-X1-N02",
        "task_registry_limit_rejected",
        "The first read-only task-registry request used an unsupported page limit and was rejected before listing any task.",
        "Use the supported bounded registry page, then resolve an exact title only at the authorized terminal gate.",
    ),
    (
        "V6536-X1-N03",
        "frozen_index_shape_and_shell_assumption",
        "The first frozen-index audit assumed one rows array and a newer PowerShell string-join command; the actual split schema and Windows PowerShell 5.1 produced no complete audit credit.",
        "Combine the declared prior and new arrays explicitly and use stable .NET byte and string primitives available in Windows PowerShell 5.1.",
    ),
    (
        "V6536-X1-N04",
        "uniform_row_and_global_proposal_id_assumption",
        "The first all-row audit assumed uniform rich row shapes and globally unique historical proposal IDs; correction segments made both assumptions false and the audit received zero novelty credit.",
        "Use row position and title as the frozen-chain identity, preserve historical ID duplicates, and require global title uniqueness plus deterministic all-row scoring.",
    ),
    (
        "V6536-X1-N05",
        "powershell_scriptblock_measure_property_failure",
        "The first maximum-title probe passed a script block where Measure-Object expected a property name and failed before producing a maximum.",
        "Materialize title lengths in a bounded foreach pass and then compute the scalar maximum.",
    ),
    (
        "V6536-X1-N06",
        "worktree_add_wrapper_timeout",
        "The worktree-add wrapper timed out while the single authorized checkout continued in Git; it received zero completion credit.",
        "Do not retry mutation; audit the exact path, worktree registration, branch, HEAD, process completion, and clean state before proceeding.",
    ),
    (
        "V6536-X1-N07",
        "worktree_list_during_active_checkout_timeout",
        "A read-only worktree-list probe timed out while the authorized checkout was still active and received zero registration credit.",
        "Wait for the bounded checkout process to finish, then run one exact registration and HEAD audit.",
    ),
    (
        "V6536-X1-N08",
        "broad_template_pattern_scan_timeout",
        "A broad pattern scan across all copied v5 templates timed out before a coherent result and received zero adaptation credit.",
        "Inspect the exact template inventory and exact files with bounded literal-path searches.",
    ),
    (
        "V6536-X1-N09",
        "method_flow_top_level_entries_assumption",
        "The first inherited Method Flow count probe assumed a top-level entries array and produced an invalid one-entry summary with zero continuity credit.",
        "Inspect the declared ledger schema first and use its methods, witnesses, state-events, and counts fields.",
    ),
    (
        "V6536-X1-N10",
        "powershell_foreach_output_pipe_parse_failure",
        "A read-only source-manifest summary piped directly from a foreach statement and hit the Windows PowerShell empty-pipe-element parser error before reading any manifest.",
        "Materialize foreach output into a task-specific array before piping it to formatting or selection commands.",
    ),
    (
        "V6536-X1-N11",
        "prestage_test_selection_included_staged_receipt_case",
        "The first pre-staging unit-test selection included the lifecycle case that requires x1 staged receipts; 21 tests passed and that case failed before any staging, so the aggregate received zero pass credit.",
        "Run the bounded pre-stage selection without the staged-receipt lifecycle case, then stage the exact allowlist and exercise that case through the dedicated x1 staged validator.",
    ),
    (
        "V6536-X1-N12",
        "method_flow_state_event_field_name_assumption",
        "The first Method Flow state-sequence summary queried a nonexistent to_state field and returned blank states, so it received zero transition-review credit.",
        "Inspect the ledger schema and verify the ordered before and after fields as candidate, validated, and preferred.",
    ),
]

REJECTED_COLLISIONS = [
    "A Library of Congress Recommended Formats Statement row was rejected because V6534-P22 already isolates that format-preference mechanism.",
    "A Broadcast Wave Format metadata row was rejected because V6513-P12 already isolates that audio-metadata mechanism.",
    "A PREMIS row was rejected because a frozen row already isolates preservation events, agents, objects, rights, and outcomes.",
    "A BagIt row was rejected because a frozen row already isolates declaration, payload, manifests, fetch, checksum, and refusal.",
    "An IIIF row was rejected because frozen image-API and presentation rows already isolate those interoperability surfaces.",
    "A DPoP row was rejected because a frozen row already isolates sender-constrained access tokens and proof replay.",
    "A PKCE row was rejected as a standalone proposal because frozen rows already isolate authorization-code verifier and challenge semantics.",
    "A generic local-covariance row was rejected because v653-v4 already isolates locally covariant QFT and relative-Cauchy mechanisms.",
    "A generic DHR row was rejected because v653-v4 and earlier rows already isolate DHR sectors and superselection structure.",
    "A generic Tomita-Takesaki row was rejected because frozen modular-flow rows already isolate that mechanism; v653-v6 uses narrower standard-form, conditional-expectation, and localization contracts.",
]
