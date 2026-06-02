# v470 THOS v4 x1 Cleanup and Retention Schema

Phase: `v470_THOS_v4_x1`

Default action: `report_only_no_delete`

## Cleanup Candidate Schema

Every cleanup candidate should carry:

- `candidate_id`
- `path_or_connector_target`
- `source_phase`
- `retention_class`
- `sensitivity_class`
- `reason_for_review`
- `evidence_source`
- `proposed_action`
- `delete_authorized: false`
- `rollback_required: true`
- `approval_required: true`

## Retention Classes

- `transient`: temporary scratch material, not durable.
- `operational`: useful for current workflow, not public proof.
- `audit_minimal`: redacted metadata suitable for durable receipt.
- `prohibited_to_persist`: raw secrets, tokens, private traces, or raw sessions.
- `unknown`: cannot decide without more evidence.

## Privacy Checks

- Raw secrets and tokens must not persist.
- Raw session transcripts must not be promoted.
- Watcher and supervisor telemetry should store redacted fingerprints rather than full payloads.
- Connector request and response bodies must not become durable logs by default.
- Derived artifacts inherit stricter source sensitivity.
- Public summaries require privacy and secret screening.

## Safe Language

- Cleanup candidate identified; deletion requires separate explicit approval.
- Dry-run report records proposed targets only; no cleanup occurred.
- Connector availability is capability only, not consent to mutate.
- THOS report is a local governance receipt, not certification.
- Journey/Solas remains `journey_context_not_canon`.
- Governance hygiene preserves open GMUT gates; it does not resolve them.
