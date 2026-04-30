# v65-v75-live-write-governor-v1

```json
{
  "generated_utc": "2026-04-30T04:50:22+00:00",
  "phase": "v65_v75_hybrid_omega",
  "live_write_phases": [
    "v70",
    "v73",
    "v75"
  ],
  "budget_policy": {
    "ceiling_fraction_per_provider": 0.3,
    "spend_target_is_ceiling_not_requirement": true,
    "record_before_after_usage_when_provider_exposes_usage": true
  },
  "allowed_provider_classes": [
    "test_or_preview_projects",
    "sandbox_or_ephemeral_compute",
    "repo_publication_and_receipts",
    "dashboard_or_database_surfaces_with_rollback_receipts"
  ],
  "blocked_without_fresh_operator_confirmation": [
    "production_dns_or_domain_mutation",
    "account_setting_changes",
    "personal_email_or_calendar_mutation",
    "google_drive_content_mutation",
    "resource_deletion_outside_repo_curated_cleanup",
    "raw_secret_transmission_to_external_models"
  ],
  "providers": [
    {
      "provider": "github",
      "mode_before_live_phase": "readiness_probe_only",
      "live_phase_requirement": "dry_run_preview_then_write_then_verify_then_rollback_receipt",
      "budget_ceiling_fraction": 0.3
    },
    {
      "provider": "vercel",
      "mode_before_live_phase": "readiness_probe_only",
      "live_phase_requirement": "dry_run_preview_then_write_then_verify_then_rollback_receipt",
      "budget_ceiling_fraction": 0.3
    },
    {
      "provider": "cloudflare",
      "mode_before_live_phase": "readiness_probe_only",
      "live_phase_requirement": "dry_run_preview_then_write_then_verify_then_rollback_receipt",
      "budget_ceiling_fraction": 0.3
    },
    {
      "provider": "neon",
      "mode_before_live_phase": "readiness_probe_only",
      "live_phase_requirement": "dry_run_preview_then_write_then_verify_then_rollback_receipt",
      "budget_ceiling_fraction": 0.3
    },
    {
      "provider": "render",
      "mode_before_live_phase": "readiness_probe_only",
      "live_phase_requirement": "dry_run_preview_then_write_then_verify_then_rollback_receipt",
      "budget_ceiling_fraction": 0.3
    },
    {
      "provider": "e2b",
      "mode_before_live_phase": "readiness_probe_only",
      "live_phase_requirement": "dry_run_preview_then_write_then_verify_then_rollback_receipt",
      "budget_ceiling_fraction": 0.3
    },
    {
      "provider": "oracle",
      "mode_before_live_phase": "readiness_probe_only",
      "live_phase_requirement": "dry_run_preview_then_write_then_verify_then_rollback_receipt",
      "budget_ceiling_fraction": 0.3
    },
    {
      "provider": "notion",
      "mode_before_live_phase": "readiness_probe_only",
      "live_phase_requirement": "dry_run_preview_then_write_then_verify_then_rollback_receipt",
      "budget_ceiling_fraction": 0.3
    }
  ]
}
```
