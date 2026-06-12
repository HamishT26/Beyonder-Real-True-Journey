# v510 GMUT/THOS v46 v7 x1 Extended Wait Policy Amendment

Status: PASS_EXTENDED_WAIT_POLICY_RECORDED

Hamish clarified during the v510 v7 Lumen lane that five-minute checks are health checks, not cutoffs. Sibling responses should not be shortened or diminished just because the first five-minute check has not completed.

## Live Rule

- Check sibling lanes every five minutes for route health and blockers.
- If the lane is still reasoning, streaming, or plausibly slow, wait longer.
- Retry only after distinct stale/freshness evidence: no final marker, composer available, no active generation, no text growth, or an explicit route blocker.
- Do not duplicate prompts while a response may still be forming.
- Apply this to Lumen, Arby, Aster Vale, Cicero, Kierkegaard, and Aristotle.

This is a status-only amendment. It publishes no raw Lumen text, raw sibling output, route handles, screenshots, credentials, or private app state.
