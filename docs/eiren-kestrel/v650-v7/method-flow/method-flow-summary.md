# GHC Family Method Flow State

- Phase: v650-v7
- Owner: Eiren Kestrel
- Methods: 10
- Passing witnesses: 10
- Failed witnesses retained: 11

## Preferred methods

### V6507-M01 — Materialize PowerShell foreach results before downstream conversion

- Trigger: A PowerShell statement-level foreach block is followed by a pipeline in the same expression.
- Method: Accumulate each term result in an explicit array and pipe that completed array to JSON conversion after the loop.
- Recurrence guard: When a PowerShell foreach statement produces structured rows, assign those rows to an array before applying a downstream pipeline.
- Rollback: Give the rejected wrapper zero novelty-audit credit and leave the repository source state unchanged.
- Witnesses: V6507-M01-WFAIL, V6507-M01-WPASS, V6507-M01-WFAIL2

### V6507-M02 — Inspect installed CLI subcommand help before constructing validation calls

- Trigger: A phase invokes a local skill runner whose current argument schema has not been read in the same phase.
- Method: Read the exact installed subcommand help first, then invoke only its declared arguments and inspect the generated receipt.
- Recurrence guard: Treat remembered CLI options as unverified until the current installed --help output confirms them.
- Rollback: Give the rejected validation call zero credit and retain its failure before constructing a corrected call.
- Witnesses: V6507-M02-WFAIL, V6507-M02-WPASS

### V6507-M03 — Resolve historical artifact paths before direct reads

- Trigger: A predecessor phase may use a different directory or filename layout for a requested artifact.
- Method: Use a bounded filename or content search first, then read only an exact resolved path or the current skill schema.
- Recurrence guard: Never infer phase-local artifact paths from a neighboring phase without an existence or indexed-search witness.
- Rollback: Give the failed read zero inspection credit and leave the repository unchanged.
- Witnesses: V6507-M03-WFAIL, V6507-M03-WPASS

### V6507-M04 — Split authoritative schema reads from bounded recent-artifact searches

- Trigger: A discovery wrapper combines a repository-wide content search with an authoritative schema read.
- Method: Read the exact current schema directly, then search only the relevant recent phase roots with a separate bound.
- Recurrence guard: Do not attach a broad historical corpus search to an authoritative small-file read.
- Rollback: Give the timed-out wrapper zero evidence credit and leave repository state unchanged.
- Witnesses: V6507-M04-WFAIL, V6507-M04-WPASS

### V6507-M05 — Inspect exact line context before count-sensitive source patches

- Trigger: A patch targets long generated-style list lines whose wrapping may differ from the proposed context.
- Method: Read the exact target lines first and apply a smaller uniquely anchored replacement.
- Recurrence guard: Do not patch long list literals from remembered wrapping; anchor against the current file text.
- Rollback: Treat the rejected patch as zero change and preserve the pre-patch file unchanged.
- Witnesses: V6507-M05-WFAIL, V6507-M05-WPASS

### V6507-M06 — Run exact portfolio counts after every list adjustment

- Trigger: A count-sensitive portfolio list is edited by removing or restoring entries.
- Method: Restore one explicitly scoped refinement entry and rerun all five portfolio counts before generation.
- Recurrence guard: Use executable cardinality checks after list edits rather than mental subtraction.
- Rollback: Do not freeze or credit the mismatched portfolio; keep the preflight result as a failed witness.
- Witnesses: V6507-M06-WFAIL, V6507-M06-WPASS

### V6507-M07 — Regenerate count mirrors from the complete retained-negative source

- Trigger: New Method Flow failures were recorded after the phase-data negative list was first authored.
- Method: Append every later operational negative plus this failed test to the source list, regenerate the packet, and rerun the isolated x1 tests.
- Recurrence guard: Derive lifecycle count mirrors from the final pre-freeze Method Flow failure set, not an earlier hand-maintained snapshot.
- Rollback: Give the failed x1 test run zero pass credit and freeze no commit until the isolated scope passes.
- Witnesses: V6507-M07-WFAIL, V6507-M07-WPASS

### V6507-M08 — Assert generated workflow fields at their exact schema path

- Trigger: A test consumes generated workflow-refinement output whose nested shape has not been inspected.
- Method: Inspect the generated output keys and assert the confirmation flag at its exact nested path.
- Recurrence guard: Inspect generated JSON shape before asserting field placement, even when the field appears in runner console output.
- Rollback: Give the failed isolated test run zero successful-pass credit and change only the incorrect assertion.
- Witnesses: V6507-M08-WFAIL, V6507-M08-WPASS

### V6507-M09 — Compare manifests within their declared Git-blob hash domain

- Trigger: A manifest declares path-filtered Git blobs while Windows checkout bytes may use a different line-ending domain.
- Method: Inspect object-id, exact Git-blob bytes, and checkout bytes separately; validate each field only in its declared domain.
- Recurrence guard: Never compare a Git-blob SHA-256 field directly to unnormalized checkout bytes on Windows.
- Rollback: Give the failed aggregate zero pre-commit review credit and retain its mismatches before a corrected domain-aware review.
- Witnesses: V6507-M09-WFAIL, V6507-M09-WPASS

### V6507-M10 — Decode staged Git text explicitly as UTF-8 on Windows

- Trigger: An inline verifier reads staged UTF-8 JSON through subprocess text mode on a legacy Windows console codec.
- Method: Read git show output as bytes and decode every staged text blob explicitly with UTF-8.
- Recurrence guard: Never rely on the process default text codec for staged repository artifacts containing Maori or other Unicode text.
- Rollback: Give the failed aggregate zero staged-review credit and preserve the exact staged content unchanged until the corrected read.
- Witnesses: V6507-M10-WFAIL, V6507-M10-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
