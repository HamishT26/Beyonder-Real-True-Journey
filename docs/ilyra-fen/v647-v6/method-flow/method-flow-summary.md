# GHC Family Method Flow State

- Phase: v647-gmut-thos-v6-x1-x2
- Owner: Ilyra Fen
- Methods: 18
- Passing witnesses: 18
- Failed witnesses retained: 18

## Preferred methods

### V6476-M01 — Bounded full skill read after short-wrapper timeout

- Trigger: A required local instruction file has not yet been read to EOF and the short wrapper timed out.
- Method: Inventory the exact file with a bounded fast probe, then read the unchanged file in full with a 60-second wrapper.
- Recurrence guard: Do not repeat the same short wrapper; preserve every timeout and verify EOF content before task action.
- Rollback: Stop the bounded probe, retain the failure, and return to the last clean repository state without external mutation.
- Witnesses: V6476-M01-WFAIL, V6476-M01-WPASS

### V6476-M02 — Explicit remote-ref revision-range equality

- Trigger: A Git equality range uses an upstream expression inside PowerShell command text.
- Method: Resolve or name the full remote-tracking ref explicitly and pass that ref to Git revision-range commands.
- Recurrence guard: Never embed an unquoted upstream hashtable-like expression in a PowerShell revision range.
- Rollback: Stop the bounded probe, retain the failure, and return to the last clean repository state without external mutation.
- Witnesses: V6476-M02-WFAIL, V6476-M02-WPASS

### V6476-M03 — Built-in JSON parser fallback without installation

- Trigger: JSON inspection is required and the optional utility is not already installed.
- Method: Use the platform built-in JSON parser under explicit UTF-8 and deterministic output; do not install unrelated software.
- Recurrence guard: Probe utility availability once, then select the built-in parser and retain the missing-tool event.
- Rollback: Stop the bounded probe, retain the failure, and return to the last clean repository state without external mutation.
- Witnesses: V6476-M03-WFAIL, V6476-M03-WPASS

### V6476-M04 — Exact portfolio collision quarantine before materialization

- Trigger: Current safe-task skill runner cleanup exact or blocked titles are audited against inherited portfolios.
- Method: Stop before materialization, rename or rewrite exact collisions, and rerun the unchanged normalized-title audit.
- Recurrence guard: Require zero inherited and zero within-current exact collisions before generating phase artifacts.
- Rollback: Stop the bounded probe, retain the failure, and return to the last clean repository state without external mutation.
- Witnesses: V6476-M04-WFAIL, V6476-M04-WPASS

### V6476-M05 — Non-self-matching forbidden-credit scanner definition

- Trigger: The scanner source is included in the staged surface it reviews.
- Method: Construct the same forbidden sequence from adjacent byte fragments while leaving target matching unchanged.
- Recurrence guard: Forward-test every literal scanner needle against its own source before staged review credit.
- Rollback: Stop the bounded probe, retain the failure, and return to the last clean repository state without external mutation.
- Witnesses: V6476-M05-WFAIL, V6476-M05-WPASS

### V6476-M06 — Case-normalized natural-language accessibility assertion

- Trigger: A test checks a natural-language reservation phrase whose capitalization may differ only because of sentence position.
- Method: Normalize both the structural report text and the expected reservation phrase with Unicode casefold before asserting presence.
- Recurrence guard: Use exact case only for case-significant syntax; use Unicode casefold for natural-language reservation phrases.
- Rollback: Restore the original assertion, retain the failure, and keep accessibility-complete claims false.
- Witnesses: V6476-M06-WFAIL, V6476-M06-WPASS

### V6476-M07 — Refresh derived failure mirrors before aggregate rerun

- Trigger: A new operational negative or witness has been added since the last generated evidence build.
- Method: Complete the focused recovery witness, refresh all authoritative and derived negative and Method Flow counts, then run the aggregate test selection.
- Recurrence guard: Before aggregate reruns, compare authoritative failure count, derived total, and Method Flow fail and pass witness counts.
- Rollback: Stop the aggregate rerun, retain its failed assertions, and return to the last consistent generated ledger set.
- Witnesses: V6476-M07-WFAIL, V6476-M07-WPASS

### V6476-M08 — Independent receipts for slow Windows probes

- Trigger: A combined or parallel wrapper includes Git status, metadata, or file reads that can exceed a short process budget.
- Method: Run slow repository and file probes as separate commands with independent timeouts and receipts.
- Recurrence guard: Give each potentially slow Windows repository probe its own process, timeout, and receipt; never infer success from a timed aggregate wrapper.
- Rollback: Discard all evidence credit from the timed wrapper and rerun only the required probes independently.
- Witnesses: V6476-M08-WFAIL, V6476-M08-WPASS

### V6476-M09 — Windows-safe exact-path inspection

- Trigger: A local inspection command would pass a wildcard path directly to a cross-platform executable.
- Method: Use ripgrep file discovery or an exact LiteralPath instead of passing a PowerShell wildcard as a literal ripgrep path.
- Recurrence guard: Discover files with rg --files and filter them, or inspect an exact file with LiteralPath.
- Rollback: Give the failed wildcard command zero evidence credit and rerun an exact bounded file probe.
- Witnesses: V6476-M09-WFAIL, V6476-M09-WPASS

### V6476-M10 — Explicit-note Method Flow state promotion

- Trigger: A validated Method Flow method is ready for a state transition.
- Method: Supply a concise bounded --note value whenever promoting a Method Flow method state.
- Recurrence guard: Preflight required CLI options and always include an evidence-bounded promotion note.
- Rollback: Retain the parser failure, leave the method unpromoted, and retry only after recording the missing-option guard.
- Witnesses: V6476-M10-WFAIL, V6476-M10-WPASS

### V6476-M11 — Fail-closed generated-receipt path verification

- Trigger: A generated count or receipt must be verified from a repository artifact.
- Method: Discover generated artifact paths first, set PowerShell errors to terminating, and reject null required fields.
- Recurrence guard: Resolve the exact artifact path, use ErrorActionPreference Stop, and fail if any required field is null.
- Rollback: Give the null-bearing probe zero evidence credit and rerun only against discovered exact paths with fail-closed field checks.
- Witnesses: V6476-M11-WFAIL, V6476-M11-WPASS

### V6476-M12 — Pre-launch UTF-8 pin for Unicode diagnostics

- Trigger: A Python process may print te reo Māori or other non-ASCII text on Windows.
- Method: Set PYTHONUTF8=1 before launching any console diagnostic that may emit non-ASCII text.
- Recurrence guard: Pin UTF-8 in the child-process environment before launch; never delete or transliterate culturally correct text to satisfy a locale-dependent console.
- Rollback: Retain the encoding failure, give the command zero pass credit, and rerun the unchanged inputs under explicit UTF-8.
- Witnesses: V6476-M12-WFAIL, V6476-M12-WPASS

### V6476-M13 — Repository-root binding for in-process unittest loading

- Trigger: A validation runner loads repository test modules in-process from a script below the repository root.
- Method: Insert the repository root at the front of sys.path before loading named repository test modules in-process.
- Recurrence guard: Bind named test loading to the exact repository root before constructing the unittest suite.
- Rollback: Retain the three import errors, give the failed selection zero test credit, and retry only after repository-root binding.
- Witnesses: V6476-M13-WFAIL, V6476-M13-WPASS

### V6476-M14 — Explicit-valid gate for validation-runner credit

- Trigger: A generated portfolio grants invocation credit from a validation receipt.
- Method: Parse the validation receipt and grant runner credit only when its explicit valid field is true.
- Recurrence guard: Never infer a passing runner from file existence; parse the declared success field and fail closed on malformed or absent receipts.
- Rollback: Keep runner invocation credit false until an explicit valid receipt exists.
- Witnesses: V6476-M14-WFAIL, V6476-M14-WPASS

### V6476-M15 — Sanitized failing-test identifiers in validation receipts

- Trigger: A bounded unittest selection can fail inside a validation runner.
- Method: Persist sanitized failing test identifiers in the bounded validation receipt before returning nonzero.
- Recurrence guard: Include sanitized test identifiers, not private traces or paths, in every failed bounded-test receipt.
- Rollback: Retain the opaque failure receipt and run one bounded diagnostic selection; do not infer the failing assertions.
- Witnesses: V6476-M15-WFAIL, V6476-M15-WPASS

### V6476-M16 — Immutable x1 Git-blob binding for historical cardinalities

- Trigger: An x1-only test examines an artifact designed to grow append-only during x2.
- Method: Load immutable x1 cardinality evidence from the exact frozen x1 Git blob rather than the advanced working-tree ledger.
- Recurrence guard: Evaluate historical x1 cardinalities from the frozen x1 commit object; use the current tree only for append-only lifecycle checks.
- Rollback: Retain the failed advanced-tree assertion and restore the test if exact x1 Git-blob loading cannot be demonstrated.
- Witnesses: V6476-M16-WFAIL, V6476-M16-WPASS

### V6476-M17 — Exact domain-wrapper staged allowlist

- Trigger: A phase stages family-current domain wrappers whose names are frozen in its runner plan.
- Method: Enumerate the nine intended family-current domain wrappers explicitly in the staged-review allowlist.
- Recurrence guard: Use an exact wrapper filename set rather than a broad scripts prefix, preserving rejection of unrelated sibling or historical files.
- Rollback: Retain the failed nine-path review and remove any wrapper not present in the frozen runner plan.
- Witnesses: V6476-M17-WFAIL, V6476-M17-WPASS

### V6476-M18 — Single-newline source-file termination

- Trigger: Exact staged diff hygiene reports a blank line at end of a newly added source file.
- Method: Remove only the extra terminal blank line and rerun exact staged diff hygiene.
- Recurrence guard: Require exactly one terminating newline and no extra blank line in generated or patched source files.
- Rollback: Retain the diff-hygiene failure and keep the evidence commit blocked until the exact staged check passes.
- Witnesses: V6476-M18-WFAIL, V6476-M18-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
