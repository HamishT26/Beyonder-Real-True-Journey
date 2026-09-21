---
name: ghc-family-stable-matching-receiver-optimal-matching-v1
description: Evaluate the receiver-optimal-matching contract for explicit finite strict stable-matching profiles.
---

# receiver-optimal-matching

Run the symmetric receiver-initiated procedure and translate the result to proposer-receiver pairs.

Use `ghc_family_stable_matching_pair_03.txt` with one UTF-8 JSON request path. The request has exactly `op` and `profile`. A profile declares two disjoint sides of equal size two through five, strict complete preference permutations, one frozen adjacent-swap mutation, `evidence_class` equal to `synthetic`, and zero real participants and allocations.

The response retains complete finite matchings, blocking-pair evidence and side-specific ranks. A rejected malformed profile exits with status two and earns zero subject-completion credit even when the refusal guard passes. Validate one accepting and one duplicate-preference subject before reuse; keep the caller with its exact core dependency.

Stability is not social optimality, fairness, consent or authority to allocate real people. Finite synthetic same-owner software and documentation evidence only; no independent reproduction, empirical GMUT confirmation, production THOS or Freed ID, professional, legal, cultural, affected-party or Maori authority, consciousness, personhood, Theory-of-Everything proof or Stage 20 readiness.
