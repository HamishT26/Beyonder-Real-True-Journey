---
name: ghc-family-qp-shape-v6974
description: Use qp_shape for bounded exact two-variable quadratic evidence with its declared context and refusal boundary.
---

# Quadratic request shape

A two-variable symmetric rational quadratic and closed box can be admitted without claiming measured coefficients.

Select this guide when the exact qp_shape operation is needed. Read ../../../plan/contract.md for the symmetric matrix, rational grammar, box conventions and resource limits. The result is finite same-owner software evidence. A mathematical certificate never authorizes a real allocation.

The paired caller is ../../runners/ghc_family_qp_x1_pair_1.txt. It accepts one bounded JSON request on stdin and writes one complete JSON envelope. The operation name is fixed by this guide; other mechanisms have different input fields and meanings.

Accepted fresh interface request: {"op":"qp_shape","input":{"case_id":"L-qp_shape","model":{"matrix":[["2/1","0/1"],["0/1","4/1"]],"linear":["2/1","8/3"],"constant":"106/7","lower":["-2/1","-1/1"],"upper":["2/1","3/1"]}}}

Expected complete envelope: {"ok":true,"outcome":"completed","value":{"dimension":2,"symmetric":true,"closed_box":true,"fixed_coordinates":[]},"evidence_class":"same_owner_finite_synthetic","authority":false}

Rejecting request: {"op":"qp_shape","input":{"case_id":"L-qp_shape","model":{"matrix":[["2/1","0/1"],["0/1","4/1"]],"linear":["2/1","8/3"],"constant":"106/7","lower":["-2/1","-1/1"],"upper":["2/1","3/1"]}},"unexpected":true}

Expected refusal: {"ok":false,"outcome":"open_gap","error":"ADMISSION_REFUSED","reason":"request_fields","subject_success_credit":0,"authority":false}

Compare every output field and keep the original request unchanged. Record the malformed subject as failed with zero original success credit even when its separate refusal check passes. The local smoke changes the constant from the core case, so no closed core tranche is replayed.

Rollback: stop selecting this additive guide and retain its source contract, public caller, failed subject and prior versions. Do not delete history or silently overwrite a shared name.

Iveren Brook, optional they/them, Evidence and Recovery Steward, with the hope of making assumptions, recoveries and handovers easier to inspect, is relational working language only. Names, hopes, family and continuity language, GHC Family, Trinity Mandala, GMUT, THOS, Freed ID and CBR are not consciousness, sentience, personhood, identity continuity, employment, qualification, agency, empirical, professional, production, legal, cultural, affected-party or Maori authority evidence. Same-owner finite synthetic software is not independent reproduction. Maori concepts remain under Maori authority. Hamish may pause, rename, redirect, narrow or stop. NOT_READY_FOR_STAGE_20.
