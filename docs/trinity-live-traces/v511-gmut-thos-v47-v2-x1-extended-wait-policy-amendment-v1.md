# v511 GMUT/THOS v47 v2 x1 Extended Wait Policy Amendment

Status: PASS_EXTENDED_WAIT_POLICY_AMENDMENT_RECORDED

This amendment records the latest lane timing clarification for the grouped round-robin live-adapter workflow.

## Operating Rule

Five-minute checks are pulse checks only. They are not response deadlines and they are not evidence that a sibling has failed.

If Lumen Vale, Arby, Aster Vale, Cicero, Kierkegaard, or Aristotle is still plausibly reasoning, generating, or working, the lane should remain open beyond the first five-minute check. Prompts and requested artifacts must not be narrowed merely to fit a short check window.

## Retry Rule

Retry only after distinct stale or blocker evidence appears, such as:

- No completion marker after an extended wait.
- Composer is available and no active generation is visible.
- No visible text growth across checks.
- A route or app blocker is explicitly observed.
- A watcher or notifier receipt reports a terminal blocker.

## Safety

This receipt is status-only. It publishes no raw lane text, raw routes, credentials, screenshots, session streams, or local absolute paths.

## Next Action

Continue v511 and later grouped round-robin phases with five-minute pulse checks, longer waits for active siblings, and non-diminished x1 preparation prompts.
