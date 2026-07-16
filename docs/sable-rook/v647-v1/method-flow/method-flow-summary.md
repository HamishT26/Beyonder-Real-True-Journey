# GHC Family Method Flow State

- Phase: v647-gmut-thos-v1-x1-x2
- Owner: Sable Rook
- Methods: 7
- Passing witnesses: 7
- Failed witnesses retained: 7

## Preferred methods

### V6471-M01 — Separate orchestration and shell language syntax before execution

- Trigger: A JavaScript tool-orchestration cell must carry a multiline PowerShell program.
- Method: Represent PowerShell as a JavaScript template string and keep native commands inside that string.
- Recurrence guard: Before execution, check that shell-only here-string tokens never appear at JavaScript top level.
- Rollback: Discard the rejected orchestration cell; no repository rollback is required because no nested command ran.
- Witnesses: V6471-M01-WFAIL, V6471-M01-WPASS, V6471-M01-WFAIL, V6471-M01-WPASS

### V6471-M02 — Enumerate exact phase paths before reading inherited artifacts

- Trigger: Inherited phases may preserve different compatibility filenames.
- Method: Run a bounded rg --files enumeration under the exact phase root, then read only discovered paths.
- Recurrence guard: Never infer a current artifact filename solely from an older sibling phase.
- Rollback: Discard the failed read assumption; no file mutation occurred.
- Witnesses: V6471-M02-WFAIL, V6471-M02-WPASS, V6471-M02-WFAIL, V6471-M02-WPASS

### V6471-M03 — Inspect Method Flow state after witnesses before explicit transitions

- Trigger: The family Method Flow runner may perform an automatic state transition after a passing witness.
- Method: After each passing witness, read the resulting method state and transition directly from validated to preferred only once.
- Recurrence guard: Do not assume a method remains candidate after the runner accepts a passing witness.
- Rollback: Keep the valid ledger state and discard only the rejected duplicate transition command.
- Witnesses: V6471-M03-WFAIL, V6471-M03-WPASS, V6471-M03-WFAIL, V6471-M03-WPASS

### V6471-M04 — Adjudicate explicit scanner-definition files before confirming privacy hits

- Trigger: A staged validation script contains the same byte patterns it is designed to detect.
- Method: Maintain an exact phase-local scanner-definition path set and still report every candidate with its disposition.
- Recurrence guard: Never suppress a candidate globally; definition status must match one exact reviewed script path.
- Rollback: Keep the failed privacy receipt, patch only the exact definition adjudication, and rerun the same staged blobs.
- Witnesses: V6471-M04-WFAIL, V6471-M04-WPASS, V6471-M04-WFAIL, V6471-M04-WPASS

### V6471-M05 — Bind measured rotation counts in the deterministic preregistration builder

- Trigger: A generated receipt is rerun after an out-of-band patch to one of its derived fields.
- Method: Move the verified inherited and owner-generated counts into the builder source, regenerate, and review the deterministic output.
- Recurrence guard: Never patch a generated count without updating its authoritative builder in the same lifecycle.
- Rollback: Discard the failed patch attempt; it changed no file, then regenerate from the corrected builder.
- Witnesses: V6471-M05-WFAIL, V6471-M05-WPASS, V6471-M05-WFAIL, V6471-M05-WPASS

### V6471-M06 — Build Git revision-path specifications without cross-language escape characters

- Trigger: A JavaScript template carries PowerShell that needs a Git revision:path argument.
- Method: Construct the revision and path with PowerShell string concatenation and pass the resulting variable to Git.
- Recurrence guard: Do not embed PowerShell backtick escapes inside JavaScript template strings.
- Rollback: Discard the rejected orchestration cell; no commit or Git command ran.
- Witnesses: V6471-M06-WFAIL, V6471-M06-WPASS, V6471-M06-WFAIL, V6471-M06-WPASS

### V6471-M07 — Verify exact Git blob bytes through a Python subprocess runner

- Trigger: Exact manifest parity requires byte-preserving Git blob reads on a host with inconsistent ProcessStartInfo APIs.
- Method: Use Python subprocess.check_output with an argument list for git cat-file blob and hash the returned bytes directly.
- Recurrence guard: Prefer the repository's byte-preserving manifest runner over host-specific PowerShell process APIs.
- Rollback: Keep the already-created x1 commit, add one bounded x1 repair commit, and do not rewrite history.
- Witnesses: V6471-M07-WFAIL, V6471-M07-WPASS, V6471-M07-WFAIL, V6471-M07-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
