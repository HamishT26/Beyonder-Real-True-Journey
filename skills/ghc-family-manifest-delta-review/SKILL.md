---
name: ghc-family-manifest-delta-review
description: "Compute manifest_diff, staged_allowlist on bounded supplied records. Use for explicit model or workflow evidence."
---

# ghc-family-manifest-delta-review

Read `references/request-profile.json` before using this interface. Send one UTF-8 JSON request on standard input to `python -X utf8 -B scripts/ghc_family_skill.py`. The script returns one complete `ok`, `value`, `error` envelope; acceptance exits zero and a declared refusal exits two. It performs no filesystem, network, account or task action.

Unknown fields, duplicate JSON keys, nonfinite JSON, malformed nested records and booleans used as integers are refused. The operation set is limited to the two responsibilities below. Read the current family workflow when using a result to plan a real action; this computational interface grants no permission.

## manifest_diff

Compare explicit path, byte-count and digest records without reading files or silently merging duplicate paths.

Example request:
```json
{"after": [{"bytes": 1, "path": "a", "sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}], "before": [], "op": "manifest_diff"}
```

Expected complete envelope:
```json
{"error": null, "ok": true, "value": {"added": ["a"], "changed": [], "removed": [], "unchanged": []}}
```

## staged_allowlist

Expose unexpected and missing staged members against a literal allowlist without broad staging.

Example request:
```json
{"allowed": ["a", "b"], "op": "staged_allowlist", "staged": ["a", "b"]}
```

Expected complete envelope:
```json
{"error": null, "ok": true, "value": {"exact": true, "missing": [], "unexpected": []}}
```

## Reuse and recovery

The source patterns in `references/merge-sources.json` contribute explicit scope, retained failures and evidence boundaries. This consolidates compatible guidance; it does not merge identities or claim that the underlying principles are original inventions. A matching result completes only its declared finite contract. Preserve the original request and every failed witness, then repair the smallest dependency. Never replay a successful phase canonical.

Select the previous compatible entry point if this candidate fails. Keep the additive source and receipts for review. Bounded same-owner model or workflow evidence; no empirical, independent-reproduction, identity, production, professional, legal, cultural, affected-party or Maori-authority claim. NOT_READY_FOR_STAGE_20.
