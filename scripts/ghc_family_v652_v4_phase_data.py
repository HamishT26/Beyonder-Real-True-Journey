#!/usr/bin/env python3
"""Frozen Sylven Arc v652-v4 x1 data; this module contains no x2 observations."""

from __future__ import annotations


PHASE = "v652-v4"
OWNER = "Sylven Arc"
PRONOUNS = "they/them"
ROLE = "relational constraint-cartographer and falsifier-keeper"
HOPE = "keep uncertainty visible, failures recoverable, and evidence from being mistaken for authority"
BRANCH = "codex/GHC-Family/sylven-arc-v642-v8-full-tools"
PHASE_ROOT = "docs/sylven-arc/v652-v4"

SOURCE_BRANCH = "codex/GHC-Family/tamar-vey-full-tools"
SOURCE_HEAD = "09140173409bc4198f3c9e30162b9bcef8a3895b"
SOURCE_ORIGIN = "fa060eec3071694e1aff8eaf7d76d6c4b0f8075e"
SOURCE_X1 = "4e905d2b0637d4db78ac55273c8b52d5cf6c2117"
SOURCE_EVIDENCE = "22c4ca1e7d4473fcf5246867bb729b3748f34441"
PRIOR_FROZEN = 1270
INHERITED_NEGATIVES = 8383
INHERITED_OPEN_GAPS = 64
INHERITED_EXACT_GATES = 65
PRIMARY_FOCUS = "GMUT Mind"
BOUNDED_PRACTICE = (
    "hydrographic multibeam acquisition planning, vessel and sensor lineage, sound-velocity and tide "
    "correction, quality review, accessible notice, workload control, correction readback, and shift handover"
)

OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]
SOURCE_STATUS_CLASSES = ["current", "stable", "experimental", "watch"]
PROTECTED_GATES = [
    "empirical_data",
    "real_participants_or_operators",
    "professional_or_hydrographic_authority",
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
            "Emit a zero-row refusal with zero query, download, ingest, fit, likelihood, posterior, "
            "constraint, prediction, or empirical promotion."
        )
    elif disposition == "exact_gate":
        approval = "exact_affected_party_competent_and_maori_authority_required"
        lane = "x2_reservation_matrix_only"
        gate = (
            "Emit unresolved decision rights and reservations only; make no collection, access, disclosure, "
            "charting, remedy, legal, cultural, data-governance, place-name, affected-party, or Māori-authority decision."
        )
    elif disposition == "represented":
        approval = "candidate_bounded_synthetic_proxy"
        lane = "x2_synthetic_proxy_only"
        gate = (
            "Reject every preregistered mutation and retain represented status with zero production, participant, "
            "operational, professional, interoperability, or authority credit."
        )
    else:
        approval = "safe_now_bounded_software_symbolic_formal_or_structural"
        lane = "x2_bounded_owner_local"
        gate = (
            "Reject every preregistered mutation and emit only the declared bounded software, symbolic, formal, "
            "structural, or workflow completion."
        )
    return {
        "proposal_id": f"V6524-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar": pillar,
        "mission_surface": mission,
        "hypothesis": (
            f"A bounded {mission} artifact can expose its declared obligations while refusing unsupported "
            "scientific, operational, identity, accessibility, privacy, or authority promotion."
        ),
        "null_or_failure_condition": (
            f"The artifact omits a declared {mission} obligation, accepts a preregistered mutation, erases a "
            "failure, crosses an approval boundary, or promotes beyond its evidence lane."
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
        "novelty_against_1270_frozen_proposals": novelty,
    }


PROPOSALS = [
    _proposal(1, "Git cat-file batch-command framing, command-response pairing, object byte count, missing-object response, flush, desynchronization, and teardown tribunal", "git-cat-file-batch-command", "THOS Body", "completed", ["SRC-GIT-CAT-FILE"], "Git batch-command stream refusal", "Prior Git object-store work does not isolate the batch-command protocol, ordered response framing, payload byte counts, explicit flush, missing objects, and desynchronization recovery."),
    _proposal(2, "DHCPv6 RFC 9915 message type, transaction id, option length, client and server identifier, identity association, relay nesting, status, retransmission, and refusal tribunal", "dhcpv6-rfc9915", "THOS Body", "completed", ["SRC-RFC9915"], "current DHCPv6 envelope refusal", "No frozen title targets the 2026 RFC 9915 consolidation with DHCPv6 transaction, identity-association, relay nesting, status, and retransmission duties."),
    _proposal(3, "SCTP common header, verification tag, checksum, chunk type, flags, length, DATA sequence, SACK gaps, padding, budget, and refusal tribunal", "sctp-packet", "THOS Body", "completed", ["SRC-RFC9260"], "SCTP packet refusal", "No inherited mechanism isolates SCTP chunk framing, transmission sequence numbers, selective acknowledgements, four-byte padding, verification tags, and checksum boundaries."),
    _proposal(4, "SMTP CHUNKING EHLO capability, BDAT size, LAST marker, exact octet count, command sequencing, premature close, reply ownership, budget, and refusal tribunal", "smtp-bdat", "THOS Body", "completed", ["SRC-RFC3030"], "SMTP BDAT refusal", "Prior mail work does not isolate the SMTP CHUNKING extension, BDAT octet ownership, LAST sequencing, partial-body closure, and command-reply framing."),
    _proposal(5, "BMP and DIB signature, file size, pixel offset, header size, dimensions, planes, bit count, compression, row stride, palette, overflow, and refusal tribunal", "bmp-dib", "THOS Body", "completed", ["SRC-MS-BMP"], "BMP and DIB byte-arithmetic refusal", "No frozen title isolates BMP file-header to DIB ownership, row-stride padding, palette bounds, signed dimensions, pixel offset, and multiplication overflow."),
    _proposal(6, "ICO and CUR directory, image count, entry dimensions, colour count, planes or hotspot, bit count, byte size, image offset, PNG-or-DIB payload, overlap, and refusal tribunal", "ico-cur", "THOS Body", "completed", ["SRC-MS-ICO"], "ICO and CUR directory refusal", "No frozen title isolates the shared ICO/CUR directory with type-dependent hotspot semantics, embedded PNG or DIB payloads, entry overlap, and exact byte ranges."),
    _proposal(7, "MPEG-2 transport-stream sync byte, transport error, PID, adaptation control, continuity counter, PCR, PAT, PMT, section length, CRC, and refusal tribunal", "mpeg2-ts", "THOS Body", "completed", ["SRC-ISO-13818-1"], "MPEG-2 transport-stream refusal", "No inherited proposal isolates 188-byte transport packets, PID continuity, adaptation fields, PCR timing, program association and map sections, and section CRC boundaries."),
    _proposal(8, "OpenDocument 1.4 package mimetype, META-INF manifest, full-path, media type, encryption data, checksum, duplicate path, traversal, resource budget, and refusal tribunal", "odf-package", "THOS Body", "completed", ["SRC-ODF14-PACKAGE"], "OpenDocument package refusal", "ZIP and office-container work does not isolate ODF 1.4 package mimetype placement, manifest full-path ownership, media types, encryption metadata, and package-specific checksum duties."),
    _proposal(9, "Standard MIDI File MThd, format, track count, time division, MTrk length, variable-length quantity, running status, meta event, SysEx, end-of-track, and refusal tribunal", "standard-midi-file", "THOS Body", "completed", ["SRC-MIDI-SMF"], "Standard MIDI File refusal", "No frozen title isolates Standard MIDI header and track chunks, time-division modes, variable-length quantities, running status, meta events, SysEx, and end-of-track."),
    _proposal(10, "EPUB 3.3 OCF mimetype, META-INF container, rootfile, package document, manifest, spine, fallback, path, encryption, byte budget, and refusal tribunal", "epub33-ocf", "THOS Body", "completed", ["SRC-EPUB33"], "EPUB 3.3 OCF refusal", "Generic ZIP and publication work does not isolate current EPUB 3.3 OCF rootfile discovery, package manifest-spine relations, fallbacks, encryption metadata, and publication path rules."),
    _proposal(11, "WOFF2 signature, flavor, declared length, table directory, transform version, Brotli stream, reconstructed size, collection directory, metadata, private data, and refusal tribunal", "woff2-font", "THOS Body", "completed", ["SRC-WOFF2"], "WOFF2 font-envelope refusal", "No frozen mechanism isolates WOFF2 table transforms, compressed stream ownership, reconstructed table sizes, collection entries, metadata and private-data offsets."),
    _proposal(12, "Java SE 26 class-file magic, version, constant pool, modified UTF-8, field, method, attribute, stack map, bootstrap method, index bounds, and refusal tribunal", "java26-classfile", "THOS Body", "completed", ["SRC-JVMS26"], "Java SE 26 class-file refusal", "No inherited title isolates the current Java SE 26 class-file version, modified UTF-8 constants, stack-map frames, bootstrap linkage, and constant-pool index bounds."),
    _proposal(13, "GMUT Einstein-Cartan coframe, independent spin connection, torsion, spin current, algebraic connection equation, contorsion, contact term, boundary, EFT, unit, and observation-firewall board", "einstein-cartan", "GMUT Mind", "completed", ["SRC-KIBBLE1961"], "Einstein-Cartan spin-torsion obligations", "Tamar's general Cartan tetrad board stops before the algebraic spin-sourced torsion equation, contorsion elimination, induced contact term, and their distinct EFT and observation limits."),
    _proposal(14, "GMUT Mathisson-Papapetrou-Dixon momentum, spin tensor, curvature force, torque, multipole order, representative worldline, spin supplementary condition, mass, unit, EFT, and observation-firewall board", "mpd-equations", "GMUT Mind", "completed", ["SRC-DIXON1974"], "Mathisson-Papapetrou-Dixon obligations", "No frozen board isolates extended-body momentum and spin evolution, multipole truncation, representative-worldline ambiguity, spin supplementary conditions, and observation refusal."),
    _proposal(15, "GMUT Penrose conformal completion, conformal factor, physical and unphysical metric, null infinity, regularity, conformal gauge, boundary, peeling reservation, EFT, unit, and observation-firewall board", "penrose-conformal-completion", "GMUT Mind", "completed", ["SRC-PENROSE1963"], "Penrose conformal-completion obligations", "No inherited title isolates physical-to-unphysical metric rescaling, null infinity, regularity and conformal-gauge duties while reserving peeling and empirical claims."),
    _proposal(16, "GMUT Lanczos potential, Weyl reconstruction, algebraic gauge, differential gauge, dual, dimension, integrability, topology, boundary, EFT, unit, and observation-firewall board", "lanczos-potential", "GMUT Mind", "completed", ["SRC-LANCZOS-POTENTIAL"], "Lanczos-potential obligations", "No frozen board isolates a potential for Weyl curvature with both gauge freedoms, dimension and integrability restrictions, topological limits, and observation refusal."),
    _proposal(17, "GMUT Brown-York quasilocal stress tensor, induced metric, extrinsic curvature, subtraction, lapse, shift, surface energy, momentum, orientation, counterterm, EFT, unit, and observation-firewall board", "brown-york", "GMUT Mind", "completed", ["SRC-BROWN-YORK"], "Brown-York quasilocal obligations", "Israel junction work treats jumps between regions; this board instead isolates one-boundary variational stress, subtraction or counterterm choice, surface energy and momentum, and observation refusal."),
    _proposal(18, "Accessible dual-listbox transfer workflow with available and chosen group labels, option state, add, remove, reorder controls, keyboard alternative, counts, status, focus, error, fallback, and manual-evaluation audit", "accessible-dual-listbox", "THOS Body", "completed", ["SRC-WAI-LISTBOX", "SRC-WCAG22"], "accessible dual-listbox structure", "The rejected date-picker duplicated an inherited surface; no frozen title instead isolates two labelled option collections, transfer and reorder controls, announced counts, focus restoration, and a non-drag keyboard path."),
    _proposal(19, "Thermo-Psyche Young-Laplace and Jurin capillary pressure, curvature, surface tension, contact angle, density difference, gravity, tube radius, sign, unit, domain, and agency-nonconversion classifier", "young-laplace-jurin", "Trinity Mandala bridge", "completed", ["SRC-NIST-CAPILLARY"], "capillary-pressure agency nonconversion", "The nearest Kelvin-equation surface concerns vapour-pressure curvature; this mechanism instead binds interfacial pressure jump to hydrostatic capillary rise, contact angle, density difference, and domain."),
    _proposal(20, "Stage 20 DeLong correlated ROC comparison, placement values, U-statistic covariance, paired observations, ties, missingness, multiplicity, uncertainty, interpretation, and nonpromotion board", "delong-roc", "Trinity Mandala bridge", "completed", ["SRC-DELONG"], "DeLong ROC nonpromotion", "No frozen board isolates correlated ROC U-statistic placement values and covariance, pairing, tie handling, missingness, multiplicity, and nonpromotion."),
    _proposal(21, "Stage 20 exact McNemar discordant-pair table, conditional binomial null, two-sided ordering, continuity convention, ties, missingness, multiplicity, effect, uncertainty, and nonpromotion board", "mcnemar-exact", "Trinity Mandala bridge", "completed", ["SRC-MCNEMAR"], "exact McNemar nonpromotion", "No inherited board isolates paired binary discordance, the conditional binomial null, exact two-sided ordering, continuity conventions, and effect interpretation."),
    _proposal(22, "Stage 20 Cochran Q matched-binary block, treatment and subject totals, tie, sparse block, post-hoc reservation, missingness, multiplicity, effect, uncertainty, and nonpromotion board", "cochran-q", "Trinity Mandala bridge", "completed", ["SRC-COCHRAN-Q"], "Cochran Q nonpromotion", "No frozen mechanism isolates three-or-more related binary conditions, block totals, sparse and tied blocks, post-hoc reservation, and nonpromotion."),
    _proposal(23, "Stage 20 Brier score calibration, reliability, resolution, uncertainty, prevalence, weighting, missingness, distribution shift, interval, interpretation, and nonpromotion board", "brier-score", "Trinity Mandala bridge", "completed", ["SRC-BRIER"], "Brier-score nonpromotion", "No inherited board isolates squared probabilistic forecast error with reliability-resolution decomposition, prevalence and weighting, distribution shift, uncertainty, and nonpromotion."),
    _proposal(24, "THOS multibeam echo-sounder line plan, vessel and sensor identity, patch test, sound-velocity profile, tide source, acquisition gap, quality flag, workload, correction readback, and shift-handover proxy", "hydrographic-acquisition", "THOS Body", "represented", ["SRC-IHO-S44"], "hydrographic multibeam acquisition proxy", "No frozen THOS surface isolates survey-line planning, multibeam sensor lineage, patch test, sound-velocity and tide sources, acquisition gaps, quality review, and hydrographic handover."),
    _proposal(25, "THOS hydrographic sounding raw-to-clean lineage, navigation latency, heave and attitude, refraction, tide correction, outlier quarantine, surface generation, accessible notice, workload, readback, and handover proxy", "hydrographic-processing", "THOS Body", "represented", ["SRC-IHO-S44"], "hydrographic sounding processing proxy", "No inherited proxy binds raw sounding lineage to navigation timing, vessel motion, refraction and tide corrections, quarantined outliers, derived surfaces, accessible notice, and handover."),
    _proposal(26, "Freed ID ACME account, nonce, JWS, order, authorization, identifier, challenge, finalize, certificate, revocation, error, minimization, privacy, and nonproduction profile", "acme-base", "Freed ID and CBR Heart", "represented", ["SRC-RFC8555"], "ACME base-protocol profile", "The inherited ACME ARI profile covers renewal information; this distinct base protocol profile covers account, order, authorization, challenge, finalization, certificate, and revocation lifecycles."),
    _proposal(27, "Freed ID EST CA certificates, CSR attributes, simple enrollment, reenrollment, server-key-generation refusal, authentication, proof of possession, minimization, privacy, and nonproduction profile", "est-enrollment", "Freed ID and CBR Heart", "represented", ["SRC-RFC7030"], "EST enrollment profile", "No frozen identity surface isolates Enrollment over Secure Transport discovery, CSR attributes, enrolment and reenrolment, proof of possession, and server-generated-key refusal."),
    _proposal(28, "Freed ID LDAP Content Synchronization request mode, cookie, entry state, present UUID, delete, refresh, persist, replay, minimization, privacy, and nonproduction profile", "ldap-content-sync", "Freed ID and CBR Heart", "represented", ["SRC-RFC4533"], "LDAP Content Sync experimental profile", "No inherited identity profile isolates refresh-only versus refresh-and-persist modes, sync cookies, entry states, present UUID sets, deletion semantics, replay, and the RFC's Experimental status."),
    _proposal(29, "GMUT WALLABY Pilot DR2 and CASDA source catalogue, spectral cube, beam, channel, flux, mask, selection, completeness, checksum, covariance, provenance, and zero-row likelihood-refusal adapter", "wallaby-pdr2-zero-row", "GMUT Mind", "open_gap", ["SRC-WALLABY-DATA", "SRC-WALLABY-PAPER"], "WALLABY Pilot DR2 likelihood readiness", "No inherited zero-row adapter targets WALLABY Pilot DR2 neutral-hydrogen source catalogues and spectral cubes with beam, channel, mask, selection, completeness, checksum, and covariance duties."),
    _proposal(30, "CBR hydrographic sounding footprint, undersea cultural and archaeological feature, taonga-related feature, raw point cloud, derived bathymetric surface, charting disclosure, access, notice, privacy, remedy, place-name stewardship, affected-party, legal, cultural, data-governance, and Māori-authority reservation", "hydrographic-authority", "Freed ID and CBR Heart", "exact_gate", ["SRC-LINZ-HYDRO", "SRC-MAORI-DATA", "SRC-PRIVACY-NZ", "SRC-NZGB"], "hydrographic data and authority reservation", "No frozen gate isolates raw and derived hydrographic surfaces, charting disclosure, undersea cultural or archaeological features, taonga-related features, place-name stewardship, remedy, affected parties, and Māori data authority together."),
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
    _source("SRC-GIT-CAT-FILE", "current", "official_project_manual", "Git cat-file manual", "https://git-scm.com/docs/git-cat-file.html", "Supports disposable local object-stream fixtures only."),
    _source("SRC-RFC9915", "current", "official_internet_standard", "RFC 9915 Dynamic Host Configuration Protocol for IPv6", "https://www.rfc-editor.org/info/rfc9915/", "Supersedes RFC 8415 and supports nonnetwork synthetic messages only."),
    _source("SRC-RFC9260", "stable", "official_internet_standard", "RFC 9260 Stream Control Transmission Protocol", "https://www.rfc-editor.org/info/rfc9260/", "Supports nonnetwork SCTP byte fixtures only."),
    _source("SRC-RFC3030", "stable", "official_internet_standard", "RFC 3030 SMTP Service Extensions for Transmission of Large and Binary MIME Messages", "https://www.rfc-editor.org/info/rfc3030/", "Supports nonnetwork SMTP command fixtures only."),
    _source("SRC-MS-BMP", "current", "official_platform_documentation", "Microsoft BMP file header and bitmap storage", "https://learn.microsoft.com/en-us/windows/win32/gdi/bitmap-storage", "Supports disposable bitmap bytes only."),
    _source("SRC-MS-ICO", "current", "official_platform_documentation", "Microsoft ICO format overview", "https://learn.microsoft.com/en-us/windows/win32/wic/ico-format-overview", "Supports disposable icon and cursor bytes only."),
    _source("SRC-ISO-13818-1", "current", "official_international_standard", "ISO/IEC 13818-1:2025 MPEG-2 Systems", "https://www.iso.org/standard/91403.html", "Supports synthetic transport-stream packets only."),
    _source("SRC-ODF14-PACKAGE", "current", "official_open_standard", "OpenDocument 1.4 Part 2 Packages", "https://docs.oasis-open.org/office/OpenDocument/v1.4/part2-packages/OpenDocument-v1.4-os-part2-packages.html", "Supports disposable ODF package structures only."),
    _source("SRC-MIDI-SMF", "current", "official_industry_specification", "MIDI Association Standard MIDI Files", "https://midi.org/standard-midi-files", "Supports synthetic MIDI chunks only."),
    _source("SRC-EPUB33", "current", "official_web_standard", "EPUB 3.3", "https://www.w3.org/TR/epub-33/", "Supports disposable EPUB package structures only."),
    _source("SRC-WOFF2", "current", "official_web_standard", "WOFF File Format 2.0", "https://www.w3.org/TR/WOFF2/", "Supports synthetic font envelopes only."),
    _source("SRC-JVMS26", "current", "official_platform_specification", "Java Virtual Machine Specification SE 26 class-file format", "https://docs.oracle.com/en/java/javase/26/docs/specs/jvms/jvms-4.html", "Supports synthetic class-file structures only."),
    _source("SRC-KIBBLE1961", "stable", "primary_research", "Lorentz invariance and the gravitational field", "https://doi.org/10.1063/1.1703702", "Supports formal Einstein-Cartan vocabulary only."),
    _source("SRC-DIXON1974", "stable", "primary_research", "Dynamics of extended bodies in general relativity III: equations of motion", "https://doi.org/10.1098/rsta.1974.0046", "Supports formal multipole-motion vocabulary only."),
    _source("SRC-PENROSE1963", "stable", "primary_research", "Asymptotic properties of fields and space-times", "https://doi.org/10.1103/PhysRevLett.10.66", "Supports formal conformal-boundary vocabulary only."),
    _source("SRC-LANCZOS-POTENTIAL", "stable", "primary_research", "The Lanczos potential for the Weyl curvature tensor", "https://arxiv.org/abs/gr-qc/9601029", "Supports formal potential and gauge vocabulary only."),
    _source("SRC-BROWN-YORK", "stable", "primary_research", "Quasilocal energy and conserved charges derived from the gravitational action", "https://doi.org/10.1103/PhysRevD.47.1407", "Supports formal quasilocal-stress vocabulary only."),
    _source("SRC-WAI-LISTBOX", "current", "official_accessibility_guidance", "WAI-ARIA Authoring Practices listbox pattern", "https://www.w3.org/WAI/ARIA/apg/patterns/listbox/", "Supports structural name, state, keyboard, and focus checks only."),
    _source("SRC-WCAG22", "stable", "official_accessibility_standard", "Web Content Accessibility Guidelines 2.2", "https://www.w3.org/TR/WCAG22/", "Supports structural checks; complete conformance remains reserved."),
    _source("SRC-NIST-CAPILLARY", "stable", "primary_research", "Capillary rise between planar surfaces", "https://doi.org/10.1103/PhysRevE.79.011604", "Supports capillary-pressure vocabulary only; agency conversion is refused."),
    _source("SRC-DELONG", "stable", "primary_research", "Comparing the areas under two or more correlated ROC curves", "https://doi.org/10.2307/2531595", "Supports statistical obligations only; no participant inference."),
    _source("SRC-MCNEMAR", "stable", "primary_research", "Note on the sampling error of the difference between correlated proportions", "https://doi.org/10.1007/BF02295996", "Supports paired-binary obligations only."),
    _source("SRC-COCHRAN-Q", "stable", "primary_research", "The comparison of percentages in matched samples", "https://doi.org/10.1093/biomet/37.3-4.256", "Supports matched-binary obligations only."),
    _source("SRC-BRIER", "stable", "primary_research", "Verification of forecasts expressed in terms of probability", "https://journals.ametsoc.org/view/journals/mwre/78/1/1520-0493_1950_078_0001_vofeit_2_0_co_2.xml", "Supports probabilistic-score obligations only."),
    _source("SRC-IHO-S44", "current", "official_intergovernmental_standard", "IHO Standards for Hydrographic Surveys Edition 6.2.0", "https://iho.int/uploads/user/pubs/standards/s-44/S-44_Edition_6.2.0_adopted.pdf", "Supplies requirements context only; no hydrographic competence or authority."),
    _source("SRC-RFC8555", "stable", "official_internet_standard", "RFC 8555 Automatic Certificate Management Environment", "https://www.rfc-editor.org/info/rfc8555/", "Supports synthetic protocol vectors only; no real keys or services."),
    _source("SRC-RFC7030", "stable", "official_internet_standard", "RFC 7030 Enrollment over Secure Transport", "https://www.rfc-editor.org/info/rfc7030/", "Supports synthetic enrollment vectors only."),
    _source("SRC-RFC4533", "experimental", "official_experimental_rfc", "RFC 4533 LDAP Content Synchronization Operation", "https://www.rfc-editor.org/info/rfc4533/", "Experimental status is retained; supports synthetic vectors only."),
    _source("SRC-WALLABY-DATA", "current", "official_survey_data_catalogue", "WALLABY Pilot Phase 2 Data Release", "https://data.csiro.au/collection/csiro%3A63398", "Supports a zero-row adapter contract only; no query or download occurs."),
    _source("SRC-WALLABY-PAPER", "stable", "primary_research", "WALLABY Pilot Phase II public data release", "https://arxiv.org/abs/2409.13130", "Supplies schema and provenance context only; no observation occurs."),
    _source("SRC-LINZ-HYDRO", "current", "official_government_data_guidance", "LINZ hydrographic data", "https://www.linz.govt.nz/products-services/data/types-linz-data/hydrographic-data", "Keeps charting, disclosure, safety, and operational decisions external."),
    _source("SRC-MAORI-DATA", "current", "maori_authority_guidance", "Te Mana Raraunga principles of Māori data sovereignty", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Keeps Māori data decisions with Māori authority."),
    _source("SRC-PRIVACY-NZ", "current", "official_legislation", "Privacy Act 2020", "https://www.legislation.govt.nz/act/public/2020/31/en/latest/", "Keeps legal interpretation, disclosure, and remedy exact-gated."),
    _source("SRC-NZGB", "current", "official_government_authority", "New Zealand Geographic Board", "https://www.linz.govt.nz/our-work/new-zealand-geographic-board", "Keeps place-name stewardship and authority decisions external."),
]


X1_OPERATIONAL_NEGATIVES = [
    {"negative_id": "V6524-X1-N01", "category": "baton_display_truncation", "failed": "The initial full committed-baton display exceeded the bounded output budget, so it earned no complete-read credit.", "recovery": "Read the immutable file in fixed line slices from a materialized line array.", "passing": "Every committed baton line was read through EOF.", "recurrence_guard": "Use bounded fixed slices for long authoritative files."},
    {"negative_id": "V6524-X1-N02", "category": "baton_chunk_still_too_large", "failed": "The first chunked baton display remained too large and truncated, so it earned no complete-read credit.", "recovery": "Reduce slices to fifty lines and continue monotonically through EOF.", "passing": "The reduced slices completed the full read.", "recurrence_guard": "Lower chunk size immediately when a bounded display still truncates."},
    {"negative_id": "V6524-X1-N03", "category": "combined_read_only_probe_timeout", "failed": "A combined source, lane, storage, and manifest probe exceeded its wrapper deadline and earned no state credit.", "recovery": "Split exact Git scalars, cleanliness, storage, and manifest probes.", "passing": "All exact scalar postconditions were independently established.", "recurrence_guard": "Do not aggregate unrelated large-tree probes under one deadline."},
    {"negative_id": "V6524-X1-N04", "category": "fast_forward_verbose_output", "failed": "The successful quiet fast-forward still emitted a large inherited checkout-progress stream, invalidating the silence assumption.", "recovery": "Do not repeat the mutation; verify exact head, branch, clean state, ancestry, and remote equality with scalar reads.", "passing": "The Sylven lane was clean, exact, and four-way equal.", "recurrence_guard": "Treat progress suppression as advisory and rely on scalar postconditions."},
    {"negative_id": "V6524-X1-N05", "category": "broad_inventory_timeout", "failed": "A parallel inherited packet and keyword inventory exceeded its deadline and earned no discovery credit.", "recovery": "Use exact Git-tree phase-root enumeration and bounded source probes.", "passing": "The required inherited artifacts and collision candidates were enumerated.", "recurrence_guard": "Prefer exact phase-root enumeration over broad parallel scans."},
    {"negative_id": "V6524-X1-N06", "category": "parallel_line_count_timeout", "failed": "A parallel exact-file line-count probe exceeded its deadline and earned no result credit.", "recovery": "Use one repository-local enumeration process.", "passing": "Exact script line counts completed in one bounded process.", "recurrence_guard": "Keep small filesystem metadata reads in one local process."},
    {"negative_id": "V6524-X1-N07", "category": "source_search_output_truncation", "failed": "A broad OpenDocument source search exceeded useful display context and earned no source-verification credit.", "recovery": "Search and open the exact OASIS OpenDocument 1.4 package target only.", "passing": "The exact OASIS Open Standard package document was verified.", "recurrence_guard": "Use one exact standards target for final source verification."},
    {"negative_id": "V6524-X1-N08", "category": "doi_redirect_open_refusal", "failed": "Direct DOI opens for the Dixon primary papers were refused by the web safety wrapper and earned no verification credit.", "recovery": "Use an exact bibliographic search and authoritative metadata result without bypassing the wrapper.", "passing": "Dixon's 1974 equations-of-motion paper and DOI were verified from bounded bibliographic metadata.", "recurrence_guard": "Use exact bibliographic discovery when direct DOI redirects are unavailable."},
    {"negative_id": "V6524-X1-N09", "category": "inherited_identifier_uniqueness_assumption", "failed": "The first x1 build assumed every identifier in the immutable 1,270-row predecessor chain was unique; twenty retained v651-v3 identifiers occur twice, so the build stopped before packet generation.", "recovery": "Preserve every inherited row unchanged, record the historical duplicates, and require only that all thirty v652-v4 identifiers are unique and absent from the inherited identifier set.", "passing": "All 1,270 inherited rows remained unchanged while thirty unique noncolliding v652-v4 identifiers extended the chain to 1,300 rows.", "recurrence_guard": "Treat immutable predecessor rows as authoritative evidence and scope new-identifier uniqueness to the additive phase."},
    {"negative_id": "V6524-X1-N10", "category": "method_flow_count_key_assumption", "failed": "The first generated x1 unittest aggregate expected nonexistent top-level failed_witnesses and passing_witnesses count keys and received a KeyError; the aggregate earned zero credit.", "recovery": "Read the Method Flow schema's nested witness_results fail and pass counters without changing the ledger.", "passing": "The corrected bounded test observed equal retained fail and pass counts for every x1 recovery method.", "recurrence_guard": "Bind tests to the current Method Flow count schema instead of inferred aliases."},
    {"negative_id": "V6524-X1-N11", "category": "ordinary_document_cap_domain_assumption", "failed": "The first generated x1 unittest aggregate applied the ordinary twenty-thousand-word document cap to the 1,300-row machine-readable frozen-chain ledger and failed; the aggregate earned zero credit.", "recovery": "Apply the cap to ordinary narrative Markdown, HTML, and text documents while recording machine-ledger counts separately.", "passing": "Every ordinary narrative document remained at or below twenty thousand words, and the large immutable index stayed visible as a machine ledger.", "recurrence_guard": "Declare ordinary narrative and machine-ledger cap domains explicitly."},
    {"negative_id": "V6524-X1-N12", "category": "powershell_hash_literal_command_expression", "failed": "The first staged-summary wrapper embedded a semicolon-bearing Git command expression inside a PowerShell hash literal and failed parsing before any child command ran.", "recovery": "Compute Git head, status count, and diff exit as separate scalar variables before constructing the summary object.", "passing": "The corrected scalar-first summary reported all x1 counts, validation state, exact head, and tracked-diff state.", "recurrence_guard": "Keep command execution outside PowerShell hash-literal value expressions."},
]


SAFE_TASKS = [
    "Verify Tamar source, x1, evidence, and final ancestry read-only.",
    "Verify three source-to-final commits, zero merges, and one final parent.",
    "Replay all Tamar commit-local manifest contracts from immutable Git blobs.",
    "Fast-forward only Sylven's clean owned D-first lane.",
    "Prove local, upstream, tracking, and fresh-live equality before x2.",
    "Preserve all 8,383 inherited effective negatives additively.",
    "Preserve all 64 inherited open gaps and 65 inherited exact gates.",
    "Audit thirty proposal titles against all 1,270 frozen titles.",
    "Retain rejected collisions and their replacement rationale.",
    "Verify current official or primary sources without ingesting real data.",
    "Freeze exactly thirty proposals with all required fields.",
    "Freeze exactly 150 synthetic mutations without executing them in x1.",
    "Freeze thirty new safe-now portfolio tasks.",
    "Freeze thirty bounded candidate prototypes.",
    "Freeze ten phase-local skill ideas.",
    "Freeze ten family-current runner ideas.",
    "Freeze thirty additive CLEAN/FIX/REFINE tasks.",
    "Keep inherited completion evidence separate from Sylven credit.",
    "Record each operational failure and bounded recovery in Method Flow.",
    "Promote no Method Flow method without a passing bounded witness.",
    "Generate a sanitized phase-scoped GHC Family Index.",
    "Run workflow-plan refinement on a sanitized immediate segment.",
    "Run Reflection Remaster in audit mode on selected mechanisms.",
    "Verify versions without updating any application.",
    "Scan public phase files across five privacy and raw-identifier classes.",
    "Separate scanner definitions from confirmed payload findings.",
    "Enforce x1-only staged paths and no observed outcome.",
    "Enforce the twenty-thousand-word document cap.",
    "Enforce the owner-generated fifteen-thousand-file threshold.",
    "Hold terminal routing as PREPARED_NOT_SENT until exact-final proof.",
]

CANDIDATE_TASKS = [f"Build and bounded-test {proposal['mission_surface']}." for proposal in PROPOSALS]

SKILL_IDEAS = [
    "ghc-family-stream-and-network-framing-tribunals",
    "ghc-family-binary-media-and-package-tribunals",
    "ghc-family-runtime-envelope-tribunals",
    "ghc-family-gmut-spin-torsion-and-multipole-boards",
    "ghc-family-gmut-conformal-potential-boundary-boards",
    "ghc-family-hydrographic-proxy-boundary",
    "ghc-family-identity-enrolment-and-sync-boundary",
    "ghc-family-accessible-transfer-workflow",
    "ghc-family-stage20-paired-and-calibration-nonpromotion",
    "ghc-family-v652-v4-validation",
]

RUNNER_IDEAS = [
    "ghc_family_stream_network_tribunals.py",
    "ghc_family_binary_media_package_tribunals.py",
    "ghc_family_runtime_envelope_tribunals.py",
    "ghc_family_gmut_spin_multipole_boards.py",
    "ghc_family_gmut_conformal_boundary_boards.py",
    "ghc_family_hydrographic_proxy.py",
    "ghc_family_identity_enrolment_sync.py",
    "ghc_family_accessibility_thermo.py",
    "ghc_family_stage20_statistics.py",
    "ghc_family_v652_v4_detailed_validator.py",
]

CLEAN_TASKS = [
    "Replace unbounded baton display with fixed immutable slices.",
    "Replace large chunks with fifty-line EOF progression.",
    "Split combined read-only probes into exact scalar postconditions.",
    "Treat quiet fast-forward output as advisory and verify postconditions.",
    "Replace broad parallel inventory with exact Git-tree enumeration.",
    "Replace parallel line counting with one local process.",
    "Replace broad source search with exact standard-target verification.",
    "Replace blocked DOI redirect opens with bounded bibliographic metadata.",
    "Reject the inherited accessible date-picker collision.",
    "Document the Einstein-Cartan distinction from a general Cartan-form board.",
    "Document the Brown-York distinction from Israel junction conditions.",
    "Document Young-Laplace and Jurin distinction from the Kelvin equation.",
    "Document ACME base-protocol distinction from ACME ARI.",
    "Document WALLABY distinction from other zero-row catalog adapters.",
    "Use explicit score keys for novelty nearest-neighbour selection.",
    "Keep token distance subordinate to manual mechanism review.",
    "Use exact phase-root privacy scanning and scanner-definition quarantine.",
    "Use Git path-filtered blob hashes for commit-local manifests.",
    "Keep working-tree bytes distinct from immutable Git-blob evidence.",
    "Parse every public phase JSON document under explicit UTF-8.",
    "Keep experimental RFC status visible in the source ledger.",
    "Keep real data query, download, row, fit, and likelihood counters at zero.",
    "Keep real key, account, service, and interoperability counters at zero.",
    "Keep real worker, vessel, sounding, incident, and outcome counters at zero.",
    "Reserve manual, browser, assistive-technology, Māori-language, and affected-user review.",
    "Keep legal, cultural, place-name, remedy, and Māori decisions exact-gated.",
    "Keep sibling branches and worktrees untouched.",
    "Keep Sandbox, Hyper-V, elevation, security, installation, update, and reboot state unchanged.",
    "Credit exactly one successful final scoped pass and perform no replay.",
    "Keep terminal routing prepared and unsent until all exact-final gates pass.",
]

REJECTED_COLLISIONS = [
    {"candidate": "accessible date-picker audit", "reason": "An inherited title already isolates the same date-grid mechanism; replaced by a dual-listbox transfer workflow."},
    {"candidate": "WebAssembly binary tribunal", "reason": "The module-section and instruction mechanisms are already frozen; replaced by current DHCPv6 framing."},
    {"candidate": "Zarr version 3 tribunal", "reason": "The chunk-grid and codec pipeline mechanism is already frozen; replaced by ODF package duties."},
    {"candidate": "FLAC or Ogg tribunal", "reason": "Both framing mechanisms are already represented in the frozen chain; replaced by Standard MIDI File."},
    {"candidate": "Matroska EBML tribunal", "reason": "EBML variable-integer and nesting refusal is already frozen; replaced by MPEG-2 transport stream."},
    {"candidate": "Hadamard parametrix board", "reason": "Hadamard and Green-operator mechanisms are already frozen; replaced by Lanczos potential obligations."},
    {"candidate": "York-Lichnerowicz decomposition board", "reason": "Conformal constraint-decomposition mechanisms are already frozen; replaced by Brown-York quasilocal stress."},
    {"candidate": "Rosenbaum sensitivity or E-value board", "reason": "Sensitivity-to-unmeasured-confounding mechanisms are already frozen; replaced by DeLong and exact McNemar boards."},
    {"candidate": "ACME renewal-information profile", "reason": "ACME ARI is already frozen; the accepted proposal isolates the distinct base account-order-authorization protocol."},
    {"candidate": "generic hydrographic data authority matrix", "reason": "Generic authority vocabulary collided with inherited matrices; the accepted gate isolates raw soundings, derived bathymetry, charting disclosure, undersea features, and place-name stewardship."},
]
