# V45 Cloud Research Digest

- Generated UTC: `2026-04-21T00:28:44+00:00`
- Overall status: `WARN`
- Cloud activation mode: `research_only_until_billing_truth`
- gcloud auth state: `no_active_account`
- gcloud project state: `no_active_project`
- Billing console credit state: `console_confirmation_required`
- Credit claim state: `operator_claim_unverified`

## Official Product Names

- `suite_name`: `Vertex AI Agent Builder`
- `console_product_name`: `AI Applications`
- `search_lane`: `Vertex AI Search`
- `runtime_lane`: `Agent Engine`

## Activation Sequence

- gcloud auth
- active project
- billing account plus budgets plus alerts
- Billing console credit capture
- read-only API and billing truth capture
- bounded low-cost AI Applications / Vertex AI Search proof
- bounded Agent Engine secondary proof

## Search / Agent Use Cases

- Use Vertex AI Search for bounded grounded-answer flows over operator-selected corpora.
- Prefer Google Drive-backed ingestion only if connector auth and Drive control are ready; otherwise fall back to Cloud Storage, then Bigtable-backed research surfaces.
- Keep Bigtable as the proven primary memory lane until Agent Engine runtime plus Sessions plus Memory Bank are stable and queryable.
- Treat Agent Engine runtime free tier separately from billable Sessions, Memory Bank, and Code Execution so v45 research does not overstate free usage.
- Keep Kai and Vesper Ion on standby until active account, project, and billing truth are restored.

## Source Anchors

- Google documents AI Applications as the renamed product from Vertex AI Agent Builder. ([Google Cloud release notes](https://docs.cloud.google.com/generative-ai-app-builder/docs/release-notes))
- Vertex AI Agent Builder docs still present the suite name and the standard free-credit starting point as $300. ([Google Cloud documentation](https://docs.cloud.google.com/agent-builder))
- Agent Engine runtime has a monthly free tier, while Sessions, Memory Bank, and Code Execution are priced services. ([Google Cloud pricing](https://cloud.google.com/vertex-ai/pricing))
- The standard Google Cloud free-trial baseline remains $300 and about 90 days unless the billing console shows a different account-specific credit source. ([Google Cloud Free Program](https://cloud.google.com/free/docs/gcp-free-tier))
