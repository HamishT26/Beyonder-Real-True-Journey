# v497 GMUT/THOS v33 v6 x1 Watcher Callback Map

- overall_status: `PASS_WATCHER_CALLBACK_MAP_READY`
- generated_utc: `2026-06-06T21:02:33Z`

## Callback Rows

- `prelaunch`: verify prompt policy, exact headings, stale-authority handoff, and launch scope before lanes start.
- `postlaunch`: record app background watcher and CLI temp-only launch metadata without raw outputs.
- `cadence`: prevent manual polling before the 15-minute x1 mark and 10-minute x2 mark.
- `completion`: harvest final-message and app completion receipts at approved marks only.
- `quality`: gate CLI output by words, exact headings, category counts, and hard raw/private markers.
- `repair`: classify gaps as prompt repair, stale-authority blocker, app wait, final-message wait, or approval-needed mutation.
- `publication`: parse, scan, exact-stage, commit, push, and remote-verify curated artifacts only.

All GMUT and canon gates remain open. No raw/private material is published.
