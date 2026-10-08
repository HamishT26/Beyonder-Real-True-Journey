# GHC Nexus Hub 2.5

This release adds readable interactive outbox delivery states, includes valid ChatGPT null-host receipts, and removes the twelve blanket MCP disable overrides and App disable override from new CLI launch plans. New sessions inherit client configuration. Existing sessions keep their original settings. Same-host registration, transport and authentication still determine tool availability.

The Config Menu plugin 0.1.2 now reports deprecated Guardian thread_context keys, including profiles. The separate config_guard.py offers read-only audit, a fingerprint-bound repair preview, and explicit repair with a verified private backup. Only this obsolete key may change; unsupported syntax or concurrent edits are retained for review. It does not continuously watch config files or refresh an already-open Settings page. Both selected live local configs were clean during this release check.

Exec plugin 0.1.4 pins fifteen runtime modules, including the delivery panel. No new lifecycle hook registration was added.

Validation: 28 Python configuration checks passed; 42 outbox/UX checks passed; the final delivery panel passed20 checks including3 added ChatGPT-host cases. The separate75-case Hub/MCP suite initially passed72 with3 timing failures under low free RAM. All3 exact failing cases subsequently passed individually with their original timeout limits. The earlier filtered wrapper that reported only1 aggregate file result is not counted as recovery. Tests overlap where rerun; do not add all invocation counts as independent cases.

The installed patch retains an exact backup, does not restart the App, start WSL, create model sessions or copy credentials. The current run3 x1 bank records peer research, launch authorization and remaining runtime gaps.

Independent review follow-up: Orenna found that diagnostics alone did not prevent an ordinary display-setting proposal from being marked ready while a selected active layer still contained the retired key. Proposals now remain held until that key is cleaned. Inactive layers retain visible diagnostics without claiming active precedence. Two focused regressions cover this distinction. The initially committed2.5 candidate and the follow-up correction remain separate Git commits.
