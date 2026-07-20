# GHC Family Method Flow State

- Phase: v649-gmut-thos-v7-x1-x2
- Owner: Eiren Kestrel
- Methods: 15
- Passing witnesses: 14
- Failed witnesses retained: 15

## Preferred methods

### V6497-M01 — Retain and recover startup failure N01

- Trigger: Startup exposes N01.
- Method: Use targeted exact skill paths and avoid broad recursive enumeration.
- Recurrence guard: Use targeted exact skill paths and avoid broad recursive enumeration.
- Rollback: Give the failed attempt zero credit; restore the last bounded state and use only attributable returned evidence.
- Witnesses: V6497-M01-WFAIL, V6497-M01-WPASS

### V6497-M02 — Retain and recover startup failure N02

- Trigger: Startup exposes N02.
- Method: Resolve named skills from the supplied catalog and inspect only required paths.
- Recurrence guard: Resolve named skills from the supplied catalog and inspect only required paths.
- Rollback: Give the failed attempt zero credit; restore the last bounded state and use only attributable returned evidence.
- Witnesses: V6497-M02-WFAIL, V6497-M02-WPASS

### V6497-M03 — Retain and recover startup failure N03

- Trigger: Startup exposes N03.
- Method: Retry once with one literal path and a measured longer bound; do not broaden scope.
- Recurrence guard: Retry once with one literal path and a measured longer bound; do not broaden scope.
- Rollback: Give the failed attempt zero credit; restore the last bounded state and use only attributable returned evidence.
- Witnesses: V6497-M03-WFAIL, V6497-M03-WPASS

### V6497-M04 — Retain and recover startup failure N04

- Trigger: Startup exposes N04.
- Method: Materialize rows in an array before ConvertTo-Json.
- Recurrence guard: Materialize rows in an array before ConvertTo-Json.
- Rollback: Give the failed attempt zero credit; restore the last bounded state and use only attributable returned evidence.
- Witnesses: V6497-M04-WFAIL, V6497-M04-WPASS

### V6497-M05 — Retain and recover startup failure N05

- Trigger: Startup exposes N05.
- Method: Use a standalone exact patch terminator and verify no file was created before retry.
- Recurrence guard: Use a standalone exact patch terminator and verify no file was created before retry.
- Rollback: Give the failed attempt zero credit; restore the last bounded state and use only attributable returned evidence.
- Witnesses: V6497-M05-WFAIL, V6497-M05-WPASS

### V6497-M06 — Retain and recover startup failure N06

- Trigger: Startup exposes N06.
- Method: Read the runner help and invoke the documented positional packet form.
- Recurrence guard: Read the runner help and invoke the documented positional packet form.
- Rollback: Give the failed attempt zero credit; restore the last bounded state and use only attributable returned evidence.
- Witnesses: V6497-M06-WFAIL, V6497-M06-WPASS

### V6497-M07 — Retain and recover startup failure N07

- Trigger: Startup exposes N07.
- Method: Preserve the passing runner audit and build an additive phase-local generalized validator instead of mutating the global compatibility surface.
- Recurrence guard: Preserve the passing runner audit and build an additive phase-local generalized validator instead of mutating the global compatibility surface.
- Rollback: Give the failed attempt zero credit; restore the last bounded state and use only attributable returned evidence.
- Witnesses: V6497-M07-WFAIL, V6497-M07-WPASS

### V6497-M08 — Retain and recover startup failure N08

- Trigger: Startup exposes N08.
- Method: Split status, head, and file inventory into narrow independent probes and credit only returned evidence.
- Recurrence guard: Split status, head, and file inventory into narrow independent probes and credit only returned evidence.
- Rollback: Give the failed attempt zero credit; restore the last bounded state and use only attributable returned evidence.
- Witnesses: V6497-M08-WFAIL, V6497-M08-WPASS

### V6497-M09 — Retain and recover startup failure N09

- Trigger: Startup exposes N09.
- Method: Select novelty neighbors with an explicit score key so tie resolution never compares dictionary payloads.
- Recurrence guard: Select novelty neighbors with an explicit score key so tie resolution never compares dictionary payloads.
- Rollback: Give the failed attempt zero credit; restore the last bounded state and use only attributable returned evidence.
- Witnesses: V6497-M09-WFAIL, V6497-M09-WPASS

### V6497-M10 — Retain and recover NEG-V6497-X2-001

- Trigger: The bounded v649-v7 x2 generator exposes this exact failure signature.
- Method: Permit exactly declared v649-v7 seed or partial-generation paths while refusing every unrelated path.
- Recurrence guard: Permit exactly declared v649-v7 seed or partial-generation paths while refusing every unrelated path.
- Rollback: Give the failed attempt zero credit, retain it, and restore the last immutable x1 state if the bounded repair fails.
- Witnesses: V6497-M10-WFAIL, V6497-M10-WPASS

### V6497-M11 — Retain and recover NEG-V6497-X2-002

- Trigger: The bounded v649-v7 x2 generator exposes this exact failure signature.
- Method: Emit ordinary dictionary literals in the non-format template, run the validator in isolation, and require a returned passing receipt before x2 credit.
- Recurrence guard: Emit ordinary dictionary literals in the non-format template, run the validator in isolation, and require a returned passing receipt before x2 credit.
- Rollback: Give the failed attempt zero credit, retain it, and restore the last immutable x1 state if the bounded repair fails.
- Witnesses: V6497-M11-WFAIL, V6497-M11-WPASS

### V6497-M12 — Retain and recover NEG-V6497-X2-003

- Trigger: The bounded v649-v7 x2 generator exposes this exact failure signature.
- Method: Check LASTEXITCODE immediately after every validation child and stop before running the next child when any test fails.
- Recurrence guard: Check LASTEXITCODE immediately after every validation child and stop before running the next child when any test fails.
- Rollback: Give the failed attempt zero credit, retain it, and restore the last immutable x1 state if the bounded repair fails.
- Witnesses: V6497-M12-WFAIL, V6497-M12-WPASS

### V6497-M13 — Retain and recover NEG-V6497-X2-004

- Trigger: The bounded v649-v7 x2 generator exposes this exact failure signature.
- Method: Parse status from the raw subprocess stdout without global strip and normalize each complete porcelain record independently.
- Recurrence guard: Parse status from the raw subprocess stdout without global strip and normalize each complete porcelain record independently.
- Rollback: Give the failed attempt zero credit, retain it, and restore the last immutable x1 state if the bounded repair fails.
- Witnesses: V6497-M13-WFAIL, V6497-M13-WPASS

### V6497-M15 — Retain and recover V6497-M15

- Trigger: The v649-v7 validation lifecycle exposes this exact failure.
- Method: Resolve the exact class declaration from source before invoking the two historical test IDs.
- Recurrence guard: Resolve the exact class declaration from source before invoking the two historical test IDs.
- Rollback: Give the failed attempt zero pass credit and preserve the immutable evidence head.
- Witnesses: V6497-M15-WFAIL, V6497-M15-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
