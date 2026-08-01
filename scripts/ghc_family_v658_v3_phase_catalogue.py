#!/usr/bin/env python3
"""Frozen x1 catalogue for Caelen Morrow's solo v658-v3 phase."""

from __future__ import annotations


def source(source_id: str, title: str, publisher: str, url: str, status: str, use: str) -> dict:
    return {
        "source_id": source_id,
        "title": title,
        "publisher": publisher,
        "url": url,
        "status": status,
        "observed_on": "2026-08-02",
        "use": use,
    }


OFFICIAL_SOURCES = [
    source(
        "ISO-18911-2010",
        "Imaging materials — Processed safety photographic films — Storage practices",
        "International Organization for Standardization",
        "https://www.iso.org/standard/46602.html",
        "confirmed",
        "processed safety-film storage, handling, inspection, enclosure, and condition vocabulary only; the standard expressly does not cover nitrate film and no conformance is claimed",
    ),
    source(
        "ISO-18901-2010",
        "Imaging materials — Processed silver-gelatin type black-and-white films — Specifications for stability",
        "International Organization for Standardization",
        "https://www.iso.org/standard/51029.html",
        "confirmed",
        "processed silver-gelatin black-and-white film stability vocabulary only; no material test, diagnosis, or conformance claim",
    ),
    source(
        "ISO-18906-2000",
        "Imaging materials — Photographic films — Specifications for safety film",
        "International Organization for Standardization",
        "https://www.iso.org/standard/31930.html",
        "published_watch",
        "safety-film classification vocabulary only; no real base identification, combustion test, handling decision, or conformance claim",
    ),
    source(
        "LOC-FILM-CARE",
        "Care, Handling, and Storage of Motion Picture Film",
        "Library of Congress",
        "https://www.loc.gov/preservation/care/film.html",
        "current",
        "film-base, enclosure, handling, nitrate, acetate, storage, and deterioration context only; repository work never instructs real handling or disposition",
    ),
    source(
        "FIAF-TECHNICAL-RESOURCES",
        "FIAF Technical Commission resources",
        "International Federation of Film Archives",
        "https://www.fiafnet.org/pages/E-Resources/Old-Technical-Commission-Resources.html",
        "current_watch",
        "archival motion-picture terminology and technical-resource discovery only; no professional or institutional endorsement",
    ),
    source(
        "FADGI-MOTION-PICTURE",
        "Motion Picture Film Digitization Performance Work Statement",
        "Federal Agencies Digital Guidelines Initiative",
        "https://www.digitizationguidelines.gov/guidelines/FilmScan_PWS-SOW_20160418.pdf",
        "published",
        "digitization workflow, frame, image, sound, metadata, and quality-control vocabulary only; no scanner operation, digitization result, or FADGI conformance claim",
    ),
    source(
        "FADGI-DPX-METADATA",
        "Embedding Metadata in Digital Picture Exchange (DPX) Files",
        "Federal Agencies Digital Guidelines Initiative",
        "https://www.digitizationguidelines.gov/guidelines/digitize-DPXembedding.html",
        "current",
        "DPX header and embedded-metadata vocabulary only; no real frame sequence, file, scanner, or checksum claim",
    ),
    source(
        "PBCORE-21",
        "PBCore 2.1 XML Schema",
        "PBCore Metadata Standard",
        "https://pbcore.org/xsd",
        "current",
        "audiovisual asset, instantiation, physical and digital format, duration, frame-rate, track, identifier, relation, rights, and annotation vocabulary only",
    ),
    source(
        "LOC-PREMIS-3",
        "PREMIS Data Dictionary for Preservation Metadata, version 3.0",
        "Library of Congress",
        "https://www.loc.gov/standards/premis/",
        "current",
        "preservation object, event, agent-placeholder, rights, relationship, fixity, and outcome-detail vocabulary only; no real custody or rights decision",
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
        "machine-checkable structure and accessibility vocabulary; manual, assistive-technology, Māori-language, and affected-user evaluation remain reserved",
    ),
    source(
        "W3C-VC-DM-20",
        "Verifiable Credentials Data Model v2.0",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/vc-data-model-2.0/",
        "current",
        "synthetic issuer, holder, subject, validity, status, evidence, terms, and disclosure vocabulary only; no live identity operation",
    ),
    source(
        "W3C-DATA-INTEGRITY",
        "Verifiable Credential Data Integrity 1.0",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/vc-data-integrity/",
        "current",
        "synthetic proof-configuration and verification-result vocabulary only; no real key, proof, signature, security, or interoperability",
    ),
    source(
        "RFC-3339",
        "Date and Time on the Internet: Timestamps",
        "RFC Editor",
        "https://www.rfc-editor.org/rfc/rfc3339.html",
        "stable",
        "synthetic inspection, validity, correction, expiry, and handover timestamps",
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
    source(
        "LOCAL-CONTEXTS-TK",
        "Traditional Knowledge Labels",
        "Local Contexts",
        "https://localcontexts.org/labels/traditional-knowledge-labels/",
        "current_watch",
        "community-defined traditional-knowledge notice and authority-reservation context only; labels are not selected, authored, or applied by this phase",
    ),
]


PROTECTED_GATES = [
    "real_archivists_conservators_projectionists_rightsholders_donors_depositors_communities_and_affected_parties",
    "real_films_reels_cans_leaders_splices_frames_soundtracks_projectors_scanners_chemicals_measurements_images_and_records",
    "real_inspection_handling_cleaning_repair_splicing_winding_projection_scanning_storage_transport_access_or_disposition",
    "nitrate_identification_testing_storage_handling_transport_disposal_fire_hazard_or_emergency_instruction",
    "professional_archival_conservation_projection_engineering_safety_privacy_security_or_accessibility_authority",
    "copyright_contract_donor_depositor_rights_access_restriction_or_legal_interpretation",
    "traditional_knowledge_culturally_restricted_information_taonga_collective_interests_and_community_protocols",
    "production_identity_live_keys_signatures_proofs_issuance_resolution_status_revocation_interoperability_recovery_and_trust",
    "privacy_complete",
    "exhaustive_security",
    "complete_accessibility",
    "legal_cultural_language_data_governance_and_maori_authority",
    "affected_party_consent_notice_contestation_remedy_collective_governance_and_acceptance",
    "independent_team_reproduction",
    "empirical_gmut_prediction_constraint_force_or_material_law",
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
        approval = "candidate_external_standards_readiness_without_network_or_real_rows"
        lane = "x2_owner_local_zero_row_readiness"
    else:
        expected_disposition = "exact_gate"
        approval = "outside_hamish_authority_affected_party_rightsholder_community_and_maori_authority_required"
        lane = "not_executed_authority_reservation"
    return {
        "proposal_id": f"V6583-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar_relation": pillar,
        "mechanism": mechanism,
        "hypothesis": (
            f"A bounded {mechanism} contract can expose falsifiable synthetic obligations while refusing unsupported "
            "real-film, empirical, participant, professional, safety, production, legal, cultural, Māori-authority, "
            "privacy-complete, accessibility-complete, identity, Theory-of-Everything, or Stage 20 promotion."
        ),
        "null_or_failure_condition": (
            f"The artifact omits a required {mechanism} obligation, accepts a frozen mutation, erases a failure, or "
            "crosses a protected person, film, material, equipment, measurement, rights, professional, empirical, "
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
            "real person, film, material, equipment, image, sound, measurement, handling, professional, production, legal, "
            "cultural, Māori-authority, identity, privacy-complete, accessibility-complete, exhaustive-security, independent-"
            "reproduction, Theory-of-Everything, or Stage 20 credit."
        ),
        "rollback_or_recovery": (
            "Stop, retain the failed witness at zero credit, rewrite no history, and leave real people, films, materials, "
            "equipment, records, sibling lanes, external systems, rights, and authority state unchanged."
        ),
        "protected_gates": PROTECTED_GATES,
        "expected_disposition": expected_disposition,
    }


PROPOSAL_SPECS = [
    ("Film-inspection request quarantine with purpose, synthetic object scope, custody hold, abort rule, and no-handling lock", "film-request-quarantine", "Freed ID and CBR Heart", "inspection request, purpose, synthetic object scope, custody hold, abort rule, and handling refusal", ["LOC-FILM-CARE", "W3C-PROV", "NZ-PRIVACY-PRINCIPLES"]),
    ("Archival element and reel identity passport with synthetic work, version, reel, can, segment, alias, and collision quarantine", "film-element-passport", "Freed ID and CBR Heart", "synthetic work, version, element, reel, can, segment, identifier alias, and collision quarantine", ["PBCORE-21", "LOC-PREMIS-3", "W3C-PROV"]),
    ("Film gauge, perforation, pitch, stock class, and uncertainty envelope with no-compatibility release", "film-gauge-perforation", "GMUT Mind and THOS Body", "film gauge, perforation geometry, pitch, stock class, uncertainty, mismatch hold, and compatibility refusal", ["FIAF-TECHNICAL-RESOURCES", "PBCORE-21", "LOC-FILM-CARE"]),
    ("Film-base, emulsion, stock, generation, and identification-provenance ledger with unknown-base quarantine", "film-base-provenance", "Freed ID and THOS Body", "film base, emulsion, stock, generation, identification provenance, uncertainty, and unknown-base quarantine", ["ISO-18906-2000", "LOC-FILM-CARE", "W3C-PROV"]),
    ("Reel, can, core, leader, segment, and footage-map graph with missing-range and no-winding instruction", "film-reel-footage-map", "THOS Body and Freed ID", "reel, can, core, leader, segment, footage map, missing range, and winding-instruction refusal", ["ISO-18911-2010", "PBCORE-21", "W3C-PROV"]),
    ("Edge-code and keycode transcription ledger with location, reading direction, ambiguity, correction, and no-date inference", "film-edge-code-ledger", "Freed ID and GMUT Mind", "edge code, keycode, location, reading direction, ambiguity, correction lineage, and manufacturing-date inference refusal", ["FIAF-TECHNICAL-RESOURCES", "W3C-PROV", "RFC-3339"]),
    ("Frame-rate, perforation cadence, pulldown, timebase, and duration contract with no-projection-speed verdict", "film-frame-timebase", "GMUT Mind", "frame rate, perforation cadence, pulldown placeholder, timebase, duration, uncertainty, and projection-speed refusal", ["PBCORE-21", "FADGI-MOTION-PICTURE", "RFC-3339"]),
    ("Image area, frame line, aperture, aspect-ratio, orientation, and masking board with no-presentation release", "film-image-aperture", "GMUT Mind and THOS Body", "image area, frame line, aperture, aspect ratio, orientation, masking placeholder, and presentation-release refusal", ["FADGI-MOTION-PICTURE", "PBCORE-21", "W3C-PROV"]),
    ("Shrinkage, warp, curl, brittleness, deformation, uncertainty, and stop-state envelope with no-material diagnosis", "film-dimensional-condition", "THOS Body and GMUT Mind", "shrinkage placeholder, warp, curl, brittleness, deformation, uncertainty, stop state, and material-diagnosis refusal", ["ISO-18911-2010", "LOC-FILM-CARE", "FIAF-TECHNICAL-RESOURCES"]),
    ("Perforation tear, notch, edge damage, buckle, repair, and transport-risk map with no-repair instruction", "film-perforation-damage", "THOS Body", "perforation tear, notch, edge damage, buckle, repair placeholder, transport-risk hold, and repair-instruction refusal", ["ISO-18911-2010", "FIAF-TECHNICAL-RESOURCES", "W3C-PROV"]),
    ("Cement, tape, ultrasonic, unknown splice, overlap, frame loss, and intervention-lineage ledger with no-splicing instruction", "film-splice-lineage", "Freed ID and THOS Body", "cement, tape, ultrasonic, unknown splice, overlap, frame loss, intervention lineage, and splicing-instruction refusal", ["FIAF-TECHNICAL-RESOURCES", "LOC-PREMIS-3", "W3C-PROV"]),
    ("Optical, magnetic, variable-area, variable-density, track-position, language-placeholder, and no-playback soundtrack topology", "film-soundtrack-topology", "GMUT Mind and CBR Heart", "optical and magnetic soundtrack kind, variable-area and variable-density form, track position, language placeholder, and playback refusal", ["PBCORE-21", "FADGI-MOTION-PICTURE", "W3C-PROV"]),
    ("Black-and-white, chromogenic, dye-transfer, tint, tone, fade, density-placeholder, and no-colorimetry observation schema", "film-colour-observation", "GMUT Mind", "image process, black-and-white, chromogenic, dye transfer, tint, tone, fade, density placeholder, and colorimetry refusal", ["ISO-18901-2010", "FADGI-MOTION-PICTURE", "W3C-PROV"]),
    ("Acetate-odor, vinegar-syndrome, channeling, plasticizer, test-placeholder, ventilation hold, and no-chemical diagnosis envelope", "film-acetate-syndrome", "THOS Body and CBR Heart", "acetate odor, vinegar syndrome, channeling, plasticizer, test placeholder, ventilation hold, and chemical-diagnosis refusal", ["LOC-FILM-CARE", "ISO-18911-2010", "W3C-PROV"]),
    ("Nitrate-or-safety classification quarantine with evidence class, uncertainty, isolation alert, escalation, and no-testing or handling instruction", "film-nitrate-quarantine", "THOS Body and CBR Heart", "nitrate or safety classification, evidence class, uncertainty, isolation alert, escalation, and testing or handling refusal", ["LOC-FILM-CARE", "ISO-18906-2000", "W3C-PROV"]),
    ("Inspection-bench path and threading-topology graph with rollers, gates, tension placeholders, stop points, and no-equipment operation", "film-inspection-path", "THOS Body and GMUT Mind", "inspection path, threading topology, rollers, gates, tension placeholders, stop points, and equipment-operation refusal", ["FIAF-TECHNICAL-RESOURCES", "ISO-18911-2010", "W3C-PROV"]),
    ("Head, tail, countdown, cue, changeover, leader, transition, and continuity graph with no-projection instruction", "film-changeover-cue", "THOS Body and GMUT Mind", "head, tail, countdown, cue, changeover, leader, transition, continuity, and projection-instruction refusal", ["FIAF-TECHNICAL-RESOURCES", "PBCORE-21", "W3C-PROV"]),
    ("Projector and archival-element interface reservation with gauge, aperture, soundhead, reel, lamp-heat, tension, and no-compatibility verdict", "film-projector-interface", "THOS Body and CBR Heart", "projector and element interface, gauge, aperture, soundhead, reel, lamp heat, tension, mismatch hold, and compatibility-verdict refusal", ["FIAF-TECHNICAL-RESOURCES", "LOC-FILM-CARE", "W3C-PROV"]),
    ("DPX frame-sequence contract with header fields, frame identity, timecode, file-order, checksum placeholder, and no-digitization claim", "film-dpx-sequence", "GMUT Mind and Freed ID", "DPX header, frame identity, timecode, file order, checksum placeholder, metadata lineage, and digitization-claim refusal", ["FADGI-DPX-METADATA", "FADGI-MOTION-PICTURE", "W3C-PROV"]),
    ("PREMIS object, event, outcome, agent-placeholder, rights-basis, fixity, and preservation-lineage graph with no-real-custody claim", "film-premis-lineage", "Freed ID and CBR Heart", "PREMIS object, event, outcome, agent placeholder, rights basis, fixity, preservation lineage, and real-custody refusal", ["LOC-PREMIS-3", "W3C-PROV", "RFC-3339"]),
    ("GMUT discrete film-transport operator with frame state, sprocket phase, gate boundary, observation placeholder, residual, and empirical firewall", "film-gmut-transport", "GMUT Mind", "typed discrete film-transport operator, frame state, sprocket phase, gate boundary, observation placeholder, residual, and empirical firewall", ["FIAF-TECHNICAL-RESOURCES", "W3C-PROV", "RFC-8785"]),
    ("GMUT optical-temporal identifiability tribunal with source, stock, generation, optics, transport, scanning, processing, and confounding alternatives", "film-gmut-identifiability", "GMUT Mind", "optical-temporal identifiability, source, stock, generation, optics, transport, scanning, processing confounders, and parameter-claim refusal", ["FADGI-MOTION-PICTURE", "W3C-PROV", "RFC-8785"]),
    ("Structurally accessible film-condition, custody, provenance, and hold report with print fallback and manual-evaluation reservation", "film-accessible-report", "CBR Heart and THOS Body", "accessible report headings, table semantics, focus order, non-colour cues, print fallback, custody and hold summaries, and manual-evaluation reservation", ["W3C-WCAG-22", "LOC-PREMIS-3", "NZ-PRIVACY-PRINCIPLES"]),
    ("THOS synthetic inspection, correction, stop-work, readback, and shift-handover proxy with matched event budget and no-worker evidence", "thos-film-inspection-proxy", "THOS Body", "synthetic inspection queue, correction, stop work, matched event budget, interruption log, readback, handover, and worker-evidence refusal", ["RFC-3339", "W3C-WCAG-22", "W3C-PROV"]),
    ("THOS synthetic reel-custody workload and recovery proxy with priorities, two-person placeholder, pause, resumption, escalation, and no-effectiveness estimate", "thos-film-workload-proxy", "THOS Body and CBR Heart", "synthetic reel-custody workload, priority, two-person placeholder, pause, resumption, escalation, and effectiveness-estimate refusal", ["RFC-3339", "LOC-PREMIS-3", "W3C-PROV"]),
    ("Freed ID dual-control reel-handoff challenge with conflicting custody claims, reciprocal confirmation, timeout, annulment, and no bearer status", "freed-id-film-handoff", "Freed ID and CBR Heart", "dual-control reel handoff challenge, conflicting custody claims, reciprocal confirmation, timeout, annulment, and bearer-status refusal", ["W3C-VC-DM-20", "LOC-PREMIS-3", "RFC-3339"]),
    ("Freed ID rights-window field-release budget with purpose binding, withheld-field reasons, correction channel, remedy pointer, and no authorization", "freed-id-film-field-budget", "Freed ID and CBR Heart", "rights-window field-release budget, purpose binding, withheld-field reasons, correction channel, remedy pointer, and authorization refusal", ["W3C-VC-DM-20", "NZ-PRIVACY-PRINCIPLES", "RFC-8785"]),
    ("Freed ID preservation-event pseudonym-rotation lineage with link-secret placeholder, correlation alarm, invalidation, and no unlinkability claim", "freed-id-film-pseudonym-rotation", "Freed ID and THOS Body", "preservation-event pseudonym rotation, link-secret placeholder, correlation alarm, invalidation, and unlinkability-claim refusal", ["W3C-VC-DM-20", "W3C-DATA-INTEGRITY", "LOC-PREMIS-3"]),
    ("FIAF, FADGI, PBCore, and PREMIS external-capability matrix with offline fixture map, version watch, disabled transport, and zero real rows", "film-standards-capability", "All pillars", "external FIAF, FADGI, PBCore, and PREMIS capability matrix, offline fixture map, version watch, disabled transport, and zero-real-row boundary", ["FIAF-TECHNICAL-RESOURCES", "FADGI-DPX-METADATA", "PBCORE-21", "LOC-PREMIS-3"]),
    ("CBR film rights, donor and depositor terms, access, cultural content, traditional knowledge, affected-party remedy, and Māori-data authority covenant", "cbr-film-authority-covenant", "CBR Heart across all pillars", "copyright, donor and depositor terms, access, culturally restricted content, traditional knowledge, affected-party remedy, Māori data, tangata whenua, iwi, hapū, and Māori-authority reservation", ["NZ-PRIVACY-PRINCIPLES", "TE-MANA-RARAUNGA", "LOCAL-CONTEXTS-TK", "W3C-PROV"]),
]


PROPOSALS = [proposal(index, *spec) for index, spec in enumerate(PROPOSAL_SPECS, 1)]


SKILL_SPECS = [
    ("ghc-family-film-intake-custody", "Constrain synthetic inspection purpose, element identity, custody, access hold, abort, and no-handling states."),
    ("ghc-family-film-format-condition", "Constrain gauge, perforation, base, stock, dimensions, damage, uncertainty, and material-diagnosis refusal."),
    ("ghc-family-film-time-image-sound", "Constrain frame cadence, duration, aperture, aspect ratio, soundtrack topology, image-process observations, and presentation refusal."),
    ("ghc-family-film-splice-transition", "Constrain splice lineage, frame loss, leaders, cues, changeovers, transitions, and repair or projection refusal."),
    ("ghc-family-film-nitrate-acetate-rail", "Fail closed around nitrate and acetate uncertainty, hazard, test, chemical, ventilation, handling, and disposition decisions."),
    ("ghc-family-film-dpx-premis", "Constrain DPX frame-sequence metadata and PREMIS object, event, outcome, rights, fixity, and preservation lineage."),
    ("ghc-family-film-gmut-firewall", "Keep transport, optical-temporal identifiability, model, unit, residual, and observation contracts within typed synthetic research bounds."),
    ("ghc-family-film-thos-handover", "Constrain synthetic inspection queues, workload, interruption, stop work, readback, recovery, escalation, and handover."),
    ("ghc-family-film-freed-id", "Constrain synthetic handoff challenge, release budget, pseudonym rotation, correlation alarm, correction, privacy, and nonproduction boundaries."),
    ("ghc-family-film-authority-reservation", "Fail closed around copyright, donor terms, access, cultural content, traditional knowledge, affected parties, and Māori authority."),
]


RUNNER_SPECS = [
    ("ghc_family_film_intake_custody.py", "film-request-quarantine"),
    ("ghc_family_film_format_condition.py", "film-gauge-perforation"),
    ("ghc_family_film_time_image_sound.py", "film-frame-timebase"),
    ("ghc_family_film_splice_transition.py", "film-splice-lineage"),
    ("ghc_family_film_nitrate_acetate_rail.py", "film-nitrate-quarantine"),
    ("ghc_family_film_dpx_premis.py", "film-dpx-sequence"),
    ("ghc_family_film_gmut_firewall.py", "film-gmut-transport"),
    ("ghc_family_film_thos_handover.py", "thos-film-inspection-proxy"),
    ("ghc_family_film_freed_id.py", "freed-id-film-handoff"),
    ("ghc_family_film_authority_reservation.py", "cbr-film-authority-covenant"),
]


def negative(number: int, slug: str, failure: str, recovery: str, guard: str) -> dict:
    return {
        "negative_id": f"V6583-X1-N{number:02d}",
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
    negative(1, "unavailable-shell-command-alias", "The first read-only source probe named an unavailable shell-command alias and produced no audit output.", "Use the supported execution command with the same literal read-only probe.", "Use only tool names present in the active tool surface."),
    negative(2, "powershell-array-syntax-in-js-orchestrator", "A JavaScript orchestration cell used PowerShell array syntax and failed to parse before execution.", "Express the tool-call list as JavaScript values and rerun only the read-only probes.", "Keep orchestration-language syntax distinct from the invoked shell language."),
    negative(3, "powershell-foreach-empty-pipe", "A PowerShell foreach statement was piped directly into JSON conversion and raised an empty-pipe-element parser error.", "Materialize the foreach result in a task-specific variable before JSON conversion.", "Materialize compound PowerShell results before piping."),
    negative(4, "activation-proposal-pointer-drift", "The named source pointer x1/proposals.json was absent even though the proposal ledger was committed elsewhere.", "Resolve and read the exact committed preregistration/proposal-ledger.json through EOF while retaining the pointer drift.", "Confirm packet pointers against the immutable tree before treating absence as missing evidence."),
    negative(5, "combined-large-worktree-status-stall", "A combined source status probe stalled after emitting the head and branch and earned no clean-state credit.", "Split exact head, branch, tracked status, untracked status, divergence, and fresh-remote checks into bounded scalar probes.", "Serialize large-worktree Git status checks."),
    negative(6, "windows-cp1252-proposal-diagnostic", "A read-only proposal diagnostic reached non-CP1252 text and raised a UnicodeEncodeError.", "Set PYTHONIOENCODING=utf-8 and rerun only the bounded diagnostic.", "Set explicit UTF-8 stdout for repository text."),
    negative(7, "parallel-startup-equality-lost-session", "A parallel startup equality probe yielded without a usable session handle and earned no equality credit.", "Run bounded scalar local, upstream, tracking, fresh-live, divergence, and clean checks through completion.", "Do not use an untracked yielded wrapper as evidence."),
    negative(8, "ancestry-expression-exitcode-parse", "An ancestry wrapper placed a command and LASTEXITCODE inside one PowerShell expression and failed to parse.", "Run the command first, capture the exit code in a task-specific scalar, and then render the result.", "Separate command execution from exit-code projection."),
    negative(9, "manifest-future-exclusion-assumption", "The first source-manifest audit assumed every declared evidence exclusion already existed at the evidence commit; two exclusions were later closeout files.", "Replay exact declared entry Git blobs and treat future lifecycle exclusions as exclusions rather than required evidence paths.", "Validate a manifest by its declared entries and hash domain, not by assuming exclusions exist."),
    negative(10, "windows-glob-and-validator-name-assumption", "A source probe passed Windows globs to rg and guessed a validator filename, returning no evidence.", "Enumerate files with rg --files, then inspect literal selected paths.", "Discover exact repository paths before literal reads."),
    negative(11, "post-checkout-combined-probe-lost-session", "A combined post-checkout worktree, index, and frozen-index probe yielded without a usable session handle and earned no evidence.", "Split registered worktree, HEAD, branch, clean, and frozen-index checks into scalar probes.", "Require attributable completion for each terminal startup fact."),
    negative(12, "proposal-summary-output-truncation", "A combined inherited proposal summary exceeded the output envelope; the truncated render earned no whole-ledger credit.", "Parse the frozen chain mechanically and emit bounded count and novelty receipts.", "Do not render compact multi-thousand-row ledgers into the conversational output envelope."),
    negative(13, "powershell-sha256-hashdata-version-assumption", "A read-only route-blob hash probe assumed a newer .NET SHA256.HashData method that was unavailable.", "Use Python hashlib over the exact Git blob and keep the checkout-byte hash in its separate domain.", "Use version-compatible hash APIs and label Git-blob versus checkout-byte domains."),
    negative(14, "powershell-foreach-empty-pipe-recurrence", "A later inherited-ledger key probe repeated the direct foreach-to-pipeline parser error and earned no ledger credit.", "Materialize the rows first and pipe only the completed task-specific collection to JSON conversion.", "Apply the materialization guard consistently to every compound PowerShell foreach result."),
    negative(15, "x1-semantic-novelty-rejection", "The first x1 build rejected V6583-P26, P27, and P28 at 0.8000, 0.6500, and 0.8235 similarity to Sylven's station-custody, selective-disclosure, and response-change proposals; no x1 packet was credited.", "Replace the repeated credential, selective-disclosure, and capability patterns with a dual-control handoff conflict, a field-release budget, and pseudonym-rotation lineage while preserving the 0.60 threshold.", "Treat novelty rejection as evidence of semantic staleness and redesign the mechanism instead of weakening the threshold."),
    negative(16, "x1-staged-review-lifecycle-order", "The first exact staged-path comparison found 40 staged paths but only 38 expected paths because the review and validation receipt were materialized after their expected-set snapshot; it earned zero exact-review credit.", "Rebuild after every lifecycle receipt exists, restage the changed files, and require exact equality between the materialized expected set and the index.", "Materialize review and receipt layers before the final x1 expected-path snapshot and exact index comparison."),
    negative(17, "x1-stale-label-scan-inherited-index-overmatch", "The first x1 stale-label scan searched the compact inherited proposal index, matched intentionally preserved seismic predecessors, and truncated the output; it earned zero hygiene credit.", "Exclude the declared inherited frozen-chain index from narrative stale-label scanning, validate its schema and 2,710-row count separately, and scan only current-phase narratives and configuration.", "Never classify immutable inherited proposal text as a stale current-phase label or render the compact chain into the output envelope."),
    negative(18, "x1-stale-label-glob-base-mismatch", "The first narrowed stale-label recovery used a glob whose base did not match the explicit search root, so the inherited compact index was still scanned and output truncated again.", "Build a literal file inventory, remove the exact frozen-chain path before matching, and report only a bounded hit count.", "Prefer literal prefiltered path inventories over root-relative exclusion globs for large immutable ledgers."),
    negative(19, "parallel-x1-exact-review-lost-attribution", "A parallel final x1 gate returned completed test and whitespace results but no attributable completion for the exact-index probe, which earned zero exact-review credit.", "Run the exact staged-path, manifest, deletion, unstaged, and untracked checks serially through completion.", "Serialize large-worktree terminal index checks and require an explicit exit code and result payload."),
]


SAFE_TASKS = [
    {
        "task_id": f"V6583-SAFE-{index:03d}",
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
        "task_id": f"V6583-CAND-{index:03d}",
        "task": f"Prototype a reversible cross-surface refinement for {PROPOSALS[(index - 1) % len(PROPOSALS)]['slug']}.",
        "approval_class": "candidate_owner_local_review_required",
        "x1_execution": False,
        "planned_lane": "x2_if_bounded_evidence_permits",
    }
    for index in range(1, 21)
]


CLEAN_TASKS = [
    {
        "task_id": f"V6583-CLEAN-{index:03d}",
        "task": f"Run additive compatibility, privacy, provenance, stale-label, and nonpromotion cleanup for {item['slug']}.",
        "approval_class": "safe_now_additive_cleanup",
        "x1_execution": False,
        "planned_lane": "x2",
    }
    for index, item in enumerate(PROPOSALS, 1)
]
