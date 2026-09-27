---
name: ghc-family-unique-code-ambiguity-witness
description: "Return a concrete bit string with two distinct parses when the finite product graph finds one. Use for finite synthetic binary codebook review."
---

# ambiguity-witness

Return a concrete bit string with two distinct parses when the finite product graph finds one.

Use the exact frozen JSON example in `../../fixtures/ambiguity-witness.json` with `../../runners/ghc_family_unique_code_pair_1.txt`. Invoke it with the existing Python runtime. The caller accepts exactly `paired-automaton`, `ambiguity-witness`. It is local and uninstalled.

## Input contract

The request has exactly `op` and `fixture`. A fixture names a binary codebook with one to five distinct nonempty words of length one to four, a message of at most three integer indices, an observed synthetic word of at most twelve bits, an identifier, and evidence exactly `synthetic`. Message indices are not Boolean values. Codeword order is part of the record.

## Procedure and interpretation

1. Read the frozen proposal and fixture before execution.
2. Invoke the paired caller on the example or a caller-owned bounded copy.
3. Inspect the full response, its exact operation, fixture identifier and evidence disposition.
4. Compare the result with the saved separate reference in `../../results/ambiguity-witness.json`. Prefix freedom, unique decipherability and the Kraft inequality remain separate predicates.
5. Keep every ambiguous parse or certificate. A unique decision is limited to the declared finite codebook.

## Failure and repair

The `ambiguity-witness-invalid.json` example contains an empty codeword and must exit two with `executed: false`. Keep this failed subject at zero credit. Restore only the codewords field from the frozen request, execute the repaired copy separately, and compare the full response. Unknown operations also reject. Never overwrite a sealed request, prior result or negative record.

## Limits and rollback

Finite synthetic same-owner evidence; no independent reproduction, empirical, production, identity, professional, legal, cultural, Maori authority, consciousness, personhood or Stage 20 claim. Mathematical decoding does not authorize real identity, custody, access or archive changes. Missing observations remain open. Revert only unsealed caller-owned changes after examining their exact diff. These guides neither install hooks nor contact any task.
