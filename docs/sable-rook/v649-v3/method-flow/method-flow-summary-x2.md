# GHC Family Method Flow State

- Phase: v649-gmut-thos-v3-x1-x2
- Owner: Sable Rook
- Methods: 11
- Passing witnesses: 11
- Failed witnesses retained: 14

## Preferred methods

### v6493-m01 — Bound and abandon an unresponsive memory-registry query

- Trigger: large memory registry; current live baton already supplies route truth
- Method: Stop after two bounded read-only attempts, retain both timeouts, use no memory-derived fact, and continue from immutable repository and live-remote evidence.
- Recurrence guard: Do not broaden or repeatedly scan the memory registry after two identical timeout envelopes.
- Rollback: Terminate the lookup, leave memory unchanged, and rely only on live source evidence for the phase.
- Witnesses: v6493-m01-wfail-a, v6493-m01-wfail-b, v6493-m01-wpass

### v6493-m02 — Decompose Windows startup preflight into single probes

- Trigger: slow D-drive; multiple Git and drive probes in one wrapper
- Method: Probe path, head, branch, clean state, equality, and drive headroom separately with bounded timeouts.
- Recurrence guard: Do not combine slow D-drive status and remote queries in one all-or-nothing wrapper.
- Rollback: Stop the combined wrapper, retain the timeout, and rerun only independent read-only probes.
- Witnesses: v6493-m02-wfail, v6493-m02-wpass

### v6493-m03 — Drain Git batch input and output atomically

- Trigger: hundreds of Git blobs; bidirectional subprocess pipes
- Method: Use subprocess communication that writes and drains atomically, then parse each declared blob and hash.
- Recurrence guard: Never manually fill a bidirectional batch pipe before draining its output.
- Rollback: Terminate the read-only process, retain the deadlock, and rerun with communicate-style I/O.
- Witnesses: v6493-m03-wfail, v6493-m03-wpass

### v6493-m04 — Inspect JSON keys before indexing a frozen ledger

- Trigger: heterogeneous phase ledgers; schema not yet inspected
- Method: Read top-level keys first, then inspect prior_proposals and new_proposals explicitly.
- Recurrence guard: Type-guard heterogeneous JSON and never index a guessed collection key.
- Rollback: Stop the read-only probe, preserve the schema-assumption failure, and retry only after key inspection.
- Witnesses: v6493-m04-wfail, v6493-m04-wpass

### v6493-m05 — Normalize expected-empty ripgrep exit state

- Trigger: read-only search; zero matches is an expected valid result
- Method: Capture output, accept exit codes 0 or 1, reject higher codes, and assert an explicit match count.
- Recurrence guard: Every expected-empty ripgrep probe must distinguish no-match from execution failure.
- Rollback: Stop after the ambiguous wrapper result; infer absence only from a zero-count recovery witness.
- Witnesses: v6493-m05-wfail, v6493-m05-wpass

### v6493-m06 — Summarize an exact staged surface without streaming its full path list

- Trigger: dozens of staged paths; bounded tool-output context; slow D-drive status traversal
- Method: Run diff hygiene separately, compute the staged-path count and deterministic SHA-256 digest in-process, report only unexpected paths, and rely on the exact staged manifest for content review.
- Recurrence guard: Do not stream a full staged path list when an exact manifest plus compact count, digest, and exception set provides the review evidence.
- Rollback: Stop the verbose wrapper, retain every failure, make no inference from truncated output, and rerun only the compact read-only review.
- Witnesses: v6493-m06-wfail-a, v6493-m06-wfail-b, v6493-m06-wpass

### v6493-m07 — Bind Method Flow tests to append-only structural invariants

- Trigger: append-only Method Flow ledger; new retained failure recorded before freeze
- Method: Assert stored counts against the actual method and witness collections, require the new method and retained-failure links explicitly, and retain exact state-result totals only at the immutable freeze.
- Recurrence guard: After any pre-freeze Method Flow addition, refresh every dependent assertion from the ledger before rerunning the suite.
- Rollback: Stop on the stale mirror, preserve the failed test, update only the owner-scoped assertion, and rerun after ledger validation.
- Witnesses: v6493-m07-wfail, v6493-m07-wpass

### v6493-m08 — Emit named PowerShell booleans for structural recovery checks

- Trigger: PowerShell 5.1; multiple structural assertions; machine-readable recovery receipt
- Method: Store each check in a named ordered dictionary, derive the failed-key list explicitly, and emit a compact object with the exact failures.
- Recurrence guard: Never rely on an anonymously constructed PowerShell boolean array for multi-check recovery evidence.
- Rollback: Stop on the collapsed result, preserve the wrapper failure, and rerun read-only with named fields.
- Witnesses: v6493-m08-wfail, v6493-m08-wpass

### v6493-m09 — Pass exact phase-local directories to the skill quick validator

- Trigger: official skill-creator quick validator; phase-local skill packages; no global installation
- Method: Read the official validator entrypoint, then invoke it with each exact phase-local skill directory as its sole positional argument.
- Recurrence guard: Invoke quick_validate.py only with one exact skill directory; inspect its source or skill instructions for usage instead of probing an unsupported help flag.
- Rollback: Stop after the read-only argument error, leave every package unchanged, and retry only with the exact documented positional form.
- Witnesses: v6493-m09-wfail, v6493-m09-wpass

### v6493-m10 — Decompose and time-budget exact staged reviews

- Trigger: more than 100 staged paths; exact Git-index manifest and privacy scan; slow D-drive traversal
- Method: Separate staging, exact staged review, and receipt staging; give the staged reviewer a timeout comfortably above its measured path-count runtime and report each exit independently.
- Recurrence guard: For staged surfaces above 100 paths, never combine all lifecycle steps in one opaque wrapper and budget at least twice the measured exact-review runtime.
- Rollback: Stop the opaque or timed-out wrapper, infer no pass from partial output, preserve the failure, and retry only the exact read-only stage with a larger bound.
- Witnesses: v6493-m10-wfail-a, v6493-m10-wfail-b, v6493-m10-wpass

### v6493-m11 — Run exact end-of-file hygiene before manifest refresh

- Trigger: new owner-scoped text or Python file; exact staged diff review; commit-local manifest pending
- Method: Run exact staged diff hygiene before manifest refresh; remove only the reported extra terminal line and verify the named file independently before the full review.
- Recurrence guard: Before regenerating a commit-local manifest, run exact staged diff hygiene and require one terminal newline with no extra blank line.
- Rollback: Stop before commit, preserve the failed diff witness, edit only the named owner-scoped line ending, and leave every sibling and x1 blob unchanged.
- Witnesses: v6493-m11-wfail, v6493-m11-wpass

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
