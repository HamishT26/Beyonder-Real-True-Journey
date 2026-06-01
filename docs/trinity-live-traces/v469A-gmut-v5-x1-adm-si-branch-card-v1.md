# v469A GMUT v5 x1 ADM/SI Branch Card

Classification: `evidence`

This artifact records a stricter convention card after `v469A_GMUT_v4_x2` found that bare `dt d3x` is not sufficient for the ADM route. It does not close the dimensional/SI gate.

## Working Rehearsal Branch

`x0 = c t` is selected as the rehearsal branch only.

- `dx0 = c dt`
- `partial_0 = (1/c) partial_t`
- Coordinates are treated as length-like.
- Metric components, lapse `N`, spatial metric `h_ij`, and `sqrt(h)` are treated as dimensionless unless a later artifact explicitly redefines them.
- A dimensionless shift variable is preferred for this branch.

The `x0 = t` branch remains held as a translation appendix. It can be valid, but it must not be mixed with `x0 = ct` rows until a separate c-factor allocation card specifies where each power of `c` sits.

## ADM/SI Row

Route A may rehearse the ADM action row as:

```text
S_ADM ~ (c^4/G) integral N sqrt(h) R_ADM dt d3x
```

The SI bookkeeping row is:

```text
[c^4/G]       = kg m s^-2
[dt d3x]      = s m^3
[N sqrt(h)]   = 1 under the selected rehearsal branch
[R_ADM]       = m^-2
product       = kg m^2 s^-1 = J s
```

This is `row_ready_for_rehearsal_not_gate_closure`.

## Open Gaps

- The exact curvature bundle must still specify whether it uses four-dimensional `R` or the ADM combination of spatial curvature, extrinsic curvature, and boundary/divergence terms.
- The action sign and normalization remain conventional until tied to a source-authority card.
- This branch card does not derive the scalar EOM, `T_Psi`, conservation, null recovery, baseline recovery, fifth-force safety, or consciousness proxy validity.

Gate status: all six GMUT gates remain open.
