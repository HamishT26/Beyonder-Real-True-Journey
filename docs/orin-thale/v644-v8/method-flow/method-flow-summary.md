# GHC Family Method Flow State

- Phase: v644-gmut-thos-v8-x1-x2
- Owner: Orin Thale
- Methods: 8
- Passing witnesses: 8
- Failed witnesses retained: 0

## Preferred methods

### V6448-M01 — Bounded single-surface audit after shared-envelope timeouts

- Trigger: large inherited checkout; recursive discovery and runner startup; shared or undersized command window; D-drive metadata latency
- Method: Run non-login, single-surface searches or allowlisted reads with independently measured windows and retain only complete child receipts.
- Recurrence guard: Never infer audit completion from a timed-out parent; separate recursive discovery from runner startup and preserve each completed witness independently.
- Rollback: Retain the failed receipts, make no evidentiary promotion from them, and return to the clean canonical lane before bounded read-only retries.
- Witnesses: V6448-M01-W01

### V6448-M02 — Literal-safe JSON field probes across PowerShell

- Trigger: orchestrator string literal; PowerShell command parsing; ripgrep regular expression; quoted JSON field names
- Method: Use an exact file and a single-quoted regex or fixed-string query, then inspect the complete result independently.
- Recurrence guard: Avoid layered backslash escaping for JSON key probes; validate one literal-safe pattern before combining search operations.
- Rollback: Retain the parser failure, make no repository inference from it, and rerun only after reducing the quoting layers.
- Witnesses: V6448-M02-W01

### V6448-M03 — One-language traversal for chained JSON indices

- Trigger: nested command-language parsers; inline Python source; f-string dictionary lookups; recursive JSON index traversal
- Method: Traverse the inherited-index chain in one PowerShell process, collecting records after recursion so order and count remain explicit.
- Recurrence guard: Use one parser for structured chain walks; if reusable complexity grows, implement a family-named committed runner rather than another inline multilanguage expression.
- Rollback: Retain the syntax fault, make no proposal-count claim from it, and rerun only with a single-language traversal.
- Witnesses: V6448-M03-W01

### V6448-M04 — Explicit collection before Windows PowerShell report pipelines

- Trigger: Windows PowerShell statement grammar; foreach output; JSON report serialization
- Method: Collect the foreach results in an explicit array and pipe that expression to the serializer.
- Recurrence guard: Use expression collection boundaries around statement output before pipelines on this host.
- Rollback: Retain the parser error, emit no similarity conclusion, and rerun only the corrected read-only report.
- Witnesses: V6448-M04-W01

### V6448-M05 — Case-sensitive ordered-pair compatibility scaffold

- Trigger: versioned compatibility copy; replacement tokens differing only by case; new destination files only
- Method: Require destination absence, copy only the predecessor scaffold, apply an ordered array of case-sensitive String.Replace pairs, and inspect all stale phase markers before semantic edits.
- Recurrence guard: Never use a case-insensitive dictionary for phase tokens that differ only by case; never promote a mechanical copy without explicit stale-marker and diff review.
- Rollback: If creation or inspection fails, retain the fault, remove no history, and leave the unpromoted new files out of the x1 commit until corrected.
- Witnesses: V6448-M05-W01

### V6448-M06 — Small exact-context semantic patches after mechanical rewrites

- Trigger: mechanically rewritten compatibility scaffold; multi-region semantic patch; mixed stale and current context
- Method: Read the current UTF-8 source and apply independent semantic regions with exact present context, then compile and inspect stale markers.
- Recurrence guard: Never assume predecessor context survives a version rewrite; keep semantic patch regions small and verify the resulting file before promotion.
- Rollback: An atomic rejection changes no file; retain the negative and retry only after exact source inspection.
- Witnesses: V6448-M06-W01

### V6448-M07 — UTF-8-exact patch regions independent of console rendering

- Trigger: non-ASCII source text; console rendering; copied patch context; combined unrelated regions
- Method: Patch ASCII regions separately, inspect the encoded source directly, and use a small exact-context change for the Unicode region.
- Recurrence guard: Never derive Unicode patch bytes from mojibake-prone output; validate UTF-8 transport before promotion.
- Rollback: An atomic rejection changes no file; retain the failure and retry only with exact encoded context.
- Witnesses: V6448-M07-W01

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
