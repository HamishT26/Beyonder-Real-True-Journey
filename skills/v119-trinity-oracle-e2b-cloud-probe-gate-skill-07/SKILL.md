---
name: v119-trinity-oracle-e2b-cloud-probe-gate-skill-07
description: Operate v119_07_oracle_e2b_cloud_probe_gate as a guarded v119 Trinity phase skill.
---

# v119-trinity-oracle-e2b-cloud-probe-gate-skill-07

- phase: `v119`
- candidate_id: `v119_07_oracle_e2b_cloud_probe_gate`
- pillar: `body`
- authority: `repo_first_guarded_receipt_only`
- provider_policy: `no_external_write_without_action_time_confirmation`

## Use

1. Start from the current phase receipt and suite statuses.
2. Keep Google Drive and personal accounts on operator hold unless explicitly confirmed for a narrow action.
3. Generate evidence as repo artifacts before claiming live-write success.
4. Preserve forward-only Git publication and curated allowlist staging.

## Purpose

record OCI and e2b availability without provisioning paid resources
