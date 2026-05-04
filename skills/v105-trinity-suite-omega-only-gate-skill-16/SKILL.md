---
name: v105-trinity-suite-omega-only-gate-skill-16
description: Operate v105_16_suite_omega_only_gate as a guarded v105 Trinity phase skill.
---

# v105-trinity-suite-omega-only-gate-skill-16

- phase: `v105`
- candidate_id: `v105_16_suite_omega_only_gate`
- pillar: `trinity`
- authority: `repo_first_guarded_receipt_only`
- provider_policy: `no_external_write_without_action_time_confirmation`

## Use

1. Start from the current phase receipt and suite statuses.
2. Keep Google Drive and personal accounts on operator hold unless explicitly confirmed for a narrow action.
3. Generate evidence as repo artifacts before claiming live-write success.
4. Preserve forward-only Git publication and curated allowlist staging.

## Purpose

run Deep and L5 suites only on Omega execution stages
