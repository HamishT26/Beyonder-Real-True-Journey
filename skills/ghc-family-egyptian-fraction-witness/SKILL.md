---
name: ghc-family-egyptian-fraction-witness
description: "Compute egyptian_fraction_search, egyptian_fraction_verify on bounded supplied records. Use for explicit model or workflow evidence."
---

# ghc-family-egyptian-fraction-witness

Read `references/request-profile.json` before using this interface. Send one UTF-8 JSON request on standard input to `python -X utf8 -B scripts/ghc_family_skill.py`. The script returns one complete `ok`, `value`, `error` envelope; acceptance exits zero and a declared refusal exits two. It performs no filesystem, network, account or task action.

Unknown fields, duplicate JSON keys, nonfinite JSON, malformed nested records and booleans used as integers are refused. The operation set is limited to the two responsibilities below. Read the current family workflow when using a result to plan a real action; this computational interface grants no permission.

## egyptian_fraction_search

Search a bounded denominator domain for one ordered positive-integer witness to four over n as three unit fractions; no universal proof follows.

Example request:
```json
{"max_denominator": 1000, "max_pairs": 10000, "n": 5, "op": "egyptian_fraction_search"}
```

Expected complete envelope:
```json
{"error": null, "ok": true, "value": {"coverage": "found_within_bounds", "witness": [2, 4, 20]}}
```

## egyptian_fraction_verify

Verify a supplied three-denominator witness with exact rational residuals and no search or universal conjecture claim.

Example request:
```json
{"denominators": [2, 4, 20], "n": 5, "op": "egyptian_fraction_verify"}
```

Expected complete envelope:
```json
{"error": null, "ok": true, "value": {"residual": "0", "valid": true}}
```

## Reuse and recovery

The source patterns in `references/merge-sources.json` contribute explicit scope, retained failures and evidence boundaries. This consolidates compatible guidance; it does not merge identities or claim that the underlying principles are original inventions. A matching result completes only its declared finite contract. Preserve the original request and every failed witness, then repair the smallest dependency. Never replay a successful phase canonical.

Select the previous compatible entry point if this candidate fails. Keep the additive source and receipts for review. Bounded same-owner model or workflow evidence; no empirical, independent-reproduction, identity, production, professional, legal, cultural, affected-party or Maori-authority claim. NOT_READY_FOR_STAGE_20.
