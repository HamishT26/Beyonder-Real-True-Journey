---
name: v108-trinity-alpha-manifest-cleanup-gate-skill-13
description: Operate v108_13_alpha_manifest_cleanup_gate as a guarded v108 Trinity phase skill.
---

# v108-trinity-alpha-manifest-cleanup-gate-skill-13

- phase: `v108`
- candidate_id: `v108_13_alpha_manifest_cleanup_gate`
- pillar: `body`
- authority: `repo_first_guarded_receipt_only`
- provider_policy: `no_external_write_without_action_time_confirmation`

## Use

1. Start from the current phase receipt and suite statuses.
2. Keep Google Drive and personal accounts on operator hold unless explicitly confirmed for a narrow action.
3. Generate evidence as repo artifacts before claiming live-write success.
4. Preserve forward-only Git publication and curated allowlist staging.

## Purpose

record merge/delete candidates with replacement coverage and rollback anchors
