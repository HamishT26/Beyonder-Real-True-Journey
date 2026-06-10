# v461A-v490A Ninety-Minute Heartbeat Workflow v2

Generated UTC: `2026-05-28T13:00:12Z`

Generated NZ: `2026-05-29T01:00:12+12:00`

Status: `paste_ready_automation_packet_created`

This replaces `v461A-v490A-three-hour-heartbeat-workflow-v1` for live automation use. It corrects the obsolete `bf527c7...` shared-head reference and changes the cadence from every 3 hours to every 90 minutes.

Calendar correction: `12:58am NZ Friday` after Thursday May 28 is `Friday, May 29, 2026`.

## Paste-Ready Automation Packet

```text
v461A-v490A GHC Family Remastered Ninety-Minute Heartbeat

Schedule: every 90 minutes.
Project authority: D:\GHC-Archives\worktrees\v58-omega.
If cwd differs, run:
Set-Location -LiteralPath 'D:\GHC-Archives\worktrees\v58-omega'

Current durable truth:
- v461A remaster packet is complete, published, and remote-verified at shared omega head 58dc715f8af9925a22e97b6e1b7d60401044d3eb.
- v461A-v463A prior canon is complete, pushed, branch-indexed, and final remote-verified; treat it as source baseline, not something to rename or overwrite.
- v464A is not opened yet.
- v461B/v462B are alias labels for the earlier completed setup phases; do not rename old artifacts.
- Kimi is held, not retried, not replaced.
- Separate Parfit main reconnect remains postponed for later week.
- Existing App lanes: Parfit/Lorentz 019e52d7-c06d-7c31-8a66-2162ff7c658b, Cicero 019e485f-172b-72c0-adf7-27daea722143, Kierkegaard 019e485f-1aa5-7c31-b578-748091f7e319, Aristotle 019e5158-28ef-75b1-a3f5-563bb358e44e.
- Arby and Aster Vale remain CLI/worktree lanes unless their CLI platform itself exposes a real callable ID; do not invent or infer one.
- Arby v461A remaster CLI report branch head: 54b365446b8b334a59407c8a0a85f93ca19fa12b.
- Aster Vale v461A remaster CLI report branch head: 7c0576c6c98529e6ec80913c9de6a757956c0a47.
- Calendar anchor correction: NZ Friday midnight after Thursday May 28 is Friday, May 29, 2026.

Run model:
- Use each 90-minute heartbeat for one phase-version half only.
- Active work target: 1 hour focused phase-version run.
- Final 30 minutes: validation, sibling follow-up, breath, blocker handling, run-status update, and handoff.
- Sequence starts: v461A v1, then v461A v2, then v462A v1, then v462A v2, continuing one half at a time through v490A v2.
- Do not skip ahead. Do not open v464A until v461A, v462A, and v463A remaster v1/v2 halves are durably complete in this new run.

Agent collaboration policy:
- Aletheon leads and publishes only after checks.
- Use existing callable App lanes only; do not spawn new subagents unless Hamish explicitly asks.
- Message App lanes for elaborate evidence-first reports by default; compact reports are only for emergency, blocker, or explicit quick-check contexts.
- Attempt at least five bounded structured exchanges/checkpoints with Parfit/Lorentz, Cicero, Kierkegaard, and Aristotle per phase-version half when safely reachable.
- Keep Arby/Aster CLI lanes branch/worktree scoped and ask them for elaborate CLI reports through their worktrees when needed.
- Attempt at least five bounded structured CLI checkpoints or report sections with Arby and Aster Vale per phase-version half when safely reachable.
- If any lane cannot be reached safely or within the timebox, record the blocker; do not fabricate messages, receipts, or callable IDs.
- Do not treat advisory receipts as CLI proof or publication authority.

Research policy:
- Use the v461A remaster web research queue as a 20 theme x 10 search plan.
- Prefer official/primary sources.
- Do not claim queued searches as completed searches.
- Classify web-derived claims as evidence, hypothesis, context, or blocker.
- Keep raw source documents, raw logs, screenshots, session JSONL, and secret-bearing material out of curated staging.

Publication policy:
- Before every shared commit/push: fetch, drift-check, forward-only merge only if needed, curated stage only, JSON parse, path/secret/whitespace checks, staged diff review, commit, push, verify remote equals local.
- Never reset, rebase, force-push, stage raw logs, expose secrets, mutate external services, spend money, or perform destructive cleanup.

Closeout policy:
- Every heartbeat must write or update a run-status artifact for the current phase-version half.
- Record blockers instead of smoothing them into success.
- If stale automation path reports C:\... vs \\?\C:\... for the same session JSONL, treat it as Codex app resume-path vitality, not repo failure; do not edit session JSONL.
- Stop after v490A v2 closeout unless Hamish explicitly asks for v491+.
```

## Operational Notes

This packet intentionally starts the new live remastered run at `v461A v1`, even though prior v461A-v463A canon and the v461A remaster setup packet are already complete. That means the prior canon is the baseline and this heartbeat drives the new v1/v2 remastered execution cycle.

The 90-minute cadence is tight. The safe interpretation is one high-quality phase-version half per heartbeat: 60 minutes of focused work, then 30 minutes to collect lane reports, validate JSON, preserve blockers, and prepare the next half.

The exchange target is aspirational but bounded by truth: if five exchanges with a lane cannot be completed safely, the correct action is to record the blocker, not synthesize a fake receipt.
