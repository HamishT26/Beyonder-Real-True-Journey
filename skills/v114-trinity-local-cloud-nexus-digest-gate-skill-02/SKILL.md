---
name: v114-trinity-local-cloud-nexus-digest-gate-skill-02
description: Operate v114_02_local_cloud_nexus_digest_gate as a guarded v114 Trinity phase skill.
---

# v114-trinity-local-cloud-nexus-digest-gate-skill-02

- phase: `v114`
- candidate_id: `v114_02_local_cloud_nexus_digest_gate`
- pillar: `body`
- authority: `repo_first_guarded_receipt_only`
- provider_policy: `no_external_write_without_action_time_confirmation`

## Use

1. Start from the current phase receipt and suite statuses.
2. Keep Google Drive and personal accounts on operator hold unless explicitly confirmed for a narrow action.
3. Generate evidence as repo artifacts before claiming live-write success.
4. Preserve forward-only Git publication and curated allowlist staging.

## Purpose

turn Solion Local/Cloud Nexus proposals into bounded repo evidence
