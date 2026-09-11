# Exact contract

Operation: `petri_release_authority_hold`

Hypothesis: Report declaration completeness while withholding every real operational release action.

Ceiling: `exact_gate`.

Example request:

```json
{
  "op": "petri_release_authority_hold",
  "record": "synthetic-workflow-01",
  "declarations": {
    "provenance": true,
    "correction": true,
    "accessibility": false,
    "professional_review": false
  },
  "external_authority": false
}
```

Expected envelope:

```json
{
  "ok": true,
  "value": {
    "record": "synthetic-workflow-01",
    "missing": [
      "accessibility",
      "professional_review"
    ],
    "external_action": false,
    "authority_verified": false,
    "exact_gate": true
  },
  "authority": false
}
```

The named unknown-field subject must be rejected while remaining a failed subject at zero acceptance credit.

Bounded same-owner synthetic software evidence only. No empirical, real-participant, professional, production-identity, deployment, legal, cultural, affected-party or Maori authority, complete privacy/accessibility/security, independent reproduction, consciousness/personhood, Theory-of-Everything, canon or Stage 20 claim. NOT_READY_FOR_STAGE_20.
