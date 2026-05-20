# v376 Stale Kimi Recovery

Generated UTC: `2026-05-20T18:35:11.9372667Z`

Status: `stale_lane_recovery_decision`

Decision: stop only the proven stale v376 runner tree, then relaunch v376 through the bounded v371-v400 runner with `--phase 376 --background --timeout-sec 86400 --kimi-timeout-sec 86400 --max-steps 10000`.

Evidence:
- `docs/trinity-live-traces/v371-v400-sibling-run-status-v1.json` records v376 as the active phase.
- `docs/trinity-live-traces/v371-v400-cli-sibling-runner-status-v1.json` records v376 active lane `Kimi`, last updated at `2026-05-20T15:29:35.625301+00:00`.
- `docs/trinity-live-traces/v371-v400-cli-sibling-receipts/arby-phase-v376-receipt-v1.md` exists, but no v376 Kimi or Aster Vale receipt exists.
- No `docs/trinity-live-traces/v371-v400-sibling-phase-v376-cli-receipts-v1.json` aggregate exists.
- Process inspection proved PID `16936` is the bounded v376 runner, and child PID `7700` is the matching Kimi CLI lane with marker `v371-v400:v376:kimi:cli-receipt-v1`.

Truth boundaries:
- Do not resume the stale Kimi session because the session identity cannot be proven healthy after the laptop sleep interruption.
- Do not stage raw transport files.
- Do not mark v376 complete until valid real CLI receipts exist for Arby, Kimi, and Aster Vale, or a later explicit blocker decision is recorded.
