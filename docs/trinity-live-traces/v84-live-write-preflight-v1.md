# v84 live-write preflight

```json
{
  "generated_utc": "2026-05-01T05:51:10+00:00",
  "phase": "v84",
  "live_write_mode": "guarded_repo_publication_only",
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
    "dry_run_preview_receipt",
    "curated_stage_allowlist",
    "git_diff_cached_check",
    "credential_pattern_scan",
    "write_receipt",
    "remote_head_verification",
    "rollback_or_forward_fix_note"
  ]
}
```
