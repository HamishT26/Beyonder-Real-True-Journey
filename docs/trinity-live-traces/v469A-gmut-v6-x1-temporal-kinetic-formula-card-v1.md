# v469A GMUT v6 x1 Temporal Kinetic Formula Card

Classification: `evidence`

This artifact drafts explicit temporal kinetic formula cards under the selected `x0=ct` rehearsal branch. It is formula-card scaffolding only.

## Branch Rule

- Active rehearsal: `x0=ct`
- Translation hold: `x0=t`
- Conversion: `partial_0 Psi = c^-1 partial_t Psi`

## Formula Cards

`x0_ct_temporal_kinetic_card`

- Required fields: coordinate branch, metric signature, action sign, derivative conversion, temporal contraction, spatial contraction, `V(Psi)` symbolic hold, source anchor.
- Temporal contraction row: `g^00 (partial_0 Psi)^2 = g^00 c^-2 (partial_t Psi)^2`.
- Status: `HOLD_OPEN_GAP`
- Reason: metric signature, action sign, scalar unit policy, and source anchors remain incomplete.

`partial_0_conversion_row`

- Required fields: `x0_dimension:length`, `time_coordinate:t`, `conversion_factor:1/c`, derivative basis, c-factor location, allowed branch.
- Status: `PASS_ROW_READY_FOR_REVIEW_ONLY`
- Reason: conversion is explicit, but this is not an EOM derivation or gate closure.

`scalar_kinetic_split_row`

- Required fields: time term, spatial term, inverse metric references, lapse/shift policy, `V(Psi)` symbolic hold, unit policy status.
- Status: `HOLD_OPEN_GAP`
- Reason: unit policy and boundary class are not fixed.

Invalid conditions include missing `partial_0=(1/c)partial_t` under `x0=ct`, mixing `x0=ct` and `x0=t` without a translation appendix, or claiming EOM derivation, fixture pass, or dimensional/SI gate closure.
