# v499 GMUT/THOS v35 v5 x2 CLI No-Space Bridge Template

- generated_utc: `2026-06-07T09:01:42Z`
- overall_status: `PASS_CLI_NO_SPACE_BRIDGE_TEMPLATE_BUILT`

## Evidence

Aster Vale's first v5 x1 CLI attempt failed at transport level because the spaced output filename broke argument parsing. The no-space bridge produced a valid Aster artifact, and the bridge copy made it visible to the notifier. Aster then passed with `3807` words, `12` items per required category, and zero strict sensitive/path markers.

## Template

- Use safe no-space internal filenames for lane display names.
- Feed prompts through stdin.
- Disable plugins for strict CLI advisory lane runs.
- Keep raw output temp-only.
- Wait for a non-empty bridge output before copying into the expected notifier filename.
- Publish only hashes, counts, status, and quality metrics.
