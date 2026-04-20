# V44 Codex Capability Audit

- Generated UTC: `2026-04-20T04:12:13+00:00`
- Overall status: `WARN`
- Codex capability audit state: `capabilities_verified_with_residuals`
- Browser iteration state: `codex_browser_supported_playwright_fallback_available`
- Computer use state: `unsupported_windows_launch_scope`
- Automation backend state: `windows_task_scheduler_authoritative`
- Repo-local model resolution state: `repo_local_fallback_lower_than_global_intent`

## Target Plugins

- `GitHub`: config=`True`, callable=`True`, status=`callable_in_session`
- `Google Drive`: config=`True`, callable=`True`, status=`callable_in_session`
- `Notion`: config=`True`, callable=`False`, status=`blocked_missing_connector`
- `Gmail`: config=`True`, callable=`False`, status=`blocked_missing_connector`
- `Figma`: config=`True`, callable=`False`, status=`blocked_missing_connector`
- `Render`: config=`True`, callable=`False`, status=`blocked_missing_connector`
- `Expo`: config=`True`, callable=`False`, status=`blocked_missing_connector`
- `Vercel`: config=`True`, callable=`False`, status=`blocked_missing_connector`
- `CircleCI`: config=`True`, callable=`False`, status=`blocked_missing_connector`
- `Neon Postgres`: config=`True`, callable=`False`, status=`blocked_missing_connector`
- `Superpowers`: config=`True`, callable=`False`, status=`blocked_missing_connector`

## Blockers

- Notion is enabled in config but is not callable from the live V44 session surface.
- Gmail is enabled in config but is not callable from the live V44 session surface.
- Figma is enabled in config but is not callable from the live V44 session surface.
- Render is enabled in config but is not callable from the live V44 session surface.
- Expo is enabled in config but is not callable from the live V44 session surface.
- Vercel is enabled in config but is not callable from the live V44 session surface.
- CircleCI is enabled in config but is not callable from the live V44 session surface.
- Neon Postgres is enabled in config but is not callable from the live V44 session surface.
- Superpowers is enabled in config but is not callable from the live V44 session surface.
- Repo-local custom-agent resolution is `gpt-5.1-codex-max` while the broader V44 intent remains `gpt-5.4`.
