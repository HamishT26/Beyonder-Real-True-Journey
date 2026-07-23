#!/usr/bin/env python3
"""Frozen Tavian Sol v652-v6 x1 data; this module contains no x2 observations."""

from __future__ import annotations


PHASE = "v652-v6"
OWNER = "Tavian Sol"
PRONOUNS = "they/them"
ROLE = "bounded CLI evidence integrator"
HOPE = "make the next handoff easier to trust without blurring any gate"
BRANCH = "codex/GHC-Family/tavian-sol-v652-v6-cli"
PHASE_ROOT = "docs/tavian-sol/v652-v6"

SOURCE_BRANCH = "codex/GHC-Family/eiren-kestrel-v648-v3-3-full-tools"
SOURCE_HEAD = "ad2a2e472c8e859296e62f1d2d6ce1f9f2b2b584"
SOURCE_ORIGIN = "3a77dacd759a499ffe94cbc281a3d7b343608e2d"
SOURCE_X1 = "7f347e548b64ea2a9065e129c3ec84dde000c13e"
SOURCE_EVIDENCE = "611a0afef841a516dd0a5cb1e9ac2448943b42c6"
SOURCE_CLOSEOUT = "516202a04e2930bfa787bcf257dafd72827cf9af"
SOURCE_ROUTE_CORRECTION = "fb47648a1c136b8147d5d52f84c6615b718bd3c8"
PRIOR_FROZEN = 1330
SOURCE_SEALED_NEGATIVES = 8734
INHERITED_NEGATIVES = 8736
INHERITED_OPEN_GAPS = 66
INHERITED_EXACT_GATES = 67
PRIMARY_FOCUS = "THOS Body with CBR Heart"
BOUNDED_PRACTICE = (
    "synthetic environmental-monitoring calibration, sample and sensor quality review, suspect-data quarantine, "
    "accessible quality notice, workload control, correction readback, and shift handover"
)

OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]
SOURCE_STATUS_CLASSES = ["current", "stable", "experimental", "watch"]
PROTECTED_GATES = [
    "empirical_data",
    "real_participants_or_operators",
    "professional_or_meteorological_authority",
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
        "proposal_id": f"V6526-P{number:02d}",
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
        "novelty_against_1330_frozen_proposals": novelty,
    }


PROPOSALS = [
    _proposal(1, "Microsoft Cabinet signature, reserve fields, folder table, file table, CFDATA checksum, compression type, continuation, name boundary, output budget, and refusal tribunal", "microsoft-cabinet", "THOS Body", "completed", ["SRC-MS-CAB"], "Microsoft Cabinet refusal", "No frozen mechanism covers Cabinet folder and file tables, CFDATA blocks, cabinet continuation, reserved areas, and extraction-name boundaries."),
    _proposal(2, "Java Object Serialization stream magic, version, type code, class descriptor, handle, back-reference, block data, reset, proxy descriptor, graph budget, and refusal tribunal", "java-serialization-stream", "THOS Body", "completed", ["SRC-JAVA-SERIAL"], "Java serialization stream refusal", "The frozen chain contains class-file framing but no Java Object Serialization handle graph, class descriptor, block-data, reset, and back-reference tribunal."),
    _proposal(3, "Android DEX magic, checksum, signature, endian tag, map list, identifier table, class definition, code item, LEB128, container boundary, and refusal tribunal", "android-dex", "THOS Body", "completed", ["SRC-ANDROID-DEX"], "Android DEX refusal", "No frozen proposal isolates DEX identifier tables, map ownership, code items, versioned containers, and LEB128-bounded offsets."),
    _proposal(4, "Python pyc magic, flags, source hash or timestamp, marshal type code, reference flag, recursive container, code-object reservation, depth budget, and refusal tribunal", "python-pyc-marshal", "THOS Body", "completed", ["SRC-PY-MARSHAL", "SRC-PEP552"], "Python pyc and marshal refusal", "No frozen proposal isolates Python pyc invalidation headers and the deliberately implementation-specific marshal reference and recursion surface."),
    _proposal(5, "Microsoft Compound File header, sector shift, DIFAT, FAT, mini FAT, directory entry, red-black sibling relation, stream chain, allocation cycle, and refusal tribunal", "microsoft-cfb", "THOS Body", "completed", ["SRC-MS-CFB"], "Microsoft Compound File refusal", "No frozen mechanism treats an OLE compound file as a bounded file system with FAT, mini-stream, DIFAT, directory-tree, and chain-cycle obligations."),
    _proposal(6, "ext4 superblock, feature flags, block group descriptor, inode, extent tree, directory entry, checksum, journal reservation, block budget, and refusal tribunal", "ext4-disk-layout", "THOS Body", "completed", ["SRC-EXT4"], "ext4 disk-layout refusal", "No frozen tribunal isolates ext4 group geometry, feature compatibility, inode and extent ownership, directory records, metadata checksums, and journal reservation."),
    _proposal(7, "ECMA-167 UDF anchor descriptor, volume descriptor sequence, partition map, file set descriptor, file entry, allocation descriptor, tag checksum, extent boundary, and refusal tribunal", "ecma167-udf", "THOS Body", "completed", ["SRC-ECMA167"], "ECMA-167 UDF refusal", "No frozen proposal covers ECMA-167 anchor and volume sequences, partition maps, descriptor tags, file entries, and allocation extents as one bounded mechanism."),
    _proposal(8, "QOI image magic, width, height, channels, colorspace, RGB or RGBA chunk, index hash, run length, pixel count, end marker, and refusal tribunal", "qoi-image", "THOS Body", "completed", ["SRC-QOI"], "QOI image refusal", "No frozen title covers QOI's stateful pixel index, run chunks, channel modes, exact pixel count, and eight-byte end marker."),
    _proposal(9, "PDF 2.0 header, indirect object, generation number, cross-reference table or stream, trailer, startxref, object stream, incremental update, cycle budget, and refusal tribunal", "pdf20-xref", "THOS Body", "completed", ["SRC-PDF20"], "PDF cross-reference refusal", "No frozen proposal isolates PDF indirect-object identity, xref table and stream alternatives, object streams, startxref, and incremental update chains."),
    _proposal(10, "BitTorrent bencode integer, byte string, list, dictionary key order, metainfo info slice, nesting, token count, byte budget, and refusal tribunal", "bittorrent-bencode", "THOS Body", "completed", ["SRC-BEP3"], "BitTorrent bencode refusal", "No frozen mechanism covers bencode canonical integer spelling, raw-byte dictionary ordering, recursive collections, and exact metainfo info-slice preservation."),
    _proposal(11, "ICC profile size, preferred CMM type, version, device class, color space, PCS, date, signature, rendering intent, tag table, overlap, and refusal tribunal", "icc-profile", "THOS Body", "completed", ["SRC-ICC1"], "ICC profile refusal", "No frozen proposal isolates ICC profile header semantics, profile connection space, rendering intent, tag signatures, tag offsets, and overlap constraints."),
    _proposal(12, "Amazon Ion binary version marker, type descriptor, length, VarUInt, symbol table, annotation wrapper, struct field SID, nop padding, container budget, and refusal tribunal", "amazon-ion-binary", "THOS Body", "completed", ["SRC-ION"], "Amazon Ion binary refusal", "No frozen proposal covers Ion's binary version marker, typed lengths, symbol identifiers, annotation wrappers, struct field SIDs, and nop padding."),
    _proposal(13, "GMUT Lovelock generalized Kronecker delta, curvature order, Euler density, dimension threshold, divergence-free tensor, coupling, boundary reservation, EFT, unit, and observation-firewall board", "lovelock-tensor", "GMUT Mind", "completed", ["SRC-LOVELOCK1971"], "Lovelock-tensor obligations", "No frozen board isolates Lovelock curvature order, generalized delta, dimension-dependent Euler densities, and divergence-free field-tensor obligations."),
    _proposal(14, "GMUT Gauss-Codazzi induced metric, unit normal, extrinsic curvature, tangential projection, normal projection, sign convention, hypersurface boundary, unit, and observation-firewall board", "gauss-codazzi", "GMUT Mind", "completed", ["SRC-GOURGOULHON31"], "Gauss-Codazzi obligations", "No frozen board isolates the paired tangential and normal curvature projections, induced connection, normal orientation, and sign convention of Gauss-Codazzi."),
    _proposal(15, "GMUT Friedmann scale factor, Hubble rate, spatial curvature, density, pressure, continuity equation, equation-of-state reservation, initial condition, unit, and observation-firewall board", "friedmann-system", "GMUT Mind", "completed", ["SRC-FRIEDMANN1922"], "Friedmann-system obligations", "No frozen proposal isolates the homogeneous scale-factor equations, curvature convention, continuity relation, equation-of-state reservation, and initial-condition boundary."),
    _proposal(16, "GMUT Tolman-Oppenheimer-Volkoff pressure gradient, enclosed mass, energy density, equation of state, central boundary, surface condition, compactness reservation, unit, and observation-firewall board", "tov-system", "GMUT Mind", "completed", ["SRC-OV1939"], "Tolman-Oppenheimer-Volkoff obligations", "No frozen board isolates hydrostatic pressure balance, enclosed mass, center and surface conditions, equation-of-state dependence, and compactness reservation."),
    _proposal(17, "GMUT Kerr-Schild background metric, null one-form, scalar profile, inverse metric, determinant relation, geodesic condition, coordinate domain, boundary, unit, and observation-firewall board", "kerr-schild", "GMUT Mind", "completed", ["SRC-KERRSCHILD1965"], "Kerr-Schild obligations", "No frozen proposal isolates the rank-one Kerr-Schild deformation, shared null property, inverse and determinant relations, and geodesic-condition boundary."),
    _proposal(18, "Accessible consistent-help set-of-pages, mechanism kind, serialized relative order, page variation, direct link, user-initiated change, absence boundary, fallback, and manual-evaluation audit", "consistent-help", "THOS Body", "completed", ["SRC-WCAG22-HELP"], "consistent-help structure", "No frozen accessibility proposal isolates repeated human-contact, self-help, and automated-contact mechanisms by serialized relative order across a set of pages and user-initiated page variation."),
    _proposal(19, "IETF vCard BEGIN and END, version, UTF-8, content line, group, property name, parameter, value escaping, line folding, cardinality, resource budget, and refusal tribunal", "ietf-vcard", "THOS Body", "completed", ["SRC-RFC6350"], "IETF vCard refusal", "No frozen tribunal isolates vCard entity framing, mandatory version and formatted-name properties, grouped content lines, parameter and value escaping, UTF-8, and vCard-specific cardinality."),
    _proposal(20, "Stage 20 integrated discrimination improvement event mean, nonevent mean, model difference, denominator, optimism, uncertainty, survival reservation, utility distinction, and nonpromotion board", "integrated-discrimination-improvement", "Trinity Mandala bridge", "completed", ["SRC-PENCINA2008"], "integrated-discrimination-improvement nonpromotion", "The inherited net-reclassification board does not isolate the difference between two models' event and nonevent discrimination slopes."),
    _proposal(21, "Stage 20 calibration belt polynomial order, likelihood-ratio selection, confidence region, probability range, multiple crossing, sample size, uncertainty, interpretation, and nonpromotion board", "calibration-belt", "Trinity Mandala bridge", "completed", ["SRC-NATTINO2014"], "calibration-belt nonpromotion", "No frozen board isolates a calibration belt's polynomial selection, confidence region, probability ranges, and multiple-crossing interpretation."),
    _proposal(22, "Stage 20 precision-recall prevalence, precision denominator, recall denominator, threshold order, average precision, interpolation reservation, uncertainty, comparison, and nonpromotion board", "precision-recall", "Trinity Mandala bridge", "completed", ["SRC-DAVIS2006"], "precision-recall nonpromotion", "No frozen proposal isolates precision-recall prevalence dependence, average-precision convention, threshold ordering, interpolation, and comparison boundaries."),
    _proposal(23, "Stage 20 conformal prediction nonconformity score, calibration split, exchangeability assumption, rank quantile, finite-sample coverage, set size, efficiency, shift refusal, and nonpromotion board", "conformal-prediction", "Trinity Mandala bridge", "completed", ["SRC-VOVK2005"], "conformal-prediction nonpromotion", "No frozen board isolates split calibration, nonconformity ranking, exchangeability, marginal coverage, set-size efficiency, and distribution-shift refusal."),
    _proposal(24, "THOS ocean buoy platform identity, mooring position, sensor depth, calibration lineage, timestamp, quality flag, telemetry gap, workload, correction readback, and shift-handover proxy", "ocean-buoy-proxy", "THOS Body", "represented", ["SRC-WMO-OBS"], "ocean buoy quality proxy", "No frozen proxy isolates ocean-buoy mooring and depth metadata, telemetry gaps, calibration lineage, quality flags, and correction handover."),
    _proposal(25, "THOS ambient-air monitor siting, analyzer identity, calibration check, drift, averaging period, completeness, suspect-data quarantine, accessible quality notice, workload, and handover proxy", "air-quality-proxy", "THOS Body", "represented", ["SRC-EPA-AIR-QA"], "ambient-air monitoring proxy", "No frozen proxy isolates ambient-air analyzer siting, calibration checks, drift, averaging completeness, suspect-data quarantine, and accessible handover notice."),
    _proposal(26, "Freed ID SPIFFE trust domain, SPIFFE ID path, SVID format, bundle, workload attestation reservation, rotation, expiry, audience, privacy, and nonproduction profile", "spiffe-id-svid", "Freed ID and CBR Heart", "represented", ["SRC-SPIFFE"], "SPIFFE ID and SVID profile", "No frozen identity profile isolates SPIFFE trust-domain naming, workload paths, SVID and bundle relationships, rotation, and attestation reservation."),
    _proposal(27, "Freed ID macaroon root key identifier, first-party caveat, third-party caveat, discharge macaroon, binding, attenuation, verification context, replay, privacy, and nonproduction profile", "macaroon-caveats", "Freed ID and CBR Heart", "represented", ["SRC-MACAROONS"], "macaroon caveat profile", "No frozen identity profile isolates macaroon attenuation, contextual first- and third-party caveats, discharge binding, and verification-context boundaries."),
    _proposal(28, "Freed ID SAML 2.0 artifact type, endpoint index, source identifier, message handle, artifact resolution request, response correlation, issuer, replay, privacy, and nonproduction profile", "saml-artifact-resolution", "Freed ID and CBR Heart", "represented", ["SRC-SAML2"], "SAML artifact-resolution profile", "No frozen profile isolates the SAML artifact reference and back-channel resolution exchange, endpoint index, source identifier, message handle, and response correlation."),
    _proposal(29, "GMUT Suzaku HEASARC master catalog, sequence number, target, public date, instrument, event file, calibration database, response, screening, checksum, covariance, provenance, and zero-row likelihood-refusal adapter", "suzaku-zero-row", "GMUT Mind", "open_gap", ["SRC-SUZAKU-ARCHIVE", "SRC-SUZAKU-MASTER"], "Suzaku likelihood readiness", "No frozen adapter targets the Suzaku archive and master-catalog lifecycle with sequence, instrument, screening, calibration, response, checksum, and covariance duties."),
    _proposal(30, "CBR community marine observation photograph, timestamp, location precision, contributor consent, taonga-species sensitivity, moderation, correction, withdrawal, reuse, affected-party, iwi, hapū, and Māori-authority reservation", "community-marine-observation-authority", "Freed ID and CBR Heart", "exact_gate", ["SRC-DOC-CITIZEN-MARINE", "SRC-MAORI-DATA", "SRC-PRIVACY-NZ"], "community marine observation data and authority reservation", "No frozen gate isolates community-contributed marine photographs and location precision with contributor consent, taonga-species sensitivity, moderation, correction, withdrawal, reuse, and iwi, hapū, and Māori data authority."),
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
    _source("SRC-MS-CAB", "current", "official_platform_specification", "Microsoft Cabinet File Format", "https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-cab/", "Supports disposable cabinet bytes only."),
    _source("SRC-JAVA-SERIAL", "stable", "official_platform_specification", "Java Object Serialization Stream Protocol", "https://docs.oracle.com/en/java/javase/17/docs/specs/serialization/protocol.html", "Supports inert synthetic stream tokens only; no class loading or object instantiation."),
    _source("SRC-ANDROID-DEX", "current", "official_platform_specification", "Android Dalvik executable format", "https://source.android.com/docs/core/runtime/dex-format", "Supports disposable DEX structures only."),
    _source("SRC-PY-MARSHAL", "current", "official_project_documentation", "Python marshal internal object serialization", "https://docs.python.org/3/library/marshal.html", "Supports version-bounded inert marshal fixtures only."),
    _source("SRC-PEP552", "stable", "official_project_specification", "PEP 552 deterministic pycs", "https://peps.python.org/pep-0552/", "Supports pyc invalidation-header vocabulary only."),
    _source("SRC-MS-CFB", "current", "official_platform_specification", "Microsoft Compound File Binary File Format", "https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-cfb/50708a61-81d9-49c8-ab9c-43c98a795242", "Supports disposable compound-file bytes only."),
    _source("SRC-EXT4", "current", "official_kernel_documentation", "Linux ext4 on-disk layout", "https://www.kernel.org/doc/html/latest/filesystems/ext4/overview.html", "Supports synthetic non-mounted file-system structures only."),
    _source("SRC-ECMA167", "stable", "official_open_standard", "ECMA-167 volume and file structure", "https://ecma-international.org/publications-and-standards/standards/ecma-167/", "Supports disposable volume descriptors only."),
    _source("SRC-QOI", "stable", "primary_format_specification", "Quite OK Image Format 1.0", "https://qoiformat.org/qoi-specification.pdf", "Supports synthetic image bytes only."),
    _source("SRC-PDF20", "current", "official_international_standard_access", "ISO 32000-2 PDF 2.0", "https://pdfa.org/resource/iso-32000-pdf/", "Supports disposable non-rendered PDF structures only."),
    _source("SRC-BEP3", "stable", "official_project_standard", "BitTorrent BEP 3 and bencoding", "https://www.bittorrent.org/beps/bep_0003.html", "Supports nonnetwork synthetic bencoded values only."),
    _source("SRC-ICC1", "current", "official_industry_specification", "ICC.1:2022 profile format", "https://www.color.org/specifications/ICC.1-2022-05.pdf", "Supports disposable colour-profile bytes only."),
    _source("SRC-ION", "current", "official_project_specification", "Amazon Ion binary encoding", "https://amazon-ion.github.io/ion-docs/docs/binary.html", "Supports synthetic Ion streams only."),
    _source("SRC-LOVELOCK1971", "stable", "primary_research", "The Einstein tensor and its generalizations", "https://doi.org/10.1063/1.1665613", "Supports formal curvature-tensor vocabulary only."),
    _source("SRC-GOURGOULHON31", "stable", "primary_research_review", "3+1 Formalism and Bases of Numerical Relativity", "https://arxiv.org/abs/gr-qc/0703035", "Supports formal hypersurface-projection vocabulary only."),
    _source("SRC-FRIEDMANN1922", "stable", "primary_research", "Über die Krümmung des Raumes", "https://cds.cern.ch/record/420425/", "Supports formal homogeneous-cosmology vocabulary only."),
    _source("SRC-OV1939", "stable", "primary_research", "On Massive Neutron Cores", "https://doi.org/10.1103/PhysRev.55.374", "Supports formal hydrostatic-equilibrium vocabulary only."),
    _source("SRC-KERRSCHILD1965", "stable", "primary_research", "Some algebraically degenerate solutions of Einstein's gravitational field equations", "https://cir.nii.ac.jp/crid/1360576121806699008", "Supports formal metric-ansatz vocabulary only."),
    _source("SRC-WCAG22-HELP", "current", "official_accessibility_standard", "WCAG 2.2 Consistent Help", "https://www.w3.org/WAI/WCAG22/Understanding/consistent-help", "Supports structural relative-order checks across synthetic page sets; complete conformance remains reserved."),
    _source("SRC-RFC6350", "stable", "official_internet_standard", "RFC 6350 vCard Format Specification", "https://www.rfc-editor.org/info/rfc6350/", "Supports disposable synthetic vCards only; no real contact, directory, message, account, or network exchange."),
    _source("SRC-PENCINA2008", "stable", "primary_research", "Evaluating the added predictive ability of a new marker", "https://doi.org/10.1002/sim.2929", "Supports discrimination-improvement obligations only; clinical utility remains external."),
    _source("SRC-NATTINO2014", "stable", "primary_research", "A new calibration test and a reappraisal of the calibration belt", "https://pubmed.ncbi.nlm.nih.gov/24497413/", "Supports calibration-belt obligations only."),
    _source("SRC-DAVIS2006", "stable", "primary_research", "The relationship between Precision-Recall and ROC curves", "https://doi.org/10.1145/1143844.1143874", "Supports precision-recall obligations only."),
    _source("SRC-VOVK2005", "stable", "primary_research_monograph", "Algorithmic Learning in a Random World", "https://link.springer.com/book/10.1007/b106715", "Supports conformal-prediction obligation vocabulary only."),
    _source("SRC-WMO-OBS", "current", "official_intergovernmental_guidance", "WMO Guide to Instruments and Methods of Observation WMO-No. 8", "https://community.wmo.int/site/knowledge-hub/programmes-and-initiatives/instruments-and-methods-of-observation-programme-imop/guide-instruments-and-methods-of-observation-wmo-no-8-0", "Supplies learning context only; no environmental-monitoring competence or authority."),
    _source("SRC-EPA-AIR-QA", "current", "official_environmental_guidance", "US EPA ambient-air monitoring quality assurance guidance", "https://www.epa.gov/amtic/ambient-air-monitoring-quality-assurance-guidance-documents", "Supports synthetic quality-workflow vocabulary only; no operational or professional authority."),
    _source("SRC-SPIFFE", "current", "official_identity_standard", "SPIFFE Identity and Verifiable Identity Document", "https://spiffe.io/docs/latest/spiffe-specs/spiffe-id/", "Supports synthetic identifiers and SVID metadata only; no real credentials or workloads."),
    _source("SRC-MACAROONS", "stable", "primary_research", "Macaroons: Cookies with Contextual Caveats for Decentralized Authorization", "https://research.google/pubs/macaroons-cookies-with-contextual-caveats-for-decentralized-authorization-in-the-cloud/", "Supports synthetic caveat graphs only; no real root keys or services."),
    _source("SRC-SAML2", "stable", "official_identity_standard", "SAML 2.0 Assertions and Protocols", "https://docs.oasis-open.org/security/saml/v2.0/saml-core-2.0-os.pdf", "Supports nonnetwork synthetic artifact-resolution vectors only."),
    _source("SRC-SUZAKU-ARCHIVE", "current", "official_scientific_archive", "NASA HEASARC Suzaku Archive", "https://heasarc.gsfc.nasa.gov/docs/suzaku/archive/suza_archivestart.html", "Supports a zero-row adapter contract only; no query or download occurs."),
    _source("SRC-SUZAKU-MASTER", "current", "official_dataset_catalogue", "NASA HEASARC Suzaku Master Catalog", "https://heasarc.gsfc.nasa.gov/W3Browse/suzaku/suzamaster.html", "Supplies schema and provenance context only; no observation occurs."),
    _source("SRC-DOC-CITIZEN-MARINE", "current", "official_conservation_context", "DOC community marine citizen-science tools", "https://www.doc.govt.nz/news/media-releases/2025-media-releases/from-laptop-to-tidepool-always-be-naturing-with-new-ways-to-safeguard-marine-life/", "Supplies public programme context only; no observation, consent, privacy, legal, cultural, data-governance, affected-party, iwi, hapū, or Māori-authority decision."),
    _source("SRC-MAORI-DATA", "current", "maori_authority_guidance", "Te Mana Raraunga principles of Māori data sovereignty", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Keeps Māori data decisions with Māori authority."),
    _source("SRC-PRIVACY-NZ", "current", "official_legislation", "Privacy Act 2020", "https://www.legislation.govt.nz/act/public/2020/31/en/latest/", "Keeps legal interpretation, disclosure, and remedy exact-gated."),
]


ACTIVATION_EXTERNAL_NEGATIVES = [
    {"negative_id": "V6525-EXT-ACT-01", "category": "exclusion_plan_summary_missing_discovered_field", "failed": "A later read-only exclusion-plan summary asked for a nonexistent discovered row field after planning had already succeeded.", "credit": "zero", "boundary": "External to Eiren's sealed head; carried additively without changing its canonical receipt."},
    {"negative_id": "V6525-EXT-ACT-02", "category": "post_success_equality_wrapper_timeout", "failed": "A combined wrapper timed out after the successful canonical receipt had already established four-way equality.", "credit": "zero", "boundary": "External to Eiren's sealed head; no replay and no retroactive receipt mutation."},
]

X1_OPERATIONAL_NEGATIVES = [
    {"negative_id": "V6526-X1-N01", "category": "combined_source_probe_timeout", "failed": "The first combined branch, status, object, packet-size, upstream, and tracking probe exceeded its wrapper bound and returned no usable output.", "recovery": "Split the source proof into exact scalar Git reads.", "passing": "Exact head, branch, clean state, upstream, tracking, and live remote were each established by bounded reads.", "recurrence_guard": "Do not combine multiple slow Windows Git operations under one short wrapper."},
    {"negative_id": "V6526-X1-N02", "category": "packet_chunk_pipeline_timeout", "failed": "The first line-numbered git-show pipeline timed out before returning a readable packet chunk.", "recovery": "Bind the clean working file to the exact Git blob, then use bounded direct line-array reads.", "passing": "The working-file hash equalled the exact-head blob and all 546 lines were read through EOF in bounded chunks.", "recurrence_guard": "For a verified clean blob, prefer bounded direct reads over a PowerShell pipeline around git show."},
    {"negative_id": "V6526-X1-N03", "category": "powershell_empty_pipe_metadata_probe", "failed": "The first skill-metadata probe piped directly from a foreach statement and failed with an empty-pipe-element parser error.", "recovery": "Assign the foreach results to an array before formatting.", "passing": "The corrected metadata probe returned exact line and byte counts for every routed skill and reference.", "recurrence_guard": "Materialize compound PowerShell statement results before a formatting pipeline."},
    {"negative_id": "V6526-X1-N04", "category": "convertfrom_json_depth_unavailable", "failed": "The first receipt probe used a ConvertFrom-Json Depth parameter unavailable in the installed PowerShell and earned no receipt-parse credit.", "recovery": "Use the supported ConvertFrom-Json surface without the unsupported parameter.", "passing": "The corrected parser read the external receipt and exposed all required exact-final fields.", "recurrence_guard": "Probe the installed PowerShell surface or use only parameters supported by Windows PowerShell 5.1."},
    {"negative_id": "V6526-X1-N05", "category": "broad_manifest_search_timeout", "failed": "A broad multi-root search for manifest helpers exceeded its wrapper bound and returned no review evidence.", "recovery": "Search the exact final-validator, correction builder, and correction test paths only.", "passing": "The bounded search located the batched manifest verifier, and all six source contracts replayed with zero issues.", "recurrence_guard": "Search exact lifecycle files before widening to phase roots."},
    {"negative_id": "V6526-X1-N06", "category": "worktree_add_wrapper_timeout_after_completion", "failed": "The worktree-add wrapper timed out after Git had already created the requested branch and worktree, so the wrapper itself earned zero creation credit.", "recovery": "Do not repeat creation; inspect the exact path, gitdir, head, branch, and status read-only.", "passing": "The unique Tavian worktree existed at the exact source head on the intended branch with a clean status.", "recurrence_guard": "After any worktree-add timeout, inspect exact postconditions before considering a retry."},
    {"negative_id": "V6526-X1-N07", "category": "combined_post_add_diagnostic_timeout", "failed": "The first combined post-timeout worktree-list and ref diagnostic also exceeded its bound.", "recovery": "Split direct filesystem gitdir inspection from the worktree-local Git status check.", "passing": "The split probes established the registered gitdir, exact head, exact branch, and clean worktree.", "recurrence_guard": "Avoid full worktree-list enumeration when an exact path and branch are already known."},
    {"negative_id": "V6526-X1-N08", "category": "novelty_tuple_tie_comparison", "failed": "A one-title novelty probe allowed Python tuple comparison to reach dictionary values on a score tie and raised TypeError.", "recovery": "Select the maximum with an explicit numeric score key.", "passing": "The corrected score-key probe returned the nearest frozen title deterministically.", "recurrence_guard": "Use an explicit key whenever score tuples contain non-orderable payloads."},
    {"negative_id": "V6526-X1-N09", "category": "stale_multi_block_patch_context", "failed": "The first combined safe-task, skill, runner, refinement, and collision patch failed atomically because one expected context block did not match.", "recovery": "Read the exact current tail and apply smaller reviewed blocks independently.", "passing": "The safe-task, skill, runner, refinement, and rejected-collision blocks were updated through exact-context patches.", "recurrence_guard": "Split multi-section semantic patches after a mechanical template transform."},
    {"negative_id": "V6526-X1-N10", "category": "repeated_native_search_timeout", "failed": "A loop of repeated native fixed-string searches for inherited template residue exceeded its wrapper bound before producing a complete audit.", "recovery": "Read the two exact files through one bounded PowerShell Select-String call with the reviewed literal pattern set.", "passing": "The bounded two-file residue audit completed with zero matching stale strings.", "recurrence_guard": "Use one in-process exact-file scan instead of repeatedly launching a native search process for many literals."},
    {"negative_id": "V6526-X1-N11", "category": "semantic_novelty_threshold_failure", "failed": "The first complete thirty-title novelty check stopped because inherited focus-not-obscured, Soret-Dufour, and environmental-authority mechanisms collided semantically or crossed the 0.60 token threshold.", "recovery": "Retain the failed audit, replace the colliding mechanisms, and rerun only the isolated novelty check.", "passing": "The corrected thirty-title audit passed with all rows manually mechanism-distinct and a maximum token Jaccard of 0.575758.", "recurrence_guard": "Search inherited titles for exact mechanisms before treating lexical distance as sufficient novelty evidence."},
    {"negative_id": "V6526-X1-N12", "category": "diagnostic_console_encoding_failure", "failed": "A candidate-term diagnostic reached a Māori macron in an inherited title under the legacy console encoding and raised UnicodeEncodeError after partial output.", "recovery": "Set PYTHONUTF8 and PYTHONIOENCODING before the same bounded read-only diagnostic.", "passing": "The UTF-8 diagnostic completed across every requested term and retained the inherited Māori-language title exactly.", "recurrence_guard": "Set explicit UTF-8 for Python text probes on Windows before printing repository content."},
    {"negative_id": "V6526-X1-N13", "category": "overview_word_floor_failure", "failed": "The first bounded overview measurement found 1,125 words, below the declared 1,500-word three-page-equivalent floor.", "recovery": "Add substantive mechanism-cluster, mutation-grammar, evidence-ownership, and routing boundaries without adding x2 observations.", "passing": "The corrected overview measured 1,773 words and remained x1-only.", "recurrence_guard": "Measure the generated narrative before builder execution and expand only with phase-relevant boundary content."},
    {"negative_id": "V6526-X1-N14", "category": "repeated_empty_pipe_receipt_probe", "failed": "A post-build receipt probe repeated the direct foreach-to-pipeline PowerShell form and failed with an empty-pipe-element parser error.", "recovery": "Assign receipt rows to an array before sending them to Format-Table.", "passing": "The corrected array-backed probe returned the existing receipt fields, including valid x1, workflow, Method Flow, privacy, and manifest values.", "recurrence_guard": "Apply the already established array-materialization rule to every compound PowerShell reporting loop."},
    {"negative_id": "V6526-X1-N15", "category": "guessed_tool_receipt_filenames", "failed": "The corrected receipt table guessed two nonexistent Reflection Remaster and GHC Family Index receipt filenames and produced path-not-found diagnostics.", "recovery": "Enumerate only the two exact output directories before reading any tool artifacts.", "passing": "The bounded enumeration returned the four Reflection Remaster outputs and two GHC Family Index outputs at their actual names.", "recurrence_guard": "Enumerate exact tool output directories instead of inferring receipt filenames from other runners."},
    {"negative_id": "V6526-X1-N16", "category": "workflow_output_schema_key_mismatch", "failed": "The first independent x1 audit expected a normalized_plan key that the workflow refinement output does not expose and raised KeyError after earlier checks passed.", "recovery": "Inspect the exact top-level schema and read the preserved normalized request through candidate_request.", "passing": "The corrected audit verified Eiren as full-repository-suite owner and Tavian as launch-scoped-validator owner from candidate_request.", "recurrence_guard": "Inspect exact workflow output keys before traversing nested ownership fields."},
    {"negative_id": "V6526-X1-N17", "category": "inherited_chain_stale_label_false_positive", "failed": "The corrected independent audit treated a historically valid inherited Ilyra proposal title as a current stale-label failure.", "recovery": "Preserve the inherited 1,330 rows unchanged and scope stale-label checks to current files and the thirty new proposal rows.", "passing": "The scoped audit found one legitimate inherited Ilyra title, zero such titles in the new rows, and no current Sylven or old-count residue.", "recurrence_guard": "Exclude immutable inherited proposal payloads from current-lane stale-label assertions while still checking new rows."},
]


SAFE_TASKS = [
    "Verify Eiren source, x1, evidence, closeout, correction, and final ancestry read-only.",
    "Verify five corrected Eiren source-phase commits, zero merges, and one final parent.",
    "Replay all six Eiren commit-local manifest contracts from immutable Git blobs.",
    "Create only Tavian's unique additive D-first lane from the exact Eiren head.",
    "Prove local, upstream, tracking, and fresh-live equality before x2.",
    "Preserve all 8,736 inherited effective negatives additively, including two external activation failures.",
    "Preserve all 66 inherited open gaps and 67 inherited exact gates.",
    "Audit thirty proposal titles against all 1,330 frozen titles.",
    "Retain rejected collisions and their replacement rationale.",
    "Verify current official or primary sources without ingesting real data.",
    "Freeze exactly thirty proposals with all required fields.",
    "Freeze exactly 150 synthetic mutations without executing them in x1.",
    "Freeze thirty new safe-now portfolio tasks.",
    "Freeze thirty bounded candidate prototypes.",
    "Freeze ten phase-local skill ideas.",
    "Freeze ten family-current runner ideas.",
    "Freeze thirty additive CLEAN/FIX/REFINE tasks.",
    "Keep inherited completion evidence separate from Tavian credit.",
    "Record each operational failure and bounded recovery in Method Flow.",
    "Promote no Method Flow method without a passing bounded witness.",
    "Generate a sanitized phase-scoped GHC Family Index.",
    "Run workflow-plan refinement on a sanitized immediate segment.",
    "Run Reflection Remaster in audit mode on selected mechanisms.",
    "Verify versions without updating any application.",
    "Scan public phase files across five privacy and raw-identifier classes.",
    "Separate scanner definitions from confirmed payload findings.",
    "Enforce x1-only staged paths and no observed outcome.",
    "Enforce the one-hundred-thousand-word narrative and baton cap.",
    "Enforce the owner-generated two-thousand-file threshold.",
    "Hold terminal routing as PREPARED_NOT_SENT until exact-final proof.",
]

CANDIDATE_TASKS = [f"Build and bounded-test {proposal['mission_surface']}." for proposal in PROPOSALS]

SKILL_IDEAS = [
    "ghc-family-container-object-stream-tribunals",
    "ghc-family-dex-pyc-compound-storage-tribunals",
    "ghc-family-filesystem-image-profile-tribunals",
    "ghc-family-gmut-hypersurface-cosmology-boards",
    "ghc-family-gmut-stellar-kerr-schild-boards",
    "ghc-family-environmental-monitoring-proxy-boundary",
    "ghc-family-spiffe-macaroon-saml-boundary",
    "ghc-family-consistent-help-and-vcard-boundary",
    "ghc-family-stage20-discrimination-calibration-conformal-nonpromotion",
    "ghc-family-v652-v6-validation",
]

RUNNER_IDEAS = [
    "ghc_family_container_object_stream_tribunals.py",
    "ghc_family_dex_pyc_compound_storage_tribunals.py",
    "ghc_family_filesystem_image_profile_tribunals.py",
    "ghc_family_gmut_hypersurface_cosmology_boards.py",
    "ghc_family_gmut_stellar_kerr_schild_boards.py",
    "ghc_family_environmental_monitoring_proxy.py",
    "ghc_family_spiffe_macaroon_saml_boundary.py",
    "ghc_family_consistent_help_and_vcard_boundary.py",
    "ghc_family_stage20_discrimination_calibration_conformal.py",
    "ghc_family_v652_v6_detailed_validator.py",
]

CLEAN_TASKS = [
    "Split combined read-only probes into exact scalar postconditions.",
    "Move PowerShell command execution outside expression and hash-literal values.",
    "Replace broad inventory with exact rg filename and phase-root enumeration.",
    "Quote every Git revision containing braces, carets, or upstream syntax.",
    "Replace repeated Get-Content line counts with bounded direct reads.",
    "Inspect frozen-index schema keys before iterating proposal rows.",
    "Separate bulk mechanical generation from trailing status enumeration.",
    "Refresh transformed context before applying a large semantic patch.",
    "Document Cabinet folder and CFDATA ownership as distinct from archive extraction generally.",
    "Document Java serialization graphs as distinct from Java class-file framing.",
    "Document DEX identifier and code-item ownership as distinct from JVM class files.",
    "Document ext4 extent and group ownership as distinct from FAT cluster chains.",
    "Document Gauss-Codazzi projections as distinct from generic ADM labels.",
    "Document Suzaku archive products as distinct from IXPE and Fermi adapters.",
    "Use explicit score keys for novelty nearest-neighbour selection.",
    "Keep token distance subordinate to manual mechanism review.",
    "Use exact phase-root privacy scanning and scanner-definition quarantine.",
    "Use Git path-filtered blob hashes for commit-local manifests.",
    "Keep working-tree bytes distinct from immutable Git-blob evidence.",
    "Parse every public phase JSON document under explicit UTF-8.",
    "Keep real data query, download, row, fit, and likelihood counters at zero.",
    "Keep real key, account, service, and interoperability counters at zero.",
    "Keep real worker, buoy, monitor, sensor, sample, observation, incident, and outcome counters at zero.",
    "Reserve manual, browser, assistive-technology, Māori-language, and affected-user review.",
    "Keep legal, cultural, environmental-data, remedy, and Māori decisions exact-gated.",
    "Keep sibling branches and worktrees untouched.",
    "Keep Sandbox, Hyper-V, elevation, security, installation, update, and reboot state unchanged.",
    "Credit exactly one successful exact-final launch-scoped aggregate and perform no replay.",
    "Keep terminal routing prepared and unsent until all exact-final gates pass.",
    "Keep owner additions below the measured two-thousand-file trigger.",
]

REJECTED_COLLISIONS = [
    {"candidate": "focus-not-obscured structural audit", "reason": "The exact sticky-overlay and focus-visibility mechanism is inherited; replaced by consistent-help relative order across page sets."},
    {"candidate": "Soret-Dufour nonconversion classifier", "reason": "The exact coupled heat-mass flux mechanism is inherited; replaced by an IETF vCard format tribunal."},
    {"candidate": "Apache ORC tribunal", "reason": "The exact stripe, stream, footer, postscript, compression, and row-index mechanism is inherited; replaced by vCard framing, grouped content lines, value escaping, and cardinality."},
    {"candidate": "Zstandard or Brotli frame tribunal", "reason": "Both exact compression mechanisms are already frozen; replaced by Microsoft Cabinet folder and CFDATA ownership."},
    {"candidate": "MessagePack tribunal", "reason": "The exact marker and collection mechanism is already frozen; replaced by Amazon Ion symbol and annotation duties."},
    {"candidate": "WebAssembly, DWARF, ELF, or PE tribunal", "reason": "Those exact binary mechanisms are already frozen; replaced by DEX, pyc, CFB, and ext4 duties."},
    {"candidate": "BigTIFF or FITS tribunal", "reason": "Those exact image and science-container mechanisms are already frozen; replaced by QOI, ICC, and PDF structures."},
    {"candidate": "BSSN or Raychaudhuri board", "reason": "Those formal mechanisms are already frozen; replaced by Lovelock, Gauss-Codazzi, Friedmann, TOV, and Kerr-Schild obligations."},
    {"candidate": "decision curve, Brier score, DeLong, or NRI board", "reason": "Those exact evaluation mechanisms are already frozen; replaced by IDI, calibration belt, precision-recall, and conformal prediction."},
    {"candidate": "OAuth PAR, DPoP, or SCIM profile", "reason": "Those protocol mechanisms are already frozen; replaced by SPIFFE, macaroon, and SAML artifact-resolution profiles."},
    {"candidate": "NICER or IXPE zero-row adapter", "reason": "Those archive lifecycles are already frozen; replaced by the distinct Suzaku master-catalog and instrument-product lifecycle."},
    {"candidate": "generic meteorological handover", "reason": "A weather-station proxy is inherited; accepted THOS proposals isolate ocean-buoy telemetry and ambient-air analyzer quality workflows."},
    {"candidate": "generic environmental authority matrix", "reason": "The accepted gate specifically reserves community-contributed marine photographs, location precision, consent, taonga-species sensitivity, moderation, correction, withdrawal, reuse, and iwi, hapū, and Māori data authority."},
]
