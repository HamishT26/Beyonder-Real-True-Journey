---
name: ghc-family-cg-efficiency-v696-v3
description: "Compare the exact allocation sum with grand-coalition worth without rounding. Use on complete three-symbol synthetic coalition-worth tables."
---

# Allocation conservation residual

Read [the exact contract](references/contract.md). Use the phase-local runner `ghc_family_coalition_x2_1.txt` from the declared owner stage. Its two operations are cg_efficiency and cg_individual. Send one JSON request on standard input; accepted envelopes exit zero and declared refusals exit two.

Every input has fixed abstract symbols A, B and C, eight integer worths in mask order with zero empty worth, and three reduced rational allocation pairs. The model is finite and synthetic. Use exact rationals for checks and floats only for explanatory display. Preserve the original request and all failures before a bounded correction. A passing refusal is separate from the rejected subject.

Same-owner synthetic evidence only; NOT_READY_FOR_STAGE_20. This guide supplies no real allocation, identity, consent, professional, cultural or public authority.
