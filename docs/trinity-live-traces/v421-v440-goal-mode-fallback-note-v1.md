# v421-v440 Goal Mode Fallback Note

Generated UTC: `2026-05-22T09:13:00Z`

Status: `goal_mode_ui_non_blocking`

Reported symptom: UI reports `failed to set goal` for the active v421-v440 goal prompt.

Decision: do not depend on UI Goal Mode for tonight's v421-v440 launch. Continue through the 20-minute automation heartbeat, run-status artifacts, and runner prompt goal-contract text.

Fallback policy:
- Automation prompt is authority.
- Runner prompt goal-contract text is allowed.
- CLI siblings should use CLI Goal Mode when their platform honors the embedded `/goal` line.
- CLI Goal Mode does not replace receipt gates.
- Do not retry Goal Mode in a loop.
- Do not block phase execution because Goal Mode failed.
- Launch v421 from automation when the heartbeat wakes.

Truth boundaries:
- Goal Mode failure does not invalidate the v421-v440 packet.
- CLI siblings may still use the embedded runner-prompt `/goal` line when their CLI platform supports it.
- Goal Mode never authorizes duplicate runners, phase collapse, external-service mutation, resets, rebases, force-pushes, or skipped validation.
- If Goal Mode works later, use one active phase-run goal at a time only.
- The durable automation prompt remains the launch surface for the night run.
