# v499 GMUT/THOS v35 v8 x2 Live Bridge Helper Proof Synthesis

- generated_utc: `2026-06-07T11:35:19Z`
- overall_status: `PASS_LIVE_BRIDGE_HELPER_PROOF_READY`
- helper: `thos_cli_bridge_surface_repair.py`

The bridge helper now has both synthetic proof and live v8 x1 proof. It repaired Arby and Aster Vale temp-only direct bridge outputs into expected notifier filenames, after which both lanes passed the notifier and strict elaboration quality gates.

The helper is now the default repair step after cadence when direct bridge raw outputs exist but expected notifier files are missing.
