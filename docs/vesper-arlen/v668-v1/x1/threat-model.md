# Vesper Arlen v668-v1 threat model

## Protected assets

The phase protects exact source anchors, strict x1-before-x2 lifecycle separation, retained failures, owner-only Git state, committed manifests, privacy boundaries, the single-success validation credit, and the single exact-title successor edge.

## Threats and controls

1. Causal-order corruption: cycles, missing dependencies, duplicate identifiers, and decreasing source sequences are rejecting fixtures.
2. Replay duplication: accepted event identifiers are idempotent and duplicates are quarantined with zero second effect.
3. Checkpoint corruption: altered leaves must change the Merkle root; a root mismatch fails closed.
4. Rollback overclaim: compensation remains a new event and never erases the original or claims external reversal.
5. Queue starvation: stop precedence is explicit and overflow cannot be silent.
6. Schema loss: unknown incompatible fields are quarantined and round-trip loss is a failure.
7. Privacy leakage: raw task identifiers, private routes, credentials, keys, transcripts, session streams, private app state, and private absolute paths are prohibited.
8. Manifest drift: ignored runtime artifacts are excluded; exact Git blobs are the final replay domain.
9. Validation-credit inflation: a failed aggregate receives zero success credit and a successful aggregate cannot be replayed.
10. Authority smuggling: real professional, production, safety, labor, legal, cultural, Maori, affected-party, and Stage 20 actions remain exact-gated.

## Residual limits

The controls are owner-local software and documentation evidence only. They are not exhaustive security, complete privacy or accessibility assurance, production certification, professional validation, legal review, cultural ratification, Maori authority, independent reproduction, AGI or ASI evidence, consciousness or personhood evidence, Theory-of-Everything proof, or Stage 20 authority.
