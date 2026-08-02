---
name: ghc-family-record-expiry-firewall
description: Evaluate a synthetic record-expiry horizon and refuse stale evidence. Use for owner-local JSON fixtures that need explicit review dates, expiry states, retained mutations, and no production or professional conclusion.
---

# Record expiry firewall

1. Confirm the input is a synthetic owner-local fixture and the output stays in an additive owned lane.
2. Run `python -X utf8 scripts/ghc_family_record_expiry_firewall.py --output <owner-receipt.json>` from the repository root.
3. Require the valid fixture to pass and all five declared mutations to be rejected.
4. Retain every rejection at zero credit and keep stale evidence unusable until a declared review occurs.

Treat the receipt as same-owner structural evidence only. Do not infer real record validity, food-safety approval, production release, professional competence, legal compliance, independent reproduction, or Stage 20 readiness.
