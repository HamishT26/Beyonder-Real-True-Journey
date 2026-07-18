# GHC Family Method Flow State

- Phase: v648-v8
- Owner: Sylven Arc
- Methods: 5
- Passing witnesses: 5
- Failed witnesses retained: 5

## Preferred methods

### v6488-m01 — Commit-manifest byte-domain discriminator

- Trigger: A commit-local manifest declares checkout_bytes_domain separately from git_blob identity.; Later commits may have changed files that were present in an earlier staged manifest.
- Method: Validate changed-path parity and Git object identity at the named commit, then use the retained staged-review receipt for checkout-domain byte parity instead of equating checkout bytes with raw blob size.
- Recurrence guard: Read hash_domain and checkout_bytes_domain before comparing sizes; never infer that the two byte domains are identical.
- Rollback: Discard the false mismatch conclusion and retain the failed probe as an operational negative.
- Witnesses: v6488-m01-wfail-01, v6488-m01-wpass-01

### v6488-m02 — Scanner-definition candidate discriminator

- Trigger: A scanner source file is included in the exact staged-file domain.; The source contains the literal patterns it is designed to detect.
- Method: Retain every raw candidate, inspect the matching source line, and classify only pattern-definition lines in the scanner itself as scanner-definition candidates rather than confirmed artifact leaks.
- Recurrence guard: Report candidate and confirmed-hit counts separately; never discard scanner self-matches without exact line-context classification.
- Rollback: Restore fail-closed classification if a candidate is outside an exact scanner-definition line.
- Witnesses: v6488-m02-wfail-01, v6488-m02-wpass-01

### v6488-m03 — Generated-JSON narrow patch recovery

- Trigger: A generated JSON artifact uses deterministic sorted keys.; The proposed patch context was inferred rather than read from the current file.
- Method: Read the exact bounded current snippet, patch source-of-truth code first, then patch or regenerate the artifact with minimal exact context.
- Recurrence guard: Inspect generated key order before patching and avoid broad multi-file contexts that depend on inferred serialization order.
- Rollback: No rollback is needed when apply_patch reports zero changes; retain the failed patch witness.
- Witnesses: v6488-m03-wfail-01, v6488-m03-wpass-01

### v6488-m04 — Lifecycle-stable x1 assertion

- Trigger: The same test module remains in the repository after x2 begins.; The test checks current path absence rather than immutable x1 truth and commit-local review evidence.
- Method: Assert the frozen x1 phase-truth flags and x1 staged-review x2 path count, which remain valid after later additive lifecycle files exist.
- Recurrence guard: Historical lifecycle tests must read frozen receipts, never infer prior state from the current later worktree.
- Rollback: Restore the exact x1 test from its commit if the receipt-based assertion no longer matches the frozen evidence.
- Witnesses: v6488-m04-wfail-01, v6488-m04-wpass-01

### v6488-m05 — Multi-file patch hunk grammar guard

- Trigger: One patch updates several files.; A hunk boundary is followed immediately by another file header without valid context.
- Method: Use one syntactically complete update hunk per file and validate each file header boundary before submitting the patch.
- Recurrence guard: Do not leave a bare hunk marker before the next file header; prefer smaller multi-file patches when contexts differ.
- Rollback: No rollback is required because patch parsing failed before mutation.
- Witnesses: v6488-m05-wfail-01, v6488-m05-wpass-01

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
