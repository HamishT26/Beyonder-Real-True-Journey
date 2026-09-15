---
name: ghc-family-cg-convex-v696-v3
description: "Check every finite pair inequality and retain all violating coalition pairs. Use on complete three-symbol synthetic coalition-worth tables."
---

# Convex-game inequality audit

Read [the exact contract](references/contract.md). Use the phase-local runner `ghc_family_coalition_x1_5.txt` from the declared owner stage. Its two operations are cg_superadditive and cg_convex. Send one JSON request on standard input; accepted envelopes exit zero and declared refusals exit two.

Every input has fixed abstract symbols A, B and C, eight integer worths in mask order with zero empty worth, and three reduced rational allocation pairs. The model is finite and synthetic. Use exact rationals for checks and floats only for explanatory display. Preserve the original request and all failures before a bounded correction. A passing refusal is separate from the rejected subject.

Same-owner synthetic evidence only; NOT_READY_FOR_STAGE_20. This guide supplies no real allocation, identity, consent, professional, cultural or public authority.
