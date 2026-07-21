# GHC Family Method Flow State

- Phase: v651-v5
- Owner: Eiren Kestrel
- Methods: 19
- Passing witnesses: 19
- Failed witnesses retained: 19

## Preferred methods

### V6515-M01 — Bounded recovery method 01: Use SHA256.Create().ComputeHash and dispose the hasher after each bounded byte-domain verification

- Trigger: PowerShell 5.1 did not expose the static SHA256 HashData helper used by the first immutable-manifest verifier.
- Method: Use SHA256.Create().ComputeHash and dispose the hasher after each bounded byte-domain verification.
- Recurrence guard: Use SHA256.Create().ComputeHash and dispose the hasher after each bounded byte-domain verification.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6515-M01-WFAIL, V6515-M01-WPASS

### V6515-M02 — Bounded recovery method 02: Separate optional searches from required reads and treat the documented no-match status explicitly

- Trigger: An optional ripgrep manifest-name search returned its normal no-match exit code and made a combined wrapper appear failed.
- Method: Separate optional searches from required reads and treat the documented no-match status explicitly.
- Recurrence guard: Separate optional searches from required reads and treat the documented no-match status explicitly.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6515-M02-WFAIL, V6515-M02-WPASS

### V6515-M03 — Bounded recovery method 03: Read the manifest schema and declared phase prefix before comparing exactly the 353 source-owner paths

- Trigger: The first source owner-manifest probe inferred the owner scope too broadly and compared 378 paths with a 353-path phase manifest.
- Method: Read the manifest schema and declared phase prefix before comparing exactly the 353 source-owner paths.
- Recurrence guard: Read the manifest schema and declared phase prefix before comparing exactly the 353 source-owner paths.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6515-M03-WFAIL, V6515-M03-WPASS

### V6515-M04 — Bounded recovery method 04: Use the immutable prior_proposals plus new_proposals arrays and assert their combined 980-row length

- Trigger: The first novelty-index probe assumed a generic rows key and failed before returning a count.
- Method: Use the immutable prior_proposals plus new_proposals arrays and assert their combined 980-row length.
- Recurrence guard: Use the immutable prior_proposals plus new_proposals arrays and assert their combined 980-row length.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6515-M04-WFAIL, V6515-M04-WPASS

### V6515-M05 — Bounded recovery method 05: Collect the foreach result in a variable before formatting or emitting it

- Trigger: A PowerShell foreach expression was piped directly into formatting and produced an empty-pipe parser error.
- Method: Collect the foreach result in a variable before formatting or emitting it.
- Recurrence guard: Collect the foreach result in a variable before formatting or emitting it.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6515-M05-WFAIL, V6515-M05-WPASS

### V6515-M06 — Bounded recovery method 06: Resolve the explicit upstream ref first and pass that literal ref to each Git command

- Trigger: A wrapper mangled the upstream shorthand ref expression while collecting four-way equality evidence.
- Method: Resolve the explicit upstream ref first and pass that literal ref to each Git command.
- Recurrence guard: Resolve the explicit upstream ref first and pass that literal ref to each Git command.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6515-M06-WFAIL, V6515-M06-WPASS

### V6515-M07 — Bounded recovery method 07: Discover the official or primary source through search before opening the returned safe reference

- Trigger: A direct open of an unprimed official documentation URL was rejected by the browsing safety boundary.
- Method: Discover the official or primary source through search before opening the returned safe reference.
- Recurrence guard: Discover the official or primary source through search before opening the returned safe reference.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6515-M07-WFAIL, V6515-M07-WPASS

### V6515-M08 — Bounded recovery method 08: Run compilation as the required gate and report an optional zero-hit search independently

- Trigger: A combined required compile and optional stale-label scan returned exit 1 solely because the correct stale-label result was empty.
- Method: Run compilation as the required gate and report an optional zero-hit search independently.
- Recurrence guard: Run compilation as the required gate and report an optional zero-hit search independently.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6515-M08-WFAIL, V6515-M08-WPASS

### V6515-M09 — Bounded recovery method 09: Use smaller exact-context patches, verify every bounded edit, and retain the failed patch with zero credit

- Trigger: A broad multi-file patch failed exact-context verification at one proposal sentence and applied no changes.
- Method: Use smaller exact-context patches, verify every bounded edit, and retain the failed patch with zero credit.
- Recurrence guard: Use smaller exact-context patches, verify every bounded edit, and retain the failed patch with zero credit.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6515-M09-WFAIL, V6515-M09-WPASS

### V6515-M10 — Bounded recovery method 10: Run compilation, optional stale-label review, diff hygiene, and Git state as separate bounded checks

- Trigger: A combined post-edit compile, stale-label, and Git-state audit exceeded its wrapper before yielding attributable sub-results.
- Method: Run compilation, optional stale-label review, diff hygiene, and Git state as separate bounded checks.
- Recurrence guard: Run compilation, optional stale-label review, diff hygiene, and Git state as separate bounded checks.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6515-M10-WFAIL, V6515-M10-WPASS

### V6515-M11 — Bounded recovery method 11: Replace P18 with a manually reviewed adaptive radix tree tribunal, rerun all 980 comparisons, and do not weaken the novelty threshold

- Trigger: The first x1 generator stopped at the semantic novelty gate because proposal P18 repeated an inherited quotient-filter mechanism.
- Method: Replace P18 with a manually reviewed adaptive radix tree tribunal, rerun all 980 comparisons, and do not weaken the novelty threshold.
- Recurrence guard: Replace P18 with a manually reviewed adaptive radix tree tribunal, rerun all 980 comparisons, and do not weaken the novelty threshold.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6515-M11-WFAIL, V6515-M11-WPASS

### V6515-M12 — Bounded recovery method 12: Use the declared family skill runners, retain the partial test at zero aggregate credit, and rerun only the isolated blocker before the complete x1 set

- Trigger: The first isolated x1 test run passed seven of eight tests but found that workflow, reflection, and Method Flow outputs had not yet been materialized from their planned inputs.
- Method: Use the declared family skill runners, retain the partial test at zero aggregate credit, and rerun only the isolated blocker before the complete x1 set.
- Recurrence guard: Use the declared family skill runners, retain the partial test at zero aggregate credit, and rerun only the isolated blocker before the complete x1 set.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6515-M12-WFAIL, V6515-M12-WPASS

### V6515-M13 — Bounded recovery method 13: Read each required skill independently and use only the exact runner paths named by its instructions

- Trigger: A combined repository-wide output search and two required skill reads timed out because the broad search dominated the wrapper.
- Method: Read each required skill independently and use only the exact runner paths named by its instructions.
- Recurrence guard: Read each required skill independently and use only the exact runner paths named by its instructions.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6515-M13-WFAIL, V6515-M13-WPASS

### V6515-M14 — Bounded recovery method 14: Inspect the already-read Method Flow script and schema directly, then invoke its documented explicit build operation

- Trigger: A three-runner help wrapper returned two successful help texts but the Method Flow help process exceeded its bounded timeout.
- Method: Inspect the already-read Method Flow script and schema directly, then invoke its documented explicit build operation.
- Recurrence guard: Inspect the already-read Method Flow script and schema directly, then invoke its documented explicit build operation.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6515-M14-WFAIL, V6515-M14-WPASS

### V6515-M15 — Bounded recovery method 15: Use an explicit zero-hit branch for optional discovery and retain required inspections as separate commands

- Trigger: An optional script-name search returned the normal no-match status without its wrapper normalizing that result.
- Method: Use an explicit zero-hit branch for optional discovery and retain required inspections as separate commands.
- Recurrence guard: Use an explicit zero-hit branch for optional discovery and retain required inspections as separate commands.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6515-M15-WFAIL, V6515-M15-WPASS

### V6515-M16 — Bounded recovery method 16: Patch short stable anchors independently and verify each additive file before generation

- Trigger: A second broad multi-file patch failed exact-context verification on a long overview sentence and applied no changes.
- Method: Patch short stable anchors independently and verify each additive file before generation.
- Recurrence guard: Patch short stable anchors independently and verify each additive file before generation.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6515-M16-WFAIL, V6515-M16-WPASS

### V6515-M17 — Bounded recovery method 17: Resolve the installed skill engine through the portable compatibility wrapper, load its schema functions without invoking main, and retain this failed helper run

- Trigger: The first phase-local Method Flow helper imported the repository compatibility wrapper as a library, but that wrapper exposes only a command entrypoint.
- Method: Resolve the installed skill engine through the portable compatibility wrapper, load its schema functions without invoking main, and retain this failed helper run.
- Recurrence guard: Resolve the installed skill engine through the portable compatibility wrapper, load its schema functions without invoking main, and retain this failed helper run.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6515-M17-WFAIL, V6515-M17-WPASS

### V6515-M18 — Bounded recovery method 18: Run the already-read index skill's phase-scoped builder, retain the partial test at zero credit, and rerun only the blocker before the complete x1 set

- Trigger: The isolated workflow blocker test progressed through workflow, reflection, and Method Flow but found that the planned phase-scoped GHC Family Index receipt had not yet been built.
- Method: Run the already-read index skill's phase-scoped builder, retain the partial test at zero credit, and rerun only the blocker before the complete x1 set.
- Recurrence guard: Run the already-read index skill's phase-scoped builder, retain the partial test at zero credit, and rerun only the blocker before the complete x1 set.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6515-M18-WFAIL, V6515-M18-WPASS

### V6515-M19 — Bounded recovery method 19: Use the checked-in document-cap receipt and x1 test as the credited witnesses, then keep the faulty ad-hoc result at zero credit

- Trigger: An ad-hoc document word-count audit over-escaped its regular expression and incorrectly reported zero words.
- Method: Use the checked-in document-cap receipt and x1 test as the credited witnesses, then keep the faulty ad-hoc result at zero credit.
- Recurrence guard: Use the checked-in document-cap receipt and x1 test as the credited witnesses, then keep the faulty ad-hoc result at zero credit.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6515-M19-WFAIL, V6515-M19-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
