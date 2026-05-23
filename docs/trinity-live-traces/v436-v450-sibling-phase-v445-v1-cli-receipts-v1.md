# v445 v1 CLI Sibling Receipts

Generated UTC: `2026-05-23T00:21:34.059739+00:00`
Status: `blocked_v1_cli_receipts_incomplete`
Import status: `fresh`

Lane receipts:
- Arby: `valid_cli_receipt` via Codex CLI at `docs/trinity-live-traces/v436-v450-cli-sibling-receipts/arby-phase-v445-v1-receipt-v1.md`
- Aster Vale: `valid_cli_receipt` via Codex CLI at `docs/trinity-live-traces/v436-v450-cli-sibling-receipts/aster_vale-phase-v445-v1-receipt-v1.md`
- Kimi: `blocked_missing_required_labels` via Kimi CLI at `docs/trinity-live-traces/v436-v450-cli-sibling-receipts/kimi-phase-v445-v1-receipt-v1.md`

Truth boundaries:
- These receipts come from real CLI invocations for Arby, Kimi, and Aster Vale.
- This aggregate completes v1 only; v2 App execution still needs its own durable receipt.
- Raw transport output is quarantined outside the curated aggregate and should not be staged.
- Sibling lanes do not commit, push, delete, rebase, reset, or rewrite history.
- Aletheon remains the publication approver.

Next action: Resolve missing or invalid CLI lane receipts before v2 starts.
