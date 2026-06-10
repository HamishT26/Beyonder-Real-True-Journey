# v504-gmut-thos-v40-v1-x2 Command-Surface Compatibility Queue

Generated UTC: `2026-06-08T22:49:18Z`

Status: `PASS_COMMAND_SURFACE_COMPATIBILITY_QUEUE_BUILT`

## Stable Versus Prerelease CLI Readiness

- Treat Codex CLI stable releases as default runner targets.
- Treat prerelease versions as research signals only until separately approved.
- Record release-channel observations in source ledgers before changing runner assumptions.
- Keep CLI output temp-only and publish status metrics, hashes, word counts, item counts, and quality status.
- If a stable release changes command behavior, run non-destructive help and sandbox probes before updating launchers.

## Surface Rows

- CLI release channel: stable default, prerelease watch only.
- CLI direct bridge: works with r2 long-form repair.
- App wrapper: requires direct repair fallback when completion receipt is missing.
