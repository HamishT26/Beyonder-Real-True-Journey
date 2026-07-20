# GHC Family Method Flow State

- Phase: v650-gmut-thos-v2-x1-x2
- Owner: Ilyra Fen
- Methods: 12
- Passing witnesses: 12
- Failed witnesses retained: 12

## Preferred methods

### V6502-M01 — Retain and recover startup failure N01

- Trigger: Startup exposes N01.
- Method: Re-read the skill in bounded sequential ranges and verify coverage through the final line before granting read credit.
- Recurrence guard: Re-read the skill in bounded sequential ranges and verify coverage through the final line before granting read credit.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6502-M01-WFAIL, V6502-M01-WPASS

### V6502-M02 — Retain and recover startup failure N02

- Trigger: Startup exposes N02.
- Method: Bypass login-profile initialization and run one independently bounded streaming probe.
- Recurrence guard: Bypass login-profile initialization and run one independently bounded streaming probe.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6502-M02-WFAIL, V6502-M02-WPASS

### V6502-M03 — Retain and recover startup failure N03

- Trigger: Startup exposes N03.
- Method: Bypass login-profile initialization and run the unchanged metadata probe independently.
- Recurrence guard: Bypass login-profile initialization and run the unchanged metadata probe independently.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6502-M03-WFAIL, V6502-M03-WPASS

### V6502-M04 — Retain and recover startup failure N04

- Trigger: Startup exposes N04.
- Method: Split path, repository, state, and live-remote probes so each result remains independently attributable.
- Recurrence guard: Split path, repository, state, and live-remote probes so each result remains independently attributable.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6502-M04-WFAIL, V6502-M04-WPASS

### V6502-M05 — Retain and recover startup failure N05

- Trigger: Startup exposes N05.
- Method: Verify the exact resulting head separately and use bounded exact-path or staged reviews for review credit.
- Recurrence guard: Verify the exact resulting head separately and use bounded exact-path or staged reviews for review credit.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6502-M05-WFAIL, V6502-M05-WPASS

### V6502-M06 — Retain and recover startup failure N06

- Trigger: Startup exposes N06.
- Method: Normalize only ripgrep exit one to an explicit no-match and preserve every other nonzero exit.
- Recurrence guard: Normalize only ripgrep exit one to an explicit no-match and preserve every other nonzero exit.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6502-M06-WFAIL, V6502-M06-WPASS

### V6502-M07 — Retain and recover startup failure N07

- Trigger: Startup exposes N07.
- Method: Read the exact Method Flow counts object and assert its witness_results fail and pass keys without changing the ledger schema.
- Recurrence guard: Read the exact Method Flow counts object and assert its witness_results fail and pass keys without changing the ledger schema.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6502-M07-WFAIL, V6502-M07-WPASS

### V6502-M08 — Retain and recover startup failure N08

- Trigger: Startup exposes N08.
- Method: Suppress advisory stderr for the bounded restage, then verify the exact cached path set and Git-index blob parity independently.
- Recurrence guard: Suppress advisory stderr for the bounded restage, then verify the exact cached path set and Git-index blob parity independently.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6502-M08-WFAIL, V6502-M08-WPASS

### V6502-M09 — Retain and recover NEG-V6502-X2-001

- Trigger: The v650-v2 x2 workflow exposes this exact bounded failure signature.
- Method: Resume from the last attributable line in smaller bounded ranges, verify the final line, then read the required metadata schema completely before creating any skill package.
- Recurrence guard: Resume from the last attributable line in smaller bounded ranges, verify the final line, then read the required metadata schema completely before creating any skill package.
- Rollback: Give the failed attempt zero credit, retain it, and restore the immutable x1 boundary if recovery fails.
- Witnesses: V6502-M09-WFAIL, V6502-M09-WPASS

### V6502-M10 — Retain and recover NEG-V6502-X2-002

- Trigger: The v650-v2 x2 workflow exposes this exact bounded failure signature.
- Method: Give the aggregate zero credit, run syntax compilation independently, and inspect exact owner-scoped status in a separately bounded probe before continuing.
- Recurrence guard: Give the aggregate zero credit, run syntax compilation independently, and inspect exact owner-scoped status in a separately bounded probe before continuing.
- Rollback: Give the failed attempt zero credit, retain it, and restore the immutable x1 boundary if recovery fails.
- Witnesses: V6502-M10-WFAIL, V6502-M10-WPASS

### V6502-M11 — Retain and recover NEG-V6502-X2-003

- Trigger: The v650-v2 x2 workflow exposes this exact bounded failure signature.
- Method: Retain the failed build with zero completion credit and verify the unchanged CLI version through a no-profile PowerShell command without updating or widening the environment.
- Recurrence guard: Retain the failed build with zero completion credit and verify the unchanged CLI version through a no-profile PowerShell command without updating or widening the environment.
- Rollback: Give the failed attempt zero credit, retain it, and restore the immutable x1 boundary if recovery fails.
- Witnesses: V6502-M11-WFAIL, V6502-M11-WPASS

### V6502-M12 — Classify every committed privacy receipt as a scanner-definition surface

- Trigger: An exact-final privacy scan includes a committed scanner receipt that describes its own definition candidates.
- Method: Add the exact committed scanner-receipt filename to the definition allowlist, preserve the failed aggregate, and exercise only the classifier before rebuilding terminal manifests.
- Recurrence guard: Enumerate every committed scanner-definition receipt explicitly and leave all unmatched files fail-closed as payload candidates.
- Rollback: Give the failed aggregate zero successful-pass credit, keep the route held, and revert only the classifier correction if its bounded witness fails.
- Witnesses: V6502-M12-WFAIL, V6502-M12-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
