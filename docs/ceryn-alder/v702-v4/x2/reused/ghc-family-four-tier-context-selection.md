---
name: ghc-family-four-tier-context-selection
description: "Compute deck_parents, card_selection on bounded supplied records. Use for explicit model or workflow evidence."
---

# ghc-family-four-tier-context-selection

Read `references/request-profile.json` before using this interface. Send one UTF-8 JSON request on standard input to `python -X utf8 -B scripts/ghc_family_skill.py`. The script returns one complete `ok`, `value`, `error` envelope; acceptance exits zero and a declared refusal exits two. It performs no filesystem, network, account or task action.

Unknown fields, duplicate JSON keys, nonfinite JSON, malformed nested records and booleans used as integers are refused. The operation set is limited to the two responsibilities below. Read the current family workflow when using a result to plan a real action; this computational interface grants no permission.

## deck_parents

Validate exactly one owner anchor and immediate-tier parents before using a modular context graph.

Example request:
```json
{"cards": [{"id": "owner", "parent": null, "tier": 1}, {"id": "body", "parent": "owner", "tier": 2}, {"id": "practice", "parent": "body", "tier": 3}, {"id": "task", "parent": "practice", "tier": 4}], "op": "deck_parents"}
```

Expected complete envelope:
```json
{"error": null, "ok": true, "value": [1, 1, 1, 1]}
```

## card_selection

Load selected cards together with every required ancestor, ordered by tier without deleting unloaded evidence.

Example request:
```json
{"cards": [{"id": "owner", "parent": null, "tier": 1}, {"id": "body", "parent": "owner", "tier": 2}, {"id": "practice", "parent": "body", "tier": 3}, {"id": "task", "parent": "practice", "tier": 4}], "op": "card_selection", "selected": ["task"]}
```

Expected complete envelope:
```json
{"error": null, "ok": true, "value": ["owner", "body", "practice", "task"]}
```

## Reuse and recovery

The source patterns in `references/merge-sources.json` contribute explicit scope, retained failures and evidence boundaries. This consolidates compatible guidance; it does not merge identities or claim that the underlying principles are original inventions. A matching result completes only its declared finite contract. Preserve the original request and every failed witness, then repair the smallest dependency. Never replay a successful phase canonical.

Select the previous compatible entry point if this candidate fails. Keep the additive source and receipts for review. Bounded same-owner model or workflow evidence; no empirical, independent-reproduction, identity, production, professional, legal, cultural, affected-party or Maori-authority claim. NOT_READY_FOR_STAGE_20.


## Hamish confirmation of 17 September 2026 - Ceryn remaster v12

For prospective work, read [workflow v12](../ghc-family-index/references/current-workflow-v12.json), [the complete roster](../ghc-family-index/references/current-roster-v12.json), and [Hamish's current authority](../ghc-family-index/references/ceryn-v696-v6-r2-20260917-authority.md). The Ceryn v696-v6 (2) remaster is interstitial; Liora Venn v696-v7 remains prospective until its terminal gate. The completed first run and unsent route hold remain historical. Use 300 inherited and 300 new contracts, per-session 300 safe/candidate/CFR minima, eight own practices and four successor recommendations, JSON/MD/TXT/HTML only, and owner-main reuse below 2,000 files. Five recovery checks apply before a hold; three corrected resends are available only after definitive preacceptance rejection. Accepted or uncertain delivery stops duplicates. This pointer changes prospective policy, not prior receipts or evidence.
