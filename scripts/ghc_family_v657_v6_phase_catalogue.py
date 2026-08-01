#!/usr/bin/env python3
"""Frozen x1 catalogue for Orin Thale's v657-v6 phase."""

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
    source("OSHA-1910-218", "29 CFR 1910.218 Forging machines", "United States Occupational Safety and Health Administration", "https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.218", "current", "forge-machine, inspection-record, guard, control, and lockout vocabulary only; no workplace procedure, training, inspection, compliance, or safety determination"),
    source("OSHA-1910-147", "29 CFR 1910.147 Control of hazardous energy", "United States Occupational Safety and Health Administration", "https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.147", "current", "hazardous-energy and isolation vocabulary only; no workplace procedure, training, authorization, or compliance determination"),
    source("WORKSAFE-HOT-WORK", "Health and safety in welding", "WorkSafe New Zealand", "https://www.worksafe.govt.nz/topic-and-industry/welding/health-safety-in-welding/", "current", "hot-work, heat, fire, fume, and risk-assessment vocabulary only; no forge procedure, legal interpretation, training, or safety release"),
    source("NIST-ALLOY-DATA", "NIST Alloy Data", "National Institute of Standards and Technology", "https://www.nist.gov/mml/acmd/trc/nist-alloy-data", "current", "thermophysical-property, provenance, composition, phase, and uncertainty fields for a zero-row adapter only; no query, download, measurement, likelihood, or material inference"),
    source("NIST-SP800-61R3", "Incident Response Recommendations and Considerations for Cybersecurity Risk Management", "National Institute of Standards and Technology", "https://csrc.nist.gov/pubs/sp/800/61/r3/final", "current", "incident, retained-negative, recovery, communication, and handover vocabulary only"),
    source("BIPM-SI-BROCHURE", "The International System of Units (SI Brochure)", "Bureau International des Poids et Mesures", "https://www.bipm.org/en/publications/si-brochure", "stable", "units, dimensions, and quantity-expression obligations only; no measurement or empirical result"),
    source("NIST-SP811", "Guide for the Use of the International System of Units", "National Institute of Standards and Technology", "https://www.nist.gov/pml/special-publication-811", "stable", "unit-symbol and dimensional-consistency context only; no calibration or measurement authority"),
    source("W3C-PROV-O", "PROV-O: The PROV Ontology", "World Wide Web Consortium", "https://www.w3.org/TR/prov-o/", "stable", "entity, activity, attribution, derivation, revision, and invalidation lineage"),
    source("RFC-3339", "RFC 3339: Date and Time on the Internet", "RFC Editor", "https://www.rfc-editor.org/rfc/rfc3339.html", "stable", "synthetic timestamps, observation windows, expiry, correction, and handover"),
    source("RFC-8785", "RFC 8785: JSON Canonicalization Scheme", "RFC Editor", "https://www.rfc-editor.org/rfc/rfc8785.html", "stable", "deterministic synthetic contracts, digests, manifests, and receipts"),
    source("W3C-WCAG-22", "Web Content Accessibility Guidelines 2.2", "World Wide Web Consortium", "https://www.w3.org/TR/WCAG22/", "current", "structural accessibility vocabulary with manual and affected-user evaluation reserved"),
    source("NZ-PRIVACY-PRINCIPLES", "Privacy Act 2020 information privacy principles", "Office of the Privacy Commissioner New Zealand", "https://www.privacy.org.nz/privacy-principles/", "current", "purpose, collection, fairness, security, access, correction, retention, use, and disclosure reservations only"),
    source("TMR-PRINCIPLES", "Principles of Māori Data Sovereignty", "Te Mana Raraunga", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "current", "authority-reservation context only; Māori data governance remains with Māori authorities"),
    source("LOCAL-CONTEXTS-LABELS", "Traditional Knowledge and Biocultural Labels", "Local Contexts", "https://localcontexts.org/labels/about-the-labels/", "current", "community-defined provenance and protocol vocabulary with community authority reserved"),
    source("W3C-VC-DM-20", "Verifiable Credentials Data Model v2.0", "World Wide Web Consortium", "https://www.w3.org/TR/vc-data-model/", "current", "synthetic credential vocabulary only; no real issuer, holder, verifier, proof, status, or trust decision"),
    source("W3C-DID-10", "Decentralized Identifiers v1.0", "World Wide Web Consortium", "https://www.w3.org/TR/did-1.0/", "stable", "synthetic identifier-document vocabulary only; no live method, resolution, key, controller, or trust claim"),
    source("W3C-BITSTRING-STATUS-10", "Bitstring Status List v1.0", "World Wide Web Consortium", "https://www.w3.org/TR/vc-bitstring-status-list/", "current", "synthetic status and privacy-obligation vocabulary only; no live status service, revocation, key, or interoperability event"),
    source("W3C-ETHICAL-WEB", "Ethical Web Principles", "World Wide Web Consortium", "https://www.w3.org/TR/ethical-web-principles/", "current", "human control, privacy, accessibility, and non-harm vocabulary only; no ethical ratification or affected-party acceptance"),
    source("NZ-HSWA", "Health and Safety at Work Act 2015", "New Zealand Legislation", "https://www.legislation.govt.nz/act/public/2015/0070/latest/whole.html", "current", "legal-status and competent-role reservation only; no legal interpretation, compliance determination, or operational authorization"),
]


PROTECTED_GATES = [
    "real_workers_blacksmiths_forgers_welders_engineers_inspectors_clients_communities_and_affected_parties",
    "real_forges_furnaces_fuels_oxygen_gases_ventilation_flames_hot_metal_tools_machines_electrical_systems_and_stored_energy",
    "real_workpieces_alloys_heat_treatment_quenching_welding_grinding_lifting_inspection_release_or_use",
    "real_measurements_calibrations_material_properties_likelihoods_predictions_constraints_and_empirical_gmut_confirmation",
    "professional_blacksmithing_metallurgy_engineering_hot_work_workplace_safety_accessibility_privacy_or_environmental_authority",
    "sensitive_client_worker_location_design_heritage_traditional_knowledge_and_culturally_restricted_information",
    "production_identity_live_keys_signatures_proofs_issuance_resolution_status_revocation_interoperability_recovery_and_trust",
    "privacy_complete", "exhaustive_security", "complete_accessibility",
    "legal_cultural_land_heritage_environmental_data_governance_and_maori_authority",
    "affected_party_consent_notice_contestation_remedy_collective_governance_and_worker_acceptance",
    "independent_team_reproduction", "agi_or_asi", "consciousness_or_personhood",
    "theory_of_everything", "stage20",
]


def proposal(number: int, title: str, slug: str, pillar: str, mechanism: str, sources: list[str], expected_disposition: str) -> dict:
    approval = "safe_now_bounded_structural_formal_or_synthetic_software"
    lane = "x2_owner_local_bounded_synthetic"
    if expected_disposition == "open_gap":
        approval = "candidate_external_readiness_without_network_call"
        lane = "x2_owner_local_zero_row_readiness"
    elif expected_disposition == "exact_gate":
        approval = "exact_approval_authorized_affected_party_required"
        lane = "not_executed_authority_reservation"
    return {
        "proposal_id": f"V6576-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar_relation": pillar,
        "mechanism": mechanism,
        "hypothesis": f"A bounded {mechanism} contract can expose falsifiable synthetic obligations while refusing unsupported empirical, workplace, professional, safety, security, accessibility, privacy, identity, production, legal, cultural, Māori-authority, or Stage 20 promotion.",
        "null_or_failure_condition": f"The artifact omits a required {mechanism} obligation, accepts a frozen mutation, erases a failure, or crosses a protected worker, forge, hot-work, material, empirical, professional, production, legal, cultural, Māori-authority, identity, or Stage 20 gate.",
        "approval_class": approval,
        "execution_lane": lane,
        "official_or_primary_source_needs": sources,
        "concrete_artifacts": [f"surfaces/{slug}/contract.json", f"surfaces/{slug}/mutation-results.json", f"surfaces/{slug}/bounded-receipt.json"],
        "falsifier_or_acceptance_gate": "The valid synthetic fixture passes, five preregistered mutations are rejected, and the receipt grants no real person, forge, workpiece, heat, fuel, oxygen, tool, machine, inspection, safety release, measurement, professional, production, legal, cultural, Māori-authority, identity, accessibility-complete, privacy-complete, security-complete, independent-reproduction, Theory-of-Everything, or Stage 20 credit.",
        "rollback_or_recovery": "Stop, retain the failed witness at zero credit, rewrite no history, and leave real people, forges, materials, heat, fuel, oxygen, tools, machines, accounts, records, sibling lanes, and authority state unchanged.",
        "protected_gates": PROTECTED_GATES,
        "expected_disposition": expected_disposition,
    }


PROPOSAL_SPECS = [
    ("Forge job-intake and workpiece custody passport with synthetic token, requested transformation, presented-owner placeholder, condition note, correction path, and no-work-start lock", "forge-intake-provenance", "Freed ID and CBR Heart", "forge job intake, workpiece custody, synthetic ownership placeholder, correction, and work-start refusal", ["W3C-PROV-O", "NZ-PRIVACY-PRINCIPLES", "RFC-3339"]),
    ("Forge metal-stock heat-number, section, supplier claim, composition placeholder, substitution quarantine, provenance, and no-alloy-authentication ledger", "forge-stock-provenance", "GMUT Mind and Freed ID", "metal-stock provenance, composition placeholder, substitution quarantine, and alloy-authentication refusal", ["NIST-ALLOY-DATA", "W3C-PROV-O", "RFC-8785"]),
    ("Forge temperature-observation envelope with sensor placeholder, scale, unit, uncertainty, clock basis, correction lineage, and no-material-state inference", "forge-temperature-observation", "GMUT Mind", "temperature observation, units, uncertainty, clock basis, correction, and material-state inference refusal", ["BIPM-SI-BROCHURE", "NIST-SP811", "RFC-3339"]),
    ("Forge fuel, oxygen, airflow, burner, valve, and exhaust topology graph with synthetic assets, isolation boundaries, state quarantine, and no-operation rule", "forge-fuel-airflow-topology", "THOS Body and GMUT Mind", "fuel, oxygen, airflow, burner, valve, exhaust topology, isolation, and operation refusal", ["WORKSAFE-HOT-WORK", "OSHA-1910-147", "W3C-PROV-O"]),
    ("Forge hammer, tongs, anvil, die, punch, and drift custody and condition ledger with synthetic identifiers, inspection placeholder, quarantine, and no-use release", "forge-tool-custody", "THOS Body and Freed ID", "forge-tool custody, condition, inspection placeholder, quarantine, and use-release refusal", ["OSHA-1910-218", "W3C-PROV-O", "RFC-3339"]),
    ("Hot-work zone clearance, ignition-source, combustible placeholder, observer role, stop-work, escalation, and competent-authority reservation board", "forge-hot-work-boundary", "THOS Body and CBR Heart", "hot-work zone, ignition, combustible placeholder, stop-work, escalation, and authority reservation", ["WORKSAFE-HOT-WORK", "NZ-HSWA", "W3C-PROV-O"]),
    ("Quench-medium batch, temperature placeholder, contamination cue, material compatibility, fire and environmental hold, correction, and no-quench instruction ledger", "forge-quench-medium", "THOS Body and CBR Heart", "quench-medium provenance, compatibility, fire and environmental hold, correction, and quench refusal", ["WORKSAFE-HOT-WORK", "W3C-PROV-O", "BIPM-SI-BROCHURE"]),
    ("Forge heat-treatment ramp, soak, cool, atmosphere, revision, deviation, replay, uncertainty, and no-property-certification schedule graph", "forge-heat-treatment-schedule", "GMUT Mind and THOS Body", "heat-treatment schedule, revision, deviation, replay, uncertainty, and property-certification refusal", ["NIST-ALLOY-DATA", "BIPM-SI-BROCHURE", "W3C-PROV-O"]),
    ("GMUT typed thermal-expansion, phase-transformation, temperature-domain, unit, reference-state, latent-heat, and observation-firewall obligation board", "gmut-forge-phase-thermal", "GMUT Mind", "typed thermal-expansion, phase-transition, reference-state, latent-heat, unit, and observation-firewall obligations", ["NIST-ALLOY-DATA", "BIPM-SI-BROCHURE", "NIST-SP811"]),
    ("GMUT radiative, convective, and conductive forge heat-transfer boundary, emissivity, view-factor, flux, unit, and no-prediction obligation board", "gmut-forge-heat-transfer", "GMUT Mind", "radiative, convective, conductive heat-transfer, emissivity, view-factor, flux, unit, and prediction refusal", ["BIPM-SI-BROCHURE", "NIST-SP811", "RFC-8785"]),
    ("GMUT nonlinear forging constitutive stress, strain, yield, hardening, rate, temperature, frame, unit, identifiability, and no-material-law obligation board", "gmut-forge-constitutive", "GMUT Mind", "nonlinear constitutive stress, strain, hardening, rate, temperature, frame, unit, identifiability, and material-law refusal", ["NIST-ALLOY-DATA", "BIPM-SI-BROCHURE", "NIST-SP811"]),
    ("Forge crack, fold, lap, inclusion, surface cue, examination-method placeholder, uncertainty, disposition hold, and nondestructive-test authority reservation board", "forge-defect-observation", "GMUT Mind and CBR Heart", "defect-cue observation, examination placeholder, uncertainty, hold, and test-authority reservation", ["OSHA-1910-218", "W3C-PROV-O", "RFC-3339"]),
    ("Forge dimension, tolerance, datum, instrument placeholder, calibration epoch, covariance, correction, and no-conformance measurement trace", "forge-dimensional-trace", "GMUT Mind", "dimension, tolerance, datum, instrument placeholder, calibration epoch, covariance, correction, and conformance refusal", ["BIPM-SI-BROCHURE", "NIST-SP811", "W3C-PROV-O"]),
    ("Forge scale, oxide, decarburization, colour, texture, observation vocabulary, lighting condition, ambiguity, and no-metallurgical-inference classifier", "forge-surface-observation", "GMUT Mind", "surface observation, lighting, ambiguity, and metallurgical-inference refusal", ["NIST-ALLOY-DATA", "W3C-PROV-O", "RFC-3339"]),
    ("Forge workpiece split, merge, weld placeholder, repair, trimming loss, mass-balance, lineage, duplicate-credit, and provenance genealogy graph", "forge-workpiece-genealogy", "Freed ID and GMUT Mind", "workpiece split, merge, repair placeholder, mass balance, lineage, duplicate-credit, and provenance genealogy", ["W3C-PROV-O", "BIPM-SI-BROCHURE", "RFC-8785"]),
    ("Forge die and tooling revision, fit, alignment, clearance, interference signal, change authority, rollback, and no-machine-release board", "forge-tooling-change", "THOS Body and Freed ID", "die and tooling revision, fit, clearance, change authority, rollback, and machine-release refusal", ["OSHA-1910-218", "W3C-PROV-O", "NIST-SP800-61R3"]),
    ("Power-hammer, press, grinder, and forge energy-source isolation, residual-energy, lock placeholder, verification hold, and no-maintenance-release board", "forge-energy-isolation", "THOS Body and CBR Heart", "forge-machine energy isolation, residual energy, lock placeholder, verification hold, and maintenance-release refusal", ["OSHA-1910-147", "OSHA-1910-218", "W3C-PROV-O"]),
    ("Forge gas, electrical, ventilation, detector, alarm, emergency-stop, acknowledgement, fault, escalation, and no-safety-determination state contract", "forge-alarm-state", "THOS Body", "gas, electrical, ventilation, detector, alarm, emergency-stop, fault, escalation, and safety-determination refusal", ["WORKSAFE-HOT-WORK", "NIST-SP800-61R3", "RFC-3339"]),
    ("Forge lifting, manual handling, heat exposure, workload, fatigue signal, stop-work, unfinished-work, correction-readback, and handover board", "forge-workload-stop", "THOS Body and CBR Heart", "lifting, heat exposure, workload, fatigue cue, stop-work, correction readback, and handover", ["NZ-HSWA", "WORKSAFE-HOT-WORK", "RFC-3339"]),
    ("Forge shift-handover packet with hot-stock placeholder, unresolved anomaly, cooling boundary, isolation state, evidence link, readback, and next-owner assignment", "forge-shift-handover", "THOS Body and Freed ID", "forge shift handover, hot-stock placeholder, anomaly, cooling, isolation, evidence, readback, and next-owner assignment", ["NIST-SP800-61R3", "W3C-PROV-O", "RFC-3339"]),
    ("Accessible public forge-demonstration notice with hot-zone text alternative, noncolour warning, captions, focus order, keyboard path, print mode, and human-review reservation", "forge-accessible-notice", "CBR Heart and THOS Body", "accessible forge notice, noncolour warning, captions, focus, keyboard, print, and human-review reservation", ["W3C-WCAG-22", "W3C-ETHICAL-WEB", "W3C-PROV-O"]),
    ("Forge client, craftsperson, material-origin, commission, location, image, retention, purpose, disclosure, correction, and privacy-minimization ledger", "forge-privacy-minimization", "Freed ID and CBR Heart", "forge-record purpose, minimization, retention, disclosure, access, correction, and privacy reservation", ["NZ-PRIVACY-PRINCIPLES", "W3C-PROV-O", "RFC-8785"]),
    ("Forge documentation threat model with tamper cue, stale state, replay, privilege boundary, rollback, evidence retention, and no-production-security claim", "forge-threat-recovery", "Freed ID, THOS Body, and CBR Heart", "forge-document tamper, stale state, replay, privilege boundary, rollback, retention, and exhaustive-security refusal", ["NIST-SP800-61R3", "RFC-8785", "NZ-PRIVACY-PRINCIPLES"]),
    ("THOS forge task-sequencing, hot-work hold, matched action budget, correction, workload, harm stop, blinded comparison, and operator-study proxy", "thos-forge-task-sequencing", "THOS Body", "forge task sequencing, matched action budget, correction, workload, harm stop, blinded comparison, and operator-study refusal", ["WORKSAFE-HOT-WORK", "NZ-HSWA", "RFC-3339"]),
    ("THOS forge correction-latency, fatigue, heat-load placeholder, anomaly escalation, skill-decay, crossover, safety-monitoring, and no-effectiveness protocol", "thos-forge-human-factors", "THOS Body", "forge correction latency, fatigue, heat-load placeholder, escalation, skill decay, crossover, monitoring, and effectiveness refusal", ["NZ-HSWA", "NIST-SP800-61R3", "RFC-3339"]),
    ("Freed ID synthetic forge workpiece and tool provenance credential with holder minimization, issuer placeholder, digest binding, purpose, disclosure, and nonproduction profile", "freed-id-forge-provenance", "Freed ID and CBR Heart", "synthetic forge provenance credential, minimization, issuer placeholder, digest, purpose, disclosure, and nonproduction boundary", ["W3C-VC-DM-20", "W3C-DID-10", "NZ-PRIVACY-PRINCIPLES"]),
    ("Freed ID synthetic forge equipment status, suspension, revocation placeholder, cache age, recovery, key-rotation reservation, and no-live-resolution profile", "freed-id-forge-status", "Freed ID", "synthetic forge-equipment status, suspension, revocation placeholder, cache, recovery, rotation reservation, and live-resolution refusal", ["W3C-BITSTRING-STATUS-10", "W3C-DID-10", "W3C-VC-DM-20"]),
    ("Thermo-Psyche forge heat, work, entropy-production, dissipation, domain, unit, analogy label, and agency-nonconversion bridge protocol", "thermo-psyche-forge-nonconversion", "GMUT Mind and CBR Heart", "heat, work, entropy production, dissipation, domain, unit, analogy label, and agency nonconversion", ["BIPM-SI-BROCHURE", "NIST-SP811", "W3C-ETHICAL-WEB"]),
    ("NIST metallurgy and thermophysical-property record, alloy identifier, temperature, phase, uncertainty, provenance, covariance, and zero-row likelihood-refusal adapter", "nist-metallurgy-zero-row-adapter", "GMUT Mind", "NIST alloy-data schema, provenance, uncertainty, covariance, zero-row readiness, and likelihood refusal", ["NIST-ALLOY-DATA", "BIPM-SI-BROCHURE", "W3C-PROV-O"]),
    ("CBR forge worker safety, craft heritage, design knowledge, client privacy, environmental exposure, land and place, remedy, legal, cultural, data-governance, affected-party, and Māori-authority covenant", "cbr-forge-authority-covenant", "CBR Heart", "forge safety, craft heritage, design knowledge, privacy, environment, land, remedy, law, culture, governance, affected-party, and Māori-authority nonautomation", ["NZ-HSWA", "TMR-PRINCIPLES", "LOCAL-CONTEXTS-LABELS", "NZ-PRIVACY-PRINCIPLES"]),
]


PROPOSALS = [
    proposal(number, title, slug, pillar, mechanism, sources, "completed" if number <= 23 else "represented" if number <= 28 else "open_gap" if number == 29 else "exact_gate")
    for number, (title, slug, pillar, mechanism, sources) in enumerate(PROPOSAL_SPECS, 1)
]


SKILL_SPECS = [
    ("ghc-family-forge-intake-provenance", "Freeze synthetic forge job, workpiece, stock, custody, correction, and no-work-start boundaries."),
    ("ghc-family-forge-thermal-observation", "Constrain temperature, units, uncertainty, reference state, schedule, and material-inference refusal."),
    ("ghc-family-forge-hot-work-boundary", "Fail closed around hot work, fuel, oxygen, ignition, combustibles, fire, fume, and authority."),
    ("ghc-family-forge-tool-machine-custody", "Model synthetic tool, die, hammer, press, grinder, condition, change, isolation, and release states."),
    ("ghc-family-forge-material-observation", "Separate bounded surface, dimensional, defect, and provenance observations from material certification."),
    ("ghc-family-forge-shift-handover", "Constrain anomaly, cooling, isolation, workload, stop-work, readback, and next-owner handover."),
    ("ghc-family-forge-accessibility-privacy", "Structure accessible notices and minimized records while reserving manual and affected-user review."),
    ("ghc-family-forge-gmut-firewall", "Keep thermal, transfer, constitutive, and zero-row adapter evidence inside typed research bounds."),
    ("ghc-family-forge-freed-id-status", "Constrain synthetic provenance and status profiles without live keys, proofs, resolution, or trust."),
    ("ghc-family-forge-authority-reservation", "Fail closed around safety, profession, heritage, land, remedy, law, culture, governance, and Māori authority."),
]


RUNNER_SPECS = [
    ("ghc_family_forge_intake_provenance.py", "forge-intake-provenance"),
    ("ghc_family_forge_thermal_observation.py", "forge-temperature-observation"),
    ("ghc_family_forge_hot_work_boundary.py", "forge-hot-work-boundary"),
    ("ghc_family_forge_tool_machine_custody.py", "forge-tool-custody"),
    ("ghc_family_forge_material_observation.py", "forge-defect-observation"),
    ("ghc_family_forge_shift_handover.py", "forge-shift-handover"),
    ("ghc_family_forge_accessibility_privacy.py", "forge-accessible-notice"),
    ("ghc_family_forge_gmut_firewall.py", "gmut-forge-phase-thermal"),
    ("ghc_family_forge_freed_id_status.py", "freed-id-forge-provenance"),
    ("ghc_family_forge_authority_reservation.py", "cbr-forge-authority-covenant"),
]


def negative(number: int, slug: str, failure: str, recovery: str, guard: str) -> dict:
    return {
        "negative_id": f"V6576-X1-N{number:02d}", "scope": "startup_and_x1",
        "signature": slug, "observed": failure, "credit": 0, "retained": True,
        "recovery": recovery, "recurrence_guard": guard, "same_owner_only": True,
        "independent_reproduction": False,
    }


X1_OPERATIONAL_NEGATIVES = [
    negative(1, "powershell-foreach-direct-pipeline-parser-error", "A read-only source-state probe used a direct foreach-to-pipeline form that PowerShell rejected before execution.", "Materialize the bounded array before piping it to JSON.", "Materialize PowerShell iteration output before downstream pipelines."),
    negative(2, "measure-object-nonempty-line-count-assumption", "A baton read used Measure-Object -Line and mistook 408 nonempty lines for the 865-line physical file.", "Use the exact UTF-8 line array Count and read through EOF.", "Distinguish physical line count from nonempty-line metrics."),
    negative(3, "broad-required-skill-read-output-truncation", "A combined required-skill read exceeded the useful output budget and hid later references.", "Read each exact skill and required reference separately through EOF.", "Bound skill reads by file and verify every exact companion."),
    negative(4, "guessed-auth-schema-extension-missing", "A read-only lookup guessed a JSON auth schema although the installed companion is Markdown.", "Enumerate the exact reference directory and read auth-permission-state-schema.md.", "Resolve installed reference names before reading."),
    negative(5, "guessed-roster-schema-name-missing", "A read-only lookup guessed roster-schema.md rather than roster-state-schema.md.", "Enumerate and read the exact roster-state-schema.md companion.", "Resolve schema filenames from the skill directory."),
    negative(6, "guessed-method-flow-schema-name-missing", "A read-only lookup guessed method-flow-state-schema.md rather than schema.md.", "Read the exact schema.md named by the skill.", "Follow the complete skill's exact reference name."),
    negative(7, "guessed-meta-tool-schema-name-missing", "A read-only lookup guessed tool-selection-schema.md rather than catalogue-schema.md.", "Read the exact catalogue-schema.md companion.", "Enumerate referenced schema files before access."),
    negative(8, "powershell-all-title-similarity-audit-timeout", "A PowerShell all-title novelty implementation exceeded its wrapper and left no attributable complete audit.", "Terminate only the owned probe and run an in-memory Python token audit.", "Use linear in-memory Python for thousands of title comparisons."),
    negative(9, "cp1252-novelty-diagnostic-output-fault", "The first Python novelty diagnostic computed results but failed while emitting Māori text through CP1252.", "Emit ASCII-safe JSON or pin UTF-8 before Unicode diagnostics.", "Pin UTF-8 before emitting proposal or Māori text."),
    negative(10, "temporary-file-git-blob-hash-command-rejected", "A proposed temporary-file Git-blob hash command was rejected before state change.", "Hash immutable Git stdout and the checkout directly without a temporary file.", "Prefer direct immutable blob bytes for read-only hash evidence."),
    negative(11, "windows-literal-wildcard-rg-path-assumption", "A read-only ripgrep call passed a literal wildcard path that Windows did not expand.", "Search the exact directory root with a -g filename filter.", "Use ripgrep globs through -g on Windows."),
    negative(12, "combined-post-checkout-audit-timeout", "A combined post-checkout audit exceeded its wrapper and left a long status process without attributable complete output.", "Terminate only the owned process and split head, branch, tracked, index, and untracked probes.", "Split large-worktree Git state checks into scalar calls."),
    negative(13, "broad-official-source-search-output-truncation", "A four-query long official-source search exceeded the useful output window and provided no complete attributable source set.", "Repeat two official-domain queries at a time with short output and retain only successfully resolved primary pages.", "Bound web-source discovery by query count and response length."),
    negative(14, "mixed-unicode-multihunk-patch-context-mismatch", "A semantic cleanup patch combined ASCII changes with a Unicode-rendered heading context and was rejected without changing the file.", "Apply ASCII-stable hunks separately and overwrite the generated heading through a bounded current block.", "Do not combine independent ASCII edits with Unicode-sensitive patch anchors."),
    negative(15, "large-worktree-porcelain-commit-completion-unattributed", "The ordinary porcelain commit wrapper returned without attributable output and an immediate head read still showed the source; a later durable-state audit found the exact single-parent x1 commit had completed.", "Keep the durable commit, rewrite no history, verify its parent and tree, and use one narrow x1-only repair commit for later lifecycle evidence.", "After an unattributed mutating wrapper, audit branch HEAD, parent, tree, index, worktree, and processes before any retry or alternate commit path."),
    negative(16, "post-x1-builder-head-guard-refusal", "A warm x1 builder rerun encountered the newly durable x1 commit and correctly refused because its original guard allowed only the exact source head.", "Extend the guard only for a single source-descendant x1-only repair commit, keep source receipts anchored to the immutable Caelen final, and reject any x2 or broader history.", "Lifecycle-aware builders must distinguish immutable source identity from the current bounded x1 repair head."),
]


SAFE_TASKS = [{"task_id": f"V6576-SAFE-{index:03d}", "proposal_id": item["proposal_id"], "task": f"Build and validate the bounded synthetic contract for {item['slug']}.", "approval_class": "safe_now_owner_local_additive", "x1_execution": False, "planned_lane": "x2"} for index, item in enumerate(PROPOSALS, 1)]
CANDIDATE_TASKS = [{"task_id": f"V6576-CAND-{index:03d}", "task": f"Prototype a reversible cross-surface refinement for {PROPOSALS[(index - 1) % len(PROPOSALS)]['slug']}.", "approval_class": "candidate_owner_local_review_required", "x1_execution": False, "planned_lane": "x2_if_bounded_evidence_permits"} for index in range(1, 21)]
CLEAN_TASKS = [{"task_id": f"V6576-CLEAN-{index:03d}", "task": f"Run additive compatibility, privacy, provenance, stale-label, and nonpromotion cleanup for {item['slug']}.", "approval_class": "safe_now_additive_cleanup", "x1_execution": False, "planned_lane": "x2"} for index, item in enumerate(PROPOSALS, 1)]
