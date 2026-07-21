# GHC Family Method Flow State

- Phase: v651-v4
- Owner: Sylven Arc
- Methods: 15
- Passing witnesses: 15
- Failed witnesses retained: 15

## Preferred methods

### V6514-M01 — Bounded recovery method 01: Use an exact committed-path read or quote the revision expression before invoking Git

- Trigger: An unquoted revision type suffix was parsed as a Git option before source verification completed.
- Method: Use an exact committed-path read or quote the revision expression before invoking Git.
- Recurrence guard: Use an exact committed-path read or quote the revision expression before invoking Git.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6514-M01-WFAIL, V6514-M01-WPASS

### V6514-M02 — Bounded recovery method 02: Use isolated scalar state, history, live-remote, and storage probes

- Trigger: A broad parallel source and worktree probe exceeded its bounded wrapper without attributable aggregate output.
- Method: Use isolated scalar state, history, live-remote, and storage probes.
- Recurrence guard: Use isolated scalar state, history, live-remote, and storage probes.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6514-M02-WFAIL, V6514-M02-WPASS

### V6514-M03 — Bounded recovery method 03: Read only manifest metadata and bounded count fields rather than rendering entries

- Trigger: An overbroad manifest display exceeded the visible output budget.
- Method: Read only manifest metadata and bounded count fields rather than rendering entries.
- Recurrence guard: Read only manifest metadata and bounded count fields rather than rendering entries.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6514-M03-WFAIL, V6514-M03-WPASS

### V6514-M04 — Bounded recovery method 04: Use commit-path, Git-object, and object-size parity while retaining Tamar's sealed SHA replay as inherited evidence

- Trigger: A full byte-and-SHA source-manifest replay exceeded its 120-second envelope and received zero credit.
- Method: Use commit-path, Git-object, and object-size parity while retaining Tamar's sealed SHA replay as inherited evidence.
- Recurrence guard: Use commit-path, Git-object, and object-size parity while retaining Tamar's sealed SHA replay as inherited evidence.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6514-M04-WFAIL, V6514-M04-WPASS

### V6514-M05 — Bounded recovery method 05: Bind the corrected final-delta manifest to the corrected final head and keep the failed binding witness

- Trigger: The first final-delta parity witness bound that manifest to the retained first closeout and reported 34 path-object mismatches.
- Method: Bind the corrected final-delta manifest to the corrected final head and keep the failed binding witness.
- Recurrence guard: Bind the corrected final-delta manifest to the corrected final head and keep the failed binding witness.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6514-M05-WFAIL, V6514-M05-WPASS

### V6514-M06 — Bounded recovery method 06: Separate optional no-match searches from required reads and normalize the optional search exit code

- Trigger: A combined optional AGENTS search and required skill-read wrapper returned exit 1 on the no-match search and masked required outputs.
- Method: Separate optional no-match searches from required reads and normalize the optional search exit code.
- Recurrence guard: Separate optional no-match searches from required reads and normalize the optional search exit code.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6514-M06-WFAIL, V6514-M06-WPASS

### V6514-M07 — Bounded recovery method 07: Use quiet fast-forward output where possible and audit the resulting exact head and clean state instead of relying on the display

- Trigger: The successful fast-forward emitted an overlarge truncated path display.
- Method: Use quiet fast-forward output where possible and audit the resulting exact head and clean state instead of relying on the display.
- Recurrence guard: Use quiet fast-forward output where possible and audit the resulting exact head and clean state instead of relying on the display.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6514-M07-WFAIL, V6514-M07-WPASS

### V6514-M08 — Bounded recovery method 08: Inspect exported names explicitly and use the declared CLEAN_FIX_REFINE collection name

- Trigger: A bounded phase-data inventory probe referenced a nonexistent CFR abbreviation and failed before emitting any counts.
- Method: Inspect exported names explicitly and use the declared CLEAN_FIX_REFINE collection name.
- Recurrence guard: Inspect exported names explicitly and use the declared CLEAN_FIX_REFINE collection name.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6514-M08-WFAIL, V6514-M08-WPASS

### V6514-M09 — Bounded recovery method 09: Narrow the title and mechanism to ECDSA canonicalization-path, curve-specific multikey, raw-signature encoding, key-format rejection, and synthetic test-vector obligations, then rerun the full 960-proposal audit

- Trigger: The first deterministic novelty audit rejected proposal V6514-P08 because its generic Data Integrity title crossed the frozen-proposal token threshold.
- Method: Narrow the title and mechanism to ECDSA canonicalization-path, curve-specific multikey, raw-signature encoding, key-format rejection, and synthetic test-vector obligations, then rerun the full 960-proposal audit.
- Recurrence guard: Narrow the title and mechanism to ECDSA canonicalization-path, curve-specific multikey, raw-signature encoding, key-format rejection, and synthetic test-vector obligations, then rerun the full 960-proposal audit.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6514-M09-WFAIL, V6514-M09-WPASS

### V6514-M10 — Bounded recovery method 10: Enumerate the required skill's scripts and invoke the exact ghc_family_method_flow_state.py entry point

- Trigger: A help probe used a nonexistent abbreviated Method Flow runner filename and Python returned file-not-found before any Method Flow operation began.
- Method: Enumerate the required skill's scripts and invoke the exact ghc_family_method_flow_state.py entry point.
- Recurrence guard: Enumerate the required skill's scripts and invoke the exact ghc_family_method_flow_state.py entry point.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6514-M10-WFAIL, V6514-M10-WPASS

### V6514-M11 — Bounded recovery method 11: Guard each optional existence check explicitly and keep required inspections in separate attributable commands

- Trigger: A combined optional generated-artifact inspection returned exit 1 because absent optional outputs were not normalized independently.
- Method: Guard each optional existence check explicitly and keep required inspections in separate attributable commands.
- Recurrence guard: Guard each optional existence check explicitly and keep required inspections in separate attributable commands.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6514-M11-WFAIL, V6514-M11-WPASS

### V6514-M12 — Bounded recovery method 12: Restrict compatibility edits to explicit current-phase fields, regenerate the chain from the immutable prior index, and verify inherited proposal identifiers remain unchanged

- Trigger: The first copied preregistration template pass left stale owner and schema labels and its broad compatibility rewrite altered inherited V6513 proposal identifiers in the frozen-chain index.
- Method: Restrict compatibility edits to explicit current-phase fields, regenerate the chain from the immutable prior index, and verify inherited proposal identifiers remain unchanged.
- Recurrence guard: Restrict compatibility edits to explicit current-phase fields, regenerate the chain from the immutable prior index, and verify inherited proposal identifiers remain unchanged.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6514-M12-WFAIL, V6514-M12-WPASS

### V6514-M13 — Bounded recovery method 13: Read the exact UTF-8 context and apply smaller bounded patches with verified anchors

- Trigger: Two additive patch attempts used stale or mojibake-sensitive context and failed verification without changing files.
- Method: Read the exact UTF-8 context and apply smaller bounded patches with verified anchors.
- Recurrence guard: Read the exact UTF-8 context and apply smaller bounded patches with verified anchors.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6514-M13-WFAIL, V6514-M13-WPASS

### V6514-M14 — Bounded recovery method 14: Use fixed-string inspection for literal labels and reserve regular expressions for separately validated patterns

- Trigger: A stale-label inspection used a malformed regular expression and returned a parser error before scanning.
- Method: Use fixed-string inspection for literal labels and reserve regular expressions for separately validated patterns.
- Recurrence guard: Use fixed-string inspection for literal labels and reserve regular expressions for separately validated patterns.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6514-M14-WFAIL, V6514-M14-WPASS

### V6514-M15 — Bounded recovery method 15: Preserve the immutable rows, publish a collision register with stable row evidence, require every v651-v4 identifier to remain outside the inherited identifier set, and never rewrite predecessor history

- Trigger: The immutable 960-row predecessor index was found to contain twenty duplicated V6513 proposal identifiers across distinct inherited titles.
- Method: Preserve the immutable rows, publish a collision register with stable row evidence, require every v651-v4 identifier to remain outside the inherited identifier set, and never rewrite predecessor history.
- Recurrence guard: Preserve the immutable rows, publish a collision register with stable row evidence, require every v651-v4 identifier to remain outside the inherited identifier set, and never rewrite predecessor history.
- Rollback: Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.
- Witnesses: V6514-M15-WFAIL, V6514-M15-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
