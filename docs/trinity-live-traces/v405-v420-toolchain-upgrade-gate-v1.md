# v405-v420 Toolchain Upgrade Gate

Generated UTC: 2026-05-21T19:54:42.9951349Z

## Status

Safe updates applied and audited after v405 was published at `29b06aa487`.

## Updated

- Codex CLI: `codex-cli 0.132.0` -> `codex-cli 0.133.0` using `npm install -g @openai/codex@0.133.0`.
- npm: `11.14.1` -> `11.15.0` using `npm install -g npm@11.15.0`.

## Audited

- GitHub CLI: `gh version 2.92.0 (2026-04-28)`; winget reported no available upgrade.
- Kimi CLI: `kimi, version 1.44.0`; no clean local self-update command was exposed by help output, so no opaque installer action was taken.
- Git: `git version 2.53.0.windows.1`.
- Node: `v24.15.0`.

## Boundaries

- Codex app desktop update was treated as user-refreshed app state; this gate verified the local CLI path only.
- Tool updates do not replace the required Arby, Kimi, and Aster Vale CLI receipt gate.
- No paid-provider, cloud, Gmail, Drive, OAuth, or external-service mutation was performed.
