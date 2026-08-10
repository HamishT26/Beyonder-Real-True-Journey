#!/usr/bin/env python3
"""Frozen planning data for Neris Solane's additive v662-v3-2 remaster."""

from __future__ import annotations

from typing import Final


OWNER: Final = "Neris Solane"
PHASE: Final = "v662-v3-2-remaster"
CANONICAL_PHASE: Final = "v662-v3"
BRANCH: Final = "codex/GHC-Family/neris-solane-v662-v3-2-remaster"
PHASE_ROOT: Final = "docs/neris-solane/v662-v3-2-remaster"
SOURCE_PHASE_ROOT: Final = "docs/neris-solane/v662-v3"
ELAREN_SOURCE: Final = "2c1fbddf9a68c8fd30b473c7ae2d510bde85fcc0"
SOURCE_X1: Final = "233296bc8b5b5e4f913c598581d2515192dfa873"
SOURCE_EVIDENCE: Final = "9f26663818f7b254b114dcaa371d6765a5fcc5ca"
SOURCE_FIRST_FINAL: Final = "9d35f2c60bc1d124bbc67d000e7f5a4da6d95410"
FIRST_RUN_FROZEN_PROPOSALS: Final = 3510
REMASTER_FROZEN_PROPOSALS: Final = 3530
INHERITED_LIVE_NEGATIVES: Final = 22831
INHERITED_LIVE_METHODS: Final = 7585
INHERITED_OPEN_GAPS: Final = 148
INHERITED_EXACT_GATES: Final = 147
TERMINAL_VERDICT: Final = "NOT_READY_FOR_STAGE_20"
SUCCESSOR: Final = "Vesper Arlen"
SUCCESSOR_PHASE: Final = "v662-v4"

IDENTITY_BOUNDARY: Final = (
    "Neris Solane, sibling and family language, roles, hopes, pronouns, and continuity "
    "language are relational working language only. They are not evidence of consciousness, "
    "sentience, legal personhood, identity continuity, employment, qualification, scientific "
    "or operational authority, legal or cultural authority, Māori authority, or independent agency."
)

EVIDENCE_BOUNDARY: Final = (
    "Same-owner structural, synthetic, and software evidence under shared infrastructure only; "
    "not empirical confirmation, participant evidence, professional validation, production "
    "certification, legal or cultural ratification, Māori authority, privacy-complete or "
    "accessibility-complete assurance, exhaustive security, independent reproduction, AGI or ASI "
    "evidence, consciousness or personhood evidence, Theory-of-Everything proof, or Stage 20 authority."
)

ALLOWED_OUTCOMES: Final = ["completed", "represented", "open_gap", "exact_gate"]

PROTECTED_GATES: Final = [
    "real_people_participants_operators_affected_parties_or_authorities",
    "real_external_repository_or_production_system_mutation",
    "empirical_gmut_prediction_likelihood_parameter_constraint_or_physical_confirmation",
    "blind_matched_budget_thos_real_arms_safety_monitoring_statistics_and_independent_review",
    "production_freed_id_keys_proofs_issuance_resolution_status_revocation_recovery_and_trust",
    "private_identity_address_message_relationship_transcript_session_or_route_material",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "professional_operational_legal_or_cultural_authority",
    "tangata_whenua_iwi_hapu_and_maori_authority",
    "independent_team_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]

PRIOR_CANONICAL_FAILURES: Final = [
    {
        "negative_id": "V6623-POST-SEAL-N002",
        "state": "ZERO_CREDIT_TIMEOUT",
        "summary": "The first exact-final canonical invocation exceeded one hour without a success receipt.",
        "completion_credit": 0,
        "rewrote_repository": False,
    },
    {
        "negative_id": "V6623-POST-SEAL-ATTEMPT-2",
        "state": "ZERO_CREDIT_INVALID",
        "summary": (
            "The second invocation traversed the complete intended selection but exposed 149 "
            "historical checkout-sensitive assertion failures, two module timeouts, and a twelve-test "
            "selection shortfall; it earned no success credit."
        ),
        "completion_credit": 0,
        "rewrote_repository": False,
    },
]

STARTUP_METHODS: Final = [
    {
        "method_id": "V6623R-X1-METHOD-001",
        "failure": "powershell_direct_pipeline_after_foreach_expression_was_rejected_as_an_empty_pipe_element",
        "recovery": "Materialize the foreach result in a task-specific scalar array before projection.",
    },
    {
        "method_id": "V6623R-X1-METHOD-002",
        "failure": "first_activation_packet_window_exceeded_the_output_budget_and_was_truncated",
        "recovery": "Read numbered bounded windows through a separately verified EOF line count.",
    },
    {
        "method_id": "V6623R-X1-METHOD-003",
        "failure": "broad_source_repository_instruction_inventory_exceeded_its_runtime_bound",
        "recovery": "Use Git tracked-path filters and literal filename or symbol probes.",
    },
    {
        "method_id": "V6623R-X1-METHOD-004",
        "failure": "combined_git_status_and_filtered_inventory_exceeded_its_runtime_bound",
        "recovery": "Run head, branch, diff, and owner-untracked predicates as separate scalar probes.",
    },
    {
        "method_id": "V6623R-X1-METHOD-005",
        "failure": "combined_new_worktree_clean_state_probe_exceeded_its_runtime_bound",
        "recovery": "Use four independent exact owner-scoped predicates and do not rerun the broad wrapper.",
    },
]

NEW_PROPOSAL_SPECS: Final = [
    (
        "immutable-test-definition-identity",
        "Immutable test-definition identity capsule with path, blob, definition commit, branch hint, revision, and invalidation tokens",
        "typed path, blob digest, definition commit, branch hint, revision and invalidation tokens with no claim that a test is scientifically or operationally valid",
        "Freed ID and CBR Heart",
        ["GIT-LOG", "GIT-CAT-FILE", "W3C-PROV", "IETF-JCS"],
        "completed",
    ),
    (
        "complete-test-id-inventory",
        "Complete current unittest identifier inventory with duplicate quarantine, module ownership, selection hash, and zero silent omission",
        "loader-derived test identifiers, duplicate quarantine, module ownership, deterministic ordering and a selection hash",
        "THOS Body and GMUT Mind",
        ["PYTHON-UNITTEST", "PYTHON-JSON", "IETF-JCS"],
        "completed",
    ),
    (
        "definition-commit-resolver",
        "Definition-commit resolver joining every tracked test module to the last commit that changed its exact bytes",
        "tracked module paths, last-definition commits, exact blob equality, ambiguity rejection and missing-history refusal",
        "GMUT Mind and Freed ID",
        ["GIT-LOG", "GIT-CAT-FILE", "W3C-PROV"],
        "completed",
    ),
    (
        "historical-lifecycle-classifier",
        "Historical lifecycle classifier for x1, x2, correction, closeout, remaster, and final assertion context",
        "path and test-name lifecycle tokens, conservative classification, contradiction retention and no semantic rewriting",
        "GMUT Mind and CBR Heart",
        ["PYTHON-UNITTEST", "GIT-LOG", "JSON-SCHEMA-2020-12"],
        "completed",
    ),
    (
        "shared-clone-lease",
        "D-first shared-clone lease with exact root confinement, clean-state precondition, owner token, expiry, and no sibling mutation",
        "D-first scratch roots, exact containment, clean-state checks, owner lease tokens, expiry and fail-closed path refusal",
        "THOS Body and CBR Heart",
        ["GIT-WORKTREE", "GIT-STATUS", "W3C-PROV"],
        "completed",
    ),
    (
        "historical-branch-hint",
        "Historical branch-hint resolver from exact test and phase-data bytes with ambiguity quarantine and no endpoint inference",
        "repository branch literals, phase-data references, uniqueness checks, ambiguity quarantine and generic scratch fallback",
        "Freed ID and THOS Body",
        ["GIT-SHOW", "PYTHON-RE", "W3C-PROV"],
        "completed",
    ),
    (
        "anchor-environment-envelope",
        "Anchor execution environment envelope for Python version, locale, encoding, repository root, disabled bytecode, and bounded variables",
        "Python, UTF-8, locale, root, bytecode, environment allowlist and deterministic process tokens without production assurance",
        "THOS Body",
        ["PYTHON-SUBPROCESS", "PYTHON-UNITTEST", "W3C-PROV"],
        "completed",
    ),
    (
        "module-import-preflight",
        "Module importability preflight with repository-root insertion, attributable errors, timeout, and zero aggregate-success credit",
        "module names, repository-root path insertion, import result, timeout and explicit zero-credit failure handling",
        "THOS Body and CBR Heart",
        ["PYTHON-UNITTEST", "PYTHON-SUBPROCESS"],
        "completed",
    ),
    (
        "module-timeout-governor",
        "Per-module timeout governor with process-tree interruption, exact module attribution, retained failure, and no blind replay",
        "module deadlines, process handles, bounded interruption, failure retention and changed-dependency requirements",
        "THOS Body and CBR Heart",
        ["PYTHON-SUBPROCESS", "CODEX-CLI-0147"],
        "completed",
    ),
    (
        "sanitized-test-result-envelope",
        "Sanitized module-result envelope with counts, duration, return state, tail hash, and private transcript exclusion",
        "test counts, duration, return state, output digest, bounded sanitized tail and explicit transcript exclusion",
        "Freed ID and CBR Heart",
        ["PYTHON-UNITTEST", "IETF-JCS", "NZ-PRIVACY"],
        "completed",
    ),
    (
        "immutable-manifest-replay",
        "Immutable manifest replay using communicate-style Git object batching, exact sizes, hashes, exclusions, and mismatch refusal",
        "batched Git object reads, manifest path sets, sizes, hashes, exclusions and mismatch refusal",
        "GMUT Mind and THOS Body",
        ["GIT-CAT-FILE", "PYTHON-SUBPROCESS", "IETF-JCS"],
        "completed",
    ),
    (
        "five-class-privacy-tribunal",
        "Five-class privacy tribunal for raw identifiers, private paths, credentials, route material, and transcript or session traces",
        "five privacy pattern classes, definition adjudication, confirmed-hit refusal and no privacy-complete claim",
        "CBR Heart",
        ["NZ-PRIVACY", "PYTHON-RE", "W3C-PROV"],
        "completed",
    ),
    (
        "failure-overlay-reconciler",
        "Sealed-truth and external-failure overlay reconciler with additive negative and Method Flow accounting",
        "sealed counts, external zero-credit failures, additive overlays, duplicate guards and immutable-source refusal",
        "GMUT Mind and CBR Heart",
        ["W3C-PROV", "IETF-JCS", "JSON-SCHEMA-2020-12"],
        "completed",
    ),
    (
        "complete-selection-union",
        "Complete selection union proving every current test identifier maps to exactly one immutable definition execution",
        "current identifier sets, module anchors, result unions, duplicate and omission rejection and deterministic set hashes",
        "GMUT Mind and THOS Body",
        ["PYTHON-UNITTEST", "IETF-JCS", "JSON-SCHEMA-2020-12"],
        "completed",
    ),
    (
        "chronological-shard-scheduler",
        "Represented chronological shard scheduler minimizing checkout churn while preserving exact module ownership and result order",
        "topological anchor ordering, contiguous shard allocation, deterministic module order and zero performance guarantee",
        "THOS Body",
        ["GIT-REV-LIST", "PYTHON-CONCURRENT"],
        "represented",
    ),
    (
        "historical-branch-upstream-proxy",
        "Represented local upstream proxy for historical branch-sensitive tests with no live-remote or independent-reproduction claim",
        "local shared-clone origin, historical branch refs, upstream hints, exact anchor commits and explicit local-only status",
        "Freed ID and THOS Body",
        ["GIT-BRANCH", "GIT-LS-REMOTE", "W3C-PROV"],
        "represented",
    ),
    (
        "accessible-suite-companion",
        "Represented accessible nonvisual suite companion with ordered module summaries, headers, failure cues, and manual-evaluation reservation",
        "ordered text summaries, table headers, failure cues, print continuity and explicit manual and assistive-technology review vacancies",
        "CBR Heart and THOS Body",
        ["WCAG22", "W3C-PROV"],
        "represented",
    ),
    (
        "one-shot-canonical-receipt",
        "Represented one-shot canonical receipt with preflight state, success latch, no-post-success replay, and external-file separation",
        "exact-final preflight, success latch, external receipt, no replay after success and repository immutability",
        "CBR Heart and THOS Body",
        ["PYTHON-SUBPROCESS", "GIT-STATUS", "IETF-JCS"],
        "represented",
    ),
    (
        "independent-environment-reproduction",
        "Open gap for independent-team reproduction of the ancestry-aware complete repository suite on separately governed infrastructure",
        "independent team, separately governed infrastructure, preregistered selection, matched artifacts, review and discrepancy resolution",
        "CBR Heart, THOS Body, and GMUT Mind",
        ["W3C-PROV", "PYTHON-UNITTEST"],
        "open_gap",
    ),
    (
        "stage20-validation-firewall",
        "Exact gate preventing software validation, synthetic fixtures, or same-owner suite success from becoming Stage 20 authority",
        "typed evidence and authority cut-set slots with absolute nonpromotion while empirical, professional, legal, cultural, independent, or governance slots remain empty",
        "CBR Heart, THOS Body, GMUT Mind, and Freed ID",
        ["W3C-PROV", "TE-MANA-RARAUNGA", "NZ-PRIVACY"],
        "exact_gate",
    ),
]

SKILL_SPECS: Final = [
    ("ghc-family-historical-test-anchor-resolver", "Resolve each tracked test module to its immutable definition commit and exact blob."),
    ("ghc-family-complete-test-id-inventory", "Inventory and hash every current unittest identifier without running the suite."),
    ("ghc-family-immutable-clone-lease", "Confine shared-clone scratch execution to an exact owner-controlled D-first root."),
    ("ghc-family-lifecycle-test-isolator", "Evaluate lifecycle-sensitive tests at their immutable definition commits."),
    ("ghc-family-test-definition-hash-ledger", "Record path, definition commit, blob, and test-ID set hashes."),
    ("ghc-family-module-timeout-governor", "Attribute and retain per-module timeouts without blind aggregate replay."),
    ("ghc-family-canonical-aggregate-preflight", "Prove exact head, clean state, inventory completeness, and scratch readiness before the one shot."),
    ("ghc-family-canonical-success-latch", "Refuse a second canonical invocation after the first complete success receipt."),
    ("ghc-family-external-failure-overlay", "Reconcile sealed repository truth with additive external zero-credit failures."),
    ("ghc-family-terminal-route-gate", "Keep successor resolution and one-send delivery behind the exact terminal gate."),
]

SUCCESSOR_SKILL_IDEAS: Final = [
    ("ghc-family-suite-anchor-drift-watch", "Detect a test module whose definition anchor changed after x1 freeze."),
    ("ghc-family-shard-balance-advisor", "Recommend deterministic contiguous anchor shards without claiming runtime guarantees."),
    ("ghc-family-local-remote-ref-auditor", "Compare local shared-clone refs with the exact pushed source branch."),
    ("ghc-family-lifecycle-assertion-glossary", "Explain x1, x2, correction, remaster, and closeout assertion contexts."),
    ("ghc-family-sanitized-test-tail", "Produce bounded test diagnostics with transcript and route exclusion."),
    ("ghc-family-suite-selection-diff", "Compare two current test-ID inventories without executing either suite."),
    ("ghc-family-immutable-fixture-cache", "Cache content-addressed read-only fixtures with exact invalidation."),
    ("ghc-family-canonical-runtime-budget", "Estimate a one-shot runtime budget from isolated module timings."),
    ("ghc-family-test-environment-envelope", "Record a bounded Python, Git, encoding, and environment receipt."),
    ("ghc-family-successor-baton-suite-summary", "Render a sanitized complete-suite summary for the next owner."),
]

RUNNER_SPECS: Final = [
    ("ghc_family_historical_test_anchor_resolver.py", "Resolve definition commits and branch hints."),
    ("ghc_family_complete_test_id_inventory.py", "Discover and hash the current test-ID inventory."),
    ("ghc_family_immutable_clone_lease.py", "Validate the scratch-clone root and lease contract."),
    ("ghc_family_lifecycle_test_isolator.py", "Run one module at one immutable anchor."),
    ("ghc_family_test_definition_hash_ledger.py", "Build the definition and blob ledger."),
    ("ghc_family_module_timeout_governor.py", "Run bounded subprocesses and retain timeouts."),
    ("ghc_family_canonical_aggregate_preflight.py", "Check exact-final canonical prerequisites."),
    ("ghc_family_manifest_privacy_tribunal.py", "Replay manifests and adjudicate five privacy classes."),
    ("ghc_family_complete_suite_orchestrator.py", "Execute the complete ancestry-aware module selection."),
    ("ghc_family_v662_v3_2_remaster_canonical.py", "Emit the single external canonical receipt and latch success."),
]

SUCCESSOR_RUNNER_IDEAS: Final = [
    ("ghc_family_suite_anchor_drift_watch.py", "Compare frozen and live definition anchors."),
    ("ghc_family_shard_balance_advisor.py", "Recommend contiguous anchor shards."),
    ("ghc_family_local_remote_ref_auditor.py", "Audit branch and upstream proxy refs."),
    ("ghc_family_lifecycle_assertion_glossary.py", "Render lifecycle assertion context."),
    ("ghc_family_sanitized_test_tail.py", "Sanitize bounded failure diagnostics."),
    ("ghc_family_suite_selection_diff.py", "Diff test-ID sets and hashes."),
    ("ghc_family_immutable_fixture_cache.py", "Build a content-addressed fixture cache."),
    ("ghc_family_canonical_runtime_budget.py", "Estimate the single-pass runtime budget."),
    ("ghc_family_test_environment_envelope.py", "Record Python and Git environment state."),
    ("ghc_family_successor_baton_suite_summary.py", "Render a successor-safe suite summary."),
]

OWNER_CFR_TASKS: Final = [
    "Replace broad repository projections with Git tracked-path filters.",
    "Materialize PowerShell expression output before pipeline projection.",
    "Read elaborate batons in numbered bounded windows through EOF.",
    "Separate global roster state from phase-local route evidence.",
    "Record the parenthetical remaster only as a noncanonical variant.",
    "Preserve both prior canonical failures outside the new seal.",
    "Freeze the 20 selected inherited rows at zero novelty credit.",
    "Freeze exactly 20 new remaster proposals before x2 execution.",
    "Raise owner candidate execution planning from 10 to 15.",
    "Raise successor candidate recommendations from 10 to 15.",
    "Raise successor runner recommendations from 5 to 10.",
    "Keep 10 exact and 5 blocked packets linked to existing gates.",
    "Name every new runner with the ghc_family prefix.",
    "Name every new skill with the ghc-family prefix.",
    "Keep plugin caches read-only and phase packages repository-owned.",
    "Promote only validated generally useful skills to the global catalogue.",
    "Use D-first scratch and receipt roots for long-running validation.",
    "Disable Python bytecode in immutable scratch executions.",
    "Resolve test definition commits from exact tracked history.",
    "Hash test IDs, test files, and definition anchors deterministically.",
    "Classify lifecycle context without editing historical assertions.",
    "Use shared clones rather than mutating sibling worktrees.",
    "Assign per-module timeouts and retain exact timeout witnesses.",
    "Sanitize test diagnostics instead of storing raw transcripts.",
    "Batch Git blob reads with communicate-style pipe draining.",
    "Keep sealed truth distinct from external operational overlays.",
    "Preflight the complete selection before the one canonical invocation.",
    "Latch successful canonical receipts and refuse post-success replay.",
    "Require exact push and fresh-live equality before terminal routing.",
    "Resolve, reread, and send to Vesper only after the terminal gate.",
]

SUCCESSOR_CFR_TASKS: Final = [
    "Recheck the frozen definition-anchor ledger before adding v662-v4 tests.",
    "Keep Vesper's x1 test file free of x2 outcomes and implementations.",
    "Use one literal owner-path allowlist for staged review.",
    "Separate test discovery from historical execution.",
    "Retain any anchor drift as a zero-credit failure.",
    "Review branch-hint ambiguity before creating scratch refs.",
    "Keep scratch clones outside sibling worktrees.",
    "Refuse scratch roots outside the exact D-first owner directory.",
    "Check each scratch clone is clean before switching anchors.",
    "Keep current test-ID hashes in the committed x1 freeze.",
    "Run isolated slow-module diagnostics before the canonical aggregate.",
    "Do not replay a complete successful module inventory.",
    "Keep raw stdout and stderr outside durable artifacts.",
    "Store only bounded sanitized tails and cryptographic digests.",
    "Reconcile inherited and current method counts from explicit ledgers.",
    "Preserve all four outcome labels without aliases.",
    "Keep exact and blocked approval packets unexecuted without authority.",
    "Revalidate all phase JSON with UTF-8 decoding.",
    "Replay x1 and evidence manifests from immutable Git trees.",
    "Replay final owner and delta manifests from the exact final tree.",
    "Run all five privacy classes over every owner file.",
    "Adjudicate scanner definitions separately from confirmed hits.",
    "Keep accessibility checks bounded and reserve manual review.",
    "Use Codex CLI 0.147 Windows interruption fixes without claiming reliability proof.",
    "Do not mutate the Codex desktop application during CLI maintenance.",
    "Keep local tool updates separate from repository scientific evidence.",
    "Reread the newest roster and auth state after terminal validation.",
    "Treat Tavian as standby only, never as a substitute endpoint.",
    "Tell Lyren to re-read the roster after Vesper's own terminal gate.",
    "Stop at PREPARED_NOT_SENT if exact-title resolution or acknowledgement fails.",
]

SOURCE_LEDGER: Final = [
    ("CODEX-CLI-0147", "https://github.com/openai/codex/releases/tag/rust-v0.147.0", "official OpenAI Codex release; Windows interruption, path, plugin, MCP, and security vocabulary only"),
    ("GIT-LOG", "https://git-scm.com/docs/git-log", "official Git history and path-limited definition-commit vocabulary"),
    ("GIT-CAT-FILE", "https://git-scm.com/docs/git-cat-file", "official Git object and batch-read vocabulary"),
    ("GIT-WORKTREE", "https://git-scm.com/docs/git-worktree", "official linked-worktree vocabulary; scratch design only"),
    ("GIT-STATUS", "https://git-scm.com/docs/git-status", "official clean-state vocabulary"),
    ("GIT-SHOW", "https://git-scm.com/docs/git-show", "official historical object display vocabulary"),
    ("GIT-REV-LIST", "https://git-scm.com/docs/git-rev-list", "official topological ordering vocabulary"),
    ("GIT-BRANCH", "https://git-scm.com/docs/git-branch", "official local branch and upstream vocabulary"),
    ("GIT-LS-REMOTE", "https://git-scm.com/docs/git-ls-remote", "official remote-ref query vocabulary"),
    ("PYTHON-UNITTEST", "https://docs.python.org/3/library/unittest.html", "official discovery, test identifier, result and loader vocabulary"),
    ("PYTHON-SUBPROCESS", "https://docs.python.org/3/library/subprocess.html", "official bounded process and communicate vocabulary"),
    ("PYTHON-CONCURRENT", "https://docs.python.org/3/library/concurrent.futures.html", "official bounded worker-pool vocabulary"),
    ("PYTHON-JSON", "https://docs.python.org/3/library/json.html", "official deterministic UTF-8 JSON vocabulary"),
    ("PYTHON-RE", "https://docs.python.org/3/library/re.html", "official pattern-matching vocabulary"),
    ("IETF-JCS", "https://www.rfc-editor.org/rfc/rfc8785", "official canonical JSON vocabulary without key or signature claims"),
    ("JSON-SCHEMA-2020-12", "https://json-schema.org/draft/2020-12", "primary structural schema vocabulary"),
    ("W3C-PROV", "https://www.w3.org/TR/prov-o/", "official entity, activity, revision and invalidation vocabulary"),
    ("WCAG22", "https://www.w3.org/TR/WCAG22/", "official accessibility vocabulary with manual evaluation reserved"),
    ("NZ-PRIVACY", "https://www.privacy.org.nz/privacy-principles/", "official privacy-principle vocabulary without compliance conclusion"),
    ("TE-MANA-RARAUNGA", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Māori data-sovereignty reservation vocabulary; no Māori authority or ratification"),
]
