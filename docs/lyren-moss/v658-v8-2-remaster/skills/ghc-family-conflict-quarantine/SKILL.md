---
name: ghc-family-conflict-quarantine
description: Preserve contradictory synthetic declarations without silently choosing one. Use for owner-local fixtures that need conflict detection, unresolved-source retention, mutation rejection, and explicit abstention.
---

# Conflict quarantine

1. Verify the declarations are synthetic and carry source labels.
2. Run `python -X utf8 scripts/ghc_family_conflict_quarantine.py --output <owner-receipt.json>` from the repository root.
3. Require one valid fixture and five rejected mutations; never erase the contradicting declaration.
4. Leave resolution, acceptance, production use, and competent-authority decisions outside the receipt.

This skill provides bounded workflow evidence only, not supplier approval, empirical confirmation, legal or cultural authority, independent reproduction, or Stage 20 readiness.
