# GHC Family Method Flow State

- Phase: v644-gmut-thos-v5-x1-x2
- Owner: Eiren Kestrel
- Methods: 8
- Passing witnesses: 8
- Failed witnesses retained: 1

## Preferred methods

### V6445-M01 — Bounded indexed and staged-content scanning

- Trigger: large repository; broad historical content search; exact public commit candidate
- Method: Discover paths with the Git index or file list, search only the bounded set, and scan the exact staged blobs before commit.
- Recurrence guard: Prefer bounded indexed discovery and require a zero-hit exact staged-content privacy scan before promotion.
- Rollback: Return to read-only file discovery and retain the timeout negative.
- Witnesses: V6445-M01-W01

### V6445-M02 — Separate package-version proof from locked cleanup

- Trigger: global CLI refresh while desktop process is active
- Method: Verify the installed CLI directly and defer deletion of any locked obsolete executable directory.
- Recurrence guard: Treat post-install cleanup warnings separately from version verification; never delete an in-use executable tree during an active desktop session.
- Rollback: Keep the verified CLI and leave locked cleanup to a later nonrunning-process window.
- Witnesses: V6445-M02-W01

### V6445-M03 — Schema introspection before pointer-chain query

- Trigger: evolving inherited pointer-chain schema
- Method: Read schema property names, recursively decode inherited pointers, and compare declared effective counts with unique IDs.
- Recurrence guard: Never guess collection field names across versioned artifacts.
- Rollback: Return to exact property inspection and retain the rejected query result.
- Witnesses: V6445-M03-W01

### V6445-M04 — Full inherited-source deduplication before slate freeze

- Trigger: new official source slate; inherited source pointer chain
- Method: Compare normalized titles and canonical URLs against every inherited source before adding a row.
- Recurrence guard: Run exact normalized-title and canonical-URL deduplication against the full inherited pointer chain before writing a source ledger.
- Rollback: Reuse the inherited source identifier and omit the duplicate addition.
- Witnesses: V6445-M04-W01

### V6445-M05 — Whole-file LF rematerialization for exact byte fixtures

- Trigger: named legacy byte fixture; automatic CRLF conversion; exact raw-hash warning branch
- Method: Recreate the complete small fixture from verified HEAD content through the patch tool, preserving the exact LF Git-blob bytes.
- Recurrence guard: For an exact byte-level fixture, rematerialize the complete file from verified repository content rather than patching one line to induce normalization.
- Rollback: Restore verified HEAD content and retain both failed hashes and isolated test results.
- Witnesses: V6445-M05-W00, V6445-M05-W01

### V6445-M06 — Explicit UTF-8 mode for Windows skill validation

- Trigger: UTF-8 skill text; validator without explicit encoding; legacy Windows code page
- Method: Run the validator under explicit Python UTF-8 mode without deleting or transliterating Māori wording.
- Recurrence guard: Use Python UTF-8 mode for local skill validators that do not declare an encoding.
- Rollback: Keep the skill unchanged and retain the decode failure if UTF-8 validation cannot run.
- Witnesses: V6445-M06-W01

### V6445-M07 — Non-circular evidence input contract

- Trigger: content manifest or staged validation receipt generated inside its own input dependency set
- Method: Declare generated outputs outside their own hash or validation dependency domain and regression-test the exclusion.
- Recurrence guard: Declare non-circular inputs for both content seals and staged validators before execution.
- Rollback: Discard the uncommitted circular seal and rebuild from the declared non-circular input set.
- Witnesses: V6445-M07-W01

### V6445-M08 — Additive lean companion with canonical rollback

- Trigger: large canonical repository; active sequential handoff; successor ancestry must remain valid
- Method: Build a D-first fresh local snapshot repository from the recent dependency closure while keeping the canonical repository authoritative.
- Recurrence guard: Check source revision, closure manifest, file limit, targeted tests, clean local commit, no public remote, and rollback before use.
- Rollback: Ignore or discard only the additive companion and continue from the unchanged canonical branch.
- Witnesses: V6445-M08-W01

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
