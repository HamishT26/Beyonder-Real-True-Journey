#!/usr/bin/env python3
"""Frozen Auren Lark v653-v4 x1 data.

This module contains preregistration inputs only. It deliberately contains no
x2 observations, mutation outcomes, completion receipts, or route result.
"""

from __future__ import annotations


PHASE = "v653-v4"
PHASE_ID = "v653-gmut-thos-v4-x1-x2"
OWNER = "Auren Lark"
PRONOUNS = "they/them"
ROLE = "relational evidence-path cartographer"
HOPE = (
    "make difficult routes legible, recoverable, and honest about every "
    "remaining boundary"
)
PHASE_ROOT = "docs/auren-lark/v653-v4"
BRANCH = "codex/GHC-Family/auren-lark-v653-v4-full-tools"

SOURCE_BRANCH = "codex/GHC-Family/ilyra-fen-v653-v3-full-tools"
SOURCE_PARENT = "c25e70eaae7c338a22ee64270ab574768835b227"
SOURCE_X1 = "7c2cc69203b827dc4b0be18c10931f8e92477b4a"
SOURCE_EVIDENCE = "684ef89d6c9ea28577b93b7df8a071cb557e9221"
SOURCE_HEAD = "431c8f0dcbc837cd87d63776771a802878a62c25"

PRIOR_FROZEN = 1510
INHERITED_NEGATIVES = 9777
INHERITED_OPEN_GAPS = 72
INHERITED_EXACT_GATES = 73
INHERITED_METHOD_FLOW_FAILED = 19
INHERITED_METHOD_FLOW_PASSING = 19
PRIMARY_FOCUS = "Freed ID/CBR Heart"
BOUNDED_PRACTICE = (
    "digital preservation, archival provenance review, fixity triage, and "
    "access handover"
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
        "SRC-AQFT-DHR",
        "stable",
        "primary_review",
        "Algebraic Quantum Field Theory",
        "https://arxiv.org/abs/math-ph/0602036",
        "Supports localized-endomorphism and superselection-category obligations without a particle, force, or empirical claim.",
    ),
    (
        "SRC-BF-SECTORS",
        "stable",
        "primary_paper",
        "Locality and the structure of particle states",
        "https://doi.org/10.1007/BF01208372",
        "Supports spacelike-cone localization obligations without establishing a physical sector in GMUT.",
    ),
    (
        "SRC-ARAKI-HAAG",
        "stable",
        "primary_paper",
        "Collision cross sections in terms of local observables",
        "https://doi.org/10.1007/BF01646080",
        "Supports asymptotic detector and energy-momentum transfer bookkeeping without an observed scattering event.",
    ),
    (
        "SRC-BORCHERS-TRIPLES",
        "stable",
        "primary_research",
        "Construction of quantum field theories with factorizing S-matrices",
        "https://arxiv.org/abs/math-ph/0601022",
        "Supports wedge algebra, translation, and intersection obligations without constructing a GMUT model.",
    ),
    (
        "SRC-NUCLEARITY",
        "stable",
        "primary_paper",
        "Causal independence and the energy-level density of states in local quantum field theory",
        "https://doi.org/10.1007/BF01211751",
        "Supports phase-space nuclearity maps and compactness reservations without a stability theorem.",
    ),
    (
        "SRC-SPLIT",
        "stable",
        "primary_paper",
        "Standard and split inclusions of von Neumann algebras",
        "https://doi.org/10.1007/BF01211060",
        "Supports type-I interpolation and inclusion obligations without a physical independence result.",
    ),
    (
        "SRC-LCQFT",
        "stable",
        "primary_paper",
        "The generally covariant locality principle",
        "https://arxiv.org/abs/math-ph/0112041",
        "Supports functorial locality, time-slice, and relative-Cauchy-evolution contracts without empirical confirmation.",
    ),
    (
        "SRC-SCALING-ALGEBRAS",
        "stable",
        "primary_paper",
        "Scaling Algebras and Renormalization Group in Algebraic Quantum Field Theory",
        "https://arxiv.org/abs/hep-th/9501063",
        "Supports scaling-family and limit-state bookkeeping without an ultraviolet completion claim.",
    ),
    (
        "SRC-DYNAMICAL-LOCALITY",
        "stable",
        "primary_paper",
        "Dynamical locality and covariance",
        "https://arxiv.org/abs/1106.4785",
        "Supports kinematic-versus-dynamical local-net comparison without proving GMUT locality.",
    ),
    (
        "SRC-MODULAR-NUCLEARITY",
        "stable",
        "primary_paper",
        "On the existence of local observables in theories with a factorizing S-matrix",
        "https://arxiv.org/abs/math-ph/0405062",
        "Supports a modular-nuclearity map and wedge-intersection refusal boundary only.",
    ),
    (
        "SRC-RESOURCESYNC",
        "stable",
        "official_standard",
        "ResourceSync Framework Specification",
        "https://www.openarchives.org/rs",
        "Supports capability-list, change-list, dump, link-relation, and resynchronization fixtures only.",
    ),
    (
        "SRC-OAI-PMH",
        "stable",
        "official_specification",
        "Open Archives Initiative Protocol for Metadata Harvesting Version 2.0",
        "https://www.openarchives.org/OAI/openarchivesprotocol.html",
        "Supports verb, metadata-prefix, datestamp, set, error, and resumption-token fixtures only.",
    ),
    (
        "SRC-NDSA-LEVELS",
        "current",
        "official_guidance",
        "NDSA Levels of Digital Preservation Version 2.1",
        "https://www.ndsa.org/publications/levels-of-digital-preservation/",
        "Supports a synthetic preservation-level matrix; it does not certify an archive or professional capability.",
    ),
    (
        "SRC-JHOVE",
        "current",
        "official_documentation",
        "JHOVE identification, validation, and characterization documentation",
        "https://jhove.openpreservation.org/documentation/",
        "Supports well-formedness, validity, module, handler, and representation-information fixtures only.",
    ),
    (
        "SRC-ARCHIVEMATICA",
        "current",
        "official_documentation",
        "Archivematica technical architecture",
        "https://www.archivematica.org/en/docs/latest/getting-started/overview/technical/",
        "Supports synthetic transfer, SIP, AIP, DIP, microservice, and refusal-state handover fixtures only.",
    ),
    (
        "SRC-LOCKSS",
        "current",
        "official_documentation",
        "How LOCKSS Works",
        "https://www.lockss.org/use-lockss/how-lockss-works",
        "Supports peer-poll, disagreement, repair, audit, and preservation-status fixtures without operating a network.",
    ),
    (
        "SRC-PRONOM",
        "current",
        "official_registry",
        "PRONOM technical registry",
        "https://pronom.nationalarchives.gov.uk/about",
        "Supports PUID, byte-signature, container-signature, version, and ambiguity fixtures only.",
    ),
    (
        "SRC-EARK-CSIP",
        "current",
        "official_specification",
        "E-ARK Common Specification for Information Packages",
        "https://digital-strategy.ec.europa.eu/en/policies/earchiving-specifications",
        "Supports synthetic CSIP hierarchy and package-integrity fixtures without repository interoperability evidence.",
    ),
    (
        "SRC-NARA-DPF",
        "current",
        "official_guidance",
        "NARA Digital Preservation Framework",
        "https://www.archives.gov/preservation/digital-preservation",
        "Supports risk, action, sustainability, and review-status fixtures without professional adoption or approval.",
    ),
    (
        "SRC-LOC-RFS",
        "current",
        "official_guidance",
        "Library of Congress Recommended Formats Statement",
        "https://www.loc.gov/preservation/resources/rfs/",
        "Supports preference-factor and acceptance-boundary fixtures without a real acquisition decision.",
    ),
    (
        "SRC-DPC-RAM",
        "current",
        "official_guidance",
        "Digital Preservation Coalition Rapid Assessment Model Version 3",
        "https://www.dpconline.org/digipres/implement-digipres/dpc-ram",
        "Supports a synthetic maturity and forward-plan matrix without organizational or professional assessment credit.",
    ),
    (
        "SRC-ROUGHTIME",
        "draft",
        "official_active_draft",
        "IETF Roughtime",
        "https://datatracker.ietf.org/doc/draft-ietf-ntp-roughtime/",
        "Supports a draft-only nonce, midpoint, radius, delegation, Merkle-path, and causality-chain profile.",
    ),
    (
        "SRC-KEYTRANS-ARCH",
        "draft",
        "official_active_draft",
        "IETF Key Transparency Architecture",
        "https://datatracker.ietf.org/doc/draft-ietf-keytrans-architecture/",
        "Supports a draft-only label, view, monitor, auditor, fork-detection, and migration profile.",
    ),
    (
        "SRC-KEYTRANS-PROTOCOL",
        "draft",
        "official_active_draft",
        "IETF Key Transparency Protocol",
        "https://datatracker.ietf.org/doc/draft-ietf-keytrans-protocol/",
        "Supports draft-only search, update, monitor, ladder, tree-head, and proof-verification fixtures.",
    ),
    (
        "SRC-COSE-HPKE",
        "draft",
        "official_active_draft",
        "Use of Hybrid Public Key Encryption with CBOR Object Signing and Encryption",
        "https://datatracker.ietf.org/doc/draft-ietf-cose-hpke/",
        "Supports a draft-only protected-header, encapsulated-key, context, sender, recipient, and downgrade-refusal profile.",
    ),
    (
        "SRC-REKOR",
        "current",
        "official_documentation",
        "Sigstore Rekor transparency log",
        "https://docs.sigstore.dev/logging/overview/",
        "Supports a synthetic log-entry, inclusion, checkpoint, consistency, and monitor profile without live signing.",
    ),
    (
        "SRC-SWHID",
        "stable",
        "official_standard",
        "ISO/IEC 18670:2025 Software Hash Identifier",
        "https://www.swhid.org/swhid-specification/",
        "Supports a synthetic intrinsic identifier and qualifier profile without archival availability or resolution credit.",
    ),
    (
        "SRC-GAIA-ARCHIVE",
        "current",
        "official_data_documentation",
        "Gaia ESA Archive",
        "https://gea.esac.esa.int/archive/",
        "Supports a zero-query, zero-download, zero-row schema and refusal adapter only.",
    ),
    (
        "SRC-GAIA-DR3",
        "current",
        "official_data_documentation",
        "Gaia Data Release 3 documentation",
        "https://gea.esac.esa.int/archive/documentation/GDR3/",
        "Supports data-model, release, known-issue, unit, and provenance obligations without a likelihood or result.",
    ),
    (
        "SRC-LOCAL-CONTEXTS",
        "current",
        "indigenous_authority_guidance",
        "Local Contexts Traditional Knowledge and Biocultural Labels",
        "https://localcontexts.org/labels/about-the-labels/",
        "Requires community-specific provenance, protocol, permission, and authority decisions to remain outside repository software.",
    ),
    (
        "SRC-MAORI-DATA",
        "current",
        "maori_authority_principles",
        "Principles of Māori Data Sovereignty",
        "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
        "Requires Māori data, taonga, governance, access, and remedy decisions to remain with Māori authorities.",
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
            "interoperability, archival-availability, or authority credit."
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
            "access, repatriation, legal, cultural, Māori-authority, "
            "affected-party, accessibility-complete, remedy, or governance decision."
        )
    return {
        "proposal_id": f"V6534-P{number:02d}",
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
        "novelty_against_1510_frozen_proposals": novelty,
    }


PROPOSAL_SPECS = [
    ("GMUT Doplicher-Haag-Roberts transportable localized endomorphism, double-cone localization, charge transport, tensor product, conjugate sector, statistics operator, gauge reconstruction reservation, and observation firewall", "dhr-superselection-category", "GMUT Mind", "completed", ["SRC-AQFT-DHR"], "No frozen row isolates the DHR localized-endomorphism category, transporters, conjugates, and statistics operators as one contract."),
    ("GMUT Buchholz-Fredenhagen spacelike-cone localization, massive charge, representation criterion, cone transportability, asymptotic localization, composition, sector equivalence, and observation firewall", "buchholz-fredenhagen-cone-sector", "GMUT Mind", "completed", ["SRC-BF-SECTORS"], "No frozen row isolates BF spacelike-cone localization and massive-charge sector transportability."),
    ("GMUT Araki-Haag detector almost-local observable, energy-momentum transfer, velocity support, time average, asymptotic functional, coincidence reservation, and observation firewall", "araki-haag-asymptotic-detector", "GMUT Mind", "completed", ["SRC-ARAKI-HAAG"], "No frozen row isolates the Araki-Haag almost-local detector limit and its energy-momentum and velocity-support obligations."),
    ("GMUT Borchers triple wedge algebra, translation representation, spectrum condition, wedge inclusion, reflected wedge, local intersection, cyclicity reservation, and observation firewall", "borchers-triple-wedge-net", "GMUT Mind", "completed", ["SRC-BORCHERS-TRIPLES"], "No frozen row isolates Borchers-triple wedge inclusions and the local-intersection existence boundary."),
    ("GMUT phase-space nuclearity local algebra, Hamiltonian damping, bounded-region map, nuclear norm, energy scale, compactness class, temperature reservation, and observation firewall", "phase-space-nuclearity-map", "GMUT Mind", "completed", ["SRC-NUCLEARITY"], "No frozen row isolates the energy-damped local-algebra nuclearity map and its phase-space norm."),
    ("GMUT split-property nested regions, local von Neumann algebras, type-I interpolating factor, collar separation, product-state map, statistical-independence reservation, and observation firewall", "split-inclusion-type-one-factor", "GMUT Mind", "completed", ["SRC-SPLIT"], "No frozen row isolates a type-I factor between nested local algebras with an explicit collar and product-state boundary."),
    ("GMUT locally covariant time-slice Cauchy morphism, induced algebra map, inverse, causal propagation, support, functorial composition, background reservation, and observation firewall", "time-slice-cauchy-morphism", "GMUT Mind", "completed", ["SRC-LCQFT"], "No frozen row isolates the locally covariant time-slice isomorphism and Cauchy-morphism composition contract."),
    ("GMUT relative Cauchy evolution metric perturbation, past and future identifications, automorphism, functional derivative, stress-energy interpretation reservation, support, and observation firewall", "relative-cauchy-evolution", "GMUT Mind", "completed", ["SRC-LCQFT"], "No frozen row isolates relative Cauchy evolution as a metric-perturbation automorphism with a derivative-interpretation firewall."),
    ("GMUT locally covariant quantum-field functor, globally hyperbolic spacetime category, algebra category, causal embedding, natural transformation, state-space subfunctor, and observation firewall", "locally-covariant-qft-functor", "GMUT Mind", "completed", ["SRC-LCQFT"], "No frozen row isolates spacetime-to-algebra functoriality together with natural fields and state-space subfunctors."),
    ("GMUT Buchholz-Verch scaling algebra scale family, localization region, continuity, scaling transformation, limit state, GNS representation, nonuniqueness reservation, and observation firewall", "buchholz-verch-scaling-algebra", "GMUT Mind", "completed", ["SRC-SCALING-ALGEBRAS"], "No frozen row isolates the scaling-algebra family, limit state, and GNS scaling-limit nonuniqueness contract."),
    ("GMUT dynamical locality kinematic subalgebra, relative-Cauchy invariant subalgebra, compact-region union, timeslice covariance, massless gauge exception, and observation firewall", "dynamical-locality-net-equality", "GMUT Mind", "completed", ["SRC-DYNAMICAL-LOCALITY"], "No frozen row isolates equality of kinematic and dynamical local nets with the massless gauge-symmetry exception."),
    ("GMUT modular nuclearity wedge algebra, translated wedge, modular operator, nuclear map, wedge separation, local-intersection consequence reservation, and observation firewall", "modular-nuclearity-wedge-map", "GMUT Mind", "completed", ["SRC-MODULAR-NUCLEARITY"], "No frozen row isolates the modular-nuclearity map from a wedge algebra into a translated-wedge domain."),
    ("THOS ResourceSync capability list, resource list, change list, change dump, link relation, modified time, hash, cursor, resynchronization, and refusal board", "resourcesync-change-audit", "THOS Body", "completed", ["SRC-RESOURCESYNC"], "No frozen row isolates ResourceSync capabilities, change dumps, link relations, and resynchronization cursor obligations."),
    ("THOS OAI-PMH Identify, ListMetadataFormats, ListSets, ListIdentifiers, ListRecords, GetRecord, metadata prefix, datestamp, resumption token, error, and refusal board", "oai-pmh-harvest-state", "THOS Body", "completed", ["SRC-OAI-PMH"], "No frozen row isolates all six OAI-PMH verbs, resumable harvesting state, and protocol-error boundaries."),
    ("THOS NDSA Levels storage, integrity, control, metadata, content, environmental sustainability, current-level evidence, target level, exception, and noncertification board", "ndsa-preservation-levels-matrix", "THOS Body", "completed", ["SRC-NDSA-LEVELS"], "No frozen row isolates the 2026 NDSA Levels 2.1 matrix with evidence, target, exception, and noncertification fields."),
    ("THOS JHOVE format identification, module selection, well-formedness, validity, characterization property, representation information, handler result, and nonpromotion board", "jhove-characterization-boundary", "THOS Body", "completed", ["SRC-JHOVE"], "No frozen row isolates JHOVE identification, well-formedness, validity, characterization, module, and handler result boundaries."),
    ("THOS Archivematica transfer, SIP, AIP, DIP, microservice, preservation action, format-policy rule, decision point, failure state, and nonproduction handover board", "archivematica-package-handover", "THOS Body", "completed", ["SRC-ARCHIVEMATICA"], "No frozen row isolates Archivematica package transitions and microservice decision points as a nonproduction handover contract."),
    ("THOS LOCKSS archival unit, peer poll, vote, disagreement, repair, audit history, preservation status, network threshold, operator reservation, and nonpromotion board", "lockss-poll-repair-boundary", "THOS Body", "completed", ["SRC-LOCKSS"], "No frozen row isolates LOCKSS peer-poll disagreement and repair state while reserving real network and operator evidence."),
    ("THOS PRONOM PUID, format version, extension, MIME type, byte signature, container signature, priority, ambiguity, registry revision, and refusal board", "pronom-format-signature-ledger", "THOS Body", "completed", ["SRC-PRONOM"], "No frozen row isolates PRONOM registry revision, PUID, byte and container signatures, priority, and ambiguous-match refusal."),
    ("THOS E-ARK CSIP package root, METS hierarchy, representation, data object, metadata object, checksum, profile, extension, validation status, and interoperability refusal board", "eark-csip-package-integrity", "THOS Body", "completed", ["SRC-EARK-CSIP"], "No frozen row isolates the current E-ARK CSIP hierarchy and profile-extension integrity contract."),
    ("THOS NARA preservation framework format risk, preservation action, access expectation, sustainability factor, dependency, review date, evidence state, and professional-reservation board", "nara-preservation-risk-register", "THOS Body", "completed", ["SRC-NARA-DPF"], "No frozen row isolates the NARA framework's format-risk, action, sustainability, dependency, and review-state obligations."),
    ("THOS Library of Congress Recommended Formats Statement content category, preferred factor, acceptable factor, technical protection, disclosure, accessibility feature, acquisition-decision reservation, and refusal board", "loc-recommended-format-factors", "THOS Body", "completed", ["SRC-LOC-RFS"], "No frozen row isolates Recommended Formats Statement preference factors with acquisition and accessibility decision reservations."),
    ("THOS DPC Rapid Assessment Model capability dimension, maturity level, evidence note, risk, forward action, review cadence, benchmark reservation, and professional-assessment refusal board", "dpc-ram-capability-matrix", "THOS Body", "completed", ["SRC-DPC-RAM"], "No frozen row isolates DPC RAM v3 maturity evidence and forward actions with benchmark and professional-assessment refusal."),
    ("Freed ID draft Roughtime nonce, midpoint, radius, delegated key, Merkle path, signature, causality chain, server set, draft status, and nonproduction profile", "roughtime-draft-proof-profile", "Freed ID/CBR Heart", "represented", ["SRC-ROUGHTIME"], "No frozen row isolates the active IETF Roughtime draft's rough interval, delegation, Merkle path, and causality-chain obligations."),
    ("Freed ID draft Key Transparency label, label version, search proof, monitor state, distinguished tree head, fork detection, migration, privacy, draft status, and nonproduction profile", "key-transparency-monitor-profile", "Freed ID/CBR Heart", "represented", ["SRC-KEYTRANS-ARCH", "SRC-KEYTRANS-PROTOCOL"], "No frozen row isolates the active IETF Key Transparency search, monitor, distinguished-head, fork, migration, and privacy obligations."),
    ("Freed ID draft COSE HPKE protected header, algorithm identifier, encapsulated key, sender context, recipient context, external AAD, downgrade refusal, draft status, and nonproduction profile", "cose-hpke-draft-envelope", "Freed ID/CBR Heart", "represented", ["SRC-COSE-HPKE"], "No frozen row isolates the active COSE HPKE draft envelope and its encapsulated-key and context-binding obligations."),
    ("Freed ID Rekor entry kind, canonical body, artifact digest, signature material, log index, integrated time, inclusion proof, checkpoint, consistency monitor, and nonproduction profile", "rekor-transparency-entry-profile", "Freed ID/CBR Heart", "represented", ["SRC-REKOR"], "Distinct from the inherited Sigstore bundle row because this surface isolates Rekor entry canonicalization, inclusion, checkpoint, and monitor state."),
    ("Freed ID ISO SWHID object type, hash algorithm, object identifier, origin qualifier, visit qualifier, anchor qualifier, path qualifier, lines qualifier, resolution boundary, and nonproduction profile", "swhid-intrinsic-identifier-profile", "Freed ID/CBR Heart", "represented", ["SRC-SWHID"], "No frozen row isolates ISO/IEC 18670 SWHID core object types and contextual qualifiers with an explicit resolution boundary."),
    ("GMUT Gaia ESA Archive release, source identifier, astrometry field, photometry field, spectroscopy field, unit, known issue, provenance, checksum, covariance, and zero-row likelihood-refusal adapter", "gaia-archive-zero-row-adapter", "GMUT Mind", "open_gap", ["SRC-GAIA-ARCHIVE", "SRC-GAIA-DR3"], "No frozen row isolates a Gaia Archive release-and-known-issue adapter with zero query, zero download, zero rows, and likelihood refusal."),
    ("CBR archival collection Traditional Knowledge or Biocultural Label, taonga provenance, community protocol, access permission, withdrawal, correction, repatriation, remedy, iwi and hapū governance, affected-party review, and Māori-authority reservation", "indigenous-archive-authority-rail", "Freed ID/CBR Heart", "exact_gate", ["SRC-LOCAL-CONTEXTS", "SRC-MAORI-DATA"], "No frozen row isolates Local Contexts label decisions together with taonga provenance, repatriation, remedy, iwi and hapū governance, and Māori authority in one reservation matrix."),
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
            "superselection localization",
            "phase-space nuclearity",
            "Cauchy evolution",
            "scaling algebra",
            "ResourceSync change audit",
            "preservation levels",
            "format characterization",
            "archival package integrity",
            "transparency draft status",
            "Indigenous archive authority",
        ],
        1,
    )
]

SKILL_IDEAS = [
    ("ghc-family-superselection-localization-ledger", "Review localized-sector, transportability, conjugate, and observation-firewall obligations."),
    ("ghc-family-phase-space-nuclearity-guard", "Review nuclearity-map scope without promoting compactness to physical stability."),
    ("ghc-family-cauchy-evolution-boundary", "Review time-slice and relative-Cauchy-evolution contracts without empirical promotion."),
    ("ghc-family-scaling-algebra-nonpromotion", "Review scaling families and limit-state nonuniqueness without ultraviolet-completion claims."),
    ("ghc-family-resourcesync-change-audit", "Review ResourceSync capability and change-state contracts without live harvesting."),
    ("ghc-family-preservation-levels-matrix", "Review preservation-level evidence and targets without certification."),
    ("ghc-family-format-characterization-boundary", "Separate format identification, well-formedness, validity, and characterization claims."),
    ("ghc-family-archival-package-integrity", "Review package hierarchy, fixity, profile, and interoperability refusal."),
    ("ghc-family-transparency-draft-watch", "Fail closed on draft Roughtime, Key Transparency, and COSE HPKE status or promotion."),
    ("ghc-family-indigenous-archive-authority-rail", "Reserve provenance, protocol, access, repatriation, remedy, iwi, hapū, and Māori authority."),
]

RUNNER_TASKS = [
    f"Build and invoke family-compatible bounded runner {index:02d} for {surface}."
    for index, (_name, surface) in enumerate(
        [
            ("sector", "superselection-localization"),
            ("nuclearity", "phase-space-nuclearity"),
            ("cauchy", "Cauchy-evolution"),
            ("scaling", "scaling-algebra"),
            ("resourcesync", "ResourceSync-change"),
            ("levels", "preservation-levels"),
            ("format", "format-characterization"),
            ("package", "archival-package-integrity"),
            ("draft", "transparency-draft-watch"),
            ("authority", "Indigenous-archive-authority"),
        ],
        1,
    )
]

RUNNER_IDEAS = [
    ("ghc_family_superselection_localization_guard.py", "superselection-localization"),
    ("ghc_family_phase_space_nuclearity_guard.py", "phase-space-nuclearity"),
    ("ghc_family_cauchy_evolution_guard.py", "Cauchy-evolution"),
    ("ghc_family_scaling_algebra_guard.py", "scaling-algebra"),
    ("ghc_family_resourcesync_change_guard.py", "ResourceSync-change"),
    ("ghc_family_preservation_levels_guard.py", "preservation-levels"),
    ("ghc_family_format_characterization_guard.py", "format-characterization"),
    ("ghc_family_archival_package_integrity.py", "archival-package-integrity"),
    ("ghc_family_transparency_draft_watch.py", "transparency-draft-watch"),
    ("ghc_family_indigenous_archive_authority_guard.py", "Indigenous-archive-authority"),
]

CLEAN_FIX_REFINE_TASKS = [
    f"REFINE-{index:02d}: review {row['slug']} terminology, falsifier, rollback, source status, and protected-gate wording without changing its frozen outcome class."
    for index, row in enumerate(PROPOSALS, 1)
]

X1_NEGATIVES = [
    (
        "V6534-X1-N01",
        "broad_memory_registry_search_timeout",
        "A broad memory-registry search timed out before returning any relevant match and received zero continuity credit.",
        "Use one exact fixed-string phase lookup with a bounded timeout and stop when it returns no relevant entry.",
    ),
    (
        "V6534-X1-N02",
        "combined_memory_skill_and_drive_probe_timeout",
        "A combined read-only memory-size, skill-discovery, and D-drive listing wrapper timed out before returning a coherent receipt.",
        "Split memory, skill, and D-drive inspection into separate bounded literal-path probes.",
    ),
    (
        "V6534-X1-N03",
        "exact_blob_aggregate_display_truncated",
        "The first exact-blob display of Ilyra's final overview was truncated by the tool and received zero complete-read credit.",
        "Read the same immutable blob in bounded, numbered line ranges and verify full first-to-last coverage.",
    ),
    (
        "V6534-X1-N04",
        "thread_list_limit_schema_rejection",
        "The first read-only task inventory requested a limit above the tool maximum and was rejected before returning titles.",
        "Use the declared maximum of fifty non-pinned tasks; pinned tasks remain included automatically.",
    ),
    (
        "V6534-X1-N05",
        "worktree_path_separator_registration_misclassification",
        "A separator-sensitive string comparison falsely reported Ilyra's registered worktree as absent and received zero registry credit.",
        "Normalize path separators or match the exact registry record before classifying worktree registration.",
    ),
    (
        "V6534-X1-N06",
        "worktree_add_wrapper_timeout_while_checkout_continued",
        "The additive worktree command exceeded its wrapper timeout while Git continued the authorized checkout in child processes.",
        "Do not retry; inspect relevant processes, wait for completion, then verify registration, branch, head, and clean state.",
    ),
    (
        "V6534-X1-N07",
        "combined_post_timeout_audit_wrapper_timeout",
        "The first combined path, registry, branch, head, and process audit also timed out and received zero recovery credit.",
        "Split filesystem, process, registry, Git identity, and clean-state checks into bounded probes.",
    ),
    (
        "V6534-X1-N08",
        "frozen_chain_index_array_key_assumption",
        "A provenance probe assumed a top-level proposals array that the declared index schema does not contain.",
        "Read top-level keys first, then combine prior_proposals and new_proposals exactly as the schema declares.",
    ),
    (
        "V6534-X1-N09",
        "overbroad_frozen_chain_projection_truncated",
        "An overbroad projection emitted the full 1,510-row frozen chain and was truncated, so it received zero full-audit display credit.",
        "Use deterministic all-row novelty scoring plus bounded fixed-term collision summaries rather than displaying the entire chain.",
    ),
    (
        "V6534-X1-N10",
        "multi_range_builder_inspection_exceeded_context",
        "A multi-range builder inspection produced more output than the active context could retain and therefore received zero review credit.",
        "Read and review one bounded builder range at a time before applying each exact-context patch.",
    ),
    (
        "V6534-X1-N11",
        "combined_status_and_search_probe_timed_out",
        "A combined worktree-status and multi-file search probe timed out before returning evidence and therefore received zero status or search credit.",
        "Run one-file, one-purpose status or search probes with bounded output and independently recorded results.",
    ),
    (
        "V6534-X1-N12",
        "powershell_search_pattern_unterminated",
        "A quoting-sensitive PowerShell search pattern was parsed as an unterminated string and therefore produced no inspection evidence.",
        "Use a literal single-quoted bounded search pattern that contains no shell interpolation.",
    ),
    (
        "V6534-X1-N13",
        "staged_validator_bootstrap_flag_omitted",
        "The first staged-validator invocation omitted the required --write bootstrap flag, so the absent lifecycle receipts caused FileNotFoundError and the attempt received zero validation credit.",
        "Regenerate the x1 packet with this retained negative, restage the exact candidate, then invoke the validator once with --write before checking receipt freshness without --write.",
    ),
]

REJECTED_COLLISIONS = [
    "A Jost-Lehmann-Dyson row was rejected because V6486-P02 already isolates that commutator and spectral-support mechanism.",
    "A Reeh-Schlieder row was rejected because V6487-P02 already isolates cyclicity, separation, locality, and no-signalling obligations.",
    "A Bisognano-Wichmann row was rejected because V6495-P02 already isolates wedge modular flow and conjugation.",
    "An OCFL row was rejected because V6498-P11 already isolates inventory, version, digest, content path, extension, and fixity.",
    "A PREMIS row was rejected because V6498-P10 already isolates preservation events, agents, objects, rights, and outcomes.",
    "A BagIt row was rejected because V6497-P07 already isolates declaration, payload, manifests, fetch, checksum, and refusal.",
    "A WARC row was rejected because V6492-P07 already isolates record types, identifiers, digests, revisits, and truncation.",
    "A RO-Crate row was rejected because V6493-P01 already isolates root data, contextual entities, parts, checksums, and orphan quarantine.",
    "A generic Sigstore bundle row was rejected because V6513-P02 already isolates bundle media type, verification material, inclusion, and checkpoint.",
    "A SCITT row was rejected because V6468-P05 already isolates signed and transparent statements, receipts, and policy registration.",
]
