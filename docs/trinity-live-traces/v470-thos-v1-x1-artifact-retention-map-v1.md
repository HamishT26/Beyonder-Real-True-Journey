# v470 THOS v1 x1 Artifact Retention Map

Classification: `evidence`

This map tells THOS what can be kept, what can be published, and what must remain private or quarantined. It is a safety scaffold, not a cleanup action.

## Retention Classes

| Class | Publishable | Requirements |
| --- | --- | --- |
| `durable_phase_artifact` | Yes | Phase id, classification, source authority, no credentials |
| `schema_contract` | Yes | Version, required fields, failure mode, approval boundary |
| `advisory_summary` | Yes | Lane name, advisory label, curated summary, no raw transcript |
| `private_or_quarantine_candidate` | No | Do not stage; summarize only if required |
| `cleanup_candidate` | Manifest only | Target, reason, owner, retention class, approval status, rollback plan |
| `journey_context_not_canon` | Short cited context only | Local path and line reference; no validation claim |

## Publication Exclusions

Raw logs, session JSONL, screenshots, credential-bearing material, unreviewed cloud exports, and uncurated sibling transcripts are not current-phase publication artifacts.

## Operational Principle

A good THOS artifact is not just useful. It is scoped, sourced, reversible where needed, and honest about authority. This phase keeps the repo publication surface curated while leaving broad cleanup for separately approved work.
