# v470 THOS v2 x1 Plugin, MCP, And Skill Boundary Card Template

Classification: `evidence`

Boundary cards separate capability, consent, and approval. They prevent a tool surface from silently becoming permission.

## Required Field Groups

| Group | Fields |
| --- | --- |
| Identity | `card_id`, `surface_id`, `surface_type`, `surface_name`, `owner`, `version` |
| Capability | `capabilities_exposed`, `capabilities_denied`, `capability_class`, `write_capable`, `network_capable` |
| Sensitive boundary | `credential_surface`, `data_classes`, `allowed_inputs`, `allowed_outputs` |
| Consent and approval | `consent_required`, `approval_required`, `approval_scope`, `human_trigger_required` |
| Retention and source | `retention_mode`, `source_of_record`, `refresh_authority` |
| Governance | `blocked_actions`, `audit_events`, `validation_targets`, `action_status` |

## Rules

Capability alone never authorizes a write. Consent alone never creates capability. Effective permission for mutation requires capability, consent, and approval when approval is required. Skills guide workflow, but do not grant authority. MCP and plugin writes are external mutations unless proven otherwise.
