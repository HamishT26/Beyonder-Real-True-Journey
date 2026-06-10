# v498 GMUT/THOS v34 v4 x2 Marker Review Policy

- generated_utc: `2026-06-07T01:56:19Z`
- overall_status: `PASS_MARKER_REVIEW_POLICY_BUILT`
- used_in_current_phase: `true`

## Policy Rows

- Final message ready and strict quality marker count is zero: allow metadata-only summary; raw output remains blocked.
- Generic marker count is greater than zero but strict quality marker count is zero: treat as a false-positive review trigger after quality pass; raw output remains blocked.
- Strict quality marker count is greater than zero: hold for repair or user approval.
- Missing final message or missing required headings: hold phase advance or route to stale-flow repair.

This policy was used for the v498 v4 x1 to x2 handoff and remains a candidate for future runner hardening.
