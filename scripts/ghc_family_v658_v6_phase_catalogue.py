#!/usr/bin/env python3
"""Frozen x1 catalogue for Neris Solane's solo v658-v6 phase."""

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
    source("USGS-VHP-WHAT-WE-DO", "What We Do - Volcano Hazards Program", "U.S. Geological Survey", "https://www.usgs.gov/programs/VHP/what-we-do-volcano-hazards-program", "current", "monitoring, assessment, research, and hazard-information vocabulary only; no operational or scientific credit"),
    source("USGS-VOLCANO-MONITORING", "Volcano Monitoring", "U.S. Geological Survey Cascades Volcano Observatory", "https://www.usgs.gov/observatories/cvo/science/volcano-monitoring", "current", "seismic, deformation, gas, hydrologic, thermal, visual, and satellite monitoring vocabulary only"),
    source("USGS-VHP-STRATEGY", "Volcano Hazards Program Strategic Science Plan 2022-2026", "U.S. Geological Survey", "https://www.usgs.gov/publications/volcano-hazards-program-strategic-science-plan-2022-2026", "published", "multi-instrument strategy and uncertainty context only; no plan adoption or conformance claim"),
    source("GEONET-VAB", "Volcanic Alert Bulletin", "GeoNet", "https://www.geonet.org.nz/volcano/vab", "current_watch", "public bulletin and alert-language boundary vocabulary only; no bulletin reproduction, alert, or advice"),
    source("GEONET-HOW", "How we monitor New Zealand volcanoes", "GeoNet", "https://www.geonet.org.nz/volcano/how", "current", "Aotearoa monitoring-method vocabulary only; no real station, observation, or authority claim"),
    source("GEONET-VOLCANO-DATA", "Volcano monitoring data", "GeoNet", "https://www.geonet.org.nz/data/types/volcano_monitoring", "current", "data-type and access-context vocabulary only; no download, transport, or row"),
    source("GEONET-TUTORIALS", "Data access tutorials", "GeoNet", "https://www.geonet.org.nz/data/access/tutorials", "current_watch", "capability-interface vocabulary only; every external transport remains disabled"),
    source("GNS-VOLCANO-MONITORING", "Volcano monitoring", "GNS Science", "https://www.gns.cri.nz/our-science/natural-hazards-and-risks/volcanoes/volcano-monitoring/", "current", "monitoring-system context only; no professional, operational, or institutional endorsement"),
    source("WOVODAT", "WOVOdat", "World Organization of Volcano Observatories", "https://www.wovodat.org/", "current_watch", "volcanic-unrest database capability vocabulary only; no query, row, analysis, or interoperability"),
    source("WOVODAT-DOCS", "WOVOdat documentation", "World Organization of Volcano Observatories", "https://www.wovodat.org/doc/", "current_watch", "database category and schema-context vocabulary only; no conformance claim"),
    source("GVP", "Global Volcanism Program", "Smithsonian Institution", "https://volcano.si.edu/gvp_about.cfm", "current_watch", "volcano catalogue and chronology context only; no real identity, location, event, or dataset ingestion"),
    source("FDSN-STATIONXML", "FDSN StationXML", "International Federation of Digital Seismograph Networks", "https://docs.fdsn.org/projects/stationxml/en/latest/overview.html", "current", "station-metadata vocabulary only; no parser or network conformance"),
    source("FDSN-MSEED3", "FDSN miniSEED 3", "International Federation of Digital Seismograph Networks", "https://docs.fdsn.org/projects/miniseed3", "current", "waveform-record vocabulary only; no binary data or format conformance"),
    source("FDSN-WEBSERVICES", "FDSN Web Services", "International Federation of Digital Seismograph Networks", "https://www.fdsn.org/webservices/", "current_watch", "service capability vocabulary only; network access and real rows remain disabled"),
    source("OGC-OMS", "Observations, Measurements and Samples", "Open Geospatial Consortium", "https://www.ogc.org/publications/standard/om/", "current", "observation, result, sampling, feature-of-interest, and procedure vocabulary only"),
    source("OGC-SENSORTHINGS", "SensorThings API", "Open Geospatial Consortium", "https://www.ogc.org/standards/sensorthings/", "current", "sensor/observation relationship vocabulary only; no API or interoperability conformance"),
    source("COPERNICUS-SENTINEL1", "Sentinel-1 documentation", "Copernicus Data Space Ecosystem", "https://documentation.dataspace.copernicus.eu/Data/Sentinel1.html", "current_watch", "SAR acquisition, orbit, geometry, and product vocabulary only; no imagery or processing"),
    source("W3C-PROV", "PROV-O: The PROV Ontology", "World Wide Web Consortium", "https://www.w3.org/TR/prov-o/", "stable", "entity, activity, derivation, revision, invalidation, and attribution lineage"),
    source("W3C-WCAG-22", "Web Content Accessibility Guidelines 2.2", "World Wide Web Consortium", "https://www.w3.org/TR/WCAG22/", "current", "machine-checkable structure and notice vocabulary; manual and affected-user evaluation remain reserved"),
    source("W3C-VC-DM-20", "Verifiable Credentials Data Model v2.0", "World Wide Web Consortium", "https://www.w3.org/TR/vc-data-model-2.0/", "current", "synthetic nonproduction artifact-envelope vocabulary only; no live identity, proof, or trust"),
    source("W3C-DATA-INTEGRITY", "Verifiable Credential Data Integrity 1.0", "World Wide Web Consortium", "https://www.w3.org/TR/vc-data-integrity/", "current", "proof-configuration vocabulary only; no key, signature, verification, security, or interoperability claim"),
    source("RFC-8785", "JSON Canonicalization Scheme", "RFC Editor", "https://www.rfc-editor.org/rfc/rfc8785.html", "stable", "deterministic JSON representation vocabulary only; no cryptographic assurance"),
    source("NZ-PRIVACY-PRINCIPLES", "Privacy principles", "Office of the Privacy Commissioner New Zealand", "https://www.privacy.org.nz/privacy-principles/", "current", "purpose, minimization, correction, retention, use, and disclosure reservations only; no legal advice"),
    source("TE-MANA-RARAUNGA", "Principles of Māori Data Sovereignty", "Te Mana Raraunga", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "current", "Māori data rights, interests, governance, collective benefit, and authority reservation only"),
    source("LOCAL-CONTEXTS-TK", "Traditional Knowledge Labels", "Local Contexts", "https://localcontexts.org/labels/traditional-knowledge-labels/", "current_watch", "community-defined notice and authority-reservation context only; no label selection or application"),
]


PROTECTED_GATES = [
    "real_people_participants_scientists_engineers_observatories_agencies_communities_and_affected_parties",
    "real_maunga_volcanoes_stations_instruments_locations_waveforms_images_samples_coordinates_observations_and_datasets",
    "real_download_ingestion_processing_interpretation_diagnosis_forecast_alert_hazard_message_publication_or_operational_decision",
    "professional_volcanology_geophysics_geochemistry_remote_sensing_engineering_science_privacy_security_or_accessibility_authority",
    "empirical_gmut_prediction_constraint_force_flow_or_confirmation",
    "blind_matched_budget_thos_real_arms_and_independent_review",
    "production_identity_live_keys_signatures_proofs_issuance_resolution_status_revocation_interoperability_recovery_and_trust",
    "privacy_complete",
    "exhaustive_security",
    "complete_accessibility",
    "legal_cultural_language_land_data_governance_and_maori_authority",
    "affected_party_consent_notice_contestation_remedy_collective_governance_and_acceptance",
    "independent_team_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]


def proposal(number: int, title: str, slug: str, pillar: str, mechanism: str, sources: list[str]) -> dict:
    if number <= 23:
        expected, approval, lane = "completed", "safe_now_bounded_structural_formal_or_synthetic_software", "x2_owner_local_bounded_synthetic"
    elif number <= 28:
        expected, approval, lane = "represented", "candidate_proxy_protocol_or_nonproduction_schema", "x2_owner_local_representation_only"
    elif number == 29:
        expected, approval, lane = "open_gap", "candidate_external_data_readiness_without_transport_or_real_rows", "x2_owner_local_zero_row_readiness"
    else:
        expected, approval, lane = "exact_gate", "outside_hamish_authority_affected_party_legal_cultural_and_maori_authority_required", "not_executed_authority_reservation"
    return {
        "proposal_id": f"V6586-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar_relation": pillar,
        "mechanism": mechanism,
        "hypothesis": f"A bounded {mechanism} contract can expose falsifiable synthetic obligations while refusing unsupported empirical, professional, production, legal, cultural, Māori-authority, identity, privacy-complete, accessibility-complete, Theory-of-Everything, or Stage 20 promotion.",
        "null_or_failure_condition": f"The artifact omits a required {mechanism} obligation, accepts a frozen mutation, erases a failure, or crosses a protected data, person, scientific, professional, production, rights, legal, cultural, Māori-authority, identity, or Stage 20 gate.",
        "approval_class": approval,
        "execution_lane": lane,
        "official_or_primary_source_needs": sources,
        "concrete_artifacts": [f"surfaces/{slug}/contract.json", f"surfaces/{slug}/mutation-results.json", f"surfaces/{slug}/bounded-receipt.json"],
        "falsifier_or_acceptance_gate": "The valid synthetic fixture passes, five preregistered mutations are rejected, and the receipt grants no real-data, empirical, monitoring, diagnosis, forecast, alert, participant, professional, production, legal, cultural, Māori-authority, identity, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, Theory-of-Everything, or Stage 20 credit.",
        "rollback_or_recovery": "Stop, retain the failed witness at zero credit, rewrite no history, and leave people, maunga, observatories, data, instruments, sibling lanes, external systems, rights, and authority state unchanged.",
        "protected_gates": PROTECTED_GATES,
        "expected_disposition": expected,
    }


PROPOSAL_SPECS = [
    ("Synthetic volcanic-observatory scope card with fictional source aliases, redacted location fields, zero real data, and no-operational-use lock", "volcano-observatory-scope-card", "All pillars", "synthetic observatory scope, fictional aliases, location redaction, zero-row state, and operational-use refusal", ["USGS-VHP-WHAT-WE-DO", "GEONET-HOW", "W3C-PROV"]),
    ("Synthetic volcano and source identity passport with fictional aliases, feature-class placeholders, location suppression, revision lineage, and no real-world resolution", "volcano-source-identity-passport", "GMUT Mind and Freed ID", "fictional source identity, alias, feature class, location suppression, revision lineage, and resolution refusal", ["GVP", "W3C-PROV", "NZ-PRIVACY-PRINCIPLES"]),
    ("Instrument and network epoch ledger with synthetic station aliases, sensor classes, response placeholders, maintenance windows, and no deployment claim", "volcano-instrument-epoch-ledger", "GMUT Mind and THOS Body", "instrument and network epochs, sensor class, response placeholder, maintenance lineage, and deployment refusal", ["FDSN-STATIONXML", "OGC-SENSORTHINGS", "W3C-PROV"]),
    ("Observation-event envelope with phenomenon time, result time, procedure, units, uncertainty, quality state, derivation, and no measured value", "volcano-observation-event-envelope", "GMUT Mind and Freed ID", "observation event, phenomenon and result times, procedure, units, uncertainty, quality state, and value refusal", ["OGC-OMS", "OGC-SENSORTHINGS", "W3C-PROV"]),
    ("Seismic waveform record boundary with synthetic channel metadata, timing quality, gap mask, calibration placeholder, and no event interpretation", "volcano-seismic-waveform-boundary", "GMUT Mind", "seismic waveform metadata, timing quality, gaps, calibration placeholder, format boundary, and interpretation refusal", ["FDSN-MSEED3", "FDSN-STATIONXML", "USGS-VOLCANO-MONITORING"]),
    ("Synthetic seismic-event classification docket with feature placeholders, alternate classes, abstention threshold, review state, and no diagnosis", "volcano-seismic-classification-docket", "GMUT Mind and CBR Heart", "synthetic seismic-event features, alternative classes, abstention threshold, review state, and diagnosis refusal", ["USGS-VOLCANO-MONITORING", "GEONET-HOW", "W3C-PROV"]),
    ("GNSS coordinate and baseline provenance card with frame epoch, synthetic displacement placeholders, covariance, outage state, and no deformation result", "volcano-gnss-deformation-card", "GMUT Mind", "GNSS frame epoch, coordinate and baseline provenance, displacement placeholder, covariance, outage, and deformation-result refusal", ["USGS-VOLCANO-MONITORING", "GEONET-VOLCANO-DATA", "OGC-OMS"]),
    ("Tilt and strain time-series contract with orientation, scale, drift, thermal coupling, gap policy, uncertainty, and no ground-motion conclusion", "volcano-tilt-strain-contract", "GMUT Mind", "tilt and strain orientation, scale, drift, thermal coupling, gaps, uncertainty, and ground-motion refusal", ["USGS-VOLCANO-MONITORING", "GEONET-HOW", "OGC-OMS"]),
    ("InSAR acquisition-pair ledger with synthetic product identifiers, orbit and geometry placeholders, coherence mask, atmosphere hold, and no displacement map", "volcano-insar-pair-ledger", "GMUT Mind and Freed ID", "SAR pair identity, orbit, geometry, coherence, atmospheric hold, provenance, and displacement-map refusal", ["COPERNICUS-SENTINEL1", "USGS-VOLCANO-MONITORING", "W3C-PROV"]),
    ("Volcanic-gas observation chain with synthetic SO2, CO2 and H2S channel placeholders, units, wind dependency, detection limits, and no flux conclusion", "volcano-gas-observation-chain", "GMUT Mind", "gas channel, units, wind dependency, detection limits, uncertainty, custody, and flux-conclusion refusal", ["USGS-VOLCANO-MONITORING", "GEONET-HOW", "OGC-OMS"]),
    ("MultiGAS calibration and cross-sensitivity ledger with synthetic standards, zero-span state, interference matrix, drift, quarantine, and no concentration claim", "volcano-multigas-calibration-ledger", "GMUT Mind and THOS Body", "MultiGAS calibration, standards, zero-span state, cross-sensitivity, drift, quarantine, and concentration-claim refusal", ["GNS-VOLCANO-MONITORING", "GEONET-VOLCANO-DATA", "W3C-PROV"]),
    ("Water and fumarole geochemistry sample-custody docket with synthetic aliquots, preservation, method placeholders, detection limits, amendments, and no composition result", "volcano-geochemistry-custody-docket", "GMUT Mind and CBR Heart", "sample custody, aliquot, preservation, analytical method placeholder, detection limit, amendment, and composition-result refusal", ["USGS-VOLCANO-MONITORING", "OGC-OMS", "W3C-PROV"]),
    ("Thermal sensor and imaging observation envelope with synthetic band, emissivity, atmospheric correction, saturation mask, uncertainty, and no heat-flux result", "volcano-thermal-observation-envelope", "GMUT Mind", "thermal band, emissivity, atmospheric correction, saturation, uncertainty, lineage, and heat-flux refusal", ["USGS-VOLCANO-MONITORING", "GEONET-HOW", "OGC-OMS"]),
    ("Camera image provenance card with fictional viewpoint, capture window, weather, illumination, occlusion, redaction, and no visual interpretation", "volcano-camera-provenance-card", "GMUT Mind and CBR Heart", "camera capture, fictional viewpoint, weather, illumination, occlusion, redaction, and interpretation refusal", ["USGS-VOLCANO-MONITORING", "GEONET-HOW", "W3C-PROV"]),
    ("Acoustic and infrasound detection board with synthetic array geometry, bandpass, association alternatives, weather coupling, and no-event claim", "volcano-acoustic-detection-board", "GMUT Mind", "acoustic array geometry, processing placeholders, association alternatives, weather coupling, uncertainty, and event-claim refusal", ["USGS-VHP-STRATEGY", "FDSN-STATIONXML", "OGC-OMS"]),
    ("Hydrothermal lake, spring and bore time-series register with synthetic level, temperature and chemistry placeholders, datum lineage, gaps, and no unrest claim", "volcano-hydrothermal-series-register", "GMUT Mind", "hydrothermal level, temperature, chemistry placeholders, datum lineage, gaps, uncertainty, and unrest-claim refusal", ["USGS-VOLCANO-MONITORING", "GEONET-VOLCANO-DATA", "OGC-OMS"]),
    ("Meteorological covariate register with synthetic wind, pressure, precipitation and cloud channels, station-distance class, gaps, and no causal adjustment claim", "volcano-meteorological-covariates", "GMUT Mind", "meteorological covariates, station-distance class, timing, gaps, uncertainty, and causal-adjustment refusal", ["USGS-VOLCANO-MONITORING", "GEONET-HOW", "OGC-OMS"]),
    ("Multistream missingness, gap, outlier and quarantine ledger with reason codes, imputation prohibition, reviewer hold, and no completeness claim", "volcano-data-quality-quarantine", "GMUT Mind and THOS Body", "missingness, gaps, outliers, quarantine, reason codes, reviewer hold, and completeness refusal", ["OGC-OMS", "W3C-PROV", "USGS-VHP-STRATEGY"]),
    ("Multi-parameter time, coordinate and uncertainty alignment matrix with synthetic offsets, resampling policy, conflict hold, and no fused observation", "volcano-multistream-alignment", "GMUT Mind and THOS Body", "multistream time and coordinate alignment, uncertainty propagation, resampling, conflict hold, and fusion refusal", ["OGC-OMS", "FDSN-STATIONXML", "W3C-PROV"]),
    ("Change-point and anomaly candidate ledger with synthetic score placeholders, baseline version, alternate explanations, review queue, and no forecast", "volcano-anomaly-candidate-ledger", "GMUT Mind", "change-point and anomaly candidate, baseline version, alternate explanation, review, uncertainty, and forecast refusal", ["USGS-VHP-STRATEGY", "GEONET-VAB", "W3C-PROV"]),
    ("Uncertainty and alert-wording firewall with synthetic evidence tier, uncertainty class, forbidden operational phrases, escalation hold, and no public message", "volcano-alert-wording-firewall", "GMUT Mind and CBR Heart", "uncertainty tier, alert wording, prohibited promotion, escalation hold, provenance, and public-message refusal", ["GEONET-VAB", "USGS-VHP-WHAT-WE-DO", "W3C-PROV"]),
    ("Blinded synthetic unrest-scenario injection and recovery protocol with commitment digest, withheld labels, scoring plan, reveal gate, and no predictive-skill claim", "volcano-synthetic-unrest-injection", "GMUT Mind and Freed ID", "blinded synthetic unrest scenario, commitment, withheld label, score, reveal gate, recovery, and predictive-skill refusal", ["RFC-8785", "W3C-PROV", "USGS-VHP-STRATEGY"]),
    ("GMUT typed volcanic-system forward operator with synthetic latent states, observation channels, identifiability matrix, falsifier registry, and no physical-law claim", "gmut-volcano-forward-operator", "GMUT Mind", "typed volcanic-system forward operator, latent state, observation channel, identifiability, falsifier, and physical-law refusal", ["USGS-VOLCANO-MONITORING", "OGC-OMS", "W3C-PROV"]),
    ("THOS channel-batch execution receipt with checkpoint lineage, bounded retries, abandoned-work isolation, and performance abstention", "thos-volcano-shard-checkpoint", "THOS Body", "deterministic multistream shard, checkpoint, partition digest, retry budget, orphan quarantine, and throughput-claim refusal", ["W3C-PROV", "RFC-8785", "OGC-OMS"]),
    ("THOS synthetic observatory duty-shift handover proxy with queue digest, unresolved anomaly register, acknowledgement placeholder, and no operational handover", "thos-volcano-duty-handover", "THOS Body and CBR Heart", "synthetic duty-shift handover, queue digest, unresolved anomaly, acknowledgement placeholder, and operational-handover refusal", ["USGS-VHP-STRATEGY", "GEONET-VAB", "W3C-PROV"]),
    ("Nonproduction Freed ID lineage capsule for fictional sensor records with content fingerprint, ancestry, correction window, sunset state, and trust abstention", "freed-id-volcano-observation-envelope", "Freed ID", "synthetic observation-provenance envelope, digest, derivation, amendment, expiry, revocation hold, and live-proof refusal", ["W3C-VC-DM-20", "W3C-DATA-INTEGRITY", "W3C-PROV"]),
    ("Nonproduction Freed ID observatory notice with intended use, prohibited use, uncertainty, change history, challenge channel, and decision abstention", "freed-id-volcano-model-card", "Freed ID and CBR Heart", "model-card and alert-draft purpose, assumptions, exclusions, limitations, contest route, provenance, and trust-decision refusal", ["W3C-VC-DM-20", "NZ-PRIVACY-PRINCIPLES", "W3C-PROV"]),
    ("Keyboard-readable multistream evidence map with heading hierarchy, text-coded states, source links, narrow-width layout, and reserved human evaluation", "volcano-accessible-evidence-atlas", "CBR Heart and THOS Body", "accessible observatory evidence atlas, scoped tables, noncolour states, provenance, reflow, and manual-evaluation reservation", ["W3C-WCAG-22", "W3C-PROV", "NZ-PRIVACY-PRINCIPLES"]),
    ("WOVOdat, GeoNet and USGS zero-row capability gateway with source watch, disabled transport, schema placeholders, and no external validation", "volcano-zero-row-capability-gateway", "All pillars", "external volcano-data capability, source watch, disabled transport, schema placeholders, zero rows, and external-validation refusal", ["WOVODAT", "GEONET-TUTORIALS", "FDSN-WEBSERVICES"]),
    ("CBR land, maunga, mātauranga, sensitive-location, affected-community, hazard-message, remedy and Māori-authority covenant", "cbr-volcano-authority-covenant", "CBR Heart across all pillars", "land and maunga relationships, mātauranga, sensitive locations, affected communities, hazard messages, remedy, collective governance, and Māori-authority reservation", ["TE-MANA-RARAUNGA", "LOCAL-CONTEXTS-TK", "NZ-PRIVACY-PRINCIPLES"]),
]


PROPOSALS = [proposal(index, *spec) for index, spec in enumerate(PROPOSAL_SPECS, 1)]


SKILL_SPECS = [
    ("ghc-family-volcano-scope-firewall", "Constrain fictional source identities, redacted locations, zero rows, and no operational use."),
    ("ghc-family-volcano-observation-provenance", "Constrain observation, sensor, sample, unit, uncertainty, quality, and derivation records."),
    ("ghc-family-volcano-seismic-acoustic", "Constrain waveform and acoustic metadata, gaps, timing, classification abstention, and no-event claims."),
    ("ghc-family-volcano-deformation-insar", "Constrain GNSS, tilt, strain, and InSAR metadata, geometry, uncertainty, and displacement abstention."),
    ("ghc-family-volcano-gas-geochemistry", "Constrain gas channels, calibration, cross-sensitivity, sample custody, detection limits, and result abstention."),
    ("ghc-family-volcano-thermal-visual", "Constrain thermal, camera, hydrothermal, and weather provenance, masks, redaction, and interpretation abstention."),
    ("ghc-family-volcano-multistream-assurance", "Constrain quality quarantine, alignment, anomaly candidates, alert wording, injections, and typed forward operators."),
    ("ghc-family-volcano-thos-handover", "Constrain deterministic shards, checkpoints, retry, quarantine, and synthetic handover proxies."),
    ("ghc-family-volcano-freed-id-provenance", "Constrain synthetic observation envelopes, model cards, digests, amendments, expiry, and revocation holds."),
    ("ghc-family-volcano-authority-reservation", "Fail closed around people, maunga, mātauranga, sensitive locations, hazard messages, law, culture, and Māori authority."),
]


RUNNER_SPECS = [
    ("ghc_family_volcano_scope_firewall.py", "volcano-observatory-scope-card"),
    ("ghc_family_volcano_observation_provenance.py", "volcano-observation-event-envelope"),
    ("ghc_family_volcano_seismic_acoustic.py", "volcano-seismic-waveform-boundary"),
    ("ghc_family_volcano_deformation_insar.py", "volcano-gnss-deformation-card"),
    ("ghc_family_volcano_gas_geochemistry.py", "volcano-gas-observation-chain"),
    ("ghc_family_volcano_thermal_visual.py", "volcano-thermal-observation-envelope"),
    ("ghc_family_volcano_multistream_assurance.py", "volcano-multistream-alignment"),
    ("ghc_family_volcano_thos_handover.py", "thos-volcano-duty-handover"),
    ("ghc_family_volcano_freed_id_provenance.py", "freed-id-volcano-observation-envelope"),
    ("ghc_family_volcano_authority_reservation.py", "cbr-volcano-authority-covenant"),
]


def negative(number: int, slug: str, failure: str, recovery: str, guard: str) -> dict:
    return {
        "negative_id": f"V6586-X1-N{number:02d}",
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
    negative(1, "compound-source-state-probe-no-serialization", "The first compound PowerShell source-state object returned no serialized evidence after its initial status marker.", "Repeat each branch, head, cleanliness, upstream, and equality probe as an isolated scalar read.", "Do not rely on an unserialized compound native-command object for source-state evidence."),
    negative(2, "powershell-foreach-empty-pipeline", "The first manifest inventory piped a foreach expression directly and PowerShell rejected an empty pipeline element before manifest verification.", "Materialize the foreach results into a collection before any pipeline or serialization step.", "Never place a foreach expression directly at a PowerShell pipeline boundary."),
    negative(3, "broad-rg-windows-glob-output-overload", "Broad ripgrep audits used an invalid Windows wildcard and later traversed pervasive historical terms, producing noisy or context-truncated evidence; a copied-file audit repeated the wildcard form. The first post-build stale-label audit then used an unbounded three-letter inherited-domain substring that matched ordinary words and ineffective rooted exclusions that exposed inherited provenance, producing another huge false-positive stream. Its first bounded recovery still matched that literal inside the retained incident description itself.", "Use an explicit active-file allowlist, semantically named word-bounded stale tokens, scalar route-value assertions, and bounded output.", "Predeclare exact files and semantic or word-bounded terms; treat wildcard, substring, self-match, exclusion, and output-overload recurrences as the same retained method failure."),
    negative(4, "target-uniqueness-parenthesis-parser-fault", "The first target uniqueness wrapper used an invalid parenthesized PowerShell form and failed before completing path, branch, remote, and registration checks.", "Run path, local branch, remote branch, and worktree registration as four isolated scalar probes.", "Separate native command execution from PowerShell expression grouping."),
    negative(5, "worktree-checkout-partial-progress-timeout", "The worktree-add call returned a partial progress stream while the original checkout remained active; early status probes also timed out during that checkout.", "Do not retry; audit the running process, exact path, worktree registration, branch, head, and eventual clean state until the original operation completes.", "After any worktree timeout, prove state read-only before deciding whether a mutation is still required."),
    negative(6, "semantic-novelty-preflight-four-title-collision", "The first 2,800-title novelty preflight rejected P24, P26, P27, and P28 because copied structural wording remained at or above the 0.60 token-set Jaccard threshold.", "Rewrite the four titles around their genuinely phase-specific mechanisms, then rerun only the isolated read-only novelty audit.", "Run title novelty before x1 materialization and retain every rejected title screen at zero credit."),
]


SAFE_TASKS = [
    {
        "task_id": f"V6586-SAFE-{index:03d}",
        "proposal_id": item["proposal_id"],
        "task": f"Materialize the bounded synthetic contract or explicit reservation for {item['slug']}.",
        "approval_class": item["approval_class"],
        "x1_execution": False,
        "planned_lane": "x2" if item["expected_disposition"] in {"completed", "represented"} else item["execution_lane"],
    }
    for index, item in enumerate(PROPOSALS, 1)
]


CANDIDATE_TASKS = [
    {
        "task_id": f"V6586-CAND-{index:03d}",
        "task": f"Prototype a reversible cross-surface refinement for {PROPOSALS[(index - 1) % len(PROPOSALS)]['slug']}.",
        "approval_class": "candidate_owner_local_review_required",
        "x1_execution": False,
        "planned_lane": "x2_if_bounded_evidence_permits",
    }
    for index in range(1, 21)
]


CLEAN_TASKS = [
    {
        "task_id": f"V6586-CLEAN-{index:03d}",
        "task": f"Run additive compatibility, privacy, provenance, stale-label, and nonpromotion cleanup for {item['slug']}.",
        "approval_class": "safe_now_additive_cleanup",
        "x1_execution": False,
        "planned_lane": "x2",
    }
    for index, item in enumerate(PROPOSALS, 1)
]
