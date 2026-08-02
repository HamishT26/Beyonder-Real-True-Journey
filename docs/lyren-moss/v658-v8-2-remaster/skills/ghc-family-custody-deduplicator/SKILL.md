---
name: ghc-family-custody-deduplicator
description: Reject orphan and duplicate events in a synthetic custody chain. Use for owner-local package, keg, sample, or evidence fixtures requiring stable event keys, lineage preservation, retained failures, and no real custody claim.
---

# Custody deduplicator

1. Confirm every object, holder, event, identity, and location is synthetic.
2. Run `python -X utf8 scripts/ghc_family_custody_deduplicator.py --output <owner-receipt.json>`.
3. Require the valid chain to pass and all five orphan, duplicate, or promotion mutations to be rejected.
4. Retain the rejected witnesses and refuse real chain-of-custody or evidentiary conclusions.

This skill does not establish legal custody, identity authority, professional competence, production use, independent reproduction, or Stage 20 readiness.
