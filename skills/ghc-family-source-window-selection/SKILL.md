---
name: ghc-family-source-window-selection
description: "Compute context_window, source_selection on bounded supplied records. Use for explicit model or workflow evidence."
---

# ghc-family-source-window-selection

Read `references/request-profile.json` before using this interface. Send one UTF-8 JSON request on standard input to `python -X utf8 -B scripts/ghc_family_skill.py`. The script returns one complete `ok`, `value`, `error` envelope; acceptance exits zero and a declared refusal exits two. It performs no filesystem, network, account or task action.

Unknown fields, duplicate JSON keys, nonfinite JSON, malformed nested records and booleans used as integers are refused. The operation set is limited to the two responsibilities below. Read the current family workflow when using a result to plan a real action; this computational interface grants no permission.

## context_window

Select the most recent completed records from explicit monotonic ordinals while keeping represented work out of the completed window.

Example request:
```json
{"count": 1, "op": "context_window", "rows": [{"id": "a", "ordinal": 1, "state": "completed"}, {"id": "b", "ordinal": 2, "state": "represented"}, {"id": "c", "ordinal": 3, "state": "completed"}]}
```

Expected complete envelope:
```json
{"error": null, "ok": true, "value": ["c"]}
```

## source_selection

Deduplicate equal source bindings by stable identifier, retain input order, and refuse conflicting bindings.

Example request:
```json
{"limit": 2, "op": "source_selection", "rows": [{"id": "a", "sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "source": "x"}, {"id": "a", "sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "source": "x"}]}
```

Expected complete envelope:
```json
{"error": null, "ok": true, "value": ["a"]}
```

## Reuse and recovery

The source patterns in `references/merge-sources.json` contribute explicit scope, retained failures and evidence boundaries. This consolidates compatible guidance; it does not merge identities or claim that the underlying principles are original inventions. A matching result completes only its declared finite contract. Preserve the original request and every failed witness, then repair the smallest dependency. Never replay a successful phase canonical.

Select the previous compatible entry point if this candidate fails. Keep the additive source and receipts for review. Bounded same-owner model or workflow evidence; no empirical, independent-reproduction, identity, production, professional, legal, cultural, affected-party or Maori-authority claim. NOT_READY_FOR_STAGE_20.
