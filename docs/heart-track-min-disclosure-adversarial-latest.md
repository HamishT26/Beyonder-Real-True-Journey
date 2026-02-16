# Freed ID Minimum-Disclosure Adversarial Verification Report

- generated_utc: `2026-02-16T04:30:30+00:00`
- control: `GOV-002`
- overall_status: **PASS**

## Checks
| check | status | detail |
|---|---|---|
| vectors_file_exists | PASS | docs/freed-id-minimum-disclosure-adversarial-vectors-v0.json |
| vectors_loaded | PASS | count=4 |
| VEC-001-default-sensitive-deny:schema_validation | PASS | presentation_valid |
| VEC-001-default-sensitive-deny:expected_disclosed_fields | PASS | disclosed=['age_over_18'] |
| VEC-001-default-sensitive-deny:expected_denied_sensitive_fields | PASS | denied=['government_id'] |
| VEC-001-default-sensitive-deny:no_unrequested_leak | PASS | none |
| VEC-001-default-sensitive-deny:no_disallowed_sensitive_leak | PASS | none |
| VEC-002-allowlisted-sensitive:schema_validation | PASS | presentation_valid |
| VEC-002-allowlisted-sensitive:expected_disclosed_fields | PASS | disclosed=['age_over_18', 'government_id'] |
| VEC-002-allowlisted-sensitive:expected_denied_sensitive_fields | PASS | denied=['phone'] |
| VEC-002-allowlisted-sensitive:no_unrequested_leak | PASS | none |
| VEC-002-allowlisted-sensitive:no_disallowed_sensitive_leak | PASS | none |
| VEC-003-overrequest-nonexistent-fields:schema_validation | PASS | presentation_valid |
| VEC-003-overrequest-nonexistent-fields:expected_disclosed_fields | PASS | disclosed=['age_over_18', 'residency_country'] |
| VEC-003-overrequest-nonexistent-fields:expected_denied_sensitive_fields | PASS | denied=['email'] |
| VEC-003-overrequest-nonexistent-fields:no_unrequested_leak | PASS | none |
| VEC-003-overrequest-nonexistent-fields:no_disallowed_sensitive_leak | PASS | none |
| VEC-004-unrequested-sensitive-leak-check:schema_validation | PASS | presentation_valid |
| VEC-004-unrequested-sensitive-leak-check:expected_disclosed_fields | PASS | disclosed=['age_over_18'] |
| VEC-004-unrequested-sensitive-leak-check:expected_denied_sensitive_fields | PASS | denied=[] |
| VEC-004-unrequested-sensitive-leak-check:no_unrequested_leak | PASS | none |
| VEC-004-unrequested-sensitive-leak-check:no_disallowed_sensitive_leak | PASS | none |
