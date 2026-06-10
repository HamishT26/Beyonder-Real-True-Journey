# v470 THOS v7 x6 Reason-Code Registry

This registry records the reason-code surface added to the local THOS publication guard during `v470_THOS_v7_x6`.

## Manifest Contract

Manifest failures now emit stable codes for missing or unreadable manifests, invalid schemas, phase mismatch, non-local validator metadata, connector or mutation boundary drift, GMUT gate-effect drift, missing refs, malformed refs, duplicate IDs, invalid paths, out-of-phase paths, duplicate normalized paths, case-colliding paths, non-JSON assertion artifacts, invalid roles, invalid expectation/status combinations, invalid coverage tokens, path-list mismatch, and closed-world stray assertions.

## Path-List Contract

Path-list failures now emit stable codes for unreadable JSON, invalid schema, phase mismatch, missing path arrays, and invalid path shapes.

## Assertion Artifact Contract

Assertion-artifact failures now emit stable codes for missing assertion sets, manifest-listed artifacts missing from the phase set, unreadable assertion JSON, local/non-mutating boundary drift, expected-status mismatch, report-input mismatch, expected-negative unexpected pass, expected failure token mismatch, positive assertion dirtiness, coverage gaps, missing positive assertions, and missing expected-negative assertions.

## Boundary

These codes improve local refusal traceability. They do not certify safety, authorize connector writes, authorize cleanup, publish externally, validate GMUT, or close any GMUT gate.
