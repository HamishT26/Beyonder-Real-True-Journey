# v477 THOS v5 x2 Command Approval Queues

- command_count: `684`
- live_write_approval_required: `88`
- connector_approval_required: `76`
- offline_low_risk_candidate: `216`
- execution_policy: metadata-only; no command execution.

## Live Approval Queue Sample
- suite_run_collab: Run collaboration-safe live reads only.
- suite_run_materialize_l1: Run materialize at disposable staging.
- suite_run_materialize_l2: Run materialize at persistent dev.
- connector_github_read_proof: Refresh GitHub live-read proof.
- connector_github_write_proof: Run GitHub write tracer in approved scope.
- connector_notion_read_proof: Refresh Notion read bridge.
- connector_notion_write_proof: Run Notion write tracer in approved scope.
- connector_linear_read_proof: Refresh Linear collaboration bridge.
- connector_linear_write_proof: Run Linear write tracer in approved scope.
- connector_postgres_read_proof: Refresh Postgres local runtime bridge.
- connector_postgres_write_proof: Run Postgres write tracer in approved scope.
- connector_figma_read_refresh: Refresh Figma read-live cache.

## Connector Queue Sample
- suite_run_collab: Run collaboration-safe live reads only.
- suite_run_materialize_l1: Run materialize at disposable staging.
- suite_run_materialize_l2: Run materialize at persistent dev.
- connector_github_read_proof: Refresh GitHub live-read proof.
- connector_github_write_proof: Run GitHub write tracer in approved scope.
- connector_notion_read_proof: Refresh Notion read bridge.
- connector_notion_write_proof: Run Notion write tracer in approved scope.
- connector_linear_read_proof: Refresh Linear collaboration bridge.
- connector_linear_write_proof: Run Linear write tracer in approved scope.
- connector_postgres_read_proof: Refresh Postgres local runtime bridge.
- connector_postgres_write_proof: Run Postgres write tracer in approved scope.
- connector_figma_read_refresh: Refresh Figma read-live cache.
