---
name: ghc-family-cg-excesses-v696-v3
description: "Report every coalition worth minus its assigned allocation sum. Use on complete three-symbol synthetic coalition-worth tables."
---

# Coalition excess profile

Read [the exact contract](references/contract.md). Use the phase-local runner `ghc_family_coalition_x2_2.txt` from the declared owner stage. Its two operations are cg_excesses and cg_core. Send one JSON request on standard input; accepted envelopes exit zero and declared refusals exit two.

Every input has fixed abstract symbols A, B and C, eight integer worths in mask order with zero empty worth, and three reduced rational allocation pairs. The model is finite and synthetic. Use exact rationals for checks and floats only for explanatory display. Preserve the original request and all failures before a bounded correction. A passing refusal is separate from the rejected subject.

Same-owner synthetic evidence only; NOT_READY_FOR_STAGE_20. This guide supplies no real allocation, identity, consent, professional, cultural or public authority.
