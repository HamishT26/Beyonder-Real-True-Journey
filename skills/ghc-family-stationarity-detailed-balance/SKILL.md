---
name: ghc-family-stationarity-detailed-balance
description: "Compute stationary_distribution, detailed_balance on bounded supplied records. Use for explicit model or workflow evidence."
---

# ghc-family-stationarity-detailed-balance

Read `references/request-profile.json` before using this interface. Send one UTF-8 JSON request on standard input to `python -X utf8 -B scripts/ghc_family_skill.py`. The script returns one complete `ok`, `value`, `error` envelope; acceptance exits zero and a declared refusal exits two. It performs no filesystem, network, account or task action.

Unknown fields, duplicate JSON keys, nonfinite JSON, malformed nested records and booleans used as integers are refused. The operation set is limited to the two responsibilities below. Read the current family workflow when using a result to plan a real action; this computational interface grants no permission.

## stationary_distribution

Solve finite stationarity equations and normalization exactly, refusing a nonunique stationary family instead of choosing silently.

Example request:
```json
{"matrix": [["3/4", "1/4"], ["1/2", "1/2"]], "op": "stationary_distribution"}
```

Expected complete envelope:
```json
{"error": null, "ok": true, "value": ["2/3", "1/3"]}
```

## detailed_balance

Test pairwise stationary probability-flow symmetry after checking stationarity; this does not infer physical equilibrium.

Example request:
```json
{"matrix": [["3/4", "1/4"], ["1/2", "1/2"]], "op": "detailed_balance", "stationary": ["2/3", "1/3"]}
```

Expected complete envelope:
```json
{"error": null, "ok": true, "value": true}
```

## Reuse and recovery

The source patterns in `references/merge-sources.json` contribute explicit scope, retained failures and evidence boundaries. This consolidates compatible guidance; it does not merge identities or claim that the underlying principles are original inventions. A matching result completes only its declared finite contract. Preserve the original request and every failed witness, then repair the smallest dependency. Never replay a successful phase canonical.

Select the previous compatible entry point if this candidate fails. Keep the additive source and receipts for review. Bounded same-owner model or workflow evidence; no empirical, independent-reproduction, identity, production, professional, legal, cultural, affected-party or Maori-authority claim. NOT_READY_FOR_STAGE_20.
