# GHC Family Method Flow State

- Phase: v645-gmut-thos-v6-x1-x2
- Owner: Orin Thale
- Methods: 6
- Passing witnesses: 6
- Failed witnesses retained: 6

## Preferred methods

### V6456-M01 — Split broad Git startup probes after an evidence-free timeout

- Trigger: large linked-worktree repository; combined read-only Git probe returned no evidence
- Method: Decompose startup Git proof into small read-only probes and capture each native result separately.
- Recurrence guard: Do not retry a broad timed-out wrapper or infer any result from its silence.
- Rollback: Make no repository mutation until the decomposed proof passes.
- Witnesses: V6456-W01-F, V6456-W01-P

### V6456-M02 — Remove unsupported ConvertFrom-Json parameters before structured audit

- Trigger: Windows PowerShell 5.1; structured JSON inspection
- Method: Keep Windows PowerShell 5.1 JSON input parsing parameter-free and apply depth only when rendering output.
- Recurrence guard: Check cmdlet version-specific parameters before using them in evidence probes.
- Rollback: Withdraw the parse conclusion and rerun the exact read-only inspection.
- Witnesses: V6456-W02-F, V6456-W02-P

### V6456-M03 — Fail closed when Windows Sandbox state is elevation-gated

- Trigger: Sandbox status requires elevation; no exact host-change authorization
- Method: Treat elevation-gated Sandbox status as an open environment gap and stop at read-only evidence.
- Recurrence guard: Never elevate, enable a feature, weaken security, or reboot to satisfy a validation template.
- Rollback: Leave the host unchanged and retain the unavailable receipt.
- Witnesses: V6456-W03-F, V6456-W03-P

### V6456-M04 — Reject predecessor portfolio collisions before materialization

- Trigger: successor portfolio design; predecessor title corpus available
- Method: Run portfolio collision detection before phase materialization and redesign every exact collision instead of waiving it.
- Recurrence guard: Generic maintenance obligations still require a distinct owner-scoped purpose, artifact, acceptance gate, or evidence surface.
- Rollback: Leave the phase directory absent, preserve the failed comparison, and redesign before the x1 freeze.
- Witnesses: V6456-W04-F, V6456-W04-P

### V6456-M05 — Use a dependency-free scoped test entrypoint when pytest is absent

- Trigger: phase-local pure-Python assertions; pytest module absent from selected runtime
- Method: Keep the assertions and add a deterministic dependency-free direct entrypoint that discovers and invokes only the phase-local test functions.
- Recurrence guard: Check the intended test runtime and preserve zero-test dependency failures before switching runners.
- Rollback: Do not count the failed invocation; retain the test source and run only the bounded phase entrypoint.
- Witnesses: V6456-W05-F, V6456-W05-P

### V6456-M06 — Normalize family-index checkout text after preserving encoding drift

- Trigger: Windows family-index generation; owner-scoped phase output; UTF-8 LF cleanup obligation
- Method: Apply an owner-scoped reviewed-current patch that corrects the visible encoding marker and normalizes the two generated files, then rescan UTF-8 and line endings.
- Recurrence guard: Inspect generated text bytes and visible headings before staging family-index output on Windows.
- Rollback: Restore the phase-local generated files from the family index and retain the encoding negative if normalization changes semantics.
- Witnesses: V6456-W06-F, V6456-W06-P

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
