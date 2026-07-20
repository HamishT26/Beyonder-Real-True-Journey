# GHC Family Method Flow State

- Phase: v650-gmut-thos-v2-x1-x2
- Owner: Ilyra Fen
- Methods: 8
- Passing witnesses: 8
- Failed witnesses retained: 8

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

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
