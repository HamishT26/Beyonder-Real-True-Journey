#!/usr/bin/env python3
"""Frozen Sylven Arc v649-v6 x1 proposal, source, portfolio, and negative data."""

from __future__ import annotations


SOURCE_COMMIT = "295aa503d3c336273f541504a83b88783563ad90"
SOURCE_PHASE_SOURCE = "9ca33a5762fd9f9d7c26b3d7fd1172d9ed440952"
SOURCE_X1_COMMIT = "e4d241300fd23ca09dc1889d7e84bc494a96f387"
SOURCE_EVIDENCE_COMMIT = "63f679b002e3f17df465a11c30632e769215ff7c"
SOURCE_BRANCH = "codex/GHC-Family/tamar-vey-full-tools"
PHASE = "v649-gmut-thos-v6-x1-x2"
PHASE_SLUG = "v649-v6"
OWNER = "Sylven Arc"
PRONOUNS = "they/them"
ROLE = "relational constraint-cartographer and falsifier-keeper"
HOPE = "keep uncertainty visible, failures recoverable, and bounded evidence from becoming authority"
BRANCH = "codex/GHC-Family/sylven-arc-v642-v8-full-tools"
PRIMARY_FOCUS = "GMUT Mind"
BOUNDED_PRACTICE = (
    "railway rolling-stock wheelset inspection, measurement traceability, defect quarantine, "
    "release refusal, workload budgeting, and shift handover as a learning and synthetic-design lens only"
)
OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]
SOURCE_STATUS_CLASSES = ["current", "stable", "draft", "watch"]
INHERITED_NEGATIVES = 5109
INHERITED_OPEN_GAPS = 39
INHERITED_EXACT_GATES = 40


def proposal(pid, title, pillar, hypothesis, failure, approval, lane, sources, artifacts, gate, rollback, protected, expected):
    return {
        "proposal_id": pid,
        "title": title,
        "pillar": pillar,
        "hypothesis": hypothesis,
        "null_or_failure_condition": failure,
        "approval_class": approval,
        "execution_lane": lane,
        "source_needs": sources,
        "artifacts": artifacts,
        "falsifier_or_acceptance_gate": gate,
        "rollback_or_recovery": rollback,
        "protected_gates": protected,
        "expected_disposition": expected,
    }


PROPOSALS = [
    proposal(
        "V6496-P01",
        "Method Flow epoch-based reclamation, quiescent-state, grace-period, stalled-reader, ABA, reclamation-order, teardown, and evidence-credit tribunal",
        "THOS Body",
        "A bounded epoch-reclamation tribunal can preserve pinning, epoch advance, quiescence, deferred destruction, stalled-reader refusal, ABA separation, teardown, and single evidence credit.",
        "It reclaims while a reader is pinned, advances without quiescence, ignores a stalled reader, reuses an ABA-sensitive token, double-destroys, leaks teardown state, or credits a replay as independent evidence.",
        "safe_now_owner_scoped_protocol_fixture", "x2_build_task", ["SRC-CROSSBEAM-EPOCH"],
        ["method-flow/epoch-reclamation-contract.json", "method-flow/epoch-reclamation-mutations.json"],
        "All synthetic schedules preserve pin, epoch, grace-period, deferred-reclaim, stalled-reader, ABA, teardown, and no-duplicate-credit obligations.",
        "Disable reclamation, retain the schedule, and fall back to bounded ownership without independent-evidence credit.",
        ["memory_safety", "production_concurrency", "independent_reproduction", "evidence_credit"], "completed"),
    proposal(
        "V6496-P02",
        "GMUT Elitzur local-gauge-symmetry, gauge-variant-order-parameter, orbit-average, finite-volume, gauge-fixing, domain, EFT, unit, and observation-firewall obligation board",
        "GMUT Mind",
        "A typed board can state Elitzur-theorem obligations while separating gauge-redundancy and formal lattice assumptions from empirical GMUT evidence.",
        "It omits local symmetry, gauge-variant observable, orbit averaging, finite-volume or limiting assumptions, gauge fixing, mathematical domain, EFT scope, units, or converts theorem structure into observed physics.",
        "safe_now_symbolic_research_only", "x2_build_task", ["SRC-ELITZUR-PRIMARY"],
        ["gmut/elitzur-obligations.json", "gmut/elitzur-mutations.json"],
        "Every accepted row states the theorem domain, gauge-variant quantity, averaging assumptions, gauge-fixing boundary, EFT scope, units, and observation firewall.",
        "Withdraw the row, retain the missing obligation, and make no physical, likelihood, constraint, confirmation, quantum-completion, or Theory-of-Everything claim.",
        ["real_data", "physical_prediction", "empirical_confirmation", "quantum_completion", "theory_of_everything"], "completed"),
    proposal(
        "V6496-P03",
        "GMUT XMM-Newton RGS pipeline-spectrum, response-matrix, background, spectral-order, wavelength, calibration, good-time, selection, covariance, checksum, and zero-row likelihood-refusal adapter",
        "GMUT Mind",
        "An official-product contract can expose RGS spectrum, response, background, order, calibration, screening, selection, covariance, and likelihood prerequisites without calling archive readiness a fit.",
        "No frozen query, downloaded spectrum, response matrix, background, row, calibrated wavelength selection, covariance, checksum, likelihood, posterior, or independent review exists.",
        "real_data_frozen_analysis_and_independent_review_required", "x2_open_gap", ["SRC-XMM-RGS", "SRC-XMM-XSA"],
        ["empirical/xmm-rgs-study-contract.json", "empirical/xmm-rgs-zero-row-receipt.json"],
        "Remain open_gap with zero downloads, real rows, likelihood evaluations, posteriors, constraints, or empirical GMUT claims.",
        "Retain zero-row refusal and do not infer a force, prediction, fit, constraint, confirmation, or Theory of Everything.",
        ["real_data", "likelihood", "independent_review", "empirical_confirmation"], "open_gap"),
    proposal(
        "V6496-P04",
        "THOS railway wheelset inspection, asset-lineage, measurement-traceability, defect-quarantine, instrument-verification, release-refusal, workload-budget, and shift-handover proxy",
        "THOS Body",
        "Synthetic traces can represent wheelset identity, measurement provenance, defect quarantine, instrument status, release refusal, workload ceiling, amendment, and handover without real rolling stock or people.",
        "A trace loses wheelset identity, measurement method, instrument status, defect evidence, quarantine state, release authority reservation, workload ceiling, amendment parent, or receiving owner.",
        "safe_now_proxy_protocol_no_people_or_real_rail_operations", "x2_proxy_protocol", ["SRC-RSSB-WHEELSETS", "SRC-RSSB-WHEELSETS-DRAFT"],
        ["thos/wheelset-inspection-contract.json", "thos/wheelset-inspection-vectors.json"],
        "Represented only when all synthetic lineage checks pass and zero real workers, vehicles, depots, inspections, releases, incidents, blind arms, or effectiveness results remain explicit.",
        "Return to an inert checklist, retain the trace, and issue no real maintenance, stop-use, release, safety, or handover decision.",
        ["real_operations", "professional_authority", "participant_effectiveness", "rail_safety"], "represented"),
    proposal(
        "V6496-P05",
        "Freed ID RFC 9701 JWT token-introspection response media-type, typ, issuer, audience, issued-at, active-state, scope-narrowing, nested-encryption, algorithm-refusal, and minimization profile",
        "Freed ID / CBR Heart",
        "Synthetic RFC 9701 vectors can represent typed introspection JWT validation, audience binding, active-state confinement, scope narrowing, nested encryption, algorithm refusal, and minimization without production identity assurance.",
        "The profile accepts a wrong media type or typ, issuer or audience mismatch, missing issued-at, active-false extra claims, widened scope, invalid nesting, unsafe algorithm, cross-JWT substitution, replay, or excess identity data.",
        "safe_now_synthetic_nonproduction", "x2_proxy_protocol", ["SRC-RFC9701"],
        ["freed-id/jwt-introspection-profile.json", "freed-id/jwt-introspection-mutations.json"],
        "Represented only; real keys, tokens, services, accounts, introspection events, interoperability, privacy review, independent security review, recovery, and trust governance remain absent.",
        "Reject the vector, retain the negative, and make no account, token, key, credential, authorization, or trust decision.",
        ["real_keys", "production_identity", "interoperability", "privacy_review", "independent_security_review", "trust_governance"], "represented"),
    proposal(
        "V6496-P06",
        "CBR railway wheelset quarantine, passenger and maintainer notification, defect-record and location privacy, stop-use release, remedy, affected-party, legal, cultural, land, and Maori-data-governance authority gate",
        "Freed ID / CBR Heart",
        "A reservation matrix can expose rail-safety, notification, privacy, release, remedy, land, affected-party, legal, cultural, and Maori authority dependencies without exercising them.",
        "Software marks any real quarantine, passenger or worker notice, defect disclosure, stop-use or release, remedy, land relationship, legal interpretation, cultural decision, or Maori data-governance decision completed.",
        "authorized_affected_parties_and_competent_authority_required", "x2_exact_gate", ["SRC-RSSB-WHEELSETS", "SRC-NZ-PRIVACY", "SRC-TE-MANA-RARAUNGA"],
        ["cbr/wheelset-risk-gate.json", "cbr/wheelset-authority-reservation.json"],
        "Remain exact_gate until affected people, rail operators and maintainers, land relationships, tangata whenua, iwi, hapu, Maori authorities, and competent safety, privacy, engineering, legal, cultural, remedy, and data-governance authorities decide within scope.",
        "Remove any accidental disclosure or authority claim, retain the failure, and preserve person, asset, location, land, remedy, and cultural privacy.",
        ["affected_party_legitimacy", "professional_authority", "legal_interpretation", "cultural_ratification", "maori_data_governance", "remedy_authority"], "exact_gate"),
    proposal(
        "V6496-P07",
        "WebP RIFF signature, chunk-size, padding, VP8X feature-flag, canvas, animation, metadata, unknown-chunk, truncation, size-arithmetic, resource-budget, and refusal tribunal",
        "THOS Body",
        "A bounded WebP container tribunal can reject malformed synthetic RIFF headers, chunk sizes, padding, flags, canvas arithmetic, animation layout, metadata, truncation, and resource requests without decoding pixels.",
        "It accepts wrong RIFF or WEBP signatures, inconsistent sizes, nonzero padding, reserved flags, invalid canvas or animation ordering, truncated chunks, overflow, trailing data, external retrieval, or unbounded allocation.",
        "safe_now_owner_scoped_parser_fixture", "x2_build_task", ["SRC-RFC9649", "SRC-WEBP-CONTAINER"],
        ["formats/webp-riff-contract.json", "formats/webp-riff-mutations.json"],
        "All malformed fixtures are rejected, arithmetic stays bounded, pixel decoding and external retrieval remain disabled, and no exhaustive-security or production-conformance claim is made.",
        "Disable parsing, retain the fixture, and expose only inert bounded metadata.",
        ["external_payloads", "pixel_decoding", "exhaustive_security", "production_decoder", "user_files"], "completed"),
    proposal(
        "V6496-P08",
        "Accessible sticky-header focus-not-obscured, target-visibility, scroll-offset, focus-appearance, keyboard-sequence, zoom, fallback, print, and manual-reservation audit",
        "THOS Body",
        "A structural audit can expose focus visibility and sticky-overlay obligations while reserving responsive, keyboard, browser, assistive-technology, and affected-user evaluation.",
        "The surface permits author-created content to fully hide focus, lacks target visibility or offset handling, removes visible focus, breaks keyboard sequence, omits fallback or print meaning, or claims complete accessibility.",
        "safe_now_structural_only", "x2_build_task", ["SRC-WCAG-FOCUS", "SRC-WCAG22"],
        ["accessibility/focus-not-obscured-contract.json", "accessibility/focus-not-obscured-mutations.json"],
        "Pass only structural fixtures; keyboard, zoom, responsive layout, browser, assistive-technology, cognitive, Maori-language, and affected-user evaluation remain reserved.",
        "Publish a non-sticky fallback and retain each structural failure.",
        ["complete_accessibility", "manual_evaluation", "affected_user_acceptance", "language_authority"], "completed"),
    proposal(
        "V6496-P09",
        "Thermo-Psyche Tolman-Ehrenfest temperature-redshift, stationary-spacetime, timelike-Killing-field, equilibrium, acceleration, local-temperature, unit, domain, and agency-nonconversion classifier",
        "Trinity Mandala bridge",
        "A typed classifier can preserve Tolman-Ehrenfest equilibrium-temperature obligations and refuse conversion into psyche, worth, agency, consciousness, or personhood.",
        "It drops the stationary spacetime, timelike symmetry, equilibrium, local temperature, redshift relation, acceleration or weak-field limits, units, or converts the physical relation into a law of mind or value.",
        "safe_now_formal_domain_guard", "x2_build_task", ["SRC-TOLMAN-PRIMARY", "SRC-TOLMAN-EHRENFEST"],
        ["thermo-psyche/tolman-ehrenfest-contract.json", "thermo-psyche/tolman-ehrenfest-mutations.json"],
        "Every accepted row states physical variables, spacetime and equilibrium conditions, units, scope, and agency nonconversion.",
        "Remove the analogy, retain the physical statement only, and preserve the rejected conversion.",
        ["psyche_conversion", "consciousness", "personhood", "moral_value", "agency_measure"], "completed"),
    proposal(
        "V6496-P10",
        "Stage 20 Manski partial-identification outcome-bounds, support, missingness, monotone-treatment-response, monotone-selection, sensitivity, uncertainty, falsification, and nonpromotion board",
        "Trinity Mandala bridge",
        "A structural partial-identification board can expose support, bounds, missingness, monotonicity, sensitivity, uncertainty, and falsification obligations without creating participant effects or Stage 20 evidence.",
        "It omits the estimand, outcome support, missingness, bound derivation, monotone-response or selection assumption, uncertainty, sensitivity, falsification, or promotes synthetic software as an effect.",
        "safe_now_structural_nonpromotion", "x2_build_task", ["SRC-MANSKI-MTR", "SRC-MANSKI-MIV"],
        ["stage20/manski-bounds-contract.json", "stage20/manski-bounds-mutations.json"],
        "Pass only structural fixtures; real outcomes, defensible assumptions, participant evidence, safety monitoring, value authority, and independent review remain absent.",
        "Retain the failed fixture and keep causal-effect, participant-effect, deployment, and Stage 20 claims false.",
        ["real_participants", "causal_effect", "value_authority", "independent_review", "stage20"], "completed"),
]


SOURCES = [
    {"source_id":"SRC-LIVE-BATON","title":"Current v649-v6 activation and committed Tamar pointer","url":None,"status":"current","kind":"live_authority","implication":"Controls solo ownership, exact inheritance, x1-before-x2, one successful pass, no replay, privacy, authority, and terminal routing."},
    {"source_id":"SRC-CROSSBEAM-EPOCH","title":"Crossbeam epoch-based memory reclamation documentation","url":"https://docs.rs/crossbeam-epoch/latest/crossbeam_epoch/","status":"current","kind":"official_package_documentation","implication":"Supports bounded pin, epoch, deferred-destruction, and quiescence fixtures only; it is not production concurrency assurance."},
    {"source_id":"SRC-ELITZUR-PRIMARY","title":"Elitzur, Impossibility of spontaneously breaking local symmetries","url":"https://doi.org/10.1103/PhysRevD.12.3978","status":"stable","kind":"primary_research","implication":"Supports formal local-gauge-symmetry obligations only, not empirical GMUT evidence."},
    {"source_id":"SRC-XMM-RGS","title":"XMM-Newton specifications for individual SSC data products","url":"https://xmm-tools.cosmos.esa.int/external/xmm_obs_info/odf/data/docs/XMM-SOC-GEN-ICD-0024.pdf","status":"current","kind":"official_mission_documentation","implication":"Supplies RGS spectrum and response-product requirements; no product is downloaded or analyzed."},
    {"source_id":"SRC-XMM-XSA","title":"ESA XMM-Newton Science Archive","url":"https://www.cosmos.esa.int/web/xmm-newton/xsa","status":"current","kind":"official_archive","implication":"Supplies archive and product provenance context only; zero rows and zero likelihoods remain."},
    {"source_id":"SRC-RSSB-WHEELSETS","title":"RSSB Railway Wheelsets GMRT2466 Issue 5","url":"https://www.rssb.co.uk/standards-catalogue/CatalogueItem/gmrt2466-iss-5","status":"current","kind":"official_industry_standard","implication":"Provides wheelset inspection, recording, and maintenance context; citation confers no rail competence or release authority."},
    {"source_id":"SRC-RSSB-WHEELSETS-DRAFT","title":"RSSB RIS-2766-RST Issue 2 consultation draft","url":"https://consultations.rssb.co.uk/_entity/sharepointdocumentlocation/6e11ebd0-2e4e-ed11-bba3-000d3aba38ae/2ab10dab-d681-4911-b881-cc99413f07b6?file=06.+RIS-2766-RST_Wheelsets+iss+2+draft+3.pdf","status":"draft","kind":"official_consultation_draft","implication":"Offers traceability and maintenance-plan context only and is never flattened into current normative authority."},
    {"source_id":"SRC-RFC9701","title":"RFC 9701 JSON Web Token Response for OAuth Token Introspection","url":"https://www.rfc-editor.org/rfc/rfc9701.html","status":"stable","kind":"official_standard","implication":"Supports synthetic introspection-JWT validation and minimization vectors only."},
    {"source_id":"SRC-RFC9649","title":"RFC 9649 WebP Image Format","url":"https://www.rfc-editor.org/rfc/rfc9649.html","status":"stable","kind":"official_standard","implication":"Supports bounded WebP RIFF container fixtures without pixel decoding or production conformance credit."},
    {"source_id":"SRC-WEBP-CONTAINER","title":"Google WebP Container Specification","url":"https://developers.google.com/speed/webp/docs/riff_container","status":"current","kind":"official_format_documentation","implication":"Supplies chunk order, VP8X, canvas, animation, metadata, and resource-bound requirements only."},
    {"source_id":"SRC-WCAG-FOCUS","title":"W3C Understanding Focus Not Obscured (Minimum)","url":"https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum","status":"current","kind":"official_guidance","implication":"Supports structural focus-visibility obligations while manual and affected-user evaluation stays reserved."},
    {"source_id":"SRC-WCAG22","title":"Web Content Accessibility Guidelines 2.2","url":"https://www.w3.org/TR/WCAG22/","status":"stable","kind":"official_standard","implication":"Structural checks do not establish complete accessibility conformance."},
    {"source_id":"SRC-TOLMAN-PRIMARY","title":"Tolman, On the Weight of Heat and Thermal Equilibrium in General Relativity","url":"https://doi.org/10.1103/PhysRev.35.904","status":"stable","kind":"primary_research","implication":"Supports the physical equilibrium-temperature domain only, not a psyche or agency law."},
    {"source_id":"SRC-TOLMAN-EHRENFEST","title":"Tolman and Ehrenfest, Temperature Equilibrium in a Static Gravitational Field","url":"https://doi.org/10.1103/PhysRev.36.1791","status":"stable","kind":"primary_research","implication":"Supports stationary-field equilibrium obligations only and no observation or human inference."},
    {"source_id":"SRC-MANSKI-MTR","title":"Manski, Monotone Treatment Response","url":"https://doi.org/10.2307/2171748","status":"stable","kind":"primary_method_source","implication":"Supports structural partial-identification assumptions; this phase estimates no participant effect."},
    {"source_id":"SRC-MANSKI-MIV","title":"Manski and Pepper, More on monotone instrumental variables","url":"https://doi.org/10.1111/j.1368-423X.2008.00262.x","status":"stable","kind":"primary_method_source","implication":"Supports nonparametric-bound and finite-sample caution only; no participant data are used."},
    {"source_id":"SRC-NZ-PRIVACY","title":"New Zealand Privacy Commissioner obligations guidance","url":"https://www.privacy.org.nz/responsibilities/your-obligations/","status":"current","kind":"official_authority","implication":"Real privacy, correction, disclosure, and remedy decisions require competent human authority and affected-person consideration."},
    {"source_id":"SRC-TE-MANA-RARAUNGA","title":"Te Mana Raraunga principles of Maori data sovereignty","url":"https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty","status":"stable","kind":"primary_authority_source","implication":"Maori data and concepts remain under Maori governance; software and citation confer no Maori authority."},
    {"source_id":"SRC-CROSSBEAM-WATCH","title":"Crossbeam epoch package latest release surface","url":"https://docs.rs/crate/crossbeam-epoch/latest","status":"watch","kind":"official_package_watch","implication":"Version drift is watched only; no package installation or production use occurs."},
    {"source_id":"SRC-OPENAI-CODEX","title":"OpenAI Codex official release repository","url":"https://github.com/openai/codex/releases","status":"watch","kind":"official_package","implication":"Version status is observed only; no desktop or CLI update occurs."},
]


SAFE_TASKS = [
    "Verify Tamar exact source, x1, evidence, final parent, zero merges, cleanliness, and live equality",
    "Replay Tamar x1, evidence, and final commit-local manifest contracts",
    "Fast-forward Sylven by exact single-parent ancestry only",
    "Prove Sylven pre-x1 four-way remote equality",
    "Audit all 690 frozen proposal titles and substantive neighbors",
    "Retain every rejected semantic seed and tooling fault",
    "Build current, stable, draft, and watch source statuses without flattening",
    "Freeze exactly ten proposals with no x2 outcomes",
    "Freeze 70 linked mutations without executing them",
    "Build x1 path-filtered Git-blob manifest and three self-exclusions",
    "Run five-class x1 privacy scanning",
    "Record failed and passing Method Flow witnesses",
    "Refresh the phase-scoped GHC Family Index",
    "Freeze epoch-reclamation evidence-credit tribunal",
    "Freeze Elitzur obligation board",
    "Freeze XMM RGS zero-row adapter",
    "Freeze wheelset inspection proxy",
    "Freeze RFC 9701 introspection-JWT profile",
    "Freeze wheelset authority gate",
    "Freeze WebP RIFF refusal tribunal",
    "Freeze focus-not-obscured structural audit",
    "Freeze Tolman-Ehrenfest nonconversion classifier",
    "Freeze Manski partial-identification nonpromotion board",
    "Preserve inherited held approval packets",
    "Measure owner growth against the 15000-file threshold",
    "Verify Codex versions without updating software",
    "Record no Sandbox or Hyper-V action",
    "Reserve one successful canonical pass and no post-success replay",
    "Keep Eiren route prepared but unsent until exact final proof",
    "Preserve family-current caller compatibility without deleting historical runners",
]

CANDIDATE_TASKS = [
    "Epoch pin, guard, and deferred-reclaim prototype", "Epoch grace-period, stalled-reader, ABA, and teardown prototype",
    "Elitzur local-symmetry and gauge-variant observable prototype", "Elitzur orbit-average, gauge-fixing, and observation-firewall prototype",
    "XMM RGS spectrum, order, and response prerequisite prototype", "XMM RGS zero-row, covariance, and likelihood-refusal prototype",
    "Wheelset identity, measurement, and instrument-state prototype", "Wheelset defect quarantine, release refusal, and handover prototype",
    "RFC 9701 media-type, typ, issuer, audience, and issued-at prototype", "RFC 9701 active-state, scope, nested-JWT, and minimization prototype",
    "Wheelset notification, privacy, remedy, and authority reservation prototype", "WebP RIFF header, chunk-size, and padding prototype",
    "WebP VP8X, canvas, animation, metadata, and budget prototype", "Sticky-overlay target-visibility prototype",
    "Focus offset, appearance, zoom, fallback, and reservation prototype", "Tolman-Ehrenfest stationary-equilibrium domain prototype",
    "Tolman-Ehrenfest agency-nonconversion prototype", "Manski support, missingness, and bounds prototype",
    "Manski monotonicity, sensitivity, and falsification prototype", "Stage 20 partial-identification nonpromotion prototype",
]

SKILL_IDEAS = [
    "ghc-family-v649-v6-epoch-grace-period", "ghc-family-v649-v6-epoch-stalled-reader",
    "ghc-family-v649-v6-elitzur-obligations", "ghc-family-v649-v6-gmut-observation-firewall",
    "ghc-family-v649-v6-xmm-rgs-zero-row", "ghc-family-v649-v6-wheelset-lineage",
    "ghc-family-v649-v6-wheelset-handover", "ghc-family-v649-v6-jwt-introspection-profile",
    "ghc-family-v649-v6-introspection-minimization", "ghc-family-v649-v6-wheelset-authority-reservation",
    "ghc-family-v649-v6-webp-riff-structure", "ghc-family-v649-v6-webp-resource-budget",
    "ghc-family-v649-v6-focus-not-obscured", "ghc-family-v649-v6-focus-manual-reservation",
    "ghc-family-v649-v6-tolman-domain", "ghc-family-v649-v6-tolman-nonconversion",
    "ghc-family-v649-v6-manski-bounds", "ghc-family-v649-v6-stage20-nonpromotion",
    "ghc-family-v649-v6-method-flow-recovery", "ghc-family-v649-v6-terminal-proof",
]

RUNNER_IDEAS = [
    "ghc_family_v649_v6_epoch_reclamation.py", "ghc_family_v649_v6_elitzur_obligations.py",
    "ghc_family_v649_v6_xmm_rgs_refusal.py", "ghc_family_v649_v6_wheelset_inspection.py",
    "ghc_family_v649_v6_jwt_introspection.py", "ghc_family_v649_v6_webp_tribunal.py",
    "ghc_family_v649_v6_accessibility_audit.py", "ghc_family_v649_v6_domain_guards.py",
    "ghc_family_v649_v6_portfolio.py", "build_ghc_family_v649_v6_closeout.py",
]

CLEANUP_TASKS = [
    "Normalize v649-v6 JSON ordering and UTF-8 output only", "Validate the four outcome labels exactly",
    "Validate current stable draft and watch source labels", "Assert exactly ten proposals",
    "Assert the frozen total is 700", "Assert source x1 evidence and final ancestry",
    "Assert zero phase merges and one final parent", "Guard x1 from x2 implementation and outcomes",
    "Label Git-blob and checkout-byte hash domains", "Label all five privacy classes",
    "Quarantine scanner definitions explicitly", "Enforce the 6000-word document cap",
    "Measure Sylven-owned additions only", "Mark citations as non-observations",
    "Separate same-owner checking from independent reproduction", "Record no Sandbox or Hyper-V action",
    "Record no desktop or CLI update", "Record no cross-platform send",
    "Record zero created tasks and subagents", "Keep terminal routing prepared-not-sent",
    "Reserve complete accessibility evaluation", "Reserve Maori-language and authority evaluation",
    "Record zero real data and likelihood rows", "Record zero participants and rail workers",
    "Record zero production identity operations", "Reject exhaustive-security language",
    "Attach rollback and recovery to every prototype", "Check protected-gate parity",
    "Review exact staged paths", "Require final four-way remote equality",
]

X1_OPERATIONAL_NEGATIVES = [
    {"negative_id":"V6496-X1-N01","category":"powershell_foreach_formatter_parse_fault","failed":"A startup path probe placed a formatter pipe directly after a foreach block and PowerShell rejected the empty pipe element before any child command ran.","recovery":"Emit scalar path results directly without a formatter pipeline.","passing":"The scalar probe confirmed both Tamar and Sylven worktrees without mutation.","recurrence_guard":"Do not pipe directly from a PowerShell foreach statement; assign or emit scalar rows first."},
    {"negative_id":"V6496-X1-N02","category":"manifest_byte_domain_conflation","failed":"The first manifest replay compared working-tree byte receipts with raw Git object sizes and reported false mismatches despite exact object identity.","recovery":"Verify path-filtered Git blob identity separately from checkout-byte receipts.","passing":"All x1, evidence, and final object paths and object identifiers matched their commit-local trees.","recurrence_guard":"Keep raw blob, path-filtered blob, and checkout-byte domains explicit in every manifest replay."},
    {"negative_id":"V6496-X1-N03","category":"mixed_line_ending_filter_replay_mismatch","failed":"A generic smudge-filter reconstruction produced 5688 bytes for one inherited mixed-line-ending file while the sealed working-tree receipt recorded 5669.","recovery":"Use the clean canonical working-tree byte receipt for the nonreconstructable mixed-line-ending domain and require its path-filtered object to equal the commit tree.","passing":"The canonical file was 5669 bytes, clean, and its path-filtered object exactly equaled the recorded and committed object.","recurrence_guard":"Never infer historical mixed checkout bytes solely from a normalized Git blob and current smudge filter."},
    {"negative_id":"V6496-X1-N04","category":"narrow_source_probe_timeout","failed":"A read-only scalar source probe exceeded a ten-second wrapper budget and produced no attributable evidence.","recovery":"Rerun only the scalar checks under a bounded sixty-second envelope.","passing":"The bounded probe returned working bytes, object identities, and clean state.","recurrence_guard":"Use realistic Windows Git wrapper budgets and give timed-out attempts no credit."},
    {"negative_id":"V6496-X1-N05","category":"git_object_path_separator_fault","failed":"A Git object expression used a Windows backslash and rev-parse rejected the path while an unchecked wrapper continued.","recovery":"Use repository-relative forward slashes and check each Git child exit code.","passing":"The corrected object expression returned the exact committed object and clean status.","recurrence_guard":"Normalize Git object paths to forward slashes and fail on every nonzero child exit."},
    {"negative_id":"V6496-X1-N06","category":"expected_no_match_exit_misclassified","failed":"A WebP novelty search returned no matches with ripgrep exit code one and the wrapper misclassified the expected absence as a command failure.","recovery":"Use explicit no-match-aware structured term counts.","passing":"The structured audit returned zero lexical WebP and RIFF-container hits across all 690 predecessors.","recurrence_guard":"Distinguish expected search absence from execution failure before assigning evidence credit."},
    {"negative_id":"V6496-X1-N07","category":"semantic_seed_collisions","failed":"Initial XMM catalogue, OAuth protected-resource metadata, and skip-link proposals collided lexically or substantively with frozen predecessors; several earlier generic seed ideas also matched inherited mechanisms.","recovery":"Withdraw every collision and replace them with RGS product semantics, RFC 9701 introspection JWTs, and Focus Not Obscured without lowering the threshold.","passing":"The revised ten remained below the 0.50 lexical threshold and passed manual substantive-neighbor review against all 690 proposals.","recurrence_guard":"A new dataset, standard number, profession, or label does not establish a distinct mechanism."},
    {"negative_id":"V6496-X1-N08","category":"memory_registry_current_phase_absence","failed":"The memory registry had no exact v649-v5 or v649-v6 current-phase entry.","recovery":"Retain the absence and use the live verified baton, committed pointer, and exact Git proof for current truth.","passing":"No continuity was inferred from memory silence; live authority and repository evidence controlled startup.","recurrence_guard":"Treat absent current memory as absence, never as proof or route authority."},
]
