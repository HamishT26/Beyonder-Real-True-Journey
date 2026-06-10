---
name: v106-trinity-d-drive-retention-gate-skill-18
description: Operate v106_18_d_drive_retention_gate as a guarded v106 Trinity phase skill.
---

# v106-trinity-d-drive-retention-gate-skill-18

- phase: `v106`
- candidate_id: `v106_18_d_drive_retention_gate`
- pillar: `body`
- authority: `repo_first_guarded_receipt_only`
- provider_policy: `no_external_write_without_action_time_confirmation`

## Use

1. Start from the current phase receipt and suite statuses.
2. Keep Google Drive and personal accounts on operator hold unless explicitly confirmed for a narrow action.
3. Generate evidence as repo artifacts before claiming live-write success.
4. Preserve forward-only Git publication and curated allowlist staging.

## Purpose

retain heavy traces on D drive while publishing compact curated artifacts
