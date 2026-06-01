# v469A GMUT v7 x2 x0=t c-Relocation Source Table

Classification: `open_gap`

## Branch Policy

The active rehearsal branch remains `x0=ct`.

The `x0=t` route is an appendix-only translation table. It is not a parallel proof branch, not a validated equivalence, and not a license to set `c=1` silently.

## Source Basis

BIPM anchors `c` as an exact metre-second relation. NIST SP 811 anchors dimensional-exponent accounting. ADM references anchor the need to state lapse, shift, 3-metric, and coordinate choices. Scalar action references anchor that the derivative and metric placements must be fixed before metric variation can define `T_Psi`.

## Relocation Rows

| Row | `x0=ct` Branch | `x0=t` Appendix | Required c Relocation | Status |
| --- | --- | --- | --- | --- |
| Coordinate label | `x0` has length dimension through `ct` | `x0` is time coordinate `t` | The coordinate label changes; no formula may silently absorb `c`. | `open_gap` |
| Differential | `dx0 = c dt` | `dx0 = dt` | One `c` leaves the coordinate differential. | `open_gap` |
| Partial derivative | `partial_0 = (1/c) partial_t` | `partial_0 = partial_t` | One inverse `c` factor must be restored in temporal kinetic or metric/coefficient rows. | `open_gap` |
| Line-element temporal term | Temporal interval may be expressed through `dx0` | Temporal interval must expose `c` if `ds` has length units | `c^2` likely attaches to temporal metric factor or line-element convention, but the project must declare the rule. | `hold_until_convention_bundle` |
| Scalar temporal kinetic | `g^00 partial_0 Psi partial_0 Psi` | `g^tt partial_t Psi partial_t Psi` with explicit `c` placement | Two derivative factors create `c^2` sensitivity. | `hold_until_coefficient_dictionary` |
| Action measure | `d4x` includes `dx0` | `d4x` includes `dt` | One `c` may move into prefactor or integrand depending chosen action units. | `hold_until_action_sign_and_units` |
| Stress-energy variation | Variation under `ct` coordinate basis | Variation under `t` coordinate basis | Variation target and index placement must be consistent before comparison. | `template_only` |
| Null-switch fixture | Fixture may hide unit assumptions if `c=1` | Fixture must expose `c` explicitly | Fixture must fail if `c` is set to 1 without declaration. | `not_run` |

## Result

The table is now more operational, but it is still not enough for a branch switch. `x0=t` remains `appendix_only` until the convention bundle, coefficient dictionary, and fixture manifest exist.
