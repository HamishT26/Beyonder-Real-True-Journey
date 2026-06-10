# v470 THOS v2 x1 Connector Write Approval Packet

Classification: `evidence`

Connector writes remain blocked unless an explicit, scoped approval packet is complete and approved. This phase creates the packet shape only.

## Required Fields

`request_id`, `connector_id`, `connector_name`, `requested_write_action`, `target_resource`, `actor`, `user_intent`, `reason`, `capability_basis`, `consent_artifact`, `consent_scope`, `consent_expiry`, `write_scope`, `data_touched`, `privacy_impact`, `risk_class`, `rollback_or_repair_plan`, `source_links`, `approver`, `decision`, `decision_reason`, and `decided_at`.

## Rules

Connector writes are blocked unless this packet is complete and approved. Approval is scoped and single-use unless explicitly stated otherwise. Automation edits, Drive/cloud writes, account changes, and credential changes require packets. No v2 x1 connector write is approved or performed.
