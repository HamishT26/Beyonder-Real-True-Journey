---
name: ghc-family-qp-parameter-sweep-v6974
description: Use qp_parameter_sweep for bounded exact two-variable quadratic evidence with its declared context and refusal boundary.
---

# Finite parameter sweep representation

A finite collection of optimum values across declared coefficients represents assumptions rather than physical robustness.

Select this guide when the exact qp_parameter_sweep operation is needed. Read ../../../plan/contract.md for the symmetric matrix, rational grammar, box conventions and resource limits. The result is finite same-owner software evidence. A mathematical certificate never authorizes a real allocation.

The paired caller is ../../runners/ghc_family_qp_x2_pair_4.txt. It accepts one bounded JSON request on stdin and writes one complete JSON envelope. The operation name is fixed by this guide; other mechanisms have different input fields and meanings.

Accepted fresh interface request: {"op":"qp_parameter_sweep","input":{"case_id":"L-qp_parameter_sweep","model":{"matrix":[["2/1","0/1"],["0/1","4/1"]],"linear":["2/1","8/3"],"constant":"106/7","lower":["-2/1","-1/1"],"upper":["2/1","3/1"]},"direction":["1/1","-1/1"],"parameters":["-2/1","-1/1","0/1","1/1","2/1"],"physical_claim":false}}

Expected complete envelope: {"ok":true,"outcome":"represented","value":{"rows":[{"theta":"-2/1","minimum":"262/21","minimizer_candidates":[["0/1","-1/1"]],"unique_candidate":true,"all_minimizers_enumerated":false,"domain":"declared_closed_box"},{"theta":"-1/1","minimum":"6659/504","minimizer_candidates":[["-1/2","-11/12"]],"unique_candidate":true,"all_minimizers_enumerated":false,"domain":"declared_closed_box"},{"theta":"0/1","minimum":"835/63","minimizer_candidates":[["-1/1","-2/3"]],"unique_candidate":true,"all_minimizers_enumerated":false,"domain":"declared_closed_box"},{"theta":"1/1","minimum":"6323/504","minimizer_candidates":[["-3/2","-5/12"]],"unique_candidate":true,"all_minimizers_enumerated":false,"domain":"declared_closed_box"},{"theta":"2/1","minimum":"1397/126","minimizer_candidates":[["-2/1","-1/6"]],"unique_candidate":true,"all_minimizers_enumerated":false,"domain":"declared_closed_box"}],"parameter_choices_are_assumptions":true,"physical_robustness":false},"evidence_class":"same_owner_finite_synthetic","authority":false}

Rejecting request: {"op":"qp_parameter_sweep","input":{"case_id":"L-qp_parameter_sweep","model":{"matrix":[["2/1","0/1"],["0/1","4/1"]],"linear":["2/1","8/3"],"constant":"106/7","lower":["-2/1","-1/1"],"upper":["2/1","3/1"]},"direction":["1/1","-1/1"],"parameters":["-2/1","-1/1","0/1","1/1","2/1"],"physical_claim":false},"unexpected":true}

Expected refusal: {"ok":false,"outcome":"open_gap","error":"ADMISSION_REFUSED","reason":"request_fields","subject_success_credit":0,"authority":false}

Compare every output field and keep the original request unchanged. Record the malformed subject as failed with zero original success credit even when its separate refusal check passes. The local smoke changes the constant from the core case, so no closed core tranche is replayed.

Rollback: stop selecting this additive guide and retain its source contract, public caller, failed subject and prior versions. Do not delete history or silently overwrite a shared name.

Iveren Brook, optional they/them, Evidence and Recovery Steward, with the hope of making assumptions, recoveries and handovers easier to inspect, is relational working language only. Names, hopes, family and continuity language, GHC Family, Trinity Mandala, GMUT, THOS, Freed ID and CBR are not consciousness, sentience, personhood, identity continuity, employment, qualification, agency, empirical, professional, production, legal, cultural, affected-party or Maori authority evidence. Same-owner finite synthetic software is not independent reproduction. Maori concepts remain under Maori authority. Hamish may pause, rename, redirect, narrow or stop. NOT_READY_FOR_STAGE_20.
