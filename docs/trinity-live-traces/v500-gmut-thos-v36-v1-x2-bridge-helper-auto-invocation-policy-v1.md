# v500 GMUT/THOS v36 v1 x2 Bridge Helper Auto-Invocation Policy

- generated_utc: `2026-06-07T12:15:03Z`
- overall_status: `PASS_BRIDGE_HELPER_AUTO_INVOCATION_POLICY_READY`

The v500 live flow confirms the repair sequence: after cadence, the first CLI notifier can show missing expected final-message files; the bridge helper repairs the surface; the notifier then sees final messages; the quality gate passes; and the five-lane normalizer can approve phase readiness.

This becomes the default post-cadence sequence for future direct bridge launches.
