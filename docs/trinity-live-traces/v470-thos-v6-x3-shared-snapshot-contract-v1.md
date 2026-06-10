# v470 THOS v6 x3 Shared Snapshot Contract

This contract defines how generated exports, visualizations, sibling synthesis, and handoffs must refer to the same phase package without drifting into separate row universes.

## Required Snapshot Fields

Every future manifest-style receipt should preserve snapshot ID, phase slug, source head, artifact count, artifact paths, SHA-256 values, family counts, row universe ID, GMUT gate effect, connector-write status, and mutation status.

## Row Universe Rule

If the visualization, sibling synthesis, exception export, and handoff talk about the same package, they must either consume the same row universe or explicitly state why they are schematic/local-only. v6 x2 currently uses a local embedded visualization row set, so v6 x4 should either derive that data from exported JSON or record the embedded rows as their own named universe.

## Boundaries

- Manifest existence is not cloud publication.
- Checksum presence is not correctness proof.
- THOS workflow readiness is not GMUT validation.
- Advisory synthesis is not publication authority.
