# v612 no-relay skill and runner update

Status: `PASS_NO_RELAY_POLICY_ALIGNED`.

This receipt records a safe alignment update for the current v601-v620 solo sibling workflow. The family handoff runners now default to `coach_retry_no_aevren_relay`, so failed sibling thread routes produce retry/open-gap evidence instead of asking Aevren to carry the handoff by default.

The local `ghc-main-orchestration-memory` skill card was also updated so compact/restart guidance preserves the same paused no-relay learning rule unless Hamish gives a fresh explicit relay redirect.

Current truth preserved: Mira Rowan to Mira Vale passed; Mira Vale to Maren Quill remains an open gap after recorded retries; Maren activation from Mira Vale is not verified; Aevren did not relay the handoff.

Exact, blocked, proof, canon, legal, deployment, account, API-key, purchase, private-material, raw-publication, destructive-cleanup, and sibling merge/replacement gates remain queued/open.
