# Trinity Command Book

- generated_utc: `2026-03-10T08:48:04+00:00`
- commands: `60`

| command_id | mode | risk | requires_live | connector |
|---|---|---|---|---|
| suite_run_standard | offline | low | False | - |
| suite_run_deep | offline | low | False | - |
| suite_run_collab | collab | medium | True | figma|linear|notion |
| suite_run_materialize_l1 | materialize | high | True | github|linear|notion|postgres |
| suite_run_materialize_l2 | materialize | high | True | github|linear|notion|postgres |
| suite_validate_manifest | offline | low | False | - |
| suite_validate_extensions | offline | low | False | - |
| suite_validate_command_book | offline | low | False | - |
| suite_validate_ladder | offline | low | False | - |
| suite_render_scoreboard | offline | low | False | - |
| connector_github_read_proof | collab | medium | True | github |
| connector_github_write_proof | materialize | high | True | github |
| connector_notion_read_proof | collab | medium | True | notion |
| connector_notion_write_proof | materialize | high | True | notion |
| connector_linear_read_proof | collab | medium | True | linear |
| connector_linear_write_proof | materialize | high | True | linear |
| connector_postgres_read_proof | collab | medium | True | postgres |
| connector_postgres_write_proof | materialize | high | True | postgres |
| connector_figma_read_refresh | collab | medium | True | figma |
| connector_status_board | offline | low | False | - |
| research_refresh_public_registry | offline | low | False | - |
| research_run_mind_board | offline | low | False | - |
| research_run_body_board | offline | low | False | - |
| research_run_heart_board | offline | low | False | - |
| research_run_api_constellation | offline | low | False | - |
| research_run_benchmark_refresh | collab | medium | True | - |
| research_search_arxiv_lane | collab | medium | True | - |
| research_refresh_governance_standards | collab | medium | True | - |
| research_update_comparative_grid | offline | medium | False | - |
| research_refresh_command_surface | collab | medium | True | - |
| recovery_reentry_sync | offline | low | False | - |
| recovery_inspect_system_wake | offline | low | False | - |
| recovery_inspect_docker_runtime | offline | medium | False | - |
| recovery_inspect_pg_container | offline | medium | False | postgres |
| recovery_inspect_command_ledger | offline | low | False | - |
| recovery_inspect_materialization_ledger | offline | low | False | - |
| recovery_rollback_dev_targets | offline | medium | False | - |
| recovery_verify_caches | offline | low | False | - |
| recovery_validate_control_tower | offline | low | False | - |
| recovery_dry_run_materialize | offline | medium | False | - |
| memory_write_reflection_entry | offline | low | False | - |
| memory_validate_log | offline | low | False | - |
| memory_refresh_personal_statement | offline | low | False | - |
| memory_refresh_next_plan | offline | low | False | - |
| memory_mirror_state_refresh | offline | medium | False | - |
| memory_inspect_authority_registry | offline | low | False | - |
| memory_inspect_memory_graph | offline | low | False | - |
| memory_inspect_corpus_index | offline | low | False | - |
| memory_reconcile_history | offline | medium | False | - |
| memory_inspect_control_tower | offline | low | False | - |
| autonomy_run_self_correction | offline | medium | False | - |
| autonomy_run_sentinel_manual | offline | medium | False | - |
| autonomy_run_semantic_firewall | offline | medium | False | - |
| autonomy_run_knowledge_graph | materialize | high | True | postgres |
| autonomy_run_dashboard_refresh | offline | low | False | - |
| autonomy_run_docker_pilot | materialize | high | True | postgres |
| autonomy_run_multi_agent_board | offline | medium | False | - |
| autonomy_run_operator_release | offline | medium | False | - |
| autonomy_run_future_readiness | offline | low | False | - |
| autonomy_run_command_pack_gates | offline | low | False | - |
