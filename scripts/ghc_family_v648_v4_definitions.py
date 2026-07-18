#!/usr/bin/env python3
"""Frozen definitions for Ilyra Fen's v648-v4 x1 packet."""

from __future__ import annotations

SOURCE_COMMIT = "979df78af2f5fe4eadd603e81234c4f88d5c10e0"
SOURCE_PHASE = "v648-gmut-thos-v3-x1-x2-r2"
SOURCE_BRANCH = "codex/GHC-Family/eiren-kestrel-v648-v3-2-full-tools"
SOURCE_X1_COMMIT = "723753e1a88427e1f8cd6ee572e3479c721dce84"
SOURCE_EVIDENCE_COMMIT = "e619a0221dc4a82aeb80ce783385a694e1d93657"
PHASE = "v648-gmut-thos-v4-x1-x2"
PHASE_SLUG = "v648-v4"
OWNER = "Ilyra Fen"
PRONOUNS = "she/they"
ROLE = "evidence-boundary steward"
HOPE = "leave every claim traceable and every gate unmistakable"
BRANCH = "codex/GHC-Family/ilyra-fen-full-tools"
PRIMARY_FOCUS = "Freed ID / CBR Heart"
BOUNDED_PRACTICE = (
    "community-radio emergency-bulletin revision, accessible fallback, correction readback, "
    "and shift handover as a learning and synthetic-design lens only"
)
OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]
SOURCE_STATUS_CLASSES = ["current", "stable", "draft", "watch"]
INHERITED_NEGATIVES = 4215
INHERITED_OPEN_GAPS = 29
INHERITED_EXACT_GATES = 30
PREREGISTERED_SYNTHETIC_NEGATIVES = 70


PROPOSALS = [
    {
        "proposal_id": "V6484-P01",
        "title": "Git mailmap canonical-display, multi-address mapping, ambiguous-entry, config-source, immutable-object, signature, provenance, privacy, and identity-nonreplacement tribunal",
        "pillar": "THOS Body",
        "hypothesis": "A disposable Git fixture can distinguish mailmap display projection from immutable commit-object and identity evidence while rejecting ambiguous mappings.",
        "null_or_failure_condition": "The tribunal rewrites commit objects, treats display mapping as identity replacement, accepts ambiguous precedence, or implies signature preservation without evidence.",
        "approval_class": "safe_now_owner_scoped_disposable_fixture",
        "execution_lane": "x2_build_task",
        "source_needs": ["SRC-GIT-MAILMAP"],
        "artifacts": ["tooling/mailmap-boundary-contract.json", "tooling/mailmap-boundary-mutations.json"],
        "falsifier_or_acceptance_gate": "All valid display mappings preserve object identity; ambiguity, external config substitution, signature overclaim, and identity replacement are rejected.",
        "rollback_or_recovery": "Discard the disposable fixture, retain every failed vector, and keep immutable object provenance authoritative.",
        "protected_gates": ["identity_records", "commit_object_integrity", "signature_truth", "external_callers"],
        "expected_disposition": "completed",
    },
    {
        "proposal_id": "V6484-P02",
        "title": "GMUT Cutkosky cut, Landau singularity, on-shell delta, branch discontinuity, optical-theorem, gauge, EFT, unit, and observation-firewall obligation board",
        "pillar": "GMUT Mind",
        "hypothesis": "A typed Cutkosky obligation board can separate perturbative discontinuity and unitarity bookkeeping from empirical GMUT support.",
        "null_or_failure_condition": "The board omits cut conditions, analytic domains, gauge or EFT qualifications, units, or converts a formal discontinuity into observed physics.",
        "approval_class": "safe_now_symbolic_research_only",
        "execution_lane": "x2_build_task",
        "source_needs": ["SRC-CUTKOSKY"],
        "artifacts": ["gmut/cutkosky-obligations.json", "gmut/cutkosky-mutations.json"],
        "falsifier_or_acceptance_gate": "Every accepted row names propagator, cut, analytic, gauge, EFT, unit, and observation boundaries; empirical confirmation remains false.",
        "rollback_or_recovery": "Withdraw the formal adapter and retain the mismatched obligation as a negative.",
        "protected_gates": ["empirical_confirmation", "physical_prediction", "quantum_completion", "theory_of_everything"],
        "expected_disposition": "completed",
    },
    {
        "proposal_id": "V6484-P03",
        "title": "GMUT Fermi-LAT 4FGL-DR4 source-catalog, exposure, diffuse-background, association, selection, covariance, spectral-systematic, checksum, and zero-row likelihood-refusal adapter",
        "pillar": "GMUT Mind",
        "hypothesis": "An official-format Fermi-LAT catalog contract can expose exact analysis prerequisites without treating catalog availability as a GMUT likelihood.",
        "null_or_failure_condition": "No real catalog rows, exposure model, diffuse background, selection function, covariance, preregistered likelihood, or independent review is present.",
        "approval_class": "real_data_and_independent_review_required",
        "execution_lane": "x2_open_gap",
        "source_needs": ["SRC-FERMI-DATA", "SRC-FERMI-DR4"],
        "artifacts": ["empirical/fermi-4fgl-dr4-study-contract.json", "empirical/fermi-4fgl-dr4-zero-row-receipt.json"],
        "falsifier_or_acceptance_gate": "Remain open_gap while zero real rows are ingested and likelihood, systematics, covariance, falsifiers, and independent review are absent.",
        "rollback_or_recovery": "Retain the zero-row refusal and make no fit, force, prediction, parameter, posterior, or confirmation claim.",
        "protected_gates": ["real_data", "empirical_likelihood", "independent_review", "physical_prediction"],
        "expected_disposition": "open_gap",
    },
    {
        "proposal_id": "V6484-P04",
        "title": "THOS community-radio emergency-bulletin source, CAP identifier, revision, cancellation, transcript, accessible fallback, correction-readback, workload, and shift-handover proxy",
        "pillar": "THOS Body",
        "hypothesis": "A synthetic CAP-aligned bulletin ledger can represent revision, correction, accessibility, workload, and handover obligations without real broadcasts or operators.",
        "null_or_failure_condition": "The proxy omits source, identifier, revision or cancellation lineage, transcript fallback, correction readback, owner, or workload boundary.",
        "approval_class": "safe_now_proxy_protocol_no_people_or_operations",
        "execution_lane": "x2_proxy_protocol",
        "source_needs": ["SRC-OASIS-CAP", "SRC-WCAG22"],
        "artifacts": ["thos/community-radio-handover-contract.json", "thos/community-radio-handover-vectors.json"],
        "falsifier_or_acceptance_gate": "Represented only when synthetic vectors preserve lineage and every real broadcast, emergency, worker, listener, and effectiveness claim remains false.",
        "rollback_or_recovery": "Revert to a design-only checklist, preserve the failed vector, and never transmit a real alert.",
        "protected_gates": ["real_operations", "public_safety", "professional_authority", "participant_effectiveness"],
        "expected_disposition": "represented",
    },
    {
        "proposal_id": "V6484-P05",
        "title": "Freed ID OAuth step-up insufficient-user-authentication, acr-values, max-age, token-context, challenge, downgrade, replay, metadata, and privacy profile",
        "pillar": "Freed ID / CBR Heart",
        "hypothesis": "Synthetic RFC 9470 vectors can test challenge propagation, recentness, authentication-context, downgrade, and privacy refusal without production identity operations.",
        "null_or_failure_condition": "The profile accepts missing or stale context, malformed max_age, unbound challenge, downgrade, replay, or treats an ACR label as universal assurance.",
        "approval_class": "safe_now_synthetic_nonproduction",
        "execution_lane": "x2_proxy_protocol",
        "source_needs": ["SRC-RFC9470", "SRC-RFC9470-ERRATA"],
        "artifacts": ["freed-id/oauth-step-up-profile.json", "freed-id/oauth-step-up-mutations.json"],
        "falsifier_or_acceptance_gate": "Represented only; synthetic tokens, absent live authentication, absent interoperability, and absent governance remain explicit.",
        "rollback_or_recovery": "Reject the fixture, retain the negative, and leave production authentication and trust decisions unmade.",
        "protected_gates": ["real_keys", "production_identity", "interoperability", "privacy_review", "trust_governance"],
        "expected_disposition": "represented",
    },
    {
        "proposal_id": "V6484-P06",
        "title": "CBR community-radio warning reach, disability access, language, journalist and listener privacy, correction, remedy, affected-party, legal, cultural, spectrum, and Māori-authority matrix",
        "pillar": "Freed ID / CBR Heart",
        "hypothesis": "A reservation matrix can expose community-radio remedy and authority dependencies without substituting repository authors for affected people or competent authorities.",
        "null_or_failure_condition": "Any real warning, access, privacy, spectrum, employment, remedy, language, cultural, legal, or Māori-authority decision is marked completed by software evidence.",
        "approval_class": "authorized_affected_parties_and_competent_authority_required",
        "execution_lane": "x2_exact_gate",
        "source_needs": ["SRC-OASIS-CAP", "SRC-NZ-PRIVACY", "SRC-TE-MANA-RARAUNGA"],
        "artifacts": ["cbr/community-radio-remedy-matrix.json", "cbr/community-radio-authority-reservation.json"],
        "falsifier_or_acceptance_gate": "Remain exact_gate until affected parties, tangata whenua, iwi, hapū, Māori authorities, and competent legal, cultural, disability, privacy, and spectrum authorities decide within scope.",
        "rollback_or_recovery": "Remove any accidental authority claim, retain the assumption failure, and preserve beneficiary and source privacy.",
        "protected_gates": ["affected_party_legitimacy", "maori_authority", "legal_interpretation", "cultural_ratification", "spectrum_authority"],
        "expected_disposition": "exact_gate",
    },
    {
        "proposal_id": "V6484-P07",
        "title": "iCalendar content-line folding, parameter quoting, component nesting, UID, sequence, recurrence, timezone, attachment, expansion-budget, and refusal tribunal",
        "pillar": "THOS Body",
        "hypothesis": "A bounded iCalendar parser tribunal can reject ambiguous, recursive, externally linked, or resource-exhausting synthetic calendar objects.",
        "null_or_failure_condition": "The tribunal accepts invalid folding, broken nesting, missing identity, unsafe attachment, unresolved timezone, or unbounded recurrence expansion.",
        "approval_class": "safe_now_owner_scoped_parser_fixture",
        "execution_lane": "x2_build_task",
        "source_needs": ["SRC-RFC5545", "SRC-ICAL-JSCAL-DRAFT"],
        "artifacts": ["formats/icalendar-contract.json", "formats/icalendar-mutations.json"],
        "falsifier_or_acceptance_gate": "All declared malformed fixtures are rejected, external retrieval is disabled, budgets are enforced, and no exhaustive-security claim is made.",
        "rollback_or_recovery": "Disable the wrapper, retain the failing fixture, and fall back to inert text display.",
        "protected_gates": ["external_payloads", "network_retrieval", "exhaustive_security", "production_parser"],
        "expected_disposition": "completed",
    },
    {
        "proposal_id": "V6484-P08",
        "title": "Accessible prerecorded-media captions, transcript, audio-description, track-label, language, control, fallback, keyboard, and manual-evaluation reservation audit",
        "pillar": "THOS Body",
        "hypothesis": "A structural audit can verify declared prerecorded-media alternatives and controls while reserving all manual and affected-user evaluation.",
        "null_or_failure_condition": "Media lacks caption or transcript association, track labels or language, nonvisual fallback, independent controls, keyboard structure, or honest reservation.",
        "approval_class": "safe_now_structural_only",
        "execution_lane": "x2_build_task",
        "source_needs": ["SRC-WCAG22", "SRC-WHATWG-MEDIA"],
        "artifacts": ["accessibility/prerecorded-media-contract.json", "accessibility/prerecorded-media-mutations.json"],
        "falsifier_or_acceptance_gate": "Pass only structural fixtures; reserve browser, keyboard, assistive-technology, cognitive, Māori-language, security-usability, and affected-user evaluation.",
        "rollback_or_recovery": "Publish an inert sequential transcript fallback and retain every structural failure.",
        "protected_gates": ["complete_accessibility", "manual_evaluation", "affected_user_acceptance", "language_authority"],
        "expected_disposition": "completed",
    },
    {
        "proposal_id": "V6484-P09",
        "title": "Thermo-Psyche thermodynamic-uncertainty current, entropy-production, precision-cost, steady-state, finite-time, unit, domain, and confidence-agency nonconversion classifier",
        "pillar": "Trinity Mandala bridge",
        "hypothesis": "A typed classifier can preserve thermodynamic-uncertainty assumptions while refusing conversion into psychological confidence, agency, worth, or consciousness.",
        "null_or_failure_condition": "A current-fluctuation precision bound is applied outside its dynamics or used as a measure of human confidence, agency, value, or mind.",
        "approval_class": "safe_now_formal_domain_guard",
        "execution_lane": "x2_build_task",
        "source_needs": ["SRC-TUR"],
        "artifacts": ["thermo-psyche/tur-contract.json", "thermo-psyche/tur-mutations.json"],
        "falsifier_or_acceptance_gate": "Every accepted row states dynamics, current, averaging regime, entropy production, units, bound direction, and domain; all psyche conversions are rejected.",
        "rollback_or_recovery": "Remove the analogy, retain only the physical statement, and preserve the rejected conversion.",
        "protected_gates": ["psyche_conversion", "consciousness", "personhood", "moral_value"],
        "expected_disposition": "completed",
    },
    {
        "proposal_id": "V6484-P10",
        "title": "Stage 20 staggered difference-in-differences cohort-time effect, parallel-trend, anticipation, interference, support, weighting, pretrend, sensitivity, and nonpromotion board",
        "pillar": "Trinity Mandala bridge",
        "hypothesis": "A difference-in-differences board can expose staggered-adoption identification obligations without converting zero-participant fixtures into causal evidence.",
        "null_or_failure_condition": "Parallel trends, anticipation, interference, comparison support, timing, weighting, pretrend limits, sensitivity, or value authority is omitted or software is promoted as an effect.",
        "approval_class": "safe_now_structural_nonpromotion",
        "execution_lane": "x2_build_task",
        "source_needs": ["SRC-DID"],
        "artifacts": ["stage20/did-contract.json", "stage20/did-mutations.json"],
        "falsifier_or_acceptance_gate": "Pass only structural protocol fixtures; real outcomes, credible identifying assumptions, safety monitoring, value authority, and independent review remain absent.",
        "rollback_or_recovery": "Retain the failed fixture and keep causal-effect and Stage 20 claims false.",
        "protected_gates": ["real_participants", "causal_effect", "value_authority", "independent_review", "stage20"],
        "expected_disposition": "completed",
    },
]


SOURCES = [
    {"source_id": "SRC-LIVE-REQUEST", "title": "Hamish current v648-v4 activation and committed Eiren baton", "url": None, "status": "current", "kind": "live_authority", "implication": "Controls solo ownership, no replay, x1-before-x2, four-commit cap, platform exclusions, privacy, and terminal route."},
    {"source_id": "SRC-GIT-MAILMAP", "title": "Git mailmap documentation", "url": "https://git-scm.com/docs/gitmailmap", "status": "current", "kind": "official", "implication": "Mailmap changes displayed canonical names and addresses; it is not an identity replacement or commit-object rewrite."},
    {"source_id": "SRC-CUTKOSKY", "title": "Singularities and Discontinuities of Feynman Amplitudes", "url": "https://doi.org/10.1063/1.1703676", "status": "stable", "kind": "primary_research", "implication": "Cut conditions constrain perturbative discontinuities; they are not empirical GMUT observations."},
    {"source_id": "SRC-FERMI-DATA", "title": "Fermi Science Support Center Data and Products", "url": "https://fermi.gsfc.nasa.gov/ssc/data/access/", "status": "current", "kind": "official", "implication": "The 4FGL-DR4 catalog and associated caveats define a possible data surface, not a GMUT likelihood."},
    {"source_id": "SRC-FERMI-DR4", "title": "HEASARC Fermi LAT 14-Year Point Source Catalog 4FGL-DR4", "url": "https://heasarc.gsfc.nasa.gov/W3Browse/fermi/fermilpsc.html", "status": "current", "kind": "official", "implication": "Catalog fields, provenance, associations, and release identity require explicit selection and systematic treatment."},
    {"source_id": "SRC-OASIS-CAP", "title": "OASIS Common Alerting Protocol 1.2", "url": "https://www.oasis-open.org/standard/cap/", "status": "stable", "kind": "official_standard", "implication": "CAP supplies structured identifiers, updates, cancellations, language, audience, and warning fields; it does not authorize a real broadcast."},
    {"source_id": "SRC-RFC9470", "title": "RFC 9470 OAuth 2.0 Step Up Authentication Challenge Protocol", "url": "https://www.rfc-editor.org/rfc/rfc9470.html", "status": "stable", "kind": "official_standard", "implication": "The protocol defines insufficient_user_authentication, acr_values, and max_age while leaving authentication mechanics and policy outside scope."},
    {"source_id": "SRC-RFC9470-ERRATA", "title": "RFC 9470 reported errata", "url": "https://www.rfc-editor.org/errata/rfc9470", "status": "watch", "kind": "official_status", "implication": "A reported example-timestamp erratum is monitored and never silently treated as accepted normative text."},
    {"source_id": "SRC-RFC5545", "title": "RFC 5545 iCalendar", "url": "https://www.rfc-editor.org/rfc/rfc5545.html", "status": "stable", "kind": "official_standard", "implication": "Content folding, components, parameters, recurrence, timezones, and attachments require bounded parsing policy."},
    {"source_id": "SRC-ICAL-JSCAL-DRAFT", "title": "IETF CALext iCalendar Format Extensions for JSCalendar draft", "url": "https://datatracker.ietf.org/doc/draft-ietf-calext-icalendar-jscalendar-extensions/", "status": "draft", "kind": "official_draft", "implication": "Extension properties remain work in progress; the bounded parser keeps unknown or draft semantics explicit and unpromoted."},
    {"source_id": "SRC-WCAG22", "title": "Web Content Accessibility Guidelines 2.2", "url": "https://www.w3.org/TR/WCAG22/", "status": "stable", "kind": "official_standard", "implication": "Media alternatives and operability obligations cannot be closed by structural checks alone."},
    {"source_id": "SRC-WHATWG-MEDIA", "title": "WHATWG HTML Standard media elements and timed text tracks", "url": "https://html.spec.whatwg.org/multipage/media.html", "status": "current", "kind": "official_standard", "implication": "Track kind, language, labels, captions, descriptions, and media controls provide structural contracts only."},
    {"source_id": "SRC-TUR", "title": "Thermodynamic Uncertainty Relation for Biomolecular Processes", "url": "https://doi.org/10.1103/PhysRevLett.114.158101", "status": "stable", "kind": "primary_research", "implication": "Current precision and entropy-production bounds are domain-specific physical results, not measures of psyche or agency."},
    {"source_id": "SRC-DID", "title": "Difference-in-Differences with Multiple Time Periods", "url": "https://doi.org/10.1016/j.jeconom.2020.12.001", "status": "stable", "kind": "primary_method", "implication": "Staggered treatment timing requires explicit comparison groups and identifying assumptions; a software board is not causal evidence."},
    {"source_id": "SRC-NZ-PRIVACY", "title": "New Zealand Privacy Commissioner privacy breach guidance", "url": "https://www.privacy.org.nz/responsibilities/privacy-breaches/", "status": "current", "kind": "official_authority", "implication": "Real harm, notification, privacy, and remedy decisions require competent human authority and affected-person consideration."},
    {"source_id": "SRC-TE-MANA-RARAUNGA", "title": "Te Mana Raraunga principles of Māori data sovereignty", "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "status": "stable", "kind": "primary_authority_source", "implication": "Māori data and concepts remain under Māori governance; software confers no Māori authority."},
    {"source_id": "SRC-CODEX-CLI", "title": "OpenAI Codex CLI stable package channel", "url": "https://www.npmjs.com/package/@openai/codex", "status": "watch", "kind": "official_package", "implication": "Version status may be observed, but this phase does not update the desktop application."},
]


SAFE_TASKS = [
    "Verify inherited anchors, zero merges, clean state, and fresh live equality",
    "Record D-first capacity and owner-lane continuity without cleanup",
    "Audit all 590 frozen titles for semantic neighbors and collisions",
    "Build the four-state official and primary source ledger",
    "Freeze the exact ten-proposal x1 contract without x2 outcomes",
    "Build the x1-to-x2 immutable Git-blob separation receipt",
    "Build exact staged-path allowlisting for owner-generated files",
    "Build five-class privacy scanning with candidate disposition",
    "Record startup parser and schema false assumptions before retries",
    "Build the phase Method Flow ledger with fail and pass witnesses",
    "Refresh the phase-scoped GHC Family Index",
    "Run Reflection-Remaster in read-only focused audit mode",
    "Build the disposable Git mailmap identity-boundary fixture plan",
    "Build the Cutkosky formal-obligation fixture plan",
    "Build the Fermi 4FGL-DR4 zero-row study contract",
    "Build the community-radio CAP handover proxy plan",
    "Build the OAuth step-up synthetic profile plan",
    "Build the community-radio CBR authority-reservation plan",
    "Build the bounded iCalendar refusal tribunal plan",
    "Build the prerecorded-media structural audit plan",
    "Build the thermodynamic-uncertainty domain guard plan",
    "Build the difference-in-differences nonpromotion board plan",
    "Freeze seventy rejecting synthetic mutations without execution credit",
    "Audit family-current callers and retain historical compatibility surfaces",
    "Pin UTF-8 for every Unicode-emitting phase command",
    "Build document-cap and file-baton word-count guards",
    "Build workload, wellbeing, and owner-file-threshold receipts",
    "Build stale-label, outcome-vocabulary, and noncompensation lints",
    "Hold terminal routing at PREPARED_NOT_SENT until final proof",
    "Verify CLI and desktop versions without updating the desktop app",
]


CANDIDATE_TASKS = [
    "Git mailmap display-versus-object identity fixture",
    "Cutkosky obligation classifier",
    "Fermi 4FGL-DR4 zero-row adapter",
    "Community-radio CAP revision and handover proxy",
    "OAuth step-up challenge profile",
    "Community-radio remedy and authority reservation matrix",
    "iCalendar expansion-budget refusal engine",
    "Prerecorded-media alternative structural auditor",
    "Thermodynamic-uncertainty domain classifier",
    "Difference-in-differences nonpromotion board",
    "Split ancestry and remote-equality proof wrapper",
    "Git-blob owner-manifest builder",
    "X1 immutable-tree outcome-absence checker",
    "Source-status and errata watch ledger",
    "Semantic-neighbor diagnostic with explicit numeric tie key",
    "Five-class privacy candidate adjudicator",
    "Method Flow record-to-witness crosslinker",
    "Single-pass validation noncompensation gate",
    "Document and baton word-count validator",
    "Exact-route hold and acknowledgement recorder",
]


SKILL_IDEAS = [
    "ghc-family-mailmap-identity-boundary",
    "ghc-family-cutkosky-obligations",
    "ghc-family-fermi-4fgl-dr4-zero-row",
    "ghc-family-community-radio-handover",
    "ghc-family-oauth-step-up-profile",
    "ghc-family-community-radio-authority-reservation",
    "ghc-family-icalendar-refusal-tribunal",
    "ghc-family-accessible-prerecorded-media",
    "ghc-family-tur-domain-guard",
    "ghc-family-did-nonpromotion",
    "ghc-family-exact-anchor-split-probe",
    "ghc-family-git-blob-owner-manifest",
    "ghc-family-single-pass-credit-v2",
    "ghc-family-source-status-ledger-v2",
    "ghc-family-semantic-neighbor-audit-v2",
    "ghc-family-privacy-candidate-disposition-v3",
    "ghc-family-x1-immutability-guard-v2",
    "ghc-family-document-baton-cap-guard",
    "ghc-family-terminal-route-hold-v2",
    "ghc-family-workload-boundary-v2",
]


RUNNER_IDEAS = [
    "ghc_family_mailmap_identity_boundary.py",
    "ghc_family_cutkosky_obligations.py",
    "ghc_family_fermi_4fgl_dr4_zero_row.py",
    "ghc_family_community_radio_handover.py",
    "ghc_family_oauth_step_up_profile.py",
    "ghc_family_community_radio_authority.py",
    "ghc_family_icalendar_tribunal.py",
    "ghc_family_accessible_prerecorded_media.py",
    "ghc_family_tur_domain_guard.py",
    "ghc_family_did_nonpromotion.py",
]


CLEANUP_TASKS = [
    "Preserve every inherited and current retained negative",
    "Recompute all count mirrors from authoritative ledgers",
    "Keep x1 paths immutable after the frozen commit",
    "Use Git-blob rather than checkout-byte identity for manifests",
    "Keep staged allowlists exact and owner-scoped",
    "Classify scanner definitions separately from confirmed payload hits",
    "Preserve unresolved privacy candidates until reviewed",
    "Normalize new generated text to UTF-8 and LF",
    "Check all generated JSON for deterministic key order",
    "Check every proposal field and protected gate is nonempty",
    "Check exactly four core outcome labels are used",
    "Check every source status uses current stable draft or watch",
    "Check citations never receive empirical evidence credit",
    "Check the Fermi adapter ingests zero real rows",
    "Check the THOS proxy contains zero people broadcasts or incidents",
    "Check Freed ID uses zero real keys accounts or tokens",
    "Check CBR makes zero real remedy or authority decisions",
    "Check Māori wording and governance remain exact-gated",
    "Check accessibility remains structural with manual evaluation reserved",
    "Check no Sandbox Hyper-V elevation or reboot action occurs",
    "Check no cross-platform sibling message occurs",
    "Check no raw task or thread identifier enters public artifacts",
    "Check no private absolute path enters public artifacts",
    "Check no credential private key token or callable identifier enters public artifacts",
    "Check no AGI ASI consciousness or personhood claim appears",
    "Check no empirical confirmation or Theory-of-Everything claim appears",
    "Check no independent-reproduction or repeatability credit appears",
    "Check every document remains at or below 6000 words",
    "Check owner-generated growth remains below 15000 files",
    "Keep the terminal route held until exact clean remote equality",
]


X1_OPERATIONAL_NEGATIVES = [
    {
        "negative_id": "V6484-X1-N01",
        "failure": "The first combined PowerShell source-proof wrapper embedded exit-code capture inside parenthesized command expressions and failed at parse time.",
        "recovery": "Run each ancestry command as an independent statement, capture LASTEXITCODE, and only then assemble the receipt.",
    },
    {
        "negative_id": "V6484-X1-N02",
        "failure": "The first version probe assumed a codex_cli field and returned null because the committed receipt schema uses codex_cli_after.",
        "recovery": "Inspect the exact serialized schema before property binding and read codex_cli_after without rewriting the source receipt.",
    },
    {
        "negative_id": "V6484-X1-N03",
        "failure": "The first x1 builder redundantly requested a candidate-to-validated state change after the Method Flow runner had already promoted each method when its passing witness was recorded.",
        "recovery": "Inspect the runner-produced state after witness ingestion and request only the remaining validated-to-preferred transition.",
    },
    {
        "negative_id": "V6484-X1-N04",
        "failure": "The first post-stage manifest coverage test inspected only unstaged and untracked paths and therefore reported every correctly staged x1 path as missing.",
        "recovery": "Union cached, unstaged, and untracked paths before comparing the intended x1 surface with manifest entries and declared self-exclusions.",
    },
    {
        "negative_id": "V6484-X1-N05",
        "failure": "A regenerated privacy scan read its prior self-referential receipt and classified the receipt's own scanner-class names as payload hits.",
        "recovery": "Treat only the exact declared privacy receipt and the scanner implementation as scanner-definition surfaces while keeping all other paths fail-closed.",
    },
]
