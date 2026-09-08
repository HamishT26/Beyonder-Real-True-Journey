---
name: ghc-family-remedy-review-coverage
description: "Compute remedy_queue, review_coverage on bounded supplied records. Use for explicit model or workflow evidence."
---

# ghc-family-remedy-review-coverage

Read `references/request-profile.json` before using this interface. Send one UTF-8 JSON request on standard input to `python -X utf8 -B scripts/ghc_family_skill.py`. The script returns one complete `ok`, `value`, `error` envelope; acceptance exits zero and a declared refusal exits two. It performs no filesystem, network, account or task action.

Unknown fields, duplicate JSON keys, nonfinite JSON, malformed nested records and booleans used as integers are refused. The operation set is limited to the two responsibilities below. Read the current family workflow when using a result to plan a real action; this computational interface grants no permission.

## remedy_queue

Build a deterministic synthetic review queue by urgency and declared intake order without resolving a grievance or allocating rights.

Example request:
```json
{"op": "remedy_queue", "rows": [{"id": "a", "ordinal": 1, "urgency": 1}, {"id": "b", "ordinal": 2, "urgency": 3}]}
```

Expected complete envelope:
```json
{"error": null, "ok": true, "value": {"decisions_taken": 0, "order": ["b", "a"]}}
```

## review_coverage

Compare explicit required review areas with completed evidence records and retain represented or missing areas as gaps.

Example request:
```json
{"observed": [{"area": "keyboard", "state": "completed"}], "op": "review_coverage", "required": ["keyboard", "screenreader"]}
```

Expected complete envelope:
```json
{"error": null, "ok": true, "value": {"complete": false, "covered": ["keyboard"], "missing": ["screenreader"]}}
```

## Reuse and recovery

The source patterns in `references/merge-sources.json` contribute explicit scope, retained failures and evidence boundaries. This consolidates compatible guidance; it does not merge identities or claim that the underlying principles are original inventions. A matching result completes only its declared finite contract. Preserve the original request and every failed witness, then repair the smallest dependency. Never replay a successful phase canonical.

Select the previous compatible entry point if this candidate fails. Keep the additive source and receipts for review. Bounded same-owner model or workflow evidence; no empirical, independent-reproduction, identity, production, professional, legal, cultural, affected-party or Maori-authority claim. NOT_READY_FOR_STAGE_20.
