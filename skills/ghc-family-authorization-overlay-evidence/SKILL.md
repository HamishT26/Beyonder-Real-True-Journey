---
name: ghc-family-authorization-overlay-evidence
description: "Compute evidence_gate, overlay_fold on bounded supplied records. Use for explicit model or workflow evidence."
---

# ghc-family-authorization-overlay-evidence

Read `references/request-profile.json` before using this interface. Send one UTF-8 JSON request on standard input to `python -X utf8 -B scripts/ghc_family_skill.py`. The script returns one complete `ok`, `value`, `error` envelope; acceptance exits zero and a declared refusal exits two. It performs no filesystem, network, account or task action.

Unknown fields, duplicate JSON keys, nonfinite JSON, malformed nested records and booleans used as integers are refused. The operation set is limited to the two responsibilities below. Read the current family workflow when using a result to plan a real action; this computational interface grants no permission.

## evidence_gate

Combine a declared user-controlled permission with explicit evidence and available prerequisites; this is a dry record assessment.

Example request:
```json
{"approval": "authorized_now", "evidence": "completed", "op": "evidence_gate", "prerequisites": true}
```

Expected complete envelope:
```json
{"error": null, "ok": true, "value": true}
```

## overlay_fold

Apply ordered correction records to a detached current view while retaining the original base and number of events.

Example request:
```json
{"base": {"route": "held"}, "events": [{"changes": {"route": "released"}, "reason": "new user instruction", "sequence": 1}], "op": "overlay_fold"}
```

Expected complete envelope:
```json
{"error": null, "ok": true, "value": {"current": {"route": "released"}, "events": 1}}
```

## Reuse and recovery

The source patterns in `references/merge-sources.json` contribute explicit scope, retained failures and evidence boundaries. This consolidates compatible guidance; it does not merge identities or claim that the underlying principles are original inventions. A matching result completes only its declared finite contract. Preserve the original request and every failed witness, then repair the smallest dependency. Never replay a successful phase canonical.

Select the previous compatible entry point if this candidate fails. Keep the additive source and receipts for review. Bounded same-owner model or workflow evidence; no empirical, independent-reproduction, identity, production, professional, legal, cultural, affected-party or Maori-authority claim. NOT_READY_FOR_STAGE_20.
