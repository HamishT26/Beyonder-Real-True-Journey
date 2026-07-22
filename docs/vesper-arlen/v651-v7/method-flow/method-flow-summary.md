# GHC Family Method Flow State

- Phase: v651-gmut-thos-v7-x1-x2
- Owner: Vesper Arlen
- Methods: 5
- Passing witnesses: 5
- Failed witnesses retained: 5

## Preferred methods

### V6517-M01 — Quote PowerShell revision expressions

- Trigger: A PowerShell argument contains @{u} and can be transformed before process launch.
- Method: Pass the entire Git revision expression as one quoted argument.
- Recurrence guard: Always quote revision expressions containing PowerShell metacharacters.
- Rollback: Retain the failed read-only attempt at zero credit; no Git mutation requires rollback.
- Witnesses: V6517-M01-WFAIL, V6517-M01-WPASS

### V6517-M02 — Resolve optional search roots before enumeration

- Trigger: A multi-root search contains a not-yet-created optional owner path.
- Method: Resolve roots first and pass only existing paths to rg.
- Recurrence guard: Separate required roots from optional roots and record verified absence explicitly.
- Rollback: Retain the failed read-only attempt at zero credit; no Git mutation requires rollback.
- Witnesses: V6517-M02-WFAIL, V6517-M02-WPASS

### V6517-M03 — Expand Windows wildcard paths before rg

- Trigger: A Windows rg invocation contains a wildcard path that the shell does not expand.
- Method: Resolve candidate files into an explicit path array and pass only concrete paths.
- Recurrence guard: Never rely on Unix-style wildcard expansion for Windows path arguments.
- Rollback: Retain the failed read-only attempt at zero credit; no Git mutation requires rollback.
- Witnesses: V6517-M03-WFAIL, V6517-M03-WPASS

### V6517-M04 — Store filtered manifest blobs before cat-file reads

- Trigger: A manifest computes a filtered blob identifier without writing it, then attempts a cat-file read.
- Method: Use git hash-object -w with the path filter before reading the exact blob.
- Recurrence guard: Bind blob storage, object read, byte count, and SHA-256 in one bounded manifest step.
- Rollback: Retain the failed read-only attempt at zero credit; no Git mutation requires rollback.
- Witnesses: V6517-M04-WFAIL, V6517-M04-WPASS

### V6517-M05 — Build commit-local manifests after final artifact writes

- Trigger: A manifest snapshot precedes a later write to one of its covered artifacts.
- Method: Complete all covered writes before building the self-excluding manifest.
- Recurrence guard: Treat manifest generation as the final content-producing step before staging.
- Rollback: Retain the failed read-only attempt at zero credit; no Git mutation requires rollback.
- Witnesses: V6517-M05-WFAIL, V6517-M05-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
