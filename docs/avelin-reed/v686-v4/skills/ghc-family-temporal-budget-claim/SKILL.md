---
name: ghc-family-temporal-budget-claim
description: "Inspect coverage budget, evidence gate using bounded synthetic JSON fixtures and explicit evidence limits."
---

# Temporal Budget Claim

Use this package for `coverage_budget`, `evidence_gate`. It combines two related frozen contract families from Avelin Reed v686-v4. A fixture is a bounded software example, and each input and expected result remains in [the contract reference](references/contracts.json).

Select the matching family by its actual operation and endpoint or record semantics. Do not substitute a similarly named family. Use the already authorized isolated runtime described in [runtime requirements](references/runtime.json). Merely finding this package does not authorize an installation or an external action.

Pass one JSON object containing exactly `family` and `input` to `python -X utf8 scripts/ghc_family_temporal_guards.py --input case.json --output result.json`. The output path must be new. The CLI emits stable refusal values for malformed inputs, so read the result JSON rather than treating exit code zero as acceptance of the proposed operation.

Compare the entire result, including JSON types, endpoint closures, record order, and refusal labels. Keep the original input unchanged. Use exact integer synthetic ticks; these examples provide no conversion between physical clocks. Retain every rejected input and use a new output path for its bounded correction.

The five portable runner sources are included so local imports remain available after relocation. Their copies are compatibility assets, not additional runner novelty. The original source and x1 definition digests in the reference identify the evidence contract; a copied guide does not transfer owner execution credit.

All names, roles, hopes, and family terms are relational working language only. A simulated allow result is not real authorization. Preserve empirical, participant, professional, production, identity, legal, cultural, affected-party, Māori-authority, complete-privacy, complete-accessibility, exhaustive-security, independent-reproduction, consciousness/personhood, AGI/ASI, Theory-of-Everything, canon, and Stage 20 boundaries. Keep `completed`, `represented`, `open_gap`, and `exact_gate` distinct.

Rollback by selecting the prior validated package. Preserve this package, its source, and every negative; do not overwrite another skill or repair an evidence mismatch by weakening a gate.
