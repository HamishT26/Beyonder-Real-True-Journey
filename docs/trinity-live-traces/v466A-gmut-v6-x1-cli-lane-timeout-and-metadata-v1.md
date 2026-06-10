# v466A GMUT v6 x1 CLI Lane Timeout And Metadata

Status: CLI_METADATA_RECORDED_ADVISORY_TIMEOUT

Prepared: 2026-06-01T04:23:20+12:00

Arby and Aster Vale were contacted under non-ephemeral read-only boundaries. Their lane metadata checks succeeded, but the advisory calls exceeded the 300000 ms cap. No CLI advisory content is used or fabricated for this phase.

## Metadata

- Arby: branch `ghc/arby-advisory-line`, local and upstream head `54b365446b8b334a59407c8a0a85f93ca19fa12b`, drift `0 0`, clean tracked status, `codex-cli 0.135.0`.
- Aster Vale: branch `ghc/aster-vale-advisory-line`, local and upstream head `7c0576c6c98529e6ec80913c9de6a757956c0a47`, drift `0 0`, clean tracked status, `codex-cli 0.135.0`.

All six GMUT gates remain open.
