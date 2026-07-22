# GHC Family Method Flow State

- Phase: v651-gmut-thos-v7-x1-x2
- Owner: Vesper Arlen
- Methods: 14
- Passing witnesses: 14
- Failed witnesses retained: 14

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

### V6517-M06 — Use transport-safe patch payloads

- Trigger: A patch carrier interprets content delimiters before apply_patch receives the patch.
- Method: Use a carrier representation with no unescaped delimiter or interpolation sequence.
- Recurrence guard: Preflight the transport representation before submitting a large patch.
- Rollback: Retain the failed owner-local attempt at zero credit and preserve every successfully created attributable file.
- Witnesses: V6517-M06-WFAIL, V6517-M06-WPASS

### V6517-M07 — Recover attributable partial skill initialization

- Trigger: The official initializer leaves a standard TODO skeleton but no agents metadata.
- Method: Inspect the partial tree, replace the template, and run the official metadata generator.
- Recurrence guard: Require SKILL.md, agents/openai.yaml, zero TODOs, and quick_validate success.
- Rollback: Retain the failed owner-local attempt at zero credit and preserve every successfully created attributable file.
- Witnesses: V6517-M07-WFAIL, V6517-M07-WPASS

### V6517-M08 — Do not reinitialize an existing partial skill

- Trigger: A diagnostic retry targets an existing skill directory.
- Method: Use the official generator and validator in place; initialize only absent directories.
- Recurrence guard: Check path existence before init_skill and never overwrite an existing skill directory.
- Rollback: Retain the failed owner-local attempt at zero credit and preserve every successfully created attributable file.
- Witnesses: V6517-M08-WFAIL, V6517-M08-WPASS

### V6517-M09 — Bind lifecycle tests to immutable commit trees

- Trigger: An x1-only test reads a mutable owner path after x2 artifacts exist.
- Method: Read x1-specific files and tree membership from the exact x1 Git object.
- Recurrence guard: Separate immutable lifecycle assertions from current-tree outcome assertions.
- Rollback: Retain the failed owner-local attempt at zero credit and preserve every successfully created attributable file.
- Witnesses: V6517-M09-WFAIL, V6517-M09-WPASS

### V6517-M10 — Credit only observable command outcomes

- Trigger: An asynchronous command result handle disappears before its output can be collected.
- Method: Assign zero credit to the unavailable result and run one directly observed bounded recovery.
- Recurrence guard: Use foreground execution or preserve a durable receipt before context boundaries.
- Rollback: Retain the failed owner-local attempt at zero credit and preserve every successfully created attributable file.
- Witnesses: V6517-M10-WFAIL, V6517-M10-WPASS

### V6517-M11 — Synchronize derived assertions with retained evidence

- Trigger: A retained failure changes Method Flow counts while a phase-local test still expects the earlier count.
- Method: Update derived assertions from the retained ledger after recording the failure.
- Recurrence guard: Regenerate evidence before testing and compare all counts to the frozen negative register.
- Rollback: Retain the failed owner-local attempt at zero credit and preserve every successfully created attributable file.
- Witnesses: V6517-M11-WFAIL, V6517-M11-WPASS

### V6517-M12 — Normalize validator diagnostics to JSON types

- Trigger: A validator records a Python set in its JSON diagnostic structure.
- Method: Sort set-like vocabularies into deterministic JSON arrays before comparison and emission.
- Recurrence guard: Reject non-JSON-native diagnostic values during validator construction.
- Rollback: Retain the failed owner-local attempt at zero credit and preserve every successfully created attributable file.
- Witnesses: V6517-M12-WFAIL, V6517-M12-WPASS

### V6517-M13 — Fail fast across native PowerShell commands

- Trigger: A PowerShell wrapper observes a native command failure but continues to a later successful command.
- Method: Inspect LASTEXITCODE after every native invocation and exit on the first failure.
- Recurrence guard: Use an explicit native-command fail-fast guard in every aggregate validation wrapper.
- Rollback: Retain the failed owner-local attempt at zero credit and preserve every successfully created attributable file.
- Witnesses: V6517-M13-WFAIL, V6517-M13-WPASS

### V6517-M14 — Reconcile manifests against the staged path domain

- Trigger: A commit-local manifest union differs from the exact staged path list.
- Method: Stage the intended set first, regenerate the self-excluding manifest, and compare both path domains exactly.
- Recurrence guard: Require zero Compare-Object differences before commit.
- Rollback: Retain the failed owner-local attempt at zero credit and preserve every successfully created attributable file.
- Witnesses: V6517-M14-WFAIL, V6517-M14-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
