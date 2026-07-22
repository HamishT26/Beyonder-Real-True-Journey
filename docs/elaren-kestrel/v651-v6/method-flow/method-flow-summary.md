# GHC Family Method Flow State

- Phase: v651-v6
- Owner: Elaren Kestrel
- Methods: 5
- Passing witnesses: 5
- Failed witnesses retained: 5

## Preferred methods

### V6516-M01 — Complete buffered Git-blob read

- Trigger: A line-limited downstream consumer closes a Git content stream before the producer finishes.
- Method: Capture the complete blob once, verify size or line count, and then inspect bounded in-memory slices.
- Recurrence guard: Use buffered object reads before any presentation limiter.
- Rollback: Discard only the truncated display and repeat the read without mutating Git.
- Witnesses: V6516-M01-WFAIL, V6516-M01-WPASS

### V6516-M02 — Attribute zero-result tree filters

- Trigger: A repository tree filter returns no rows and a nonzero grep-style status.
- Method: Capture the tree listing and apply an explicit zero-result-safe match.
- Recurrence guard: Separate tree acquisition from optional filtering.
- Rollback: Give the empty filter zero evidence credit and preserve the underlying tree.
- Witnesses: V6516-M02-WFAIL, V6516-M02-WPASS

### V6516-M03 — Use tracked index for optional instruction discovery

- Trigger: A no-match file search is misclassified as a tool fault.
- Method: Query the tracked-file index and distinguish verified absence from execution failure.
- Recurrence guard: Use git ls-files for tracked optional control files.
- Rollback: Retain the no-match command and stop if the tracked index itself cannot be read.
- Witnesses: V6516-M03-WFAIL, V6516-M03-WPASS

### V6516-M04 — Accumulate PowerShell loop output before piping

- Trigger: Windows PowerShell rejects a foreach block followed immediately by a pipeline.
- Method: Append records to an array and pipe only the completed array.
- Recurrence guard: Avoid direct loop-to-pipeline syntax under Windows PowerShell 5.1.
- Rollback: Retain the parser failure; no repository state needs rollback.
- Witnesses: V6516-M04-WFAIL, V6516-M04-WPASS

### V6516-M05 — Preserve live policy over a legacy compatibility projection

- Trigger: The installed workflow runner encodes narrower historical caps than the live activation baton.
- Method: Retain the authoritative failed audit and validate only immediate route structure with a marked compatibility projection.
- Recurrence guard: Never present compatibility validation as validation of newer live policy values.
- Rollback: Stop route execution if the compatibility projection also fails; never silently narrow the live plan.
- Witnesses: V6516-M05-WFAIL, V6516-M05-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
