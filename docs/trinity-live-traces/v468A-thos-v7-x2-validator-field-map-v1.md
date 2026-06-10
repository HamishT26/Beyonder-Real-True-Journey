# v468A THOS v7 x2 Validator Field Map

Direct mappings:

- `phase_id` to report phase property.
- `thos_gmut_boundary` to report boundary properties.

Summarized mappings:

- `validation_chain` to human-readable result text.
- `blocked_actions` to warning-level results.

Future routes:

- Forbidden-claim hits can become error-level results.
- Artifact path checks can become report locations.

Parity gap: the report is a receipt, not a replacement for validator execution or remote verification.
