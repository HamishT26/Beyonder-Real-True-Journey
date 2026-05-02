# v86-live-write-preflight-v1

```json
{
  "generated_utc": "2026-05-02T15:50:59+00:00",
  "phase": "v86_beta_alpha_omega",
  "live_write_mode": "guarded_repo_publication_only",
  "online_live_write_free_memory_floor_kb": 358400,
  "browser_free_memory_floor_kb": 409600,
  "online_live_write_policy": "allowed at or above 350 MB for repo and GitHub receipt writes only; provider and account writes remain blocked without a fresh sandbox receipt",
  "browser_use_policy": "allowed at or above 400 MB when the browser task is worth the extra host load",
  "allowed_live_writes": [
    "repo_artifact_generation",
    "curated_git_commit",
    "github_branch_push_after_diff_check_and_secret_scan",
    "publication_receipt_regeneration_after_push"
  ],
  "blocked_without_fresh_operator_confirmation": [
    "google_drive_content_mutation",
    "gmail_or_personal_email_send",
    "calendar_event_mutation",
    "account_setting_change",
    "production_dns",
    "provider_billing_change",
    "raw_secret_transmission"
  ],
  "required_receipt_chain": [
    "beta_plan",
    "alpha_record_only_audit",
    "candidate_direct_sweep",
    "manifest_validation",
    "deep_suite",
    "materialize_l5_suite",
    "curated_stage_allowlist",
    "git_diff_cached_check",
    "credential_pattern_scan",
    "write_receipt",
    "remote_head_verification"
  ]
}
```
