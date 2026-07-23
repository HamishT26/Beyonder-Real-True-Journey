# GHC Family Method Flow State

- Phase: v652-v2
- Owner: Orin Thale
- Methods: 14
- Passing witnesses: 14
- Failed witnesses retained: 0

## Preferred methods

### V6522-METHOD-01 — Derive the remote-tracking ref from the configured upstream

- Trigger: A branch name contains a hierarchical owner prefix; A four-way equality probe needs the configured remote-tracking ref
- Method: Resolve the full tracking ref with git rev-parse --symbolic-full-name @{u}, then resolve that exact ref and compare it with local, upstream, and live remote heads.
- Recurrence guard: Never derive a tracking ref by editing a branch-name string; ask Git for the configured upstream ref.
- Rollback: Stop after read-only output and leave refs, branches, worktrees, and remotes unchanged.
- Witnesses: V6522-WITNESS-01

### V6522-METHOD-02 — Bind manifest path parity to the immutable validator coverage predicate

- Trigger: A commit-local manifest covers documents plus phase-owned scripts or tests; A successor is rechecking sealed manifest parity without rerunning canonical validation
- Method: Read the immutable final validator coverage predicate, use full commit deltas for staged and delta manifests, and use the validator's owner-path predicate for owner manifests while checking exact Git blobs, byte counts, and SHA-256 values.
- Recurrence guard: Do not invent a directory-only path scope; bind successor checks to the sealed validator's explicit coverage predicate and immutable commits.
- Rollback: Stop after read-only output and leave repository bytes, refs, branches, worktrees, and remote state unchanged.
- Witnesses: V6522-WITNESS-02

### V6522-METHOD-03 — Bound repository searches before emitting matched content

- Trigger: A large inherited repository contains repetitive long-form phase packets; A search pattern can match both structured indices and narrative batons
- Method: Locate exact candidate files with rg --files and narrow structured queries to known JSON keys or bounded filenames before emitting content.
- Recurrence guard: Never use an unbounded content search as the primary proposal-index reader; resolve the exact structured artifact first.
- Rollback: Stop after read-only output and leave repository bytes and Git state unchanged.
- Witnesses: V6522-WITNESS-03

### V6522-METHOD-04 — Inspect structured-artifact keys before indexing arrays

- Trigger: A successor consumes an inherited JSON artifact with phase-specific naming; The expected array key has not been confirmed
- Method: Read only the top-level property names first, then bind the novelty reader to the observed array key and validate the declared count.
- Recurrence guard: Do not index an inherited JSON member before checking its exact key and type.
- Rollback: Stop after read-only output and leave repository bytes and Git state unchanged.
- Witnesses: V6522-WITNESS-04

### V6522-METHOD-05 — Discover novelty-audit schema before reading thresholds and rows

- Trigger: A successor reuses an inherited novelty-audit artifact; The exact audit row and threshold keys have not been inspected
- Method: Inspect top-level keys and types first, then bind candidate similarity checks to the observed fields while independently preserving manual mechanism review.
- Recurrence guard: Treat phase-specific novelty schemas as data to inspect, not a universal proposals-key contract.
- Rollback: Stop after read-only output and leave repository and Git state unchanged.
- Witnesses: V6522-WITNESS-05

### V6522-METHOD-06 — Split startup evidence probes into attributable bounded commands

- Trigger: A startup audit combines repository topology, long artifact content, and file enumeration; The wrapper has a bounded output or time budget
- Method: Run no-profile probes separately, emit only bounded summaries, and retain each exit status with its own evidence domain.
- Recurrence guard: Do not group long artifact reads with topology checks; isolate each probe and cap emitted fields.
- Rollback: Stop after the failed wrapper and rerun only smaller read-only probes.
- Witnesses: V6522-WITNESS-06

### V6522-METHOD-07 — Fetch official protocol sources in bounded units

- Trigger: Several long primary specifications are requested; Only title, status, and bounded mechanism anchors are needed
- Method: Open one primary specification at a time with short response bounds and record only the exact source facts required by the proposal ledger.
- Recurrence guard: Do not batch many long specifications into one response when a bounded title-and-section receipt suffices.
- Rollback: Discard the unattributable combined response and retain no source credit until an isolated read passes.
- Witnesses: V6522-WITNESS-07

### V6522-METHOD-08 — Avoid all-or-nothing parallel shell evidence collection

- Trigger: Independent shell probes have different startup or output costs; The orchestration layer rejects a promise group on one failure
- Method: Use isolated no-profile commands with individual timeouts and retain each result independently.
- Recurrence guard: Do not make independent evidence probes share one all-or-nothing promise when one slow startup can discard the others.
- Rollback: Let the failed wrapper terminate, then rerun each read-only probe independently with login disabled.
- Witnesses: V6522-WITNESS-08

### V6522-METHOD-09 — Measure the generated overview against its declared floor before freeze credit

- Trigger: An overview has a declared minimum word floor; The generator can materialize before its terminal acceptance check
- Method: Add a substantive evidence-domain paragraph, measure the function output directly, and rerun only after it exceeds the floor.
- Recurrence guard: Check the exact generated overview word count before treating the packet builder as a passing witness.
- Rollback: Keep the failed materialization uncommitted, add no outcome, and revise only the under-floor document surface.
- Witnesses: V6522-WITNESS-09

### V6522-METHOD-10 — Use exact bounded patch hunks for lifecycle source edits

- Trigger: A source edit targets a long generated string near the end of a file; The patch contains multiple distant hunks or manually prefixed markers
- Method: Split the change into small exact-context apply_patch operations, inspect the bounded target lines, and parse the full source before execution.
- Recurrence guard: Never prefix a hunk marker as added content; parse the source after each nontrivial patch and split failed context repairs.
- Rollback: Keep the source uncommitted, remove only the literal patch debris, and preserve all other owner content.
- Witnesses: V6522-WITNESS-10

### V6522-METHOD-11 — Pin UTF-8 before Unicode-emitting source diagnostics

- Trigger: A Windows process may emit Unicode text; The inherited console encoding can be CP1252
- Method: Set PYTHONUTF8 and PYTHONIOENCODING to UTF-8 before rerunning the bounded diagnostic.
- Recurrence guard: Pin UTF-8 before any diagnostic that may emit Maori or other non-ASCII text.
- Rollback: Discard the incomplete output and rerun only the same read-only diagnostic with explicit UTF-8.
- Witnesses: V6522-WITNESS-11

### V6522-METHOD-12 — Reject patch inputs that add hunk markers as file content

- Trigger: A hand-composed patch updates multiple files; Hunk marker lines are embedded in a string payload
- Method: Inspect patch syntax before execution, ensure hunk markers are unprefixed control lines, apply exact bounded contexts, and parse every changed source.
- Recurrence guard: Reject any patch payload where a line intended as a hunk marker begins with an added-content prefix.
- Rollback: Keep all changes uncommitted, remove only literal diff debris, and preserve intended owner content.
- Witnesses: V6522-WITNESS-12

### V6522-METHOD-13 — Use literal searches for literal diff-marker postflight

- Trigger: The target strings are fixed patch markers; Regex metacharacter escaping adds no value
- Method: Use fixed-string search and model the expected empty result as a successful zero-hit outcome.
- Recurrence guard: Prefer fixed-string search for exact control tokens and handle exit one as expected empty output.
- Rollback: Discard the parser-failed search and rerun only an exact literal probe.
- Witnesses: V6522-WITNESS-13

### V6522-METHOD-14 — Quarantine exact privacy-receipt scanner definitions in staged scans

- Trigger: A staged privacy receipt contains scanner class names or definitions; The postflight scans all staged UTF-8 files
- Method: Add the exact privacy receipt path to the scanner-definition set while leaving every other path subject to confirmed-hit adjudication.
- Recurrence guard: Explicitly identify self-referential scanner receipts before classifying their pattern vocabulary as payload.
- Rollback: Award zero staged-scan credit, change only the definition allowlist, and rerun the same exact staged inputs.
- Witnesses: V6522-WITNESS-14

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
