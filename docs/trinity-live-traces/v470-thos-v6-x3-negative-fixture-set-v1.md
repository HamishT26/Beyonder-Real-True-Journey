# v470 THOS v6 x3 Negative Fixture Set

This fixture set defines five fail-closed cases for the next THOS checker expansion.

## Fixtures

- Duplicate join in the same snapshot.
- Missing source provenance.
- Unknown status enum.
- Non-none GMUT gate effect.
- Manifest checksum mismatch.

## Current Execution Status

The fixture set is defined but not executed in v6 x3. That is intentional: v6 x3 is adding the manifest and contract layer. v6 x4 should execute these cases or add a checker capable of failing them deterministically.

## Boundary

These fixtures protect workflow integrity only. They do not test GMUT equations, null recovery, dimensional/SI consistency, conservation, baseline recovery, fifth-force/equivalence constraints, or consciousness measurement.
