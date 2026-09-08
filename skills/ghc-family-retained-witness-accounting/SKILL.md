---
name: ghc-family-retained-witness-accounting
description: "Compute method_transition, witness_accounting on bounded supplied records. Use for explicit model or workflow evidence."
---

# ghc-family-retained-witness-accounting

Read `references/request-profile.json` before using this interface. Send one UTF-8 JSON request on standard input to `python -X utf8 -B scripts/ghc_family_skill.py`. The script returns one complete `ok`, `value`, `error` envelope; acceptance exits zero and a declared refusal exits two. It performs no filesystem, network, account or task action.

Unknown fields, duplicate JSON keys, nonfinite JSON, malformed nested records and booleans used as integers are refused. The operation set is limited to the two responsibilities below. Read the current family workflow when using a result to plan a real action; this computational interface grants no permission.

## method_transition

Require an allowed state transition and a passing witness before promoting a candidate or preferred method.

Example request:
```json
{"op": "method_transition", "passing_witnesses": 0, "state": "observed", "successor_validated": false, "to": "candidate"}
```

Expected complete envelope:
```json
{"error": null, "ok": true, "value": true}
```

## witness_accounting

Count subject failures separately from passing rejection checks and prevent repeated identifiers from multiplying credit.

Example request:
```json
{"op": "witness_accounting", "rows": [{"check": "pass", "id": "a", "subject": "fail"}]}
```

Expected complete envelope:
```json
{"error": null, "ok": true, "value": {"checks_fail": 0, "checks_pass": 1, "original_success_credit": 0, "subject_fail": 1, "subject_pass": 0}}
```

## Reuse and recovery

The source patterns in `references/merge-sources.json` contribute explicit scope, retained failures and evidence boundaries. This consolidates compatible guidance; it does not merge identities or claim that the underlying principles are original inventions. A matching result completes only its declared finite contract. Preserve the original request and every failed witness, then repair the smallest dependency. Never replay a successful phase canonical.

Select the previous compatible entry point if this candidate fails. Keep the additive source and receipts for review. Bounded same-owner model or workflow evidence; no empirical, independent-reproduction, identity, production, professional, legal, cultural, affected-party or Maori-authority claim. NOT_READY_FOR_STAGE_20.
