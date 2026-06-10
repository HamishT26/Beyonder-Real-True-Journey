# v500 GMUT/THOS v36 v3 x1 CLI CMD Launcher Helper Build

- generated_utc: `2026-06-07T14:10:25Z`
- overall_status: `PASS_CLI_CMD_LAUNCHER_HELPER_BUILT`
- helper_script: `scripts/thos_cli_direct_bridge_cmd_launcher.py`

Built a reusable Windows `.cmd` direct bridge launcher for existing read-only CLI lanes. The helper standardizes temp prompt files, temp runner files, Codex global option ordering, hidden process launch, redacted process IDs, and launch-safe receipt output.

Validated surfaces:

- Python compile passed.
- Help surface loaded.

Use policy: existing read-only CLI lanes only; publish status receipts only; do not read or publish raw prompt, stdout, stderr, session, screenshot, credential, or private dump content; run notifier, bridge repair, quality gate, and marker ledger only after cadence.

Retry 2 remains undisturbed until `2026-06-07T14:19:49Z`. GMUT, physics, consciousness, and canon gates remain open.
