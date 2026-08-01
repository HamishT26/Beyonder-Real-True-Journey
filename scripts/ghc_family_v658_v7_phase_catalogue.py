#!/usr/bin/env python3
"""Frozen x1 catalogue for Vesper Arlen's solo v658-v7 phase."""

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
    source("NZCAA-P43-B", "Part 43 Subpart B - Maintenance", "Civil Aviation Authority of New Zealand", "https://www.aviation.govt.nz/rules/rule-part/part-43/subpart-b/", "current", "maintenance-person, performance, test, non-destructive-testing, and record vocabulary only; no qualification or maintenance authority"),
    source("NZCAA-P43-C", "Part 43 Subpart C - Release to Service", "Civil Aviation Authority of New Zealand", "https://www.aviation.govt.nz/rules/rule-part/part-43/subpart-c/", "current", "release, inoperative-equipment, defect, duplicate-inspection, and performance-check vocabulary only; no certification or release authority"),
    source("NZCAA-AC43-1", "AC43-1 - Aircraft maintenance", "Civil Aviation Authority of New Zealand", "https://www.aviation.govt.nz/rules/advisory-circulars/show/AC43-1/", "current_watch", "maintenance-data, records, tools, facilities, parts, and practice vocabulary only; no compliance or professional claim"),
    source("NZCAA-AC43-3", "AC43-3 - Parts Documentation - CAA Form Two", "Civil Aviation Authority of New Zealand", "https://www.aviation.govt.nz/rules/advisory-circulars/show/AC43-3/", "current", "parts-documentation and traceability vocabulary only; no form issue, acceptance, installation, or release claim"),
    source("FAA-14CFR43", "14 CFR Part 43 - Maintenance, Preventive Maintenance, Rebuilding, and Alteration", "Electronic Code of Federal Regulations", "https://www.ecfr.gov/current/title-14/chapter-I/subchapter-C/part-43", "current_watch", "maintenance, performance, record, inspection, and approval vocabulary only; no United States compliance claim"),
    source("FAA-AC20-109B", "AC 20-109B - Service Difficulty Reporting System", "Federal Aviation Administration", "https://www.faa.gov/regulations_policies/advisory_circulars/index.cfm/go/document.information/documentID/1042240", "active", "malfunction, failure, defect, report, supplement, and reporting-boundary vocabulary only; no filing or regulatory claim"),
    source("FAA-SDR-DOWNLOAD", "Download Service Difficulty Reports by Year", "Federal Aviation Administration", "https://www.faa.gov/av-info/download_SDR", "current_watch", "external dataset capability and schema-watch vocabulary only; no download, row, analysis, or safety conclusion"),
    source("FAA-AC25-571", "AC 25.571-1D - Damage Tolerance and Fatigue Evaluation of Structure", "Federal Aviation Administration", "https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_25_571-1D.pdf", "published", "fatigue, damage, inspection, and uncertainty vocabulary only; no design, substantiation, airworthiness, or compliance claim"),
    source("EASA-CAW", "Easy Access Rules for Continuing Airworthiness", "European Union Aviation Safety Agency", "https://www.easa.europa.eu/en/document-library/easy-access-rules/easy-access-rules-continuing-airworthiness", "revision_2025_09_watch", "continuing-airworthiness, Part-M, Part-145, record, component, worksheet, and traceability vocabulary only; no European compliance claim"),
    source("W3C-PROV", "PROV-O: The PROV Ontology", "World Wide Web Consortium", "https://www.w3.org/TR/prov-o/", "stable", "entity, activity, derivation, revision, invalidation, and attribution lineage"),
    source("W3C-WCAG-22", "Web Content Accessibility Guidelines 2.2", "World Wide Web Consortium", "https://www.w3.org/TR/WCAG22/", "current", "machine-checkable document structure and notice vocabulary; manual and affected-user evaluation remain reserved"),
    source("W3C-VC-DM-20", "Verifiable Credentials Data Model v2.0", "World Wide Web Consortium", "https://www.w3.org/TR/vc-data-model-2.0/", "current", "synthetic nonproduction artifact-envelope vocabulary only; no live identity, proof, or trust"),
    source("W3C-DATA-INTEGRITY", "Verifiable Credential Data Integrity 1.0", "World Wide Web Consortium", "https://www.w3.org/TR/vc-data-integrity/", "current", "proof-configuration vocabulary only; no key, signature, verification, security, or interoperability claim"),
    source("RFC-8785", "JSON Canonicalization Scheme", "RFC Editor", "https://www.rfc-editor.org/rfc/rfc8785.html", "stable", "deterministic JSON representation vocabulary only; no cryptographic assurance"),
    source("NZ-PRIVACY-PRINCIPLES", "Privacy principles", "Office of the Privacy Commissioner New Zealand", "https://www.privacy.org.nz/privacy-principles/", "current", "purpose, minimisation, correction, retention, use, and disclosure reservations only; no legal advice"),
    source("TE-MANA-RARAUNGA", "Principles of Māori Data Sovereignty", "Te Mana Raraunga", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "current", "Māori data rights, interests, governance, collective benefit, and authority reservation only"),
    source("LOCAL-CONTEXTS-TK", "Traditional Knowledge Labels", "Local Contexts", "https://localcontexts.org/labels/traditional-knowledge-labels/", "current_watch", "community-defined notice and authority-reservation context only; no label selection or application"),
]


PROTECTED_GATES = [
    "real_people_maintainers_engineers_inspectors_operators_organisations_passengers_communities_and_affected_parties",
    "real_aircraft_registrations_flights_components_parts_tools_defects_measurements_tasks_inspections_and_records",
    "real_maintenance_repair_installation_inspection_certification_release_to_service_dispatch_airworthiness_or_flight_safety_decision",
    "professional_maintenance_engineering_ndt_metrology_airworthiness_safety_privacy_security_or_accessibility_authority",
    "empirical_gmut_prediction_constraint_force_flow_fatigue_life_or_confirmation",
    "blind_matched_budget_thos_real_arms_and_independent_review",
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
        expected, approval, lane = "completed", "safe_now_bounded_structural_formal_or_synthetic_software", "x2_owner_local_bounded_synthetic"
    elif number <= 28:
        expected, approval, lane = "represented", "candidate_proxy_protocol_or_nonproduction_schema", "x2_owner_local_representation_only"
    elif number == 29:
        expected, approval, lane = "open_gap", "candidate_external_data_readiness_without_transport_or_real_rows", "x2_owner_local_zero_row_readiness"
    else:
        expected, approval, lane = "exact_gate", "outside_hamish_authority_affected_party_legal_cultural_and_maori_authority_required", "not_executed_authority_reservation"
    return {
        "proposal_id": f"V6587-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar_relation": pillar,
        "mechanism": mechanism,
        "hypothesis": f"A bounded {mechanism} contract can expose falsifiable synthetic obligations while refusing unsupported empirical, professional, production, legal, cultural, Māori-authority, identity, privacy-complete, accessibility-complete, Theory-of-Everything, or Stage 20 promotion.",
        "null_or_failure_condition": f"The artifact omits a required {mechanism} obligation, accepts a frozen mutation, erases a failure, or crosses a protected aircraft, person, maintenance, professional, production, rights, legal, cultural, Māori-authority, identity, or Stage 20 gate.",
        "approval_class": approval,
        "execution_lane": lane,
        "official_or_primary_source_needs": sources,
        "concrete_artifacts": [f"surfaces/{slug}/contract.json", f"surfaces/{slug}/mutation-results.json", f"surfaces/{slug}/bounded-receipt.json"],
        "falsifier_or_acceptance_gate": "The valid synthetic fixture passes, five preregistered mutations are rejected, and the receipt grants no real-aircraft, real-maintenance, empirical, airworthiness, release, participant, professional, production, legal, cultural, Māori-authority, identity, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, Theory-of-Everything, or Stage 20 credit.",
        "rollback_or_recovery": "Stop, retain the failed witness at zero credit, rewrite no history, and leave people, aircraft, organisations, parts, maintenance state, sibling lanes, external systems, rights, and authority state unchanged.",
        "protected_gates": PROTECTED_GATES,
        "expected_disposition": expected,
    }


PROPOSAL_SPECS = [
    ("Fictional maintenance-organisation scope card with aircraft-use refusal and zero operational records", "aircraft-maintenance-scope-card", "All pillars", "fictional maintenance scope, synthetic organisation alias, zero-record state, bounded purpose, and operational-use refusal", ["NZCAA-P43-B", "EASA-CAW", "W3C-PROV"]),
    ("Synthetic aircraft configuration passport with effectivity epochs and registry-resolution refusal", "aircraft-configuration-passport", "THOS Body and Freed ID", "fictional aircraft alias, type and configuration placeholder, effectivity epoch, amendment lineage, and registry-resolution refusal", ["NZCAA-AC43-1", "EASA-CAW", "W3C-PROV"]),
    ("Applicability and effectivity baseline matrix for fictional maintenance instructions", "maintenance-effectivity-baseline", "THOS Body", "maintenance-data applicability, effectivity, configuration dependency, conflict hold, revision lineage, and use refusal", ["NZCAA-AC43-1", "EASA-CAW", "W3C-PROV"]),
    ("Controlled maintenance-data revision pin with supersession and authorization holds", "maintenance-data-revision-pin", "THOS Body and CBR Heart", "controlled maintenance-data identity, revision, supersession, amendment, authorization hold, and instruction-use refusal", ["NZCAA-P43-B", "EASA-CAW", "W3C-PROV"]),
    ("Synthetic work-order and task-card state machine with prerequisite and certification abstention", "maintenance-task-card-lifecycle", "THOS Body", "work order, task card, prerequisite, step transition, interruption, placeholder signoff, and certification refusal", ["NZCAA-P43-B", "EASA-CAW", "W3C-PROV"]),
    ("Access-panel and zone closure docket with foreign-object reconciliation", "maintenance-access-closure-docket", "THOS Body", "access, panel, zone, opening, closure, foreign-object check, reconciliation, and completion refusal", ["NZCAA-AC43-1", "EASA-CAW", "W3C-PROV"]),
    ("Tool and test-equipment calibration ledger with expiry and quarantine transitions", "maintenance-tool-calibration-ledger", "THOS Body", "tool identity, calibration status, expiry, traceability placeholder, quarantine, and measurement-use refusal", ["NZCAA-P43-B", "NZCAA-AC43-1", "W3C-PROV"]),
    ("Part and material eligibility envelope with batch lineage and installation abstention", "maintenance-part-eligibility-envelope", "THOS Body and Freed ID", "part and material identity, batch, documentation, shelf state, eligibility placeholder, quarantine, and installation refusal", ["NZCAA-AC43-3", "EASA-CAW", "W3C-PROV"]),
    ("Life-limited component counter with uncertainty and mandatory limit hold", "maintenance-life-limit-counter", "THOS Body and GMUT Mind", "component counter, interval, uncertainty, limit state, discrepancy hold, and airworthiness refusal", ["EASA-CAW", "FAA-AC25-571", "W3C-PROV"]),
    ("Serialized component removal-installation chain with custody and configuration holds", "maintenance-component-chain", "THOS Body and Freed ID", "serialized component lineage, removal, installation placeholder, custody, configuration hold, and real-component refusal", ["NZCAA-AC43-3", "EASA-CAW", "W3C-PROV"]),
    ("Non-routine finding docket with engineering-disposition and repair-authority refusal", "maintenance-nonroutine-finding", "THOS Body and CBR Heart", "non-routine finding, evidence placeholder, classification, disposition request, hold, amendment, and engineering-authority refusal", ["NZCAA-P43-C", "EASA-CAW", "W3C-PROV"]),
    ("NDT procedure and qualification placeholder with result and competence abstention", "maintenance-ndt-boundary", "THOS Body", "NDT method, procedure revision, equipment state, qualification placeholder, indication placeholder, and inspection-result refusal", ["NZCAA-P43-B", "EASA-CAW", "W3C-PROV"]),
    ("Critical torque and locking record with independent-witness eligibility boundary", "maintenance-critical-task-witness", "THOS Body", "critical task, torque placeholder, locking method, witness eligibility, duplicate check, and certification refusal", ["NZCAA-P43-C", "EASA-CAW", "W3C-PROV"]),
    ("Fluid and chemical material-control card with shelf life and compatibility hold", "maintenance-material-control", "THOS Body", "fluid and chemical identity, batch, shelf life, storage, compatibility placeholder, quarantine, and application refusal", ["NZCAA-AC43-1", "EASA-CAW", "W3C-PROV"]),
    ("Tool and foreign-object accountability reconciliation for synthetic shift boundaries", "maintenance-tool-fod-reconciliation", "THOS Body and CBR Heart", "tool issue and return, foreign-object state, unresolved item, reconciliation, escalation hold, and aircraft-use refusal", ["NZCAA-AC43-1", "EASA-CAW", "W3C-PROV"]),
    ("Maintenance-environment suitability register with access, lighting and temperature holds", "maintenance-environment-register", "THOS Body", "environment, access, lighting, temperature, contamination state, suitability hold, and task-performance refusal", ["NZCAA-P43-B", "NZCAA-AC43-1", "W3C-PROV"]),
    ("Independent and duplicate inspection eligibility board without certification authority", "maintenance-independent-inspection", "THOS Body and CBR Heart", "independent inspection, duplicate inspection, eligibility placeholder, separation, conflict hold, and certification refusal", ["NZCAA-P43-C", "EASA-CAW", "W3C-PROV"]),
    ("Functional-check boundary with expected-state comparison and return-to-service abstention", "maintenance-functional-check", "THOS Body", "functional check, expected state, observed placeholder, discrepancy, abort, restoration, and return-to-service refusal", ["NZCAA-P43-C", "EASA-CAW", "W3C-PROV"]),
    ("Loadable aircraft-part revision and checksum docket with upload prohibition", "maintenance-software-load-docket", "THOS Body and Freed ID", "software and loadable-part identity, revision, checksum, compatibility placeholder, rollback, and upload refusal", ["EASA-CAW", "RFC-8785", "W3C-PROV"]),
    ("Deferred-item rectification clock with status linkage and dispatch abstention", "maintenance-deferred-item-clock", "THOS Body and CBR Heart", "deferred item, interval placeholder, status link, rectification hold, escalation, and MEL or dispatch refusal", ["NZCAA-P43-C", "EASA-CAW", "W3C-PROV"]),
    ("Maintenance-record correction and amendment trail with original-value preservation", "maintenance-record-amendment", "THOS Body and Freed ID", "record correction, original preservation, reason, attribution placeholder, chronology, and silent-rewrite refusal", ["NZCAA-P43-B", "EASA-CAW", "W3C-PROV"]),
    ("Fatigue, workload, interruption and shift-handover register for synthetic maintenance work", "maintenance-human-factors-handover", "THOS Body and CBR Heart", "workload, fatigue declaration placeholder, interruption, task status, unresolved risk, readback, and operational-handover refusal", ["EASA-CAW", "NZ-PRIVACY-PRINCIPLES", "W3C-PROV"]),
    ("GMUT typed fatigue-crack and damage operator with unit, domain and airworthiness firewalls", "gmut-fatigue-damage-operator", "GMUT Mind", "typed fatigue and crack-growth state, load placeholder, damage operator, unit and domain check, identifiability, falsifier, and airworthiness refusal", ["FAA-AC25-571", "W3C-PROV", "RFC-8785"]),
    ("THOS deterministic maintenance job-batch receipt with checkpoints and orphan isolation", "thos-maintenance-checkpoint", "THOS Body", "deterministic maintenance job batch, partition digest, checkpoint, bounded retry, orphan quarantine, and throughput-claim refusal", ["W3C-PROV", "RFC-8785", "EASA-CAW"]),
    ("THOS synthetic maintenance-shift handover proxy with unresolved-card digest", "thos-maintenance-handover", "THOS Body and CBR Heart", "synthetic maintenance-shift handover, unresolved card digest, status conflict, acknowledgement placeholder, and operational-handover refusal", ["EASA-CAW", "NZCAA-AC43-1", "W3C-PROV"]),
    ("Nonproduction Freed ID maintenance-record lineage capsule with correction window", "freed-id-maintenance-record", "Freed ID", "synthetic maintenance-record envelope, digest, derivation, amendment, expiry, revocation hold, and live-proof refusal", ["W3C-VC-DM-20", "W3C-DATA-INTEGRITY", "W3C-PROV"]),
    ("Nonproduction Freed ID tool-part provenance notice with selective-disclosure abstention", "freed-id-maintenance-provenance", "Freed ID and CBR Heart", "tool and part provenance notice, purpose, minimum disclosure, challenge route, expiry, and trust-decision refusal", ["W3C-VC-DM-20", "NZ-PRIVACY-PRINCIPLES", "W3C-PROV"]),
    ("Keyboard-readable maintenance evidence atlas with reserved human evaluation", "maintenance-accessible-evidence-atlas", "CBR Heart and THOS Body", "accessible maintenance evidence atlas, scoped tables, noncolour states, source links, reflow, and manual-evaluation reservation", ["W3C-WCAG-22", "W3C-PROV", "NZ-PRIVACY-PRINCIPLES"]),
    ("CAA and FAA service-difficulty zero-row gateway with disabled transport", "maintenance-zero-row-sdr-gateway", "All pillars", "external service-difficulty capability, source watch, disabled transport, schema placeholders, zero rows, and external-validation refusal", ["FAA-AC20-109B", "FAA-SDR-DOWNLOAD", "NZCAA-P43-B"]),
    ("CBR aircraft-maintenance safety, privacy, incident-disclosure, remedy and Māori-authority covenant", "cbr-maintenance-authority-covenant", "CBR Heart across all pillars", "worker and passenger safety, maintenance and incident privacy, disclosure, remedy, affected-party governance, law, culture, and Māori-authority reservation", ["NZ-PRIVACY-PRINCIPLES", "TE-MANA-RARAUNGA", "LOCAL-CONTEXTS-TK"]),
]


PROPOSALS = [proposal(index, *spec) for index, spec in enumerate(PROPOSAL_SPECS, 1)]


SKILL_SPECS = [
    ("ghc-family-maintenance-scope-firewall", "Constrain fictional aircraft and organisation aliases, zero operational records, bounded purpose, and no airworthiness use."),
    ("ghc-family-maintenance-configuration-control", "Constrain aircraft, maintenance-data, applicability, effectivity, revision, and conflict-hold records."),
    ("ghc-family-maintenance-task-card", "Constrain work-order steps, prerequisites, interruptions, amendments, and certification abstention."),
    ("ghc-family-maintenance-tool-part-provenance", "Constrain calibration, expiry, part documentation, batch, custody, quarantine, and installation abstention."),
    ("ghc-family-maintenance-inspection-boundary", "Constrain NDT, critical tasks, independent inspection, functional checks, and competence or release refusal."),
    ("ghc-family-maintenance-human-factors", "Constrain workload, fatigue placeholders, interruptions, reconciliation, and synthetic handover."),
    ("ghc-family-gmut-fatigue-firewall", "Constrain typed fatigue and damage operators, units, domains, identifiability, falsifiers, and airworthiness refusal."),
    ("ghc-family-thos-maintenance-checkpoint", "Constrain deterministic batches, checkpoints, bounded retries, orphan isolation, and handover proxies."),
    ("ghc-family-maintenance-freed-id", "Constrain nonproduction record and tool-part lineage, digests, amendments, expiry, and trust abstention."),
    ("ghc-family-maintenance-authority-reservation", "Fail closed around people, aircraft, safety decisions, privacy, law, culture, affected parties, and Māori authority."),
]


RUNNER_SPECS = [
    ("ghc_family_maintenance_scope_firewall.py", "aircraft-maintenance-scope-card"),
    ("ghc_family_maintenance_configuration_control.py", "maintenance-effectivity-baseline"),
    ("ghc_family_maintenance_task_card.py", "maintenance-task-card-lifecycle"),
    ("ghc_family_maintenance_tool_part_provenance.py", "maintenance-tool-calibration-ledger"),
    ("ghc_family_maintenance_inspection_boundary.py", "maintenance-ndt-boundary"),
    ("ghc_family_maintenance_human_factors.py", "maintenance-human-factors-handover"),
    ("ghc_family_gmut_fatigue_firewall.py", "gmut-fatigue-damage-operator"),
    ("ghc_family_thos_maintenance_checkpoint.py", "thos-maintenance-checkpoint"),
    ("ghc_family_maintenance_freed_id.py", "freed-id-maintenance-record"),
    ("ghc_family_maintenance_authority_reservation.py", "cbr-maintenance-authority-covenant"),
]


def negative(number: int, slug: str, failure: str, recovery: str, guard: str) -> dict:
    return {
        "negative_id": f"V6587-X1-N{number:02d}",
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
    negative(1, "activation-packet-whole-display-truncated", "The first whole-packet display exceeded the bounded output surface and truncated before EOF.", "Reread the immutable packet in bounded numbered line windows through exact EOF.", "Use bounded line windows for long activation packets and retain the initial truncation at zero credit."),
    negative(2, "prospective-manifest-byte-domain-mismatch", "Read-only inheritance review found that Neris prospective manifests had exact Git blob identities but checkout-byte lengths in a field described as Git-clean blob bytes; CRLF files therefore showed metadata-size divergence.", "Credit only the exact Git-blob replay already verified, preserve the metadata defect, and make Vesper manifests calculate or label byte domains exactly.", "Never infer blob-byte size from a Windows checkout; hash and size the exact prospective Git-clean bytes."),
    negative(3, "worktree-registration-before-checkout-quiescence", "The worktree-add wrapper yielded after registration while checkout remained active, and the first target-workdir audit failed because the directory was not yet ready.", "Do not retry; audit registration, branch, head, process state, eventual path readiness, and clean state until the original operation completes.", "After a worktree wrapper yield, prove quiescence and target readiness before any mutation."),
    negative(4, "tasklist-filter-quoting-fault", "The first cmd-style tasklist filter split the IMAGENAME equality expression and returned an invalid-option error.", "Invoke tasklist through PowerShell with the entire filter as one literal argument.", "Keep Windows native filter expressions in one literal argument and inspect the exact error before retry."),
    negative(5, "profile-shell-native-probe-silence", "Login-profile PowerShell wrappers returned empty output while checkout activity was still present.", "Use non-login PowerShell for bounded repository probes and serialize command metadata when process completion is uncertain.", "Prefer login=false for Windows repository probes and never treat silence as passing evidence."),
    negative(6, "combined-manifest-map-no-output", "The first combined four-manifest tree-map wrapper returned no serialized evidence.", "Replay each immutable manifest in a bounded per-revision scalar check.", "Keep manifest replays revision-local and bounded; no output earns zero credit."),
    negative(7, "status-traversal-yielded-before-clean-proof", "The first full status wrapper yielded while its traversal child remained active and therefore supplied no clean-state proof.", "Wait for the original child, then prove tracked, staged, and untracked state with separate scalar checks.", "Use split clean-state probes after a long status traversal and never duplicate a still-running operation."),
    negative(8, "powershell-utf8nobom-enum-incompatibility", "A PowerShell 5.1 diagnostic wrapper rejected the utf8NoBOM encoding enum before hashing the route-state bytes.", "Hash the exact Git blob through a byte-preserving subprocess and avoid rewriting the content.", "Do not assume PowerShell 7 encoding enums in Windows PowerShell 5.1."),
    negative(9, "broad-official-search-output-truncation", "The first four-query official-source search exceeded the available result context and was truncated.", "Repeat only bounded pairs of domain-filtered official queries and use primary or regulator pages.", "Limit technical source searches to one or two precise official-domain queries per call."),
    negative(10, "primary-pillar-label-omitted-mind-token", "The first scoped x1 test found that the primary-focus string used typed GMUT wording but omitted the exact protected pillar label GMUT Mind.", "Add the exact GMUT Mind label while retaining THOS Body as primary and leaving all authority boundaries unchanged.", "Assert the exact names of all protected Trinity Mandala pillars before x1 freeze."),
    negative(11, "staged-privacy-scan-self-definition-candidate", "The first exact staged privacy scan matched the builder's own literal scanner-policy definition and reported one unqualified candidate.", "Classify the exact policy-definition path separately, retain the candidate, and require zero confirmed payload hits across every staged file.", "Separate scanner-definition candidates from confirmed privacy findings without suppressing any staged path."),
    negative(12, "stale-label-exclusion-path-domain-fault", "The first staged stale-label probe used glob exclusions that did not bind to Windows-rendered path separators, so inherited frozen-chain and nearest-neighbour provenance produced metadata candidates and a context-truncated stream.", "Use an explicit active-code and current-authored-document allowlist while reviewing inherited provenance files separately as immutable evidence.", "Never infer stale current content from inherited proposal or novelty metadata; bind the audit to exact active paths."),
]


SAFE_TASKS = [
    {
        "task_id": f"V6587-SAFE-{index:03d}",
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
        "task_id": f"V6587-CAND-{index:03d}",
        "task": f"Prototype a reversible cross-surface refinement for {PROPOSALS[(index - 1) % len(PROPOSALS)]['slug']}.",
        "approval_class": "candidate_owner_local_review_required",
        "x1_execution": False,
        "planned_lane": "x2_if_bounded_evidence_permits",
    }
    for index in range(1, 21)
]


CLEAN_TASKS = [
    {
        "task_id": f"V6587-CLEAN-{index:03d}",
        "task": f"Run additive compatibility, privacy, provenance, stale-label, and nonpromotion cleanup for {item['slug']}.",
        "approval_class": "safe_now_additive_cleanup",
        "x1_execution": False,
        "planned_lane": "x2",
    }
    for index, item in enumerate(PROPOSALS, 1)
]
