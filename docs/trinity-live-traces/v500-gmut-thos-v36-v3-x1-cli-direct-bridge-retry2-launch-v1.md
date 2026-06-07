# v500 GMUT/THOS v36 v3 x1 CLI Direct Bridge Retry 2 Launch

- generated_utc: `2026-06-07T14:04:49Z`
- overall_status: `PASS_RETRY2_DIRECT_BRIDGE_CLI_LANES_LAUNCHED`
- next_manual_status_check_not_before_utc: `2026-06-07T14:19:49Z`

Retry 1 reached its cadence with missing bridge sources. Retry 2 switches to temp `.cmd` runner files so Windows quoting is owned by a stable launch script instead of a long `Start-Process` argument string.

Safe bridge names:

- Arby: `ArbyDirectV3R2`
- Aster Vale: `AsterValeDirectV3R2`

Launch-health observation: event and stderr surfaces exist; final-message files are still pending. No raw prompts, raw sibling text, local temp paths, stdout/stderr, screenshots, credentials, session streams, or private dumps are published. No phase advancement is allowed until all five lanes are receipt-backed.
