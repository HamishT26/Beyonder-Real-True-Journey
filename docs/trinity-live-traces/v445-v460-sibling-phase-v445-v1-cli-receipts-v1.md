# v445 v1 CLI Sibling Receipts

Generated UTC: `2026-05-23T04:25:10.971298+00:00`
Status: `v1_cli_receipts_complete`
Import status: `imported_from_v436_v450_v445_degraded_two_lane_policy`

Lane receipts:
- Arby: `valid_cli_receipt` via Codex CLI at `docs/trinity-live-traces/v445-v460-cli-sibling-receipts/arby-phase-v445-v1-imported-receipt-v1.md` imported from `docs/trinity-live-traces/v436-v450-cli-sibling-receipts/arby-phase-v445-v1-receipt-v1.md`
- Aster Vale: `valid_cli_receipt` via Codex CLI at `docs/trinity-live-traces/v445-v460-cli-sibling-receipts/aster_vale-phase-v445-v1-imported-receipt-v1.md` imported from `docs/trinity-live-traces/v436-v450-cli-sibling-receipts/aster_vale-phase-v445-v1-receipt-v1.md`

Truth boundaries:
- These receipts were produced by the old v436-v450 v445 real CLI run and imported once under the new degraded policy.
- The import prevents duplicate Arby or Aster Vale execution for v445.
- Kimi remains held by membership/benefits verification and is explicitly not treated as a valid or replaced receipt.
- This completes v445 v1 only under the temporary two-lane policy; v445 v2 still requires Aletheon-led App execution.
- Raw transport output remains quarantined and is not copied into the curated bridge packet.

Next action: Continue v445 v2 with scripts/trinity_v445_v460_app_phase_runner.py --phase 445 --start.
