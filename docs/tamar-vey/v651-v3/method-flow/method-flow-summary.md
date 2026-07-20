# GHC Family Method Flow State

- Phase: v651-v3
- Owner: Tamar Vey
- Methods: 14
- Passing witnesses: 14
- Failed witnesses retained: 14

## Preferred methods

### V6513-M01 — Bounded recovery method 01: Read each required skill and reference in bounded direct calls and require complete EOF evidence

- Trigger: A sequential four-skill read wrapper timed out after the first file.
- Method: Read each required skill and reference in bounded direct calls and require complete EOF evidence.
- Recurrence guard: Read each required skill and reference in bounded direct calls and require complete EOF evidence.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6513-M01-WFAIL, V6513-M01-WPASS

### V6513-M02 — Bounded recovery method 02: Use scalar lane, path, head, status, and equality probes for the owned and source lanes

- Trigger: A broad worktree inventory returned overlarge truncated output.
- Method: Use scalar lane, path, head, status, and equality probes for the owned and source lanes.
- Recurrence guard: Use scalar lane, path, head, status, and equality probes for the owned and source lanes.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6513-M02-WFAIL, V6513-M02-WPASS

### V6513-M03 — Bounded recovery method 03: Read exact bounded line ranges through the known final line and require EOF

- Trigger: A combined full-baton read was truncated and received no complete-read credit.
- Method: Read exact bounded line ranges through the known final line and require EOF.
- Recurrence guard: Read exact bounded line ranges through the known final line and require EOF.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6513-M03-WFAIL, V6513-M03-WPASS

### V6513-M04 — Bounded recovery method 04: Audit head, status, divergence, upstream, tracking, and fresh live remote before any retry

- Trigger: The fast-forward wrapper produced overlarge truncated output although the operation completed.
- Method: Audit head, status, divergence, upstream, tracking, and fresh live remote before any retry.
- Recurrence guard: Audit head, status, divergence, upstream, tracking, and fresh live remote before any retry.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6513-M04-WFAIL, V6513-M04-WPASS

### V6513-M05 — Bounded recovery method 05: Discover bounded commit-tree paths before reading the exact final truth files

- Trigger: A phase-truth path was assumed at the inherited phase root and did not exist.
- Method: Discover bounded commit-tree paths before reading the exact final truth files.
- Recurrence guard: Discover bounded commit-tree paths before reading the exact final truth files.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6513-M05-WFAIL, V6513-M05-WPASS

### V6513-M06 — Bounded recovery method 06: Inspect the top-level schema and combine prior_proposals with new_proposals

- Trigger: The frozen chain index was assumed to expose a proposals key and null indexing failed.
- Method: Inspect the top-level schema and combine prior_proposals with new_proposals.
- Recurrence guard: Inspect the top-level schema and combine prior_proposals with new_proposals.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6513-M06-WFAIL, V6513-M06-WPASS

### V6513-M07 — Bounded recovery method 07: Query only targeted title terms and retain the full index as immutable input

- Trigger: A broad JSON rendering of all 940 proposals was truncated.
- Method: Query only targeted title terms and retain the full index as immutable input.
- Recurrence guard: Query only targeted title terms and retain the full index as immutable input.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6513-M07-WFAIL, V6513-M07-WPASS

### V6513-M08 — Bounded recovery method 08: Collect rows in an explicit result array, then serialize the bounded result

- Trigger: A PowerShell foreach pipeline form failed to parse before the novelty audit ran.
- Method: Collect rows in an explicit result array, then serialize the bounded result.
- Recurrence guard: Collect rows in an explicit result array, then serialize the bounded result.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6513-M08-WFAIL, V6513-M08-WPASS

### V6513-M09 — Bounded recovery method 09: Use one bounded rg file inventory and separate scalar probes

- Trigger: A parallel four-command inventory wrapper timed out without attributable aggregate output.
- Method: Use one bounded rg file inventory and separate scalar probes.
- Recurrence guard: Use one bounded rg file inventory and separate scalar probes.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6513-M09-WFAIL, V6513-M09-WPASS

### V6513-M10 — Bounded recovery method 10: Enumerate the exact phase-local method-flow root and read named files there

- Trigger: Method Flow records and witnesses were assumed to live in nonexistent subdirectories.
- Method: Enumerate the exact phase-local method-flow root and read named files there.
- Recurrence guard: Enumerate the exact phase-local method-flow root and read named files there.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6513-M10-WFAIL, V6513-M10-WPASS

### V6513-M11 — Bounded recovery method 11: Replace every repeated mechanism with genuinely distinct surfaces and rerun the unchanged threshold against all 940 predecessors

- Trigger: The first formal all-940 novelty build rejected three proposals and mechanism review exposed two more repeated surfaces.
- Method: Replace every repeated mechanism with genuinely distinct surfaces and rerun the unchanged threshold against all 940 predecessors.
- Recurrence guard: Replace every repeated mechanism with genuinely distinct surfaces and rerun the unchanged threshold against all 940 predecessors.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6513-M11-WFAIL, V6513-M11-WPASS

### V6513-M12 — Bounded recovery method 12: Do not delete the phase directory; use deterministic overwrite of declared generated files and exact staged review

- Trigger: A proposed recursive cleanup wrapper was blocked before execution by command policy.
- Method: Do not delete the phase directory; use deterministic overwrite of declared generated files and exact staged review.
- Recurrence guard: Do not delete the phase directory; use deterministic overwrite of declared generated files and exact staged review.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6513-M12-WFAIL, V6513-M12-WPASS

### V6513-M13 — Bounded recovery method 13: Preserve the historical input alias for caller compatibility while publishing the v651-v3 all-940 novelty field

- Trigger: The reused predecessor builder expected its historical novelty-key name and stopped before completing the freeze.
- Method: Preserve the historical input alias for caller compatibility while publishing the v651-v3 all-940 novelty field.
- Recurrence guard: Preserve the historical input alias for caller compatibility while publishing the v651-v3 all-940 novelty field.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6513-M13-WFAIL, V6513-M13-WPASS

### V6513-M14 — Bounded recovery method 14: Bind the threat-model novelty control to all 940 inherited proposals and regenerate the exact staged manifest

- Trigger: Exact staged stale-label review found one all-940 predecessor label in the generated threat model.
- Method: Bind the threat-model novelty control to all 940 inherited proposals and regenerate the exact staged manifest.
- Recurrence guard: Bind the threat-model novelty control to all 940 inherited proposals and regenerate the exact staged manifest.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6513-M14-WFAIL, V6513-M14-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
