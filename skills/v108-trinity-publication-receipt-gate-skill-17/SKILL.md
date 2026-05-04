---
name: v108-trinity-publication-receipt-gate-skill-17
description: Operate v108_17_publication_receipt_gate as a guarded v108 Trinity phase skill.
---

# v108-trinity-publication-receipt-gate-skill-17

- phase: `v108`
- candidate_id: `v108_17_publication_receipt_gate`
- pillar: `body`
- authority: `repo_first_guarded_receipt_only`
- provider_policy: `no_external_write_without_action_time_confirmation`

## Use

1. Start from the current phase receipt and suite statuses.
2. Keep Google Drive and personal accounts on operator hold unless explicitly confirmed for a narrow action.
3. Generate evidence as repo artifacts before claiming live-write success.
4. Preserve forward-only Git publication and curated allowlist staging.

## Purpose

require post-push remote/local equality before declaring cloud live write success
