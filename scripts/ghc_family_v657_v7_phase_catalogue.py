#!/usr/bin/env python3
"""Frozen x1 catalogue for Liora Venn's v657-v7 phase."""

from __future__ import annotations


def source(
    source_id: str,
    title: str,
    publisher: str,
    url: str,
    status: str,
    use: str,
) -> dict:
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
        "OSHA-1910-147",
        "29 CFR 1910.147 Control of hazardous energy",
        "United States Occupational Safety and Health Administration",
        "https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.147",
        "current",
        "hazardous-energy and isolation vocabulary only; no procedure, training, authorization, compliance, or safety determination",
    ),
    source(
        "NIST-ASD-512",
        "NIST Atomic Spectra Database, version 5.12",
        "National Institute of Standards and Technology",
        "https://www.nist.gov/pml/atomic-spectra-database",
        "current",
        "spectral-line field and version vocabulary for a zero-row adapter only; no query, download, observation, identification, likelihood, or astronomical inference",
    ),
    source(
        "NIST-OPTICAL-RADIOMETRY",
        "Principles of Optical Radiometry and Measurement Uncertainty",
        "National Institute of Standards and Technology",
        "https://www.nist.gov/publications/principles-optical-radiometry-and-measurement-uncertainty",
        "stable",
        "radiometric quantity, spectral response, uncertainty, and covariance vocabulary only; no measurement, calibration, conformance, or performance determination",
    ),
    source(
        "BIPM-SI-BROCHURE",
        "The International System of Units (SI Brochure), ninth edition",
        "Bureau International des Poids et Mesures",
        "https://www.bipm.org/en/publications/si-brochure",
        "current",
        "units, dimensions, and quantity-expression obligations only; no measurement or empirical result",
    ),
    source(
        "NIST-SP811",
        "Guide for the Use of the International System of Units",
        "National Institute of Standards and Technology",
        "https://www.nist.gov/pml/special-publication-811",
        "stable",
        "unit-symbol and dimensional-consistency context only; no calibration or measurement authority",
    ),
    source(
        "NIST-SP800-61R3",
        "Incident Response Recommendations and Considerations for Cybersecurity Risk Management",
        "National Institute of Standards and Technology",
        "https://csrc.nist.gov/pubs/sp/800/61/r3/final",
        "current",
        "incident, retained-negative, recovery, communication, and handover vocabulary only",
    ),
    source(
        "W3C-PROV-O",
        "PROV-O: The PROV Ontology",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/prov-o/",
        "stable",
        "entity, activity, attribution, derivation, revision, and invalidation lineage",
    ),
    source(
        "RFC-3339",
        "RFC 3339: Date and Time on the Internet",
        "RFC Editor",
        "https://www.rfc-editor.org/rfc/rfc3339.html",
        "stable",
        "synthetic timestamps, observation windows, expiry, correction, and handover",
    ),
    source(
        "RFC-8785",
        "RFC 8785: JSON Canonicalization Scheme",
        "RFC Editor",
        "https://www.rfc-editor.org/rfc/rfc8785.html",
        "stable",
        "deterministic synthetic contracts, digests, manifests, and receipts",
    ),
    source(
        "W3C-WCAG-22",
        "Web Content Accessibility Guidelines 2.2",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/WCAG22/",
        "current",
        "structural accessibility vocabulary with manual and affected-user evaluation reserved",
    ),
    source(
        "NZ-PRIVACY-PRINCIPLES",
        "Privacy Act 2020 information privacy principles",
        "Office of the Privacy Commissioner New Zealand",
        "https://www.privacy.org.nz/privacy-principles/",
        "current",
        "purpose, collection, fairness, security, access, correction, retention, use, and disclosure reservations only",
    ),
    source(
        "TMR-PRINCIPLES",
        "Principles of Māori Data Sovereignty",
        "Te Mana Raraunga",
        "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
        "current",
        "authority-reservation context only; Māori data governance remains with Māori authorities",
    ),
    source(
        "LOCAL-CONTEXTS-LABELS",
        "Traditional Knowledge and Biocultural Labels",
        "Local Contexts",
        "https://localcontexts.org/labels/about-the-labels/",
        "current",
        "community-defined provenance and protocol vocabulary with community authority reserved",
    ),
    source(
        "W3C-VC-DM-20",
        "Verifiable Credentials Data Model v2.0",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/vc-data-model/",
        "current",
        "synthetic credential vocabulary only; no real issuer, holder, verifier, proof, status, or trust decision",
    ),
    source(
        "W3C-DID-10",
        "Decentralized Identifiers v1.0",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/did-1.0/",
        "stable",
        "synthetic identifier-document vocabulary only; no live method, resolution, key, controller, or trust claim",
    ),
    source(
        "W3C-BITSTRING-STATUS-10",
        "Bitstring Status List v1.0",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/vc-bitstring-status-list/",
        "current",
        "synthetic status and privacy-obligation vocabulary only; no live service, revocation, key, or interoperability event",
    ),
    source(
        "W3C-ETHICAL-WEB",
        "Ethical Web Principles",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/ethical-web-principles/",
        "current",
        "human control, privacy, accessibility, and non-harm vocabulary only; no ethical ratification or affected-party acceptance",
    ),
    source(
        "NZ-HSWA",
        "Health and Safety at Work Act 2015",
        "New Zealand Legislation",
        "https://www.legislation.govt.nz/act/public/2015/0070/latest/whole.html",
        "current",
        "legal-status and competent-role reservation only; no legal interpretation, compliance determination, or operational authorization",
    ),
]


PROTECTED_GATES = [
    "real_workers_optical_engineers_technicians_astronomers_visitors_communities_and_affected_parties",
    "real_observatories_telescopes_mirrors_lenses_filters_coatings_lasers_vacuum_systems_instruments_and_stored_energy",
    "real_alignment_cleaning_coating_pumping_lifting_exposure_observation_measurement_inspection_release_or_use",
    "real_celestial_data_calibrations_spectral_lines_likelihoods_predictions_constraints_and_empirical_gmut_confirmation",
    "professional_optical_engineering_astronomy_radiometry_laser_vacuum_workplace_safety_accessibility_privacy_or_environmental_authority",
    "sensitive_visitor_worker_location_target_image_land_heritage_traditional_knowledge_and_culturally_restricted_information",
    "production_identity_live_keys_signatures_proofs_issuance_resolution_status_revocation_interoperability_recovery_and_trust",
    "privacy_complete",
    "exhaustive_security",
    "complete_accessibility",
    "legal_cultural_land_heritage_environmental_data_governance_and_maori_authority",
    "affected_party_consent_notice_contestation_remedy_collective_governance_and_worker_acceptance",
    "independent_team_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]


def proposal(
    number: int,
    title: str,
    slug: str,
    pillar: str,
    mechanism: str,
    sources: list[str],
    expected_disposition: str,
) -> dict:
    approval = "safe_now_bounded_structural_formal_or_synthetic_software"
    lane = "x2_owner_local_bounded_synthetic"
    if expected_disposition == "open_gap":
        approval = "candidate_external_readiness_without_network_call"
        lane = "x2_owner_local_zero_row_readiness"
    elif expected_disposition == "exact_gate":
        approval = "exact_approval_authorized_affected_party_required"
        lane = "not_executed_authority_reservation"
    return {
        "proposal_id": f"V6577-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar_relation": pillar,
        "mechanism": mechanism,
        "hypothesis": (
            f"A bounded {mechanism} contract can expose falsifiable synthetic obligations "
            "while refusing unsupported empirical, workplace, professional, safety, security, "
            "accessibility, privacy, identity, production, legal, cultural, Māori-authority, "
            "or Stage 20 promotion."
        ),
        "null_or_failure_condition": (
            f"The artifact omits a required {mechanism} obligation, accepts a frozen mutation, "
            "erases a failure, or crosses a protected person, telescope, optic, instrument, "
            "observation, empirical, professional, production, legal, cultural, Māori-authority, "
            "identity, or Stage 20 gate."
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
            "The valid synthetic fixture passes, five preregistered mutations are rejected, and "
            "the receipt grants no real person, observatory, telescope, optic, coating, laser, "
            "vacuum system, instrument, observation, measurement, safety release, professional, "
            "production, legal, cultural, Māori-authority, identity, accessibility-complete, "
            "privacy-complete, security-complete, independent-reproduction, Theory-of-Everything, "
            "or Stage 20 credit."
        ),
        "rollback_or_recovery": (
            "Stop, retain the failed witness at zero credit, rewrite no history, and leave real "
            "people, observatories, telescopes, optics, instruments, records, sibling lanes, "
            "external systems, and authority state unchanged."
        ),
        "protected_gates": PROTECTED_GATES,
        "expected_disposition": expected_disposition,
    }


PROPOSAL_SPECS = [
    ("Telescope configuration-change request with interface-impact map, reversible state delta, redacted science-purpose placeholder, decision-owner hold, abort condition, and precondition lock", "optics-change-request-lock", "Freed ID and CBR Heart", "configuration-change impact, reversible delta, purpose redaction, decision ownership, abort, and precondition refusal", ["W3C-PROV-O", "NZ-PRIVACY-PRINCIPLES", "RFC-3339"]),
    ("Optical substrate blank provenance, material-claim placeholder, serial quarantine, substitution hold, correction lineage, and no-authentication ledger", "optics-substrate-provenance", "GMUT Mind and Freed ID", "substrate provenance, material-claim quarantine, substitution hold, and authentication refusal", ["W3C-PROV-O", "RFC-8785", "NIST-OPTICAL-RADIOMETRY"]),
    ("Optical surface-figure observation envelope with instrument placeholder, quantity, unit, uncertainty, covariance, clock basis, correction lineage, and no-conformance inference", "optics-surface-figure-envelope", "GMUT Mind", "surface-figure observation, units, uncertainty, covariance, correction, and conformance refusal", ["BIPM-SI-BROCHURE", "NIST-SP811", "NIST-OPTICAL-RADIOMETRY"]),
    ("Telescope optical-train topology graph with synthetic mirror, lens, filter, baffle, detector placeholders, interface boundaries, state quarantine, and no-operation rule", "optics-train-topology", "THOS Body and GMUT Mind", "optical-train topology, interface boundary, state quarantine, and operation refusal", ["W3C-PROV-O", "RFC-8785", "NIST-OPTICAL-RADIOMETRY"]),
    ("Optic mount, fixture, handling aid, and metrology-tool custody and condition ledger with inspection placeholder, quarantine, correction, and no-use release", "optics-tool-instrument-custody", "THOS Body and Freed ID", "mount, fixture, handling-aid, and metrology-tool custody, quarantine, and use-release refusal", ["W3C-PROV-O", "RFC-3339", "NZ-HSWA"]),
    ("Optical coating, vacuum, chemical, electrical, and radiation-source hold board with synthetic assets, isolation boundary, stop-work, escalation, and competent-authority reservation", "optics-coating-vacuum-hold", "THOS Body and CBR Heart", "coating, vacuum, chemical, electrical, radiation-source hold, stop-work, and authority reservation", ["OSHA-1910-147", "NZ-HSWA", "W3C-PROV-O"]),
    ("Optical enclosure particulate-ingress and humidity witness board with sampler placeholder, exposure window, quarantine class, reversible containment, and expert cleaning decision reserved", "optics-ingress-quarantine", "THOS Body and CBR Heart", "particulate ingress, humidity witness, exposure window, quarantine, containment, and expert cleaning-decision reservation", ["W3C-PROV-O", "BIPM-SI-BROCHURE", "NZ-HSWA"]),
    ("Optical alignment target, sequence, datum, revision, deviation, replay, uncertainty, rollback, and no-performance-certification schedule graph", "optics-alignment-schedule", "GMUT Mind and THOS Body", "alignment schedule, datum, revision, deviation, replay, uncertainty, rollback, and performance-certification refusal", ["NIST-OPTICAL-RADIOMETRY", "BIPM-SI-BROCHURE", "W3C-PROV-O"]),
    ("GMUT typed geometric and wave-optics domain, coordinate frame, boundary condition, reference state, unit, uncertainty, and observation-firewall obligation board", "gmut-optics-domain-firewall", "GMUT Mind", "typed geometric and wave-optics domain, frame, boundary, reference, unit, uncertainty, and observation firewall", ["BIPM-SI-BROCHURE", "NIST-SP811", "RFC-8785"]),
    ("GMUT diffraction, aperture, pupil, wavelength-domain, point-spread proxy, modulation-transfer proxy, unit, and no-prediction obligation board", "gmut-optics-diffraction-proxy", "GMUT Mind", "diffraction, aperture, pupil, wavelength domain, PSF and MTF proxy, unit, and prediction refusal", ["NIST-OPTICAL-RADIOMETRY", "BIPM-SI-BROCHURE", "NIST-SP811"]),
    ("GMUT aberration and Zernike-basis coefficient frame, normalization, degeneracy, covariance, identifiability, reference-surface, and no-optical-law obligation board", "gmut-optics-aberration-basis", "GMUT Mind", "aberration basis, coefficient frame, normalization, covariance, identifiability, and optical-law refusal", ["NIST-OPTICAL-RADIOMETRY", "BIPM-SI-BROCHURE", "RFC-8785"]),
    ("Optic scratch, dig, scatter, edge, coating cue, examination-method placeholder, illumination condition, uncertainty, disposition hold, and grading-authority reservation board", "optics-surface-cue-hold", "GMUT Mind and CBR Heart", "surface-cue observation, examination placeholder, illumination, uncertainty, hold, and grading-authority reservation", ["NIST-OPTICAL-RADIOMETRY", "W3C-PROV-O", "RFC-3339"]),
    ("Optic curvature, radius, sag, datum, instrument placeholder, calibration epoch, covariance, correction, and no-conformance trace", "optics-curvature-sag-trace", "GMUT Mind", "curvature, radius, sag, datum, instrument placeholder, calibration epoch, covariance, correction, and conformance refusal", ["BIPM-SI-BROCHURE", "NIST-SP811", "W3C-PROV-O"]),
    ("Optical spectral response, throughput, scatter, stray-light, detector-placeholder, wavelength grid, ambiguity, uncertainty, and no-astronomical-inference classifier", "optics-spectral-response-envelope", "GMUT Mind", "spectral response, throughput, scatter, stray light, wavelength grid, ambiguity, uncertainty, and astronomical-inference refusal", ["NIST-OPTICAL-RADIOMETRY", "NIST-ASD-512", "BIPM-SI-BROCHURE"]),
    ("Optic assembly split, merge, recoating, repair, rejection, component-balance, lineage, duplicate-credit, and provenance genealogy graph", "optics-assembly-genealogy", "Freed ID and GMUT Mind", "optic assembly split, merge, recoating, repair, component balance, duplicate-credit, and provenance lineage", ["W3C-PROV-O", "RFC-8785", "BIPM-SI-BROCHURE"]),
    ("Optic mount and fixture revision, fit, alignment, clearance, interference cue, change authority, rollback, and no-instrument-release board", "optics-mount-change", "THOS Body and Freed ID", "mount and fixture revision, fit, alignment, clearance, change authority, rollback, and instrument-release refusal", ["W3C-PROV-O", "NIST-SP800-61R3", "RFC-3339"]),
    ("Vacuum pump, coating chamber, positioner, drive, and optical-bench energy-source isolation, residual-energy, lock placeholder, verification hold, and no-maintenance-release board", "optics-energy-isolation", "THOS Body and CBR Heart", "optical equipment energy isolation, residual energy, lock placeholder, verification hold, and maintenance-release refusal", ["OSHA-1910-147", "NZ-HSWA", "W3C-PROV-O"]),
    ("Telescope interlock transition-causality graph with edge timestamp, debounce window, acknowledgement lineage, unknown-state quarantine, conflicting-sensor branch, and authority-held reset", "optics-interlock-transition-causality", "THOS Body", "interlock transition causality, debounce, acknowledgement lineage, unknown-state quarantine, sensor conflict, and reset-authority reservation", ["NIST-SP800-61R3", "NZ-HSWA", "RFC-3339"]),
    ("Low-light adaptation and night-shift pacing ledger with orientation cue, glare break, task-switch cost, buddy-check placeholder, pause request, and unfinished-state transfer", "optics-low-light-pacing", "THOS Body and CBR Heart", "low-light adaptation, night pacing, orientation, glare break, task-switch cost, buddy-check placeholder, pause, and unfinished-state transfer", ["NZ-HSWA", "W3C-ETHICAL-WEB", "RFC-3339"]),
    ("Dawn-closure observatory turnover with aperture-position placeholder, condensation-risk flag, cryogenic-stabilization window, anomaly owner, evidence pointer, and reciprocal readback", "optics-dawn-closure-handover", "THOS Body and Freed ID", "dawn closure, aperture position, condensation risk, cryogenic stabilization, anomaly ownership, evidence pointer, and reciprocal readback", ["NIST-SP800-61R3", "W3C-PROV-O", "RFC-3339"]),
    ("Multisensory low-light wayfinding contract for public observing with tactile-route placeholder, sensory-trigger warning, assistive-technology fallback, quiet-space option, and affected-user evaluation reservation", "optics-multisensory-wayfinding", "CBR Heart and THOS Body", "multisensory low-light wayfinding, tactile route, sensory trigger, assistive fallback, quiet-space option, and affected-user evaluation reservation", ["W3C-WCAG-22", "W3C-ETHICAL-WEB", "W3C-PROV-O"]),
    ("Observatory visitor, observer, image, target, location, retention, purpose, disclosure, correction, and privacy-minimization ledger", "optics-privacy-minimization", "Freed ID and CBR Heart", "observatory-record purpose, minimization, retention, disclosure, access, correction, and privacy reservation", ["NZ-PRIVACY-PRINCIPLES", "W3C-PROV-O", "RFC-8785"]),
    ("Optical prescription and configuration-integrity attack tree with unauthorized delta, calibration-epoch drift, digest binding, privilege separation, recovery snapshot, and nondeployment boundary", "optics-configuration-integrity", "Freed ID, THOS Body, and CBR Heart", "optical prescription integrity, unauthorized delta, calibration drift, digest binding, privilege separation, recovery snapshot, and deployment refusal", ["NIST-SP800-61R3", "RFC-8785", "NZ-PRIVACY-PRINCIPLES"]),
    ("THOS interrupted-observation recovery-load proxy with equalized event budget, concealed record scoring, abort threshold, reorientation count, and nonparticipant boundary", "thos-optics-interruption-recovery", "THOS Body", "interrupted-observation recovery load, equal event budget, concealed record scoring, abort threshold, reorientation count, and participant refusal", ["NZ-HSWA", "W3C-ETHICAL-WEB", "RFC-3339"]),
    ("THOS night-vigilance and dark-adaptation crossover proxy with circadian-window placeholder, glare recovery, abstention path, sequence counterbalance, and operator-harm stop", "thos-optics-night-vigilance", "THOS Body", "night vigilance, dark adaptation, circadian window, glare recovery, abstention, sequence counterbalance, and operator-harm stop", ["NZ-HSWA", "NIST-SP800-61R3", "RFC-3339"]),
    ("Freed ID synthetic observing-plan audience capsule with purpose window, target-category redaction, selective-disclosure placeholder, expiry, correction, and nonproduction boundary", "freed-id-observing-plan-disclosure", "Freed ID and CBR Heart", "synthetic observing-plan audience capsule, purpose window, target redaction, selective-disclosure placeholder, expiry, correction, and nonproduction boundary", ["W3C-VC-DM-20", "W3C-DID-10", "NZ-PRIVACY-PRINCIPLES"]),
    ("Freed ID synthetic calibration-assertion supersession graph with validity epoch, offline-cache quarantine, stale-state proof placeholder, rollback pointer, and no-live-verification boundary", "freed-id-calibration-supersession", "Freed ID", "synthetic calibration-assertion supersession, validity epoch, offline-cache quarantine, stale-state proof placeholder, rollback, and live-verification refusal", ["W3C-BITSTRING-STATUS-10", "W3C-DID-10", "W3C-VC-DM-20"]),
    ("Thermo-Psyche coherence, phase, interference, visibility, contrast, analogy-domain label, and attention-nonconversion map", "thermo-psyche-coherence-nonconversion", "GMUT Mind and CBR Heart", "coherence, phase, interference, visibility, contrast, analogy domain, and attention nonconversion", ["NIST-OPTICAL-RADIOMETRY", "BIPM-SI-BROCHURE", "W3C-ETHICAL-WEB"]),
    ("NIST Atomic Spectra Database line, level, wavelength, uncertainty, provenance, species placeholder, covariance, version, and zero-row likelihood-refusal adapter", "nist-asd-zero-row-adapter", "GMUT Mind", "NIST ASD version and spectral-line schema, provenance, uncertainty, covariance, zero-row readiness, and likelihood refusal", ["NIST-ASD-512", "BIPM-SI-BROCHURE", "W3C-PROV-O"]),
    ("CBR astronomy heritage, dark skies, land and place, traditional knowledge, target and image privacy, remedy, legal, cultural, data-governance, affected-party, and Māori-authority covenant", "cbr-astronomy-authority-covenant", "CBR Heart", "astronomy heritage, dark skies, land, place, traditional knowledge, privacy, remedy, law, culture, governance, affected-party, and Māori-authority nonautomation", ["TMR-PRINCIPLES", "LOCAL-CONTEXTS-LABELS", "NZ-PRIVACY-PRINCIPLES", "W3C-ETHICAL-WEB"]),
]


PROPOSALS = [
    proposal(
        number,
        title,
        slug,
        pillar,
        mechanism,
        sources,
        "completed"
        if number <= 23
        else "represented"
        if number <= 28
        else "open_gap"
        if number == 29
        else "exact_gate",
    )
    for number, (title, slug, pillar, mechanism, sources) in enumerate(PROPOSAL_SPECS, 1)
]


SKILL_SPECS = [
    ("ghc-family-optics-intake-provenance", "Freeze synthetic observatory job, optic, substrate, custody, correction, and no-work-start boundaries."),
    ("ghc-family-optics-observation-firewall", "Constrain optical quantities, units, uncertainty, covariance, reference states, and inference refusal."),
    ("ghc-family-optics-hazard-boundary", "Fail closed around coating, vacuum, chemicals, radiation sources, energy, interlocks, and authority."),
    ("ghc-family-optics-tool-instrument-custody", "Model synthetic optic, mount, fixture, instrument, condition, change, isolation, and release states."),
    ("ghc-family-optics-surface-observation", "Separate bounded figure, curvature, surface-cue, and spectral envelopes from calibration or conformance."),
    ("ghc-family-optics-shift-handover", "Constrain anomaly, cooling, aperture, isolation, workload, stop-work, readback, and next-owner handover."),
    ("ghc-family-optics-accessibility-privacy", "Structure accessible notices and minimized records while reserving manual and affected-user review."),
    ("ghc-family-optics-gmut-firewall", "Keep geometric, wave, diffraction, aberration, spectral, and zero-row evidence inside typed research bounds."),
    ("ghc-family-optics-freed-id-status", "Constrain synthetic provenance and status profiles without live keys, proofs, resolution, or trust."),
    ("ghc-family-optics-authority-reservation", "Fail closed around safety, profession, astronomy heritage, land, remedy, law, culture, governance, and Māori authority."),
]


RUNNER_SPECS = [
    ("ghc_family_optics_intake_provenance.py", "optics-change-request-lock"),
    ("ghc_family_optics_observation_firewall.py", "optics-surface-figure-envelope"),
    ("ghc_family_optics_hazard_boundary.py", "optics-coating-vacuum-hold"),
    ("ghc_family_optics_tool_instrument_custody.py", "optics-tool-instrument-custody"),
    ("ghc_family_optics_surface_observation.py", "optics-surface-cue-hold"),
    ("ghc_family_optics_shift_handover.py", "optics-dawn-closure-handover"),
    ("ghc_family_optics_accessibility_privacy.py", "optics-multisensory-wayfinding"),
    ("ghc_family_optics_gmut_firewall.py", "gmut-optics-domain-firewall"),
    ("ghc_family_optics_freed_id_status.py", "freed-id-observing-plan-disclosure"),
    ("ghc_family_optics_authority_reservation.py", "cbr-astronomy-authority-covenant"),
]


def negative(number: int, slug: str, failure: str, recovery: str, guard: str) -> dict:
    return {
        "negative_id": f"V6577-X1-N{number:02d}",
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
    negative(1, "powershell-foreach-direct-pipeline-parser-error", "A read-only source-state probe used a direct foreach-to-pipeline form that PowerShell rejected before execution.", "Materialize the bounded array before piping it to JSON.", "Materialize PowerShell iteration output before downstream pipelines."),
    negative(2, "overbroad-exact-head-path-resolver-output-truncation", "An overbroad exact-head resolver matched 7,003 repository files and exceeded useful output before the ordered Orin packet could be attributed.", "Restrict discovery to the exact Orin v657-v6 subtree and named installed-skill paths.", "Never scan the whole historical tree for current-phase guidance."),
    negative(3, "guessed-nonexistent-closeout-validation-path", "A read-only lookup guessed docs/orin-thale/v657-v6/validation/closeout-validation.json, which does not exist.", "Enumerate the immutable exact-final tree and use its exact receipt names.", "Never infer lifecycle artifact names when the exact tree is available."),
    negative(4, "archive-wide-rg-files-maxbuffer-overflow", "An archive-wide rg --files probe exceeded the wrapper maxBuffer and returned no complete bounded inventory.", "Query exact named archive directories and patterns without enumerating the entire archive.", "Bound archive discovery before recursive enumeration."),
    negative(5, "worktree-content-hash-search-timeout", "A content search for an external canonical-receipt digest timed out and reset its helper without finding a repository-backed receipt.", "Do not repeat the search; preserve the digest from the acknowledged activation as activation evidence only.", "Never content-scan a huge worktree after the bounded exact artifact path is established absent."),
    negative(6, "guessed-nonexistent-v6576-x2-test-name", "A read-only test lookup guessed tests/test_ghc_family_v657_v6_x2.py, which is not part of the exact source tree.", "Enumerate the exact test tree before loading a lifecycle suite.", "Never infer per-stage test filenames."),
    negative(7, "worktree-add-session-attribution-lost-during-checkout", "The worktree-add wrapper yielded without preserving its inner session while git reset --hard still held index.lock; a premature status probe displayed a huge transient deletion view.", "Wait for the exact owned Git processes and index lock to clear, then verify the registered branch and materialized tree with scalar probes.", "After an unattributed worktree-add wrapper, audit process, lock, path, branch, and HEAD before status or retry."),
    negative(8, "combined-post-checkout-clean-audit-lost-inner-sessions", "A combined clean-state wrapper did not preserve the inner sessions for long diff, status, and untracked probes, so blank outputs lacked exit-code attribution.", "Run the exact clean-state probes individually and poll each through an attributable exit code.", "Use one scalar Git state probe per supervised session on a large worktree."),
    negative(9, "unicode-sensitive-multihunk-phase-data-patch-rejected", "A multi-hunk phase-data patch mixed ASCII anchors with a differently decoded Māori line and was atomically rejected without changing the file.", "Replace the bounded owner file through apply-patch delete-and-add with explicit UTF-8 text.", "Keep Unicode-sensitive whole-file replacements atomic and independently review the resulting bytes."),
    negative(10, "unnecessary-bootstrap-placeholder-created-and-removed", "An owner-local untracked bootstrap placeholder was created and immediately removed before any staging because it was not required for the x1 edit surface.", "Retain the no-credit workflow lapse and keep only declared x1 files.", "Do not create sentinel files when apply-patch can directly target the intended owner file."),
    negative(11, "dynamic-unused-template-removal-patch-decoding-mismatch", "A generated apply-patch removal for an inert migration template used PowerShell-decoded text that did not byte-match the UTF-8 source and was atomically rejected.", "Leave the template explicitly marked inert and route all generated output through the reviewed v657-v7 overview function.", "Do not build exact patches from a shell-decoded Unicode round trip; use stable ASCII anchors or direct UTF-8 patch text."),
    negative(12, "first-full-frozen-chain-novelty-screen-rejected-twelve", "The first complete 2,590-row novelty screen rejected twelve proposal titles at or above the 0.60 token-set Jaccard threshold, mostly against Orin's immediately preceding forge structures.", "Redesign the affected mechanisms around configuration change, ingress quarantine, interlock causality, low-light pacing, dawn turnover, multisensory wayfinding, configuration integrity, interruption recovery, night vigilance, audience-limited observing plans, calibration supersession, and coherence nonconversion, then rerun the full screen.", "Treat predecessor analogues as semantic collision evidence and change the mechanism, not only the domain noun or title."),
]


SAFE_TASKS = [
    {
        "task_id": f"V6577-SAFE-{index:03d}",
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
        "task_id": f"V6577-CAND-{index:03d}",
        "task": (
            "Prototype a reversible cross-surface refinement for "
            f"{PROPOSALS[(index - 1) % len(PROPOSALS)]['slug']}."
        ),
        "approval_class": "candidate_owner_local_review_required",
        "x1_execution": False,
        "planned_lane": "x2_if_bounded_evidence_permits",
    }
    for index in range(1, 21)
]
CLEAN_TASKS = [
    {
        "task_id": f"V6577-CLEAN-{index:03d}",
        "task": (
            "Run additive compatibility, privacy, provenance, stale-label, "
            f"and nonpromotion cleanup for {item['slug']}."
        ),
        "approval_class": "safe_now_additive_cleanup",
        "x1_execution": False,
        "planned_lane": "x2",
    }
    for index, item in enumerate(PROPOSALS, 1)
]
