#!/usr/bin/env python3
"""Frozen x1 catalogue for Lyren Moss's v657-v1 phase."""

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
        "observed_on": "2026-07-31",
        "use": use,
    }


OFFICIAL_SOURCES = [
    source(
        "NIST-SSDF-11",
        "Secure Software Development Framework (SSDF) Version 1.1",
        "National Institute of Standards and Technology",
        "https://csrc.nist.gov/pubs/sp/800/218/final",
        "stable",
        "secure-development, provenance, vulnerability, and release vocabulary only; no conformance or security verdict",
    ),
    source(
        "NIST-SSDF-12-DRAFT",
        "Secure Software Development Framework (SSDF) Version 1.2 Initial Public Draft",
        "National Institute of Standards and Technology",
        "https://csrc.nist.gov/Projects/ssdf/publications",
        "draft",
        "revision-watch vocabulary only; the draft is not treated as a final requirement",
    ),
    source(
        "NIST-SP800-61R3",
        "Incident Response Recommendations and Considerations for Cybersecurity Risk Management",
        "National Institute of Standards and Technology",
        "https://csrc.nist.gov/pubs/sp/800/61/r3/final",
        "current",
        "incident, evidence, containment, recovery, communication, and handover vocabulary only",
    ),
    source(
        "CISA-SBOM-RESOURCES",
        "Software Bill of Materials Resources",
        "Cybersecurity and Infrastructure Security Agency",
        "https://www.cisa.gov/topics/cyber-threats-and-advisories/sbom/sbomresourceslibrary",
        "current",
        "component-inventory and dependency-transparency vocabulary only; no completeness claim",
    ),
    source(
        "CISA-KEV",
        "Known Exploited Vulnerabilities Catalog",
        "Cybersecurity and Infrastructure Security Agency",
        "https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
        "current",
        "catalog identity and zero-row adapter readiness only; no network call or vulnerability decision",
    ),
    source(
        "SPDX-30",
        "SPDX Specification",
        "Linux Foundation SPDX Project",
        "https://spdx.dev/use/specifications/",
        "current",
        "package, file, snippet, relationship, checksum, license-reference, and lifecycle vocabulary only",
    ),
    source(
        "CYCLONEDX-17",
        "CycloneDX Specification Overview 1.7",
        "OWASP Foundation CycloneDX Project",
        "https://cyclonedx.org/specification/overview/",
        "current",
        "component, service, dependency, vulnerability, formulation, and attestation vocabulary only",
    ),
    source(
        "SLSA-PROVENANCE-12",
        "SLSA Provenance 1.2",
        "OpenSSF SLSA Project",
        "https://slsa.dev/spec/v1.2/provenance",
        "current",
        "subject, builder, build definition, run details, and material vocabulary without production attestation",
    ),
    source(
        "IN-TOTO-SPECS",
        "in-toto Specifications",
        "in-toto Project",
        "https://in-toto.io/docs/specs/",
        "current",
        "link, layout, statement, subject, predicate, material, and product vocabulary without signatures or trust",
    ),
    source(
        "W3C-PROV-O",
        "PROV-O: The PROV Ontology",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/prov-o/",
        "stable",
        "entity, activity, attribution, derivation, revision, invalidation, and delegation lineage",
    ),
    source(
        "RFC-3339",
        "RFC 3339: Date and Time on the Internet",
        "RFC Editor",
        "https://www.rfc-editor.org/rfc/rfc3339.html",
        "stable",
        "synthetic UTC timestamps, maintenance windows, embargo clocks, expiry, and handovers",
    ),
    source(
        "RFC-8785",
        "RFC 8785: JSON Canonicalization Scheme",
        "RFC Editor",
        "https://www.rfc-editor.org/rfc/rfc8785.html",
        "stable",
        "deterministic synthetic contracts, receipts, manifests, and patch cards",
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
        "purpose, collection, fairness, security, access, correction, retention, use, and disclosure reservations",
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
        "community-defined provenance, protocol, and permission vocabulary with community authority reserved",
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
]


PROTECTED_GATES = [
    "real_reporters_users_maintainers_operators_reviewers_communities_and_affected_parties",
    "real_repositories_services_components_dependencies_accounts_keys_artifacts_and_production_systems",
    "real_defect_triage_patch_merge_release_deployment_rollback_incident_and_procurement_decisions",
    "real_measurements_statistics_likelihoods_predictions_reliability_and_empirical_confirmation",
    "professional_software_engineering_security_incident_response_accessibility_privacy_operations_and_health_and_safety_authority",
    "sensitive_vulnerability_personal_operational_location_traditional_knowledge_and_culturally_restricted_information",
    "production_identity_live_keys_signatures_proofs_resolution_status_revocation_interoperability_and_trust",
    "privacy_complete",
    "exhaustive_security",
    "complete_accessibility",
    "legal_cultural_indigenous_traditional_knowledge_data_governance_and_maori_authority",
    "affected_party_consent_notice_contestation_remedy_collective_governance_and_release_acceptance",
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
    execution_lane = "x2_owner_local_bounded_synthetic"
    if expected_disposition == "open_gap":
        approval = "candidate_external_readiness_without_network_call"
        execution_lane = "x2_owner_local_zero_row_readiness"
    elif expected_disposition == "exact_gate":
        approval = "exact_approval_authorized_affected_party_required"
        execution_lane = "not_executed_authority_reservation"
    return {
        "proposal_id": f"V6571-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar_relation": pillar,
        "mechanism": mechanism,
        "hypothesis": (
            f"A bounded {mechanism} contract can expose falsifiable software obligations while "
            "refusing unsupported empirical, professional, security, accessibility, privacy, "
            "identity, production, legal, cultural, Māori-authority, or Stage 20 promotion."
        ),
        "null_or_failure_condition": (
            f"The artifact omits a required {mechanism} obligation, accepts a frozen mutation, "
            "erases a failure, or crosses a protected participant, empirical, professional, "
            "production, legal, cultural, Māori-authority, identity, or Stage 20 gate."
        ),
        "approval_class": approval,
        "execution_lane": execution_lane,
        "official_or_primary_source_needs": sources,
        "concrete_artifacts": [
            f"surfaces/{slug}/contract.json",
            f"surfaces/{slug}/mutation-results.json",
            f"surfaces/{slug}/bounded-receipt.json",
        ],
        "falsifier_or_acceptance_gate": (
            "The valid synthetic fixture passes, five preregistered mutations are rejected, "
            "and the receipt grants no real-user, maintainer, security, professional, production, "
            "legal, cultural, Māori-authority, identity, accessibility-complete, privacy-complete, "
            "security-complete, independent-reproduction, Theory-of-Everything, or Stage 20 credit."
        ),
        "rollback_or_recovery": (
            "Stop, retain the failed witness at zero credit, rewrite no history, and leave real "
            "people, repositories, services, accounts, credentials, components, incidents, "
            "vulnerability disclosures, production systems, sibling lanes, releases, deployments, "
            "professional decisions, and authority state unchanged."
        ),
        "protected_gates": PROTECTED_GATES,
        "expected_disposition": expected_disposition,
    }


PROPOSAL_SPECS = [
    ("Public-interest application asset census with service token, repository hold, deployment-context quarantine, custodian-role reservation, supersession lineage, and ownership nonclaim", "repair-asset-census", "Freed ID and CBR Heart", "public-interest application asset census, service token, repository hold, deployment-context quarantine, custodian-role reservation, supersession lineage, and ownership nonclaim", ["W3C-PROV-O", "NIST-SSDF-11", "RFC-8785"]),
    ("Repair request intake docket with symptom narrative, reporter pseudonym, urgency cue, duplicate link, consent-minimization check, and diagnosis refusal", "repair-request-intake", "CBR Heart and THOS Body", "repair request intake, symptom narrative, reporter pseudonym, urgency cue, duplicate link, consent minimization, and diagnosis refusal", ["NIST-SP800-61R3", "NZ-PRIVACY-PRINCIPLES", "W3C-PROV-O"]),
    ("Reproduction envelope with version, platform class, synthetic fixture, clock and locale controls, missing step, and real-user-impact noninference", "repair-reproduction-envelope", "GMUT Mind and THOS Body", "defect reproduction envelope, version, platform class, synthetic fixture, clock and locale controls, missing step, and real-user-impact noninference", ["NIST-SSDF-11", "RFC-3339", "W3C-PROV-O"]),
    ("Component relationship inventory with SPDX package token, CycloneDX dependency edge, version provenance, license-reference hold, and completeness refusal", "repair-component-inventory", "Freed ID and GMUT Mind", "component relationship inventory, SPDX package token, CycloneDX dependency edge, version provenance, license-reference hold, and completeness refusal", ["SPDX-30", "CYCLONEDX-17", "CISA-SBOM-RESOURCES"]),
    ("Defect severity deliberation card with impact class, exploitability placeholder, accessibility cue, confidence, competent-reviewer hold, and priority nonautomation", "repair-severity-card", "CBR Heart and GMUT Mind", "defect severity deliberation, impact class, exploitability placeholder, accessibility cue, confidence, competent-reviewer hold, and priority nonautomation", ["NIST-SP800-61R3", "W3C-WCAG-22", "NIST-SSDF-11"]),
    ("Repair proposal ancestry ledger with issue token, hypothesis branch, rejected alternative, change intent, review checkpoint, and merge-authority reservation", "repair-proposal-ancestry", "Freed ID and CBR Heart", "repair proposal ancestry, issue token, hypothesis branch, rejected alternative, change intent, review checkpoint, and merge-authority reservation", ["W3C-PROV-O", "NIST-SSDF-11", "RFC-8785"]),
    ("Maintainer authorization boundary matrix with repository-role placeholder, least privilege, expiry, dual review, emergency break-glass refusal, and no-appointment claim", "repair-maintainer-boundary", "Freed ID and CBR Heart", "maintainer authorization boundary, repository-role placeholder, least privilege, expiry, dual review, emergency break-glass refusal, and appointment nonclaim", ["NIST-SSDF-11", "RFC-3339", "W3C-VC-DM-20"]),
    ("Change-set provenance envelope with file intent, patch-digest placeholder, build subject, source-material link, review state, and signature nonclaim", "repair-changeset-envelope", "Freed ID and GMUT Mind", "change-set provenance, file intent, patch-digest placeholder, build subject, source-material link, review state, and signature nonclaim", ["SLSA-PROVENANCE-12", "IN-TOTO-SPECS", "RFC-8785"]),
    ("Dependency blast-radius map with direct and transitive distinction, runtime and optional scope, affected artifact set, unknown edge, and deployment-fitness refusal", "repair-blast-radius-map", "GMUT Mind and THOS Body", "dependency blast-radius mapping, direct and transitive distinction, runtime and optional scope, affected artifact set, unknown edge, and deployment-fitness refusal", ["CYCLONEDX-17", "SPDX-30", "CISA-SBOM-RESOURCES"]),
    ("Repair test contract with precondition, failing fixture, expected invariant, regression set, nondeterminism cue, and coverage-completeness refusal", "repair-test-contract", "GMUT Mind and THOS Body", "repair test contract, precondition, failing fixture, expected invariant, regression set, nondeterminism cue, and coverage-completeness refusal", ["NIST-SSDF-11", "W3C-PROV-O", "RFC-8785"]),
    ("Rollback rehearsal docket with restore point, data-shape hold, forward-fix alternative, abort condition, evidence capture, and recovery-readiness refusal", "repair-rollback-rehearsal", "THOS Body and CBR Heart", "rollback rehearsal, restore point, data-shape hold, forward-fix alternative, abort condition, evidence capture, and recovery-readiness refusal", ["NIST-SP800-61R3", "NIST-SSDF-11", "RFC-3339"]),
    ("Accessibility regression witness board with keyboard path, name role and state, focus visibility, noncolour cue, manual-evaluation hold, and complete-accessibility refusal", "repair-accessibility-regression", "THOS Body and CBR Heart", "accessibility regression witness, keyboard path, name role and state, focus visibility, noncolour cue, manual-evaluation hold, and complete-accessibility refusal", ["W3C-WCAG-22", "W3C-PROV-O", "RFC-3339"]),
    ("Privacy regression minimization docket with purpose, data category, retention delta, disclosure path, correction right, legal-review hold, and privacy-complete refusal", "repair-privacy-regression", "CBR Heart and Freed ID", "privacy regression minimization, purpose, data category, retention delta, disclosure path, correction right, legal-review hold, and privacy-complete refusal", ["NZ-PRIVACY-PRINCIPLES", "W3C-PROV-O", "RFC-3339"]),
    ("Coordinated vulnerability disclosure quarantine with reporter-channel placeholder, embargo clock, affected range, exploit-detail shield, competent-triage hold, and security-verdict refusal", "repair-vulnerability-quarantine", "CBR Heart and THOS Body", "coordinated vulnerability disclosure quarantine, reporter-channel placeholder, embargo clock, affected range, exploit-detail shield, competent-triage hold, and security-verdict refusal", ["NIST-SSDF-11", "NIST-SP800-61R3", "RFC-3339"]),
    ("Patch attestation nonclaim card with SLSA predicate vocabulary, in-toto subject, builder placeholder, material digest, unsigned state, and production-trust refusal", "repair-attestation-nonclaim", "Freed ID and GMUT Mind", "patch attestation nonclaim, SLSA predicate vocabulary, in-toto subject, builder placeholder, material digest, unsigned state, and production-trust refusal", ["SLSA-PROVENANCE-12", "IN-TOTO-SPECS", "RFC-8785"]),
    ("Release approval reservation board with candidate identifier, dependency lock, test-receipt links, risk-acceptance hold, separation of duties, and no-deployment order", "repair-release-reservation", "CBR Heart and THOS Body", "release approval reservation, candidate identifier, dependency lock, test-receipt links, risk-acceptance hold, separation of duties, and deployment-order refusal", ["NIST-SSDF-11", "SLSA-PROVENANCE-12", "W3C-PROV-O"]),
    ("Maintenance-window choreography with freeze start, stakeholder notice, dependency checkpoint, abort trigger, rollback window, readback, and no-operational authorization", "repair-window-choreography", "THOS Body and CBR Heart", "maintenance-window choreography, freeze start, stakeholder notice, dependency checkpoint, abort trigger, rollback window, readback, and operational-authorization refusal", ["NIST-SP800-61R3", "RFC-3339", "W3C-PROV-O"]),
    ("Incident-to-repair handover register with containment state, evidence preservation, unresolved hypothesis, workload cue, next-review checkpoint, and incident-command refusal", "repair-incident-handover", "THOS Body and CBR Heart", "incident-to-repair handover, containment state, evidence preservation, unresolved hypothesis, workload cue, next-review checkpoint, and incident-command refusal", ["NIST-SP800-61R3", "W3C-PROV-O", "RFC-3339"]),
    ("Replacement component equivalence proxy with interface contract, behavioral delta, support-horizon placeholder, migration-cost hold, unknown risk, and procurement refusal", "repair-component-equivalence", "GMUT Mind and CBR Heart", "replacement component equivalence, interface contract, behavioral delta, support-horizon placeholder, migration-cost hold, unknown risk, and procurement refusal", ["SPDX-30", "CYCLONEDX-17", "NIST-SSDF-11"]),
    ("Warranty and license interpretation reservation docket with package context, obligation placeholder, conflicting notice, counsel hold, and legal-conclusion refusal", "repair-legal-reservation", "CBR Heart and Freed ID", "warranty and license interpretation reservation, package context, obligation placeholder, conflicting notice, counsel hold, and legal-conclusion refusal", ["SPDX-30", "W3C-PROV-O", "RFC-3339"]),
    ("Accessible community repair notice with plain-language summary, heading hierarchy, status text, known limitation, correction link, translation hold, and affected-user review", "repair-community-notice", "THOS Body and CBR Heart", "accessible community repair notice, plain-language summary, heading hierarchy, status text, known limitation, correction link, translation hold, and affected-user review reservation", ["W3C-WCAG-22", "NZ-PRIVACY-PRINCIPLES", "W3C-PROV-O"]),
    ("Repair contestation and correction docket with pseudonymous account, competing evidence, uncertainty, response clock, remedy hold, and consensus-promotion refusal", "repair-contestation-docket", "CBR Heart and Freed ID", "repair contestation and correction, pseudonymous account, competing evidence, uncertainty, response clock, remedy hold, and consensus-promotion refusal", ["NZ-PRIVACY-PRINCIPLES", "W3C-PROV-O", "RFC-3339"]),
    ("Sensitive and culturally restricted maintenance-publication firewall with audience grant, redaction class, community checkpoint, expiry, audit trail, and fail-closed disclosure", "repair-sensitive-publication", "CBR Heart and Freed ID", "sensitive and culturally restricted maintenance-publication firewall, audience grant, redaction class, community checkpoint, expiry, audit trail, and fail-closed disclosure", ["TMR-PRINCIPLES", "LOCAL-CONTEXTS-LABELS", "NZ-PRIVACY-PRINCIPLES"]),
    ("GMUT Bayesian defect-prior dimensional proxy with likelihood vocabulary, prior provenance, calibration quarantine, sensitivity envelope, and prediction refusal", "gmut-repair-defect-prior", "GMUT Mind", "GMUT Bayesian defect-prior dimensional proxy, likelihood vocabulary, prior provenance, calibration quarantine, sensitivity envelope, and prediction refusal", ["NIST-SSDF-11", "RFC-8785", "W3C-PROV-O"]),
    ("GMUT repairable-system hazard-rate dimensional proxy with observation window, censoring, unit discipline, competing-failure cue, calibration hold, and reliability-claim refusal", "gmut-repair-hazard-rate", "GMUT Mind", "GMUT repairable-system hazard-rate dimensional proxy, observation window, censoring, unit discipline, competing-failure cue, calibration hold, and reliability-claim refusal", ["RFC-3339", "RFC-8785", "W3C-PROV-O"]),
    ("THOS maintainer-shift handover choreography with alert backlog, partial rollback, fatigue and workload cue, safety stop, readback, and operations-decision refusal", "thos-repair-handover", "THOS Body", "THOS maintainer-shift handover choreography, alert backlog, partial rollback, fatigue and workload cue, safety stop, readback, and operations-decision refusal", ["NIST-SP800-61R3", "RFC-3339", "W3C-PROV-O"]),
    ("Freed ID synthetic maintainer-role credential capsule with purpose, audience, minimized claims, expiry, correction, revocation placeholder, and live proof disabled", "freed-id-maintainer-capsule", "Freed ID and CBR Heart", "Freed ID synthetic maintainer-role credential capsule, purpose, audience, minimized claims, expiry, correction, revocation placeholder, and live-proof refusal", ["W3C-VC-DM-20", "W3C-DID-10", "NZ-PRIVACY-PRINCIPLES"]),
    ("Freed ID synthetic patch provenance card with subject digest, material link, review relation, disclosure shield, unsigned state, and origin nonclaim", "freed-id-patch-card", "Freed ID", "Freed ID synthetic patch provenance card, subject digest, material link, review relation, disclosure shield, unsigned state, and origin nonclaim", ["SLSA-PROVENANCE-12", "IN-TOTO-SPECS", "NZ-PRIVACY-PRINCIPLES"]),
    ("CISA Known Exploited Vulnerabilities no-network query readiness with product placeholder, catalog-version hold, snapshot-digest reservation, zero rows, citation capture, and exploitability refusal", "repair-kev-zero-row", "Freed ID and GMUT Mind", "CISA Known Exploited Vulnerabilities no-network query readiness, product placeholder, catalog-version hold, snapshot-digest reservation, zero rows, citation capture, and exploitability refusal", ["CISA-KEV", "NIST-SSDF-11", "NZ-PRIVACY-PRINCIPLES"]),
    ("CBR public-interest software repair authority non-automation covenant for safety, security, release, maintainer impact, privacy, accessibility, remedy, law, culture, data governance, and Māori authority", "cbr-repair-authority-covenant", "CBR Heart", "public-interest software repair authority non-automation for safety, security, release, maintainer impact, privacy, accessibility, remedy, law, culture, data governance, and Māori authority", ["TMR-PRINCIPLES", "LOCAL-CONTEXTS-LABELS", "NZ-PRIVACY-PRINCIPLES", "W3C-WCAG-22"]),
]


PROPOSALS = [
    proposal(
        number,
        title,
        slug,
        pillar,
        mechanism,
        sources,
        "completed" if number <= 23 else "represented" if number <= 28 else "open_gap" if number == 29 else "exact_gate",
    )
    for number, (title, slug, pillar, mechanism, sources) in enumerate(PROPOSAL_SPECS, 1)
]


SKILL_SPECS = [
    ("ghc-family-repair-intake-provenance", "Freeze synthetic asset, defect-intake, reproduction, correction, and ownership boundaries."),
    ("ghc-family-repair-component-boundary", "Separate component and dependency structure from inventory completeness, license, procurement, and deployment claims."),
    ("ghc-family-repair-triage-nonpromotion", "Expose impact, severity, exploitability, and priority cues without issuing professional or operational decisions."),
    ("ghc-family-repair-changeset-attestation", "Preserve patch, material, builder, review, unsigned-state, and production-trust boundaries."),
    ("ghc-family-repair-test-rollback-evidence", "Constrain test, nondeterminism, rollback, forward-fix, and recovery-readiness evidence."),
    ("ghc-family-repair-privacy-accessibility", "Structure privacy and accessibility regression witnesses while reserving legal and affected-user evaluation."),
    ("ghc-family-repair-vulnerability-reserve", "Fail closed around vulnerability reporting, embargo, exploit detail, triage, notification, and security authority."),
    ("ghc-family-repair-release-handover", "Constrain maintenance windows, incidents, release reservations, readback, workload, and handover."),
    ("ghc-family-repair-freed-id-disclosure", "Constrain synthetic maintainer identity, purpose, disclosure, status, proof, and patch-lineage claims."),
    ("ghc-family-repair-cultural-authority", "Fail closed around restricted knowledge, community protocol, remedy, governance, and Māori authority."),
]


RUNNER_SPECS = [
    ("ghc_family_repair_intake_provenance.py", "repair-request-intake"),
    ("ghc_family_repair_component_boundary.py", "repair-component-inventory"),
    ("ghc_family_repair_triage_nonpromotion.py", "repair-severity-card"),
    ("ghc_family_repair_changeset_attestation.py", "repair-changeset-envelope"),
    ("ghc_family_repair_test_rollback.py", "repair-rollback-rehearsal"),
    ("ghc_family_repair_privacy_accessibility.py", "repair-accessibility-regression"),
    ("ghc_family_repair_vulnerability_reserve.py", "repair-vulnerability-quarantine"),
    ("ghc_family_repair_release_handover.py", "repair-window-choreography"),
    ("ghc_family_repair_freed_id_disclosure.py", "freed-id-maintainer-capsule"),
    ("ghc_family_repair_cultural_authority.py", "cbr-repair-authority-covenant"),
]


def negative(number: int, signature: str, observed: str, recovery: str, guard: str) -> dict:
    return {
        "negative_id": f"V6571-X1-N{number:02d}",
        "scope": "startup_and_x1",
        "signature": signature,
        "observed": observed,
        "credit": 0,
        "retained": True,
        "recovery": recovery,
        "recurrence_guard": guard,
        "same_owner_only": True,
        "independent_reproduction": False,
    }


X1_OPERATIONAL_NEGATIVES = [
    negative(1, "completion-gate-skill-login-shell-timeout", "The first login-shell read of the selected completion-gate skill exceeded its bound and returned no complete instruction evidence.", "Repeat only the same literal skill read without login-shell startup and continue through EOF.", "Keep instruction reads scalar and disable unnecessary login-shell initialization on bounded Windows probes."),
    negative(2, "powershell-d-candidate-probe-empty-pipe-element", "The first D-drive candidate probe contained an empty PowerShell pipeline element and failed before producing a path result.", "Materialize the bounded candidate list, then inspect each literal path in a separate pipeline.", "Materialize foreach output before piping and validate the expression before combining probes."),
    negative(3, "narrowed-d-candidate-probe-timeout", "A narrowed read-only D-drive candidate probe exceeded its outer bound without a complete source result.", "Use the exact activation branch and repository-relative baton to address one known source worktree directly.", "Prefer exact activation anchors over exploratory directory traversal when the source branch and baton are already supplied."),
    negative(4, "powershell-metadata-size-foreach-pipe-parser", "A metadata-size summary piped directly from foreach and failed during PowerShell parsing.", "Materialize each metadata row first, then pipe the completed array to the formatter.", "Separate collection from formatting in PowerShell metadata audits."),
    negative(5, "powershell-convert-tohexstring-unavailable", "The first external receipt digest sweep used Convert.ToHexString, which was unavailable in the installed PowerShell runtime.", "Repeat the bounded candidate-directory sweep with Get-FileHash SHA256 and retain a no-match result without expanding scope.", "Use Get-FileHash for portable Windows SHA-256 sweeps unless the runtime capability was proved first."),
    negative(6, "broad-external-receipt-filename-search-timeout", "A recursive exact-filename search across the archive exceeded 120 seconds and returned no complete result.", "Stop broad searching, retain the activation-supplied receipt digest, and rely only on exact source equality, ancestry, manifest replay, and the supplied canonical counts.", "Do not search the whole archive for external receipts when the activation provides a digest and repository verification is independently bounded."),
    negative(7, "additive-worktree-timeout-with-partial-checkout", "The additive D-first worktree wrapper timed out after registration, leaving the correct branch and HEAD with an incomplete 60,011-deletion checkout.", "Audit registration, branch, HEAD, process and lock state, then restore the worktree in place from HEAD and prove zero deleted, modified, and untracked files.", "After a mutating timeout, inspect durable state before retrying and recover the exact registered lane without creating a duplicate."),
    negative(8, "combined-post-recovery-audit-timeout", "The first combined HEAD, branch, status, and top-level audit timed out and returned no complete cleanliness proof.", "Run exact HEAD and branch probes separately, then count deleted, modified, and untracked paths with bounded scalar Git commands.", "Keep large-worktree cleanliness checks independent rather than bundling them into one orchestration call."),
    negative(9, "encoding-rendered-patch-context-mismatch", "Three context-rich patches did not match copied files at rendered encoding boundaries and changed nothing.", "Stop context retries, bind the replacement to ASCII-safe function or file anchors, write UTF-8 without a byte-order mark, and inspect the exact result.", "Avoid using terminal-rendered mojibake as patch context; bind edits to ASCII-safe anchors or complete UTF-8 file content."),
    negative(10, "combined-replacement-precondition-mismatch", "A bounded multi-replacement command stopped before writing because one expected Unicode line did not satisfy its regex precondition.", "Inspect exact UTF-8 source lines, then apply only small verified patches whose preconditions are present.", "Require every combined transformation precondition before writing and fall back to audited exact hunks on any mismatch."),
    negative(11, "powershell-composite-unicode-audit-parse-failure", "A composite stale-label audit embedded terminal-rendered Unicode in a PowerShell string and failed during parsing before scanning.", "Split the audit into ASCII-only stale-label patterns and a separate non-ASCII code-point inventory.", "Never copy rendered mojibake into a PowerShell regex literal; keep encoding and stale-label audits separate."),
    negative(12, "sequential-rg-no-match-treated-as-wrapper-failure", "A sequential multi-file audit stopped when an expected no-match ripgrep result returned exit code one.", "Run one bounded search across all declared files and explicitly treat ripgrep exit code one as a valid no-match state.", "Normalize documented search-tool no-match exits before composing sequential audits."),
    negative(13, "powershell-literal-path-existence-foreach-pipe-recurrence", "A literal-path existence audit repeated the PowerShell foreach-to-pipeline parser fault and failed before checking any path.", "Materialize all literal-path result rows first, then pass the completed array to JSON formatting.", "Encode the materialize-before-pipe rule directly in every PowerShell audit that begins with foreach."),
]


SAFE_TASKS = [
    {
        "task_id": f"V6571-SAFE-{index:03d}",
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
        "task_id": f"V6571-CAND-{index:03d}",
        "task": f"Prototype a reversible cross-surface refinement for {PROPOSALS[(index - 1) % len(PROPOSALS)]['slug']}.",
        "approval_class": "candidate_owner_local_review_required",
        "x1_execution": False,
        "planned_lane": "x2_if_bounded_evidence_permits",
    }
    for index in range(1, 21)
]


CLEAN_TASKS = [
    {
        "task_id": f"V6571-CLEAN-{index:03d}",
        "task": f"Run additive compatibility, privacy, provenance, and stale-label cleanup for {item['slug']}.",
        "approval_class": "safe_now_additive_cleanup",
        "x1_execution": False,
        "planned_lane": "x2",
    }
    for index, item in enumerate(PROPOSALS, 1)
]
