#!/usr/bin/env python3
"""Frozen x1 data for Elaren Kestrel's v654-v7 phase."""

from __future__ import annotations


PHASE = "v654-v7"
PHASE_CODE = "V6547"
OWNER = "Elaren Kestrel"
PRONOUNS = "they/them"
ROLE = "relational privacy-boundary steward and evidence cartographer"
HOPE = (
    "make identity and records systems easier to contest, minimize, recover, "
    "and govern without promoting prototypes into authority"
)
BRANCH = "codex/GHC-Family/elaren-kestrel-v654-v7-full-tools"
PHASE_ROOT = "docs/elaren-kestrel/v654-v7"

SOURCE_OWNER = "Eiren Kestrel"
SOURCE_BRANCH = "codex/GHC-Family/eiren-kestrel-v654-v6-2-remaster"
SOURCE_TAVIAN = "a6987b3a572254d52721066d19bdbcd0686a8098"
SOURCE_X1 = "37872a3fb9593bd0a8d862164a0ccc44bb946793"
SOURCE_EVIDENCE = "f878615e289d8d383bc54f75c0dca4c75b16b0e4"
SOURCE_FINAL = "fe0dda857137856654566b52875df769ecf781dd"
PRIOR_FROZEN = 1870
SOURCE_EFFECTIVE_NEGATIVES = 11871
SOURCE_OPEN_GAPS = 86
SOURCE_EXACT_GATES = 85
SOURCE_METHODS = 130

PRIMARY_FOCUS = "Freed ID and CBR Heart"
BOUNDED_PRACTICE = (
    "privacy engineering and public-interest records stewardship, used only as "
    "a bounded specification, synthetic-fixture, and evidence-assurance lens"
)
OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]
PROTECTED_GATES = [
    "real_empirical_data_and_likelihood",
    "real_participants_affected_parties_and_communities",
    "professional_scientific_engineering_security_identity_and_governance_authority",
    "production_identity_issuance_resolution_status_revocation_and_interoperability",
    "privacy_complete",
    "exhaustive_security",
    "complete_accessibility",
    "legal_cultural_and_maori_authority",
    "affected_party_acceptance_remedy_and_beneficiary_privacy",
    "independent_team_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]

OFFICIAL_SOURCES = [
    {
        "source_id": "W3C-VC-DM-2",
        "title": "Verifiable Credentials Data Model v2.0",
        "publisher": "W3C",
        "url": "https://www.w3.org/TR/vc-data-model/",
        "status": "stable",
        "use": "credential lifecycle, subject, issuer, holder, verifier, and privacy vocabulary",
    },
    {
        "source_id": "W3C-VC-DI-1",
        "title": "Verifiable Credential Data Integrity 1.0",
        "publisher": "W3C",
        "url": "https://www.w3.org/TR/vc-data-integrity/",
        "status": "stable",
        "use": "proof-domain, verification-method, and securing-mechanism boundaries",
    },
    {
        "source_id": "W3C-BSL-1",
        "title": "Bitstring Status List v1.0",
        "publisher": "W3C",
        "url": "https://www.w3.org/TR/vc-bitstring-status-list/",
        "status": "stable",
        "use": "status freshness, caching, correlation, and revocation semantics",
    },
    {
        "source_id": "NIST-800-63-4",
        "title": "Digital Identity Guidelines, Revision 4",
        "publisher": "NIST",
        "url": "https://pages.nist.gov/800-63-4/",
        "status": "current",
        "use": "identity risk, assurance, redress, recovery, privacy, and customer-experience controls",
    },
    {
        "source_id": "NIST-PF-1",
        "title": "NIST Privacy Framework 1.0",
        "publisher": "NIST",
        "url": "https://www.nist.gov/privacy-framework/privacy-framework",
        "status": "stable",
        "use": "privacy-risk governance and processing-data management",
    },
    {
        "source_id": "NIST-PF-11-IPD",
        "title": "NIST Privacy Framework 1.1 Initial Public Draft",
        "publisher": "NIST",
        "url": "https://www.nist.gov/news-events/news/2025/04/nist-privacy-framework-11-initial-public-draft-available-comment",
        "status": "draft",
        "use": "watch-only mapping for evolving privacy-risk language",
    },
    {
        "source_id": "IETF-RFC9700",
        "title": "Best Current Practice for OAuth 2.0 Security",
        "publisher": "IETF",
        "url": "https://datatracker.ietf.org/doc/html/rfc9700",
        "status": "current",
        "use": "authorization, token, redirect, sender-constraint, and downgrade boundaries",
    },
    {
        "source_id": "NZ-OPC-PRINCIPLES",
        "title": "New Zealand Privacy Act principles",
        "publisher": "Office of the Privacy Commissioner New Zealand",
        "url": "https://www.privacy.org.nz/privacy-principles/",
        "status": "current",
        "use": "collection, use, disclosure, correction, retention, and security reservations",
    },
    {
        "source_id": "NZ-ARCHIVES-DISPOSAL",
        "title": "Disposal guidance",
        "publisher": "Archives New Zealand",
        "url": "https://www.archives.govt.nz/manage-information/how-to-manage-your-information/disposal",
        "status": "current",
        "use": "records retention, disposal authority, transfer, destruction, and audit controls",
    },
    {
        "source_id": "W3C-WCAG-22",
        "title": "Web Content Accessibility Guidelines 2.2",
        "publisher": "W3C",
        "url": "https://www.w3.org/TR/WCAG22/",
        "status": "stable",
        "use": "accessible static-report and lifecycle-explainer structure",
    },
    {
        "source_id": "TMR-PRINCIPLES",
        "title": "Principles of Māori Data Sovereignty",
        "publisher": "Te Mana Raraunga",
        "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
        "status": "current",
        "use": "authority reservation and Māori data-sovereignty boundary only",
    },
    {
        "source_id": "W3C-BBS-WATCH",
        "title": "Selective-disclosure cryptosuite work",
        "publisher": "W3C Verifiable Credentials Working Group",
        "url": "https://www.w3.org/TR/vc-di-bbs/",
        "status": "watch",
        "use": "non-production selective-disclosure compatibility watch only",
    },
]


def _proposal(
    number: int,
    title: str,
    slug: str,
    pillar: str,
    disposition: str,
    mechanism: str,
    sources: list[str],
) -> dict:
    if disposition == "completed":
        approval = "safe_now_bounded_structural_or_synthetic_software"
        lane = "x2_owner_local_bounded"
        acceptance = (
            "The valid fixture passes, all five preregistered mutations are rejected, "
            "and the receipt makes no external, production, participant, authority, "
            "effectiveness, or completeness claim."
        )
    elif disposition == "represented":
        approval = "candidate_bounded_synthetic_proxy"
        lane = "x2_synthetic_representation_only"
        acceptance = (
            "The protocol and mutation evidence pass while real infrastructure, keys, "
            "records, affected users, professional review, or production operation stay absent."
        )
    elif disposition == "open_gap":
        approval = "candidate_real_interoperability_and_participant_evidence_required"
        lane = "x2_zero_live_action_readiness_only"
        acceptance = (
            "Emit a zero-account, zero-key, zero-query, zero-participant refusal receipt "
            "and leave the empirical or interoperability gap open."
        )
    else:
        approval = "exact_affected_party_legal_cultural_and_maori_authority_required"
        lane = "x2_reservation_matrix_only"
        acceptance = (
            "Emit unresolved authority, remedy, language, sovereignty, and governance "
            "reservations only; make no legal, cultural, Māori-authority, or affected-party decision."
        )
    return {
        "proposal_id": f"{PHASE_CODE}-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar": pillar,
        "mechanism": mechanism,
        "hypothesis": (
            f"A bounded {mechanism} contract can expose falsifiable obligations while "
            "refusing unsupported identity, scientific, operational, or authority promotion."
        ),
        "null_or_failure_condition": (
            f"The artifact omits a required {mechanism} obligation, accepts a frozen "
            "mutation, erases a failure, or exceeds its evidence and authority lane."
        ),
        "approval_class": approval,
        "execution_lane": lane,
        "official_or_primary_source_needs": sources,
        "concrete_artifacts": [
            f"surfaces/{slug}/contract.json",
            f"surfaces/{slug}/mutation-results.json",
            f"surfaces/{slug}/bounded-receipt.json",
        ],
        "falsifier_or_acceptance_gate": acceptance,
        "rollback_or_recovery": (
            "Stop, retain the failed witness at zero credit, rewrite no history, and "
            "leave account, sibling, participant, production, professional, legal, "
            "cultural, Māori-authority, and external state unchanged."
        ),
        "protected_gates": PROTECTED_GATES,
        "expected_disposition": disposition,
    }


_P = [
    (1, "Purpose-use binding ledger with declared purpose, allowed operation, prohibited reuse, provenance, expiry, and fail-closed decision", "purpose-use-binding", "Freed ID and CBR Heart", "completed", "purpose-to-operation binding", ["NIST-PF-1", "NZ-OPC-PRINCIPLES"]),
    (2, "Consent and authorization freshness lattice with grant class, scope, timestamp, withdrawal, delegation, conflict, and stale-grant refusal", "consent-freshness-lattice", "Freed ID and CBR Heart", "represented", "authorization freshness", ["NIST-800-63-4", "NZ-OPC-PRINCIPLES"]),
    (3, "Live status and revocation latency budget with publication interval, cache ceiling, offline age, uncertainty, outage, and stale-verifier refusal", "revocation-latency-budget", "Freed ID and CBR Heart", "represented", "live status freshness", ["W3C-BSL-1", "NIST-800-63-4"]),
    (4, "Selective-disclosure claim minimization compiler with request purpose, predicate sufficiency, attribute suppression, linkability warning, and oversharing rejection", "claim-minimization-compiler", "Freed ID and CBR Heart", "completed", "selective-disclosure minimization", ["W3C-VC-DM-2", "W3C-BBS-WATCH"]),
    (5, "Pairwise identifier unlinkability harness with relying-party domain, salt domain, rotation, collision, cross-context join, and correlation refusal", "pairwise-unlinkability-harness", "Freed ID and CBR Heart", "completed", "pairwise identifier unlinkability", ["W3C-VC-DM-2", "NIST-800-63-4"]),
    (6, "Status-list correlation leakage audit with index allocation, list population, retrieval path, cache behavior, churn, and herd-privacy warning", "status-correlation-audit", "Freed ID and CBR Heart", "completed", "status-list correlation leakage", ["W3C-BSL-1"]),
    (7, "Recovery and appeal dual-control workflow with requester, independent reviewer, evidence boundary, timeout, escalation, remedy, and unilateral-action refusal", "recovery-appeal-dual-control", "Freed ID and CBR Heart", "completed", "recovery and appeal dual control", ["NIST-800-63-4", "NZ-OPC-PRINCIPLES"]),
    (8, "Retention and cryptographic-erasure readiness contract with record class, disposal trigger, legal hold, key boundary, verification, and destruction-claim refusal", "retention-erasure-readiness", "Freed ID and CBR Heart", "represented", "retention and erasure readiness", ["NZ-ARCHIVES-DISPOSAL", "NZ-OPC-PRINCIPLES"]),
    (9, "Purpose-change reauthorization gate with original purpose, proposed purpose, compatibility test, notice, authority, consent dependency, and silent-reuse rejection", "purpose-change-reauthorization", "Freed ID and CBR Heart", "completed", "purpose-change reauthorization", ["NIST-PF-1", "NZ-OPC-PRINCIPLES"]),
    (10, "Remedy and beneficiary privacy-budget ledger with harm class, minimum disclosure, beneficiary shielding, fund audit placeholder, appeal, and publicity refusal", "remedy-beneficiary-budget", "Freed ID and CBR Heart", "completed", "remedy privacy budgeting", ["NZ-OPC-PRINCIPLES", "TMR-PRINCIPLES"]),
    (11, "Contestability and correction-statement propagation contract with disputed field, evidence, recipient set, correction status, downstream notice, and silent-overwrite refusal", "correction-propagation", "Freed ID and CBR Heart", "completed", "correction and contestability propagation", ["NZ-OPC-PRINCIPLES"]),
    (12, "Legal-hold and records-disposition simulator with authority placeholder, class, trigger, suspension, approval, audit trace, and unauthorized-disposal refusal", "records-disposition-simulator", "Freed ID and CBR Heart", "represented", "records disposition under holds", ["NZ-ARCHIVES-DISPOSAL"]),
    (13, "Algorithmic-decision notice completeness contract with decision purpose, data classes, logic category, material effect, challenge path, human contact, and opacity rejection", "decision-notice-completeness", "Freed ID and CBR Heart", "completed", "algorithmic decision notice completeness", ["NIST-PF-1", "NZ-OPC-PRINCIPLES"]),
    (14, "Accessible credential lifecycle explainer with issue, use, expiry, status, correction, recovery, revocation, help, and manual-evaluation reservation", "credential-lifecycle-accessibility", "Freed ID and CBR Heart", "completed", "credential lifecycle accessibility structure", ["W3C-WCAG-22", "W3C-VC-DM-2"]),
    (15, "Offline verifier freshness envelope with signed time, clock tolerance, maximum age, cached status, risk class, network absence, and freshness refusal", "offline-verifier-freshness", "Freed ID and CBR Heart", "completed", "offline verification freshness", ["W3C-BSL-1", "NIST-800-63-4"]),
    (16, "Issuer trust-registry dependency graph with authority source, namespace, delegation, expiry, revocation, conflict, missing resolver, and trust-promotion refusal", "trust-registry-dependency", "Freed ID and CBR Heart", "represented", "issuer trust dependency mapping", ["W3C-VC-DM-2", "NIST-800-63-4"]),
    (17, "Key-rotation split-brain guard with old and new verification windows, resolver view, status epoch, cache invalidation, rollback, and ambiguous-key rejection", "key-rotation-split-brain", "Freed ID and CBR Heart", "completed", "key rotation split-brain detection", ["W3C-VC-DI-1", "NIST-800-63-4"]),
    (18, "Pseudonym collision and identifier-reuse sentinel with namespace, derivation context, lifetime, collision witness, tombstone, and reassignment refusal", "pseudonym-reuse-sentinel", "Freed ID and CBR Heart", "completed", "pseudonym collision and reuse detection", ["W3C-VC-DM-2", "NIST-PF-1"]),
    (19, "Holder-binding downgrade-resistance contract with binding class, channel, proof domain, assurance transition, recovery state, and weaker-mode refusal", "holder-binding-downgrade", "Freed ID and CBR Heart", "completed", "holder-binding downgrade resistance", ["W3C-VC-DI-1", "IETF-RFC9700"]),
    (20, "Credential status-event causal-order validator with issuance, suspension, refresh, revocation, correction, recovery, clock skew, and impossible-order rejection", "status-event-causality", "Freed ID and CBR Heart", "completed", "credential status event ordering", ["W3C-BSL-1", "W3C-VC-DM-2"]),
    (21, "Incident harm-triage template with impact category, urgency, evidence quality, vulnerable group, notification placeholder, remedy path, and real-case refusal", "incident-harm-triage", "Freed ID and CBR Heart", "completed", "synthetic incident harm triage", ["NIST-PF-1", "NZ-OPC-PRINCIPLES"]),
    (22, "Evidence-retention minimization matrix with claim class, minimum proof, retention clock, access class, hold override, disposal witness, and over-retention rejection", "evidence-retention-minimization", "Freed ID and CBR Heart", "completed", "evidence retention minimization", ["NZ-ARCHIVES-DISPOSAL", "NIST-PF-1"]),
    (23, "Authority-credential expiration clock with mandate source, territorial scope, role, delegation, effective interval, renewal evidence, and expired-authority refusal", "authority-expiration-clock", "Freed ID and CBR Heart", "completed", "authority credential expiry", ["W3C-VC-DM-2"]),
    (24, "Cross-jurisdiction conflict reservation map with data location, subject location, issuer location, rule source, conflict class, competent-review placeholder, and legal-conclusion refusal", "jurisdiction-conflict-map", "Freed ID and CBR Heart", "completed", "cross-jurisdiction conflict reservation", ["NZ-OPC-PRINCIPLES", "NIST-PF-1"]),
    (25, "THOS signed task-envelope rights boundary with objective, capability, data purpose, privacy class, expiry, revocation, rollback, and authority-escalation refusal", "thos-rights-task-envelope", "THOS Body", "completed", "rights-aware task envelope", ["IETF-RFC9700", "NIST-PF-1"]),
    (26, "THOS capability attenuation-chain checker with issuer, delegate, scope reduction, expiry, audience, replay key, conflict, and privilege-amplification rejection", "thos-capability-attenuation", "THOS Body", "completed", "capability attenuation chain", ["IETF-RFC9700"]),
    (27, "GMUT claim-to-observable preregistration hash chain with model version, observable, units, inclusion rule, null, analysis digest, timestamp, and hindsight-edit refusal", "gmut-preregistration-hash-chain", "GMUT Mind", "completed", "claim-to-observable preregistration integrity", ["NIST-PF-1"]),
    (28, "GMUT dimensional-provenance differential ledger with equation term, unit basis, coefficient origin, transformation, uncertainty class, revision, and silent-unit-drift rejection", "gmut-dimensional-provenance", "GMUT Mind", "completed", "dimensional provenance differential", ["NIST-PF-1"]),
    (29, "Real Freed ID interoperability and affected-user study adapter with standards profile, live keys, resolver, status, participant protocol, independent review, and zero-action firewall", "real-interoperability-study-adapter", "Freed ID and CBR Heart", "open_gap", "real interoperability and participant evidence readiness", ["W3C-VC-DM-2", "W3C-VC-DI-1", "W3C-BSL-1", "NIST-800-63-4"]),
    (30, "Affected-party and Māori authority governance reservation for identity, records, language, data sovereignty, remedy, beneficiary privacy, ratification, and enacted-law status", "affected-party-maori-governance", "Freed ID and CBR Heart", "exact_gate", "affected-party and Māori authority reservation", ["TMR-PRINCIPLES", "NZ-OPC-PRINCIPLES", "NZ-ARCHIVES-DISPOSAL"]),
]
PROPOSALS = [_proposal(*row) for row in _P]

SAFE_TASKS = [
    f"Build the bounded contract and five rejecting fixtures for {row['proposal_id']} {row['slug']}"
    for row in PROPOSALS
]
CANDIDATE_TASKS = [
    f"Resolve only the declared evidence lane for {row['proposal_id']} {row['mechanism']}"
    for row in PROPOSALS
]
SKILL_IDEAS = [
    "ghc-family-purpose-binding",
    "ghc-family-consent-freshness",
    "ghc-family-selective-disclosure-minimizer",
    "ghc-family-linkability-audit",
    "ghc-family-recovery-appeal-dual-control",
    "ghc-family-records-disposition-guard",
    "ghc-family-credential-lifecycle-accessibility",
    "ghc-family-offline-verifier-freshness",
    "ghc-family-capability-attenuation",
    "ghc-family-claim-observable-preregistration",
]
RUNNER_IDEAS = [
    "ghc_family_purpose_binding.py",
    "ghc_family_consent_freshness.py",
    "ghc_family_selective_disclosure_minimizer.py",
    "ghc_family_linkability_audit.py",
    "ghc_family_recovery_appeal_dual_control.py",
    "ghc_family_records_disposition_guard.py",
    "ghc_family_credential_lifecycle_accessibility.py",
    "ghc_family_offline_verifier_freshness.py",
    "ghc_family_capability_attenuation.py",
    "ghc_family_v654_v7_suite.py",
]
CLEAN_TASKS = [
    f"{kind} owner-local {surface} without deletion, sibling mutation, gate weakening, or unsupported promotion"
    for kind in ("CLEAN", "FIX", "REFINE")
    for surface in (
        "schema clarity",
        "purpose binding",
        "consent freshness",
        "records disposition",
        "privacy boundary",
        "rollback wording",
        "manifest coverage",
        "failure retention",
        "source status",
        "stale-label refusal",
    )
]


def _negative(number: int, signature: str, failed: str, recovery: str, guard: str) -> dict:
    return {
        "negative_id": f"{PHASE_CODE}-X1-N{number:02d}",
        "signature": signature,
        "failed": failed,
        "recovery": recovery,
        "recurrence_guard": guard,
        "credit": "retained_negative_zero_initial_pass_credit",
    }


X1_OPERATIONAL_NEGATIVES = [
    _negative(1, "parallel_skill_discovery_timeout_a", "The first parallel skill-discovery probe exceeded its bound and returned no complete evidence.", "Read the exact named skill sequentially through EOF.", "Prefer exact scalar skill reads over broad concurrent discovery."),
    _negative(2, "parallel_skill_discovery_timeout_b", "A second parallel discovery probe exceeded its bound and earned no read credit.", "Read only the routing reference named by the selected skill.", "Route from the selected SKILL.md before opening references."),
    _negative(3, "parallel_skill_discovery_timeout_c", "A third parallel discovery probe exceeded its bound and earned no read credit.", "Use one literal-path read with an explicit line count.", "Bound archive-backed reads independently."),
    _negative(4, "narrowed_skill_probe_timeout_a", "The first narrowed PowerShell skill probe still timed out.", "Use Python UTF-8 direct reads for the exact file.", "Switch access mechanism after a repeated shell timeout."),
    _negative(5, "narrowed_skill_probe_timeout_b", "The second narrowed PowerShell skill probe still timed out.", "Read the exact schema with Python UTF-8.", "Do not repeat the same timed-out shell shape."),
    _negative(6, "narrowed_skill_probe_timeout_c", "The third narrowed PowerShell skill probe still timed out.", "Read the exact current-state file with Python UTF-8.", "Use one bounded file at a time under archive pressure."),
    _negative(7, "stale_baton_path_assumption", "The first baton read targeted an older Eiren worktree and found no file.", "Resolve the committed baton from the exact verified source branch and tree.", "Never infer a baton path from an earlier owner lane."),
    _negative(8, "restricted_node_process_environment", "The first Node wrapper assumed unrestricted process.env access and failed before evidence collection.", "Launch Unicode-sensitive diagnostics through python -X utf8 without relying on private environment access.", "Treat secure-kernel process surfaces as capability-limited."),
    _negative(9, "composite_source_git_probe_timeout", "A composite source Git probe timed out before returning a complete cleanliness receipt.", "Run HEAD, branch, tracked status, untracked status, and remote equality as scalar probes.", "Split local Git state from remote state and avoid composite status wrappers."),
    _negative(10, "broad_receipt_search_timeout", "A broad cross-bank receipt search exceeded its bound and earned no terminal-source credit.", "Use exact committed receipt paths and live authoritative state.", "Narrow receipt discovery by phase, owner, and lifecycle."),
    _negative(11, "recursive_archive_search_timeout", "A recursive archive filename search timed out and reset its helper kernel.", "Use Git tree maps and exact phase-relative paths.", "Avoid recursive filesystem searches across the archive bank."),
    _negative(12, "node_baseline_composite_timeout", "The first Node baseline composite timed out before returning a complete result.", "Use bounded scalar shell probes for exact HEAD and branch.", "After a kernel reset, reduce the command surface before retry."),
    _negative(13, "source_truth_path_assumption", "The first source receipt inspection assumed phase-truth.json at the phase root and stopped on a missing path.", "Discover exact committed truth filenames before reading them.", "Resolve lifecycle artifact paths from the Git tree, not naming convention alone."),
    _negative(14, "inherited_proposal_id_global_uniqueness_assumption", "The first focused x1 test required all 1,900 row identifiers to be globally unique and failed because the inherited 1,870-row history intentionally preserves 20 earlier duplicate identifiers.", "Require Elaren's thirty new identifiers to be unique and disjoint from the inherited identifier set while preserving the inherited rows unchanged.", "Separate immutable historical irregularities from the current phase's additive uniqueness obligation."),
    _negative(15, "composite_staged_validation_wrapper_timeout", "The combined staged-review, diff-hygiene, test, and status wrapper exceeded its bound after writing a valid staged receipt but before returning a complete terminal result.", "Audit the receipt, unstaged diff, diff hygiene, and focused tests as separate bounded scalar checks.", "Do not aggregate several archive-backed validation gates into one timeout domain."),
    _negative(16, "composite_staged_scope_count_timeout", "The combined staged-count, unstaged-count, x2-path, and out-of-scope classification probe exceeded its bound and returned no complete scope result.", "Use the exact staged-review receipt for staged scope and path-bounded scalar Git checks for unstaged owner changes.", "Do not recompute a validated staged scope through a second aggregate Git wrapper."),
]
