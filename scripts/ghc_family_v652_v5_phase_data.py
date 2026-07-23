#!/usr/bin/env python3
"""Frozen Eiren Kestrel v652-v5 x1 data; this module contains no x2 observations."""

from __future__ import annotations


PHASE = "v652-v5"
OWNER = "Eiren Kestrel"
PRONOUNS = "she/they"
ROLE = "relational evidence-boundary integrator"
HOPE = "make each advance useful without letting confidence outrun evidence"
BRANCH = "codex/GHC-Family/eiren-kestrel-v648-v3-3-full-tools"
PHASE_ROOT = "docs/eiren-kestrel/v652-v5"

SOURCE_BRANCH = "codex/GHC-Family/sylven-arc-v642-v8-full-tools"
SOURCE_HEAD = "3a77dacd759a499ffe94cbc281a3d7b343608e2d"
SOURCE_ORIGIN = "09140173409bc4198f3c9e30162b9bcef8a3895b"
SOURCE_X1 = "19a442b69da03da6cfaa78d3182ce182a29eda78"
SOURCE_EVIDENCE = "925be6fb40bcb12ff7fe6636f4f19dfa25ae3071"
PRIOR_FROZEN = 1300
INHERITED_NEGATIVES = 8549
INHERITED_OPEN_GAPS = 65
INHERITED_EXACT_GATES = 66
PRIMARY_FOCUS = "Freed ID and CBR Heart"
BOUNDED_PRACTICE = (
    "meteorological observing-station calibration, observation-quality review, suspect-data quarantine, "
    "severe-weather escalation, accessible quality notice, workload control, correction readback, and shift handover"
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
        "proposal_id": f"V6525-P{number:02d}",
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
        "novelty_against_1300_frozen_proposals": novelty,
    }


PROPOSALS = [
    _proposal(1, "ASN.1 BER, CER, and DER identifier octet, tag number, length form, primitive or constructed value, indefinite length, end-of-contents, canonical ordering, size budget, nesting budget, and refusal tribunal", "asn1-x690-ber-cer-der", "THOS Body", "completed", ["SRC-X690"], "ASN.1 BER, CER, and DER refusal", "The inherited DER-only tribunal does not cover BER and CER indefinite-length, constructed-value, end-of-contents, and canonical-encoding distinctions together."),
    _proposal(2, "AVIF 1.2 ISO Base Media File Format box, brands, meta, item location, item properties, image item, alpha auxiliary image, grid, sequence, extent budget, and refusal tribunal", "avif12-isobmff", "THOS Body", "completed", ["SRC-AVIF12"], "AVIF 1.2 item-graph refusal", "No frozen title isolates AVIF 1.2 item locations and properties, alpha auxiliary images, grids, sequences, brand constraints, and extent ownership."),
    _proposal(3, "lzip member header, dictionary size, LZMA stream, trailer CRC, uncompressed size, member size, concatenation, trailing data, output budget, and refusal tribunal", "lzip-member", "THOS Body", "completed", ["SRC-LZIP"], "lzip member refusal", "Existing compression tribunals do not isolate lzip dictionary coding, LZMA member ownership, trailer CRC, uncompressed and member sizes, concatenation, and trailing-data policy."),
    _proposal(4, "SPIR-V module magic, version, generator, bound, schema, instruction word count, opcode, id definition, capability, memory model, control-flow, and refusal tribunal", "spirv-module", "THOS Body", "completed", ["SRC-SPIRV"], "SPIR-V module refusal", "No inherited mechanism isolates SPIR-V word-count framing, result-id bounds, capabilities, memory model, and structured control-flow obligations."),
    _proposal(5, "LLVM bitcode wrapper, magic, offset, size, bitstream block, abbreviation, record, VBR width, nesting, alignment, resource budget, and refusal tribunal", "llvm-bitcode", "THOS Body", "completed", ["SRC-LLVM-BITCODE"], "LLVM bitcode refusal", "No frozen tribunal isolates LLVM wrapper offsets, bitstream block abbreviations, variable-bit-rate fields, record ownership, alignment, and nesting budgets."),
    _proposal(6, "FlatBuffers root offset, table, vtable, field offset, vector length, string terminator, union discriminator, alignment, bounds, recursion budget, and refusal tribunal", "flatbuffers-wire", "THOS Body", "completed", ["SRC-FLATBUFFERS"], "FlatBuffers wire refusal", "Protocol-buffer and generic offset work does not isolate FlatBuffers reverse vtables, relative offsets, vector and string ownership, unions, alignment, and recursion."),
    _proposal(7, "Apache Thrift Compact Protocol message, field delta, type nibble, zigzag integer, varint, collection, map, binary length, nesting, resource budget, and refusal tribunal", "thrift-compact", "THOS Body", "completed", ["SRC-THRIFT-COMPACT"], "Thrift Compact Protocol refusal", "No inherited title isolates Thrift Compact field-id deltas, compact type nibbles, zigzag integers, collection and map headers, and nesting budgets."),
    _proposal(8, "ESRI Shapefile main header, file length, shape type, record header, record length, index offset, DBF row relation, endianness, bounding box, multi-file consistency, and refusal tribunal", "esri-shapefile", "THOS Body", "completed", ["SRC-SHAPEFILE"], "ESRI Shapefile refusal", "No frozen mechanism binds the mixed-endian main and record headers to SHX offsets, DBF row relations, shape consistency, and cross-file bounds."),
    _proposal(9, "OGC GeoPackage 1.4 SQLite application id, user version, core table, geometry columns, spatial reference, extension, tile matrix, trigger, integrity, resource budget, and refusal tribunal", "geopackage14", "THOS Body", "completed", ["SRC-GPKG14"], "GeoPackage 1.4 refusal", "Existing SQLite and geospatial work does not isolate GeoPackage application identifiers, core metadata tables, geometry and tile relations, extensions, and integrity triggers."),
    _proposal(10, "ASPRS LAS 1.4 public header, version, point data offset, variable length record, extra bytes, point format, scale, offset, count, bounds, waveform, and refusal tribunal", "las14-point-cloud", "THOS Body", "completed", ["SRC-LAS14"], "LAS 1.4 point-cloud refusal", "No inherited tribunal isolates LAS public headers, variable-length metadata, point formats, scale and offset arithmetic, point counts, bounds, waveform references, and extra bytes."),
    _proposal(11, "RPM v4 and v6 lead, signature header, immutable region, main header, index entry, tag type, payload compressor, digest, size budget, path boundary, and refusal tribunal", "rpm-package", "THOS Body", "completed", ["SRC-RPM"], "RPM package refusal", "No frozen title isolates RPM lead compatibility, signature and immutable header regions, typed tag indexes, payload compressors, digests, and extraction boundaries."),
    _proposal(12, "FAT32 BIOS parameter block, reserved sectors, FAT count, cluster geometry, root cluster, FSInfo, FAT entry, cluster chain, long file name, directory entry, and refusal tribunal", "fat32-volume", "THOS Body", "completed", ["SRC-FAT32"], "FAT32 volume refusal", "No inherited mechanism isolates FAT32 BPB geometry, FSInfo hints, cluster-chain bounds, root cluster, paired FAT policy, directory entries, and long-file-name assembly."),
    _proposal(13, "GMUT Regge simplicial edge length, hinge deficit angle, dual volume, discrete curvature, Regge action, boundary, variation, triangulation, convergence reservation, unit, and observation-firewall board", "regge-calculus", "GMUT Mind", "completed", ["SRC-REGGE1961"], "Regge-calculus obligations", "Regge-Wheeler perturbations are unrelated; no frozen board isolates simplicial hinges, deficit angles, discrete action variation, triangulation dependence, and continuum-convergence reservation."),
    _proposal(14, "GMUT Ashtekar-Barbero connection, densitized triad, Barbero-Immirzi parameter, Gauss constraint, diffeomorphism constraint, Hamiltonian constraint, reality, orientation, boundary, unit, and observation-firewall board", "ashtekar-barbero", "GMUT Mind", "completed", ["SRC-BARBERO1995"], "Ashtekar-Barbero obligations", "The inherited Cartan and ADM surfaces do not isolate a real SU(2) connection, densitized triad, Immirzi parameter, and the three canonical constraint families."),
    _proposal(15, "GMUT Komar Killing field, antisymmetric derivative, two-surface integral, orientation, normalization, mass, angular momentum, matter correction, asymptotic condition, boundary, and observation-firewall board", "komar-charge", "GMUT Mind", "completed", ["SRC-KOMAR1959"], "Komar-charge obligations", "No frozen board isolates Killing-field surface integrals, normalization and orientation, mass versus angular-momentum factors, matter corrections, and asymptotic conditions."),
    _proposal(16, "GMUT Petrov Weyl tensor, self-dual bivector, principal null direction, algebraic multiplicity, invariant, degeneracy, type transition, tetrad dependence, domain, boundary, and observation-firewall board", "petrov-classification", "GMUT Mind", "completed", ["SRC-PETROV-REVIEW"], "Petrov-classification obligations", "No inherited board isolates algebraic Weyl types through principal-null-direction multiplicities, degeneracy and type transition while reserving coordinate, tetrad, and empirical claims."),
    _proposal(17, "GMUT geodesic-deviation tangent, separation vector, covariant acceleration, Riemann contraction, affine parameter, sign convention, conjugate point, Jacobi field, domain, unit, and observation-firewall board", "geodesic-deviation", "GMUT Mind", "completed", ["SRC-LEVI-CIVITA"], "geodesic-deviation obligations", "Existing geodesic and curvature boards do not isolate the Jacobi separation equation, sign convention, affine parameter, conjugate points, and its linear-neighbourhood domain."),
    _proposal(18, "Accessible session-timeout warning dialog name, countdown, timing adjustment, extend action, sign-in transition, focus, keyboard, status announcement, persistence, fallback, and manual-evaluation audit", "accessible-timeout-warning", "THOS Body", "completed", ["SRC-WCAG22-TIME", "SRC-WAI-DIALOG"], "accessible timeout-warning structure", "No frozen accessibility title isolates advance timeout warning, extension control, countdown announcements, focus ownership, sign-in transition, and timing-adjustment reservation."),
    _proposal(19, "Thermo-Psyche Maxwell-Stefan multicomponent chemical-potential gradient, mole fraction, diffusion velocity, reference frame, pair diffusivity, flux constraint, sign, unit, domain, and agency-nonconversion classifier", "maxwell-stefan", "Trinity Mandala bridge", "completed", ["SRC-IUPAC-DIFFUSION"], "Maxwell-Stefan agency nonconversion", "Prior diffusion work does not isolate multicomponent force-flux balance, pair diffusivities, reference-frame dependence, flux closure, and explicit refusal to convert transport into agency."),
    _proposal(20, "Stage 20 time-dependent ROC case and control definition, censoring, horizon, incident or cumulative convention, inverse-probability weighting, discrimination, uncertainty, missingness, interpretation, and nonpromotion board", "time-dependent-roc", "Trinity Mandala bridge", "completed", ["SRC-HEAGERTY2000"], "time-dependent ROC nonpromotion", "No frozen board isolates horizon-specific case and control definitions, censoring, incident versus cumulative conventions, and time-dependent discrimination."),
    _proposal(21, "Stage 20 partial AUC specificity interval, standardization, interpolation, paired comparison, sampling distribution, uncertainty, multiplicity, interpretation, and nonpromotion board", "partial-auc", "Trinity Mandala bridge", "completed", ["SRC-MCCLISH1989"], "partial-AUC nonpromotion", "DeLong and full-AUC work does not isolate a declared specificity interval, partial-area standardization, endpoint interpolation, and restricted operating-region interpretation."),
    _proposal(22, "Stage 20 Spiegelhalter calibration test predicted probability, binary outcome, standardized residual, variance, grouping refusal, calibration intercept or slope distinction, uncertainty, interpretation, and nonpromotion board", "spiegelhalter-calibration", "Trinity Mandala bridge", "completed", ["SRC-SPIEGELHALTER1986"], "Spiegelhalter calibration nonpromotion", "No inherited board isolates an ungrouped probability-calibration residual statistic and explicitly distinguishes it from calibration intercept, slope, and grouping-based tests."),
    _proposal(23, "Stage 20 net reclassification improvement event movement, nonevent movement, category threshold, category-free variant, denominator, optimism, uncertainty, clinical-utility distinction, interpretation, and nonpromotion board", "net-reclassification", "Trinity Mandala bridge", "completed", ["SRC-PENCINA2008"], "net-reclassification nonpromotion", "No frozen board isolates event and nonevent reclassification directions, category thresholds, category-free variants, optimism, and the distinction from clinical utility."),
    _proposal(24, "THOS meteorological observing-station siting record, instrument identity, calibration lineage, exposure, maintenance, timestamp, quality flag, workload, readback, and shift-handover proxy", "meteorological-station", "THOS Body", "represented", ["SRC-WMO-OBS"], "meteorological station proxy", "The optical-observatory weather proxy does not isolate meteorological station siting, instrument calibration lineage, exposure, maintenance, observation timestamp, and quality-control handover."),
    _proposal(25, "THOS synoptic observation encoding, station-pressure reduction, wind-gust averaging, precipitation trace, present-weather code, temporal consistency, suspect-data quarantine, correction version, accessible quality notice, workload, and handover proxy", "synoptic-observation-qc", "THOS Body", "represented", ["SRC-WMO-OBS"], "synoptic observation-quality proxy", "Prior warning-amendment work does not isolate observation encoding, pressure reduction, gust averaging, trace precipitation, present-weather coding, quarantine, and correction versioning."),
    _proposal(26, "Freed ID OpenID Connect RP-Initiated Logout id token hint, logout hint, client id, post-logout redirect, state, discovery, consent, replay, minimization, privacy, and nonproduction profile", "oidc-rp-logout", "Freed ID and CBR Heart", "represented", ["SRC-OIDC-RP-LOGOUT"], "RP-Initiated Logout profile", "Back-channel and front-channel logout profiles do not isolate the relying-party initiated request, hints, registered post-logout redirect, state return, and end-user consent boundary."),
    _proposal(27, "Freed ID OpenID Connect Session Management client state, session state, origin, check-session iframe, changed event, prompt-none response, logout distinction, minimization, privacy, and nonproduction profile", "oidc-session-management", "Freed ID and CBR Heart", "represented", ["SRC-OIDC-SESSION"], "OpenID Session Management profile", "No inherited profile isolates session-state calculation, RP origin, OP check-session iframe polling, changed events, prompt-none response, and logout distinction."),
    _proposal(28, "Freed ID RFC 7033 WebFinger resource, relation, host-meta refusal, HTTPS, JRD subject, link relation, redirect, cross-origin, minimization, privacy, and nonproduction profile", "webfinger-rfc7033", "Freed ID and CBR Heart", "represented", ["SRC-RFC7033"], "WebFinger discovery profile", "No frozen identity profile isolates WebFinger resource and relation queries, JRD subjects and links, HTTPS, redirect and cross-origin boundaries, and host-meta non-substitution."),
    _proposal(29, "GMUT IXPE HEASARC master-catalog, observation id, target, public date, detector unit, event list, calibration database, response, quality, selection, checksum, covariance, provenance, and zero-row likelihood-refusal adapter", "ixpe-zero-row", "GMUT Mind", "open_gap", ["SRC-IXPE-ARCHIVE", "SRC-IXPE-MASTER"], "IXPE likelihood readiness", "No inherited adapter targets IXPE polarization event products and master-catalog lifecycle with detector-unit, public-date, calibration, response, selection, and covariance duties."),
    _proposal(30, "CBR meteorological station location, whenua and environmental data, severe-weather bulletin, household and worker privacy, accessible notice, service continuity, remedy, affected-party, legal, cultural, data-governance, and Māori-authority reservation", "meteorological-authority", "Freed ID and CBR Heart", "exact_gate", ["SRC-WMO-OBS", "SRC-MAORI-DATA", "SRC-PRIVACY-NZ"], "meteorological data and authority reservation", "No frozen gate combines station-location and whenua data, observation and bulletin disclosure, household and worker privacy, accessible notice, service continuity, remedy, and Māori data authority."),
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
    _source("SRC-X690", "current", "official_international_standard", "ITU-T X.690 ASN.1 encoding rules", "https://www.itu.int/rec/T-REC-X.690/en", "Supports disposable ASN.1 bytes only."),
    _source("SRC-AVIF12", "current", "official_industry_specification", "AV1 Image File Format 1.2", "https://aomediacodec.github.io/av1-avif/", "Supports synthetic AVIF item graphs only."),
    _source("SRC-LZIP", "current", "official_project_manual", "lzip manual 1.26", "https://www.nongnu.org/lzip/manual/lzip_manual.html", "Supports disposable lzip members only."),
    _source("SRC-SPIRV", "current", "official_industry_registry", "Khronos SPIR-V Registry", "https://registry.khronos.org/SPIR-V/", "Supports synthetic SPIR-V words only."),
    _source("SRC-LLVM-BITCODE", "current", "official_project_manual", "LLVM bitcode file format", "https://llvm.org/docs/BitCodeFormat.html", "Supports synthetic bitstreams only."),
    _source("SRC-FLATBUFFERS", "current", "official_project_manual", "FlatBuffers internals", "https://flatbuffers.dev/internals/", "Supports disposable FlatBuffers bytes only."),
    _source("SRC-THRIFT-COMPACT", "current", "official_project_specification", "Apache Thrift Compact Protocol", "https://github.com/apache/thrift/blob/master/doc/specs/thrift-compact-protocol.md", "Supports nonnetwork synthetic messages only."),
    _source("SRC-SHAPEFILE", "stable", "official_vendor_specification", "ESRI Shapefile Technical Description", "https://www.esri.com/content/dam/esrisites/sitecore-archive/Files/Pdfs/library/whitepapers/pdfs/shapefile.pdf", "Supports disposable multi-file fixtures only."),
    _source("SRC-GPKG14", "current", "official_open_standard", "OGC GeoPackage Encoding Standard 1.4", "https://www.geopackage.org/spec140/", "Supports disposable SQLite fixtures only."),
    _source("SRC-LAS14", "stable", "official_industry_specification", "ASPRS LAS 1.4 Revision 15", "https://www.asprs.org/wp-content/uploads/2019/07/LAS_1_4_r15.pdf", "Supports synthetic point-record structures only."),
    _source("SRC-RPM", "current", "official_project_manual", "RPM package format v4", "https://rpm-software-management.github.io/rpm/manual/format_v4.html", "Supports disposable package structures only."),
    _source("SRC-FAT32", "current", "official_platform_specification", "UEFI 2.11 media-access and file-system format", "https://uefi.org/specs/UEFI/2.11/13_Protocols_Media_Access.html", "Supports synthetic volume bytes only."),
    _source("SRC-REGGE1961", "stable", "primary_research", "General relativity without coordinates", "https://doi.org/10.1007/BF02733251", "Supports formal simplicial-gravity vocabulary only."),
    _source("SRC-BARBERO1995", "stable", "primary_research", "Real Ashtekar variables for Lorentzian signature space-times", "https://doi.org/10.1103/PhysRevD.51.5507", "Supports formal canonical-variable vocabulary only."),
    _source("SRC-KOMAR1959", "stable", "primary_research", "Covariant conservation laws in general relativity", "https://doi.org/10.1103/PhysRev.113.934", "Supports formal Killing-charge vocabulary only."),
    _source("SRC-PETROV-REVIEW", "stable", "primary_research", "Petrov classification of perturbed spacetimes: the Kasner example", "https://arxiv.org/abs/gr-qc/0404075", "Supports algebraic-classification vocabulary only."),
    _source("SRC-LEVI-CIVITA", "stable", "primary_research_archive", "Sur l'écart géodésique", "https://eudml.org/doc/182639", "Supports formal Jacobi-field vocabulary only."),
    _source("SRC-WCAG22-TIME", "stable", "official_accessibility_standard", "WCAG 2.2 timing adjustable", "https://www.w3.org/WAI/WCAG22/Understanding/timing-adjustable.html", "Supports structural timing checks; complete conformance remains reserved."),
    _source("SRC-WAI-DIALOG", "current", "official_accessibility_guidance", "WAI-ARIA Authoring Practices dialog modal pattern", "https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/", "Supports structural dialog and focus checks only."),
    _source("SRC-IUPAC-DIFFUSION", "current", "official_scientific_technical_report", "IUPAC definitions and preferred symbols for mass diffusion coefficients", "https://doi.org/10.1515/pac-2024-0251", "Supports physical transport vocabulary only; agency conversion is refused."),
    _source("SRC-HEAGERTY2000", "stable", "primary_research", "Time-dependent ROC curves for censored survival data", "https://doi.org/10.1111/j.0006-341X.2000.00337.x", "Supports statistical obligations only; no participant inference."),
    _source("SRC-MCCLISH1989", "stable", "primary_research", "Analyzing a portion of the ROC curve", "https://doi.org/10.1177/0272989X8900900307", "Supports partial-AUC obligations only."),
    _source("SRC-SPIEGELHALTER1986", "stable", "primary_research", "Probabilistic prediction in patient management and clinical trials", "https://doi.org/10.1002/sim.4780050506", "Supports calibration-test obligations only."),
    _source("SRC-PENCINA2008", "stable", "primary_research", "Evaluating the added predictive ability of a new marker", "https://doi.org/10.1002/sim.2929", "Supports reclassification obligations only; clinical utility remains external."),
    _source("SRC-WMO-OBS", "current", "official_intergovernmental_guidance", "WMO Guide to Instruments and Methods of Observation WMO-No. 8", "https://wmo.int/publication-series/guide-instruments-and-methods-of-observation-wmo-no-8", "Supplies learning context only; no meteorological competence or authority."),
    _source("SRC-OIDC-RP-LOGOUT", "current", "official_identity_standard", "OpenID Connect RP-Initiated Logout 1.0", "https://openid.net/specs/openid-connect-rpinitiated-1_0.html", "Supports synthetic protocol vectors only; no real keys, accounts, or services."),
    _source("SRC-OIDC-SESSION", "current", "official_identity_standard", "OpenID Connect Session Management 1.0", "https://openid.net/specs/openid-connect-session-1_0.html", "Supports synthetic session-state vectors only."),
    _source("SRC-RFC7033", "stable", "official_internet_standard", "RFC 7033 WebFinger", "https://www.rfc-editor.org/info/rfc7033/", "Supports nonnetwork synthetic discovery vectors only."),
    _source("SRC-IXPE-ARCHIVE", "current", "official_scientific_archive", "NASA HEASARC IXPE Data Archive", "https://heasarc.gsfc.nasa.gov/docs/ixpe/archive/", "Supports a zero-row adapter contract only; no query or download occurs."),
    _source("SRC-IXPE-MASTER", "current", "official_dataset_catalogue", "NASA IXPE Master Catalog", "https://data.nasa.gov/dataset/ixpe-master-catalog", "Supplies schema and provenance context only; no observation occurs."),
    _source("SRC-MAORI-DATA", "current", "maori_authority_guidance", "Te Mana Raraunga principles of Māori data sovereignty", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Keeps Māori data decisions with Māori authority."),
    _source("SRC-PRIVACY-NZ", "current", "official_legislation", "Privacy Act 2020", "https://www.legislation.govt.nz/act/public/2020/31/en/latest/", "Keeps legal interpretation, disclosure, and remedy exact-gated."),
]


X1_OPERATIONAL_NEGATIVES = [
    {"negative_id": "V6525-X1-N01", "category": "combined_source_audit_timeout", "failed": "The initial combined sequential source audit exceeded its wrapper deadline and earned no source-state credit.", "recovery": "Split branch, anchor, manifest, storage, and remote probes into bounded scalar reads.", "passing": "Every required source scalar and all four manifest contracts were established independently.", "recurrence_guard": "Do not aggregate large-tree and live-remote checks under one short wrapper deadline."},
    {"negative_id": "V6525-X1-N02", "category": "powershell_merge_base_expression", "failed": "A PowerShell wrapper embedded a semicolon-bearing merge-base command inside an expression and failed parsing before the ancestry result existed.", "recovery": "Run the Git command first, capture LASTEXITCODE separately, and then construct the summary.", "passing": "All four source anchors were proven ancestral with separate scalar commands.", "recurrence_guard": "Keep child command execution outside PowerShell expression and hash-literal values."},
    {"negative_id": "V6525-X1-N03", "category": "broad_inventory_timeout", "failed": "A broad inherited inventory wrapper exceeded its deadline and earned no discovery credit.", "recovery": "Use exact phase-root and filename enumeration with rg and bounded direct reads.", "passing": "The required source builders, tests, index, and routing artifacts were enumerated.", "recurrence_guard": "Prefer exact filenames and phase roots over whole-repository content inventories."},
    {"negative_id": "V6525-X1-N04", "category": "unquoted_revision_suffix", "failed": "An unquoted revision ending in caret-brace-commit was interpreted by PowerShell instead of Git and earned no object-type credit.", "recovery": "Quote the complete revision argument literally before passing it to git cat-file.", "passing": "Every source and anchor resolved as an exact commit object.", "recurrence_guard": "Quote all Git revision expressions containing braces, carets, or upstream syntax."},
    {"negative_id": "V6525-X1-N05", "category": "template_line_count_timeout", "failed": "A combined template existence, full-content line-count, and status wrapper timed out and earned no inventory result.", "recovery": "Enumerate exact filenames first, then use bounded direct reads only for selected files.", "passing": "All required template files were confirmed without another broad content read.", "recurrence_guard": "Do not use repeated Get-Content line counts across large generated builders."},
    {"negative_id": "V6525-X1-N06", "category": "frozen_index_shape_assumption", "failed": "The first novelty probe treated the frozen-chain top-level dictionary as a proposal list and raised an attribute error; it earned no novelty credit.", "recovery": "Inspect the exact schema and concatenate prior_proposals with new_proposals.", "passing": "All 1,300 inherited rows were audited and every accepted v652-v5 title had zero exact matches.", "recurrence_guard": "Probe machine-ledger keys before iterating a new or inherited schema."},
    {"negative_id": "V6525-X1-N07", "category": "bulk_clone_wrapper_timeout", "failed": "The mechanical template-clone wrapper timed out during its trailing status read after the file generation step, so the wrapper itself earned no completion credit.", "recovery": "Do not repeat the write; enumerate every exact destination and inspect their contents read-only.", "passing": "All twelve intended phase-local template destinations existed exactly once and were then reviewed additively.", "recurrence_guard": "Separate bulk mechanical generation from expensive status enumeration."},
    {"negative_id": "V6525-X1-N08", "category": "stale_patch_context", "failed": "The first large proposal-block patch used one stale inherited owner phrase and failed atomically with no content change.", "recovery": "Read the exact current block and apply smaller reviewed hunks.", "passing": "All thirty proposal rows were replaced through exact-context additive patches.", "recurrence_guard": "Refresh mechanically transformed context before applying a large semantic patch."},
    {"negative_id": "V6525-X1-N09", "category": "powershell_regex_quoting", "failed": "A stale-label rg pattern was enclosed in a PowerShell double-quoted string containing an escaped quote and failed parsing before rg ran.", "recovery": "Use a literal single-quoted PowerShell argument for the complete regex.", "passing": "The corrected bounded stale-label search completed and exposed the exact remaining patch targets.", "recurrence_guard": "Use PowerShell single-quoted literals for regexes containing quotes, commas, or dollar anchors."},
    {"negative_id": "V6525-X1-N10", "category": "powershell_discovery_quoting", "failed": "A later multi-term discovery wrapper contained an unterminated PowerShell string and stopped before rg ran, earning no discovery credit.", "recovery": "Reduce the command to one literal pattern per bounded read.", "passing": "Direct single-pattern searches found the intended phase-local references.", "recurrence_guard": "Prefer one single-quoted search literal per PowerShell command when discovery terms contain punctuation."},
    {"negative_id": "V6525-X1-N11", "category": "multi_pattern_pipeline_timeout", "failed": "The corrected multi-pattern rg pipeline timed out while feeding a broad result set through Select-Object and earned no review credit.", "recovery": "Use a simple one-pattern rg invocation against exact files.", "passing": "The bounded search completed and supplied the required review targets.", "recurrence_guard": "Avoid downstream formatting pipelines for large multi-pattern searches."},
    {"negative_id": "V6525-X1-N12", "category": "combined_status_search_timeout", "failed": "A combined Git status and multi-pattern source search exceeded its bound before returning usable evidence and earned no state or review credit.", "recovery": "Split repository state from direct file-bounded searches and use Select-String on exact paths.", "passing": "The direct bounded reads located the operational-negative ledger and remaining rotation threshold.", "recurrence_guard": "Do not combine worktree enumeration with content discovery in one bounded wrapper."},
    {"negative_id": "V6525-X1-N13", "category": "module_symbol_assumption", "failed": "The first phase-data count probe requested inherited names SKILL_SPECS, RUNNER_SPECS, and CLEAN_FIX_REFINE_TASKS that this module does not export; syntax evidence remained valid but the count probe earned zero credit.", "recovery": "Enumerate top-level assignment names from the parsed syntax tree before importing the module.", "passing": "The exact exported names SKILL_IDEAS, RUNNER_IDEAS, and CLEAN_TASKS were identified without guessing.", "recurrence_guard": "Discover phase-data symbols before reusing count wrappers across generations."},
    {"negative_id": "V6525-X1-N14", "category": "proposal_source_field_assumption", "failed": "The corrected count witness completed, but its optional source-coverage tail requested a source_ids field that this proposal schema does not expose and raised a key error; that tail earned zero coverage credit.", "recovery": "Inspect the exact proposal and source keys before testing their relationship.", "passing": "The schema exposed official_or_primary_source_needs on proposals and source_id on the source ledger.", "recurrence_guard": "Bind source-coverage checks to inspected schema keys rather than inherited field names."},
    {"negative_id": "V6525-X1-N15", "category": "foreground_generator_timeout", "failed": "The first foreground x1 generator wrapper exceeded its two-minute bound after producing intermediate files but before a validation receipt, so the entire attempt earned zero x1-build credit.", "recovery": "Confirm no child remains, preserve the intermediate state as zero-credit evidence, and run the same deterministic builder in one hidden bounded process while polling its explicit exit code and logs.", "passing": "The polled deterministic builder completed with an explicit zero exit code and emitted both x1 validation receipts.", "recurrence_guard": "Run process-heavy Method Flow generation under a pollable bounded process instead of a short foreground wrapper."},
    {"negative_id": "V6525-X1-N16", "category": "generated_test_count_literal", "failed": "Review found that the generated x1 test embedded an earlier operational-negative count literal, which would become stale as new failures were retained; it received no test credit.", "recovery": "Compare ledger counts to the generated negative-register length instead of freezing a numeric literal in test source.", "passing": "The regenerated test derives all Method Flow count assertions from the current negative register and passes after generation.", "recurrence_guard": "Use schema relationships rather than lifecycle-sensitive count literals in generated tests."},
    {"negative_id": "V6525-X1-N17", "category": "background_launch_policy_rejection", "failed": "The first background-launch wrapper bundled destructive log cleanup with process creation and was rejected by command policy before execution; it created no process and earned zero credit.", "recovery": "Use unique log filenames and a launch-only Start-Process command with an explicit interpreter and hidden window.", "passing": "The launch-only wrapper created one pollable hidden process without cleanup or elevated permissions.", "recurrence_guard": "Separate optional log housekeeping from process launch and avoid destructive operations in orchestration wrappers."},
]


SAFE_TASKS = [
    "Verify Sylven source, x1, evidence, and final ancestry read-only.",
    "Verify three source-to-final commits, zero merges, and one final parent.",
    "Replay all Sylven commit-local manifest contracts from immutable Git blobs.",
    "Fast-forward only Eiren's clean owned D-first lane.",
    "Prove local, upstream, tracking, and fresh-live equality before x2.",
    "Preserve all 8,549 inherited effective negatives additively.",
    "Preserve all 65 inherited open gaps and 66 inherited exact gates.",
    "Audit thirty proposal titles against all 1,300 frozen titles.",
    "Retain rejected collisions and their replacement rationale.",
    "Verify current official or primary sources without ingesting real data.",
    "Freeze exactly thirty proposals with all required fields.",
    "Freeze exactly 150 synthetic mutations without executing them in x1.",
    "Freeze thirty new safe-now portfolio tasks.",
    "Freeze thirty bounded candidate prototypes.",
    "Freeze ten phase-local skill ideas.",
    "Freeze ten family-current runner ideas.",
    "Freeze thirty additive CLEAN/FIX/REFINE tasks.",
    "Keep inherited completion evidence separate from Eiren credit.",
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
    "ghc-family-binary-schema-and-container-tribunals",
    "ghc-family-geospatial-package-tribunals",
    "ghc-family-runtime-and-volume-format-tribunals",
    "ghc-family-gmut-discrete-and-canonical-boards",
    "ghc-family-gmut-charge-classification-deviation-boards",
    "ghc-family-meteorological-proxy-boundary",
    "ghc-family-oidc-discovery-boundary",
    "ghc-family-accessible-timeout-and-transport-nonconversion",
    "ghc-family-stage20-roc-calibration-reclassification-nonpromotion",
    "ghc-family-v652-v5-validation",
]

RUNNER_IDEAS = [
    "ghc_family_binary_schema_container_tribunals.py",
    "ghc_family_geospatial_package_tribunals.py",
    "ghc_family_runtime_volume_tribunals.py",
    "ghc_family_gmut_discrete_canonical_boards.py",
    "ghc_family_gmut_charge_classification_deviation_boards.py",
    "ghc_family_meteorological_proxy.py",
    "ghc_family_oidc_discovery_boundary.py",
    "ghc_family_accessibility_transport_nonconversion.py",
    "ghc_family_stage20_roc_calibration.py",
    "ghc_family_v652_v5_detailed_validator.py",
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
    "Document BER and CER distinction from the inherited DER-only tribunal.",
    "Document Thrift Compact distinction from Protocol Buffers wire framing.",
    "Document Regge calculus distinction from Regge-Wheeler perturbations.",
    "Document Ashtekar-Barbero distinction from Cartan and ADM surfaces.",
    "Document Komar charges as distinct from generic conservation labels.",
    "Document IXPE polarization products as distinct from Fermi catalog adapters.",
    "Use explicit score keys for novelty nearest-neighbour selection.",
    "Keep token distance subordinate to manual mechanism review.",
    "Use exact phase-root privacy scanning and scanner-definition quarantine.",
    "Use Git path-filtered blob hashes for commit-local manifests.",
    "Keep working-tree bytes distinct from immutable Git-blob evidence.",
    "Parse every public phase JSON document under explicit UTF-8.",
    "Keep real data query, download, row, fit, and likelihood counters at zero.",
    "Keep real key, account, service, and interoperability counters at zero.",
    "Keep real worker, station, instrument, observation, bulletin, incident, and outcome counters at zero.",
    "Reserve manual, browser, assistive-technology, Māori-language, and affected-user review.",
    "Keep legal, cultural, environmental-data, remedy, and Māori decisions exact-gated.",
    "Keep sibling branches and worktrees untouched.",
    "Keep Sandbox, Hyper-V, elevation, security, installation, update, and reboot state unchanged.",
    "Credit exactly one successful exact-final full-repository aggregate and perform no replay.",
    "Keep terminal routing prepared and unsent until all exact-final gates pass.",
    "Keep owner additions below the measured two-thousand-file trigger.",
]

REJECTED_COLLISIONS = [
    {"candidate": "Fermi-LAT 4FGL-DR4 zero-row adapter", "reason": "An inherited title already isolates that exact catalogue; replaced by the distinct IXPE polarization archive lifecycle."},
    {"candidate": "Protocol Buffers wire tribunal", "reason": "The exact wire mechanism is already frozen; retained Thrift Compact and FlatBuffers as distinct encoding graphs."},
    {"candidate": "Gibbons-Hawking-York boundary board", "reason": "The exact boundary term is already frozen; replaced by Komar charge and geodesic-deviation obligations."},
    {"candidate": "WebAssembly binary tribunal", "reason": "Module and section mechanisms are already frozen; replaced by SPIR-V word-framed instruction duties."},
    {"candidate": "Zarr version 3 tribunal", "reason": "Chunk-grid and codec-pipeline mechanisms are already frozen; replaced by GeoPackage relational constraints."},
    {"candidate": "FLAC or Ogg tribunal", "reason": "Both framing mechanisms are already frozen; replaced by lzip member and RPM package duties."},
    {"candidate": "Matroska EBML tribunal", "reason": "EBML nesting and variable integers are already frozen; replaced by AVIF item-graph duties."},
    {"candidate": "generic weather-warning handover", "reason": "A severe-weather amendment handover is inherited; accepted THOS proposals isolate station calibration and synoptic observation quality control."},
    {"candidate": "generic OpenID logout profile", "reason": "Front-channel and back-channel logout are inherited; accepted RP-Initiated Logout and Session Management isolate different protocol actors and state."},
    {"candidate": "generic meteorological authority matrix", "reason": "Generic authority wording was insufficient; the accepted gate isolates station location, whenua and environmental data, bulletin disclosure, privacy, service continuity, and remedy."},
]
