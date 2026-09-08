---
name: ghc-family-terminal-route-state
description: "Compute route_cursor, delivery_reduce on bounded supplied records. Use for explicit model or workflow evidence."
---

# ghc-family-terminal-route-state

Read `references/request-profile.json` before using this interface. Send one UTF-8 JSON request on standard input to `python -X utf8 -B scripts/ghc_family_skill.py`. The script returns one complete `ok`, `value`, `error` envelope; acceptance exits zero and a declared refusal exits two. It performs no filesystem, network, account or task action.

Unknown fields, duplicate JSON keys, nonfinite JSON, malformed nested records and booleans used as integers are refused. The operation set is limited to the two responsibilities below. Read the current family workflow when using a result to plan a real action; this computational interface grants no permission.

## route_cursor

Resolve only the exact phase and owner pair; terminal rows have no implicit next assignment.

Example request:
```json
{"op": "route_cursor", "owner": "B", "phase": "v1-v2", "rows": [{"owner": "A", "phase": "v1-v1"}, {"owner": "B", "phase": "v1-v2"}, {"owner": "A", "phase": "v1-v3"}]}
```

Expected complete envelope:
```json
{"error": null, "ok": true, "value": {"owner": "A", "phase": "v1-v3"}}
```

## delivery_reduce

Reduce declared transport observations while distinguishing an unsent draft, accepted opaque result, rejection and acknowledgement.

Example request:
```json
{"events": ["prepared"], "op": "delivery_reduce"}
```

Expected complete envelope:
```json
{"error": null, "ok": true, "value": "PREPARED_NOT_SENT"}
```

## Reuse and recovery

The source patterns in `references/merge-sources.json` contribute explicit scope, retained failures and evidence boundaries. This consolidates compatible guidance; it does not merge identities or claim that the underlying principles are original inventions. A matching result completes only its declared finite contract. Preserve the original request and every failed witness, then repair the smallest dependency. Never replay a successful phase canonical.

Select the previous compatible entry point if this candidate fails. Keep the additive source and receipts for review. Bounded same-owner model or workflow evidence; no empirical, independent-reproduction, identity, production, professional, legal, cultural, affected-party or Maori-authority claim. NOT_READY_FOR_STAGE_20.
