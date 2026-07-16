# GHC Family Method Flow State

- Phase: v646-gmut-thos-v2-x1-x2
- Owner: Ilyra Fen
- Methods: 28
- Passing witnesses: 28
- Failed witnesses retained: 38

## Preferred methods

### V6462-M01 — Separate scanner definitions from confirmed staged-file hits

- Trigger: scanner implementation is itself in the scanned staged surface; a definition literal matches its own signature
- Method: Construct scanner signatures from source fragments that do not themselves match while preserving the compiled detection expression.
- Recurrence guard: Scanner definitions and confirmed content hits remain separate evidence classes; a definition-safe scanner must still detect constructed marker fixtures.
- Rollback: Give each invalid staged review zero freeze credit and retain the preceding Git-index state.
- Witnesses: V6462-M01-F1, V6462-M01-F2, V6462-M01-F3, V6462-M01-P

### V6462-M02 — Stabilize a receipt-inclusive self-excluding staged manifest

- Trigger: review receipts are generated from the staged path set; the manifest excludes its own hash
- Method: Finalize the staged path set, generate receipts, add them, regenerate once, add again, then require an unchanged review.
- Recurrence guard: A staged manifest receives freeze credit only when a post-add regeneration is byte-unchanged.
- Rollback: Do not commit while generated receipts differ from their Git-index copies.
- Witnesses: V6462-M02-F, V6462-M02-P

### V6462-M03 — Resolve inherited Method Flow records before reading examples

- Trigger: an inherited record layout may differ from an assumed template; the lookup is read-only
- Method: Resolve record paths from the current inherited tree before reading any optional subdirectory.
- Recurrence guard: Use repository-relative file discovery and select existing records before any content read.
- Rollback: Give the failed lookup zero evidence credit and make no inherited-tree mutation.
- Witnesses: V6462-M03-F, V6462-M03-P

### V6462-M04 — Synchronize structural assertions with append-only Method Flow growth

- Trigger: operational failures occur before x1 freeze; Method Flow correctly retains their witnesses; x2 lifecycle remains absent
- Method: Bind structural validation to append-only Method Flow cardinality and retained-negative coverage instead of a frozen zero-count assumption.
- Recurrence guard: Count-dependent assertions derive from the current append-only ledger and negative rows; lifecycle separation is checked independently.
- Rollback: Give every structurally invalid replay zero freeze credit and retain its negative.
- Witnesses: V6462-M04-F1, V6462-M04-F2, V6462-M04-F3, V6462-M04-F4, V6462-M04-P

### V6462-M05 — Inspect Method Flow auto-promotion before explicit transitions

- Trigger: a passing witness was just recorded; the runner may auto-promote candidate to validated
- Method: Inspect the current ledger state after a passing witness and request only the next permitted transition.
- Recurrence guard: Never assume the pre-witness state persists; read the post-witness state before set-state.
- Rollback: Give each invalid transition zero state-change credit while preserving the successful state already recorded by the witness.
- Witnesses: V6462-M05-F1, V6462-M05-F2, V6462-M05-F3, V6462-M05-P

### V6462-M07 — Assert positive and expected-empty cardinality in source-search witnesses

- Trigger: a search result is used as validation evidence; the expected presence or absence is known
- Method: Require positive cardinality for expected-present searches and independently verify the obsolete pattern is expected-empty.
- Recurrence guard: Every search witness declares expected-present or expected-empty semantics and checks native exit status and cardinality accordingly.
- Rollback: Deprecate the method supported by the flawed witness and give the zero-line result no validation credit.
- Witnesses: V6462-M07-F, V6462-M07-F2, V6462-M07-P

### V6462-M08 — Resolve configured skill location from receipts before reading

- Trigger: an inherited skill build may target the configured skill root; repository-local package location is not guaranteed
- Method: Resolve the skill build receipt and indexed configured skill root before assuming a repository-local package directory.
- Recurrence guard: Locate the committed receipt first and use only its sanitized package names; never publish the configured local root.
- Rollback: Give the failed path assumption zero evidence credit and make no skill or source mutation.
- Witnesses: V6462-M08-F, V6462-M08-P

### V6462-M09 — Bind skill smoke assertions to the frozen artifact schema

- Trigger: a skill smoke test consumes a frozen phase artifact; field names may differ from the test assumption
- Method: Read the frozen rotation-guard schema and bind smoke assertions to its actual threshold and inherited-baseline fields.
- Recurrence guard: Smoke tests read the frozen artifact schema before asserting field names, and retry accounting preserves first-invocation origins.
- Rollback: Give the 19-of-20 smoke result zero portfolio completion credit and preserve all initialized packages unchanged.
- Witnesses: V6462-M09-F, V6462-M09-P

### V6462-M10 — Allow retained active candidates without premature promotion

- Trigger: a retry runs while its recovery method is still candidate; a failed witness is already retained
- Method: Permit a current candidate only when its retained failed witness is present; require a passing witness before terminal promotion.
- Recurrence guard: Candidate state is accepted only for an active recorded failure; it never receives preferred credit before a pass.
- Rollback: Give the 19-of-20 retry zero portfolio credit and leave the active candidate unpromoted.
- Witnesses: V6462-M10-F, V6462-M10-P

### V6462-M11 — Bind identity validation to the declared receipt field

- Trigger: identity receipt has a specialized schema key; validator uses an assumed generic alias
- Method: Read the frozen identity-receipt schema and assert the relational language through its identity_boundary field.
- Recurrence guard: Validator field access is bound to the committed schema key rather than an assumed generic alias.
- Rollback: Give the failed minimal run zero validation credit and leave the evidence candidate uncommitted.
- Witnesses: V6462-M11-F, V6462-M11-P

### V6462-M12 — Bind the source-status runner to the frozen ledger schema

- Trigger: a runner consumes a frozen source ledger; field placement differs from an assumed schema
- Method: Bind source-status assertions to the frozen top-level checked_on field, per-row use field, authority descriptor, and nullable local-skill URL.
- Recurrence guard: Runner guards inspect the frozen ledger schema before asserting row and ledger field placement.
- Rollback: Stop the aggregate at the first failed runner, preserve its output, and give all ten zero aggregate-use credit.
- Witnesses: V6462-M12-F, V6462-M12-P

### V6462-M13 — Split compound read-only preflight probes

- Trigger: a wrapper combines multiple worktree probes; one probe may exceed the shared timeout
- Method: Split compound status, head, and file probes into independently bounded commands with explicit output expectations.
- Recurrence guard: Read-only preflight wrappers keep Git identity, Git status, and potentially large file reads in separate bounded invocations.
- Rollback: Give the timed-out wrapper zero evidence credit and make no repository mutation based on partial output.
- Witnesses: V6462-M13-F, V6462-M13-P

### V6462-M14 — Bind proposal counts to the frozen index schema

- Trigger: a guard consumes the frozen proposal index; cardinality fields have schema-specific names
- Method: Bind the proposal-neighbor guard to frozen_chain_count_after_x1 in the immutable proposal index.
- Recurrence guard: Proposal-count guards inspect the immutable index schema and bind to its declared prior and after-x1 cardinality keys.
- Rollback: Stop the aggregate, preserve both runner outputs, and give all ten zero aggregate completion credit.
- Witnesses: V6462-M14-F, V6462-M14-P

### V6462-M15 — Resolve runner diagnostic paths from current source

- Trigger: a diagnostic follows a runner failure; the runner source declares its actual inputs
- Method: Resolve diagnostic input paths from the runner implementation and verify existence before reading.
- Recurrence guard: Diagnostics select repository-relative inputs from the current runner source and require path existence before content reads.
- Rollback: Give the missing-path read zero evidence credit and make no repository mutation based on the failed lookup.
- Witnesses: V6462-M15-F, V6462-M15-P

### V6462-M16 — Bind prior count to the collision-audit schema

- Trigger: the proposal guard consumes both collision audit and proposal index; each artifact declares its own count key
- Method: Bind the collision-audit prior count to prior_frozen_proposal_count and require an isolated pass before aggregate reuse.
- Recurrence guard: Proposal guards bind both prior_frozen_proposal_count and frozen_chain_count_after_x1 from their respective immutable artifacts.
- Rollback: Give the failed isolated replay zero validation credit and leave aggregate use incomplete.
- Witnesses: V6462-M16-F, V6462-M16-P

### V6462-M17 — Discover exact reviewer filenames before reuse

- Trigger: a prior-phase reviewer is being inspected; filename conventions may differ
- Method: Discover phase reviewer names repository-relatively before selecting a source file for reuse.
- Recurrence guard: Reviewer-source reuse begins with a positive-cardinality repository-relative filename search.
- Rollback: Give the missing-file lookup zero evidence credit and make no design inference from an absent path.
- Witnesses: V6462-M17-F, V6462-M17-P

### V6462-M18 — Bind current-phase tests to generated evidence schemas

- Trigger: a new test module consumes generated phase artifacts; artifact names or fields are schema-specific
- Method: Discover exact generated artifact paths and fields, synchronize the test module, and replay all tests from a fresh invocation.
- Recurrence guard: Tests bind generated artifact names and fields only after positive-cardinality discovery and targeted schema inspection.
- Rollback: Give the six-pass three-error run zero suite credit and leave the evidence candidate uncommitted.
- Witnesses: V6462-M18-F, V6462-M18-P

### V6462-M19 — Use generic D-first scratch roots in public runner sources

- Trigger: a staged runner source embeds an owner-bank path; the path is not required in a public artifact
- Method: Replace owner-bank scratch paths with a generic D-first scratch root while keeping all five scanner classes and constructed-fixture detection intact.
- Recurrence guard: Repository scripts use generic D-first scratch roots and never embed an owner archive or profile path.
- Rollback: Give the three-hit review zero evidence credit and do not commit the staged surface while any confirmed hit remains.
- Witnesses: V6462-M19-F, V6462-M19-P

### V6462-M20 — Require an empty index before evidence rebuild

- Trigger: a builder enforces an empty Git index; all staged paths are verified owner-scoped
- Method: Unstage only the verified owner-scoped surface, rebuild with an empty index, and restage the same bounded paths.
- Recurrence guard: Evidence builders run only after explicit expected-path review confirms an empty Git index; staging occurs afterward.
- Rollback: Leave worktree bytes unchanged, give the refusal zero credit, and never clear unrelated staged paths.
- Witnesses: V6462-M20-F, V6462-M20-P

### V6462-M21 — Defer terminal Method Flow aggregate use until recovery closes

- Trigger: a current recovery method remains candidate; the aggregate requires terminal Method Flow states
- Method: Defer terminal Method Flow aggregate use until the active recovery method has a bounded passing witness and terminal state.
- Recurrence guard: The ten-runner terminal aggregate is invoked only when the ledger contains no candidate or observed method.
- Rollback: Stop the aggregate, preserve all four outputs, and give all ten zero aggregate completion credit.
- Witnesses: V6462-M21-F, V6462-M21-P

### V6462-M22 — Quarantine original-phase commit-cap assertions in successor scope

- Trigger: successor commits extend an inherited phase history; inherited validators assert the original phase commit cap
- Method: Retain the two original-phase failures and run an explicit successor selection excluding only their phase-local commit-cap assertions.
- Recurrence guard: Successor scoped suites enumerate every exclusion by exact test ID and reason; excluded failures remain visible with zero pass credit.
- Rollback: Give the 65-pass two-failure broad run zero full-selection credit and do not alter inherited test code.
- Witnesses: V6462-M22-F, V6462-M22-P

### V6462-M23 — Bind scoped-test credit to the invoked revision

- Trigger: a receipt predates the commit it is later associated with; no exact-head invocation was recorded
- Method: Keep precommit candidate results unbound to later commits and require exact-head plus clean-state checks for canonical scoped credit.
- Recurrence guard: A scoped-test receipt receives canonical credit only when its runner records the exact HEAD and required clean state during the invocation.
- Rollback: Withdraw exact-evidence credit additively and preserve the earlier candidate receipt as noncanonical evidence.
- Witnesses: V6462-M23-F, V6462-M23-P

### V6462-M24 — Bind direct test-runner imports to the repository root

- Trigger: a family runner executes as a script; test modules are repository-root packages
- Method: Insert the resolved repository root into the import search path before direct-script unittest loading.
- Recurrence guard: Direct family test runners establish the repository root as an explicit import origin before module discovery.
- Rollback: Give the six loader errors zero test credit and do not weaken the selected module list.
- Witnesses: V6462-M24-F, V6462-M24-P

### V6462-M25 — Bound PowerShell startup probes to the measured envelope

- Trigger: a read-only PowerShell probe has a ten-second bound; local startup overhead is not yet characterized
- Method: Split read-only probes, disable login-shell startup, and use a bounded window matched to the observed PowerShell startup envelope.
- Recurrence guard: Use decomposed login-disabled PowerShell probes with an explicit sixty-second ceiling when the measured startup envelope exceeds ten seconds.
- Rollback: Give both timed-out probes zero evidence credit and make no repository or host-state claim from them.
- Witnesses: V6462-M25-F1, V6462-M25-F2, V6462-M25-P

### V6462-M26 — Keep ripgrep globs out of Windows path arguments

- Trigger: ripgrep runs on Windows; the intended search targets a filename family
- Method: Search the containing directory with ripgrep's explicit glob filter or pass explicit file paths.
- Recurrence guard: On Windows, pass a real directory to ripgrep and use -g for filename selection rather than embedding a wildcard in the path argument.
- Rollback: Give the failed diagnostic zero evidence credit and do not infer absence from an invalid-path search.
- Witnesses: V6462-M26-F, V6462-M26-F2, V6462-M26-P

### V6462-M27 — Resolve installed skill entrypoints before invocation

- Trigger: an installed skill runner is required; the exact runner filename has not been resolved
- Method: Enumerate the installed skill package and invoke the entrypoint that actually exists.
- Recurrence guard: Resolve installed skill entrypoints from the selected skill package before invocation; never infer a runner filename from the skill name.
- Rollback: Give the missing-entrypoint invocation zero index credit and leave the existing index unchanged.
- Witnesses: V6462-M27-F, V6462-M27-P

### V6462-M28 — Separate native commands from PowerShell summary objects

- Trigger: a PowerShell summary includes a native-command result; the result needs an exit code
- Method: Run native commands before object construction, capture their exit codes in scalar variables, and build the summary only from those values.
- Recurrence guard: Never embed compound native-command statements inside PowerShell hashtable value expressions; evaluate and store them first.
- Rollback: Give the parser-failed wrapper zero staged-review credit and make no inference from it.
- Witnesses: V6462-M28-F, V6462-M28-P

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
