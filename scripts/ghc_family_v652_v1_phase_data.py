#!/usr/bin/env python3
"""Frozen Sable Rook v652-v1 x1 data with no x2 observations."""

from __future__ import annotations


PHASE = "v652-v1"
OWNER = "Sable Rook"
PRONOUNS = "they/them"
ROLE = "relational evidence-and-reproducibility steward"
HOPE = "keep every surviving claim easy to challenge, reproduce within scope, and retract"
BRANCH = "codex/GHC-Family/sable-rook-full-tools"
PHASE_ROOT = "docs/sable-rook/v652-v1"

SOURCE_BRANCH = "codex/GHC-Family/ilyra-fen-v651-v8-special-cli-prep"
SOURCE_HEAD = "4b31ec3d1bb4db24f48967da5c4e27a05b43e1f9"
SOURCE_ORIGIN = "68f7e9b7fc454746c02b8a85987e10b87a0725c3"
SOURCE_X1 = "580a3f0155c589866fd7f4aacd88790419cd147a"
SOURCE_EVIDENCE = "0b382d660837536e12672e28cc68f6208e2b0069"
PRIOR_FROZEN = 1180
INHERITED_NEGATIVES = 7856
INHERITED_OPEN_GAPS = 61
INHERITED_EXACT_GATES = 62
PRIMARY_FOCUS = "Freed ID and CBR Heart"
BOUNDED_PRACTICE = (
    "court-registry exhibit accession, sealed-record custody, correction readback, accessible notice, "
    "workload control, and shift handover as a synthetic learning and design lens only"
)

OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]
SOURCE_STATUS_CLASSES = ["current", "stable", "draft", "watch"]
PROTECTED_GATES = [
    "empirical_data",
    "real_participants_or_operators",
    "professional_or_court_authority",
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


def _proposal(number, title, slug, pillar, disposition, source_ids, mission, novelty):
    if disposition == "open_gap":
        approval = "candidate_empirical_data_and_independent_review_required"
        lane = "x2_zero_row_readiness_only"
        gate = (
            "Emit a zero-row refusal receipt with zero query, download, ingest, fit, likelihood, "
            "posterior, constraint, prediction, or empirical promotion."
        )
    elif disposition == "exact_gate":
        approval = "exact_affected_party_competent_court_and_maori_authority_required"
        lane = "x2_reservation_matrix_only"
        gate = (
            "Emit unresolved decision rights and reservations only; make no access, sealing, disclosure, "
            "remedy, legal, cultural, data-governance, or Māori-authority decision."
        )
    elif disposition == "represented":
        approval = "candidate_bounded_synthetic_proxy"
        lane = "x2_synthetic_proxy_only"
        gate = (
            "Reject every preregistered mutation and retain represented status with zero production, "
            "participant, operational, professional, interoperability, or authority credit."
        )
    else:
        approval = "safe_now_bounded_software_symbolic_formal_or_structural"
        lane = "x2_bounded_owner_local"
        gate = (
            "Reject every preregistered mutation and emit only the declared bounded software, symbolic, "
            "formal, structural, or workflow completion."
        )
    return {
        "proposal_id": f"V6521-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar": pillar,
        "mission_surface": mission,
        "hypothesis": (
            f"A bounded {mission} artifact can expose its declared obligations while refusing unsupported "
            "scientific, operational, identity, accessibility, or authority promotion."
        ),
        "null_or_failure_condition": (
            f"The artifact omits a declared {mission} obligation, accepts a preregistered mutation, erases "
            "a failure, crosses an approval boundary, or promotes beyond its evidence lane."
        ),
        "approval_class": approval,
        "execution_lane": lane,
        "official_or_primary_source_needs": source_ids,
        "concrete_artifacts": [
            f"surfaces/{slug}/contract.json",
            f"surfaces/{slug}/mutation-results.json",
            f"surfaces/{slug}/bounded-receipt.json",
        ],
        "falsifier_or_acceptance_gate": gate,
        "rollback_or_recovery": (
            "Stop the proposal, retain every failed witness, rewrite no history, and leave external, sibling, "
            "participant, production, professional, legal, cultural, and authority state unchanged."
        ),
        "protected_gates": PROTECTED_GATES,
        "expected_disposition": disposition,
        "novelty_against_1180_frozen_proposals": novelty,
    }


PROPOSALS = [
    _proposal(1, "Evidence claim lease, expiry, renewal, supersession, retraction, dependent-demotion, noncompensation, and lineage tribunal", "claim-lease-demotion", "Trinity Mandala bridge", "completed", ["SRC-W3C-PROV"], "claim lifecycle and dependent demotion", "Prior invalidation work does not isolate renewable claim leases, expiry-triggered demotion, dependency propagation, noncompensation, and retained lineage together."),
    _proposal(2, "Git cruft-pack mtime sideband, unreachable-object horizon, promisor exclusion, duplicate-object, checksum, expiry, rescue, and refusal tribunal", "git-cruft-pack", "THOS Body", "completed", ["SRC-GIT-CRUFT"], "Git cruft-pack retention control", "Earlier pack and multi-pack work does not isolate cruft mtimes, expiry horizons, promisor exclusions, duplicate unreachable objects, rescue, and refusal behavior."),
    _proposal(3, "OCI Distribution referrers, subject digest, artifact manifest, repository scope, media type, pagination, fallback tag, deletion race, and refusal tribunal", "oci-referrers", "THOS Body", "completed", ["SRC-OCI-DISTRIBUTION", "SRC-OCI-IMAGE"], "OCI referrer provenance control", "Prior OCI layer work does not isolate subject-linked artifact manifests, referrer discovery, pagination, fallback tags, repository scope, and deletion races."),
    _proposal(4, "GMUT Belinfante-Rosenfeld canonical stress, spin current, improvement divergence, tensor symmetry, on-shell conservation, boundary term, unit, EFT-scope, and observation-firewall board", "belinfante-rosenfeld", "GMUT Mind", "completed", ["SRC-BELINFANTE"], "Belinfante-Rosenfeld stress-tensor obligations", "No frozen title isolates canonical stress improvement by spin current, symmetry, on-shell conservation, boundary terms, units, and observation refusal."),
    _proposal(5, "GMUT Dirac-Bergmann primary constraint, secondary constraint, consistency chain, first-class, second-class, total Hamiltonian, multiplier, gauge generator, unit, EFT-scope, and observation-firewall board", "dirac-bergmann-constraints", "GMUT Mind", "completed", ["SRC-DIRAC-BERGMANN"], "Dirac-Bergmann constraint obligations", "No inherited title isolates primary and secondary constraint chains, consistency, first and second class separation, total Hamiltonians, multipliers, gauge generators, units, and observation refusal."),
    _proposal(6, "GMUT Noether-second-theorem gauge generator, differential identity, off-shell Euler-Lagrange relation, boundary term, constraint map, unit, EFT-scope, and observation-firewall board", "noether-second-theorem", "GMUT Mind", "completed", ["SRC-NOETHER"], "Noether second-theorem obligations", "No frozen proposal isolates differential gauge generators, off-shell Euler-Lagrange identities, boundary terms, constraint maps, units, and observation refusal."),
    _proposal(7, "GMUT Hadamard-parametrix geodesic-neighbourhood, wavefront set, U-V-W coefficient, state dependence, subtraction, curvature, unit, EFT-scope, and observation-firewall board", "hadamard-parametrix", "GMUT Mind", "completed", ["SRC-HADAMARD"], "Hadamard-parametrix obligations", "Earlier microlocal work does not isolate local geodesic domains, U-V-W coefficients, state-dependent smooth terms, subtraction, curvature, units, and observation refusal."),
    _proposal(8, "Canonical GMUT Omega-sector decomposition, covariant-divergence, exchange-current, mass-dimension, sign, background, stability, identifiability, and observation-firewall board", "canonical-omega-sector", "GMUT Mind", "completed", ["SRC-GMUT-CANONICAL", "SRC-WALD-GR"], "canonical GMUT Omega-sector typing and conservation", "The canonical register and earlier exchange-current board do not jointly isolate the frozen Omega decomposition, mass dimensions, sign conventions, background domain, stability and identifiability firewalls."),
    _proposal(9, "C2PA JUMBF manifest-store, claim, assertion, ingredient, redaction, update-manifest, signature-box, hash-link, resource-budget, and refusal tribunal", "c2pa-jumbf", "THOS Body", "completed", ["SRC-C2PA"], "C2PA manifest structural refusal", "No frozen proposal isolates C2PA JUMBF stores, claims, assertions, ingredients, redaction, update manifests, signature boxes, hash links, and budgets."),
    _proposal(10, "SARIF 2.1.0 result fingerprint, baseline state, suppression, artifact location, code flow, thread flow, taxon, redaction, resource-budget, and refusal tribunal", "sarif-result-lineage", "THOS Body", "completed", ["SRC-SARIF"], "SARIF result-lineage control", "No inherited proposal isolates SARIF fingerprints, baseline states, suppressions, locations, code and thread flows, taxonomies, redaction, and budgets."),
    _proposal(11, "Reproducible-build SOURCE_DATE_EPOCH archive-mtime, timezone, locale, path, ordering, uid-gid, umask, random-seed, dependency-lock, and refusal tribunal", "source-date-epoch", "THOS Body", "completed", ["SRC-REPRODUCIBLE-BUILDS"], "reproducible-build environment control", "No frozen title isolates SOURCE_DATE_EPOCH with archive mtimes, timezone, locale, paths, ordering, ownership metadata, umask, seeds, and locks."),
    _proposal(12, "Debian APT InRelease, Release, Packages, by-hash, Valid-Until, version, architecture, component, digest, rollback, freeze, and refusal tribunal", "debian-apt-metadata", "THOS Body", "completed", ["SRC-DEBIAN-REPOSITORY"], "Debian repository metadata refusal", "No inherited proposal isolates signed Release metadata, package indexes, by-hash acquisition, Valid-Until, architecture and component scoping, rollback and freeze refusal."),
    _proposal(13, "Python wheel RECORD path, urlsafe-digest, size, dist-info, data-scheme, script, symlink, duplicate, traversal, installation-budget, and refusal tribunal", "python-wheel-record", "THOS Body", "completed", ["SRC-PYPA-WHEEL"], "Python wheel RECORD refusal", "No frozen proposal isolates wheel RECORD path-digest-size triples, dist-info and data schemes, scripts, symlinks, duplicates, traversal, and budgets."),
    _proposal(14, "ZIP64 end-record, locator, central-directory offset, extra-field, data-descriptor, duplicate-name, overlap, traversal, expansion-budget, and refusal tribunal", "zip64-central-directory", "THOS Body", "completed", ["SRC-ZIP-APPNOTE"], "ZIP64 central-directory refusal", "Prior archive work does not isolate ZIP64 end records and locators, central offsets, extra fields, descriptors, duplicate names, overlap, traversal, and expansion budgets."),
    _proposal(15, "HDF5 superblock signature, version, offset-size, length-size, base-address, end-of-file address, free-space address, driver-info, extension, object-header, resource-budget, and refusal tribunal", "hdf5-superblock", "THOS Body", "completed", ["SRC-HDF5"], "HDF5 superblock refusal", "No frozen proposal isolates HDF5 superblock versions, address widths, base and end addresses, free-space and driver information, extensions, object headers, and budgets."),
    _proposal(16, "PDF incremental-update xref-table, xref-stream, object generation, free-list, trailer Prev chain, startxref, encryption-state, revision-budget, and refusal tribunal", "pdf-incremental-update", "THOS Body", "completed", ["SRC-PDF-REFERENCE"], "PDF incremental-update refusal", "No inherited proposal isolates incremental xref tables and streams, generations, free lists, Prev chains, startxref, encryption-state continuity, and revision budgets."),
    _proposal(17, "ELF note segment owner, type, name-size, descriptor-size, alignment, build-id, GNU property, duplicate, truncation, segment-budget, and refusal tribunal", "elf-note-segment", "THOS Body", "completed", ["SRC-ELF-GABI"], "ELF note structural refusal", "No frozen proposal isolates ELF note ownership and types, aligned name and descriptor sizes, build IDs, GNU properties, duplicates, truncation, and segment budgets."),
    _proposal(18, "Multiformats CIDv1 multibase, multicodec, multihash, varint-canonicality, digest-length, identity-hash, representation, resource-budget, and refusal tribunal", "multiformats-cidv1", "THOS Body", "completed", ["SRC-MULTIFORMATS"], "Multiformats CIDv1 refusal", "No inherited proposal isolates CIDv1 composition across multibase, multicodec, multihash, canonical varints, digest lengths, identity hashes, and budgets."),
    _proposal(19, "THOS court-registry exhibit accession, custody, seal-state, discrepancy-hold, correction-readback, accessible-notice, workload, and shift-handover proxy", "court-registry-handover", "THOS Body", "represented", ["SRC-ISO15489", "SRC-NZ-COURTS"], "court-registry custody handover", "No frozen practice proxy isolates exhibit accession, seal state, custody, discrepancy holds, correction readback, accessible notice, workload, and accepted handover."),
    _proposal(20, "THOS preregistered blind matched-budget court-registry comparator-arm, allocation, contamination, safety-stop, workload, missingness, analysis-lock, and independent-review proxy", "court-registry-matched-budget", "THOS Body", "represented", ["SRC-CONSORT"], "blind matched-budget court-registry evaluation design", "No inherited THOS proxy applies matched time and resource budgets, allocation concealment, contamination, safety stops, missingness, analysis locks, and independent review to this practice."),
    _proposal(21, "Freed ID ACME ARI certificate-identifier, suggested-window, Retry-After, fallback, replacement-link, already-replaced, cache, privacy, and nonproduction profile", "acme-ari", "Freed ID and CBR Heart", "represented", ["SRC-RFC9773", "SRC-RFC8555"], "ACME renewal-information identity lifecycle", "No frozen identity profile isolates ACME ARI identifiers, renewal windows, Retry-After, fallback schedules, replacement linkage, conflict state, caching, and privacy."),
    _proposal(22, "Freed ID SCIM cursor pagination cursor, nextCursor, previousCursor, count, sort, filter, invalid-cursor, expiry, consistency, privacy, and nonproduction profile", "scim-cursor-pagination", "Freed ID and CBR Heart", "represented", ["SRC-RFC-SCIM-CURSOR", "SRC-RFC7644"], "SCIM cursor-pagination lifecycle", "Earlier SCIM work does not isolate cursor creation and expiry, next and previous cursors, page counts, sort and filter consistency, invalid cursors, and privacy."),
    _proposal(23, "Freed ID FIDO Credential Exchange format, protocol, provider, importer, exporter, encryption-boundary, consent, duplicate, recovery, draft-status, and nonproduction profile", "fido-credential-exchange", "Freed ID and CBR Heart", "represented", ["SRC-FIDO-CREDENTIAL-EXCHANGE"], "FIDO credential-exchange draft profile", "No frozen profile isolates FIDO credential exchange format and protocol roles, import-export boundaries, consent, duplicates, recovery, and explicit working-draft status."),
    _proposal(24, "Accessible code-diff addition, deletion, unchanged-context, line-number, hunk-label, keyboard-order, wrap, contrast, table-alternative, and manual-evaluation structural audit", "accessible-code-diff", "THOS Body", "completed", ["SRC-WCAG22", "SRC-WAI-APG"], "accessible code-diff structure", "No inherited accessibility title isolates diff additions and deletions, unchanged context, line and hunk labelling, keyboard order, wrapping, contrast, and a table alternative."),
    _proposal(25, "W3C Web Annotation body, target, motivation, TextQuoteSelector, TextPositionSelector, refinedBy, state, canonical, privacy, resource-budget, and refusal tribunal", "web-annotation-selectors", "Freed ID and CBR Heart", "completed", ["SRC-WEB-ANNOTATION"], "Web Annotation selector provenance", "No frozen proposal isolates annotation bodies and targets, motivations, text quote and position selectors, refinement, state, canonical resources, privacy, and budgets."),
    _proposal(26, "Thermo-Psyche Widom-line response-function maximum, path dependence, crossover, critical-region, finite-size, observable choice, uncertainty, unit, and agency-nonconversion classifier", "widom-line-nonconversion", "Trinity Mandala bridge", "completed", ["SRC-WIDOM-LINE"], "Widom-line crossover nonconversion", "No frozen nonconversion classifier isolates response-function maxima, path and observable dependence, crossover versus transition, critical regions, finite size, uncertainty, units, and agency refusal."),
    _proposal(27, "Stage 20 multiverse-analysis decision-grid, specification-curve, vibration-of-effects, outcome-blinding, multiplicity, subgroup, missingness, uncertainty, and nonpromotion board", "multiverse-analysis", "Trinity Mandala bridge", "completed", ["SRC-MULTIVERSE"], "multiverse-analysis nonpromotion", "No inherited Stage 20 board isolates a frozen analysis decision grid, specification curve, vibration of effects, outcome blinding, multiplicity, subgroup and missingness uncertainty together."),
    _proposal(28, "Same-owner reproduction capsule dependency-lock, seed, locale, timezone, filesystem-order, build-path, network-refusal, output-manifest, drift, and independent-team-gap tribunal", "reproduction-capsule", "THOS Body", "completed", ["SRC-REPRODUCIBLE-BUILDS"], "same-owner reproduction capsule boundary", "No frozen proposal isolates dependency locks, seeds, locale, timezone, filesystem order, build paths, network refusal, manifests, drift, and the independent-team gap as one capsule."),
    _proposal(29, "GMUT Pan-STARRS1 DR2 stack-object, detection, mean-object, filter, astrometry, photometry, quality-flag, selection, covariance, provenance, checksum, and zero-row likelihood-refusal adapter", "panstarrs-dr2-zero-row", "GMUT Mind", "open_gap", ["SRC-PANSTARRS-DR2"], "Pan-STARRS1 DR2 likelihood readiness", "No inherited zero-row adapter targets the official Pan-STARRS1 DR2 stack, detection, and mean-object products with filter, astrometry, photometry, quality, selection, covariance, provenance, and checksum duties."),
    _proposal(30, "CBR sealed-case-file decision-rights reservation for exhibit inspection, suppression-order boundary, transcription correction, accessible service, retention, redress, tikanga context, and tangata-whenua governance", "court-registry-authority", "Freed ID and CBR Heart", "exact_gate", ["SRC-NZ-COURTS", "SRC-NZ-PRIVACY", "SRC-TE-MANA-RARAUNGA"], "court-registry authority reservation", "No frozen exact-gate surface combines sealed case-file inspection, suppression-order boundaries, transcription correction, accessible service, retention, redress, tikanga context, and tangata-whenua governance."),
]


def _source(source_id, status, kind, title, url, implication):
    return {
        "source_id": source_id,
        "status": status,
        "kind": kind,
        "title": title,
        "url": url,
        "phase_implication": implication,
    }


SOURCES = [
    _source("SRC-W3C-PROV", "stable", "official_recommendation", "PROV-O: The PROV Ontology", "https://www.w3.org/TR/prov-o/", "Supports typed lineage and invalidation vocabulary only."),
    _source("SRC-GIT-CRUFT", "current", "official_software_documentation", "Git cruft packs", "https://git-scm.com/docs/gitformat-pack#_cruft_packs", "Supports disposable retention fixtures only; no canonical object deletion."),
    _source("SRC-OCI-DISTRIBUTION", "current", "official_specification", "OCI Distribution Specification", "https://github.com/opencontainers/distribution-spec/blob/main/spec.md", "Supports synthetic referrer and artifact-manifest structure only."),
    _source("SRC-OCI-IMAGE", "current", "official_specification", "OCI Image Format Specification", "https://github.com/opencontainers/image-spec/blob/main/manifest.md", "Anchors subject and artifact manifest fields only."),
    _source("SRC-BELINFANTE", "stable", "primary_research_context", "On the spin angular momentum of mesons", "https://doi.org/10.1016/S0031-8914(40)90091-X", "Supports formal stress-tensor improvement vocabulary only."),
    _source("SRC-DIRAC-BERGMANN", "stable", "primary_text", "Lectures on Quantum Mechanics", "https://store.doverpublications.com/products/9780486417134", "Supports formal constrained-Hamiltonian vocabulary only."),
    _source("SRC-NOETHER", "stable", "primary_research", "Invariant variation problems", "https://arxiv.org/abs/physics/0503066", "Supports Noether identity vocabulary only."),
    _source("SRC-HADAMARD", "stable", "primary_research", "Micro-local approach to the Hadamard condition in quantum field theory on curved space-time", "https://doi.org/10.1007/BF02104546", "Supports typed Hadamard-domain obligations only."),
    _source("SRC-GMUT-CANONICAL", "stable", "phase_canonical_scaffold", "Canonical GMUT scalar-tensor and EFT scaffold", "docs/eiren-kestrel/v641-v6/physics/equation-register-covenant.json", "Repository context only; not empirical evidence or canon."),
    _source("SRC-WALD-GR", "stable", "primary_text", "General Relativity", "https://press.uchicago.edu/ucp/books/book/chicago/G/bo5952261.html", "Supports covariance and Bianchi context only."),
    _source("SRC-C2PA", "current", "official_specification", "C2PA Technical Specification", "https://spec.c2pa.org/specifications/specifications/2.2/specs/C2PA_Specification.html", "Supports bounded manifest fixtures only; no provenance completeness."),
    _source("SRC-SARIF", "stable", "official_standard", "Static Analysis Results Interchange Format Version 2.1.0", "https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html", "Supports structural result-lineage fixtures only."),
    _source("SRC-REPRODUCIBLE-BUILDS", "current", "official_project_documentation", "Reproducible Builds SOURCE_DATE_EPOCH", "https://reproducible-builds.org/docs/source-date-epoch/", "Supports bounded environment controls only; no independent reproduction."),
    _source("SRC-DEBIAN-REPOSITORY", "current", "official_distribution_documentation", "Debian repository format", "https://wiki.debian.org/DebianRepository/Format", "Supports synthetic repository metadata fixtures only."),
    _source("SRC-PYPA-WHEEL", "current", "official_packaging_specification", "Binary distribution format", "https://packaging.python.org/en/latest/specifications/binary-distribution-format/", "Supports synthetic wheel structure only; no installation."),
    _source("SRC-ZIP-APPNOTE", "current", "official_format_specification", "APPNOTE.TXT ZIP File Format Specification", "https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT", "Supports disposable ZIP64 byte fixtures only."),
    _source("SRC-HDF5", "current", "official_format_specification", "HDF5 File Format Specification", "https://support.hdfgroup.org/documentation/hdf5/latest/_f_m_t3.html", "Supports disposable HDF5 byte fixtures only."),
    _source("SRC-PDF-REFERENCE", "stable", "primary_format_reference", "PDF Reference 1.7", "https://opensource.adobe.com/dc-acrobat-sdk-docs/pdfstandards/pdfreference1.7old.pdf", "Supports bounded incremental-update structure only."),
    _source("SRC-ELF-GABI", "current", "official_abi_specification", "System V ABI ELF gABI", "https://gabi.xinuos.com/", "Supports synthetic ELF note fixtures only."),
    _source("SRC-MULTIFORMATS", "current", "official_specification", "Multiformats CID specification", "https://github.com/multiformats/cid", "Supports synthetic CID fixtures only."),
    _source("SRC-ISO15489", "stable", "official_standard_context", "ISO 15489-1 Records management", "https://www.iso.org/standard/62542.html", "Supplies records-management context only; no court or professional authority."),
    _source("SRC-NZ-COURTS", "current", "official_public_context", "Courts of New Zealand", "https://www.courtsofnz.govt.nz/", "Keeps court procedure and authority outside the software packet."),
    _source("SRC-CONSORT", "current", "official_reporting_guidance", "CONSORT Statement", "https://www.consort-statement.org/", "Supports matched-arm design vocabulary only; no participant study."),
    _source("SRC-RFC9773", "stable", "official_standard", "RFC 9773 ACME Renewal Information Extension", "https://www.rfc-editor.org/rfc/rfc9773.html", "Supports synthetic renewal-information vectors only."),
    _source("SRC-RFC8555", "stable", "official_standard", "RFC 8555 Automatic Certificate Management Environment", "https://www.rfc-editor.org/rfc/rfc8555.html", "Anchors base ACME semantics only."),
    _source("SRC-RFC-SCIM-CURSOR", "stable", "official_standard", "SCIM Protocol Extension for Cursor-Based Pagination", "https://www.rfc-editor.org/rfc/rfc9865.html", "Supports synthetic cursor-pagination vectors only; no live identity service."),
    _source("SRC-RFC7644", "stable", "official_standard", "RFC 7644 System for Cross-domain Identity Management Protocol", "https://www.rfc-editor.org/rfc/rfc7644.html", "Anchors base SCIM semantics only."),
    _source("SRC-FIDO-CREDENTIAL-EXCHANGE", "draft", "official_working_draft", "FIDO Credential Exchange Specifications", "https://fidoalliance.org/specifications-overview/", "Keeps credential exchange draft-gated and nonproduction."),
    _source("SRC-WCAG22", "stable", "official_accessibility_standard", "Web Content Accessibility Guidelines 2.2", "https://www.w3.org/TR/WCAG22/", "Supports structural checks; complete conformance remains reserved."),
    _source("SRC-WAI-APG", "current", "official_accessibility_guidance", "WAI-ARIA Authoring Practices Guide", "https://www.w3.org/WAI/ARIA/apg/", "Supports keyboard and naming structure only."),
    _source("SRC-WEB-ANNOTATION", "stable", "official_recommendation", "Web Annotation Data Model", "https://www.w3.org/TR/annotation-model/", "Supports synthetic selector provenance only."),
    _source("SRC-WIDOM-LINE", "stable", "primary_research", "Widom line and the liquid-liquid critical point for the TIP5P model of water", "https://doi.org/10.1073/pnas.0704299104", "Supports crossover and response-maximum vocabulary only; psyche conversion is refused."),
    _source("SRC-MULTIVERSE", "stable", "primary_research", "Increasing transparency through a multiverse analysis", "https://doi.org/10.1177/1745691616658637", "Supports structural analysis-decision auditing only."),
    _source("SRC-PANSTARRS-DR2", "current", "official_data_catalogue", "Pan-STARRS1 Data Release 2", "https://catalogs.mast.stsci.edu/panstarrs/", "Supports a zero-row readiness contract only; no query or download occurs."),
    _source("SRC-NZ-PRIVACY", "current", "official_legal_context", "New Zealand Information Privacy Principles", "https://www.privacy.org.nz/privacy-principles/", "Keeps privacy compliance and legal interpretation exact-gated."),
    _source("SRC-TE-MANA-RARAUNGA", "current", "maori_authority_context", "Te Mana Raraunga principles of Māori data sovereignty", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Keeps Māori data governance under Māori authority."),
]


X1_OPERATIONAL_NEGATIVES = [
    {
        "negative_id": "V6521-X1-N01",
        "category": "guessed_sealed_path",
        "failed": "A read-only startup probe guessed an ordinary phase-truth path that did not exist.",
        "recovery": "List the sealed phase root first and bind later reads to exact discovered paths.",
        "passing": "The exact final phase-truth path was discovered and read without mutation.",
        "recurrence_guard": "Never infer lifecycle filenames when an exact phase-root listing is cheap.",
    },
    {
        "negative_id": "V6521-X1-N02",
        "category": "workflow_schema_boundary_token",
        "failed": "The first workflow-plan audit used a live prohibition token where the runner required its standard user-mediated boundary token.",
        "recovery": "Use the standard schema token and preserve the stronger live no-action rule in an additive explicit field.",
        "passing": "The corrected sanitized plan passed all twenty policy checks with the live prohibition still explicit.",
        "recurrence_guard": "Separate schema vocabulary from stronger phase-local constraints rather than overloading an enumerated field.",
    },
    {
        "negative_id": "V6521-X1-N03",
        "category": "powershell_foreach_pipeline",
        "failed": "A statement-level foreach block was piped directly and failed at parse time before evidence or mutation.",
        "recovery": "Materialize foreach output in an array before piping it.",
        "passing": "The corrected bounded novelty inventory completed and returned exact rows.",
        "recurrence_guard": "In Windows PowerShell 5.1, assign statement-level foreach output before piping.",
    },
    {
        "negative_id": "V6521-X1-N04",
        "category": "semantic_novelty_collision",
        "failed": "The first exact 1,180-title novelty gate rejected duplicated Lee-Wald, Nielsen, Zstandard, minimum-entropy, Fermi, federation, and generic authority mechanisms.",
        "recovery": "Replace collided mechanisms with substantively different Belinfante-Rosenfeld, Dirac-Bergmann, HDF5, Widom-line, Pan-STARRS, SCIM-cursor, and sealed-case decision-right surfaces.",
        "passing": "The corrected thirty-title portfolio passed the exact lexical threshold and retained manual mechanism distinctions.",
        "recurrence_guard": "Run the exact frozen-chain neighbour gate before treating a renamed surface as novel.",
    },
    {
        "negative_id": "V6521-X1-N05",
        "category": "predecessor_template_count_and_label_drift",
        "failed": "Pre-generation review found predecessor portfolio minima, source-manifest cardinalities, and domain labels still embedded in the adapted x1 builder.",
        "recovery": "Bind every copied count to the current phase data and replace stale domain labels before materializing the freeze packet.",
        "passing": "A bounded import and stale-label review returned the exact 30/30/10/10/30 portfolios, thirty proposals, thirty-six sources, and current Sable surfaces.",
        "recurrence_guard": "Audit mechanically copied builders for numeric and semantic predecessor drift before their first artifact-writing invocation.",
    },
    {
        "negative_id": "V6521-X1-N06",
        "category": "powershell_utf8nobom_version_mismatch",
        "failed": "A mechanical validator-copy rewrite requested the PowerShell 7 utf8NoBOM encoding token under Windows PowerShell 5.1 and stopped before rewriting content.",
        "recovery": "Keep the harmless copied file and perform the semantic rewrite with apply_patch, which preserves the intended UTF-8 source text.",
        "passing": "The validator source was rewritten to the Sable phase and its bounded count contracts were reviewed directly.",
        "recurrence_guard": "Do not use PowerShell 7-only encoding names in Windows PowerShell 5.1; prefer apply_patch for substantive source edits.",
    },
]


SAFE_TASKS = [
    "Verify every inherited source anchor and the exact three-commit zero-merge special lineage.",
    "Verify the clean Sable fast-forward boundary and four-way branch equality.",
    "Reconcile the 7,855 sealed and one external source negative without rewriting source truth.",
    "Audit all source rows for current, stable, draft, or watch status only.",
    "Compute lexical nearest neighbours across all 1,180 frozen proposal titles.",
    "Record manual mechanism distinctions and rejected semantic collisions.",
    "Protect every frozen x1 path with an exact staged-surface allowlist.",
    "Seal x1 content in the Git path-filtered blob domain.",
    "Parse every phase JSON document with explicit UTF-8.",
    "Check deterministic JSON ordering for generated ledgers.",
    "Separate privacy scanner definitions from confirmed payload dispositions.",
    "Declare checkout-byte and Git-blob hash domains without conflation.",
    "Prove owner-manifest coverage including scripts and tests.",
    "Enforce the live document and baton word envelopes.",
    "Hold terminal routing before exact-final proof.",
    "Emit workload and correction-readiness metadata without human-state claims.",
    "Record environment versions without updating the desktop application.",
    "Verify eight inherited future CLI seats remain unnamed, uncreated, and unlaunched.",
    "Enforce ordinary x1, x2, and total commit caps.",
    "Verify zero merges and one-parent lifecycle commits.",
    "Require exactly one successful canonical bounded final pass and no replay after success.",
    "Review stale lifecycle labels and count mirrors after every additive ledger change.",
    "Lint scientific, identity, production, professional, legal, cultural, and Stage 20 boundaries.",
    "Enforce the four-value core outcome vocabulary.",
    "Verify held exact-approval and blocked packets remain visible and unexecuted.",
    "Separate official citations from observations, measurements, or delegated authority.",
    "Keep Pan-STARRS network, row, likelihood, posterior, and constraint counts at zero.",
    "Keep identity profiles synthetic with zero real key, account, certificate, or exchange events.",
    "Keep THOS proxies at zero real people, court exhibits, operations, or outcomes.",
    "Reserve manual, browser, assistive-technology, Māori-language, and affected-user evaluation.",
]


CANDIDATE_TASKS = [f"Build and bounded-test {proposal['mission_surface']}." for proposal in PROPOSALS]


SKILL_IDEAS = [
    "ghc-family-claim-lease-demotion",
    "ghc-family-cruft-pack-retention-guard",
    "ghc-family-oci-referrer-tribunal",
    "ghc-family-gmut-constraint-identity-board",
    "ghc-family-gmut-gauge-identity-board",
    "ghc-family-c2pa-sarif-lineage-audit",
    "ghc-family-reproducible-build-envelope",
    "ghc-family-court-registry-handover-proxy",
    "ghc-family-identity-lifecycle-boundary",
    "ghc-family-stage20-multiverse-nonpromotion",
]


RUNNER_IDEAS = [
    "ghc_family_claim_lease_demoter.py",
    "ghc_family_cruft_pack_guard.py",
    "ghc_family_oci_referrer_tribunal.py",
    "ghc_family_gmut_covariant_boards.py",
    "ghc_family_artifact_lineage_tribunals.py",
    "ghc_family_reproducible_build_envelope.py",
    "ghc_family_court_registry_proxy.py",
    "ghc_family_identity_lifecycle_profiles.py",
    "ghc_family_stage20_multiverse_board.py",
    "ghc_family_v652_v1_detailed_validator.py",
]


CLEAN_TASKS = [
    "Reconcile retained-negative counts from authoritative ledgers.",
    "Refresh count-dependent truth mirrors after every retained failure.",
    "Normalize generated text through the declared Git-blob hash domain.",
    "Replace working-byte historical assumptions with exact commit-blob checks.",
    "Split broad Windows inspections into bounded attributed probes.",
    "Pin UTF-8 before every Unicode-emitting process.",
    "Classify privacy candidates by exact file and scanner class.",
    "Preserve unresolved privacy candidates until explicit review.",
    "Use exact eligible-test arithmetic instead of brittle raw cardinality.",
    "Verify family-current caller collisions before adding wrappers.",
    "Retain historical tools as compatibility surfaces unless migration evidence exists.",
    "Rebuild accessible static output and preserve manual-evaluation reservations.",
    "Check every phase document against the word cap.",
    "Check owner-generated file growth against the rotation threshold.",
    "Hold the terminal route until exact final proof.",
    "Refresh the phase-scoped GHC Family Index after new tools exist.",
    "Refresh Reflection Remaster recommendations after new tools exist.",
    "Refresh workflow-refinement output without activating future placeholders.",
    "Validate Method Flow after every new witness.",
    "Keep all failed witnesses append-only and linked to negatives.",
    "Remove no memory, identity, source, negative, or sibling record.",
    "Delete no user or sibling material during cleanup.",
    "Keep future CLI seat placeholders unnamed and unlaunched.",
    "Keep Sandbox and Hyper-V states unchanged.",
    "Keep the Codex desktop application unchanged.",
    "Keep Pan-STARRS adapter counters at exact zero without data access.",
    "Keep THOS participant, operator, exhibit, and outcome counters at exact zero.",
    "Keep Freed ID real-key, issuance, exchange, and production counters at exact zero.",
    "Keep CBR decision and authority counters at exact zero.",
    "Verify all 150 synthetic mutations retain reject-or-quarantine outcomes.",
]


REJECTED_COLLISIONS = [
    {"candidate": "Kallen-Lehmann spectral board", "reason": "frozen at V6497-P02; replaced by Belinfante-Rosenfeld stress-improvement obligations"},
    {"candidate": "Peierls bracket board", "reason": "frozen at V6465-P02; replaced by Dirac-Bergmann and Noether constraint-identity surfaces"},
    {"candidate": "generic OCI layer parser", "reason": "overlaps V6472-P07; rewritten around Distribution referrers and subject-linked artifact manifests"},
    {"candidate": "generic TUF tribunal", "reason": "overlaps V6471-P01; replaced by Debian APT by-hash and Valid-Until control"},
    {"candidate": "generic SLSA and in-toto provenance", "reason": "overlaps V6477-P01; replaced by C2PA and SARIF lineage mechanisms"},
    {"candidate": "generic Arrow or Parquet parser", "reason": "frozen in v650; replaced by wheel, ZIP64, HDF5, PDF, ELF, and CID surfaces"},
    {"candidate": "generic public-library or community-archive proxy", "reason": "overlaps v6475 and v6491; replaced by court-registry exhibit custody"},
    {"candidate": "generic OpenID Federation trust chain", "reason": "overlaps v6451; replaced by the distinct SCIM cursor-expiry and pagination lifecycle"},
    {"candidate": "IceCube public-data adapter", "reason": "frozen at V6467-P03; replaced by the Pan-STARRS1 DR2 stack, detection, and mean-object contract"},
    {"candidate": "generic reproducibility claim", "reason": "rewritten as an exact same-owner capsule with dependency, locale, ordering, network, and independent-team boundaries"},
]
