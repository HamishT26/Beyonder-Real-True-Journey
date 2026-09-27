---
name: ghc-family-rook-permutation-hit-census
description: Enumerate all permutations and count exactly how many selected cells each permutation hits. Use for finite synthetic board records with exact fixture binding.
---

# Permutation Hit Census

Enumerate all permutations and count exactly how many selected cells each permutation hits.

Read the complete immutable board request and preserve its definition digest. The square universe is bounded to n=0 through n=6; cell coordinates are zero-based integers, sorted and unique. Boolean dimensions, duplicates, changed definitions, real participants, and authority actions are rejected.

Invoke `x2/runners/ghc_family_rook_pair_6.txt` with Python, passing one UTF-8 JSON request on standard input. Select operation `permutation-hit-census`. The caller admits only its two declared operations. Input is limited to 65,536 bytes and sixteen nesting levels; duplicate keys and nonfinite JSON constants are refused. Exit zero means the stated bounded outcome was represented; inspect disposition and completion_credit before assigning credit.

Expected disposition: completed. Read `x2/results/permutation-hit-census.json` for saved exact certificates and `x2/packets/permutation-hit-census.json` for failed originals, passing refusal predicates and separate repair copies. These are shared-fixture contracts, not independent observations.

If an identity disagrees, retain the failed subject and its output. Correct only that dependency in a new unsealed record, then retry it once; never reclassify a failed original or replay a successful stage. If already frozen, append a separate correction. Rollback means retire this candidate from selection while preserving its bytes and evidence.

Finite synthetic same-owner combinatorics and software only; not independent reproduction, empirical GMUT, production THOS or Freed ID, identity continuity, consciousness, personhood, professional, legal, cultural, affected-party or Maori authority, complete assurance, Theory-of-Everything proof, canon or Stage 20 readiness.
