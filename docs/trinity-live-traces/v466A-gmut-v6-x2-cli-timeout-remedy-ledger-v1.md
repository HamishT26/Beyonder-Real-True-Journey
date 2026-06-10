# v466A GMUT v6 x2 CLI Timeout Remedy Ledger

Status: CLI_TIMEOUT_REMEDY_RECORDED

Prepared: 2026-06-01T04:30:28+12:00

The v6 x1 CLI advisory calls exceeded the 300000 ms cap. The safe remedy is to avoid fabricating missing advisories, keep metadata separate from content, and use narrower bounded retries before future long CLI runs.

This is a workflow blocker, not a physics result. All six GMUT gates remain open.
