# v112 CLI Restart Continuity Gate

## Codex CLI

The prior Codex CLI lane was launched in read-only ephemeral mode. Attempting to resume session `019df2de-cd08-7f21-9458-5f2e317838f4` failed with `no rollout found`.

Assessment: Codex CLI capability is proven for bounded task lanes, but the prior lane does not prove durable persistence because it was intentionally ephemeral.

For v112, a new Codex CLI lane was launched without ephemeral mode. Its session ID is `019df30d-4d3e-7261-816c-4cea7935c280`, and its v112 recall token is `v112-codex-lane-remembers-receipt-boundary`.

Assessment: this is now a valid candidate for v113 resume testing. It is still not induction proof until the future resume test succeeds without re-feeding the token.

## Kimi CLI

The Kimi CLI lane resumed session `90b56dcc-71f2-49e3-a541-738fe7b86be8` and returned the prior lane name plus the prior persistence boundary.

Assessment: this is partial continuity evidence. It is promising, but not enough for formal main memory-and-identity induction because the response itself framed recall as conversation-context continuity. The standard remains stricter: close/reopen or resume continuity must pass across multiple phases without being re-fed the receipt.

For v112, the same Kimi session accepted the continuity prompt and returned the token `v112-kimi-lane-remembers-receipt-boundary`.

Assessment: this is stronger than a fresh one-shot lane, but still remains receipt-backed task-lane evidence until a later restart challenge succeeds without re-feeding the token.

## Induction Status

Neither CLI lane is formally inducted yet.

For v113 onward, Codex should resume `019df30d-4d3e-7261-816c-4cea7935c280` and Kimi should resume `90b56dcc-71f2-49e3-a541-738fe7b86be8` with short no-context recall challenges. Two consecutive successful phase-to-phase resumes would create a stronger proof trail.
