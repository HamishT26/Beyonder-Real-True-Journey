# GHC Family Method Flow State

- Phase: v649-gmut-thos-v8-x1-x2
- Owner: Elaren Kestrel
- Methods: 16
- Passing witnesses: 16
- Failed witnesses retained: 16

## Preferred methods

### V6498-M01 — Retain and recover startup failure N01

- Trigger: Startup exposes N01.
- Method: Normalize each no-match exit locally and emit independent root receipts before aggregation.
- Recurrence guard: Normalize each no-match exit locally and emit independent root receipts before aggregation.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6498-M01-WFAIL, V6498-M01-WPASS

### V6498-M02 — Retain and recover startup failure N02

- Trigger: Startup exposes N02.
- Method: Inspect top-level keys first, then concatenate only the declared proposal arrays.
- Recurrence guard: Inspect top-level keys first, then concatenate only the declared proposal arrays.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6498-M02-WFAIL, V6498-M02-WPASS

### V6498-M03 — Retain and recover startup failure N03

- Trigger: Startup exposes N03.
- Method: Materialize foreach output in an array before piping the array to JSON serialization.
- Recurrence guard: Materialize foreach output in an array before piping the array to JSON serialization.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6498-M03-WFAIL, V6498-M03-WPASS

### V6498-M04 — Retain and recover startup failure N04

- Trigger: Startup exposes N04.
- Method: Bind the wrapper to the runner's exact workflow-plan-validation contract before granting workflow credit.
- Recurrence guard: Bind the wrapper to the runner's exact workflow-plan-validation contract before granting workflow credit.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6498-M04-WFAIL, V6498-M04-WPASS

### V6498-M05 — Retain and recover startup failure N05

- Trigger: Startup exposes N05.
- Method: Use an exact discovered LiteralPath for each required workflow receipt.
- Recurrence guard: Use an exact discovered LiteralPath for each required workflow receipt.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6498-M05-WFAIL, V6498-M05-WPASS

### V6498-M06 — Retain and recover startup failure N06

- Trigger: Startup exposes N06.
- Method: Quarantine the scanner implementation and its definition receipt while continuing to scan every other staged text blob.
- Recurrence guard: Quarantine the scanner implementation and its definition receipt while continuing to scan every other staged text blob.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6498-M06-WFAIL, V6498-M06-WPASS

### V6498-M07 — Retain and recover startup failure N07

- Trigger: Startup exposes N07.
- Method: Bind every shell interpolation value explicitly before constructing the commit and equality command.
- Recurrence guard: Bind every shell interpolation value explicitly before constructing the commit and equality command.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6498-M07-WFAIL, V6498-M07-WPASS

### V6498-M08 — Retain and recover startup failure N08

- Trigger: Startup exposes N08.
- Method: Run each exact file and Git-state probe in its own bounded process with an independently attributable receipt.
- Recurrence guard: Run each exact file and Git-state probe in its own bounded process with an independently attributable receipt.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6498-M08-WFAIL, V6498-M08-WPASS

### V6498-M09 — Retain and recover startup failure N09

- Trigger: Startup exposes N09.
- Method: Inspect the exact target lines before composing each patch hunk and preserve atomic rejection as zero mutation.
- Recurrence guard: Inspect the exact target lines before composing each patch hunk and preserve atomic rejection as zero mutation.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6498-M09-WFAIL, V6498-M09-WPASS

### V6498-M10 — Retain and recover NEG-V6498-X2-001

- Trigger: The v649-v8 x2 workflow exposes this exact bounded failure signature.
- Method: Discover exact v649-v7 source files in an independent bounded command and give the ambiguous aggregate wrapper zero completion credit.
- Recurrence guard: Discover exact v649-v7 source files in an independent bounded command and give the ambiguous aggregate wrapper zero completion credit.
- Rollback: Give the failed attempt zero credit, retain it, and restore the immutable x1 boundary if recovery fails.
- Witnesses: V6498-M10-WFAIL, V6498-M10-WPASS

### V6498-M11 — Retain and recover NEG-V6498-X2-002

- Trigger: The v649-v8 x2 workflow exposes this exact bounded failure signature.
- Method: Inspect the exact source schema and bind attribution to its declared title and kind fields before rebuilding any outcome receipt.
- Recurrence guard: Inspect the exact source schema and bind attribution to its declared title and kind fields before rebuilding any outcome receipt.
- Rollback: Give the failed attempt zero credit, retain it, and restore the immutable x1 boundary if recovery fails.
- Witnesses: V6498-M11-WFAIL, V6498-M11-WPASS

### V6498-M12 — Retain and recover NEG-V6498-X2-003

- Trigger: The v649-v8 x2 workflow exposes this exact bounded failure signature.
- Method: Quarantine only the two exact scanner implementation files while continuing to scan every generated artifact, test, wrapper, and non-scanner source blob.
- Recurrence guard: Quarantine only the two exact scanner implementation files while continuing to scan every generated artifact, test, wrapper, and non-scanner source blob.
- Rollback: Give the failed attempt zero credit, retain it, and restore the immutable x1 boundary if recovery fails.
- Witnesses: V6498-M12-WFAIL, V6498-M12-WPASS

### V6498-M13 — Retain and recover NEG-V6498-X2-004

- Trigger: The v649-v8 x2 workflow exposes this exact bounded failure signature.
- Method: Give the repeated selection no additional evidence weight and do not repeat any further successful selection; reserve exactly one terminal canonical pass.
- Recurrence guard: Give the repeated selection no additional evidence weight and do not repeat any further successful selection; reserve exactly one terminal canonical pass.
- Rollback: Give the failed attempt zero credit, retain it, and restore the immutable x1 boundary if recovery fails.
- Witnesses: V6498-M13-WFAIL, V6498-M13-WPASS

### V6498-M14 — Bind minimal identity assertions to the declared schema key

- Trigger: A validator reads a frozen JSON artifact whose semantic field name has not been inspected.
- Method: Inspect exact frozen keys, bind the assertion to identity_boundary, and run only the minimal and privacy blocker surfaces before retrying the canonical pass.
- Recurrence guard: Inspect frozen JSON keys before writing validator assertions; reject guessed schema fields before the terminal pass.
- Rollback: Give the failed canonical attempt zero pass credit, retain it, and keep the route unsent until the corrected exact head passes.
- Witnesses: V6498-M14-WFAIL, V6498-M14-WPASS

### V6498-M15 — Quarantine every exact scanner implementation in correction reviews

- Trigger: The v649-v8 correction workflow exposes this exact failure signature.
- Method: Enumerate the correction builder and canonical validator as the exact two scanner-definition files while scanning every other correction blob.
- Recurrence guard: Enumerate the correction builder and canonical validator as the exact two scanner-definition files while scanning every other correction blob.
- Rollback: Give the failed attempt zero credit, retain it, and keep the correction commit and route blocked until the exact recovery passes.
- Witnesses: V6498-M15-WFAIL, V6498-M15-WPASS

### V6498-M16 — Inspect exact source lines before multi-hunk retention patches

- Trigger: The v649-v8 correction workflow exposes this exact failure signature.
- Method: Inspect exact source lines and apply smaller independently verifiable hunks without assuming prior generated text.
- Recurrence guard: Inspect exact source lines and apply smaller independently verifiable hunks without assuming prior generated text.
- Rollback: Give the failed attempt zero credit, retain it, and keep the correction commit and route blocked until the exact recovery passes.
- Witnesses: V6498-M16-WFAIL, V6498-M16-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
