#!/usr/bin/env python3
"""Frozen Tamar Vey v652-v3 x1 data with no x2 observations."""

from __future__ import annotations


PHASE = "v652-v3"
OWNER = "Tamar Vey"
PRONOUNS = "they/them"
ROLE = "relational evidence-systems cartographer and boundary keeper"
HOPE = "keep decisions legible, failures recoverable, and authority boundaries intact"
BRANCH = "codex/GHC-Family/tamar-vey-full-tools"
PHASE_ROOT = "docs/tamar-vey/v652-v3"

SOURCE_BRANCH = "codex/GHC-Family/orin-thale-v642-v6-full-tools"
SOURCE_HEAD = "fa060eec3071694e1aff8eaf7d76d6c4b0f8075e"
SOURCE_ORIGIN = "f168bcb798715d61d8b0a9ec2c6646a7af09ce29"
SOURCE_X1 = "3f5b49dc1a380452593c8080c3ae134e654c2079"
SOURCE_EVIDENCE = "d185405470b9205a21d9b018bc0d3f7f44f49444"
SOURCE_CLOSEOUT = "0053eef587ebdc88d8bafbf09b2f214737abd539"
SOURCE_CORRECTION_1 = "19239aa3b00c8d7e32b329a2addae8391c8662a8"
PRIOR_FROZEN = 1240
INHERITED_NEGATIVES = 8212
INHERITED_OPEN_GAPS = 63
INHERITED_EXACT_GATES = 64
PRIMARY_FOCUS = "THOS Body"
BOUNDED_PRACTICE = (
    "freshwater environmental-DNA sample accession, contamination controls, correction readback, "
    "accessible notice, workload control, and shift handover as a synthetic learning and design lens only"
)

OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]
SOURCE_STATUS_CLASSES = ["current", "stable", "draft", "watch"]
PROTECTED_GATES = [
    "empirical_data",
    "real_participants_or_operators",
    "professional_or_environmental_authority",
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
            "Emit a zero-row refusal receipt with zero query, download, ingest, fit, likelihood, posterior, "
            "constraint, prediction, or empirical promotion."
        )
    elif disposition == "exact_gate":
        approval = "exact_affected_party_competent_and_maori_authority_required"
        lane = "x2_reservation_matrix_only"
        gate = (
            "Emit unresolved decision rights and reservations only; make no collection, access, disclosure, "
            "remedy, legal, cultural, data-governance, affected-party, or Maori-authority decision."
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
        "proposal_id": f"V6523-P{number:02d}",
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
        "novelty_against_1240_frozen_proposals": novelty,
    }


PROPOSALS = [
    _proposal(1, "BigTIFF byte order, magic, eight-byte offset size, IFD8 count, LONG8, SLONG8, IFD8 value, strip bounds, cycle, budget, and refusal tribunal", "bigtiff-ifd8", "THOS Body", "completed", ["SRC-BIGTIFF"], "BigTIFF 64-bit directory refusal", "Classic TIFF work does not isolate version 43, eight-byte offsets, IFD8 entry counts, LONG8 or SLONG8 values, and the reserved-header refusal contract."),
    _proposal(2, "glTF GLB magic, version, total length, JSON chunk, BIN chunk, bufferView, accessor, alignment, sparse accessor, external URI, budget, and refusal tribunal", "gltf-glb", "THOS Body", "completed", ["SRC-GLTF"], "glTF binary envelope refusal", "No frozen title isolates GLB chunk order with JSON/BIN ownership, bufferView-accessor arithmetic, sparse accessors, external URI refusal, and byte budgets."),
    _proposal(3, "SquashFS superblock, compression id, metadata block, inode table, directory table, fragment table, export table, xattr, duplicate id, decompression budget, and refusal tribunal", "squashfs-metadata", "THOS Body", "completed", ["SRC-SQUASHFS"], "SquashFS metadata refusal", "Earlier filesystem work does not isolate SquashFS compressed metadata blocks, fragment and export tables, xattr lookup, duplicate identifiers, and decompression limits."),
    _proposal(4, "CoAP version, type, token length, code, message id, option delta, option length, payload marker, Block1, Block2, retransmission budget, and refusal tribunal", "coap-message", "THOS Body", "completed", ["SRC-RFC7252", "SRC-RFC7959"], "CoAP message and blockwise refusal", "No frozen proposal isolates CoAP token-length bounds, option delta-length expansion, payload markers, blockwise sequencing, and retransmission budgets."),
    _proposal(5, "XAR header, table-of-contents length, compressed XML, checksum algorithm, file offset, extent length, encoding, duplicate path, traversal, budget, and refusal tribunal", "xar-toc", "THOS Body", "completed", ["SRC-XAR"], "XAR table-of-contents refusal", "Generic archive work does not isolate XAR's compressed XML table of contents, heap extents, checksum style, path duplication, and traversal refusal."),
    _proposal(6, "7z signature header, start-header CRC, next-header offset, next-header size, next-header CRC, streams info, coder graph, solid block, extraction budget, and refusal tribunal", "sevenzip-header", "THOS Body", "completed", ["SRC-7ZIP"], "7z stream-graph refusal", "ZIP work does not isolate 7z start and next-header CRCs, streams-info coder graphs, solid blocks, and bounded extraction."),
    _proposal(7, "NumPy NPY magic, major version, header length, Python-literal dictionary, descr, Fortran order, shape, dtype endian, payload size, object refusal, and budget tribunal", "numpy-npy", "THOS Body", "completed", ["SRC-NPY-CURRENT", "SRC-NPY-NEP"], "NumPy NPY structural refusal", "Tensor-envelope work does not isolate NPY versioned header lengths, literal-dictionary parsing, Fortran ordering, dtype endianness, object-array refusal, and exact payload arithmetic."),
    _proposal(8, "LMDB meta page, transaction id, root page, freelist page, branch node, leaf node, overflow page, duplicate sort, page bounds, map size, and refusal tribunal", "lmdb-pages", "THOS Body", "completed", ["SRC-LMDB"], "LMDB page-graph refusal", "Database journaling work does not isolate LMDB dual meta pages, transaction ordering, branch/leaf/overflow roles, duplicate sorting, map-size bounds, and freelist linkage."),
    _proposal(9, "DDS texture magic, header size, pixel format, FourCC, width, height, mipmap count, array size, DX10 header, surface byte arithmetic, budget, and refusal tribunal", "dds-texture", "THOS Body", "completed", ["SRC-DDS"], "DDS texture-envelope refusal", "Image work does not isolate DDS legacy and DX10 headers, FourCC/pixel-format obligations, mip and array cardinality, and surface byte arithmetic."),
    _proposal(10, "JPEG XL signature, container box length, codestream box, level, dimensions, colour encoding, animation timing, preview, metadata, resource budget, and refusal tribunal", "jpeg-xl-container", "THOS Body", "completed", ["SRC-JPEGXL"], "JPEG XL container refusal", "No frozen title isolates JPEG XL signature/container boxes, codestream ownership, level and dimension duties, animation timing, previews, and metadata budgets."),
    _proposal(11, "KTX 2 identifier, header, level index, data-format descriptor, key-value data, supercompression global data, vkFormat, face and layer count, offset overlap, budget, and refusal tribunal", "ktx2-texture", "THOS Body", "completed", ["SRC-KTX2"], "KTX 2 texture-envelope refusal", "No frozen proposal isolates KTX 2 level indexes, data-format descriptors, key-value data, supercompression global data, face/layer cardinality, and overlap refusal."),
    _proposal(12, "GRIB2 indicator section, discipline, edition, total length, identification, grid definition, product definition, data representation, bitmap, end marker, budget, and refusal tribunal", "grib2-sections", "THOS Body", "completed", ["SRC-WMO-GRIB2"], "GRIB2 section-order refusal", "Meteorological schema work does not isolate GRIB2 edition-two section ordering, grid/product/data templates, bitmap presence, end markers, and message budgets."),
    _proposal(13, "PDF linearization dictionary, first-page object, hint stream, xref boundary, object offset, length, incremental update, duplicate key, byte range, budget, and refusal tribunal", "pdf-linearization", "THOS Body", "completed", ["SRC-QPDF-LINEAR"], "PDF linearization refusal", "Prior PDF incremental-update work does not isolate the first-page linearization dictionary, hint stream ranges, object ordering, byte offsets, and linearized/incremental interaction."),
    _proposal(14, "GMUT Fermi normal coordinate geodesic, orthonormal tetrad, proper time, spatial exponential map, curvature expansion, domain, caustic, sign, unit, EFT, and observation-firewall board", "fermi-normal", "GMUT Mind", "completed", ["SRC-FERMI"], "Fermi-normal coordinate obligations", "No frozen board isolates a base geodesic, transported tetrad, proper-time chart, curvature expansion, normal-neighbourhood boundary, caustics, and observation refusal."),
    _proposal(15, "GMUT Synge world function geodesic interval, coincidence limit, bitensor derivative, Van Vleck determinant, convex normal neighbourhood, sign, unit, EFT, and observation-firewall board", "synge-world-function", "GMUT Mind", "completed", ["SRC-SYNGE"], "Synge world-function obligations", "No inherited proposal isolates the two-point interval, coincidence limits, bitensor derivatives, Van Vleck determinant, convex-normal-neighbourhood domain, and observation firewall."),
    _proposal(16, "GMUT DeWitt supermetric superspace, lapse, shift, three-metric, signature parameter, constraint, gauge, degeneracy, unit, EFT, and observation-firewall board", "dewitt-supermetric", "GMUT Mind", "completed", ["SRC-DEWITT"], "DeWitt supermetric obligations", "No frozen title isolates the metric on superspace, lapse/shift split, signature parameter, constraint surface, degeneracy, and observation refusal."),
    _proposal(17, "GMUT Cartan tetrad coframe, spin connection, torsion two-form, curvature two-form, local Lorentz gauge, orientation, boundary, unit, EFT, and observation-firewall board", "cartan-tetrad", "GMUT Mind", "completed", ["SRC-CARTAN"], "Cartan tetrad and connection obligations", "Metric-affine work does not isolate coframes, spin connections, Cartan two-form equations, local Lorentz gauge, orientation, boundary, and observation refusal together."),
    _proposal(18, "GMUT Bel-Robinson tensor Weyl curvature, dual, symmetry, trace, divergence, timelike contraction, superenergy dimension, causal domain, unit, EFT, and observation-firewall board", "bel-robinson", "GMUT Mind", "completed", ["SRC-BEL-ROBINSON"], "Bel-Robinson superenergy obligations", "No frozen proposal isolates the Bel-Robinson Weyl/dual construction, symmetry, trace and divergence duties, timelike contraction, dimensions, and observation firewall."),
    _proposal(19, "Stage 20 Fisher exact test contingency table, fixed margins, hypergeometric tail, two-sided ordering, sparse cell, multiplicity, interpretation, and nonpromotion board", "fisher-exact", "Trinity Mandala bridge", "completed", ["SRC-FISHER"], "Fisher-exact nonpromotion", "No inherited Stage 20 board isolates fixed margins, hypergeometric tail ordering, two-sided conventions, sparse cells, multiplicity, and interpretation limits."),
    _proposal(20, "Stage 20 Hodges-Lehmann estimator pairwise difference, pseudomedian, confidence interval, ties, missingness, multiplicity, interpretation, and nonpromotion board", "hodges-lehmann", "Trinity Mandala bridge", "completed", ["SRC-HODGES-LEHMANN"], "Hodges-Lehmann nonpromotion", "No frozen board isolates the pairwise-difference estimator, pseudomedian distinction, inversion interval, ties, missingness, multiplicity, and causal refusal."),
    _proposal(21, "Accessible faceted search group label, checkbox state, result count, active-filter summary, clear action, live result status, focus return, keyboard order, noncolour state, and manual-evaluation structural audit", "accessible-faceted-search", "THOS Body", "completed", ["SRC-WCAG22", "SRC-WAI-APG"], "accessible faceted-search structure", "Earlier sort, filter, and graph audits do not isolate faceted group labels, active-filter summaries, result-count announcements, clear actions, and focus return as one surface."),
    _proposal(22, "Thermo-Psyche Poynting correction fugacity, pressure integral, partial molar volume, reference pressure, liquid approximation, sign, unit, uncertainty, domain, and agency-nonconversion classifier", "poynting-correction", "Trinity Mandala bridge", "completed", ["SRC-POYNTING"], "Poynting-correction agency nonconversion", "No frozen nonconversion surface isolates pressure-integrated partial molar volume, reference pressure, liquid approximation, uncertainty, and refusal of agency conversion."),
    _proposal(23, "DICOMweb WADO-RS multipart boundary, media type, transfer syntax, bulk-data URI, content location, instance identity, duplicate part, byte budget, privacy, and refusal tribunal", "dicomweb-wado", "THOS Body", "completed", ["SRC-DICOMWEB"], "DICOMweb response-envelope refusal", "MIME and DICOM-file work does not isolate WADO-RS resource identity, transfer-syntax parameters, BulkDataURI linkage, multipart content locations, and privacy refusal."),
    _proposal(24, "THOS freshwater eDNA sample accession, collection site code, field blank, negative control, contamination flag, chain of custody, correction readback, workload, and shift-handover proxy", "edna-sample-handover", "THOS Body", "represented", ["SRC-MFE-EDNA"], "freshwater eDNA sample handover", "Earlier drinking-water and archaeological handovers do not isolate eDNA field blanks, negative controls, contamination flags, collection-site coding, and laboratory accession."),
    _proposal(25, "THOS freshwater eDNA taxonomic assignment disagreement, detection threshold, batch contamination, fatigue, harm stop, missingness, escalation, readback, workload budget, and handover proxy", "edna-assignment-latency", "THOS Body", "represented", ["SRC-MFE-EDNA"], "freshwater eDNA assignment proxy", "No frozen THOS proxy binds eDNA taxonomic disagreement, detection thresholds, batch contamination, missingness, fatigue, harm stops, escalation, and readback."),
    _proposal(26, "Freed ID OpenSSH certificate nonce, public key, serial, type, key id, principals, validity interval, critical option, extension, signature key, privacy, and nonproduction profile", "openssh-certificate", "Freed ID and CBR Heart", "represented", ["SRC-OPENSSH-CERT"], "OpenSSH certificate profile", "No frozen identity profile isolates OpenSSH certificate serial/type, principals, critical options, extensions, signature key, and validity intervals."),
    _proposal(27, "Freed ID SAML metadata entity, role descriptor, key descriptor, endpoint, binding, entity category, validity, cache duration, signature, privacy, and nonproduction profile", "saml-metadata", "Freed ID and CBR Heart", "represented", ["SRC-SAML-METADATA"], "SAML metadata profile", "Earlier SAML assertion or federation work does not isolate metadata entity/role descriptors, endpoint bindings, cache duration, entity categories, and signature boundaries."),
    _proposal(28, "Freed ID X.509 attribute certificate holder, issuer, signature, serial, validity, attributes, issuer unique id, extensions, targeting, revocation, privacy, and nonproduction profile", "x509-attribute-certificate", "Freed ID and CBR Heart", "represented", ["SRC-RFC5755"], "X.509 attribute-certificate profile", "Delegated and public-key certificate work does not isolate an attribute certificate's holder, issuer, authorization attributes, targeting, revocation, and privacy boundaries."),
    _proposal(29, "GMUT Hyper Suprime-Cam PDR3 catalogue object, tract, patch, band, photometry, mask, point-spread function, selection, covariance, provenance, checksum, and zero-row likelihood-refusal adapter", "hsc-pdr3-zero-row", "GMUT Mind", "open_gap", ["SRC-HSC-PDR3", "SRC-HSC-PDR3-DB"], "HSC PDR3 likelihood readiness", "No inherited zero-row adapter targets the official HSC PDR3 tract/patch catalogue and database with band, PSF, mask, selection, covariance, and checksum duties."),
    _proposal(30, "CBR freshwater eDNA collection location, sensitive species, raw sequence, access, public notice, privacy, remedy, affected-party legitimacy, legal and cultural limits, data governance, and Maori-authority reservation", "edna-authority", "Freed ID and CBR Heart", "exact_gate", ["SRC-MFE-EDNA", "SRC-MFE-FRESHWATER", "SRC-PRIVACY-NZ"], "freshwater eDNA authority reservation", "No frozen exact-gate surface combines eDNA collection locations, sensitive species, raw sequences, access, notice, privacy, remedy, affected-party legitimacy, and Maori data-governance authority."),
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
    _source("SRC-BIGTIFF", "current", "official_project_specification", "LibTIFF BigTIFF design", "https://libtiff.gitlab.io/libtiff/specification/bigtiff.html", "Supports synthetic version-43 and IFD8 fixtures only."),
    _source("SRC-GLTF", "current", "official_industry_specification", "glTF 2.0 specification", "https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html", "Supports disposable GLB structures only."),
    _source("SRC-SQUASHFS", "current", "official_kernel_documentation", "SquashFS 4.0 filesystem", "https://docs.kernel.org/filesystems/squashfs.html", "Supports synthetic filesystem tables only; no mount occurs."),
    _source("SRC-RFC7252", "stable", "official_standard", "RFC 7252 Constrained Application Protocol", "https://www.rfc-editor.org/rfc/rfc7252.html", "Supports nonnetwork CoAP vectors only."),
    _source("SRC-RFC7959", "stable", "official_standard", "RFC 7959 Block-Wise Transfers in CoAP", "https://www.rfc-editor.org/rfc/rfc7959.html", "Supports synthetic blockwise fields only."),
    _source("SRC-XAR", "watch", "project_source_and_format", "eXtensible ARchiver source", "https://github.com/mackyle/xar", "Supplies watched legacy XAR structures only; no installation or production claim."),
    _source("SRC-7ZIP", "stable", "official_project_specification", "7z format description", "https://www.7-zip.org/7z.html", "Supports synthetic archive headers only."),
    _source("SRC-NPY-CURRENT", "current", "official_project_documentation", "NumPy NPY format", "https://numpy.org/doc/stable/reference/generated/numpy.lib.format.html", "Supports bounded NPY byte fixtures only."),
    _source("SRC-NPY-NEP", "draft", "official_project_proposal", "A simple file format for NumPy arrays", "https://numpy.org/neps/nep-0001-npy-format.html", "Historical draft context is subordinate to current NumPy documentation."),
    _source("SRC-LMDB", "stable", "official_project_source", "Lightning Memory-Mapped Database", "https://git.openldap.org/openldap/openldap/-/tree/mdb.master/libraries/liblmdb", "Supports disposable page graphs only; no live database."),
    _source("SRC-DDS", "current", "official_platform_documentation", "DirectDraw Surface format", "https://learn.microsoft.com/en-us/windows/win32/direct3ddds/dx-graphics-dds", "Supports synthetic texture envelopes only."),
    _source("SRC-JPEGXL", "current", "official_standards_body_overview", "JPEG XL image coding system", "https://jpeg.org/jpegxl/", "Supports bounded container requirements only."),
    _source("SRC-KTX2", "current", "official_industry_specification", "KTX file format specification 2.0", "https://registry.khronos.org/KTX/specs/2.0/ktxspec.v2.html", "Supports synthetic KTX2 structures only."),
    _source("SRC-WMO-GRIB2", "current", "official_intergovernmental_standard", "WMO Manual on Codes Volume I.2", "https://community.wmo.int/site/knowledge-hub/programmes-and-initiatives/wmo-information-system-wis/about-manual-codes-volume-i2", "Supports synthetic GRIB2 sections only."),
    _source("SRC-QPDF-LINEAR", "current", "official_project_documentation", "QPDF linearization", "https://qpdf.readthedocs.io/en/stable/linearization.html", "Supports bounded linearization fixtures only; no general PDF assurance."),
    _source("SRC-FERMI", "stable", "primary_research", "Fermi normal coordinates and some basic concepts in differential geometry", "https://doi.org/10.1063/1.1724316", "Supports formal coordinate-domain vocabulary only."),
    _source("SRC-SYNGE", "stable", "primary_research_review", "Synge's world function and the quantum spacetime", "https://arxiv.org/abs/2304.01995", "Supports formal bitensor vocabulary only."),
    _source("SRC-DEWITT", "stable", "primary_research", "Quantum theory of gravity I: the canonical theory", "https://doi.org/10.1103/PhysRev.160.1113", "Supports formal superspace vocabulary only."),
    _source("SRC-CARTAN", "stable", "primary_mathematical_reference", "On manifolds with an affine connection and the theory of general relativity", "https://doi.org/10.1007/978-1-4612-2904-6_15", "Supports Cartan connection vocabulary only."),
    _source("SRC-BEL-ROBINSON", "stable", "primary_research_review", "The Bel-Robinson tensor and its applications", "https://arxiv.org/abs/gr-qc/9906087", "Supports formal tensor duties only."),
    _source("SRC-FISHER", "stable", "primary_statistical_reference", "Statistical methods for research workers", "https://psychclassics.yorku.ca/Fisher/Methods/", "Supports exact-test vocabulary only; no participant inference."),
    _source("SRC-HODGES-LEHMANN", "stable", "primary_research", "Estimates of location based on rank tests", "https://doi.org/10.1214/aoms/1177704172", "Supports estimator vocabulary only."),
    _source("SRC-WCAG22", "stable", "official_accessibility_standard", "Web Content Accessibility Guidelines 2.2", "https://www.w3.org/TR/WCAG22/", "Supports structural checks; complete conformance remains reserved."),
    _source("SRC-WAI-APG", "current", "official_accessibility_guidance", "WAI-ARIA Authoring Practices Guide", "https://www.w3.org/WAI/ARIA/apg/", "Supports keyboard, name, state, and status structure only."),
    _source("SRC-POYNTING", "stable", "official_terminology", "IUPAC Gold Book Poynting correction", "https://goldbook.iupac.org/terms/view/P04718", "Supports thermodynamic vocabulary only; agency conversion is refused."),
    _source("SRC-DICOMWEB", "current", "official_health_informatics_standard", "DICOM PS3.18 Web Services", "https://dicom.nema.org/medical/dicom/current/output/html/part18.html", "Supports synthetic WADO-RS envelopes only; no patient or clinical data."),
    _source("SRC-MFE-EDNA", "current", "official_government_research_report", "Environmental DNA indicators for the National Objectives Framework", "https://environment.govt.nz/publications/environmental-dna-indicators-for-supporting-implementation-of-the-national-objectives-framework-nof-in-the-nps-fm/", "Supplies freshwater eDNA context only; no operational or authority decision."),
    _source("SRC-OPENSSH-CERT", "current", "official_project_protocol", "OpenSSH certificate key protocol", "https://github.com/openssh/openssh-portable/blob/master/PROTOCOL.certkeys", "Supports synthetic certificate fields only; no real key or principal."),
    _source("SRC-SAML-METADATA", "stable", "official_standard", "Metadata for SAML V2.0", "https://docs.oasis-open.org/security/saml/v2.0/saml-metadata-2.0-os.pdf", "Supports synthetic metadata elements only."),
    _source("SRC-RFC5755", "stable", "official_standard", "RFC 5755 Internet Attribute Certificate Profile", "https://www.rfc-editor.org/rfc/rfc5755.html", "Supports synthetic attribute-certificate vectors only."),
    _source("SRC-HSC-PDR3", "watch", "official_data_release", "Hyper Suprime-Cam Public Data Release 3", "https://hsc-release.mtk.nao.ac.jp/doc/index.php/sample-page/pdr3/", "Supports a zero-row readiness contract only; no query or download occurs."),
    _source("SRC-HSC-PDR3-DB", "watch", "official_data_service_documentation", "Hyper Suprime-Cam PDR3 database", "https://hsc-release.mtk.nao.ac.jp/doc/index.php/database__pdr3/", "Supplies schema and provenance context only; no observation."),
    _source("SRC-MFE-FRESHWATER", "current", "official_government_environment_report", "Our Freshwater 2026", "https://environment.govt.nz/publications/our-freshwater-2026/", "Keeps environmental interpretation and Maori knowledge external to software."),
    _source("SRC-PRIVACY-NZ", "current", "official_legislation", "Privacy Act 2020", "https://www.legislation.govt.nz/act/public/2020/0031/latest/whole.html", "Keeps privacy interpretation, disclosure, and remedy exact-gated."),
]


X1_OPERATIONAL_NEGATIVES = [
    {"negative_id": "V6523-X1-N01", "category": "startup_path_probe_timeout", "failed": "A two-candidate Test-Path startup wrapper exceeded its bounded wait and returned no attributable result.", "recovery": "Probe the required exact paths directly and independently.", "passing": "The required skill and repository paths resolved.", "recurrence_guard": "Use one exact path per startup probe."},
    {"negative_id": "V6523-X1-N02", "category": "baton_chunk_broken_pipe", "failed": "A git-show producer received a broken pipe when Select-Object stopped after the first baton chunk.", "recovery": "Materialize the exact commit blob into an in-memory line array and slice that array.", "passing": "All 740 records were read through EOF.", "recurrence_guard": "Do not truncate a live Git producer when complete-file evidence is required."},
    {"negative_id": "V6523-X1-N03", "category": "method_schema_filename_assumption", "failed": "A startup read guessed a nonexistent Method Flow schema filename.", "recovery": "Follow the exact reference named by the selected skill.", "passing": "references/schema.md was read completely.", "recurrence_guard": "Resolve skill-linked references verbatim."},
    {"negative_id": "V6523-X1-N04", "category": "workflow_enum_assumption", "failed": "The first workflow-plan request used an unsupported cross-platform enum and failed one policy check.", "recovery": "Use the runner-supported user-mediated relay enum while separately prohibiting live-phase cross-platform action.", "passing": "The refined plan passed all 20 policy checks with eight intentional placeholder warnings.", "recurrence_guard": "Validate policy enums against the current runner schema."},
    {"negative_id": "V6523-X1-N05", "category": "fast_forward_verbose_output", "failed": "The successful fast-forward emitted an overlarge inherited change listing that was truncated by the wrapper.", "recovery": "Do not repeat the mutation; verify branch, exact head, and clean state with scalar postconditions.", "passing": "The Tamar lane was exact, clean, pushed, and four-way equal.", "recurrence_guard": "Suppress or bound fast-forward summaries in large inherited histories."},
    {"negative_id": "V6523-X1-N06", "category": "overbroad_keyword_audit", "failed": "A forty-term novelty probe emitted samples as well as counts and exceeded useful response context.", "recovery": "Emit counts only, then inspect bounded samples for selected or colliding terms.", "passing": "The bounded audit isolated viable unused mechanisms.", "recurrence_guard": "Separate discovery counts from sample inspection."},
    {"negative_id": "V6523-X1-N07", "category": "powershell_foreach_pipeline", "failed": "A PowerShell foreach expression was piped without an enclosing array and failed before execution.", "recovery": "Assign the foreach results to an array before JSON serialization.", "passing": "The bounded term-count table completed.", "recurrence_guard": "Materialize foreach output before a trailing pipeline."},
    {"negative_id": "V6523-X1-N08", "category": "python_tuple_tie_comparison", "failed": "A novelty probe used max on score-and-dictionary tuples and a tied score attempted to compare dictionaries.", "recovery": "Select the maximum with an explicit score key.", "passing": "All thirty nearest neighbours were computed; the accepted packet maximum was 0.407407.", "recurrence_guard": "Never rely on nonorderable payloads as tuple tie-breakers."},
    {"negative_id": "V6523-X1-N09", "category": "method_request_utf8_bom", "failed": "PowerShell Set-Content emitted a UTF-8 BOM that the Method Flow runner's strict UTF-8 JSON reader rejected.", "recovery": "Write temporary runner request JSON with an explicit UTF-8 encoding that emits no BOM.", "passing": "The Method Flow requests parsed and the additive ledger validated.", "recurrence_guard": "Use explicit no-BOM UTF-8 for strict JSON runner inputs."},
    {"negative_id": "V6523-X1-N10", "category": "powershell_json_array_wrapper", "failed": "An array-subexpression wrapped the parsed Method Flow negative array as one aggregate record instead of nine independent methods.", "recovery": "Index the parsed object array directly and emit one method plus two witnesses per negative.", "passing": "Every retained negative received its own failed witness, passing recovery witness, and preferred bounded method.", "recurrence_guard": "Inspect parsed-array cardinality before batch Method Flow ingestion."},
]


SAFE_TASKS = [
    "Verify all six named Orin lifecycle anchors and five-commit zero-merge lineage.",
    "Verify Tamar fast-forward provenance and four-way equality without source mutation.",
    "Preserve all 8,212 inherited effective negatives before adding Tamar failures.",
    "Replay all eight inherited manifest contracts from immutable Git blobs.",
    "Audit current, stable, draft, and watch source statuses.",
    "Compute token-Jaccard neighbours across all 1,240 frozen titles.",
    "Record manual mechanism distinctions and rejected near-collisions.",
    "Protect every x1 path with an exact staged allowlist.",
    "Seal x1 content in the Git path-filtered blob domain.",
    "Parse every phase JSON document with explicit UTF-8.",
    "Separate scanner definitions, candidates, and confirmed payload hits.",
    "Declare working-byte and Git-blob hash domains without conflation.",
    "Measure inherited checkout and Tamar-generated file footprints separately.",
    "Hold the terminal route before exact-final proof.",
    "Emit workload metadata without emotion, health, or consciousness claims.",
    "Record environment versions without updating desktop applications.",
    "Verify eight future CLI seats remain unnamed, uncreated, and unlaunched.",
    "Enforce declared x1, x2, and total commit caps.",
    "Verify zero merges and one-parent lifecycle commits.",
    "Require one successful canonical bounded final pass and no replay.",
    "Review stale lifecycle labels after additive ledger changes.",
    "Lint scientific, identity, production, professional, legal, and cultural boundaries.",
    "Enforce the four-value core outcome vocabulary.",
    "Keep inherited exact-approval and blocked packets visible and unexecuted.",
    "Separate official citations from observations and authority.",
    "Keep HSC query, row, likelihood, posterior, and constraint counts at zero.",
    "Keep identity profiles synthetic with zero real keys, accounts, or exchanges.",
    "Keep THOS proxies at zero real people, samples, operations, or outcomes.",
    "Reserve manual, browser, assistive-technology, Maori-language, and affected-user evaluation.",
    "Keep every Method Flow failure linked to its bounded recovery witness.",
]

CANDIDATE_TASKS = [f"Build and bounded-test {proposal['mission_surface']}." for proposal in PROPOSALS]

SKILL_IDEAS = [
    "ghc-family-binary-media-envelope-tribunals",
    "ghc-family-filesystem-database-refusal",
    "ghc-family-network-archive-refusal",
    "ghc-family-gmut-local-bitensor-boards",
    "ghc-family-gmut-superspace-tetrad-boards",
    "ghc-family-gmut-superenergy-board",
    "ghc-family-edna-handover-proxy",
    "ghc-family-federated-certificate-boundary",
    "ghc-family-accessible-faceted-search",
    "ghc-family-stage20-exact-rank-nonpromotion",
]

RUNNER_IDEAS = [
    "ghc_family_binary_media_tribunals.py",
    "ghc_family_filesystem_database_tribunals.py",
    "ghc_family_network_archive_tribunals.py",
    "ghc_family_gmut_local_bitensor_boards.py",
    "ghc_family_gmut_superspace_tetrad_boards.py",
    "ghc_family_gmut_superenergy_board.py",
    "ghc_family_edna_proxy.py",
    "ghc_family_federated_certificate_profiles.py",
    "ghc_family_accessibility_thermo_stage20.py",
    "ghc_family_v652_v3_detailed_validator.py",
]

CLEAN_TASKS = [
    "Replace multi-path startup probes with exact independently attributable reads.",
    "Replace live-producer baton truncation with in-memory exact-blob slicing.",
    "Replace guessed Method Flow reference names with skill-linked exact paths.",
    "Normalize workflow policy enums through the current refinement schema.",
    "Suppress overlarge fast-forward summaries and verify scalar postconditions.",
    "Split novelty discovery counts from sample inspection.",
    "Materialize PowerShell foreach output before serialization.",
    "Use explicit score keys for novelty-neighbour selection.",
    "Reconcile count-dependent truth mirrors after every retained failure.",
    "Normalize generated text through the declared Git-blob hash domain.",
    "Separate privacy scanner definitions from payload findings.",
    "Preserve unresolved privacy candidates until explicit adjudication.",
    "Use exact eligible-test arithmetic rather than raw discovery cardinality.",
    "Verify family-current caller collisions before adding wrappers.",
    "Preserve historical tools as compatibility surfaces.",
    "Rebuild accessible output while retaining manual-evaluation reservations.",
    "Check every ordinary phase document against the 20,000-word cap.",
    "Check Tamar-generated growth against the 15,000-file threshold.",
    "Refresh the phase-scoped GHC Family Index after tools exist.",
    "Refresh Reflection Remaster recommendations after tools exist.",
    "Refresh workflow refinement without activating future placeholders.",
    "Validate Method Flow after every new witness.",
    "Keep failed witnesses append-only and linked to negatives.",
    "Remove no memory, identity, source, negative, or sibling record.",
    "Delete no user or sibling material during cleanup.",
    "Keep Sandbox and Hyper-V states unchanged.",
    "Keep desktop applications and host-security state unchanged.",
    "Keep empirical, participant, production-identity, and authority counters at zero.",
    "Verify all 150 synthetic mutations retain reject-or-quarantine outcomes.",
    "Keep terminal routing prepared and unsent until every exact-final gate passes.",
]

REJECTED_COLLISIONS = [
    {"candidate": "Noether-Wald charge board", "reason": "It duplicates the frozen Iyer-Wald covariant phase-space mechanism; replaced by Bel-Robinson tensor obligations."},
    {"candidate": "accessible structured diff viewer", "reason": "It duplicates a frozen insertion/deletion diff audit; replaced by faceted-search state and result-status structure."},
    {"candidate": "Tolman temperature nonconversion", "reason": "The Tolman-Ehrenfest classifier is already frozen; replaced by the Poynting correction."},
    {"candidate": "OAuth DPoP profile", "reason": "A DPoP nonce and replay-cache profile is already frozen; replaced by X.509 attribute certificates."},
    {"candidate": "WebP animation tribunal", "reason": "A WebP VP8X and animation tribunal is already frozen; replaced by DDS texture envelopes."},
    {"candidate": "GNU tar sparse tribunal", "reason": "A PAX sparse-map tribunal is already frozen; replaced by LMDB page graphs."},
    {"candidate": "RIFF WAVE tribunal", "reason": "A Broadcast Wave RIFF tribunal is already frozen; replaced by GRIB2 section ordering."},
    {"candidate": "drinking-water chain-of-custody proxy", "reason": "A drinking-water laboratory chain proxy is already frozen; replaced by freshwater eDNA accession and contamination controls."},
]
