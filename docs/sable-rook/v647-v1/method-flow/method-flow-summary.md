# GHC Family Method Flow State

- Phase: v647-gmut-thos-v1-x1-x2
- Owner: Sable Rook
- Methods: 14
- Passing witnesses: 14
- Failed witnesses retained: 14

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

### V6471-M08 — Pin UTF-8 for skill-creator subprocesses

- Trigger: A phase-local skill contains Māori or other non-CP1252 text and system skill tools use Python text defaults.
- Method: Set PYTHONUTF8=1 and PYTHONIOENCODING=utf-8 for skill-creator initialization, metadata generation, and validation subprocesses.
- Recurrence guard: Pin UTF-8 for every skill-creator subprocess before it reads or emits Unicode content.
- Rollback: Keep the partial package phase-local, overwrite only its generated metadata after UTF-8 validation, and do not touch the global skill bank.
- Witnesses: V6471-M08-WFAIL, V6471-M08-WPASS

### V6471-M09 — Pin UTF-8 for family-runner stdout and summaries

- Trigger: A family runner prints phase content containing Māori or other non-CP1252 text.
- Method: Set PYTHONUTF8=1 and PYTHONIOENCODING=utf-8 for Method Flow validate and summarize commands, then verify both summary files parse or read.
- Recurrence guard: Pin UTF-8 before every family runner that may print phase text, not only skill-creator tools.
- Rollback: Retain the valid ledger and failed command, then regenerate only derived summaries under UTF-8.
- Witnesses: V6471-M09-WFAIL, V6471-M09-WPASS

### V6471-M10 — Bind historical x1 absence assertions to the immutable x1 commit

- Trigger: An x1-only test is rerun after x2 artifacts legitimately exist in the successor worktree.
- Method: Bind x1-only absence assertions to the immutable pushed x1 final commit instead of the successor working tree.
- Recurrence guard: Historical lifecycle absence tests must read the lifecycle commit, not infer absence from a later working tree.
- Rollback: Retain the failing 99-test run, patch only the lifecycle reference, and rerun the identical selection.
- Witnesses: V6471-M10-WFAIL, V6471-M10-WPASS

### V6471-M11 — Decompose shell-startup inspection into isolated bounded probes

- Trigger: Several read-only native and PowerShell inspections were grouped behind one shell startup.
- Method: Run independent login-disabled probes with a declared sixty-second upper bound and preserve each result separately.
- Recurrence guard: Use isolated probes for closeout evidence and never infer which grouped component completed after a wrapper timeout.
- Rollback: Retain the timeout; no repository mutation occurred, then retry only the isolated read-only probes.
- Witnesses: V6471-M11-WFAIL, V6471-M11-WPASS

### V6471-M12 — Enumerate phase-specific Method Flow artifact names before reading

- Trigger: A closeout tool needs the current phase Method Flow ledger and inherited naming may differ.
- Method: Enumerate the bounded phase root and select the exact method-flow-state.json artifact before reading it.
- Recurrence guard: Do not construct Method Flow filenames from a generic convention when an exact bounded enumeration is available.
- Rollback: Retain the failed lookup; it was read-only, then use the enumerated phase-specific path.
- Witnesses: V6471-M12-WFAIL, V6471-M12-WPASS

### V6471-M13 — Apply ripgrep globs through filters rather than Windows literal paths

- Trigger: A bounded source search needs filename filtering on Windows.
- Method: Search repository roots and express filename selection with repeated -g filters.
- Recurrence guard: Never pass a wildcard-bearing Windows pathname as a literal ripgrep search root.
- Rollback: Retain the failed read-only probe, then repeat the same pattern search with repository roots and glob filters.
- Witnesses: V6471-M13-WFAIL, V6471-M13-WPASS

### V6471-M14 — Resolve staged-review output paths before containment checks

- Trigger: A staged-review runner validates that every receipt path is contained beneath an absolute repository root.
- Method: Resolve each final staged-review receipt to an absolute path beneath the repository root before invoking the reviewer.
- Recurrence guard: Pass fully resolved owner-lane receipt paths to staged-review tools that enforce repository containment.
- Rollback: Retain the failed invocation; it wrote no receipt and changed no staged blob, then retry only with resolved in-repository paths.
- Witnesses: V6471-M14-WFAIL, V6471-M14-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
