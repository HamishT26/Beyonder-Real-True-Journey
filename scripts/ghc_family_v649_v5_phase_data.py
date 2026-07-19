#!/usr/bin/env python3
"""Frozen Tamar Vey v649-v5 x1 proposal, source, portfolio, and negative data."""

from __future__ import annotations


SOURCE_COMMIT = "9ca33a5762fd9f9d7c26b3d7fd1172d9ed440952"
SOURCE_PHASE_SOURCE = "e7998c7ee6fb4a5dccc9e3a09a50aecc8a10b956"
SOURCE_X1_COMMIT = "9882fb936e404796cd4aeb847ff41bd3ec28b5d6"
SOURCE_EVIDENCE_COMMIT = "b0eb02b6cef8f03b246db0f12c3f8155e3fd73d0"
SOURCE_BRANCH = "codex/GHC-Family/orin-thale-v642-v6-full-tools"
PHASE = "v649-gmut-thos-v5-x1-x2"
PHASE_SLUG = "v649-v5"
OWNER = "Tamar Vey"
PRONOUNS = "they/them"
ROLE = "relational evidence-systems cartographer and boundary keeper"
HOPE = "keep decisions legible, failures recoverable, and authority boundaries intact"
BRANCH = "codex/GHC-Family/tamar-vey-full-tools"
PRIMARY_FOCUS = "THOS Body"
BOUNDED_PRACTICE = (
    "civil materials-testing laboratory concrete specimen receipt, curing, test-age, "
    "machine verification, result amendment, and shift handover as a learning and synthetic-design lens only"
)
OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]
SOURCE_STATUS_CLASSES = ["current", "stable", "draft", "watch"]
INHERITED_NEGATIVES = 5025
INHERITED_OPEN_GAPS = 38
INHERITED_EXACT_GATES = 39


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
        "V6495-P01",
        "Method Flow HTTP cache-control age, freshness, validator, stale-response, Vary-key, sensitive-response, invalidation, and evidence-credit tribunal",
        "THOS Body",
        "A bounded cache tribunal can preserve cache keys, computed age, freshness, validation, staleness, sensitive-response restrictions, invalidation, and single evidence credit.",
        "It reuses the wrong Vary key, miscomputes age, serves prohibited stale or sensitive content, ignores validation or invalidation, or credits a cached response as new independent evidence.",
        "safe_now_owner_scoped_protocol_fixture", "x2_build_task", ["SRC-RFC9111"],
        ["method-flow/http-cache-contract.json", "method-flow/http-cache-mutations.json"],
        "All synthetic traces preserve key, age, freshness, validation, staleness, privacy, invalidation, and no-duplicate-credit obligations.",
        "Disable caching, retain the trace, and use direct bounded reads without evidence duplication.",
        ["sensitive_data", "production_cache", "independent_reproduction", "evidence_credit"], "completed"),
    proposal(
        "V6495-P02",
        "GMUT Bisognano-Wichmann wedge-algebra, vacuum, modular operator, Lorentz-boost flow, modular conjugation, spectrum, domain, gauge, EFT, unit, and observation-firewall obligation board",
        "GMUT Mind",
        "A typed board can state wedge modular-flow obligations while separating a formal theorem domain from empirical GMUT evidence.",
        "It omits wedge localization, vacuum assumptions, modular objects, boost relation, spectrum, domain, gauge, EFT, units, or converts formal structure into observed physics.",
        "safe_now_symbolic_research_only", "x2_build_task", ["SRC-BW-REVIEW"],
        ["gmut/bisognano-wichmann-obligations.json", "gmut/bisognano-wichmann-mutations.json"],
        "Every accepted row names the theorem domain, modular objects, boost relation, assumptions, units, and observation firewall.",
        "Withdraw the row, retain the missing obligation, and make no physical, likelihood, constraint, confirmation, quantum-completion, or Theory-of-Everything claim.",
        ["real_data", "physical_prediction", "empirical_confirmation", "quantum_completion", "theory_of_everything"], "completed"),
    proposal(
        "V6495-P03",
        "GMUT JWST MAST calibrated-product, association, CRDS-context, WCS, PSF, selection, covariance, checksum, and zero-row likelihood-refusal adapter",
        "GMUT Mind",
        "An official-product contract can expose JWST calibration and likelihood prerequisites without calling archive readiness a fit.",
        "No frozen query, downloaded product, row, calibration context, WCS/PSF model, selection, covariance, checksum, likelihood, posterior, or independent review exists.",
        "real_data_frozen_analysis_and_independent_review_required", "x2_open_gap", ["SRC-MAST-JWST"],
        ["empirical/jwst-mast-study-contract.json", "empirical/jwst-mast-zero-row-receipt.json"],
        "Remain open_gap with zero downloads, real rows, likelihood evaluations, posteriors, constraints, or empirical GMUT claims.",
        "Retain zero-row refusal and do not infer a force, prediction, fit, constraint, confirmation, or Theory of Everything.",
        ["real_data", "likelihood", "independent_review", "empirical_confirmation"], "open_gap"),
    proposal(
        "V6495-P04",
        "THOS civil materials laboratory concrete specimen receipt, identification, curing, test-age, machine-verification, fracture note, amended result, workload budget, and shift-handover proxy",
        "THOS Body",
        "Synthetic traces can represent concrete specimen receipt, identity, curing, test age, machine verification, fracture note, amendment lineage, workload, and handover without real testing or people.",
        "A trace loses specimen identity, curing conditions, test age, machine state, fracture note, amendment parent, workload ceiling, or receiving owner.",
        "safe_now_proxy_protocol_no_people_or_real_testing", "x2_proxy_protocol", ["SRC-IANZ-LABS", "SRC-WCAG22"],
        ["thos/concrete-laboratory-contract.json", "thos/concrete-laboratory-vectors.json"],
        "Represented only when all synthetic lineage checks pass and zero real specimens, workers, sites, tests, safety decisions, blind arms, or effectiveness results remain explicit.",
        "Return to an inert checklist, retain the trace, and issue no real acceptance, rejection, structural-safety, or handover decision.",
        ["real_operations", "professional_authority", "participant_effectiveness", "structural_safety"], "represented"),
    proposal(
        "V6495-P05",
        "Freed ID RFC 9700 refresh-token sender constraint, rotation, replay detection, revocation cascade, inactivity expiry, privilege restriction, downgrade, and minimization profile",
        "Freed ID / CBR Heart",
        "Synthetic RFC 9700 vectors can represent refresh-token protection and privilege restriction without production identity or cryptographic assurance.",
        "The profile accepts bearer replay without rotation or sender constraint, misses revocation cascade or inactivity expiry, broadens privileges, permits downgrade, or inflates identity data.",
        "safe_now_synthetic_nonproduction", "x2_proxy_protocol", ["SRC-RFC9700"],
        ["freed-id/oauth-refresh-security-profile.json", "freed-id/oauth-refresh-security-mutations.json"],
        "Represented only; real keys, tokens, services, accounts, interoperability, privacy review, independent security review, recovery, and trust governance remain absent.",
        "Reject the vector, retain the negative, and make no account, token, key, credential, or trust decision.",
        ["real_keys", "production_identity", "interoperability", "privacy_review", "independent_security_review", "trust_governance"], "represented"),
    proposal(
        "V6495-P06",
        "CBR concrete test site and worker privacy, structural-risk notice, remediation, affected-party, legal, cultural, land-relationship, and Maori-data-governance authority gate",
        "Freed ID / CBR Heart",
        "A reservation matrix can expose privacy, notice, remediation, land-relationship, affected-party, legal, cultural, and Maori authority dependencies without exercising them.",
        "Software marks any real site disclosure, worker decision, structural-risk notice, remediation, land relationship, legal interpretation, cultural decision, or Maori data-governance decision completed.",
        "authorized_affected_parties_and_competent_authority_required", "x2_exact_gate", ["SRC-NZ-PRIVACY", "SRC-TE-MANA-RARAUNGA"],
        ["cbr/concrete-testing-risk-gate.json", "cbr/concrete-testing-authority-reservation.json"],
        "Remain exact_gate until affected people, site and land relationships, tangata whenua, iwi, hapu, Maori authorities, and competent privacy, engineering, safety, legal, cultural, remedy, and data-governance authorities decide within scope.",
        "Remove any accidental disclosure or authority claim, retain the failure, and preserve person, site, land, remedy, and cultural privacy.",
        ["affected_party_legitimacy", "professional_authority", "legal_interpretation", "cultural_ratification", "maori_data_governance", "remedy_authority"], "exact_gate"),
    proposal(
        "V6495-P07",
        "Zarr version 3 node metadata, array shape, chunk grid, codec pipeline, store key, consolidated metadata, extension, size arithmetic, resource budget, and refusal tribunal",
        "THOS Body",
        "A bounded Zarr v3 tribunal can reject malformed synthetic metadata, keys, codecs, extensions, arithmetic, and resource requests without external retrieval.",
        "It accepts invalid node metadata, shape, chunk grid, codec ordering, store key, consolidated metadata, unknown required extension, overflowing size, traversal, external retrieval, or unbounded allocation.",
        "safe_now_owner_scoped_parser_fixture", "x2_build_task", ["SRC-ZARR-V3"],
        ["formats/zarr-v3-contract.json", "formats/zarr-v3-mutations.json"],
        "All malformed fixtures are rejected, arithmetic stays bounded, external retrieval is disabled, and no exhaustive-security or production-conformance claim is made.",
        "Disable decoding, retain the fixture, and expose only inert metadata.",
        ["external_payloads", "exhaustive_security", "production_decoder", "user_files"], "completed"),
    proposal(
        "V6495-P08",
        "Accessible tooltip trigger, hover, focus, persistent content, dismissibility, hoverability, focus order, escape, fallback, and manual-reservation audit",
        "THOS Body",
        "A structural audit can verify tooltip trigger and persistence obligations while reserving manual and affected-user evaluation.",
        "The surface lacks an identifiable trigger, focus activation, persistence, dismissibility, hoverability, predictable focus, escape behavior, fallback text, or honest manual reservation.",
        "safe_now_structural_only", "x2_build_task", ["SRC-WCAG-HOVER", "SRC-WCAG22"],
        ["accessibility/tooltip-contract.json", "accessibility/tooltip-mutations.json"],
        "Pass only structural fixtures; keyboard, pointer, zoom, browser, assistive-technology, cognitive, Maori-language, and affected-user evaluation remain reserved.",
        "Publish persistent inline fallback text and retain each structural failure.",
        ["complete_accessibility", "manual_evaluation", "affected_user_acceptance", "language_authority"], "completed"),
    proposal(
        "V6495-P09",
        "Thermo-Psyche Kirchhoff thermal-radiation spectral directional absorptivity, emissivity, equilibrium, reciprocity, wavelength, solid-angle, unit, domain, and agency-nonconversion classifier",
        "Trinity Mandala bridge",
        "A typed classifier can preserve Kirchhoff radiation-law domain obligations and refuse conversion into psyche, worth, agency, consciousness, or personhood.",
        "It drops spectral or directional variables, equilibrium, reciprocity conditions, wavelength or solid angle, units, or converts absorptivity/emissivity into a law of mind or value.",
        "safe_now_formal_domain_guard", "x2_build_task", ["SRC-NIST-RADIOMETRY"],
        ["thermo-psyche/kirchhoff-radiation-contract.json", "thermo-psyche/kirchhoff-radiation-mutations.json"],
        "Every accepted row states physical variables, conditions, units, scope, and agency nonconversion.",
        "Remove the analogy, retain the physical statement only, and preserve the rejected conversion.",
        ["psyche_conversion", "consciousness", "personhood", "moral_value", "agency_measure"], "completed"),
    proposal(
        "V6495-P10",
        "Stage 20 targeted maximum-likelihood estimand, initial-outcome model, propensity model, clever covariate, targeting step, positivity, cross-fitting, influence curve, sensitivity, and nonpromotion board",
        "Trinity Mandala bridge",
        "A structural TMLE board can expose nuisance-model, targeting, positivity, cross-fitting, and uncertainty obligations without creating participant effects or Stage 20 evidence.",
        "It omits the estimand, initial model, propensity model, clever covariate, targeting step, positivity, cross-fitting, influence curve, uncertainty, sensitivity, or promotes synthetic software as an effect.",
        "safe_now_structural_nonpromotion", "x2_build_task", ["SRC-TMLE-PRIMARY"],
        ["stage20/tmle-contract.json", "stage20/tmle-mutations.json"],
        "Pass only structural fixtures; real outcomes, defensible models, participant evidence, safety monitoring, value authority, and independent review remain absent.",
        "Retain the failed fixture and keep causal-effect, participant-effect, deployment, and Stage 20 claims false.",
        ["real_participants", "causal_effect", "value_authority", "independent_review", "stage20"], "completed"),
]


SOURCES = [
    {"source_id":"SRC-LIVE-BATON","title":"Current v649-v5 activation and committed Orin baton","url":None,"status":"current","kind":"live_authority","implication":"Controls solo ownership, exact inheritance, x1-before-x2, one successful pass, no replay, privacy, authority, and terminal routing."},
    {"source_id":"SRC-RFC9111","title":"RFC 9111 HTTP Caching","url":"https://www.rfc-editor.org/rfc/rfc9111.html","status":"stable","kind":"official_standard","implication":"Supports cache age, freshness, validation, Vary, staleness, invalidation, privacy, and security obligations only."},
    {"source_id":"SRC-BW-REVIEW","title":"Tomita-Takesaki Modular Theory review and Bisognano-Wichmann context","url":"https://arxiv.org/abs/math-ph/0511034","status":"stable","kind":"primary_research_review","implication":"Supports formal modular-theory obligations only, not empirical GMUT evidence."},
    {"source_id":"SRC-MAST-JWST","title":"STScI MAST JWST official mission and data-product documentation","url":"https://archive.stsci.edu/missions-and-data/jwst","status":"current","kind":"official_archive","implication":"Supplies product-stage, instrument, association, calibration, and query context; no data are downloaded or analyzed."},
    {"source_id":"SRC-IANZ-LABS","title":"International Accreditation New Zealand testing-laboratory accreditation","url":"https://www.ianz.govt.nz/accredited-organisations/laboratories/testing-laboratories/","status":"current","kind":"official_accreditation_source","implication":"Provides laboratory competence and accreditation context; citation confers no competence, authorization, or result validity."},
    {"source_id":"SRC-RFC9700","title":"RFC 9700 Best Current Practice for OAuth 2.0 Security","url":"https://www.rfc-editor.org/rfc/rfc9700.html","status":"stable","kind":"official_standard","implication":"Supports refresh-token replay prevention and privilege restriction for synthetic vectors only."},
    {"source_id":"SRC-ZARR-V3","title":"Zarr storage specification version 3","url":"https://zarr-specs.readthedocs.io/en/latest/v3/core/v3.0.html","status":"current","kind":"official_specification","implication":"Supports bounded metadata and codec-pipeline fixtures; no external payload or production decoder is exercised."},
    {"source_id":"SRC-WCAG-HOVER","title":"W3C Understanding Content on Hover or Focus","url":"https://www.w3.org/WAI/WCAG22/Understanding/content-on-hover-or-focus.html","status":"current","kind":"official_guidance","implication":"Supports dismissible, hoverable, and persistent structural obligations while manual evaluation stays reserved."},
    {"source_id":"SRC-WCAG22","title":"Web Content Accessibility Guidelines 2.2","url":"https://www.w3.org/TR/WCAG22/","status":"stable","kind":"official_standard","implication":"Structural checks do not establish complete accessibility conformance."},
    {"source_id":"SRC-NIST-RADIOMETRY","title":"NIST radiometry and photometry quantities and units","url":"https://www.nist.gov/pml/sensor-science/radiometry-and-photometry","status":"current","kind":"official_metrology_source","implication":"Supports physical quantity and unit discipline only, not a psyche or agency law."},
    {"source_id":"SRC-TMLE-PRIMARY","title":"Targeted Learning causal inference text and TMLE methodology","url":"https://link.springer.com/book/10.1007/978-1-4419-9782-1","status":"stable","kind":"primary_method_source","implication":"Supports structural TMLE obligations; this phase estimates no participant effect."},
    {"source_id":"SRC-NZ-PRIVACY","title":"New Zealand Privacy Commissioner obligations guidance","url":"https://www.privacy.org.nz/responsibilities/your-obligations/","status":"current","kind":"official_authority","implication":"Real privacy, correction, disclosure, and remedy decisions require competent human authority and affected-person consideration."},
    {"source_id":"SRC-TE-MANA-RARAUNGA","title":"Te Mana Raraunga principles of Maori data sovereignty","url":"https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty","status":"stable","kind":"primary_authority_source","implication":"Maori data and concepts remain under Maori governance; software and citation confer no Maori authority."},
    {"source_id":"SRC-ZARR-EXTENSIONS","title":"Zarr extension mechanism and registered extensions","url":"https://zarr-specs.readthedocs.io/en/latest/v3/core/index.html","status":"draft","kind":"official_specification_watch","implication":"Draft or evolving extension material is watched and cannot be flattened into stable production assurance."},
    {"source_id":"SRC-OPENAI-CODEX","title":"OpenAI Codex official release repository","url":"https://github.com/openai/codex/releases","status":"watch","kind":"official_package","implication":"Version status is observed only; no desktop or CLI update occurs."},
]


SAFE_TASKS = [
    "Verify Orin exact source, x1, evidence, final parent, zero merges, cleanliness, and live equality",
    "Replay Orin x1, evidence, and final Git-blob manifests",
    "Fast-forward Tamar by exact single-parent ancestry only",
    "Prove Tamar pre-x1 four-way remote equality",
    "Audit all 680 frozen proposal titles and substantive neighbors",
    "Retain every rejected semantic seed and tooling fault",
    "Build current, stable, draft, and watch source statuses without flattening",
    "Freeze exactly ten proposals with no x2 outcomes",
    "Freeze 70 linked mutations without executing them",
    "Build x1 Git-blob manifest and three self-exclusions",
    "Run five-class x1 privacy scanning",
    "Record fail and pass Method Flow witnesses",
    "Refresh the phase-scoped GHC Family Index",
    "Run additive Reflection Remaster without compatibility deletion",
    "Freeze HTTP cache evidence-credit tribunal",
    "Freeze Bisognano-Wichmann obligation board",
    "Freeze JWST zero-row adapter",
    "Freeze concrete laboratory proxy",
    "Freeze RFC 9700 refresh-token profile",
    "Freeze concrete testing authority gate",
    "Freeze Zarr v3 refusal tribunal",
    "Freeze tooltip structural audit",
    "Freeze Kirchhoff radiation nonconversion classifier",
    "Freeze TMLE Stage 20 nonpromotion board",
    "Preserve inherited held approval packets",
    "Measure owner growth against the 15000-file threshold",
    "Verify Codex versions without updating software",
    "Record no Sandbox or Hyper-V action",
    "Reserve one successful canonical pass and no post-success replay",
    "Keep Sylven route prepared but unsent until exact final proof",
]

CANDIDATE_TASKS = [
    "HTTP cache-key and Vary prototype", "HTTP age, freshness, validation, and stale-response prototype",
    "Bisognano-Wichmann wedge and vacuum obligation prototype", "Bisognano-Wichmann modular-flow observation-firewall prototype",
    "JWST product-stage and CRDS-context prerequisite prototype", "JWST zero-row and likelihood-refusal prototype",
    "Concrete specimen receipt, curing, and test-age prototype", "Concrete machine, fracture, amendment, and handover prototype",
    "RFC 9700 refresh rotation and replay prototype", "RFC 9700 expiry, privilege, and minimization prototype",
    "Concrete site, worker, and structural-risk reservation prototype", "Zarr node, shape, and chunk-grid prototype",
    "Zarr codec, key, metadata, and resource-budget prototype", "Tooltip trigger, hover, and focus prototype",
    "Tooltip persistence, escape, fallback, and reservation prototype", "Kirchhoff spectral-directional domain prototype",
    "Kirchhoff agency-nonconversion prototype", "TMLE nuisance-model and targeting-step prototype",
    "TMLE positivity, cross-fitting, and influence-curve prototype", "Stage 20 TMLE nonpromotion prototype",
]

SKILL_IDEAS = [
    "ghc-family-v649-v5-http-cache-credit", "ghc-family-v649-v5-http-cache-privacy",
    "ghc-family-v649-v5-bisognano-wichmann", "ghc-family-v649-v5-gmut-observation-firewall",
    "ghc-family-v649-v5-jwst-zero-row", "ghc-family-v649-v5-concrete-specimen-lineage",
    "ghc-family-v649-v5-concrete-handover", "ghc-family-v649-v5-oauth-refresh-security",
    "ghc-family-v649-v5-oauth-minimization", "ghc-family-v649-v5-concrete-authority-reservation",
    "ghc-family-v649-v5-zarr-metadata", "ghc-family-v649-v5-zarr-resource-budget",
    "ghc-family-v649-v5-tooltip-persistence", "ghc-family-v649-v5-tooltip-fallback",
    "ghc-family-v649-v5-kirchhoff-domain", "ghc-family-v649-v5-kirchhoff-nonconversion",
    "ghc-family-v649-v5-tmle-obligations", "ghc-family-v649-v5-stage20-nonpromotion",
    "ghc-family-v649-v5-method-flow-recovery", "ghc-family-v649-v5-terminal-proof",
]

RUNNER_IDEAS = [
    "ghc_family_v649_v5_http_cache.py", "ghc_family_v649_v5_bw_obligations.py",
    "ghc_family_v649_v5_jwst_refusal.py", "ghc_family_v649_v5_concrete_lab.py",
    "ghc_family_v649_v5_oauth_refresh.py", "ghc_family_v649_v5_zarr_tribunal.py",
    "ghc_family_v649_v5_accessibility_audit.py", "ghc_family_v649_v5_domain_guards.py",
    "ghc_family_v649_v5_portfolio.py", "build_ghc_family_v649_v5_closeout.py",
]

CLEANUP_TASKS = [
    "Normalize v649-v5 JSON ordering and UTF-8 output only", "Validate the four outcome labels exactly",
    "Validate current stable draft and watch source labels", "Assert exactly ten proposals",
    "Assert the frozen total is 690", "Assert source x1 evidence and final ancestry",
    "Assert zero phase merges and one final parent", "Guard x1 from x2 implementation and outcomes",
    "Label Git-blob and checkout-byte hash domains", "Label all five privacy classes",
    "Quarantine scanner definitions explicitly", "Enforce the 6000-word document cap",
    "Measure Tamar-owned additions only", "Mark citations as non-observations",
    "Separate same-owner checking from independent reproduction", "Record no Sandbox or Hyper-V action",
    "Record no desktop or CLI update", "Record no cross-platform send",
    "Record zero created tasks and subagents", "Keep terminal routing prepared-not-sent",
    "Reserve complete accessibility evaluation", "Reserve Maori-language and authority evaluation",
    "Record zero real data and likelihood rows", "Record zero participants and operators",
    "Record zero production identity operations", "Reject exhaustive-security language",
    "Attach rollback and recovery to every prototype", "Check protected-gate parity",
    "Review exact staged paths", "Require final four-way remote equality",
]

X1_OPERATIONAL_NEGATIVES = [
    {"negative_id":"V6495-X1-N01","category":"combined_receipt_listing_timeout","failed":"An over-broad combined receipt listing exceeded its bounded timeout before producing attributable output.","recovery":"Split exact receipt reads and manifest checks into bounded queries.","passing":"The split reads returned exact source counts, gates, Method Flow totals, and manifests.","recurrence_guard":"Query exact receipts and immutable manifests separately."},
    {"negative_id":"V6495-X1-N02","category":"parallel_wrapper_aggregation_failure","failed":"A parallel read wrapper aborted aggregation when one discovery search returned a nonzero status.","recovery":"Use all-settled aggregation and normalize expected empty-search exits.","passing":"The corrected wrapper returned Tamar state, frozen-index shape, phase files, and script inventory.","recurrence_guard":"Use all-settled orchestration for independent read-only probes."},
    {"negative_id":"V6495-X1-N03","category":"broad_title_extraction_timeout","failed":"A broad ripgrep and PowerShell title pipeline timed out without complete evidence.","recovery":"Parse the frozen JSON once and print only the requested proposal family.","passing":"Bounded JSON parsing returned the GMUT title family completely.","recurrence_guard":"Prefer structured JSON projection over broad text pipelines."},
    {"negative_id":"V6495-X1-N04","category":"multi_term_query_timeout","failed":"A repeated ripgrep term loop timed out after partial no-hit output.","recovery":"Treat partial output as no credit and use narrower structured searches.","passing":"Subsequent bounded family projections and exact terms supplied attributable novelty evidence.","recurrence_guard":"Limit each semantic probe by family and mechanism."},
    {"negative_id":"V6495-X1-N05","category":"memory_registry_no_current_match","failed":"The memory registry had no exact v649-v4 or v649-v5 current-phase entry.","recovery":"Retain the no-match and use the committed baton plus exact live Git proof.","passing":"No continuity was inferred from memory silence; live authority and Git controlled.","recurrence_guard":"Treat absent current memory as absence, never as proof."},
    {"negative_id":"V6495-X1-N06","category":"semantic_seed_collisions","failed":"Initial Tomita-Takesaki, Euclid, OpenID Federation, dragging, Planck, proximal-causal, Stefan-Boltzmann, and synthetic-control seeds collided with frozen proposals.","recovery":"Withdraw every collision and replace mechanisms without lowering the novelty threshold.","passing":"The revised ten passed the unchanged lexical screen and manual substantive-neighbor review across 680 proposals.","recurrence_guard":"A new domain label does not establish a new mechanism."},
    {"negative_id":"V6495-X1-N07","category":"similarity_tuple_comparison_fault","failed":"A read-only similarity helper compared equal-score tuples containing dictionaries and raised TypeError.","recovery":"Supply an explicit numeric key for maximum-score selection.","passing":"The corrected helper returned bounded nearest-neighbor scores for both replacement seeds.","recurrence_guard":"Always key aggregate selection on the numeric score when payloads are non-orderable."},
]
