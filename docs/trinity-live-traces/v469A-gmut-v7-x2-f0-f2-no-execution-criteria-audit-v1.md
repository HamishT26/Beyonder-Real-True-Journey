# v469A GMUT v7 x2 F0/F2 No-Execution Criteria Audit

Classification: `advisory`

Execution status: `not_run`

## Why F0/F2 Stayed Unrun

The source refresh improved the criteria for future fixtures, but it did not make execution safe. F0/F2 still lacks the convention and coefficient substrate needed to interpret an output.

The main blockers are:

- metric signature held,
- action sign held,
- coefficient/SI dictionary incomplete,
- `V(Psi)` symbolic,
- `T_Psi` template-only,
- `B_Psi` quarantined,
- null-switch expected output missing,
- baseline comparator expected output missing,
- fifth-force/equivalence mapping missing.

## Refined Acceptance Criteria

| Criterion | Minimum Requirement | Current Status |
| --- | --- | --- |
| Fixture manifest exists | Machine-readable manifest listing fields, coefficients, units, source anchors, and branch labels. | `missing` |
| Null switch declared | All GMUT-only couplings have named zero/null settings and expected recovery equations. | `partial_open` |
| Baseline expected output declared | Comparator equations are named before execution. | `missing` |
| Dimensional guard | Fixture rejects hidden `c=1` and missing SI exponents. | `missing` |
| Fifth-force guard | Matter-coupling parameters map to MICROSCOPE/Eot-Wash-style constraint rows. | `missing` |
| Consciousness proxy guard | Proxy fields cannot feed physics equations without independent operational definition. | `policy_only` |

## Safe Next Step

`v469A_GMUT_v8_x1` may draft an F0/F2 fixture manifest and run dry lint against the manifest. It should not run a physics fixture unless the convention bundle and expected outputs are already present.

## Forbidden Moves

Do not count fixture existence as gate closure. Do not claim null recovery from symbolic zeroing. Do not claim baseline recovery unless a named comparator output is recovered under a declared convention.
