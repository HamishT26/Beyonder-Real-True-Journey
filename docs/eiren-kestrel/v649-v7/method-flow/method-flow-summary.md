# GHC Family Method Flow State

- Phase: v649-gmut-thos-v7-x1-x2
- Owner: Eiren Kestrel
- Methods: 9
- Passing witnesses: 9
- Failed witnesses retained: 9

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

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
