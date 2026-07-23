#!/usr/bin/env python3
"""Frozen Orin Thale v652-v2 x1 data with no x2 observations."""

from __future__ import annotations


PHASE = "v652-v2"
OWNER = "Orin Thale"
PRONOUNS = "they/them"
ROLE = "relational boundary-and-method steward"
HOPE = "keep every surviving claim inspectable, challengeable, and retractable within its evidence class"
BRANCH = "codex/GHC-Family/orin-thale-v642-v6-full-tools"
PHASE_ROOT = "docs/orin-thale/v652-v2"

SOURCE_BRANCH = "codex/GHC-Family/sable-rook-full-tools"
SOURCE_HEAD = "f168bcb798715d61d8b0a9ec2c6646a7af09ce29"
SOURCE_ORIGIN = "4b31ec3d1bb4db24f48967da5c4e27a05b43e1f9"
SOURCE_X1 = "0e7efd8f49dbb530d60e9d2f1b474a3de9a035c2"
SOURCE_EVIDENCE = "fddc360ee643b7b50f7c65395a39948cf0c0d535"
SOURCE_CLOSEOUT = "67ea89adf25dc958c757123501cf43f62f461e2f"
PRIOR_FROZEN = 1210
INHERITED_NEGATIVES = 8022
INHERITED_OPEN_GAPS = 62
INHERITED_EXACT_GATES = 63
PRIMARY_FOCUS = "GMUT Mind"
BOUNDED_PRACTICE = (
    "archaeological collections registration, conservation hold, correction readback, accessible notice, "
    "workload control, and shift handover as a synthetic learning and design lens only"
)

OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]
SOURCE_STATUS_CLASSES = ["current", "stable", "draft", "watch"]
PROTECTED_GATES = [
    "empirical_data",
    "real_participants_or_operators",
    "professional_or_collection_authority",
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
            "Emit unresolved decision rights and reservations only; make no access, research, imaging, "
            "storage, return, repatriation, remedy, legal, cultural, governance, or Maori-authority decision."
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
        "proposal_id": f"V6522-P{number:02d}",
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
        "novelty_against_1210_frozen_proposals": novelty,
    }


PROPOSALS = [
    _proposal(1, "Git reachability-bitmap EWAH word, object-position, XOR flag, commit lookup, pack reverse-index, multi-pack mapping, checksum, stale-pack, and refusal tribunal", "git-bitmap-reverse-index", "THOS Body", "completed", ["SRC-GIT-BITMAP"], "Git reachability-bitmap and reverse-index refusal", "Earlier multi-pack work does not isolate EWAH words, object positions, XOR flags, stale-pack mapping, and reverse-index refusal together."),
    _proposal(2, "Nix NAR magic, type, name, executable, contents length, lexicographic directory, padding, store path, hash, budget, and refusal tribunal", "nix-nar", "THOS Body", "completed", ["SRC-NIX-NAR"], "Nix archive structural refusal", "No frozen title isolates NAR node types, lexicographic directory order, executable metadata, padding, store-path confinement, and byte budgets."),
    _proposal(3, "RPM repository repomd revision, location, checksum, open-checksum, size, timestamp, primary, filelists, other, updateinfo, budget, and refusal tribunal", "rpm-repomd", "THOS Body", "completed", ["SRC-RPM-REPOMD"], "RPM repository metadata refusal", "Debian and OCI repository work does not isolate repomd revision, compressed and open checksums, metadata-role cardinality, and updateinfo refusal."),
    _proposal(4, "NuGet package OPC relationships, nuspec, content-types, package signature, repository countersignature, certificate chain, timestamp, duplicate part, traversal, budget, and refusal tribunal", "nuget-package", "THOS Body", "completed", ["SRC-NUGET-SIGN"], "NuGet package and repository-signature refusal", "Earlier wheel and archive work does not isolate OPC parts, NuGet package signatures, repository countersignatures, certificate chains, and timestamp boundaries."),
    _proposal(5, "PE Authenticode image hash, checksum exclusion, certificate-table exclusion, WIN_CERTIFICATE length, alignment, PKCS7, timestamp, page hash, budget, and refusal tribunal", "pe-authenticode", "THOS Body", "completed", ["SRC-PE-COFF"], "PE Authenticode structural refusal", "No frozen proposal isolates the Authenticode image-hash exclusions, certificate-table placement, WIN_CERTIFICATE alignment, and page-hash boundary."),
    _proposal(6, "GMUT Gibbons-Hawking-York induced metric, extrinsic curvature, unit normal, orientation, sign, joint, corner, variational principle, counterterm, EFT, and observation-firewall board", "gibbons-hawking-york", "GMUT Mind", "completed", ["SRC-GHY"], "Gibbons-Hawking-York boundary obligations", "Israel junction work does not isolate a well-posed action boundary term, normal orientation, corners, counterterms, and observation refusal."),
    _proposal(7, "GMUT Palatini metric-affine independent connection, torsion, nonmetricity, projective symmetry, connection equation, boundary, matter coupling, EFT, unit, and observation-firewall board", "palatini-metric-affine", "GMUT Mind", "completed", ["SRC-PALATINI"], "Palatini metric-affine obligations", "No frozen title isolates independent connection variation with torsion, nonmetricity, projective symmetry, matter coupling, and a typed observation firewall."),
    _proposal(8, "GMUT Raychaudhuri congruence, expansion, shear, vorticity, affine parameter, focusing, caustic, energy-condition assumption, unit, and observation-firewall board", "raychaudhuri-congruence", "GMUT Mind", "completed", ["SRC-RAYCHAUDHURI"], "Raychaudhuri congruence obligations", "Earlier stability and causal boards do not isolate congruence kinematics, affine parameter, caustics, explicit energy-condition assumptions, and non-observation."),
    _proposal(9, "GMUT Bondi-Sachs null-coordinate, asymptotic expansion, mass-aspect, news-tensor, flux, BMS-frame, gauge, boundary, EFT, unit, and observation-firewall board", "bondi-sachs", "GMUT Mind", "completed", ["SRC-BONDI", "SRC-SACHS"], "Bondi-Sachs asymptotic obligations", "No inherited proposal isolates Bondi-Sachs coordinates, mass aspect, news, flux, BMS frames, asymptotic gauge, and an EFT observation firewall."),
    _proposal(10, "GMUT Isaacson two-scale expansion, wavelength hierarchy, averaging cell, gauge, effective stress, backreaction, boundary, EFT, unit, and observation-firewall board", "isaacson-two-scale", "GMUT Mind", "completed", ["SRC-ISAACSON"], "Isaacson two-scale obligations", "Earlier averaging boards do not isolate wavelength hierarchy, averaging-cell choice, gauge behavior, effective stress, backreaction, and observation refusal."),
    _proposal(11, "Safetensors header length, JSON metadata, dtype, shape, data offsets, overlap, duplicate key, endian, byte budget, and refusal tribunal", "safetensors", "THOS Body", "completed", ["SRC-SAFETENSORS"], "Safetensors structural refusal", "No frozen parser isolates the Safetensors header/data split, dtype-shape byte arithmetic, overlapping offsets, duplicate metadata keys, and budgets."),
    _proposal(12, "Mercurial revlog index, data record, node id, linkrev, base revision, delta chain, generaldelta, censoring, sidedata, decompression budget, and refusal tribunal", "mercurial-revlog", "THOS Body", "completed", ["SRC-MERCURIAL-REVLOG"], "Mercurial revlog refusal", "Git object work does not isolate revlog link revisions, generaldelta chains, censoring, sidedata, and decompression bounds."),
    _proposal(13, "OSTree commit, dirtree, dirmeta, file object, checksum, mode, xattr, parent, timestamp, static-delta boundary, traversal budget, and refusal tribunal", "ostree-objects", "THOS Body", "completed", ["SRC-OSTREE"], "OSTree object refusal", "No frozen title isolates OSTree commit, tree, metadata, file-object roles, xattrs, parent lineage, and static-delta boundaries."),
    _proposal(14, "IPFS CARv2 pragma, header, data offset, size, index offset, characteristics, embedded CARv1, multicodec index, padding, checksum, budget, and refusal tribunal", "ipfs-carv2", "THOS Body", "completed", ["SRC-CARV2"], "CARv2 envelope refusal", "Prior CID work does not isolate the CARv2 outer envelope, embedded CARv1 range, index offset, characteristics, padding, and bounded refusal."),
    _proposal(15, "DNSSEC NSEC3 hash algorithm, flags, iterations, salt, owner hash, next hash, type bitmap, closest encloser, opt-out, iteration budget, and refusal tribunal", "dnssec-nsec3", "THOS Body", "completed", ["SRC-RFC5155"], "DNSSEC NSEC3 refusal", "DNS wire-format work does not isolate NSEC3 denial proofs, closest-encloser logic, opt-out, and iteration budgets."),
    _proposal(16, "BGP UPDATE withdrawn routes, path attribute flags, length, ORIGIN, AS_PATH, NEXT_HOP, MP_REACH, MP_UNREACH, duplicate attribute, NLRI, message budget, and refusal tribunal", "bgp-update", "THOS Body", "completed", ["SRC-RFC4271", "SRC-RFC4760"], "BGP UPDATE structural refusal", "No frozen network tribunal isolates BGP UPDATE route withdrawals, attribute flag-length contracts, multiprotocol reachability, duplicate attributes, and NLRI bounds."),
    _proposal(17, "APNG acTL frame count, fcTL sequence, fdAT sequence, IDAT ownership, dispose, blend, frame bounds, CRC, decompression budget, and refusal tribunal", "apng-frames", "THOS Body", "completed", ["SRC-PNG3"], "APNG frame-sequence refusal", "PNG chunk work does not isolate APNG control and frame sequencing, IDAT ownership, dispose/blend operations, bounds, and decompression budgets."),
    _proposal(18, "Accessible provenance graph node and edge text equivalence, reading order, keyboard navigation, focus, name, description, noncolour, zoom, table alternative, and manual-evaluation structural audit", "accessible-provenance-graph", "THOS Body", "completed", ["SRC-WCAG22", "SRC-WAI-APG"], "accessible provenance-graph structure", "Earlier graph and chart audits do not isolate provenance-node and edge equivalence, keyboard graph traversal, and a tabular lineage alternative."),
    _proposal(19, "Thermo-Psyche Kelvin equation curvature radius, surface tension, molar volume, saturation pressure, sign, convex-concave convention, domain, uncertainty, unit, and agency-nonconversion classifier", "kelvin-equation-nonconversion", "Trinity Mandala bridge", "completed", ["SRC-IUPAC-KELVIN"], "Kelvin-equation agency nonconversion", "No frozen nonconversion classifier isolates curvature sign conventions, saturation-pressure shift, molar volume, and domain uncertainty."),
    _proposal(20, "Stage 20 fragility index event flip, loss to follow-up, tie handling, binary endpoint, multiplicity, model dependence, uncertainty, interpretation, and nonpromotion board", "fragility-index", "Trinity Mandala bridge", "completed", ["SRC-FRAGILITY"], "fragility-index nonpromotion", "No inherited Stage 20 board isolates event-flip sensitivity, loss to follow-up, ties, binary endpoints, multiplicity, and model dependence."),
    _proposal(21, "Stage 20 Akaike information criterion likelihood, parameter count, small-sample correction, weight, model set, selection uncertainty, averaging, causal boundary, and nonpromotion board", "akaike-information", "Trinity Mandala bridge", "completed", ["SRC-AKAIKE"], "Akaike-information nonpromotion", "No frozen board isolates AIC, AICc, model weights, candidate-set dependence, model averaging, and causal refusal together."),
    _proposal(22, "WebSocket FIN, RSV, opcode, masking key, payload length, continuation, control frame, UTF-8, close code, message budget, and refusal tribunal", "websocket-frames", "THOS Body", "completed", ["SRC-RFC6455"], "WebSocket frame refusal", "HTTP parser work does not isolate WebSocket masking, fragmentation, control-frame constraints, close codes, UTF-8 validity, and message budgets."),
    _proposal(23, "Kerberos V5 AP-REQ ticket, authenticator, realm, principal, enctype, key usage, clock skew, replay cache, channel binding, authorization data, no-live-realm, and refusal profile", "kerberos-ap-req", "Freed ID and CBR Heart", "completed", ["SRC-RFC4120"], "Kerberos AP-REQ nonlive profile", "No frozen identity profile isolates AP-REQ ticket-authenticator binding, key usage, skew, replay caches, channel binding, and a no-live-realm boundary."),
    _proposal(24, "THOS archaeological collection accession, provenance uncertainty, condition check, location custody, conservation hold, correction readback, accessible notice, workload, and shift-handover proxy", "archaeology-handover", "THOS Body", "represented", ["SRC-CIDOC-CRM"], "archaeological collections handover", "Court, archive, museum, and heritage proxies do not isolate archaeological provenance uncertainty, conservation holds, location custody, correction readback, and workload handover."),
    _proposal(25, "THOS archaeological catalogue correction latency, provenance disagreement, fatigue, harm stop, skill decay, workload budget, missingness, readback, and handover proxy", "archaeology-correction-latency", "THOS Body", "represented", ["SRC-CIDOC-CRM"], "archaeological catalogue correction proxy", "No frozen THOS proxy binds archaeological provenance disagreement and correction latency to fatigue, harm stops, skill decay, missingness, readback, and handover."),
    _proposal(26, "Freed ID X.509 delegated credential signature algorithm, expected certificate verify, validity, private-key separation, transcript binding, rotation, compromise, privacy, and nonproduction profile", "x509-delegated-credential", "Freed ID and CBR Heart", "represented", ["SRC-RFC9345"], "X.509 delegated-credential profile", "Earlier certificate profiles do not isolate delegated-credential validity, expected CertificateVerify algorithms, transcript binding, key separation, and compromise handling."),
    _proposal(27, "Freed ID RATS attester, verifier, relying party, evidence, endorsement, reference value, appraisal policy, trustworthiness vector, privacy, and nonproduction architecture profile", "rats-architecture", "Freed ID and CBR Heart", "represented", ["SRC-RFC9334"], "RATS architecture profile", "EAT claim-set work does not isolate RATS roles, endorsements, reference values, appraisal policy, relying-party decisions, and privacy boundaries as an architecture."),
    _proposal(28, "Freed ID MLS KeyPackage credential, ciphersuite, extension, lifetime, signature, Welcome, GroupInfo, tree hash, external sender, privacy, and nonproduction profile", "mls-keypackage", "Freed ID and CBR Heart", "represented", ["SRC-RFC9420"], "MLS KeyPackage profile", "No frozen identity proposal isolates MLS KeyPackage credentials, lifetime and extension checks, Welcome and GroupInfo linkage, tree hashes, and external senders."),
    _proposal(29, "GMUT Zwicky Transient Facility IRSA light-curve object, exposure, filter, photometry, quality, cadence, reference image, selection, covariance, provenance, checksum, and zero-row likelihood-refusal adapter", "ztf-zero-row", "GMUT Mind", "open_gap", ["SRC-ZTF"], "ZTF likelihood readiness", "No inherited zero-row adapter targets the official ZTF light-curve object and exposure products with cadence, reference-image, selection, covariance, provenance, and checksum duties."),
    _proposal(30, "CBR archaeological human remains and taonga decision-rights reservation for access, research, imaging, provenance, storage, return, repatriation, remedy, tikanga context, tangata-whenua governance, and Maori authority", "archaeology-authority", "Freed ID and CBR Heart", "exact_gate", ["SRC-PROTECTED-OBJECTS-NZ", "SRC-HERITAGE-NZ"], "archaeological authority reservation", "No frozen exact-gate surface combines archaeological human remains and taonga access, imaging, provenance, storage, return, repatriation, remedy, tikanga context, and tangata-whenua governance."),
]


def _source(source_id, status, kind, title, url, implication):
    return {"source_id": source_id, "status": status, "kind": kind, "title": title, "url": url, "phase_implication": implication}


SOURCES = [
    _source("SRC-GIT-BITMAP", "current", "official_software_documentation", "Git bitmap format", "https://git-scm.com/docs/bitmap-format.html", "Supports disposable bitmap fixtures only; no canonical object or pack mutation."),
    _source("SRC-NIX-NAR", "current", "official_software_documentation", "Nix Archive format", "https://nix.dev/manual/nix/2.25/protocols/nix-archive", "Supports synthetic NAR fields only; no store import."),
    _source("SRC-RPM-REPOMD", "current", "official_project_documentation", "createrepo_c repomd API", "https://rpm-software-management.github.io/createrepo_c/c/group__repomd.html", "Supports synthetic RPM repository metadata only."),
    _source("SRC-NUGET-SIGN", "current", "official_platform_documentation", "NuGet repository signatures resource", "https://learn.microsoft.com/en-us/nuget/api/repository-signatures-resource", "Supports synthetic package and signature fixtures only; no trust decision."),
    _source("SRC-PE-COFF", "current", "official_platform_specification", "PE format", "https://learn.microsoft.com/en-us/windows/win32/debug/pe-format", "Supports disposable PE byte fixtures only."),
    _source("SRC-GHY", "stable", "primary_research", "Action integrals and partition functions in quantum gravity", "https://doi.org/10.1103/PhysRevD.15.2752", "Supports formal boundary-term vocabulary only."),
    _source("SRC-PALATINI", "stable", "primary_research", "Metric-affine gravity and Palatini formalism", "https://arxiv.org/abs/2105.07053", "Supports formal connection-variation vocabulary only."),
    _source("SRC-RAYCHAUDHURI", "stable", "primary_research", "Relativistic cosmology I", "https://doi.org/10.1103/PhysRev.98.1123", "Supports formal congruence vocabulary only."),
    _source("SRC-BONDI", "stable", "primary_research", "Gravitational waves in general relativity VII", "https://doi.org/10.1098/rspa.1962.0161", "Supports asymptotic null-coordinate vocabulary only."),
    _source("SRC-SACHS", "stable", "primary_research", "Gravitational waves in general relativity VIII", "https://doi.org/10.1098/rspa.1962.0206", "Supports news and asymptotic-symmetry vocabulary only."),
    _source("SRC-ISAACSON", "stable", "primary_research", "Gravitational radiation in the limit of high frequency", "https://doi.org/10.1103/PhysRev.166.1263", "Supports two-scale formal obligations only."),
    _source("SRC-SAFETENSORS", "current", "official_project_specification", "Safetensors format", "https://github.com/huggingface/safetensors", "Supports synthetic tensor-envelope fixtures only."),
    _source("SRC-MERCURIAL-REVLOG", "current", "official_project_documentation", "Mercurial revlog", "https://www.mercurial-scm.org/wiki/Revlog", "Supports disposable revlog fixtures only."),
    _source("SRC-OSTREE", "current", "official_project_documentation", "OSTree repository formats", "https://ostreedev.github.io/ostree/formats/", "Supports synthetic OSTree objects only."),
    _source("SRC-CARV2", "current", "official_specification", "Content Addressable aRchives v2", "https://ipld.io/specs/transport/car/carv2/", "Supports synthetic CAR envelopes only."),
    _source("SRC-RFC5155", "stable", "official_standard", "RFC 5155 DNS Security Hashed Authenticated Denial of Existence", "https://www.rfc-editor.org/rfc/rfc5155.html", "Supports synthetic NSEC3 vectors only."),
    _source("SRC-RFC4271", "stable", "official_standard", "RFC 4271 Border Gateway Protocol 4", "https://www.rfc-editor.org/rfc/rfc4271.html", "Supports bounded UPDATE fields only; no network traffic."),
    _source("SRC-RFC4760", "stable", "official_standard", "RFC 4760 Multiprotocol Extensions for BGP-4", "https://www.rfc-editor.org/rfc/rfc4760.html", "Supports synthetic MP_REACH and MP_UNREACH fields only."),
    _source("SRC-PNG3", "current", "official_recommendation", "Portable Network Graphics Third Edition", "https://www.w3.org/TR/png-3/", "Supports disposable APNG chunks only."),
    _source("SRC-WCAG22", "stable", "official_accessibility_standard", "Web Content Accessibility Guidelines 2.2", "https://www.w3.org/TR/WCAG22/", "Supports structural checks; complete conformance remains reserved."),
    _source("SRC-WAI-APG", "current", "official_accessibility_guidance", "WAI-ARIA Authoring Practices Guide", "https://www.w3.org/WAI/ARIA/apg/", "Supports keyboard and naming structure only."),
    _source("SRC-IUPAC-KELVIN", "stable", "official_terminology", "IUPAC Gold Book Kelvin equation", "https://goldbook.iupac.org/terms/view/K03378", "Supports thermodynamic vocabulary only; agency conversion is refused."),
    _source("SRC-FRAGILITY", "stable", "primary_research", "The fragility index of randomized controlled trials", "https://doi.org/10.1016/j.jclinepi.2013.10.019", "Supports structural sensitivity vocabulary only; no participant inference."),
    _source("SRC-AKAIKE", "stable", "primary_research", "A new look at the statistical model identification", "https://doi.org/10.1109/TAC.1974.1100705", "Supports model-selection vocabulary only."),
    _source("SRC-RFC6455", "stable", "official_standard", "RFC 6455 The WebSocket Protocol", "https://www.rfc-editor.org/rfc/rfc6455.html", "Supports disposable frame fixtures only; no network service."),
    _source("SRC-RFC4120", "stable", "official_standard", "RFC 4120 Kerberos Network Authentication Service V5", "https://www.rfc-editor.org/rfc/rfc4120.html", "Supports nonlive AP-REQ vectors only; no realm, key, account, or ticket."),
    _source("SRC-CIDOC-CRM", "current", "official_domain_model", "CIDOC Conceptual Reference Model", "https://www.cidoc-crm.org/", "Supplies collections-information vocabulary only; no professional or affected-party authority."),
    _source("SRC-RFC9345", "stable", "official_standard", "RFC 9345 Delegated Credentials for TLS and DTLS", "https://www.rfc-editor.org/rfc/rfc9345.html", "Supports synthetic delegated-credential vectors only."),
    _source("SRC-RFC9334", "stable", "official_standard", "RFC 9334 Remote ATtestation procedureS Architecture", "https://www.rfc-editor.org/rfc/rfc9334.html", "Supports synthetic role and appraisal-policy structure only."),
    _source("SRC-RFC9420", "stable", "official_standard", "RFC 9420 The Messaging Layer Security Protocol", "https://www.rfc-editor.org/rfc/rfc9420.html", "Supports synthetic MLS structures only; no group or key operation."),
    _source("SRC-ZTF", "current", "official_data_service", "Zwicky Transient Facility at IRSA", "https://irsa.ipac.caltech.edu/Missions/ztf.html", "Supports a zero-row readiness contract only; no query or download occurs."),
    _source("SRC-PROTECTED-OBJECTS-NZ", "current", "official_legal_context", "Protected Objects Act 1975", "https://www.legislation.govt.nz/act/public/1975/0041/9.0/whole.html", "Keeps legal interpretation and return decisions exact-gated."),
    _source("SRC-HERITAGE-NZ", "current", "official_legal_context", "Heritage New Zealand Pouhere Taonga Act 2014", "https://legislation.govt.nz/act/public/2014/26/en/latest/whole.html", "Keeps archaeological, cultural, tangata-whenua, and Maori authority external."),
]


X1_OPERATIONAL_NEGATIVES = [
    {"negative_id": "V6522-X1-N01", "category": "tracking_ref_construction", "failed": "A read-only probe constructed a tracking ref by stripping a hierarchical branch prefix and Git rejected it.", "recovery": "Ask Git for the configured symbolic upstream ref.", "passing": "The exact tracking ref resolved and four-way equality passed.", "recurrence_guard": "Never derive a tracking ref by editing branch-name text."},
    {"negative_id": "V6522-X1-N02", "category": "manifest_scope_assumption", "failed": "A read-only manifest audit invented a docs-only path scope and reported phase-owned scripts and tests as false extras.", "recovery": "Bind path parity to the immutable validator coverage predicate.", "passing": "All six source manifests and 911 entries matched.", "recurrence_guard": "Use sealed coverage predicates rather than guessed directory scopes."},
    {"negative_id": "V6522-X1-N03", "category": "unbounded_repository_search", "failed": "A broad proposal-chain search emitted repetitive baton text and exceeded useful output.", "recovery": "Resolve the exact structured index and emit a bounded schema summary.", "passing": "The exact index reported 1,210 titles.", "recurrence_guard": "Search filenames first and query exact structured artifacts."},
    {"negative_id": "V6522-X1-N04", "category": "proposal_index_schema_assumption", "failed": "A read-only probe assumed a proposals key that the frozen index does not define.", "recovery": "Inspect keys and types before selecting arrays.", "passing": "prior_proposals and new_proposals were read with the declared count.", "recurrence_guard": "Never index inherited JSON before checking its schema."},
    {"negative_id": "V6522-X1-N05", "category": "novelty_schema_assumption", "failed": "A read-only probe assumed a proposals key in the novelty audit and received null.", "recovery": "Inspect keys before reading rows and threshold.", "passing": "The exact rows and threshold fields were identified.", "recurrence_guard": "Treat phase-specific novelty schemas as data, not universal contracts."},
    {"negative_id": "V6522-X1-N06", "category": "grouped_startup_output", "failed": "A grouped read-only source and lane probe exceeded useful wrapper output and yielded no attributable evidence.", "recovery": "Split it into isolated no-profile bounded commands.", "passing": "Each topology, ledger, and inventory probe returned independently.", "recurrence_guard": "Do not group long artifact reads with topology checks."},
    {"negative_id": "V6522-X1-N07", "category": "overlarge_primary_source_fetch", "failed": "One read-only request opened eight long RFCs and exceeded useful response context.", "recovery": "Open official specifications in bounded units.", "passing": "An isolated RFC 6455 read returned attributable framing anchors.", "recurrence_guard": "Fetch one long specification at a time when only bounded anchors are needed."},
    {"negative_id": "V6522-X1-N08", "category": "parallel_shell_all_or_nothing", "failed": "One slow login shell caused an all-or-nothing parallel wrapper to discard three read-only results.", "recovery": "Use isolated no-profile probes with individual timeouts.", "passing": "All three probes returned independently with zero exits.", "recurrence_guard": "Do not share one rejecting promise across evidence probes with different costs."},
    {"negative_id": "V6522-X1-N09", "category": "overview_word_floor", "failed": "The first x1 generator materialized a 1,283-word overview and stopped below the 1,300-word floor.", "recovery": "Add a substantive evidence-domain paragraph and measure the exact generated function output.", "passing": "The revised overview measured 1,350 words before retry.", "recurrence_guard": "Measure the exact generated overview before accepting the builder witness."},
    {"negative_id": "V6522-X1-N10", "category": "malformed_apply_patch_hunk", "failed": "A malformed patch hunk was appended as literal source text and made the x1 builder unparsable.", "recovery": "Use bounded exact-context patches and parse the full source.", "passing": "Literal patch debris was removed and the source parsed.", "recurrence_guard": "Never prefix a hunk marker as added content."},
    {"negative_id": "V6522-X1-N11", "category": "apply_patch_context_mismatch", "failed": "The first broad cleanup patch failed exact-context verification and changed nothing.", "recovery": "Split the repair into small independently verified hunks.", "passing": "Both bounded repairs applied and preserved intended content.", "recurrence_guard": "Inspect exact target lines before combining distant cleanup hunks."},
    {"negative_id": "V6522-X1-N12", "category": "unicode_diagnostic_cp1252", "failed": "A read-only source repr diagnostic failed on a Maori macron under the default CP1252 stream.", "recovery": "Pin UTF-8 before the same bounded diagnostic.", "passing": "The UTF-8 syntax and word-count diagnostic completed.", "recurrence_guard": "Pin UTF-8 before Unicode-emitting diagnostics."},
    {"negative_id": "V6522-X1-N13", "category": "recurrent_malformed_patch_hunk", "failed": "A later multi-file patch again prefixed hunk markers as added content and appended literal diff debris to two owner sources.", "recovery": "Apply exact hunks without prefixed markers, remove only the appended debris, and parse both complete sources.", "passing": "Both sources parsed and the intended negative-count contract was present in its real location.", "recurrence_guard": "Inspect patch syntax before calling apply_patch and reject any added line whose content is a hunk marker."},
    {"negative_id": "V6522-X1-N14", "category": "ripgrep_diff_marker_regex", "failed": "A speculative ripgrep alternation for patch markers had an unclosed group and returned no evidence.", "recovery": "Use fixed-string search and treat the expected empty result as a zero-hit pass.", "passing": "The exact marker search reported zero hits.", "recurrence_guard": "Use literal search for literal control tokens."},
    {"negative_id": "V6522-X1-N15", "category": "privacy_receipt_definition_classification", "failed": "The first exact staged scan treated two pattern-name echoes inside its own privacy receipt as confirmed payload hits.", "recovery": "Add the exact privacy receipt path to the scanner-definition set and rerun the same staged blobs.", "passing": "All 53 staged files and 41 JSON blobs passed with five candidates and zero confirmed payload hits.", "recurrence_guard": "Quarantine exact scanner-receipt definitions before payload adjudication."},
]


SAFE_TASKS = [
    "Verify all five Sable anchors and the four-commit zero-merge lineage.",
    "Verify Orin fast-forward provenance and four-way equality without source mutation.",
    "Reconcile the 8,021 sealed and one external activation negative.",
    "Replay six inherited manifest contracts from immutable Git blobs.",
    "Audit current, stable, draft, and watch source statuses.",
    "Compute token-Jaccard neighbours across all 1,210 frozen titles.",
    "Record manual mechanism distinctions and rejected collisions.",
    "Protect every x1 path with an exact staged allowlist.",
    "Seal x1 content in the Git path-filtered blob domain.",
    "Parse every phase JSON document with explicit UTF-8.",
    "Separate scanner definitions, review candidates, and confirmed payload hits.",
    "Declare working-byte and Git-blob hash domains without conflation.",
    "Measure full checkout and Orin-generated file footprints separately.",
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
    "Keep ZTF query, row, likelihood, posterior, and constraint counts at zero.",
    "Keep identity profiles synthetic with zero real keys, accounts, or exchanges.",
    "Keep THOS proxies at zero real people, collections, operations, or outcomes.",
    "Reserve manual, browser, assistive-technology, Maori-language, and affected-user evaluation.",
    "Keep every Method Flow failure linked to its bounded recovery witness.",
]


CANDIDATE_TASKS = [f"Build and bounded-test {proposal['mission_surface']}." for proposal in PROPOSALS]


SKILL_IDEAS = [
    "ghc-family-git-bitmap-reverse-index",
    "ghc-family-nar-rpm-envelope",
    "ghc-family-nuget-authenticode-boundary",
    "ghc-family-gmut-boundary-congruence-board",
    "ghc-family-gmut-null-backreaction-board",
    "ghc-family-content-store-format-tribunals",
    "ghc-family-routing-security-format-tribunals",
    "ghc-family-archaeology-handover-proxy",
    "ghc-family-attestation-group-identity-boundary",
    "ghc-family-stage20-robustness-nonpromotion",
]


RUNNER_IDEAS = [
    "ghc_family_git_bitmap_guard.py",
    "ghc_family_archive_repository_tribunals.py",
    "ghc_family_package_signature_tribunals.py",
    "ghc_family_gmut_boundary_congruence_boards.py",
    "ghc_family_gmut_null_backreaction_boards.py",
    "ghc_family_content_store_tribunals.py",
    "ghc_family_network_format_tribunals.py",
    "ghc_family_archaeology_proxy.py",
    "ghc_family_identity_attestation_profiles.py",
    "ghc_family_v652_v2_detailed_validator.py",
]


CLEAN_TASKS = [
    "Ingest the external routing negative without rewriting Sable's sealed count.",
    "Replace constructed tracking refs with Git-resolved upstream refs.",
    "Replace guessed manifest scopes with immutable validator predicates.",
    "Bound repository-search output before evidence attribution.",
    "Inspect inherited JSON keys before indexing arrays.",
    "Split all-or-nothing shell probes into independently attributable commands.",
    "Fetch long primary specifications in bounded units.",
    "Pin UTF-8 before every Unicode-emitting diagnostic.",
    "Reconcile count-dependent truth mirrors after retained failures.",
    "Normalize generated text through the declared Git-blob hash domain.",
    "Separate privacy scanner definitions from payload findings.",
    "Preserve unresolved privacy candidates until explicit adjudication.",
    "Use exact eligible-test arithmetic rather than raw discovery cardinality.",
    "Verify family-current caller collisions before adding wrappers.",
    "Preserve historical tools as compatibility surfaces.",
    "Rebuild accessible output while retaining manual-evaluation reservations.",
    "Check every phase document against the live word cap.",
    "Check Orin-generated growth against the 15,000-file threshold.",
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
    {"candidate": "Protocol Buffers wire tribunal", "reason": "token collision above threshold with V6501-P20; replaced by WebSocket framing"},
    {"candidate": "generic archaeological matched-budget comparator", "reason": "mechanism and lexical collision with Sable's generic matched-budget board; rewritten as correction-latency and provenance-disagreement proxy"},
    {"candidate": "Newman-Penrose obligation board", "reason": "manual mechanism adjacency to the frozen Geroch-Held-Penrose board; replaced by Bondi-Sachs asymptotic obligations"},
    {"candidate": "Git reftable parser", "reason": "already frozen in the proposal chain; replaced by bitmap EWAH and reverse-index mechanics"},
    {"candidate": "CycloneDX component ledger", "reason": "already represented by inherited software-bill-of-materials work; replaced by RPM repomd"},
    {"candidate": "generic EAT claims profile", "reason": "already frozen; replaced by RATS role and appraisal-policy architecture"},
    {"candidate": "generic Rubin or Euclid adapter", "reason": "existing survey adapters are frozen; replaced by the distinct ZTF IRSA light-curve product contract"},
    {"candidate": "generic sortable-table audit", "reason": "inherited accessibility surfaces cover sorting; replaced by provenance graph node-edge equivalence"},
    {"candidate": "Gibbs-Duhem nonconversion", "reason": "already frozen in adjacent thermodynamic obligation work; replaced by the Kelvin curvature equation"},
    {"candidate": "generic alpha-spending board", "reason": "already frozen in sequential-analysis work; replaced by fragility-index and AIC nonpromotion controls"},
]
