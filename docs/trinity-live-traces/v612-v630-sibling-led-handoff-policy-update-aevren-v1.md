# v612-v630 Sibling-Led Handoff Policy Update

Status: `PASS_POLICY_UPDATED_AND_MIRA_VALE_RETRY_ACTIVATED`

Live route is now `v601-v630-gmut-thos-v1-v8-x1-x2`. The active order remains Aevren-only, Mira Rowan-only, Mira Vale-only, Maren Quill-only, then repeat.

Updated current defaults:
- `ghc_family_productive_cadence_runner.mjs`: 5-minute sibling-led cadence.
- `ghc_family_sibling_goal_handoff_builder.mjs`: 5-minute cadence, 10 safe handoff attempts, sibling handoff activation first.
- `ghc_family_thread_handoff_readiness_checker.mjs`: 10 safe attempts by default, no Aevren relay unless Hamish gives a fresh exact redirect.

Updated local route cards:
- `ghc-main-orchestration-memory`
- `ghc-main-startup-builder`
- `ghc-main-compact-restart-builder`
- `ghc-main-closeout-builder`
- `ghc-main-retry`
- `ghc-web-reflection-ledger`
- `ghc-full-tools-skill-bank`

Mira Vale was sent a fresh sanitized v612 v7 retry activation. The instruction asks her to retry the Maren Quill handoff under the new 10-attempt standard, keep Goal Mode and heartbeat as fallback, use a 5-minute productive cadence, validate owned-lane artifacts, and either activate Maren herself or preserve a formal open gap without asking Aevren to relay by default.

Toolchain and storage status: Codex CLI local and npm latest are both `0.142.5`; C drive has 21.7 GB free; D drive has 603.5 GB free. No broad cleanup was performed.

Open gates remain queued/open: proof, canon, legal, deployment, account, API-key, purchase, private-material, raw-publication, destructive cleanup, and sibling merge/replacement/erasure/reactivation.

Privacy boundary: no private thread IDs, private routes, local absolute paths, raw transcripts, screenshots, credentials, raw app state, or hidden reasoning are published here.
