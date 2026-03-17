# Trinity API Book

- generated_utc: `2026-03-17T04:12:19+00:00`
- apis: `34`

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
| openai_official | public_vendor | official_primary | public_no_auth | `scripts/trinity_api_shortcuts.py show openai_official` |
| nvidia_official | public_vendor | official_primary | public_no_auth | `scripts/trinity_api_shortcuts.py show nvidia_official` |
| google_quantum_ai | public_vendor | official_primary | public_no_auth | `scripts/trinity_api_shortcuts.py show google_quantum_ai` |
| ibm_quantum_research | public_vendor | official_primary | public_no_auth | `scripts/trinity_api_shortcuts.py show ibm_quantum_research` |
| quantinuum | public_vendor | official_primary | public_no_auth | `scripts/trinity_api_shortcuts.py show quantinuum` |
| w3c_did_core_v13 | public_standard | official_primary | public_no_auth | `scripts/trinity_api_shortcuts.py show w3c_did_core_v13` |
| w3c_vc_data_model_v13 | public_standard | official_primary | public_no_auth | `scripts/trinity_api_shortcuts.py show w3c_vc_data_model_v13` |
| nist_ai_rmf_v13 | public_standard | official_primary | public_no_auth | `scripts/trinity_api_shortcuts.py show nist_ai_rmf_v13` |
| oecd_ai_principles_v13 | public_standard | official_primary | public_no_auth | `scripts/trinity_api_shortcuts.py show oecd_ai_principles_v13` |
| eu_ai_act_v13 | public_standard | official_primary | public_no_auth | `scripts/trinity_api_shortcuts.py show eu_ai_act_v13` |
| nz_justice_treaty_context_v13 | public_standard | official_primary | public_no_auth | `scripts/trinity_api_shortcuts.py show nz_justice_treaty_context_v13` |
| world_bank_governance_v13 | public_standard | official_primary | public_no_auth | `scripts/trinity_api_shortcuts.py show world_bank_governance_v13` |
| openai_codex_intro_v14 | public_vendor | official_primary | public_no_auth | `scripts/trinity_api_shortcuts.py show openai_codex_intro_v14` |
| openai_codex_help_v14 | public_vendor | official_primary | public_no_auth | `scripts/trinity_api_shortcuts.py show openai_codex_help_v14` |
| codex_subagent_adapter_v14 | repo_operator | repo_authoritative | repo_only | `scripts/trinity_api_shortcuts.py codex-adapter-status --json` |
| control_tower_v14 | repo_operator | repo_authoritative | repo_only | `scripts/trinity_api_shortcuts.py control-tower-status --json` |
| council_roster_v14 | repo_operator | repo_authoritative | repo_only | `scripts/trinity_api_shortcuts.py council-roster-status --json` |
| subagent_registry_v14 | repo_operator | repo_authoritative | repo_only | `scripts/trinity_api_shortcuts.py subagent-status --json` |
| multi_instance_registry_v14 | repo_operator | repo_authoritative | repo_only | `scripts/trinity_api_shortcuts.py multi-instance-status --json` |
| v14_verdict_v14 | repo_operator | repo_authoritative | repo_only | `scripts/trinity_api_shortcuts.py show v14_verdict_v14` |
