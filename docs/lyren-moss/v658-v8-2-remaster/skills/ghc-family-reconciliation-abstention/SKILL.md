---
name: ghc-family-reconciliation-abstention
description: Check a synthetic tank-to-package reconciliation envelope while refusing release conclusions. Use when declared quantities, units, uncertainty, unexplained balance, and retained mutation evidence must remain explicit.
---

# Reconciliation abstention

1. Keep all quantities fictional and require declared units and uncertainty placeholders.
2. Run `python -X utf8 scripts/ghc_family_reconciliation_abstention.py --output <owner-receipt.json>`.
3. Require the valid fixture to pass and five mutations to fail closed.
4. Preserve unexplained balance as a hold; do not convert arithmetic consistency into product suitability or release authority.

The output is same-owner synthetic evidence only and makes no production, safety, professional, empirical, or Stage 20 claim.
