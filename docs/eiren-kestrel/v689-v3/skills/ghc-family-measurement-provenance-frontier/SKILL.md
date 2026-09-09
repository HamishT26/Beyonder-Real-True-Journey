---
name: ghc-family-measurement-provenance-frontier
description: Validate append-ordered measurement-evidence digests and report roots and frontier nodes without claiming independent review.
---

# ghc-family-measurement-provenance-frontier

Use `ghc_family_missingness_provenance.py` for the declared `provenance_frontier` operation.

1. Preserve every event and require exactly `id`, `parents`, and lowercase digest fields.
2. Resolve parents only against prior events; reject missing, duplicate, or forward parents.
3. Report roots, terminal frontier nodes, and submitted topological order without altering the ledger.
4. Retain malformed events at zero success credit and keep byte correspondence separate from authorship or trust.
5. Stop before real measurement, professional action, participant use, publication, legal or cultural interpretation, Maori authority, identity issuance, deployment, or Stage 20 promotion.

This skill supports synthetic same-owner software evidence only. It does not establish empirical confirmation, qualification, production readiness, complete privacy or accessibility, exhaustive security, independent reproduction, consciousness, personhood, Theory-of-Everything proof, or Stage 20 authority.
