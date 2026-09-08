---
name: ghc-family-first-hit-markov-evidence
description: "Compute absorption_probabilities, hitting_times on bounded supplied records. Use for explicit model or workflow evidence."
---

# ghc-family-first-hit-markov-evidence

Read `references/request-profile.json` before using this interface. Send one UTF-8 JSON request on standard input to `python -X utf8 -B scripts/ghc_family_skill.py`. The script returns one complete `ok`, `value`, `error` envelope; acceptance exits zero and a declared refusal exits two. It performs no filesystem, network, account or task action.

Unknown fields, duplicate JSON keys, nonfinite JSON, malformed nested records and booleans used as integers are refused. The operation set is limited to the two responsibilities below. Read the current family workflow when using a result to plan a real action; this computational interface grants no permission.

## absorption_probabilities

Solve first-hit probabilities for declared target states while retaining probability lost to closed non-target classes.

Example request:
```json
{"matrix": [["1/2", "1/2"], [0, 1]], "op": "absorption_probabilities", "targets": [1]}
```

Expected complete envelope:
```json
{"error": null, "ok": true, "value": [["1"], ["1"]]}
```

## hitting_times

Compute exact expected first-hit steps only when the target is reached almost surely; retain infinity as null otherwise.

Example request:
```json
{"matrix": [["1/2", "1/2"], [0, 1]], "op": "hitting_times", "targets": [1]}
```

Expected complete envelope:
```json
{"error": null, "ok": true, "value": ["2", "0"]}
```

## Reuse and recovery

The source patterns in `references/merge-sources.json` contribute explicit scope, retained failures and evidence boundaries. This consolidates compatible guidance; it does not merge identities or claim that the underlying principles are original inventions. A matching result completes only its declared finite contract. Preserve the original request and every failed witness, then repair the smallest dependency. Never replay a successful phase canonical.

Select the previous compatible entry point if this candidate fails. Keep the additive source and receipts for review. Bounded same-owner model or workflow evidence; no empirical, independent-reproduction, identity, production, professional, legal, cultural, affected-party or Maori-authority claim. NOT_READY_FOR_STAGE_20.
