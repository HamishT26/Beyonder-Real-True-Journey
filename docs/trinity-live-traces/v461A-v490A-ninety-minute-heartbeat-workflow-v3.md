# v461A-v490A Ninety-Minute Heartbeat Workflow v3

Generated UTC: `2026-05-28T13:26:15Z`

Generated NZ: `2026-05-29T01:26:15+12:00`

Status: `paste_ready_self_refreshing_automation_packet_created`

This replaces `v461A-v490A-ninety-minute-heartbeat-workflow-v2` for live automation use.

Reason: v2 corrected the `bf527c7...` series but still embedded the pre-v2 publication head `58dc715...` inside the paste-ready text. v3 avoids that trap by making live git verification authoritative at the start of every heartbeat. The known-good baseline before authoring v3 was `7e270a876da7b7af179dd87e02265bc182fe3da2`, but each heartbeat must record the live head it observes.

## Paste-Ready Automation Packet

```text
v461A-v490A GHC Family Remastered Ninety-Minute Heartbeat v3

Schedule: every 90 minutes.
Project authority: D:\GHC-Archives\worktrees\v58-omega.
If cwd differs, run:
Set-Location -LiteralPath 'D:\GHC-Archives\worktrees\v58-omega'

Live head policy:
- At the start of every heartbeat: fetch, read local HEAD, read upstream HEAD, and record drift.
- Treat live git verification as authoritative over any embedded head in this packet.
- Record the observed live head in the current heartbeat's run-status artifact.
- Known-good baseline before v3 authoring: 7e270a876da7b7af179dd87e02265bc182fe3da2.

Current durable truth:
- v461A remaster packet is complete, published, and remote-verified.
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

## Note

This packet is intentionally self-refreshing. The next heartbeat should not fail merely because this commit changes the repository head again; instead, it should record the live head observed at runtime.
