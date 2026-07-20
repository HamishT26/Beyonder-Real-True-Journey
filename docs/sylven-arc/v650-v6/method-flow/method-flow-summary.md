# GHC Family Method Flow State

- Phase: v650-v6
- Owner: Sylven Arc
- Methods: 19
- Passing witnesses: 19
- Failed witnesses retained: 19

## Preferred methods

### V6506-M01 — Recover composite source verification timeout without erasing its failed witness

- Trigger: A bounded v650-v6 workflow exposes composite source verification timeout.
- Method: Split local ancestry and clean-state checks from the live remote lookup.
- Recurrence guard: Keep network lookup separate from local history and manifest checks.
- Rollback: Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6506-M01-WFAIL, V6506-M01-WPASS

### V6506-M02 — Recover per-blob manifest timeout without erasing its failed witness

- Trigger: A bounded v650-v6 workflow exposes per-blob manifest timeout.
- Method: Use one ls-tree map per commit and one git cat-file batch stream.
- Recurrence guard: Never use one child process per blob for large manifest verification.
- Rollback: Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6506-M02-WFAIL, V6506-M02-WPASS

### V6506-M03 — Recover broad worktree inventory timeout without erasing its failed witness

- Trigger: A bounded v650-v6 workflow exposes broad worktree inventory timeout.
- Method: Run one bounded inventory and retain only the exact owned branch and path mapping.
- Recurrence guard: Do not print or inspect unrelated sibling worktree blocks.
- Rollback: Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6506-M03-WFAIL, V6506-M03-WPASS

### V6506-M04 — Recover PowerShell automatic variable collision without erasing its failed witness

- Trigger: A bounded v650-v6 workflow exposes PowerShell automatic variable collision.
- Method: Use a non-reserved result variable name.
- Recurrence guard: Avoid Matches, Error, Input, and other automatic-variable names.
- Rollback: Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6506-M04-WFAIL, V6506-M04-WPASS

### V6506-M05 — Recover legacy console encoding without erasing its failed witness

- Trigger: A bounded v650-v6 workflow exposes legacy console encoding.
- Method: Set explicit UTF-8 input and output for Python audit processes.
- Recurrence guard: Set PYTHONIOENCODING and Python UTF-8 mode before Unicode audits.
- Rollback: Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6506-M05-WFAIL, V6506-M05-WPASS

### V6506-M06 — Recover stale compatibility filename without erasing its failed witness

- Trigger: A bounded v650-v6 workflow exposes stale compatibility filename.
- Method: Resolve compatibility filenames with rg before reading them.
- Recurrence guard: Never infer a historical builder name from another phase's naming pattern.
- Rollback: Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6506-M06-WFAIL, V6506-M06-WPASS

### V6506-M07 — Recover PowerShell version syntax mismatch without erasing its failed witness

- Trigger: A bounded v650-v6 workflow exposes PowerShell version syntax mismatch.
- Method: Use a PowerShell 5.1-compatible explicit conditional.
- Recurrence guard: Author host wrappers for the verified PowerShell major version.
- Rollback: Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6506-M07-WFAIL, V6506-M07-WPASS

### V6506-M08 — Recover empty search exit handling without erasing its failed witness

- Trigger: A bounded v650-v6 workflow exposes empty search exit handling.
- Method: Interpret a bounded no-match result as zero hits and verify freshness with a sorted note listing.
- Recurrence guard: Handle ripgrep exit one as an empty result only when stderr is empty and no match was expected.
- Rollback: Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6506-M08-WFAIL, V6506-M08-WPASS

### V6506-M09 — Recover stale inherited held-packet directory without erasing its failed witness

- Trigger: A bounded v650-v6 workflow exposes stale inherited held-packet directory.
- Method: Resolve the actual inherited checklist and exact-open-gate surfaces before creating a visibility pointer.
- Recurrence guard: Never infer an inherited packet directory from an older phase layout.
- Rollback: Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6506-M09-WFAIL, V6506-M09-WPASS

### V6506-M10 — Recover semantic novelty collision without erasing its failed witness

- Trigger: A bounded v650-v6 workflow exposes semantic novelty collision.
- Method: Retain the collision with zero proposal credit and replace it before freeze with a covariant Hamilton-Jacobi field-theory obligation board.
- Recurrence guard: Run the exact frozen-index collision gate before writing any x1 packet and retain rejected near-neighbor drafts.
- Rollback: Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6506-M10-WFAIL, V6506-M10-WPASS

### V6506-M11 — Recover second semantic novelty collision without erasing its failed witness

- Trigger: A bounded v650-v6 workflow exposes second semantic novelty collision.
- Method: Retain the collision with zero proposal credit and replace it before freeze with a target-trial emulation nonpromotion board.
- Recurrence guard: Treat a changed adjective list as non-novel when the causal design and protected gate are already frozen.
- Rollback: Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6506-M11-WFAIL, V6506-M11-WPASS

### V6506-M12 — Recover diagnostic wrapper timeout without erasing its failed witness

- Trigger: A bounded v650-v6 workflow exposes diagnostic wrapper timeout.
- Method: Credit neither the timed-out wrapper nor its partial output as a passing witness; split candidate search from status inspection.
- Recurrence guard: Do not append a broad status traversal to a diagnostic whose primary answer is already available.
- Rollback: Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6506-M12-WFAIL, V6506-M12-WPASS

### V6506-M13 — Recover preflight tuple tie comparison without erasing its failed witness

- Trigger: A bounded v650-v6 workflow exposes preflight tuple tie comparison.
- Method: Select the maximum with an explicit score key so tie handling never compares proposal dictionaries.
- Recurrence guard: Always provide a scalar key when ranking tuples whose later members are non-orderable records.
- Rollback: Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6506-M13-WFAIL, V6506-M13-WPASS

### V6506-M14 — Recover hidden target-trial semantic collision without erasing its failed witness

- Trigger: A bounded v650-v6 workflow exposes hidden target-trial semantic collision.
- Method: Retain both rejected P20 drafts and replace the mechanism with a front-door causal-identification nonpromotion board.
- Recurrence guard: Search hyphenated and compact mechanism variants, then run the complete frozen-index score before accepting a replacement.
- Rollback: Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6506-M14-WFAIL, V6506-M14-WPASS

### V6506-M15 — Recover Method Flow test schema assumption without erasing its failed witness

- Trigger: A bounded v650-v6 workflow exposes Method Flow test schema assumption.
- Method: Retain the failed test and inspect the required ledger schema before correcting the assertion to iterate list records and use result values.
- Recurrence guard: Test the committed schema shape directly; do not infer container types from identifiers.
- Rollback: Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6506-M15-WFAIL, V6506-M15-WPASS

### V6506-M16 — Recover mutation-plan path assumption without erasing its failed witness

- Trigger: A bounded v650-v6 workflow exposes mutation-plan path assumption.
- Method: Resolve the exact generated path and correct the assertion without moving or duplicating the artifact.
- Recurrence guard: Resolve generated artifact paths from the builder mapping before writing test fixtures.
- Rollback: Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6506-M16-WFAIL, V6506-M16-WPASS

### V6506-M17 — Recover overview length gate without erasing its failed witness

- Trigger: A bounded v650-v6 workflow exposes overview length gate.
- Method: Retain the short draft with zero delivery credit and expand the overview with phase scope, pillar, source, portfolio, failure, validation, accessibility, and authority boundaries.
- Recurrence guard: Measure the overview word count before staging instead of inferring adequacy from its section count.
- Rollback: Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6506-M17-WFAIL, V6506-M17-WPASS

### V6506-M18 — Recover stale generated narrative without erasing its failed witness

- Trigger: A bounded v650-v6 workflow exposes stale generated narrative.
- Method: Retain the stale draft with zero review credit and regenerate from the final x1 count and accepted covariant Hamilton-Jacobi mechanism.
- Recurrence guard: Run a stale-label and count scan after the final preregistration recovery, before staging.
- Rollback: Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6506-M18-WFAIL, V6506-M18-WPASS

### V6506-M19 — Recover credential-class privacy scan hit without erasing its failed witness

- Trigger: A bounded v650-v6 workflow exposes credential-class privacy scan hit.
- Method: Retain the failed scan with zero privacy credit and replace the literal with the sanitized phrase account-secret action without weakening the prohibition.
- Recurrence guard: Run the scanner against prose boundaries as well as data artifacts before manifest freeze.
- Rollback: Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6506-M19-WFAIL, V6506-M19-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
