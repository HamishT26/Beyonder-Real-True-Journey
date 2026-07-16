# GHC Family Method Flow State

- Phase: v646-gmut-thos-v7-x1-x2
- Owner: Eiren Kestrel
- Methods: 17
- Passing witnesses: 23
- Failed witnesses retained: 23

## Preferred methods

### V6467-M01 — Resolve frozen proposal collection from declared schema keys

- Trigger: inherited JSON index; unknown proposal collection field; PowerShell ConvertFrom-Json; partial output after runtime error
- Method: Inspect and record the frozen-index top-level keys first, then select the declared proposal collection by exact schema field and fail explicitly if it is absent.
- Recurrence guard: Never let a later successful PowerShell expression mask an earlier schema-access error; inspect declared keys and check every native or runtime failure before credit.
- Rollback: Give the partial probe zero novelty-audit credit, retain the null-array error, and rerun only the smallest key-first read-only query.
- Witnesses: V6467-M01-W-F, V6467-M01-W-P

### V6467-M02 — Serialize PowerShell loop results after explicit accumulation

- Trigger: PowerShell foreach loop; structured result objects; JSON serialization; read-only novelty audit
- Method: Accumulate PowerShell loop results in an explicit array and pipe that completed array to ConvertTo-Json after the loop.
- Recurrence guard: PowerShell loops that feed serialization must assign to an explicit results array; parser failures receive no downstream evidence credit.
- Rollback: Retain the parser failure, award zero novelty-search credit, and rerun only the corrected read-only loop.
- Witnesses: V6467-M02-W-F, V6467-M02-W-P

### V6467-M03 — Split login-shell startup from bounded filesystem and compiler probes

- Trigger: Windows PowerShell login shell; large Git worktree; short wrapper deadline; filesystem or compiler inspection
- Method: Disable login-shell initialization for bounded probes, use an already responsive neutral working directory, address the target by absolute path, and separate existence, content, and compilation checks.
- Recurrence guard: Do not retry an identical timed-out login-shell inspection; change one causal dimension, split the probe, and preserve the original timeout as a failed witness.
- Rollback: Award no inspection or compilation credit to either timeout and retain both wrapper expirations before using the bounded recovery.
- Witnesses: V6467-M03-W-F, V6467-M03-W-P

### V6467-M04 — Interrogate Method Flow subcommand help before receipt emission

- Trigger: Method Flow CLI; receipt refresh; locally guessed option name; partially completed command sequence
- Method: Read the exact validate and summarize subcommand help, use validate --receipt and summarize --json-output plus --markdown-output, and avoid replaying already successful append-only mutations.
- Recurrence guard: Treat each Method Flow subcommand as a separate contract; check help before first use and resume only from the first failed step.
- Rollback: Retain the parser failure, award no validation-receipt credit to it, and do not duplicate the preceding successful ledger events.
- Witnesses: V6467-M04-W-F, V6467-M04-W-P

### V6467-M05 — Fail closed and rename exact inherited portfolio collisions

- Trigger: expanded x1 portfolio; inherited portfolio corpus; exact normalized title collision; pre-materialization novelty gate
- Method: Emit each exact collision and source, rename the new designs around their phase-specific acceptance semantics, and rerun the unchanged counted audit before materialization.
- Recurrence guard: No quota, prefix, or nearby purpose earns novelty credit when a normalized portfolio title collides exactly with inherited work.
- Rollback: Write no x1 portfolio, retain the collision evidence, and change only the colliding declarations before rerunning the same audit.
- Witnesses: V6467-M05-W-F, V6467-M05-W-P

### V6467-M06 — Discover prior artifact names before reading a presumed ledger

- Trigger: inherited phase packet; unknown artifact filename; compound shell inspection; later successful output after an earlier path error
- Method: Enumerate bounded prior-phase filenames first, select the actual skill-build-use and runner-build-use receipts, and treat an earlier missing-path error as failure even when later commands succeed.
- Recurrence guard: Never infer an artifact filename from a conceptual label; discover the bounded file surface and stop compound-command success from masking an earlier error.
- Rollback: Give the presumed-path read zero reuse credit, retain the missing-path witness, and use only the discovered exact filenames.
- Witnesses: V6467-M06-W-F, V6467-M06-W-P

### V6467-M07 — Pin UTF-8 for console diagnostics containing Māori text

- Trigger: Windows console; Python stdout; Unicode source text; legacy code page
- Method: Set PYTHONIOENCODING=utf-8 for the bounded diagnostic, preserve UTF-8 source and artifacts, and rerun only the incomplete display.
- Recurrence guard: Any diagnostic expected to emit te reo Māori or other non-ASCII text must pin UTF-8 before Python starts; partial output earns no complete-review credit.
- Rollback: Retain the encoding exception, award no complete-list credit, and do not transliterate or remove the source text.
- Witnesses: V6467-M07-W-F, V6467-M07-W-P, V6467-M07-W-F2, V6467-M07-W-P2, V6467-M07-W-F3, V6467-M07-W-P3

### V6467-M08 — Bind x1 lifecycle assertions to the immutable x1 Git object

- Trigger: strict x1-before-x2 lifecycle; x1 tests rerun during x2; append-only Method Flow growth; live working-tree assertions
- Method: Check x2 absence against the exact x1 Git object and check x1 Method Flow records as a preserved identified subset while allowing later append-only methods and witnesses.
- Recurrence guard: Lifecycle tests must state whether their domain is an immutable commit or the current head; never infer historical contamination from legitimate additive later-phase files.
- Rollback: Retain the two-test failure, award no current-suite credit, and change only the time-domain assertions before rerunning the same 26 tests.
- Witnesses: V6467-M08-W-F, V6467-M08-W-P

### V6467-M09 — Classify complete-suite failures against an exact inherited exclusion set

- Trigger: complete repository discovery; phase-local historical assertions; exact inherited exclusion set; bounded diagnostic tail
- Method: Parse every FAIL and ERROR header, reserve only the two exact inherited v646-v1 commit-cap methods, bind the v646-v6 x1 absence check to its x1 Git object, and fail on any other event.
- Recurrence guard: A raw nonzero suite may earn eligible credit only when every event is named and belongs to the frozen exact exclusion set; exclusions cannot grow implicitly.
- Rollback: Retain the raw three-failure run, award no full-suite credit, and change only the unexpected lifecycle assertion plus diagnostic classification.
- Witnesses: V6467-M09-W-F, V6467-M09-W-P

### V6467-M10 — Bind historical route-state assertions to their lifecycle commit

- Trigger: x1 route-state assertion; live closeout tree; terminal route lifecycle; immutable x1 commit
- Method: Read the terminal route plan from the exact x1 Git object when testing x1 state, while testing the live HOLD state separately in closeout tests.
- Recurrence guard: Every state assertion must name its lifecycle commit or current-head domain; later truthful transitions never invalidate an earlier sealed state.
- Rollback: Retain the failed 33-test run, award no closeout validation credit, and change only the route-state time domain.
- Witnesses: V6467-M10-W-F, V6467-M10-W-P

### V6467-M11 — Validate Method Flow witness parity without assuming one pair per method

- Trigger: append-only Method Flow; repeated failure under one method; witness count assertion; closeout validation
- Method: Require exact method-ID coverage, failed/passing parity, and at least one pair per method while allowing additional retained recurrence witnesses.
- Recurrence guard: Witness counts may exceed method counts; tests must preserve repetitions instead of compressing them to one synthetic pair.
- Rollback: Retain the failed closeout run, award no validation credit, and replace only the invalid cardinality assumption.
- Witnesses: V6467-M11-W-F, V6467-M11-W-P

### V6467-M12 — Build final owner manifests from exact staged Git blobs

- Trigger: Windows autocrlf; generated index files; working-byte manifest; staged Git-blob verification
- Method: Stage the complete intended surface, regenerate only the final owner manifest from exact index blobs, stage that manifest, and rerun the unchanged review.
- Recurrence guard: Cross-worktree final identity uses Git blobs, never checkout bytes; line-ending normalization remains visible but cannot create false content drift.
- Rollback: Retain the two mismatches, award no staged closeout credit, and do not rewrite the index files merely to match a checkout hash domain.
- Witnesses: V6467-M12-W-F, V6467-M12-W-P, V6467-M12-W-F2, V6467-M12-W-P2

### V6467-M13 — Disposition exact-head audit regex literals as scanner definitions

- Trigger: five-class privacy scan; new scanner implementation; regex definition literals; filename-scoped disposition
- Method: Add the exact-head audit to the narrow scanner-definition filename set while leaving every other path and pattern unresolved by default.
- Recurrence guard: Only exact scanner implementation files may receive definition disposition; no general source-code or documentation exemption is allowed.
- Rollback: Retain all three candidates and the failed receipt, award no privacy-pass credit, and change only the exact scanner-file disposition.
- Witnesses: V6467-M13-W-F, V6467-M13-W-F2, V6467-M13-W-F3, V6467-M13-W-P, V6467-M13-W-P2, V6467-M13-W-P3, V6467-M13-W-F4, V6467-M13-W-P4

### V6467-M14 — Verify frozen x1 content against exact x1 Git blobs

- Trigger: clean named Windows worktree; x1 content seal; checkout line-ending filter; working-byte test
- Method: Read each of the seven frozen paths from the exact x1 commit and compare its Git-blob SHA-256 to the sealed value, independent of checkout filters.
- Recurrence guard: Historical content seals are always checked in their declared Git-object domain; clean checkout bytes never substitute for canonical blobs.
- Rollback: Retain the failed 33-test and 1,168-test named replay, award no replay credit, and correct only the seal test's hash domain.
- Witnesses: V6467-M14-W-F, V6467-M14-W-P

### V6467-M15 — Split large-tree correction inspection into exact bounded probes

- Trigger: large inherited Windows repository; recursive document-tree search; Git-status inspection in the same command; bounded command wrapper
- Method: Search only the exact correction files first, list relevant filenames separately, and run Git status as its own bounded probe.
- Recurrence guard: Do not combine recursive phase-tree searches with whole-worktree status checks when a narrow exact-file probe can answer the question.
- Rollback: Retain the timed-out attempt, award no evidence from it, and return to read-only exact-file probes.
- Witnesses: V6467-M15-W-F, V6467-M15-W-P

### V6467-M16 — Refresh every count-dependent closeout surface after ledger growth

- Trigger: append-only retained-negative growth; append-only Method Flow growth; generated closeout receipts; count-dependent current tests
- Method: Rebuild evidence registers first, rebuild closeout and final Method Flow mirrors second, verify the new totals directly, and only then rerun the unchanged current tests.
- Recurrence guard: Any retained-negative or Method Flow append invalidates every generated count mirror until the evidence and closeout builders refresh them together.
- Rollback: Retain the two-test failure, award no current-suite credit, and modify no frozen proposal or executed outcome.
- Witnesses: V6467-M16-W-F, V6467-M16-W-P

### V6467-M17 — Gate full-suite truth by exact exclusions instead of a frozen raw count

- Trigger: complete repository discovery; additive closeout tests; exact inherited exclusions; hardcoded historical suite cardinality
- Method: Require the raw suite to be at least the preregistered baseline, compute eligible tests as raw minus the exact named exclusions, and fail on any unexpected event.
- Recurrence guard: Additive tests may increase raw cardinality; only the exact exclusion identities, eligible arithmetic, and zero-unexpected-failure contract remain frozen.
- Rollback: Retain the one-test failure, award no current-suite credit, and change only the brittle raw-count assertion.
- Witnesses: V6467-M17-W-F, V6467-M17-W-P

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
