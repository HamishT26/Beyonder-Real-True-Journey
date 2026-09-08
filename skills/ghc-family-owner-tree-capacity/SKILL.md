---
name: ghc-family-owner-tree-capacity
description: "Compute file_budget, path_scope on bounded supplied records. Use for explicit model or workflow evidence."
---

# ghc-family-owner-tree-capacity

Read `references/request-profile.json` before using this interface. Send one UTF-8 JSON request on standard input to `python -X utf8 -B scripts/ghc_family_skill.py`. The script returns one complete `ok`, `value`, `error` envelope; acceptance exits zero and a declared refusal exits two. It performs no filesystem, network, account or task action.

Unknown fields, duplicate JSON keys, nonfinite JSON, malformed nested records and booleans used as integers are refused. The operation set is limited to the two responsibilities below. Read the current family workflow when using a result to plan a real action; this computational interface grants no permission.

## file_budget

Check both admission and the need for rotation at the hard owner file ceiling.

Example request:
```json
{"ceiling": 2000, "current": 1999, "incoming": 1, "op": "file_budget"}
```

Expected complete envelope:
```json
{"error": null, "ok": true, "value": {"admit": true, "remaining": 0, "rotate": true, "total": 2000}}
```

## path_scope

Compare literal path segments and reject traversal syntax before any scope decision; no filesystem action is performed.

Example request:
```json
{"op": "path_scope", "path": "docs/seren/a.json", "roots": ["docs/seren"]}
```

Expected complete envelope:
```json
{"error": null, "ok": true, "value": true}
```

## Reuse and recovery

The source patterns in `references/merge-sources.json` contribute explicit scope, retained failures and evidence boundaries. This consolidates compatible guidance; it does not merge identities or claim that the underlying principles are original inventions. A matching result completes only its declared finite contract. Preserve the original request and every failed witness, then repair the smallest dependency. Never replay a successful phase canonical.

Select the previous compatible entry point if this candidate fails. Keep the additive source and receipts for review. Bounded same-owner model or workflow evidence; no empirical, independent-reproduction, identity, production, professional, legal, cultural, affected-party or Maori-authority claim. NOT_READY_FOR_STAGE_20.
