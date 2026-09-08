---
name: ghc-family-risk-consent-records
description: "Compute risk_register_projection, consent_scope_check on bounded supplied records. Use for explicit model or workflow evidence."
---

# ghc-family-risk-consent-records

Read `references/request-profile.json` before using this interface. Send one UTF-8 JSON request on standard input to `python -X utf8 -B scripts/ghc_family_skill.py`. The script returns one complete `ok`, `value`, `error` envelope; acceptance exits zero and a declared refusal exits two. It performs no filesystem, network, account or task action.

Unknown fields, duplicate JSON keys, nonfinite JSON, malformed nested records and booleans used as integers are refused. The operation set is limited to the two responsibilities below. Read the current family workflow when using a result to plan a real action; this computational interface grants no permission.

## risk_register_projection

Order declared ordinal risk scores while preserving each record evidence label; ordinal products are a local prioritization convention.

Example request:
```json
{"op": "risk_register_projection", "rows": [{"evidence": "represented", "id": "a", "impact": 3, "likelihood": 2}]}
```

Expected complete envelope:
```json
{"error": null, "ok": true, "value": [{"evidence": "represented", "id": "a", "score": 6}]}
```

## consent_scope_check

Compare a synthetic grant record with action, resource, purpose and expiry, without treating the comparison as real consent or authority.

Example request:
```json
{"action": "read", "grant": {"actions": ["read"], "expires": 10, "purpose": "research", "resources": ["a"], "revoked": false}, "now": 1, "op": "consent_scope_check", "purpose": "research", "resource": "a"}
```

Expected complete envelope:
```json
{"error": null, "ok": true, "value": {"authority_granted": false, "matches": true}}
```

## Reuse and recovery

The source patterns in `references/merge-sources.json` contribute explicit scope, retained failures and evidence boundaries. This consolidates compatible guidance; it does not merge identities or claim that the underlying principles are original inventions. A matching result completes only its declared finite contract. Preserve the original request and every failed witness, then repair the smallest dependency. Never replay a successful phase canonical.

Select the previous compatible entry point if this candidate fails. Keep the additive source and receipts for review. Bounded same-owner model or workflow evidence; no empirical, independent-reproduction, identity, production, professional, legal, cultural, affected-party or Maori-authority claim. NOT_READY_FOR_STAGE_20.
