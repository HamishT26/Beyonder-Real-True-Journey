# v436 v1 CLI Sibling Receipts

Generated UTC: `2026-05-22T19:57:13.215349+00:00`
Status: `v1_cli_receipts_complete`
Import status: `imported_from_v421_v440_v436`

Lane receipts:
- Arby: `valid_cli_receipt` via Codex CLI at `docs/trinity-live-traces/v436-v450-cli-sibling-receipts/arby-phase-v436-v1-imported-receipt-v1.md` imported from `docs/trinity-live-traces/v421-v440-cli-sibling-receipts/arby-phase-v436-v1-receipt-v1.md`
- Kimi: `valid_cli_receipt` via Kimi CLI at `docs/trinity-live-traces/v436-v450-cli-sibling-receipts/kimi-phase-v436-v1-imported-receipt-v1.md` imported from `docs/trinity-live-traces/v421-v440-cli-sibling-receipts/kimi-phase-v436-v1-receipt-v1.md`
- Aster Vale: `valid_cli_receipt` via Codex CLI at `docs/trinity-live-traces/v436-v450-cli-sibling-receipts/aster_vale-phase-v436-v1-imported-receipt-v1.md` imported from `docs/trinity-live-traces/v421-v440-cli-sibling-receipts/aster_vale-phase-v436-v1-receipt-v1.md`

Truth boundaries:
- These receipts were produced by the old v421-v440 v436 real CLI run and imported once.
- The import prevents duplicate Arby, Kimi, or Aster Vale execution for v436.
- This completes v436 v1 only; v436 v2 still requires Aletheon-led App execution.
- Raw transport output remains quarantined and is not copied into the curated bridge packet.

Next action: Continue v436 v2 with scripts/trinity_v436_v450_app_phase_runner.py --phase 436 --start.
