# Freed ID Minimum-Disclosure Verification Report

- generated_utc: `2026-02-16T03:35:48+00:00`
- control: `GOV-002`
- overall_status: **PASS**

## Checks
| check | status | detail |
|---|---|---|
| policy_doc_exists | PASS | docs/freed-id-minimum-disclosure-policy-v0.md |
| schema_doc_exists | PASS | docs/freed-id-minimum-disclosure-schema-v0.json |
| schema_required_fields_present | PASS | count=8 |
| default_sensitive_block | PASS | government_id blocked by default |
| denied_sensitive_tracking | PASS | government_id listed |
| presentation_validation_default | PASS | presentation_valid |
| allowlisted_sensitive_field | PASS | government_id disclosed, email withheld |
| presentation_validation_allowlisted | PASS | presentation_valid |
| schema_alignment | PASS | presentation contains all required schema keys |
