# v463A GMUT v2 SI Natural Unit Bridge Blocker

Generated UTC: 2026-05-29T12:48:47Z
Generated NZ: 2026-05-30T00:48:47+12:00

## Status

The SI/natural-unit bridge is required and not completed.

## Rule

Any natural-unit scalar-route quantity intended for public physical interpretation must state its SI bridge dependencies or remain fixture-only.

## Dependencies

- `c`: speed-of-light conversion dependency; source-backed by NIST, not applied to GMUT rows.
- `hbar`: action conversion dependency from `h / 2 pi`; `h` is source-backed by NIST, row conversion not expanded in v2.
- `stress_energy_SI_target`: energy-density or pressure target for `T` rows; named but not derived.
- `coordinate_units`: derivative operator dimension; not selected.

## Boundary

Allowed: v2 identifies missing conversion dependencies.

Forbidden: v2 completes the SI bridge, closes dimensional consistency, or validates the scalar sector.
