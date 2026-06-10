# v469A GMUT v7 x1 Metric Signature Hold Card

Classification: `blocker`

This artifact attempts a metric-signature decision card and records the honest hold state.

Decision attempt:

- Candidate: `mostly_plus_rehearsal_candidate`
- Status: `EXPLICIT_HOLD`
- Reason: metric signature cannot be frozen until source anchors, sign-sensitive formula cards, and route-wide dependencies are exact.

Required before freeze:

- signature label
- `g00` policy
- inverse metric policy
- raising and lowering rule
- temporal kinetic sign propagation
- spatial kinetic sign propagation
- source anchor reference
- statement that convention choice is not validation

Safe language: mostly-plus may remain a rehearsal candidate only; it is not validation, derivation, or gate closure.

Blocked promotions: temporal kinetic validated, scalar EOM derived, `T_Psi` derived, dimensional/SI consistency closed, null fixture passed, or baseline recovered.

Gate effect: all six GMUT gates remain open.
