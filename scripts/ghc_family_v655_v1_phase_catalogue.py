#!/usr/bin/env python3
"""Vesper v655-v1 source, proposal, portfolio, and startup-negative catalogue."""

from __future__ import annotations


OFFICIAL_SOURCES = [
    {
        "source_id": "IAU-SOFA-COOKBOOKS",
        "title": "Standards of Fundamental Astronomy — SOFA Cookbooks",
        "publisher": "International Astronomical Union SOFA Board",
        "url": "https://www.iausofa.org/cookbooks",
        "status": "current",
        "use": (
            "astrometry, celestial reference systems, calendars, and seven "
            "time-scale conversion boundaries"
        ),
    },
    {
        "source_id": "NAIF-SPICE-TIME",
        "title": "SPICE Time Subsystem Required Reading",
        "publisher": "NASA Navigation and Ancillary Information Facility",
        "url": "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/time.html",
        "status": "current",
        "use": (
            "UTC, TAI, TT, TDB, leap-second-kernel, J2000, and conversion-order "
            "boundaries"
        ),
    },
    {
        "source_id": "NAIF-SPICE-KERNEL",
        "title": "SPICE Kernel Required Reading",
        "publisher": "NASA Navigation and Ancillary Information Facility",
        "url": "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/kernel.html",
        "status": "current",
        "use": (
            "kernel type, naming, provenance, loading, conflict, and "
            "competing-data boundaries"
        ),
    },
    {
        "source_id": "IAU-FITS-4",
        "title": "Definition of the Flexible Image Transport System, version 4.0",
        "publisher": "International Astronomical Union FITS Working Group",
        "url": "https://fits.gsfc.nasa.gov/fits_standard.html",
        "status": "stable",
        "use": (
            "astronomical image, table, header, world-coordinate, "
            "time-coordinate, and checksum vocabulary"
        ),
    },
    {
        "source_id": "W3C-PROV-O",
        "title": "PROV-O: The PROV Ontology",
        "publisher": "W3C",
        "url": "https://www.w3.org/TR/prov-o/",
        "status": "stable",
        "use": (
            "entity, activity, derivation, revision, responsibility, and "
            "provenance-interchange vocabulary"
        ),
    },
    {
        "source_id": "ISO-14807-2001",
        "title": "ISO 14807:2001 — Densitometer performance reporting",
        "publisher": "International Organization for Standardization",
        "url": "https://www.iso.org/standard/25605.html",
        "status": "current",
        "use": (
            "measurement-performance reporting parameters and "
            "calibration-limit vocabulary only"
        ),
    },
    {
        "source_id": "IEC-62471-7-2023",
        "title": (
            "IEC 62471-7:2023 — Photobiological safety for visible light sources"
        ),
        "publisher": "International Electrotechnical Commission",
        "url": "https://webstore.iec.ch/en/publication/68810",
        "status": "current",
        "use": (
            "visible-light risk-assessment scope and professional safety "
            "reservation only"
        ),
    },
    {
        "source_id": "IAU-WGSN",
        "title": "IAU Working Group on Star Names",
        "publisher": "International Astronomical Union",
        "url": "https://www.iau.org/WG280/WG280/Home.aspx",
        "status": "current",
        "use": (
            "official star-name scope, cultural responsibility, and "
            "no-local-naming-authority boundary"
        ),
    },
    {
        "source_id": "IAU-WGSN-2026",
        "title": "IAU 2026 star-name announcement and cultural-method update",
        "publisher": "International Astronomical Union",
        "url": (
            "https://www.iau.org/Iau/News/Ann2026/New-Star-Names-2026.aspx"
        ),
        "status": "watch",
        "use": (
            "current cultural-astronomy methodology signal and "
            "postponement-when-authority-is-insufficient rule"
        ),
    },
    {
        "source_id": "W3C-WCAG-22",
        "title": "Web Content Accessibility Guidelines 2.2",
        "publisher": "W3C",
        "url": "https://www.w3.org/TR/WCAG22/",
        "status": "stable",
        "use": (
            "text alternatives, captions, audio description, flash, timing, "
            "structure, and manual-evaluation reservations"
        ),
    },
    {
        "source_id": "NZ-OPC-PRINCIPLES",
        "title": "New Zealand Privacy Act 2020 principles",
        "publisher": "Office of the Privacy Commissioner New Zealand",
        "url": "https://www.privacy.org.nz/privacy-principles/",
        "status": "current",
        "use": (
            "purpose, collection, notification, security, access, correction, "
            "retention, and disclosure reservations"
        ),
    },
    {
        "source_id": "TMR-PRINCIPLES",
        "title": "Principles of Māori Data Sovereignty",
        "publisher": "Te Mana Raraunga",
        "url": (
            "https://www.temanararaunga.maori.nz/"
            "principles-of-maori-data-sovereignty"
        ),
        "status": "current",
        "use": (
            "Māori rights, interests, governance, and authority reservation only"
        ),
    },
]


PROPOSAL_ROWS = [
    (
        1,
        "Celestial catalogue intake board with catalogue identity, epoch, frame, "
        "column contract, provenance, checksum, uncertainty, and no-silent-default "
        "rule",
        "celestial-catalogue-intake",
        "GMUT Mind",
        "completed",
        "celestial catalogue intake and assumption boundary",
        ["IAU-FITS-4", "W3C-PROV-O"],
    ),
    (
        2,
        "Celestial reference-frame crosswalk with ICRS, equatorial, ecliptic, "
        "horizontal, origin, epoch, handedness, transformation order, and "
        "mixed-frame refusal",
        "celestial-frame-crosswalk",
        "GMUT Mind",
        "completed",
        "celestial reference-frame crosswalk",
        ["IAU-SOFA-COOKBOOKS", "NAIF-SPICE-KERNEL"],
    ),
    (
        3,
        "Astronomical time-scale normalization ledger with UTC, TAI, TT, TDB, "
        "UT1 placeholder, leap-second-kernel identity, epoch, precision, and "
        "unlabelled-time refusal",
        "astronomical-timescale-ledger",
        "GMUT Mind",
        "completed",
        "astronomical time-scale normalization",
        ["IAU-SOFA-COOKBOOKS", "NAIF-SPICE-TIME"],
    ),
    (
        4,
        "SPICE meta-kernel provenance graph with kernel class, source, digest, "
        "coverage interval, load order, competing datum, supersession, and "
        "implicit-load refusal",
        "spice-kernel-provenance",
        "GMUT Mind",
        "completed",
        "SPICE kernel provenance and load-order boundary",
        ["NAIF-SPICE-KERNEL", "W3C-PROV-O"],
    ),
    (
        5,
        "FITS celestial-product header tribunal with HDU class, WCS keys, units, "
        "time keys, checksum, null semantics, distortion convention, and "
        "header-inference refusal",
        "fits-celestial-header-tribunal",
        "GMUT Mind",
        "completed",
        "FITS celestial header and world-coordinate boundary",
        ["IAU-FITS-4"],
    ),
    (
        6,
        "Planetarium dome geometry survey proxy with dome radius, centre, horizon "
        "ring, zenith, fiducial network, uncertainty, instrument placeholder, and "
        "real-measurement hold",
        "dome-geometry-survey-proxy",
        "THOS Body",
        "represented",
        "dome geometry and fiducial survey proxy",
        ["ISO-14807-2001", "W3C-PROV-O"],
    ),
    (
        7,
        "Projection-channel registration proxy with projector identity, fiducial "
        "pair, pose placeholder, residual map, overlap, confidence, drift signal, "
        "and alignment-release hold",
        "projection-channel-registration",
        "THOS Body",
        "represented",
        "projection channel registration proxy",
        ["ISO-14807-2001", "W3C-PROV-O"],
    ),
    (
        8,
        "Dome distortion-mesh calibration proxy with mesh version, control point, "
        "inverse map, interpolation domain, seam, foldover detector, residual, and "
        "deployment refusal",
        "dome-distortion-mesh",
        "THOS Body",
        "represented",
        "dome distortion mesh and foldover hold",
        ["IAU-FITS-4", "ISO-14807-2001"],
    ),
    (
        9,
        "Projection luminance-uniformity and black-level proxy with patch grid, "
        "meter placeholder, dark adaptation hold, unit, repeat count, uncertainty, "
        "and photometric-claim refusal",
        "projection-luminance-proxy",
        "THOS Body",
        "represented",
        "projection luminance and black-level proxy",
        ["ISO-14807-2001", "IEC-62471-7-2023"],
    ),
    (
        10,
        "Projection chromaticity and channel-balance proxy with primary point, "
        "white-point target, transfer placeholder, gamut boundary, drift, "
        "instrument status, and colour-accuracy refusal",
        "projection-chromaticity-proxy",
        "THOS Body",
        "represented",
        "projection chromaticity and channel-balance proxy",
        ["ISO-14807-2001", "IEC-62471-7-2023"],
    ),
    (
        11,
        "Projector focus and modulation-transfer docket with field position, "
        "target class, spatial-frequency placeholder, scoring rule, uncertainty, "
        "operator hold, and optical-performance refusal",
        "projector-focus-mtf-docket",
        "THOS Body",
        "completed",
        "focus and modulation-transfer evidence docket",
        ["ISO-14807-2001"],
    ),
    (
        12,
        "Multi-projector blend-zone board with overlap mask, gamma placeholder, "
        "seam metric, clipping, saturation, stale-calibration signal, rollback, "
        "and show-release refusal",
        "projector-blend-zone-board",
        "THOS Body",
        "completed",
        "multi-projector blend-zone boundary",
        ["ISO-14807-2001", "W3C-PROV-O"],
    ),
    (
        13,
        "Stray-light and horizon-mask ledger with source class, dome sector, "
        "occultation region, reflection path placeholder, observation condition, "
        "mitigation status, and completeness refusal",
        "stray-light-horizon-mask",
        "THOS Body",
        "completed",
        "stray-light and horizon-mask provenance",
        ["IEC-62471-7-2023", "W3C-PROV-O"],
    ),
    (
        14,
        "Frame-synchronization tribunal with channel clock, frame counter, "
        "timestamp basis, skew budget, dropped-frame signal, resynchronization, "
        "and stable-playback refusal",
        "frame-synchronization-tribunal",
        "THOS Body",
        "completed",
        "projection frame synchronization boundary",
        ["NAIF-SPICE-TIME", "W3C-PROV-O"],
    ),
    (
        15,
        "Planetarium show-cue dependency graph with asset, cue, prerequisite, "
        "clock basis, manual hold, cancellation edge, recovery point, and "
        "autoplay-release refusal",
        "planetarium-show-cue-graph",
        "THOS Body",
        "completed",
        "planetarium show-cue dependency graph",
        ["W3C-PROV-O", "W3C-WCAG-22"],
    ),
    (
        16,
        "Projection calibration drift ledger with baseline version, observation "
        "placeholder, elapsed interval, environmental context, threshold source, "
        "trend, quarantine, and auto-correction refusal",
        "projection-drift-ledger",
        "THOS Body",
        "completed",
        "projection calibration drift and quarantine",
        ["ISO-14807-2001", "W3C-PROV-O"],
    ),
    (
        17,
        "Visible-light exposure and stop-work reservation with source class, "
        "audience distance placeholder, duration, risk-group source, interlock "
        "status, competent review gap, and safety-decision refusal",
        "visible-light-stop-work-reservation",
        "THOS Body",
        "completed",
        "visible-light safety reservation and stop-work boundary",
        ["IEC-62471-7-2023"],
    ),
    (
        18,
        "Planetarium maintenance handover packet with projector state, calibration "
        "age, unresolved anomaly, isolated asset, evidence link, readback, "
        "escalation, and competence-boundary declaration",
        "planetarium-maintenance-handover",
        "THOS Body",
        "completed",
        "planetarium maintenance and calibration handover",
        ["W3C-PROV-O", "ISO-14807-2001"],
    ),
    (
        19,
        "Calibration-instrument custody ledger with instrument class, identifier, "
        "calibration-status placeholder, environment, operator role placeholder, "
        "result linkage, expiry, and authority refusal",
        "calibration-instrument-custody",
        "THOS Body",
        "completed",
        "calibration instrument custody and status boundary",
        ["ISO-14807-2001", "W3C-PROV-O"],
    ),
    (
        20,
        "Planetarium asset rollback envelope with asset digest, dependency, "
        "previous known state, compatibility check, activation hold, rollback "
        "witness, and external-deployment refusal",
        "planetarium-asset-rollback",
        "THOS Body",
        "completed",
        "projection asset rollback and activation hold",
        ["W3C-PROV-O", "IAU-FITS-4"],
    ),
    (
        21,
        "GMUT curved-dome projection tensor with celestial direction, projector "
        "ray, dome intersection, chart transition, Jacobian, singularity set, unit, "
        "and observation firewall",
        "gmut-dome-projection-tensor",
        "GMUT Mind",
        "completed",
        "curved-dome projection tensor firewall",
        ["IAU-SOFA-COOKBOOKS", "IAU-FITS-4"],
    ),
    (
        22,
        "GMUT spectral-radiance transfer field with channel response symbol, "
        "wavelength domain, dome reflectance placeholder, angular kernel, exposure "
        "term, unit, gauge note, and empirical firewall",
        "gmut-spectral-radiance-field",
        "GMUT Mind",
        "completed",
        "spectral-radiance transfer field firewall",
        ["IEC-62471-7-2023", "ISO-14807-2001"],
    ),
    (
        23,
        "GMUT coupled-clock phase field with source oscillator, channel phase, "
        "drift symbol, synchronization edge, reset map, stability domain, unit, and "
        "physical-prediction firewall",
        "gmut-coupled-clock-field",
        "GMUT Mind",
        "completed",
        "coupled-clock phase field firewall",
        ["NAIF-SPICE-TIME", "W3C-PROV-O"],
    ),
    (
        24,
        "THOS projection job charter with dome region, evidence prerequisites, "
        "reversible asset delta, permission ceiling, abort path, witness predicate, "
        "and external-release refusal",
        "thos-projection-task-envelope",
        "THOS Body",
        "completed",
        "typed projection calibration task envelope",
        ["W3C-PROV-O", "NZ-OPC-PRINCIPLES"],
    ),
    (
        25,
        "THOS fail-closed show scheduler with cue DAG, clock source, readiness "
        "predicate, missing-asset hold, accessibility dependency, operator "
        "confirmation placeholder, cancellation, and no-auto-release invariant",
        "thos-show-scheduler",
        "THOS Body",
        "completed",
        "fail-closed planetarium show scheduler",
        ["W3C-PROV-O", "W3C-WCAG-22"],
    ),
    (
        26,
        "Freed ID celestial asset relation profile with catalogue row, SPICE "
        "kernel, FITS HDU, projection mesh, show asset, namespace source, version, "
        "collision, resolver placeholder, privacy, and nonproduction refusal",
        "freed-id-celestial-asset-profile",
        "Freed ID and CBR Heart",
        "completed",
        "celestial and projection asset identifier separation",
        ["IAU-FITS-4", "NAIF-SPICE-KERNEL", "W3C-PROV-O"],
    ),
    (
        27,
        "CBR planetarium claim-provenance ledger with source assertion, "
        "interpretive layer, uncertainty, correction route, affected audience, "
        "review gap, withdrawal state, remedy hold, and no-canon rule",
        "cbr-planetarium-claim-provenance",
        "Freed ID and CBR Heart",
        "completed",
        "planetarium claim provenance and correction boundary",
        ["W3C-PROV-O", "NZ-OPC-PRINCIPLES", "IAU-WGSN"],
    ),
    (
        28,
        "Accessible planetarium calibration report and show explainer with text "
        "alternative, reading order, caption reservation, audio-description "
        "reservation, nonvisual cue, flash warning field, help route, and "
        "manual-evaluation hold",
        "accessible-planetarium-report",
        "THOS Body",
        "completed",
        "accessible planetarium report structure",
        ["W3C-WCAG-22"],
    ),
    (
        29,
        "Real planetarium photometric calibration and professional review adapter "
        "with venue authorization, instrument calibration, measurement plan, "
        "safety assessment, independent reviewer, affected-user evaluation, and "
        "zero-action firewall",
        "real-planetarium-calibration-adapter",
        "THOS Body",
        "open_gap",
        "real planetarium calibration evidence readiness",
        ["ISO-14807-2001", "IEC-62471-7-2023", "W3C-WCAG-22"],
    ),
    (
        30,
        "Tangata whenua, iwi, hapū, Māori authority, cultural astronomy, "
        "mātauranga Māori, star-name, narrative, language, recording, public-show, "
        "access, correction, remedy, and data-governance reservation",
        "maori-cultural-astronomy-authority-reservation",
        "Freed ID and CBR Heart",
        "exact_gate",
        "Māori cultural astronomy and affected-party authority reservation",
        [
            "TMR-PRINCIPLES",
            "IAU-WGSN",
            "IAU-WGSN-2026",
            "NZ-OPC-PRINCIPLES",
        ],
    ),
]


SKILL_IDEAS = [
    "ghc-family-celestial-coordinate-boundary",
    "ghc-family-astronomical-timescale-normalizer",
    "ghc-family-spice-kernel-provenance",
    "ghc-family-dome-geometry-map",
    "ghc-family-projection-channel-registration",
    "ghc-family-photometric-proxy-firewall",
    "ghc-family-show-cue-handover",
    "ghc-family-planetarium-accessibility",
    "ghc-family-celestial-identifier-profile",
    "ghc-family-projection-evidence-firewall",
]


RUNNER_IDEAS = [
    "ghc_family_celestial_coordinate_boundary.py",
    "ghc_family_astronomical_timescale_normalizer.py",
    "ghc_family_spice_kernel_provenance.py",
    "ghc_family_dome_geometry_map.py",
    "ghc_family_projection_channel_registration.py",
    "ghc_family_photometric_proxy_firewall.py",
    "ghc_family_show_cue_handover.py",
    "ghc_family_planetarium_accessibility.py",
    "ghc_family_celestial_identifier_profile.py",
    "ghc_family_v655_v1_suite.py",
]


CLEAN_SURFACES = [
    "celestial frame vocabulary",
    "time-scale declarations",
    "kernel provenance",
    "dome geometry assumptions",
    "projection calibration proxy",
    "privacy boundary",
    "rollback wording",
    "manifest coverage",
    "failure retention",
    "cultural-authority refusal",
]


X1_OPERATIONAL_NEGATIVES = [
    {
        "negative_id": "V6551-X1-N01",
        "signature": "parallel_index_routing_skill_read_timeout",
        "failed": (
            "The first parallel GHC Family Index and routing-reference read "
            "exceeded its wrapper bound and earned no complete-read credit."
        ),
        "recovery": (
            "Read each exact skill and required reference through EOF with one "
            "bounded literal-path operation."
        ),
        "recurrence_guard": (
            "Prefer direct sequential reads for required instruction files on "
            "archive-backed Windows paths."
        ),
        "credit": "retained_negative_zero_initial_pass_credit",
    },
    {
        "negative_id": "V6551-X1-N02",
        "signature": "parallel_method_schema_read_timeout",
        "failed": (
            "The first parallel Method Flow skill and schema read exceeded its "
            "wrapper bound and earned no complete-read credit."
        ),
        "recovery": (
            "Read the Method Flow skill and schema separately through EOF before "
            "recording a method."
        ),
        "recurrence_guard": (
            "Do not rely on short parallel wrappers for required schema reads."
        ),
        "credit": "retained_negative_zero_initial_pass_credit",
    },
    {
        "negative_id": "V6551-X1-N03",
        "signature": "memory_registry_query_timeout",
        "failed": (
            "The first bounded memory-registry query timed out without a usable "
            "result and earned no continuity credit."
        ),
        "recovery": (
            "Use one narrower exact-keyword query and read only the directly "
            "referenced current continuity rows."
        ),
        "recurrence_guard": (
            "Keep memory lookup to exact owner, phase, and route keywords."
        ),
        "credit": "retained_negative_zero_initial_pass_credit",
    },
    {
        "negative_id": "V6551-X1-N04",
        "signature": "broad_phase_script_inventory_output_truncated",
        "failed": (
            "A broad phase-script inventory emitted more content than the tool "
            "surface could return, so the listing was incomplete and zero credit."
        ),
        "recovery": (
            "Enumerate exact filenames with a phase-bounded basename filter and "
            "inspect only the selected builders, validators, and tests."
        ),
        "recurrence_guard": (
            "List names and sizes first; never dump every matching source file."
        ),
        "credit": "retained_negative_zero_initial_pass_credit",
    },
    {
        "negative_id": "V6551-X1-N05",
        "signature": "powershell_branch_probe_parser_error",
        "failed": (
            "The first branch-uniqueness probe embedded native command sequencing "
            "inside a parenthesized assignment and failed PowerShell parsing."
        ),
        "recovery": (
            "Run the native command, capture its exit code in a separate scalar, "
            "then construct the result object."
        ),
        "recurrence_guard": (
            "Do not place semicolon-separated native commands inside a PowerShell "
            "value expression."
        ),
        "credit": "retained_negative_zero_initial_pass_credit",
    },
    {
        "negative_id": "V6551-X1-N06",
        "signature": "combined_uniqueness_live_remote_probe_timeout",
        "failed": (
            "The corrected combined lane-uniqueness and live-remote probe timed "
            "out before returning its complete result."
        ),
        "recovery": (
            "Split local path, local branch, worktree registration, and live-remote "
            "checks; preserve an empty live-remote result as an explicit zero-row "
            "success."
        ),
        "recurrence_guard": (
            "Separate local Git checks from network-backed remote checks."
        ),
        "credit": "retained_negative_zero_initial_pass_credit",
    },
    {
        "negative_id": "V6551-X1-N07",
        "signature": "worktree_add_timeout_late_success",
        "failed": (
            "The additive Vesper worktree command exceeded its wrapper bound while "
            "Git continued materializing the registered checkout."
        ),
        "recovery": (
            "Do not retry; inspect process count, registration, target existence, "
            "branch, head, locks, and cleanliness after convergence."
        ),
        "recurrence_guard": (
            "Never replay an ambiguously timed-out Git mutation before exact-state "
            "convergence."
        ),
        "credit": "retained_negative_zero_initial_pass_credit",
    },
    {
        "negative_id": "V6551-X1-N08",
        "signature": "transitional_worktree_state_audit_timeout",
        "failed": (
            "The first full post-timeout state audit stalled while checkout "
            "processes were still active and returned no complete evidence."
        ),
        "recovery": (
            "Use a scalar process-and-existence probe, wait within a bounded "
            "window for zero Git processes, then inspect Git state."
        ),
        "recurrence_guard": (
            "Avoid worktree-status plumbing while checkout is observably active."
        ),
        "credit": "retained_negative_zero_initial_pass_credit",
    },
    {
        "negative_id": "V6551-X1-N09",
        "signature": "combined_postconvergence_state_audit_timeout",
        "failed": (
            "One combined post-convergence registration, head, branch, diff, and "
            "untracked audit exceeded its wrapper bound before returning output."
        ),
        "recovery": (
            "Run exact head, branch, tracked status, and untracked checks as "
            "separate bounded scalar probes."
        ),
        "recurrence_guard": (
            "Use small scalar Git commands for archive-backed Windows worktrees."
        ),
        "credit": "retained_negative_zero_initial_pass_credit",
    },
    {
        "negative_id": "V6551-X1-N10",
        "signature": "semantic_novelty_threshold_rejected_task_envelope_title",
        "failed": (
            "The first thirty-proposal novelty audit rejected P24 because its "
            "typed-task-envelope title reached token Jaccard 0.615385 against an "
            "inherited book-repair task-envelope title."
        ),
        "recovery": (
            "Replace the shared template phrasing with a projection-job charter "
            "whose mechanism names dome region, asset delta, permission ceiling, "
            "abort path, and external-release refusal."
        ),
        "recurrence_guard": (
            "Audit both mechanism and title tokens against the complete inherited "
            "chain before freezing x1."
        ),
        "credit": "retained_negative_zero_initial_pass_credit",
    },
]
