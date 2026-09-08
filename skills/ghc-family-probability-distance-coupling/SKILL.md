---
name: ghc-family-probability-distance-coupling
description: "Compute distribution_distance, coupling_bounds on bounded supplied records. Use for explicit model or workflow evidence."
---

# ghc-family-probability-distance-coupling

Read `references/request-profile.json` before using this interface. Send one UTF-8 JSON request on standard input to `python -X utf8 -B scripts/ghc_family_skill.py`. The script returns one complete `ok`, `value`, `error` envelope; acceptance exits zero and a declared refusal exits two. It performs no filesystem, network, account or task action.

Unknown fields, duplicate JSON keys, nonfinite JSON, malformed nested records and booleans used as integers are refused. The operation set is limited to the two responsibilities below. Read the current family workflow when using a result to plan a real action; this computational interface grants no permission.

## distribution_distance

Compute exact L1 and total-variation distances between two finite distributions on the same ordered states.

Example request:
```json
{"op": "distribution_distance", "p": [1, 0], "q": [0, 1]}
```

Expected complete envelope:
```json
{"error": null, "ok": true, "value": {"l1": "2", "tv": "1"}}
```

## coupling_bounds

Compare the total-variation lower bound with disagreement under the explicitly independent product coupling.

Example request:
```json
{"op": "coupling_bounds", "p": ["1/2", "1/2"], "q": ["1/2", "1/2"]}
```

Expected complete envelope:
```json
{"error": null, "ok": true, "value": {"independent_disagreement": "1/2", "minimum_disagreement": "0"}}
```

## Reuse and recovery

The source patterns in `references/merge-sources.json` contribute explicit scope, retained failures and evidence boundaries. This consolidates compatible guidance; it does not merge identities or claim that the underlying principles are original inventions. A matching result completes only its declared finite contract. Preserve the original request and every failed witness, then repair the smallest dependency. Never replay a successful phase canonical.

Select the previous compatible entry point if this candidate fails. Keep the additive source and receipts for review. Bounded same-owner model or workflow evidence; no empirical, independent-reproduction, identity, production, professional, legal, cultural, affected-party or Maori-authority claim. NOT_READY_FOR_STAGE_20.
