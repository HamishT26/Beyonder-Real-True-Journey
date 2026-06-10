# v498-gmut-thos-v34-v7-x2 Watcher/Notifier Trust Policy

- generated_utc: `2026-06-07T03:50:02Z`
- overall_status: `PASS_POLICY_BUILT`

## Rules
- `x1_no_babysit_before_15_minute_gate`: after all five x1 prompts are sent, do not manually check status before the 15-minute gate unless a watcher emits a blocker receipt.
- `x2_no_babysit_before_10_minute_gate`: after x2 prep starts, do not manually check status before the 10-minute prep gate unless a watcher emits a blocker receipt.
- `productive_wait_required`: use wait windows for research, reflection, task design, source refresh, runner hardening, and approval-packet preparation.
- `completion_requires_receipt`: waiting time alone is not completion proof; completion needs a watcher/notifier/final-marker/app/CLI/normalized-board receipt.
- `status_only_publication`: publish status, hashes, byte counts, word counts, timing, and policy outcomes only.

## Escalation
Missed cadence gates stay on the roster and flow into stale-flow repair. Generic marker counts with strict marker count zero remain marker-review items, not automatic blockers.
