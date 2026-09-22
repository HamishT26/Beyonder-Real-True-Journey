---
name: ghc-family-dm-distance-v702-v1
description: "Enumerate every nearest feasible set under exact symmetric-difference distance. Use for frozen six-element binary delta-matroid fixtures in Avelin v702-v1."
---

# Nearest feasible subsets

Use the phase-local paired TXT runner `runners/dm-pair-05.txt` from the owner root. Send one closed JSON object with `operation`, `fixture_id`, and the exact `fixture_sha256` from `plan.json`. This guide selects `dm_distance`; its declared outcome is `completed`.

Enumerate every nearest feasible set under exact symmetric-difference distance.

The input represents a symmetric binary matrix and a declared initial twist. The empty principal determinant is one. Symmetric exchange permits equal first and second elements, so their set toggles once. Deletion of a coloop uses the contraction-equivalent family; contraction of a loop uses the deletion-equivalent family. An even delta-matroid means uniform feasible-set parity, including uniformly odd sizes.

The immutable plan supplies full expected envelopes and all malformed classes. Exact witnesses concern these fixtures only. Preserve the failed subject when a refusal or correction passes. The runner returns accepted envelopes with exit zero and refusals with exit two. No observation, authority, identity, fairness, production or independent-reproduction claim follows. Same-owner finite synthetic evidence only. NOT_READY_FOR_STAGE_20.
