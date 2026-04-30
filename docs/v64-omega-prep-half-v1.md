# V64 Omega Prep Half

- First half state: `cooldown_prep_started`
- Goal: research, internalize, plan, and package extension candidates before suite load.
- Validation remains Deep plus Materialize L5 after prep and load gates are open.

## Extension Tasks
- Run wrangler_readonly_probe as identity/status only; no worker or Pages creation.
- Run cloudflare_pages_probe as list/read capability proof with account details redacted.
- Run d1_schema_dry_run against local schema files only; no D1 database creation.
- Run r2_inventory_probe as read-only capability check or blocker truth.
- Create workers_ai_capability_card from CLI/docs/cache evidence only; no inference call without confirmation.
- Run vercel_static_probe as missing-CLI or read-only status only.
- Run render_static_probe as missing-CLI or read-only status only.
- Run neon_readonly_state as missing-CLI or read-only status only.
- Run circleci_config_probe as config validation/read status only; no pipeline trigger.
- Run github_pr_truth_sync_readonly and preserve PR body edit gate.
- Record google_drive_operator_hold_receipt and keep Drive non-authoritative.
- Carry V63 cooldown notes into V64 validation gate.
- Start V64 provider readiness review during V63 cooldown only.
- Prepare Cloudflare/Vercel/Render/Neon read-only cards without live writes.
- Block V64 Deep and L5 until V63 is complete and V64 prep is complete.

## Safety Gates
- No raw secrets are read into committed artifacts.
- No Kimi/Codex CLI external sibling induction without receipt proof and explicit action-time confirmation for data transmission.
- No Docker Desktop, local Kubernetes, cloud resource creation, Notion live write, or PR body edit without a fresh gate.
