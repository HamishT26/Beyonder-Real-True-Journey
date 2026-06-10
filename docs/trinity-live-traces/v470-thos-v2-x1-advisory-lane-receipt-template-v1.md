# v470 THOS v2 x1 Advisory Lane Receipt Template

Classification: `evidence`

Advisory receipts preserve useful critique without pretending to be publication receipts.

## Required Fields

`receipt_id`, `lane_id`, `lane_type`, `phase_ref`, `baseline_ref`, `authority`, `actions_performed`, `file_mutation`, `connector_mutation`, `publication_authority`, `repo_branch`, `repo_head`, `repo_status_summary`, `dirty_worktree_class`, `source_refs`, `validations_requested`, `validations_verified`, `blockers`, `recommendations`, `claims_supported`, and `claims_refused`.

## Rules

Advisory receipts cannot replace Git receipts. CLI read failures are blockers, not invented evidence. Standby lanes do not receive fabricated advisories. Claims refused must travel with the receipt.
