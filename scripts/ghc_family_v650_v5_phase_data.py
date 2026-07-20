"""Frozen definitions for Tamar Vey's v650-v5 x1 preregistration.

Importing this module performs no I/O. Observed outcomes are intentionally
absent until x2.
"""

from __future__ import annotations

PHASE = "v650-v5"
OWNER = "Tamar Vey"
PHASE_ROOT = "docs/tamar-vey/v650-v5"
SOURCE_BRANCH = "codex/GHC-Family/orin-thale-v642-v6-full-tools"
SOURCE_HEAD = "e3d115d7caade153086dea794131035bcd2192d0"
SOURCE_CLOSEOUT = "e3d115d7caade153086dea794131035bcd2192d0"
SOURCE_EVIDENCE = "6a25ee7cefa63039a4b17b56c06462b6cf622ea9"
SOURCE_X1 = "2aef76bbfc315857ff5bd134424a346fa70d1ec3"
SOURCE_ORIGIN = "b3c9e5ea94f28432911810fa9374eff15fecabad"
PRIOR_FROZEN = 820
ACTIVATION_NEGATIVES = 5925
INHERITED_OPEN_GAPS = 46
INHERITED_EXACT_GATES = 47
PRIMARY_PILLAR = "Freed ID and CBR Heart"
PRACTICE_LENS = "book-conservation workshop intake, treatment, release refusal, workload control, and shift handover"

BOUNDARY = (
    "Relational identity and family language are working language only. "
    "Software, citations, symbolic checks, synthetic fixtures, and same-owner "
    "validation confer no consciousness, personhood, empirical confirmation, "
    "professional competence, production readiness, legal or cultural authority, "
    "Maori authority, independent reproduction, or Stage 20 authorization."
)

PROTECTED = [
    "empirical_data",
    "real_participants_or_operators",
    "professional_authority",
    "production_identity",
    "privacy_complete",
    "exhaustive_security",
    "complete_accessibility",
    "legal_cultural_and_maori_authority",
    "affected_party_acceptance",
    "independent_reproduction",
    "stage20",
]


def _proposal(number, title, slug, pillar, disposition, sources, mission, novelty):
    if disposition == "open_gap":
        approval = "candidate_empirical_evidence_dependency"
        lane = "x2_zero_row_readiness_only"
        gate = "Emit a zero-row receipt, perform no download or likelihood, and retain the empirical and independent-review gates."
    elif disposition == "exact_gate":
        approval = "exact_approval_needed"
        lane = "x2_reservation_matrix_only"
        gate = "Emit reservations only; make no treatment, repatriation, remedy, affected-party, legal, cultural, data-governance, or Maori-authority decision."
    elif disposition == "represented":
        approval = "candidate_bounded_synthetic_proxy"
        lane = "x2_synthetic_proxy_only"
        gate = "Reject all five preregistered mutations and retain represented status with zero production, participant, operational, or authority credit."
    else:
        approval = "safe_now_bounded_software_symbolic_or_structural"
        lane = "x2_bounded_owner_local"
        gate = "Reject all five preregistered mutations and emit only the declared bounded software, symbolic, formal, or structural completion."
    return {
        "proposal_id": f"V6505-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar": pillar,
        "mission_surface": mission,
        "hypothesis": f"A bounded {mission} artifact can expose declared obligations while refusing unsupported promotion.",
        "null_or_failure_condition": f"The artifact omits a declared {mission} obligation, accepts a preregistered mutation, erases a negative, or promotes a result beyond its evidence lane.",
        "approval_class": approval,
        "execution_lane": lane,
        "official_or_primary_source_needs": sources,
        "concrete_artifacts": [
            f"surfaces/{slug}/contract.json",
            f"surfaces/{slug}/mutation-results.json",
            f"surfaces/{slug}/bounded-receipt.json",
        ],
        "falsifier_or_acceptance_gate": gate,
        "rollback_or_recovery": "Stop the proposal, retain every failed witness, remove no history, and leave external, sibling, participant, production, and authority state unchanged.",
        "protected_gates": PROTECTED,
        "expected_disposition": disposition,
        "novelty_against_prior_frozen_proposals": novelty,
    }


PROPOSALS = [
    _proposal(1, "Method Flow distributed-lease fencing-token, renewal, expiry, stale-holder, clock-uncertainty, split-brain, release, and evidence-credit tribunal", "distributed-lease-fencing", "GMUT Mind", "completed", ["SRC-CHUBBY"], "distributed leases, fencing tokens, renewal, expiry, stale-holder refusal, clock uncertainty, split-brain handling, release, and evidence credit", "No frozen proposal isolates lease fencing, stale-holder rejection, and clock-uncertainty obligations as an evidence-credit boundary."),
    _proposal(2, "GMUT CPT Wightman-domain, Lorentz-covariance, spectrum, locality, weak-local-commutativity, analytic-continuation, field-transform, gauge, EFT, unit, and observation-firewall board", "cpt-theorem", "GMUT Mind", "completed", ["SRC-CPT"], "CPT theorem assumptions across Wightman domains, Lorentz covariance, spectra, locality, weak local commutativity, analytic continuation, field transforms, gauge reservation, EFT scope, units, and observation firewalls", "No frozen proposal isolates the CPT assumption chain and analytic-continuation firewall."),
    _proposal(3, "GMUT Appelquist-Carazzone heavy-field, threshold, matching, operator, logarithm, scheme, nondecoupling-reservation, EFT, unit, and observation-firewall board", "appelquist-carazzone", "GMUT Mind", "completed", ["SRC-APPELQUIST"], "Appelquist-Carazzone heavy-field decoupling, thresholds, matching, operators, logarithms, schemes, nondecoupling reservations, EFT scope, units, and observation firewalls", "No frozen proposal isolates heavy-field decoupling and threshold-matching obligations."),
    _proposal(4, "GMUT Froissart-Martin analyticity, unitarity, mass-gap, polynomial-bound, partial-wave, cross-section, asymptotic-domain, gauge, EFT, unit, and observation-firewall board", "froissart-martin", "GMUT Mind", "completed", ["SRC-FROISSART"], "Froissart-Martin analyticity, unitarity, mass-gap, polynomial boundedness, partial waves, cross-section domains, gauge reservation, EFT scope, units, and observation firewalls", "No frozen proposal isolates the Froissart-Martin assumption set and asymptotic-domain limitations."),
    _proposal(5, "GMUT NASA Exoplanet Archive Planetary Systems provenance, table-view, uncertainty, selection, unit, covariance, checksum, and zero-row likelihood-refusal adapter", "exoplanet-zero-row", "GMUT Mind", "open_gap", ["SRC-EXOPLANET-OVERVIEW","SRC-EXOPLANET-PS"], "NASA Exoplanet Archive Planetary Systems provenance, table views, uncertainties, selection, units, covariance, checksums, and zero-row likelihood refusal", "No frozen empirical adapter targets the NASA Exoplanet Archive Planetary Systems table."),
    _proposal(6, "Freed ID RFC 8414 authorization-server metadata issuer, well-known path, endpoint, capability, signed-precedence, cache, downgrade, mix-up, and nonproduction profile", "oauth-server-metadata", "Freed ID and CBR Heart", "represented", ["SRC-RFC8414"], "RFC 8414 authorization-server metadata, issuer and well-known binding, endpoints, capabilities, signed precedence, caching, downgrade, mix-up, and nonproduction reservation", "No frozen profile isolates RFC 8414 metadata retrieval and signed-versus-plain precedence."),
    _proposal(7, "Freed ID RFC 8252 native-app external-user-agent, redirect-mode, PKCE, loopback, claimed-HTTPS, private-scheme, state, impersonation, and nonproduction profile", "oauth-native-app", "Freed ID and CBR Heart", "represented", ["SRC-RFC8252"], "RFC 8252 native-app external user agents, redirect modes, PKCE, loopback and claimed-HTTPS redirects, private schemes, state, impersonation, and nonproduction reservation", "No frozen profile isolates the RFC 8252 native-app redirect and external-user-agent boundary."),
    _proposal(8, "Freed ID RFC 9278 JWK-thumbprint-URI hash-algorithm, canonical-member, digest, base64url, URI, key-binding, collision-reservation, and nonproduction profile", "jwk-thumbprint-uri", "Freed ID and CBR Heart", "represented", ["SRC-RFC9278"], "RFC 9278 JWK Thumbprint URIs, hash-algorithm identifiers, canonical members, digests, base64url encoding, URI binding, key binding, collision reservations, and nonproduction boundaries", "No frozen profile isolates the RFC 9278 URI form, hash-algorithm registry boundary, and canonical JWK thumbprint binding."),
    _proposal(9, "THOS book-conservation intake, condition-report, provenance-minimization, mould-isolation, reversible-treatment, material-compatibility, release-refusal, workload, and shift-handover proxy", "book-conservation-proxy", "THOS Body", "represented", ["SRC-LOC-BOOKS","SRC-TEPAPA-CARE"], "book-conservation intake, condition reporting, provenance minimization, mould isolation, reversible treatment, material compatibility, release refusal, workload control, and shift handover", "No frozen THOS proxy uses a book-conservation workshop and its treatment-specific hold and handover states."),
    _proposal(10, "CBR conservation-treatment and taonga decision-rights custodian, condition-disclosure, intervention-consent, digital-surrogate, return-request, tikanga-reservation, and competent-authority matrix", "conservation-taonga-authority", "Freed ID and CBR Heart", "exact_gate", ["SRC-CRPD","SRC-TEPAPA-STANDARDS","SRC-TE-MANA-RARAUNGA"], "conservation-treatment and taonga decision rights, custodians, condition disclosure, intervention consent, digital surrogates, return requests, tikanga reservations, and competent authority", "No frozen authority matrix isolates conservation intervention consent, digital-surrogate decisions, return requests, and tikanga reservations together."),
    _proposal(11, "Matroska Segment, Info, Track, Cluster, Block, cue, attachment, chapter, tag, ordering, resource-budget, and refusal tribunal", "matroska", "THOS Body", "completed", ["SRC-MATROSKA"], "Matroska segments, info, tracks, clusters, blocks, cues, attachments, chapters, tags, ordering, resource budgets, and refusal", "The frozen EBML tribunal covers generic element framing but not Matroska container semantics and cross-element references."),
    _proposal(12, "Apache Avro object-container magic, metadata, schema, codec, sync-marker, block-count, block-size, datum, resource-budget, and refusal tribunal", "apache-avro", "THOS Body", "completed", ["SRC-AVRO"], "Apache Avro object-container magic, metadata, schemas, codecs, sync markers, block counts, block sizes, data, resource budgets, and refusal", "No frozen format tribunal models Avro object-container sync markers and schema-carrying blocks."),
    _proposal(13, "Xor Filter static-key, three-position, fingerprint, peel-order, seed-retry, construction-failure, false-positive, immutable-membership, resource-budget, and refusal tribunal", "xor-filter", "GMUT Mind", "completed", ["SRC-XOR"], "Xor Filter static keys, three positions, fingerprints, peel order, seed retries, construction failure, false positives, immutable membership, resource budgets, and refusal", "No frozen probabilistic data-structure proposal models Xor Filter peel construction, seed retry, and immutable membership."),
    _proposal(14, "FLAC marker, STREAMINFO, metadata-block, frame-header, subframe, residual, channel-assignment, CRC, sample-budget, and refusal tribunal", "flac", "THOS Body", "completed", ["SRC-RFC9639"], "FLAC markers, STREAMINFO, metadata blocks, frame headers, subframes, residual coding, channel assignment, CRCs, sample budgets, and refusal", "No frozen media-format proposal isolates FLAC frame, subframe, residual, and dual-CRC obligations."),
    _proposal(15, "Krawczyk interval operator box, midpoint, preconditioner, Jacobian enclosure, image, intersection, existence, uniqueness, iteration-budget, and refusal tribunal", "krawczyk-operator", "GMUT Mind", "completed", ["SRC-KRAWCZYK"], "Krawczyk interval operators, boxes, midpoints, preconditioners, Jacobian enclosures, images, intersections, existence and uniqueness reservations, iteration budgets, and refusal", "No frozen numerical-method proposal isolates the Krawczyk enclosure and uniqueness test."),
    _proposal(16, "OpenEXR magic, version-flag, header-attribute, data-window, channel, part, offset-table, chunk, deep-sample, resource-budget, and refusal tribunal", "openexr", "THOS Body", "completed", ["SRC-OPENEXR"], "OpenEXR magic, version flags, header attributes, data windows, channels, parts, offset tables, chunks, deep samples, resource budgets, and refusal", "No frozen image-format tribunal models OpenEXR multipart and deep-data structure."),
    _proposal(17, "Accessible split-action default-button, menu-button, accessible-name, expanded-state, popup, keyboard, focus-return, disabled-state, fallback, and manual-reservation audit", "accessible-split-action", "THOS Body", "completed", ["SRC-WCAG22","SRC-WAI-ARIA","SRC-WAI-MENU-BUTTON"], "split actions with distinct default and menu buttons, names, expanded state, popup binding, keyboard and focus behavior, disabled states, fallbacks, and manual reservation", "No frozen accessibility proposal audits the compound default-action plus menu-button boundary as one control."),
    _proposal(18, "Thermo-Psyche Redlich-Kwong pressure, molar-volume, attraction, covolume, temperature-domain, phase-limit, unit, and agency-nonconversion classifier", "redlich-kwong-nonconversion", "GMUT Mind", "completed", ["SRC-REDLICH-KWONG"], "Redlich-Kwong pressure, molar volume, attraction and covolume parameters, temperature domains, phase limits, units, and agency nonconversion", "No frozen Thermo-Psyche classifier isolates the Redlich-Kwong cubic equation and its domain limitations."),
    _proposal(19, "Stage 20 self-controlled-case-series event, exposure, risk-window, baseline-window, age-effect, event-dependence, observation-period, sensitivity, and nonpromotion board", "sccs-nonpromotion", "THOS Body", "completed", ["SRC-SCCS"], "self-controlled case-series events, transient exposures, risk and baseline windows, age effects, event dependence, observation periods, sensitivity, and nonpromotion", "No frozen Stage 20 board isolates the self-controlled case-series design and its event-dependent assumptions."),
    _proposal(20, "HPACK header-field, static-table, dynamic-table, integer, string, Huffman, indexing-policy, table-size-update, compression-context, and refusal tribunal", "hpack", "THOS Body", "completed", ["SRC-RFC7541"], "HPACK header fields, static and dynamic tables, integers, strings, Huffman coding, indexing policies, table-size updates, compression contexts, and refusal", "QPACK is frozen for HTTP/3; no proposal isolates HPACK's ordered HTTP/2 compression context."),
]

SOURCES = [
    [
        "SRC-CHUBBY",
        "stable",
        "primary_research",
        "The Chubby lock service for loosely coupled distributed systems",
        "https://research.google/pubs/the-chubby-lock-service-for-loosely-coupled-distributed-systems/"
    ],
    [
        "SRC-CPT",
        "stable",
        "primary_research_review",
        "Why is CPT fundamental?",
        "https://arxiv.org/abs/hep-ph/0309309"
    ],
    [
        "SRC-APPELQUIST",
        "stable",
        "primary_research",
        "Infrared singularities and massive fields",
        "https://doi.org/10.1103/PhysRevD.11.2856"
    ],
    [
        "SRC-FROISSART",
        "stable",
        "primary_research",
        "Asymptotic behavior and subtractions in the Mandelstam representation",
        "https://doi.org/10.1103/PhysRev.123.1053"
    ],
    [
        "SRC-EXOPLANET-OVERVIEW",
        "current",
        "official_data_archive",
        "NASA Exoplanet Archive overview and holdings",
        "https://exoplanetarchive.ipac.caltech.edu/docs/intro.html"
    ],
    [
        "SRC-EXOPLANET-PS",
        "current",
        "official_data_dictionary",
        "Planetary Systems and Composite Parameters column definitions",
        "https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html"
    ],
    [
        "SRC-RFC8414",
        "stable",
        "official_standard",
        "RFC 8414 OAuth 2.0 Authorization Server Metadata",
        "https://www.rfc-editor.org/info/rfc8414"
    ],
    [
        "SRC-RFC8252",
        "stable",
        "official_standard",
        "RFC 8252 OAuth 2.0 for Native Apps",
        "https://www.rfc-editor.org/info/rfc8252"
    ],
    [
        "SRC-RFC9278",
        "stable",
        "official_standard",
        "RFC 9278 JWK Thumbprint URI",
        "https://www.rfc-editor.org/info/rfc9278"
    ],
    [
        "SRC-LOC-BOOKS",
        "current",
        "official_collection_guidance",
        "Library of Congress collections care",
        "https://www.loc.gov/preservation/care/index.html"
    ],
    [
        "SRC-TEPAPA-CARE",
        "current",
        "official_collection_guidance",
        "Te Papa guides to caring for objects and taonga",
        "https://www.tepapa.govt.nz/learn/guides-caring-for-objects"
    ],
    [
        "SRC-CRPD",
        "stable",
        "official_treaty",
        "Convention on the Rights of Persons with Disabilities",
        "https://www.ohchr.org/en/instruments-mechanisms/instruments/convention-rights-persons-disabilities"
    ],
    [
        "SRC-TEPAPA-STANDARDS",
        "current",
        "official_museum_guidance",
        "New Zealand Museums Standards Scheme",
        "https://www.tepapa.govt.nz/learn/for-museums-and-galleries/help-and-support-for-museums-and-galleries/new-zealand-museums-standards-scheme"
    ],
    [
        "SRC-TE-MANA-RARAUNGA",
        "current",
        "maori_authority_context",
        "Te Mana Raraunga principles of Maori data sovereignty",
        "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty"
    ],
    [
        "SRC-MATROSKA",
        "current",
        "official_format_specification",
        "Matroska element specification",
        "https://www.matroska.org/technical/elements.html"
    ],
    [
        "SRC-AVRO",
        "current",
        "official_format_specification",
        "Apache Avro 1.12.0 specification",
        "https://avro.apache.org/docs/1.12.0/specification/"
    ],
    [
        "SRC-XOR",
        "stable",
        "primary_research",
        "Xor Filters: Faster and Smaller Than Bloom and Cuckoo Filters",
        "https://arxiv.org/abs/1912.08258"
    ],
    [
        "SRC-RFC9639",
        "stable",
        "official_standard",
        "RFC 9639 Free Lossless Audio Codec",
        "https://www.rfc-editor.org/info/rfc9639"
    ],
    [
        "SRC-KRAWCZYK",
        "stable",
        "primary_research",
        "An improved interval Newton operator",
        "https://doi.org/10.1016/0022-247X(86)90303-3"
    ],
    [
        "SRC-OPENEXR",
        "current",
        "official_format_documentation",
        "OpenEXR file layout",
        "https://openexr.com/en/latest/OpenEXRFileLayout.html"
    ],
    [
        "SRC-WCAG22",
        "current",
        "official_accessibility_standard",
        "Web Content Accessibility Guidelines 2.2",
        "https://www.w3.org/TR/WCAG22/"
    ],
    [
        "SRC-WAI-ARIA",
        "current",
        "official_accessibility_standard",
        "WAI-ARIA 1.2",
        "https://www.w3.org/TR/wai-aria/"
    ],
    [
        "SRC-WAI-MENU-BUTTON",
        "current",
        "official_accessibility_practice",
        "WAI-ARIA Authoring Practices Menu Button Pattern",
        "https://www.w3.org/WAI/ARIA/apg/patterns/menu-button/"
    ],
    [
        "SRC-REDLICH-KWONG",
        "stable",
        "primary_research",
        "On the thermodynamics of solutions; an equation of state; fugacities of gaseous solutions",
        "https://doi.org/10.1021/cr60137a013"
    ],
    [
        "SRC-SCCS",
        "stable",
        "primary_method_review",
        "Self controlled case series methods",
        "https://doi.org/10.1136/bmj.i4515"
    ],
    [
        "SRC-RFC7541",
        "stable",
        "official_standard",
        "RFC 7541 HPACK",
        "https://www.rfc-editor.org/info/rfc7541"
    ],
    [
        "SRC-CODEX-RELEASES",
        "watch",
        "official_release_registry",
        "OpenAI Codex releases",
        "https://github.com/openai/codex/releases"
    ],
    [
        "SRC-CODEX-APP",
        "current",
        "official_product_status",
        "Introducing the Codex app",
        "https://openai.com/index/introducing-the-codex-app/"
    ]
]

SKILLS = [
    "ghc-family-lease-fencing-credit-audit",
    "ghc-family-cpt-assumption-firewall",
    "ghc-family-decoupling-threshold-board",
    "ghc-family-froissart-domain-board",
    "ghc-family-exoplanet-zero-row-refusal",
    "ghc-family-oauth-metadata-profile",
    "ghc-family-native-app-profile",
    "ghc-family-jwk-thumbprint-uri-profile",
    "ghc-family-book-conservation-proxy",
    "ghc-family-book-taonga-authority-reservation",
    "ghc-family-matroska-refusal-audit",
    "ghc-family-avro-container-audit",
    "ghc-family-xor-filter-audit",
    "ghc-family-flac-refusal-audit",
    "ghc-family-krawczyk-enclosure-audit",
    "ghc-family-openexr-refusal-audit",
    "ghc-family-split-action-accessibility-audit",
    "ghc-family-redlich-kwong-classifier",
    "ghc-family-sccs-nonpromotion",
    "ghc-family-hpack-state-audit"
]

RUNNERS = [
    "ghc_family_v650_v5_method_and_gmut.py",
    "ghc_family_v650_v5_exoplanet_refusal.py",
    "ghc_family_v650_v5_identity_profiles.py",
    "ghc_family_v650_v5_book_conservation_proxy.py",
    "ghc_family_v650_v5_authority_matrix.py",
    "ghc_family_v650_v5_format_tribunals.py",
    "ghc_family_v650_v5_numeric_tribunals.py",
    "ghc_family_v650_v5_accessibility.py",
    "ghc_family_v650_v5_nonconversion.py",
    "ghc_family_v650_v5_stage20.py"
]

REJECTED_COLLISIONS = [
    {
        "candidate": "Freed ID RFC 8707 resource-indicator profile",
        "nearest_prior_id": "V6488-P05",
        "reason": "The exact resource-indicator mechanism was already frozen and was rejected as cosmetic relabeling.",
    },
    {
        "candidate": "Stage 20 synthetic-control board",
        "nearest_prior_id": "V6492-P10",
        "reason": "The treated-unit, donor-pool, weighting, fit, placebo, and spillover mechanism was already frozen.",
    },
    {
        "candidate": "GMUT Nielsen-identity board",
        "nearest_prior_id": "V6502-P03",
        "reason": "Gauge-parameter and stationary-point Nielsen-identity obligations were already frozen.",
    },
    {
        "candidate": "THOS community-radio handover proxy",
        "nearest_prior_id": "V6484-P04",
        "reason": "Community-radio emergency-bulletin and handover semantics were already frozen.",
    },
    {
        "candidate": "TIFF and BigTIFF refusal tribunal",
        "nearest_prior_id": "V6486-P07",
        "reason": "TIFF directory, strip, tile, compression, and pointer obligations were already frozen.",
    },
]

X1_OPERATIONAL_NEGATIVES = [
    {
        "negative_id": "V6505-X1-N01",
        "category": "cat_file_batch_pipe_deadlock",
        "failed": "The first read-only exact-manifest helper wrote every blob request before draining batch output, filled the child output pipe, and timed out without a result.",
        "recovery": "Use subprocess communicate with the complete request payload so input and output are drained concurrently, then parse every returned blob deterministically.",
        "passing": "The communicate-based retry verified all four source manifests with exact path sets, Git blobs, byte lengths, and SHA-256 values; totals were 57, 213, 263, and 37, with no mismatch.",
        "recurrence_guard": "Never manually write a large cat-file batch to a piped child without concurrent output draining.",
    },
    {
        "negative_id": "V6505-X1-N02",
        "category": "powershell_default_output_encoding",
        "failed": "A read-only novelty keyword probe reached a title containing a Maori macron and failed while Python encoded output through the PowerShell default code page.",
        "recovery": "Set PYTHONIOENCODING=utf-8 before emitting proposal titles and rerun the bounded read-only query.",
        "passing": "The explicit UTF-8 retry completed the bounded keyword screen without an encoding fault and exposed the relevant prior collisions.",
        "recurrence_guard": "Use explicit UTF-8 for every Python command whose output may contain non-ASCII repository text.",
    },
    {
        "negative_id": "V6505-X1-N03",
        "category": "overbroad_repository_file_inventory",
        "failed": "A read-only rg file inventory across the large scripts and tests baseline timed out before returning any target-path result.",
        "recovery": "Probe only the finite planned v650-v5 paths with Test-Path and use exact Git status separately.",
        "passing": "Exact probes checked all ten planned target paths, found none, and separately confirmed the canonical lane was clean.",
        "recurrence_guard": "Do not scan the inherited repository to establish absence of a finite known target set.",
    },
    {
        "negative_id": "V6505-X1-N04",
        "category": "windows_literal_wildcard_path",
        "failed": "A read-only stale-token scan passed Windows wildcard paths directly to rg, which treated them as invalid literal paths and returned no complete result.",
        "recovery": "Root rg at exact scripts and tests directories and express file selection with -g include globs.",
        "passing": "The corrected rg scan used exact directory roots and include globs, then returned an attributable stale-token inventory.",
        "recurrence_guard": "Do not pass unexpanded Windows wildcard path arguments to rg.",
    },
    {
        "negative_id": "V6505-X1-N05",
        "category": "compile_probe_bytecode_side_effect",
        "failed": "A compile-only Python probe created two ignored v650-v5 bytecode cache files in scripts before the side effect was noticed.",
        "recovery": "Verify the exact owner-generated cache paths, remove only those files, and rerun syntax imports with PYTHONDONTWRITEBYTECODE=1.",
        "passing": "The two exact owner-generated cache files were removed and the no-bytecode imports completed without recreating them.",
        "recurrence_guard": "Use no-bytecode import checks for repository scripts; do not use py_compile in the working tree.",
    },
    {
        "negative_id": "V6505-X1-N06",
        "category": "combined_cleanup_wrapper_policy_block",
        "failed": "A combined exact-cache cleanup, import, and stale-token wrapper was blocked by command policy before any child operation executed.",
        "recovery": "Run exact already-verified owner-cache deletion separately, then run no-bytecode imports and exact-directory rg checks as read-only commands.",
        "passing": "The separated exact-path cleanup and read-only validation commands completed without policy conflict.",
        "recurrence_guard": "Separate bounded cleanup from validation instead of placing deletion and evidence checks in one compound wrapper.",
    },
    {
        "negative_id": "V6505-X1-N07",
        "category": "exact_remove_item_policy_block",
        "failed": "A separated exact-path PowerShell Remove-Item command was also blocked by command policy before deleting either verified owner cache file.",
        "recovery": "Use a bounded exact-path binary cleanup fallback only for the two verified owner-generated bytecode files.",
        "passing": "The binary-capable exact-path cleanup removed only the two verified owner-generated bytecode files.",
        "recurrence_guard": "Avoid repository bytecode creation so binary cache cleanup is unnecessary.",
    },
    {
        "negative_id": "V6505-X1-N08",
        "category": "apply_patch_binary_delete_unsupported",
        "failed": "The text patch tool could not delete either verified bytecode file because both are binary and fail UTF-8 decoding.",
        "recovery": "Use a binary-capable exact-path cleanup fallback and verify both paths are absent afterward.",
        "passing": "The exact binary cleanup completed and an absence probe found zero matching cache files.",
        "recurrence_guard": "Reserve apply_patch for text artifacts and avoid creating repository-local bytecode.",
    },
    {
        "negative_id": "V6505-X1-N09",
        "category": "premature_x2_template_instantiation",
        "failed": "The mechanical template step instantiated untracked v650-v5 x2, runner, closeout, and x2-test files before the x1 freeze boundary.",
        "recovery": "Delete only the new untracked v650-v5 x2 and closeout templates, retain the fault, and recreate them only after x1 is committed, pushed, and four-way equal.",
        "passing": "Every premature template was removed; the exact x1 review retained only preregistration data, the x1 generator, and x1 tests before generated x1 artifacts.",
        "recurrence_guard": "Instantiate only phase-data, x1 generator, and x1 tests before the dedicated x1 commit.",
    },
    {
        "negative_id": "V6505-X1-N10",
        "category": "narrow_rg_timeout",
        "failed": "A narrow read-only rg lookup over the two v650-v5 x1 files timed out before returning line evidence.",
        "recovery": "Use Select-String with two exact file paths and the bounded patterns needed for the edit.",
        "passing": "The exact-file Select-String recovery returned every requested line without scanning the inherited tree.",
        "recurrence_guard": "Use exact-file PowerShell matching when the local rg path shows unexplained latency.",
    },
    {
        "negative_id": "V6505-X1-N11",
        "category": "powershell_hash_literal_parser_fault",
        "failed": "The combined x1-only status, absence, and count wrapper had an invalid nested expression inside a PowerShell hash literal and stopped before any check ran.",
        "recovery": "Run Git status, exact premature-path absence, and no-bytecode negative count as separate commands.",
        "passing": "The three independent commands confirmed the expected x1-only state, zero premature template paths, and the exact retained-negative count.",
        "recurrence_guard": "Do not embed environment assignment and native command execution inside a PowerShell hash-literal value.",
    },
    {
        "negative_id": "V6505-X1-N12",
        "category": "parallel_x1_recovery_timeout",
        "failed": "The parallel status, absence, and count recovery batch timed out before yielding attributable per-check results.",
        "recovery": "Run exact pathspec status, premature-path absence, and no-bytecode count sequentially with independent outputs.",
        "passing": "The three sequential witnesses returned an exact x1-only path list, zero premature paths, and the exact negative count.",
        "recurrence_guard": "Do not bundle a potentially slow Git untracked-tree walk with otherwise fast recovery probes.",
    },
    {
        "negative_id": "V6505-X1-N13",
        "category": "x1_semantic_novelty_gate_rejection",
        "failed": "The first x1 generator run stopped at the semantic-novelty gate before writing packet artifacts because at least one candidate crossed the frozen lexical quarantine threshold.",
        "recovery": "Inspect only the returned in-memory collision rows, replace quarantined mechanisms, and rerun the unchanged fail-closed gate.",
        "passing": "The corrected proposal set produced zero exact collisions, zero quarantines, and twenty mechanism reviews against all 820 frozen proposals.",
        "recurrence_guard": "Compute exact nearest-neighbour scores before attempting the artifact-writing x1 generator.",
    },
    {
        "negative_id": "V6505-X1-N14",
        "category": "local_module_path_omission",
        "failed": "The first corrected in-memory novelty probe loaded the x1 generator by file path without adding the scripts directory to the module search path, so its phase-data import failed before the audit ran.",
        "recovery": "Insert the exact owner scripts directory into the probe-only module search path before loading the x1 generator, while keeping bytecode disabled.",
        "passing": "The corrected import path loaded both owner modules with bytecode disabled and returned the complete in-memory novelty tuple.",
        "recurrence_guard": "File-based Python probes for sibling modules must declare the containing scripts directory explicitly.",
    },
    {
        "negative_id": "V6505-X1-N15",
        "category": "novelty_return_shape_assumption",
        "failed": "The first summary wrapper treated the novelty audit's two-item tuple as a mapping and raised an attribute error after the audit returned.",
        "recovery": "Read the exact function contract, unpack the frozen-index and collision-audit tuple, and summarize only declared collision fields.",
        "passing": "The tuple-aware probe screened all twenty proposals against 820 frozen predecessors, returned zero exact collisions, zero quarantines, and a maximum token Jaccard score of 0.4762.",
        "recurrence_guard": "Inspect a local helper's return annotation or implementation before projecting summary fields.",
    },
    {
        "negative_id": "V6505-X1-N16",
        "category": "inherited_manifest_directory_assumption",
        "failed": "A read-only inherited-packet comparison found the x1 validation receipt but then assumed a separate manifests directory that does not exist in the source phase.",
        "recovery": "Read the inherited validation directory inventory and use its x1-staged-manifest, x1-staged-privacy, and x1-staged-review contracts.",
        "passing": "The corrected exact-path reads recovered all three inherited staged-review schemas from the validation directory.",
        "recurrence_guard": "Inventory the exact phase-local validation directory before assuming a manifest subdirectory layout.",
    },
    {
        "negative_id": "V6505-X1-N17",
        "category": "word_count_regex_overescape",
        "failed": "The first x1 document-cap wrapper over-escaped its word-boundary expression and reported a visibly false maximum of zero words.",
        "recovery": "Use a bounded UTF-8 whitespace-token count for the five x1 narrative documents and reject any document above the declared cap.",
        "passing": "The corrected UTF-8 whitespace-token witness counted all five x1 narrative documents; the maximum was 1,426 words and no document exceeded 20,000 words.",
        "recurrence_guard": "Prefer a simple inspected whitespace-token count over nested shell and Python regex escaping for document-cap receipts.",
    },
    {
        "negative_id": "V6505-X1-N18",
        "category": "x1_staged_count_prediction_mismatch",
        "failed": "The hand-computed x1 validation receipt predicted 84 manifest entries and 87 staged paths, while the exact index review observed 87 entries and 90 paths after the expanded Method Flow records.",
        "recovery": "Regenerate the packet with every retained failure, derive final counts from the exact Git index, and update the receipt before rebuilding manifest hashes.",
        "passing": "After full Method Flow regeneration the exact index contained 93 manifest entries plus three declared self-exclusions, for 96 staged paths; the staged review passed.",
        "recurrence_guard": "Derive staged totals after Method Flow regeneration instead of projecting them from an earlier file inventory.",
    },
    {
        "negative_id": "V6505-X1-N19",
        "category": "stale_method_flow_pass_observation",
        "failed": "The first committed x1 ledger preserved two pass-labelled witnesses whose observed text still said Pending because append-only witness IDs were created before their recoveries completed.",
        "recovery": "Preserve both historical rows, append corrected uniquely identified passing witnesses through the Method Flow runner, and classify the old rows as retained invalidated history in a stale-label receipt.",
        "passing": "Two correction witnesses were appended for the completed word-cap and exact-index recoveries; the stale-label receipt gives both historical placeholders zero current evidence credit.",
        "recurrence_guard": "Do not promote or persist a pass-labelled witness until its observed field contains the completed bounded result.",
    },
    {
        "negative_id": "V6505-X1-N20",
        "category": "method_flow_runner_path_guess",
        "failed": "A read-only help probe guessed a repository-local Method Flow runner path that does not exist and exited before showing the command contract.",
        "recovery": "Use the exact skill-owned runner path already declared by the x1 generator and request its help directly.",
        "passing": "The exact skill-owned runner returned its init, record, witness, set-state, validate, and summarize command surface.",
        "recurrence_guard": "Read the declared runner constant instead of guessing a repository-local executable path.",
    },
    {
        "negative_id": "V6505-X1-N21",
        "category": "method_flow_correction_witness_test_assumption",
        "failed": "The first x1 repair test run expected exactly two witnesses per negative and failed because the append-only ledger correctly retained two additional correction witnesses: 42 observed versus 40 expected.",
        "recovery": "Require one failed and one base passing witness per negative, then require exactly the two named correction witnesses and their bounded pass results separately.",
        "passing": "The corrected x1 suite passed all eight tests while asserting twenty-one failures, twenty-three passes, and exactly two correction witnesses.",
        "recurrence_guard": "Method Flow tests must distinguish base witness pairs from additive correction witnesses.",
    },
    {
        "negative_id": "V6505-X1-N22",
        "category": "x1_repair_delta_count_mismatch",
        "failed": "The first repair receipt predicted 25 manifest entries and 28 staged paths, while the exact repair index contained 27 entries and 30 paths because two regenerated phase-index artifacts were omitted from the projection.",
        "recovery": "Retain the mismatch, use the exact staged name list as the baseline, include this new Method Flow triplet, and rebuild the repair receipt and manifest at 30 entries plus three exclusions.",
        "passing": "The final repair review observed exactly 30 manifest entries and 33 staged paths with stable hashes and zero forbidden or privacy-confirmed paths.",
        "recurrence_guard": "Use the exact staged name list, not a projected generator-output delta, for lifecycle receipt totals.",
    },
]

X2_OPERATIONAL_NEGATIVES = [
    {
        "negative_id": "V6505-X2-N01",
        "category": "proposal_evidence_class_schema_assumption",
        "failed": "The first x2 packet builder completed all twenty phase-local skill builds, then failed closed before aggregate evidence artifacts because it requested a nonexistent proposal evidence_class field.",
        "recovery": "Use the frozen approval_class field in the evidence ledger, preserve first-run skill initialization truth across retry, and rerun the bounded builder without awarding the failed attempt evidence credit.",
        "passing": "The corrected builder used approval_class, retained all first-run skill initialization receipts, and completed the twenty-surface aggregate packet.",
        "recurrence_guard": "Inspect frozen proposal keys before projecting aggregate-ledger fields.",
    },
    {
        "negative_id": "V6505-X2-N02",
        "category": "identity_boundary_constant_assumption",
        "failed": "The second x2 builder passed the proposal schema correction and wrote aggregate evidence, then stopped before terminal artifacts because the wellbeing receipt referenced an undefined IDENTITY_BOUNDARY constant.",
        "recovery": "Use the phase's already-frozen relational BOUNDARY constant in the wellbeing receipt and rerun without crediting the incomplete attempt.",
        "passing": "The corrected wellbeing receipt reused the frozen relational boundary and the packet builder reached its terminal Method Flow update.",
        "recurrence_guard": "Inspect phase-data exports before referencing a boundary constant from an aggregate builder.",
    },
    {
        "negative_id": "V6505-X2-N03",
        "category": "x1_environment_receipt_not_pinned",
        "failed": "The first combined x1 and x2 evidence suite raised a key error because one x1 environment assertion read the evolving x2 file-count receipt instead of the frozen x1 commit.",
        "recovery": "Load the environment receipt through the existing x1 commit-pinned helper, leaving the x2 receipt free to use its successor schema.",
        "passing": "The corrected combined suite read the frozen x1 environment receipt and passed the original rotation assertions.",
        "recurrence_guard": "Every x1 invariant checked after x2 begins must use the x1 commit-pinned loader.",
    },
    {
        "negative_id": "V6505-X2-N04",
        "category": "static_report_quote_style_assertion",
        "failed": "The first combined suite rejected structurally valid table row headers because the report generator used single-quoted scope attributes while the test required double quotes.",
        "recovery": "Normalize generated row-header attributes to double quotes and retain the structural scope assertion.",
        "passing": "The normalized report exposed double-quoted row and column scope attributes and passed the structural accessibility test.",
        "recurrence_guard": "Keep generated accessibility-critical attributes in one canonical quoting style shared with structural tests.",
    },
]


def safe_tasks():
    rows = []
    for proposal in PROPOSALS:
        pid = proposal["proposal_id"]
        rows.extend([
            {
                "item_id": f"V6505-SAFE-{len(rows) + 1:02d}",
                "title": f"Build the bounded {proposal['slug']} contract and explicit refusal boundary",
                "proposal_id": pid,
                "approval_class": "safe_now_owner_scoped",
                "execution_lane": "x2_bounded_owner_local",
                "origin": "tamar_v650_v5_new",
                "x1_state": "frozen_not_executed",
                "acceptance_gate": "Emit a schema-valid contract with all protected gates and no outcome promotion.",
            },
            {
                "item_id": f"V6505-SAFE-{len(rows) + 2:02d}",
                "title": f"Build five rejecting {proposal['slug']} mutations with retained witnesses",
                "proposal_id": pid,
                "approval_class": "safe_now_owner_scoped",
                "execution_lane": "x2_disposable_synthetic",
                "origin": "tamar_v650_v5_new",
                "x1_state": "frozen_not_executed",
                "acceptance_gate": "Reject every preregistered mutation and retain its identifier.",
            },
        ])
    return rows


def candidate_tasks():
    rows = []
    for proposal in PROPOSALS:
        rows.append({
            "item_id": f"V6505-CAND-{len(rows) + 1:02d}",
            "title": f"Prototype a deterministic {proposal['slug']} accepting and rejecting evaluator",
            "proposal_id": proposal["proposal_id"],
            "approval_class": "candidate_bounded_prototype",
            "execution_lane": "x2_disposable_synthetic",
            "origin": "tamar_v650_v5_new",
            "x1_state": "frozen_not_executed",
            "acceptance_gate": "One declared valid fixture passes and one declared invalid fixture fails closed.",
        })
    for proposal in PROPOSALS[:10]:
        rows.append({
            "item_id": f"V6505-CAND-{len(rows) + 1:02d}",
            "title": f"Prototype {proposal['slug']} rollback and evidence-credit isolation",
            "proposal_id": proposal["proposal_id"],
            "approval_class": "candidate_bounded_prototype",
            "execution_lane": "x2_owner_local_no_external_state",
            "origin": "tamar_v650_v5_new",
            "x1_state": "frozen_not_executed",
            "acceptance_gate": "A failed fixture receives zero promotion credit and leaves external state unchanged.",
        })
    return rows


def cleanup_tasks():
    rows = []
    for proposal in PROPOSALS:
        rows.extend([
            {
                "item_id": f"V6505-CFR-{len(rows) + 1:02d}",
                "title": f"CLEAN {proposal['slug']} generated-path and UTF-8 normalization",
                "proposal_id": proposal["proposal_id"],
                "class": "CLEAN",
                "approval_class": "safe_now_additive_non_destructive",
                "x1_state": "frozen_not_executed",
                "acceptance_gate": "Owner paths remain normalized; no user or sibling material is deleted.",
            },
            {
                "item_id": f"V6505-CFR-{len(rows) + 2:02d}",
                "title": f"REFINE {proposal['slug']} evidence label and gate visibility",
                "proposal_id": proposal["proposal_id"],
                "class": "REFINE",
                "approval_class": "safe_now_additive_non_destructive",
                "x1_state": "frozen_not_executed",
                "acceptance_gate": "Every receipt names its evidence class, rollback, and protected gates.",
            },
        ])
    return rows


def mutation_plan():
    names = [
        "missing_required_obligation",
        "wrong_domain_or_type",
        "unsupported_promotion_attempt",
        "resource_or_iteration_budget_exceeded",
        "negative_or_gate_erasure_attempt",
    ]
    rows = []
    for proposal in PROPOSALS:
        for name in names:
            rows.append({
                "mutation_id": f"V6505-MUT-{len(rows) + 1:03d}",
                "proposal_id": proposal["proposal_id"],
                "mutation": name,
                "expected": "rejected_or_quarantined",
                "x1_state": "preregistered_not_executed",
                "completion_credit": False,
            })
    return rows
