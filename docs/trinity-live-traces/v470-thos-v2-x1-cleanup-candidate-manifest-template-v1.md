# v470 THOS v2 x1 Cleanup Candidate Manifest Template

Classification: `evidence`

This manifest identifies possible cleanup candidates without performing cleanup. It is a proposal format, not an action record.

## Required Candidate Fields

| Field | Purpose |
| --- | --- |
| `candidate_id` | Stable candidate id. |
| `artifact_type` | Artifact, scratch, cache, log, source, or unknown. |
| `target_ref` | Target path or surface reference. |
| `created_by_surface` | Originating surface if known. |
| `cleanup_class` | Observation, hygiene, reversible approval, destructive blocked, or external blocked. |
| `risk_class` | Low, medium, high, or unknown. |
| `source_backlink` | Source of record or none. |
| `cleanup_reason` | Why the candidate exists. |
| `safe_to_delete` | Defaults false. |
| `approval_required` | Defaults true. |
| `delete_preconditions` | Required before any action. |
| `rollback_or_repair_plan` | Required before any action. |

## Rules

Cleanup manifests do not authorize deletion. Unknown or sensitive candidates require review. No v2 x1 artifact performs cleanup.
