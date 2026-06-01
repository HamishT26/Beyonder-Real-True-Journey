# v468A THOS v6 x2 Fixture Results

Fixture execution passed through `scripts/validate_thos_phase_schema.py` and generated `v468A-thos-v6-x2-fixture-results-v1.json`.

Expected cases:

- `pass_manifest`: valid THOS manifest shape with open GMUT boundary and remote equality wording.
- `fail_missing_upstream`: missing required live upstream head.
- `fail_bad_head`: non-hash local head.
- `fail_boundary_closed`: forbidden boundary state under schema const.
- `fail_extra_property`: rejected by `additionalProperties: false`.

Boundary: fixture success proves only that the schema accepts and rejects the intended shapes. It does not replace live git verification, repo-root path checks, publication review, or GMUT gate evidence.

Result: PASS. The valid fixture passed; missing upstream head, bad local head, closed GMUT boundary, and extra-property fixtures failed as expected.
