#!/usr/bin/env python3
"""Frozen definitions for Sable Rook's v648-v5 x1 packet."""

from __future__ import annotations

SOURCE_COMMIT = "99c22f254672807ee3839142f261d0ab01585a4a"
SOURCE_PHASE = "v648-gmut-thos-v4-x1-x2"
SOURCE_BRANCH = "codex/GHC-Family/ilyra-fen-full-tools"
SOURCE_X1_COMMIT = "29a68883f8caadf356531f67c8ac367ac5a289bb"
SOURCE_EVIDENCE_COMMIT = "d78e50f50b2fa87ccbbc4c2bfc62a6857ddd455f"
PHASE = "v648-gmut-thos-v5-x1-x2"
PHASE_SLUG = "v648-v5"
OWNER = "Sable Rook"
PRONOUNS = "they/them"
ROLE = "evidence-and-reproducibility steward"
HOPE = "keep every surviving claim easy to challenge or retract"
BRANCH = "codex/GHC-Family/sable-rook-full-tools"
PRIMARY_FOCUS = "GMUT Mind"
BOUNDED_PRACTICE = (
    "newsroom correction, source-status, accessible amendment, workload, and editorial "
    "handover as a learning and synthetic-design lens only"
)
OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]
SOURCE_STATUS_CLASSES = ["current", "stable", "draft", "watch"]
INHERITED_NEGATIVES = 4299
INHERITED_OPEN_GAPS = 30
INHERITED_EXACT_GATES = 31
PREREGISTERED_SYNTHETIC_NEGATIVES = 70


PROPOSALS = [
    {
        "proposal_id": "V6485-P01",
        "title": "W3C PROV bundle, entity-activity-agent, qualified-derivation, specialization, alternate, invalidation, source-independence, duplicate-credit, and replay tribunal",
        "pillar": "THOS Body",
        "hypothesis": "A bounded PROV fixture can distinguish derivation, specialization, alternates, and invalidation while refusing duplicate completion credit across dependent bundles.",
        "null_or_failure_condition": "The tribunal accepts an orphan reference, dependency cycle, invalidated entity as current, alternate as identity, specialization as replacement, or dependent bundles as independent sources.",
        "approval_class": "safe_now_owner_scoped_provenance_fixture",
        "execution_lane": "x2_build_task",
        "source_needs": ["SRC-W3C-PROV-DM", "SRC-W3C-PROV-CONSTRAINTS"],
        "artifacts": ["provenance/prov-bundle-contract.json", "provenance/prov-bundle-mutations.json"],
        "falsifier_or_acceptance_gate": "Every accepted edge resolves inside an identified bundle, invalidation is time-ordered, dependent sources receive no independence credit, and duplicate completion credit is rejected.",
        "rollback_or_recovery": "Withdraw the derived view, preserve the orphan or cycle as a negative, and retain the exact source bundles unchanged.",
        "protected_gates": ["source_independence", "identity_records", "historical_evidence", "completion_credit", "independent_reproduction"],
        "expected_disposition": "completed",
    },
    {
        "proposal_id": "V6485-P02",
        "title": "GMUT LSZ asymptotic-field, pole, residue, amputation, wavefunction-renormalization, mass-gap, infrared, gauge, EFT, unit, and observation-firewall obligation board",
        "pillar": "GMUT Mind",
        "hypothesis": "A typed LSZ obligation board can separate scattering-amplitude reduction assumptions from empirical GMUT evidence.",
        "null_or_failure_condition": "The board omits asymptotic-state, pole-residue, amputation, normalization, mass-gap or infrared, gauge, EFT, unit, or observation boundaries, or converts a formal reduction into observed physics.",
        "approval_class": "safe_now_symbolic_research_only",
        "execution_lane": "x2_build_task",
        "source_needs": ["SRC-LSZ-PRIMARY"],
        "artifacts": ["gmut/lsz-obligations.json", "gmut/lsz-mutations.json"],
        "falsifier_or_acceptance_gate": "Every accepted row names the interpolating field, asymptotic and pole assumptions, residue, amputation, infrared and gauge scope, EFT truncation, units, and a false empirical-confirmation flag.",
        "rollback_or_recovery": "Withdraw the formal adapter, retain the missing obligation as a negative, and make no scattering or physical claim.",
        "protected_gates": ["empirical_confirmation", "physical_prediction", "quantum_completion", "theory_of_everything"],
        "expected_disposition": "completed",
    },
    {
        "proposal_id": "V6485-P03",
        "title": "GMUT Chandra Source Catalog 2.1 release-view, master-source, stack, detection, sensitivity, calibration, variability, selection, covariance, checksum, and zero-row likelihood-refusal adapter",
        "pillar": "GMUT Mind",
        "hypothesis": "An official-format Chandra catalog contract can expose release-view and analysis prerequisites without treating catalog availability as a GMUT likelihood.",
        "null_or_failure_condition": "No real release-view rows, frozen selection, calibration treatment, sensitivity model, covariance, preregistered likelihood, or independent review is present.",
        "approval_class": "real_data_and_independent_review_required",
        "execution_lane": "x2_open_gap",
        "source_needs": ["SRC-CHANDRA-CSC21", "SRC-CHANDRA-RELEASE-VIEWS"],
        "artifacts": ["empirical/chandra-csc21-study-contract.json", "empirical/chandra-csc21-zero-row-receipt.json"],
        "falsifier_or_acceptance_gate": "Remain open_gap while zero real rows and likelihood evaluations exist and release state, calibration, systematics, covariance, falsifiers, and independent review are absent.",
        "rollback_or_recovery": "Retain the zero-row refusal and make no fit, source, force, prediction, parameter, posterior, or confirmation claim.",
        "protected_gates": ["real_data", "empirical_likelihood", "independent_review", "physical_prediction"],
        "expected_disposition": "open_gap",
    },
    {
        "proposal_id": "V6485-P04",
        "title": "THOS newsroom source-status, embargo, correction, retraction, headline, alternative-format, conflict-disclosure, late-arrival, workload, and editorial-handover proxy",
        "pillar": "THOS Body",
        "hypothesis": "A synthetic newsroom event ledger can represent source status, correction, retraction, accessibility, conflicts, late arrivals, workload, and handover without real publication or journalists.",
        "null_or_failure_condition": "The proxy omits source status, version lineage, correction prominence, retraction state, headline linkage, accessible alternative, conflict disclosure, late-arrival replay, owner, or workload boundary.",
        "approval_class": "safe_now_proxy_protocol_no_people_or_publication",
        "execution_lane": "x2_proxy_protocol",
        "source_needs": ["SRC-NZ-MEDIA-COUNCIL", "SRC-WCAG22"],
        "artifacts": ["thos/newsroom-handover-contract.json", "thos/newsroom-handover-vectors.json"],
        "falsifier_or_acceptance_gate": "Represented only when synthetic vectors preserve event lineage and every real journalist, source, publication, audience, complaint, and effectiveness claim remains false.",
        "rollback_or_recovery": "Revert to a design-only checklist, preserve the failed vector, and publish no real story or correction.",
        "protected_gates": ["real_operations", "professional_authority", "source_confidentiality", "participant_effectiveness"],
        "expected_disposition": "represented",
    },
    {
        "proposal_id": "V6485-P05",
        "title": "Freed ID OAuth authorization-server issuer-identification, mix-up, redirect, state, discovery, JARM-interaction, downgrade, replay, metadata, and privacy profile",
        "pillar": "Freed ID / CBR Heart",
        "hypothesis": "Synthetic RFC 9207 vectors can test issuer-parameter validation and mix-up refusal without production identity operations.",
        "null_or_failure_condition": "The profile accepts a missing or mismatched issuer, unbound redirect or state, discovery conflict, downgrade, replay, or treats issuer identification as authentication or universal trust.",
        "approval_class": "safe_now_synthetic_nonproduction",
        "execution_lane": "x2_proxy_protocol",
        "source_needs": ["SRC-RFC9207", "SRC-OAUTH21-DRAFT"],
        "artifacts": ["freed-id/oauth-issuer-id-profile.json", "freed-id/oauth-issuer-id-mutations.json"],
        "falsifier_or_acceptance_gate": "Represented only; synthetic messages, absent real keys and servers, absent interoperability, absent privacy review, and absent trust governance remain explicit.",
        "rollback_or_recovery": "Reject the fixture, retain the negative, and leave production authentication, issuer, and trust decisions unmade.",
        "protected_gates": ["real_keys", "production_identity", "interoperability", "privacy_review", "trust_governance"],
        "expected_disposition": "represented",
    },
    {
        "proposal_id": "V6485-P06",
        "title": "CBR corrections-desk contested-fact, confidential-source, archival-amendment, reply, complainant-privacy, public-interest, remedy, legal-limit, affected-party, cultural, and Māori-authority matrix",
        "pillar": "Freed ID / CBR Heart",
        "hypothesis": "A reservation matrix can expose newsroom remedy and authority dependencies without substituting repository authors for affected people, editors, publishers, or competent authorities.",
        "null_or_failure_condition": "Any real publication, source disclosure, privacy, access, correction, reply, remedy, legal, cultural, or Māori-authority decision is marked completed by software evidence.",
        "approval_class": "authorized_affected_parties_and_competent_authority_required",
        "execution_lane": "x2_exact_gate",
        "source_needs": ["SRC-NZ-MEDIA-COUNCIL", "SRC-NZ-PRIVACY", "SRC-TE-MANA-RARAUNGA", "SRC-WCAG22"],
        "artifacts": ["cbr/newsroom-remedy-matrix.json", "cbr/newsroom-authority-reservation.json"],
        "falsifier_or_acceptance_gate": "Remain exact_gate until affected parties, confidential sources, editors, publishers, tangata whenua, iwi, hapū, Māori authorities, and competent legal, cultural, disability, privacy, and media authorities decide within scope.",
        "rollback_or_recovery": "Remove any accidental authority claim, retain the assumption failure, and preserve source, complainant, and beneficiary privacy.",
        "protected_gates": ["affected_party_legitimacy", "maori_authority", "legal_interpretation", "cultural_ratification", "editorial_authority"],
        "expected_disposition": "exact_gate",
    },
    {
        "proposal_id": "V6485-P07",
        "title": "MIME multipart boundary, nesting, header, transfer-encoding, content-type, filename, external-body, truncation, part-count, byte-budget, and refusal tribunal",
        "pillar": "THOS Body",
        "hypothesis": "A bounded MIME multipart tribunal can reject ambiguous boundaries, unsafe nesting, malformed encodings, external retrieval, filename abuse, truncation, and resource exhaustion in synthetic messages.",
        "null_or_failure_condition": "The tribunal accepts a missing or colliding boundary, malformed header or transfer encoding, unsafe filename, external-body retrieval, truncated closure, or unbounded part and byte expansion.",
        "approval_class": "safe_now_owner_scoped_parser_fixture",
        "execution_lane": "x2_build_task",
        "source_needs": ["SRC-RFC2045", "SRC-RFC2046"],
        "artifacts": ["formats/mime-multipart-contract.json", "formats/mime-multipart-mutations.json"],
        "falsifier_or_acceptance_gate": "All declared malformed fixtures are rejected, external retrieval is disabled, depth and byte budgets are enforced, and no exhaustive-security claim is made.",
        "rollback_or_recovery": "Disable the wrapper, retain the failing fixture, and fall back to inert byte-preserving display.",
        "protected_gates": ["external_payloads", "network_retrieval", "exhaustive_security", "production_parser"],
        "expected_disposition": "completed",
    },
    {
        "proposal_id": "V6485-P08",
        "title": "Accessible timeline chronology, date-time, heading, current-marker, correction-link, non-colour cue, keyboard order, alternative table, print, and manual-evaluation reservation audit",
        "pillar": "THOS Body",
        "hypothesis": "A structural audit can verify a chronological timeline and equivalent tabular fallback while reserving all manual and affected-user evaluation.",
        "null_or_failure_condition": "The timeline lacks machine-readable dates, ordered chronology, current and corrected-item cues, heading structure, keyboard order, equivalent table, print fallback, or honest reservation.",
        "approval_class": "safe_now_structural_only",
        "execution_lane": "x2_build_task",
        "source_needs": ["SRC-WCAG22", "SRC-WHATWG-TIME"],
        "artifacts": ["accessibility/timeline-contract.json", "accessibility/timeline-mutations.json"],
        "falsifier_or_acceptance_gate": "Pass only structural fixtures; reserve browser, keyboard, responsive, assistive-technology, cognitive, Māori-language, security-usability, and affected-user evaluation.",
        "rollback_or_recovery": "Publish an inert sequential table fallback and retain every structural failure.",
        "protected_gates": ["complete_accessibility", "manual_evaluation", "affected_user_acceptance", "language_authority"],
        "expected_disposition": "completed",
    },
    {
        "proposal_id": "V6485-P09",
        "title": "Thermo-Psyche Carathéodory adiabatic-inaccessibility, Pfaffian-form, integrating-factor, local-equilibrium, state-space, domain, and choice-agency nonconversion classifier",
        "pillar": "Trinity Mandala bridge",
        "hypothesis": "A typed classifier can preserve Carathéodory thermodynamic assumptions while refusing conversion of adiabatic accessibility into psychological choice, freedom, agency, worth, or consciousness.",
        "null_or_failure_condition": "A local equilibrium or Pfaffian statement is applied outside its state-space assumptions or used as a measure of human choice, agency, value, or mind.",
        "approval_class": "safe_now_formal_domain_guard",
        "execution_lane": "x2_build_task",
        "source_needs": ["SRC-CARATHEODORY"],
        "artifacts": ["thermo-psyche/caratheodory-contract.json", "thermo-psyche/caratheodory-mutations.json"],
        "falsifier_or_acceptance_gate": "Every accepted row states state space, equilibrium, Pfaffian form, local inaccessibility, integrating-factor scope, units, and domain; all psyche conversions are rejected.",
        "rollback_or_recovery": "Remove the analogy, retain only the physical or mathematical statement, and preserve the rejected conversion.",
        "protected_gates": ["psyche_conversion", "consciousness", "personhood", "moral_value"],
        "expected_disposition": "completed",
    },
    {
        "proposal_id": "V6485-P10",
        "title": "Stage 20 differential-outcome-misclassification sensitivity, validation-substudy, sensitivity-specificity, dependence, matrix-invertibility, subgroup, uncertainty, and nonpromotion board",
        "pillar": "Trinity Mandala bridge",
        "hypothesis": "A misclassification board can expose sensitivity-analysis obligations without converting zero-participant fixtures into corrected outcomes or causal evidence.",
        "null_or_failure_condition": "Validation data, sensitivity and specificity uncertainty, dependence, matrix invertibility, subgroup variation, systematic and random error, or value authority is omitted or software is promoted as an effect.",
        "approval_class": "safe_now_structural_nonpromotion",
        "execution_lane": "x2_build_task",
        "source_needs": ["SRC-MISCLASSIFICATION-PSA"],
        "artifacts": ["stage20/misclassification-contract.json", "stage20/misclassification-mutations.json"],
        "falsifier_or_acceptance_gate": "Pass only structural protocol fixtures; real outcomes, validation-substudy evidence, credible error parameters, safety monitoring, value authority, and independent review remain absent.",
        "rollback_or_recovery": "Retain the failed fixture and keep corrected-effect, causal-effect, and Stage 20 claims false.",
        "protected_gates": ["real_participants", "corrected_effect", "value_authority", "independent_review", "stage20"],
        "expected_disposition": "completed",
    },
]


SOURCES = [
    {"source_id": "SRC-LIVE-REQUEST", "title": "Hamish current v648-v5 activation and committed Ilyra baton", "url": None, "status": "current", "kind": "live_authority", "implication": "Controls solo ownership, no replay, x1-before-x2, four-commit cap, platform exclusions, privacy, and terminal route."},
    {"source_id": "SRC-W3C-PROV-DM", "title": "W3C PROV Data Model", "url": "https://www.w3.org/TR/prov-dm/", "status": "stable", "kind": "official_standard", "implication": "Defines entities, activities, agents, derivation, invalidation, specialization, alternates, and bundles; it does not prove source independence."},
    {"source_id": "SRC-W3C-PROV-CONSTRAINTS", "title": "W3C Constraints of the PROV Data Model", "url": "https://www.w3.org/TR/prov-constraints/", "status": "stable", "kind": "official_standard", "implication": "Supplies validity and ordering constraints for bounded provenance fixtures, not real-world completeness."},
    {"source_id": "SRC-LSZ-PRIMARY", "title": "Lehmann, Symanzik, and Zimmermann, On the formulation of quantized field theories", "url": "https://doi.org/10.1007/BF02731765", "status": "stable", "kind": "primary_research", "implication": "LSZ reduction has explicit asymptotic, pole, normalization, and field-theory assumptions and is not an empirical GMUT result."},
    {"source_id": "SRC-CHANDRA-CSC21", "title": "Chandra Source Catalog Release 2.1", "url": "https://cxc.harvard.edu/csc2.0/about2.1.html", "status": "current", "kind": "official_data", "implication": "Release 2.1 and its processing states expose a candidate official data surface but supply no GMUT likelihood."},
    {"source_id": "SRC-CHANDRA-RELEASE-VIEWS", "title": "Chandra Source Catalog release and current database views", "url": "https://cxc.harvard.edu/csc1/releases_dbaccess.html", "status": "current", "kind": "official_data", "implication": "Static release views and mutable current views have different statistical and provenance properties that must not be flattened."},
    {"source_id": "SRC-NZ-MEDIA-COUNCIL", "title": "New Zealand Media Council Principles", "url": "https://www.mediacouncil.org.nz/principles/", "status": "current", "kind": "primary_authority_source", "implication": "Accuracy, fairness, privacy, confidentiality, conflicts, and corrections are professional and affected-party obligations, not software authority."},
    {"source_id": "SRC-RFC9207", "title": "RFC 9207 OAuth 2.0 Authorization Server Issuer Identification", "url": "https://www.rfc-editor.org/rfc/rfc9207.html", "status": "stable", "kind": "official_standard", "implication": "The iss response parameter counters mix-up attacks but does not authenticate people or establish universal trust."},
    {"source_id": "SRC-OAUTH21-DRAFT", "title": "IETF OAuth 2.1 Authorization Framework draft", "url": "https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/", "status": "draft", "kind": "official_draft", "implication": "The active draft remains work in progress and is monitored without being treated as settled normative authority."},
    {"source_id": "SRC-RFC2045", "title": "RFC 2045 MIME Part One", "url": "https://www.rfc-editor.org/rfc/rfc2045.html", "status": "stable", "kind": "official_standard", "implication": "MIME headers and transfer encodings require bounded, fail-closed parsing."},
    {"source_id": "SRC-RFC2046", "title": "RFC 2046 MIME Part Two", "url": "https://www.rfc-editor.org/rfc/rfc2046.html", "status": "stable", "kind": "official_standard", "implication": "Multipart boundaries and nesting rules support a synthetic parser tribunal, not exhaustive security."},
    {"source_id": "SRC-WCAG22", "title": "Web Content Accessibility Guidelines 2.2", "url": "https://www.w3.org/TR/WCAG22/", "status": "stable", "kind": "official_standard", "implication": "Structural checks cover only declared markup obligations and cannot close manual or affected-user evaluation."},
    {"source_id": "SRC-WHATWG-TIME", "title": "WHATWG HTML time element", "url": "https://html.spec.whatwg.org/multipage/text-level-semantics.html#the-time-element", "status": "current", "kind": "official_standard", "implication": "Machine-readable date and time semantics support a structural timeline contract only."},
    {"source_id": "SRC-CARATHEODORY", "title": "Carathéodory, Untersuchungen über die Grundlagen der Thermodynamik", "url": "https://doi.org/10.1007/BF01450409", "status": "stable", "kind": "primary_research", "implication": "Adiabatic inaccessibility and Pfaffian integrability are thermodynamic-domain statements, not measures of choice or agency."},
    {"source_id": "SRC-MISCLASSIFICATION-PSA", "title": "Fox, Lash, and Greenland, probabilistic sensitivity analysis of misclassified binary variables", "url": "https://doi.org/10.1093/ije/dyi184", "status": "stable", "kind": "primary_method", "implication": "Misclassification sensitivity analysis requires declared error parameters and uncertainty; a software board is not corrected evidence."},
    {"source_id": "SRC-NZ-PRIVACY", "title": "New Zealand Privacy Commissioner privacy guidance", "url": "https://www.privacy.org.nz/responsibilities/your-obligations/", "status": "current", "kind": "official_authority", "implication": "Real privacy, harm, correction, and remedy decisions require competent human authority and affected-person consideration."},
    {"source_id": "SRC-TE-MANA-RARAUNGA", "title": "Te Mana Raraunga principles of Māori data sovereignty", "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "status": "stable", "kind": "primary_authority_source", "implication": "Māori data and concepts remain under Māori governance; software confers no Māori authority."},
    {"source_id": "SRC-OPENAI-CODEX", "title": "OpenAI Codex official repository and package channel", "url": "https://github.com/openai/codex", "status": "watch", "kind": "official_package", "implication": "CLI version status may be observed, but this phase performs no application update."},
    {"source_id": "SRC-OPENAI-CODEX-APP", "title": "OpenAI Codex app announcement", "url": "https://openai.com/index/introducing-the-codex-app/", "status": "current", "kind": "official_product", "implication": "Confirms the Windows app surface; the installed desktop build is verified locally and not updated."},
]


SAFE_TASKS = [
    "Verify inherited source, x1, evidence, parent-count, zero-merge, clean, and live-remote anchors",
    "Record the external V6484-POST-N05 carry-forward without rewriting Ilyra's sealed count",
    "Record D-first capacity and owner-lane continuity without cleanup",
    "Audit all 600 frozen proposal titles and semantics with readable collision reasons",
    "Build the four-state official and primary source ledger without status flattening",
    "Freeze exactly ten core proposals without x2 outcomes or completion claims",
    "Build the x1-to-x2 immutable Git-blob separation receipt",
    "Build an exact staged-path allowlist for owner-generated files",
    "Build five-class privacy scanning with candidate versus confirmed-hit separation",
    "Record every startup timeout, no-match, encoding fault, and failed recovery before retry",
    "Build and validate Method Flow fail and pass witness parity",
    "Refresh the phase-scoped GHC Family Index without global skill churn",
    "Run Reflection-Remaster as a read-only additive audit and record reviewed-current disposition",
    "Build the W3C PROV source-independence fixture plan",
    "Build the LSZ formal-obligation fixture plan",
    "Build the Chandra CSC 2.1 zero-row study contract",
    "Build the newsroom correction and editorial-handover proxy plan",
    "Build the OAuth issuer-identification synthetic profile plan",
    "Build the newsroom CBR authority-reservation plan",
    "Build the MIME multipart refusal tribunal plan",
    "Build the accessible timeline structural audit plan",
    "Build the Carathéodory domain nonconversion plan",
    "Build the outcome-misclassification nonpromotion board plan",
    "Freeze seventy rejecting synthetic mutations without execution credit",
    "Audit family-current callers and preserve historical compatibility surfaces",
    "Pin UTF-8 for every Unicode-emitting phase command and receipt",
    "Build single-pass consumption, document-cap, and baton word-count guards",
    "Build workload, wellbeing, host-change, and owner-file-threshold receipts",
    "Build stale-label, count-mirror, outcome-vocabulary, and noncompensation lints",
    "Hold terminal routing at PREPARED_NOT_SENT until exact final proof and acknowledgement",
]


CANDIDATE_TASKS = [
    "W3C PROV bundle independence and duplicate-credit fixture",
    "LSZ formal-obligation classifier",
    "Chandra CSC 2.1 zero-row adapter",
    "Newsroom correction and editorial-handover proxy",
    "OAuth authorization-server issuer-identification profile",
    "Newsroom remedy and authority reservation matrix",
    "MIME multipart boundary and expansion-budget refusal engine",
    "Accessible timeline and alternative-table structural auditor",
    "Carathéodory thermodynamic-domain classifier",
    "Outcome-misclassification nonpromotion board",
    "Exact 600-proposal semantic-neighbour diagnostic",
    "Read-only Reflection-Remaster reviewed-current adjudicator",
    "External post-seal negative reconciliation wrapper",
    "Git-blob owner-manifest fixed-point builder",
    "X1 immutable-tree outcome-absence checker",
    "Four-state source drift and watch ledger",
    "Five-class privacy candidate adjudicator with exact exceptions",
    "Method Flow pre-retry record and recurrence crosslinker",
    "Single-pass budget consumption and result-receipt sealer",
    "Exact terminal file-baton length and route-hold recorder",
]


SKILL_IDEAS = [
    "ghc-family-prov-bundle-independence",
    "ghc-family-lsz-obligation-board",
    "ghc-family-chandra-csc21-zero-row",
    "ghc-family-newsroom-correction-handover",
    "ghc-family-oauth-issuer-id-profile",
    "ghc-family-newsroom-authority-reservation",
    "ghc-family-mime-multipart-tribunal",
    "ghc-family-accessible-timeline-audit",
    "ghc-family-caratheodory-domain-guard",
    "ghc-family-misclassification-nonpromotion",
    "ghc-family-six-hundred-proposal-neighbour-audit",
    "ghc-family-reflection-remaster-reviewed-current",
    "ghc-family-external-negative-carry-forward-v2",
    "ghc-family-single-pass-consumption-guard-v4",
    "ghc-family-final-receipt-fixed-point-v2",
    "ghc-family-source-drift-four-state-v3",
    "ghc-family-git-blob-surface-parity-v3",
    "ghc-family-method-flow-pretry-record",
    "ghc-family-private-path-boundary-v2",
    "ghc-family-terminal-file-baton-guard-v2",
]


RUNNER_IDEAS = [
    "ghc_family_prov_bundle_independence.py",
    "ghc_family_lsz_obligations.py",
    "ghc_family_chandra_csc21_zero_row.py",
    "ghc_family_newsroom_correction_handover.py",
    "ghc_family_oauth_issuer_id_profile.py",
    "ghc_family_newsroom_authority.py",
    "ghc_family_mime_multipart_tribunal.py",
    "ghc_family_accessible_timeline.py",
    "ghc_family_caratheodory_domain.py",
    "ghc_family_misclassification_board.py",
]


CLEANUP_TASKS = [
    "Preserve all 4299 inherited and external activation negatives",
    "Recompute every count mirror only from its authoritative ledger",
    "Keep x1 paths immutable after the frozen commit",
    "Use explicit Git-blob, Git-index, clean-filter, and checkout-byte hash domains",
    "Keep staged allowlists exact and owner-scoped",
    "Classify scanner definitions separately from confirmed payload hits",
    "Preserve every unresolved privacy candidate until exact review",
    "Normalize all new generated text to UTF-8 and LF",
    "Check generated JSON ordering and complete parseability",
    "Check every proposal field, artifact, rollback, source, and protected gate is nonempty",
    "Check only the four allowed core outcome labels appear",
    "Check every source status is current, stable, draft, or watch",
    "Check citations receive no observation or authority credit",
    "Check the Chandra adapter ingests zero real rows and evaluates zero likelihoods",
    "Check the THOS proxy contains zero real people, sources, publications, or complaints",
    "Check Freed ID uses zero real keys, servers, accounts, tokens, or network exchanges",
    "Check CBR makes zero real editorial, remedy, legal, cultural, or authority decisions",
    "Check Māori wording, concepts, data governance, and authority remain exact-gated",
    "Check accessibility remains structural with manual and affected-user evaluation reserved",
    "Check no Sandbox, Hyper-V, elevation, feature change, security weakening, or reboot occurs",
    "Check no cross-platform sibling message or standby contact occurs",
    "Check no raw task or thread identifier enters public artifacts",
    "Check no private absolute path, app state, or conversation enters public artifacts",
    "Check no credential, private key, token, API key, or private callable enters public artifacts",
    "Check no AGI, ASI, consciousness, personhood, employment, or qualification claim appears",
    "Check no empirical confirmation, physical prediction, or Theory-of-Everything claim appears",
    "Check no replay, external audit, or independent-reproduction credit appears",
    "Check every document remains at or below 6000 words and the successor baton reaches 4000 words",
    "Check owner-generated growth remains below 15000 files",
    "Keep the terminal route held until the exact final head is clean, pushed, four-way equal, and acknowledged",
]


X1_OPERATIONAL_NEGATIVES = [
    {
        "negative_id": "V6485-X1-N01",
        "failure": "The exact-current memory registry lookup returned the search tool's no-match exit and supplied no continuity evidence.",
        "recovery": "Use the live activation and exact committed baton as authority, record the absent memory hit, and do not infer continuity from silence.",
    },
    {
        "negative_id": "V6485-X1-N02",
        "failure": "The first all-in-one Sable worktree probe exceeded its bounded startup window before returning evidence.",
        "recovery": "Split anchors, tracked diffs, and untracked-file checks into independent read-only Git probes.",
    },
    {
        "negative_id": "V6485-X1-N03",
        "failure": "The first Unicode-bearing proposal summary used the legacy PowerShell output encoding and rendered Māori text as mojibake.",
        "recovery": "Pin console and Python output to UTF-8 before every Unicode-emitting diagnostic while leaving the Git blob unchanged.",
    },
    {
        "negative_id": "V6485-X1-N04",
        "failure": "The first skill-name collision audit launched twenty independent whole-repository searches and timed out without evidence.",
        "recovery": "Replace repeated content searches with one indexed-path-domain collision audit.",
    },
    {
        "negative_id": "V6485-X1-N05",
        "failure": "The first alternation recovery still traversed every document body and exceeded its bound without evidence.",
        "recovery": "Use Git's indexed path list and adjudicate only matching filenames; do not scan historical document bodies for exact package-name collisions.",
    },
    {
        "negative_id": "V6485-X1-N06",
        "failure": "The initial mechanical scaffold copy placed x2-only placeholder builders and tests in the worktree before the x1 freeze.",
        "recovery": "Remove only the exact owner-created untracked placeholders before x1 staging and recreate them after the x1 commit is clean, pushed, and remote-equal.",
    },
]
