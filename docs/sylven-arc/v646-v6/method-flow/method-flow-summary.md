# GHC Family Method Flow State

- Phase: v646-gmut-thos-v6-x1-x2
- Owner: Sylven Arc
- Methods: 10
- Passing witnesses: 10
- Failed witnesses retained: 10

## Preferred methods

### V6466-M01 — Use a bounded complete-file read after a short skill-read timeout

- Trigger: required complete skill read; short wrapper deadline; no returned content
- Method: Retry once with a bounded longer deadline and direct complete-file read; do not begin repository work until content is returned.
- Recurrence guard: Required skills and references must be read to EOF before repository commands; a timeout earns no partial credit.
- Rollback: Retain the negative and award no affected credit until the bounded recovery witness passes.
- Witnesses: V6466-M01-W-F, V6466-M01-W-P

### V6466-M02 — Split PowerShell probes before exit-code capture

- Trigger: PowerShell; native Git command; exit-code capture; compound expression
- Method: Run each native command separately, capture LASTEXITCODE on the following statement, then construct the summary object.
- Recurrence guard: Do not place native commands and LASTEXITCODE capture in one parenthesized expression.
- Rollback: Retain the negative and award no affected credit until the bounded recovery witness passes.
- Witnesses: V6466-M02-W-F, V6466-M02-W-P

### V6466-M03 — Use native include filters rather than Windows wildcard path operands

- Trigger: Windows; ripgrep; wildcard path operand; nested proposal corpus
- Method: Traverse the docs root and apply -g x1-proposals.json, then confirm the complete count with structured JSON parsing.
- Recurrence guard: On Windows, use tool-native include filters instead of shell-style wildcard path operands.
- Rollback: Retain the negative and award no affected credit until the bounded recovery witness passes.
- Witnesses: V6466-M03-W-F, V6466-M03-W-P

### V6466-M04 — Replace broad proposal text scans with a counted structured corpus audit

- Trigger: large inherited corpus; recursive text scan; semantic novelty; bounded deadline
- Method: Use structured JSON enumeration, exact count assertions, normalized-title collision checks, and bounded nearest-neighbor summaries.
- Recurrence guard: Do not award full-corpus novelty credit from a truncated text search.
- Rollback: Retain the negative and award no affected credit until the bounded recovery witness passes.
- Witnesses: V6466-M04-W-F, V6466-M04-W-P

### V6466-M05 — Constrain standards novelty searches to title fields before corpus confirmation

- Trigger: standards keyword search; large JSON corpus; common token; title novelty
- Method: Anchor the search to title fields, then confirm exact novelty through the structured 440-proposal audit.
- Recurrence guard: Common standards tokens in mission or boundary fields are not title-level semantic collisions.
- Rollback: Retain the negative and award no affected credit until the bounded recovery witness passes.
- Witnesses: V6466-M05-W-F, V6466-M05-W-P

### V6466-M06 — Separate large fast-forward movement from bounded equality proof

- Trigger: large inherited fast-forward; Git diffstat; bounded tool output
- Method: Treat the command exit as movement evidence only and run a separate bounded exact-ref and clean-state proof.
- Recurrence guard: A large transition display never substitutes for exact local/upstream/tracking/live equality.
- Rollback: Retain the negative and award no affected credit until the bounded recovery witness passes.
- Witnesses: V6466-M06-W-F, V6466-M06-W-P

### V6466-M07 — Enumerate and rewrite exact portfolio collisions before x1 materialization

- Trigger: expanded portfolio; prior title corpus; exact normalized collision; x1 freeze
- Method: Emit the exact colliding titles and sources, rewrite the new work with genuinely phase-specific semantics, and rerun the same audit before writing the packet.
- Recurrence guard: No prefix, quota, or inherited reuse earns novelty credit when the central title and purpose collide exactly.
- Rollback: Retain the negative and award no affected credit until the bounded recovery witness passes.
- Witnesses: V6466-M07-W-F, V6466-M07-W-P

### V6466-M08 — Read Method Flow witness counts from the emitted schema surface

- Trigger: Method Flow validation; derived counts; schema key; unit assertion
- Method: Read counts.witness_results.fail and counts.witness_results.pass and verify them against witness result values.
- Recurrence guard: Tests must validate emitted schema keys rather than locally guessed aliases.
- Rollback: Retain the negative and award no affected credit until the bounded recovery witness passes.
- Witnesses: V6466-M08-W-F, V6466-M08-W-P

### V6466-M09 — Declare reviewer dependencies before structural execution

- Trigger: new reviewer; standard-library dependency; structural check; first invocation
- Method: Add the exact missing import, preserve the failed invocation, and rerun the unchanged checks.
- Recurrence guard: Reviewer modules must import every runtime dependency and receive no credit from import-failed runs.
- Rollback: Retain the negative and award no affected credit until the bounded recovery witness passes.
- Witnesses: V6466-M09-W-F, V6466-M09-W-P

### V6466-M10 — Separate five-class scanner-definition candidates from confirmed payload hits

- Trigger: five-class privacy scan; scanner source; policy wording; embedded hyphenated skill name
- Method: Keep full-file coverage and every pattern class, add token boundaries, record candidate dispositions, and leave all other matches confirmed.
- Recurrence guard: Only exact scanner-definition, policy-exclusion, or proven embedded-name contexts may be dispositioned; files remain scanned and candidates remain counted.
- Rollback: Retain the negative and award no affected credit until the bounded recovery witness passes.
- Witnesses: V6466-M10-W-F, V6466-M10-W-P

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
