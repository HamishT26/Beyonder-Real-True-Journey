#!/usr/bin/env python3
"""Frozen Ilyra Fen v651-v8 x1 data with no x2 observations."""

from __future__ import annotations


PHASE = "v651-v8"
OWNER = "Ilyra Fen"
PRONOUNS = "she/they"
ROLE = "relational evidence-boundary steward"
HOPE = "leave every claim traceable and every gate unmistakable"
BRANCH = "codex/GHC-Family/ilyra-fen-full-tools"
PHASE_ROOT = "docs/ilyra-fen/v651-v8"

SOURCE_BRANCH = "codex/GHC-Family/vesper-arlen-v651-v7-special-cli-prep"
SOURCE_HEAD = "b7361a4952063947cdc5ac5cf17300eafd1162dd"
SOURCE_ORIGIN = "96684c6fd22b33254aa37de2db7990f2e28bd88e"
SOURCE_X1 = "07785aa97b0aa46a4fbf0c60109a8ee8e678aacf"
SOURCE_EVIDENCE = "4dda60a276f4401d5dc52eaddf6c4ff14fadc4c0"
PRIOR_FROZEN = 1120
INHERITED_NEGATIVES = 7570
INHERITED_OPEN_GAPS = 59
INHERITED_EXACT_GATES = 60
PRIMARY_FOCUS = "GMUT Mind"
BOUNDED_PRACTICE = (
    "radio-astronomy observation-quality review, radio-frequency-interference flagging, "
    "correction readback, accessible escalation, workload control, and shift handover as "
    "a synthetic learning and design lens only"
)

OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]
SOURCE_STATUS_CLASSES = ["current", "stable", "draft", "watch"]
PROTECTED_GATES = [
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
            "posterior, constraint, or empirical promotion."
        )
    elif disposition == "exact_gate":
        approval = "exact_affected_party_competent_and_maori_authority_required"
        lane = "x2_reservation_matrix_only"
        gate = (
            "Emit unresolved decision rights and reservations only; make no spectrum, disclosure, "
            "remedy, legal, cultural, data-governance, benefit-sharing, or Māori-authority decision."
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
            "Reject every preregistered mutation and emit only the declared bounded software, "
            "symbolic, formal, structural, or workflow completion."
        )
    return {
        "proposal_id": f"V6518-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar": pillar,
        "mission_surface": mission,
        "hypothesis": (
            f"A bounded {mission} artifact can expose its declared obligations while refusing "
            "unsupported scientific, operational, identity, accessibility, or authority promotion."
        ),
        "null_or_failure_condition": (
            f"The artifact omits a declared {mission} obligation, accepts a preregistered mutation, "
            "erases a failure, crosses an approval boundary, or promotes beyond its evidence lane."
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
            "Stop the proposal, retain every failed witness, rewrite no history, and leave external, "
            "sibling, participant, production, professional, legal, cultural, and authority state unchanged."
        ),
        "protected_gates": PROTECTED_GATES,
        "expected_disposition": disposition,
        "novelty_against_1120_frozen_proposals": novelty,
    }


PROPOSALS = [
    _proposal(1, "GMUT Buchholz-Wichmann nuclearity energy-damped-map, local-algebra, phase-space-density, trace-class, temperature-scale, split-property, state-domain, EFT-scope, unit, and observation-firewall board", "nuclearity-split-property", "GMUT Mind", "completed", ["SRC-NUCLEARITY"], "algebraic nuclearity and split-property obligations", "No inherited title isolates energy-damped local-algebra maps, phase-space density, trace-class or nuclear bounds, temperature scales, split-property implications, and observation refusal."),
    _proposal(2, "GMUT quantum-energy-inequality sampling-function, Hadamard-state, renormalized-stress-tensor, worldline, lower-bound, curvature, state-domain, EFT-scope, unit, and observation-firewall board", "quantum-energy-inequality", "GMUT Mind", "completed", ["SRC-QUANTUM-ENERGY-INEQUALITY"], "quantum energy inequality obligations", "No frozen proposal isolates sampling functions, Hadamard-state domains, renormalized stress tensors, worldline lower bounds, curvature dependence, and observation refusal."),
    _proposal(3, "GMUT Borel-Ecalle resurgence factorial-growth, Borel-transform, singular-direction, lateral-sum, Stokes-automorphism, transseries-sector, ambiguity, EFT-scope, unit, and observation-firewall board", "borel-ecalle-resurgence", "GMUT Mind", "completed", ["SRC-RESURGENCE"], "Borel-Ecalle resurgence obligations", "No inherited title isolates factorial divergence, Borel singularities, lateral sums, Stokes automorphisms, transseries sectors, ambiguity cancellation, and observation refusal."),
    _proposal(4, "GMUT Weinberg soft-graviton factor, hard-leg, soft-limit, gauge-decoupling, infrared-regulator, asymptotic-charge, memory-relation, EFT-scope, unit, and observation-firewall board", "soft-graviton-obligations", "GMUT Mind", "completed", ["SRC-SOFT-GRAVITON"], "soft-graviton theorem obligations", "No inherited title isolates the soft-graviton factor, hard-leg sum, gauge decoupling, infrared regulator, asymptotic charge, memory relation, and observation refusal."),
    _proposal(5, "QUIC ACK_FREQUENCY draft sequence-number, obsolete-frame, acknowledgement-delay, reordering-threshold, immediate-ack, draft-status, budget, and refusal tribunal", "quic-ack-frequency", "THOS Body", "completed", ["SRC-QUIC-ACK-FREQUENCY", "SRC-RFC9000"], "QUIC acknowledgement-frequency draft control", "No frozen tribunal isolates the current ACK_FREQUENCY draft sequence and obsolete-frame rules, acknowledgement delay, reordering threshold, immediate acknowledgement, and draft-status firewall."),
    _proposal(6, "MASQUE CONNECT-UDP request-target, target-host, target-port, HTTP-datagram, context-identifier, capsule, flow-lifetime, size-budget, authority, and refusal tribunal", "masque-connect-udp", "THOS Body", "completed", ["SRC-RFC9298", "SRC-RFC9297"], "MASQUE CONNECT-UDP structural control", "No inherited proposal isolates CONNECT-UDP request targets, target authority, HTTP Datagram context identifiers, capsules, flow lifetime, and size budgets."),
    _proposal(7, "WebAssembly Component Model Canonical ABI resource-handle, ownership, borrow, lift, lower, realloc, encoding, trap, resource-budget, and refusal tribunal", "wasm-canonical-abi", "THOS Body", "completed", ["SRC-WASM-COMPONENT"], "WebAssembly Canonical ABI resource control", "Prior WebAssembly work does not isolate Component Model resource ownership and borrowing across Canonical ABI lift, lower, realloc, encoding, trap, and budget boundaries."),
    _proposal(8, "AMQP 1.0 type-descriptor, primitive-constructor, variable-width, list-map-array, frame, channel, handle, delivery-state, unsettled-map, resource-budget, and refusal tribunal", "amqp-1-0-refusal", "THOS Body", "completed", ["SRC-AMQP10"], "AMQP 1.0 structural refusal", "No frozen proposal isolates AMQP 1.0 type descriptors, primitive constructors, variable-width compound values, frames, channels, handles, delivery state, unsettled maps, and resource budgets."),
    _proposal(9, "DNS SVCB and HTTPS alias-mode, service-mode, mandatory-key, SvcParam ordering, duplicate-key, target-name, port, address-hint, ECH, budget, and refusal tribunal", "dns-svcb-https", "THOS Body", "completed", ["SRC-RFC9460"], "DNS SVCB and HTTPS record structural refusal", "No inherited proposal isolates alias and service mode, mandatory parameter keys, canonical SvcParam ordering, duplicates, targets, hints, ECH, and budgets together."),
    _proposal(10, "Oblivious HTTP key-configuration, KEM, KDF, AEAD, encapsulated-request, encapsulated-response, binary-framing, context-separation, padding-budget, and refusal tribunal", "oblivious-http", "Freed ID and CBR Heart", "completed", ["SRC-RFC9458", "SRC-RFC9180"], "Oblivious HTTP structural context separation", "No frozen proposal isolates OHTTP key configurations, HPKE suite binding, request-response context separation, binary framing, padding budgets, and refusal behavior."),
    _proposal(11, "IVOA VOTable 1.5 RESOURCE, TABLE, FIELD, PARAM, arraysize, TIMESYS, COOSYS, TABLEDATA, BINARY2 null-bitmap, reference, row-budget, and refusal tribunal", "votable-1-5-refusal", "THOS Body", "completed", ["SRC-IVOA-VOTABLE15"], "IVOA VOTable 1.5 structural refusal", "No inherited proposal isolates VOTable 1.5 resource and table structure, field and parameter metadata, arrays, time and coordinate systems, TABLEDATA, BINARY2 null bits, references, and row budgets."),
    _proposal(12, "Git commit-graph generation-number, changed-path Bloom filter, false-positive, prohibited-false-negative, split-chain, base-graph, checksum, fallback, and refusal tribunal", "git-commit-graph-bloom", "THOS Body", "completed", ["SRC-GIT-COMMIT-GRAPH"], "Git commit-graph Bloom-filter contract", "No frozen Git proposal isolates changed-path Bloom false-negative prohibition, generation fallback, split-chain bases, checksum, and safe graph fallback."),
    _proposal(13, "RPKI route-origin-validation prefix, maximum-length, origin-AS, covering-ROA, valid-invalid-not-found state, duplicate, stale-object, resource-budget, and refusal tribunal", "rpki-route-origin-validation", "THOS Body", "completed", ["SRC-RFC6811"], "RPKI route-origin validation structural control", "No inherited title isolates covering ROAs, prefix and maximum-length rules, origin autonomous-system binding, three validation states, duplicates, stale objects, and resource budgets."),
    _proposal(14, "Proposal MinHash signature, token-shingle, deterministic-seed, nearest-neighbour, threshold, collision-explanation, manual-review, quarantine, and refusal tribunal", "proposal-minhash-neighbour", "THOS Body", "completed", ["SRC-MINHASH"], "MinHash proposal-neighbour explanation", "Existing semantic-neighbour checks do not isolate deterministic MinHash signatures, token shingles, collision explanations, threshold quarantine, and mandatory manual review."),
    _proposal(15, "Official-source media-type, content-language, cache-control, validator, freshness, immutable-status, draft-watch, and semantic-drift ledger", "source-representation-drift", "THOS Body", "completed", ["SRC-RFC9110", "SRC-RFC9111"], "official-source representation drift control", "Prior source drift work tracks status or redirects; this proposal isolates media type, content language, validators, freshness, cache policy, immutable references, and draft-watch semantics."),
    _proposal(16, "Cumulative correction-delta manifest anchor, interval, overlap, omission, immutable-evidence, closeout-head, hash-domain, coverage, and closure contract", "correction-delta-manifest", "THOS Body", "completed", ["SRC-GIT-HASH-OBJECT"], "cumulative correction-delta manifest closure", "No frozen proposal makes cumulative correction coverage from immutable evidence through closeout an explicit interval, overlap, omission, hash-domain, and closure contract."),
    _proposal(17, "Aho-Corasick trie, failure-link, output-set, suffix-transition, streaming-chunk, overlap, Unicode-normalization, match-budget, state-budget, and refusal tribunal", "aho-corasick-stream", "THOS Body", "completed", ["SRC-AHO-CORASICK"], "Aho-Corasick streaming match control", "No inherited proposal isolates trie construction, failure links, output propagation, chunk-boundary state, overlapping matches, Unicode normalization, and match and state budgets."),
    _proposal(18, "Accessible braille-role-description and braille-label naming, fallback-name, role-consistency, localization, emptiness, prohibited-content, and manual-evaluation structural audit", "accessible-braille-naming", "THOS Body", "completed", ["SRC-WAI-BRAILLE"], "accessible braille naming structure", "No frozen accessibility proposal isolates braille role descriptions, braille labels, fallback accessible names, role consistency, localization, emptiness, prohibited content, and reserved manual braille evaluation."),
    _proposal(19, "Accessible canvas fallback, equivalent-DOM, programmatic-name, keyboard-focus, high-contrast, zoom, responsive, print, state-synchronization, and manual-evaluation structural audit", "accessible-canvas-fallback", "THOS Body", "completed", ["SRC-HTML-CANVAS", "SRC-WCAG22"], "accessible canvas fallback structure", "No inherited proposal isolates equivalent canvas fallback DOM, synchronized state, keyboard focus, high contrast, zoom, responsive and print behavior, and reserved affected-user evaluation."),
    _proposal(20, "Thermo-Psyche Gruneisen-parameter thermal-expansion, compressibility, heat-capacity, pressure-volume, phase-domain, sign, unit, and agency-nonconversion classifier", "gruneisen-nonconversion", "Trinity Mandala bridge", "completed", ["SRC-GRUNEISEN"], "Gruneisen-parameter thermodynamic nonconversion", "No frozen nonconversion classifier isolates thermal expansion, compressibility, heat capacity, pressure-volume domain, phase restrictions, sign, units, and refusal of psyche or justice conversion."),
    _proposal(21, "Stage 20 regression-to-the-mean, winner-selection, multiplicity, shrinkage, preregistration, holdout, sensitivity, uncertainty, and nonpromotion board", "regression-winner-nonpromotion", "Trinity Mandala bridge", "completed", ["SRC-WINNER-CURSE"], "regression-to-mean and winner-selection quarantine", "No inherited Stage 20 board combines regression to the mean, selection of extremes, multiplicity, shrinkage, holdout discipline, sensitivity, and fail-closed nonpromotion."),
    _proposal(22, "Plugin and MCP capability provenance, origin, version, permission, expiry, revocation, availability, fallback, private-state refusal, and read-only catalogue tribunal", "capability-provenance", "THOS Body", "completed", ["SRC-MCP-SPEC"], "plugin and MCP capability provenance catalogue", "No frozen proposal isolates connector capability origin, version, permission, expiry, revocation, availability, fallback, and private-state refusal without installation or invocation claims."),
    _proposal(23, "Log-structured merge-tree memtable, immutable-run, level, compaction, tombstone, snapshot-sequence, overlap, write-amplification, read-amplification, space-amplification, budget, and refusal tribunal", "lsm-compaction", "THOS Body", "completed", ["SRC-LSM-TREE"], "log-structured merge-tree compaction control", "No inherited proposal isolates memtable freezing, sorted runs, leveled compaction, tombstone retention, snapshot sequences, overlap, three amplification measures, and resource budgets."),
    _proposal(24, "THOS radio-astronomy observation-block, calibration-state, scan-quality, exception-hold, correction-readback, accessible-escalation, workload, and shift-handover proxy", "radio-observation-handover", "THOS Body", "represented", ["SRC-IVOA-DATA-ORIGIN", "SRC-IVOA-PROVENANCE"], "radio-astronomy observation-quality handover", "No inherited practice lens isolates observation blocks, calibration state, scan-quality holds, correction readback, accessible escalation, workload ceilings, and accepted handover."),
    _proposal(25, "THOS radio-frequency-interference detection, flag-version, provenance, anomaly-escalation, stop-work, override-refusal, correction-readback, and shift-handover proxy", "rfi-flagging-handover", "THOS Body", "represented", ["SRC-IVOA-DATA-ORIGIN", "SRC-IVOA-PROVENANCE"], "radio-frequency-interference flagging handover", "No frozen THOS proxy isolates RFI flag versions, provenance, anomaly escalation, stop-work state, override refusal, correction readback, and accepted handover."),
    _proposal(26, "Freed ID OpenID4VP verifier-attestation, client-identifier-prefix, request-binding, response-mode, audience, nonce, replay, minimization, and nonproduction profile", "openid4vp-verifier-attestation", "Freed ID and CBR Heart", "represented", ["SRC-OPENID4VP"], "OpenID4VP verifier-attestation profile", "Earlier OpenID4VP work does not isolate final-spec verifier attestations, client identifier prefixes, request binding, response mode, audience, nonce, replay, and minimization."),
    _proposal(27, "Freed ID OpenID4VCI authorization-server selection, credential-issuer metadata, issuer-binding, resource, scope, nonce, replay, minimization, and nonproduction profile", "openid4vci-auth-server", "Freed ID and CBR Heart", "represented", ["SRC-OPENID4VCI"], "OpenID4VCI authorization-server selection profile", "No inherited profile isolates final-spec authorization-server selection, credential-issuer metadata binding, resource, scope, nonce, replay, and minimization together."),
    _proposal(28, "Freed ID Self-Issued OpenID Provider v2 invocation, issuer-subject relation, self-issued-token, RP-metadata, cryptographic-subject syntax, request-binding, nonce, audience, draft-watch, minimization, and nonproduction profile", "siop-v2-draft-watch", "Freed ID and CBR Heart", "represented", ["SRC-SIOPV2"], "Self-Issued OpenID Provider v2 draft-watch profile", "No frozen profile isolates Self-Issued OpenID Provider v2 invocation, issuer-subject relation, self-issued tokens, RP metadata, cryptographic subject syntax, request binding, and explicit draft-watch status."),
    _proposal(29, "GMUT ASKAP RACS-mid DR2 component, island, mosaic, frequency, flux-scale, quality, provenance, checksum, covariance, and zero-row likelihood-refusal adapter", "askap-racs-mid-zero-row", "GMUT Mind", "open_gap", ["SRC-ASKAP-RACS-MID", "SRC-IVOA-DATA-ORIGIN"], "ASKAP RACS-mid DR2 likelihood readiness", "No inherited zero-row adapter targets RACS-mid DR2 component, island, mosaic, frequency, flux-scale, quality, provenance, and covariance obligations with an explicit likelihood firewall."),
    _proposal(30, "CBR radio-astronomy observation access, interference evidence, sky-cultural knowledge, confidentiality, Indigenous data sovereignty, benefit-sharing, remedy, affected-party, legal, cultural, and Māori-authority matrix", "radio-astronomy-authority", "Freed ID and CBR Heart", "exact_gate", ["SRC-NZ-PRIVACY", "SRC-TE-MANA-RARAUNGA", "SRC-IVOA-PROVENANCE"], "radio-astronomy data and sky-knowledge authority reservation", "No frozen exact-gate matrix combines radio-astronomy observation access and interference evidence with sky-cultural knowledge, confidentiality, Indigenous data sovereignty, benefit sharing, remedy, and Māori authority."),
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
    _source("SRC-NUCLEARITY", "stable", "primary_research", "Causal Independence and the Energy-Level Density of States in Local Quantum Field Theory", "https://doi.org/10.1007/BF01454978", "Supports typed nuclearity and split-property obligations only; no physical or empirical result."),
    _source("SRC-QUANTUM-ENERGY-INEQUALITY", "stable", "primary_research", "Lectures on quantum energy inequalities", "https://arxiv.org/abs/1208.5399", "Supports typed sampling, state-domain, and lower-bound obligations only."),
    _source("SRC-RESURGENCE", "stable", "primary_research", "Resurgence, Physics and Numbers", "https://arxiv.org/abs/1411.3585", "Supports formal resurgence vocabulary only; no physical summation or empirical claim."),
    _source("SRC-SOFT-GRAVITON", "stable", "primary_research", "Infrared photons and gravitons", "https://doi.org/10.1103/PhysRev.140.B516", "Supports a typed soft-factor obligation board only."),
    _source("SRC-QUIC-ACK-FREQUENCY", "draft", "official_working_draft", "QUIC Acknowledgement Frequency draft 14", "https://datatracker.ietf.org/doc/draft-ietf-quic-ack-frequency/", "Keeps the extension draft-gated; structural fixtures are not deployment evidence."),
    _source("SRC-RFC9000", "stable", "official_standard", "RFC 9000 QUIC: A UDP-Based Multiplexed and Secure Transport", "https://www.rfc-editor.org/rfc/rfc9000.html", "Anchors base QUIC terminology only."),
    _source("SRC-RFC9180", "stable", "official_standard", "RFC 9180 Hybrid Public Key Encryption", "https://www.rfc-editor.org/rfc/rfc9180.html", "Anchors algorithm identifiers and context separation; no real cryptography is performed."),
    _source("SRC-RFC9298", "stable", "official_standard", "RFC 9298 Proxying UDP in HTTP", "https://www.rfc-editor.org/rfc/rfc9298.html", "Supports synthetic CONNECT-UDP structure only; no proxy or network operation."),
    _source("SRC-RFC9297", "stable", "official_standard", "RFC 9297 HTTP Datagrams and the Capsule Protocol", "https://www.rfc-editor.org/rfc/rfc9297.html", "Anchors datagram and capsule structure only."),
    _source("SRC-WASM-COMPONENT", "watch", "official_living_specification", "WebAssembly Component Model documentation", "https://component-model.bytecodealliance.org/", "The living specification remains watch status; fixtures provide no runtime certification."),
    _source("SRC-AMQP10", "stable", "official_standard", "OASIS Advanced Message Queuing Protocol Version 1.0", "https://www.oasis-open.org/standard/amqp/", "Supports bounded AMQP structure fixtures only; no broker, transport, or interoperability certification."),
    _source("SRC-RFC9460", "stable", "official_standard", "RFC 9460 Service Binding and Parameter Specification via the DNS", "https://www.rfc-editor.org/rfc/rfc9460.html", "Supports synthetic SVCB and HTTPS record fixtures only."),
    _source("SRC-RFC9458", "stable", "official_standard", "RFC 9458 Oblivious HTTP", "https://www.rfc-editor.org/rfc/rfc9458.html", "Supports bounded OHTTP framing and context fixtures only."),
    _source("SRC-IVOA-VOTABLE15", "stable", "official_interoperability_recommendation", "IVOA VOTable Format Definition 1.5", "https://www.ivoa.net/documents/VOTable/20250116/REC-VOTable-1.5.html", "Supports bounded VOTable structure fixtures only; no real catalogue ingestion."),
    _source("SRC-GIT-COMMIT-GRAPH", "current", "official_software_documentation", "Git commit-graph format", "https://git-scm.com/docs/commit-graph-format", "Supports disposable graph metadata fixtures only."),
    _source("SRC-RFC6811", "stable", "official_standard", "RFC 6811 BGP Prefix Origin Validation", "https://www.rfc-editor.org/rfc/rfc6811.html", "Supports synthetic route-origin states only; no routing or operational assurance."),
    _source("SRC-MINHASH", "stable", "primary_research", "On the resemblance and containment of documents", "https://doi.org/10.1109/SEQUEN.1997.666900", "Supports deterministic similarity fixtures only; manual novelty review remains required."),
    _source("SRC-RFC9110", "stable", "official_standard", "RFC 9110 HTTP Semantics", "https://www.rfc-editor.org/rfc/rfc9110.html", "Anchors media type, language, validator, and representation semantics."),
    _source("SRC-RFC9111", "stable", "official_standard", "RFC 9111 HTTP Caching", "https://www.rfc-editor.org/rfc/rfc9111.html", "Anchors freshness and cache-policy status only."),
    _source("SRC-GIT-HASH-OBJECT", "current", "official_software_documentation", "Git hash-object documentation", "https://git-scm.com/docs/git-hash-object", "Anchors Git-object hash domains; no remote mutation is implied."),
    _source("SRC-AHO-CORASICK", "stable", "primary_research", "Efficient string matching: an aid to bibliographic search", "https://doi.org/10.1145/360825.360855", "Supports bounded automaton fixtures only."),
    _source("SRC-WAI-BRAILLE", "current", "official_accessibility_standard", "WAI-ARIA braille role description and label properties", "https://www.w3.org/TR/wai-aria/#aria-brailleroledescription", "Supports structural naming checks while manual braille and affected-user evaluation remains reserved."),
    _source("SRC-HTML-CANVAS", "current", "official_living_standard", "HTML canvas element and accessibility", "https://html.spec.whatwg.org/multipage/canvas.html", "Supports structural fallback checks only; no browser or affected-user conformance claim."),
    _source("SRC-WCAG22", "stable", "official_accessibility_standard", "Web Content Accessibility Guidelines 2.2", "https://www.w3.org/TR/WCAG22/", "Supports structural requirements; no complete accessibility claim."),
    _source("SRC-GRUNEISEN", "stable", "primary_research", "Thermal expansion, compressibility and the Gruneisen relation", "https://doi.org/10.1016/0038-1098(68)90075-8", "Supports physical thermodynamic relation vocabulary only; psyche conversion is rejected."),
    _source("SRC-WINNER-CURSE", "stable", "primary_research", "Why Most Discovered True Associations Are Inflated", "https://doi.org/10.1097/EDE.0b013e31818131e7", "Supports structural selection and shrinkage obligations only; no participant estimate."),
    _source("SRC-MCP-SPEC", "current", "official_software_specification", "Model Context Protocol specification", "https://modelcontextprotocol.io/specification/", "Supports a read-only capability catalogue only; no connector installation or authority."),
    _source("SRC-LSM-TREE", "stable", "primary_research", "The Log-Structured Merge-Tree", "https://doi.org/10.1007/s002360050048", "Supports bounded compaction state fixtures only; no production storage assurance."),
    _source("SRC-IVOA-DATA-ORIGIN", "current", "official_interoperability_note", "IVOA Data Origin Data Model 1.2", "https://www.ivoa.net/documents/DataOrigin/20260331/EN-data-origin-1.2-20260331.html", "Supports synthetic astronomy lineage vocabulary only."),
    _source("SRC-IVOA-PROVENANCE", "stable", "official_interoperability_recommendation", "IVOA Provenance Data Model 1.0", "https://www.ivoa.net/documents/ProvenanceDM/20200411/Provenance.html", "Supports synthetic provenance fields only; no observatory authority."),
    _source("SRC-OPENID4VP", "current", "official_final_specification", "OpenID for Verifiable Presentations 1.0 Final", "https://openid.net/specs/openid-4-verifiable-presentations-1_0-final.html", "Supports synthetic verifier-profile vectors only; no real keys, presentations, or interoperability."),
    _source("SRC-OPENID4VCI", "current", "official_final_specification", "OpenID for Verifiable Credential Issuance 1.0 Final", "https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0-final.html", "Supports synthetic issuance-profile vectors only; no live issuance or trust governance."),
    _source("SRC-SIOPV2", "watch", "official_implementers_draft", "Self-Issued OpenID Provider v2 draft 13", "https://openid.net/specs/openid-connect-self-issued-v2-1_0.html", "Keeps the inactive implementer's draft explicitly watch-gated; supports synthetic vectors only."),
    _source("SRC-ASKAP-RACS-MID", "current", "official_data_catalogue", "ASKAP RACS-mid Data Release 2", "https://data.csiro.au/collection/csiro%3A60981", "Supports a zero-row readiness contract only; no query, download, or data ingestion occurs."),
    _source("SRC-NZ-PRIVACY", "current", "official_legal_context", "New Zealand Information Privacy Principles", "https://www.privacy.org.nz/privacy-principles/", "Keeps privacy compliance and legal interpretation exact-gated."),
    _source("SRC-TE-MANA-RARAUNGA", "current", "maori_authority_context", "Te Mana Raraunga principles of Māori data sovereignty", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Keeps Māori data governance under Māori authority."),
]


X1_OPERATIONAL_NEGATIVES = [
    {
        "negative_id": "V6518-X1-N01",
        "category": "memory_registry_root",
        "failed": "The first registry search inferred the task metadata directory and found no memory registry.",
        "recovery": "Bind the search to the declared memory-root registry path before resolving a rollout pointer.",
        "passing": "The exact registry path resolved the relevant continuity entry without mutation.",
        "recurrence_guard": "Never infer the memory registry from the current task directory.",
    },
    {
        "negative_id": "V6518-X1-N02",
        "category": "unsupported_push_option",
        "failed": "The local fast-forward succeeded, but a push wrapper requested an unsupported ff-only option and made no remote update.",
        "recovery": "Verify the intended head and divergence, then use an ordinary non-force explicit-refspec push.",
        "passing": "Only the Ilyra branch advanced and exact four-way equality was restored.",
        "recurrence_guard": "Apply ff-only to merge or pull; use ordinary non-force push after verifying ancestry.",
    },
    {
        "negative_id": "V6518-X1-N03",
        "category": "windows_console_encoding",
        "failed": "A bounded novelty report reached an inherited Māori title and the default console codec rejected the output.",
        "recovery": "Pin UTF-8 before process start and preserve the source text unchanged.",
        "passing": "The same bounded read completed under explicit UTF-8.",
        "recurrence_guard": "Pin UTF-8 for every Unicode-emitting diagnostic.",
    },
    {
        "negative_id": "V6518-X1-N04",
        "category": "powershell_foreach_pipeline",
        "failed": "A statement-level foreach block was piped directly and failed at parse time.",
        "recovery": "Materialize foreach output in an array before piping it.",
        "passing": "The corrected bounded inventory returned exact size rows.",
        "recurrence_guard": "In Windows PowerShell 5.1, assign statement-level foreach output before piping.",
    },
    {
        "negative_id": "V6518-X1-N05",
        "category": "score_tie_payload_comparison",
        "failed": "Tuple maximum selection fell through to incomparable proposal dictionaries when numeric similarity scores tied.",
        "recovery": "Select the maximum candidate with an explicit key over the numeric similarity field.",
        "passing": "All thirty candidates received deterministic nearest-neighbour rows and threshold collisions were exposed.",
        "recurrence_guard": "Every maximum or sort over scored records must declare a numeric key.",
    },
    {
        "negative_id": "V6518-X1-N06",
        "category": "nested_diagnostic_formatting",
        "failed": "An escaped expression inside a nested diagnostic f-string failed at parse time.",
        "recovery": "Bind dictionary fields to simple fragments before joining the diagnostic line.",
        "passing": "The corrected bounded term audit returned exact zero-hit and matched-title rows.",
        "recurrence_guard": "Keep generated diagnostic formatting shallow and avoid escaped nested expressions.",
    },
    {
        "negative_id": "V6518-X1-N07",
        "category": "windows_python_timezone_database",
        "failed": "The first x1 builder stopped before artifact generation because the optional IANA tzdata package was unavailable.",
        "recovery": "Pair UTC with the verified Windows system-local New Zealand offset and record the Windows timezone name separately.",
        "passing": "The corrected x1 builder emitted paired UTC and verified system-local timestamps and completed without installing tzdata.",
        "recurrence_guard": "On Windows, do not assume Python ships an IANA zone database; use the verified system-local offset or an existing approved runtime.",
    },
    {
        "negative_id": "V6518-X1-N08",
        "category": "unittest_nonpackage_import",
        "failed": "The first x1 test invocation addressed the tests directory as an importable package and failed before discovery.",
        "recovery": "Use unittest discover with the exact tests directory and exact test filename.",
        "passing": "Exact unittest discovery executed seven of seven x1 tests successfully.",
        "recurrence_guard": "Prefer exact unittest discovery when a repository tests directory has no package initializer.",
    },
    {
        "negative_id": "V6518-X1-N09",
        "category": "compound_wrapper_exit_masking",
        "failed": "A compound PowerShell wrapper continued after the failed unittest child and returned a later command's success status.",
        "recovery": "Run the test as a separate fail-fast command and propagate its child status before later checks.",
        "passing": "The corrected wrapper ran the authoritative test alone, checked its exit immediately, and returned zero only after seven tests passed.",
        "recurrence_guard": "Every compound validation wrapper must test and propagate each authoritative child exit code.",
    },
    {
        "negative_id": "V6518-X1-N10",
        "category": "staged_diff_hygiene",
        "failed": "The first exact staged diff check rejected a second blank line at the end of the new x1 validator.",
        "recovery": "Remove only the reported terminal blank line, restage the file, and rerun the unchanged diff check.",
        "passing": "The unchanged exact staged diff-hygiene gate passed after only the reported terminal blank line was removed.",
        "recurrence_guard": "Run staged diff hygiene before every commit and correct only attributable owner-local defects.",
    },
    {
        "negative_id": "V6518-X1-N11",
        "category": "count_bearing_receipt_manifest_staleness",
        "failed": "The first exact staged manifest replay found the x1 validation receipt changed after the manifest captured its earlier JSON count.",
        "recovery": "Declare the count-bearing validation receipt as a manifest self-exclusion while preserving owner-path coverage.",
        "passing": "The corrected staged replay matched all eighty-eight manifest entries and covered all ninety-two staged paths with four declared exclusions.",
        "recurrence_guard": "Exclude a count-bearing receipt from its enclosing manifest or stabilize it before the manifest is sealed.",
    },
    {
        "negative_id": "V6518-X1-N12",
        "category": "scanner_definition_quarantine_drift",
        "failed": "The first independent staged privacy replay omitted the privacy receipt from its scanner-definition quarantine and produced two false confirmed hits.",
        "recovery": "Use the same exact builder-and-receipt definition set as the preregistered five-class scanner.",
        "passing": "The corrected replay scanned ninety-two staged text surfaces, retained five definition candidates, and confirmed zero private payload hits.",
        "recurrence_guard": "Bind every replay to the exact scanner patterns and definition-quarantine set recorded by the phase.",
    },
    {
        "negative_id": "V6518-X1-N13",
        "category": "method_flow_witness_argument_contract",
        "failed": "The first Method Flow witness invocation passed the method-record option where the runner requires its dedicated witness-file option.",
        "recovery": "Use record with the record option for methods and witness with the witness-file option for witnesses.",
        "passing": "The corrected witness invocation used the dedicated witness-file option and recorded the retained failed witness without mutating another method.",
        "recurrence_guard": "Bind each Method Flow subcommand to its exact documented argument contract before invocation.",
    },
    {
        "negative_id": "V6518-X1-N14",
        "category": "generator_owned_count_mirror_staleness",
        "failed": "The first full x1 validator retry failed one targeted test because the builder regenerated a stale twelve-negative assertion after the authoritative ledger reached thirteen.",
        "recovery": "Update the generator-owned test template and all validator expectations from the authoritative ledger before regenerating the test.",
        "passing": "The corrected builder regenerated exact fourteen-negative, 7,584-effective, and fourteen-witness assertions matching the authoritative ledgers.",
        "recurrence_guard": "When a generated assertion fails, update its generator source and authoritative count mirrors together before retrying.",
    },
]


SAFE_TASKS = [
    "Verify the exact Vesper source anchors and special three-commit zero-merge lineage.",
    "Verify the clean Ilyra fast-forward boundary and four-way branch equality.",
    "Audit all source rows for current, stable, draft, or watch status only.",
    "Record content-type, language, validator, and cache-policy source drift without fetching data.",
    "Compute lexical nearest neighbours across all 1,120 frozen proposal titles.",
    "Record manual mechanism distinctions and rejected semantic collisions.",
    "Protect every frozen x1 path with an exact staged-surface allowlist.",
    "Seal x1 content in the Git path-filtered blob domain.",
    "Parse every phase JSON document with explicit UTF-8.",
    "Check deterministic JSON ordering for every generated x1 ledger.",
    "Separate privacy scanner definitions from confirmed payload dispositions.",
    "Declare checkout-byte and Git-blob hash domains without conflation.",
    "Prove owner-manifest coverage including scripts and tests.",
    "Enforce the six-thousand-word cap for every phase document.",
    "Hold terminal routing before exact-final proof.",
    "Emit workload, pacing, and correction-readiness metadata without human-state claims.",
    "Record environment versions without updating the desktop application.",
    "Verify eight inherited future CLI seats remain unnamed, uncreated, and unlaunched.",
    "Enforce ordinary x1, x2, and total commit caps.",
    "Verify zero merges and one-parent lifecycle commits.",
    "Require exactly one successful canonical bounded final pass and no replay after success.",
    "Review stale lifecycle labels and count mirrors after every additive ledger change.",
    "Lint scientific, identity, production, professional, legal, cultural, and Stage 20 boundaries.",
    "Enforce the four-value core outcome vocabulary.",
    "Verify exact-approval and blocked packets remain visible and unexecuted.",
    "Separate official citations from observations, measurements, or delegated authority.",
    "Keep ASKAP network, row, likelihood, posterior, and constraint counts at zero.",
    "Keep OpenID profiles synthetic with zero real key, account, token, or issuance events.",
    "Keep THOS proxies at zero real people, instruments, observations, or operational outcomes.",
    "Reserve manual, browser, assistive-technology, and affected-user accessibility evaluation.",
    "Preserve Māori wording in UTF-8 while leaving Māori authority exact-gated.",
    "Audit every new family-current caller for compatibility and collision.",
    "Inventory historical aliases without destructive renaming.",
    "Validate Method Flow method, witness, state, and recommendation parity.",
    "Bound every subprocess timeout and attribute partial output before retry.",
    "Require process-tree quiescence before teardown credit.",
    "Prevent inherited seed evidence from receiving Ilyra completion credit.",
    "Restrict cleanup to additive owner-scoped paths.",
    "Reject any x2 implementation or observed-outcome path from the x1 commit.",
    "Preserve same-owner validation wording and independent-reproduction abstention.",
]

CANDIDATE_TASKS = [
    "Build the Buchholz-Wichmann nuclearity and split-property board and five rejection fixtures.",
    "Build the quantum-energy-inequality obligation board and five rejection fixtures.",
    "Build the Borel-Ecalle resurgence obligation board and five rejection fixtures.",
    "Build the soft-graviton theorem obligation board and five rejection fixtures.",
    "Build the QUIC ACK_FREQUENCY draft structural tribunal.",
    "Build the MASQUE CONNECT-UDP structural tribunal.",
    "Build the WebAssembly Canonical ABI resource-handle tribunal.",
    "Build the AMQP 1.0 type and frame structural tribunal.",
    "Build the DNS SVCB and HTTPS record tribunal.",
    "Build the Oblivious HTTP context-separation tribunal.",
    "Build the IVOA VOTable 1.5 structural tribunal.",
    "Build the Git commit-graph changed-path Bloom contract.",
    "Build the RPKI route-origin validation contract.",
    "Build the deterministic MinHash proposal-neighbour explainer.",
    "Build the official-source representation-drift ledger.",
    "Build the cumulative correction-delta manifest closure contract.",
    "Build the Aho-Corasick streaming-match tribunal.",
    "Build the accessible braille naming structural audit.",
    "Build the accessible canvas fallback structural audit.",
    "Build the Gruneisen-parameter physical-domain nonconversion classifier.",
    "Build the regression-to-mean and winner-selection Stage 20 quarantine.",
    "Build the read-only plugin and MCP capability provenance catalogue.",
    "Build the log-structured merge-tree compaction tribunal.",
    "Build the radio-observation quality and correction-readback proxy.",
    "Build the RFI flagging, anomaly escalation, and stop-work proxy.",
    "Build the OpenID4VP verifier-attestation synthetic profile.",
    "Build the OpenID4VCI authorization-server selection synthetic profile.",
    "Build the Self-Issued OpenID Provider v2 draft-watch synthetic profile.",
    "Build the ASKAP RACS-mid DR2 zero-row readiness adapter.",
    "Build the spectrum, provenance, remedy, data-sovereignty, and Māori-authority reservation matrix.",
]

SKILL_IDEAS = [
    "ghc-family-nuclearity-split-property-board",
    "ghc-family-quantum-energy-inequality-board",
    "ghc-family-borel-ecalle-resurgence-board",
    "ghc-family-soft-graviton-obligation-board",
    "ghc-family-draft-protocol-status-envelope",
    "ghc-family-masque-connect-udp-tribunal",
    "ghc-family-canonical-abi-resource-guard",
    "ghc-family-amqp-structure-refusal",
    "ghc-family-svcb-service-mode-validator",
    "ghc-family-ohttp-config-refusal",
    "ghc-family-votable-structure-refusal",
    "ghc-family-commit-graph-bloom-contract",
    "ghc-family-rpki-origin-validation-contract",
    "ghc-family-minhash-neighbour-explainer",
    "ghc-family-correction-delta-closure",
    "ghc-family-aho-corasick-stream-guard",
    "ghc-family-braille-naming-audit",
    "ghc-family-canvas-fallback-audit",
    "ghc-family-radio-handover-proxy",
    "ghc-family-identity-profile-boundary",
]

RUNNER_IDEAS = [
    "ghc_family_gmut_functional_boards.py",
    "ghc_family_draft_protocol_tribunals.py",
    "ghc_family_transport_structure_tribunals.py",
    "ghc_family_canonicalization_tribunals.py",
    "ghc_family_manifest_closure.py",
    "ghc_family_radio_handover_proxy.py",
    "ghc_family_identity_profile_tribunals.py",
    "ghc_family_accessibility_structure_audits.py",
    "ghc_family_stage20_nonpromotion_boards.py",
    "ghc_family_portfolio_evidence.py",
    "ghc_family_v651_v8_detailed_validator.py",
    "ghc_family_v651_v8_minimal_validator.py",
]

CLEAN_TASKS = [
    "Reconcile retained-negative counts after startup and mutation growth.",
    "Refresh all count-dependent truth mirrors from authoritative ledgers.",
    "Normalize generated text through the declared Git-blob hash domain.",
    "Replace any working-byte historical seal with exact commit-blob checks.",
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
    "Refresh workflow-refinement output without normalizing conflicting future routes.",
    "Validate Method Flow after every new witness.",
    "Keep all failed witnesses append-only and linked to negatives.",
    "Remove no memory, identity, or sibling record to satisfy a quota.",
    "Delete no user or sibling material during cleanup.",
    "Keep future CLI seat placeholders unnamed and unlaunched.",
    "Keep Sandbox and Hyper-V states unchanged.",
    "Keep the Codex desktop application unchanged.",
    "Remove no draft or watch status merely to make a source ledger look stable.",
    "Keep ASKAP adapter counters at exact zero without data access.",
    "Keep THOS participant and operator counters at exact zero.",
    "Keep Freed ID real-key and live-issuance counters at exact zero.",
    "Keep CBR decision and authority counters at exact zero.",
    "Verify all 150 synthetic mutations retain reject-or-quarantine outcomes.",
    "Verify core outcomes use no fifth label or compensation rule.",
    "Verify open gaps and exact gates are additive and remain visible.",
    "Verify x1 content remains immutable after the frozen commit.",
    "Verify evidence and closeout commits are direct single-parent descendants.",
    "Verify exact staged paths at evidence and closeout boundaries.",
    "Verify final owner-manifest coverage and declared self exclusions.",
    "Verify stale route labels remain PREPARED_NOT_SENT before terminal proof.",
    "Verify canonical success is not replayed.",
    "Emit sibling recommendations without contacting a standby task.",
]

REJECTED_COLLISIONS = [
    {"candidate": "generic functional-renormalization board", "reason": "overlaps inherited FRG obligations; rewritten as a split-Ward identity board"},
    {"candidate": "generic QUIC parser", "reason": "overlaps inherited QUIC work; rewritten around ACK_FREQUENCY draft sequence rules"},
    {"candidate": "generic HPKE profile", "reason": "overlaps inherited HPKE work; rewritten around COSE-HPKE draft envelope binding"},
    {"candidate": "generic WebAssembly validator", "reason": "overlaps inherited WebAssembly work; rewritten around Canonical ABI resource handles"},
    {"candidate": "generic JSON canonicalizer", "reason": "overlaps inherited canonical JSON work; rewritten around decimal negative-zero and exponent obligations"},
    {"candidate": "generic manifest parity", "reason": "overlaps inherited manifests; rewritten as cumulative correction-delta interval closure"},
    {"candidate": "generic accessibility status audit", "reason": "rewritten to isolate status atomicity, busy-state coalescing, and focus nonmovement"},
    {"candidate": "generic astronomy handover", "reason": "rewritten to isolate observation-block calibration and RFI flag-version provenance"},
    {"candidate": "generic OpenID4VC profile", "reason": "rewritten into three final-spec profiles with nonoverlapping mechanisms"},
    {"candidate": "generic spectrum rights matrix", "reason": "rewritten to preserve interference reporting, data sovereignty, benefit sharing, remedy, and Māori authority"},
]
