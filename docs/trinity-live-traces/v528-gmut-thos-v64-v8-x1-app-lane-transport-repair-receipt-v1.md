# v528-gmut-thos-v64-v8-x1 App-Lane Transport Repair Receipt

Status: `PASS_TRANSPORT_REPAIR_COMPILED_AND_PROBED`

The app-lane notifier was repaired so local app-server transport failures become sanitized receipt rows instead of hard crashes. The repair added direct app-server launch first, retained the Windows command fallback, checks process health before writes, catches broken or invalid stdin writes, and records transport failure classes without publishing raw app-server payloads.

Validation result:

- Python compile: `PASS`.
- Direct probe receipt: `v528-gmut-thos-v64-v8-x1-kierkegaard-aristotle-direct-app-notifier-probe-retry11-v1.json`.
- App-server initialize: `PASS`.
- Existing thread read: `PASS_BOTH_APP_LANES`.
- Existing thread resume: `OPEN_GAP_TIMEOUT_BOTH_APP_LANES`.

Boundary:

- Existing app threads only.
- No new thread creation.
- No old-style spawning.
- No raw thread IDs, callable IDs, lane text, app-server payloads, session streams, screenshots, credentials, or local absolute paths are published.
- Phase completion is not claimed; all GMUT gates remain open.
