#!/usr/bin/env python3
"""Frozen Sable Rook v653-v5 x1 data.

This module contains preregistration inputs only. It deliberately contains no
x2 observations, mutation outcomes, completion receipts, or route result.
"""

from __future__ import annotations


PHASE = "v653-v5"
PHASE_ID = "v653-gmut-thos-v5-x1-x2"
OWNER = "Sable Rook"
PRONOUNS = "they/them"
ROLE = "relational evidence-and-reproducibility steward"
HOPE = (
    "make every surviving claim easy to challenge, reproduce, or retract"
)
PHASE_ROOT = "docs/sable-rook/v653-v5"
BRANCH = "codex/GHC-Family/sable-rook-v653-v5-full-tools"

SOURCE_BRANCH = "codex/GHC-Family/auren-lark-v653-v4-full-tools"
SOURCE_PARENT = "431c8f0dcbc837cd87d63776771a802878a62c25"
SOURCE_X1 = "db90fae5fad768233a7c812c484c3907ceb07584"
SOURCE_EVIDENCE = "c75956f62b8aa2046405aa9be9a2c2d72276a347"
SOURCE_HEAD = "78a34e98758362bae231eaec1f4a8b08b9f787dc"

PRIOR_FROZEN = 1540
INHERITED_NEGATIVES = 9945
INHERITED_OPEN_GAPS = 73
INHERITED_EXACT_GATES = 74
INHERITED_METHOD_FLOW_FAILED = 18
INHERITED_METHOD_FLOW_PASSING = 18
PRIMARY_FOCUS = "GMUT Mind"
BOUNDED_PRACTICE = (
    "public-library conservation-laboratory collection-environment logging, "
    "treatment-proposal review, condition-note correction, accessible notice, "
    "workload control, and handover"
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
        "SRC-HOLLANDS-WALD-WICK",
        "stable",
        "primary_paper",
        "Local Wick Polynomials and Time Ordered Products of Quantum Fields in Curved Spacetime",
        "https://arxiv.org/abs/gr-qc/0103074",
        "Supports locality, covariance, scaling, continuity, and finite-renormalization obligations without constructing or confirming GMUT.",
    ),
    (
        "SRC-BUCHHOLZ-LTE",
        "stable",
        "primary_paper",
        "Thermodynamic Properties of Non-Equilibrium States in Quantum Field Theory",
        "https://arxiv.org/abs/hep-ph/0105051",
        "Supports local thermal observables, reference KMS states, thermal functions, and local-stability classes without a temperature observation or GMUT result.",
    ),
    (
        "SRC-ARAKI-RELATIVE-ENTROPY",
        "stable",
        "primary_paper",
        "Relative Entropy of States of von Neumann Algebras",
        "https://doi.org/10.2977/prims/1195191148",
        "Supports relative-modular-operator and monotonicity typing without an empirical information or gravity claim.",
    ),
    (
        "SRC-CONNES-COCYCLE",
        "stable",
        "primary_paper",
        "Une classification des facteurs de type III",
        "https://doi.org/10.24033/asens.1247",
        "Supports modular-weight and cocycle-derivative obligations without interpreting modular flow as observed physical time.",
    ),
    (
        "SRC-WIESBROCK-HSMI",
        "stable",
        "primary_paper",
        "Half-sided modular inclusions of von Neumann algebras",
        "https://doi.org/10.1007/BF02098019",
        "Supports inclusion, cyclic-separating vector, modular-flow, and positive-generator obligations without reconstructing GMUT.",
    ),
    (
        "SRC-ARVESON-AUTOMORPHISMS",
        "stable",
        "primary_paper",
        "On groups of automorphisms of operator algebras",
        "https://doi.org/10.1016/0022-1236(74)90034-2",
        "Supports spectral-subspace and positive-energy implementer obligations without a physical spectrum or conserved-energy result.",
    ),
    (
        "SRC-WIGHTMAN-VACUUM",
        "stable",
        "primary_paper",
        "Quantum Field Theory in Terms of Vacuum Expectation Values",
        "https://doi.org/10.1103/PhysRev.101.860",
        "Supports distribution, covariance, spectrum, locality, positivity, and reconstruction obligations without proving a GMUT field theory.",
    ),
    (
        "SRC-BROWDER-EDGE",
        "stable",
        "primary_paper",
        "On the Edge of the Wedge Theorem",
        "https://doi.org/10.4153/CJM-1963-015-4",
        "Supports tube-domain, common-boundary, and analytic-continuation obligations without deriving a GMUT amplitude or prediction.",
    ),
    (
        "SRC-PAQFT-ADIABATIC",
        "stable",
        "primary_paper",
        "Perturbative Algebraic Quantum Field Theory and the Renormalization Groups",
        "https://arxiv.org/abs/0901.2038",
        "Supports local S-matrix, cocycle, and algebraic adiabatic-limit obligations without an interacting GMUT construction.",
    ),
    (
        "SRC-PUSZ-WORONOWICZ",
        "stable",
        "primary_paper",
        "Passive states and KMS states for general quantum systems",
        "https://doi.org/10.1007/BF01614224",
        "Supports passivity, complete-passivity, KMS, and ground-state distinctions without a psyche or consciousness conversion.",
    ),
    (
        "SRC-AQFT-REVIEW",
        "stable",
        "primary_review",
        "Algebraic Quantum Field Theory",
        "https://arxiv.org/abs/math-ph/0602036",
        "Supports net, commutant, duality, and superselection terminology without proving Haag duality for GMUT.",
    ),
    (
        "SRC-LONGO-INDEX",
        "stable",
        "primary_paper",
        "Index of subfactors and statistics of quantum fields. I",
        "https://doi.org/10.1007/BF02125124",
        "Supports canonical-endomorphism, conjugate-sector, and index-statistics obligations without identifying a physical sector.",
    ),
    (
        "SRC-ISO-11799",
        "current",
        "official_standard",
        "ISO 11799:2024 document storage requirements for archive and library materials",
        "https://www.iso.org/standard/82306.html",
        "Supports repository-characteristic and mixed-media zoning fields without certifying a facility or professional practice.",
    ),
    (
        "SRC-NEDCC-ENV-MONITOR",
        "current",
        "official_guidance",
        "NEDCC Monitoring Temperature and Relative Humidity",
        "https://www.nedcc.org/free-resources/preservation-leaflets/2.-the-environment/2.2-monitoring-temperature-and-relative-humidity",
        "Supports sensor, location, calibration, sampling, data-gap, and handover fixtures without real environmental evidence.",
    ),
    (
        "SRC-IPI-TWPI",
        "current",
        "official_guidance",
        "Image Permanence Institute New Tools for Preservation",
        "https://store.imagepermanenceinstitute.org/new-tools-preservation",
        "Supports time-weighted preservation-index inputs and uncertainty fields without collection-life prediction or certification.",
    ),
    (
        "SRC-CCI-AGENTS",
        "current",
        "official_guidance",
        "Canadian Conservation Institute Agents of Deterioration",
        "https://www.canada.ca/en/conservation-institute/services/agents-deterioration.html",
        "Supports avoid, block, detect, respond, and agent-specific risk fields without a real collection decision.",
    ),
    (
        "SRC-AIC-CODE",
        "current",
        "professional_guidance",
        "American Institute for Conservation Code of Ethics and Guidelines for Practice",
        "https://www.culturalheritage.org/conservation-at-work/uphold-professional-standards/code",
        "Supports examination, proposal, consent, confidentiality, and documentation reservations without conferring professional status.",
    ),
    (
        "SRC-MUSEUMPESTS",
        "current",
        "official_practice_guidance",
        "Integrated Pest Management for Cultural Heritage monitoring guidance",
        "https://museumpests.net/monitoring-introduction/",
        "Supports trap, zone, count, identification, threshold, and recheck fixtures without pest-control authority or a live program.",
    ),
    (
        "SRC-LOC-LIGHT",
        "current",
        "official_guidance",
        "Library of Congress Limiting Light Damage",
        "https://www.loc.gov/preservation/care/light.html",
        "Supports cumulative exposure, lux, duration, ultraviolet, and access-tradeoff fields without a display authorization.",
    ),
    (
        "SRC-GETTY-MICROFADE",
        "current",
        "official_research_guidance",
        "Getty Conservation Institute Microfading Tester: Light Sensitivity Assessment and Role in Lighting Policy",
        "https://www.getty.edu/conservation/publications_resources/pdf_publications/microfading_tester.html",
        "Supports reference, spot, reflectance, Blue Wool, uncertainty, and policy-boundary fixtures without permission to test an object.",
    ),
    (
        "SRC-BM-ODDY",
        "current",
        "official_practice_guidance",
        "British Museum Oddy test fiftieth-anniversary method account",
        "https://www.britishmuseum.org/blog/metal-protector-celebrating-50-years-oddy-test",
        "Supports test-material, coupon, control, temperature, duration, and observation fields without materials approval or lab competence.",
    ),
    (
        "SRC-LOC-WET",
        "current",
        "official_guidance",
        "Library of Congress Salvaging Wet Collections",
        "https://guides.loc.gov/wet-collections",
        "Supports triage, human-safety, format, time, freezing, drying, and escalation fields without authorizing an emergency intervention.",
    ),
    (
        "SRC-FADGI-STILL",
        "current",
        "official_guidance",
        "FADGI Technical Guidelines for Digitizing Cultural Heritage Materials, Third Edition",
        "https://www.digitizationguidelines.gov/guidelines/digitize-technical.html",
        "Supports target, scale, lighting, color-space, capture, and quality-control fields without digitization certification.",
    ),
    (
        "SRC-SD-CWT",
        "draft",
        "official_active_draft",
        "IETF Selective Disclosure CBOR Web Tokens",
        "https://datatracker.ietf.org/doc/draft-ietf-spice-sd-cwt/",
        "Supports a draft-only disclosure, digest, salt, holder, and verification profile without real credentials or production status.",
    ),
    (
        "SRC-COSE-THUMBPRINT",
        "stable",
        "official_standard",
        "RFC 9679 COSE Key Thumbprint",
        "https://www.rfc-editor.org/rfc/rfc9679.html",
        "Supports deterministic key-member and thumbprint fixtures without real keys, proof of control, or trust governance.",
    ),
    (
        "SRC-ACME-ARI",
        "stable",
        "official_standard",
        "RFC 9773 ACME Renewal Information Extension",
        "https://www.rfc-editor.org/rfc/rfc9773.html",
        "Supports renewal-window, retry, replacement, and invalid-window fixtures without operating an ACME service.",
    ),
    (
        "SRC-VC-BARCODES",
        "draft",
        "official_working_draft",
        "W3C Verifiable Credential Barcodes v1.0",
        "https://www.w3.org/TR/vc-barcodes/",
        "Supports a working-draft optical-barcode profile without real credentials, scanners, issuers, holders, or verifier interoperability.",
    ),
    (
        "SRC-OAUTH-CIMD",
        "draft",
        "official_active_draft",
        "IETF OAuth Client ID Metadata Document",
        "https://datatracker.ietf.org/doc/draft-ietf-oauth-client-id-metadata-document/",
        "Supports a draft URL-client-id and metadata-fetch profile without registration, network, reputation, or production trust evidence.",
    ),
    (
        "SRC-LAMOST-DR",
        "current",
        "official_data_documentation",
        "LAMOST official data-release table",
        "https://www.lamost.org/lmusers/",
        "Supports release-state and public-versus-internal refusal fields without downloading or interpreting data.",
    ),
    (
        "SRC-LAMOST-API",
        "current",
        "official_api_documentation",
        "LAMOST Data Access OpenAPI",
        "https://www.lamost.org/openapi/docs",
        "Supports endpoint, table, schema, query, version, and authorization obligations with zero network query and zero rows.",
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
            "treatment, access, return, repatriation, legal, cultural, Māori-"
            "authority, affected-party, accessibility-complete, remedy, or "
            "governance decision."
        )
    return {
        "proposal_id": f"V6535-P{number:02d}",
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
        "novelty_against_1540_frozen_proposals": novelty,
    }


PROPOSAL_SPECS = [
    ("GMUT Hollands-Wald local Wick-polynomial field, time-ordered-product locality, covariance, scaling, metric continuity, commutator, finite-renormalization ambiguity, curvature coupling, and observation firewall", "hollands-wald-wick-covariance", "GMUT Mind", "completed", ["SRC-HOLLANDS-WALD-WICK"], "No frozen row isolates Hollands-Wald local covariant Wick polynomials with finite curvature-dependent renormalization freedom."),
    ("GMUT Buchholz-Ojima-Roos local-thermal observable, reference KMS state, thermal function, comparison map, local-equilibrium class, stability order, temperature reservation, entropy-density reservation, and observation firewall", "buchholz-ojima-roos-local-thermal-state", "GMUT Mind", "completed", ["SRC-BUCHHOLZ-LTE"], "No frozen row isolates the Buchholz-Ojima-Roos comparison of local observables with global KMS reference states and local thermal-stability classes."),
    ("GMUT Araki relative-entropy faithful normal states, relative modular operator, support, positivity, lower semicontinuity, convexity, monotonicity, channel scope, and observation firewall", "araki-relative-entropy-monotonicity", "GMUT Mind", "completed", ["SRC-ARAKI-RELATIVE-ENTROPY"], "No frozen row isolates Araki relative entropy through the relative modular operator and its monotonicity domain."),
    ("GMUT Connes cocycle-derivative normal faithful weights, modular automorphisms, unitary cocycle, chain rule, time parameter, support, outer-flow reservation, and observation firewall", "connes-cocycle-derivative", "GMUT Mind", "completed", ["SRC-CONNES-COCYCLE"], "No frozen row isolates the Connes cocycle derivative, modular covariance, and chain-rule obligations."),
    ("GMUT Wiesbrock half-sided modular inclusion, common cyclic-separating vector, modular operator, inclusion direction, semigroup, positive generator, translation relation, factor-type reservation, and observation firewall", "wiesbrock-half-sided-modular-inclusion", "GMUT Mind", "completed", ["SRC-WIESBROCK-HSMI"], "No frozen row isolates Wiesbrock half-sided modular-inclusion hypotheses and positive-translation conclusion."),
    ("GMUT Borchers-Arveson positive-energy implementer, automorphism group, Arveson spectrum, inner implementation, minimal generator, central ambiguity, strong continuity, and observation firewall", "borchers-arveson-positive-implementer", "GMUT Mind", "completed", ["SRC-ARVESON-AUTOMORPHISMS"], "No frozen row isolates positive-energy implementation, Arveson spectrum, and minimal-generator ambiguity."),
    ("GMUT Wightman reconstruction tempered distributions, test-function algebra, Poincare covariance, spectral support, locality, positivity, cluster reservation, Hilbert-space reconstruction, and observation firewall", "wightman-reconstruction-obligations", "GMUT Mind", "completed", ["SRC-WIGHTMAN-VACUUM"], "Distinct from the frozen Osterwalder-Schrader reconstruction and CPT rows because this surface starts from Wightman vacuum distributions and Hilbert-space positivity."),
    ("GMUT edge-of-the-wedge tube domains, holomorphic functions, distributional boundary values, common real edge, equality domain, envelope continuation, singularity reservation, and observation firewall", "edge-of-wedge-analytic-continuation", "GMUT Mind", "completed", ["SRC-BROWDER-EDGE"], "No frozen row isolates edge-of-the-wedge boundary-value equality and analytic continuation as a separate obligation set."),
    ("GMUT perturbative-AQFT algebraic adiabatic limit, local S-matrix, switching function, causal factorization, relative S-matrix, cocycle, local net, infrared reservation, and observation firewall", "paqft-algebraic-adiabatic-limit", "GMUT Mind", "completed", ["SRC-PAQFT-ADIABATIC"], "No frozen row isolates the algebraic adiabatic limit and switching-function independence of local observables."),
    ("GMUT Pusz-Woronowicz state passivity, cyclic work process, tensor powers, complete passivity, KMS state, ground state, inverse temperature, phase reservation, and psyche-nonconversion firewall", "pusz-woronowicz-complete-passivity", "GMUT Mind", "completed", ["SRC-PUSZ-WORONOWICZ"], "No frozen row isolates complete passivity and its KMS-or-ground-state characterization."),
    ("GMUT Haag-duality local net, causal complement, commutant, double-complement, essential-duality completion, additivity, topological-sector reservation, and observation firewall", "haag-essential-duality-comparison", "GMUT Mind", "completed", ["SRC-AQFT-REVIEW"], "No frozen row isolates Haag duality versus essential duality and additive completion as one comparison contract."),
    ("GMUT Longo canonical endomorphism, subfactor inclusion, conjugate endomorphism, Jones index, statistical dimension, canonical tower, finite-index scope, sector reservation, and observation firewall", "longo-canonical-endomorphism-index", "GMUT Mind", "completed", ["SRC-LONGO-INDEX"], "No frozen row isolates Longo canonical endomorphisms, conjugates, Jones index, and statistical dimension in one typed board."),
    ("THOS ISO 11799 repository siting, construction, renovation, equipment, mixed-media zone, compartment, environment, exception, revision, and noncertification board", "iso11799-library-storage-matrix", "THOS Body", "completed", ["SRC-ISO-11799"], "No frozen row isolates ISO 11799:2024 repository characteristics and mixed-media compartment boundaries."),
    ("THOS NEDCC temperature and relative-humidity sensor identifier, calibration, location, sampling cadence, clock, gap, drift, excursion, facilities handover, and noncertification board", "nedcc-environment-monitoring-handover", "THOS Body", "completed", ["SRC-NEDCC-ENV-MONITOR"], "No frozen row isolates collection-environment sensor calibration, placement, data gaps, and facilities handover."),
    ("THOS Image Permanence Institute time-weighted preservation index, temperature, relative humidity, sampling interval, preservation-index estimate, weighting, missingness, uncertainty, and nonprediction board", "ipi-time-weighted-preservation-index", "THOS Body", "completed", ["SRC-IPI-TWPI"], "No frozen row isolates time-weighted preservation-index inputs, weighting, gaps, and nonprediction boundaries."),
    ("THOS Canadian Conservation Institute agents-of-deterioration hazard, asset, location, avoid, block, detect, respond, evidence, priority, review, and professional-reservation matrix", "cci-agents-control-cycle", "THOS Body", "completed", ["SRC-CCI-AGENTS"], "No frozen row isolates the agents-of-deterioration avoid-block-detect-respond control cycle as a bounded matrix."),
    ("THOS AIC examination, sampling consent, treatment proposal, alternative, risk, dated action, material, alteration, confidentiality, permanent documentation, and professional-reservation board", "aic-treatment-documentation-boundary", "THOS Body", "completed", ["SRC-AIC-CODE"], "No frozen row isolates examination, consent, treatment planning, confidentiality, and permanent treatment documentation together."),
    ("THOS integrated-pest-management trap identifier, zone, placement, check date, taxon, count, trend, collection-specific action threshold, escalation, recheck, and nonoperational board", "ipm-trap-threshold-ledger", "THOS Body", "completed", ["SRC-MUSEUMPESTS"], "No frozen row isolates trap-level pest monitoring with a collection-specific threshold and recheck trail."),
    ("THOS cumulative light-dose source, illuminance, ultraviolet, duration, lux-hour, display cycle, dark-storage interval, sensitivity, access exception, and authority-reservation ledger", "cumulative-light-dose-ledger", "THOS Body", "completed", ["SRC-LOC-LIGHT"], "No frozen row isolates cumulative lux-hour exposure, display cycles, dark intervals, and documented access exceptions."),
    ("THOS Getty microfade-test object area, spot size, source spectrum, reflectance series, color difference, Blue Wool reference, stop rule, uncertainty, consent, and professional-reservation board", "microfade-dose-response-boundary", "THOS Body", "completed", ["SRC-GETTY-MICROFADE"], "No frozen row isolates microfade test dose-response, reference, stop, uncertainty, and permission obligations."),
    ("THOS British Museum Oddy-test material sample, silver-copper-lead coupons, blank control, vessel, water, temperature, duration, coupon observation, classification, and professional-reservation board", "oddy-coupon-control-tribunal", "THOS Body", "completed", ["SRC-BM-ODDY"], "No frozen row isolates the Oddy test sample, three coupons, blank control, accelerated exposure, and bounded classification."),
    ("THOS wet-library-material human-safety, contamination, format, saturation, elapsed time, separation, freezing eligibility, packing, drying route, escalation, and incident-handover board", "wet-collection-freezing-triage", "THOS Body", "completed", ["SRC-LOC-WET"], "No frozen row isolates wet-book and paper freezing eligibility, format exclusions, safety, and recovery handover."),
    ("THOS condition-photography object identifier, view, scale, gray target, color target, lighting, capture profile, file checksum, correction lineage, and noncertification board", "condition-photography-target-lineage", "THOS Body", "completed", ["SRC-FADGI-STILL"], "No frozen row isolates condition-photography targets, capture conditions, checksum, and correction lineage without treatment or digitization certification."),
    ("Freed ID draft SD-CWT disclosure claim, digest, salt, decoy, key binding, holder proof, verifier input, overdisclosure refusal, draft status, and nonproduction profile", "sd-cwt-draft-disclosure-profile", "Freed ID/CBR Heart", "represented", ["SRC-SD-CWT"], "No frozen row isolates the active SD-CWT draft disclosure and key-binding grammar."),
    ("Freed ID RFC 9679 COSE Key Thumbprint key type, required members, deterministic encoding, hash algorithm, thumbprint, URI, entropy warning, transformation caveat, and nonproduction profile", "cose-key-thumbprint-profile", "Freed ID/CBR Heart", "represented", ["SRC-COSE-THUMBPRINT"], "No frozen row isolates RFC 9679 COSE Key Thumbprints and their symmetric-key and transformed-key caveats."),
    ("Freed ID RFC 9773 ACME renewal-info directory, certificate identifier, suggested window, retry-after, fallback, replacement, already-replaced error, invalid-window refusal, and nonproduction profile", "acme-ari-renewal-window-profile", "Freed ID/CBR Heart", "represented", ["SRC-ACME-ARI"], "No frozen row isolates ACME ARI renewal windows, retry semantics, replacement linkage, and invalid-window refusal."),
    ("Freed ID W3C draft VC Barcode credential payload, CBOR-LD compression, optical symbol, issuer material, holder data, verifier algorithm, size budget, disclosure, draft status, and nonproduction profile", "vc-barcode-draft-profile", "Freed ID/CBR Heart", "represented", ["SRC-VC-BARCODES"], "No frozen row isolates the 2026 W3C VC Barcodes working draft and its compact optical representation boundary."),
    ("Freed ID draft OAuth Client ID Metadata Document HTTPS client identifier, fetched metadata, exact identifier match, redirect URI, cache, origin, shared-secret refusal, reputation warning, draft status, and nonproduction profile", "oauth-client-id-metadata-draft-profile", "Freed ID/CBR Heart", "represented", ["SRC-OAUTH-CIMD"], "No frozen row isolates the OAuth Client ID Metadata Document URL-fetch and unregistered-client boundary."),
    ("GMUT LAMOST public-release version, low and medium resolution product, table schema, target, wavelength, radial velocity, quality flag, selection, checksum, covariance, and zero-row likelihood-refusal adapter", "lamost-dr11-zero-row-adapter", "GMUT Mind", "open_gap", ["SRC-LAMOST-DR", "SRC-LAMOST-API"], "No frozen row isolates a LAMOST public-release and OpenAPI adapter with zero query, zero download, zero rows, and likelihood refusal."),
    ("CBR public-library conservation treatment, condition image, access restriction, digitization, return, repatriation, taonga provenance, mātauranga, remedy, affected-party review, iwi and hapū governance, and Māori-authority reservation", "library-conservation-authority-rail", "Freed ID/CBR Heart", "exact_gate", ["SRC-LOCAL-CONTEXTS", "SRC-MAORI-DATA"], "No frozen row isolates public-library conservation treatment, access, digitization, return, repatriation, taonga, mātauranga, iwi and hapū governance, and Māori authority in one reservation matrix."),
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
            "local Wick covariance",
            "modular-information typing",
            "half-sided modular inclusion",
            "positive-energy implementation",
            "Wightman reconstruction",
            "library environment monitoring",
            "light and microfade exposure",
            "treatment documentation",
            "identity-draft status",
            "library conservation authority",
        ],
        1,
    )
]

SKILL_IDEAS = [
    ("ghc-family-wick-covariance-ledger", "Review local Wick-field covariance and finite-renormalization obligations without physical promotion."),
    ("ghc-family-modular-information-boundary", "Review relative entropy and cocycle typing without converting modular quantities into observed physics."),
    ("ghc-family-half-sided-inclusion-guard", "Review half-sided modular-inclusion hypotheses and positive-generator conclusions."),
    ("ghc-family-positive-implementer-scope", "Review Arveson spectrum and positive-energy implementation with central-ambiguity reservation."),
    ("ghc-family-wightman-reconstruction-firewall", "Review distribution, spectrum, locality, positivity, and reconstruction fields without constructing a theory."),
    ("ghc-family-library-environment-monitor", "Review sensor calibration, location, cadence, missingness, and handover fields without facility certification."),
    ("ghc-family-light-dose-microfade-rail", "Review cumulative exposure and microfade uncertainty without testing or authorizing an object."),
    ("ghc-family-treatment-documentation-rail", "Review examination, proposal, consent, confidentiality, and correction lineage without professional authority."),
    ("ghc-family-identity-draft-status-watch", "Fail closed on SD-CWT, VC Barcode, and Client ID Metadata draft status or production promotion."),
    ("ghc-family-library-conservation-authority-rail", "Reserve treatment, access, digitization, return, repatriation, taonga, mātauranga, iwi, hapū, and Māori authority."),
]

RUNNER_TASKS = [
    f"Build and invoke family-compatible bounded runner {index:02d} for {surface}."
    for index, surface in enumerate(
        [
            "wick-covariance",
            "modular-information",
            "half-sided-inclusion",
            "positive-implementer",
            "Wightman-reconstruction",
            "library-environment",
            "light-dose-microfade",
            "treatment-documentation",
            "identity-draft-watch",
            "library-authority",
        ],
        1,
    )
]

RUNNER_IDEAS = [
    ("ghc_family_wick_covariance_guard.py", "wick-covariance"),
    ("ghc_family_modular_information_guard.py", "modular-information"),
    ("ghc_family_half_sided_inclusion_guard.py", "half-sided-inclusion"),
    ("ghc_family_positive_implementer_guard.py", "positive-implementer"),
    ("ghc_family_wightman_reconstruction_guard.py", "Wightman-reconstruction"),
    ("ghc_family_library_environment_guard.py", "library-environment"),
    ("ghc_family_light_dose_microfade_guard.py", "light-dose-microfade"),
    ("ghc_family_treatment_documentation_guard.py", "treatment-documentation"),
    ("ghc_family_identity_draft_watch.py", "identity-draft-watch"),
    ("ghc_family_library_conservation_authority_guard.py", "library-authority"),
]

CLEAN_FIX_REFINE_TASKS = [
    f"REFINE-{index:02d}: review {row['slug']} terminology, falsifier, rollback, source status, and protected-gate wording without changing its frozen outcome class."
    for index, row in enumerate(PROPOSALS, 1)
]

X1_NEGATIVES = [
    (
        "V6535-X1-N01",
        "memory_registry_relative_path_miss",
        "The first memory-registry lookup used a repository-relative path that did not identify the memory registry and received zero continuity credit.",
        "Use the verified memory-root-relative literal path and limit the lookup to current Sable and exact-closeout terms.",
    ),
    (
        "V6535-X1-N02",
        "immutable_activation_pipe_closed_early",
        "The first immutable activation display piped Git output into a first-lines consumer; the closed pipe produced a nonzero exit and no complete-read credit.",
        "Materialize the immutable Git blob completely before bounded line slicing and verify first-to-last coverage.",
    ),
    (
        "V6535-X1-N03",
        "multi_file_size_probe_timeout",
        "A combined size probe across fifteen required files timed out before a coherent receipt and received zero review credit.",
        "Use one exact tree listing and then inspect required files in bounded, one-purpose ranges.",
    ),
    (
        "V6535-X1-N04",
        "combined_drive_status_identity_probe_timeout",
        "A combined D-drive, Git status, and identity probe timed out without a coherent receipt.",
        "Split capacity, branch identity, remote equality, and worktree cleanliness into separate bounded probes.",
    ),
    (
        "V6535-X1-N05",
        "powershell_hash_literal_parse_failure",
        "A combined branch and path-existence probe used a quoting-sensitive PowerShell hash literal and failed before producing evidence.",
        "Use separate native Git and literal-path checks, then construct summaries only after each command completes.",
    ),
    (
        "V6535-X1-N06",
        "combined_new_lane_postflight_timeout",
        "The first combined new-worktree branch, head, upstream, and cleanliness postflight timed out and received zero lane credit.",
        "Split registration, exact head, upstream, status, and live-remote equality into bounded probes without retrying mutation.",
    ),
    (
        "V6535-X1-N07",
        "bounded_file_inventory_pipe_nonzero",
        "A bounded file-inventory pipeline returned a nonzero status after emitting no selected rows and received zero inventory credit.",
        "Use an exact literal phase pattern or a materialized list before selection, and distinguish no-match from tool failure.",
    ),
    (
        "V6535-X1-N08",
        "overbroad_primary_source_search_truncated",
        "A broad multi-topic primary-source search returned unrelated and truncated results, so it received zero source-selection credit.",
        "Use bounded exact-title or official-domain searches and retain only directly reviewed primary or official records.",
    ),
    (
        "V6535-X1-N09",
        "semantic_novelty_threshold_rejected_qei_duplicate",
        "The first x1 build stopped before materialization because the proposed quantum-energy-inequality row matched an inherited QEI mechanism at the frozen novelty threshold.",
        "Retain the failed build with zero credit, replace the duplicate with the mechanism-distinct Buchholz-Ojima-Roos local-thermal-observable contract, and rerun the unexecuted x1 build.",
    ),
    (
        "V6535-X1-N10",
        "powershell_null_coalescing_operator_unsupported",
        "A read-only generated-receipt summary used the null-coalescing operator unavailable in Windows PowerShell 5.1 and failed before reading any evidence.",
        "Read exact properties with explicit conditional checks in Windows PowerShell 5.1, then construct the bounded summary.",
    ),
    (
        "V6535-X1-N11",
        "x1_staged_receipt_fixed_point_stale",
        "The first read-only x1 receipt-freshness check ran after the three lifecycle receipts were newly staged, so the pre-receipt snapshot no longer matched the exact staged surface and received zero aggregate validation credit.",
        "Rebuild the immutable x1 packet with the failure retained, stage the exact surface, compute the self-excluding receipt fixed point with all receipt paths present, restage those receipts, and require a read-only freshness pass.",
    ),
]

REJECTED_COLLISIONS = [
    "A Peierls-bracket row was rejected because a frozen row already isolates that causal functional-bracket mechanism.",
    "An Epstein-Glaser row was rejected because frozen causal-renormalization rows already isolate that extension mechanism.",
    "An Osterwalder-Schrader row was rejected because a frozen row already isolates reflection positivity and Euclidean reconstruction.",
    "A Källén-Lehmann row was rejected because a frozen row already isolates spectral-measure and pole-continuum obligations.",
    "A Reeh-Schlieder row was rejected because a frozen row already isolates cyclicity, separation, locality, and no-signalling obligations.",
    "A Tomita-Takesaki row was rejected because frozen modular-flow rows already isolate that mechanism; the new rows instead isolate relative and inclusion structures.",
    "A PREMIS row was rejected because a frozen row already isolates preservation events, agents, objects, rights, and outcomes.",
    "A BagIt row was rejected because a frozen row already isolates declaration, payload, manifests, fetch, checksum, and refusal.",
    "An IIIF row was rejected because frozen image-API and presentation rows already isolate those interoperability surfaces.",
    "A Fermi-LAT 4FGL-DR4 adapter was rejected because an inherited row already isolates that exact official data product and zero-row mechanism.",
    "A quantum-energy-inequality row was rejected by the exact novelty scorer because V6518-P02 already isolates the sampling, state-domain, stress-tensor, and lower-bound mechanism.",
]
