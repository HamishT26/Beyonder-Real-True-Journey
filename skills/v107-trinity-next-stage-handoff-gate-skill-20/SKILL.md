---
name: v107-trinity-next-stage-handoff-gate-skill-20
description: Operate v107_20_next_stage_handoff_gate as a guarded v107 Trinity phase skill.
---

# v107-trinity-next-stage-handoff-gate-skill-20

- phase: `v107`
- candidate_id: `v107_20_next_stage_handoff_gate`
- pillar: `trinity`
- authority: `repo_first_guarded_receipt_only`
- provider_policy: `no_external_write_without_action_time_confirmation`

## Use

1. Start from the current phase receipt and suite statuses.
2. Keep Google Drive and personal accounts on operator hold unless explicitly confirmed for a narrow action.
3. Generate evidence as repo artifacts before claiming live-write success.
4. Preserve forward-only Git publication and curated allowlist staging.

## Purpose

derive each next stage from the current closeout, not a stale global plan
