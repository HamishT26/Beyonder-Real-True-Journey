# GHC Family Method Flow State

- Phase: v652-v3
- Owner: Tamar Vey
- Methods: 15
- Passing witnesses: 15
- Failed witnesses retained: 15

## Preferred methods

### V6523-METHOD-01 — startup path probe timeout

- Trigger: The matching bounded workflow failure signature is observed; Recovery must preserve the failed witness and protected state
- Method: Probe the required exact paths directly and independently.
- Recurrence guard: Use one exact path per startup probe.
- Rollback: Stop after the bounded attempt, retain the failed witness, and leave sibling, external, participant, production, authority, and host-security state unchanged.
- Witnesses: V6523-FAILED-WITNESS-01, V6523-WITNESS-01

### V6523-METHOD-02 — baton chunk broken pipe

- Trigger: The matching bounded workflow failure signature is observed; Recovery must preserve the failed witness and protected state
- Method: Materialize the exact commit blob into an in-memory line array and slice that array.
- Recurrence guard: Do not truncate a live Git producer when complete-file evidence is required.
- Rollback: Stop after the bounded attempt, retain the failed witness, and leave sibling, external, participant, production, authority, and host-security state unchanged.
- Witnesses: V6523-FAILED-WITNESS-02, V6523-WITNESS-02

### V6523-METHOD-03 — method schema filename assumption

- Trigger: The matching bounded workflow failure signature is observed; Recovery must preserve the failed witness and protected state
- Method: Follow the exact reference named by the selected skill.
- Recurrence guard: Resolve skill-linked references verbatim.
- Rollback: Stop after the bounded attempt, retain the failed witness, and leave sibling, external, participant, production, authority, and host-security state unchanged.
- Witnesses: V6523-FAILED-WITNESS-03, V6523-WITNESS-03

### V6523-METHOD-04 — workflow enum assumption

- Trigger: The matching bounded workflow failure signature is observed; Recovery must preserve the failed witness and protected state
- Method: Use the runner-supported user-mediated relay enum while separately prohibiting live-phase cross-platform action.
- Recurrence guard: Validate policy enums against the current runner schema.
- Rollback: Stop after the bounded attempt, retain the failed witness, and leave sibling, external, participant, production, authority, and host-security state unchanged.
- Witnesses: V6523-FAILED-WITNESS-04, V6523-WITNESS-04

### V6523-METHOD-05 — fast forward verbose output

- Trigger: The matching bounded workflow failure signature is observed; Recovery must preserve the failed witness and protected state
- Method: Do not repeat the mutation; verify branch, exact head, and clean state with scalar postconditions.
- Recurrence guard: Suppress or bound fast-forward summaries in large inherited histories.
- Rollback: Stop after the bounded attempt, retain the failed witness, and leave sibling, external, participant, production, authority, and host-security state unchanged.
- Witnesses: V6523-FAILED-WITNESS-05, V6523-WITNESS-05

### V6523-METHOD-06 — overbroad keyword audit

- Trigger: The matching bounded workflow failure signature is observed; Recovery must preserve the failed witness and protected state
- Method: Emit counts only, then inspect bounded samples for selected or colliding terms.
- Recurrence guard: Separate discovery counts from sample inspection.
- Rollback: Stop after the bounded attempt, retain the failed witness, and leave sibling, external, participant, production, authority, and host-security state unchanged.
- Witnesses: V6523-FAILED-WITNESS-06, V6523-WITNESS-06

### V6523-METHOD-07 — powershell foreach pipeline

- Trigger: The matching bounded workflow failure signature is observed; Recovery must preserve the failed witness and protected state
- Method: Assign the foreach results to an array before JSON serialization.
- Recurrence guard: Materialize foreach output before a trailing pipeline.
- Rollback: Stop after the bounded attempt, retain the failed witness, and leave sibling, external, participant, production, authority, and host-security state unchanged.
- Witnesses: V6523-FAILED-WITNESS-07, V6523-WITNESS-07

### V6523-METHOD-08 — python tuple tie comparison

- Trigger: The matching bounded workflow failure signature is observed; Recovery must preserve the failed witness and protected state
- Method: Select the maximum with an explicit score key.
- Recurrence guard: Never rely on nonorderable payloads as tuple tie-breakers.
- Rollback: Stop after the bounded attempt, retain the failed witness, and leave sibling, external, participant, production, authority, and host-security state unchanged.
- Witnesses: V6523-FAILED-WITNESS-08, V6523-WITNESS-08

### V6523-METHOD-09 — method request utf8 bom

- Trigger: The matching bounded workflow failure signature is observed; Recovery must preserve the failed witness and protected state
- Method: Write temporary runner request JSON with an explicit UTF-8 encoding that emits no BOM.
- Recurrence guard: Use explicit no-BOM UTF-8 for strict JSON runner inputs.
- Rollback: Stop after the bounded attempt, retain the failed witness, and leave sibling, external, participant, production, authority, and host-security state unchanged.
- Witnesses: V6523-FAILED-WITNESS-09, V6523-WITNESS-09

### V6523-METHOD-10 — powershell json array wrapper

- Trigger: The matching bounded workflow failure signature is observed; Recovery must preserve the failed witness and protected state
- Method: Index the parsed object array directly and emit one method plus two witnesses per negative.
- Recurrence guard: Inspect parsed-array cardinality before batch Method Flow ingestion.
- Rollback: Stop after the bounded attempt, retain the failed witness, and leave sibling, external, participant, production, authority, and host-security state unchanged.
- Witnesses: V6523-FAILED-WITNESS-10, V6523-WITNESS-10

### V6523-METHOD-11 — bounded validator source inspection

- Trigger: A validator source must be inspected without exceeding the active context budget; The failed broad read remains retained
- Method: Locate exact symbols with rg, then read two bounded non-overlapping line windows.
- Recurrence guard: Inspect large validator sources by symbol index and bounded line windows rather than a single broad read.
- Rollback: Stop the inspection, retain the failed witness, and make no repository claim from truncated output.
- Witnesses: V6523-FAILED-WITNESS-11, V6523-WITNESS-11

### V6523-METHOD-12 — split repository state probes

- Trigger: A combined read-only status and file-count probe times out; Recovery must remain read-only and bounded
- Method: Split Git scalars from phase-root file discovery and bound each command independently.
- Recurrence guard: Keep Git state and filesystem inventory probes separate, scalar, and independently time-bounded.
- Rollback: Stop after the timeout, retain it, and avoid using partial or absent output as repository-state evidence.
- Witnesses: V6523-FAILED-WITNESS-12, V6523-WITNESS-12

### V6523-METHOD-13 — listed exact Method Flow receipt path

- Trigger: A guessed Method Flow validation filename does not exist; The directory listing already exposes the exact current names
- Method: Use the exact listed method-flow-ledger.json and method-flow-validation.json paths.
- Recurrence guard: Resolve current phase receipt names from an exact directory listing before reading a suffixed variant.
- Rollback: Stop the guessed-path read, retain it, and do not infer ledger state from a missing file.
- Witnesses: V6523-FAILED-WITNESS-13, V6523-WITNESS-13

### V6523-METHOD-14 — exact compact-builder patch context

- Trigger: An additive patch fails because its expected dictionary layout is not present; The failed patch changed no bytes
- Method: Read the exact bounded builder window and patch the compact dictionary in place.
- Recurrence guard: Inspect the current bounded context before patching generated compact dictionaries.
- Rollback: Keep the failed no-op patch retained and make no source claim until the exact-context patch applies.
- Witnesses: V6523-FAILED-WITNESS-14, V6523-WITNESS-14

### V6523-METHOD-15 — exact evidence change-domain parity

- Trigger: A validator manifest omits a current changed path despite reporting valid; The credited rerun must preserve the failed result
- Method: Union tracked unstaged, tracked staged, and untracked path sets, subtract only declared self-exclusions, and require exact path parity.
- Recurrence guard: Never credit a staged manifest without an independent exact path-set parity check.
- Rollback: Give the first validator attempt zero credit, retain its receipts as superseded working evidence, and do not commit until corrected parity passes.
- Witnesses: V6523-FAILED-WITNESS-15, V6523-WITNESS-15

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
