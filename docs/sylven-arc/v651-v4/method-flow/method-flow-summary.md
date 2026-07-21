# GHC Family Method Flow State

- Phase: v651-v4
- Owner: Sylven Arc
- Methods: 24
- Passing witnesses: 24
- Failed witnesses retained: 24

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

### V6514-M16 — Bounded skill-name enumeration before initialization

- Trigger: A shell wrapper consumes Python-emitted skill names as separate records.
- Method: Emit one skill name per output record with a real newline separator and assert the twenty-record count before initialization.
- Recurrence guard: Use a line-emitting separator such as chr(10), then assert exactly twenty skill names before any write.
- Rollback: Give the failed enumeration zero credit and create no partial skills until the exact count is attributable.
- Witnesses: V6514-M16-WFAIL, V6514-M16-WPASS

### V6514-M17 — Explicit UTF-8 envelope for official skill validation

- Trigger: The unchanged validator reads a UTF-8 SKILL.md under a Windows locale default.
- Method: Set Python UTF-8 mode explicitly before running the unchanged official quick validator.
- Recurrence guard: Set PYTHONUTF8=1 for the official validator whenever phase-local UTF-8 content is present.
- Rollback: Retain the decode failure, do not strip or transliterate Māori text, and stop if explicit UTF-8 validation does not pass.
- Witnesses: V6514-M17-WFAIL, V6514-M17-WPASS

### V6514-M18 — Preflight required Method Flow record fields

- Trigger: A hand-authored method or witness input is about to enter the append-only ledger.
- Method: Validate hand-authored Method Flow inputs against the required schema fields before invoking the append-only ledger runner.
- Recurrence guard: Require retained_negative_ids on every method and witness input before ledger invocation.
- Rollback: Keep the schema rejection at zero credit and confirm the ledger remained unchanged before retrying.
- Witnesses: V6514-M18-WFAIL, V6514-M18-WPASS

### V6514-M19 — Explicit target headers for multi-file additive patches

- Trigger: One additive patch changes structurally similar fields across multiple JSON files.
- Method: Use one explicit patch file header per target file and exact UTF-8 context for multi-file Method Flow corrections.
- Recurrence guard: Give every edited file its own explicit patch header and verify exact context before applying.
- Rollback: Retain the no-change patch failure and inspect exact target files before retrying.
- Witnesses: V6514-M19-WFAIL, V6514-M19-WPASS

### V6514-M20 — Resume append-only Method Flow after witness-schema rejection

- Trigger: A method record succeeded but its first witness failed schema validation.
- Method: Preflight every witness for retained_negative_ids and independent_reproduction before appending; when a method was already recorded, resume from its first missing witness rather than duplicating it.
- Recurrence guard: Validate required witness fields before ledger invocation and inspect method state before resuming a partial sequence.
- Rollback: Retain the rejected witness, preserve the already-recorded candidate method, and append only missing valid events.
- Witnesses: V6514-M20-WFAIL, V6514-M20-WPASS

### V6514-M21 — Explicit UTF-8 Method Flow summary envelope

- Trigger: A Method Flow summary contains UTF-8 text and is printed through a Windows console encoding.
- Method: Set Python UTF-8 mode before Method Flow summarize so the file-backed summary and console receipt share one encoding envelope.
- Recurrence guard: Set PYTHONUTF8=1 for Method Flow summarize when any retained method contains UTF-8 text.
- Rollback: Retain the console-encoding failure, preserve the valid ledger, and do not strip or transliterate Māori text.
- Witnesses: V6514-M21-WFAIL, V6514-M21-WPASS

### V6514-M22 — Bounded predecessor-script inspection after wrapper timeout

- Trigger: A read-only inspection combines multiple large predecessor files under one wrapper deadline.
- Method: Split broad source-file inspection into bounded UTF-8 reads and verify repository state separately after any wrapper timeout.
- Recurrence guard: Read one bounded file segment per command and audit HEAD plus clean state before continuing after a timeout.
- Rollback: Give the timed-out inspection zero evidence credit, retain it, and stop if repository state cannot be attributed read-only.
- Witnesses: V6514-M22-WFAIL, V6514-M22-WPASS

### V6514-M23 — Exact generated-file anchor recovery after rejected patch

- Trigger: A patch must change long generated text and adjacent validation constants.
- Method: Locate exact generated-file anchors first, then apply small single-purpose patches.
- Recurrence guard: Use fixed-string line discovery and one exact patch hunk per generated-file concern.
- Rollback: Retain the rejected patch at zero credit and verify no file changed before retrying.
- Witnesses: V6514-M23-WFAIL, V6514-M23-WPASS

### V6514-M24 — Raw porcelain framing for closeout preflight

- Trigger: A machine preflight parses Git porcelain state and paths.
- Method: Parse raw Git porcelain output without trimming framing whitespace.
- Recurrence guard: Use raw subprocess bytes or NUL-delimited porcelain for machine parsing; never strip state columns first.
- Rollback: Retain the preflight rejection, verify no closeout artifact was written, and repair only the parser.
- Witnesses: V6514-M24-WFAIL, V6514-M24-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
