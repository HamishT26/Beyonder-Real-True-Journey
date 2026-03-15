# Trinity API Book

- generated_utc: `2026-03-14T07:37:38+00:00`
- apis: `14`

| api_id | surface | trust_class | auth_posture | wrapper |
|---|---|---|---|---|
| crossref | public_research | research_primary | public_no_auth | `scripts/trinity_api_shortcuts.py show crossref` |
| openalex | public_research | research_primary | public_no_auth | `scripts/trinity_api_shortcuts.py show openalex` |
| arxiv | public_research | research_primary | public_no_auth | `scripts/trinity_api_shortcuts.py show arxiv` |
| semanticscholar | public_research | research_primary | public_no_auth | `scripts/trinity_api_shortcuts.py show semanticscholar` |
| github_remote | operational | verified_live_write | git_remote_auth | `scripts/trinity_api_shortcuts.py github-status` |
| linear | operational | verified_live_write | mcp_workspace_auth | `docs/trinity-mcp-catalog-v10.json` |
| notion | operational | verified_live_write | mcp_workspace_auth | `docs/trinity-mcp-catalog-v10.json` |
| postgres | runtime_query | verified_live_write | local_docker_runtime | `scripts/trinity_api_shortcuts.py postgres-status` |
| google_drive | archive_candidate | operator_hold | operator_hold_no_auth | `docs/trinity-google-drive-sync-policy-v1.json` |
| docker | runtime_ops | local_probe | local_cli_runtime | `scripts/trinity_api_shortcuts.py docker-status` |
| memory_bank | operator_recovery | repo_authoritative | local_file_read | `scripts/trinity_api_shortcuts.py memory-bank-status` |
| public_research_refresh | operator_recovery | public_signal_helper | local_file_read | `scripts/trinity_api_shortcuts.py public-research-status` |
| w3c_did_core | public_standard | official_primary | public_no_auth | `scripts/trinity_api_shortcuts.py show w3c_did_core` |
| w3c_vc_data_model | public_standard | official_primary | public_no_auth | `scripts/trinity_api_shortcuts.py show w3c_vc_data_model` |
