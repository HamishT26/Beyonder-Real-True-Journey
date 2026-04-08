# V35 Gemini CLI Proof

- Generated UTC: `2026-04-06T15:31:14+00:00`
- Overall status: `PASS`
- Proof state: `authenticated_headless_identity_verified_with_cli_assertion`
- Selected route: `gemini-2.5-flash`
- Identity captured: `True`
- Promotion gate ready: `True`

## Completed Steps

- `node_detected`
- `npm_detected`
- `npx_detected`
- `help_invocation_verified`
- `authenticated_headless_prompt_verified`

## Route Attempts

- `pro` -> returncode `1` / state `not_exposed`
- `gemini-2.5-pro` -> returncode `1` / state `not_exposed`
- `gemini-2.5-flash` -> returncode `3221226505` / state `verified_with_teardown_bug`

## Blockers

- The live Gemini CLI identity proof succeeded, but the process exited through a known Windows async teardown assertion after printing the valid JSON payload.
- Higher Gemini CLI routes were not exposed in this account/region, so the live proof promoted the bounded flash fallback path instead.
