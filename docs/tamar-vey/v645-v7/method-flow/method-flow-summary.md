# GHC Family Method Flow State

- Phase: v645-gmut-thos-v7-x1-x2
- Owner: Tamar Vey
- Methods: 9
- Passing witnesses: 9
- Failed witnesses retained: 9

## Preferred methods

### V6457-M01 — Increase only the schema-read envelope after retaining the first timeout

- Trigger: required local schema; first bounded read returned no content
- Method: Retain the timeout, widen only the read envelope, and require complete content before task action.
- Recurrence guard: Never infer schema content from silence or discard the first timed-out attempt.
- Rollback: Keep task action paused until a complete read succeeds.
- Witnesses: V6457-W01-F, V6457-W01-P

### V6457-M02 — Split D-drive and worktree inventory after a silent composite timeout

- Trigger: large linked-worktree repository; composite inventory returned no evidence
- Method: Decompose slow startup inventory into independently evidenced read-only probes.
- Recurrence guard: Do not rerun broad worktree enumeration when exact owned paths are already known.
- Rollback: Make no branch change until all required split probes pass.
- Witnesses: V6457-W02-F, V6457-W02-P

### V6457-M03 — Avoid the PowerShell automatic Matches table in proposal-audit collections

- Trigger: Windows PowerShell; regex-driven structured audit
- Method: Reserve automatic PowerShell variables and use explicit collection names in structured audits.
- Recurrence guard: Never use Matches as an accumulator after a regex condition.
- Rollback: Withdraw the failed query and rerun without changing repository artifacts.
- Witnesses: V6457-W03-F, V6457-W03-P

### V6457-M04 — Use search-discovered official pages after a direct URL safety rejection

- Trigger: official public source needed; direct browser open rejected
- Method: Prefer search-discovered official pages when direct URL canonicalization is rejected.
- Recurrence guard: A rejected direct open is not evidence and must not be silently replaced by an assumed URL.
- Rollback: Retain the failed open and use no source claim until an official result is returned.
- Witnesses: V6457-W04-F, V6457-W04-P

### V6457-M05 — Inspect runner subcommand help after a zero-match source-code search

- Trigger: delegating compatibility wrapper; narrow implementation search returned no matches
- Method: Use executable help as the source of truth when a compatibility wrapper delegates implementation.
- Recurrence guard: Do not treat zero text matches as proof that a delegated CLI lacks a capability.
- Rollback: Withdraw the source-search inference and make no ledger call until help succeeds.
- Witnesses: V6457-W05-F, V6457-W05-P

### V6457-M06 — Let the passing-witness transition stand before preferred promotion

- Trigger: canonical runner auto-promotes on passing witness; builder requests an explicit state transition
- Method: Treat a passing witness as the validated transition and request only the next legal state.
- Recurrence guard: Re-read method state after every witness command before issuing an explicit transition.
- Rollback: Stop the builder, preserve the partial ledger, and resume without deleting or duplicating evidence.
- Witnesses: V6457-W06-F, V6457-W06-P

### V6457-M07 — Normalize only phase-local family-index checkout text after CRLF detection

- Trigger: Windows family-index generation; owner-scoped UTF-8 LF requirement
- Method: Audit generated owner-scoped text bytes and normalize line endings without changing semantic content.
- Recurrence guard: Never stage family-index outputs on Windows before checking CRLF and visible encoding.
- Rollback: Restore the generated phase-local outputs if normalization changes decoded text and retain the failure.
- Witnesses: V6457-W07-F, V6457-W07-P

### V6457-M08 — Return validation evidence from separate commands when one parallel child may fail

- Trigger: multiple evidence-producing child commands; wrapper may fail fast on one nonzero exit
- Method: Separate evidence-producing validation commands when one expected failure could suppress another result.
- Recurrence guard: Parallelize only when the orchestration layer preserves every child result on partial failure.
- Rollback: Assign no credit to the suppressed run and rerun only the bounded validations independently.
- Witnesses: V6457-W08-F, V6457-W08-P

### V6457-M09 — Select the predecessor final test after its x2 artifacts exist

- Trigger: completed predecessor x2 packet; both x1-only and final scoped tests exist
- Method: Match a validation entrypoint to the artifact stage it was designed to test.
- Recurrence guard: Before invoking inherited tests, inspect whether the entrypoint asserts x1-only absence or final-packet presence.
- Rollback: Assign no credit to the stage-mismatched run and preserve both the test and completed predecessor artifacts.
- Witnesses: V6457-W09-F, V6457-W09-P

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
