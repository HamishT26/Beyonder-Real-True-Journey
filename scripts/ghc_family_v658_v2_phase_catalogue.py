#!/usr/bin/env python3
"""Frozen x1 catalogue for Sylven Arc's v658-v2 phase."""

from __future__ import annotations


def source(source_id: str, title: str, publisher: str, url: str, status: str, use: str) -> dict:
    return {
        "source_id": source_id,
        "title": title,
        "publisher": publisher,
        "url": url,
        "status": status,
        "observed_on": "2026-08-01",
        "use": use,
    }


OFFICIAL_SOURCES = [
    source(
        "FDSN-STATIONXML-12",
        "FDSN StationXML 1.2",
        "International Federation of Digital Seismograph Networks",
        "https://docs.fdsn.org/projects/stationxml/en/latest/",
        "current",
        "station, channel, epoch, unit, response-stage, sensitivity, provenance, and schema vocabulary only; no station operation or real response claim",
    ),
    source(
        "FDSN-STATIONXML-RESPONSE",
        "Specifying and Using Response Information",
        "International Federation of Digital Seismograph Networks",
        "https://docs.fdsn.org/projects/stationxml/en/latest/response.html",
        "current",
        "typed poles, zeros, transfer-function, normalization, convolution, stage-order, and unit obligations only; no calibrated instrument result",
    ),
    source(
        "FDSN-MINISEED3",
        "FDSN miniSEED 3 specification",
        "International Federation of Digital Seismograph Networks",
        "https://docs.fdsn.org/projects/miniseed3/en/latest/",
        "current",
        "source identifier, timing, sample payload, extra-header, encoding, CRC, and record-boundary vocabulary only; no waveform ingestion",
    ),
    source(
        "FDSN-SOURCE-ID",
        "FDSN Source Identifiers",
        "International Federation of Digital Seismograph Networks",
        "https://docs.fdsn.org/projects/source-identifiers/en/latest/",
        "current",
        "synthetic network, station, location, channel, source-code, and collision-quarantine vocabulary only",
    ),
    source(
        "BIPM-SI-9",
        "The International System of Units, ninth edition",
        "Bureau International des Poids et Mesures",
        "https://www.bipm.org/en/publications/si-brochure",
        "current",
        "units, dimensions, quantity symbols, and expression obligations only; no real measurement or calibration claim",
    ),
    source(
        "W3C-PROV",
        "PROV-O: The PROV Ontology",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/prov-o/",
        "stable",
        "entity, activity, agent-placeholder, derivation, revision, invalidation, and attribution lineage",
    ),
    source(
        "W3C-WCAG-22",
        "Web Content Accessibility Guidelines 2.2",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/WCAG22/",
        "current",
        "machine-checkable report structure and accessibility vocabulary; manual, assistive-technology, Māori-language, and affected-user evaluation remain reserved",
    ),
    source(
        "W3C-VC-DM-20",
        "Verifiable Credentials Data Model v2.0",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/vc-data-model-2.0/",
        "current",
        "synthetic credential subject, issuer-placeholder, status, validity, evidence, disclosure, and lifecycle vocabulary only; no live identity operation",
    ),
    source(
        "W3C-DATA-INTEGRITY",
        "Verifiable Credential Data Integrity 1.0",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/vc-data-integrity/",
        "current",
        "synthetic proof-configuration and verification-result schema vocabulary only; no real key, proof, or interoperability",
    ),
    source(
        "RFC-3339",
        "Date and Time on the Internet: Timestamps",
        "RFC Editor",
        "https://www.rfc-editor.org/rfc/rfc3339.html",
        "stable",
        "synthetic epoch, validity, correction, expiry, and handover timestamps",
    ),
    source(
        "RFC-8785",
        "JSON Canonicalization Scheme",
        "RFC Editor",
        "https://www.rfc-editor.org/rfc/rfc8785.html",
        "stable",
        "deterministic synthetic JSON representation vocabulary only; no cryptographic or production assurance",
    ),
    source(
        "NZ-PRIVACY-PRINCIPLES",
        "Privacy principles",
        "Office of the Privacy Commissioner New Zealand",
        "https://www.privacy.org.nz/privacy-principles/",
        "current",
        "privacy minimization, access, correction, retention, use, and disclosure context only; no legal advice or compliance finding",
    ),
    source(
        "TE-MANA-RARAUNGA",
        "Principles of Māori Data Sovereignty",
        "Te Mana Raraunga",
        "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
        "current",
        "Māori data-sovereignty reservation and authority-routing context only; no substitution for tangata whenua, iwi, hapū, or Māori authority",
    ),
]


PROTECTED_GATES = [
    "real_station_owners_operators_engineers_technicians_scientists_landholders_communities_and_affected_parties",
    "real_sites_stations_sensors_dataloggers_timing_systems_channels_waveforms_coordinates_responses_and_calibrations",
    "real_installation_access_maintenance_calibration_data_ingestion_processing_release_or_operational_decision",
    "real_instrument_response_orientation_timing_quality_noise_event_detection_location_or_hazard_judgment",
    "real_likelihood_prediction_parameter_constraint_detected_force_material_law_empirical_gmut_confirmation_or_theory_of_everything",
    "professional_seismology_geophysics_metrology_engineering_safety_privacy_security_or_accessibility_authority",
    "land_property_access_monitoring_surveillance_liability_regulation_and_legal_interpretation",
    "traditional_knowledge_culturally_restricted_information_taonga_place_and_collective_interests",
    "production_identity_live_keys_signatures_proofs_issuance_resolution_status_revocation_interoperability_recovery_and_trust",
    "privacy_complete",
    "exhaustive_security",
    "complete_accessibility",
    "legal_cultural_language_data_governance_and_maori_authority",
    "affected_party_consent_notice_contestation_remedy_collective_governance_and_acceptance",
    "independent_team_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]


def proposal(number: int, title: str, slug: str, pillar: str, mechanism: str, sources: list[str]) -> dict:
    if number <= 23:
        expected_disposition = "completed"
        approval = "safe_now_bounded_structural_formal_or_synthetic_software"
        lane = "x2_owner_local_bounded_synthetic"
    elif number <= 28:
        expected_disposition = "represented"
        approval = "candidate_proxy_protocol_or_nonproduction_schema"
        lane = "x2_owner_local_representation_only"
    elif number == 29:
        expected_disposition = "open_gap"
        approval = "candidate_external_readiness_without_network_call"
        lane = "x2_owner_local_zero_row_readiness"
    else:
        expected_disposition = "exact_gate"
        approval = "outside_hamish_authority_affected_party_and_maori_authority_required"
        lane = "not_executed_authority_reservation"
    return {
        "proposal_id": f"V6582-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar_relation": pillar,
        "mechanism": mechanism,
        "hypothesis": (
            f"A bounded {mechanism} contract can expose falsifiable synthetic obligations while refusing unsupported "
            "real-station, empirical, participant, professional, safety, production, legal, cultural, Māori-authority, "
            "privacy-complete, accessibility-complete, identity, Theory-of-Everything, or Stage 20 promotion."
        ),
        "null_or_failure_condition": (
            f"The artifact omits a required {mechanism} obligation, accepts a frozen mutation, erases a failure, or "
            "crosses a protected station, person, instrument, measurement, waveform, rights, professional, empirical, "
            "production, legal, cultural, Māori-authority, identity, privacy, accessibility, security, Theory-of-Everything, or Stage 20 gate."
        ),
        "approval_class": approval,
        "execution_lane": lane,
        "official_or_primary_source_needs": sources,
        "concrete_artifacts": [
            f"surfaces/{slug}/contract.json",
            f"surfaces/{slug}/mutation-results.json",
            f"surfaces/{slug}/bounded-receipt.json",
        ],
        "falsifier_or_acceptance_gate": (
            "The valid synthetic fixture passes, five preregistered mutations are rejected, and the receipt grants no "
            "real person, station, instrument, waveform, measurement, calibration, operation, professional, production, "
            "legal, cultural, Māori-authority, identity, privacy-complete, accessibility-complete, exhaustive-security, "
            "independent-reproduction, Theory-of-Everything, or Stage 20 credit."
        ),
        "rollback_or_recovery": (
            "Stop, retain the failed witness at zero credit, rewrite no history, and leave real people, sites, stations, "
            "instruments, measurements, waveforms, sibling lanes, external systems, and authority state unchanged."
        ),
        "protected_gates": PROTECTED_GATES,
        "expected_disposition": expected_disposition,
    }


PROPOSAL_SPECS = [
    ("Station-metadata request quarantine with purpose, synthetic scope, access hold, abort rule, and no-operation lock", "seis-request-quarantine", "THOS Body and CBR Heart", "metadata request, purpose, synthetic scope, access hold, abort rule, and operation refusal", ["FDSN-STATIONXML-12", "W3C-PROV", "NZ-PRIVACY-PRINCIPLES"]),
    ("FDSN source-identifier passport with synthetic network, station, location, channel, revision, and collision quarantine", "seis-source-id-passport", "Freed ID and THOS Body", "synthetic source identifier, network, station, location, channel, revision, and collision quarantine", ["FDSN-SOURCE-ID", "W3C-PROV", "RFC-3339"]),
    ("Station and channel epoch ledger with start, end, overlap, supersession, invalidation, and no-live-validity claim", "seis-epoch-ledger", "Freed ID and GMUT Mind", "station and channel epoch, overlap, supersession, invalidation, correction, and live-validity refusal", ["FDSN-STATIONXML-12", "RFC-3339", "W3C-PROV"]),
    ("Coordinate-frame and datum envelope with latitude, longitude, elevation, depth, uncertainty, redaction, and no-site-location release", "seis-coordinate-datum", "GMUT Mind and CBR Heart", "coordinate frame, datum placeholder, latitude, longitude, elevation, depth, uncertainty, redaction, and site-release refusal", ["FDSN-STATIONXML-12", "BIPM-SI-9", "NZ-PRIVACY-PRINCIPLES"]),
    ("Channel orientation board with azimuth, dip, handedness, frame, uncertainty, correction, and no-installation verdict", "seis-orientation-board", "GMUT Mind and THOS Body", "channel azimuth, dip, handedness, coordinate frame, uncertainty, correction, and installation-verdict refusal", ["FDSN-STATIONXML-12", "BIPM-SI-9", "W3C-PROV"]),
    ("Rational sample-rate contract with numerator, denominator, unit, tolerance, decimation relation, and no-clock-quality inference", "seis-sample-rate-contract", "GMUT Mind", "rational sample rate, numerator, denominator, unit, tolerance, decimation relation, and clock-quality refusal", ["FDSN-STATIONXML-12", "FDSN-MINISEED3", "BIPM-SI-9"]),
    ("Timing-correction envelope with clock basis, offset, leap-second placeholder, uncertainty, provenance, and no-absolute-time claim", "seis-timing-correction", "GMUT Mind and Freed ID", "clock basis, timing offset, leap-second placeholder, uncertainty, provenance, correction, and absolute-time refusal", ["FDSN-MINISEED3", "RFC-3339", "W3C-PROV"]),
    ("Instrument-response stage graph with ordered sensor, preamplifier, digitizer, decimation, gain, and no-calibration certificate", "seis-response-stage-graph", "GMUT Mind and THOS Body", "ordered response stages, sensor, preamplifier, digitizer, decimation, gain, and calibration-certificate refusal", ["FDSN-STATIONXML-RESPONSE", "FDSN-STATIONXML-12", "W3C-PROV"]),
    ("Poles-and-zeros typed board with transfer-function kind, complex roots, normalization, units, domain, and no-physical-response claim", "seis-poles-zeros-board", "GMUT Mind", "poles, zeros, transfer-function type, complex roots, normalization, units, domain, and physical-response refusal", ["FDSN-STATIONXML-RESPONSE", "BIPM-SI-9", "W3C-PROV"]),
    ("Instrument-sensitivity chain with input and output units, frequency, stage product, mismatch hold, and no-traceability claim", "seis-sensitivity-chain", "GMUT Mind", "instrument sensitivity, input units, output units, frequency, stage product, mismatch hold, and traceability refusal", ["FDSN-STATIONXML-RESPONSE", "BIPM-SI-9", "FDSN-STATIONXML-12"]),
    ("Finite-impulse and coefficient stage ledger with symmetry, normalization, delay, correction, uncertainty, and no-filter-release", "seis-coefficient-stage", "GMUT Mind and THOS Body", "coefficient stage, finite impulse response, symmetry, normalization, delay, correction, uncertainty, and filter-release refusal", ["FDSN-STATIONXML-RESPONSE", "FDSN-STATIONXML-12", "BIPM-SI-9"]),
    ("Waveform record-boundary tribunal with header, payload length, encoding, CRC, extra-header, resource budget, and no-ingest release", "seis-record-boundary", "THOS Body", "record header, payload length, encoding, CRC, extra header, resource budget, and ingest-release refusal", ["FDSN-MINISEED3", "FDSN-SOURCE-ID", "RFC-8785"]),
    ("Gap and overlap interval ledger with inclusive boundaries, precedence, correction lineage, ambiguity, and no-data-quality grade", "seis-gap-overlap-ledger", "GMUT Mind and THOS Body", "gap, overlap, interval boundaries, precedence, correction lineage, ambiguity, and quality-grade refusal", ["FDSN-MINISEED3", "RFC-3339", "W3C-PROV"]),
    ("Calibration-event provenance graph with stimulus placeholder, reference chain, result quarantine, supersession, and no-certificate claim", "seis-calibration-provenance", "Freed ID and GMUT Mind", "calibration event, stimulus placeholder, reference chain, result quarantine, supersession, and certificate-claim refusal", ["W3C-PROV", "BIPM-SI-9", "FDSN-STATIONXML-12"]),
    ("Vault-environment observation envelope with temperature, humidity, power, clock, missingness, uncertainty, and no-instrument-health verdict", "seis-vault-environment", "THOS Body and GMUT Mind", "vault environment, temperature, humidity, power, clock, missingness, uncertainty, and instrument-health refusal", ["BIPM-SI-9", "W3C-PROV", "RFC-3339"]),
    ("Mass-position and state-of-health surrogate with channel placeholder, bounds, staleness, escalation, and no-maintenance instruction", "seis-state-health-surrogate", "THOS Body and GMUT Mind", "mass position, state-of-health channel, bounds, staleness, escalation, and maintenance-instruction refusal", ["FDSN-STATIONXML-12", "FDSN-SOURCE-ID", "W3C-PROV"]),
    ("Response-removal typed contract with convolution direction, stage selection, unit transform, water-level placeholder, and no-ground-motion inference", "seis-response-removal", "GMUT Mind", "response removal, convolution direction, stage selection, unit transform, water-level placeholder, and ground-motion-inference refusal", ["FDSN-STATIONXML-RESPONSE", "BIPM-SI-9", "W3C-PROV"]),
    ("Spectral-window and leakage board with taper, segment length, overlap, frequency grid, normalization, and no-signal-discovery claim", "seis-spectral-window", "GMUT Mind", "spectral window, taper, segment length, overlap, frequency grid, normalization, and signal-discovery refusal", ["BIPM-SI-9", "FDSN-MINISEED3", "W3C-PROV"]),
    ("Noise-covariance placeholder with station pairs, frequency bins, missingness, regularization hold, and no-noise-model fit", "seis-noise-covariance", "GMUT Mind", "noise covariance, station pairs, frequency bins, missingness, regularization hold, and model-fit refusal", ["BIPM-SI-9", "W3C-PROV", "FDSN-STATIONXML-12"]),
    ("GMUT instrument-forward operator with typed source placeholder, response kernel, boundary, residual, unit audit, and observation firewall", "seis-gmut-forward-operator", "GMUT Mind", "typed instrument forward operator, source placeholder, response kernel, boundary, residual, unit audit, and observation firewall", ["FDSN-STATIONXML-RESPONSE", "BIPM-SI-9", "W3C-PROV"]),
    ("GMUT inverse-identifiability tribunal with source, path, site, instrument, timing, processing, and confounding alternatives", "seis-gmut-identifiability", "GMUT Mind", "inverse identifiability, source, path, site, instrument, timing, processing confounding, and parameter-claim refusal", ["FDSN-STATIONXML-RESPONSE", "W3C-PROV", "BIPM-SI-9"]),
    ("GMUT gauge, EFT, domain, and scale-separation board with operator typing, cutoff placeholder, provenance, and no-fundamental-law promotion", "seis-gmut-eft-firewall", "GMUT Mind", "gauge typing, effective-field-theory domain, scale separation, cutoff placeholder, provenance, and fundamental-law refusal", ["BIPM-SI-9", "W3C-PROV", "FDSN-STATIONXML-RESPONSE"]),
    ("Structurally accessible station-response report with headings, table semantics, focus order, print fallback, and manual-evaluation reservation", "seis-accessible-report", "THOS Body and CBR Heart", "accessible report headings, table semantics, focus order, non-colour cues, print fallback, and manual-evaluation reservation", ["W3C-WCAG-22", "FDSN-STATIONXML-12", "NZ-PRIVACY-PRINCIPLES"]),
    ("THOS station-metadata correction and shift-handover proxy with matched synthetic budget, interruption log, readback, and no-operator evidence", "thos-seis-handover-proxy", "THOS Body", "synthetic correction queue, matched event budget, interruption log, stop threshold, readback, handover, and operator-evidence refusal", ["RFC-3339", "W3C-WCAG-22", "W3C-PROV"]),
    ("THOS alarm-ownership and workload-recovery proxy with synthetic alerts, priority, pause, resumption, escalation, and no-effectiveness estimate", "thos-seis-workload-proxy", "THOS Body", "synthetic alarm ownership, priority, pause, resumption, escalation, workload, and effectiveness-estimate refusal", ["RFC-3339", "W3C-PROV", "W3C-WCAG-22"]),
    ("Freed ID synthetic station-custody credential with pseudonymous station, role placeholder, validity, correction, status, and nonproduction boundary", "freed-id-seis-custody", "Freed ID and CBR Heart", "synthetic station custody credential, pseudonym, role placeholder, validity, correction, status, and production refusal", ["W3C-VC-DM-20", "W3C-PROV", "NZ-PRIVACY-PRINCIPLES"]),
    ("Freed ID selective-disclosure response provenance with concealed site fields, disclosed stage digest, purpose, expiry, and no-real-proof", "freed-id-seis-disclosure", "Freed ID and GMUT Mind", "synthetic selective disclosure, concealed site fields, response-stage digest, purpose, expiry, and real-proof refusal", ["W3C-VC-DM-20", "W3C-DATA-INTEGRITY", "RFC-8785"]),
    ("Freed ID synthetic response-change capability with scoped action vocabulary, delegation refusal, holder-binding placeholder, expiry, and no operational power", "freed-id-seis-change-capability", "Freed ID and THOS Body", "synthetic response-change capability, scoped action vocabulary, delegation refusal, holder-binding placeholder, expiry, and operational-power refusal", ["W3C-VC-DM-20", "W3C-PROV", "RFC-3339"]),
    ("FDSN station and dataselect service-capability matrix with offline fixture map, endpoint-version watch, disabled transport, and zero observations", "seis-fdsn-capability-matrix", "GMUT Mind and THOS Body", "FDSN station and dataselect capability matrix, offline fixture map, endpoint-version watch, disabled transport, and zero-observation boundary", ["FDSN-STATIONXML-12", "FDSN-MINISEED3", "FDSN-SOURCE-ID"]),
    ("CBR station land, monitoring privacy, seismic-risk communication, traditional-knowledge, affected-party, and Māori-data authority covenant", "cbr-seis-authority-covenant", "CBR Heart across all pillars", "station land, access, monitoring privacy, risk communication, traditional knowledge, affected-party, Māori-data, tangata whenua, iwi, hapū, and Māori-authority reservation", ["NZ-PRIVACY-PRINCIPLES", "TE-MANA-RARAUNGA", "W3C-PROV"]),
]


PROPOSALS = [proposal(index, *spec) for index, spec in enumerate(PROPOSAL_SPECS, 1)]


SKILL_SPECS = [
    ("ghc-family-seismic-metadata-intake", "Constrain purpose, synthetic station scope, source identifiers, epochs, correction, abort, and no-operation states."),
    ("ghc-family-seismic-coordinate-orientation", "Constrain coordinate frames, datums, orientation, uncertainty, privacy redaction, and no-installation judgments."),
    ("ghc-family-seismic-timing-sampling", "Constrain clocks, offsets, sample rates, decimation, intervals, gaps, overlaps, and absolute-time refusal."),
    ("ghc-family-seismic-response-stages", "Constrain response stages, poles, zeros, sensitivity, coefficients, units, normalization, and no-calibration claims."),
    ("ghc-family-seismic-record-boundaries", "Constrain miniSEED-style headers, lengths, encodings, CRC, extra headers, budgets, and ingest refusal."),
    ("ghc-family-seismic-provenance", "Constrain calibration, environment, health, correction, derivation, invalidation, and certificate refusal."),
    ("ghc-family-seismic-gmut-firewall", "Keep forward, inverse, spectral, covariance, gauge, EFT, unit, domain, and observation contracts within typed research bounds."),
    ("ghc-family-seismic-thos-handover", "Constrain synthetic correction queues, alarm ownership, workload, interruption, stop state, readback, and handover."),
    ("ghc-family-seismic-freed-id", "Constrain synthetic custody, disclosure, proof, status, expiry, recovery, privacy, and nonproduction boundaries."),
    ("ghc-family-seismic-authority-reservation", "Fail closed around land, monitoring privacy, risk communication, law, culture, affected parties, and Māori authority."),
]


RUNNER_SPECS = [
    ("ghc_family_seismic_metadata_intake.py", "seis-request-quarantine"),
    ("ghc_family_seismic_coordinate_orientation.py", "seis-coordinate-datum"),
    ("ghc_family_seismic_timing_sampling.py", "seis-timing-correction"),
    ("ghc_family_seismic_response_stages.py", "seis-response-stage-graph"),
    ("ghc_family_seismic_record_boundaries.py", "seis-record-boundary"),
    ("ghc_family_seismic_provenance.py", "seis-calibration-provenance"),
    ("ghc_family_seismic_gmut_firewall.py", "seis-gmut-forward-operator"),
    ("ghc_family_seismic_thos_handover.py", "thos-seis-handover-proxy"),
    ("ghc_family_seismic_freed_id.py", "freed-id-seis-custody"),
    ("ghc_family_seismic_authority_reservation.py", "cbr-seis-authority-covenant"),
]


def negative(number: int, slug: str, failure: str, recovery: str, guard: str) -> dict:
    return {
        "negative_id": f"V6582-X1-N{number:02d}",
        "scope": "startup_and_x1",
        "signature": slug,
        "observed": failure,
        "credit": 0,
        "retained": True,
        "recovery": recovery,
        "recurrence_guard": guard,
        "same_owner_only": True,
        "independent_reproduction": False,
    }


X1_OPERATIONAL_NEGATIVES = [
    negative(1, "powershell-json-nonstring-key-serialization", "The first skill-discovery object serialization failed before emitting paths.", "Emit literal path lines without object serialization.", "Prefer scalar path output for startup discovery."),
    negative(2, "memory-range-read-no-output", "A bounded memory range read returned no attributable output and earned zero credit.", "Use a narrower indexed search and rely only on returned lines.", "Treat absent output as absent evidence."),
    negative(3, "method-flow-schema-filename-assumption", "The first Method Flow schema probe guessed a nonexistent filename.", "Follow the exact SKILL.md reference to references/schema.md.", "Resolve required references from the selected skill, never from naming intuition."),
    negative(4, "reflection-schema-filename-assumption", "The first Reflection Remaster schema probe guessed a nonexistent filename.", "Follow the exact SKILL.md reference to references/decision-schema.md.", "Resolve every skill-relative reference literally."),
    negative(5, "cmd-quoted-git-c-path", "A cmd.exe Git batch passed quoted -C paths literally and every child refused the path.", "Set the literal workdir and omit -C.", "Under cmd.exe prefer the execution workdir over embedded quoted -C paths."),
    negative(6, "cmd-caret-parent-expansion", "cmd.exe consumed a commit-parent caret and returned the final commit itself.", "Use the tilde-parent notation and verify the commit header.", "Avoid caret revision syntax in cmd.exe wrappers."),
    negative(7, "parallel-source-status-lost-attribution", "A parallel source status probe returned no attributable completion state.", "Split tracked, untracked, and scalar revision checks; then run one supervised status.", "Do not combine slow large-worktree status with unrelated probes."),
    negative(8, "inline-python-cmd-quote-split", "cmd.exe split an inline Python payload before manifest parsing.", "Use file-oriented helpers or PowerShell literal scripts.", "Avoid complex inline language payloads through cmd.exe."),
    negative(9, "jq-not-installed", "A jq fallback was unavailable and performed no manifest read.", "Use the installed PowerShell JSON reader or committed Python helper.", "Probe dependencies before selecting an optional parser."),
    negative(10, "cmd-roster-seat-quote-split", "cmd.exe split the two-word roster seat and the query failed.", "Use PowerShell single-quoted literal arguments.", "Pass relational names through a shell with literal argument semantics."),
    negative(11, "worktree-checkout-returned-during-initialization", "The worktree command yielded after checkout began while Git still held the initialization lock.", "Audit registered HEAD, branch, Git processes, lock state, and wait for natural completion without retrying.", "Never duplicate a worktree mutation after an early-yield wrapper result."),
    negative(12, "parallel-new-worktree-cleanliness-lost-attribution", "A parallel cleanliness batch lost output for slower Git probes.", "Audit processes and locks, then run one scalar status through completion.", "Serialize large-worktree clean-state checks."),
    negative(13, "source-proposal-render-truncated", "A combined source proposal and portfolio render exceeded the output envelope.", "Read schemas and summary receipts, then parse the frozen proposal index mechanically.", "Do not render large compact ledgers as conversational evidence."),
    negative(14, "cmd-rg-pattern-quote-reinterpreted", "cmd.exe reinterpreted a quoted rg pattern beginning with a dash fragment.", "Use PowerShell single-quoted patterns and explicit -e arguments.", "Use literal pattern semantics for shell metacharacters and leading dashes."),
    negative(15, "windows-cp1252-catalogue-render", "A read-only Python catalogue summary reached a Māori character that the inherited Windows CP1252 stdout codec could not encode; the command earned zero credit and changed no repository state.", "Set PYTHONIOENCODING=utf-8 and rerun only the bounded read-only catalogue summary.", "Set an explicit UTF-8 stdout encoding before rendering repository text that can contain Māori or other non-CP1252 characters."),
    negative(16, "multi-ledger-inline-key-probe-no-output", "A combined read-only inline Python probe over five inherited ledgers returned no attributable output and earned zero credit.", "Read the three required count ledgers individually with explicit UTF-8 PowerShell JSON parsing.", "Use bounded per-ledger reads for source count verification instead of a multi-ledger inline expression."),
    negative(17, "source-route-checkout-hash-domain-assumption", "The first x1 build assumed the CRLF working-tree checkout of the source route file had the same SHA-256 as its immutable LF Git blob and stopped before emitting x1 artifacts.", "Preserve the exact Git-object identifier and Git-blob SHA-256 gate while recording the independently verified checkout-byte SHA-256 in its own hash domain.", "Never equate Git-blob and working-tree byte hashes when line-ending conversion is possible; label and validate both domains explicitly."),
    negative(18, "compound-temporary-hash-probe-policy-rejection", "A compound diagnostic containing temporary-file creation and cleanup was rejected by the command policy before execution and earned zero credit.", "Use a non-writing bounded Get-FileHash, Git object query, and file-length probe.", "Prefer non-writing scalar diagnostics when the needed evidence already exists in the checkout and object database."),
    negative(19, "x1-semantic-novelty-rejection", "The first novelty aggregate rejected V6582-P28 at 0.7368 similarity and V6582-P29 at 0.6364 similarity to Elowen v658-v1 predecessors; no x1 packet was credited.", "Replace the repeated proof-lifecycle and generic zero-row-adapter mechanisms with a scoped synthetic response-change capability and an offline FDSN service-capability matrix, then rerun the x1 builder.", "Treat lexical novelty failures as evidence of semantic staleness and redesign the mechanism rather than weakening the 0.60 threshold."),
    negative(20, "stale-label-scan-inherited-index-overmatch", "The first staged stale-label scan searched the compact inherited proposal index, misclassified intentionally preserved v658-v1 dry-stone titles, and produced truncated output; it earned zero credit.", "Exclude the declared inherited frozen-chain index from narrative stale-label review, validate its schema and counts separately, and scan current phase narratives and configuration with bounded scalar output.", "Never treat retained historical proposal text as a stale current-phase label or render a compact inherited chain into the output envelope."),
]


SAFE_TASKS = [
    {
        "task_id": f"V6582-SAFE-{index:03d}",
        "proposal_id": item["proposal_id"],
        "task": f"Build and validate the bounded synthetic contract for {item['slug']}.",
        "approval_class": "safe_now_owner_local_additive",
        "x1_execution": False,
        "planned_lane": "x2",
    }
    for index, item in enumerate(PROPOSALS, 1)
]


CANDIDATE_TASKS = [
    {
        "task_id": f"V6582-CAND-{index:03d}",
        "task": f"Prototype a reversible cross-surface refinement for {PROPOSALS[(index - 1) % len(PROPOSALS)]['slug']}.",
        "approval_class": "candidate_owner_local_review_required",
        "x1_execution": False,
        "planned_lane": "x2_if_bounded_evidence_permits",
    }
    for index in range(1, 21)
]


CLEAN_TASKS = [
    {
        "task_id": f"V6582-CLEAN-{index:03d}",
        "task": f"Run additive compatibility, privacy, provenance, stale-label, and nonpromotion cleanup for {item['slug']}.",
        "approval_class": "safe_now_additive_cleanup",
        "x1_execution": False,
        "planned_lane": "x2",
    }
    for index, item in enumerate(PROPOSALS, 1)
]
